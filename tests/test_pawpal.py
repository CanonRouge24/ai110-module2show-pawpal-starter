import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from pawpal_system import Task, Pet, TaskType, Priority


def test_mark_complete_changes_status():
    task = Task(id="1", name="Walk", type=TaskType.WALK, duration_minutes=30, priority=Priority.MEDIUM)
    assert task.is_completed is False
    task.mark_complete()
    assert task.is_completed is True


def test_add_task_increases_pet_task_count():
    pet = Pet(id="p1", name="Buddy", species="dog", breed="Lab", age=3, weight_lbs=60.0)
    task = Task(id="2", name="Feed", type=TaskType.FEEDING, duration_minutes=10, priority=Priority.HIGH)
    assert len(pet.tasks) == 0
    pet.add_task(task)
    assert len(pet.tasks) == 1
