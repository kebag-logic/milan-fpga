[A753c] TAKEN
Branch: `823-nvm-format`, at `61eec0c3` (rounds 1 and 2), from `dev-soft-core` `a9d69c77`; the PR will target `dev-soft-core`. Commits are added only: no push, PR, merge, rebase, force or amend.
Authoritative references: the round 3 ruling (issuecomment-6730985093), which scopes decisions 1, 2 and 6 of issuecomment-6730773797 to the split placement; `docs/design/SAVED_STATE_FORMAT_32X32.md` sections 2, 3 and 5 and its test plan; #823 scope items 1 to 4; the #859 census at `6857012d`, read only; `docs/design/SAVED_STATE_FASTCONNECT.md` sections 4 to 7.
Interpreted scope: the record space and framing for the split placement only.
- One layout 3 declaration (1,129 ids, a 16-bit `record_id` in a 10-byte F07.8 header, NAME ids 222 to 1,128), read by the builder's split output and by the F1 store's codec.
- The split's firmware tables, the Python reference (a KLJ3 codec beside the unchanged KLJ2 one) and its gates.
- KLJ3 in the 640 KiB journal below today's; a KLJ2 container is refused `VD_VER`, the store boots blank and records the reason; today's journal is never written.
- The VERSION step, and the split's open bits as a word array with a count.
- The whole-image commit is unchanged. No processor change. The all-fabric placement, `KL_nvm_backend`, `milan_baremetal.c` and KLJ2 stay as they are, and the builder keeps refusing an all-fabric shape over today's limits, with a gate and a plant.
- The design page is updated: the format is the split's, the all-fabric placement keeps KLJ2, and A3 is graded at the typical 15 µs with its margin. Its drift gate stays green.
Tests, one plant per rule, for the split: NAME first, last and one past; at capacity accepted and one over refused in the builder; a KLJ2 journal at boot refused, blank, reason recorded.
Validation plan: every `run:` step of the four workflows a `pull_request` to `dev-soft-core` triggers, on a clean clone of the head, with a reason for each step not run; the full sweep as four shard units; `test_builder.py --require-rv32`; `test_ctrl_nvm.py --require-rv32 --self-test`; the LiteX simulations; the saved-state writer gate across its shapes; `git diff --check` against the merge base. No Vivado.
Blockers: none to start. If the split's save path reaches flash through the processor or `KL_nvm_backend`, this round stops with the line.
