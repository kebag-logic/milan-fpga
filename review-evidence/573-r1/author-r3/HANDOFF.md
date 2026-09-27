# Round 3 author handoff

Local assignment complete; ready for independent review.

Head: `8c956234699b5dec5e6c9aeada651be667974e9b`. Branch: `573-builder-model-refusals`.
Starting head: `08374721d958b32ade38e7e62d25a7ccea215119`.
Remote verified: `https://github.com/kebag-logic/milan-fpga.git`.
Working directory: `$LANES/573-builder-refusals`.

The author implements the [round-3 decision](https://github.com/kebag-logic/milan-fpga/issues/573#issuecomment-5854630094).
The internal [round-2 report](https://github.com/kebag-logic/milan-fpga/pull/585#issuecomment-5854625819)
and external [round-2 report](https://github.com/kebag-logic/milan-fpga/pull/585#issuecomment-5854626574)
were read with their full public evidence packets.

## Commits and change list

Each item group has one commit, with a one-line subject and no trailers.

| Group | Commit | Change and exact source location |
|---|---|---|
| F1 | `9e47e48c650ea70b2744696a10061d862f89a3bd` | `sw/builder/endstation_builder.py:1329`: reject non-string hex inputs with field name and quote instruction. `:4376`: a declared null pin refuses. `:4379`: format internal hash output as hex text before the reserved-ID guard. |
| F1 tests/docs | Same commit | `sw/builder/test_declarations.py:92`: eight field paths, actual YAML text, quoted prefixed/unprefixed digits, underscores, integer/octal spellings and non-string types. `sw/builder/README-parameters.md:152` and `docs/reference/PP_DESCRIPTOR_OWNERSHIP.md:198`: the string and quote contract. |
| F2 | `0d5820aee25e41d8bc9f83a36231c46986dfcfea` | `scripts/audit_pp_descriptors.py:210`: add the legal 46-entry/506-octet control; `:211`: label 47/514 as above the 2021 cap. `docs/reference/PP_DESCRIPTOR_OWNERSHIP.md:168`: report processor acceptance as PP60 defence-in-depth debt. |
| S1 | `8c956234699b5dec5e6c9aeada651be667974e9b` | `avdecc/aem_descriptors.py:187`: strict unsigned packing through the existing encoding, without a mask. `sw/builder/test_declarations.py:150`: exact bytes at zero and maximum; negative and overflow refusals. `docs/reference/PP_DESCRIPTOR_OWNERSHIP.md:38`: document the shared packing boundary. |

No tracked configuration was changed or refused. The STOP condition never occurred.
No HDL or submodule change was made. No push, pull-request edit, merge or hardware work was performed.

## Finding and disposition table

These are author dispositions, not reviewer approval or a completion ledger.

| Finding | Author disposition | Evidence and remaining ownership |
|---|---|---|
| R340-2 F1 / R341-2 F1 (MINOR: Conformance, Robustness, Tests, Docs) | Implemented | All eight `_eui64`/`_fmt64` input paths reject non-strings by field with a quote instruction. Both unchanged round-2 probes return zero; no accepted scalar changes its written hex value. A3-01 restores integer acceptance and is killed. |
| R340-2 F2 / R341-2 F2 (MINOR: Conformance, Docs; external report assigns Docs) | Implemented | Both legal 46/506 and invalid 47/514 packer probes remain accepted, accurately labelled. Parent declarations reject 47. `audit-l4-probes.json` retains the observed processor acceptance. PP60 owns its semantic refusal. |
| R341-2 S1, taken (SUGGESTION: Robustness) | Implemented | `be32` raises `struct.error` outside u32. A3-05 restores masking and is killed. Both artifact inventories remain identical. `be16` and `be64` were outside this assignment. |
| R340-2 S1, boolean part | Covered by assigned non-string rule | Boolean declarations are tested on all eight paths. The old mutation pattern no longer applies; current integer/boolean restoration is killed by A3-02. |
| R340-2 S1, null media-clock-source test suggestion | Optional, unchanged | Production refusal remains correct. The unchanged R2-17 PROBE mutation still survives the declaration suite; no clean coverage claim is made for that suggestion. |
| R340-2 S2, parameter-table expansion | Optional, not assigned | No expansion of the large design-document parameter table. Its primary identity discussion was already corrected in round 2. |
| Earlier round findings | Preserved | Format cap, listener floor/width, reserved-ID clauses, shadowed literals, hash endpoints and clock-source rules retain their controls. Both historical mutation banks and probes were rerun unchanged. |

The shared scalar tests decode arbitrary quoted hex digits independently of later field semantics.
`"1234567890123456"` is a valid 64-bit number but cannot be a MAC-48 destination or a supported AAF word.
Those fields use their own legal quoted controls through the complete loader, while all three assigned unquoted numeric spellings receive the quote refusal before their width/family checks.
All identity fields also resolve that quoted digit-only spelling through the complete loader.
The loader enforces YAML string type; a plain scalar already resolved as a string retains its hex value. Documentation tells users to quote values to avoid YAML numeric resolution.

## Standards evidence

Only cited pages were extracted with `pdftotext -f/-l` into `/tmp`.
IEEE 1722.1-2021 PDF page 64 supplies section 7.2; pages 73-74 supply Table 7-8.
The maximum descriptor is 508 octets, formats start at 138, and the count maximum is 46.
Milan v1.2 PDF pages 32 and 108 supply 5.3.3.1 and 5.6.2 respectively.
Both prohibit zero and all-ones model IDs. See [source hashes and extraction receipt](standards-receipt.txt).

## Mutation table

All mutation runs use an exact committed archive export under `/tmp`.
Every restored control returns zero, and every mutated source is restored byte-identically.
Old patterns absent from the new source are reported as not applied, never killed.
Current replacements cover the changed integer parser and hash-derived guard.

| Bank | Mutation | Outcome |
|---|---|---|
| Author round 3 | A3-01 restore integer acceptance | KILLED |
| Author round 3 | A3-02 restore integer and boolean acceptance | KILLED |
| Author round 3 | A3-03 ignore a declared null pin | KILLED |
| Author round 3 | A3-04 bypass hash-derived reserved ID guard | KILLED |
| Author round 3 | A3-05 restore u32 truncation | KILLED |
| Internal round 2 | R2-01 listener upper bound removed | KILLED |
| Internal round 2 | R2-02 upper bound admits 2^32 (off by one) | KILLED |
| Internal round 2 | R2-03 upper bound refuses 0xFFFFFFFF | KILLED |
| Internal round 2 | R2-04 upper bound applied to talkers too | KILLED |
| Internal round 2 | R2-05 shared field maximum one bit narrow | KILLED |
| Internal round 2 | R2-06 derived format cap raised by one | KILLED |
| Internal round 2 | R2-07 derived format cap lowered by one | KILLED |
| Internal round 2 | R2-08 descriptor maximum restated as 2013-era 516 | KILLED |
| Internal round 2 | R2-09 builder restates the old literal cap 47 | KILLED |
| Internal round 2 | R2-10 formats_offset shifted (layout and cap) | KILLED |
| Internal round 2 | R2-11 YAML int reinterpreted as hex digits again | NOT APPLIED: old source pattern absent |
| Internal round 2 | R2-12 bool admitted as an integer EUI-64 | NOT APPLIED: old source pattern absent |
| Internal round 2 | R2-13 shadowed literal no longer validated | KILLED |
| Internal round 2 | R2-14 hash-derived arm bypasses the guard | NOT APPLIED: old source pattern absent |
| Internal round 2 | R2-15 shadowed literal checked for width only | KILLED |
| Internal round 2 | R2-16 empty clock-source guard removed | KILLED |
| Internal round 2 | R2-17 empty guard matches only the empty list (null crashes) | SURVIVED (optional PROBE) |
| External round 2 | R2-M1 format cap raised by one at the use site | KILLED |
| External round 2 | R2-M2 descriptor maximum raised by one format (cap 47) | KILLED |
| External round 2 | R2-M3 2013 formats_offset 132 (cap 47, layout moved) | KILLED |
| External round 2 | R2-M4 listener upper bound removed | KILLED |
| External round 2 | R2-M5 upper bound exclusive (refuses 0xFFFFFFFF) | KILLED |
| External round 2 | R2-M6 upper bound raised by one (accepts 2^32) | KILLED |
| External round 2 | R2-M7 upper bound applied to talkers too | KILLED |
| External round 2 | R2-M8 field maximum derived as 2^32 | KILLED |
| External round 2 | R2-M9 empty clock-source refusal removed | KILLED |
| External round 2 | R2-M10 literal not validated when a pin is present | KILLED |
| External round 2 | R2-M11 hash-derived arm bypasses the guard | NOT APPLIED: old source pattern absent |
| External round 2 | R2-M12 YAML integer reparsed as hex text (round-1 behaviour) | NOT APPLIED: old source pattern absent |
| Internal historical | A573-01 zero guard removed | KILLED |
| Internal historical | A573-02 all-ones guard removed | KILLED |
| Internal historical | A573-03 literal validation removed | KILLED |
| Internal historical | A573-04 pin validation removed | KILLED |
| Internal historical | A574-05 listener floor guard removed | KILLED |
| Internal historical | A575-06 format count guard removed | KILLED |
| Internal historical | A575-07 AAF family guard removed | KILLED |
| Internal historical | A575-08 output count guard removed | KILLED |
| Internal historical | A575-09 output family guard removed | KILLED |
| Internal historical | A575-10 CRF word guard removed | KILLED |
| Internal historical | A575-11 CRF output word guard removed | KILLED |
| Internal historical | A576-12 INTERNAL guard removed | KILLED |
| Internal historical | A576-13 AAF output arm removed | KILLED |
| Internal historical | A576-14 CRF output arm removed | KILLED |
| Internal historical | R-F1a legal near-endpoint rejected | KILLED |
| Internal historical | R-F1b guard after literal only via hash path | KILLED |
| Internal historical | R-F2a floor off-by-one (<=) | KILLED |
| Internal historical | R-F2b floor lowered by one | KILLED |
| Internal historical | R-F2c integer-type check removed | KILLED |
| Internal historical | R-F2d guard applied to talkers instead | KILLED |
| Internal historical | R-F3a count off-by-one (>=) | KILLED |
| Internal historical | R-F3b declared list validated before completion | KILLED |
| Internal historical | R-F3c family compared on top nibble only | KILLED |
| Internal historical | R-F3d family checks current format only | KILLED |
| Internal historical | R-F3e CRF word checks only first entry | KILLED |
| Internal historical | R-F3f CRF input unvalidated | KILLED |
| Internal historical | R-F3g CRF output unvalidated | KILLED |
| Internal historical | R-F4a selection instead of availability | KILLED |
| Internal historical | R-F4b call site removed | KILLED |
| Internal historical | R-F4c call site reads listeners (equivalent in reachable space) | KILLED |
| External historical | R-M1 listener list validated before family derivation | KILLED |
| External historical | R-M2 floor lowered by one ns | KILLED |
| External historical | R-M3 floor made exclusive | KILLED |
| External historical | R-M4 integer type check removed | KILLED |
| External historical | R-M5 floor applied to talkers instead of listeners | KILLED |
| External historical | R-M6 family compare ignores the v bit | KILLED |
| External historical | R-M7 family compare only inspects the current format | KILLED |
| External historical | R-M8 count cap raised to 48 | NOT APPLIED: old source pattern absent |
| External historical | R-M9 AAF stream list validation call removed | KILLED |
| External historical | R-M10 CRF family check skipped (word check kept) | KILLED |
| External historical | R-M11 INTERNAL availability replaced by INTERNAL selection | KILLED |
| External historical | R-M12 output clock-source call removed from the loader | KILLED |
| External historical | R-M13 reserved-ID check on a value adjacent to all ones | KILLED |

The historical format-length script has no exception handler for the corrected 47-entry refusal.
Its unchanged raw exit is 1, retained in [raw output](format-reproducer-raw.log).
The [separate evidence check](check_format_reproducer.py) requires that exact refusal plus the accepted 46-entry/506-octet boundary and returns zero.
This expected raw nonzero is not presented as a zero exit from the historical script.

## SHA-256 tables against e0920d77

Baseline: `e0920d77162284d8da52ffaf13a973e451e44f90`.
Both versions were generated from committed archive exports, including each pinned submodule's archive.
Both unchanged reviewer inventories match: 85/85 generated artifacts and 80/80 CLI artifacts.
All five configurations, including all three Arty configurations, are accepted.
These are source/artifact checks, not bitstream or hardware qualification.

### Generated artifact inventory

The SHA-256 column gives the exact shared baseline/head hash; sizes match too.
Full independent inputs: [baseline](artifacts-base.json) and [head](artifacts-head.json).

| Configuration | Artifact | Bytes | Baseline = head SHA-256 |
|---|---|---:|---|
| arty_4x4 | `builder/adp_shape_defaults.svh` | 7562 | `f5539f2c29b0ab0440be88f5985ba41bebb508bede7095e5387a03721e50a418` |
| arty_4x4 | `builder/aecp_aem_rom.svh` | 52444 | `1cd6c92190c1b4f8c14783423a1618328e2fbefe286ab78edb00f96adb45f59d` |
| arty_4x4 | `builder/aem_overlay.json` | 11920 | `a9b9d900fb425e95e2b3728b47bc5c10b7d7f6b1027be1758f27b01b00b8f98c` |
| arty_4x4 | `builder/build_plan.md` | 11000 | `c040b872fa0102576fccf0f235cd9436722efd9f66cf885b220a5dfcd502d722` |
| arty_4x4 | `builder/cfg_adp_shape_svh` | 7562 | `f5539f2c29b0ab0440be88f5985ba41bebb508bede7095e5387a03721e50a418` |
| arty_4x4 | `builder/gptp_ucode.hex` | 13312 | `09f5d05defa759905f23630affc619d6af658e4c5f20aa0f63cc65f41317e651` |
| arty_4x4 | `builder/lwsrp_csr_defaults.svh` | 2183 | `90d4615e95883d5c1fdf5ce4eb8e716ac655114d8f0eb9e5579ec8e671bbfa88` |
| arty_4x4 | `builder/lwsrp_table.json` | 4084 | `90e1aa992317980e97ec42768d524e9b8af65e2279a31e1696f5f68254f05221` |
| arty_4x4 | `builder/lwsrp_table.svh` | 4288 | `36331d96c16b57ba3660a3183af58752195d94f2681d03ccfcf50003f227b222` |
| arty_4x4 | `builder/platform_shape.json` | 246 | `bbd040ba298a66ff0bd856f8f0b4e75c04c1831ba635a5b3ad756625ab8b0a28` |
| arty_4x4 | `builder/soc_params.json` | 589 | `fe552b1ec220f349b55cd499bc62680e9f7abf28397125cc457fd7cf63f61fb8` |
| arty_4x4 | `builder/sweep_opts` | 1209 | `f50e8a7f952d693de9c85e76caec5d77c252726cd6409eaee57e4a328efe8dcc` |
| arty_4x4 | `image/aem_desc.bin` | 10112 | `1b288e13ccbf03410c593a53bc22f4a68e3d289eef8a7f907e63bc98a51415ff` |
| arty_4x4 | `image/aem_desc.json` | 20716 | `0ea2e47927e0a0eff12d781d979a255c39a935b7f06e07366d9ab3ff368d4e3e` |
| arty_4x4 | `image/aem_desc.map` | 1311 | `09cf3da5a39730c1acedae4f09474c2d98d1aa17d8fa36f0238adc210fdaa571` |
| arty_4x4 | `store/aecp_aem_rom.svh` | 52444 | `1cd6c92190c1b4f8c14783423a1618328e2fbefe286ab78edb00f96adb45f59d` |
| arty_4x4 | `store/aem_rom.json` | 22180 | `b9ef1f60be8ed24ce5545a98f4f899d3078d06694a791caef8f69086ffc70b7b` |
| arty_8ch | `builder/adp_shape_defaults.svh` | 7836 | `41c02ad55f431ac15262d8a5db8e4a24945d375f217f7f0e552cd0b3f18cdd89` |
| arty_8ch | `builder/aecp_aem_rom.svh` | 71921 | `19dd262b93e56aeab1641f3d3e534fc7af372f1c2f8c1801e5a7895d1982ae34` |
| arty_8ch | `builder/aem_overlay.json` | 16978 | `87fc3c51e2fc5a49b91d67e05ea621449391619430ecfaef4cac5422b5b4b94e` |
| arty_8ch | `builder/build_plan.md` | 11003 | `1a93c95f35d176c5b52e03c1f0d5ccea7726c682a803948a5763029a509edf76` |
| arty_8ch | `builder/cfg_adp_shape_svh` | 7836 | `41c02ad55f431ac15262d8a5db8e4a24945d375f217f7f0e552cd0b3f18cdd89` |
| arty_8ch | `builder/gptp_ucode.hex` | 13312 | `09f5d05defa759905f23630affc619d6af658e4c5f20aa0f63cc65f41317e651` |
| arty_8ch | `builder/lwsrp_csr_defaults.svh` | 2183 | `f2519804843397b4bde6393e3be67f348e3b3ef6e73e62fef22b3a71b4ecf87f` |
| arty_8ch | `builder/lwsrp_table.json` | 4084 | `0e151e2854b3799281d19d01e67c27b04a53ca470a672ad27bc48f93ea840987` |
| arty_8ch | `builder/lwsrp_table.svh` | 4288 | `c7189e2e3dcf79a7fcd6c204674fca581d89aea327c77b65ea7aa57f38aa3e19` |
| arty_8ch | `builder/platform_shape.json` | 246 | `b818b72a035c5f73870925ffe208eda20292bedc629a399d5d31aa14160242ce` |
| arty_8ch | `builder/soc_params.json` | 589 | `7a10be52746259e11e1c43402cb8097ca5234e9b358fd6160af5c5e42673faff` |
| arty_8ch | `builder/sweep_opts` | 1209 | `8ea30219313f53e66c302861aa6e8824d0ded1f7f6ddc159a113ff79326a75f3` |
| arty_8ch | `image/aem_desc.bin` | 15360 | `2b5c008cf3a2ff1eca11ef5e24c5a2e391e97f25435854430e563758de516b9b` |
| arty_8ch | `image/aem_desc.json` | 31200 | `22d2815009a4d468faf1d48322b57e5ef2f6260d34219299810b7e5aafaced18` |
| arty_8ch | `image/aem_desc.map` | 1311 | `163d5a414e34591ad639c3682747a35c43db64dcb3d46cb06c77d4c33edb634a` |
| arty_8ch | `store/aecp_aem_rom.svh` | 71921 | `19dd262b93e56aeab1641f3d3e534fc7af372f1c2f8c1801e5a7895d1982ae34` |
| arty_8ch | `store/aem_rom.json` | 32868 | `de55410b93502c4ddfa3e1555efcde68b9e805833bf528969d78bcbd2af7ae45` |
| arty_current | `builder/adp_shape_defaults.svh` | 7089 | `54f350a99a0e6883f394858fe12457cffb4a1fea08ae23f5ba42c02636a46c98` |
| arty_current | `builder/aecp_aem_rom.svh` | 33428 | `d8365928caecf01dc79b3d9a75a6c56573669ad121d8cc04b42f44820601c999` |
| arty_current | `builder/aem_overlay.json` | 6238 | `12f48ab98be36408d6090158d5fc27341ca72d53217fcf892e097fbadab4e70e` |
| arty_current | `builder/build_plan.md` | 9105 | `4eb5e433433f1c3af1311a4585c9a80101178766c8aa9f7573a75d3e034167bf` |
| arty_current | `builder/cfg_adp_shape_svh` | 7089 | `54f350a99a0e6883f394858fe12457cffb4a1fea08ae23f5ba42c02636a46c98` |
| arty_current | `builder/gptp_ucode.hex` | 13312 | `09f5d05defa759905f23630affc619d6af658e4c5f20aa0f63cc65f41317e651` |
| arty_current | `builder/lwsrp_csr_defaults.svh` | 2187 | `d10ce5559b108f54800b8432b672a0d33379721bf2a4edf0058e185484f3881d` |
| arty_current | `builder/lwsrp_table.json` | 2274 | `dc4a200fa4dae047598419a78713677aefeab85b957808b9ec7284f2411a668f` |
| arty_current | `builder/lwsrp_table.svh` | 3826 | `df3c4fa0289d23deea8f8e688573faa1adbb12f8485a7b5613bd30b8b288f8e4` |
| arty_current | `builder/platform_shape.json` | 250 | `03328f238565f45f775a8fb17921a20ac4172d864b218e3703c23e185e678c99` |
| arty_current | `builder/soc_params.json` | 498 | `696350eee365adb614b78e445d6522569e73d0eaa555b4de6603319d45da59cb` |
| arty_current | `builder/sweep_opts` | 1143 | `969f765fe53c592a9fd4afcbb415733fd3ed1c2e367d788faf81e9f2e88ec6c7` |
| arty_current | `image/aem_desc.bin` | 5792 | `ac833c3ccde42a2d9a78b517d660b9f7da03c4b3d31227aa65dcaf9e8def6192` |
| arty_current | `image/aem_desc.json` | 11356 | `3c4b9440bccdc59198dacbc073fbb01671dec866d5adcf1b98225c8b6f822057` |
| arty_current | `image/aem_desc.map` | 1310 | `77dad531965096987d682f77e93f81e5b6f182eaae879fb43b084be8570bec4c` |
| arty_current | `store/aecp_aem_rom.svh` | 33428 | `d8365928caecf01dc79b3d9a75a6c56573669ad121d8cc04b42f44820601c999` |
| arty_current | `store/aem_rom.json` | 12722 | `1c25578eda1352acf7442ca90d0eb964709388ad23954e07f9bbc726004faa5a` |
| ax7101_1x1_tdm8 | `builder/adp_shape_defaults.svh` | 7199 | `eb03dfaa2f914f49b07c31ddcc62ebc4a64e839a466a3387650f25823afb1020` |
| ax7101_1x1_tdm8 | `builder/aecp_aem_rom.svh` | 40979 | `deea618d789b235c532edc47db08838afc7ffc2f74953f1a117d1fb2c7bd5d33` |
| ax7101_1x1_tdm8 | `builder/aem_overlay.json` | 7196 | `e148841ac36dbf3e6d6729c49c7c944ed5194adc75941ceb69e3af80b11e3621` |
| ax7101_1x1_tdm8 | `builder/build_plan.md` | 10825 | `203c4859f9557b4a250454fe9e0561706cc581708811988cd926edda9b942858` |
| ax7101_1x1_tdm8 | `builder/cfg_adp_shape_svh` | 7199 | `eb03dfaa2f914f49b07c31ddcc62ebc4a64e839a466a3387650f25823afb1020` |
| ax7101_1x1_tdm8 | `builder/gptp_ucode.hex` | 13312 | `78c8418a00b35cdae75c459c5269ca3892355507c4dc8af9eb2c29d81b87673b` |
| ax7101_1x1_tdm8 | `builder/lwsrp_csr_defaults.svh` | 2190 | `0e9df2d455d90782c87546dab4dd1fe7b5fb7f4bc81074e910ba71ddc7016d74` |
| ax7101_1x1_tdm8 | `builder/lwsrp_table.json` | 2289 | `61b2e71d9a40c61bfb0eaf884af6257b1b030e441c5f507f99720d0c18dad47d` |
| ax7101_1x1_tdm8 | `builder/lwsrp_table.svh` | 3832 | `8209fdee3cd744d24a066b76017f71f16d87f636c4470eb95e9f986dce550522` |
| ax7101_1x1_tdm8 | `builder/platform_shape.json` | 253 | `0325a3cc988f7f97b34997ef3ac53c6624edfc62b0bd4b5ffb42dc72894ddae7` |
| ax7101_1x1_tdm8 | `builder/soc_params.json` | 799 | `d5ec9866f86c339dc1c178c31c7800a359813660d9cbcc95e242e1e29b13c516` |
| ax7101_1x1_tdm8 | `builder/sweep_opts` | 1366 | `515d8610aa1a58f3b2e6b004d63eada43e826886ab420370ac9c45b63697670f` |
| ax7101_1x1_tdm8 | `image/aem_desc.bin` | 7352 | `9b077636b1d42aca660b16dce8eafa06f1e3cac842134e51ba65930d16214404` |
| ax7101_1x1_tdm8 | `image/aem_desc.json` | 14387 | `679d8286a0151b921aa1c6d38370c7c231020f1a5c75a85e565fce9fe1ba0c17` |
| ax7101_1x1_tdm8 | `image/aem_desc.map` | 1243 | `07151f7c4b493da8e1d3fea32a7e9755951d8e97e021e040ef2a9f3899cb7ede` |
| ax7101_1x1_tdm8 | `store/aecp_aem_rom.svh` | 40979 | `deea618d789b235c532edc47db08838afc7ffc2f74953f1a117d1fb2c7bd5d33` |
| ax7101_1x1_tdm8 | `store/aem_rom.json` | 15820 | `9469c9d0e79e8d949c2246437f8276a09098875ab2bf5e0b514256d40bc37f54` |
| ax7101_8x8 | `builder/adp_shape_defaults.svh` | 8449 | `26a61e545097a577f1b6bae2e15e92c867e4143a8f8ceb13e2abc21d03279333` |
| ax7101_8x8 | `builder/aecp_aem_rom.svh` | 86567 | `9f6963190256809964376e8747ebc3465d4b4831df01ec3d91c7e8892e46d755` |
| ax7101_8x8 | `builder/aem_overlay.json` | 20163 | `baef8bb15a57606b047e657c8ba50460d7f806983a0e08bf24432fc32435fb0c` |
| ax7101_8x8 | `builder/build_plan.md` | 15177 | `cda16a14dfa18d0021888a34e98af04c549c280adece820137712db93fb04f72` |
| ax7101_8x8 | `builder/cfg_adp_shape_svh` | 8449 | `26a61e545097a577f1b6bae2e15e92c867e4143a8f8ceb13e2abc21d03279333` |
| ax7101_8x8 | `builder/gptp_ucode.hex` | 13312 | `21e846a7e1989091e555486bbb571b6967eb014925f768dbca7d41124d1d3748` |
| ax7101_8x8 | `builder/lwsrp_csr_defaults.svh` | 2185 | `c9849c561b9aab3f682e2974ce1ba81443c2696a0c1a4e53d3975f2557c159c4` |
| ax7101_8x8 | `builder/lwsrp_table.json` | 6498 | `604cd1bae811ba9ff4c115db0009bb73f538223a90ca79466d28240cbc2e9415` |
| ax7101_8x8 | `builder/lwsrp_table.svh` | 4918 | `59bfe055ba72d4d9254163ba9fff232ad7edf7511235caf7aacb93f789ff10fa` |
| ax7101_8x8 | `builder/platform_shape.json` | 248 | `a08aef1e775ecd345a7f87157f4bf3eed28306250d49003d0c5231e714e6cf17` |
| ax7101_8x8 | `builder/soc_params.json` | 787 | `fe470422d9e29e0f9727deca18945d57975f4cb7d1e61722332205c411d99927` |
| ax7101_8x8 | `builder/sweep_opts` | 1359 | `734ba3acf384b296987156b2e676001fbe4e0558a49e1052e66009c3912d2fc2` |
| ax7101_8x8 | `image/aem_desc.bin` | 18288 | `193bf18736d23256c1b25d9af1bddb0721d95780fb36a14cf5f91476aff1a2d4` |
| ax7101_8x8 | `image/aem_desc.json` | 37534 | `50eaefa69bcad009479d1d7df3ced08f26b319d1a91dfe2ce659ef97c53620ad` |
| ax7101_8x8 | `image/aem_desc.map` | 1244 | `14d38a422d09d4b729032b19cfeb515756b30156c22f65df842184956ffd989f` |
| ax7101_8x8 | `store/aecp_aem_rom.svh` | 86567 | `9f6963190256809964376e8747ebc3465d4b4831df01ec3d91c7e8892e46d755` |
| ax7101_8x8 | `store/aem_rom.json` | 39074 | `8bd1f3f6e3d790d3c819741a787a5d04c5d9b4c37faf81011f1989a371fda476` |

### Independent CLI inventory

The CLI inventory includes generated headers and the store/image boundaries.
Full inputs: [baseline](shipping-base.sha256) and [head](shipping-head.sha256).

| Artifact | Baseline = head SHA-256 |
|---|---|
| `builder/endstation_arty_4x4/adp_shape_defaults.svh` | `f5539f2c29b0ab0440be88f5985ba41bebb508bede7095e5387a03721e50a418` |
| `builder/endstation_arty_4x4/aecp_aem_rom.svh` | `1cd6c92190c1b4f8c14783423a1618328e2fbefe286ab78edb00f96adb45f59d` |
| `builder/endstation_arty_4x4/aem_overlay.json` | `a9b9d900fb425e95e2b3728b47bc5c10b7d7f6b1027be1758f27b01b00b8f98c` |
| `builder/endstation_arty_4x4/build_plan.md` | `c040b872fa0102576fccf0f235cd9436722efd9f66cf885b220a5dfcd502d722` |
| `builder/endstation_arty_4x4/gptp_ucode.hex` | `09f5d05defa759905f23630affc619d6af658e4c5f20aa0f63cc65f41317e651` |
| `builder/endstation_arty_4x4/lwsrp_csr_defaults.svh` | `90d4615e95883d5c1fdf5ce4eb8e716ac655114d8f0eb9e5579ec8e671bbfa88` |
| `builder/endstation_arty_4x4/lwsrp_table.json` | `90e1aa992317980e97ec42768d524e9b8af65e2279a31e1696f5f68254f05221` |
| `builder/endstation_arty_4x4/lwsrp_table.svh` | `36331d96c16b57ba3660a3183af58752195d94f2681d03ccfcf50003f227b222` |
| `builder/endstation_arty_4x4/platform_shape.json` | `bbd040ba298a66ff0bd856f8f0b4e75c04c1831ba635a5b3ad756625ab8b0a28` |
| `builder/endstation_arty_4x4/soc_params.json` | `fe552b1ec220f349b55cd499bc62680e9f7abf28397125cc457fd7cf63f61fb8` |
| `builder/endstation_arty_8ch/adp_shape_defaults.svh` | `41c02ad55f431ac15262d8a5db8e4a24945d375f217f7f0e552cd0b3f18cdd89` |
| `builder/endstation_arty_8ch/aecp_aem_rom.svh` | `19dd262b93e56aeab1641f3d3e534fc7af372f1c2f8c1801e5a7895d1982ae34` |
| `builder/endstation_arty_8ch/aem_overlay.json` | `87fc3c51e2fc5a49b91d67e05ea621449391619430ecfaef4cac5422b5b4b94e` |
| `builder/endstation_arty_8ch/build_plan.md` | `1a93c95f35d176c5b52e03c1f0d5ccea7726c682a803948a5763029a509edf76` |
| `builder/endstation_arty_8ch/gptp_ucode.hex` | `09f5d05defa759905f23630affc619d6af658e4c5f20aa0f63cc65f41317e651` |
| `builder/endstation_arty_8ch/lwsrp_csr_defaults.svh` | `f2519804843397b4bde6393e3be67f348e3b3ef6e73e62fef22b3a71b4ecf87f` |
| `builder/endstation_arty_8ch/lwsrp_table.json` | `0e151e2854b3799281d19d01e67c27b04a53ca470a672ad27bc48f93ea840987` |
| `builder/endstation_arty_8ch/lwsrp_table.svh` | `c7189e2e3dcf79a7fcd6c204674fca581d89aea327c77b65ea7aa57f38aa3e19` |
| `builder/endstation_arty_8ch/platform_shape.json` | `b818b72a035c5f73870925ffe208eda20292bedc629a399d5d31aa14160242ce` |
| `builder/endstation_arty_8ch/soc_params.json` | `7a10be52746259e11e1c43402cb8097ca5234e9b358fd6160af5c5e42673faff` |
| `builder/endstation_arty_current/adp_shape_defaults.svh` | `54f350a99a0e6883f394858fe12457cffb4a1fea08ae23f5ba42c02636a46c98` |
| `builder/endstation_arty_current/aecp_aem_rom.svh` | `d8365928caecf01dc79b3d9a75a6c56573669ad121d8cc04b42f44820601c999` |
| `builder/endstation_arty_current/aem_overlay.json` | `12f48ab98be36408d6090158d5fc27341ca72d53217fcf892e097fbadab4e70e` |
| `builder/endstation_arty_current/build_plan.md` | `4eb5e433433f1c3af1311a4585c9a80101178766c8aa9f7573a75d3e034167bf` |
| `builder/endstation_arty_current/gptp_ucode.hex` | `09f5d05defa759905f23630affc619d6af658e4c5f20aa0f63cc65f41317e651` |
| `builder/endstation_arty_current/lwsrp_csr_defaults.svh` | `d10ce5559b108f54800b8432b672a0d33379721bf2a4edf0058e185484f3881d` |
| `builder/endstation_arty_current/lwsrp_table.json` | `dc4a200fa4dae047598419a78713677aefeab85b957808b9ec7284f2411a668f` |
| `builder/endstation_arty_current/lwsrp_table.svh` | `df3c4fa0289d23deea8f8e688573faa1adbb12f8485a7b5613bd30b8b288f8e4` |
| `builder/endstation_arty_current/platform_shape.json` | `03328f238565f45f775a8fb17921a20ac4172d864b218e3703c23e185e678c99` |
| `builder/endstation_arty_current/soc_params.json` | `696350eee365adb614b78e445d6522569e73d0eaa555b4de6603319d45da59cb` |
| `builder/endstation_ax7101_1x1_tdm8/adp_shape_defaults.svh` | `eb03dfaa2f914f49b07c31ddcc62ebc4a64e839a466a3387650f25823afb1020` |
| `builder/endstation_ax7101_1x1_tdm8/aecp_aem_rom.svh` | `deea618d789b235c532edc47db08838afc7ffc2f74953f1a117d1fb2c7bd5d33` |
| `builder/endstation_ax7101_1x1_tdm8/aem_overlay.json` | `e148841ac36dbf3e6d6729c49c7c944ed5194adc75941ceb69e3af80b11e3621` |
| `builder/endstation_ax7101_1x1_tdm8/build_plan.md` | `203c4859f9557b4a250454fe9e0561706cc581708811988cd926edda9b942858` |
| `builder/endstation_ax7101_1x1_tdm8/gptp_ucode.hex` | `78c8418a00b35cdae75c459c5269ca3892355507c4dc8af9eb2c29d81b87673b` |
| `builder/endstation_ax7101_1x1_tdm8/lwsrp_csr_defaults.svh` | `0e9df2d455d90782c87546dab4dd1fe7b5fb7f4bc81074e910ba71ddc7016d74` |
| `builder/endstation_ax7101_1x1_tdm8/lwsrp_table.json` | `61b2e71d9a40c61bfb0eaf884af6257b1b030e441c5f507f99720d0c18dad47d` |
| `builder/endstation_ax7101_1x1_tdm8/lwsrp_table.svh` | `8209fdee3cd744d24a066b76017f71f16d87f636c4470eb95e9f986dce550522` |
| `builder/endstation_ax7101_1x1_tdm8/platform_shape.json` | `0325a3cc988f7f97b34997ef3ac53c6624edfc62b0bd4b5ffb42dc72894ddae7` |
| `builder/endstation_ax7101_1x1_tdm8/soc_params.json` | `d5ec9866f86c339dc1c178c31c7800a359813660d9cbcc95e242e1e29b13c516` |
| `builder/endstation_ax7101_8x8/adp_shape_defaults.svh` | `26a61e545097a577f1b6bae2e15e92c867e4143a8f8ceb13e2abc21d03279333` |
| `builder/endstation_ax7101_8x8/aecp_aem_rom.svh` | `9f6963190256809964376e8747ebc3465d4b4831df01ec3d91c7e8892e46d755` |
| `builder/endstation_ax7101_8x8/aem_overlay.json` | `baef8bb15a57606b047e657c8ba50460d7f806983a0e08bf24432fc32435fb0c` |
| `builder/endstation_ax7101_8x8/build_plan.md` | `cda16a14dfa18d0021888a34e98af04c549c280adece820137712db93fb04f72` |
| `builder/endstation_ax7101_8x8/gptp_ucode.hex` | `21e846a7e1989091e555486bbb571b6967eb014925f768dbca7d41124d1d3748` |
| `builder/endstation_ax7101_8x8/lwsrp_csr_defaults.svh` | `c9849c561b9aab3f682e2974ce1ba81443c2696a0c1a4e53d3975f2557c159c4` |
| `builder/endstation_ax7101_8x8/lwsrp_table.json` | `604cd1bae811ba9ff4c115db0009bb73f538223a90ca79466d28240cbc2e9415` |
| `builder/endstation_ax7101_8x8/lwsrp_table.svh` | `59bfe055ba72d4d9254163ba9fff232ad7edf7511235caf7aacb93f789ff10fa` |
| `builder/endstation_ax7101_8x8/platform_shape.json` | `a08aef1e775ecd345a7f87157f4bf3eed28306250d49003d0c5231e714e6cf17` |
| `builder/endstation_ax7101_8x8/soc_params.json` | `fe470422d9e29e0f9727deca18945d57975f4cb7d1e61722332205c411d99927` |
| `image/endstation_arty_4x4/aem_desc.bin` | `1b288e13ccbf03410c593a53bc22f4a68e3d289eef8a7f907e63bc98a51415ff` |
| `image/endstation_arty_4x4/aem_desc.json` | `0ea2e47927e0a0eff12d781d979a255c39a935b7f06e07366d9ab3ff368d4e3e` |
| `image/endstation_arty_4x4/aem_desc.map` | `09cf3da5a39730c1acedae4f09474c2d98d1aa17d8fa36f0238adc210fdaa571` |
| `image/endstation_arty_8ch/aem_desc.bin` | `2b5c008cf3a2ff1eca11ef5e24c5a2e391e97f25435854430e563758de516b9b` |
| `image/endstation_arty_8ch/aem_desc.json` | `22d2815009a4d468faf1d48322b57e5ef2f6260d34219299810b7e5aafaced18` |
| `image/endstation_arty_8ch/aem_desc.map` | `163d5a414e34591ad639c3682747a35c43db64dcb3d46cb06c77d4c33edb634a` |
| `image/endstation_arty_current/aem_desc.bin` | `ac833c3ccde42a2d9a78b517d660b9f7da03c4b3d31227aa65dcaf9e8def6192` |
| `image/endstation_arty_current/aem_desc.json` | `3c4b9440bccdc59198dacbc073fbb01671dec866d5adcf1b98225c8b6f822057` |
| `image/endstation_arty_current/aem_desc.map` | `77dad531965096987d682f77e93f81e5b6f182eaae879fb43b084be8570bec4c` |
| `image/endstation_ax7101_1x1_tdm8/aem_desc.bin` | `9b077636b1d42aca660b16dce8eafa06f1e3cac842134e51ba65930d16214404` |
| `image/endstation_ax7101_1x1_tdm8/aem_desc.json` | `679d8286a0151b921aa1c6d38370c7c231020f1a5c75a85e565fce9fe1ba0c17` |
| `image/endstation_ax7101_1x1_tdm8/aem_desc.map` | `07151f7c4b493da8e1d3fea32a7e9755951d8e97e021e040ef2a9f3899cb7ede` |
| `image/endstation_ax7101_8x8/aem_desc.bin` | `193bf18736d23256c1b25d9af1bddb0721d95780fb36a14cf5f91476aff1a2d4` |
| `image/endstation_ax7101_8x8/aem_desc.json` | `50eaefa69bcad009479d1d7df3ced08f26b319d1a91dfe2ce659ef97c53620ad` |
| `image/endstation_ax7101_8x8/aem_desc.map` | `14d38a422d09d4b729032b19cfeb515756b30156c22f65df842184956ffd989f` |
| `store/endstation_arty_4x4/aecp_aem_rom.svh` | `1cd6c92190c1b4f8c14783423a1618328e2fbefe286ab78edb00f96adb45f59d` |
| `store/endstation_arty_4x4/aem_rom.json` | `b9ef1f60be8ed24ce5545a98f4f899d3078d06694a791caef8f69086ffc70b7b` |
| `store/endstation_arty_8ch/aecp_aem_rom.svh` | `19dd262b93e56aeab1641f3d3e534fc7af372f1c2f8c1801e5a7895d1982ae34` |
| `store/endstation_arty_8ch/aem_rom.json` | `de55410b93502c4ddfa3e1555efcde68b9e805833bf528969d78bcbd2af7ae45` |
| `store/endstation_arty_current/aecp_aem_rom.svh` | `d8365928caecf01dc79b3d9a75a6c56573669ad121d8cc04b42f44820601c999` |
| `store/endstation_arty_current/aem_rom.json` | `1c25578eda1352acf7442ca90d0eb964709388ad23954e07f9bbc726004faa5a` |
| `store/endstation_ax7101_1x1_tdm8/aecp_aem_rom.svh` | `deea618d789b235c532edc47db08838afc7ffc2f74953f1a117d1fb2c7bd5d33` |
| `store/endstation_ax7101_1x1_tdm8/aem_rom.json` | `9469c9d0e79e8d949c2246437f8276a09098875ab2bf5e0b514256d40bc37f54` |
| `store/endstation_ax7101_8x8/aecp_aem_rom.svh` | `9f6963190256809964376e8747ebc3465d4b4831df01ec3d91c7e8892e46d755` |
| `store/endstation_ax7101_8x8/aem_rom.json` | `8bd1f3f6e3d790d3c819741a787a5d04c5d9b4c37faf81011f1989a371fda476` |
| `tracked/endstation_arty_4x4/adp_shape_defaults.svh` | `eb03dfaa2f914f49b07c31ddcc62ebc4a64e839a466a3387650f25823afb1020` |
| `tracked/endstation_arty_8ch/adp_shape_defaults.svh` | `eb03dfaa2f914f49b07c31ddcc62ebc4a64e839a466a3387650f25823afb1020` |
| `tracked/endstation_arty_current/adp_shape_defaults.svh` | `eb03dfaa2f914f49b07c31ddcc62ebc4a64e839a466a3387650f25823afb1020` |
| `tracked/endstation_ax7101_1x1_tdm8/adp_shape_defaults.svh` | `eb03dfaa2f914f49b07c31ddcc62ebc4a64e839a466a3387650f25823afb1020` |
| `tracked/endstation_ax7101_8x8/adp_shape_defaults.svh` | `eb03dfaa2f914f49b07c31ddcc62ebc4a64e839a466a3387650f25823afb1020` |

## Gate table

Commands ran in the foreground, without output pipelines. Each gate retains its actual exit.
The two builder modes and focused gates use the physical `/data` candidate path.
Reviewer mutations and artifact generation use committed archive exports.
`builder_absent.py` hides only the three RV32 compiler candidates in process; no compiler is modified.
The complete builder entry point runs in both modes.
The pinned Markdown dependencies are installed only in disposable scratch.

| Gate | Exit | Seconds | Evidence | Exact command |
|---|---:|---:|---|---|
| reviewer-round2-probes | 0 | 0.57 | [reviewer-round2-probes.log](reviewer-round2-probes.log) | `python3 -B /tmp/573-a355/reviews/R340-2/scripts/round2_probes.py /tmp/573-a355/head $MANAGEMENT/2026-09-23/573-a355/round2-probes.json` |
| reviewer-scalar-spellings | 0 | 0.41 | [reviewer-scalar-spellings.log](reviewer-scalar-spellings.log) | `python3 -B /tmp/573-a355/reviews/R341-2/scripts/scalar_spelling_probe.py /tmp/573-a355/head` |
| reviewer-internal-mutants | 0 | 24.06 | [reviewer-internal-mutants.log](reviewer-internal-mutants.log) | `python3 -B /tmp/573-a355/reviews/R340-2/scripts/mutants_r2.py /tmp/573-a355/head /tmp/573-a355/reviews/R340-2/scripts/mutant_cases_r2.json $MANAGEMENT/2026-09-23/573-a355/internal-mutants.json` |
| reviewer-external-mutants | 0 | 16.39 | [reviewer-external-mutants.log](reviewer-external-mutants.log) | `python3 -B /tmp/573-a355/reviews/R341-2/scripts/run_mutants_r2.py /tmp/573-a355/head /tmp/573-a355/reviews/R341-2/scripts/reviewer_mutants_r2.json` |
| artifacts-base | 0 | 1.12 | [artifacts-base.log](artifacts-base.log) | `python3 -B /tmp/573-a355/reviews/R340-2/scripts/r340-1/hash_artifacts.py /tmp/573-a355/base $MANAGEMENT/2026-09-23/573-a355/artifacts-base.json` |
| shipping-base | 0 | 1.72 | [shipping-base.log](shipping-base.log) | `bash /tmp/573-a355/reviews/R340-2/scripts/r341-1/shipping_identity.sh /tmp/573-a355/base /tmp/573-a355/shipping-base $MANAGEMENT/2026-09-23/573-a355/shipping-base.sha256` |
| artifacts-head | 0 | 1.12 | [artifacts-head.log](artifacts-head.log) | `python3 -B /tmp/573-a355/reviews/R340-2/scripts/r340-1/hash_artifacts.py /tmp/573-a355/head $MANAGEMENT/2026-09-23/573-a355/artifacts-head.json` |
| shipping-head | 0 | 1.67 | [shipping-head.log](shipping-head.log) | `bash /tmp/573-a355/reviews/R340-2/scripts/r341-1/shipping_identity.sh /tmp/573-a355/head /tmp/573-a355/shipping-head $MANAGEMENT/2026-09-23/573-a355/shipping-head.sha256` |
| author-mutants | 0 | 4.77 | [author-mutants.log](author-mutants.log) | `python3 -B /tmp/573-a355/reviews/R340-2/scripts/mutants_r2.py /tmp/573-a355/head $MANAGEMENT/2026-09-23/573-a355/author-mutation-cases.json $MANAGEMENT/2026-09-23/573-a355/author-mutants.json` |
| historical-internal-probes | 0 | 0.67 | [historical-internal-probes.log](historical-internal-probes.log) | `python3 -B /tmp/573-a355/reviews/R340-2/scripts/r340-1/probes.py /tmp/573-a355/head $MANAGEMENT/2026-09-23/573-a355/historical-probes.json` |
| historical-buffer-wrap | 0 | 0.26 | [historical-buffer-wrap.log](historical-buffer-wrap.log) | `python3 -B /tmp/573-a355/reviews/R340-2/scripts/r340-1/buffer_wrap_probe.py /tmp/573-a355/head` |
| historical-bypass-probes | 0 | 0.41 | [historical-bypass-probes.log](historical-bypass-probes.log) | `python3 -B /tmp/573-a355/reviews/R340-2/scripts/r341-1/bypass_probes.py /tmp/573-a355/head` |
| historical-format-boundary | 0 | 0.21 | [historical-format-boundary.log](historical-format-boundary.log) | `python3 -B $MANAGEMENT/2026-09-23/573-a355/check_format_reproducer.py` |
| declarations | 0 | 3.07 | [declarations.log](declarations.log) | `python3 -B sw/builder/test_declarations.py` |
| descriptor-audit | 0 | 0.46 | [descriptor-audit.log](descriptor-audit.log) | `python3 scripts/audit_pp_descriptors.py --output /tmp/573-a355/audit-head.json` |
| aem-store-selftest | 0 | 0.06 | [aem-store-selftest.log](aem-store-selftest.log) | `python3 avdecc/gen_aem_store.py --self-test` |
| rtl-lint | 0 | 6.46 | [rtl-lint.log](rtl-lint.log) | `python3 scripts/lint_rtl.py --check` |
| python-idiom | 0 | 3.27 | [python-idiom.log](python-idiom.log) | `python3 scripts/check_py_idiom.py` |
| naming | 0 | 0.47 | [naming.log](naming.log) | `python3 scripts/measure_naming.py --check` |
| docs-git | 0 | 4.17 | [docs-git.log](docs-git.log) | `python3 scripts/docs_check.py` |
| historical-internal-mutants | 0 | 48.64 | [historical-internal-mutants.log](historical-internal-mutants.log) | `python3 -B /tmp/573-a355/reviews/R340-2/scripts/r340-1/mutants.py /tmp/573-a355/head /tmp/573-a355/reviews/R340-2/scripts/r340-1/mutant_cases.json $MANAGEMENT/2026-09-23/573-a355/historical-internal-mutants.json` |
| docs-no-git | 0 | 4.17 | [docs-no-git.log](docs-no-git.log) | `env GIT_DIR=/dev/null python3 scripts/docs_check.py` |
| em-dash | 0 | 2.97 | [em-dash.log](em-dash.log) | `/tmp/573-a355/venv/bin/python scripts/check_em_dash.py --base e0920d77` |
| doc-style | 0 | 0.06 | [doc-style.log](doc-style.log) | `python3 scripts/check_doc_style.py` |
| toc | 0 | 2.47 | [toc.log](toc.log) | `/tmp/573-a355/venv/bin/python scripts/gen_toc.py --check` |
| anchors | 0 | 1.62 | [anchors.log](anchors.log) | `/tmp/573-a355/venv/bin/python scripts/gen_toc.py --verify-anchors` |
| doc-paths | 0 | 0.06 | [doc-paths.log](doc-paths.log) | `python3 scripts/check_doc_paths.py` |
| diff-worktree | 0 | 0.02 | [diff-worktree.log](diff-worktree.log) | `git diff --check` |
| diff-branch | 0 | 0.01 | [diff-branch.log](diff-branch.log) | `git diff --check e0920d77 HEAD` |
| historical-external-mutants | 0 | 19.15 | [historical-external-mutants.log](historical-external-mutants.log) | `python3 -B /tmp/573-a355/reviews/R340-2/scripts/r341-1/run_mutants.py /tmp/573-a355/head /tmp/573-a355/reviews/R340-2/scripts/r341-1/reviewer_mutants.json` |
| archive-integrity | 0 | 0.16 | [archive-integrity.log](archive-integrity.log) | `bash /tmp/573-a355/reviews/R340-2/scripts/clone_integrity.sh /tmp/573-a355/head 8c956234699b5dec5e6c9aeada651be667974e9b 16767fc674e46e4f210feaf6e21dbeb096a76fe3` |
| builder-present | 0 | 759.75 | [builder-present.log](builder-present.log) | `python3 -u -B sw/builder/test_builder.py --require-rv32` |
| builder-absent | 0 | 550.85 | [builder-absent.log](builder-absent.log) | `python3 -u -B $MANAGEMENT/2026-09-23/573-a355/builder_absent.py` |
| evidence-summary | 0 | 0.03 | [evidence-summary.log](evidence-summary.log) | `python3 $MANAGEMENT/2026-09-23/573-a355/check_evidence.py` |

The gate receipt also records working directories, complete-log sizes and SHA-256 hashes: [gate-results.jsonl](gate-results.jsonl).
Logs above 190000 bytes are retained as bounded excerpts; complete logs stay in `/tmp/573-a355/logs`.
No toolchain, environment, tree export, installed package or file over 200 KB is stored in this output directory.

## Reviewer script provenance and reproduction

The 17 extracted public script/case files are byte-identical to the evidence branch.
Their full commit and SHA-256 values are in [reviewer-script-sha256.tsv](reviewer-script-sha256.tsv).
Retrieve them with `git fetch origin 573-review-evidence` and `git show FETCH_HEAD:<path>`.
Use `git archive` of the candidate and baseline, with pinned submodule archives under their paths.
Archive-local Git metadata and a private index support the scripts' Git queries and temporary restoration; no implementation checkout or shared index is used for mutation.
The unchanged integrity script proves candidate archive bytes, index and tree agree after every bank.

The runners are [run_public_evidence.py](run_public_evidence.py), [run_additional_evidence.py](run_additional_evidence.py),
[run_local_gates.py](run_local_gates.py) and [run_gate.py](run_gate.py).
The current mutation definitions are [author-mutation-cases.json](author-mutation-cases.json).

## Limits and next steps

The absent compiler mode intentionally stands down compiler-dependent instruments.
The builder's unavailable utilization-calibration report remains an explicit skip.
No hardware result is claimed. The scoped lint gate is separate from exhaustive simulation/synthesis qualification.
No hosted or local workflow replica is run for this unpushed head.
The maintainer owns publication, exact-head workflow evidence and candidate-merge validation.
The two independent reviewers must re-cover all five lenses, including RTL because `be32` changed.
No review verdict or reviewer-owned completion ledger is supplied by the author.
The replacement body is [PR-BODY.md](PR-BODY.md); it is prepared but not applied to the PR.
After posting the prepared `[A355] REVIEW READY` comment on issue #573, this author session stops.
