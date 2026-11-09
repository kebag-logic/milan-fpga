[A754] MRP Applicant: New on two tx!, sJ by the Registrar, and LeaveAll with nothing declared (IEEE 802.1Q-2018 Table 10-3, 10.7.6.3, 10.7.9)

Closes #216

Parent issues: kebag-logic/milan-fpga#860 and kebag-logic/milan-fpga#857, found by the two-placement simulation of
kebag-logic/milan-fpga#665.

## The three defects, reproduced at main `044cb25f`

The new `tb/srp_top` group `applicant` (rows AP1 to AP7), run on the base HDL with this head's testbench:
`18 checks: 9 PASS, 9 FAIL`.

- One New. AP1: the Domain declared at LINK_UP with no peer sent `New@202 JoinMt@1002 JoinMt@2002 ...`; AP2: VID 2
  sent `New@401 JoinIn@1201 ...`. Table 10-3: tx! from VN sends New (AN), tx! from AN sends New again.
- JoinIn with the Registrar MT. AP3: VID 2 sent 4 JoinIn and 0 JoinMt with no peer, and JoinIn again after the peer's
  Lv. 10.7.6.3: sJ is JoinIn only with the Registrar IN.
- No MVRP LeaveAll with nothing declared. AP5 (from Begin!, no VID ever declared) and AP6 (every declaration
  withdrawn): no MVRP LeaveAll at all. 10.7.9, Table 10-5: the LeaveAll state machine runs whatever the participant
  declares; Milan v1.2 Table 4.3: 10 to 15 s.

AP7 (the round's drain waits for the Domain's tx!) also fails at the base. At this head the group reads
`18 checks: 18 PASS, 0 FAIL`.

## The fix: the Applicant and LeaveAll machines

- `hdl/srp/srp_pkg.sv`: the Table 10-3 Applicant, row by row (`srp_app_next`, `srp_app_rx_next`, `srp_app_msg`,
  `srp_app_declaring`). Notes 4, 5 (operPointToPointMAC) and 8 (AN on tx!: QA with the Registrar IN, AA otherwise).
  sJ and s encode against the Registrar (10.7.6.3, 10.7.6.5).
- `hdl/srp/KL_srp_domain.sv`: the declared Domain value has that Applicant. LINK_UP (Begin!, New!) and an adoption
  (New!) enter VN. Every message is decided at an MSRP tx! (the join round's, or the own sLA round's on the txLA!
  row). rLA!, periodic! and the value's received events move the state. Its Registrar follows Table 10-4 with Milan
  v1.2 4.2.7.2.2.
- `hdl/srp/KL_srp_vlan.sv`: each VID entry has its own Applicant and a one-bit Table 10-4 Registrar (MVRP as printed).
  A first user's join is New!, the last user's leave Lv! (the entry stays until its tx! sends the Lv). Received VID
  values, LeaveAll and periodic! reach every entry. An MVRP tx! walks the entries.
- `hdl/srp/KL_srp_top.sv`: an MVRP tx! round (VID walk, then the drain). An own MVRP expiry makes the LeaveAll state
  machine Active, and the next MVRP tx! is its sLA (Table 10-5), whether or not a VID is declared; a peer MVRP
  LeaveAll on that edge wins (Passive). The MSRP round's drain waits for the Domain's tx! as it waits for the stream
  walks.
- `hdl/srp/KL_srp_encoder.sv`: an MVRP drain also starts for its LeaveAll alone, which is the LeaveAll-only MVRPDU:
  one VID message, NumberOfValues 0, a zero FirstValue (10.8.2.8 f).
- Talker Advertise and Listener were checked for the same behaviour. Their Applicants already followed Table 10-3
  (AP4 passes at the base), and they are now held by the arms `talker-one-new` and `listener-one-new`.

No top-level port, parameter or register-map change. `KL_srp_top`'s port list is unchanged, and the new ports are
internal (`KL_srp_domain`, `KL_srp_vlan`). `hdl/adp`, `hdl/aecp` and `hdl/acmp` are untouched. No MRP timer changed.

## Tests and planted arms

Each new row has an arm that must fail it by name in `make -C tb/srp_top mutants`. The three acceptance arms:

| Arm | What it plants | Fails |
|---|---|---|
| `domain-one-new`, `vlan-one-new` | LINK_UP / a first user's New! enters AN: one New, as the base | AP1 / AP2 (and encoder D1 / V1) |
| `vlan-joinin-registrar-mt` | every VID sJ JoinIn, the Registrar MT | AP2, AP3 (and encoder V3) |
| `mvrp-leaveall-needs-content` | an MVRP drain needs a pending VID, as the base | AP5, AP6 (and encoder L7) |

The others: `talker-one-new`, `listener-one-new` (AP4); `top-mvrp-la-flag-dropped`, `domain-txla-row-ignored`
(AP5, AP6); `top-mvrp-drain-at-tick` (AP2); `top-round-ignores-domain` (AP7); `vlan-registrar-never-in`,
`vlan-rlv-ignored` (AP3); and the encoder-level Domain and VID arms (DT, DA, V, VR rows). The record is in
`docs/architecture/09_verification.md` 8.15 and the `tb/srp_top` and `tb/srp_encoder` READMEs.

Two existing rows changed with the fix:

- M11 (`tb/srp_top` peer) now feeds a peer JoinIn of the Domain before the release. Since this change the Domain has
  its JoinMt to send at that round's tx!, so the round was never empty and the arm `empty-canceled-pdu` could not
  show. With the JoinIn (AA to QA) the round is empty again: the control passes 90 of 90, and the arm fails M11.
- OV0 to OV10 (group onevec, issue #214) now hold while either layer does. Each Applicant decides one message per tx!,
  and the encoder merges a second push of a pending value. So `second-queueing` and `join-displaces-new` alone no
  longer fail them; both are still killed at the encoder (PV rows). The new arm `push-twice-encoder-appends`
  removes both layers (the intake takes every push twice, and the encoder appends) and fails OV0 to OV10. The
  assertion coverage now requires OV1 to OV10 (OV8 to OV10 had no arm before). The push-twice hunk alone passes
  onevec.

## Docs

`docs/architecture/10_srp_engine.md` section 6.1 and F10.2 (the Domain's Applicant and its message ladder: New, New,
then sJ), section 6.2 and F10.3 (each VID's Applicant and Registrar), sections 3, 5 and 5.1 (storage and area), and
6.5 (the MVRP LeaveAll with nothing declared). `09_verification.md` 8.14 (the OV controls) and 8.15 (new). The
`tb/srp_top`, `tb/srp_encoder` and `tb/pp_top` READMEs.

## Area

The processor's syn/yosys flow, xc7, flattened, base `044cb25f` to this head:

| Shape | LUT | FF | RAM cells |
|---|---|---|---|
| `KL_srp_top` 2x2 | 13,536 to 14,109 (+573) | 5,407 to 5,447 (+40) | 114 to 112 |
| `KL_srp_top` 8x8 | 28,002 to 28,814 (+812) | 11,297 to 11,337 (+40) | 179 to 177 |
| `KL_srp_domain` | 150 to 215 (+65) | 119 to 128 (+9) | 0 |
| `KL_srp_vlan` | 364 to 594 (+230) | 132 to 147 (+15) | 3 to 1 |

## Gates at this head

All on a clean clone of this head, each rc 0:

| Gate | Command | Result |
|---|---|---|
| docs | `make check` | OK |
| matrix | `python3 scripts/gen_matrix.py --check` | `matrix: OK (94 rows, 0 untested)` |
| HDL lint | `bash scripts/lint_hdl.sh` | every module `LINT OK` |
| suites | `bash scripts/run_suites.sh` (with `REQ_TAG_LOG`) | 36 suites, `1032092 checks total, 0 failing` (srp_top 8703, srp_encoder 1646, pp_top 11066) |
| requirement tags | `python3 scripts/check-req-tags.py --suites ... --evidence ...` | `266 evidence lines, 14 suites, OK` |
| portability | `bash syn/yosys/run.sh`; `python3 -B tb/elab_guards/guards.py --frontend yosys --jobs 4` | every top OK; `93 checks: 93 PASS, 0 FAIL` |
| whitespace | `git diff --check 044cb25f HEAD` | empty |
| SRP campaign | `make -C tb/srp_top mutants` | `350 checks: 350 PASS, 0 FAIL`, every arm killed, `assertion coverage: 184/184` |
| AECP campaigns | `make -C tb/pp_top aecp-mutants`; `make -C tb/pp_top aecp-dispatch-mutants` | `67 checks: 67 PASS, 0 FAIL`; `105 checks: 105 PASS, 0 FAIL` (100 arms killed) |

## Consumer gate (scratch milan-fpga dev `ac0a01e3` with this head pinned)

A local copy of milan-fpga dev `ac0a01e3` with protocol-processor pinned at this head and its ROM digests
re-recorded with `syn/yosys/ooc.sh --record-rom-digests`, committed locally, not pushed. The rtl-fast workflow's run
steps, milan_dp, and the docs workflow's gates that read the processor tree: 40 gates, each rc 0.

| Job | Result |
|---|---|
| `make -C tb/verilator/milan_dp` | 19 `RESULT: PASS`, 0 FAIL |
| firmware-srp-mutants (`test_ctrl_firmware.py --shard 3/4`: both SRP mutation campaigns and the pin controls) | PASS |
| firmware-control-mutants (`--shard 1/4`) | `mutants: 523 of 523 caught` |
| firmware-aecp-mutants (`--shard 2/4`) | PASS |
| firmware-unit (`--shard 0/4`, ctrl_nvm, coverage) | PASS, `firmware coverage: PASS (30 files)` |
| firmware-boundary, firmware-verilator | `ctrl_boundary: PASS` each |
| changes, verilator-lint, bdd-conformance | PASS; `LINT GATE: PASS (89 violation(s) <= ratchet 89)`; 508 scenarios passed |
| yosys-elaboration, publication-census | PASS; resource gate baseline PASS, its 236 mutants fail; census arms all prove |
| docs ratchets and idiom gates | each OK |

The two-placement simulation of kebag-logic/milan-fpga#665 (`make -C tb/verilator/milan_dp twin`), on a local copy
with this head pinned, reports its three owed rows for this defect as gone:

```
[DIFF] owed row fabric-mvrp-leave-all: the defect has gone, the all-fabric half's grade finds none of it; the lane that fixed it (#857 (a release-image defect)) deletes the row
[DIFF] owed row fabric-domain-one-new: the defect has gone, the all-fabric half's grade finds none of it; the lane that fixed it (#860 (a release-image defect)) deletes the row
[DIFF] owed row fabric-vid2-join-in: the defect has gone, the all-fabric half's grade finds none of it; the lane that fixed it (#860 (a release-image defect)) deletes the row
twin: 3 finding(s)
```

Its exit status is nonzero until the parent deletes those three rows when it adopts this head. The fourth owed row,
`entity-available-index` (#217), still holds. It belongs to that issue.
