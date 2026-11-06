[A702e] REVIEW READY

Commit: `c73be9b93101fde17c5545145b21066f24f7b99b` on `665-s5-hooks`, two commits on `3f8caae5` (`d7cb56ef`, `c73be9b9`), no rebase, not pushed. PR #844, target `dev-soft-core`.

Changed, by the round 4 ruling issuecomment-6694276050, in `tb/verilator/ctrl_service_hooks/hooks_selftest.py` and its README alone:
1. **A case and a mutant.** `check_superseded` has a row of another path, in the named group, on the same interface: both refusals stay. `supersede: a row of another path supersedes a refusal` goes through the rule as written and fails on it. Dropping the path term from `run.py:141` now fails `another path`.
2. **`any later group`.** Renamed to what it does, the ruling's second option: `supersede: every refusal is superseded`.
3. **The rule table, the README row and the PR sentence** match. Round 3's two paragraphs that said this mutant reached its rule are corrected in place.
4. **The remaining rule table, once.** All 96 names read beside each mutant and what it fires, and each of the 58 mutants that wrap a rule's output given a twin, the same defect made in the rule's source: 61 twins, 60 on the mutant's own assertion, 1 on another, none surviving. It found two more names to rename, below, and I stopped there.

96 mutants, up from 94. No figure or verdict changed. `run.py`, `hooks.py`, `hooks_build.py` and `hooks_soc.py` equal `3f8caae5`, so nothing was re-measured. No RTL or firmware file changed.

**Beyond the ruling's list, each needed for its sentence to be true.**
- The old `another path` case could not fail for what it was labelled, as both reviews show. A new label alone would have repeated that, so it is `a path the table does not name` with a row of its own path, and `supersede: the table names a second path` fails on it. 96 rather than 95 is that mutant.
- `bound: the margin is not recorded` records a margin, so it is `bound: the margin is taken from a timeout of zero`. `held missing: its finding is dropped` leaves a generic finding, so it is `held missing: its finding by name is dropped`.

Validation, at `c73be9b9`, on clean clones, all rc 0 unless stated:
- `python3 -B tb/verilator/ctrl_service_hooks/run.py --self-test`, and `hooks_selftest.py` directly: 28 of 28 checks, 96 of 96 mutants.
- R783-3's `source_probe.py`, unedited: `sup-no-path` killed by `another path`, and `sup-second-entry`, which survived, killed by `a path the table does not name`; 43 of 51, up from 41. The other 8 survivors are ones R783-3 lists.
- R783-3's `deletion_probe.py` and R784-3's `r3_probes.py`, unedited: with `another path` deleted the new mutant alone escapes. R784-3's `sup-any-path` is killed by that assertion, and `sup-table-any-path` now by an assertion rather than by a sibling.
- R784-2's `rule_probes.py` and R783-2's `source_mutants.py`, unedited: B and C as before; 48 of 58, the same 10 survivors.
- The audit: 96 of 96 on their own rule, by an assertion. With `another path` deleted on a copy it reports that mutant `ESCAPED`, rc 1, the required result. On `3f8caae5` it flags the three renamed rows, rc 1, also required, though that control fails on any renamed row.
- The twins: rc 0, none surviving. Their control at `3f8caae5` reports the finding's own path term as `TWIN SURVIVES`, rc 1, the required result, so the method would have found this finding.
- The other probes of both rounds: all four `table.md` byte-equal at this head's code, exactly the four known 8x8 rows move, 96 README rows name their mutants, no label in the added lines.
- The docs gates: 0 of 98 nonzero or left the tree dirty, among them `git diff --check` and `cd tests && behave` (1977 steps passed).
- Privacy: `push-privacy-check.py`, 0 private lines over `5b5f4336..HEAD`; the PR body and this comment pass the same rules and a scan for host paths, account and tool names and attribution, each with a positive control.

**Two reviewer scripts do not apply, rc 1.** R783-3's `supersede_fix_check.py` and R784-3's `fix_feasibility.py` patch the pre-fix text this change replaced, so each stops on its own anchor check. Their case is in the tree, and `sup-no-path` and `sup-any-path` show it working.

Not run again: the four runs, the 16 plants and the no-op control, the firmware self-test, the CPU budget harness, the builder, the boundary gate and the candidate merge. They are outside this round's gate set, and their receipts stand at the heads listed in the PR.

Acceptance criteria:
- Round 4 items 1 to 4: met, as above.
- S5's "each hook within its bound": still not met. It stays open on #665, as ruled, and the PR relates to #665.

Open risks/questions:
- "The rule it names" stays a judgement. The row-by-row reading is in the receipts for a reviewer to dispute.
- `buckets: the window opens right after the registrations` is disclosed, not changed. Its name is true, but it fires the wait's length, and no mutant fires the group's own assertion. Its twin fails that assertion, so the rule is held.
- Deleting `other interface` alone lets nothing escape, as `every refusal is superseded` falls through to the next case. The term is held by that assertion directly, with no single-term mutant.
- The group term has no assertion of its own: it is held by `the table names another group` escaping, as both reviews found. I took the rename, so no case varies the group.
- 48 `expect` statements are fired first by no mutant, down from 49. They are not rows of the rule table, so this check did not audit them.
- For the maintainer, unchanged: the column's scope, and the one-path or per-descriptor decision.
