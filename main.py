from datetime import date

from pawpal_system import Owner, Pet, Task


owner = Owner("Alex", "Morgan", available_minutes=60)
buddy = Pet(name="Buddy", species="dog", breed="Labrador", age=4)
luna = Pet(name="Luna", species="cat", breed="Domestic Shorthair", age=2)

owner.add_pet(buddy)
owner.add_pet(luna)

buddy.add_task(
    Task(
        description="Morning walk",
        due_date=date.today(),
        time="08:00",
        duration_minutes=20,
        priority="high",
        frequency="daily",
    )
)
buddy.add_task(
    Task(
        description="Feeding",
        due_date=date.today(),
        time="09:00",
        duration_minutes=10,
        priority="high",
        frequency="daily",
    )
)
luna.add_task(
    Task(
        description="Brushing",
        due_date=date.today(),
        time="10:00",
        duration_minutes=15,
        priority="low",
        frequency="weekly",
    )
)

print("Today's Schedule")
for pet, task in owner.get_all_tasks():
    completion_status = "Completed" if task.is_completed else "Not completed"
    print(
        f"{task.time} | {pet.name} | {task.description} | "
        f"{task.duration_minutes} minutes | Priority: {task.priority} | "
        f"{completion_status}"
    )
