# R399-4 pre-read verdict (written before reading any other reviewer's report on PR #133 in this round)

Exact head 99bfd4bc3180bab97d47f63056513fb39eea6a37, tree d8ec1053bf0968ed462d8a419a0cf859c41e9c3c (unchanged since R399-3).

- R399-3 F1 (MINOR, Docs): RESOLVED by the body section "Composed head `99bfd4bc` (manager note, R399-3 F1)".
  - Item 1 names #132's consolidated list plus section 4 (crflic `>= 3` at :953,956, README `[C]` row and "What it cannot show", parent documents).
  - Item 2 scopes the three section-4 claims to `412efeb7` against `c951a9ff`, and names #132's ports, parameters and word 37.
  - Item 3 links comment 5890073527 (16 of 16 rc 0 at dev 79c36963, both lists applied).
  - The body diff from the round-3 revision (09:58:59Z) to now is a pure append of that section. Closing references are exactly #29, #108, #64 and #65.
  - The 14 named parent entries equal #132's consolidated list (12 files) + `sim_crf_licence.cpp` + the gitlink.
- New S2 (SUGGESTION, Docs): `tb/verilator/milan_dp/README.md` at 79c36963 documents the `[AECP]` no-descriptor-memory degrade arm and the restore-walk harness list, both of which #132's list changes. #132's list names no parent document for them, so at adoption both lists' edits meet in that README. This is routed to the pin-adoption lane and does not block.
- R399-3 S1 (SUGGESTION, Tests): retained and non-blocking. It is routed to a processor issue (the manager's routing).
- Lenses: Conformance, RTL, Robustness, Tests and Docs are all CLEAN. Verdict: POSITIVE.
