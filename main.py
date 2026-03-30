from datetime import date
from pawpal_system import Owner, Pet, Task, TaskType, Priority, Frequency, TimeWindow, Scheduler
import uuid

# Create owner
owner = Owner(
    id=str(uuid.uuid4()),
    name="Alex Rivera",
    email="alex@example.com",
    availability=[TimeWindow("07:00", "09:00"), TimeWindow("17:00", "20:00")],
)

# Create pets
buddy = Pet(
    id=str(uuid.uuid4()),
    name="Buddy",
    species="Dog",
    breed="Golden Retriever",
    age=3,
    weight_lbs=65.0,
)

whiskers = Pet(
    id=str(uuid.uuid4()),
    name="Whiskers",
    species="Cat",
    breed="Tabby",
    age=5,
    weight_lbs=10.5,
    medical_notes="Needs thyroid medication daily",
)

owner.add_pet(buddy)
owner.add_pet(whiskers)

# Add tasks to Buddy
buddy.add_task(Task(
    id=str(uuid.uuid4()),
    name="Morning Walk",
    type=TaskType.WALK,
    duration_minutes=30,
    priority=Priority.HIGH,
    date=date.today(),
    time="07:00",
    frequency=Frequency.DAILY,
))

buddy.add_task(Task(
    id=str(uuid.uuid4()),
    name="Breakfast",
    type=TaskType.FEEDING,
    duration_minutes=10,
    priority=Priority.HIGH,
    date=date.today(),
    time="07:30",
    frequency=Frequency.DAILY,
))

buddy.add_task(Task(
    id=str(uuid.uuid4()),
    name="Evening Walk",
    type=TaskType.WALK,
    duration_minutes=45,
    priority=Priority.MEDIUM,
    date=date.today(),
    time="17:00",
    frequency=Frequency.DAILY,
))

# Add tasks to Whiskers
whiskers.add_task(Task(
    id=str(uuid.uuid4()),
    name="Thyroid Medication",
    type=TaskType.MEDICATION,
    duration_minutes=5,
    priority=Priority.CRITICAL,
    date=date.today(),
    time="08:00",
    frequency=Frequency.DAILY,
))

whiskers.add_task(Task(
    id=str(uuid.uuid4()),
    name="Dinner",
    type=TaskType.FEEDING,
    duration_minutes=10,
    priority=Priority.HIGH,
    date=date.today(),
    time="18:00",
    frequency=Frequency.DAILY,
))

# Build and print Today's Schedule
scheduler = Scheduler(date=date.today(), owner=owner, pets=owner.get_pets())
scheduler.generate_plan()

print("=" * 50)
print("         TODAY'S SCHEDULE")
print(f"         Owner: {owner.name}")
print("=" * 50)
print(scheduler.display_plan())
print()
print("--- Scheduling Notes ---")
print(scheduler.explain_reasoning())
print("=" * 50)
