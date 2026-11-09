# [A754] HANDOFF: processor issue #216

Status: REVIEW READY at head `60094a2`. Every gate at the head and all 40 scratch-parent consumer gates are rc 0;
the twin reports the three owed rows of this defect gone; every acceptance item is met (the table at the end).

- Repository: Mister-M-alt/protocol-processor-control-plane-avb-milan (`git remote get-url origin` checked before the
  first commit). Branch `216-mrp-applicant`, local, not pushed.
- Base `044cb25f4ed2187bd238490650e73d5d189855d1` (processor main). Head `60094a268c0df46703a3bee08c94118153634fd9`.
- Commits on the base (one-line subjects, no body, no trailers):
  - `f247533` Give the Domain and each VID a Table 10-3 Applicant decided at tx!, a Registrar per VID and an MVRP
    LeaveAll with nothing declared, graded end to end and per unit (issue #216)
  - `1cf865b` Plant one arm per new row, the three acceptance arms included, and re-express the 23 arms whose lines
    moved (issue #216)
  - `3da1427` Record the Applicants, the VID Registrar and the MVRP LeaveAll in 10 sections 3, 5, 6.1 (F10.2), 6.2
    (F10.3) and 6.5, 09 8.15 and the three READMEs, with the measured arm counts (issue #216)
  - `8a73a9c` Split the two VLAN rows' functions under 100 lines and record the measured area in 10 section 5.1
    (issue #216)
  - `06cce32` Feed M11 a peer JoinIn of the Domain so the canceled round is empty again and the arm
    empty-canceled-pdu fails (issue #216)
  - `60094a2` Grade OV0 to OV10 with one arm that hands every push over twice and appends, since each Applicant now
    decides once per tx! and either layer alone holds them (issue #216)
- `hdl/adp` and `hdl/aecp` untouched (`git diff --stat 044cb25f HEAD -- hdl/adp hdl/aecp hdl/acmp` is empty). No
  top-level port, parameter or register-map change: `protocol_processor_top.sv` is unchanged and `KL_srp_top`'s
  input/output/parameter declarations are identical at base and head; the new ports are on `KL_srp_domain` and
  `KL_srp_vlan`, both internal. No MRP timer changed (Milan v1.2 Table 4.3 values untouched). The HDL is unchanged
  since `f247533` (`git diff --stat f247533 HEAD -- hdl` is empty).
- Parent issues: kebag-logic/milan-fpga#860 (one New, JoinIn with the Registrar MT) and #857 (no MVRP LeaveAll once
  nothing is declared).

## Resumed (2026-11-09 10:5x)

The session ended at 10:34 on a planned host reboot. The checkout was at `60094a2`, clean; nothing after that commit
existed in scratch (the clones `h60094a2` and the scratch parent are both at `60094a2`, clean). Complete before the
reboot, kept: the processor gates, the SRP campaign, `make -C tb/pp_top aecp-mutants`, the area, the twin, and the
scratch parent's milan_dp, firmware SRP campaigns (shard 3/4), firmware-verilator, firmware-boundary, changes,
verilator-lint, bdd, yosys-elaboration and publication-census. Killed by the reboot and re-run from the start:
`make -C tb/pp_top aecp-dispatch-mutants` (its partial log kept as `camp-aecp-dispatch-killed-by-reboot.log`) and the
parent's firmware-unit job (its last step, fw_coverage, was running). Not yet run at the head, run now: the parent's
firmware-control and firmware-aecp campaigns (shards 1/4, 2/4), and the docs ratchets and idiom gates.

## Resumed (2026-11-09 07:2x)

The previous session ended on a session-host authentication failure at 06:4x, with two files modified and
uncommitted (tb/srp_top/README.md, tb/srp_top/sim_main.cpp). Both were read and kept, as commit `06cce32`. Every
gate below was then re-run from clean clones; nothing is carried over from an incomplete log.

1. `06cce32` (row M11). The SRP campaign at `8a73a9c` had reported `empty-canceled-pdu: rc=0 failures=0 UNPROVEN`
   (receipts/resume). That arm lets the encoder drain an MSRP round with no content, a ProtocolVersion/EndMark-only
   PDU. M11 lets a canceled own LeaveAll round wait for content and checks every later MSRPDU carries a vector.
   Since #216 the Domain's Applicant is AA at that round's tx! (periodic! moved it from QA), so the round always had
   the Domain's JoinMt to send and was never empty. The kept change feeds a peer JoinIn of the declared Domain
   before the release (rJoinIn!: AA to QA, 802.1Q-2018 Table 10-3), so the round's tx! has nothing to send and is
   empty again. Measured: control `srp_top peer` 90 checks, 90 PASS; with the arm 89 PASS, 1 FAIL, row M11 ("M11:
   quiet canceled round emits valid content and recovers").
2. `60094a2` (group onevec). The full campaign at `06cce32` returned rc 1 (receipts/head-06cce32/camp-srp):
   `second-queueing` and `join-displaces-new` UNPROVEN on `srp_top onevec` (12 checks, 12 PASS each), so the
   coverage check missed OV1 to OV7. Cause: since #216 each Applicant decides one message per tx! and each round's
   drain waits for that tx!, so no OV scenario puts a second push of a value into one pending table; the encoder's
   merge (#214) is no longer exercised end to end. Both arms are still killed at the encoder (PV rows: 68 and 4
   failures, as recorded). Holding the transmitter does not reach it either (OV10 already does): a drain owns its
   table from its start, so a second push waits and its round coalesces. Fix: one combined arm, as SW1 has
   (`listener-shares-nothing-encoder-appends`): `push-twice-encoder-appends`, the intake taking every push twice
   (a hand-over handshake fault) plus the encoder's `second-queueing`. Measured on onevec (receipts/onevec-regrade):
   the push-twice hunk alone 12 PASS, `second-queueing` alone 12 PASS, the two together 11 FAIL, OV0 to OV10. The
   onevec grading of the two encoder arms is removed (their encoder grading stays), the coverage check now requires
   OV1 to OV10 (OV8 to OV10 had no arm before), and the records follow: tb/srp_top/README.md (the #214 table and
   its coverage line, a note in the #216 section) and 09 section 8.14 (the OV controls).
3. Not changed, reported: tools/cmp_counts.py compares every `tb/srp_top` README arm count with the campaign. Seven
   arms differ (`pending-peer-ignored` 14 recorded / 26 measured, `mvrp-supersedes-msrp` 6/8,
   `leaveall-expiry-lost` 18/16, `preparation-before-slot` 22/21, `mvrp-expiry-only-redraw` 6/17,
   `stale-expiry-honoured` 1/7, `mvrp-stale-expiry-honoured` 1/7), and two recorded rows are not graded by the
   campaign (`peer-restarts-timer`, `lv-never-ends`). The seven give the same counts at the base 044cb25f
   (receipts/pre-existing-counts), so these figures were stale before #216; they are outside this issue and left
   for a follow-up.

## Reproduction at the base

`hdl/` of `044cb25f` with `tb/srp_top` and `tb/common` of `06cce32` (the applicant group is unchanged since),
`make run RUN_ARGS=applicant` in `tb/srp_top`: `18 checks: 9 PASS, 9 FAIL`, rc 2 (receipts/base/base-h06tb-applicant.log):

- AP1 `... sent New@202 JoinMt@1002 JoinMt@2002 JoinMt@3002 JoinMt@4002` (the Domain, one New).
- AP2 `... sent New@401 JoinIn@1201 JoinIn@2201 ...` (VID 2, one New); AP3 `4 JoinIn, 0 JoinMt` with the Registrar
  MT, and `JoinIn@10201 JoinIn@11201` after the peer's Lv.
- AP5 `LeaveAlls at none ms, Begin! at 0` (MVRP declaring nothing since Begin!), AP6 `Lv at 3001 ms, LeaveAlls at
  none ms` (every declaration withdrawn), and their two byte-exact rows.
- AP7 (the round's drain waits for the Domain's tx!).

AP4 (Talker Advertise and Listener Ready: New, New, then the Join) and the MSRP LeaveAll rows of AP5 and AP6 pass at
the base: the stream Applicants already followed Table 10-3, and the MSRP prepared LeaveAll round already had a
LeaveAll-only form, the Domain riding it. At head the group is `18 checks: 18 PASS, 0 FAIL`
(receipts/head-60094a2/camp-srp/selected-out/control-srp_top-applicant.log).

## Changes (file:line at head, clause)

| Where | What | Clause |
|---|---|---|
| `hdl/srp/srp_pkg.sv:80-258` | the Applicant: states and events (:84-109), `srp_app_next` row by row (:115), `srp_app_rx_next` (:207), `srp_app_msg` (:225; sJ/s against the Registrar), `srp_app_declaring` (:255) | 802.1Q-2018 10.7.7, Table 10-3 with notes 4, 5, 8; 10.7.6.2, 10.7.6.3, 10.7.6.5 |
| `hdl/srp/KL_srp_domain.sv:162-200` | the declared Domain value's Applicant: received event, rLA! (not the own), periodic!, then tx! or txLA! decided at the MSRP tx! (`tx_serve_w` :187); one-bit Registrar (:136, :162-175) | Table 10-3; Table 10-4 with Milan v1.2 4.2.7.2.2; Milan v1.2 4.2.7.2.1 (declared at LINK_UP) |
| `hdl/srp/KL_srp_domain.sv:246-271` | a tx! that cannot be served is owed; `tx_done_o` once the tx! is served and its message accepted | Table 10-3 tx! (one transmit opportunity, one message) |
| `hdl/srp/KL_srp_vlan.sv:252-281` | per VID: Registrar (:254-261: rNew/rJoinIn/rJoinMt register, rLv!, rLA! and txLA! to LV), rLA! and periodic! on every entry (:266-269), New!/Lv!/tx!/txLA! (:274-277), the walk's message (:281) | Table 10-3, Table 10-4 (MVRP as printed), 10.7.6.3, Table 10-3 note 11 |
| `hdl/srp/KL_srp_vlan.sv:179, 325-344, 437` | an MVRP tx! walks every entry (owed if it cannot start), `tx_done_o` when its messages are accepted | Table 10-3 tx! |
| `hdl/srp/KL_srp_top.sv:1212-1230` | the MVRP tx! round: VID walk, then the drain; a pending own LeaveAll is that tx!'s sLA (txLA! row, LeaveAll flag), a peer MVRP LeaveAll on the edge wins | 10.7.9, Table 10-5 (Active, tx! sLA; rLA! Passive) |
| `hdl/srp/KL_srp_top.sv:1304-1308` | an own MVRP expiry makes the machine Active and redraws the timer (10-15 s, unchanged) | Table 10-5 leavealltimer!; Milan v1.2 Table 4.3 |
| `hdl/srp/KL_srp_top.sv:1233-1241` | the MSRP round's drain also waits for the Domain's tx! (`td_dom_r`) | Table 10-3 (the tx!'s message rides its MRPDU) |
| `hdl/srp/KL_srp_top.sv:378-411, 432-489` | Domain and VLAN wiring: received Domain/VID events, `p2p_i`, the own sLA, tx!/txLA!, `tx_done_o` | |
| `hdl/srp/KL_srp_encoder.sv:406-410` | an MVRP drain also starts for its LeaveAll alone: the LeaveAll-only MVRPDU | 10.7.9; 10.8.2.8 f) |

Talker Advertise and Listener: checked, already Table 10-3 (`KL_srp_talker_fsm.sv`, `KL_srp_listener_fsm.sv`
unchanged); AP4 passes at the base and is held by `talker-one-new` and `listener-one-new`.

Docs: `docs/architecture/10_srp_engine.md` 6.1 and F10.2 (:363-405), 6.2 and F10.3 (:466-501), 3 (:117-135), 5 and
5.1 (storage and area :259, :295-296, :339-347), 6.5 (:1085, :1110-1123); `09_verification.md` 8.14 (:823-854) and
8.15 (:856, new); `docs/traceability/MODULE_MATRIX.md`; the `tb/srp_top`, `tb/srp_encoder` and `tb/pp_top` READMEs.

## New checks and their planted arms (failing words)

Each arm is a checked-in patch under `tb/srp_top/mutations`, run by `make -C tb/srp_top mutants`; the campaign
requires the named words in a FAIL line. All are KILLED at head (receipts/head-60094a2/camp-srp/camp-srp.log).

| Check | Arm | Failing words (the campaign's expected substring) | Failures at head |
|---|---|---|---|
| AP1 the Domain New, New, then JoinMt | `domain-one-new` | `AP1:`; encoder `D1 four tx!` | 1; 3 |
| AP2 VID 2 New, New, then JoinMt | `vlan-one-new` | `AP2:`; encoder `V1 four tx!` | 1; 7 |
| AP3 VID 2 JoinMt with the Registrar MT | `vlan-joinin-registrar-mt` | `AP3: VID 2 with its Registrar MT`; encoder `V3 periodic JoinMt` | 3; 13 |
| AP3 JoinIn with the Registrar IN, JoinMt after the peer's Lv | `vlan-registrar-never-in`, `vlan-rlv-ignored` | `AP3: with its Registrar IN`, `AP3: after the peer's Lv`; encoder `VR1`, `VR2` | |
| AP4 Talker Advertise and Listener New, New | `talker-one-new`, `listener-one-new` | `AP4: the Talker Advertise`, `AP4: the Listener Ready` | 1 each |
| AP5 MVRP LeaveAll from Begin! with nothing declared | `mvrp-leaveall-needs-content`, `top-mvrp-la-flag-dropped` | `AP5: MVRP declaring nothing`; encoder `L7 the LeaveAll-only MVRPDU is captured` | 4; 6 |
| AP6 MVRP LeaveAll after every declaration is withdrawn | `mvrp-leaveall-needs-content` | `AP6: with every declaration withdrawn` | 4 |
| AP5/AP6 the MSRP LeaveAll carrying the Domain's txLA! sJ | `domain-txla-row-ignored` | `AP5: MSRP sends a LeaveAll`; encoder `DR4 own LeaveAll` | 2; 1 |
| AP2 the MVRP drain after the VID walk | `top-mvrp-drain-at-tick` | `AP2:` | 1 |
| AP7 the MSRP drain waits for the Domain's tx! | `top-round-ignores-domain` | `AP7:` | 1 |
| encoder DT1, DT3, DA1, DA5 (the Domain's tx! hand-over, its received messages) | `domain-tx-done-at-serve`, `domain-tx-owed-dropped`, `domain-applicant-deaf`, `domain-applicant-any-value` | `DT1`, `DT3`, `DA1`, `DA5` | |
| encoder VR3 to VR11, V6, V10, V11, `tb/srp_top` R4 (each VID's Registrar and Applicant) | `vlan-rx-any-vid`, `vlan-s-registers`, `vlan-leaveall-keeps-in`, `vlan-rx-loses-to-leaveall`, `vlan-txla-keeps-in`, `vlan-applicant-deaf`, `vlan-note8-ignores-registrar`, `vlan-registrar-kept-on-allocation`, `vlan-leave-abandoned`, `vlan-rejoin-of-leaving-allocates`, `vlan-walk-frees-lo` | `VR3` ... `VR11`, `V6 last user out -> Lv VID 2`, `R4: WITHDRAW_LISTENER`, `V10`, `V11` | |
| M11 (changed) a canceled own LeaveAll round waits for content | `empty-canceled-pdu` | `M11:` | 1 |
| OV0 to OV10 (control changed) no value twice in one MRPDU | `push-twice-encoder-appends` (new) | `OV1:` (fails OV0 to OV10) | 11 |

The issue's three acceptance arms are `domain-one-new`/`vlan-one-new` (one New), `vlan-joinin-registrar-mt` (JoinIn
with the Registrar MT) and `mvrp-leaveall-needs-content` (LeaveAll stopped with the last declaration). The full
per-arm counts are in `tb/srp_top/README.md` (the #216 section) and `tb/srp_encoder/README.md`.

## Area (the processor's syn/yosys flow; xc7, flattened; tools/area/area.sh)

Base: a clone of `044cb25f`; head: the clean clone of `60094a2` (receipts/area). The head figures equal the ones
recorded in 10 section 5.1 at `8a73a9c` (hdl/ unchanged since `f247533`).

| Shape | LUT base / head | FF base / head | RAM cells |
|---|---|---|---|
| `KL_srp_top` 2x2 | 13,536 / 14,109 (+573) | 5,407 / 5,447 (+40) | 114 / 112 |
| `KL_srp_top` 8x8 | 28,002 / 28,814 (+812) | 11,297 / 11,337 (+40) | 179 / 177 |
| `KL_srp_domain` | 150 / 215 (+65) | 119 / 128 (+9) | 0 / 0 |
| `KL_srp_vlan` | 364 / 594 (+230) | 132 / 147 (+15) | 3 / 1 |
| `KL_srp_encoder` | 2,747 / 2,712 (-35) | 1,358 / 1,358 | 52 / 52 |

Recorded in `docs/architecture/10_srp_engine.md` 5.1.

## Gates at the head `60094a2` (processor)

Every gate ran on a clean clone of `60094a2`, with CI's pinned Verilator 5.050, Yosys 0.66, sv2v v0.0.12 and a CPython
3.12.3 venv. None was piped; each has its cmd, log, rc, start, end and interpreter record.

| Gate (CI job) | Command | rc | Result | Receipt |
|---|---|---|---|---|
| docs-gates | `make check` | 0 | the docs, AECP command and diagram lints OK | head-60094a2/proc/make_check.* |
| matrix | `python3 scripts/gen_matrix.py --check` | 0 | `matrix: OK (94 rows, 0 untested)` | proc/gen_matrix_check.* |
| HDL lint | `bash scripts/lint_hdl.sh` | 0 | every module `LINT OK` (Verilator 5.050) | proc/lint_hdl_5050.* |
| suites (full sweep) | `env REQ_TAG_LOG=... bash scripts/run_suites.sh` | 0 | 36 suites, `suites: 1032092 checks total, 0 failing`; srp_top 8703, srp_encoder 1646, pp_top 11066 | proc/sweep.* |
| requirement tags | `python3 scripts/check-req-tags.py --suites ... --evidence ...` | 0 | `266 evidence lines, 14 suites, OK` | proc/req_tags_executed.* |
| portability | `bash syn/yosys/run.sh` | 0 | `YOSYS XILINX OK` for every top | proc/yosys_portability.* |
| portability | `python3 -B tb/elab_guards/guards.py --frontend yosys --jobs 4` | 0 | `elab guards: 93 checks: 93 PASS, 0 FAIL` | proc/elab_guards.* |
| whitespace | `git diff --check 044cb25f HEAD` | 0 | empty | proc/diff_check.* |
| SRP campaign | `python3 -B tb/srp_top/mutants.py --jobs 8` | 0 | `350 checks: 350 PASS, 0 FAIL`, every arm KILLED, `assertion coverage: 184/184; missing=[]` | head-60094a2/camp-srp/ |
| AECP campaign | `make -C tb/pp_top aecp-mutants` | 0 | `67 checks: 67 PASS, 0 FAIL` | head-60094a2/camp-pp/camp-aecp.* |
| AECP dispatch campaign | `make -C tb/pp_top aecp-dispatch-mutants` | 0 | `105 checks: 105 PASS, 0 FAIL`, 100 arms KILLED (re-run whole after the reboot) | head-60094a2/camp-pp/camp-aecp-dispatch.* |
| area | `tools/area/area.sh` (the processor's syn/yosys flow) at the base and the head | 0, 0 | the table above | area/ |

The full sweep ran serially inside this lane's unit (2305 s), not as four shard units; it completed rc 0 at the
head before the reboot and is not repeated.

## Scratch-parent consumer gate (milan-fpga dev `ac0a01e3`, protocol-processor pinned at `60094a2`)

The parent is a clone of dev `ac0a01e3` with two local commits, never pushed (push URL disabled): `5541fb5c31` the
gitlink at `60094a2`, `6705f8c216` `syn/yosys/rom_digests.tsv` re-recorded by `syn/yosys/ooc.sh
--record-rom-digests`. The commands are the rtl-fast workflow's run steps, plus milan_dp and the docs workflow's gates
that read the processor tree, jobs 4. All 40 gates return rc 0 (receipts/parent-60094a2).

| Job | Gates (each rc 0) | Result |
|---|---|---|
| milan_dp | `make -C tb/verilator/milan_dp SIM_JOBS=2` | 19 `RESULT: PASS`, 12,075 `[ok]`, 0 FAIL |
| firmware-srp-mutants (the SRP campaigns) | `python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --jobs 4 --shard 3/4` | both SRP mutation campaigns and the pin controls, `test_ctrl_firmware: PASS` |
| firmware-control-mutants | the same, `--shard 1/4` | `mutants: 523 of 523 caught`, PASS |
| firmware-aecp-mutants | the same, `--shard 2/4` | PASS |
| firmware-unit | `tally_selftest.py`, `ci_rv32_sdk_selftest.py`, `fw_rv32_selftest.py`, `--shard 0/4`, `test_ctrl_nvm.py`, `fw_coverage.py --selftest`, `fw_coverage.py --check` | PASS; `firmware coverage: PASS (30 files)` (re-run whole after the reboot) |
| firmware-boundary, firmware-verilator | `ctrl_boundary.py --without verilator`, `--only verilator` | `ctrl_boundary: PASS` each |
| changes | `ci_scope.py --selftest`; the diff against `ac0a01e3` classified | `selftest: PASS`; `col-processor` |
| verilator-lint | `lint_rtl.py --check --self-test`, `pp_srcs.py --check --selftest` | `LINT GATE: PASS (89 violation(s) <= ratchet 89)` |
| bdd-conformance | `behave --no-capture -f plain` | 508 scenarios, 2330 steps passed, 0 failed |
| yosys-elaboration | `syn/yosys/run.sh --mode elaborate ...`, the OOC read sets and baseline, `ooc_selftest.py`, `guard_selftest.py`, `cache_selftest.py` | `RESULT: PASS`; resource gate `baseline PASS: 3 endpoints`, its 236 mutants fail |
| publication-census | `publication_census.py --check --selftest` | `mutations: 0 of 31 rule(s) no arm proves` |
| docs ratchets | `docs_check.py`, `check_hygiene.py`, `measure_fail_fast.py`, `measure_test_evidence.py`, `measure_naming.py`, `check_doc_paths.py`, `check_port_contracts.py`, `check_rtl_source_lists.py` | each OK or PASS |
| idiom | `check_{cpp,py,sv,sh}_idiom.py` and each `--selftest` | each OK |

### The two-placement simulation (milan-fpga #665), with this head pinned

A scratch copy of the #665 lane (branch `665-s6b-cosim` at `a88772f1`, read only; that lane was not edited), with
protocol-processor at `60094a2` and its ROM digests re-recorded through the recorder, committed locally
(`b3117fc249`, `d90ab7a5ff`), never pushed. `make -C tb/verilator/milan_dp twin` returns rc 2 (twin_compare.py exits 1)
on exactly the three owed rows of this defect, each reporting the defect has gone (receipts/twin-60094a2):

```
[DIFF] owed row fabric-mvrp-leave-all: the defect has gone, the all-fabric half's grade finds none of it; the lane that fixed it (#857 (a release-image defect)) deletes the row
[DIFF] owed row fabric-domain-one-new: the defect has gone, the all-fabric half's grade finds none of it; the lane that fixed it (#860 (a release-image defect)) deletes the row
[DIFF] owed row fabric-vid2-join-in: the defect has gone, the all-fabric half's grade finds none of it; the lane that fixed it (#860 (a release-image defect)) deletes the row
twin: 3 finding(s)
```

The owed row `entity-available-index` (milan-fpga #858, processor #217) still holds (`[OWED]`); it is not this
issue's. The three rows live in the #665 lane and are deleted on the parent side when this head is adopted.

## Acceptance (issue #216)

| Item | Met by |
|---|---|
| Each Applicant (MSRP Domain, Talker Advertise, Listener; MVRP) sends New on two tx! after New!, then the Join | AP1 (Domain), AP2 (VID 2), AP4 (Talker Advertise, Listener Ready) |
| sJ follows the Registrar: JoinIn only when IN, else JoinMt | AP3; encoder V3, VR1, VR2, VR10 |
| The LeaveAll state machine runs with nothing declared, within Milan v1.2 Table 4.3, for MVRP and MSRP | AP5 (from Begin!), AP6 (every declaration withdrawn): the first LeaveAll within 15.5 s and each next 9.5 to 15.5 s after, MVRP and MSRP |
| Tests: the Domain and VID 2 with no peer, New, New, then JoinMt; LeaveAll within 15.5 s and again; the three planted mutants fail | AP1, AP2, AP6; `domain-one-new`, `vlan-one-new`, `vlan-joinin-registrar-mt`, `mvrp-leaveall-needs-content`, each KILLED |
| F10.2 and the section 6.1 text updated; MRP timers unchanged | `docs/architecture/10_srp_engine.md` 6.1 and F10.2; no timer value changed |
| The parent's gates that read SRP and MVRP pass on a scratch parent with this head pinned | the table above, 40 of 40 rc 0 |
