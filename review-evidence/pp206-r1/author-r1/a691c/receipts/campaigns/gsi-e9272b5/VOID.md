# Void run

A first launch of the same driver at `e9272b5` with `--jobs 4` (started 2026-10-27T08:48:33Z) was stopped by
this lane at 08:53Z, after its golden PASS, on memory alone. The lane unit's memory.current reached 8.7 GiB
(7.9 GiB anonymous, four builds of eight compile threads each) against the 9 GB budget. Its process group was
terminated, and its four temporary build trees (each `pp-gsi-mutants-*`, created at the stop) were removed after
checking that no process used them. Its output was discarded and is cited nowhere. The run here used `--jobs 3`,
which keeps the eight pinned CPUs busy during compiles with fewer concurrent compilers (MEMORY.txt).
