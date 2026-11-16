# Tools

The scratch scripts this round ran, copied as text with host paths replaced. `route_queue2.sh` and `route_queue4.sh`
ran the Vivado builds one after another, each through the shared `vivado-slot.sh`; `unitpool.sh` and `unit.sh` run
each job as its own user unit under a memory cap; `pick4.py` takes the sweep's four CPU ranges from `cpu_ranges.py`.
