[A753d] TAKEN
Branch: `823-nvm-format`, at `f3e902f2` (round 3), PR #863 to `dev-soft-core`. Commits are added only, plus one merge commit of `dev-soft-core` `1d6bf555`: no push, PR edit, rebase, force or amend.
Authoritative references: the round 4 ruling (issuecomment-6742264763) on R805-1 (PR #863 issuecomment-6742254074) and R806-1 (issuecomment-6741711708); `docs/design/SAVED_STATE_FORMAT_32X32.md`; `docs/design/SAVED_STATE_FASTCONNECT.md` section 5.
Interpreted scope: a sync and fix round, items 1 to 7 of the ruling.
- Merge `1d6bf555` with a merge commit. Make the format page's drift gate green on the merged tree, with each anchor found by a unique token rather than a line number. Check the 7 files both sides changed for semantic conflicts and list them.
- The store's per-step byte bound counts the layout 3 header, with a test that fails on the layout 2 figure.
- `journal_klj3` shown in FASTCONNECT section 5, and in every map generated from `FLASHBOOT_RESERVED`.
- Tests, each with a plant: the `legacy` rule's negative paths and today's slot B address, and the multi-block erase graded on non-blank flash.
- The VERSION wording, "not moved, as ruled (#823)", made through the generator.
- Residue RS1 to RS4.
- Compile-time width asserts on the `MAPIN` and `MAPOUT` entries, each with a plant.
- Out of scope: the append-only save path (round 5).
Validation plan: on a clean clone of the merged head, every `run:` step of the workflows a `pull_request` to `dev-soft-core` triggers, with a reason for each step not run; the full sweep as four shard units; `test_builder.py --require-rv32`; `test_ctrl_nvm.py --require-rv32 --self-test`; the page's drift gate and its self-test; the LiteX simulations; the saved-state writer gate; `git diff --check` against the merge base. No Vivado.
Blockers: none.
