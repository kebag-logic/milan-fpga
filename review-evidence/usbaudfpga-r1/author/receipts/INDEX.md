Round-3 desk evidence passes at `75db86a926a9f4d2f7734246eac06a8f58c57bac`. The overall handoff is STOP because the initial documentation self-check violated required advance cleanup logging. Independent review [R2] is complete and NEGATIVE overall; the technical delta and evidence pass. External review, protected checks, merge validation and bench acceptance remain separate.

- [Independent review and coverage ledger](r3-internal-review.md)
- [Contract comparison and FPGA duties](r3-contract-delta.json)
- [Round-3 validation](r3-validation.md), [default-suite results](r3-default-results.txt), [million-frame result](r3-duplex.json)
- [All 70 planted defects](r3-planted-defects.json)
- [Fresh Arty route, corners, recipe and image hashes](r3-arty-route.json)
- [Final resource cost](r3-arty-cost.json), [crossings, skew and routing](r3-arty-crossings.json), [55-pad placement](r3-arty-packing.txt)
- [Retained generated inputs and current RTL](r3-arty-inputs.json), [reproduction](r3-reproduction.md), [fresh-synthesis helper](helpers/rebuild_audio.tcl)
- [ALINX complete payload comparisons](r3-alinx-payloads.json), [unchanged input closure](r3-alinx-lineage.json)
- [All network files unchanged](r3-network-identity.json)
- [Cleanup-rule exception](r3-cleanup-exception.md)
- [Frozen source digests](r3-source-digests.json), [receipt digests](r3-artifact-digests.json), [handoff-file digests](r3-deliverable-digests.json)
- [Completed runtime digests](r3-runtime-digests.json), [preliminary failed attempts](r3-preliminary-attempts.json), [resource limits and cleanup](r3-resource-budget.json)

The following round-2 evidence is historical. Its payload and unchanged-input proofs support the new comparisons; its old setup margin and verdict do not replace the round-3 route and review.

- [Desk validation](r2-validation.md)
- [Independent review and coverage ledger](r2-internal-review.md)
- [Arty routes, exact recipe and image hashes](r2-arty-routes.json)
- [Final routed resource cost](r2-arty-cost.json)
- [Crossings, skew, external timing and routing](r2-arty-crossings.json)
- [Actual 55-pad placement](r2-arty-packing.json), [complete endpoint receipt](r2-arty-packing.txt)
- [Named planted defects](r2-planted-defects.json)
- [Control-image and register-map pairing](r2-control-images.json)
- [Network files unchanged](r2-network-identity.json)
- [ALINX image identity](r2-image-identity.md), [source lineage](r2-alinx-source-lineage.json)
- [ALINX single-stream payload comparison](r2-alinx-1x1-identity.json)
- [ALINX eight-stream payload comparison](r2-alinx-8x8-identity.json)
- [All ALINX corner results, both sides](r2-alinx-all-corners.json)
- [Reproduction procedure](r2-reproduction.md), [physical recipe helper](helpers/implement_audio.tcl)
- [Evidence digests](r2-artifact-digests.json); [handoff-file digests](r2-deliverable-digests.json)
- [Resource-budget snapshot](r2-resource-budget.json)
- [Historical fabric-control Arty baseline](r2-arty-baseline.json)
- [Round 1 blockers](blockers.md), superseded by the interval-record and A1:A0 decisions

Failed routes remain failed evidence. Cancelled queued attempts supply no result. Round 1 artifacts and the earlier fabric-control area result remain historical. Cleanup exceptions are disclosed in the handoff. No desk receipt discharges bench acceptance.
