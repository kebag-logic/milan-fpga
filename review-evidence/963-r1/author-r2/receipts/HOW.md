# Lane 963, round 2 receipts: head a18f0996f4b1b654a232dfe56fa64ee7ecaf697e

Every unit ran in the foreground on a fresh clean `--shared` clone of `a18f0996`, under `timeout 570` so that each
fits one foreground call (`scripts/fg.sh`). A unit that the cap cut has rc 124 and is named as cut; it is not a pass.
Host paths are replaced by placeholders; a sha256 quoted inside a receipt is of the raw file.

- `delta/`: the round's one commit, `4cca9569..a18f0996` (test and plant table only), the lane's log, and the
  stat from `25d3dd7a`, the final firmware (no firmware, RTL or `tb/` file since).
- `tests/focused-head/`: at the head, `Core.MapEditsAreTheirDefinitionRowForRow` and
  `Core.MapEditWorkObservesEachOutputStreamOnce` unplanted (app and work arms, pass), then the new row
  `map-read-before-legal` and the 16 other rows the edit test grades, each caught on its own words (`scripts/focused.py`).
- `tests/probe-plant-on-r1-test/`: the new row against round 1's `test_aecp.cpp` (`4cca9569`): unplanted pass, the
  plant ESCAPED (rc 1, as wanted). The new illegal mapping is what catches it.
- `tests/probe-tallies/`: a disposable copy with the test's `>= 20` floors raised to 1,000,000, so that the log prints
  each seeded tally: 86 output edits refused at an illegal mapping of a stream they have not read.
- `firmware/shard0-aecp-arms/`: of the gate's suites phase (shard 0), the 18 AECP arms, the only arms that compile
  `test_aecp.cpp`, after the gate's own shard inventory (`1848 live invocations ...; shard sizes [88, 827, 391, 542]`).
  The other 70 suite arms of shard 0 were not re-run at this head (`scripts/aecp_suite_arms.py`).
- `firmware/aecp-campaign/p0..p19/`: shard 2's table, the AECP campaign, through its own foreground-sized entry point
  (`aecp_mutants.py --output D --shard i 20`, the same `campaign()` the gate's shard 2 calls with `(0, 1)`);
  `union.txt`: 390 rows, 390 `[ok]`, 0 `[ESCAPED]`, every row once. The gate command `--shard 2/4` itself was not run.
- `firmware/plant-tally.txt`: each shard's own units, counted from the gate's printed lines in its complete log
  (`scripts/count_plants.py`). The round-1 logs' sha256 match the headers of round 1's published excerpts.
- `coverage/`: the coverage ratchet. `coverage-selftest` is `fw_coverage.py --selftest`. `--check` as one unit was cut
  by the cap (`coverage-check-cut-by-cap`, rc 124), so `scripts/coverage_split.py` ran its two coverage-mode gate runs
  (`coverage-ctrl`, `coverage-nvm`, the argv `coverage_runs` gives) and then `coverage-check`, the path `--check`
  takes over both directories: `firmware coverage: PASS (40 files)`.
- `docs/group-1..4/`: 43 of the docs workflow's 46 gate steps, each the workflow's own step body
  (`scripts/docs_steps.py`), rc 0 each; `gate_8` (em dash) against the push base `dd163e41`, which is the merge base
  with `dev-soft-core` `854bd723`. `docs/gate_24-cut-by-cap-{1,2}/`: `gate_24` (compiler-absent firmware controls) was
  cut by the cap twice, rc 124: not run to completion. The two builder legs (`gate_25_0`, `gate_25_1`) were not run.
- `side-effects.txt`: what the runs left in their clones.
- `scripts/`: every script this round ran.
