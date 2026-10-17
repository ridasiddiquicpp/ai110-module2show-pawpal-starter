# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

I included classes Owner, Pet, Task, and Scheduler.
The owner can add, remove, and get pets. Pet has tasks, it can add, remove, and get tasks.
A task can be rescheduled or marked as complete.
Scheduler is where you find out what task the owner should do and when. So it has methods like get daily schedule, sort by priority of tasks, as well as add and remove tasks.

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

I changed detect_conflicts inside Scheduler to return a list of tuples with both conflicting tasks inside. Previously it was returning each conflicting task, without any way of knowing which one it conflicts with.
I also added a function to calculate end time inside of Task. End time will help detect conflicts in tasks by comparing start and end times for both tasks.

Changed Scheduler to get all tasks, and require an Owner (changed design - more on that later)

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

written by AI

I used AI to generate the Mermaid class diagram and the Python class skeletons, to review the skeleton for missing relationships and logic problems, and to explain each method before I wrote it. It influenced several design decisions: the review pointed out that `detect_conflicts` should return pairs of tasks and that `Task` needed an `end_time`, and it showed that the Scheduler keeping its own task list duplicated data the pets already held. The most helpful questions were the ones asking why, such as why the Scheduler should not hold its own list and why `extend` is used instead of `append`.

written by AI

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

written by AI

Accepted: moving `get_all_tasks` to Owner so the Scheduler reads across all pets, and removing the Scheduler's own `add_task`/`remove_task` and task list. I questioned this suggestion until I understood why, and checked it against the assignment guideline that the Scheduler must read from the Owner method.

Rejected or changed: the AI edited my skeleton when I had only asked for an explanation, so I had it revert the file and asked it to check with me before changing code. I also kept priority as a plain string instead of the suggested Enum, and left recurring-task logic out for now. I verified suggestions by reading the code, running `main.py` to check the printed schedule, and writing tests. Running the tests also caught a mistake in my own test: a function not named `test_...` was silently skipped, so it looked like it passed.

written by AI

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

written by AI

I tested three behaviors: `mark_complete` changes a task's status, `add_task` increases a pet's task count, and `detect_conflicts` finds overlapping tasks on different pets. These matter because everything the Scheduler does depends on tasks being attached to pets correctly, and conflict detection is the most complex logic in the project.

written by AI

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

written by AI

All three tests pass (`3 passed`) and the demo prints the expected schedule, so I am fairly confident in the basic behavior, but only a few cases are covered. Edge cases to test next: back-to-back tasks that should not count as conflicts, completed tasks being ignored by `detect_conflicts`, a priority value other than high/medium/low (which currently raises an error), and recurring tasks, which the daily schedule does not handle yet.

written by AI

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
