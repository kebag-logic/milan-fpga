[A278] REVIEW READY

Commit: `0c61d458941088f3847513b7c6fe6589c75b4270` (local, unpushed).

Changed: corrected the receiver comment and timing document to cite IEEE 802.1AS Annex B.1.1 for the assumed +/-100 ppm LocalClock bound, and Milan v1.2 section 7.4 for the better-than +/-50 ppm media-source requirement, with 100 ppm retained as conservative margin. The replacement PR body agrees. U13 now requires trim response after validity returns; the default campaign kills `servo_never_resumes` through `[U13] valid offset resumes PI trim`. The evidence-reader disposition names both receiver and servo reads.

Validation: all final command results are rc 0:

- `make -C tb/verilator/crf_rx`: 13,836 unit, 1,658 discontinuity, 69 connected checks; eight campaign controls, including the new mutant.
- `make -C tb/verilator/mmcm_servo`: 85 unit, eight rails, 113 PHC-step checks.
- `python3 scripts/docs_check.py`, both git and no-git CI modes.
- `python3 scripts/check_em_dash.py --base 57456af96b3127b9d309a995bbbd35a6113ce52d`.
- `python3 scripts/check_doc_style.py`; `python3 scripts/gen_toc.py --check`; `python3 scripts/check_doc_paths.py`.
- `python3 docs/traceability/gen_module_matrix.py --check`.
- `python3 scripts/xvlog_gate.py --check`: actual analysis, zero parent HDL findings; four existing pinned-processor findings match the ratchet.
- `python3 scripts/check_cpp_idiom.py`; `python3 scripts/check_py_idiom.py`.
- `python3 scripts/measure_test_evidence.py`, also with `--check`.
- `git diff --check`, also over `d04a61678c9fc710df9bc2cad5e1bcb9d8925ae1..HEAD`.

Simulation and source checks passed at `28b6bfd38300afd9b66c2e7893c30f6141521a38`. The final commit only shortens two timing-document sentences after the style gate flagged their length. All documentation checks were rerun at the final head. An exhaustive changed-path check proves every other tracked file, mode and dependency pin unchanged since the measured ancestor.

Final-head proof: comment-free content is identical to the assigned starting head across all 72 tracked HDL files under `hdl/`. The servo is byte-identical. Both revisions elaborate `RATE_DRIFT_NS_C` to 601 and `TS_JUMP_NS_C` to 2048 ns.

Assigned round-3 items are addressed. `HANDOFF.md`, full replacement `PR-BODY.md`, command receipts and reproduction scripts are prepared in the assigned output directory. No push, PR edit, merge or hardware action was performed. Independent re-review and publication remain pending.
