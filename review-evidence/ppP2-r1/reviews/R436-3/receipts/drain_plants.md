# R436-3 plants in the owed READ's drain bound (exact head 527662d6)

Edit text: `scripts/plants_drain.py`. Each plant: `scripts/run_plant.sh NAME scripts/plants_drain.py`
(`make -k run`: elab_bounds.sh, suite at 100/37/20, standing randomized harness at 1/2/3/37;
a failing build ends the recipe). Directed probes: R436g `scripts/babble_probe.sh` (babble
abandoned at every byte and terminal of a restore), R436h `scripts/resume_long_probe.sh`
(resume with payloads up to 600 bytes). Raw: `plant_*.log`, `babble_*.log`, `resumelong_*.log`.

| Plant | Defect | Standing suite + harness (1,104 checks) | R436g FZ9 fails at 3 / 37 / 100 | R436h FZ7 fails at 3 / 37 | Verdict |
|---|---|---|---|---|---|
| head | none | 1,104 PASS | 0 / 0 / 0 | 0 / 0 | - |
| Z1 | header READ abandoned in S_RHCOLL owes all 8 | **1,104 PASS** | 229 / 249 / 241 | - | survives the standing checks |
| Z2 | payload READ abandoned in S_RPPUMP owes all plen | T28f (1 of 356) | 341 / 362 / 360 | - | killed |
| Z3 | READ abandoned in S_RHWAIT/S_RPWAIT still owes 8 | **1,104 PASS** | 70 / 81 / 54 | - | survives the standing checks |
| Z4 | late-granted READ request owes 0 | 19 of 356 (T24 ...) | - | - | killed |
| Z5 | S_RPPUMP owes one more | T28f (1 of 356) | - | - | killed |
| Z6 | S_RPPUMP owes one fewer | 18 of 356 (T24, T28d-f, T30e) | - | - | killed |
| Z7 | S_RHCOLL owes one fewer | 17 of 356 (T24 ...) | - | - | killed |
| Z8 | S_RHCOLL owes one more | **1,104 PASS** | 316 / 299 / 285 | - | survives the standing checks |
| Z9 | count decremented on any byte while owed (wraps) | 3 of 356 (T28f x2, RW1) | - | - | killed |
| Z10 | count 8 bits wide (width-lint-unclean spelling) | elab_bounds.sh ELAB FAIL (WIDTHTRUNC/WIDTHEXPAND under -Wall) | - | - | killed by lint only |
| Z10b | count 8 bits wide, lint-clean spelling | **1,104 PASS** | - | 63 / 53 | survives the standing checks |
| Z11 | rready unbounded, count kept | 3 of 356 (T28f x2, RW1) | - | - | killed |
| Z12 | late-granted READ request owes len - 1 | 19 of 356 (T24 ...) | - | - | killed |
