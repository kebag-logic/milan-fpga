[R519] NEGATIVE - exact head c4539ff107a6a4c7d2e4a4844182b00a2bf33c82

Independent verdict and ledger written before consulting another reviewer's report or findings in this round.

R519-2-F1 remains MINOR, Conformance / Tests / Docs. The published final record now contains inputs_sha256 24ba6a244a83a0b764e6de5131a9c94752135f01ecab5afad83258c7b4767be1. Independent recovery and hashing cover 117 of 121 direct recipe inputs, including all 46 processor sources at this head. Four input bytes remain absent: two external RAM helpers, the external CPU netlist and the generated integrated top. The aggregate digest cannot be recomputed; no mismatch is asserted. Reproduced processor ROM digests, numeric parameters, generic ordering, clock and published figures do not replace those missing components.

The final record and companion summary agree on +3.337 ns, maximum 16 levels and zero pairs above 20. The cone transcript explicitly exposes the traversal now, with 187 cells, 561 pins, 328 startpoints and 17,990 pairs. Retained S1 is narrowed: complete pin/pair artifacts remain absent, while the traversal commands can now be inspected. S2 remains a nonblocking coverage suggestion at this unchanged source head.

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN | Frozen issue/merge assignments, 50 MHz recipe, exact-head input and parameter audit; F1 | R519-3 F1; R519-2 unchanged source conclusions | c4539ff107a6a4c7d2e4a4844182b00a2bf33c82 |
| RTL | CLEAN | Pairwise selection, withdraw stage and all three readers, merged notification owner/counter state, exact source identities | R519-3 independent inspection; R519-2 executed coverage | c4539ff107a6a4c7d2e4a4844182b00a2bf33c82 |
| Robustness | CLEAN | Reset, cancellation versus serializer acceptance, queued cancellation and settle interaction; S1/S2 retained as suggestions | R519-3 inspection; R519-2 functional/fault coverage | c4539ff107a6a4c7d2e4a4844182b00a2bf33c82 |
| Tests | UNCLEAN | Digest recovery script, image regeneration, parameter/chparam checks, histogram and rc reconciliation; F1 | R519-3 measurement audit; R519-2 suites/campaign | c4539ff107a6a4c7d2e4a4844182b00a2bf33c82 |
| Docs | UNCLEAN | Withdrawal contract, WD/CX/CA4 explanations, record provenance, addendum and normalized recipes; F1 | R519-3 evidence review; R519-2 documentation execution | c4539ff107a6a4c7d2e4a4844182b00a2bf33c82 |

No source edits or new hardware claims. The packet is an evidence re-review, not a new full-bank execution.
