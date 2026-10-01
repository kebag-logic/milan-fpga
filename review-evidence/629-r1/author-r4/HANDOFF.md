# [A487] HANDOFF: #629 lane M1, round 4 (design only)

Status: DONE for round 4. REVIEW READY posted; waiting for the round-4 reviews. Stopped.

- Branch `629-media-clock-follow`, start `a463a1deb9d63614e8bd2134ccd7b2cd541c72ed`, head `1bdd68957dd1357645c500014002b1e5a115864c` (two commits: `0cf1ef48` the answers, `1bdd6895` four statements made exact; local, NOT pushed). PR #631.
- Changed: `docs/design/MEDIA_CLOCK_FOLLOWING.md` only (+337 / -102). Index row in `docs/README.md` unchanged (still "proposed": nothing is implemented).
- No RTL, builder, generator, config or processor change.
- Assignment: #629 comment 5938156583. Reviews answered: R428-3 (PR #631 comment 5938155947), R429-3 (PR #631 comment 5938134329).
- Rulings recorded: 5935520588 (round 1), 5937449258 (round 3), owner 5937643550 (D4 = A2-a), owner 5937848189 (oscillator-grade known risk; supersedes the accuracy note 5937738214).
- Posted: TAKEN (#629 comment 5938185645) and REVIEW READY (#629 comment 5938892492) with head `1bdd6895`. Nothing else posted; no comment edited or deleted.

## Gates at `1bdd6895` (receipts in `gates/`, each unpiped, all rc 0)

| Gate | Result |
|---|---|
| `scripts/docs_check.py` | 0 findings, 184 md + 955 scrubbed files |
| `scripts/check_doc_style.py` | OK, 22 documents |
| `scripts/gen_toc.py --check` / `--verify-anchors` | OK / 292 links reproduced |
| `scripts/check_em_dash.py --base d4dd7426` | 0 findings over 1,341 added lines |
| `scripts/check_doc_paths.py` | 875 paths resolve |
| `scripts/check_entity_shape.py` | `checks: 166 failures: 0` |
| `git diff --check` (worktree, `d4dd7426..HEAD`, `a463a1de..HEAD`) | clean |

Markdown gates ran with the pinned environment's interpreter, from the physical `/data` lane path (`run_gates.sh`). The script removes only the `__pycache__` directories its own run creates; the worktree was clean afterwards.

## Round 4: what changed

1. **Rulings (R428-3 F1 = R429-3 F1).** Header "Where the decisions stand" lists every ruling with its link. D1 L1, D2 wording, D8 E8, D5 C1 with E8 (C2 "not taken"), D4 A2-a (owner, in this issue's fabric lane), #633 in Limits, and a new Limits item for the owner's known risk: A2-a meets Milan v1.2 7.4's +/-50 ppm at INTERNAL only for an oscillator grade of +/-39 ppm or better; assumed adequate, unconfirmed; no PLL search or per-grade analysis; the bench records INTERNAL as an observation. The Decisions table's columns are now Ruling / Ruled by. The plan offset is shape-dependent (plan A -10.64 ppm; a TDM-master shape takes plan B -0.66 ppm, `sw/litex/milan_soc.py:347-356`); the Arty shapes take a 100 MHz input (`:228-230`). The page states both; the owner's text names the AX7101's 200 MHz oscillator (`:232`, `:341`). The part number is not written anywhere.
2. **Loss rule, option (b) (R429-3 F2).** New subsection "Lost PDUs":
   - a loss void (sequence gap: PDU lost or not consumed) voids only its group and restarts nothing; a deviation void and every other restart rule stay;
   - continuity across the gap: k group intervals from `sequence_num[7:4]` mod 16; k = 1: 2 ms +/- 4,096 ns; k = 2: 4 ms +/- 5,120 ns; k >= 3: restart; a gap of 256+ PDUs aliases in sequence_num but misses by >= 32 ms, so it restarts;
   - snapshots on the group grid; a loss-voided snapshot group is filled with `last + ((new - last) >>> 1)`: exact for any rate, error <= J;
   - **bound derivation**: 2J + 601k <= B_k < 10,417 - 2J - 601k; window exists for k <= 3, none at k = 4; K = 2 (one voided group) chosen because a fill in a two-group gap needs /3;
   - **pattern**: rate valid within E8's bound and servo LOCKED whenever each loss-voided group has fully received neighbours: lost PDUs sharing a group or >= 32 PDUs apart (up to 250 loss events/s). Generic bound for any E8 rate sequence with snapshot error <= J: 2.125 x 2J / 8 = 758 ns at 1,426 ns;
   - beyond the bound: restart; locked servo holds trim and LOCKED (`KL_mmcm_drp_servo.sv:613-615`, `:567-568`); never valid only if two-adjacent-group gaps recur within 4.1 s: ~11 lost PDUs/s random (p ~ 1.4e-3), against p ~ 3e-5 under round 3's rule;
   - test rows added (meter suite): periodic single-PDU loss 1/1 s and 1/0.3 s with the restart-on-any-loss mutant; snapshot-group loss with "next pick less 2 ms" (25 ns off) and "restart on voided snapshot" mutants; the bound with a "larger gaps accepted" mutant; a step inside a loss-voided group with a "no check across the gap" mutant. Servo-with-meter row: a loss leg with a +4 ppm step, graded on the trim (the mutant holds LOCKED but not the trim). Counter row: a loss leg (C1 moves nothing);
   - area +40 to 70 LUT, < 10 FF; total now about 420 to 660 LUT, 290 to 460 FF, 0 RAMB18.
3. **Suggestions.** R429-3 S1 taken with a correction (see "Open point"); S2 taken with a 16-phase sweep; S3 taken (Milan v1.2 4.4.2.3, Annex B.1). R428-3 S1 taken (104/351 open loop; 184/465 closed loop); S2 superseded by item 2; S3 taken (pinned seed, 120 s; 13 of 227 windows under P1).
4. **Also:** the round-3 servo-with-meter table row had `|e|` inside a code span; GitHub's table parser split the cell there (verified with the pinned renderer). Both such rows now escape the pipes; a check of every table finds no row whose unescaped-pipe count differs from its header.

## Open point for the manager and reviewers

R429-3 S1 says the indistinguishability bound for an arbitrary estimator is J / T. That is a valid lower bound, but not the tight one. Error-free data of slope s is consistent with every rate in [s - 2J/T, s + 2J/T] (rising ramp for the low end, falling for the high, phase free), so any estimator's worst case is >= 2J / T. That agrees with R428-3 section 1. The page states J / T as the assignment asked, keeps the headline (J / T at 1,042 ns over 512 ms is 1,042 ns per window, 18 ns above the test), and also states 2J / T as the tight figure with the reason. No decision is needed for the design; it is flagged in REVIEW READY.

## Clause findings (unchanged from round 3 except where noted)

- (a) Milan v1.2 5.3.3.6 is a minimum; an AAF INPUT_STREAM source may sit beside the CRF source; IEEE 1722.1-2021 7.2.32 caps the list at 216, no order.
- (b) Milan v1.2 5.3.11.1 (selection saved), 5.4.2.15 (no non-ATDECC change while locked), 5.3.11.2 Table 5.7 counters; free-wheel per IEEE 1722-2016 10.6 and 4.4.4.7 NOTE; no fallback is this design's choice.
- (c) `mr`: 4.4.4.3 / 10.4.3 shalls name CRF only; acted on for AAF too (PICS AAF-5 reading).
- (d) eight places where the current reading is wrong (FR-CLK-03, BAD_ARGUMENTS attribution, 7.2.2 citation, A2's clause, three stale RTL comments, matrix rows, flag label).
- New in round 4: IEEE 1722-2016 4.4.4.6 (sequence_num detects loss), 10.1 (CRF tolerates lost packets) and 10.6 ground the loss rule; Milan v1.2 4.4.2.3 and Annex B.1 (informative) for the 4.096 s hold; Milan v1.2 7.4 for the INTERNAL accuracy risk.

## Code map (file:line at dev `d4dd7426`; the page's Current state has the full table)

- Servo: PI `KL_mmcm_drp_servo.sv:228-233`; LOCKED -> ACQUIRE only on lock count 0 `:564-568`; HOLDOVER `:571-579`; PI and lock count run only on a valid rate `:613-615`; writeback `:689-694`.
- `KL_crf_rx.sv`: jump bound `:279-294`; lock/timeout `:296-298`; ring `:320-325`; restart incl. any sequence gap `:390-403` (`:398-400`); rate kept, valid cleared on break `:522-526`, `:596-605`; a gap resets the settle run only `:569-570`; timeout `:529-557`.
- RX monitor Table 5.6 counters (SEQ_NUM_MISMATCH, STREAM_INTERRUPTED): `KL_avtp_rx_monitor_ctx.sv:24-28`, `:173-174`.
- Clocking: `sw/litex/milan_soc.py:228-233` (board input), `:341` (audio from sys), `:347-356` (plans A and B).
- Root: decode `milan_datapath.sv:1554-1570`; `mr` triggers `:3108-3156`, `:3180-3203`; counters `:3469-3475`, `:3492`; INTERNAL free-run rule `:5713-5718`; aligner `:5733-5748`.

## Design options and the rulings

D1 L1; D2 M1 (P2 pick, B2 4,096 ns bound, 48 kHz base format); D3 W2; D4 A2-a (owner); D5 C1 with E8; D6 all five configs; D7 #632; D8 E8, plus round 4's loss rule (option (b)). All ruled.

## Parent-visible changes (page "Parent-visible changes")

Requirements FR-CLK-03/04 and status row; configs admit `input_stream`; builder `_load_clocking`, overlay, names, shape tables, its test; entity model `CS_TYPE`, tables, flag value, model id; generated shape headers (six tracked copies); RTL new meter (now with the loss rule); root decode and consumers, A2-a, C1 banner, request tap, stale comments; servo port renames; two CSR words; two gates' pinned text; docs. Round 4 adds the loss rule to the "RTL, new" row and fixes "A2-a (D4) and C1 (D5) as ruled" in the root row.

## Processor-visible changes (page "Protocol-processor changes"; protocol-processor #141)

No RTL or microcode. L6 and REQ-MDL-005 restated as a minimum and credited to IEEE 1722.1-2021 7.2.32 and Table 7-141; four top-level tests with mutants; lands first or with the parent. Unchanged in round 4.

## Test plan (page "Test plan")

Meter suite (rates, error shapes at the design point with a pinned seed, beyond tolerance, formats, wrap, lock, restarts, **periodic loss, snapshot-group loss, the loss bound, a step in a loss gap**, selection, pulses), servo (select, and servo-with-meter with a **loss leg**), `milan_dp` (true-ratio with an **A2-a mutant**, W2, switch, loss, echo, **counters under C1 with a loss leg**, CSR, AECP walk), builder; bench B AAF, B CRF, controls, A1, A2 at INTERNAL (passes under A2-a), **INTERNAL accuracy observation**, switch, lock loss, synthetic controls.

## Evidence in this packet

| File | What |
|---|---|
| `meter_rules_model_r4.py`, `.out`, `.rc` | Desk model, rc 0; a second run byte-identical |
| `compare_r3_r4_noloss.py`, `.out`, `.rc` | 40 of 40 shared no-loss E8-P2 cases equal to round 3's published output, field by field (rc 0) |
| `run_gates.sh`, `gates/` | Gate script and receipts at `1bdd6895` |
| `table_render_check.out` | Every table rendered with the pinned renderer: one broken row at `a463a1de`, none at the head |
| `taken.md`, `review_ready.md` | The two posted comments |
| `PR-BODY.md` | Prepared body for PR #631 (first line [A482] kept; Round 4 section; "Relates to #629") |
| `MANIFEST.sha256` | sha256 of every file above, verifiable with `sha256sum -c` from this directory |

## Not done, by the rules

No push, no PR edit, no merge, no hardware, no RTL/builder/processor change. Pushing the commit and applying `PR-BODY.md` are the manager's.
