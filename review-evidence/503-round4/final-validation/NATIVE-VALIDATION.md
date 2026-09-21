[A10] Complete native validation passed at `2a2007cff57bd2a01254e1da7c43ec73b9d8d4b3`, finished 2026-09-21 18:55:41 CEST.

The clean tested tree `1fc6e7edcfc5a3e1f055ed1f73ba70614996977e` is also the candidate merge tree against live `dev` `2d8fd62fd986ea2d6a87d284e144f023034c0944`: base ancestry and `git merge-tree --write-tree --no-messages <base> <head>` were checked after the run. Candidate and trusted-runner checkouts are clean; all three required submodules match their pins. Only four Markdown files under `docs/` change.

| Native command, from the candidate checkout | Result |
|---|---|
| `bash scripts/run_all_suites.sh "$VALIDATION_TMP/full-suite-logs" --wait` | exit 0; 55 suites, 2,118,264 counted checks, zero failures/timeouts |
| `bash syn/yosys/run.sh --results "$VALIDATION_TMP/yosys-results"` | exit 0; 54 module PASS rows, plus structural/connection/tied-input/observer gates |
| `(cd protocol-processor && bash scripts/run_suites.sh)` | exit 0; 14,903 checks, zero failing |
| `make -C gptp-processor all` | exit 0; contract, simulation, mutation, lint and documentation targets passed |
| `behave tests/features` | exit 0; 14 features, 316 scenarios, 1,515 steps; zero failed/skipped |

Use a fresh `VALIDATION_TMP` directory. The parent sweep explicitly declares four optional skips: absent tsn-gen AAF/AVTP and gPTP field campaigns and their two freshness checks; they contribute no passing checks. These are unchanged from the #498 run. The earlier builder result still explicitly excludes its existing gate 11 physical-report arm, whose required mf48 report is absent. No physical calibration or silicon result is claimed.

The 38 manager checks and compiler-present builder passed as previously published. Trusted local docs/rtl-fast/elaborate and all five hosted fast contexts passed at this head. Both completed independent reviews publish clean covering ledgers for all five lenses at this head, with no open finding or review in flight.

Next: mark ready and immediately run the trusted serialized remaining rtl-full replica, keeping head and readiness fixed; verify the resulting hosted ready run and final merge preflight. This is validation evidence, not a reviewer verdict or merge authorization.
