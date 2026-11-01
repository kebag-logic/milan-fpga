# D0 findings: reference

Verified against dev `1e80128f`.
Source lines cite dev `1f29f189`.

## D0-001: REQUIREMENTS.md:27

- Statement: The Mark II default places them on the bare-metal core.
- Contradicted by: Copy of the D0-001 statement on `README.md`. `sw/litex/milan_soc.py` lines 2854-2856 and line 4097: `--ctrl-mailbox` defaults off and the default build carries no mailbox; the same section says all-fabric is the shipping default
- Correction: Say that the Mark II split placement moves ADP, ACMP, AECP, MAAP and SRP into bare-metal firmware, and that the default build keeps all of them in fabric (`sw/litex/milan_soc.py` lines 2854-2856: `--ctrl-mailbox` is off by default and the default build carries no mailbox; line 4097: `store_true`). `REQUIREMENTS.md` is the normative page, so its copy goes to a maintainer decision on what "Mark II default" names, and every copy takes that one answer.

## D0-033: docs/integration/AXIS_CORES_ON_BAREMETAL_SOC.md:23

- Statement: Its default is bare-metal control; all-fabric remains supported.
- Contradicted by: Same as D0-001: `sw/litex/milan_soc.py` lines 2854-2856, `--ctrl-mailbox` defaults off and the default build carries no mailbox; the page's next line says all-fabric is the shipping default
- Correction: Say that the Mark II split placement puts the selected functions in bare-metal firmware and that the default build keeps all five in fabric.

## D0-034: docs/integration/AXIS_CORES_ON_BAREMETAL_SOC.md:18

- Statement: may cross clock domains only with a complete-packet asynchronous FIFO.
- Contradicted by: `sw/litex/milan_soc.py` lines 1553-1583 and 1871-1873: the shipping MAC adapter crosses each direction with a 16-beat buffered `stream.ClockDomainCrossing` (`_AXIS_CDC_DEPTH`, line 1413), not a complete-packet FIFO; the store-and-forward `PacketFIFO` (`tx_sf`, line 1810) is a separate transmit stage in the sys domain, and `configs/endstation_ax7101_1x1_tdm8.yaml` lines 43-44 put the datapath at 50 MHz against a 100 MHz sys clock, so the crossing is live
- Correction: State the shipping crossing: a 16-beat buffered asynchronous FIFO per direction, with a store-and-forward packet FIFO before the MAC core on transmit; say what a port must preserve instead of naming a FIFO type the shipping SoC does not use.

## D0-011: docs/integration/BAREMETAL_FIRMWARE.md:215

- Statement: pending #403, which decides the receive-filter posture
- Contradicted by: #403 closed as completed on 2026-09-26; `sw/litex/boot_policy.py` line 58 generates `MILAN_MAC_CTRL_SET` (bit 3), written at `sw/firmware/milan_baremetal/milan_baremetal.c` line 1827
- Correction: Name the generated `MILAN_MAC_CTRL_SET` word and drop the pending reference.

## D0-012: docs/integration/BAREMETAL_FIRMWARE.md:218

- Statement: `srp.talker_declare_at_reset`, pending #400
- Contradicted by: #400 closed as completed on 2026-09-26; the firmware writes `MILAN_LWSRP_CTRL_RESET | 3u` at `sw/firmware/milan_baremetal/milan_baremetal.c` line 1833
- Correction: Drop the pending reference and state the forced bits as the shipped behaviour.

## D0-013: docs/integration/BAREMETAL_FIRMWARE.md:219

- Statement: block count `MILAN_N_TALKERS` + 1 in `[15:8]`
- Contradicted by: `sw/litex/boot_policy.py` line 56: `MILAN_MAAP_CTRL_BOOT` is `len(stream_outputs) << 8 | 1`, so the extra block exists only when the CRF output is declared
- Correction: Write the generated `MILAN_MAAP_CTRL_BOOT`: one block per declared AAF output, plus one when the CRF output is enabled.

## D0-061: docs/integration/BAREMETAL_FIRMWARE.md:200

- Statement: writes these words in this order and no others
- Contradicted by: `sw/firmware/milan_baremetal/milan_baremetal.c` line 1828: `configure_fabric()` also writes `MILAN_TCAM_CTRL` (0x700) with `MILAN_TCAM_CTRL_BOOT` = 1 (`sw/litex/boot_policy.py` line 59), right after `MAC_CTRL`; the table has no `TCAM_CTRL` row
- Correction: Add the `TCAM_CTRL` (`0x700`) row between `MAC_CTRL` and `AAF_CTRL`: value `MILAN_TCAM_CTRL_BOOT` (1), the existing accept-all posture.

## D0-062: docs/integration/BAREMETAL_FIRMWARE.md:2286

- Statement: record below is the shipping option-on measurement; an elaboration estimate
- Contradicted by: The record below measures commit `1e80a106` (2026-08-19, line 2291): 15,849 of 15,850 slices and +0.033 ns WNS. The shipping route has moved since: the #787 re-pin record in `docs/reference/SUBMODULES.md` lines 511-517 and `docs/design/AREA_BUDGET.md` lines 149-150 gives +0.365 ns WNS with 63 of 15,850 slices free at processor `a9e84b66`, and the resource records live in `docs/design/AREA_BUDGET.md`
- Correction: Call the table the first option-on record (commit `1e80a106`) and point at the current shipping route record instead of naming this one the shipping measurement.

## D0-010: docs/integration/BOARD_PORTING_AX7101.md:110

- Statement: acceptance remains on [#599](https://github.com/kebag-logic/milan-fpga/issues/599).
- Contradicted by: #599 closed as completed on 2026-09-29; the bench result is `docs/findings/599_394_E1_LINK_CYCLES.md`
- Correction: Point at the #599 link-cycle finding instead of an open issue.

## D0-038: docs/integration/BOARD_PORTING_AX7101.md:81

- Statement: `s7ddrphy.A7DDRPHY` + `add_sdram(module=MT41J256M16, l2_cache_size=8192)` behind a new
- Contradicted by: `sw/litex/milan_soc.py` lines 3270-3274: `add_staged_sdram(..., l2_cache_size = 0)` with the comment "The product profile is cacheless end to end"; line 4301 refuses any `--l2-bytes` in the bare-metal profile
- Correction: Write `l2_cache_size=0` and say the product SoC is cacheless.

## D0-039: docs/integration/BOARD_PORTING_AX7101.md:88

- Statement: `./sw/litex/milan_soc.py --full --xlen 64` elaborates and **exports a P&R-ready
- Contradicted by: `sw/litex/milan_soc.py` lines 3963-3966 make `baremetal` the only `--software-profile`, and lines 4298-4300 refuse it unless `--xlen 32`, so the command exits with an argument error instead of elaborating
- Correction: Give the current elaboration command (RV32, the bare-metal profile) or mark section 4 as the dated record of an earlier RV64 build; the Contents entry repeats the same command.

## D0-063: docs/integration/INTEGRATION_GUIDE.md:60

- Statement: The processor answers four Stream Input fields itself.
- Contradicted by: `protocol-processor/hdl/top/protocol_processor_top.sv` lines 3624-3648 (`gsi_answer`, processor pin `a9e84b66`; lines 3573-3585 at `f65c8ff7`): for a Stream Input it writes five fields itself, the page's four and selector 6's `stream_vlan_id` [63:48] from its `bound_vlan_r` (line 3632), and it also masks selectors 0, 2 and 4 while the input is unsettled (lines 3639-3645). `hdl/milan/milan_datapath.sv` lines 6444-6445 say the same of the VLAN
- Correction: Give each Stream Input word and flag its writer. Selector 0: `milan_datapath` writes every flag (`hdl/milan/milan_datapath.sv` lines 6194-6217), and while the input is unsettled the processor clears STREAM_ID_VALID, STREAM_DEST_MAC_VALID and STREAM_VLAN_ID_VALID (`0x52000000`, `protocol-processor/hdl/top/protocol_processor_top.sv` line 3641). Selectors 1 (stream_format) and 3 (msrp_accumulated_latency): `milan_datapath` (lines 6401 and 6421). Selector 2 (stream_id): `milan_datapath` (line 6413), and the processor answers 0 while unsettled (top line 3642). Selector 4: `milan_datapath` writes stream_dest_mac [63:16] (line 6430), and the processor answers 0 there while unsettled (top line 3643); the processor writes msrp_failure_code [15:8] (top line 3628). Selector 5 (msrp_failure_bridge_id) and selector 7 (probing_status, acmp_status): the processor alone, never asked of `milan_datapath` (top lines 3593-3595, 3629, 3633). Selector 6: the processor writes stream_vlan_id [63:48], `bound_vlan_r` when settled and 0 otherwise (top lines 3631-3632); `milan_datapath` writes [47:0] (line 6451). A Stream Output's words pass through from `milan_datapath` unchanged (top line 3626).

## D0-064: docs/integration/INTEGRATION_GUIDE.md:64

- Statement: `milan_datapath` answers every other word and every validity flag.
- Contradicted by: `protocol-processor/hdl/top/protocol_processor_top.sv` lines 3631-3632 replace selector 6's VLAN and lines 3639-3645 clear `0x52000000`, the stream_id and the destination MAC while the input is unsettled, on the answer the wire carries; `hdl/milan/milan_datapath.sv` lines 6048-6053 state that it cannot see probing_status, so the processor applies that rule
- Correction: Say that `milan_datapath` gathers the other words and the flags (`hdl/milan/milan_datapath.sv` lines 6194-6217 and 6392-6456), and that the processor's answer is final for a Stream Input: `protocol-processor/hdl/top/protocol_processor_top.sv` lines 3624-3648 pass the gathered data through, then replace the VLAN and mask the three flags and two identity fields while the input is unsettled, which is probing_status other than PROBING_COMPLETED (line 3621). Keep the gather data as the parent's. D0-063 lists each word.

## D0-065: docs/integration/INTEGRATION_GUIDE.md:65

- Statement: Never add a second source for the processor's four fields.
- Contradicted by: Same as D0-063: the processor owns five Stream Input fields, the VLAN included (`protocol-processor/hdl/top/protocol_processor_top.sv` lines 3631-3632; `hdl/milan/milan_datapath.sv` lines 6444-6445)
- Correction: Name all five: probing_status, acmp_status, msrp_failure_code, msrp_failure_bridge_id and stream_vlan_id (`protocol-processor/hdl/top/protocol_processor_top.sv` lines 3628-3633).

## D0-024: docs/integration/QSPI_FLASHBOOT.md:60

- Statement: was deleted 2026-08-13 with this repository's own AECP/AEM engine, so nothing
- Contradicted by: `sw/firmware/milan_baremetal/milan_baremetal.c` lines 329-331 put saved-state slots A and B in `MILAN_FLASH_JOURNAL_OFFSET`, the `journal` range of `sw/litex/milan_soc.py` line 173; `nvm_commit()` (line 1405) erases, programs and verifies the alternate slot, and `nvm_boot()` (line 1656, called at line 1914) judges both slots at every boot
- Correction: Say that the `journal` range holds the bare-metal firmware's two 64 KiB saved-state slots, written alternately and judged at every boot, which is why a reflash must not erase it; the `user` range stays reserved and unused.

## D0-025: docs/integration/QSPI_FLASHBOOT.md:62

- Statement: the protocol processor's NVM face is answered by a blank-flash responder, so a
- Contradicted by: `hdl/milan/KL_pp_shadow.sv` line 1128 instantiates `KL_nvm_backend` behind the processor's NVM face; `docs/design/SAVED_STATE_MATERIALIZATION.md` line 163 records the binding surviving a cold power cycle on silicon since 2026-09-21 (#70)
- Correction: State that the restore walk reads the saved records back from the journal and that the binding survives a power cycle on silicon (#70); keep separate what is still owed physically: no board cold cycle grades the names or the channel maps yet (`docs/design/SAVED_STATE_MATERIALIZATION.md` lines 15-16 and 23).

## D0-035: docs/integration/QSPI_FLASHBOOT.md:96

- Statement: The AEM copy goes through the BIOS's `copy_image_from_flash_to_ram`, so the
- Contradicted by: `sw/firmware/milan_baremetal/milan_baremetal.c` lines 1860-1892: `load_aem_image()` checks the `AEMI` magic, copies `MILAN_AEM_IMAGE_BYTES` with its own loop and then compares the CRC32 with the compiled-in `MILAN_AEM_IMAGE_CRC32`; nothing under `sw/` calls `copy_image_from_flash_to_ram`
- Correction: Name `load_aem_image()` (`sw/firmware/milan_baremetal/milan_baremetal.c` lines 1860-1892) and its two rejection checks: a bad `AEMI` magic before the copy (lines 1869-1873) and a CRC32 mismatch after it (lines 1877-1883). State that `MILAN_AEM_IMAGE_BYTES` only bounds the copy and the CRC (lines 1874-1878), and that no length is compared or rejected. Keep the consequence: a failed check leaves the entity disabled (lines 1913 and 1915, `entity_advertise()` takes the verdict).

## D0-036: docs/integration/QSPI_FLASHBOOT.md:162

- Statement: reachable with the standard quad read (`READ_1_1_4`, 0x6B). `mode="4x"` drives all four DQ,
- Contradicted by: `sw/litex/milan_soc.py` lines 3287-3302: the AX7101 uses `N25Q128A13(SpiCodes.READ_1_1_1_FAST)` with `add_spi_flash(mode="1x", clk_freq=int(12.5e6))`, because the quad read CRC-failed non-deterministically on silicon (2026-07-08); line 3309 skips the BIOS frequency calibration
- Correction: State the single-lane fast read (0x0B, 1-1-1) at the 12.5 MHz request with `SPIFLASH_SKIP_FREQ_INIT`, and why the quad read was dropped.

## D0-037: docs/integration/QSPI_FLASHBOOT.md:108

- Statement: `ax8x8` and `arty` differ from `ax7101` only in dataplane shape:
- Contradicted by: `sw/litex/build.sh` lines 382-399: `ax8x8` has never produced a bitstream, and `arty` is a retired DUT on another board (datapath 50 MHz, sys 83.333 MHz); `sw/litex/milan_soc.py` lines 3282-3288 give the Arty an S25FL128S on `READ_1_1_1`
- Correction: Say that the named configs share the {bitstream, AEM} manifest, that `ax8x8` differs in dataplane shape and has not been built, and that `arty` is a retired DUT on another board.

## D0-028: docs/reference/EGRESS_QUEUE_MAP.md:38

- Statement: | q3 | gPTP classification target | disabled |
- Contradicted by: `hdl/common/ethernet_packet_pkg.sv` lines 220-221: `GPTP_CLASS = 3'd2` (q2) and `SRB_CLASS = 3'd3` (q3); the reset `CLS_TCQ` word `0x004898C0` (`hdl/common/csr/milan_csr.sv` line 2008) maps TC2 to q3, and the page's own slope table (lines 56-57) agrees
- Correction: Swap the two rows: q3 is class B (disabled until configured) and q2 is the gPTP classification target (disabled).

## D0-019: docs/reference/FR_NFR.md:173

- Statement: | **FR-QOS-01..03** | **MET** | Classifier + CBS untouched;
- Contradicted by: `docs/reference/EGRESS_QUEUE_MAP.md` lines 3-8 and `hdl/common/csr/milan_csr.sv` lines 1996-2000 (CAP.CBS = 0): since VERSION 0x0056 `milan_datapath` instantiates no classifier or shaper; the same page says so at lines 50 and 228-230
- Correction: Mark FR-QOS-01 and FR-QOS-02 not met in the product (the blocks exist and are verified, but are not instantiated), and keep FR-QOS-03 as the processor's admission ceiling.

## D0-020: docs/reference/FR_NFR.md:277

- Statement: 802.1Q / 802.1Qav  *(already in HW)*
- Contradicted by: Same as D0-019: the classifier and CBS are not instantiated in the shipping datapath
- Correction: Drop the already-in-HW marker, or say the blocks are verified but not instantiated.

## D0-056: docs/reference/FR_NFR.md:77

- Statement: Its default is bare-metal control over packet mailboxes.
- Contradicted by: Same as D0-001 and D0-033: `sw/litex/milan_soc.py` lines 2854-2856, `--ctrl-mailbox` defaults off and the default build carries no mailbox; the paragraph's first and fifth lines say all-fabric is the shipping default
- Correction: Say that the Mark II split placement puts the selected functions in bare-metal firmware and that the default build keeps all five in fabric.

## D0-001: docs/reference/FR_NFR.md:322

- Statement: Mark II defaults to firmware
- Contradicted by: Copy of the D0-001 statement on `README.md`. `sw/litex/milan_soc.py` lines 2854-2856 and line 4097: `--ctrl-mailbox` defaults off and the default build carries no mailbox; the same section says all-fabric is the shipping default
- Correction: Say that the Mark II split placement moves ADP, ACMP, AECP, MAAP and SRP into bare-metal firmware, and that the default build keeps all of them in fabric (`sw/litex/milan_soc.py` lines 2854-2856: `--ctrl-mailbox` is off by default and the default build carries no mailbox; line 4097: `store_true`). `REQUIREMENTS.md` is the normative page, so its copy goes to a maintainer decision on what "Mark II default" names, and every copy takes that one answer.

## D0-021: docs/reference/MILAN_COMPLIANCE_MATRIX.md:265

- Statement: | 8.6.8.1 | strict priority (non-CBS queues) | fabric | implemented
- Contradicted by: `docs/reference/EGRESS_QUEUE_MAP.md` lines 3-8: `milan_datapath` does not instantiate the shaper since 0x0056; the page describes the shipping image (line 3)
- Correction: Mark the row as verified RTL that is not instantiated in the shipping image.

## D0-022: docs/reference/MILAN_COMPLIANCE_MATRIX.md:266

- Statement: | 8.6.8.2 | credit-based shaper: idleSlope/sendSlope, transmitAllowed
- Contradicted by: Same as D0-021
- Correction: Mark the row as verified RTL that is not instantiated in the shipping image.

## D0-029: docs/reference/MILAN_COMPLIANCE_MATRIX.md:262

- Statement: | 9.4 / 9.6 | C-TAG TPID 0x8100; TCI = PCP·DEI·VID | fabric | implemented
- Contradicted by: `hdl/milan/milan_datapath.sv` lines 684-694: the classifier the row cites as evidence is not instantiated since VERSION 0x0056; the shipping C-TAG is written by `KL_aaf_packetizer` (`hdl/ieee1722/aaf/KL_aaf_packetizer.sv` line 514) and `KL_crf_tx` (`hdl/ieee1722/crf/KL_crf_tx.sv` line 514) and read by `avtp_stream_parser` (`hdl/ieee1722/avtp/avtp_stream_parser.sv` line 159), all instantiated in `milan_datapath`
- Correction: Cite the instantiated framers and stream parser as the evidence instead of the uninstantiated classifier.

## D0-030: docs/reference/MILAN_COMPLIANCE_MATRIX.md:263

- Statement: | 6.9.3 / 6.9.4 | PCP encoding on transmit; priority regeneration on receive | fabric | implemented
- Contradicted by: `hdl/milan/milan_datapath.sv` lines 684-694: receive priority regeneration is the classifier's (`CLS_PRIO_REGEN`), which `milan_datapath` does not instantiate since VERSION 0x0056; `git grep` finds no instance of `traffic_classifier` outside its own sources
- Correction: Keep the transmit half (AAF and CRF TCI bytes) as implemented and mark receive priority regeneration as verified RTL that is not instantiated in the shipping image.

## D0-031: docs/reference/MILAN_COMPLIANCE_MATRIX.md:264

- Statement: | 8.6.6 + Table 8-4 | queue per traffic class | fabric | implemented
- Contradicted by: Same as D0-030: no per-class queue bank (`traffic_queues`) is instantiated in `milan_datapath`, and `docs/reference/EGRESS_QUEUE_MAP.md` lines 3-8 say so
- Correction: Mark the row as verified RTL that is not instantiated in the shipping image.

## D0-032: docs/reference/MILAN_COMPLIANCE_MATRIX.md:267

- Statement: granted slope drives the class-A queue's idleSlope
- Contradicted by: `hdl/milan/milan_datapath.sv` lines 8583-8589: no shaper reads the slope or the verdict; the granted slope reaches only the `LWSRP_STATUS[9]` and `LWSRP_SLOPE` (0x698) diagnostics
- Correction: Say that the granted slope reaches only the two diagnostics and that no shaper consumes it in the shipping image; keep the TSpec half.

## D0-045: docs/reference/MILAN_COMPLIANCE_MATRIX.md:242

- Statement: | 8.4.2.2 / 8.4.3 | event messages timestamped at the reference plane; general messages never | fabric (`ptp_ts_core/top`) |
- Contradicted by: `hdl/milan/milan_datapath.sv` lines 684-687: the `ptp_ts_top` TX/RX record stampers left the datapath with the retired target (#259); the shipping event timestamps are the gPTP plane's RX-tap stamp and its reconstructed launch (`hdl/milan/milan_datapath.sv` lines 8843-8849, #360; `hdl/ieee8021as/gptp_plane/KL_gptp_txret.sv`)
- Correction: Name the gPTP plane's RX tap and launch reconstruction as the owner and its suites (`tb/verilator/gptp_txts`, `tb/verilator/gptp_shadow`) as the evidence.

## D0-050: docs/reference/PP_DESCRIPTOR_OWNERSHIP.md:119

- Statement: | arty_current | 32 | 5792 | 2 / 1 | 1 / 1 | 16 / 1 | 1 / 2 |
- Contradicted by: `python3 scripts/audit_pp_descriptors.py --output <file>` at this head measures 33 descriptors and 5952 bytes for arty_current, 68/10728 for arty_4x4, 100/15976 for arty_8ch, 42/7512 for ax7101_1x1_tdm8 and 124/19520 for ax7101_8x8; the CLOCK_DOMAIN offsets are 4008, 7120, 10320, 4928 and 12576 (the page's second table says 3920, 6768, 9968, 4840, 11872): the tables predate one INPUT_STREAM clock source per AAF input (#629)
- Correction: Regenerate both measurement tables from the audit receipt at the head the page states.

## D0-051: docs/reference/PP_DESCRIPTOR_OWNERSHIP.md:129

- Statement: All singleton counts are one; CLOCK_SOURCE count is two.
- Contradicted by: The same audit: the CONFIGURATION descriptor counts 3 CLOCK_SOURCEs on arty_current and ax7101_1x1_tdm8, 6 on arty_4x4 and arty_8ch, 10 on ax7101_8x8 (INTERNAL, CRF and one per AAF input, #629; the page's own row L6 at line 91 says so)
- Correction: State the CLOCK_SOURCE count as 2 plus the AAF input count, per configuration.

## D0-052: docs/reference/PP_DESCRIPTOR_OWNERSHIP.md:140

- Statement: Every domain's source list is exactly `[0,1]`.
- Contradicted by: The same audit: the CLOCK_DOMAIN source lists are [0..2] (arty_current, ax7101_1x1_tdm8), [0..5] (arty_4x4, arty_8ch) and [0..9] (ax7101_8x8), with lengths 82, 88 and 96
- Correction: Give the measured source lists and lengths, and the AAF-input entries the CRF-only text omits.

## D0-053: docs/reference/PP_DESCRIPTOR_OWNERSHIP.md:288

- Statement: | arty_current | `0x001BC50AC1000005` | pin |
- Contradicted by: The same audit: the entity_model_id values are 0x001BC50AC1000006 (arty_current, pin), 0x001BC549808B210C (arty_4x4), 0x001BC55491CCAA9B (arty_8ch), 0x001BC5C1935893E1 (ax7101_1x1_tdm8) and 0x001BC5572467AF35 (ax7101_8x8), all five different from the table
- Correction: Regenerate the identity table from the audit receipt, or state the head it was measured at.

## D0-054: docs/reference/PP_DESCRIPTOR_OWNERSHIP.md:308

- Statement: On arty_4x4, image byte 6741 changes; the ID remains unchanged.
- Contradicted by: The same audit's identity probe at this head: the reset_time control changes image byte 7093 and the model ID stays 0x001BC549808B210C (the page's next line quotes 0x001BC557FC6ABBC8); the residue it reproduces (#495) still holds
- Correction: Update the byte offset and the quoted ID from the audit receipt.

## D0-055: docs/reference/PP_DESCRIPTOR_OWNERSHIP.md:246

- Statement: Each accepted; no semantic refusal
- Contradicted by: `python3 scripts/audit_pp_descriptors.py` at this head: the packer probes for L10 (nine rate words, offset 143, count/extent mismatch, one byte short), L6 (source list reversed), L4 (buffer 2125999 ns, 47 formats) and L1, L2, L7, L8, L9 and ADP are all refused, by the processor's default model lint that #661 adopted (processor PR #144; the page's own lines 28 and 183 say so); the table records the earlier audit pin
- Correction: Regenerate the processor rows from the current receipt, or mark the table as the record of the earlier pin and drop the PP60 defence-in-depth sentence that the lint has discharged.

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
- Contradicted by: `sw/litex/milan_soc.py` lines 1958-1972 and 2184-2185: MAC_STATUS is the LiteX `milan_mac_link_status` CSR, reset link up, 1000 Mb/s on GMII (100 on MII), full duplex
- Correction: State the reset value, and that the bits follow the PHY once firmware publishes them: `nvm_boot()` arms the poll (`sw/firmware/milan_baremetal/milan_baremetal.c` line 1671, polled at lines 1099-1102 and 1106), and a CSR identity mismatch returns before it (lines 1900-1903), which leaves the reset value. Point to LINKG_STAT (0x774) and the AVB_INTERFACE LINK_UP/LINK_DOWN counters.

## D0-057: docs/reference/REGISTER_MAP.md:137

- Statement: presentation-time offset is pinned at the Milan 2 ms
- Contradicted by: `docs/reference/REGISTER_MAP.md`'s own 0x0053 note (lines 351-356): SET_STREAM_INFO is served and "the stored offset feeds the framers' transit entries"; `docs/reference/MILAN_COMPLIANCE_MATRIX.md` row 5.3.7.6 / 4.4.2.1: the 2 ms default is settable via SET_STREAM_INFO and the stamp adds the offset as set
- Correction: Say that 2 ms is the default and that SET_STREAM_INFO sets each Stream Output's offset, which the framers apply.

## D0-058: docs/reference/REGISTER_MAP.md:1327

- Statement: **Nothing in this device persists a binding across a power cycle.** The
- Contradicted by: `hdl/milan/KL_pp_shadow.sv` line 1128 instantiates `KL_nvm_backend` behind the processor's NVM face (the blank-flash responder is gone; the page's own `PP_STAT` notes at lines 2390-2406 describe `nvm_backed` and the firmware journal writer); `docs/design/SAVED_STATE_MATERIALIZATION.md` line 163: the binding survives a cold power cycle on silicon since 2026-09-21 (#70)
- Correction: Keep the 0x7A0 port a dead CSR face, and say that bindings persist through the processor's restore walk and `KL_nvm_backend`, pointing at the `PP_NVM_*` and `PP_STAT` rows.

## D0-059: docs/reference/REGISTER_MAP.md:1374

- Statement: is **not met by this build**. The
- Contradicted by: Same as D0-058: the bound state is saved and restored by the processor's walk over `KL_nvm_backend` and the firmware's A/B journal, and survives a cold cycle on silicon (#70); only this retired 0x7B8 ingest face is dead (`hdl/milan/milan_datapath.sv` lines 6709-6710)
- Correction: Say that this CSR face is retired and that Milan v1.2 5.3.8.2 is served by the saved-state store, with the open physical items (#70).

## D0-060: docs/reference/REGISTER_MAP.md:1578

- Statement: and the shipping AX7101 shape is 8
- Contradicted by: `sw/litex/build.sh` line 378: the shipping AX7101 recipe is `endstation_ax7101_1x1_tdm8`, and lines 382-384 say the 8x8 recipe has never produced a bitstream; `configs/generated/endstation_ax7101_1x1_tdm8/gen/adp_shape_defaults.svh` declares 2 talker sources and 2 listener sinks (one AAF stream each way plus CRF)
- Correction: Say the shipping AX7101 (`endstation_ax7101_1x1_tdm8`) is the one-AAF-stream shape and that `endstation_ax7101_8x8.yaml` declares 8 of each.

## D0-018: docs/reference/REGISTER_MAP_CLASSES.md:101

- Statement: | `0x7C8–0x7D4` | AEM saved-state write master |
- Contradicted by: `hdl/common/csr/milan_csr.sv` line 897 allocates `A_ETH_GUARD` at 0x7D8, between the 0x7C8-0x7D4 and 0x7DC-0x7E4 rows; the page judges every CSR group
- Correction: Add a 0x7D8 ETH_GUARD row with its production class.

## D0-040: docs/reference/REGISTER_MAP_CLASSES.md:100

- Statement: **Nothing in this device persists a binding across a power cycle**
- Contradicted by: `docs/design/SAVED_STATE_MATERIALIZATION.md` line 163: the binding survives a cold power cycle on silicon since 2026-09-21 (#70), through `KL_nvm_backend` (`hdl/milan/KL_pp_shadow.sv` line 1128) and the firmware journal writer (`sw/firmware/milan_baremetal/milan_baremetal.c` lines 1405 and 1656); only this retired journal-ingest CSR face is a structural zero (`hdl/milan/milan_datapath.sv` line 6709)
- Correction: Keep the row a structural zero for its CSR face and point at the saved-state store that does persist bindings (`PP_NVM_*`, 0x934-0x93C).

## D0-041: docs/reference/REGISTER_MAP_CLASSES.md:84

- Statement: `S50milan` writes these every boot.
- Contradicted by: `S50milan` was an init script of the retired operating-system image (#259): `scripts/check_baremetal_only.py` line 1625 forbids its init.d path as a target service, and the test benches call its write "the retired S50milan poke" (`tb/verilator/milan_dp/sim_main.cpp` line 464); the bare-metal `configure_fabric()`, called by `milan_init()`, writes the identity and enables (`sw/firmware/milan_baremetal/milan_baremetal.c` lines 1818-1821)
- Correction: Say that the bare-metal firmware writes these words at every boot.

## D0-042: docs/reference/REGISTER_MAP_CLASSES.md:83

- Statement: | `0x4xx` | CBS queue window, classifier map | **needed** | live |
- Contradicted by: `docs/reference/EGRESS_QUEUE_MAP.md` lines 3-12 and `hdl/milan/milan_datapath.sv` lines 684-694: no classifier, queue or shaper is instantiated since VERSION 0x0056, so the 0x4xx words are write-only scratch and `CAP.CBS` reads 0 (`hdl/common/csr/milan_csr.sv` lines 1996-2000)
- Correction: Mark the group write-only scratch with no consumer in the shipping image, and drop "boot software programs it" as production configuration.

## D0-043: docs/reference/REGISTER_MAP_CLASSES.md:109

- Statement: Saved-state restoration remains absent
- Contradicted by: `docs/design/SAVED_STATE_MATERIALIZATION.md` lines 19-23 and 203: since #637 `milan_datapath` writes channel-map records 0x60 and 0x70 and restores them after the D3 walk's COMPLETE terminal
- Correction: Say that the channel maps are saved and restored by the parent (#637), and that their board cold cycle is still owed.

## D0-044: docs/reference/REGISTER_MAP_CLASSES.md:131

- Statement:    persistence remains absent.
- Contradicted by: Same as D0-043 and D0-040: bindings, scalar records and channel maps are written to and restored from the journal
- Correction: Replace with the implemented saved state and what still lacks physical evidence (names and channel maps across a board cold cycle).

## D0-048: docs/reference/TRACE_EVENTS.md:7

- Statement: Every event type the bare-metal end-station can write into its DRAM
- Contradicted by: Nothing outside `sw/trace/` includes `milan_trace.h` or calls `MILAN_TRACE`; `sw/firmware/milan_baremetal/Makefile` line 6 builds `milan_baremetal.o` alone, so the shipping image writes no trace record; `docs/design/TRACE_LOGGING.md` lines 246-250 leave the integration to the board
- Correction: Say the catalogue is the ABI of the producer in `sw/trace/`, which the shipping bare-metal image does not link yet (the text comes from `sw/trace/gen_trace_events.py` line 117).

## D0-049: docs/reference/TRACE_EVENTS.md:262

- Statement: Saved-state journal: 0x7C0 verdict + 0x7C4 SEQ, and the A/B slot decision on the write side.
- Contradicted by: `hdl/milan/milan_datapath.sv` lines 6709-6710 tie `jnl_stat_w` and `jnl_seq_w` (0x7C0, 0x7C4) to zero: the journal-ingest CSR face is a structural zero, and the saved-state verdicts now live in the firmware's slot judgement (`sw/firmware/milan_baremetal/milan_baremetal.c` lines 463-465, 1656-1694)
- Correction: Describe the journal event from the firmware's slot verdicts (`nvm_verdict_a`/`_b`, the chosen slot) instead of the retired CSR pair; the text comes from `sw/trace/milan_trace.yaml`.

## D0-001: docs/traceability/ieee8021q.md:5

- Statement: Its default is bare-metal ADP, ACMP, AECP, MAAP and SRP.
- Contradicted by: Copy of the D0-001 statement on `README.md`. `sw/litex/milan_soc.py` lines 2854-2856 and line 4097: `--ctrl-mailbox` defaults off and the default build carries no mailbox; the same section says all-fabric is the shipping default
- Correction: Say that the Mark II split placement moves ADP, ACMP, AECP, MAAP and SRP into bare-metal firmware, and that the default build keeps all of them in fabric (`sw/litex/milan_soc.py` lines 2854-2856: `--ctrl-mailbox` is off by default and the default build carries no mailbox; line 4097: `store_true`). `REQUIREMENTS.md` is the normative page, so its copy goes to a maintainer decision on what "Mark II default" names, and every copy takes that one answer.
