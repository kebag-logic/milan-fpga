[R456] NEGATIVE - exact head 6b96391d13c5d777a98b1c7be9265c63d651c911

# R456-2: internal cleared-context review of #643 / PR #648, round 2

- **Head:** `6b96391d13c5d777a98b1c7be9265c63d651c911`, tree `20de609684af73ef2e8dff3da994e45c976ba5bd`.
- **Round 2 delta:** `98729742..6b96391d`. It holds three commits:
  - the `--no-ff` merge of dev `241f9184` (`7aa7b449`);
  - `e63c4279`: the window, the gradable checks, the setpoint mutants, `--law-boundary` and the docs;
  - `6b96391d`: TIME_SYNC.md wording.
- **Files against live dev `241f9184`:** seven: `sim_tdm8_render.cpp`, `tdm8_render_mutants.py`, the suite Makefile, `MEDIA_CLOCK_FOLLOWING.md`, `TIME_SYNC.md`, `TESTING.md` and `tb/verilator/README.md`. No file under `hdl/` and no gitlink changes.
- **Scope reconstructed from:**
  - `AGENTS.md`;
  - the #643 body;
  - the lane assignment (5972861856), the item-1 STOP (5973437153), the ruling (5973450039), the round-2 ruling (5974715857) and REVIEW READY round 2 (5975549174);
  - the PR body;
  - the published round-2 hand-off (`643-review-evidence` at `5aff1fcb`, `author-r2/HANDOFF.md`);
  - `KL_render_setpoint.sv` and `milan_datapath.sv`.
- **Verdict:** NEGATIVE, on one open MINOR (F1).
  - The window is built as W = S + guard = 4 + 4. The stated walk S = 4 understates the head's own measurement of the CRF window at dev's processor pin, which is 5 cycles.
  - Everything else the round-2 ruling asked for is met, and I reproduced it at both processors.
  - The four round-1 findings (R456-1 F1 MAJOR and F2; R457-1 F1 and F2) are resolved at this head.

## Findings

### R456-2-F1 MINOR: the stated walk, and so W's stated basis, is one cycle below the head's own CRF measurement at dev's pin

**Severity and lenses:** MINOR. Lenses: Conformance, Tests, Docs.

**Where:**
- `tb/verilator/milan_dp_render/sim_tdm8_render.cpp:189-197`: "at most 3 cycles in a [LAW] phase ... and 4 across T30's CRF window, so the walk is stated as 4", then `kLawWalkCycles = 4`.
- `sim_tdm8_render.cpp:1431-1444`: `walk()` is the smaller of two ranges, the nearest pop's and the next pop's.
- `sim_tdm8_render.cpp:3232-3240`: one line prints the nearest-pop range and that `walk` side by side.
- `docs/design/MEDIA_CLOCK_FOLLOWING.md:1371`: "within one graded window it walks by up to 4 cycles".
- `MEDIA_CLOCK_FOLLOWING.md:1379-1383`: "T30's CRF window, 292 PDUs under CRF, walked 4 ... The window is the walk plus a guard of 4 cycles: 8 cycles".
- The PR body, Known limitations: "W = 8 is the largest walk measured (4, in the CRF window) plus an equal guard ... `tdm8render-law-boundary` re-measures it".

**Authority and evidence.**
- **Authority.** The round-2 ruling, item 1, says: "State the measured spread S, and set the window W = S plus a guard". The page defines the spread as how far "the offset from a PDU end to its nearest pop" walks within one graded window (`MEDIA_CLOCK_FOLLOWING.md:1370-1371`).
- **The full leg at dev's pin `631eeb34`.** For the CRF window it prints "the pop nearest the boundary -592..-587 (walk 4)" (`receipts/suites/suite-p631.log:31`). The author's published table shows the same pair: nearest pop -592..-587 beside "Walk 4" (`author-r2/HANDOFF.md`, R2.3).
- **The CRF window's histogram.** A probe added one harness line that prints the histogram and changed no grading (`crfhist`).
  - At dev's pin: `-592:3 -591:32 -590:54 -589:71 -588:106 -587:26` over all 292 steady ends (`receipts/probes/hp-crfhist-full.log:24`). That is six offsets, so the nearest pop walks 5 cycles.
  - At `c4cb84ff`: 336..340, 4 cycles (`c4-crfhist-full.log:24`).
- **The two figures use different measures.**
  - The `[LAW]` figure, "at most 3", came from the nearest-pop histograms ("recomputed from the logged histograms", HANDOFF R2.1 item 2). I confirm it: the largest range over 786 settled `[LAW]` histograms is 3 (`receipts/summary.txt`).
  - The CRF figure, 4, came from the printed `walk`, which is the smaller range.
  - Measured the way the page defines it, S is 5 at the lane's own pin.
- **The printed walk is narrower than its own line.** In 89 of the 1,042 windows across this round's logs, `walk` is below the nearest-pop range printed on the same line. For example, "-11..-8 (walk 2)" (`c4-clean-lb-2036alone.log`). The tick is fractional (2083.3 cycles), so the next-pop range can be one cycle narrower even where nothing wraps.
- **`tdm8render-law-boundary` does not show the walk.** Its runner keeps each leg's output for judging and prints only the verdict lines. `receipts/suites/bnd-p631.log` contains no histogram and no walk, so the claim "re-measures it" cannot be checked from the target's output.

**Impact.**
- At the lane's own processor pin, the documented basis of `kLawWalkCycles` is one cycle low. So is the "walk plus an equal guard" construction of W: the data supports W = 5 + 3, not 4 + 4.
- A reader who re-measures with the head's own output sees "(walk 4)" printed beside a 5-cycle nearest-pop range.
- No verdict, margin or graded result changes:
  - W = 8 still exceeds 5;
  - every graded window's clearance is measured directly;
  - the CRF window's margin is 579 at dev's pin and 327 at `c4cb84ff`.
- The defect is a stated measurement figure, so under the owner rule it is not RESIDUE.

**Required outcome.**
- One walk measure is stated and used for both the `[LAW]` figure and the CRF figure.
- The stated S, the `kLawWalkCycles` comment, `MEDIA_CLOCK_FOLLOWING.md:1371` and `:1379-1383`, and the PR body agree with the head's instrument at both processors.
  - For example, S = 5 from the CRF window's nearest-pop histogram at `631eeb34`, with W restated as 5 plus the guard.
  - Whether W stays 8 or changes is an explicit, stated choice.
- The printed walk no longer contradicts the nearest-pop range on its own line, or the line says which range it reports.
- Either the diagnostic shows the walk it measures, or the PR body and docs stop saying it re-measures it.
- If W changes, rerun the standing suite and `tdm8render-law-boundary` at both processors.

**Verification.**
- At both processors, run the full leg with the CRF histogram printed. This packet's `crfhist` edit does that (`scripts/r2_builds.sh`, lane L7).
- Compare the stated S with the largest nearest-pop range over the 18 `[LAW]` windows and the CRF window.
- Then read the docs and the PR body against that figure.

### Suggestions (non-blocking)

- **S1 (Tests, Robustness): include the recentre's PDU end in the CRF clearance span.**
  - The T30 CRF LAW's clearance span starts at `crf_first + 4` (`sim_tdm8_render.cpp:3411`). The settled recentre's re-snap end sets that window's fill reference, but it lies outside the span.
  - A `[LAW]` span starts at 0 and does include its snap, as `:3171` says ("the snap's included").
  - With margins of 327 to 579 cycles this cannot matter today. Include that end, or state the difference.
- **S2 (Tests): check the measured walk against `kLawWalkCycles`.**
  - Nothing checks it today, and my ablations show no test notices a smaller W. At W = 0 and at W = 4, every graded window of the sound design still passes and both setpoint defects still fail (`hp-w0-*`, `hp-w4-*`, `hp-spm1w0-*`, `hp-spp1w0-*`).
  - A check in each standing window that the walk is at most `kLawWalkCycles` would keep the stated S true as the model moves.
- **S3 (Docs, Robustness): document what a CRF gradability failure means.**
  - The CRF window's position against the grid moves with processor content and run history. Its nearest pop is at -587 at dev's pin and +336 at `c4cb84ff` in the full leg, and at -1018 under `--crf-only`.
  - A later pin can therefore put it inside W. "T30 CRF LAW: gradable" would then fail by name with no design defect; `hp-crfw1104-crf.log` shows that path.
  - The test section should say how to recognise such a failure and what the remedy is.
- **S4 (Tests): a stray quote in the verdict line.** `tdm8_render_mutants.py:676` prints `breaks "<name>" and 35 more"`. It came in with `22f9a244`, and the executor disclosed it. Cosmetic.
- **Retained from R456-1, not taken (optional):**
  - S1: the accept-pulse instrument in `milan_dp`. It is out of scope and a candidate new Issue (= R457-1 S3).
  - S2: require the stage's counters to stay unchanged across each graded window.
  - S3: name the ceiling check for what it bounds.

## Prior public review findings, resolved or retained at this head

| Finding | Status at `6b96391d` | Evidence (this round) |
|---|---|---|
| R456-1-F1 MAJOR: the tie rule's one-cycle premise fails at the boundary | **Resolved** | The tie rule is gone: the fill must read exactly 14 (`:3296`) and `kBandSlackCycles` went from 64 to 1 (`:183`). Gradability is measured per window (`:3228-3254`). My unchanged boundary probes: `tieon` (+2018..+2035 as a standing list) fails "gradable" by name at +2018..+2034, with PDU and offset and no law check. It grades +2035 PASS. Both processors agree (`hp-tieon-law`, `c4-tieon-law`, 55/17). `tiespm1` and `tiespp1` leave the same 17 phases not gradable and grade +2035 FAIL on fill and band (55/19). In three +2025 histories (the +2018 scan, the +2010 scan and +2025 alone), +2025 is NOT GRADABLE at both processors (`hp-clean-lb-*`, `c4-clean-lb-2025alone`). Setpoint −1 in the +2018 history fails the only graded phase at both processors (`hp-/c4-spm1-lb-2018up`). The docs no longer claim one cycle. |
| R456-1-F2 MINOR: `TIME_SYNC.md:451` gives the accept-pulse reading | **Resolved** | `TIME_SYNC.md:451-455` now states the PDU-end reading and points to the test plan's window. That matches `prove_the_setpoint_law_still_holds` (`:3268-3323`). The docs gates pass. |
| R457-1-F1 MINOR (= R456-1-F1) | **Resolved** | As above. R457's `probe-instrument.patch` targets the removed tie code. This round's equivalents of its runs: +2025 alone is NOT GRADABLE at both processors, and setpoint −1 is never graded PASS (the published diagnostic, 81/81 at both). |
| R457-1-F2 MINOR (= R456-1-F2) | **Resolved** | As above. |
| R457-1 S1: grade the exact PDU count | Adopted | `check.dec(... 124)` at `:3311`. Every `[LAW]` window logs 124 PDUs. |
| R457-1 S2: the A2-a arm proves only the settle gate | Superseded | The setpoint ±1 arms now prove the law checks: 36/36 at both processors. |

## The focus items, verified

| Item | Result | Evidence |
|---|---|---|
| The measured walk and W = 4 + 4 = 8 are supported by the published boundary data at both processors and in three histories | **`[LAW]`: yes. CRF: no (F1)** | The published R2.1 table gives a maximum walk of 2 ascending, 3 descending and 3 alone, identical at both pins. My own histories reproduce the maximum of 3 for `[LAW]`. My ascending and descending scans over +1986..+2066 (explicit lists, so without the leg's locating +0 phase) give **identical offset lines and histograms at both processors in all 81 phases** (`hp-w0/w4-lb-up/down` against `c4-clean-lb-up/down`). Their largest histogram range is 3 in each direction, and it is 3 across my 12 alone runs. The CRF window walks 5 at dev's pin and 4 at `c4cb84ff` (F1). |
| A window within W of the boundary is NOT GRADABLE (never passed, never failed) and named | Yes | A window is gradable only if its clearance exceeds 8 (`:3231`). It prints `[NOT GRADABLE] <tag>: PDU <id>'s end has a pop taken <offset> cycles` (`:3241-3245`), and its law checks are skipped (`:3268`). Under `--law-boundary` no check is added; for a standing window the gradable check fails. Example: +2016 alone has clearance 8, is NOT GRADABLE, and fails nothing (`hp-clean-lb-2016alone`). |
| Every standing window asserts its margin, and the suite fails if one is not gradable | Yes | The check is at `:3246-3252` and applies to each of the 18 `[LAW]` windows and to the CRF window (245 checks = 226 + 19). Margins: +0 is 48 in `--law-only` and 49 in the full leg; +1953 is 64 and 63; the CRF window is 579 at dev's pin and 327 at `c4cb84ff` (`suite-*.log`). The failure is shown for `[LAW]` (`tieon`) and for the CRF window (`hp-crfw1104-crf`). There, with W widened past every clearance, "T30 CRF LAW: gradable" fails and the law is not graded (50/1). |
| Graded windows read a fill of exactly 14, and the band has no tie slack | Yes | `:3296`, and `:183` (one cycle, for the pop pulse's register). Every graded window of the sound design in this round reads `fill 14..14` (`summary.txt`). At the gradable edge, +2035 with margin 1, the band still separates the designs: 8.996 T sound, 7.996 T low, 9.996 T high. |
| Setpoint −1 and +1 fail all 18 phases | Yes | `hp-spm1-law`, `hp-spp1-law`, `c4-spm1-law` and `c4-spp1-law` each read 106/36: exactly the fill and band checks at all 18 phases. The campaign's own `verdict()` reads each one as `caught` against its 36-name target, and reads the clean log as `pass` (`setpoint-arm-verdicts.log`). Under `--crf-only` both fail the CRF fill and band checks. |
| The boundary diagnostic never fails the sound design and never passes setpoint ±1 in a graded window | Yes | I ran the published target as TESTING.md documents it (`cd tb/verilator/milan_dp_render && make tdm8render-law-boundary`): **rc 0, 81 checks, 81 PASS at both processors** (`bnd-p631.log`, `bnd-pc4c.log`). It located the boundary at +2026. It left +2017..+2034 not gradable in both scans and +2016..+2036 alone, identical to the published table. I unit checked the judge: it refuses a defect graded PASS, a NOT GRADABLE phase with a failure, and a crash (`arg-parsing.log`). |
| The docs (`TIME_SYNC.md:451-455`, the MEDIA_CLOCK_FOLLOWING ambiguity window, README, TESTING) match the code | Yes, except the walk figure (F1) | Read against the code. The inventory matches the runner: 21 mutants, 3 leg defects, 3 clean controls, 32 checks, and 81 diagnostic checks. Docs gates rc 0 (`gates.log`, `gates-md.log`): `docs_check`, `check_doc_style` and `check_doc_paths`. With the pinned Markdown environment: `check_em_dash --base 241f9184` (0 findings over 71 added lines), and `gen_toc --check` and `--verify-anchors`. |
| The dev merge is `--no-ff` and clean | Yes | `7aa7b449` has parents `98729742` and `241f9184`. Its tree `5c72a5b4` equals `git merge-tree --write-tree 98729742 241f9184`, so no conflict was hand-resolved. All five lane commits are one line with no trailer. |
| The R456-1 steps rerun unchanged | Yes | `scripts/r1-unchanged/` is byte-identical to the R456-1 packet, and the edit strings are copied verbatim into `scripts/r2_builds.sh`. The driver plants harness edits in place, so builds ran in parallel lanes on separate copies of the tree. `tieoff`, `tietr18` and `tietr36` refuse to build because their edits target the removed tie code. `check_mutant_verdict.py`: 7/7 PASS. The base harness reproduces #643's failure at `c4cb84ff` (227/292, 285/292) and passes at `631eeb34`. |
| The suite passes at both processors | Yes | The default target is rc 0 at both: 245/0, 65/0, leg defects 5/5. Wall times were 683 s and 701 s under GNU make 4.4.1, after the diagnostic had built the default elaboration. |

## Lens results

```text
[R456] UNCLEAN Conformance - sim_tdm8_render.cpp:189-197, MEDIA_CLOCK_FOLLOWING.md:1371,1379-1383 against ruling 5974715857 item 1 - F1 MINOR: stated S = 4 against a measured 5-cycle CRF nearest-pop walk at 631eeb34 (receipts/probes/hp-crfhist-full.log:24). Items 2-5 of the ruling are met (focus table).
[R456] PASS RTL - hdl/ and gitlinks (0-line diff 241f9184..6b96391d); KL_render_setpoint.sv:454,497-499,533-534; the milan_datapath.sv taps the harness reads - pop_take = pulse cycle - 1 matches pop_p_o registered from pop_take_w, and fill_end_w counts a pop taken in the end beat's cycle, so "delta <= 0 is in the fill" (sim_tdm8_render.cpp:716-747) is the RTL's own boundary; no RTL or interface change
[R456] PASS Robustness - sim_tdm8_render.cpp:305-328,3228-3254,3486-3519,4009-4017; tdm8_render_mutants.py:558-580,691-721 - six malformed --law-boundary lists refused; --jobs refused outside --law-boundary and at 0; the judge refuses a crash, a NOT GRADABLE phase with a failure, and a defect graded PASS (receipts/arg-parsing.log); history dependence at +2016/+2025/+2035/+2036 comes out NOT GRADABLE, never graded wrong (bnd-*.log, hp-/c4-clean-lb-*); law_reset runs per phase through build_injection_record; the settled-hold and ceiling paths are unchanged (hp-a2a-law, hp-bootnodwell-law)
[R456] UNCLEAN Tests - sim_tdm8_render.cpp:1431-1444,3232-3240; tdm8_render_mutants.py:776-806 - F1 MINOR: the printed walk understates its own nearest-pop range (89 of 1,042 windows), and the diagnostic prints no walk. Otherwise the tests discriminate: setpoint +/-1 36/36 at both processors, A2-a 19 failing at both, the boundary diagnostic 81/81 at both, and the standing gradable check shown to fail for [LAW] and for CRF.
[R456] UNCLEAN Docs - MEDIA_CLOCK_FOLLOWING.md:1329-1330,1356-1413; TIME_SYNC.md:451-455; TESTING.md:285-287,521,523; tb/verilator/README.md:63; suite Makefile:18-26,198-205; PR body - F1 MINOR (the walk figure and "re-measures it"); everything else matches the code and the receipts; docs gates rc 0
```

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1) | the #643 body; rulings 5973450039 and 5974715857; REVIEW READY 5975549174; the window, gradability, law, `[LAW]` and `--law-boundary` code in `sim_tdm8_render.cpp`; the `TIME_SYNC.md` law table and `:451-455`; suite, probe and diagnostic receipts at both processors | R456-2 | `6b96391d13c5d777a98b1c7be9265c63d651c911` |
| RTL | CLEAN | the `hdl/` and gitlink diff (none); the pop, fill-end and PDU-end logic in `KL_render_setpoint.sv`; the `milan_datapath.sv` taps the harness reads | R456-2 | `6b96391d13c5d777a98b1c7be9265c63d651c911` |
| Robustness | CLEAN | argument refusal in the harness and the runner; the judge's refusal paths; history-dependent boundary phases in four histories at both processors; the gradability edge (+2016, +2035, +2036); the CRF window at three positions; the A2-a and no-dwell settled paths | R456-2 | `6b96391d13c5d777a98b1c7be9265c63d651c911` |
| Tests | UNCLEAN (F1) | the suite at both processors; `--law-only` clean, A2-a and setpoint ±1 at both; setpoint ±1 under `--crf-only`; the published diagnostic at both; the W ablations; the CRF gradable-failure probe; `check_mutant_verdict.py`; the campaign's `verdict()` on the setpoint logs | R456-2 | `6b96391d13c5d777a98b1c7be9265c63d651c911` |
| Docs | UNCLEAN (F1) | the `MEDIA_CLOCK_FOLLOWING.md` test rows and "The render law's grading instant"; `TIME_SYNC.md:451-455`; the `TESTING.md` rows and wall time; `tb/verilator/README.md:63`; the Makefile header; the PR body; the docs gates | R456-2 | `6b96391d13c5d777a98b1c7be9265c63d651c911` |

## Real limits

- **Make version and wall times.** GNU make 4.3 is not installed on this host, so every run used GNU make 4.4.1. The suite walls (683 s and 701 s) came after the diagnostic had already built the default elaboration, on a shared host (load average 23 to 101). They are not a cold figure to compare with 663.8 s.
- **Campaign not run.** I did not run the full `tdm8render-mutants` campaign (32 checks; the author reports rc 2 on four pre-existing arms). I reproduced the three arms this round touches (A2-a and setpoint ±1) directly at both processors, and applied the campaign's own `verdict()` to them.
- **Alone history.** The ±40 alone runs of item 1 are the author's. The published target ran ±12 alone at both processors. I added 12 alone runs between +1990 and +2062: 9 at dev's pin and 3 at `c4cb84ff`.
- **Published round-2 evidence.** The hand-off cites `law-boundary-scan.md` and the suite, campaign and diagnostic logs by hash. The public archive (`5aff1fcb`) holds only `HANDOFF.md` and `PR-BODY.md`. My conclusions rest on my own receipts.
- **Not run:** Yosys; the parent, processor, gPTP and builder banks; `act`; Docker; hosted runs; physical calibration; hardware. Field skips are not hardware proof.
- **Hosted state, read-only snapshot at 02:24 UTC** (`receipts/hosted-snapshot.tsv`):
  - success: rtl-fast, elaborate, verilator-lint, Yosys shards 0-3, yosys-elaboration, Verilator shards 0 and 3, bdd-conformance, wire-accountability, docs-check-no-git and full-ci-gate;
  - in progress: Verilator shards 1, 2 and 4, and docs-check;
  - skipped: the physical gPTP context. A skip is not an executed result.

## Pending manager duties

- Carry F1 to the executor. If W changes, that is a measurement restatement under the round-2 ruling. A new ruling is needed only if the window's construction changes.
- Publish the round-2 evidence the hand-off cites (`law-boundary-scan.md` and the logged gate receipts), or record that it stays private.
- Consider S1 to S3, and R456-1 S1 as a new Issue.
- Hosted and act acceptance at the exact head, and the current-dev candidate build at the merge turn.
- A fresh review of the corrected head under Conformance, Tests and Docs. RTL and Robustness are covered clean at this head and stay covered while nothing in their scope changes.

## Receipts

- **Scripts:**
  - `scripts/r1-unchanged/`: R456-1's scripts, byte-identical.
  - `scripts/r2_builds.sh` and `scripts/r2_runs.sh`: the probe builds and the run batches. The builds use R456-1's edit strings verbatim, plus the probes marked NEW.
  - `scripts/r2_suite_lane.sh`: runs the published diagnostic, then the default target.
  - `scripts/r2_summarize.py`: writes `receipts/summary.txt`.
- **Inputs:** `inputs/` holds the two adoption patches, byte-identical to the public evidence.
- **Suites:** `receipts/suites/` holds `bnd-*.log` (the published diagnostic) and `suite-*.log` (the default target), each with an `.rc` file, at both processors. Home-directory paths are replaced by placeholders.
- **Probes and builds:** `receipts/probes/` holds every probe log with its `.rc` and the batch lists. `receipts/builds/` holds the build receipts. Where two lanes built the same probe name in different trees they share one `.rc`; the lane logs carry each result.
- **Other receipts:** `receipts/summary.txt`, `environment.txt`, `clone-state.txt`, `gates.log`, `gates-md.log`, `arg-parsing.log`, `check_mutant_verdict.log`, `setpoint-arm-verdicts.log` and `hosted-snapshot.tsv`.
- **Clone state** (`receipts/clone-state.txt`):
  - the review clone is at the exact head and byte-clean, with 0 status entries including ignored files;
  - the index's (mode, blob, path) set hashes the same as HEAD's tree;
  - gitlinks: protocol-processor `631eeb34`, gptp-processor `5dce647a`, third_party/verilog-axis `48ff7a7e`, external `efeb541a`;
  - I removed two `__pycache__` directories left by an offline import, and deleted a temporary ref I had used to read the public evidence branch.

R456-2 FINISHED
