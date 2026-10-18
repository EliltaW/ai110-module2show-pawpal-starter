from datetime import date

from pawpal_system import Pet, Task


def test_task_mark_complete() -> None:
    task = Task(
        description="Morning walk",
        due_date=date.today(),
        time="08:00",
        duration_minutes=20,
        priority="high",
        frequency="daily",
    )

    assert task.is_completed is False

    task.mark_complete()

    assert task.is_completed is True


def test_pet_add_task() -> None:
    pet = Pet(name="Buddy", species="dog", breed="Labrador", age=4)
    task = Task(
        description="Morning walk",
        due_date=date.today(),
        time="08:00",
        duration_minutes=20,
        priority="high",
        frequency="daily",
    )
    initial_task_count = len(pet.tasks)

    pet.add_task(task)

    assert len(pet.tasks) == initial_task_count + 1
    assert pet.tasks[-1] is task
