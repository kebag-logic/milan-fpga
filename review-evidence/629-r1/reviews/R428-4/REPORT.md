[R428] NEGATIVE - exact head 1bdd68957dd1357645c500014002b1e5a115864c

# R428-4: internal cleared-context review of PR #631 (#629 lane M1, design only)

- **Head:** `1bdd68957dd1357645c500014002b1e5a115864c`, tree `7e3d8c95ea755c9a225cff1a70df650c49b0d7f0`.
- **Base:** source base `d4dd742679b902b2bc5eedf89d525066d59aafbb`.
- **Round-4 range:** `a463a1de..1bdd6895`, two one-line commits (`0cf1ef48`, `1bdd6895`). They change only `docs/design/MEDIA_CLOCK_FOLLOWING.md` (+337 / -102).
- **The whole PR** changes that page and adds one row to `docs/README.md`.
- **Assignment:** #629 comment 5938156583. **REVIEW READY:** #629 comment 5938892492.

**Verdict: NEGATIVE.** Two MINOR findings are open: F1 under Robustness and Docs, and F2 under Tests.

Everything else asked for this round is met. Each of these was confirmed by an independent model written from the page text, or by a probe:
- the rulings recorded on the page;
- the loss rule (option (b)), its bound and its validity region;
- every listed loss mutant;
- the midpoint fill;
- the loop gains;
- the author's desk model, reproduced byte for byte;
- the table-cell fix;
- every gate.

## How this round was done

1. **Read, in order:**
   - AGENTS.md and CONTRIBUTING.md;
   - the #629 body and every lane M1 comment by the manager and the owner (the assignments, the rulings, D4 = A2-a, the A2-a accuracy note and the known-risk decision that supersedes it);
   - the live PR #631 body;
   - the round-4 diff, then the whole page at the head;
   - every cited RTL and SoC line at the head;
   - from the public evidence branch `629-review-evidence` (tip `1ef4ddb8`), the `author-r4/` packet and the round-3 model output only.
2. **Ran:**
   - an independent desk model of the loss rule, written from the page alone (`probes/loss_rule_model.py`);
   - the author's model, re-run;
   - a cmark-gfm table render at `a463a1de` and at the head;
   - the gates.
3. **Wrote** the verdict and ledger.
4. **Only then read the prior review findings on this PR.** They are resolved in the last section, and none changes the verdict.

## Findings

### F1 - MINOR - Robustness, Docs - the random-loss "cliff" is wrong: the rate does validate, and a cold start does lock, at about 11 lost PDUs a second

**Where:**
- `docs/design/MEDIA_CLOCK_FOLLOWING.md:817-825`: "The rate never validates only if these gaps recur within every 4.1 s ... p = 1.4e-3, 11 lost PDUs a second: one restart in 4.1 s, the cliff. Round 3's rule reached its cliff at p = 3e-5".
- `:1320-1324` (Limits): "if that recurs within every 4.1 s the rate never validates: about 11 lost PDUs a second under independent loss ... a cold start does not lock".
- The live PR #631 body, Round 4 table, item 2: "The rate never validates only if such gaps recur within every 4.1 s, about 11 lost PDUs a second under independent loss".

**Authority and evidence:**
- **The model.** Under independent loss at rate p per PDU, the loss rule's restarts (two adjacent voided groups) arrive at close to a Poisson rate λ = 500 q². That is the page's own rate. My group-level Monte Carlo measures 0.242/s at p = 1.4e-3, against 500 q² = 0.246/s. The rate is valid whenever 4.096 s have passed since the last restart, so the valid fraction is about e^(-4.096 λ).
- **At p = 1.4e-3, 11.2 lost PDUs/s, the rate is valid about 37 % of the time.** The formula gives 0.366, and my model, 8 seeds of 600 s, measures 0.369.
- **A cold start locks.** All 8 seeds reach a restart-free run of 7.3 s (the page's cold-start LOCKED time). The median arrival is 18.5 s after the first PDU.
- **The page's own row agrees with the model.** p = 1e-3 reads valid 0.55 (`:846`), against the formula's 0.597 and my 0.621.
- **Validity is negligible only near p = 3e-3, 24 lost PDUs/s:** about 1 % in both the formula and my model. Even there, the author's own published model row `random p=3e-03` reads `valid=0.0137 ... t_lock_s=254.62` (evidence `author-r4/meter_rules_model_r4.out`, section P). The servo locked.
- **Round 3's "cliff at p = 3e-5" has the same error.** Its mean restart interval is 4.1 s, but its valid fraction is 0.374.
- **What is true.** The deterministic statement holds: periodic adjacent-group voids recurring within every 4.1 s keep the rate invalid. The two-PDU-burst-across-a-boundary row at 1 in 1 s (`:843`) shows it. What is wrong is equating that with a mean of one such void per 4.1 s under random loss.

Receipts: `probes/model_part1.out` section 6; `probes/loss_rule_model.py`.

**Impact:** The design's Limits misstates the loss envelope that the fabric and bench lanes inherit:
- "A cold start does not lock" is false at the loss rate it names.
- A bench observation of LOCKED under about 11/s of loss would contradict the page.
- A loss budget sized from the page would be sized to a cliff that does not exist.

The loss rule itself is sound. Only the statement of its envelope is wrong.

**Required outcome:**
- State random-loss behaviour as the graded degradation it is: the mean restart interval 1/(500 q²) and the valid fraction, about e^(-4.096 x 500 q²).
- State cold-start lock as probabilistic.
- If a threshold is wanted, give its definition and value, for example about 24 lost PDUs/s for 1 % validity.
- Correct Limits and the PR body to match, and treat round 3's comparison figure the same way.
- Keep the deterministic statement, which is true.

**Verification:**
- The desk model, with a row at p = 1.4e-3 (and one near 3e-3), agrees with the stated valid fraction.
- No text says "never validates" or "a cold start does not lock" for a random-loss rate at which the model validates and locks.

### F2 - MINOR - Tests - the CLOCK_DOMAIN counter row's new PDU-loss leg is not shown failing under any mutant

**Where:**
- `docs/design/MEDIA_CLOCK_FOLLOWING.md:1216`, the pass criterion: "60 s with one PDU lost in every 0.3 s ... neither moves during the PDU-loss leg".
- The row's mutants: C0's level and C2's level.
- The plan's own rule, `:1189-1190`: "Each new check is shown failing at the base or under a named mutant before it is trusted".

**Authority and evidence:** The loss leg passes under every named mutant and under round 3's rule:
- **C0** counts `~tu`, which no PDU loss moves. Its listed failure is at the holdover leg.
- **C2** counts the meter's lock, which a sequence gap does not drop (`:880-881`; `hdl/ieee1722/crf/KL_crf_rx.sv:569-570`). Its listed failure is at the return.
- **C1, the design,** follows the servo's LOCKED. An invalid rate holds the PI and the lock count (`hdl/ieee1722/crf/KL_mmcm_drp_servo.sv:611-615`), and LOCKED falls only on a lock count of zero (`:567-568`).
- **Restart on any loss** (round 3's rule) therefore leaves both counters still through the leg as well.

So the leg can show none of the defects the row names. The REVIEW READY (#629 comment 5938892492) says of the new loss legs: "Each has a failing mutant".

There is one rule this leg could grade: "a sequence gap ... does not drop a lock already held" (`:880-881`). The page's "stays LOCKED under loss" claims rest on it, yet no row names a mutant for it. The servo-with-meter loss leg (`:1210`, "LOCKED ... never left") would also kill such a mutant, but does not name one.

**Impact:**
- The implementation lane inherits a check with no demonstrated failure mode.
- The held-lock rule under loss is never graded by name.

**Required outcome:** Do one of these:
- name a mutant that the loss leg kills, for example "the meter's held lock cleared on a sequence gap": the servo enters HOLDOVER and C1 counts UNLOCKED inside the loss leg. Name it in this row, in the servo-with-meter row, or in both;
- or state that the leg is a regression check without a mutant of its own.

**Verification:** The row's mutant column names a mutant under which "neither moves during the PDU-loss leg" fails.

### S1 - SUGGESTION - RTL, Robustness - say what k = 0 does, and state the alias in group intervals

**Where:** `:757-763`.

**The gap:**
- k is the 4-bit difference of `sequence_num[7:4]`.
- Sixteen group intervals give k = 0. Fifteen voided groups between two good ones does it, which takes fewer than 256 lost PDUs.
- The text covers k = 1, k = 2 and "k >= 3", and states the alias as "a gap of 256 PDUs or more".

**Suggested change:**
- Write "every k other than 1 and 2 restarts".
- State the alias as 16 or more group intervals. The 32 ms timestamp argument holds for any such alias.

**Receipt:** My model treats k = 0 as a restart, so it restarts at 15, 16 and 17 whole lost groups (`probes/model_mutants.out`, the alias lines).

### S2 - SUGGESTION - Tests - nothing grades the value of the one-voided-group bound

**The constraint:** The page derives B_2 < 6,363 ns, the condition for catching a half-sample step across one voided group (`:778-799`).

**The gap:** Every listed row passes with B_2 = 6,400 or 8,192 ns. At the design point under random-sign error, all 256 of 256 steps inside a loss-voided group restart at either width (`probes/model_steps.out`).

**Suggested rows:**
- a deterministic upper-edge case: the picks at -/+J, with the 300 ppm term opposing a half-sample step;
- a lower-edge case: correlated +/-1,960 ns at 300 ppm across one voided group.

### S3 - SUGGESTION - Docs - "exact for any talker rate" should say "constant"

**Where:** `:768-769` and the PR body.

**Suggested change:** "Exact for any constant talker rate". A rate that changes inside 4 ms adds a second-order term.

**Receipt:** The fill equals the true pick to 0 ns in 40 cases from -300 to +300 ppm, including the 2^32 wrap (`probes/model_part1.out` section 2).

## Assigned questions, judged

**The rulings (R428-3 F1 = R429-3 F1).** Recorded on the page and in the PR body:
- D1 = L1, D5 = C1 with E8, D8 = E8 and the D2 wording: `:23-48`, `:347-349`, `:402-412`, `:561-562`, `:1050-1054`, Decisions `:1264-1275`.
- #633: `:1302`.
- D4 = A2-a: `:1031-1046`.
- The owner's known risk: Limits `:1305-1319`. A2-a meets Milan v1.2 7.4's +/-50 ppm at INTERNAL only for a grade of +/-39 ppm or better, and the grade is assumed adequate and unconfirmed.
- The bench INTERNAL observation row: `:1258`. It is an observation, not graded, which matches the superseding owner decision 5937848189.
- The `1bdd6895` additions are accurate against `sw/litex/milan_soc.py:228-232` and `:341-356`: plan B at -0.66 ppm gives +/-49 ppm, and the Arty shapes take the same plan from their 100 MHz input.
- No stale "for decision" state remains.

**The loss rule (R429-3 F2, option (b)):**
- **A lost PDU voids only its own group:** `:748-751`.
- **The check across the gap, 4 ms +/- 5,120 ns:** `:757-763`.
- **The midpoint fill:** exact for a constant rate (S3), with an error of at most J.
- **The bound.** The windows reproduce exactly: k = 1, 3,453 to 6,963 ns; k = 2, 4,054 to 6,362 ns; k = 3, 4,655 to 5,761 ns; none at k = 4. The design's one-voided-group limit is a stated choice (a fill would need a division by 3), not forced by the bound.
- **The validity region.** Losses within one group, or 32 or more PDUs apart, up to 250/s. Reproduced:
  - 0 restarts in 96 periodic cases (spacing 32 to 8,000; four phases; independent, random-sign, 10 ms and 512 ms-block shapes at +/-1,426 ns and 300 ppm);
  - 0 restarts at a random 242/s;
  - the region is tight: two losses 31 apart restart when they straddle a boundary;
  - every rate stays within 2J/8 (357 ns) of the planted rate.
- **The random-loss figure** is F1.

**The new test rows** (my model, `probes/model_mutants.out`, `model_steps.out`, `steps_exact_once.out`):
- **Periodic loss, 1 in 1 s and 1 in 0.3 s, at the design point, both shapes:** 0 restarts and 227 valid rates. Under the restart-on-any-loss mutant, 0 valid rates.
- **A lost snapshot group at +100 ppm:** every rate equals the no-loss run's. The next-pick-less-2-ms mutant leaves one rate 25 ns off. The voided-snapshot-restarts mutant gives one restart.
- **The bound row:** exactly one restart for each of the first three cases and none for the last two. The k >= 3-accepted mutant gives no restart in the first three.
- **A step inside a gap:** 256 of 256 cases restart exactly once. The no-check mutant gives 0.
- **The servo row's loss leg:** the restart-on-any-loss mutant keeps the rate invalid while LOCKED holds (`KL_mmcm_drp_servo.sv:611-615`, `:567-568`), so the trim check alone fails, as the row states.
- **The counter row's loss leg** is F2.

**The desk-model re-run (author's model):**
- Re-run from the public evidence: byte-identical (`f164966b...4081`).
- 40 of 40 no-loss cases identical to round 3's published output.
- 204 lossy shape cases with no restart and no LOCKED drop; worst 773 ns, and 868 ns at a plant gain of 1.2.
- The 64 in-gap steps each restart once, and the no-check mutant drops LOCKED twice per case.
- Receipt: `probes/author_model_rerun.receipt`.

**R429-3 S1.** The page's two statements are both correct:
- J/T is a true lower bound for any estimator.
- 2J/T is the tight one. The rates consistent with error-free data of slope s span s +/- 2J/T (a ramp from -J to +J, either sign, with a free phase), so any estimator is 2J/T from one end, and the two-point difference attains it.
- The headline holds under either.

**The loop.** My linear model of the page's PI (`e = x - r`; `u = I + e/4`; `I += e/2`; a plant one window late) gives the l1 gain 2.125. E8's composite gain is 0.5278: 753 ns at J = 1,426 ns, and 700 and 890 ns at plant gains 0.8 and 1.2, as the page states. The 758 ns for filled snapshots is a valid, looser product bound (`probes/model_part1.out` section 7).

**The table-cell fix.**
- At `a463a1de`, one row renders with a split code span: the servo-with-meter row.
- At the head, no row is irregular. The only rows with an empty cell are the three intended ones in the change list (`probes/table_render.out`).
- `\|e\|` renders as `|e|`.

**The gates.** All rc 0 at the head:
- `check_entity_shape.py`: `checks: 166 failures: 0`.
- `docs_check`, `check_doc_style`, `gen_toc --check`, `gen_toc --verify-anchors` (292), `check_em_dash --base d4dd7426` (0 over 1,341 lines) and `check_doc_paths` (875), in the pinned Markdown environment (`cmarkgfm==2025.10.22`, `html5lib==1.1`).
- `git diff --check` on the worktree, `d4dd7426..HEAD` and `a463a1de..HEAD`.

**Public text.** Issue references are "Relates to #629". The round-4 diff, the PR body and the commit messages contain no private name, path or tool name. The commits are one line with no trailer.

## Clean lenses

```text
[R428] PASS Conformance - docs/design/MEDIA_CLOCK_FOLLOWING.md:23-48, :347-349, :402-412, :559-562, :650-657, :727-745, :1031-1054, :1257-1258, :1264-1319 and the live PR #631 body at 1bdd6895 - each ruling against #629 comments 5937449258, 5937643550, 5937848189 and the option (b) text of 5938156583; the INTERNAL accuracy arithmetic against sw/litex/milan_soc.py:228-232, :341-356; the loss and latency clause basis against the repository's own recorded readings (docs/history/v1/reference/PROTOCOL_TRACEABILITY.md:336, docs/design/GM_LOSS_RECOVERY.md:98, :158); the R429-3 S1 bound re-derived (2J/T tight, J/T true)
[R428] PASS RTL - docs/design/MEDIA_CLOCK_FOLLOWING.md:747-799, :802-812, :860-863, :869-881, :1118-1130, :1144-1147 at 1bdd6895; hdl/ieee1722/crf/KL_crf_rx.sv:398-399, :569-570; hdl/ieee1722/crf/KL_mmcm_drp_servo.sv:567-568, :611-615; hdl/ieee1722/avtp/KL_avtp_rx_monitor_ctx.sv:24-28, :173-174 - the loss rule's widths and arithmetic (4-bit k, 12-bit group counter, signed midpoint of a positive 4 ms difference modulo 2^32), the bound windows (probes/model_part1.out section 1), the loop gains (section 7), the area deltas (meter 380-580 LUT; total 420-660 LUT, 290-460 FF), and every cited line holds at the head; S1 is optional
```

## Ledger (reviewer-owned)

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Page rulings, Decisions, Limits and Bench rows against #629 comments 5937449258, 5937643550, 5937848189 and 5938156583; the live PR body; `sw/litex/milan_soc.py:228-232`, `:341-356`; the clause basis of the loss rule and the latency; the R429-3 S1 derivation | R428-4 | `1bdd68957dd1357645c500014002b1e5a115864c` |
| RTL | CLEAN | Loss rule and bound `:747-812`; area `:860-863`, `:1118-1130`; restart and lock lists `:869-881`; RTL change rows `:1144-1147`; the cited RTL at the head; the re-derived bound and loop gains | R428-4 | `1bdd68957dd1357645c500014002b1e5a115864c` |
| Robustness | UNCLEAN (F1) | The validity region (reproduced; tight at 31 apart); the bound and the alias (S1); periodic, burst, snapshot and random loss; the random-loss envelope (F1) | R428-4 | `1bdd68957dd1357645c500014002b1e5a115864c` |
| Tests | UNCLEAN (F2) | Test rows `:1197`, `:1202-1206`, `:1210`, `:1211`, `:1216`, `:1257-1258`, each with its mutants (my model; the author's model re-run); the counter row's loss leg (F2) | R428-4 | `1bdd68957dd1357645c500014002b1e5a115864c` |
| Docs | UNCLEAN (F1) | The whole page at the head, the round-4 diff, the live PR body; the table render; the docs gates; Limits `:1320-1324` (F1) | R428-4 | `1bdd68957dd1357645c500014002b1e5a115864c` |

## Executed evidence

Every file named here is listed in `MANIFEST.sha256`.

- **`run_gates.sh` and `gates/`:**
  - the gate receipts at the head;
  - the pinned environment's `pip freeze`;
  - `restore_check.txt`: HEAD, tree, worktree and index all equal the head; no untracked or ignored entries; index modes and blobs equal the HEAD tree; submodule checkouts at their gitlinks;
  - the gitlinks, unchanged from the base;
  - the exact-head hosted check runs.
- **`probes/loss_rule_model.py`, with outputs `model_part1.out`, `model_region.out`, `model_mutants.out` and `model_steps.out`:** my independent model of the loss rule, standard library only and deterministic.
- **`probes/steps_exact_once.py` and `.out`:** the exactly-once restart count.
- **`probes/table_render.py` and `.out`:** the cmark-gfm render of every table at both heads.
- **`probes/rerun_author_model.sh` and `author_model_rerun.receipt`:** the author's model re-run against the public evidence, with hashes.

**Hosted at the exact head** (manager-owned acceptance; `gates/hosted_check_runs.txt`):
- Succeeded: `rtl-fast`, `changes`, `elaborate`, `wire-accountability`, `full-ci-gate`, `bdd-conformance`, `docs-check-no-git`.
- In progress when sampled: `docs-check`.
- Skipped, as a docs-only head allows: `verilator-suites`, `verilator-lint`, `yosys-portability`, `yosys-elaboration`, the shards, and Physical gPTP.

## Real limits

- **No standard texts.** No copy of Milan v1.2 or IEEE 1722-2016 was available. Clause readings are checked against the repository's recorded readings, not the texts.
- **Desk work, like the design.** My model is of the page's rules, not of RTL; none exists. My closed-loop check is the loop's linear gain, without the servo's clamps or slew.
- **Not run:**
  - the area run;
  - any full parent, processor, gPTP, Yosys or builder bank;
  - Docker or act.
- **No hardware.** Physical calibration is NOT RUN, and nothing here is bench proof.
- **Not the merge candidate.** Source validation at this head is not the current-dev candidate (live dev `7f0927bb`).

## Pending manager duties

- **Publication fix.** The published `author-r4/MANIFEST.sha256` lists `./run_gates.sh`, which the evidence branch does not carry: 33 of its 34 entries verify. Publish it, or record the omission.
- **Hosted and act acceptance** at the final head, including `docs-check`, still in progress when sampled.
- **At the merge turn:** the candidate merge build on live dev, then post-merge containment.
- **Re-review** of F1 and F2 at the next head. Both are docs-only fixes.

## Prior public findings on PR #631

These were read after the verdict and ledger above were written.

| Finding | State at `1bdd6895` | Evidence |
|---|---|---|
| R428-3 F1 = R429-3 F1: the rulings shown as open | Resolved | Header `:23-48`; D1 `:347-349`; D2 `:402-412`; D8 `:561-562`, `:616`, `:678`; D5 `:1050-1054`, `:1072-1073`; Decisions `:1264-1275`; Limits #633 `:1302`; the live PR body's Status and Decisions. A scan finds no "for decision" or "to confirm" state left |
| R429-3 F2: E8's cost under PDU loss | Resolved by option (b) | The design change, test rows and desk model are reproduced above. The new text states the random-loss envelope wrongly: that is F1, raised on the round-4 text, not a retention of R429-3 F2 |
| R429-3 S1: J/T for an arbitrary estimator | Taken, and correct | `:577-594`; see "R429-3 S1" above |
| R429-3 S2: E1's step response depends on phase | Taken | `:658-665`. The 16-phase sweep is in the author's model, section Q |
| R429-3 S3: the latency clauses | Taken | `:650-657`: Milan v1.2 4.4.2.3 and Annex B.1 |
| R428-3 S1: name the window-error quantity | Taken | `:723-725`: open loop 104 against 351 ns, closed loop 184 against 465 ns |
| R428-3 S2: the loss rate at which E8 never validates | Superseded by option (b) | See F1 for the new statement |
| R428-3 S3: make the P1 mutant deterministic | Taken | `:1197`: a pinned seed and 120 s; 13 of 227 windows in the desk model |
| R428-2 F1 to F3, R429-2 N1 to N3, and their suggestions | Remain resolved | The round-4 hunks keep the void rule, the error-shape fix (E8) and the switch-test checks (`:1208`, `:1213`, `:1221-1242` unchanged) |
| R428-1 F1 to F6, R429-1 F1 to F5, and their suggestions | Remain resolved | Round 4 touches their text only to record rulings, which completes R428-1 F6's class. The D5 reversal stays stated (`:1052-1054`, `:1076-1081`), and the no-fallback choice keeps its clause basis (`:966-970`) |

R428-4 FINISHED
