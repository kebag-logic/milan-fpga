[A829] REVIEW READY

Commit: `4adfa9dc84f58c1c7ad23d6a64fa019985fe62a1` (local only; nothing pushed or posted).

Changed:
- `f7b90e3b7`, Arty row step 1: slice 1250 us, pace 10 ms, transmit bound 35 ms, retry cold 130 us and raised stated costs.
- `74f942be5`, step 2, from the complete census at step 1's row: poll base 235, centisecond 160, LINK 190, MAAP 165, withdrawal 95 us.
- `2d911d2bf`: docs section 15 with the qualification figures.
- `4adfa9dc8`: the receipt regrader applies `run.py`'s #969 disposition.
Both row steps are installed exactly as the rules derive them.

Validation:
- At `74f942be5`: four firmware shards, Arty native boot (0 findings), native controls 6/6, region self-test.
- Service self-test 297/297; `rows_tiers` 1033/1033, `load_grade` 28/28, `egress_ledger` 21, `record_classes` 9/9; `arty_grade` and its self-test; `test_ctrl_memory`; MII/`lat` 15/15.
- At `4adfa9dc8`: all ten documentation and idiom gates.
- Route: all three directives clear the floors at all four corners. Selected AltSpreadLogic_high, WNS +0.433, WHS +0.050 ns; 33015 LUT / 40369 FF / 78.0 BRAM.
- Qualification: PASS over 147 cases, with the derived model equal to the installed row. Load 0.5005, ACMP 29.77/30 ms, txL 48.82/49 ms, last notice 117.47/140 ms, longest pass 1.785/2 ms. Held-egress rows are below their ledger.
- `receipt_regrade.py` over the packet: 147/147 grades reproduced, cross-case PASS, timing PASS. A control packet without `srp-bound` is refused.

Acceptance criteria: the Arty row is re-derived by the rule, installed, qualified by a complete census at it, and routed at every corner. #878's bench items stay as ruled: #878 stays open for #1007's offset criterion.

Open risks/questions:
- The derivation applies #969's disposition (`kept_grade.py` PASS): `srp-kept`/`srp-bound` registrations over their statements are owed to #977 and excluded from the maxima. Without it no row meets the 140 ms last-notice bound. A reviewer should confirm this reading of the 2026-11-23 amendment.
- Step 2 regrades step 1's traces rather than measuring again; every run input is identical and the identity proof is in the receipts.
- ACMP, txL and the longest pass sit within 0.25 ms of their bounds.

Evidence: [PR-BODY.md](PR-BODY.md), [receipts/INDEX.md](receipts/INDEX.md).
