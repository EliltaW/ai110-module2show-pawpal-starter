from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date


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
        """Return tasks in chronological order."""
        pass

    def filter_tasks(
        self,
        pet_name: str | None = None,
        is_completed: bool | None = None,
    ) -> list[tuple[Pet, Task]]:
        """Return tasks matching the optional filters."""
        pass

    def detect_conflicts(self) -> list[str]:
        """Identify tasks with matching dates and start times."""
        pass

    def generate_daily_plan(self) -> list[tuple[Pet, Task]]:
        """Return a daily plan within the owner's time limit."""
        pass

    def mark_task_complete(self, pet: Pet, task: Task) -> None:
        """Mark a task complete and handle recurrence."""
        pass