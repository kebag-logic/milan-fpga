# #977 round 12 handoff

**Status (2026-11-28 00:50 CET):** REVIEW READY at `3256d1d21e525e564eb92d1cf721750ddf44fde2`, with tsn-c-stack `5a07d9b7` and lwSRP `e27b34c9`, both unchanged. The tree is clean, and nothing is pushed or posted. Every gate the resume asked for passes, and every product ELF is byte-identical to 25ff0632's (80 of 80). The 8x8/1if load is 0.78214, within the 0.79 the owner is asked for, so there is no STOP. The ceiling commit `3256d1d2` is last and droppable, and it cites "owner decision pending"; the manager amends the citation when the owner answers.
**ETA:** done. Next: the manager publishes REVIEW-READY.md, PR-BODY.md and receipts/, plus the appended notes in round10/receipts/INDEX.md and round11/receipts/INDEX.md, which remain to be published.

## Commits past 3181a3ec

- `feefd047` reverts the 0.78 ceiling (9976b94f).
- `0a71ca6b` R958-3-F1: the flip check's ceiling-control names are built from `RULED_FLIP`/`EDGE_1IF`, and both adapters (`flip_grade.flip_checks`, `load_grade.ceiling_checks`) fail any escape they do not name.
- `ddf5c568` item 1, the deliveries cost against the ordinary passes after the delivery window, with the measured floor, plus R957-3-R1, R957-3-R2 and S1.
- `3256d1d2` item 2, the single droppable 0.79 ceiling, owner decision pending.

## Log

- 23:51 resumed at 3181a3ec; no units running.
- 23:52 deliveries against the ordinary passes in the 50 ms after the window (tools/deliv12.py over every registering log of both arms at both points): 8x8/1if 15,104 cycles a sink (answering-ports swap, its after-median 12,089), 160 us by the rule; beside it 125 us (50 ms before) and 145 us (500 ms before); 1x1/1if 18,778, 200 us (190 and 200 beside). Reverted the 0.78 ceiling (feefd047).
- 23:5x 0a71ca6b: at its head no flip_checks failure; with 8x8/2if at 0.71 both paths fail the ceilings control; an unnamed escape is reported by both; flip --selftest 628/628.
- 23:5x ddf5c568: loads at the pin: 8x8/1if 0.78214 (0.76614 without the term; 0.77864 and 0.78064 at the 50 ms and 500 ms before-record costs); 1x1/1if 0.53254. load --check PASS, --selftest 32/32, load_deliveries every control refused. 0.78214 <= 0.79: no STOP.
- 23:5x 3256d1d2: flip --check at 1x1/1if and 8x8/1if PASS, --selftest 628/628; 0.790 passes, 0.791 fails; with 8x8/1if at 0.77 both ceiling controls escape; 8x8/2if at 0.71 fails through flip_checks and ceiling_checks; `git apply -R --check` of its patch is clean; `git diff --check` against 71bad8c0 and 0b594023 is clean.
- 00:00 first units r12-elf and r12-gates had relative output paths and failed at once (plat_ledger refused an in-clone build dir); stopped r12-elf (mine); clones cE and cG left clean (porcelain 0). The partial r12/oE is left in place, not removed. Restarted as r12-elf2 (out r12/oF) and r12-gates2 with absolute paths; gave cG the ref origin/dev-soft-core = 0b594023 for the em-dash gate.
- 00:02 appended the dated supersession and publication note to round10/receipts/INDEX.md, and a publication note to round11/receipts/INDEX.md. Both are appends only; these notes remain to be published with the next packet.
- 00:13 r12-elf2 done: plat_ledger PASS, 80 ELFs, every sha256 identical to 25ff0632's (r10d/oZ); receipt receipts/elf-identity-3256d1d2.txt (host paths stripped from the plat_ledger part). r12-gates2 still in run.py --self-test.
- 00:44 r12-gates2 done (clean clone cG at 3256d1d2): harness self-tests all rc 0 (run.py --self-test 0 failures, kept 33, load 32/32 and --check, flip 628/628 and --check at 1x1/1if and 8x8/1if, shape_costs 25/25 and --check); py and cpp idiom PASS; docs workflow 100/100, no tracked file changed.
- 00:46 receipts copied; host paths in the run.py log and docs steps replaced by <clone>/<out>/<scratch>/<home>; run.py log gzipped (1.05 MB); receipts/INDEX.md generated (index.py) with a publication note.
- 00:50 REVIEW-READY.md and PR-BODY.md written (PR body link labels "[the internal review]" / "[the external review]"). Scratch left in place, nothing removed: r12/cE, r12/cG, r12/oE (partial), r12/oF. /data has 33G free.
