################################################################################
# AnimalShelter.py
#
# Enhanced CS 499 ePortfolio Version
#
# Description:
#     Provides a reusable Python data-access layer for the Austin Animal Center
#     (AAC) MongoDB database. The class supports validated CRUD operations,
#     server-side sorting and pagination, bulk inserts, aggregation, indexing,
#     optional Pandas DataFrame output, connection health checks, and clean
#     resource management.
#
# Database Defaults:
#     - Database: aac
#     - Collection: animals
#     - Host: localhost
#     - Port: 27017
#     - Authentication source: admin
#
# Security / Configuration:
#     Credentials may be passed to the constructor or supplied through these
#     environment variables:
#         MONGO_USERNAME
#         MONGO_PASSWORD
#         MONGO_HOST
#         MONGO_PORT
#         MONGO_AUTH_SOURCE
#         MONGO_DB_NAME
#         MONGO_COLLECTION_NAME
#         MONGO_URI                 (optional full URI override)
#
# Dependencies:
#     Required: pymongo
#     Optional: pandas (only for read_dataframe())
#
# Author: Michael Langille
# Course: CS 499 Computer Science Capstone
################################################################################

from __future__ import annotations

import logging
import os
from typing import Any, Dict, Iterable, List, Mapping, Optional, Sequence, Tuple
from urllib.parse import quote_plus

from pymongo import ASCENDING, DESCENDING, MongoClient
from pymongo.collection import Collection
from pymongo.database import Database
from pymongo.errors import PyMongoError


LOGGER = logging.getLogger(__name__)

# Type aliases make method signatures easier to read and maintain.
Document = Dict[str, Any]
Query = Mapping[str, Any]
Projection = Mapping[str, int]
SortSpec = Sequence[Tuple[str, int]]


class AnimalShelter:
    """MongoDB data-access class for the AAC ``animals`` collection.

    The class intentionally keeps the original ``create``, ``read``, ``update``,
    and ``delete`` method names so code written for the earlier CS-340 project
    remains compatible while gaining stronger validation, security, performance,
    and analytical capabilities.
    """

    DEFAULT_INDEXES: Tuple[Tuple[Tuple[str, int], ...], ...] = (
        (("animal_id", ASCENDING),),
        (("animal_type", ASCENDING),),
        (("breed", ASCENDING),),
        (("outcome_type", ASCENDING),),
        (("animal_type", ASCENDING), ("breed", ASCENDING)),
    )

    ALLOWED_UPDATE_OPERATORS = frozenset(
        {
            "$set",
            "$unset",
            "$inc",
            "$mul",
            "$min",
            "$max",
            "$rename",
            "$currentDate",
            "$push",
            "$addToSet",
            "$pull",
        }
    )

    def __init__(
        self,
        username: Optional[str] = None,
        password: Optional[str] = None,
        host: Optional[str] = None,
        port: Optional[int] = None,
        auth_source: Optional[str] = None,
        db_name: Optional[str] = None,
        collection_name: Optional[str] = None,
        tls: bool = False,
        connection_uri: Optional[str] = None,
        server_selection_timeout_ms: int = 5000,
        auto_create_indexes: bool = True,
    ) -> None:
        """Connect to MongoDB and select the requested database/collection.

        Constructor arguments take precedence over environment variables. When
        username/password are omitted, the class can connect to a local MongoDB
        instance that does not require authentication.

        Args:
            username: MongoDB username.
            password: MongoDB password.
            host: MongoDB host name or IP address.
            port: MongoDB port.
            auth_source: Database used to authenticate the MongoDB user.
            db_name: Target database name.
            collection_name: Target collection name.
            tls: Enable TLS for the MongoDB connection.
            connection_uri: Optional complete MongoDB URI. If supplied, it takes
                precedence over host/port/credential URI construction.
            server_selection_timeout_ms: Connection verification timeout.
            auto_create_indexes: Create commonly queried indexes at startup.

        Raises:
            ValueError: If configuration values are invalid.
            RuntimeError: If MongoDB cannot be reached or initialized.
        """
        self._closed = False

        resolved_host = host or os.getenv("MONGO_HOST", "localhost")
        resolved_port = self._resolve_port(port)
        resolved_auth_source = auth_source or os.getenv("MONGO_AUTH_SOURCE", "admin")
        resolved_db_name = db_name or os.getenv("MONGO_DB_NAME", "aac")
        resolved_collection = collection_name or os.getenv(
            "MONGO_COLLECTION_NAME", "animals"
        )
        resolved_username = username if username is not None else os.getenv("MONGO_USERNAME")
        resolved_password = password if password is not None else os.getenv("MONGO_PASSWORD")
        resolved_uri = connection_uri or os.getenv("MONGO_URI")

        self._validate_configuration(
            resolved_host,
            resolved_port,
            resolved_db_name,
            resolved_collection,
            server_selection_timeout_ms,
        )

        if bool(resolved_username) != bool(resolved_password):
            raise ValueError(
                "MongoDB username and password must either both be provided or both be omitted."
            )

        if resolved_uri is None:
            resolved_uri = self._build_uri(
                host=resolved_host,
                port=resolved_port,
                username=resolved_username,
                password=resolved_password,
                auth_source=resolved_auth_source,
            )

        try:
            self.client: MongoClient = MongoClient(
                resolved_uri,
                tls=tls,
                serverSelectionTimeoutMS=server_selection_timeout_ms,
                appname="CS499-AnimalShelter",
            )

            # PyMongo connects lazily. ping forces an immediate health check so a
            # bad host, stopped MongoDB service, or invalid credential is detected
            # during initialization instead of during the first CRUD operation.
            self.client.admin.command("ping")

            self.database: Database = self.client[resolved_db_name]
            self.collection: Collection = self.database[resolved_collection]

            if auto_create_indexes:
                self.ensure_indexes()

            LOGGER.info(
                "Connected to MongoDB database '%s', collection '%s'.",
                resolved_db_name,
                resolved_collection,
            )
        except PyMongoError as exc:
            self.close()
            raise RuntimeError(f"Failed to connect to MongoDB: {exc}") from exc

    # ------------------------------------------------------------------
    # Connection and configuration helpers
    # ------------------------------------------------------------------
    @staticmethod
    def _resolve_port(port: Optional[int]) -> int:
        if port is not None:
            return port
        env_port = os.getenv("MONGO_PORT", "27017")
        try:
            return int(env_port)
        except ValueError as exc:
            raise ValueError("MONGO_PORT must be a valid integer.") from exc

    @staticmethod
    def _validate_configuration(
        host: str,
        port: int,
        db_name: str,
        collection_name: str,
        timeout_ms: int,
    ) -> None:
        if not isinstance(host, str) or not host.strip():
            raise ValueError("MongoDB host must be a non-empty string.")
        if not isinstance(port, int) or not 1 <= port <= 65535:
            raise ValueError("MongoDB port must be an integer between 1 and 65535.")
        if not isinstance(db_name, str) or not db_name.strip():
            raise ValueError("Database name must be a non-empty string.")
        if not isinstance(collection_name, str) or not collection_name.strip():
            raise ValueError("Collection name must be a non-empty string.")
        if not isinstance(timeout_ms, int) or timeout_ms <= 0:
            raise ValueError("server_selection_timeout_ms must be a positive integer.")

    @staticmethod
    def _build_uri(
        host: str,
        port: int,
        username: Optional[str],
        password: Optional[str],
        auth_source: str,
    ) -> str:
        """Build a MongoDB URI while safely escaping credential characters."""
        if username and password:
            user = quote_plus(username)
            secret = quote_plus(password)
            auth_db = quote_plus(auth_source)
            return f"mongodb://{user}:{secret}@{host}:{port}/?authSource={auth_db}"
        return f"mongodb://{host}:{port}/"

    def _ensure_open(self) -> None:
        if self._closed:
            raise RuntimeError("AnimalShelter connection has already been closed.")

    def ping(self) -> bool:
        """Return ``True`` when the MongoDB server responds to a health check."""
        self._ensure_open()
        try:
            self.client.admin.command("ping")
            return True
        except PyMongoError as exc:
            LOGGER.error("MongoDB ping failed: %s", exc)
            return False

    def close(self) -> None:
        """Close the MongoDB client safely. Calling close more than once is safe."""
        client = getattr(self, "client", None)
        if client is not None and not self._closed:
            client.close()
        self._closed = True

    def __enter__(self) -> "AnimalShelter":
        self._ensure_open()
        return self

    def __exit__(self, exc_type: Any, exc_value: Any, traceback: Any) -> None:
        self.close()

    # ------------------------------------------------------------------
    # Validation helpers
    # ------------------------------------------------------------------
    @staticmethod
    def _is_nonempty_mapping(value: Any) -> bool:
        return isinstance(value, Mapping) and bool(value)

    @staticmethod
    def _validate_document(document: Any) -> bool:
        """Reject empty documents and top-level keys that look like operators."""
        if not isinstance(document, Mapping) or not document:
            return False
        return all(isinstance(key, str) and not key.startswith("$") for key in document)

    @classmethod
    def _normalize_update(cls, update_values: Query) -> Document:
        """Convert plain field/value updates to ``$set`` and validate operators."""
        if not cls._is_nonempty_mapping(update_values):
            raise ValueError("update_values must be a non-empty mapping.")

        has_operator = any(str(key).startswith("$") for key in update_values)
        if not has_operator:
            if not cls._validate_document(update_values):
                raise ValueError("Update field names must be valid strings.")
            return {"$set": dict(update_values)}

        operators = set(update_values.keys())
        if not all(isinstance(key, str) and key.startswith("$") for key in operators):
            raise ValueError("Do not mix MongoDB update operators with plain field names.")

        unsupported = operators - cls.ALLOWED_UPDATE_OPERATORS
        if unsupported:
            raise ValueError(
                "Unsupported update operator(s): " + ", ".join(sorted(unsupported))
            )

        return dict(update_values)

    @staticmethod
    def _normalize_sort(sort: Optional[SortSpec]) -> Optional[List[Tuple[str, int]]]:
        if sort is None:
            return None

        normalized: List[Tuple[str, int]] = []
        for item in sort:
            if not isinstance(item, (tuple, list)) or len(item) != 2:
                raise ValueError("Each sort item must be a (field, direction) pair.")
            field, direction = item
            if not isinstance(field, str) or not field:
                raise ValueError("Sort field names must be non-empty strings.")
            if direction not in (ASCENDING, DESCENDING, 1, -1):
                raise ValueError("Sort direction must be 1/ASCENDING or -1/DESCENDING.")
            normalized.append((field, int(direction)))
        return normalized

    # ------------------------------------------------------------------
    # Database indexes
    # ------------------------------------------------------------------
    def ensure_indexes(self) -> List[str]:
        """Create indexes that support common AAC queries efficiently.

        No unique constraint is placed on ``animal_id`` because an animal may
        legitimately appear in multiple outcome records in the source dataset.
        """
        self._ensure_open()
        index_names: List[str] = []
        try:
            for keys in self.DEFAULT_INDEXES:
                index_names.append(self.collection.create_index(list(keys)))
            return index_names
        except PyMongoError as exc:
            LOGGER.error("Index creation failed: %s", exc)
            return index_names

    # ------------------------------------------------------------------
    # CREATE
    # ------------------------------------------------------------------
    def create(self, document: Document) -> bool:
        """Insert one validated document and return whether MongoDB acknowledged it."""
        self._ensure_open()
        if not self._validate_document(document):
            LOGGER.warning("Create rejected: document must be a non-empty valid mapping.")
            return False

        try:
            result = self.collection.insert_one(dict(document))
            return bool(result.acknowledged)
        except PyMongoError as exc:
            LOGGER.error("Create failed: %s", exc)
            return False

    def create_many(self, documents: Iterable[Document], ordered: bool = False) -> int:
        """Insert multiple valid documents and return the number inserted.

        Args:
            documents: Iterable of animal documents.
            ordered: When False, MongoDB can continue after an individual insert
                failure and can optimize bulk execution.
        """
        self._ensure_open()
        docs = [dict(doc) for doc in documents if self._validate_document(doc)]
        if not docs:
            return 0

        try:
            result = self.collection.insert_many(docs, ordered=ordered)
            return len(result.inserted_ids)
        except PyMongoError as exc:
            LOGGER.error("Bulk create failed: %s", exc)
            return 0

    # ------------------------------------------------------------------
    # READ
    # ------------------------------------------------------------------
    def read(
        self,
        query: Optional[Query] = None,
        projection: Optional[Projection] = None,
        limit: Optional[int] = None,
        *,
        sort: Optional[SortSpec] = None,
        skip: int = 0,
    ) -> List[Document]:
        """Return documents matching a MongoDB query.

        Sorting, skipping, limiting, and projection are performed by MongoDB so
        unnecessary records are not loaded into Python memory.
        """
        self._ensure_open()

        if query is not None and not isinstance(query, Mapping):
            raise ValueError("query must be a mapping or None.")
        if projection is not None and not isinstance(projection, Mapping):
            raise ValueError("projection must be a mapping or None.")
        if not isinstance(skip, int) or skip < 0:
            raise ValueError("skip must be a non-negative integer.")
        if limit is not None and (not isinstance(limit, int) or limit < 0):
            raise ValueError("limit must be a non-negative integer or None.")

        normalized_sort = self._normalize_sort(sort)

        try:
            cursor = self.collection.find(
                dict(query) if query is not None else {},
                dict(projection) if projection is not None else None,
            )

            if normalized_sort:
                cursor = cursor.sort(normalized_sort)
            if skip:
                cursor = cursor.skip(skip)
            if limit:
                cursor = cursor.limit(limit)

            return list(cursor)
        except PyMongoError as exc:
            LOGGER.error("Read failed: %s", exc)
            return []

    def read_page(
        self,
        query: Optional[Query] = None,
        *,
        page: int = 1,
        page_size: int = 25,
        projection: Optional[Projection] = None,
        sort: Optional[SortSpec] = None,
    ) -> Dict[str, Any]:
        """Return a page of results plus pagination metadata."""
        if not isinstance(page, int) or page < 1:
            raise ValueError("page must be an integer greater than or equal to 1.")
        if not isinstance(page_size, int) or not 1 <= page_size <= 500:
            raise ValueError("page_size must be between 1 and 500.")

        filter_doc = dict(query) if query is not None else {}
        total = self.count(filter_doc)
        skip = (page - 1) * page_size
        items = self.read(
            filter_doc,
            projection,
            page_size,
            sort=sort,
            skip=skip,
        )
        total_pages = (total + page_size - 1) // page_size if total else 0

        return {
            "items": items,
            "page": page,
            "page_size": page_size,
            "total_items": total,
            "total_pages": total_pages,
        }

    def count(self, query: Optional[Query] = None) -> int:
        """Return the number of documents matching ``query``."""
        self._ensure_open()
        if query is not None and not isinstance(query, Mapping):
            raise ValueError("query must be a mapping or None.")
        try:
            return int(self.collection.count_documents(dict(query or {})))
        except PyMongoError as exc:
            LOGGER.error("Count failed: %s", exc)
            return 0

    def read_dataframe(
        self,
        query: Optional[Query] = None,
        projection: Optional[Projection] = None,
        limit: Optional[int] = None,
        *,
        sort: Optional[SortSpec] = None,
        skip: int = 0,
        drop_mongo_id: bool = True,
    ) -> Any:
        """Return query results as a Pandas DataFrame for vectorized analysis.

        Pandas is imported only when this method is used, so it remains an
        optional dependency for applications that only need CRUD operations.
        """
        try:
            import pandas as pd
        except ImportError as exc:
            raise RuntimeError(
                "read_dataframe() requires pandas. Install it with: pip install pandas"
            ) from exc

        records = self.read(
            query=query,
            projection=projection,
            limit=limit,
            sort=sort,
            skip=skip,
        )
        frame = pd.DataFrame.from_records(records)
        if drop_mongo_id and "_id" in frame.columns:
            frame = frame.drop(columns=["_id"])
        return frame

    # ------------------------------------------------------------------
    # UPDATE
    # ------------------------------------------------------------------
    def update(
        self,
        query: Query,
        update_values: Query,
        many: bool = False,
    ) -> int:
        """Update one or many matching documents and return modified count.

        Empty filters are intentionally rejected to reduce the chance of an
        accidental collection-wide update.
        """
        self._ensure_open()
        if not self._is_nonempty_mapping(query):
            LOGGER.warning("Update rejected: query must be a non-empty mapping.")
            return 0

        try:
            update_doc = self._normalize_update(update_values)
            result = (
                self.collection.update_many(dict(query), update_doc)
                if many
                else self.collection.update_one(dict(query), update_doc)
            )
            return int(result.modified_count)
        except (ValueError, PyMongoError) as exc:
            LOGGER.error("Update failed: %s", exc)
            return 0

    # ------------------------------------------------------------------
    # DELETE
    # ------------------------------------------------------------------
    def delete(self, query: Query, many: bool = False) -> int:
        """Delete one or many matching documents and return deleted count.

        Empty filters are intentionally rejected to reduce the chance of an
        accidental collection-wide delete.
        """
        self._ensure_open()
        if not self._is_nonempty_mapping(query):
            LOGGER.warning("Delete rejected: query must be a non-empty mapping.")
            return 0

        try:
            result = (
                self.collection.delete_many(dict(query))
                if many
                else self.collection.delete_one(dict(query))
            )
            return int(result.deleted_count)
        except PyMongoError as exc:
            LOGGER.error("Delete failed: %s", exc)
            return 0

    # ------------------------------------------------------------------
    # ALGORITHMS / ANALYTICS
    # ------------------------------------------------------------------
    def aggregate(self, pipeline: Sequence[Mapping[str, Any]]) -> List[Document]:
        """Execute a validated MongoDB aggregation pipeline."""
        self._ensure_open()
        if not isinstance(pipeline, Sequence) or isinstance(pipeline, (str, bytes)):
            raise ValueError("pipeline must be a sequence of MongoDB pipeline stages.")
        if not pipeline:
            return []
        if not all(isinstance(stage, Mapping) and stage for stage in pipeline):
            raise ValueError("Every aggregation stage must be a non-empty mapping.")

        try:
            return list(self.collection.aggregate([dict(stage) for stage in pipeline]))
        except PyMongoError as exc:
            LOGGER.error("Aggregation failed: %s", exc)
            return []

    def group_counts(
        self,
        field: str,
        query: Optional[Query] = None,
        limit: Optional[int] = None,
    ) -> List[Document]:
        """Count records by a field using a server-side aggregation algorithm.

        Example:
            shelter.group_counts("breed", {"animal_type": "Dog"}, limit=10)

        Returns documents shaped as ``{"value": <group>, "count": <n>}``, sorted
        from largest to smallest count.
        """
        if not isinstance(field, str) or not field or field.startswith("$"):
            raise ValueError("field must be a valid MongoDB field name.")
        if query is not None and not isinstance(query, Mapping):
            raise ValueError("query must be a mapping or None.")
        if limit is not None and (not isinstance(limit, int) or limit <= 0):
            raise ValueError("limit must be a positive integer or None.")

        pipeline: List[Document] = []
        if query:
            pipeline.append({"$match": dict(query)})
        pipeline.extend(
            [
                {"$group": {"_id": f"${field}", "count": {"$sum": 1}}},
                {"$sort": {"count": DESCENDING, "_id": ASCENDING}},
                {"$project": {"_id": 0, "value": "$_id", "count": 1}},
            ]
        )
        if limit:
            pipeline.append({"$limit": limit})
        return self.aggregate(pipeline)

    def top_breeds(
        self,
        animal_type: Optional[str] = None,
        limit: int = 10,
    ) -> List[Document]:
        """Return the most common breeds, optionally filtered by animal type."""
        if not isinstance(limit, int) or limit <= 0:
            raise ValueError("limit must be a positive integer.")

        query: Document = {}
        if animal_type:
            query["animal_type"] = animal_type
        return self.group_counts("breed", query=query, limit=limit)

    def outcome_summary(self, animal_type: Optional[str] = None) -> List[Document]:
        """Return outcome-type counts, optionally filtered by animal type."""
        query: Document = {}
        if animal_type:
            query["animal_type"] = animal_type
        return self.group_counts("outcome_type", query=query)
