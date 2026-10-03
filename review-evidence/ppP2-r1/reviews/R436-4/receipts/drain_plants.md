# R436-4 drain-bound plants at exact head 3957814550f164d72bfaad5d28cd0e7cac0ecaaf

R436-3's plants run unchanged (`scripts/plants_drain.py`, byte-identical to the R436-3 packet;
`scripts/run_plant.sh` with only its head pin and clone path changed): `make -k run` =
elab_bounds.sh, then the suite at 100 / 37 / 20, then the harness at 1 / 2 / 3 / 37 (built at
MAX_PAYLOAD_P = 65,527); the first failing build ends the recipe. R436-4's own plants:
`scripts/plants_r4.py` (W9-W15: the owed count N bits wide, lint-clean; Y1: every abandoned
command taken as a READ). Raw: `plant_*.log`, `r4plant_*.log`, `babble_*.log`, `resumelong_*.log`.

| Plant | Defect | Standing `make run` at the head | Named by | Round 3 |
|---|---|---|---|---|
| head | none | 1,219 / 1,219 PASS (393 x 3 + 10 x 4) | - | 1,104 PASS |
| Z1 | S_RHCOLL owes its whole 8 | fails 2 of 393 | T28g | passed everything |
| Z2 | S_RPPUMP owes its whole length | fails 1 of 393 | T28f | killed |
| Z3 | a READ wait state owes 8 | fails 2 of 393 | T28h | passed everything |
| Z4 | late-granted READ owes 0 | fails 22 of 393 | T24, T28i, T28j | killed |
| Z5 | S_RPPUMP one over | fails 1 of 393 | T28f | killed |
| Z6 | S_RPPUMP one short | fails 20 of 393 | T24, T28d-f, T28j, T30e | killed |
| Z7 | S_RHCOLL one short | fails 19 of 393 | T24, T28g | killed |
| Z8 | S_RHCOLL one over | fails 2 of 393 | T28g | passed everything |
| Z9 | count decremented on any byte (wraps) | fails 15 of 393 | T28f-i, RW1 | killed |
| Z10 | count 8 bits (lint-unclean spelling) | elab_bounds.sh width lint (ELAB FAIL at 1 and 2^31-1) | lint | lint only |
| Z10b | count 8 bits, lint-clean | fails 3 of 393 | T28j (590 and 1,024 owed) | passed everything |
| Z11 | rready for the whole owed READ | fails 15 of 393 | T28f-i, RW1 | killed |
| Z12 | late grant owes len - 1 | fails 27 of 393 | T24, T28h-j, RW1 | killed |
| W9 | count 9 bits | fails 3 of 393 | T28j | (new) |
| W10 | count 10 bits | fails 2 of 393 | T28j (1,024 owed) | (new) |
| W11 | count 11 bits | suite 393/0 x3; harness at 1 fails 2 of 10 | FZ7, FZ10 (READ owing 65,527) | (new) |
| W12 | count 12 bits | suite 393/0 x3; harness at 1 fails 2 of 10 | FZ7, FZ10 | (new) |
| W13 | count 13 bits | suite 393/0 x3; harness at 1 fails 2 of 10 | FZ7, FZ10 | (new) |
| W14 | count 14 bits | suite 393/0 x3; harness at 1 fails 2 of 10 | FZ7, FZ10 | (new) |
| W15 | count 15 bits | suite 393/0 x3; harness at 1 fails 2 of 10 | FZ7, FZ10 | (new) |
| Y1 | an abandoned WRITE taken as a READ | fails 1 of 393 | T28k (48 read bytes taken) | (new) |

R436g (`babble_probe.sh`, babble abandoned at every byte and terminal, MAX_PAYLOAD_P 1,024):
head 0 fails at 3 / 37 / 100; Z1 293 / 281 / 299, Z2 297 / 274 / 320, Z3 80 / 70 / 105,
Z8 356 / 332 / 348 FZ9 failures. R436h (`resume_long_probe.sh`, resume with payloads to 600):
head 0 at 3 and 37, both branches taken; Z10b fails FZ7 117 (3) and 111 (37) times.

The gate's rows for Z1-Z12 and Z10b carry R436-3's edit text byte-for-byte
(`rows_vs_plants.txt`), and `measure_figures.py --check` measured every Z and B row equal
to the README (`figures.log`).
