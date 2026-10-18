import streamlit as st
from pawpal_system import Owner, Pet, Task
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


st.subheader("Quick Demo Inputs (UI only)")
owner_name = st.text_input("Owner name", value="Jordan")
owner.name = owner_name
st.write(owner)


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
    pet_choice = st.selectbox("Pet", owner.pets, format_func=lambda p: p.name)


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
        pet_choice.add_task(task)
        st.success(f"Added {task.description} for {pet_choice.name}")


all_tasks = owner.get_all_tasks()
if all_tasks:
    st.write("Current tasks:")
    for task in all_tasks:
        st.write(
            f"{task.pet.name} - {task.description} ({task.priority}) "
            f"at {task.due_time:%b %d, %I:%M %p}"
        )
else:
    st.info("No tasks yet. Add one above.")

st.divider()

st.subheader("Build Schedule")
st.caption("This button should call your scheduling logic once you implement it.")

if st.button("Generate schedule"):
    st.warning(
        "Not implemented yet. Next step: create your scheduling logic (classes/functions) and call it here."
    )
    st.markdown(
        """
Suggested approach:
1. Design your UML (draft).
2. Create class stubs (no logic).
3. Implement scheduling behavior.
4. Connect your scheduler here and display results.
"""
    )
