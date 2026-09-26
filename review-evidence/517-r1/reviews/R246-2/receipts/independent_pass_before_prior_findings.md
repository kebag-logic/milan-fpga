# R246-2 independent pass (written before reading any other reviewer's findings on this round)

Written: 2026-09-26T10:52:59Z. Head 1d694677c8f376ec44e3b59b1d7fa7abccda106b. Delta judged: f36b40dd..1d694677 (7 files, +49/-25), with the full PR at head re-read where the delta touches it.

Provisional verdict: POSITIVE. No BLOCKER, MAJOR or MINOR finding at this head.

My prior findings:
- R246-1 F1 (MAJOR; Conformance, RTL, Docs): CLOSED. sim_nxn.cpp is byte-identical to base again; five --exclusive marks removed; docstring/README/TESTING state the write set I measured (per-leg strace + timestamp audits with positive controls: 5 writers x 14 private files in distinct milan_nxn_* dirs, 6 legs no data files, no shared written path, no repository write during the pooled phase).
- R246-1 F2 (MINOR; Tests): CLOSED. Runner launched with its own INT/TERM/HUP default + empty mask; the only ledger read happens while both writers are held. 25+24 runs default and 25+24 runs inherited-ignored all 28/28; R245-1 runner 761ec858 fails 6/6 runs; M15/M16/M17 killed; removing the new preconditions (T1) brings back 12 failures under inherited-ignored.
- Suggestions S1-S5: unchanged, assigned to #495 by the manager decision.

New SUGGESTIONS only: (a) the no-repository-write statement assumes gmstep-build has already refreshed the interpreter caches, which make run always does; a leg run by hand on a fresh checkout writes ignored __pycache__ files (atomic). (b) obj_aclk (~450-465 s) is ~85% of the ordinary phase and starts last, so the pool is bounded by it; starting it first (replay order unchanged) would be the remaining lever.

Provisional ledger: Conformance CLEAN, RTL CLEAN, Robustness CLEAN, Tests CLEAN, Docs CLEAN, all R246-2 at 1d694677c8f376ec44e3b59b1d7fa7abccda106b.
