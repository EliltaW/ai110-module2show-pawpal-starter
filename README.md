# PawPal+ (Module 2 Project)

**PawPal+** helps pet owners manage care tasks and build a daily plan around priorities and available time.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

The app keeps data in memory for the current session only; it is not saved permanently.

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Run the app, demo, and tests

```bash
streamlit run app.py
python main.py
python -m pytest
```

## Implementation Summary

PawPal+ is implemented with four backend classes in `pawpal_system.py`. `Owner` manages pets and gathers their tasks as pet-task pairs. `Pet` stores pet details and tasks, and `Task` stores care details and completion status. `Scheduler` implements sorting, filtering, conflict detection, daily planning, and completion with daily or weekly recurrence.

The Streamlit UI supports owner and pet information, task creation and editing, task completion, display filters, conflict warnings, and daily plan generation. The completion control is disabled for future-dated tasks. The CLI example is in `main.py`.

## Features

- Manage owner details, available care minutes, and multiple pets.
- Add and edit care tasks with due date, time, duration, priority, and frequency.
- Filter the task table by pet name and completion status, and display tasks chronologically.
- Complete today's and overdue unfinished tasks; daily and weekly tasks create their next occurrence. Future tasks remain visible but cannot be completed early in the UI.
- Warn about unfinished tasks sharing a date and start time; warnings require manual review.
- Build a plan from today's unfinished tasks by priority, selecting tasks that fit the available time and displaying the selection chronologically.
- Keep application data for the current session only; no permanent storage is implemented.

The final class diagram is [diagrams/uml_final.mmd](diagrams/uml_final.mmd).

## CLI Demo Output

Captured by running `python main.py`:

```text
Today's Schedule
2026-10-18 08:00 | Buddy | Morning walk | 20 minutes | Priority: high | Not completed
2026-10-18 08:00 | Luna | Medication | 5 minutes | Priority: high | Not completed
2026-10-18 09:00 | Buddy | Feeding | 10 minutes | Priority: high | Completed
2026-10-18 10:00 | Luna | Brushing | 15 minutes | Priority: low | Not completed

Buddy's unfinished tasks
2026-10-18 08:00 | Buddy | Morning walk | 20 minutes | Priority: high | Not completed

Conflict warnings
Conflict on 2026-10-18 at 08:00: Buddy - Morning walk and Luna - Medication.

Schedule after completing the daily walk
2026-10-18 08:00 | Buddy | Morning walk | 20 minutes | Priority: high | Completed
2026-10-18 08:00 | Luna | Medication | 5 minutes | Priority: high | Not completed
2026-10-18 09:00 | Buddy | Feeding | 10 minutes | Priority: high | Completed
2026-10-18 10:00 | Luna | Brushing | 15 minutes | Priority: low | Not completed
2026-10-19 08:00 | Buddy | Morning walk | 20 minutes | Priority: high | Not completed

Today's plan — 10-minute budget
Luna | Medication | 08:00 | 5 minutes | Priority: high
Total selected duration: 5 minutes
```

## 🧪 Testing PawPal+

Run the test suite:

```bash
python -m pytest
```

The 16 tests cover task addition and completion, sorting, filtering, daily and weekly recurrence, duplicate prevention, conflict detection, daily-plan budgets, and empty collections.

### Test Results

```text
=================================== 16 passed in 0.08s ===================================
```

Confidence level: (4/5). All 16 automated tests pass,
and core browser workflows were manually checked. Conflict
detection checks exact start times rather than overlapping
durations, and data is stored only for the current session.

## 📐 Smarter Scheduling

| Feature    | Method                            | Behavior                                                                                                                                                           |
| ---------- | --------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Sorting    | `Scheduler.sort_by_time()`        | Sorts by due date, then HH:MM start time.                                                                                                                          |
| Filtering  | `Scheduler.filter_tasks()`        | Filters by pet name (case-insensitive), completion status, or both.                                                                                                |
| Conflicts  | `Scheduler.detect_conflicts()`    | Warns about unfinished tasks with matching dates and start times, including across pets.                                                                           |
| Recurrence | `Scheduler.mark_task_complete()`  | Keeps the completed original and creates an unfinished task 1 day from today for daily tasks or 7 days for weekly tasks. Repeated completion creates no duplicate. |
| Daily plan | `Scheduler.generate_daily_plan()` | Selects today's unfinished tasks by priority within the time budget, skips tasks that do not fit, and displays selected tasks chronologically.                     |

Conflict warnings do not automatically resolve conflicts. Overlapping durations are not detected.

## 📸 Demo Walkthrough

1. Enter the owner's first and last name and set the available care time in minutes.
2. Add multiple pets with each pet's name, species, breed, and age.
3. Add tasks for a pet, then use **Edit a task** to change its description, due date, time, duration, priority, or frequency.
4. Use the task-table filters to show all pets or a pet name, and all, unfinished, or completed tasks. Pet-name filtering includes every pet that shares that name.
5. Complete an eligible unfinished task with **Mark complete**. The UI disables this button for future tasks and explains they can be completed on their due date. Completing a daily or weekly task keeps the original completed and adds its next occurrence.
6. Review conflict warnings for unfinished tasks with the same date and start time. Warnings are not automatically resolved; check them manually.
7. Select **Generate schedule** to choose today's unfinished tasks by priority within the available-time budget. Tasks that fit are displayed by time with selected and available minutes shown.
