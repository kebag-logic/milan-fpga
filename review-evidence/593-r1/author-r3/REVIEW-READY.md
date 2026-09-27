[A384] REVIEW READY
Commit: 7a051e618677ecd907ed04b086afbdfe374b4336 (local branch 593-mr-tu-soak; not pushed).

Round 3 implements the two-sided tu model: 2R < 0.25 s, with equality NOT RUN; the upper check admits no true hold beyond 0.5 s + R. I3e/I3f/I3g are NOT RUN; I3h is FAIL. GM-history boundaries, record validation, assertion text and resolution metadata are mutation-pinned. REQ-VER-06, TESTING 6d and the Outgoing mr row cite #602's ruling and explain the current-image failure until its RTL fix lands. Reset wording is reconciled.

Validation at this committed head, all foreground and unpiped:
- `python3 -B tb/tools/torture_campaign.py --self-test`: rc 0, 78 tests.
- `python3 -B tb/tools/torture_release_mutants.py`: rc 0, 132 killed, including all 25 retained from PR #586.
- Plan feature and torture tier: rc 0, 87 and 232 scenarios respectively.
- `python3 scripts/ci_scope.py --selftest`, `python3 scripts/check_baremetal_only.py --check` and `--selftest`: rc 0.
- All assigned documentation, source-fact, style and whitespace gates: rc 0; all 35 required commands pass.
- Unchanged review inputs under the round-3 ruling: internal 41/41, external 59/59. Re-anchored review controls: 103 named kills, one disclosed crash-only control, zero surviving verdict mutations; the verdict-preserving replacement is killed.

Acceptance criteria: all assigned round-3 desk items met. HANDOFF.md contains per-item file:line evidence, original-probe limitations, mutation dispositions and the complete gate table; PR-BODY.md retains its first line and Closes #593 and adds Round 3.
Open risks/questions: independent re-review remains required. #602's RTL correction and physical release qualification remain separate. No firmware, RTL or builder changes.
