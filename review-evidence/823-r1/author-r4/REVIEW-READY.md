[A753d] REVIEW READY
Commit: `30ca4b216e6f7dd386e1d0a0015b0b23b4e08c14` on `823-nvm-format`, for PR #863 to `dev-soft-core`. It is not pushed: this round may not push.
It merges `dev-soft-core` `1d6bf555` (merge commit `3bcf0cdd`, tree `a643419a`, the tree both reviews examined), then adds 5 commits. The remote `dev-soft-core` was still at `1d6bf555` when this was posted.

Changed, by item of the round 4 ruling (issuecomment-6742264763):
1. **Sync.**
   - The format page's drift gate finds each anchor by a token that only one line of its file carries. The page prints file and token, never a line number.
   - The page's prose cites by token too. The gate refuses a `path:line` citation and requires every prose anchor.
   - New plants: a token gone, a token on two lines, a line-number citation, a dropped citation. A control that moves every cited line by 300 gives 0 findings.
   - The seven files both sides changed have no semantic conflict. The only conflict was the page's line anchors. There is a table in the PR body.
2. **Step bound.** A latched record's crc16 is counted over `NVM_REC_HDR - 2` header bytes, and `NVM_STEP_BOUND` matches.
   - `service_bound` takes the header size from the reference fixture.
   - The plant `step_bytes_layout2` (the layout 2 `6u`) is caught.
   - The store README gives 280 B at 1x1 and 1,160 at 8x8.
3. **Flash maps.** `journal_klj3` appears in:
   - FASTCONNECT section 5, its table and prose;
   - QSPI_FLASHBOOT;
   - the `milan_soc.py` slot comment;
   - the diagram regenerated from `FLASHBOOT_RESERVED`.
4. **Tests, each with its plant:**
   - `legacy_other_format_not_recorded`, plant `legacy_any_nonblank_header`;
   - `own_refusal_kept_over_legacy`, plant `ver_overrides_own_refusal`;
   - `klj2_journal_at_its_flash_map_address`, with today's slots read from `FLASHBOOT_RESERVED` through the fixture, plant `legacy_b_wrong_place`;
   - `capacity_commit_over_stale`: commits into A, B, then A at capacity, each erase address checked against the flash map, plant `erase_first_block_every_time`.
5. **VERSION.** The page and the generated T16 cell say "not moved, as ruled (#823)".
6. **Residue:**
   - No issue-comment ID, round label or lane label in this change's source comments.
   - Citations by token.
   - KLJ3 wording on the page, in SPLIT_CONTROL_MEMORY, and in `ctrl_memory.RULES`, whose text that page's rule table is read against.
   - The PR body cites the VERSION ruling.
7. **Width asserts.** `nvm_shape.h` refuses a map entry count past its table: 256 for an input port, 65,536 for an output port.
   - `test_ctrl_nvm.py` requires both refusals in their words.
   - The controls `mapin_width_assert_removed` and `mapout_width_assert_removed` are caught.
   - Only the doctored DR3b build compiles without the input check (`NVM_DOCTORED_MAPIN`), so the run-time check behind it stays tested and covered.

Validation: every run is on a fresh clean clone of `30ca4b21`. Receipts are in the round's receipts directory (SUMMARY.md, and INDEX.md generated from the files present).
- Every `run:` step of `rtl-fast` (with `split-cdc`), `elaborate`, `rtl` (as for a ready PR) and `docs`: 152 ran, all rc 0. 198 did not run, each with a stated reason. `verify_wf` reports 0 bad.
- The full sweep as four shard units, four CPUs each, the `capture_coherence` shard included: 65 of 65 suites PASS, 0 timeouts, 2,192,899 checks, 0 in-suite failures. Every preflight passed, suite cancellation included.
- The builder bank, `docs` legs (`--require-rv32`) and `elaborate` legs (`--require-elaboration`): 107 gates exactly once in each union, rc 0.
- `test_ctrl_nvm.py --require-rv32 --self-test`: `OK across 5 shape(s), 506 tests, and all 130 planted defects reddened`.
- The drift gate, in the docs workflow's NVM record-space step and on its own: `0 finding(s)`. Its self-test: PASS.
- LiteX simulations 8 of 8; the saved-state writer gate `OK across 5 shape(s)`; `git diff --check 1d6bf555 HEAD` rc 0.
- The two-placement simulation of `1d6bf555`, which compiles this store: `twin: 0 finding(s)`, and `twin-plants` refuses all 20 plants.
- A first full run on `8c66ab1e` failed one LiteX simulation, `test_ctrl_memory`: the memory plan's rule table said KLJ3 and `ctrl_memory.RULES` still said KLJ2. Commit `30ca4b21` fixes the rule text, and everything above was run again on it. The failing log is kept.

Acceptance criteria (the ruling's "done means"), on a clean clone of the merged head:
- Every `run:` step of the `dev-soft-core` workflows: met.
- The full sweep as four shard units: met.
- The builder bank: met.
- `test_ctrl_nvm.py --require-rv32 --self-test`: met.
- The page's drift gate: met.

Open risks/questions:
- Hosted CI has not run on this head, which is not pushed; the evidence above is local.
- The append-only save path is round 5, as ruled.
- `flash_layout.png` is rendered from the regenerated SVG at 1,800 px wide. This host's renderer does not reproduce the base PNG byte for byte, so its pixels are this renderer's.
- Found, not changed here: QSPI_FLASHBOOT's following sentences still say nothing writes or reads the `journal` slots today. The shipping all-fabric firmware has a KLJ2 writer (`milan_baremetal.c`).
- FASTCONNECT section 5.1's citation table gives `milan_soc.py` lines from an older head. Both items predate this lane.
