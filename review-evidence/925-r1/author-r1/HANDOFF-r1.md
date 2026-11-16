# HANDOFF — lane 925 ([A790]), round 1

**Status (07:1x CET 2026-11-16): STOP posted once on #925 (issuecomment-6908790238, STOP-COMMENT.md): both split
images miss the +0.030 ns floor on all three directives (by 6 to 22 ps); the base's own 1x1/1if image misses it too.**
The fix, tests and plants are done (`95426618`); head `1be0a6c4`, not pushed. Awaiting the manager's decision on
the routes. Everything else is green (section 4).

Assignment: #925 (part of #665), finding 18 of the replica report (#665 issuecomment-6904803181), the manager decision
#665 issuecomment-6904832963. Branch `925-srp-ta-tf` at #901's review head `16ba667d` (clean, submodules initialised).

## 1. Step 1 report (written before any change)

**The split listener path at `16ba667d`** (`sw/firmware/ctrl/srp/srp_mbx.c`; finding 18's `:711-724` is the image
commit's numbering, the same code is at `:844-859` and `:353` here):
- Talker indications `advertised` :209, `failed` :216, `left` :223 call `talker_changed` :194, which clears the kind's
  bit of each bound sink with that StreamID and sets it again when registered with the sink's destination and VID
  (`registered_kinds`: bit 0 Failed, bit 1 Advertise).
- The receive filter `interested_msrp` :350-355 (called before each attribute, so it sees the previous complete
  event) sets `desired = (kinds & 1) ? 1 : (kinds & 2)`: **Failed first**.
- The registrar walk `snapshot` :875 / `registrations` :844-859: a registered Failed sets `desired = 1` and an
  Advertise sets 2 only `if (sink->desired != 1)`: **Failed first** again.
- `desired` decides the Listener declaration (`prepare_declarations` :958-993: 1 AskingFailed, 2 Ready once the VLAN
  commits, their union ReadyFailed) and, through `capture` :865 / `feedback_kind`, the kind ACMP sees
  (`ctrl_app_srp.c:96-104`: `acmp_tk_registered` / `acmp_tk_kind_changed`, GET_RX_STATE's REGISTERING_FAILED).
- The README states the rule: `sw/firmware/ctrl/srp/README.md:468-469` "conflicting New registrations retain Failed
  precedence until replacement/expiry".

**lwSRP (`08ee86e8`, read only)**:
- `rx_on_attr` (`src/core/mrp_mad.c:1026-1047`) withdraws a registered Talker of the other type with the same StreamID
  (`msrp_attr_replaces`, `src/modules/msrp.c:391-396`) **only on a received JoinIn/JoinMt**; "New conflicts are left
  to the application's declared precedence rule" (`:1028`; `doc/developer.md` "Conflicting New registrations remain
  distinguishable for host precedence policy").
- Registrar (`mrp_mad.c:347-364`, `:674-682`): rNew in IN, LV or MT goes IN with New! (`join_ind`, is_new true);
  rJoinIn/rJoinMt in IN or LV gives no indication (unless the value changed), in MT Join!. Built `LWSRP_MILAN=1`:
  IN/rLv gives Lv! and MT at once (Milan v1.2 4.2.7.2.2).
- So a Talker Advertise New over a registered Talker Failed leaves both registered, and the adapter's Failed-first
  rule holds Asking Failed until the talker's next MRPDU (its Advertise JoinIn replaces the Failed, or the Failed's
  Lv removes it): the bench's 2.1 s.
- **The fix belongs in the adapter, not lwSRP**: lwSRP leaves exactly this case to the host by design. No STOP.

**The release's processor** (`protocol-processor/hdl/srp/KL_srp_listener_fsm.sv:1145-1151`): one registrar per sink
whose type `rtype_r` every registering event (New, JoinIn, JoinMt) of either kind sets, "the in-place
Advertise<->Failed swap ... 802.1Q §35.2.6": the most recent registering event decides. (It also withdraws on a Lv of
either type, `:1171-1176`; not carried over.)

**IEEE 802.1Q-2018**: the standard's text is not on this host or in the tree. Read through the tree's citations: 35.2.4
(the issue's: a talker declares one of the two Talker attributes for a stream), 35.2.6 (lwSRP's `doc/manager.md:37`
and the processor's reading: a Talker registration of the other type replaces the one held, atomically in event
order), 35.2.2.8 (one FirstValue per StreamID: the hold-off, untouched here), 35.2.2.7.2 (Listener declaration types).

**The rule to implement**: per bound sink, the most recently registered (Join or New indicated) of the two kinds decides
the Listener declaration and the kind ACMP sees; when the latest is not registered, the remaining one decides; a
binding that saw neither indication (bound after both registered) keeps Failed first. Every registration lwSRP holds
was indicated (MT->IN always indicates), so the event order is complete for a sink bound before them.

## 2. Changes (file:line at `a9f0dbc0`, reason)

Commits on `16ba667d`: `95426618` (the fix, its tests and plants, the SRP README), `a9f0dbc0` (the ledger record).

- `sw/firmware/ctrl/srp/srp_mbx.h:33-35` `srp_sink.latest_kind`: the kind (bit 0 Failed, bit 1 Advertise) of the
  StreamID's latest Talker registration indicated while bound. The registrar walk carries no order; only lwSRP's
  indications do (New! on rNew in every state, Join! on MT->IN), so the adapter records it.
- `srp_mbx.c:192-201` `listener_kind`: while both kinds are registered the latest decides; when the latest is not
  registered the remaining one decides; a binding that saw neither (latest 0) keeps Failed first. 802.1Q-2018 35.2.4,
  35.2.6, 35.2.2.7.2 in the comment.
- `srp_mbx.c:213-215` `talker_changed`: every bound binding of the StreamID records the latest registration, whatever
  its destination and VID, so a later binding can take it from any of them.
- `srp_mbx.c:367` the receive filter (`interested_msrp`) and `:905` the walk's end (`snapshot`) compute `desired`
  with `listener_kind` (both were Failed first); `registrations` `:864-868` only accumulates the kinds now.
- `srp_mbx.c:622-624` `srp_mbx_bind`: a new binding takes `latest_kind` from a bound binding of the same StreamID.
- `sw/firmware/ctrl/srp/README.md:244-258` the rule with its clauses; `:483-484` the processor comparison's line
  ("conflicting New registrations retain Failed precedence" replaced: the latest decides, as the processor's swap).
- `sw/firmware/ctrl/test/srp_mbx.cpp:1410-1418` the registrar-walk reference model (`HeldRegistrations...`) follows
  the new rule (it was Failed first; no step of that test registers both kinds, so its verdicts are unchanged).
- `sw/firmware/ctrl/test/srp_mutants.py` the existing plant `failed-listener-ready` moved to its new site (the walk's
  Failed now maps in `listener_kind`); same test, same needle; imports `srp_kind_mutants`.
- `sw/litex/ctrl_memory_ledger.py:35`, `sw/litex/ctrl_memory.py:266-277`, `docs/design/SPLIT_CONTROL_MEMORY.md:138,
  147`: `ctrl_plat` at 8x8/2if 20,352 -> 20,416 B (the field's 2 B a sink, padded), the same 60.5 RAMB36; no other
  point's `ctrl_plat` changes.
- Not changed: any SRP timer or bound, lwSRP, the mailbox contract, RTL, ACMP's interface (it reads the same
  `desired`/`feedback_kind`, which now follow the rule).

## 3. New checks, their planted mutants and failing words

Tests (`srp_mbx.cpp` fixture `SrpTalkerKinds` :1807-1956; `srp_feedback.hpp` :112-148), all at 1x1/1if and 2if
(gate arms) and 8x8/2if (dev run):

| Test | Holds |
|---|---|
| `SrpTalkerKinds.AnAdvertiseNewReplacesARegisteredFailedWithinAJoinTime` | finding 18: TF JoinIn -> AskingFailed within a JoinTime; TA New -> Ready within a JoinTime, no later MRPDU, both still registered |
| `SrpTalkerKinds.AFailedNewReplacesARegisteredAdvertiseWithinAJoinTime` | the reverse |
| `SrpTalkerKinds.LeaveOfEitherKindLeavesTheOtherDeciding` | both orders: the latest's Lv hands the declaration to the other, its Lv withdraws; the older's Lv changes nothing on the wire |
| `SrpTalkerKinds.CoincidentRegistrationsInOneMrpduFollowTheirOrder` | one MRPDU TF New + TA New -> Ready, TA New + TF New -> AskingFailed; TA New + TF Lv in one MRPDU continuous |
| `SrpTalkerKinds.ABindingMadeLaterTakesTheLatestFromAnyBindingOfTheStream` | a second binding (same and other destination) takes the latest: Ready, not ReadyFailed |
| `SrpTalkerKinds.ABindingThatSawNeitherRegistrationTakesFailedFirst` | the documented fallback, then the talker's JoinIn replaces |
| `SrpFeedback.AdvertiseNewOverARegisteredFailedUpdatesTheSettledWireView` | ACMP and GET_RX_STATE follow: Advertise at the New, Failed at its Lv, reprobe at the Failed's Lv |
| `SrpFeedback.AWithdrawalInsideOneMrpduRetainsTheLatestKind` | the receive filter's copy: ACMP never sees Failed before an intra-MRPDU withdrawal |

Plants (`sw/firmware/ctrl/test/srp_kind_mutants.py`, each caught by name at both interface counts, dev run
`plants-if2`, `plants-if1`, `plants-if2b`; the gate campaigns re-run them):

| Plant | Test | Failing words |
|---|---|---|
| feedback-latest-failed-first (the pre-fix rule) | AnAdvertiseNew... | "an Advertise New replaces the registered Failed" |
| feedback-latest-walk-failed-first | AnAdvertiseNew... | same |
| feedback-latest-advertise-only | AFailedNew... | "a Failed New replaces the registered Advertise" |
| feedback-latest-decides-unregistered | LeaveOfEither... | "the latest leaves: the other decides" |
| feedback-latest-earliest-decides | Coincident... | "Failed then Advertise in one MRPDU" |
| feedback-latest-not-carried | ABindingMadeLater... | "the shared declaration stays Ready, not ReadyFailed" |
| feedback-latest-matching-only | ABindingMadeLater... | "a later binding takes the latest registration" |
| feedback-latest-unknown-advertise | ABindingThatSawNeither... | "neither registration seen: Failed first" |
| feedback-latest-filter-failed-first | SrpFeedback.AWithdrawalInsideOneMrpdu... | "the latest kind precedes the withdrawal" |
| feedback-latest-acmp-failed-first | SrpFeedback.AdvertiseNewOver... | "current kind reaches ACMP" |
| failed-listener-ready (moved) | SinkPortUsesMatching... | "declared" |

Pre-existing, not this change: `srp_mbx.cpp` at the 8x8 entity (a shape no gate runs that suite at) fails
`StartupDeclaresTalkersDomainAndVlan` and `OneLoopOwnsTheGlobalCentisecondDispatch` at `16ba667d` too.

## 4. Gate table (clean clones)

Heads: `a9f0dbc0` (the image's head) and `1be0a6c4` (= `a9f0dbc0` + a plant's line wrapped to 120 columns and
srp_mbx.c's ratchet counts; no image input).

| Gate | Head | Result | Receipt |
|---|---|---|---|
| test_ctrl_firmware --require-rv32 --self-test --shard 0/4 (suites) | a9f0dbc0 | rc 0, PASS (SRP arm 80 checks at if1) | firmware/fw0.log |
| shard 1/4 (control mutants) | a9f0dbc0 | rc 0, 716 of 716 caught | (log 96 KB, in scratch) |
| shard 2/4 (AECP mutants) | a9f0dbc0 | rc 0, 299 ok, 0 escaped | firmware/fw2.log |
| shard 3/4 (SRP mutants both counts, lwSRP pin) | a9f0dbc0 | rc 0, 441 ok (421 + the 10 new at both counts), 0 escaped | firmware/fw3.log |
| shard 3/4 again | 1be0a6c4 | rc 0, 441 ok, 0 escaped | (scratch units/fw3b.log) |
| fw_coverage --check | a9f0dbc0 | rc 0, PASS (39 files); srp_mbx.c 741/741, 671/671 after its 3 exclusions | firmware/cov.log |
| fw_coverage --write (scratch, to read the counts) | a9f0dbc0 | srp_mbx.c 741/741 671/671; also rewrites aecp_commands.c, aecp_face.c, aecp_maps.c, stale at the base (not this change; not taken) | |
| plat_ledger.py | worktree = a9f0dbc0 | rc 0, every point PASS | ledger/ |
| test_ctrl_memory.py | worktree = a9f0dbc0 | rc 0 | |
| rtl-fast replay: changes, verilator-lint, bdd-conformance, yosys-tool, yosys-elaboration, publication-census, split-cdc, firmware-boundary, firmware-verilator, ci-* | a9f0dbc0 | every job failed 0 | workflows/ |
| rtl-fast replay: firmware-unit (shard 0, ctrl_nvm, coverage selftest and check) | a9f0dbc0 | failed 0 | workflows/ |
| elaborate replay: elaborate-gates-0, -1, elaborate, ci-* | a9f0dbc0 | failed 0 (gates-0 re-run once: its first run lacked the replay HOME's SDK link, an environment fault) | workflows/ |
| docs replay: every job | a9f0dbc0 | failed 0 but docs-gates-0's Python idiom gate (srp_kind_mutants.py:50, 121 columns), fixed in 1be0a6c4 | workflows/ |
| docs replay: every job | 1be0a6c4 | every job failed 0; verify table 61 ran, 34 reasoned, 0 bad | workflows/verify-1be0a6c4-docs.md |
| rtl-fast replay: firmware-unit, changes | 1be0a6c4 | failed 0, failed 0 | workflows/logs-1be0/ |
| Split boots 1x1, 8x8 | a9f0dbc0 | PASS, PASS | images/ |
| S9 exports 1x1/1if, 8x8/1if (identity gate) | a9f0dbc0 | rc 0, rc 0 | images/ |
| Release image (all-fabric, base vs head) | 16ba667d / a9f0dbc0 | bios.bin identical both configs; stripped ELF identical | release-image/ |
| Budget 1x1/1if (arm A, every group) | a9f0dbc0 | rc 0: 96 graded, 0 refusals, 0 of 129,813 passes over the share, 7 misses all in backlog-owed (the same 7 as #919's run), no STATED | budget/ |
| Budget 8x8/1if (arm A, every group) | a9f0dbc0 | rc 1 from STATED only: 95 graded, 0 refusals, 0 of 266,195 over the share, the same 7 backlog-owed misses; STATED: polls base (77, at most 24,499 vs 22,500), ACMP item (3, vs 5,500), declined ACMP offer (4, vs 2,000) over the one-interface statements, the shape's known excess (#894's 8x8/1if gate showed the same classes); SRP items within | budget/8x8-1if/ |
| flip_grade.py --check --point 1x1/1if | 1be0a6c4 | PASS, every row within its bound (R4 13.25/20, R5 75.84/90, R6 73.36/90, last 136.65/140, R4L 203.57/238, txL 48.58/49, ...) | budget/graders/ |
| load_grade.py --check | 1be0a6c4 | PASS, 1x1/1if 0.517 / 0.514 vs 0.70 | budget/graders/ |
| Stated costs | | none changed: at 1x1/1if every held cost within its statement, the SRP items' rule figures unchanged (walk 2,733 cycles -> 30 us, stated 35; record 25,078 -> 265, stated 280; #901's lane survey had 2,719 and 24,933); at 8x8/1if the SRP items within (walk 2,145, record 21,816) | budget/*/survey.md |
| Routes, both shapes, three directives | a9f0dbc0 | every route rc 0, none meets +0.030 at every corner (section 5) | route/ |
| Base route 1x1/1if (comparison), EPPO / ETO | 16ba667d | rc 0 / rc 0: +0.208 / +0.014 and +0.260 / +0.014 (Slow WNS / Fast WHS): misses on hold, 16 ps, the same TDM render FIFO | route/base-1x1-*/ |
| Base route 1x1/1if ASL | 16ba667d | NOT RUN: it waited for a 16-CPU range while holding a Vivado slot; stopped at 07:09 after the STOP (two base directives already show the miss) | |
| Sweep (verilator-suites, 4 shards) | | NOT RUN: it may not run beside a route, and the routes' STOP waits on a decision; the next head (after the decision and any train sync) needs it | |

## 5. Images, ROM, area, timing

ROM (plat_ledger.py, platform image; base `16ba667d` -> head): 1x1/1if 117,488 -> 117,576 B (+88), 43 RAMB36;
1x1/2if 119,072 -> 119,160 (+88), 44; 8x8/1if 130,200 -> 130,232 (+32), 56.0 (the budget, PASS); 8x8/2if 131,752 ->
131,784 (+32), 60.5 (its ledger's). sram unchanged but 8x8/2if 114,224 -> 114,288 (+64). ctrl_plat unchanged but
8x8/2if 20,352 -> 20,416 (ledger raised, same tiles).

Release image: bios.bin identical at both configs, stripped bios.elf identical (receipts/release-image/).

Routes (S9's recipe, the #919 lane's chain; route dir scratch rt/):

| Shape | Directive | rc | Slow WNS / WHS | Fast WNS / WHS | Floors (+0.030) |
|---|---|---|---|---|---|
| 1x1/1if | ExtraPostPlacementOpt (recipe) | 0 (03:29-04:00) | +0.024 / +0.092 | +1.660 / +0.036 | not met (Slow WNS) |
| 1x1/1if | ExtraTimingOpt | 0 (04:00-04:09) | +0.008 / +0.050 | +1.641 / +0.023 | not met (WNS, Fast WHS) |
| 1x1/1if | AltSpreadLogic_high | 0 (04:09-04:17) | +0.177 / +0.050 | +1.641 / +0.023 | not met (Fast WHS) |
| 8x8/1if | ExtraPostPlacementOpt (recipe) | 0 (04:17-05:01) | +0.011 / +0.070 | +1.370 / +0.034 | not met (Slow WNS) |
| 8x8/1if | ExtraTimingOpt | 0 (05:02-05:16) | +0.171 / +0.102 | +1.636 / +0.014 | not met (Fast WHS) |
| 8x8/1if | AltSpreadLogic_high | 0 (05:16-05:31) | +0.215 / +0.102 | +1.636 / +0.014 | not met (Fast WHS) |
| 1x1/1if at the base 16ba667d | ExtraPostPlacementOpt | 0 (05:31-06:06) | +0.208 / +0.051 | +1.636 / +0.014 | not met (Fast WHS) |
| 1x1/1if at the base 16ba667d | ExtraTimingOpt | 0 (06:43-06:52) | +0.260 / +0.053 | +1.636 / +0.014 | not met (Fast WHS) |
| 1x1/1if at the base 16ba667d | AltSpreadLogic_high | not run (stopped while waiting for CPUs) | | | |

1x1/1if EPPO worst setup: `KL_mbx/rd_off_r_reg[13]` -> `KL_mbx/reg_rdata_r_reg[4]` (bus clock, 16 levels), the S9
known read path. ETO/ASL worst hold: `chan_tdm_render/bank_r_reg[5][21]` -> `chan_tdm_render/u_fcdc/mem_r_reg_1`
(the TDM render FIFO's CDC BRAM write port, Fast corner); EPPO's hold +0.036 is the gPTP engine's LUTRAM. 8x8/1if
EPPO worst setup: `KL_mbx_cdc/u_edit/rq_r_reg[80]` -> `milan_datapath/amap_edit_oclaim_expect_r_reg[599]/CE`
(clkout1, 40 levels); 8x8/1if ETO/ASL worst hold: `g_aaf_meter.aaf_clock_meter/s2_ts_r_reg[6]` -> `grp_ts0_r_reg[6]`.
The base's 1x1/1if EPPO worst hold: `chan_tdm_render/bank_r_reg[6][22]` -> `u_fcdc/mem_r_reg_2/DIADI[22]` (the same
FIFO), its worst setup `KL_mbx/rd_off_r_reg[8]` -> `reg_rdata_r_reg[6]` at +0.208. Every route: 0 failing
endpoints, 0 routing errors.

Area: the base's exports (`16ba667d`, the same recipe, no Vivado) and the head's are the same netlist apart from
LiteX's comment tree (the same integrated script too); only the ROM's contents differ: 1x1/1if `rom_bank3` 700 ->
722 words in its bank, banks 0-2 their contents; 8x8/1if its one bank 32,550 -> 32,558 words. So no area delta in
logic. Placed (EPPO): 1x1/1if LUT 31,386, FF 42,122, Slice 13,370, BRAM 81 tiles, DSP 9; 8x8/1if LUT 42,607,
FF 50,722, Slice 15,415, BRAM 92.5, DSP 9.

## 6. Run history

- 02:32 assignment read; #925, the replica report, handoff section 10, the manager decision read.
- 02:4x step 1 read (section 1); TAKEN posted (#925 issuecomment-6904972364).
- 02:5x-03:1x the change, its tests and plants on the worktree (dev arms and plants in scratch); idiom gates: a
  multi-declarator (three sites) and srp_mutants.py over 1,000 lines found and fixed (the plants moved to
  srp_kind_mutants.py).
- 03:0x plat_ledger at the base PASS; on the worktree FAIL (KEY/LINK at 8x8-if2: ctrl_plat 20,416 B); the ledger
  record raised; plat_ledger PASS; test_ctrl_memory PASS. Commits `95426618`, `a9f0dbc0`.
- 03:22 gate units on fresh clones of `a9f0dbc0`: budget 1x1 (80-95) and 8x8-1if (64-79), --jobs 15; firmware
  self-test shards 0-3 (56-63, 48-55, 40-47, 32-39); fw_coverage --check (8-15).
- 03:23-03:25 image prep unit (0-7): split boots 1x1 and 8x8 PASS; S9's exports 1x1/1if and 8x8/1if, identity
  gate rc 0 each, integrated scripts written.
- 03:26 route chain unit (both shapes, three directives each, one Vivado at a time through vivado-slot.sh, each
  route booking its own 16 CPUs when free); 03:27 release-image unit (0-7): base then head.
- 03:3x-03:5x firmware shards: suites PASS, AECP 299/0, SRP 441/0, control 716/716; fw_coverage PASS; release image
  identical; docs and elaborate replays started (elaborate-gates-0's first run failed for want of the replay HOME's
  SDK link: an environment fault, the link made and the job re-run at 04:31: failed 0).
- 03:5x the docs replay's Python idiom gate found srp_kind_mutants.py:50 at 121 columns (untracked when the worktree
  check passed); wrapped.
- 04:00-05:31 the route chain: none of the six meets +0.030 at every corner (section 5).
- 04:1x the base's exports (no Vivado): the netlists equal the head's but LiteX's comment tree; only ROM contents differ.
- 05:31-06:52 the base's 1x1/1if routes for comparison: EPPO and ETO miss on hold (+0.014), ASL queued for CPUs.
- 05:49 budget 1x1 rc 0; 06:42 budget 8x8-1if rc 1 (STATED only, the shape's known excess); survey: no stated cost
  changes.
- 05:5x `1be0a6c4` (the line wrap, srp_mbx.c's ratchet line; fw_coverage --write's other three lines, aecp_*.c,
  stale at the base, not taken). Re-runs there: docs every job failed 0, firmware-unit and changes failed 0, the SRP
  shard 441/0; flip check 1x1/1if PASS, load gate PASS.
- 07:0x STOP posted once (#925 issuecomment-6908790238); the base's queued ASL route stopped (unit, its own
  processes listed first); receipts INDEX.md generated (499 files, no host path, none over 200 KB). No unit runs.

## 7. Incidents

- A pick race at 04:09:32-33: the coverage `--write` unit booked 8-15 a second before the ASL route booked 0-15
  (cpu_ranges.py had not seen the unit yet), so 8 CPUs were shared until the coverage run ended (about 8 minutes).
- A unit that would wait on the session pool and book CPUs when free was refused by the permission layer (no such
  unit started); the re-runs were started from the foreground once a range was free.
- Two backgrounded commands (a filesystem-wide find, a receipts grep) passed the foreground limit; both ended on
  their own, nothing depended on them.

## 8. For the manager

- Decide the routes (STOP). Every route is in scratch `rt/` (route/, route8/, route-base/), each with its routed
  checkpoint and the signoff reports (hashes in receipts/route/*/artifacts.txt).
- The base's 1x1/1if ASL route was not run: its unit waited for a 16-CPU range while holding a Vivado slot, so I
  stopped it at 07:09 (its script is ready: `rt/route-base/split-AltSpreadLogic_high/baseline_implementation.tcl`).
  No unit of this lane runs.
- Not run this round: the sweep (it may not run beside a route; it needs the decision's head), and arms other than
  arm A of the budget (the SRP change exercises the receive filter, the walk and the bind; arm A's groups cover
  those, and no stated SRP cost moved).
- The 8x8/1if budget point exits 1 on STATED lines that are not SRP's (polls base, ACMP item and declined offer over
  the one-interface statements), the classes #894's 8x8/1if gate recorded; restating the one-interface costs to them
  would move 1x1/1if's rows (`last` 136.65 of 140, `txL` 48.58 of 49), a decision outside #925.
- fw_coverage's ratchet holds three AECP lines below their measurement at the base (aecp_commands.c, aecp_face.c,
  aecp_maps.c); --write records them; left for their owner.
- Push `925-srp-ta-tf` at `1be0a6c4` once the routes are decided (PR-BODY.md is the draft; REVIEW READY is owed
  after the decision, not posted).
