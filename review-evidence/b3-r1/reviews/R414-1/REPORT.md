[R414] NEGATIVE - exact head 6dfa64a7506a8660a70d77eaa7c96c5de2886f5d

# R414-1: internal independent review of PR #624 (issue #617 acceptance 4, issue #451 USB Audio capture)

- Head `6dfa64a7506a8660a70d77eaa7c96c5de2886f5d`, tree `1538061a99a88ef7e870dbcc079cc9dbdf0ca16f`, one commit on dev `ec0cc0c1df7d7ab3e25d973958f53f0074393d2c`. The PR adds two findings pages and nothing else (`git diff --stat ec0cc0c1..6dfa64a7`: 2 files, +474).
- Round R414-1. Cleared context. Reconstructed from AGENTS.md, CONTRIBUTING.md, docs/README.md, the #617 issue body and comments (the B3 assignment is 5903384996), the #451 recipe, amendment 5729936674 and owner report 5872564358, the PR body, the diff, and the published packet `review-evidence/b3-r1` at `68e0f45b6313bee8d74f2a92d990ba200b78d518` (branch `b3-review-evidence`).
- Prior public review findings on this PR: none at this head. The only other PR comments are the two manager review-start notices.

## Verdict summary

The measurements hold up.

- The identity gate passes as the assignment specifies it.
- The torn-frame definition is exactly #617's.
- All 62 figures I checked re-derive from the published grading outputs: DIN, DOUT and both USB runs.
- The DIN continuity reading matches the frame-atomic RTL and the INTERNAL beat.
- The USB Audio FAIL is measured correctly, and its attribution away from the DUT follows from the evidence.
- The restore is proven.

**#617 acceptance 4 is met.** Acceptance 1 to 3 landed with merged PR #618 (`9e3ccbfb`), so #617 can be closed by hand after this PR merges. The PR says `Refs #617`, so the merge will not close it.

Three MINOR documentation findings stay open, so the verdict is NEGATIVE:

- the findings index is stale;
- one McASP0 rate figure does not re-derive;
- the evidence packet has no public locator on either page.

None of the three changes a measured verdict.

## Findings

### F1: MINOR (Docs). The findings index has no row for either new page, and its first-light row now states a superseded result

- **Where:** `docs/findings/README.md:11`, and the absence of rows for `617_DIN_FRAME_COHERENCE_BENCH.md` and `451_USB_AUDIO_CAPTURE.md`.
- **Authority and evidence:**
  - AGENTS.md section 7 requires that "authoritative documentation is current". The Docs lens asks that "the PR and Issue contain enough evidence for another cold reviewer".
  - The index calls itself the list of "current hardware findings".
  - After merge, its only #451 row, the first-light row, still reads "DIN frame coherence NOT MET, tracked by #617; continuity check, scope and calibrated items NOT RUN". Nothing points to the `ec0cc0c1` re-run (0 torn frames) or to the USB Audio capture FAIL.
  - Recent bench lanes kept the index current:
    - `335e55c41` indexed the first-light page.
    - PR #622 rewrote the `75_RECONNECT...` row to point at the `13eda870` re-measurements.
  - The executor flagged the gap as an open question. It followed the frozen assignment ("No other doc edits"), so this is not an executor fault. It is the state of the PR.
- **Impact:** a reader entering through the index sees #617's bench item as NOT MET. The #451 USB Audio result and its FAIL cannot be found from the index.
- **Required outcome:** a public manager decision, either of:
  - allow the index edit in this PR: one row per new page, and the first-light row's State pointing to the re-run;
  - or record that index maintenance is deferred, naming the follow-up Issue that owns it.
- **Verification:** read `docs/findings/README.md` at the new head. If it is edited, the docs gates return rc 0.

### F2: MINOR (Docs, Tests). "McASP0 receive 250.7 periods/s" does not re-derive; the published counts give 250.0

- **Where:** `docs/findings/451_USB_AUDIO_CAPTURE.md:126` and `:127`. The packet `author/HANDOFF.md:30` repeats the figure.
- **Evidence:** `receipts/mcasp-rx-rate.txt`, from `scripts/mcasp_rx_rate.py`.
  - The 485c0100 chan1 Edge interrupt counts 192-frame receive periods. It rose by 18,942 across `usb-long` and by 18,957 across `usb-long2`.
  - I bracket each read by the `/proc/uptime` read taken just before it. The before and after logs run the same command, so this is a consistent bracket. The intervals are 75.78 s and 75.83 s, so the rates are 249.96 and 249.99 periods/s. That is 47,992 and 47,999 frames/s: nominal, and consistent with the 47,999.49 Hz frame rate of the #451 recipe.
  - 250.7 comes out only when the before log's closing uptime is paired with the after log's opening uptime: 75.57 s and 75.63 s. That is the shortest interval the two reads allow, so 250.7 is the top of the timing uncertainty, not the measurement.
  - The restart count (Level delta 5 per run) and the as-found 1,252 periods in 5.02 s re-derive exactly.
- **Impact:**
  - The page states a McASP0 rate 0.28% above nominal (48,134 frames/s), which a DUT-clocked TDM link cannot produce.
  - A reader could take it as evidence of a rate fault in the direction the page is using to exonerate.
  - The "full rate" conclusion is unchanged, and is stronger with the correct figure.
- **Required outcome:** the page states the rate from a consistent bracket, for example "250.0 periods/s (18,942 and 18,957 periods in 75.8 s)", or states the bracket explicitly.
- **Verification:** `python3 scripts/mcasp_rx_rate.py` on the two status-log pairs reproduces the stated figure.

### F3: MINOR (Docs). Neither page says where the published evidence packet is

- **Where:** `docs/findings/617_DIN_FRAME_COHERENCE_BENCH.md:250` and `docs/findings/451_USB_AUDIO_CAPTURE.md:210`. Both read: "The lane packet `b3-a453` holds the tools, the per-action evidence and the raw-artifact index".
- **Authority and evidence:**
  - The Docs lens requires evidence a cold reviewer can reconstruct from GitHub and the repository (AGENTS.md sections 2 and 6).
  - `b3-a453` is a lane-private name. The published redacted copy is `review-evidence/b3-r1/author/` on branch `b3-review-evidence` (commit `68e0f45b`). Its tool hashes match the pages.
  - The merged B2 pages set the precedent. They locate their packet by path and branch: `606_FIRST_BIND_MEASUREMENT.md:257` and `:297`, and `608_75_WITHDRAWAL_AND_RESTART.md:450`.
- **Impact:** the raw recordings are not public, so the published grading outputs and tools are the only way to re-derive the counts. A cold reader of the merged page cannot find them.
- **Required outcome:** each page names the published packet location (path and branch), or an equivalent public locator.
- **Verification:** open the named location and check that `grade_617.py` and `grade_usb.py` match the hashes on the pages.

### Suggestions (optional; they do not affect coverage)

- **S1 (Conformance, Docs): identity chain.**
  - VERSION `00020060`, AEM CRC `93742dd2`, ROM CRC `acad92b9` and the entity are identical on `13eda870` and `ec0cc0c1`.
  - The only readback that tells the two images apart is the QSPI payload CRC: `d178f19a` against `d84bce7b`. It shows a different bitstream, not which one.
  - The page states the limit (lines 54-56), and the result itself (0 torn frames against 67.5%) corroborates the #618 RTL.
  - Suggestion: publish the `ec0cc0c1` build's payload CRC32 over 3,825,788 bytes, to close the chain. This is listed under pending manager duties.
- **S2 (Docs): the residuals at `617_DIN_FRAME_COHERENCE_BENCH.md:224`.** Suggest the page state that:
  - The six commits match three STREAM_INPUT 0 bind/unbind pairs, which are the binding records 0x20 to 0x2F. The map edits are never persisted.
  - `nvm_pend`, and with it `PP_STAT` bit 11, is the design's sticky report of a channel-map write, cleared only by reset (`docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md:1289`). So the next lane starts without the durable reading (backed 1, dirty 0, stale 0, pend 0) until a reset.
  - The monotonic counters it inherits changed: SLIP_LB went from 0 to 35,316 dups and 35,080 skips, SLIP_TDM from 333 to 999 dups, and the RENDER_STAT rails from 0 to 692 (`receipts/dut-state-diff.txt`).

  "Every control word read equals the start" (line 216) is accurate for control words, and the NVM facts themselves are stated.
- **S3 (Docs): attribution wording at `451_USB_AUDIO_CAPTURE.md:154-161`.** Suggest the page say that:
  - The McASP0-direct reference is a separate run minutes earlier, not simultaneous.
  - The bridge leg's own McASP0 capture restarts, 5 per run, lie inside the unlocated span.
  - The bench host recorded the gadget's `hw` device directly (packet `runs/usb-long/arecord.log`: card 1 hardware PCM), so no host-side conversion ran. That places the interpolated words on the SoC side, alongside the `-S samplerate` legs.

## Answers to the assigned questions

1. **Identity gate: PASS as specified** (`receipts/identity.txt`, from `scripts/check_identity.py`, independent of the lane's tool).
   - VERSION `00020060`. CRC32 over the AEM (7,352 B) is `93742dd2`, over the ROM (53,344 B) `acad92b9`, and over the QSPI payload (3,825,788 B) `d178f19a`.
   - AECP ENTITY (312 B) and CONFIGURATION (106 B) payloads, minus their 4-byte prefix, are byte-equal to the console's QSPI AEM dumps at 0x01400110 and 0x01400248.
   - Entity `020000fffe000001`, firmware string `2.96.0`. The grader passed 10 of 10.
   - The chain limit is under S1.
2. **#617 acceptance 4: MET.**
   - **Torn-frame definition:** "a frame whose valid words carry more than one ordinal" is #617's "samples from two TDM frames" under the pattern.
   - **Grader probes** (`receipts/grader-probes.txt`, synthetic pcaps through the lane's own `grade_617.py`):
     - The rule counts every first-light tear state: 149,998 of 149,998.
     - It reports a single skipped TDM frame as a +2 step.
     - It counts whole-frame repeats identically in all channels.
     - It does not count a zero/pattern mix like the first-light stop-tail frame. That is irrelevant here: no pattern word lies outside the region (outside-region census: 9,526,486 `ffffff00`, 6,217 zero, 1 other), and the page lists the edge frames.
   - **Counts:** 0 torn of 3,360,036 region frames and 0 of 4,551,624 recorded, re-derived (`receipts/rederive-counts.txt`, 62/62):
     - 758,604 PDUs × 6 = 4,551,624 frames, 0 sequence gaps, 0 header errors;
     - region 45,588 to 3,405,623;
     - pair offsets 0,0,0 in every frame;
     - per channel 3,359,999 +1 steps and 36 repeats, at identical frames in all channels, 93,990 to 93,993 frames apart.
   - **Pattern period:** regenerated independently: SHA-256 `b6a92e97…a97c` (`receipts/pattern-period.txt`).
   - **Continuity against the design:**
     - `KL_chan_map_capture.sv:567-590` publishes whole frames on the last pair's strobe.
     - `:1036-1039` counts a dup when a snapshot finds no fresh frame.
     - `:1067-1078` holds the walk snapshot.
     - So a TDM frame running 10.64 ppm slow repeats one whole frame per 1.958 s beat and counts it once (`TIME_SYNC.md:478`).
     - Bench: 36 repeats in-stream, and SLIP_TDM 391 to 427 dups (+36) with 0 skips across the reads that bracket playback.
     - Across the whole lane SLIP_TDM went 333 to 999 dups in 1,303.4 s. That is 666 = 1,303.4/1.958.
   - **DOUT:** unchanged in kind from first light.
     - 3,360,000 frames, 0 torn, 0 invalid, identity order.
     - 36 beat clusters: 696 repeats and 732 drops, net one drop each, spaced 93,989 to 93,992.
     - 23 underrun clusters: 12 sender, 11 unexplained.
   - **Order:** identity in both directions.
   - **Scope of the change:** RTL scope of `13eda870..ec0cc0c1` confirmed; only PR #618 changes `.sv` files.
3. **#451 USB Audio capture FAIL: measured correctly.**
   - Both runs: 3,600,000 frames (115,200,000 B), 75.116 s and 75.108 s, rc 0, captured on the `hw` device, 0 strict passes.
   - The class sums, rotation counts, low-byte shares (97.4% and 97.7%), silent stretches and joins all re-derive.
   - Probes confirm the classifier. A shift of k words is reported as rot k, and a half-sample interpolation reads as in order with non-zero low bytes.
   - The McASP0-direct recording of the same DUT output is exact: 0 zero, 0 non-pattern and 0 torn words.
   - The attribution away from the DUT follows and is not overstated:
     - The DUT has no rate converter, and it rendered the same stream bit-exact minutes earlier.
     - DUT listener errors and depacketizer drops were 0, and media stayed locked.
     - McASP0 received at the nominal rate.
     - The rotation changes (2,833 and 238) far outnumber the bridge's 5 capture restarts per run.
     - The page declines to separate bridge leg, USB function and host path.
   - One supporting figure is wrong: F2.
4. **Continuity check NOT RUN:** correctly recorded. The recipe and the amendment need a meter on unpowered boards, and the assignment forbade power, instrument and wiring changes. The page claims only signal-pin connectivity from the data, and says the grounds and resistances are not measured.
5. **Restore: proven** (`receipts/restore-census.txt`, from `scripts/check_restore_census.py`).
   - 18 stream states (DUT 2 rx + 2 tx, peer 10 rx + 4 tx), all `conn_count` 0.
   - Both DUT maps: `number_of_mappings` 0.
   - 33 of 33 entries equal, keyed field by field.
   - DUT clock source 0 at 48 kHz.
   - Controller host: PHC frequency 28,062.332153 ppb at start and end, `tx_type 1` / `rx_filter 1` at both, no ptp4l, staging removed.
   - Bridge legs restarted with the byte-identical `alsaloop` lines. The McASP playback XRUN state is as found.
   - **NVM:** commits went 0 to 6, slots 229/230 to 235/236, `pend=1`, `PP_STAT` 0x5b000444 to 0x5b000c44.
     - Per the design, the channel-map writes leave `nvm_pend` set until reset.
     - What matters for the next lane is that the durable reading is unavailable until a reset. No saved-content hazard is visible: `dirty=0`, the last commit was VD_OK, and the maps are never persisted.
     - The page states the facts but not that consequence (S2).
6. **Docs gates:** rc 0 at this head in the pinned Markdown environment (`receipts/docs-gates.txt`).
   - `docs_check`, `check_doc_style`, `gen_toc --check`, `check_em_dash --base ec0cc0c1` (0 findings over 474 added lines), `check_doc_paths`, and `git diff --check`.
   - All 28 relative links and anchors in the two pages resolve (`receipts/anchor-check.txt`).
   - No private host, peer, switch or instrument name, path, address or MAC. The PocketBeagle 2 is named per amendment 5729936674.
   - The findings index needs rows: F1.

## Lens results (clean lenses in the finding format)

- `[R414] PASS Conformance` — `docs/findings/617_DIN_FRAME_COHERENCE_BENCH.md:14-20,102-106,210-228`, `451_USB_AUDIO_CAPTURE.md:15-23,98-127,163-177`, against the #617 body (acceptance 4, torn definition), assignment 5903384996 steps 1-5, the #451 checklist and amendment 5729936674. Packet `runs/*/grade*.json`, `pairs.json`, `decode.json`, `attribution.json`, `identity/*`. Receipts `rederive-counts.txt` (62/62), `identity.txt`, `pattern-period.txt`. No open finding under this lens.
- `[R414] PASS RTL` — no RTL in the diff. `hdl/ieee1722/aaf/KL_chan_map_capture.sv:567-590,1022-1046,1067-1078` and `hdl/milan/milan_datapath.sv:1217-1223`, checked against the bench readings: SLIP_TDM +36 dups and 0 skips across playback, and 333 to 999 over 1,303.4 s. Also checked: `docs/design/TIME_SYNC.md:463-479` and `docs/reference/REGISTER_MAP.md:1859-1862` (SLIP_TDM halves), and `git diff 13eda870 ec0cc0c1 -- hdl` (only PR #618's four `.sv` files; `sw/litex/milan_soc.py` changes only its import mechanism).
- `[R414] PASS Robustness` — the grader edge handling in packet `tools/grade_617.py:36-102`, `decode_din_pairs.py:30-73` (16-bit signed wrap, header and sequence checks) and `grade_usb.py:34-112`. Probes A-G (`receipts/grader-probes.txt`) cover wrap, skip, tear states, stop-tail mix, rotation and interpolation. The census includes the region-edge and outside-region frames. Also examined: the STOP conditions (full-length rc 0, card present), the restore after activity (`receipts/restore-census.txt`, `dut-state-diff.txt`), and repeat runs (two USB captures).
- `Tests`: UNCLEAN, from F2. Applied through probes A-G. The torn rule fails for the defect it claims to detect, the skip and repeat classes are exact, and the USB classifier is right. Tool hashes match the pages and the first-light origin list (`receipts/evidence-integrity.txt`).
- `Docs`: UNCLEAN, from F1, F2 and F3. The gates and anchors pass as above.

## Reviewer-owned completion ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | both pages vs #617 acceptance 4, assignment 5903384996, #451 checklist and amendment; packet grading JSON and identity; `rederive-counts.txt`, `identity.txt`, `pattern-period.txt` | R414-1 | `6dfa64a7506a8660a70d77eaa7c96c5de2886f5d` |
| RTL | CLEAN | `KL_chan_map_capture.sv:567-590,1022-1046,1067-1078`; `milan_datapath.sv:1217-1223`; `TIME_SYNC.md:463-479`; `REGISTER_MAP.md:1859-1862`; `git diff 13eda870 ec0cc0c1 -- hdl`; SLIP_TDM readings | R414-1 | `6dfa64a7506a8660a70d77eaa7c96c5de2886f5d` |
| Robustness | CLEAN | grader edge paths; probes A-G; outside-region census; STOP conditions; `restore-census.txt`; `dut-state-diff.txt` | R414-1 | `6dfa64a7506a8660a70d77eaa7c96c5de2886f5d` |
| Tests | UNCLEAN (F2) | `grader-probes.txt`; tool hashes; `mcasp-rx-rate.txt` | R414-1 | `6dfa64a7506a8660a70d77eaa7c96c5de2886f5d` |
| Docs | UNCLEAN (F1, F2, F3) | `docs-gates.txt`; `anchor-check.txt`; privacy scan; `docs/findings/README.md`; locator precedent in the 606 and 608 pages | R414-1 | `6dfa64a7506a8660a70d77eaa7c96c5de2886f5d` |

## Real limits

- **Raw recordings:** the DIN pcap, the DOUT capture and both USB captures (about 532 MB, indexed by size and SHA-256 in `RAW-ARTIFACTS.json`) are not public. The counts are re-derived from the published grading outputs, and the grading tools are fault-probed on synthetic data. The raw bytes were not re-graded.
- **USB low-byte detail:** the "0x20 at tag 1 to 0xc0 at tag 8" detail of frame 1,632 sits only in the unpublished per-segment grade file. It is not verified.
- **Simulation:** the scoped simulator path given for this round does not exist on this host (no such file at the assigned location). No Verilator suite was run. The PR changes no RTL. The RTL lens is applied by reading the RTL against the bench readings, and the manager's banks cover the source.
- **Hosted checks at the head:**
  - Executed and passed: `changes`, `rtl-fast`, `docs-check`, `docs-check-no-git`, `elaborate`, `bdd-conformance`, `wire-accountability`, `full-ci-gate`.
  - Skipped for docs-only scope: `verilator-suites`, `verilator-lint`, `yosys-portability`, `yosys-elaboration`, their shards, and `Physical gPTP`. A skipped context is not evidence (`receipts/hosted-check-runs.txt`).
- **Physical proof:** physical calibration, scope and continuity were NOT RUN. The bench readings are the operator's, not reviewer hardware proof.

## Pending manager duties

- Rule on F1: allow the index edit in this PR, or defer it to a named follow-up.
- Carry F2 and F3 to the executor. Re-review is needed for Docs and Tests at the corrected head.
- Optionally tie `d178f19a` to the `ec0cc0c1` build artifact (S1).
- Build and validate the final current-dev candidate at the merge turn. Source base and live dev are both `ec0cc0c1`.
- Hosted and act acceptance.
- Close #617 by hand after merge. Acceptance 4 is met here, and 1 to 3 landed with PR #618. #451 stays open: USB Audio FAIL, playback direction, continuity, scope and calibrated items.
- Merge needs the second independent positive review and the full completion bar.

## Receipts and scripts (listed in MANIFEST.sha256)

- `scripts/check_identity.py`, `check_restore_census.py`, `rederive_counts.py`, `probe_graders.py`, `mcasp_rx_rate.py`, `dut_state_diff.py`, `pattern_period.py`.
- `receipts/identity.txt`, `rederive-counts.txt`, `grader-probes.txt`, `mcasp-rx-rate.txt`, `restore-census.txt`, `dut-state-diff.txt`, `pattern-period.txt`, `docs-gates.txt`, `anchor-check.txt`, `hosted-check-runs.txt`, `evidence-integrity.txt`, `clone-integrity.txt`.
- **Clone:** after the round the clone is at the exact head with a clean worktree and index. The `git ls-files -s` digest equals the `HEAD` tree digest. The gitlinks are unchanged: `external` efeb541a, `gptp-processor` 5dce647a, `protocol-processor` c951a9ff, `third_party/verilog-axis` 48ff7a7e. One ignored `scripts/__pycache__/`, created by the docs-gate run, was removed.

R414-1 FINISHED
