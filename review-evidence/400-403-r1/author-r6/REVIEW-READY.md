[A323] REVIEW READY

Commit: `a07a75de78b19369e228d4ab8403a52f7435fd64` (local head; not pushed).
Merge: dev `220cb5a34507bb79bbf976b031bb55eb05543d6f` merged cleanly in `6d1819220f452ed9dcc086127f3f0695d14642aa`.

Changed: refreshed `tb/verilator/nvm_capture_cpu/measurements.json` for the composed firmware, including all 96 measured rows and binary hashes; updated `SAVED_STATE_SNAPSHOT_OWNERSHIP.md` section 18 and UNRESOLVED 6. No firmware or hold change.

Measurement: both shapes at aligned 50 MHz, ON/OFF, 16 captures per arm; both labelled 100 MHz 8x8 comparison arms, also 16 each. All rows pass their census, byte, ownership, attestation, traffic and timing checks.

| Point | Old maximum ms | New maximum ms |
|---|---|---|
| 1x1, 50 MHz | 6.60642 | 6.60642 |
| 8x8, 50 MHz | 24.30454 | 24.30246 |
| 8x8, 100 MHz, non-contract | 19.79024 | 19.79024 |

The 8x8 contract maximum includes both arms. It is 0.19754 ms below 24.5 ms and gives 2.0163x margin against the 49 ms floor. The STOP condition was not triggered.

Validation: all assigned normal gates returned 0. This includes `python3 scripts/check_nvm_capture.py`; the complete documentation workflow gate set, with every one of the 22 downstream steps executed; both documentation inventory modes; `scripts/ci_events.py --check` and `--selftest`; both full builder modes; declaration checks; firmware self-tests; `make -C tb/verilator/nvm_cosim`, `make -C tb/verilator/csr`, and `make -C tb/verilator/pp_shadow`; bare-metal scope; em-dash against the assigned dev SHA; and `git diff --check`. Co-simulation passed 465 checks and detected 39/39 mutants. Explicit capture input mutations returned their required rejection status; both two-capture simulation controls returned 0 with their named defects detected.

Execution: used installed prerequisites without downloads; the pinned SDK was verified read-only. The workflow-runner self-test ran only inside a disposable network-disabled container. Compiler-absent target checks are intentionally unmeasured and covered separately by the SDK run. The existing historical calibration-report arm remains NOT RUN in both modes.

Round 5 acceptance: met locally; R249-4 F1 is ready for independent re-review. The final worktree is clean. `HANDOFF.md`, `PR-BODY.md`, commands, raw logs, capture counts, row/hash audits and the full gate table are in the assigned handoff directory. No push, PR edit, merge into dev, donor edit or hardware operation was performed. Physical timing/memory ordering, independent re-review and hosted/integration validation remain outstanding.
