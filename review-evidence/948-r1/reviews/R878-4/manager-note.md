Manager commit 8aeb2f0b on PR #959 (#948), from 64117b77.

The hosted rtl-fast job firmware-verilator (run 45191675681, attempt 2, on PR #959's merge ref over dev-soft-core aa30d77f) failed ctrl_boundary: "sw/firmware/ctrl/README.md gives the pin controls as 185, where the self-test has 192". The count is ctrl_pin.pin_controls'. It counts the Makefile targets whose recipes build against the TSN stack, and #959 adds stack-building plants (tb/verilator/milan_dp fan_stop_plant.py, twin_fanout_plant.py and their recipes).

The merge candidate passed because its native bank does not run ctrl_boundary. That gap is the manager's.

The commit changes one line, README.md:255, from 185 to 192. docs_inventory.py --check is fresh. The hosted ctrl_boundary run on the new head is the verifying run.
