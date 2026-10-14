[A615]

# Image lane handoff

Status: REVIEW READY; implementation and scoped verification complete.
Head: `2b2e4d2c5b7f43cfc9df5347d99f9fee2c1fb895`. Branch: `737-ci-image`.
Base: `fa7347fc59173f90e4feec2df207692e6e6e72ec`.
Assignment: https://github.com/kebag-logic/milan-fpga/issues/737#issuecomment-6160953880.
Executor: [A615]. Internal reviewer: [R638]. External reviewer: [R639].
Origin was confirmed as the assigned public repository before editing. The explicit assignment authorized this lane while the shared issue board remained Backlog.

## Changes

| File:line | Change |
|---|---|
| `scripts/ci_tool_inventory.py:210` | Derive requests from every workflow and recursively inspect literal script references and local imports. |
| `scripts/ci_tool_inventory_selftest.py:12` | Refuse additions, removals, orphan entries, pin drift, unsupported installers and hidden script installs. |
| `ci/image/tool-inventory.json:1` | Generated workflow, job and step provenance for every request. |
| `ci/image/Dockerfile:1` | Digest-pinned base, separate tool stages and offline builds. |
| `ci/image/sources.lock.json:1` | 214 distribution packages and 476 public source artifacts, including 423 Maven artifacts and 28 Python distributions. |
| `ci/image/install.py:29` | Verify every source at the layer boundary; build exact workflow tools and apply the existing patch series. |
| `ci/image/build.py:45` | Check workflow pins, stage a clean allowlisted context, derive the CPU pin, build, tag and generate the image lock. |
| `ci/image/build_selftest.py:28` | Planted wrong versions, hashes, missing tools, duplicate sources, traversal paths, corrupt downloads and wrong derived CPU pin. |
| `ci/image/sbt-repositories:1` | Public repository configuration for the checksum-locked offline Scala cache. |
| `ci/image/smoke.py:25` | Check every package version and exercise each tool family inside the image. |
| `ci/image/image.lock.json:1` | Generated per-layer tool/version/source/recipe digests and final OCI manifest digest. |
| `docs/testing/CI_IMAGE.md:1` | Rebuilding, pin updates, smoke checks and future digest consumption. |
| `docs/README.md:88` | Index the image guide. |

## Derived tool inventory

The table preserves requested pins and every requesting workflow step. Unversioned requests are resolved by the source lock. Runner entries identify runtime uses rather than installation commands. The renderer is the current Python implementation; the retired Node module graph is absent from the workflows.

| Tool | Workflow pin / resolved version | Workflow, job and step |
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

Additional system dependencies include the host C/C++ compilers, build systems, Java runtime and development libraries. Their exact package versions are checked by the smoke test and preserved in the source lock. Node 22.23.3 and GitHub CLI 2.102.0 match the public runner inventory at `ubuntu24/20261004.327`; their official release checksum lists were checked. All 214 distribution archives matched the package repository SHA-256 index.

Only these submodules were initialized: `third_party/tsn-c-stack`, `protocol-processor`, and `gptp-processor`. Their top-level paths and own origins were verified before use. The firmware, source-list and evidence-reader contracts were read. No firmware, linked image, existing test check or workflow changed.

## Dockerfile layer table

| Stage | Installed tool family | Source manifest |
|---|---|---|
| `system-tools` | 211 compiler, runtime and build prerequisite packages | `locked distribution packages excluding GoogleTest` |
| `gtest-tools` | GoogleTest and GoogleMock 1.14.0 | `three locked distribution packages` |
| `python-tools` | CPython 3.12.3 environment and 28 Python distributions | `python.lock.json` |
| `litex-tools` | seven workflow Git pins, CPU sources and existing patches | `litex.lock.json` |
| `verilator-tools` | Verilator 5.050 | `verilator.lock.json` |
| `yosys-tools` | Yosys 0.66, pinned ABC and cxxopts | `yosys.lock.json` |
| `rv32-tools` | RV32 SDK stable-2025.08-1, GCC 14.3.0 | `rv32.lock.json` |
| `sv2v-tools` | sv2v 0.0.12 | `sv2v.lock.json` |
| `sbt-tools` | launcher 1.10.7, project-selected 1.10.0, offline Maven closure | `sbt.lock.json` |
| `oracle-tools` | pinned tsn-gen and recursive parser sources | `oracle.lock.json` |
| `node-tools` | Node 22.23.3 | `node.lock.json` |
| `gh-tools` | GitHub CLI 2.102.0 | `gh.lock.json` |
| `validation-tools` | assembled installed prefixes and smoke checker | `sources.lock.json` |

The per-tool manifests are generated in the build context. A tool pin changes its selected inputs; independent tool stages retain reusable layers. Common prerequisites and installer changes may invalidate multiple stages.

## Lock and measured image

Recipe: `aa3be31ce1924fac59d15ba2992f96561c5d8fb4c307c34b28568eae95b1a5fe`.
Final OCI manifest: `sha256:94128cff4711ebfe6d3c5ac10bf88cdc9bac5caff4f4b28fc873fc83897d8427`.
Local tag: `fpga-validation:aa3be31ce1924fac59d15ba2992f96561c5d8fb4c307c34b28568eae95b1a5fe`.
Platform: `linux/amd64`. Size: **3,989,528,152 bytes**.
The uncached native build took **393.856 seconds**. The final recipe verification rebuild reused those identical image bytes in **2.896 seconds**. Timing excludes input download and verification. Cross-host cold-build byte identity was not tested.

| Artifact | Size | SHA-256 |
|---|---|---|
| `ci/image/sources.lock.json` | 389579 | `b028de67bb45924d328ab45aa1c98619f348b32f70eed8705db2f0d34344a02e` |
| `ci/image/image.lock.json` | 166056 | `150b658fb842e940ce71ae47580f7538fb92f93fc99f206a3ac96c91095a78d0` |
| `ci/image/tool-inventory.json` | 84241 | `075c257a4272f227b659037a72283de67af1fd5168ee195a8b5c0c93eb2532ab` |

`sources.lock.json` exceeds the output-directory limit and remains only in the checkout. The image lock and derived inventory are also copied beside this handoff. No installed packages, toolchains or tree exports are in this directory.

## Versions measured inside the image

| Command or package | Measured version |
|---|---|
| CPython | `3.12.3 (main, Aug 31 2026, 10:18:26) [GCC 13.3.0]` |
| PyYAML | `6.0.3` |
| behave | `1.3.3` |
| certifi | `2026.7.22` |
| cffi | `2.1.1` |
| charset-normalizer | `3.5.2` |
| cmarkgfm | `2025.10.22` |
| colorama | `0.4.6` |
| cucumber-expressions | `20.1.0` |
| cucumber-tag-expressions | `11.0.1` |
| html5lib | `1.1` |
| idna | `3.20` |
| liteiclink | `2025.4` |
| packaging | `26.3` |
| parse | `1.22.3` |
| parse_type | `0.6.6` |
| pycparser | `3.0` |
| pyserial | `3.5` |
| pyslang | `11.0.0` |
| requests | `2.34.2` |
| setuptools | `84.0.0` |
| setuptools_scm | `10.3.4` |
| six | `1.17.0` |
| svgwrite | `1.4.3` |
| urllib3 | `2.8.0` |
| vcs_versioning | `2.6.0` |
| wavedrom | `2.0.3.post3` |
| webencodings | `0.6.1` |
| wheel | `0.48.0` |
| migen | `0.9.2` |
| litex | `2026.4` |
| liteeth | `2026.4` |
| litedram | `2026.4` |
| litespi | `2026.4` |
| litex-boards | `2026.4` |
| pythondata-cpu-vexiiriscv | `1.0.1.post325` |
| `verilator --version` | `Verilator 5.050 2026-07-01 rev vUNKNOWN-built20261014` |
| `yosys -V` | `Yosys 0.66 (git sha1 86f2ddebce7e98ce7cacc27e8a5c14cb53b51b51, g++ 13.3.0-6ubuntu2~24.04.1 -fPIC -O3)` |
| `sv2v --version` | `sv2v v0.0.12` |
| `riscv32-linux-gcc -dumpfullversion` | `14.3.0` |
| `sbt --script-version` | `copying runtime jar...` |
| `node --version` | `v22.23.3` |
| `gh --version` | `gh version 2.102.0 (2026-09-30)` |
| `gcc --version` | `gcc (Ubuntu 13.3.0-6ubuntu2~24.04.1) 13.3.0` |
| `g++ --version` | `g++ (Ubuntu 13.3.0-6ubuntu2~24.04.1) 13.3.0` |
| `clang --version` | `Ubuntu clang version 18.1.3 (1ubuntu1)` |
| `gcov --version` | `gcov (Ubuntu 13.3.0-6ubuntu2~24.04.1) 13.3.0` |
| `cmake --version` | `cmake version 3.28.3` |
| `git --version` | `git version 2.43.0` |
| `make --version` | `GNU Make 4.3` |
| `autoconf --version` | `autoconf (GNU Autoconf) 2.71` |
| `flex --version` | `flex 2.6.4` |
| `bison --version` | `bison (GNU Bison) 3.8.2` |
| `automake --version` | `automake (GNU automake) 1.16.5` |
| `help2man --version` | `GNU help2man 1.49.3` |
| `ninja --version` | `1.11.1` |
| `curl --version` | `curl 8.5.0 (x86_64-pc-linux-gnu) libcurl/8.5.0 OpenSSL/3.0.13 zlib/1.3 brotli/1.1.0 zstd/1.5.5 libidn2/2.3.7 libpsl/0.21.2 (+libidn2/2.3.7) libssh/0.10.6/openssl/zlib nghttp2/1.59.0 librtmp/2.3 OpenLDAP/2.6.10` |
| `python3 -m pip --version` | `pip 24.0 from /opt/python/lib/python3.12/site-packages/pip (python 3.12)` |
| `pkg-config --version` | `1.8.1` |
| `rsvg-convert --version` | `rsvg-convert version 2.58.0` |
| `java -version` | `openjdk version "17.0.20.1" 2026-08-18` |
| `/opt/tsn-gen/build/traffic-gen/packet_gen --version` | `packet_gen 0.1.0` |
| `pkg-config --modversion gtest` | `1.14.0` |

The complete smoke log records all 214 exact package-version comparisons and every subprocess exit code. Native checks compile and run C/C++, GoogleTest/GoogleMock, coverage, Ninja/CMake, Autoconf, Flex and Bison cases; inspect generated manual output; exercise Git, Perl, Tcl, pkg-config, curl, JavaScript and the API command parser. HDL checks simulate an assertion, convert and synthesize logic, invoke ABC, and compile/audit a separate freestanding RV32 ELF. Python checks exercise the Markdown renderer, parser, diagrams, BDD and LiteX imports/conversion. Java and Scala programs run; the oracle emits a seeded protocol packet. All passed without networking.

The pinned VexiiRiscv/SpinalHDL sources also compiled completely with networking disabled in 72 seconds. Compilation emitted upstream warnings and returned 0. This produced no repository firmware or linked image.

## Validation and evidence

Every completed command below returned 0. The repository checks ran with the image CPython 3.12.3 and locked packages. Commands in this section are plain shell; the local Docker access prefix is an execution-environment detail.

```sh
python3 scripts/ci_tool_inventory.py --check
python3 scripts/ci_tool_inventory_selftest.py
python3 ci/image/build_selftest.py
python3 ci/image/build.py --work "$IMAGE_WORK" --check-lock
python3 scripts/docs_check.py
python3 scripts/check_doc_paths.py
python3 scripts/check_doc_style.py
python3 scripts/check_py_idiom.py
python3 scripts/gen_toc.py --check
python3 scripts/gen_toc.py --verify-anchors
python3 scripts/gen_toc.py --selftest
python3 scripts/check_em_dash.py --base fa7347fc
python3 scripts/gen_wavedrom.py --selftest
python3 scripts/gen_wavedrom.py docs/diagrams/wd_axis_backpressure.json --background=white --check
python3 scripts/check_diagram_pngs.py
python3 docs/DOC_MAP.gen.py --check
python3 scripts/gen_hdl_reference.py --selftest
git diff --check
```

The build preparation also removed a planted unlisted context file. The pinned CPU source reader rejected a mismatched derived CPU pin. The final image smoke command is:

```sh
docker run --rm --network none --mount "type=bind,src=$IMAGE_WORK,dst=/scratch" "$IMAGE_REFERENCE" python3 /opt/ci-image/smoke.py --work /scratch/smoke
```

The additional offline source compilation used:

```sh
docker run --rm --network none "$IMAGE_REFERENCE" python3 -c 'from pathlib import Path; import subprocess; import pythondata_cpu_vexiiriscv as p; subprocess.run(["sbt", "--batch", "-J-Xmx2G", "-J-XX:ActiveProcessorCount=4", "compile"], cwd=Path(p.data_location)/"ext/VexiiRiscv", check=True)'
```

Evidence files and their sizes/SHA-256 values are listed in `evidence-manifest.json`. All 13 final repository gate commands returned 0. The final added-line prose gate examined the committed change, with 0 findings.

## Remaining review and integration work

The manager owns publication. Workflow adoption belongs to the separate integration lane. No push, pull-request creation, hosted run, merge, hardware access or flashing occurred. Independent reviews remain pending; this author report is evidence, not a verdict. Full RTL and firmware regression campaigns were not rerun for this image-only lane. Required hosted and merge-result evidence remains part of subsequent PR integration.

The service recorded peak memory of 3,901,345,792 bytes, below the 9 GB working limit. There was one native Verilator build at a time, with make -j8; smoke simulation used two build workers. No Vivado run or lock was used.
