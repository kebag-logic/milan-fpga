[A615]

# Image lane handoff

Status: REVIEW READY; round-three validation completed. PR #738; relates to #737. No push or PR modification.
Head: `e6b86814e6844ef61ba46a867a0fdbfbb925cceb`. Branch: `737-ci-image`. Source base: `fa7347fc59173f90e4feec2df207692e6e6e72ec`.
Round-three starting head: `18f2df92b13cb3f4036b073ed76940187bf10487`.

## Authority

Issue #737 assignment 6160953880; PR #738 round-three assignment 6167899804; amendment 6167966247 resolving STOP 6167951082; reviews R638-2 (6167893456) and R639-2 (6166908258). The round-two literal-mask ruling 6162190578 authorizes exact public host-tool URL literals in the existing image metadata files. No product scan scope or product-test assertion was changed.

## Round 3

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
Recipe: `08fe0f5bdedde8382351617017df7af89055b106af11e3946966845dc0ca906e`.
Image size: 3,931,071,698 bytes. First cold Docker build: 434,933 ms. Second cold Docker build: 398,716 ms.
These measured Docker build times exclude preparation, export authentication and privacy scanning. `round3-build-results.json` records end-to-end stage wall times separately.

The generated schema-2 lock is `ci/image/image.lock.json`. It binds the manifest/config, base and every logical layer to compressed digest, uncompressed diff-id, source digest and recipe digest. It is generated by `build.py --record-lock`; no digest was hand-edited. `round3-first-identity.json` shows that the base and all twelve tool layers are byte-identical to round two; only the final source-declaration layer differs.

| Layer | Dockerfile line / stage | Compressed OCI digest | Uncompressed diff-id |
|---|---|---|---|
| base | `ci/image/Dockerfile:1` / `pinned base` | `sha256:edd1ed89f0d443580bd42e5a10cd8736aba5a3438b2a0645c2ebb50119bb0eba` | `sha256:65e5d715ea720349e6475f91651a0956279fc295a45fd73aa04f1cec046281a1` |
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
| `ci/image/image.lock.json` | 164289 | `1f2ccc8aa51bf9bd61d5157d478126283afe190b541ae74ca10f9bad76e4c551` |
| `ci/image/sources.lock.json` | 419596 | `08bc8bde35b8adbbd882a2e7ede392ae56ef7b3c085e03fa2b26e82fd2ef800b` |
| `ci/image/tool-inventory.json` | 131784 | `98e78e9a5d5b8d04df7b44c96805cb15cbee03fb7d41713e0012a17009ebfe30` |
| `ci/image/command-table.json` | 55676 | `44e85ee742eb62d1d0aae1b866a83da1d0c642396537402938d1da0d6c4ebb4f` |

## Versions and smoke checks inside the final image

`round3-smoke-0.log` and its receipt record the unchanged smoke program on the new manifest, networking disabled, using the image default user. Result: rc 0 in 30,028 ms. Every recorded command below returned 0; the program also checked its assertions and reported `PASS: all image tool families`.

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

Large logs, exports, build contexts and caches remain in scratch. The evidence packet contains only text/JSON records at most 200 KB; large-file receipts record size and SHA-256. The final round-three artifact manifest identifies the current packet. `round3-final-tree.json` records the clean checkout, unchanged protected paths, three one-line commits and 6,657,994,752-byte service memory peak.
