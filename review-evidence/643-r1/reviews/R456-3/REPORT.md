[R456] POSITIVE - exact head 36207e91c81fd33782b01486e3bc2fea50e91a1e

# R456-3: internal cleared-context review of #643 / PR #648, round 3

- **Head:** `36207e91c81fd33782b01486e3bc2fea50e91a1e`, tree `efadbdb9b540bb8c78a8d707557c65f936052579`.
- **Round-3 delta:** `6b96391d..36207e91`, two commits, each one line with no trailer:
  - `ca3db9f3`: code. `sim_tdm8_render.cpp` (the walk measure, the window constant, two print lines, a comment, the ceiling check's name) and `tdm8_render_mutants.py` (the per-window walk print, the largest-walk line, the verdict-line quoting, the usage text).
  - `36207e91`: docs only. `MEDIA_CLOCK_FOLLOWING.md`, `TESTING.md` and `tb/verilator/README.md`.
- **Lane against live dev `241f9184`:** the same seven files as round 2. No file under `hdl/` changes and no gitlink changes.
- **Scope reconstructed from:**
  - `AGENTS.md`, the #643 body (frozen acceptance);
  - the lane assignment (5972861856), the item-1 STOP (5973437153), the ruling (5973450039), the round-2 ruling (5974715857), the round-3 assignment (5976170456) and REVIEW READY round 3 (5977016377);
  - the PR body at the head;
  - the author's public round-3 archive (`643-review-evidence` at `8a1fe1f0`: `author-r3/round3-boundary-walks.md`, `HANDOFF.md`, `PR-BODY.md`);
  - my own round-2 report and scripts.
- **Verdict:** POSITIVE. No BLOCKER, MAJOR, MINOR or RESIDUE is open.
  - My round-2 MINOR (R456-2-F1, the stated walk) is resolved. The walk is now the nearest-pop range, as the design page defines it. S = 5 and W = 9 are what the head measures, and both outputs print them.
  - Every round-3 item is met, and I reproduced each one at both processors.
  - All five lenses were applied at this head and are clean.

## Findings

No BLOCKER, MAJOR, MINOR or RESIDUE.

### Suggestions (non-blocking)

- **R456-3-S1 (Docs, Robustness): the wrap branch is reachable, and was exercised.**
  - `MEDIA_CLOCK_FOLLOWING.md:1379-1381` says no measured window sits where the nearest pop changes side.
  - That was true of the lane's windows. A new probe in this round scans +975..+995, half a tick from the boundary, at both processors (`hp-/c4-clean-lb-975up`). At +983 and +984 the nearest pop changes side, with offsets -1041..+1042. The branch prints its suffix, and `walk()` reports 2, the first-pop-after range (+1042..+1044 and +1041..+1043). That agrees with the histogram (`-1041:19 -1040:106 -1039:9 1042:3`). Both windows are graded PASS, with clearance 1039 and 1040.
  - Optionally, the sentence could cite these windows as evidence that the branch works.
- **Retained, still optional (all listed as open in the PR body):**
  - R456-2-S2 (= R457-2 S2): check the measured walk against `kLawWalkCycles`. My unchanged ablations still pass the sound design at W = 5 (`w4`) and W = 1 (`w0`) and fail both setpoint defects wherever they grade. A walk that grew past 5 would show up only in the printed lines.
  - R456-1-S1 (= R457-1 S3): the accept-pulse instrument in `milan_dp`, as a candidate new Issue.
  - R456-1-S2: require the stage's counters to stay unchanged across each graded window.

## Round-3 focus items, verified

| Item | Result | Evidence |
|---|---|---|
| `walk` is the range of the end-to-nearest-pop offset over each window, as `MEDIA_CLOCK_FOLLOWING.md:1376-1381` defines it | **Yes** | `sim_tdm8_render.cpp:1449-1452`: `walk()` is `dmax - dmin`, the nearest pop's range. Only when that range exceeds half a tick does it use `nmax - nmin`, the first pop after. `offsets_at_pdu_ends` (`:3183-3203`) takes `delta` from `pop_nearest_the_end` (`:736-750`) over the steady ends only. Over every window line in this round's logs, the printed walk equals the printed nearest-pop range, or on the 4 wrap lines the first-pop-after range: 0 mismatches (`receipts/walks.txt`). In round 2 there were 89 mismatches. |
| S = 5 at dev's pin, from the CRF window at -592..-587, is supported by the published `[LAW]`, CRF and boundary windows at both processors | **Yes** | **CRF, dev's pin:** "the pop nearest the boundary -592..-587 (walk 5) ... clearance 587 ... margin 578" (`suites/suite-p631.log`, `probes/hp-crfhist-full.log:23`). The histogram is `-592:3 -591:32 -590:54 -589:71 -588:106 -587:26`, six offsets (`hp-crfhist-full.log:24`), so my round-2 `crfhist` agrees with S = 5. **CRF, `c4cb84ff`:** +336..+340, walk 4, margin 326 (`suite-c4c.log`, `c4-crfhist-full.log:23-24`). **`[LAW]`:** at most 3 over every settled window, and at most 2 in the 18 standing phases. **Boundary:** all 564 windows of my `tdm8render-law-boundary` run match `round3-boundary-walks.md` cell for cell at both processors: range, walk, clearance and outcome, 0 differences (`receipts/compare-published.log`). **Larger walks:** walks above 5 occur only where the settled hold failed: A2-a removed, walk 18 at all 18 phases; no dwell, walk 11 and 6. Each of those windows fails "the aligner held its settled report" (`hp-a2a-law`, `hp-bootnodwell-law`). |
| W = S + 4 = 9 everywhere (suite comment, design page, README, TESTING, PR body Known limitations) | **Yes** | `sim_tdm8_render.cpp:184-199` (`kLawWalkCycles = 5`, guard 4); the leg prints "the ambiguity window is 9 cycles: a walk of 5 plus a guard of 4" (`:3502-3505`); `MEDIA_CLOCK_FOLLOWING.md:1371` ("up to 5"), `:1385-1394` (5 and 3, "9 cycles"); `tb/verilator/README.md:63` ("9-cycle"); `TESTING.md:521` ("the 9-cycle ambiguity window"); the PR body's Status, Round 3 table, expected results and Known limitations ("W = 9 ... 5 ... plus a guard of 4"). No "8-cycle" and no "walk of 4" remains in the lane's files. |
| Every standing window (18 `[LAW]` phases and the T30 CRF window) stays gradable at W = 9, and its stated margin matches the log | **Yes** | **Full leg:** every window is gradable. +0 has clearance 57, margin 48, at both processors (`suite-p631.log`, `suite-c4c.log`); the next nearest, +1953, has margin 62. **`--law-only`:** +0 has clearance 56, margin 47, at both (`hp-clean-law`, `c4-clean-law`). **CRF:** 578 at dev's pin, 326 at `c4cb84ff`. These are the figures in `MEDIA_CLOCK_FOLLOWING.md:1397-1400` and the PR body. **Placement:** under `--crf-only` the CRF window's nearest pop is at -1018 (dev's pin, margin 1009) and -91 (`c4cb84ff`, margin 82), as the page and the PR body say (`hp-/c4-clean-crf`). **The check fails when it should:** with W widened past every clearance (`crfw1104`), "T30 CRF LAW: gradable" fails by name and its law checks are not run (50/1). At W = 9, the standing list +2018..+2035 (`tieon`) fails "gradable" at all 18 phases, at both processors (52/18). |
| Setpoint -1 and +1 still fail every graded standing phase | **Yes** | `hp-spm1-law`, `hp-spp1-law`, `c4-spm1-law` and `c4-spp1-law` each read 106 checks with 36 failing: exactly the fill and band checks at all 18 phases. The campaign's own `verdict()` reads all four as `caught` against their 36-name targets, A2-a as `caught` at both processors (19 failing: 18 settled checks plus the ceiling check), and the clean logs as `pass` (`receipts/setpoint-arm-verdicts.log`). Under `--crf-only` both defects fail the CRF fill and band checks. |
| `tdm8render-law-boundary` prints each window's walk and nearest-pop range, and the largest walk | **Yes** | I ran the published target as `TESTING.md` documents it, from the suite directory. It exits 0 at both processors with `81 checks: 81 PASS, 0 FAIL` (`suites/bnd-p631.log`, `bnd-c4c.log`). It prints 564 per-window lines, `+<phase>: <outcome>; the pop nearest the boundary <lo>..<hi> (walk <w>), least clearance <c>`, under their verdict lines (`tdm8_render_mutants.py:808-811`). It ends with "the largest walk over 564 windows is 3 cycles (the unmutated gateware, descending, +2066); the leg states a walk of 5" (`:771-783`). Not gradable: ascending +2015..+2035, descending +2016..+2036, alone +2015..+2037, the same at both processors and as published. The window parser accepts `+0`, signed offsets and the wrap suffix, and ignores the CRF and histogram lines (`receipts/runner-checks.log`). |
| The taken suggestions are as described, and the open ones are listed in the body | **Yes** | R456-2-S1, stated: `sim_tdm8_render.cpp:3422-3424` and `MEDIA_CLOCK_FOLLOWING.md:1400-1403`. R456-2-S3: `:1404-1414`. R456-2-S4: `tdm8_render_mutants.py:687-696`; stubbed `run_mutations` prints `breaks "check A" and 2 more` with no stray quote (`runner-checks.log`). R457-2 S1: `TESTING.md:270`, `:523`, the runner's usage (`:80-82`); no `make -C ... tdm8render-mutants` or `-law-boundary` invocation remains. R456-1-S3: the check now reads "inside the declared 32768-tick ceiling, counted from this wait's start" (`:3488-3490`), which matches the wait (`:3478-3483`); the design-page row (`:1329`) says the same. Open in the body: R456-2-S2 = R457-2 S2, R457-2 S3, R456-1-S2, R456-1-S1 = R457-1 S3. |
| #643's frozen acceptance still holds | **Yes** | An 18-phase sweep over one grid tick, including +927 and +1156, graded only after the settled report: wait 0 ticks in the full leg, 4014 in `--law-only`, with each phase's hold checked. It passes at both processors. A2-a removed fails all 18 phases at both. The base harness still reproduces #643's failure at `c4cb84ff` (227/292, 285/292) and passes at `631eeb34` (`c4-base-full`, `p631-base-full`). |
| "In every graded window measured the first event landed at least 10 cycles inside both edges" (`MEDIA_CLOCK_FOLLOWING.md:1418-1419`) | **Yes** | Over every graded sound-design window in this round's W = 9 logs, the least margin is 10.00 cycles: +2037 descending at `c4cb84ff`, delays 18740..18741 against an upper edge of 18751 (`walks.txt`). |
| My round-2 probes, rerun unchanged | **Yes** | `scripts/r2_builds.sh`, `r2_runs.sh` and `r2_suite_lane.sh` are byte-identical to the R456-2 packet. `scripts/r1-unchanged/` is byte-identical too. The archive stores every file as 100644, so I set the executable bit on the seven `.sh` files locally; the build wrapper `vl_jobs.sh` is executed directly. Every edit anchor still matches, except the three tie-code probes. `tieoff`, `tietr18` and `tietr36` refuse to build, as in round 2 ("edit pattern matches 0 times"). None of my probes edits the restated walk line, so no edit had to be applied by hand. Outcomes that changed with W = 9 are expected, not regressions. +2035 has clearance 9, so `tieon` and `tiespp1`/`tiespm1` now read 52/18 (round 2: 55/17 and 55/19), and the +2018 setpoint -1 history has no graded phase left (`hp-/c4-spm1-lb-2018up`). In the guard ablations, guard 0 is now W = 5 and guard -4 is W = 1. |

## Lens results

[R456] PASS Conformance - round-3 assignment 5976170456 items 1-4 against sim_tdm8_render.cpp:184-199,1440-1453,3236-3265,3502-3505 and receipts/suites/suite-p631.log, suite-c4c.log, bnd-p631.log, bnd-c4c.log, probes/hp-crfhist-full.log:23-24 - S = 5 is the head's own nearest-pop range for the CRF window at 631eeb34; W = 9; all 19 standing windows are gradable with the stated margins (47/48, 578, 326); setpoint +/-1 fail 36/36 and A2-a 18/18 at both processors; the diagnostic prints every walk and the largest; #643's frozen acceptance still holds.

[R456] PASS RTL - hdl/ and the gitlinks (0-line diff 241f9184..36207e91 and 6b96391d..36207e91); the harness taps unchanged by the delta (pop_take = pulse cycle - 1 at sim_tdm8_render.cpp:718-719, observe_pdu_end, pop_nearest_the_end :736-750); EndOffsets::walk_wraps :1449-1451 - no RTL or interface change. The new branch compares a long range, converted to double, against the fractional tick (2083.33 cycles), with no truncation or overflow. It selects the unwrapped range exactly when the nearest pop changes side, as exercised at +983/+984 on both processors.

[R456] PASS Robustness - sim_tdm8_render.cpp:1449-1452,3240-3250; tdm8_render_mutants.py:482-485,764-811; probes/hp-/c4-clean-lb-975up, hp-/c4-clean-crf, hp-crfw1104-crf, hp-a2a-law, hp-bootnodwell-law, c4-clean-lb-up/down - the wrap path is exercised at both processors and handled; the CRF window is measured at four positions (two pins, full leg and --crf-only) and fails by name when widened past them; history dependence in four histories leaves boundary phases NOT GRADABLE, never graded wrong; moving-grid windows (walk 6 to 18) all fail their settled hold; the runner's parser survives the wrap suffix, +0 and the CRF and histogram lines (runner-checks.log). The argument-refusal paths are unchanged by the delta.

[R456] PASS Tests - receipts/suites/*, receipts/probes/*, setpoint-arm-verdicts.log, runner-checks.log, check_mutant_verdict.log, compare-published.log - the suite passes at both processors (245/0, 65/0, leg defects 5/5); setpoint -1/+1 fail exactly the 36 law checks and the campaign's verdict() calls them caught; A2-a is caught at both; the diagnostic is 81/81 at both and identical to the published 564 windows; the standing gradable check is shown to fail for [LAW] (tieon) and for CRF (crfw1104); the new print lines and the verdict-line quoting are unit-checked; check_mutant_verdict 7/7.

[R456] PASS Docs - MEDIA_CLOCK_FOLLOWING.md:1329-1330,1356-1420; TESTING.md:270,521,523; tb/verilator/README.md:63; sim_tdm8_render.cpp:184-199,1433-1439,3422-3424; tdm8_render_mutants.py:70-83,464-469; the PR body at 36207e91 - every figure (5, 3, 4, W = 9, margins 47/48/578/326, -1018/-91, at least 10 cycles) matches this round's logs; no stale 8-cycle or make -C campaign text remains. Docs gates rc 0 (receipts/gates.log): docs_check, check_doc_style, check_doc_paths, check_em_dash --base 241f9184 (0 findings over 94 added lines) and --base 6b96391d (0 over 37), gen_toc --check and --verify-anchors; code gates check_cpp_idiom, check_py_idiom and check_hygiene rc 0.

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | the #643 body; rulings 5973450039, 5974715857; round-3 assignment 5976170456; REVIEW READY 5977016377; the window, walk, gradability, `[LAW]` and `--law-boundary` code in `sim_tdm8_render.cpp`; suite, probe and diagnostic receipts at both processors; the published `round3-boundary-walks.md` | R456-3 | `36207e91c81fd33782b01486e3bc2fea50e91a1e` |
| RTL | CLEAN | the `hdl/` and gitlink diff (none); the harness taps the delta did not touch; `EndOffsets::walk_wraps`/`walk` types and threshold | R456-3 | `36207e91c81fd33782b01486e3bc2fea50e91a1e` |
| Robustness | CLEAN | the wrap path at +983/+984 at both processors; the CRF window at four positions and widened past them; four boundary histories; moving-grid windows; the runner parser's edge inputs | R456-3 | `36207e91c81fd33782b01486e3bc2fea50e91a1e` |
| Tests | CLEAN | the suite at both processors; `--law-only` clean, A2-a and setpoint +/-1 at both; setpoint +/-1 under `--crf-only`; the published diagnostic at both, compared cell by cell with the published table; the W ablations; the standing gradable-failure probes; `verdict()` on the arm logs; runner unit checks | R456-3 | `36207e91c81fd33782b01486e3bc2fea50e91a1e` |
| Docs | CLEAN | the `MEDIA_CLOCK_FOLLOWING.md` test rows and the grading-instant section; `TESTING.md:270,521,523`; `tb/verilator/README.md:63`; the suite and runner comments; the PR body; docs and code gates | R456-3 | `36207e91c81fd33782b01486e3bc2fea50e91a1e` |

## Prior public review findings, resolved or retained at this head

| Finding | Status at `36207e91` | Evidence (this round) |
|---|---|---|
| R456-2-F1 MINOR: the stated walk S = 4 came from `walk()`, the smaller of two ranges | **Resolved** | `walk()` is the nearest-pop range (`:1449-1452`). The CRF line at dev's pin reads "-592..-587 (walk 5)". S = 5 and W = 9 are stated in the code, the design page, the README, TESTING and the PR body. The diagnostic prints every walk and the largest. 0 lines anywhere where the walk disagrees with its own range. |
| R457-2-F1 MINOR (= R456-2-F1): the stated spread S (4) understates the CRF window's nearest-pop walk (5) | **Resolved** | Its verification holds at this head. The default target at `631eeb34` prints the T30 CRF LAW walk equal to its nearest-pop range, "-592..-587 (walk 5)" (`suite-p631.log`). The code comment (`:184-199`, `:1433-1439`), `MEDIA_CLOCK_FOLLOWING.md:1367-1394` and the PR body state 5 and W = 9. The docs gates pass. Its "one fix" is the one taken: the nearest pop's range unless it wraps (`:1449-1452`). |
| R456-1-F1 MAJOR / R457-1-F1 MINOR: the tie rule's one-cycle premise | **Still resolved** | No tie code at the head: three probes refuse because their anchors are gone. Boundary phases come out NOT GRADABLE in every history, never graded wrong. |
| R456-1-F2 / R457-1-F2 MINOR: `TIME_SYNC.md:451` read at the accept pulse | **Still resolved** | `TIME_SYNC.md` is unchanged since round 2 (`:451-455`, the PDU end). |
| R456-2-S1, S3, S4; R456-1-S3; R457-2 S1 | Taken | Focus table, last row but two. |
| R456-2-S2 = R457-2 S2; R457-2 S3 (the CRF window still checks "at least 100" PDUs: `expect_n` 0 at the T30 CRF LAW call, `:3425-3427`; it measured 292 at both processors); R456-1-S1 = R457-1 S3; R456-1-S2 | Retained, optional | Listed as open in the PR body. |
| R457-2 S4 (not a finding): the hand-off cites evidence that is not in the public packet | Still applies | The round-3 hand-off cites `law-boundary-scan.md` and the lane's suite, campaign and diagnostic logs. The public round-3 archive (`8a1fe1f0`) holds only `HANDOFF.md`, `PR-BODY.md` and `round3-boundary-walks.md`. My conclusions rest on my own receipts and on the published table, which I reproduced exactly. |

## Real limits

- **Make version and wall times.** GNU make 4.3 is not installed on this host, so every build used GNU make 4.4.1, from inside the suite directory where the documented commands require it. The host was shared (load average 55 to 78). The default target took 689 s (dev's pin) and 710 s (`c4cb84ff`), after the diagnostic had built its elaboration, and the diagnostic took 3345 s and 3250 s at five legs. These are not cold figures.
- **Campaign not run in full.** I did not run `tdm8render-mutants` (32 checks; the author reports rc 2 on four pre-existing arms). This round changes only its verdict-line quoting, which I unit-checked with the build and leg stubbed out. I reproduced the arms the lane adds (A2-a and setpoint +/-1) directly at both processors and judged them with the campaign's own `verdict()`.
- **The published diagnostic's temporary tree.** The runner builds its setpoint defects in the system temporary directory, not under my scratch directory. Both trees were gone when it exited.
- **Alone history.** The +/-40 alone runs of the round-2 item-1 scan are the author's. The published target runs +/-12 alone. My own alone runs are the 12 unchanged round-2 points.
- **Processor `c4cb84ff`** ran only in scratch clones, with the gitlink set in the index and both adoption patches applied, never committed.
- **Not run:** Yosys; the parent, processor, gPTP and builder banks; `act`; Docker; physical calibration; hardware. Field skips are not hardware proof.
- **Hosted state, read-only snapshot at 07:02 UTC** (`receipts/hosted-snapshot.tsv`):
  - success: rtl-fast, verilator-suites, yosys-portability, Verilator shards 0-4, Yosys shards 0-3, yosys-elaboration, elaborate, verilator-lint, bdd-conformance, changes, wire-accountability, docs-check, docs-check-no-git and full-ci-gate;
  - skipped: the physical gPTP context. A skip is not an executed result.
  - Acceptance of the hosted and act evidence is the manager's.

## Pending manager duties

- Hosted and act acceptance at the exact head, and the current-dev candidate build at the merge turn (source base `5fabb46e`, live dev `241f9184`).
- No RESIDUE to carry.
- Publish the evidence the round-3 hand-off cites but the archive lacks (`law-boundary-scan.md` and the suite, campaign and diagnostic logs), or record that it stays private (R457-2 S4).
- Consider the optional suggestions: R456-3-S1, R456-2-S2, R456-1-S2, and R456-1-S1 as a new Issue. The pre-existing `make -C` Makefile defect and the campaign's four pre-existing failing arms are listed in the PR body for new Issues and are still unfiled.

## Receipts

- **Scripts** (`scripts/`):
  - `r1-unchanged/`, `r2_builds.sh`, `r2_runs.sh`, `r2_suite_lane.sh` and `r2_summarize.py`: my round-2 scripts, unchanged.
  - `r3_setup_trees.sh`: the scratch clones.
  - `r3_launch.sh`: the lane launcher.
  - `r3_runs.sh`: batch B5, round 2's ad hoc runs plus the NEW +975..+995 and `--crf-only` runs.
  - `r3_gates.sh`: the static gates.
  - `r3_runner_checks.py`: the runner unit checks.
  - `r3_setpoint_verdicts.py`: `verdict()` on the arm logs.
  - `r3_walks.py`: the walk re-measure and band margins.
  - `r3_compare_published.py`: the comparison with the published table.
- **Inputs** (`inputs/`): the two adoption patches, byte-identical to the public evidence.
- **Suites** (`receipts/suites/`): `bnd-*.log` is the published diagnostic and `suite-*.log` the default target, each with an `.rc` file, at both processors.
- **Probes and builds:** `receipts/probes/` holds every probe log with its `.rc` and the batch lists. `receipts/builds/` holds the build receipts; where two trees built the same probe name they share one `.rc`. `receipts/lanes/` holds each lane's log and rc.
- **Other:** `receipts/summary.txt`, `walks.txt`, `compare-published.log`, `runner-checks.log`, `check_mutant_verdict.log`, `setpoint-arm-verdicts.log`, `gates.log`, `environment.txt`, `setup-trees.log`, `clone-state.txt` and `hosted-snapshot.tsv`.
- **Path redaction:** home-directory paths in the receipts are replaced by `<home>` before hashing. `MANIFEST.sha256` hashes the files as published.
- **Clone state** (`receipts/clone-state.txt`):
  - the review clone is at the exact head and byte-clean, with 0 status entries including ignored files;
  - the index tree equals HEAD's tree `efadbdb9`, and the index's (mode, blob, path) set hashes the same as HEAD's;
  - gitlinks: protocol-processor `631eeb34`, gptp-processor `5dce647a`, third_party/verilog-axis `48ff7a7e`, external `efeb541a`; the three initialized submodules are clean;
  - the code gates ran in the clone with bytecode writing off. I removed the temporary ref I used to read the public evidence branch.

R456-3 FINISHED
