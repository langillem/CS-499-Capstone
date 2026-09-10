"""Simple local smoke test for the enhanced AnimalShelter class.

Run this only after MongoDB is running and the AAC database has been imported.
Set MONGO_USERNAME and MONGO_PASSWORD in the PyCharm run configuration if your
MongoDB installation requires authentication.
"""

from AnimalShelter import AnimalShelter


def main() -> None:
    test_id = "CS499-TEST-001"

    with AnimalShelter() as shelter:
        print("MongoDB connected:", shelter.ping())
        print("Total animal records:", shelter.count())

        created = shelter.create(
            {
                "animal_id": test_id,
                "animal_type": "Dog",
                "breed": "Test Breed",
                "name": "Capstone Test",
                "outcome_type": "Adoption",
            }
        )
        print("CREATE:", created)

        record = shelter.read({"animal_id": test_id}, limit=1)
        print("READ:", record)

        modified = shelter.update(
            {"animal_id": test_id},
            {"name": "Capstone Test Updated"},
        )
        print("UPDATE modified count:", modified)

        summary = shelter.outcome_summary("Dog")[:5]
        print("DOG OUTCOME SUMMARY:", summary)

        frame = shelter.read_dataframe(
            {"animal_type": "Dog"},
            projection={"animal_id": 1, "breed": 1, "outcome_type": 1},
            limit=5,
        )
        print("DATAFRAME SAMPLE:")
        print(frame)

        deleted = shelter.delete({"animal_id": test_id})
        print("DELETE count:", deleted)


if __name__ == "__main__":
    main()
