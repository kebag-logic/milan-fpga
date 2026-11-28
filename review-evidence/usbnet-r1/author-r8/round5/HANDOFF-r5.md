Status: STOP — the required 100 Mb/s egress allowance is not proved. ETA: implementation and desk evidence are complete; no defensible completion ETA for the remaining egress proof.

Local candidate: `ddda29e1e28ec5b1a58786a750fd1f21b8f6c0d0` on `1011-usbnet`, clean. Nothing pushed or posted. Bench and flash untouched. Packet finalized 2026-11-27T11:09:37.741684+00:00.

The round-3 work and #1004 `4adfa9dc84f58c1c7ad23d6a64fa019985fe62a1` remain ancestors. The dependency was merged without rewriting its commits. The firmware observer, its 45 plants, the writable LED register and all LED code in the Arty control image are removed. There is no LED polling through the production adapter. A read-only diagnostic state remains.

LD0 retains link/activity indication; LD1 retains FX3 station-record, freshness and bus-alive indication. LD2 is any media-locked stream input or any open output transmit gate. LD3 is internal source selection, or media-clock lock when the selected source is external; a selected stream also requires that input to be media-locked. The two complete predicates register in the 50 MHz datapath clock and each cross through two 80 MHz system-clock stages. RGB outputs use green only at 6.25% PWM duty. Every fabric source, top-level port and synchronizer is traced in [CDC findings](receipts/CDC-FINDINGS.md).

The unchanged PHY owner publishes LD0's existing link level; activity comes from accepted MAC beats. This adds no LED-specific CPU work. The FX3 slave-FIFO attachment remains terminated in this desk image and holds bus-alive low, so LD1 cannot claim a working USB connection until that attachment is integrated. The documented station record and stream interfaces remain the FX3-lane contract.

The comparison head `b646e520eb0c51b5e16ae94cbabf2cb835ef9226` is #1004 `4adfa9dc84f58c1c7ad23d6a64fa019985fe62a1` with only the tsn-c-stack and gptp-processor gitlinks changed to the candidate pins. No other comparison-source change was made. Both builds use these pins:

| Dependency | Pin in both builds |
|---|---|
| tsn-c-stack | `a795471c0abc4e38f7e5146b4e539dd607b6f501` |
| gptp-processor | `3ce71b768a2f6f6a5274c127080146e755d02275` |
| protocol-processor | `801ef2283ec793e35a2590fc6593c90313a64041` |
| lwSRP | `d1bb4f4e5954af6dabe7f210a6bf7adbb76bdd6b` |
| verilog-axis | `48ff7a7e2ef782cf778d47910cf85835c64b1bce` |
| external gitlink | `efeb541ae5fe1e078332d8462dca2fc2d9cb8db5` |

The unused external submodule is not initialized in the comparison worktree; its gitlink matches. The original #1004 r7 census used tsn-c-stack `715589c1` and gptp-processor `1213ac5b`. Its old ELF is not used as an identity claim at the newer pins.

Fresh final-head production builds establish these identities:

| Image | Matching candidate and comparison ELF SHA-256 |
|---|---|
| Arty | `f08cac5b313b85ad48a5835d0c9071b261829d5e0d35d58b3100aa86643265ea` |
| ALINX 1x1 | `286f9c0d6bdc8943e6fa8238c77dd235716611072f0248ece111a672a174ee5e` |
| ALINX 8x8 | `1ca3c0b24fd310aa6c2d38c34f482eef8a98f32b7c996bd57681547463c54e06` |

All six generated control map headers have SHA-256 `5f0c602687dacba302959ebb99763e5922aff8ad19f76e7c7c05919b45a936fa`. [Exact commands and hashes](receipts/product-head-identity.json), [firmware pairs](receipts/firmware/) and [pin/source evidence](receipts/source/pins.json) are retained. The firmware app/platform/loop delta against #1004 is empty. The Arty comparison uses separately generated USB-enabled and USB-disabled CSR inputs; the ALINX comparison uses the same frozen board inputs on both sides. This proves control ELF and map-header identity, not whole ALINX routed-bitstream identity.

The full 147-case census at the matching pins passes across all eight images. No case is excluded. The rule takes the larger measured/r7 maxima, applies its 105% ceiling to 5 us, and selects the first legal row. The installed row is already that fixed point: slice 1250 us, AECP pace 10 ms, queued bound 125 ms, transmit bound 35 ms; retry cold 130 us; poll base 235 us, centisecond 160 us, LINK 190 us, MAAP 165 us and withdrawal 95 us. No new cost installation or hand tuning is required. [Qualification](receipts/qualification/qualification.json), [complete derivation table](receipts/qualification/DERIVATION.md), [merged maxima](receipts/qualification/merged-census.json) and [all 147 trace hashes](receipts/census-traces/manifest.json) are retained.

| Quantity | Qualified value | Unchanged bound |
|---|---:|---:|
| Load | 0.5004771140 | 0.70 |
| ACMP CPU row | 29.77 ms | 30 ms |
| ACMP plus conservative local-merger wait | 29.808075 ms | 30 ms |
| txL | 48.82 ms | 49 ms |
| Last notice | 117.47 ms | 140 ms |
| Longest measured pass | 1.7846875 ms | 2 ms |

#969's existing disposition remains explicit: owed registration observations belong to #977 under the unchanged `kept_grade` conditions. Seven held-egress budget misses remain recorded and checked against their own ledger. Neither is silently excluded or converted into a clean physical timing claim. The CPU row qualification does not prove the separate 1 ms wire-egress allowance.

The production local receiver/mailbox test observes a maximum added wait of 21.3375 us. Its conservative bound is `(2 * 1515 + 16) / 80 MHz = 38.075 us` for a control frame already valid at the byte merger. Network priority at the next boundary prevents two queued local copies from overtaking it. The resulting ACMP row is 29.808075 ms, with 191.925 us margin. Both sources share the same mailbox rings and admission buckets; the test exercises actual admission, full/oversize drops and rate drops. [Mailbox limits and scope](receipts/MAILBOX-WAIT.md) state exactly what is bounded.

All four routes pass Slow/0 C, Slow/85 C, Fast/0 C and Fast/85 C, with zero route errors. Three routes have USB enabled and the fourth is the matched USB-disabled comparison. Whole-image LUT/register/BRAM/DSP costs and every slack appear in [route results](receipts/ROUTES.md). The matched USB delta is +1,987 LUTs, +1,685 registers, +4 block RAM tiles and +0 DSP; both images retain LEDs. The smallest setup/hold margins across the four recipes are 0.158/0.018 ns. All use the identical Arty ELF above. Source and generated-logic equivalence connect the routed heads to the final head; raw differences are retained. The new display crossings are CDC-3 Info, depth 2, ASYNC_REG, in all four reports.

The route reports still contain 20 CDC-1 and five CDC-10 critical findings, plus ten inputs without input delays and 22 outputs without output delays. These are recorded whole-image limitations, not cleared by this work. The temperature pairs use the supplied speed-file models. Passing constrained internal timing is not a board-interface or physical release signoff.

Validation passes 92,755 functional checks, four real SET_CLOCK_SOURCE command cases, and all 72 named planted defects. The command tests exercise the real command handler and join its selected index to fabric predicates with explicit lock levels; they do not simulate the complete processor bus or physical clock acquisition. Existing CBS, shaper and queue regressions pass. CI contract checks and 6,008 self-test arms pass; documentation/port checks and 49 mutation controls pass; RTL lint remains at its existing 89-warning allowance with no new lint-off. Exact commands and final logs are indexed in [receipts](receipts/INDEX.md).

Two inherited repository gate problems remain: six bare-metal documentation wording findings and two stale register-reference artifacts. Both reproduce on the same-pin #1004 comparison. They were not weakened or opportunistically changed. Full repository exhaustive RTL/portability gates, hosted checks, independent review and physical validation are not claimed at this head.

The blocking finding is [the 100 Mb/s egress proof](receipts/EGRESS-FINDING.md). The 123.2 us injected-frame figure is the rounded wire-serialization component; the original path plus composition overhead must fit the remaining 876.8 us inside the unchanged 1 ms allowance. The 0.18 ms spare in txL cannot be borrowed. FR_NFR 3.4.1's published capacity argument assumes a gigabit link. A witness through the production mailbox transmitter accepts 254 minimum records; 253 predecessors alone serialize in 1700.16 us at 100 Mb/s. This refutes that capacity argument at the Arty rate. It does not show that production firmware creates the backlog or that an endpoint deadline has been observed to fail. A tighter reachable-production-traffic, arbitration and complete MAC/PHY serialization proof is required. No owner bound or requirement is relaxed.

All commands ran in the foreground within the assigned CPU unit (weight 200). Physical implementation used only the slot wrapper at priority 19; the shared compiler cache was used. Scratch remained under its 25 GB cap; cleanup and evidence relocation were logged before deletion, with literal absolute paths. Completed traces, checkpoints, firmware and bitstreams are retained in this packet; original trace paths resolve to the same hashed bytes. Final resource evidence is in `receipts/resource-final.json`.

Next action: establish the reachable original egress plus composition bound of at most 876.8 us, then complete the remaining review/gate and board-integration obligations. The present work does not justify a REVIEW READY verdict. The draft uses `Relates to #1011` and `Relates to #1018`, because their board items and slave-FIFO attachment remain open.
