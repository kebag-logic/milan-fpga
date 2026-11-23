# The CPU service-budget harness at the final firmware `25d3dd7a`, against the base `dd163e41`

**What ran (re-run after the host crash of 2026-11-23 00:39, from clean state).**
- **The groups.** Every group of every arm at 1x1/1if and 8x8/1if, `run.all_groups` of each of the 16 builds: 481 a
  tree, the 72 save windows of arm A and answering-ports at each point included.
- **The driver.** A process checkpoint driver (`ck7-*.log`) forks the compiled model at the prefixes the groups'
  scripts share, on the original compiled model archive. Each arm is calibrated: one group's ordinary complete run
  must be byte-identical to the driver's log of it (`calibration/`, 16 of 16 identical).
- **The journal groups.** The groups that write a journal (`save-burst`, `save-flight`) run ordinarily.
- **The grade.** Every group is graded by the tree's own `run.py --regrade` with the formal options
  (`--record-budget-findings --record-share-findings`); every rc is 0.
- **The base.** The base's 481 come from the same procedure (`harness-complete/base/`).

**What it shows.**
- `strict-diff.txt`, `strict-rows.json` compare, per group and with nothing masked: every wire frame per channel and
  interface, in order, byte for byte; the publication writes; the TXC counts; RESULT; the refusals; every probe's
  status and budget and ceiling verdicts. Only timestamps are excluded. 481 of 481 groups exact.
- `record-classes-head.txt`: the harness's `record_classes.py` over the head's 481 runs, RESULT: PASS.
- `measured-model.json`, `load-comparison.json`: #872's load model (`load_grade.load`, the same derivations) on this
  lane's complete measurements, base and head. Delta 0.0 at both points.
