# HANDOFF (round 3) — [A775] lane 895

**Status (21:5x CET): STOP at head `9e30c2c3` (firmware `cf5b1441`; the last commit docs only).** The 1x1/1if
build-one stated cost (`CTRL_LOOP_BUILD_ONE_PASS_US`, 430 us) in this lane's `valid-destinations` arm is over (at most
46,489 cycles), already at the sync merge; it needs a decision (section (d)). Every other leg at the head passes. The
STOP text is STOP-COMMENT-2.md, posted once on #895 as this resume's one comment: issuecomment-6864607963 (21:5x CET). RESUMED at
16:27 by the ruling issuecomment-6857334948 on #895. Started
2026-11-13 14:04 CET. Round 2 ended at REVIEW READY `18300f6e` (issuecomment-6850450637); R835-2 POSITIVE, R836-2
NEGATIVE on the PR body only. The STOP (STOP-COMMENT.md) is posted once on #895: issuecomment-6857286369; this
resume allows exactly one more comment, the REVIEW READY (or STOP) at the final head.

- Worktree $LANES/895-talker, branch `895-talker-redeclare`, not pushed.
- Base: `origin/665-s2b-cycles` at `084cf7a8` (#810 open, not merged into dev-soft-core `e5f88a8e`; checked 16:22).
- Scratch: /data-2/milan/tmp/895-a775/r3 (clones B, M, H, W, F, Z, N; builds; ledgers).

| Commit | Subject (short) |
|---|---|
| `cd6d79b6` | the sync merge of #810's `084cf7a8` (item 1) |
| `e9011df6` | #905 first design (SID after each closing, cached comparison); superseded in code by `3496eaa3` |
| `fa3f31ee` | R835-2-RS1 (`srp_bounds.h`, comment only) |
| `3496eaa3` | #905 final design: SID written again just before each reopening; 5 plants (its subject's "16 B of sram" is the 8x8/2if fixture's; 0 to 32 B across images) |
| `1aa59f75` | srptx `[SID]` check, capture plant, code arm |
| `99b71b44` | the code arm's planted line `(void)id` (it did not compile under -Werror) |
| `f1f21546` | docs: MAILBOX_SPLIT writer row, SRP README, milan_dp README (srptx at this head) |
| `a9fd4415` | #894's names patch (C4-names.patch), unchanged: ruling 6844175391, applied to #895 by 6857334948 |
| `cd863d40` | #905's state 24 B -> 8 B of `struct maap_mbx` (one source's SRC_SID words in flight, each on its own interface), so the 8x8/2if stack keeps #810's data cache sets; plants' anchors and the srptx arm's line follow |
| `cf5b1441` | test: a name change just past the last run of its type queues nothing (`EveryChangeQueuesOnlyItsOwnedRecords`), so the names patch's new branch is covered; `aecp_nvm.c` 90/90 in the ratchet |

## The ruling issuecomment-6857334948 (on the STOP) and what answers it

| Ruling item | What answers it |
|---|---|
| (a) carry #894's names patch unchanged, its own commit | `a9fd4415`: `git apply` of `894m-a778b/patches/C4-names.patch` (sha256 `52869928...f2aea0`) on `f1f21546`, applied cleanly; every `+`/`-` line identical to the patch (only hunk offsets differ: the patch was cut on #894's tree). Its subject names the patch and the two rulings. Full firmware suite on its clean clone: unit `fwsuiteN` (below) |
| (b) re-link every 8x8/2if image; each at most 58.5, else the 59.0 fallback | at `a9fd4415` (ledger.sh, plat_ledger.py's exports and runtime): fixture 124,520 / 113,232 B, 58.5 (408 B of rom left); `answering-every-port` 124,828 / 113,296, 58.5 (100 B left); `valid-destinations` 124,688 / 113,248, 58.5 (240 B left). **No fallback needed; no cap or ledger entry changed.** Platform 8x8/2if 129,680 / 114,224, 60.0; every other point at most 56 (fixture 38.5, 42.0, 51.5; platform 40.0, 43.5, 53.0); `plat_ledger.py` PASS. #905 acceptance 5's ROM half holds |
| (c) srptx `[TIME]` is #906, the hold `[TX]` path #907; not fixed | recorded with the issue numbers here, in the PR body and in the milan_dp README; `[SID]` graded on its own words (no `[SID]` finding at the head; its plant and arm refused on its words) |
| (d) finish round 3: legs on the head, the gates, the full pass once, PR body, the comment | legs `Q-*` on `a9fd4415` found two stated costs over (section (d)); the first fixed (`cd863d40`), the coverage drop fixed (`cf5b1441`); legs `S-*` on `cf5b1441`, every arm at both points: all rc 0 but `valid-destinations` 1x1/1if (the second, the merge's); acceptance 4 from those legs (fed tables, scratch): 1x1/1if 0.503 / 0.502; section 5 restated, section 13 not (waits on the decision); the gate pass not run; PR-BODY.md; STOP |

## (d) at `a9fd4415`: two stated costs over, and what each is (17:25 on)

Legs `Q-*` on `a9fd4415` (clone N): Q-N1 rc 0, Q-W8 rc 0, Q-A1 and its 3 parts rc 0, Q-A8 parts 1-2 rc 0 (parts 3-4
stopped by me at 17:4x to free CPUs for the trace below, 5-7 never started: superseded by the fix). Two failed:

- **Q-N8 rc 1**: `STATED notice-burst-1/-4: a pass's polls base of 32,594 / 32,597 CPU cycles, over its stated 32,500`
  (poll_grade 325 us at 8x8/2if; no bound may change). Every `maap_mbx:poll` call costs a constant ~2,300 cycles more
  than #810's (`X-GN8`, the bench lane's leg of `084cf7a8`): min 6,987 vs 4,725, the three modes 7,588/7,118/7,355 vs
  5,293/4,804/5,041. A committed-PC trace of the heaviest pass at both images (`BUDGET_TRACE_AFTER`, 40,000 PCs, the
  same script; r3/trace) shows the same 13 instruction refills and 69 more instructions, the extra cycles stalls in
  `ctrl_app_srp`'s `source` (+1,217 over 8 calls) and `acmp_declaring` (+666): **a data cache conflict** (8 KiB,
  direct-mapped, 128 sets of 64 B). `refresh_demand` calls `acmp_declaring` per source (8); `acmp_declaring`'s saved
  registers (stack 0x1001b900) and the fixture's `image_aecp_bridge.acmp_owner` (0x10005924, which `ctrl_app_aecp`'s
  `source` loads) share set 100, two refills a source. At #810 the frame sat on set 99. The stack is `_ebss` + 8 KiB
  (`ctrl_split.ld`, ALIGN(16)), so it moves with `.bss`: #895's Talker +48 B, #905's `struct maap_mbx` +24 B, and
  #905's poll frame 16 -> 48 B. Static check (r3/trace/dloop.py, the loop's lines by image): the conflict is in every
  8x8/2if image at `a9fd4415` (arm A, `answering-every-port`, `valid-destinations`), none at #810, none at 1x1.
- **Q-W1 rc 1**: `STATED srp-talker(-loss): a build-one pass of 45,566 to 46,367 CPU cycles, over its stated 43,000`
  (`CTRL_LOOP_BUILD_ONE_PASS_US` 430 us at 1x1/1if). Round 2's R3-W1: heaviest 37,089 (no STATED). The passes run SRP
  code only (`mrp_mad`, `srp_mbx`, `ctrl_mem`, `msrp`; no MAAP, no ACMP); at sys 327.5 M `srp_mbx` 5,351 -> 10,274,
  `mrp_mad` 22,409 -> 25,845, same instruction count, fewer refills.

**The first, fixed (`cd863d40`):** #905's state from 24 B to 8 B of `struct maap_mbx`: one source's SRC_SID words in
flight at a time, the high word on its source's own interface (`sid_owed`, inlined into `poll`), `sid_written` one
16-bit mask, `sid_wait` 16 bits per interface; `_Static_assert(MBX_N_PUB_SOURCES <= 16u)`. The stack keeps the sets
#810's image measured. dloop.py on every 8x8/2if image (ledger/P): arm A and `answering-every-port` keep only
`refresh_demand`'s once-a-call frame on the bridge's set; `valid-destinations` keeps the per-source conflict, as at
`a9fd4415` (its heaviest polls' base there 28,167, Q-W8 rc 0). Probes of the first 84 M sys cycles, median
`maap_mbx:poll`: `answering-every-port` 5,235 (a9fd4415 7,118, #810 4,804), arm A 5,373 (7,283), `valid-destinations`
7,918 (7,981). A first candidate let either interface's poll write the in-flight high word: `talker-sid-opens-before-
its-high-word` then escaped at 2if (the other interface wrote the high word before the early-marked gate could open), so
the high word is written only by its own interface's poll; all 5 SID plants caught at both points after (r3/plantsP).
Also: `talker-sid-unwritten-at-start` and the srptx arm plant `(void)id; (void)k;` (`k` no longer used otherwise).
Images (ledger/P, worktree = `cd863d40`'s firmware; platform rows reused from N): fixture 8x8/2if 124,568 / 113,216
(58.5, 360 B left); `answering-every-port` 124,876 / 113,280 (58.5, 52 B left); `valid-destinations` 124,728 /
113,232 (58.5, 200 B left); 1x1/1if 109,984 / 45,952; 1x1/2if 111,920 / 57,360; 8x8/1if 122,688 / 87,056.

**Found on the way: the names patch drops coverage.** `fw_coverage.py --check` at `a9fd4415`: `aecp_nvm.c` branches
89/90 below the recorded 88/88: `aecp_nvm.c:155` `if (r->type == type && at < r->count)`, the arc "type matches, index
past the run" never taken. Fixed by a test (`cf5b1441`): a type-5 name change at the index just past its last run (from
the fixture's own runs) queues nothing. Planted `at < r->count` dropped: caught by its words (round3/scripts/
nvm_plant.py, r3/nvmplant). Coverage written: `aecp_nvm.c` 113/113, 90/90; `maap_mbx.c` 161/161, 94/94.

**The second, not fixable here: the STOP.** Probes of `srp-talker-loss`'s first ~400 M sys cycles (r3/units
w1probe-*; round3/... trace/buildone.py), its first build-one pass (sys 327.5 M): round 2 `17ac263f` 35,270; the
sync merge `cd6d79b6` **45,339**; `f1f21546` 46,528; `a9fd4415` 45,566; the fix 45,204. So it is the merge's, before
any round 3 firmware. Committed-PC traces of that pass (round 2 and the fix, 12,000 PCs, r3/trace/stalls.py): 6,795 vs
6,798 commits, 129 vs 130 instruction refills, waits 38,405 vs 28,468, the extra spread over `mrp_transmit`, `forward`,
`declare_sources`, `transmit`, `deliver_event_changed`, `reg_event`, several at stack loads and stores. Layout: round 2
and the merge place `image_arena`, `image_srp` and `image_app` at the same addresses; #810's `nvm_stage` (+110 B) and
the store's `nvm` (552 B) move `_ebss`, so the 8 KiB stack, 368 B (about 6 sets) against SRP's objects. The bound is
`CTRL_LOOP_BUILD_ONE_PASS_US` (ctrl_loop.h, #810/#665's: the heaviest over every group of its arms plus 5 %); this arm
is #895's and not in that set. Closing it needs a bound change or a stack-placement decision: neither is this lane's.

## Items (round 3 assignment)

| Item | What | State | Commit | Evidence |
|---|---|---|---|---|
| 1 | sync: one merge of #810's head `084cf7a8` | done; boots at the merge PASS at 1x1/1if, 8x8/1if, 8x8/2if | `cd6d79b6` | section 1, receipts/boot |
| 2 | #905: SRC_SID before DA_GATE | done (firmware, 4 tests at 3 points, 5 plants at 2 points, coverage, sim check + 2 plants) | `3496eaa3`, `1aa59f75`, `99b71b44` | section 2 |
| 3 | R835-2 RS1, R836-2 RS1 | RS1 (R835-2) done `fa3f31ee`; RS1 (R836-2) in PR-BODY.md (the comment it names may not be edited) | `fa3f31ee` | |
| 4 | acceptance 4 at the new head; ROM ledger | 1x1/1if load HELD 0.503/0.501; **cap NOT held at 8x8/2if**: STOP | | section 4, receipts/graders, receipts/ledger |
| 5 | gates; full pass once; PR-BODY.md | gate pass not run (STOP); PR-BODY.md for round 3 | | |

**Decision taken (14:4x):** the cap STOP is item 4's; items 1-3 do not depend on it, so they are completed as local
commits and the ROM ledger measured at their head, so the STOP states what the S2b names patch must recover. No
bound, cap or ceiling changed. The full gate pass (item 5) is not run, and no harness leg (the arm cannot build at
8x8/2if, and the names patch moves the layout again).

## 1. The sync merge `cd6d79b6` (parents `18300f6e`, `084cf7a8`; merge base `b2d39235`)

Submodule pins identical on both sides (protocol-processor `a9e84b66`, gptp-processor `135afd04`, lwSRP `08ee86e8`,
tsn-c-stack `715589c1`, verilog-axis `48ff7a7e`). 149 files from #810; #810 does not touch `srp_mbx.c` but changes
the hot list and `ctrl_split.ld` (`nvm_any` out), so the hot layout moved under the merge.

8 conflicted files (the same 8 as the bench lane's merge 1). Scripts: round3/scripts/resolve_hunks.py (per hunk:
ours, theirs or composed text, the specs res-*.json), resolve_load_grade.py.

| File | Hunks | Resolution |
|---|---:|---|
| `tb/verilator/ctrl_service_budget/load_grade.py` | 3 | `STATED_US`, `STATED_US_DONOR`: each cost the larger of the two sides' (both define each cost as "the larger of that measurement and this table's"); 24 keys differ; table values identical to the bench lane's merge `8d95e569`. Comments: #810's, with #895's sentence appended and "on their merge each cost is the larger of the two sides' (#895)" (the bench lane's comment carried a scratch label; not reused). Not re-measured on this head's legs (STOP) |
| `sw/litex/ctrl_memory.py` | 1 | stage 13,594 (#810), entries 58.5 / 60.0 (both), `ctrl_plat` 20,352 (#895: +64 B; #810 leaves it 20,288), reasons #810's with "SRP's Talker declarations plan within it (#895)" / "ctrl_plat 64 B more with SRP's Talker declarations (#895)" |
| `sw/litex/ctrl_memory_ledger.py` | 1 | #810's docstring (a superset) |
| `sw/litex/test_ctrl_memory.py` | 1 | #810's `ledger_elf` (two tiles of .text, reaches 61.0, past 60.5: #895's purpose too) |
| `sw/firmware/gtest/coverage.ratchet` | 1 | `srp_mbx.c` #895's (725/725, 651/651; #810 does not change it), `nvm_klj2.c`, `nvm_store.c` #810's |
| `docs/design/SPLIT_CONTROL_MEMORY.md` | 6 | 1: ledger rows 13,594 + 20,352, #810's four paragraphs, plus one #895 sentence; 2: #895's table and paragraph kept as "at #895's round 2 head (`18300f6e`)", in the past tense, then #810's three lines ("Before #895, " on the first); 3-6: #810's (section 6 note; section 13 figures, which #895 changed only as figures) |
| `sw/firmware/ctrl/plat/README.md` | 2 | #810's text, with the platform image "60.0 RAMB36 with SRP's Talker declarations (#895)" and the 16,384 B cold-code move |
| `tb/verilator/ctrl_service_budget/README.md` | 2 | #810's (a superset) |

Split boot at the merge (clean clone, 3 units): 1x1/1if ready 26.276 ms, 8x8/1if 65.007 ms, 8x8/2if 67.062 ms, each
banners 1, `ctrl_split_boot: PASS (0 finding(s))` (receipts/boot/merge-*.log). At the final head: pending.

## 2. #905

- **Owner and source of the ID.** DA_GATE's owner is the MAAP adapter (`maap_mbx.c`), so it writes SRC_SID. The value
  is the declaration owner's source port (`acmp->env->source`, the port `acmp_declaring` reads; in the platform
  `ctrl_plat.c` `stream_id()` = entity MAC << 16 | the output's unique ID, the value SRP's Talker and GET_TX_STATE
  carry). No literal.
- **Writer:** `mbx.c:255` `mbx_pub_src_sid(interface, source, high, word)`, one write; refuses an interface or a source
  past the contract's (D14 cases in `test_unit_driver.cpp`).
- **When (final design, `3496eaa3`):** `maap_mbx_start` (`maap_mbx.c:243-256`) writes every source's two words before
  any pass and any DA_GATE bit (so before any declaration or PROBE_TX response, KL_mbx_pkg.sv:345) and marks it
  written. `declaring` (`:52-71`) lets a closed source open only with that mark (`may = gate & (published |
  written)`), spends the mark of each source it lets open, and leaves the rest in `sid_wait`; the poll (`:220-225`),
  in a poll that writes no gate, calls `publish_sid` (`:85-105`): one word a poll, the low word first, read from the
  port at the low word; the high word sets the mark; the poll reports work owed meanwhile. So each reopening is
  preceded by both words, read from the port just before. `range` is untouched.
- **First design (`e9011df6`), replaced:** rewrite after each closing plus a cached comparison at each opening;
  896 to 1,056 B of rom and 144 B of sram. The final design: 600 to 744 B of rom, 0 to 32 B of sram (section 4).
- **Bounds unchanged:** the MAAP poll's one publication write is "a changed gate, or else one SRC_SID word"
  (`maap_mbx.h:15-19`, README "Service evidence"); `MAAP_MBX_*_MAX` and every composed pass bound keep their values;
  `range` and the event path write no SRC_SID and do not read the port (the pinned rule: no source query inside a
  MAAP callback). The 47-access allocation count (`CallbackWorkAndEveryOutputCount`) is unchanged.
- **Stated limits:** a source's first opening carries the start's stream_id; a stream_id the port changes while the
  gate stays open is written before the next reopening. The platform's stream_id never changes.
- **Kept anchors:** `range`'s three lines (gate, DA_GATE write, report) unchanged: `ctrl_mutants.py:675,861`,
  `maap_gate_mutants.py:16` and `ctrl_service_hooks/hooks.py:247` plant on them (round3/scripts/anchors.py against
  the merge: 0 broken).
- **Tests** (`srp_gate.hpp`, SrpGate; run at 1x1/1if, 1x1/2if and 8x8/2if; ACMP's port set to the declared ID):
  `F905AEachSourceStreamIdIsWrittenBeforeItsGateOpens`, `F905AStreamIdChangedWhileClosedIsWrittenBeforeTheGateReopens`,
  `F905AGateReopensOnlyOnceItsStreamIdIsWrittenAgain`, `F905ARangeLostClosesTheGateUntilItsStreamIdIsWrittenAgain`
  (a publication-write history from the model's reset: the SRC_SID at each opening, no word written while open, both
  words again between closing and reopening).
- **Plants** (`srp_talker_mutants.py`, 34 = 29 + 5), each caught by its test's words at 8x8/2if and 1x1/1if
  (receipts/plants/talker-sid-worktree.log):

| Plant | Mutation | Test | Failing words |
|---|---|---|---|
| `talker-sid-unwritten-at-start` | start writes no SRC_SID (gate before SID) | `...WrittenBeforeItsGateOpens` | SRC_SID holds the source's stream_id when its DA_GATE bit opens |
| `talker-sid-words-swapped` | HI/LO registers swapped (`mbx.c`) | same | SRC_SID_LO holds the stream_id's low word and SRC_SID_HI its high word |
| `talker-sid-never-held` | a closed source opens with no rewrite (stale SID after a change) | `...ChangedWhileClosed...` | SRC_SID holds the source's stream_id when its DA_GATE bit opens |
| `talker-sid-opens-before-its-high-word` | the mark set at the low word (gate before SID) | `...ReopensOnlyOnce...` | SRC_SID is written only while the source's DA_GATE bit is clear |
| `talker-sid-written-mark-kept` | the opening spends no mark | same | both SRC_SID words are written again between the bit's closing and its reopening |

- **Coverage:** `fw_coverage.py --write` (refuses a drop): `maap_mbx.c` 158/158, 92/92; `mbx.c` 365/365, 186/186.
- **Arms on the worktree at `3496eaa3`:** maap, maap_if2, maap_debug, acmp, acmpif2, srp test_acmp_mbx if1/if2 (76
  tests), talker arms (srp_talker both points, SrpGate 8x8/2if 7 tests), platboot if1/if2, unit: all PASS (plat,
  platrv32, plattrace, rv32, hot, service_bounds PASS at `e9011df6`; to re-run at the head).
- **Simulation check** (`1aa59f75`): `srptx_grade.py` `[SID]`, the licence scenario on the twin's split half (the
  platform firmware on KL_mbx + milan_datapath, 1x1/1if): a stream leaves and every stream frame's AVTPDU stream_id
  is one the split's own Talker Advertise declares.
  - head (`1aa59f75` clone): 119 stream frames, all `0200000000010000` = the declared ID; no `[SID]` finding.
  - #810's head `084cf7a8` (its own firmware, no SRC_SID writer) graded by the head's grader: `[SID] 119 stream
    frame(s), ms 3161 to 20952, carry stream_id 0000000000000000, which no Talker Advertise the split declared
    carries (0200000000010000)`: the check refuses the real defect.
  - capture plant `stream-id-unwritten` (srptx_plants.py): refused by its words on the head's licence capture.
    `srptx_plants.py` itself stopped before it: the hold scenario's `backpressure-unseen` escaped and
    `refused-with-room` raised StopIteration (no refusal in the hold capture since #895, below).
  - code arm "no source's SRC_SID written (#905)" (srptx_mutants.py): its clean control is refused by `[TIME]`, so it
    ran by hand (round3/scripts/arm905.py, the script's own build() and run()): REFUSED by `[SID] 119 stream frame(s)
    ... carry stream_id 0000000000000000`; the unplanted capture 0 `[SID]`. Its first planted line `(void)k;` did not
    compile (-Werror, unused `id`): fixed `99b71b44`.
  - srptx hold `[TX]`: at the merge and the head, not at `084cf7a8` (receipts/srptx/*-hold-report.json): 176 MRPDUs,
    no refusal; the base refused a 30-word MSRP record at 507 of 512 words. Cause read: #895 removed the boot-time
    Talker Failed, so the MSRP MRPDUs are smaller and the 3 s hold no longer fills the ring. A test-coverage
    regression of srptx's retention path, for its own issue (newly found work, not fixed here).
  - **Found, pre-existing, not this lane's:** every srptx scenario reports `[TIME]` findings (a "requested"
    MSRP/MVRP transmit opportunity at each whole second, 400 to 800 ms after lwSRP's last idle poll): 47 on the
    licence scenario at #810's head `084cf7a8`, 45 at this head. The suite README's "every scenario grades with no
    finding" is #867's head's. So `make srptx`, `srptx-plants` (its controls) and `srptx-mutants` (its clean control)
    fail at #810's head already. For the manager: a separate issue (srptx's `[TIME]` attribution against the SRP
    transmit scheduling #810 merged after #867).

## 4. Acceptance 4 and the ROM ledger

Graders (analytical, the composed tables; not re-measured on this head's legs) at #810's head `084cf7a8` and at the
head (receipts/graders, clean clones):

| Point | Figure | Bound | Base `084cf7a8` | Head | Delta |
|---|---|---|---:|---:|---:|
| 1x1/1if | load at the pin / with tsn-c-stack#32 | <= 0.70 | 0.501 / 0.499 | **0.503 / 0.501 (HELD)** | +0.002 / +0.002 |
| 1x1/1if | R4 / R5 / R6 | 20 / 90 / 90 ms | 74.83 / 38.25 / 33.65 | 75.39 / 38.47 / 33.87 | +0.56 / +0.22 / +0.22 |
| 1x1/1if | first / last notice | 20 / 125 ms | 20.00 / 22.00 | 20.00 / 22.00 | 0 |
| 8x8/2if | load at the pin / with #32 | 0.75 (#890) | 0.822 / 0.770 | 0.823 / 0.771 | +0.001 / +0.001 |
| 8x8/2if | R4 / R5 / R6 | 20 / 90 / 90 ms | 377.98 / 148.68 / 139.23 | 378.94 / 148.98 / 139.51 | +0.96 / +0.30 / +0.28 |
| 8x8/2if | first / last notice | 20 / 125 ms | 22.00 / 62.00 | 22.00 / 62.00 | 0 |
| both | pass own cost | | 230, 355 us | 230, 355 us | 0 |

ROM (RV32 images linked on each shape's own split export and runtime, plat_ledger.py's; receipts/ledger):

| 8x8/2if image | cap | base `084cf7a8` | merge `cd6d79b6` | head `3496eaa3` |
|---|---:|---|---|---|
| fixture | 58.5 | 123,808 / 113,168, 58.5 | 124,832 / 113,216, 58.5 (96 B rom left) | **125,576 / 113,232: 59.0, refused** (648 B past 124,928) |
| harness arm `answering-every-port` | 58.5 | 124,116 / 113,232, 58.5 | **125,140 / 113,280: 59.0, refused** (212 B past) | 125,884 / 113,296: 59.0, refused (956 B past) |
| harness arm `valid-destinations` | 58.5 | (none at the base) | **124,992 / 113,216: 59.0, refused** (64 B past) | 125,736 / 113,248: 59.0, refused (808 B past) |
| platform | 60.5 (plans 60.0) | 128,960 / 114,160, 59.5 | 129,984 / 114,224, 60.0 | 130,728 / 114,224, 60.0 |

Other points at the head: fixture 1x1/1if 38.5, 1x1/2if 42.0, 8x8/1if 52.0; platform 40.0, 43.5, 53.0 (all <= 56).
`ctrl_plat` at the head: 17,536, 19,072, 18,176, 20,352 B, as at the merge (the 13 B an interface fit the padding;
the first design's `sid[]` cache made them 17,664 to 20,480 and failed plat_ledger's KEY): `plat_ledger.py` PASS.
#905's text at 1x1/1if: 604 B (publish_sid 192, maap_mbx_start +172, stream_of 96, mbx_pub_src_sid 60, declaring
+36, poll +32, request +16 from a field moved past a load's reach); sram +16 B there, 0 to 32 B an image.

Final head checks (clean clone Z at `f1f21546`): 19 arms PASS (receipts/fw/arms-final-clone.log); boots PASS at
1x1/1if 26.278 ms, 8x8/1if 65.118, 8x8/2if 67.208 (receipts/boot/head-*); graders identical to `fa3f31ee`'s
(receipts/graders/final-*); `git diff --check 084cf7a8..f1f21546` clean.

## Run history

- 14:04 assignment read; skeleton written. 14:05-14:12 #905, the bench report (round 4), R835-2, R836-2 read.
- 14:12 fetched: #810 `084cf7a8`, not in dev-soft-core. Merge; 8 conflicts resolved; committed `cd6d79b6`.
- 14:3x cap probe at the merge (round3/scripts/cap_probe.py): the arm refused at 59.0 (receipts/cap).
- 14:4x-15:00 #905 design; tests; plants; coverage; `e9011df6`.
- 15:22 boots at the merge (3 units): PASS. 15:22 srptx on `e9011df6`: `[SID]` clean; `[TIME]` findings.
- 15:24 ledgers at base, merge, head (3 units). 15:25 graders at base and head.
- 15:30-15:40 the first design's cost (896 to 1,056 B rom) led to the final design `3496eaa3` (600 to 744 B).
- 15:41 srptx at #810's head: 47 `[TIME]` findings, stream_id 0 on every frame: `[TIME]` pre-existing.
- 15:44 the code arm's planted line did not compile (-Werror, unused `id`): fixed `99b71b44`; 15:45 the arm by hand:
  refused by `[SID]`. 15:46 the capture plant: refused. 15:47 hold at the base (no `[TX]`) and the merge (`[TX]`).
- 15:47-15:52 the final firmware's ledger: plat_ledger PASS, `ctrl_plat` unchanged. 15:53 docs `f1f21546`.
- 15:55 boots at `f1f21546` (3 units): PASS. 15:56-16:01 the control campaign cut to 80 MAAP-reachable mutants: 80
  caught (its 68 "no defect names the test" lines are the cut's own artifact: the unnamed-test check reads the cut
  table). 16:00-16:07 19 arms on the final clone: PASS. 16:08 the full firmware suite on the final clone (unit
  `fwsuite`).
- A receipt-tidying command that deleted two oversized logs from the output directory was refused by the harness; the
  logs were moved back to scratch instead (kept), summaries written, hashes in receipts/srptx/large.sha256.
- CPU: 0-95 mostly booked by other lanes; units picked 8-wide ranges as they freed. Units of this round (all
  `milan-895-a775-r3-*`, transient, collected): bootM-*, srptx, ledger-B/M/H/F, srptxM, srptxB, srptxBhold, srptxF,
  arm905 (twice), bootZ-*, fwsuite.
- 16:22 the full firmware suite on the final clone: 71 arms, PASS, tree clean after (receipts/fw). #810 re-read:
  `084cf7a8`, open. Receipts scrubbed, then INDEX.md generated (54 files). 16:2x STOP posted once on #895
  (issuecomment-6857286369). No unit of this lane runs.
- 16:25 RESUME check (the session was told the host restarted; uptime showed no reboot since the round began):
  worktree clean at `f1f21546`, no round-3 unit running, all 17 units left their rc (none killed); one STOP
  comment on #895 (issuecomment-6857286369), its body equal to STOP-COMMENT.md; receipts match INDEX.md (54
  files, 0 mismatched). Nothing re-run, nothing posted again.
- 16:27 RESUMED by the ruling 6857334948: (a) `a9fd4415` (names patch, unchanged); (b) every 8x8/2if image 58.5;
  legs `Q-*` on `a9fd4415` (clone N) 16:30 on.
- 17:25 Q-N8 rc 1 (polls' base 32,597 > 32,500). 17:4x Q-A8 parts 3-4 stopped by me (their units listed first) to free
  CPUs; committed-PC traces of the heaviest pass at the head and #810's image (units trace-N, trace-M): a data cache
  conflict (section (d)). 17:48 Q-W1 rc 1 (build-one 46,367 > 43,000).
- 18:0x the 8-B candidate (worktree); fixtures (ledger/P1); unit arms PASS; probes P-N8/W8/A8 (5.5 min each);
  W1 probes at M, Z, P (16 min each): the build-one overrun is the merge's. Coverage check: the names patch's
  `aecp_nvm.c` drop (89/90). 18:3x-18:4x W1 traces (trace-w1P, trace-w1R; stopped by me after their 12,000 PCs,
  units listed first): data-side waits, the stack moved 368 B by #810's `.bss`.
- 18:4x the SID plants on the first candidate: `talker-sid-opens-before-its-high-word` escaped at 2if and
  `talker-sid-unwritten-at-start` did not compile; fixed (`sid_owed`, `(void)k;`); all 5 caught (plantsP2); MAAP
  campaign 80 of 80; arms PASS; coverage written; the names-runs test and its plant (nvm_plant.py) PASS.
- 18:5x commits `cd863d40`, `cf5b1441`; clone r3/S; legs `S-*` 18:59 on (legs_s.sh; arm A in parts, tick.sh);
  clone r3/S2 for the head checks: ledger PASS, boots PASS (3), srptx licence/hold (no [SID]; #906, #907), arm905 REFUSED.
- 20:3x `9e30c2c3` (docs: section 5 at the head, section 9 "Where the stack falls in it", milan_dp README #906/#907).
  S-B1, S-B8, S-N1, S-N8, S-W8, S-A1 (merged) rc 0; S-W1 rc 1 (the STOP's four build-one passes).

## At the head `9e30c2c3` (firmware `cf5b1441`): what ran and where

| What | Result | Receipt |
|---|---|---|
| Legs S-* (clean clone r3/S; legs_s.sh, tick.sh, parts as Q-*'s splits) | A1 (merged) 94 groups, 7 of 945; A8 (merged) 93, 7 of 996; N1 0 of 280; N8 0 of 736, polls' base 31,030; W8 0 of 20, base 29,093; B1, B8 0; **W1 rc 1: 4 build-one STATED (45,452-46,489 > 43,000)**; no pass over the share | receipts/legs |
| Feed (feed4.sh: costs.sh at both points, tables895.py, least_margin.py) | tables move event.AECP, event.MAAP, record.maap, the donor column's base (8x8) and build_one/item.mrpdu (1x1, 430 -> 490); least margins all positive | receipts/graders/head-cf5b1441-* |
| load_grade / flip_grade on the fed tables (S2's copy, updated in place, restored after) | load rc 0: 1x1/1if 0.503 / 0.502; 8x8/2if 0.825 / 0.773; flip rc 1, the base's OVER set | receipts/graders/head-cf5b1441-*-fed.log |
| Ledger (ledger.sh on clean clone r3/S2) | plat_ledger PASS; fixture 8x8/2if 124,568 / 113,216 (58.5), arms 124,876 and 124,728 (58.5) | receipts/ledger/cf5b1441-* |
| Boots (S2) | 26.299 / 65.016 / 67.085 ms, PASS (0 findings) | receipts/boot/head-cf5b1441-* |
| srptx (S2, make -k licence hold) | licence 119 frames `0200000000010000`, no [SID]; 45 [TIME] (#906); hold [TX] (#907); arm905: REFUSED by [SID] | receipts/srptx/cf5b1441-*, arm905-cf5b1441.log |
| Firmware arms, plants, coverage (worktree = cd863d40's firmware) | arms PASS; SID plants 5/5 at both points; MAAP campaign 80/80; nvm plant caught; coverage written | receipts/fw, receipts/plants |
| Full firmware suite (S2) | 79 results PASS, 0 FAIL, the tree clean after | receipts/fw/full-suite-cf5b1441.log |
| Trace analyses | the N8 conflict (calls, spans, dloop) and the W1 build-one (early passes at 6 commits, stalls, layout) | receipts/trace |

Scratch kept (not receipts, over 200 KB): r3/units/trace-{N,M,w1P,w1R}.log (committed-PC traces), r3/trace/*.dis.
- 21:5x the full firmware suite at `cf5b1441` (S2): 79 PASS, 0 FAIL, tree clean. Receipts copied and scrubbed,
  INDEX.md generated (119 files). STOP posted once on #895: issuecomment-6864607963 (its body equal to
  STOP-COMMENT-2.md). No unit of this lane runs; nothing pushed (the remote branch stays at `18300f6e`).
