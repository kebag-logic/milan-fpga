[R429] POSITIVE - exact head f4f0ecb4b41866cd30875e08e74114868ece5b4c

# R429-5: external review of PR #631 (#629, lane M1, design only), round 5

Head `f4f0ecb4b41866cd30875e08e74114868ece5b4c`, tree `a3a3fadd634b76469f7359628697ff527686a3c5`. The head is one docs commit on round 4's `1bdd6895`. Source base is dev `d4dd742679b902b2bc5eedf89d525066d59aafbb`. This round answers the round-5 assignment (#629 comment 5939246995) and the REVIEW READY (#629 comment 5940218896).

## Verdict

POSITIVE. No BLOCKER, MAJOR or MINOR finding is open at this head. All five lenses are covered clean.

- **F1 is resolved.** This was round 4's F1 (shared with R428-4 F1): the random-loss cliff. "Lost PDUs", "What round 3 cost", the estimator's "Residual" bullet, Limits and the PR body now state a graded falloff. I re-derived it with my own closed-form check and two independent models:
  - the restart rate, 500 q^2 (1 - q);
  - the valid fraction, e^(-4.096 x rate);
  - every table figure, the 90/50/10/1 % crossings and the round-4 expectations;
  - every seed locks, and no case drops LOCKED.

  The 32-seed lock-time medians on the page lie inside the sampling spread of my 512-seed population.
- **F2 is resolved.** This was round 4's F2 (shared with R428-4 F2): the counter row's loss leg had no mutant. Both the counter row and the servo-with-meter row now name the held-lock mutant, "the meter's held lock cleared on a sequence gap". My PDU-level model of the meter and of the servo's state machine shows each leg failing under it as the page says:
  - LOCKED is left at the first lost PDU, with 199 HOLDOVER entries;
  - LOCKED is not regained in the leg;
  - the trim ends 3.92 ppm off;
  - LOCKED returns 2.53 s after the counter leg ends.

  The design moves neither counter in the leg. The C0, C2 and restart-on-any-loss levels move nothing.
- **Every round-4 suggestion is taken, and each statement checks:**
  - k = 0 restarts;
  - the deviation check runs up to the gap;
  - the step row has 120 cases: 56 restart at the step's PDU and 64 across the gap. The no-cross-check mutant fails exactly the 64, with LOCKED dropping twice in each;
  - the gap-bound row passes only for a bound of 5,100 to 6,364 ns;
  - the midpoint fill is exact for a constant rate, and moves at most 0.76 ns per ppm of change in my sweep;
  - "LOCKED drops twice in each of them".
- **Nothing outside the page changed** (`git diff 1bdd6895 f4f0ecb4`).
- **Every gate returns rc 0:** the docs gates in the pinned Markdown environment, `check_entity_shape.py` (166 checks, 0 failures) and `git diff --check` on both ranges.
- **The PR body equals the prepared body.** It says "Relates to #629", and the added lines carry no private names.

Three SUGGESTIONs follow. They are optional and affect no lens.

## How the task was reconstructed

Read in this order:

1. `AGENTS.md` and `CONTRIBUTING.md` sections 3 and 6.
2. `docs/README.md`.
3. #629's body.
4. The manager's lane and ruling comments on #629: 5935051587, 5935520588, 5937449258, the owner decisions 5937643550 and 5937848189, and the accuracy note 5937738214.
5. The A482 DECISION, 5935490330.
6. The diffs: `git diff d4dd7426..f4f0ecb4` (two files: the design page and its index row) and `git diff 1bdd6895..f4f0ecb4` (the design page only, +153/-50).
7. The cited RTL at this head: `hdl/ieee1722/crf/KL_mmcm_drp_servo.sv:228-233, :520-700` and `hdl/ieee1722/crf/KL_crf_rx.sv:279-300, :376-405, :525-592, :615-626`.
8. The public round-5 author packet: `review-evidence/629-r1/author-r5` on branch `629-review-evidence` at `5c89a6c6`.

The round-5 assignment and the round-4 reports (R429-4 5939232297, R428-4 5939246407) were read only after the independent pass over the diff and the models below. No other reviewer's round-5 report was read.

## Findings

No BLOCKER, MAJOR or MINOR finding.

### S1 - SUGGESTION - Docs - give the lock-time medians' sampling spread, and soften two wordings

- **Where:**
  - `docs/design/MEDIA_CLOCK_FOLLOWING.md:861-868`, the table's lock-time column;
  - `:874-878`, "which puts the model's median at 17.3 s";
  - `:1423-1425`, Limits: "in the desk model's median, 7.8 s ... 17.3 s ... 288 s";
  - `:670-671`: "costs the rate's validity in proportion to how often it comes".
- **Evidence:**
  - Each median on the page is from one draw of 32 seeds.
  - My 512-seed population (256 at 24 a second; `receipts/locktime_pop/`, `receipts/pool_locktimes.out`) gives these population medians: 9.9 s, 14.5 s, 32.9 s and 262 s.
  - The 95 % range of a 32-seed median is 7.3 to 11.4 s, 11.4 to 18.6 s, 24.4 to 42.1 s and 194 to 345 s.
  - The page's 7.8, 17.3, 29.1 and 288 s all lie inside those ranges, so the figures are honest. But the 17.3 s against 18.5 s comparison is inside the noise. The mechanism the page names is right: an invalid rate holds the lock count, `KL_mmcm_drp_servo.sv:613-615`. It just cannot be read off those two numbers.
  - The cost of loss is 1 - e^(-4.096 x rate), which is proportional only while the rate is small.
- **Optional change:**
  - Say the medians are single 32-seed draws, with a spread of a few seconds at 8 to 16 a second.
  - Credit the mechanism, not the 1.2 s difference.
  - Write "grows with how often it comes".

### S2 - SUGGESTION - Docs - one packet file is listed but not published

- **Where:**
  - the published packet `review-evidence/629-r1/author-r5/MANIFEST.sha256`, which lists `./run_gates.sh`;
  - the PR body, which names "`gates/` with `run_gates.sh`".
- **Evidence:**
  - The file is absent from the packet tree at `5c89a6c6`, so 87 of the 88 manifest entries verify (`receipts/author_replay/REPLAY.txt`).
  - Every gate's output and rc are present.
  - I re-ran every gate independently (`receipts/gates/`). The design head is unaffected.
- **Optional change:** the manager publishes the file, or the manifest and PR body stop naming it.

### S3 - SUGGESTION - Docs, Tests - the bound table and the gap-bound row differ by 2 ns at the upper edge

- **Where:**
  - `:802-807`: B_2 must lie in 4,054 to 6,362 ns, from 601 ns per 2 ms, the rounded-up rate term;
  - `:818-826` and row `:1300`: the row passes for 5,100 to 6,364 ns, from the exact 600 ns.
- **Evidence:**
  - Both are correct in their own frames. My sweep gives exactly 5,100 to 6,364 ns (`receipts/pdu_gapbound.out`).
  - The row's lower edge, 5,100 ns, is the +/-1,950 ns tolerance case, not the design point's 4,054 ns.
- **Optional change:** a half-sentence saying the row uses the exact rate term and a near-tolerance lower edge. Without it, a reader may take the row as contradicting the table.

## Round-5 items, re-derived

### Item 1: random loss as a graded falloff

The prior finding is R429-4 F1, shared with R428-4 F1.

**Closed form** (`scripts/formula_check.py`, `receipts/formula_check.out`):

| Lost PDUs a second | 500 q^2 | Exact 500 q^2 (1 - q) | Valid, approximate | Valid, exact |
|---|---|---|---|---|
| 0.8 | 0.0013 | 0.0013 | 0.9948 | 0.9948 |
| 4 | 0.0318 | 0.0315 | 0.878 | 0.879 |
| 8 | 0.1261 | 0.1241 | 0.597 | 0.602 |
| 11.2 | 0.2457 | 0.2402 | 0.366 | 0.374 |
| 16 | 0.497 | 0.481 | 0.131 | 0.139 |
| 24 | 1.101 | 1.050 | 0.0110 | 0.0136 |

- **The crossings,** by the exact rate: 90 % at 3.61, 50 % at 9.37, 10 % at 17.34 and 1 % at 24.88 lost PDUs a second. The page says 3.6, 9.4, 17 and about 25.
- **Round 3's comparison:** p = 3e-5 is 0.24 lost PDUs a second, one in 4.17 s, and validity 0.374. The 1 % point is 1.12 a second. The page says 37 % and 1.1.
- **Round 4's rows:**
  - expected restarts 0.38 and 37.2, against 1 and 41 published;
  - expected validity 0.981 and 0.593 after the 0.9863 fill factor, against 0.98 and 0.55 published.

  The page's figures match.

**Independent group-level Monte Carlo** (`scripts/random_loss_model.py`, `receipts/random_loss/`):

- **The model.** It applies the page's rules 1 to 4 and E8, with the servo's PI and lock rule from `KL_mmcm_drp_servo.sv:562-579` and `:609-648`.
- **Why it is exact.** With +/-1,042 ns of independent error at 0 ppm, no deviation, spacing or k = 2 check can fail. So Bernoulli(q) voiding per group is exactly PDU-level Bernoulli(p) loss.
- **Calibration.** The window phase is set so that no loss gives LOCKED at 7.3 s, the page's figure. Phase 0 is also run.

| Lost PDUs a second | Restarts a second | Valid | LOCKED median, middle half, slowest (32 seeds) | Never locked | LOCKED drops |
|---|---|---|---|---|---|
| 0.8 | 0.0014 | 0.9945 | 7.3; 7.3; 7.3 s | 0 | 0 |
| 4 | 0.0301 | 0.885 | 7.3; 7.3 to 7.3; 14.5 s | 0 | 0 |
| 8 | 0.1271 | 0.596 | 10.6; 7.3 to 12.9; 24.2 s | 0 | 0 |
| 11.2 | 0.2446 | 0.368 | 12.4; 10.4 to 21.3; 41.1 s | 0 | 0 |
| 16 | 0.4868 | 0.139 | 34.9; 20.9 to 50.4; 113.3 s | 0 | 0 |
| 24 | 1.0534 | 0.0137 | 234.6; 135.8 to 379.1; 713.3 s | 0 | 0 |

- **Agreement.** Restart rates and validity agree with the page's model columns within sampling.
- **"A cold start still locks", and the seven-window lock.** Every seed locks, and none drops LOCKED. My PI arithmetic from 5,448 ns gives |e| = 5,448, 1,362 and 1,703 ns, then four clean windows. That is the page's "three to converge and four to qualify".
- **The lock-time spread** is the subject of S1.
- **The author's model.** Its `random` section re-runs byte-identical (`receipts/author_replay/`).

### Item 2: the held-lock mutant

The prior finding is R429-4 F2, shared with R428-4 F2.

**RTL basis at this head.**

- `KL_mmcm_drp_servo.sv:564`: ACQUIRE or LOCKED goes to HOLDOVER on `!crf_locked_i`.
- `:573-578`: HOLDOVER goes to ACQUIRE with `win_skip_r <= 2` and `lock_cnt_r <= 0`.
- `:613-618`: the PI runs only when the skip is 0, the state is not HOLDOVER and the rate is valid.
- `KL_crf_rx.sv:569-570`: a gap breaks the settle run but does not clear a held lock.

Losses 0.3 s apart leave at most one window boundary between two HOLDOVER entries, so the skip never reaches 0.

**Model.** `scripts/pdu_model.py`, sections `servoleg`, `counter` and `legtrim`. The talker runs at +20 ppm with +/-1,426 ns of independent error. The leg loses one PDU every 0.3 s for 60 s. The servo row also steps the talker to +24 ppm at the leg's start.

| Level | Servo row | Counter row |
|---|---|---|
| Design | LOCKED kept; 0 HOLDOVER entries; trim +0.08 ppm off at the leg's end (pass: within 0.5 ppm) | 0 UNLOCKED, 0 LOCKED in the leg |
| Held lock cleared on a gap | LOCKED left at the first lost PDU (40.300 s); 199 HOLDOVER entries; not regained in the leg; trim -3.92 ppm off | UNLOCKED once, at the first loss; LOCKED 0 in the leg; LOCKED 2.53 s after the leg ends |
| Restart on any loss | 199 restarts; LOCKED kept; trim -3.92 ppm off | no counter moves |

So the mutant is killed by both legs as the page states (`:1305`, `:1311`, `:1186-1188`, `:970-973`).

- **The leg grades this mutant alone.** C0 and C2 move nothing in the leg, because the reference lock is held under the design.
- **The figures.** The author's `counter` and `legs5` sections re-run byte-identical. They show 200 HOLDOVER entries and LOCKED 2.6 s after the leg, a loss-count and window-phase difference from mine.

### Item 3: the suggestions

- **k = 0 and aliasing** (`:765-777`). My `alias` section ran every run of 1 to 600 lost PDUs, from start positions 0 to 15, at 0, +300 and -300 ppm: 28,800 cases.
  - None departs from "one restart if and only if two or more groups are voided".
  - The page's 42 named cases each restart once: whole runs of 2 to 33 groups, and 255, 256, 257 and 512 PDUs from PDU 0 and PDU 5.
  - One whole lost group restarts nothing.
  - k = 0, 15 voided groups, restarts once.
  - The 32 ms argument holds.
- **The deviation check up to the gap** (rule 1, `:751-759`; `:788-793`; `:959-966`). This is the author's design statement, which REVIEW READY offers for judgement.
  - **I accept it.** It is what a compare made as each PDU arrives does. It needs no verdict held to the group's end.
  - **It costs nothing.** It uses the compare that the void and the status word's largest deviation already make.
  - **It is consistent with the rest of the page:** the pick's "every PDU is required", rule 2, and the History bullet's "(before a gap too)".
  - **Both readings catch every step under the design** (`receipts/pdu_steps.out`). The page's reading gives 120 single restarts: 56 at the step's PDU, which are positions 1 to 14 of placement (b), and 64 at the next pick. The no-cross-check mutant then leaves the 64 unrestarted, with LOCKED dropping exactly twice in each, and the 56 still restart. Under round 4's reading, with the verdict at PDU 15, the design still restarts all 120 once, and the mutant fails all 120, as the REVIEW READY says.
  - **Recommendation:** keep rule 1 as written. The step row (`:1301`) matches it.
- **The gap bound's value** (`:818-826`, row `:1300`). My sweep finds that (a) stops restarting from 5,100 ns, and (b) restarts up to 6,364 ns. The design's 5,120 ns passes both. 4,096 ns fails (a), and 6,365, 6,400 and 8,192 ns fail (b). The row kills a wrong bound in either direction. On the 2 ns against the table, see S3.
- **"Exact for any constant talker rate"** (`:782-786`). The fill run at +100 ppm, with PDU 5 of a snapshot group lost, gives rates identical to the no-loss run (0 ns) and no restart. A 50 ppm change at any of 32 positions inside the 4 ms moves the midpoint by at most 38 ns, 0.76 ns per ppm, inside the stated 1 ns per ppm.
- **"LOCKED drops twice in each of them"** (`:933`): confirmed, 2 in each of the 64.
- **The baseline line** (`:61-64`, `:1427-1429`). PR #630 is MERGED, its merge commit is `7f0927bb3377d67d5455ef7cc336ab93adb58dcd` (2026-10-01T18:49:45Z), and that is live dev. The text is correct, and the page still cites the PR.

## Prior public findings at this head

| Finding | State at `f4f0ecb4` | Where |
|---|---|---|
| R429-4 F1, shared with R428-4 F1 (random-loss cliff) | Resolved: re-derived independently, above | `:736-740`, `:667-673`, `:838-891`, `:1417-1426`; PR body Round 5 item 1, Known limitations; the Round 4 table row annotated "Corrected in round 5" |
| R429-4 F2, shared with R428-4 F2 (the counter leg had no mutant) | Resolved: the mutant is shown killing both legs | `:1311`, `:1305`, `:967-973`, `:1186-1188` |
| R429-4 S1 (deviation check in a loss-voided group; "drops twice"; k = 0) | Taken | `:755-759`, `:765-777`, `:926-944`, `:1301` |
| R428-4 S1 (k = 0, alias in group intervals) | Taken | `:767-777` |
| R428-4 S2 (grade the 5,120 ns bound at both edges) | Taken | `:818-826`, `:1300` |
| R428-4 S3 ("constant" rate) | Taken | `:782-784` |
| Rounds 1 to 4 findings | Unregressed: the round-5 diff removes only the cliff text that F1 required, the old step row, and the "unmerged" Limits item | `git diff 1bdd6895 f4f0ecb4`, its removed lines |

## Lens coverage at this head

```text
[R429] PASS Conformance - docs/design/MEDIA_CLOCK_FOLLOWING.md:6-45, :729-793, :959-973, :1183-1188 at f4f0ecb4 - round-5 rules (loss void up to the gap, k other than 1 and 2 restarts, 8-bit sequence_num alias) checked against IEEE 1722-2016 4.4.4.6 as cited and the rulings 5935520588, 5937449258, 5937643550, 5937848189 and the option (b) assignment; no ruling is restated differently; round-5 assignment items 1-3 met; "Relates to #629" at :6 and in the PR body
[R429] PASS RTL - hdl/ieee1722/crf/KL_mmcm_drp_servo.sv:228-233, :562-579, :609-618, :643-648; hdl/ieee1722/crf/KL_crf_rx.sv:296-298, :398-400, :569-570 at f4f0ecb4 - every RTL claim the round-5 text adds (HOLDOVER on lock fall :564, two-window skip :576-577 and :617-618, PI and lock count held on an invalid rate :613-615, settle broken but lock held on a gap :569-570) read against the source and reproduced in scripts/pdu_model.py
[R429] PASS Robustness - receipts/random_loss/, receipts/locktime_pop/, receipts/pdu_alias.out, receipts/pdu_gapbound.out, receipts/pdu_fill.out - the loss envelope (0.8 to 24 lost PDUs a second), 28,800 alias runs at three rates, the gap bound at both edges and the midpoint fill against :729-951 and :1417-1426; no escape, and every figure within sampling of the page
[R429] PASS Tests - docs/design/MEDIA_CLOCK_FOLLOWING.md:1283, :1300, :1301, :1305, :1311 at f4f0ecb4; receipts/pdu_steps.out, receipts/pdu_servoleg.out, receipts/pdu_counter.out, receipts/pdu_legtrim.out - each new or changed row's named mutant fails it and the design passes it in an independent model (step row 120 cases, 64 killed; gap-bound row both edges; held-lock mutant in the servo and counter legs; the counter leg kills no other named level)
[R429] PASS Docs - docs/design/MEDIA_CLOCK_FOLLOWING.md (git diff 1bdd6895 f4f0ecb4, only file changed), PR #631 body (equal to the prepared body), receipts/gates/ - docs_check, check_doc_style, gen_toc --check and --verify-anchors, check_em_dash --base d4dd7426, check_doc_paths, check_entity_shape and git diff --check on both ranges all rc 0 in the pinned Markdown environment; worktree status empty before and after; no private names in the added lines; three SUGGESTIONs only
```

## Reviewer-owned completion ledger

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | design page `:6-45`, `:729-793`, `:959-973`, `:1183-1188`; #629 body, rulings and owner decisions; PR body | R429-5 | `f4f0ecb4b41866cd30875e08e74114868ece5b4c` |
| RTL | CLEAN | `KL_mmcm_drp_servo.sv:228-233, :562-579, :609-648`; `KL_crf_rx.sv:296-298, :398-400, :569-570` against the page's RTL claims | R429-5 | `f4f0ecb4b41866cd30875e08e74114868ece5b4c` |
| Robustness | CLEAN | closed form; group-level Monte Carlo (32-seed table and a 512-seed population); PDU-level alias, gap-bound and fill sections | R429-5 | `f4f0ecb4b41866cd30875e08e74114868ece5b4c` |
| Tests | CLEAN | test-plan rows `:1300`, `:1301`, `:1305`, `:1311` and the mutant contract `:1283`; PDU-level steps, servo leg, counter leg and leg-trim sections | R429-5 | `f4f0ecb4b41866cd30875e08e74114868ece5b4c` |
| Docs | CLEAN (S1 to S3 are SUGGESTIONs) | round-5 diff; PR body; gates; author packet manifest | R429-5 | `f4f0ecb4b41866cd30875e08e74114868ece5b4c` |

This head is the merge candidate's source head. The ledger covers this head only. A later commit that touches the page un-covers the lenses whose scope it changes.

## Executed evidence

Every command ran in the foreground, from the clean clone at the exact head. Disposable trees went under `scratch/`, which is not published.

- **`scripts/formula_check.py`** writes `receipts/formula_check.out`, rc 0.
- **`scripts/random_loss_model.py <lost/s> <secs> <seeds> [phi] [seed_base] [--raw]`:**
  - the table runs are `receipts/random_loss/*.out` and `*.rc`, all 0;
  - the 512-seed population is `receipts/locktime_pop/*.out` and `*.rc`, all 0;
  - `scripts/pool_locktimes.py` writes `receipts/pool_locktimes.out`.
- **`scripts/pdu_model.py <section>`,** for the sections steps, gapbound, alias, fill, servoleg, counter and legtrim, writes `receipts/pdu_<section>.out`, `.err` and `.rc`, all rc 0 with empty stderr. The steps and alias sections use 8 worker processes.
- **The author's model** `meter_rules_model_r5.py` (sha256 `cf3ac84f...`) was re-run for formula, counter, gapbound, alias, legs5, random and steps5. Each run is rc 0 and byte-identical to the published section (`receipts/author_replay/`).
- **The gates** (`receipts/gates/`, each `.out` with its `.rc`) ran in the pinned Markdown environment, whose lock file equals the tree's `tools/markdown/requirements.txt`: `cmarkgfm 2025.10.22`, `html5lib 1.1`. Every gate is rc 0:
  - docs_check: 0 findings;
  - check_doc_style: OK;
  - gen_toc --check: OK;
  - gen_toc --verify-anchors: 292 links;
  - check_em_dash --base d4dd7426: 0 findings over 1,444 added lines, arms 339/339;
  - check_doc_paths: 875 paths;
  - check_entity_shape: 166 checks, 0 failures;
  - git diff --check on d4dd7426..f4f0ecb4 and 1bdd6895..f4f0ecb4.
- **Clone integrity** (`receipts/clone_integrity.txt`):
  - HEAD and tree are as stated, and the status is empty;
  - worktree = index = HEAD;
  - no assume-unchanged or skip-worktree flag;
  - 983 index entries match the tree, 979 regular files hash-equal with matching modes;
  - gitlinks: `protocol-processor` `b2db3a97`, `gptp-processor` `5dce647a`, `third_party/verilog-axis` `48ff7a7e`, `external` `efeb541a` (uninitialised, as found).

  No file in the clone was modified at any point.
- **Hosted checks at the exact head** (`receipts/hosted_check_runs.tsv`, re-queried in `receipts/hosted_docs_check_requery.tsv`, 2026-10-01T21:10Z):
  - success: changes, docs-check-no-git, wire-accountability, full-ci-gate, bdd-conformance, elaborate and rtl-fast;
  - skipped: verilator-suites, yosys-portability, verilator-lint, yosys-elaboration, both shard matrices and Physical gPTP;
  - still in progress at the re-query: docs-check.

  A skipped context is not executed evidence.

## Limits

- **Design only.** Nothing here is implemented, and no RTL of this design was simulated. My models are desk models of the page's rules and of the servo's PI and state machine. They do not model any real talker or network, nor the servo's fine phase-shift actuator, PHC step and slew guards, or gPTP wander.
- **Error shapes.** The PDU-level checks used independent uniform error, or ideal timestamps where the page says so. The worst-case error shapes were not re-run in this round, because the round-5 diff does not change them.
- **Two model choices:**
  - **Window phase.** It was calibrated so that a cold start without loss locks at 7.3 s, the page's figure. Phase 0 locks at 7.7 s and moves the medians by under 2 s at 8 and 11.2 a second, and by about 35 s at 24 a second.
  - **The plant.** The command set at a boundary applies over the next window.
- **Not run:** physical calibration, any bench or hardware case, the full parent, PP, gPTP, Yosys and builder banks, Docker or act. Field skips are not hardware proof.
- **This is source validation,** distinct from the final current-dev candidate. The source base is `d4dd7426`; live dev is `7f0927bb`.

## Pending manager duties

- Build and validate the final current-dev candidate at the merge turn: source base `d4dd742679b902b2bc5eedf89d525066d59aafbb` on live dev `7f0927bb3377d67d5455ef7cc336ab93adb58dcd`.
- Own hosted and act acceptance. At the re-query, `docs-check` was still in progress at this head, and the long RTL and Yosys contexts were skipped.
- Publish `run_gates.sh` into the author-r5 packet, or correct its manifest and the PR body's mention (S2).
- Publish this report with the files listed in `MANIFEST.sha256`.
- The implementation, simulation and bench items of #629 stay open. This PR relates to #629 and does not close it.

R429-5 FINISHED
