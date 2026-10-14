[A615]

# Image lane handoff

Status: REVIEW READY for PR #738. The corrected compiler-backed campaign completed with rc 0 in 1,014,708 ms (1014.708 seconds), without a timeout. All 103 builder function invocations returned across nine groups; the existing mf48 resource-calibration and inert MAKEFLAGS mutation arms remain NOT RUN.
Head: `18f2df92b13cb3f4036b073ed76940187bf10487`.
Branch: `737-ci-image`; base: `fa7347fc59173f90e4feec2df207692e6e6e72ec`.
Relates to #737 and PR #738. Executor: [A615]. Internal reviewer: [R638]. External reviewer: [R639].
No push, PR edit, merge, firmware change, linked-image change or product-test assertion change was made.

## Authority

Assignment: issue #737 comment 6160953880. Round 2: PR #738 comment 6162190578. Privacy ruling: comment 6162652582. Patched-file refinement: comment 6163057631. Background-run authorization: PR #738 comment 6165220472. Setup correction and rerun: PR #738 comment 6166238176.
CONTRIBUTING.md, docs/README.md, REQUIREMENTS.md and the linked CI/toolchain documents were read. The explicit assignment authorized this lane despite the shared board remaining Backlog.

## Changes

| File:line | Change |
|---|---|
| `ci/image/Dockerfile:1` | Pinned base and distinct filesystem layers; fixed build epoch; documented runtime environment. |
| `ci/image/build.py:134` | Bind the recipe and each layer to exact inputs; clean allowlisted context; cold-build option; exported image identity and privacy verification before lock generation. |
| `ci/image/build_selftest.py:20` | Source, pin, duplicate, traversal, download and derived-CPU refusal controls. |
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
| `scripts/ci_tool_inventory.py:265` | Follow workflows and reached scripts/Makefiles; resolve supported installers and refuse unsupported or ambiguous installation forms. |
| `scripts/ci_tool_inventory_selftest.py:12` | Planted installer/action/Makefile/string/variable and drift controls; harmless comparison data remains accepted. |

## Derived tool inventory

Every installing workflow/job/step is retained below. Runner tools are inherited from the recorded runner image rather than installed by a shell step. Dependency packages and every archive pin are recorded in the source and image locks.

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
| VexiiRiscv | `litex.soc.cores.cpu.vexiiriscv.core:git_setup` / `235753e24f2d960e49a0852205bae1400bf22c19` | `.github/workflows/elaborate.yml:elaborate` / Place the VexiiRiscv source at the revision LiteX pins |
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
| rv32-sdk | `riscv32-ilp32d--glibc--stable-2025.08-1` / `riscv32-ilp32d--glibc--stable-2025.08-1` | `.github/workflows/docs.yml:docs-check` / Install and verify the pinned RV32 SDK<br>`.github/workflows/elaborate.yml:elaborate` / Install and verify the pinned RV32 SDK<br>`.github/workflows/rtl-fast.yml:firmware-unit` / Install and verify the pinned RV32 SDK<br>`.github/workflows/rtl-fast.yml:firmware-control-mutants` / Install and verify the pinned RV32 SDK<br>`.github/workflows/rtl-fast.yml:firmware-aecp-mutants` / Install and verify the pinned RV32 SDK<br>`.github/workflows/rtl-fast.yml:firmware-srp-mutants` / Install and verify the pinned RV32 SDK<br>`.github/workflows/rtl-fast.yml:firmware-boundary` / Install and verify the pinned RV32 SDK<br>`.github/workflows/rtl-fast.yml:firmware-verilator` / Install and verify the pinned RV32 SDK |
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

### Additional consumed package roots

| Package | Exact pin | Consumer / reason |
|---|---|---|
| docker-ce-cli | `5:28.0.4-1~ubuntu.24.04~noble` | `docs.yml:docs-check` / Local act runner contract gate<br>`scripts/act_ci.py`: The docs workflow's offline runner selftest constructs and checks its isolation prefix. |
| sudo | `1.9.15p5-3ubuntu5.24.04.4` | `docs.yml:docs-check` / Local act runner contract gate<br>`scripts/act_ci.py`: The docs workflow's offline runner selftest constructs and checks its isolation prefix. |
| clang | `1:18.0-59~exp2` | Image recipe / system package stage<br>`third_party/tsn-c-stack/scripts/check_boundary.py`: The workflow's stack boundary gate compiles with both compilers. |
| cmake | `3.28.3-1build7` | `rtl.yml:verilator-shards` / Build the pinned tsn-gen field oracle on its suite owner<br>`.github/workflows/rtl.yml`: The protocol oracle is built with CMake. |
| curl | `8.5.0-2ubuntu10.15` | `elaborate.yml:elaborate` / Install the pinned sv2v release<br>`elaborate.yml:elaborate` / Install sbt<br>`.github/workflows/elaborate.yml`: Workflow downloads use the command-line HTTP client. |
| ca-certificates | `20260601~24.04.1` | `elaborate.yml:elaborate` / Install the pinned sv2v release<br>`elaborate.yml:elaborate` / Install sbt<br>`elaborate.yml:elaborate` / Build Verilator from source on cache miss<br>`.github/workflows/elaborate.yml`: Public HTTPS tool downloads require the system trust store. |
| openjdk-17-jdk-headless | `17.0.20.1+1-1~24.04` | `elaborate.yml:elaborate` / Install sbt<br>`.github/workflows/elaborate.yml`: The Scala toolchain requires Java 17 and its compiler. |
| unzip | `6.0-28ubuntu4.1` | `elaborate.yml:elaborate` / Install the pinned sv2v release<br>`.github/workflows/elaborate.yml`: The converter installation extracts a ZIP archive. |
| xz-utils | `5.6.1+really5.4.5-1ubuntu0.3` | `docs.yml:docs-check` / Install and verify the pinned RV32 SDK<br>`elaborate.yml:elaborate` / Install and verify the pinned RV32 SDK<br>`rtl-fast.yml:firmware-unit` / Install and verify the pinned RV32 SDK<br>`rtl-fast.yml:firmware-control-mutants` / Install and verify the pinned RV32 SDK<br>`rtl-fast.yml:firmware-aecp-mutants` / Install and verify the pinned RV32 SDK<br>`rtl-fast.yml:firmware-srp-mutants` / Install and verify the pinned RV32 SDK<br>`rtl-fast.yml:firmware-boundary` / Install and verify the pinned RV32 SDK<br>`rtl-fast.yml:firmware-verilator` / Install and verify the pinned RV32 SDK<br>`scripts/ci_rv32_sdk.py`: The existing SDK installer extracts its checked XZ archive through tar. |
| python3-venv | `3.12.3-0ubuntu2.1` | Image recipe / system package stage<br>`ci/image/install.py`: The recipe creates the isolated Python prefix. |
| automake | `1:1.16.5-1.3ubuntu1` | Image recipe / system package stage<br>`ci/image/smoke.py`: Retain the existing image smoke's build-system version check. |
| ninja-build | `1.11.1-2` | Image recipe / system package stage<br>`ci/image/smoke.py`: The existing image smoke builds its CMake fixture with Ninja. |

## Dockerfile layers and lock

Manifest: `sha256:8cc05a5c51aa04a23063c5d0593065912845a4ba4ce5a5dfd3ff53b12ccd1d19`.
Config: `sha256:1eac3b02d4109a09c63bbf68893a2695c6380f1ce6d444168a3828c9a83e0b9b`.
Recipe: `a6fd01e6bf2ced24f6a68a33c899199dfda2eb46fe4a0def569542d5c5240b7f`.

| Layer | Tool/source entries | Per-layer recipe digest | OCI digest |
|---|---|---|---|
| system | 183 | `1100a5332daa5348841a9648dfb473d4d4fbc481eba93d08ed13c9bcdbb5a11c` | `sha256:d0069157b863d07eea5fcbfc9ee66b570e10d1aa60777775c3563783966b9737` |
| gtest | 3 | `baee4c785f9ab25254df6fcdbf49b1d4653e57f906326901d9a79a0376973830` | `sha256:24553cea3585e22b395adf775b099eb7aaa2d9454c7781aa55a4b3b1e139fb6a` |
| python | 28 | `ec12881013b00aab38c47744ed58f550af5c0b9538b1afdb9ed65cbf0eb6adfa` | `sha256:ccf8dd6ad48dc2ccc0aed6480859bd2ecb65398fcb5176854aa543f4c2665a41` |
| litex | 13 | `802c686a2b6270251daad24a10c497c5eef6d9f21ab26f1403be5e1f2010588c` | `sha256:72443935f2aac03c176be8c487114571e1c8451482d08014f4c2a94af8ec1768` |
| verilator | 1 | `83884a9407625d3f679412a0de32b886b318555c629d88c4d6113298b53b5420` | `sha256:221d9dbcae4a620737a7865b08d0225f19123404e1dc6f3f6fad718fa6bf54e3` |
| yosys | 3 | `d638c23309155928cd27b1886a600df5e359f651eb8ed89d35c141ffbb115ddf` | `sha256:abf98b1fd75417049213b62d411bed952b862cebf602f150974c40f3235f5157` |
| rv32 | 1 | `7f53570b95c5c1902d1e5e706dcc987a29106e91dec881af31bc16acd4571789` | `sha256:5f5a5c47cb0db16a41ad0cc057d2383ef989a28172da4e8c7a8a502ea3ab5d3c` |
| sv2v | 1 | `50d6c97941c0c570f10f99382b1d2df54b540e1746e10c63d7a68b747ce984f9` | `sha256:dca2e7a4352a8f069098b0e72ba771f4f6f19124795f8c9cbfd2d1c989513536` |
| sbt | 424 | `e86de0e6787f3c26b2a387ac9a5b9932f1917d86227c457741abebe2e0b61f8c` | `sha256:2ea388efe8d5ebebc23b60672941b852b518d7e6622e087bbcb3d73b9000fea1` |
| oracle | 6 | `89befee10d7fcecade31ab761528eb75601d64af8792a134ab5426012a4fa079` | `sha256:4f577b318f2252bfd426276bca8e1ab971fb03b925b67f032e11e7029bff511d` |
| node | 1 | `6663bbd4ce59489b7080fc1415b9b5d23de6e46c8f31462bc9f6089eb37faefa` | `sha256:a1272fb2b0690eaa802dc72c4a6961f166289812dac259f681b77a39db20b28c` |
| gh | 1 | `6960122e156cfbdd511c417443334a0f3193c5f7fa61e21f725df12f6a57c232` | `sha256:083772e48637c9b6c20d769084fd37b53775ad80a051c6963fc6ce61ef60c24e` |
| validation | 0 | `eebf5d792dea6b93a8ae45950957ba748332b7307bb8841bf91e570e5a5b4147` | `sha256:099f3eebdbfde4ae22ef31aeaa95263e4107c9e67659feb6ed2b958c70c58faa` |

The unchanged pinned base layer precedes these 13 recipe layers. `image.lock.json` in this packet is the generated lock; `sources.lock.json` remains in the repository. Large artifacts are retained only in scratch storage; file receipts record their SHA-256 and size.

## Builds and identity proof

- candidate-a: 456784 ms, 3931041388 bytes, manifest `sha256:8cc05a5c51aa04a23063c5d0593065912845a4ba4ce5a5dfd3ff53b12ccd1d19`.
- candidate-b: 404539 ms, 3931041388 bytes, manifest `sha256:8cc05a5c51aa04a23063c5d0593065912845a4ba4ce5a5dfd3ff53b12ccd1d19`.

Two no-cache builds are accepted only when cold-comparison.json records identical authenticated manifest, configuration, compressed layers and uncompressed layer identities. Source download cache reuse is checksum-verified. Build times measure the foreground build invocation; source staging, archive export, privacy and smoke are separate. Cross-host reproducibility is not claimed.

## Versions and image smoke

The smoke runs inside the image with networking disabled. Every installed package is checked against its pin. Binary versions below come from each executable's own output, rather than inferring the version from the lock.

| Command | Observed first line |
|---|---|
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
| `sudo --version` | sudo: unable to resolve host 4cf7e1f13989: Temporary failure in name resolution |
| `docker --version` | Docker version 28.0.4, build b8034c0 |
| `gcc --version` | gcc (Ubuntu 13.3.0-6ubuntu2~24.04.1) 13.3.0 |
| `g++ --version` | g++ (Ubuntu 13.3.0-6ubuntu2~24.04.1) 13.3.0 |
| `clang --version` | Ubuntu clang version 18.1.3 (1ubuntu1) |
| `gcov --version` | gcov (Ubuntu 13.3.0-6ubuntu2~24.04.1) 13.3.0 |
| `cmake --version` | cmake version 3.28.3 |
| `git --version` | git version 2.43.0 |
| `make --version` | GNU Make 4.3 |
| `autoconf --version` | autoconf (GNU Autoconf) 2.71 |
| `flex --version` | flex 2.6.4 |
| `bison --version` | bison (GNU Bison) 3.8.2 |
| `automake --version` | automake (GNU automake) 1.16.5 |
| `help2man --version` | GNU help2man 1.49.3 |
| `ninja --version` | 1.11.1 |
| `curl --version` | curl 8.5.0 (x86_64-pc-linux-gnu) libcurl/8.5.0 OpenSSL/3.0.13 zlib/1.3 brotli/1.1.0 zstd/1.5.5 libidn2/2.3.7 libpsl/0.21.2 (+libidn2/2.3.7) libssh/0.10.6/openssl/zlib nghttp2/1.59.0 librtmp/2.3 OpenLDAP/2.6.10 |
| `python3 -m pip --version` | pip 24.0 from /opt/python/lib/python3.12/site-packages/pip (python 3.12) |
| `pkg-config --version` | 1.8.1 |
| `rsvg-convert --version` | rsvg-convert version 2.58.0 |
| `java -version` | openjdk version "17.0.20.1" 2026-08-18 |
| `/opt/tsn-gen/build/traffic-gen/packet_gen --version` | packet_gen 0.1.0 |

Functional smoke: GCC/Clang compile and execute; coverage reaches 100%; GoogleTest/GoogleMock; CMake/Ninja; Autoconf; Flex/Bison; Tcl/Perl; curl and XZ; client help; Node; package consistency; Verilator simulation; converter/Yosys/ABC; RV32 ELF identity; YAML/parser/rendering/diagram/BDD libraries; LiteX; Java/Scala; seeded oracle packet generation. See candidate-smoke.json and its log.

Accepted runner deviations are documented in docs/testing/CI_IMAGE.md and tied to the public round-2 ruling. The independent runner manifest and earlier elaborate log are hashed in runner-version-baseline.json. Docker client 28.0.4 matches that manifest.

## Evidence and remaining work

See the gate receipts in this packet. Historical failed probes remain distinguishable from their passing replacements. Two isolated scratch checkouts prevent fixture collisions. The bounded builder driver invokes unchanged functions in their original order within each group, preserving --require-rv32, and records source hashes, every function and every reported skip.

Full workflow adoption acceptance belongs to lane 737-ci30's switch round under the public ruling. Independent review, hosted evidence, publication and merge are not claimed here.


## Final validation status

REVIEW READY under PR #738 comment 6166238176. The unchanged `sw/builder/test_builder.py:3245` function `test_baremetal_profile_contract` completed with `--require-rv32`, rc 0, in 1,014,708 ms (1014.708 seconds). It ran in the final immutable image as a background job without a timeout. The function itself returned after 1,012,757 ms. The existing `MAKEFLAGS += -e` mutation arm was NOT RUN because this make does not re-read MAKEFLAGS mid-parse; the gate reports that no tool is missing. The compiler-backed census and identity checks ran.

The setup correction restored the exact round-2 HOME mapping. The existing `br-milan-rv32/host` symlink still targets `/opt/rv32-sdk`. Before the campaign, the home-relative compiler printed `riscv32-linux-gcc.br_real (Buildroot 2021.11-18033-g83947c7bb6) 14.3.0` inside the same image, rc 0. `builder-home-preflight.json` records this check. `builder-home-environment-proof.json` proves every explicit environment variable, mount, working directory and network setting matches the original group-1 invocation. Network access remained disabled. The image reference is immutable, pulling is disabled, and the container has an 8 GiB memory limit and four-CPU limit.

`builder-home-tree-comparison.json` records equality for all 1,338 tracked superproject paths between the existing validation tree and the unchanged lane checkout. `builder-home-background.receipt.json` records the complete command, image manifest, timestamps, wall time, source digest and scratch artifact sizes/hashes. `builder-functions-1.json` records the completed function and its explicit inert-mutation skip. The full raw log stays in scratch.

The previous 3,302 ms prerequisite failure and 580-second/590-second timeouts remain historical evidence. The corrected run supplies the previously missing compiler-backed verdict. The two identical cold image builds stand unchanged.

All 103 function invocations returned across nine groups, each command rc 0, including elaboration of every shipped recipe. The existing `mf48` resource-calibration arm remains NOT RUN: it requires a Vivado build tree, and hosted CI takes the same skip, as confirmed by the public ruling. No Vivado, hardware or bench run was performed. `builder-validation.json` records the coverage, grouped-execution limitation, historical attempts and both explicit skips. A completed monolithic builder invocation is not claimed.

The separate intentional compiler-absent run exited 0 after 531,540 ms, with its two explicit NOT RUN arms. It remains evidence for absent-compiler behavior; the corrected compiler-backed run independently supplies the required verdict.

| Evidence | Result and scope |
|---|---|
| `builder-home-preflight.json` | Home-relative compiler resolves inside the final image and prints GCC 14.3.0; rc 0. |
| `builder-home-background.receipt.json` | Corrected background invocation without timeout: rc 0 in 1,014,708 ms; required compiler-backed function completed; inert MAKEFLAGS mutation explicitly skipped. |
| `builder-background.receipt.json` | Historical setup failure: rc 1 in 3,302 ms before the compiler campaign. Superseded by the corrected run. |
| `cold-comparison.json` | Both cold builds have identical authenticated manifest, config, 14 compressed layers and 14 uncompressed layer identities. |
| `second-export-verification.json` | Final-head lock verified against the second exported archive, rc 0. |
| `candidate-privacy.json` | All 14 layers scanned; 526 authenticated upstream allowances; zero unmatched findings and zero first-party allowances. |
| `candidate-smoke.json` | Final image offline binary-version and functional smoke, rc 0; 29,038 ms. |
| `cpu-tree-proof.json` | Final immutable image matches all 4,550 expected files/links across six pinned repositories; zero missing, extra or changed entries. |
| `oracle-data-invariance.json` | All 37 protocol documents retain identical parsed data; seeded packet output unchanged. |
| `java-store.json` | Actual `keytool -list -cacerts -storepass changeit` accepts the normalized truststore, rc 0. |
| `runtime-fix.json` | Twelve final-code checks, all rc 0: inventory, build/integrity/privacy controls, Python idiom, package regeneration, baremetal check and 738 refusal controls, docs and diff checks. |
| `pin-regeneration.json`, `maven-check.json` | Base/recursive source and Maven closure generators/checks exit 0; no handwritten generated-file changes. |
| `source-doc-gates.json` | Evidence-reader and source-list checks plus their controls pass. The three earlier documentation failures are superseded by `final-docs.json`. |
| `final-docs.json` | Eight final-image commands exit 0: docs consistency, paths/style, contents/anchors, em-dash check, HDL reference generation and compiler-gate selftest. |
| `documentation-validation.json` | Every one of 76 extracted docs-check Python commands has a passing invocation; 65 initial successes plus 11 passing replacements. Receipts identify their actual images; these are not all final-image runs. |
| `client-dependency.json` | Ordinary and isolated offline runner selftests pass in disposable containers with the pinned client. No candidate runner was used as a host orchestrator. |
| `docs-fixtures-retry.json` | Eight fixture/documentation commands pass, including `make -C gptp-processor docs`. |
| `final-tree-check.json` | Seven new one-line commits; clean checkout including ignored files; workflow, HDL, firmware, linked-image patch and submodule paths unchanged from base. |
| `final-memory.json` | Prior round-2 peak 5,451,419,648 bytes, below the 9 GB working limit. |
| `builder-home-final-check.json` | Current continuation: clean unchanged head; 103 unique functions returned; two explicit skipped arms; service peak 615,067,648 bytes; no final-image container remains running. |

Historical probes and prior STOP drafts remain for provenance. `HANDOFF.md`, `PR-BODY.md`, `REVIEW-READY-HOME.md`, `builder-validation.json`, `builder-home-background.receipt.json` and `final-evidence-manifest.json` define the current packet. Large exports, logs and reports remain in scratch; receipts record their size and SHA-256. No source change, new commit, push or PR modification was performed in this continuation.

## Documentation gate command ledger

Commands are shown as plain shell. `evidence/` is an output directory outside the checkout. Each row names the passing receipt and its zero-based record; image identity and full invocation are in that receipt. These invocations supplement the completed compiler-backed builder gate. Full workflow-adoption acceptance remains assigned to the switch lane.

| Command | Passing receipt / record | rc |
|---|---|---|
| `python3 scripts/gen_hdl_reference.py --selftest` | `docs-image-gates.json` / 0 | 0 |
| `python3 scripts/gen_hdl_reference.py --output evidence/hdl-reference` | `final-docs.json` / 6 | 0 |
| `python3 scripts/docs_check.py` | `docs-image-gates.json` / 2 | 0 |
| `python3 scripts/check_em_dash.py --base fa7347fc` | `docs-image-gates.json` / 3 | 0 |
| `python3 scripts/check_doc_style.py` | `docs-image-gates.json` / 4 | 0 |
| `python3 scripts/check_doc_style.py --selftest` | `docs-image-gates.json` / 5 | 0 |
| `python3 scripts/check_gptp_docs.py` | `docs-image-gates.json` / 6 | 0 |
| `python3 scripts/check_gptp_docs.py --selftest` | `docs-image-gates.json` / 7 | 0 |
| `python3 docs/DOC_MAP.gen.py --check` | `docs-image-gates.json` / 8 | 0 |
| `python3 docs/DOC_MAP.gen.py --selftest` | `docs-image-gates.json` / 9 | 0 |
| `python3 docs/diagrams/timesync_chain.gen.py --check` | `docs-image-gates.json` / 10 | 0 |
| `python3 docs/diagrams/timesync_chain.gen.py --selftest` | `docs-image-gates.json` / 11 | 0 |
| `python3 scripts/check_solution_docs.py` | `docs-image-gates.json` / 12 | 0 |
| `python3 scripts/check_solution_docs.py --selftest` | `docs-image-gates.json` / 13 | 0 |
| `python3 docs/diagrams/submodule_boundaries.gen.py --check` | `docs-image-gates.json` / 14 | 0 |
| `python3 docs/diagrams/submodule_boundaries.gen.py --selftest` | `docs-image-gates.json` / 15 | 0 |
| `python3 scripts/check_submodule_docs.py` | `docs-image-gates.json` / 16 | 0 |
| `python3 scripts/check_submodule_docs.py --selftest` | `docs-image-gates.json` / 17 | 0 |
| `python3 scripts/gen_wavedrom.py --selftest` | `docs-image-gates.json` / 18 | 0 |
| `python3 scripts/gen_wavedrom.py docs/diagrams/wd_axis_backpressure.json --background=white --check` | `docs-image-gates.json` / 19 | 0 |
| `python3 scripts/gen_wavedrom.py docs/diagrams/wd_cdc_handshake.json --background=white --check` | `docs-image-gates.json` / 20 | 0 |
| `python3 scripts/gen_wavedrom.py docs/diagrams/wd_gptp_pdelay.json --background=white --check` | `docs-image-gates.json` / 21 | 0 |
| `python3 scripts/check_diagram_pngs.py` | `docs-image-gates.json` / 22 | 0 |
| `python3 scripts/check_diagram_pngs.py --selftest` | `docs-image-gates.json` / 23 | 0 |
| `python3 scripts/check_feature_status.py --self-test` | `docs-image-gates.json` / 24 | 0 |
| `python3 docs/traceability/gen_module_matrix.py --check` | `docs-image-gates.json` / 25 | 0 |
| `python3 scripts/check_gptp_docs.py --with-submodule` | `docs-image-gates.json` / 26 | 0 |
| `python3 scripts/measure_control_flow.py --selftest` | `docs-image-gates.json` / 27 | 0 |
| `python3 scripts/measure_cohesion.py --selftest` | `docs-image-gates.json` / 28 | 0 |
| `python3 scripts/check_baremetal_only.py --check` | `docs-image-gates.json` / 29 | 0 |
| `python3 scripts/check_baremetal_only.py --selftest` | `docs-image-gates.json` / 30 | 0 |
| `python3 scripts/ci_rv32_sdk_selftest.py` | `docs-image-gates.json` / 31 | 0 |
| `python3 sw/builder/test_firmware_compiler.py --selftest` | `final-docs.json` / 7 | 0 |
| `python3 sw/builder/test_firmware_compiler.py --absent --audit evidence/rv32-absent.jsonl` | `docs-absent-retry.json` / 0 | 0 |
| `python3 scripts/check_nvm_record_space.py` | `docs-fixtures-retry.json` / 0 | 0 |
| `python3 scripts/check_nvm_record_space.py --self-test` | `docs-fixtures-retry.json` / 1 | 0 |
| `python3 scripts/check_nvm_capture.py` | `docs-fixtures-retry.json` / 2 | 0 |
| `python3 sw/firmware/nvm_hosttest/test_nvm_firmware.py --self-test` | `docs-fixtures-retry.json` / 3 | 0 |
| `python3 scripts/check_soc_sources.py` | `docs-image-gates.json` / 38 | 0 |
| `python3 scripts/check_soc_sources.py --selftest` | `docs-image-gates.json` / 39 | 0 |
| `python3 sw/litex/iob_pack_selftest.py` | `docs-image-gates.json` / 40 | 0 |
| `python3 scripts/check_rtl_source_lists.py` | `docs-image-gates.json` / 41 | 0 |
| `python3 scripts/check_rtl_source_lists.py --selftest` | `docs-fixtures-retry.json` / 4 | 0 |
| `python3 scripts/measure_naming.py --check` | `docs-image-gates.json` / 43 | 0 |
| `python3 scripts/measure_naming.py --selftest` | `docs-image-gates.json` / 44 | 0 |
| `python3 scripts/check_port_contracts.py` | `docs-image-gates.json` / 45 | 0 |
| `python3 scripts/check_port_contracts.py --selftest` | `docs-image-gates.json` / 46 | 0 |
| `python3 scripts/measure_fail_fast.py --check` | `docs-image-gates.json` / 47 | 0 |
| `python3 scripts/measure_fail_fast.py --selftest` | `docs-image-gates.json` / 48 | 0 |
| `python3 scripts/check_todo_ownership.py` | `docs-image-gates.json` / 49 | 0 |
| `python3 scripts/check_todo_ownership.py --selftest` | `docs-image-gates.json` / 50 | 0 |
| `python3 scripts/measure_test_evidence.py --check` | `docs-image-gates.json` / 51 | 0 |
| `python3 scripts/measure_test_evidence.py --selftest` | `docs-image-gates.json` / 52 | 0 |
| `python3 scripts/check_hygiene.py --check` | `docs-image-gates.json` / 53 | 0 |
| `python3 scripts/check_hygiene.py --selftest` | `docs-image-gates.json` / 54 | 0 |
| `python3 scripts/check_sv_idiom.py` | `docs-image-gates.json` / 55 | 0 |
| `python3 scripts/check_sv_idiom.py --selftest` | `docs-image-gates.json` / 56 | 0 |
| `python3 scripts/check_cpp_idiom.py` | `docs-image-gates.json` / 57 | 0 |
| `python3 scripts/check_cpp_idiom.py --selftest` | `docs-image-gates.json` / 58 | 0 |
| `python3 scripts/check_py_idiom.py` | `docs-image-gates.json` / 59 | 0 |
| `python3 scripts/check_py_idiom.py --selftest` | `docs-image-gates.json` / 60 | 0 |
| `python3 scripts/check_sh_idiom.py` | `docs-image-gates.json` / 61 | 0 |
| `python3 scripts/check_sh_idiom.py --selftest` | `docs-image-gates.json` / 62 | 0 |
| `python3 scripts/ci_events.py --check` | `docs-image-gates.json` / 63 | 0 |
| `python3 scripts/ci_events.py --selftest` | `docs-image-gates.json` / 64 | 0 |
| `python3 scripts/act_ci.py --selftest` | `client-dependency.json` / 0 | 0 |
| `python3 scripts/check_doc_paths.py` | `docs-image-gates.json` / 66 | 0 |
| `python3 scripts/check_archive.py` | `docs-image-gates.json` / 67 | 0 |
| `python3 scripts/check_archive.py --selftest` | `docs-image-gates.json` / 68 | 0 |
| `python3 scripts/gen_toc.py --selftest` | `docs-image-gates.json` / 69 | 0 |
| `python3 scripts/gen_toc.py --verify-anchors` | `docs-image-gates.json` / 70 | 0 |
| `python3 scripts/gen_toc.py --check` | `docs-image-gates.json` / 71 | 0 |
| `python3 avdecc/gen_aem_store.py --self-test` | `docs-image-gates.json` / 72 | 0 |
| `python3 scripts/check_sweep_shape.py --self-test` | `docs-fixtures-retry.json` / 5 | 0 |
| `python3 scripts/check_deploy_shape.py --self-test` | `docs-image-gates.json` / 74 | 0 |
| `python3 scripts/check_entity_shape.py --self-test` | `docs-fixtures-retry.json` / 6 | 0 |
