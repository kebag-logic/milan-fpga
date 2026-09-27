# Reviewer sweep disposition at 92c6154a17d1f1192f20a3a642e6a01b616afb67

Raw hits: `receipts/sweep_92c6154a.txt` (script `scripts/sweep.sh`, whole tracked
tree, gitlinks not recursed). Parent comparison: `receipts/sweep_867a2e38.txt`.
Supplementary searches (run by hand, recorded in REPORT.md section "Sweep"):
`pend_i` composition statements, `sticky` statements with pend/mark/name/map/class/D2,
every `D2` scope reference, every `_nc_w` reference, and `mark` in READMEs,
testing docs and scripts.

| Pattern group | Hits at head | Disposition |
|---|---|---|
| `aecp_mark_pend`, `mark_pend` | 0 | none remain |
| `every commit beat`, `conservative duplicate` | 0 | none remain |
| `[Cc]onservative` | 42 | all unrelated (CDC flags, CI classification, shapers, builder, firmware); none about pending |
| late-mark / mark-tail | 11 | CHANGELOG:45, MAT:245, TESTING:268, measure_test_evidence:601, pp_shadow README:101, pending_mutant.py:4/60/64/67 name the deliberate historical mutant (accurate); MAT:1973 is the dated evidence-model limits list; MAT:2083 now RESOLVED |
| program tail | 5 | MAT:218, 2073 labelled historical; MAT:271 is the proposed D3 rule 3 rationale (marks do follow writes; accurate); sim_main.cpp:264/1389 test comments/labels (accurate) |
| class-6/7 wording | 4 | MAT:213 historical; OWN:976 and KL_pp_shadow.sv:927 say marks keep completion meaning (accurate); OWN:1378 labelled "Original parent use" |
| commit mark + pend/trigger/sticky | 2 | MAT:213 historical; MAT:1612 IDENTIFY row (SET_CONTROL carries no mark; unrelated) |
| NVM_MARK + pend/trigger/sticky/durable | 0 | none |
| `#502` | 40 | all read as resolved/landing or as dated history; MAT:1654-1676 keep landing as a release prerequisite (true until merge); MAT:2225 labels the round table as history; checked individually |
| `reads durable over` | 6 | FASTCONNECT:1118, MAT:1124, OWN:602/1744/1917, nvm_cosim cases:1208 are other contracts or now-correct #502 text |
| supplementary: `pend_i` composition | 13 docs/RTL lines | all current or D3-proposed EXCEPT `docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md:1354-1355` (finding F1) |

MAT = docs/design/SAVED_STATE_MATERIALIZATION.md; OWN = docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md.

Residual current-state statement of the old trigger: exactly one,
`docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md:1354-1355`
("Parent use: KL_pp_shadow drives the backend's
`pend_i = aecp_dyn_dirty_o | (|nvm_unflushed_o) | <the D2 sticky bit>`"),
where the same page defines the D2 bit as "a class-6/7 mark set sticky pending"
(now labelled "Original parent use", :1378-1383). It is not reached by any of the
author's seven published patterns (`receipts/author_sweep_repro.txt`).
