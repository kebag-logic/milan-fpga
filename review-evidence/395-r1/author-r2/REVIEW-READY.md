[A390] REVIEW READY
Commit: `3a0cb4cf4fed2d71436a43f4b96cb375f9178342`
Branch: `395-timing-grade`, base `8bc97021f28fb7f729418d3a00851c84ea0b50fd`.

Changed: round-2 responses to R372-1 F1/F2/F3 and R373-1 F1/S2. The timing record names rejected crossing constraints, warning/source/log locations, the clock-prefix cause, unbounded Ethernet/sys false paths, measured intended-bound slack and #607. BUILDING retains the critical-warning census. The builder exercises hook-level refusals and report arguments; the PLL speed grade derives from the declared part.

Validation at this head, all rc 0:

- Full builder bank: `python3 -B sw/builder/test_builder.py --require-rv32 --require-elaboration` (771.97 s).
- Full builder bank with exactly the three RV32 compiler candidates hidden and required elaboration retained (565.43 s).
- `python3 -B scripts/ci_scope.py --selftest`.
- `python3 -B scripts/docs_check.py`, `python3 -B scripts/check_doc_paths.py`, contents, punctuation, feature-status, documentation-style and solution-documentation gates; Python idiom gate/self-test; committed and worktree `git diff --check`.
- Foreground checkpoint reports (58.39 s, 16 threads) and crossing diagnostic (41.85 s, 8 threads). All seven shipping input size/hash pairs remain unchanged.
- All five required faults fail with timing-grade assertions through the full builder entry point. The reviewer's 21-fault campaign returns `unexpected=0`; its unmodified control passes. All four hook refusal probes return 1. Restoring the PLL literal fails its changed-part control.

The recorded margin is WNS >= +0.03 ns and WHS >= 0 at every corner. Slow WNS/WHS is +0.123/+0.101 ns; Fast is +1.429/+0.036 ns. Both repeat at 0 and 85 C; TNS/THS are zero. The intended 8 ns crossing bound is met in all four directions at both models, with worst slack +2.560 ns. Clearing all false paths exposes fourteen milan-to-Ethernet endpoints, including reset paths: Slow/Fast worst slack +4.056/+5.878 ns. The review's narrower six-endpoint measurement was +7.066/+7.538 ns; the record distinguishes both.

The shipping log has 14 emitted critical warnings; its fifteenth substring match is echoed source, not another warning. #607 owns the constraint fix. No timing or constraint fix is included. CDC diagnostics and missing I/O delays remain unwaived. Both builder modes record the unavailable historical Arty calibration; the absent mode additionally records expected compiler-dependent stand-downs. No timing-grade or required-elaboration arm was skipped.

Acceptance: items 1, 2 and 5 and the assigned round-2 responses are delivered for independent review. Items 3 and 4 remain open. Relates to #395.

HANDOFF.md and PR-BODY.md are updated in the assigned packet, with per-item file/line responses, crossing and planted-fault tables, exact gate receipts and evidence hashes. Worktree clean. No push, PR edit, merge, hardware access or firmware/RTL edit occurred. Independent reviewers remain [R372] and [R373].
