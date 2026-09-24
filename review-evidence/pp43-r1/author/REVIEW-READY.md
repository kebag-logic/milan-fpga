[A253] REVIEW READY

Head: `5771578784c77e945980c78faa52f3e54bcf5e2d`
Branch: `43-49-gsi-internal` (local; not pushed).

Implemented #43/#49's internal seam: input failure code/64-bit bridge come from SRP; pbsta/acmpsta come from committed ACMP listener records. Input selectors 5/7 no longer request the integrator. No top-level parameter or port changed.

Evidence:
- All processor CI gates pass; full suite bank: 16,317 checks, zero failures (processor top: 1,876).
- Focused response proof: 416 checks, with real state-machine values, solicited/unsolicited responses, distinct sinks, reset and missing descriptor. All eight retained mutants fail their named checks; golden/restored controls pass.
- Default-shape synthesis delta: +640 LUTs (+2.28%), +784 registers (+2.58%), no block RAM increase.
- All five parent consumer commands return 0 on an isolated copy of parent head `3eaee03f0c50522c4e4da8e12c771ec130a8c2f9` with this processor gitlink staged. Consumer simulation: 371 checks, zero failures.

Exact-checkout limitation: after the prescribed fetch/checkout in `pp94-parent-consumer`, source-list and consumer simulation checks pass, but the C++, Python and HDL gates refuse with rc 2 because its unchanged index pins `2e1675d2`. Their guard requires the indexed gitlink to match the checkout. The designated parent's index and tracked files remain untouched; no parent commits were made. The isolated copy provides the matching-pin evidence without violating that restriction, but does not make those three original-checkout refusals rc 0.

Specification detail: a new BIND_RX immediately enters ACTIVE (Milan 5.5.3.5.3), then reaches PASSIVE after unanswered probes/backoff with no talker (5.5.3.5.29). Tests grade both transitions while preserving the existing state machine.

`HANDOFF.md` and `PR-BODY.md` are complete in the assigned output directory, including field lineage, test/mutant tables, both repositories' gate results and area reports. Review-ready status here identifies the implemented candidate; the exact-checkout pin restriction above still requires resolution for that location to report all gates green.
