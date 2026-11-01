# D0 findings: overview and guides

Verified against dev `1e80128f`.
Source lines cite dev `1f29f189`.

## D0-001: README.md:60

- Statement: ADP, ACMP, AECP, MAAP and SRP default to bare-metal firmware.
- Contradicted by: `sw/litex/milan_soc.py` lines 2854-2856 and line 4097: `--ctrl-mailbox` defaults off and the default build carries no mailbox; the same section says all-fabric is the shipping default
- Correction: Say that the Mark II split placement moves ADP, ACMP, AECP, MAAP and SRP into bare-metal firmware, and that the default build keeps all of them in fabric (`sw/litex/milan_soc.py` lines 2854-2856: `--ctrl-mailbox` is off by default and the default build carries no mailbox; line 4097: `store_true`). `REQUIREMENTS.md` is the normative page, so its copy goes to a maintainer decision on what "Mark II default" names, and every copy takes that one answer.

## D0-002: README.md:142

- Statement: clock-source selection now reaches the media plane's wrapper but nothing there
- Contradicted by: `hdl/milan/milan_datapath.sv` lines 734-750: the stored CLOCK_SOURCE is resolved in `media_clk_resolve` and consumed by the INTERNAL, CRF and AAF followers (#74, #629)
- Correction: State that SET_CLOCK_SOURCE selects the followed media clock (INTERNAL, CRF or one AAF input), and link the media-clock following design.

## D0-003: README.md:419

- Statement: Stream restart latency after an ACMP rebind (2026-08, OPEN)
- Contradicted by: #75 is closed; the measurement is `docs/findings/75_RECONNECT_RESTART_MEASUREMENT.md`; the roadmap figure repeats it as open (12 to 90 s)
- Correction: Retire section P1.6 and the roadmap bullet, and point at the #75 finding.

## D0-004: README.md:441

- Statement: **Not the index-bus narrowing** in `KL_lwsrp_ctx.sv`
- Contradicted by: Commit `eff99a9c` (2026-08-13) deleted the fabric SRP context; no `KL_lwsrp_ctx.sv` is tracked, and `JOIN_TIME_MS_C` (line 447) has no definition in the tree
- Correction: Remove the analysis of the deleted module with section P1.6.

## D0-005: README.md:471

- Statement: is **steerability**. `media_tick_p` is a compile-time constant with no
- Contradicted by: `hdl/ieee1722/crf/KL_media_nco.sv` (steerable media grid, 2026-08-10) and `hdl/ieee1722/crf/KL_media_grid_align.sv` (#74) replaced the constant divider
- Correction: Rewrite P1.7 as the current media-clock status (#629, #74) with a link to the media-clock following design, or retire it.

## D0-023: README.md:41

- Statement: | TSN datapath in fabric | MAC · 802.1Qav CBS · gPTP
- Contradicted by: Same as D0-019: CAP.CBS reads 0 and no shaper is instantiated since 0x0056
- Correction: Remove CBS from the shipping datapath row, or mark it as an earlier measurement on an older image.

## D0-046: README.md:348

- Statement: proof (#394)
- Contradicted by: #394 closed on 2026-09-29; the one-port link loss and return proof is recorded in `docs/findings/599_394_E1_LINK_CYCLES.md`, and the same figure marks the closed #389 as done
- Correction: Mark the #394 link-loss and return proof done, with a pointer to the finding, as the figure does for #389.

## D0-047: README.md:383

- Statement: open is the write side. See the mandatory gaps in
- Contradicted by: `docs/reference/milan_feature_status.json` `missing_mandatory_aem_operations` is empty and the README's own gated block (lines 136-139) says every mandated operation is served since 0x0002_0054, the setters included (`docs/reference/MILAN_COMPLIANCE_MATRIX.md` rows 5.4.2.5 to 5.4.2.16)
- Correction: Name what is still open instead (the saved-state cold cycles, Auto Connect, the media plane's adoption of the sampling rate) and link the feature ledger.

## D0-026: docs/guides/VERIFICATION_DEVELOPER.md:32

- Statement: Migen scripts lack one aggregate runner.
- Contradicted by: `scripts/run_litex_sims.sh` lines 99-108 (`INVENTORY`) and line 150 (`run_aggregate`) run every standalone Migen simulation as one aggregate and refuse a missing or unlisted member; the page itself names the runner at line 23
- Correction: Say that `scripts/run_litex_sims.sh` is the aggregate runner of the standalone Migen simulations.

## D0-027: docs/guides/VERIFICATION_DEVELOPER.md:49

- Statement: C has no general harness framework.
- Contradicted by: `sw/firmware/gtest/README.md` lines 3-13: the bare-metal control-plane firmware and its saved-state store are unit-tested on the host with GoogleTest and GoogleMock through one shared harness, graded by `sw/firmware/ctrl/test/test_ctrl_firmware.py` and `sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py`
- Correction: Name the shared host harness `sw/firmware/gtest/` for the control-plane firmware's C (`sw/firmware/gtest/README.md` lines 3-13). Call `sw/trace/test_trace_roundtrip.py` the round-trip of the supplied `sw/trace/` producer, and state separately that the shipping image does not link that producer (`sw/firmware/milan_baremetal/Makefile` line 6; D0-048).

## D0-066: docs/guides/VERIFICATION_DEVELOPER.md:25

- Statement: | C with Python | Shipping trace producer |
- Contradicted by: Same as D0-048: `sw/firmware/milan_baremetal/Makefile` line 6 builds `milan_baremetal.o` alone, and nothing outside `sw/trace/` includes `milan_trace.h`, so `sw/trace/test_trace_roundtrip.py` grades the supplied producer and not the shipping image
- Correction: Write "Supplied trace producer", not linked by the shipping image (`sw/firmware/milan_baremetal/Makefile` line 6; `sw/trace/test_trace_roundtrip.py` lines 17-18 compile it on the host; D0-048).

## D0-001: docs/overview/ARCHITECTURE.md:5

- Statement: Mark II defaults ADP, ACMP, AECP, MAAP and SRP to firmware.
- Contradicted by: Copy of the D0-001 statement on `README.md`. `sw/litex/milan_soc.py` lines 2854-2856 and line 4097: `--ctrl-mailbox` defaults off and the default build carries no mailbox; the same section says all-fabric is the shipping default
- Correction: Say that the Mark II split placement moves ADP, ACMP, AECP, MAAP and SRP into bare-metal firmware, and that the default build keeps all of them in fabric (`sw/litex/milan_soc.py` lines 2854-2856: `--ctrl-mailbox` is off by default and the default build carries no mailbox; line 4097: `store_true`). `REQUIREMENTS.md` is the normative page, so its copy goes to a maintainer decision on what "Mark II default" names, and every copy takes that one answer.

## D0-001: docs/overview/FULL_FPGA_SOLUTION.md:5

- Statement: Mark II defaults control protocols to the core through packet mailboxes.
- Contradicted by: Copy of the D0-001 statement on `README.md`. `sw/litex/milan_soc.py` lines 2854-2856 and line 4097: `--ctrl-mailbox` defaults off and the default build carries no mailbox; the same section says all-fabric is the shipping default
- Correction: Say that the Mark II split placement moves ADP, ACMP, AECP, MAAP and SRP into bare-metal firmware, and that the default build keeps all of them in fabric (`sw/litex/milan_soc.py` lines 2854-2856: `--ctrl-mailbox` is off by default and the default build carries no mailbox; line 4097: `store_true`). `REQUIREMENTS.md` is the normative page, so its copy goes to a maintainer decision on what "Mark II default" names, and every copy takes that one answer.

## D0-001: docs/overview/SYSTEM_DOMAIN_MAP.md:5

- Statement: Its default is bare-metal ADP, ACMP, AECP, MAAP and SRP.
- Contradicted by: Copy of the D0-001 statement on `README.md`. `sw/litex/milan_soc.py` lines 2854-2856 and line 4097: `--ctrl-mailbox` defaults off and the default build carries no mailbox; the same section says all-fabric is the shipping default
- Correction: Say that the Mark II split placement moves ADP, ACMP, AECP, MAAP and SRP into bare-metal firmware, and that the default build keeps all of them in fabric (`sw/litex/milan_soc.py` lines 2854-2856: `--ctrl-mailbox` is off by default and the default build carries no mailbox; line 4097: `store_true`). `REQUIREMENTS.md` is the normative page, so its copy goes to a maintainer decision on what "Mark II default" names, and every copy takes that one answer.
