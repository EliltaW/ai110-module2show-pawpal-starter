from datetime import date, timedelta

from pawpal_system import Owner, Pet, Scheduler, Task


def make_task(
    description: str,
    due_date: date,
    time: str = "09:00",
    duration_minutes: int = 15,
    priority: str = "medium",
    frequency: str = "once",
    is_completed: bool = False,
) -> Task:
    return Task(
        description=description,
        due_date=due_date,
        time=time,
        duration_minutes=duration_minutes,
        priority=priority,
        frequency=frequency,
        is_completed=is_completed,
    )


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


def test_sort_by_time_orders_dates_and_times_across_pets_stably() -> None:
    today = date.today()
    yesterday = today - timedelta(days=1)
    tomorrow = today + timedelta(days=1)
    first_pet = Pet(name="Buddy", species="dog", breed="Labrador", age=4)
    second_pet = Pet(name="Milo", species="cat", breed="Tabby", age=3)
    later_task = make_task("Evening walk", today, "18:00")
    first_tie = make_task("Morning walk", today, "08:00")
    second_tie = make_task("Breakfast", today, "08:00")
    earlier_date_task = make_task("Dinner", yesterday, "19:00")
    later_date_task = make_task("Vet visit", tomorrow, "10:00")
    first_pet.tasks.extend([later_task, first_tie, later_date_task])
    second_pet.tasks.extend([earlier_date_task, second_tie])
    scheduler = Scheduler(Owner("Alex", "Rivera", 60, [first_pet, second_pet]))

    sorted_tasks = scheduler.sort_by_time()

    assert sorted_tasks == [
        (second_pet, earlier_date_task),
        (first_pet, first_tie),
        (second_pet, second_tie),
        (first_pet, later_task),
        (first_pet, later_date_task),
    ]


def test_filter_tasks_can_select_incomplete_tasks() -> None:
    today = date.today()
    pet = Pet(name="Buddy", species="dog", breed="Labrador", age=4)
    incomplete_task = make_task("Walk", today)
    completed_task = make_task("Feed", today, is_completed=True)
    pet.tasks.extend([incomplete_task, completed_task])
    scheduler = Scheduler(Owner("Alex", "Rivera", 60, [pet]))

    filtered_tasks = scheduler.filter_tasks(is_completed=False)

    assert filtered_tasks == [(pet, incomplete_task)]


def test_filter_tasks_combines_pet_name_and_completion_status() -> None:
    today = date.today()
    buddy = Pet(name="Buddy", species="dog", breed="Labrador", age=4)
    milo = Pet(name="Milo", species="cat", breed="Tabby", age=3)
    buddy_task = make_task("Walk", today)
    buddy_completed_task = make_task("Feed", today, is_completed=True)
    milo_task = make_task("Play", today)
    buddy.tasks.extend([buddy_task, buddy_completed_task])
    milo.tasks.append(milo_task)
    scheduler = Scheduler(Owner("Alex", "Rivera", 60, [buddy, milo]))

    filtered_tasks = scheduler.filter_tasks(pet_name="bUdDy", is_completed=False)

    assert filtered_tasks == [(buddy, buddy_task)]


def test_mark_daily_task_complete_preserves_original_and_adds_tomorrow() -> None:
    today = date.today()
    pet = Pet(name="Buddy", species="dog", breed="Labrador", age=4)
    original_task = make_task(
        "Morning walk", today, "08:30", 25, "high", "daily"
    )
    pet.add_task(original_task)
    scheduler = Scheduler(Owner("Alex", "Rivera", 60, [pet]))

    scheduler.mark_task_complete(pet, original_task)

    recurring_task = pet.tasks[1]
    assert len(pet.tasks) == 2
    assert pet.tasks[0] is original_task
    assert original_task.is_completed is True
    assert recurring_task is not original_task
    assert recurring_task.due_date == today + timedelta(days=1)
    assert recurring_task.description == original_task.description
    assert recurring_task.time == original_task.time
    assert recurring_task.duration_minutes == original_task.duration_minutes
    assert recurring_task.priority == original_task.priority
    assert recurring_task.frequency == original_task.frequency
    assert recurring_task.is_completed is False


def test_mark_weekly_task_complete_adds_occurrence_seven_days_later() -> None:
    today = date.today()
    pet = Pet(name="Milo", species="cat", breed="Tabby", age=3)
    original_task = make_task("Brush", today, "10:00", 10, "low", "weekly")
    pet.add_task(original_task)
    scheduler = Scheduler(Owner("Alex", "Rivera", 60, [pet]))

    scheduler.mark_task_complete(pet, original_task)

    recurring_task = pet.tasks[1]
    assert len(pet.tasks) == 2
    assert original_task.is_completed is True
    assert recurring_task is not original_task
    assert recurring_task.due_date == today + timedelta(days=7)
    assert recurring_task.description == original_task.description
    assert recurring_task.time == original_task.time
    assert recurring_task.duration_minutes == original_task.duration_minutes
    assert recurring_task.priority == original_task.priority
    assert recurring_task.frequency == original_task.frequency
    assert recurring_task.is_completed is False


def test_repeated_completion_does_not_add_duplicate_recurrence() -> None:
    today = date.today()
    pet = Pet(name="Buddy", species="dog", breed="Labrador", age=4)
    original_task = make_task("Walk", today, frequency="daily")
    pet.add_task(original_task)
    scheduler = Scheduler(Owner("Alex", "Rivera", 60, [pet]))

    scheduler.mark_task_complete(pet, original_task)
    first_recurring_task = pet.tasks[1]
    scheduler.mark_task_complete(pet, original_task)

    assert len(pet.tasks) == 2
    assert pet.tasks[1] is first_recurring_task
    assert original_task.is_completed is True


def test_detect_conflicts_reports_same_date_and_time_across_pets() -> None:
    today = date.today()
    buddy = Pet(name="Buddy", species="dog", breed="Labrador", age=4)
    milo = Pet(name="Milo", species="cat", breed="Tabby", age=3)
    buddy_task = make_task("Walk", today, "09:00")
    milo_task = make_task("Feed", today, "09:00")
    buddy.add_task(buddy_task)
    milo.add_task(milo_task)
    scheduler = Scheduler(Owner("Alex", "Rivera", 60, [buddy, milo]))

    warnings = scheduler.detect_conflicts()

    assert len(warnings) == 1
    assert "09:00" in warnings[0]
    assert "Buddy" in warnings[0]
    assert "Walk" in warnings[0]
    assert "Milo" in warnings[0]
    assert "Feed" in warnings[0]


def test_detect_conflicts_ignores_same_time_when_one_task_is_completed() -> None:
    today = date.today()
    buddy = Pet(name="Buddy", species="dog", breed="Labrador", age=4)
    milo = Pet(name="Milo", species="cat", breed="Tabby", age=3)
    completed_task = make_task("Walk", today, "09:00", is_completed=True)
    unfinished_task = make_task("Feed", today, "09:00")
    buddy.add_task(completed_task)
    milo.add_task(unfinished_task)
    scheduler = Scheduler(Owner("Alex", "Rivera", 60, [buddy, milo]))

    warnings = scheduler.detect_conflicts()

    assert warnings == []


def test_detect_conflicts_ignores_same_time_on_different_dates() -> None:
    today = date.today()
    tomorrow = today + timedelta(days=1)
    buddy = Pet(name="Buddy", species="dog", breed="Labrador", age=4)
    milo = Pet(name="Milo", species="cat", breed="Tabby", age=3)
    today_task = make_task("Walk", today, "09:00")
    tomorrow_task = make_task("Feed", tomorrow, "09:00")
    buddy.add_task(today_task)
    milo.add_task(tomorrow_task)
    scheduler = Scheduler(Owner("Alex", "Rivera", 60, [buddy, milo]))

    warnings = scheduler.detect_conflicts()

    assert warnings == []


def test_daily_plan_prioritizes_tasks_and_includes_exact_budget_fit() -> None:
    today = date.today()
    pet = Pet(name="Buddy", species="dog", breed="Labrador", age=4)
    high_priority_task = make_task("Walk", today, "11:00", 20, "high")
    medium_priority_task = make_task("Feed", today, "09:00", 10, "medium")
    low_priority_task = make_task("Play", today, "08:00", 1, "low")
    pet.tasks.extend(
        [high_priority_task, medium_priority_task, low_priority_task]
    )
    scheduler = Scheduler(Owner("Alex", "Rivera", 30, [pet]))

    daily_plan = scheduler.generate_daily_plan()

    assert daily_plan == [
        (pet, medium_priority_task),
        (pet, high_priority_task),
    ]


def test_daily_plan_skips_oversized_task_and_selects_later_fitting_tasks() -> None:
    today = date.today()
    pet = Pet(name="Buddy", species="dog", breed="Labrador", age=4)
    oversized_task = make_task("Long walk", today, "07:00", 11, "high")
    fitting_task = make_task("Feed", today, "08:00", 7, "medium")
    exact_fit_task = make_task("Play", today, "09:00", 3, "low")
    pet.tasks.extend([oversized_task, fitting_task, exact_fit_task])
    scheduler = Scheduler(Owner("Alex", "Rivera", 10, [pet]))

    daily_plan = scheduler.generate_daily_plan()

    assert daily_plan == [(pet, fitting_task), (pet, exact_fit_task)]


def test_daily_plan_with_zero_budget_selects_no_positive_duration_tasks() -> None:
    today = date.today()
    pet = Pet(name="Buddy", species="dog", breed="Labrador", age=4)
    pet.add_task(make_task("Walk", today, duration_minutes=1))
    scheduler = Scheduler(Owner("Alex", "Rivera", 0, [pet]))

    daily_plan = scheduler.generate_daily_plan()

    assert daily_plan == []


def test_daily_plan_excludes_completed_and_future_tasks() -> None:
    today = date.today()
    tomorrow = today + timedelta(days=1)
    pet = Pet(name="Buddy", species="dog", breed="Labrador", age=4)
    completed_task = make_task("Feed", today, is_completed=True)
    future_task = make_task("Walk", tomorrow)
    pet.tasks.extend([completed_task, future_task])
    scheduler = Scheduler(Owner("Alex", "Rivera", 60, [pet]))

    daily_plan = scheduler.generate_daily_plan()

    assert daily_plan == []


def test_scheduler_operations_return_empty_for_no_pets_and_pets_without_tasks() -> None:
    empty_owner_scheduler = Scheduler(Owner("Alex", "Rivera", 60))
    pet_without_tasks = Pet(name="Buddy", species="dog", breed="Labrador", age=4)
    empty_pet_scheduler = Scheduler(
        Owner("Alex", "Rivera", 60, [pet_without_tasks])
    )

    empty_owner_results = (
        empty_owner_scheduler.sort_by_time(),
        empty_owner_scheduler.filter_tasks(),
        empty_owner_scheduler.detect_conflicts(),
        empty_owner_scheduler.generate_daily_plan(),
    )
    empty_pet_results = (
        empty_pet_scheduler.sort_by_time(),
        empty_pet_scheduler.filter_tasks(is_completed=False),
        empty_pet_scheduler.detect_conflicts(),
        empty_pet_scheduler.generate_daily_plan(),
    )

    assert empty_owner_scheduler.owner.get_all_tasks() == []
    assert empty_owner_results == ([], [], [], [])
    assert empty_pet_results == ([], [], [], [])
