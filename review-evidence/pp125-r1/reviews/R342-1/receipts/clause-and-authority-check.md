# Clause and authority check (R342-1, exact head 1d249e6e18a91c16a2620904483634548b0414a6)

Only the cited pages were extracted, with `pdftotext -layout -f N -l N` (poppler 26.08.0), into an
unpublished scratch directory. No standard text is published beyond the short citations below.

| Source (sha256 of local copy) | PDF page(s) | Printed page | Clause | Reviewer reading |
|---|---|---|---|---|
| Milan v1.2 consolidated (`6bb902be…3bba8`) | 34 | 27 (printed = PDF − 7) | §5.3.3.8 | "Each Stream Port Input of a Configuration shall contain at least one AUDIO_CLUSTER descriptor." The next sentence states the same for each Stream Port Output. Unconditional per existing port. |
| Milan v1.2 | 34 | 27 | §5.3.3.7, §5.3.3.9 | STREAM_PORT_INPUT has no attached AUDIO_MAP (dynamic input mapping). Nothing there relaxes §5.3.3.8. |
| Milan v1.2 | 32 | 25 | §5.3.3.1 | entity_model_id must be a valid EUI-64 (neither all zeros nor all ones); talker_stream_sources / listener_stream_sinks are maxima among all possible Configurations. |
| Milan v1.2 | 31 | 24 | §5.3.1 | A static-property change is reported with a different Entity Model ID. |
| Milan v1.2 | 35 | 28 | §5.3.3.10 | Primary IDENTIFY CONTROL exists in all Configurations at the same index. |
| IEEE 1722.1-2021 (`ad7b8220…65b9c`) | 81–82 | 81–82 (PDF = printed) | §7.2.13, Table 7-23 | number_of_clusters (offset 12): "The number of clusters within the Port."; number_of_maps (offset 16) is separate. Dynamic-mapping entities "set the number_of_maps field to zero (0)". No text sets or relaxes number_of_clusters for dynamic mapping. |
| IEEE 1722.1-2021 | 50 | 50 | §6.2.2.8 | A structure change needs a new entity_model_id, with a list of excluded fields. The integrator-guide phrase "subject to IEEE 1722.1 §6.2.2.8's exclusions" is correct. |

Conclusion on #122: the standard needs at least one cluster on every STREAM_PORT_INPUT (Milan §5.3.3.8 governs, and
Milan wins over IEEE). number_of_maps=0 for dynamic mapping does not waive this. Dynamic mappings
address cluster offsets, so a port with no cluster gives a dynamic mapping nothing to target. STOP was the right call.
F07.2 `1..*` is correct and the parent fix stays with kebag-logic/milan-fpga#584 (open).

## Parent ownership page, kebag-logic/milan-fpga@e0920d77 `docs/reference/PP_DESCRIPTOR_OWNERSHIP.md`

sha256 `ad9bb61ffcdccb5bced39be2316c7378042785109505dd08af7525e2e26bf6d8` (fetched read-only through the API).

| Parent line | Parent statement | PR #126 §3.1 at 07_memory_maps.md | Match |
|---|---|---|---|
| :23 | Parent owns shipping-model content and ADP metadata | :86 "The consuming product owns its shipping-model semantics" | yes |
| :24, :31-32 | Processor owns generic packed-image format; image extents, directory structure, type/index consistency | :89-92 | yes |
| :27-29 | Parent must validate configuration-dependent obligations; "These include" identity evolution, AUDIO_UNIT layout, clock-source shape; ADP maxima | :99-102 (enumerated after a colon) | yes, but now reads as an exhaustive list |
| :33 | Allocated duty does not establish an implemented check | :92-93 | yes |
| :36 | "Parent shipping checks are authoritative for generated model content." | :99 narrows this to the four enumerated classes | **no, narrower (finding R342-1-F1)** |
| :37 | Retained processor semantic checks are defence in depth | :102-103 (only "for the same semantic constraints", meaning the four) | partial |
| :38 | Generic packer checks remain authoritative for packed-image acceptance | :89-92 (ownership only; "authoritative" not stated) | implied |
| :58-65, :244 | L1/L3/L4/L5/L7/L8: parent construction/refusals, follow-ups F2/F3/F4, "PP60, with parent semantic allocation above" | no authority stated for these rules; #60 listed as "(model-rule coverage)" | **gap (R342-1-F1)** |
| :67, :156-158 | Loader ≤8 distinct entries; conversion 48/96/192 kHz only; shipped N=1 or 3; one configuration per image | :131-135 | yes |
| :134-137 | D8 zero-cluster 8x8 inputs vs F07.2 `1..*`, to be dispositioned under PP60 | :78-84 | yes (dispositioned) |
| :241 (F6), :242 (F7) | L6/L10 image checks open (PP89/F6); body/key refusal needed (F7) | :96-97 (F7 now enforced at 493e5e4b), :135-137 (L6/L10 open under #89/F6) | yes, updated correctly |

Processor issue scopes fetched read-only: #38 open (L9 validity/evolution), #39 open (ADP maxima), #60 open
("Entity-model lint L1-L8 ... does not exist: add it to gen_desc_image.py or re-scope"), #89 open (packer L10 and L6
refusals, acceptance items 1-2), #584 (parent) open.
