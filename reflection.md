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
returning None to returning a list of warning strings. This lets
the terminal demo and Streamlit UI display conflicts without
putting display logic inside Scheduler.

I kept task editing simple: the UI updates the fields of an
existing Task object directly rather than adding another method.

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

Daily planning considers unfinished tasks due today, their priorities, and the owner's available minutes. Availability limits how much care fits in the plan, priority helps choose important tasks first, and today's unfinished-task requirement keeps the plan focused on work still due today. Tasks that do not fit are skipped, and selected tasks are displayed chronologically. Owner preferences beyond the time budget are not implemented.

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

I used AI to brainstorm the UML, create class skeletons, implement small methods, and draft tests. Chat-based explanations, automatic file editing, and terminal test execution were useful assistant features.
Focused prompts limited changes to a few methods at a time, making mistakes easier to catch and the code easier to understand. Separate AI chats for algorithm planning and testing kept each discussion focused and reduced unrelated context.
We reviewed the code, checked the CLI output, and ran pytest; all 16 final tests passed.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

-The generated skeleton declared detect_conflicts() -> None. After review, we changed it to list[str] so the UI could receive warning messages.
-We rejected an AI-generated conflict test that changed both the task date and completion status together. We split it into two independent tests so each exclusion was verified separately.
-We checked the CLI demo and ran the complete pytest suite to verify the implemented behavior.

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

The 16 automated tests cover task addition and completion, sorting, filtering, recurrence, duplicate prevention, conflict detection, daily-plan budget rules, and empty collections. These tests check core behaviors and edge cases directly, so regressions in scheduling rules are easier to catch.

I also checked the app in a browser for adding pets and tasks, retaining data during the current session, selecting tasks within a time budget, displaying conflict warnings, editing and filtering tasks, completing tasks, and disabling completion of future tasks. These checks matter because they verify that the backend behavior is connected correctly to the visible controls and that the main user flows work together.

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

My confidence is 4/5. With more time, I would test malformed time and priority inputs, clarify and test overdue-task policies, and cover more browser edge cases. Those cases are not covered by the current tests.

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

I am most satisfied with understanding and checking AI-generated code. I reviewed changes and used CLI output, automated tests, and browser checks instead of accepting generated code without verification.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

I would improve conflict detection to catch overlapping durations, such as a walk from 08:00 to 08:30 and medication at 08:15, rather than only tasks with identical start times.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?

I learned that I still need to understand the design and verify the code even when AI writes it. As lead architect, I am responsible for deciding what to accept and checking that it meets the requirements.
