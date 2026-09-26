# Processor descriptor ownership and evidence

This is the parent contract allocation for [#509][coordination].
It records measurements at `7eb3b0d4a6987fd2e93ffc3b5be125267df7f53a`.
The processor pin is `990f96526bb89356c963a260ebbdcf2a77e6623a`.

The [assignment decision][decision] settles ownership, not implementation completeness.
Processor contract publication follows independent review in a separate change.
No ownership transfer relies on that unpublished processor change.

## Contents

- **[Ownership boundary](#ownership-boundary)** -- Separate shipping semantics from generic packing obligations.
- **[Rule matrix](#rule-matrix)** -- Name producers, consumers, checks, limits and existing owners.
- **[Five configuration measurements](#five-configuration-measurements)** -- Read actual offsets, counts, lengths and metadata.
- **[Boundary and invalid-change probes](#boundary-and-invalid-change-probes)** -- Distinguish demonstrated refusals from accepted invalid inputs.
- **[Identity reconciliation](#identity-reconciliation)** -- Trace advertised identity and retain generator-owned evolution debt.
- **[Follow-up allocation](#follow-up-allocation)** -- Bound remaining work without changing adjacent acceptance criteria.
- **[Reproduction](#reproduction)** -- Regenerate the evidence without changing deployment ownership.

## Ownership boundary

The parent owns shipping-model content and ADP metadata.
The processor owns the generic packed-image format and consumer.
Requirements [REQ-VER-03/04](../../REQUIREMENTS.md#8-verification-and-release-acceptance) remain applicable.

The parent must validate configuration-dependent semantic obligations.
These include identity evolution, AUDIO_UNIT layout and clock-source shape.
ADP counts must represent maxima across supported configurations.

The processor retains generic structural validation duties.
These include image extents, directory structure and type/index consistency.
An allocated duty does not establish an implemented check.
The matrix identifies existing enforcement and remaining gaps separately.

Parent shipping checks are authoritative for generated model content.
Retained processor semantic checks provide defence in depth.
Generic packer checks remain authoritative for packed-image acceptance.
Neither layer's passing result proves every rule below.

The current parent emits one configuration per image.
It emits one AVB_INTERFACE, CLOCK_DOMAIN and AUDIO_UNIT.
Five product configurations do not make one five-configuration entity.
Cross-configuration claims require separate fixtures and implementation.

## Rule matrix

Rule labels refer to [processor memory-map section 3.1][memory-map].
`C` means construction; it is not a refusal.
`R` means a demonstrated input refusal.
`T` means a test comparison, not a production validator.

Source abbreviations below identify exact files and functions.
The consumer names identify the boundary relying on each rule.

| Rule and clause | Producer -> consumer | Authoritative enforcement and evidence | Supported boundary; open owner |
|---|---|---|---|
| L1: single parent, cardinalities; Milan 5.3.2 | Parent assembly -> processor descriptor store | Parent **C**: `A._entity_descriptors`, `_port_descriptors`, `B.cluster_layout`; **T**: builder gate 6 `test_port_layout_invariants`. No general parent-partition refusal. | Single AUDIO_UNIT/domain; generated contiguous pools. Changed output `base_cluster=0` still packs. F07.2's cluster minimum conflicts with the zero-cluster 8x8 input pools; [PP60][pp60], [F5](#follow-up-allocation). |
| L2: dense indices and hierarchy ordering; IEEE 1722.1 7.2 | Parent directory -> processor index map/store | Processor **R**: `P._grouped_descriptors` rejects duplicates; `P._index_entries` rejects index gaps. Parent **C/T**: `A.two_level_directory`, `check_two_level`, generator self-test. | Density is checked per configuration/type. Parent multi-level ordering is constructed. Packer accepts disagreement between row metadata and wire type/index. Generic gap remains [PP60][pp60]. |
| L3: Base formats, role presence and rate completeness; Milan 5.3.3.4, 6.3/6.4 | Parent stream declarations -> processor format tables and media fabric | Parent **R**: `B._streams` rejects an empty direction. **C**: `B.base_format_complete`; **T**: builder gate 29 `test_milan_base_formats_are_rate_complete`. | One configuration; listener Base-rate family completion. Talkers follow 6.3's separate obligation, not listener-wide family completion. Generic model lint remains [PP60][pp60]; multi-configuration claims untested. |
| L4: buffer floor, CLASS_A, format family, current membership, 47-format cap; Milan 5.3.3.4, IEEE Table 7-8 | Parent descriptor constructors -> processor and media consumers | Parent **C**: `D.d_stream`, `A._entity_descriptors` set CLASS_A, use first format as current, and emit Table 7-8. **T**: gate 29 checks shipped formats. Neither parent nor packer generally refuses all L4 violations. | All shipped inputs use 2,126,000 ns; format lists have one or two entries. Buffer, CRF-word, mixed-list and 48-entry inputs still build. [PP60][pp60], [F2/F3](#follow-up-allocation). |
| L5: stable physical-port index across configurations; Milan 5.3.3.5 | Parent AVB_INTERFACE -> processor/ADP interface selection | Parent **C**: `D.d_avb_interface` emits descriptor index 0. **T**: builder gate 37 checks its physical port_number against the gPTP declaration. Processor density is only supporting evidence. | One physical interface and configuration. Port_number is 1; descriptor index is 0. No cross-configuration mapping refusal is claimed. [PP60][pp60]. |
| L6: source construction and identity list; Milan 5.3.3.6, 7.5; IEEE 7.4.23.1 | Parent source rows/domain -> processor SET_CLOCK_SOURCE range check | Parent **C**: `B._overlay_clock_sources`, `D.d_clock_domain` produce `[0,1]`. **R/T**: `_load_clocking`, gate 33 reject retired AAF-derived sources and CRF without its sink. These do not grade an arbitrary packed list. | INTERNAL plus one CRF input source ships. Reversed packed lists pass; a CRF-only configuration with outputs builds. [PP60][pp60], [PP89][pp89], [F4/F6](#follow-up-allocation). |
| L7: dynamic input maps, output uniqueness, mono clusters; Milan 5.3.3.7-.9; IEEE 7.2.19 | Parent ports/maps/clusters -> processor maps and media crossbars | Parent **R**: `B._streams` rejects static listener maps; `M._map_duplicate_rule` rejects duplicate output stream/channel targets. **C**: `D.d_audio_cluster` fixes channel_count=1. Generator self-test supplies negative controls. | Parent checks map bounds before packing. Packer accepts static input-map fields, duplicate mapping bytes and channel_count=2. Generic semantic coverage remains [PP60][pp60]; repaired self-test belongs to [#464][selftest]. |
| L8: IDENTIFY at one stable index; Milan 5.3.3.10 | Parent CONTROL/ADP CSR -> processor control lookup | Parent **C**: `D.d_control_identify`, `A._entity_descriptors` emit IDENTIFY[0]. `milan_csr.sv` resets ADP_IDX0 to zero; its upper half drives `identify_index_i`. **T**: gate 37 grades reset_time, not general IDENTIFY/CSR consistency. | Single configuration; no general missing/wrong CONTROL refusal. Packer accepts control_type=0. [PP60][pp60]; closed reset-time repair stays closed. |
| L9: valid model identity and evolution; Milan 5.3.1/5.6.2; IEEE 6.2.2.8, Table 7-2 | Parent model hash/identity join -> ENTITY bytes, firmware and ADP inputs | Parent **C**: `B.model_shape`, `derive_model_id`, `J.identity_from_overlay`, `apply_identity`. **T**: gates 8/28 compare hashes and packed identity. `_eui64` checks numeric width only. | Zero/all-ones pins still build; generator-only reset_time changes retain a hash-derived ID. Evolution belongs to [#495][residue]/[PP38][pp38]; validity needs [F1](#follow-up-allocation). |
| L10: offset 144, count <=8, full words, length=144+4N; IEEE 7.2.3/7.4.21.1; Milan 5.3.3.3 | Parent AUDIO_UNIT -> processor SET_SAMPLING_RATE immediate-address walk | Parent **R**: `B._load_clocking` rejects >8 and duplicates; gate 36a proves distinct ninth-entry refusal. **C**: `D.d_audio_unit` emits offset/length. **T**: `test_audio_unit_shipping_rates` checks offset/count/words, not exact length. | Shipped N=1 or 3. Eight-entry loader acceptance does not widen `S.spec_from_overlay`'s 48/96/192 kHz restriction. Packer accepts wrong offset, count/length mismatch and ninth entry. [#478][rate-bound] remains closed; [PP89][pp89]/[F6](#follow-up-allocation) retain the rest. |
| ADP maxima; Milan 5.3.3.1, IEEE Table 7-2 | Parent `B.adp_shape`/overlay -> generated header, ENTITY bytes and processor ADP | Parent **C**: common stream counts feed all three paths. **T**: `scripts/check_entity_shape.py --self-test` and builder gate 28 compare artifacts. `J` bakes the same metadata into ENTITY. | One configuration, so its count is its maximum. Packer accepts incorrect ENTITY counts. No two-configuration maximum calculation/refusal is claimed. [PP39][pp39]; future parent multi-configuration delivery remains a prerequisite. |

| Source | Path and relevant responsibilities |
|---|---|
| B | [endstation_builder.py](../../sw/builder/endstation_builder.py): configuration validation, model identity, overlays and ADP shape |
| D | [aem_descriptors.py](../../avdecc/aem_descriptors.py): descriptor field layouts |
| A | [aem_assemble.py](../../avdecc/aem_assemble.py): descriptor tree, directory and validation tables |
| M | [aem_maps.py](../../avdecc/aem_maps.py): per-port bounds and configuration-wide output uniqueness |
| S | [aem_specs.py](../../avdecc/aem_specs.py): overlay-to-model restrictions |
| J | [gen_aemi_image.py](../../avdecc/gen_aemi_image.py): identity, names and processor packing join |
| P | [pinned processor packer][packer]: `build`, `_grouped_descriptors`, `_index_entries`, `_index_runs`, `_check_name_binding` |
| Tests | [test_builder.py](../../sw/builder/test_builder.py), [gen_aem_store.py](../../avdecc/gen_aem_store.py), [check_entity_shape.py](../../scripts/check_entity_shape.py) |
| CSR | [milan_csr.sv](../../hdl/common/csr/milan_csr.sv): ADP_IDX0 reset and IDENTIFY index connection |

## Five configuration measurements

Names below abbreviate `configs/endstation_<name>.yaml`.
All offsets and lengths are decimal bytes.
The receipt includes every descriptor's absolute image offset and stride.

| Configuration | Descriptors | Image bytes | STREAM_INPUT / OUTPUT | Port input / output | Clusters / static maps | ADP sources / sinks |
|---|---|---|---|---|---|---|
| arty_current | 32 | 5792 | 2 / 1 | 1 / 1 | 16 / 1 | 1 / 2 |
| arty_4x4 | 64 | 10112 | 5 / 5 | 4 / 4 | 32 / 4 | 5 / 5 |
| arty_8ch | 96 | 15360 | 5 / 5 | 4 / 4 | 64 / 4 | 5 / 5 |
| ax7101_1x1_tdm8 | 41 | 7352 | 2 / 2 | 1 / 1 | 25 / 0 | 2 / 2 |
| ax7101_8x8 | 116 | 18288 | 9 / 9 | 8 / 8 | 72 / 0 | 9 / 9 |

Every ENTITY is 312 bytes; configurations_count/current_configuration are `1/0`.
CONFIGURATION uses count offset 74, eight entries, length 106.
Its entries are AUDIO_UNIT, STREAM_INPUT, STREAM_OUTPUT, AVB_INTERFACE,
CLOCK_DOMAIN, CLOCK_SOURCE, CONTROL and LOCALE.
All singleton counts are one; CLOCK_SOURCE count is two.

| Configuration | AUDIO_UNIT image offset | Rate offset / count / length | Rate words, decimal | CLOCK_DOMAIN image offset | Source offset / count / length |
|---|---|---|---|---|---|
| arty_current | 712 | 144 / 3 / 156 | 48000, 96000, 192000 | 3920 | 76 / 2 / 80 |
| arty_4x4 | 712 | 144 / 1 / 148 | 48000 | 6768 | 76 / 2 / 80 |
| arty_8ch | 712 | 144 / 1 / 148 | 48000 | 9968 | 76 / 2 / 80 |
| ax7101_1x1_tdm8 | 696 | 144 / 1 / 148 | 48000 | 4840 | 76 / 2 / 80 |
| ax7101_8x8 | 696 | 144 / 1 / 148 | 48000 | 11872 | 76 / 2 / 80 |

Every rate word has pull=0; current rate is 48000.
Every domain's source list is exactly `[0,1]`.
CLOCK_SOURCE[0] is INTERNAL, located at CLOCK_SOURCE[0].
CLOCK_SOURCE[1] is INPUT_STREAM, located at the CRF input.
That input index is respectively 1, 4, 4, 1, 8.
Each source descriptor is 86 bytes.

| Descriptor class, every configuration | Count/offset/length and other decoded fields |
|---|---|
| AAF STREAM_INPUT | Two formats at 138; length 154; redundant_offset=154; R=0; timing=0; flags=0x0003; buffer_length=2126000 |
| AAF STREAM_OUTPUT | One format at 138; length 146; redundant_offset=146; R=0; timing=0; flags=0x0002 |
| CRF INPUT/OUTPUT | One format at 138; length 146; flags=0x0003; only `0x041060010000BB80`; no CRF output on arty_current |
| AVB_INTERFACE | Index 0; length 102; port_number=1; number_of_controls=0 |
| CONTROL | Index 0; length 113; values_offset=104; type=`0x90E0F00000000001`; reset_time=0 |
| AUDIO_CLUSTER | Length 90; channel_count=1 |
| STREAM_PORT_INPUT/OUTPUT | Length 20; input maps=0; all base/count pairs decoded in the receipt |
| AUDIO_MAP | Offset 8; arty_current: 8 rows, length 72; arty_4x4: 4 rows/map, length 40; arty_8ch: 8 rows/map, length 72 |

All stream current_format values equal their first listed format.
Listener AAF lists include the 48 kHz family-completing ut entry.
ADP capabilities are `0x4001/0x4801` for arty_current, talker/listener.
Every other configuration uses `0x4801/0x4801`.
ENTITY capabilities are `0x0000C588` in all five images.

The 8x8 inputs own zero clusters, as parent D8 specifies.
The processor's F07.2 diagram instead draws a `1..*` minimum.
This audit records that discrepancy without resolving its normative interpretation.
The separate processor contract change must disposition it under PP60.

The compatibility model retains six recorded static-map coherence deviations.
They map channels 2..7 against a stereo output format.
[#464][selftest] repaired their fixture indices, not their product policy.
They do not become resolved through this ownership audit.

## Boundary and invalid-change probes

Each mutation starts from a fresh accepted input.
Packer acceptance also verifies the mutated bytes survive packing.
These experiments measure existing enforcement; they add no shipping validator.

| Layer and rule | Accepted control or boundary | One invalid change | Measured result |
|---|---|---|---|
| Parent loader, L3 | One listener in arty_current | Empty listener list | Refused: `needs at least one listener stream` |
| Parent loader, L7 | Dynamic input map | Set input map_mode to static | Refused for Milan dynamic-input requirement |
| Parent map validator, L7 | Distinct output channels can share a cluster | Repeat output stream/channel with a different cluster | Refused by `_map_duplicate_rule`, IEEE 7.2.19 |
| Parent loader, L10 | Eight distinct unsorted entries, current rate last | Add a distinct ninth entry | Refused for the eight-entry L10 walk bound |
| Parent loader, L10 | Distinct entries | Duplicate 48000 | Refused for duplicate entries |
| Overlay conversion | Shipping one/three-rate lists | The eight-entry loader fixture includes 44100 | Refused for unsupported sampling rates; not an L10 refusal |
| Processor L2 | Dense metadata indices `[0,1]` | Change index 1 to 2 | Refused for density |
| Processor directory | One row per key | Duplicate ENTITY row | Refused for duplicate descriptor |
| Processor name binding | ENTITY name matches name table | Change its first inline name byte | Refused for disagreement with name-table entry |
| Processor generic extent | Opaque descriptor length 576 | Length 577 | Refused for line-buffer size |
| Processor L10 | Offset/count/length `144/8/176` | `144/9/180`, offset 143, count/extent mismatch, or one byte short | Each accepted; no semantic refusal |
| Processor L6 | Source list `[0,1]` | List `[1,0]` | Accepted; no membership-shape refusal |
| Processor L4 | Buffer 2126000; 47-entry size 514 | Buffer 2125999; 48-entry size 522 | Both accepted; 576-byte buffer is not the 47-format cap |
| Processor L1/L2/L7/L8/L9/ADP | Pristine shipping document | Shared cluster block; mismatched wire type/index; static input map; duplicate output target; two-channel cluster; non-IDENTIFY type; invalid ID; wrong counts | Each accepted; see individual receipt rows |

The synthetic size boundaries establish only the named structural property.
Their rate/format lists do not establish supported media operation.
No multi-configuration validity or maximum-count refusal is claimed.

Reachable parent YAML probes also expose missing validation:

| Rule | Single changed input | Loader / generated image |
|---|---|---|
| L4 | buffer_length_ns=2125999 | accepted / accepted |
| L4 | CRF word `0x041060010000BB81` | accepted / accepted |
| L4 | 48 AAF output format entries | accepted / accepted |
| L4 | AAF output list also contains CRF | accepted / accepted |
| L6 | Sources `[crf]`, default_source=crf, outputs retained | accepted / accepted |
| L9 | model_id_pin=0 or all ones | accepted / accepted |

These variants are not the five tracked shipping inputs.
Their acceptance is a product validation gap, not shipping-image conformity.

## Identity reconciliation

`model_shape()` hashes configuration fields with `AEM_LAYOUT_REV`.
The default vendor prefix is `0x001BC5`.
An explicit pin overrides that hash without model-history validation.
`_eui64()` accepts both forbidden endpoint values within its numeric range.

| Configuration | ENTITY entity_model_id | Source |
|---|---|---|
| arty_current | `0x001BC50AC1000005` | pin |
| arty_4x4 | `0x001BC557FC6ABBC8` | hash |
| arty_8ch | `0x001BC507C86F4172` | hash |
| ax7101_1x1_tdm8 | `0x001BC5C40236BA0E` | hash |
| ax7101_8x8 | `0x001BC572F79BC5D1` | hash |

`overlay_adp_block()` derives identity from the same resolved configuration.
`identity_from_overlay()` supplies MODEL_ID and the ADP metadata fields.
`apply_identity()` fills those spans before the processor packs them.
The generated firmware constants program the same identity into ADP.
Builder gate 28 compares packed fields with their declared authorities.
Its existing loop covers four configurations; this audit decodes all five.
That additional measurement does not repair its [#495][residue] coverage residue.

Generator-owned fields do not automatically enter `model_shape()`.
The audit changes IDENTIFY reset_time from 0 to 3 in memory.
On arty_4x4, image byte 6741 changes; the ID remains unchanged.
The unchanged ID is `0x001BC557FC6ABBC8`, including packed ENTITY bytes.
This reproduces the existing [#495][residue]/[PP38][pp38] evolution residue.

| arty_4x4 image | SHA-256 |
|---|---|
| Original | `1b288e13ccbf03410c593a53bc22f4a68e3d289eef8a7f907e63bc98a51415ff` |
| reset_time mutation | `bb036e26ddb773e5b0e59f92dbd2d0eed0ce7793fcca5175cedd657996f50562` |

The mutation is evidence of incomplete identity coverage.
It neither restores old behavior nor reopens the reset-time repair.
Unused tracked ROM snapshot drift also remains with #495.

## Follow-up allocation

The maintainer files newly established parent defects from this list.
Until filing, [#509][coordination] owns these bounded follow-up records.
Existing processor issues retain their published scope and acceptance criteria.

| Record | Owner and bounded remaining work | Required discriminating evidence |
|---|---|---|
| F1 | Parent validity follow-up; coordinate [PP38][pp38]. Refuse zero/all-ones literal and pinned model IDs. Keep model evolution with #495. | Legal ID accepted; both endpoint values refused on both input forms; generated ENTITY/ADP equality retained. |
| F2 | Parent buffer-floor follow-up; coordinate [PP60][pp60] L4. Validate every declared listener buffer. | 2126000 accepted, 2125999 refused; all five images unchanged. |
| F3 | Parent stream-format follow-up; coordinate [PP60][pp60] L3/L4. Bound format count and validate AAF/CRF family and Milan CRF word. | Legal family controls; independently refuse 48 entries, mixed family and altered CRF word; test inputs and outputs. |
| F4 | Parent source-construction follow-up; coordinate [PP60][pp60] L6. Outputs must have INTERNAL available. | INTERNAL+CRF accepted; outputs with only CRF refused; preserve applicable input-only behavior. |
| F5 | Processor contract follow-up under [PP60][pp60]. Reconcile F07.2's minimum with parent D8 zero-cluster input pools. | Public clause-backed disposition; do not infer a requirement waiver from successful packing. |
| F6 | Parent image-check follow-up and [PP89][pp89]. Add discriminating L6 identity-list and L10 offset/count/length checks at the shipping image boundary. Processor retained semantic checks are defence in depth. | Legal one/eight-entry structural boundaries; independently reject offset, count, truncated/extra length and non-identity source lists. Preserve #478's narrower loader scope. |
| Existing L1/L2/L3/L5/L7/L8 debt | [PP60][pp60], with parent semantic allocation above. Generic metadata/body consistency remains processor-owned. Parent construction has no comprehensive negative model lint. | Named minimum/parent/order/Base-format/interface/map/IDENTIFY fixtures; supported configuration boundaries stated explicitly. |
| Existing ADP debt | [PP39][pp39]; parent maximum calculation is required before supporting multiple configurations. | Two unequal configurations; legal maximum accepted; under/overstatement and wrong metadata refused. |
| Existing evolution and snapshots | [#495][residue] and [PP38][pp38]; no duplicate repair. | Generator-only field changes rotate identity; excluded instance fields do not; pins are bound to model content. |

[#478][rate-bound] owns the landed rate and bench-drift checks.
[#464][selftest] owns the landed self-test and CI repair.
Neither issue is extended by this audit.

[PP82][pp82] contributes only its model-lint/layout coordination subset.
Dynamic READ_DESCRIPTOR overlays and oversize responses remain processor work.
Parent [#76 qualification][qualification] is also outside this audit.

## Reproduction

Run from the parent checkout with initialized pinned submodules.
The audit writes one JSON receipt and no build tree.

```bash
python3 scripts/audit_pp_descriptors.py --output /tmp/pp-descriptor-audit.json
python3 sw/builder/test_builder.py
python3 avdecc/gen_aem_store.py --self-test
```

For one configuration, reproduce the two generator CLI boundaries:

```bash
python3 sw/builder/endstation_builder.py configs/endstation_arty_current.yaml -o /tmp/pp-audit-build
python3 avdecc/gen_aem_store.py --overlay /tmp/pp-audit-build/endstation_arty_current/aem_overlay.json --out-dir /tmp/pp-audit-store
python3 avdecc/gen_aemi_image.py --overlay /tmp/pp-audit-build/endstation_arty_current/aem_overlay.json -o /tmp/pp-audit-image.bin -m /tmp/pp-audit-image.map --json /tmp/pp-audit-document.json
```

Substitute each other tracked configuration stem for equivalent evidence.
Do not request deployment ownership when reproducing the audit.

The generator self-test historically failed with stale map fixtures.
At this base, #464's repair and docs-check wiring are present.
The audit ran its self-test successfully: 20 checks, exit status 0.
Builder compiler availability and calibration skips remain explicit evidence limits.

[coordination]: https://github.com/kebag-logic/milan-fpga/issues/509
[decision]: https://github.com/kebag-logic/milan-fpga/issues/509#issuecomment-5844867005
[memory-map]: https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/blob/990f96526bb89356c963a260ebbdcf2a77e6623a/docs/architecture/07_memory_maps.md#31-descriptor-tree
[packer]: https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/blob/990f96526bb89356c963a260ebbdcf2a77e6623a/hdl/aecp/desc/gen_desc_image.py
[pp38]: https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/38
[pp39]: https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/39
[pp60]: https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/60
[pp82]: https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/82
[pp89]: https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/89
[rate-bound]: https://github.com/kebag-logic/milan-fpga/issues/478
[selftest]: https://github.com/kebag-logic/milan-fpga/issues/464
[residue]: https://github.com/kebag-logic/milan-fpga/issues/495
[qualification]: https://github.com/kebag-logic/milan-fpga/issues/76
