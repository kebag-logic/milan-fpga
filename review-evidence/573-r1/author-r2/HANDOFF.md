# Round 2 handoff

Author: [A352]. Issues #573-#576; PR #585.
Branch: `573-builder-model-refusals`.
Starting head: `4f746408a15f494c4b30bdc9add6d7295309dff9`.
Final head: `08374721d958b32ade38e7e62d25a7ccea215119`.
Comparison base: `e0920d77162284d8da52ffaf13a973e451e44f90`.
Remote verified: `https://github.com/kebag-logic/milan-fpga.git`.

Implementation is complete in five item-group commits.
Both full builder modes and the code/documentation gates return zero.
The unchanged historical format-length reproducer has the documented rc 1.
Independent re-review of all five lenses is required.
This author evidence does not clear the reviewer-owned completion ledger.
No tracked configuration was refused; the STOP rule did not trigger.
No push, PR change, merge, hardware activity or submodule edit occurred.

## Public contract and authorities

- [Assignment and decisions](https://github.com/kebag-logic/milan-fpga/issues/573#issuecomment-5854262940).
- [Internal review](https://github.com/kebag-logic/milan-fpga/pull/585#issuecomment-5854235849).
- [External review](https://github.com/kebag-logic/milan-fpga/pull/585#issuecomment-5854260028).
- Full reports and unchanged scripts came from branch `573-review-evidence`,
  under `review-evidence/573-r1/reviews/R340-1/` and `R341-1/`.
  Fetched evidence commit: `b2e55a725a0111b9d2626447d08fee9a235d3228`.
- IEEE 1722.1-2021 section 7.2: descriptor maximum 508 octets.
  Table 7-8: formats_offset 138, number_of_formats maximum 46,
  buffer_length width four octets.
- Milan v1.2 5.3.3.1 applies the reserved-ID rule to ENTITY;
  5.6.2 applies it to ADPDUs. Section 5.3.1 remains evolution-only.
- Only PDF pages 64-65, 73-74 (IEEE) and 32, 108 (Milan) were
  extracted with `pdftotext -layout -f/-l`; extracts remain under `/tmp`.
  Processor-owned cap statements remain assigned to processor issue 60.

## Change list

| Group | Commit | Files and behavior |
|---|---|---|
| 1 | `2a15d68b7cf8475547ab9ae43cba93266b0be627` | `avdecc/aem_descriptors.py:272` owns layout-derived `MAX_STREAM_FORMATS`; `sw/builder/endstation_builder.py:1395` enforces it after completion; `sw/builder/test_declarations.py:153` checks 46/47 final entries and packed length; README:128 and matrix:62,243 state 46. |
| 2 | `71b614ba6061c147d7781985c20309e3c0af8b96` | `avdecc/aem_descriptors.py:183` shares u32 encoding and maximum; `sw/builder/endstation_builder.py:1380` refuses overflow; `sw/builder/test_declarations.py:103` verifies packed equality at every listener index; README:131 and matrix:62,242 describe both bounds. |
| 3 | `d20eeb892b669060278f669be977b0540f7c0d34` | `sw/builder/endstation_builder.py:1339`, `sw/builder/test_declarations.py:36,46`, README:153 and matrix:67 cite the correct ENTITY/ADPDU clauses. |
| 4 | `5cf31b2c2628903b03998b3a19623a13a313db5e` | `docs/ENDSTATION_BUILDER.md:443` states the enforced refusal. Optional parameter-table expansion was unnecessary. |
| 5 | `08374721d958b32ade38e7e62d25a7ccea215119` | `sw/builder/endstation_builder.py:1329,3841,4373` preserves numeric EUI-64 values, refuses empty sources and validates shadowed/derived identities. `sw/builder/test_declarations.py:69,218` covers each accepted suggestion. README:121,150 and matrix:64,193 describe the resulting contracts. |

All line references name the final head. README means
`sw/builder/README-parameters.md`; matrix means
`docs/reference/PP_DESCRIPTOR_OWNERSHIP.md`.

## Finding and disposition table

| Finding | Reviewer severity and lenses | Disposition | Discriminating evidence |
|---|---|---|---|
| R341-1 F1 | MAJOR; Conformance, Robustness, Tests, Docs | Fixed; re-review pending | 46 final entries accepted in both directions; 47 refused. Listeners accept 45+1 and refuse 46+1. Accepted boundary packs to 506 bytes. Raising the cap is killed. |
| R340-F1 / R341-1 F2 | MAJOR governs; Conformance, RTL, Robustness, Tests | Fixed; re-review pending | Every listener accepts and packs 0xFFFFFFFF unchanged; 2^32 and 2^32+2125999 refuse. Width comes from the same Struct used to pack. Removing the upper guard is killed. Unchanged buffer probe confirms results. |
| R340-F3 / R341-1 F3 | MINOR; Conformance, Docs | Fixed under public clause decision; re-review pending | Message, test comments, README and L9 cite 5.3.3.1/5.6.2. Evolution keeps 5.3.1. |
| R340-F2 | MINOR; Docs | Fixed; re-review pending | Builder design doc now describes named reserved-ID refusal. |
| R340-S1 | SUGGESTION; Tests | Implemented | Direct helper call with no AAF talker refuses CRF output without INTERNAL. Removed CRF arm fails that exact assertion. |
| R340-S2 | SUGGESTION; Robustness | Implemented; also addresses #495 R331-1 S3 | Empty sources refuse with L6 ConfigError, with default present or omitted. `[internal]` remains accepted. |
| R340-S3 | SUGGESTION; Robustness | Implemented | Literal guard runs even with a pin; both reserved literals refuse. A valid pin still wins over a valid literal. |
| R341-1 S1 | SUGGESTION; Robustness | Implemented using exact numeric parsing | Quoted/unquoted YAML hex IDs preserve the written value for literal and pin keys. Reinterpretation mutant is killed. |
| R341-1 S2 | SUGGESTION; Conformance | Implemented | Literal, pin and resolved hash use `_model_id`; forced derived endpoints refuse and legal derived control passes. Bypass mutant is killed. |

## Mutation evidence

Unchanged reviewer runners execute only in a committed archive export.
Each mutation is restored before the next; restored controls pass.
The first runner detects 30/30 original mutations.
The second detects 26/26 applicable original mutations.
Its R-M8 and R-M14 patterns name the removed `MAX_STREAM_FORMATS = 47`
assignment. They remain unchanged and report `applied: false`.
A new cap-plus-one mutation independently covers the current derived bound.
Eight round-2 mutations are detected. Counts include overlapping executions.

| Runner | Mutation | Result | Observable failure |
|---|---|---|---|
| Internal original | A573-01 zero guard removed | KILLED (rc 1) | AssertionError: accepted invalid entity.entity_model_id: must not be zero or all ones |
| Internal original | A573-02 all-ones guard removed | KILLED (rc 1) | AssertionError: accepted invalid entity.entity_model_id: must not be zero or all ones |
| Internal original | A573-03 literal validation removed | KILLED (rc 1) | AssertionError: accepted invalid entity.entity_model_id: must not be zero or all ones |
| Internal original | A573-04 pin validation removed | KILLED (rc 1) | AssertionError: accepted invalid entity.model_id_pin: must not be zero or all ones |
| Internal original | A574-05 listener floor guard removed | KILLED (rc 1) | AssertionError: accepted invalid streams.listeners[0].buffer_length_ns: listener buffer floor |
| Internal original | A575-06 format count guard removed | KILLED (rc 1) | AssertionError: accepted invalid streams.listeners[0].formats: format count |
| Internal original | A575-07 AAF family guard removed | KILLED (rc 1) | AssertionError: accepted invalid streams.listeners[0].formats: must contain only AAF formats |
| Internal original | A575-08 output count guard removed | KILLED (rc 1) | AssertionError: accepted invalid streams.talkers[0].formats: format count |
| Internal original | A575-09 output family guard removed | KILLED (rc 1) | AssertionError: accepted invalid streams.talkers[0].formats: must contain only AAF formats |
| Internal original | A575-10 CRF word guard removed | KILLED (rc 1) | AssertionError: accepted invalid clocking.crf_format: CRF format must be |
| Internal original | A575-11 CRF output word guard removed | KILLED (rc 1) | AssertionError: accepted invalid clocking.crf_output.format: CRF format must be |
| Internal original | A576-12 INTERNAL guard removed | KILLED (rc 1) | AssertionError: accepted invalid clocking.media_clock_sources: requires INTERNAL |
| Internal original | A576-13 AAF output arm removed | KILLED (rc 1) | AssertionError: accepted invalid clocking.media_clock_sources: requires INTERNAL |
| Internal original | A576-14 CRF output arm removed | KILLED (rc 1) | AssertionError: CRF output accepted without INTERNAL |
| Internal original | R-F1a legal near-endpoint rejected | KILLED (rc 1) | endstation_builder.ConfigError: entity.entity_model_id: entity_model_id must not be zero or all ones (Milan v1.2 5.3.3.1 ENTITY; 5.6.2 ADPDU) |
| Internal original | R-F1b guard after literal only via hash path | KILLED (rc 1) | AssertionError: accepted invalid entity.model_id_pin: must not be zero or all ones |
| Internal original | R-F2a floor off-by-one (<=) | KILLED (rc 1) | endstation_builder.ConfigError: streams.listeners[0].buffer_length_ns: must be an integer >= 2126000 ns (Milan v1.2 5.3.3.4 listener buffer floor) |
| Internal original | R-F2b floor lowered by one | KILLED (rc 1) | AssertionError: accepted invalid streams.listeners[0].buffer_length_ns: listener buffer floor |
| Internal original | R-F2c integer-type check removed | KILLED (rc 1) | AssertionError: accepted invalid streams.listeners[0].buffer_length_ns: listener buffer floor |
| Internal original | R-F2d guard applied to talkers instead | KILLED (rc 1) | AssertionError: accepted invalid streams.listeners[0].buffer_length_ns: listener buffer floor |
| Internal original | R-F3a count off-by-one (>=) | KILLED (rc 1) | endstation_builder.ConfigError: streams.listeners[0].formats: format count 46 exceeds 46 (IEEE 1722.1-2021 Table 7-8; final list including derived entries) |
| Internal original | R-F3b declared list validated before completion | KILLED (rc 1) | AssertionError: accepted invalid streams.listeners[0].formats: format count |
| Internal original | R-F3c family compared on top nibble only | KILLED (rc 1) | AssertionError: accepted invalid streams.listeners[0].formats: must contain only AAF formats |
| Internal original | R-F3d family checks current format only | KILLED (rc 1) | AssertionError: accepted invalid streams.listeners[0].formats: must contain only AAF formats |
| Internal original | R-F3e CRF word checks only first entry | KILLED (rc 1) | AssertionError: accepted invalid clocking.crf_format: CRF format must be |
| Internal original | R-F3f CRF input unvalidated | KILLED (rc 1) | AssertionError: accepted invalid clocking.crf_format: CRF format must be |
| Internal original | R-F3g CRF output unvalidated | KILLED (rc 1) | AssertionError: accepted invalid clocking.crf_output.format: CRF format must be |
| Internal original | R-F4a selection instead of availability | KILLED (rc 1) | endstation_builder.ConfigError: clocking.media_clock_sources: every Stream Output requires INTERNAL among its clock sources (Milan v1.2 5.3.3.6) |
| Internal original | R-F4b call site removed | KILLED (rc 1) | AssertionError: accepted invalid clocking.media_clock_sources: requires INTERNAL |
| Internal original | R-F4c call site reads listeners (equivalent in reachable space) | KILLED (rc 1) | AssertionError: ('streams.talkers', 'needs at least one talker stream', 'clocking.media_clock_sources: every Stream Output requires INTERNAL among its clock sources (Milan v1.2 5.3.3.6)') |
| Round 2 | cap raised by one | KILLED (rc 1) | AssertionError: accepted invalid streams.listeners[0].formats: format count |
| Round 2 | buffer upper bound removed | KILLED (rc 1) | AssertionError: accepted invalid streams.listeners[0].buffer_length_ns: listener buffer width |
| Round 2 | buffer upper bound excludes maximum | KILLED (rc 1) | endstation_builder.ConfigError: streams.listeners[0].buffer_length_ns: must be <= 4294967295 ns (IEEE 1722.1-2021 Table 7-8 listener buffer width) |
| Round 2 | empty source refusal removed | KILLED (rc 1) | IndexError: list index out of range |
| Round 2 | pin shadows invalid literal | KILLED (rc 1) | AssertionError: accepted invalid entity.entity_model_id: must not be zero or all ones |
| Round 2 | YAML integer reparsed as hex digits | KILLED (rc 1) | AssertionError |
| Round 2 | derived ID bypasses guard | KILLED (rc 1) | AssertionError: accepted invalid entity.entity_model_id: must not be zero or all ones |
| Round 2 | CRF output arm removed | KILLED (rc 1) | AssertionError: CRF output accepted without INTERNAL |
| External original | zero guard removed | KILLED | AssertionError: accepted invalid entity.entity_model_id: must not be zero or all ones |
| External original | all-ones guard removed | KILLED | AssertionError: accepted invalid entity.entity_model_id: must not be zero or all ones |
| External original | literal validation removed | KILLED | AssertionError: accepted invalid entity.entity_model_id: must not be zero or all ones |
| External original | pin validation removed | KILLED | AssertionError: accepted invalid entity.model_id_pin: must not be zero or all ones |
| External original | listener floor guard removed | KILLED | AssertionError: accepted invalid streams.listeners[0].buffer_length_ns: listener buffer floor |
| External original | format count guard removed | KILLED | AssertionError: accepted invalid streams.listeners[0].formats: format count |
| External original | AAF family guard removed | KILLED | AssertionError: accepted invalid streams.listeners[0].formats: must contain only AAF formats |
| External original | output count guard removed | KILLED | AssertionError: accepted invalid streams.talkers[0].formats: format count |
| External original | output family guard removed | KILLED | AssertionError: accepted invalid streams.talkers[0].formats: must contain only AAF formats |
| External original | CRF word guard removed | KILLED | AssertionError: accepted invalid clocking.crf_format: CRF format must be |
| External original | CRF output word guard removed | KILLED | AssertionError: accepted invalid clocking.crf_output.format: CRF format must be |
| External original | INTERNAL guard removed | KILLED | AssertionError: accepted invalid clocking.media_clock_sources: requires INTERNAL |
| External original | AAF output arm removed | KILLED | AssertionError: accepted invalid clocking.media_clock_sources: requires INTERNAL |
| External original | CRF output arm removed | KILLED | AssertionError: CRF output accepted without INTERNAL |
| External original | R-M1 listener list validated before family derivation | KILLED | AssertionError: accepted invalid streams.listeners[0].formats: format count |
| External original | R-M2 floor lowered by one ns | KILLED | AssertionError: accepted invalid streams.listeners[0].buffer_length_ns: listener buffer floor |
| External original | R-M3 floor made exclusive | KILLED | endstation_builder.ConfigError: streams.listeners[0].buffer_length_ns: must be an integer >= 2126000 ns (Milan v1.2 5.3.3.4 listener buffer floor) |
| External original | R-M4 integer type check removed | KILLED | AssertionError: accepted invalid streams.listeners[0].buffer_length_ns: listener buffer floor |
| External original | R-M5 floor applied to talkers instead of listeners | KILLED | AssertionError: accepted invalid streams.listeners[0].buffer_length_ns: listener buffer floor |
| External original | R-M6 family compare ignores the v bit | KILLED | AssertionError: accepted invalid streams.listeners[0].formats: must contain only AAF formats |
| External original | R-M7 family compare only inspects the current format | KILLED | AssertionError: accepted invalid streams.listeners[0].formats: must contain only AAF formats |
| External original | R-M8 count cap raised to 48 | NOT APPLIED: obsolete literal pattern | No current source match |
| External original | R-M9 AAF stream list validation call removed | KILLED | AssertionError: accepted invalid streams.listeners[0].formats: format count |
| External original | R-M10 CRF family check skipped (word check kept) | KILLED | AssertionError: ('clocking.crf_format', 'must contain only CRF formats', 'clocking.crf_format: CRF format must be 0x041060010000BB80 (Milan v1.2 7.3.2 Table 7.1)') |
| External original | R-M11 INTERNAL availability replaced by INTERNAL selection | KILLED | endstation_builder.ConfigError: clocking.media_clock_sources: every Stream Output requires INTERNAL among its clock sources (Milan v1.2 5.3.3.6) |
| External original | R-M12 output clock-source call removed from the loader | KILLED | AssertionError: accepted invalid clocking.media_clock_sources: requires INTERNAL |
| External original | R-M13 reserved-ID check on a value adjacent to all ones | KILLED | endstation_builder.ConfigError: entity.entity_model_id: entity_model_id must not be zero or all ones (Milan v1.2 5.3.3.1 ENTITY; 5.6.2 ADPDU) |
| External original | R-M14 cap lowered to the IEEE 1722.1-2021 Table 7-8 value 46 (spec probe, expected to fail the 47-acceptance control) | NOT APPLIED: obsolete literal pattern | No current source match |

## Five-configuration SHA256 tables

The unchanged internal artifact script produced 85 records per revision:
17 artifacts for each of five configurations. Sizes and SHA256 agree 85/85.
The unchanged external shipping script independently agrees for 80/80 files.
Its inventory omits the five in-memory sweep option strings.
Full JSON receipts are `hashes-base.json` and `hashes-head.json`;
external tables are `shipping-base.sha256` and `shipping-head.sha256`.

Builds include all three Arty configurations, preserving #583 behavior.
Exports came from `git archive` at the two commits, with pinned inputs
exported independently. No other implementation lane was read or changed.
Disposable Git metadata supplies the original HEAD and tracked inventory
required by the unchanged reviewer scripts. All trees remain under `/tmp`.
`export_archives.py` records the exact procedure.

### endstation_arty_4x4

| Artifact | Bytes | Base SHA256 | Head SHA256 |
|---|---:|---|---|
| `builder/adp_shape_defaults.svh` | 7562 | `f5539f2c29b0ab0440be88f5985ba41bebb508bede7095e5387a03721e50a418` | `f5539f2c29b0ab0440be88f5985ba41bebb508bede7095e5387a03721e50a418` |
| `builder/aecp_aem_rom.svh` | 52444 | `1cd6c92190c1b4f8c14783423a1618328e2fbefe286ab78edb00f96adb45f59d` | `1cd6c92190c1b4f8c14783423a1618328e2fbefe286ab78edb00f96adb45f59d` |
| `builder/aem_overlay.json` | 11920 | `a9b9d900fb425e95e2b3728b47bc5c10b7d7f6b1027be1758f27b01b00b8f98c` | `a9b9d900fb425e95e2b3728b47bc5c10b7d7f6b1027be1758f27b01b00b8f98c` |
| `builder/build_plan.md` | 11000 | `c040b872fa0102576fccf0f235cd9436722efd9f66cf885b220a5dfcd502d722` | `c040b872fa0102576fccf0f235cd9436722efd9f66cf885b220a5dfcd502d722` |
| `builder/cfg_adp_shape_svh` | 7562 | `f5539f2c29b0ab0440be88f5985ba41bebb508bede7095e5387a03721e50a418` | `f5539f2c29b0ab0440be88f5985ba41bebb508bede7095e5387a03721e50a418` |
| `builder/gptp_ucode.hex` | 13312 | `09f5d05defa759905f23630affc619d6af658e4c5f20aa0f63cc65f41317e651` | `09f5d05defa759905f23630affc619d6af658e4c5f20aa0f63cc65f41317e651` |
| `builder/lwsrp_csr_defaults.svh` | 2183 | `90d4615e95883d5c1fdf5ce4eb8e716ac655114d8f0eb9e5579ec8e671bbfa88` | `90d4615e95883d5c1fdf5ce4eb8e716ac655114d8f0eb9e5579ec8e671bbfa88` |
| `builder/lwsrp_table.json` | 4084 | `90e1aa992317980e97ec42768d524e9b8af65e2279a31e1696f5f68254f05221` | `90e1aa992317980e97ec42768d524e9b8af65e2279a31e1696f5f68254f05221` |
| `builder/lwsrp_table.svh` | 4288 | `36331d96c16b57ba3660a3183af58752195d94f2681d03ccfcf50003f227b222` | `36331d96c16b57ba3660a3183af58752195d94f2681d03ccfcf50003f227b222` |
| `builder/platform_shape.json` | 246 | `bbd040ba298a66ff0bd856f8f0b4e75c04c1831ba635a5b3ad756625ab8b0a28` | `bbd040ba298a66ff0bd856f8f0b4e75c04c1831ba635a5b3ad756625ab8b0a28` |
| `builder/soc_params.json` | 589 | `fe552b1ec220f349b55cd499bc62680e9f7abf28397125cc457fd7cf63f61fb8` | `fe552b1ec220f349b55cd499bc62680e9f7abf28397125cc457fd7cf63f61fb8` |
| `builder/sweep_opts` | 1209 | `f50e8a7f952d693de9c85e76caec5d77c252726cd6409eaee57e4a328efe8dcc` | `f50e8a7f952d693de9c85e76caec5d77c252726cd6409eaee57e4a328efe8dcc` |
| `image/aem_desc.bin` | 10112 | `1b288e13ccbf03410c593a53bc22f4a68e3d289eef8a7f907e63bc98a51415ff` | `1b288e13ccbf03410c593a53bc22f4a68e3d289eef8a7f907e63bc98a51415ff` |
| `image/aem_desc.json` | 20716 | `0ea2e47927e0a0eff12d781d979a255c39a935b7f06e07366d9ab3ff368d4e3e` | `0ea2e47927e0a0eff12d781d979a255c39a935b7f06e07366d9ab3ff368d4e3e` |
| `image/aem_desc.map` | 1311 | `09cf3da5a39730c1acedae4f09474c2d98d1aa17d8fa36f0238adc210fdaa571` | `09cf3da5a39730c1acedae4f09474c2d98d1aa17d8fa36f0238adc210fdaa571` |
| `store/aecp_aem_rom.svh` | 52444 | `1cd6c92190c1b4f8c14783423a1618328e2fbefe286ab78edb00f96adb45f59d` | `1cd6c92190c1b4f8c14783423a1618328e2fbefe286ab78edb00f96adb45f59d` |
| `store/aem_rom.json` | 22180 | `b9ef1f60be8ed24ce5545a98f4f899d3078d06694a791caef8f69086ffc70b7b` | `b9ef1f60be8ed24ce5545a98f4f899d3078d06694a791caef8f69086ffc70b7b` |

### endstation_arty_8ch

| Artifact | Bytes | Base SHA256 | Head SHA256 |
|---|---:|---|---|
| `builder/adp_shape_defaults.svh` | 7836 | `41c02ad55f431ac15262d8a5db8e4a24945d375f217f7f0e552cd0b3f18cdd89` | `41c02ad55f431ac15262d8a5db8e4a24945d375f217f7f0e552cd0b3f18cdd89` |
| `builder/aecp_aem_rom.svh` | 71921 | `19dd262b93e56aeab1641f3d3e534fc7af372f1c2f8c1801e5a7895d1982ae34` | `19dd262b93e56aeab1641f3d3e534fc7af372f1c2f8c1801e5a7895d1982ae34` |
| `builder/aem_overlay.json` | 16978 | `87fc3c51e2fc5a49b91d67e05ea621449391619430ecfaef4cac5422b5b4b94e` | `87fc3c51e2fc5a49b91d67e05ea621449391619430ecfaef4cac5422b5b4b94e` |
| `builder/build_plan.md` | 11003 | `1a93c95f35d176c5b52e03c1f0d5ccea7726c682a803948a5763029a509edf76` | `1a93c95f35d176c5b52e03c1f0d5ccea7726c682a803948a5763029a509edf76` |
| `builder/cfg_adp_shape_svh` | 7836 | `41c02ad55f431ac15262d8a5db8e4a24945d375f217f7f0e552cd0b3f18cdd89` | `41c02ad55f431ac15262d8a5db8e4a24945d375f217f7f0e552cd0b3f18cdd89` |
| `builder/gptp_ucode.hex` | 13312 | `09f5d05defa759905f23630affc619d6af658e4c5f20aa0f63cc65f41317e651` | `09f5d05defa759905f23630affc619d6af658e4c5f20aa0f63cc65f41317e651` |
| `builder/lwsrp_csr_defaults.svh` | 2183 | `f2519804843397b4bde6393e3be67f348e3b3ef6e73e62fef22b3a71b4ecf87f` | `f2519804843397b4bde6393e3be67f348e3b3ef6e73e62fef22b3a71b4ecf87f` |
| `builder/lwsrp_table.json` | 4084 | `0e151e2854b3799281d19d01e67c27b04a53ca470a672ad27bc48f93ea840987` | `0e151e2854b3799281d19d01e67c27b04a53ca470a672ad27bc48f93ea840987` |
| `builder/lwsrp_table.svh` | 4288 | `c7189e2e3dcf79a7fcd6c204674fca581d89aea327c77b65ea7aa57f38aa3e19` | `c7189e2e3dcf79a7fcd6c204674fca581d89aea327c77b65ea7aa57f38aa3e19` |
| `builder/platform_shape.json` | 246 | `b818b72a035c5f73870925ffe208eda20292bedc629a399d5d31aa14160242ce` | `b818b72a035c5f73870925ffe208eda20292bedc629a399d5d31aa14160242ce` |
| `builder/soc_params.json` | 589 | `7a10be52746259e11e1c43402cb8097ca5234e9b358fd6160af5c5e42673faff` | `7a10be52746259e11e1c43402cb8097ca5234e9b358fd6160af5c5e42673faff` |
| `builder/sweep_opts` | 1209 | `8ea30219313f53e66c302861aa6e8824d0ded1f7f6ddc159a113ff79326a75f3` | `8ea30219313f53e66c302861aa6e8824d0ded1f7f6ddc159a113ff79326a75f3` |
| `image/aem_desc.bin` | 15360 | `2b5c008cf3a2ff1eca11ef5e24c5a2e391e97f25435854430e563758de516b9b` | `2b5c008cf3a2ff1eca11ef5e24c5a2e391e97f25435854430e563758de516b9b` |
| `image/aem_desc.json` | 31200 | `22d2815009a4d468faf1d48322b57e5ef2f6260d34219299810b7e5aafaced18` | `22d2815009a4d468faf1d48322b57e5ef2f6260d34219299810b7e5aafaced18` |
| `image/aem_desc.map` | 1311 | `163d5a414e34591ad639c3682747a35c43db64dcb3d46cb06c77d4c33edb634a` | `163d5a414e34591ad639c3682747a35c43db64dcb3d46cb06c77d4c33edb634a` |
| `store/aecp_aem_rom.svh` | 71921 | `19dd262b93e56aeab1641f3d3e534fc7af372f1c2f8c1801e5a7895d1982ae34` | `19dd262b93e56aeab1641f3d3e534fc7af372f1c2f8c1801e5a7895d1982ae34` |
| `store/aem_rom.json` | 32868 | `de55410b93502c4ddfa3e1555efcde68b9e805833bf528969d78bcbd2af7ae45` | `de55410b93502c4ddfa3e1555efcde68b9e805833bf528969d78bcbd2af7ae45` |

### endstation_arty_current

| Artifact | Bytes | Base SHA256 | Head SHA256 |
|---|---:|---|---|
| `builder/adp_shape_defaults.svh` | 7089 | `54f350a99a0e6883f394858fe12457cffb4a1fea08ae23f5ba42c02636a46c98` | `54f350a99a0e6883f394858fe12457cffb4a1fea08ae23f5ba42c02636a46c98` |
| `builder/aecp_aem_rom.svh` | 33428 | `d8365928caecf01dc79b3d9a75a6c56573669ad121d8cc04b42f44820601c999` | `d8365928caecf01dc79b3d9a75a6c56573669ad121d8cc04b42f44820601c999` |
| `builder/aem_overlay.json` | 6238 | `12f48ab98be36408d6090158d5fc27341ca72d53217fcf892e097fbadab4e70e` | `12f48ab98be36408d6090158d5fc27341ca72d53217fcf892e097fbadab4e70e` |
| `builder/build_plan.md` | 9105 | `4eb5e433433f1c3af1311a4585c9a80101178766c8aa9f7573a75d3e034167bf` | `4eb5e433433f1c3af1311a4585c9a80101178766c8aa9f7573a75d3e034167bf` |
| `builder/cfg_adp_shape_svh` | 7089 | `54f350a99a0e6883f394858fe12457cffb4a1fea08ae23f5ba42c02636a46c98` | `54f350a99a0e6883f394858fe12457cffb4a1fea08ae23f5ba42c02636a46c98` |
| `builder/gptp_ucode.hex` | 13312 | `09f5d05defa759905f23630affc619d6af658e4c5f20aa0f63cc65f41317e651` | `09f5d05defa759905f23630affc619d6af658e4c5f20aa0f63cc65f41317e651` |
| `builder/lwsrp_csr_defaults.svh` | 2187 | `d10ce5559b108f54800b8432b672a0d33379721bf2a4edf0058e185484f3881d` | `d10ce5559b108f54800b8432b672a0d33379721bf2a4edf0058e185484f3881d` |
| `builder/lwsrp_table.json` | 2274 | `dc4a200fa4dae047598419a78713677aefeab85b957808b9ec7284f2411a668f` | `dc4a200fa4dae047598419a78713677aefeab85b957808b9ec7284f2411a668f` |
| `builder/lwsrp_table.svh` | 3826 | `df3c4fa0289d23deea8f8e688573faa1adbb12f8485a7b5613bd30b8b288f8e4` | `df3c4fa0289d23deea8f8e688573faa1adbb12f8485a7b5613bd30b8b288f8e4` |
| `builder/platform_shape.json` | 250 | `03328f238565f45f775a8fb17921a20ac4172d864b218e3703c23e185e678c99` | `03328f238565f45f775a8fb17921a20ac4172d864b218e3703c23e185e678c99` |
| `builder/soc_params.json` | 498 | `696350eee365adb614b78e445d6522569e73d0eaa555b4de6603319d45da59cb` | `696350eee365adb614b78e445d6522569e73d0eaa555b4de6603319d45da59cb` |
| `builder/sweep_opts` | 1143 | `969f765fe53c592a9fd4afcbb415733fd3ed1c2e367d788faf81e9f2e88ec6c7` | `969f765fe53c592a9fd4afcbb415733fd3ed1c2e367d788faf81e9f2e88ec6c7` |
| `image/aem_desc.bin` | 5792 | `ac833c3ccde42a2d9a78b517d660b9f7da03c4b3d31227aa65dcaf9e8def6192` | `ac833c3ccde42a2d9a78b517d660b9f7da03c4b3d31227aa65dcaf9e8def6192` |
| `image/aem_desc.json` | 11356 | `3c4b9440bccdc59198dacbc073fbb01671dec866d5adcf1b98225c8b6f822057` | `3c4b9440bccdc59198dacbc073fbb01671dec866d5adcf1b98225c8b6f822057` |
| `image/aem_desc.map` | 1310 | `77dad531965096987d682f77e93f81e5b6f182eaae879fb43b084be8570bec4c` | `77dad531965096987d682f77e93f81e5b6f182eaae879fb43b084be8570bec4c` |
| `store/aecp_aem_rom.svh` | 33428 | `d8365928caecf01dc79b3d9a75a6c56573669ad121d8cc04b42f44820601c999` | `d8365928caecf01dc79b3d9a75a6c56573669ad121d8cc04b42f44820601c999` |
| `store/aem_rom.json` | 12722 | `1c25578eda1352acf7442ca90d0eb964709388ad23954e07f9bbc726004faa5a` | `1c25578eda1352acf7442ca90d0eb964709388ad23954e07f9bbc726004faa5a` |

### endstation_ax7101_1x1_tdm8

| Artifact | Bytes | Base SHA256 | Head SHA256 |
|---|---:|---|---|
| `builder/adp_shape_defaults.svh` | 7199 | `eb03dfaa2f914f49b07c31ddcc62ebc4a64e839a466a3387650f25823afb1020` | `eb03dfaa2f914f49b07c31ddcc62ebc4a64e839a466a3387650f25823afb1020` |
| `builder/aecp_aem_rom.svh` | 40979 | `deea618d789b235c532edc47db08838afc7ffc2f74953f1a117d1fb2c7bd5d33` | `deea618d789b235c532edc47db08838afc7ffc2f74953f1a117d1fb2c7bd5d33` |
| `builder/aem_overlay.json` | 7196 | `e148841ac36dbf3e6d6729c49c7c944ed5194adc75941ceb69e3af80b11e3621` | `e148841ac36dbf3e6d6729c49c7c944ed5194adc75941ceb69e3af80b11e3621` |
| `builder/build_plan.md` | 10825 | `203c4859f9557b4a250454fe9e0561706cc581708811988cd926edda9b942858` | `203c4859f9557b4a250454fe9e0561706cc581708811988cd926edda9b942858` |
| `builder/cfg_adp_shape_svh` | 7199 | `eb03dfaa2f914f49b07c31ddcc62ebc4a64e839a466a3387650f25823afb1020` | `eb03dfaa2f914f49b07c31ddcc62ebc4a64e839a466a3387650f25823afb1020` |
| `builder/gptp_ucode.hex` | 13312 | `78c8418a00b35cdae75c459c5269ca3892355507c4dc8af9eb2c29d81b87673b` | `78c8418a00b35cdae75c459c5269ca3892355507c4dc8af9eb2c29d81b87673b` |
| `builder/lwsrp_csr_defaults.svh` | 2190 | `0e9df2d455d90782c87546dab4dd1fe7b5fb7f4bc81074e910ba71ddc7016d74` | `0e9df2d455d90782c87546dab4dd1fe7b5fb7f4bc81074e910ba71ddc7016d74` |
| `builder/lwsrp_table.json` | 2289 | `61b2e71d9a40c61bfb0eaf884af6257b1b030e441c5f507f99720d0c18dad47d` | `61b2e71d9a40c61bfb0eaf884af6257b1b030e441c5f507f99720d0c18dad47d` |
| `builder/lwsrp_table.svh` | 3832 | `8209fdee3cd744d24a066b76017f71f16d87f636c4470eb95e9f986dce550522` | `8209fdee3cd744d24a066b76017f71f16d87f636c4470eb95e9f986dce550522` |
| `builder/platform_shape.json` | 253 | `0325a3cc988f7f97b34997ef3ac53c6624edfc62b0bd4b5ffb42dc72894ddae7` | `0325a3cc988f7f97b34997ef3ac53c6624edfc62b0bd4b5ffb42dc72894ddae7` |
| `builder/soc_params.json` | 799 | `d5ec9866f86c339dc1c178c31c7800a359813660d9cbcc95e242e1e29b13c516` | `d5ec9866f86c339dc1c178c31c7800a359813660d9cbcc95e242e1e29b13c516` |
| `builder/sweep_opts` | 1366 | `515d8610aa1a58f3b2e6b004d63eada43e826886ab420370ac9c45b63697670f` | `515d8610aa1a58f3b2e6b004d63eada43e826886ab420370ac9c45b63697670f` |
| `image/aem_desc.bin` | 7352 | `9b077636b1d42aca660b16dce8eafa06f1e3cac842134e51ba65930d16214404` | `9b077636b1d42aca660b16dce8eafa06f1e3cac842134e51ba65930d16214404` |
| `image/aem_desc.json` | 14387 | `679d8286a0151b921aa1c6d38370c7c231020f1a5c75a85e565fce9fe1ba0c17` | `679d8286a0151b921aa1c6d38370c7c231020f1a5c75a85e565fce9fe1ba0c17` |
| `image/aem_desc.map` | 1243 | `07151f7c4b493da8e1d3fea32a7e9755951d8e97e021e040ef2a9f3899cb7ede` | `07151f7c4b493da8e1d3fea32a7e9755951d8e97e021e040ef2a9f3899cb7ede` |
| `store/aecp_aem_rom.svh` | 40979 | `deea618d789b235c532edc47db08838afc7ffc2f74953f1a117d1fb2c7bd5d33` | `deea618d789b235c532edc47db08838afc7ffc2f74953f1a117d1fb2c7bd5d33` |
| `store/aem_rom.json` | 15820 | `9469c9d0e79e8d949c2246437f8276a09098875ab2bf5e0b514256d40bc37f54` | `9469c9d0e79e8d949c2246437f8276a09098875ab2bf5e0b514256d40bc37f54` |

### endstation_ax7101_8x8

| Artifact | Bytes | Base SHA256 | Head SHA256 |
|---|---:|---|---|
| `builder/adp_shape_defaults.svh` | 8449 | `26a61e545097a577f1b6bae2e15e92c867e4143a8f8ceb13e2abc21d03279333` | `26a61e545097a577f1b6bae2e15e92c867e4143a8f8ceb13e2abc21d03279333` |
| `builder/aecp_aem_rom.svh` | 86567 | `9f6963190256809964376e8747ebc3465d4b4831df01ec3d91c7e8892e46d755` | `9f6963190256809964376e8747ebc3465d4b4831df01ec3d91c7e8892e46d755` |
| `builder/aem_overlay.json` | 20163 | `baef8bb15a57606b047e657c8ba50460d7f806983a0e08bf24432fc32435fb0c` | `baef8bb15a57606b047e657c8ba50460d7f806983a0e08bf24432fc32435fb0c` |
| `builder/build_plan.md` | 15177 | `cda16a14dfa18d0021888a34e98af04c549c280adece820137712db93fb04f72` | `cda16a14dfa18d0021888a34e98af04c549c280adece820137712db93fb04f72` |
| `builder/cfg_adp_shape_svh` | 8449 | `26a61e545097a577f1b6bae2e15e92c867e4143a8f8ceb13e2abc21d03279333` | `26a61e545097a577f1b6bae2e15e92c867e4143a8f8ceb13e2abc21d03279333` |
| `builder/gptp_ucode.hex` | 13312 | `21e846a7e1989091e555486bbb571b6967eb014925f768dbca7d41124d1d3748` | `21e846a7e1989091e555486bbb571b6967eb014925f768dbca7d41124d1d3748` |
| `builder/lwsrp_csr_defaults.svh` | 2185 | `c9849c561b9aab3f682e2974ce1ba81443c2696a0c1a4e53d3975f2557c159c4` | `c9849c561b9aab3f682e2974ce1ba81443c2696a0c1a4e53d3975f2557c159c4` |
| `builder/lwsrp_table.json` | 6498 | `604cd1bae811ba9ff4c115db0009bb73f538223a90ca79466d28240cbc2e9415` | `604cd1bae811ba9ff4c115db0009bb73f538223a90ca79466d28240cbc2e9415` |
| `builder/lwsrp_table.svh` | 4918 | `59bfe055ba72d4d9254163ba9fff232ad7edf7511235caf7aacb93f789ff10fa` | `59bfe055ba72d4d9254163ba9fff232ad7edf7511235caf7aacb93f789ff10fa` |
| `builder/platform_shape.json` | 248 | `a08aef1e775ecd345a7f87157f4bf3eed28306250d49003d0c5231e714e6cf17` | `a08aef1e775ecd345a7f87157f4bf3eed28306250d49003d0c5231e714e6cf17` |
| `builder/soc_params.json` | 787 | `fe470422d9e29e0f9727deca18945d57975f4cb7d1e61722332205c411d99927` | `fe470422d9e29e0f9727deca18945d57975f4cb7d1e61722332205c411d99927` |
| `builder/sweep_opts` | 1359 | `734ba3acf384b296987156b2e676001fbe4e0558a49e1052e66009c3912d2fc2` | `734ba3acf384b296987156b2e676001fbe4e0558a49e1052e66009c3912d2fc2` |
| `image/aem_desc.bin` | 18288 | `193bf18736d23256c1b25d9af1bddb0721d95780fb36a14cf5f91476aff1a2d4` | `193bf18736d23256c1b25d9af1bddb0721d95780fb36a14cf5f91476aff1a2d4` |
| `image/aem_desc.json` | 37534 | `50eaefa69bcad009479d1d7df3ced08f26b319d1a91dfe2ce659ef97c53620ad` | `50eaefa69bcad009479d1d7df3ced08f26b319d1a91dfe2ce659ef97c53620ad` |
| `image/aem_desc.map` | 1244 | `14d38a422d09d4b729032b19cfeb515756b30156c22f65df842184956ffd989f` | `14d38a422d09d4b729032b19cfeb515756b30156c22f65df842184956ffd989f` |
| `store/aecp_aem_rom.svh` | 86567 | `9f6963190256809964376e8747ebc3465d4b4831df01ec3d91c7e8892e46d755` | `9f6963190256809964376e8747ebc3465d4b4831df01ec3d91c7e8892e46d755` |
| `store/aem_rom.json` | 39074 | `8bd1f3f6e3d790d3c819741a787a5d04c5d9b4c37faf81011f1989a371fda476` | `8bd1f3f6e3d790d3c819741a787a5d04c5d9b4c37faf81011f1989a371fda476` |

## Gate table

All commands run from `$LANES/573-builder-refusals`.
Reviewer arguments point to disposable archive exports as assigned.
`$EVIDENCE` denotes this directory. `run_gate.py` runs the command directly,
without a pipeline, with a 10800-second limit and its actual return code.
Raw logs remain under `/tmp/573-a352`; public logs scrub home-path identity.
Large text logs are split below 200 KB per file, preserving their contents.
Required Markdown packages live only in `/tmp/573-a352/env`.

| Gate | Exact command | rc | Seconds | Receipt |
|---|---|---:|---:|---|
| builder-absent | `python3 $EVIDENCE/builder_absent.py` | 0 | 549.94 | `builder-absent.result.json` |
| builder-present | `python3 sw/builder/test_builder.py --require-rv32` | 0 | 756.33 | `builder-present.result.json` |
| declarations | `python3 sw/builder/test_declarations.py` | 0 | 4.74 | `declarations.result.json` |
| descriptor-audit | `python3 scripts/audit_pp_descriptors.py --output /tmp/573-a352/descriptor-audit.json` | 0 | 1.39 | `descriptor-audit.result.json` |
| diff-whitespace | `git diff e0920d77 --check` | 0 | 0.03 | `diff-whitespace.result.json` |
| diff-worktree-whitespace | `git diff --check` | 0 | 0.03 | `diff-worktree-whitespace.result.json` |
| doc-paths | `python3 scripts/check_doc_paths.py` | 0 | 0.06 | `doc-paths.result.json` |
| doc-style | `python3 scripts/check_doc_style.py` | 0 | 0.06 | `doc-style.result.json` |
| docs-git | `/tmp/573-a352/env/bin/python scripts/docs_check.py` | 0 | 4.22 | `docs-git.result.json` |
| docs-no-git | `env GIT_DIR=/dev/null /tmp/573-a352/env/bin/python scripts/docs_check.py` | 0 | 4.23 | `docs-no-git.result.json` |
| em-dash | `/tmp/573-a352/env/bin/python scripts/check_em_dash.py --base e0920d77` | 0 | 2.97 | `em-dash.result.json` |
| evidence-check | `python3 $EVIDENCE/verify_round2.py` | 0 | 0.03 | `evidence-check.result.json` |
| hashes-base | `python3 -B /tmp/573-a352/R340-1/scripts/hash_artifacts.py /tmp/573-a352/base /tmp/573-a352/hashes-base.json` | 0 | 1.17 | `hashes-base.result.json` |
| hashes-head | `python3 -B /tmp/573-a352/R340-1/scripts/hash_artifacts.py /tmp/573-a352/head /tmp/573-a352/hashes-head.json` | 0 | 1.12 | `hashes-head.result.json` |
| naming | `python3 scripts/measure_naming.py --check` | 0 | 0.47 | `naming.result.json` |
| python-idiom | `python3 scripts/check_py_idiom.py` | 0 | 3.52 | `python-idiom.result.json` |
| review-buffer | `python3 -B /tmp/573-a352/R340-1/scripts/buffer_wrap_probe.py /tmp/573-a352/head` | 0 | 0.26 | `review-buffer.result.json` |
| review-format-length | `python3 -B /tmp/573-a352/R341-1/scripts/format_cap_length.py /tmp/573-a352/head` | 1 | 0.21 | `review-format-length.result.json` |
| review-mutants-340 | `python3 -B /tmp/573-a352/R340-1/scripts/mutants.py /tmp/573-a352/head /tmp/573-a352/R340-1/scripts/mutant_cases.json /tmp/573-a352/review-mutants-340.json` | 0 | 35.33 | `review-mutants-340.result.json` |
| review-mutants-341 | `python3 -B /tmp/573-a352/R341-1/scripts/run_mutants.py /tmp/573-a352/head /tmp/573-a352/R341-1/receipts/author_mutations_input.json /tmp/573-a352/R341-1/scripts/reviewer_mutants.json` | 0 | 32.56 | `review-mutants-341.result.json` |
| review-probes-340 | `python3 -B /tmp/573-a352/R340-1/scripts/probes.py /tmp/573-a352/head /tmp/573-a352/review-probes-340.json` | 0 | 0.72 | `review-probes-340.result.json` |
| review-probes-341 | `python3 -B /tmp/573-a352/R341-1/scripts/bypass_probes.py /tmp/573-a352/head` | 0 | 0.46 | `review-probes-341.result.json` |
| round2-mutants | `python3 -B /tmp/573-a352/R340-1/scripts/mutants.py /tmp/573-a352/head $EVIDENCE/round2-mutants.json /tmp/573-a352/round2-mutants-result.json` | 0 | 8.78 | `round2-mutants.result.json` |
| rtl-lint | `python3 scripts/lint_rtl.py --check` | 0 | 6.91 | `rtl-lint.result.json` |
| shipping-hash-comparison | `diff -u /tmp/573-a352/shipping-base.sha256 /tmp/573-a352/shipping-head.sha256` | 0 | 0.0 | `shipping-hash-comparison.result.json` |
| shipping-identity-base | `bash /tmp/573-a352/R341-1/scripts/shipping_identity.sh /tmp/573-a352/base /tmp/573-a352/shipping-base /tmp/573-a352/shipping-base.sha256` | 0 | 1.77 | `shipping-identity-base.result.json` |
| shipping-identity-head | `bash /tmp/573-a352/R341-1/scripts/shipping_identity.sh /tmp/573-a352/head /tmp/573-a352/shipping-head /tmp/573-a352/shipping-head.sha256` | 0 | 1.72 | `shipping-identity-head.result.json` |
| store-self-test | `python3 avdecc/gen_aem_store.py --self-test` | 0 | 0.11 | `store-self-test.result.json` |
| toc-anchors | `/tmp/573-a352/env/bin/python scripts/gen_toc.py --verify-anchors` | 0 | 1.67 | `toc-anchors.result.json` |
| toc | `/tmp/573-a352/env/bin/python scripts/gen_toc.py --check` | 0 | 2.62 | `toc.result.json` |

### Full builder limits

The full compiler-present bank returns rc 0. Its gate 11 utilization
calibration arm is NOT RUN because the pre-existing build report is absent.
The full compiler-absent bank also returns rc 0. Its gate 1b compiled
instruments are deliberately NOT RUN; gate 11 is likewise NOT RUN.
All three RV32 candidates were audited as hidden. The absent result
is not compiler evidence. No hardware or
physical calibration was run. These limits do not affect descriptor bytes.

### Historical script exception

`format_cap_length.py` is preserved byte-for-byte. It has no ConfigError
handler and assumes both 46 and 47 are accepted. At this head it prints the
accepted 46-format / 506-byte result, then exits 1 on the mandated named
47-format refusal. Consequently, the requested all-zero raw reviewer-script
exit condition cannot coexist with the required fix and unchanged script.
No failed return code is relabeled zero. `verify_round2.py` separately checks
this exact expected rejection, artifact identity, mutation kills, source
restoration and passing controls; its own result is rc 0.
The obsolete R-M8/R-M14 source patterns are likewise reported, not counted killed.

## Remaining responsibilities

Independent reviewers must re-cover Conformance, RTL, Robustness, Tests and Docs
at the final head and publish their own completion ledger.
The coordinator owns publication, hosted/local workflow evidence and any later
candidate-merge validation. No merge approval is requested or inferred here.
Processor-owned cap corrections remain in processor issue 60.
Evolution and model-history comparison remain with #495 and processor issue 38.
`PR-BODY.md` is a replacement draft only; the PR has not been edited.
Both full builder modes have finished. The final integrity record is
`final-integrity.json`; the prepared issue comment is `REVIEW-READY.md`.

## Final integrity

Head: `08374721d958b32ade38e7e62d25a7ccea215119`. Worktree and index: clean.
Pinned submodule revisions and tracked bytes are unchanged.
The five round-2 commit messages are single subjects without trailers.

[A352] REVIEW READY posted on [issue #573](https://github.com/kebag-logic/milan-fpga/issues/573#issuecomment-5854525373).
