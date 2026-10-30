# Sampling ledger: docs/reference/PP_DESCRIPTOR_OWNERSHIP.md

Every numeric or normative statement, with the mechanical checks and the manual verdict.

| Line | Kind | Statement | Mechanical | Verdict |
|---:|---|---|---|---|
| 3 | sentence | This is the parent contract allocation for [#509][coordination]. | - | ok: #509 CLOSED is the coordination record; F1-F4/F6 enforcement rows 329-334 |
| 3 | sentence | F1-F4 and F6 enforcement reflects the assigned parent follow-ups. | - | ok: #509 CLOSED is the coordination record; F1-F4/F6 enforcement rows 329-334 |
| 8 | sentence | The [assignment decision][decision] settles ownership, not implementation completeness. | - | policy: ownership allocation |
| 8 | sentence | No ownership transfer relies on that unpublished processor change. | - | policy: ownership allocation |
| 24 | sentence | The parent owns shipping-model content and ADP metadata. | path 1 | ok: REQUIREMENTS.md anchor (anchor gate) |
| 24 | sentence | Requirements [REQ-VER-03/04](../../REQUIREMENTS.md#8-verification-and-release-acceptance) remain applicable. | path 1 | ok: REQUIREMENTS.md anchor (anchor gate) |
| 28 | sentence | The parent must validate configuration-dependent semantic obligations. | - | ok: #661 CLOSED adopted the processor lint; gate 36b exists (sampling/ownership-identifiers.txt) |
| 28 | sentence | Since #661 the processor packer's default model lint checks the last two. | - | ok: #661 CLOSED adopted the processor lint; gate 36b exists (sampling/ownership-identifiers.txt) |
| 28 | sentence | Both parent image emitters run it; gate 36b holds each to it. | - | ok: #661 CLOSED adopted the processor lint; gate 36b exists (sampling/ownership-identifiers.txt) |
| 28 | sentence | ADP counts must represent maxima across supported configurations. | - | ok: #661 CLOSED adopted the processor lint; gate 36b exists (sampling/ownership-identifiers.txt) |
| 34 | sentence | An allocated duty does not establish an implemented check. | - | policy: ownership allocation |
| 39 | sentence | Parent shipping checks are authoritative for generated model content. | - | ok: avdecc/aem_descriptors.py D.be32 (identifier check) |
| 39 | sentence | Every parent AEM u32 pack rejects negative or overflowing values. | - | ok: avdecc/aem_descriptors.py D.be32 (identifier check) |
| 39 | sentence | The shared `D.be32` encoder cannot silently truncate these fields. | - | ok: avdecc/aem_descriptors.py D.be32 (identifier check) |
| 39 | sentence | Neither layer's passing result proves every rule below. | - | ok: avdecc/aem_descriptors.py D.be32 (identifier check) |
| 46 | sentence | Five product configurations do not make one five-configuration entity. | - | policy: ownership allocation |
| 62 | sentence | Milan v1.2 Section 5.3.3 requires these descriptor classes. | - | ok: Milan v1.2 5.3.3 descriptor classes |
| 62 | sentence | No configuration input removes them; zero is unreachable. | - | ok: Milan v1.2 5.3.3 descriptor classes |
| 62 | sentence | Therefore no new configuration refusal is needed for these counts. | - | ok: Milan v1.2 5.3.3 descriptor classes |
| 62 | sentence | Its self-test rejects unbound, literal and swapped bindings. | - | ok: Milan v1.2 5.3.3 descriptor classes |
| 72 | sentence | [integration-parameters]: https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/blob/870ff88ad35bbd532244e4c7e6d7661b9f6e1366/docs/guide... | - | ok: processor link (pinned commit) |
| 76 | sentence | Rule labels refer to [processor memory-map section 3.1][memory-map]. | - | policy: ownership allocation |
| 76 | sentence | `C` means construction; it is not a refusal. | - | policy: ownership allocation |
| 76 | sentence | `T` means a test comparison, not a production validator. | - | policy: ownership allocation |
| 86 | row | \| L1: single parent, cardinalities; Milan 5.3.2 \| Parent assembly -> processor descriptor store \| Parent **C**: `A._entity_descriptors`, `_port_descriptor... | issue 2; clause 2 | mech: identifiers exist (sampling/ownership-identifiers.txt); Milan 5.3.2 exists |
| 87 | row | \| L2: dense indices and hierarchy ordering; IEEE 1722.1 7.2 \| Parent directory -> processor index map/store \| Processor **R**: `P._grouped_descriptors` re... | clause 1 | mech: identifiers exist; IEEE 1722.1 7.2 exists |
| 88 | row | \| L3: Base formats, role presence and rate completeness; Milan 5.3.3.4, 6.3/6.4 \| Parent stream declarations -> processor format tables and media fabric \|... | clause 1 | mech: identifiers exist; clauses exist |
| 89 | row | \| L4: buffer floor, CLASS_A, format family, current membership, 46-format cap; Milan 5.3.3.4, IEEE Table 7-8 \| Parent descriptor constructors -> processor ... | issue 2; clause 1 | mech: identifiers exist; #574/#575 CLOSED; IEEE Table 7-8 exists |
| 90 | row | \| L5: stable physical-port index across configurations; Milan 5.3.3.5 \| Parent AVB_INTERFACE -> processor/ADP interface selection \| Parent **C**: `D.d_avb... | clause 1 | mech: identifiers exist |
| 91 | row | \| L6: one INPUT_STREAM per CRF input and per AAF input (#629), in class order INTERNAL, CRF, AAF; INTERNAL with outputs, at least one source per domain, ide... | issue 7; clause 2 | mech: identifiers exist; #629 one INPUT_STREAM per CRF and AAF input matches the audit's CLOCK_SOURCE counts |
| 92 | row | \| L7: dynamic input maps, output uniqueness, mono clusters; Milan 5.3.3.7-.9; IEEE 7.2.19 \| Parent ports/maps/clusters -> processor maps and media crossbar... | issue 1; clause 1 | mech: identifiers exist; #464 CLOSED |
| 93 | row | \| L8: IDENTIFY at one stable index; Milan 5.3.3.10 \| Parent CONTROL/ADP CSR -> processor control lookup \| Parent **C**: `D.d_control_identify`, `A._entity... | clause 1 | mech: identifiers exist; milan_csr.sv ADP_IDX0 |
| 94 | row | \| L9: valid model identity and evolution; Milan 5.3.3.1/5.6.2 validity, 5.3.1 evolution; IEEE 6.2.2.8, Table 7-2 \| Parent model hash/identity join -> ENTIT... | issue 1; clause 1 | mech: identifiers exist |
| 95 | row | \| L10: offset 144, count 1..8, full words, length=144+4N, current-rate membership; IEEE 7.2.3/7.4.21.1; Milan 5.3.3.3 \| Parent AUDIO_UNIT -> processor SET_... | issue 3; clause 1 | ok: audit receipt AUDIO_UNIT rates_offset 144, count 1..3, length 144+4N |
| 96 | row | \| ADP maxima; Milan 5.3.3.1, IEEE Table 7-2 \| Parent `B.adp_shape`/overlay -> generated header, ENTITY bytes and processor ADP \| Parent **C**: common stre... | clause 1 | mech: identifiers exist |
| 109 | row | \| CSR \| [milan_csr.sv](../../hdl/common/csr/milan_csr.sv): ADP_IDX0 reset and IDENTIFY index connection \| | path 1 | ok: hdl/common/csr/milan_csr.sv exists |
| 113 | sentence | All offsets and lengths are decimal bytes. | - | ok: the receipt carries image_offset and stride per row (receipts/sampling/pp-descriptor-audit.json) |
| 113 | sentence | The receipt includes every descriptor's absolute image offset and stride. | - | ok: the receipt carries image_offset and stride per row (receipts/sampling/pp-descriptor-audit.json) |
| 119 | row | \| arty_current \| 32 \| 5792 \| 2 / 1 \| 1 / 1 \| 16 / 1 \| 1 / 2 \| | - | F: D0-050 |
| 120 | row | \| arty_4x4 \| 64 \| 10112 \| 5 / 5 \| 4 / 4 \| 32 / 4 \| 5 / 5 \| | - | F: D0-050 |
| 121 | row | \| arty_8ch \| 96 \| 15360 \| 5 / 5 \| 4 / 4 \| 64 / 4 \| 5 / 5 \| | - | F: D0-050 |
| 122 | row | \| ax7101_1x1_tdm8 \| 41 \| 7352 \| 2 / 2 \| 1 / 1 \| 25 / 0 \| 2 / 2 \| | - | F: D0-050 |
| 123 | row | \| ax7101_8x8 \| 116 \| 18288 \| 9 / 9 \| 8 / 8 \| 72 / 0 \| 9 / 9 \| | - | F: D0-050 |
| 125 | sentence | Every ENTITY is 312 bytes; configurations_count/current_configuration are `1/0`. | - | F: D0-051 (third sentence); first two ok: ENTITY 312 bytes, CONFIGURATION counts at 74, eight entries, length 106 (audit receipt) |
| 125 | sentence | CONFIGURATION uses count offset 74, eight entries, length 106. | - | F: D0-051 (third sentence); first two ok: ENTITY 312 bytes, CONFIGURATION counts at 74, eight entries, length 106 (audit receipt) |
| 125 | sentence | All singleton counts are one; CLOCK_SOURCE count is two. | - | F: D0-051 (third sentence); first two ok: ENTITY 312 bytes, CONFIGURATION counts at 74, eight entries, length 106 (audit receipt) |
| 133 | row | \| arty_current \| 712 \| 144 / 3 / 156 \| 48000, 96000, 192000 \| 3920 \| 76 / 2 / 80 \| | - | F: D0-050 (CLOCK_DOMAIN offset 3920 vs 4008; length 80 vs 82) |
| 134 | row | \| arty_4x4 \| 712 \| 144 / 1 / 148 \| 48000 \| 6768 \| 76 / 2 / 80 \| | - | F: D0-050 |
| 135 | row | \| arty_8ch \| 712 \| 144 / 1 / 148 \| 48000 \| 9968 \| 76 / 2 / 80 \| | - | F: D0-050 |
| 136 | row | \| ax7101_1x1_tdm8 \| 696 \| 144 / 1 / 148 \| 48000 \| 4840 \| 76 / 2 / 80 \| | - | F: D0-050 |
| 137 | row | \| ax7101_8x8 \| 696 \| 144 / 1 / 148 \| 48000 \| 11872 \| 76 / 2 / 80 \| | - | F: D0-050 |
| 139 | sentence | Every rate word has pull=0; current rate is 48000. | - | F: D0-052 (second sentence); the rest ok: CLOCK_SOURCE[1] is INPUT_STREAM at CRF input 1, 4, 4, 1, 8 and each source is 86 bytes (audit receipt) |
| 139 | sentence | Every domain's source list is exactly `[0,1]`. | - | F: D0-052 (second sentence); the rest ok: CLOCK_SOURCE[1] is INPUT_STREAM at CRF input 1, 4, 4, 1, 8 and each source is 86 bytes (audit receipt) |
| 139 | sentence | CLOCK_SOURCE[0] is INTERNAL, located at CLOCK_SOURCE[0]. | - | F: D0-052 (second sentence); the rest ok: CLOCK_SOURCE[1] is INPUT_STREAM at CRF input 1, 4, 4, 1, 8 and each source is 86 bytes (audit receipt) |
| 139 | sentence | CLOCK_SOURCE[1] is INPUT_STREAM, located at the CRF input. | - | F: D0-052 (second sentence); the rest ok: CLOCK_SOURCE[1] is INPUT_STREAM at CRF input 1, 4, 4, 1, 8 and each source is 86 bytes (audit receipt) |
| 139 | sentence | That input index is respectively 1, 4, 4, 1, 8. | - | F: D0-052 (second sentence); the rest ok: CLOCK_SOURCE[1] is INPUT_STREAM at CRF input 1, 4, 4, 1, 8 and each source is 86 bytes (audit receipt) |
| 139 | sentence | Each source descriptor is 86 bytes. | - | F: D0-052 (second sentence); the rest ok: CLOCK_SOURCE[1] is INPUT_STREAM at CRF input 1, 4, 4, 1, 8 and each source is 86 bytes (audit receipt) |
| 148 | row | \| AAF STREAM_INPUT \| Two formats at 138; length 154; redundant_offset=154; R=0; timing=0; flags=0x0003; buffer_length=2126000 \| | - | ok: audit receipt AAF STREAM_INPUT two formats at 138, length 154, flags 0x0003 |
| 149 | row | \| AAF STREAM_OUTPUT \| One format at 138; length 146; redundant_offset=146; R=0; timing=0; flags=0x0002 \| | - | ok: audit receipt AAF STREAM_OUTPUT one format at 138, length 146, flags 0x0002 |
| 150 | row | \| CRF INPUT/OUTPUT \| One format at 138; length 146; flags=0x0003; only `0x041060010000BB80`; no CRF output on arty_current \| | - | ok: audit receipt CRF input length 146, flags 0x0003 |
| 151 | row | \| AVB_INTERFACE \| Index 0; length 102; port_number=1; number_of_controls=0 \| | - | ok: AVB_INTERFACE index 0 (audit receipt) |
| 152 | row | \| CONTROL \| Index 0; length 113; values_offset=104; type=`0x90E0F00000000001`; reset_time=0 \| | - | ok: CONTROL IDENTIFY row (audit receipt) |
| 153 | row | \| AUDIO_CLUSTER \| Length 90; channel_count=1 \| | - | ok: AUDIO_CLUSTER length 90 (audit receipt) |
| 154 | row | \| STREAM_PORT_INPUT/OUTPUT \| Length 20; input maps=0; all base/count pairs decoded in the receipt \| | - | ok: STREAM_PORT rows (audit receipt) |
| 155 | row | \| AUDIO_MAP \| Offset 8; arty_current: 8 rows, length 72; arty_4x4: 4 rows/map, length 40; arty_8ch: 8 rows/map, length 72 \| | - | ok: AUDIO_MAP rows (audit receipt) |
| 157 | sentence | All stream current_format values equal their first listed format. | - | ok: audit receipt: current_format equals the first format; ADP caps 0x4001/0x4801 on arty_current, 0x4801/0x4801 elsewhere; ENTITY capabilities 0x0000C588 in all five |
| 157 | sentence | Listener AAF lists include the 48 kHz family-completing ut entry. | - | ok: audit receipt: current_format equals the first format; ADP caps 0x4001/0x4801 on arty_current, 0x4801/0x4801 elsewhere; ENTITY capabilities 0x0000C588 in all five |
| 157 | sentence | ADP capabilities are `0x4001/0x4801` for arty_current, talker/listener. | - | ok: audit receipt: current_format equals the first format; ADP caps 0x4001/0x4801 on arty_current, 0x4801/0x4801 elsewhere; ENTITY capabilities 0x0000C588 in all five |
| 157 | sentence | Every other configuration uses `0x4801/0x4801`. | - | ok: audit receipt: current_format equals the first format; ADP caps 0x4001/0x4801 on arty_current, 0x4801/0x4801 elsewhere; ENTITY capabilities 0x0000C588 in all five |
| 157 | sentence | ENTITY capabilities are `0x0000C588` in all five images. | - | ok: audit receipt: current_format equals the first format; ADP caps 0x4001/0x4801 on arty_current, 0x4801/0x4801 elsewhere; ENTITY capabilities 0x0000C588 in all five |
| 163 | sentence | The 8x8 inputs own zero clusters, as parent D8 specifies. | issue 1 | ok: #584 owns the 8x8 zero-cluster correction; processor #122 decision cited |
| 163 | sentence | The processor's F07.2 diagram requires a `1..*` minimum. | issue 1 | ok: #584 owns the 8x8 zero-cluster correction; processor #122 decision cited |
| 163 | sentence | The [processor #122 disposition][cluster-decision] retains that Milan 5.3.3.8 requirement. | issue 1 | ok: #584 owns the 8x8 zero-cluster correction; processor #122 decision cited |
| 163 | sentence | Dynamic mapping permits zero maps, not zero clusters. | issue 1 | ok: #584 owns the 8x8 zero-cluster correction; processor #122 decision cited |
| 163 | sentence | The 8x8 input pools violate the requirement. | issue 1 | ok: #584 owns the 8x8 zero-cluster correction; processor #122 decision cited |
| 163 | sentence | Parent [#584][cluster-fix] owns the D8 product correction. | issue 1 | ok: #584 owns the 8x8 zero-cluster correction; processor #122 decision cited |
| 170 | sentence | The shipping `arty_current` image retains six static-map coherence deviations. | - | ok: #464 CLOSED repaired the fixture indices; F8 row 336 owns the policy |
| 170 | sentence | They map channels 2..7 against a stereo output format. | - | ok: #464 CLOSED repaired the fixture indices; F8 row 336 owns the policy |
| 170 | sentence | [#464][selftest] repaired their fixture indices, not their product policy. | - | ok: #464 CLOSED repaired the fixture indices; F8 row 336 owns the policy |
| 170 | sentence | [F8](#follow-up-allocation) owns their remaining product-policy disposition. | - | ok: #464 CLOSED repaired the fixture indices; F8 row 336 owns the policy |
| 170 | sentence | They do not become resolved through this ownership audit. | - | ok: #464 CLOSED repaired the fixture indices; F8 row 336 owns the policy |
| 178 | sentence | Processor acceptance remains distinct from subsequent parent shipping checks. | - | policy |
| 183 | sentence | Parent #577 checks both descriptor-image emitters. | - | ok: #577 CLOSED, #661 CLOSED (processor PR #144); audit receipt AUDIO_UNIT 144/<=8/144+4N, CLOCK_DOMAIN list at 76 |
| 183 | sentence | Both pack through the processor's `build()`, which lints the model by default. | - | ok: #577 CLOSED, #661 CLOSED (processor PR #144); audit receipt AUDIO_UNIT 144/<=8/144+4N, CLOCK_DOMAIN list at 76 |
| 183 | sentence | #661 retired that checker as a duplicate of the processor lint (processor PR #144). | - | ok: #577 CLOSED, #661 CLOSED (processor PR #144); audit receipt AUDIO_UNIT 144/<=8/144+4N, CLOCK_DOMAIN list at 76 |
| 183 | sentence | The ordinary builder CLI emits the overlay, not the image. | - | ok: #577 CLOSED, #661 CLOSED (processor PR #144); audit receipt AUDIO_UNIT 144/<=8/144+4N, CLOCK_DOMAIN list at 76 |
| 183 | sentence | The loader and model constructors supply no expected field values. | - | ok: #577 CLOSED, #661 CLOSED (processor PR #144); audit receipt AUDIO_UNIT 144/<=8/144+4N, CLOCK_DOMAIN list at 76 |
| 183 | sentence | It requires the CLOCK_DOMAIN list at 76, per Table 7-61, as the identity list. | - | ok: #577 CLOSED, #661 CLOSED (processor PR #144); audit receipt AUDIO_UNIT 144/<=8/144+4N, CLOCK_DOMAIN list at 76 |
| 183 | sentence | It requires the AUDIO_UNIT list at 144, at most 8 words, and length `144 + 4N`. | - | ok: #577 CLOSED, #661 CLOSED (processor PR #144); audit receipt AUDIO_UNIT 144/<=8/144+4N, CLOCK_DOMAIN list at 76 |
| 199 | sentence | Builder gate 36b plants faults after successful configuration loading. | - | ok: gate 36b exists in sw/builder/test_builder.py (identifier check) |
| 199 | sentence | Only the overlay-path lookup is substituted. | - | ok: gate 36b exists in sw/builder/test_builder.py (identifier check) |
| 199 | sentence | All five shipping configurations pass without image changes. | - | ok: gate 36b exists in sw/builder/test_builder.py (identifier check) |
| 212 | row | \| Rate offset 143 \| `L10 rate-offset` \| | - | ok: audit receipt L10 rate-offset refusal |
| 213 | row | \| Nine complete rate words, declared count 9 \| `L10 rate-count` \| | - | ok: audit receipt L10 rate-count refusal |
| 214 | row | \| No rate words, declared count 0 \| `L10 rate-empty` \| | - | ok: L10 rate-empty class |
| 217 | row | \| Declared count 2, one complete rate word \| `L10 rate-length` \| | - | ok: audit receipt L10 rate-length refusal |
| 223 | row | \| Source offset 70, or padded list at offset 78 \| `L6 domain-source-offset` \| | - | ok: L6 domain-source-offset class |
| 226 | row | \| Configuration without its CLOCK_DOMAIN, either emitter \| `L1 required-type` \| | - | ok: L1 required-type class |
| 228 | sentence | The image header and index rows are the packer's generic format. | - | policy: format ownership |
| 231 | sentence | The same committed test fails if either emitter switches the lint off. | issue 1 | ok: #478 CLOSED boundary |
| 231 | sentence | These checks preserve #478's separate loader acceptance boundary. | issue 1 | ok: #478 CLOSED boundary |
| 236 | row | \| Parent loader, L3 \| One listener in arty_current \| Empty listener list \| Refused: `needs at least one listener stream` \| | - | ok: audit config_probes L3 refusal text |
| 237 | row | \| Parent loader, L7 \| Dynamic input map \| Set input map_mode to static \| Refused for Milan dynamic-input requirement \| | - | ok: audit config_probes L7 static input map refused |
| 238 | row | \| Parent map validator, L7 \| Distinct output channels can share a cluster \| Repeat output stream/channel with a different cluster \| Refused by `_map_dupl... | - | ok: audit map_probes duplicate output stream channel refused (IEEE 7.2.19) |
| 239 | row | \| Parent loader, L10 \| Eight distinct unsorted entries, current rate last \| Add a distinct ninth entry \| Refused for the eight-entry L10 walk bound \| | - | ok: audit config_probes nine distinct rates refused (walk bound 8) |
| 240 | row | \| Parent loader, L10 \| Distinct entries \| Duplicate 48000 \| Refused for duplicate entries \| | - | ok: audit config_probes duplicate rates refused |
| 241 | row | \| Overlay conversion \| Shipping one/three-rate lists \| The eight-entry loader fixture includes 44100 \| Refused for unsupported sampling rates; not an L10... | - | ok: audit config_probes eight distinct rates: loader accepted, image refused for unsupported rates |
| 242 | row | \| Processor L2 \| Dense metadata indices `[0,1]` \| Change index 1 to 2 \| Refused for density \| | - | ok: audit packer_probes L2 metadata index gap refused |
| 245 | row | \| Processor generic extent \| Opaque descriptor length 576 \| Length 577 \| Refused for line-buffer size \| | - | partial: the 576-byte control is now refused by the lint for another reason (audit packer_probes 'opaque 576-byte row') |
| 246 | row | \| Processor L10 \| Offset/count/length `144/8/176` \| `144/9/180`, offset 143, count/extent mismatch, or one byte short \| Each accepted; no semantic refusa... | - | F: D0-055 |
| 247 | row | \| Processor L6 \| Source list `[0,1]` \| List `[1,0]` \| Accepted; no membership-shape refusal \| | - | F: D0-055 (L6 reversed list is refused at this head) |
| 248 | row | \| Processor L4 \| Buffer 2126000; 46-entry size 506 \| Buffer 2125999; 47-entry size 514 exceeds the 2021 cap \| All accepted; missing semantic refusal rema... | - | F: D0-055 (L4 probes are refused at this head) |
| 249 | row | \| Processor L1/L2/L7/L8/L9/ADP \| Pristine shipping document \| Shared cluster block; mismatched wire type/index; static input map; duplicate output target;... | - | F: D0-055 (L1/L2/L7/L8/L9/ADP probes are refused at this head) |
| 251 | sentence | F7's body/key probes are refused from processor `493e5e4b`. | - | hist: processor 493e5e4b |
| 254 | sentence | The synthetic size boundaries establish only the named structural property. | - | policy |
| 254 | sentence | Their rate/format lists do not establish supported media operation. | - | policy |
| 254 | sentence | No multi-configuration validity or maximum-count refusal is claimed. | - | policy |
| 258 | sentence | These reachable parent YAML probes now demonstrate the F1-F4 refusals: | - | ok: audit config_probes refusals |
| 262 | row | \| L4 \| buffer_length_ns=2125999 \| refused by `_stream_buffer_ns` / not generated (#574) \| | issue 1 | ok: audit config_probes L4 buffer refusal (#574) |
| 263 | row | \| L4 \| CRF word `0x041060010000BB81` \| refused by `_crf_format` / not generated (#575) \| | issue 1 | ok: audit config_probes CRF word refusal (#575) |
| 264 | row | \| L4 \| 47 AAF output format entries \| refused by `_validate_stream_formats` / not generated (#575) \| | issue 1 | ok: audit config_probes 48-format refusal (#575) |
| 265 | row | \| L4 \| AAF output list also contains CRF \| refused by `_validate_stream_formats` / not generated (#575) \| | issue 1 | ok: audit config_probes mixed family refusal (#575) |
| 266 | row | \| L6 \| Sources `[crf]`, default_source=crf, outputs retained \| refused by `_validate_output_clock_sources` / not generated (#576) \| | issue 1 | ok: audit config_probes outputs without INTERNAL refusal (#576) |
| 267 | row | \| L9 \| model_id_pin=0 or all ones \| refused by `_model_id` / not generated (#573) \| | issue 1 | ok: audit config_probes model ID pin refusals (#573) |
| 269 | sentence | These variants are not the five tracked shipping inputs. | - | policy |
| 269 | sentence | The assigned parent follow-ups now refuse them before generation. | - | policy |
| 275 | sentence | The default vendor prefix is `0x001BC5`. | - | ok: model IDs start 0x001BC5 (audit receipt); B._model_id exists |
| 275 | sentence | `_model_id()` now rejects both endpoint values after numeric-width validation. | - | ok: model IDs start 0x001BC5 (audit receipt); B._model_id exists |
| 275 | sentence | Literal, pinned and resolved hash identities share this refusal (#573). | - | ok: model IDs start 0x001BC5 (audit receipt); B._model_id exists |
| 275 | sentence | A pin cannot shadow an invalid literal. | - | ok: model IDs start 0x001BC5 (audit receipt); B._model_id exists |
| 275 | sentence | Quote these values; an optional `0x` prefix and single underscores between digits are accepted. | - | ok: model IDs start 0x001BC5 (audit receipt); B._model_id exists |
| 288 | row | \| arty_current \| `0x001BC50AC1000005` \| pin \| | - | F: D0-053 |
| 289 | row | \| arty_4x4 \| `0x001BC557FC6ABBC8` \| hash \| | - | F: D0-053 |
| 290 | row | \| arty_8ch \| `0x001BC507C86F4172` \| hash \| | - | F: D0-053 |
| 291 | row | \| ax7101_1x1_tdm8 \| `0x001BC5C40236BA0E` \| hash \| | - | F: D0-053 |
| 292 | row | \| ax7101_8x8 \| `0x001BC572F79BC5D1` \| hash \| | - | F: D0-053 |
| 294 | sentence | Builder gate 28 compares packed fields with their declared authorities. | issue 1 | ok: gate 28 exists; #495 OPEN residue |
| 294 | sentence | Its existing loop covers four configurations; this audit decodes all five. | issue 1 | ok: gate 28 exists; #495 OPEN residue |
| 294 | sentence | That additional measurement does not repair its [#495][residue] coverage residue. | issue 1 | ok: gate 28 exists; #495 OPEN residue |
| 302 | sentence | Generator-owned fields do not automatically enter `model_shape()`. | issue 1 | F: D0-054 (byte 6741 and the quoted ID); the residue itself holds (ID unchanged in the probe) |
| 302 | sentence | The audit changes IDENTIFY reset_time from 0 to 3 in memory. | issue 1 | F: D0-054 (byte 6741 and the quoted ID); the residue itself holds (ID unchanged in the probe) |
| 302 | sentence | The audit refuses evidence unless that control changes packed identity. | issue 1 | F: D0-054 (byte 6741 and the quoted ID); the residue itself holds (ID unchanged in the probe) |
| 302 | sentence | On arty_4x4, image byte 6741 changes; the ID remains unchanged. | issue 1 | F: D0-054 (byte 6741 and the quoted ID); the residue itself holds (ID unchanged in the probe) |
| 302 | sentence | The unchanged ID is `0x001BC557FC6ABBC8`, including packed ENTITY bytes. | issue 1 | F: D0-054 (byte 6741 and the quoted ID); the residue itself holds (ID unchanged in the probe) |
| 302 | sentence | This reproduces the existing [#495][residue]/[PP38][pp38] evolution residue. | issue 1 | F: D0-054 (byte 6741 and the quoted ID); the residue itself holds (ID unchanged in the probe) |
| 317 | sentence | It neither restores old behavior nor reopens the reset-time repair. | issue 1 | ok: #495 residue |
| 317 | sentence | Unused tracked ROM snapshot drift also remains with #495. | issue 1 | ok: #495 residue |
| 323 | sentence | Parent issues #573 through #577 implement F1-F4 and F6 below. | issue 1 | ok: #573-#577 CLOSED implement F1-F4/F6; #509 CLOSED holds the record (owner of F8 to confirm, review suggestion S3) |
| 323 | sentence | [#509][coordination] retains the remaining bounded follow-up records. | issue 1 | ok: #573-#577 CLOSED implement F1-F4/F6; #509 CLOSED holds the record (owner of F8 to confirm, review suggestion S3) |
| 329 | row | \| F1 (#573) \| Enforced by `B._model_id` for literal, pinned and resolved hash IDs. Evolution remains with #495 and [PP38][pp38]. \| Declaration tests accep... | issue 2 | mech: identifier exists; #573 CLOSED |
| 330 | row | \| F2 (#574) \| Enforced by `B._stream_buffer_ns` on every listener declaration. Coordinates [PP60][pp60] L4. \| Declaration tests pack 2126000 and 0xFFFFFFF... | issue 1 | mech: identifier exists; #574 CLOSED |
| 331 | row | \| F3 (#575) \| Enforced by `B._validate_stream_formats` and `_crf_format`. Coordinates [PP60][pp60] L3/L4. \| Both directions accept legal families and 46 f... | issue 1 | mech: identifiers exist; #575 CLOSED |
| 332 | row | \| F4 (#576) \| Enforced by `B._validate_output_clock_sources` for every AAF/CRF output. Coordinates [PP60][pp60] L6. \| Declaration tests accept INTERNAL+CR... | issue 1 | mech: identifier exists; #576 CLOSED |
| 333 | row | \| F5 \| [Processor #122][cluster-decision] retains F07.2's Milan 5.3.3.8 minimum. Parent [#584][cluster-fix] owns correcting D8's non-conforming zero-cluste... | issue 3; clause 1 | ok: #584 owner |
| 334 | row | \| F6 (#577) \| Enforced by the processor packer's default model lint ([PP89][pp89], processor PR #144) inside `build()`, which `B._entity_model_image` and `... | issue 4 | mech: identifiers exist; #577 CLOSED |
| 335 | row | \| F7 \| Body/key refusal is enforced by the processor packer at `493e5e4b`, adopted through `16be6768` in #580. This is separate from [PP60][pp60]'s publish... | path 1; issue 1 | ok: processor 493e5e4b adopted through 16be6768 in #580 |
| 336 | row | \| F8 \| Parent static-map product-policy follow-up. Disposition the six shipping arty_current stream-channel width deviations. Record a clause-backed policy... | issue 1 | ok: F8 open allocation (#464 CLOSED for the fixture part) |
| 337 | row | \| Existing L1/L2/L3/L5/L7/L8 debt \| [PP60][pp60], with parent semantic allocation above. Generic metadata/body consistency is allocated separately to F7. P... | - | policy |
| 338 | row | \| Existing ADP debt \| [PP39][pp39]; parent maximum calculation is required before supporting multiple configurations. \| Two unequal configurations; legal ... | - | policy |
| 339 | row | \| Existing evolution and snapshots \| [#495][residue] and [PP38][pp38]; no duplicate repair. \| Generator-only field changes rotate identity; excluded insta... | issue 1 | ok: #495 OPEN |
| 341 | sentence | [#478][rate-bound] owns the landed rate and bench-drift checks. | issue 1 | ok: #478, #464 CLOSED |
| 341 | sentence | [#464][selftest] owns the landed self-test and CI repair. | issue 1 | ok: #478, #464 CLOSED |
| 345 | sentence | [PP82][pp82] contributes only its model-lint/layout coordination subset. | issue 1 | ok: #76 OPEN |
| 345 | sentence | Parent [#76 qualification][qualification] is also outside this audit. | issue 1 | ok: #76 OPEN |
| 351 | sentence | The audit writes one JSON receipt and no build tree. | - | ok: the audit writes one JSON and no build tree (rerun here) |
| 354 | code | ```bash python3 scripts/audit_pp_descriptors.py --output /tmp/pp-descriptor-audit.json python3 sw/builder/test_builder.py python3 avdecc/gen_aem_store.py --s... | command 3 | ok: scripts/audit_pp_descriptors.py --output exists and ran rc 0 (receipts/sampling/audit_pp_descriptors.log) |
| 362 | code | ```bash python3 sw/builder/endstation_builder.py configs/endstation_arty_current.yaml -o /tmp/pp-audit-build python3 avdecc/gen_aem_store.py --overlay /tmp/p... | command 3 | ok: scripts exist (auto) |
| 368 | sentence | Do not request deployment ownership when reproducing the audit. | - | policy |
| 371 | sentence | At this base, #464's repair and docs-check wiring are present. | - | hist: dated self-test record |
| 371 | sentence | The audit ran its self-test successfully: 20 checks, exit status 0. | - | hist: dated self-test record |
| 376 | sentence | [coordination]: https://github.com/kebag-logic/milan-fpga/issues/509 [decision]: https://github.com/kebag-logic/milan-fpga/issues/509#issuecomment-5844867005... | issue 7 | ok: reference links |
| 392 | sentence | [image-boundary-decision]: https://github.com/kebag-logic/milan-fpga/issues/577#issuecomment-5866340517 | issue 1 | ok: reference link |
