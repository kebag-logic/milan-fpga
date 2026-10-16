[A615]

# Image lane handoff

Status: Round 9 REVIEW READY for PR #738 at `6f86eee60` (issue #737 comment 6207079152); relates to #737. No push or PR modification.
Round-nine starting head: `1c4d722cb1d0279f0ec44b0fbe87c810adfb9267` (confirmed against origin).
Round-eight starting head: `feef7c9fd239ef62b7c6aad301e80a13275e47ef` (confirmed against origin).
Round-seven starting head: `6918d4f9bee7081a71f94d9090d01c557085658a` (confirmed against origin).
Round-six starting head: `4391f353690972f4844cb641b1e77fa94f38cdf4` (confirmed against origin).
Round-five starting head: `e355f789b4f59b86083809299134557ca47bbcfb`. Branch: `737-ci-image`. Source base: `fa7347fc59173f90e4feec2df207692e6e6e72ec`.
Round-three starting head: `18f2df92b13cb3f4036b073ed76940187bf10487`.

## Authority

Round nine: assignment 6204018211; reviews R638-8 (6204009418) and R639-8 (6203890877).

Round eight: assignment 6196923564; reviews R638-7 (6196727731) and R639-7 (6196901768).

Round seven: assignment 6183738772; reviews R638-6 (6183731799) and R639-6 (6183445346).

Round six: assignment 6177332782; reviews R638-5 (6177303373) and R639-5 (6176507644).

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

Round seven leaves all 45 records byte-identical. GNU time (`time 1.9-0.2build1`) enters as a declared runtime consumer, not a workflow installation request: `ci/image/package_roots.json:12` names `.github/workflows/rtl.yml` and its `/usr/bin/time -f` literal, and `ci/image/sources.lock.json:2419` pins the package.

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

Round-seven image (adds GNU time; the Dockerfile is unchanged):

Manifest: `sha256:98a316549753d63e8b4118dc0f85af3e3813d667485817ee96f6dd597ba1c059`.
Configuration: `sha256:a2c4d52af85bc218ddd2d3958a2283f64ab175ec4254960eba891ae2271df1fd`.
Recipe: `b3fdd9003ee3ba95176f83d4bfd390c6be94841a10e5dacca2863e6ac056ae68`.
Image size: 3,930,997,226 bytes. Final round-seven cold Docker builds: 473,918 ms and 424,315 ms (`round7-cold-build-a.receipt.json`, `round7-cold-build-b.receipt.json`, chain log `round7-cold-chain.log`). The first pair, for recipe `88d59f27…` (`73fde2bf5`), took 432,708 ms and 430,562 ms (`round7-cold-build-a.log`, `round7-cold-build-b.log`) and produced the same image.
Both builds used `--no-cache`. The times measure buildx, excluding preparation, separate archive saving and authentication.
The two exports have identical manifest, configuration and all 14 compressed/uncompressed layer identities, and the archives are byte-identical (1,135,069,184 bytes, sha256 `1b1e263fbe9803c67b68524bc7ae14558222237f3b87e322ec988b5e548c0928`; the first pair's archives were `29120350…`, differing only in the recipe-named tag the archive carries).
Against the round-six image only the system (GNU time files and dpkg status), gtest (dpkg status) and validation (smoke program and lock copy) layers changed.

The generated schema-2 lock is `ci/image/image.lock.json`. `build.py --record-lock` authenticated the first export;
`build.py --check-lock --verify-archive` independently authenticated the second (`round7-cold-chain.log`; the first pair: `round7-record-lock.log`, `round7-verify-second-export.log`). No digest was hand-edited; the final re-record (`afdf0ef0c`) changed only `recipe_digest`.

| Layer | Dockerfile line / stage | Compressed OCI digest | Uncompressed diff-id |
|---|---|---|---|
| base | `ci/image/Dockerfile:1` / pinned base | `sha256:edd1ed89f0d443580bd42e5a10cd8736aba5a3438b2a0645c2ebb50119bb0eba` | `sha256:65e5d715ea720349e6475f91651a0956279fc295a45fd73aa04f1cec046281a1` |
| system | `ci/image/Dockerfile:4` / `system-tools` | `sha256:e29a079230603f60b44e21a5cc2e970f44c61e7fd19968e249eb77ffeaf18469` | `sha256:8827fab566ba3075494515052c4b1386d9cdd8633d2e468c88017ecac06a07f6` |
| gtest | `ci/image/Dockerfile:13` / `gtest-tools` | `sha256:1cb1faf264975957d7cd1c2f385021a3c2d454544b4b41f7b0e4104ee87b3696` | `sha256:b68a2760717514699a57ab4b728984d0e3e995c149c85d93315c3210ec17773e` |
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
| validation | `ci/image/Dockerfile:111` / `validation-tools` | `sha256:f78384782c1c764d5bcfbea10209c25fd41aab74b7d6cd0620f7416f75d13d94` | `sha256:9fe809d0c1c9470f3838e8197b1556b45e5fe58dbaff53d725a84ec62d82a7d2` |

Generated and locked files at the final head `feef7c9fd`:

| Locked file | Bytes | SHA-256 |
|---|---|---|
| `ci/image/image.lock.json` | 164468 | `bb4f43b657a1ae117b197602ade5b1cbef0bf422af2dae17c2399b3bc38457c2` |
| `ci/image/sources.lock.json` | 420057 | `ef450d20026f4ea9d48b2b7b84a9c501dd66564e2995e893089311bbb6a1330b` |
| `ci/image/tool-inventory.json` | 111879 | `295727b39a3f3b4e875b4ee8d64980d446a0eb04fe75315c05f0c4f836ab4226` |
| `ci/image/command-table.json` | 406302 | `50a531d79f0323d3bb5323a64f97ec0ec6a5cb06d3ad09d79f525c3ed4553765` |
| `ci/image/syntax-census.json` | 24418 | `134c1e6be19ea5a2e7838baa23e08feea01cefa4dee5f82aad5f7a97e486af2f` |
| `ci/image/differential-receipt.json` | 147983 | `48423733e626b506c2b0150fcfe6a73c4c65f924f770aa77e24351feb4655d5a` |
| `ci/image/exec-audit.json` | 3117 | `c72a508fd2b146f63207c3cf1fa0174b9573f722a6795794a027a293188eeec6` |
| `ci/image/exec-audit-receipt.json` | 498278 | `a67553ae7187afcfc445801d49e977f0e8e7e9a0ef476592da4708817e47bba2` |
| `ci/image/make-builtins.json` | 20185 | `70d43efc879f93e97c2e59bcff3fa28a9be858877c2e7ffd3c4fa5d362aa74c4` |

The round-five/six image (`sha256:86d7aa16…`, 3,931,071,698 bytes, cold builds 442,460 ms and 452,858 ms) is superseded.

## Versions and smoke checks inside the final image

`round7-image-smoke.log` records the smoke program on the round-seven manifest `sha256:98a31654…`, networking disabled, as the image's default user. Result: rc 0, `PASS: all image tool families`; all 133 version and smoke records passed (the round-five 131 plus the two GNU time checks). Every command in the following tables returned zero; all version and functional assertions passed.

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
| `/usr/bin/time --version` | time (GNU Time) UNKNOWN (package `time` 1.9-0.2build1, checked by `dpkg-query`) |

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
| `/usr/bin/time -f status=%x true` | rc 0, `status=0` |
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

## Round 7

Assignment: PR #738 comment 6183738772 (accepted means differentially proven; ambiguous state never literal; audit judges full invocations with provenance; full 79 + 36 population receipt; F1 stale pin).
Reviews: R638-6 (6183731799) and R639-6 (6183445346), both NEGATIVE at `6918d4f9b`.
Starting head: `6918d4f9bee7081a71f94d9090d01c557085658a`, equal to origin.

Plan, in assignment order (item 5 first):

1. Item 5 (F1): re-pin the reviewed `scripts/check_baremetal_only.py`, refresh the inventory inputs, re-record the lock. (done: `e1c7551ef`; lock re-recorded `73fde2bf5` for GNU time and `afdf0ef0c` after the last recipe-input change)
2. Items 1-2: closed differential census; every accepted shape has a fixture run through the real tool in the image and through the walker; every R638-6/R639-6 probe a fixture; ambiguous state never literal; function names never builtins. (done: `ccaa37a60`, `f617e6052`, `863ac16a9`; 188/188 fixtures meet expectations; census 177 shapes)
   - The census needs GNU time in the image: `rtl.yml:375` and `tb/verilator/milan_dp/Makefile:539` run `/usr/bin/time`, which the image lacked. `time 1.9-0.2build1` added as a documented runtime consumer (`package_roots.json`), resolved through the candidate mechanism; one new lock row; smoke check added. The image digest therefore changes; two cold builds re-recorded the lock.
3. Item 3: audit judges complete invocations with provenance; installer subcommands refused by name; reviewer negatives as controls. (done: `f60f8d9d5` through `6ddf5725e`; 20/20 controls)
4. Item 4: every reached docs-check and rtl-fast step traced in the image, committed per-step receipt and reconciliation. (see below)
5. Final: full docs-check and rtl-fast step sets at the committed head, inventory `--check` and `--prepare-only` last. (see below)

### Round 7 item 5

- `ci/image/command-table.json:13060`: `scripts/check_baremetal_only.py` declaration re-pinned to `bc594d82…` after review of the `6918d4f9b` change (one file-pinned `HOST_RUNTIME_MASKS` entry for `ci/image/exec_audit.py`, data only, non-installing).
- `ci/image/tool-inventory.json:14,32`: regenerated by `--write`; only the two input digests change; all 45 tool records unchanged.
- `ci_tool_inventory.py --check` rc 0, `ci_tool_inventory_selftest.py` rc 0, `check_baremetal_only.py --check` rc 0 (0 findings, 1326 files), `--selftest` rc 0 (738 arms), `build.py --prepare-only` rc 0 with recipe `a0337622…` (the lock is re-recorded once, after the remaining recipe-input changes).

### Round 7 items 1-2: differential census (`ccaa37a60`, `f617e6052`, `863ac16a9`)

- Census = exactly the 177 shapes the current tree applies (`syntax-census.json` `shapes`, generated by `scripts/ci_differential.py --write-census`), each naming its focus fixture: 175 at `ccaa37a60`, plus `bash:set.errexit` and `sh:set.errexit` at `863ac16a9`.
- `scripts/ci_differential_fixtures.py`: 188 fixtures (173 at `ccaa37a60`, 15 added at `863ac16a9`): one focus fixture per shape group, and every R638-6 probe (M1-M21, S1-S10, Python PYW1-6 and the 15 refused forms) and R639-6 probe (make-explicit-stem, shell-short-circuit, make-unlisted, shell-unlisted, python-unlisted, python-network, shell-pwd-shadow), with a `zz_probe` sentinel in place of the reviewers' hidden command.
- `scripts/ci_differential.py --run` (inside the image, offline, as root for the `sudo` fixture): walker resolution with the gate off vs. real GNU Make 4.3 / bash 5.2.21 / dash / CPython 3.12.3, stubs recording each sentinel's directory and argv; outcomes `identical`, `residue` (declared-script residue covers what the walker left unresolved) or `refused` (by name; probes with a hidden command must show it executing).
- `ci/image/differential-receipt.json`: 188/188 met their expectation at image `sha256:98a31654…` (`round7-differential-harness.log`); bound to the walker sources, fixtures and census shapes (`ci_command_table.binding`). Generation refuses a stale receipt; a shape is accepted only via its focus fixture meeting its expectation (`ci_command_table.py` `accepted_shapes`, `shape`).
- Probe outcomes: refused M1, M2, M7, M11, M15, M17, M21, S1, S2, S3, S5, S6, S9, S10, all Python capability forms, all R639-6 forms; resolved identically M3, M3b, M4, M5, M6, M8, M9, M10, M12, M13, M14, M16, M18, M19, M20, S4, S7, S8.
- Item 2 semantics (shell): joined state at `&&`/`||`/if/case/loops (values differing between paths become runtime; differing directories refuse); `exit`/`return`/`break`/`continue` frames; loop fixed point; certain tests take one branch; function names anywhere in scope never builtin/external (partly-defined calls are declared residue); trap handlers with unknown variables and directory; exact field splitting, pathname expansion, tilde, `"$@"`; prefix assignments after word expansion; `source` needs a slash; POSIX `sh` dialect for recipes, `$(shell)`, `sh -c`, Python shell strings; shebang-selected dialect for direct execution.
- Make: exact conditional directive words; environment/command-line values recursive; `$(call)` binds `$(0)` and blanks outer arguments; simple macros not re-expanded; lazy `$(if)`/`$(and)`; lexical `$(abspath)`; `$*` refuses outside implicit rules; `$(shell)` sees the startup environment; `MAKEFLAGS`/`MAKELEVEL` computed for recipes and the only route for flags and command-line variables to a child make; `-n` dry-run lines inspected only; inline recipe after `;` keeps `#`.
- Python: namespace reflection (`sys.modules`, reflective dunders, `builtins` executors, `getattr`/`vars` on a module, `globals()[...]`) is execution capability; four existing test files that reflect for patching gained reviewed declarations; `python3 -I` drops the script directory; several in-tree portions are inspected alternatives; strings without `shell=True` name one program.
- GNU time: the census needs `/usr/bin/time` (rtl.yml:375, tb/verilator/milan_dp/Makefile:539), which the image lacked. `time 1.9-0.2build1` (45,246 bytes, sha256 `abe09ee9…`) added through `package_roots.json` and the candidate mechanism; `smoke.py` checks it. Only the system (+8 files, dpkg status), gtest (dpkg status) and validation (smoke, lock copies) layers change.
- Tool records: all 45 byte-identical; 22 new located residue entries, all in declared scripts.
- Self-tests: walker semantics tests run with the gate off; `scripts/ci_differential_selftest.py` proves the gate refuses an uncensused shape, a stale receipt and an unmet expectation by name.
- Failed `cd` (`863ac16a9`), found while proving the certain-test rule: a fixture showed that a test's own `cd` carried into the failure branch, so `if cd missing; then …; fi; zz_probe` recorded a directory bash never entered. The walker now models a failed `cd` as changing nothing. Under errexit it ends the shell; workflow steps start under errexit (`bash -e`), and `set -e`/`+e`/`-o errexit` change it (new census shapes `bash:set.errexit` and `sh:set.errexit`). Tests suspend errexit (`&&`/`||` left sides, `if`/`while` conditions, negation, and functions called from them). A test that is one `cd` fails where it started. A certain `cd` is a non-symlink directory inside the checkout (a path outside it depends on the runner's filesystem), with operand values literal after exact field expansion. Where paths continue in different directories, the directory is ambiguous and the next statement there refuses by name, so the tree's `cd obj_fw && $(CC) …` recipe lines, which end there, still resolve. After a certain test, the right side of `||` and a conditional's other branch are inspected only, and inspected paths leave no escape state.
  - 15 new fixtures, each run through the image's real bash or GNU Make and `sh`: certain `if cd`/`if true`; `cd` outside the checkout; a failing test `cd` that continues (refused); a test `cd` ending its shell (identical, two variants); `cd sub || …` inspected; negated `cd`; errexit-ended `cd` at step level and after `set -euo pipefail` (identical); a script without errexit, `set +e`, and a function called from a test (refused); the recipe forms (`sh-cd-test-last`, `sh-cd-test-fails`, `sh-plain-cd`, `sh-set-errexit`).
  - Measured on the tree before the change: 0 of 4,167 `if` and 0 of 10,617 `&&`/`||` evaluations took a certain branch, and every literal `cd` in a test ends its shell; the derived 45 tool records and all residue are byte-identical after it (`ci_tool_inventory.py --write` changed only the receipt and census input digests).
  - Harness: 188/188 fixtures meet their expectation; census 177 shapes.

### Round 7 item 3: audit judges complete invocations (`f60f8d9d5`, `c4aa92d34`, `9e6d8c552`, `47592e05a`, `87bfa4a64`, `4a63d2dad`, `57696d7ee`, `e3d1f981f`, `d39500955`, `fef1e6fda`, `e9e6c2069`, `6ddf5725e`)

- Tracer: a seccomp user-notification filter on `execve`/`execveat` (no ptrace). The first population discovery showed LeakSanitizer suites (`test_ctrl_nvm.py`, the coverage ratchet) failing under ptrace, because LSan traces its own threads; the seccomp tracer observes every exec (static binaries included), reads the file the call names and its argv from the caller's memory, resolves interpreter lines as exec does, and lets the call continue. The step never holds the listener descriptor. A LeakSanitizer control passes under the audit.
- Every exec instance is kept with full argv, directory and stream links (one JSON line each in the step log; the receipt carries the count and log digest).
- Interpreters are judged by script, `-m` module, inline or streamed program, reading combined shell/Python/Perl/Node options as the tools read them. Installers are refused by name as program, script or module; `gem|cargo install` and `go install|get` by subcommand; an interpreter fed from a fetcher's pipe is refused.
- Names: a program or script under the image's own directories must be named in `ci/image/exec-audit.json`; there is no path exemption for anything else.
- Provenance, judged at the exec and scoped to the traced job (shared across its steps):
  - program: the `-o` output of a build program in the job; or a byte copy of one; or a file written during the job that is not a byte copy of any executable the image or checkout held before the job; otherwise none;
  - script: in the checkout when the job started, or written during the job. A job-written script with the bytes of an executable the image held before the job runs that file's code, so it is judged as that file, by its name (`6ddf5725e`): a renamed `pip3` copy is caught as the installer `pip`. (`e9e6c2069` first refused such copies outright; the traced boundary step then showed the stand-in simulator's `#!/bin/sh\nexit 0` model stubs, `ctrl_pin.py:224`, match the base image's no-op `/usr/sbin/initctl`, so `initctl` is named.) A missing script operand runs nothing and is recorded `absent`; a linked script is judged as the file it names, and a link named as an installer is caught by that name.
  - Boundary: "written during the job" is established by creation time and byte comparison, not data-flow tracking; a transformed (not byte-identical) image file is not distinguished. The network is disabled, so every input is the checkout or the image.
- Allowlist additions found by the population, each an image tool the reached steps run: programs `ls`, `toolchain-wrapper`, `clang`, `jspawnhelper`, `stat`; scripts `behave`, `git-submodule`, `ldconfig`, `sbt`, `verilator`, `verilator_includer` (the pinned Verilator's own Python helper, run by its generated makefile; missed when reading discovery 2 and caught by the `d39500955` run) and `initctl` (see above).
- Controls (`exec_audit.py --selftest`, 20/20 in the image, offline, root; `round7-exec-audit-selftest.log`): step-built static binary observed and provenanced; static binary planted in a system directory; `pip3 --version`; `npm --version`; a real offline local-wheel `pip install` (caught as the `pip` module); unlisted shebang script in a system directory; shebang `apt-get` outside; copied unlisted ELF; renamed copy of the image's `pip3` script (caught as `pip`); a job-written stub with `initctl`'s bytes (judged as `initctl`, clean); `curl file://… | sh`; `gem install`; link to a checkout script judged as that script; link named `apt-get` caught; missing script operand; permitted interpreter call and checkout script clean; program built under a temporary name then renamed clean; built program and installed copy clean; LeakSanitizer leak check runs; failing step reported.

### Round 7 item 4: full population

- Reached set: every `run` step of docs.yml `docs-check` (46) and of every rtl-fast job (52) = 98 steps (`ci/image/audit_population.py`, `reached_steps`). The round-six "79 + 36" are the gate commands inside these steps; the merged receipt also finds each of those 115 commands among the exec instances of its traced step.
- Runner emulation: `bash -e` on the step text, step/job/workflow env with runner expressions resolved for a push of the head onto `fa7347fc`, `GITHUB_PATH`/`GITHUB_ENV`/`GITHUB_OUTPUT` carried within a job, a clean checkout, fresh home and temp per job, the image's own environment inherited (as a job container does). rtl-fast runs as uid 1000 (`ooc_selftest.py` refuses root), docs-check as root (the image default user); the merge refuses differing sources or images.
- Image forms (recorded per step with removed lines and text digest): fetch steps become `git submodule status <same paths>`; install steps the image replaces become version/import probes; the RV32 install becomes the documented adoption form; top-level `python3 -m pip install`, `sudo apt-get`, and `sudo ln -sf /opt/yosys/bin/...` lines are removed; fallbacks inside never-taken blocks stay verbatim; the four cache-miss build steps (Verilator in `verilator-lint` and `firmware-verilator`, Yosys in `yosys-elaboration` and `publication-census`) are not run and are named in the reconciliation with the layer that replaces them.
- Command reconciliation: an instance matches a listed command when it runs the listed script, module or program; arguments are compared with absolute paths as placeholders, and where none matches the listed arguments the observed ones are kept beside them.
- Runs, in order (all offline in image `sha256:98a31654…`, clean clones with the five submodules verified):
  - earlier discovery runs from `9e6d8c552` (ptrace tracer): two nonzero docs-check exits and findings from runner-emulation gaps (the job lacked the image's environment, combined interpreter options, cross-step provenance) and LeakSanitizer suites failing under ptrace; fixed in `c8e0cf778`, `47592e05a`, `87bfa4a64` and the seccomp tracer `4a63d2dad`;
  - discovery 2 at `57696d7ee` (seccomp): 94/94 exit 0; findings `jspawnhelper` and `stat` (docs-check builder bank), `pp_srcs.py.broken` (absent operand), `clang`, `.ctrl-recorder` (a renamed build output) and `verilator_includer`;
  - `d39500955`: 94/94 exit 0, docs-check clean, one rtl-fast step with 18 `verilator_includer` findings; its listed-command matching compared raw argv and missed 7 of 115 (shebang forms, `$(nproc)`, the runner's full base SHA, a suffixed round-six label), which led to matching by what runs (`fef1e6fda`);
  - `fef1e6fda`: stopped after a few steps when the script-copy gap was found (`e9e6c2069`);
  - `e9e6c2069`: docs-check 46/46 clean; rtl-fast 46 steps, all exit 0, one step with two findings (the `initctl`-identical model stubs), stopped before its last two steps once `6ddf5725e` and the failed-`cd` model (`863ac16a9`, lock `afdf0ef0c`) superseded it;
  - final at `afdf0ef0c` (committed as `ci/image/exec-audit-receipt.json` in `feef7c9fd`, 498,278 bytes, sha256 `a67553ae…`): **94 of 98 reached steps traced, every exit status 0, zero findings, 183,845 exec instances**; docs-check 46/46 as root, rtl-fast 48/48 as uid 1000. The 4 untraced steps are the cache-miss Verilator/Yosys builds the image's layers replace, each named in the reconciliation with its reason; there is no other omission. All 115 round-six listed gate commands are observed in their traced steps; 111 with the listed arguments, and 4 with the workflow's own values the listing had replaced by hand (`check_em_dash.py --base` with the full base SHA from the runner context; `--jobs 16` from `$(nproc)` for the publication census, `test_ctrl_nvm.py` and `fw_coverage.py`), kept beside the listed ones in the receipt. Provenance of the 1,969 population rows: named image tools 640, checkout 242, written during the job 989, built by the linker 94, copy of a program the job built 1, copy of `initctl` 2, absent 1. Evidence: `round7-population-receipt.json` (identities, reconciliation, argument differences, scratch log digests and sizes: 48 rtl-fast logs 186,705,311 bytes, 46 docs-check logs 24,395,515 bytes), `round7-population-docs-check.json`.


### Round 7 change map

Line numbers are at the final head `feef7c9fd`.

| File:line | Change |
|---|---|
| `scripts/ci_command_table.py:20` | `BOUND` walker files and `GATE`; `binding` (`:110`) digests them with the census shapes; `accepted_shapes` (`:165`) accepts a shape only through its focus fixture meeting its expectation in the receipt; `shape` (`:181`) refuses any other by name; `script` (`:187`) selects the dialect by shebang or invocation kind; `command` (`:263`), `python_command` (`:438`) and `shell_command` (`:479`) record shapes, read `python3 -I`, and treat `find {}` and `xargs -I` operands as runtime. |
| `scripts/ci_python_walk.py:24` | New module split from the command table: reflection capability (`sys.modules`, reflective dunders, `builtins` executors, `getattr`/`vars`/`setattr` on a module, `globals()[...]`); `PythonWalk` (`:51`) with isolation, several in-tree portions as inspected alternatives, and string commands naming one program. |
| `scripts/ci_shell_walk.py:36` | `AMBIGUOUS` directory; `errexit_option` (`:47`) reads `set`; `join` (`:128`) merges reachable states (differing values become runtime, differing directories ambiguous); `escape` (`:168`) frames `exit`/`return`/`break`/`continue` and records nothing from inspected paths; `fields` (`:273`) exact splitting, globbing and tilde; `enterable` (`:447`) and `certain` (`:455`); `test` (`:472`) suspends errexit and continues a failed test `cd` where it started; `inspect` (`:495`); `statement` (`:505`) refuses work in an ambiguous directory and suspends errexit for negation; `conditional` (`:608`), `loop` (`:631`, to a fixed point) and `binary` (`:702`) walk tests; `call` (`:729`) expands words before prefix assignments; `builtin` (`:768`) tracks errexit; `change_directory` (`:826`); `trap` (`:859`) handlers with unknown state; `function` (`:920`) names never builtin; `run` (`:968`) sweeps every function alternative. |
| `scripts/ci_syntax.py:89` | `function_names` and `assigned_names` (`:94`) moved here from the shell walker (module size). |
| `scripts/ci_tool_inventory.py:211` | Workflow steps are walked as the runner's `bash -e`. |
| `scripts/ci_make_walk.py:27` | `MakeFlags` propagation (`sBnrw` letters and command-line variables); `invocation` (`:159`); `variable` (`:289`) recursive environment and command-line values, `$*` only in implicit rules; `function` (`:395`) exact `$(call)`/`$(foreach)`; `lazy` (`:465`) `$(if)`/`$(and)`; `recipe_environment` (`:490`) adds `MAKEFLAGS`/`MAKELEVEL`; `parse` (`:610`) keeps `#` in an inline recipe; `target` (`:723`) inspects `-n` dry-run lines. |
| `scripts/ci_differential.py:146` | Harness: `walk` with the gate off, `run` (`:185`) through the real tool with recording stubs, `outcome` (`:220`), `check` (`:323`) binding the committed receipt. |
| `scripts/ci_differential_fixtures.py:41` | 188 fixtures; the failed-`cd` and errexit fixtures from `:85`; the R638-6 probes from `:301`; the R639-6 probes. |
| `scripts/ci_differential_selftest.py:39` | The census equals the tree's shapes; the gate refuses an uncensused shape, a stale receipt and an unmet expectation by name. |
| `ci/image/syntax-census.json:241`, `ci/image/differential-receipt.json` | Census `shapes` (177) and the in-image receipt (188/188 at `sha256:98a31654…`). |
| `ci/image/exec_audit.py:62` | Seccomp filter; `_executed` (`:152`) reads the call from the caller's memory; `Origin` (`:187`) per-job provenance with `existing_copy` (`:197`) and `judge` (`:227`); `trace` (`:269`); `operands` (`:374`) and `invocation` (`:419`) read interpreter options; `judge` (`:459`) names, installers, copies and provenance; `selftest` (`:554`) 20 controls. |
| `ci/image/exec-audit.json:13` | Installer subcommands; programs (`:64`) and scripts (`:219`) the image runs. |
| `ci/image/audit_population.py:53` | `REPLACED` image forms; `TRIPLET` (`:70`); `image_form` (`:84`); `reached_steps` (`:150`); `listed_program` (`:173`) and `commands` (`:204`) match listed commands by what runs; `untripled` (`:236`); `merge` (`:247`); `trace_population` (`:303`). |
| `ci/image/exec-audit-receipt.json` | The merged population receipt at `afdf0ef0c` (see item 4). |
| `ci/image/package_roots.json:12`, `ci/image/sources.lock.json:2419`, `ci/image/smoke.py:64` | GNU time runtime consumer, lock row and smoke checks. |
| `ci/image/build.py:153` | `ci_python_walk.py` is a recipe input. |
| `ci/image/image.lock.json:3460` | Recipe `b3fdd900…` bound to image `sha256:98a31654…`. |
| `ci/image/command-table.json:13057` | Bare-metal gate re-pinned (F1); reviewed non-installing declarations for `scripts/check_nvm_capture.py` (`:13087`), `scripts/gen_hdl_reference_selftest.py` (`:13192`), `sw/firmware/ctrl/test/test_ctrl_firmware.py` (`:13332`) and `syn/ooc/pp_resource_gate_selftest.py` (`:13452`), which reflect on modules for patching. |
| `scripts/check_baremetal_only.py:439` | File-bound mask for the audit's `/proc` and `/etc` spellings. |
| `ci/image/tool-inventory.json:15` | Regenerated; the differential receipt is an input; 45 tool records byte-identical. |
| `docs/testing/CI_IMAGE.md:137` | Differential census; exact resolution (`:178`) with the failed-`cd` model (`:187`); execution audit (`:298`) with provenance, controls and the population runner (`:358`), its merge (`:388`) and the committed receipt (`:394`); GNU time parity (`:423`). |
| `scripts/ci_inventory_patterns_selftest.py:18` and the other walker self-tests | Run with the census gate off (the gate has its own self-test). Expectation changes, each the exact semantics item 1 requires and proven by a differential fixture against the real tool: `cd sub \|\| cd elsewhere`, `if true; then cd sub; fi` and `if cd sub; then …` with an existing `sub` now resolve (bash takes the certain branch; fixtures `bash-or`, `bash-and`, `bash-if-certain`, `bash-or-certain`), each paired with a new refusing control for the uncertain form; `source fragment.sh` now refuses (bash searches `PATH` first) and the followed-source controls use `./fragment.sh` (fixture `bash-source`); two refusal messages are reworded (`unsupported script language`, `undefined or unmodelled Make macro`). No control that refused an installer or unknown command was removed. |

### Round 7 full step sets at the committed head

Both sets were traced again inside the image (`--network none`, 16-CPU set, 13 GB) against fresh clones of `feef7c9fd`, with the five required submodules initialized and their roots and origins verified. docs-check ran as root and rtl-fast as uid 1000, as in the committed receipt.

- **docs-check: 46/46 steps, every exit status 0, zero findings** (16:02 to 16:47). This set includes every docs gate the workflow runs: the inventory check, the bare-metal and idiom gates, the documentation, TOC and anchor gates, the Entity shape gate, the builder bank and the act-runner contract self-tests.
- **rtl-fast: 48/48 steps, every exit status 0, zero findings** (16:02 to 17:35). It includes the lint ratchet, the yosys elaboration and its self-tests, the publication census, the firmware suites and RV32 builds, the three mutation campaigns, the coverage ratchet and the TSN stack boundary over both builders.
- Merged, as the committed receipt was: 94 of 98 traced, the same 4 replaced cache-miss builds, 183,837 exec instances, all 115 listed commands observed (111 with the listed arguments; the same 4 runner-value differences). Merged receipt sha256 `39d5828c…` (498,278 bytes, scratch); per-user receipts `0bf79a44…` (rtl-fast) and `2f4f27b7…` (docs-check, `round7-head-retrace-docs-check.json`); logs 186,694,430 and 24,395,519 bytes.
- Against the committed receipt (`round7-head-retrace-comparison.json`): the same step set, reconciliation, listed-command results, exit statuses and cleanliness, and zero population differences once per-run temporary names are normalized. Row counts by kind and provenance are identical. Instance counts differ only in two steps (15,557 vs 15,550 and 307 vs 306), from timing-dependent parallel work.

### Round 7 final checks

`round7-final-checks.json` records 26 checks run at `feef7c9fd` under CPython 3.12.3 after both step sets completed. All return rc 0, with `ci_tool_inventory.py --check` last:
- the inventory, pattern, node and exact walker self-tests;
- `ci_differential.py --check` (188 fixtures, 177 shapes) and the census-gate self-test;
- the build, integrity, privacy and privacy-patch self-tests;
- the bare-metal check (1,333 files, 0 findings) and its 738-arm self-test;
- the idiom gate and its 54 checks;
- the documentation, style, path, em-dash, TOC, anchor, hygiene and whitespace gates;
- `exec_audit.py --selftest` in the image (20/20, `round7-exec-audit-selftest.log`);
- `build.py --check-lock --verify-archive` on the second cold export;
- `build.py --prepare-only` (recipe `b3fdd900…`);
- `ci_tool_inventory.py --check`.

### Round 7 final disposition

Final head `feef7c9fd239ef62b7c6aad301e80a13275e47ef`, worktree clean, round-seven commits unpushed (`e1c7551ef` through `feef7c9fd`). The image is `sha256:98a31654…`, with recipe `b3fdd900…` bound in the lock; both cold exports authenticate, and only GNU time distinguishes it from the round-six image. Every assignment item is addressed. All 188 differential fixtures meet their expectation, the audit's 20 controls pass, the traced population is clean and reconciled, and the 45 tool records are unchanged. Independent re-review, the reviewer-owned coverage ledger, publication, adoption and merge remain outstanding. No push, registry login or PR modification occurred.

## Round 8

Assignment: PR #738 comment 6196923564 (close each guard by construction; threat model = accidental drift in reviewed source; evasion of a closed guard is RESIDUE).
Reviews: R638-7 (6196727731: N1, N2, N3) and R639-7 (6196901768: F1-F4), both NEGATIVE at `feef7c9fd`.
Starting head: `feef7c9fd239ef62b7c6aad301e80a13275e47ef`, equal to origin. Current dev `84f9e300` was not merged (no conflict forces it).

### Round 8 commits (one-line subjects, no push)

| Commit | Content |
|---|---|
| `1bcca3659` | Exec audit guards: foreign-ABI and x32 calls refused, non-path exec targets refused, interpreter programs by digest, programs by declared build output only, exec-time checkout digests and the checkout watch; controls split into `exec_audit_selftest.py`, operand readers into `exec_operands.py`. |
| `1cebf676b` | Walker: workflow `env:` names by allowlist; `local`/`declare` as bash; no certainty from checkout state; `$(cd X && pwd)` only where a failed `cd` cannot continue; 23 new fixtures; census 178 shapes. |
| `e977cc44b` | R639-7-S2 (PYW2 primes `subprocess`, sentinel runs), R638-7-S4 (installer subcommands past leading options), the dash loader-import control. |
| `dd824ee1c` | Held streamed programs: exec completes with a pending SIGSTOP (`SECCOMP_FILTER_FLAG_WAIT_KILLABLE_RECV`), text read once writers close, then SIGCONT (fixes a deadlock with vfork-spawned `python3 -`); file-state helpers moved to `exec_files.py`. |
| `facc20020` | Generated programs by masked digest; the checkout watch scoped to the inventory's inputs; reviewed `checkout_writes`. |
| `cd9ef1bef` | Lock re-recorded for recipe `4f7a0b3b…` (only `recipe_digest` changes; image bytes unchanged). |
| `7b976dbbd` | Reviewed lists: 81 inline/streamed programs, 334 generated programs, one checkout write. |
| `c2531c634` | `docs/testing/CI_IMAGE.md`: threat model and each guard as built. |

### Round 8 changes (file:line at `c2531c634`)

| Item | Where | What |
|---|---|---|
| 1 ABI | `ci/image/exec_audit.py:86` `FILTER`; `:76` flags; `:621` `_Trace.notified` | Any non-x86-64 arch and any x32-bit call is notified and refused with EPERM before it runs, named `i386 system call refused: 11` / `x32 system call refused: 520`. exec, execveat and exit_group are notified; everything else allowed. |
| 2 non-path | `exec_audit.py:191` `resolve`, `:239` `_target`, `:282` `_loaded` | Path resolved component by component (symlinks, `..`, ENOTDIR/ELOOP as exec's lookup), refusing anything through the process filesystem or `/dev`; AT_EMPTY_PATH needs the descriptor's link to resolve to the same inode; the caller's own view (cwd/root/fd links) must be the same file; failed lookups return the errno exec would; non-ELF non-`#!` files get ENOEXEC (nothing runs). |
| 3 programs by digest | `exec_audit.py:414` `Origin.judge`; `ci/image/exec_operands.py:31`, `:56`; `exec_audit.py:485` `_stream_source`, `:509` `_pipe_text`, `:571` `_Trace` | Inline text read from argv as bash/dash/CPython read options; streamed text read without consuming it (tee) once every writer closed the pipe (POLLHUP), holding the interpreter stopped before its first instruction; accepted only by exact digest in `inline_programs`, the step's own text, or a checkout file; `dash` (`EXEC_ONLY`, `exec_operands.py:17`) judged by its execs. |
| 4 provenance | `exec_audit.py:391` `started_exec`, `:401` `ended`, `:787` `built_output`, `:321` mask | A program outside the image needs the bytes of a successful toolchain invocation's declared output (`-o`, `--output`, `a.out`), digested at that invocation's exit_group if it wrote it; renamed/installed copies keep it; else `generated_programs`. Job-written in-process interpreter scripts: checkout copy, image copy (judged by name), step text, or `generated_programs` by masked digest. Creation time and byte inequality are not used. |
| 5 env allowlist | `scripts/ci_syntax.py:23` `HOOKS`, `:36` `workflow_environment`; `scripts/ci_tool_inventory.py:201`; `ci/image/syntax-census.json:1207` | 25 reviewed names; `BASH_FUNC_*` and hooks (`PERL5OPT`, `NODE_OPTIONS`, `GIT_EXEC_PATH`, `GIT_CONFIG_*`, `PYTHONUSERBASE`, `PYTHONSTARTUP`, `LD_AUDIT`, `HOME`, …) refused by name; others refused as unmodelled. |
| 6a declarations | `scripts/ci_shell_walk.py:546` `declaration`, `:583` `declared_value` | Initializers expand before any local is created; a new local hides and is empty; re-declaring a same-function local keeps its value; appending forms refused (by the syntax census). |
| 6b certainty | `ci_shell_walk.py:422` `certain`, `:862`; `:325` `exact_substitution`, `:737`, `:745` | Only `true`, `:` and plain assignments are certain; any `cd` without errexit leaves the directory ambiguous; `$(cd X && pwd)` literal only as the sole substitution of a bare assignment under errexit, or for the running script's own directory before any command ran (new shape `bash:word.cd-pwd.script-directory`, `scripts/run_all_suites.sh:110`). |
| 6c rewritten scripts | `exec_audit.py:414` (exec-time digest), `:367` `sweep`, `:341` scope; `ci/image/exec_files.py:54` `Watch` | Every file present at job start is digested; a script whose bytes differ at its exec is a finding; any change to an inventory input during the job is a finding (inotify read at every notification, full compare at step end); `checkout_writes` records reviewed rewrites. |
| Fixtures | `scripts/ci_differential_fixtures.py:75`, `:79`, `:107`, `:425`-`:456` | 211 fixtures (188 + 23): N3a exported function, unmodelled name and 9 hooks; N3b if/or after an rmtree; F1 initializer, redeclared, new local, words-first, declare, nested scope, appending; cd-pwd script-directory and after-a-program; true-certain; `bash-if-certain`/`bash-or-certain` now refused; `bash-and`, `bash-cd-pwd`, `sh-block` reshaped to keep their focus shapes. |
| Population | `ci/image/audit_population.py:342` | Origin per job with the job's scratch root for masking; step text accepted by digest. |
| Docs | `docs/testing/CI_IMAGE.md:62` threat model, `:224` exact resolution, `:356` execution audit | Threat model, each guard as built, named boundaries. |

### Round 8 tool inventory, image and lock

- The 45 tool records and the 303 residue lines are byte-identical to `feef7c9fd` (`ci_tool_inventory.py --write` changed only the census and receipt input digests).
- Recipe `4f7a0b3b84da7816d8cb1d21f1d87905c771748127a83820f4b86d727a17dd44`. Two cold builds: 463,836 ms and 446,068 ms; image `sha256:98a316549753d63e8b4118dc0f85af3e3813d667485817ee96f6dd597ba1c059`, config `sha256:a2c4d52af85bc218ddd2d3958a2283f64ab175ec4254960eba891ae2271df1fd`, 3,930,997,226 bytes; both exports byte-identical (1,135,069,184 bytes, sha256 `0bdcc1d4a7d8ce6b9b8c98b9f0a5e04cbe20a5fb2b7083467c88785b5a6568a6`); `--record-lock` PASS on export A, `--check-lock --verify-archive` PASS on export B. Layer table unchanged from round 7 (only the lock's `recipe_digest` changes).

### Round 8 evidence so far

- Differential harness in the image, offline: 211/211 fixtures meet their expectation; 178 census shapes (`round8-differential-harness.log`).
- Exec audit selftest in the image (root, network none): 41/41 controls (`round8-exec-audit-selftest.log`).
- Exploratory traces: explore1 at `1bcca3659` (stopped: vfork deadlock found, fixed in `dd824ee1c`); explore2 at `dd824ee1c` (98 reached, 94 traced, all exit 0; findings were the unpinned programs that became the reviewed lists, and three tracked files rewritten during docs-check: two regenerated headers outside the walker's inputs and `tb/verilator/csr/Makefile`); explore3 at `facc20020` (docs-check and the rtl jobs that write programs, for masked digests). Inline and streamed digests are identical across round 7's two traces and explore2 (74 inline texts); 67 of 68 docs-side digests matched between explore2 and explore3.

- Smoke inside the image as its default user, offline: rc 0, 133 JSON records (97 commands, all rc 0), `PASS: all image tool families` (`round8-image-smoke.log`). Under uid 1000 the smoke stops at `sudo --version`, as before; the documented invocation uses the default user.

### Round 8 final population and checks

- Final trace at `c2531c634` (tree `69b94ed6…`, base `fa7347fc`, the six submodule lines unchanged), image `sha256:98a31654…`, `--network none`, clean clones with the five fetched submodules: docs-check 46/46 traced as root, rtl-fast 48 traced as uid 1000; **94 of 98 reached steps traced, every exit status 0, zero findings**; 183,834 exec instances; the 4 untraced steps are the cache-miss Verilator and Yosys builds the image's layers replace (reconciliation names each with its reason). All 115 round-six gate commands observed, 111 with the listed arguments (the same 4 runner-value differences as round 7). Population rows 2,042 by provenance: named 606, `dash` exec-only 505, generated (reviewed list) 357, checkout 242, step text 94, pinned inline/streamed 93, built by a traced linker 93, copy (of a build output, a checkout file or an image file judged by name) 51, absent 1. One reviewed checkout write recorded (`tb/verilator/csr/Makefile` in docs-check step 49).
- Committed as `ci/image/exec-audit-receipt.json` in `1c4d722cb` (531,052 bytes, sha256 `9f3ff9084c89d68c63c2b5d6b0ca88672b773facb58c32ba1370db8a7a87cd1c`); `1c4d722cb` changes only the receipt, so the receipt names its parent `c2531c634`. Per-user receipts: docs `443ef22e…` (161,459 bytes, `round8-population-docs-check.json`), rtl `3f34f0d0…` (376,700 bytes, scratch); step logs 46 files 25,964,623 bytes and 48 files 202,671,356 bytes (manifests in `round8-population-receipt.json`). No head re-trace was run this round.
- Final checks at `1c4d722cb` under CPython 3.12.3: all 26 rc 0, the inventory `--check` last (`round8-final-checks.json`, logs in `round8-final-checks-logs/`): inventory, patterns, nodes and exact self-tests; differential check (211 fixtures, 178 shapes) and census-gate self-test; build, integrity, privacy and privacy-patch self-tests; bare-metal check (0 findings, 1,336 files) and self-test (738 arms); idiom and its self-test; docs, doc-style, doc-paths, em-dash, TOC, anchors, hygiene, whitespace; the exec audit self-test in the image (41/41); `--check-lock --verify-archive` on export B; `--prepare-only` (recipe `4f7a0b3b…`); `ci_tool_inventory.py --check`.
- Read-only merge shape with current dev `84f9e300`: `git merge-tree` writes `e7fc8c81…` with no conflict; 0 files overlap.

### Round 8 disposition of findings

| Finding | Disposition | Control |
|---|---|---|
| R638-7-N1, R639-7-F2 (inline/streamed programs unjudged) | Closed by digest allowlist; any other refused by name | `-c` and `-` local-wheel installs refused; `print(1)` pinned clean; vfork-spawned stream read whole |
| R638-7-N2 (foreign ABI, fd/memfd execs), R639-7-F3 | ABI refused before it runs; non-path targets refused before they run | i386 and x32 trampolines (marker never runs); memfd, deleted file, descriptor link |
| R639-7-F4, R638-7-N2 copies (provenance by inequality) | Positive provenance only | appended-byte copy and failed-build output refused; renamed, installed and `a.out` outputs clean |
| R638-7-N3a (workflow env denylist) | Allowlist of 25 names; hooks and `BASH_FUNC_*` by name | 11 `R638-7-N3a-*` fixtures |
| R638-7-N3b (certain `cd` from checkout state) | No certainty from the checkout | `R638-7-N3b-if`, `-or` refused as ambiguous; patterns self-test arms |
| R638-7-N3c (rewritten script) | Exec-time digest and checkout watch | rewritten script and rewritten sourced file caught |
| R639-7-F1 (local declarations) | Bash semantics, differentially proven | 7 `R639-7-F1-*` fixtures |
| R638-7-S3 (`/sbin//initctl`) | Paths joined with pathlib | receipt spells `/sbin/initctl` |
| R638-7-S4 (subcommands after options) | First operand after options | `cargo +stable -v install` caught |
| R639-7-S2 (PYW2 sentinel) | Fixture primes `subprocess` | real status 0 and sentinel, refused by name |
| R638-7-S1, S2; R639-7-S1 | Not taken (optional) | — |

Final head `1c4d722cb1d0279f0ec44b0fbe87c810adfb9267`, worktree clean, round-eight commits unpushed. Independent re-review (R638-8, R639-8), the reviewer-owned coverage ledger, publication, adoption and merge remain outstanding. No push or registry login occurred.

REVIEW READY posted as issue #737 comment 6203674207 (`ROUND8-REVIEW-READY.md`).

## Round 9

Assignment: PR #738 comment 6204018211 (two guards were not closed; close them on bytes and on fail-closed text).
Reviews: R638-8 (6204009418: N1, N2 MAJOR; N3, N4 MINOR; R1, R2 RESIDUE) and R639-8 (6203890877: F1 MAJOR = N1; F2 MINOR; RES1 = R1; S1), both NEGATIVE at `1c4d722cb`.
Starting head: `1c4d722cb1d0279f0ec44b0fbe87c810adfb9267`, equal to origin.

Status: REVIEW READY at `6f86eee604729b80684526fc5b9be720d94f179a`, posted as issue #737 comment 6207079152 (`ROUND9-REVIEW-READY.md`). Round-nine commits unpushed (`b83e2966e` through `6f86eee60`); worktree clean. Independent re-review (R638-9, R639-9), the reviewer-owned coverage ledger, publication, adoption and merge remain outstanding. No push, registry login or PR modification occurred.

### Round 9 commits (one-line subjects, no push)

| Commit | Items | Content |
|---|---|---|
| `b83e2966e` | 1, 2 | Interpreter families by the identity of the image's own files; exact Perl, Node and Tcl option readers; unreadable text and unmodelled options refused; programs are the image's own only by their job-start key, otherwise item-4 provenance; the `dash` exemption bound to the image's `dash` file; one image snapshot per population run; 65 controls. |
| `8f66a634f` | 3 | The load's own errno or reason is answered and the target kept apart; bash's in-process run of a text file without `#!` is judged as a bash script; an exec the audit cannot judge is refused, never left unanswered; 71 controls. |
| `ce3dd4bd3` | 5, 6 (R1) | `$(realpath <literal>)` only for the running script's own unlinked path before it runs a command; a substitution's words expand with the state at its start; `certain()` reads words without running them; fixtures `bash-realpath-script-path` (focus) and `bash-realpath-after-a-program` (refused, probe R638-8-N4); the probe-group comment reworded; census 178 shapes; 213/213 fixtures. |
| `4df2f2f06` | 5 | Lock re-recorded for recipe `53fb5abd…` (only `recipe_digest` changes; image bytes unchanged). |
| `6ed849b93` | 1 | Inline and streamed texts identified with job-temporary paths masked; no `.` or `..` component is masked (R638-8-S1); 73 controls. |
| `575e7df8c` | 1 | A checkout path in a program text masked below what the checkout held at job start (a job-written file); masked paths start a word; 74 controls. |
| `e41f18f65` | 1, 4 | Reviewed lists: 23 streamed Tcl texts and 117 generated Tcl drivers added; the self-test's three entries moved out of the production lists. |
| `84caae9af` | 4, 6 (R2) | `docs/testing/CI_IMAGE.md`: accepted sources per kind, identity, readers, fallback, masks, `realpath`, the notify-then-lookup limit. |
| `6f86eee60` | 7 | The re-traced population receipt. |

### Round 9 changes (file:line at `84caae9af`)

| Item | Where | What |
|---|---|---|
| 1 readers | `ci/image/exec_operands.py:32` `FAMILIES`, `:41` `interpreter`, `:46` `refused`, `:51` `shell_operands`, `:85` `python_operands`, `:128` `perl_operands`, `:188` `node_operands`, `:230` `tcl_operands` | Each family's command line read as the interpreter reads it (perl 5.38 `S_parse_body`/`moreswitches`, node 22, Tcl 8.6 `Tcl_Main`, CPython 3.12, bash/dash). Perl switches bundle and each `-e`/`-E` adds its text and a newline; node's last `-e`/`--eval`/`-p`/`-pe` wins; `tclsh` script iff its first word lacks a leading `-` (or `-encoding NAME FILE`). Refused by name: shell `-i`, `-l`, `--login`, `--rcfile`, `--init-file`, `--debugger`; Python `-i` and unknown letters; Perl `-M`, `-m`, `-d`, `-D`, `-x`, `-S`, `-V`, `-v`, `-h`, `-0x`, unknown switches; every node option outside the modelled set; any `-c`/`-e` without its text. |
| 1 text | `ci/image/exec_audit.py:462` `Origin.judge`, `:407` `masked`, `:412` `held`, `:848` `judge` | Every family's inline and streamed text is read (streams for every family, held as before); accepted only as the step's own text or a reviewed `inline_programs` entry of that interpreter, keyed by masked digest; unreadable text refused (`streamed program not readable at its exec`); `interpreter command line refused: …` for unmodelled options. |
| 1 masks | `ci/image/exec_audit.py:119` `WORD`, `:121` `COMPONENT`, `:345`, `:351`-`:352` | A masked path starts a word, holds only name characters and no `.`/`..` component; under `/tmp` or a job scratch root, or a checkout path below what the checkout held at job start. Checked against every round-8 reviewed digest: 333 generated and 81 inline entries unchanged. |
| 2 identity | `ci/image/exec_files.py:124` `Image`, `:157` `held`; `ci/image/exec_audit.py:427` `identify`; `ci/image/exec_operands.py:261` `invocation`; `ci/image/audit_population.py:322` | The image's executables are snapshotted once before any job; a program is the image's own only if its physical path is in that snapshot with an unchanged key; an interpreter is such a file named for a family or holding a named file's bytes; the family and `dash`'s exec-only status come from that identity, never from the name the program was run by. Any other program, whatever its name or directory, needs a traced build output's bytes or the reviewed generated list. |
| 3 loader | `ci/image/exec_audit.py:717` `executed`, `:762` `fallback`, `:692` `notified`, `:661` `finish`, `:255` `_target`, `:301` `_loaded` | The target and the load are kept apart; the load's errno is answered, a refused `#!` interpreter refused with its own reason; stat races return the exec's errno; an exception while judging refuses the call (`exec not judged: …`), a held stream that cannot be judged is killed. On ENOEXEC from the image's `bash` (bash's `shell_execve`: no empty file, no NUL in the first line or two after `#!`, within 128 bytes) the file is judged as a script of that `bash`; `dash` re-execs `/bin/sh`, which is seen. |
| Controls | `ci/image/exec_audit_selftest.py:33` `CONTROLS`, `:271` `interpreter_programs`, `:185` `provenance`, `:319` `masks`, `:336` `loader_errors`, `:360` `selftest` | 74 controls (41 kept, 33 new). The self-test's own reviewed entries are merged for its steps only. |
| 4 lists | `ci/image/exec-audit.json` | `checkout_writes` 1 entry; `inline_programs` 103 (44 shell, 36 Python, 23 Tcl); `generated_programs` 450 (298 Python, 117 Tcl, 35 shell). |
| 4, 6 docs | `docs/testing/CI_IMAGE.md:71` guard table, `:85`-`:101` boundaries (the notify-then-lookup limit at `:99`), `:313` realpath, `:378` execution audit, `:405` interpreters and readers, `:429` accepted sources per kind, `:439` masks | As built. |
| 5 walker | `scripts/ci_shell_walk.py:325` `own`, `:331` `exact_substitution`, `:436` `certain`; `scripts/ci_differential_fixtures.py:40`, `:74`-`:85`; `scripts/ci_inventory_exact_selftest.py:135`-`:149`; `ci/image/syntax-census.json:294` | See commit `ce3dd4bd3`. |
| 6 R1 | `scripts/ci_differential_fixtures.py:437` | "Probes for workflow environment names, checkout state and local declarations". |

### Round 9 tool inventory, image and lock

- The 45 tool records and the 303 residue lines are byte-identical to `1c4d722cb`; `ci_tool_inventory.py --write` changed only the census and differential-receipt input digests.
- Recipe `53fb5abd7dc664e8ce168e7c08d5f4b5b09503905ff03fd3fbdf80b394ba2bfa`. Two cold builds: 411,216 ms and 493,323 ms; image `sha256:98a316549753d63e8b4118dc0f85af3e3813d667485817ee96f6dd597ba1c059`, config `sha256:a2c4d52af85bc218ddd2d3958a2283f64ab175ec4254960eba891ae2271df1fd`, 3,930,997,226 bytes; `--record-lock` PASS on export A, `--check-lock --verify-archive` PASS on export B (`round9-cold-chain.log`). The layer table is unchanged; only the lock's `recipe_digest` changes.

### Round 9 evidence

- Self-test in the image (root, network none): 74/74 (`round9-exec-audit-selftest.log`).
- Differential harness in the image, offline: 213/213 fixtures; 178 census shapes (`round9-differential-harness.log`). `bash-realpath-after-a-program`: real runs record `zz_probe ok` and, with the link re-pointed, `zz_probe hidden`; the walker refuses (`unclassified runtime command name '${RUNTIME}/run.sh'`).
- Exploratory trace at `8f66a634f` (`explore1`): docs-check 46 and rtl-fast 48 traced, every exit 0; the only findings were the newly judged Tcl programs (23 streamed builder-gate texts, 484 IOB-pack arm drivers, 274 OOC and placement drivers), which became the reviewed entries. No option refusal, identity or provenance finding appeared anywhere else.

### Round 9 final population and checks

- **Final trace.**
  - Traced at `84caae9af` (tree `6932e0aa…`, base `fa7347fc`, the six submodule lines unchanged) in image `sha256:98a31654…`, with `--network none`.
  - Clean clones with the five fetched submodules; docs-check 46/46 traced as root, rtl-fast 48 traced as uid 1000.
  - **94 of 98 reached steps traced, every exit status 0, zero findings**, 183,831 exec instances.
  - The 4 untraced steps are the cache-miss Verilator and Yosys builds the image's layers replace.
  - All 115 round-six gate commands observed, 111 with the listed arguments; the other 4 are the same runner-value differences as before.
- **Population rows.**
  - 2,124 rows by provenance: image 603, `dash` exec-only 505, generated (reviewed list) 419, checkout 242, pinned inline or streamed 116, step text 94, built by a traced linker 93, copy 51, absent 1. A copy is of a build output, of a checkout file, or of an image file judged by name.
  - All 103 inline or streamed and 450 generated reviewed entries are used by the population, and it uses no other.
  - One reviewed checkout write: `tb/verilator/csr/Makefile` in docs-check step 49.
- **Against the round-8 receipt** (`round9-population-comparison.json`).
  - The step set, reconciliation, listed-command results and exit statuses are the same.
  - 555 rows are relabelled from `named` to `image`: provenance by identity.
  - The three `program tclsh8.6` rows are replaced by the Tcl scripts and streams they run: 23 pinned streams, and the IOB-pack, OOC and placement drivers as generated rows.
  - Nothing else differs.
- **Committed receipt.** `ci/image/exec-audit-receipt.json` in `6f86eee60`: 546,532 bytes, sha256 `56e0a4192f65a6516d6e3e8551dc4193382de962a7ce6b2a4f2ae48c15ae3e6b`. `6f86eee60` changes only the receipt.
  - The per-user receipts are docs (`round9-population-docs-check.json`) and rtl (scratch; digest in `round9-population-receipt.json`).
  - Step logs: 46 files, 30,816,876 bytes, and 48 files, 206,761,489 bytes; their manifests are in `round9-population-receipt.json`.
- **Final checks.** At `6f86eee60` under CPython 3.12.3, all 26 return rc 0, with the inventory `--check` last (`round9-final-checks.json`, logs in `round9-final-checks-logs/`). They are:
  - the inventory, patterns, nodes and exact self-tests;
  - the differential check (213 fixtures, 178 shapes) and the census-gate self-test;
  - the build, integrity, privacy and privacy-patch self-tests;
  - the bare-metal check (0 findings, 1,336 files) and its self-test (738 arms);
  - the idiom gate and its self-test;
  - the docs, doc-style, doc-paths, em-dash, TOC, anchors, hygiene and whitespace gates;
  - the exec audit self-test in the image (74/74, `round9-exec-audit-selftest.log`);
  - `--check-lock --verify-archive` on export B;
  - `--prepare-only` (recipe `53fb5abd…`);
  - `ci_tool_inventory.py --check`.
- **Merge shape.** A read-only `git merge-tree` with the current dev `734eb780` writes `210759d5…` with no conflict, and 0 files overlap.

### Round 9 decisions published

Decision points, published for the reviewers and the manager:

1. **Masked identity for inline and streamed texts.** The round-eight mask for generated programs now also keys inline and streamed texts. The builder gates' timing-grade cases stream Tcl that names a per-run report directory, so an exact digest would change on every run. A text without a job-temporary path keeps its exact digest; all 80 earlier inline and streamed entries are unchanged.
2. **A job-written checkout path is masked.** The OOC Tcl harness writes its mutant to `syn/ooc/.ooc-mut-<random>.tcl` and its driver sources that file. In a program text, a checkout path is therefore masked below the part the checkout held when the job started. A file the checkout held stays exact, and so does a `..` component. Checked against the round-eight traces, no earlier reviewed digest changes. With R638-8-S1 taken, a masked path also starts a word and has no `.` or `..` component.
3. **Readers refuse more than the controls named.** Besides unmodelled options, the readers refuse options that make an interpreter read code other than its program. These are shell `-i`, `-l` and `--login`, Python `-i`, Perl `-M`, `-m`, `-d`, `-x` and `-S`, and Node's preload, loader and interactive options. None occurs in the reached population.
4. **R638-8-R2 wording.** The boundary text is the reviewer's, with "the call" in place of one word. The bare-metal gate (#259) refuses that word in every tracked file.
5. **Expectation changes, each stricter.**
   - `ci_inventory_exact_selftest.py` now expects a step-level `$(realpath sub/bootstrap.sh)` to be refused as runtime, and adds an own-path control and an after-a-command control.
   - The `bash-realpath` fixture is no longer the focus fixture: its argument is runtime, and the outcome is still identical.
   - The audit's refusal names "system program/script not in the allowlist" become "image program/script not in the allowlist".
6. **Module split.** The idiom gate's 1000-line limit moved the image snapshot to `exec_files.py`, and `invocation`, `lexical`, `subcommand` and `built_output` to `exec_operands.py`. `ci_shell_walk.py` is at the limit.

### Round 9 disposition of findings

| Finding | Disposition | Control |
|---|---|---|
| R638-8-N1, R639-8-F1 | Closed: every family and spelling reads its text exactly or refuses by name; unreadable text refused | unlisted `perl -e`, `-le`, `-wE`, `-l012e … -e …`, `node -e`, `--eval=`, `-p -e`, `\| tclsh`, `\| tclsh8.6`, `\| python3` refused with the digest of the text run; pinned Perl, Node, Tcl texts clean; socket stream refused |
| R638-8-N2 | Closed: image programs by job-start identity; everything else item-4 provenance; `dash` by its file | appended `/usr/local/bin/cp`, appended `python3` with a checkout script, `bash` named `dash` refused; build outputs, `a.out`, LeakSanitizer, `initctl` stub clean |
| R639-8-F2 | Closed: own errno and reason; never raises; fallback judged | no-`#!` text by `bash` (job-written refused, checkout clean), `dash` fallback observed, binary file and missing interpreter run nothing, `#!/proc/self/exe` refused with its reason |
| R638-8-N3 | Closed: guide, docstring and PR body list the accepted sources per kind; self-test entries out of the production lists | `checkout_writes` holds one entry |
| R638-8-N4 | Closed: `realpath` like `cd … && pwd` | `bash-realpath-after-a-program` refused; `bash-realpath-script-path` identical |
| R638-8-R1, R639-8-RES1 | Comment replaced with the manager's text | — |
| R638-8-R2 | Named in the guide's boundary list | reviewer's text, with "the call" for the word the bare-metal gate forbids |
| R638-8-S1 | Taken: no `.`/`..` component is masked | `..` control |
| R639-8-S1 | The `dash` boundary is restated precisely and bound to the image's file | dash loader check; `bash` named `dash` refused |
| R638-8-S2, S3, S4 | S2 addressed by N2; S3, S4 not taken (optional) | — |
