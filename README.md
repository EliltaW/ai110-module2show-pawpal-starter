# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## Implementation Summary

PawPal+ uses four backend classes in pawpal_system.py.
Owner manages multiple pets and gathers their tasks as
Pet–Task pairs. Pet stores pet details and supports adding tasks.
Task stores care activity details and can be marked complete.

Scheduler has method stubs for the scheduling features that
will be implemented next. The main.py demo currently prints
tasks across two pets. Two pytest tests verify task completion
and task addition.

## 🖥️ Sample Output

Paste a sample of your app's CLI or Streamlit output here so a reader can see what a generated plan looks like:

```
Today's Schedule
08:00 | Buddy | Morning walk | 20 minutes | Priority: high | Not completed
09:00 | Buddy | Feeding | 10 minutes | Priority: high | Not completed
10:00 | Luna | Brushing | 15 minutes | Priority: low | Not completed
```

## 🧪 Testing PawPal+

```bash
# Run the full test suite:
pytest

# Run with coverage:
pytest --cov
```

Sample test output:

```
# Paste your pytest output here
```

## 📐 Smarter Scheduling

> Fill in once you've implemented scheduling logic.

| Feature           | Method(s) | Notes                             |
| ----------------- | --------- | --------------------------------- |
| Task sorting      |           | e.g., by priority, duration       |
| Filtering         |           | e.g., skip tasks if time runs out |
| Conflict handling |           | e.g., overlapping time slots      |
| Recurring tasks   |           | e.g., daily vs. weekly            |

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. <!-- Describe this step -->
2. <!-- Describe this step -->
3. <!-- Describe this step -->
4. <!-- Describe this step -->
5. <!-- Add more steps as needed -->

**Screenshot or video** _(optional)_: <!-- Insert a screenshot or link to a demo video here -->
