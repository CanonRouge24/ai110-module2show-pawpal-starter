# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

Three core actions the user should be able to perform:
1. Modify their list of current pets (add, remove)
2. Add a new task for a pet
3. Modify their constraints and preferences

Main objects needed for system:
* Pet
  Attributes:
    • Name
    • Type + Species (for completeness's sake)
    • Age
    • Birthday (for fun)
    • Dates of various things, like previous grooming and medicine dates
  Methods:
    • Update the dates
* Task
  Attributes:
    • Type + Name
    • Date, time, duration
    • Frequency (once, daily, weekly, monthly)
    • Priority
    • Which pet(s)?
    • Completed?
  Methods:
    • Create repeated scheduled tasks
    • Setters for any of the attributes, for when they need to be updated.
* Owner
  Attributes:
    • Name
    • Available times
    • Preferences
    • Pets
  Methods:
    • Add/remove pets
    • Get all tasks across all owned pets
    • Getters for times and preferences
* Scheduler
  Attributes:
    • Owner (for constraints/availability)
    • List of pets being scheduled for
    • Generated plan (list of scheduled tasks)
  Methods:
    • Retrieve all tasks across pets
    • Retrieve tasks filtered by priority or date
    • Generate a prioritized plan
    • Add, remove, or reschedule tasks
    • Explain scheduling reasoning


classDiagram
  class Owner {
      +String id
      +String name
      +String email
      +List~TimeWindow~ availability
      +List~String~ preferences
      +List~Pet~ pets
      +addPet(pet) void
      +removePet(petId) void
      +getPets() List~Pet~
      +getAllTasks() List~Task~
      +setAvailability(windows) void
      +getAvailability() List~TimeWindow~
      +getPreferences() List~String~
  }

  class Pet {
      +String id
      +String name
      +String species
      +String breed
      +int age
      +float weightLbs
      +String medicalNotes
      +Date birthday
      +Date lastGrooming
      +Date lastMedication
      +List~Task~ tasks
      +addTask(task) void
      +removeTask(taskId) void
      +editTask(taskId, updates) void
      +getTasks() List~Task~
      +updateDates(field, date) void
  }

  class Task {
      +String id
      +String name
      +TaskType type
      +Date date
      +String time
      +int durationMinutes
      +Frequency frequency
      +Priority priority
      +String petId
      +boolean isCompleted
      +markComplete() void
      +edit(updates) void
      +createRecurring(intervalDays, count) List~Task~
  }

  class Scheduler {
      +Date date
      +Owner owner
      +List~Pet~ pets
      +List~ScheduledTask~ plan
      +String reasoning
      +getAllTasksAcrossPets() List~Task~
      +getTasksByPriority() List~Task~
      +getTasksByDate(date) List~Task~
      +generatePlan() List~ScheduledTask~
      +addTask(scheduledTask) void
      +removeTask(taskId) void
      +explainReasoning() String
      +displayPlan() String
      +adjustTask(taskId, newTime) void
  }

  class TimeWindow {
      +String startTime
      +String endTime
  }

  class ScheduledTask {
      +Task task
      +String petId
      +String assignedTime
      +String rationale
  }

  class TaskType {
      <<enumeration>>
      WALK
      FEEDING
      MEDICATION
      ENRICHMENT
      GROOMING
      VET
      OTHER
  }

  class Priority {
      <<enumeration>>
      CRITICAL
      HIGH
      MEDIUM
      LOW
  }

  class Frequency {
      <<enumeration>>
      ONCE
      DAILY
      WEEKLY
      MONTHLY
  }

  Owner "1" --> "1..*" Pet : owns
  Owner "1" --> "0..*" TimeWindow : has availability
  Pet "1" --> "0..*" Task : has
  Task --> TaskType : categorized by
  Task --> Priority : ranked by
  Task --> Pet : assigned to
  Scheduler --> Owner : constrained by
  Scheduler "1" --> "1..*" Pet : plans for
  Scheduler "1" --> "0..*" ScheduledTask : produces
  ScheduledTask --> Task : wraps
  ScheduledTask --> Pet : belongs to


**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

No, not especially. I did ask Claude to shore up the missing bits in its UML and
skeleton code, though.

Scatch that. I saw the four class descriptions in Section 2, and had to change
some stuff.

Added a frequency attribute to the Tasks, added stuff to let Owners get all the
necessary tasks for all their pets, and renamed Schedule to Scheduler and gave
it more of a manager class role.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

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
