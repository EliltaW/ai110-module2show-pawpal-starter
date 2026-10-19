from datetime import date, time

import streamlit as st
from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")
if "owner" not in st.session_state:
    st.session_state["owner"] = Owner(
        first_name="Alex",
        last_name="Morgan",
        available_minutes=60,
    )

owner = st.session_state["owner"]

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
owner.first_name = st.text_input("First name", value=owner.first_name)
owner.last_name = st.text_input("Last name", value=owner.last_name)
owner.available_minutes = int(
    st.number_input(
        "Available care time (minutes per day)",
        min_value=0,
        value=owner.available_minutes,
        step=1,
    )
)
with st.form("add_pet_form"):
    pet_name = st.text_input("Pet name")
    species = st.selectbox("Species", ["dog", "cat", "other"])
    breed = st.text_input("Breed")
    age = st.number_input("Age in years", min_value=0, step=1)
    submitted = st.form_submit_button("Add pet")

if submitted:
    if not pet_name.strip():
        st.warning("Enter a pet name before adding the pet.")
    else:
        pet = Pet(
            name=pet_name.strip(),
            species=species,
            breed=breed,
            age=int(age),
        )
        owner.add_pet(pet)
        st.success(f"Added {pet.name}.")

if owner.pets:
    st.write("Your pets:")
    st.table(
        [
            {
                "Name": pet.name,
                "Species": pet.species,
                "Breed": pet.breed,
                "Age": pet.age,
            }
            for pet in owner.pets
        ]
    )
else:
    st.info("No pets added yet.")

st.markdown("### Tasks")
if not owner.pets:
    st.info("Add a pet before creating tasks.")
else:
    with st.form("add_task_form"):
        selected_pet_index = st.selectbox(
            "Pet",
            options=list(range(len(owner.pets))),
            format_func=lambda index: owner.pets[index].name,
        )
        description = st.text_input("Description")
        due_date = st.date_input("Due date", value=date.today())
        start_time = st.time_input("Start time", value=time(8, 0))
        duration_minutes = st.number_input(
            "Duration in minutes",
            min_value=1,
            value=20,
            step=1,
        )
        priority = st.selectbox("Priority", ["low", "medium", "high"])
        frequency = st.selectbox("Frequency", ["once", "daily", "weekly"])
        submitted = st.form_submit_button("Add task")

    if submitted:
        if not description.strip():
            st.warning("Enter a task description before adding the task.")
        else:
            selected_pet = owner.pets[selected_pet_index]
            task = Task(
                description=description.strip(),
                due_date=due_date,
                time=start_time.strftime("%H:%M"),
                duration_minutes=int(duration_minutes),
                priority=priority,
                frequency=frequency,
            )
            selected_pet.add_task(task)
            st.success(f"Added {task.description} for {selected_pet.name}.")

    task_rows = [
        {
            "Pet": pet.name,
            "Description": task.description,
            "Due date": task.due_date,
            "Time": task.time,
            "Duration (minutes)": task.duration_minutes,
            "Priority": task.priority,
            "Frequency": task.frequency,
            "Completed": task.is_completed,
        }
        for pet, task in owner.get_all_tasks()
    ]
    if task_rows:
        st.write("Current tasks:")
        st.table(task_rows)
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
