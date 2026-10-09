from AnimalShelter import AnimalShelter

shelter = AnimalShelter()

TEST_ID = "CS499TEST001"

print("\n--- CREATE TEST ---")

test_animal = {
    "animal_id": TEST_ID,
    "name": "Capstone Test",
    "animal_type": "Dog",
    "breed": "Test Breed",
    "age_upon_outcome": "2 years",
    "outcome_type": "Adoption"
}

created = shelter.create(test_animal)

print("Created:", created)

created_record = shelter.read(
    {"animal_id": TEST_ID},
    limit=1
)

print("Record after create:", created_record)


print("\n--- UPDATE TEST ---")

modified = shelter.update(
    {"animal_id": TEST_ID},
    {
        "name": "Capstone Test Updated",
        "breed": "Updated Test Breed"
    }
)

print("Modified:", modified)

updated_record = shelter.read(
    {"animal_id": TEST_ID},
    limit=1
)

print("Record after update:", updated_record)


print("\n--- DELETE TEST ---")

deleted = shelter.delete(
    {"animal_id": TEST_ID}
)

print("Deleted:", deleted)

remaining_record = shelter.read(
    {"animal_id": TEST_ID},
    limit=1
)

print("Record after delete:", remaining_record)