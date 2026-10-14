# CI tools image

The image supplies public, pinned validation tools.
Issue #737 owns its recipe and workflow adoption.
This lane supplies the image without changing workflows.

## Contents

- **[Inputs](#inputs)** -- Trace workflow requests to checked public sources.
- **[Reached construct census](#reached-construct-census)** -- Define supported syntax and refused variants.
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
Commands match complete argument patterns or bounded handlers.
Unknown names, subcommands and argument forms refuse generation.
Installers require an explicit tool and pin reader.
Python capability detection precedes argument decoding.
Literal keyword dictionaries and function aliases remain classified.
Execution-capable or network-using Python scripts require reviewed declarations.
Non-installing declarations include a reason and content SHA-256.
Installer declarations include their tools, pins and content SHA-256.
Changed declared scripts refuse generation until reviewed again.
Job containers and services record immutable image references.
Moving image tags refuse generation.
Runtime assembly in reviewed scripts produces located residue entries.
Shell `eval` and unpinned interpreter programs refuse generation.
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

## Reached construct census

Round five retains the `e6b86814` tool requests.
The census follows scripts, local imports and suite recipes.
The initial census encountered 69 Makefiles and 214 import names.
The generated inventory records every followed input digest.
All 45 tool records retain their original pins and provenance.
The command table records individual permitted argument forms.
This table defines the construct boundary, including refused variants.
Resolution never executes workflow commands or Make shell expressions.

| Construct | Reached example | Resolution and refused variant |
|---|---|---|
| Workflow commands and environment | `.github/workflows/rtl.yml` | Resolve literal environment values; refuse unknown command forms. |
| Workflow working directories | `.github/workflows/rtl-fast.yml` | Step overrides job and workflow defaults; refuse unresolved directories. |
| Actions, containers and services | `.github/workflows/docs.yml` | Classify actions; require image digests; refuse reusable jobs. |
| Shell sequences and pipelines | `.github/workflows/elaborate.yml` | Walk every operand; refuse unclassified commands. |
| Shell redirections and data heredocs | `syn/yosys/run.sh` | Walk substitutions; refuse unpinned interpreter input. |
| Shell literal assignments and arrays | `scripts/run_all_suites.sh` | Retain literals; record runtime values; refuse computed function calls. |
| Shell parameter and arithmetic expansion | `scripts/run_litex_sims.sh` | Walk nested execution; refuse unsupported expansion syntax. |
| Shell command and process substitution | `syn/yosys/malloc.sh` | Walk child scope; refuse unresolved directory changes. |
| Shell directory changes and subshells | `scripts/run_litex_sims.sh` | Preserve child scope; unresolved directories require content-pinned review. |
| Shell blocks and conditionals | `.github/workflows/docs.yml` | Inspect every branch; refuse ambiguous following directories. |
| Shell loops and cases | `sw/litex/patches/apply.sh` | Inspect every body; retain runtime iteration residue. |
| Shell declarations and functions | `scripts/run_all_suites.sh` | Preserve local/global scope and every censused function alternative. |
| Shell sourced files | `syn/yosys/run.sh` | Follow exact censused calls in caller scope; refuse other calls and computed paths. |
| Inline interpreter programs | `.github/workflows/elaborate.yml` | Require interpreter and exact program digest; refuse changed bytes. |
| Command wrappers | `.github/workflows/rtl.yml` | Parse supported options and classify children; refuse unknown options. |
| Make options and variable overrides | `tb/verilator/maap/Makefile` | Keep file selection separate from recipe directory; refuse unsupported options. |
| Make first target and default goal | `tb/verilator/tcam/Makefile` | Use literal default goal; refuse computed goals. |
| Make explicit rules and prerequisites | `tb/verilator/cbs/Makefile` | Traverse selected dependencies; refuse missing targets. |
| Make single-stem pattern rules | `tb/verilator/nvm_backend/Makefile` | Substitute the unique stem; refuse ambiguous patterns. |
| Make variable assignment and expansion | `tb/verilator/milan_dp/Makefile` | Resolve recursive/simple/default/append assignments; refuse unknown functions. |
| Make multiline definitions and calls | `tb/verilator/milan_dp/Makefile` | Expand declared macros and literal call arguments; refuse undefined macros. |
| Make automatic variables | `tb/verilator/nvm_backend/Makefile` | Bind target, prerequisite and stem; refuse directory/file modifiers. |
| Make string and list functions | `tb/verilator/nvm_backend/Makefile` | Resolve `foreach`, `call`, `subst`, `patsubst`, filters and prefixes. |
| Make path and selection functions | `tb/verilator/milan_dp/Makefile` | Resolve `abspath`, `wildcard`, `firstword`, `strip`, `if`, `and`. |
| Make literal shell expressions | `tb/verilator/milan_dp/Makefile` | Classify expanded literal commands; refuse computed executables. |
| Make conditions and errors | `tb/verilator/capture_coherence/Makefile` | Inspect error-only guards; refuse conditional assignments and other directives. |
| Make target-specific variables | `tb/verilator/milan_dp/Makefile` | Inherit literal values into prerequisites; refuse computed values. |
| Make order-only prerequisites | `tb/verilator/mbx/Makefile` | Traverse both classes; exclude order-only entries from automatic variables. |
| Make recursive invocations | `tb/verilator/milan_dp/Makefile` | Inherit command-line overrides; refuse interpreter-selection overrides. |
| Python imports and local modules | `scripts/measure_test_evidence_readers.py` | Follow local files; require declarations for execution/network capabilities. |
| Python positional and keyword calls | `scripts/check_rtl_source_lists.py` | Decode literal argv and keywords; refuse undeclared executors. |
| Python aliases and dynamic calls | `scripts/act_ci.py` | Require content-pinned review; locate undecodable commands as residue. |

[`syntax-census.json`](../../ci/image/syntax-census.json) enumerates accepted syntax nodes.
Its fields include operators, special variables and Python builtins.
Unknown nodes and fields refuse before command classification.
The command table separately bounds executable options and subcommands.
Typed HDL operands accept data paths, never command options.
Source-list contents remain owned by their reached recipes.

Environment-changing forms require exact source-bound syntax declarations.
Directory search and interpreter startup variables are refused unless censused.
Make startup files and flag overrides have the same boundary.
The allocator's existing `LD_PRELOAD` assignments and unsets are censused exactly.
Assignments retain their shell scope and expose loader selection as runtime residue.
That residue does not establish which shared library a runtime path loads.
These cover existing path additions and environment-file writes.
The same boundary limits input-reading builtins and `xargs`.
Literal inline text requires its complete program digest.
Literal marker strings never authorize runtime execution.

Conditional function definitions normally refuse.
Two cleanup definitions are censused in `scripts/run_all_suites.sh`.
Their alternatives survive the conditional merge and both receive inspection.
New conditional definitions require an explicit census decision.
Background statements, alternate workflow shells and interpreter overrides refuse.
Make defaults respect exported environment values and command-line overrides.
Unexported shell assignments remain outside Make's environment.
Local Python packages take precedence over external-import allowances.
Their initializers and selected members receive independent capability checks.
Foreign-function imports require reviewed content declarations.

The tree also pins two additional interpreter forms.
The synthesis driver reads statistics through a Python heredoc.
The render suite selects simulation modes through shell `-c`.
Both programs require exact text digests in the table.
Changed bytes refuse generation.

Runtime fixture commands retain their enclosing Python declaration.
Runtime directories retain their enclosing shell declaration and scope.
Their paths never resolve to unrelated literal source files.
Changing those scripts invalidates the declaration before traversal.
Known external builds bind to recorded installer destinations.
Checkout location never creates an external-build allowance.
Runtime argument slots require expression provenance.
Literal dollar signs and marker text never acquire that provenance.
Double-quoted backslashes follow shell quoting rules.
The reached `awk` programs are exact literal argument entries.
Sourced fragments preserve caller variables, directories and function definitions.
Unfollowed foreign functions remain refused.

Each supported category has accepted and refused controls.
[`ci_inventory_patterns_selftest.py`](../../scripts/ci_inventory_patterns_selftest.py)
exercises both generation and comparison for each fixture.
Unlisted constructs and unlisted command forms refuse generation.
Runtime assembly remains subject to the declared residue boundary.


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
python3 scripts/ci_inventory_patterns_selftest.py
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
