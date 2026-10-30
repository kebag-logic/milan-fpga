# D0 findings: reference

Verified against dev `1e80128f`.

## D0-011: docs/integration/BAREMETAL_FIRMWARE.md:215

- Statement: pending #403, which decides the receive-filter posture
- Contradicted by: #403 closed as completed on 2026-09-26; `sw/litex/boot_policy.py` line 58 generates `MILAN_MAC_CTRL_SET` (bit 3), written at `sw/firmware/milan_baremetal/milan_baremetal.c` line 1808
- Correction: Name the generated `MILAN_MAC_CTRL_SET` word and drop the pending reference.

## D0-012: docs/integration/BAREMETAL_FIRMWARE.md:218

- Statement: `srp.talker_declare_at_reset`, pending #400
- Contradicted by: #400 closed as completed on 2026-09-26; the firmware writes `MILAN_LWSRP_CTRL_RESET | 3u` at `sw/firmware/milan_baremetal/milan_baremetal.c` line 1814
- Correction: Drop the pending reference and state the forced bits as the shipped behaviour.

## D0-013: docs/integration/BAREMETAL_FIRMWARE.md:219

- Statement: block count `MILAN_N_TALKERS` + 1 in `[15:8]`
- Contradicted by: `sw/litex/boot_policy.py` line 56: `MILAN_MAAP_CTRL_BOOT` is `len(stream_outputs) << 8 | 1`, so the extra block exists only when the CRF output is declared
- Correction: Write the generated `MILAN_MAAP_CTRL_BOOT`: one block per declared AAF output, plus one when the CRF output is enabled.

## D0-010: docs/integration/BOARD_PORTING_AX7101.md:110

- Statement: acceptance remains on [#599](https://github.com/kebag-logic/milan-fpga/issues/599).
- Contradicted by: #599 closed as completed on 2026-09-29; the bench result is `docs/findings/599_394_E1_LINK_CYCLES.md`
- Correction: Point at the #599 link-cycle finding instead of an open issue.

## D0-019: docs/reference/FR_NFR.md:173

- Statement: | **FR-QOS-01..03** | **MET** | Classifier + CBS untouched;
- Contradicted by: `docs/reference/EGRESS_QUEUE_MAP.md` lines 3-8 and `hdl/common/csr/milan_csr.sv` lines 1996-2000 (CAP.CBS = 0): since VERSION 0x0056 `milan_datapath` instantiates no classifier or shaper; the same page says so at lines 50 and 228-230
- Correction: Mark FR-QOS-01 and FR-QOS-02 not met in the product (the blocks exist and are verified, but are not instantiated), and keep FR-QOS-03 as the processor's admission ceiling.

## D0-020: docs/reference/FR_NFR.md:277

- Statement: 802.1Q / 802.1Qav  *(already in HW)*
- Contradicted by: Same as D0-019: the classifier and CBS are not instantiated in the shipping datapath
- Correction: Drop the already-in-HW marker, or say the blocks are verified but not instantiated.

## D0-021: docs/reference/MILAN_COMPLIANCE_MATRIX.md:265

- Statement: | 8.6.8.1 | strict priority (non-CBS queues) | fabric | implemented
- Contradicted by: `docs/reference/EGRESS_QUEUE_MAP.md` lines 3-8: `milan_datapath` does not instantiate the shaper since 0x0056; the page describes the shipping image (line 3)
- Correction: Mark the row as verified RTL that is not instantiated in the shipping image.

## D0-022: docs/reference/MILAN_COMPLIANCE_MATRIX.md:266

- Statement: | 8.6.8.2 | credit-based shaper: idleSlope/sendSlope, transmitAllowed
- Contradicted by: Same as D0-021
- Correction: Mark the row as verified RTL that is not instantiated in the shipping image.

## D0-006: docs/reference/REGISTER_MAP.md:1226

- Statement: attribute's 802.1Q 35.2.2.7.4 FourPackedEvents value
- Contradicted by: IEEE 802.1Q-2022 (and 802.1Q-2018) define MSRP FourPackedEvents in 35.2.2.7.2 with Table 35-3; there is no 35.2.2.7.4
- Correction: Cite IEEE 802.1Q 35.2.2.7.2 (Table 35-3).

## D0-007: docs/reference/REGISTER_MAP.md:1286

- Statement: (STREAM_INPUT[0], Milan Table 7-156)
- Contradicted by: Table 7-156 is IEEE 1722.1-2021's STREAM_INPUT counters_valid table; Milan v1.2 lists the Stream Input counters in Table 5.6 (5.3.8.10)
- Correction: Write IEEE 1722.1-2021 Table 7-156 (Milan v1.2 Table 5.6).

## D0-008: docs/reference/REGISTER_MAP.md:199

- Statement: The Milan Table 7-156 stream counters
- Contradicted by: Same as D0-007: Table 7-156 belongs to IEEE 1722.1-2021
- Correction: Write the IEEE 1722.1-2021 Table 7-156 stream counters, in the section description and its Contents entry.

## D0-009: docs/reference/REGISTER_MAP.md:423

- Statement: Bare-metal firmware publishes PHY state into LiteX `milan_mac.link_status`.
- Contradicted by: `sw/firmware/milan_baremetal/milan_baremetal.c` lines 1086-1094: `phy_link_tick()` runs inside `nvm_heartbeat_tick()`, which returns until `nvm_started` (line 1668) is set; a refused record-set shape never sets it
- Correction: Add that publication runs only while the saved-state writer runs; otherwise MAC_STATUS keeps its reset value (link up, 1000 Mb/s, full duplex).

## D0-014: docs/reference/REGISTER_MAP.md:1427

- Statement: | `0x7D4` | `AEMP_CTRL` | W1S / RO |
- Contradicted by: `hdl/common/csr/milan_csr.sv` lines 885-897 (`A_ETH_GUARD` at 0x7D8), 1578 (reset armed), 1731 (write rule), 2389 (readback); the map has no 0x7D8 row, against REQ-CSR-01's acceptance
- Correction: Add `0x7D8 ETH_GUARD`: RW, reset 1 (armed); writing 0x554E4C4B disarms, any other write re-arms; while armed PHY_RESET writes are dropped and LINK_CTRL[1] is masked; the link guard's own recovery is not gated.

## D0-015: docs/reference/REGISTER_MAP.md:419

- Statement: `[0]` phy_reset_n (0 = hold PHY in reset)
- Contradicted by: `hdl/common/csr/milan_csr.sv` line 2692 drives `o_phy_reset_n` and line 1688 drops writes while ETH_GUARD is armed; `sw/litex/milan_soc.py` never connects the datapath's `o_phy_reset_n`; the pin is driven by LiteEth's CRG reset CSR (`sw/litex/patches/0002-liteeth-gmii-tx-clk-invert.patch`, `pads.rst_n` from `self._reset`)
- Correction: Document PHY_RESET as inert in the shipping SoC, and document `milan_mac_phy_crg_reset` (LiteX CSR) as the reset that reaches the PHY for the `--eth-port` the image is built for.

## D0-016: docs/reference/REGISTER_MAP.md:752

- Statement: `[1]` manual mac_reinit (hold MAC sys-side in reset)
- Contradicted by: `hdl/common/csr/milan_csr.sv` lines 1726-1730: while ETH_GUARD is armed a LINK_CTRL write stores bit 1 as 0
- Correction: Add that bit 1 is masked to 0 while ETH_GUARD (0x7D8) is armed.

## D0-017: docs/reference/REGISTER_MAP.md:416

- Statement: | `0x110` | `MAC_STATUS` | RO | – |
- Contradicted by: `sw/litex/milan_soc.py` lines 1893-1907 and 2084-2085: MAC_STATUS is the LiteX `milan_mac_link_status` CSR, reset link up, 1000 Mb/s on GMII (100 on MII), full duplex
- Correction: State the reset value and that the bits follow the PHY only while firmware publishes them (D0-009); point to LINKG_STAT (0x774) and the AVB_INTERFACE LINK_UP/LINK_DOWN counters.

## D0-018: docs/reference/REGISTER_MAP_CLASSES.md:101

- Statement: | `0x7C8–0x7D4` | AEM saved-state write master |
- Contradicted by: `hdl/common/csr/milan_csr.sv` line 897 allocates `A_ETH_GUARD` at 0x7D8, between the 0x7C8-0x7D4 and 0x7DC-0x7E4 rows; the page judges every CSR group
- Correction: Add a 0x7D8 ETH_GUARD row with its production class.
