[R770] NEGATIVE - exact head 04856e48619866e08ccaf5ffc34cf1636d8c5b74

# R770-1 independent review: PR #213 (issue #212), round 1

- Repository: Mister-M-alt/protocol-processor-control-plane-avb-milan, PR #213
- Exact head reviewed: `04856e48619866e08ccaf5ffc34cf1636d8c5b74`, tree `b42073919da06557b45ec794c4cb5c0b7ba3ffe6`
  (the clone's `HEAD` and `HEAD^{tree}`, checked before and after the probes)
- Base: `a9e84b66d4cd0c331c8d6f2c1a71a62fcc824645` (nine commits, `350d976` .. `04856e4`)
- Reconstructed in this order: the repository docs (`docs/README.md`; the repository has no
  AGENTS.md or CONTRIBUTING.md), the issue #212 body and its comments (frozen acceptance 1-5),
  the PR body, the compliance rows the PR touches (REQ-ACMP-018, REQ-ACMP-022, REQ-SRP-005, Δ13),
  F08.1, the full delta `a9e84b66..04856e48`, its history, the published evidence
  (`kebag-logic/milan-fpga@c87fe4c3`, `review-evidence/pp212-r1`: the area, campaign and
  scratch-parent receipts), then my own executions and fault probes.

## Verdict

NEGATIVE. The RTL I read does what the PR says, and I found no wrong behaviour at the head. Every number I re-ran
matches the PR: suites, campaign counts, the six re-recorded issue #193 counts, and the area figures at both
shapes. Four MINOR findings stay open:

- F1-F3 are test gaps. Each one is a defect I planted in the new port-registrar or seed path that passes all
  of `tb/srp_stream_fsms` (1,468 checks), `tb/srp_top` (8,669) and the default `tb/pp_top` build (10,509
  checks, every section). Two of them sit directly on acceptance items 3 and 2.
- F4 is a conformance gap. The new port registrars leave out Table 10-4's Flush!/Begin! on LINK_DOWN and
  LINK_UP, so a registration made before a link loss can be seeded into a sink that settles after it.

There is also one RESIDUE (F5) and one SUGGESTION (S1).

## What was verified (exact-head and base execution, pinned Verilator 5.050)

The pinned Verilator wrapper is `$VALIDATION_TOOLS/pinned-verilator-5.050/verilator`; it reports
`Verilator 5.050 2026-07-01 rev v5.050` and its sha256 is `905795b9...79e92f`. It was put first on PATH
for every build. Receipts are under `receipts/`.

| Run | Tree | Result | Receipt |
|---|---|---|---|
| `tb/srp_stream_fsms` (`make`, walk arms at four shapes, then the suite) | head | rc 0, **1468 checks: 1468 PASS**, matching the README and the PR | `receipts/suites/srp_stream_fsms-head.log` |
| `make check` (in a git-initialised export of the head tree, same tree id `b4207391`) | head | rc 0 | `receipts/suites/make-check-head.log` |
| `scripts/lint_hdl.sh` | head | rc 0, every module `LINT OK` | `receipts/suites/lint_hdl-head-verilator5050.log` |
| SRP campaign `tb/srp_top/mutants.py --only <27 arms> --jobs 6`: the 19 issue #212 arms, `listener-park-never-retires`, the re-cut `listener-retire-skips-group-mark`, and the six issue #193 arms whose counts were re-recorded | head | **35 checks: 35 PASS**, every arm KILLED by its named check. Each failing-check count equals its README cell (22, 22, 17, 8, 5, 5, 6, 4, 9, 1, 2, 1, 2, 1, 1, 4, 1, 2, 1; #193: 40, 15, 74, 14, 12, 3) | `receipts/campaigns/srp-head/`, `receipts/logs/J3_srpcamp_head.log` |
| The same six #193 arms plus `listener-park-never-retires` | base | 13/13. Counts 35, 14, 65, 13, 7, 2: exactly the README's "at main 35, 14, 65, 13, 7 and 2" | `receipts/campaigns/srp-base/`, `receipts/logs/J7_srpcamp_base.log` |
| ACMP campaign `tb/pp_top/acmp_mutants.py --only presettle_seed_dropped presettle_park_declares_next_walk park_never_retires --jobs 3` | head | golden `pp_top --acmp-only` PASS (62 checks); **3 of 3 KILLED** by their named checks, including the renamed `AS7: the MRPDU after it goes on with the new stream` | `receipts/campaigns/acmp-head/` |
| Area, the author's published flow (`receipts/area/area.sh` in the evidence; sv2v, then `read_verilog all.v; hierarchy -check -top KL_srp_top -chparam ...; synth_xilinx -family xc7 -flatten`) | base, head | `KL_srp_top` 2x2: LUT1-6 11,475 → 12,690 (**+1,215**), FF 4,812 → 5,372 (**+560**), INV 2,811 → 2,944. 8x8: LUT 23,046 → 27,399 (**+4,353**), FF 9,236 → 11,376 (**+2,140**), INV 3,483 → 4,411. Matches the PR and `10_srp_engine.md` exactly. All four stat files are byte-identical (same sha256) to the published `author/receipts/area/{base,head}/srp_top_{2x2,8x8}.stat` | `receipts/area/author-flow/` |
| Area, an independent front end (`read_verilog -sv -defer` + `chparam`, same synth command) | base, head | 2x2: LUT 11,385 → 13,033 (+1,648), FF +560 (identical). The flip-flop figure does not depend on the flow. The LUT delta moves by about 430 with the front end alone | `receipts/area/independent-flow/` |
| Reviewer fault probes (`scripts/probe.py`, one exact text edit each, RTL only) | head | see F1-F3 and the table below | `receipts/probes/` |

Reviewer probe results (each probe is one edit to `hdl/srp/KL_srp_listener_fsm.sv`; "pp_top" is the
`gsi-build` binary with `--acmp-only`, as the ACMP campaign grades AS7-AS9; "pp_top_all" is the same binary
with no argument, every section of the default build):

| Probe | Planted defect | srp_stream_fsms | srp_top | pp_top | pp_top_all |
|---|---|---|---|---|---|
| `presettle-removed` | `seed_v_w` and `pk_decl_w` forced 0: the whole pre-settle path removed | **26 FAIL** (PS1-PS5, PS7-PS13, PS15, RB1, RB4, RB6, RB7) | - | - | - |
| `seed-declares-ready-only` | a seeded Talker Failed declares Ready | **6 FAIL** (PS2-PS5) | - | - | - |
| `pt-type-on-alloc-only` | the port registrar keeps its allocation's type (no Advertise↔Failed follow) | 0 FAIL | - | **2 FAIL (AS8)** | - |
| `pt-alloc-any-event` | an unheld value is allocated IN on any Talker event (rLv, rIn, rMt included) | 0 FAIL | 0 FAIL | 0 FAIL | 0 FAIL |
| `pt-fcode-first-only` | the port registrar keeps its first FailureInformation | 0 FAIL | 0 FAIL | 0 FAIL | 0 FAIL |
| `pt-lat-on-alloc-only` | the port registrar keeps its allocation's accumulated_latency | 0 FAIL | 0 FAIL | 0 FAIL | - |
| `seed-on-teardown` | an A8 teardown seeds the registrar (`ctl_settle_i` dropped from `seed_v_w`) | 0 FAIL | 0 FAIL | 0 FAIL | - |
| `pt-rlv-on-lv-ends` | rLv on an LV port registrar ends it at once (Table 10-4: `-x-`) | 0 FAIL | - | - | - |

The PS6 and PS14 rows do not fail when the whole path is removed, and they should not: a withdrawal that is
not applied looks the same as no path at all. The PR's arms for them (`pt-rlv-ignored`,
`park-retire-without-hold`) break the withdrawal handling instead, and I confirmed that both fail their named
checks. So point (3) of the focus holds for every new row: PS1-PS15, AS7-AS9 and WK12 each have an arm that
fails it by name. The assertion-coverage check requires PS1-PS15.

## Findings

### F1 - MINOR - Tests, Robustness - acceptance 3 is not graded against allocation by a non-registering event

- **Where:** `hdl/srp/KL_srp_listener_fsm.sv:654`. `pt_alloc_w[e] = pt_rx_w && rx_registering_w && ...` is the
  only thing stopping an rLv (or rIn, rMt) of a Talker value that no entry holds from creating an IN
  registration. The test rows are `tb/srp_stream_fsms/sim_main.cpp` PS6/PS7/PS9/PS11 and `tb/pp_top` AS7-AS9.
- **Evidence:** probe `pt-alloc-any-event` drops `rx_registering_w` from that term. It passes every check in
  all four runs: `receipts/probes/pt-alloc-any-event@{srp_stream_fsms,srp_top,pp_top,pp_top_all}.log`.
  - PS6 injects JoinIn and then Lv, so the value is already held and the Lv hits it. No row presents a
    withdrawal, or an In/Mt, of a value that is not held.
  - In practice that happens when the JoinIn arrived while every entry was held (PS11's state), then an entry
    freed, then the talker withdrew.
- **Authority:** issue #212 acceptance 3 ("A Talker attribute that is withdrawn (rLv ...) before the settle is
  not applied") and acceptance 5 (rows with mutants that fail by name). 802.1Q-2022 Table 10-4: rLv!, rIn!
  and rMt! never take MT to IN.
- **Impact:** a regression that registers a withdrawn Talker, and declares Listener Ready for it at the next
  settle, would land green.
- **Required outcome:** a row (for example PS16) that sends rLv, rIn and rMt for a Talker value not held,
  including one that was refused while the table was full. It then settles a sink on that value and expects
  nothing applied. Add an SRP-campaign arm (this probe's edit) that fails it by name, and update the coverage
  list and README counts.
- **Verification:** the new arm is KILLED by its named check and the full suite stays green.

### F2 - MINOR - Tests - acceptance 2's "failure code follows the registered Talker Failed" is not graded for a change made before the settle

- **Where:** `hdl/srp/KL_srp_listener_fsm.sv:1462-1465`. Here the port registrar re-latches accumulated_latency
  and FailureInformation on every registering event, and the seed (`pt_seed`, lines 689-708) hands them to
  the settling sink.
- **Evidence:**
  - Probe `pt-fcode-first-only` latches FailureInformation only at allocation or on the first Failed. It
    passes all four runs.
  - Probe `pt-lat-on-alloc-only` latches latency only at allocation. It passes three runs.
  - Every PS/AS row registers one Talker Failed with one FailureInformation (`SYSF`/`FCODE`, `FAIL_CODE`) and
    one latency.
  - The in-place type swap is graded: `pt-type-on-alloc-only` fails AS8. But a changed failure code, failure
    bridge or latency on a value no sink is settled on is never presented before a settle.
- **Authority:** issue #212 acceptance 2 ("the REGISTERING_FAILED / FAILED counters and the stream-info
  failure code follow the registered Talker Failed at once"). Milan v1.2 §5.4.5.2 / Table 5.22 for
  GET_STREAM_INFO's failure and latency fields.
- **Impact:** a seed of a stale failure code, bridge ID or latency would land green. That stale value is what
  GET_STREAM_INFO reports from the settle until the talker's next declaration, which with periodic
  transmission off is the next LeaveAll, 10-15 s later.
- **Required outcome:** a PS row that changes the Talker Failed FailureInformation (code and bridge) and the
  accumulated_latency of a held value before any sink settles, then checks the sink's `msrp_fail_code`,
  `msrp_fail_bridge` and `acc_latency` at the settle. Add campaign arms for both edits that fail it by name.
- **Verification:** both arms are KILLED by name.

### F3 - MINOR - Tests - the settle-only seed guard and Table 10-4's rLv-on-LV `-x-` for the port registrars are ungraded

- **Where:** `hdl/srp/KL_srp_listener_fsm.sv:706-707` (`seed_v_w` requires `ctl_settle_i`) and `:670`
  (`if (pt_reg_r[e] == R_IN_C)`: rLv on LV leaves the entry LV).
- **Evidence:**
  - Probe `seed-on-teardown` makes every A8 teardown on a held value seed the sink's registrar and strobe
    EVT_TK_REGISTERED on the unbind. It passes srp_stream_fsms, srp_top and pp_top `--acmp-only`.
  - Probe `pt-rlv-on-lv-ends` passes srp_stream_fsms. No PS row sends an rLv to an entry that a LeaveAll has
    taken to LV and then settles inside that entry's T-MRP-LEAVE.
- **Authority:**
  - F10.5 (`10_srp_engine.md`): teardown edges carry no registration event.
  - 802.1Q-2022 Table 10-4: rLv! in LV is `-x-`, the PR's own claim "rLv ... on LV `-x-`", and the focus
    item "follow the registrar state machine exactly".
  - Acceptance 5.
- **Impact:** a regression that strobes TK_ATTR_REGISTERED on every unbind, or drops an LV registration early,
  would land green.
- **Required outcome:** an A8-on-a-held-value check (no EVT_TK_REGISTERED, nothing registered) and an
  LV-plus-rLv-then-settle check (LV seeded, `PS8`-style deadline), each with an arm that fails it by name.
- **Verification:** both arms are KILLED by name.

### F4 - MINOR - Conformance, RTL, Robustness - the port registrars have no Flush!/Begin! on LINK_DOWN/LINK_UP, so a pre-outage registration is seeded after the link returns

- **Where:**
  - `hdl/srp/KL_srp_listener_fsm.sv` (no link input; `pt_plane` clears only on `rst_n`, lines 1444-1450).
  - `hdl/srp/KL_srp_top.sv:143,374`: `link_up_i` reaches only `u_domain`.
  - `docs/architecture/10_srp_engine.md:782-783`: "As the sink registrars, the entries have no link input".
- **Authority:**
  - 802.1Q-2022 Table 10-4: Begin! and Flush! take every registrar to MT. The focus item asks that the port
    registrars follow the 10.7 registrar state machine exactly.
  - The engine's own model applies these events to the Domain registrar: `10_srp_engine.md:309`, "LINK_UP
    (Begin!) or LINK_DOWN (Flush!) | MT".
  - The PR justifies the table with §10.7 and §10.7.8 ("a full participant keeps a registrar per attribute
    value registered").
- **Impact:** this is new behaviour. Before the PR, an unsettled sink could not inherit registrar state. Now
  every Talker value registered before a link loss stays IN across it, and a sink that settles after the link
  returns is seeded from it:
  - EVT_TK_REGISTERED, `tk_reg_state`, the ACMP listener's SETTLED_RSV_OK and Listener Ready New all follow
    for an attribute the current link has not registered.
  - Example: a talker that rebooted during the outage, answers PROBE_TX, but has not declared its stream
    again.
  - This lasts until this participant's own LeaveAll ages the entry (T-MRP-LEAVEALL plus T-MRP-LEAVE). The
    sink registrars' existing lack of a link input applied only to sinks already settled through the outage.
    The port table spreads it to every value on the port.
- **Required outcome:** take every port registrar to MT on LINK_DOWN (Flush!) and on LINK_UP (Begin!). This
  means a link-level input to `KL_srp_listener_fsm`; `KL_srp_top` already has `link_up_i`, so the processor
  top and the register map do not change (acceptance 4). Add a row (register, link down/up, settle, nothing
  applied) and an arm that fails it by name. The alternative is to record this as a justified deviation with
  a Δ row in F01.4 and the compliance matrix; that is a scope decision for the maintainer.
- **Verification:** the new row passes at the fixed head, and the arm that removes the flush fails it by name.

### F5 - RESIDUE - Docs - two timing values copied outside F08.1

- **Where:** `docs/architecture/10_srp_engine.md:759` ("the next LeaveAll, 10 to 15 s later (Milan Table
  4.3)") and `:805` ("the timer's expiry after a random 10 to 15 s").
- **Authority:** `docs/README.md` §2, single-source rules: timing values only in F08.1, and a value copied
  outside its table is a review finding.
- **Exact fix:**
  - At `:759`, "10 to 15 s later (Milan Table 4.3)" becomes "one `T-MRP-LEAVEALL` later".
  - At `:805`, "after a random 10 to 15 s" becomes "after a random `T-MRP-LEAVEALL` draw".
- This is wording only: it changes no figure, test, code or claim.

### S1 - SUGGESTION - RTL area (no verdict effect)

The measured cost is +1,215 LUT and +560 FF at 2x2, and +4,353 LUT and +2,140 FF at 8x8. Bounded at N =
`N_SINKS_P`, each entry's 263 flip-flops carry only information the clauses need at the settle:

- the exact value (124 bits) and the state (2) for the match;
- the type (1), latency (32) and FailureInformation (72) for acceptance 2;
- the absolute leave deadline (32) to keep Table 4.3 timing.

I found no change that meets the same clauses at a clearly lower cost:

- **Narrower deadline.** The deadline could be held in 13 bits (T-MRP-LEAVE of 5000 ms fits a wrap-safe
  8,192 ms window), widened to absolute only for `sdl_ms_r`. That saves 19 FF and a 19-bit subtractor per
  entry, about 150 FF at 8x8.
- **Sinks reference entries.** The sink registrars could point into the port table instead of copying from
  it. That removes about 107 FF per sink and the seed copy muxes, but it adds per-sink N:1 output muxes and
  an eviction rule. The LUT saving is not shown.
- **Author's variant.** The author's own lighter variant (`opt-variant` in the evidence) measured no LUT
  saving at 2x2: 12,712 against 12,690.

So I do not rate the cost as avoidable. Two caveats:

- The LUT figure moves by about 430 at 2x2 with the yosys front end alone (independent flow, +1,648). The
  FF figure does not move.
- The parent's slice fit at the shipping shape is unproven until the integrator's Vivado route runs (below).

## Conformance notes (no finding beyond F4)

- **Table 10-4 rows (`pt_next`, lines 661-676):**
  - New, JoinIn and JoinMt take an entry to IN; a re-declaration in LV returns it to IN.
  - leavetimer! takes LV to MT.
  - rLv takes IN to MT at once (Δ13, Milan v1.2 §4.2.7.2.2; REQ-SRP-005), and LV is `-x-`.
  - A LeaveAll on the lane of the held type, or the own LeaveAll, takes IN to LV with now + `LEAVE_MS_P`
    (T-MRP-LEAVE, Milan Table 4.3).
  - The leavetimer runs only from LeaveAll.
  - The priority (registering event > leavetimer! > rLv > LeaveAll) equals the sink registrar's
    (`reg_plane`, lines 1365-1397).
  - The expiry compare is wrap-safe, as in `KL_pp_timer_service`.
- **The seed is the entry's next state.** `pt_seed` uses `pt_nreg_w`/`pt_ndl_w`, so a same-clock LeaveAll or
  leavetimer! applies (PS9). The payloads cannot change on a settle clock, since a settle is accepted only
  without a decoder event (`ctl_ready_o`).
- **No double count.** One EVT_TK_REGISTERED per seeding settle, checked by AS8/AS9 `registered_traced(...) ==
  1`. An old expiry on the settle's clock is silenced (PS15). A seeded LV arms the slot with the entry's
  deadline on the next clock, guarded through `tpend_r == T_ARM_C` (PS8, PS15).
  - Several settles on consecutive clocks each issue their arm in turn: the `sdl_*` register is reloaded on
    the same clock it issues.
- **One join period.** A seeded request is granted on the next clock and New! follows through the owner
  election, so the next tx! sends New (PS1/PS2, AS9 ≤ 240 ms with no LeaveAll).
  - With a parked Leave, `pk_decl_w` applies New! in the clock that sends the parked Lv and leaves the slot
    unmarked, so the walk's second pass sends the New in the same walk and one MRPDU (PS4, RB1/4/6/7, AS7,
    AS8).
  - `pk_alone_w` defers to an existing group declarer (PS13), and `pk_hold_w` holds the walk one clock on a
    same-clock indication (PS14).
  - I traced the remaining same-clock interleavings: a settle or teardown of the walk sink, or of another
    sink onto the new stream, on the `pk_decl_w` clock. Each leaves one applicant per stream_id (issue #193).
- **Acceptance 4.** `hdl/top/protocol_processor_top.sv` and `KL_srp_top`'s port list are unchanged, and the
  listener's port list is unchanged. No register-map file changed.
- **Bound behaviour.** First-come with N entries. On a port that registers more Talker values than N_SINKS_P
  (2 at the shipping shape), values registered after the table fills are not held, and their sinks wait for
  the next LeaveAll as before. The PR states this limit and PS11 grades it.
- **Comment rule (owner 2026-10-15).** The new source comments in `hdl/`, `tb/` and the campaign drivers cite
  issue and clause IDs. A scan of every added line found no bench lane labels, lane names, review rounds,
  reviewer IDs or issue-comment IDs ("lane" occurs only as the LeaveAll lane of an AttributeType). No RESIDUE
  under that rule.

## Reviewer-owned ledger

| Lens | Status | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F4) | `KL_srp_listener_fsm.sv` `pt_match`/`pt_next`/`pt_seed`/`pt_plane`/`pt_data`, `reg_plane`, `park_hold`, `park_retire_declare`, `app_plane`; `KL_srp_top.sv` link wiring; 802.1Q-2022 Table 10-3/10-4 roles, Milan v1.2 §4.2.7.2.2 (Δ13), §5.3.8.5, §5.3.8.9, §5.5.3.5.18 step 4, Table 4.3 via F08.1; REQ-ACMP-018/022, REQ-SRP-005 | R770-1 | `04856e48619866e08ccaf5ffc34cf1636d8c5b74` |
| RTL | UNCLEAN (F4) | the full listener delta (lines 470-708, 818-831, 1026-1053, 1133-1218, 1326-1472); lint rc 0 under 5.050; area re-run at 2x2 and 8x8 (both flows) | R770-1 | `04856e48619866e08ccaf5ffc34cf1636d8c5b74` |
| Robustness | UNCLEAN (F1, F4) | same-clock interleavings of settle/teardown/decoder event/LeaveAll/expiry/walk; bound and allocation policy; link loss; the seeded-timer handoff | R770-1 | `04856e48619866e08ccaf5ffc34cf1636d8c5b74` |
| Tests | UNCLEAN (F1, F2, F3) | `tb/srp_stream_fsms` PS1-PS15 and the RB/L9/SH14/SH15 edits; `tb/pp_top` AS7-AS9 and the new MRPDU reader; `tb/srp_top/mutants.py` (19 arms + coverage), `tb/pp_top/acmp_mutants.py` (2 arms); my runs: suite 1468/1468, SRP subset 35/35 head and 13/13 base, ACMP 3/3; 8 reviewer probes over up to four suites | R770-1 | `04856e48619866e08ccaf5ffc34cf1636d8c5b74` |
| Docs | CLEAN (F5 is RESIDUE) | `docs/architecture/10_srp_engine.md` (§5 storage rows and the measured cost, F10.5 arcs, owed-Leave rule, §6.4 "A Talker registered before the settle"), `02_interfaces.md`, `05_acmp_engine.md`, `00_MILAN_COMPLIANCE_REVIEW.md` REQ-ACMP-018, the three tb READMEs (counts checked against my runs), the PR body; `make check` rc 0 | R770-1 | `04856e48619866e08ccaf5ffc34cf1636d8c5b74` |

## Scratch-parent consumer gate (focus 5), from the published receipts

Evidence: `review-evidence/pp212-r1/author/receipts/parent/` at `kebag-logic/milan-fpga@c87fe4c3`.

- **What it shows:**
  - The scratch parent is milan-fpga dev `604899c0` with local commits only. Its push URL is disabled.
  - At pin `0b5e988` (the last code commit), `parent-records.txt` and `pin-0b5e988/` show the rtl-fast
    steps rc 0: changes, `lint_rtl`, `pp_srcs`, behave (14 features, 508 scenarios), the yosys elaboration
    of `milan_datapath`/`KL_pp_shadow`/`KL_gptp_shadow`, firmware unit/boundary/verilator and shards, and
    `milan_dp`. The ROM digest rows are identical to main's.
  - At this exact head, `pin-04856e4/` shows `rom_digests_final.log` naming pin `04856e48...` and these
    steps rc 0: changes, `lint_rtl`, `pp_srcs`, behave (508 scenarios) and the yosys elaboration (3 of 3 PASS).
- **Why that is enough:** `git diff --stat 0b5e988 04856e4` touches only `10_srp_engine.md` and two tb
  READMEs. No RTL or build input differs, so the firmware and `milan_dp` results at `0b5e988` carry to this
  head.
- **What it does not show:** I found no defect that appears only in the parent. The receipts carry no
  physical fit (Vivado) at the shipping shape; see the limits below.
- I did not run the parent gates myself (not allowed here).

## Real limits

- No manager source bank ran at this head, and I claim none. Source-head execution is the author's published
  receipts plus my focused runs above.
- I did not run the full SRP campaign (247 arms), or the ACMP, AECP, GSI, CTR, notification, D3 or dispatch
  campaigns beyond the arms listed. I did not run the full seven-build `tb/pp_top` sweep: I ran only the
  default build's binary (10,509 checks) under two probes, and `--acmp-only` for the rest. I did not run
  `scripts/run_suites.sh`.
- I did not run Vivado. Physical calibration was NOT RUN, and field skips are not hardware proof. Slice fit of
  `+1,215 LUT / +560 FF` (yosys) at the shipping shape is unproven.
- Not examined: the pre-existing type-agnostic rLv rule of the sink registrar. An rLv of either Talker type
  withdraws the held value. The port registrars copy that rule, and its ordering against an in-place
  Failed→Advertise swap was not probed.
- The probes are reviewer edits run in disposable trees under `scratch/`. Nothing was edited in the clone. I
  checked `HEAD`, the tree, the index and the status after the runs (below). The repository has no submodule
  gitlinks; the parent gitlink is in milan-fpga.

## Pending manager duties

- Build the current-dev merge candidate (source base `a9e84b66`, live dev `604899c0`), run the builder and
  native banks, and link the receipts on the PR.
- Hosted/act acceptance for the exact head.
- The parent pin bump with its ROM-digest rows and documented-pin update, and a Vivado slice-fit measurement at
  the shipping shape before adoption.
- Carry F5 to the residue checklist.

## Prior public review findings at this head

I read these only after the verdict and ledger above were written. At the time of this review, PR #213 and
issue #212 carried no published review findings:

- PR #213 has three review-start notices (R769-1 twice, R770-1), no review objects and no line comments.
- Issue #212 has the author's TAKEN and REVIEW READY comments.

There is nothing to resolve or retain. I found no manager evidence comment on the issue or PR either; the
evidence I used is the published `review-evidence/pp212-r1` tree.

## Clone integrity after the probes

`receipts/clone-integrity.txt` shows the following:

- `HEAD` is `04856e48619866e08ccaf5ffc34cf1636d8c5b74`, `HEAD^{tree}` and the index tree are
  `b42073919da06557b45ec794c4cb5c0b7ba3ffe6`, and status is empty (ignored files included).
- The index modes and blobs equal the HEAD tree (769 files).
- Every work-tree file hashes, without filters, to its HEAD blob.
- There are no gitlinks.

R770-1 FINISHED
