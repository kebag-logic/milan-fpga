[A366] REVIEW READY

Commit: `499b15f97eb0a469b7cd1308fbba7af3c64d1851` (local head), branch `580-pp-pin-16be6768`, base `682ecf0cb995473b72d5b4921088053ba753fc93`.
Independent reviewers: [R352] and [R353].

Changed: processor gitlink `870ff88a` -> `16be6768`; two new ROM ledger rows with all prior rows retained; assigned packer-test disposition; F7 enforcement record; pin text, boundary renders/manifest and changelog; capture receipt pin.

Acceptance criteria: met for the assigned local author work. All five AEM images, their maps/JSON and all 50 builder outputs are byte-identical between pins. No parent RTL or firmware change was committed.

Capture decision: no remeasurement required. `scripts/check_nvm_capture.py:32` derives census and clock inputs; `check_receipt` at line 58 compares them, product firmware and harness hashes and regrades the recorded rows. It never reads `processor_pins`. The check passed with the adopted pin. The retained 8x8/50 MHz maximum is 24.30246 ms, below 24.5 ms; this is retained evidence, not a new measurement. The conditional STOP was not triggered.

Validation: every assigned command returned rc 0, from the physical worktree, in the foreground and without a pipeline.

| Gate | Command | rc |
|---|---|---:|
| builder-rv32 | `python3 sw/builder/test_builder.py --require-rv32` | 0 |
| builder-absent | `python3 builder_absent.py` | 0 |
| rom-check | `syn/yosys/ooc.sh KL_chan_map_render` | 0 |
| capture | `python3 scripts/check_nvm_capture.py` | 0 |
| test-evidence | `python3 scripts/measure_test_evidence.py --check` | 0 |
| port-contracts | `python3 scripts/check_port_contracts.py` | 0 |
| pp-shadow | `make -C tb/verilator/pp_shadow` | 0 |
| milan-dp | `make -C tb/verilator/milan_dp` | 0 |
| docs_check | `python3 scripts/docs_check.py` | 0 |
| check_doc_style | `python3 scripts/check_doc_style.py` | 0 |
| check_submodule_docs | `python3 scripts/check_submodule_docs.py` | 0 |
| check_diagram_pngs | `python3 scripts/check_diagram_pngs.py` | 0 |
| gen_toc-check | `python3 scripts/gen_toc.py --check` | 0 |
| check_em_dash-base | `python3 scripts/check_em_dash.py --base 682ecf0cb995473b72d5b4921088053ba753fc93` | 0 |
| diff-check | `git diff --check 682ecf0cb995473b72d5b4921088053ba753fc93 HEAD` | 0 |
| worktree-diff-check | `git diff --check` | 0 |

Both builder modes ran all 86 top-level tests, in the exact normal-entry order.
The compiler-present run has one NOT RUN arm: gate 11's absent external
calibration report. Absent mode additionally marks the RV32-dependent instruments
as NOT RUN. These are recorded limits, not passing claims for those arms.
The wrapper suite passed 2,068 checks across all four default legs.
The datapath ran 14 normal simulation legs with 11,196 checks and zero failures,
followed by its required render and grandmaster-step mutation campaigns.
The documentation set also includes the generation guide's required checks and
self-tests, reference paths, feature status, traceability, Contents/anchors,
archive, solution/submodule references and decoded raster checks. The generated
PNG, direct editable-master export and A4 print were visually inspected.

The absent run used the complete normal main entry with only the three compiler
candidate calls reporting their deliberate absence. Reproduction wrapper:

<details><summary>Compiler-absent wrapper</summary>

```python
"""Run the complete builder bank with RV32 compiler candidates unavailable."""
from pathlib import Path
import runpy
import subprocess
import sys
from unittest.mock import patch

ROOT = Path.cwd()
CROSS = {str(Path.home() / 'br-milan-rv32/host/bin/riscv32-linux-gcc'),
         'riscv64-elf-gcc', 'riscv32-unknown-elf-gcc'}
original_run = subprocess.run
hidden = set()

def absent(argv, **kwargs):
    if str(argv[0]) in CROSS:
        hidden.add(str(argv[0]))
        print('HIDDEN RV32 CANDIDATE', argv[0], flush=True)
        raise FileNotFoundError('deliberately absent RV32 candidate')
    return original_run(argv, **kwargs)

sys.path.insert(0, str(ROOT/'sw/builder'))
sys.argv = [str(ROOT/'sw/builder/test_builder.py')]
with patch.object(subprocess, 'run', side_effect=absent):
    result = runpy.run_path(sys.argv[0], run_name='__main__')
assert hidden == CROSS, hidden
assert any('THREE INSTRUMENTS' in why for _, why, _ in result['SKIPPED'])
print('PASS: full builder bank completed with all RV32 candidates absent')

```

</details>

<details><summary>ROM ledger rows</summary>


`ooc.sh --record-rom-digests` recorded the new rows. Older rows are retained.
The new processor digests equal the old pin's digests.
The unchanged gPTP row was re-recorded by the same command.

| Processor pin | Image | SHA256 |
|---|---|---|
| `16be6768f710e79450aace277abacd6c2c3336e5` | `ltn_rom.hex` | `23cc67eeadc7ecad8c9ceb7f9391095b64ada44d4e0f3a232ce82a2a69e7e956` |
| `16be6768f710e79450aace277abacd6c2c3336e5` | `ucode.hex` | `23605682298004274d80437a4ad83640c2d70e4fc161b23defb7c6eab6fa7144` |
| `5dce647ab5a01a6ecff9a982b22e3a4a1d946d3d` | `gptp_ucode.hex` | `c496ed8af59edd424e7d980aa3442bb725c745f44469ce53ec3a4d219fa30371` |
| `870ff88ad35bbd532244e4c7e6d7661b9f6e1366` | `ltn_rom.hex` | `23cc67eeadc7ecad8c9ceb7f9391095b64ada44d4e0f3a232ce82a2a69e7e956` |
| `870ff88ad35bbd532244e4c7e6d7661b9f6e1366` | `ucode.hex` | `23605682298004274d80437a4ad83640c2d70e4fc161b23defb7c6eab6fa7144` |


</details>

<details><summary>Five-configuration SHA256 evidence</summary>


The same physical parent worktree generated both sets, first at the old pin,
then at the new pin. No second checkout or tree export was used.
`measure_artifacts.py` records the exact commands, every file size and SHA256,
and checks actual bytes after the hash comparison. `old-artifacts.json` and
`new-artifacts.json` hold independent measurements. Each configuration's ten
builder outputs and its AEM image, map and JSON were byte-identical: 65 files.

Commands for each `configs/endstation_*.yaml`:

```sh
python3 sw/builder/endstation_builder.py configs/endstation_<name>.yaml -o <run>/builder
python3 avdecc/gen_aemi_image.py --overlay <run>/builder/endstation_<name>/aem_overlay.json --line-bytes 576 -o <run>/aem.bin -m <run>/aem.map --json <run>/aem.json
```

All 20 generator commands returned rc 0. Tables below use one digest column
because each SHA256 was measured equal at both pins.

| Configuration | AEM bytes | Old pin = new pin SHA256 |
|---|---:|---|
| `endstation_arty_4x4` | 10112 | `1b288e13ccbf03410c593a53bc22f4a68e3d289eef8a7f907e63bc98a51415ff` |
| `endstation_arty_8ch` | 15360 | `2b5c008cf3a2ff1eca11ef5e24c5a2e391e97f25435854430e563758de516b9b` |
| `endstation_arty_current` | 5792 | `ac833c3ccde42a2d9a78b517d660b9f7da03c4b3d31227aa65dcaf9e8def6192` |
| `endstation_ax7101_1x1_tdm8` | 7352 | `9b077636b1d42aca660b16dce8eafa06f1e3cac842134e51ba65930d16214404` |
| `endstation_ax7101_8x8` | 18288 | `193bf18736d23256c1b25d9af1bddb0721d95780fb36a14cf5f91476aff1a2d4` |

### endstation_arty_4x4

| Artifact | Bytes | Old pin = new pin SHA256 |
|---|---:|---|
| `aem.bin` | 10112 | `1b288e13ccbf03410c593a53bc22f4a68e3d289eef8a7f907e63bc98a51415ff` |
| `aem.json` | 20716 | `0ea2e47927e0a0eff12d781d979a255c39a935b7f06e07366d9ab3ff368d4e3e` |
| `aem.map` | 1311 | `09cf3da5a39730c1acedae4f09474c2d98d1aa17d8fa36f0238adc210fdaa571` |
| `builder/adp_shape_defaults.svh` | 7562 | `f5539f2c29b0ab0440be88f5985ba41bebb508bede7095e5387a03721e50a418` |
| `builder/aecp_aem_rom.svh` | 52444 | `1cd6c92190c1b4f8c14783423a1618328e2fbefe286ab78edb00f96adb45f59d` |
| `builder/aem_overlay.json` | 11920 | `a9b9d900fb425e95e2b3728b47bc5c10b7d7f6b1027be1758f27b01b00b8f98c` |
| `builder/build_plan.md` | 11000 | `c040b872fa0102576fccf0f235cd9436722efd9f66cf885b220a5dfcd502d722` |
| `builder/gptp_ucode.hex` | 13312 | `09f5d05defa759905f23630affc619d6af658e4c5f20aa0f63cc65f41317e651` |
| `builder/lwsrp_csr_defaults.svh` | 2183 | `90d4615e95883d5c1fdf5ce4eb8e716ac655114d8f0eb9e5579ec8e671bbfa88` |
| `builder/lwsrp_table.json` | 4084 | `90e1aa992317980e97ec42768d524e9b8af65e2279a31e1696f5f68254f05221` |
| `builder/lwsrp_table.svh` | 4288 | `36331d96c16b57ba3660a3183af58752195d94f2681d03ccfcf50003f227b222` |
| `builder/platform_shape.json` | 246 | `bbd040ba298a66ff0bd856f8f0b4e75c04c1831ba635a5b3ad756625ab8b0a28` |
| `builder/soc_params.json` | 589 | `fe552b1ec220f349b55cd499bc62680e9f7abf28397125cc457fd7cf63f61fb8` |

### endstation_arty_8ch

| Artifact | Bytes | Old pin = new pin SHA256 |
|---|---:|---|
| `aem.bin` | 15360 | `2b5c008cf3a2ff1eca11ef5e24c5a2e391e97f25435854430e563758de516b9b` |
| `aem.json` | 31200 | `22d2815009a4d468faf1d48322b57e5ef2f6260d34219299810b7e5aafaced18` |
| `aem.map` | 1311 | `163d5a414e34591ad639c3682747a35c43db64dcb3d46cb06c77d4c33edb634a` |
| `builder/adp_shape_defaults.svh` | 7836 | `41c02ad55f431ac15262d8a5db8e4a24945d375f217f7f0e552cd0b3f18cdd89` |
| `builder/aecp_aem_rom.svh` | 71921 | `19dd262b93e56aeab1641f3d3e534fc7af372f1c2f8c1801e5a7895d1982ae34` |
| `builder/aem_overlay.json` | 16978 | `87fc3c51e2fc5a49b91d67e05ea621449391619430ecfaef4cac5422b5b4b94e` |
| `builder/build_plan.md` | 11003 | `1a93c95f35d176c5b52e03c1f0d5ccea7726c682a803948a5763029a509edf76` |
| `builder/gptp_ucode.hex` | 13312 | `09f5d05defa759905f23630affc619d6af658e4c5f20aa0f63cc65f41317e651` |
| `builder/lwsrp_csr_defaults.svh` | 2183 | `f2519804843397b4bde6393e3be67f348e3b3ef6e73e62fef22b3a71b4ecf87f` |
| `builder/lwsrp_table.json` | 4084 | `0e151e2854b3799281d19d01e67c27b04a53ca470a672ad27bc48f93ea840987` |
| `builder/lwsrp_table.svh` | 4288 | `c7189e2e3dcf79a7fcd6c204674fca581d89aea327c77b65ea7aa57f38aa3e19` |
| `builder/platform_shape.json` | 246 | `b818b72a035c5f73870925ffe208eda20292bedc629a399d5d31aa14160242ce` |
| `builder/soc_params.json` | 589 | `7a10be52746259e11e1c43402cb8097ca5234e9b358fd6160af5c5e42673faff` |

### endstation_arty_current

| Artifact | Bytes | Old pin = new pin SHA256 |
|---|---:|---|
| `aem.bin` | 5792 | `ac833c3ccde42a2d9a78b517d660b9f7da03c4b3d31227aa65dcaf9e8def6192` |
| `aem.json` | 11356 | `3c4b9440bccdc59198dacbc073fbb01671dec866d5adcf1b98225c8b6f822057` |
| `aem.map` | 1310 | `77dad531965096987d682f77e93f81e5b6f182eaae879fb43b084be8570bec4c` |
| `builder/adp_shape_defaults.svh` | 7089 | `54f350a99a0e6883f394858fe12457cffb4a1fea08ae23f5ba42c02636a46c98` |
| `builder/aecp_aem_rom.svh` | 33428 | `d8365928caecf01dc79b3d9a75a6c56573669ad121d8cc04b42f44820601c999` |
| `builder/aem_overlay.json` | 6238 | `12f48ab98be36408d6090158d5fc27341ca72d53217fcf892e097fbadab4e70e` |
| `builder/build_plan.md` | 9105 | `4eb5e433433f1c3af1311a4585c9a80101178766c8aa9f7573a75d3e034167bf` |
| `builder/gptp_ucode.hex` | 13312 | `09f5d05defa759905f23630affc619d6af658e4c5f20aa0f63cc65f41317e651` |
| `builder/lwsrp_csr_defaults.svh` | 2187 | `d10ce5559b108f54800b8432b672a0d33379721bf2a4edf0058e185484f3881d` |
| `builder/lwsrp_table.json` | 2274 | `dc4a200fa4dae047598419a78713677aefeab85b957808b9ec7284f2411a668f` |
| `builder/lwsrp_table.svh` | 3826 | `df3c4fa0289d23deea8f8e688573faa1adbb12f8485a7b5613bd30b8b288f8e4` |
| `builder/platform_shape.json` | 250 | `03328f238565f45f775a8fb17921a20ac4172d864b218e3703c23e185e678c99` |
| `builder/soc_params.json` | 498 | `696350eee365adb614b78e445d6522569e73d0eaa555b4de6603319d45da59cb` |

### endstation_ax7101_1x1_tdm8

| Artifact | Bytes | Old pin = new pin SHA256 |
|---|---:|---|
| `aem.bin` | 7352 | `9b077636b1d42aca660b16dce8eafa06f1e3cac842134e51ba65930d16214404` |
| `aem.json` | 14387 | `679d8286a0151b921aa1c6d38370c7c231020f1a5c75a85e565fce9fe1ba0c17` |
| `aem.map` | 1243 | `07151f7c4b493da8e1d3fea32a7e9755951d8e97e021e040ef2a9f3899cb7ede` |
| `builder/adp_shape_defaults.svh` | 7199 | `eb03dfaa2f914f49b07c31ddcc62ebc4a64e839a466a3387650f25823afb1020` |
| `builder/aecp_aem_rom.svh` | 40979 | `deea618d789b235c532edc47db08838afc7ffc2f74953f1a117d1fb2c7bd5d33` |
| `builder/aem_overlay.json` | 7196 | `e148841ac36dbf3e6d6729c49c7c944ed5194adc75941ceb69e3af80b11e3621` |
| `builder/build_plan.md` | 10825 | `203c4859f9557b4a250454fe9e0561706cc581708811988cd926edda9b942858` |
| `builder/gptp_ucode.hex` | 13312 | `78c8418a00b35cdae75c459c5269ca3892355507c4dc8af9eb2c29d81b87673b` |
| `builder/lwsrp_csr_defaults.svh` | 2190 | `0e9df2d455d90782c87546dab4dd1fe7b5fb7f4bc81074e910ba71ddc7016d74` |
| `builder/lwsrp_table.json` | 2289 | `61b2e71d9a40c61bfb0eaf884af6257b1b030e441c5f507f99720d0c18dad47d` |
| `builder/lwsrp_table.svh` | 3832 | `8209fdee3cd744d24a066b76017f71f16d87f636c4470eb95e9f986dce550522` |
| `builder/platform_shape.json` | 253 | `0325a3cc988f7f97b34997ef3ac53c6624edfc62b0bd4b5ffb42dc72894ddae7` |
| `builder/soc_params.json` | 799 | `d5ec9866f86c339dc1c178c31c7800a359813660d9cbcc95e242e1e29b13c516` |

### endstation_ax7101_8x8

| Artifact | Bytes | Old pin = new pin SHA256 |
|---|---:|---|
| `aem.bin` | 18288 | `193bf18736d23256c1b25d9af1bddb0721d95780fb36a14cf5f91476aff1a2d4` |
| `aem.json` | 37534 | `50eaefa69bcad009479d1d7df3ced08f26b319d1a91dfe2ce659ef97c53620ad` |
| `aem.map` | 1244 | `14d38a422d09d4b729032b19cfeb515756b30156c22f65df842184956ffd989f` |
| `builder/adp_shape_defaults.svh` | 8449 | `26a61e545097a577f1b6bae2e15e92c867e4143a8f8ceb13e2abc21d03279333` |
| `builder/aecp_aem_rom.svh` | 86567 | `9f6963190256809964376e8747ebc3465d4b4831df01ec3d91c7e8892e46d755` |
| `builder/aem_overlay.json` | 20163 | `baef8bb15a57606b047e657c8ba50460d7f806983a0e08bf24432fc32435fb0c` |
| `builder/build_plan.md` | 15175 | `2d303d06c5fc2f13648734ea1cb9660963bf745e73ee312476cc3a10c914a20e` |
| `builder/gptp_ucode.hex` | 13312 | `78c8418a00b35cdae75c459c5269ca3892355507c4dc8af9eb2c29d81b87673b` |
| `builder/lwsrp_csr_defaults.svh` | 2185 | `c9849c561b9aab3f682e2974ce1ba81443c2696a0c1a4e53d3975f2557c159c4` |
| `builder/lwsrp_table.json` | 6496 | `b525824ef9b4a7c52bc99946b08807708f5c7a0ac9087d20a0cc62f3b5e95266` |
| `builder/lwsrp_table.svh` | 4917 | `eed72271ec9a0e3d68b8ca9f367d83251140c5464272a65ef0843a00ce95525e` |
| `builder/platform_shape.json` | 248 | `a08aef1e775ecd345a7f87157f4bf3eed28306250d49003d0c5231e714e6cf17` |
| `builder/soc_params.json` | 786 | `41763d46738df0e907116212b9bedb85beebba34f6a66057bee0d921321ef823` |


</details>

<details><summary>Final gate log identities</summary>

| Gate | Bytes | SHA256 |
|---|---:|---|
| old-artifacts | 25606 | `f6481537122c97e5d0daf3f8a5b082941cc1be99eb9531620219edfe55b34103` |
| new-artifacts | 25687 | `2e9204ef28680bb9a4b8958809d9cd460742b2f5b6b86aa1643bb4873ab8ab12` |
| rom-record | 198 | `936104f286f7661ce4d5d05a5654a687bf07aa16e19066355151b5ce19c395d0` |
| capture | 324 | `9a4196c774ce4ddfa9980cf9345d111028f3afa812677fe5bab392f81c955439` |
| rom-check | 299 | `96813b468620e139df7f940979bc84641f5bf8519a2a70ae3334e010957bc2eb` |
| test-evidence | 10961 | `bcf70fde889a7765d72f22e992e88b6f7ce0372f2207813c2bd34dc30ba48428` |
| port-contracts | 421 | `eed4188366eced1ee727819ad607f9af837b98bee5d2ec97d18f375cdb0b00fd` |
| packer-tests | 947 | `8e380633a779cca26f6a1adcf799be046cd80cc8e80f1a2bfd58d99ca5144189` |
| py-idiom | 461 | `9dc0e09bb9cfdde0b8ee795fffa2c63fe626abe43385129f5f1a138f4a265287` |
| diagram-check | 54 | `905777610f39981543faabafcc11309ac6ab670121c8866a45e171e5c9b7d00c` |
| diagram-selftest | 60 | `51bca8fb66fd6f0acc480e3364f74fd7a4874946b191468bfbe20ad159cca889` |
| docs_check | 127 | `84a84432d8adfff3fb83b714ee2e07a9290c6406f11229400a2e0a34ef4c0198` |
| docs_check-selftest | 56 | `83cb6b9c5f7a556a8ea31ad3a751a39e6d573b00fe44ac39f5e1591022048339` |
| check_em_dash-base | 139 | `dc4fbb399c6357d6c2aa42da1af2b17047f580bb0ae2a34a0ecd77dab4e73f3a` |
| check_em_dash-selftest | 42 | `46aaf33b1a5f1d99dba778a65e86a452bbd5642cde32cf136a7a8e1721f7a19a` |
| check_doc_style | 47 | `1491d3f6bec03b920cf58f5fb28e6abff4a9d433a758bc0fe5d2db77bf4f53cd` |
| check_doc_style-selftest | 33 | `0acc8195c60dd145a8f17d24b7b07c29074ac131d71893f9cef5f880239dd909` |
| check_gptp_docs | 41 | `d8a77a32600566f0613626fd361bad845759693a08b1095dd54865c1aa25455d` |
| check_gptp_docs-selftest | 46 | `200332e4eddfd8a6338d8a4dbe27d2f513de92f951a1aa1f6b25882182bc290e` |
| check_solution_docs | 87 | `48ac84ddbd532247deb21834ee60bd4b7322f69bb9ab9fc5f9901969ccb38c42` |
| check_solution_docs-selftest | 59 | `c57d3ed2e5c9be43085106227b69fe55f866b1198ad209fbb27f940e5757ec30` |
| check_submodule_docs | 47 | `dffc750855c2574e23bad0174564fcde9dc0d351b65e2f5e954f2dc64e894835` |
| check_submodule_docs-selftest | 66 | `54dbecff3ad17dc651e86c7b313ef57fa96baf89fb40f0fb90af4bbb8ddc802b` |
| check_diagram_pngs | 66 | `05e0fcfa26a97494e8983dcfca3ad89cdaf91e390acbfb9dbdfb6f614cba4e51` |
| check_diagram_pngs-selftest | 59 | `918e8cc85a2a2b0d45eeb3f0c7b006824c81e2ed404a535eded095b09d875dc5` |
| check_archive | 93 | `69d45782911c2958be2fef681f849e9b3915293c938de331bb6885dab21fd46c` |
| check_archive-selftest | 35 | `83aa5efe967935657a1678bf63262a7c435d29d571cc08dd2ae8cf6f8569d34a` |
| gen_hdl_reference-selftest | 385 | `3b89a1b5a5d26c89b15d883724481fb2d40d5e02853a711f7b77150155760ff0` |
| check_doc_paths | 84 | `095a3297a6597fc768401cd8e85340a8400511da1d1df735b0e717e6ccc02105` |
| check_feature_status-self-test | 1500 | `77f7649b1865c0daf4f3de04dd18c78be4885c9c94a8f03fd1e4f262758c3184` |
| gen_toc-selftest | 38 | `d7fd5f6ebcdd25e6cf93b623b0fba00cfa32d19c812ce34eb6b8d8b352ac9b32` |
| gen_toc-verify-anchors | 64 | `f06944107d85564cb11bb5da8e7bae4313631a6599d1f0d826eee6e1b8d9def6` |
| gen_toc-check | 94 | `809c4d1d747037e3abf90b86d58f95a8830965a48f302e5107fde95e0bbea028` |
| timesync-check | 60 | `51058c96a481bf763246394b619601227bdec11b6b11ddcaa1d6f57593d2f1f4` |
| timesync-selftest | 61 | `7c7ad79fa685d29607abf71e3a99d98855fd7ffa1ba5fbf7de23bfb41a33c8fa` |
| module-matrix | 118 | `cc9edd89394353084471aad6ea6b5f2e292b331712a07fa90ca9beb934a0e2d7` |
| doc-map-check | 61 | `74408f0fbcdfc1c7e22f6eccd3eb299da61cabe9bb4526eed416b31a8bf61e16` |
| doc-map-selftest | 60 | `85ddf25d9a99974b71a9c165cbfbbf390be3d7bf74f081b4cc669622a0a562b9` |
| builder-rv32 | 84499 | `81af49af7b9b9b74f7b8ab560bbc5856cd086541746fc20d046795a9b5f18fec` |
| builder-absent | 86750 | `8d70400c1aa1101f2b8ce13886d340625daae76377e1e4fe267a1e685a79473c` |
| pp-shadow | 284323 | `87cbf436707b62ca34095ff18ad245f34c961a1e6640bcef71a05b9c11de06ff` |
| milan-dp | 1959014 | `c8b6a3fc71e2822503b72a73800963bd35ef8ec77c1c3c6b524c31573e48945c` |
| diff-check | 47 | `ed658cc2701b76b948a5c9308b123bc927a68ee04fbe54746d47d779d0d14f7c` |
| worktree-diff-check | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |

</details>

Open risks/questions: the recorded calibration limit above; independent review remains pending. Local handoff and PR body are prepared. Publication and PR operations remain with the next authorized step.
