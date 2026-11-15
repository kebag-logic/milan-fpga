# HANDOFF round 5: lane 897 (A776), the ruled ledger, GET_AS_PATH's record tracked, on #902's round-13 head

Status: **REVIEW READY** (2026-11-15, started 08:05 CET), posted once on #897, issuecomment-6894799910 (`REVIEW-READY-COMMENT.md`). No STOP condition holds.
Assignment: #897 issuecomment-6890824581, the ruling on round 4's STOP (issuecomment-6890794725).
Base: round 4's local merge `b58a5430` (`f098f893` + `894-tiers` `234bc149`). `dev-soft-core` is still `cec88385`.
Final head: `eca1b9ca8d9f0090ebc9b55b1bbb827d20bf7ffd`. Nothing is pushed; the manager pushes.

## 1. The ledger (item 1)

`git cherry-pick 8238156d` (#901, on `origin/895-talker-redeclare`) conflicted in three files. The base lines differ between the trees: #895's tree states `ctrl_plat` at 20,352 B and the entry's reason with SRP's Talker declarations, while this tree states 20,288 B and "(#665 decision D3)". So the cherry-pick was aborted and **the identical text applied** where the two trees agree. The result is `2170b22e`; the per-file receipt is `receipts/ledger/8238156d-vs-2170b22e.txt`.

| File | Against `8238156d` | Why |
|---|---|---|
| `sw/litex/ctrl_memory_ledger.py` | identical: the same 30 changed lines, nothing differing | OWN/HELD at 60.5, the controls "plans 61.0" |
| `sw/litex/test_ctrl_memory.py` | identical: the same 4 lines | the control "the size fixture's entry at the platform's 60.5" |
| `sw/litex/ctrl_memory.py`, the platform's 8x8/2if entry | the value is the same, `60.0` -> `60.5`; the reason string and header comment are adapted | this tree's `ctrl_plat` of 20,288 B is kept, since `plat_ledger` reads the built image; the reason names GET_AS_PATH's 168 B and #897's ruling item 1, not #895's 184 B |
| `sw/firmware/ctrl/plat/README.md`, two lines | adapted | 1,880 B of `rom` left in 133,120, not #895's 1,864 |
| `SPLIT_CONTROL_MEMORY.md` section 3's table row, section 5 | the "entry is 60.5 since..." sentence and #901's caps sentence are verbatim; the row and section 5 are adapted | section 5 states this head's plan: 1,880 B left, a debt of 4.5 RAMB36, GET_AS_PATH using 312 B of the half tile, graded against 133,120 B once #901 is composed (ruling items 3 and 5) |

At the #901 merge, `ctrl_memory.py`'s entry and the two docs lines will conflict on the `ctrl_plat` figure and the reason wording. They resolve by taking the composed image's measured `ctrl_plat` and both rulings' names. `ctrl_memory_ledger.py` and `test_ctrl_memory.py` merge trivially.

`plat_ledger.py --self-test` on a clean clone of `2170b22e` passes every point, with 7 of 7 planted controls. The platform's 8x8/2if image is 131,240 B, 60.5, PASS. `test_ctrl_memory.py` has 0 failures, and the fixtures exit 0.

## 2. GET_AS_PATH's record, tracked (item 4)

- `3079bb1e`: the answering-ports arm's `path` port reads what the face's reads ([`arm_path.py`]): the count at kind 2 selector 0, then each entry at selector 8 by its ordinal, each word a bounded `mbx_win_read` to the contract's whole bound. It answers eight entries, the shipped datapath's most.
  - The `aecp` group's `get_as_path` row is in `scenario.py`'s group list, so every pass runs it.
  - `record_classes.py` names GET_AS_PATH, and refuses a pass whose 1x1/1if answering-ports leg answered no GET_AS_PATH SUCCESS, or a GET_AS_PATH over `record.aecp`. Both are planted controls, 13 of 13 refused.
- `6ef7a8ff`: the row sends GET_AS_PATH on **AVB_INTERFACE 0 at every interface**, as `get_avb_info`'s row does.
  - At `3079bb1e` it sent descriptor_index = the interface. Both 8x8 legs were refused there with "aecp.get_as_path.if1: unexpected response: status NO_SUCH_DESCRIPTOR", because each image holds one AVB_INTERFACE (`MBX_CTRCHG_AVB_INTERFACE_COUNT 1u`).
  - The check is "the get_as_path row sends GET_AS_PATH on AVB_INTERFACE 0 at its length, SUCCESS where the ports answer". It catches 3 planted mutants by name, among them the new "get_as_path sent on AVB_INTERFACE 9, a descriptor no image has".
  - The harness self-test: 0 failures, 249 of 249 mutants caught.

| Point | Leg (head) | GET_AS_PATH record | By the rule | Ordinary class | Verdict |
|---|---|---:|---:|---:|---|
| 1x1/1if | arm B `aecp` (`3079bb1e`; the 1x1 script is the same at `6ef7a8ff`, interface 0 only) | 16,208 cycles, SUCCESS | 175 us | 235 (245 restated) | held |
| 8x8/2if | arm B `aecp` (`6ef7a8ff`), if0 / if1 | 16,397 / 15,966, SUCCESS | 175 / 170 | 265 | held |
| 1x1/1if | arm A `aecp` | 10,948, ENTITY_MISBEHAVING | 115 | 235 | held |
| 8x8/2if | arm A `aecp` | 11,328 / 11,150, ENTITY_MISBEHAVING | 120 | 265 | held |

- The response carries 8 entries, a control_data_length of 80.
- The nine answers' two data words each (18 reads at 60 cycles), which an unanswered read does not fetch, would add about 1,080 cycles: about 17,290 cycles, 185 us. That is still within.
- No STOP condition: the record is not over the ordinary class, and the response is not changed on the wire.

## 3. The record classes, the stated-table compare, the pace and slice rules

**The legs, one interface:**
- the full arm A at 1x1/1if (`mA1`, 4 quarters, 96 groups, one build) at `3079bb1e`: rc 0 each, 0 refusals, the 7 known held-egress `backlog-owed` misses, 0 of 140,748 passes over THE SHARE;
- the whole answering-every-port arm (`mE1`, 16 groups): rc 0, 0 misses;
- arm B (`mB1`: `aecp`, `aecp-fanout`, `aecp-largest-notice`): rc 0.

**The 8x8 legs** at `6ef7a8ff`:
- `m2B8` (arm B: `aecp`, `aecp-largest-notice`, `aecp-fanout`): rc 0. Two `aecp-largest-notice` passes are over THE SHARE, the longest 244,460 cycles; this is #902's reported 8x8 condition.
- `m2A8` (arm A: `aecp`, `datapath-events`): rc 0.
- `mN8` (every-port: `notice-every-0`, `notice-burst-0`) at `3079bb1e`: rc 0.

**`record_classes.py` over every leg, before the restatements:** FAIL on two class lines (`receipts/compare/record_classes-before-restate.txt`).

| Class at 1x1/1if | Record | Cycles | By the rule | Stated | At `234bc149` | At `b58a5430` (the merge, the arm's ports unchanged) |
|---|---|---:|---:|---:|---:|---:|
| other (`record.aecp`) | answering-every-port SET_NAME, all 16 groups | 23,051 | 245 | 235 | 22,236 (235) | 23,051, the same ELF as `mE1`'s |
| paced (`edit_rows.PACED`) | answering-ports accepted SET_CONFIGURATION | 28,752 | 305 | 300 | 28,376 (300, #902's figure) | 28,357 (300), with the stub port |

Attribution (`receipts/harness/attribution/`): each is the same work with its fetches moved by the code's placement.
- The every-port image at the merge moves 156 of its 407 uniquely named functions by 4 to 868 B (107 of them, from `srp` on, by 332 B).
- The arm B image moves every function after the arm's ports by 304 B: 159 of them, from `a_random`, where the reading port is longer than the stub.

**The stated-table compare** (`compare5.sh`, the round's tools over A1-A4, E1 and B1; `receipts/compare/compare-1x1-before-restate.txt`): every other cost holds by the rule. Examples (measured / rule / stated, us):
- the build of one, 690.59 / 730 / 735;
- AECP's timer slot, 66.47 / 70 / 70;
- LINK 150 / 155; TICK 50 / 55;
- an SRP record, 280 / 280;
- the largest legal notice, 360 / 365; the largest legal command, 925 / 975;
- AS_PATH_CHANGED 29.18 us / 35, AVB_INFO_CHANGED 30.53 / 35, AMAP_LIVE_WRITE 24.24 / 30.

The only class lines are the two above, plus arm A's one-row REMOVE at 240 (the paced class).

**The restatements by the rule** (ruling item 4: "the stated-table compare, then the pace and slice rules"):
- `load_grade.py` `STATED_US` and `STATED_US_DONOR` `1x1/1if` `record.aecp` 235 -> 245;
- `edit_rows.PACED['1x1/1if']['an accepted SET_CONFIGURATION']` 300 -> 305.

Re-graded (`receipts/restate/`, `receipts/compare/compare-1x1-restated.txt`):
- the compare's only exceedances are the class lines, each within its own class: the notice 360 of 365, SET_CONFIGURATION 305 of 305;
- `record_classes.py` over every leg, both points: **RESULT PASS**;
- `flip_grade.py --check --point 1x1/1if`: **PASS**:

  | R4 (20) | R4L (238) | ACMP (30) | ADP (30) | MAAP (30) | First (20) | R5 (90) | R6 (90) | Last (130) | tx (49) | txL (49) |
  |---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
  | 13.25 | 188.48 | 29.14 | 27.49 | 27.61 | 14.67 | 74.32 | 72.41 | 127.52 | 33.57 | 48.61 |

  #902's figures were 13.10, 188.48, 28.95, 27.30, 27.42, 14.66, 74.07, 69.86, 127.21, 33.38 and 48.43.
- `load_grade.py --check`: 0.518 at the pin, 0.514 with tsn-c-stack#32 (0.516, 0.512);
- the pace rule (`paced_rows.choice`): 8 ms, matching `aecp_mbx.h`;
- the slice rule (`tier_grid.py --point 1x1/1if`): 6 of 420 hold. CHOSEN: slice 950 us, tier 1 aecp-first, tier 2 srp-first, AECP queue, cap 2, least margin +0.0080 (#902: 10 of 420, +0.0116). That is the built design.

No firmware header states either cost, so every image is unchanged.

**8x8/2if, reported, not held, not restated** (`receipts/8x8/`). Arm A's `datapath-events` measures 38.64, 34.56 and 23.88 us for AVB_INFO_CHANGED, AS_PATH_CHANGED and AMAP_LIVE_WRITE (37.40, 33.67 and 23.19 at `234bc149`).
- By the rule that is 45, 40 and 30, against `DATAPATH_US`'s 40, 40 and 25.
- This pass compared the 1x1/1if tables only, so the 8x8 statements are left. With them restated in a scratch tree, the reported last queued notice is 836.57 ms (806.60) and txL 469.52 (459.40).
- Every other 8x8 class is within: long 1,540 of 1,650, other 240 of 265, paced 585 of 595.

**The answered notice** (a scratch every-port arm, `cl-path5`, never committed; `receipts/harness/scratch/`): the round that builds it is 28,098 cycles in `notice-every-0` (1 notice, admitted at 34,000) and 65,576 in `notice-burst-0` (3 notices, 85,000). The 8 entry reads take 3,103 cycles. rc 0, 0 misses.

## 4. Residue R833-3 R1 and R2

- R1: section 13's "GET_AS_PATH through the face" no longer says "at the merge of `894-tiers` `5b264bf2`" as current. It is measured on `234bc149`. Section 5's paragraph was replaced in `2170b22e`, and section 5's arm table adds the `234bc149` row (126,436 B), so the `5b264bf2` row reads as history.
- R2: the record's remaining reads are stated as "the nine answers' two data words each (18 reads)".
- R3 (the PR body's reviewer lines) is applied in `PR-BODY.md`.

## 5. Full gate pass

One pass at `eca1b9ca` (`final_pass5.sh`), each part on its own fresh clean clone: 24 dispatched units, every one rc 0 (`receipts/gates/dispatch-final-eca1b9ca.log`), and the four sweep shards on their own picked ranges.

| Gate | Result | Receipt |
|---|---|---|
| every workflow job a PR to `dev-soft-core` triggers, every `run:` step (`rtl-fast`, `docs`, `elaborate`, `rtl` with its four yosys shards) | 139 steps ran, 226 not run with a stated reason, 0 bad (`verify_wf rc=0`); the 28 job clones have no tracked change afterwards | `receipts/gates/verify-table.md`, `gates/wf/` |
| AECP campaign | 308 caught, none missed (#902's 299 and the nine `face-as-path-*` plants, each by its named test) | `gates/wf/rtl-fast__firmware-aecp-mutants__ci_step_9.log` |
| control campaign | 717 of 717; `plat-as-path-unavailable` caught by `platboot1` and `platboot2` | `...firmware-control-mutants__ci_step_9.log` |
| SRP campaign | 345 caught | `...firmware-srp-mutants__ci_step_9.log` |
| firmware unit, coverage, boundary | `fw_coverage.py --check` PASS (39 files); `ctrl_boundary: PASS` | `...firmware-unit__*`, `...firmware-boundary__*` |
| lane gates, three parts | 40 at 0, and the 4 that exit 1 by design, each refusing the same rows as at `234bc149` (8x8/2if's ten; as built at 1x1/1if R4, first and last; `receipts/gates/exits-1-vs-234bc149/`). Among the 40: the harness self-test (0 failures, 249 of 249 mutants), `rows_tiers` 1,033 of 1,033, flip 585 of 585, load 26 of 26, `flip_grade.py --check --point 1x1/1if` PASS (the figures of section 3), `load_grade.py --check` 0.518 / 0.514, `tier_grid.py` CHOSEN 950 us (+0.0080), `plat_ledger` PASS (8x8-if2 131,240 B, 60.5), the fixtures, `test_ctrl_memory`, `docs_check` 0 findings, the em-dash gate against `cec88385` and `234bc149`, both idiom ratchets (long module 10 of 10), the split boot ready at 26.921, 66.545 and 68.766 ms against 20,000, 6 of 6 native controls and 3 of 3 plants, `test_builder.py --require-rv32` (the 2 arms not run as at round 3), the NVM gate (526 tests, 144 plants), `behave`, the twin and its plants, the hooks self-test (28 of 28, 96 of 96) | `receipts/gates/lane/` |
| CPU budget harness legs, one a point and arm (`fB1`, `fB8`, `fA1`, `fA8`, `fE1`, `fN8`) | every leg rc 0; every ELF byte-identical to its measurement build; the 1x1 group scripts byte-identical to `3079bb1e`'s and the 8x8 to `6ef7a8ff`'s; GET_AS_PATH 16,208 and 16,397 cycles and SET_CONFIGURATION 28,752 and 55,631 again | `receipts/harness/final-eca1b9ca/` |
| full Verilator sweep, four shards | 65 suites (15, 17, 17 and 16 a shard, each shard on its own picked range): 64 passed, 0 failed; `milan_dp` timed out at its 4,800 s in shard 0 under the host's contention (load average about 200; "result UNKNOWN, not a failure" by the runner, its partial log 13,690 checks, 0 failures), and ran again alone on its own booked range on a fresh clean clone at the head, as the runner asks: PASS in 2,548 s, `suite_tally.py --verdict` clean, 13,878 checks. 2,713,040 checks in all, 0 in-suite failures, round 3's count | `receipts/sweep/`, `sweep/rerun-milan_dp/` |

**#909.** The 8 images at `2170b22e` (the final head's firmware) are byte-identical to `b58a5430`'s, and every writable symbol has the address and size it has at `234bc149` (`receipts/rom/sram-layout-234bc149-vs-2170b22e.txt`).

**#902 moved during the round** to `478ff78c` (six commits). Not merged: this round is on round 13's `234bc149`, as the ruling fixes. A scratch trial merge into `eca1b9ca`, aborted and never committed, conflicts only in FR_NFR 3.4.1's paced paragraph (`receipts/sync/894-tiers-478ff78c-trial-merge.txt`).

## 6. Changes (file:line, reason)

| Commit | File | Change | Reason |
|---|---|---|---|
| `2170b22e` | `sw/litex/ctrl_memory.py`, `ctrl_memory_ledger.py`, `test_ctrl_memory.py`, `plat/README.md`, `SPLIT_CONTROL_MEMORY.md` sections 3 and 5 | the platform's 8x8/2if entry at 60.5 | ruling item 1 |
| `3079bb1e` | `tb/verilator/ctrl_service_budget/arm_path.py` (new), `build.py`, `answers.py`, `scenario.py`, `record_classes.py`, `selftest_answers.py`, `selftest_mutants.py`, `README.md` | GET_AS_PATH's record tracked in arm B's `aecp` group and held as an ordinary record | ruling item 4 |
| `6ef7a8ff` | `answers.py`, `scenario.py`, `selftest_answers.py`, `selftest_mutants.py`, `README.md` | the row on AVB_INTERFACE 0 at every interface | the 8x8 legs' NO_SUCH_DESCRIPTOR |
| `eca1b9ca` | `load_grade.py`, `edit_rows.py`, `SPLIT_CONTROL_MEMORY.md` (sections 5 and 13), `FR_NFR.md` 3.4.1, the harness README | the two restatements and section 13's GET_AS_PATH subsection at `234bc149` | the compare by the rule; R1, R2 |

## 7. New checks (planted mutant, failing words)

- "scenario: get_as_path sent on AVB_INTERFACE 9, a descriptor no image has", "...stated SUCCESS on the image as linked", "...sent as GET_AVB_INFO". Each is caught by "the get_as_path row sends GET_AS_PATH on AVB_INTERFACE 0 at its length, SUCCESS where the ports answer".
- `record_classes.py`: "a pass missing arm B's GET_AS_PATH" and "a GET_AS_PATH over record.aecp", refused by "the pass is missing arm B's GET_AS_PATH" and "over the other record's 235 us (command GET_AS_PATH)". The synthetic pass keeps its own statements.

## 8. Notes

- **Open observation, not changed:** at two interfaces each image's entity model holds one AVB_INTERFACE. The mailbox contract keeps one (`MBX_CTRCHG_AVB_INTERFACE_COUNT 1u`), so a command naming AVB_INTERFACE 1 finds no descriptor: GET_AS_PATH there answered NO_SUCH_DESCRIPTOR. Whether a two-interface Milan entity must hold an AVB_INTERFACE an interface is outside #897's scope, and this round cannot open an Issue for it.
- The `aecp-fanout` SET_NAME (0x0010) of arm B is reported, not held: 22,134 cycles, 235 us, within 245.
- Scratch: `r4/` holds the clones `cl-base` (`234bc149`), `cl-head` (`b58a5430`), `cl-m` (`3079bb1e`), `cl-m2` (`6ef7a8ff`), `cl-path5` (scratch) and `trial-r`/`trial-8` (scratch copies, never committed).
- Posted: REVIEW READY on #897, issuecomment-6894799910, once. No other comment was posted, edited or deleted. Nothing is pushed, and no PR was edited; `PR-BODY.md` is for the manager.
- No unit of this lane is left running. The session runner's own unit was not touched.
- Scratch: 12 GB. It holds the measurement and final builds (`r4/builds/`), the final pass's outputs (`r4/gates-out/`), the clones `cl-base`, `cl-head`, `cl-m`, `cl-m2`, `cl-path5`, `cl-final-eca1b9ca` and the sweep source. The `milan_dp` re-run clone, `trial-r`, `trial-8`, `trial-m`, round 4's `cl-cut` and its lane-gate clones are deleted.
- The receipts are sanitized and indexed after sanitizing (`receipts/INDEX.md`, copied to `INDEX.md`): 579 files, no host path, none over 200 KB. The scripts are in `scripts/`.
