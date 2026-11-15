[A776] STOP
Head: `b58a5430`, round 4's sync merge of `894-tiers` `234bc149` (#902 round 13) into `f098f893`. Not pushed.

**The composed platform image at 8x8/2if is over its ledger entry.** `plat_ledger.py --self-test` at `b58a5430` reports:

- `POINT 8x8-if2: rom 131,240 B, sram 114,160 B, 60.5 RAMB36 (platform-8x8-two-interfaces) ... FAIL`;
- `TILES 8x8-if2: 60.5 RAMB36 past the 60 its override ledgers`. `ctrl_plat_image.py` refuses the link.

At `234bc149` the same image is 130,928 B in 131,072 at 60.0 (#902 states 130,920, 152 B spare). GET_AS_PATH's read adds 312 B, as it did in rounds 2 and 3: `aecp_face.o` grows by 340 B (`path()` is 280 B) and the platform's removed stub saves 20 B. That puts the image 168 B past the 60.0 tiles. `plat_ledger` is a lane gate that no hosted job runs.

**No cut in this branch's own code recovers it.** A scratch rewrite of `path()`, never committed, saves 16 B: the same words in the same order through one `gsi()` call site gives 131,224 B, still 60.5.

**Everything else at the composed head is within its cap**, against `234bc149`:

| Image | 1x1/1if | 1x1/2if | 8x8/1if | 8x8/2if |
|---|---|---|---|---|
| fixture | 41.0 | 41.5 (8 B before its next granule) | 54.0 | 59.0, its entry (126,112 B, 864 B before its next granule) |
| platform | 42.5 | 43.5 | 56.0 (1,128 B before its next granule) | over its 60.0 entry (above) |

Every image is +304 to +320 B of `rom`; `sram` is unchanged.

**Otherwise green so far.** The merge keeps both sides' behaviour. Three files conflicted: `SPLIT_CONTROL_MEMORY.md`, `aecp_mutants.py` and `test_aecp.cpp`. In each, both sides' tests, plants and sections are kept, and the face's GSI model serves GET_AS_PATH's kind 2 and records #902's selectors.

The flip check at 1x1/1if passes with #902's figures (txL 48.43 of 49 ms, the last queued notice 127.21 of 130). The load is 0.516 and 0.512. Both idiom ratchets and `docs_check` pass. The gate pass waits for the ruling.

**Options for a ruling** (none taken):
- **(a)** Raise the platform's 8x8/2if entry to 60.5, the cap of the owner's decision of 2026-11-12. The entry's own text says "60.0, capped at 60.5". This would be ROM debt to the hybrid XIP work, and it uses the cap whole. It is a ledger change in `ctrl_memory.py`, and `test_ctrl_memory.py`'s planted control "the platform's entry plans 60.5" moves with it.
- **(b)** A cut of at least 168 B elsewhere in that image. That is a design decision outside this sync.
- **(c)** #898 waits until the hybrid XIP work frees ROM at that point.
