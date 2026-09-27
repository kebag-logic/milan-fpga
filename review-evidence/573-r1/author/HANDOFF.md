# [A347] Parent shipping-model refusals F1-F4

All requested local gates passed; ready for the assigned independent reviewers.

Head: `4f746408a15f494c4b30bdc9add6d7295309dff9`. Base: `e0920d77162284d8da52ffaf13a973e451e44f90`.
Branch: `573-builder-model-refusals`.
Physical worktree: `$LANES/573-builder-refusals`.
Origin confirmed: `https://github.com/kebag-logic/milan-fpga.git`.
Assignment: https://github.com/kebag-logic/milan-fpga/issues/573#issuecomment-5853854503.
Executor: [A347]. Independent reviewers: [R340] and [R341].

All five tracked configurations remain accepted. No STOP condition occurred.
All 85 generated artifacts have identical before/after sizes and SHA-256 hashes.
No tracked configuration, submodule, hardware, or deployment changes were made.
No push, pull request mutation, merge, or other checkout was performed.

## Change list

- `sw/builder/endstation_builder.py:1341`: reserved model-ID refusal; literal and pin call sites at 4367/4371.
- `sw/builder/endstation_builder.py:1382`: per-listener integer buffer floor; called for every stream at 1501.
- `sw/builder/endstation_builder.py:1393`: final format count and family validation; AAF call at 1460 includes derived listener entries.
- `sw/builder/endstation_builder.py:1410`: exact Milan CRF word; both clocking inputs call it at 3869/3872.
- `sw/builder/endstation_builder.py:4214`: output INTERNAL availability; called before stream construction at 4226.
- `sw/builder/test_declarations.py:34`: model-ID controls and packed ENTITY/ADP equality; buffer tests at 68; AAF tests at 90; CRF tests at 118; source tests at 140.
- `sw/builder/test_declarations.py:207`: existing declaration entry executes all new tests; the full builder already calls this entry.
- `sw/builder/README-parameters.md:117`: user-visible clock, format and buffer rules; identity endpoints at 146.
- `docs/reference/PP_DESCRIPTOR_OWNERSHIP.md:239`: F1-F4 enforcement and evidence; L4/L6/L9 and reachable YAML probe rows updated consistently.

## Per-issue evidence

| Issue | Rule | Clause | Where enforced | Legal control | Refusals | Mutant result |
|---|---|---|---|---|---|---|
| #573 / F1 | Reserved model-ID endpoints | Milan v1.2 5.3.1; IEEE 1722.1-2021 6.2.2.8 and Table 7-2 | `_model_id`, literal/pin resolution | 1, max-minus-one and shipping ID on both forms; packed ENTITY and ADP boot constants agree | Zero and all ones on both forms | 4/4 killed: each endpoint guard, literal call, pin call |
| #574 / F2 | Every listener buffer at least 2126000 ns | Milan v1.2 5.3.3.4 | `_stream_buffer_ns`, every `_streams` row | 2126000 and 2126001 at all eight listener indices | 2125999, zero, negative, fraction, string and boolean at all eight indices | 1/1 killed: floor guard removed |
| #575 / F3 | At most 47 final formats; homogeneous declared family; exact CRF word | IEEE 1722.1-2021 Table 7-8; Milan 5.3.3.4, 6.4, 7.3.2 Table 7.1 | `_validate_stream_formats`, `_crf_format` | AAF controls and 47 final entries at every input/output index; both CRF directions accept 0x041060010000BB80 | 48 final/declared entries, mixed families in either order, wrong family/version, CRF word ending BB81 | 6/6 killed: count/family checks on inputs and outputs; exact CRF word checks in both directions |
| #576 / F4 | Any AAF/CRF output requires INTERNAL available | Milan v1.2 5.3.3.6 | `_validate_output_clock_sources` | INTERNAL+CRF with either selected; CRF-only input clock loading | AAF output without INTERNAL; AAF+CRF outputs without INTERNAL; isolated CRF-output obligation | 3/3 killed: complete guard, AAF arm, CRF arm |

Each invalid fixture requires `ConfigError` and its own field/rule text.
Production refusals are explicit exceptions, not assertions.
All numerical oracles in the new tests are independent specification boundaries.
Count controls repeat formats to isolate list cardinality; they do not claim new media modes.
The count bound applies after listener family completion, so 47 declared AAF entries
requiring one derived entry are refused as 48 final entries.

Input-only behavior is deliberately measured at the existing clock-loading boundary.
The complete product YAML loader still requires nonempty AAF directions.
The new output check imposes no INTERNAL requirement when there are no outputs.
Clock source selection may remain CRF when INTERNAL is available.

Only parent configuration validation changed. Generic processor packing remains unchanged.
Model evolution stays with #495. F5-F8 and other ownership-matrix debt remain separate.
`docs/spec-refs.md` was absent at the assigned base and in the processor documentation.
Clause references came from the ownership matrix, processor memory-map section 3.1,
integrator guide, and existing clause-backed builder/descriptor documentation.
No specification PDF or private transcript was read.

## Commits

- `638182177e3e8b3fad502389a4efa90d97771e20 Refuse reserved literal and pinned model IDs (#573)`
- `556901b5f4048654c7259f7626cba3d0ac31ebc0 Validate every declared listener buffer against the Milan floor (#574)`
- `82fa859b147b62bf2a943f21654a5bf5bb767d8f Bound stream format counts and enforce AAF and Milan CRF families (#575)`
- `4f746408a15f494c4b30bdc9add6d7295309dff9 Require INTERNAL clock availability for every stream output (#576)`

## Gate table

Every command ran in the foreground from the physical worktree, without a pipeline.
`run_gate.py` applies a 7200-second deadline and records the actual exit status.
The Markdown gates use the already-installed pinned renderer environment.
An initial system-interpreter em-dash attempt lacked that dependency; its rerun passed.

| Gate | Exact command | Exit status | Seconds | Evidence |
|---|---|---|---|---|
| builder-present | `python3 sw/builder/test_builder.py --require-rv32` | 0 | 763.1 | `builder-present.log` |
| builder-absent | `python3 $MANAGEMENT/2026-09-23/573-a347/builder_absent.py` | 0 | 558.09 | `builder-absent.log` |
| declarations | `python3 sw/builder/test_declarations.py` | 0 | 1.92 | `declarations.log` |
| descriptor-audit | `python3 scripts/audit_pp_descriptors.py --output /tmp/573-descriptor-audit.json` | 0 | 1.49 | `descriptor-audit.log` |
| store-self-test | `python3 avdecc/gen_aem_store.py --self-test` | 0 | 0.11 | `store-self-test.log` |
| rtl-lint | `python3 scripts/lint_rtl.py --check` | 0 | 7.27 | `rtl-lint.log` |
| python-idiom | `python3 scripts/check_py_idiom.py` | 0 | 6.58 | `python-idiom.log` |
| naming | `python3 scripts/measure_naming.py --check` | 0 | 1.69 | `naming.log` |
| docs-git | `python3 scripts/docs_check.py` | 0 | 4.17 | `docs-git.log` |
| docs-no-git | `env GIT_DIR=/dev/null python3 scripts/docs_check.py` | 0 | 4.87 | `docs-no-git.log` |
| em-dash | `$VALIDATION_TOOLS/md-venv-40cdefe08ebd/bin/python scripts/check_em_dash.py --base e0920d77` | 0 | 3.07 | `em-dash.log` |
| doc-style | `python3 scripts/check_doc_style.py` | 0 | 0.06 | `doc-style.log` |
| toc | `$VALIDATION_TOOLS/md-venv-40cdefe08ebd/bin/python scripts/gen_toc.py --check` | 0 | 2.57 | `toc.log` |
| toc-anchors | `$VALIDATION_TOOLS/md-venv-40cdefe08ebd/bin/python scripts/gen_toc.py --verify-anchors` | 0 | 1.62 | `toc-anchors.log` |
| doc-paths | `python3 scripts/check_doc_paths.py` | 0 | 0.11 | `doc-paths.log` |
| diff-whitespace | `git diff --check e0920d77 HEAD` | 0 | 0.02 | `diff-whitespace.log` |

Compiler-absent mode runs the entire `test_builder.py` main entry via `runpy`.
`builder_absent.py` uses the existing compiler audit to hide only its three RV32
candidates. All other subprocesses execute normally; no host tool or SDK changes.
It verifies that all three candidates were hidden after the complete entry returns.
Compiler-present mode invokes the full entry directly with `--require-rv32`.

The filesystem-mode documentation gate records its expected Git-inventory parity skip.
Builder skip details, if any, are quoted below from the actual final verdicts.

### builder-present recorded evidence limits

```text
1 GATE ARM(S) DID NOT RUN - this verdict does not cover them:
  - [gate 11] real report not on disk ($WORKSPACE_HOME/litex-milan/work/build_arty_eto_milanfinal48/gateware/digilent_arty_utilization_place.rpt) - the calibration gate needs the mf48 build tree
ALL GATES PASS EXCEPT 1 NOT RUN
```

### builder-absent recorded evidence limits

```text
2 GATE ARM(S) DID NOT RUN - this verdict does not cover them:
  - [gate 1b] the compiled CSR-address census: cc is not the RV32 target and no flag set here drives it as one, so the census-only mutations, the phase-2 splice compile proofs and the census of the shipping firmware itself did not run -- and neither did the RESOLVING half (#153), which reads the same compile: no resolved store census, no proof that the verdict test dominates the enable writes, and no proof that the CRC-equality edge dominates every non-zero verdict or that the CRC was taken over MILAN_AEM_DESC_BASE, so its mutations did not run either. THE THREE INSTRUMENTS THE TEXT RULES RETIRED BY #408 AND #409 REST ON ARE DOWN WITH THEM -- the -E comparison of the boot path this gate reads against the one the compiler compiles, the -H include-resolution measurement and the resolved store census -- so on this runner NOTHING refuses what those instruments carry: a token-joining splice or a ## paste OUTSIDE the six boot-path bodies, a file beside the firmware, a cast, store or asm the resolver would place in the window, and the COMPILER half of the retired conditional-reach ban -- an arm only one build compiles whose defect no text rule reads, such as `0 &&` in the choke point's verdict test, is graded here by the text rules alone, which do not refuse it -- and every mutation pinned on those instruments is SKIPPED, not counted. WHAT STILL GRADED is every text rule that survives: the splice and ## bans KEPT inside the six boot-path bodies, one #define per name (which is what refuses a read hidden in a second definition of the identity magic), the macro-body rule, the closed-grammar subset check S (the character allowlist, then the literal, digraph, trigraph, $, universal-character-name, __has_include, header-name, _Pragma and unterminated-comment refusals), read on the whole firmware before any reader, the directive readers as the two lexer corpora and the character-closure table recorded them (not re-measured), and the per-selection grading of each conditional (its text half); and the hosted builder jobs require this compiler
  - [gate 11] real report not on disk ($WORKSPACE_HOME/litex-milan/work/build_arty_eto_milanfinal48/gateware/digilent_arty_utilization_place.rpt) - the calibration gate needs the mf48 build tree
ALL GATES PASS EXCEPT 2 NOT RUN
ABSENT MODE: all three RV32 compiler candidates hidden; full builder entry completed
```

## Removed-check evidence

`mutations.py` replaces one exact production guard per case, runs the existing
`test_declarations.py` entry, requires its discriminating assertion failure,
and restores the source in a `finally` block. No changed mutant source remains.
`mutations.json` contains the exact changes and required failure diagnostics.
The final campaign records the exact reviewed head in every result row.
Reproduce per issue: `python3 mutations.py 573` (then 574, 575, 576), from this bundle.

| Issue | Mutation | Result | Diagnostic |
|---|---|---|---|
| #573 | zero guard removed | KILLED, rc 1 | `AssertionError: accepted invalid entity.entity_model_id: must not be zero or all ones` |
| #573 | all-ones guard removed | KILLED, rc 1 | `AssertionError: accepted invalid entity.entity_model_id: must not be zero or all ones` |
| #573 | literal validation removed | KILLED, rc 1 | `AssertionError: accepted invalid entity.entity_model_id: must not be zero or all ones` |
| #573 | pin validation removed | KILLED, rc 1 | `AssertionError: accepted invalid entity.model_id_pin: must not be zero or all ones` |
| #574 | listener floor guard removed | KILLED, rc 1 | `AssertionError: accepted invalid streams.listeners[0].buffer_length_ns: listener buffer floor` |
| #575 | format count guard removed | KILLED, rc 1 | `AssertionError: accepted invalid streams.listeners[0].formats: format count` |
| #575 | AAF family guard removed | KILLED, rc 1 | `AssertionError: accepted invalid streams.listeners[0].formats: must contain only AAF formats` |
| #575 | output count guard removed | KILLED, rc 1 | `AssertionError: accepted invalid streams.talkers[0].formats: format count` |
| #575 | output family guard removed | KILLED, rc 1 | `AssertionError: accepted invalid streams.talkers[0].formats: must contain only AAF formats` |
| #575 | CRF word guard removed | KILLED, rc 1 | `AssertionError: accepted invalid clocking.crf_format: CRF format must be` |
| #575 | CRF output word guard removed | KILLED, rc 1 | `AssertionError: accepted invalid clocking.crf_output.format: CRF format must be` |
| #576 | INTERNAL guard removed | KILLED, rc 1 | `AssertionError: accepted invalid clocking.media_clock_sources: requires INTERNAL` |
| #576 | AAF output arm removed | KILLED, rc 1 | `AssertionError: accepted invalid clocking.media_clock_sources: requires INTERNAL` |
| #576 | CRF output arm removed | KILLED, rc 1 | `AssertionError: ('clocking.media_clock_sources', 'requires INTERNAL', 'streams.talkers: needs at least one talker stream')` |

## Five-configuration SHA-256 tables

`measure_artifacts.py` generated each tracked configuration into temporary scratch,
then called both generator CLIs on its overlay. Only hashes and sizes were retained.
The builder table includes the generated per-configuration shape and sweep text.
`before.json` was measured before the first source change; `after.json` after F1-F4.
`through-575.json` is an identical intermediate measurement.
No build tree, toolchain, package installation or generated artifact was stored here.

### Before

#### endstation_arty_4x4

| Artifact | Bytes | SHA-256 |
|---|---|---|
| `builder/adp_shape_defaults.svh` | 7562 | `f5539f2c29b0ab0440be88f5985ba41bebb508bede7095e5387a03721e50a418` |
| `builder/aecp_aem_rom.svh` | 52444 | `1cd6c92190c1b4f8c14783423a1618328e2fbefe286ab78edb00f96adb45f59d` |
| `builder/aem_overlay.json` | 11920 | `a9b9d900fb425e95e2b3728b47bc5c10b7d7f6b1027be1758f27b01b00b8f98c` |
| `builder/build_plan.md` | 11000 | `c040b872fa0102576fccf0f235cd9436722efd9f66cf885b220a5dfcd502d722` |
| `builder/gen/adp_shape_defaults.svh` | 7562 | `f5539f2c29b0ab0440be88f5985ba41bebb508bede7095e5387a03721e50a418` |
| `builder/gptp_ucode.hex` | 13312 | `09f5d05defa759905f23630affc619d6af658e4c5f20aa0f63cc65f41317e651` |
| `builder/lwsrp_csr_defaults.svh` | 2183 | `90d4615e95883d5c1fdf5ce4eb8e716ac655114d8f0eb9e5579ec8e671bbfa88` |
| `builder/lwsrp_table.json` | 4084 | `90e1aa992317980e97ec42768d524e9b8af65e2279a31e1696f5f68254f05221` |
| `builder/lwsrp_table.svh` | 4288 | `36331d96c16b57ba3660a3183af58752195d94f2681d03ccfcf50003f227b222` |
| `builder/platform_shape.json` | 246 | `bbd040ba298a66ff0bd856f8f0b4e75c04c1831ba635a5b3ad756625ab8b0a28` |
| `builder/soc_params.json` | 589 | `fe552b1ec220f349b55cd499bc62680e9f7abf28397125cc457fd7cf63f61fb8` |
| `builder/sweep_opts.generated.sh` | 1209 | `f50e8a7f952d693de9c85e76caec5d77c252726cd6409eaee57e4a328efe8dcc` |
| `image/aem_desc.bin` | 10112 | `1b288e13ccbf03410c593a53bc22f4a68e3d289eef8a7f907e63bc98a51415ff` |
| `image/aem_desc.json` | 20716 | `0ea2e47927e0a0eff12d781d979a255c39a935b7f06e07366d9ab3ff368d4e3e` |
| `image/aem_desc.map` | 1311 | `09cf3da5a39730c1acedae4f09474c2d98d1aa17d8fa36f0238adc210fdaa571` |
| `store/aecp_aem_rom.svh` | 52444 | `1cd6c92190c1b4f8c14783423a1618328e2fbefe286ab78edb00f96adb45f59d` |
| `store/aem_rom.json` | 22180 | `b9ef1f60be8ed24ce5545a98f4f899d3078d06694a791caef8f69086ffc70b7b` |

#### endstation_arty_8ch

| Artifact | Bytes | SHA-256 |
|---|---|---|
| `builder/adp_shape_defaults.svh` | 7836 | `41c02ad55f431ac15262d8a5db8e4a24945d375f217f7f0e552cd0b3f18cdd89` |
| `builder/aecp_aem_rom.svh` | 71921 | `19dd262b93e56aeab1641f3d3e534fc7af372f1c2f8c1801e5a7895d1982ae34` |
| `builder/aem_overlay.json` | 16978 | `87fc3c51e2fc5a49b91d67e05ea621449391619430ecfaef4cac5422b5b4b94e` |
| `builder/build_plan.md` | 11003 | `1a93c95f35d176c5b52e03c1f0d5ccea7726c682a803948a5763029a509edf76` |
| `builder/gen/adp_shape_defaults.svh` | 7836 | `41c02ad55f431ac15262d8a5db8e4a24945d375f217f7f0e552cd0b3f18cdd89` |
| `builder/gptp_ucode.hex` | 13312 | `09f5d05defa759905f23630affc619d6af658e4c5f20aa0f63cc65f41317e651` |
| `builder/lwsrp_csr_defaults.svh` | 2183 | `f2519804843397b4bde6393e3be67f348e3b3ef6e73e62fef22b3a71b4ecf87f` |
| `builder/lwsrp_table.json` | 4084 | `0e151e2854b3799281d19d01e67c27b04a53ca470a672ad27bc48f93ea840987` |
| `builder/lwsrp_table.svh` | 4288 | `c7189e2e3dcf79a7fcd6c204674fca581d89aea327c77b65ea7aa57f38aa3e19` |
| `builder/platform_shape.json` | 246 | `b818b72a035c5f73870925ffe208eda20292bedc629a399d5d31aa14160242ce` |
| `builder/soc_params.json` | 589 | `7a10be52746259e11e1c43402cb8097ca5234e9b358fd6160af5c5e42673faff` |
| `builder/sweep_opts.generated.sh` | 1209 | `8ea30219313f53e66c302861aa6e8824d0ded1f7f6ddc159a113ff79326a75f3` |
| `image/aem_desc.bin` | 15360 | `2b5c008cf3a2ff1eca11ef5e24c5a2e391e97f25435854430e563758de516b9b` |
| `image/aem_desc.json` | 31200 | `22d2815009a4d468faf1d48322b57e5ef2f6260d34219299810b7e5aafaced18` |
| `image/aem_desc.map` | 1311 | `163d5a414e34591ad639c3682747a35c43db64dcb3d46cb06c77d4c33edb634a` |
| `store/aecp_aem_rom.svh` | 71921 | `19dd262b93e56aeab1641f3d3e534fc7af372f1c2f8c1801e5a7895d1982ae34` |
| `store/aem_rom.json` | 32868 | `de55410b93502c4ddfa3e1555efcde68b9e805833bf528969d78bcbd2af7ae45` |

#### endstation_arty_current

| Artifact | Bytes | SHA-256 |
|---|---|---|
| `builder/adp_shape_defaults.svh` | 7089 | `54f350a99a0e6883f394858fe12457cffb4a1fea08ae23f5ba42c02636a46c98` |
| `builder/aecp_aem_rom.svh` | 33428 | `d8365928caecf01dc79b3d9a75a6c56573669ad121d8cc04b42f44820601c999` |
| `builder/aem_overlay.json` | 6238 | `12f48ab98be36408d6090158d5fc27341ca72d53217fcf892e097fbadab4e70e` |
| `builder/build_plan.md` | 9105 | `4eb5e433433f1c3af1311a4585c9a80101178766c8aa9f7573a75d3e034167bf` |
| `builder/gen/adp_shape_defaults.svh` | 7089 | `54f350a99a0e6883f394858fe12457cffb4a1fea08ae23f5ba42c02636a46c98` |
| `builder/gptp_ucode.hex` | 13312 | `09f5d05defa759905f23630affc619d6af658e4c5f20aa0f63cc65f41317e651` |
| `builder/lwsrp_csr_defaults.svh` | 2187 | `d10ce5559b108f54800b8432b672a0d33379721bf2a4edf0058e185484f3881d` |
| `builder/lwsrp_table.json` | 2274 | `dc4a200fa4dae047598419a78713677aefeab85b957808b9ec7284f2411a668f` |
| `builder/lwsrp_table.svh` | 3826 | `df3c4fa0289d23deea8f8e688573faa1adbb12f8485a7b5613bd30b8b288f8e4` |
| `builder/platform_shape.json` | 250 | `03328f238565f45f775a8fb17921a20ac4172d864b218e3703c23e185e678c99` |
| `builder/soc_params.json` | 498 | `696350eee365adb614b78e445d6522569e73d0eaa555b4de6603319d45da59cb` |
| `builder/sweep_opts.generated.sh` | 1143 | `969f765fe53c592a9fd4afcbb415733fd3ed1c2e367d788faf81e9f2e88ec6c7` |
| `image/aem_desc.bin` | 5792 | `ac833c3ccde42a2d9a78b517d660b9f7da03c4b3d31227aa65dcaf9e8def6192` |
| `image/aem_desc.json` | 11356 | `3c4b9440bccdc59198dacbc073fbb01671dec866d5adcf1b98225c8b6f822057` |
| `image/aem_desc.map` | 1310 | `77dad531965096987d682f77e93f81e5b6f182eaae879fb43b084be8570bec4c` |
| `store/aecp_aem_rom.svh` | 33428 | `d8365928caecf01dc79b3d9a75a6c56573669ad121d8cc04b42f44820601c999` |
| `store/aem_rom.json` | 12722 | `1c25578eda1352acf7442ca90d0eb964709388ad23954e07f9bbc726004faa5a` |

#### endstation_ax7101_1x1_tdm8

| Artifact | Bytes | SHA-256 |
|---|---|---|
| `builder/adp_shape_defaults.svh` | 7199 | `eb03dfaa2f914f49b07c31ddcc62ebc4a64e839a466a3387650f25823afb1020` |
| `builder/aecp_aem_rom.svh` | 40979 | `deea618d789b235c532edc47db08838afc7ffc2f74953f1a117d1fb2c7bd5d33` |
| `builder/aem_overlay.json` | 7196 | `e148841ac36dbf3e6d6729c49c7c944ed5194adc75941ceb69e3af80b11e3621` |
| `builder/build_plan.md` | 10825 | `203c4859f9557b4a250454fe9e0561706cc581708811988cd926edda9b942858` |
| `builder/gen/adp_shape_defaults.svh` | 7199 | `eb03dfaa2f914f49b07c31ddcc62ebc4a64e839a466a3387650f25823afb1020` |
| `builder/gptp_ucode.hex` | 13312 | `78c8418a00b35cdae75c459c5269ca3892355507c4dc8af9eb2c29d81b87673b` |
| `builder/lwsrp_csr_defaults.svh` | 2190 | `0e9df2d455d90782c87546dab4dd1fe7b5fb7f4bc81074e910ba71ddc7016d74` |
| `builder/lwsrp_table.json` | 2289 | `61b2e71d9a40c61bfb0eaf884af6257b1b030e441c5f507f99720d0c18dad47d` |
| `builder/lwsrp_table.svh` | 3832 | `8209fdee3cd744d24a066b76017f71f16d87f636c4470eb95e9f986dce550522` |
| `builder/platform_shape.json` | 253 | `0325a3cc988f7f97b34997ef3ac53c6624edfc62b0bd4b5ffb42dc72894ddae7` |
| `builder/soc_params.json` | 799 | `d5ec9866f86c339dc1c178c31c7800a359813660d9cbcc95e242e1e29b13c516` |
| `builder/sweep_opts.generated.sh` | 1366 | `515d8610aa1a58f3b2e6b004d63eada43e826886ab420370ac9c45b63697670f` |
| `image/aem_desc.bin` | 7352 | `9b077636b1d42aca660b16dce8eafa06f1e3cac842134e51ba65930d16214404` |
| `image/aem_desc.json` | 14387 | `679d8286a0151b921aa1c6d38370c7c231020f1a5c75a85e565fce9fe1ba0c17` |
| `image/aem_desc.map` | 1243 | `07151f7c4b493da8e1d3fea32a7e9755951d8e97e021e040ef2a9f3899cb7ede` |
| `store/aecp_aem_rom.svh` | 40979 | `deea618d789b235c532edc47db08838afc7ffc2f74953f1a117d1fb2c7bd5d33` |
| `store/aem_rom.json` | 15820 | `9469c9d0e79e8d949c2246437f8276a09098875ab2bf5e0b514256d40bc37f54` |

#### endstation_ax7101_8x8

| Artifact | Bytes | SHA-256 |
|---|---|---|
| `builder/adp_shape_defaults.svh` | 8449 | `26a61e545097a577f1b6bae2e15e92c867e4143a8f8ceb13e2abc21d03279333` |
| `builder/aecp_aem_rom.svh` | 86567 | `9f6963190256809964376e8747ebc3465d4b4831df01ec3d91c7e8892e46d755` |
| `builder/aem_overlay.json` | 20163 | `baef8bb15a57606b047e657c8ba50460d7f806983a0e08bf24432fc32435fb0c` |
| `builder/build_plan.md` | 15177 | `cda16a14dfa18d0021888a34e98af04c549c280adece820137712db93fb04f72` |
| `builder/gen/adp_shape_defaults.svh` | 8449 | `26a61e545097a577f1b6bae2e15e92c867e4143a8f8ceb13e2abc21d03279333` |
| `builder/gptp_ucode.hex` | 13312 | `21e846a7e1989091e555486bbb571b6967eb014925f768dbca7d41124d1d3748` |
| `builder/lwsrp_csr_defaults.svh` | 2185 | `c9849c561b9aab3f682e2974ce1ba81443c2696a0c1a4e53d3975f2557c159c4` |
| `builder/lwsrp_table.json` | 6498 | `604cd1bae811ba9ff4c115db0009bb73f538223a90ca79466d28240cbc2e9415` |
| `builder/lwsrp_table.svh` | 4918 | `59bfe055ba72d4d9254163ba9fff232ad7edf7511235caf7aacb93f789ff10fa` |
| `builder/platform_shape.json` | 248 | `a08aef1e775ecd345a7f87157f4bf3eed28306250d49003d0c5231e714e6cf17` |
| `builder/soc_params.json` | 787 | `fe470422d9e29e0f9727deca18945d57975f4cb7d1e61722332205c411d99927` |
| `builder/sweep_opts.generated.sh` | 1359 | `734ba3acf384b296987156b2e676001fbe4e0558a49e1052e66009c3912d2fc2` |
| `image/aem_desc.bin` | 18288 | `193bf18736d23256c1b25d9af1bddb0721d95780fb36a14cf5f91476aff1a2d4` |
| `image/aem_desc.json` | 37534 | `50eaefa69bcad009479d1d7df3ced08f26b319d1a91dfe2ce659ef97c53620ad` |
| `image/aem_desc.map` | 1244 | `14d38a422d09d4b729032b19cfeb515756b30156c22f65df842184956ffd989f` |
| `store/aecp_aem_rom.svh` | 86567 | `9f6963190256809964376e8747ebc3465d4b4831df01ec3d91c7e8892e46d755` |
| `store/aem_rom.json` | 39074 | `8bd1f3f6e3d790d3c819741a787a5d04c5d9b4c37faf81011f1989a371fda476` |

### After

#### endstation_arty_4x4

| Artifact | Bytes | SHA-256 |
|---|---|---|
| `builder/adp_shape_defaults.svh` | 7562 | `f5539f2c29b0ab0440be88f5985ba41bebb508bede7095e5387a03721e50a418` |
| `builder/aecp_aem_rom.svh` | 52444 | `1cd6c92190c1b4f8c14783423a1618328e2fbefe286ab78edb00f96adb45f59d` |
| `builder/aem_overlay.json` | 11920 | `a9b9d900fb425e95e2b3728b47bc5c10b7d7f6b1027be1758f27b01b00b8f98c` |
| `builder/build_plan.md` | 11000 | `c040b872fa0102576fccf0f235cd9436722efd9f66cf885b220a5dfcd502d722` |
| `builder/gen/adp_shape_defaults.svh` | 7562 | `f5539f2c29b0ab0440be88f5985ba41bebb508bede7095e5387a03721e50a418` |
| `builder/gptp_ucode.hex` | 13312 | `09f5d05defa759905f23630affc619d6af658e4c5f20aa0f63cc65f41317e651` |
| `builder/lwsrp_csr_defaults.svh` | 2183 | `90d4615e95883d5c1fdf5ce4eb8e716ac655114d8f0eb9e5579ec8e671bbfa88` |
| `builder/lwsrp_table.json` | 4084 | `90e1aa992317980e97ec42768d524e9b8af65e2279a31e1696f5f68254f05221` |
| `builder/lwsrp_table.svh` | 4288 | `36331d96c16b57ba3660a3183af58752195d94f2681d03ccfcf50003f227b222` |
| `builder/platform_shape.json` | 246 | `bbd040ba298a66ff0bd856f8f0b4e75c04c1831ba635a5b3ad756625ab8b0a28` |
| `builder/soc_params.json` | 589 | `fe552b1ec220f349b55cd499bc62680e9f7abf28397125cc457fd7cf63f61fb8` |
| `builder/sweep_opts.generated.sh` | 1209 | `f50e8a7f952d693de9c85e76caec5d77c252726cd6409eaee57e4a328efe8dcc` |
| `image/aem_desc.bin` | 10112 | `1b288e13ccbf03410c593a53bc22f4a68e3d289eef8a7f907e63bc98a51415ff` |
| `image/aem_desc.json` | 20716 | `0ea2e47927e0a0eff12d781d979a255c39a935b7f06e07366d9ab3ff368d4e3e` |
| `image/aem_desc.map` | 1311 | `09cf3da5a39730c1acedae4f09474c2d98d1aa17d8fa36f0238adc210fdaa571` |
| `store/aecp_aem_rom.svh` | 52444 | `1cd6c92190c1b4f8c14783423a1618328e2fbefe286ab78edb00f96adb45f59d` |
| `store/aem_rom.json` | 22180 | `b9ef1f60be8ed24ce5545a98f4f899d3078d06694a791caef8f69086ffc70b7b` |

#### endstation_arty_8ch

| Artifact | Bytes | SHA-256 |
|---|---|---|
| `builder/adp_shape_defaults.svh` | 7836 | `41c02ad55f431ac15262d8a5db8e4a24945d375f217f7f0e552cd0b3f18cdd89` |
| `builder/aecp_aem_rom.svh` | 71921 | `19dd262b93e56aeab1641f3d3e534fc7af372f1c2f8c1801e5a7895d1982ae34` |
| `builder/aem_overlay.json` | 16978 | `87fc3c51e2fc5a49b91d67e05ea621449391619430ecfaef4cac5422b5b4b94e` |
| `builder/build_plan.md` | 11003 | `1a93c95f35d176c5b52e03c1f0d5ccea7726c682a803948a5763029a509edf76` |
| `builder/gen/adp_shape_defaults.svh` | 7836 | `41c02ad55f431ac15262d8a5db8e4a24945d375f217f7f0e552cd0b3f18cdd89` |
| `builder/gptp_ucode.hex` | 13312 | `09f5d05defa759905f23630affc619d6af658e4c5f20aa0f63cc65f41317e651` |
| `builder/lwsrp_csr_defaults.svh` | 2183 | `f2519804843397b4bde6393e3be67f348e3b3ef6e73e62fef22b3a71b4ecf87f` |
| `builder/lwsrp_table.json` | 4084 | `0e151e2854b3799281d19d01e67c27b04a53ca470a672ad27bc48f93ea840987` |
| `builder/lwsrp_table.svh` | 4288 | `c7189e2e3dcf79a7fcd6c204674fca581d89aea327c77b65ea7aa57f38aa3e19` |
| `builder/platform_shape.json` | 246 | `b818b72a035c5f73870925ffe208eda20292bedc629a399d5d31aa14160242ce` |
| `builder/soc_params.json` | 589 | `7a10be52746259e11e1c43402cb8097ca5234e9b358fd6160af5c5e42673faff` |
| `builder/sweep_opts.generated.sh` | 1209 | `8ea30219313f53e66c302861aa6e8824d0ded1f7f6ddc159a113ff79326a75f3` |
| `image/aem_desc.bin` | 15360 | `2b5c008cf3a2ff1eca11ef5e24c5a2e391e97f25435854430e563758de516b9b` |
| `image/aem_desc.json` | 31200 | `22d2815009a4d468faf1d48322b57e5ef2f6260d34219299810b7e5aafaced18` |
| `image/aem_desc.map` | 1311 | `163d5a414e34591ad639c3682747a35c43db64dcb3d46cb06c77d4c33edb634a` |
| `store/aecp_aem_rom.svh` | 71921 | `19dd262b93e56aeab1641f3d3e534fc7af372f1c2f8c1801e5a7895d1982ae34` |
| `store/aem_rom.json` | 32868 | `de55410b93502c4ddfa3e1555efcde68b9e805833bf528969d78bcbd2af7ae45` |

#### endstation_arty_current

| Artifact | Bytes | SHA-256 |
|---|---|---|
| `builder/adp_shape_defaults.svh` | 7089 | `54f350a99a0e6883f394858fe12457cffb4a1fea08ae23f5ba42c02636a46c98` |
| `builder/aecp_aem_rom.svh` | 33428 | `d8365928caecf01dc79b3d9a75a6c56573669ad121d8cc04b42f44820601c999` |
| `builder/aem_overlay.json` | 6238 | `12f48ab98be36408d6090158d5fc27341ca72d53217fcf892e097fbadab4e70e` |
| `builder/build_plan.md` | 9105 | `4eb5e433433f1c3af1311a4585c9a80101178766c8aa9f7573a75d3e034167bf` |
| `builder/gen/adp_shape_defaults.svh` | 7089 | `54f350a99a0e6883f394858fe12457cffb4a1fea08ae23f5ba42c02636a46c98` |
| `builder/gptp_ucode.hex` | 13312 | `09f5d05defa759905f23630affc619d6af658e4c5f20aa0f63cc65f41317e651` |
| `builder/lwsrp_csr_defaults.svh` | 2187 | `d10ce5559b108f54800b8432b672a0d33379721bf2a4edf0058e185484f3881d` |
| `builder/lwsrp_table.json` | 2274 | `dc4a200fa4dae047598419a78713677aefeab85b957808b9ec7284f2411a668f` |
| `builder/lwsrp_table.svh` | 3826 | `df3c4fa0289d23deea8f8e688573faa1adbb12f8485a7b5613bd30b8b288f8e4` |
| `builder/platform_shape.json` | 250 | `03328f238565f45f775a8fb17921a20ac4172d864b218e3703c23e185e678c99` |
| `builder/soc_params.json` | 498 | `696350eee365adb614b78e445d6522569e73d0eaa555b4de6603319d45da59cb` |
| `builder/sweep_opts.generated.sh` | 1143 | `969f765fe53c592a9fd4afcbb415733fd3ed1c2e367d788faf81e9f2e88ec6c7` |
| `image/aem_desc.bin` | 5792 | `ac833c3ccde42a2d9a78b517d660b9f7da03c4b3d31227aa65dcaf9e8def6192` |
| `image/aem_desc.json` | 11356 | `3c4b9440bccdc59198dacbc073fbb01671dec866d5adcf1b98225c8b6f822057` |
| `image/aem_desc.map` | 1310 | `77dad531965096987d682f77e93f81e5b6f182eaae879fb43b084be8570bec4c` |
| `store/aecp_aem_rom.svh` | 33428 | `d8365928caecf01dc79b3d9a75a6c56573669ad121d8cc04b42f44820601c999` |
| `store/aem_rom.json` | 12722 | `1c25578eda1352acf7442ca90d0eb964709388ad23954e07f9bbc726004faa5a` |

#### endstation_ax7101_1x1_tdm8

| Artifact | Bytes | SHA-256 |
|---|---|---|
| `builder/adp_shape_defaults.svh` | 7199 | `eb03dfaa2f914f49b07c31ddcc62ebc4a64e839a466a3387650f25823afb1020` |
| `builder/aecp_aem_rom.svh` | 40979 | `deea618d789b235c532edc47db08838afc7ffc2f74953f1a117d1fb2c7bd5d33` |
| `builder/aem_overlay.json` | 7196 | `e148841ac36dbf3e6d6729c49c7c944ed5194adc75941ceb69e3af80b11e3621` |
| `builder/build_plan.md` | 10825 | `203c4859f9557b4a250454fe9e0561706cc581708811988cd926edda9b942858` |
| `builder/gen/adp_shape_defaults.svh` | 7199 | `eb03dfaa2f914f49b07c31ddcc62ebc4a64e839a466a3387650f25823afb1020` |
| `builder/gptp_ucode.hex` | 13312 | `78c8418a00b35cdae75c459c5269ca3892355507c4dc8af9eb2c29d81b87673b` |
| `builder/lwsrp_csr_defaults.svh` | 2190 | `0e9df2d455d90782c87546dab4dd1fe7b5fb7f4bc81074e910ba71ddc7016d74` |
| `builder/lwsrp_table.json` | 2289 | `61b2e71d9a40c61bfb0eaf884af6257b1b030e441c5f507f99720d0c18dad47d` |
| `builder/lwsrp_table.svh` | 3832 | `8209fdee3cd744d24a066b76017f71f16d87f636c4470eb95e9f986dce550522` |
| `builder/platform_shape.json` | 253 | `0325a3cc988f7f97b34997ef3ac53c6624edfc62b0bd4b5ffb42dc72894ddae7` |
| `builder/soc_params.json` | 799 | `d5ec9866f86c339dc1c178c31c7800a359813660d9cbcc95e242e1e29b13c516` |
| `builder/sweep_opts.generated.sh` | 1366 | `515d8610aa1a58f3b2e6b004d63eada43e826886ab420370ac9c45b63697670f` |
| `image/aem_desc.bin` | 7352 | `9b077636b1d42aca660b16dce8eafa06f1e3cac842134e51ba65930d16214404` |
| `image/aem_desc.json` | 14387 | `679d8286a0151b921aa1c6d38370c7c231020f1a5c75a85e565fce9fe1ba0c17` |
| `image/aem_desc.map` | 1243 | `07151f7c4b493da8e1d3fea32a7e9755951d8e97e021e040ef2a9f3899cb7ede` |
| `store/aecp_aem_rom.svh` | 40979 | `deea618d789b235c532edc47db08838afc7ffc2f74953f1a117d1fb2c7bd5d33` |
| `store/aem_rom.json` | 15820 | `9469c9d0e79e8d949c2246437f8276a09098875ab2bf5e0b514256d40bc37f54` |

#### endstation_ax7101_8x8

| Artifact | Bytes | SHA-256 |
|---|---|---|
| `builder/adp_shape_defaults.svh` | 8449 | `26a61e545097a577f1b6bae2e15e92c867e4143a8f8ceb13e2abc21d03279333` |
| `builder/aecp_aem_rom.svh` | 86567 | `9f6963190256809964376e8747ebc3465d4b4831df01ec3d91c7e8892e46d755` |
| `builder/aem_overlay.json` | 20163 | `baef8bb15a57606b047e657c8ba50460d7f806983a0e08bf24432fc32435fb0c` |
| `builder/build_plan.md` | 15177 | `cda16a14dfa18d0021888a34e98af04c549c280adece820137712db93fb04f72` |
| `builder/gen/adp_shape_defaults.svh` | 8449 | `26a61e545097a577f1b6bae2e15e92c867e4143a8f8ceb13e2abc21d03279333` |
| `builder/gptp_ucode.hex` | 13312 | `21e846a7e1989091e555486bbb571b6967eb014925f768dbca7d41124d1d3748` |
| `builder/lwsrp_csr_defaults.svh` | 2185 | `c9849c561b9aab3f682e2974ce1ba81443c2696a0c1a4e53d3975f2557c159c4` |
| `builder/lwsrp_table.json` | 6498 | `604cd1bae811ba9ff4c115db0009bb73f538223a90ca79466d28240cbc2e9415` |
| `builder/lwsrp_table.svh` | 4918 | `59bfe055ba72d4d9254163ba9fff232ad7edf7511235caf7aacb93f789ff10fa` |
| `builder/platform_shape.json` | 248 | `a08aef1e775ecd345a7f87157f4bf3eed28306250d49003d0c5231e714e6cf17` |
| `builder/soc_params.json` | 787 | `fe470422d9e29e0f9727deca18945d57975f4cb7d1e61722332205c411d99927` |
| `builder/sweep_opts.generated.sh` | 1359 | `734ba3acf384b296987156b2e676001fbe4e0558a49e1052e66009c3912d2fc2` |
| `image/aem_desc.bin` | 18288 | `193bf18736d23256c1b25d9af1bddb0721d95780fb36a14cf5f91476aff1a2d4` |
| `image/aem_desc.json` | 37534 | `50eaefa69bcad009479d1d7df3ced08f26b319d1a91dfe2ce659ef97c53620ad` |
| `image/aem_desc.map` | 1244 | `14d38a422d09d4b729032b19cfeb515756b30156c22f65df842184956ffd989f` |
| `store/aecp_aem_rom.svh` | 86567 | `9f6963190256809964376e8747ebc3465d4b4831df01ec3d91c7e8892e46d755` |
| `store/aem_rom.json` | 39074 | `8bd1f3f6e3d790d3c819741a787a5d04c5d9b4c37faf81011f1989a371fda476` |

## Delivery state

`PR-BODY.md` is prepared for the assigned publication role and starts with [A347].
It carries all four closing references on separate lines.
Independent review, push, pull request creation and merge are not performed here.
The final authorized action is the [A347] REVIEW READY comment on issue #573,
using the exact head above. All four project items are In review before that comment.
