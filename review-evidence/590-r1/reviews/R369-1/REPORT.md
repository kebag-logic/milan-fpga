[R369] NEGATIVE - exact head 792a57b092efaee8920f344faacb7675c8e163bd

# R369-1 external independent review: PR #609 (#590, #592, #599)

- Round: R369-1, external reviewer, cleared context.
- Exact head: `792a57b092efaee8920f344faacb7675c8e163bd`, tree `111acdbb305c57aedae2e7451cd13fbc2f96d79b`.
- Source base: `8bc97021f28fb7f729418d3a00851c84ea0b50fd`; lane range read from the dev merge `20aa4eabf` to head.
- Processor pin at head: `16be6768f710e79450aace277abacd6c2c3336e5`.
- Scope sources: #590 body, assignment 5859537529, scope correction 5859930453, findings-page scope 5857603294; #592 and #599 bodies; PR #609 body; public evidence tree `0f817be1:review-evidence/590-r1` (111 entries, every published SHA-256 re-verified, 0 mismatches).
- Lenses applied: Conformance, RTL, Robustness, Tests, Docs.
- Overall result: one BLOCKER and one MINOR are open, so every lens is unclean. The #590 heartbeat work and the #592 copy are sound in what they cover. The #599 MDIO reader samples one bit late against IEEE 802.3.

## Findings

### F1 - BLOCKER - Conformance, RTL, Robustness, Tests - the firmware MDIO reader samples one bit late

- **Where:**
  - `sw/firmware/milan_baremetal/milan_baremetal.c:790-822` (`phy_mdio_bit`, `phy_mdio_read`; the ack is read at `:817`, the data at `:819`).
  - The two committed peers encode the same timing: `sw/firmware/nvm_hosttest/phy_host.c:55` and `tb/verilator/fw_service_budget/phy.hpp:26`.
- **Authority:**
  - IEEE 802.3 clause 22.3.4: "When the MDIO signal is sourced by the PHY, it is sampled by the STA synchronously with respect to the rising edge of MDC. The clock to output delay from the PHY ... shall be a minimum of 0 ns, and a maximum of 300 ns."
  - So a PHY-driven bit k is driven after rising edge k-1 and must be read before or at rising edge k.
  - Reference reader: LiteX `libliteeth/mdio.c` at the LiteX revision the capture receipt pins (`a1e1c365`). This is the BIOS reader for the same `LiteEthPHYMDIO` pins. It gives two turnaround clocks, then samples with MDC low **before** each data rising edge.
- **Evidence:**
  - The firmware also gives two turnaround clocks, but samples in the high phase **after** each rising edge.
  - The sample comes at least `cdelay(32)` plus a CSR access after the rise. The target measures 0.126 ms per 64-clock transaction (`docs/findings/397_SERVICE_BUDGET.md`), so the sample is roughly 1 us after the rise, well past the 300 ns maximum clock-to-output.
  - Against a standard PHY, "ack" is therefore D15 and the data word is D14..D0 followed by the idle pull-up bit.
  - Both committed peers instead change MDIO **at** rising edge k to frame bit k (TA2 at edge 47, D15 at edge 48). That is one bit later than clause 22.3.4, which is why both tests pass.
  - Reviewer probe `probe_mdio_phase.py` / `probe_mdio_phase.c` (output `probe_mdio_phase.out`) compiles the **unchanged** firmware translation unit the same way `test_phy_firmware.py` does. It runs against two peers that differ only in output phase, and reads each peer with the firmware and with the LiteX reference algorithm:
    - Committed-peer phase: the firmware reads BMSR `0x796d` correctly. The LiteX reference reads `0x3cb6`, so this peer is not what the BIOS reader talks to.
    - IEEE phase: the LiteX reference reads `0x796d` and PHYID1 `0x001c` correctly. The firmware reads `0xf2db` and `0x0039`, finds the PHY, and publishes `link_status=0` for a negotiated 1000/full link. The expected value is 13.
- **Impact:**
  - On a real Clause-22 PHY (the AX7101's RTL8211E; the Arty's on-board MII PHY is wired the same way), every register read is shifted left by one.
  - The BMSR link bit (bit 2) is read from jabber-detect (bit 1), which is 0 on a live link. So the shipping image publishes link down, 10 Mb/s, half duplex on every poll.
  - Before this PR the register held its reset default of link up and board speed. After it:
    - `eff_link_w` (`hdl/milan/milan_datapath.sv:2904`), which gates ADP and the datapath, is held low.
    - `o_mac_is_1g` and the lwSRP admission limit follow a false 10 Mb/s.
    - LINK_UP/LINK_DOWN can never report real link cycles.
  - #599 acceptance 1 is not met on hardware, and merging to dev regresses every image built from it.
  - The simulation and host evidence cannot reveal this, because both peers reproduce the implementation's sampling assumption (AGENTS section 6, Tests: "Tests do not merely reproduce implementation assumptions").
  - The ack guard also offers no protection: a shifted frame yields a confident wrong value, not an error.
- **Required outcome:**
  - The firmware samples PHY-driven bits as clause 22.3.4 requires. Either sample before each rising edge after two turnaround clocks, as the LiteX reader does, or clock one turnaround bit and then sample after each rise, as post-edge readers must.
  - Both committed peers model IEEE output timing: after rising edge k the PHY presents bit k+1.
  - A committed control fails when the one-bit phase error is planted.
  - The simulation claims in `397_SERVICE_BUDGET.md` and `BAREMETAL_FIRMWARE.md` are re-established against the corrected peer.
- **Verification:**
  - `probe_mdio_phase.py <repo> <work>` prints `firmware_reader` equal to the true value, and `link_status=13`, under `PHASE=1`.
  - `test_phy_firmware.py` and the service harness pass with IEEE-timed peers and kill a phase-shift mutant.
  - The #599 bench lane then confirms on silicon.

### F2 - MINOR - Conformance, Tests, Docs - queued BIOS built-in commands still get no dispatch opportunity

- **Where:**
  - Ticks exist only at the entry of the five Milan-registered handlers (`milan_baremetal.c:1635`, `:1737`, `:1770`, `:1781`, `:1802`).
  - The harness excludes built-ins (`tb/verilator/fw_service_budget/run.py:23`, "BIOS maintenance is separate"), and the queued plans use only Milan commands.
  - Docs: `docs/integration/BAREMETAL_FIRMWARE.md:1896-1897`, `docs/findings/397_SERVICE_BUDGET.md:170`.
- **Authority:**
  - #590 acceptance 1: "A heartbeat tick opportunity at each console command dispatch".
  - Decision: "An operator pasting commands must never lapse the saved-state liveness."
  - The #590 body records that the BIOS runs the idle hook only while no UART byte is pending.
  - AGENTS section 2: an Issue/implementation interpretation conflict is published for decision, not chosen privately.
- **Evidence:**
  - BIOS built-in handlers are outside this translation unit, and there is no dispatch hook.
  - A pasted run of built-in commands therefore has no heartbeat opportunity until input drains.
  - The implementation narrows "each console command dispatch" to "each registered Milan command". That narrowing appears only as a description in the docs. It was not published as an interpretation or limitation, and no decision records it.
  - I did not measure a built-in queue on the product CPU.
- **Impact:** the #590 defect class remains reachable through console paste of built-ins, for example repeated long-output commands. The documentation does not warn the operator.
- **Required outcome:** either give BIOS dispatch the same opportunity, or publish the limitation on #590 and have the manager record a decision. Either way, the firmware contract and findings page must state what queued built-ins do to liveness.
- **Verification:** a queued built-in plan keeps continuous backing, or the recorded decision and matching documentation text are published.

### Suggestions (do not affect coverage)

- **S1 (Robustness)** - `milan_baremetal.c:882-890`, `:903-906`.
  - While no PHY acknowledges, discovery clears `phy_last_poll`. Every service opportunity (idle loop, every 256 CRC bytes, every 16 records, every flash poll) then runs an MDIO transaction and republishes link down, replacing the safe reset default indefinitely.
  - A single missed acknowledgement on a found PHY publishes a false down/up pair, which the fabric counters count as a link cycle.
  - Consider holding the last published state on a transaction error, and rate-limiting discovery.
  - `hdl/common/KL_link_guard.sv:39-40` records an Arty variant whose MDIO is unusable; I did not establish whether that applies to current Arty builds.
- **S2 (Tests)** - the byte-only capture control is not self-grading.
  - `tb/verilator/nvm_capture_cpu/run.py` grades `byte-only` with the ordinary oracles, and the README asks for a manual comparison.
  - A regression to the byte path (24.30 ms) would still pass `check_nvm_capture.py` against 24.5 ms.
  - Consider grading the word path's contribution mechanically.
- **S3 (Tests)** - `sw/builder/test_builder.py:13304` uses the literal 4.
  - The proposed fixture patch derived it as twice the product's base selections.
  - The literal is within the authorization, but the next product conditional reopens the same STOP.
- **S4 (Docs)** - `CHANGELOG.md` has no entry for this lane.
  - The new MAC_STATUS publisher, the 13.23262 ms capture receipt and the heartbeat opportunities are not recorded there.
  - The #580 entry's capture lines now describe a replaced receipt.

## What was checked and held (evidence for the assigned verification items)

1. **#590 heartbeat service.**
   - Opportunities:
     - At entry of every Milan handler.
     - In `nvm_crc32` every 256 bytes after `nvm_ready` (`:470-473`).
     - In `nvm_validate` every 16 records (`:634-636`).
     - Between the two wipe slot erases (`:1753-1755`).
     - Existing restore and flash-wait opportunities are retained.
     - None inside the capture copy.
   - The rate limit is unchanged: `NVM_HEARTBEAT_NS` (`:344`) and `nvm_heartbeat_tick` (`:917-930`).
   - Published service JSONs for both shapes, all plans:
     - Empty `service_findings`.
     - 133-byte queued plans with 0 unbacked cycles.
     - Largest heartbeat gap 322.47112 ms.
     - Largest armed no-tick stretch 137.03828 ms (8x8 AEM), below 250 ms.
   - The dispatch-removal control loses backing: 2769.99749 ms gap, "continuous backing lost". It is a committed `--mutation remove-dispatch`, selected by exact handler anchors.
2. **#592 capture copy.**
   - Aligned word load/store is used only when `i` is aligned, at least 4 bytes remain before `next`, and `i <= NVM_AREA_RAW - 4`. Otherwise bytes are copied. No word crosses a record edge (`:1170-1189`).
   - The receipt has 0 mismatches and 0 open-record copies in all 96 rows.
   - The byte-only control measures 24.29666-24.30636 ms against the new 13.23262 ms (previous receipt 24.30246 ms).
   - The skip-copy control replaces both stores.
3. **#599 (outside F1).**
   - The pins match `LiteEthPHYMDIO` (mdc bit 0, oe bit 1, w bit 2). The accessor names match a product `csr.h`.
   - Clause-22 command framing (ST 01, OP 10, 5+5 address bits) is correct.
   - Negotiation resolution follows the priority order: 1000FD, 1000HD, 100FD, 100HD, 10FD, 10HD. The master/slave fault check and forced-mode decoding are correct.
   - The latched-loss commit (`5e8edc868`) is correct given correct register reads: a latched loss publishes 0, then a second BMSR read resolves current state in the same poll, one transaction apart across the 2-FF CDC.
   - `PHY_POLL_NS` is derived from the heartbeat constant, and the 250 ms bound is stated and graded.
   - The host test and both no-publish mutants are killed (`receipts/phy-host-baseline.log`).
4. **Capture receipt.**
   - `product_firmware_sha256` equals the head's `milan_baremetal.c` (`91d6ca57...`).
   - `tree` equals `5e8edc868^{tree}` (`8d017a28...`). No firmware or capture-harness file changes between `5e8edc868` and head.
   - The six `harness_sha256` values equal the head files. The pins are `16be6768`, `5dce647a` and `48ff7a7e`.
   - All six arms have 16 captures. 8x8 at 50 MHz: 13.23262 ms against 24.5 ms. Labelled 100 MHz point: 9.94948 ms.
   - `scripts/check_nvm_capture.py` rc 0 at head, re-run by me.
5. **#397 refresh.**
   - `docs/findings/397_SERVICE_BUDGET.md` states the measured tree (`5e8edc86`).
   - It states that the old 8x8 figures came from `ac18b509` with 100 MHz generated gPTP/lwSRP constants.
   - It gives the new 50 MHz figures.
6. **Builder fixture.** The only `sw/builder` change is `== 2` to `== 4` at `test_builder.py:13304`. The published present and absent builder logs end in PASS with recorded NOT RUN arms.
7. **No RTL or processor change by the lane.**
   - 0 diff lines under `hdl`, `protocol-processor`, `gptp-processor`, `third_party`, `configs` and `sw/litex` between `20aa4eabf` and head.
   - Merge `42f7f4fe7` is resolution-only: its diff against the lane parent has the same stable patch-id as `8bc97021f..20aa4eabf` (`71aec980...`), and there is no remerge conflict.

## Reviewer-owned ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
| --- | --- | --- | --- | --- |
| Conformance | UNCLEAN (F1, F2) | `milan_baremetal.c:790-930,1170-1189,1633-1802` against IEEE 802.3 22.3.4, #590/#592/#599 acceptance and assignment; `probe_mdio_phase.out`; `measurements.json`; service JSONs | R369-1 | `792a57b092efaee8920f344faacb7675c8e163bd` |
| RTL | UNCLEAN (F1: external MDIO clock-edge/interface timing assumption) | `hdl/milan/milan_datapath.sv:2077-2080,2904-2914`, `sw/litex/milan_soc.py:1761-1800`, `LiteEthPHYMDIO` pin map, `phy.py` CDC model, empty lane diff under hdl/processor/configs, merge patch-id | R369-1 | `792a57b092efaee8920f344faacb7675c8e163bd` |
| Robustness | UNCLEAN (F1) | MDIO NAK/absent/latched paths `milan_baremetal.c:873-907`; host peer negative cases; word-copy edge guards; no-tick stretches | R369-1 | `792a57b092efaee8920f344faacb7675c8e163bd` |
| Tests | UNCLEAN (F1, F2) | `phy_host.c`, `phy.hpp`, `test_phy_firmware.py`, `fw_service_budget/run.py` controls, `nvm_capture_cpu/firmware.py` mutations; re-runs: host self-test (5 shapes), service self-test (42 controls), capture gate, CI-scope self-test | R369-1 | `792a57b092efaee8920f344faacb7675c8e163bd` |
| Docs | UNCLEAN (F2) | `BAREMETAL_FIRMWARE.md:63-70,1896-1942`, `397_SERVICE_BUDGET.md`, `REGISTER_MAP.md:405-417`, compliance matrix 7.4.42.2 row, `nvm_capture_cpu/README.md`, `fw_service_budget/README.md`; `docs_check`, `check_doc_paths`, `check_doc_style` rc 0; no added U+2014 | R369-1 | `792a57b092efaee8920f344faacb7675c8e163bd` |

Prior public review findings on PR #609: none existed at this head. The PR has no reviews and no inline comments, and its issue comments are the two review-start notices. Nothing to resolve or retain.

## Receipts (listed in MANIFEST.sha256)

- `probe_mdio_phase.py`, `probe_mdio_phase.c`, `probe_mdio_phase.out`: the F1 probe and its output.
- `verify_head_bytes.py`, `receipts/verify-head-bytes.log`: the clone's HEAD, tree, index and all 944 file blobs/modes plus 4 gitlinks match the exact head after the probes. The only artifacts my runs created in the clone, bytecode caches, were removed.
- `receipts/host-selftest.log`, `receipts/phy-host-baseline.log`, `receipts/service-selftest.log`, `receipts/ci-scope-selftest.log`.
- `receipts/docs-check.log`, `receipts/check_doc_paths.py.log`, `receipts/check_doc_style.py.log`, `receipts/gen_toc.log` (NOT RUN; see limits).
- `receipts/public-evidence-MANIFEST.json`, `receipts/public-evidence-verify.txt`, `receipts/hosted-checks-snapshot.txt`.

## Real limits

- I did not rebuild or re-run any native product-CPU simulation (service plans, capture arms, target controls). Native figures come from the published receipts and bound logs, whose hashes I verified against head. The scoped Verilator was not used.
- The F1 probe runs on the host with the unchanged firmware translation unit, not on the product CPU. The silicon consequence is inferred from IEEE 802.3 22.3.4 and the LiteX reference reader. It is not bench-measured. Physical calibration NOT RUN; field skips are not hardware proof.
- `gen_toc.py --check` NOT RUN locally: the pinned Markdown renderer is not installed and I made no installs. The author's gate record shows rc 0.
- Builder banks not run (outside my allowance); I relied on the published logs.
- Hosted snapshot at review time: `rtl-fast` SUCCESS, Yosys shards SUCCESS, Verilator shards 1/5 and 4/5 IN_PROGRESS, physical gPTP SKIPPED. Not acceptance evidence.
- F2 is argued from structure; no built-in queue was simulated.

## Pending manager duties

- Route F1 and F2 to the executor. Re-review the corrected head across all five lenses.
- Hosted/act acceptance at the corrected head, and the final current-dev candidate build and merge validation (live dev `c07232228c12b72805dd20e6852bf93f25794da0`).
- The internal review (R368) remains independent. Merge still needs two positive reviews and the full completion bar.
- #599 acceptance 4 (bench switch cycles) after merge, which should also confirm F1's fix on silicon. Post-merge containment.

R369-1 FINISHED
