[A352] REVIEW READY

Commit: `08374721d958b32ade38e7e62d25a7ccea215119`
Branch: `573-builder-model-refusals` (five round-2 item-group commits, retained locally; no push).

Changed: derive the 46-format cap from the 2021 layout; share the packed u32 bound and refuse listener overflow; correct identity clauses and the stale design-document claim; implement all five accepted suggestions. Every assigned boundary has an independent declaration control, including actual packed buffer equality and direct CRF-output behavior.

Validation: both complete builder modes rc 0 (756 s with RV32, 550 s with the three RV32 candidates hidden); declaration suite, descriptor audit, store self-test, RTL lint, Python idiom, naming, both docs inventory modes, em-dash against `e0920d77`, style, contents, anchors, paths and whitespace gates rc 0. The absent run records its intended compiled-instrument skip; both runs record the unavailable utilization-calibration report. No hardware validation is claimed.

Acceptance: all five tracked configurations remain accepted, including all three Arty configurations; STOP did not trigger. All 85 generated artifacts match `e0920d77162284d8da52ffaf13a973e451e44f90` in size and SHA256, with the second unchanged artifact script independently matching 80/80. Unchanged mutation runners detect 30/30 and 26/26 applicable original mutations; eight round-2 mutations are detected. Restored controls pass and sources are restored exactly.

Open validation exception: the unchanged `format_cap_length.py` prints the accepted 46-format / 506-byte boundary, then exits 1 on the required named refusal of 47. Its lack of a refusal handler makes the requested all-zero raw-script condition incompatible with the required fix. This rc 1 is preserved, not relabeled. The separate evidence check returns 0 after verifying that exact rejection. Original patterns R-M8/R-M14 target the removed literal cap and report not applied; the new cap-plus-one mutation is killed. All other unchanged reviewer probe and mutation runners return 0.

`HANDOFF.md` contains file:line changes, finding dispositions, every mutation, both artifact inventories, exact commands and the gate table. `PR-BODY.md` is the complete replacement body with Round 2. The assigned evidence packet is ready for coordinator publication. The worktree and index are clean, submodule revisions/bytes are unchanged, and all five commits have one-line subjects without bodies or trailers. Independent re-review of all five lenses remains required; no author review approval is claimed. No PR edit or merge was performed.
