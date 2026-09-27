[A387] REVIEW READY
Commit: `66001a307ce5de57577e66d6e3a18b9f4020764b`
Branch: `395-timing-grade`, base `8bc97021f28fb7f729418d3a00851c84ea0b50fd`.

Changed: #395 items 1, 2 and 5. `sw/litex/platforms/ax7101_timing.py` declares the commercial part/grade/range once. The platform and saved-checkpoint reporter derive their conditions from it; builder tests pin the declaration and refusal paths. BUILDING section 5, RUNNING_TESTS section 5, LITEX_SOC section 7 and `docs/findings/COMMERCIAL_TIMING_395.md` record the corner rule and measured limits.

Validation at this commit, all rc 0:
- Full builder bank with `python3 -B sw/builder/test_builder.py --require-rv32 --require-elaboration` (775.77 s), then the complete entry point with the three RV32 compiler candidates hidden and required elaboration retained (559.57 s).
- `python3 -B scripts/ci_scope.py --selftest`.
- `python3 -B scripts/docs_check.py`, `python3 -B scripts/check_doc_paths.py`, contents, added-line punctuation, feature-status, documentation-style and solution-documentation gates.
- Python idiom gate/self-test, `git diff --check`, and the committed diff against the base.
- Foreground routed-checkpoint analysis with 16 threads (56.89 s), and nine live wrong-condition refusal controls with one thread. Run exit codes and logs retained.

Timing for the nominated `9e9954e9` shipping checkpoint (WNS/TNS/WHS/THS, ns):

| Fixed timing model | Recorded junction endpoint | WNS | TNS | WHS | THS |
|---|---|---:|---:|---:|---:|
| Slow | 0 C and 85 C | 0.123 | 0.000 | 0.101 | 0.000 |
| Fast | 0 C and 85 C | 1.429 | 0.000 | 0.036 | 0.000 |

The junction settings are power metadata; these are two fixed timing models repeated at the endpoints, not four independent timing models. No negative-slack paths were found. Checkpoint SHA-256: `5f7a442b6a9327ad5d41aa0b10e18c84d9ca4c0aacd573d2ad25d444f5b2f5d1`. All six retained shipping inputs remain byte-identical.

Acceptance: items 1, 2 and 5 delivered for independent review. Items 3 and 4 remain open; this work relates to #395 and does not close it.

Open risks/limits: ten Critical CDC diagnostics, two unsafe clock-pair classifications, and 46 input/87 output ports without delay constraints remain visible and unwaived. Both builder modes record gate 11's unavailable historical Arty calibration report; the absent mode additionally records expected compiler-dependent skips. No timing-grade or required-elaboration arm was skipped. No timing fix was made.

Handoff: `HANDOFF.md`, `PR-BODY.md`, gate/report inventories and small report/log copies are in the assigned output directory. Larger reports remain under the physical data path with sizes and SHA-256 hashes recorded. Worktree clean. Independent reviewers: [R372] and [R373].
