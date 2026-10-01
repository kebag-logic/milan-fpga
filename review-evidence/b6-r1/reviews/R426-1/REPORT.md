[R426] NEGATIVE - exact head b5e9242e2e1911bb2bac11221527f8965a4ccaef

# R426-1: internal cleared-context review of PR #630 (Refs #629, bench lane B6)

- Head under review: `b5e9242e2e1911bb2bac11221527f8965a4ccaef`, tree `06140cbdf91f0722643609b5520ef32c6179854d`, one commit on dev `ea3fb38877842f223afea97e3bd72a10500455c9`.
- Diff: `docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md` (new, 534 lines) and one row in `docs/findings/README.md`. No RTL, test or tool file changes.
- Evidence read: `review-evidence/b6-r1/` at `128bc058af554ce9c1229fd036fe08c25b4250ac` (the `c9ada338` archive plus the manifest's `original_sha256` values).
- Reconstruction order: AGENTS.md, CONTRIBUTING.md, docs/README.md, Issue #629 body, the B6 assignment (#629 comment 5929778646), the executor's TAKEN, STOP and both REVIEW READY comments, the PR body, then the diff, then the evidence packet.
- Prior public review findings on PR #630: none exist at this head. The PR thread holds only the two review-start notices, and no review objects or inline comments. Nothing to resolve or retain.

Verdict: NEGATIVE. Three MINOR findings are open, under the Robustness, Tests and Docs lenses. Conformance and RTL are covered clean. The measured verdicts on the page hold up: A0 and B INTERNAL as controls, A1 PASS, A2 FAIL and B CRF PASS. All three findings concern what the page states about its own method and limits.

## What was checked independently

| Check | Result | Receipt |
|---|---|---|
| Every hash and byte count on the page against the packet | 54 of 54 resolve. 21 match `RAW-ARTIFACTS.json` with their sizes. 33 match the MANIFEST.json `original_sha256`. 12 of those are label-masked, so their page sizes cannot be checked against published bytes. All 21 unmasked sizes match. | `receipts/page-hashes.txt` |
| Packet integrity | 240 of 240 published files match `published_sha256`. The author's `MANIFEST.sha256` agrees with every `original_sha256`. It also lists a `.pyc` that the archive does not retain. | `receipts/packet-manifest-check.txt` |
| Tone loop | Regenerated with the published `b6_tone.py`. The bytes are identical: SHA-256 `566d3dfa...5588`, 48,000 unique pairs, no silent frame. | `receipts/tone-regenerate.txt` |
| Tool controls | Re-ran `b6_thdn.py controls`. The output is byte-identical to the published `controls.json` (`7bbefc71...530e`) and ALL_PASS. The clean floor is -146.065 / -145.993 dB. The drop and the repeat are found at frames 216,777 and 289,234. Resampled offsets fit at +16 and +1 ppm. Slips are found as 23 skips at 62,500 spacing and 4 at 1,000,000. | `receipts/controls-rerun.log`, `receipts/controls-compare.txt` |
| Per-case figures | Recomputed from `summary/<case>/grade.json`, `events.csv` and `blocks.csv`. Checked: windows, blocks at the floor, THD+N and SNR, fitted offsets, listener, beat and capture counts, counted and timed ratios with half-widths and halves, comb period, residual and SLIP_TDM agreement, the capture table, the "1, 2, 7, 3, 0" read-gap counts, and "255 of 265". All match, except the items in F3 and S1. | `receipts/reconcile-figures.txt`, `receipts/one-frame-rise.txt` |
| Binding rule and clock sources | Audited every run, including the probe and three smoke runs the page does not mention. Before every bind, the listener read back the talker's format. No talker format was set. Clock sources were set only on the listener (peer in A1 and A2, DUT in B CRF), read back equal, then restored and read back. Every format and map final state equals the as-found state. | `receipts/binding-clock-audit.txt` |
| B CRF servo | `MCSRV_STAT` decoded against `docs/reference/REGISTER_MAP.md:2082`. The servo went IDLE `0x20`, then ACQUIRE `0xffaa0033` 3.33 s after the set, then LOCKED `0xffa10034` 6.49 s after it. Trim is -6.0 ppm. Bit 4 is the DRP config mismatch. All three window reads show LOCKED. `SLIP_TDM` holds at `0xc066`. | packet `runs/bcrf/events.jsonl` |
| Residuals | `restore/dut-start.txt` and `dut-end.txt`: NVM commits went from 2 to 8, seq 243 and 244, `pend=1`. `census-compare.txt`: 43 of 46 equal, with the two peer talker states carrying a stream ID, destination MAC and VLAN at connection count 0. Both match the page. | packet |
| Identity | VERSION, the AEM, ROM and QSPI CRCs, the ENTITY and CONFIGURATION byte-equality, and the grader 10/10 all match `identity/*`. | packet |
| Attribution probe | Disposable synthetic run through the unmodified `grade_b6.py`, with planted events of known cause. See F1. | `receipts/attribution-probe.txt`, `scripts/attribution_probe.py` |
| Absorption bound on the real cases | See F1. | `receipts/absorption-bounds.txt` |
| Docs gates at head, pinned renderer (cmarkgfm 2025.10.22, html5lib 1.1) | All rc 0: `docs_check.py`, `check_doc_style.py`, `gen_toc.py --check`, `check_em_dash.py --base ea3fb388...`, `check_doc_paths.py`, `gen_toc.py --verify-anchors`, `check_feature_status.py --self-test`, `ci_scope.py --selftest`, and `git diff --check ea3fb388 HEAD`. | `receipts/gates.txt` |

## Judgement on the assignment's five questions

1. **Tool and synthetic controls.** Sound, and independently reproduced byte-for-byte (above). The controls prove only the decoder and fitter in `b6_thdn.py`. Nothing exercises the attribution layer in `grade_b6.py` (F1).
2. **Clock-source record.** Holds. See the audit row above.
3. **Case verdicts.**
   - A0 and B INTERNAL show the mismatch.
     - A0: 519 drops and 321 beat repeats, ratio +6.52 counted and +6.44 +-0.72 timed.
     - B INTERNAL: +6.05 counted and +6.85 +-1.46 timed.
   - A1 PASS holds: 0 listener events, counted -10.631 ppm equal to exactly -315 beat repeats, and every clean block within 0.0002 dB of the floor.
   - B CRF PASS holds against its pre-stated criteria: LOCKED, 0 net steps in 30,237,600 frames, a timed interval of -0.007 +-0.652 that holds zero, and 0 listener events.
   - A2 FAIL holds. The diagnosis is **supported by measurement, not merely consistent with it**. Through the same peer, the DUT's two streams are measured at two different rates:
     - following the AAF stream, McASP0 against the peer is -10.631 ppm, which is the beat;
     - following the CRF stream, it is -0.068 ppm, so the peer locks to the DUT's TDM clock;
     - `SLIP_TDM`, at 0.5096 to 0.5111 per s, is the 10.64 ppm gap.

     The design references agree. `hdl/ieee1722/crf/KL_crf_tx.sv:20-21` sets the timestamp grid by a /512 divide of `clk_audio_i`; the cited `hdl/milan/milan_datapath.sv:445` is the port comment stating that contract. `docs/design/TIME_SYNC.md:166-169` gives the 47,999.4893 Hz physical grid against the 48,000.0000 Hz free-running `KL_media_nco` packet grid. Issue #74 keeps INTERNAL free-running by design. No root-cause tracking is named on the page (S4).
4. **Attribution rules.**
   - The rules are stated, and the stated rules match the code. The rule history is disclosed.
   - Uniform application is consistent with the per-case outputs. One grader binary produced all five grades, and the read-gap and size counts reconcile.
   - The capture-path attributions follow from the published read-time evidence. Each rise-matched cluster's rise equals its loss within the stated tolerance.
   - The one-buffer replays net to zero, or to the rise with one loop added.
   - The refinement **can** hide a listener event through three mechanisms, which the probe demonstrates (F1). For A1 and B CRF the published summaries bound all three to zero outside lost audio. The two verdicts therefore stand, but the page states neither the mechanisms nor the bound.
5. **Restore and residuals.** Verified as stated. The three smoke runs also edited DUT maps and are part of the NVM commit history the page reports (S2).

Public-text hygiene: the page names roles only. It does not state the capture channel count or indices, or the peer's descriptor indices. The words it uses (McASP0, bridge legs, the board's USB network link, identity mappings, the clock consumer) appear on the merged pages `451_TDM8_TIMING_SOC_BOARD.md` and `617_DIN_FRAME_COHERENCE_BENCH.md`, and `docs_check.py` passes. The PR body uses the template's sections except the optional Contents list (S5), and says `Relates to #629` with no closing keyword. That matches the assignment's "Refs #629 only" intent.

## Findings

### F1 MINOR: Robustness, Tests, Docs. The refined attribution can absorb listener events, and the page neither states how nor shows the bound

- **Where:**
  - `docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md:149-171` (Attribution);
  - `:405-412` (capture-path bullets, "Two are one frame off the pattern");
  - `:448-466` (Limits);
  - artifact `tools/grade_b6.py` in the packet: clustering of `|step| >= 2`, the `cap` decision, and `BEAT_RES = 50`.
- **Authority/evidence:** AGENTS.md section 8 says "Never hide a material assumption". The assignment asked whether the capture-path attributions could hide listener slips, and the page states that the A1 and B CRF verdicts rest on the refined attribution. The unmodified grader, run on a synthetic capture with planted causes (`receipts/attribution-probe.txt`), shows three absorption paths:
  - (a) a one-frame listener drop at the same step as a 540-frame capture-path loss became one 541-frame step, classed capture path by the read-time rise (11.25 ms against 11.27 ms, inside 1 ms + 2 %);
  - (b) a one-frame listener repeat 20 frames after a beat repeat was classed `DUT beat`, because comb membership is a 50-frame window with no one-member-per-tooth check;
  - (c) a 60-frame listener skip whose measured rise was 0.0 ms was classed capture path. The "spoiled rise" arm accepts any non-matching rise after a read gap of 11 ms or more, here a lossless 18 ms gap, when the size is 48 n + 12.

  In the real data:
  - A0 cluster 0 (step 1,165) and A2 cluster 15 (step 109) are 48 n + 13. Path (a) predicts exactly that size, but the page reports them only as "one frame off the pattern".
  - For A1 and B CRF, `receipts/absorption-bounds.txt` shows no off-pattern capture-path skip outside replay edges and losses longer than a loop, no two beat members closer than 1,000 frames, and no spoiled-rise cluster.
  - A1's two rise-unmeasurable clusters are all 48 n + 12.
- **Impact:** No verdict changes. A cold reader cannot tell from the page that the attribution has these blind spots, or that A1 and B CRF were checked against them. A0's 519 and A2's 494 listener drops may each be one low.
- **Required outcome:**
  - The page states the three ways the attribution can absorb a listener event. For each, it gives the published evidence that bounds it in A1 and B CRF, at least the observations above.
  - It qualifies the A0 and A2 listener counts for the two 48 n + 13 steps.
  - Or the grader flags such cases itself, with the page reporting the flags.
- **Verification:** Read the revised page. Reproduce the bound from the packet's `summary/` with `scripts/absorption_bounds.py` (output `receipts/absorption-bounds.txt`) and `scripts/reconcile_figures.py`.

### F2 MINOR: Docs, Tests. The B CRF window is misstated as starting 20 s after LOCKED

- **Where:** `docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md:138-139`: "for B CRF, from 20 s after the DUT's servo read LOCKED".
- **Authority/evidence:** packet `runs/bcrf/events.jsonl`. The clock set is at t = ...054.756. `servo-lock` comes 6.49 s later, at ...061.249. `window-start` is at ...075.253: 14.00 s after LOCKED and 20.50 s after the set. Packet `tools/run_b6.py` starts `t_set` right after the clock-source set and read-back (around line 513), then waits until `SETTLE_S` = 20 s from `t_set` (around line 526). That is not 20 s from the lock.
- **Impact:** The method record of a PASS case misstates the settle time it actually had. The verdict is unaffected: 0 net steps over the window, and LOCKED at every in-window read.
- **Required outcome:** The page states the B CRF window as it was run: from 20 s after the clock-source set, which was 14.0 s after the servo read LOCKED.
- **Verification:** Compare the revised sentence with the `set-clock`, `servo-lock` and `window-start` timestamps in `runs/bcrf/events.jsonl`.

### F3 MINOR: Docs. The read-rise exceptions are DUT-beat events, not listener events, and A2's coverage is unstated

- **Where:** `docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md:420-422`: "One-frame listener events show no read-time rise ... The two exceptions, 2.7 ms and 177 ms, sit next to A2's 13.3 s stall."
- **Authority/evidence:** packet `summary/a2/events.csv`.
  - The 2.6798 ms and 176.8061 ms rises are on capture frames 28,121,160 and 28,147,698, and both have cause `DUT beat`.
  - The largest listener-event rise in any case is 1.0067 ms.
  - In A2 only 135 of 674 listener events have a measurable rise. The other 539 sit too close to a neighbouring event.

  Receipt: `receipts/one-frame-rise.txt`.
- **Impact:** A stated piece of evidence for the attribution cannot be reproduced as written. The A2 statement rests on a fifth of its events without saying so.
- **Required outcome:** The bullet attributes the two exceptions to the class they belong to. It states, per case, how many one-frame events had a measurable rise.
- **Verification:** Recompute from `summary/<case>/events.csv` with `scripts/one_frame_rise.py` (output `receipts/one-frame-rise.txt`).

### Suggestions (do not affect coverage)

- **S1** (`:26`, `:310-311`): 519 drops in 629.56 s is 17.2 ppm. The 17.1 ppm figure is the net of the one silent insert (518). Say which one is meant.
- **S2** (`:16-18`, Method): the packet holds three preliminary A0 runs that the page does not mention:
  - `smoke-a0`, with a 30 s window;
  - `smoke2-a0`, with a 90 s window;
  - `smoke-a0-clkparse`, aborted before any bind.

  The first two bound the DUT's AAF stream, set the peer's format and edited the DUT's map, and are part of the reported NVM commit count. All of them followed the binding rule and restored (`receipts/binding-clock-audit.txt`). Name them as tool shakedown runs.
- **S3** (`:378-379`): "stayed LOCKED through the window" rests on three in-window reads, at 5 s, about 315 s and about 615 s. Say so.
- **S4** (A2 section): name where the A2 root cause is tracked or awaiting decision. The cause is the CRF talker on the physical clock against the AAF packet grid at INTERNAL, which #74 keeps free-running. Today that disposition appears only in the REVIEW READY comment, and the page offers nothing durable. This is a manager or owner duty, not a defect in this diff.
- **S5** (PR body): the template's Contents list is omitted.

## Prior public findings

None existed on PR #630 at this head when this round finished its independent pass. The two PR comments are review-start notices, and there are no review objects or inline comments. Nothing is resolved or retained.

## Reviewer-owned completion ledger

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #629 acceptance (bench items and quality metric) and assignment 5929778646, against page `:20-33`, `:219-229`, `:250-271` and `:448-466`. The packet's `runs/*/events.jsonl` were audited for binding, clock source and restore. PR body against `.github/PULL_REQUEST_TEMPLATE.md`. `Relates to #629`, no closing keyword. | R426-1 | `b5e9242e2e1911bb2bac11221527f8965a4ccaef` |
| RTL | CLEAN | No RTL in the diff. The A2 diagnosis was checked against `hdl/milan/milan_datapath.sv:445`, `hdl/ieee1722/crf/KL_crf_tx.sv:20-21`, `docs/design/TIME_SYNC.md:166-169,463-479` and Issue #74's INTERNAL rule. `MCSRV_STAT` and `SLIP_TDM` decodes were checked against `docs/reference/REGISTER_MAP.md:2082` and TIME_SYNC.md:169. The scoped Verilator was identified (5.050) and not needed. | R426-1 | `b5e9242e2e1911bb2bac11221527f8965a4ccaef` |
| Robustness | UNCLEAN (F1) | Packet `tools/grade_b6.py` attribution. Synthetic absorption probe. `summary/*/grade.json` clusters and `events.csv` bounds. | R426-1 | `b5e9242e2e1911bb2bac11221527f8965a4ccaef` |
| Tests | UNCLEAN (F1, F2) | `b6_thdn.py` controls re-run byte-identical. No control covers the attribution layer. `run_b6.py` settle against the page's method. | R426-1 | `b5e9242e2e1911bb2bac11221527f8965a4ccaef` |
| Docs | UNCLEAN (F1, F2, F3) | Full page and index row. 54 of 54 hashes. All per-case figures recomputed. Docs gates at head, pinned renderer. Hygiene compared with the merged precedent pages. | R426-1 | `b5e9242e2e1911bb2bac11221527f8965a4ccaef` |

## Real limits of this round

- The raw captures, read-time records and McASP0 samples stay on the bench host. The grades were not re-run from raw data, so the per-case figures are checked for internal consistency against the published summaries, not re-derived.
- The original "first rule" outcome (A1 4 and B CRF 3 multi-frame events) could not be re-derived. It needs the raw read-time records.
- For label-masked files (12 cited on the page), only the hash is checkable. The cited byte counts are of unpublished originals.
- The attribution probe uses a simplified read-time model: exact 48 kHz device time, 10 ms reads, and a 30 ms gap at each loss. It shows that the mechanisms exist, not how often they occur on the bench.
- No hardware, bench, or hosted or local CI run was performed. Physical calibration was NOT RUN.
- Hosted contexts at this head when read: `rtl-fast`, `elaborate`, `docs-check-no-git`, `wire-accountability`, `bdd-conformance` and `full-ci-gate` concluded success. The long aggregates (`verilator-suites`, `yosys-portability`) and their shards were skipped contexts, as for a docs-only PR. `docs-check` was still in progress (`receipts/hosted-checks.txt`).

## Pending manager duties

- Hosted and local-replica acceptance at the exact head, including the in-progress `docs-check`.
- The candidate merge build on live dev.
- The A2 root-cause disposition (S4): an owner decision or a new Issue.
- The external review (R427).
- Re-review of F1 to F3 at the corrected head.

Clone restored: HEAD and tree as above, an empty `status --porcelain --ignored`, 978 tracked blobs equal to HEAD in bytes and mode, and the four gitlinks equal to HEAD (`receipts/clone-state.txt`).

R426-1 FINISHED
