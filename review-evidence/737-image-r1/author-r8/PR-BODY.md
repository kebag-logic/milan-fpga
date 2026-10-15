[A615]

## Contents

- **[Status](#status)** - Local implementation and validation.
- **[Linked Issue / roles](#linked-issue--roles)** - Public task and reviewers.
- **[Description](#description)** - Image recipe and verification behavior.
- **[Authoritative references](#authoritative-references)** - Public scope decisions.
- **[How to get into the same state](#how-to-get-into-the-same-state)** - Checkout and prerequisites.
- **[How to validate](#how-to-validate)** - Reproduction and expected results.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** - Adoption and evidence boundaries.
- **[Definition of Done](#definition-of-done)** - Remaining merge conditions.
- **[Round 3](#round-3)** - Closed command table and rebuild portability.
- **[Round 4](#round-4)** - Positive forms and scope-correct traversal.
- **[Round 5](#round-5)** - Structural census and full workflow checks.
- **[Round 6](#round-6)** - Exact tool semantics, in-tree imports and the execution audit.
- **[Round 7](#round-7)** - Differentially proven shapes, invocation audit and the traced population.
- **[Round 8](#round-8)** - The threat model, and each guard closed by construction.

## Status

Round-eight local validation passes at the committed head `1c4d722cb`: every reached docs-check (46) and rtl-fast (48) step runs clean under the closed-by-construction execution audit in the image, 211/211 differential fixtures meet their expectation, the audit's 41 controls pass, and all 26 final checks return zero. Independent re-review is required; the previous verdicts remain NEGATIVE. `737-ci-image` -> `dev`.
No push is authorized.

## Linked Issue / roles

Relates to #737. Image implementation for PR #738.

Executor: `[A615]`
Internal cleared-context reviewer: `[R638]`
External reviewer: `[R639]`

## Description

The workflows currently reinstall their toolchains. This adds a pinned prebuilt tool image with a generated installation inventory, separate tool layers, reproducible cold builds and an authenticated image lock.

The inventory now classifies literal commands through a closed table. It follows executed scripts and Makefile targets, refuses unknown commands and changed script declarations, and records digest-pinned job containers and services. Retained package URLs preserve the locked downloads after archive updates. Export authentication binds the manifest, config and every layer, and privacy allowances require exact public-source provenance.

## Authoritative references

- Issue #737 assignment, comment 6160953880.
- Round-eight assignment 6196923564; reviews R638-7 (6196727731) and R639-7 (6196901768).
- Round-seven assignment 6183738772; reviews R638-6 (6183731799) and R639-6 (6183445346).
- Round-six assignment 6177332782; reviews R638-5 (6177303373) and R639-5 (6176507644).
- Round-five assignment 6173370560; reviews R638-4 (6173357081) and R639-4 (6173248621).
- Round-four assignment 6170435035 and amendments 6170543242 and 6170640746.
- Reviews R638-3 (6170421890) and R639-3 (6169543700).
- PR #738 round-three assignment 6167899804 and amendment 6167966247.
- Reviews R638-2 (6167893456) and R639-2 (6166908258).
- Round-two scope/version/literal-mask ruling 6162190578; privacy rulings 6162652582 and 6163057631.
- [Contribution contract](CONTRIBUTING.md), [requirements](REQUIREMENTS.md), [CI workflow policy](docs/testing/CI_WORKFLOWS.md) and [image guide](docs/testing/CI_IMAGE.md).

## How to get into the same state

Use Linux x86-64, Python 3.12 with PyYAML, buildx v0.38.0, the Docker driver with containerd image storage, and the remaining host prerequisites in the image guide. Set `IMAGE_WORK` to persistent writable storage outside the checkout.

```sh
git switch --detach 1c4d722cb1d0279f0ec44b0fbe87c810adfb9267
git submodule update --init protocol-processor gptp-processor third_party/verilog-axis third_party/tsn-c-stack third_party/lwSRP
mkdir -p "$IMAGE_WORK/first" "$IMAGE_WORK/second"
export CI_IMAGE_SHFMT="$IMAGE_WORK/shfmt"
python3 ci/image/prepare_parser.py --output "$CI_IMAGE_SHFMT"
base=$(python3 -c 'import json; print(json.load(open("ci/image/sources.lock.json"))["base"])')
docker pull "$base"
docker image save --output "$IMAGE_WORK/first/base-locked.tar" "$base"
cp "$IMAGE_WORK/first/base-locked.tar" "$IMAGE_WORK/second/base-locked.tar"
```

## How to validate

```sh
python3 scripts/ci_tool_inventory.py --check
python3 scripts/ci_tool_inventory_selftest.py
python3 scripts/ci_inventory_patterns_selftest.py
python3 scripts/ci_inventory_nodes_selftest.py
python3 scripts/ci_inventory_exact_selftest.py
python3 scripts/ci_differential.py --check
python3 scripts/ci_differential_selftest.py
python3 ci/image/build_selftest.py
python3 ci/image/integrity_selftest.py
python3 ci/image/privacy_selftest.py
python3 ci/image/privacy_patch_selftest.py
python3 scripts/check_baremetal_only.py --check
python3 scripts/check_baremetal_only.py --selftest
python3 scripts/check_py_idiom.py
python3 scripts/check_py_idiom.py --selftest
python3 scripts/docs_check.py
python3 scripts/check_doc_style.py
python3 scripts/check_doc_paths.py
python3 scripts/check_em_dash.py --base fa7347fc
python3 scripts/gen_toc.py --check
python3 ci/image/build.py --work "$IMAGE_WORK/first" --no-cache --defer-lock
python3 ci/image/build.py --work "$IMAGE_WORK/first" --check-lock --verify-archive "$IMAGE_WORK/first/image.tar"
python3 ci/image/build.py --work "$IMAGE_WORK/second" --no-cache --defer-lock
python3 ci/image/build.py --work "$IMAGE_WORK/second" --check-lock --verify-archive "$IMAGE_WORK/second/image.tar"
python3 ci/image/resolve_packages.py --cache "$IMAGE_WORK/first/context/debs"
docker run --rm --network none --mount "type=bind,src=$IMAGE_WORK,dst=/scratch" sha256:98a316549753d63e8b4118dc0f85af3e3813d667485817ee96f6dd597ba1c059 python3 /opt/ci-image/smoke.py --work /scratch/smoke
docker run --rm --network none --user 0:0 --mount "type=bind,src=$PWD,dst=/work,readonly" --workdir /work sha256:98a316549753d63e8b4118dc0f85af3e3813d667485817ee96f6dd597ba1c059 python3 ci/image/exec_audit.py --selftest
docker run --rm --network none --user 0:0 --mount "type=bind,src=$PWD,dst=/work,readonly" --mount "type=bind,src=$IMAGE_WORK,dst=/out" --mount "type=bind,src=$CI_IMAGE_SHFMT,dst=/shfmt,readonly" -e CI_IMAGE_SHFMT=/shfmt --workdir /work sha256:98a316549753d63e8b4118dc0f85af3e3813d667485817ee96f6dd597ba1c059 python3 scripts/ci_differential.py --run --image sha256:98a316549753d63e8b4118dc0f85af3e3813d667485817ee96f6dd597ba1c059 --receipt /out/receipt.json
```

Expected: every command exits zero; both exports match the committed manifest, config and all 14 layer identities; the differential run's receipt equals `ci/image/differential-receipt.json` in its 211 outcomes; the audit passes its 41 controls. The image smoke uses the image's default user. The traced population commands are in the image guide's execution audit section. Package regeneration requires `dpkg` and `dpkg-deb`; it was verified inside the image with the repository and package cache mounted read-only.

Manifest: `sha256:98a316549753d63e8b4118dc0f85af3e3813d667485817ee96f6dd597ba1c059`. Config: `sha256:a2c4d52af85bc218ddd2d3958a2283f64ab175ec4254960eba891ae2271df1fd`. Recipe: `4f7a0b3b84da7816d8cb1d21f1d87905c771748127a83820f4b86d727a17dd44`. Size: 3,930,997,226 bytes. Round-eight cold Docker builds: 463,836 ms and 446,068 ms. Offline smoke: rc 0 across 133 version and smoke records.

The two round-eight exports are byte-identical archives (1,135,069,184 bytes), with the same image as round seven; only the lock's recipe digest changed, because the walker it binds changed. Round seven's image added GNU time to the round-six image. The round-five image receipts remain as history. Setup failures and preliminary builds are retained and explicitly superseded in `HANDOFF.md`.

## Known limitations / out of scope

- Declared runtime-assembled commands remain a located manual residue checklist. Literal evaluation and unsupported interpreter forms are refused.
- The audit's guards are closed by construction for the stated threat model, accidental drift in reviewed source. Deliberately evasive code in committed workflows or scripts is a code-review matter; the remaining named boundaries are listed under Round 8.
- The committed population receipt is traced at its parent commit `c2531c634`, which a receipt cannot name about itself; the receipt commit changes only the receipt.
- Reproducibility is measured on one host. Registry publication and round-trip verification are pending.
- The full builder command returns zero and explicitly reports two NOT RUN arms: the inert `MAKEFLAGS += -e` mutation on this Make version, and calibration against the unavailable `mf48` report. Neither arm is claimed as covered. Earlier grouped-builder evidence is historical.
- Workflow adoption and full hosted/act acceptance belong to the switch lane. Independent approval, publication and merge remain outstanding.
- No workflow, HDL, firmware, linked-image patch or product-test assertion changed.

## Definition of Done

- [ ] Linked Issue acceptance criteria are satisfied
- [x] New or changed behavior has self-checking tests
- [ ] Required local verification bar passes
- [ ] Self-test evidence is posted in a PR comment
- [x] No undocumented requirement or interface change remains
- [ ] Internal cleared-context review is positive
- [ ] External review is positive
- [ ] Blocking and major findings are fixed and re-reviewed
- [ ] No review round remains in flight
- [ ] Candidate merge result is validated per [CONTRIBUTING.md](CONTRIBUTING.md)
- [x] Documentation is updated where needed
- [ ] Post-merge containment will be checked before the Issue moves to Done

## Round 3

The amended assignment resolves STOP 6167951082. The table declares 214 command names and 109 content-pinned scripts, including reviewed non-installing scripts with network imports or subprocess calls. Controls cover the reported installation forms, keyword `args=`, a newly introduced command, root scripts, Makefile recipes, changed declarations, missing/orphan entries and job image digests.

All 185 timestamped Ubuntu fallback URLs were fetched and matched their original size and SHA-256. The HTTP-404 fallback and corrupt-download controls pass. Configuration identity is read from the exported manifest, and cold builds run with buildx v0.38.0. Patch self-tests pass without a configured global/system commit identity. A fresh-HOME SDK-link preflight resolves GCC 14.3.0 at the documented census location.

The reviewer-owned coverage ledger and verdicts must be refreshed for this head.

## Round 4

The reached-construct census was committed before implementation.
Positive command forms now include subcommands, arguments and executable paths.
Shell directory scope and Make file/default/pattern selection are explicit.
Python capability detection precedes keyword or alias decoding.
Unsupported forms refuse generation and comparison by name.

All 45 tool records, pins and workflow provenance remain identical.
The traversal now binds 328 inputs and locates all 269 residue entries.
Alternate Makefiles retain the invocation directory; shell functions retain local/global scope.
Literal dollar text cannot match a runtime argument allowance.
The original controls and new generation/comparison controls pass.
All 13 source gates and three Markdown checks pass.
Two cold builds match in manifest, configuration and all 14 layers.
Both exports authenticate against the generated lock.
All ten rebuilt-image checks and the final source gates pass.
The reviewer-owned coverage ledger and verdicts must be refreshed for this head.

## Round 5

The Entity shape and derived-source gates pass with unchanged assertions.
Typed HDL data operands replace copied source lists in the command table.
A structural allowlist now checks shell and Python nodes, operators and builtins.
Sensitive shell assignments and conditional cleanup functions require exact censused nodes.
Sourced scripts retain caller state; both censused function alternatives are inspected.
Make defaults respect exported values, and command-line overrides propagate into recursive invocations.
Local Python package initializers and members are followed before external-import allowances.
Foreign-function capabilities require a reviewed declaration.
Literal dollar text and checkout-prefix collisions cannot hide executable paths.

All 45 tool/pin/provenance records remain identical to the previous accepted inventory.
The reported probes and existing inventory controls pass. Startup-variable controls
also refuse directory-search, interpreter and Make startup overrides; the exact
allocator environment uses retain explicit runtime loader residue.
All 79 docs-check and 36 rtl-fast commands return zero, as does the unchanged
local aggregate. Receipts identify the actual tested ancestors; subsequent
validator and lock changes have fresh affected-check evidence. Product gate
inputs and submodule pins remain unchanged. The builder reports the two
NOT RUN arms listed above. Two sequential cold builds, independent export
authentication, 131 image version/smoke records and both alternate-root
inventory checks pass. The image archives also match byte-for-byte.
The reviewer-owned coverage ledger and both verdicts must be refreshed.

## Round 6

The walker now refuses every construct it does not resolve with the real tool's
exact semantics, and an observed execution audit backs the static inventory.

Every in-tree Python import is followed through a modelled per-process module
search path. Literal path insertions, imported path constants and call-argument
parameters resolve exactly; an unresolved search-path entry opens the path to
every in-tree portion; literal module loaders are followed and a runtime one is
a declared capability. No external-import allowance may name a module the
checkout supplies. The capture harness reached this way is declared, and the 45
tool records are unchanged.

Make lines are read as GNU Make 4.3 reads them. Assignments start in column zero
with a censused operator; indented, double-colon and escaped-end spellings
refuse. A built-in implicit rule that could apply refuses the target unless the
makefile removes the built-in rules. Implicit-rule prerequisites bind with
make's directory-keeping stems. A target-specific value that a command-line name
would override refuses. A recipe runs in make's exact child environment, and the
traversal cache keys on the complete incoming environment and Make state. The
built-in rules and default variables are recorded from the image's own make.

A command substitution resolves to a directory only in the exact shape
`$(cd <literal> && pwd)`, unredirected and non-symlink; any other output is a
runtime value.

The execution audit follows `execve` with `ptrace` and records every program a
step runs with the network disabled. A step is rejected when it runs a program
the allowlist does not name or a package manager. Its controls catch a planted
installer and a planted system program by name; the current-tree receipt shows
the reached offline steps running only allowlisted programs. Wiring it into
every pull request's signed replay is the documented follow-up.

The image guide states the verified RV32 adoption form: the switch lane verifies
at `/opt/rv32-sdk` and uses the home link only for compiler lookup, with the
step and contract change named and backed by a receipt.

Two sequential cold builds produce the recipe `54cd38de`, the unchanged image
`sha256:86d7aa16...`, config `sha256:62b56e1a...`, all 14 layers and
byte-identical archives; only the lock's recipe identity changed. The full
docs-check and rtl-fast step sets run on the committed head. Independent
re-review and the reviewer-owned coverage ledger are required.

## Round 7

Accepted now means differentially proven. Every construct shape the walker
accepts is one of the 177 census shapes the tree applies. Each names a focus
fixture that runs through the walker and through the image's real GNU Make 4.3,
bash 5.2.21, dash or CPython 3.12.3, offline. The two must resolve the same
command, or the walker must refuse it by name. All 188 fixtures, including every
R638-6 and R639-6 probe, meet their expectation. Generation refuses a shape
without a passing fixture and a receipt measured at another walker. The image
gains GNU time, because two reached recipes run it.

Ambiguous state is never a literal. Values that differ between reachable paths
become runtime. A directory that differs is ambiguous, and the next statement
there refuses. A failed `cd` changes nothing: under errexit it ends the shell,
and tests, which suspend errexit, continue where it started. Loops reach a fixed
point, and a certain test takes one branch. A name defined as a function
anywhere in scope is never resolved as a builtin or external. Make conditionals,
`$(call)`, lazy functions, `MAKEFLAGS` and `MAKELEVEL` follow GNU Make exactly.

The audit judges complete invocations. A seccomp notification filter observes
every exec, static binaries included, without ptrace, so sanitizer suites run.
Every instance is kept with its full argument vector. Interpreters are judged by
script, module or inline program. Installers are refused by name, by subcommand,
or as a fetcher-fed interpreter. A non-system program needs provenance from its
traced job: a build output, or a file the job wrote that copies nothing that
existed before. A script must be in the checkout or written by the job; one with
an image executable's bytes is judged as that file, by its name. The 20 controls
include a real local-wheel install, a shebang `apt-get`, a copied unlisted ELF
and a renamed `pip3` copy, each refused by name.

Every reached step is traced in the image with the network disabled. That is
all 46 `docs-check` steps and the run steps of every rtl-fast job, 98 in total.
The committed `ci/image/exec-audit-receipt.json` records 94 traced steps, each
with exit status 0 and no finding. It holds the source and image identity, each
step's invocation population and the digest of its full exec log. The other 4
are the cache-miss Verilator and Yosys builds that the image's layers replace,
each named with its reason. All 115 round-six gate commands are found in their
traced steps; 4 run with the workflow's own `$(nproc)` or base-commit values in
place of the ones the earlier listing set by hand, and the receipt shows both.
The full step sets were traced again at the committed head: all 94 steps clean, with the same population.

The reviewed bare-metal gate declaration is re-pinned (F1). Two sequential
cold builds produce identical layers and byte-identical archives; the lock
authenticates both. The 45 tool records are unchanged. Independent re-review and
the reviewer-owned coverage ledger are required.

## Round 8

The threat model is now stated: the lane guards against accidental drift in
reviewed source, where a step starts to need a tool the image lacks, to fetch,
to install, or to read an unpinned input. Deliberately evasive code in committed
workflows or scripts is a code-review matter. Each guard is closed by
construction, as an allowlist or a check that fails closed, and each has a
control it refuses by name.

| Guard | Closed by | Refused control |
|---|---|---|
| Exec ABI | The filter notifies every call from another architecture and every x32 call; the audit refuses it before it runs | static i386 and x32 trampolines that exec a marker; the marker never runs |
| Exec target | Only a regular file reached by a path runs: the path is resolved component by component and the caller's own view must be the same file | memfd, deleted file and descriptor-link execs of an unlisted copy |
| Inline and streamed programs | `python3`, `bash`, Perl, Node and Tcl programs by exact text digest in `inline_programs`, the step's own text, or a checkout file; `dash` runs nothing in-process and is judged by its execs | local-wheel installs by `python3 -c` and by `python3 -` from a pipe; an unpinned `bash -c` |
| Positive provenance | A program needs the bytes of a successful toolchain invocation's declared output, digested at its exit, or the reviewed `generated_programs`; a job-written interpreter script needs a checkout copy, the step text or `generated_programs` | a copied program with one byte appended; a failed build's declared output; an unpinned job-written script |
| Workflow `env:` | The census's 25 reviewed names; `BASH_FUNC_*` and interpreter hooks refused by name | an exported function, nine hooks and an unmodelled name |
| Walker | `local`/`declare` as bash; nothing decided from checkout state; `$(cd X && pwd)` only where a failed `cd` cannot continue | R639-7-F1 and R638-7-N3b fixtures through the image's bash |
| Checkout | Exec-time digest of every checkout script; any change to a file the walker read is a finding; reviewed `checkout_writes` | a rewritten script, a rewritten sourced file |

The reviewed lists hold 81 inline or streamed programs and 334 generated
programs. Inline and streamed entries keep their exact text, or their exact
difference from the tracked script they vary. Generated entries are the tests'
mutants, stand-ins and staged copies, each naming the test that writes it; their
digest is taken with job-temporary paths masked, which carry no command.

The named, closed boundaries that remain: code an accepted entry program loads
in-process is that program's own behaviour; a named program reading its own
input files (`make`, `yosys`, `sbt`) is judged by name, and any fetch it tries
fails offline; a checkout file changed and restored between two looks is not
reported; runtime assembly in declared scripts stays located residue.

Every reached step was traced again in the image with the network disabled, at
`c2531c634`: 94 of 98 traced, every exit status 0 and no finding, 183,834 exec
instances, and all 115 round-six gate commands observed. The other 4 remain the
cache-miss builds the image's layers replace. The committed receipt records each
step's population with the provenance of every row and the one reviewed checkout
write. The walker's 45 tool records are unchanged; 211 differential fixtures,
including every R638-7 and R639-7 probe, meet their expectation over 178 census
shapes. Two cold builds reproduce the same image and byte-identical archives,
and the lock binds the new recipe. Independent re-review and the reviewer-owned
coverage ledger are required.
