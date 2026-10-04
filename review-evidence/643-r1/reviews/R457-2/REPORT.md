[R457] NEGATIVE - exact head 6b96391d13c5d777a98b1c7be9265c63d651c911

# R457-2: external review of #643 / PR #648, round 2

- **Head under review:** `6b96391d13c5d777a98b1c7be9265c63d651c911`, tree `20de609684af73ef2e8dff3da994e45c976ba5bd`.
  - Source base: dev `5fabb46e767c9308ab2580916237f43577698c6e`.
  - Merged dev: `241f91845230ae410506dffb16b71937127fd175`.
  - Processor pin: `631eeb34`.
- **Round:** R457-2, external, cleared context. It ran from the [review start](https://github.com/kebag-logic/milan-fpga/pull/648#issuecomment-5975558494).
- **Context reconstructed from:**
  - `AGENTS.md`;
  - the #643 body, the [lane assignment](https://github.com/kebag-logic/milan-fpga/issues/643#issuecomment-5972861856), the [ruling 5973450039](https://github.com/kebag-logic/milan-fpga/issues/643#issuecomment-5973450039), the [round-2 ruling 5974715857](https://github.com/kebag-logic/milan-fpga/issues/643#issuecomment-5974715857) and the round-2 REVIEW READY (5975549174);
  - the PR #648 body at this head;
  - the diff `98729742..6b96391d` and its three commits;
  - the public evidence `review-evidence/643-r1` at `531abe2b`, and the executor's round-2 hand-off at `643-review-evidence` `5aff1fcb`.
- **Prior public findings:** I read R456-1 (5974712082) only after my own pass over the diff. My own R457-1 is 5974627143.

## Verdict in one paragraph

The round-2 change does what the ruling asked, and I reproduced it at both processors.

- **The tie rule is gone.** A window with any PDU end within 8 cycles of the fill's boundary is NOT GRADABLE: it is named and neither passes nor fails. Every standing window must be gradable, and that is asserted by name.
- **The suite discriminates.** Graded windows require fill exactly 14, and the band keeps only the one-cycle pulse register. The setpoint −1 and +1 mutants fail fill and band at all 18 standing phases.
- **The diagnostic holds.** In five histories at both processors, no graded window failed the sound design or passed a setpoint defect.
- **Round 1's failure cases are now handled.** At +2,025 and +2,026 the sound design reads 15, depending on history, and setpoint −1 reads 14 at 112 and 63 of 124 PDUs. Both phases are now NOT GRADABLE and, as standing phases, fail by name.
- **The dev merge is clean,** `--no-ff`, with no `hdl/` change.

The verdict is NEGATIVE because of F1, one MINOR. The stated spread S, "4 across T30's CRF window", understates the measured spread. At dev's pin the CRF window's PDU-end-to-nearest-pop offset spans −592..−587, which is 5 cycles. The harness's `walk()` reports the smaller of two ranges even when neither wraps. W = 8 still exceeds the true spread, so no grading verdict changes. But the measurement that the ruling made the basis of W is misstated in the code, the design page and the PR body.

## Findings

### F1: MINOR. Lenses: Conformance, Tests, Docs. The stated spread S (4) understates the measured end-to-nearest-pop walk of the CRF window (5) at dev's pin

- **Where:**
  - `tb/verilator/milan_dp_render/sim_tdm8_render.cpp:1444`: `long walk() const { return std::min(dmax - dmin, nmax - nmin); }`. Its comment at `:1431-1433` reads "one of the two wraps at a tick, never both, so the walk is the smaller range".
  - `:186-196`: "4 across T30's CRF window, so the walk is stated as 4 and the guard doubles it"; `kLawWalkCycles = 4`, `kLawGuardCycles = 4`.
  - `docs/design/MEDIA_CLOCK_FOLLOWING.md:1371`: "within one graded window it walks by up to 4 cycles".
  - `:1381-1383`: "T30's CRF window, 292 PDUs under CRF, walked 4. The window is stated against the larger"; "the walk plus a guard of 4 cycles".
  - The PR body: Round 2 item 1 ("4 in T30's CRF window") and Known limitations ("W = 8 is the largest walk measured (4, in the CRF window) plus an equal guard").
- **Authority:**
  - Round-2 ruling item 1: "Record, per phase, the PDU-end-to-pop offsets over the graded window. State the measured spread S, and set the window W = S plus a guard."
  - The page's own definition: the walk is that of "the offset from a PDU end to its nearest pop".
  - `AGENTS.md` section 6, Tests ("Tests do not merely reproduce implementation assumptions") and Docs.
- **Evidence:**
  - At `631eeb34` the full leg prints `T30 CRF LAW: ... the first pop after the end is taken +1492..+1496 ... and the pop nearest the boundary -592..-587 (walk 4); the least clearance is 587` (`receipts/suite-head.log:479`).
    - Every CRF end's nearest pop is the previous one (−587..−592), and that range is 5.
    - The reported 4 is the range of the next pop, which is 1,492 cycles away and is not the pop that would sit at a boundary.
    - Neither range wraps, so the `min` in `walk()` picks the smaller of two valid ranges.
  - The executor's own published table shows the same row: `review-evidence/643-r1/author-r2/HANDOFF.md` R2.3, "T30 CRF (292 PDUs) | -592..-587 | 4".
  - At `c4cb84ff` the CRF window's nearest pop is the next one, +336..+340, a range of 4 (`receipts/suite-c4.log:488`).
  - Over 587 `[LAW]` windows (the suites, `--law-only`, both arms, the probes and all three histories at both processors), the largest non-wrapping range of either offset is 3 (`receipts/walks.tsv`, `receipts/hist-summary.tsv`). So the `[LAW]` statement "at most 3" holds, and only the CRF figure is wrong.
  - In 49 `[LAW]` windows and 1 CRF window, the nearest-pop range exceeds the reported walk by 1.
- **Impact:**
  - The spread that W is declared against is understated by 1 cycle. The derivation "the guard doubles it" is false: the guard over the measured CRF walk is 3 cycles, not 4.
  - The docs name `tdm8render-law-boundary` and the per-window walk line as how W is re-measured after a model change. That metric under-reports whenever the two ranges differ, so a future re-measurement can understate S again.
  - No graded verdict changes today. Every graded window in my runs had a clearance of at least 9 and was graded correctly.
  - The finding is a misstated measurement and the instrument that produces it, so it is not RESIDUE.
- **Required outcome:**
  - The stated S equals the measured range of the end-to-nearest-pop offset across the windows W is declared against. That is 5 for the CRF window at `631eeb34`, unless a corrected metric shows a different value.
  - W is restated as S plus its guard: for example W = 8 with a guard of 3, or a larger W.
  - The printed walk no longer understates when neither range wraps. One fix: use the range of the nearest pop when it does not wrap, and the range of the next pop only when it does.
  - The code comment at `:186-196` and `:1431-1433`, `MEDIA_CLOCK_FOLLOWING.md:1371-1385` and the PR body agree with the new figures.
- **Verification:**
  - Rerun `make -C tb/verilator/milan_dp_render` at both processors. The T30 CRF LAW line at `631eeb34` must report a walk equal to its nearest-pop range.
  - Read the code comment and the docs against it, and rerun `scripts/walks.py` over the new logs.
  - Run the docs gates.

### Suggestions (non-blocking)

- **S1. Lenses: Tests, Docs. Pre-existing; a new Issue for the manager.**
  - `make -C tb/verilator/milan_dp_render tdm8render-law-boundary` fails every defect build: the nested `print-srcs` captures make's "Entering directory" banner (`receipts/lb-head-makeC.log`, `lb-c4-makeC.log`; their rc was not captured, and each log ends in make's `Error 1`).
  - The PR documents this for the new target (`TESTING.md:523`, Makefile header). But `TESTING.md:270` and `:523` still advertise `make -C tb/verilator/milan_dp_render tdm8render-mutants`, which fails the same way.
  - The executor reports the cause as pre-existing and unfiled.
- **S2. Lens: Tests.** Assert each standing window's walk against `kLawWalkCycles`, not only its clearance against W. W is declared "a measurement of this model", and the campaign's `--law-boundary` round keeps only verdict lines, so nothing in the suite's output would flag a walk that outgrew the stated S.
- **S3. Lens: Tests.** The T30 CRF LAW window still checks "at least 100" PDUs (`sim_tdm8_render.cpp:3413`, `expect_n` 0). The `[LAW]` phases now check exactly 124. The CRF window measured 292 at both processors.
- **S4. Lens: Docs.** The hand-off cites per-phase tables in `law-boundary-scan.md` ("Every row, with its offset histogram"). That file is not in the public packet `5aff1fcb`, which holds only `HANDOFF.md` and `PR-BODY.md`. I reproduced the data independently (below), so this is not a finding.

## Prior public review findings at this head

| Finding | Status at `6b96391d` | Evidence |
|---|---|---|
| R457-1 F1 (MINOR): the tie rule's one-cycle premise is false | **Resolved.** The measured-spread clause is carried into R457-2 F1 | Tie rule removed; `kBandSlackCycles` 64 → 1 (`:183`); NOT GRADABLE gate (`:3228-3253`). The round-1 probes, rerun unchanged in spirit (patch ported, phase lists identical): <br>• `tiehist`: +2,023..+2,028 and +2,025 ×3, all NOT GRADABLE, each failing "gradable" by name, rc 1. The sound design's history-dependent reads (124, 12, 5 of 124 at fill 14 at +2,025) are no longer graded. <br>• `tiealone`: +2,025 NOT GRADABLE (4 of 124 at fill 14). <br>• `sp-std`: setpoint −1 fails fill and band at all 18 standing phases. +2,025 and +2,026 are NOT GRADABLE (they read 14 at 112 and 63 of 124 PDUs and would have passed under the tie rule). <br>• `sphi-std`: the same for +1. <br>• `stdhist`: 18/18 graded, fill 14 at 124/124 each, rc 0. <br>The PR body withdraws the "+2,025 and +2,026 only" tie-scan statement. |
| R457-1 F2 (MINOR): `TIME_SYNC.md:451` | **Resolved** | `TIME_SYNC.md:451-455`: "Each PDU end's fill is the setpoint plus that PDU ... Both are graded at the PDU end", with a link to the ambiguity window. That matches the T30 CRF LAW lines (fill 14..14, 292 PDUs, both processors). |
| R456-1 F1 (MAJOR): the tie rule fails at the boundary after settle | **Resolved** (the excluded-phase form). The measured-walk statement is carried into R457-2 F1 | The bound is stated and enforced. The standing margins are asserted: the least is 48 (+0, `--law-only`), 49 (+0, full leg), and the CRF window's 579 / 327. No "one cycle of feed jitter" or tie wording remains (searched in `docs/`, the README and the suite). Setpoint ±1 never pass a graded window (below). |
| R456-1 F2 (MINOR): `TIME_SYNC.md:451` | **Resolved** | As R457-1 F2. |
| R457-1 S1, R456-1 S1-S3, R457-1 S2-S3 | Suggestions, not findings. | <br>• R457-1 S1 is adopted for `[LAW]` (exactly 124); the CRF part is S3 above. <br>• R456-1 S2: my probe confirms the fill read equals `fill_end_w` at every end except the ungraded snap PDU. <br>• The others are unchanged and remain new-Issue candidates. |

## The focus items, verified

| Item | Result | Evidence |
|---|---|---|
| The dev merge is `--no-ff` and clean | Yes | `7aa7b449` has parents `98729742` and `241f9184`. `git merge-tree --write-tree` of the two gives `5c72a5b4…`, equal to `7aa7b449^{tree}`. Head against `241f9184` differs only in the 7 lane files. `hdl/` diff from `5fabb46e`: 0 lines. All four gitlinks are unchanged. |
| The measured walk and W = 4 + 4 = 8 are supported by `--law-boundary` at both processors and three histories | **`[LAW]`: yes. CRF: no (F1)** | `receipts/hist/` (54 legs) and `hist-summary.tsv`: ascending (own located scan, boundary near +2,026), descending (+2,066..+1,986) and alone (+2,014..+2,038), at both processors, rc 0 throughout. Largest `[LAW]` offset range 3; reported walk at most 3. CRF at `631eeb34`: 5 (F1). W = 8 still exceeds every measured walk. |
| A window within W of the boundary is NOT GRADABLE, never pass, never fail, and named | Yes | `:3228-3253`; `[NOT GRADABLE] <tag>: PDU <id>'s end has a pop taken <off> cycles from it`. In `--law-boundary` mode, every NOT GRADABLE phase failed 0 checks: `lb-*.log` (162 legs), `il-*.judge.tsv`, `hist/`. In standing mode it fails "gradable" by name (`probe-tiehist`). Clearance ≤ 8 ⇔ NOT GRADABLE in every interleaved row (`il-*.judge.tsv`). |
| Every standing window (18 `[LAW]` + CRF) asserts its margin, and the suite fails if one is not gradable | Yes | Fault probe `scripts/probe-window-wider-than-a-tick.patch` (guard 2,100, so W exceeds a tick). The full leg fails exactly 19 "gradable" checks (18 `[LAW]` + T30 CRF LAW), rc 1, and their law checks are skipped (245 → 188 checks) (`probe-wfault-full.log`). |
| Graded windows read fill 14 exactly; no tie slack | Yes | `:3296` `f == kPrefillTargetEvt` only; `kBandSlackCycles = 1` (`:183`). Least band-edge margin over graded windows in the interleaved scan: 9.00 cycles (`il-head-probe.judge.tsv`), so "more than 8 cycles inside both edges" (`MEDIA_CLOCK_FOLLOWING.md:1397`) holds. |
| Setpoint −1 and +1 fail all 18 phases | Yes, both processors | Through the campaign's own `plant`/`build`/`run_leg`/`verdict` (`scripts/law_arm.py`): `arm-{head,c4}-sp-{low,high}`, each `caught`, 36/36 named checks, no other failure. Fill 13 or 15 at every phase; delays 7.03..7.97 T and 9.03..9.97 T. |
| The boundary diagnostic never fails the sound design, never passes setpoint ±1 among graded windows | Yes | `make tdm8render-law-boundary LAW_BOUNDARY_JOBS=4` from the suite directory: rc 0, 81/81 at both processors, identical verdict lines. NOT GRADABLE +2,017..+2,034 in the scans, +2,016..+2,036 alone, as published. <br>Independently, an interleaved history the runner does not use (+2,005, +2,045, +2,006, … inward), on my probe builds: sound 22/22 graded PASS; −1 and +1 22/22 graded FAIL on both checks; 19 NOT GRADABLE (+2,017..+2,035) with 0 failures (`il-*.judge.tsv`). The judge rejects every bad case I fed it (`judge-test.log`, 24/24). |
| The A2-a arm still fails every phase | Yes | `arm-{head,c4}-a2a`: `caught`, 18 settled checks plus the ceiling, no other failure. |
| Both processors | Yes | `631eeb34`: rc 0, 245/0, 65/0, 5/5, 747 s cold. `c4cb84ff` scratch parent (gitlink set, c8 `bbf704ec` then p2-p1 `1269cdaf` applied, never committed; `c4-parent-state.txt`): rc 0, same counts, 766 s. `--law-only` 106/0 at both (margin 48). The host's load average was 30 to 60 from unrelated work; at 1.58× that is about 1,210 s, inside 1,800 s. |
| The docs match the code | Yes, except the CRF walk figure (F1) | `TIME_SYNC.md:451-455`; `MEDIA_CLOCK_FOLLOWING.md:1329-1330` rows and `:1367-1398`; `tb/verilator/README.md:63`; `TESTING.md:521`, `:523` (inventory 21 + 3 + 3 + 5 = 32, matching the runner's tables; 81 boundary checks); Makefile header. Margins 48/49 and CRF 579/327 match my logs. Docs gates rc 0 (`docs-gates.log`). |

## Lens coverage at this head

| Lens | Result | Artifacts examined at `6b96391d` |
|---|---|---|
| Conformance | UNCLEAN (F1) | Round-2 ruling items 1 to 5 against the code, the runner and the logs above. Every item is met except item 1's stated S for the CRF window. |
| RTL | CLEAN | See the PASS line below. |
| Robustness | CLEAN | See the PASS line below. |
| Tests | UNCLEAN (F1) | `tdm8_render_mutants.py` diff: `SETPOINT_DEFECTS` `:141`, `MUTATIONS` `:340`, `boundary_problems` `:691`, `run_law_boundary` `:776`. Offline judge and parser test (`judge-test.log`, 24/24). All arms. Diagnostic at both processors. The interleaved independent judge. F1 is the `walk()` metric. |
| Docs | UNCLEAN (F1) | `MEDIA_CLOCK_FOLLOWING.md:1329-1330`, `:1355-1400`; `TIME_SYNC.md:440-457`; `TESTING.md:270`, `:280-287`, `:521`, `:523`; `tb/verilator/README.md:63`; the Makefile header; the PR body; the docs gates. |

The two clean lenses, in findings format:

```text
[R457] PASS RTL - hdl/ and all four gitlinks (0-line diff 5fabb46e..6b96391d; merge tree == merge-tree of 98729742+241f9184), KL_render_setpoint.sv:346/454/499/533-534, sim_tdm8_render.cpp:703-718, receipts/probe-stdhist.log - harness end beat == stage pdu_end_w and the pulse seen at c <=> pop_take_w at c-1 on every cycle of 18 phases (0 mismatches each); fill read == fill_end_w except the ungraded snap PDU; probe [LAW] lines byte-identical to the clean binary's
[R457] PASS Robustness - receipts/probe-wfault-full.log, probe-tiehist.log, probe-tiealone.log, probe-nodwell.log, parse-refusals.log, hist-summary.tsv, suite-*.log, lawonly-*.log - every standing window fails loudly when not gradable (19/19); boundary phases are NOT GRADABLE in every history, not misgraded; standing margins >= 48 at both processors (CRF 579/327); a moving grid still fails 14 holds; 7 malformed --law-boundary lists refused before simulation; runner parse refusals (6/6)
```

## Reviewer-owned completion ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1) | Round-2 ruling items 1-5; `sim_tdm8_render.cpp:177-226`, `:3175-3313`, `:3438-3567`; `tdm8_render_mutants.py`; suite, arm, diagnostic and history receipts | R457-2 | `6b96391d13c5d777a98b1c7be9265c63d651c911` |
| RTL | CLEAN | `hdl/` 0-line diff; gitlinks; merge-tree; `KL_render_setpoint.sv:346, 454, 499, 533-534`; instant, take and fill probe | R457-2 | `6b96391d13c5d777a98b1c7be9265c63d651c911` |
| Robustness | CLEAN | Window fault probe; tie, nodwell and setpoint probes; parse refusals; three histories at both processors; standing margins | R457-2 | `6b96391d13c5d777a98b1c7be9265c63d651c911` |
| Tests | UNCLEAN (F1) | Runner diff; `judge_test.py`; `law_arm.py` (sp-low, sp-high, a2a) at both processors; `tdm8render-law-boundary` at both; interleaved independent judge; `walk()` `:1444` | R457-2 | `6b96391d13c5d777a98b1c7be9265c63d651c911` |
| Docs | UNCLEAN (F1) | `MEDIA_CLOCK_FOLLOWING.md`, `TIME_SYNC.md`, `TESTING.md`, `tb/verilator/README.md`, Makefile header, PR body; docs gates rc 0 | R457-2 | `6b96391d13c5d777a98b1c7be9265c63d651c911` |

## Real limits

- **Not run:**
  - the full `tdm8render-mutants` campaign. Its three setpoint and A2-a arms ran individually through the campaign's own functions, at both processors;
  - Yosys, `syn/ooc`, and any parent, PP, gPTP or builder bank;
  - act; hardware. Physical calibration was NOT RUN, and skipped field contexts are not hardware proof.
- **My boundary-history alone set is ±12** (+2,014..+2,038), the runner's own. The executor's measurement ran alone over ±40. My scans cover ±40 in both directions at both processors.
- **The round-1 `probe-instrument.patch` no longer applies,** because it edits the removed tie code. I ported it (`scripts/probe-instrument.patch`: three `public_flat_rd` nets, `LAW_PHASES`, `LAW_NODWELL`, the offset histogram, and a new pulse-and-take identity check) and ran my round-1 phase lists unchanged. The setpoint −1 patch is unchanged; +1 is its counterpart (`RENDER_ALLOW_EVT_C` 3).
- **Job accounting:**
  - The first launch's `bg` wrapper ran under `set -e`, so legs exiting nonzero wrote no rc file. Those five probe runs were rerun with the fixed wrapper, and the reruns were byte-identical to the first runs, which I then discarded.
  - The two `make -C` diagnostic runs (S1) also have no rc file.
  - A history-driver restart killed its parent. Its eight already-started legs ran to completion and wrote their rc. For about a minute, seven legs were paused (SIGSTOP), one of them a diagnostic leg, to stay within 16 jobs. Every leg is cycle-bounded with no wall deadline, so pausing changes no result.
- **Redaction:** home-directory paths in the suite and `make -C` logs are replaced by placeholders.
- **Hosted state:** `receipts/hosted-snapshot.tsv` is a read-only snapshot at 02:04 UTC.
  - Already green: 10 contexts, including the Yosys shards, lint, `bdd-conformance` and `full-ci-gate`.
  - Still in progress: the Verilator shards 0-4, `docs-check`, `elaborate` and `yosys-elaboration`.
  - Physical gPTP was skipped.
  - The manager owns hosted and act acceptance.

## Pending manager duties

- Publish this report and its manifest.
- Carry F1 to the executor.
- Re-review Conformance, Tests and Docs at the corrected head.
- File new Issues for:
  - S1 (`make -C`);
  - the pre-existing campaign failures the executor lists (the `--epoch-only` control, the surviving underrun mutant);
  - R457-1 S3 / R456-1 S1 (the accept-pulse instrument in `milan_dp`).
- Publish `law-boundary-scan.md` if it is to be cited (S4).
- Exact-head hosted `verilator-suites` and `yosys-portability`.
- The current-dev candidate build at the merge turn (base `5fabb46e`, live dev `241f9184`).

## Clone state after probes

All probes ran in copies under the scratch directory. The review clone is at `6b96391d`:

- worktree equals the index equals HEAD;
- 0 untracked or ignored files, and no `__pycache__`;
- the index's (mode, blob, path) set hashes the same as HEAD's tree (`282a96b2…`);
- gitlinks: protocol-processor `631eeb34`, gptp-processor `5dce647a`, third_party/verilog-axis `48ff7a7e`, external `efeb541a`;
- every submodule worktree is clean (`receipts/clone-state.txt`).

The round-2 evidence branch was fetched into a scratch copy, not into the review clone.

R457-2 FINISHED
