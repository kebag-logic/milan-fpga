# superseded/engine-arm-fixcheck

The engine mutation arm (`tb/verilator/engine/mutants.py`) run by arm_jobs.py: job 000 is the arm's own unmutated control, every other job is `mutants.run_mutant()` on one MUTATIONS entry, in parallel workers (8 for a full arm, 3 for the fix check).

Tally: 3 checks: 3 PASS, 0 FAIL

## 000 ok: control (108.3 s)
    [PASS] the unmutated engine: pass

## 129 ok: a late response completes its exchange (107.0 s)
    FAIL #100 late responses: the fifth clears asCapable got 0000000000000000 exp 0000000000000001
    FAIL #100 late responses: none moves the delay got 0000000000000001 exp 0000000000000000
    [PASS] mutant caught: a late response completes its exchange - breaks "#100 late responses: the fifth clears asCapable | #100 late responses: none moves the delay"

## 137 ok: mastership never publishes the master bit (141.4 s)
    FAIL #84 master cycles were graded got 0000000000000000 exp 0000000000000001
    FAIL p1 255 #84 master cycles were graded got 0000000000000000 exp 0000000000000001
    [PASS] mutant caught: mastership never publishes the master bit - breaks "#84 master cycles were graded | p1 255 #84 master cycles were graded"

