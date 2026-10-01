[R429] NEGATIVE - exact head 1bdd68957dd1357645c500014002b1e5a115864c

# R429-4: external review of PR #631 (#629, lane M1, design only), round 4

Exact head `1bdd68957dd1357645c500014002b1e5a115864c`, tree `7e3d8c95ea755c9a225cff1a70df650c49b0d7f0`. Two docs commits on round 3's head `a463a1de`: `0cf1ef48` and `1bdd6895`. They change only `docs/design/MEDIA_CLOCK_FOLLOWING.md` (+337 / -102).

## Verdict

NEGATIVE, on two MINOR findings. There is no BLOCKER or MAJOR.

- **What is resolved.** Every prior finding is resolved at this head: R429-3 F1 and F2, and R428-3 F1. The rulings are recorded on the page and in the PR body. The loss rule, option (b), is sound where it matters:
  - a lost PDU voids only its own group;
  - the check across one voided group (4 ms +/- 5,120 ns) and the midpoint fill behave as stated;
  - the bound derivation is exact;
  - the "share a group, or lie at least 32 PDUs apart" validity region is tight.
- **Reproduction.** An independent model written from the page text reproduces every loss-table figure I re-derived. The author's model re-runs byte-identical to its published output: 40/40 shared no-loss cases, 204 lossy shape cases with no restart and no drop, and 64/64 in-gap steps.
- **F1 (Robustness, Docs).** The page calls about 11 lost PDUs a second of random loss a cliff, where "the rate never validates" and "a cold start does not lock". At that rate the rate is valid in about 37 to 39 % of windows, and a cold start locks (at 20.6 s in my model). Validity falls off as exp(-500 q^2 x 4.096 s). It reaches about 1 % only near 24 lost PDUs a second.
- **F2 (Tests).** The counter row's new PDU-loss leg names no mutant that fails it. Neither named mutant (C0, C2) moves a counter during PDU loss, and neither does the restart-on-any-loss mutant. That breaks the page's own rule that each new check is shown failing under a named mutant. It also breaks the REVIEW READY claim "Each has a failing mutant".

Both fixes are text-only and cheap.

## How the task was reconstructed

Sources, in order:

- **Repository rules:** AGENTS.md, CONTRIBUTING.md (by reference) and `docs/README.md` (the index row at `:72`).
- **Issue #629:** the body, then the manager comments on it:
  - rulings 5935520588 (round 1) and 5937449258 (round 3);
  - the owner decisions 5937643550 (D4 = A2-a) and 5937848189 (the known risk, superseding the accuracy note 5937738214);
  - the round-4 assignment 5938156583 and REVIEW READY 5938892492;
  - the start comment 5938919910.
- **The diffs:** `git diff d4dd7426..1bdd6895` (2 files, +1,341) and `a463a1de..1bdd6895`. I read the whole page at the head, and the round-4 removals line by line.
- **The cited RTL, re-read at the head** (unchanged from `d4dd7426`): `KL_mmcm_drp_servo.sv:228-233`, `:538-579`, `:606-700`; `KL_crf_rx.sv:320-329`, `:390-403`, `:569-570`; `KL_avtp_rx_monitor_ctx.sv:24-28`, `:173-174`; `sw/litex/milan_soc.py:226-234`, `:339-358`.
- **Public evidence:** the author's round-4 packet on branch `629-review-evidence` at `1ef4ddb858c3041879a4e26fdcb3b0309cf6a888`, under `review-evidence/629-r1/author-r4/`. The tree link given in the assignment (`0c17547b`) holds only the round-1 packet.
- **Prior public reviews:** R429-3 and R428-3, read only after my own pass, my model and my findings were written.

## Findings

### F1 - MINOR - Robustness, Docs - random PDU loss at about 11 per second is stated as "never validates", and it does not

- **Where:**
  - `docs/design/MEDIA_CLOCK_FOLLOWING.md:817-825`: "The rate never validates only if these gaps recur within every 4.1 s ... p = 1.4e-3, 11 lost PDUs a second: one restart in 4.1 s, the cliff."
  - `:1320-1324` (Limits): "if that recurs within every 4.1 s the rate never validates: about 11 lost PDUs a second under independent loss ... a cold start does not lock."
- **Authority and evidence:**
  - Under independent loss, restarts form a near-Poisson process at a rate of lambda = 500 q^2 per second. The rate is valid only in the part of each inter-restart interval beyond 4.096 s, so the valid fraction is exp(-lambda x 4.096 s).
  - At p = 1.4e-3 (11.2 lost PDUs a second) the mean interval is 4.1 s, as the page says. But 37 % of intervals are longer, so the expected valid fraction is 0.366.
  - My model simulated 300 s at p = 1.4e-3 (`model/r429_4_loss_model.out`, section "random loss"): 74 restarts, rate valid in 0.386 of windows, a cold start LOCKED at 20.6 s, 0 drops. At p = 1e-3 it gave 0.618.
  - The author's own model agrees on the trend (`meter_rules_model_r4.out:138-140`, re-run byte-identical):
    - p = 1e-3: valid 0.546, LOCKED at 17.6 s;
    - p = 3e-3 (24 per second): valid 0.014, LOCKED at 254.6 s.
  - So there is no cliff at 11 per second. "Never validates" and "a cold start does not lock" are wrong at that rate. The roll-off is gradual: about 60 % valid at 8 per second, 37 % at 11, and 1 % at about 24.
  - The statement errs on the pessimistic side, and round 3's "cliff at 3e-5" uses the same mean-interval definition. The page's own conditional, "if gaps recur within every 4.1 s", is true. Its equation with a random-loss rate is not.
- **Impact:** the Limits section is the place an implementation, bench or release reader takes the operating envelope from. It mis-states that envelope by about 2x, and states a hard failure where the real behaviour is degraded. A bench run at about 10 lost PDUs a second would contradict the page.
- **Required outcome:** state random loss as a roll-off, not a cliff. Either:
  - give the valid fraction, exp(-500 q^2 x 4.096 s): about 0.6 at 8 lost PDUs a second, 0.37 at 11, and 0.01 at about 24, with a cold start that still locks but late; or
  - keep "about 11 a second" only as the rate at which the mean restart interval reaches 4.1 s, and drop "never validates" and "a cold start does not lock" from it.

  The same applies to the "the cliff" bullet at `:823` and to the Limits item.
- **Verification:** re-read `:811-825` and `:1320-1324` at the next head. Optionally add a model row at p = 1.4e-3, and one at about 3e-3, beside the existing 1e-4 and 1e-3 rows.

### F2 - MINOR - Tests - the counter row's PDU-loss leg has no mutant that fails it

- **Where:**
  - `docs/design/MEDIA_CLOCK_FOLLOWING.md:1216`: the CLOCK_DOMAIN counter row adds "60 s with one PDU lost in every 0.3 s", and its pass column adds "neither moves during the PDU-loss leg";
  - against the contract at `:1189-1190`: "Each new check is shown failing at the base or under a named mutant before it is trusted".
- **Authority and evidence:**
  - The row names two mutants. **C0's level (`~tu` only)** moves no counter during PDU loss. **C2's level (the reference lock)** does not either, because a sequence gap does not drop a lock already held (`:880-881`; `KL_crf_rx.sv:569-570`). So both pass the loss leg.
  - The restart-on-any-loss mutant, which the other new rows use, also passes it. On an invalid rate the servo holds its PI and lock count (`KL_mmcm_drp_servo.sv:613-615`), and it leaves LOCKED only on a lock count of zero (`:567-568`). C1 therefore does not move under that mutant. My model shows LOCKED held with 0 drops through 200 restarts (`model/r429_4_loss_model.out`, servo row loss leg).
  - REVIEW READY 5938892492 says of this leg and the servo row's loss leg: "Each has a failing mutant". That holds for the servo row: under the restart-on-any-loss mutant the trim stays 4.03 ppm off in my model. It does not hold for the counter row.
  - A real mutant exists, unnamed. If the meter dropped its lock on a sequence gap, the servo would pass HOLDOVER at every lost PDU (`KL_mmcm_drp_servo.sv:564`), and under C1 UNLOCKED would move every 0.3 s.
- **Impact:** a leg no named mutant can fail is the pattern the test-plan contract excludes. An implementation could ship a mis-wired lock, for example the CRF settle-run rule applied to a held lock, without this leg being shown able to see it.
- **Required outcome:** the leg names a mutant that fails it, with its symptom. For example: "the meter's lock dropped on a sequence gap: HOLDOVER and an UNLOCKED count at every lost PDU". Or the page states that the leg is a regression guard with no mutant of its own, and why.
- **Verification:** read row `:1216` at the next head. In the implementation lane, the named mutant is shown failing the leg.

### S1 - SUGGESTION - RTL, Tests - state whether a loss-voided group is still deviation-checked, and what "drops twice" counts

These are optional and do not affect coverage.

- **The precedence is unstated.** Rules 1 and 2 (`:748-756`) do not say what happens when one group has both a sequence gap and an in-group deviation. A streaming implementation sees the deviation at the step's PDU, before it learns of a later loss in the group, so it would naturally restart there.
- **Both readings catch every step.** My model ran both readings: 64/64 in-gap steps restart exactly once under either.
- **But the step row's mutant holds under one reading only.** The row's mutant symptom at `:1206` ("No check across a gap: no restart") and the text at `:856-858` hold only if a loss-voided group is not deviation-checked, which is the author model's choice.
- **Under the other reading the row still kills the mutant, at 2 positions only.** The mutant still restarts at step positions 1 to 14. It fails only at positions 0 and 15 (8 of 64 cases), so the row kills it there.
- **k = 0.** The page could also say that it is a gap of 16 groups, and restarts, as the author model treats it (`k = ... % 16 or 16`). `:757-763` defines k = 1, 2 and >= 3 only.
- **"LOCKED drops twice"** at `:858` is per case. The author model shows `drops=2` in each of the 64 mutant cases, and mine gives 128 drops over 64 cases. Saying "in each case" avoids reading it as two in total.

## The round-4 checks requested

### Item 1: the rulings (R429-3 F1 = R428-3 F1)

The rulings are recorded on the page and in the PR body:

- **On the page:**
  - the header, `:20-45`;
  - D1 = L1 at `:350-351` and in the L1 row;
  - D2's wording at `:402-411`;
  - D8 = E8 at `:561-562` and in the option row at `:678`;
  - D4 = A2-a by the owner at `:1031-1037`;
  - D5 = C1 with E8 at `:1050-1051` and `:1083-1095`, with C2 marked "not taken";
  - the Decisions table at `:1264-1275`, every row linked to its ruling;
  - #633 at `:35` and `:1302`.
- **The known risk** is in Limits at `:1305-1319`: A2-a meets Milan v1.2 7.4's +/-50 ppm at INTERNAL only for an oscillator grade of +/-39 ppm or better. The grade is assumed adequate and unconfirmed, and no plan search is required.
  - The arithmetic holds: plan A at -10.64 ppm leaves 39.36 ppm, and plan B at -0.66 ppm leaves 49.34 ppm (`sw/litex/milan_soc.py:347-356`).
  - The board's 200 MHz input is at `:232`, and the Arty's 100 MHz at `:228-230`.
  - The text matches owner decision 5937848189, which supersedes the plan-search requirement of 5937738214.
- **Bench rows:** the INTERNAL accuracy row at `:1258` is "recorded as an observation, not graded", as the owner decided. A2 at INTERNAL passes under A2-a (`:1257`), as decision 5937643550 requires.
- **The PR body** records the same in Status, the Decisions table and Known limitations. It says "Relates to #629" and does not close #629.

### Item 2: the loss rule, option (b) (R429-3 F2), re-derived independently

All results below are in `model/r429_4_loss_model.out`.

| Claim (page) | Independent result |
|---|---|
| A lost PDU voids only its group; isolated losses restart nothing (`:748-751`) | Losses 1 in 1 s, 1 in 0.3 s, every snapshot group, and 1 in 32, at +/-1,426 ns and 300 ppm, independent and random-sign-per-group: 0 restarts, `rate_valid` never falls after 4.1 s, 0 drops. The restart-on-any-loss mutant never validates in any of the eight. |
| Check across one voided group: 4 ms +/- 5,120 ns (`:757-763`) | Tolerance edge across one gap: no restart at +/-1,955 ns and a restart at +/-1,965 ns at 300 ppm; no restart at +/-2,555 ns and a restart at +/-2,565 ns at 0 ppm. The page's +/-1,960 and +/-2,560 ns (`:795-797`) hold. |
| Midpoint fill "exact for any talker rate", error at most J (`:766-770`) | Ideal timestamps at 7 rates from -300 to +300 ppm with two snapshot groups lost: 0 LSB from the no-loss rates. The fill is linear interpolation, so it is exact for any constant rate up to the 0.5 ns floor. Its error is the mean of two pick errors, so at most J. |
| The bound: 2J + 601k <= B_k < 10,417 - 2J - 601k; windows at k = 1, 2, 3 and none at 4 (`:778-790`) | Reproduced exactly: 3,453 to 6,963; 4,054 to 6,362; 4,655 to 5,761; none at k = 4. Taking one voided group (k = 2) is justified: k = 3 has a window, but its fill needs a division by 3, as stated (`:792-794`). The half-sample criterion is a stated design margin; a one-sample step leaves it far behind. |
| Validity region: losses that share a group or lie >= 32 PDUs apart, at any phase, up to 250 per second (`:801-805`) | Exhaustive two-loss sweep, gaps 1 to 39 PDUs at 16 phases: no restart for any pair at >= 32 apart or in one group; a restart at some phase for every different-group pair up to 31 apart. 32 is tight, and 8,000 / 32 = 250. |
| Fill bound 2.125 x 2J / 8 = 758 ns, against 753 ns without fills (`:806-809`) | Loop l1 gain 2.125 at plant gain 1 (2.000 at 0.8, 2.505 at 1.2). E8 worst-case coefficient 0.5278 J, which is 753 ns; the triangle bound is 758 ns. The figures at 700 and 890 ns are reproduced. Worst shape in closed loop: 756 ns without fills and 370 ns with every snapshot filled (the page's model: 773 and 425 ns). |
| Beyond the bound a locked servo holds trim and stays LOCKED (`:811-816`) | Confirmed against `KL_mmcm_drp_servo.sv:613-615` (no PI or lock-count update on an invalid rate) and `:567-568` (LOCKED falls only on a zero lock count). |
| Random loss, 500 q^2 restarts a second; "the cliff" at about 11 per second (`:817-825`) | The formula is right: 0.246 restarts a second at p = 1.4e-3, and 74 restarts in 300 s simulated. The cliff is not: see **F1**. |
| Servo row loss leg (`:1210`) | Rule (b): LOCKED, 0 drops, trim within 0.15 ppm of the +4 ppm step. The restart-on-any-loss mutant: 200 restarts, LOCKED held, trim 4.03 ppm off, so only the trim check fails, as the page says. |
| Meter rows `:1203-1206` | Periodic loss: the mutant never validates; every random-sign rate is within 357 ns of the planted rate, inside 360. Snapshot-group loss: rates equal within 0 LSB; the next-pick-less-2-ms mutant leaves exactly one rate 25 ns off; the restart mutant gives one restart. The bound row: exactly one restart for each of the first three patterns and none for the last two; the any-gap mutant gives none in all five. Step in a gap: 64/64 restart once; the no-cross-check mutant gives 0/64 restarts, and after lock it drops LOCKED twice per case (see S1 for the precedence caveat). |
| Counter row loss leg (`:1216`) | No named mutant fails it: see **F2**. |

The author's model, re-run at this head: rc 0, output byte-identical to the published `meter_rules_model_r4.out` (sha256 `f164966b...4081`).

- `compare_r3_r4_noloss.py`: "compared 40 cases; identical 40".
- Section A: 204 cases, 0 with a restart, 0 with a drop, every `closed<2ppm=1.000`, worst `closed_max` 773 ns at plant gain 1 and 868 ns at 1.2.
- Section S: 64 in-gap steps restart once.

All of these match the page (`:848-858`).

### Item 3: R429-3 S1 (J/T and 2J/T, `:572-598`)

The statement is correct. Error-free data of slope s over span T is consistent with every rate in [s - 2J/T, s + 2J/T]: each rate pairs with a ramp inside +/-J and a free offset. So no estimator does better than 2J/T in the worst case, and the two-point difference attains it. That makes 2J/T the tight minimax figure: 4.07 ppm at 1,042 ns over 512 ms.

The pairwise argument, two hypotheses 2J/T apart, gives the weaker J/T: 2.035 ppm, 18 ns over the test. The least-squares worst case is 3J/T, which I recomputed as 2.999 J. "Either figure exceeds the test" is right, and the headline holds.

### Other suggestions and the table fix

- **R429-3 S2** is taken (`:658-665`). The E8 half is reproduced: no drop at any of 16 phases up to 8 ppm, and a drop at all 16 from 8.5 ppm. The page has one phase in 16 at 8 ppm, a model-boundary detail. The E1 half was not re-run this round.
- **R429-3 S3** is taken (`:650-657`). Milan v1.2 4.4.2.3 and Annex B.1 are cited as the repository's own traceability reads them (`docs/history/v1/traceability/milan-v12.md:180`). No clause sets a lock time.
- **R428-3 S1** is taken (`:721-725`), with both quantities. **R428-3 S2** is superseded by option (b). **R428-3 S3** is taken: a pinned seed, 120 s, 13 of 227 windows (`:1197`).
- **The table pipe fix is verified** (`table_check/`). At `a463a1de`, source line 999 (the servo-with-meter row) has more unescaped pipes than its header, and its rendered cell ends in a stray backtick. At the head, no source row's pipe count differs from its header's, and no cell holds a stray backtick. The two cells with a literal `|` are the intended escaped `|e|`.

## Prior public findings at this head

| Finding | State at `1bdd6895` | Where |
|---|---|---|
| R429-3 F1 (rulings recorded as open) | Resolved | `:20-45`, `:350-351`, `:402-411`, `:561-562`, `:1031-1037`, `:1050-1051`, `:1264-1275`, `:1302`, `:1305-1319`; PR body Status, Decisions, Known limitations |
| R429-3 F2 (any loss restarts E8; cost unstated, ungraded) | Resolved under the manager's option (b): `:727-867`; test rows `:1203-1206`, `:1210`, `:1216`. Two residual defects in the new text are filed as new findings F1 and F2 | as listed |
| R428-3 F1 (same class as R429-3 F1) | Resolved | as R429-3 F1 |
| R429-3 S1, S2, S3 | Taken | `:572-598`, `:658-665`, `:650-657` |
| R428-3 S1, S3 | Taken | `:721-725`, `:1197` |
| R428-3 S2 | Superseded by option (b) | `:727-867` |
| Round 1 and 2 findings, and the round-3 switch-test resolution | Unregressed: the round-4 diff removes none of their text except the state words that F1 above required | round-4 diff, removed lines |

## Lens coverage at this head

```text
[R429] PASS Conformance - docs/design/MEDIA_CLOCK_FOLLOWING.md:20-45, :79-239, :350-411, :561-665, :727-867, :1031-1095, :1264-1319 at 1bdd6895 - every ruling (5935520588, 5937449258), owner decision (5937643550, 5937848189) and the round-4 assignment (5938156583) recorded as decided; the +/-39 / +/-49 ppm limits checked against milan_soc.py:347-356; IEEE 1722-2016 4.4.4.6, 10.1 and 10.6 as the loss-rule basis; Milan v1.2 4.4.2.3 / Annex B.1 latency reading; the S1 estimator bound (2J/T tight, J/T pairwise) re-derived
[R429] PASS RTL - hdl/ieee1722/crf/KL_mmcm_drp_servo.sv:228-233, :538-579, :606-700; KL_crf_rx.sv:320-329, :390-403, :569-570; KL_avtp_rx_monitor_ctx.sv:24-28, :173-174 at 1bdd6895 - every RTL claim of the loss rule (hold on invalid rate, LOCKED fall rule, gap restart in KL_crf_rx, loss counters) holds as cited; the meter's loss-rule arithmetic (k from sequence_num[7:4], midpoint >>> 1 modulo 2^32, count-by-k snapshot grid) modelled and consistent; S1 only (precedence, k = 0)
[R429] MINOR Robustness - see F1 (docs/design/MEDIA_CLOCK_FOLLOWING.md:817-825, :1320-1324); model/r429_4_loss_model.out: periodic, snapshot-group and 1-in-32 loss, bound patterns, two-loss region sweep, tolerance across a gap, steps in a gap, random loss 1e-4 / 1e-3 / 1.4e-3
[R429] MINOR Tests - see F2 (docs/design/MEDIA_CLOCK_FOLLOWING.md:1216 against :1189-1190); every other new or changed row (:1196-1219) checked mutant against pass criterion in model/r429_4_loss_model.out; the author model re-run byte-identical (model/author_model_rerun_sha256.txt, model/author_compare_r3_r4_noloss_rerun.out)
[R429] MINOR Docs - see F1; docs gates rc 0 in the pinned Markdown environment, check_entity_shape rc 0 (166/0), git diff --check rc 0 on three ranges (gates/); table render fix verified (table_check/); docs/README.md:72 row; commit messages one line, no trailers; PR body records the rulings and "Relates to #629"; no private paths or names on the page or in the PR body
```

## Reviewer-owned completion ledger

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | the page's clause findings, rulings, D1 to D8, Limits, and the loss rule's clause basis; the owner and manager decisions on #629; `sw/litex/milan_soc.py:226-234`, `:339-358` | R429-4 | 1bdd68957dd1357645c500014002b1e5a115864c |
| RTL | CLEAN (S1 only) | `KL_mmcm_drp_servo.sv`, `KL_crf_rx.sv`, `KL_avtp_rx_monitor_ctx.sv` at the cited lines; the meter's loss-rule arithmetic in `r429_4_loss_model.py` | R429-4 | 1bdd68957dd1357645c500014002b1e5a115864c |
| Robustness | UNCLEAN (F1) | `r429_4_loss_model.py` and its output; the author model re-run | R429-4 | 1bdd68957dd1357645c500014002b1e5a115864c |
| Tests | UNCLEAN (F2) | test plan `:1185-1262`, each new or changed row's mutant against its pass criterion | R429-4 | 1bdd68957dd1357645c500014002b1e5a115864c |
| Docs | UNCLEAN (F1) | the whole page; `docs/README.md`; the PR #631 body; the commit messages; `gates/`; `table_check/` | R429-4 | 1bdd68957dd1357645c500014002b1e5a115864c |

## Executed evidence

Every file below is listed in `MANIFEST.sha256`.

- **`r429_4_loss_model.py`:** this reviewer's model, written from the page text and the servo RTL. Standard library only, deterministic seeds, and 8 parallel jobs at most.
  - **`model/r429_4_loss_model.out`:** its output. The run exited rc 0 (`model/r429_4_loss_model.rc`), and a second run is byte-identical (`model/second_run_cmp.txt`).
- **The author's round-4 model, re-run** from branch `629-review-evidence` at `1ef4ddb8`:
  - `model/author_model_rerun_sha256.txt`: the output is byte-identical to the published one;
  - `model/author_compare_r3_r4_noloss_rerun.out`: 40/40 identical;
  - `model/author_r4_manifest_check.txt`: the author packet's own manifest check.
- **`gates/`:** at the head, in the pinned Markdown environment (`tools/markdown/requirements.txt` versions), each command's output and rc:
  - `docs_check`: 0 findings;
  - `check_doc_style`: OK, 22 documents;
  - `gen_toc --check`: OK, and `--verify-anchors`: 292 links;
  - `check_em_dash --base d4dd7426`: 0 findings over 1,341 lines;
  - `check_doc_paths`: 875 paths resolve;
  - `check_entity_shape.py`: checks 166, failures 0;
  - `git diff --check` on `d4dd7426..1bdd6895`, on `a463a1de..1bdd6895` and on the worktree;
  - every one at rc 0.
- **`table_check/table_cells.py`, with `at_a463a1de.out` and `at_1bdd6895.out`:** the render check of the table fix.
- **`integrity/clone_integrity.txt`:** HEAD and tree are exact; the worktree, index and status are clean; index blobs and modes equal the HEAD tree; the four submodule gitlinks are unchanged. No probe touched the review clone. All model work ran outside it.

## Limits

- Design only. Nothing in the page is implemented, and both models are desk models of the stated rules and of the servo's PI, not of any talker, network or the servo's RTL.
- My servo model is window-level, with plant gain 1 one window late and +/-20 ns of quantisation. Its figures agree with the author's to within a few tens of ns, and with the analytic l1 bound exactly.
- No HDL simulation was run this round. Round 3's switch-test probe was not repeated, because the round-4 diff does not touch that design.
- The Milan v1.2 and IEEE texts were not available locally. Clause readings rely on the page, the prior rounds and the repository's own traceability.
- E1's 16-phase step figures (R429-3 S2) were not re-run.
- Physical calibration was NOT RUN. No hardware was used, and hosted or act acceptance is the manager's.

## Pending manager duties

- Route F1 (re-word the random-loss envelope) and F2 (name a failing mutant for the counter row's loss leg) to the lane. S1 is optional.
- The archived author packet's `MANIFEST.sha256` (`review-evidence/629-r1/author-r4/` at `1ef4ddb8`) lists `run_gates.sh`, which the archive does not contain (`model/author_r4_manifest_check.txt`). Archive it or drop it from the manifest.
- The assignment's evidence link (`tree/0c17547b...`) holds only the round-1 packet. Later packets are on branch `629-review-evidence`.
- Hosted and act acceptance at the head, and the final current-dev candidate (source base `d4dd7426`, live dev `7f0927bb`), stay with the manager.

R429-4 FINISHED
