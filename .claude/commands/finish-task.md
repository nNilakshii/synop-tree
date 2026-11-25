---
description: Verify, tick and commit the current tracker task
---
1. Run `make check`. If the Makefile doesn't exist yet, run whatever checks exist and say so. If anything fails, stop and report.
2. Show evidence that the task's "done when" condition is met.
3. In docs/TRACKER.md: tick the task, update the Done counts in the Progress table, and set "Now" to the next task.
4. If something non-obvious was learned and docs/notes/learning-log.md exists, append a dated entry (Pacific Time).
5. Stage only this task's files and commit as "<TaskID>: <short summary>". Don't push.
