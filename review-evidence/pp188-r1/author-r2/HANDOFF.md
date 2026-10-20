# [A651] HANDOFF — processor #188 and #189 (listener lane), round 2

Status: **REVIEW READY** at head `cca12e3cbdbecc00eeb62d11c74dfb19d6472af0` (local branch; not
pushed, no PR edited). Every processor gate, every campaign that builds a changed file and every
scratch-parent consumer gate ran at base and head. A host reset (2026-10-19 21:53) cut three head
campaigns (acmp, d3, notify) and the head `milan_dp` consumer gate mid-run; they were rerun whole
at the same head (the cut logs kept under `receipts/round2/superseded/`), with the OOC head gates
and the reviewer probes. No code changed after the reset.

- Repository: Mister-M-alt/protocol-processor-control-plane-avb-milan (origin verified), PR #195.
- Branch `188-189-listener`, round-2 base `cb8bab044d98a89d8c4eb2b56bd81835e6fc5d48` (the PR head
  after round 1: the two author commits and the manager merge of main `b48312e1`).
- Assignment: PR #195 comment 6264243047, answering R665-1 (comment 6264221765) and R666-1
  (comment 6263408703). All three read in full. The reviewers' probe material (R665-1
  `probes.py`, `rv_section.cpp`; R666-1 `reviewer-probes.patch`) was fetched from the parent
  repository's `pp188-review-evidence` branch as data, read, and run only from a scratch copy.
- New commits on cb8bab04, no rebase, no amend (one-line subjects, no body, no trailers):
  1. `114f16a6929995eda7634df1d0a15a37bf2fc826` Read the Failed bit of a coalesced TK_ATTR_REGISTERED from the registered type, so REGISTERING_FAILED follows the last swap (issue #189)
  2. `51df2b618839643d59a24a6e6d7df0f04956142a` Check every documented settle arm of the owed Listener Leave, and let a sink with no record owe nothing (issue #188)
  3. `66785d2c82aa25fc1269b81d47c8693c4a455582` Word the same-stream settle for LA or LO, and drop check labels from the explanatory comments (issues #188, #189)
  4. `0f9a4f2dc43d84d7777d4e6669d78b21e98a0c52` Record RB1-RB9 in the srp_top coverage note and the coalescing case in the ACMP driver docstring (issues #188, #189)
  5. `518b365806cca14414d48e7773abdee662d8651f` Grade WK12's counts and precondition and AS5d's start with planted controls, and re-record the walk-copy and teardown-as-declare counts (issues #188, #189)
  6. `cca12e3cbdbecc00eeb62d11c74dfb19d6472af0` Split the owed-Leave suite section into functions under the parent's 100-line limit (issue #188)
- STOP conditions: none hit. No top-level port, parameter or register-map change: the RTL edits
  are one combinational block inside `protocol_processor_top` (the router-to-listener Failed bit),
  one expression inside `KL_srp_listener_fsm`, and comments.

## Round-2 items

| Item | Finding | Done |
|---|---|---|
| 1 | R666-001, R665-1-F2: REGISTERING_FAILED after two coalesced type changes | option (a): closed in RTL, regression AS5d/AS5e both directions, five planted controls, 05 §6.3 and PR body corrected, the "residual, not changed here" sentence removed |
| 2 | R665-1-F1: a suite check per documented settle arm | RB4-RB8 (the five arms) plus WK12 (the parked stream_id at the flop arm too), seven planted controls, coverage set WK1-WK12 and RB1-RB9; U6/U7 recorded as accepted likely equivalent |
| 2+ | found while checking U7: a sink with no record since reset "owed" an Empty for a stream_id it never held | fixed (`set_lv_w` gated on the record), RB9 and its control (see below) |
| 3 | R665-1-F3 and the R666-1 RESIDUE table | applied as written; executable labels, selectors and receipt strings unchanged |
| 4 | R665-1-S1 | not assigned, not done |

### Item 1: the coalesced swap (R666-001, R665-1-F2)

The event router keeps the FIRST payload of a source that strobes again before the consumer
acks (KL_pp_event_router, F02.6). The listener takes router events only from X_IDLE, so two
type changes of one sink while it is busy were one event whose payload Failed bit named the type
in between, and GET_RX_STATE kept it (R666-1 reproduced it with MAC TX held: 0x0042 after the
return to Advertise, 0x0002 after the return to Failed).

The top now drives the listener's `evt_tk_failed_i` from the SRP listener's registered-type level
of the presented source (`srp_tk_reg_state_w[k] == FAILED` for router source `EVR_TKREG_BASE_C +
k`), not from the payload. The listener latches it when it takes the event (X_IDLE) and writes
`srp_decl[1]` from it in X_ROM; a strobe in the cycle of the ack is a new event (the router's own
rule), so a change after the take raises another event. Strobe and level update on the same
clock edge in the SRP listener, so the level read is never older than the strobe. Table 5.30's
no-transition rule is untouched: the listener, its ROM and the generator are unchanged apart
from one comment; the payload still carries the type at strobe time to the trace ring.

Changes:

- `hdl/top/protocol_processor_top.sv:3300-3313` the `evt_tk_failed_live` block (was
  `assign lstn_evt_tk_failed_w = evr_pay_w[15];`).
- `hdl/acmp/KL_pp_acmp_listener.sv:1167-1169` the SOK bookkeeping comment.
- `tb/pp_top/sim_main.cpp:10075-10169` `as_coalesced_swaps_follow_the_last_type` (AS5d, AS5e);
  :9776 its call after AS5b/AS5c.
- `tb/pp_top/acmp_mutants.py:362-394` `COALESCE` (five controls); :414 `MUTANTS`; :20-23 the
  docstring.
- `docs/architecture/05_acmp_engine.md:318-326` the §6.3 cell note; :191-192 the §5.1 pointer.
- `tb/pp_top/README.md:2038-2047` AS5d/AS5e; :2103, :2111-2115 the controls.

### Item 2: the settle arms (R665-1-F1), and the no-record case

Checks in `tb/srp_stream_fsms/sim_main.cpp` section "an A15 settle never abandons the owed
Listener Leave" (expectations from the suite's own Table 10-3 model), one per documented arm, in
three new functions beside `settle_keeps_the_owed_listener_leave()` (RB1-RB3, :1089-1153):
`a_settle_while_parked_keeps_the_held_stream()` :1157-1227 (RB4-RB6),
`a_parked_leave_survives_txla_and_received_values()` :1231-1277 (RB7, RB8) and
`a_sink_with_no_record_owes_nothing()` :1282-1294 (RB9), each under the parent C++ gate's
100-line function limit; declared at :433-435 and called in `run()` at :1353-1355:

| Check | Arm (10 §6.4, banner) | Lines |
|---|---|---|
| RB4 | a settle while parked onto a third stream: the tx! sends the first stream's Lv, the tx! after it declares the third | :1166-1187 |
| RB5 | a rebind back to the parked stream, whose talker registers again: applicant kept, park cleared, New Ready, no Lv | :1189-1206 |
| RB6 | an LO applicant settled onto another stream: the tx! sends the held stream's Empty, then the new stream's New | :1208-1227 |
| RB7 | a txLA! walk while parked: nothing sent, park kept, then the held Empty, then New | :1237-1262 |
| RB8 | a received Listener value while parked (LO): not applied, the held Empty still goes out | :1264-1277 |
| RB9 | a sink with no record since reset, its applicant taken to LO by a received LeaveAll: the first settle owes nothing, New Ready, no Empty | :1282-1294 |

`tb/srp_stream_fsms/walk_main.cpp:542-567` WK12 (every declaring sink settled on a second and a
third stream before tx!: each Leave names the stream_id declared, at 1/1, 2/2, 3/5, 9/9), so the
flop arm of `csid_w` is reached too (the suite elaborates only the RAM arm); :315 its call.

The no-record defect: while checking R665's U7 ("likely equivalent"), a probe (scratch only)
showed that after a reset and a received LeaveAll, the first settle of a sink sent an Empty for a
stream_id the sink never held (the stale leave-copy word) and its New one T-MRP-JOIN late. That
was the round-1 #188 change: a received LeaveAll takes every sink's applicant from VO to LO,
records or not. `hdl/srp/KL_srp_listener_fsm.sv:609-610`: `set_lv_w` is VO for a sink with no
record, so it owes nothing (:601-602 the comment). With that, U7 (the same-value test without
`rec_valid_r`) is equivalent, not only likely: the test matters only when something is owed.

U6 (the retire keeps the old FourPacked) is not strictly equivalent: it shows as the parameter of
an Empty the sink sends before its next declaration, after a received LeaveAll takes its VO
applicant to LO. An Empty registers nothing; the assignment accepts U6 as likely equivalent, and
the srp_top README records both with that reasoning.

Other changes: `tb/srp_top/mutants.py:172-187` the comment and eight new arm entries and :303 the coverage
set (WK 12, RB 9); `tb/srp_top/mutations/` seven new patches (`listener-csid-ram-ignores-park`,
`listener-csid-flops-ignores-park`, `listener-rebind-back-keeps-park`, `listener-lo-not-owed`,
`listener-park-retires-on-txla`, `listener-parked-applies-rx`,
`listener-unrecorded-applicant-owes`) and three re-anchored on the new context with the same
edits (`listener-rebind-abandons-leave`, `listener-reprobe-abandons-leave`,
`listener-reprobe-parks-own-stream`); `docs/architecture/10_srp_engine.md:596-606` (§6.4: the
arms paragraph and the no-record sentence); READMEs `tb/srp_stream_fsms/README.md:8, 83-98, 229,
240, 247` and `tb/srp_top/README.md:707, 745-821`.

### Item 3: wording (R665-1-F3, R666-1 RESIDUE)

- F3: `docs/architecture/10_srp_engine.md:596` and the banner `hdl/srp/KL_srp_listener_fsm.sv:69-76`
  in the exact words of the review; the PR body row likewise.
- R666-002, every row: `tb/acmp_listener/sim_main.cpp:1178`; `tb/pp_top/sim_main.cpp:10039,
  10242`; `tb/srp_stream_fsms/sim_main.cpp:1075, 1095, 1120, 1136`;
  `tb/srp_stream_fsms/walk_main.cpp:36-40, 464, 532`; `tb/srp_top/mutants.py:162`. The new
  comments of this round carry no check labels either. Executable check labels, mutation
  selectors and receipt strings are unchanged.

## New checks, their planted controls and failing words

Every line below is from the head campaigns at cca12e3c (`receipts/round2/campaigns/head/`
`srp_top.log`, `acmp.log`; per-arm receipts listed in `receipts/round2/campaign-arms-head.csv`;
the per-arm FAIL sets are identical to the earlier head run at 518b3658,
`receipts/round2/compare/campaigns/{acmp,srp_top}-518b3658-vs-head.txt`), except RB4's words:
the srp_top driver keeps one receipt per label and `listener-csid-ram-ignores-park` also runs
the walk arms, so its suite run was repeated alone at cca12e3c from a fresh export
(`receipts/round2/extra/csid-ram-suite.log`, rc 2; RB4 and RB5 fail). Every control is KILLED.

| Check | Control (campaign) | Failing words |
|---|---|---|
| RB4 "a second rebind while parked: the next tx! sends the held stream's Lv, Ready" | `listener-csid-ram-ignores-park` (srp_top) | `FAIL: RB4: a second rebind while parked: the next tx! sends the held stream's Lv, Ready (1 pushes, code 5)` (the Lv names the middle stream) |
| RB4 "the tx! after it declares the third stream, New Ready" | `listener-park-never-retires`, `listener-declaration-not-held` | `... New Ready (0 pushes)` / `(1 pushes)` |
| RB5 "a rebind back to the parked stream keeps its applicant: the next tx! sends New Ready on it, no Lv" | `listener-rebind-back-keeps-park`; also `listener-csid-ram-ignores-park`, `listener-reprobe-parks-own-stream` | `... (1 pushes, code 5)` |
| RB6 "an LO applicant settled on another stream: the next tx! sends the held stream's Empty" | `listener-lo-not-owed`; also `listener-rebind-abandons-leave`, `listener-declaration-not-held` | `... (1 pushes, code 0)` |
| RB6 "the tx! after it declares the new stream, New Ready" | `listener-park-never-retires`, `listener-declaration-not-held` | `... (0 pushes)` / `(1 pushes)` |
| RB7 "a txLA! walk while parked sends nothing and keeps the park: the tx! after it sends the held stream's Empty" | `listener-park-retires-on-txla`; also `listener-declaration-not-held` | `... (quiet 1, 1 pushes, code 0)` |
| RB7 "the tx! after the Empty declares the new stream, New Ready" | `listener-park-never-retires`, `listener-declaration-not-held` | `... (0 pushes)` |
| RB8 "a Listener value received while parked is not applied: the next tx! sends the held stream's Empty" | `listener-parked-applies-rx`; also `listener-lo-not-owed`, `listener-rebind-abandons-leave` | `... (0 pushes, code -1)` |
| RB9 "a first settle after a received LeaveAll owes nothing: the next tx! sends New Ready and no Empty" | `listener-unrecorded-applicant-owes` | `... (1 pushes, code 4)` |
| WK12 "Leave i names the stream_id its sink held" | `listener-csid-flops-ignores-park` (1/1, 2/2), `listener-csid-ram-ignores-park` (3/5, 9/9); also the four WK11 leave-copy controls | e.g. `FAIL: WK12: Leave 0 names the stream_id its sink held (type 3, fp 2, stream_id 0011..9007) [2/2]` |
| WK12 "the listener walk sends N Leaves" | `listener-rebind-abandons-leave` (walk run) | `FAIL: WK12: the listener walk sends 5 Leaves (got 0) [3/5]` |
| WK12 "the listener walk pushes N stream_ids" | `listener-park-never-retires` (walk run) | `FAIL: WK12: the listener walk pushes 5 stream_ids (got 0) [3/5]` |
| WK12 "precondition: every listener applicant goes quiet" | `listener-aa-tx-stays-aa` | `FAIL: WK12 precondition: every listener applicant goes quiet [1/1]` (and 2/2, 3/5, 9/9) |
| AS5d/AS5e "after the queue drains GET_RX_STATE follows the last swap, REGISTERING_FAILED 0 (AS5d) or 1 (AS5e), byte-exact, with no arc: the queue held the six answers and nothing else" | `tk_failed_first_payload` (both; the base behaviour), `tk_failed_or_payload` (AS5d), `tk_failed_and_payload` (AS5e); also `rf_swap_sticky` (AS5d), `rf_swap_unlatched`, `tk_type_unlatched` (AS5e) | `FAIL: AS5d: ... (reg 1, decl 2, flags 0x0042, 6 answers, 6 ACMP frames)`, `FAIL: AS5e: ... (reg 2, decl 1, flags 0x0002, 6 answers, 6 ACMP frames)` |
| AS5d/AS5e "an unchanged refresh keeps it, byte-exact" | `tk_failed_first_payload` (both), `tk_failed_or_payload` (d), `tk_failed_and_payload` (e) | `FAIL: AS5d: an unchanged refresh keeps it, byte-exact (flags 0x0042)` |
| AS5d/AS5e "precondition: the listener took the two strobes as one coalesced TK_ATTR_REGISTERED" | `router_coalesce_unflagged` (both); also `tk_type_unlatched` | `... (taken 1, coalesced 0)` |
| AS5d/AS5e "precondition: with the four ordinary TX slots full, both type changes register" | `tk_type_unlatched` (both) | `... (free 1, reg 1 then 1)` |
| AS5d "precondition: the start type taken alone, GET_RX_STATE byte-exact" | `rf_swap_sticky` | `... (reg 1)` (the flags stay 0x0042 from AS5b) |
| AS5e "precondition: the start type taken alone, GET_RX_STATE byte-exact" | `tk_type_unlatched`, `rf_swap_unlatched` | `... (reg 1)` / `(reg 2)` |

Existing arms that break the settle path wholesale (`st_ls_index_zero`, `st_ls_settle_as_withdraw`,
`st_ls_sid_da_swapped`, `st_ls_state_none`, `st_ls_vid_dropped`, `cdl_not_44_rejected`) now also
fail every AS5d/AS5e line (`receipts/round2/compare/campaigns/acmp.txt`).

## Base and head records

Base ran in the scratch parent's submodule at cb8bab04; head in the lane at cca12e3c (clean, no
untracked files). Pinned Verilator 5.050, sv2v 0.0.12, Yosys 0.33 for the processor gates
(`receipts/round2/gates/*/tools.txt`). Logs, rc and seconds in `receipts/round2/gates/` and
`receipts/round2/campaigns/`; normalised diffs (roots, temporary names, timings, `all.v:N`) in
`receipts/round2/compare/gates/` and `compare/campaign-logs*`; per-arm FAIL-set comparisons in
`compare/campaigns/`. Every rc is 0.

| Processor gate | Base cb8bab04 | Head cca12e3c | Base vs head |
|---|---|---|---|
| `scripts/run_suites.sh` (REQ_TAG_LOG set) | rc 0, 1,030,051 checks, 0 failing | rc 0, 1,030,070, 0 failing | only pp_top 10,533 -> 10,543 (AS5d, AS5e), srp_stream_fsms 1,352 -> 1,361 (RB4-RB9, WK12) and the total |
| `check-req-tags.py --suites --evidence` | rc 0, 230 evidence lines | rc 0, 230 | identical |
| `scripts/lint_hdl.sh` | rc 0 | rc 0 | identical |
| `make check` | rc 0 | rc 0 | links 1,215 -> 1,216, ids 617 -> 625 files (the eight new patches); the rest identical |
| `scripts/gen_matrix.py --check` | rc 0 | rc 0 | identical |
| `syn/yosys/run.sh` | rc 0 | rc 0 | identical |
| `tb/elab_guards/guards.py --frontend yosys --jobs 4` | rc 0 | rc 0 | identical |

Campaigns that build a changed file:

| Campaign | Base | Head | Base vs head |
|---|---|---|---|
| `make -C tb/srp_top mutants` | rc 0, 168 of 168, coverage 94/94 | rc 0, 179 of 179, coverage 101/101 | 144 common logs identical; 11 existing arms (the round-1 settle and walk controls) now also fail RB4-RB8 or WK12; 8 new arms |
| `tb/pp_top/acmp_mutants.py` | rc 0, 60 of 60 KILLED | rc 0, 65 of 65 KILLED | 59 common logs identical; 8 existing arms now also fail AS5d/AS5e (`rf_swap_sticky`, `rf_swap_unlatched` and the six wholesale settle-path arms above); 5 new arms |
| `tb/srp_admission/mutants.py` | rc 0, 12 | rc 0, 12 | identical |
| `make -C tb/maap mutants` | rc 0, 32 | rc 0, 32 | identical |
| `make -C tb/adp_engine mutants` | rc 0, 62 | rc 0, 62 | identical |
| `make -C tb/pp_top aecp-mutants` | rc 0, 67 | rc 0, 67 | identical |
| `make -C tb/pp_top aecp-dispatch-mutants` | rc 0, 58 | rc 0, 58 | identical |
| `make -C tb/pp_top ctr-mutants` | rc 0, 18 | rc 0, 18 | identical |
| `tb/pp_top/gsi_mutants.py` | rc 0, 20 | rc 0, 20 | identical |
| `tb/pp_top/name_wr_mutant.py` | rc 0 | rc 0 | identical |
| `tb/pp_top/notify_mutants.py` | rc 0, 109 of 109 | rc 0, 109 of 109 | identical |
| `make -C tb/name_state mutants` | rc 0 | rc 0 | identical (completion order only) |
| `make -C tb/elab_guards mutants` | rc 0, 160 of 160 | rc 0, 160 of 160 | identical |
| `tb/pp_top/d3_mutants.py` | rc 0, 110 of 110 | rc 0, 110 of 110 | identical |

The host reset cut the head acmp, d3 and notify campaigns; they were rerun whole from empty
output directories (the cut logs in `receipts/round2/superseded/head-camps-cut/`). Records taken
at the superseded heads 0f9a4f2d and 518b3658 are kept beside them.

Reviewer probes at cca12e3c, from a fresh export (`receipts/round2/reviewer-checks/`):

- R665-1 `probes.py`: U1, U2, U3 and U5 KILLED by RB6/RB8, RB7, RB8 and WK12; U6 and U7 SURVIVED
  (accepted as likely equivalent, recorded in `tb/srp_top/README.md`).
- R666-1 `reviewer-probes.patch` (its pp_top call hunk placed by hand, the file has moved;
  `r666.apply.log`): the stalled and unstalled ACMP phases 68 checks, 0 failures each, the stream
  suite rc 0. Identical to the run at 518b3658.

## Scratch-parent consumer gate table

Parent: kebag-logic/milan-fpga dev `e9cbb676d7fdd6539aa408e5dfe38870a4ae1a5f`, every submodule
initialised, under the scratch root. Both patches applied in its working tree only
(`pp178-a634/parent-evidence-classification.patch`, `pp176-a629/parent-adoption-milan_dp-67.patch`);
working-tree diff sha256 ef322a60…dac at base and head. The protocol-processor gitlink was staged
at cb8bab04 (base), then at cca12e3c (head, fetched into the submodule from the lane), never
committed or pushed; every git command in the submodule was preceded by a top-level identity
check. `STATE.txt` in `receipts/round2/consumers/{base,head}` (and `STATE-resume.txt` for the
rerun `milan_dp`); diffs in `receipts/round2/compare/consumers*` and `compare/ooc/`.

| Parent consumer gate | Base cb8bab04 | Head cca12e3c | Base vs head |
|---|---|---|---|
| `check_cpp_idiom.py`, `check_rtl_source_lists.py`, `pp_srcs.py --check --selftest`, `check_port_contracts.py`, `measure_naming.py --check`, `measure_test_evidence.py --check`, `docs_check.py`, `check_sh_idiom.py`, `check_hygiene.py --check`, `check_sv_idiom.py`, `check_baremetal_only.py --check` | 0 each | 0 each | identical |
| `check_py_idiom.py` | 0 | 0 | line total 258,943 -> 258,992 (the processor's Python grew) |
| `tests: behave --no-capture -f plain` | 0 | 0 | identical (406 scenarios, 1,977 steps) |
| `syn/yosys/run.sh --mode elaborate --no-structural --top milan_datapath --top KL_pp_shadow --top KL_gptp_shadow` | 0 | 0 | cells: milan_datapath 74,816 -> 74,824, KL_pp_shadow 62,260 -> 62,286 |
| `sw/builder/test_builder.py` | 0 | 0 | "ALL GATES PASS EXCEPT 1 NOT RUN" at both (gate 11 needs a build tree not on this host); self-test finding counts and temp names vary run to run |
| `flock $VIVADO_LOCK python3 scripts/xvlog_gate.py --check` | 0 | 0 | only the pin line |
| `make -j16 -C tb/verilator/pp_shadow` | 0 | 0 | 609 + 609 + 649 + 317 checks, 0 failures at both; lines interleave (parallel binaries) |
| `make -j16 -C tb/verilator/nvm_cosim lint` / `quick JOBS=4 POOL=2` | 0 / 0 | 0 / 0 | identical |
| `make -j16 -C tb/verilator/milan_dp_render` | 0 | 0 | identical once sorted |
| `make -j16 -C tb/verilator/milan_dp SIM_JOBS=2` | 0 | 0 | 10,465 `[ok]`, 1,127 `[PASS]`, 0 failures at both, the check lines identical (`compare/consumers-checklines.txt`); timings differ. The head run was cut by the host reset and rerun whole |
| `syn/yosys/ooc.sh --record-rom-digests tcam` (ledger row recorded in the scratch tree, then restored) | 0 | 0 | rows: ltn_rom.hex 23cc67ee… and ucode.hex a3b62cab… at both pins |
| `syn/yosys/ooc_selftest.py` | 0 | 0 | identical |
| `syn/yosys/ooc.sh KL_pp_shadow` | 0 | 0 | LUT 56,701 -> 56,105 (LUT_TOT 60,937 -> 60,341); LUTRAM, FF, RAMB, DSP and CARRY4 unchanged |
| `lint_rtl.py --check --self-test --jobs 4` | 1 | 1 | identical: "hdl/milan has 3 violation(s), ratchet allows 2", from the parent's `KL_pp_shadow`/`milan_datapath` against processor main b48312e1 (the merge in the base); nothing in this round's diff |
| `check_submodule_docs.py` | 1 | 1 | identical: "documented pin differs from Git" and the stale pin diagram, which any moved gitlink fails until an adoption re-records the pin |

The two rc 1 gates fail identically at base and head and name nothing this round changes. Not
run: the parent's Vivado resource gate (`syn/ooc/pp_resource_gate.py check`), which needs a
Vivado route measurement.

## Output directory

`receipts/INDEX.md` is generated from the files present. Round-2 receipts are under
`receipts/round2/`: `gates/`, `campaigns/`, `consumers/` (base, head, OOC), `compare/`,
`reviewer-checks/`, `extra/`, `dev/`, `superseded/`, `scripts/`, `campaign-arms-{base,head}.csv`
and `EXTERNAL-RECORDS.csv` (sha256 and size of the eight logs over 200 KB kept in the scratch
root). Round-1 receipts are unchanged beside them.

## Round 1

The round-1 handoff is kept unchanged as `receipts/round2/HANDOFF-round1.md` (and the round-1 PR
body as `receipts/round2/PR-BODY-round1.md`).

## Final state

`[A651] REVIEW READY cca12e3cbdbecc00eeb62d11c74dfb19d6472af0` posted on processor issue #188
(issuecomment-6284903468). Lane clean at that head; nothing pushed; scratch parent never
committed.
