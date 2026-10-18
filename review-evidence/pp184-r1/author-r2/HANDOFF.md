# [A648] #184 HANDOFF: MSRP Domain re-declaration JoinMt unless a Domain registration is IN

Status (round 1): REVIEW READY at head e11fb36b; round 2 at the end of this file. Every processor gate and every campaign that builds a changed
file is rc 0 at base and head; the parent consumer gates match base (two fail identically at
both, for reasons owned outside this lane: see the parent table).

- Repository: Mister-M-alt/protocol-processor-control-plane-avb-milan
- Branch: `184-domain-joinmt`, one commit on processor main 08ae00130f096f241463172c4781885934400ee4
- Head: e11fb36b366587b5e2403c5d47452c16aae6ec31
  "MSRP Domain re-join: JoinIn only while the declared Domain is registered, JoinMt otherwise (#184)"
- Assignment: issue #184 comment 6249574916. TAKEN: comment 6249589579 (2026-10-18T13:52:51+02:00).
- REVIEW READY: comment 6253204124 (2026-10-18T19:56:30+02:00), naming head e11fb36b366587b5e2403c5d47452c16aae6ec31.
- Not pushed, no PR (both not allowed in this session). PR-BODY.md is beside this file.

## Clauses read (local texts)

- IEEE 802.1Q-2018 10.7.6.3 (sJ: JoinIn if the Registrar is IN, JoinMt if MT or LV), 10.7.6.6
  (sLA gives rise to rLA! on every Registrar of the participant), Table 10-3, Table 10-4
  (Registrar: rNew/rJoinIn/rJoinMt to IN; rLv!/rLA!/txLA! IN to LV; Begin!/Flush! to MT),
  Table 10-5, Clause 35.2.1.4 h), 35.2.2.9 (Domain FirstValue), 35.2.4 (no MAP function for
  Domain attributes).
- Milan v1.2 4.2.7.1, 4.2.7.2.1 (defaults at startup and Link Up; adopt a differing Class A
  Domain), 4.2.7.2.2 (MSRP Registrar IN / rLv! goes to MT with Lv, no leavetimer).
- Processor: README, hdl/README rules, docs/guides/hdl-engineer.md, docs 09 (sections 1-8),
  docs 10 (all), `hdl/srp/KL_srp_domain.sv`, `KL_srp_top.sv`, `KL_srp_encoder.sv` (intake and
  drain), `KL_srp_talker_fsm.sv` (walk timing, sJ in the stream FSMs), the CI workflow,
  `scripts/run_suites.sh`, `lint_hdl.sh`, `syn/yosys/run.sh`, `scripts/check_upc_map.py`,
  `hdl/aecp/ucode/gen_ucode.py` and `KL_aecp_engine.sv` OP_*_C (untouched by this change),
  `hdl/acmp/rom/gen_ltn_rom.py` (untouched; ROM digests below).

## Design

1. **Registrar.** `KL_srp_domain` keeps one bit for the Registrar of its declared value
   (1 = IN, 0 = MT or LV). LV is folded into MT: sJ encodes the two alike (10.7.6.3), and
   nothing else reads the Domain registration (35.2.4 gives the Domain no MAP; an adopted
   Domain is kept until LINK_DOWN, F10.2). So no leavetimer and no timer slot are added.

   | Event for the declared value | Registrar | Re-join |
   |---|---|---|
   | received New, JoinIn or JoinMt | IN | JoinIn |
   | received Lv | IN to MT at once (Milan 4.2.7.2.2) | JoinMt |
   | LeaveAll on the Domain lane (received) or the own sLA | IN to LV | JoinMt until re-declared |
   | LINK_UP (Begin!), LINK_DOWN (Flush!) | MT | JoinMt |
   | adoption of a received value | that value's registration (IN unless its Lv came first) | JoinIn / JoinMt |

   Events of other values do nothing; received In/Mt never register (Table 10-4 has no such
   row). A received event wins over a LeaveAll in the same clock, as the stream registrars
   do (10 6.5).
2. **Hand-over timing.** The code is chosen when the re-join is handed to the encoder.
   `periodic!` and the own LeaveAll (its sLA comes on the round's tx! clock) hand over at
   once, exactly as on main. A LeaveAll outside a tx! clock is a received one; its re-join
   waits for the next tx! (`KL_srp_top`'s `join_fsm_w`), the drain it would have reached
   anyway, so a peer's Domain declaration later in its LeaveAll MRPDU registers first.
   A first version issued every re-join at tx!; it moved each periodic re-join one
   T-MRP-JOIN later (the periodic expiry follows the join expiry in the same millisecond)
   and failed srp_top N12, O1, O2 and O7, whose own-LeaveAll timelines rest on the main
   timing. It was replaced before the commit; no record below is from it.
3. **Own LeaveAll is JoinMt.** 10.7.6.6 / Table 10-4 txLA! take the Registrar to LV at
   the sLA, so the re-join in the own LeaveAll MRPDU is JoinMt; the next one is JoinIn again
   once the peer re-declares. This is the 10.7.6.3 reading; an owner who wants JoinIn there
   would be asking for an exception to the clause.
4. **Single New** at startup and LINK_UP is unchanged (D1, D9, DR11, srp_top 0, pp_top S1/DV2/DV6).

## Changes (file:line at head e11fb36b)

- `hdl/srp/KL_srp_domain.sv`
  - :26-42 banner: the sJ rule, the Registrar, the hand-over timing (issue #184).
  - :72 new input `rxdom_lv_i` (received Domain Lv strobe); :77 new input `tx_tick_i`;
    :81 output comment now lists JoinMt (3).
  - :97 `EV_JOINMT_C`; :117 `rxla_pend_r`; :121-122 `reg_in_r`, `pend_in_r`.
  - :141-145 `rx_is_decl_w`, `rx_is_pend_w`; :149-160 `registrar_next` (Table 10-4 with the
    Milan cell, receive-over-LeaveAll priority).
  - :188-189 Registrar registers; :203 a captured adoption is registered by its own event;
    :205-214 hand-over: periodic! and own sLA at once, a received LeaveAll held for tx!.
  - :229-230 Flush! on LINK_DOWN; :237-238 Begin! on LINK_UP; :249 adoption carries the
    adopted value's registration; :257 the re-join is `reg_in_r ? JoinIn : JoinMt`.
  - The three lines `tb/pp_top/notify_mutants.py` anchors on are byte-identical.
- `hdl/srp/KL_srp_top.sv` :348, :362-366 `dom_rx_lv_w` (Class A Domain Lv from the decoder);
  :380 `.rxdom_lv_i`; :383 `.tx_tick_i (join_fsm_w)`. Ports and parameters unchanged.
- `tb/srp_encoder/srp_tb_wrap.sv` :64, :67, :182, :185 the two new inputs exposed.
- `tb/srp_encoder/sim_main.cpp` :392-409 helpers `dom_cadence`, `dom_rx`; :492-494 reset
  defaults; :999, :1005, :1089, :1395 D2, D3, D8, B1 follow the rule; :1111-1251 DR1-DR11
  in three functions (each under the parent's 100-line function limit).
- `tb/srp_top/sim_main.cpp` :299 `dom_rejoin_in`; :628 group `domjoin`; :1964 Q2 Domain
  JoinMt (no peer); :2327 F1 Domain JoinMt in the own LeaveAll cycle; :2526, :2547, :2553
  the F5c negatives look for any Domain re-join (JoinIn or JoinMt), so they stay meaningful;
  :2953-2990 DJ1-DJ4.
- `tb/srp_top/mutants.py` :161-182 fifteen arms (21 runs); :276 coverage requires DJ1-DJ4.
- `tb/srp_top/mutations/` fifteen new patches (listed below).
- `docs/architecture/10_srp_engine.md` :190-194 singleton state; :267-268 F10.2 re-join
  edges; :271-313 "Re-join encoding (issue #184)"; :642-643 transmit paragraph; :664
  Domain row of the lane table.
- `tb/srp_encoder/README.md` :6 count 593; :73-102 hand-over and DR1-DR11; :124-140 arms.
- `tb/srp_top/README.md` :61-63 F1; :82-84, :88-90 F5b/F5c; :251 group list; :446 Q2;
  :463-494 section DJ and its arms.
- `tb/pp_top/README.md` :2578, :2581 Domain strobe line citations (`:252`, `:219`).

No register-map change, no top-level port or parameter change (`protocol_processor_top`
and `KL_srp_top` ports and parameters are byte-identical), no generator or ROM change.

## Behaviour: what is encoded when

- No peer Domain: every periodic and LeaveAll re-join is JoinMt (DR1, D2, D3, DJ1, Q2).
- Peer declaring the same Domain: JoinIn (DR2, DJ2); a bridge LeaveAll MRPDU that
  re-declares its Domain: JoinIn (DR3, DJ3).
- Own LeaveAll: JoinMt (DR4, F1); back to JoinIn after the peer re-declares (DR5).
- Peer withdrawal (Lv): JoinMt from the next re-join on (DR6, DJ4); an Lv of another
  value changes nothing (DR7).
- A re-join already handed to the encoder keeps its code; it waits at most one T-MRP-JOIN.

## New checks and planted mutants

Every new check is the required named failure of at least one arm of
`tb/srp_top/mutants.py`; the campaign fails if any arm is not killed by its named check.

| Arm (patch in `tb/srp_top/mutations/`) | Planted defect | Required failing check (suite) | Failing words |
|---|---|---|---|
| `domain-rejoin-always-joinin` | every re-join JoinIn (main's behaviour) | DR1 (srp_encoder) | `FAIL: DR1 no peer: the periodic re-join is JoinMt {6, 3, 2}` |
| same | | DJ1 (srp_top domjoin) | `FAIL: DJ1: no peer Domain: our re-join is JoinMt, got 1` |
| same | | Q2 (srp_top timers) | `FAIL: Q2: periodic! re-joins recur every 900-1500 ms (...)` |
| `domain-rejoin-always-joinmt` | every re-join JoinMt | DR2, DR5 (srp_encoder) | `FAIL: DR2 peer declaring: ...`, `FAIL: DR5 LV re-joins JoinMt until the peer re-declares, then JoinIn` |
| same | | DJ2 (srp_top domjoin) | `FAIL: DJ2: the peer declaring our Domain: JoinIn, got 3` |
| `domain-rejoin-at-request` | a received LeaveAll's re-join handed over at once | DR3a | `FAIL: DR3a a received LeaveAll's re-join waits for tx!` |
| `domain-rx-leaveall-dropped` | a received LeaveAll's re-join never handed over | DR3; DJ3 | `FAIL: DR3 a peer LeaveAll re-declared before tx!: ...`; `FAIL: DJ3: ... got -1` |
| `domain-leaveall-keeps-in` | a LeaveAll leaves IN | DR4 | `FAIL: DR4 own LeaveAll: the registration is LV at its tx!, JoinMt` |
| `domain-lv-ignored` | a received Lv leaves IN | DR6; DJ4 | `FAIL: DR6 peer withdrawal (Lv): ...`; `FAIL: DJ4: the peer's Lv: the next re-join is JoinMt, got 1` |
| `domain-lv-any-value` | an Lv of any value clears IN | DR7 | `FAIL: DR7 an Lv of another Domain value leaves the registration IN` |
| `domain-leaveall-after-receive` | the LeaveAll wins its clock over a received event | DR8 | `FAIL: DR8 a registering event in the LeaveAll's clock keeps IN: JoinIn` |
| `domain-adoption-drops-registrar` | an adoption clears the registration | DR9 | `FAIL: DR9 the adopted value is registered: ...` |
| `domain-capture-unregistered` | the captured adoption is not registered | DR9 | same |
| `domain-pending-lv-ignored` | an Lv of the pending adoption is lost | DR10 | `FAIL: DR10 an adoption withdrawn before it applies re-joins JoinMt` |
| `domain-link-keeps-registrar` | LINK_DOWN and LINK_UP keep IN | DR11 | `FAIL: DR11 LINK_DOWN and LINK_UP clear the registration: New, then JoinMt` |
| `top-domain-lv-unwired` | `KL_srp_top` ties the Domain Lv strobe to 0 | DJ4 | `FAIL: DJ4: ... got 1` |
| `top-domain-tx-every-clock` | `KL_srp_top` ties `tx_tick_i` to 1 | DJ3 | `FAIL: DJ3: ... got 3` |
| `top-domain-tx-unwired` | `KL_srp_top` ties `tx_tick_i` to 0 | DJ3 | `FAIL: DJ3: ... got -1` |

Per-arm failure counts are in the suite READMEs and the campaign record below.

## Base and head records

Where each side ran. Base processor gates: the scratch parent's submodule checked out at
08ae0013. Head processor gates: the lane tree at e11fb36b (cleaned of ignored files before and
after). Campaigns and the elaboration-guard grading: `git archive` exports of each commit
(632 and 647 blobs rehashed against the commit trees, 0 mismatches). Same pinned tools on both
sides; nothing piped. `RECORDS.tsv` beside this file lists every log with rc, size and
sha256; the logs and receipts stay in the scratch root.

| Record | Base 08ae0013 | Head e11fb36b | Identity |
|---|---|---|---|
| `scripts/run_suites.sh` (REQ_TAG_LOG set) | rc 0, 1,030,000 checks | rc 0, 1,030,016 checks | identical except srp_encoder 581 -> 593 (+12: DR1-DR11 with DR3a) and srp_top 8,656 -> 8,660 (+4: DJ1-DJ4); pp_top 10,519 at both |
| `check-req-tags.py --suites --evidence` (CI's executed half) | rc 0, 226 evidence lines, 14 suites | rc 0, 227, 14 | identical except the new REQ-SRP-005 tag (DR6) and moved line numbers |
| `scripts/lint_hdl.sh` | rc 0 | rc 0 | identical |
| `make check` | rc 0 | rc 0 | identical except links 1,196 -> 1,202, REQ tags 226 -> 227, ID-scanned files 592 -> 607 (the 15 new patches) |
| `scripts/gen_matrix.py --check` | rc 0 | rc 0 | identical |
| `syn/yosys/run.sh` (sv2v 0.0.12, Yosys 0.66) | rc 0 | rc 0 | identical except the `all.v` line numbers of three existing Yosys memory warnings (the Domain module is longer) |
| `tb/elab_guards/guards.py --frontend yosys` (CI portability) | rc 0, 93/93 | rc 0, 93/93 | identical except `all.v` line numbers in five refusal texts; the base run from the submodule and from the export are identical |

Campaigns that build a changed file (`KL_srp_domain.sv`, `KL_srp_top.sv`, the srp_encoder and
srp_top benches); "receipts" compares each arm's sorted failing-check lines:

| Campaign | Base | Head | Identity |
|---|---|---|---|
| `tb/srp_top/mutants.py` (SRP LeaveAll campaign; CI) | rc 0, 137 checks, coverage 86/86 | rc 0, 159 checks, coverage 90/90 | 130 common receipts identical; +1 control (domjoin) and the 21 new arm runs, all KILLED by their named check |
| `tb/srp_admission/mutants.py` | rc 0, 12/12 | rc 0, 12/12 | identical |
| `tb/pp_top/aecp_mutants.py` (CI) | rc 0, 67/67 | rc 0, 67/67 | identical, 67 receipts |
| `tb/pp_top/aecp_dispatch_mutants.py` (CI) | rc 0, 58/58 | rc 0, 58/58 | identical, 59 receipts |
| `tb/pp_top/ctr_mutants.py` | rc 0, 18/18 | rc 0, 18/18 | identical |
| `tb/pp_top/notify_mutants.py` (includes the Domain adoption arms) | rc 0, 98 of 98 | rc 0, 98 of 98 | identical as a set (print order follows completion); 112 receipts identical |
| `tb/pp_top/gsi_mutants.py` | rc 0, 20 detected | rc 0, 20 detected | identical |
| `tb/pp_top/name_wr_mutant.py` | rc 0 | rc 0 | identical |
| `tb/pp_top/acmp_mutants.py` | rc 0, 51 of 51 | rc 0, 51 of 51 | identical |
| `tb/pp_top/d3_mutants.py` | rc 0, 110 of 110 | rc 0, 110 of 110 | identical, 117 receipts |
| `tb/adp_engine/mutants.py` (CI) | rc 0, 62/62 | rc 0, 62/62 | identical |
| `tb/maap/mutants.py` (CI) | rc 0, 32/32 | rc 0, 32/32 | identical |
| `tb/name_state/mutants.py` | rc 0 | rc 0 | identical, 124 receipts |
| `tb/elab_guards/mutants.py` | rc 0, 160 of 160 | rc 0, 160 of 160 | identical, 161 receipts |

Not run, because they build no changed file: `tb/aecp_cmds` mutants (AECP engine only),
`tb/acmp_talker/retry_mutants.py`, `tb/nvm_port` figures. No Vivado synthesis or
implementation; Vivado ran only as the parent's xvlog gate, under the exclusive lock (it
waited about an hour behind another holder at head). No hardware, bench or flashing.

Area: standalone `KL_srp_domain` (sv2v + Yosys `synth_xilinx`) goes from 116 to 119 flip-flops
(`reg_in_r`, `pend_in_r`, `rxla_pend_r`) and from 130 to 131 LUTs. The parent's priced
`KL_pp_shadow` moves from 56,150 to 55,878 LUT and 26,293 to 26,284 FF (LUTRAM 4,104, RAMB36 15,
RAMB18 4, DSP 10, CARRY4 2,381 unchanged): whole-design synthesis variation, not this module's
cost.

## Scratch-parent consumer gate table

Scratch parent: kebag-logic/milan-fpga dev e9cbb676d7fdd6539aa408e5dfe38870a4ae1a5f (dev's head
when cloned), every submodule initialised, under the scratch root. Its protocol-processor
gitlink was staged at 08ae0013 for the base column and at e11fb36b for the head column (the
submodule fetched the lane branch from the lane tree; nothing was pushed). Every git command
in the submodule was preceded by a top-level identity check. The parent was never committed or
pushed; it ends with the staged gitlink at e11fb36b and the two patches below in its working
tree. Both patches were applied for both columns:

- `parent-evidence-classification.patch` (#180 lane), sha256 7662517046007f77b0e3763814226a50af87e06d01261586bcaf32cd4a75495e, 2,689 B;
- `parent-adoption-milan_dp-67.patch` (#176 lane), sha256 e142e2e7d7aec88fdc0bb7b6443d296f671f06391712b214339a50b84acc66d3, 1,541 B.

| Parent consumer gate | Base gitlink 08ae0013 | Head gitlink e11fb36b | Identity |
|---|---|---|---|
| `check_cpp_idiom.py` / `--selftest` | 0 / 0 | 0 / 0 | identical (the new DR functions are under the 100-line limit) |
| `check_py_idiom.py` / `--selftest` | 0 / 0 | 0 / 0 | identical except scanned lines 258,800 -> 258,823 |
| `check_rtl_source_lists.py` / `--selftest` | 0 / 0 | 0 / 0 | identical |
| `pp_srcs.py --check --selftest` | 0 | 0 | identical |
| `check_port_contracts.py` / `--selftest` | 0 / 0 | 0 / 0 | identical except protocol-processor ports 1,761 -> 1,763 (the two documented Domain inputs); undocumented 111 <= 111 |
| `measure_naming.py --check` / `--selftest` | 0 / 0 | 0 / 0 | identical except ports scanned 3,989 -> 3,991 |
| `measure_test_evidence.py --check` / `--selftest` (patched) | 0 / 0 | 0 / 0 | identical: 0 unexplained readers |
| `measure_test_evidence.py --check` without the evidence patch | 1 | 1 | identical: the 3 readers already on processor main (`tb/aecp_cmds/mutants.py`, `tb/elab_guards/guards.py`, `tb/elab_guards/mutants.py`); this lane adds none |
| `docs_check.py` | 0 | 0 | identical |
| `check_sh_idiom.py` / `--selftest` | 0 / 0 | 0 / 0 | identical |
| `check_hygiene.py --check` / `--selftest` | 0 / 0 | 0 / 0 | identical |
| `check_sv_idiom.py` / `--selftest` | 0 / 0 | 0 / 0 | identical |
| `check_submodule_docs.py` / `--selftest` | 1 / 0 | 1 / 0 | identical: "documented pin differs from Git" and the stale pin diagram, which any moved gitlink fails until an adoption re-records it |
| `check_todo_ownership`, `check_soc_sources` (each with `--selftest`) | 0 | 0 | identical |
| `measure_fail_fast` (`--check`, `--selftest`), `measure_control_flow --selftest`, `measure_cohesion --selftest` | 0 | 0 | identical |
| `check_feature_status.py` / `--self-test` | 0 / 0 | 0 / 0 | identical |
| `check_nvm_record_space.py` / `--self-test`, `check_entity_shape.py --self-test` | 0 | 0 | identical |
| `lint_rtl.py --check` / `--self-test` | 0 / 0 | 0 / 0 | identical: 90 violations <= ratchet 90 |
| `sw/builder/test_builder.py` | 0 | 0 | "ALL GATES PASS EXCEPT 1 NOT RUN" at both; only temp paths and seconds differ |
| `tests`: `behave --no-capture -f plain` | 0 | 0 | identical: 14 features, 406 scenarios, 1,977 steps (step times aside) |
| `flock $VIVADO_LOCK python3 scripts/xvlog_gate.py --check` (exclusive lock) | 0 | 0 | identical except the line naming the processor pin; 0 findings |
| `make -j16 -C tb/verilator/pp_shadow` | 0 | 0 | identical tallies: 609 + 649 + 609 + 317 checks, 0 failures |
| `make -j16 -C tb/verilator/nvm_cosim lint` | 0 | 0 | identical (Verilator wall times aside) |
| `make -j16 -C tb/verilator/nvm_cosim quick JOBS=4 POOL=2` | 0 | 0 | identical: 315/315 |
| `make -j16 -C tb/verilator/milan_dp_render` | 0 | 0 | identical tallies; head reused images the base run generated in the same scratch tree |
| `make -j16 -C tb/verilator/milan_dp SIM_JOBS=2` (with the #67 patch) | 0 | 0 | identical tallies: legs 423, 416, 162, 1,967, 1,969, 3,751, 1,967, 33 checks, milan_datapath 236/236/233, 182/182 and 6/6, 0 failures |
| `syn/yosys/ooc.sh --record-rom-digests tcam` (scratch ledger only, restored after) | 0 | 0 | rows at both pins: `ucode.hex` a3b62cabe2cb091383f999bf58b830ff2d3ab63cd8699b95d2529dbf4d02bcb3, `ltn_rom.hex` 23cc67eeadc7ecad8c9ceb7f9391095b64ada44d4e0f3a232ce82a2a69e7e956: no ROM changes |
| `syn/yosys/ooc_selftest.py` | 0 | 0 | identical: 75 arms. (A first base run, ordered before the digest record, refused setup with rc 2 for the missing pin row; rerun after the record, as the head run was ordered.) |
| `syn/yosys/ooc.sh KL_pp_shadow` | 0 | 0 | 56,150 -> 55,878 LUT, 26,293 -> 26,284 FF, all else equal (see Area above) |

## Tool identities

- Verilator 5.050 (rev v5.050), the pinned wrapper (sha256 905795b99e0a8803383b198b118bafcbd87d20b877e3f09c39c31ea81979e92f); the host default 5.052 was not used.
- sv2v v0.0.12 (sha256 b29952bc8f400ca90207507db0ff6763263e03d3eec711da80338430ed636b9b).
- Yosys 0.66 (git sha1 86f2ddebc), sha256 ec566d8fbb0d24e09ce7ab4e86c55c7169f24097d90611ee354b446925f36b5b,
  the version the parent pins and the HDL guide names as the CI pin. No Yosys exists under
  the shared tools directory (searched); the brief said there would be one.
- wavedrom 2.0.3.post3 (the CI pin) in a scratch virtualenv outside every tree; mmdc 11.16.0.
- Python 3.14.8, g++ 16.2.1.

## Notes and scope interpretation

- **Scope wording.** The session brief limits changes to "E_SCFG, its tests, generators that
  must follow it, and the docs that record it". E_SCFG is the SET_CONFIGURATION microprogram
  and has nothing to do with #184; the brief's own assignment (#184) can only be met in the
  SRP Domain participant. I read the limit as "the unit the assignment names, its tests, and
  the docs that record it" and changed only `KL_srp_domain`, its wiring in `KL_srp_top`, the
  SRP suites and campaign, and the docs. Likewise "the accepted lengths and the refusal
  cases" (a SET_STREAM_INFO item) has no counterpart here; the encodings table above takes
  its place. Please confirm this reading.
- **Closes #179: not claimed.** #179 (SET_CONFIGURATION NO_SUCH_DESCRIPTOR) is already
  closed and unrelated to this change; PR-BODY.md closes #184 only.
- **Port additions.** `KL_srp_domain` gains two inputs. It is internal (instantiated only by
  `KL_srp_top` and the srp_encoder wrap). `protocol_processor_top` and `KL_srp_top` keep
  every port and parameter, so the assignment's STOP condition (top-level port or parameter)
  is not met. Yosys still elaborates `KL_srp_domain` as one of its tops (rc 0).
- **The round-completion guard I tried and removed.** A guard holding the MSRP drain until
  the Domain push is accepted was considered; the walk takes at least three clocks after
  tx! while the Domain offers its push on the next clock, and a guard no test could kill
  would be untested RTL, so it is not in the commit.
- The stale "Domain FSM keeps no registrar" sentences in docs 10 are corrected.
- **History of the head.** The commit was amended once before any head record was taken:
  a `tb/pp_top/README.md` line citation still pointed at the first RTL draft's line
  numbers. Head runs started at the pre-amend commit 91e99e63 were stopped and discarded;
  every head record above is from e11fb36b.
- **Final state.** The lane tree is at e11fb36b with no tracked change and no ignored file
  (`git status --short --ignored` is empty). Generated and scratch files never entered the
  tree; logs, receipts, exports and the scratch parent stay under the scratch root.

## Round 2 (PR #191, assignment comment 6253529699)

Status: REVIEW READY at head 88cb206135c23eb86488ad110fe19cfca5f341cf, posted as issue #184
comment 6256377696 (2026-10-19). Not pushed, PR not
edited, TAKEN not posted again. Round 1 above is kept as it was; where it differs, this
section supersedes it (Design item 2, the "Behaviour" bullet "waits at most one T-MRP-JOIN",
and the RTL line numbers after `KL_srp_domain.sv:35`).

Inputs read: the assignment (6253529699) and both reviews, R652-1 POSITIVE (6253525919) and
R653-1 NEGATIVE (6253382633). R653-1 links the issue assignment, the round-1 evidence and
the review-start notice; R652-1 has no external links. No reviewer packet was available
here, so their probes were not rerun; the boundary probe below is this lane's own.

### Commits (branch `184-domain-joinmt`, no rebase)

| Commit | Subject |
|---|---|
| 4e87b88c | `Merge processor main 5addf297 into 184-domain-joinmt` (step 0; clean, no conflicts; brings #181's 12 files) |
| 88cb2061 | `Domain re-join docs: snapshot at enqueue, kept until the encoder accepts it, no fixed drain bound (#184)` |

`git diff 4e87b88c 88cb2061`: 16 files, +49 / -39. No RTL logic change: `KL_srp_domain.sv`
with comments and blank lines stripped is identical at e11fb36b and 88cb2061 (checked
before the commit). No register map, port, parameter, generator or ROM change.

### Changes (file:line at 88cb2061)

- **R653-1-F1** `docs/architecture/10_srp_engine.md`
  - :299-303: the hand-over sentence ("The encoding is chosen when the re-join is handed to
    the encoder ...") is replaced by the review's exact text, first three sentences: the
    snapshot of the previously registered state at servicing, the queued event keeping its
    encoding until the encoder accepts it, the enqueue-edge receive updating the registrar
    for subsequent re-joins.
  - :314-317 (was :309-310): "every re-join handed over after it" and "it waits at most one
    T-MRP-JOIN for its drain" are replaced by the review's exact last two sentences. :314 is a
    one-line lead-in I added ("A peer's withdrawal (its Lv) takes the Registrar to MT at
    once, as the table gives."), because the exact text says "the withdrawal" and the
    sentence that introduced it was the one replaced.
  - The paragraph is reordered so the pending (hand-over) timing comes first and the
    servicing snapshot after it; every sentence of both exact corrections is verbatim.
- **R652-1-RS1** `docs/architecture/10_srp_engine.md:295-299`: "Its re-join waits ... the
  drain it would have reached anyway, so a declaration later in the peer's MRPDU registers
  first." is replaced by the review's exact three sentences ("normally registers first";
  a received LeaveAll on a tx! clock; a tx! inside the peer's MRPDU; either is JoinMt).
  :293 now says "handed over (made pending)" so the review's "handed over" has one meaning
  next to F1's "pending re-join is serviced".
- **Source banner** `hdl/srp/KL_srp_domain.sv:35-44` (was :35-42, +2 lines): made pending at
  once for periodic! and for a LeaveAll on a tx! clock, as the own sLA is; a received
  LeaveAll waits for the next tx!, so a later declaration normally registers first;
  servicing snapshots the previously registered state into the event queue; the queued code
  keeps its encoding until the encoder accepts it; backpressure can extend the drain.
- **R652-1-RS1 optional comment** `hdl/srp/KL_srp_domain.sv:208`: "periodic!, or the own sLA
  on its tx!" -> "periodic!, or a LeaveAll on a tx! clock (own sLA)".
- Followers of those two comment edits:
  - `tb/pp_top/README.md:2578`, `:2581`: citations `:252` -> `:254` (adoption
    DOMAIN_CHANGE) and `:219` -> `:221` (revert), the same statements as before.
  - `tb/srp_top/mutations/domain-*.patch` (12 files): hunk offsets +2, and in
    `domain-capture-unregistered` and `domain-rejoin-at-request` the context line of :208.
    Rewritten by `bin/regen_patches.py` (git apply in scratch, re-emitted); the planted
    defects are byte-identical. The head campaign output equals round 1's line for line.
  - `tb/srp_encoder/README.md:74-78`: "handed to the encoder at once" -> "made pending at
    once", plus one sentence: the queued re-join carries the registration as it stood when
    it was queued, until the encoder accepts it.
- **PR body**, second "What changes" bullet: the same boundary (PR-BODY.md).
- **R652-1-RS2**: the round-1 `synthdom/` directory is now published under
  `r2-receipts/synthdom/` (sv2v output and Yosys stat at e11fb36b and 08ae0013), and the
  area is re-measured at 5addf297 and 88cb2061 with the command recorded
  (`r2-receipts/bin/domain_area.sh`, `area/`, `gates/*-area.log`): FF 116 -> 119, LUT 130 ->
  131. R652-1 counted FDRE only (113 -> 116); FDSE is 3 at both. The evidence branch line
  itself is the manager's; I cannot push.
- **R652-1-S1 (optional): not taken.** The assignment scopes round 2 as docs plus a merge,
  with a single re-reviewer on that basis; two new DR7 checks and two new campaign arms
  would widen it to Tests. Left for a follow-up if the owner wants it.

Behaviour, corrected (supersedes round 1's "Behaviour" last bullet): a queued Domain re-join
carries the Registrar state of the clock before it was queued and keeps it until the encoder
accepts it. A receive in the enqueue clock affects only later re-joins. No fixed drain bound:
encoder or TX backpressure holds the queued event as long as ready stays low.

### New receipt check: the documented boundary (probe, outside the tree)

Not a tree check; it backs the corrected text. `r2-receipts/probe/probe.cpp` drives
`KL_srp_domain` alone (pinned Verilator 5.050); the expected values come from the text.

| Check | What | Head 88cb2061 | Round-1 head e11fb36b |
|---|---|---|---|
| B1a-d | registered: queued JoinIn survives a peer Lv while ready is low; accepted; next fresh re-join JoinMt | PASS | PASS |
| B2a-c | inverse: queued JoinMt survives a peer JoinIn while waiting; next re-join JoinIn | PASS | PASS |
| B3a-c | Lv on the enqueue edge: the queued re-join is JoinIn; the next is JoinMt | PASS | PASS |
| B4, B4b | ready held low 200,000 clocks: still queued (no fixed bound); accepted when ready rises | PASS | PASS |

12 PASS, 0 FAIL, rc 0 at both. Planted mutants (`probe/mut-*.patch`), each rc 1:

| Mutant | Planted defect | Failing words |
|---|---|---|
| `refresh-while-waiting` | the queued re-join follows the registrar while it waits (the old acceptance-time text) | `FAIL: B1b a peer Lv while it waits leaves the queued JoinIn`, `FAIL: B2b a peer JoinIn while it waits leaves the queued JoinMt` |
| `enqueue-next-state` | the enqueue uses the enqueue edge's next registrar state | `FAIL: B3b an Lv on the enqueue edge: queued JoinIn` |
| `pop-without-ready` | the queue pops without the encoder's acceptance | `FAIL: B1b ...`, `FAIL: B2b ...`, `FAIL: B4 the queued re-join waits 200000 clocks while ready stays low` |

### Base and head records (round 2)

Base: processor main 5addf29759a22372ed6aa3e1d52a3aad29e3ecd7, run in the scratch parent's
submodule (checked out there for these runs, then returned to its staged e11fb36b) and from
a `git archive` export. Head: 88cb2061 in the lane tree and from an export. Same pinned
tools (`r2-receipts/tool-identity.txt`: Verilator 5.050 v5.050, sv2v v0.0.12, Yosys 0.66,
wavedrom 2.0.3.post3, mmdc 11.16.0). Nothing piped; each record is a log with its rc file.
Both trees had their ignored build products removed afterwards; the lane tree is clean.

| Record | Base 5addf297 | Head 88cb2061 | Identity |
|---|---|---|---|
| `scripts/run_suites.sh` (REQ_TAG_LOG set) | rc 0, 1,030,013 checks | rc 0, 1,030,029 | identical except srp_encoder 581 -> 593, srp_top 8,656 -> 8,660 (the round-1 +16) |
| `check-req-tags.py --suites --evidence` | rc 0, 227 lines | rc 0, 228 | +1 (REQ-SRP-005 on DR6) |
| `scripts/lint_hdl.sh` | rc 0 | rc 0 | identical |
| `make check` | rc 0 | rc 0 | identical except links 1,196 -> 1,202, tags 227 -> 228, ID files 593 -> 608 |
| `scripts/gen_matrix.py --check` | rc 0 | rc 0 | identical |
| `syn/yosys/run.sh` | rc 0 | rc 0 | identical except `all.v` line numbers of three memory warnings |
| `tb/elab_guards/guards.py --frontend yosys` | rc 0, 93/93 | rc 0, 93/93 | identical except `all.v` line numbers in six refusal texts |
| `KL_srp_domain` area (module only) | FF 116, LUT 130 | FF 119, LUT 131 | as round 1 |

Every campaign that builds a changed file (the round-1 list; `KL_srp_domain.sv` changed in
comments, and the merge puts the lane's RTL beside main's):

| Campaign | Base | Head | Identity |
|---|---|---|---|
| `tb/srp_top/mutants.py` | rc 0, 137, coverage 86/86 | rc 0, 159, coverage 90/90 | 130 common receipts identical; only the 21 new arm runs and the domjoin control differ; head output identical to round 1's head |
| `tb/srp_admission/mutants.py` | rc 0, 12/12 | rc 0, 12/12 | identical |
| `tb/pp_top/aecp_mutants.py` | rc 0, 67/67 | rc 0, 67/67 | identical |
| `tb/pp_top/aecp_dispatch_mutants.py` | rc 0, 58/58 | rc 0, 58/58 | identical |
| `tb/pp_top/ctr_mutants.py` | rc 0, 18/18 | rc 0, 18/18 | identical |
| `tb/pp_top/notify_mutants.py` | rc 0, 109 of 109 | rc 0, 109 of 109 | identical (main's #181 adds 11 arms to round 1's 98) |
| `tb/pp_top/gsi_mutants.py` | rc 0, 20 | rc 0, 20 | identical |
| `tb/pp_top/name_wr_mutant.py` | rc 0 | rc 0 | identical |
| `tb/pp_top/acmp_mutants.py` | rc 0, 51 of 51 | rc 0, 51 of 51 | identical |
| `tb/pp_top/d3_mutants.py` | rc 0, 110 of 110 | rc 0, 110 of 110 | identical |
| `tb/adp_engine/mutants.py` | rc 0, 62/62 | rc 0, 62/62 | identical |
| `tb/maap/mutants.py` | rc 0, 32/32 | rc 0, 32/32 | identical |
| `tb/name_state/mutants.py` | rc 0 | rc 0 | identical, 124 receipts |
| `tb/elab_guards/mutants.py` | rc 0, 160 of 160 | rc 0, 160 of 160 | identical |

"identical": the sorted, normalised logs match line for line, and every per-arm receipt
has the same failing-check set (`r2-receipts/campaign-compare.txt`, `gate-compare.txt`).

### Scratch-parent consumer gates: not rerun in round 2

The round-2 assignment names the docs gates and the README suites at the merged head. The
parent table above is round 1's (gitlink e11fb36b). The merged head changes no RTL logic
relative to e11fb36b except what main 5addf297 brings, and the current-dev merge candidate
with builder and native banks is listed by both reviews as the manager's duty. The parent
is unchanged: never committed or pushed, staged gitlink e11fb36b, the two patches in its
working tree.

### Receipts

`r2-receipts/` beside this file: 123 files, 1.1 MB, none over 200 KB, with host paths
replaced by placeholders. `r2-receipts/INDEX.md` is generated by `bin/gen_index.py` from the
files present (path, bytes, sha256, and each log's own command and rc). The only rc-1
records are the three planted probe mutants.
