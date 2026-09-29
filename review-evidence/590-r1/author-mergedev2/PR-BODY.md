[A385]

Closes #590
Closes #592
Relates to #599

Queued Milan commands and long validation walks now provide heartbeat opportunities, retaining the 250 ms rate limit. Wipe yields between slot erases. Capture copies use aligned words inside closed records and bytes at their edges. Firmware reads PHY state over MDIO and publishes link, speed and duplex through the existing status CSR; a brief latched loss and its recovery are resolved in the same poll.

All six capture arms pass 16 captures each at processor pin `16be6768` in the current (round-3) receipt. The worst 8x8 interval is 13.23352 ms at 50 MHz, 11.26648 ms under the 24.5 ms limit; the labelled 100 MHz comparison is 9.95464 ms. The word-copy remedy gains 11.06894 ms of margin over the historical 24.30246 ms byte-copy receipt. The receipt binds the measured firmware and processor. Both shapes pass all six service plans with continuous backing and a largest observed heartbeat gap of 322.47884 ms. The derived publication period is at most 250 ms, using a 125 ms eligibility interval plus measured service reserve.

The byte-only control restores the old copy cost. Missing-copy, missing-traffic, missing-publication, delayed-recovery and dispatch-removal controls are detected. Simulation checks actual MAC_STATUS and fabric link counters; both queued plans and the device-wait plan show one down/up cycle per shape.

Round 1: required local gates returned zero at `792a57b092efaee8920f344faacb7675c8e163bd` (the current gate head is in the Round 3 section): both compiler modes of the full builder bank, all-shape host tests including Arty, firmware census, capture receipt, service checks, CI scope, source and documentation checks, and whitespace. The builder's existing physical-utilization calibration remains explicitly unrun because its report is absent; the absent-compiler mode also records its intentional instrument omission. The only builder edit is the authorized fixture count change from 2 to 4.

The physical switch-cycle rerun remains #599 acceptance 4 after merge. Independent review is pending.

## Round 2

Round 2 answers R368-1 and R369-1. Its measurements, controls and gate head supersede the round-1 figures. Round 3 changed the firmware and re-measured; its figures supersede this section's.

**MDIO phase (F1).** The reader now samples PHY output with MDC low before each rising edge, after two turnaround clocks, as the pinned LiteX `libliteeth/mdio.c` reader does (IEEE 802.3 section 22.3.4). Both committed peers launch frame bit k+1 after rising edge k, independently of the reader. The unchanged review phase probe reads BMSR `0x796d` and PHYID1 `0x001c` and publishes `link_status=13` under IEEE timing. A late-sample mutant fails in the host PHY test and in the target service harness.

**Every console dispatch (F2).** `sw/litex/patches/0006-bios-dispatch-hook.patch` adds a weak no-op hook to the pinned BIOS, called after `readline` and before any parsing. Every line reaches it: Milan commands, LiteX built-ins, unknown commands and empty input. The firmware overrides it with one rate-limited heartbeat and PHY opportunity; the per-handler entry ticks are removed as redundant. A new `queued-builtins` plan sends 1051 back-to-back lines (14363 bytes: bounded `mem_read`, empty and unknown lines, then `milan_status`). It passes on both shapes with a service entry for every line and zero unbacked cycles. Emptying the hook loses backing (8238.99363 ms gap). The pinned BIOS line buffer is 128 bytes, so the 133-byte requirement applies to the queue, not to a single line. Long single built-ins such as `mem_test` or large-range `mem_read` remain a documented limitation, in BAREMETAL_FIRMWARE.md and the #397 findings page, for both the 500 ms heartbeat and the 250 ms PHY publication bound.

**Record edge (F3).** The host bench now drives a partial ownership vector. On every shape, including Arty, an open record beside an unaligned closed predecessor must keep its staged bytes while the predecessor's change commits byte-identically. The review edge-crossing mutant (`next - i >= 1u`) fails on all five shapes.

**Suggestions taken.** The byte-only control grades itself: every sample must exceed 1.5 times the matched optimized maximum (measured 1.83666x). The capture README states that the capture SoC compiles the PHY path out.

**Capture re-measure.** The receipt binds firmware SHA-256 `2e715af6bdb4ffce409ab2f913784dbe71e419dda75091eba16fd015093ade1b` and processor pin `16be6768`. All six arms pass sixteen captures with zero byte mismatches and zero open-record copies:

| Shape | CPU MHz | Traffic | Maximum ms |
| --- | --- | --- | --- |
| 1x1 | 50 | on | 3.88578 |
| 1x1 | 50 | off | 3.84214 |
| 8x8 | 50 | on | 13.22872 |
| 8x8 | 50 | off | 13.07044 |
| 8x8 | 100 (labelled comparison) | on | 9.94948 |
| 8x8 | 100 (labelled comparison) | off | 9.94094 |

**#397 service harness.** All twelve positive plans pass with continuous backing on both shapes: `all`, `uart-paced`, `queued-input`, `queued-short`, `queued-builtins` and `device-wait` (3 s erase, 5 ms page WIP). The largest heartbeat gap is 322.45756 ms. Queued and device-wait plans observe one down/up cycle in MAC_STATUS and the fabric link counters. The largest MDIO transaction is 0.12451 ms and the largest complete poll 0.83327 ms. The worst steady-state duty plus UART plus conservative poll charge is 120.53831 ms, so the 125 ms trigger keeps publication within 250 ms. No capture or MDIO STOP condition occurred.

**Gates.** Required local gates return zero at `c64f8cd896a4462bd42c4b90b32861ac7fd35176`:

- the full builder bank in both compiler modes, including the ordered firmware census;
- the all-shape host self-test, Arty included, and the host PHY test;
- the refreshed capture receipt check;
- the service harness self-test and bound-log regrades;
- CI scope, documentation and source checks, and whitespace.

Round 2 makes no builder edit; the lane keeps only the authorized fixture count change from 2 to 4. The physical-utilization calibration stays explicitly unrun because its report is absent. No RTL, processor or configuration file changes. The physical switch-cycle rerun remains #599 acceptance 4 after merge, and independent review is pending.


## Round 3

Round 3 answers R368-2 (N1, N2) and R369-2 (F4, F5, F6), and takes R369-2 S5-S9. Its measurements supersede the round-2 figures above.

**Rejected writers stay silent (N1).** A new startup admission flag in `milan_baremetal.c` is set only after both the CSR identity check and the record-shape check pass. `nvm_heartbeat_tick()` returns before reading time, polling the PHY or writing the heartbeat strobe unless the writer was admitted. So neither the dispatch hook nor any Milan command can arm `nvm_backed` after a shape-mismatch disable or an identity-mismatch return. The retired-writer and tag-mismatch rules are unchanged. A rejected startup therefore also performs no PHY poll. On the identity path the firmware must not touch a foreign fabric; on the shape path the idle service was never installed.

A new host test, `test_disabled_writer.py`, plants each rejected state on every shipped shape, Arty included. It drives each of nine console lines twice: empty input, an unknown command and every Milan command. It requires `hb=0 backed=0 stale=0` immediately and after 2500 ms. Removing the admission guard fails both states. The reviewer's disabled-writer probe, run unchanged, reports `hb=0 backed=0 stale=0` in both states.

**Design authority matches the receipt (N2, F4).** `SAVED_STATE_SNAPSHOT_OWNERSHIP.md` section 18 and section 20 item 6 now state the current receipt: measured commit `26a26e1f`, tree `1ced48e2`, firmware SHA-256 `89c0360ed2eb63566d0413e9c721aee05aae4581f23d3897a1ae853b46a10070`, all six maxima with floor ratios, the 8x8 margin to 24.5 ms, and the margin gained. The pre-word-copy 24.30246 ms figure appears only as the labelled historical value. The receipt's BIOS patch digest is stated as informational provenance.

**Built-in lapse threshold (F5).** BAREMETAL_FIRMWARE.md and the #397 findings page now say that a long built-in body can lapse backing after about 1,750 ms. This is because the 2,000 ms deadline includes up to 250 ms of rate-limit phase before the body starts.

**Capture re-measure.** The firmware changed, so all six arms were re-measured: 96 captures, zero byte mismatches and zero open-record copies.

| Shape | CPU MHz | Traffic | Maximum ms | 49 ms floor ratio |
| --- | --- | --- | --- | --- |
| 1x1 | 50 | on | 3.88779 | 12.6036x |
| 1x1 | 50 | off | 3.84214 | 12.7533x |
| 8x8 | 50 | on | 13.23352 | 3.7027x |
| 8x8 | 50 | off | 13.06923 | 3.7493x |
| 8x8 | 100 (labelled comparison) | on | 9.95464 | 4.9223x |
| 8x8 | 100 (labelled comparison) | off | 9.94094 | 4.9291x |

The contract 8x8 maximum of 13.23352 ms leaves 11.26648 ms to the 24.5 ms limit. It gains 11.06894 ms over the historical 24.30246 ms byte-copy maximum.

**#397 service harness.** All twelve positive plans pass on both shapes with zero unbacked cycles and zero service findings: `all`, `uart-paced`, `queued-input`, `queued-short`, `queued-builtins` and `device-wait`. The largest heartbeat gap is 322.47884 ms. The largest MDIO transaction is 0.12457 ms and the largest complete poll 0.83375 ms. The worst 8x8 duty plus UART plus conservative poll charge is 120.53971 ms, leaving 4.46029 ms of reserve under the 125 ms trigger and the 250 ms publication bound. No capture or MDIO STOP condition occurred.

**Retained native evidence (F6).** The evidence packet keeps the raw logs, JSON receipts, specs and build logs of every native run. Files over 200 KB are gzip-compressed and bound by raw and stored SHA-256 and size. `run.py --regrade` passes on every kept service log at the final head.

- `queued-builtins`, 1x1 and 8x8: 1051 of 1051 lines, each with a dispatch tick; zero unbacked cycles.
- `remove-dispatch` on `queued-builtins`: 1051 named per-line findings, backing lost, 8238.99253 ms gap.
- Target `late-sample`: the named finding "PHY initial gigabit negotiation was not published".
- Byte-only capture: 24.30310 to 24.30446 ms, a 1.83648x slowdown against the 1.5x bound.

**Suggestions taken.**

- S5: patch 0006 now defines a strong `bios_dispatch_hook_required()` that the firmware calls at NVM startup. A BIOS without 0006 fails to link by name. The host test and a replay of the product RV32 BIOS link recipe both show this. The dependency is stated where the hook is introduced.
- S6: the `apply.sh` header lists 0006, and the builder comment counts four patches.
- S7: the `remove-dispatch` verdict requires the named per-line finding, pinned by four new portable controls (47 grading checks).
- S8: the host PHY peer NAKs register 5 after the status and control reads succeed, which kills an ignored-acknowledgement mutant.
- S9: the findings page links the phase probe and explains its N/A rows.

The builder change adds the two S6 comment corrections and gives the gate-35 host fixture a declaration and empty definition of the BIOS marker. The S5 link dependency forces that fixture; no assertion or grading rule changes. There is no RTL, processor or configuration change. The physical switch-cycle rerun remains #599 acceptance 4 after merge, and independent review is pending.

**Gates.** Required local gates return zero at `93262f2512054166ae753eda24d76c99f2ea6714`:

- the full builder bank in both compiler modes, including the ordered firmware census and the gate-35 host link;
- the all-shape host self-test, Arty included, with the disabled-writer, link-guard and PHY mutant controls;
- the capture receipt check and a regrade of all 96 kept capture rows;
- the service harness self-test and bound-log regrades of all 15 kept native runs;
- CI scope, documentation and source checks, and whitespace.

The unchanged reviewer probes (MDIO phase, disabled writer, built-in oracle and edge-crossing mutant) and the product link-guard replay give their expected verdicts at this head. The physical-utilization calibration stays explicitly unrun because its report is absent.

## Merge with dev

Dev `7a7582f03ce5ba7863a90ac342c21be18d90db0b` is merged at `9e3df3edc025f73278894ff021a2011e46e2575e`. The only conflict, in `docs/integration/BAREMETAL_FIRMWARE.md`, keeps both lanes' text unchanged: #610's D3 DR2a debounce clause and retry-policy paragraph, and this PR's runtime, capture and PHY paragraphs. `SAVED_STATE_SNAPSHOT_OWNERSHIP.md` section 18 and section 20 item 6 hold this PR's receipt figures beside #610's D3 text without contradiction. `test_builder.py` merged with no gate collision. The processor pin stays `16be6768`.

`1f039cfe86d5337f5c9b7248696dba1c4bdda67e` rewords two statements this PR falsifies:
- the AX7101 porting page no longer waits for a MAC_STATUS driver;
- the findings index no longer calls the #397 architecture decision open.

At that head, the following return their expected results:
- the full builder bank in both compiler modes, including dev's clock-contract checks;
- the host self-test, the capture receipt check and the kept capture oracles;
- the service self-test, CI scope, documentation and source checks, and whitespace;
- the reviewer probes.

Dev's #596 and #597 changed three inputs that the service builds bind: `KL_pp_shadow.sv`, `milan_datapath.sv` and `milan_soc.py`. At the merge head the harness therefore refused the kept round-3 logs, as designed. All 15 native service runs were re-run at `1f039cfe`, and all 15 regrade there. The capture harness compiles both changed RTL files, so the six capture arms were re-measured as well. So were the byte-only, missing-copy, missing-traffic and missing-publication controls.

Every simulation log is byte-identical to round 3's, and every graded result matches. On both shapes the merge passes the new processor counts as 1, the processor's default. The round-3 figures above therefore hold at the merge head:
- the capture table and receipt;
- the 322.47884 ms largest heartbeat gap;
- the MDIO timings;
- every control verdict.

No file in the tree changed for this re-run.

## Merge with dev `b5c0f69d`

Dev `b5c0f69d5d11f0ec4bc847a2cfdd13e89e199a8a` (#395, #595 and #602) is merged at `9f94b246bc714e76e52a3dab3d4be4cd7bf3ca67`. The processor pin moves to dev's `c951a9ff`.
- **The one conflict**, the findings index, keeps dev's commercial-timing row and this PR's #397 row.
- **The firmware contract, compliance matrix and register map merged cleanly.** Dev's #602 text covers PHC-only re-base and `mr`; this PR's text covers the dispatch hook, the capture copy and MDIO link publication. Neither describes the other.
- **`test_builder.py` merged with no gate collision.** Both builder modes pass, including dev's gate 36b and timing-grade checks.

Two test-fixture commits let the `nvm_cosim` suite run the round-3 firmware again. No firmware or RTL changes.
- `d0203aac9724653ea0fb4a61d28ad2e42e515e74` adds the round-3 admission flag `nvm_started` to the writer-restart model, whose statics refusal had stopped the suite since round 3.
- `4c2a30debb031595b81c5c4bfc53b601a0fec528` gives the suite's host `cosim_host.c` an empty patch-0006 marker `bios_dispatch_hook_required()`. Round 3 gave the builder and host-test fixtures the same stub; the refusal had hidden this link failure.
- At `4c2a30de` the suite passes 465 of 465 checks at both shapes, and each of its 39 mutants is killed by its named check.
- After a restart on a live backend the writer re-attaches and keeps heartbeating for 3 s, so `nvm_boot()` re-arms `nvm_started`. Restarts after refused window loads stay retired.

At `4c2a30de` the following return their expected results:
- the full builder bank in both compiler modes, including dev's gate 36b and timing-grade checks;
- the host self-test, the capture receipt check and the kept capture oracles;
- the service self-test, CI scope, documentation and source checks, and whitespace;
- the reviewer probes.

Dev's #602 RTL, the processor re-pin and `milan_soc.py` change inputs that the service builds bind and that the capture harness compiles. So all 15 native service runs, the six capture arms and the four controls were re-run at `4c2a30de`, and all 15 service runs regrade there. Every simulation log and every graded result is byte-identical to the previous merge head's, and so to round 3's. The #595 change does not alter the generated SoC: only LiteX timestamps and debug information differ, and `bios.bin` is identical. The round-3 capture table, the 322.47884 ms largest heartbeat gap, the MDIO timings and every control verdict therefore hold at the new processor pin.
