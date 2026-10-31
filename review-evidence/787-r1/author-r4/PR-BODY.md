[A700e]

## Contents

- **[Status](#status)** -- STOP at the head below: the merge of dev is clean, the route misses the floor; `787-reboot-reset` -> `dev`.
- **[Linked Issue / roles](#linked-issue--roles)** -- The task, the release gate it serves, and roles.
- **[Description](#description)** -- The reset on an AECP REBOOT, the processor pin, the silicon defect this round fixes and how it is graded.
- **[Authoritative references](#authoritative-references)** -- The clauses, the processor PR and the design pages.
- **[How to get into the same state](#how-to-get-into-the-same-state)** -- Checkout, submodules and tools.
- **[How to validate](#how-to-validate)** -- The gate commands and the expected results, and the route timing measured at the head.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** -- The record, the bench step and what this PR does not change.
- **[Definition of Done](#definition-of-done)** -- The merge bar from CONTRIBUTING.md.

## Status

**STOP** at `3e67de9c1d42557f222edd2b079d23265bf1b726`: the route misses the floor. `787-reboot-reset` -> `dev`
(`02ca829a`). This round merges dev `02ca829a` into the branch, with no behaviour change. Dev's new merges are PR #813
(#806, gPTP `135afd04`), PR #821 (#817) and PR #816 (#70). The pushed head stays `4aa5666e` until the owner rules.

- **The merge is clean.** Six files conflicted: `CHANGELOG.md`, `docs/design/AREA_BUDGET.md`,
  `docs/reference/SUBMODULES.md`, and the submodule-boundaries diagram with its PNG manifest. The three documents
  keep both sides' facts. The diagram records were produced again by their generator at the merged tree. No
  conflict needed a behaviour choice, and no RTL, test or build file conflicted.
- **Every regenerated record is the union of the two sides.**
  - The ROM ledger re-records byte-identical to the textual merge.
  - The diagram differs from this lane's copy only in the gPTP pin, and from dev's only in the processor pin.
  - One more commit re-records the port census in `scripts/port_docs.budget` through its generator: hdl 2181,
    gptp-processor 127 and protocol-processor 1771 ports. That is base plus each side's per-file additions; the
    ratchets are unchanged.
- **Gates at the head pass.**
  - `git diff --check` against dev: rc 0.
  - The static and pin-record bank, 32 of 32; the builder bank passes except the same two arms this host cannot
    exercise.
  - The milan_dp suites: 14,516 checks, 0 failures. milan_dp is 13,796 = this branch's 13,757 + 16 from #806's
    gPTP legs + 23 from #70's volatile-set block.
  - The campaigns whose inputs the merge changed: `[RB]` 68 checks, `reboot-mutant` 6 of 6, the LiteX simulations
    7 of 7, the MAC model check, and #70's service budget 69 checks.
  - #70's `dynmap-mutants`: 66 of 66 arms caught, every clean leg passing. Its two end-to-end arms needed a second
    run: their legs' suites must first make the inputs the campaign keeps unmade.
  - rtl-fast: every job succeeds, behave 14 features and 508 scenarios. The docs workflow: 44 steps, 0 failed;
    builder leg 1 with LiteX passes; the markdown gates 5 of 5. xvlog: 0 findings.
- **The route misses the floor.** Route-1x1 on the three placement directives, judged by the #818 gate: rc 1,
  `RESULT: MATERIAL REGRESSION`. The best directive, ExtraPostPlacementOpt, has +0.018 ns worst-corner WNS at both
  slow corners. AltSpreadLogic_high has +0.000 ns and ExtraTimingOpt +0.017 ns. Hold, every resource figure and
  every ceiling pass. All three worst paths are in the SoC's SDRAM controller, outside this PR
  ([Route timing](#route-timing)).

One pre-existing record was found stale and not changed in a merge-only round:
`docs/diagrams/cdc_census.{svg,drawio}`. Its generator now counts three SoC MultiReg call sites, this branch's PHY
hold being the third; the committed file says two.

## Linked Issue / roles

Relates to #787 (the bench soft-reset run on the shipping image closes it)

Relates to #396

Executor: `[A700e]` (round 4, the merge of dev; `[A700d]` round 3, the route; `[A700c]` round 2; `[A700]` round 1)
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
git fetch origin dev
git diff --check "$(git merge-base origin/dev HEAD)" HEAD
python3 docs/diagrams/submodule_boundaries.gen.py --check
python3 scripts/check_submodule_docs.py
bash syn/yosys/ooc.sh --record-rom-digests
git diff --exit-code syn/yosys/rom_digests.tsv
python3 scripts/check_port_contracts.py
make -C tb/verilator/reboot_ctrl
make -C tb/verilator/pp_shadow build-base exec-base SIM_ARGS=--reboot-only
make -C tb/verilator/pp_shadow reboot-mutant
make -C tb/verilator/milan_dp
make -C tb/verilator/milan_dp dynmap-mutants DYNMAP_MUTANT_JOBS=4
make -C tb/verilator/milan_dp_render ltn_rom.hex ucode.hex tdm8r_aemi.bin
make -C tb/verilator/capture_coherence ltn_rom.hex ucode.hex
unset MAKEFLAGS
cd tb/verilator/milan_dp
python3 dynmap_mutants.py --jobs 2 36 37
cd ../../..
python3 sw/builder/test_builder.py
python3 sw/litex/gen_mac_tx_model.py --check
bash scripts/run_all_suites.sh <logs> --wait
```

Expected result / pass criteria:

- `git diff --check` prints nothing.
- The diagram check prints `OK (6 exact gitlinks, decoded PNG)`, and the submodule documentation check prints
  `OK (6 exact gitlinks)`.
- The ROM ledger re-records with no diff.
- The port contract gate passes with hdl 2181, gptp-processor 127 and protocol-processor 1771 ports.
- `reboot_ctrl` passes both legs (221 and 46 checks), and 30 of 30 mutants are killed.
- `[RB]` passes alone (68 checks), and `reboot-mutant` reports 6 of 6 arms caught.
- milan_dp passes with 13,796 checks.
- From a clean clone, `dynmap-mutants` catches 64 of its 66 arms and fails its two end-to-end legs' controls: the
  campaign builds them with `make -o` over inputs their own suites make. With those inputs made, arms 36 and 37 and
  both controls pass. Together that is all 66 arms, the README's count.
- The builder bank prints `ALL GATES PASS`. Two arms stay NOT RUN where the host cannot exercise them: gate 1b's
  `MAKEFLAGS += -e` arm, and gate 11 without an Arty build tree.
- The model check prints OK, and the sweep reports every suite PASS.

### Route timing

Route-1x1 at the merge `5640e4d7`, Vivado 2026.1, recipe unchanged
([`docs/testing/PP_SHADOW_BASELINE_RECIPE.md`](docs/testing/PP_SHADOW_BASELINE_RECIPE.md), "Integrated measurements"),
default seed. One synthesis, then the three placement directives from its checkpoint, in parallel. The head
`3e67de9c` differs from `5640e4d7` only in `scripts/port_docs.budget`, which no synthesis input reads. The set is
judged by the #818 route-set gate (`syn/ooc/pp_resource_gate.py` as PR #820 has it at `50e5d08d`; that file is not
part of this PR). **The gate refuses the set**: rc 1, `RESULT: MATERIAL REGRESSION`. It selects ExtraPostPlacementOpt
for the best worst-corner WNS, +0.018 ns, which is below the +0.030 ns floor at both slow corners.

| Directive | WNS ns, Slow 0C / 85C | WNS ns, Fast 0C / 85C | WHS ns, Slow / Fast | TNS / THS ns | LUT | FF | Slices (free) |
|---|---|---|---|---|---:|---:|---|
| ExtraPostPlacementOpt (selected) | **+0.018 / +0.018** | +1.633 / +1.633 | +0.062 / +0.033 | 0 / 0 | 52,291 | 53,833 | 15,837 (13) |
| AltSpreadLogic_high | **+0.000 / +0.000** | +1.456 / +1.456 | +0.058 / +0.030 | 0 / 0 | 52,370 | 53,833 | 15,824 (26) |
| ExtraTimingOpt | **+0.017 / +0.017** | +1.513 / +1.513 | +0.051 / +0.013 | 0 / 0 | 52,367 | 53,833 | 15,824 (26) |

Every directive has RAMB36 74, RAMB18 27, DSP 13 and 87.5 Block RAM tiles (ceiling 121.5). Every route completes
with no routing error. The resource figures are inside their tolerances against the record: LUT +279, FF +126,
slices +57. The WNS fall from the record's +0.440 ns is also printed as the #818 WARNING.

The worst setup path of each directive is in the 100 MHz `sys` clock, in the SoC's SDRAM controller, which neither
this PR nor dev's three merges change:

| Directive | Slack ns | Path | Levels, route share |
|---|---:|---|---|
| ExtraPostPlacementOpt | +0.018 | `milansoc_sdram_zqcs_timer_count1_reg[2]` -> `subfragments_bankmachine3_state_reg[0]/CE` | 18, 74 % |
| AltSpreadLogic_high | +0.000 | `milansoc_sdram_zqcs_timer_count1_reg[13]` -> `subfragments_bankmachine2_state_reg[0]/CE` | 16, 79 % |
| ExtraTimingOpt | +0.017 | `milansoc_sdram_zqcs_timer_count1_reg[10]` -> `milansoc_sdram_bankmachine0_level_reg[2]/CE` | 17, 76 % |

**Against each side's own route set** (one seed per directive each):

| Directive | Worst-corner WNS ns: this branch before the merge (`667b9bbc`) -> #806 (PR #813) -> the merge | LUT | Slices (free) |
|---|---|---|---|
| ExtraPostPlacementOpt | +0.165 -> +0.032 -> **+0.018** | 51,568 -> 51,837 -> 52,291 | 15,749 (101) -> 15,823 (27) -> 15,837 (13) |
| AltSpreadLogic_high | +0.151 -> +0.235 -> **+0.000** | 51,520 -> 51,874 -> 52,370 | 15,837 (13) -> 15,837 (13) -> 15,824 (26) |
| ExtraTimingOpt | +0.120 -> +0.218 -> **+0.017** | 51,524 -> 51,849 -> 52,367 | 15,837 (13) -> 15,837 (13) -> 15,824 (26) |

Each side's best directive met the floor: +0.165 ns before the merge, and +0.235 ns for #806. The merged image's
best is +0.018 ns. With one seed per directive, and all three worst paths in SDRAM-controller logic outside both
changes, this measurement cannot separate a design effect from placement. The resource record is not re-recorded.

This PR's own logic in the route: the frame-end toggle crossing from the Ethernet clock into the Milan clock is under
its 8 ns `Max Delay Datapath Only` bound, at +6.62 ns over 51 endpoints. The MultiReg census is the same as before
the merge, and so is check_timing. The shipping log has no critical warning and no error. ICAPE2 and STARTUPE2 are
both placed.

The other checks at the head: `python3 scripts/xvlog_gate.py --check` reports 0 findings. The IOB packing check
reports `IOB-PACK OK` for 22 ports on each directive, and `python3 sw/litex/iob_pack_selftest.py` passes. The #607
implementation-log check finds no 12-4739, 20-1307 or 12-5201 diagnostic in any route log.

To judge a route set the same way, with the three runs prepared as the recipe says:

```sh
python3 syn/ooc/pp_resource_gate.py check "$WORK/ax7101/gateware" --endpoint route-1x1 \
  --comparison "$WORK/ax7101-AltSpreadLogic_high" --comparison "$WORK/ax7101-ExtraTimingOpt"
```

Expected at this head (with #820's gate): `directive ExtraPostPlacementOpt selected`, then `REGRESSION: below the
floor 0.03 at Slow_0C, Slow_85C` and `RESULT: MATERIAL REGRESSION`, rc 1.

## Known limitations / out of scope

- **The resource record is not re-recorded here.** Under the record rule it is re-recorded once on dev, after the
  last release merge. This PR's route is measured against the current record and passes.
- **The bench decides the end-to-end claim.** The manager rebuilds the pre-run image with this fix, and the bench
  re-runs the REBOOT checks: the DEPARTING on the wire, then the #396 power area's 50 soft resets. #787 stays open
  until that run.
- **What the egress wait cannot see.** A frame the MAC takes and never sends (its internal loopback, or a reset of one
  side only) keeps the count high, and the wait ends at its bound. A frame another source starts on the clock the wait
  ends is lost with the reset, as at a cut; the REBOOT's own frames are all counted before then.

## Definition of Done

- [ ] Linked Issue acceptance criteria are satisfied (the bench soft-reset run remains)
- [x] New or changed behavior has self-checking tests
- [ ] Required local verification bar passes (route-1x1 set: the #818 gate refuses it at this head, below the +0.030 ns floor; xvlog, IOB packing and the #607 log check pass)
- [ ] Self-test evidence is posted in a PR comment
- [x] No undocumented requirement or interface change remains
- [ ] Internal cleared-context review is positive
- [ ] External review is positive
- [ ] Blocking and major findings are fixed and re-reviewed
- [ ] No review round remains in flight
- [ ] Candidate merge result is validated per [CONTRIBUTING.md](CONTRIBUTING.md)
- [x] Documentation is updated where needed
- [ ] Post-merge containment will be checked before the Issue moves to Done

