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

User can enter pet info
user can enter owner info
add or edit tasks
delete tasks
chedule walk
see tasks

Owner
Pet
Task
Scheduler

## System Overview

written by AI

PawPal+ is built from four classes in `pawpal_system.py`:

- **Task**: one care activity (description, type, due time, duration, priority, frequency, completion status). It knows which pet it belongs to. `mark_complete()` finishes it, `reschedule()` moves it, and `end_time` is calculated from the due time plus the duration.
- **Pet**: stores pet details and its own list of tasks. `add_task()` and `remove_task()` keep the task and pet linked in both directions.
- **Owner**: manages multiple pets. `get_all_tasks()` returns every pet's tasks together in one list.
- **Scheduler**: the "brain". It is given an Owner and reads tasks through `owner.get_all_tasks()`, so it works across all pets instead of one. It does not store its own copy of the tasks.

written by AI

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

## 🖥️ Sample Output

Paste a sample of your app's CLI or Streamlit output here so a reader can see what a generated plan looks like:


```
# e.g.:
# Daily plan for Biscuit (Golden Retriever):
#   08:00 — Morning walk (30 min) [priority: high]
#   09:00 — Feeding (10 min) [priority: high]
#   ...
```

Today's Schedule
09:00:AM - Cheeto - vet appointment - 60 minutes
05:00:PM - Cheeto - playtime - 30 minutes
06:00:PM - Misty - evening walk - 30 minutes

Tasks by Priority
high - 09:00:AM - Cheeto - vet appointment - 60 minutes
high - 06:00:PM - Misty - evening walk - 30 minutes
medium - 05:00:PM - Cheeto - playtime - 30 minutes

## 🧪 Testing PawPal+

written by AI

**Run the demo** (prints today's schedule and the tasks sorted by priority). Run from the project folder, `ai110-module2show-pawpal-starter`:

```bash
python main.py
```

**Run the tests** from the same folder. Use `python -m pytest` so the tests can import `pawpal_system.py`:

```bash
python -m pytest -v
```

**Test coverage summary:**

- `test_mark_complete`: calling `mark_complete()` changes a task from incomplete to complete.
- `test_add_task`: adding a task to a pet increases that pet's task count by one.
- `test_detect_conflicts`: two overlapping tasks on different pets are reported as one conflicting pair.

Sample test output:

```
============================= test session starts =============================
collecting ... collected 3 items

tests/test_pawpal.py::test_mark_complete PASSED                          [ 33%]
tests/test_pawpal.py::test_add_task PASSED                               [ 66%]
tests/test_pawpal.py::test_detect_conflicts PASSED                       [100%]

============================== 3 passed in 0.02s ==============================
```

written by AI

## 📐 Smarter Scheduling

written by AI

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | `Scheduler.sort_by_priority`, `get_daily_schedule` | Priority first (high, medium, low), then earliest time. The daily schedule is ordered by time. |
| Filtering | `get_daily_schedule`, `get_tasks_by_pet`, `get_upcoming_tasks` | By day, by pet, or incomplete tasks still ahead. All read from every pet's tasks. |
| Conflict handling | `Scheduler.detect_conflicts` | Returns pairs of incomplete tasks whose time windows overlap, including across different pets. Back-to-back tasks are not a conflict. |
| Recurring tasks | `Task.frequency` | Each task stores "once", "daily" or "weekly". The schedule does not expand recurring tasks yet. |

written by AI

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. <!-- Describe this step -->
2. <!-- Describe this step -->
3. <!-- Describe this step -->
4. <!-- Describe this step -->
5. <!-- Add more steps as needed -->

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
