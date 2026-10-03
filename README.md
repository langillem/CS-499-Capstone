# CS 499 Computer Science Capstone ePortfolio

**Michael Langille**  
Southern New Hampshire University  
B.S. Computer Science  
CS 499 Computer Science Capstone

## ePortfolio

This repository contains my final CS 499 Computer Science Capstone ePortfolio. The portfolio demonstrates my growth throughout the Computer Science program through a code review, professional self-assessment, artifact enhancements, written narratives, source-code comparisons, and course-outcome mapping.

### View the Live Portfolio

[CS 499 ePortfolio](https://langillem.github.io/CS-499-Capstone/)

---

## Portfolio Overview

The primary artifact used throughout the capstone is my `AnimalShelter.py` project, originally developed for **CS 340 Client/Server Development**.

The original project provided a Python interface for performing CRUD operations on animal records stored in MongoDB. During CS 499, I enhanced the artifact in three areas:

1. **Software Design and Engineering**
2. **Algorithms and Data Structures**
3. **Databases**

Using the same core artifact across the three categories makes it possible to show the progression from a functional academic project to a more maintainable, efficient, secure, and professional computing solution.

---

## Enhancement One: Software Design and Engineering

The first enhancement focused on improving the internal design and maintainability of the original `AnimalShelter` CRUD module.

Key improvements include:

- Separation of MongoDB configuration from application behavior
- `MongoConfig` configuration object
- Centralized input validation
- Custom exception classes
- Structured logging
- Dependency injection for testing
- MongoDB connection verification
- Resource-management improvements
- Context-manager support
- Improved testability and maintainability

The enhancement preserved the original CRUD purpose while restructuring the application to follow stronger software-engineering practices.

[View Software Design and Engineering](software-design.html)

---

## Enhancement Two: Algorithms and Data Structures

The second enhancement added purposeful algorithms and data structures for working with animal-shelter records after they are retrieved from MongoDB.

The enhancement includes:

- Non-mutating merge sort
- Binary search
- Dictionary-based lookup indexing
- Frequency counting
- In-memory sorting and searching
- Complexity analysis
- Design trade-off evaluation
- Integration between MongoDB query results and custom algorithms
- Unit testing of algorithm behavior

This enhancement demonstrates how algorithm selection involves more than making code work. Time complexity, memory use, data organization, repeated operations, and application requirements all affect the choice of an appropriate solution.

[View Algorithms and Data Structures](algorithms.html)

---

## Enhancement Three: Databases

The database enhancement focuses on improving how the application communicates with and protects the MongoDB database.

Areas addressed include:

- MongoDB CRUD operations
- Database configuration
- Credential protection
- Query validation
- Safe update and delete operations
- Server-side data processing
- Indexing considerations
- Query performance
- Connection management
- Database security
- Data integrity

This work demonstrates that database design involves more than storing and retrieving records. Performance, security, validation, reliability, and efficient data access must also be considered.

[View Databases](databases.html)

---

## Original and Enhanced Source Code

The portfolio includes browser-friendly versions of the Python source code so visitors can review the artifact without downloading the files.

- [View Original AnimalShelter Source Code](artifacts/source/original-animal-shelter.html)
- [View Enhanced AnimalShelter Source Code](artifacts/source/enhanced-animal-shelter.html)

The original and enhanced versions make it possible to directly compare the artifact before and after the capstone enhancement process.

---

## Artifact Narratives

Each enhancement includes a written narrative explaining:

- The origin and purpose of the artifact
- Why the artifact was selected
- How the enhancement improved the artifact
- Skills demonstrated through the enhancement
- Course outcomes addressed
- Design decisions and trade-offs
- Challenges encountered
- Lessons learned during the enhancement process

Narratives:

- [Software Design and Engineering Narrative](narratives/software-design-narrative.html)
- [Algorithms and Data Structures Narrative](narratives/algorithms-narrative.html)
- [Databases Narrative](narratives/database-narrative.html)

---

## Code Review

The CS 499 code review examines the original `AnimalShelter.py` artifact before the enhancements were completed.

The review discusses:

- Existing functionality
- Code organization
- Maintainability
- Algorithms and efficiency
- Database practices
- Testing
- Security
- Planned enhancements

[View Code Review](code-review.html)

---

## Professional Self-Assessment

The professional self-assessment reflects on my growth throughout the Computer Science program and discusses how my coursework prepared me for professional work in computing.

Topics include:

- Growth through the Computer Science program
- Collaboration and communication
- Algorithms and data structures
- Software engineering
- Database development
- Security
- Professional goals
- Lifelong learning
- How the capstone artifacts fit together

[View Professional Self-Assessment](self-assessment.html)

---

## Computer Science Program Outcomes

The portfolio demonstrates progress toward the five Computer Science program outcomes:

1. **Collaboration and Decision Support**  
   Employ strategies for building collaborative environments that enable diverse audiences to support organizational decision-making.

2. **Professional Communication**  
   Design, develop, and deliver professional-quality oral, written, and visual communications appropriate to specific audiences and contexts.

3. **Algorithms and Design Trade-Offs**  
   Design and evaluate computing solutions using algorithmic principles and computer science practices while considering trade-offs in design decisions.

4. **Tools and Computing Techniques**  
   Use well-founded and innovative techniques, skills, and tools to implement computing solutions that deliver value.

5. **Security Mindset**  
   Anticipate vulnerabilities, mitigate design flaws, protect data and resources, and incorporate secure development practices.

[View Course Outcomes Mapping](course-outcomes.html)

---

## Technologies and Tools

This portfolio demonstrates experience with:

- Python
- Object-oriented programming
- MongoDB
- PyMongo
- CRUD operations
- Data structures
- Merge sort
- Binary search
- Dictionaries and indexing
- Unit testing
- Mock testing
- Logging
- Exception handling
- Input validation
- HTML
- CSS
- Git
- GitHub
- GitHub Pages
- PyCharm

---

## Repository Structure

```text
CS-499-ePortfolio/
│
├── index.html
├── self-assessment.html
├── code-review.html
├── software-design.html
├── algorithms.html
├── databases.html
├── course-outcomes.html
├── README.md
│
├── assets/
│   └── css/
│       └── styles.css
│
├── artifacts/
│   ├── original/
│   │   └── Original_AnimalShelter.py
│   │
│   ├── enhanced/
│   │   └── Enhanced_AnimalShelter.py
│   │
│   └── source/
│       ├── original-animal-shelter.html
│       └── enhanced-animal-shelter.html
│
├── narratives/
│   ├── software-design-narrative.html
│   ├── algorithms-narrative.html
│   └── database-narrative.html
│
└── tests/
    ├── software-design-tests.html
    ├── algorithms-tests.html
    └── database-tests.html
```
