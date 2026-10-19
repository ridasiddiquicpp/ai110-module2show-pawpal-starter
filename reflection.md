# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

I included the classes Owner, Pet, Task, and Scheduler.
The owner can add, remove, and get pets. Pet can add, remove, and get tasks.
A task can be rescheduled or marked as complete.
Scheduler is where you find out what task the owner should do and when. It has methods like get daily schedule and sort by priority of tasks

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

I changed detect_conflicts inside Scheduler to return a list of tuples with both conflicting tasks inside. Previously it was returning each conflicting task, without any way of knowing which one it conflicts with.
I also added a function to calculate end time inside of Task. End time will help detect conflicts in tasks by comparing start and end times for both tasks.

I changed Scheduler to require an Owner and get its tasks through owner.get_all_tasks(), instead of keeping its own list.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

My scheduler considers time conflicts. It uses a tasks start time and duration to find overlaps. It also considers whether a task is already complete when checking for conflicts. 
As well as considering a tasks frequency and after a daily or weekly task is completed it creates another one.

I decided that time conflicts mattered most because a pet can't be in two places at the same time and the owner can't do two things at the time. This is why if a task overlaps another task on the same pet it is rejected, but an overlap between different pets shows a warning, since the owner could be able to do both at the same time (like walking two dogs). 


**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

One tradeoff my scheduler makes is how it handles recurring tasks that overlap. When a daily or weekly task is marked complete, the next occurrence is always added to the pet, even if it overlaps another task on that pet. 

I considered rejecting it, shifting it to the next free slot, or skipping it, but decided to leave it in anyways. 

This is reasonable for this scenario because the logic was complicated and would take more time to flesh out, skipping it could stop the recurrence, and shifting it would move a task off its usual time without asking. 
The owner is in a better position then the schedule to decide which task should move. 

Adding it and flagging the clash keeps the schedule predictable and keeps the code simple, at the cost of letting a conflict exist until the owner fixes it.

Adding it keeps the schedule predictable and keeps the code simple. The cost is that a conflict can exist without the owner being told. The method detect_conflicts can find the overlap, but the app does not show it yet, so a future improvement would be to display those warnings in the UI.


---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?


I used AI to generate the Mermaid class diagram, and I reviewed it asking AI questions to understand some of the methods listed. Then I used AI to generate the class skeletons in pawpal_system.py. In this phase I used AI very extensively to figure out what relationships between the classes was and different methods we would need to have for that. Methods like sorting, and filtering in the Scheduler class I worked with AI to generate skeleton. 


AI also influenced certain design decisions, like detect_conflicts should return a pair of tasks, instead of just returning a list of all conflicting tasks and that Task needed an end_time to make sure we could properly detect conflicts.


The AI's conflict design only warned about overlapping tasks on the same pet. I rejected this because I wanted to make sure that a pet can't do two tasks at the same time. So I worked with AI to completely reject a task that overlaps another incomplete task on the same pet. 
Overlaps between different pets still only produce a warning, since one owner could handle two pets at once. I verified this with tests for partial overlaps, exact duplicates, and different pets.


The questions that were most helpful were asking AI to explain why it did something, such as why the Scheduler should not hold its own list and why extend was used instead of append.


**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

The AI's first design gave the Scheduler its own task list with add_task and remove_task. 
I did not accept the design because it duplicated tasks the pets already store. I asked for the Scheduler to read the tasks the users put on the pets, so I added the get_all_tasks method in the Owner class, and the Scheduler can call it whenever needed.

I evaluated what AI suggested by using the project guidelines and verified by writing tests and by manually testing on the app, for example making sure that added tasks actually showed up in the table. 


---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

I tested sorting by time and priority, recurring tasks, conflict detection and prevention, and input validation, along with adding a task and marking it complete. These tests were important because sorting and conflicts are an integral part of scheduler's functionality, and recurring tasks have edge cases, such as completing the same task twice, that could silently create duplicates. 

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

I'm fairly confident that the scheduler works mostly correct, because all tests pass, and they cover sorting, conflict detection, and recurring tasks. But there were some method and edge cases I wasn't able to write tests for.

I would test methods, like filter_tasks, get_daily_schedule, and get_upcoming_tasks, and the Streamlit UI. I would also want to decide how to handle a recurring task's next occurence that conflicts with another scheduled task.
I also want to handle edge cases like adding a task with a date and time in the past.

---

## 5. Reflection

ADD HERE

**a. What went well**

- What part of this project are you most satisfied with?



I am most satisfied with how the UI looks and how it interacts nicely with the classes and methods in pawpal_system.py. For example, it uses methods like get_conflict_warnings and displays a clean warning or error box. 




**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

I would decide how to handle a recurring task whose next occurrence overlaps another task, because right now it is added anyway. I would also let users delete tasks and pets in the app.


**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?


One important thing I learned is that it is beneficial to tell AI what the project requirements first, because there was a time when AI gave me suggestions that didnt match the requirements.

Also building the code one piece at a time with AI can help you understand what's going on. I used AI to help make the skeleton code in pawpal_system.py, but made sure to code the classes one by one.

