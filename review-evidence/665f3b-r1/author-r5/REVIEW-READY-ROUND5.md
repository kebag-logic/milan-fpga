[A612] REVIEW READY - F3b round 5

Commit: `7032bca5a51d8d97fcb73d7fc106ca4af21de38e`. It merges dev `fa7347fc59173f90e4feec2df207692e6e6e72ec` into `6b4feeca5d2fab0ec35cf071322cc775a5b15cb5` with a merge commit: no rebase, no amend, no push.

Changed: nothing of its own. The merge tree is `f1c1f47cb4fefb8a6c68418d03dc762f72cbee15`, as the assignment requires and as `git merge-tree` predicted. Each path keeps one side's bytes, the gitlinks are the lane's (stack pin `70936b77`), and `git diff fa7347fc HEAD` is exactly the lane's 46 paths. `scripts/ci_scope.py`, `docs/testing/CI_WORKFLOWS.md` and `sw/firmware/ctrl/maap/README.md` changed on both sides and merged without overlap. The prepared PR body states the tree.

Validation at the merge commit, with CPython 3.12.3, all rc 0:
- `python3 scripts/act_ci.py --selftest`: PASS, 570 arms. The flat isolated install the docs job runs (`python3 -I <install>/act_ci.py --selftest --worktree <checkout>`): PASS. The runner is byte-identical to dev's.
- `python3 scripts/ci_scope.py --selftest`: PASS, 202 arms, including the #734 scope-history arms and each of the eight gate-read pages refused when filed as documentation only.
- `python3 scripts/ci_events.py --check`: 2174 contract items. `--selftest`: 3096 arms.
- `MAILBOX_SPLIT.md` is still in `GATE_READ_DOCS` after #734's rewrite, which changed only the classifier's self-test. The packet check `round5/mailbox_split_registration.py` finds it once and the classifier prints `true`. Its four planted edits (removed, commented out, misspelled, duplicated) are all refused. On dev's own `ci_scope.py` it returns 1.
- The MAAP differential, where #696's test change meets this lane's adapter and pin: 12/12 checks, 17/17 mutants caught.
- Documentation, em-dash (base `fa7347fc`), doc paths, contents/anchors, bare-metal, hygiene, documentation map, submodule docs, Python/shell/C++ idiom, evidence-reader, RTL and SoC source-list gates, each with its self-test.
- The integrity check covers the parents, the tree, the bytes from each side, the pins, raw blobs and modes, and a clean checkout. Dev changes no firmware image input (6/6 planted inputs flagged). All 30 retained ELF digests still match.

Acceptance: round 5 items 1 to 3 are met. HANDOFF.md (Round 5), PR-BODY.md and the round5 receipts and ledger are in the evidence packet.

Open risks/questions: none. The full firmware campaigns were not rerun locally because no lane or image input changed. The candidate with this tree passed the builder bank, and its full-native bank was still finishing when the assignment was written. The manager owns the push, the `act` replica, exact-head hosted acceptance, review of the merge head and the rest of the merge bar. No hosted or review verdict is claimed.
