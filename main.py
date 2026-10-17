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


