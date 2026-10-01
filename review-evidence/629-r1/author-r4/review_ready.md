[A487] REVIEW READY
Commit: `1bdd68957dd1357645c500014002b1e5a115864c` on `629-media-clock-follow`: two commits on `a463a1de`, `0cf1ef48` (the answers) and `1bdd6895` (four statements made exact). Both are local and not pushed; pushing them and applying the prepared PR body are the manager's.
Changed: `docs/design/MEDIA_CLOCK_FOLLOWING.md` only (+337 / -102). The index row is unchanged. No RTL, builder, generator, config or processor change.

- **1. The rulings** (R428-3 F1 = R429-3 F1). The header, the D1, D2, D4, D5 and D8 sections and the Decisions table now record the [rulings on round 3](https://github.com/kebag-logic/milan-fpga/issues/629#issuecomment-5937449258): D1 = L1, D5 = C1 with E8, D8 = E8, and D2's wording. They also record the owner's [D4 = A2-a](https://github.com/kebag-logic/milan-fpga/issues/629#issuecomment-5937643550). Each ruling is linked. Limits links #633, and gains the owner's [known risk](https://github.com/kebag-logic/milan-fpga/issues/629#issuecomment-5937848189): A2-a meets Milan v1.2 7.4's +/-50 ppm at INTERNAL only for an oscillator grade of +/-39 ppm or better; the grade is assumed adequate and is unconfirmed. The bench gains an INTERNAL observation row.
- **2. The packet-loss cliff, option (b)** (R429-3 F2). New subsection "Lost PDUs".
  - A sequence gap voids only its group and restarts nothing. Every other restart stays.
  - The next valid pick is checked across the gap: one voided group needs 4 ms +/- 5,120 ns, and two or more restart the history.
  - Snapshots stay on the group grid. A loss-voided snapshot group is filled with the midpoint of its neighbours, which is exact for any talker rate and within J.
  - **Bound:** a continuity bound must satisfy 2J + 601k <= B_k < 10,417 - 2J - 601k. That holds up to k = 3 group intervals and fails at 4. The design takes one voided group at a time, since a fill inside a two-group gap needs a division by 3.
  - **Pattern:** the rate stays valid within E8's bound, and the servo stays LOCKED, while every loss-voided group has fully received neighbours. Lost PDUs that share a group or lie 32 or more PDUs (4 ms) apart always qualify: up to 250 loss events a second.
  - **Beyond the bound:** a locked servo holds its trim and stays LOCKED (`KL_mmcm_drp_servo.sv:613-615`, `:567-568`). The rate never validates only when such gaps recur within every 4.1 s: about 11 lost PDUs a second at random, against one per 4.1 s before.
  - **Tests:** meter rows for single-PDU loss at 1 in 1 s and 1 in 0.3 s, with the restart-on-any-loss mutant; a snapshot-group loss; the bound; a step inside a loss gap. A trim-graded loss leg in the servo-with-meter row, and a loss leg in the C1 counter row. Each has a failing mutant.
- **3. Suggestions:** R429-3 S1, S2 (a 16-phase step sweep) and S3 (Milan v1.2 4.4.2.3, Annex B.1); R428-3 S1 and S3; R428-3 S2 is superseded by item 2. One pre-existing defect is fixed: the round-3 servo-with-meter table row rendered broken, because a pipe inside a code span split its cell.

Validation, at `1bdd6895`, from the lane worktree, each unpiped with output to a receipt:
- The pinned Markdown environment: `scripts/docs_check.py` (0 findings); `scripts/check_doc_style.py` (OK); `scripts/gen_toc.py --check` (OK) and `--verify-anchors` (292 links); `scripts/check_em_dash.py --base d4dd7426` (0 findings over 1,341 added lines); `scripts/check_doc_paths.py` (875 paths resolve).
- `python3 scripts/check_entity_shape.py` (`checks: 166 failures: 0`).
- `git diff --check` on the worktree, on `d4dd7426..HEAD` and on `a463a1de..HEAD`.
- All rc 0.

The desk model `meter_rules_model_r4.py` (rc 0, deterministic; a second run is byte-identical):
- **No loss:** equal to round 3's published output in all 40 shared E8-P2 cases, field by field.
- **Rule (b):** 0 restarts and 0 drops at 1 PDU lost in 1 s, in 0.3 s, in every snapshot group and in 32. The restart-on-any-loss mutant never validates under any of them.
- **Error shapes with losses:** 204 cases, every round-3 shape at +/-1,042 and +/-1,426 ns, 0 and 300 ppm, plus plant gains 0.8 and 1.2. None restarts or drops LOCKED, and every window is under 1,024 ns. The worst is unchanged: 773 ns at a plant gain of 1, 868 ns at 1.2.
- **Steps inside a loss gap:** 64 of 64 restart once; with the check across the gap removed, none restarts.
- **Tolerance:** the edges are unchanged with loss.

Acceptance criteria: the round-4 items 1 to 3 are met as above. #629's implementation, simulation and bench items stay open; this is the design step.

Open risks/questions: one point is flagged on R429-3 S1. The page states J / T as asked; the headline holds, at 18 ns over the test at 1,042 ns. The page also states that the tight bound for an arbitrary estimator is 2J / T, as R428-3 section 1 has it. Error-free data of slope s is consistent with every rate within 2J / T of s, with a rising or falling ramp and a free phase. The pairwise argument sees one end of that set. This changes no conclusion and needs no decision unless a reviewer disputes it. The loss rule is shown in the desk model only, as is the rest of the meter.

The packet holds the model, the comparison, the gate receipts, HANDOFF.md and PR-BODY.md (with "Relates to #629" and a Round 4 section). Stopping here.
