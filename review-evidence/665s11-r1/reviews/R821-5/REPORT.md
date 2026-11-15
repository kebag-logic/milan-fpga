[R821] NEGATIVE - exact head d3566d44dcae75069f56d97402a5f1b351743008

# R821-5: internal cleared-context delta review of PR #881 (issue #871, S11 AECP REBOOT), round 5

- **Head:** `d3566d44dcae75069f56d97402a5f1b351743008`, tree `32693acb2b16ca8dc329fd20fcbc6b92f2b45db3`. The live PR head equals it; the PR is not a draft; base `dev-soft-core` (`659d7687`).
- **Delta:** `049f0e4d..d3566d44`, 16 first-parent commits.
  - The merge `6cfdf650` of #902's review head `41ca9f87`.
  - 15 lane commits after it.
  - #902's own code was not reviewed. Only this lane's conflict resolution and its consequences were.
- **Assignment:** maintainer ruling #665 issuecomment-6894152131, item 1:
  - #881 joins the flip train;
  - REBOOT's record is measured, accepted and refused, as an ordinary record;
  - the survey covers every stated table over every 1x1/1if leg, then the pace, slice and bound rules;
  - STOP on the last queued notice over 140 ms, any other 1x1/1if row over its bound, the load over 0.70, or REBOOT's record over the ordinary class.
- **Verdict: NEGATIVE, on one MINOR (F1, Tests and Docs).** The restatement moved SRP's record cost, and the polls gate's retained-retry statement derived from it, to 285 us in the load gate. The polls gate itself, `poll_grade.py`, still states 280 us, and its docstring and the design doc's table still say it is "stated at the SRP record's cost".
  - The fix is one figure plus its two statements.
  - It changes no row, load or measurement verdict: the row model already charges `max(item.retained, record.srp)` = 285.
  - It is a figure in a code table that contradicts its own stated derivation and the PR's "a retained retry 285 us", so it is not wording only.
- **Everything else the assignment names checks out at this head.** Three RESIDUE items and two SUGGESTIONs are listed for the author's single pass.
- **No STOP condition holds.** I reproduced each one at the exact head, on a tree extracted from the commit.

## Inputs, in order

1. AGENTS.md, used as the lens and authority map. CONTRIBUTING.md and docs/README were used only for gate and authority references.
2. Issue #871: the body's frozen acceptance items 1 to 5 and its measurements.
3. The assignment and its authorities:
   - the maintainer ruling #665 issuecomment-6894152131, item 1, read in full;
   - the owner's ROM decision #665 issuecomment-6892332745;
   - the REVIEW READY #871 issuecomment-6899968849.
4. The code delta, read before any prior review:
   - the merge resolution (`git show --remerge-diff 6cfdf650`);
   - `6cfdf650..d3566d44` in full for firmware, tests, harness, LiteX and ledger;
   - the docs by word diff.
5. Executable evidence: the author packet `review-evidence/665s11-r1/author-r5` at `f2e8fa9f`, which I hash-verified and read by section.
6. Hosted check runs at the exact head, read only.
7. Prior public findings (R821-4 issuecomment-6811057292, R822-4 issuecomment-6810823985). I read these only after my own pass, to resolve or retain them.

## What I executed (receipts under `receipts/`, scripts under `scripts/`)

All probes ran on a tree extracted from `d3566d44` under `scratch/`, with the tsn-c-stack and lwSRP submodules copied in at their gitlinks. The review clone was only read.

| Run | Result | Receipt |
|---|---|---|
| Packet manifest: every `author-r5/` entry of `MANIFEST.json` hashed (`scripts/verify_manifest.py`) | 1166 entries, 1166 present, 0 mismatched, 0 missing, 0 unlisted. The archive commit `f2e8fa9f` carries no cryptographic signature (`%G?` = N); integrity is the manifest's | `manifest-author-r5.txt`, `.rc`, `packet-commit-signature.txt` |
| The model gates at the head (`scripts/model_gates.sh`) | `flip_grade.py --check --point 1x1/1if` rc 0, RESULT PASS: last queued notice 134.74 of 135, ACMP 29.22 of 30, txL 48.75 of 49, every row within bound. `load_grade.py --check` rc 0: load 0.520 (0.516 with tsn-c-stack#32), ceiling 0.70. The rules: last 134.74, ruled 135, stated 135; pace 8; no statement off; no control escaped. Self-tests: load 26 of 26, record classes 14 of 14, flip 585 of 585 | `model/*.txt`, `model/*.rc` |
| Re-grade of the author's rebuilt legs with the head's `record_classes.py` | Not possible offline: it needs each leg's built image header (`adp_entity_gen.h`), which the packet does not carry. I relied on the author's `model/record-classes-legs2.txt` (RESULT PASS) and the survey's `compare2` instead | `model/record_classes_legs2_regrade.*` |
| Merge onto live `dev-soft-core` `659d7687` (`git merge-tree --write-tree`, read only) | clean, rc 0. `41ca9f87..659d7687` changes only `docs/design/SPLIT_CONTROL_MEMORY.md` | `merge-tree-dev-soft-core.txt` |
| Consolidated delta checks | Covers: the HDL carry, the CSR pins, the author's CSR diff, the files changed after each carried-gate head, the comment-only run.py change, the step and campaign tallies, the REBOOT simulation self-test, the REBOOT records and the record classes | `delta-checks.txt` |
| F1 evidence | covers `poll_grade.py`, `load_grade.py`, the design doc's row, the co-change history and the survey's lines | `f1-retained.txt` |
| Clone integrity after the probes | Clean: porcelain status empty, `diff-index` and `--cached` rc 0, `write-tree` equals the head tree, all five gitlinks equal their checkouts | `clone-integrity.txt` |

## The assignment's items, checked against code and receipts

### (1) The four merge fixes

**CSR bank.** `milan_soc.py:3309` pins `ctrl_reboot` at `n_locs - 4`:
- The mailbox is at `n_locs - 2`, #902's record mover at `n_locs - 3` (`:3322-3323`) and `ppmem` at `n_locs - 1`, so there is no collision.
- The fixture still checks the mover at `n_locs - 3` (`split_soc.py:384`).
- The author's 1x1 split SoC export against `41ca9f87`'s differs only by the LiteX timestamp and `ctrl_reboot` at `0xf000e000`, bank 28 of 32.
- The firmware takes the address by name (`ctrl_plat_gen.py` MAP_ROWS `ctrl_reboot_req`), so the move needs no firmware change.

**Merge resolution.**
- `aecp_ready` keeps both terms: the queue slot and `reboot == 0` (`aecp.c:282-287`).
- `aecp_tx_complete` keeps the REBOOT's `tx_done` beside #902's awaited list.
- `aecp_config` gains `reboot` after #902's `owed`, `owed_slots` and `queue`. The wire model's positional initializer drops the trailing `false`, which leaves `reboot` zero-initialized, as before.
- The lane's `milan_datapath.sv` change is carried byte-identical: the diff sha256 is the same over `1d6bf555..049f0e4d` and `41ca9f87..HEAD`.

**THE RETRY stops at the REBOOT.** `round_waits` gains `|| a->reboot != 0u` (`aecp.c:969-972`), so `aecp_retry` starts no round and `aecp_retry_aged` reports none after the SUCCESS.
- The core check is `test_aecp.cpp:3090-3091`.
- Its defect is `reboot-retries-after-its-success` (`aecp_reboot_mutants.py`).
- The AECP campaign at `d3566d44` shows `[ok] reboot-retries-after-its-success: Core.RebootIsAnsweredNotifiedAndDueOnlyOnceItsFramesComplete`, with 314 `[ok]` lines and nothing else.
- This matches 7.4.43 and the processor's behaviour: no frame is started after the SUCCESS.

**The four platform boot tests** (`7072343a`, `88b0fcd1`):
- B15 and B17 step after each 10 ms pass (THE STEP).
- B18's ADP ring is full at the boot's first read, then has room for one frame (the driver's cached tail), then is full for the SHUTDOWN's sends and the next poll's from the loop's stop.
- B23's AECP ring is full from the boot.
- The control campaign at `57daf4ff` shows 738 `[ok]` and 0 other, including all 22 `plat-reboot-*` defects. `plat-reboot-departing-owed-ignored` is caught on B18.

**The REBOOT simulation.**
- Its flash device is held to the map's KLJ3 journal span (`sim_main.cpp:105-106`).
- The early-reset plant now fires in the take of every AEM_COMMAND REBOOT, before AECP's handler, for this reason: under #894 a plain response is committed in the record's own turn, so firing after the handler would come after the SUCCESS was handed to send.
- The plant's frame test reads subtype `0xFB` at byte 14, message type 0, and command_type `0x2A` at bytes 36-37. These are the correct offsets for an untagged AECPDU.
- The self-test at `20e08ceb` reports "12 of 12 plants and controls caught", each on its own words, and `ctrl_reboot: PASS`.
- `cb0fc679` changes only comments in `run.py` (0 non-comment lines) and the README, so that receipt holds at the head.

### (2) REBOOT's record

- `reboot_group.py` runs only in the answering-ports arm. `build.py` gives that arm's fixture `.reboot=true`.
- The group sends four refusals on each interface, then the accepted REBOOT last.
- `record_classes.py` holds `aecp-reboot`'s REBOOT records as ordinary. It refuses a pass whose 1x1/1if answering-ports leg lacks an accepted or a refused one, and its three new controls are among the 14 refused.
- At 1x1/1if: SUCCESS 11,467 cycles = 125 us; refusals 9,291 to 10,511 = 100 to 115 us; all within 240.
- At 8x8/2if, reported: 95 to 115 us within 265.
- `record-classes-legs2.txt`: RESULT PASS.

### (3) The restated 1x1/1if costs and the knock-on bound

Each restated cost applies the rule to the survey's dearest measurement (100 cycles = 1 us; plus 5 %; rounded up to 5 us):

| Cost | Dearest measurement | By the rule | Stated |
|---|---|---|---|
| `record.srp` | 26,865 cycles = 268.65 us | 282.1 | 285 |
| `record.aecp` | 22,531 cycles = 225.31 us | 236.6 | 240 |
| `events_none` | 3,627 cycles = 36.27 us | 38.1 | 40 |
| the paced class | 28,750 cycles = 287.50 us | 301.9 | 305 |

- On the survey of the rebuilt image (`survey/compare2/compare-1x1.txt`), the only OVER-raw lines left are #894's class lines: the paced SET_CONFIGURATION and the long notice. `record_classes.py` holds those by class, with RESULT PASS.
- `queued_bound.ruled(134.74)` = 135, which is at most 140. `AECP_QUEUED_MS` (`aecp_mbx.h:71`), `notice_window.RUN_MS` and the notice self-test case follow it.
- Slice 950 us and pace 8 ms: by their rules, reproduced.
- Load 0.520: reproduced.
- One gap remains: the polls gate's derived `retained` was not restated. See F1.

### (4) `ctrl_loop.h`

- The only non-comment change is `CTRL_LOOP_SRP_UNIT_US` 280 to 285 at one interface (`ctrl_loop.h:284`). The other changed line is a comment, 130 to 135 ms.
- The constant is derived: `load_grade.py:266-286` refuses any value other than the load gate's `record.srp`, and `load_grade.py --check` gives rc 0 at the head.

### (5) The #902 defect's anchor (`d3566d44`)

- `owed-round-beside-the-queue` now plants on the same line as the REBOOT term.
- `model/anchor-check-d3566d44.txt`: 314 defects, each with exactly one site.
- The AECP campaign at the head: 314 `[ok]`.

### (6) The full pass and per-gate heads

- `verify-wf.md` has 88 rows at rc 0 (56 at `20e08ceb`, 28 at `57daf4ff`, 4 at `d3566d44`), 167 not run, each with a reason, and 0 bad.
- Files changed after `57daf4ff`: only `ctrl_reboot/run.py`, its README and `aecp_owed_mutants.py`.
- After `20e08ceb`: the run.py and README comments, then `aecp_owed_mutants.py`.
- The only gates that read `aecp_owed_mutants.py` run the AECP campaign, which ran again at `d3566d44`. `test_ctrl_firmware_shards.py` uses defect names only, and those are unchanged.
- The SRP job's pin control runs `aecp_mutants.py --shard 0 1000` but requires its own `edited ...` refusal text (`ctrl_pin.py:944-971`). So a wrong-reason pass on the broken anchor at `57daf4ff` was impossible.
- The REBOOT simulation ran after its last behavioural change.
- The carried receipts are valid for the head.
- Sweep 65 of 65, docs, ledger, `test_ctrl_memory` and `ctrl_hot`: accepted from the author's receipts at their stated heads, none of whose inputs changed later.

### The ROM ledger

- `ctrl_memory.py` and `ctrl_memory_ledger.py` raise the platform's 8x8/2if entry to 60.5, refused at 61.0, with `ctrl_plat` 20,416 B (+128 B at every point). This follows the owner's 2026-11-15 decision and is stated as S14 debt.
- `plat_ledger` at `cb0fc679`: every point PASS (8x8/1if at 56.0, within).
- The decision keeps device fit and timing at every corner as gates. Neither is evidenced by a source-head gate here; see the manager's duties.

## Findings

### F1 MINOR - Tests, Docs - the polls gate still states SRP's retained retry at 280 us at 1x1/1if

- **Where:**
  - `tb/verilator/ctrl_service_budget/poll_grade.py:90`: `STATED_US = {1: dict(..., retained=280, ...)`;
  - its derivation at `poll_grade.py:68-70`: "a retained record's retry is the apply an SRP record's handler makes, stated at the SRP record's cost (280 and 365 us)";
  - `docs/design/SPLIT_CONTROL_MEMORY.md:2238`, the polls table's `retained` row, `280 (250)`.
- **Authority and evidence:**
  - The ruling requires costs restated by rule only, over every stated table.
  - `7653571f` restates SRP's record to 285 and, with it, `load_grade.STATED_US` `item.retained` to 285 in both columns ("a retained record's retry at SRP's record cost, 285").
  - The PR and REVIEW READY say "SRP's record and a retained retry 285 us".
  - `poll_grade.py` is not touched by the lane. Its 8x8 entry, 365, still equals `record.srp`'s 365.
  - The previous restatement of `record.srp` (260 to 280, `5bea2597`) moved `poll_grade`'s `retained` in the same commit.
  - The author's survey prints both statements of the same item side by side: `item.retained ... 285 load_grade.STATED_US` and `item.retained ... 280 poll_grade.STATED_US[1] retained` (`f1-retained.txt`).
- **Impact:**
  - Two stated tables give the same item two costs, and the polls table's documented derivation is now false.
  - The harness's polls gate holds the retained retry and the SRP record's own apply (`poll_grade.RECORD`, `limits[RECORD] = limits['retained']`) at 280, while the row model charges 285 (`rows_grade.costs`: `max(item.retained, record.srp)`).
  - No row, load or measurement verdict changes today: the apply measures 26,363 cycles, 280 by the rule.
  - The next image whose apply measures 281 to 285 by the rule would be refused by a gate whose limit the design no longer states.
- **Required outcome:** one of the following.
  - (a) Restate `poll_grade.STATED_US[1]['retained']` to 285 by its stated rule, and update the docstring's figures and the `SPLIT_CONTROL_MEMORY.md` polls row to `285 (280)`.
  - (b) Publish why the polls' retained is held to the apply's own measurement rather than the SRP record's cost. That means rewriting the docstring and the doc row to that rule, and making the PR's "a retained retry 285" name which table it means.
- **Verification:**
  - `compare_point.py`, or a grep, shows `poll_grade.STATED_US[1] retained` equal to the load gate's `item.retained`, or the published rule.
  - `selftest_polls.py` passes.
  - `flip_grade.py --check --point 1x1/1if` and `load_grade.py --check` stay rc 0 (`scripts/model_gates.sh`).

### RS-1 RESIDUE - Docs - a rewritten source comment carries a bench label

- **Where:** `sw/firmware/ctrl/test/test_plat_boot.cpp:187`: "ADP's TX_TAIL as the driver reads it (B18): ...". The delta rewrote this line; the label was on the older line too.
- **Authority:** the owner's comment rule (2026-10-15).
- **Impact:** wording only.
- **Exact fix:** replace `(B18)` with `(ADepartingTheRingRefusedHoldsTheReset)`.
- **Verification:** `grep -n "(B18)" sw/firmware/ctrl/test/test_plat_boot.cpp` prints nothing new; `check_cpp_idiom.py` rc 0.

### RS-2 RESIDUE - Docs - the REBOOT defects are named as living in `aecp_mutants.py`

- **Where:**
  - `docs/design/REBOOT_RESET.md:315` ("fifteen planted defects in `aecp_mutants.py`");
  - `REBOOT_RESET.md:316`, `test_plat_boot.cpp:76` and `plat_mutants.py:263` ("... `reboot-retries-after-its-success` in `aecp_mutants.py`").
- **Evidence:** since `9447702a` the rows are in `aecp_reboot_mutants.py`, which `aecp_mutants.py` plants (`aecp_mutants.py:18, 873`). The count, fifteen, is correct.
- **Impact:** wording only. A reader searching `aecp_mutants.py` for the defect finds no row.
- **Exact fix:** "in `aecp_reboot_mutants.py`, which `aecp_mutants.py` plants". In the two comments, "in aecp_reboot_mutants.py".
- **Verification:** `docs_check.py` and `check_py_idiom.py` rc 0.

### RS-A (R821-4) = RES-A (R822-4) RESIDUE - Docs - retained

- **Where:** `plat_mutants.py:259-262` still reads "caught on B20's ACMP, MAAP and SRP words. B20's AECP check ...", "on B19's and B23's AECP words". The delta re-wrapped `:262` without removing them.
- **Exact fix:** R821-4 RS-A's text, with `reboot-retries-after-its-success` added to the final defect list.

### SUGGESTIONS

- **S1 (Tests, Robustness):** no core test holds a REBOOT behind an owed-notice queue.
  - `REBOOT_RESET.md` section 8 and `aecp/README.md` now state that the REBOOT "is due only once the owed-notice queue is empty".
  - This holds structurally: `aecp_poll` reaches `reboot = 2` only when `transmit(a, true)` is false, and `notices()` returns true while `owed_count != 0` (`aecp.c:762-766, 952-960`).
  - But `Core.RebootIsAnsweredNotifiedAndDueOnlyOnceItsFramesComplete` runs without the queue configured, and no B test queues a prior notice before the REBOOT.
  - Optional: give the core REBOOT test the owed-queue fixture (`test_aecp.cpp:753`) with an earlier command's notice owed, and check that the reset is not due until that notice and the REBOOT's frames have completed.
- **S2 (Docs):** `rows_tiers.py:81` cites `aecp.c:277-280` for `aecp_ready`, which is at `:282-287` at this head. The citation was already stale at `41ca9f87`, so this is not the lane's change, but the merge moved the lines again. Optional: cite the function by name.

## Prior findings, resolved or retained at this head

| Finding | State at `d3566d44` | Evidence |
|---|---|---|
| R821-4 RS-A / R822-4 RES-A (RESIDUE): bench labels in the `plat_mutants.py` comment | **Retained** | `plat_mutants.py:259-262` (above) |
| R822-4 RES-B (RESIDUE): the "each carry one, ..." comma in REBOOT_RESET section 8 | **Retained** | `REBOOT_RESET.md:316` still reads "...after its SUCCESS: its three layers each carry one, the loop's stop (...)" |
| R822-2 R2 (RESIDUE): when ADP's poll runs | **Retained**, not taken by this round's ruling | `REBOOT_RESET.md` and `plat/README.md` passages unchanged in substance |
| R821-4 S-A / R822-4 S1: B20's AECP line is reached by no pair of defects | **Retained** (optional). The new third layer `reboot-retries-after-its-success` is caught by the core test | as before |
| R821-4 S-B / R822-4 S2: "starts no frame" read as "no new frame" | **Retained** (optional) | wording unchanged |
| R821-4 S-C: "88 failed checks" is the campaign's tally | **Retained** (optional) | |
| R822-4 S3, R821-3 S7 and S8, S-b, R821-2 S1 to S6 | **Retained** (optional); the delta does not take them | |

No prior BLOCKER, MAJOR or MINOR was open at `049f0e4d`.

## Lens results

```text
[R821] PASS Conformance - aecp.c:282-287,952-972; aecp_reboot_mutants.py; reboot_group.py; record_classes.py; load_grade.py:132-186,266-286; queued_bound.py; aecp_mbx.h:71; ctrl_loop.h:284; receipts/model/*; author model/reboot-records.txt, record-classes-legs2.txt, survey/compare2 - REBOOT (7.4.43) starts no frame after its SUCCESS, THE RETRY included; its records are ordinary (125 us accepted, 100-115 refused, of 240); the four restated costs are at or above their measurement by the rule; the last queued notice 134.74 of 135 (at most 140), every 1x1/1if row within bound, load 0.520, slice 950 us, pace 8 ms reproduced at the head; no STOP holds. F1 was considered here and not attributed: every stated cost stays at or above its measurement, and the model charges 285
[R821] PASS RTL - sw/litex/milan_soc.py:3304-3323; tb/verilator/ctrl_service_budget/split_soc.py:375-390; ctrl_plat_gen.py MAP_ROWS; author csr/csr-diff.txt; milan_datapath.sv diff identity (delta-checks.txt) - the reset port's bank n_locs-4 below the record mover's n_locs-3, no collision, the export adds only ctrl_reboot at 0xf000e000; the firmware reads it by name; the lane's HDL is carried byte-identical; no other gateware change in the delta
[R821] PASS Robustness - aecp.c round_waits/aecp_retry/aecp_retry_aged; aecp_ready's merged terms; test_plat_boot.cpp B15/B17/B18/B23 (ring full at boot, room for one, full from the loop's stop); the REBOOT simulation's refused-REBOOT take in the early plant; control campaign 738/738 - REBOOT behind a refused one, a full ring, the cached tail and a pending change are each held; S1 is optional
[R821] UNCLEAN Tests - poll_grade.py:90 - F1 (MINOR): the polls gate's retained retry stated at 280 against its own derivation and the load gate's 285. Otherwise: test_aecp.cpp:3090-3091 and reboot-retries-after-its-success caught; AECP 314/314 at the head; control 738/738; REBOOT simulation 12/12; record classes 14/14, load 26/26, flip 585/585 reproduced
[R821] UNCLEAN Docs - poll_grade.py:68-70, SPLIT_CONTROL_MEMORY.md:2238 - F1 (MINOR), same cause. Otherwise: REBOOT_RESET.md section 8, FR_NFR 3.4.1, SPLIT_CONTROL_MEMORY sections 3, 5 and 13, the AECP, harness and REBOOT simulation READMEs state the head's figures (checked against the receipts); RS-1, RS-2 and the retained RS-A/RES-A/RES-B/R2 are RESIDUE
```

## Reviewer-owned ledger

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `aecp.c`, `aecp_reboot_mutants.py`, `reboot_group.py`, `record_classes.py`, `load_grade.py`, `queued_bound.py`, `aecp_mbx.h`, `ctrl_loop.h`; model gates rerun at the head; the author's REBOOT records, record classes and survey | R821-5 | `d3566d44dcae75069f56d97402a5f1b351743008` |
| RTL | CLEAN | `milan_soc.py:3304-3323`, `split_soc.py:375-390`, `ctrl_plat_gen.py`, the author's CSR diff, the `milan_datapath.sv` carry identity | R821-5 | `d3566d44dcae75069f56d97402a5f1b351743008` |
| Robustness | CLEAN | `aecp.c` (`round_waits`, retry, ready, poll), `test_plat_boot.cpp` B15/B17/B18/B23, `ctrl_reboot/run.py` plant, control campaign receipt | R821-5 | `d3566d44dcae75069f56d97402a5f1b351743008` |
| Tests | UNCLEAN (F1) | `poll_grade.py`, `test_aecp.cpp`, the AECP/control/REBOOT campaign receipts, self-tests rerun | R821-5 | `d3566d44dcae75069f56d97402a5f1b351743008` |
| Docs | UNCLEAN (F1) | `poll_grade.py` docstring, `SPLIT_CONTROL_MEMORY.md`, `REBOOT_RESET.md`, `FR_NFR.md`, READMEs, source comments in the delta, PR body (live equals packet but for the manager's packet link) | R821-5 | `d3566d44dcae75069f56d97402a5f1b351743008` |

## Real limits

- **Measurements.** I re-measured no CPU cycles. Costs, records and rows rest on the author's legs, which I hash-verified and read by section, plus my rerun of the model gates on the head's stated tables. Re-grading the legs with the head's `record_classes.py` needs the built images, which the packet does not carry.
- **Campaigns and simulations.** I ran no firmware campaign, Verilator simulation, LiteX build, sweep or workflow step. Those rest on the author's receipts at their stated heads, which I verified as still valid for this head.
- **Packet integrity.** The packet archive commit is not cryptographically signed. Its integrity is the published manifest's, 1166 of 1166.
- **Hardware.** Physical calibration NOT RUN. Field skips and NOT RUN rows are not hardware proof.
- **Hosted CI.** At the time of review, only `changes` had completed (success). The other contexts were queued or in progress, so no hosted verdict is claimed.
- **Device fit and timing.** Fit and timing at every corner, which the owner's ROM decision keeps as gates, are not evidenced at this source head.

## Pending manager duties

- Hosted and act acceptance of the exact head.
- The current-dev merge candidate (builder and native banks): source base `1d6bf555`, live dev `6b66f66d89cf25d2717687bcc2c3bf617685a99a`. Include `659d7687`'s 31-line `SPLIT_CONTROL_MEMORY.md` change: textually clean against this head, but section 13's figures need a semantic look.
- Device fit and timing of the composed image under the owner's 2026-11-15 decision.
- The #898 sync and its rerun survey: the 1x1/1if margins are 0.25, 0.26 and 0.78 ms.
- Carrying RS-1, RS-2 and the retained residue to the residue checklist.

R821-5 FINISHED
