# D0 findings: overview and guides

Verified against dev `1e80128f`.

## D0-001: README.md:60

- Statement: ADP, ACMP, AECP, MAAP and SRP default to bare-metal firmware.
- Contradicted by: `sw/litex/milan_soc.py` line 2621: `--ctrl-mailbox` defaults off and the default build carries no mailbox; the same section says all-fabric is the shipping default
- Correction: Say that the Mark II split placement moves ADP, ACMP, AECP, MAAP and SRP into bare-metal firmware, and that the default build keeps all of them in fabric.

## D0-002: README.md:141

- Statement: clock-source selection now reaches the media plane's wrapper but nothing there
- Contradicted by: `hdl/milan/milan_datapath.sv` lines 704-720: the stored CLOCK_SOURCE is resolved in `media_clk_resolve` and consumed by the INTERNAL, CRF and AAF followers (#74, #629)
- Correction: State that SET_CLOCK_SOURCE selects the followed media clock (INTERNAL, CRF or one AAF input), and link the media-clock following design.

## D0-003: README.md:418

- Statement: Stream restart latency after an ACMP rebind (2026-08, OPEN)
- Contradicted by: #75 is closed; the measurement is `docs/findings/75_RECONNECT_RESTART_MEASUREMENT.md`; the roadmap figure repeats it as open (12 to 90 s)
- Correction: Retire section P1.6 and the roadmap bullet, and point at the #75 finding.

## D0-004: README.md:440

- Statement: **Not the index-bus narrowing** in `KL_lwsrp_ctx.sv`
- Contradicted by: Commit `eff99a9c` (2026-08-13) deleted the fabric SRP context; no `KL_lwsrp_ctx.sv` is tracked, and `JOIN_TIME_MS_C` (line 447) has no definition in the tree
- Correction: Remove the analysis of the deleted module with section P1.6.

## D0-005: README.md:470

- Statement: is **steerability**. `media_tick_p` is a compile-time constant with no
- Contradicted by: `hdl/ieee1722/crf/KL_media_nco.sv` (steerable media grid, 2026-08-10) and `hdl/ieee1722/crf/KL_media_grid_align.sv` (#74) replaced the constant divider
- Correction: Rewrite P1.7 as the current media-clock status (#629, #74) with a link to the media-clock following design, or retire it.

## D0-023: README.md:41

- Statement: | TSN datapath in fabric | MAC · 802.1Qav CBS · gPTP
- Contradicted by: Same as D0-019: CAP.CBS reads 0 and no shaper is instantiated since 0x0056
- Correction: Remove CBS from the shipping datapath row, or mark it as an earlier measurement on an older image.
