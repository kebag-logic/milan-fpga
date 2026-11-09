[A754] MRP Applicant: New on two tx!, sJ by the Registrar, LeaveAll with nothing declared, and each VID across a link change (IEEE 802.1Q-2018 Table 10-3, Table 10-4, 10.7.6.3, 10.7.9)

Closes #216

Parent issues: kebag-logic/milan-fpga#860 and kebag-logic/milan-fpga#857, found by the two-placement simulation of
kebag-logic/milan-fpga#665. This PR carries the branch `216-mrp-applicant` from main `044cb25f` to `84f6d6a`: the
six commits first reviewed as PR #218 (head `60094a2`) and four commits that answer its two reviews and the round 2
ruling on #216.

## The three defects, reproduced at main `044cb25f`

The `tb/srp_top` group `applicant`, run on the base HDL with the testbench of `60094a2`: `18 checks: 9 PASS, 9 FAIL`.

- One New. AP1: the Domain declared at LINK_UP with no peer sent `New@202 JoinMt@1002 JoinMt@2002 ...`; AP2: VID 2
  sent `New@401 JoinIn@1201 ...`. Table 10-3: tx! from VN sends New (AN), tx! from AN sends New again.
- JoinIn with the Registrar MT. AP3: VID 2 sent 4 JoinIn and 0 JoinMt with no peer, and JoinIn again after the peer's
  Lv. 10.7.6.3: sJ is JoinIn only with the Registrar IN.
- No MVRP LeaveAll with nothing declared. AP5 (from Begin!, no VID ever declared) and AP6 (every declaration
  withdrawn): no MVRP LeaveAll at all. 10.7.9, Table 10-5: the LeaveAll state machine runs whatever the participant
  declares; Milan v1.2 Table 4.3: 10 to 15 s.

At this head the group reads `21 checks: 21 PASS, 0 FAIL` (AP1 to AP8).

## The fix: the Applicant and LeaveAll machines

- `hdl/srp/srp_pkg.sv`: the Table 10-3 Applicant, row by row (`srp_app_next`, `srp_app_rx_next`, `srp_app_msg`,
  `srp_app_declaring`), with notes 4, 5 (operPointToPointMAC) and 8 (AN on tx!: QA with the Registrar IN, AA
  otherwise). sJ and s encode against the Registrar (10.7.6.3, 10.7.6.5).
- `hdl/srp/KL_srp_domain.sv`: the declared Domain value has that Applicant. LINK_UP (Begin!, New!) and an adoption
  (New!) enter VN; every message is decided at an MSRP tx! (the join round's, or the own sLA round's on the txLA!
  row). Its Registrar follows Table 10-4 with Milan v1.2 4.2.7.2.2.
- `hdl/srp/KL_srp_vlan.sv`: each VID entry has its own Applicant and a one-bit Table 10-4 Registrar (MVRP as
  printed). A first user's join is New!, the last user's leave Lv!; received VID values, LeaveAll and periodic! reach
  every entry; an MVRP tx! walks the entries. A link change: LINK_DOWN (Flush!) and LINK_UP (Begin!) take every VID
  Registrar to MT, winning over a received value of their clock (Table 10-4), and LINK_UP is Begin! on every VID
  Applicant, then New! for each VID with users (Table 10-3), so the new link partner gets New, New, then the Join, as
  it does for the Domain. A VID with no user left is VO there and is discarded (note 11); a message the walk holds
  for the encoder when the link comes up is withdrawn and the VID sends New instead. LINK_DOWN leaves the Applicants
  as they are (Flush! is a Registrar event, 10.7.5.2).
- `hdl/srp/KL_srp_top.sv`: an MVRP tx! round (VID walk, then the drain). An own MVRP expiry makes the LeaveAll state
  machine Active, and the next MVRP tx! is its sLA (Table 10-5), whether or not a VID is declared; a peer MVRP
  LeaveAll on that edge wins (Passive). The MSRP round's drain waits for the Domain's tx! as it waits for the stream
  walks. The VID participant gets the engine's `link_up_i`. An elaboration guard refuses `N_VIDS_P` above
  `ENC_DEPTH_P`, where the MVRP round would wait on its own walk (there is no MVRP high-water drain); the defaults
  (4, 12) and the processor top pass.
- `hdl/srp/KL_srp_encoder.sv`: an MVRP drain also starts for its LeaveAll alone, the LeaveAll-only MVRPDU: one VID
  message, NumberOfValues 0, a zero FirstValue (10.8.2.8 f).
- Talker Advertise and Listener were checked for the same behaviour: their Applicants already followed Table 10-3 for
  a new declaration (AP4 passes at the base); the arms `talker-one-new` and `listener-one-new` now hold it.

No top-level port, parameter or register-map change: `hdl/top` is untouched and `KL_srp_top`'s ports and parameters
are unchanged; the new ports are on `KL_srp_domain` and `KL_srp_vlan`, both internal. `hdl/adp`, `hdl/aecp` and
`hdl/acmp` are untouched. No MRP timer changed.

## Tests and planted arms

Each new row has an arm that must fail it by name in `make -C tb/srp_top mutants`. The issue's three acceptance arms:

| Arm | What it plants | Fails |
|---|---|---|
| `domain-one-new`, `vlan-one-new` | LINK_UP / a first user's New! enters AN: one New, as the base | AP1 / AP2 (and encoder D1 / V1) |
| `vlan-joinin-registrar-mt` | every VID sJ JoinIn, the Registrar MT | AP2, AP3, AP8 (and encoder V3) |
| `mvrp-leaveall-needs-content` | an MVRP drain needs a pending VID, as the base | AP5, AP6 (and encoder L7) |

The VID across a link change: `tb/srp_top` AP8 (the Registrar IN from the peer's JoinIn, the link down for 30 ms and
up: no VID 2 JoinIn after it, and New, New, then JoinMt, the first within 240 ms of LINK_UP) and `tb/srp_encoder`
VR14 to VR18 (LINK_DOWN takes IN to MT and leaves the Applicant; LINK_UP takes IN to MT and restarts in VN; a
received JoinIn on either link clock registers nothing; a VID whose Lv is owed with no user sends nothing; a message
held across LINK_UP is withdrawn, and on the clock the walk evaluates a VID the LINK_UP comes first). Arms:
`vlan-link-keeps-registrar`, `vlan-link-no-begin`, `top-vlan-link-unwired` (AP8), `vlan-link-rx-wins` (VR16),
`vlan-link-keeps-leaving` (VR17), `vlan-link-push-kept`, `vlan-link-after-tx` (VR18).

The two Table 10-3 rows where VP and AP differ, on the Domain (DA6, DA7) and on VID 2 (VR12, VR13): a peer LeaveAll
riding its JoinIn leaves VP alone (note 4), so JoinIn goes out on two tx!, then nothing; after a peer Lv, the own
LeaveAll's tx! from VP sends Mt (s, then AA), then one JoinMt. Arms `vp-rjoinin-ignores-note4`, `vp-txla-stays-vp`,
`vp-txla-sends-sj`.

The elaboration guard `KL_srp_top.g_vids_fit` is in `tb/elab_guards` (refused as a `$fatal` by Verilator and Yosys at
13 VIDs, elaborates at 12), with the bench's five arms.

The other arms of the first commits: `talker-one-new`, `listener-one-new` (AP4); `top-mvrp-la-flag-dropped`,
`domain-txla-row-ignored` (AP5, AP6); `top-mvrp-drain-at-tick` (AP2); `top-round-ignores-domain` (AP7);
`vlan-registrar-never-in`, `vlan-rlv-ignored` (AP3); and the encoder-level Domain and VID arms (DT, DA, V, VR rows).
Two existing rows changed with the fix: M11 (a peer JoinIn of the Domain before the release, so the canceled round is
empty again and `empty-canceled-pdu` shows) and OV0 to OV10 (graded by `push-twice-encoder-appends`, which removes
both layers that keep one vector per value). The record is in `docs/architecture/09_verification.md` 8.15 and the
`tb/srp_top` and `tb/srp_encoder` READMEs, every count measured at this head.

## Known, recorded, not changed here

- A VID a peer registered before the first local join is first answered JoinMt and is IN from the peer's next
  declaration: the VID's Registrar exists from its first local join. Recorded as GAP-18 in
  `docs/00_MILAN_COMPLIANCE_REVIEW.md` with its basis: Table 10-3 note 11 covers discarding the Applicant only, and a
  Table 10-4 Registrar would read IN. It errs the conservative way (never JoinIn without IN).
- The talker and listener stream Applicants have no link input. Measured: after a 30 ms link bounce a declared Talker
  Advertise is not declared again with New; it goes out as JoinMt at the next `periodic!` (872 ms after LINK_UP in
  the probe). A Listener Ready is withdrawn with its sink registration and declared again (New, New, then JoinMt)
  once the peer's Talker Advertise registers again. That is filed as #220.

## Docs

`docs/architecture/10_srp_engine.md`: 6.1 and F10.2 (the Domain's Applicant and its message ladder, the VP rows),
6.2 and F10.3 (each VID's Applicant and Registrar, the link change, the pre-join registration as a recorded
deviation), 3, 5 and 5.1 (storage and area), 6.5 (the MVRP LeaveAll with nothing declared, every `T-MRP-LEAVEALL`).
`docs/00_MILAN_COMPLIANCE_REVIEW.md` GAP-18. `09_verification.md` 8.14 (the OV controls) and 8.15. The `tb/srp_top`,
`tb/srp_encoder`, `tb/pp_top` and `tb/elab_guards` READMEs.

## Area

The processor's syn/yosys flow, xc7, flattened, base `044cb25f` to this head:

| Shape | LUT | FF | RAM cells |
|---|---|---|---|
| `KL_srp_top` 2x2 | 13,536 to 14,108 (+572) | 5,407 to 5,447 (+40) | 114 to 112 |
| `KL_srp_top` 8x8 | 28,002 to 28,903 (+901) | 11,297 to 11,337 (+40) | 179 to 177 |
| `KL_srp_domain` | 150 to 215 (+65) | 119 to 128 (+9) | 0 |
| `KL_srp_vlan` | 364 to 643 (+279) | 132 to 148 (+16) | 3 to 1 |

The VID link change alone is 49 LUT and 1 FF of `KL_srp_vlan`; in `KL_srp_top` it is inside the flow's LUT noise
(-1 at 2x2, +89 at 8x8) with no flip-flop.

## Gates at this head

All on clean clones of this head, each rc 0:

| Gate | Command | Result |
|---|---|---|
| docs | `make check` | OK |
| matrix | `python3 scripts/gen_matrix.py --check` | `matrix: OK (94 rows, 0 untested)` |
| HDL lint | `bash scripts/lint_hdl.sh` | every module `LINT OK` |
| suites | `bash scripts/run_suites.sh` with `REQ_TAG_LOG`, run as four shards (the script's own text, its suite loop split by suite index) | 36 suites PASS, `1032113 checks total, 0 failing` (srp_top 8706, srp_encoder 1659, pp_top 11066) |
| requirement tags | `python3 scripts/check-req-tags.py --suites ... --evidence ...` on the merged shard records | `266 evidence lines, 14 suites, OK` |
| portability | `bash syn/yosys/run.sh`; `python3 -B tb/elab_guards/guards.py --frontend yosys --jobs 4` | every top OK; `96 checks: 96 PASS, 0 FAIL` |
| nvm_port figures | `make -C tb/nvm_port figures` (with PR #13's ref fetched, as CI does) | `all measured figures agree with the tree` |
| whitespace | `git diff --check 044cb25f HEAD` | empty |
| SRP campaign | `make -C tb/srp_top mutants` | `365 checks: 365 PASS, 0 FAIL`, every arm killed, `assertion coverage: 185/185` |
| AECP campaigns | `make -C tb/pp_top aecp-mutants`; `make -C tb/pp_top aecp-dispatch-mutants` | `67 checks: 67 PASS, 0 FAIL`; `105 checks: 105 PASS, 0 FAIL` (100 arms killed) |
| MAAP, ADP, AECP command campaigns | `make -C tb/maap mutants`; `make -C tb/adp_engine mutants`; `make -C tb/aecp_cmds mutants` | `32 checks: 32 PASS`; `62 checks: 62 PASS`; `17 of 17 detected by their named failures` |
| elaboration-guard campaign | `make -C tb/elab_guards mutants` | `165 of 165 killed`, the new guard's five arms among them |

The two reviews' Applicant probes are killed at this head: `p09-note4-inverted` fails DA6 and VR12, and
`p12-txla-vp-stays` and `p19-txla-vp-sends-sj` fail DA7 and VR13, each `1659 checks: 1657 PASS, 2 FAIL`. The second
review's link-bounce probe passes: VID 2 after LINK_UP sends `New@3801 New@4001 JoinMt@4201`.

Every README arm count the new rows move was re-measured. Against the campaign at this head, the only counts that
differ from the previous head are those 12 arms. Seven older `tb/srp_top/README.md` counts were stale before this
PR (`pending-peer-ignored`, `mvrp-supersedes-msrp`, `leaveall-expiry-lost`, `preparation-before-slot`,
`mvrp-expiry-only-redraw`, `stale-expiry-honoured`, `mvrp-stale-expiry-honoured`). They are unchanged here and left
for a follow-up.

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
| yosys-elaboration, publication-census | PASS; resource gate `baseline PASS: 3 endpoints`, its 236 mutants fail; census arms all prove |
| docs ratchets and idiom gates | each OK |

The two-placement simulation of kebag-logic/milan-fpga#665 (`make -C tb/verilator/milan_dp twin`), on a local copy
with this head pinned, reports its three owed rows for this defect as gone:

```
[DIFF] owed row fabric-mvrp-leave-all: the defect has gone, the all-fabric half's grade finds none of it; the lane that fixed it (#857 (a release-image defect)) deletes the row
[DIFF] owed row fabric-domain-one-new: the defect has gone, the all-fabric half's grade finds none of it; the lane that fixed it (#860 (a release-image defect)) deletes the row
[DIFF] owed row fabric-vid2-join-in: the defect has gone, the all-fabric half's grade finds none of it; the lane that fixed it (#860 (a release-image defect)) deletes the row
twin: 3 finding(s)
```

Its exit status is nonzero until the parent deletes those three rows when it adopts this head. The other owed rows
still hold and are not this issue's (`entity-available-index` belongs to #217).
