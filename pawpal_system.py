from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from datetime import date, timedelta
import copy
import uuid


# --- Enumerations ---

class TaskType(Enum):
    """Categorizes the kind of care activity a task represents."""
    WALK = "walk"
    FEEDING = "feeding"
    MEDICATION = "medication"
    ENRICHMENT = "enrichment"
    GROOMING = "grooming"
    VET = "vet"
    OTHER = "other"


class Priority(Enum):
    """Numeric urgency levels used to order tasks during scheduling."""
    CRITICAL = 4
    HIGH = 3
    MEDIUM = 2
    LOW = 1


class Frequency(Enum):
    """Recurrence cadence for a task."""
    ONCE = "once"
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"


# --- Supporting Value Objects ---

@dataclass
class TimeWindow:
    """Represents a contiguous block of time during which the owner is available."""
    start_time: str  # e.g. "08:00"
    end_time: str    # e.g. "10:00"


@dataclass
class ScheduledTask:
    """Pairs a Task with the pet, time slot, and rationale assigned by the scheduler."""
    task: Task
    pet_id: str         # which pet this task belongs to
    assigned_time: str  # e.g. "09:00"
    rationale: str


# --- Helpers ---

def _time_to_minutes(t: str) -> int:
    """Parse "HH:MM" into total minutes since midnight."""
    h, m = t.split(":")
    return int(h) * 60 + int(m)


def _minutes_to_time(minutes: int) -> str:
    """Convert total minutes since midnight to "HH:MM"."""
    return f"{minutes // 60:02d}:{minutes % 60:02d}"


# --- Core Classes ---

@dataclass
class Task:
    """A single care action to be performed for a pet, with scheduling metadata."""
    id: str
    name: str
    type: TaskType
    duration_minutes: int
    priority: Priority
    pet_id: str = ""
    date: date | None = None
    time: str | None = None
    frequency: Frequency = Frequency.ONCE
    is_completed: bool = False

    def mark_complete(self) -> None:
        """Mark this task as completed."""
        self.is_completed = True

    def edit(self, updates: dict) -> None:
        """Update any task fields supplied in the updates dict."""
        for key, value in updates.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def create_recurring(self, interval_days: int, count: int) -> list[Task]:
        """Return `count` copies of this task spaced `interval_days` apart."""
        base_date = self.date or date.today()
        recurring = []
        for i in range(1, count + 1):
            new_task = copy.copy(self)
            new_task.id = str(uuid.uuid4())
            new_task.date = base_date + timedelta(days=interval_days * i)
            new_task.is_completed = False
            recurring.append(new_task)
        return recurring


@dataclass
class Pet:
    """Stores a pet's profile, health records, and associated care tasks."""
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
        """Assign a task to this pet and append it to the pet's task list."""
        task.pet_id = self.id
        self.tasks.append(task)

    def remove_task(self, task_id: str) -> None:
        """Delete the task with the given ID from this pet's task list."""
        self.tasks = [t for t in self.tasks if t.id != task_id]

    def edit_task(self, task_id: str, updates: dict) -> None:
        """Apply field updates to the task matching task_id."""
        for task in self.tasks:
            if task.id == task_id:
                task.edit(updates)
                return

    def get_tasks(self) -> list[Task]:
        """Return a shallow copy of this pet's task list."""
        return list(self.tasks)

    def update_dates(self, field_name: str, new_date: date) -> None:
        """Set birthday, last_grooming, or last_medication."""
        valid_fields = {"birthday", "last_grooming", "last_medication"}
        if field_name in valid_fields:
            setattr(self, field_name, new_date)


@dataclass
class Owner:
    """Represents a pet owner with availability windows, preferences, and owned pets."""
    id: str
    name: str
    email: str
    availability: list[TimeWindow] = field(default_factory=list)
    preferences: list[str] = field(default_factory=list)
    pets: list[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Register a new pet under this owner."""
        self.pets.append(pet)

    def remove_pet(self, pet_id: str) -> None:
        """Remove the pet with the given ID from this owner's roster."""
        self.pets = [p for p in self.pets if p.id != pet_id]

    def get_pets(self) -> list[Pet]:
        """Return a shallow copy of this owner's pet list."""
        return list(self.pets)

    def get_all_tasks(self) -> list[Task]:
        """Return every task across all owned pets."""
        all_tasks: list[Task] = []
        for pet in self.pets:
            all_tasks.extend(pet.get_tasks())
        return all_tasks

    def set_availability(self, windows: list[TimeWindow]) -> None:
        """Replace the owner's availability with the provided time windows."""
        self.availability = windows

    def get_availability(self) -> list[TimeWindow]:
        """Return a shallow copy of the owner's availability windows."""
        return list(self.availability)

    def get_preferences(self) -> list[str]:
        """Return a shallow copy of the owner's scheduling preferences."""
        return list(self.preferences)


@dataclass
class Scheduler:
    """Builds and manages a daily care plan for an owner's pets within their availability."""
    date: date
    owner: Owner
    pets: list[Pet] = field(default_factory=list)
    plan: list[ScheduledTask] = field(default_factory=list)
    reasoning: str = ""

    def get_all_tasks_across_pets(self) -> list[Task]:
        """Collect and return every task from all pets in this scheduler."""
        tasks: list[Task] = []
        for pet in self.pets:
            tasks.extend(pet.get_tasks())
        return tasks

    def get_tasks_by_priority(self) -> list[Task]:
        """Return all tasks sorted highest → lowest priority."""
        return sorted(
            self.get_all_tasks_across_pets(),
            key=lambda t: t.priority.value,
            reverse=True,
        )

    def get_tasks_by_date(self, target_date: date) -> list[Task]:
        """Return all tasks scheduled on the given date."""
        return [t for t in self.get_all_tasks_across_pets() if t.date == target_date]

    def generate_plan(self) -> list[ScheduledTask]:
        """
        Build a prioritized schedule for self.date within the owner's availability.

        Tasks with no date set are treated as due today. Completed tasks are
        skipped. Tasks that don't fit in any remaining time window are noted in
        self.reasoning but excluded from self.plan.
        """
        candidates = [
            t for t in self.get_all_tasks_across_pets()
            if not t.is_completed and (t.date is None or t.date == self.date)
        ]
        candidates.sort(key=lambda t: t.priority.value, reverse=True)

        # Fall back to a sensible default if the owner has no availability set.
        windows = self.owner.get_availability() or [TimeWindow("08:00", "20:00")]
        slots = [
            (_time_to_minutes(w.start_time), _time_to_minutes(w.end_time))
            for w in windows
        ]

        scheduled: list[ScheduledTask] = []
        reasoning_lines: list[str] = []
        slot_idx = 0
        current_min = slots[0][0]

        for task in candidates:
            placed = False
            while slot_idx < len(slots):
                slot_start, slot_end = slots[slot_idx]
                if current_min < slot_start:
                    current_min = slot_start
                if current_min + task.duration_minutes <= slot_end:
                    assigned_time = _minutes_to_time(current_min)
                    rationale = (
                        f"Scheduled at {assigned_time} "
                        f"(priority: {task.priority.name}, "
                        f"duration: {task.duration_minutes} min)"
                    )
                    scheduled.append(ScheduledTask(
                        task=task,
                        pet_id=task.pet_id,
                        assigned_time=assigned_time,
                        rationale=rationale,
                    ))
                    reasoning_lines.append(
                        f"- {task.name} [{task.priority.name}] → {assigned_time}"
                        + (f" (pet: {task.pet_id})" if task.pet_id else "")
                    )
                    current_min += task.duration_minutes
                    placed = True
                    break
                else:
                    slot_idx += 1
                    if slot_idx < len(slots):
                        current_min = slots[slot_idx][0]

            if not placed:
                reasoning_lines.append(
                    f"- {task.name} [{task.priority.name}] — could not be scheduled"
                    " (no remaining availability)"
                )

        self.plan = scheduled
        self.reasoning = (
            "\n".join(reasoning_lines) if reasoning_lines else "No tasks to schedule."
        )
        return self.plan

    def add_task(self, scheduled_task: ScheduledTask) -> None:
        """Append a pre-built ScheduledTask directly to the current plan."""
        self.plan.append(scheduled_task)

    def remove_task(self, task_id: str) -> None:
        """Remove the scheduled entry for the given task ID from the plan."""
        self.plan = [st for st in self.plan if st.task.id != task_id]

    def explain_reasoning(self) -> str:
        """Return the human-readable reasoning string produced by the last generate_plan() call."""
        return self.reasoning or "No plan generated yet. Call generate_plan() first."

    def display_plan(self) -> str:
        """Format the current plan as a time-sorted, human-readable string."""
        if not self.plan:
            return "No scheduled tasks. Call generate_plan() first."
        lines = [f"Schedule for {self.date}:"]
        for st in sorted(self.plan, key=lambda x: x.assigned_time):
            end_time = _minutes_to_time(
                _time_to_minutes(st.assigned_time) + st.task.duration_minutes
            )
            lines.append(
                f"  {st.assigned_time}–{end_time}  {st.task.name}"
                f"  [{st.task.type.value} | {st.task.priority.name}]"
                + (f"  pet: {st.pet_id}" if st.pet_id else "")
            )
        return "\n".join(lines)

    def adjust_task(self, task_id: str, new_time: str) -> None:
        """Manually override the assigned time for a task already in the plan."""
        for st in self.plan:
            if st.task.id == task_id:
                st.assigned_time = new_time
                st.rationale += f" [manually adjusted to {new_time}]"
                return
