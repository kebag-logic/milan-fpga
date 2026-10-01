[R428] POSITIVE - exact head f4f0ecb4b41866cd30875e08e74114868ece5b4c

# R428-5: internal cleared-context review of PR #631 (#629, lane M1, design only), round 5

Exact head `f4f0ecb4b41866cd30875e08e74114868ece5b4c`, tree
`a3a3fadd634b76469f7359628697ff527686a3c5`. Round 5 is one docs commit on the
round-4 head `1bdd68957dd1`. Against `1bdd6895` it changes only
`docs/design/MEDIA_CLOCK_FOLLOWING.md` (+153 / -50). Against the source base
`d4dd742679b9` the PR is still two files: the new page and its index row in
`docs/README.md` (receipts `gates/diff_names_r4.out`, `gates/diff_names_base.out`).

## Verdict

POSITIVE. No BLOCKER, MAJOR or MINOR is open at this head. Two SUGGESTIONs
follow; they are optional and do not affect coverage.

- **Round-4 F1 (random loss) is resolved.** The cliff is gone. The page now
  gives a graded falloff: restarts at about 500 q^2 a second (exactly
  500 q^2 (1 - q)), the rate valid about e^(-4.096 x 500 q^2) of the time, a
  table at 0.8 to 24 lost PDUs a second, and cold-start lock times. My own
  model, written from the page and the servo RTL, reproduces the falloff:
  - restart rates match to within the seed spread;
  - validity is 0.60, 0.36 and 0.013 at 8, 11.2 and 24 lost PDUs a second, against the page's model figures of 0.60, 0.37 and 0.015;
  - every seed locks and no case drops LOCKED.

  The cold-start medians agree to within the spread of a 32-seed sample (S2).
  The same correction appears in Limits, "What round 3 cost", the "Residual"
  bullet and the live PR body.
- **Round-4 F2 (the counter row's loss leg) is resolved.** The counter row and
  the servo-with-meter row now name the mutant "the meter's held lock cleared
  on a sequence gap". In my 1 ms model of the meter lock and the servo state
  machine (`KL_mmcm_drp_servo.sv:562-579`, `:603-618`, `:677-697`):
  - the design moves no counter during the leg;
  - the mutant enters HOLDOVER 200 times, counts UNLOCKED once at the first lost PDU and LOCKED only 2.64 s after the last loss, and runs no PI window in the leg;
  - C0, C2 and restart-on-any-loss move nothing;
  - in the servo row, the mutant leaves LOCKED at the leg's first loss and ends 4.00 ppm off the stepped talker, while the design ends at 0.00 ppm.

  So both legs fail under the named mutant, and the counter leg grades that
  mutant alone, as the page says.
- **Every round-4 suggestion was taken and is correct.** I checked each one with
  my own model: k = 0 and the alias; the deviation check up to a gap with the
  rebuilt 120-case step row (the mutant fails exactly 64); the 5,120 ns
  gap-bound row (both edges pass only for 5,100 to 6,364 ns); "exact for any
  constant talker rate"; and "LOCKED drops twice in each of them".
- **The stale baseline line is corrected.** PR #630 is MERGED, with merge commit
  `7f0927bb3377d67d5455ef7cc336ab93adb58dcd`, which is also the live `dev` tip
  (checked through the public API).
- **Gates.** Every documentation gate, `check_entity_shape.py` and
  `git diff --check` (against both the base and round 4) exit 0 at this head.
  A render check finds 24 tables and 198 body rows, none irregular. The PR body
  says "Relates to #629" and does not close it. It is byte-identical, modulo
  trailing whitespace, to the packet's PR-BODY.md, and a scan finds no private
  names or paths.

## How the task was reconstructed

1. AGENTS.md and CONTRIBUTING.md (section 3, the verification bar; section 6,
   wording, privacy and the em-dash rule); the design-index row in
   `docs/README.md`.
2. Issue #629: the body (owner decision, work items, proof and acceptance), then
   the manager and owner comments: the lane M1 assignment 5935051587, the
   rulings 5935520588 and 5937449258, the owner's D4 = A2-a decision 5937643550,
   the accuracy note 5937738214, the known-risk decision 5937848189, and the
   round 5 assignment 5939246995. Then the round-5 TAKEN (5939262004) and
   REVIEW READY (5940218896).
3. Interface authorities the round-5 text rests on, re-read at this head:
   - `hdl/ieee1722/crf/KL_mmcm_drp_servo.sv`: the parameters `:228-233`, the FSM `:537-587`, the window and the PI run gate `:596-623`, the writeback `:677-697`;
   - `hdl/ieee1722/crf/KL_crf_rx.sv`: `:290-298`, `:389-403`, `:565-570`.
4. `git diff d4dd7426..f4f0ecb4` and `git diff 1bdd6895..f4f0ecb4`, read in
   full; the log of the eight branch commits. I also read the meter sections at
   this head in full (`:540-1010`, `:1290-1310`, `:1356-1443`).
5. Public executable evidence: the author's round-5 packet
   `review-evidence/629-r1/author-r5` on branch `629-review-evidence` at
   `5c89a6c6` (the linked tree `0c17547b` holds only the round-1 packet). Its
   gates and model sections all show rc 0. I read the C, V5, G, Z, S5 and N
   outputs and the round-4 comparison after my own model had run.
6. Prior public findings: R428-4 (5939246407) and R429-4 (5939232297), read only
   after my verdict and ledger were drafted.

## Findings

No BLOCKER, MAJOR or MINOR.

### S1 - SUGGESTION - Tests, Docs - the gap-bound row says "ideal timestamps", but its case (b) carries +/-J offsets

- **Where:**
  - `docs/design/MEDIA_CLOCK_FOLLOWING.md:818-826`;
  - the test-plan row "The gap bound's value" at `:1300`.
- **Authority and evidence:**
  - The paragraph opens "graded at both edges, with ideal timestamps" and then gives (b) "picks at +J before the gap and -J after it".
  - The row's stimulus column also says "ideal timestamps" before stating, for (b), every timestamp at +1,426 ns before the step and -1,426 ns from it.
  - The arithmetic is right. My model applies (b) with those constant offsets and finds 6,365 ns, and the pair passes only for a bound of 5,100 to 6,364 ns (`model/out/meter.out`).
  - Separately, `:821` is one source line of 128 characters. That is cosmetic, and the style gate passes.
- **Impact:** an implementer might drive (b) with random ±J error and not the
  constant opposing offsets. The edge would then not be reproduced exactly.
- **Required outcome (optional):** say "no random error" or "ideal timestamps
  except for the stated offsets", and re-wrap `:821`.
- **Verification:** re-read `:818-826` and `:1300`.

### S2 - SUGGESTION - Docs, Robustness - the cold-start medians are single 32-seed samples; give their spread

- **Where:** `:861-878` (the table and the comparison with the round-4 reviews),
  and Limits `:1423-1425` ("7.8 s ... 17.3 s ... 288 s").
- **Authority and evidence:** my group-level model has the servo PI, the lock
  count, and an invalid window holding both (`model/out/random.out`,
  `model/out/medians.out`). With 256 seeds at a random window phase, 32-seed
  block medians range over:
  - 7.8 to 11.6 s at 8 lost PDUs a second (256-seed median 9.8 s);
  - 11.5 to 16.7 s at 11.2 a second (256-seed median 14.2 s);
  - 248 to 354 s at 24 a second (256-seed median 296 s).

  The page's 7.8 s and 288 s lie inside these ranges. Its 17.3 s at 11 a second
  lies just above. The author's own receipt reproduces 17.3 s from its seeds
  (`author-r5/model/sections/random.out`). The difference is sampling and
  modelling detail, not a defect. The qualitative claims hold in my model:
  validity falls smoothly, every seed locks, and no case drops LOCKED. The same
  spread also covers the page's sentence that 17.3 s sits below the 18.5 s
  round-4 figure because the servo holds its PI.
- **Impact:** none on the design. A bench or implementation lane could read
  17.3 s as a precise prediction.
- **Required outcome (optional):** say that the medians vary by a few seconds
  between seed sets, or quote a larger-seed figure.
- **Verification:** re-read `:870-878`.

## Round-5 items, judged

- **Item 1, random loss (R428-4 F1 = R429-4 F1): RESOLVED.**
  - **The formula.** `model/out/formula.out`: 500 q^2 = 0.1261, 0.2457 and 1.1014 at p = 1e-3, 1.4e-3 and 3e-3. The approximate validity is 0.597, 0.366 and 0.011; the exact validity is 0.602, 0.374 and 0.0136. The page rounds these correctly.
  - **The falloff points.** The exact-rate validity reaches 90 / 50 / 10 / 1 % at 3.61 / 9.37 / 17.34 / 24.88 lost PDUs a second, matching "3.6, 9.4, 17, about 25".
  - **The round-3 rule.** It gives 0.374 at p = 3e-5, and 1 % at 1.124 lost PDUs a second.
  - **The round-4 single-seed rows.** Expected restarts are 0.38 and 37.23, and expected validity with the fill is 0.981 and 0.593.
  - **The spread.** One 300 s run at p = 1e-3 has sd 0.053 over 64 seeds (`model/out/spread.out`), matching "about 0.05".
  - **The model table.** `model/out/random.out`, against the page:

    | Lost/s | Restarts/s | Valid | Lock median, middle half, slowest | Drops | Unlocked seeds |
    |---|---|---|---|---|---|
    | 0.8 | 0.0016 | 0.993 | 7.3 s; 7.3-7.3; 7.3 | 0 | 0 |
    | 4.0 | 0.0305 | 0.883 | 7.3 s; 7.3-7.3; 10.9 | 0 | 0 |
    | 8.0 | 0.123 | 0.603 | 11.4 s; 7.3-13.0; 22.1 | 0 | 0 |
    | 11.2 | 0.247 | 0.360 | 16.7 s; 10.2-21.6; 37.0 | 0 | 0 |
    | 16.0 | 0.482 | 0.141 | 29.8 s; 18.3-48.2; 71.3 | 0 | 0 |
    | 24.0 | 1.04 | 0.013 | 261 s; 146-360; 784 | 0 | 0 |

    The restart and validity columns agree with the page's model columns
    within the seed spread. The lock medians are taken up in S2.
  - **No stale text.** "never validates", "does not lock" and "cliff" no longer appear for random loss. The remaining "never validates" (`:668`, `:720`) is correlated error beyond the tolerance. The deterministic statement is kept (`:843-846`).
- **Item 2, the counter row's loss leg (R428-4 F2 = R429-4 F2): RESOLVED.**
  - **The counter leg would fail.** Its pass criterion, "neither moves during the PDU-loss leg", is broken by the mutant, which counts UNLOCKED at 20.1 s, inside the leg (`model/out/counter.out`).
  - **The servo-with-meter leg would fail.** "LOCKED ... never left" is broken at the first loss, and the trim check fails: 4.00 ppm off against 0.5 ppm allowed (`model/out/servoleg.out`).
  - **The page's figures fit.** 200 HOLDOVER entries; LOCKED 2.6 s after the leg (mine 2.64 s after the last loss, within the bound of two skipped windows plus four qualifying windows); the trim frozen.
  - **The citations are correct.** `:564` (HOLDOVER on a lock fall), `:576-577` (skip 2, lock count cleared on return) and `:617-618` (the skip decrement).
- **Suggestions: all taken and correct.**
  - **k = 0 and the alias** (`:767-777`). In my PDU-level model of the rules, 1 lost group restarts nothing. Runs of 2 to 33 whole lost groups each restart once. 255, 256, 257 and 512 lost PDUs from PDU 0 or PDU 5 each restart once, by the mechanism the page names (spacing, k = 2 across the gap, or deviation). Receipt `model/out/meter.out`.
  - **The deviation check up to a gap** (`:755-759`). The author asks whether this reading or the other is preferred. My judgement: either reading is sound. Both catch every step: the check across the gap sees the whole of any step in or beside a voided group. Checking up to the gap catches 56 of the 120 cases earlier. Within tolerance it costs no validity, and beyond tolerance only groups that are never valid restart a little more often. It is also what a streaming compare naturally does, so I accept the design statement. The rebuilt step row matches my model exactly: in the design, 120 of 120 cases restart once (60 in (a) and 4 at (b) position 0 across the gap, 56 by deviation); under the no-check mutant, 64 do not restart and the 56 still do. The mutant's carried step drops LOCKED exactly twice for each step size and sign (`model/out/steploop.out`).
  - **The gap-bound row** (`:818-826`, `:1300`). (a) lands at 5,100 ns and (b) at 6,365 ns. A sweep of every bound from 4,096 to 8,192 ns passes the pair for exactly the contiguous range 5,100 to 6,364. The bound row's "gap of more than one voided group accepted" mutant is killed in its first three cases. See S1 for wording only.
  - **"Exact for any constant talker rate"** (`:782-784`). With a rate change of D ppm at the snapshot instant, the midpoint of the picks at -2 ms and +2 ms misses by D x 1e-6 x 1 ms = D ns, so "at most 1 ns per ppm of change" is right.
  - **"LOCKED drops twice in each of them"** (`:933`). Correct, as above.

## Lens results (each with its artifact)

```text
[R428] PASS Conformance - docs/design/MEDIA_CLOCK_FOLLOWING.md:729-956,1290-1310 at f4f0ecb4; #629 body; comments 5935051587, 5935520588, 5937449258, 5937643550, 5937848189, 5939246995 - round 5 changes no clause reading and no ruling; D1 to D8 are recorded as ruled (:1359-1370); the PR stays design only and "Relates to #629" (diff_names_r4/base); the issue's simulation acceptance ("lock loss ... graded by a failing mutant") is served by the newly named held-lock mutant; the frozen acceptance is unchanged
[R428] PASS RTL - hdl/ieee1722/crf/KL_mmcm_drp_servo.sv:228-233,537-587,596-623,677-697 and KL_crf_rx.sv:290-298,389-403,565-570 at f4f0ecb4, against page :755-786,:838-846,:946-951,:967-973,:1385-1393 - every line the round-5 text cites says what the page says; k from sequence_num[7:4] modulo 16 and the 32-bit midpoint are width-consistent; "the deviation check up to a gap adds nothing" means one gating flag on an existing compare, inside the 40-70 LUT / <10 FF estimate
[R428] PASS Robustness - model/out/{random,spread,medians,meter,counter,servoleg}.out - independent loss from 0.8 to 24 lost PDUs a second; periodic loss; long gaps and every alias case (k = 0; 17 and 18 intervals; 255/256/257/512 PDUs at two phases); both edges of the gap bound; the held-lock fault; no case drops LOCKED or fails to lock; S2 is presentation only
[R428] PASS Tests - page test-plan rows :1300 (gap bound), :1301 (steps in a loss-voided group), :1305 (servo with meter), :1311 (counters) at f4f0ecb4, against model/out/{meter,steploop,counter,servoleg}.out - each new or changed check fails under its named mutant, and only for the stated cases; S1 is wording only
[R428] PASS Docs - gates/*.out and *.rc (docs_check, check_doc_style, gen_toc --check and --verify-anchors, check_em_dash against d4dd7426 and 1bdd6895, check_doc_paths, check_entity_shape, git diff --check against both), model/table_check.out, the live PR #631 body - all rc 0; 24 tables and 198 rows with no irregular row; the stale "unmerged" baseline is corrected and PR #630's merge at 7f0927bb is confirmed; no private names; the PR body equals the packet's PR-BODY.md
```

## Reviewer-owned completion ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | page `:729-956`, `:1290-1310`, `:1359-1370`; the #629 body; rulings 5935520588 and 5937449258; owner decisions 5937643550 and 5937848189; assignment 5939246995 | R428-5 | `f4f0ecb4b41866cd30875e08e74114868ece5b4c` |
| RTL | CLEAN | `KL_mmcm_drp_servo.sv:228-233,537-587,596-623,677-697`; `KL_crf_rx.sv:290-298,389-403,565-570`; page `:755-786`, `:946-951`, `:967-973` | R428-5 | `f4f0ecb4b41866cd30875e08e74114868ece5b4c` |
| Robustness | CLEAN | `model/r428_5_model.py`; `model/out/random.out`, `spread.out`, `medians.out`, `meter.out`, `counter.out`, `servoleg.out` | R428-5 | `f4f0ecb4b41866cd30875e08e74114868ece5b4c` |
| Tests | CLEAN | test-plan rows `:1297-1311`; `model/out/meter.out`, `steploop.out`, `counter.out`, `servoleg.out`; author-r5 sections C, V5, G, Z, S5 | R428-5 | `f4f0ecb4b41866cd30875e08e74114868ece5b4c` |
| Docs | CLEAN | `gates/*.out`, `gates/*.rc`; `model/table_check.out`; the PR #631 body; `docs/README.md` index row | R428-5 | `f4f0ecb4b41866cd30875e08e74114868ece5b4c` |

Only SUGGESTIONs remain open (S1: Tests, Docs; S2: Docs, Robustness), so they do
not un-cover any lens. Every lens was applied at the merge candidate's source
head.

## Prior public findings on PR #631, at this head

- **R428-4 F1 (MINOR, Robustness, Docs): RESOLVED.** See item 1. The falloff
  is stated and reproduced, cold-start lock is stated as probabilistic,
  Limits and the PR body are corrected, round 3's comparison is restated, and
  the deterministic statement is kept.
- **R428-4 F2 (MINOR, Tests): RESOLVED.** See item 2. The mutant is named in
  both rows and fails both legs.
- **R428-4 S1, S2, S3 (SUGGESTION): taken.** k = 0 and the alias stated in
  group intervals; a gap-bound value row graded at both edges; "constant".
- **R429-4 F1 (MINOR, Robustness, Docs) and F2 (MINOR, Tests): RESOLVED.**
  They are the same defects as R428-4 F1 and F2, with the same fixes and
  verification.
- **R429-4 S1 (SUGGESTION): taken.** The precedence is stated (the deviation
  check runs up to the gap), the step row and its mutant positions are
  rebuilt to match (fails 64 of 120), k = 0 is stated, and "in each of them"
  is written.
- **Rounds 1 to 3 (R428-1 to R428-3, R429-1 to R429-3).** Both round-4
  reviews found every one resolved at `1bdd6895`. I read the round-5 diff in
  full, and it touches none of those resolutions: only the loss section, three
  test-plan rows, two bullets in "History, lock, era and outputs", the D5
  rationale, the "Residual" bullet, the baseline line and Limits change. I did
  not re-derive the earlier findings from scratch this round.

## Executed evidence (all under this packet)

- `gates/`: every gate above with its output and rc, the exact head, and the
  clone's status before and after (both empty). `gates/md_venv_locked_pins.txt`:
  the Markdown environment's cmarkgfm 2025.10.22, html5lib 1.1, cffi 2.1.1,
  pycparser 3.0, six 1.17.0 and webencodings 0.6.1 match
  `tools/markdown/requirements.txt`. `gates/hosted_check_runs.tsv`: the
  exact-head hosted check runs as queried (see the manager duties below).
- `model/r428_5_model.py` (standard library only, deterministic) and
  `model/run_model.sh`. `model/out/<section>.out` and `.rc`: eight sections,
  all rc 0. `model/out/second_run.txt`: a second run of all eight is
  byte-identical.
- `model/table_check.py`, `.out`, `.rc`: the pinned-renderer table check.
- `gates/clone_integrity.txt`, the clone after review:
  - HEAD, tree and index tree are `f4f0ecb4` / `a3a3fadd` / `a3a3fadd`;
  - no modified or untracked file; `git diff-index` is clean;
  - the page's and README's blob hashes equal HEAD's;
  - the four gitlinks are mode 160000 at stage 0 in both the index and HEAD: external `efeb541a` (uninitialised, as found), gptp-processor `5dce647a`, protocol-processor `b2db3a97`, verilog-axis `48ff7a7e`.

  No probe touched the clone; every model ran from this packet.

## Real limits

- **Design only.** Nothing here is implemented, and no RTL of this design was
  simulated in this round. My figures come from a desk model of the page's
  rules:
  - the random-loss section is group-level, which is exact for independent loss except aliasing;
  - the servo is modelled at window resolution (PI, clamps, slew, lock count) on a plant of gain 1, one window late, with ±20 ns of quantisation;
  - the legs are modelled at 1 ms resolution (meter lock, HOLDOVER, the two-window skip);
  - the fine phase-shift actuator, the PHC step and slew guards, and gPTP wander are not modelled.
- **Standards text.** I did not re-read the standards clauses this round,
  because round 5 changes no clause reading. The Conformance result rests on
  the issue, the rulings and the unchanged clause text of earlier rounds.
- **Physical calibration NOT RUN.** No bench and no hardware. Field skips are
  not hardware proof.
- **Not run.** No full parent, processor, gPTP, Yosys or builder bank, no
  container or local CI replica, and no hosted run triggered.

## Pending manager duties

- **Hosted checks.** At my query (`gates/hosted_check_runs.tsv`), `docs-check`
  was `in_progress` on this head. `rtl-fast`, `changes`, `bdd-conformance`,
  `docs-check-no-git`, `wire-accountability`, `full-ci-gate` and `elaborate`
  had succeeded. `verilator-suites`, `yosys-portability`, `verilator-lint`,
  `yosys-elaboration`, the shard matrices and physical gPTP were skipped, as
  expected for a docs-only head. Exact-head hosted acceptance and the act
  replica are the manager's.
- **Merge preparation.** The current-dev candidate merge build and validation:
  source base `d4dd7426`, live dev `7f0927bb`.
- **Remaining review.** The R429-5 external verdict; two independent POSITIVE
  reviews and the full section 7 bar before any merge; explicit maintainer
  authorization to merge.
- **Publication.** Publishing this report and the MANIFEST-listed receipts.
- **The issue.** #629 stays open (the PR relates to it and does not close it).
  Its implementation, simulation and bench items remain for later lanes.

R428-5 FINISHED
