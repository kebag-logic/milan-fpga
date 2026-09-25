[A294] REVIEW READY

Commit: `f5532c4c3f94a516b748cc4627dc5f78d05fa73e` (local; not pushed).
Parents: `0c61d458941088f3847513b7c6fe6589c75b4270` and `c266432dcb0cdd464205823a3d82cad260eedde2`.
Message: `Merge dev into 546-crf-talker-step`.

Changed: fetched dev and merged the assigned commit. The only manual resolution is `docs/design/GM_LOSS_RECOVERY.md`: retain the landed render, `mr`, MEDIA_RESET and pending-restart rows; retain the receiver isolation/refill wording and both `crf_rx` rows; keep the gmstep row's three negative controls. The five assigned automatic overlaps agree with both parents. No other manual content change was made. All three required submodules were updated to the merged gitlinks.

Validation at this head (foreground, no pipelines):

| Command | Result |
|---|---|
| `make -C tb/verilator/crf_rx` | exit 0 |
| `make -C tb/verilator/mmcm_servo` | exit 0 |
| `python3 scripts/measure_test_evidence.py --check` | exit 0 |
| `python3 scripts/measure_test_evidence.py --selftest` | exit 0 |
| `python3 scripts/docs_check.py` (Git inventory) | exit 0 |
| `python3 scripts/docs_check.py` (tracked export without Git) | exit 0 |
| `python3 scripts/check_em_dash.py --base c266432dcb0cdd464205823a3d82cad260eedde2` | exit 0 |
| `python3 scripts/check_doc_style.py` | exit 0 |
| `python3 scripts/gen_toc.py --check` | exit 0 |
| `python3 scripts/check_doc_paths.py` | exit 0 |
| `python3 docs/traceability/gen_module_matrix.py --check` | exit 0 |
| `python3 scripts/xvlog_gate.py --check` | exit 0 |
| `python3 scripts/check_cpp_idiom.py` | exit 0 |
| `python3 scripts/check_py_idiom.py` | exit 0 |
| `git diff --check` | exit 0 |

Receiver results: 13,836 main checks, 1,658 discontinuity checks, 69 connected checks and 8 mutation controls, all with zero failures. The ignored-validity and PI-never-resumes controls both reached their named U13 rejection. The connected cases retained LOCKED with at most 0.020 ppm integrator movement.

Servo results: 85 unit, 8 rails and 113 PHC-step checks, all with zero failures. The evidence self-test passed 101/101 checks. Both documentation modes reported zero findings; the no-Git mode explicitly skips Git inventory parity. Source analysis reported zero first-party findings and the four existing pinned-processor findings, matching its ratchet.

Acceptance criteria: round-4 assignment items 1-3 met. The final worktree is clean. `HANDOFF.md` records the before/after resolution, overlap check and gate table; `PR-BODY.md` preserves the current description with the round-4 update.

Open risks/questions: none from the assigned checks. Publication and the assigned independent merge-delta review remain pending. No push or PR edit was performed.
