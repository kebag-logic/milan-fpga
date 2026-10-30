[A700d]

## Contents

- **[Status](#status)** -- Review ready at the head below; `787-reboot-reset` -> `dev`.
- **[Linked Issue / roles](#linked-issue--roles)** -- The task, the release gate it serves, and roles.
- **[Description](#description)** -- The reset on an AECP REBOOT, the processor pin, the silicon defect this round fixes and how it is graded.
- **[Authoritative references](#authoritative-references)** -- The clauses, the processor PR and the design pages.
- **[How to get into the same state](#how-to-get-into-the-same-state)** -- Checkout, submodules and tools.
- **[How to validate](#how-to-validate)** -- The gate commands and the expected results, and the route timing measured at the head.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** -- The record, the bench step and what this PR does not change.
- **[Definition of Done](#definition-of-done)** -- The merge bar from CONTRIBUTING.md.

## Status

**REVIEW READY** at `667b9bbc02b99a08d71efab750f95e8702cbbe57`; `787-reboot-reset` -> `dev` (`1e80128f`). Gates at that head:

- The full sweep: 65 of 65 suites, each once, 2,192,196 checks, 0 in-suite failures, none timed out. They include
  `reboot_ctrl` (298) and `pp_shadow` (2,514, with section `[RB]` on its three full legs).
- The rtl-fast workflow, every job: success; behave 14 features, 508 scenarios.
- Yosys: 61 of 61 tops; tied inputs justified; tap purity PASS.
- The static and pin-record bank: 32 of 32. The builder bank passes except two arms this host cannot exercise. RTL
  lint, the idiom and evidence ratchets, the port contracts and the pin records all pass.
- The docs workflow at the head: 44 steps, 0 failed; builder leg 1 with the LiteX interpreter passes; the markdown
  gates 5 of 5; the no-git step's gates pass.
- The mutant drivers this PR adds: `reboot_ctrl` 30 of 30, `pp_shadow` `reboot-mutant` 6 of 6, builder gate 1f 9 of 9.
- Route-1x1 on the recipe's three placement directives from one synthesis: the #818 route-set gate `RESULT: PASS`,
  ExtraPostPlacementOpt selected at +0.165 ns, both floors met at every corner. xvlog 0 findings; IOB packing OK;
  the #607 log check clean on each route log ([Route timing](#route-timing)).

The sweep, rtl-fast and Yosys ran at `e12147d4`. From there to the head only a mutant driver, three documents, the
generated pin records and the processor gitlink change, and the gitlink moves to a commit with the identical tree.
Every gate that reads those ran again at the head. The route and xvlog ran at the head itself.

## Linked Issue / roles

Relates to #787 (the bench soft-reset run on the shipping image closes it)

Relates to #396

Executor: `[A700d]` (round 3, the route; `[A700c]` round 2; `[A700]` round 1)
Internal cleared-context reviewer: `[R<n>]`
External reviewer: `[R<n>]`

## Description

A controller's AECP REBOOT of ENTITY 0 (IEEE 1722.1-2021 7.4.43) resets the end station, so the #396 release gate's 50
soft resets can run. The reset is a configuration reload from flash through ICAPE2 IPROG, after the saved state drains
and with the PHY held in reset. The decision, what each candidate resets, the bound and the JTAG argument are in
[`docs/design/REBOOT_RESET.md`](docs/design/REBOOT_RESET.md).

### The defect this round fixes

On silicon, a REBOOT of an advertising entity sent SUCCESS and the notification, then nothing: no ENTITY_DEPARTING, no
gPTP. Milan v1.2 5.6.3.3 (SHUTDOWN), 5.6.3.5.8, 5.6.3.5.11 and Table 5.51 require the DEPARTING, and so do IEEE
1722.1-2021 6.2.4.1.3 and 6.2.5.2.2.

**The cause.** `KL_reboot_ctrl` raised the PHY hold two clocks after `reboot_req_o`. The processor raises the request
once the DEPARTING's last byte has left its own transmit face. At that moment the frame is still in the SoC's MAC:
`mac_tx_cdc`, the store-and-forward `tx_sf`, LiteEth's transmit crossing and pipeline, and the PHY stage. The PHY reset
dropped it. `pp_shadow` section `[RB]`, now graded at a MAC model's wire-side output, reproduces this on the unfixed
RTL: the DEPARTING never leaves the MAC.

**The fix.** `KL_reboot_ctrl` gains an EGRESS phase between the saved-state drain and the PHY hold.

| Piece | Change |
|---|---|
| `hdl/milan/KL_reboot_ctrl.sv` | An account from reset counts frames in on the MAC port's handshake and out on the MAC's frame-end toggle, three-flop synchronised. EGRESS ends on a millisecond tick once nothing is half taken at the port and nothing is in the MAC, and the path has stayed so on every clock since the previous tick. That quiet millisecond covers the PHY's own transmit path. Otherwise EGRESS ends at `T_EGRESS_MS_C`. The count saturates, so it can only lengthen the wait, and the link guard's full reset episode clears it |
| The bound | `T_EGRESS_MS_C` is derived, not copied: the time to send the MAC's stated octets at its slowest line rate, rounded up to whole ms, plus the quiet ms. The statement is every transmit buffer, each buffered frame's framing and one maximum envelope frame (IEEE 802.3-2022 3.2.1, 3.2.2, Table 4-2). The result is 2 ms on the AX7101 (GMII, 1 Gb/s) and 11 ms on the Arty (MII, 10 Mb/s slowest) |
| `hdl/milan/milan_datapath.sv` | The MAC's statement as two parameters (`REBOOT_MAC_TX_OCTETS_P`, `REBOOT_MAC_MIN_MBPS_P`) and the toggle as one input (`i_ethtxend_tgl`). The account reads the existing RMON tap of the MAC port. The MAC handshake assignments are unchanged |
| `sw/litex/milan_soc.py` `MilanMAC` | `ethtxend_tgl`, a reset-less toggle flipped on each frame's last octet at LiteEth's `phy.sink`, the seam the gPTP launch observer already reads. `_mac_tx_egress_octets` computes the statement from the named depths the FIFOs are built with: 11,656 octets. The PHY model gives the slowest line rate. The no-MAC stub ties the toggle 0 |
| The builder | `reboot_mac_statement` evaluates the same SoC definitions to state the two parameters, so gate 23m holds the SoC's Instance to them. New gate 1f holds the FIFOs to the named depths and the toggle to its seam, with nine planted cuts. Gate 1d admits the toggle's reads of `phy.sink` |
| Bound restated | From `reboot_req_o` to the IPROG word: at most drain + egress + hold + 3 ms + 8 clocks. That is 13,505 ms on the AX7101, 13,514 ms on the Arty and 13,531 ms at the datapath's default statement (13,502 ms before the egress wait) |
| Not gated | The MAC port is not stopped during the wait. Builder gate 1b holds the MAC handshake direct and censuses its references: no gate may sit between the MAC-boundary arbiter and the MAC, which is the gPTP plane's direct path (#187). Every frame the REBOOT owes was handed over before the request, so the account already holds it. Frames other sources start later are counted while the path still empties; one that starts on the clock the wait ends is lost with the reset, as at a cut |

**The signal used** ([A10]'s question): frames counted in at the datapath's own `m_axis_mac_tx` handshake, and out
at LiteEth's `phy.sink` through the new reset-less toggle. Both are parent code; no submodule changes.

### Processor pin

`protocol-processor` is pinned at `a9e84b66`, the merge commit of processor PR #209 (#203). Its tree is the reviewed
head `013ee63f`'s, where `reboot_req_o` rises only after every frame the processor started has left. The ROM ledger
rows and the boundary diagram were regenerated through their generators, and the pin table updated.

### Tests

| Suite | What it grades |
|---|---|
| `tb/verilator/pp_shadow` section `[RB]` | three REBOOTs graded at a MAC model's wire-side output. **Advertising**, with a second controller and KL_maap probing: SUCCESS, the notification and ENTITY_DEPARTING whole and in order before the PHY hold, which follows the request and comes more than 1 ms and at most two ticks after the last frame; no frame cut or left in the MAC. **Not advertising**: no DEPARTING, and the hold after the last frame the port started. **A dead transmit clock**: the hold at the egress bound. `make reboot-mutant` plants six arms, each failing its named check: the request ignored, an early request, the PHY hold on the request alone, an egress wait that ignores the MAC FIFO, one with no bound, and the toggle unwired |
| `tb/verilator/reboot_ctrl` | the account and every bound at two MAC statements and three tick phases, the stated bound to the IPROG word, and a frame between two ticks restarting the quiet millisecond; 30 planted mutants, each failing its named check |
| `sw/builder/test_builder.py` | gates 1f, 23m, 1d and 1b as above |

## Authoritative references

- IEEE 1722.1-2021 7.4.43 (REBOOT), 6.2.4.1.3 (doTerminate), 6.2.5.2.2 (txEntityDeparting)
- Milan v1.2 5.6.3.3, 5.6.3.5.8, 5.6.3.5.11, Table 5.51 (the SHUTDOWN event)
- IEEE 802.3-2022 3.2.1, 3.2.2, Table 4-2 (preamble, start delimiter, maxEnvelopeFrameSize, minFrameSize, interPacketGap)
- IEEE 802.1AS-2011 11.2.2, 11.2.15, 10.2.4.7 (the gPTP relock the #396 power area grades)
- Processor PR #209 (#203), merge commit `a9e84b66` (tree of the reviewed head `013ee63f`)
- [`docs/design/REBOOT_RESET.md`](docs/design/REBOOT_RESET.md), [`docs/design/SAVED_STATE_FASTCONNECT.md`](docs/design/SAVED_STATE_FASTCONNECT.md) 7, 9
- [`docs/litex/CLOCK_DOMAINS.md`](docs/litex/CLOCK_DOMAINS.md) (the frame-end toggle crossing), [`docs/integration/INTEGRATION_GUIDE.md`](docs/integration/INTEGRATION_GUIDE.md) (the End-station reset group)

## How to get into the same state

```sh
git fetch origin
git checkout 787-reboot-reset
git submodule update --init third_party/verilog-axis protocol-processor gptp-processor third_party/lwSRP third_party/tsn-c-stack
git -C protocol-processor rev-parse HEAD
```

Expected: `a9e84b66d4cd0c331c8d6f2c1a71a62fcc824645`. Verilator 5.050, Yosys 0.66 and sv2v v0.0.12 as
`docs/testing/TESTING.md` section 2 lists; the pinned LiteX interpreter for the builder's LiteX gates.

## How to validate

```sh
make -C tb/verilator/reboot_ctrl
make -C tb/verilator/pp_shadow build-base exec-base SIM_ARGS=--reboot-only
make -C tb/verilator/pp_shadow reboot-mutant
make -C tb/verilator/pp_shadow
python3 sw/builder/test_builder.py --gates test_baremetal_profile_contract,test_gptp_launch_observer_seam,test_reboot_egress_statement,test_reboot_egress_statement_gate_bites,test_datapath_params_match_the_instance,test_datapath_params_gate_bites
python3 sw/litex/gen_mac_tx_model.py --check
bash scripts/run_all_suites.sh <logs> --wait
```

Expected result / pass criteria: `reboot_ctrl` passes both legs (221 and 46 checks) and 30 of 30 mutants are killed.
`[RB]` passes alone, and `reboot-mutant` reports 6 of 6 arms caught. The four `pp_shadow` legs pass. The builder subset
prints `ALL GATES PASS`, with one gate 1b arm NOT RUN where make does not re-read MAKEFLAGS. The model check prints OK.
The sweep reports every suite PASS.

### Route timing

Route-1x1 at `667b9bbc`, Vivado 2026.1, recipe unchanged
([`docs/testing/PP_SHADOW_BASELINE_RECIPE.md`](docs/testing/PP_SHADOW_BASELINE_RECIPE.md), "Integrated measurements"),
default seed. One synthesis, then the three placement directives from its checkpoint, in parallel. The set is judged by
the #818 route-set gate (`syn/ooc/pp_resource_gate.py` as PR #820 has it at `32f0d9b5`; that file is not part of this
PR). The gate passes: ExtraPostPlacementOpt is selected, the best worst-corner WNS.

| Directive | WNS ns, Slow 0C / 85C | WNS ns, Fast 0C / 85C | WHS ns, Slow / Fast | TNS / THS ns | LUT | FF | Slices (free) |
|---|---|---|---|---|---:|---:|---|
| ExtraPostPlacementOpt (selected) | +0.165 / +0.165 | +1.565 / +1.565 | +0.102 / +0.036 | 0 / 0 | 51,568 | 53,680 | 15,749 (101) |
| AltSpreadLogic_high | +0.151 / +0.151 | +1.331 / +1.331 | +0.061 / +0.032 | 0 / 0 | 51,520 | 53,682 | 15,837 (13) |
| ExtraTimingOpt | +0.120 / +0.120 | +1.331 / +1.331 | +0.101 / +0.036 | 0 / 0 | 51,524 | 53,680 | 15,837 (13) |

Every directive has RAMB36 74, RAMB18 27, DSP 13 and 87.5 Block RAM tiles (ceiling 121.5). Every route completes
with no routing error.

The worst setup path of each directive is in the 100 MHz `sys` clock, in SoC memory-path logic this PR does not
change:

| Directive | Slack ns | Path | Levels, route share |
|---|---:|---|---|
| ExtraPostPlacementOpt | +0.165 | `milansoc_write_w_buffer_readable_reg` -> `storage_15_reg_1/ENARDEN` | 10, 83 % |
| AltSpreadLogic_high | +0.151 | `milansoc_write_w_buffer_level0_reg[0]` -> `storage_10_dat1_reg[20]/D` | 12, 82 % |
| ExtraTimingOpt | +0.120 | `FSM_sequential_subfragments_fsm2_state_reg[0]` -> `milansoc_tmod1_reg[11]/CE` | 16, 77 % |

**Against dev's own routes** (dev `1e80128f`, the same recipe; the same gate passes them with ExtraPostPlacementOpt at
+0.303 ns):

| Directive | WNS ns, dev -> head | WHS ns, dev -> head | LUT | FF | Slices (free) |
|---|---|---|---|---|---|
| ExtraPostPlacementOpt | +0.303 -> +0.165 (-0.138) | +0.028 -> +0.036 | 51,801 -> 51,568 (-233) | 53,760 -> 53,680 (-80) | 15,834 (16) -> 15,749 (101) |
| AltSpreadLogic_high | +0.230 -> +0.151 (-0.079) | +0.014 -> +0.032 | 51,846 -> 51,520 (-326) | 53,759 -> 53,682 (-77) | 15,795 (55) -> 15,837 (13) |
| ExtraTimingOpt | +0.106 -> +0.120 (+0.014) | +0.054 -> +0.036 | 51,833 -> 51,524 (-309) | 53,758 -> 53,680 (-78) | 15,794 (56) -> 15,837 (13) |

One directive rose and two fell. With one seed each, that is within the placement spread across directives. Against
the current record (+0.440 ns) the selected WNS is 0.275 ns lower. The gate prints that as a WARNING, reported and
never gated (#818); the floor is the gate.

This PR's own logic in the route: `KL_reboot_ctrl` is 46 LUTs and 34 FFs in context. The frame-end toggle crossing
from the Ethernet clock into the Milan clock is under the 8 ns `Max Delay Datapath Only` bound, with that pair at
+5.87 ns. The PHY hold's crossing into `sys` is a MultiReg with `ASYNC_REG`. The CDC report gains that one synchroniser
and is otherwise dev's. check_timing is dev's, and neither route log has a critical warning or an error. ICAPE2 and
STARTUPE2 are both placed.

The other checks at the head: `python3 scripts/xvlog_gate.py --check` reports 0 findings over every hdl/ and
pinned-processor source, including the three changed RTL files. The IOB packing check reports `IOB-PACK OK` for 22
ports on each directive, and `python3 sw/litex/iob_pack_selftest.py` passes. The #607 implementation-log check finds
no 12-4739, 20-1307 or 12-5201 diagnostic in any route log.

To judge a route set the same way, with the three runs prepared as the recipe says:

```sh
python3 syn/ooc/pp_resource_gate.py check "$WORK/ax7101/gateware" --endpoint route-1x1 \
  --comparison "$WORK/ax7101-AltSpreadLogic_high" --comparison "$WORK/ax7101-ExtraTimingOpt"
```

Expected (with #820's gate): `directive ExtraPostPlacementOpt selected`, every corner at or above +0.030 ns setup and
0 ns hold, and `RESULT: PASS`.

## Known limitations / out of scope

- **The resource record is not re-recorded here.** Under the record rule it is re-recorded once on dev, after the
  last release merge. This PR's route is measured against the current record and passes.
- **The bench decides the end-to-end claim.** The manager rebuilds the pre-run image with this fix, and the bench
  re-runs the REBOOT checks: the DEPARTING on the wire, then the #396 power area's 50 soft resets. This PR does not
  close #787.
- **What the egress wait cannot see.** A frame the MAC takes and never sends (its internal loopback, or a reset of one
  side only) keeps the count high, and the wait ends at its bound. A frame another source starts on the clock the wait
  ends is lost with the reset, as at a cut; the REBOOT's own frames are all counted before then.

## Definition of Done

- [ ] Linked Issue acceptance criteria are satisfied (the bench soft-reset run remains)
- [x] New or changed behavior has self-checking tests
- [x] Required local verification bar passes (route-1x1 set, xvlog, IOB packing and the #607 log check included)
- [ ] Self-test evidence is posted in a PR comment
- [x] No undocumented requirement or interface change remains
- [ ] Internal cleared-context review is positive
- [ ] External review is positive
- [ ] Blocking and major findings are fixed and re-reviewed
- [ ] No review round remains in flight
- [ ] Candidate merge result is validated per [CONTRIBUTING.md](CONTRIBUTING.md)
- [x] Documentation is updated where needed
- [ ] Post-merge containment will be checked before the Issue moves to Done
