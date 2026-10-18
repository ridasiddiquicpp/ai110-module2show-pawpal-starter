from __future__ import annotations

from dataclasses import dataclass, field, replace
from datetime import date, datetime, timedelta
from typing import List, Optional, Tuple


@dataclass
class Task:
    task_id: int
    description: str
    task_type: str
    due_time: datetime
    duration_minutes: int
    priority: str = "medium"
    frequency: str = "once"  # "once", "daily", "weekly"
    is_complete: bool = False
    pet: Optional[Pet] = field(default=None, repr=False, compare=False)

    def mark_complete(self) -> None:
        """Mark this task as completed."""
        self.is_complete = True

    def next_occurrence(self) -> Optional[Task]:
        """Return a fresh copy due today + 1 period (same time of day), or None if it doesn't repeat."""
        deltas = {"daily": timedelta(days=1), "weekly": timedelta(weeks=1)}
        if self.frequency not in deltas:
            return None
        next_date = date.today() + deltas[self.frequency]
        return replace(
            self,
            due_time=datetime.combine(next_date, self.due_time.time()),
            is_complete=False,
        )

    def reschedule(self, new_time: datetime) -> None:
        """Move this task to a new due time."""
        self.due_time = new_time

    @property
    def end_time(self) -> datetime:
        """Calculate end time using due time and duration"""
        return self.due_time + timedelta(minutes=self.duration_minutes)
        


   

@dataclass
class Pet:
    pet_id: int
    name: str
    species: str
    breed: str = ""
    age: int = 0
    owner: Optional[Owner] = field(default=None, repr=False, compare=False)
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Attach a task to this pet."""
        if any(t is task for t in self.tasks):
            #checking for any duplicate tasks before adding
            return
        task.pet = self
        self.tasks.append(task)

    def remove_task(self, task: Task) -> None:
        """Remove a task from this pet."""
        #rebuild pet list, keeping every task expect the one being removed
        self.tasks = [t for t in self.tasks if t is not task]
        if task.pet is self:
            task.pet = None
        

    def get_tasks(self) -> List[Task]:
        """Return all tasks for this pet."""
        return list(self.tasks)


@dataclass
class Owner:
    owner_id: int
    name: str
    email: str = ""
    pets: List[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner."""
        if any(p is pet for p in self.pets):
            #checking for any duplicate pets before adding
            return
        pet.owner = self
        self.pets.append(pet)

    def remove_pet(self, pet: Pet) -> None:
        """Remove a pet from this owner."""
        self.pets = [p for p in self.pets if p is not pet]
        if pet.owner is self:
            pet.owner = None

    def get_pets(self) -> List[Pet]:
        """Return all pets owned by this owner."""
        return list(self.pets)

    
    def get_all_tasks(self) -> List[Task]:
        """Return every pet's tasks together in one list."""
        all_tasks = []
        for pet in self.pets:
            all_tasks.extend(pet.get_tasks())
        return all_tasks


class Scheduler:
    def __init__(self, owner: Owner) -> None:
        self.owner = owner

    def get_daily_schedule(self, day: date) -> List[Task]:
        """Return tasks due on the given day, ordered by time."""
        todays_tasks = []
        for task in self.owner.get_all_tasks():
            if task.due_time.date() == day:
                todays_tasks.append(task)
        todays_tasks.sort(key=lambda t: t.due_time)
        return todays_tasks

    def get_tasks_by_pet(self, pet: Pet) -> List[Task]:
        """Return tasks belonging to the given pet."""
        # return list(pet.tasks)
        pet_tasks = []
        for task in self.owner.get_all_tasks():
            if task.pet is pet:
                pet_tasks.append(task)

        return pet_tasks

    def filter_tasks(
        self,
        is_complete: Optional[bool] = None,
        pet_name: Optional[str] = None,
    ) -> List[Task]:
        """Return tasks filtered by completion status and/or pet name.

        A filter left as None is ignored, so passing neither returns every task.
        """
        tasks = self.owner.get_all_tasks()
        if is_complete is not None:
            tasks = [t for t in tasks if t.is_complete == is_complete]
        if pet_name is not None:
            tasks = [
                t for t in tasks
                if t.pet is not None and t.pet.name.lower() == pet_name.lower()
            ]
        return tasks

    def mark_task_complete(self, task: Task) -> Optional[Task]:
        """Mark a task complete and, if it repeats, add the next occurrence to its pet."""
        if task.is_complete:  # guard against creating duplicate occurrences
            return None
        task.mark_complete()

        next_task = task.next_occurrence()
        if next_task is None:
            return None

        next_task.task_id = max(t.task_id for t in self.owner.get_all_tasks()) + 1
        if task.pet is not None:
            task.pet.add_task(next_task)  # also sets next_task.pet
        return next_task

    def get_upcoming_tasks(self) -> List[Task]:
        """Return incomplete tasks due in the future."""
        now = datetime.now()
        upcoming = []
        for task in self.owner.get_all_tasks():
            if not task.is_complete and task.due_time > now:
                upcoming.append(task)
        upcoming.sort(key=lambda t: t.due_time)
        return upcoming



    def detect_conflicts(self) -> List[Tuple[Task, Task]]:
        """Return pair of incomplete tasks whose time windows overlap."""
        active = []
        for task in self.owner.get_all_tasks():
            if not task.is_complete:
                active.append(task)
        active.sort(key=lambda t: t.due_time)

        conflicts = []
        for i in range(len(active)):
            current = active[i]
            for other in active[i + 1:]:
                if other.due_time >= current.end_time:
                    break
                conflicts.append((current, other))
        return conflicts



    @staticmethod
    def _format_conflict(first: Task, second: Task) -> str:
        """Build a warning message for two overlapping tasks."""
        first_pet = first.pet.name if first.pet else "no pet"
        second_pet = second.pet.name if second.pet else "no pet"
        kind = "same pet" if first.pet is second.pet and first.pet else "different pets"
        return (
            f"WARNING ({kind}): '{first.description}' ({first_pet}, "
            f"{first.due_time:%m/%d %I:%M %p}-{first.end_time:%I:%M %p}) overlaps "
            f"'{second.description}' ({second_pet}, "
            f"{second.due_time:%m/%d %I:%M %p}-{second.end_time:%I:%M %p})"
        )

    def get_conflict_warnings(self) -> List[str]:
        """Return a warning message for each pair of overlapping incomplete tasks.

        Works for the same pet or different pets. Never raises: if anything goes
        wrong while checking, a single warning is returned instead of crashing.
        """
        try:
            return [self._format_conflict(a, b) for a, b in self.detect_conflicts()]
        except Exception as error:
            return [f"WARNING: could not check for conflicts ({error})"]

    def add_task(self, pet: Pet, task: Task) -> List[str]:
        """Add a task to a pet and return warnings for any conflicts it creates.

        The task is always added; conflicts only produce warning messages.
        """
        pet.add_task(task)  # add first so task.pet is set for the warning text
        try:
            clashes = [
                other for other in self.owner.get_all_tasks()
                if other is not task
                and not other.is_complete
                and other.due_time < task.end_time
                and task.due_time < other.end_time
            ]
            return [self._format_conflict(task, other) for other in clashes]
        except Exception as error:
            return [f"WARNING: could not check for conflicts ({error})"]

    def sort_by_time(self) -> List[Task]:
        """Return all tasks in chronological order (date, then time)."""
        # due_time is a datetime, so comparing it directly covers both date and time.
        return sorted(self.owner.get_all_tasks(), key=lambda t: t.due_time)

    def sort_by_priority(self) -> List[Task]:
        """Return tasks sorted from highest to lowest priority."""
        order = {"high": 0, "medium": 1, "low": 2}
        tasks = self.owner.get_all_tasks()
        tasks.sort(key=lambda t: (order[t.priority], t.due_time))
        return tasks

