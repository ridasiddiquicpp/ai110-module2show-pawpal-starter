from pawpal_system import Owner, Task, Pet, Scheduler
from datetime import datetime, date

cheeto = Pet(1, "Cheeto", "cat")
misty = Pet(2, "Misty", "cat")

owner = Owner(1, "Bobby")

owner.add_pet(cheeto)
owner.add_pet(misty)

vet_app = Task(1, "vet appointment", "appointment", datetime(2026, 10, 16, 9, 0), 60, "high")
cheeto.add_task(vet_app)

walk = Task(2, "evening walk", "walk", datetime(2026, 10, 16, 18, 0), 30, "high", "daily")
misty.add_task(walk)

playtime = Task(3, "playtime", "play", datetime(2026, 10, 16, 17, 0), 30, "medium", "daily")
cheeto.add_task(playtime)

breakfast = Task(4, "breakfast", "feeding", datetime(2026, 10, 17, 7, 30), 15, "medium", "daily")
misty.add_task(breakfast)

groom = Task(5, "grooming", "grooming", datetime(2026, 10, 16, 12, 0), 45, "low")
cheeto.add_task(groom)

meds = Task(6, "give medicine", "medication", datetime(2026, 10, 16, 8, 0), 5, "high", "daily")
misty.add_task(meds)
meds.mark_complete()   # so there's a completed task to filter on


print("Today's Schedule")

scheduler = Scheduler(owner)
todays_tasks = scheduler.get_daily_schedule(date(2026, 10, 16))

# print(todays_tasks)

for task in todays_tasks:
    print(task.due_time.strftime("%I:%M:%p"), "-", task.pet.name, "-", task.description, "-", task.duration_minutes, "minutes")


print()
print("Tasks by Priority")
tasks_by_priority = scheduler.sort_by_priority()

for task in tasks_by_priority:
    print(task.priority, "-", task.due_time.strftime("%I:%M:%p"), "-", task.pet.name, "-", task.description, "-", task.duration_minutes, "minutes")


print()
print("Recurring tasks")
print("Tasks before:", len(owner.get_all_tasks()))

next_walk = scheduler.mark_task_complete(walk)      # daily -> new task due tomorrow
next_vet = scheduler.mark_task_complete(vet_app)    # "once" -> no new task
repeat_walk = scheduler.mark_task_complete(walk)    # already complete -> no duplicate

print("Tasks after:", len(owner.get_all_tasks()))
print("Next walk:", next_walk.due_time.strftime("%m/%d %I:%M %p"), "-", next_walk.pet.name, "- id", next_walk.task_id)
print("Next vet (once):", next_vet)
print("Second completion of walk:", repeat_walk)


print()
print("Conflict detection")
print("Before adding conflicts:", scheduler.get_conflict_warnings() or "no conflicts")

# (the vet appointment is already complete, so it is ignored by conflict checks)
bath = Task(20, "bath", "grooming", datetime(2026, 10, 16, 10, 0), 30, "low")
print("Adding bath:", scheduler.add_task(misty, bath) or "no conflicts")
# Different pets, starting at exactly the same time as the bath
nails = Task(21, "nail trim", "grooming", datetime(2026, 10, 16, 10, 0), 15, "low")
for warning in scheduler.add_task(cheeto, nails):
    print(warning)
# Same pet (Misty), overlapping the end of the bath (10:00-10:30)
brush = Task(22, "brushing", "grooming", datetime(2026, 10, 16, 10, 15), 20, "low")
try:
    scheduler.add_task(misty, brush)
except ValueError as error:
    print("REJECTED:", error)

print("All conflicts now:", len(scheduler.get_conflict_warnings()))


def print_tasks(tasks):
    if not tasks:
        print("(no tasks)")
    for task in tasks:
        status = "done" if task.is_complete else "pending"
        print(task.due_time.strftime("%m/%d %I:%M %p"), "-", task.pet.name, "-", task.description, "-", status)


print("\nRaw order (as added)")
print_tasks(owner.get_all_tasks())

print("\nSorted by time")
print_tasks(scheduler.sort_by_time())

print("\nIncomplete tasks")
print_tasks(scheduler.filter_tasks(is_complete=False))

print("\nCompleted tasks")
print_tasks(scheduler.filter_tasks(is_complete=True))

print("\nMisty's tasks")
print_tasks(scheduler.filter_tasks(pet_name="Misty"))
