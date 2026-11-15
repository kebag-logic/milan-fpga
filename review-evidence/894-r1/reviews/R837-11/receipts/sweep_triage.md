# Reviewer sweep triage, exact head 478ff78cc7752635147511490b06a0aa9ec1f25c

Inputs: `scripts/constant_history.py` (every value each stated constant took over the PR's 125 snapshots, base
66f71326 to head; `constant_history.txt`, 73 constants moved) and `scripts/figure_sweep.py` (`figure_sweep.tsv`:
797 files, 720 hits). Scope: every Markdown file the PR changes, every first-party README, every first-party source
line under `sw/` and `tb/`, and the PR body. The rules pair each moved constant's subject with its superseded values;
ROW and LOAD flag every two-decimal ms figure and three-decimal load not among the head's rows (`flip_grade.py --check`
at both points) and loads (`load_grade.py --check`, `tier_grid.py --point 1x1/1if`).

Every hit without a history marker (470) was read; hits with only a weak marker ("first", "since", "once", "from N")
were read again (`weak_marker_hits.txt`, 32 sentences). Classification:

| Class | Sites |
|---|---|
| Superseded figure stated as current: finding F1 | SPLIT_CONTROL_MEMORY.md:2204-2205 (14.60 / 91.59 ms "held to 125" at 1x1/1if; 20.25 / 647.23 ms at 8x8/2if), and :2207 ("At 1x1/1if both are decision D's tier bounds") |
| Superseded figure stated as current: finding F2 | SPLIT_CONTROL_MEMORY.md:2477 (`EDIT_RECORD_US`, 260 us at 1x1/1if and 325 us at 8x8/2if) |
| Completeness claim the two above falsify: finding F3 | PR body section 15 / Status round 15 ("Every superseded 1x1/1if row figure ... is stated as history or beside the head's"), section 17.2 ("None states a superseded figure as current"), REVIEW READY issuecomment-6892298990 ("None is current") |
| Wording around figures correct at their own head: residue | SPLIT_CONTROL_MEMORY.md:2427 ("None (the head)"), :2432 (present-tense what-if), :2244 ("before #894, ... R4 is"); PR body:67 ("and its TICK stand") |
| Known, its own Issue (#916) | tb/verilator/milan_dp/srptx.hpp:82-83; tb/verilator/milan_dp/README.md:1610, :1639 |
| Clause figure, not a statement | FR_NFR.md:415 (JoinTime 200 ms, 180 to 240); twin_grades.py:147; README.md:448 (`JOIN_TIME_MS_C`, the RTL engine's); ctrl_service_budget/README.md:624 (the path's W, JoinTime) |
| History or anchored to a named head | every other SPLIT_CONTROL_MEMORY.md section 13 hit (rows-history table :2360-2370, :2287, :2310, :2312-2322, :2342, :2353, :2377, :2380, :2402, :2457, :2467, :2479, :2498, :2509, :2602 at a30c9986); FR_NFR.md:383, :389; aecp_mbx.h:46-50; PR body round sections and the 14.1 old/head table |
| Another quantity | the CPU budget harness's S2-era and cache-arm measurement tables and prose (ctrl_service_budget/README.md, ctrl_service_hooks/README.md), sections 9 to 12 and 14 measurements, MAILBOX_SPLIT.md's F0 access bounds, NVM and media figures, code literals and plants (load_grade.py:570, rows_tiers.py:934, flip_grade.py:135) |

Checked against the head: `EDIT_RECORD_US` = {1x1/1if: 300, 8x8/2if: 595} (`edit_rows.py:41`); the queued rows 14.66 /
127.21 ms at 1x1/1if within 20 / 130, and 20.93 / 806.60 ms at 8x8/2if (`gates/flip_1x1.log`, `gates/flip_8x8.log`);
`AECP_QUEUED_MS` (130u at one interface, 62u at two; `aecp_mbx.h:70`); 0.695 with every notice the largest legal one
and 10 of 420 designs (`tier_grid_1x1.log`).
