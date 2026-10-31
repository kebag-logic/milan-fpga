[A700f]

## Contents

- **[Status](#status)** -- Review ready at the head below, carrying PR #826's commits; the route meets the floor; `787-reboot-reset` -> `dev`.
- **[Linked Issue / roles](#linked-issue--roles)** -- The task, the release gate it serves, and roles.
- **[Description](#description)** -- The reset on an AECP REBOOT, the processor pin, the silicon defect this round fixes and how it is graded.
- **[Authoritative references](#authoritative-references)** -- The clauses, the processor PR and the design pages.
- **[How to get into the same state](#how-to-get-into-the-same-state)** -- Checkout, submodules and tools.
- **[How to validate](#how-to-validate)** -- The gate commands and the expected results, and the route timing measured at the head.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** -- The record, the bench step and what this PR does not change.
- **[Definition of Done](#definition-of-done)** -- The merge bar from CONTRIBUTING.md.

## Status

**REVIEW READY** at `cbc7c6043ebf84d5bcd74652dc0a7131b7d54271`. `787-reboot-reset` -> `dev` (`02ca829a`).
**This PR carries PR #826's commits (#814, `814-soc-timing-cut` at `4ee2aa96`) and PR #820's (#818, `818-wns-gate` at `81f78a81`), and merges after both.** Rounds 4 and 5
each merge into the branch. Neither changes the reset on an AECP REBOOT (IEEE 1722.1-2021 7.4.43, Milan v1.2
5.4.5.2) or its ENTITY_DEPARTING (Milan v1.2 5.6.3.3).

- **Round 5 merges PR #826.** One merge commit, `f7d5fc3c`, of `4ee2aa96` into round 4's head `3e67de9c`.
  - It is clean: there is no conflict.
  - Its change against the branch has the same patch-id as #826's own change against dev `1e80128f`.
  - #826 changes no gitlink, no HDL and no generator, so nothing was regenerated. The ROM ledger, the boundary
    diagram, the port census and the MAC model each check unchanged at the merge.
- **Round 4 merges dev `02ca829a`:** PR #813 (#806, gPTP `135afd04`), PR #821 (#817) and PR #816 (#70).
  - Six files conflicted: `CHANGELOG.md`, `docs/design/AREA_BUDGET.md`, `docs/reference/SUBMODULES.md`, and the
    submodule-boundaries diagram with its PNG manifest.
  - The three documents keep both sides' facts. The diagram records were produced again by their generator.
  - One more commit re-records the port census in `scripts/port_docs.budget` through its generator: hdl 2181,
    gptp-processor 127 and protocol-processor 1771 ports. That is base plus each side's per-file additions.
  - Round 4's route missed the floor, at +0.018 ns. Its deciding path was LiteDRAM's ZQCS timer into the bank
    machines, the path #826 cuts.
- **Gates at the head pass.**
  - `git diff --check` against dev: rc 0.
  - The LiteX simulations: 8 of 8. Among them is #826's `test_soc_timing_cuts`: 23 arms, `RESULT: PASS`.
  - The static and pin-record bank, 32 of 32. The builder bank passes, except the same two arms this host cannot
    exercise. xvlog: 0 findings.
  - The MAC model check, and #70's service budget at 69 checks: both read `milan_soc.py`.
  - rtl-fast: every job succeeds; behave has 14 features and 508 scenarios.
  - The docs workflow: 44 steps, 0 failed. Builder leg 1 with LiteX passes, and the markdown gates pass 5 of 5.
  - From round 4 at `3e67de9c`, on inputs #826 does not change:
    - the milan_dp suites: 14,516 checks, 0 failures;
    - `[RB]`: 68 checks;
    - `reboot-mutant`: 6 of 6;
    - #70's `dynmap-mutants`: 66 of 66.
- **The route meets the floor.** Route-1x1 on the three placement directives, judged by the #818 gate: rc 0,
  `RESULT: PASS`.
  - The gate selects AltSpreadLogic_high at +0.365 ns worst-corner WNS. ExtraTimingOpt has +0.204 ns and
    ExtraPostPlacementOpt +0.090 ns.
  - Hold, every resource figure and every ceiling pass.
  - LiteDRAM's ZQCS timer no longer appears among any directive's listed `sys` paths ([Route timing](#route-timing)).

Round 6 (manager, on R731-3 and R732-3):
- `ddbf87e6` regenerates `docs/diagrams/cdc_census.{svg,drawio}` through `cdc_census.gen.py` and re-renders its PNG.
  This branch's PHY hold is the third SoC MultiReg call site (`x3`); round 2 had left the record at two.
- `6ffadb07` merges PR #820's head `81f78a81`, so that its edit of the same `AREA_BUDGET.md` paragraph composes here.
- `cbc7c604` states the re-pin route measured in round 5 (+0.365 ns, 52,021 LUTs, 63 slices left, the #818 gate
  PASS) in `docs/reference/SUBMODULES.md` and `docs/design/AREA_BUDGET.md`. It names the `1be824fc` route's gPTP pin
  (`f97c1803`), states that route's 0.333 ns fall as refused before #818, and names #806 where "this change" had lost its referent.

## Linked Issue / roles

Relates to #787 (the bench soft-reset run on the shipping image closes it)

Relates to #396

Carries PR #826 (#814): this PR holds its commits, through the merge of `814-soc-timing-cut` at `4ee2aa96`, and merges after it.

Executor: `[A700f]` (round 5, the merge of PR #826; `[A700e]` round 4, the merge of dev; `[A700d]` round 3, the route; `[A700c]` round 2; `[A700]` round 1)
Internal cleared-context reviewer: `[R731]`
External reviewer: `[R732]`

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
bash scripts/run_litex_sims.sh <litex-logs>
cd sw/litex
python3 test_soc_timing_cuts.py
cd ../..
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
- The model check prints OK.
- The LiteX aggregate prints `simulations: 8   passed: 8   failed: 0   skipped: 0   timed out: 0`.
- `test_soc_timing_cuts.py` prints 23 `[ok  ]` arms, `test_soc_timing_cuts: 0 failure(s)` and `RESULT: PASS`. Run
  alone it took 686 s here, and in the aggregate 789 s. On a loaded host it can pass the aggregate's 900 s limit a
  member, as PR #826's review notes. The aggregate then reports the member TIMED OUT, result unknown, not failed: it
  did so once here, and the run was repeated unchanged.
- The sweep reports every suite PASS.

### Route timing

Route-1x1 at the head `f7d5fc3c`, Vivado 2026.1, recipe unchanged
([`docs/testing/PP_SHADOW_BASELINE_RECIPE.md`](docs/testing/PP_SHADOW_BASELINE_RECIPE.md), "Integrated measurements"),
default seed. One synthesis, then the three placement directives from its checkpoint, in parallel. The set is judged
by the #818 route-set gate (`syn/ooc/pp_resource_gate.py` as PR #820 has it at `50e5d08d`; that file is not part of
this PR). **The gate passes the set**: rc 0, `RESULT: PASS`. It selects AltSpreadLogic_high for the best worst-corner
WNS, +0.365 ns, and holds the +0.030 ns setup and 0 ns hold floors at every signoff corner.

| Directive | WNS ns, Slow 0C / 85C | WNS ns, Fast 0C / 85C | WHS ns, Slow / Fast | TNS / THS ns | LUT | FF | Slices (free) |
|---|---|---|---|---|---:|---:|---|
| AltSpreadLogic_high (selected) | **+0.365 / +0.365** | +1.633 / +1.633 | +0.053 / +0.015 | 0 / 0 | 52,021 | 54,102 | 15,787 (63) |
| ExtraTimingOpt | +0.204 / +0.204 | +1.633 / +1.633 | +0.053 / +0.015 | 0 / 0 | 52,017 | 54,101 | 15,787 (63) |
| ExtraPostPlacementOpt | +0.090 / +0.090 | +1.660 / +1.660 | +0.052 / +0.028 | 0 / 0 | 51,960 | 54,101 | 15,820 (30) |

Every directive has RAMB36 74, RAMB18 27, DSP 13 and 87.5 Block RAM tiles (ceiling 121.5). Every route completes
with no routing error. Against the record, the selected route is within every tolerance: LUT +9, FF +395, slices
+7. The WNS fall from the record's +0.440 ns is 0.075 ns, under the 0.25 ns warning.

The deciding path of each directive:

| Directive | Slack ns | Clock | Path | Levels, route share | Family |
|---|---:|---|---|---|---|
| AltSpreadLogic_high | +0.365 | `sys`, 100 MHz | `VexiiRiscvLitex_*/dma_bridge_write_bridge/aligner/downW_header_reg[2]_replica` -> `.../onPerId_bridge/pendings_valids_reg[0]/D` | 18, 76 % | F4: the CPU's DMA write bridge, inside the generated VexiiRiscv netlist |
| ExtraTimingOpt | +0.204 | Milan, 50 MHz | `pp_shadow/u_pp/u_aecp/u_ucpu/uop_e_r_reg[imm][0]` -> `u_aecp/u_d3/deb_cnt_r_reg[0]/R` | 36, 65 % | the processor's AECP: the micro-CPU's immediate into the NVM writer's debounce counter |
| ExtraPostPlacementOpt | +0.090 | Milan, 50 MHz | `pp_shadow/u_pp/u_aecp/u_ucpu/uop_e_r_reg[imm][0]` -> `u_aecp/u_d3/deb_cnt_r_reg[25]/R` | 36, 66 % | the same AECP path |

- F1 to F3 are #826's three families: the flash bridge, the DRAM arbitration and the refresh path. None of them is
  among any directive's listed `sys` paths. On ExtraPostPlacementOpt the worst `sys` path is +0.452 ns, a LiteDRAM
  bank machine's row register into the write-to-read turnaround timer.
- F4 is the family the F4 ruling on #814 (issuecomment-6516396929) accepts as the one that decides the record.
- The AECP path lies wholly in `KL_aecp_ucpu`, `KL_aecp_nvm_writer` and `KL_aecp_dyn_state`, which this PR's
  processor pin `a9e84b66` does not change against dev's `f65c8ff7`.
- On the selected directive the Milan clock's worst path is +0.540 ns, from `u_notify` into `u_event_router`. The AECP
  path is at +0.823 ns there.

**Against the earlier route sets** (one seed per directive each):

| Directive | Worst-corner WNS ns: round 3 (`667b9bbc`) -> round 4 (merge of dev) -> this head | LUT | Slices (free) |
|---|---|---|---|
| AltSpreadLogic_high | +0.151 -> +0.000 -> **+0.365** | 51,520 -> 52,370 -> 52,021 | 15,837 (13) -> 15,824 (26) -> 15,787 (63) |
| ExtraTimingOpt | +0.120 -> +0.017 -> **+0.204** | 51,524 -> 52,367 -> 52,017 | 15,837 (13) -> 15,824 (26) -> 15,787 (63) |
| ExtraPostPlacementOpt | +0.165 -> +0.018 -> **+0.090** | 51,568 -> 52,291 -> 51,960 | 15,749 (101) -> 15,837 (13) -> 15,820 (30) |

With #826's cuts every directive gains, and the best directive is 0.200 ns above round 3's best. PR #826's own set,
dev `1e80128f` plus #814, selected ExtraTimingOpt at +0.406 ns. It was measured at `0d4a899f`; #826's head changes
only the test and `TESTING.md` after that. The resource record is not re-recorded.

This PR's own logic in the route:
- The frame-end toggle crosses from the Ethernet clock into the Milan clock, under that pair's 8 ns `Max Delay
  Datapath Only` bound.
- On the selected directive the toggle's own path has +6.44 ns, and the pair's worst is +6.12 ns over its 51
  endpoints. On ExtraPostPlacementOpt the pair's worst is +6.44 ns.
- The MultiReg census (`eth=12 part=199`) and check_timing are as before the merge.
- No route log has a critical warning or an error. ICAPE2 and STARTUPE2 are both placed.

The other checks at the head: `python3 scripts/xvlog_gate.py --check` reports 0 findings. The IOB packing check
reports `IOB-PACK OK` for 22 ports on each directive, and `python3 sw/litex/iob_pack_selftest.py` passes. The #607
implementation-log check finds no 12-4739, 20-1307 or 12-5201 diagnostic in any route log.

To judge a route set the same way, with the three runs prepared as the recipe says:

```sh
python3 syn/ooc/pp_resource_gate.py check "$WORK/ax7101/gateware" --endpoint route-1x1 \
  --comparison "$WORK/ax7101-AltSpreadLogic_high" --comparison "$WORK/ax7101-ExtraTimingOpt"
```

Expected at this head (with #820's gate): `directive AltSpreadLogic_high selected: the best worst-corner WNS, 0.365 ns`,
every figure `ok`, and `RESULT: PASS`, rc 0.

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


