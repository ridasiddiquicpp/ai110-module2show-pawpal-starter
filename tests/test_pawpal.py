from datetime import datetime
from pawpal_system import Task, Pet, Owner, Scheduler, Priority, Frequency



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


# ---------- sort_by_time ----------
from datetime import date, timedelta
import pytest


def _owner_with_pets():
    owner = Owner(1, "Bobby")
    cheeto, misty = Pet(1, "Cheeto", "cat"), Pet(2, "Misty", "cat")
    owner.add_pet(cheeto)
    owner.add_pet(misty)
    return owner, cheeto, misty


def test_sort_by_time_orders_across_pets_and_dates():
    owner, cheeto, misty = _owner_with_pets()
    late = Task(1, "late", "walk", datetime(2026, 10, 16, 18, 0), 10)
    next_day = Task(2, "next day early", "walk", datetime(2026, 10, 17, 7, 0), 10)
    early = Task(3, "early", "walk", datetime(2026, 10, 16, 8, 0), 10)
    cheeto.add_task(late)
    misty.add_task(next_day)
    cheeto.add_task(early)

    result = Scheduler(owner).sort_by_time()

    # the date must outrank time of day: 10/17 07:00 comes after 10/16 18:00
    assert [t.description for t in result] == ["early", "late", "next day early"]


def test_sort_by_time_empty_owner_and_pet_without_tasks():
    owner, _, _ = _owner_with_pets()
    assert Scheduler(owner).sort_by_time() == []
    assert Scheduler(Owner(2, "Nobody")).sort_by_time() == []


def test_sort_by_time_equal_times_keep_insertion_order():
    owner, cheeto, misty = _owner_with_pets()
    t = datetime(2026, 10, 16, 9, 0)
    a, b, c = (Task(i, n, "walk", t, 10) for i, n in [(1, "a"), (2, "b"), (3, "c")])
    cheeto.add_task(a)
    misty.add_task(b)
    cheeto.add_task(c)

    result = Scheduler(owner).sort_by_time()

    assert [x.description for x in result] == ["a", "c", "b"]  # pet order, stable


def test_sort_by_time_does_not_mutate_pet_task_lists():
    owner, cheeto, _ = _owner_with_pets()
    second = Task(1, "second", "walk", datetime(2026, 10, 16, 10, 0), 10)
    first = Task(2, "first", "walk", datetime(2026, 10, 16, 9, 0), 10)
    cheeto.add_task(second)
    cheeto.add_task(first)

    Scheduler(owner).sort_by_time()

    assert [t.description for t in cheeto.tasks] == ["second", "first"]


def test_sort_by_time_includes_completed_tasks():
    owner, cheeto, _ = _owner_with_pets()
    done = Task(1, "done", "walk", datetime(2026, 10, 16, 9, 0), 10)
    cheeto.add_task(done)
    done.mark_complete()
    assert Scheduler(owner).sort_by_time() == [done]


def test_sort_by_time_midnight_and_microsecond_boundaries():
    owner, cheeto, _ = _owner_with_pets()
    just_before = Task(1, "11:59pm", "walk", datetime(2026, 10, 16, 23, 59, 59), 1)
    midnight = Task(2, "midnight", "walk", datetime(2026, 10, 17, 0, 0), 1)
    cheeto.add_task(midnight)
    cheeto.add_task(just_before)
    assert [t.description for t in Scheduler(owner).sort_by_time()] == ["11:59pm", "midnight"]


# ---------- recurring tasks ----------
def test_daily_task_creates_next_day_occurrence():
    owner, cheeto, _ = _owner_with_pets()
    due = datetime.combine(date.today(), datetime(2000, 1, 1, 8, 30).time())
    feed = Task(1, "feed", "food", due, 5, frequency="daily")
    cheeto.add_task(feed)

    nxt = Scheduler(owner).mark_task_complete(feed)

    assert nxt is not None and nxt is not feed
    assert nxt.due_time == due + timedelta(days=1)   # same time of day
    assert nxt.is_complete is False
    assert nxt.pet is cheeto and nxt in cheeto.tasks
    assert nxt.task_id != feed.task_id
    assert feed.is_complete is True


def test_weekly_task_creates_occurrence_seven_days_later():
    owner, cheeto, _ = _owner_with_pets()
    due = datetime.combine(date.today(), datetime(2000, 1, 1, 17, 0).time())
    bath = Task(1, "bath", "groom", due, 20, frequency="weekly")
    cheeto.add_task(bath)
    nxt = Scheduler(owner).mark_task_complete(bath)
    assert nxt.due_time == due + timedelta(weeks=1)


def test_one_time_task_does_not_recur():
    owner, cheeto, _ = _owner_with_pets()
    vet = Task(1, "vet", "appointment", datetime(2026, 10, 16, 9, 0), 60)
    cheeto.add_task(vet)
    assert Scheduler(owner).mark_task_complete(vet) is None
    assert len(cheeto.tasks) == 1


def test_completing_twice_does_not_duplicate_occurrence():
    owner, cheeto, _ = _owner_with_pets()
    feed = Task(1, "feed", "food", datetime.now(), 5, frequency="daily")
    cheeto.add_task(feed)
    s = Scheduler(owner)
    s.mark_task_complete(feed)
    assert s.mark_task_complete(feed) is None
    assert len(cheeto.tasks) == 2


def test_unknown_frequency_is_rejected():
    with pytest.raises(ValueError):
        Task(1, "x", "walk", datetime(2026, 10, 16, 9, 0), 5, frequency="dayly")


def test_recurrence_chain_ids_stay_unique():
    owner, cheeto, misty = _owner_with_pets()
    misty.add_task(Task(50, "other", "walk", datetime(2026, 10, 16, 9, 0), 5))
    feed = Task(1, "feed", "food", datetime.now(), 5, frequency="daily")
    cheeto.add_task(feed)
    s = Scheduler(owner)
    n1 = s.mark_task_complete(feed)
    n2 = s.mark_task_complete(n1)
    ids = [t.task_id for t in owner.get_all_tasks()]
    assert len(ids) == len(set(ids))


def test_overdue_recurring_task_next_occurrence_is_relative_to_original_due_date():
    # Completing a task that was due 5 days ago: the next one should follow the
    # original schedule (due + 1 day) or at least land in the future.
    old_due = datetime.combine(date.today() - timedelta(days=5), datetime(2000, 1, 1, 8, 0).time())
    feed = Task(1, "feed", "food", old_due, 5, frequency="daily")
    nxt = feed.next_occurrence()
    assert nxt.due_time == old_due + timedelta(days=1)


def test_recurring_task_without_pet_is_not_lost_silently():
    owner, _, _ = _owner_with_pets()
    orphan = Task(1, "orphan", "walk", datetime.now(), 5, frequency="daily")
    nxt = Scheduler(owner).mark_task_complete(orphan)  # orphan not in owner's tasks
    assert nxt is not None


def test_recurring_occurrence_can_conflict_and_is_detected():
    owner, cheeto, misty = _owner_with_pets()
    tomorrow_9 = datetime.combine(date.today() + timedelta(days=1), datetime(2000, 1, 1, 9, 0).time())
    misty.add_task(Task(1, "grooming", "groom", tomorrow_9, 60))
    feed = Task(2, "feed", "food", datetime.combine(date.today(), datetime(2000, 1, 1, 9, 0).time()), 30, frequency="daily")
    cheeto.add_task(feed)
    s = Scheduler(owner)
    s.mark_task_complete(feed)
    assert len(s.detect_conflicts()) == 1


# ---------- other sorting ----------
def test_unknown_priority_is_rejected():
    with pytest.raises(ValueError):
        Task(1, "x", "walk", datetime(2026, 10, 16, 9, 0), 5, priority="urgent")


def test_priority_and_frequency_accept_any_casing_and_enums():
    t = Task(1, "x", "walk", datetime(2026, 10, 16, 9, 0), 5, priority=" HIGH ", frequency="Daily")
    assert t.priority is Priority.HIGH and t.frequency is Frequency.DAILY
    assert t.priority == "high" and str(t.frequency) == "daily"
    assert t.next_occurrence().frequency is Frequency.DAILY


def test_sort_by_priority_orders_high_medium_low_then_time():
    owner, cheeto, _ = _owner_with_pets()
    low = Task(1, "low", "walk", datetime(2026, 10, 16, 8, 0), 5, priority="Low")
    med_late = Task(2, "med late", "walk", datetime(2026, 10, 16, 12, 0), 5)  # default medium
    med_early = Task(3, "med early", "walk", datetime(2026, 10, 16, 9, 0), 5, priority="medium")
    high = Task(4, "high", "walk", datetime(2026, 10, 16, 18, 0), 5, priority="HIGH")
    for t in (low, med_late, med_early, high):
        cheeto.add_task(t)

    result = Scheduler(owner).sort_by_priority()

    assert [t.description for t in result] == ["high", "med early", "med late", "low"]


# ---------- same-pet overlaps ----------
def test_overlapping_tasks_on_same_pet_conflict_without_same_start():
    owner, cheeto, _ = _owner_with_pets()
    walk = Task(1, "walk", "walk", datetime(2026, 10, 16, 9, 0), 30)   # 9:00-9:30
    feed = Task(2, "feed", "food", datetime(2026, 10, 16, 9, 15), 10)  # 9:15-9:25
    cheeto.add_task(walk)
    cheeto.add_task(feed)

    conflicts = Scheduler(owner).detect_conflicts()

    assert conflicts == [(walk, feed)]
    assert "same pet" in Scheduler(owner).get_conflict_warnings()[0]


def test_scheduler_add_task_rejects_overlap_on_same_pet():
    owner, cheeto, _ = _owner_with_pets()
    s = Scheduler(owner)
    s.add_task(cheeto, Task(1, "walk", "walk", datetime(2026, 10, 16, 9, 0), 30))

    with pytest.raises(ValueError):
        s.add_task(cheeto, Task(2, "feed", "food", datetime(2026, 10, 16, 9, 15), 10))

    assert len(cheeto.tasks) == 1  # rejected task was not added


def test_scheduler_add_task_allows_back_to_back_on_same_pet():
    owner, cheeto, _ = _owner_with_pets()
    s = Scheduler(owner)
    s.add_task(cheeto, Task(1, "walk", "walk", datetime(2026, 10, 16, 9, 0), 30))
    assert s.add_task(cheeto, Task(2, "feed", "food", datetime(2026, 10, 16, 9, 30), 10)) == []
    assert len(cheeto.tasks) == 2


def test_scheduler_add_task_ignores_completed_task_on_same_pet():
    owner, cheeto, _ = _owner_with_pets()
    s = Scheduler(owner)
    done = Task(1, "walk", "walk", datetime(2026, 10, 16, 9, 0), 30)
    s.add_task(cheeto, done)
    done.mark_complete()
    s.add_task(cheeto, Task(2, "feed", "food", datetime(2026, 10, 16, 9, 0), 10))
    assert len(cheeto.tasks) == 2


def test_scheduler_add_task_only_warns_for_overlap_on_different_pets():
    owner, cheeto, misty = _owner_with_pets()
    s = Scheduler(owner)
    t = datetime(2026, 10, 16, 9, 0)
    s.add_task(cheeto, Task(1, "walk", "walk", t, 30))

    warnings = s.add_task(misty, Task(2, "feed", "food", t, 10))

    assert len(warnings) == 1 and "different pets" in warnings[0]
    assert len(misty.tasks) == 1


# ---------- duplicate tasks ----------
def test_detect_conflicts_flags_exact_duplicate_tasks():
    owner, cheeto, _ = _owner_with_pets()
    t = datetime(2026, 10, 16, 9, 0)
    a = Task(1, "walk", "walk", t, 30)
    b = Task(2, "walk", "walk", t, 30)   # same description, time and duration
    cheeto.add_task(a)
    cheeto.add_task(b)

    assert Scheduler(owner).detect_conflicts() == [(a, b)]


def test_scheduler_add_task_rejects_exact_duplicate():
    owner, cheeto, _ = _owner_with_pets()
    s = Scheduler(owner)
    t = datetime(2026, 10, 16, 9, 0)
    s.add_task(cheeto, Task(1, "walk", "walk", t, 30))
    with pytest.raises(ValueError):
        s.add_task(cheeto, Task(2, "walk", "walk", t, 30))
    assert len(cheeto.tasks) == 1


def test_detect_conflicts_empty_owner_and_pet_without_tasks():
    owner, _, _ = _owner_with_pets()
    assert Scheduler(owner).detect_conflicts() == []
    assert Scheduler(owner).get_conflict_warnings() == []
    assert Scheduler(Owner(2, "Nobody")).detect_conflicts() == []
