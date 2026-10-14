[R638] NEGATIVE - exact head 4391f353690972f4844cb641b1e77fa94f38cdf4

# R638-5: internal independent review of issue #737 / PR #738

Tree `f2882c85eb46b66b35cdec6e69861849af690f4b`. Full range `fa7347fc59173f90e4feec2df207692e6e6e72ec..4391f353690972f4844cb641b1e77fa94f38cdf4` (27 commits, 37 files, all additions except `docs/README.md` and `scripts/check_baremetal_only.py`); round-five range `e355f789..4391f353` (8 commits, 14 files). No workflow file, `.gitmodules`, gitlink, HDL, firmware or testbench changes.

Context was reconstructed in the contract order: AGENTS.md, CONTRIBUTING.md, docs/README.md, the issue body and public rulings, the lane assignment, the round-five assignment, the diff and history, then public executable evidence. The R638-4 and R639-4 findings were read only after the independent pass over the diff and the probes below.

## Verdict summary

- **The round-four BLOCKER is closed.** At this exact head, the Entity shape gate passes (228 checks, 0 failures) and the protocol-processor source-list step passes, both in the hosted contexts and in my own in-image run. Every hosted context at this head is green. My in-image replay of every docs-check and rtl-fast gate step is green, except the RV32 adoption link (F4).
- **Every R638-4 and R639-4 form is refused at this head** (30 fixtures), and so are 25 of my own closure controls, at least one per walker.
- **The closure criterion does not hold.** Seven constructs are ACCEPTED: the census or the node allowlist admits them, and the deriver then resolves them differently from the real tool. In each one, a planted installer passes generation and comparison with the committed `tools` and residue unchanged, while the real tool runs it. One of the seven is live in the current tree: an executing, undeclared local module is reached by a docs-check gate and never followed.
  - F1 MAJOR: Python local modules are hidden by the external-import allowlist.
  - F2 MAJOR: four Make forms are mis-resolved.
  - F3 MAJOR: the shell `$(… pwd …)` heuristic is mis-resolved.
- **One MINOR:** F4, the image guide's RV32 adoption procedure fails against the workflow's own pinned verify step.
- **The image is correct.** The image lock is bound to this census (recipe `214fefe3…`). The local export of `sha256:86d7aa16…` authenticates against the lock's manifest, config and all 14 layers. The built-in privacy scan and my independent scan find no private content.

## Findings

### R638-5-F1 MAJOR — Conformance, Robustness, Tests, Docs — local Python modules hidden by the external-import allowlist

- **Where:**
  - `ci/image/command-table.json:12882` (`python_imports`): 131 of its 210 names are in-tree module or package names, among them `run` (`:13049`) and `flash_map` (`:12954`).
  - `scripts/ci_command_table.py:190-192`: an import the walker cannot resolve from its fixed bases (`:253-258`: importer directory, root, `scripts/`) is accepted when the allowlist contains its name. It is neither followed nor declared, and it leaves no residue.
- **Authority:**
  - Round-five assignment 6173370560, item 2 (Python): "a local module or package whose name shadows an external import" is refused, and initializers are followed.
  - Closure criterion, item 5.
  - Manager class ruling: followed Python scripts that import a network module or run subprocesses must be declared.
  - Guide `docs/testing/CI_IMAGE.md:102` and `:131`: "Local Python packages take precedence over external-import allowances."
- **Evidence, current tree:**
  - `scripts/check_nvm_capture.py:27-29` (the docs-check step "Capture measurement census and clock gate") runs `sys.path.insert(0, HARNESS)` and then `import run as capture`. Python loads `tb/verilator/nvm_capture_cpu/run.py`, which imports `subprocess` and calls `subprocess.run` (`:31`, `:185`).
  - That file is absent from the inventory `inputs` and has no table declaration.
  - 17 allowlisted local modules are never followed. Among them are `sw/litex/flash_map.py` (imported by `sw/firmware/nvm_hosttest/test_nvm_firmware.py:88`, `sw/firmware/ctrl_nvm/test/nvm_bench.py:42` and `sw/builder/test_builder.py:339`), `board_audio_routing`, `check_gptp_owner_pair`, `soc` and `firmware`.
- **Evidence, probes** (`receipts/probes/run1.txt`, `real-tool-confirmation.txt`):
  - P1 appends an installer call to `run.py`. P2 appends one to `flash_map.py`.
  - The deriver returns ACCEPTED with tools and residue identical to the committed inventory. The planted file is still not an input, so `--check` stays rc 0.
  - In the image, the real docs-check gate `python3 scripts/check_nvm_capture.py`, and the `test_nvm_firmware.py` importer, both execute the planted call.
- **Impact:** A docs-check gate imports an executing, undeclared module that the inventory never inspected. An installer added there, or in any of the other allowlisted local modules, passes both inventory modes. This is the failure the inventory check exists to catch.
- **Required outcome:**
  - No allowlist entry silently stands in for an in-tree module.
  - An import whose name resolves to an in-tree file the walker did not follow is either followed, for example by modelling literal `sys.path` insertions, or refused by name.
  - Reached executing modules carry declarations.
  - The deriver records no tool change for the current tree.
- **Verification:**
  - P1 and P2 are refused, or followed and refused as undeclared executing modules.
  - `tb/verilator/nvm_capture_cpu/run.py` appears in `inputs` with a declaration.
  - `ci_tool_inventory.py --check` is rc 0 with the 45 tool records unchanged.

### R638-5-F2 MAJOR — Conformance, Robustness, Tests, Docs — Make constructs accepted and resolved differently from GNU make

- **Where:**
  - `scripts/ci_make_walk.py:298` with `:324`: an assignment the regex misses becomes a rule whenever the line contains `:`.
  - `:370-383`: an explicit rule with no recipe and no matching pattern contributes no command.
  - `:379` and `:395`: under a pattern rule, `$<` binds to the explicit prerequisite.
  - Census rows `CI_IMAGE.md:90`, `:92` and `:94`.
- **Authority:** Standing ruling 6170640746 and round-five item 3: every census construct keeps the tool's real semantics, or is refused. Closure criterion item 5.
- **Evidence:** Each fixture below sits in a new `tb/verilator/*/Makefile`, which the deriver walks. In every case the deriver returned ACCEPTED, with tools and residue unchanged (`receipts/probes/run1.txt`, `run2.txt`). Real GNU Make 4.3 in the image (`receipts/probes/real-tool-confirmation.txt`) behaves as follows:

  | ID | Fixture | Deriver | GNU make |
  |---|---|---|---|
  | P3b | `CMD = echo ok`, then ` CMD = sudo apt-get install -y cowsay # note:` (leading space), then recipe `$(CMD)` | treats the second line as a rule; recipe `echo ok` | `make -n` prints `sudo apt-get install -y cowsay` |
  | P6b | `X != sudo apt-get install -y cowsay >&2; echo a:` | treats it as a rule | runs the shell at parse time, even under `-n` |
  | P4 | `CC = sudo apt-get install -y cowsay ; cc` and a recipe-less `probe_builtin: probe_builtin.c` | no command | built-in implicit rule: `sudo apt-get install -y cowsay ; cc probe_builtin.c -o probe_builtin` |
  | P5 | `probe.out: benign.sh`, then `%.out: %_evil.sh` with recipe `bash $<` | follows `benign.sh` | `$<` is the implicit rule's prerequisite; runs `bash probe_evil.sh` |

- **Impact:** For each form, the deriver blesses a recipe population other than the one make executes. A literal installer passes both inventory modes.
- **Required outcome:** Each of these forms is refused by name, or resolved with make's semantics:
  - leading-whitespace and other assignment spellings;
  - `!=`;
  - built-in implicit rules for recipe-less targets (or require `-r`/`MAKEFLAGS += -r` and refuse otherwise);
  - the `$<`/`$^` binding of implicit rules.

  Each needs a control.
- **Verification:** P3b, P4, P5 and P6b are refused, or record or refuse the planted installer. `--check` is rc 0 on the tree.

### R638-5-F3 MAJOR — Conformance, Robustness, Tests, Docs — command substitution resolved to `pwd` when its output is not pwd's stdout

- **Where:** `scripts/ci_shell_walk.py:57-66`. The substitution's value becomes the walked directory whenever the last pre-order `CallExpr` is a bare `pwd`, whatever its redirections or reachability. Census row `CI_IMAGE.md:80`.
- **Authority:** Same as F2.
- **Evidence:**
  - P7 adds a step `cd "$(cd scripts && pwd > /dev/null)"` followed by `python3 zz_probe_cwd.py`. `zz_probe_cwd.py` at the root holds an installer call, and `scripts/zz_probe_cwd.py` is benign.
  - The deriver follows `scripts/zz_probe_cwd.py` and returns ACCEPTED, with tools and residue unchanged.
  - Real bash 5.2.21 in the image yields an empty substitution. `cd ""` stays at the root, which resolves `/work/zz_probe_cwd.py`, the installer (`receipts/probes/real-tool-confirmation.txt`).
- **Impact:** The deriver follows a different script from the one bash runs.
- **Required outcome:** Resolve the substitution's value only when its stdout is provably that of an unredirected, unconditionally final `pwd`. Otherwise use a runtime value, which is refused or becomes residue under the existing rules. Add a control.
- **Verification:** P7 is refused, or follows the root script and refuses it. The current tree derives the same inventory.

### R638-5-F4 MINOR — Docs, Conformance — the RV32 adoption procedure fails against the workflow's pinned verify step

- **Where:** `docs/testing/CI_IMAGE.md:432-443` says to link `$HOME/br-milan-rv32/host` to `/opt/rv32-sdk` and that "No download or compiler change is required."
- **Evidence** (`receipts/image/rv32_adoption_probe.log`; every `rv32-link+verify` row in `receipts/gates/*/rc.tsv`):
  - The docs-check step and six rtl-fast jobs run `python3 scripts/ci_rv32_sdk.py --destination "$HOME/br-milan-rv32/host"`, and `scripts/ci_events.py:735-739` pins that exact text. Through the documented link it fails: "SDK destination must be an absolute path without symlink parents".
  - `--verify-only` through the link fails with "SDK provenance mismatch".
  - `--destination /opt/rv32-sdk` passes ("SDK cache hit: verified").
- **Impact:** A switch lane that follows the guide gets a red install step in seven jobs. The guide's claim is a technical statement, not wording.
- **Required outcome:** The guide states a verified adoption form. For example, it names the step and contract change the switch lane must make (verification at `/opt/rv32-sdk`, with the link used only for compiler lookup), and it backs that form with a receipt.
- **Verification:** The documented sequence, run in the image, returns rc 0 for the RV32 verification and for the `--require-rv32` consumers.

No RESIDUE is recorded. No new SUGGESTION. The prior suggestions (working-root privacy rules, registry digest round-trip check) remain optional.

## BLOCKER check and full gate step sets (round-five item 1)

**Hosted contexts at the exact head** (`receipts/hosted/exact-head-check-runs-2.tsv`):

- Every context is `success`, including docs-check, verilator-lint, rtl-fast, publication-census, all firmware jobs, elaborate, and the Verilator and Yosys shards.
- The one exception is "Physical gPTP (nightly and manual)", which is `skipped`.
- The hosted docs-check log shows "Entity shape gate … checks: 228 failures: 0, RESULT: PASS" (`receipts/hosted/exact-head-docs-check-excerpt.txt`).

**My offline in-image replay** used `--network none`, uid 1000, four-CPU sets and a total memory of at most 12 GB (`scripts/jobs/`, `receipts/gates/`). Install-only steps were replaced by version proofs: Verilator 5.050, Yosys 0.66 with ABC, sv2v, gtest/gmock, and the presence of PyYAML, wavedrom, rsvg-convert and litex.

- **docs-check: 42 step groups.** 41 return rc 0, including:
  - Entity shape: 228 checks, 0 failures;
  - Bare-metal scope;
  - CI event/SHA contract;
  - the act-runner self-test inside the disposable container;
  - em-dash against the merge base with live dev `f6260253`;
  - the HDL reference, compiler-absent controls and all ratchets.

  The one failure is the RV32 link-verify step (F4).
- **wire-accountability and docs-check-no-git:** rc 0.
- **changes:** rc 0 against the live-dev merge tree; RTL/tooling relevant: true.
- **verilator-lint:**
  - lint: PASS, 90 ≤ ratchet 90;
  - protocol-processor source lists derived: rc 0 ("46 tracked source(s) derived; no build input carries a literal copy").

  A first attempt at 3-5 GB was killed by my container memory limit. The 8 GB rerun is clean (`receipts/gates/lint2/`).
- **bdd-conformance:** rc 0.
- **yosys-elaboration:** all 7 groups rc 0. Elaboration of the three tops, the OOC read sets, ooc.sh, guard and cache self-tests.
- **publication-census:** rc 0 (1087 s).
- **firmware-unit:** tally, control shard 0/4, saved-state suites and the coverage ratchet, all rc 0.
- **Control, AECP and SRP mutation shards 1/4, 2/4 and 3/4:** rc 0.
- **firmware-boundary and firmware-verilator:** rc 0.
- **In all six RV32 jobs,** the only failing row is the RV32 link-verify step (F4). The `--require-rv32` consumers pass through the link.

**Not run by me.** The full builder gate (`sw/builder/test_builder.py --require-rv32`) is a prohibited builder bank. The hosted docs-check at this head ran it successfully.

## Closure criterion and structural allowlist (round-five items 2 and 5)

Every walker was planted with unlisted constructs (`receipts/probes/run1.txt`, `run2.txt`, `run3.txt`). Each one below was **refused by name** before generation:

- **Shell:** `TestClause`, `ArithmCmd`, `CoprocClause`, `Stmts.Background`, step `shell:` and `defaults.run.shell`.
- **Startup variables:** `BASH_ENV` in step env, `export PYTHONPATH`, a `LD_LIBRARY_PATH` prefix, `PATH` assignments and prefixes, and a `GITHUB_PATH` write.
- **Nested trap programs:** a `TestClause` inside a trap.
- **Make:**
  - `MAKEFILES`, `SHELL` assignment and override, `vpath`, `$(eval)`, `ifdef`, `.ONESHELL` and `$(@D)`;
  - `make -C 'sub$x'`, which is classified by its literal recipe.
- **Python:** the `Global` and `AsyncFunctionDef` nodes, the `__import__` builtin, a local `yaml` package beside a reached importer, and a local package initializer.
- **Workflow structure:** job-level `uses:`, a moving container tag, and a new command name.

The sourced-file control (`syn/yosys/malloc.sh`) and two early Python controls on a declared script are refused by content pin, which also blocks any new construct there.

`match` and walrus are census-listed. They were accepted, as listed, with capability detection intact.

**The criterion still fails:** F1, F2 and F3 are ACCEPTED census or allowlist constructs that are mis-resolved.

## Re-run of every R638-4 and R639-4 form at this head

All 30 fixtures are refused (`receipts/probes/run3.txt`).

| Prior finding | Forms | Result | Status |
|---|---|---|---|
| R638-4-F1 BLOCKER | Entity shape, pp_srcs | Pass, hosted and in image | **Closed** |
| R638-4-F2 | W1-W5, S7, M1, M1b | REFUSED by name | **Closed** |
| R638-4-F3 | X1-X3 | REFUSED | **Closed** |
| R638-4-F4 | S2-S6, S8, M2, M2b, M3, M4 | REFUSED. M2, M2b, M4 and S8 classify the real value and refuse the unclassified command. | **Closed** |
| R638-4-F5 | Mounts at `/src` and `/include` | `--check` rc 0 under CPython 3.12.3 at `/work`, `/src` and `/include` (`receipts/image/inventory-in-image-mounts.log`) | **Closed** |
| R638-4-F6 | Y1 `ctypes`, Y3 `from pkg import mod` | REFUSED (undeclared executing script) | **Listed forms closed.** The cause class, local import traversal, is **retained as R638-5-F1**: the allowlist still hides local modules. |
| R639-4-F1 | Sourced directory and variable, background `cd`, branch functions | REFUSED | **Closed** |
| R639-4-F2 | Make `SHELL` file and command-line forms | REFUSED | **Closed** |
| R639-4-F3 | Literal marker inline programs | REFUSED (unpinned inline text) | **Closed** |
| R639-4-F4 | Local `json` shadow, local package initializer | REFUSED | **Listed forms closed.** The cause is **retained as R638-5-F1**. |

## Other focus items

- **Inventory:**
  - The current tree's `--check` is rc 0 on host and in the image.
  - All seven self-tests pass: inventory, patterns, nodes, build, integrity, privacy and privacy-patch (`receipts/selftests/`).
  - Control C1 shows a recorded installer changes `tools`. The baseline harness run is ACCEPTED with tools and residue identical.
- **Lock binding:**
  - `build.py --check-lock` passes, and the recomputed `recipe_digest()` is `214fefe3bd807c3403558de25d553d5a5a10f682a6bb5a824257f2a27ef192be`, equal to the lock.
  - Recipe inputs include `syntax-census.json`, `command-table.json`, `tool-inventory.json` and all four walker modules.
  - In round five only `recipe_digest` changed in the lock. The image bytes are unchanged at manifest `sha256:86d7aa16e7d2464baf8e0d246434982838c8174de8c8fa610608cce5b23b5e6c`, config `sha256:62b56e1a…`.
- **Export authentication and privacy:**
  - I exported the local image by digest (no pull) and the pinned base, then fetched and verified all 665 locked artifacts with `--prepare-only`.
  - `build.py --check-lock --verify-archive` returns "PASS: image identity verified against exported manifest, config and every layer", including the provenance-based privacy scan (`receipts/image/verify.log`, `privacy-report.json`).
  - My independent scan covered every member's bytes, name, link and owner metadata in all 14 layers, plus the config, environment, labels and history (`receipts/image/privacy-scan.json`, terms hashed). Every hit is inside an upstream binary or an upstream source member: gnutls, unistring, python3.12, the docker client, the node and gh binaries, and VexiiRiscv `Soc.scala`. The project organisation name appears only in the public tsn-gen source URL in `/opt/ci-image/sources.lock.json`.
  - There is no builder home, account, host, credential, label or environment leak.
  - Layer timestamps are uniform. Set-id bits remain only on base-layer upstream binaries and directories. `sudo` works for the default root user.
- **Versions and rulings:**
  - CPython 3.12.3 (`python3.12 3.12.3-1ubuntu0.17`), make `4.3-4.1build2`, git 2.43.0.
  - Ruling (c): the hosted docs-check at current dev `f6260253` (runner `ubuntu24/20261004.327.1`) reports the same "SKIP: the MAKEFLAGS += -e mutation". The image shows the same NOT RUN, so adopting the image loses no coverage and this is not a finding.
  - Ruling (a): the mf48 calibration NOT RUN appears in the hosted log as the existing skip. Not a finding.
  - Ruling (d): no workflow file changed.
- **Cold reproducibility:**
  - Not rebuilt by me: the recipe is unchanged in round five, and buildx v0.38.0 is not installed for this user.
  - The author's round-five cold records are not in public evidence that I could authenticate. R639-4 authenticated two published cold exports of the same manifest.
  - My own evidence is the authentication of the local export against the lock.

## Reviewer-owned ledger

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1, F2, F3, F4) | rulings 6160953880, 6173370560, 6170640746; `ci_command_table.py:190-258`; `ci_make_walk.py:298-395`; `ci_shell_walk.py:57-66`; `receipts/probes/*`; `receipts/hosted/*` | R638-5 | 4391f353690972f4844cb641b1e77fa94f38cdf4 |
| RTL | CLEAN | `ci/image/Dockerfile` stages and layer map; in-image lint (`receipts/gates/lint2/`), pp_srcs, yosys-elaboration (`receipts/gates/yosys/`); diff touches no HDL or gitlink (`receipts/restore-check.txt`) | R638-5 | 4391f353690972f4844cb641b1e77fa94f38cdf4 |
| Robustness | UNCLEAN (F1, F2, F3) | 7 targeted probes, 25 refused closure controls and 30 prior-form fixtures (`receipts/probes/run1-3.txt`, `probe-results-*.json`) | R638-5 | 4391f353690972f4844cb641b1e77fa94f38cdf4 |
| Tests | UNCLEAN (F1, F2, F3) | `scripts/ci_inventory_nodes_selftest.py` and `ci_inventory_patterns_selftest.py` have no control for the F1-F3 forms; `receipts/selftests/*`; full in-image gate replay (`receipts/gates/*/rc.tsv`) | R638-5 | 4391f353690972f4844cb641b1e77fa94f38cdf4 |
| Docs | UNCLEAN (F1, F2, F3, F4) | `docs/testing/CI_IMAGE.md:80`, `:90-102`, `:131`, `:432-443`; `docs/README.md:88` | R638-5 | 4391f353690972f4844cb641b1e77fa94f38cdf4 |

[R638] PASS RTL — `ci/image/Dockerfile`, `receipts/gates/lint2/rc.tsv`, `receipts/gates/yosys/rc.tsv` — The multi-stage, one-layer-per-tool recipe is digest-pinned. The image's Verilator 5.050 and Yosys 0.66 pass the whole-tree lint ratchet, the derived protocol-processor source lists, and the three-top elaboration with its OOC, guard and cache gates. No product RTL, interface or gitlink is changed.

## Real limits

- No reviewer cold rebuild: buildx is absent for this user, and the recipe is unchanged this round. Reproducibility relies on lock authentication of the local export plus earlier public cold records.
- I did not run the full builder gate (prohibited builder bank). It passed in the hosted docs-check at this head.
- Docker use was limited to the lane's allowance:
  - offline runs of the PR's own image, with read-only or disposable mounts;
  - `image save` of the locked image and of the pinned base, both already local.

  There was no pull, push, login or build.
- In-image gate steps replace install steps with version proofs, and run as uid 1000 with HOME `/tmp/home`. This is evidence for the gates and the image, not hosted equivalence.
- One probe fixture (a local `yaml` package under `scripts/`) was imported by my harness process itself. Its payload was a package-manager call that cannot exist on this host, and it failed without effect. I replaced it with N18b.
- The clone is byte-identical to the head after the work: 1347 tracked entries checked for bytes and modes, the index matches, and all six gitlinks are unchanged (`receipts/restore-check.txt`).

## Pending manager duties

- Current-dev merge-candidate builder and native banks, and their receipts.
- Hosted and act acceptance.
- Registry publication and a digest round-trip check.
- The switch lane's adoption, including the F4 change.
- Completion of both independent reviews.

R638-5 FINISHED
