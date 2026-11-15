# Reviewer triage of the mechanical sweep at 4ae887a16674416fdbf9c3dc0a0e3aed056906f6

Input: `receipts/figure_sweep_auto.tsv` (824 hits, 541 without a history marker), byte-identical to the author's
reassembled `figure_sweep.tsv`. Read with `scripts/hit_context.py` (every unmarked hit, with its context) and
`scripts/weak_markers.py` (every HIST hit whose only marker is a weak word: 40 sentences, 74 hits,
`receipts/weak_marker_hits.txt`). Off-sweep probe: `scripts/removed_constants.py` (`receipts/removed_constants.tsv`).

## Unmarked hits (541), by group

- **Another quantity, not a moved constant's figure (the bulk of ROW):** measurement prose and tables of earlier
  records (SPLIT_CONTROL_MEMORY.md :634-:1994, :2569-:2664; ctrl_service_budget/README.md :505-:1136, its 5xx/6xx
  measurement tables; ctrl_service_hooks/README.md :439-:474; MAILBOX_SPLIT.md :792-:830; SAVED_STATE_FORMAT_32X32.md
  :287-:310; ctrl_nvm README/nvm_store.h; milan_soc.py guard times; media_phase, aaf_clock_meter, mmcm, render sims),
  clause/table numbers read as ms (5.22, 5.26, 5.42, 5.43, 5.50, 5.54), step sizes (0.01 ms in paced_rows, rows_grade,
  rows_tiers, queued_bound docstrings), the 0.70 ceiling, plant offsets (flip_grade.py:107/:109 0.001).
- **T_svc and per-path budget bounds (AUTO tier1_rows.CHANNEL_BOUNDS 20 ms):** FR_NFR.md :344-:443 table rows and
  derivations, MAILBOX_SPLIT.md :817/:867/:2099, acmp_mbx.h:140, ctrl_service_bounds.py:53, budget README :422/:996/
  :1147/:1150/:1504, build.py:59, flip_grade.py:16 ("tier 1's 20 ms" for R4L, ACMP/ADP/MAAP at 30 in the same line),
  hooks README :115-:451, hooks_selftest.py:344. Each is T_svc or a measured path's own budget, not the tier-1 channel
  rows' bound (30 ms at the head, stated beside it where the rows are named: FR_NFR.md:380).
- **Standards figures:** FR_NFR.md:415 JoinTime 200 ms (180 to 240), the clause's value; README.md:448
  `JOIN_TIME_MS_C` 200 ms (the fabric's constant); milan_dp README :1610/:1639 and srptx.hpp :82/:83, twin_grades.py:147
  are #916 (known, not this PR's).
- **History tables and history chains:** SPLIT_CONTROL_MEMORY.md :2364-:2370 (the rows-history table, each row
  labelled by its move), :2342/:2353/:2377/:2380/:2405/:2457/:2479/:2509 (past-tense chains), load_grade.py
  :126/:171 (restatement history), :2602 (an earlier comparison table), PR body :148-:713 (round narratives, quotes,
  token lists, findings rows).
- **The head's own or beside it:** :2205 (127.21 held to 130, 12180198's beside), :2491 (PACED members 260/300 and
  325/595, the head's), aecp_mbx.h:62 and ctrl_loop.h:208 (decision D's 125 ms with the 1x1/1if 130 ms beside),
  rows_grade.py:15 and rows_tiers.py:24 (decision D's BOUNDS, which rows_grade.BOUNDS still are), rows_tiers.py:934
  and load_grade.py:570 (self-test plants), ctrl_loop.h:263 (the slice ruling's 800 us beside the rule's choice).
- **Plant description, true but labelled by the superseded bound:** ctrl_service_budget/README.md:1490
  (`AECP_QUEUED_MS` planted "past 125 ms at 1x1/1if"; the plant is 1,250, the head's bound 130). RESIDUE R2.

No unmarked hit states a superseded figure as current.

## Weak-marker HIST hits (40 sentences)

Each read in full. tb/verilator/ctrl_service_budget/README.md:172 gives decision D's 125 ms and, in the next sentence,
the 1x1/1if 130 ms; sw/firmware/ctrl/aecp/README.md:120 gives 130 at 1x1/1if with decision D's 125 beside; FR_NFR.md
:381/:392/:415 are derivations with history beside; PR body :121 is labelled "The rows at e4d80a8a". None states a
superseded figure as current.

## Off-sweep (removed constants; verdicts with no moved figure)

`removed_constants.py`: 10 `#define`s at 66f71326 are gone at the head (AECP_QUEUED_CEILING_MS, AECP_QUEUED_PASSES,
CTRL_LOOP_DRAIN_TAKES, CTRL_LOOP_SRP_DRAINED, CTRL_LOOP_SRP_DRAINS, CTRL_LOOP_SRP_FIRST_US, CTRL_LOOP_SRP_MS,
CTRL_LOOP_SRP_PASSES, CTRL_LOOP_SRP_RECORD_US, CTRL_LOOP_TX_PASSES); three lines name one, all CTRL_LOOP_SRP_MS:
- SPLIT_CONTROL_MEMORY.md:2010, present tense, in a subsection whose framing (:1970) says only two of its statements
  no longer hold and that a retried notice "is now inside its 20 ms under any input, by construction": F1 (MINOR).
- :2519, names it as a bound THE TIERS replaced: correct.
- :2522, present tense under :2519's "The three bullets below record the loop before them": RESIDUE R1.
