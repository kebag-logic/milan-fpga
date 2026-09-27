# L1-L10 authoritative layer: processor 07 §3.1 at e04234e1 vs parent page at e0920d77

Processor text: `docs/architecture/07_memory_maps.md` at `e04234e115cfdcaace393ae62ba68562d47834c6`, lines 87-117 (ownership introduction), 122-133 (rule table), 135-143 (post-table note).
Parent text: kebag-logic/milan-fpga `docs/reference/PP_DESCRIPTOR_OWNERSHIP.md` at `e0920d77162284d8da52ffaf13a973e451e44f90`
(sha256 of fetched blob `ad9bb61ffcdccb5bced39be2316c7378042785109505dd08af7525e2e26bf6d8`), boundary :23-38, matrix rows :58-68.

## Boundary sentences

| Parent | Processor at e04234e1 | Same split |
|---|---|---|
| :36 "Parent shipping checks are authoritative for generated model content." | :100-105 "Parent shipping checks are authoritative for all generated model content, including every L1–L10 model obligation below: …" | yes |
| :37 "Retained processor semantic checks provide defence in depth." | :105-106 "All processor semantic checks, including those retained or added under #60, provide defence in depth." | yes (extends explicitly to future #60 checks, per manager decision 5854030459) |
| :38 "Generic packer checks remain authoritative for packed-image acceptance." | :106-107 "Generic packer checks remain authoritative for packed-image acceptance, including L2's index density." | yes |
| :31-33 processor retains generic structural duties; allocated duty is not an implemented check | :90-94 processor owns generic packed-image structure and validation; "An ownership assignment is not evidence that every check is implemented." | yes (unchanged from round 1) |
| :39 "Neither layer's passing result proves every rule below." | :108-109 "Neither construction nor byte-exact serving substitutes for a negative validation case." | compatible (unchanged from round 1) |

## Per-rule authoritative layer

| Rule | Parent row (column "Authoritative enforcement and evidence") | Processor §3.1 statement | Stated authoritative layer | Identical |
|---|---|---|---|---|
| L1 | :58 Parent C + T; "No general parent-partition refusal"; F07.2 minimum conflict → PP60, F5 (now milan-fpga#584) | :101-102 "L1 partition and cardinalities (including F07.2's minima)" under parent authority | parent | yes |
| L2 | :59 Processor R (duplicates, index gaps); Parent C/T (multi-level ordering constructed) | :102 "L2 multi-level ordering" under parent; :107 "including L2's index density" under generic packer | ordering: parent; density/duplicates: generic packer | yes (the parent row itself splits L2 the same way) |
| L3 | :60 Parent R/C/T | :102 "L3" under parent | parent | yes |
| L4 | :61 Parent C/T; "Neither parent nor packer generally refuses all L4 violations" | :102 "L4" under parent | parent | yes |
| L5 | :62 Parent C/T; "Processor density is only supporting evidence" | :102 "L5" under parent | parent | yes |
| L6 | :63 Parent C/R/T | :102-103 "L6 clock-source construction and list shape" under parent | parent | yes |
| L7 | :64 Parent R/C | :103 "L7" under parent | parent | yes |
| L8 | :65 Parent C/T | :103 "L8" under parent | parent | yes |
| L9 | :66 Parent C/T | :103 "L9 model identity and evolution" under parent | parent | yes |
| L10 | :67 Parent R/C/T | :103-104 "L10 AUDIO_UNIT rate-list offset, count and length" under parent | parent | yes |
| ADP maxima | :68 Parent C/T | :104-105 "plus ADP stream-count maxima across supported configurations" under parent | parent | yes |

No sentence in the delta or elsewhere in §3.1 (:78-143) states processor authority for a semantic rule. The processor-side
L6/L10 text (:129, :133) states consumer reliance (SET_CLOCK_SOURCE / SET_SAMPLING_RATE preconditions), and :140-143 states
the packer does not enforce L10's semantic checks or L6's identity list; both remain open under #89 (processor, defence in
depth) and the parent matrix's F6, matching parent row :67 "[PP89]/[F6] retain the rest".

Packer-side claims used by this split (density, duplicates, body/key, name binding, line buffer) are re-measured at this head and at
`493e5e4b` by `scripts/probe_packer_claims.py` (unchanged from round 1, sha256 `f5ca7619…c8d5`): 18/18 OK.
