"""
Scheduler library for MicroPython.
Manages multiple cooperative tasks with optional profiling and enable/disable.
"""

import time
import gc

class Scheduler:
    def __init__(self, tasks=None, enable_profiling=True):
        """
        tasks: list of task modules
        enable_profiling: if True, collect execution time stats
        """
        self.tasks = tasks or []
        self.stats = {}
        self.enable_profiling = enable_profiling
        self._init_stats()
        self._sort_tasks()
        self._last_print = time.ticks_ms()  # Track last print
        
    # ----------------------
    # Internal Methods
    # ----------------------
    def _sort_tasks(self):
        # Sort tasks by PRIORITY (higher runs first)
        self.tasks.sort(key=lambda t: getattr(t, "PRIORITY", 0), reverse=True)

    def _init_stats(self):
        self.stats = {}
        for t in self.tasks:
            self.stats[t.__name__] = {
                "calls": 0,
                "total_us": 0,
                "max_us": 0,
                "enabled": True
            }

    # ----------------------
    # Public Methods
    # ----------------------
    def add_task(self, task_module):
        """Add a new task and initialize stats."""
        self.tasks.append(task_module)
        self.stats[task_module.__name__] = {
            "calls": 0,
            "total_us": 0,
            "max_us": 0,
            "enabled": True
        }
        self._sort_tasks()
        if hasattr(task_module, "init"):
            task_module.init()

    def remove_task(self, task_module):
        """Remove task from scheduler."""
        if task_module in self.tasks:
            self.tasks.remove(task_module)
            self.stats.pop(task_module.__name__, None)

    def enable_task(self, task_module):
        self.stats[task_module.__name__]["enabled"] = True

    def disable_task(self, task_module):
        self.stats[task_module.__name__]["enabled"] = False

    def initialize(self):
        """Call init() for all tasks."""
        self._sort_tasks()
        for t in self.tasks:
            if hasattr(t, "init"):
                t.init()

    def step(self):
        """Run one scheduler cycle (non-blocking)."""
        for t in self.tasks:
            if not self.stats[t.__name__]["enabled"]:
                continue

            start = time.ticks_us()
            if hasattr(t, "step"):
                t.step()
            duration = time.ticks_diff(time.ticks_us(), start)

            if self.enable_profiling:
                s = self.stats[t.__name__]
                s["calls"] += 1
                s["total_us"] += duration
                if duration > s["max_us"]:
                    s["max_us"] = duration

    def run_forever(self, print_interval=5000):
        """
        Blocking loop that runs step() continuously.
        Optional print_interval in ms to show stats.
        """
        last_print = time.ticks_ms()
        while True:
            self.step()

            # Print stats periodically
            if self.enable_profiling:
                now = time.ticks_ms()
                if time.ticks_diff(now, last_print) >= print_interval:
                    self.print_stats()
                    last_print = now
                    gc.collect()

            time.sleep_ms(1)  # scheduler tick

    def print_stats(self, interval_ms=5000):
        """Print stats if interval_ms has passed since last print."""
        now = time.ticks_ms()
        if time.ticks_diff(now, self._last_print) >= interval_ms:
            print("\n--- Task Stats ---")
            for name, s in self.stats.items():
                avg = s["total_us"] // s["calls"] if s["calls"] else 0
                print(name,
                        "avg:", avg, "us",
                        "max:", s["max_us"], "us",
                        "calls:", s["calls"],
                        "enabled:", s["enabled"])
            gc.collect()
            self._last_print = now