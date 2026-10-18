# Independent verdict and ledger, written before reading prior review findings

Exact head 8f3c376d1e07d2f1417889ae2ac590c71b8cb910 (tree 359e2e25).
Verdict: NEGATIVE (one MINOR).

F1 MINOR (Tests, Docs, Conformance): two consumer-visible claims of the new
asCapable departure path are not graded by any check.
 (a) The drop commit clears the presence and sync flags. A planted control that
     removes the flags write (drop_keeps_flags) passes 1634/1634; measured drop
     commit flags: head 0x0, control 0x1 (PRESENT with GM thisClock, not master).
     The sync bit is already 0 at the fall in phase 36, so "clears sync" is never exercised.
 (b) Restored capability with no Announces grants mastership through the
     re-armed receipt watch. A control that removes BECGATE's re-arm
     (held_no_rearm) passes 1634/1634.
 The PR body lists "gm_present stays 0 ... after a dropped peer" as a known limit
 "unchanged by this PR". This PR introduces the asCapable drop state (at base the
 only departure, BECOME, sets PRESENT).

| lens | verdict |
|---|---|
| Conformance | UNCLEAN (F1 wording on gmPresent scope) |
| RTL | CLEAN |
| Robustness | CLEAN |
| Tests | UNCLEAN (F1) |
| Docs | UNCLEAN (F1) |
