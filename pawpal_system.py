from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from datetime import date


# --- Enumerations ---

class TaskType(Enum):
    WALK = "walk"
    FEEDING = "feeding"
    MEDICATION = "medication"
    ENRICHMENT = "enrichment"
    GROOMING = "grooming"
    VET = "vet"
    OTHER = "other"


class Priority(Enum):
    CRITICAL = 4
    HIGH = 3
    MEDIUM = 2
    LOW = 1


# --- Supporting Value Objects ---

@dataclass
class TimeWindow:
    start_time: str  # e.g. "08:00"
    end_time: str    # e.g. "10:00"


@dataclass
class ScheduledTask:
    task: Task
    pet_id: str      # which pet this task belongs to
    assigned_time: str  # e.g. "09:00"
    rationale: str


# --- Core Classes ---

@dataclass
class Task:
    id: str
    name: str
    type: TaskType
    duration_minutes: int
    priority: Priority
    pet_id: str = ""             # back-reference to owning pet
    date: date | None = None     # specific date for this task, if any
    time: str | None = None      # e.g. "09:00"
    is_completed: bool = False

    def mark_complete(self) -> None:
        pass

    def edit(self, updates: dict) -> None:
        pass

    def create_recurring(self, interval_days: int, count: int) -> list[Task]:
        pass


@dataclass
class Pet:
    id: str
    name: str
    species: str
    breed: str
    age: int
    weight_lbs: float
    medical_notes: str = ""
    birthday: date | None = None
    last_grooming: date | None = None
    last_medication: date | None = None
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        pass

    def remove_task(self, task_id: str) -> None:
        pass

    def edit_task(self, task_id: str, updates: dict) -> None:
        pass

    def get_tasks(self) -> list[Task]:
        pass

    def update_dates(self, field_name: str, new_date: date) -> None:
        pass


@dataclass
class Owner:
    id: str
    name: str
    email: str
    availability: list[TimeWindow] = field(default_factory=list)
    preferences: list[str] = field(default_factory=list)
    pets: list[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        pass

    def remove_pet(self, pet_id: str) -> None:
        pass

    def set_availability(self, windows: list[TimeWindow]) -> None:
        pass

    def get_availability(self) -> list[TimeWindow]:
        pass

    def get_preferences(self) -> list[str]:
        pass


@dataclass
class Schedule:
    date: date
    owner: Owner
    pets: list[Pet] = field(default_factory=list)
    plan: list[ScheduledTask] = field(default_factory=list)
    reasoning: str = ""

    def generate_plan(self) -> list[ScheduledTask]:
        pass

    def add_task(self, scheduled_task: ScheduledTask) -> None:
        pass

    def explain_reasoning(self) -> str:
        pass

    def display_plan(self) -> str:
        pass

    def adjust_task(self, task_id: str, new_time: str) -> None:
        pass
