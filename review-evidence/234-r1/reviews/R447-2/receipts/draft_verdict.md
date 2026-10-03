[R447] NEGATIVE - exact head 0feff20fa228d0cb91d507943e6d39495b28b880

DRAFT (own verdict and ledger written before reading any other reviewer's report; final text follows)

F1 MINOR Conformance, Robustness, Tests, Docs: exit-code contract not total (malformed baseline record fields: traceback rc 1 or silent pass; non-ASCII digit in route status: traceback rc 1). receipts/probe_contract.log, receipts/probe_route_real_A.log.
F2 MINOR Conformance, Robustness, Tests: a route status report without its routable and fully-routed rows reads as a complete route (exit 0). receipts/probe_route_real_A.log.

| lens | state | covering round | head |
|---|---|---|---|
| Conformance | UNCLEAN (F1, F2) | R447-2 | 0feff20f |
| RTL | CLEAN | R447-2 | 0feff20f |
| Robustness | UNCLEAN (F1, F2) | R447-2 | 0feff20f |
| Tests | UNCLEAN (F1, F2) | R447-2 | 0feff20f |
| Docs | UNCLEAN (F1) | R447-2 | 0feff20f |
