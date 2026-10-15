[R638] NEGATIVE - exact head 6918d4f9bee7081a71f94d9090d01c557085658a

# R638-6: internal independent review of issue #737 / PR #738

- Tree `cf35c3b9acfa5215f285a867f39fb583d84f01cc`.
- Full range `fa7347fc59173f90e4feec2df207692e6e6e72ec..6918d4f9bee7081a71f94d9090d01c557085658a`: 34 commits, 42 files, no workflow file.
- Round-six delta `4391f353..6918d4f9`: 7 commits, 19 files.
- No `.github/`, HDL, firmware, testbench, `.gitmodules` or gitlink change.

## How the review was done

- **Order of reading.** I rebuilt the contract in the required order: AGENTS.md and CONTRIBUTING.md, docs/README.md, the issue body and public rulings, the round-six class ruling (6177332782), the author's READY (6183149185), the diff and history, then public executable evidence (`review-evidence/737-image-r1/author-r6` at `3bd3d938`).
- **Independence.** I read the R638-5 and R639-5 findings only after my own pass over the diff and my own probes were complete.
- **Ground truth.** Every walker probe below was compared with the real tools in the PR's own locked image, run offline: GNU Make 4.3, bash 5.2.21 and CPython 3.12.3. A disposable `brand_new_command` sentinel marks the hidden command. The real tool proves it executed that command by failing with "not found".

## Verdict summary

- **Items 2, 4 and 5 of the ruling hold:**
  - `run.py` is reached and declared.
  - No external-import allowance names an in-tree module.
  - Installers appended to `run.py` or `flash_map.py`, or planted as stdlib-shadowing local modules, are refused by name.
  - The documented RV32 sequence and the `--require-rv32` consumers return rc 0 in the image.
  - The image (`sha256:86d7aa16…`, config `sha256:62b56e1a…`, 14 layers) authenticates against the lock at this head. The author's two cold records agree with each other and with the lock.
  - The smoke checks pass offline.
  - All 45 tool records keep their tools, pins and step provenance.
- **Every R638-5 and R639-5 form is refused at this head:** P1-P7, `make_target_override` and the two traversal-cache fixtures.
- **The head is not consistent with itself (F1).** The final commit changed a declared script without re-pinning it. At this exact head, `scripts/ci_tool_inventory.py --check` refuses, and so does `build.py --prepare-only`, which runs that check. This holds on the host and in the image under CPython 3.12.3. The guide's rebuild sequence cannot be followed.
- **Item 1 of the ruling fails (F2, F3).** The walkers still accept forms that they resolve differently from the real tools:
  - 6 Make forms;
  - 5 shell forms;
  - 4 literal Python capability forms.

  In each case both inventory modes return rc 0, while the real tool runs the hidden command.
- **Item 3 of the ruling is incomplete (F4, F5):**
  - The ptrace audit judges only the interpreter binary that the kernel reports. So `pip3`, `npm`, an offline `python3 -m pip install` that succeeds, and an unlisted shebang script in a system directory are all clean. Only ELF programs are judged by name.
  - The current-tree receipt covers 9 steps, mostly version probes, rather than every reached docs-check and rtl-fast step. It is not committed.

## Findings

### R638-6-F1 MAJOR: inventory check refuses at the exact head (stale declared-script pin)

**Lenses:** Conformance, Tests, Docs.

**Where:**

- `ci/image/command-table.json:13060` and `ci/image/tool-inventory.json:32` pin `scripts/check_baremetal_only.py` at `a402f516…`.
- Commit `6918d4f9` added `HOST_RUNTIME_MASKS["ci/image/exec_audit.py"]` at `scripts/check_baremetal_only.py:436-444`. The file now hashes to `bc594d82…`.
- Neither pin was refreshed.

**Authority:**

- Lane deliverables (1) and (3): the derived inventory and its check pass on the tree, and the image rebuilds from the recipe.
- The ruling's rule that a changed declared script refuses.
- `docs/testing/CI_IMAGE.md:283` and `:292`: the rebuild sequence.
- The READY claim that the inventory self-tests return rc 0 at the committed head.

**Evidence:**

- `receipts/image-inventory-check-exact-head.log`: in the image, CPython 3.12.3, read-only mount of the exact head, `REFUSED: changed declared script 'scripts/check_baremetal_only.py'`, rc 2.
- `receipts/host-inventory-check-exact-head.log`: the same on the host.
- The author's public inventory receipts (`round6-item1/item3-source-inventory.log`) predate this commit. No receipt at this head shows the check passing.
- In a disposable copy I re-pinned the two hashes. `--check` then fails only on the inventory's own recorded `command-table.json` digest (`receipts/inv-check-repinned-copy.log`). After `--write`, that digest line is the only change, and all 45 tool records are identical (`receipts/inv-repinned-copy.diff`).
- That copy's `--prepare-only` reports recipe `a0337622…`, not the lock's `54cd38de…` (`receipts/prepare-fixed-copy.log`). So the repair also changes the recipe digest and requires a re-recorded lock.

**Impact:**

- At the head under review, the lane's own check is red.
- `build.py --prepare-only` refuses, so the lock cannot be reproduced from this tree by the documented procedure.
- The follow-up lane would adopt a red gate.

**Required outcome:**

- The declared pin and the inventory inputs match the committed `check_baremetal_only.py`.
- The lock's `recipe_digest` is re-recorded for the changed recipe inputs, with the image digest still authenticated.
- A receipt at the final head shows `ci_tool_inventory.py --check` rc 0.

**Verification:**

- `python3 scripts/ci_tool_inventory.py --check` rc 0, on the host and in the image.
- `build.py --check-lock` and `--check-lock --verify-archive` PASS at the new head.
- The tool records are unchanged.

### R638-6-F2 MAJOR: Make and shell forms accepted silently but resolved differently from GNU Make 4.3 and bash 5.2

**Lenses:** Conformance, Robustness, Tests, Docs.

**Where:**

- `scripts/ci_make_walk.py:512`: inside a conditional, the guard admits any line that starts with `else` or `endif`. An assignment such as `elseX = …` or `endifX = …` is therefore applied unconditionally. The census says "refuse conditional assignments" (`docs/testing/CI_IMAGE.md:99`).
- `scripts/ci_make_walk.py:190`: environment-origin variables are marked simple. GNU make treats them as recursive, so a later `+=` must stay deferred.
- `scripts/ci_make_walk.py:313`:
  - `$(call)` never binds `$(0)` to the macro name;
  - a nested call inherits the outer call's higher-numbered arguments, which make blanks.
- `scripts/ci_make_walk.py:345-346`: `$(abspath)` uses `Path.resolve()`, which follows symlinks. Make's `abspath` is lexical.
- `scripts/ci_shell_walk.py:99-127` (`exact_substitution`):
  - `dirname`, `realpath`, `cd` and `pwd` are modelled as the coreutils program or the builtin, even when the same shell has defined a function of that name;
  - `cd -` is resolved as a directory named `-`.

**Authority:**

- Class ruling 6177332782, item 1: accept only shapes resolved with the real tool's exact semantics, and refuse everything else by name.
- Round-six focus (1): each form is refused or resolved exactly against the image's Make 4.3 and bash 5.2.
- `docs/testing/CI_IMAGE.md:136-137`.

**Evidence:** the walker results are in `receipts/probes-make-walker.json`, `probes-shell-walker.json` and `probe-m20-walker.json`. The real-tool results are in `receipts/probes-make-real.txt` and `probes-shell-real.txt`. The fixtures are in `scripts/probes_make.py`, `probes_shell.py` and `probe_m20.py`.

| ID | Fixture (abridged) | Walker `--write` / `--check` | Real tool in image |
|---|---|---|---|
| M1 | `ifeq (a,b)` / `elseX = echo` / `endif` / `all: ; $(elseX) brand_new_command` | rc 0 / rc 0 | make runs `brand_new_command` |
| M2 | same with `endifX` | rc 0 / rc 0 | runs it |
| M3, M3b | step env `FOO=echo` (and `export FOO=echo`); `FOO += $(BAR)`; `BAR = ; brand_new_command`; `all: ; $(FOO) okay` | rc 0 / rc 0 | `echo ; brand_new_command okay`; runs it |
| M4 | `RUN = $(if $(0),,echo) brand_new_command`; `$(call RUN)` | rc 0 / rc 0 | runs it |
| M5 | `inner = $(if $(2),echo,brand_new_command) okay`; `outer = $(call inner,x)`; `$(call outer,a,b)` | rc 0 / rc 0 | runs it |
| M20 | committed symlink `sub/link -> ../other/deep`; `bash $(abspath sub/link/../run.sh)` | rc 0 / rc 0 (walks `other/run.sh`) | make runs `sub/run.sh` (sentinel) |
| M21 | recipe `dirname() { echo sub; }; bash "$$(dirname x/run.sh)/run.sh"` | rc 0 / rc 0 | runs `sub/run.sh` (sentinel) |
| S1 | `dirname() { echo sub; }` then `bash "$(dirname x/run.sh)/run.sh"` | rc 0 / rc 0 | runs `sub/run.sh` |
| S3 | `pwd() { echo sub; }` then `bash "$(cd scripts && pwd)/run.sh"` | rc 0 / rc 0 | runs `sub/run.sh` |
| S5 | `bash "$(cd - && pwd)/run.sh"` with a directory named `-` | rc 0 / rc 0 (walks `-/run.sh`) | bash goes to `$OLDPWD`, never `-/` |
| S6 | `realpath() { echo sub/run.sh; }` then `bash "$(realpath x/run.sh)"` | rc 0 / rc 0 | runs `sub/run.sh` |

Forms that are refused or resolved exactly, and are therefore not findings:

- target-specific inheritance into a prerequisite (M6) and target-specific values on a later line (M19);
- `\tendef` (M7);
- `$(wildcard)` order (M8);
- an unselected `$(if)` branch (M9);
- a late `.DEFAULT_GOAL` (M10);
- a recursive command-line value (M11);
- `#` inside a reference (M12);
- target-specific values beating the environment (M13);
- `all: ;` followed by tab lines (M14);
- `else:` rules (M15, M17);
- a recipe across blank and comment lines (M16);
- `make -n` (M18);
- function shadowing of `cd`, `echo` or `bash` as a command (S2, S4, S7, S8);
- `expand_aliases` (S9);
- `command cd` (S10).

**Impact:** an accepted, fully literal Make or shell input runs a command the inventory never examined, while both inventory modes stay green. This is the class the round-six ruling closes.

**Required outcome:**

- Conditional bodies admit only the exact directive words, never prefixes.
- Environment-origin variables keep make's recursive flavor for `+=`.
- `$(call)` binds `$(0)` and blanks unpassed arguments as make does, or refuses `$(0)` and nested calls.
- `$(abspath)` is lexical, or refuses when a symlink lies on the path.
- Exact substitution shapes and `cd` refuse when a same-named function is defined in scope, and refuse `cd -` and option operands.

Each fix needs a planted control.

**Verification:**

- M1-M5, M20, M21, S1, S3, S5 and S6 are each refused by name, or resolve to the sentinel and refuse it.
- The current tree derives the same 45 tool records.

### R638-6-F3 MAJOR: literal Python execution through module attributes escapes capability detection

**Lenses:** Conformance, Robustness, Tests, Docs.

**Where:**

- `scripts/ci_command_table.py:426-445`: capability is decided by a qualified-symbol prefix list (`os.system`, `subprocess.`, …) and by the bare names `eval`, `exec` and `__import__`.
- These all reach execution without matching:
  - `sys.modules["os"].system(...)`;
  - `sys.modules["subprocess"].run(...)`;
  - `os.__dict__["system"](...)`;
  - `builtins.eval(...)`.
- `builtins` and `sys` are allowed imports.

**Authority:**

- Class ruling item 1, and the standing rule: detection-triggered declarations for executing or network-capable Python, and everything outside the census refused by name.
- `docs/testing/CI_IMAGE.md:34`, `:108`.

**Evidence:**

- In a disposable copy (exact head plus the F1 re-pin), I appended each form to `sw/litex/flash_map.py`, which is reached and undeclared.
- `--write` returns rc 0 with tools and residue unchanged, for PYW1, PYW2, PYW4 and PYW6 (`receipts/py-write-{1,2,4,6}.log`).
- `--check` fails for these forms only because the file's recorded input digest changed, which every edit triggers (`receipts/py-probe-{8,18}.log`).
- Assembled-string forms (`getattr(os, "sys"+"tem")`, `getattr(builtins, "ex"+"ec")`) are recorded as residue, which is acceptable under the ruling (`py-write-{3,5}.log`).
- Fifteen other forms are refused by name (`receipts/py-probe-*.log`): `__import__`, `exec`, `compile`, `from os import system as s`, `importlib.import_module`, `ctypes`, `os.posix_spawnp`, `os.execvp`, `pty`, `asyncio`, `runpy`, `pip`, `socket`, `webbrowser` and `os.popen`.

**Impact:** an installer call in a reached, undeclared module passes generation, and the regenerated inventory passes comparison. These are literal forms, not runtime assembly.

**Required outcome:** subscripting `sys.modules` or a module `__dict__`, and attribute access to executing builtins through `builtins`, are detected as capability (requiring a declaration), or refused by name. Each needs a control.

**Verification:**

- PYW1, PYW2, PYW4 and PYW6 refuse as undeclared executing scripts, or by name.
- The current tree's inventory is unchanged.

### R638-6-F4 MAJOR: the execution audit judges only the kernel's interpreter binary, so scripted installers and unlisted scripts pass

**Lenses:** Conformance, Robustness, Tests, Docs.

**Where:**

- `ci/image/exec_audit.py:97-99`: the program is `readlink /proc/<pid>/exe`. For a shebang script that is the interpreter. Only the first argv per program is kept.
- `ci/image/exec_audit.py:120-133` (`judge`): the installer denylist and the system-root rule apply to that basename only.
- `ci/image/exec-audit.json`: `pip`, `pip3`, `npm`, `npx`, `poetry`, `uv` and others are denylisted, but in the image `pip`, `pip3`, `npm` and `npx` are scripts (`/opt/python/bin/pip3`, `/opt/node/bin/npm`).
- `docs/testing/CI_IMAGE.md:215-221`.

**Authority:**

- Class ruling item 2: "Fail when a program is not in the command table, a package manager or installer is executed, or a step needs the network".
- A hidden installer in a future PR must be caught at that PR's replay.
- The workflows themselves install with `python3 -m pip install`.

**Evidence:** `receipts/audit-selftest-and-controls.log` and `receipts/audit-controls-receipt.json` record an in-image run with `--network none`:

- **The author's `--selftest` passes.**
- **Static binaries are observed:**
  - C1 records the job-built static binary `/tmp/zz_static_probe`.
  - C2 catches a static binary planted in `/usr/local/bin` by name.
- **The network check works:** C7 is caught by its exit status.
- **These run clean with no finding:**
  - C3: `pip3 --version`, seen only as `python3.12`.
  - C4: an offline `python3 -m pip install --no-index --target … local.whl`, which succeeded ("Successfully installed zz-probe-pkg-0.1").
  - C5: `npm --version`, seen only as `node`.
  - C6: an unlisted shebang script planted in `/usr/local/bin`.
- The planted-installer control in the selftest uses an ELF copy named `apt-get`, the one shape the judge can see.

**Impact:**

- The audit is the declared execution authority for the follow-up replay. It cannot name the repository's most likely installer, pip run offline from in-tree wheels or `--find-links`, or any scripted tool.
- The "a system program must be named" guarantee does not hold for scripts.

**Required outcome:**

- Judge each exec by the file that `execve` named, including the script path for interpreter execs, and by interpreter module or script arguments (for example `python3 -m pip`).
- Apply the allowlist and denylist to those names.
- Record every distinct argv rather than only the first per binary.
- Document the receipt's output fields as the follow-up interface.
- Controls: scripted `pip3`/`npm`, `python3 -m pip install` offline, and an unlisted shebang script in a system directory, each caught by name.

**Verification:** the C3-C6 controls are rejected by name in the image with `--network none`, and the selftest and the C1, C2 and C7 controls still pass.

### R638-6-F5 MAJOR: the current-tree audit receipt does not cover the reached step sets and is not committed

**Lenses:** Conformance, Tests.

**Where:**

- There is no receipt in the tree (`git diff --name-only fa7347fc..6918d4f9`).
- The public author receipt `review-evidence/737-image-r1/author-r6/round6-exec-audit-receipt.json` has 9 steps:
  - a g++ setup;
  - `verilator --version`, `yosys -V`, `sv2v --version` and `behave --version`;
  - four self-tests.

**Authority:** class ruling item 2:

- "Run every inventory-reached docs-check and rtl-fast step inside the image with `--network none`. Record the executed program set per job and step."
- "Commit the audit tool, its controls … and the current-tree receipt."

**Evidence:**

- The docs-check job has about 45 run steps, and rtl-fast has 12 jobs.
- The 79 + 36 commands in `round6-docs-gate-results.json` ran without the audit, so their program sets are unrecorded.
- My own audited run of 7 real steps across docs-check, verilator-lint and firmware-unit is clean (`receipts/audit-steps-receipt.json`). This supports the tool but does not substitute for the ruled receipt.

**Impact:** the ruled observed-execution baseline for the current tree does not exist. The allowlist has not been shown to cover what the reached steps actually execute, so the follow-up replay starts from an unmeasured allowlist.

**Required outcome:**

- A committed current-tree receipt for every inventory-reached docs-check and rtl-fast step, run under the audit in the image with `--network none`, with per-job and per-step program sets and no findings.
- Install-only steps that the image replaces are named as such.

**Verification:** the receipt lists every reached step label, and `clean: true` holds under the F4-corrected judge.

### RESIDUE

R638-6-RES1 (Docs, wording only), `docs/testing/CI_IMAGE.md:529-530`. The text "Create the link in a fresh job home. An existing destination must already resolve to `/opt/rv32-sdk`." implies that an existing correct link is accepted. The documented `ln -s` fails on any existing destination: a second run in the image returns rc 1 (`receipts/rv32-adoption-sequence-rc.log`).

Exact fix: replace the second sentence with "The `ln -s` step fails if the destination exists, so it runs only in a fresh job home."

### Observation (no severity)

At `4391f353` the RV32 tool record listed the docs-check provenance entry "Install and verify the pinned RV32 SDK" twice. At this head it is listed once. The tools, pins and the set of provenance entries for all 45 records are otherwise identical.

## Round-six items, judged against the ruling

| Item | Result | Evidence |
|---|---|---|
| (1) exact semantics, refuse by name | **Fails (F2, F3).** Every R638-5 and R639-5 form is refused. | `receipts/probes-replay-walker.json`; F2/F3 receipts |
| (2) live gap | **Holds**, except for F1 at the exact head. `run.py` is reached and declared (`command-table.json`; inventory inputs `tb/verilator/nvm_capture_cpu/{run,soc,probe,firmware}.py`). No allowance names an in-tree module: only `litex.*` matches `sw/litex` and `docs/litex`, which are namespace directories that no reached path places at the import root. Appended pip, `urllib` and `os.system` to `run.py`/`flash_map.py`, and stdlib-shadowing `shlex.py`/`recipe.py` beside `run.py`, are refused by name. | `receipts/live-gap-*.log` |
| (3) ptrace audit | **Partial (F4, F5).** The selftest passes. The planted ELF installer and the unlisted ELF are caught by name. A static binary is observed. My 7-step, 3-job audit is clean offline. The spec interface (`job`, `label`, `argv`, `working-directory`, `env`) is documented. | `receipts/audit-*` |
| (4) RV32 adoption | **Holds.** The documented sequence returns rc 0 in a fresh home. `fw_rv32_selftest.py --require-rv32` and `test_ctrl_nvm.py --require-rv32` return rc 0 offline. | `receipts/rv32-adoption.log`, `rv32-adoption-sequence-rc.log` |
| (5) records and digest | **Holds.** The 45 tool records are unchanged. The image digest is unchanged. The local export authenticates at this head. The two cold records agree with the lock. | `receipts/verify-archive-exact-head.log`, `image-export.sha256` |

## Prior findings reconciliation (read after the independent pass)

| Prior finding | Status at this head |
|---|---|
| R638-5-F1 (local modules hidden by allowlist) | **Closed:** P1/P2 equivalents refused; `run.py` declared; no in-tree allowance. A new and distinct capability-detection cause is filed as F3. |
| R638-5-F2 (P3b, P6b, P4, P5) | **Listed forms closed:** all refused by name. The cause class (accepted Make forms mis-resolved) is **retained as F2** with new instances. |
| R638-5-F3 (P7 redirected `pwd`) | **Listed form closed:** refused ("unresolved shell cd"). The cause class (exact substitution shapes) is **retained as F2** (S1, S3, S5, S6, M21). |
| R638-5-F4 (RV32 adoption) | **Closed:** sequence and consumers rc 0. Wording residue RES1. |
| R639-5-F1 (`make_target_override`) | **Closed:** refused by name. |
| R639-5-F2 (traversal-cache pair) | **Closed:** both refused at the sentinel. |
| R638-1..4, R639-1..4 | Reconciled in R638-5 and R639-5 as closed, or retained into the round-five findings above. No earlier finding is reopened. The walker cause class stays open as F2/F3. |

Manager rulings from earlier rounds:

- (a) mf48 NOT RUN, and (c) `MAKEFLAGS += -e` parity: unchanged since round five; not re-litigated.
- (d) no workflow file changed: verified.

## Other checks at this head

- **Self-tests.**
  - On the host: the walker self-tests (inventory, patterns, nodes, exact) and `build`, `integrity`, `privacy` and `privacy_patch` all return rc 0 (`receipts/host-*.log`).
  - In the image: the exact self-test returns rc 0, and `make_builtins.py --check` passes ("GNU Make 4.3 built-in rules and default variables recorded").
- **Lock and identity.**
  - `build.py --check-lock` passes, and `recipe_digest()` is `54cd38de…`, equal to the lock.
  - The image-context inputs are unchanged since `4391f353` (Dockerfile, install, sources, smoke, normalize, sbt repositories, RV32 installer, patches).
  - `--check-lock --verify-archive` on my export of `sha256:86d7aa16…`, with all 665 artifacts fetched and verified and the base export authenticated, prints "PASS: image identity verified against exported manifest, config and every layer".
- **Privacy.** History (27 entries), environment and labels contain no account, host, home, project-private path or credential (`receipts/image-history.txt`, `image-config.txt`, `privacy-report.json`, with 526 authenticated upstream allowances).
- **Smoke.** The offline smoke checks pass ("PASS: all image tool families", `receipts/smoke-offline.log`).
- **Hosted contexts at the exact head** (`receipts/hosted-exact-head-check-runs.tsv`), read only:
  - 21 success, including docs-check, verilator-lint, rtl-fast, publication-census, all firmware jobs and the Yosys shards;
  - "Physical gPTP" skipped;
  - elaborate and Verilator shards 0, 1, 2, 3 and 5 still in progress when read.

  The manager owns hosted and act acceptance.

## Reviewer-owned ledger

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1, F2, F3, F4, F5) | ruling 6177332782 items 1-4; `ci/image/command-table.json:13060`; `scripts/ci_make_walk.py:190,313,345,512`; `scripts/ci_shell_walk.py:99-127`; `scripts/ci_command_table.py:426-445`; `ci/image/exec_audit.py:97-133`; `receipts/probes-*`, `receipts/audit-*` | R638-6 | 6918d4f9bee7081a71f94d9090d01c557085658a |
| RTL | CLEAN | `ci/image/Dockerfile` stages and layer map (unchanged since 4391f353), `ci/image/image.lock.json` 14-layer binding, `receipts/verify-archive-exact-head.log`, `receipts/smoke-offline.log` (Verilator, Yosys, sv2v, RV32 offline), `receipts/audit-steps-receipt.json` (pp_srcs derived-source step rc 0), `receipts/restore-check.txt` (no HDL/gitlink change) | R638-6 | 6918d4f9bee7081a71f94d9090d01c557085658a |
| Robustness | UNCLEAN (F2, F3, F4) | 64 own walker, Python and live-gap probes and 7 audit controls (`receipts/probes-*`, `py-*`, `audit-controls-receipt.json`) compared with Make 4.3, bash 5.2 and CPython 3.12.3 in the image | R638-6 | 6918d4f9bee7081a71f94d9090d01c557085658a |
| Tests | UNCLEAN (F1, F2, F3, F4, F5) | `scripts/ci_inventory_exact_selftest.py` (no control for F2 forms); `ci/image/exec_audit.py` selftest (ELF-only installer control); `receipts/host-*.log`; `receipts/image-inventory-check-exact-head.log`; author `round6-exec-audit-receipt.json` (9 steps) | R638-6 | 6918d4f9bee7081a71f94d9090d01c557085658a |
| Docs | UNCLEAN (F1, F2, F3, F4) | `docs/testing/CI_IMAGE.md:99,108,136-137,215-221,283,292,505-532`; `docs/README.md`; READY 6183149185 claims | R638-6 | 6918d4f9bee7081a71f94d9090d01c557085658a |

[R638] PASS RTL — `ci/image/Dockerfile`, `ci/image/image.lock.json`, `receipts/verify-archive-exact-head.log`, `receipts/smoke-offline.log` — The multi-stage, one-layer-per-tool recipe is unchanged since round five and still digest-pinned. The exported image authenticates against all 14 locked layers at this head. Verilator, Yosys, sv2v and the RV32 SDK work offline in it. The derived protocol-processor source-list step passes in the image. No product RTL, interface or gitlink is changed.

## Real limits

- **No cold rebuild by me.**
  - Docker buildx is not installed for this account.
  - The image-context inputs are unchanged since round five.
  - Reproducibility rests on authenticating my own export against the lock, and on the author's two public cold records, both of which equal the lock.
- **Full step sets not run.** I did not run the full docs-check or rtl-fast step sets, nor the builder bank, which is prohibited. The audit ran on 7 real steps across 3 jobs, and the RV32 consumers ran in full.
- **Docker use** was limited to the focus allowance:
  - offline (`--network none`) runs of the PR's own locked image on disposable copies;
  - `image save` of the locked image and the pinned base, both already local.

  There was no pull, push, login or build.
- **Disposable copy for some probes.** The Python probes and live-gap controls ran in a disposable copy carrying the two-hash F1 re-pin, because the exact head refuses before any walking. Every other probe ran against the exact-head scripts.
- **Clone state.** Host Python created two `__pycache__` directories in the clone during my runs, and I removed them. The clone is byte-identical to the head:
  - 1352 tracked blobs match by hash;
  - the index tree equals `cf35c3b9…`;
  - worktree and index are clean;
  - all six gitlinks are unchanged (`receipts/restore-check.txt`).

## Pending manager duties

- Current-dev merge-candidate builder and native banks, and their receipts.
- Hosted and act acceptance at the final head, including the in-progress elaborate and Verilator shards.
- Registry publication and a digest round-trip check after a POSITIVE pair.
- RES1 on the residue checklist.
- Completion of both independent reviews.

R638-6 FINISHED
