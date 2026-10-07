[R532] NEGATIVE - exact head c1049de1970e93d2c36ace62891ee9d947cd3191

Recorded before any prior review report on PR #690 was opened.

Findings (independent pass):
- R532-3-F1 MINOR Tests - sw/firmware/ctrl/srp/srp_mbx.c:313-325 (round-3 Applicant inheritance)
  undiscriminated: plants RP3 (inherit only from the replaced slot) and RP10 (inherit from any
  StreamID) survive the whole srp_mbx.cpp suite at IF=1 and IF=2; reviewer probes show both are
  observable wire defects (stale Ready after the original eligible binding leaves; missing Ready
  for a rebound registered StreamID). Head passes the probes.
- R532-3-F2 MINOR Tests, Docs - sw/firmware/ctrl/srp/srp_mbx.c:334 Domain-VID guard on the final
  unbind undiscriminated (plant RP5 survives; probe shows an MVRP Leave for SR class VID 2 under
  the plant); sw/firmware/ctrl/srp/README.md:65 states the final binding releases its VID with no
  Domain-VID exception.

Ledger (independent pass):
| Lens | Status |
|---|---|
| Conformance | CLEAN |
| RTL | CLEAN |
| Robustness | CLEAN |
| Tests | UNCLEAN (F1, F2) |
| Docs | UNCLEAN (F2) |
