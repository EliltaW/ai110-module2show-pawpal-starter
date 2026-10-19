from datetime import date

from pawpal_system import Owner, Pet, Scheduler, Task


owner = Owner("Alex", "Morgan", available_minutes=60)
buddy = Pet(name="Buddy", species="dog", breed="Labrador", age=4)
luna = Pet(name="Luna", species="cat", breed="Domestic Shorthair", age=2)

owner.add_pet(buddy)
owner.add_pet(luna)

brushing = Task(
        description="Brushing",
        due_date=date.today(),
        time="10:00",
        duration_minutes=15,
        priority="low",
        frequency="weekly",
    )
luna.add_task(brushing)

feeding = Task(
    description="Feeding",
    due_date=date.today(),
    time="09:00",
    duration_minutes=10,
    priority="high",
    frequency="daily",
)
feeding.mark_complete()
buddy.add_task(feeding)

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

luna.add_task(
    Task(
        description="Medication",
        due_date=date.today(),
        time="08:00",
        duration_minutes=5,
        priority="high",
        frequency="daily",
    )
)

scheduler = Scheduler(owner)

print("Today's Schedule")
for pet, task in scheduler.sort_by_time():
    completion_status = "Completed" if task.is_completed else "Not completed"
    print(
        f"{task.due_date} {task.time} | {pet.name} | {task.description} | "
        f"{task.duration_minutes} minutes | Priority: {task.priority} | "
        f"{completion_status}"
    )

print("\nBuddy's unfinished tasks")
for pet, task in scheduler.filter_tasks(pet_name="Buddy", is_completed=False):
    print(
        f"{task.due_date} {task.time} | {pet.name} | {task.description} | "
        f"{task.duration_minutes} minutes | Priority: {task.priority} | "
        "Not completed"
    )

print("\nConflict warnings")
for warning in scheduler.detect_conflicts():
    print(warning)

for pet, task in scheduler.filter_tasks(pet_name="Buddy", is_completed=False):
    if task.description == "Morning walk":
        scheduler.mark_task_complete(pet, task)
        break

print("\nSchedule after completing the daily walk")
for pet, task in scheduler.sort_by_time():
    completion_status = "Completed" if task.is_completed else "Not completed"
    print(
        f"{task.due_date} {task.time} | {pet.name} | {task.description} | "
        f"{task.duration_minutes} minutes | Priority: {task.priority} | "
        f"{completion_status}"
    )

owner.available_minutes = 10
daily_plan = scheduler.generate_daily_plan()
print("\nToday's plan — 10-minute budget")
total_duration = 0
for pet, task in daily_plan:
    print(
        f"{pet.name} | {task.description} | {task.time} | "
        f"{task.duration_minutes} minutes | Priority: {task.priority}"
    )
    total_duration += task.duration_minutes
print(f"Total selected duration: {total_duration} minutes")
