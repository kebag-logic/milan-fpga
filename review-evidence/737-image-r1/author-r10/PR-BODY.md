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
- **[Round 9](#round-9)** - Interpreter text that fails closed, and provenance by the image file's identity.
- **[Round 10](#round-10)** - The merged `dev`, its inventory, lock and traced population.

## Status

Round-ten local validation passes at the committed head `d7cb1f90a`, which merges `dev` `4a9b5a2a`. Every reached docs, elaboration and rtl-fast step runs clean under the execution audit in the image: 195 of 230 traced, and the other 35 are orchestration or replaced builds. 224/224 differential fixtures meet their expectation, the audit's 76 controls pass, and all 26 final checks return zero. Both round-nine reviews are POSITIVE at `6f86eee6`; the round-ten merge-and-regeneration re-review is required. `737-ci-image` -> `dev`.
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
- Round-ten assignment 6208056999; reviews R638-9 (6207639165) and R639-9 (6207314215).
- Round-nine assignment 6204018211; reviews R638-8 (6204009418) and R639-8 (6203890877).
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
git switch --detach d7cb1f90af1b8c2f115f58281991f1c9626447f9
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
python3 scripts/check_em_dash.py --base 4a9b5a2a
python3 scripts/gen_toc.py --check
python3 ci/image/build.py --work "$IMAGE_WORK/first" --no-cache --defer-lock
python3 ci/image/build.py --work "$IMAGE_WORK/first" --check-lock --verify-archive "$IMAGE_WORK/first/image.tar"
python3 ci/image/build.py --work "$IMAGE_WORK/second" --no-cache --defer-lock
python3 ci/image/build.py --work "$IMAGE_WORK/second" --check-lock --verify-archive "$IMAGE_WORK/second/image.tar"
python3 ci/image/resolve_packages.py --cache "$IMAGE_WORK/first/context/debs"
docker run --rm --network none --mount "type=bind,src=$IMAGE_WORK,dst=/scratch" sha256:68331c7908fcf2c1c6226c621bcd48287916ff20bac23f1f2b7279dffab94e08 python3 /opt/ci-image/smoke.py --work /scratch/smoke
docker run --rm --network none --user 0:0 --mount "type=bind,src=$PWD,dst=/work,readonly" --workdir /work sha256:68331c7908fcf2c1c6226c621bcd48287916ff20bac23f1f2b7279dffab94e08 python3 ci/image/exec_audit.py --selftest
docker run --rm --network none --user 0:0 --mount "type=bind,src=$PWD,dst=/work,readonly" --mount "type=bind,src=$IMAGE_WORK,dst=/out" --mount "type=bind,src=$CI_IMAGE_SHFMT,dst=/shfmt,readonly" -e CI_IMAGE_SHFMT=/shfmt --workdir /work sha256:68331c7908fcf2c1c6226c621bcd48287916ff20bac23f1f2b7279dffab94e08 python3 scripts/ci_differential.py --run --image sha256:68331c7908fcf2c1c6226c621bcd48287916ff20bac23f1f2b7279dffab94e08 --receipt /out/receipt.json
```

Expected: every command exits zero; both exports match the committed manifest, config and all 14 layer identities; the differential run's receipt equals `ci/image/differential-receipt.json` in its 224 outcomes; the audit passes its 76 controls. The image smoke uses the image's default user. The traced population commands are in the image guide's execution audit section. Package regeneration requires `dpkg` and `dpkg-deb`; it was verified inside the image with the repository and package cache mounted read-only.

Manifest: `sha256:68331c7908fcf2c1c6226c621bcd48287916ff20bac23f1f2b7279dffab94e08`. Config: `sha256:772f24cefe10c87f577e91f50bbc42541e5ef0473721aa3e8a857c3e53853555`. Recipe: `712f7b38fde7d2c1fc61de98c99f697a1b356c1c194dad2a632972c4220f21ac`. Size: 3,930,754,018 bytes. Round-ten cold Docker builds for this recipe: 353,518 ms and 386,192 ms (and 434,076 ms and 419,175 ms for the earlier recipe `a8e55b00…`, the same image). Offline smoke: rc 0 across all 97 records, `PASS: all image tool families`.

The round-ten exports differ from round nine's in two layers. The Python layer holds PyYAML 6.0.2, the version the merged CI constraints file pins, in place of 6.0.3. The validation layer holds the merged walker and audit. The LiteX and oracle layers change only their recipe digest; their content is identical. Round nine's exports authenticated against the same manifest, config and layers as rounds seven and eight. Round seven's image added GNU time to the round-six image. The round-five image receipts remain as history. Setup failures and preliminary builds are retained and explicitly superseded in `HANDOFF.md`.

## Known limitations / out of scope

- Declared runtime-assembled commands remain a located manual residue checklist. Literal evaluation and unsupported interpreter forms are refused.
- The audit's guards are closed by construction for the stated threat model, accidental drift in reviewed source. Deliberately evasive code in committed workflows or scripts is a code-review matter; the remaining named boundaries are listed under Rounds 8 and 9 and in the image guide.
- The committed population receipt is traced at its parent commit `54fbcba6a`, which a receipt cannot name about itself; the receipt commit changes only the receipt.
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
| Inline and streamed programs (superseded in Round 9) | `python3`, `bash`, Perl, Node and Tcl programs by exact text digest in `inline_programs`, the step's own text, or a checkout file; `dash` runs nothing in-process and is judged by its execs | local-wheel installs by `python3 -c` and by `python3 -` from a pipe; an unpinned `bash -c` |
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

## Round 9

Both round-eight reviews found two guards that were not closed by construction.
Inline and streamed Perl and Node text, and Tcl run as `tclsh8.6`, could pass
without a digest. Program provenance was decided by name and by directory. Round
nine closes both on the bytes and on fail-closed text, and takes the other
round-eight items.

| Item | Closed by | Refused control |
|---|---|---|
| Interpreter text (N1, F1) | Every image interpreter, under every installed spelling, reads its program as the interpreter does. Perl bundles switches and joins each `-e`; Node's last program wins; `tclsh` takes a first word without `-` as its script, otherwise stdin. Inline and streamed text needs the step's own text or a reviewed entry of that interpreter. Unreadable text and unmodelled options are refused by name | unlisted `perl -e`, `perl -le`, `perl -wE`, `perl -l012e … -e …`, `node -e`, `node --eval=…`, `node -p -e`, `printf … \| tclsh` and `\| tclsh8.6`, each refused with the digest of the text the interpreter runs; `perl -M`, `-x`, `node -r`, `-i`, shell `-i`, `--login`, Python `-i`; a socket stream |
| Provenance (N2) | A program is the image's own only if its path is in the snapshot of the image's directories taken before any job, with an unchanged key. An interpreter is an image program whose file the image names for its family, or that holds such a file's bytes. The `dash` exemption belongs to the image's `dash` file. Every other program needs a traced build output's bytes or the reviewed generated list | an appended copy installed as `/usr/local/bin/cp`; an appended copy named `python3` given a checkout script; `bash` copied to a job path named `dash` running `-c`; `perl5.38.2` as an unlisted spelling |
| Loader errors (F2) | The load's own errno or reason is answered, the target kept apart; an exec the audit cannot judge is refused, never left unanswered. A text file without `#!` that the image's `bash` runs in-process is judged as a bash script | a job-written file without `#!` run by `bash`; `#!/proc/self/exe` refused with its own reason; a missing `#!` interpreter and a binary file run nothing |
| Accepted sources (N3) | File program: an image file present before the job and unchanged, named in `scripts`; a checkout file unchanged since the job started, or a byte copy of one; a job-written copy of an image executable, judged as that file by its name; the step's own text; a reviewed `generated_programs` entry of its interpreter. Inline or streamed program: the step's own text, or a reviewed `inline_programs` entry of its interpreter, by its masked digest. The image's own `dash` file is judged by its execs; `bash < checkout file` is refused as built. The self-test's own reviewed entries live in the self-test; the production `checkout_writes` holds one entry | — |
| `realpath` (N4) | `$(realpath <literal>)` yields a path only for the running script's own unlinked path, its directory or an ancestor, before the script runs a command; elsewhere it is runtime | `bash-realpath-after-a-program`: an earlier program re-points a link; refused |
| Residue (R1, R2) | The fixture comment reads "Probes for workflow environment names, checkout state and local declarations". The guide names the notify-then-lookup limit | — |

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

Every reached step was traced again in the image, with the network disabled, at
`84caae9af`. 94 of 98 steps were traced, every exit status was 0, there was no
finding, there were 183,831 exec instances, and all 115 round-six gate commands
were observed. The other 4 remain the cache-miss builds the image's layers
replace. Against the round-eight receipt, 555 rows are relabelled from `named`
to `image`, and the three `tclsh8.6` program rows become the Tcl scripts and
streams they run. Every one of the 103 inline or streamed and 450 generated
reviewed entries is used. The 45 tool records and 303 residue lines are
unchanged. 213 differential fixtures meet their expectation over 178 census
shapes, and the audit passes 74 controls in the image. Two cold builds reproduce
the same image, and the lock binds recipe `53fb5abd…`. All 26 final checks
return zero at `6f86eee60`, with the inventory `--check` last. Independent
re-review and the reviewer-owned coverage ledger are required.


## Round 10

Both round-nine reviews are POSITIVE at `6f86eee6`. Round ten merges `dev`
`4a9b5a2a` (#739's split workflows, #745's memory-bounded census, #749's
job-private elaboration interpreter) and regenerates every record through its
generator. No workflow changed. Each guard that refused a merged form was
extended, with a differential fixture for each new shape.

| Item | Change | Evidence |
|---|---|---|
| Merge | `03dcd0c36`, a merge commit. One conflict: both sides added an arm function at the same place in `scripts/check_baremetal_only.py`; both are kept | bare-metal check and self-test (867 arms) |
| Readers | `PIP_CONSTRAINT` read exactly: a checkout file whose every line is an exact archive URL with its `sha256`; an unpinned request takes its pin and digest. `apt-get -o Dir::Cache::archives=…`, `scripts/ci_install_cache.py` and `python3 -m venv DIR` are modelled; any other option refuses by name | inventory self-tests; 46 records |
| Make and shell | `-` in names, `\#`, quoted runtime job counts, unassigned runtime environment values, computed names, `foreach`, whole-line `eval`, `or`, static pattern rules; `[[ ]]`, ternary and grouped arithmetic, `%` removal, `-lt` | 224 of 224 differential fixtures, 185 census shapes, measured in the locked image |
| Image | PyYAML 6.0.2, the constraints file's pin, replaces 6.0.3 in the Python layer | two cold builds per recipe; manifest `68331c79…`, recipe `712f7b38…` |
| Audit | `python3 --version`/`-V` and `node --version`/`-v`, exactly, are runs of the image interpreter | 76 controls in the image |
| Reviewed programs | 26 inline and 15 generated entries for the merged workflows' new programs; 21 and 4 that no traced step runs any more are removed | lists hold 108 and 461 |
| Population | The docs gate legs and union, every rtl-fast job, and the elaboration legs and union, with runner `steps`, `needs` and `job.status` values and artifacts between jobs. A merge keeps each step's row from the run that selected its job | see below |
| Residue | R638-9-R3: the Round 9 row text above is the reviewer's. R638-9-R2: the reviewer's line is in the guide's boundary list | `docs/testing/CI_IMAGE.md:107-108` |

Decision points, published for the reviewers and the manager:

1. **Guards, never workflows.** Every refusal the merged workflows raised was answered in the reader, the census or the reviewed lists. The new census shapes each entered with a passing focus fixture.
2. **Reviewed scope texts.** The scope history self-test runs the shipping scope step of each workflow, and planted mutations of it, in a fixture repository. Each entry names the generated workflow it reads, not the `.github/ci-templates/` file it is generated from. The removed entries said "as committed at a historical revision"; the new ones state what the self-test runs.
3. **Elaboration in the population.** The elaboration legs are traced for the first time. Their job-private environment step runs in its image form, `import litex, migen, yaml`. The LiteX patch series runs as committed, as root. Two elaboration arms report NOT RUN for recorded reasons: the inert `MAKEFLAGS += -e` mutation and the mf48 calibration report. Both are the known limitations above.
4. **Base commit.** The trace uses `--base fa7347fc`, the lane's fork point, as before. Every diff-scoped gate sees a superset of this PR's diff against `4a9b5a2a`, and the scope steps classify the head as RTL-relevant, so no reached step is skipped.
5. **Receipt image.** The differential receipt was first measured in the round-nine image, because the recipe binds the inventory and the inventory binds the receipt. The image's content does not depend on either. So the receipt was measured again in the locked image, with the same 224 outcomes. The recipe digest changed with the inventory's input digest, and two more cold builds reproduced the same image.
6. **Merge defect.** The first final trace was clean, but its merge refused. An elaboration cache-miss build kept the rtl-fast run's "not selected" row instead of its replacement reason. The fix keeps the selecting run's row. Merging in either order gives the same steps and reasons. That trace is superseded, so the committed receipt is traced at its parent commit.
7. **Orchestration jobs.** `ci-manifest`, `ci-fail-fast` and `ci-cancel-tail` call the GitHub API by design. The reconciliation names their 30 steps, untraced.

Every reached step was traced again in the image, with the network disabled, at
`54fbcba6a`. 195 of 230 steps were traced: 112 docs and elaboration steps as
root, and 83 rtl-fast steps as uid 1000. Every exit status was 0, there was no
finding, there were 320,983 exec instances, and all 115 listed gate commands
were observed. The other 35 are the 30 orchestration steps and the 5 cache-miss
Verilator and Yosys builds the image's layers replace. Every one of the 108
inline or streamed and 461 generated reviewed entries is used, and no other.
224 differential fixtures meet their expectation over 185 census shapes in the
locked image, and the audit passes 76 controls in the image. Two cold builds
per recipe reproduce the same image, and the lock binds recipe `712f7b38…`. The
receipt is committed in `d7cb1f90a`, which changes only the receipt. All 26
final checks return zero there, with the inventory `--check` last. `dev` has
since moved to `1f6f2f57`, changing only documentation and the doc-style gate,
none of it in this PR's files. A read-only merge with it is conflict-free, and
the doc-style gate passes on the result. The round-ten merge-and-regeneration
re-review is required.
