[A723d] TAKEN

Round 2 of the dev `1f29f189` -> dev-soft-core sync, answering the reviews of PR #830 at `9f81df00` (R760-1 POSITIVE, R759-1 NEGATIVE, two MINOR).

Branch: `sync-dev-1f29f189-into-dev-soft-core`, from `9f81df00`. The merge and the existing commits stay as made; new commits only, one per finding.
Authoritative references: the two review rounds on PR #830; rulings on this issue; `tb/verilator/ctrl_split_boot/README.md`; `tb/verilator/ctrl_service_budget/README.md`; `sw/mailbox/census_ports.py`; `sw/mailbox/mailbox.yaml`.
Interpreted scope: (F1) re-measure the split boot's figures at 1x1 and 8x8 on the head against a no-stage control and restate them, correcting the earlier statement that the stage does not reach that SoC. (F2) the 1x1 4 KiB rows under "every backlog window" carry every window's figures, or the heading says which windows they cover, measuring rather than rewording if the data is not published. Then search every other figure the stage could have moved, in every harness README it reaches. Residue: issue-comment IDs in `census_ports.py` and `mailbox.yaml`, cited by issue and requirement only, regenerating through the generator if a digest requires it; the PR body's stale sentence; the other round's residue where its fix is exact.
Validation plan: `gen_mailbox.py --check --crosscheck` and `--selftest`; `publication_census.py --check`; every docs workflow step; both builder legs; `git diff --check` against the merge base; the affected harnesses' suites and whatever attests a changed firmware digest, each named in the handoff. No full native sweep unless RTL or firmware changes.
Blockers: none
