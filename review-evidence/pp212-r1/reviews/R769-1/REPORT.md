[R769] NEGATIVE - exact head 04856e48619866e08ccaf5ffc34cf1636d8c5b74

# Internal independent review R769-1: processor PR #213 (issue #212)

- Repository: Mister-M-alt/protocol-processor-control-plane-avb-milan, PR #213, round R769-1.
- Exact head `04856e48619866e08ccaf5ffc34cf1636d8c5b74`, tree `b42073919da06557b45ec794c4cb5c0b7ba3ffe6`
  (verified in the review clone: HEAD, tree, worktree = index = HEAD for all 769 entries,
  0 untracked/ignored files, 0 gitlinks; `receipts/clone-integrity.txt`).
- Source base `a9e84b66d4cd0c331c8d6f2c1a71a62fcc824645` (nine commits). Live parent dev
  `604899c08ff1cd1830e1dd08b733109ef852400c` was read only for its area-budget record.
- No manager source bank runs at this head, and none is claimed or inferred here. The source-head
  execution evidence is the author's published receipts. Everything marked "reviewer run" below
  was run by this reviewer at the exact head, in disposable copies, with the pinned Verilator 5.050
  (identity in `receipts/tools-and-hosted.txt`).

## Verdict

NEGATIVE. One MINOR finding (F1) is open: a re-bind to the **same** stream is not applied when the
port's Talker registrar table already holds N other values, although the sink's own registrar
held the value until the unbind. In that case acceptance item 2's named scenario fails, and at the
2-sink shipping shape the condition only needs two other Talker values on the port. The rest of
the change checks out: the port registrars follow Table 10-4 with Δ13; the seed takes the next
state and doesn't double-count; withdrawals aren't applied; every new row fails by name under
its arm; every recorded count is unchanged or re-recorded with its reason; the area figures
reproduce exactly. One RESIDUE and three SUGGESTIONs are listed as well.

## Findings

### F1 — MINOR — Conformance, RTL, Robustness, Tests
**A re-bind to the same declared stream loses its registration when the port table is full.**

- **Where**: `hdl/srp/KL_srp_listener_fsm.sv:1399-1411` (an A8 or A15 takes the sink registrar to
  MT and clears its payloads). Also `:1419-1429` and `:689-708`, where only a port registrar
  (`pt_*`) can seed the settle. And `:653-658`: a value is allocated only when an entry is MT,
  and an entry frees only on rLv or leavetimer!.
- **Authority**: issue #212 acceptance 2 says "A re-bind (unbind, then bind to the **same** or
  another stream) with the Talker already declared: the same within one join period". The PR
  itself cites IEEE 802.1Q-2022 §10.7 and §10.7.8: a registrar's state does not depend on when
  the application became interested in the attribute. Milan v1.2 §5.3.8.5 and §5.5.3.5.18 step 4
  also apply.
- **Evidence** (reviewer run): a probe check was added to the end of section PS in
  `tb/srp_stream_fsms` (`receipts/probe-rebind-same-full-table.diff`;
  `scripts/probe_rebind_same_full_table.py`). It does this:
  1. Fill the port registrars with other values (the suite's own `fill_port_registrars()`).
  2. Settle sink 0 on V. The talker then declares V, so sink 0's own registrar holds V IN and
     sink 0 declares Ready.
  3. Unbind, then bind again to V, before the old Lv goes out (R1a) and after it (R1b).

  Both fail (`receipts/probe-rebind-same-full-table.summary.txt`, 1,470 checks, 1,468 PASS,
  2 FAIL):
  - R1a: nothing registers at the settle (tk 0), and the next tx! sends only the old Lv
    (`5/2@0001`), with no New.
  - R1b: nothing registers, and the next tx! sends nothing.

  So the Listener declaration waits for the talker's re-join after a LeaveAll (10 to 15 s). This
  is the exact symptom the issue reports for a re-bind.
- **Impact**: the table is filled first-come and holds values that no sink settled on until
  their talkers withdraw. At the shipping 2-sink shape, two other Talker values registered before
  V are enough. MSRP propagates every Talker declaration in the VLAN to each port, so that is the
  common case. The issue's re-bind defect then persists for a stream whose registration the port
  held until the A8. The registrar budget doesn't force this: at the A8 the sink's own registrar
  becomes free and still matches V.
- **Not a regression**: the base behaves the same. The PR's and §6.4's bound bullet ("a value
  registered while all N entries are registered is not held") covers this case by its letter. It
  doesn't say that a re-bind to the stream a sink was just using is lost too, and the issue's
  acceptance 2 has no such qualifier.
- **Required outcome**: one of the following.
  - (a) Keep the sink's registration of its value across the A8, so a re-bind to the same
    {stream_id, DA, VLAN} finds it whatever the table holds. Examples:
    - the sink registrar keeps registering its last value, unarmed, until its next A15, and an
      A15 on the same triple keeps that state; or
    - at the A8, hand the registration to a port registrar, replacing an entry no sink is
      settled on.

    Whichever is used, add a PS row (table full of other values, re-bind to the same stream,
    before and after the old Lv) and an arm that fails it by name.
  - (b) A recorded maintainer scope decision on issue #212 that acceptance 2 is bounded in the
    same way. §6.4, the PR limits and the integrator-facing text must then say that a re-bind to
    the same stream is also not applied while N other values are held.
- **Verification**: the probe above (or the new row) passes at the fixed head. Under (a) its arm
  is KILLED by name. The SRP campaign and the stream-FSM, srp_top and pp_top suites stay green.

### R1 — RESIDUE — Docs
**The storage row's write description is imprecise.**

- **Where**: `docs/architecture/10_srp_engine.md:222`, the storage row of the port Talker
  registrars, which says "state reset, the rest written with a registration and read only while
  it is not MT".
- **Problem**: the 32-bit leave deadline (`pt_dl_r`) is not written with a registration. It takes
  `now + T-MRP-LEAVE` at the LeaveAll that moves IN to LV (`KL_srp_listener_fsm.sv:671-673`,
  `:1454`). This is wording only: no figure, measurement or claim changes.
- **Exact fix**: replace "the rest written with a registration and read only while it is not MT"
  with "the value, type and payloads written with a registration, the leave deadline at the
  LeaveAll that starts LV; all read only while it is not MT".

### S1 — SUGGESTION — Docs, Robustness
**The pre-settle path's practical reach is not stated where integrators read.**

At N sinks the table holds the first N Talker values the port registers. A listener port receives
every Talker declaration in its VLAN, so on a network with more Talker values than N, the first
settle after power-on generally still waits for a LeaveAll. That is acceptance 1's own case. §6.4
states the bound abstractly. Suggest that the integrator guide (or the PR limits) state this in
these terms, with the shipping N.

### S2 — SUGGESTION — RTL (area)
**Two unmeasured area ideas.**

- **Narrower deadline**: the per-entry 32-bit absolute deadline and 32-bit age subtractor could
  become a 13-bit remaining-time count (5000 ms), with the absolute deadline rebuilt only for the
  seeded arm. That would be about 19 FF per entry plus part of the subtractor.
- **Unified table**: make the sink registrars pointers into a single N-entry table. That would
  remove about 107 FF per sink, but it changes the bound's semantics.

Neither is a finding:
- the reviewer's one measured restructure (a shared payload bus for the seed) was larger
  (`receipts/area-variant`, +176 LUT at listener N=2, +214 LUT at `KL_srp_top` 2x2);
- the author's published variant was mixed (+22 LUT at 2x2, -401 LUT at 8x8);
- the flip-flop content is what the clauses need: exact triple 124, FailureInformation 72,
  latency 32, state 2, type 1, and a deadline.

### S3 — SUGGESTION — RTL, Robustness
**The guard against a stale expiry ends earlier than the system-level window.**

An LV seed over an old LV registration keeps the old leave slot's deadline live until the seeded
arm reaches the timer service. In `KL_srp_top` that arm goes through the timer-arm FIFO
(`KL_srp_top.sv:972-984`). The listener's guard (`tpend_r != T_ARM_C`,
`KL_srp_listener_fsm.sv:555-557`, `:1383-1384`) ends when the arm *issues*, on the clock after
the settle. An old-deadline expiry that falls in the few-cycle FIFO latency would end the seeded
registration early.

- **Reachability**: it needs the old and new deadlines to differ and the old one to first expire
  inside a window of a few cycles, so it is practically unreachable. Base code has the same class
  of window after an LV→IN→LV sequence.
- **Docs claim**: §6.4's "until it is armed an expiry of the slot is the old registration's" holds
  at the listener face (PS15), not at the service.

Suggest a note, or a guard that holds until the service applies the arm.

## Prior public review findings

At this head the PR and the issue carry only the author's TAKEN / REVIEW READY comments and the
manager's review-start notices. No review FINDINGS are published, so none is resolved or retained.
This reviewer read no other reviewer's report.

## Lens evidence

### Conformance

- **The port registrars follow Table 10-4 with Δ13**:
  - New, JoinIn or JoinMt move to IN (`:665-666`);
  - rLv on IN moves to MT at once, and rLv on LV is `-x-` (`:669-670`, Δ13 per REQ-SRP-005
    "outside the LeaveAll cycle");
  - LV is reachable only from a LeaveAll on the lane of the held type, or the own LeaveAll
    (`:645-647`, `:671-673`);
  - LeaveTime is `LEAVE_MS_P` (5000 ms, F08.1 T-MRP-LEAVE, Milan Table 4.3), wired from
    `KL_srp_top.sv:614`;
  - leavetimer! moves LV to MT (`:650-651`, `:667-668`);
  - the priority (registering event, leavetimer!, rLv, LeaveAll) matches the sink registrar
    (`:1366-1397`).
- **Allocation keeps one entry per value**: a value is allocated only when no entry holds it
  (`pt_hit_w == '0`), so the seed's OR-mux is exact.
- **The seed** (`:689-708`) takes the entry's *next* state, so a LeaveAll or leavetimer! on the
  settle's clock applies. It takes the current payload registers, which can't change on a settle
  clock because a settle is accepted only without a decoder value (`ctl_ready_o`, `:818`). So no
  stale value is taken.
- **No double counting**: the seeded EVT_TK_REGISTERED is the sink's only registration strobe. A
  later JoinIn on IN or LV is silent (`ind_reg_w`, `:550-551`; PS8 "returns IN silently"). The old
  expiry on the settle clock is suppressed (PS15).
- **Withdrawals are not applied**: rLv (PS6), LeaveAll with no re-declare (PS7, received lane and
  own), and a settle on the leavetimer!'s clock (PS9).
- **FailureInformation at once**: FailureInformation, FAILED, REGISTERING_FAILED and
  GET_STREAM_INFO's code and bridge follow at once: PS2-PS5 and pp_top AS8 (flags 0x0042
  byte-exact, one TK_ATTR_REGISTERED).
- **Withdrawal while LV is consistent**: a Talker that sends rLv while its entry is LV (after a
  LeaveAll) is still seeded LV until leavetimer!. That is what a sink settled from the start
  would hold under Table 10-4 and Δ13 (`-x-` on LV), so it is not a finding.
- **The one-walk re-bind**: the parked Lv and the New of the settled value go in the same walk
  (§10.7.7, two values, two tx!). This is graded by RB1, RB4, RB6, RB7, PS4, PS13, PS14 and
  AS7/AS8.
- **No interface change**: `hdl/top/protocol_processor_top.sv` is unchanged (acceptance 4).
- **Open**: F1.

### RTL

Reviewed the full delta of `KL_srp_listener_fsm.sv` (+286/-8): `pt_match`, `pt_next`, `pt_seed`,
`park_hold`, `park_retire_declare`, the seed in `app_plane` and `reg_plane`, `sdl_*`, `pt_plane`
and `pt_data`.

- **The seeded arm path**: the `sdl_*` register issues the arm on the next clock, ahead of the
  pend queue. It clears `tpend_r` there, and a later same-clock pend assignment still wins.
  Back-to-back seeding settles re-load `sdl_*` after the issue of the previous one.
- **The retiring walk** (`pk_decl_w`):
  - its later assignments override the walk's own `app_r`/`fourpack_r` writes in the intended
    order;
  - it is blocked on settle clocks of the same sink (`app_arb` order);
  - `pk_alone_w` reads `eq_r`/`lq_r` with the correct index order;
  - `pk_hold_w` can't stall without bound, because it needs a registrar indication of that sink
    on each clock.
- **Reset**: `pt_reg_r` resets to MT, and every unreset `pt_*` field is read only under
  `pt_reg_r != MT`.
- **Lint and suites**:
  - Reviewer run, `scripts/lint_hdl.sh` with pinned Verilator 5.050: rc 0, 41 modules LINT OK
    (`receipts/head-lint_hdl-5050.log`).
  - Reviewer run at head (pinned 5.050):
    - `tb/srp_stream_fsms`: 1,468 checks PASS (base 1,435);
    - `tb/srp_top`: 8,669 PASS (base 8,669);
    - `tb/pp_top`: 11,064 PASS, rc 0.
- **Comment rule**: the added source comments carry behaviour, reason and issue/requirement IDs.
  A raw scan of every added line found no lane label, lane name, review round, reviewer ID or
  issue-comment ID ("lane" occurs only as the MSRP LeaveAll lane), so there is no RESIDUE.
- **Open**: F1. S3 is a suggestion.

### Robustness

- **Bound and allocation**: lowest-index MT entry; PS11 grades the full table and an entry freed
  by rLv.
- **Exact match**: the triple is matched exactly, and a VID with bits above 11 is never held
  (PS10).
- **Same-clock events**: LeaveAll and leavetimer! on the settle's clock (PS9), and a registrar
  change on every clock 0 to 8 of the retiring walk (PS14).
- **Link input**: the entries have no link input, like the sink registrars (documented). So a
  stale entry across a link flap can seed a settle until the peer re-declares, typically within
  one join period after link-up. That is consistent with the existing design, so it is not a
  finding.
- **Open**: F1. S1 and S3 are suggestions.

### Tests

All campaign runs are reviewer runs at the exact head, pinned 5.050, with `--jobs`.

- **SRP campaign, the 19 PS arms and the arms touched by the change**: 31 of 31 KILLED by their
  named checks, controls PASS (`receipts/srp-campaign-selected.log`, 33 of 33). Every per-arm
  failing count matches the `tb/srp_top/README.md` issue #212 table. pt-seed-dropped (the
  pre-settle path removed) fails PS1-PS5 and PS7-PS13, PS15. PS6 is caught by `pt-rlv-ignored`
  and PS14 by `park-retire-without-hold`. Union: PS1-PS15.
- **The six re-recorded issue #193 counts**: head 40/15/74/14/12/3 and base 35/14/65/13/7/2,
  exactly as the README says, and the tag lists match the cells (`receipts/srp-campaign-193*.log`).
- **Walk arms**: all 36 walk-group arms at head and at base, per shape
  (`receipts/walk-arm-shape-counts.md`). Only `listener-park-never-retires` moved (2/5/5/5 →
  2/4/10/18). It has no recorded count, and its named check was re-named with its reason
  (`WK12: push`). Every per-shape count recorded in the README is unchanged.
- **Patches apply**: all 203 SRP campaign patches apply at the exact head
  (`receipts/patch-apply-check.log`). The listener banner changed after the author's campaign
  run.
- **ACMP campaign, the two new arms**: 2 of 2 KILLED by name, goldens PASS
  (`receipts/acmp-campaign-presettle.log`). `presettle_seed_dropped` fails AS8 and AS9, and
  `presettle_park_declares_next_walk` fails AS7 and AS8.
- **Counts verified against the PR**:
  - pp_top 11,064 (author: 11,060 at base, +4 for AS8/AS9);
  - stream-FSM suite 1,468 vs 1,435;
  - srp_top unchanged.
- **Open**: F1. The F1 scenario has no row.

### Docs

- **`make check`**: rc 0 at the exact head (reviewer run, disposable clone;
  `receipts/head-make-check.log`).
- **Reproduced figures**:
  - storage figures: N×263 = 2+124+1+32+72+32, and `sdl_*` 1+log2 N+32 (34 to 36);
  - +560 FF at 2x2, and +2,140 FF at 8x8 from the same formula;
  - the area figures, by reviewer run with the same flow: `KL_srp_top` 2x2 goes from 11,475 to
    12,690 LUT and from 4,812 to 5,372 FF, and listener N=2 from 4,532 to 5,471 LUT; RAM is
    unchanged (`receipts/area-*`).
- **Text matches the code**:
  - the F10.5 arcs, the owed-Leave paragraph and the §6.4 subsection match the RTL;
  - the REQ-ACMP-018 row and the 02, 05, 00 edits are accurate;
  - the bench READMEs match the rows and arms.
- **Open**: R1 (RESIDUE, does not make the lens unclean). S1 is a suggestion.

## Area judgement (focus item 4)

The cost is real and close to what the chosen construction needs. On flip-flops it is near
minimal for "one registrar per port Talker value, bounded by N_SINKS_P": every field except
roughly 19 bits of each deadline is needed to seed "at once". The two restructures measured so
far did not reduce LUTs at the shipping shape (S2). So no avoidable large cost is shown, and no
area finding is raised.

The parent's record does matter here. `docs/design/AREA_BUDGET.md` at parent dev `604899c0`
records 63 of 15,850 slices left on the shipping route at processor `a9e84b66`, and says the next
shipping-image growth "has no slice room and needs its own owner decision". +1,215 LUT and
+560 FF (yosys, 2x2) is far beyond that room. This is a pending manager and owner duty, below.

## Ledger

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1) | issue #212 acceptance 1-5; 802.1Q-2022 §10.7/10.7.7/10.7.8/Table 10-3/10-4 as cited; Milan v1.2 §4.2.7.2.2 (Δ13, REQ-SRP-005), §5.3.8.5, §5.3.8.9, §5.5.3.5.18, Table 4.3; `KL_srp_listener_fsm.sv` delta; PS1-PS15, AS7-AS9; reviewer probe R1a/R1b | R769-1 | 04856e48619866e08ccaf5ffc34cf1636d8c5b74 |
| RTL | UNCLEAN (F1) | full RTL delta; reviewer lint (41 modules, 5.050); reviewer suites (stream-FSM 1,468, srp_top 8,669, pp_top 11,064); yosys area at base, head and one variant | R769-1 | 04856e48619866e08ccaf5ffc34cf1636d8c5b74 |
| Robustness | UNCLEAN (F1) | bound and allocation, same-clock events, retiring-walk hold, seeded-arm path through `KL_srp_top` timer FIFO, link behaviour; reviewer probe | R769-1 | 04856e48619866e08ccaf5ffc34cf1636d8c5b74 |
| Tests | UNCLEAN (F1: no row) | SRP arms 31/31 entries (26 labels) + 2 controls; #193 arms 8/8 entries + 2 controls at head and at base; 36 walk-group arms (41 entries) head/base per shape; 203 patches apply; ACMP arms 2/2; README count cells | R769-1 | 04856e48619866e08ccaf5ffc34cf1636d8c5b74 |
| Docs | CLEAN (R1 residue) | 10_srp_engine §5 storage, §6.4 (F10.5, owed Leave, pre-settle), 02, 05, 00 REQ-ACMP-018; tb READMEs (srp_top, srp_stream_fsms, pp_top); PR body figures; `make check` rc 0 | R769-1 | 04856e48619866e08ccaf5ffc34cf1636d8c5b74 |

## Real limits of this review

- **Not run by this reviewer**:
  - the full processor suite sweep (`scripts/run_suites.sh`), `syn/yosys/run.sh`,
    `tb/elab_guards`, the Verilator 5.052 lint, and the full SRP and ACMP campaigns;
  - the AECP, GSI, CTR, name-write, AECP-dispatch, notification and D3 campaigns.

  For these, the author's receipts at `0b5e988`/`913214a` are the evidence. Between `0b5e988` and
  this head only docs and READMEs changed. The `0615f32` banner change after `913214a` is comment
  only, and all 203 SRP patches still apply.
- **Rows-by-name claim**: "each new row fails by name" was verified for the PS, RB, AS and WK12
  arms. The SRP arms outside the 26 selected labels, the six issue #193 arms and the 36
  walk-group arms, and the other 101 ACMP arms, were not re-run at this head.
- **Re-run artefact**: the first pp_top attempt was superseded. It was killed after a second run
  had started in the same tree, and is not used. The reported pp_top result is the second,
  complete run (rc 0, 11,064 PASS).
- **Scratch-parent gates not reproduced**: the evidence is the author's receipts at pin
  `0b5e988` (full rtl-fast job set and milan_dp) and at pin `04856e4` (changes, lint, behave, the
  yosys elaboration job). The receipts show these as rc 0 and the ROM digests recorded for the
  pin.
- **Hosted CI at the exact head**, inspected and not accepted, since the manager owns that:
  - pull_request run 41912844101: portability, suites and docs-gates success;
  - push run 41912834785: portability and docs-gates success, suites CANCELLED, so it is not
    evidence.
- **No hardware, no timing**: no Vivado run and no route. Physical calibration was NOT RUN, and
  field skips are not hardware proof.
- **Spec text**: spec clauses were checked against the repository's transcriptions (Δ13 / F01.4,
  REQ rows, F08.1) and the PR's citations. Spec PDFs were not available here.
- **Redaction**: local home-directory paths in published logs were replaced by `<home>`.

## Pending manager duties

1. Resolve F1 on a new head, by fix plus row plus arm, or by a recorded scope decision with the
   docs stating it. Then run a re-review.
2. **Parent fit**: at adoption, run the parent's Vivado route of the shipping image with the new
   pin. The parent record shows 63 slices free at `a9e84b66`, and the yosys growth is
   +1,215 LUT and +560 FF at 2x2. Get the owner decision the parent's area budget requires for
   any shipping-image growth.
3. Validate the current-dev merge candidate (builder and native banks) at the merge turn, and link
   its receipts. Carry R1 to the residue checklist.
4. Accept the hosted runs. The push-event `suites` job at this head was cancelled; the
   pull_request one passed.

## Receipts

Every file below is listed in `MANIFEST.sha256`. Scripts: `scripts/area.sh`,
`scripts/area_summary.py`, `scripts/variant_shared_payload.py`,
`scripts/probe_rebind_same_full_table.py`, `scripts/walk_counts.py`, `scripts/run_bg.sh`.

R769-1 FINISHED
