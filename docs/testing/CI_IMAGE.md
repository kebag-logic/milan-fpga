# CI tools image

The image supplies public, pinned validation tools.
Issue #737 owns its recipe and workflow adoption.
This lane supplies the image without changing workflows.

## Contents

- **[Inputs](#inputs)** -- Trace workflow requests to checked public sources.
- **[Accepted version changes](#accepted-version-changes)** -- Compare the image with its previous runner.
- **[Rebuild](#rebuild)** -- Stage verified inputs and build offline.
- **[Identity and layers](#identity-and-layers)** -- Authenticate declarations and exported image bytes separately.
- **[Privacy](#privacy)** -- Authenticate upstream allowances and refuse private content.
- **[Regenerating source closures](#regenerating-source-closures)** -- Reproduce distribution, CPU and Scala dependencies.
- **[Environment](#environment)** -- Document each image default and its consumer.
- **[Smoke checks](#smoke-checks)** -- Exercise every installed tool family offline.
- **[CI and act adoption](#ci-and-act-adoption)** -- Select the published image by digest.

## Inputs

[`tool-inventory.json`](../../ci/image/tool-inventory.json) derives installation requests.
Each entry names its workflow, job and step.
[`ci_tool_inventory.py`](../../scripts/ci_tool_inventory.py) reads every workflow.
It follows executed scripts, local imports and selected Makefile targets.
The suite driver's owned Makefiles are checked too.
[`command-table.json`](../../ci/image/command-table.json) classifies the permitted commands.
Every literal command must have a declared classification.
Unknown names and unclassified subcommands refuse generation.
Installers require an explicit tool and pin reader.
Python subprocess calls include positional and keyword arguments.
Network-using or subprocess-using Python scripts require reviewed declarations.
Non-installing declarations include a reason and content SHA-256.
Installer declarations include their tools, pins and content SHA-256.
Changed declared scripts refuse generation until reviewed again.
Job containers and services record immutable image references.
Moving image tags refuse generation.
Commands assembled at runtime, including string building, `eval`, `getattr`,
and indirect shells, remain outside static analysis and enter the residue checklist.
Changed requests and unused inventory entries fail comparison.

[`sources.lock.json`](../../ci/image/sources.lock.json) resolves those requests.
Every downloaded artifact carries its size and SHA-256.
The base image uses an immutable manifest digest.
Python packages retain the repository's existing hash pins.
Git archives retain the workflows' exact revisions.
The existing LiteX patch series remains unchanged.
The CPU tree includes every recursive upstream gitlink.
Unversioned requests resolve to the source lock's versions.
The Markdown renderer uses Python packages, without Node modules.
JavaScript actions require Node; workflow selection requires GitHub CLI.
Both runtime tools have separate checked release layers.

Scala dependencies include the pinned CPU generator's requirements.
The launcher is 1.10.7; that project selects 1.10.0.
Both versions belong to the same installed toolchain.
Every downloaded JAR and metadata file has its checksum.

## Accepted version changes

The [round-two decision](https://github.com/kebag-logic/milan-fpga/pull/738#issuecomment-6162190578)
accepts these differences from the previous hosted runner.
The [runner manifest](https://github.com/actions/runner-images/blob/ubuntu24/20261004.327/images/ubuntu/Ubuntu2404-Readme.md)
identifies that independent baseline, version `20261004.327.1`.
The image becomes the reference toolset upon adoption.
The switch lane must pass every workflow's suites inside it.

| Tool | Previous runner | Image |
|---|---|---|
| Git | 2.55.0 | 2.43.0 |
| CMake | 3.31.6 | 3.28.3 |
| Ninja | 1.13.2 | 1.11.1 |
| Java | Temurin 17.0.20+1 | Ubuntu OpenJDK 17.0.20.1 |
| CPython | elaborate selected 3.12.15 through `3.12` | 3.12.3 everywhere |

The image's Verilator reports `rev v5.050`.
Its revision no longer depends on the build date.
Node 22.23.3 and GitHub CLI 2.102.0 retain runner parity.
Clang 18.1.3 and system CPython 3.12.3 retain parity too.
Smoke checks compare binaries' version output against locked versions.
Package database comparisons are additional checks.

## Rebuild

Use Linux x86-64, Docker, BuildKit and Python 3.12.
Install Docker buildx v0.38.0 and PyYAML.
Inventory derivation also requires the pinned shfmt Bash parser.
Its version, URL, size and checksum live under `host_tools`.
The source lock records these host prerequisites separately.
It parses shell syntax without executing candidate scripts.
This is a host prerequisite, like buildx.
Use the Docker driver with the containerd image store.
This setup supports local cache export and image inspection.
The build authenticates configuration identity from the exported manifest.
The host privacy reader also needs `zstd`.
Package regeneration needs `dpkg` and `dpkg-deb`.
Git authenticates the committed patch series.
Choose disk storage outside the checkout.
Allow eight compilation workers per native tool stage.

```sh
mkdir -p "$IMAGE_WORK"
export CI_IMAGE_SHFMT="$IMAGE_WORK/shfmt"
python3 ci/image/prepare_parser.py --output "$CI_IMAGE_SHFMT"
base=$(python3 -c 'import json; print(json.load(open("ci/image/sources.lock.json"))["base"])')
docker pull "$base"
docker image save --output "$IMAGE_WORK/base-locked.tar" "$base"
python3 scripts/ci_tool_inventory.py --check
python3 scripts/ci_tool_inventory_selftest.py
python3 ci/image/build_selftest.py
python3 ci/image/integrity_selftest.py
python3 ci/image/privacy_selftest.py
python3 ci/image/privacy_patch_selftest.py
python3 ci/image/build.py --work "$IMAGE_WORK" --prepare-only
python3 ci/image/build.py --work "$IMAGE_WORK" --no-cache --defer-lock
python3 ci/image/build.py --work "$IMAGE_WORK" --record-lock
```

Preparation downloads and verifies every locked artifact.
Existing downloads undergo identical size and hash checks.
Superseded Ubuntu packages fall back to timestamped snapshots.
Retained downloads must match the original size and SHA-256.
Other HTTP failures and corrupt downloads still refuse acceptance.
Simultaneous downloads use separate temporary files.
Only allowlisted recipe files enter the build context.
Build instructions run with networking disabled.
The base export authenticates unchanged distribution files during scanning.
Build logs, receipts and cache exports use `IMAGE_WORK`.
The final receipt records size and build time.
The build never logs in or pushes.
Individual stages accept `--stage`, including `verilator-tools` and `yosys-tools`.

Cold reproducibility requires two `--no-cache` builds.
Preserve each export and receipt before starting another.
Compare manifest, config, compressed layers and uncompressed layer digests.
Cached builds provide no cold-build evidence.
The fixed build epoch is `1791940308`.
The recipe normalizes timestamps, ownership and trust-store entry dates.
It removes bytecode, package logs and transient caches.
Cross-host reproducibility remains unproved until independently measured.

## Identity and layers

The recipe digest covers installers, source pins and validators.
It also covers the patch series and smoke checks.
A changed pin produces a changed recipe digest.
The local image tag contains that digest.

[`image.lock.json`](../../ci/image/image.lock.json) records the measured result.
Schema 2 binds each tool group to one OCI layer.
Each record carries its own recipe and source digests.
Each also carries compressed and uncompressed layer identities.
The manifest and config digests identify the whole image.

| Layer | Contents | Recipe stage |
|---|---|---|
| Base | Pinned distribution filesystem | Pinned base manifest |
| System | Derived packages and their required dependencies | `system-tools` |
| GoogleTest | Test libraries and headers | `gtest-tools` |
| Python | Interpreter environment and locked Python packages | `python-tools` |
| LiteX | Ecosystem packages, recursive CPU sources, existing patches | `litex-tools` |
| Verilator | Pinned simulator | `verilator-tools` |
| Yosys | Pinned synthesis tools and bundled ABC | `yosys-tools` |
| RV32 | Checked SDK | `rv32-tools` |
| sv2v | Checked converter | `sv2v-tools` |
| Scala | Launcher, public artifact cache and bootstrap placements | `sbt-tools` |
| Oracle | Executable, shared libraries, protocol definitions and licence | `oracle-tools` |
| Node | Actions runtime | `node-tools` |
| GitHub CLI | Workflow selector client | `gh-tools` |
| Validation | Smoke program and source declarations | `validation-tools` |

Recipe consistency and artifact authentication are separate operations.
The first command alone leaves image identity unverified.
The second authenticates the export and every privacy allowance.

```sh
python3 ci/image/build.py --work "$IMAGE_WORK" --check-lock
python3 ci/image/build.py --work "$IMAGE_WORK" --check-lock \
  --verify-archive "$IMAGE_WORK/image.tar"
```

Never edit generated image digests manually.
The builder writes the lock only after verification.

## Privacy

[`privacy.json`](../../ci/image/privacy.json) holds the protected classes.
The scanner also reads the builder's account, home and hostname.
It checks contents, member metadata, history, labels and environment.
It refuses private paths, project identities, addresses and credentials.
Reports contain hashes and classifications, never protected matches.

The [privacy ruling](https://github.com/kebag-logic/milan-fpga/pull/738#issuecomment-6162652582)
allows byte-identical members of pinned public upstream archives.
Every allowance records the authenticated source and member hashes.
Embedded wheel members retain their containing package provenance.
First-party sources receive no upstream allowance.
The oracle ships no bytecode or build logs.
Protocol YAML also omits comment-only prose.
Before writing, its parsed data must remain identical.
This removes dotted clause citations resembling private addresses.
Runtime fields and values remain unchanged.

The [patch refinement](https://github.com/kebag-logic/milan-fpga/pull/738#issuecomment-6163057631)
allows exactly reproduced committed patches, with additional conditions.
Every matching line must remain unchanged from upstream.
No added or modified line may match the table.
The proof records patch hashes and upstream line numbers.
A planted identity on a patch-added line refuses acceptance.
Unknown postimages and uncommitted patch changes are refused too.

## Regenerating source closures

Review new commands before adding their table classifications.
Review script changes before updating their content hashes.
Then refresh workflow provenance whenever its inputs change.

```sh
python3 scripts/ci_tool_inventory.py --write
```

Distribution roots combine workflow requests with documented consumers.
[`package_roots.json`](../../ci/image/package_roots.json) names each additional consumer.
The checker refuses absent consumers and unused locked packages.
Dependencies come from checksum-verified package control records.
The pinned base supplies its own installed-package records.

```sh
python3 ci/image/resolve_base.py "$IMAGE_WORK/base-locked.tar"
python3 ci/image/resolve_packages.py --cache "$IMAGE_WORK/context/debs" \
  --snapshot 20261014T000000Z --write
python3 ci/image/resolve_packages.py --cache "$IMAGE_WORK/context/debs"
python3 ci/image/resolve_git.py --cache "$IMAGE_WORK/context"
```

Package regeneration uses the lock's existing candidate archive pool.
Adding packages first requires collecting their public archive records.
Use the distribution's package index and `apt-get --print-uris`.
Record package, exact version, URL, filename, size and SHA-256.
Download each candidate and verify its published size and checksum.
Place those records in a candidate source-lock file.
Pass that file through `--candidates` during regeneration.
The generator verifies candidates before selecting the used closure.
Never resolve moving package indexes during the image build.
Pin the snapshot timestamp when refreshing Ubuntu package records.
Verify every retained artifact before accepting the refreshed lock.
Update `CI_IMAGE_LOCK_LITERALS` in `scripts/check_baremetal_only.py` when versions change.
Its file-specific allowances must match the generated public package literals.
The CPU generator instead follows exact public Git tree objects.
It refuses undeclared gitlinks and verifies archive checksums.

Resolve Scala dependencies in a fresh disposable cache.
Use the pinned launcher and complete patched CPU tree.
Point `COURSIER_CACHE` and `SBT_OPTS` at that cache.
Use [`sbt-repositories`](../../ci/image/sbt-repositories) for public repository selection.
Resolve the CPU project's `update` and `compile` tasks.
Resolve a separate Scala 2.12.18 project with sbt 1.10.7.
The latter supplies the smoke project's bootstrap closure.
Then collect the resulting cache:

```sh
python3 ci/image/resolve_maven.py --cache "$SCALA_CACHE" --write
python3 ci/image/resolve_maven.py --cache "$SCALA_CACHE"
```

The writer redownloads public artifacts before recording their hashes.
It generates both artifact rows and bootstrap placements.
Checks require exact equality with the locked closure.
Rebuild and rerun smoke after every source-lock change.

## Environment

| Variable | Value | Consumer and origin |
|---|---|---|
| `PATH` | Image tool prefixes followed by the base path | Replaces workflow tool-install path exports |
| `LANG`, `LC_ALL` | `C.UTF-8` | Stable command output and Python decoding |
| `DEBIAN_FRONTEND` | `noninteractive` | Distribution package installation |
| `MILAN_RV32_CC` | `/opt/rv32-sdk/bin/riscv32-linux-gcc` | `fw_rv32.py` and control-firmware tests select the compiler |
| `TSN_GEN_ROOT` | `/opt/tsn-gen` | Existing oracle suite's root override |
| `COURSIER_CACHE` | `/opt/sbt/cache/coursier` | Public Scala dependency cache |
| `SBT_OPTS` | Boot, global and Ivy directories under `/opt/sbt/cache`; repository override | Offline Scala bootstrap and pinned public repositories |

The complete values are in [`Dockerfile`](../../ci/image/Dockerfile).
The offline runner self-test requires the Docker client executable.
Its pinned 28.0.4 release matches the recorded runner manifest.
The image contains the client; daemon access belongs to the caller.

No image-level worker limit overrides job concurrency settings.
`SOURCE_DATE_EPOCH` is a build argument, not runtime policy.

## Smoke checks

Run the checks inside the produced image.
Mount writable scratch storage for their temporary builds.
Disable networking to expose missing dependencies.

```sh
mkdir -p "$IMAGE_WORK/smoke"
docker run --rm --network none \
  --mount "type=bind,src=$IMAGE_WORK/smoke,dst=/scratch" \
  "$IMAGE_REFERENCE" python3 /opt/ci-image/smoke.py --work /scratch
```

Checks compile host programs, RV32 code and a simulation.
They exercise synthesis, conversion, unit tests and coverage.
Rendering, protocol generation and Scala compilation run as well.
These checks establish tool availability and basic operation.
Repository suites still establish product correctness.

## CI and act adoption

The manager publishes the reviewed image separately.
Consumers use its manifest digest from the image lock.
Configure the registry repository through `REGISTRY_IMAGE`.

```sh
digest=$(python3 -c 'import json; print(json.load(open("ci/image/image.lock.json"))["image_digest"])')
docker pull "$REGISTRY_IMAGE@$digest"
```

Hosted job containers and act must select that reference.
Their run manifests must record the same image digest.
The complete CPU source tree already exists inside it.
It contains source files, without upstream Git working directories.
Adoption replaces `ci_litex_env.py` placement with its offline `--check`.
The existing patches are already applied in the image.
The census also requires `$HOME/br-milan-rv32/host`.
Its compiler lookup does not consume `MILAN_RV32_CC`.
Adoption must link that location for the actual job user:

```sh
mkdir -p "$HOME/br-milan-rv32"
ln -s /opt/rv32-sdk "$HOME/br-milan-rv32/host"
"$HOME/br-milan-rv32/host/bin/riscv32-linux-gcc" --version
```

Create this link in a fresh job home.
An existing destination must already resolve to `/opt/rv32-sdk`.
The image supplies the SDK at that immutable location.
No download or compiler change is required.

The switch lane must pin CPython to 3.12.3 everywhere.
Every workflow's suites must pass using these accepted versions.
Hosted contexts and independent reviews remain mandatory.
