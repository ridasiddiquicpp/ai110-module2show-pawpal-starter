from datetime import datetime
from pawpal_system import Task, Pet, Owner, Scheduler



#Testing Task Completion
def test_mark_complete():
    task = Task(1, "Morning walk", "walk", datetime(2026, 10, 16, 9, 0), 30)

    assert task.is_complete is False    # starts incomplete

    task.mark_complete()

    assert task.is_complete is True     # now complete


#Testing Task Addition
def test_add_task():
   pet = Pet(1, "Cheeto", "cat")
   task = Task(1, "breakfast", "food", datetime(2026, 10, 16, 9, 0), 5, "high")

   count_before = len(pet.get_tasks())
   #verify thats tasks is 0
   assert count_before == 0
  
   pet.add_task(task)

   count_after = len(pet.get_tasks())
   #verify that tasks is 1
   assert count_after == count_before + 1

    

#Testing Detect Conflicts
def test_detect_conflicts():
    owner = Owner(1, "Bobby")
    pet1 = Pet(1, "Cheeto", "cat")
    pet2 = Pet(2, "Misty", "cat")

    owner.add_pet(pet1)
    owner.add_pet(pet2)

    vet = Task(1, "Vet appointment", "appointment", datetime(2026, 10, 16, 9, 0), 60)     # 9:00 - 10:00
    walk = Task(2, "Walk", "walk", datetime(2026, 10, 16, 9, 30), 30)          # 9:30 - 10:00

    pet1.add_task(vet)
    pet2.add_task(walk)

    conflicts = Scheduler(owner).detect_conflicts()

    print(conflicts)
    assert len(conflicts) == 1