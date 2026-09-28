[R368] NEGATIVE - exact head 792a57b092efaee8920f344faacb7675c8e163bd

# R368-1 internal independent review: issue #590 / PR #609 (with #592 and #599 simulation scope)

- Head reviewed: `792a57b092efaee8920f344faacb7675c8e163bd`, tree `111acdbb305c57aedae2e7451cd13fbc2f96d79b`, in a clean detached clone.
- Source base: `8bc97021f28fb7f729418d3a00851c84ea0b50fd`. The lane-owned diff was read against the merged dev parent `20aa4eabf` (processor pin `16be6768f710e79450aace277abacd6c2c3336e5`).
- Round: R368-1, the first review of this PR. No earlier public review findings exist on PR #609, so none needed to be resolved or retained.
- Authorities read:
  - AGENTS.md and CONTRIBUTING.md.
  - Issue #590: body, assignment 5859537529, scope correction 5859930453, findings-page scope 5857603294, STOP and REVIEW READY.
  - Issue #592 and issue #599 bodies.
  - REQUIREMENTS.md REQ-MAC-03/08.
  - REGISTER_MAP, BAREMETAL_FIRMWARE, BOARD_PORTING_AX7101 §5, the compliance matrix and the 397 findings page.
  - `sw/litex/milan_soc.py` for `link_status` and the MilanMAC PHY; `hdl/milan/milan_datapath.sv` for the `eff_link` consumers.
  - Public evidence packet `0f817be126dcba12e1317a909946e08d58e47a2b:review-evidence/590-r1`.

## Verdict summary

NEGATIVE. Three findings are open: one BLOCKER, one MAJOR and one MINOR. Two SUGGESTIONs are optional.

What holds at this head:
- The capture copy (#592) and the dispatch and walk ticks (#590) behave as claimed inside their measured scope:
  - the 8x8 maximum is 13.23262 ms against 24.5 ms;
  - the byte-only control is 24.30636 ms;
  - `check_nvm_capture` passes;
  - the service receipts show zero unbacked cycles.
- The builder change is only the forced 2→4 selection count.
- There is no RTL or processor change in the lane.

Why the verdict is NEGATIVE:
1. **The firmware's MDIO read samples one bit late on a PHY that follows the IEEE 802.3 22.3.4 timing.** Both peer models encode the same assumption as the firmware, so every PHY test passes by construction. A review probe with a standard-timed peer shows the unchanged firmware reads BMSR `0x796d` as `0xf2db` and publishes **link down** (0) for a live 1000FD link. `eff_link` gates ADP and the datapath (`milan_datapath.sv:2904-2914`), so on the board the entity would stop advertising.
2. **Acceptance 1 of #590 asks for a tick "at each console command dispatch".** The implementation covers only the five registered Milan handlers. LiteX built-in commands, and queued input that is not a Milan command, still suppress every heartbeat and every PHY poll. The documentation sentence that recorded this residual was deleted, not narrowed.
3. **The #592 edge property "no access crosses the next record's boundary" has no killing test.** A planted edge-crossing word store passes the all-shape host gate. The target harness only admits captures with every record closed.

## Findings

### F1: BLOCKER: MDIO read data is sampled one MDC cycle late relative to IEEE 802.3 22.3.4; peers encode the same assumption

- **Lenses:** Conformance, RTL, Tests, Docs.
- **Where:**
  - `sw/firmware/milan_baremetal/milan_baremetal.c:790-822`: `phy_mdio_bit` samples in the high phase after the rising edge; `phy_mdio_read` discards input clock 46, takes `ack` on clock 47 and data on clocks 48-63.
  - `sw/firmware/nvm_hosttest/phy_host.c:33-60`: the host peer.
  - `tb/verilator/fw_service_budget/phy.hpp:14-27`: the simulation peer.
  - `docs/integration/BAREMETAL_FIRMWARE.md` (new PHY paragraph) and `docs/findings/397_SERVICE_BUDGET.md` ("An independent Clause-22 peer drives simulated MDIO pins").
- **Authority and evidence:**
  - IEEE 802.3 22.3.4: when MDIO is sourced by the PHY, the STA samples it on the rising edge of MDC. The PHY's clock-to-output delay is 0 to 300 ns from the rising edge. So the value visible after rising edge *k* is frame bit *k+1*.
  - The firmware reads 32 delay cycles after edge *k* (at least 320 ns by its own comment) and treats the value as bit *k*. It therefore reads the turnaround zero on the clock it discards, D15 as `ack`, and D14..D0 plus the released-line one as the data.
  - Upstream Linux `drivers/net/mdio/mdio-bitbang.c` (7.1.13; `MDIO_READ_DELAY 350` "the PHY may take up to 300 ns to produce data") clocks the same 46 command bits. It then checks the turnaround zero on the **first** input clock and reads data on the next 16. The firmware checks it on the **second**.
  - Both lane peers present bit *k* in response to edge *k*. That is the firmware's assumption, not the clause, so `test_phy_firmware.py` and the service harness cannot distinguish the two conventions.
  - Probe `probes/mdio_timing_probe.py` with `probes/mdio_peer_probe.c` (receipt `receipts/mdio_timing_probe.log`) uses the unchanged product translation unit:
    - Lane-convention peer: published 13. Correct under that peer.
    - 802.3-timed peer: BMSR read `0xf2db` for `0x796d`, published **0**.
    - The same peer with the turnaround sampled on the first input clock (the Linux shape): published 13.
    - The two conventions are mutually exclusive, and the firmware matches only the non-standard one.
- **Impact:**
  - On a standard-timed PHY every register read is shifted left by one bit. BMSR bit 2 reads as bit 1 (jabber, normally 0), so the firmware publishes `link_up=0` permanently.
  - `eff_link_w = i_link_up & cfg_sw_link & ...` gates ADP and the datapath, so the shipping ALINX images lose advertisement. The on-board Arty PHY on builds that carry the MDIO CSR is affected the same way.
  - Before this lane, `link_status` stayed at its reset value 1. The change therefore regresses a working bench image into an invisible one.
  - The #599 bench re-run is out of scope and would only detect this after merge to `dev`.
  - The documentation calls the peer "independent", which it is not with respect to this assumption.
- **Required outcome:**
  - Sample PHY-sourced bits at the 22.3.4 point. The turnaround zero belongs to the first input clock after the 46 command bits, with 16 data bits following. Alternatively, cite board-PHY evidence that the chosen phase is correct for every supported PHY.
  - Make at least one peer (host or simulation) launch read data per 22.3.4, independently of the firmware's convention.
  - Add a mutant with the off-by-one sampling that this peer kills.
  - Correct the "independent peer" wording.
- **Verification:** the probe here, or an equivalent committed test, publishes 13 for a `0x796d` BMSR under 802.3 timing. The one-bit-late mutant fails. `test_phy_firmware.py` and the service PHY checks stay green on the corrected peer.

### F2: MAJOR: dispatch ticks cover registered Milan commands only; BIOS built-ins and queued non-Milan input still starve heartbeat and PHY poll; the residual was deleted from the documentation

- **Lenses:** Conformance, Robustness, Docs.
- **Where:**
  - `sw/firmware/milan_baremetal/milan_baremetal.c:1635,1737,1770,1781,1802`: ticks at the entry of the five `define_command` handlers only.
  - `docs/integration/BAREMETAL_FIRMWARE.md` Runtime paragraph (`git diff 20aa4eabf..HEAD`, hunk at old line 1886).
  - `docs/findings/397_SERVICE_BUDGET.md` "Tick placement".
- **Authority and evidence:**
  - #590 acceptance 1 asks for "a heartbeat tick opportunity at each console command dispatch, and inside every console handler or walk that can exceed the tick period".
  - The manager decision reads: "An operator pasting commands must never lapse the saved-state liveness."
  - The mechanism the issue documents is the BIOS `readline` idle hook, which runs only while no byte is pending. It applies to every line, not only Milan commands.
  - `nvm_heartbeat_tick` has no caller on the path for LiteX built-in commands (the product BIOS is the full console; `milan_soc.py:2658` sets only `BIOS_NO_BOOT`) or for unknown or empty lines.
  - The harness plans (`tb/verilator/fw_service_budget/run.py:20-49`) exercise only Milan commands.
  - The pre-lane documentation said a console command running past 2,000 ms lets `nvm_backed` lapse until the prompt returns. The new text says "Every registered Milan command begins with a heartbeat opportunity" and "These placements service single long commands". It no longer states that long or queued non-Milan commands stay unserviced.
  - No public decision narrows acceptance 1 from "each console command dispatch" to "each registered Milan command". AGENTS.md §2 requires publishing such a conflict rather than choosing an interpretation.
  - This review did not measure the effect on the product CPU (no LiteX environment was available). The magnitude below is arithmetic from 115,200 baud serialization, not a measurement.
- **Impact:**
  - A pasted queue of LiteX `help` lines under the 128-byte ring, or one `mem_read` of a few KB, keeps the idle hook suppressed for well over 2,000 ms. `help` output alone is on the order of 1-2 KB per line.
  - That lapses T-NVM-WRITER-ALIVE, which is the #590 failure mode.
  - It also stops PHY publication for the same interval, so the stated 250 ms publication bound does not hold outside Milan commands.
  - Operators reading the new text would believe any single long command is serviced.
- **Required outcome:** one of the following.
  - (a) A heartbeat opportunity at every console dispatch, built-ins and unknown lines included, for example through the product LiteX patch series. Add a harness plan with queued non-Milan input that keeps backing.
  - (b) A published maintainer decision that scopes acceptance 1 to registered Milan commands. BAREMETAL_FIRMWARE.md and the findings page must then restate the residual, covering long built-ins and queued non-Milan input for both the heartbeat and the PHY publication bound.
- **Verification:**
  - For (a): a service plan of back-to-back built-in lines at least 133 bytes long, graded with `--enforce-service`, shows zero unbacked cycles. Removing the new dispatch hook fails it.
  - For (b): the decision link and the restored limitation text in both documents.

### F3: MINOR: the record-edge guard of the word-wide copy is untested; an edge-crossing word store survives every gate

- **Lenses:** Tests, Robustness.
- **Where:**
  - `sw/firmware/milan_baremetal/milan_baremetal.c:1174-1186`: `next - i >= 4u` guard.
  - `sw/firmware/nvm_hosttest/nvm_host.c:392-396`: ownership vector all-open or all-closed.
  - `tb/verilator/nvm_capture_cpu/run.py:59,88`: rows with `open != 0` are refused.
- **Authority and evidence:**
  - The BAREMETAL_FIRMWARE text and the code comment say "Never cross a record edge: its neighbour may be open". AGENTS.md §6 Tests says "each new test can fail for the defect it claims to detect".
  - Probe `probes/host_mutant.py edge-cross` changes the guard to `next - i >= 1u`, so a word may cover up to three bytes of the next record. The unchanged all-shape host gate returns OK for all five shapes (`receipts/mutant_edge_cross_host.log`).
  - In the target harness every published capture row has `open=0` (6×16 rows, receipt `measurements.json`). An overrun into a closed neighbour is rewritten with identical bytes, so byte equality cannot catch it either. This is an inference from code reading; the target mutant was not run here.
- **Impact:** a regression of the safety property that makes the word path legal, namely that an open neighbour keeps its last verified bytes, would merge green.
- **Required outcome:** a test with a partial ownership vector. For example, a host model or capture arm with an open record whose predecessor ends unaligned. The edge-crossing mutant must fail it.
- **Verification:** the mutant above is reported as a finding by the new test. The unmutated firmware passes.

### S1: SUGGESTION: grade the byte-only control automatically

The byte-only control (`tb/verilator/nvm_capture_cpu/run.py`, `--mutation byte-only`) is graded as a normal run and compared by hand ("Compare its measured interval…"). The published result (24.30636 ms against 13.23262 ms) does restore the old timing. A committed threshold, for example byte-only above the receipt maximum by a stated factor, would make it self-checking.

### S2: SUGGESTION: say that the capture build compiles the PHY path out

The capture SoC (`tb/verilator/nvm_capture_cpu/soc.py`) has no `milan_mac`, so `CSR_MILAN_MAC_PHY_MDIO_W_ADDR` is undefined and `phy_link_tick` is the empty stub in the measured binary. This is harmless for the ARM-to-ATTEST window, which contains no tick. The receipt nevertheless binds the product source digest, so the capture README or receipt should say which arm of that conditional was measured. The re-run rows after 5e8edc86 are identical to the earlier rows, which is consistent with this.

## Lens coverage and clean-result evidence

| Lens | Result | Examined artifacts at `792a57b0` |
| --- | --- | --- |
| Conformance | UNCLEAN (F1, F2) | Frozen acceptance: #590 1-4, #592 1-4, #599 1/2/3/5, and the scope correction. Checked `milan_baremetal.c` ticks (`:473,:636,:1635,:1737,:1754,:1770,:1781,:1802`), `PHY_POLL_NS` derived from `NVM_HEARTBEAT_NS/2` (`:773`), the 250 ms rate limit unchanged (`:925-929`), the Clause-22 register decode (`:826-871`: BMCR/BMSR/ESTATUS/1000T ctrl/status/ANAR/ANLPAR bit positions and priority correct), the `measurements.json` pin `16be6768` and firmware digest `91d6ca57…` equal to the head source hash, the 8x8 at 13.23262 ms against 24.5 ms, the findings page naming the measured tree, the `ac18b509` 100 MHz-declaration history and the 50 MHz figures. |
| RTL | UNCLEAN (F1) | The lane diff `20aa4eabf..HEAD` touches no `hdl/`, `sw/litex/` or `protocol-processor` (gitlink `16be6768` equals dev). The `link_status` CDC (`milan_soc.py:1782-1805`, MultiReg) and the fabric consumers `eff_link_w`/`ctr_linkup_r`/`ctr_linkdn_r` (`milan_datapath.sv:2904-2914,3472-3494`) are unchanged and consistent with the down-then-up single-poll publication (one MDIO read, about 126 µs, between writes). F1 is recorded here because it breaks the MDC sampling contract at the LiteEthPHYMDIO pin interface. |
| Robustness | UNCLEAN (F2, F3) | Traced the PHY paths: missing ACK → down; `0xffff`/0 ID → next address with no rate limit; latched loss → down, then a re-read in the same poll; read error while up → down; clock rewind → poll; retired writer keeps polling (`:873-907,:917-930`). The capture word path stays within `[off,next)` and below `NVM_AREA_RAW` (`:1170-1187`). Tick placement inside the commit (`nvm_seal`/`nvm_validate` after ATTEST) is not re-entrant. The residuals are F2 and F3. |
| Tests | UNCLEAN (F1, F3) | Re-ran at head (receipts): `test_nvm_firmware.py --self-test` (5 shapes, planted defects reddened, PHY mutants caught); `test_phy_firmware.py`; `check_nvm_capture.py`; `fw_service_budget` make (14 flash) and `--self-test` (42 checks); `test_builder.test_baremetal_profile_contract` rc 0 (the fixture count 4 = 2 planted selections × the new MDIO conditional; no other builder edit). Published controls: `remove-dispatch` lost backing (2769.99749 ms gap), `no-publish` detected, `byte-only` 24.30636 ms, `skip-copy`/`no-traffic` detected. Gaps are F1 (peer not independent) and F3 (edge mutant survives). |
| Docs | UNCLEAN (F1, F2) | Checked the BAREMETAL_FIRMWARE, REGISTER_MAP, compliance-matrix row 7.4.42.2, 397_SERVICE_BUDGET, fw_service_budget/README and nvm_capture_cpu/README diffs against the code and receipts: the publisher statement is present, the single-long and chained-short cases are present, the #599 bench deferral is stated. The defects are F1 ("independent peer") and F2 (deleted residual). |

## Reviewer-owned completion ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
| --- | --- | --- | --- | --- |
| Conformance | UNCLEAN | Issue acceptance and scope comments; `milan_baremetal.c` ticks, PHY and copy; `measurements.json`; `397_SERVICE_BUDGET.md` | R368-1 | `792a57b092efaee8920f344faacb7675c8e163bd` |
| RTL | UNCLEAN | Lane diff (no RTL); `milan_soc.py:1761-1805`; `milan_datapath.sv:2904-2914,3472-3494`; MDIO pin contract | R368-1 | `792a57b092efaee8920f344faacb7675c8e163bd` |
| Robustness | UNCLEAN | PHY error, latch and discovery paths; word-copy bounds; console dispatch coverage | R368-1 | `792a57b092efaee8920f344faacb7675c8e163bd` |
| Tests | UNCLEAN | Host, PHY, capture-gate, service and builder-fixture re-runs; MDIO and edge probes; published controls | R368-1 | `792a57b092efaee8920f344faacb7675c8e163bd` |
| Docs | UNCLEAN | BAREMETAL_FIRMWARE, REGISTER_MAP, compliance matrix, 397 findings, both harness READMEs | R368-1 | `792a57b092efaee8920f344faacb7675c8e163bd` |

## Real limits

- **No product-CPU simulation was run here.** No LiteX, CPU-netlist or SoC environment was available in the permitted areas, and the scoped Verilator path named in the assignment does not exist on this host. Capture, service, dispatch-removal, no-publish and byte-only results are taken from the public packet `0f817be1:review-evidence/590-r1`, which I read but did not reproduce.
- **F1 rests on the 802.3 clause text, the upstream reference reader and a host probe.** No board PHY timing was observed. F2's magnitude is arithmetic, not measurement. F3's target-side survival is inferred from the `open=0` admission rule.
- **The builder profile-contract test ran longer than the foreground limit** of the review session (13 min 21 s). It finished with rc 0 and its complete log is the receipt. No full builder, parent, processor, gPTP or Yosys bank was run.
- **Physical calibration was not run.** Field skips and simulation are not hardware proof.
- The `queued-short` service receipts are published only by hash. Their summary figures come from the findings page.

## Pending manager duties

- Hosted and act acceptance at the exact head, and the final current-dev candidate build (source base `8bc97021`, live dev `c0723222`) at the merge turn.
- The external review ([R369]).
- Routing F1, F2 and F3 to the executor. F2 needs a maintainer decision if option (b) is chosen.
- The #599 physical re-run lane after merge. With F1 open, its read-only BMSR check would itself be affected by the firmware's reader.

## Post-probe state

- `receipts/clean_state.txt`: HEAD and tree unchanged, empty porcelain status, index mode/blob/path listing identical to the HEAD tree.
- Gitlinks `protocol-processor 16be6768`, `gptp-processor 5dce647a` and `third_party/verilog-axis 48ff7a7e` are checked out clean. `external` is uninitialized, as at clone time.
- No source edits, commits, pushes or GitHub writes were made. All mutants ran from temporary copies or `scratch/`.

R368-1 FINISHED
