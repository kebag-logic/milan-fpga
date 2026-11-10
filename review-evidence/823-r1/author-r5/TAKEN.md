[A753e] TAKEN
Branch: `823-nvm-format`, at `30ca4b21` (round 4), PR #863 to `dev-soft-core`. The remote `dev-soft-core` is still `1d6bf555`. Commits are added only: no push, PR edit, merge, rebase, force or amend.
Authoritative references: the round 5 ruling (issuecomment-6754858510) on R805-4 (PR #863 issuecomment-6752573647) and R806-4 (issuecomment-6754770706); decisions 3, 4, 5 and 7 of issuecomment-6730773797, scoped to the split by issuecomment-6730985093; the owner's 0.5 s bound (issuecomment-6545924397) and the append-only direction (issuecomment-6545894131); `docs/design/SAVED_STATE_FORMAT_32X32.md` section 4 and test plan rows T7 to T13 and T15; FASTCONNECT sections 5, 6, 7 and 9.4.
Interpreted scope:
- The F1 store's append-only save path (`sw/firmware/ctrl_nvm`), through its own flash port only:
  - a save appends one delta segment to the authoritative slot and never erases;
  - compaction writes a fresh base into the other slot, and authority moves only when that base verifies with a higher sequence;
  - the old slot is erased in the background, one block at a time, and a save during that erase suspends it, programs, then resumes it;
  - boot replays the base, then each delta whose CRC closes, in sequence order, and stops at the first that does not. A torn delta makes the next write a compaction.
  - Each has its host test and its planted defects.
- The split's 150 ms firmware first-dirty window, and `T-NVM-COMMIT-TIMEOUT` 500 ms for an append. The 32x32 TDM8 worst case comes from the model and is graded against 500 ms.
- The suspend latency is graded at the typical 15 us, as the bound's one typical term. The writer times every suspend and reports a slow one. The page states the margin against 95.29 ms.
- N1, N2, RS5, RS6, RS-a, RS-b, SG3 = S-a, SG4 = S-b and S-c, as ruled.
- The format page, its drift gate, the store README and the test plan rows, updated where the save path fixes a figure or a state.
Validation plan: on a clean clone of the head:
- every `run:` step of the workflows a `pull_request` to `dev-soft-core` triggers, with a reason for each step not run;
- the full sweep as four shard units;
- `test_builder.py --require-rv32`;
- `test_ctrl_nvm.py --require-rv32 --self-test`;
- the LiteX simulations;
- the saved-state writer gate across its shapes;
- the drift gate and its self-test;
- `make twin` and `twin-plants`;
- `git diff --check` against the merge base.
Blockers: none to start. Two facts for the record:
- Item 6: #818's gate is a routed Vivado gate, and this round runs no Vivado. The split memory plan is measured without Vivado and reported. The #818 route is recorded as not run, for a ruling.
- If the save path reaches flash through the processor or `KL_nvm_backend`, this round stops and names the line.
