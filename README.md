CS 499 Computer Science Capstone

AnimalShelter Artifact Enhancements

Michael Langille

09/30/2026



Overview

\--------

This project is based on the AnimalShelter.py CRUD artifact originally created

for CS 340 Client/Server Development. The artifact has been enhanced for the

CS 499 Computer Science Capstone to demonstrate growth in multiple computer

science areas.



Completed enhancement categories:

1\. Software Design and Engineering

2\. Algorithms and Data Structures

3\. Databases



Project Files

\-------------

Original\_AnimalShelter.py

&#x20;   Original CS 340 MongoDB CRUD artifact used as the baseline for comparison.



Enhanced\_AnimalShelter.py

&#x20;   Milestone Two - Software Design and Engineering enhancement.



Enhanced\_AnimalShelter\_Algorithms.py

&#x20;   Milestone Three - Algorithms and Data Structures enhancement. This version

&#x20;   builds on the Software Design and Engineering improvements and adds custom

&#x20;   algorithms and data structures for sorting, searching, indexing, and

&#x20;   analysis.



Enhanced\_AnimalShelter\_Database.py

&#x20;   Milestone Four - Databases enhancement. This version builds on the earlier

&#x20;   improvements and adds stronger MongoDB query handling, credential

&#x20;   protection, server-side operations, index management, aggregation, and

&#x20;   query-plan analysis.



test\_software\_design\_animal\_shelter.py

&#x20;   Unit tests for the Software Design and Engineering enhancement.



test\_algorithms\_animal\_shelter.py

&#x20;   Unit tests for the Algorithms and Data Structures enhancement.



test\_database\_animal\_shelter.py

&#x20;   Unit tests for the Databases enhancement.



Enhancement One: Software Design and Engineering

\------------------------------------------------

The Software Design and Engineering enhancement improved the structure,

maintainability, testability, validation, error handling, logging, and resource

management of the original CRUD class.



Major improvements include:

\- MongoConfig dataclass for database configuration

\- safer credential handling

\- custom exceptions

\- structured logging

\- centralized input validation

\- dependency injection for unit testing

\- MongoDB connection verification

\- deterministic close and context-manager support

\- preserved create, read, update, and delete behavior



Enhancement Two: Algorithms and Data Structures

\-----------------------------------------------

The Algorithms and Data Structures enhancement adds custom in-memory

algorithms and data structures to make the artifact more useful for organizing

and analyzing shelter records.



Major improvements include:



Merge Sort

&#x20;   Sorts animal records by a selected field while returning a new list so the

&#x20;   original record order is not changed.



&#x20;   Time complexity:

&#x20;       Best case:    O(n log n)

&#x20;       Average case: O(n log n)

&#x20;       Worst case:   O(n log n)



&#x20;   Space complexity:

&#x20;       O(n) additional memory



Binary Search

&#x20;   Searches an already sorted list by repeatedly narrowing the search area.

&#x20;   The implementation also returns duplicate matches when multiple records

&#x20;   have the same value.



&#x20;   Lookup behavior:

&#x20;       O(log n), plus the time needed to return duplicate matches



Dictionary-Based Lookup Index

&#x20;   Groups records by a selected field such as animal\_type or breed. Building

&#x20;   the index requires one pass through the records, but repeated exact-key

&#x20;   lookups are usually very fast.



&#x20;   Build time:

&#x20;       O(n)



&#x20;   Average exact-key lookup:

&#x20;       O(1)



Frequency Counting

&#x20;   Uses a dictionary to count how often values appear in a selected field,

&#x20;   such as the number of dogs, cats, or individual breeds.



&#x20;   Time complexity:

&#x20;       O(n)



read\_sorted()

&#x20;   Connects the custom merge-sort logic to records returned from MongoDB so

&#x20;   query results can be sorted in memory using the enhancement.



Design Trade-Offs

\-----------------

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

\----------------------------

The Databases enhancement strengthens the MongoDB layer of the AnimalShelter

artifact by improving security, query safety, database efficiency, and

administrative visibility. It moves more data-processing work to MongoDB when

that is more appropriate than performing the work in application memory.



Major improvements include:



Environment-Based Configuration

&#x20;   MongoConfig.from\_environment() supports loading MongoDB credentials and

&#x20;   connection settings from environment variables so passwords do not need to

&#x20;   be hard-coded in the source code.



Query Validation

&#x20;   MongoDB query documents are validated before execution. Potentially unsafe

&#x20;   operators such as $where, $function, and $accumulator are rejected.



Safer Update and Delete Operations

&#x20;   Update operations use an allowlist of supported MongoDB update operators.

&#x20;   Empty filters are rejected for update and delete operations to reduce the

&#x20;   risk of accidentally modifying or deleting an entire collection.



Server-Side Sorting and Pagination

&#x20;   Read operations support MongoDB sort, skip, and limit features so large

&#x20;   result sets can be ordered and paginated by the database instead of loading

&#x20;   everything into application memory first.



Document Counting

&#x20;   count() uses MongoDB count\_documents() to count matching records directly

&#x20;   in the database.



Aggregation

&#x20;   aggregate\_by() performs server-side grouping and counting. This supports

&#x20;   summaries such as the number of animals by breed or animal type without

&#x20;   requiring every record to be processed in Python.



Index Management

&#x20;   ensure\_indexes() creates useful MongoDB indexes for common shelter queries,

&#x20;   including breed, animal type, a compound animal-type/breed index, and an

&#x20;   outcome-related index.



Query Plan Analysis

&#x20;   explain\_query() exposes MongoDB query-plan information so index usage and

&#x20;   query performance can be evaluated.



Database Design Trade-Offs

\--------------------------

The database enhancement demonstrates the difference between processing data

in Python and allowing MongoDB to perform work close to the stored data.

Server-side sorting, counting, aggregation, and indexed searches can reduce the

amount of data transferred to the application and can improve scalability.



Indexes also involve trade-offs. They can make common read operations faster,

but they require additional storage and add maintenance cost when records are

inserted or updated. The enhancement therefore focuses on indexes that support

common AnimalShelter query patterns rather than indexing every field.



Requirements

\------------

\- Python 3.x

\- PyMongo

\- MongoDB for live CRUD and database operations



Install PyMongo with:



&#x20;   pip install pymongo



Suggested MongoDB Configuration

\-------------------------------

The project supports configurable connection settings rather than requiring

database credentials to be hard-coded directly into the source code.



Typical settings include:

\- username

\- password

\- host

\- port

\- authentication source

\- database name

\- collection name

\- TLS setting



Default local development values use:

&#x20;   Host: localhost

&#x20;   Port: 27017

&#x20;   Database: aac

&#x20;   Collection: animals



The Databases enhancement also supports these optional environment variables:

&#x20;   MONGODB\_USERNAME

&#x20;   MONGODB\_PASSWORD

&#x20;   MONGODB\_HOST

&#x20;   MONGODB\_PORT

&#x20;   MONGODB\_AUTH\_SOURCE

&#x20;   MONGODB\_DB

&#x20;   MONGODB\_COLLECTION

&#x20;   MONGODB\_TLS



Example database-enhancement usage:



&#x20;   config = MongoConfig.from\_environment()



&#x20;   with AnimalShelter(config=config) as shelter:

&#x20;       shelter.ensure\_indexes()

&#x20;       dogs = shelter.read(

&#x20;           {"animal\_type": "Dog"},

&#x20;           sort=\[("breed", 1)],

&#x20;           limit=20

&#x20;       )

&#x20;       summary = shelter.aggregate\_by(

&#x20;           "breed",

&#x20;           match={"animal\_type": "Dog"}

&#x20;       )



Running the Tests

\-----------------

Software Design and Engineering tests:



&#x20;   python -m unittest test\_software\_design\_animal\_shelter.py



Algorithms and Data Structures tests:



&#x20;   python -m unittest test\_algorithms\_animal\_shelter.py



Databases tests:



&#x20;   python -m unittest test\_database\_animal\_shelter.py



The Algorithms and Data Structures enhancement was tested in PyCharm with all

8 unit tests passing successfully.



The Databases enhancement was tested with all 11 database-focused unit tests

passing successfully.



CS 499 Course Outcome Connection

\--------------------------------

Together, the three enhancements demonstrate progress across several CS 499

course outcomes.



Software Design and Engineering demonstrates:

\- maintainable and reusable object-oriented design

\- validation, logging, exception handling, and resource management

\- testability through dependency injection

\- secure configuration and connection practices



Algorithms and Data Structures demonstrates:

\- selection and implementation of appropriate algorithms

\- use of dictionaries as purposeful data structures

\- analysis of time and space complexity

\- testing of normal, duplicate, reverse-sort, and no-match cases

\- explanation of practical algorithmic trade-offs



Databases demonstrates:

\- secure credential and connection management

\- safer MongoDB query and update practices

\- server-side sorting, pagination, counting, and aggregation

\- creation and evaluation of MongoDB indexes

\- use of query plans to analyze database performance

\- consideration of security, scalability, and data-access trade-offs



These enhancements support the CS 499 outcomes related to designing and

evaluating computing solutions, using well-founded computing techniques and

tools to deliver value, communicating technical design choices, and developing

a security mindset that protects data and resources.



Portfolio Purpose

\-----------------

The goal of this artifact is to show the progression from a basic working CRUD

class to a more maintainable, testable, analytically capable, secure, and

database-aware solution. The different versions make it possible to compare the

original artifact with each enhanced version and explain the reasoning,

trade-offs, testing, and skills demonstrated by each stage of improvement.

