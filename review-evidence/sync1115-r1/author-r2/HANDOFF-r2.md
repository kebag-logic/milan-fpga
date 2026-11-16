# HANDOFF r2: [A787] sync dev 6b66f66d into dev-soft-core, round 2 (#665)

Status: REVIEW READY posted on #665 (issuecomment-6930817036), with three open questions (section 6). Round 1: receipts and handoff in round1/; STOP #665 issuecomment-6903515775.
Ruling on the STOP: #665 issuecomment-6907491626 (the row is an open miss, never debt; phase spread on the sync alone
and on a trial merge of #914; merge dev-soft-core 70f4056f; finish the gates and the sweep). #919
issuecomment-6907491954 takes the 1000BASE-T-only advertisement. BRAM rule: #923 issuecomment-6906679024.

## 1. The merge of dev-soft-core `70f4056f` (#901), `10b2fe21`

One `git merge --no-ff origin/dev-soft-core` (`70f4056f`) onto `d2da3159`; parents `d2da3159` and `70f4056f`. 52 files
differ from `d2da3159`; the pins are unchanged on both sides (gptp-processor `1616fc8f`, protocol-processor `801ef228`,
tsn-c-stack `715589c1`). `git merge-tree` reports two textual conflicts, both in documentation:

| File | Conflict | Resolution |
|---|---|---|
| `docs/design/SPLIT_CONTROL_MEMORY.md` | section 5: the lane's round-1 restatement (`3a5ba178`) of the fit table against #901's rewrite of the same section; the auto-merge put the lane's figures under #901's "#894's head" columns | dev-soft-core's file whole, plus the lane's one sentence on the sync's delta (receipts/merge2-fit-page-vs-dsc.diff); its figures restated at the merged head in `30c5d3d6` |
| `tb/verilator/milan_dp/README.md` | the contents list: the lane's split (twenty-eight plants) and twin (fourteen plants) lines against #901's srptx line (twenty-seven plants, thirteen code mutants, the stream frames' stream_id) | every line of both sides kept (receipts/merge2-cc-readme.diff) |

No code conflicted. #901 changes no RTL, so the split and release images' gateware inputs are those of `d2da3159`
except the firmware it links (section 4). lwSRP's LeaveAll seed is unchanged by it (`srp_mbx.c:433-434` at the merge,
`mrp_port_configure(..., (uint32_t)i->mac, ...)` and `^ 0x91u`).

## 2. Commits after it

| Commit | Kind | What |
|---|---|---|
| `30c5d3d6` | restatement (docs) | section 5's sync sentence at the merge: 32 to 40 B of `rom` against dev-soft-core `70f4056f`, no tile moved; the 8x8/1if platform 130,224 B in 131,072 (56.0, 848 B spare), the 8x8/2if platform 131,784 B at its ledger's 60.5 |
| `4cb7d7ab` | regeneration (docs) | `docs/DOCUMENTATION_AUDIT.md` through `docs_inventory.py --write`: two rows, the budget harness's README (802.1Q among its standards) and milan_dp's README (`sw/firmware/ctrl` among its paths), stale after the merge; `--check` passes after. dev-soft-core has no `docs_inventory.py` (it came with dev) |

| `9715a30a` | semantic conflict (tests; found by the sweep) | `pp_shadow`'s and `milan_dp`'s bootsa benches read KL_pp_shadow's internals at dev's flat path, `milan_datapath__DOT__pp_shadow__DOT__...`. On this line the wrapper sits in dev-soft-core's `generate if (CTRL_SPLIT_P == 0) begin : g_af_pp` (`milan_datapath.sv`), so both benches failed to compile in the sweep: `pp_shadow` in its vid73 and crf fixture builds, and `milan_dp` at `bootsa-build`, which stopped its run. The five reads dev added (#862's drop probes, bootsa's early-offer probe) take the `g_af_pp` path, as the bench's other nine reads from dev-soft-core already did. With it, `pp_shadow` passes, and bootsa 67 checks with 0 failures |

The final head is `9715a30a`. It differs from the merge `10b2fe21` in the two documentation files and those two bench
sources only. So every firmware, RTL and harness measurement taken at `10b2fe21` holds for it: the routes, the twin,
srptx and the seed runs. The harness legs are attested at the final head too (section 5).

**Semantic conflicts checked and not committed** (each fails identically on dev-soft-core `70f4056f`, so none comes
from the merge; receipts/twin/, receipts/srptx/):
- `make twin` gives 1 finding at the merge and at `70f4056f`: `[DIFF] owed row split-talker-failed does not hold`.
  #901 makes the split declare Talker Advertise for STREAM_OUTPUT 0 from the PROBE_TX until it withdraws, as the
  fabric does (split `New x2, JoinMt x19, Lv x1`, fabric `New x2, JoinMt x15, Lv x1, Mt x5`). The row still asserts the
  split's old Talker Failed. The twin's rule is that the lane that fixes a difference deletes its row; #901 did not.
- `make twin-plants`: plant `srp-plus-k` ESCAPED at both, by its words "MSRP Talker Failed stream_id ...0001". The
  plant's bump is now refused by other words (`[MRP] split MSRP Talker Advertise ... is not an Applicant's message`).
- `make srptx` fails at both on one kind, `[TIME] ... a requested transmit opportunity`. At `70f4056f`: wire 1,103,
  hold 58, licence 47 findings. At the merge: 1,108, 59, 49, the counts moving with the MAC-seeded draws (#916).
- The stream-output-0-notices owed row still holds, but its stated cause ("the split's talker declaration state never
  changes") is no longer true after #901. The split now changes its declaration state and still sends no GET_STREAM_INFO
  notice for it.

None of these is a CI gate or a sweep case. Fixing them is #901's follow-up, not this sync's (section 6).

## 3. LeaveAll phase spread at 8x8/1if (ruling items 2 and 3)

**Method (an experiment; no product change, nothing committed).** lwSRP draws a participant's first LeaveAll at
62 ms + 10 ms x (1001 + r mod 499), r = seed x 1664525 + 1013904223 mod 2^32, seeded with the interface MAC's low 32 bits
for MSRP and those XOR 0x91 for MVRP (`srp_mbx.c:433-434`). The draw reproduces every run-out observed (product MAC:
14,092 and 14,922 ms drawn, 14,092.0 and 14,922.0 ms run out). Ten MACs `02:4b:4c:00:xx:xx` were chosen to place
MSRP's first LeaveAll from 10,092 to 15,032 ms, about every 500 ms, across the window `save-held` and `save-starved`
cover; the product MAC is the eleventh phase. Each seed is its own clone of `10b2fe21` whose only change is
`configs/endstation_ax7101_8x8.yaml`'s `mac_address` (receipts/tools/mkseed.sh), run with
`run.py --point 8x8-1if --groups save-held,save-starved`.
- **The sync alone:** `10b2fe21`, whose firmware is the final head's.
- **The trial merge:** `10b2fe21` with `origin/894-8x8-1if` `d539f162` (#914's pushed head) merged locally, never
  committed or pushed. Conflicts resolved as follows: `ctrl_loop.h` takes #914's shape table (THE SHAPES), with 1x1/1if's
  slice at #895's 900 us; `aecp_shape.py` takes both sides (#914's guarded key domain and #901's name runs);
  `poll_grade.py` takes #914's shape-keyed table with #901's restated base and `aecp_long` figures; comments and
  documents take one side. The patch is 206,048 B, sha256 `c13c7171dcfd521cb62657e04085eb378cade54e52514c12e2d7531131312f09`
  (kept in scratch, over the receipt size limit). The trial's harness is the composed one, whose MRPDU row budget is
  #914's 49 ms (`mrpdu_grade.BUDGET_MS`); the sync's is T_svc, 20 ms.

**Result** (receipts/budget/leaveall-spread-table.md, every run-out; receipts/budget/leaveall-spread/, one read-out a
run). The worst of the two groups at each phase; bold is over that tree's row budget:

| First LeaveAll drawn, MSRP / MVRP, ms | MAC in the 8x8 config | sync: leaveall.if0, ms | sync: periodic.if0, ms | trial: leaveall.if0, ms | trial: periodic.if0, ms |
|---:|---|---:|---:|---:|---:|
| 10,092 / 10,492 | 02:4b:4c:00:01:51 | **160.6** | 1.8 | **160.6** | 1.4 |
| 10,592 / 10,992 | 02:4b:4c:00:01:5f | 0.6 | **100.6** | 0.6 | **100.6** |
| 11,102 / 14,142 | 02:4b:4c:00:00:06 | **150.5** | 1.8 | **150.6** | 1.6 |
| 11,602 / 14,212 | 02:4b:4c:00:00:14 | **40.6** | 1.7 | 40.6 | 1.5 |
| 12,102 / 10,152 | 02:4b:4c:00:00:22 | **151.6** | 1.6 | **151.9** | 1.4 |
| 12,602 / 10,222 | 02:4b:4c:00:00:30 | **30.6** | 1.7 | 30.5 | 1.4 |
| 13,102 / 10,722 | 02:4b:4c:00:00:3e | **150.5** | 2.0 | **150.6** | 1.7 |
| 13,602 / 11,652 | 02:4b:4c:00:00:4c | 1.3 | 3.0 | 1.3 | 2.3 |
| 14,092 / 14,922 | 02:4b:4c:4b:4c:01 (the product's) | **160.6** | 1.8 | **160.5** | 1.6 |
| 14,602 / 12,652 | 02:4b:4c:00:00:68 | 0.6 | 1.8 | 0.6 | 1.4 |
| 15,032 / 14,632 | 02:4b:4c:00:00:88 | 0.5 | **140.8** | 0.6 | **140.6** |

- **Worst row, the sync alone:** `mrpdu.leaveall.if0` 160.6 ms (seed `02:4b:4c:00:01:51`, `save-held`; the product
  MAC 160.6 ms). 9 of 11 phases are over 20 ms, 7 of them over THE TRANSMIT's 49 ms.
- **Worst row, the trial merge with #914:** `mrpdu.leaveall.if0` 160.6 ms (the same seed). 7 of 11 phases are over 49 ms.
  **The trial merge still misses** (ruling item 3). Its rows equal the sync's within 0.4 ms at every phase.
- `mrpdu.periodic.if0` misses the same way at two phases (100.6 and 140.8 ms): a periodic timer's frame waits like a
  LeaveAll's.

**What holds the frame (measured; reported for the decision, not acted on).** This covers all 36 LeaveAll run-outs
delayed past 5 ms, on both trees (receipts/tools/la_join.py):
- the first frame goes 0.44 to 1.56 ms after its participant's next join-timer run-out;
- that run-out is 189.1 to 189.6 ms after the participant's previous build (for example 29.5 + 160.0 or 39.9 + 149.4 ms);
- the CPU is busy for 11.6 to 21.9 % of the wait in `save-held`. In `save-starved` it is busy 96.9 to 98.7 % under
  the grandmaster flood, and the frame still leaves at the join timer's run-out;
- THE TRANSMIT's longest build is 31,247 to 31,753 cycles, inside the 90,000-cycle slice (the sync) and the 147,500
  (the trial).

A run-out whose join timer is not running is released within 0.5 ms.

lwSRP's code matches the measurement:
- `mrp_transmit` returns without sending while `join_wait` is set (`third_party/lwSRP/src/core/mrp_mad.c:1421`);
- every transmission sets it and arms the join timer for `join_cs` (`:1539-1540`), the adapter's 19 cs;
- only `on_join_timer` clears it (`:854`);
- a LeaveAll (`:803-807`) or periodic (`:828-838`) run-out sets `tx_pending`.

So a timer that runs out within one JoinTime of its participant's last transmission is sent at the join timer's run-out,
up to 190 ms later. The CPU budget does not decide it, and no slice change can remove it. Whether THE TRANSMIT's
row (FR_NFR.md 3.4.1) is meant to time that wait is a decision for #665 (section 6). The same deferral explains the
1x1/1if leg in section 4.2.

Also measured once, on the trial tree only: its 8x8/1if slice is 1,475 us (147,500 cycles), and SRP's longest record
there is 119,589 cycles (70,755 to 73,044 on the sync).

## 4. Figures

### 4.1 ROM per split image (receipts/images/)

Each image linked as `ctrl_srp_image.py` and `ctrl_plat_image.py` link it, at dev-soft-core `70f4056f` and at the merge
`10b2fe21` (the final head's firmware). `rom` grows 32 to 40 B at every point (the #840 identity's immediates). `sram`
and the tile counts are unchanged:

| Image | `rom`, B, at `70f4056f` -> merge | `sram`, B | RAMB36 | Ledger entry |
|---|---|---:|---:|---|
| fixture 1x1/1if | 112,424 -> 112,456 in 112,640 | 55,200 | 41.0 | none (cap 56) |
| fixture 1x1/2if | 113,984 -> 114,016 in 114,688 | 57,376 | 42.5 | none |
| fixture 8x8/1if | 125,088 -> 125,128 in 126,976 | 96,304 | 55.0 | none |
| fixture 8x8/2if | 126,608 -> 126,640 in 126,976 | 113,248 | 59.0 | 59.0 |
| platform 1x1/1if | 117,480 -> 117,512 in 118,784 | 56,224 | 43.0 | none |
| platform 1x1/2if | 119,064 -> 119,096 in 120,832 | 58,400 | 44.0 | none |
| platform 8x8/1if | 130,184 -> 130,224 in 131,072 (848 B spare) | 97,328 | 56.0 | none |
| platform 8x8/2if | 131,744 -> 131,784 in 133,120 | 114,224 | 60.5 | 60.5 |

The owner's BRAM rule (#923 issuecomment-6906679024) is not triggered: no image is over its ledger entry, and no
unledgered image is over 56 (the 8x8/1if platform plans exactly 56.0). No S14 debt is added.

### 4.2 CPU service-budget harness at 1x1/1if (the product MAC)

Builds at `10b2fe21`, from one checkout (c-b2), attested at the final head in section 5. Against round 1's legs at
`d2da3159`:

| Leg | Merge | Round 1 |
|---|---|---|
| arm A q1 (24 groups) | 0 refusals, 0 misses (0/254 instances, 0/12 paths), 0/17,844 passes over the share, rc 0 | 0, 0 (0/254, 0/12), 0/17,791, rc 0 |
| arm A q2 (24) | 0, 0 (0/218, 0/61), 0/38,208, rc 0 | 0, 0 (0/218, 0/61), 0/41,093, rc 0 |
| arm A q3 (24) | 0, 0 (0/253, 0/11), 0/59,514, rc 0 | 0, 0 (0/253, 0/11), 0/64,107, rc 0 |
| arm A q4 (24) | 0, 7 (7/225, 4/52): `backlog-owed`'s ruled held-egress rows, each within 0.25 ms of round 1's; 0/16,248, rc 0 | the same 7, 0/16,244, rc 0 |
| answering-every-port (16) | 0, 0 (0/280, 0/7), 0/20,747, rc 0 | 0, 0 (0/280, 0/7), 0/21,765, rc 0 |
| answering-ports: aecp-fanout, aecp, aecp-largest-notice | 0, 0 (0/44, 0/43), 0/339, rc 0 | 0, 0 (0/44, 0/43), 0/339, rc 0 |
| **valid-destinations (#901's arm; 2 groups)** | 0 refusals, 0 misses (0/5, 0/3), 0/2,666; **rc 1**: `srp-talker`'s LeaveAll run-out at 14,054.1 ms, its first frame 160.5 ms after it, past THE TRANSMIT's 49 ms (late) | not on that line; #901 reports it at 1x1/1if with no miss, with the pre-#840 MAC |

The valid-destinations leg's late LeaveAll is the section 3 deferral at the shipping point. The previous build was
29.2 ms before it, the join timer runs out 160.0 ms after it, and the CPU is busy for 2.3 % of the wait. #840's MAC draws
MSRP's first LeaveAll at 14,092 ms; the pre-#840 MAC drew it at 14,622 ms.

Model gates on a clean clone of the final head (receipts/budget/models/):
- `flip_grade.py --check --point 1x1/1if`: PASS (R4 13.25, R5 75.84, R6 73.36, first 14.72, last 136.65 of 140, R4L
  203.57 of 238, ACMP 29.63, ADP 27.86, MAAP 27.96, tx 34.00 of 49 ms).
- `load_grade.py --check`: PASS (1x1/1if 0.517 at the pin, 0.514 with tsn-c-stack #32, ceiling 0.70).
- `tier_grid.py --point 1x1/1if`: 900 us chosen, 6 candidates hold every row and the load.
- Self-tests: flip 585 of 585, load 26 of 26, record_classes 11 of 11, rows_tiers 1033 of 1033; `run.py --self-test`
  0 failures.

### 4.3 CPU service-budget harness at 8x8/1if (the product MAC)

As in round 1, the point is held to one interface's 1x1/1if stated costs (#914's scope), so `STATED` lines stand at
both heads. At the merge the slice is 900 us (#895's ruling), THE TRANSMIT's longest build is 31,247 cycles, and the
build-one `STATED` lines of round 1 are gone in arm A.

| Leg | Merge | Round 1 (`d2da3159`) |
|---|---|---|
| arm A part 0 (22) | 0 refusals, 7 misses (7/213, 4/24): `backlog-owed`'s ruled held-egress rows, each within 0.8 ms of round 1's; saves durable 22,829.5 and 4,818.8 ms; 0/141,280 passes; 10 `STATED` lines (polls base, ACMP item); rc 1 | the same 7; saves 22,829.7 and 4,817.8 ms; 221 `STATED` lines |
| arm A part 1 (24) | 0 refusals, **1 miss**: `save-held.mrpdu.leaveall.if0` 160.557 ms (run-out 14,092.2 ms); 0/23,464 passes; 2 `STATED` lines; rc 1 | 1 miss, 161.123 ms; 214 `STATED` |
| arm A part 2 (24) | 0 refusals, **1 miss**: `save-starved.mrpdu.leaveall.if0` 160.506 ms (run-out 14,092.1 ms); 0/80,514; 2 `STATED`; rc 1 | 1 miss, 161.069 ms; 218 `STATED` |
| arm A part 3 (25) | 0 refusals, 0 misses (0/231, 0/20), 0/24,066, no `STATED` line, **rc 0** | 0 misses, 208 `STATED`, rc 1 |
| answering-ports `aecp-largest-notice` | 0, 0 (0/5, 0/5), 2 of 105 passes over the share (longest 2.238 ms), **rc 0** | 1 of 106 (2.025 ms), rc 1 |
| answering-every-port `notice-every-0` | `RuntimeError: the model holds 40 notices, not AECP_NOTICES_MOST at 8x8-1if` | the same |
| valid-destinations (2) | 0, 0 (0/19, 0/10), 0/2,986; rc 1: `srp-talker`'s LeaveAll at 14,092.1 ms late by 160.9 ms (the section 3 deferral), and `STATED` build-one lines | not on that line |

## 5. Gates (clean clones of the final head `9715a30a` unless stated)

Every job of the four workflows ran on its own clean clone of `9715a30a` in one runner root, `runs/J`. The sweep ran at
`4cb7d7ab`, and it is what found `9715a30a`'s conflict. The two suites that commit touches, and the one suite that ran out
its wall clock, ran again at `9715a30a`; the other suites read neither changed file (receipts/sweep/final-head-vs-sweep-head.txt).

Earlier in the round the host ran at 2x to 5x its CPU count, from every lane, and was restarted three times. Workflow
attempts at `4cb7d7ab` timed out on wall-clock limits under it (sv2v's 900 s in the census, the NVM self-tests' 1,200 and
180 s, the LiteX simulations' 900 s). None of them failed a check. They are superseded by `runs/J`, and listed with
their causes in receipts/workflows/earlier-attempts.txt.

| Gate | Command | Result | Receipt |
|---|---|---|---|
| **all four workflows** | `run_wf.py` per job; `verify_wf.py 9715a30a runs/J docs.yml rtl-fast.yml elaborate.yml rtl.yml --matrix=yosys-shards=shard:0,1,2,3` | **154 steps ran rc 0, 256 not run with a reason, 0 bad** (round 1's tally) | receipts/workflows/verify-wf-final.md |
| docs | every job; docs-check's steps are hosted-only (not run, with the reason) | rc 0, `docs-gates-2`'s NVM self-tests included. docs-check-no-git deletes `.git` by design, so the runner's after-status reads nothing there | receipts/workflows/ |
| rtl-fast | every job; firmware-boundary with the LiteX venv as its job venv | rc 0: BDD 511 scenarios, `fw_coverage` PASS on 39 files, lint, Yosys elaboration, split CDC | receipts/workflows/ |
| publication census | rtl-fast's publication-census, on a booked range | rc 0: 6 shapes elaborated and classified in 234 s; self-test 0 of 163 arms failed (887 s); 0 of 57 rules unproven | receipts/workflows/logs/ |
| rtl-fast mutation campaigns | firmware-control-mutants, firmware-aecp-mutants, firmware-srp-mutants | control 716 of 716 caught; AECP 299 `[ok]`, 0 bad; SRP (both campaigns, #901's Talker mutants and the pin controls) 421 `[ok]`, 0 bad | receipts/workflows/logs/ |
| elaborate | legs 0 to 4 and the aggregate, LiteX venv | rc 0, no simulation timed out | receipts/workflows/logs/ |
| rtl.yml | full-ci-gate, yosys-shards 0..3 of 4, yosys-portability, yosys-tool | rc 0 (verilator-shards is the native sweep's partition, below) | receipts/workflows/logs/ |
| **full 65-suite sweep, 4 shards** | `native-shards.py` at `4cb7d7ab` on four booked ranges | shard 0: 13 of 15 passed, `pp_shadow` and `milan_dp` failing to compile (the conflict `9715a30a` fixes); shard 1: 16 of 17 and `milan_dp_gm_steps` TIMEOUT (1,800 s, UNKNOWN); shards 2 and 3: 17 of 17 and 16 of 16. In-suite failures 0 | receipts/sweep/ |
| the sweep's three suites at the final head | `timeout <its limit> make -C tb/verilator/<suite>` and `suite_tally.py`, as `run_all_suites.sh` runs each | `pp_shadow` 2,571 checks, `milan_dp` 14,018 (its split leg 84 of 84, bootsa 67), `milan_dp_gm_steps` 202 (747 s); 0 failures, every verdict 0. **All 65 suites pass** | receipts/sweep/ |
| split leg plants | `make split-mutants` (`4cb7d7ab`; the split leg's sources are unchanged since) | 28 of 28 caught by the check each names | receipts/split-tx/ |
| two-placement simulation | `make twin`, `make twin-plants` (`10b2fe21`, and `70f4056f` for comparison) | **fail at both, identically**: 1 finding (`split-talker-failed` no longer holds); plant `srp-plus-k` escapes (section 2) | receipts/twin/ |
| srptx | `make srptx` (both) | fails at both on `[TIME]` (#916) | receipts/srptx/ |
| harness model gates | flip, load, tier grid, self-tests, `run.py --self-test` (at `9715a30a`) | PASS (section 4.2) | receipts/budget/models-final/ |
| harness legs, attested at the final head | `run.py --reuse-build --regrade` from the harness checkout moved to `9715a30a` | every build accepted against the head's inputs; all 13 legs' `table.md` byte-identical, each rc as first run | receipts/budget/regrade-at-final-head.txt |
| **record classes over every leg** | `record_classes.py` over the 13 legs' results (at `9715a30a`) | **RESULT FAIL**: `REFUSED 1x1/1if answering-ports aecp-fanout: a record of 28,700 CPU cycles, 305 us by the rule, over the paced record's 300 us (SET_CONFIGURATION, paced)`; every other class within its statement (D2) | receipts/budget/record-classes-final.txt |
| routes | `chain.sh` at `10b2fe21` (the final head's RTL, firmware and build inputs), one Vivado at a time through `vivado-slot.sh` | split 1x1/1if: met at all three directives. Split 8x8/1if: met on AltSpreadLogic_high only. **Release 1x1: setup met at all three, hold +0.014 to +0.016 ns at the fast corners, under the +0.030 floor at all three** (F5) | receipts/route/ |
| release export identity | `cmp_export.py`, round 1's head `d2da3159` against the merge | every `gateware/` file equal after path normalisation; `alinx_ax7101.v` equal outside its comments | receipts/route/release-export-round1-vs-merge.txt |

### 5.1 Routes (receipts/route/; signoff.py at the four corners)

| Image | Directive | Slow 85/0 C WNS / WHS, ns | Fast 85/0 C WNS / WHS, ns | LUT | BRAM tiles |
|---|---|---|---|---:|---:|
| split 1x1/1if | ExtraPostPlacementOpt (integrated) | +0.189 / +0.102 | +1.660 / +0.036 | 32,110 | 81 |
| split 1x1/1if | ExtraTimingOpt | **+0.196** / +0.102 | +1.636 / **+0.036** | 32,060 | 81 |
| split 1x1/1if | AltSpreadLogic_high | +0.118 / +0.102 | +1.636 / +0.036 | 32,050 | 81 |
| split 8x8/1if | ExtraPostPlacementOpt (integrated) | -0.595 (307 failing) / +0.102 | +1.636 / +0.036 | 43,580 | 92.5 |
| split 8x8/1if | ExtraTimingOpt | +0.014 (under the floor) / +0.102 | +1.636 / +0.036 | 43,578 | 92.5 |
| split 8x8/1if | AltSpreadLogic_high | **+0.140** / +0.102 | +1.636 / **+0.036** | 43,559 | 92.5 |
| release 1x1 (all-fabric) | ExtraPostPlacementOpt (integrated) | +0.108 / +0.054 | +1.642 / +0.016 | 53,571 | 87.5 |
| release 1x1 (all-fabric) | ExtraTimingOpt | +0.071 / +0.088 | +1.638 / +0.014 | 53,601 | 87.5 |
| release 1x1 (all-fabric) | AltSpreadLogic_high | **+0.209** / +0.102 | +1.638 / **+0.016** | 53,598 | 87.5 |

Split 8x8/1if equals round 1 at every directive. The worst setup path is the EDIT window's request register into the
audio map's output-claim logic (`KL_mbx_cdc/u_edit/rq_r_reg[85]` -> `milan_datapath/amap_out_owner_r_reg[308]/CE`,
33 levels). #810's route of this image at `084cf7a8` met at ExtraTimingOpt +0.292 ns. On its best directive this line
meets the floor at +0.140 ns, which the ruling accepts and asks to be reported beside #810's margin.

The release image meets setup at every directive, the best AltSpreadLogic_high at +0.209 ns. Its fast-corner hold is
+0.014 to +0.016 ns at all three, which clears the build gate's WHS >= 0 and not the round's +0.030. The worst hold paths
are inside the LiteX CPU: its fetch-to-decode PC registers (`fetch_logic_ctrls_1_up_Fetch_WORD_PC_reg[30]` ->
`decode_ctrls_1_up_PC_0_reg[30]/D`), and its memory bus into the I/O bus RAM's data pin. Its gateware export equals round
1's head's file for file, and round 1 showed it equal to dev `6b66f66d`'s. So this is dev's release image's margin, not
the sync's. dev's area plan records +0.027 ns hold for it at an earlier round (`MARK_II_AREA_PLAN.md`).

## 6. Open misses and findings

Three questions are open. Each blocks the merge, not the review, and they are listed in the round's REVIEW READY on #665. The manager's plan of 2026-11-16 20:20 (#665 issuecomment-6928162994) asks every flip lane, this sync included, to reach REVIEW READY. The ruling allows the MRPDU miss to be listed open.

- **D1. THE TRANSMIT's MRPDU rows and lwSRP's join timer** (ruling items 1 to 3; sections 3, 4.2 and 4.3). The rows miss
  at 9 of 11 LeaveAll phases at 8x8/1if on the sync alone, the worst 160.6 ms, and at 7 of 11 on the trial merge with
  #914, the worst 160.6 ms. The #840 MAC's phase also makes #901's valid-destinations leg exit 1 at 1x1/1if; with the
  pre-#840 MAC the same code passes there. Every late frame waits for its participant's join timer, one JoinTime
  (190 ms) after its previous transmission (lwSRP `mrp_mad.c:1421`, `:1539-1540`), with the CPU mostly idle. THE
  TRANSMIT's build is inside its slice. So the fix the ruling assigns to #914 (THE TRANSMIT's build within its slice at
  every phase) is already true at the merge, and the rows still miss. The decision: does THE TRANSMIT's row (FR_NFR.md
  3.4.1) time the wait lwSRP's join timer imposes, and if so who owns it? It is not a CPU-budget change, a harness
  change or a firmware change this sync may make.
- **D2. The paced record at 1x1/1if** (section 5). The merge's accepted SET_CONFIGURATION in the answering-ports arm is
  28,700 cycles, 129 past the 28,571 that 300 us holds by the rule. #901's head measured 28,288, and round 1 28,452. The
  composition moves the record, not either side alone.
  - Restating `edit_rows.PACED['1x1/1if']['an accepted SET_CONFIGURATION']` to 305 by the rule, as an experiment in a
    scratch copy (receipts/budget/paced-305/), keeps every row within its bound (tx 34.02 of 49 ms, ACMP 29.65 of 30).
  - But it puts the model's tx row past `CTRL_LOOP_TX_MS` (34 ms), so `flip_grade.py --check` fails and one
    rows_tiers control escapes. The restatement therefore reaches a firmware constant (`ctrl_loop.h`).
  - The decision: restate both by the rule (and which lane does it), or recover the 129 cycles in that path.

Findings reported, not fixed (none is a CI gate):
- **F1.** #840's 1000BASE-T-only advertisement is not on the split; #919 takes it (#919 issuecomment-6907491954).
- **F2.** The twin and twin-plants fail on dev-soft-core `70f4056f` as at the merge: #901's Talker declarations
  retired the split's Talker Failed, and the twin's owed row `split-talker-failed` and plant `srp-plus-k` still name
  it. #929 takes the row. The stream-output-0-notices row's stated cause is stale for the same reason (section 2).
- **F3.** `make srptx` fails at `70f4056f` as at the merge (#916).
- **F4.** The answering-every-port arm cannot run at 8x8/1if (`the model holds 40 notices, not AECP_NOTICES_MOST`),
  as in round 1 (#914's scope).
- **F5.** The release AX7101 1x1 route's fast-corner hold is +0.014 to +0.016 ns at every directive: under the round's
  +0.030 floor, and over the build gate's 0 (section 5.1). The image is dev's, file for file, so it is not this sync's.
  Whether the +0.030 floor applies to the release image is for #665 to say.

Scratch: 19.6 GB, under the 20 GB limit after deleting round 1's harness builds, superseded clones and the first
workflow run's job directories (their logs kept). It holds the seed runs' builds and group logs, about 9.7 GB, their
figures being in the receipts. The sweep's four shard clones under the lanes directory hold 9.1 GB more.

## 7. Host restarts

The host was power-cycled at 15:40 CET, crashed at 18:46 and was shut down at 19:39. After each, every unit without a
recorded rc was treated as cut, its half-written output removed and the unit run again:
- 15:40: the release integrated route (its work directory removed, the release re-run from its export), and the census
  in `runs/H4`.
- 18:46: the release ExtraTimingOpt route, whose signoff reports were left 0 bytes. Its directory was removed and its two
  prepared inputs rebuilt from AltSpreadLogic_high's, the directive's name alone differing; the synthesis checkpoint
  both open was checked intact. Also the census in `runs/H7`.
- 19:39: the same route again (rebuilt the same way), and the census in `runs/H8`.

No output file was left empty, and the tree and its object store checked clean (`git fsck`).
