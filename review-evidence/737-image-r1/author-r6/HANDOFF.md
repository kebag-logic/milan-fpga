[A615]

# Image lane handoff

Status: Round 6 IN PROGRESS for PR #738; relates to #737. No push or PR modification.
Round-six starting head: `4391f353690972f4844cb641b1e77fa94f38cdf4` (confirmed against origin).
Round-five starting head: `e355f789b4f59b86083809299134557ca47bbcfb`. Branch: `737-ci-image`. Source base: `fa7347fc59173f90e4feec2df207692e6e6e72ec`.
Round-three starting head: `18f2df92b13cb3f4036b073ed76940187bf10487`.

## Authority

Round five: assignment 6173370560; reviews R638-4 (6173357081) and R639-4 (6173248621).

Round four: assignment 6170435035, amendments 6170543242 and 6170640746; reviews R638-3 (6170421890) and R639-3 (6169543700). The latest amendment supersedes both prior scope STOPs.

Issue #737 assignment 6160953880; PR #738 round-three assignment 6167899804; amendment 6167966247 resolving STOP 6167951082; reviews R638-2 (6167893456) and R639-2 (6166908258). The round-two literal-mask ruling 6162190578 authorizes exact public host-tool URL literals in the existing image metadata files. No product scan scope or product-test assertion was changed.

## Round 3 (historical)

| Finding | Implementation and evidence |
|---|---|
| R638-2-F1 and R639-2-F1 | Closed table of 214 command names and 109 content-pinned script declarations. Followed Python network or subprocess users require installer or reviewed non-installing declarations. Unknown names/subcommands, undeclared scripts, changed declarations and missing literal script paths refuse. `scripts/ci_command_table.py:68`, `scripts/ci_tool_inventory.py:155`, `scripts/ci_tool_inventory_selftest.py:73`. |
| Runtime residue | Runtime command construction, indirect shells, evaluation and unresolved runtime paths are recorded in `ci/image/tool-inventory.json`, not silently certified. The guide states the static-analysis limit at `docs/testing/CI_IMAGE.md:37`. |
| R638-2-F2 | 185 Ubuntu package rows carry ordered timestamped fallbacks with unchanged size/SHA-256. All 185 fallback downloads were verified (`round3-snapshots.json`). HTTP-404 fallback and corrupt-byte controls pass. `ci/image/build.py:114`, `ci/image/resolve_packages.py:105`, `ci/image/build_selftest.py:31`. |
| R638-2-F3 | Config digest comes from the authenticated exported manifest. Cold builds use buildx v0.38.0 and the Docker driver with containerd storage. `ci/image/build.py:288`, `ci/image/image_archive.py:40`. |
| R638-2-F4 | Disposable fixture commits supply their own identity. The final-image self-test passes with no configured global/system identity. `ci/image/privacy_patch_selftest.py:17`; `round3-image-6.receipt.json`, `round3-image-10.receipt.json`. |
| R638-2-F5 | The guide documents the adopting job's home-relative SDK link and the actual `MILAN_RV32_CC` consumers. Fresh-HOME preflight resolves GCC 14.3.0 through that link. `docs/testing/CI_IMAGE.md:326`; `round3-image-10.receipt.json`. |

The generated inventory binds 296 input files and exposes 735 static-analysis residue entries for manual review. These entries are not certified as non-installing.

The parser prerequisite is shfmt v3.11.0, 2,916,536 bytes, SHA-256 `1904ec6bac715c1d05cd7f6612eec8f67a625c3749cb327e5bfb4127d09035ff`. It is a host prerequisite, not an additional image tool. `sources.lock.json` records it under `host_tools`; `prepare_parser.py` downloads and authenticates it, and the audit authenticates it before every use. The Bash parser supplies syntax only; candidate scripts are never executed by inventory derivation.

## Changes

| File:line | Change |
|---|---|
| `ci/image/Dockerfile:1` | Pinned base and distinct filesystem layers; fixed build epoch; documented runtime environment. |
| `ci/image/build.py:144` | Bind the recipe and each layer to exact inputs; clean allowlisted context; cold-build option; exported image identity and privacy verification before lock generation. |
| `ci/image/build_selftest.py:31` | Source, pin, duplicate, traversal, download and derived-CPU refusal controls. |
| `ci/image/image.lock.json:1` | Generated schema-2 manifest/config identity and logical-to-OCI layer bindings. |
| `ci/image/image_archive.py:40` | Authenticate metadata and every layer; inspect content, paths, link metadata, history and environment. |
| `ci/image/image_lock.py:27` | Validate complete schema and recomputed records; separate recipe consistency from artifact identity. |
| `ci/image/install.py:130` | Exact source installers; complete recursive CPU tree; separate Python and LiteX prefixes; minimal oracle runtime with its shared libraries. |
| `ci/image/integrity_selftest.py:96` | Lock/artifact and normalization refusal controls; unchanged parsed protocol data and scalar refusal. |
| `ci/image/normalize.py:15` | Remove only runtime-irrelevant protocol comments after equality proof; normalize timestamps, ownership and Java trust-store dates; discard transient files. |
| `ci/image/package_roots.json:1` | Consumer-bound runtime and recipe package roots, including SDK extractor and offline runner dependencies. |
| `ci/image/patch_provenance.py:22` | Authenticate pinned upstream members and committed patches, reproduce postimages, and allow matches only on unchanged upstream lines. |
| `ci/image/privacy.json:1` | Single protected identity/pattern table, without publishing literal private identities. |
| `ci/image/privacy.py:124` | Authenticate per-file public provenance, embedded wheels and whole public artifacts; reject first-party allowances. |
| `ci/image/privacy_patch_selftest.py:17` | Planted identity on a patch-added line is refused; unchanged upstream lines pass; changed archive, patch and postimage are refused. |
| `ci/image/privacy_selftest.py:18` | Identity-class, layer, metadata and provenance refusal controls, including nested wheel and whole-artifact controls. |
| `ci/image/resolve_base.py:14` | Regenerate base layers and package metadata from the authenticated pinned export. |
| `ci/image/resolve_git.py:22` | Resolve every recursive CPU gitlink from its pinned public parent tree. |
| `ci/image/resolve_maven.py:55` | Generate the complete public Scala closure and bootstrap placements; authenticate downloads before writing. |
| `ci/image/resolve_packages.py:19` | Derive workflow roots and closure from verified package metadata and the pinned base; check explicit runtime consumers. |
| `ci/image/sbt-repositories:1` | Public repositories for the pinned offline Scala cache. |
| `ci/image/smoke.py:25` | Check installed pins and binary-reported versions, then exercise every tool family offline; handle rollback-named package versions. |
| `ci/image/sources.lock.json:1` | Generated lock: 186 distribution packages, 479 public source artifacts, 423 Maven artifacts and 88 bootstrap placements. |
| `ci/image/tool-inventory.json:1` | Generated 45 workflow-derived tool requests with every installing step and reached-source digest. |
| `docs/README.md:88` | Index the image guide. |
| `docs/testing/CI_IMAGE.md:1` | Reproduction, pin generators, privacy proofs, environment, accepted runner deviations and adoption boundaries. |
| `scripts/check_baremetal_only.py:295` | Authorized file-bound literal masks; protected product documents and other files remain refused, with controls. |
| `scripts/ci_tool_inventory.py:169` | Derive workflow provenance through the closed command audit; record immutable job container/service references. |
| `scripts/ci_tool_inventory_selftest.py:73` | Planted installer/action/Makefile/string/variable and drift controls; harmless comparison data remains accepted. |
| `scripts/ci_command_table.py:68` | New closed command audit, Python declarations, Bash AST traversal and Makefile target traversal. |
| `ci/image/command-table.json:1` | Reviewed command forms and content-pinned script declarations. |
| `ci/image/prepare_parser.py:12` | Fetch the separately pinned host parser outside the source tree. |

## Derived tool inventory

All 45 requests below are generated from workflow installing steps. Unversioned requests resolve to the source lock. Additional runtime dependencies and recipe roots are declared with consumers in `ci/image/package_roots.json`. No workflow file changed.

| Tool | Requested pin / resolved pin | Workflow, job and installing step |
|---|---|---|
| python | `3.12` / `3.12.3` | `.github/workflows/elaborate.yml:elaborate` / actions/setup-python@v5 |
| autoconf | `unversioned` / `2.71-3` | `.github/workflows/elaborate.yml:elaborate` / Build Verilator from source on cache miss<br>`.github/workflows/rtl-fast.yml:verilator-lint` / Build Verilator from source on cache miss<br>`.github/workflows/rtl-fast.yml:firmware-verilator` / Build Verilator from source on cache miss<br>`.github/workflows/rtl.yml:verilator-shards` / Build Verilator from source on cache miss<br>`.github/workflows/rtl.yml:physical-gptp` / Build Verilator from source on cache miss |
| bison | `unversioned` / `2:3.8.2+dfsg-1ubuntu0.24.04.1` | `.github/workflows/elaborate.yml:elaborate` / Build Verilator from source on cache miss<br>`.github/workflows/rtl-fast.yml:verilator-lint` / Build Verilator from source on cache miss<br>`.github/workflows/rtl-fast.yml:yosys-elaboration` / Build Yosys from source on cache miss<br>`.github/workflows/rtl-fast.yml:publication-census` / Build Yosys from source on cache miss<br>`.github/workflows/rtl-fast.yml:firmware-verilator` / Build Verilator from source on cache miss<br>`.github/workflows/rtl.yml:verilator-shards` / Build Verilator from source on cache miss<br>`.github/workflows/rtl.yml:verilator-shards` / Build Yosys from source on cache miss<br>`.github/workflows/rtl.yml:physical-gptp` / Build Verilator from source on cache miss<br>`.github/workflows/rtl.yml:yosys-shards` / Build Yosys from source on cache miss |
| flex | `unversioned` / `2.6.4-8.2build1` | `.github/workflows/elaborate.yml:elaborate` / Build Verilator from source on cache miss<br>`.github/workflows/rtl-fast.yml:verilator-lint` / Build Verilator from source on cache miss<br>`.github/workflows/rtl-fast.yml:yosys-elaboration` / Build Yosys from source on cache miss<br>`.github/workflows/rtl-fast.yml:publication-census` / Build Yosys from source on cache miss<br>`.github/workflows/rtl-fast.yml:firmware-verilator` / Build Verilator from source on cache miss<br>`.github/workflows/rtl.yml:verilator-shards` / Build Verilator from source on cache miss<br>`.github/workflows/rtl.yml:verilator-shards` / Build Yosys from source on cache miss<br>`.github/workflows/rtl.yml:physical-gptp` / Build Verilator from source on cache miss<br>`.github/workflows/rtl.yml:yosys-shards` / Build Yosys from source on cache miss |
| g++ | `unversioned` / `4:13.2.0-7ubuntu1` | `.github/workflows/elaborate.yml:elaborate` / Build Verilator from source on cache miss<br>`.github/workflows/rtl-fast.yml:verilator-lint` / Build Verilator from source on cache miss<br>`.github/workflows/rtl-fast.yml:yosys-elaboration` / Build Yosys from source on cache miss<br>`.github/workflows/rtl-fast.yml:publication-census` / Build Yosys from source on cache miss<br>`.github/workflows/rtl-fast.yml:firmware-verilator` / Build Verilator from source on cache miss<br>`.github/workflows/rtl.yml:verilator-shards` / Build Verilator from source on cache miss<br>`.github/workflows/rtl.yml:verilator-shards` / Build Yosys from source on cache miss<br>`.github/workflows/rtl.yml:physical-gptp` / Build Verilator from source on cache miss<br>`.github/workflows/rtl.yml:yosys-shards` / Build Yosys from source on cache miss |
| git | `unversioned` / `1:2.43.0-1ubuntu7.3` | `.github/workflows/elaborate.yml:elaborate` / Build Verilator from source on cache miss<br>`.github/workflows/rtl-fast.yml:verilator-lint` / Build Verilator from source on cache miss<br>`.github/workflows/rtl-fast.yml:yosys-elaboration` / Build Yosys from source on cache miss<br>`.github/workflows/rtl-fast.yml:publication-census` / Build Yosys from source on cache miss<br>`.github/workflows/rtl-fast.yml:firmware-verilator` / Build Verilator from source on cache miss<br>`.github/workflows/rtl.yml:verilator-shards` / Build Verilator from source on cache miss<br>`.github/workflows/rtl.yml:verilator-shards` / Build Yosys from source on cache miss<br>`.github/workflows/rtl.yml:physical-gptp` / Build Verilator from source on cache miss<br>`.github/workflows/rtl.yml:yosys-shards` / Build Yosys from source on cache miss |
| help2man | `unversioned` / `1.49.3` | `.github/workflows/elaborate.yml:elaborate` / Build Verilator from source on cache miss<br>`.github/workflows/rtl-fast.yml:verilator-lint` / Build Verilator from source on cache miss<br>`.github/workflows/rtl-fast.yml:firmware-verilator` / Build Verilator from source on cache miss<br>`.github/workflows/rtl.yml:verilator-shards` / Build Verilator from source on cache miss<br>`.github/workflows/rtl.yml:physical-gptp` / Build Verilator from source on cache miss |
| libfl-dev | `unversioned` / `2.6.4-8.2build1` | `.github/workflows/elaborate.yml:elaborate` / Build Verilator from source on cache miss<br>`.github/workflows/rtl-fast.yml:verilator-lint` / Build Verilator from source on cache miss<br>`.github/workflows/rtl-fast.yml:yosys-elaboration` / Build Yosys from source on cache miss<br>`.github/workflows/rtl-fast.yml:publication-census` / Build Yosys from source on cache miss<br>`.github/workflows/rtl-fast.yml:firmware-verilator` / Build Verilator from source on cache miss<br>`.github/workflows/rtl.yml:verilator-shards` / Build Verilator from source on cache miss<br>`.github/workflows/rtl.yml:verilator-shards` / Build Yosys from source on cache miss<br>`.github/workflows/rtl.yml:physical-gptp` / Build Verilator from source on cache miss<br>`.github/workflows/rtl.yml:yosys-shards` / Build Yosys from source on cache miss |
| libfl2 | `unversioned` / `2.6.4-8.2build1` | `.github/workflows/elaborate.yml:elaborate` / Build Verilator from source on cache miss<br>`.github/workflows/rtl-fast.yml:verilator-lint` / Build Verilator from source on cache miss<br>`.github/workflows/rtl-fast.yml:firmware-verilator` / Build Verilator from source on cache miss<br>`.github/workflows/rtl.yml:verilator-shards` / Build Verilator from source on cache miss<br>`.github/workflows/rtl.yml:physical-gptp` / Build Verilator from source on cache miss |
| libgmock-dev | `unversioned` / `1.14.0-1` | `.github/workflows/rtl-fast.yml:firmware-unit` / Install GoogleTest and GoogleMock and print the versions<br>`.github/workflows/rtl-fast.yml:firmware-control-mutants` / Install GoogleTest and GoogleMock and print the versions<br>`.github/workflows/rtl-fast.yml:firmware-aecp-mutants` / Install GoogleTest and GoogleMock and print the versions<br>`.github/workflows/rtl-fast.yml:firmware-srp-mutants` / Install GoogleTest and GoogleMock and print the versions<br>`.github/workflows/rtl-fast.yml:firmware-boundary` / Install GoogleTest and GoogleMock and print the versions<br>`.github/workflows/rtl-fast.yml:firmware-verilator` / Install GoogleTest and GoogleMock and print the versions |
| libgtest-dev | `unversioned` / `1.14.0-1` | `.github/workflows/rtl-fast.yml:firmware-unit` / Install GoogleTest and GoogleMock and print the versions<br>`.github/workflows/rtl-fast.yml:firmware-control-mutants` / Install GoogleTest and GoogleMock and print the versions<br>`.github/workflows/rtl-fast.yml:firmware-aecp-mutants` / Install GoogleTest and GoogleMock and print the versions<br>`.github/workflows/rtl-fast.yml:firmware-srp-mutants` / Install GoogleTest and GoogleMock and print the versions<br>`.github/workflows/rtl-fast.yml:firmware-boundary` / Install GoogleTest and GoogleMock and print the versions<br>`.github/workflows/rtl-fast.yml:firmware-verilator` / Install GoogleTest and GoogleMock and print the versions |
| libjemalloc2 | `unversioned` / `5.3.0-2build1` | `.github/workflows/rtl.yml:verilator-shards` / Install the pinned Yosys and prove the version<br>`.github/workflows/rtl.yml:yosys-shards` / Install the pinned Yosys and prove the version |
| librsvg2-bin | `unversioned` / `2.58.0+dfsg-1ubuntu0.1` | `.github/workflows/docs.yml:docs-check` / Install diagram gate dependencies |
| make | `unversioned` / `4.3-4.1build2` | `.github/workflows/elaborate.yml:elaborate` / Build Verilator from source on cache miss<br>`.github/workflows/rtl-fast.yml:verilator-lint` / Build Verilator from source on cache miss<br>`.github/workflows/rtl-fast.yml:yosys-elaboration` / Build Yosys from source on cache miss<br>`.github/workflows/rtl-fast.yml:publication-census` / Build Yosys from source on cache miss<br>`.github/workflows/rtl-fast.yml:firmware-verilator` / Build Verilator from source on cache miss<br>`.github/workflows/rtl.yml:verilator-shards` / Build Verilator from source on cache miss<br>`.github/workflows/rtl.yml:verilator-shards` / Build Yosys from source on cache miss<br>`.github/workflows/rtl.yml:physical-gptp` / Build Verilator from source on cache miss<br>`.github/workflows/rtl.yml:yosys-shards` / Build Yosys from source on cache miss |
| perl | `unversioned` / `5.38.2-3.2ubuntu0.6` | `.github/workflows/elaborate.yml:elaborate` / Build Verilator from source on cache miss<br>`.github/workflows/rtl-fast.yml:verilator-lint` / Build Verilator from source on cache miss<br>`.github/workflows/rtl-fast.yml:firmware-verilator` / Build Verilator from source on cache miss<br>`.github/workflows/rtl.yml:verilator-shards` / Build Verilator from source on cache miss<br>`.github/workflows/rtl.yml:physical-gptp` / Build Verilator from source on cache miss |
| pkg-config | `unversioned` / `1.8.1-2build1` | `.github/workflows/rtl-fast.yml:yosys-elaboration` / Build Yosys from source on cache miss<br>`.github/workflows/rtl-fast.yml:publication-census` / Build Yosys from source on cache miss<br>`.github/workflows/rtl.yml:verilator-shards` / Build Yosys from source on cache miss<br>`.github/workflows/rtl.yml:yosys-shards` / Build Yosys from source on cache miss |
| python3 | `unversioned` / `3.12.3-0ubuntu2.1` | `.github/workflows/elaborate.yml:elaborate` / Build Verilator from source on cache miss<br>`.github/workflows/rtl-fast.yml:verilator-lint` / Build Verilator from source on cache miss<br>`.github/workflows/rtl-fast.yml:yosys-elaboration` / Build Yosys from source on cache miss<br>`.github/workflows/rtl-fast.yml:publication-census` / Build Yosys from source on cache miss<br>`.github/workflows/rtl-fast.yml:firmware-verilator` / Build Verilator from source on cache miss<br>`.github/workflows/rtl.yml:verilator-shards` / Build Verilator from source on cache miss<br>`.github/workflows/rtl.yml:verilator-shards` / Build Yosys from source on cache miss<br>`.github/workflows/rtl.yml:physical-gptp` / Build Verilator from source on cache miss<br>`.github/workflows/rtl.yml:yosys-shards` / Build Yosys from source on cache miss |
| tcl | `unversioned` / `8.6.14build1` | `.github/workflows/docs.yml:docs-check` / SoC source-list gate (Vivado would fail 40 min in without this)<br>`.github/workflows/rtl-fast.yml:yosys-elaboration` / Prove the OOC read sets come from run.sh and refuse a bad one |
| zlib1g-dev | `unversioned` / `1:1.3.dfsg-3.1ubuntu2.2` | `.github/workflows/rtl-fast.yml:yosys-elaboration` / Build Yosys from source on cache miss<br>`.github/workflows/rtl-fast.yml:publication-census` / Build Yosys from source on cache miss<br>`.github/workflows/rtl.yml:verilator-shards` / Build Yosys from source on cache miss<br>`.github/workflows/rtl.yml:yosys-shards` / Build Yosys from source on cache miss |
| sv2v | `v0.0.12` / `v0.0.12` | `.github/workflows/docs.yml:docs-check` / Install the pinned sv2v release<br>`.github/workflows/elaborate.yml:elaborate` / Install the pinned sv2v release<br>`.github/workflows/rtl-fast.yml:yosys-elaboration` / Install the pinned sv2v release<br>`.github/workflows/rtl-fast.yml:publication-census` / Install the pinned sv2v release<br>`.github/workflows/rtl.yml:verilator-shards` / Install sv2v for the netlist-level suite owner<br>`.github/workflows/rtl.yml:yosys-shards` / Install the pinned sv2v release |
| sbt | `v1.10.7` / `1.10.7` | `.github/workflows/elaborate.yml:elaborate` / Install sbt |
| VexiiRiscv | `235753e24f2d960e49a0852205bae1400bf22c19` / `235753e24f2d960e49a0852205bae1400bf22c19` | `.github/workflows/elaborate.yml:elaborate` / Place the VexiiRiscv source at the revision LiteX pins |
| litespi | `02d5a209bc0010d33ddb506ba18e736636d4109a` / `02d5a209bc0010d33ddb506ba18e736636d4109a` | `.github/workflows/elaborate.yml:elaborate` / Install LiteX at the pinned revisions<br>`.github/workflows/rtl-fast.yml:firmware-boundary` / Install GoogleTest and GoogleMock and print the versions |
| pythondata-cpu-vexiiriscv | `15cfab529a17c473d0fc75edf3f409eb374cef35` / `15cfab529a17c473d0fc75edf3f409eb374cef35` | `.github/workflows/elaborate.yml:elaborate` / Install LiteX at the pinned revisions<br>`.github/workflows/rtl-fast.yml:firmware-boundary` / Install GoogleTest and GoogleMock and print the versions |
| liteeth | `276c9e37fb4d92a5c0f30d39a51c20f42a59cf93` / `276c9e37fb4d92a5c0f30d39a51c20f42a59cf93` | `.github/workflows/elaborate.yml:elaborate` / Install LiteX at the pinned revisions<br>`.github/workflows/rtl-fast.yml:firmware-boundary` / Install GoogleTest and GoogleMock and print the versions |
| migen | `4c2ae8dfeea37f235b52acb8166f12acaaae4f7c` / `4c2ae8dfeea37f235b52acb8166f12acaaae4f7c` | `.github/workflows/elaborate.yml:elaborate` / Install LiteX at the pinned revisions<br>`.github/workflows/rtl-fast.yml:firmware-boundary` / Install GoogleTest and GoogleMock and print the versions |
| litex-boards | `9ac53c7a11f2571ba2c9f165f468ae021a4f9bda` / `9ac53c7a11f2571ba2c9f165f468ae021a4f9bda` | `.github/workflows/elaborate.yml:elaborate` / Install LiteX at the pinned revisions<br>`.github/workflows/rtl-fast.yml:firmware-boundary` / Install GoogleTest and GoogleMock and print the versions |
| litex | `a1e1c3652ec2f1346ebaea7663d2867f393ae2c4` / `a1e1c3652ec2f1346ebaea7663d2867f393ae2c4` | `.github/workflows/elaborate.yml:elaborate` / Install LiteX at the pinned revisions<br>`.github/workflows/rtl-fast.yml:firmware-boundary` / Install GoogleTest and GoogleMock and print the versions |
| tsn-gen | `deca300c9eb4863fa13383b45ba6cb6fd0828671` / `deca300c9eb4863fa13383b45ba6cb6fd0828671` | `.github/workflows/rtl.yml:verilator-shards` / Build the pinned tsn-gen field oracle on its suite owner |
| litedram | `f9b75e0347fc43267d083f7ff5965170fe8f9a58` / `f9b75e0347fc43267d083f7ff5965170fe8f9a58` | `.github/workflows/elaborate.yml:elaborate` / Install LiteX at the pinned revisions<br>`.github/workflows/rtl-fast.yml:firmware-boundary` / Install GoogleTest and GoogleMock and print the versions |
| yosys | `v0.66` / `v0.66` | `.github/workflows/rtl-fast.yml:yosys-elaboration` / Build Yosys from source on cache miss<br>`.github/workflows/rtl-fast.yml:publication-census` / Build Yosys from source on cache miss<br>`.github/workflows/rtl.yml:verilator-shards` / Build Yosys from source on cache miss<br>`.github/workflows/rtl.yml:yosys-shards` / Build Yosys from source on cache miss |
| verilator | `v5.050` / `v5.050` | `.github/workflows/elaborate.yml:elaborate` / Build Verilator from source on cache miss<br>`.github/workflows/rtl-fast.yml:verilator-lint` / Build Verilator from source on cache miss<br>`.github/workflows/rtl-fast.yml:firmware-verilator` / Build Verilator from source on cache miss<br>`.github/workflows/rtl.yml:verilator-shards` / Build Verilator from source on cache miss<br>`.github/workflows/rtl.yml:physical-gptp` / Build Verilator from source on cache miss |
| rv32-sdk | `riscv32-ilp32d--glibc--stable-2025.08-1` / `riscv32-ilp32d--glibc--stable-2025.08-1` | `.github/workflows/docs.yml:docs-check` / Install and verify the pinned RV32 SDK<br>`.github/workflows/docs.yml:docs-check` / Install and verify the pinned RV32 SDK<br>`.github/workflows/docs.yml:docs-check` / Compiler-absent firmware controls<br>`.github/workflows/elaborate.yml:elaborate` / Install and verify the pinned RV32 SDK<br>`.github/workflows/rtl-fast.yml:firmware-unit` / Install and verify the pinned RV32 SDK<br>`.github/workflows/rtl-fast.yml:firmware-control-mutants` / Install and verify the pinned RV32 SDK<br>`.github/workflows/rtl-fast.yml:firmware-aecp-mutants` / Install and verify the pinned RV32 SDK<br>`.github/workflows/rtl-fast.yml:firmware-srp-mutants` / Install and verify the pinned RV32 SDK<br>`.github/workflows/rtl-fast.yml:firmware-boundary` / Install and verify the pinned RV32 SDK<br>`.github/workflows/rtl-fast.yml:firmware-verilator` / Install and verify the pinned RV32 SDK |
| webencodings | `0.6.1` / `0.6.1` | `.github/workflows/docs.yml:docs-check` / Install the pinned Markdown renderer |
| html5lib | `1.1` / `1.1` | `.github/workflows/docs.yml:docs-check` / Install the pinned Markdown renderer |
| six | `1.17.0` / `1.17.0` | `.github/workflows/docs.yml:docs-check` / Install the pinned Markdown renderer |
| pyslang | `11.0.0` / `11.0.0` | `.github/workflows/docs.yml:docs-check` / Build the validated HDL reference |
| wavedrom | `2.0.3.post3` / `2.0.3.post3` | `.github/workflows/docs.yml:docs-check` / Install diagram gate dependencies |
| cffi | `2.1.1` / `2.1.1` | `.github/workflows/docs.yml:docs-check` / Install the pinned Markdown renderer |
| cmarkgfm | `2025.10.22` / `2025.10.22` | `.github/workflows/docs.yml:docs-check` / Install the pinned Markdown renderer |
| pycparser | `3.0` / `3.0` | `.github/workflows/docs.yml:docs-check` / Install the pinned Markdown renderer |
| behave | `unversioned` / `1.3.3` | `.github/workflows/rtl-fast.yml:bdd-conformance` / Install behave |
| pyyaml | `unversioned` / `6.0.3` | `.github/workflows/docs.yml:docs-check` / Install the python gate dependencies<br>`.github/workflows/docs.yml:docs-check` / End-station builder gates<br>`.github/workflows/docs.yml:wire-accountability` / Advertised-vs-emitted gate (green since 2026-07-28, item 00)<br>`.github/workflows/elaborate.yml:elaborate` / Install LiteX at the pinned revisions<br>`.github/workflows/rtl-fast.yml:publication-census` / Run the publication census in every shape the builder builds<br>`.github/workflows/rtl-fast.yml:firmware-unit` / Install GoogleTest and GoogleMock and print the versions<br>`.github/workflows/rtl-fast.yml:firmware-control-mutants` / Install GoogleTest and GoogleMock and print the versions<br>`.github/workflows/rtl-fast.yml:firmware-aecp-mutants` / Install GoogleTest and GoogleMock and print the versions<br>`.github/workflows/rtl-fast.yml:firmware-srp-mutants` / Install GoogleTest and GoogleMock and print the versions<br>`.github/workflows/rtl-fast.yml:firmware-boundary` / Install GoogleTest and GoogleMock and print the versions<br>`.github/workflows/rtl-fast.yml:firmware-verilator` / Install GoogleTest and GoogleMock and print the versions<br>`.github/workflows/rtl.yml:full-ci-gate` / Hold every workflow file to its contract<br>`.github/workflows/rtl.yml:physical-gptp` / Fetch RTL dependencies |
| gh | `unversioned` / `2.102.0` | `.github/workflows/rtl.yml:full-ci-gate` / Assert the repository default branch is dev |
| node | `unversioned` / `22.23.3` | `.github/workflows/docs.yml:docs-check` / actions/checkout@v4<br>`.github/workflows/docs.yml:docs-check` / Upload the HDL reference HTML<br>`.github/workflows/docs.yml:docs-check` / Cache the pinned Markdown renderer downloads<br>`.github/workflows/docs.yml:docs-check` / Cache the pinned RV32 SDK<br>`.github/workflows/docs.yml:wire-accountability` / actions/checkout@v4<br>`.github/workflows/docs.yml:docs-check-no-git` / actions/checkout@v4<br>`.github/workflows/elaborate.yml:elaborate` / actions/checkout@v4<br>`.github/workflows/elaborate.yml:elaborate` / actions/setup-python@v5<br>`.github/workflows/elaborate.yml:elaborate` / Cache the pinned pip downloads<br>`.github/workflows/elaborate.yml:elaborate` / Cache the Scala toolchain<br>`.github/workflows/elaborate.yml:elaborate` / Cache the generated CPU metadata<br>`.github/workflows/elaborate.yml:elaborate` / Cache the pinned RV32 SDK<br>`.github/workflows/elaborate.yml:elaborate` / Cache the pinned Verilator build<br>`.github/workflows/rtl-fast.yml:changes` / actions/checkout@v4<br>`.github/workflows/rtl-fast.yml:verilator-lint` / actions/checkout@v4<br>`.github/workflows/rtl-fast.yml:verilator-lint` / Cache the pinned Verilator build<br>`.github/workflows/rtl-fast.yml:bdd-conformance` / actions/checkout@v4<br>`.github/workflows/rtl-fast.yml:yosys-elaboration` / actions/checkout@v4<br>`.github/workflows/rtl-fast.yml:yosys-elaboration` / Cache the pinned Yosys build<br>`.github/workflows/rtl-fast.yml:publication-census` / actions/checkout@v4<br>`.github/workflows/rtl-fast.yml:publication-census` / Cache the pinned Yosys build<br>`.github/workflows/rtl-fast.yml:firmware-unit` / actions/checkout@v4<br>`.github/workflows/rtl-fast.yml:firmware-unit` / Cache the pinned RV32 SDK<br>`.github/workflows/rtl-fast.yml:firmware-control-mutants` / actions/checkout@v4<br>`.github/workflows/rtl-fast.yml:firmware-control-mutants` / Cache the pinned RV32 SDK<br>`.github/workflows/rtl-fast.yml:firmware-aecp-mutants` / actions/checkout@v4<br>`.github/workflows/rtl-fast.yml:firmware-aecp-mutants` / Cache the pinned RV32 SDK<br>`.github/workflows/rtl-fast.yml:firmware-srp-mutants` / actions/checkout@v4<br>`.github/workflows/rtl-fast.yml:firmware-srp-mutants` / Cache the pinned RV32 SDK<br>`.github/workflows/rtl-fast.yml:firmware-boundary` / actions/checkout@v4<br>`.github/workflows/rtl-fast.yml:firmware-boundary` / Cache the pinned RV32 SDK<br>`.github/workflows/rtl-fast.yml:firmware-verilator` / actions/checkout@v4<br>`.github/workflows/rtl-fast.yml:firmware-verilator` / Cache the pinned Verilator build<br>`.github/workflows/rtl-fast.yml:firmware-verilator` / Cache the pinned RV32 SDK<br>`.github/workflows/rtl.yml:full-ci-gate` / actions/checkout@v4<br>`.github/workflows/rtl.yml:verilator-shards` / actions/checkout@v4<br>`.github/workflows/rtl.yml:verilator-shards` / Cache the pinned Verilator build<br>`.github/workflows/rtl.yml:verilator-shards` / Cache the pinned Yosys build for the netlist-level suite owner<br>`.github/workflows/rtl.yml:verilator-shards` / Upload this shard's suite logs<br>`.github/workflows/rtl.yml:physical-gptp` / actions/checkout@v4<br>`.github/workflows/rtl.yml:physical-gptp` / Cache the pinned Verilator build<br>`.github/workflows/rtl.yml:physical-gptp` / Upload the physical suite evidence<br>`.github/workflows/rtl.yml:verilator-suites` / actions/checkout@v4<br>`.github/workflows/rtl.yml:verilator-suites` / Download every shard's logs<br>`.github/workflows/rtl.yml:yosys-shards` / actions/checkout@v4<br>`.github/workflows/rtl.yml:yosys-shards` / Cache the pinned Yosys build<br>`.github/workflows/rtl.yml:yosys-shards` / Restore the portability result cache seeded from dev<br>`.github/workflows/rtl.yml:yosys-shards` / Upload per-top and structural evidence<br>`.github/workflows/rtl.yml:yosys-portability` / actions/checkout@v4<br>`.github/workflows/rtl.yml:yosys-portability` / Download every shard's evidence |

## Dockerfile layers and lock

Manifest: `sha256:86d7aa16e7d2464baf8e0d246434982838c8174de8c8fa610608cce5b23b5e6c`.
Configuration: `sha256:62b56e1ab52dce1a1914e8469429c014e69a465e74e0bdb9a7d8bf4a626b2776`.
Recipe: `214fefe3bd807c3403558de25d553d5a5a10f682a6bb5a824257f2a27ef192be`.
Image size: 3,931,071,698 bytes. Round-five cold Docker builds: 442,460 ms and 452,858 ms.
Both final-source builds used `--no-cache`. The times measure buildx, excluding preparation, separate archive saving and authentication.
The two exports have identical manifest, configuration and all 14 compressed/uncompressed layer identities.

The generated schema-2 lock is `ci/image/image.lock.json`. `build.py --record-lock` authenticated the first export;
`build.py --check-lock --verify-archive` independently authenticated the second. No digest was hand-edited.

| Layer | Dockerfile line / stage | Compressed OCI digest | Uncompressed diff-id |
|---|---|---|---|
| base | `ci/image/Dockerfile:1` / pinned base | `sha256:edd1ed89f0d443580bd42e5a10cd8736aba5a3438b2a0645c2ebb50119bb0eba` | `sha256:65e5d715ea720349e6475f91651a0956279fc295a45fd73aa04f1cec046281a1` |
| system | `ci/image/Dockerfile:4` / `system-tools` | `sha256:d0069157b863d07eea5fcbfc9ee66b570e10d1aa60777775c3563783966b9737` | `sha256:1f3ed2fa656eba3b57e4326d3d546bf5ec223754f765cdd17434e2d25ffa01ff` |
| gtest | `ci/image/Dockerfile:13` / `gtest-tools` | `sha256:24553cea3585e22b395adf775b099eb7aaa2d9454c7781aa55a4b3b1e139fb6a` | `sha256:4c5431ca66b2edc72aeab1af553521b6da88fb31b1f64869824b2a2d40ef6dd0` |
| python | `ci/image/Dockerfile:96` / `python-tools` | `sha256:ccf8dd6ad48dc2ccc0aed6480859bd2ecb65398fcb5176854aa543f4c2665a41` | `sha256:26dd9d83ef709bc7a351bbf5deef319d88040284498e8b052a92df036300cdcb` |
| litex | `ci/image/Dockerfile:97` / `litex-tools` | `sha256:72443935f2aac03c176be8c487114571e1c8451482d08014f4c2a94af8ec1768` | `sha256:f63a28dee6d731e88cc82c6cb2661c07b36db4aee3ed017f30a3d32f125212d2` |
| verilator | `ci/image/Dockerfile:98` / `verilator-tools` | `sha256:221d9dbcae4a620737a7865b08d0225f19123404e1dc6f3f6fad718fa6bf54e3` | `sha256:2f955a59302fb1961b1cf975b400bea2cd03c335cc2bd0b0f2bbdba1b55dd961` |
| yosys | `ci/image/Dockerfile:99` / `yosys-tools` | `sha256:abf98b1fd75417049213b62d411bed952b862cebf602f150974c40f3235f5157` | `sha256:f37082af1c0d3d4ca529308f98f67e1e874b43993dd043559cca4934506fb4a0` |
| rv32 | `ci/image/Dockerfile:100` / `rv32-tools` | `sha256:5f5a5c47cb0db16a41ad0cc057d2383ef989a28172da4e8c7a8a502ea3ab5d3c` | `sha256:e1535d1989a3dfc47d920c3889004c0f9757c0482224760d43aa7179597259c0` |
| sv2v | `ci/image/Dockerfile:101` / `sv2v-tools` | `sha256:dca2e7a4352a8f069098b0e72ba771f4f6f19124795f8c9cbfd2d1c989513536` | `sha256:1e9c8c4ea9ea72952f2a6fe272fea169e4910d39c06e3bbaaee6710c29ce5c47` |
| sbt | `ci/image/Dockerfile:102` / `sbt-tools` | `sha256:2ea388efe8d5ebebc23b60672941b852b518d7e6622e087bbcb3d73b9000fea1` | `sha256:7a095a6f67e8f0f9a2573dc45238d875b5454154a7b81428fe2211d2382e45e4` |
| oracle | `ci/image/Dockerfile:103` / `oracle-tools` | `sha256:4f577b318f2252bfd426276bca8e1ab971fb03b925b67f032e11e7029bff511d` | `sha256:ac18c822de4ce34ebe834b7d25a9ea2ab254eb0054ef87931ac91b4a9b1bba95` |
| node | `ci/image/Dockerfile:104` / `node-tools` | `sha256:a1272fb2b0690eaa802dc72c4a6961f166289812dac259f681b77a39db20b28c` | `sha256:e875b7c24ebc3671a16300aca725b18c55f6dd925af85d047d653fd3e70f309c` |
| gh | `ci/image/Dockerfile:105` / `gh-tools` | `sha256:083772e48637c9b6c20d769084fd37b53775ad80a051c6963fc6ce61ef60c24e` | `sha256:3dd5809f87ff44492ef13b581221dc9336e21d24bbf0860b95bd265b5f6979fc` |
| validation | `ci/image/Dockerfile:111` / `validation-tools` | `sha256:568426dc1e395127c4b39bba0e3f0bde36a2d0fedf8c773e2d3eb430eadc1503` | `sha256:ae526b7cb409825b8c8aede5ea22f1ecb23571f1d8475ad024b8fd904d1734a7` |

| Locked file | Bytes | SHA-256 |
|---|---|---|
| `ci/image/image.lock.json` | 164289 | `779400636ab2322c0426f8ed98f59984b1185fa2b70485af22d4c088517885bd` |
| `ci/image/sources.lock.json` | 419596 | `08bc8bde35b8adbbd882a2e7ede392ae56ef7b3c085e03fa2b26e82fd2ef800b` |
| `ci/image/tool-inventory.json` | 107663 | `d11d3dc98e93b8f808368d976eaa9c60b0be8b5e7ddd253951d4e83d3b6c0825` |
| `ci/image/command-table.json` | 404891 | `c428e6fe9106b4d154ce18cc6d7b7e962f270266717d5cae5bde6ecf71841c67` |
| `ci/image/syntax-census.json` | 16603 | `65b66b6d74e7664a70f3e67626b3614a76b22588de0768e5fd7c98935dab26aa` |

## Versions and smoke checks inside the final image

`round5-image-smoke.log` records the unchanged smoke program on the current manifest, networking disabled. Result: rc 0; all 131 version and smoke records passed. Every command in the following tables returned zero; all version and functional assertions passed.

| Version query | Reported version |
|---|---|
| CPython | 3.12.3 (main, Aug 31 2026, 10:18:26) [GCC 13.3.0] |
| PyYAML | 6.0.3 |
| behave | 1.3.3 |
| certifi | 2026.7.22 |
| cffi | 2.1.1 |
| charset-normalizer | 3.5.2 |
| cmarkgfm | 2025.10.22 |
| colorama | 0.4.6 |
| cucumber-expressions | 20.1.0 |
| cucumber-tag-expressions | 11.0.1 |
| html5lib | 1.1 |
| idna | 3.20 |
| liteiclink | 2025.4 |
| packaging | 26.3 |
| parse | 1.22.3 |
| parse_type | 0.6.6 |
| pycparser | 3.0 |
| pyserial | 3.5 |
| pyslang | 11.0.0 |
| requests | 2.34.2 |
| setuptools | 84.0.0 |
| setuptools_scm | 10.3.4 |
| six | 1.17.0 |
| svgwrite | 1.4.3 |
| urllib3 | 2.8.0 |
| vcs_versioning | 2.6.0 |
| wavedrom | 2.0.3.post3 |
| webencodings | 0.6.1 |
| wheel | 0.48.0 |
| migen | 0.9.2 |
| litex | 2026.4 |
| liteeth | 2026.4 |
| litedram | 2026.4 |
| litespi | 2026.4 |
| litex-boards | 2026.4 |
| pythondata-cpu-vexiiriscv | 1.0.1.post325 |
| `verilator --version` | Verilator 5.050 2026-07-01 rev v5.050 |
| `yosys -V` | Yosys 0.66 (git sha1 86f2ddebce7e98ce7cacc27e8a5c14cb53b51b51, g++ 13.3.0-6ubuntu2~24.04.1 -fPIC -O3) |
| `sv2v --version` | sv2v v0.0.12 |
| `riscv32-linux-gcc -dumpfullversion` | 14.3.0 |
| `sbt --script-version` | 1.10.7 |
| `node --version` | v22.23.3 |
| `gh --version` | gh version 2.102.0 (2026-09-30) |
| `git --version` | git version 2.43.0 |
| `cmake --version` | cmake version 3.28.3 |
| `ninja --version` | 1.11.1 |
| `gcc --version` | gcc (Ubuntu 13.3.0-6ubuntu2~24.04.1) 13.3.0 |
| `g++ --version` | g++ (Ubuntu 13.3.0-6ubuntu2~24.04.1) 13.3.0 |
| `clang --version` | Ubuntu clang version 18.1.3 (1ubuntu1) |
| `gcov --version` | gcov (Ubuntu 13.3.0-6ubuntu2~24.04.1) 13.3.0 |
| `make --version` | GNU Make 4.3 |
| `autoconf --version` | autoconf (GNU Autoconf) 2.71 |
| `flex --version` | flex 2.6.4 |
| `bison --version` | bison (GNU Bison) 3.8.2 |
| `automake --version` | automake (GNU automake) 1.16.5 |
| `help2man --version` | GNU help2man 1.49.3 |
| `curl --version` | curl 8.5.0 (x86_64-pc-linux-gnu) libcurl/8.5.0 OpenSSL/3.0.13 zlib/1.3 brotli/1.1.0 zstd/1.5.5 libidn2/2.3.7 libpsl/0.21.2 (+libidn2/2.3.7) libssh/0.10.6/openssl/zlib nghttp2/1.59.0 librtmp/2.3 OpenLDAP/2.6.10 |
| `pkg-config --version` | 1.8.1 |
| `rsvg-convert --version` | rsvg-convert version 2.58.0 |
| `java -version` | openjdk version "17.0.20.1" 2026-08-18 |
| `xz --version` | xz (XZ Utils) 5.4.5 |
| `sudo --version` | Sudo version 1.9.15p5 |
| `docker --version` | Docker version 28.0.4, build b8034c0 |
| `python3 -m pip --version` | pip 24.0 from /opt/python/lib/python3.12/site-packages/pip (python 3.12) |
| `perl -v` | This is perl 5, version 38, subversion 2 (v5.38.2) built for x86_64-linux-gnu-thread-multi |
| `/opt/tsn-gen/build/traffic-gen/packet_gen --version` | packet_gen 0.1.0 |
| `pkg-config --modversion gtest` | 1.14.0 |

| Functional smoke command | Result |
|---|---|
| `gcc -std=c11 -Wall -Werror $SMOKE_WORK/smoke.c -o $SMOKE_WORK/gcc` | rc 0 |
| `$SMOKE_WORK/gcc` | rc 0 |
| `clang -std=c11 -Wall -Werror $SMOKE_WORK/smoke.c -o $SMOKE_WORK/clang` | rc 0 |
| `$SMOKE_WORK/clang` | rc 0 |
| `gcc --coverage -c smoke.c -o smoke.o` | rc 0 |
| `gcc --coverage smoke.o -o covered` | rc 0 |
| `$SMOKE_WORK/covered` | rc 0 |
| `gcov -b smoke.c` | rc 0 |
| `g++ -std=c++20 gtest.cpp -lgmock -lgtest_main -lgtest -pthread -o gtest` | rc 0 |
| `$SMOKE_WORK/gtest` | rc 0 |
| `cmake -G Ninja -S $SMOKE_WORK -B $SMOKE_WORK/cmake` | rc 0 |
| `cmake --build $SMOKE_WORK/cmake --parallel 2` | rc 0 |
| `$SMOKE_WORK/cmake/smoke` | rc 0 |
| `autoconf` | rc 0 |
| `bash configure` | rc 0 |
| `git init --quiet $SMOKE_WORK/git` | rc 0 |
| `git -C $SMOKE_WORK/git rev-parse --is-inside-work-tree` | rc 0 |
| `perl -e 'print 6*7'` | rc 0 |
| `tclsh $SMOKE_WORK/smoke.tcl` | rc 0 |
| `flex scanner.l` | rc 0 |
| `gcc lex.yy.c -o scanner` | rc 0 |
| `bison parser.y` | rc 0 |
| `gcc parser.tab.c -o parser` | rc 0 |
| `$SMOKE_WORK/parser` | rc 0 |
| `help2man --no-info --output $SMOKE_WORK/gcc.1 gcc` | rc 0 |
| `curl --silent --fail file://$SMOKE_WORK/smoke.c` | rc 0 |
| `xz --keep $SMOKE_WORK/smoke.c` | rc 0 |
| `xz --decompress --stdout $SMOKE_WORK/smoke.c.xz` | rc 0 |
| `sudo --help` | rc 0 |
| `docker --help` | rc 0 |
| `node -e 'require('"'"'assert'"'"').strictEqual(6*7, 42); console.log('"'"'JS_OK'"'"')'` | rc 0 |
| `gh api --help` | rc 0 |
| `python3 -m pip check` | rc 0 |
| `verilator --binary --assert --top-module simulation -j 2 --Mdir $SMOKE_WORK/verilated $SMOKE_WORK/simulation.sv` | rc 0 |
| `$SMOKE_WORK/verilated/Vsimulation` | rc 0 |
| `sv2v $SMOKE_WORK/logic.sv` | rc 0 |
| `yosys -p 'read_verilog logic.v; synth -top smoke; abc -g AND; check -assert'` | rc 0 |
| `yosys-abc -c version` | rc 0 |
| `riscv32-linux-gcc -march=rv32i -mabi=ilp32 -ffreestanding -fno-stack-protector -nostdlib -nostartfiles -static -Wl,-e,_start $SMOKE_WORK/rv32.c -o $SMOKE_WORK/rv32.elf` | rc 0 |
| `riscv32-linux-readelf -h -A $SMOKE_WORK/rv32.elf` | rc 0 |
| `rsvg-convert -o $SMOKE_WORK/wave.png $SMOKE_WORK/wave.svg` | rc 0 |
| `behave $SMOKE_WORK/features --no-capture -f plain` | rc 0 |
| `javac $SMOKE_WORK/Smoke.java` | rc 0 |
| `java -cp $SMOKE_WORK Smoke` | rc 0 |
| `sbt --batch 'show sbtVersion' 'runMain Smoke'` | rc 0 |
| `/opt/tsn-gen/build/traffic-gen/packet_gen --yaml-dir /opt/tsn-gen/protocols/application/1722_1/aecp --interface atdecc_aecp_acquire_entity::AECP_ACQUIRE_ENTITY::AECP_ACQUIRE_ENTITY_IF --count 1 --seed 42 --output json` | rc 0 |

The scanner fixture additionally ran with `smoke.c` as standard input. Python assertions checked YAML, Markdown/HTML parsing, C FFI, C parsing, encodings, SystemVerilog syntax, SVG-to-PNG output, Migen/LiteX and ecosystem imports. All 186 distribution package versions were checked with `dpkg-query` against the lock; the raw smoke log contains the full mapping.

## Validation and limitations

- `round3-build-results.json`: cold builds, first export authentication/lock generation and second export verification. All four stages completed with rc 0; both privacy scans authenticated all 14 layers and 526 public-source allowances.
- `round3-image.json`: final-image inventory check/control, build/integrity/privacy/patch controls, package closure and Markdown gates all pass. Its initial smoke entry is a superseded invocation error: an arbitrary numeric user had no account entry and could not write the Scala cache. The documented default-user invocation is `round3-smoke.json`, rc 0. No assertion changed.
- `round3-source.json`: host bare-metal check and controls, Python idiom and controls, documentation consistency/style/path checks pass. Its stale inventory-hash failure is superseded by the final-image inventory check.
- `round3-final-source.json`: inventory check and controls pass; package closure on the host lacked `dpkg-deb`. `round3-image-7.receipt.json` supersedes that prerequisite failure and verifies all 186 packages from 30 roots.
- `round3-final-gates.json`: eight checks after lock generation, all rc 0: bare-metal scope and all 738 controls, Python idiom and controls, docs consistency/style/paths and whitespace.
- `round3-snapshots.json`: all 185 timestamped Ubuntu fallbacks match their existing pins.
- Earlier intermediate receipts remain for provenance. They are not represented as passing commands.

The round-two grouped builder evidence remains historical and was accepted by both round-two reviews: all 103 functions covered exactly once, including the compiler-backed campaign. The inert `MAKEFLAGS += -e` mutation and unavailable `mf48` physical-calibration arm remain explicitly NOT RUN. This round did not repeat that campaign or claim a monolithic builder run. Tool-layer byte equality is recorded separately; it does not constitute a new product regression verdict.

Runtime-built commands remain a manual residue checklist. Reproducibility is measured on this host, not across hosts. Registry publication/round-trip, workflow adoption, complete hosted/act acceptance, independent review and candidate-merge validation remain assigned follow-up work. No workflow, HDL, firmware, linked-image patch or product-test assertion changed; no hardware was used.

Large logs, exports, build contexts and caches remain in scratch. The evidence packet contains only text/JSON records at most 200 KB; large-file receipts record size and SHA-256. The round-three manifest identifies the historical packet; `round4-packet-manifest.json` identifies the current handoff. `round3-final-tree.json` records the clean checkout, unchanged protected paths, three one-line commits and 6,657,994,752-byte service memory peak.

## Round 4

Implemented under assignment 6170435035 and amendments 6170543242 and 6170640746.
Starting local and remote head: `e6b86814e6844ef61ba46a867a0fdbfbb925cceb`.
The construct census was committed first. The readers now require positive command forms,
resolve the censused shell/Make/Python subset, and refuse unsupported forms by name.
No workflow, existing test assertion, product source or gitlink changed.

| Change | Source |
|---|---|
| Positive executable and argument forms, exact inline text, reviewed script hashes | `ci/image/command-table.json:1` |
| Runtime expression provenance; literal dollar and marker text refused as runtime | `scripts/ci_command_table.py:27` |
| Function local/global state and positional restoration | `scripts/ci_shell_walk.py:277` |
| Make invocation directory and order-only automatic-variable separation | `scripts/ci_make_walk.py:80`, `scripts/ci_make_walk.py:366` |
| Generated current recipe and authenticated image/layer lock | `ci/image/image.lock.json:1` |
| Capability detection before argument decoding; literal keyword dictionaries and aliases | `scripts/ci_command_table.py:142` |
| Full command forms and explicit pin readers | `scripts/ci_command_table.py:275` |
| Scoped shell traversal, literal function calls and pinned source definitions | `scripts/ci_shell_walk.py:93` |
| Make option, default-goal, pattern, variable and prerequisite semantics | `scripts/ci_make_walk.py:17` |
| Workflow working-directory selection and reusable-job refusal | `scripts/ci_tool_inventory.py:181` |
| Generation/comparison controls for reported and supported forms | `scripts/ci_inventory_patterns_selftest.py:74` |
| Generated input hashes and located residue; unchanged tools | `ci/image/tool-inventory.json:1` |
| Reached syntax census and supported/refused boundaries | `docs/testing/CI_IMAGE.md:60` |
| New implementation modules enter the recipe digest | `ci/image/build.py:150` |

The final scope corrections preserve the common directory of conditional branches,
separate Makefile selection from the recipe directory, preserve function locals/globals
and subshell/pipeline definitions, and exclude order-only prerequisites from automatic variables.
Runtime argument slots require expression provenance; literal dollar and marker text cannot qualify.
Exact `awk`, `sort`, `tr` and no-op forms come from newly resolved existing scripts.

Intermediate failures are retained as provenance, not passing evidence. Initial source probes
found stale generated hashes, an overlong function and missing exact forms; these were fixed.
The reference environment initially lacked the hash-pinned Markdown packages; they were installed
only in scratch. An initial container invocation used a host interpreter path and exited 127;
the final invocations use container Python. The `cold-a` and `cold-final-a` preliminary builds
predate the final scope corrections and do not support the final lock. No assertion was weakened.

### Round 4 final result

Review-ready head: `e355f789b4f59b86083809299134557ca47bbcfb`. Source implementation: `e32352833`.
The generated lock is the only following repository change.
All 45 tool/pin/provenance records equal the starting head; 328 inputs and 269 located residue entries are recorded.
The round-four image identity is unchanged; the tables above now include round-five smoke evidence.

- `round4-source-candidate.json`: 13 source gates pass after the final semantic fixes.
- `round4-markdown-final.json`: three Markdown checks pass.
- `round4-final-gates.json`: source checks pass again after lock generation.
- `round4-lock.json` and `round4-second-archive.json`: both exported images authenticate against the generated lock, including privacy provenance.
- `round4-rebuilt-image.json`: all ten image checks pass, including default temporary-directory controls, a checkout below `/tmp`, package closure and the complete smoke program.
- `round4-cold-comparison.json`: two cold builds match in recipe, manifest, configuration, size and all layers.
- `round4-build-results.json`: both cold commands returned zero; only the pinned base was cached.
- `round4-build-artifacts.json`: large exports and build logs are recorded by size and SHA-256 and remain outside this packet.

Earlier round-four source failures and preliminary builds are superseded by these final receipts. No product test assertion, firmware behavior, linked image, workflow or gitlink changed. The previously accepted grouped campaign is historical evidence, not a newly executed campaign. Registry publication, hosted/act adoption, independent reviews and merge remain outstanding. No push occurred.

`round4-final-tree.json` confirms the clean final branch, unchanged protected paths, five one-line commits with empty bodies, unchanged remote head and a service memory peak of 10930085888 bytes.

## Round 5

Starting head: `e355f789b4f59b86083809299134557ca47bbcfb`, confirmed against origin.
Assignment: newest round-five direction on PR #738; findings R638-4 and R639-4.
Status: author implementation and local validation complete; independent re-review required. No push authorized.

1. Repair command-table compatibility with the unchanged Entity shape and derived-source gates.
2. Enforce the syntax census structurally and correct supported semantics.
3. Run every reported probe and the complete docs-check and rtl-fast step sets.
4. Regenerate inventory and lock through their generators; cold rebuild only if recipe changes.
5. Record file/line changes, evidence, image provenance and final head here.

Round-five evidence and final disposition are recorded below.

### Round 5 step 1

The copied HDL/header operands became typed data slots in `ci/image/command-table.json:5242`.
`scripts/ci_command_table.py:339` accepts non-option data paths and source sequences;
the recipe remains the source-list owner. `scripts/ci_inventory_nodes_selftest.py:9`
checks changed source populations, forbidden options, wrong suffixes and runtime values.
The inventory was regenerated with `scripts/ci_tool_inventory.py --write`.
All 45 tool/pin/provenance records equal `e6b86814`.

`round5-blocker-entity-shape.log`: 228 checks, zero failures.
`round5-blocker-final.json`: source-list, inventory, both existing inventory controls,
new data controls, Python idiom and whitespace checks all return zero.
An initial overlapping inventory check observed the shape self-test's temporary
Makefile mutation; its sequential rerun passed after automatic fixture cleanup.
Full workflow results are recorded below.

### Round 5 step 2

Implementation head: `8882ce17eb14cc6fa14d4d4c902a106204f1c958`.
The structural census is `ci/image/syntax-census.json:1`;
`scripts/ci_syntax.py:37` rejects uncensused nodes, fields and operators.
The shell walker preserves sourced caller state and both censused cleanup alternatives.
The Make walker carries exported values and recursive command-line overrides.
Directory/file automatic modifiers and interpreter-changing variables refuse.
Python follows local package initializers and members, checks foreign-function capabilities,
and rejects uncensused builtins/nodes. Checkout normalization preserves later path components.
The reviewed render `xargs` program now binds exact text, not a runtime marker.
`docs/testing/CI_IMAGE.md:60` describes the narrowed boundary.
Both fixture harnesses only gained the required census-file dependency; assertions are unchanged.
`round5-final-controls.json`: all seven checks return zero, including new reviewer probes.
The source/documentation checks in `round5-precommit.json` passed except a line-length
violation subsequently corrected and passed in the final-controls run.
Complete workflow results and updated cold-image proof are recorded below.

### Round 5 literal-path follow-up

Commit `5ed43fd83` preserves runtime provenance while following literal-dollar loop paths.
`scripts/ci_shell_walk.py:178` distinguishes typed runtime values from literal text.
`scripts/ci_command_table.py:537` and `scripts/ci_command_table.py:549` make the same
distinction for Git and Make classification.
`scripts/ci_inventory_nodes_selftest.py:36` checks the loop-path regression.
`round5-provenance-final.json`: all seven gates return zero; generated inventory unchanged.
Full workflow checks run in two isolated copies at `8882ce17e`; the follow-up only
changes inventory interpretation and its new controls, which passed separately.
Cold rebuilds bind the final validator sources.

### Round 5 nested syntax and source calls

Commit `4e8984373` checks censused boolean flags and applies structural validation
to nested trap programs. All seven controls pass (`round5-nested-final.json`).
The final source-call restriction binds the current call in `syn/yosys/run.sh:145`
to its exact semantic node. Existing source-scope fixture assertions are unchanged;
the fixture now declares its exact source call. The added uncensused-source probe
refuses. All seven controls pass (`round5-source-census-final.json`).
The preliminary cold build predates these final validator changes and will be
superseded by two cold builds of the final recipe.

Final implementation head before image-lock regeneration: `605e312dd26ca3a0c565d942dc23bf73c6cc6f9f`.
`round5-source-census-docs.json` records all 13 source/documentation checks at rc 0.
`round5-inventory-comparison.json` records 45 unchanged tool records, 329 input digests
and 264 located runtime residue entries. The syntax-census, documentation and fixture
changes are committed in `605e312dd`.

### Round 5 image execution and workflow setup

`round5-image-smoke.json` and `round5-image-smoke.log` record 131 successful version
and smoke records on manifest `86d7aa16e7d2464baf8e0d246434982838c8174de8c8fa610608cce5b23b5e6c`,
with networking disabled and the image default user. The tool versions and functional
checks in the tables above are unchanged. `round5-mount-final.json` records successful
inventory derivation at both `/src` and `/include`, plus the structural controls.

The initial full docs run used a non-default UID. Its builder gate refused writes
to the image's SBT cache. A default-user attempt then exposed mismatched ownership
of the disposable checkout. The final run uses the image default user and a checkout
owned by that user, without changing Git configuration, product code or assertions.
It restarts the entire docs-check set at `605e312dd`. Earlier setup attempts remain
in scratch evidence and are excluded from the final pass tally.

### Round 5 cold builds and lock

The final recipe digest is `214fefe3bd807c3403558de25d553d5a5a10f682a6bb5a824257f2a27ef192be`.
Sequential cold builds took 442460 ms and 452858 ms and each produced 3931071698 bytes.
The manifest, configuration and image contents remain unchanged from round four.
`round5-cold-comparison.json` records both receipts and build-log hashes; only the
pinned base step was cached in each final build. `round5-image-exports.json` records
archive sizes and hashes without placing the archives in this packet.
The first export passed authentication and privacy checks before `build.py --record-lock`
generated the lock. The independent second-export verification passed (`round5-second-archive.json`).
`round5-final-source.json`: all 13 source/documentation checks return zero.

The two final exported archives also match byte-for-byte: 1135213568 bytes, SHA-256 `725ba52e874f840e66272eae9ba0cbbbee872d407d389b2b463dd6e76e734c47`.

### Round 5 lock commit and blocker closure

Intermediate lock commit: `4d192b5d0ef087c1ab400a70de46283650df5d7c`, superseded by the final lock binding below. `ci/image/image.lock.json:3455`
binds the final validator recipe; the image content and all layer records are unchanged.
`round5-blockers-final.json` records the final Entity shape result (228 checks,
zero failures) and the derived protocol-processor source-list check/self-test, both rc 0.
Full documentation and RTL workflow results are recorded below. No push occurred.

### Round 5 final change map

| File:line | Change |
|---|---|
| `ci/image/build.py:144` | Bind the syntax census and its validator to the image recipe digest. |
| `ci/image/command-table.json:5243` | Typed HDL data operands replace copied paths; the derived source population uses `data_paths` at line 12459. The reviewed renderer has an explicit capability declaration. |
| `ci/image/image.lock.json:3455` | Generated final recipe binding; image and layer identities unchanged. |
| `ci/image/syntax-census.json:1` | Closed shell/Python syntax and Make construct census, including exact sensitive shell uses. |
| `ci/image/tool-inventory.json:16` | Regenerated input bindings and located residue; all 45 tool records unchanged. |
| `docs/testing/CI_IMAGE.md:60` | Document accepted constructs, exact source calls, refusal boundaries and runtime residue. |
| `scripts/ci_command_table.py:35` | Component-aware checkout normalization; local package traversal at line 253; typed operands at line 411; wrapper and capability checks. |
| `scripts/ci_inventory_nodes_selftest.py:17` | Data, syntax, shell state, Make environment/override, Python package and location controls for both CLI modes. |
| `scripts/ci_inventory_patterns_selftest.py:27` | Supply the census and exact source fixture call; existing assertions unchanged. |
| `scripts/ci_make_walk.py:18` | Carry exported environment and recursive overrides; reject uncensused interpreter variables and automatic-variable modifiers. |
| `scripts/ci_shell_walk.py:111` | Enforce syntax, preserve alternatives and caller scope; exact sourced calls at line 330, function alternatives at line 356, and loader residue at line 97. |
| `scripts/ci_syntax.py:14` | Refuse uncensused startup variables; shell fields, operators, flags and conditional functions at line 41; Python nodes, builtins and special names at line 73. |
| `scripts/ci_tool_inventory.py:173` | Refuse alternate workflow shells and sensitive environment overrides; preserve runtime provenance. |
| `scripts/ci_tool_inventory_selftest.py:148` | Supply the new census dependency; existing assertions unchanged. |

### Round 5 workflow scheduling

The full RTL command set is split after publication census: the first 19 commands
run in the original isolated checkout; the remaining 17 run independently at
`4d192b5d0`, with the image default user, split into nine initial firmware commands,
two AECP commands, two SRP commands and four boundary commands. All five required submodule roots and
origins were verified before that run. The first sequence stops after recording
the publication result; the second owns all remaining firmware commands.
Publication census uses `--jobs 1` to keep simultaneous source conversions within
the memory limit. Firmware campaign drivers use `--jobs 4`; assertions are unchanged.

### Round 5 full builder result

The unchanged full command `python3 sw/builder/test_builder.py --require-rv32`
returned zero in 1503.427 seconds. Its 102820-byte raw log has SHA-256
`8ff88e147d3e3758386641c1a7896ca7c0892a91c660c074d5a5f357054376c0`.
It reports `ALL GATES PASS EXCEPT 2 NOT RUN`: gate 1b's inert `MAKEFLAGS += -e`
mutation on this Make version, and gate 11's calibration against an unavailable
`mf48` utilization report. Neither arm is claimed as covered. This is the full
command, not the historical grouped replacement. No assertion was changed.

`round5-scope.json` records the actual branch-diff classification as RTL/tooling
relevant. `round5-sdk-verify.json` records the SDK installer's cached-tree
authentication inside the image at rc 0. Workflow dependency installation is
supplied by the authenticated prebuilt image; package versions, HDL parser,
Markdown renderer and SDK checks remain active in the unchanged gates.
All validation containers use the service's 16-CPU affinity. The observed service
memory peak is 6289797120 bytes, below the 13 GB limit.

### Round 5 completed documentation and publication gates

`round5-docs-results.json` records all 79 docs-check commands at rc 0, including
the full builder command and the final Entity shape gate. The builder's two
NOT RUN arms remain explicit above. The act runner's offline checks ran only
inside the disposable job, including its isolated-copy check.
`round5-publication.json` records the unchanged publication census at rc 0 in
2227.666 seconds with `--jobs 1`. The final rule-removal tally is zero of 31
rules without a proving arm. The original sequence then stopped as planned;
the independent firmware sequences own the remaining RTL commands.

The control mutation shard returned zero in 823.068 seconds. Its sequence
stopped at that job boundary. AECP, SRP and boundary jobs completed independently
in the recorded ancestor checkouts, with only the five submodules their workflow steps
require. Every submodule root and origin was verified. The native jobs have
four-CPU and 3 GiB caps; the boundary job has four CPUs and 5 GiB. All use
the service's 16-CPU affinity. No test command or assertion was removed.

### Round 5 startup variables

The closed environment boundary now also refuses uncensused directory-search,
interpreter-startup, loader and Make startup variables. The existing allocator
assignments/unsets are bound to exact syntax at `syn/yosys/malloc.sh`; their
loader choice remains explicitly recorded runtime residue. New controls cover
CDPATH, Python/shell startup, loader variables and implicit Make input files.
`round5-startup-closed.json` records all seven controls/checks at rc 0.
The previous successful cold pair is retained as `round5-before-startup-*`;
it covers the preceding recipe. The replacement sequential pair covers this change and its receipts are the current image evidence.

### Round 5 completed RTL workflow

`round5-rtl-results.json` records all 36 RTL workflow commands at rc 0.
AECP shard 2/4 passed in 269.301 seconds; SRP shard 3/4 passed in 676.314 seconds.
The native boundary gate passed in 786.731 seconds and its Verilator counterpart
passed in 581.037 seconds. The latter judged 836 compiled sources with zero
findings and all six boundary, 120 pin and four figure controls behaving correctly.
`round5-aggregate.json` records the unchanged workflow aggregate at rc 0, using
only statuses derived from those actual local results. This is not hosted evidence.
Each command receipt states the precise ancestor tested; firmware/RTL gate inputs,
workflow definitions and submodule pins are unchanged through the startup fix.
The affected inventory, source/documentation checks and ratchets were rerun at
`5e55cfc6c316b1fd9055c3a02c8b47a29bba4739`, all rc 0. Both alternate-root checks
also pass at that head. The inventory has 45 unchanged tools, 329 bound inputs
and 268 located residue entries, including four allocator-loader selections.

### Round 5 final disposition

Final head: `4391f353690972f4844cb641b1e77fa94f38cdf4`. The worktree is clean. Eight local round-five commits
remain unpushed. The final image recipe is `214fefe3bd807c3403558de25d553d5a5a10f682a6bb5a824257f2a27ef192be`.
Both cold exports authenticate and match the manifest, config, all 14 layers
and archive bytes. The same image passed all 131 version/smoke records.
The final Entity shape and pp source-list checks pass with unchanged assertions.
All 79 docs-check and 36 rtl-fast command receipts return zero; the aggregate
returns zero. Receipts identify the actual tested ancestors, and the final
source checks cover the subsequent validator and lock changes.
The full builder command has the two explicit NOT RUN arms described above.
`round5-final-state.json` records the clean tree, protected-path comparison,
commit subjects, unchanged remote head and exact final source identities.
`round5-final-source.json`, `round5-final-controls.json`,
`round5-startup-ratchets.json`, `round5-blockers-final.json` and
`round5-mount-final.json` provide the affected-check evidence.
Independent review, publication, adoption and merge remain outstanding.
No hosted result or review verdict is claimed by these local checks.

## Round 6

Assignment: PR #738 comment 6177332782 (class ruling and items 1-4).
Reviews: R638-5 (6177303373) and R639-5 (6176507644), both NEGATIVE at `4391f353`.
Starting head: `4391f353690972f4844cb641b1e77fa94f38cdf4`, equal to origin.

Plan, in assignment order (item 3 first):

1. Item 3 (R638-5-F1): in-tree imports never hidden by the external-import allowlist; literal `sys.path` insertions followed; `tb/verilator/nvm_capture_cpu/run.py` reached and declared; 45 tool records unchanged. (done: `bae4d9fa7`)
2. Item 1 (class ruling): Make canonical-form refusals, recipe-less targets, implicit-rule automatic variables, target-specific precedence, complete-state traversal keys; shell `$(cd <literal> && pwd)` only. Planted controls; current tree derives the same tools. (done: `85b045d3b`)
3. Item 2: ptrace execution audit of every inventory-reached docs-check and rtl-fast step inside the image with networking disabled; controls; committed current-tree receipt; follow-up interface. (done: `6bec5606a`, `9279316b3`)
4. Item 4 (R638-5-F4): verified RV32 adoption form with receipt. (done: `dc4a3f7d6`)
5. Full docs-check and rtl-fast step sets at the committed head. (see below)

Final head: `6918d4f9b`. Image recipe `54cd38dea89d143d3c4ba40e72971be5de3b16592652658659e670f230ad7a29` (unchanged by the audit tool and the gate mask, which are not recipe inputs).

Commits (atop round-five `4391f3536`): `bae4d9fa7` item 3; `85b045d3b` item 1; `dc4a3f7d6` item 4; `1af6c72c4` lock; `6bec5606a` + `9279316b3` item 2; `6918d4f9b` audit toolchain-prefix normalization and the bare-metal host-inventory mask.

### Round 6 change map

| File:line | Change |
|---|---|
| `scripts/ci_command_table.py:155` | Per-process Python module search path: literal `sys.path` insertions, imported path constants and call-argument parameters resolved; an unresolved entry opens the path to every in-tree portion; `runpy`/`spec_from_file_location` loaders followed; compiled in-tree modules refused; a child under a changed `PYTHONPATH` refused; `check_import_allowances` forbids an allowance naming an in-tree module. Path helpers `_join`/`_dirname`/`_normpath` reproduce the analysed program's `os.path`. `Scope` dataclass carries the evaluation context. `incoming_state` keys traversal caches. |
| `ci/image/command-table.json` | 133 in-tree names removed from `python_imports` (77 external remain); five newly reached modules declared; exact Verilator capture form; whitespace-exact Make recipe forms; three stale `dirname` forms removed. |
| `scripts/ci_make_walk.py:1` | Rewritten around a canonical line classifier: assignments only in column zero with a censused operator; `!=`, double-colon, indented and escaped-end lines refuse; built-in implicit rules (from the recorded database) that could apply refuse; `MAKEFLAGS += -r` honoured; implicit-rule prerequisites bound as make binds them with directory-keeping stems; target-specific `=`/`:=` for exact targets, refusing a command-line collision; recipes split per expanded line and run in make's exact child environment; `.SHELLSTATUS` modelled as runtime. |
| `scripts/ci_shell_walk.py:72` | `$(cd <literal> && pwd)` is the only directory-yielding substitution, unredirected and non-symlink; `$(dirname\|realpath <literal>)` exact; `$0` and `${BASH_SOURCE[0]}` are the exact invocation words; a new shell starts from its exported environment alone. |
| `ci/image/make_builtins.py:1`, `ci/image/make-builtins.json:1` | Generator (run inside the image) and recorded GNU Make 4.3 built-in rules and default variables. |
| `ci/image/exec_audit.py:1`, `ci/image/exec-audit.json:1` | ptrace execve audit, its allowlist and installer denylist. |
| `scripts/ci_inventory_nodes_selftest.py:149` | `import_controls` for search paths, loaders, namespace members, compiled modules, startup modules and the allowance invariant. |
| `scripts/ci_inventory_exact_selftest.py:1` | New: canonical-Make, rule, traversal and substitution controls, each resolved as the image tools resolve it or refused by name; the `dirname` model equals the image coreutils. |
| `ci/image/build.py:151` | `make-builtins.json` and `make_builtins.py` enter the recipe digest. |
| `ci/image/image.lock.json:3` | Regenerated recipe binding `54cd38de`; image bytes unchanged. |
| `docs/testing/CI_IMAGE.md` | Python search-path model, exact Make/shell boundary, the execution audit section and interface, and the verified RV32 adoption form with the switch lane's step and contract change. |

### Round 6 evidence

- Item 3: `tb/verilator/nvm_capture_cpu/run.py` and `soc.py`, `sw/litex/platforms/*`, and `protocol-processor/hdl/aecp/desc/gen_desc_image.py` are now reached and declared; 10 new followed inputs, 13 new located-residue entries; all 45 tool/pin/provenance records equal `e6b86814`. Reviewer probes P1 (installer appended to `run.py`) and P2 (installer appended to `flash_map.py`) refuse by name (`round6-item3-*`; scratch `probes/item3-results.json`).
- Item 1: cold GNU Make 4.3 probes in the image confirm the modelled semantics; `make-builtins.json` is `--check`-equal to the image's database. `ci_inventory_exact_selftest.py` holds 42 planted controls, each resolved as the real tool resolves it or refused by name.
- Item 2: `exec_audit.py --selftest` passes five controls (benign step; job-built artifact allowed; planted installer caught by name; planted system program caught by name; network-needing step caught). `round6-exec-audit-receipt.json`: nine inventory-reached offline steps at the committed tree, every executed program allowlisted, rc 0.
- Item 4: `round6-rv32-adoption-sequence.log` records the documented `--verify-only --destination /opt/rv32-sdk` sequence returning rc 0 in a fresh image home, with the compiler resolved through the link.
- Lock: two sequential `--no-cache` cold builds produced recipe `54cd38de`, identical image `sha256:86d7aa16…`, config `sha256:62b56e1a…`, all 14 layers and byte-identical 1,135,213,568-byte archives (sha256 `d82f97e8294c2a3e71db24eb8e513faffcf8bbe9e55b5864bb9b0d765e40f768`). `--record-lock` authenticated the first; `--check-lock --verify-archive` authenticated the second. Only `recipe_digest` changed in the lock. `round6-cold-comparison.json`.
- All source/documentation gates run at the committed head return rc 0 (`round6-item1-source.json`, `round6-item3-source.json`, `round6-item1-final.json`, `round6-item2-docs2.json`), including Entity shape (228 checks, 0 failures) and the derived protocol-processor source list.

### Round 6 full gate sets at the committed head

Both sets ran inside the authenticated image (`--network none`, 16-CPU set, 13 GB) against a clean clone of `6918d4f9b` with all five required submodules initialized and their roots and origins verified.

- **docs-check: all 79 commands rc 0** (`round6-docs-gate-results.json`, 2587 s). Includes the Entity shape gate (228 checks, 0 failures), the bare-metal scope gate with the new host-inventory mask, `test_builder.py --require-rv32` (the full builder bank, 1494 s), the compiler-absent controls, the act-runner contract self-tests, and all documentation and ratchet gates. Install-only steps are the image's own prebuilt tools. The RV32 census path `$HOME/br-milan-rv32/host` is the documented adoption link to `/opt/rv32-sdk`.
- **rtl-fast: all 36 commands rc 0** (`round6-rtl-gate-results.json`, 6633 s, run as uid 1000 so the custody-oracle self-tests that refuse under root — `syn/yosys/ooc_selftest.py` — run as intended). Includes the whole-tree Verilator lint ratchet, the derived protocol-processor source list, the three-top yosys elaboration with its OOC/guard/cache self-tests, the publication census (`--jobs 1`, 1712 s), the firmware unit suites and RV32 builds, the control/AECP/SRP mutation campaigns, the firmware coverage ratchet, and the TSN stack boundary over both the firmware and Verilator builders.

The two self-tests that refuse under root are the reason the docs set (which contains none) ran as the image default user while rtl-fast ran as uid 1000; each set is clean under the user its gates require. Receipts record each step's command, rc and wall time; large logs stay in scratch.

### Round 6 final disposition

Final head `6918d4f9b`, worktree clean, seven one-line round-six commits unpushed. The image recipe `54cd38de` is bound in the lock; both cold exports authenticate and the image bytes are unchanged from round five (`sha256:86d7aa16…`). Every assignment item is addressed, every planted control refuses by name, the current tree derives the same 45 tool records, and both full gate sets pass at the committed head. Independent re-review, the reviewer-owned coverage ledger, publication, adoption and merge remain outstanding. No push, registry login or push occurred.
