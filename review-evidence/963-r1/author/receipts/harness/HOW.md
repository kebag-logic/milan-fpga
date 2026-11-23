# The CPU service-budget harness, base `dd163e41` against head `e9627b31`

**What ran.** Every arm at 1x1/1if and 8x8/1if, each run one group in its own unit, with the formal measurement's
options: `run.py --reuse-build --groups G --record-budget-findings --record-share-findings --fetch-l1 split`. Each
arm's build is `legs.py build` (as `run.py` builds by default). The runs:
- **Every group of every arm**, except arm A's and answering-ports' 72 save windows (`backlog-adp@...`) at each point.
- **Of those windows, one a phase-and-age family**, 9 of 72, at offsets spread over the eight: `blank-0`,
  `blank-aged2-3`, `blank-aged1-6`, `program-1`, `program-aged2-4`, `program-aged1-7`, `verify-2`, `verify-aged2-5`,
  `verify-aged1-0`. The host's load (100 to 320 on 96 CPUs) left the full set, 35 % of the measurement's simulated
  time, out of a day's reach.
- **The count:** 229 groups a tree, 458 runs, every run rc 0. A run whose scheduler stopped before it ended was graded
  again from its log (`run.py --regrade`, same options) for its rc.

**The differential** (`diff.txt`, `diff.json`; `tools/diff_full.py`). For each group both trees ran, what the device
made observable, times aside, each compared in each run's own order:
- every wire frame per channel and interface, byte for byte;
- every publication word write;
- the TXC counts, the RESULT line, the refusals;
- each probe's status and budget and ceiling verdicts;
- the graded costs over their statements, and the refusals and findings.

THE SHARE is reported beside it: the base's over-counts are the finding.

Two equivalences are named and counted where they apply. Each is timing, not function, and each is checked, not
assumed:
- **The flood's grandmaster identity.** In a group whose stimulus floods a grandmaster change as every pass starts
  (`flood gm 1`), the testbench's identity is `0x0a0b0c0dfffd0000` plus the flood's count, one a pass (`sim_main.cpp`,
  `flood_gm`). A frame carries the identity current at its build, so it counts the passes before it. Such identities
  are masked, and every masked frame is counted.
- **The order of AECP notices across descriptors.** In the answering-every-port arm's notice windows, THE RETRY's
  rounds send every pending notice in another order across descriptors. Each recipient (`controller_entity_id`) must
  receive the same unsolicited frames, `sequence_id` aside, with its sequence_ids consecutive in both runs; every
  solicited frame must be the same, in order.

**The costs** (`costs.txt`; `tools/cost_compare.py`). The most measured of each graded cost over every group of every
arm, per point, base and head:
- the poll items, the passes given whole, THE RETRY's rounds, the tier-2 slices;
- the longest work pass;
- the record handlers' spans.

`record.adp_mbx:on_frame` is not a handler's cost: its spans run from an entry to a much later return, median 2,647
cycles, the outliers identical at base and head.

**The record classes** (`record-classes-base.txt`, `record-classes-head.txt`; the harness's `record_classes.py`, run
over each tree's runs):
- each held AECP record class's dearest record against its statement, at both points;
- the arm-A completeness refusals, one for each window not run, the same at base and head by design.
