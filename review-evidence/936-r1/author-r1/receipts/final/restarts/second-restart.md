Original file: <scratch>/restart2-notes.md
Original size: 3106 bytes
Original sha256: 1b0570d69040a99fe14bb2096e4907739a12708fe981a60a3cb7d17911e1818b

# Second restart (host down 07:25, back 08:00 CET 2026-11-17), resumed about 08:14

- 08:15-08:17: qrun.sh started 21 units; cpu_ranges.py pick answered for every one, overlapping ranges. Cause: the
  owner's pool-spill (changed 08:12, "use all processors") widens every pinned process of the user to 0-95 each
  minute, so busy() sees no booking. Not a fault of the jobs; their results are simulated cycles, not wall time.
- 08:21: 10 of the 18 then running stopped by name (j-a1-1, j-a1-2, j-a8-0..2, j-every-1x1, j-later-1x1,
  j-later-8x8-1if, j-vd-1x1, j-vd-8x8-1if); their cut outputs removed; requeued. 8 kept (j-unit, j-srp, j-aecp,
  j-ctl, j-bnd, j-twin, j-docs, j-a1-0).
- 08:22-08:27: re-pinned the 8 kept units to 0-7..56-63; the spill widened them again within 60 s; then found the
  owner's rule and stopped re-pinning. qrun.sh now caps the lane at 8 concurrent j-* units (load < 80, mem > 20 GB).
- The first shard replay (j-shards-a/b/c, 08:17) ran no suite: the replay tool's not_run.json, inherited from
  another lane, skipped every step of rtl.yml/verilator-shards with that lane's reason. Voided (logs/void/); the
  skip list now runs steps 1, 2, 3, 8, 9 and 21 and skips only apt installs, the shard-3-only Yosys/sv2v installs
  and the tsn-gen clone (TSN_GEN_ROOT is the same revision's build). Shards 4, 1, 6, 10, 17 requeued one per unit.
- wf_batch.sh's clone cleanup glob would have removed a concurrent shard's clone; now removes its own job's only.
- 08:36-08:39: the shard replays then reached step 21 and the sweep refused shards 4 and 6 at once ("source
  dependency origin differs: third_party/tsn-c-stack", `scripts/ci_case_receipts.py:84`): the replay had pointed the
  submodules' origin at the lane's module stores. Both runs voided (wf/void-shards-origin/), shards 1, 10, 17 stopped
  by name before they reached it; run_wf.py now sets each initialized submodule's origin to its .gitmodules URL after
  the submodule step, as the hosted checkout leaves it (named at the end of that step's log). All five re-run.
- 09:10-: host load about 120 (another lane's nine 8-CPU units and mine); qrun.sh holds new starts while the 1-minute
  load is 80 or more.
- 11:07: host load 190-240 for an hour from other lanes' 22 units; the lane's variant arms had waited since 09:50 at 3 of its 8 units. qrun.sh run with LOAD=250 (the cap of 8 units, the 60 s spacing and the 20 GB memory floor kept).
- 11:41: qrun.sh counted only j-* units, so k-litex started as the lane's ninth unit; the count now takes j-* and k-*.
- 12:20: k-litex's first run: the builder legs refused on tsn-c-stack's origin (clone.sh leaves the lane's module store as each submodule's origin), and test_soc_timing_cuts timed out at the hosted 900 s at load 150 (an unknown, not a failure; the other 7 LiteX members passed). Voided (logs/void/k-litex-1.log, out/litex-k-1); k_litex.sh now restores each submodule's origin and sets LITEX_SIM_TIMEOUT=3600; requeued.
- 12:22-12:37: cpu_ranges.py pick answered nothing (another lane's act replay booked every range); the queue waited, the running units went on.
