[A393] REVIEW READY
Commit: `3b5603e3d16a164c35329efeb633800fe4fe9f95`
Branch: `395-timing-grade`, base `8bc97021f28fb7f729418d3a00851c84ea0b50fd`.

Changed: both round-2 bare-metal gate blockers and every accepted round-3 suggestion. The crossing wording preserves its meaning; the record distinguishes MultiReg D endpoints from AsyncResetSynchronizer PRE endpoints and leaves reset-assertion policy with #607. The standalone entry runs the PLL control. The older margin wording now states WNS >= +0.03 ns and WHS >= 0 at every corner, with manual seed selection and no automatic enforcement. The record links the published crossing receipts and is listed in the findings index.

Validation at this committed head: all 21 accepted foreground commands returned rc 0, with explicit timeouts and no pipelines.
- Full builder: `python3 -B sw/builder/test_builder.py --require-rv32 --require-elaboration`, 767.40 s.
- Compiler-absent full builder: `python3 -B <packet>/run_builder_absent.py`, 601.01 s; hides exactly the three RV32 compiler candidates and retains `--require-elaboration`.
- `python3 -B scripts/check_baremetal_only.py --check`: zero findings across 919 tracked first-party files; `--selftest`: 700 arms pass. The gate and patterns are unchanged.
- CI scope self-test; documentation, cited-path, contents, added-line punctuation, feature-status, documentation-style, solution-documentation and Python-idiom gates/self-tests; committed and worktree whitespace checks: rc 0. Exact commands, log hashes and timings are in `gate-results.json` and `HANDOFF.md`.
- The standalone PLL control passes; restoring the literal in memory fails at the expected changed-part assertion.
- Read-only corner reports: rc 0 in 59.27 s with 16 threads. Crossing classification: rc 0 in 55.47 s with 8 threads, reproducing the round-2 reviewer receipt byte for byte. All seven shipping input size/hash pairs remain unchanged.

Both builder modes execute the timing-grade and required-elaboration arms. Both record the unavailable historical Arty calibration report; the absent mode additionally records the expected compiler-dependent stand-down. These skips are not coverage.

Acceptance: assigned round-3 responses for items 1, 2 and 5 are delivered for independent review. Items 3 and 4 remain open. Relates to #395. The recorded timing margins are met for the applied constraints; existing missing constraints and CDC diagnostics remain unwaived, with no timing or constraint fix.

`HANDOFF.md` contains per-item file/line responses and the gate table; local `PR-BODY.md` has the Round 3 section. Worktree clean. No push, PR edit, merge, hardware access or firmware/RTL edit occurred. Independent reviewers remain [R372] and [R373]; hosted and merge acceptance remain pending with the manager.
