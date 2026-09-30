"""AnimalShelter - CS 499 Software Design and Engineering Enhancement.

Author: Michael Langille
Date: 2026-09-20

This version enhances the original CS 340 CRUD artifact only in the Software
Design and Engineering category. It keeps the original CRUD purpose and
familiar constructor while improving maintainability, testability, validation,
error handling, logging, and resource management.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Any, Dict, List, Optional
from urllib.parse import quote_plus

from pymongo import MongoClient
from pymongo.errors import PyMongoError


LOGGER = logging.getLogger(__name__)


class AnimalShelterError(Exception):
    """Base exception for errors raised by the AnimalShelter module."""


class DataValidationError(AnimalShelterError):
    """Raised when invalid input is supplied to a CRUD operation."""


class DatabaseConnectionError(AnimalShelterError):
    """Raised when the MongoDB connection cannot be created or verified."""


@dataclass(frozen=True)
class MongoConfig:
    """Immutable MongoDB configuration used by AnimalShelter."""

    username: str = ""
    password: str = ""
    host: str = "localhost"
    port: int = 27017
    auth_source: str = "admin"
    db_name: str = "aac"
    collection_name: str = "animals"
    tls: bool = False
    server_selection_timeout_ms: int = 5000

    def build_uri(self) -> str:
        """Return a MongoDB URI with safely escaped credential values."""
        if self.username and self.password:
            username = quote_plus(self.username)
            password = quote_plus(self.password)
            auth_source = quote_plus(self.auth_source)
            return (
                f"mongodb://{username}:{password}@{self.host}:{self.port}/"
                f"?authSource={auth_source}"
            )

        return f"mongodb://{self.host}:{self.port}"


class AnimalShelter:
    """Provide CRUD operations for the AAC animals MongoDB collection."""

    def __init__(
        self,
        username: str = "",
        password: str = "",
        host: str = "localhost",
        port: int = 27017,
        auth_source: str = "admin",
        db_name: str = "aac",
        collection_name: str = "animals",
        tls: bool = False,
        *,
        config: Optional[MongoConfig] = None,
        client: Optional[MongoClient] = None,
        verify_connection: bool = True,
    ) -> None:
        self.config = config or MongoConfig(
            username=username,
            password=password,
            host=host,
            port=port,
            auth_source=auth_source,
            db_name=db_name,
            collection_name=collection_name,
            tls=tls,
        )
        self._owns_client = client is None

        try:
            self.client = client or MongoClient(
                self.config.build_uri(),
                tls=self.config.tls,
                serverSelectionTimeoutMS=self.config.server_selection_timeout_ms,
            )

            self.database = self.client[self.config.db_name]
            self.collection = self.database[self.config.collection_name]

            if verify_connection:
                self.client.admin.command("ping")

            LOGGER.info(
                "Connected to MongoDB database '%s', collection '%s'.",
                self.config.db_name,
                self.config.collection_name,
            )
        except (PyMongoError, ValueError, TypeError) as exc:
            LOGGER.exception("MongoDB initialization failed.")
            raise DatabaseConnectionError(
                "Unable to initialize the AnimalShelter MongoDB connection."
            ) from exc

    @staticmethod
    def _require_nonempty_dict(value: Any, field_name: str) -> Dict[str, Any]:
        """Validate and return a required non-empty dictionary."""
        if not isinstance(value, dict) or not value:
            raise DataValidationError(
                f"{field_name} must be a non-empty dictionary."
            )
        return value

    @staticmethod
    def _optional_dict(
        value: Optional[Dict[str, Any]], field_name: str
    ) -> Dict[str, Any]:
        """Validate an optional dictionary and normalize None to {}."""
        if value is None:
            return {}
        if not isinstance(value, dict):
            raise DataValidationError(f"{field_name} must be a dictionary or None.")
        return value

    def create(self, document: Dict[str, Any]) -> bool:
        """Insert one animal document and return whether MongoDB acknowledged it."""
        document = self._require_nonempty_dict(document, "document")

        try:
            result = self.collection.insert_one(document)
            return bool(result.acknowledged)
        except PyMongoError as exc:
            LOGGER.exception("Create operation failed.")
            raise AnimalShelterError("Unable to create the animal record.") from exc

    def read(
        self,
        query: Optional[Dict[str, Any]] = None,
        projection: Optional[Dict[str, int]] = None,
        limit: Optional[int] = None,
    ) -> List[Dict[str, Any]]:
        """Return animal documents that match the supplied MongoDB query."""
        query_doc = self._optional_dict(query, "query")

        if projection is not None and not isinstance(projection, dict):
            raise DataValidationError("projection must be a dictionary or None.")

        if limit is not None and (not isinstance(limit, int) or limit < 1):
            raise DataValidationError("limit must be a positive integer or None.")

        try:
            cursor = self.collection.find(query_doc, projection)
            if limit is not None:
                cursor = cursor.limit(limit)
            return list(cursor)
        except PyMongoError as exc:
            LOGGER.exception("Read operation failed.")
            raise AnimalShelterError("Unable to read animal records.") from exc

    def update(
        self,
        query: Dict[str, Any],
        update_values: Dict[str, Any],
        many: bool = False,
    ) -> int:
        """Update matching animal records and return the modified count."""
        query = self._require_nonempty_dict(query, "query")
        update_values = self._require_nonempty_dict(update_values, "update_values")

        if not isinstance(many, bool):
            raise DataValidationError("many must be True or False.")

        has_operator = any(str(key).startswith("$") for key in update_values)
        update_doc = update_values if has_operator else {"$set": update_values}

        try:
            if many:
                result = self.collection.update_many(query, update_doc)
            else:
                result = self.collection.update_one(query, update_doc)
            return int(result.modified_count or 0)
        except PyMongoError as exc:
            LOGGER.exception("Update operation failed.")
            raise AnimalShelterError("Unable to update animal records.") from exc

    def delete(self, query: Dict[str, Any], many: bool = False) -> int:
        """Delete matching animal records and return the deleted count."""
        query = self._require_nonempty_dict(query, "query")

        if not isinstance(many, bool):
            raise DataValidationError("many must be True or False.")

        try:
            if many:
                result = self.collection.delete_many(query)
            else:
                result = self.collection.delete_one(query)
            return int(result.deleted_count or 0)
        except PyMongoError as exc:
            LOGGER.exception("Delete operation failed.")
            raise AnimalShelterError("Unable to delete animal records.") from exc

    def close(self) -> None:
        """Close the MongoDB client when this object created the client."""
        if self._owns_client and self.client is not None:
            self.client.close()
            LOGGER.info("MongoDB client closed.")

    def __enter__(self) -> "AnimalShelter":
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        self.close()
