# [A496] Lane C8 (descriptor model lint) handoff

Repository: Mister-M-alt/protocol-processor-control-plane-avb-milan, branch
`c8-descriptor-lint` from `main` 03c842a7. Issues #38, #39, #60, #89.
Assignment: issue #60 comment 5948562638. Ruling on the design STOP: issue
#60 comment 5948872196. Reviewers: [R434] internal, [R435] external.

Head: `e6cca1ff0114f10ea1a5d402d4aa7f45f2c986df` (three commits on 03c842a7,
not pushed).

## Status

- 2026-10-02 10:55 CEST: TAKEN on #60 (comment 5948577086).
- 2026-10-02: STOP at the design on #60 (comment 5948825547), head 03c842a7.
- 2026-10-02 11:12 CEST: resumed under the ruling (comment 5948872196).
- 11:47 CEST: three lane commits, head e6cca1f.
- 12:13 CEST: `./scripts/run_suites.sh` rc 0 at e6cca1f.
- Parent adoption patch written. Parent consumer set and the parent models
  run at dev cdf49d1a, and the parent models at PR #634's head; results
  below.
- 13:56 CEST: every gate run; HANDOFF and PR-BODY written.
- REVIEW READY posted on #60 with head e6cca1f (comment 5951843868). The lane
  stops here.

## Design, as ruled

- **Where the lint runs.** `hdl/aecp/desc/model_lint.py` (the API: `lint()`,
  waivers, report, digest) with the rules in `hdl/aecp/desc/model_rules.py`.
  - `gen_desc_image.build()` calls it by default. It runs after the existing
    layout checks, which keep their order and text, and before the image is
    rendered.
  - It judges the grouped bodies `_grouped_descriptors()` builds, so the
    bytes it judges are the bytes packed.
  - It reads IEEE 1722.1-2021 §7.2 wire offsets and every variable part
    through the descriptor's own offset field.
- **Opt-out.** `build(..., lint=False)` and `--no-lint`, for layout vectors
  and deliberate negatives that another checker must name. The report ends
  with `semantic lint: off`, or `semantic lint: off (N lint waivers not
  evaluated)` when the document carries waivers.
  - `adp` or `model_ids` given with the lint off is refused, because the
    caller asked for a check it switched off.
- **Refusal.** `ImageError` with one line per finding:
  `<rule> <check>: cfg C TYPE I: <detail> (<clause>)`. Waiver errors come
  first, then the findings, then stale waivers. The CLI prints
  `gen_desc_image: <text>`, exits 1 and writes no file. The parent's three
  callers (`avdecc/gen_aemi_image.py`, `endstation_builder._entity_model_image`,
  `milan_soc.build_desc_image`) see the same `ImageError`.
- **Waivers** (ruling item 2). Key `lint_waivers` of the document `build()`
  consumes: `{rule, check, configuration, type, first, last, reason}`.
  - A waiver names one check, never a rule. `first`/`last` give an
    inclusive index range; a configuration-level check takes neither.
  - The reason must name a tracking issue (`repo#N`).
  - Refused when malformed (unknown or missing key, unknown check, rule not
    the check's rule, no issue reference, one of first/last, empty range,
    unknown type).
  - Refused when stale: any descriptor of its scope missing, or passing the
    check (`lint waiver N (...) is stale: ...; remove or narrow it`).
  - The report lists every applied waiver:
    `  waiver L1 port-cluster-minimum: cfg 0 STREAM_PORT_INPUT 0..7: 8 finding(s) waived; reason: ...`.
- **Report** (lint on): `semantic lint: on (07 §3.1 rules L1 to L11)`, the
  applied waivers, the four ADP input values the model requires, and
  `model digest sha256 <hex> (IEEE 1722.1-2021 §6.2.2.8[, recorded digest checked])`.
- **ADP report and check** (#38 item 2, #39 item 2). The report prints
  `entity_model_id_i`, `talker_sources_i`, `listener_sinks_i` and
  `identify_index_i`. `build(adp={...})` and `--adp-*` refuse a driven value
  that differs.
  - No generated constant replaces an input; no port, parameter or register
    changes.
- **Digest** (#38 item 3). SHA-256 over every descriptor in (configuration,
  type, index) order, each keyed and length-prefixed.
  - Zeroed: the IEEE 1722.1-2021 §6.2.2.8 exclusions (object_name; ENTITY
    available_index, association_id, entity_name, firmware_version,
    group_name, serial_number, current_configuration; AUDIO_UNIT
    current_sampling_rate; STREAM current_format; CLOCK_SOURCE identifier
    and flags; CLOCK_DOMAIN clock_source_index; AVB_INTERFACE mac_address
    to log_pdelay_interval; CONTROL linear current values, and the whole
    value_details of other value types).
  - Also zeroed: entity_id and entity_model_id.
  - Recorded in `hdl/aecp/desc/model_ids.json` for this repository's models
    only. The parent records nothing.
- **Models** (ruling item 3).
  - `hdl/aecp/desc/milan_min.json` is new: the minimal Milan model and the
    positive case, recorded in `model_ids.json`.
  - `example_milan_8.json` keeps its NOT A COMPLIANCE REFERENCE label and
    gains one line ("The semantic lint (model_lint.py) is off for it: pack
    with --no-lint."). Its descriptors are unchanged. `tb/desc_store` packs
    it with `--no-lint`.
  - The pp_top fixture is built in C++ and does not change. Its README
    states that it is not a Milan model.

## Items

### 1. #89: L10 and L6's clock_sources list

- Rule L10: AUDIO_UNIT `sampling_rates_offset` = 144, `sampling_rates_count`
  in 1..8, length `144 + 4 × count`, `current_sampling_rate` a listed word
  (pull field included). Clauses: IEEE 1722.1-2021 §7.2.3, §7.4.21.1;
  Milan v1.2 §5.3.3.3; 07 §3.1 L10.
- Rule L6 (list): CLOCK_DOMAIN `clock_sources_offset` 76, count ≥ 1, length
  `76 + 2 × count`, list = 0..count-1, every entry an existing CLOCK_SOURCE.
  Clauses: IEEE 1722.1-2021 §7.2.32, §7.4.23.1; Milan v1.2 §5.3.3.6;
  06 §6.4.
- Files: `hdl/aecp/desc/model_rules.py` (`_rule_rates`, `_rule_domains`),
  `model_lint.py`, `gen_desc_image.py` (`build`, CLI),
  `tb/desc_store/lint_mutations.py`, `tb/desc_store/test_gen_desc_image.py`.

| Rule | Check | Negative case (one named mutation of `milan_min.json`) | Refusal text (the check's line) |
|---|---|---|---|
| L6 | `domain-source-offset` | clock_sources_offset 78 | `L6 domain-source-offset: cfg 0 CLOCK_DOMAIN 0: clock_sources_offset 78; SET_CLOCK_SOURCE reads the list at 76 (IEEE 1722.1-2021 §7.2.32; 06 §6.4)` |
| L6 | `domain-source-count` | no clock source in the domain | `L6 domain-source-count: cfg 0 CLOCK_DOMAIN 0: clock_sources_count 0 (Milan v1.2 §5.3.3.6)` |
| L6 | `domain-source-length` | domain one word too long | `L6 domain-source-length: cfg 0 CLOCK_DOMAIN 0: is 82 bytes; 2 sources make 80 (IEEE 1722.1-2021 §7.2.32)` |
| L6 | `domain-source-identity` | clock_sources [1, 0] | `L6 domain-source-identity: cfg 0 CLOCK_DOMAIN 0: clock_sources [1, 0], not 0..1; the SET_CLOCK_SOURCE range check is the membership test only for the identity list (IEEE 1722.1-2021 §7.4.23.1; 06 §6.4)` |
| L6 | `domain-source-exists` | domain names CLOCK_SOURCE 2 | `L6 domain-source-exists: cfg 0 CLOCK_DOMAIN 0: names CLOCK_SOURCE 2, which does not exist (IEEE 1722.1-2021 §7.2.32)` |
| L10 | `rate-offset` | sampling_rates_offset 143 | `L10 rate-offset: cfg 0 AUDIO_UNIT 0: sampling_rates_offset 143; SET_SAMPLING_RATE reads the list at 144 (IEEE 1722.1-2021 §7.2.3, §7.4.21.1; 07 §3.1)` (+1 more) |
| L10 | `rate-count` | nine sampling rates | `L10 rate-count: cfg 0 AUDIO_UNIT 0: sampling_rates_count 9; SET_SAMPLING_RATE consults the first 8 (07 §3.1 L10)` |
| L10 | `rate-empty` | no sampling rate | `L10 rate-empty: cfg 0 AUDIO_UNIT 0: sampling_rates_count 0 (Milan v1.2 §5.3.3.3)` |
| L10 | `rate-length` | one word past the rate list | `L10 rate-length: cfg 0 AUDIO_UNIT 0: is 152 bytes; 1 rates make 148 (IEEE 1722.1-2021 §7.2.3; 07 §3.1)` |
| L10 | `current-rate` | current_sampling_rate 96000 | `L10 current-rate: cfg 0 AUDIO_UNIT 0: current_sampling_rate 0x00017700 is not one of 0x0000BB80 (Milan v1.2 §5.3.3.3)` |

### 2. #38: L9, the driven entity_model_id, the model digest

- Rule L9: entity_model_id neither 0 nor all ones; equal to the driven
  `entity_model_id_i` when given; with `model_ids`, recorded, and with its
  recorded digest. Clauses: Milan v1.2 §5.3.1, §5.3.3.1, §5.6.2;
  IEEE 1722.1-2021 §6.2.2.8, §7.2.1.
- Files: `model_rules.py` (`rule_identity`), `model_lint.py`
  (`model_digest`, `_structural`), `model_ids.json`, `gen_desc_image.py`
  (`--model-ids`, `--adp-entity-model-id`), the gate (`IdentityTest`), and
  `docs/guides/integrator.md` §6 (#38 item 4).

| Rule | Check | Negative case (one named mutation of `milan_min.json`) | Refusal text (the check's line) |
|---|---|---|---|
| L9 | `model-id-valid` | entity_model_id 0 | `L9 model-id-valid: cfg 0 ENTITY 0: entity_model_id 0x0000000000000000 is not a valid EUI-64 (Milan v1.2 §5.3.3.1, §5.6.2)` |
| L9 | `model-id-valid` | entity_model_id all ones | `L9 model-id-valid: cfg 0 ENTITY 0: entity_model_id 0xFFFFFFFFFFFFFFFF is not a valid EUI-64 (Milan v1.2 §5.3.3.1, §5.6.2)` |
| L9 | `model-id-driven` | entity_model_id_i differs (adp) | `L9 model-id-driven: cfg 0 ENTITY 0: entity_model_id_i 0x020000FFFE00C802; the ENTITY carries 0x020000FFFE00C801 (Milan v1.2 §5.6.2; IEEE 1722.1-2021 §7.2.1)` |
| L9 | `model-id-recorded` | an unrecorded entity_model_id (model_ids) | `L9 model-id-recorded: cfg 0 ENTITY 0: entity_model_id 0x020000FFFE00C802 has no recorded digest; record 6d7982fbd1657a88838ff40bbe0746eaa8600e5be7bebae670e1de0c6f46ae20 (IEEE 1722.1-2021 §6.2.2.8)` |
| L9 | `model-digest` | buffer_length edited under the recorded id (model_ids) | `L9 model-digest: cfg 0 ENTITY 0: digest 951babef1e36cbfed1b1053a0b53bbc579e231ce9d34fd9ba45a95ff7f6baa3f differs from the 6d7982fbd1657a88838ff40bbe0746eaa8600e5be7bebae670e1de0c6f46ae20 recorded for 0x020000FFFE00C801: the structure changed and the id did not (Milan v1.2 §5.3.1; IEEE 1722.1-2021 §6.2.2.8)` |

### 3. #39: stream-count maxima, the reported values, integrator.md §6

- Rule L11 (new row of 07 §3.1): ENTITY `talker_stream_sources` and
  `listener_stream_sinks` are the most STREAM_OUTPUTs and STREAM_INPUTs of
  any configuration, and equal the driven `talker_sources_i` and
  `listener_sinks_i` when given. Clauses: Milan v1.2 §5.3.3.1, §5.6.2.
- The second L11 mutation is the two-configuration negative image #39 asks
  for: configuration 1 has two Stream Outputs and the ENTITY says one.
- Files: `model_rules.py` (`_rule_counts`), `gen_desc_image.py`
  (`--adp-talker-sources`, `--adp-listener-sinks`), the gate, and
  `docs/guides/integrator.md` §6.

| Rule | Check | Negative case (one named mutation of `milan_min.json`) | Refusal text (the check's line) |
|---|---|---|---|
| L11 | `talker-sources` | talker_stream_sources 2 | `L11 talker-sources: cfg 0 ENTITY 0: talker_stream_sources 2; the most STREAM_OUTPUTs of any configuration is 1 (Milan v1.2 §5.3.3.1)` |
| L11 | `talker-sources` | configuration 1 has two talkers | `L11 talker-sources: cfg 0 ENTITY 0: talker_stream_sources 1; the most STREAM_OUTPUTs of any configuration is 2 (Milan v1.2 §5.3.3.1)` |
| L11 | `listener-sinks` | listener_stream_sinks 1 | `L11 listener-sinks: cfg 0 ENTITY 0: listener_stream_sinks 1; the most STREAM_INPUTs of any configuration is 2 (Milan v1.2 §5.3.3.1)` |
| L11 | `talker-sources-driven` | talker_sources_i 2 (adp) | `L11 talker-sources-driven: cfg 0 ENTITY 0: talker_sources_i 2; the most STREAM_OUTPUTs of any configuration is 1 (Milan v1.2 §5.3.3.1, §5.6.2)` |
| L11 | `listener-sinks-driven` | listener_sinks_i 3 (adp) | `L11 listener-sinks-driven: cfg 0 ENTITY 0: listener_sinks_i 3; the most STREAM_INPUTs of any configuration is 2 (Milan v1.2 §5.3.3.1, §5.6.2)` |

### 4. #60: L1 to L8 with the cardinalities

- L1: one parent, and the F07.2 / Milan v1.2 §5.3.2 cardinalities:
  - exactly one ENTITY, in configuration 0 (§5.3.3.1; IEEE §7.4.5.2);
  - ENTITY configurations_count and current_configuration (IEEE §7.2.1);
  - one CONFIGURATION per configuration in configuration 0, with
    descriptor_counts equal to the top-level counts (IEEE §7.2.2);
  - per configuration an AVB_INTERFACE, a CLOCK_DOMAIN and a CLOCK_SOURCE
    (§5.3.2, §5.3.3.5, §5.3.3.6, §5.3.3.11);
  - an AUDIO_UNIT, and a Stream Port of the stream's direction, where a
    stream carries AAF (§5.3.3.3, §5.3.3.7);
  - at least one AUDIO_CLUSTER per Stream Port (§5.3.3.8);
  - child ranges naming existing descriptors, no descriptor with two
    parents, and every Stream Port, AUDIO_CLUSTER and AUDIO_MAP with one.
- L2: dense indices (the packer's existing refusal), and child ranges in
  the order IEEE 1722.1-2021 §7.2 walks the hierarchy, configuration-level
  CONTROLs first.
- L3: Milan v1.2 §5.3.3.4, §6.3, §6.4, §7.3.
  - At least one stream per configuration.
  - A Talker (any Stream Output not carrying only CRF) has a Base-format
    Stream Output in some configuration; a Listener likewise has a
    Base-format Stream Input.
  - Every Base channel count at each Base rate an input lists.
  - One set of Base rates per configuration.
  - A CRF stream lists 0x041060010000BB80.
- L4: Milan v1.2 §5.3.3.4; IEEE 1722.1-2021 §7.2, Table 7-8.
  - buffer_length ≥ 2 126 000 ns; CLASS_A set.
  - No CRF and AAF mix; current_format in the list (an `ut` entry covers the
    channel counts up to its own).
  - number_of_formats ≤ 46 (#60 comment 5854263065).
  - The Table 7-8 layout with no redundancy tail (REQ-MDL-003).
- L5: the AVB_INTERFACE index-to-port_number map is the same in every
  configuration (Milan v1.2 §5.3.3.5).
- L6 (construction), Milan v1.2 §5.3.3.6 and §7.5:
  - exactly one INPUT_STREAM source per CRF input, or, with no CRF input,
    exactly one at an AAF input;
  - an INTERNAL source where outputs exist;
  - a gPTP media clock source (EXTERNAL at TIMING) only with a single
    AVB_INTERFACE.
- L7: no AUDIO_MAP on a Stream Port Input; at most one static mapping per
  output stream channel; AUDIO_CLUSTER channel_count 1 (Milan v1.2 §5.3.3.7
  to §5.3.3.9).
- L8: an IDENTIFY CONTROL at one index in every configuration, and the
  driven `identify_index_i` names it when given (Milan v1.2 §5.3.3.10,
  §5.6.2).
  - The ADPDU always sets AEM_IDENTIFY_CONTROL_INDEX_VALID (F04.6), so a
    model without one is refused.
- The packer's existing refusals each gained one negative case
  (`LayoutRefusalTest`, #60 item 3):
  - index gap: `cfg 0 type 0x0014 indices are not dense from 0: [0, 1, 2, 4] (07 §3.1 rule L2)`;
  - duplicate: `duplicate descriptor cfg 0 type 0x0014 index 0`;
  - mixed names: `cfg 0 type 0x0014 mixes named and unnamed descriptors in one index run`;
  - ENTITY index 1: `cfg 0 ENTITY must contain only index 0`;
  - configuration gap: `configuration indices are not dense from 0`.
- Not linted (07 §3.1 says so):
  - the formats a statically mapped output may list (§5.3.3.4);
  - interface_flags and entity_capabilities bits (§5.3.3.5, §5.3.3.1);
  - the CRF input/output obligations of Milan §7.2.2 and §7.2.3;
  - whether a rate list matches what the Audio Unit does (§5.3.3.3).
- Files: `model_rules.py` (`_rule_entity`, `_descriptor_counts`,
  `_rule_tree`, `_rule_order`, `_rule_streams`, `_rule_stream_fields`,
  `_stream_layout`, `_rule_interfaces`, `_rule_sources`, `_rule_maps`,
  `_rule_identify`, the survey), the gate.

| Rule | Check | Negative case (one named mutation of `milan_min.json`) | Refusal text (the check's line) |
|---|---|---|---|
| L1 | `entity-count` | no ENTITY | `L1 entity-count: cfg 0 ENTITY: the model has no ENTITY descriptor (Milan v1.2 §5.3.3.1; IEEE 1722.1-2021 §7.4.5.2)` |
| L1 | `configurations-count` | configurations_count 2 | `L1 configurations-count: cfg 0 ENTITY 0: configurations_count 2; the image has 1 configurations (IEEE 1722.1-2021 §7.2.1)` |
| L1 | `current-configuration` | current_configuration 1 | `L1 current-configuration: cfg 0 ENTITY 0: current_configuration 1 is not below configurations_count 1 (IEEE 1722.1-2021 §7.2.1)` |
| L1 | `configuration-descriptors` | no CONFIGURATION | `L1 configuration-descriptors: cfg 0 CONFIGURATION: CONFIGURATION indices [] for configurations [0] (Milan v1.2 §5.3.2; IEEE 1722.1-2021 §7.2.2, §7.4.5.2)` |
| L1 | `descriptor-counts` | descriptor_counts says 3 STREAM_INPUTs | `L1 descriptor-counts: cfg 0 CONFIGURATION 0: STREAM_INPUT 3; configuration 0 holds 2 at the top level (IEEE 1722.1-2021 §7.2.2)` |
| L1 | `required-type` | no AVB_INTERFACE | `L1 required-type: cfg 0 AVB_INTERFACE: configuration 0 has no AVB_INTERFACE (Milan v1.2 §5.3.2, §5.3.3.5, §5.3.3.6, §5.3.3.11)` (+1 more) |
| L1 | `audio-unit-for-aaf` | no AUDIO_UNIT | `L1 audio-unit-for-aaf: cfg 0 AUDIO_UNIT: a stream lists an AAF format and the configuration has no AUDIO_UNIT (Milan v1.2 §5.3.3.3)` (+10 more) |
| L1 | `stream-port-for-aaf` | AUDIO_UNIT owns no output port | `L1 stream-port-for-aaf: cfg 0 STREAM_PORT_OUTPUT: AAF streams [0] and no STREAM_PORT_OUTPUT in an AUDIO_UNIT (Milan v1.2 §5.3.3.7)` (+4 more) |
| L1 | `port-cluster-minimum` | input port with no cluster | `L1 port-cluster-minimum: cfg 0 STREAM_PORT_INPUT 0: number_of_clusters 0; a Stream Port contains at least one AUDIO_CLUSTER (Milan v1.2 §5.3.3.8)` |
| L1 | `child-exists` | output port names AUDIO_CLUSTER 4 | `L1 child-exists: cfg 0 STREAM_PORT_OUTPUT 0: names AUDIO_CLUSTER 4, which does not exist (Milan v1.2 §5.3.2; IEEE 1722.1-2021 §7.2.3, §7.2.8, §7.2.13)` |
| L1 | `single-parent` | two ports share AUDIO_CLUSTER 2 | `L1 single-parent: cfg 0 AUDIO_CLUSTER 2: claimed by STREAM_PORT_INPUT 0, STREAM_PORT_OUTPUT 0 (Milan v1.2 §5.3.2)` (+1 more) |
| L1 | `has-parent` | AUDIO_MAP 0 has no port | `L1 has-parent: cfg 0 AUDIO_MAP 0: no descriptor's range claims it (Milan v1.2 §5.3.2)` |
| L2 | `parent-order` | output clusters before input clusters | `L2 parent-order: cfg 0 STREAM_PORT_OUTPUT 0: its AUDIO_CLUSTER range starts at 0, before the end 4 of the range of STREAM_PORT_INPUT 0 (IEEE 1722.1-2021 §7.2)` |
| L3 | `stream-presence` | no stream at all | `L3 stream-presence: cfg 0: no STREAM_INPUT and no STREAM_OUTPUT (Milan v1.2 §5.3.3.4)` (+4 more) |
| L3 | `talker-base-format` | output format 24-bit | `L3 talker-base-format: cfg 0 STREAM_OUTPUT: the entity is a Talker and no Stream Output lists a Base format (Milan v1.2 §6.3)` |
| L3 | `listener-base-format` | input format 24-bit | `L3 listener-base-format: cfg 0 STREAM_INPUT: the entity is a Listener and no Stream Input lists a Base format (Milan v1.2 §6.4)` |
| L3 | `base-channel-completeness` | input Base format up to 6 channels | `L3 base-channel-completeness: cfg 0 STREAM_INPUT 0: Base 48 kHz without channel counts [8] (Milan v1.2 §6.4)` |
| L3 | `base-rate-uniformity` | second Base input at 96 kHz | `L3 base-rate-uniformity: cfg 0 STREAM_INPUT: Base-format inputs with different Base rates (STREAM_INPUT 0: 48 kHz; STREAM_INPUT 1: 96 kHz) (Milan v1.2 §6.4)` |
| L3 | `crf-format` | CRF input at 44.1 kHz only | `L3 crf-format: cfg 0 STREAM_INPUT 1: lists CRF formats without 0x041060010000BB80 (Milan v1.2 §7.3.1, §7.3.4)` |
| L4 | `buffer-length` | buffer_length 2125999 ns | `L4 buffer-length: cfg 0 STREAM_INPUT 0: buffer_length 2125999 ns, below 2126000 (Milan v1.2 §5.3.3.4)` |
| L4 | `class-a` | output without CLASS_A | `L4 class-a: cfg 0 STREAM_OUTPUT 0: stream_flags 0x0000 without CLASS_A (Milan v1.2 §5.3.3.4, §7.3.3)` |
| L4 | `format-family` | CRF input lists an AAF format | `L4 format-family: cfg 0 STREAM_INPUT 1: lists both CRF and AAF formats (Milan v1.2 §5.3.3.4)` |
| L4 | `current-format` | output current_format 96 kHz | `L4 current-format: cfg 0 STREAM_OUTPUT 0: current_format 0x020702200080C000 is not in its list (Milan v1.2 §5.3.3.4)` |
| L4 | `format-count` | input with 47 formats | `L4 format-count: cfg 0 STREAM_INPUT 0: number_of_formats 47, above 46 (IEEE 1722.1-2021 §7.2, §7.2.6 Table 7-8)` |
| L4 | `stream-layout` | output with a redundant stream | `L4 stream-layout: cfg 0 STREAM_OUTPUT 0: number_of_redundant_streams 1 on a non-redundant PAAD (Milan v1.2 §5.3.3.4; IEEE 1722.1-2021 §7.2.6 Table 7-8)` |
| L5 | `interface-index` | configuration 1 moves the port to AVB_INTERFACE 0 port 2 | `L5 interface-index: cfg 1 AVB_INTERFACE: index-to-port_number {0: 2}; configuration 0 has {0: 1} (Milan v1.2 §5.3.3.5)` |
| L6 | `crf-input-source` | CRF source at the AAF input | `L6 crf-input-source: cfg 0 STREAM_INPUT 1: a CRF input with 0 INPUT_STREAM sources (Milan v1.2 §5.3.3.6)` |
| L6 | `aaf-input-source` | no CRF input and no INPUT_STREAM source | `L6 aaf-input-source: cfg 0 CLOCK_SOURCE: no CRF input, and 0 INPUT_STREAM sources at AAF inputs [0, 1] (Milan v1.2 §5.3.3.6)` |
| L6 | `internal-source` | no INTERNAL source | `L6 internal-source: cfg 0 CLOCK_SOURCE: Stream Outputs and no INTERNAL CLOCK_SOURCE (Milan v1.2 §5.3.3.6)` |
| L6 | `gptp-source-interfaces` | gPTP media clock with two interfaces | `L6 gptp-source-interfaces: cfg 0 CLOCK_SOURCE 2: a gPTP media clock source with 2 AVB_INTERFACEs (Milan v1.2 §5.3.3.6, §7.5.1)` |
| L7 | `input-port-maps` | input port owns AUDIO_MAP 0 | `L7 input-port-maps: cfg 0 STREAM_PORT_INPUT 0: number_of_maps 1; input mappings are dynamic (Milan v1.2 §5.3.3.7, §5.3.3.9)` (+2 more) |
| L7 | `unique-mapping` | stream 0 channel 0 mapped twice | `L7 unique-mapping: cfg 0 AUDIO_MAP 0: stream 0 channel 0 is also mapped by AUDIO_MAP 0 (Milan v1.2 §5.3.3.9)` |
| L7 | `cluster-channels` | stereo AUDIO_CLUSTER 3 | `L7 cluster-channels: cfg 0 AUDIO_CLUSTER 3: channel_count 2 (Milan v1.2 §5.3.3.8)` |
| L8 | `identify-index` | no IDENTIFY CONTROL | `L8 identify-index: cfg 0 CONTROL: no index holds an IDENTIFY CONTROL in every configuration, and the ADPDU advertises identify_control_index as valid (Milan v1.2 §5.3.3.10, §5.6.2)` |
| L8 | `identify-index` | IDENTIFY at index 0, then 1 | `L8 identify-index: cfg 0 CONTROL: no index holds an IDENTIFY CONTROL in every configuration, and the ADPDU advertises identify_control_index as valid (Milan v1.2 §5.3.3.10, §5.6.2)` |
| L8 | `identify-driven` | identify_index_i 1 (adp) | `L8 identify-driven: cfg 0 CONTROL 1: identify_index_i 1 is not an IDENTIFY CONTROL in every configuration (Milan v1.2 §5.3.3.10, §5.6.2)` |

Waiver behaviour (`WaiverTest`), on "input port with no cluster":
- Applied and reported: `waiver L1 port-cluster-minimum: cfg 0 STREAM_PORT_INPUT 0: 1 finding(s) waived; reason: kebag-logic/milan-fpga#584: ...`.
- The waiver removed: `L1 port-cluster-minimum: cfg 0 STREAM_PORT_INPUT 0: number_of_clusters 0; ...` (ruling test 1).
- Kept on the fixed model: `lint waiver 0 (L1 port-cluster-minimum: cfg 0 STREAM_PORT_INPUT 0) is stale: its check passes for STREAM_PORT_INPUT 0; remove or narrow it` (ruling test 2).
- Past the descriptors: `... is stale: STREAM_PORT_INPUT 1 does not exist; remove or narrow it`.
- It excuses no other check (`L1 has-parent` still refuses) and no other
  scope (`L7 cluster-channels: cfg 0 AUDIO_CLUSTER 2` still refuses).
- Seven malformed waivers are refused, and a configuration-scope waiver
  applies.

### 5. The self-test gate CI runs

- `tb/desc_store/test_gen_desc_image.py`, run by `make` in `tb/desc_store`
  as `generator-check` before the RTL suite. `scripts/run_suites.sh` runs
  it, and so does the `hdl` workflow's suites job.
- 32 tests: `BodyKeyTest` (6, existing, now lint off), `LayoutRefusalTest`
  (5), `LintTest` (5), `WaiverTest` (9), `IdentityTest` (4) and
  `CommandLineTest` (3).
  - The 56 mutations hold one negative image per check (53 checks). A test
    holds the set of mutated checks equal to `CHECKS`.
  - Each mutated model also packs with the lint off, so every counted
    refusal is the lint's.
- `example_milan_8.json` still packs (`image.bin`, `--no-lint`) and boots
  the RTL suite. The pp_top fixture is untouched and its suite passes.
- Check-suppression proof: each check suppressed alone fails the gate, 53
  of 53. The record is in `tb/desc_store/README.md` and 09 §8.4. The
  driver is scratch, not in the tree:
  `$VALIDATION_STORAGE/c8-a496/lint_selfmut.py`.

### 6. Docs

- `docs/architecture/07_memory_maps.md` §3.1:
  - the model lint: where it runs, refusals, waivers, report, models;
  - the rule table gains a Checks column and the L11 row;
  - L4's cap is 46; the "not linted" list;
  - the 8×8 / #584 waiver paragraph; the L10/L6 status;
  - §3.2 F ≤ 46; §3.3.1 sizing text (576 unchanged).
- `docs/00_MILAN_COMPLIANCE_REVIEW.md`:
  - REQ-MDL-001 to 011: Arch "packer model lint Lx (defence in depth)",
    Doc 07 §3.1 and 09 §8.4, Ver DIR; Cov (the original document) unchanged;
  - REQ-MDL-003 and GAP-08: N ≤ 46;
  - REQ-ADP-003 and 004 point at L9 and L11;
  - the GAP-08 text and disposition residue.
- `docs/architecture/09_verification.md` §8.4 (new): the gate's evidence
  map and the mutation record.
- `docs/architecture/04_adp_engine.md`: the field-sourcing rows for
  entity_model_id, the stream counts and identify_control_index point at
  L9, L11 and L8.
- `docs/guides/integrator.md` §6: the rules for `entity_model_id_i`,
  `talker_sources_i`, `listener_sinks_i` and `identify_index_i`, the report
  excerpt, the `adp` and `model_ids` checks (#38 item 4, #39 item 3).
- `tb/desc_store/README.md` (the gate, the mutation proof) and
  `tb/pp_top/README.md` (the fixture is not a Milan model).

### 7. Parent-visible list

- `gen_desc_image.build()` lints by default and refuses a model that breaks
  a rule. Signature: `build(model, line_bytes=576, *, lint=True, adp=None,
  model_ids=None)`. CLI: `--no-lint`, `--model-ids`,
  `--adp-entity-model-id`, `--adp-talker-sources`, `--adp-listener-sinks`,
  `--adp-identify-index`.
- New document key `lint_waivers`.
- New refusal texts: `L<n> <check>: ...` lines, and `lint waiver N ...`.
- The layout report gains, after a blank line, the `semantic lint:` block:
  waivers, ADP values, digest. The parent writes it to `aem_desc.map`; no
  parent code reads it.
- New files beside the packer: `model_lint.py` and `model_rules.py`, which
  the packer imports from its own directory (it puts that directory on
  `sys.path`), plus `milan_min.json` and `model_ids.json`.
- `tb/desc_store/test_gen_desc_image.py` stays the one dispositioned DUT
  reader there. It still imports the generator by path and calls `build()`
  and the CLI. It now also reads `milan_min.json`, `example_milan_8.json`
  and `model_ids.json` beside it. `tb/desc_store/lint_mutations.py` is new
  and reads nothing (the parent's evidence gate classifies it as no
  reader).
- `example_milan_8.json`: one comment line, descriptors unchanged.
  DescriptorImage.MILAN_8 does not move.
- 07 §3.1, the compliance rows, 04, 09 and `integrator.md` §6 change text
  the parent cites.
- Parent adaptation: `parent-adoption-c8-cdf49d1a.patch`, applied after
  `parent-c4-disposition.patch`. Seven files.
  - Gate 36b (`sw/builder/test_builder.py`):
    - the 17 deliberate negatives pack with `lint=False` (`_pack_changed`
      passes `lint=reason is None`, so the 6 accepted cases keep the lint
      on);
    - every index-walk and presence document packs with `lint=False`.
  - The 8×8 waiver, from its config: `configs/endstation_ax7101_8x8.yaml`
    `model_lint_waivers` (L1 `port-cluster-minimum`, configuration 0,
    STREAM_PORT_INPUT 0..7, reason `kebag-logic/milan-fpga#584: ...`),
    passed through unread:
    - `endstation_builder.load_config` → `_overlay_document` (emitted only
      when declared, so the other four overlays are byte-identical);
    - → `aem_specs.spec_from_overlay` → `aem_assemble.build_model` →
      `gen_aemi_image.model_to_document` → `lint_waivers` of the document.
    - No caller of `build()` changed.
  - `docs/ENDSTATION_BUILDER.md` §3: row 45 for the new key, and "71 rows"
    → "72 rows".
    - The builder test's gate 32 refuses an accepted config key without a
      row. Its first run here failed on exactly that: `keys with no row:
      ['model_lint_waivers']`.
    - The row is part of carrying the waiver from the config, and nothing
      beyond it.
- For the parent's pin-adoption lane: the parent's own L10/L6 checks in
  `sw/builder/aem_image_checks.py` now duplicate the processor's. The
  ruling leaves removing them to that lane.

## Commits

| Commit | Subject |
|---|---|
| 345b763 | Lint the descriptor model in the packer by default: rules L1 to L11, per-check waivers, the ADP input report and checks, and the recorded model digest (#38, #39, #60, #89) |
| 0730a08 | Record the packer gate and its check-suppression proof in the desc_store README, and state that the pp_top fixture image is not a Milan model |
| e6cca1f | Document the model lint: 07 §3.1 rules and checks with the 46-format cap, the REQ-MDL and REQ-ADP-003/004 rows, 09 §8.4, the ADPDU sourcing rows and integrator guide section 6 |

Items 1 to 5 are in the first commit; one engine serves all four issues and
every intermediate split would have had to rewrite the gate. The per-item
breakdown is above.

## Suites and gates (processor, at e6cca1f)

| Command | Result |
|---|---|
| `./scripts/run_suites.sh` | rc 0: 33 suites, 1,018,843 checks, 0 failing. `desc_store` 584 RTL checks after its `generator-check` (32 tests OK); `pp_top` 8,901 |
| each suite's `make`, one by one before the sweep | all 33 rc 0, the same tallies |
| `make -C tb/desc_store generator-check` | rc 0, 32 tests (the new gate) |
| `./scripts/lint_hdl.sh` | rc 0 |
| `make check` | rc 0: 41 mermaid and 18 wavedrom blocks, 1,031 links, matrix 115 REQ rows / 17 GAPs, module matrix 94 rows / 0 untested, parameters 26 |
| `python3 scripts/gen_matrix.py --check` | rc 0 |
| `git diff --check 03c842a7..HEAD` | rc 0 |
| check-suppression proof (scratch `lint_selfmut.py`) | control 0 failing; 53 of 53 checks killed |

Not run, with the reason:
- The mutation campaigns (`srp_top`, `maap`, `adp_engine`, `pp_top` aecp and
  dispatch), `nvm_port` figures and `syn/yosys/run.sh`. The branch changes no
  RTL file, no harness source and no mutation patch; they grade RTL.

## Parent consumer set (milan-fpga dev cdf49d1a, both patches)

Scratch parent: a `git archive` of the read-only checkout (tree 904f3079, equal
to the checkout's), with the four gitlinks recorded.
- `gptp-processor` 5dce647a and `third_party/verilog-axis` 48ff7a7e are cloned
  at their pins.
- `protocol-processor` is a clone of this branch at e6cca1f, and its gitlink
  is recorded there, so the scope helper sees every project submodule on-pin.
- `parent-c4-disposition.patch` is applied, then
  `parent-adoption-c8-cdf49d1a.patch`. The trusted checkout was not touched.

| # | Gate | Result |
|---|---|---|
| 1, 2 | `check_cpp_idiom.py`, `check_py_idiom.py` | rc 0, every ratchet held (296 Python modules, including `model_lint.py`, `model_rules.py`, `gen_desc_image.py`, `test_gen_desc_image.py`, `lint_mutations.py`) |
| 3 | `xvlog_gate.py --check` | rc 0: 4 findings == ratchet, none new |
| 4, 5 | `check_rtl_source_lists.py`, `pp_srcs.py --check --selftest` | rc 0 (36/42 tops, 6 recorded; 46 sources, self-test passed) |
| 6 | `sw/builder/test_builder.py` | rc 0: all gates pass except 1 not run (gate 11 needs a board implementation report not on this host). Gate 36b: 67 lines, every case at its verdict; gate 32: 113 loader keys == 113 keys across 65 rows |
| 7 | `make -C tb/verilator/pp_shadow -j8` | rc 0: builds of 606, 606, 646 and 311 checks, 0 failures |
| 8 | `check_port_contracts.py` | rc 0: 48 literal-bound, 59 without a rationale (lowerable by 3, as before) |
| 9 | `measure_naming.py --check` | rc 0, 96 recorded |
| 10 | `measure_test_evidence.py --check` | rc 0: 72 <= 77 suites without a mutation arm, 10 <= 10 unseeded, 0 <= 0 unexplained DUT readers, 3 <= 3 wall-clock files |
| 11 | `docs_check.py` | rc 0, 0 findings |
| 12 | `lint_rtl.py --check` | rc 0, 90 <= 90 |
| 13, 14 | `nvm_cosim` lint and quick | rc 0, 315/315 |
| 15 | `make -C tb/verilator/milan_dp -j8` | rc 0, 9 RESULT PASS, none failing |
| 16 | `make -C tb/verilator/milan_dp_render -j8` | rc 0, leg defects 5/5 |

The patch took two corrections from these gates, both inside the waiver
item:
- The first builder-test run failed gate 32 (`keys with no row:
  ['model_lint_waivers']`). That added the `ENDSTATION_BUILDER.md` §3 row.
- docs_check then refused the section sign in that row, which now reads
  "section 3.1".
- Gates 1, 2, 4, 5 and 8 to 12 ran again on the final patch state, and so did
  gate 6 (rc 0, the same verdict). Gates 3, 7 and 13 to 16 read no file the
  corrections touched.

## Parent models packed through the lint

Each of the five tracked configs was packed at both heads, with both patches
applied:
- through `endstation_builder._entity_model_image`, the builder caller, which
  also runs the parent's post-pack shipping checks;
- again through `build()` with `adp=` taken from the overlay;
- through `avdecc/gen_aemi_image.py`, the CLI caller.

Gate 36b's SoC test at dev confirms `milan_soc.build_desc_image`, the third
caller, makes identical images for all five.

| Model | dev cdf49d1a | PR #634 head 57f4b742 |
|---|---|---|
| `endstation_arty_current` | packed, 0 waivers, driven values agree | packed, 0 waivers, driven values agree |
| `endstation_arty_4x4` | packed, 0 waivers | packed, 0 waivers |
| `endstation_arty_8ch` | packed, 0 waivers | packed, 0 waivers |
| `endstation_ax7101_1x1_tdm8` | packed, 0 waivers | packed, 0 waivers |
| `endstation_ax7101_8x8` | packed only with its waiver, reported: `waiver L1 port-cluster-minimum: cfg 0 STREAM_PORT_INPUT 0..7: 8 finding(s) waived; reason: kebag-logic/milan-fpga#584: ...` | the same |
| `endstation_ax7101_8x8` without the waiver | refused: 8 lines, all `L1 port-cluster-minimum` (STREAM_PORT_INPUT 0..7) | the same |

PR #634 notes:
- The adoption patch applies at PR #634's head with reduced context in one
  hunk (`avdecc/aem_assemble.py`, whose context moved).
- PR #634's added INPUT_STREAM source at the AAF input passes L6: Milan
  §5.3.3.6 requires one per CRF input and forbids no more.

The two ruling tests are in the processor gate (`WaiverTest`):
- `test_without_the_waiver_the_rule_refuses`;
- `test_waiver_on_a_fixed_model_is_stale`.

## Scratch evidence (not in the output directory)

Under `$VALIDATION_STORAGE/c8-a496/`:

| File | Bytes | sha256 |
|---|---|---|
| `lint_selfmut.py` (check-suppression driver) | 1420 | 1d92be886de13e14aa7023b2545e09053d974fb493171cd1ac3f6677a97ce083 |
| `selfmut.txt` (its output) | 2387 | 3f194be066bd060f2c8806b2282267b0344b790f77cf487909998c459fd2825c |
| `pack_models.py` (builder-path packing) | 2041 | 4c9b80ac90b4d563bf07c8397dc66840cfaa56489d1dfaf2dfc7d0365649d582 |
| `pack_cli.sh` (CLI-path packing) | 822 | 9ffb1e17bcbbe3baf19b537c9b2abf81b561a6bf1b86e65fb3e67656233bc212 |
| `pack-dev.txt` | 2801 | 8b19af663dfe04b96cc4c0b2cab1fa5b567f2184480c45b87c74c8d5fd13e501 |
| `pack-pr634.txt` | 2801 | eb82619453a76227d178374a48c70e1325e6f63e855582401e77f3ee366e6258 |
| `make_milan_min.py` (wrote `milan_min.json`) | 12593 | 6cdb4d79f64cc5af682e2e0102b08a1700baf29749aa49f269ef219bf95272e5 |
| `run_suites-e6cca1f.log` | 1762 | 3e26cf592ed47f1a245de437b27c44684ec87ebf06b35a336bfdac78f06b642e |
| `gates-dev/test_builder.log` | 99934 | f8f705e1ea2e3d5821d89825bde49f128215b2dc3e6ded7ff3649dd6afc53105 |
| `gates-dev/pp_shadow.log` | 293764 | 31fae304705d6de5db00148c2cff12bb78fbcc3388bc1931a46a9ba54ac89b91 |
| `gates-dev/milan_dp.log` | 1962984 | f756188548700ca37c5846ae0c4ce9b9b31679b8403978f8cd7b68d497418d7c |
| `gates-dev/milan_dp_render.log` | 153553 | 768454443ec32c0c117a99293fb4fc0c6546eff204253a5f6c7193275a949bd1 |
| `gates-dev/xvlog_gate.log` | 1320 | 0613d8c234bf0337826317420e0f140ef843208acf4f8dd41c40e3db98658e8a |
| `docs-dev/endstation_ax7101_8x8.json` (8×8 document, no waiver) | 35180 | 5a6e445bcf905a80288bf81531230887cdcec471ee2dde2bb05f62177a917f4b |
| `docs-pr634/endstation_ax7101_8x8.json` | 37539 | 65860949f31e513b13d5d1026c49d8ec957c40cd9693b0a1dae8e31886a1a24f |

Output directory:

| File | sha256 |
|---|---|
| `parent-adoption-c8-cdf49d1a.patch` (7 files) | aa5a88eb8e04e5ce0d44ec65973e88215860a9ea5317255016409442000ad209 |
| `parent-c4-disposition.patch` (input, unchanged) | 904a252ce4979f3a19a5bb5ae22a05efc2cde00fdc95b05e1ab52d5021a9d1cf |

## What remains

- The parent's pin-adoption lane applies `parent-adoption-c8-cdf49d1a.patch`
  after `parent-c4-disposition.patch` when it moves the pin to this branch,
  and may retire its duplicate L10/L6 checks.
- milan-fpga#584: once the 8×8 input pools carry clusters, the waiver is
  stale, the packer refuses it, and it must leave the config.
- The checks 07 §3.1 lists as not linted.

