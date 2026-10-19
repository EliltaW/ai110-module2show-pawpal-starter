from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, timedelta


class Owner:
    """Store owner details and the owner's pets."""

    def __init__(
        self,
        first_name: str,
        last_name: str,
        available_minutes: int,
        pets: list[Pet] | None = None,
    ) -> None:
        self.first_name = first_name
        self.last_name = last_name
        self.available_minutes = available_minutes
        self.pets = list(pets) if pets is not None else []

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner."""
        self.pets.append(pet)

    def get_all_tasks(self) -> list[tuple[Pet, Task]]:
        """Return task pairs for all pets."""
        result = []
        for pet in self.pets:
            for task in pet.tasks:
                result.append((pet, task))
        return result


@dataclass
class Pet:
    """Represent a pet and its care tasks."""

    name: str
    species: str
    breed: str
    age: int
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a task to this pet."""
        self.tasks.append(task)


@dataclass
class Task:
    """Represent one scheduled pet-care task."""

    description: str
    due_date: date
    time: str
    duration_minutes: int
    priority: str
    frequency: str
    is_completed: bool = False

    def mark_complete(self) -> None:
        """Mark this task as complete."""
        self.is_completed = True


class Scheduler:
    """Provide scheduling operations for one owner."""

    def __init__(self, owner: Owner) -> None:
        self.owner = owner

    def sort_by_time(self) -> list[tuple[Pet, Task]]:
        """Return task pairs sorted by due date and start time."""
        return sorted(
            self.owner.get_all_tasks(),
            key=lambda pair: (pair[1].due_date, pair[1].time),
        )

    def filter_tasks(
        self,
        pet_name: str | None = None,
        is_completed: bool | None = None,
    ) -> list[tuple[Pet, Task]]:
        """Return task pairs matching the supplied pet and status filters."""
        result = []
        for pet, task in self.owner.get_all_tasks():
            if pet_name is not None and pet.name.casefold() != pet_name.casefold():
                continue
            if is_completed is not None and task.is_completed != is_completed:
                continue
            result.append((pet, task))
        return result

    def detect_conflicts(self) -> list[str]:
        """Return warnings for unfinished tasks sharing a date and start time."""
        tasks = [
            pair for pair in self.owner.get_all_tasks() if not pair[1].is_completed
        ]
        warnings = []
        for index, (pet, task) in enumerate(tasks):
            for other_pet, other_task in tasks[index + 1 :]:
                if (
                    task.due_date == other_task.due_date
                    and task.time == other_task.time
                ):
                    warnings.append(
                        f"Conflict on {task.due_date} at {task.time}: "
                        f"{pet.name} - {task.description} and "
                        f"{other_pet.name} - {other_task.description}."
                    )
        return warnings

    def generate_daily_plan(self) -> list[tuple[Pet, Task]]:
        """Select today's unfinished tasks within the owner's time budget."""
        priority_rank = {"high": 0, "medium": 1, "low": 2}
        candidates = [
            pair
            for pair in self.owner.get_all_tasks()
            if pair[1].due_date == date.today() and not pair[1].is_completed
        ]
        candidates.sort(
            key=lambda pair: (priority_rank[pair[1].priority], pair[1].time)
        )

        remaining_minutes = self.owner.available_minutes
        selected = []
        for pair in candidates:
            task = pair[1]
            if task.duration_minutes <= remaining_minutes:
                selected.append(pair)
                remaining_minutes -= task.duration_minutes

        return sorted(
            selected,
            key=lambda pair: (pair[1].due_date, pair[1].time),
        )

    def mark_task_complete(self, pet: Pet, task: Task) -> None:
        """Complete an owned task and add its next daily or weekly occurrence."""
        if not any(owner_pet is pet for owner_pet in self.owner.pets):
            raise ValueError("Pet does not belong to this owner.")
        if not any(pet_task is task for pet_task in pet.tasks):
            raise ValueError("Task does not belong to this pet.")
        if task.is_completed:
            return

        task.mark_complete()

        if task.frequency == "daily":
            due_date = date.today() + timedelta(days=1)
        elif task.frequency == "weekly":
            due_date = date.today() + timedelta(days=7)
        else:
            return

        pet.add_task(
            Task(
                description=task.description,
                due_date=due_date,
                time=task.time,
                duration_minutes=task.duration_minutes,
                priority=task.priority,
                frequency=task.frequency,
                is_completed=False,
            )
        )