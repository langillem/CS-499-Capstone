CS 499 Computer Science Capstone
AnimalShelter Artifact Enhancements
Michael Langille
09/29/2026

Overview
--------
This project is based on the AnimalShelter.py CRUD artifact originally created
for CS 340 Client/Server Development. The artifact has been enhanced for the
CS 499 Computer Science Capstone to demonstrate growth in multiple computer
science areas.

Completed enhancement categories:
1. Software Design and Engineering
2. Algorithms and Data Structures
3. Databases

Project Files
-------------
Original_AnimalShelter.py
    Original CS 340 MongoDB CRUD artifact used as the baseline for comparison.

Enhanced_AnimalShelter.py
    Milestone Two - Software Design and Engineering enhancement.

Enhanced_AnimalShelter_Algorithms.py
    Milestone Three - Algorithms and Data Structures enhancement. This version
    builds on the Software Design and Engineering improvements and adds custom
    algorithms and data structures for sorting, searching, indexing, and
    analysis.

Enhanced_AnimalShelter_Database.py
    Milestone Four - Databases enhancement. This version builds on the earlier
    improvements and adds stronger MongoDB query handling, credential
    protection, server-side operations, index management, aggregation, and
    query-plan analysis.

test_software_design_animal_shelter.py
    Unit tests for the Software Design and Engineering enhancement.

test_algorithms_animal_shelter.py
    Unit tests for the Algorithms and Data Structures enhancement.

test_database_animal_shelter.py
    Unit tests for the Databases enhancement.

Enhancement One: Software Design and Engineering
------------------------------------------------
The Software Design and Engineering enhancement improved the structure,
maintainability, testability, validation, error handling, logging, and resource
management of the original CRUD class.

Major improvements include:
- MongoConfig dataclass for database configuration
- safer credential handling
- custom exceptions
- structured logging
- centralized input validation
- dependency injection for unit testing
- MongoDB connection verification
- deterministic close and context-manager support
- preserved create, read, update, and delete behavior

Enhancement Two: Algorithms and Data Structures
-----------------------------------------------
The Algorithms and Data Structures enhancement adds custom in-memory
algorithms and data structures to make the artifact more useful for organizing
and analyzing shelter records.

Major improvements include:

Merge Sort
    Sorts animal records by a selected field while returning a new list so the
    original record order is not changed.

    Time complexity:
        Best case:    O(n log n)
        Average case: O(n log n)
        Worst case:   O(n log n)

    Space complexity:
        O(n) additional memory

Binary Search
    Searches an already sorted list by repeatedly narrowing the search area.
    The implementation also returns duplicate matches when multiple records
    have the same value.

    Lookup behavior:
        O(log n), plus the time needed to return duplicate matches

Dictionary-Based Lookup Index
    Groups records by a selected field such as animal_type or breed. Building
    the index requires one pass through the records, but repeated exact-key
    lookups are usually very fast.

    Build time:
        O(n)

    Average exact-key lookup:
        O(1)

Frequency Counting
    Uses a dictionary to count how often values appear in a selected field,
    such as the number of dogs, cats, or individual breeds.

    Time complexity:
        O(n)

read_sorted()
    Connects the custom merge-sort logic to records returned from MongoDB so
    query results can be sorted in memory using the enhancement.

Design Trade-Offs
-----------------
This enhancement demonstrates that selecting an algorithm is not only about
choosing the fastest Big-O value. Other factors also matter, including memory
usage, the size of the dataset, whether searches will be repeated, code
complexity, and how the application will actually be used.

For example, merge sort provides predictable performance but needs additional
memory. A dictionary index takes time and memory to build, but it can make
repeated exact-key searches much faster. In a large production system,
database-side sorting and MongoDB indexes may be more appropriate, but the
custom implementations in this project clearly demonstrate algorithm and data
structure concepts for the capstone.

Enhancement Three: Databases
----------------------------
The Databases enhancement strengthens the MongoDB layer of the AnimalShelter
artifact by improving security, query safety, database efficiency, and
administrative visibility. It moves more data-processing work to MongoDB when
that is more appropriate than performing the work in application memory.

Major improvements include:

Environment-Based Configuration
    MongoConfig.from_environment() supports loading MongoDB credentials and
    connection settings from environment variables so passwords do not need to
    be hard-coded in the source code.

Query Validation
    MongoDB query documents are validated before execution. Potentially unsafe
    operators such as $where, $function, and $accumulator are rejected.

Safer Update and Delete Operations
    Update operations use an allowlist of supported MongoDB update operators.
    Empty filters are rejected for update and delete operations to reduce the
    risk of accidentally modifying or deleting an entire collection.

Server-Side Sorting and Pagination
    Read operations support MongoDB sort, skip, and limit features so large
    result sets can be ordered and paginated by the database instead of loading
    everything into application memory first.

Document Counting
    count() uses MongoDB count_documents() to count matching records directly
    in the database.

Aggregation
    aggregate_by() performs server-side grouping and counting. This supports
    summaries such as the number of animals by breed or animal type without
    requiring every record to be processed in Python.

Index Management
    ensure_indexes() creates useful MongoDB indexes for common shelter queries,
    including breed, animal type, a compound animal-type/breed index, and an
    outcome-related index.

Query Plan Analysis
    explain_query() exposes MongoDB query-plan information so index usage and
    query performance can be evaluated.

Database Design Trade-Offs
--------------------------
The database enhancement demonstrates the difference between processing data
in Python and allowing MongoDB to perform work close to the stored data.
Server-side sorting, counting, aggregation, and indexed searches can reduce the
amount of data transferred to the application and can improve scalability.

Indexes also involve trade-offs. They can make common read operations faster,
but they require additional storage and add maintenance cost when records are
inserted or updated. The enhancement therefore focuses on indexes that support
common AnimalShelter query patterns rather than indexing every field.

Requirements
------------
- Python 3.x
- PyMongo
- MongoDB for live CRUD and database operations

Install PyMongo with:

    pip install pymongo

Suggested MongoDB Configuration
-------------------------------
The project supports configurable connection settings rather than requiring
database credentials to be hard-coded directly into the source code.

Typical settings include:
- username
- password
- host
- port
- authentication source
- database name
- collection name
- TLS setting

Default local development values use:
    Host: localhost
    Port: 27017
    Database: aac
    Collection: animals

The Databases enhancement also supports these optional environment variables:
    MONGODB_USERNAME
    MONGODB_PASSWORD
    MONGODB_HOST
    MONGODB_PORT
    MONGODB_AUTH_SOURCE
    MONGODB_DB
    MONGODB_COLLECTION
    MONGODB_TLS

Example database-enhancement usage:

    config = MongoConfig.from_environment()

    with AnimalShelter(config=config) as shelter:
        shelter.ensure_indexes()
        dogs = shelter.read(
            {"animal_type": "Dog"},
            sort=[("breed", 1)],
            limit=20
        )
        summary = shelter.aggregate_by(
            "breed",
            match={"animal_type": "Dog"}
        )

Running the Tests
-----------------
Software Design and Engineering tests:

    python -m unittest test_software_design_animal_shelter.py

Algorithms and Data Structures tests:

    python -m unittest test_algorithms_animal_shelter.py

Databases tests:

    python -m unittest test_database_animal_shelter.py

The Algorithms and Data Structures enhancement was tested in PyCharm with all
8 unit tests passing successfully.

The Databases enhancement was tested with all 11 database-focused unit tests
passing successfully.

CS 499 Course Outcome Connection
--------------------------------
Together, the three enhancements demonstrate progress across several CS 499
course outcomes.

Software Design and Engineering demonstrates:
- maintainable and reusable object-oriented design
- validation, logging, exception handling, and resource management
- testability through dependency injection
- secure configuration and connection practices

Algorithms and Data Structures demonstrates:
- selection and implementation of appropriate algorithms
- use of dictionaries as purposeful data structures
- analysis of time and space complexity
- testing of normal, duplicate, reverse-sort, and no-match cases
- explanation of practical algorithmic trade-offs

Databases demonstrates:
- secure credential and connection management
- safer MongoDB query and update practices
- server-side sorting, pagination, counting, and aggregation
- creation and evaluation of MongoDB indexes
- use of query plans to analyze database performance
- consideration of security, scalability, and data-access trade-offs

These enhancements support the CS 499 outcomes related to designing and
evaluating computing solutions, using well-founded computing techniques and
tools to deliver value, communicating technical design choices, and developing
a security mindset that protects data and resources.

Portfolio Purpose
-----------------
The goal of this artifact is to show the progression from a basic working CRUD
class to a more maintainable, testable, analytically capable, secure, and
database-aware solution. The different versions make it possible to compare the
original artifact with each enhanced version and explain the reasoning,
trade-offs, testing, and skills demonstrated by each stage of improvement.
