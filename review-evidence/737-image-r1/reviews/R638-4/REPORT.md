[R638] NEGATIVE - exact head e355f789b4f59b86083809299134557ca47bbcfb

# R638-4: internal cleared-context review of PR #738 (issue #737, image lane), round 4

- Reviewer: [R638], internal independent reviewer, round R638-4.
- Exact head `e355f789b4f59b86083809299134557ca47bbcfb`, tree `42f0ade89e45e059ac27a477376ec3f289996e54`. The PR's recorded head equals it.
- Source base `fa7347fc59173f90e4feec2df207692e6e6e72ec`; live dev `113493920448a8fe6cebd7988408f071b99894c8`.
- Full range `fa7347fc..e355f789`: 19 commits, 34 files. Round-4 delta `e6b86814..e355f789`: five commits, 10 files.
- `git diff --quiet fa7347fc HEAD -- .github` is rc 0, so no workflow file changed (ruling d holds).
- Authorities read, in order:
  - AGENTS.md, CONTRIBUTING.md (by reference) and docs/README.md.
  - Issue #737: body, lane assignment 6160953880 and author REVIEW READY 6172213656.
  - PR #738: round-4 rule 6170435035, amendment 6170543242 and standing authority 6170640746; the earlier rulings named in the assignment; review start 6172401779.
  - The diff and history.
  - Public evidence `review-evidence/737-image-r1/author-r4` at `42bb379c`.
- Independence: I applied all five lenses and planted my own probes before reading any prior review. Only then did I read R638-3 (6170421890) and R639-3 (6169543700), to re-run their forms and resolve their findings. I read no private author material, no lane scratchpad, no management checkout and no other round-4 report. The evidence tree's `reviews/` directory was not opened.
- No manager source bank ran at this head, and none is claimed or inferred. Physical calibration is NOT RUN, and field skips are not hardware proof.

## Verdict summary

Round 4 closes every form R638-3 and R639-3 listed. I re-ran all of them as 33 refusal probes plus one digest-recording fixture: every refusal probe is refused by name, and the digest-pinned `container:`/`services:` images are recorded as image tools. R638-3-F2 (`/tmp` location) is closed as specified.

The image side reproduces:

- **Image unchanged since round 3.** Dockerfile, `install.py`, `smoke.py`, `normalize.py` and `sources.lock.json` are unchanged since `e6b86814`. The lock changes only its overall recipe digest, to `e689418b…`, because the walker scripts are recipe inputs.
- **My own cold `--no-cache` build** (buildx v0.38.0, empty client configuration, separate repository name) reproduced the image exactly:
  - manifest `sha256:86d7aa16e7d2464baf8e0d246434982838c8174de8c8fa610608cce5b23b5e6c`;
  - config `sha256:62b56e1ab52dce1a1914e8469429c014e69a465e74e0bdb9a7d8bf4a626b2776`.
  - Only the pinned base step was cached. Both author cold records agree with it.
- **Lock and privacy proof.** `build.py --check-lock --verify-archive` passes against my export and my own `--prepare-only` context, with every one of 666 artifacts re-downloaded and verified.
- **Privacy scan.** My independent scan of all 14 layers, the config, history and Env found no protected identity, host path, account or credential outside an authenticated upstream allowance.
- **Offline smoke.** The smoke run passes offline (rc 0).

Four blocking defects remain, so the verdict is NEGATIVE.

- **R638-4-F1 (BLOCKER).** The round-4 `command-table.json` breaks two existing repository gates at this exact head:
  - the hosted `docs-check` "Entity shape gate";
  - the `verilator-lint` "Prove protocol-processor source lists are derived" step, and with it the `rtl-fast` aggregate.

  Both were green at `e6b86814`, and I reproduced both failures locally.
- **R638-4-F2 (MAJOR).** Five constructs outside the census (seven probes), which select an interpreter or resolve a command name, are accepted silently. Examples: a step `shell:`, `BASH_ENV`, a `GITHUB_PATH` write, `PATH` lookup and Make `SHELL`.
- **R638-4-F3 (MAJOR).** `xargs` in front of an installer, such as `… | xargs python3 -m pip install`, passes with no tool recorded. That is exactly the case the inventory check must fail on.
- **R638-4-F4 (MAJOR).** Six census constructs (ten probes) are resolved with semantics that differ from the real tool's, so the walker classifies a different script or command from the one that runs. They are `source`, `read`/`printf -v`, Make `?=` against the environment, `$(@D)`, recursive-make overrides, and literal `$`/marker text.
- Two MINOR findings: F5, location-dependent normalization, and F6, Python capability gaps.

## Findings

### R638-4-F1 BLOCKER: the round-4 command table breaks two existing CI gates at this exact head

- **Lenses:** Conformance, RTL, Tests.
- **Where:** `ci/image/command-table.json` at these lines:
  - `:5242`: `obj_mclk_aem/endstation_mclk/gen/adp_shape_defaults.svh`;
  - `:6613` and `:6618`: `../../../configs/generated/…/gen/adp_shape_defaults.svh`;
  - `:12450`: `../../../protocol-processor/hdl/acmp/KL_acmp_nvm_shadow.sv`, part of a literal submodule source list.

  None of these strings existed at `e6b86814` (`receipts/hosted-repro/table-content-delta.txt`).
- **Authority:**
  - AGENTS.md §7: the current PR head needs a successful `rtl-fast` verdict, and existing regressions must remain green (§6, `Tests`).
  - The existing gates encode two contracts:
    - `scripts/check_entity_shape.py`: "every shape-header consumer resolves";
    - `scripts/pp_srcs.py`: "A build input names a stale set of submodule sources… Derive the list with this script rather than editing the copy".
- **Evidence:**
  - Hosted runs at this head, snapshot at 16:23Z (`receipts/exact-head-check-runs.tsv`):
    - `docs-check` failed at step "Entity shape gate": `checks: 228 failures: 1`, `RESULT: FAIL`;
    - `verilator-lint` failed at "Prove protocol-processor source lists are derived": `ci/image/command-table.json: names submodule source(s) literally`;
    - `rtl-fast` failed at "Require every applicable fast gate to pass" because `verilator-lint` failed.
  - The same three contexts were green at `e6b86814` (`receipts/hosted-repro/e6b86814-check-runs.tsv`).
  - Local reproduction at this head:
    - `python3 scripts/check_entity_shape.py --self-test` is rc 1, and its only failure names the three `command-table.json` shape-header paths (`receipts/hosted-repro/entity-shape-head.log`);
    - `python3 scripts/pp_srcs.py --check --selftest` is rc 1 for `command-table.json` (`receipts/hosted-repro/pp-srcs-head.log`).
  - The author's validation set (REVIEW READY 6172213656) does not include either gate.
- **Impact:**
  - The PR cannot meet the completion bar while the required fast gates fail because of its own content.
  - The table also copies a protocol-processor source list. A submodule bump that changes that list would make inventory derivation refuse, or would make the table stale. This is the coupling the source-list contract forbids.
- **Required outcome:**
  - The committed table and its walkers satisfy both existing gates as written; the gates are not weakened or bypassed.
  - The submodule source lists and generated shape headers that the reached recipes use are matched without literally restating what those gates require to be derived.
  - The derived inventory still equals the `e6b86814` tools.
- **Verification:**
  - At the corrected head, `python3 scripts/check_entity_shape.py --self-test` and `python3 scripts/pp_srcs.py --check --selftest` are both rc 0.
  - The hosted `docs-check`, `verilator-lint` and `rtl-fast` contexts succeed at that exact head.
  - `ci_tool_inventory.py --check` is rc 0 with an unchanged `tools` list.

### R638-4-F2 MAJOR: constructs outside the census that select an interpreter or resolve command names are accepted silently

- **Lenses:** Conformance, Robustness, Tests, Docs.
- **Where:**
  - `scripts/ci_tool_inventory.py:193-202`: steps are walked as Bash. The step and `defaults.run` `shell:` key and environment entries with execution semantics are ignored.
  - `scripts/ci_command_table.py:287-293`: a bare name resolves by table key or by the working directory, never by `PATH`.
  - `scripts/ci_make_walk.py:266-283`: `SHELL` is an ordinary variable.
  - `docs/testing/CI_IMAGE.md:71-104`: the census has no row for `GITHUB_PATH`/`GITHUB_ENV` writes, although the workflows reach them at `elaborate.yml:217`, `:299`, `rtl-fast.yml:111`, `:576`, `rtl.yml:209`, `:297` and `:363`.
  - `docs/testing/CI_IMAGE.md:128`: "Unlisted constructs and unlisted command forms refuse generation."
- **Authority:** Standing authority 6170640746:
  - item 3: "Everything outside the census is refused by name";
  - item 2: each supported construct is "resolved with the tool's real semantics".
  - Round-4 rule: a form that is accepted silently is a finding.
- **Evidence:** `probes/r638_4_probes.py` writes each fixture under a fresh temporary tree with the head's table and source lock. It then runs the head's `ci_tool_inventory.py` in `--write` and `--check` mode (`receipts/probes/probes.log`, `probe-results.json`). A hidden file containing the unclassified `brand_new_command` stands for any unreviewed installer, and the baseline B0 confirms it is refused when followed.

  Each case below was ACCEPTED in both modes with `tools: []` and no residue. `probes/real_semantics.sh` (`receipts/probes/real_semantics.log`; bash 5.3, GNU Make 4.4.1) shows the real tool executing the hidden file in every case.

  | ID | Form | Real execution |
  |---|---|---|
  | W1 | step `shell: bash hidden.sh {0}` with `run: echo okay` | the runner runs `hidden.sh <step file>` |
  | W2 | the same through workflow `defaults.run.shell` | same |
  | W3 | step `env: BASH_ENV: hidden.sh` | non-interactive bash sources `hidden.sh` before the step |
  | W4 | `echo "$PWD/tools" >> "$GITHUB_PATH"`, then a later step `git rev-parse HEAD` | `tools/git` runs |
  | W5 | `export PATH="tools:$PATH"; git rev-parse HEAD` | `tools/git rev-parse HEAD` runs |
  | S7 | `PATH="sub:$PATH" bootstrap.sh` | `sub/bootstrap.sh` runs; the walker follows `./bootstrap.sh` |
  | M1 | Makefile `SHELL := ./hidden.sh` with an `echo okay` recipe | make runs `./hidden.sh -c 'echo okay'` |

  The current tree's `GITHUB_PATH` writes and `PATH=` prefix name installer destinations (`/opt/verilator/bin`, `/opt/sbt/bin`), so the current inventory is not affected. These are missing refusal guards.
- **Impact:**
  - A workflow or recipe edit using any of these forms installs or runs an unreviewed program while `--write` and `--check` both pass.
  - The guide's census and its refusal guarantee are both incomplete for constructs the tree already reaches.
- **Required outcome:**
  - Every reached construct is in the census, including environment-file writes.
  - Each of these forms is either resolved with its real semantics or refused by name: step/default `shell:`, environment entries that alter execution (`BASH_ENV`, `PATH`, and equivalents), `GITHUB_PATH`/`GITHUB_ENV` writes, `PATH`-based lookup, and Make `SHELL`.
  - Each refusal has a control in generation and in comparison.
- **Verification:** Re-run `probes/r638_4_probes.py` at the corrected head:
  - W1-W5, S7 and M1 report REFUSED, or classify the real target;
  - the B1 and DECL-03 positive controls stay ACCEPTED;
  - `--check` stays rc 0 on the tree.

### R638-4-F3 MAJOR: an installer behind `xargs` is accepted with no tool recorded

- **Lenses:** Conformance, Robustness, Tests, Docs.
- **Where:**
  - `scripts/ci_command_table.py:347-371`: `wrapper_command` classifies the child argv as written. The words `xargs` appends at run time are never modelled.
  - `:296`: rows with a handler skip their argument patterns, so the `xargs` row's one recorded pattern (`command-table.json:12796`) is never enforced.
  - `docs/testing/CI_IMAGE.md:87`: the census row "Command wrappers: Parse supported options and classify children".
- **Authority:**
  - Assignment 6160953880 item 1: "A check fails when a workflow installs a tool the inventory lacks."
  - Round-4 rule item 1: commands pass only by a positive command, subcommand and argument pattern; installers stay entries with tool and pin.
- **Evidence:**
  - X1: a workflow step `echo evilpkg | xargs python3 -m pip install` is ACCEPTED with `tools: []`.
  - X2: `echo evilpkg | sudo xargs apt-get install -y` is ACCEPTED with `tools: []`.
  - Real `xargs` passes `python3 -m pip install evilpkg` to the child (`receipts/probes/real_semantics.log`).
  - X3: `xargs bash` is refused, because the shell handler requires an operand. The installer handlers accept an empty package list and record nothing.
- **Impact:** A real package installation passes both inventory modes with the package absent from the inventory. This is the failure acceptance item 1 exists to prevent.
- **Required outcome:** A wrapper that supplies run-time operands (`xargs`, and any similar row) either is refused in front of installers and followed interpreters, or is limited to positively listed complete child forms. An installer form with no literal request is refused.
- **Verification:**
  - X1 and X2 report REFUSED in both modes.
  - The tree's existing `xargs -P 6 -I{} sh -c … sh {}` form is still classified.
  - `--check` is rc 0.

### R638-4-F4 MAJOR: census constructs resolved with semantics that differ from the real tools

- **Lenses:** Conformance, Robustness, Tests, Docs.
- **Where:**
  - `scripts/ci_shell_walk.py:257-269`: a sourced file is walked as a separate script. Its assignments and `cd` never reach the caller.
  - `scripts/ci_command_table.py:296`: `data`-handler rows (`printf`, `test`, `[`, `shift`, `echo`) skip their recorded patterns, so `printf -v` is accepted. `read` (`command-table.json:6091`) has patterns, but the walker never models the variable it assigns.
  - `scripts/ci_make_walk.py:84`: Make variables start without the environment, so `?=` and undefined references ignore workflow and exported values.
  - `ci_make_walk.py:132-135`: `$(@D)`, `$(@F)` and similar forms silently expand to ''.
  - `ci_make_walk.py:17-73` and `:84-88`: command-line overrides are not passed to a recursive `$(MAKE)`.
  - `ci_command_table.py:410-412` and `ci_make_walk.py:12-14`, `:60-62`: literal text containing `<dynamic>` or `$` is treated as runtime residue. This contradicts `CI_IMAGE.md:118-119`: "Literal dollar signs and marker text never acquire that provenance."
  - `CI_IMAGE.md:78`, `:84-85`, `:92`, `:94` and `:101`: the census rows for these constructs.
- **Authority:**
  - Standing authority 6170640746 item 2: each construct is "resolved with the tool's real semantics".
  - Round-4 rule: a MIS-RESOLVED form is a finding. Amendment 6170543242: inline text is pinned exactly or refused.
- **Evidence:** All cases below were ACCEPTED in both modes with `tools: []`. Real execution of the hidden file is confirmed in `receipts/probes/real_semantics.log`.

  | ID | Form | Walker follows | Real tool runs |
  |---|---|---|---|
  | S2 | `name=bootstrap.sh; printf -v name '%s' hidden.sh; bash "$name"` | `bootstrap.sh` | `hidden.sh` |
  | S3 | `f=bootstrap.sh; read -r f <<< hidden.sh; bash "$f"` | `bootstrap.sh` | `hidden.sh` |
  | S4 | `name=bootstrap.sh; source fragment.sh; bash "$name"`, where the fragment sets `name=hidden.sh` | `bootstrap.sh` | `hidden.sh` |
  | S5 | `source fragment.sh; bash bootstrap.sh`, where the fragment does `cd sub` | `./bootstrap.sh` | `sub/bootstrap.sh` |
  | M2 | `TOOL ?= echo` with step `env: TOOL: brand_new_command` | `echo` | the environment value |
  | M2b | the same with `export TOOL=…; make` | `echo` | the exported value |
  | M3 | target `sub/x`, recipe `bash ./$(@D)/bootstrap.sh` | `./bootstrap.sh` | `./sub/bootstrap.sh` |
  | M4 | `make TOOL=brand_new_command`, recipe `$(MAKE) -C sub`, where the sub-Makefile has `TOOL = echo` | `echo` | the override |
  | S6 | `bash -c 'brand_new_command <dynamic>'` in an undeclared workflow | residue "declared runtime shell program" | the literal program |
  | S8 | `make -C 'sub$x'`, where a literal directory `sub$x/Makefile` exists | residue "runtime Makefile selection" | that recipe |

  S6 and S8 leave a located residue line. It is mislabelled as runtime even though the text is literal, so the residue checklist would wave through a literal unpinned program.
- **Impact:** For each form, the walker classifies a script or command other than the one that runs. An installer placed in the real target passes both modes.
- **Required outcome:** Each of these constructs is either resolved with its real semantics or refused by name, with a refusal control:
  - sourced-file scope;
  - variable-assigning builtins;
  - Make environment and `?=`;
  - Make automatic directory and file forms;
  - recursive-make overrides.

  Literal text never satisfies a runtime allowance in any walker.
- **Verification:** S2-S6, S8, M2, M2b, M3 and M4 report REFUSED, or classify the real target, in both modes. The tree's own `syn/yosys/run.sh` → `malloc.sh` source and its recipe overrides still derive the same inventory.

### R638-4-F5 MINOR: derivation depends on the checkout location through substring normalization

- **Lenses:** Robustness, Tests.
- **Where:** `scripts/ci_command_table.py:292`, `:295`, `:423` and `:440` apply `str.replace(str(self.root), '${CHECKOUT}')` to every argument. Any later occurrence of the root string inside an in-tree path is rewritten too.
- **Authority:** Round-4 rule item 5: "No location heuristics… A checkout or fixture under `/tmp` is treated like any other."
- **Evidence:** In the image, on CPython 3.12.3, offline, with the clone mounted read-only (`receipts/image/in-image-location.log`):
  - a mount at `/workspace/milan-fpga` gives rc 0;
  - a mount at `/src` gives rc 2, `unclassified command 'cc … /src/third_party/tsn-c-stack/src/adp.c …' at tb/verilator/mbx/Makefile:95`;
  - a mount at `/include` gives rc 2 in the same way.

  On the host, a `/tmp` checkout copy derives byte-identical output (`receipts/f2/`).
- **Impact:** A checkout at a common container mount point such as `/src` cannot derive the inventory. The verdict depends on where the tree is mounted, not on its content.
- **Required outcome:** Normalize only an exact leading checkout path component. The derivation result must not depend on the checkout path.
- **Verification:** `ci_tool_inventory.py --check` is rc 0 with the checkout mounted at `/src` and at `/include`, and a control fixture covers a root string that recurs inside a path.

### R638-4-F6 MINOR: Python capability detection misses foreign-function execution and submodules of allow-listed package names

- **Lenses:** Conformance, Robustness, Tests.
- **Where:**
  - `ci/image/command-table.json:12936`: `ctypes` is an allow-listed import, and `scripts/ci_command_table.py:19-20` and `:181-191` contain no `ctypes` trigger.
  - `ci_command_table.py:155-158` and `:171-180`: `from pkg import mod` records only `pkg`. When `pkg` is a local package directory whose name is allow-listed, `pkg/mod.py` is never followed.
- **Authority:**
  - Census row `CI_IMAGE.md:102`: "Follow local files; require declarations for execution/network capabilities".
  - Round-4 rule item 4: declaration is triggered by detection, not decoding.
- **Evidence:** Both cases were ACCEPTED with `tools: []` and no residue, and real CPython executes the hidden program in both (`receipts/probes/real_semantics.log`).
  - Y1: `ctypes.CDLL(None).system(b"brand_new_command")` in an undeclared script.
  - Y3: `from firmware import hidden`, where `firmware/hidden.py` runs `subprocess.run(["brand_new_command"])`.

  No current-tree instance: the four reached scripts that import `ctypes` are all declared, and no allow-listed import name is a local package directory.
- **Impact:** An undeclared script can execute commands, or reach an unfollowed executing module, while both modes pass.
- **Required outcome:** Treat foreign-function libraries (`ctypes`, `cffi` call surfaces) as execution capabilities requiring a declaration. Follow the submodule files of local packages, or refuse them.
- **Verification:** Y1 and Y3 report REFUSED, or follow and classify the hidden module, in both modes.

### Not findings (checked)

- **Y2, `getattr(os, "system")(…)`.** This is recorded as located residue `bootstrap.py:2: runtime Python execution or lookup`. It falls inside the residue class the earlier ruling assigns to `getattr`.
- **NEW-06, a `select` loop.** It is accepted as a word loop, and its body is walked with the literal list values, so no command escapes classification.
- **S1, `shift` inside a function.** It is refused as a runtime command name.
- **All 12 other new-construct probes are refused by name:** `coproc`, `[[ ]]`, the `time` keyword, `(( ))`, `eval`, `alias`, Make `vpath`, `ifdef`, `$(info)`, `.ONESHELL`, `!=`, and a new command name.
- **One unsupported variant per supported construct is refused:** a computed `.DEFAULT_GOAL`, a target matching two pattern rules, a subshell `cd` to a computed path, a changed byte of a pinned `-c` text, a function called from another file, a computed `$(shell)`, and a computed function name.

### Suggestions (do not affect the verdict)

- **S1 (retained from R638-3-S1).** Add runtime privacy rules for the checkout and `--work` roots. My scan found no host working root in any layer.
- **S2 (retained from R638-3-S2).** Before announcing the image, check that the registry serves the lock's manifest digest unchanged.
- **S3 (new).** Require a declaration when `getattr` targets an execution module (`os`, `subprocess`), even though the call stays residue.

No RESIDUE is recorded.

## Re-run of every form R638-3 and R639-3 listed

All forms were re-run through `probes/prior_forms.py` (`receipts/probes/probes.log`), in both modes:

| Forms | Result at e355f789 |
|---|---|
| R638-3-F1, all 19 forms | REFUSED by name: `gh extension install`; `gh release download`; `git submodule add <url>`; `git config … url` with `submodule update`; `git clone host:path`; `git archive --remote`; `python3 <<EOF`; `python3 -I - <<EOF`; `os.popen`, `os.execvp`, `os.spawnlp` and `asyncio.create_subprocess_exec`; `pip._internal`; `urllib3`; `asyncio`+`ssl`; pattern-rule prerequisite; `make --directory=fx run`; `working-directory: fx` with `make`; job-level `uses:` |
| R638-3 four borderline forms | REFUSED: `echo … \| bash`; `bash <<<`; alias `runner = subprocess.run`; `importlib.import_module` |
| Container and service images | Digests recorded as image tools; moving container and service tags REFUSED |
| R639-3-F1 | REFUSED: `--file=install.mk`; `-finstall.mk`; literal `.DEFAULT_GOAL := install`; `make install` through `%:` |
| R639-3-F2 | Undeclared `subprocess.run(**{"args": …})` REFUSED. A declared script's unpacked unclassified command is still REFUSED. |
| R639-3-F3 | `working-directory: subdir` follows `subdir/bootstrap.sh` (refused); `(cd subdir); bash bootstrap.sh` follows the root script (refused) |
| Declared-script controls | A changed declared script and an undeclared network import are both REFUSED; a declared script with a classified command is ACCEPTED |
| Missing and orphan controls | Pass in `ci_tool_inventory_selftest.py` (rc 0 on host and in image) |
| Current tree versus e6b86814 | `tools` are identical: 45 records with the same pins and provenance. Inputs went from 296 to 328 and residue from 735 to 269 located entries (`receipts/inventory-same-as-e6b86814.txt`) |

## Focus items at this head

| Item | Result | Evidence |
|---|---|---|
| 1. Derived inventory and check | `--check` rc 0 on CPython 3.12.3 (host venv and image) and on a `/tmp` checkout; missing and orphan controls pass; every prior form refused. Not closed against the new forms: F2-F4 and F6 (silent acceptance or mis-resolution) and F5 (location). | `receipts/gates/`, `receipts/probes/`, `receipts/f2/`, `receipts/image/in-image-*.log` |
| 2. Dockerfile | Unchanged since `e6b86814`. History shows the digest-pinned base plus 13 tool COPY/RUN layers. My `--prepare-only` re-verified all 666 checksummed artifacts and reproduced recipe `e689418b…`. | `receipts/image/history.txt`, `receipts/image/prepare.log` |
| 3. Reproducible build and lock | Both author cold records agree on manifest, config, size 3,931,071,698 and 14 layers. My own cold `--no-cache` build produced the same manifest and config, with only the base cached. `--verify-archive` binds the lock to my export. | public `author-r4/round4-cold-comparison.json`; `receipts/image/r638-cold-rebuild.*`, `cold-rebuild.log`, `verify-archive.log` |
| 4. Versions and offline smoke | `--network none` smoke rc 0: 95 checks at rc 0 and none failing. Verilator `5.050 rev v5.050`, Yosys 0.66 (`86f2ddeb`), sv2v v0.0.12, GNU Make 4.3, CPython 3.12.3; Scala and the oracle packet both run. | `receipts/image/smoke.log` |
| 5. Privacy | No `User`, `WorkingDir` or `Author`. The only label is the base `org.opencontainers.image.version`. The 8 Env entries are documented. No host path in history. My scan: no metadata hits; 55 word-bounded content hits, all covered by authenticated allowances; config clean. The repository report re-proves 526 allowances. | `receipts/image/inspect.json`, `history.txt`, `r638-privacy-scan.*`, `privacy-report.json` |
| 6. CI_IMAGE.md | The rebuild, digest-change, pull-by-digest, SDK link and environment sections are accurate; I followed the rebuild steps myself. The census and refusal claims at `:71-104`, `:118-119` and `:128` are inaccurate (F2, F4). | doc gates in `receipts/gates/` |
| 7. No workflow change | Holds | `receipts/integrity/clone-integrity.txt` |

## Manager rulings, checked

- **(a)** The mf48 calibration arm NOT RUN is the existing hosted skip. It is not a finding.
- **(b)** The grouped builder evidence is an exact cover. `probes/builder_groups_cover.py` reads the `__main__` loop of `sw/builder/test_builder.py` at this head and finds 103 invocations. The nine published `author-r4/builder-functions-*.json` records hold 103 results: none missing, extra or duplicated. All are at source SHA-256 `997e8528…`, which equals this head's file and the table pin, and all require RV32. The image those groups ran on is byte-identical to this head's image. Accepted as the completed verdict, and not re-run (`receipts/builder-groups/cover.log`).
- **(c)** `MAKEFLAGS += -e`: the image's make is GNU Make 4.3 (`smoke.log`), in an image byte-identical to the round-3 image. Both round-3 reviews read the hosted docs-check at live dev and found it takes the same skip on the same make 4.3, so no coverage loss arises. Not a finding.
- **(d)** No workflow file changed.

## Prior findings at this head

| Finding | Status | Evidence |
|---|---|---|
| R638-3-F1 MAJOR | Every listed form closed. The cause class, silent acceptance or mis-resolution by the walkers, is retained under new forms as R638-4-F2, F3, F4 and F6. | table above |
| R638-3-F2 MINOR, `/tmp` location | Closed as specified: default-TMPDIR self-tests rc 0 on host and in image, and a `/tmp` checkout derives byte-identical output. A different location dependence is raised as R638-4-F5. | `receipts/f2/`, `receipts/image/in-image-inventory.log` |
| R639-3-F1, F2, F3 MAJOR | Every listed form closed | table above |
| R638-3-S1 and S2 | Not implemented; retained as S1 and S2 | |
| R638-3-S3, `installer_forms` unused | Implemented: `ci_command_table.py:380` reads the table field | |
| R638-2 and R638-1 findings, R639-2 and R639-1 findings | Closed in earlier rounds. Nothing in round 4 reopens them: the image recipe files are unchanged since `e6b86814`, my cold rebuild reproduces the image, and the privacy and bare-metal gates pass. | `receipts/image/`, `receipts/gates/` |

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1, F2, F3, F4, F6) | Round-4 rule, amendment and standing authority; assignment item 1; `ci_tool_inventory.py`, `ci_command_table.py`, `ci_shell_walk.py`, `ci_make_walk.py`, `command-table.json`, `tool-inventory.json`; image lock; probes and real-semantics receipts; hosted gate failures | R638-4 | e355f789b4f59b86083809299134557ca47bbcfb |
| RTL | UNCLEAN (F1) | `pp_srcs.py --check --selftest` failure on the copied protocol-processor source list (`command-table.json:12450`); unchanged `Dockerfile`/`install.py` tool layers reproduced by my cold build; offline Verilator, Yosys and sv2v smoke; gitlinks equal at base and head | R638-4 | e355f789b4f59b86083809299134557ca47bbcfb |
| Robustness | UNCLEAN (F2, F3, F4, F5, F6) | 23 defect-flagged probes (21 findings, plus Y2 and NEW-06 judged not findings); 33 prior-form refusals and one digest record; 12 new-construct and 7 variant refusals; mount-location runs in the image; `/tmp` checkout; `--prepare-only` over 666 artifacts | R638-4 | e355f789b4f59b86083809299134557ca47bbcfb |
| Tests | UNCLEAN (F1, F2, F3, F4, F5, F6) | 15 source gates, plus `--selftest` of em-dash and py-idiom, all rc 0; `ci_inventory_patterns_selftest.py` (117 PASS) and inventory self-test on host and in image; hosted `docs-check`, `verilator-lint` and `rtl-fast` failures reproduced locally; builder exact cover | R638-4 | e355f789b4f59b86083809299134557ca47bbcfb |
| Docs | UNCLEAN (F2, F3, F4) | `docs/testing/CI_IMAGE.md`, all sections, especially the census `:60-129`; `docs/README.md`; REVIEW READY 6172213656; doc gates (`docs_check`, doc style, doc paths, TOC, em-dash) all rc 0 | R638-4 | e355f789b4f59b86083809299134557ca47bbcfb |

## Real limits

- **Docker use.** Following the round's focus instruction to rebuild or inspect the image, I did the following:
  - saved the final image and the locally present pinned base, with no pull;
  - ran one cold `--no-cache` build through `build.py`, using buildx v0.38.0 installed only into a scratch client-configuration directory with no credentials (release checksum verified), and the separate repository name `r638-4-cold`;
  - removed both `r638-4-cold` tags afterwards, so the six pre-existing tags on `86d7aa16` remain;
  - ran offline `--rm --network none` containers for the smoke check and the in-image inventory runs.

  The build added entries to the daemon's build cache. There was no push, login, other pull, or tag change to any other image.
- **Host environment.** The host interpreter is CPython 3.14.7, so the gates ran in a scratch venv on CPython 3.12.3 with PyYAML 6.0.3 and the hash-pinned Markdown requirements. The `real_semantics.sh` demonstrations use host bash 5.3, GNU Make 4.4.1 and host Python; the image has Make 4.3, whose `SHELL`, `?=`, `$(@D)` and override semantics are the same.
- **One host only.** Cross-host reproducibility and a registry round trip are untested.
- **Not run.** No builder campaign, product regression, act run, full bank, hardware or physical calibration.
- **Hosted snapshot.** One observation at 16:23Z: 18 success, 3 failure (F1), 1 skipped (Physical gPTP), and 5 in progress (four Verilator shards and `elaborate`). It is not a hosted verdict.
- **Clone untouched.** All probes ran in temporary fixture trees. `receipts/integrity/clone-integrity.txt` records:
  - worktree and index equal HEAD, and the porcelain status is empty;
  - the index listing equals the HEAD tree listing (`4c7f5a68…`);
  - all six gitlinks equal HEAD and base.

## Pending manager duties

- Hosted and act acceptance at the eventual head. At this head the `docs-check`, `verilator-lint` and `rtl-fast` contexts fail (F1).
- Current-dev merge-candidate validation: source base `fa7347fc`, live dev `11349392`.
- Re-review of F1-F6 at a corrected head. `command-table.json` and the walker scripts are recipe inputs, so a corrected head changes the recipe digest. The Docker recipe may still leave the image bytes unchanged, which a new cold pair should show.
- Image publication only after both reviews are POSITIVE, then confirmation that the registry digest equals `image.lock.json` (S2).

## Publishable files

`MANIFEST.sha256` lists every published script and receipt. Host paths are replaced by `<packet>`, `<clone>`, `<home>` and `<data>`. The image scan reads the protected identities from the repository's codepoint table and from an unpublished local marker file, and publishes labels, paths, hashes and counts only. The exported image, staged sources, fixture trees, scratch venv and parser stay under `scratch/` and are not published.

R638-4 FINISHED
