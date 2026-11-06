[A702d] REVIEW READY

Commit: `3f8caae5eca7e681c3452eacdd818d1033a89f8d` on `665-s5-hooks`, one commit on `26ba56e1`, no rebase, not pushed. PR #844, target `dev-soft-core`.

Changed, by the round 3 ruling issuecomment-6692737899, in `tb/verilator/ctrl_service_hooks/hooks_selftest.py` and its README alone:
1. **Mutants (R784-2 F-1).** The `aging` and `amended` mutants fail on the rule they name, and a new finding-level mutant holds the `LATE` rule. 94 mutants, up from 79.
2. **Grading rules (R783-2 F1).** A check fails on all six source mutants. The narrow boundary is tested at a slack of 6,490 and of 6,489. The held rows' labels are pinned, and `README.md:206` says only what is pinned.
3. **Amended-bounds wording (R783-2 F2 = R784-2 F-2).** R783-2's sentence is in the README and the PR body. No hook's verdict changes; per descriptor, four 8x8 rows move inside the 60 ms ceiling. That is the whole difference between the two readings.

No figure or verdict changed. `run.py`, `hooks.py`, `hooks_build.py` and `hooks_soc.py` equal `26ba56e1`, so run.py's graded output is unchanged and the 732-path measurement was not rerun. No RTL or firmware file changed.

**One finding beyond the reviews.** The audit found a third mutant of F-1's class that neither review named: `supersede: any later group supersedes a refusal` failed the positive control and never reached `only by its own path`. It now reaches that rule, and the old edit stays as `supersede: the table names another group`.

**One departure from a reviewer's shape.** R784-2's D2 reads the column at two interfaces, and that shape does not escape probe C, because the table's `NO` pin is a third assertion that catches it. I kept that pin, since loosening it would weaken a test. The mutant reads the column at one interface, where only SRP's verdict moves, and it escapes as required. D2 itself still fails on `the amended bounds graded a path`.

Validation, at `3f8caae5`, on clean clones, all rc 0 unless stated:
- `python3 -B tb/verilator/ctrl_service_hooks/run.py --self-test`, and `hooks_selftest.py` directly: 28 of 28 checks, 94 of 94 mutants.
- R784-2's `rule_probes.py`, unedited: A 94 of 94. B, the arm rule deleted: the aging mutant escapes. C, both grades-nothing assertions deleted: both amended mutants escape.
- R783-2's `source_mutants.py`, unedited: the six are killed, each on its own assertion, with the labels and `hp-margin-round`; 48 of 58, up from 37. The 10 survivors are the ones R783-2 lists as suggestions or no defect, and the README claims none of them.
- The audit of all 94: each fails by an assertion on the rule it names. It records the assertion each fires. Run on a clean clone of `26ba56e1` it flags exactly those three mutants, rc 1, the required result for that control.
- The other probes of both packets: `amended_audit.py` and `amended_table.py` list exactly the four rows the sentence names; all four published `table.md` re-render byte for byte; `verdict_independence.py`, `doc_checks.py`, `doc_figures.py` and `comment_scan.py` agree, with all 94 mutants in the README.
- The docs gates: 0 of 98 nonzero or left the tree dirty, among them `git diff --check` and `cd tests && behave` (1977 steps passed).
- Privacy: `push-privacy-check.py`, 0 private lines over `5b5f4336..HEAD`; the PR body and this comment pass the same rules and a scan for host paths, account and tool names and attribution, each with a positive control.

Not run again: the four runs, the 16 plants and the no-op control, the firmware self-test, the CPU budget harness, the builder, the boundary gate and the candidate merge. They are outside this round's gate set, and their receipts stand at the heads listed in the PR.

Acceptance criteria:
- Round 3 items 1 to 3: met, as above.
- S5's "each hook within its bound": still not met. It stays open on #665, as ruled, and the PR relates to #665.

Open risks/questions:
- "The rule it names" is a judgement. The audit compares what fires against a table I wrote by reading each mutant beside its check; it is in the receipts for a reviewer to dispute.
- Three deletion chains end in an exception rather than an escape, downstream of the deleted rule. Each one's first assertion is its rule.
- For the maintainer, unchanged: the column's scope, and the one-path or per-descriptor decision.
