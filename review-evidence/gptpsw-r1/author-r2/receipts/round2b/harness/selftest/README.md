# The harness self-test at `62fcd154`

`python3 -B tb/verilator/ctrl_service_budget/run.py --self-test` in a clean clone at `62fcd154`; `f15b3a7d` after it changes only the closed loop's Makefile, none of the harness's inputs. `run-self-test.log` keeps its PASS/FAIL, MUTANT and verdict lines; the CONTROL lines are dropped (the full log is in LARGE.txt).

Checks: 1017 PASS, 0 FAIL. Mutants: 298 caught, 0 escaped (round 2's 297 and "grade: a burst stated an interface held at one interface's"). Verdict: self-test: 0 failures.
