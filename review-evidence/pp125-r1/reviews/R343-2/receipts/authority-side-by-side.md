# L1-L10 authority: processor 07 section 3.1 at e04234e1 vs parent PP_DESCRIPTOR_OWNERSHIP.md at e0920d77

Parent page fetched read-only at `e0920d77162284d8da52ffaf13a973e451e44f90`
(git blob `ba9674d4b6c780e9358089910f0737218dcc61b5`, 25970 bytes).
Processor text: `docs/architecture/07_memory_maps.md:90-117` and `:135-143` at `e04234e1`.

## Split statement

| Parent `:36-38` | Processor `07:100-107` |
|---|---|
| "Parent shipping checks are authoritative for generated model content." | "Parent shipping checks are authoritative for all generated model content, including every L1-L10 model obligation below: ..." (`:100-105`) |
| "Retained processor semantic checks provide defence in depth." | "All processor semantic checks, including those retained or added under #60, provide defence in depth." (`:105-106`) |
| "Generic packer checks remain authoritative for packed-image acceptance." | "Generic packer checks remain authoritative for packed-image acceptance, including L2's index density." (`:106-107`) |
| `:39` "Neither layer's passing result proves every rule below." | `:93-94` "An ownership assignment is not evidence that every check is implemented."; `:108-109` "Neither construction nor byte-exact serving substitutes for a negative validation case." |

## Per rule

| Rule | Parent row (`:58-68`), authoritative column | Processor stated layer (`07:100-107`) | Same? |
|---|---|---|---|
| L1 | `:58` Parent C/T; no processor check named | Parent: "L1 partition and cardinalities (including F07.2's minima)" | yes |
| L2 ordering | `:59` Parent C/T: `two_level_directory`, `check_two_level` | Parent: "L2 multi-level ordering" | yes |
| L2 density | `:59` Processor R: `_grouped_descriptors` duplicates, `_index_entries` gaps | Generic packer: "including L2's index density"; `:90-92` processor owns dense indices | yes |
| L3 | `:60` Parent R/C/T | Parent: "L3" | yes |
| L4 | `:61` Parent C/T | Parent: "L4" | yes |
| L5 | `:62` Parent C/T; "Processor density is only supporting evidence" | Parent: "L5" | yes |
| L6 | `:63` Parent C, R/T | Parent: "L6 clock-source construction and list shape" | yes |
| L7 | `:64` Parent R/C | Parent: "L7" | yes |
| L8 | `:65` Parent C/T | Parent: "L8" | yes |
| L9 | `:66` Parent C/T | Parent: "L9 model identity and evolution" | yes |
| L10 | `:67` Parent R/C/T | Parent: "L10 AUDIO_UNIT rate-list offset, count and length" | yes |
| ADP maxima | `:68` Parent C/T | Parent: "plus ADP stream-count maxima across supported configurations" | yes |

No L1-L10 obligation is left without a stated layer, none is given two layers, and the
processor is stated authoritative for no semantic rule. The only processor-authoritative
items are the generic packed-image checks (`07:90-98`, `:107`), matching parent `:31-32`
and `:38`.

Parent-page staleness noted, not a processor defect: parent `:59` still says the packer
accepts body/key disagreement (F7). Processor `07:97-98` states the `493e5e4b` refusal;
`receipts/packer-claims-probe.log` measures it.
