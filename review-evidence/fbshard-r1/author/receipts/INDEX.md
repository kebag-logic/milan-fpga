# Receipts: #980 firmware-boundary shards, round 1 ([A827])

Lane `pf-fbshard-1`, base `854bd7236`, head `b7b351935f65416c8632c21dd13e08fb2e9c1d9c`.
Local runs used a shared 96-CPU host under load (load average 34 to 43 from other lanes).
Every builder ran with its own four jobs, as on the hosted runner.
Each log line carries seconds since its run started (`tools/a827-ts.py`).

## Final evidence (at the commits named)

| Receipt | What | Result |
|---|---|---|
| `final-shard-0of3.log` | `--shard 0/3` at `d7da99cf`: control gate part 0/2, store, RV32 self-test | rc 0, **462 s** |
| `final-shard-1of3.log` | `--shard 1/3` at `d7da99cf`: control gate part 1/2, reset entry | rc 0, **393 s** |
| `final-shard-2of3.log` | `--shard 2/3` at `d7da99cf`: coverage gate, F5 at both shapes | rc 0, **449 s** |
| `final-judge-3-shards.log` | judging run at `d7da99cf` over upload-shaped copies of the three captures (records, manifest, text only), the workflow step's own shell loop | PASS, 259 s |
| `head-judge-3-shards.log` | the same judging run at head `b7b35193` | PASS, 250 s; 112 boundary, 185 pin, 4 figure, 4 shard controls, 0 misbehaved |
| `control-gate-union-proof.log` | source-level union: the whole `test_ctrl_firmware.py --build-only` capture against its two parts' captures | 1262 = 1262 distinct compiles, 0 missing, 0 extra: PASS |
| `full-control-gate-build-capture.log` | the whole control gate build-only run under a capture at `d7da99cf` | rc 0, 714 s |
| `plant-dropped-capture.log` | judging run given shards 0 and 1 only | rc 2, refused naming `fw_coverage.py` and both F5 runs |
| `plant-duplicated-capture.log` | judging run given shard 0's capture twice | rc 2, refused naming each shard-0 unit run twice |
| `plant-table.log` | `ctrl_configs.SHARDS` with a unit dropped, then with it in two shards; `--shard 0/3` | rc 2 each, refused by name before building |
| `head-ci-and-docs-gates.log` | 28 CI and docs gates at head (generator check, `ci_events --check`, every CI scheduling self-test, wire-accountability, docs, doc paths, doc style, em-dash, hygiene, TODO, sh and py idiom, docs inventory, act runner self-test) | all rc 0 |
| `head-ci_events-selftest.log` | `ci_events.py --selftest` at head | PASS, 2369 items, 5881 arms |
| `hosted-unsharded-45071981993.txt` | the last green hosted unsharded job, phase by phase | step 1273 s, builds 1063 s |

## Baseline and design measurements

| Receipt | What |
|---|---|
| `full-baseline-854bd723.log` | the unsharded `--selftest --without verilator` run at the base: RV32 self-test 9 s, control gate 714 s, store 96 s, coverage gate 378 s; it then stopped at `test_ctrl_memory.py` because this host's default Python has no `migen` (later runs used the LiteX venv, as the hosted job installs `sw/litex/litex_pins.txt`) |
| `arm-times-part-*of3-pre-flatten.txt` | per-suite build times through `suite_arms` before the AECP arms were flattened: `aecp_arms.all_arms` alone took 334 s of about 690 s, which is why it is now a list of arms |
| `shard-*of3.log`, `judge-trial.log` | the first, unbalanced table (411 / 502 / 383 s) and its judging run (PASS, 253 s), which set the final table |
| `ci_events-selftest.log`, `ci-scheduling-controls.log`, `act_ci-selftest.log`, `check_py_idiom.log`, `docs-and-hygiene-gates-pre-docs.log` | the same gates on the working tree before the docs commit |
| `commits.txt`, `diffstat.txt` | the lane's three commits and their footprint |

## Tools (measurement only, not committed)

- `tools/a827-ts.py`: prefixes each line with seconds since start.
- `tools/arm_times.py`: times each `suite_arms` entry of one `--build-part` share.
- `tools/compare_sets.py`: the source-level union proof (compiled source plus dependency list, temporary directories normalised).
