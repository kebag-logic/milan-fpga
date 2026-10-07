[R533] NEGATIVE - exact head 500b8f64443777685e6a54049d933476710d26f0

Round R533-5, external independent delta review of issue #665 / PR #690.
Tree: b1b7d3b1b9dcf7d8f3f7f299365392ebc1f17ed8.
This independent verdict and ledger were written before reading prior review findings or reports.

R533-5-F1 | MAJOR | Conformance, RTL, Robustness, Tests
Artifact: sw/firmware/ctrl/srp/srp_mbx.c:373; sw/firmware/ctrl/loop/ctrl_loop.c:129; third_party/lwSRP/doc/integrator.md:215; sw/firmware/ctrl/test/srp_fixture.hpp:142.
Authority/evidence: the new pin requires receive-payload retry after temporary propagation reservation fails. The adapter consumes the mailbox record before calling mrp_rx, counts every negative result as malformed, and retains no payload for retry. An existing registered Listener now needs temporary storage even for its withdrawal. In independent.cpp, establish Ready, exhaust the actual static pool, receive valid Lv, release every held block and service another 10 ms. Both interface configurations remain active, received=1, malformed=1, stops=0. The identical probe with the previous library pin stops correctly: active=0, received=2, malformed=0, stops=1. Milan 4.2.7.2.2, the F4 rapid-withdrawal contract and FR_NFR 3.4.1's prohibition on dropping accepted records apply. The four adjusted fixtures correctly preserve their post-receive allocation tests but do not cover this new receive-refusal obligation.
Impact: a valid withdrawal can be permanently lost locally after transient exhaustion; storage recovery does not revoke the talker's licence. This is a dependency-integration regression, distinct from the passing ordinary #608 LV case.
Required outcome: handle the new recoverable receive failure without losing the accepted payload or later attributes, preserving interface identity, ordering, lifecycle cancellation and bounded service. Add a receive-time exhaustion/recovery regression alongside the existing poll-time allocation tests. Do not label a valid transiently refused PDU as malformed.
Verification: the attached exact-head probe must pass at IF=1/2 without retransmission from the peer, and an appropriate retry-removal plant must fail it. Recheck mixed-attribute payloads, repeated refusal, link reset and cross-interface ordering, plus the unchanged coverage ratchet and existing SRP campaign.

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN, F1 | REQUIREMENTS.md:23; docs/reference/FR_NFR.md:332; srp_mbx.c:349; lwSRP integrator.md:215; independent.cpp | R533-5 | 500b8f64443777685e6a54049d933476710d26f0 |
| RTL | UNCLEAN, F1 | srp_mbx.c:342; ctrl_loop.c:122; mbx.c:132; lwSRP mrp_mad.c:534; production-scope diff | R533-5 | 500b8f64443777685e6a54049d933476710d26f0 |
| Robustness | UNCLEAN, F1 | srp_mbx.cpp lifecycle/shared-binding/#608 cases; independent.cpp; receipts/head-probes-if1.log and head-probes-if2.log | R533-5 | 500b8f64443777685e6a54049d933476710d26f0 |
| Tests | UNCLEAN, F1 | srp_fixture.hpp:142; srp_mbx.cpp:333; srp_mutants.py; fw_coverage.py; coverage.ratchet; receipts/campaign.log and probes.json | R533-5 | 500b8f64443777685e6a54049d933476710d26f0 |
| Docs | CLEAN | sw/firmware/ctrl/srp/README.md; docs/reference/SUBMODULES.md; docs/testing/CI_WORKFLOWS.md; .github/workflows/rtl-fast.yml; public author-r5/HANDOFF.md; receipts/sizes.json and submodule-docs.log | R533-5 | 500b8f64443777685e6a54049d933476710d26f0 |

All five lenses have been independently applied. Prior public findings will now be reconciled before completing this report. Final integrity verification and receipt manifest are pending.
