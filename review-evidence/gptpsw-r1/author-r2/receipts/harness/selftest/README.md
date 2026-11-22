# The harness self-test at `c9f6b873`

`python3 -B tb/verilator/ctrl_service_budget/run.py --self-test` in a clean clone at `c9f6b873`; the commits after it change none of the harness's inputs. `run-self-test.log` keeps its PASS/FAIL, MUTANT and verdict lines; the CONTROL lines are dropped (the full log is in LARGE.txt).

Checks: 1017 PASS, 0 FAIL. Mutants: 297 caught, 0 escaped. Verdict: self-test: 0 failures.
