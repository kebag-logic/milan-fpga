[R457] POSITIVE - exact head 36207e91c81fd33782b01486e3bc2fea50e91a1e

# R457-3: external review of #643 / PR #648, round 3

- **Head under review:** `36207e91c81fd33782b01486e3bc2fea50e91a1e`, tree `efadbdb9b540bb8c78a8d707557c65f936052579`.
  - Source base: dev `5fabb46e767c9308ab2580916237f43577698c6e`.
  - Live dev: `241f91845230ae410506dffb16b71937127fd175`, already merged. The merge-base of the head and live dev is `241f9184`.
  - Processor pin: `631eeb34`.
  - Second processor: `c4cb84ff`, in a scratch parent with both adoption patches, never committed.
- **Round:** R457-3, external, cleared context. It ran from the [review start](https://github.com/kebag-logic/milan-fpga/pull/648#issuecomment-5977028664).
- **Context reconstructed from:**
  - `AGENTS.md`;
  - the #643 body and these issue comments:
    - the [lane assignment](https://github.com/kebag-logic/milan-fpga/issues/643#issuecomment-5972861856);
    - the [ruling 5973450039](https://github.com/kebag-logic/milan-fpga/issues/643#issuecomment-5973450039);
    - the [round-2 ruling 5974715857](https://github.com/kebag-logic/milan-fpga/issues/643#issuecomment-5974715857);
    - the [round-3 assignment 5976170456](https://github.com/kebag-logic/milan-fpga/issues/643#issuecomment-5976170456);
    - the round-3 REVIEW READY (5977016377);
  - the PR #648 body at this head. It is byte-identical to the archived `author-r3/PR-BODY.md` except for a trailing newline;
  - the diff `6b96391d..36207e91`: two one-line commits, `ca3db9f3` (code) and `36207e91` (docs). For scope, `5fabb46e..36207e91`;
  - the public evidence on `643-review-evidence` at `8a1fe1f0`:
    - `review-evidence/643-r1/author`, `author-r2` and `author-r3` (`HANDOFF.md`, `PR-BODY.md`, `round3-boundary-walks.md`);
    - my own R457-2 packet.
- **Prior public findings:** I read R456-1 (5974712082) and R456-2 (5976136338) only after my own pass over the diff, the probes and this report's verdict and ledger were written. My own rounds are R457-1 (5974627143) and R457-2 (5976168264).

## Verdict in one paragraph

Round 3 does what the round-3 assignment asked, and I reproduced it at both processors.

- **The walk is measured as defined.** `EndOffsets::walk()` is now the nearest-pop range over the window's steady ends (`sim_tdm8_render.cpp:1449-1452`). Only when that range exceeds half a tick does it take the first-pop-after range, and the line then says so.
  - No published window reaches that branch. My new probe does: at +983 and +984 the nearest pop changes side (`-1041..+1042`).
  - There the walk is printed as 2 with the stated suffix, at both processors.
- **S = 5 is right.** At dev's pin the CRF window prints `-592..-587 (walk 5)`; at `c4cb84ff`, `+336..+340 (walk 4)`. No sound `[LAW]` window walks more than 3, over 558 windows and 1,128 diagnostic window lines across my logs.
- **W = 5 + 4 = 9 everywhere:**
  - the suite comment and the constant;
  - the leg's own `[LAW-BOUNDARY]` header;
  - the design page, the README and both TESTING rows;
  - the PR body.
- **Every standing window is gradable at W = 9.** The margins match the published figures exactly: the least is 47 (`--law-only`) and 48 (full leg) at +0; the CRF window's is 578 and 326.
- **Setpoint −1 and +1 still fail** fill and band at all 18 standing phases at both processors.
- **The diagnostic re-measures the window.** It prints every window's nearest-pop range, walk and clearance, then "the largest walk over 564 windows is 3 cycles …; the leg states a walk of 5". All 376 cells of the published table equal my run's.

My round-2 MINOR (R457-2 F1) is resolved. One RESIDUE remains: the PR body cites as published an evidence file that is not in the public archive. It changes no figure, and it is recorded with its fix below. The verdict is POSITIVE.

## Findings

### RES-1: RESIDUE. Lens: Docs. The PR body counts round 2's 486-window scan among "published" windows, but its file is not in the public archive

- **Where:**
  - The PR body, Round 3, item 1: "Re-derived from every published window (1,903 in both round-2 review packets, and round 2's 486-window scan)".
  - `author-r3/HANDOFF.md` R3.4: "R457-2 S4: `law-boundary-scan.md` not in the public packet | For the manager: it is in this directory".
- **Evidence:**
  - `643-review-evidence` at `8a1fe1f0` holds no `law-boundary-scan.md`: no path in `git ls-tree -r` matches.
  - `author-r2/` holds only `HANDOFF.md` and `PR-BODY.md`. `author-r3/` holds those two and `round3-boundary-walks.md`.
  - `author-r2/HANDOFF.md` cites the same file ("Every row, with its offset histogram, is in `law-boundary-scan.md`").
- **Why RESIDUE and not MINOR:** no figure rests on the missing file.
  - S = 5 comes from the CRF window, which is published: my R457-2 `receipts/suite-head.log:479`, and this round's `receipts/suite-head.log:479`.
  - "At most 3 in a `[LAW]` window" is published in `round3-boundary-walks.md` (564 windows per processor), which my run reproduces cell for cell.
  - Only the word "published" is wrong, for one parenthetical source.
- **Exact fix (either):**
  - The manager publishes `law-boundary-scan.md` beside `round3-boundary-walks.md` under `review-evidence/643-r1/author-r3/`.
  - Or the parenthetical reads "(1,903 in both round-2 review packets; round 2's 486-window scan, `law-boundary-scan.md`, is held by the executor and not published)".
- **Verification:** `git ls-tree -r <evidence head> | grep law-boundary-scan.md`, or read the reworded PR body.

### Suggestions (non-blocking)

S1 and S2 are retained from round 2, and the PR body lists them as open.

- **S1 (= R457-2 S2). Lens: Tests.** No check compares a window's measured walk with `kLawWalkCycles`.
  - Round 3 made the comparison visible: the diagnostic prints the largest walk beside the stated one.
  - But nothing fails if a sound window's walk outgrows 5.
- **S2 (= R457-2 S3). Lens: Tests.** The T30 CRF LAW window still checks "at least 100" PDUs (`sim_tdm8_render.cpp:3425-3427`, `expect_n` 0). It measured 292 at both processors.
- **S3. Lens: Docs.** `MEDIA_CLOCK_FOLLOWING.md:1376-1381` says no measured window sits where the nearest pop changes side.
  - My probe found two: +983 and +984 (`receipts/wrap-*.log`).
  - The text is accurate for the executor's data, and the branch does what the page says.
  - When the page is next touched, it could cite those two phases as the measured instance.

## Round-3 focus items, verified

| Item | Result | Evidence |
|---|---|---|
| `walk` is the range of the end-to-nearest-pop offset, as `MEDIA_CLOCK_FOLLOWING.md` "The walk" defines it | Yes | **The code.** `sim_tdm8_render.cpp:1433-1453`: `walk_wraps()` is `2*(dmax-dmin) > kTickCycles`, and `walk()` is `dmax-dmin` unless it wraps. The steady-end filter (`:742-749`, `:3178-3203`) matches the page's "a pop within two ticks on each side".<br>**The audit.** `scripts/walk_audit.py` checks every offsets line:<br>• the walk equals the nearest-pop range;<br>• in `--law-boundary` legs, the histogram spans that range and sums to the steady ends;<br>• NOT GRADABLE iff clearance ≤ 9;<br>• margin = clearance − 9.<br>Over 4 CRF, 558 sound `[LAW]` and 248 defect `[LAW]` windows, and 1,128 runner window lines, it finds 0 problems (`receipts/walk-audit.txt`).<br>**Its negative control.** The same script reports 222 problems on my round-2 logs, including `CRF walk 4 != range 5` (`receipts/walk-audit-selftest-r2.txt`).<br>**`walks.py`, unchanged:** 0 windows whose nearest-pop range exceeds the reported walk, against 49 in round 2 (`receipts/walks.tsv`). |
| The wrap branch | Correct where it fires; never reached by a standing window | A new probe, `--law-boundary=974..994`, at both processors (`receipts/wrap-{head,c4}.log`, rc 0, 100/0).<br>• At +983 and +984 the nearest pop is `-1041..+1042`. The histogram at +984 is `-1041:31 -1040:7 1041:1 1042:98`.<br>• The walk prints the first-pop-after range, 2, with "; the nearest pop changes side half a tick from the grid, so the walk is the first pop after's range".<br>• At +982 and +985 it prints the nearest-pop range.<br>• Clearance is about 1,040, and the windows are graded PASS. |
| S = 5 at dev's pin (CRF −592..−587) is supported by the [LAW], CRF and boundary windows at both processors | Yes | **CRF, dev's pin.** `receipts/suite-head.log:479`: `-592..-587 (walk 5)`, clearance 587, margin 578, 292 PDUs, fill 14..14.<br>**CRF, `c4cb84ff`.** `suite-c4.log:488`: `+336..+340 (walk 4)`, margin 326.<br>**`[LAW]`, sound.** The largest walk is 3, at the boundary only. The standing phases walk at most 2.<br>**`--crf-only`** (`crfonly-*.log`): −1021..−1018 (walk 3), and −94..−91 (walk 3, margin 82).<br>**Above 5.** Walks above 5 occur only in defects whose grid moves: the A2-a arm (18) and the no-dwell probe (11). |
| W = S + 4 = 9 everywhere | Yes | • `sim_tdm8_render.cpp:184-199`: `kLawWalkCycles = 5`, guard 4, `kLawAmbiguityCycles` = 9.<br>• The leg's header (`:3502-3505`): "the ambiguity window is 9 cycles: a walk of 5 plus a guard of 4". The diagnostic reads it back as "the leg states a walk of 5".<br>• `MEDIA_CLOCK_FOLLOWING.md:1371`, `:1382-1394`.<br>• `tb/verilator/README.md:63` and `TESTING.md:521`, both "9-cycle".<br>• The PR body's Status and Known limitations ("W = 9 is the largest walk measured, 5 … plus a guard of 4").<br>No 8-cycle or walk-of-4 wording remains in `docs/`, the README or the suite. |
| Every standing window (18 `[LAW]` + CRF) is gradable at W = 9, and its stated margin matches the log | Yes, at both processors | **Margins** (`receipts/standing-margins.txt`, from `suite-*.log` and `lawonly-*.log`):<br>• least 48 (+0, full leg) and 47 (+0, `--law-only`);<br>• +1953: 62 and 63;<br>• CRF: 578 (dev) and 326 (`c4cb84ff`).<br>Every "gradable" check passes (245/0, 106/0), and all 19 rows equal the hand-off's R3.1 table.<br>**The window-fault probe** applies the one edit `kLawGuardCycles` 4 → 2100 by hand (`scripts/probe-window-wider-than-a-tick-r3.patch`). It fails exactly the 19 "gradable" checks and skips every law check (245 → 188 checks), rc 1 (`probe-wfault-full.log`). |
| Setpoint −1 and +1 still fail every graded standing phase | Yes, both processors | **The campaign's own arms.** Through its `plant`, `build`, `run_leg` and `verdict` (`scripts/law_arm.py`, unchanged), `arm-{head,c4}-sp-{low,high}` are `caught`: 36 `[FAIL]` lines each, 0 named checks not failing.<br>**The probe builds.** `sp-std` and `sphi-std` fail fill 18/18 and band 18/18. +2,025 and +2,026 are NOT GRADABLE.<br>**A2-a:** `caught` at both, with 19 `[FAIL]` (18 settled checks plus the ceiling). |
| `tdm8render-law-boundary` prints each window's walk and nearest-pop range, and the largest walk | Yes | `receipts/lb-{head,c4}.log`, run from the suite directory with `LAW_BOUNDARY_JOBS=4`. rc 0, 81/81 at both processors.<br>**The window lines.** The verdict and window lines are byte-identical between processors. Each run prints 564 window lines:<br>• 123 graded PASS, all sound;<br>• 246 graded FAIL, all defects;<br>• 195 NOT GRADABLE.<br>**The summary.** Both end with "the largest walk over 564 windows is 3 cycles (the unmutated gateware, descending, +2066); the leg states a walk of 5".<br>**NOT GRADABLE bands,** as the PR body states: +2,015..+2,035 ascending, +2,016..+2,036 descending, +2,015..+2,037 alone.<br>**The published table** (`scripts/compare_walks_table.py`, `receipts/walks-table-compare.txt`):<br>• all 376 cells of `round3-boundary-walks.md` equal my run's;<br>• in every history the defects' windows carry the sound design's ranges;<br>• no defect window is graded PASS. |
| A graded window lands "at least 10 cycles inside both edges" (`MEDIA_CLOCK_FOLLOWING.md:1415-1420`) | Yes, against the graded band (8T, 9T + 1] | Over 402 sound graded windows (`walk-audit.txt`):<br>• the least lower-edge margin is 12.33;<br>• the least upper-edge margin is 10.00 to 9T + 1, which is 9.00 to 9T itself. |
| Taken suggestions as described | Yes | • **The CRF span sentence:** `sim_tdm8_render.cpp:3422-3424` and the page's `:1399-1403`.<br>• **The CRF-gradability paragraph:** the page's `:1404-1414`.<br>• **The stray quote:** `tdm8_render_mutants.py:687-696`. I exercised the formatting offline for a string and a tuple.<br>• **`make -C`:** no `make -C … tdm8render-mutants` or `make -C … tdm8render-law-boundary` remains in any `.md`, `.py`, Makefile or workflow outside the submodules. `TESTING.md:270`, `:523` and the runner's usage (`:76-82`) say "from inside the suite directory".<br>• **The ceiling check's name:** `sim_tdm8_render.cpp:3488-3490` and `TESTING.md:521`. |
| The open suggestions are listed in the body | Yes | PR body, Round 3 item 4, "Open:": R456-2 S2 = R457-2 S2; R457-2 S3; R456-1 S2; R456-1 S1 = R457-1 S3.<br>R457-2 S4 (publish the scan file) is passed to the manager in the hand-off, not in the body. That is RES-1. |
| My round-2 probes, rerun | Unchanged where they apply; one edit by hand | **Unchanged.** Every R457-2 script was copied byte-identically; each sha256 equals its round-2 manifest entry. `probe-instrument.patch` and both setpoint patches apply to this head.<br>**By hand.** `probe-window-wider-than-a-tick.patch` does not apply, because its context is the restated walk line. Its single edit was applied by hand.<br>**`judge_il.py`** hard-codes W = 8 (clearance ≤ 8 ⇔ NOT GRADABLE). At W = 9 it flags only +2,016 and +2,036, both at clearance 9 and correctly NOT GRADABLE. `walk_audit.py` checks the same logs at W = 9 and finds 0 problems. |

## Prior public review findings at this head

| Finding | Status at `36207e91` | Evidence |
|---|---|---|
| R457-2 F1 (MINOR) = R456-2-F1 (MINOR): the stated walk S = 4 came from `walk()`, the smaller of two ranges; the CRF window's nearest-pop walk at dev's pin is 5 | **Resolved** | **One measure.** `walk()` is the nearest-pop range, `sim_tdm8_render.cpp:1449-1452`. The `[LAW]` figure (3) and the CRF figure (5) are now one measure, and the printed walk equals the range on its own line in every window: 0 problems in `walk-audit.txt`, 0 in `walks.tsv`.<br>**The figures.** S = 5 and W = 5 + 4 = 9 are stated in the code comment (`:184-199`), `MEDIA_CLOCK_FOLLOWING.md:1371` and `:1382-1394`, and the PR body. W = 9 is the round-3 assignment's explicit choice.<br>**The diagnostic** prints every window's walk and the largest beside the stated one (`lb-*.log`).<br>**Rerun at W = 9:** the suite and the diagnostic at both processors. |
| R456-1-F1 (MAJOR) = R457-1 F1 (MINOR): the tie rule's one-cycle premise | **Resolved, still** | No tie code at this head: `kBandSlackCycles = 1` (`:183`), and a graded fill must equal 14 (`:3307`). Boundary phases are NOT GRADABLE in every history and never graded (`lb-*.log`, `hist/`, `probe-tie*.log`). |
| R456-1-F2 (MINOR) = R457-1 F2 (MINOR): `TIME_SYNC.md:451` | **Resolved, still** | `TIME_SYNC.md` is untouched since `6b96391d`, where both rounds found it resolved. The T30 CRF LAW lines still read fill 14..14 at the PDU end at both processors. |
| R456-2 S1: the CRF clearance span leaves out the recentre's re-snap end | Taken as "state the difference" | `sim_tdm8_render.cpp:3422-3424`; `MEDIA_CLOCK_FOLLOWING.md:1399-1403`. The span itself is unchanged. |
| R456-2 S2 = R457-2 S2: check the walk against `kLawWalkCycles` | Open, listed in the PR body | S1 above |
| R456-2 S3: what a CRF gradability failure means | Taken | `MEDIA_CLOCK_FOLLOWING.md:1404-1414`. Its figures match `suite-*.log` and `crfonly-*.log` (−587 and +336; −1,018 and −91). |
| R456-2 S4: the stray quote | Taken | `tdm8_render_mutants.py:687-696`, exercised offline |
| R457-2 S1: `make -C … tdm8render-mutants` advertised | Taken for the docs and the runner's usage | No such form remains. The Makefile defect is a manager duty (a new Issue). |
| R457-2 S3: the CRF window's exact PDU count | Open, listed in the PR body | S2 above |
| R457-2 S4: `law-boundary-scan.md` not public | Not done | RES-1 |
| R456-1 S1 = R457-1 S3: the accept-pulse instrument; R456-1 S2: the stage's counters across a window | Open, listed in the PR body | New-Issue candidates |
| R456-1 S3: name the ceiling check for what it bounds | Taken | `sim_tdm8_render.cpp:3488-3490`; `MEDIA_CLOCK_FOLLOWING.md:1329`; `TESTING.md:521` |

## Lens coverage at this head

```text
[R457] PASS Conformance - sim_tdm8_render.cpp:184-199, :1433-1453, :3236-3265, :3420-3427, :3488-3490 at 36207e91; receipts/suite-*.log, lawonly-*.log, crfonly-*.log, lb-*.log, arm-*.log, standing-margins.txt, walks-table-compare.txt - round-3 assignment items 1-4 against the code and both processors' logs: walk as defined, S = 5 (CRF -592..-587), W = 9, all 19 standing windows gradable with the stated margins, setpoint +/-1 caught 36/36, the diagnostic's per-window and largest-walk print; the round-2 ruling's grading rules still hold (NOT GRADABLE iff clearance <= 9, graded fill exactly 14)
[R457] PASS RTL - receipts/scope-rtl.txt and clone-state.txt: hdl/ 0-line diff 5fabb46e..36207e91; round 3 touches only tb/ and docs/ (ca3db9f3 code, 36207e91 docs only); all four gitlinks equal live dev 241f9184's; the probe nets (receipts/probe-stdhist.log) still show 0 instant and 0 take-cycle mismatches and the fill read equal to fill_end_w except the ungraded snap PDU, on all 18 phases
[R457] PASS Robustness - receipts/wrap-*.log (the walk's wrap branch, exercised at +983/+984), probe-wfault-full.log (19/19 standing windows fail loudly), probe-tiehist.log, probe-tiealone.log, probe-nodwell.log, il-*.log, hist/ (54 legs, rc 0, identical at both processors), crfonly-*.log, judge-test.log (ALL OK) - a not-gradable window never passes or fails the law; boundary phases are NOT GRADABLE in every history; a moving grid fails its settled hold; the CRF window's nearest standing-style margin is 82 (--crf-only, c4cb84ff)
[R457] PASS Tests - tdm8_render_mutants.py:476-485, :684-696, :764-813 (window_walks, print_the_largest_walk, judge_boundary_rounds); receipts/arm-*.log, lb-*.log, walk-audit.txt, walk-audit-selftest-r2.txt, walks.tsv, il-*.judge.tsv - the setpoint and A2-a arms are caught at both processors; the diagnostic's judge is unchanged (offline test ALL OK) and its print re-measures; my independent audit catches the round-2 metric (222 problems) and finds 0 at this head
[R457] PASS Docs - MEDIA_CLOCK_FOLLOWING.md:1329-1330, :1367-1420; TESTING.md:270, :521, :523; tb/verilator/README.md:63; tdm8_render_mutants.py docstring :70-83; Makefile header; the PR body; receipts/docs-gates.log (7/7 rc 0) - every figure matches the logs (walk 5/4/3, W 9, margins 47/48 and 578/326, CRF -1,018/-91 under --crf-only, band margins >= 10); RES-1 is wording only and leaves the lens clean
```

## Reviewer-owned completion ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Round-3 assignment items 1-4 and round-2 ruling items 1-5; `sim_tdm8_render.cpp:184-199`, `:1433-1453`, `:3236-3334`, `:3420-3427`, `:3468-3505`; suites, `--law-only`, `--crf-only`, arms and the diagnostic at both processors | R457-3 | `36207e91c81fd33782b01486e3bc2fea50e91a1e` |
| RTL | CLEAN | `hdl/` 0-line diff from `5fabb46e`; changed paths `6b96391d..36207e91` and `241f9184..36207e91`; gitlinks against live dev; the instrumented probe's identities | R457-3 | `36207e91c81fd33782b01486e3bc2fea50e91a1e` |
| Robustness | CLEAN | Wrap-branch probe; window-fault probe; tie, no-dwell and setpoint probes; the interleaved history; three histories × 2 processors; `--crf-only` | R457-3 | `36207e91c81fd33782b01486e3bc2fea50e91a1e` |
| Tests | CLEAN | Runner diff `:70-83`, `:465-485`, `:684-696`, `:761-813`; `law_arm.py` (sp-low, sp-high, a2a) at both; `tdm8render-law-boundary` at both; `judge_test.py`; `walk_audit.py` with its round-2 negative control; `compare_walks_table.py` | R457-3 | `36207e91c81fd33782b01486e3bc2fea50e91a1e` |
| Docs | CLEAN (RES-1 is RESIDUE) | `MEDIA_CLOCK_FOLLOWING.md`, `TESTING.md`, `tb/verilator/README.md`, the Makefile header, the runner docstring, the PR body; docs gates rc 0 | R457-3 | `36207e91c81fd33782b01486e3bc2fea50e91a1e` |

## Real limits

- **Not run:**
  - the full `tdm8render-mutants` campaign. Its three `--law-only` arms ran individually through the campaign's own functions, at both processors;
  - Yosys, `syn/ooc`, and any parent, PP, gPTP or builder bank;
  - act; hardware. Physical calibration was NOT RUN, and skipped field contexts are not hardware proof.
- **Wall times:**
  - The diagnostic ran 4 legs at a time (`LAW_BOUNDARY_JOBS=4`, the round-2 recipe). It took 3,688 s and 3,851 s on a shared host.
  - The default suite took 757 s and 783 s cold, beside every other job of this round.
  - The load average was 27 to 90.
- **The wrap-branch and `--crf-only` legs are new this round.** Every other step is round 2's recipe.
  - `scripts/reproduce.sh` records the deltas:
    - the hand-applied window edit;
    - the A2-a arm beside the setpoint arms;
    - `TMPDIR` on disk;
    - `launch2` split in two, to stay within 16 jobs.
  - `histories.sh` ran unchanged, at 2 and then 4 parallel legs.
- **Job accounting:**
  - To raise my history driver's parallelism, I first signalled by command-line pattern. The shell running that command matched the pattern and exited, so the command's output was lost.
  - The pattern could also have matched one other parallel driver on the shared host. The signal only raises a driver's parallelism by one, and that process had exited when I checked.
  - I then signalled my own driver by process ID, and it rose from 2 to 4 legs.
  - No leg was killed or paused, and every leg wrote its rc.
  - I edited `scripts/reproduce.sh` (the `launch2b` split and the `analyse` lines) while its `launch3` step was still running the history driver.
    - When that step finished, the shell read on in the edited file and printed a syntax error at its end (`receipts/launch3-step.log`).
    - Every `launch3` leg had already run and written its rc.
    - The published script passes `sh -n` and `bash -n`.
- **Redaction:** absolute host paths in the receipts are replaced by `$PKT`, `$VALIDATION_STORAGE`, `$VALIDATION_TOOLS` and `$HOME`. `MANIFEST.sha256` was computed after redaction, over the files as published.
- **Hosted state:** `receipts/hosted-snapshot.tsv` holds two read-only snapshots of the exact head's check runs, the latest last.
  - At 06:57 UTC, 21 contexts had completed with success. They include `rtl-fast`, `verilator-suites` (Verilator shards 0-4), `yosys-portability` (Yosys shards 0-3), `elaborate`, `docs-check` and `full-ci-gate`.
  - Physical gPTP was skipped. That is not hardware proof.
  - The manager owns hosted and act acceptance.

## Pending manager duties

- Publish this report and its manifest.
- RES-1: publish `law-boundary-scan.md`, or carry the reworded parenthetical to the residue checklist.
- Exact-head hosted `verilator-suites` and `yosys-portability` evidence.
- The current-dev candidate build at the merge turn (source base `5fabb46e`, live dev `241f9184`).
- File new Issues for the open items the PR lists:
  - the `make -C` Makefile defect;
  - the `--epoch-only` control and the surviving underrun mutant;
  - the accept-pulse instrument;
  - S1 and S2 above, if the maintainer wants them as checks.

## Clone state after probes

All probes ran in copies under the scratch directory. The review clone is at `36207e91`:

- worktree equals the index equals HEAD;
- 0 untracked or ignored files, and no `__pycache__`;
- the index's (mode, blob, path) set hashes the same as HEAD's tree;
- gitlinks: protocol-processor `631eeb34`, gptp-processor `5dce647a`, third_party/verilog-axis `48ff7a7e`, external `efeb541a`;
- every submodule worktree is clean (`receipts/clone-state.txt`).

The evidence branch was fetched into a scratch repository, not into the review clone.

R457-3 FINISHED
