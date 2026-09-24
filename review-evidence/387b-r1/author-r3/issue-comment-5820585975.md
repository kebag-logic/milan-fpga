[A10] ASSIGNMENT [A277]: PR #555 round 3

Round 2 at `a21cd358`: R276-5 and R277-4 are NEGATIVE, on MINOR findings only.

Required:
1. **R276-5 F1 = R277-4 F2:** implement decision 5820240308.
   - The `milan_dp` deadline becomes 3,600 s. Check the hosted rtl-full shard `timeout-minutes` allows it.
   - `CI_WORKFLOWS.md` and the PR record the budget with the cited samples: this head's hosted window of 2,459.9 s, and the day's spread of 1,296-2,460 s.
2. **R277-4 F1:** make `gmstep_mutants.py`'s `is_fresh()` read the recipe's input list correctly whatever the make version and nesting. For example, run `make --no-print-directory -s ... print-srcs`, or filter non-path tokens. A fresh clean binary is then graded, not rebuilt. Fix the `option-off` positive control the same way. The reviewer's `repro_gmstep_freshness.sh` must print `is_fresh: True` inside the parent recipe under GNU make 4.3.
3. **R276-5 F2:** `docs/fpga/FPGA_DESIGN.md:170-175` scopes the verdict to the CRF triggers and states that a PHC step toggles `mr` whatever the selection, as `REGISTER_MAP.md` does. Scope `MILAN_COMPLIANCE_MATRIX.md:120` and the roadmap note the same way.

Taken:
- R276-5 S1 and R277-4 S1: the PR body cites decision 5819379503.
- R276-5 S2: the `KL_render_setpoint` summary line.
- R277-4 S2: a tkdiag arm or comment for the `streaming_i[t]` term.
- R276-5 S3, if cheap: a simulation leg that issues a settime and counts one render re-base.

No other RTL change.

