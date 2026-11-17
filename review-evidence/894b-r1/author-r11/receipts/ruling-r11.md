[A10] Ruling on the round-10 STOP: **the `service.aecp.last` ledger figure moves to the rule's 62.16 ms at 8x8/1if, by this ruling.**

- **Why:** both traces show phase, not cost. #930's cheaper records open the composed window 290 us earlier, so the hold releases at a different point in the millisecond, and ACMP's owed frame now goes before AECP's. AECP's last service moves 0.296 ms later while the other six held rows move earlier, all 0.22 to 0.37 ms under their figures.
- **Not a new miss in kind:** the row is one of the seven held-egress rows already owed to the stack issue. This PR's own fix moves its phase, which is the case #894 issuecomment-6892938049 item 3 leaves to a ruling.
- **The ledger file** names this ruling, states both measurements and keeps the rule's derivation.

**The #930 targets are met:**
- at 1x1/1if, SRP's record is 250 us against 280 and the last queued notice 136.65 ms against 140;
- at 8x8/1if, the load is 0.735 at the pin against 0.75;
- the restatements down to each point's earlier figures, never below them, are right.

The single column at the pin (item 4) is accepted. R4 by every source at 8x8/1if (21.39 ms) stays owed to #872.

**Round 11:** the ledger move, then the final gates the STOP left (the firmware campaigns, docs jobs, lane gates and verilator shards 1, 3, 4, 6, 10 and 17) on a clean clone, then REVIEW READY. Close #930 from the PR body.

