# [A488] HANDOFF: #629 lane M1, round 5 (design only)

Status: DONE for round 5. REVIEW READY posted (#629 comment 5940218896) with head `f4f0ecb4`; stopped, waiting for the round-5 reviews.

- Branch `629-media-clock-follow`, start `1bdd68957dd1357645c500014002b1e5a115864c`, head `f4f0ecb4b41866cd30875e08e74114868ece5b4c` (one commit; local, NOT pushed). PR #631.
- Changed: `docs/design/MEDIA_CLOCK_FOLLOWING.md` only (+153 / -50 against `1bdd6895`). Index row in `docs/README.md` unchanged (still "proposed": nothing is implemented).
- No RTL, builder, generator, config or processor change.
- Assignment: #629 comment 5939246995. Reviews answered: R428-4 (PR #631 comment 5939246407), R429-4 (PR #631 comment 5939232297), both NEGATIVE on the same two MINOR findings.
- Rulings in force (unchanged): 5935520588 (round 1), 5937449258 (round 3), owner 5937643550 (D4 = A2-a), owner 5937848189 (oscillator-grade known risk). No new ruling was needed or asked for.
- Posted: TAKEN (#629 comment 5939262004) and REVIEW READY (#629 comment 5940218896) with head `f4f0ecb4`. Nothing else posted; no comment edited or deleted.

## Gates at `f4f0ecb4` (receipts in `gates/`, each unpiped, all rc 0)

| Gate | Result |
|---|---|
| `scripts/docs_check.py` | 0 findings, 184 md + 955 scrubbed files |
| `scripts/check_doc_style.py` | OK, 22 documents |
| `scripts/gen_toc.py --check` / `--verify-anchors` | OK / 292 links reproduced |
| `scripts/check_em_dash.py --base d4dd7426` | 0 findings over 1,444 added lines |
| `scripts/check_doc_paths.py` | 875 paths resolve |
| `scripts/check_entity_shape.py` | `checks: 166 failures: 0` |
| `git diff --check` (worktree, `d4dd7426 HEAD`, `1bdd6895 HEAD`) | clean |

The Markdown gates ran with the pinned environment's interpreter from the physical `/data` lane path (`run_gates.sh`), with bytecode writing off, so the run leaves no `__pycache__`. `gates/status_before.txt` and `status_after.txt` are empty: the worktree was clean around the run. `table_render_check.py` (pinned renderer): 24 tables, 198 body rows, 0 irregular.

## Round 5: what changed

1. **Random loss (R428-4 F1 = R429-4 F1).** "Lost PDUs" no longer has a cliff.
   - "Beyond the bound" keeps the deterministic statement: gaps recurring within every 4.1 s keep the rate invalid.
   - New paragraph "Random loss degrades the rate gradually, with no cliff". Runs of two or more voided groups begin about 500 q^2 a second, exactly 500 q^2 (1 - q). The rate is valid about e^(-4.096 x 500 q^2) of the time.
   - A 6-row table: formula against model (32 seeds each) for restarts a second, valid fraction and cold-start LOCKED (median, middle half, slowest) at 0.8, 4, 8, 11, 16 and 24 lost PDUs a second. Valid: 0.995, 0.88, 0.60, 0.37, 0.14, 0.015. Median LOCKED: 7.3, 7.3, 7.8, 17.3, 29.1 and 288 s. Every seed locks, and no case drops LOCKED.
   - Why the 17.3 s model median sits below R428-4's 18.5 s: the servo holds its PI and lock count across invalid windows (`KL_mmcm_drp_servo.sv:613-615`), so it need not wait for one restart-free stretch. R429-4's single run (20.6 s) is inside the model's middle half.
   - The formula is checked against round 4's published rows: 1 and 41 restarts against 0.38 and 37.2 expected; valid 0.98 and 0.55 against 0.98 and 0.59. A 300 s run at p = 1e-3 has an sd of 0.052 (model section O).
   - The falloff by the exact rate: 90 % at 3.6, 50 % at 9.4, 10 % at 17, 1 % at about 25 lost PDUs a second. Round 3's rule, e^(-4.096 x 8000 p): 37 % at p = 3e-5, 1 % at 1.1 lost PDUs a second.
   - The same correction is made in Limits, in "What round 3 cost", in the estimator's "Residual" bullet (which said loss beyond the bound "does the same" as a continuous restart), and in PR-BODY.md (Round 4 item 2, corrected in place with a note, and Known limitations).
2. **The counter row's loss leg (R428-4 F2 = R429-4 F2).** The named mutant is "the meter's held lock cleared on a sequence gap".
   - The servo enters HOLDOVER at the leg's first lost PDU (`KL_mmcm_drp_servo.sv:564`): UNLOCKED +1. Each later loss, 0.3 s on, returns it to HOLDOVER before its two-window skip ends (`:576-577`, `:617-618`), so LOCKED moves only after the leg.
   - The row says the leg grades this mutant alone: C0's level, C2's level and restart on any loss move nothing in it.
   - The same mutant is named in the servo-with-meter row: LOCKED is left at the loss leg's first lost PDU, and the trim stays 4 ppm off.
   - "History, lock, era and outputs" and the D5 rationale say the two rows grade the held-lock rule.
   - Desk model (sections C and V5): the design moves no counter in the leg. The mutant shows HOLDOVER x200, UNLOCKED at 20.197 s, LOCKED only at 82.586 s, and a trim moved by -13 against the 2,048 step.
3. **Suggestions.** All taken.
   - **k = 0** is 16 group intervals and restarts: every k other than 1 and 2 restarts. The alias is stated in group intervals: 17 and 18 read as k = 1 and 2, and 256 lost PDUs leave no gap. The model (section Z) restarts every run of 2 to 33 whole lost groups, and 255, 256, 257 and 512 lost PDUs at two phases, exactly once; one lost group restarts nothing.
   - **A loss-voided group is deviation-checked up to its gap** (rule 1). This is a design statement made this round: a per-PDU compare against PDU 0, so it costs nothing. The step row is rebuilt to match: (a) PDU 0 lost, steps at 1 to 15; (b) PDU 15 lost, steps at 0 to 14; 120 cases. The no-check mutant fails the 64 cases the deviation check cannot see, with 2 LOCKED drops each. The 56 others restart at the step's PDU under either variant.
   - **The gap bound's value** gets a new meter-suite row: +3,900 ns at +300 ppm (5,100 ns across the gap, no restart) and a half-sample step at -300 ppm opposed by +/-J (6,365 ns, restart). It passes only for a bound from 5,100 to 6,364 ns. 4,096 ns fails (a); 6,400 and 8,192 ns fail (b).
   - "Exact for any **constant** talker rate", with at most 1 ns per ppm of change inside the 4 ms.
   - "LOCKED drops twice **in each of them**".
4. **Also:** PR #630 merged into dev at `7f0927bb` (2026-10-01 18:49Z) after this page's base. The Baseline header line and the Limits item now say so. The findings page is still cited through the PR, because this branch does not carry it. The Limits model bullets name what round 5 adds.

## Open point for the reviewers

Rule 1's deviation check up to a gap is a design statement made in this round, as item 3 asked ("say whether"), not a ruling. The alternative, a verdict held to the group's end so that a loss-voided group is never checked, also catches every step: round 4's model read it that way. The page states the streaming reading because a compare made at each PDU does it without a held verdict. Under it the step row's no-check mutant fails 64 of 120 cases, not all of them. No decision is needed unless a reviewer prefers the other reading.

## Clause findings (unchanged in round 5)

- (a) Milan v1.2 5.3.3.6 is a minimum: an AAF INPUT_STREAM source may sit beside the CRF source. IEEE 1722.1-2021 7.2.32 caps the list at 216 and sets no order.
- (b) Milan v1.2 5.3.11.1 (the selection is saved), 5.4.2.15 (no non-ATDECC change while locked), and 5.3.11.2 with the Table 5.7 counters. Free-wheel per IEEE 1722-2016 10.6 and the 4.4.4.7 NOTE. No fallback is this design's choice.
- (c) `mr`: the 4.4.4.3 and 10.4.3 shalls name CRF only; this design acts on them for AAF too (the PICS AAF-5 reading).
- (d) Eight places where the current reading is wrong.
- The loss rule rests on IEEE 1722-2016 4.4.4.6, 10.1 and 10.6. Milan v1.2 4.4.2.3 and Annex B.1 cover the 4.096 s hold, and Milan v1.2 7.4 the INTERNAL accuracy risk. Round 5 cites no new clause.

## Code map (file:line at dev `d4dd7426`; the page's Current state has the full table)

- **Servo (`KL_mmcm_drp_servo.sv`):**
  - PI `:228-233`;
  - the state machine: ACQUIRE/LOCKED to HOLDOVER on a reference unlock `:562-564`; LOCKED to ACQUIRE only on a lock count of 0 `:567-568`; HOLDOVER back to ACQUIRE with a two-window skip and the lock count cleared `:571-579`;
  - the PI runs only with no skip, outside HOLDOVER, on a valid rate `:613-615`; the skip decrements `:617-618`; writeback `:689-694`.
- **`KL_crf_rx.sv`:**
  - jump bound `:279-294`; lock and timeout `:296-298`; ring `:320-325`;
  - restart, including any sequence gap `:390-403` (`:398-400`);
  - a gap resets the settle run only `:569-570`; nothing in `:569-580` clears a held lock, which only the timeout drops (`:529-557`).
- **RX monitor** Table 5.6 counters: `KL_avtp_rx_monitor_ctx.sv:24-28`, `:173-174`.
- **Clocking:** `sw/litex/milan_soc.py:228-233`, `:341`, `:347-356`.
- **Root:** decode `milan_datapath.sv:1554-1570`; `mr` triggers `:3108-3156`, `:3180-3203`; counters `:3469-3475`, `:3492`; INTERNAL free-run rule `:5713-5718`; aligner `:5733-5748`.

## Design options and the rulings (unchanged)

D1 L1; D2 M1 (P2 pick, B2 4,096 ns bound, 48 kHz base format); D3 W2; D4 A2-a (owner); D5 C1 with E8; D6 all five configs; D7 #632; D8 E8 with round 4's loss rule (option (b)). All ruled. Round 5 states rule 1's deviation check up to a gap (see the open point) and grades the 5,120 ns bound.

## Parent-visible changes (page "Parent-visible changes"; unchanged in round 5)

- Requirements FR-CLK-03 and FR-CLK-04, and the status row.
- Configs admit `input_stream`.
- Builder: `_load_clocking`, the overlay, names, the shape tables and its test.
- Entity model: `CS_TYPE`, the tables, the flag value and the model id. The generated shape headers (six tracked copies).
- RTL: the new meter with the loss rule; the root decode and its consumers, A2-a, the C1 banner, the request tap and the stale comments; the servo port renames.
- Two CSR words; two gates' pinned text; the documentation.

The meter's rule 1 wording now includes the deviation check up to a gap, which the "RTL, new" row inherits from the design section.

## Processor-visible changes (page "Protocol-processor changes"; protocol-processor #141; unchanged)

No RTL or microcode. L6 and REQ-MDL-005 are restated as a minimum, credited to IEEE 1722.1-2021 7.2.32 and Table 7-141. Four top-level tests with mutants. It lands first, or with the parent.

## Test plan (page "Test plan"; round-5 changes in bold)

- **Meter suite:** rates; error shapes at the design point with a pinned seed; beyond tolerance; formats; wrap; lock; restarts; periodic loss; snapshot-group loss; the loss bound; **the gap bound's value (new row)**; **a step in a loss gap (rebuilt: two placements, 120 cases, the mutant fails 64)**; selection; pulses.
- **Servo:** select, and servo-with-meter with a loss leg (**the held-lock mutant named**).
- **`milan_dp`:** true ratio with an A2-a mutant; W2; switch; loss; echo; counters under C1 with a loss leg (**the held-lock mutant named; the leg grades it alone**); CSR; AECP walk.
- **Builder.**
- **Bench:** B AAF, B CRF, controls, A1, A2 at INTERNAL, the INTERNAL accuracy observation, switch, lock loss and synthetic controls (unchanged).

## Evidence in this packet

| File | What |
|---|---|
| `model/meter_rules_model_r5.py` | Desk model: the round-4 model plus rule 1's deviation check up to a gap, the meter lock (hold/drop), the servo state machine, C0/C1/C2 counters, and the gap bound as a parameter |
| `model/run_model.sh`, `model/sections/<name>.out`, `.rc`, `.err` | One process per section, all rc 0, stderr empty. New sections: `random` (N), `formula` (O), `counter` (C), `legs5` (V5), `steps5` (S5), `gapbound` (G), `alias` (Z). Round-4 sections re-run: `bound regress fill p1 loss steps tol fstep legs shapes` |
| `model/compare_r4_r5.py`, `.out`, `.rc` | The round-4 sections against round 4's published output (round 4 packet `meter_rules_model_r4.out`): K, R, F, M, P, Q, V, A identical. S differs in 112 lines and T in 5, each checked as an expected change. rc 0 |
| `model/second_run.txt` | A second run of every new section is byte-identical |
| `run_gates.sh`, `gates/` | Gate script and receipts at `f4f0ecb4` |
| `table_render_check.py`, `.out`, `.rc` | Every table of the page rendered with the pinned renderer: 24 tables, 198 rows, 0 irregular |
| `taken.md`, `review_ready.md` | The two posted comments |
| `PR-BODY.md` | Prepared body for PR #631 (first line [A482] kept; Round 5 section; "Relates to #629"; no closing keyword) |
| `MANIFEST.sha256` | sha256 of every file above, verifiable with `sha256sum -c MANIFEST.sha256` from this directory |

No single file is over 200 KB: the model output is kept per section, with no concatenated file.

## Not done, by the rules

No push, no PR edit, no merge, no hardware, and no RTL, builder or processor change. Pushing the commit, applying `PR-BODY.md` and publishing the packet are the manager's.

R429-4 and R428-4 noted, as manager duties, that round 4's published `MANIFEST.sha256` lists a `run_gates.sh` the archive lacks. This packet carries its `run_gates.sh`, listed in its manifest.
