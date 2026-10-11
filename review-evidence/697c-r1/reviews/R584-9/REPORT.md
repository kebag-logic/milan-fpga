[R584] NEGATIVE - exact head be607527eaac84cfc8d7456167b070a22228345b

Internal independent review R584-9 of issue #697 / PR #705, round 10 delta (two commits on `feed95bb`: `65115fce`, `be607527`). Tree `0ff64b4d0d26c7d6d737802cafacf3fde3356f04`. All five lenses applied. One MINOR finding is open (F1), under Conformance, Robustness, Tests and Docs. Two SUGGESTIONs are recorded. RTL is clean.

Read in order: AGENTS.md and CONTRIBUTING.md; the issue body and its manager comments up to the round-10 ruling ([6112358746](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6112358746)) and REVIEW READY ([6113121913](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6113121913)); `git diff feed95bb..be607527` (4 files) and the PR's whole-range scope against `8b61b709`; then the PR body at this head. The prior public findings (R584-8, R585-8) and their probes were read only after the independent pass below, and then replayed. No private author material and no parallel review report was read.

## Findings

### R584-9-F1 - MINOR - Conformance, Robustness, Tests, Docs - the census does not see the helper's name, or a vocabulary name, rebound by attribute assignment inside the proof's own modules, so the pin decision can start every Git process through the harness's runner with every check green

- **Where:**
  - `sw/firmware/ctrl/test/ctrl_pin.py:189-215` (`scope`). It records only module-level statements that bind a plain name.
  - `ctrl_pin.py:224-251` (`launches`). An attribute store (`X.git = ...`, `os.walk = ...`) is not a reference it refuses.
  - `ctrl_pin.py:262-264` (`judge`). A `def` named after the helper is never followed.
  - `ctrl_pin.py:327-334`. The "bound again" check reads `scope` only.
- **Claims it falsifies:**
  - `sw/firmware/ctrl/README.md:181`: "So the decision reaches no process but through the helper, whatever the route or the name of the program".
  - `README.md:182`: "the census also refuses ... `ctrl_build.py` ... with its name bound again".
  - The stated limit at `README.md:186` covers only "code *elsewhere* that rebinds their names".
  - The docstring at `ctrl_pin.py:32-36` ("by any route or name") and at `:42-43` (the same "elsewhere" limit).
  - The PR body Status: "the decision reaches no process but through the helper, by any route". Round 10 item 1 says the same ("whatever the route").
  - The round-10 ruling, "launch route by construction".
- **Evidence** (`scripts/make_rebind_mutants.py`, `scripts/rebind_runtime_probe.py`, receipts `05_*`, `06_*`, `07_*`, `13_*`):
  - Each mutant keeps the helper's environment (`git_env()`), so the pin's verdicts are unchanged and only the launch route moves.
  - **E2b**, in `ctrl_build.py` itself: an adapter function is set as `ctrl_build.git` through `import ctrl_build`, with its `__name__` set to `"git"` (`__name__` is the one dunder the census allows).
    - Census: `[]`, both statically and when imported live.
    - Pin controls (all but the Makefile bench arms): 29 of 29 `[ok]`.
    - `check_py_idiom.py`: rc 0.
    - At run time `stack_pin()` started all 5 of its Git processes through `fw_gtest.run`, the runner that the census says is refused where the pin is decided.
  - **E6**, in `ctrl_pin.py`: `ctrl_build.git = plain` at the end of the module.
    - Census `[]`, controls 29 of 29 `[ok]`, code-quality gate rc 0.
    - The boundary gate imports `ctrl_pin` before its own `stack_pin()` at `ctrl_boundary.py:489`. That call then made 5 runner starts.
  - **E7**, in `ctrl_build.py`: `os.walk`, a vocabulary name, is rebound to a function that starts `git status` through the runner and then walks.
    - Census `[]`, controls 29 of 29 `[ok]`, code-quality gate rc 0.
    - `stack_pin()` started a process outside the helper.
  - Two forms are caught, but by something other than the census:
    - **E1b** (`global git` and a nested `def git` in a function run at import): census `[]` and controls `[ok]`, but the code-quality gate's `global statement` ratchet refuses it.
    - **E1** (a plain `global git; git = plain`): the census `[]` on the text, but it is caught at run time, because `HELPER = git.__name__` (`ctrl_pin.py:96`) reads the live object (`04_runtime_E1.txt`).
  - Control: the clean head copy has census `[]`, 0 runner starts during `stack_pin()`, and controls `[ok]` (`03_runtime_clean.txt`, `07_controls_tree.txt`).
- **Impact:**
  - No such code exists at this head. The pin check is not weakened today, and an env-dropping rebinding in a module the controls' process imports would still fail the replacement controls.
  - But the round's "by construction" guarantee does not hold. A rebinding written in the proof's own modules moves the decision's launches off the helper, past the census and every standing gate. Neither the README, the docstring nor the PR body states this limit.
  - Same class and same severity rule as R584-8-F1 and R585-8-F1: a census escape with no present defect.
- **Required outcome:** one of the following.
  - The census refuses, in both pin-proof modules, a store that rebinds the helper's name or any vocabulary name used by the decision. That includes a `global`/`nonlocal` declaration of a module name, a store to an attribute of a module object (a self-import of `ctrl_build`, or `os.walk = ...`), and an attribute store whose name is the helper's. A standing census control plants an E2b- or E6-shaped rebinding and must be refused by name at its line.
  - Or, if the manager rules this out of scope: `README.md:181-182,186`, `ctrl_pin.py:32-36,42-43`, the PR body's Status and Round 10 item 1 state that a rebinding by assignment inside the proof's modules is not seen, and drop "by any route" / "whatever the route".
- **Verification:**
  - For `E2b`, `E6` and `E7`, run `python3 -I scripts/make_rebind_mutants.py <copy> <form>` and then `python3 -I scripts/rebind_runtime_probe.py <copy>`. The census line must name the planted line.
  - The new census control is `[ok]` under `ctrl_boundary.py --selftest`, and the README's pin-control figure moves with it (the figure check holds it).

### R584-9-S1 - SUGGESTION - Robustness - `ctrl_pin.py:332-333`: the census raises `IndexError` when the helper's name is bound only by assignment

- **Evidence:** `ctrl_build.py` with `def git(` renamed `def git_run(` and `git = git_run` added. `census()` raises `IndexError: list index out of range` (`defs[0]` with no `def`) instead of a named finding (`16_helper_value_only_probe.txt`).
- **Impact:** None on the verdict. The boundary gate fails closed with a traceback.
- **Suggested outcome:** When there is no `def`, report each binding as "binds the helper's name again" without indexing.

### R584-9-S2 - SUGGESTION - Robustness, Docs - process starts outside the listed facilities are not refused module-wide

- **Evidence:** Four forms are not named outside the decision (`14_module_wide_forms.txt`):
  - `multiprocessing`;
  - `concurrent.futures.ProcessPoolExecutor`;
  - `_posixsubprocess.fork_exec`;
  - a C library's `system` by subscript (`ctypes.CDLL(None)["system"]`).
- **Why not a finding:** This is within the stated limit ("a route of Python's own ... that none of the refused names opens", `README.md:186`), and inside the decision these names are refused by the vocabulary.
- **Suggested outcome:** Optionally add them to `LAUNCH_NAMES`/`DYNAMIC`, or name them in the limit.

## What was confirmed at this head (clean for the assigned items)

| Assigned item | Result | Evidence |
|---|---|---|
| Only the helper names a facility | Of the two modules, only `ctrl_build.git` (`ctrl_build.py:197-204`) names `subprocess`, imported in its own body. The module-level `import subprocess` is gone. Other mentions are strings or docstrings. | `git diff feed95bb..HEAD`; `rg` over both modules; clean census `[]` (`01`, `11`) |
| Facilities refused module-wide, in both modules, by import, alias or attribute | 46 of 46 planted forms behave as expected. All 19 listed forms are named at their line in each module, among them: an aliased `os` with `.system`; `from os import posix_spawnp as ps` and `execv`; `pty`; `asyncio.subprocess as asp`; `create_subprocess_shell as c`, and the `create_subprocess_exec` attribute; `os.fork` and `os.popen`; `shutil.os.spawnl`. The four forms outside the list are unseen, as stated (S2). | `scripts/module_wide_forms.py`, `14_module_wide_forms.txt` |
| `eval`/`exec`/`compile`/`__import__`/`importlib` refused | Each is named at its line (and so are `builtins`, `getattr` with a computed name, `vars()[...]`, a dunder attribute and a wildcard import). | `14_module_wide_forms.txt` |
| Five standing controls, refused by name, with the clean proof passing | All 8 census controls are refused at their planted line: computed name `git.__name__` and dashed `git-ls-tree` at `ctrl_build.py:260 stack_pin names run`; aliased import at `:260 imports subprocess.run as r`; `os.system` at `ctrl_pin.py:745`; `exec` at `ctrl_build.py:210`; the runner form; and both environment settings by name. Clean census `[]`. | `01_census_escape_probe.txt` |
| R585-8 `census_probe.py` (sha256 `0cc5e43f...`, matching its manifest) | Exit 1, `AssertionError: Probe no longer reproduces the census escape`. The census names `ctrl_build.py:260`. The original proof refuses the replacement tree. | `09_R585-8_census_probe_at_head.txt` |
| R584-8 `proof_mutants.py` (sha256 `e93fd950...`), M8 and M11 | M8: the census names `ctrl_build.py:260 stack_pin names run`. M11: it names `ctrl_build.py:210 stack_gitlink names run`. M1-M4, M5b, M6, M7 and M10 are each caught by their own control or the census. M5 passes every control, as R584-8 tabled (caught by type). A census control whose anchor a mutant replaced reports its anchor missing, by name. | `10_R584-8_proof_mutants_at_head.txt` |
| Pin controls and figures | 35 of 35 pin controls `[ok]`, the mailbox bench's Makefile arms included. Population 96 / 8 / 5 / 35. README figure findings `[]`; 4 of 4 figure controls `[ok]`. Makefile findings `[]`. | `scripts/pin_and_figures.py`, `11_pin_controls_figures_full.txt` |
| No image byte changed | The delta touches no C, header, linker script, Makefile or image builder. `ctrl_build.run` is now `fw_gtest.run` itself; every call in its five importing modules fits the old `(argv, cwd)` signature, so behaviour is unchanged. Images were not relinked here (see limits). | `15_delta_scope.txt`, `19_run_alias_calls.txt` |
| README, docstring and PR body state the contract and limits | They state the enforced list and the "another module's function" limit. The "by any route" claim and the "elsewhere" limit are wrong under F1. | F1 |
| Docs gates | `docs_check.py` 0 findings. `check_em_dash.py --base feed95bb`: 0 findings over 19 added lines. `ci_scope.py --selftest` PASS. `check_py_idiom.py` and `--selftest` rc 0, every ratchet held. | `12_docs_gates.txt` |
| Commits | Two one-line commits, no trailers. | `15_delta_scope.txt` |

`ctrl_pin.run` now runs through `fw_gtest.run`, so stdout comes before stderr rather than interleaved, `GTEST_*` is dropped, and a missing program is rc 127. Every arm's verdict is unchanged in the full 35-control run.

## Prior findings at this head

| IDs | Disposition | Evidence |
|---|---|---|
| R584-8-F1 (dashed program); R585-8-F1 (computed name) | RESOLVED for the reported forms. Both probes now refuse, and standing controls plant both. The ruling's wider "by construction" obligation is not met through another route: new R584-9-F1. | `09`, `10`, `01` |
| R585-8-RS1 (stale "not pushed" in the Status) | Applied in the body: the round-9 paragraph reads "published" and the round-10 Status names no push state. The residue checklist entry (#495) is the manager's. | PR body read 2026-10-11 20:08Z |
| R584-8-S1, S2, S3 | RETAINED SUGGESTIONs, optional, not taken. | Unchanged artifacts |
| R584-8-RES-1; R584-7-RES1 / R585-7-RS1 | RETAINED for the manager's residue checklist (#495). | — |
| R584-7-F1 / R585-7-F1 (replacement objects); R584-6-S2 (mode) | Still RESOLVED: the replacement-tree, replacement-commit, graft, filter and mode controls are `[ok]` at this head. | `11` |
| R584-7-F2 / R585-7-F2 (README 96) | Still RESOLVED: figure check `[]`, 4 of 4 figure controls `[ok]`. | `11` |
| Rounds 1-6 IDs, as dispositioned in R585-8's table | Unchanged: this delta touches only the four pin-proof and README files, none of those artifacts. | `15_delta_scope.txt` |

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1) | Round-10 ruling items against `ctrl_pin.py:93-345`, `ctrl_build.py:100-106,185-204`; both prior probes; 8 standing controls; 46 module-wide forms; rebinding mutants E1-E7 | R584-9 | be607527eaac84cfc8d7456167b070a22228345b |
| RTL | CLEAN | `15_delta_scope.txt`: the delta has no HDL, SystemVerilog, constraint or processor-submodule change; across the whole PR the only gitlink added is `third_party/tsn-c-stack` (C). The mailbox bench's Makefile arms run in the 35 pin controls, `[ok]` (`11`). No clock, reset, CDC or FSM artifact is in scope. | R584-9 | be607527eaac84cfc8d7456167b070a22228345b |
| Robustness | UNCLEAN (F1) | Census escape and runtime probes (`01`, `03`-`07`), helper-value-only probe (`16`, S1), facility-list edge forms (`14`, S2), `ctrl_pin.run` timeout and missing-program paths through `fw_gtest.run` (`fw_gtest.py:110-126`) | R584-9 | be607527eaac84cfc8d7456167b070a22228345b |
| Tests | UNCLEAN (F1) | `CENSUS_PLANTS` and `census_arms` (`ctrl_pin.py:153-169,623-661`); 35 pin controls and 4 figure controls run (`11`); prior mutant suites replayed (`09`, `10`); no standing control covers a rebinding (`07_controls_tree-E2b/E6/E7`) | R584-9 | be607527eaac84cfc8d7456167b070a22228345b |
| Docs | UNCLEAN (F1) | `README.md:166-200`; `ctrl_pin.py:11-43`; `ctrl_boundary.py:78-85`; PR body Status and Round 10; docs gates (`12`) | R584-9 | be607527eaac84cfc8d7456167b070a22228345b |

## Real limits

- **Hosted:** no workflow run and no check run exists at `be607527` as of 2026-10-11 20:14Z (`18_hosted_at_head.txt`). The latest hosted runs on `697-consume` are at `feed95bb` (all success). No hosted evidence at this head is claimed.
- **Gates run here:** The full `firmware-boundary`, `firmware-verilator` and `firmware-unit` gates were not run. The census, the 35 pin controls, the figure check, the Makefile findings and the docs and code-quality gates were run directly, in a disposable copy of the head with tsn-c-stack cloned at `1a9f651c`.
- **Interpreters:** CPython 3.14.7 (the pin controls need `yaml`) and 3.12.13 (census probes). CI uses 3.12.3.
- **Images:** not relinked, because no RV32 toolchain is here. Their equality rests on the delta's scope, the `run` call-shape check, and the author's published 35-of-35 receipt.
- **Verilator:** not used; no RTL is in the delta.
- **Physical calibration:** NOT RUN. Field skips are not hardware proof.
- **Manager source bank:** none at this head, and none is claimed or inferred.

## Pending manager duties

- Rule on F1's alternative if the by-construction refusal is not taken, and obtain re-review of the corrected head.
- Accept hosted and local-replica evidence at the final head (none exists at `be607527` yet).
- Validate the current-dev merge candidate with the builder and native banks: source base `8b61b70902f3ebf118e56967277e2686731081bd`, live dev `cfadd767a7ad47aaee68de655e1066cc000fb8a0`.
- Carry R584-8-RES-1, R585-8-RS1 and R584-7-RES1 / R585-7-RS1 to #495.
- Handle merge authorization, two independent positive reviews, post-merge containment, and issue/project completion.

## Checkout integrity

- The review clone is at exact head with an empty status.
- Index entries (mode, blob, path) equal the HEAD tree: 1272 entries. Every tracked file's bytes hash to its index blob.
- No hidden-index flags and no replace refs.
- The initialised submodules (protocol-processor `2ad2f845`, gptp-processor `5dce647a`, verilog-axis `48ff7a7e`) match their gitlinks and are clean. tsn-c-stack, lwSRP and external are uninitialised in the clone, with gitlinks unchanged.
- Every probe ran on disposable copies under `scratch/`, which is not published (`17_clone_integrity.txt`).

R584-9 FINISHED
