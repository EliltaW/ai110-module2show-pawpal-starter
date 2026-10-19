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
scheduler = Scheduler(owner)

st.title("🐾 PawPal+")

st.markdown(
    "PawPal+ helps owners manage pets, schedule care tasks, and build a daily plan "
    "using priorities and available care time."
)
st.caption("Your data is kept only for the current session and is not saved permanently.")

st.divider()

st.subheader("Owner and pets")
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

    st.markdown("### Complete a task")
    unfinished_tasks = scheduler.filter_tasks(is_completed=False)
    if not unfinished_tasks:
        st.info("No unfinished tasks to complete.")
    else:
        selected_task_index = st.selectbox(
            "Task to complete",
            options=list(range(len(unfinished_tasks))),
            format_func=lambda index: (
                f"{unfinished_tasks[index][0].name} - "
                f"{unfinished_tasks[index][1].description} - "
                f"{unfinished_tasks[index][1].due_date} "
                f"{unfinished_tasks[index][1].time}"
            ),
        )
        selected_pet, selected_task = unfinished_tasks[selected_task_index]
        is_future_task = selected_task.due_date > date.today()
        if is_future_task:
            st.info("Future tasks can be completed on their due date.")
        if st.button("Mark complete", disabled=is_future_task):
            scheduler.mark_task_complete(selected_pet, selected_task)
            st.rerun()

    st.markdown("### Edit a task")
    editable_tasks = scheduler.filter_tasks(is_completed=False)
    if not editable_tasks:
        st.info("No unfinished tasks to edit.")
    else:
        selected_edit_index = st.selectbox(
            "Task to edit",
            options=list(range(len(editable_tasks))),
            format_func=lambda index: (
                f"{editable_tasks[index][0].name} - "
                f"{editable_tasks[index][1].description} - "
                f"{editable_tasks[index][1].due_date} "
                f"{editable_tasks[index][1].time}"
            ),
        )
        edit_pet, edit_task = editable_tasks[selected_edit_index]
        edit_task_id = id(edit_task)

        with st.form(f"edit_task_form_{edit_task_id}"):
            edited_description = st.text_input(
                "Description",
                value=edit_task.description,
                key=f"edit_description_{edit_task_id}",
            )
            edited_due_date = st.date_input(
                "Due date",
                value=edit_task.due_date,
                key=f"edit_due_date_{edit_task_id}",
            )
            edited_start_time = st.time_input(
                "Start time",
                value=time.fromisoformat(edit_task.time),
                key=f"edit_start_time_{edit_task_id}",
            )
            edited_duration = st.number_input(
                "Duration in minutes",
                min_value=1,
                value=max(edit_task.duration_minutes, 1),
                step=1,
                key=f"edit_duration_{edit_task_id}",
            )
            edited_priority = st.selectbox(
                "Priority",
                ["low", "medium", "high"],
                index=["low", "medium", "high"].index(edit_task.priority),
                key=f"edit_priority_{edit_task_id}",
            )
            edited_frequency = st.selectbox(
                "Frequency",
                ["once", "daily", "weekly"],
                index=["once", "daily", "weekly"].index(edit_task.frequency),
                key=f"edit_frequency_{edit_task_id}",
            )
            save_changes = st.form_submit_button("Save changes")

        if save_changes:
            if not edited_description.strip():
                st.warning("Enter a task description before saving changes.")
            else:
                edit_task.description = edited_description.strip()
                edit_task.due_date = edited_due_date
                edit_task.time = edited_start_time.strftime("%H:%M")
                edit_task.duration_minutes = max(int(edited_duration), 1)
                edit_task.priority = edited_priority
                edit_task.frequency = edited_frequency
                st.rerun()

    st.write("Current tasks:")
    pet_names = list(dict.fromkeys(pet.name for pet in owner.pets))
    selected_pet_name = st.selectbox(
        "Filter by pet name",
        options=["All pets", *pet_names],
    )
    st.caption("Pet-name filtering includes all pets sharing that name.")
    selected_status = st.selectbox(
        "Filter by status",
        options=["All", "Unfinished", "Completed"],
    )
    completion_filter = {
        "All": None,
        "Unfinished": False,
        "Completed": True,
    }[selected_status]
    filtered_tasks = scheduler.filter_tasks(
        pet_name=None if selected_pet_name == "All pets" else selected_pet_name,
        is_completed=completion_filter,
    )
    filtered_task_ids = {id(task) for _, task in filtered_tasks}
    displayed_tasks = [
        (pet, task)
        for pet, task in scheduler.sort_by_time()
        if id(task) in filtered_task_ids
    ]

    if displayed_tasks:
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
            for pet, task in displayed_tasks
        ]
        st.table(task_rows)
    else:
        st.info("No tasks match the selected filters.")

st.divider()

st.subheader("Build Schedule")
st.caption(
    "Today's unfinished tasks are considered by priority, selected when they fit "
    "the available time, then displayed by time."
)

if st.button("Generate schedule"):
    selected_tasks = scheduler.generate_daily_plan()
    if selected_tasks:
        st.table(
            [
                {
                    "Pet": pet.name,
                    "Description": task.description,
                    "Date": task.due_date,
                    "Time": task.time,
                    "Duration (minutes)": task.duration_minutes,
                    "Priority": task.priority,
                }
                for pet, task in selected_tasks
            ]
        )
    else:
        st.info("No tasks fit the available time today.")

    total_selected_minutes = sum(
        task.duration_minutes for _, task in selected_tasks
    )
    st.write(
        f"Selected time: {total_selected_minutes} minutes | "
        f"Available time: {owner.available_minutes} minutes"
    )

    st.markdown("**Warnings across all unfinished tasks**")
    st.caption(
        "Warnings may include tasks outside the selected daily plan. "
        "Conflicts require manual review and are not automatically resolved."
    )
    for warning in scheduler.detect_conflicts():
        st.warning(warning)
