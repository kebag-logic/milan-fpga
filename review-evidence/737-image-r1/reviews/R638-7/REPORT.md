[R638] NEGATIVE - exact head feef7c9fd239ef62b7c6aad301e80a13275e47ef

# R638-7: internal independent review of issue #737 / PR #738, round 7 (delta 6918d4f9..feef7c9f)

Exact head `feef7c9fd239ef62b7c6aad301e80a13275e47ef`, tree `4f1e8d01c600c2bdb5ba5ea6ec64a5d5e7f1b808`, source base `fa7347fc`.
Three MAJOR findings are open: N1, N2 and N3. All five lenses were applied. RTL is CLEAN. Conformance, Robustness, Tests and Docs are UNCLEAN.
Every R638-6 and R639-6 finding named in the round-7 assignment is resolved at this head (table below).
N1 and N2 are residual forms in the same class as the round-6 audit findings F4/F5. N3 is in the same class as round-6 F2/F3. Each is a new form, demonstrated at this head.

## How the review was done

- Context was reconstructed in the required order: AGENTS.md / CONTRIBUTING.md, the #737 issue body and lane assignment (6160953880), the round-7 ruling (PR comment 6183738772), the author's REVIEW READY (6196137082), then `git diff 6918d4f9..feef7c9f` (28 files) and history (`e1c7551ef`..`feef7c9fd`).
- Public author evidence came from `review-evidence/737-image-r1/author-r7` at `d43f00d7`. All 24 round-7 files (HANDOFF, PR-BODY, `round7-*`) match `MANIFEST.json` byte for byte (`receipts/evidence-verification.json`).
- The prior R638-6 and R639-6 findings were read only after the independent pass and the N1-N3 probes.
- No Docker, no image run, no act, no push, no GitHub write. The real-tool side of my probes uses host tools (see Real limits).
- The clone was restored and verified afterwards:
  - HEAD and tree are exact;
  - the worktree and index are clean;
  - the `ls-files -s` and `ls-tree` digests agree;
  - the six gitlinks equal the head's;
  - the bytecode caches my runs created were removed.

## Round-7 items, judged

| Item | Result | Evidence |
|---|---|---|
| (1) Accepted means differentially proven: 177 shapes, 188 fixtures, every R638-6/R639-6 probe a fixture | Mechanism holds. The census gate works. **Not closed**: see N3. | `ci_differential.py --check` rc 0: 188 fixtures, 177 shapes, image `sha256:98a31654…` (`receipts/differential-check.log`). The census-gate self-test rc 0 shows three planted refusals; it also asserts census == tree shapes (`differential-selftest.log`). The receipt holds 131 identical, 52 refused and 5 residue results, each equal to its expectation. All 60 R638-6/R639-6 probe IDs are present. Each is refused by name or resolved identically: M1, M2, M7, M11, M15, M17, M21, S1-S3, S5, S6, S9, S10, PYW1-6 and the R639-6 forms are refused; M3-M6, M8-M10, M12-M14, M16, M18-M20, S4, S7 and S8 resolve identically. The bound tool versions are bash 5.2.21, GNU Make 4.3, dash 0.5.12-6ubuntu5 and CPython 3.12.3. |
| (2) Runtime vs ambiguous values, loop fixed point, function names never builtins | Holds for every in-script form I tried. **Fails** for workflow-environment and filesystem-state forms: see N3. | 50 reviewer walker probes and 28 Python probes through the head's own harness functions, beyond the author's 188 (`probes/walker_probes.py`, `probes/python_probes.py`, `receipts/walker-probes*.jsonl`, `receipts/python-probes.jsonl`). The following were all refused by name or identical: a pipeline-subshell assignment; a function `cd` escape; subshell and pipe `cd`; a prefix assignment on a function; a loop `cd` (refused as ambiguous); MAKEFLAGS, MAKEFILES, BASH_ENV, CDPATH, PATH, PYTHONPATH, IFS and SHELLOPTS, both in-script and as workflow `env:`; `.ONESHELL`, `vpath`, the static-pattern stem and `make -e`; and all 28 Python execution forms (`getoutput`, `pty`, `posix_spawnp`, aliases, `partial`, `map`, threads, `atexit`, `ctypes`, `multiprocessing`, `os.environ['PATH']`, …). |
| (3) Seccomp tracer, full argv, interpreters by program, installers by name/subcommand | The named controls pass. **Inline and streamed Python programs are not judged (N1). Some exec entries are not observed (N2).** | The author's in-image selftest shows 20/20 (`round7-exec-audit-selftest.log`). On the host, the head's audit code catches `-m pip` and a copied unlisted ELF, as positive controls of my probe (`receipts/audit-gaps.jsonl`, 7 JSON rows). |
| (4) `exec-audit-receipt.json`: 94/98 traced, exit 0, zero findings | **Verified, and acceptable.** | Source `afdf0ef0c` (tree `eb1df07b`, base `fa7347fc`; the six submodule lines equal the head's gitlinks). Image `sha256:98a31654…`, users 1000 and 0. 98 reconciliation rows; 94 traced, all `exit_status` 0. Zero findings, `clean: true`, 183,845 instances, 1,969 population rows (provenance split as the author states). All 115 listed commands are observed: 111 with the listed arguments, 4 with the runner's values. `afdf0ef0c..feef7c9fd` changes only the receipt, `audit_population.py` (`<triplet>` spelling) and three doc lines. The head re-trace comparison shows the same step set, reconciliation and commands, 0 material differences, and instance counts in two steps differing by 7 and 1. |
| (4) The 4 untraced steps | **Acceptable.** | `rtl-fast.yml#verilator-lint#3` and `#firmware-verilator#4` ("Build Verilator from source on cache miss"); `#yosys-elaboration#3` and `#publication-census#3` ("Build Yosys from source on cache miss"). Each is gated on a cache miss (`rtl-fast.yml:95`, `:155`, `:270`, `:559`). Each needs apt and a network clone, so it cannot run offline. Each is replaced by a locked image layer at the workflow's pin: `VERILATOR_VERSION: v5.050` and `YOSYS_VERSION: v0.66` (`rtl-fast.yml:18`, `:22`) match the lock rows and the smoke output "Verilator 5.050 … rev v5.050" and "Yosys 0.66". The consuming steps (`firmware-verilator#5` "Put Verilator on PATH and prove the version", the elaboration and census steps) are traced verbatim and exit 0. `merge()` keeps `clean` true only when every untraced row carries a REPLACED reason (`audit_population.py:270-271`). The "79 + 36" in the ruling are the 115 gate commands inside these 98 run steps. Tracing every run step is a superset of what was asked. |
| (5) `check_baremetal_only.py` re-pin | **Resolved.** | The `:433-440` change narrows the `exec_audit.py` mask to the two exact spellings now at `exec_audit.py:84` and `:69`. The declaration `sha256` `3d10365d…` equals the file bytes. My head runs: `--check` rc 0 (1,333 files, 0 findings), `--selftest` rc 0 (738 arms), `ci_tool_inventory.py --check` rc 0, `build.py --prepare-only` rc 0 with recipe `b3fdd900…`, which equals the lock. 45 tool records are identical to `6918d4f9`; 22 residue lines were added, all in declared scripts. |
| Image identity | Verified from receipts. | The two cold builds, `round7-cold-build-{a,b}.receipt.json`, show recipe `b3fdd900…`, image `sha256:98a31654…`, id `a2c4d52a…` and 3,930,997,226 bytes, at 473,918 and 424,315 ms. The chain log shows `--record-lock` PASS on export A and `--check-lock --verify-archive` PASS on export B. `image.lock.json` binds the same recipe and digest. |
| Merge | Clean (read-only check). | `git merge-tree` of the head with live dev `84f9e300` writes a tree with no conflict. 0 files overlap between `fa7347fc..84f9e300` and `fa7347fc..feef7c9f`. Every PR file is under `ci/image/`, `scripts/` or `docs/`. |

## Findings

### R638-7-N1 MAJOR: inline and streamed interpreter programs are never judged, so a real pip install through `python3 -c` or `python3 -` is clean

**Lenses:** Conformance, Robustness, Tests, Docs.

**Where:**

- `ci/image/exec_audit.py:430-435` (`invocation`): `-c` becomes kind `inline` and `-`/stdin becomes kind `stream`, with no program content kept.
- `ci/image/exec_audit.py:483-490` (`judge`):
  - no branch judges an `inline` invocation;
  - a `stream` is refused only when a fetcher (`curl`, `wget`, …) wrote the pipe;
  - `inline` and `stream` always get provenance `named` (`:238-239`).
- The selftest's only inline control is benign (`:635-636`, `python3 -c 'print(1)'`).
- Documentation:
  - `docs/testing/CI_IMAGE.md:311` says "An interpreter is judged by its script, `-m` module, or inline program.";
  - `:398` says "With it, a hidden installer is caught at the replay whatever the walker accepts.";
  - the module docstring (`exec_audit.py:16-17`) and the REVIEW READY say the same.

**Authority:** round-7 ruling item 3: interpreter invocations are "judged by what they run", installers are refused by name, including `pip install`, and the audit is the backstop for what the walker accepts.

**Evidence:** `probes/audit_gaps.py` runs `exec_audit.audit_step` from the head clone. The run uses CPython 3.12.3 with pip on PATH and the head's `exec-audit.json` (`receipts/audit-gaps.jsonl`).

| Case | Exit | Wheel installed | Findings |
|---|---|---|---|
| control: `python3 -m pip install --no-index --no-deps --target … local.whl` | 0 | yes | `installer module executed: pip` |
| `python3 -c "import runpy,sys; sys.argv=['pip','install',…]; runpy.run_module('pip', run_name='__main__')"` | 0 | yes ("Successfully installed zz-probe-pkg-0.1") | **none** |
| `printf '%s\n' "<same program>" \| python3 -` | 0 | yes | **none** |

The population records only `inline python3.12 named` and `stream python3.12 named`. The committed population holds 3,457 inline and 752 stream instances, all accepted this way.

**Impact:**

- The repository's most likely installer, pip run offline from a wheel or `--find-links` content, passes the execution authority clean when it is invoked in-process.
- The docs' "whatever the walker accepts" guarantee is false for a whole class.

**Required outcome:**

- Inline and streamed interpreter programs are judged by what they run, or refused unless declared. For example:
  - pin each inline/stream program text by digest against a reviewed table, as the static walker does for literal inline programs;
  - or detect in-process installer entry points (`pip`, `ensurepip`, `runpy` targets, `pip._internal`) by an import or audit hook in the traced interpreter.
- An unjudged inline or stream program does not yield `clean`.
- `CI_IMAGE.md:311` and `:398` and the docstring state exactly what is judged.

**Verification:**

- New selftest controls: a real local-wheel install through `python3 -c` and through `python3 -` from a non-fetcher pipe, each refused by name in the image with `--network none`.
- `python3 -c 'print(1)'` and the existing 20 controls keep their results.
- The population receipt is re-traced clean.

### R638-7-N2 MAJOR: some exec calls are never observed (foreign-ABI entries and fd/memfd execs), so a copied unlisted program runs with zero findings

**Lenses:** Conformance, Robustness, Tests, Docs.

**Where:**

- `ci/image/exec_audit.py:61-63` (`FILTER`): any syscall whose arch is not `AUDIT_ARCH_X86_64` is `RET_ALLOW`. That includes i386 `int $0x80` `execve` (11) from any x86-64 process. An x32 call (`__X32_SYSCALL_BIT` set, `execve` 520) matches neither 59 nor 322, so it is also allowed. Neither raises a notification.
- `ci/image/exec_audit.py:165-166` (`_executed`): when the named file is not a regular path, the instance is dropped (`return None`) with the comment "The call fails". That includes an `execveat(fd, "", AT_EMPTY_PATH)` on a memfd or deleted file, whose `/proc/<pid>/fd` link is `/memfd:… (deleted)`. The call is then continued and succeeds.
- `docs/testing/CI_IMAGE.md:303` says "Every `execve` and `execveat` becomes a notification the audit reads first.", and `:309` says "Every exec instance is kept …".

**Authority:**

- Round-7 ruling item 3: "It keeps every exec instance with its full argv". A copied unlisted ELF is a ruled negative control, refused by name.

**Evidence:** `receipts/audit-gaps.jsonl`. Each route executes a copy of `/usr/bin/true` that is unlisted and has no provenance. The direct exec of that copy is caught (`program without provenance: zz_hidden`).

| Route | Exit | `zz_hidden` in instances | Findings |
|---|---|---|---|
| `os.execve(memfd, …)` (fexecve) | 0 | no | **none** |
| a job-built launcher calling `int $0x80` `execve` (`probes/compat_exec.c`) | 0 (the launcher returns 99 on failure) | no | **none** (launcher `built by ld`) |
| the same launcher through the x32 entry | 0 | no | **none** |

The host kernel 7.2 has `CONFIG_IA32_EMULATION=y` and `CONFIG_X86_X32_ABI=y`.

**Impact:** the "every exec instance" premise of the audit, and so of the population receipt, does not hold for these entries. A program run through them is neither named nor provenance-checked. This defeats the copied-ELF control by a trivial variant.

**Required outcome:**

- The filter notifies (or kills) on any non-native arch and on any x32-flagged number.
- An exec whose file the audit cannot resolve to a path is recorded and judged by content, or yields a finding. It is never dropped while the call is allowed.
- Docs `:303` and `:309` match.

**Verification:** selftest controls for an i386-entry exec, an x32-entry exec and a memfd fexecve of an unlisted copy, each caught by name in the image. The existing 20 controls are unchanged.

### R638-7-N3 MAJOR: the accepted language is not closed; three forms derive rc 0 with the census gate on while the real tool runs a command the inventory never examined

**Lenses:** Conformance, Robustness, Tests, Docs.

**Where:**

- (a) Workflow `env:` is checked only against a denylist: `scripts/ci_syntax.py:14-19` (`SENSITIVE`) and `scripts/ci_tool_inventory.py:201-202`. No census shape or fixture covers it. An exported-function entry `BASH_FUNC_echo%%: '() { zz_probe …; }'` turns `echo ok` into the hidden command. Bash has imported these since 4.3, and 5.2.21 does too. The walker resolves the builtin. Other behaviour-changing names are absent from the list in the same way, for example:
  - `PERL5OPT`, `NODE_OPTIONS`;
  - `GIT_EXEC_PATH`, `GIT_CONFIG_COUNT`/`_KEY_n`/`_VALUE_n`;
  - `PYTHONUSERBASE`, `PYTHONSTARTUP`, `LD_AUDIT`, `HOME`.
  The in-script `export` and `env NAME=…` channels refuse these names correctly.
- (b) The round-7 certain-test rule decides `cd` from the checkout as it is at walk time: `scripts/ci_shell_walk.py:447-453` (`enterable`) and `:455-470` (`certain`). After an accepted program changes the filesystem, the walker takes the wrong branch. `python3 clean.py` (an undeclared, non-executing `shutil.rmtree('sub')`), then `if cd sub; then :; else cd other; fi; bash run.sh`: the walker follows `sub/run.sh`, while bash runs `other/run.sh`. `cd sub || cd other` behaves the same. The fixtures `bash-if-certain` and `bash-or-certain` (`ci_differential_fixtures.py:85`, `:93`) prove only the unchanged-filesystem case.
- (c) For the same reason, a followed script whose bytes an accepted program rewrote is walked as committed. `python3 gen.py` rewrites `run.sh`, then `bash run.sh`.
- `docs/testing/CI_IMAGE.md:138` says "The accepted language is a closed census of construct shapes."; `:183-184` state the certain-`cd` rule without that precondition.

**Authority:** round-7 ruling items 1 and 2:

- "Any shape without a passing differential fixture is refused by name before generation";
- "Ambiguous state is never a literal".

**Evidence:**

- `receipts/gate-on-env.jsonl` (`probes/gate_on_env.py`) derives the planted workflow exactly as the census-gate self-test does: `ci_tool_inventory.py --root <tree> --write` with the committed tables and differential receipt, gate on.

  | Case | rc |
  |---|---|
  | (a) exported function in `env:` | **0** |
  | (b) certain `cd` after an accepted rmtree | **0** |
  | (c) script rewritten by an accepted program | **0** |
  | control: the same hidden command reached directly | 2, `unclassified command 'zz_probe'` |
  | control: `CDPATH` in `env:` | 2, refused by name |

- The differential outcomes are in `receipts/walker-probes-envfunc.jsonl` and `walker-probes-certain2.jsonl`. Each is `mismatch`: the real tool ran `zz_probe` where the walker resolved nothing, or resolved `sub`. None has an uncensused shape.

**Impact:**

- An accepted, fully literal workflow or step runs a command the inventory never classified, while generation and comparison both pass. This is the class the round-6 and round-7 rulings close.
- Today's tree does not use these forms. The author measured 0 certain branches on the tree. So the 45 records stand, but the gate admits these forms without proof.

**Required outcome:**

- Workflow `env:` names are a closed census: an allowlist of exact names or values with fixtures, and everything else refused by name.
- A `cd` (or test) is certain only when nothing earlier in the job could have changed that path. Otherwise, since the tree never relies on certainty, drop the rule and treat the branch as uncertain.
- The walker's trust in committed bytes of followed scripts is either enforced (refuse a followed script that an earlier reached program could write) or stated in `CI_IMAGE.md` as an explicit boundary that the execution audit backs.
- `CI_IMAGE.md:138` and `:183-184` match.

**Verification:**

- Fixtures for (a), (b) and (c) run in the image: refused by name, or resolved identically.
- `ci_differential.py --check` and the census self-test stay green.
- The 45 tool records are unchanged.

### SUGGESTIONS (non-blocking)

- **S1 (Tests):** `scripts/ci_differential.py:228-229`. `outcome()` returns `residue` when any residue exists, not when the residue's location covers the unresolved real command. I checked the five residue fixtures by hand, and each is correct. Binding residue to the unresolved command's file and line would make the outcome self-checking.
- **S2 (Tests):** `scripts/ci_differential.py:206-208`. Real-tool exit statuses are recorded but never compared. Recording an expected status per fixture would catch a fixture that errors before reaching its sentinel.
- **S3 (Robustness):** `ci/image/exec_audit.py:204`. `f"{base}/{name}"` with a root ending in `/` yields `copy of /sbin//initctl` in the committed receipt. Normalising the joined path would remove the double slash.
- **S4 (Robustness):** `ci/image/exec_audit.py:489`. Installer subcommands are matched on `args[0]` only, so `cargo +toolchain install` and `go -C dir install` escape. They are not used in the tree, and the network is off.

No RESIDUE item. R638-6-RES1 is fixed verbatim at `docs/testing/CI_IMAGE.md:699`.

## Prior findings reconciliation (read after the independent pass)

| Finding | Status at `feef7c9f` | Evidence |
|---|---|---|
| R638-6-F1 / R639-6-F1 (stale bare-metal pin) | Resolved | Pin equals bytes; `--check` and `--prepare-only` rc 0 (item 5). |
| R638-6-F2 (M1-M5, M20, M21, S1, S3, S5, S6) | Resolved | Each is a fixture: M1, M2, M21, S1, S3, S5 and S6 are refused by name; M3, M3b, M4, M5 and M20 resolve the sentinel identically. 45 records are unchanged. |
| R638-6-F3 (PYW1, 2, 4, 6) | Resolved | All PYW1-6 are refused as undeclared executing scripts. 28 further Python forms of mine are all refused. |
| R638-6-F4 / R639-6-F4 (audit judges only the kernel binary) | Resolved for every named control | Scripted `pip3`/`npm`, `-m pip` local wheel, shebang `apt-get`, an unlisted shebang script in a system directory and a copied ELF are each caught. The positives stay clean, and static binaries are observed. The residual forms are new findings N1 and N2, not a reopening. |
| R638-6-F5 / R639-6-F5 (population receipt) | Resolved | Committed receipt, item 4. |
| R639-6-F2 (explicit-target `$*`) | Resolved | Refused: `unmodelled Make explicit-rule stem`. |
| R639-6-F3 (short-circuit, `pwd` shadow) | Resolved | Both refused by name. |
| R638-6-RES1 | Resolved | `CI_IMAGE.md:699`. |

## Clean-lens evidence

[R638] PASS RTL - `git diff --name-only fa7347fc..feef7c9f` (49 files, all under `ci/image/`, `scripts/`, `docs/`; no `.sv`/`.v`, `hdl/`, `tb/` or `syn/` file) - no RTL, CDC, FSM or interface contract is in scope. The diff changes no RTL suite. The traced rtl-fast population ran the lint ratchet, elaboration, publication census and firmware suites at exit 0 in the image (author receipt).

## Reviewer-owned ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (N1, N2, N3) | Round-7 ruling items 1-5 against `ci_differential.py`, `syntax-census.json`, `differential-receipt.json`, `exec_audit.py`, `exec-audit.json`, `audit_population.py`, `exec-audit-receipt.json`, `check_baremetal_only.py:433-440`, `command-table.json` pin, `image.lock.json`, cold-build receipts | R638-7 | feef7c9fd239ef62b7c6aad301e80a13275e47ef |
| RTL | CLEAN | Diff file list (no RTL in scope) | R638-7 | feef7c9fd239ef62b7c6aad301e80a13275e47ef |
| Robustness | UNCLEAN (N1, N2, N3) | `exec_audit.py:61-63`, `:165-166`, `:430-490`; `ci_syntax.py:14-19`; `ci_tool_inventory.py:201`; `ci_shell_walk.py:447-470`; 50 walker, 28 Python and 7 audit probes | R638-7 | feef7c9fd239ef62b7c6aad301e80a13275e47ef |
| Tests | UNCLEAN (N1, N2, N3) | `exec_audit.py --selftest` controls (`:554-649`), `ci_differential_selftest.py`, `ci_differential_fixtures.py` (188), my head runs: differential check, census self-test, inventory check, four walker self-tests, bare-metal check and self-test, `--prepare-only` (all rc 0) | R638-7 | feef7c9fd239ef62b7c6aad301e80a13275e47ef |
| Docs | UNCLEAN (N1, N2, N3) | `docs/testing/CI_IMAGE.md:137-200`, `:298-400`, `:699`; `exec_audit.py` docstring; author REVIEW READY and HANDOFF Round 7 | R638-7 | feef7c9fd239ef62b7c6aad301e80a13275e47ef |

## Real limits

- No image, Docker or act run: this round prohibits them. The real-tool side of my walker probes used host GNU bash 5.3.20, GNU Make 4.4.1 and CPython 3.12.3 (a scratch venv with PyYAML 6.0.1), not the image's bash 5.2.21, Make 4.3 or dash. The behaviours the findings depend on have been stable across those versions: exported-function import, `cd` failing on a removed directory, and a script read at execution time. They were not re-measured in the image.
- The N1/N2 audit probes ran the head's `exec_audit.py` on the host (kernel 7.2), not in the image under Docker's seccomp profile. The judge is pure Python, and the image's pip is importable the same way (`round7-exec-audit-selftest.log`). Docker's default amd64 profile normally admits the x86 and x32 arches, but I did not verify that in the image.
- The step logs behind the population receipt (186.7 MB and 24.4 MB) are not published. Per-instance argv was checked only through the receipt's counts, digests and the author's re-trace comparison.
- The cold-build byte identity and the in-image 188/188 and 20/20 results are taken from the authenticated author receipts and were not re-run.
- `receipts/audit-gaps.jsonl` interleaves pip's own stdout lines with the 7 JSON result rows.
- No manager source bank exists at this head, and none is claimed. Physical calibration was NOT RUN. Field skips are not hardware proof.

## Pending manager duties

- Carry N1, N2 and N3 to the next round. Each needs fixes plus in-image controls and a re-traced population receipt at the new head.
- At the merge turn: validate the current-dev merge candidate (builder and native banks) on live dev `84f9e300`. A read-only `merge-tree` here was clean, with no overlapping files. Also own hosted and act acceptance, distinguishing executed jobs from skipped ones.
- The image push to `docker.io/walkirye/fpga-validation` and its adoption by the workflow lane remain manager-owned.

R638-7 FINISHED
