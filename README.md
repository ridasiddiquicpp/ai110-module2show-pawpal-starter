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


## System Overview

In pawpal_system.py I added 4 main classes, Task, Pet, Owner, and Scheduler.

The Task class is used to create a task, with description, due time, duration, priority, frequency, and completion status. It has methods to mark task complete, reschedule, and create a copy of a repeating task.

A task can be assigned to a certain pet. You can add a task to a certain pet.

The pet class stores the pet details and its own list of tasks. It has methods like add_task and remove_task, which keep task and pet linked in both directions.

The owner class stores a list of all pets, and the get_all_tasks method returns every pet's tasks together.

The scheduler class is given an Owner and reads all the owner's tasks. It can get the daily schedule using owner.get_all_tasks, filter tasks by pet or completion status, sort by time and priority, create the next task when a repeating task is completed, and detect conflicts.

When you complete a daily task, Scheduler.mark_task_complete marks it done, asks the task for next_occurrence, and adds the new task to the same pet.
 
When you add a task through Scheduler.add_task, it rejects a task that overlaps another on the same pet and warns if it overlaps a different pet's task.

An owner has pets, each pet has tasks, and the Scheduler works on top of the owner to read and manage all of them.



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
Today's Schedule
08:00:AM - Misty - give medicine - 5 minutes
09:00:AM - Cheeto - vet appointment - 60 minutes
12:00:PM - Cheeto - grooming - 45 minutes
05:00:PM - Cheeto - playtime - 30 minutes
06:00:PM - Misty - evening walk - 30 minutes

Tasks by Priority
high - 08:00:AM - Misty - give medicine - 5 minutes
high - 09:00:AM - Cheeto - vet appointment - 60 minutes
high - 06:00:PM - Misty - evening walk - 30 minutes
medium - 05:00:PM - Cheeto - playtime - 30 minutes
medium - 07:30:AM - Misty - breakfast - 15 minutes
low - 12:00:PM - Cheeto - grooming - 45 minutes

Recurring tasks
Tasks before: 6
Tasks after: 7
Next walk: 10/17 06:00 PM - Misty - id 7
Next vet (once): None
Second completion of walk: None

Conflict detection
Before adding conflicts: no conflicts
Adding bath: no conflicts
WARNING (different pets): 'nail trim' (Cheeto, 10/16 10:00 AM-10:15 AM) overlaps 'bath' (Misty, 10/16 10:00 AM-10:30 AM)
REJECTED: Misty already has 'bath' (10/16 10:00 AM-10:30 AM) at that time
All conflicts now: 1

Raw order (as added)
10/16 09:00 AM - Cheeto - vet appointment - done
10/16 05:00 PM - Cheeto - playtime - pending
10/16 12:00 PM - Cheeto - grooming - pending
10/16 10:00 AM - Cheeto - nail trim - pending
10/16 06:00 PM - Misty - evening walk - done
10/17 07:30 AM - Misty - breakfast - pending
10/16 08:00 AM - Misty - give medicine - done
10/17 06:00 PM - Misty - evening walk - pending
10/16 10:00 AM - Misty - bath - pending

Sorted by time
10/16 08:00 AM - Misty - give medicine - done
10/16 09:00 AM - Cheeto - vet appointment - done
10/16 10:00 AM - Cheeto - nail trim - pending
10/16 10:00 AM - Misty - bath - pending
10/16 12:00 PM - Cheeto - grooming - pending
10/16 05:00 PM - Cheeto - playtime - pending
10/16 06:00 PM - Misty - evening walk - done
10/17 07:30 AM - Misty - breakfast - pending
10/17 06:00 PM - Misty - evening walk - pending

Incomplete tasks
10/16 05:00 PM - Cheeto - playtime - pending
10/16 12:00 PM - Cheeto - grooming - pending
10/16 10:00 AM - Cheeto - nail trim - pending
10/17 07:30 AM - Misty - breakfast - pending
10/17 06:00 PM - Misty - evening walk - pending
10/16 10:00 AM - Misty - bath - pending

Completed tasks
10/16 09:00 AM - Cheeto - vet appointment - done
10/16 06:00 PM - Misty - evening walk - done
10/16 08:00 AM - Misty - give medicine - done

Misty's tasks
10/16 06:00 PM - Misty - evening walk - done
10/17 07:30 AM - Misty - breakfast - pending
10/16 08:00 AM - Misty - give medicine - done
10/17 06:00 PM - Misty - evening walk - pending
10/16 10:00 AM - Misty - bath - pending
```

## 🧪 Testing PawPal+

Run from the project folder:
`ai110-module2show-pawpal-starter`

Command to run tests:
python -m pytest


Command to run test with each test name:
python -m pytest -v


Description of what tests cover:
These tests cover sorting by time and pets, making sure with recurring tasks that completing a daily/weekly task creates another one, conflicting tasks are either rejected or gives a warning, validating and making sure unknown frequency or priority values are rejected. Also adding task to a pet, and marking a task complete is tested


Output of successful test run:
```
============================= test session starts =============================
platform win32 -- Python 3.13.15, pytest-9.1.1, pluggy-1.7.0
rootdir: C:\Users\Rida\Desktop\CodePathProject2\ai110-module2show-pawpal-starter
plugins: anyio-4.15.1
collected 29 items

tests\test_pawpal.py .............................                       [100%]

============================= 29 passed in 0.02s ==============================
```

Confidence Level:
4 stars 

I'm giving 4 stars because all 29 tests pass, and they cover sorting, recurring tasks, conflict detection and input validation, including some edge cases. 
I'm not giving 5 stars because some methods don't have direct tests, such as filter_tasks and get_daily_schedule. These along with more edge case tests can be added to be more extensive, and the Streamlit UI isn't tested.


## 📐 Smarter Scheduling


| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Sorting by time | `Scheduler.sort_by_time`, `get_daily_schedule` | Sorts in chronological order (earliest date and time first). `get_daily_schedule` returns only one day's tasks, sorted by time.
 |
| Sorting by priority | `Scheduler.sort_by_priority` | Sorts by priority, high, medium, or low. |
| Filtering | `Scheduler.filter_tasks`, `get_tasks_by_pet`, `get_upcoming_tasks` | Filters by completion status or pet name. |
| Conflict detection | `Scheduler.detect_conflicts`, `get_conflict_warnings` | Detects pairs of incomplete tasks whose time windows overlap, across pets.  |
| Conflict prevention | `Scheduler.add_task` | Rejects a task that overlaps another on the same pet. Overlaps across different pets only gives a warning. |
| Recurring tasks | `Task.next_occurrence`, `Scheduler.mark_task_complete` | Completing a daily or weekly task creates the next copy one day or week after its due time and adds it to the same pet.  |



## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

A User can add an owner, multiple pets, and task for those pets. A warning is given if two tasks are added at same times for different pets, but the task is still added. 
If two task are added for the same pet at the same time, then it is rejected. 
In 'Your Tasks' sections, the user can sort the tasks by time and priority. The user can also filter by pet and by completion status.
After a user marks a task as complete, a green check mark is shown next to the task, on the done column.

1. Run 'streamlit run app.py'
2. In 'Basic Information' section, enter Jordan in 'Owner name' box
3. Type Mochi in 'Pet name' box and dog in 'species' box. Click 'Add pet'
4. Type Max in 'Pet name' box and dog in 'species' box. Click 'Add pet'
5. In 'Tasks' section, pick Mochi from dropdown and add Morning walk with frequency set to daily with low priority with time 8:00AM on Oct 18, 2026
6. Pick Max from dropdown and add Vet Appointment with frequency set to once with high priority with time 9:00AM on Oct 18, 2026
7. Now in 'Your Tasks' section you can sort by priority or time and see the difference.
8. Can filter by pet, either pick Max, Mochi, or all to see different tasks
9. Use the dropdown beloe 'Mark a task complete' and select 'Mochi - Morning walk (Oct 18, 08:00 AM)' and then press the 'Mark complete' button
10. Notice the same task is created for the next day. And the today's task is marked as done.
11. Use 'Status' dropdown to see all complete, incomplete, or all tasks
12. On the 'Build Schedule' section pick 2026/10/18 from calendar and click 'Generate Schedule' button.
13. It shows all the tasks for that day and also if they are complete or incomplete.

14. In the 'Tasks' section select Max from dropdown and add playtime with time 6:00PM on Oct 18, 2026 
15. Repeat number 14
16. You will see that this task is not added, because it has same pet at same time.
15. In the 'Tasks' section select Mochi from dropdown and add walk with time 6:00PM on Oct 18, 2026 
16. A warning is shown that both are scheduled at same time, but the task is still added



**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
