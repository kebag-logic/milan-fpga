[A794] STOP

The flip train's composition (#665 issuecomment-6939460730, -6939574513) stops at step 7, #931 `d06ded5a`: two frozen PRs require opposite behaviour of the product SoC build past 56 RAMB36, and the ruling both cite does not settle which. Nothing is pushed; the branch `flip-train-1117` is local.

**The conflict (#933 `1a1e6665`, step 5, against #931 `d06ded5a`, step 7).** Each added an 8x8 one-interface platform entry, `platform-8x8-one-interface` at 56.5, and a way for `milan_soc.add_ctrl_memory` to plan a ledgered image by its symbols:

| | #933 (#919) | #931 (#923, #924) |
|---|---|---|
| Lookup | `ctrl_memory.product_point`: only entries flagged `product` | `ctrl_memory.own_point`: every `LEDGERED` entry |
| The product build of the platform's 8x8 two-interface image | refused past 56 | planned at its entry, 61.0 |
| The size fixture's image in a product build | refused | planned at 59.5 |
| Its memory test (`test_ctrl_memory.py`) | requires `add_ctrl_memory` to refuse every entry's image but the product one's, and two planted ledgers ("the platform's two-interface entry a product entry", "the size fixture's entry a product entry") to turn the ledger red | requires `add_ctrl_memory` to build and plan each of the three entries' images at its own entry |

No resolution keeps both tests. Both cite [#923's ruling of 2026-11-16](https://github.com/kebag-logic/milan-fpga/issues/923#issuecomment-6906679024): "a new ledgered product entry" for the 8x8/1if image, then "The product SoC build plans a ledgered image at its own entry by its symbols; every unledgered image stays refused past 56." The second sentence reads as #931's; the first names a product entry, which #933 makes a class of its own. The 8x8/1if image is planned at 56.5 either way, and neither split route (1x1/1if, 8x8/1if) is affected. Only a product build of an 8x8 two-interface image differs.

**Decision asked:**
- **(a), recommended:** #931's reading, the ruling's sentence as written. Every ledgered image plans at its own entry in a product build. #933's refusal cases for the non-product entries and its two `product`-flag plants go; the flag goes too, since nothing would read it.
- **(b):** #933's reading. Only a product entry plans in a product build. #931's acceptance cases for the size fixture's and the platform's 8x8 two-interface images become refusals.

Either way both PRs' other behaviour stays; the rest of step 7 is resolved and waits only on this.

**#914 (step 2):** both reviews at the frozen head `8883d499` are NEGATIVE (R843-5, R844-4). R844-4-F1 (MAJOR) raises 8x8/1if's `CTRL_LOOP_TX_MS` past 70 ms, so the 8x8/1if image moves. Its head had not moved at 09:29 CET. As instructed, the composition is rebuilt from step 2 on #914's new head. Every resolution is recorded, so steps 3 to 7 replay.

**Composed so far (local):**

| Step | PR | Merge | Conflicted files | Checks at the merge |
|---|---|---|---|---|
| 1 | #881 `d3e61e37` | `43b954e6` | 18 | docs, idioms, harness self-test, `rows_tiers`, record classes, load gate, flip check at 1x1/1if, ledger test, firmware suites and control campaign: pass |
| 2 | #914 `8883d499` | `136e64ce` | 12 | as step 1, with #914's `shape_costs` and `egress_ledger` self-tests and the AECP and SRP campaigns: pass |
| 3 | #918 `394612c5` | `874bd403`, fix `d7941d4d` | 7 | pass after `d7941d4d` |
| 4 | #935 `37255683` | `d21f7aab` | 2 | pass, firmware suites and SRP campaign too |
| 5 | #933 `1a1e6665` | `89eea108` | 13 | firmware suites pass; light gates and the control campaign running |
| 6 | #938 `81c9a1a0` | not yet in the branch | 5 | resolved, light gates pass in a scratch tree |

- **Fix `d7941d4d`.** Each side left `build.py` at the Python idiom gate's 1,000-line module limit and `grade.parse` at 100 and 98 of its 100 lines; the union broke the ratchet. Three comments are rewrapped and one is moved; words and the AST are unchanged.
- **Step 6 needs the same kind of fix.** #914's `shape` and #938's `journal` give `grade.grade` seven parameters, one past the gate's six. `shape` and `interfaces` fold into one, behaviour unchanged. Two modules go back to 1,000 lines by layout alone.
- **The all-points flip check** fails only on the 8x8/2if rows. These are the base `cb96336d`'s same eleven findings, reported, not held, by the owner's decision of 2026-11-12.
- **The tier model at the composed tree through step 7** (ledger aside) holds every 1x1/1if row. The last queued notice is 137.89 within 140, txL 48.89 within 49 and ACMP 29.91 within 30; the load is 0.522, ceiling 0.70.
- **Not yet run:** the CPU harness measurement, the routes and the final gates. They need step 7 and #914's new head.
