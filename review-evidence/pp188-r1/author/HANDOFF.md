# [A651] HANDOFF — processor #188 and #189 (listener lane)

Status: **REVIEW READY** at head `dc01aec48c7e397ab929e37596b60f43828829c8` (not pushed, no PR).

- Repository: Mister-M-alt/protocol-processor-control-plane-avb-milan (origin verified).
- Lane: branch `188-189-listener`, base main `5addf29759a22372ed6aa3e1d52a3aad29e3ecd7`.
- Commits (one-line subjects, no body, no trailers):
  - `9c8859add313bfc53b6dd7e9053665b31b5eb0a2` "Keep the owed Listener Leave when a bound sink settles again before tx! (issue #188)"
  - `dc01aec48c7e397ab929e37596b60f43828829c8` "Let GET_RX_STATE REGISTERING_FAILED follow the in-place Talker Advertise/Failed swap in SETTLED_RSV_OK (issue #189)"
- Assignment: issue #188 comment 6256482476 (read in full with issues #188 and #189).
- TAKEN: issue #188 comment 6256505724. REVIEW READY: issue #188 comment 6263032718 ("[A651] REVIEW READY dc01aec4…").
- STOP conditions: none hit. No register-map, top-level port or parameter change: the only RTL
  edits are inside `KL_srp_listener_fsm` (internal state, no port) and `KL_pp_acmp_listener`
  (one bookkeeping assignment).

## Two discrepancies in the lane brief, and what was done

1. The brief's scope rule ("no change outside E_SCFG, its tests, generators that must follow it,
   and the docs that record it") and its "Closes #179" belong to the SET_CONFIGURATION lane
   (#179 is closed and is about E_SCFG). The assignment comment on #188 requires changes in the SRP
   listener FSM and the ACMP listener. The assignment was followed; the change is confined to the
   listener path, its suites, their mutation campaigns and the docs that record it. PR-BODY.md says
   "Closes #188" and "Closes #189", the two issues the assignment names, not #179.
2. The brief says the CI-pinned Yosys is under the tools tree. It is not (searched). The processor
   gates used Yosys 0.33 (the version CI's Ubuntu package installs) from a local container layer; the
   parent gates used the host's 0.66, the parent's pinned `YOSYS_VERSION`. `receipts/toolchain.txt`.

Process notes:

- The two longest records (processor `run_suites.sh`, about 80 min at base under load, and every
  campaign) cannot finish inside one foreground command here. They ran detached under wrapper
  scripts that write each command's own exit status to an `.rc` file (never through a pipe), and the
  session polled them in the foreground until every one had finished. Nothing was left running.
- Commit 2 was amended three times before it became the head (`receipts/compare/head-history.txt`):
  bacfb90 (a README tally off by one, srp_stream_fsms 1353 -> 1352), ea5226c (B4/B4b reduced to four
  named checks, each with a planted control, instead of re-running the suite's per-transaction
  oracle), 2176035 (the acmp campaign found `st_ls_teardown_as_declare` SURVIVED: see "A control
  that changed"). Records taken at those trees are kept apart under `receipts/superseded/`. The
  srp_top and srp_admission campaigns ran on the bacfb90 tree; every file they copy is byte-identical
  at dc01aec4 except `tb/srp_stream_fsms/README.md` (one tally number), so they stand as head records.
  Commit 1 is unchanged; its README still reads 1353 for srp_stream_fsms, which commit 2 corrects.
- The AS6 VLAN check and the re-graded control ride in commit 2 although they follow from commit 1's
  behaviour; commit 1 alone leaves `st_ls_teardown_as_declare` surviving in the acmp campaign. Commit
  1 was not rewritten (no rebase).

## #188 design

`KL_srp_listener_fsm` forced the sink's applicant to VO on every A15 settle, abandoning a Listener
Lv still pending (LA) from the A8 before it. IEEE 802.1Q-2018 10.7.7 keeps one Applicant per
attribute value, and Table 10-3 takes AA/QA to LA on Lv! and sends the Leave from LA at tx!. The
settle now applies Lv! (as the A8 before it already did) and then, by the state that leaves:

| Applicant after Lv! | New stream_id vs the one the applicant holds | Settle does |
|---|---|---|
| LA or LO (Lv or Empty owed) | same (the re-probe) | keeps the applicant and its FourPacked parameter: the next tx! sends the Lv, or New if the talker registers again first (LA + New! = VN) |
| LA or LO | other (the rebind, or a third stream while one is parked) | arms the matcher on the new stream at once; parks the old stream_id in the leave copy (`lvp_r` set); while parked the Listener values of either stream are not applied and the declaration request waits; the parked tx! sends the owed message and clears `lvp_r`; the walk after that declares the new stream |
| VO, AO or QO | either | the new stream starts in VO at once (Table 10-3 note 11), as before |

A rebind back to the parked stream_id is "same": the applicant is kept and the park cleared.
Nothing back-pressures ACMP (`ctl_ready_o` unchanged). Δ13 (Milan v1.2 4.2.7.2.2) is untouched.
Cost: a new declaration that meets an owed Lv goes out one T-MRP-JOIN later; 64 bits per sink for
the leave copy and one 64-bit comparator. Parent Yosys pricing of `KL_pp_shadow`
(`syn/yosys/ooc.sh`): LUT 55,888 -> 55,820, LUTRAM 4,104 -> 4,236, LUT_TOT 59,992 -> 60,056,
FF 26,282 -> 26,296, CARRY4 2,381 -> 2,392, RAMB36/RAMB18/DSP unchanged.

## #189 design

In SETTLED_RSV_OK an EVT_TK_REGISTERED is the in-place Talker Advertise <-> Failed swap (802.1Q
35.2.6). Its F05.3 cell stays '—' (Milan Table 5.30 'x'): no arc, no action, no frame, no timer op,
no notification. `KL_pp_acmp_listener` now writes `srp_decl[1]` from the event's Failed bit there,
so GET_RX_STATE's REGISTERING_FAILED (Table 5.39) follows the swap both ways. The event router's
payload already carries the type at strobe time (end-to-end AS5b/AS5c prove it). The transition ROM
and its generator are unchanged (ltn_rom.hex 23cc67ee… at base and head).

## Changes (file:line at dc01aec4)

Commit 1 (#188):

- `hdl/srp/KL_srp_listener_fsm.sv`
  - :68-82 the design banner (the old trade-off at :67-71 replaced).
  - :371-373 `lvp_r`, the per-sink "old stream_id parked" bit.
  - :420 Listener values are not applied to a parked sink.
  - :525-529 the declaration request waits while parked; the settle comment.
  - :555-594 the leave copy beside the walk's copy: `lsid_r` in distributed RAM from three sinks
    (:568, :574-578, :581-583), flip-flops at one and two (:585-593); `csid_w`, the stream_id the
    control sink's applicant holds.
  - :596-611 `settle_app`: Lv! applied, "owes" (LA/LO), "same", the parked write `lv_take_w`.
  - :616-623 the walk publishes the parked stream_id while parked; `wnext_w`.
  - :639 reset; :693-697 the settle sets the applicant from `set_app_w`, sets `lvp_r`, keeps the
    FourPacked parameter of an owed message; :720-726 the parked tx! retires the park.
- `tb/srp_stream_fsms/sim_main.cpp:1072-1150` section M (RB1, RB2, RB3); :432, :1208 its call.
- `tb/srp_stream_fsms/walk_main.cpp:35-39` WK11 in the header; :353-371 `expect_leaves`;
  :452-468 WK8's re-settle now passes through WK11; :529-536 WK10's likewise.
- `tb/srp_top/mutants.py:161-171` nine arms; :264 coverage now WK1-WK11 and RB1-RB3.
- `tb/srp_top/mutations/`: nine new patches (`listener-rebind-abandons-leave`,
  `listener-declaration-not-held`, `listener-park-never-retires`, `listener-reprobe-abandons-leave`,
  `listener-reprobe-parks-own-stream`, `walk-ignores-leave-copy`, `lsid-ram-read-sink-0`,
  `lsid-flops-read-sink-0`, `lsid-ram-written-with-new-stream`); five walk-copy patches
  (`wsid-*`) re-anchored on the new context with the same edits.
- `tb/pp_top/sim_main.cpp:9700-9722` `has_listener_of`; :9771 and :10138-10197 AS7
  (`bind_and_settle`, `as_rebind_before_tx_sends_the_old_leave`).
- `tb/pp_top/acmp_mutants.py:329-340` `REBIND` (two controls).
- `docs/architecture/10_srp_engine.md:209` the leave copy in the §5.1 storage table; :240-242 the
  cost table's note; :529-548 "A settle while a Leave is still owed" in §6.4.
- READMEs: `tb/srp_stream_fsms/README.md:73-83, 213, 224-233`; `tb/srp_top/README.md:670, 713,
  736-763`; `tb/pp_top/README.md` AS7 and the REBIND rows.

Commit 2 (#189, plus the AS6 follow-up):

- `hdl/acmp/KL_pp_acmp_listener.sv:1162-1171` the SOK bookkeeping.
- `tb/acmp_listener/sim_main.cpp:404-408` the model's same bookkeeping (05 §6.3 cell note);
  :1178-1206 B4 and B4b.
- `tb/pp_top/sim_main.cpp:9681-9692` `failed()`; :9719-9722 `rx_state_settled` flags; :9769 and
  :10032-10067 AS5b/AS5c; :10096-10108 AS6's VLAN-release check.
- `tb/pp_top/acmp_mutants.py:116, :123-128` the VLAN-release name and the re-graded
  `st_ls_teardown_as_declare`; :342-360 `SWAP` (four controls); :18-20 the docstring; :361 `MUTANTS`.
- `docs/architecture/05_acmp_engine.md:314-320` the cell note.
- READMEs: `tb/acmp_listener/README.md:7, 36-37, 176-197`; `tb/pp_top/README.md:2033-2058, 2082,
  2094-2109`; `tb/srp_stream_fsms/README.md:8` (tally 1352).

## Accepted cases and refusal cases

This lane has no length or refusal rule (no command format changed). Its cases are the settle
table above and, for #189: in SETTLED_RSV_OK a Failed registration sets REGISTERING_FAILED and an
Advertise registration clears it; in every other state the rule is unchanged (SNR's TK_REG takes its
A11 arc and latches the type as before; GET_RX_STATE outside SOK reports 0, F05.14).

## New checks, their planted controls and failing words

Receipts: `receipts/compare/new-checks.txt` (every FAIL line of every arm).

| Check | Control (campaign) | Failing words |
|---|---|---|
| RB1 "the new stream registers at once, its Listener not yet declared" | `listener-declaration-not-held` (srp_top) | `FAIL: RB1: the new stream registers at once, its Listener not yet declared (reg 1, decl 2)` |
| RB1 "the next tx! sends the old stream's Lv, Ready, and nothing else" | `listener-rebind-abandons-leave`, `listener-declaration-not-held` | `... (0 pushes, code -1)` / `(1 pushes, code 0)` |
| RB1 "the tx! after it declares the new stream, New Ready" | `listener-park-never-retires`, `listener-declaration-not-held` | `... (0 pushes, decl 0)` / `(1 pushes, decl 0)` |
| RB2 "after a re-probe onto the same stream the next tx! sends its Lv, Ready" | `listener-reprobe-abandons-leave` | `... (0 pushes, code -1)` |
| RB3 "a re-probe whose talker registers before tx! sends New Ready on the same stream, no Lv" | `listener-reprobe-parks-own-stream` | `... (1 pushes, code 5)` |
| WK11 "the listener walk sends N Leaves" | `wsid-write-ignores-ready` | `FAIL: WK11: the listener walk sends 1 Leaves (got 0) [3/5]`, `[9/9]` |
| WK11 "Leave i names the stream_id its sink held" | `walk-ignores-leave-copy` (1/1, 2/2, 3/5, 9/9), `lsid-ram-read-sink-0` (3/5, 9/9), `lsid-flops-read-sink-0` (2/2), `lsid-ram-written-with-new-stream` (3/5, 9/9) | e.g. `FAIL: WK11: Leave 1 names the stream_id its sink held (type 3, fp 2, stream_id 0011..1007) [3/5]` |
| AS7 "a rebind settled N ms after a T-MRP-JOIN, before the next: that MRPDU carries the old stream's Lv and nothing for the new one" | `rebind_abandons_leave` (acmp; the base behaviour) | `FAIL: AS7: a rebind settled 6 ms after a T-MRP-JOIN, before the next: ... (ready 1, settled 1, quiet 1)` |
| AS7 "the MRPDU after it declares the new stream, New Ready" | `park_never_retires` (acmp) | `FAIL: AS7: the MRPDU after it declares the new stream, New Ready (decl 0, reg 1)` |
| B4 "no invented arc; the swap to Talker Failed latches RF" and "after the swap to Talker Failed GET_RX_STATE carries REGISTERING_FAILED 0x0040" | `rf_swap_unlatched` (acmp, acmp_listener; the base behaviour) | `... (flags 0x0002)`; also `F05.3 TK_REG x SOK` and `B4 REF-BUG` record checks |
| B4b "no invented arc; the swap back to Talker Advertise clears RF" and "after the swap back GET_RX_STATE clears REGISTERING_FAILED" | `rf_swap_sticky` (acmp, acmp_listener) | `... (flags 0x0042)` |
| AS5b "after the in-place swap to Talker Failed: FAILED registered, Asking Failed declared, and GET_RX_STATE carries REGISTERING_FAILED (Milan Table 5.39), byte-exact" | `rf_swap_unlatched` (acmp, pp_top) | `... (reg 2, decl 1)` |
| AS5c "after the swap back to Talker Advertise: ... GET_RX_STATE clears REGISTERING_FAILED, byte-exact" | `rf_swap_sticky` (acmp, pp_top) | `... (reg 1, decl 2)` |
| AS6 "the sink's VLAN membership is released: MVRP Lv of VID 2" (new) | `st_ls_teardown_as_declare`, `st_ls_teardown_lost` (acmp) | `FAIL: AS6: the sink's VLAN membership is released: MVRP Lv of VID 2` |

The two controls marked "the base behaviour" are the base RTL's own logic, so the end-to-end checks
reproduce the qualification run's observations on the base.

### A control that changed

`st_ls_teardown_as_declare` (the top's service stage issues the A8 teardown as a settle) was graded
by "AS6: the Listener attribute is withdrawn on the wire". Since #188 a settle withdraws the old
Listener declaration too, so that teardown still puts the Lv on the wire: at 21760351 the control
SURVIVED in the acmp campaign, and the full default pp_top run (10,021 checks) passed with it planted
(probe in scratch). What it still breaks is the VLAN release (a settle adds a membership where the
teardown removes one). AS6 now checks MVRP's Lv of the sink's VID, and the control names that check.

## Base and head records

Base ran in the scratch parent's submodule at 5addf297; head in the lane at dc01aec4. Pinned
Verilator 5.050, sv2v 0.0.12, Yosys 0.33 (processor), Python 3.14. `receipts/compare/records.txt`,
`receipts/compare/gates/*.diff` (normalised: roots, temporary names, timings, `all.v:N`).

| Processor gate | Base | Head | Identical? |
|---|---|---|---|
| `scripts/run_suites.sh` (REQ_TAG_LOG set) | rc 0, 1,030,013 checks, 0 failing | rc 0, 1,030,026, 0 failing | only acmp_listener 3,167 -> 3,170, pp_top 10,519 -> 10,524, srp_stream_fsms 1,347 -> 1,352 and the total |
| `check-req-tags.py --suites --evidence` | rc 0, 227 evidence lines | rc 0, 229 | +2 tags (REQ-ACMP-022 at AS5b, REQ-ACMP-018 at AS7) |
| `scripts/lint_hdl.sh` | rc 0 | rc 0 | yes |
| `make check` | rc 0 | rc 0 | links 1,196 -> 1,205, ids 593 -> 602 files (the nine new patches), req-tags 227 -> 229 |
| `scripts/gen_matrix.py --check` | rc 0 | rc 0 | yes |
| `syn/yosys/run.sh` | rc 0 | rc 0 | yes after `all.v:N` |
| `tb/elab_guards/guards.py --frontend yosys --jobs 4` | rc 0 | rc 0 | yes after `all.v:N` |

Campaigns that build a changed file (`receipts/compare/campaigns.txt`, per-arm FAIL-set comparison):

| Campaign | Base | Head | Identical? |
|---|---|---|---|
| `make -C tb/srp_top mutants` | rc 0, 137 of 137, coverage 86/86 | rc 0, 146 of 146, coverage 90/90 | 129 common logs identical; `wsid-write-ignores-ready` also fails WK11 now (2 lines); 9 new arms |
| `tb/srp_admission/mutants.py` | rc 0, 12 | rc 0, 12 | yes |
| `make -C tb/maap mutants` | rc 0, 32 | rc 0, 32 | yes |
| `make -C tb/adp_engine mutants` | rc 0, 62 | rc 0, 62 | yes |
| `make -C tb/pp_top aecp-mutants` | rc 0, 67 | rc 0, 67 | yes |
| `make -C tb/pp_top aecp-dispatch-mutants` | rc 0, 58 | rc 0, 58 | yes |
| `make -C tb/pp_top ctr-mutants` | rc 0, 18 | rc 0, 18 | yes |
| `tb/pp_top/acmp_mutants.py` | rc 0, 51 of 51 KILLED | rc 0, 57 of 57 KILLED | 45 common logs identical; 12 existing arms now also fail the new AS5b/AS5c/AS6/AS7 or B4/B4b checks, and `st_ls_teardown_as_declare` fails AS6's VLAN check instead of the Lv check (`receipts/compare/acmp-camp.txt`); 6 new arms |
| `tb/pp_top/gsi_mutants.py` | rc 0, 20 | rc 0, 20 | yes |
| `tb/pp_top/name_wr_mutant.py` | rc 0 | rc 0 | yes |
| `tb/pp_top/notify_mutants.py` | rc 0, 109 of 109 | rc 0, 109 of 109 | yes |
| `make -C tb/name_state mutants` | rc 0 | rc 0 | yes |
| `make -C tb/elab_guards mutants` | rc 0, 160 of 160 | rc 0, 160 of 160 | yes after `all.v:N` |
| `tb/pp_top/d3_mutants.py` | rc 0, 110 of 110 | rc 0, 110 of 110 | yes |

Not run: `tb/aecp_cmds` mutants, `tb/acmp_talker/retry_mutants.py` and `tb/nvm_port` figures, which
build none of the changed files. No Vivado synthesis or route; no hardware.

## Scratch-parent consumer gate table

Parent: kebag-logic/milan-fpga dev `e9cbb676d7fdd6539aa408e5dfe38870a4ae1a5f`, every submodule
initialised, under the scratch root. Both patches applied in its working tree only:
`pp178-a634/parent-evidence-classification.patch` (sha256 76625170…495e, 2,689 B) and
`pp176-a629/parent-adoption-milan_dp-67.patch` (sha256 e142e2e7…66d3, 1,541 B); working-tree diff
sha256 ef322a60…dac at base and head. The protocol-processor gitlink was staged at 5addf297 (base)
and then at dc01aec4 (head, fetched into the submodule from the lane), never committed or pushed.
Every git command in the submodule was preceded by a top-level identity check. `STATE.txt` in each
`receipts/consumers/{base,head}`; diffs in `receipts/compare/consumers/`.

| Parent consumer gate | Base 5addf297 | Head dc01aec4 | Base vs head |
|---|---|---|---|
| `check_cpp_idiom.py`, `check_rtl_source_lists.py`, `pp_srcs.py --check --selftest`, `check_port_contracts.py`, `measure_naming.py --check`, `measure_test_evidence.py --check`, `docs_check.py`, `check_sh_idiom.py`, `check_hygiene.py --check`, `check_sv_idiom.py`, `check_baremetal_only.py --check` | 0 each | 0 each | identical |
| `check_py_idiom.py` | 0 | 0 | line total 258,851 -> 258,899 (the processor's Python grew) |
| `lint_rtl.py --check --self-test --jobs 4` | 0 | 0 | identical (90 <= ratchet 90) |
| `tests: behave --no-capture -f plain` | 0 | 0 | identical (406 scenarios, 1,977 steps) |
| `syn/yosys/run.sh --mode elaborate --no-structural --top milan_datapath --top KL_pp_shadow --top KL_gptp_shadow` | 0 | 0 | cells: KL_pp_shadow 61,970 -> 62,211, milan_datapath 74,537 -> 74,767 |
| `sw/builder/test_builder.py` | 0 | 0 | "ALL GATES PASS EXCEPT 1 NOT RUN" at both (gate 11 needs a build tree not on this host); the self-tests' finding counts and temp names vary run to run |
| `flock $VIVADO_LOCK python3 scripts/xvlog_gate.py --check` | 0 | 0 | only the pin line; 0 findings. The first base attempt waited on another holder of the lock and was cut (kept as `xvlog.lockwait-cut`), then rerun at base |
| `make -j16 -C tb/verilator/pp_shadow` | 0 | 0 | 609 + 609 + 649 + 317 checks, 0 failures at both; lines interleave (parallel binaries) |
| `make -j16 -C tb/verilator/nvm_cosim lint` / `quick JOBS=4 POOL=2` | 0 / 0 | 0 / 0 | identical |
| `make -j16 -C tb/verilator/milan_dp_render` | 0 | 0 | the 5 PASS lines identical; the head reused the generated images (inputs unchanged), so the generators' lines appear at base only |
| `make -j16 -C tb/verilator/milan_dp SIM_JOBS=2` | 0 | 0 | 10,465 `[ok]`, 1,127 `[PASS]`, 0 failures at both, the check lines identical; timings and the ROM generators' lines (base only) differ |
| `syn/yosys/ooc.sh --record-rom-digests tcam` (ledger row recorded in the scratch tree, then restored) | 0 | 0 | rows: ltn_rom.hex 23cc67ee… and ucode.hex a3b62cab… at both pins |
| `syn/yosys/ooc_selftest.py` | 0 | 0 | identical (needs the ledger row: the run inside the consumer pass refused setup at both, rc 2, before the row existed) |
| `syn/yosys/ooc.sh KL_pp_shadow` | 0 | 0 | the area row in "#188 design" above |
| `check_submodule_docs.py` | 1 | 1 | identical: "documented pin differs from Git" and the stale pin diagram, which any moved gitlink fails until an adoption re-records the pin |

Not run: the parent's Vivado resource gate (`syn/ooc/pp_resource_gate.py check`), which needs a
Vivado route measurement.

## Output directory

| Path | Contents |
|---|---|
| `HANDOFF.md`, `PR-BODY.md` | this file; the PR body for a new processor PR |
| `receipts/INDEX.md` | generated from the files present |
| `receipts/toolchain.txt` | tool identities |
| `receipts/compare/` | records.txt, campaigns.txt, acmp-camp.txt, new-checks.txt, head-history.txt, gate/consumer/ooc diffs |
| `receipts/gates/{base,head}`, `receipts/campaigns/{base,head,head-bacfb90}`, `receipts/consumers/{base,head,ooc-base,ooc-head}` | every record's log, rc and seconds (host paths replaced) |
| `receipts/campaign-arms-*.csv`, `receipts/EXTERNAL-RECORDS.csv` | sha256 and size of every per-arm receipt and of the logs over 200 KB, kept in the scratch root |
| `receipts/superseded/` | records taken at the superseded commit-2 trees |
| `receipts/scripts/` | the wrappers and comparison scripts that produced the records |

## Final state

- Lane: `188-189-listener` at dc01aec4, clean, build outputs removed (`git clean -fdX`). Not pushed.
- Scratch parent: dev e9cbb676, gitlink staged at dc01aec4, both patches in its working tree; nothing
  committed or pushed. No job of this lane is running.
- Issue #188: "[A651] TAKEN" (6256505724) and "[A651] REVIEW READY dc01aec48c7e…" (6263032718).
  No other comment posted or edited.
