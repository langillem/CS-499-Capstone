################################################################################
# AnimalShelter.py
#
# Description:
#     This module provides a Python interface for performing CRUD (Create, Read,
#     Update, Delete) operations on an animal shelter database stored in MongoDB.
#     It encapsulates database connection logic and provides a clean API for
#     managing animal records in the AAC (Animal Adoption Center) database.
#
# Author: Michael Langille
# Course: CS-340: Client/Server Development
################################################################################

from typing import Any, Dict, List, Optional
from pymongo import MongoClient
from pymongo.errors import PyMongoError


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
        tls: bool = False
    ) -> None:
        try:
            scheme = "mongodb+srv" if tls else "mongodb"

            if username and password:
                uri = (
                    f"{scheme}://{username}:{password}@"
                    f"{host}:{port}/?authSource={auth_source}"
                )
            else:
                uri = f"mongodb://{host}:{port}"

            self.client = MongoClient(uri)
            self.database = self.client[db_name]
            self.collection = self.database[collection_name]

            # Original version created the MongoClient a second time.
            self.client = MongoClient(uri, tls=tls)
            self.database = self.client[db_name]
            self.collection = self.database[collection_name]

        except PyMongoError as exc:
            raise RuntimeError(f"Failed to connect to MongoDB: {exc}") from exc

    def create(self, document: Dict[str, Any]) -> bool:
        if not isinstance(document, dict) or not document:
            return False

        try:
            result = self.collection.insert_one(document)
            return bool(result.acknowledged)
        except PyMongoError as exc:
            print(f"Create error: {exc}")
            return False

    def read(
        self,
        query: Optional[Dict[str, Any]] = None,
        projection: Optional[Dict[str, int]] = None,
        limit: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        try:
            cursor = self.collection.find(query or {}, projection or {})
            if isinstance(limit, int) and limit > 0:
                cursor = cursor.limit(limit)
            return list(cursor)
        except PyMongoError as exc:
            print(f"Read error: {exc}")
            return []

    def update(
        self,
        query: Dict[str, Any],
        update_values: Dict[str, Any],
        many: bool = False
    ) -> int:
        if not isinstance(query, dict) or not query:
            return 0
        if not isinstance(update_values, dict) or not update_values:
            return 0

        try:
            has_operator = any(k.startswith("$") for k in update_values.keys())
            update_doc = update_values if has_operator else {"$set": update_values}

            if many:
                result = self.collection.update_many(query, update_doc)
            else:
                result = self.collection.update_one(query, update_doc)

            return int(result.modified_count or 0)

        except PyMongoError as exc:
            print(f"Update error: {exc}")
            return 0

    def delete(self, query: Dict[str, Any], many: bool = False) -> int:
        if not isinstance(query, dict) or not query:
            return 0

        try:
            if many:
                result = self.collection.delete_many(query)
            else:
                result = self.collection.delete_one(query)

            return int(result.deleted_count or 0)

        except PyMongoError as exc:
            print(f"Delete error: {exc}")
            return 0
