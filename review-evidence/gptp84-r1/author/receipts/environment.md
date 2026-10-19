# Run environment and method

## Revisions
lane base: 43acfbcc098f5af1be20a4a5458770ead3717622
lane #84 commit: 4d6288e82ebf40d10d7521a7a675feacd502b847
lane head (#85 commit): 53ac2e9d75ceb381c2d2b04854e760304d9ae43f
parent: milan-fpga dev e9cbb676d7fdd6539aa408e5dfe38870a4ae1a5f
parent base snapshot (local commit, gitlink 43acfbcc): f33791181f7be9265a7757a299f80ad2f1054ea1
parent head snapshot (local commit, gitlink 53ac2e9d): 0edefe5dc98bfcdbf102f21426a92326e450b5b6
parent #84-only snapshot (local commit, gitlink 4d6288e8): 7ffb076372802e81035547d73fb1920012e63d84
parent adoption snapshot (local commit on the head snapshot: gitlink 53ac2e9d plus parent-adoption-gptp_shadow-85.patch, committed; its diff from dev e9cbb676 is exactly those two): 28e1085fb57ac95ec660f3f6a4449e08657e956c
parent companion demonstration snapshot (local commit, gitlink 53ac2e9d, plus the uncommitted patch): dfe515e9840a1eb7f919efa5391c2de114560bd5

## Submodules of each snapshot
### parent
 efeb541ae5fe1e078332d8462dca2fc2d9cb8db5 external (heads/main)
 43acfbcc098f5af1be20a4a5458770ead3717622 gptp-processor (heads/main)
 2cbed0a987c1e68402658d69459ab7e5aa571adc protocol-processor (v2.0-695-g2cbed0a)
 08ee86e812a0eb5e1dc6cd61b494d8baf3491348 third_party/lwSRP (remotes/origin/lwsrp17-group-1-g08ee86e)
 70936b77dc41981e192438388cd0aced69954f18 third_party/tsn-c-stack (heads/main)
 48ff7a7e2ef782cf778d47910cf85835c64b1bce third_party/verilog-axis (heads/master)
### parent-c (head snapshot and adoption snapshot; unchanged by the adoption commit)
 efeb541ae5fe1e078332d8462dca2fc2d9cb8db5 external (heads/main)
 53ac2e9d75ceb381c2d2b04854e760304d9ae43f gptp-processor (heads/main-2-g53ac2e9)
 2cbed0a987c1e68402658d69459ab7e5aa571adc protocol-processor (v2.0-695-g2cbed0a)
 08ee86e812a0eb5e1dc6cd61b494d8baf3491348 third_party/lwSRP (08ee86e)
 70936b77dc41981e192438388cd0aced69954f18 third_party/tsn-c-stack (heads/main)
 48ff7a7e2ef782cf778d47910cf85835c64b1bce third_party/verilog-axis (heads/master)

## Tools
Verilator 5.050 2026-07-01 rev v5.050
Python 3.14.8

## Method
- Lane gates: every target of the repository Makefile's 'all' recipe, run one by one (contract, lint, docs with diagrams-check, each tb suite, bench test), plus the ooc clock-order selftest.
- Engine mutation arm: tb/verilator/engine/mutants.py's own stage/build/run_harness/run_mutant functions, driven in parallel slices of three arms (24 slices), each slice repeating the unmutated positive control, because the sequential arm exceeds one foreground command.
- Parent gates: the manager's 11-command consumer list, same PATH shape and VERILATOR_ROOT. sw/builder/test_builder.py ran as the parent's own two measured legs (--gates/--receipt): leg 0 = test_baremetal_profile_contract alone, leg 1 = the other 102 gates in inventory order; scripts/ci_builder_legs.py union() judged both receipts per snapshot.
- Leg 0 takes 1087 s (base) and 1263 s (head), longer than one foreground command, so that single gate ran as a background job while the session polled in the foreground until it ended. Every other command ran in the foreground.
- Base and head parent snapshots ran in separate parent checkouts, each with its submodules initialised at their pins (no copies, no symlinks); one checkout never ran two gates at once.
- Temporary files: the engine mutation slices always used the lane's scratch. The lane base gates (whose parser, gasket and tsngen arms create temporary directories) and the base parent snapshot's baremetal leg used the tools' default temporary directory; every other cited run set TMPDIR to the lane's scratch.
- Round 1b (parent companion): the full 11-command list reran on the adoption snapshot in the parent-c checkout, same method; builder leg 0 took 1082 s and again ran as a background job polled in the foreground, nothing else ran in that checkout meanwhile. TMPDIR was the lane's scratch for every Round 1b run.
- Round 1b companion mutants (parent-adoption-mutants/): in the separate parent-head checkout, the companion patch applied uncommitted and one gptp-processor mutant planted at a time (exact text from the lane's engine mutants.py), then the shadow suite alone (make run); the tree was restored afterwards. The mutation arm was not run there because it refuses uncommitted input by design.
- Placeholders: <parent-base-snapshot> is the checkout of the base snapshot; <parent-head-snapshot> is the checkout of the #84-only and demonstration snapshots and of the companion mutants; <parent-c-checkout> is the checkout of the head and adoption snapshots (parent-head/06.log was rescrubbed with that placeholder, which an earlier rule had rendered as <parent-base-snapshot>-c).
- Host paths in these receipts are replaced by placeholders: <lane>, <lane-base>, <lane-head>, <parent-base-snapshot>, <parent-head-snapshot>, <parent-c-checkout>, <scratch>, <pinned-tools>, <home>, <tmp>, <data>, <user>.
