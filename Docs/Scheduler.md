# Chapter 9: Scheduler

**Author: Somtochukwu Emeka-Onwuneme**

---

This document presents the entity-relationship model of the library ```scheduler.py```

---

## Entity Relationship

**Entity Relationship Model: ```Scheduler```**

**Entity: Scheduler**

**Attributes (Properties / State)**

```tasks``` → List of task modules currently registered with the scheduler. Each task module is expected to have ```init()``` and ```step()``` functions.

```stats``` → Dictionary mapping each task's ```__name__``` to a stats dict containing: ```calls``` (number of times stepped), ```total_us``` (cumulative execution time in microseconds), ```max_us``` (worst-case execution time), and ```enabled``` (boolean).

```enable_profiling``` → Boolean flag controlling whether execution time statistics are collected during ```step()```.

```_last_print``` → Timestamp (ms) of the last stats printout, used to throttle ```print_stats()``` output.

**Methods (Behaviours)**

```__init__(tasks=None, enable_profiling=True)``` → Constructor; accepts an optional list of task modules, initialises stats for each, sorts tasks by priority, and records the initial timestamp.

```_sort_tasks()``` → Internal method. Sorts the task list by each module's ```PRIORITY``` attribute in descending order (higher priority runs first). Tasks without a ```PRIORITY``` attribute default to 0.

```_init_stats()``` → Internal method. Rebuilds the stats dictionary from the current task list.

```add_task(task_module)``` → Adds a new task module to the scheduler, initialises its stats, re-sorts by priority, and calls the task's ```init()``` if it exists.

```remove_task(task_module)``` → Removes a task module from the scheduler and deletes its stats entry.

```enable_task(task_module)``` → Sets a task's ```enabled``` flag to ```True``` so it runs on the next ```step()```.

```disable_task(task_module)``` → Sets a task's ```enabled``` flag to ```False```, skipping it during ```step()``` without removing it.

```initialize()``` → Re-sorts tasks by priority and calls ```init()``` on every registered task module that has one. Intended for initial setup after all tasks are registered.

```step()``` → Runs one scheduler cycle. Iterates through all enabled tasks and calls their ```step()``` function. If profiling is enabled, measures each task's execution time and updates stats (call count, total time, max time).

```run_forever(print_interval=5000)``` → Blocking loop that calls ```step()``` continuously. If profiling is enabled, prints stats and runs garbage collection at the specified interval (ms). Includes a 1ms tick delay per cycle.

```print_stats(interval_ms=5000)``` → Prints average execution time, max execution time, call count, and enabled state for each task — but only if the specified interval has elapsed since the last print. Runs ```gc.collect()``` after printing.

**Relationships**

- Scheduler ↔ Task Modules
    - 1 Scheduler manages 0 or more task modules. Each task module is a standard Python module with ```init()``` and ```step()``` functions.

- Scheduler ↔ Priority
    - Tasks are sorted by a ```PRIORITY``` attribute (integer). Higher values run first. Tasks without ```PRIORITY``` default to 0.

- Scheduler ↔ Stats
    - 1 Scheduler maintains 1 stats dictionary entry per registered task, tracking execution performance.

- Scheduler ↔ MicroPython Modules
    - Depends on ```time``` (for ```ticks_ms```, ```ticks_us```, ```ticks_diff```) and ```gc``` (for memory management on constrained boards).

---

## Task Module Contract

Any module registered with the Scheduler should follow this interface:

```PRIORITY``` → (Optional) Integer. Higher values run first. Defaults to 0 if not defined.

```init()``` → (Optional) Called once when the task is first added or when ```scheduler.initialize()``` is called. Used for hardware setup.

```step()``` → (Required) Called on every scheduler cycle. Must be non-blocking — return quickly and let the scheduler call you again on the next cycle.

```cleanup()``` → (Optional) Not called by the scheduler directly, but used by programs like ```buttonTogglePrograms.py``` to tear down hardware state when switching tasks.
