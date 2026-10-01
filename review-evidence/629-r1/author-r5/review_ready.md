[A488] REVIEW READY
Commit: `f4f0ecb4b41866cd30875e08e74114868ece5b4c` on `629-media-clock-follow`, one commit on `1bdd6895`. It is local and not pushed; pushing it and applying the prepared PR body are the manager's.
Changed: `docs/design/MEDIA_CLOCK_FOLLOWING.md` only (+153 / -50). The index row is unchanged. No RTL, builder, generator, config or processor change.

- **1. Random loss** (R428-4 F1 = R429-4 F1). "Lost PDUs" no longer has a cliff. "Beyond the bound" keeps the deterministic statement: gaps that recur within every 4.1 s keep the rate invalid. A new paragraph gives the restart rate, about 500 q^2 a second (exactly 500 q^2 (1 - q), the rate at which runs of two or more voided groups begin), and the valid fraction, about e^(-4.096 x 500 q^2). A table sets the formula beside the round-5 desk model, 32 seeds per rate:
  - valid 0.60 at 8 lost PDUs a second, 0.37 at 11, 0.14 at 16 and 0.015 at 24;
  - cold-start LOCKED medians of 7.8 s, 17.3 s, 29.1 s and 288 s; every seed locks, and no case drops LOCKED.

  The model's 17.3 s at 11 a second is below R428-4's 18.5 s because the servo holds its PI and lock count across invalid windows (`KL_mmcm_drp_servo.sv:613-615`), so it need not wait for one restart-free stretch. R429-4's 20.6 s run lies inside the model's middle half. The formula is checked against round 4's published rows: 1 and 41 restarts against 0.38 and 37.2 expected, and valid 0.98 and 0.55 against 0.98 and 0.59, inside one 300 s run's spread (sd 0.052 at p = 1e-3). Round 3's comparison is restated as e^(-4.096 x 8,000 p). The same correction is in Limits, "What round 3 cost", the estimator's "Residual" bullet, and the prepared PR body.
- **2. The counter row's loss leg** (R428-4 F2 = R429-4 F2). The leg now names a mutant it kills: **the meter's held lock cleared on a sequence gap**. The servo enters HOLDOVER at the leg's first lost PDU (`KL_mmcm_drp_servo.sv:564`), so UNLOCKED moves. Each later loss, 0.3 s on, returns it to HOLDOVER before its two-window skip ends (`:576-577`, `:617-618`), so LOCKED moves only after the leg. The row says the leg grades this mutant alone: under C0's level, C2's level or restart on any loss, neither counter moves. The servo-with-meter row names the same mutant: LOCKED left at the leg's first loss, and the trim 4 ppm off. The desk model now models the meter's lock and the servo's state machine.
  - The design moves no counter in the leg.
  - The mutant enters HOLDOVER 200 times, counts UNLOCKED at 20.197 s and LOCKED only at 82.586 s, 2.6 s after the leg, and leaves the trim frozen.
  - Its design and restart-on-any-loss rows reproduce round 4's servo-leg figures exactly.
- **3. Suggestions**, all taken.
  - **k = 0**, 16 group intervals, restarts, like every k other than 1 and 2. The alias is stated in group intervals (17 and 18 read as k = 1 and 2; 256 lost PDUs leave no gap). The model restarts once for every run of 2 to 33 whole lost groups and for 255, 256, 257 and 512 lost PDUs at two phases; one lost group restarts nothing.
  - **A loss-voided group is deviation-checked up to its gap** (rule 1): each PDU is compared with PDU 0 as it arrives, and nothing after the gap is used. The step row is rebuilt to match: steps at positions 1 to 15 of a group that loses its PDU 0, and at 0 to 14 of one that loses its PDU 15, 120 cases, each restarting once. The no-check mutant fails the 64 cases the deviation check cannot see, with LOCKED dropping twice in each.
  - **The gap bound's value:** a new meter row. (a) At +300 ppm, a +3,900 ns step lands 5,100 ns across the gap and must not restart. (b) At -300 ppm, a half-sample step opposed by picks at +/-J lands 6,365 ns across and must restart. Only a bound from 5,100 to 6,364 ns passes both: 4,096 ns fails (a), and 6,400 or 8,192 ns fails (b).
  - **"Exact for any constant talker rate"**, with at most 1 ns per ppm of change inside the 4 ms.
  - **"LOCKED drops twice in each of them".**
- **Also:** PR #630 merged into dev at `7f0927bb` after this page's base. The Limits item that called the baseline unmerged now says so; the page still cites it through the PR.

Validation, at `f4f0ecb4`, from the lane worktree, each unpiped with its output to a receipt; the worktree was clean before and after:
- The pinned Markdown environment:
  - `scripts/docs_check.py`: 0 findings;
  - `scripts/check_doc_style.py`: OK;
  - `scripts/gen_toc.py --check`: OK, and `--verify-anchors`: 292 links;
  - `scripts/check_em_dash.py --base d4dd7426`: 0 findings over 1,444 added lines;
  - `scripts/check_doc_paths.py`: 875 paths resolve.
- `python3 scripts/check_entity_shape.py`: `checks: 166 failures: 0`.
- `git diff --check` on the worktree, on `d4dd7426 HEAD` and on `1bdd6895 HEAD`.
- All rc 0. A render check with the pinned renderer finds 24 tables and 198 rows, none irregular.

The desk model `meter_rules_model_r5.py` (every section rc 0, deterministic; a second run of every new section is byte-identical) is the round-4 model plus:
- rule 1's deviation check up to a gap;
- the meter's lock;
- the servo's state machine;
- the C0, C1 and C2 levels;
- the gap bound as a parameter.

Re-run with round 4's seeds, its round-4 sections match round 4's published output line for line in 8 of 10 sections (`compare_r4_r5.py`, rc 0). The other 2 differ only where rule 1 now checks a loss-voided group: the in-gap step lines, and five cases beyond the tolerance that are never valid in either model.

Acceptance criteria: the round-5 items 1 to 3 are met as above. #629's implementation, simulation and bench items stay open; this is the design step.

Open risks/questions: one design statement for the reviewers. Item 3 asked whether a loss-voided group is still deviation-checked. The page says yes, up to its gap, because a compare made at each PDU does that without a verdict held to the group's end, and it costs nothing. The other reading also catches every step, and round 4's model used it. It differs only in which check fires: under it the no-check mutant would fail all 120 step cases, not 64. No decision is needed unless a reviewer prefers it.

The packet holds the model with its per-section output, the comparison, the gate receipts, the render check, HANDOFF.md and PR-BODY.md (with "Relates to #629" and a Round 5 section). Stopping here.
