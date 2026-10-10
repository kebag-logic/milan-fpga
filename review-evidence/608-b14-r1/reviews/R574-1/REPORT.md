[R574] NEGATIVE - exact head 6ec1a3a9a827575a84fb60d42ad3b085ecb70f19

# R574-1: internal independent review of PR #709 (issue #608, lane B14)

- Head `6ec1a3a9a827575a84fb60d42ad3b085ecb70f19`, tree `efa7f95f688d7e3380e0c3b18fa514f6360e803e`, on dev `5603c353137e90c1fa95429f6d00ef7a2298d9ee`.
- Diff: one new file, `docs/findings/B14_BENCH_5603C353.md` (619 lines), in three one-line commits with no trailers (`receipts/commits.txt`).
- Evidence judged: the published packet `review-evidence/608-b14-r1` at commit `c848925d2e88a98e7f31b663e5dd4f342b765487` (2,357 files). Author `MANIFEST.sha256` sha256 `e44c20a5c1c92721dfabe5cf79ee462382437ec049baf745fcd77f56dc194012`; `RAW-ARTIFACTS.json` sha256 `d8bc2a5f229cfd599d03e2429236b9864294de85eb42ecddffc5db670a3a961a`.
- Authorities read:
  - AGENTS.md, CONTRIBUTING.md (section 6, privacy), docs/README.md and docs/findings/README.md.
  - Issue #608: its body, the B14 assignment (6085135051), both STOPs (6088157558, 6093984746) and the ruling (6094000332).
  - Issues #645, #647, #667, #682, #686, #691 and #658, with their acceptance criteria and rulings.
  - `docs/design/MEDIA_CLOCK_FOLLOWING.md` (settle recentre, declared transient), `docs/reference/REGISTER_MAP.md` (0x110, 0x200, 0x6CC-0x6D4, 0x764, 0x8D4, 0x8DC) and `docs/design/MAAP_FABRIC.md` (Annex B contract).
  - The counter engines' headers (`KL_avtp_rx_monitor_ctx.sv`, `KL_talker_diag_ctx.sv`, `KL_avtp_rx_monitor.sv`) and `tests/features/counters_contract_milan.feature`.
  - The prior lane pages (608_75, 629, 667).
  - Clause text: Milan v1.2 Tables 5.4, 5.6 and 5.22 and Sections 5.4.5.1-5.4.5.2; IEEE 1722.1-2021 clause headings 7.4.x and 8.2.x; IEEE 1722-2016 4.4.4.x, 10.4.6, B.2.1, B.3.4.1 and Table B.7.
- Prior public review findings on PR #709 at this head: none. After my own pass I read the PR's reviews and comments: there are no review bodies, and the two PR comments are the manager's review-start notices. Nothing to resolve or retain.

## Verdict basis

The bench work itself is sound. I recomputed every per-cycle and per-start table from the packet: item 2 (30 rows), item 3 (101 rows) and item 4 (100 rows). They match the packet exactly, and planted single-cell edits are caught. The headline grades hold on the evidence:

- #645/#647: 1 to 3 frames slipped before the settle boundary and none after it; no MEDIA_UNLOCKED.
- #608: 100 of 100 stops within one PDU period, with STREAM_START/STOP +1/+1.
- #667: 0 of 100 EARLY or LATE.
- Soak: 0 error-class increments.
- MAAP: ANNOUNCE every 30.505 to 31.405 s, with no overlap.

The NOT RUN items are stated as not run, with their reasons. The reference peer's clock-source deviation is recorded and was restored in both items that changed it. The page names no instrument, product, host, interface or bench address.

The verdict is NEGATIVE on six MINOR defects in what the page records:

- one misreads a Milan clause and points the triage at the wrong counters;
- two state figures that the packet contradicts;
- one overstates the basis of the restore PASS;
- two leave recorded evidence out of the page: a loopback slip, and the packet's identity.

## Findings

### F1 MINOR: the FRAMES observation inverts Milan v1.2 Tables 5.4 and 5.6

- Lenses: Conformance, RTL, Docs.
- Location: `docs/findings/B14_BENCH_5603C353.md:468-471`. Also the PR body's first "Observations for triage" bullet.
- Authority and evidence:
  - The page says the DUT's FRAMES_TX (both talkers) and its CRF listener's FRAMES_RX advance once per second. It then says "Milan v1.2 Table 5.4 and Table 5.6 define these as frame counts, so this needs triage."
  - Milan v1.2 Table 5.4 defines FRAMES_TX as "Incremented at the end of every observation interval during which at least one Stream Data AVTPDU has been transmitted ... shall be less than or equal to 1 second". Table 5.6 defines FRAMES_RX the same way. These are interval counters, not frame counts.
  - The repository declares the same semantics:
    - `docs/reference/REGISTER_MAP.md:955`: FRAMES_TX "advances once per observation interval (1 s)".
    - `hdl/ieee1722/avtp/KL_talker_diag_ctx.sv:28-40`.
    - `hdl/ieee1722/avtp/KL_avtp_rx_monitor_ctx.sv:20-40`: FRAMES_RX is an observation-interval counter, and "the per-frame reading is IEEE 1722.1-2021 Table 7-153's, not Milan's, and serving it read 8000x high at class A".
    - `tests/features/counters_contract_milan.feature:42-53`, the third reading trap.
    - The B13 page already read it this way (`docs/findings/667_TALKER_START_BENCH.md:197-198`).
  - So the three counters that advance once per second are the conformant ones.
  - The counter that departs from Table 5.6, and from the declared AAF engine contract, is the one the page treats as normal. The DUT's AAF listener FRAMES_RX advanced 57,599,387 in 7,200.5 s: about 8,000 per second, one per PDU (`receipts/soak-maap-restore-check.txt`, `dut|5|0`).
- Impact:
  - The findings page makes a wrong clause claim.
  - Triage is pointed at three conformant counters.
  - The AAF listener's per-PDU FRAMES_RX, the real candidate deviation, goes unflagged.
- Required outcome:
  - The observation cites Tables 5.4 and 5.6 as observation-interval counters of at most 1 s.
  - It records the once-per-second FRAMES_TX and CRF FRAMES_RX as matching the clause and the declared engines.
  - It names the AAF listener's per-PDU FRAMES_RX as the observation for triage, against Table 5.6 and `KL_avtp_rx_monitor_ctx.sv:20-40`.
  - The PR body says the same.
- Verification: re-read lines 466-471 and the PR body against Milan v1.2 Tables 5.4 and 5.6 and the soak counter deltas in `author/soak/summary.json`.

### F2 MINOR: the Talker Advertise withdrawal times have the wrong reference

- Lenses: Tests, Docs.
- Location: `docs/findings/B14_BENCH_5603C353.md:190`.
- Authority and evidence:
  - The page says cycles 2 and 42 show the DUT withdrawing its Talker Advertise "0.104 and 0.328 s after the bridge's `Lv`".
  - From each cycle's `msrp.tsv`, the DUT's Talker Advertise `Lv` follows the bridge's Listener `Lv` by 0.0951 s in cycle 2 and 0.3184 s in cycle 42 (`receipts/item3-check.txt`).
  - 0.104 and 0.328 s are the same events measured from the DISCONNECT_RX response (0.0951 + 0.00888 and 0.3184 + 0.00924). That is the analyser's `dut_ta_lv_after_response_s` field.
  - The pilot cycle 1 shows the same withdrawal, 0.039 s after its `Lv`.
- Impact: a recorded time is attributed to the wrong reference event and is about 9 ms off, in the observation the page offers for triage.
- Required outcome: either state 0.095 and 0.318 s after the bridge's `Lv`, or keep 0.104 and 0.328 s and say they are measured from the DISCONNECT_RX response.
- Verification: `scripts/check_item3.py` prints both references from the packet.

### F3 MINOR: the soak capture-loss bursts did not hit all four streams in every capture

- Lenses: Tests, Docs.
- Location: `docs/findings/B14_BENCH_5603C353.md:460-461`.
- Authority and evidence:
  - The page says three captures "each lose a burst ... on all four streams at once: 9 to 12 AAF PDUs and 1 CRF PDU".
  - `author/soak/soak-overlap-recovery.txt` and `soak-wire-aggregate.txt` show that captures 002 and 042 lost PDUs on four streams.
  - Capture 035 lost PDUs on three streams: the port-3 CRF stream lost nothing, and its aggregate counts 2 gaps, not 3 (`receipts/soak-maap-restore-check.txt`).
- Impact: a recorded tap observation disagrees with the packet. The attribution to the capture path still holds, because every missing PDU is recovered from the overlapping capture.
- Required outcome: the sentence matches the packet. For example: "two captures on all four streams and one on three; 9 to 12 AAF PDUs and 1 CRF PDU per affected stream".
- Verification: compare the sentence with `author/soak/soak-overlap-recovery.txt`.

### F4 MINOR: the restore PASS overstates its as-found coverage, and the saved-state content is asserted without a read-back

- Lenses: Conformance, Docs.
- Location: `docs/findings/B14_BENCH_5603C353.md:41` (summary: "44 of 44 inventory rows equal the as-found record"), `:22` and `:550`. Also the PR body's item 8 row.
- Authority and evidence:
  - The packet's as-found record (05:17 to 05:20, `author/item2/setup*/events.jsonl`) has 15 rows: 7 formats, 2 clock sources, 2 DUT maps and 4 listener states. All 15 were equal at item 2's teardown.
  - The 44-row inventory was first read at 06:22, after items 2 to 4 had changed state and restored it. The final 44 rows equal that 06:22 inventory (`author/restore/restore-compare.txt`, `author/HANDOFF.md:441`).
  - The page body says exactly this at lines 541-543, but the summary row and the Contents line say "the as-found record".
  - Line 550 says the saved state's "content restores the as-found clock source and bindings". The console shows only:
    - image sequence 234 to 272, with 38 commits and 0 failed;
    - `dirty=0`;
    - the same 54 records and 3,336 B before and after (`author/restore/console-final.txt`, `author/item2/setup/dut-before.txt`).

    The packet holds no content read-back or digest.
- Impact: the summary overstates the basis of the item 8 PASS, and a residual is stated as fact without evidence. The PASS itself is supported, because the 15 as-found rows cover every item the lane changed.
- Required outcome:
  - The summary, the Contents line and the PR body give the actual basis: 15 of 15 as-found rows equal (05:17 to 05:20), and 44 of 44 equal the 06:22 inventory.
  - Line 550 is either backed by a content read-back or worded as an expectation that was not verified.
- Verification: re-read lines 22, 41 and 541-550 and the PR body against `author/restore/restore-compare.txt` and the item 2 teardown comparison.

### F5 MINOR: the SLIP_LB record omits a slip at the soak's own bind and most of the movement behind the 0x92 residual

- Lenses: RTL, Robustness, Docs.
- Location: `docs/findings/B14_BENCH_5603C353.md:477-483`, `:121-127` and `:551`.
- Authority and evidence (console reads of `0x8D4` in the packet, `receipts/slip-timeline.txt`):
  - `SLIP_LB` read 0 as found, at 05:17 and 05:20. It reads `0x92` at the end: 146 dups, or 73 frames.
  - The page accounts for 25 of those frames: 21 in the switch transients, 3 in the INTERNAL returns and 1 in the soak.
  - It does not record the other 48:
    - 6 frames between the item 2 setup bind and the first switch (0 to 12).
    - 41 frames at INTERNAL between cycles and between runs. For example, the count went from 24 to 60 between runs `cyc01` and `cyc03` (phase before and end values in `author/item2/summary/switches.json`).
    - 1 frame across the soak's own bind: `0x8e` at 06:22:39, before the bind, became `0x90` at 06:23:23, the first soak read.
  - The soak-bind step happened with the peer following the DUT's CRF. That is the configuration the page explains with "a ring near an edge can slip once".
  - The page's mechanism for the soak slip (a bind primes the ring, and no later settle recentre fires at INTERNAL) is the subject of #647: a running stream that is not re-centred at INTERNAL. The bind-time step is direct evidence on it.
- Impact:
  - An undeclared loopback-ring slip in the soak configuration is missing from the record.
  - The triage note reports one slip where that configuration produced two.
  - The `0x92` residual cannot be reconciled from the page.
- Required outcome:
  - The soak observation records the bind-time step.
  - The page states the as-found `SLIP_LB` (0) and accounts for the 73 frames by phase: transients, returns, INTERNAL time between cycles and runs, the setup bind, the soak bind and the soak.
  - No new claim about the cause is required.
- Verification: `scripts/slip_timeline.py` and the phase values in `switches.json`.

### F6 MINOR: the page does not identify its evidence packet

- Lenses: Tests, Docs.
- Location: `docs/findings/B14_BENCH_5603C353.md:601-619`.
- Authority and evidence:
  - `docs/findings/README.md:33-34`: "New findings must describe the exact candidate, measurement boundary, raw artifact identity, conclusion, and owning issue."
  - The Evidence section refers to "the lane's handoff packet" and says the raw captures are "listed by name, size and SHA-256". It gives no packet name, location, manifest digest or raw-index digest.
  - The prior lane pages identify theirs: `667_TALKER_START_BENCH.md:488-499` gives the packet name and receipt hashes, and `608_75_WITHDRAWAL_AND_RESTART.md:448-460` gives the packet path, branch and capture hashes.
- Impact: a cold reader cannot get from the page to the evidence that grades it. The raw-artifact identity required for new findings is missing.
- Required outcome: the Evidence section identifies the packet. For example: `review-evidence/608-b14-r1`, the author `MANIFEST.sha256` digest `e44c20a5...4012` and the `RAW-ARTIFACTS.json` digest `d8bc2a5f...961a`. It may also give each capture group's total with its index digest.
- Verification: the cited identifiers resolve to the published packet and its digests.

### RESIDUE (wording only; carried to the residue checklist)

- **R1** (`:35`, `:149`): the assignment's "counted once per switch" measure is labelled NOT OBSERVABLE instead of NOT RUN. Exact fix:
  - Line 149: `So "once per switch" is NOT RUN on this image: no silicon register or poll observes it.`
  - Line 35: replace "NOT OBSERVABLE on silicon" with "NOT RUN (not observable on silicon)".
- **R2** (`:428`): "at the first ATDECC access of the day (05:17 UTC)". The identity gate had already read the DUT over ATDECC at 04:54. Exact fix: "at 05:17 UTC, the first ATDECC read after the identity gate".
- **R3** (`:172`): "It came 57 to 96 ms late in cycles 26, 56 and 97". The values are delays after the response, not lateness. Exact fix: "It crossed the tap 57.5 to 95.7 ms after the response in cycles 26, 56 and 97".

### SUGGESTION

- **S1**: add the page to the current-entries table in `docs/findings/README.md`, as the 608_75 and 629 pages are.
- **S2** (`:430-436`): state that the 4 and 8 mappings equal #658's ruled identity default, clipped to the restored 4-channel input format (rulings 5988293154 and 5988843004). Then #682 acceptance 5 can be read against its rule.

## Per-lens results

### Conformance: UNCLEAN (F1, F4)

Checked and found correct:

- Item 2 against `MEDIA_CLOCK_FOLLOWING.md:1190-1222`: the settle boundary is LOCKED + 4.096 s + 0.5 s; at most 3 frames slip before it and none after it; a stream-to-stream switch slips nothing.
- No MEDIA_UNLOCKED on the DUT's inputs from before each set to the end of its hold. I decoded the GET_COUNTERS payloads from all 130 counter marks (`receipts/item2-counters-check.txt`).
- Item 3 against #608 item 3 and the rulings 5885808887 and 5886425487.
- Item 4 against #667.
- The MAAP announce interval against B.3.4.1 and `MAAP_FABRIC.md:85-89`.
- The unsolicited-counter claim against Milan Table 5.22.
- The clause headings in the page's authorities table.
- The NOT RUN items (#691 RMON counters, MAAP acquisition and DEFEND, the recentre count): each is stated with its reason.

### RTL: UNCLEAN (F1, F5)

Checked and found correct:

- `SLIP_LB` counts 2 per slipped frame, from 2 fed pairs (`REGISTER_MAP.md:1870`; the peer's AAF stream has 4 channels).
- The `RENDER_STAT` rail count never moved in a followed hold (`author/item2/summary/rails.txt`).
- The converged-bit timing is consistent with the #386 at-switch recentre.
- The MAAP registers decode as `REGISTER_MAP.md:1258-1260` defines them.
- `MAC_STATUS` `0x0d` decodes as `:410` defines it.
- An RMON zero means "no valid snapshot" (`:457-482`).

### Robustness: UNCLEAN (F5)

Checked and found correct:

- No malformed MSRPDUs and no tap record reversals.
- In the three late-`Lv` cycles, the stop is graded against the `Lv`.
- The pilot cycle's rc 137 capture is excluded and disclosed.
- The capture-path loss is recovered from the overlapping capture.
- The peer's clock-loop deviation is recorded, and its restore is read back in both items (`author/item3/setup.out`, `restore.out`, item 2 teardown).
- One read-only AECP call in `author/restore/peer-clock-sources.jsonl` failed on its argument (rc 1). It changed nothing, and later reads supersede it.

### Tests: UNCLEAN (F2, F3, F6)

Checked and found correct:

- Packet integrity (`receipts/manifest-check.txt`):
  - 1,933 author-manifest entries match their files.
  - The other 422 are path redactions made at publication; their original and published digests both match the manager's `MANIFEST.json`.
  - 2,356 of 2,356 published hashes match.
- Every table row was recomputed from the packet:
  - Item 4 from the raw first-ten AAF header bytes: 1,000 headers, all with `tv=1` and `tu=0`; first-step histogram 66/26/6/2.
  - EARLY and LATE were 0 at all 800 post-bind polls.
- The analyser's stop rule can fail (`author/tools/an608_b14.py:282-283`).
- Planted edits are caught by all three table checkers (`receipts/planted-controls.txt`).
- Every receipt reproduces byte for byte through `scripts/run_all.sh`.

### Docs: UNCLEAN (F1 to F6; R1 to R3)

Checked and found correct:

- Privacy against CONTRIBUTING section 6: no instrument, vendor, product, host, interface, subnet or USB serial.
  - The serial "AX7101-0001" is the configured identity (`configs/endstation_ax7101_1x1_tdm8.yaml:28`).
  - The MAAP ranges are protocol multicast allocations, which earlier pages also publish.
- All seven documentation gates and `git diff --check` return rc 0 at the head, with the pinned renderer pair (`receipts/doc-gates.txt`).
- Links and anchors resolve.
- The capture totals (1.507 GB, 89.8 MB, 452.5 MB and 25.885 GB) match the raw indexes.

## Reviewer-owned completion ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1, F4) | page items 1-8 and its authorities table; issue #608/#645/#647/#667/#682/#686/#691/#658 acceptance and rulings; Milan v1.2 Tables 5.4, 5.6 and 5.22; 1722-2016 Annex B; MEDIA_CLOCK_FOLLOWING.md settle recentre and declared transient; packet item2/3/4, soak, maap and restore records | R574-1 | 6ec1a3a9a827575a84fb60d42ad3b085ecb70f19 |
| RTL | UNCLEAN (F1, F5) | REGISTER_MAP.md 0x110, 0x200-0x230, 0x6CC-0x6D4, 0x764, 0x8D4 and 0x8DC; KL_avtp_rx_monitor_ctx.sv, KL_talker_diag_ctx.sv and KL_avtp_rx_monitor.sv headers; milan_datapath.sv:3446-3518; 30 console reads of 0x8D4 | R574-1 | 6ec1a3a9a827575a84fb60d42ad3b085ecb70f19 |
| Robustness | UNCLEAN (F5) | item 3 late-`Lv`, pilot, malformed and reversal fields; soak overlap recovery and coverage; deviation and restore records; the failed read-only AECP call | R574-1 | 6ec1a3a9a827575a84fb60d42ad3b085ecb70f19 |
| Tests | UNCLEAN (F2, F3, F6) | packet manifests (2,356 files); item 2/3/4 tables recomputed; raw AAF first-ten headers; 130 item 2 counter marks; the analyser's stop rule; planted controls | R574-1 | 6ec1a3a9a827575a84fb60d42ad3b085ecb70f19 |
| Docs | UNCLEAN (F1-F6; R1-R3) | the page (619 lines), the PR body, docs/findings/README.md, CONTRIBUTING.md section 6, doc gates rc 0 | R574-1 | 6ec1a3a9a827575a84fb60d42ad3b085ecb70f19 |

## Referenced issues: which acceptance items the evidence meets, and which stay open

The PR says Refs, not Closes.

- **#608 (open), item 3: met on this image.**
  - 100 of 100 graded withdrawals stopped within one PDU period of the bridge's `Lv`, and STREAM_STOP counted each stop.
  - No LeaveAll of either party preceded any `Lv`, so the LV-registrar case (processor #134) was not exercised on the bench.
  - The DUT's Talker Advertise withdrawal in cycles 2 and 42 remains an open observation (see F2).
  - Closing the issue is the manager's decision.
- **#645 (open), acceptance 3 (a bench repeat shows no undeclared discontinuity on the followed receive path): met.**
  - Met against the declared transient in 20 of 20 switches, with 60 s holds that run past #645's 44.9 s.
  - The "settle recentre counted once per switch" measure is NOT RUN (R1).
  - Acceptance items 1 and 2 belong to the design lane (PR #672).
- **#647 (open), bench item (B8's INTERNAL to AAF repeat shows the declared behaviour): met for the switches.**
  - The INTERNAL aligner pull-in itself is not exercised.
  - The slips at INTERNAL, at the soak's bind and during the soak, remain open observations (F5).
- **#667 (closed): bench confirmation.**
  - 0 of 100 EARLY or LATE, against B13's 14 of 100.
  - The run had the DUT at INTERNAL rather than at B13's clock source 1. The page discloses this, and the fix sits in the talker's start path, which does not depend on the clock source.
  - Absolute gPTP correlation is NOT RUN.
- **#682 (closed), acceptance 5: met for the withdrawal re-run and the soak.**
  - Soak: 0 error-class increments and no grandmaster or AS path change.
  - Default map read: 4 and 8 mappings, consistent with #658's ruling (S2). A contribution from the saved state is not excluded.
- **#658 (closed).** The map read moved from 1 and 0 mappings to 4 and 8. The as-flashed default after a cold boot was not re-read, because the lane allows no power cycle.
- **#686 (closed), acceptance 4: partly evidenced.**
  - ANNOUNCE coexistence is shown: one 2-address range, intervals of 30.505 to 31.405 s, no overlap and no conflict.
  - Acquisition (PROBE timing) and DEFEND are NOT RUN.
  - "Unchanged" is not compared with an earlier MAAP record.
- **#691 (closed).**
  - Its frozen acceptance items are build and timing items, none of them a bench item.
  - B14's added link check passed: `0x0d` at 27 of 27 reads over the soak.
  - The RX error counters are NOT RUN, because the `STATS_CTRL[0]` write they need is outside the lane's rules.

## Real limits

- Raw captures, the 0.5 s console polls, controller transcripts and the soak's per-poll counter records are outside the published packet. Only their sizes and digests are indexed.
- Some figures rest on the executor's derived summaries in the packet: item 2's tap statistics, item 3's PDU timing, the soak tap totals and the MAAP decodes. I did not re-decode raw captures.
- I checked item 4's headers, the GET_COUNTERS payloads, the MSRP event tables and the console dumps at byte or row level.
- No bench action can be repeated by a reviewer. Physical calibration was not run, and field skips are not hardware proof.
- The documentation gates ran in an existing local Markdown environment. Its cmarkgfm 2025.10.22 and html5lib 1.1 match the lock, but one transitive package (pycparser 3.1) differs from the locked 3.0.
- No RTL build or suite was run. The diff is one Markdown page, and no source bank was run or is claimed.

## Pending manager duties

- Hosted acceptance at the exact head (`receipts/hosted-check-runs.tsv`). At 09:10 UTC:
  - rtl-fast, changes, elaborate, bdd-conformance, wire-accountability, docs-check-no-git and full-ci-gate had succeeded;
  - docs-check was still in progress;
  - verilator-suites, yosys-portability, verilator-lint, yosys-elaboration, firmware-unit and Physical gPTP were skipped contexts, which are not evidence.
- The local replication of the hosted run.
- Candidate-merge validation against live dev `e8454e2751d05b02ee8e5a571857589ab358ab86`.
- Publishing this report.
- Carrying R1 to R3 to the residue checklist.

Clone integrity after review (`receipts/clone-integrity.txt`):

- HEAD and tree are the exact head.
- The index equals the HEAD tree, blob for blob and mode for mode.
- There are no untracked or ignored files.
- Gitlinks: external `efeb541a`, gptp-processor `5dce647a`, protocol-processor `2ad2f845`.

R574-1 FINISHED
