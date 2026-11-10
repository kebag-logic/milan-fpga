[A753f] TAKEN
Branch: `823-format`, new, at round 4's `30ca4b21`, on `dev-soft-core` `1d6bf555`; the PR will target `dev-soft-core`. Commits are added only: no push, PR, merge, rebase, force or amend. Branch `823-nvm-format` (#876, PR #863) is not touched.
Authoritative references: the round 6 ruling (PR #863 issuecomment-6767385787); items 2 to 5 of the round 5 ruling (issuecomment-6754858510); R805-5 RS-d (issuecomment-6766982225) and R806-5 R2 (issuecomment-6767224297); `docs/design/SAVED_STATE_FORMAT_32X32.md`; FASTCONNECT section 5.
Interpreted scope: the saved-state format only, with nothing of the save path.
- N1: SPLIT_CONTROL_MEMORY reports what the `c20ed894` run printed, 3,344 against 13,264 bytes.
- N2: QSPI_FLASHBOOT agrees with FASTCONNECT section 5: the all-fabric writer owns `journal`, and the split store reads its two headers and never writes it.
- RS5 and RS6 (FASTCONNECT's contents entry and status row name `journal_klj3`); RS-a, RS-b and RS-d (comment wording); R2 (the 95.29 ms room is the all-fabric row's, conservative for the split).
- S-a (`LINE_CITE_RE` widened, with plants), S-b (the codec compiles at 255 input entries) and S-c (`#error` for the doctored input build outside the host test), each re-authored on this branch, not cherry-picked.
- The format page and the PR body say section 4 (the save path) is designed here and built under #876.
- #818's route is waived while the head changes no HDL, gitlink or generated SoC RTL: the diff against `dev-soft-core` `1d6bf555` is shown empty, and the memory table at `30ca4b21` is the area evidence (57.5 RAMB36 at the ledgered point).
Validation plan: on a clean clone of the head, every `run:` step of the workflows a `pull_request` to `dev-soft-core` triggers, with a reason for each step not run; the full sweep as four shard units; `test_builder.py --require-rv32`; `test_ctrl_nvm.py --require-rv32 --self-test`; the LiteX simulations; the saved-state writer gate; the page's drift gate and its self-test; `git diff --check` against the merge base. A gate whose inputs this change does not touch is not re-run, and its round 4 result is cited with the reason. No Vivado.
Blockers: none to start. STOP if an accepted item cannot be built without the save path, naming the line.
