[R361] NEGATIVE - exact head fddc58e43733afd90d6222e58999e0f416a30df9

Round R361-1 is the external independent review of PR #600 (Refs #394, Refs #387).

- Tree: `fbb9754c086d837643fe580ed7eb903b630b5aad`, one commit on dev `2a2a7bb655e528edc3087c88033cd3a47546feb4`.
- Changed file: only `docs/findings/394_387_E1_SWITCH_CYCLES.md` (+416).
- Result: all five lenses were applied. One MAJOR and three MINOR findings are open, so every lens is unclean.

Reconstructed from public state:

- AGENTS.md, CONTRIBUTING.md and docs/README.md.
- #394: body, owner decisions 5789765478 and 5857769804, assignment 5858215210, TAKEN 5858224404, REVIEW READY 5858459678 and manager note 5858862351.
- #387: body and its decision and ruling comments (5606198212, 5794731090, 5802264260, 5810378282, 5818091077, 5819379503, 5858215380).
- The #75 body and #117 decision 5795898094.
- The base..head diff.
- The published operator packet at `8f983d245a12e18a47ced37904d405b624c7e024:review-evidence/394-387-r1/`.

## Findings

### F1 - MAJOR - Conformance, Tests, Docs - the #387 acceptance 4 PASS is graded against a bound #387 item 2 does not record, and on PHC steps that landed while no stream flowed

- **Where:** `docs/findings/394_387_E1_SWITCH_CYCLES.md:11`, `:159-163`, `:307-309`.
- **Authority:** #387 acceptance 4 requires the time from the step to relocked media "inside the bound recorded in item 2". Item 2 records two things.
  - The step policy, `docs/design/TIME_SYNC.md:76-100`, gives step and slew thresholds only.
  - The media re-base, `docs/design/GM_LOSS_RECOVERY.md:142-157`, makes each step one counted event: one `mr` toggle and one MEDIA_RESET, with licensed streams streaming on (REQ-PTP-08).
  - Neither records a step-to-relocked-media time or a restart bound.
- **Where the page's bound comes from:** the page grades against "one further stream restart" (`:159-161`). That row is `GM_LOSS_RECOVERY.md:99`.
  - It records the #117 GM loss/return bound, owner decision [5795898094](https://github.com/kebag-logic/milan-fpga/issues/117#issuecomment-5795898094).
  - It was added by `0abf147f` in the #117 findings lane, not by #387's item-2 lane (#540).
  - No public decision maps it to #387 acceptance 4. The assignment (5858215210) asked for observations and named no bound.
- **Evidence (`receipts/step_vs_stream.txt`, rc 0):** in all ten cycles, both of these hold:
  - the DUT's CRF talker licence word (0x750) had dropped 7.58 to 20.34 s after OFF;
  - neither direction was streaming when the step happened. The step brackets end 40.05 to 43.05 s after OFF, and the first returning PDUs arrive 43.99 to 52.60 s after OFF.
- **What was actually measured:** the "Step to media" column (7.50 to 12.54 s) is how long the stream took to come back after the outage.
- **What could not be observed:** the item-2 contract for a step, one `mr` toggle and one MEDIA_RESET on a running stream that is never stopped. The page says so itself: toggles inside the wire gap are not counted, and MEDIA_RESET resets at STREAM_START (`:283-299`).
- **Impact:** a PASS on a frozen acceptance criterion rests on a bound chosen in private.
  - It also rests on a quantity that cannot fail for an item-2 re-base defect: a step that toggled `mr` twice, or never, would produce the same table.
  - AGENTS.md section 2 requires such an interpretation conflict to be published as needing a decision.
  - Read as closing #387 acceptance 4, this PASS would close it without the item's measurement.
- **Required outcome:** the #387 verdict row rests on a bound that has been decided in public. Either:
  - a manager or owner decision, cited on the page, rules that the recovery-bound media row is the item-2 bound for acceptance 4 and that a step during a stream outage satisfies it; or
  - the row says item 2 records no step-to-relock time bound, that the re-base contract could not be observed because every step landed while both streams were stopped, and grades it NOT GRADED or NOT MET pending that decision.
  - Either way, the page states the step-while-stopped condition in plain words.
- **Verification:** re-read `:11` and the method paragraph at the corrected head. Check they cite the decision (or the ungraded status) and state the condition that `scripts/step_vs_stream.py` reproduces.

### F2 - MINOR - Docs - the per-cycle table does not render on GitHub

- **Where:** `docs/findings/394_387_E1_SWITCH_CYCLES.md:209-210`.
- **Evidence:** the header row has 9 cells and the delimiter row has 10. GFM recognizes a table only when those counts match.
  - With the repository's pinned renderer (`tools/markdown/requirements.txt`, in an isolated environment), the page renders 5 tables out of 6 table blocks. Lines 209-220 come out as one paragraph of pipe text.
  - Failing run: `receipts/render_tables.txt` (rc 1) and `receipts/render_percycle_excerpt.txt`.
  - Control: the same page with a 9-cell delimiter renders all 6 tables (`receipts/render_tables_control.txt`, rc 0).
  - `docs_check`, `gen_toc --check/--verify-anchors`, `check_doc_style`, `check_em_dash` and `check_doc_paths` all return 0 at the head and do not catch this (`receipts/doc_gates.txt`).
- **Impact:** the assignment's central artifact, "one per-cycle table", cannot be read on GitHub.
- **Required outcome:** a nine-cell delimiter row. The packet's generator (`tools/report.py`) carries the same row, so fix it there too if the page is regenerated.
- **Verification:** `scripts/render_tables.py <page>` returns 0.

### F3 - MINOR - Conformance, RTL, Robustness, Tests, Docs - the link-counter explanation is incomplete and does not say that no DUT PHY link drop was observed

- **Where:** `docs/findings/394_387_E1_SWITCH_CYCLES.md:165-169`, `:244-260`.
- **Evidence:** receipts are in `receipts/link_counter_path.txt`.
  - **The cause is misstated.** `:252-256` reads: "This run never wrote that status to manufacture edges".
    - The product fact is that nothing in the bare-metal build writes `link_status` (`sw/litex/milan_soc.py:1782-1797`; no writer in `sw/` or `hdl/`).
    - Its reset value (link 1, speed 2, duplex 1) is exactly the `0x0d` the run read.
    - That is the #599 defect, not something the operator chose. The page does not cite #599.
  - **The counters have a second input the page omits.** LINK_UP/LINK_DOWN count edges of `eff_link_w` (`hdl/milan/milan_datapath.sv:3472-3494`). That signal is the AND of three inputs:
    - `i_link_up`, the unwritten CSR;
    - `LINK_CTRL[0]`, which resets to 1;
    - the link guard's `rx_alive`, unless the guard is disabled (`milan_datapath.sv:2904-2905`; `hdl/common/KL_link_guard.sv:36-39`, `:320`). The guard is a hardware link signal that does not depend on software.
  - **That input was not sampled.** The console read `0x110`, `0x720`, `0x750`, `0x764`, `0x780` and `0x8F8`, but not `LINKG_STAT` (`0x774`) or `LINK_CTRL` (`0x71C`).
    - So the run cannot say whether the e1 RX clock ever stopped.
    - The #117 page (`:340`) recorded `LINKG_STAT` with both clocks alive during the outage.
  - **No DUT PHY link loss was observed.**
    - MAC_STATUS is the CSR nothing writes, and MDIO was not read.
    - The tap recorded no frame in either direction from about 1.5-2.2 s to 38.3-40.6 s after OFF. That fits a PHY drop but does not prove one.
    - #117 Observation 8 (`:501`) says "whether the DUT's PHY link dropped is not recorded".
  - **The wording implies more than was seen.** "defect" (`:260`) and "The link-counter failure reproduced" (`:244`) read as a counter that missed an edge the run saw.
  - **Relevant evidence is left out.** The reference peer's own AVB_INTERFACE LINK_UP/LINK_DOWN also stayed 1/0 (+0/+0) in all ten cycles (`peer:counter-9-0` in every `analysis.json`), as in #117 Observation 8.
- **Impact:** the #394 FAIL verdict is correct: the expected increments are missing whatever the cause.
  - But the durable record gives the cause as one CSR, and the #599 re-run inherits that framing.
  - Publishing the PHY state moves the counters only if the DUT PHY link actually drops, and this run did not establish that it does.
- **Required outcome:** the counter paragraph states four things:
  - (a) no bare-metal path publishes the PHY state, so `i_link_up` / MAC_STATUS[0] stays at reset (#599);
  - (b) the counters' other input, the link guard's RX-clock-alive veto, was not sampled;
  - (c) no DUT PHY link loss was observed, so the run cannot tell "link dropped but not counted" from "link did not drop at the DUT PHY";
  - (d) the reference peer's counters were also flat.
  - "defect" is then attributed to #599, not to an observed missed edge.
- **Verification:** re-read the page against `milan_datapath.sv:2904-2914` and `:3472-3494` and against the packet's `peer:counter-9-0` deltas.

### F4 - MINOR - Docs - the raw-evidence locator paragraph points to a volatile path and a private folder name, and its manifest claim does not hold for the published packet

- **Where:** `docs/findings/394_387_E1_SWITCH_CYCLES.md:341-351`.
- **Known correction:** `:345` names the volatile local path `/tmp/a375/cycleNN/`. The raw captures are now in private cold storage, which the PR body says and the page contradicts.
- **Also:**
  - `:343` "identified as `2026-09-23/394-a375`" is a private working-folder name that no cold reader can resolve. The public packet is branch `394-387-review-evidence`, commit `8f983d245a12e18a47ced37904d405b624c7e024`, path `review-evidence/394-387-r1/`.
  - `:347` says each cycle's `raw-artifacts.json` "lists paths". The paths listed are those same `/tmp` paths: 117 of 119 under `/tmp/a375`, 2 at `/tmp/a375-census-*` (`receipts/check_hashes.txt`).
  - `:349` says "`MANIFEST.sha256` covers retained packet files". In the published packet, 13 of its 163 entries fail verification (`receipts/packet_manifest_check.txt`).
    - 12 are publisher path redactions recorded in `MANIFEST.json`.
    - `PR-BODY.md` changed after the manifest was written (`5c71a3d7...` to `7407cd57...`), but `MANIFEST.json` records it as unmodified.
- **Impact:** a cold reader cannot find the packet or the raw index from the page.
- **Required outcome:**
  - The paragraph points to the public packet (branch, commit, path).
  - It says the raw captures are in private cold storage, indexed by name, size and SHA-256 in `RAW-ARTIFACTS.json`.
  - No `/tmp` path or private folder name remains.
  - The manifest sentence matches what a reader of the published packet can verify.
- **Verification:** `receipts/hygiene_scan.txt` rerun finds no absolute path; the packet link resolves.

### Suggestions (do not affect coverage)

- **S1 - Tests (for the #599 re-run, not this page):** during each outage, sample `LINKG_STAT` (`0x774`), `LINK_CTRL` (`0x71C`) and the e1 PHY's MDIO basic-status link bit. That observes a DUT PHY drop directly, which is the read-only check the manager plans.
- **S2 - Docs:** the "GM return / PHC step" column mixes tap-clock and console-clock times.
  - In cycles 2, 5, 6, 7, 8 and 10 the step bracket opens 0.06 to 0.15 s before the GM return. That is inside the stated 0.15 s half-round-trip bound.
  - One sentence saying the usable bracket starts at the GM return would stop a reader from seeing a step before its cause.

## Verified with no finding (focus items)

- **(1) Identity gate and OUT4 proof.**
  - The page's CRCs, sizes and SHA-256 values match `expected-crc.txt`, `identity-result.txt` and `image-artifacts.json`. The packet `csr.csv` hashes to `92981a36...`.
  - Image source `9e9954e9` is an ancestor of base `2a2a7bb6`, and the difference between them is four documentation and evidence files (`receipts/image_to_base_diff.txt`).
  - e1 pins K18/L16 match `sw/litex/platforms/alinx_ax7101.py:46,70`.
  - The cycle 1 events show only OUT4 going OFF and ON, with the other six outlets ON.
  - During cycle 1, the rest of the proof also holds:
    - no switch gPTP frame on the tap from OFF+5 s until ON;
    - the controller carrier dropped;
    - DUT reset epoch stayed 1, with console gaps ≤0.251 s;
    - the peer's available_index (65863 to 65871) and GPTP_GM_CHANGED (15 to 17) kept counting.
- **(2) Per-cycle numbers.** `scripts/recompute_table.py` recomputes every cell of all ten rows from the packet's `analysis.json` files, plus the summary claims. Result: 0 mismatches (`receipts/recompute_table.txt`). The summary claims covered are:
  - gPTP recovery 0.44-1.82 s, longest step-to-media 12.54 s, first PDUs 5.07-14.00 s after wire return, largest console gap 0.251 s;
  - step sizes -358,781 / -162.46 / -95.74 to -96.47 s, and the intermediate zero caught in 5 of 10 cycles;
  - the counter deltas, MAC_STATUS 13, the servo sequence and post-return `tu=0`.
  - The artifact-hash table's 50 rows match both the per-cycle `raw-artifacts.json` files and `RAW-ARTIFACTS.json` (`receipts/check_hashes.txt`).
  - Timing resolution and cross-host uncertainty are stated and match the analyses: tap half-RTT ≤0.151 s, controller ≤0.074 s, anchor spread ±0.051 s.
- **(3) #394 acceptance 2 FAIL:** correct. The expected LINK_UP/LINK_DOWN increments are absent in all ten cycles (see F3 for the explanation).
  - The page does not claim a DUT PHY link drop in so many words (`:167`).
  - It does leave out the limits F3 lists.
- **(5) #75:** first-PDU times are recorded against the 1 s bound relative to a wire landmark.
  - The page separates this from #75's CONNECT_RX trigger and its 100-cycle experiment (`:177-187`, `:236-240`).
  - It says it does not close #75 (`:15`).
- **(6) Restore:** `scripts/check_restore.py` compares the published start and end census (`receipts/check_restore.txt`):
  - the 18 stream states are unbound at both ends;
  - the 33 clock, configuration, sample-rate and descriptor payloads are byte-equal, including the DUT clock source 0;
  - the outlet censuses are equal, all ON.
  - Final analysis: no CRF PDU in either direction, servo IDLE, epoch 1. Final UART grader 10/10.
- **(7) Hygiene:** the page carries no peer, switch, host, instrument or private-suite name, serial, MAC/EUI or home path (`receipts/hygiene_scan.txt`). The only exception is the locator paragraph (F4).
- **Documentation gates at head (all rc 0, `receipts/doc_gates.txt`):**
  - `docs_check.py`, `check_doc_style.py`;
  - `gen_toc.py --check` and `--verify-anchors`;
  - `check_em_dash.py --base 2a2a7bb6`, `check_doc_paths.py`, `git diff --check`.

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1 MAJOR, F3 MINOR) | #394 acc 2 + decision 5857769804; #387 acc 4 vs item 2 (`TIME_SYNC.md:76-100`, `GM_LOSS_RECOVERY.md:88-157`); #117 decision 5795898094; #75 body; page `:8-15`, `:155-187`, `:242-309` | R361-1 | fddc58e43733afd90d6222e58999e0f416a30df9 |
| RTL | UNCLEAN (F3 MINOR) | `sw/litex/milan_soc.py:1761-1811,1966-1978`; `hdl/milan/milan_datapath.sv:2885-2914,3430-3494`; `hdl/common/KL_link_guard.sv:1-80,320`; `REGISTER_MAP.md:405,734-736`; page `:165-169`, `:252-256` | R361-1 | fddc58e43733afd90d6222e58999e0f416a30df9 |
| Robustness | UNCLEAN (F3 MINOR) | fault injection's reach at the DUT (tap silence, carrier, `LINKG_STAT` not sampled); recovery without reboot or re-bind, 180 s stop, repeated-cycle behaviour across all ten `analysis.json`; restore census | R361-1 | fddc58e43733afd90d6222e58999e0f416a30df9 |
| Tests | UNCLEAN (F1 MAJOR, F3 MINOR) | packet `tools/analyze.py`, `tools/report.py`; ten `cycleNN/analysis.json`; recomputation `scripts/recompute_table.py`; ordering probe `scripts/step_vs_stream.py`; restore `scripts/check_restore.py` | R361-1 | fddc58e43733afd90d6222e58999e0f416a30df9 |
| Docs | UNCLEAN (F1 MAJOR, F2/F3/F4 MINOR) | whole page `docs/findings/394_387_E1_SWITCH_CYCLES.md:1-416`, rendered with the pinned renderer; doc gates; hash table vs `RAW-ARTIFACTS.json`; #117 page anchors `:66`, `:277`, `:344` | R361-1 | fddc58e43733afd90d6222e58999e0f416a30df9 |

## Prior public review findings

Before this round's own pass, PR #600 carried two review-start notices and no review. Issue #394 carried no review findings. No prior findings needed resolving or retaining at this head.

## Real limits

- **Raw captures were not available.** The per-cycle `console.jsonl`, `controller.jsonl`, `tap.pcap` and `controller-wire.pcap` are in private cold storage.
  - The table was recomputed from the operator's `analysis.json`, not from the raw captures. Their hashes match the index.
  - Page claims that only the raw files can show were not checked independently. Examples: `:248`, that the valid-mask bits were present in every response, and the per-sample 250 ms cadence.
- **Analyzer dependence.** `analysis.json` is the output of the packet's analyzer (`tools/analyze.py`, which was read). An error inside the raw decoding would carry through into it.
- **No hardware.** No hardware was touched and physical calibration was not run. USB acquisition latency is uncalibrated, as the page states.
- **Banks not re-run.** The manager's full source static/builder and native banks, and the Verilator/Yosys banks, were not re-run: that is outside this round's allowance, and the diff touches no RTL. The scoped Verilator was not needed, and no disposable mutation of the tree was made.
- **Hosted checks at the exact head (`receipts/hosted_checks.tsv`), as fetched:**
  - `docs-check` was still `in_progress`;
  - `rtl-fast`, `docs-check-no-git`, `elaborate`, `wire-accountability` and `full-ci-gate` succeeded;
  - `verilator-suites` and `yosys-portability` were skipped contexts, not executed jobs.
- **Clone integrity after review (`receipts/clone_integrity.txt`):**
  - HEAD and index tree are `fbb9754c...`, and the status is clean;
  - 929 tracked files rehash with 0 mismatches, no mode drift, and no assume-unchanged or skip-worktree flags;
  - the required gitlinks are initialised at their pins: `gptp-processor 5dce647a`, `protocol-processor 870ff88a`, `third_party/verilog-axis 48ff7a7e`.

## Pending manager duties

- Publish this report. F1 needs a public manager or owner decision on the #387 acceptance 4 bound, or a re-scoped verdict.
- Run a correction round for F1-F4, then re-review at the new head.
- Hosted and act acceptance at the exact head, including the in-progress `docs-check`.
- Candidate merge validation against live dev `6d5ebd7357c1e468e446f18a61527c5be6118a04` from source base `2a2a7bb6`.
- The second independent review (the internal round) and merge authorization.
- The #599 re-run of #394 acceptance 2 (see S1).
- Fix the published packet's `MANIFEST.json` record for `PR-BODY.md` (F4).

R361-1 FINISHED
