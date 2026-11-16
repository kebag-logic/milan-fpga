[A790] REVIEW READY
Commit: `FINAL_SHORT` on `16ba667d` (#901's review head), branch `925-srp-ta-tf`; not pushed (the manager pushes and opens the PR).
Changed:
- `sw/firmware/ctrl/srp/srp_mbx.c` / `.h`: of a stream's Talker Advertise and Talker Failed, the one registered latest decides each binding's Listener declaration and the kind ACMP sees while it stays registered, and the other once it leaves (IEEE 802.1Q-2018 35.2.4, 35.2.6). lwSRP replaces the other type only for a JoinIn/JoinMt and registers a New beside it, so the adapter records the order from lwSRP's indications (`latest_kind`, `listener_kind`). The receive filter and the registrar walk were Failed first, which held Asking Failed until the talker's next MRPDU. A later binding takes the StreamID's latest from any binding of it. No SRP timer or bound changes; lwSRP, the mailbox contract and RTL are unchanged.
- Tests: `srp_mbx.cpp` `SrpTalkerKinds` (6) and `srp_feedback.hpp` (2). They cover TF->TA and TA->TF by New within a JoinTime, leave of either kind in both orders, coincident registrations in one MRPDU in both orders, a later binding, the fallback, and ACMP's view. `srp_kind_mutants.py` adds ten plants, each caught by name at both interface counts. The `failed-listener-ready` plant moved to its new site.
- `srp/README.md` states the rule. The ledger records `ctrl_plat` at 8x8/2if as 20,416 B (+64), still 60.5 RAMB36. COVERAGE_LINE
Validation (clean clones of the final head unless stated):
VALIDATION_LINES
Acceptance criteria: desk part met (above); the bench part (Listener Ready within 1 s of the Talker Advertise) is the gating run's.
Open risks/questions: OPEN_RISKS
