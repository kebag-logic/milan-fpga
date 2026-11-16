# Suite runs in the lane's tree before the commits (the committed content)

These ran in the lane's worktree at 70f4056f with the five changes uncommitted (each log's first line says `dirty`),
through `tools/sim.sh.txt`, each its own unit on 8 booked CPUs, the pinned Verilator 5.050. The commits a4a0c7dc to
1010aa6f carry the same content (the docs and comments of 1010aa6f and a4a0c7dc's wording aside, which change no
build input of these suites but the meter's and the datapath's comments). The clean-clone runs are in `../editpath/`.

- `split-wip.log`: `make split`: checks 143, failures 0, the `[EDIT]` checks built in.
- `split-mut-wip.log`: `make split-mutants`: 29 of 29 caught, the three new arms among them.
- `meter-wip.log`: `make all` in `tb/verilator/aaf_clock_meter`: 465 + 6 checks, mutants 38/38.
