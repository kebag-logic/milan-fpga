[R711] NEGATIVE - exact head 66f713267f201d1a00d7f711e04b3a996d804dee

# R711-7: internal cleared-context review of PR #810 (#665 Mark II split, stage S2b), round 28's delta

- Head `66f713267f201d1a00d7f711e04b3a996d804dee`, tree `3f30ac591059d9dd6f77dcbb908e43e6416a30fb` (verified in the clone).
- Delta: `e7e2b744..66f71326`, five commits (`24ea9c04`, `71e905fb`, `5a19b0ca`, `19f16f80`, `66f71326`). The source base is `a68536fa`.
- Authority:
  - the round 28 ruling (#665 issuecomment-6805157674, maintainer-delegated), and the owner decisions it quotes: option D, and option B's tiers (tier 1 20 ms, SRP 90 ms, last queued notice 125 ms, rows held by every source and never by measurement alone);
  - the ruling on round 28 (issuecomment-6813183455), which keeps the merge gate and the bounds and moves the tier rows to #894.

## Verdict

**NEGATIVE.** Two MINOR findings are open. There is no BLOCKER and no MAJOR.

- **F1 (MINOR; Conformance, Tests, Docs).** The new rows-by-every-source model charges an SRP retained retry once a pass. The tree's rule is at most once a centisecond (`srp_mbx.c:1024-1031`). It is also the rule the load gate and section 13 state, and round 25 replaced "once a pass" with it.
  - So 1x1/1if's R4 is overstated: 73.02 ms as built, 57.93 ms by the tree's rule. Its "retained retries 9.00 ms" term is really 1.50 ms.
  - A smaller under-count works the other way: SRP's arrivals are cut by the AECP burst's whole work, which adds about 0.25 ms (58.18 ms).
  - The model also neither counts nor names as excluded three coalesced datapath events.
  - No self-test control can tell the wrong charge from the right one: the flip self-test passes 129 of 129 with either.
  - R4 still misses tier 1 under every correction. This is a wrong model and a wrong published figure, not the R4 miss itself, which is an accepted finding.
- **F2 (MINOR; Tests, Robustness).** The record-commit code is correct. But the one distinction in it that decides whether a recipient gets a notice twice is pinned by no test: REFUSED means the frame before was delivered, LOST means it was not. Two planted defects that make a refusal resume at the previous recipient, which sends it the notice again at the same sequence_id, pass all 124 tests of the AECP suite.

Everything else in the delta is closed at this head:
- all four of my round-6 findings, and the other reviewer's round-6 findings;
- the load gate's pin column and its new control (falsified by four planted gate defects, each refused);
- the portable-C header (objects byte-identical, independently compiled);
- the disclosed deviations.

One RESIDUE and seven suggestions follow.

## Method and scope

- **Context:** AGENTS.md and CONTRIBUTING.md's review rules, the round 28 ruling and the ruling on round 28, then the PR body at this head.
- **Diff and code:** `git diff e7e2b744..66f71326` (31 files), with the code each change depends on: `ctrl_loop.h` and `ctrl_loop.c` (THE DRAIN, as built), `srp_mbx.c`'s retained retry, `plat/mbx_dma.h`, `aecp.c`'s poll, scan and retry, and `aecp_mbx.c`'s completions.
- **Prior findings:** my round-6 findings and the other reviewer's round-6 findings, read only after my own pass over the diff.
- **The author's packet:** `review-evidence/665s2b-r1/author-r28` at archive `ac5d8de2`.
- **Probes:** I ran my own probes only where a claim needed falsifying. Every probe ran on scratch copies. The clone was restored and verified at the end (`receipts/restore.txt`).
- **What I did not run:** no full bank, no Docker, no hosted run, no hardware, and no manager source bank. No manager source bank exists at this head, and I infer none.

### Evidence integrity

- `scripts/verify_index.py` checks the packet's `receipts/INDEX.md`: 666 rows, 0 files missing, 0 unlisted. Output: `receipts/packet-index-verify.txt`.
- **6 rows do not verify.** Their hashes and sizes are short by 8 to 12 bytes. Each of those files now holds `<home>` or `<home-path>` placeholders, so a host-path scrub ran after the index was generated.
  - The files: the two `elaborate-gates-1` `gate_15_1` logs (first run and rerun), `elaborate-gates-0` `gate_15_0`, `docs-gates-1` `gate_25_0`, `docs-gates-2` `gate_25_1`, and the first run's copy under `logs/`.
  - None of the six is an rc file. All 139 workflow rc files read 0.
  - I take this as a publication defect of the packet, not a hidden failure (Suggestion S7).
- The archive commit carries no signature (`git log %G?` is `N`). I treated the index plus the rc files as the packet's integrity claim.

## Findings

### F1 - MINOR - Conformance, Tests, Docs - `tb/verilator/ctrl_service_budget/rows_grade.py:227` (and `:41`, `:199`) - the rows by every source charge an SRP retained retry once a pass, against the tree's rule of once a centisecond, so 1x1/1if's R4 is 73.02 ms where the tree's own rule gives 57.93

**Where.**
- `rows_grade.py:227`: `out['item.retained'] = min(passes, srp_in) * c['item.retained']`.
- The docstring, `:41`: "a retained record one a pass and no more than SRP's records".

**Authority (the tree's own statement of the source).**
- `sw/firmware/ctrl/srp/srp_mbx.c`:
  - `:1024-1026` says "Even then at most one retry a centisecond (tick), so the retries come at THE TICK's rate, not the passes'".
  - `:1030` enforces it (`else if (!m->retry_spent)`).
  - `:86` gives the retry back only in the centisecond consumer (`m->retry_spent = false;`, after `shlan_timer_tick()`).
- The load gate states it as a rate, `load_grade.py:284` (`c['item.retained'] / k['tick_ms']`), and holds it with its control "the retained retry counted once a record".
- Section 13, `docs/design/SPLIT_CONTROL_MEMORY.md`:
  - `:2112` records that round 24's once-a-poll rule ("every pass retried it") was replaced by the retry's own rule (the round 25 ruling, item 1);
  - `:2180` states "SRP's retained retry is bounded by its source, at most once a centisecond".
- Option B: rows are held by every source's arrival bound, and the docstring's own method (`rows_grade.py:7-11`) is that each bound is a contract rate or a protocol timer. The retained retry's bound is THE TICK's rate.

**Re-derivation of R4, R5 and R6 at 1x1/1if.** I did this from `ctrl_loop.h`/`ctrl_loop.c` as built and the stated costs, item by item. Receipts: `receipts/rows-inputs-1x1.txt` and `receipts/rows-variants.txt`; scripts: `scripts/dump_rows_inputs.py` and `scripts/rows_variants.py`.

The inputs:
- contract rates: AECP 16 per 5 ms, SRP 32 per 2 ms, ACMP 16 per 5 ms, ADP 8 per 10 ms, MAAP 8 per 20 ms; TICK every 10 ms;
- THE DRAIN as built (`ctrl_loop.c:254-274`): SRP is served first, up to 12 records while the pass has spent under 1,300 us, and a pass that takes more than 2 of them takes no other channel's;
- the stated pin costs.

At W = 73.02 ms I reproduce every term of the author's figure exactly (sum 73.020 ms):

| Term | Derivation | ms |
|---|---|---:|
| srp | (32 + floor((73.02 − 3.28)/2)) × 250 us | 16.50 |
| others | ACMP 30 × 280, ADP 15 × 105, MAAP 11 × 90 | 10.965 |
| item.retained | min(36 passes, 68 SRP records) × 250 us | **9.00** |
| item.aecp | min(36, 16 + 14 + 16) × 210 us | 7.56 |
| passes | 36 × (25 + 155) us | 6.48 |
| ticks | 8 × (40 + max(125, 430)) us | 3.76 |
| aecp | 16 × 205 us | 3.28 |
| rounds | 12 notices: (85 + 7 × 255) + (85 + 5 × 255) us | 3.23 |
| timers | ADP 11 × 110, ACMP 2 × 185, MAAP 165, AECP 24 × 60 us | 3.185 |
| steps | (floor(73.02/30) + 1) × 975 us | 2.925 |
| item.acmp | 36 × 65 us | 2.34 |
| item.reclaim | min(72, 138) × 25 us | 1.80 |
| builds | max(900, 2 × 405) us | 0.90 |
| item.mrpdu | 2 × 405 us | 0.81 |
| item.walk | min(36, 9) × 20 us | 0.18 |
| gm | 3 × 35 us | 0.105 |

Where the passes count comes from: passes = ceil(16/2) + 8 ticks + 1 + drained 19 = 36, where drained = ceil((16,500 + 3,760 + 3,185)/1,300).

**Is 73.02 right, too high or too low?**

1. **Too high (the error).** `item.retained` is charged once a pass: 36 retries, 9.00 ms. The tree allows one retry per centisecond dispatched, and THE TICK's records in W bound those: floor(W/10) + 1, the model's own `ticks`.
   - With `min(passes, srp_in, ticks)` the fixed point is **R4 57.93 ms**. Its terms become `item.retained` 1.50 ms (6 retries), srp 14.75 ms and passes 31.
   - R5 goes from 37.19 to 34.94 ms (`item.retained` 3.25 to 1.00), and R6 from 32.69 to 28.55 ms.
   - At 8x8/2if, for #894's term table only: R4 goes from 489.97 to 338.86 ms, and its `item.retained` from 63.88 to 12.41 ms.
2. **Too low, by a smaller amount.** `rows_grade.py:199` counts SRP's arrivals over `W − out['aecp']`, that is, W less the whole AECP burst's 3.28 ms.
   - The docstring's method counts each source's arrivals over the whole window. Under THE DRAIN as built, an SRP record that arrives while an earlier AECP record of the burst runs is still taken ahead of the row's record, in the next pass, SRP first.
   - Only the row's own record (205 us) can be excluded. With that, R4 is 73.52 ms as built, and 58.18 ms together with the correction in point 1.
3. **Not counted and not stated.** AVB_INFO_CHANGED, AS_PATH_CHANGED and AMAP_LIVE_WRITE (`mailbox.yaml:1046-1080`, event types 6 to 8) appear neither in `demand()` nor in the docstring's source list.
   - The load gate excludes them in its docstring, "coalesced events with no contract rate" (`load_grade.py:68-70`). That is a reason for a long-window rate, not for a response-time window.
   - For a window, coalescing bounds each source at one an ordinary pass, as `rows_grade` already does for the timer slots and the grandmaster event.
   - `rows_grade` should count them at a stated sink cost, or state the exclusion and its reason. Their cost is not stated today, so I do not quantify it.

**Charged twice?** No term is charged twice in the sense of one piece of work counted under two names. There are two over-counts that are conservative and small; I record them as S4 and S5, not as part of the finding:
- `item.walk` at the tick rate may also be inside `CTRL_LOOP_TICK_US` ("lwSRP's timers and the walks after them", `ctrl_loop.h:224-226`), 0.18 ms;
- the owed-frame items (`item.aecp`, `item.mrpdu`) sit beside costs measured with the send done in place.

**Tests.** No control of the rows anchors an arrival rule to the tree.
- The row controls test the solver's mechanics: a bound a hundredth of a millisecond either side of W, each term left out shortening W, a cost raised lengthening R5, the tier constants.
- With the corrected charge planted, `flip_grade.py --selftest` still prints 129 of 129 refused, and `--check --point 1x1/1if` reports R4 57.93 (`receipts/rows-charge-selftest.txt`, `scripts/rows_charge_selftest.sh`). So the self-test passes with the right charge and with the wrong one.
- The load gate holds this same rule with a control; the rows do not.

**Docs.** The wrong figure and its term are published as the 1x1/1if finding in:
- section 13 (`:2085`: "R4 is 73.02 ms ... the retained retries (9.00 ms)");
- the PR body (Status, Round 28 item 4, the rows table, Known limitations 1);
- the packet's `ROWS-FINDING.md`.

Section 13 also contradicts itself: `:2180` says the retry is "at most once a centisecond".

**Impact.**
- The conclusion holds: 1x1/1if's R4 misses tier 1 under every correction, R5 and R6 fit, and the 1x1/1if flip stays refused.
- But the figure the flip check publishes, and the term table it reports, is not the tree's every-source count. The ruling on round 28 (issuecomment-6813183455) reasons from it: "the retained retries (9.00 ms) are not reordered by tiers".
- By the tree's rule the retained term is 1.50 ms. What tiers leave at 1x1/1if is therefore different from the published table, and #894 is to start "with the model first". A model that over-states one source by a factor of six is the wrong input to that lane.

**Required outcome.**
- The retained retry in `rows_grade.demand` is bounded by the retry's own rule: at most one per centisecond dispatched in W, and no more than SRP's records.
- The docstring's source line says so.
- SRP's arrivals ahead of AECP's last record are counted over the window less only the row's own record, or the reason for the larger exclusion is stated.
- The coalesced datapath events are counted at a stated cost, or their exclusion is stated with its reason.
- A control ties the retained charge to `load_grade.RETRY_RULE` or the tick rate, so that a once-a-pass charge is refused.
- Section 13, the PR body and the finding text restate R4, R5 and R6, and their largest terms, from the corrected model.
- If the manager prefers to carry the model to #894: a public decision that `rows_grade` moves there, with this finding named, and section 13 and the PR body marking 73.02 ms as superseded.

**Verification.**
- `flip_grade.py --check --point 1x1/1if` reports R4 at the corrected figure: 57.93 ms with only the retry corrected, 58.18 ms with the SRP window too, plus whatever the event sources add.
- `flip_grade.py --selftest` counts a new control that refuses `min(passes, srp_in)`.
- `scripts/rows_variants.py` agrees with the head's own output.

### F2 - MINOR - Tests, Robustness - `sw/firmware/ctrl/aecp/aecp.c:639` and `:661`, `sw/firmware/ctrl/test/test_aecp.cpp:1450-1472` and `:2521-2542` - no test can fail for a refusal resumed as a loss, which sends a recipient the notice twice at the same sequence_id

**Where.**
- `fan_out` resumes at the held recipient, and gives back its sequence_id, only for AECP_FAN_LOST (`aecp.c:639`, `:661`, `:667-671`).
- AECP_FAN_REFUSED means the frame before was delivered (`aecp.h:145`). Resuming there would send that recipient a second copy at the sequence_id it already received.
- The code is correct. What decides a duplicate is the one comparison per call that tells LOST from REFUSED.

**Evidence.** The scratch probe `scripts/aecp_fan_probe.py` and `scripts/aecp_fan_probe2.py` plants into a copy and runs the AECP core arm in app mode at two interfaces, with the whole suite (124 tests). Receipts: `receipts/aecp-fan-probe.txt` and `receipts/aecp-fan-probe2.txt`.

| Plant | Effect | Result |
|---|---|---|
| none | | 124 pass |
| `fan-end-refused-taken-as-lost`: `lost = lost \|\| end != AECP_FAN_TAKEN;` | the completion queue full, the last frame delivered, resumed at it: the last recipient sent the notice twice, same sequence_id | **escaped: 124 pass** |
| `refused-mid-fan-after-a-taken-frame-taken-as-lost`: `lost = taken == AECP_FAN_LOST \|\| held_r != NULL;` | the ring full mid-walk, resumed at the recipient before, already delivered | **escaped: 124 pass** |
| `refused-mid-fan-taken-as-lost`: `lost = true;` | as above, also at a walk's first frame | caught only as a crash (signal 11, NULL `held_r`) in an unrelated test, `ALockExpiryIsNotifiedOnceThePlatformAppliedTheRelease` |
| the author's four `notice-lost-*` plants | | each caught by `Core.ANoticeWhoseFrameWasLostSendsItToItsRecipientAgain` |

- `Mailbox.ANoticeWithNoRoomStaysOwed` (`test_aecp.cpp:2521`) is the only test that drives `fan_end` to REFUSED. It checks `notify`, not what each recipient received.
- No test drives a mid-walk refusal after a frame was taken and checks delivery.

**Authority.**
- The ruling's item 2 says a failed move is reported for the record it carried, with a planted defect for each rule. "For the record it carried" excludes reporting a delivered record as lost.
- The brief asks whether a record can be duplicated, and whether the tests prove it cannot.
- IEEE 1722.1-2021 7.5.2 and Milan v1.2 5.4.5.1: each registered controller is sent the notice, under its own sequence_id.

**Impact.**
- A later edit that reads `end != AECP_FAN_TAKEN` for "lost", which is an easy slip beside the line `owed = end != AECP_FAN_TAKEN || owed` just under it, makes a full completion queue deliver the last recipient's notice twice under one sequence_id.
- Every gate would stay green.

**Required outcome.**
- A test in which `fan_end` is REFUSED, and one in which a mid-walk `fan` is REFUSED after a frame was taken. Each asserts that every recipient receives the notice exactly once, in order, with its own sequence_id.
- A named planted defect for each, like the two above.

**Verification.** The two plants above are caught by name in the AECP campaign, and the suite passes at the fix's head.

### RESIDUE

- **RES-1 (PR body).** The text says the R4 finding is "for an issue of its own, the manager's to open" (Round 28, item 4) and "it is for an issue of its own" (Known limitations, 1). That issue now exists: #894, from the ruling on round 28. **Exact fix:** name #894 in both places.

New source comments in the delta show no issue-comment ID, review round, reviewer ID or lane label. The scan over the added `.c`, `.h`, `.cpp`, `.py` and `.sh` lines found 0 (`receipts/comment-rule-scan.txt`). A looser pattern matched only the C identifier `lanes`.

## Round-6 findings and other prior public findings, at this head

| Prior finding (at `e7e2b744`) | At this head | Evidence |
|---|---|---|
| R711-6 F1 = R712-6 F1 (MINOR): the merge gate holds 1x1/1if on the donor column only | **Closed** | See the first table below. |
| R711-6 F2 (MINOR): round 16's margin at 8x8/2if | **Closed by ruling** (round 28, item 3) | Deferred to the 8x8/2if flip under #890. Section 13 cites #890's owner decision of 2026-11-11 (the 0.75 flip ceiling). 1x1/1if keeps the margin: 160,618 cycles, 39,382 under the share (round 28's legs). |
| R711-6 F3 (MINOR): decision D's tier bounds not in force for the flips | **Closed as ruled**; a new defect in the gate is F1 | See the second table below. |
| R711-6 F4 (MINOR): GNU attributes in portable C | **Closed** | See the third table below. |
| R712-6 F2 (MINOR): a move's ERR reported against the wrong record | **Closed** | See the fourth table below. The REFUSED/LOST test gap is new (F2), not a retention. |
| R712-6 F3 (MINOR): the cut's growth attributed to the wrong image | **Closed** | Section 13 now reads "adds 152 B at the pin and 160 B with tsn-c-stack #32 ... (122,936 B in 122,880)". |
| R711-6 RES-1 and R712-6 RESIDUE-1 (comment IDs and round labels) | **Closed** | 0 `issuecomment` or "round N ruling" in `load_grade.py`, `flip_grade.py`, `poll_grade.py`, `poll_items.py`, `selftest_polls.py` and `rows_grade.py`. |
| R711-6 RES-2 (#890 and #891 unnamed) | **Closed** | `answers.py:105` cites #891, and the PR body names #890. RES-1 above is the same pattern for #894. |
| R712-6 RESIDUE-2 (round 26's load block headed "at this head") | **Closed** | The round 26 sections moved to `evidence/ROUND-HISTORIES.md`. The round 27 block is headed "at round 27's head `e7e2b744`". |
| R712-6 S5 (a sweep suite rewrites tracked files) | Still observed | `gates/sweep/shard-3-tree-after.txt`: `tsn_fuzz` rewrites the date line of two `TEST_RESULTS.md` (the diff is the timestamp only). This PR's lane gates leave their trees clean. Suggestion S6. |

**R711-6 F1 = R712-6 F1: the evidence for "Closed".**

| Check | Evidence |
|---|---|
| Both columns held | `load_grade.py:168` `COLUMNS` holds the pin and the donor column. `findings()` names the column (`:357`). |
| My run | `--check` prints `HELD 1x1/1if at the pin: the load 0.463` and `HELD ... with tsn-c-stack#32: the load 0.450`, rc 0. `--selftest`: 24 of 24 (`receipts/head-load_grade.py_*`). |
| The new control is real | Each of four planted gate defects makes `--selftest` print `ESCAPED a rise at the pin alone`, with 23 of 24: the pin column dropped, the column not named, a planted pin column ignored, the pin column held only at the donor ceiling (`receipts/load-gate-mutants.txt`). |
| My round-6 probe | Now refused by name (author's receipt `gates/lane/probe_r711_1x1_column.log`). |
| Section 13's margin | Names both columns: 0.237 and 0.250. |

**R711-6 F3: the evidence for "Closed as ruled".**

| Check | Evidence |
|---|---|
| The rows held at both points | `flip_grade.py --check` holds them, with controls. `--point 1x1/1if` exits 1 on R4, and I reproduced it (rc 1). |
| What is now wrong | The gate's model and figure are wrong: F1. |

**R711-6 F4: the evidence for "Closed".**

| Check | Evidence |
|---|---|
| Alignment | `aecp.h:50-56` and `:292`: `_Alignas(64)`, and C++ `alignas` for the tests. |
| One platform header | `plat/ctrl_cc.h`. `git grep __attribute__ -- sw/firmware/ctrl ':!*/test/*'` shows only `ctrl_cc.h:31-32`. |
| The portable arm | Plus `Pool.P10` and three plants (author's receipts: each `[ok]`). |
| Byte identity | See below. |

The byte identity has two independent pieces of evidence:
- `scripts/item5_objects.sh` compiles `aecp/aecp.c` and `port/ctrl_pool.c` for RV32IM at `-Os` with the pinned SDK, from `e7e2b744` and from `24ea9c04`. Every allocated section is byte-identical, and the section tables are identical (`receipts/item5-objects.txt`).
- The author's receipt `item5/image-identity.txt` gives three images byte-identical (`5b2317d8...`, `be42e7c9...`, `57b60044...`) and the `control` log identical.

`srp_mbx.c` needs generated headers and I did not compile it. With `CTRL_CC_GNU` = 1, its macro expands to the attribute it replaced.

**R712-6 F2: the evidence for "Closed".**

| Rule | Evidence |
|---|---|
| A record's commit judges only its own move | `mbx.c:515-534`: `TX_MOVED` is set only where the mover started (`:576-577`), and the wait is only for such a record (`:526`). |
| A failed move is reported for its record | `mbx_tx_begin` returns `MBX_STATUS_LOST` (`:547-549`). |
| The fan port reports it | `aecp_mbx.c:20-41`: LOST from the next `fan`, or from `fan_end`, which keeps no completion for a lost last frame. |
| The notice resumes at the lost recipient | `fan_out` resumes at `held` and gives its sequence_id back (`aecp.c:667-672`). |
| The contract is stated | `mbx.h:189-198`. |
| Tests | Driver T2 (extended), T4 and T5. AECP `Core.ANoticeWhoseFrameWasLostSendsItToItsRecipientAgain`. |
| Plants | Nine plants, each `[ok]` in the author's campaign receipts. I re-ran the four AECP plants myself, and each was caught by its test. |

## The brief's checks

**(2) Record commit: lost, duplicated, reordered, wrong status.**
- **Lost:** no. A failed move leaves TX_HEAD and `tx_seq` unadvanced (`mbx.c:528-533`), so the ring never exposes a partial record. The resume writes the next record over the same head.
- **Duplicated:** not by the code. A LOST frame was never committed, so its re-send is the first delivery. The tests do not prove the REFUSED case (F2).
- **Reordered:** no. The resume restarts at the earliest uncommitted recipient (`held`, the last TAKEN), before the one whose call reported it.
- **Status:** LOST only from `mbx_tx_begin`'s commit of the record before; `mbx_tx_send` can return it only if a begin is pending on that channel, and `fan_out` always ends with `fan_end`'s commit.
- **sequence_id:** the frame never reached the wire, so giving its sequence_id back keeps each controller's sequence without a gap or a reuse (IEEE 1722.1-2021 7.5.2, 9.2.1.1). The brief's "Milan v1.2 7.5.2" reads as Milan v1.2 5.4.5.1, the clause the PR cites.
- Two pre-existing behaviours, now reached through LOST as well as REFUSED, are S1 and S2.

**(3) The load gate.**
- It holds 1x1/1if at the pin, 0.463, and with tsn-c-stack#32, 0.450, each at most 0.70.
- It refuses by column name, and its new control is real (above).
- The 8x8/2if column with tsn-c-stack#32 keeps its committed costs: see (6).

**(4) The rows.** F1. 73.02 ms is too high: 57.93 ms by the tree's retained-retry rule. It is too low by about 0.25 ms on SRP's window. It misses three coalesced sources, which are neither counted nor stated. No term is charged twice beyond S4 and S5. R4 misses tier 1 either way, and R5 and R6 fit either way.

**(5) Portable C.** Closed. Byte identity is verified independently for the two objects that compile standalone, and by the author's three-image receipt.

**(6) The deviations, each honest and hiding no failure.**
- **8x8/2if column with tsn-c-stack#32 not re-measured.**
  - The figures reconcile: 122,776 B + 120 B = 122,896 B, over the 122,880 B granule. 122,328 B + 112 B = 122,440 B for arm A at the pin.
  - That column grades nothing at merge: the merge gate is 1x1/1if, and the 8x8/2if flip check reads the pin.
  - The ruling on round 28 (item 3) orders it re-graded on the composed head.
- **The shared session pool.**
  - It is disclosed.
  - Cycle counts come from cycle-accurate simulation and are not affected by host load.
  - The only wall-clock casualty was `test_soc_timing_cuts`.
- **`elaborate-gates-1` run twice.**
  - The first run's `gate_19.rc` is 92: 7 of 8 passed, 1 timed out at 900 s with its result unknown, 0 failed.
  - The rerun on a fresh clone printed `RESULT: PASS`, 8 of 8, and every step rc 0.
  - Both logs are kept.
- **Fresh rebuilds for the harness regrade.**
  - The reused legs' builds refused reuse (`head-G*.log.rc` = 1, "reused build is stale: tree:firmware changed", the ratchet's commit).
  - The fresh builds (`headS-*`, rc 0) have byte-identical images (objcopy and ELF) and byte-identical sample logs at all six legs.
  - Five build inputs differ (`sim.v`, `libc.a`, `libcompiler_rt.a`, `flash_port.json`, `tree:firmware`). The identical images and the 5.4 MB identical sample logs show the simulation is unchanged.
  - The six regrades print 0 refusals and the stated tallies.

## Suggestions (optional; no verdict effect)

- **S1.** After a walk breaks on a mid-walk REFUSED or LOST, `fan_end` still keeps a completion (`aecp_mbx.c:34-40`) under a cookie no event holds yet, because `sent_frame` did not run.
  - If that completion is not drained before the resumed walk's `sent_frame`, it starts the counter notice's holdoff (`counter_at`) from an earlier departure.
  - This was already so for REFUSED at `e7e2b744`.
  - `aecp.h:144`'s "the last frame delivered and its completion kept" overstates TAKEN in that case.
  - Consider keeping no completion when the walk broke, or stating the case.
- **S2.** Under a persistent mover ERR (an error response on its memory port), a lost notice frame is re-sent every pass with no bound. While the notice is owed, `aecp_ready` refuses AECP's records.
  - Responses already behave this way, since `mbx_tx_send` returns BAD and the response stays owed.
  - The PR changes notices from silently dropped to retried forever under such a fault.
  - Consider a stated bound or give-up, or an issue.
- **S3.** `rows_grade.py:198` assumes two AECP records a pass. A command that changes state leaves `notify` set, and `aecp_ready` (`aecp.c:277-280`) then refuses the second, so the count should be at least the burst. At both points `ceil(16/2) + ticks` is already 16 or more, so nothing moves today.
- **S4.** `drained` assumes each blocking pass ends on THE DRAIN's time limit. A pass that takes 3 or more SRP records and ends on an empty ring spends less. State the assumption, or bound the blocking passes by SRP's records over (cap + 1).
- **S5.** State whether `CTRL_LOOP_TICK_US` already holds the walk after a centisecond. If it does, `item.walk` at the tick rate is counted twice, 0.18 ms at R4.
- **S6.** The lost-frame test's recipients are all on interface 0. A resume across interfaces is not exercised: a held frame on interface 0, reported from interface 1's call. Separately, R712-6 S5's sweep tree-after still applies.
- **S7.** Regenerate the packet's `receipts/INDEX.md` after the host-path scrub, or scrub before indexing. 6 of 666 rows do not verify at the archive.

## Reviewer-owned ledger

| Lens | Status | Examined artifacts (at the head) | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1) | The round 28 ruling, items 1 to 7, against the code: `load_grade.py:84-200, :336-430`; `flip_grade.py`; `rows_grade.py:1-325` re-derived against `ctrl_loop.c:137-299`, `ctrl_loop.h:172-183, :220-258` and `srp_mbx.c:80-90, :1010-1037`; `mbx.c:515-586` and `aecp.c:598-676` against IEEE 1722.1-2021 7.5.2 and 9.2.1.1 and Milan v1.2 5.4.5.1; `plat/ctrl_cc.h` against C11 6.7.5 and 6.5p7 | R711-7 | `66f713267f201d1a00d7f711e04b3a996d804dee` |
| RTL | CLEAN | No `hdl/` or `sw/mailbox` change in the delta (`git diff --stat`). The firmware architecture and interfaces: `mbx.h:38-44, :179-200` (the new `MBX_STATUS_LOST`, appended; no ordered comparison of `mbx_status` anywhere in `sw/firmware/ctrl`); `mbx.c:80-85` (`TX_MOVED` 0x400 above every record's words, `_Static_assert`); `plat/mbx_dma.h:14-20, :55-80` (ERR held to the next accepted start); `aecp_mbx.c:16-41`; THE DRAIN unchanged; the image growth within each ledger but the disclosed 8x8/2if column with tsn-c-stack#32 | R711-7 | `66f713267f201d1a00d7f711e04b3a996d804dee` |
| Robustness | UNCLEAN (F2) | The fault path of a failed move: the first frame of a walk cannot be LOST (the previous walk's `fan_end` always commits); LOST mid-walk and from `fan_end`; REFUSED mid-walk and at `fan_end`; persistent ERR (S2); a stale completion (S1); the reviewer's plants (`receipts/aecp-fan-probe*.txt`) | R711-7 | `66f713267f201d1a00d7f711e04b3a996d804dee` |
| Tests | UNCLEAN (F1, F2) | `test_mbx_dma_driver.cpp:322-407` (T2, T4, T5); `test_aecp.cpp:1419-1472, :2521-2542`; `test_port_loop.cpp` P10; the plant tables (`mbx_dma_mutants.py`, `aecp_fan_mutants.py`, `aecp_retry_mutants.py`, `ctrl_mutants.py`); my AECP probe (6 plants); `load_grade --selftest` with 4 reviewer gate defects; `flip_grade --selftest` with the corrected retained charge (129 of 129, unchanged); the author's campaign receipts | R711-7 | `66f713267f201d1a00d7f711e04b3a996d804dee` |
| Docs | UNCLEAN (F1) | `SPLIT_CONTROL_MEMORY.md` section 13 (`:2085`, `:2112`, `:2138`, `:2160-2180`); `tb/verilator/ctrl_service_budget/README.md`'s rows and load sections; `sw/firmware/ctrl/README.md`, `aecp/README.md`, `plat/README.md`; `mbx.h` and `aecp.h` contract comments; the PR body at the head; the comment-rule scan of the delta (0 new instances) | R711-7 | `66f713267f201d1a00d7f711e04b3a996d804dee` |

## Real limits

- **No full banks.** I ran no full bank, no firmware campaign, no harness leg, no Yosys, no Docker or act, and nothing on hosted CI or hardware.
  - Gate and campaign results other than my probes are the author's published receipts at this head, checked through rc files and spot reads.
  - Physical calibration was NOT RUN, and field skips are not hardware proof.
- **Probe scope.** My AECP probe ran the core arm in app mode at two interfaces, one configuration (`endstation_ax7101_1x1_tdm8`), not the image arm. My object comparison covers `aecp.c` and `ctrl_pool.c` only.
- **F1 is re-derived, not measured.** It uses the stated costs and `rows_grade`'s own structure. The three uncounted event sources have no stated cost, so I do not quantify them.
- **The packet.** Six index rows do not verify (S7), and the archive is unsigned.
- **No manager validation.** There is no manager source bank at this head. The current-dev merge candidate (source base `a68536fa`, live dev `fa6c094b8e196666a8a8865788d5e83b5bbaea09`) is not validated here.

## Pending manager duties

- Validate the current-dev merge candidate (builder and native banks) at the merge turn, and link its receipts.
- Own hosted and act acceptance at the exact head, separating executed jobs from skipped contexts.
- Decide where F1 is fixed: in this lane before merge, or carried into #894 with the restated figures. The ruling on round 28 reasons from the 9.00 ms term, and #894's term table should start from the tree's retry rule.
- Carry RES-1 to the residue checklist.
- Have the packet's index regenerated after the scrub (S7).

## Receipts

Listed in `MANIFEST.sha256`:
- `scripts/`: `verify_index.py`, `dump_rows_inputs.py`, `rows_variants.py`, `rows_charge_selftest.sh`, `aecp_fan_probe.py`, `aecp_fan_probe2.py`, `load_gate_mutants.py`, `item5_objects.sh`;
- `receipts/`: the six head gate runs (`head-*.log` and `.rc`), `packet-index-verify.txt`, `comment-rule-scan.txt`, `rows-inputs-1x1.txt`, `rows-variants.txt`, `rows-charge-selftest.txt`, `aecp-fan-probe.txt`, `aecp-fan-probe2.txt`, `load-gate-mutants.txt`, `item5-objects.txt`, `restore.txt`.

After the probes, the clone is at the exact head with 0 status entries, including ignored files. Every bytecode cache my probes wrote into it was removed. The index equals the head tree with modes (sha256 `cf216656...` both ways), and the five required gitlinks are at their recorded commits (`receipts/restore.txt`).

R711-7 FINISHED
