import streamlit as st
from pawpal_system import Owner, Pet, Scheduler, Task
from datetime import datetime

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

if "owner" not in st.session_state:
    st.session_state.owner = Owner(1, "")

owner = st.session_state.owner

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()


st.subheader("Basic Information")
owner_name = st.text_input("Owner name", value="Jordan")
owner.name = owner_name
# st.write(owner)


pet_name = st.text_input("Pet name", value="Mochi")
species = st.selectbox("Species", ["dog", "cat", "other"])
if st.button("Add pet"):
    pet = Pet(len(owner.pets) + 1, pet_name, species)
    owner.add_pet(pet)

st.markdown("### Tasks")
st.caption("Add a few tasks. In your final version, these should feed into your scheduler.")

if "tasks" not in st.session_state:
    st.session_state.tasks = []

if not owner.pets:
    st.warning("Add a pet first, then you can add tasks.")

else:
    pet_index = st.selectbox(
        "Pet", range(len(owner.pets)), format_func=lambda i: owner.pets[i].name
    )
    pet_choice = owner.pets[pet_index]



    col1, col2, col3 = st.columns(3)
    with col1:
        task_title = st.text_input("Task title", value="Morning walk")
    with col2:
        duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
    with col3:
        priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)

    col4, col5, col6 = st.columns(3)

    with col4:
        task_date = st.date_input("Date")
    with col5:
        task_time = st.time_input("Time")
    with col6:
        frequency = st.selectbox("Frequency", ["once", "daily", "weekly"])


if st.button("Add task"):
        due = datetime.combine(task_date, task_time)
        task = Task(
            len(owner.get_all_tasks()) + 1,
            task_title,
            "general",
            due,
            int(duration),
            priority,
            frequency,
        )
        try:
            warnings = Scheduler(owner).add_task(pet_choice, task)
        except ValueError as error:
            st.error(f"Task not added: {error}")
        else:
            st.success(f"Added {task.description} for {pet_choice.name}")
            for warning in warnings:
                st.warning(warning)


scheduler = Scheduler(owner)

warnings = scheduler.get_conflict_warnings()
if warnings:
    st.markdown("### ⚠️ Scheduling Conflicts")
    for message in warnings:
        st.warning(message)
elif owner.get_all_tasks():
    st.success("No scheduling conflicts. Your schedule looks good!")


st.divider()

st.markdown("### Your Tasks")
if "complete_msg" in st.session_state:
    st.success(st.session_state.pop("complete_msg"))

if owner.get_all_tasks():
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        sort_by = st.radio("Sort by", ["Time", "Priority"], horizontal=True)
    with col_b:
        pet_filter = st.selectbox("Pet filter", ["All"] + [p.name for p in owner.pets])
    with col_c:
        status_filter = st.selectbox("Status", ["All", "Incomplete", "Complete"])

    
    incomplete = scheduler.filter_tasks(is_complete=False)
    if incomplete:
        st.markdown("**Mark a task complete**")
        select_col, button_col = st.columns([4, 1])
        with select_col:
            task_index = st.selectbox(
                "Task to complete",
                range(len(incomplete)),
                format_func=lambda i: f"{incomplete[i].pet.name} - {incomplete[i].description} ({incomplete[i].due_time:%b %d, %I:%M %p})",
                label_visibility="collapsed",
            )
        with button_col:
            mark_clicked = st.button("Mark complete")

        if mark_clicked:
            next_task = scheduler.mark_task_complete(incomplete[task_index])
            message = f"Marked '{incomplete[task_index].description}' complete."
            if next_task:
                message += f" Next {next_task.frequency} task scheduled for {next_task.due_time:%b %d, %I:%M %p}."
            st.session_state.complete_msg = message
            st.rerun()

    if sort_by == "Priority":
        sorted_tasks = scheduler.sort_by_priority()
    else:
        sorted_tasks = scheduler.sort_by_time()

    wanted = scheduler.filter_tasks(
        is_complete={"All": None, "Incomplete": False, "Complete": True}[status_filter],
        pet_name=None if pet_filter == "All" else pet_filter,
    )
    sorted_tasks = [t for t in sorted_tasks if any(t is w for w in wanted)]

    if sorted_tasks:
        st.table(
            [
                {
                    "Date": f"{t.due_time:%b %d}",
                    "Time": f"{t.due_time:%I:%M %p}",
                    "Pet": t.pet.name,
                    "Task": t.description,
                    "Priority": str(t.priority),
                    "Duration (min)": t.duration_minutes,
                    "Done": "✅" if t.is_complete else "",
                }
                for t in sorted_tasks
            ]
        )
    else:
       st.info("No tasks match these filters.") 
else:
    st.info("No tasks yet. Add one above.")



st.subheader("Build Schedule")
st.caption("Pick a day to see its tasks in time order.")

schedule_day = st.date_input("Schedule for", key="schedule_day")

if st.button("Generate schedule"):
    todays_tasks = scheduler.get_daily_schedule(schedule_day)
    if todays_tasks:
        st.success(f"{len(todays_tasks)} task(s) scheduled for {schedule_day:%B %d, %Y}")
        st.table(
            [
                {
                    "Time": f"{t.due_time:%I:%M %p}",
                    "Pet": t.pet.name,
                    "Task": t.description,
                    "Priority": str(t.priority),
                    "Duration (min)": t.duration_minutes,
                    "Done": "✅" if t.is_complete else "",

                }
                for t in todays_tasks
            ]
        )
    else:
        st.info(f"Nothing scheduled for {schedule_day:%B %d, %Y}.")

