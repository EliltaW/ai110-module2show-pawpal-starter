# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

The three core actions I want a user to perform are:

1. Enter owner information and add a pet.
2. Add or edit pet care tasks with a scheduled time, duration, and priority.
3. Generate and view today's care plan based on the owner's availability and task priorities.

My initial UML design includes four classes: Owner, Pet, Task, and Scheduler.

- Owner stores the owner's name, available care time, and pets. Its get_all_tasks() method gathers Pet–Task pairs across all its pets.
- Pet stores an animal's details and its list of care tasks.
- Task represents one care activity, including its description, date, time, duration, priority, frequency, and completion status.
- Scheduler uses the Owner's tasks to organize the schedule. Its planned responsibilities include sorting, filtering, conflict warnings, daily planning, and handling recurring tasks.

One Owner can have many Pets, and each Pet can have many Tasks. Scheduler holds a reference to Owner so it can coordinate care across multiple pets.

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

During the skeleton review, I changed detect_conflicts() from
returning None to returning a list of warning strings. This will
let the terminal demo and Streamlit UI display conflicts without
putting display logic inside Scheduler.

I kept task editing simple: the UI will update the fields of an
existing Task object directly rather than adding another method.
These are design decisions; the behavior is not implemented yet.

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

- Conflict detection checks matching dates and start times, rather than overlapping durations. This keeps it simple but can miss partial overlaps.
- We kept the nested-loop approach after comparing it with dictionary grouping because readability matters for this small project.
- Daily planning chooses tasks by priority within a time budget. It warns about conflicts separately rather than automatically resolving them.

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

I used AI to brainstorm the UML, create class skeletons, implement small methods, and draft tests.
Focused prompts limited changes to a few methods at a time, making mistakes easier to catch and the code easier to understand.
We reviewed the code, checked the CLI output, and ran pytest; both initial tests passed.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

-The generated skeleton declared detect_conflicts() -> None. After review, we changed it to list[str] so the UI could receive warning messages.
-The CLI demo and two passing tests verified the methods we’ve implemented so far

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
