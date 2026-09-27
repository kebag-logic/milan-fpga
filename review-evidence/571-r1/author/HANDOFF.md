# Issue #571 author handoff

Role: [A371], author. Reviewers: [R356] internal and [R357] external.
Status: author work validated and committed; independent review pending.
Head: f8a52f919bd309960046330a5af127b56731cb27
Repository: https://github.com/kebag-logic/milan-fpga.git
Branch: 571-pp-unit-counts
Base: 2a2a7bb655e528edc3087c88033cd3a47546feb4
Processor pin: 870ff88a (must remain unchanged).

## Decision record

Assignment: https://github.com/kebag-logic/milan-fpga/issues/571#issuecomment-5857833068
Takeover: https://github.com/kebag-logic/milan-fpga/issues/571#issuecomment-5857841165

The assignment on issue #571 chooses binding, not refusal of non-default
counts. Derive CONTROL from the same descriptor_counts pass as AUDIO_UNIT and
CLOCK_DOMAIN. Preserve N_CLK_DOM_P in the parent. The model constructor unconditionally supplies one of each descriptor, and
the descriptor assembler unconditionally emits their bytes. No configuration
can remove them, so zero is unreachable and no new refusal is needed. Stop if any tracked configuration
would be refused or change a count.

Reference availability: `docs/spec-refs.md` is absent from this worktree and
from the processor submodule. No private management material was read.
The assignment explicitly names Milan v1.2 Section 5.3.3; the parent
ownership matrix cites Section 5.3.3.3 for AUDIO_UNIT and 5.3.3.10 for
IDENTIFY. The zero-count conclusion is independently established by
`_overlay_document` and `aem_assemble._entity_descriptors`, not an assumption
that the processor default enforces those clauses. The processor inventory
was read at the assigned pin. No alternative specification revision was used.

## Changes with file and line

- `sw/builder/endstation_builder.py:2790`: derive CONTROL from descriptor_counts;
  document why the model cannot produce a zero count.
- `hdl/milan/KL_pp_shadow.sv:238`: expose N_CONTROL_P;
  `hdl/milan/KL_pp_shadow.sv:1060`: forward all three counts into u_pp.
- `hdl/milan/milan_datapath.sv:7429`: bind AEM_N_CONTROL_C into pp_shadow.
- `hdl/common/gen/adp_shape_defaults.svh:38` and all five
  `configs/generated/endstation_*/gen/adp_shape_defaults.svh:38`:
  regenerated CONTROL count line only.
- `scripts/check_entity_shape.py:171`: count inventory;
  `scripts/check_entity_shape.py:372`: both symbolic binding hops;
  `scripts/check_entity_shape.py:395`: header/census comparison;
  `scripts/check_entity_shape.py:576`: count actual descriptor-directory entries.
- `scripts/entity_shape_selftest.py:598`: 2/3/4 positive fixture and 24 mutants.
- `docs/reference/PP_DESCRIPTOR_OWNERSHIP.md:49`: integration inventory,
  positive-count construction, and executable validation boundary.

No parent inventory listing these parameters as unbound was found.
The existing descriptor ownership page now records the explicit bindings.

## Per-configuration header diff

All three counts remain 1 in every configuration. The STOP condition was not triggered.

### endstation_arty_4x4

```diff
--- base/adp_shape_defaults.svh
+++ candidate/adp_shape_defaults.svh
@@ -36,4 +36,5 @@
   localparam int AEM_N_AUDIO_UNIT_C = 1;
   localparam int AEM_N_CLKDOM_C     = 1;
+  localparam int AEM_N_CONTROL_C    = 1;
   //! talker_capabilities (1722.1-2021 Table 6.4): IMPLEMENTED |
   //! AUDIO_SOURCE, + MEDIA_CLOCK_SOURCE only when a CRF STREAM_OUTPUT
```

### endstation_arty_8ch

```diff
--- base/adp_shape_defaults.svh
+++ candidate/adp_shape_defaults.svh
@@ -36,4 +36,5 @@
   localparam int AEM_N_AUDIO_UNIT_C = 1;
   localparam int AEM_N_CLKDOM_C     = 1;
+  localparam int AEM_N_CONTROL_C    = 1;
   //! talker_capabilities (1722.1-2021 Table 6.4): IMPLEMENTED |
   //! AUDIO_SOURCE, + MEDIA_CLOCK_SOURCE only when a CRF STREAM_OUTPUT
```

### endstation_arty_current

```diff
--- base/adp_shape_defaults.svh
+++ candidate/adp_shape_defaults.svh
@@ -36,4 +36,5 @@
   localparam int AEM_N_AUDIO_UNIT_C = 1;
   localparam int AEM_N_CLKDOM_C     = 1;
+  localparam int AEM_N_CONTROL_C    = 1;
   //! talker_capabilities (1722.1-2021 Table 6.4): IMPLEMENTED |
   //! AUDIO_SOURCE, + MEDIA_CLOCK_SOURCE only when a CRF STREAM_OUTPUT
```

### endstation_ax7101_1x1_tdm8

```diff
--- base/adp_shape_defaults.svh
+++ candidate/adp_shape_defaults.svh
@@ -36,4 +36,5 @@
   localparam int AEM_N_AUDIO_UNIT_C = 1;
   localparam int AEM_N_CLKDOM_C     = 1;
+  localparam int AEM_N_CONTROL_C    = 1;
   //! talker_capabilities (1722.1-2021 Table 6.4): IMPLEMENTED |
   //! AUDIO_SOURCE, + MEDIA_CLOCK_SOURCE only when a CRF STREAM_OUTPUT
```

### endstation_ax7101_8x8

```diff
--- base/adp_shape_defaults.svh
+++ candidate/adp_shape_defaults.svh
@@ -36,4 +36,5 @@
   localparam int AEM_N_AUDIO_UNIT_C = 1;
   localparam int AEM_N_CLKDOM_C     = 1;
+  localparam int AEM_N_CONTROL_C    = 1;
   //! talker_capabilities (1722.1-2021 Table 6.4): IMPLEMENTED |
   //! AUDIO_SOURCE, + MEDIA_CLOCK_SOURCE only when a CRF STREAM_OUTPUT
```

## Five-configuration SHA-256 tables

Every file in each generated directory was compared byte for byte.
The table includes the descriptor image/map and two derived outputs,
sweep options and interface parameters. "Same" means the candidate SHA-256
and byte count equal the printed base values.
Large artifacts are retained in `/tmp/571-a371`, outside this packet.

### endstation_arty_4x4

| Artifact | Base bytes | Base SHA-256 | Candidate bytes | Candidate SHA-256 |
|---|---:|---|---:|---|
| `adp_shape_defaults.svh` | 7562 | `f5539f2c29b0ab0440be88f5985ba41bebb508bede7095e5387a03721e50a418` | 7603 | `fbf4bf36ab9c972789aa4a774fea6a1e8f462eadebc919ea30384bc89b3d02fe` |
| `aecp_aem_rom.svh` | 52444 | `1cd6c92190c1b4f8c14783423a1618328e2fbefe286ab78edb00f96adb45f59d` | 52444 | Same |
| `aem_desc.bin` | 10112 | `1b288e13ccbf03410c593a53bc22f4a68e3d289eef8a7f907e63bc98a51415ff` | 10112 | Same |
| `aem_desc.map` | 1311 | `09cf3da5a39730c1acedae4f09474c2d98d1aa17d8fa36f0238adc210fdaa571` | 1311 | Same |
| `aem_overlay.json` | 11920 | `a9b9d900fb425e95e2b3728b47bc5c10b7d7f6b1027be1758f27b01b00b8f98c` | 11920 | Same |
| `build_plan.md` | 11000 | `c040b872fa0102576fccf0f235cd9436722efd9f66cf885b220a5dfcd502d722` | 11000 | Same |
| `gptp_ucode.hex` | 13312 | `09f5d05defa759905f23630affc619d6af658e4c5f20aa0f63cc65f41317e651` | 13312 | Same |
| `interface_params.json` | 5 | `38e0b9de817f645c4bec37c0d4a3e58baecccb040f5718dc069a72c7385a0bed` | 5 | Same |
| `lwsrp_csr_defaults.svh` | 2183 | `90d4615e95883d5c1fdf5ce4eb8e716ac655114d8f0eb9e5579ec8e671bbfa88` | 2183 | Same |
| `lwsrp_table.json` | 4084 | `90e1aa992317980e97ec42768d524e9b8af65e2279a31e1696f5f68254f05221` | 4084 | Same |
| `lwsrp_table.svh` | 4288 | `36331d96c16b57ba3660a3183af58752195d94f2681d03ccfcf50003f227b222` | 4288 | Same |
| `platform_shape.json` | 246 | `bbd040ba298a66ff0bd856f8f0b4e75c04c1831ba635a5b3ad756625ab8b0a28` | 246 | Same |
| `soc_params.json` | 589 | `fe552b1ec220f349b55cd499bc62680e9f7abf28397125cc457fd7cf63f61fb8` | 589 | Same |
| `sweep_opts.sh` | 1209 | `f50e8a7f952d693de9c85e76caec5d77c252726cd6409eaee57e4a328efe8dcc` | 1209 | Same |

### endstation_arty_8ch

| Artifact | Base bytes | Base SHA-256 | Candidate bytes | Candidate SHA-256 |
|---|---:|---|---:|---|
| `adp_shape_defaults.svh` | 7836 | `41c02ad55f431ac15262d8a5db8e4a24945d375f217f7f0e552cd0b3f18cdd89` | 7877 | `48076cb36b171972c3e060087ad98755d957f13603b4793cb2784725eda0bf48` |
| `aecp_aem_rom.svh` | 71921 | `19dd262b93e56aeab1641f3d3e534fc7af372f1c2f8c1801e5a7895d1982ae34` | 71921 | Same |
| `aem_desc.bin` | 15360 | `2b5c008cf3a2ff1eca11ef5e24c5a2e391e97f25435854430e563758de516b9b` | 15360 | Same |
| `aem_desc.map` | 1311 | `163d5a414e34591ad639c3682747a35c43db64dcb3d46cb06c77d4c33edb634a` | 1311 | Same |
| `aem_overlay.json` | 16978 | `87fc3c51e2fc5a49b91d67e05ea621449391619430ecfaef4cac5422b5b4b94e` | 16978 | Same |
| `build_plan.md` | 11003 | `1a93c95f35d176c5b52e03c1f0d5ccea7726c682a803948a5763029a509edf76` | 11003 | Same |
| `gptp_ucode.hex` | 13312 | `09f5d05defa759905f23630affc619d6af658e4c5f20aa0f63cc65f41317e651` | 13312 | Same |
| `interface_params.json` | 5 | `38e0b9de817f645c4bec37c0d4a3e58baecccb040f5718dc069a72c7385a0bed` | 5 | Same |
| `lwsrp_csr_defaults.svh` | 2183 | `f2519804843397b4bde6393e3be67f348e3b3ef6e73e62fef22b3a71b4ecf87f` | 2183 | Same |
| `lwsrp_table.json` | 4084 | `0e151e2854b3799281d19d01e67c27b04a53ca470a672ad27bc48f93ea840987` | 4084 | Same |
| `lwsrp_table.svh` | 4288 | `c7189e2e3dcf79a7fcd6c204674fca581d89aea327c77b65ea7aa57f38aa3e19` | 4288 | Same |
| `platform_shape.json` | 246 | `b818b72a035c5f73870925ffe208eda20292bedc629a399d5d31aa14160242ce` | 246 | Same |
| `soc_params.json` | 589 | `7a10be52746259e11e1c43402cb8097ca5234e9b358fd6160af5c5e42673faff` | 589 | Same |
| `sweep_opts.sh` | 1209 | `8ea30219313f53e66c302861aa6e8824d0ded1f7f6ddc159a113ff79326a75f3` | 1209 | Same |

### endstation_arty_current

| Artifact | Base bytes | Base SHA-256 | Candidate bytes | Candidate SHA-256 |
|---|---:|---|---:|---|
| `adp_shape_defaults.svh` | 7089 | `54f350a99a0e6883f394858fe12457cffb4a1fea08ae23f5ba42c02636a46c98` | 7130 | `13540133426c56e849bfc7b5fbbac883c0f90bc0a0af4700247179e17372fe34` |
| `aecp_aem_rom.svh` | 33428 | `d8365928caecf01dc79b3d9a75a6c56573669ad121d8cc04b42f44820601c999` | 33428 | Same |
| `aem_desc.bin` | 5792 | `ac833c3ccde42a2d9a78b517d660b9f7da03c4b3d31227aa65dcaf9e8def6192` | 5792 | Same |
| `aem_desc.map` | 1310 | `77dad531965096987d682f77e93f81e5b6f182eaae879fb43b084be8570bec4c` | 1310 | Same |
| `aem_overlay.json` | 6238 | `12f48ab98be36408d6090158d5fc27341ca72d53217fcf892e097fbadab4e70e` | 6238 | Same |
| `build_plan.md` | 9105 | `4eb5e433433f1c3af1311a4585c9a80101178766c8aa9f7573a75d3e034167bf` | 9105 | Same |
| `gptp_ucode.hex` | 13312 | `09f5d05defa759905f23630affc619d6af658e4c5f20aa0f63cc65f41317e651` | 13312 | Same |
| `interface_params.json` | 5 | `38e0b9de817f645c4bec37c0d4a3e58baecccb040f5718dc069a72c7385a0bed` | 5 | Same |
| `lwsrp_csr_defaults.svh` | 2187 | `d10ce5559b108f54800b8432b672a0d33379721bf2a4edf0058e185484f3881d` | 2187 | Same |
| `lwsrp_table.json` | 2274 | `dc4a200fa4dae047598419a78713677aefeab85b957808b9ec7284f2411a668f` | 2274 | Same |
| `lwsrp_table.svh` | 3826 | `df3c4fa0289d23deea8f8e688573faa1adbb12f8485a7b5613bd30b8b288f8e4` | 3826 | Same |
| `platform_shape.json` | 250 | `03328f238565f45f775a8fb17921a20ac4172d864b218e3703c23e185e678c99` | 250 | Same |
| `soc_params.json` | 498 | `696350eee365adb614b78e445d6522569e73d0eaa555b4de6603319d45da59cb` | 498 | Same |
| `sweep_opts.sh` | 1143 | `969f765fe53c592a9fd4afcbb415733fd3ed1c2e367d788faf81e9f2e88ec6c7` | 1143 | Same |

### endstation_ax7101_1x1_tdm8

| Artifact | Base bytes | Base SHA-256 | Candidate bytes | Candidate SHA-256 |
|---|---:|---|---:|---|
| `adp_shape_defaults.svh` | 7199 | `eb03dfaa2f914f49b07c31ddcc62ebc4a64e839a466a3387650f25823afb1020` | 7240 | `c6c43feb9ae573103527e71b33be9bb6625b2dbca74d7bb2db1e01c6fd255d3e` |
| `aecp_aem_rom.svh` | 40979 | `deea618d789b235c532edc47db08838afc7ffc2f74953f1a117d1fb2c7bd5d33` | 40979 | Same |
| `aem_desc.bin` | 7352 | `9b077636b1d42aca660b16dce8eafa06f1e3cac842134e51ba65930d16214404` | 7352 | Same |
| `aem_desc.map` | 1243 | `07151f7c4b493da8e1d3fea32a7e9755951d8e97e021e040ef2a9f3899cb7ede` | 1243 | Same |
| `aem_overlay.json` | 7196 | `e148841ac36dbf3e6d6729c49c7c944ed5194adc75941ceb69e3af80b11e3621` | 7196 | Same |
| `build_plan.md` | 10825 | `203c4859f9557b4a250454fe9e0561706cc581708811988cd926edda9b942858` | 10825 | Same |
| `gptp_ucode.hex` | 13312 | `78c8418a00b35cdae75c459c5269ca3892355507c4dc8af9eb2c29d81b87673b` | 13312 | Same |
| `interface_params.json` | 5 | `38e0b9de817f645c4bec37c0d4a3e58baecccb040f5718dc069a72c7385a0bed` | 5 | Same |
| `lwsrp_csr_defaults.svh` | 2190 | `0e9df2d455d90782c87546dab4dd1fe7b5fb7f4bc81074e910ba71ddc7016d74` | 2190 | Same |
| `lwsrp_table.json` | 2289 | `61b2e71d9a40c61bfb0eaf884af6257b1b030e441c5f507f99720d0c18dad47d` | 2289 | Same |
| `lwsrp_table.svh` | 3832 | `8209fdee3cd744d24a066b76017f71f16d87f636c4470eb95e9f986dce550522` | 3832 | Same |
| `platform_shape.json` | 253 | `0325a3cc988f7f97b34997ef3ac53c6624edfc62b0bd4b5ffb42dc72894ddae7` | 253 | Same |
| `soc_params.json` | 799 | `d5ec9866f86c339dc1c178c31c7800a359813660d9cbcc95e242e1e29b13c516` | 799 | Same |
| `sweep_opts.sh` | 1366 | `515d8610aa1a58f3b2e6b004d63eada43e826886ab420370ac9c45b63697670f` | 1366 | Same |

### endstation_ax7101_8x8

| Artifact | Base bytes | Base SHA-256 | Candidate bytes | Candidate SHA-256 |
|---|---:|---|---:|---|
| `adp_shape_defaults.svh` | 8449 | `26a61e545097a577f1b6bae2e15e92c867e4143a8f8ceb13e2abc21d03279333` | 8490 | `85939da9c5718d5aacd63ba6be04279e93ad06db16e0f55f2d2f58b7d5926a00` |
| `aecp_aem_rom.svh` | 86567 | `9f6963190256809964376e8747ebc3465d4b4831df01ec3d91c7e8892e46d755` | 86567 | Same |
| `aem_desc.bin` | 18288 | `193bf18736d23256c1b25d9af1bddb0721d95780fb36a14cf5f91476aff1a2d4` | 18288 | Same |
| `aem_desc.map` | 1244 | `14d38a422d09d4b729032b19cfeb515756b30156c22f65df842184956ffd989f` | 1244 | Same |
| `aem_overlay.json` | 20163 | `baef8bb15a57606b047e657c8ba50460d7f806983a0e08bf24432fc32435fb0c` | 20163 | Same |
| `build_plan.md` | 15175 | `2d303d06c5fc2f13648734ea1cb9660963bf745e73ee312476cc3a10c914a20e` | 15175 | Same |
| `gptp_ucode.hex` | 13312 | `78c8418a00b35cdae75c459c5269ca3892355507c4dc8af9eb2c29d81b87673b` | 13312 | Same |
| `interface_params.json` | 5 | `38e0b9de817f645c4bec37c0d4a3e58baecccb040f5718dc069a72c7385a0bed` | 5 | Same |
| `lwsrp_csr_defaults.svh` | 2185 | `c9849c561b9aab3f682e2974ce1ba81443c2696a0c1a4e53d3975f2557c159c4` | 2185 | Same |
| `lwsrp_table.json` | 6496 | `b525824ef9b4a7c52bc99946b08807708f5c7a0ac9087d20a0cc62f3b5e95266` | 6496 | Same |
| `lwsrp_table.svh` | 4917 | `eed72271ec9a0e3d68b8ca9f367d83251140c5464272a65ef0843a00ce95525e` | 4917 | Same |
| `platform_shape.json` | 248 | `a08aef1e775ecd345a7f87157f4bf3eed28306250d49003d0c5231e714e6cf17` | 248 | Same |
| `soc_params.json` | 786 | `41763d46738df0e907116212b9bedb85beebba34f6a66057bee0d921321ef823` | 786 | Same |
| `sweep_opts.sh` | 1358 | `3261424191ebeaa7d5bff89627aa2e47f7d0614aa1d27951e91e228cb99d2ad5` | 1358 | Same |

## Elaboration statistics comparison

Base and candidate Verilator elaborations pass for AX 1x1 and 8x8.
Every post-elaboration node-kind row is identical: 127 rows at 1x1, 128 at
8x8, comparing all four PreOrder/Scoped/WroteAll/WroteFast columns.
The normalized reports are adjacent to this handoff.
Raw linked syntax counts increase for the added parameter and bindings; these
are not hardware cells.

| Shape | Streams in/out | Ports in/out | Names | Counts AU/CD/CONTROL | PreOrder cells | PreOrder variables | PreOrder ARRAYSEL | ASSIGNDLY at WroteAll |
|---|---|---|---:|---|---:|---:|---:|---:|
| AX 1x1 | 2/2 | 1/1 | 38 | 1/1/1 | 5 | 3974 | 726 | 3936 |
| AX 8x8 | 9/9 | 8/8 | 99 | 1/1/1 | 5 | 4255 | 1241 | 3943 |

Each figure is identical in base and candidate. The standalone wrapper's
other parameters retain the same defaults on both sides. Shapes are derived
from each configuration's descriptor census and generated name count.
The base leaves processor unit parameters unbound; the candidate forwards
the generated values and also passes N_CONTROL_P=1 to the wrapper.

Recipe: `verilator --cc --stats -Wno-fatal --top-module KL_pp_shadow`
plus the `-G` shape arguments recorded in `base-shapes.json` and
`candidate-shapes.json`. Sources come from
`bash syn/yosys/run.sh --emit KL_pp_shadow` (the `src=` records).
`capture.py base --elaborate` ran before editing, and
`capture.py candidate --elaborate` ran after editing, from the physical path.
Both phases completed with rc 0. Verilator version: 5.052.
These are elaboration statistics, not placed-cell or timing measurements.
Raw report, argv and log sizes/hashes are in `elaboration-files.json`.
The source syntax column (Link), execution time and memory usage differ;
all four post-elaboration node-count columns agree exactly.

## Mutant table

| Boundary | Subject | Unbound | Literal 1 | Swapped pair |
|---|---|---|---|---|
| datapath -> pp_shadow | AUDIO_UNIT | killed | killed | killed with CLOCK_DOMAIN |
| datapath -> pp_shadow | CLOCK_DOMAIN | killed | killed | killed with CONTROL |
| datapath -> pp_shadow | CONTROL | killed | killed | killed with AUDIO_UNIT |
| pp_shadow -> u_pp | AUDIO_UNIT | killed | killed | killed with CLOCK_DOMAIN |
| pp_shadow -> u_pp | CLOCK_DOMAIN | killed | killed | killed with CONTROL |
| pp_shadow -> u_pp | CONTROL | killed | killed | killed with AUDIO_UNIT |

| Header/census control | AUDIO_UNIT | CLOCK_DOMAIN | CONTROL |
|---|---|---|---|
| Non-default emitted census | 2 accepted | 3 accepted | 4 accepted |
| Emitted literal 1 | killed | killed | killed |
| Zero census | killed | killed | killed |

Binding mutants run in memory against the same checker called by the gate.
Every rejection must name its affected parameter; swapped pairs must name both.
The two-hop check removes comments and requires one binding per parameter.
Zero controls exercise the gate, not a newly introduced builder refusal.

All 24 new mutants are killed (including separator-correct unbound maps): 18 binding mutants (three mutation kinds
for each of three counts at both hops), three literal-emitter mutants, and
three zero-census mutants. A positive synthetic census of 2/3/4 passes.
The entity-shape gate including its complete self-test passed (rc 0).

## Gate table

All commands ran in the foreground from the physical worktree:
`$LANES/571-pp-unit-counts`. No gate was piped.
The validated source was committed as `f8a52f919bd309960046330a5af127b56731cb27` without further edits.

| Gate | Command | RC |
|---|---|---:|
| doc-paths | `rtk proxy python3 scripts/check_doc_paths.py` | 0 |
| toc | `rtk proxy /tmp/571-a371-markdown-env/bin/python3 scripts/gen_toc.py --check` | 0 |
| feature-status | `rtk proxy python3 scripts/check_feature_status.py` | 0 |
| doc-style | `rtk proxy python3 scripts/check_doc_style.py` | 0 |
| declarations | `rtk proxy python3 sw/builder/test_declarations.py` | 0 |
| nvm-capture | `rtk proxy python3 scripts/check_nvm_capture.py` | 0 |
| builder-present | `rtk proxy timeout 7200 python3 -u sw/builder/test_builder.py --require-rv32` | 0 |
| builder-absent | `rtk proxy /usr/bin/python3 -u $MANAGEMENT/2026-09-23/571-a371/builder_absent.py` | 0 |
| entity-shape-final | `rtk proxy /usr/bin/python3 -u scripts/check_entity_shape.py --self-test` | 0 |
| python-idiom-final | `rtk proxy /usr/bin/python3 scripts/check_py_idiom.py` | 0 |
| diff-check | `rtk proxy git diff --check` | 0 |
| em-dash-final | `rtk proxy /tmp/571-a371-markdown-env/bin/python3 scripts/check_em_dash.py --base 2a2a7bb655e528edc3087c88033cd3a47546feb4` | 0 |
| docs-check-final | `rtk proxy python3 scripts/docs_check.py` | 0 |
| diff-check-final | `rtk proxy git diff --check 2a2a7bb655e528edc3087c88033cd3a47546feb4 HEAD` | 0 |

The compiler-present bank reports one NOT RUN arm: historical resource
calibration (gate 11), because the placement report is absent. The absent
bank reports that same arm plus the intentionally unavailable compiler-backed
census (gate 1b). The present bank exercised the compiler-dependent checks.
The absent wrapper hides only the three cross-compiler candidates; it executes
the full bank, leaves native probes intact, and asserts the absence audit.
No hardware run or SDK modification was used to fill those missing inputs.

Final entity shape: 219 checks, zero failures. All 24 new mutants killed.
Final docs-check: zero findings across 169 Markdown and 904 text files.
Final em-dash check: 23 added lines, zero findings; all 339 self-test arms pass.
Log sizes, SHA-256 and exact commands are in `gate-results.json`.
Raw builder logs stay under `/tmp/571-a371`; their hashes and sizes are recorded.

Setup corrections: the docs gate initially rejected a relative submodule
link; the final document uses the assigned processor commit in its URL.
The Markdown requirements were installed with their hashes in
`/tmp/571-a371-markdown-env`, outside this packet. The early pre-commit
em-dash run covered zero lines and is not used as evidence; the final run
above covers the committed diff. The source-list capture initially needed
its `src=` records decoded; both recorded elaborations then completed at rc 0.

## Final state

- Local head: `f8a52f919bd309960046330a5af127b56731cb27`; parent is the assigned base.
- One-line commit subject, no body and no trailers.
- Worktree clean; processor worktree clean; gitlink unchanged at
  `870ff88ad35bbd532244e4c7e6d7661b9f6e1366`.
- All five tracked configurations build and keep counts 1/1/1.
  The assignment STOP condition was not triggered.
- No push, PR creation, merge, other checkout, hardware operation,
  firmware-source edit or processor-source edit was performed.
- `PR-BODY.md` and `REVIEW-READY.md` contain the prepared public text.
  Posting REVIEW READY on issue #571 is the final authorized action.
- Reviewers remain [R356] (internal) and [R357] (external).
  This packet contains test evidence, not an approval.
- The assigned `docs/spec-refs.md` remains unavailable, as recorded above.
  No unresolved implementation decision was introduced.
