[A583] REVIEW READY

Round 11 for PR #705 ([assignment](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6113306444)), answering R584-9 and R585-9. Two new commits on `be607527`, no rebase or amend; not pushed.

Commit: `aca5e8afc58a12ca050cd4c4c5f1c7c02c9ff783`

Changed:
- `d32ceac87` (R584-9-F1 / R585-9-F1). The guarantee moves to run time.
  - **Install.** `ctrl_build.audited` decorates the helper (`@audited def git`). It installs a PEP 578 audit hook when the helper is defined, before the proof's first Git call, and the hook stays for the life of the process.
  - **What it binds.** At install it binds everything it judges by:
    - the helper's own code object and `ctrl_build`'s namespace;
    - the Git program `PATH` names when the module loads (`ctrl_build.GIT`). The helper now starts it by that path; argv is unchanged.
    - every function, builtin and constant it uses.

    So rebinding a name later does not change how it judges an event. This includes a builtin's name rebound in the module.
  - **Launches.** While the proof runs (a function of `stack_gitlink`, `stack_pin`, `main` in any thread, or one of the two modules' top level), every launch event the interpreter raises is refused, and so is every thread start. The one exception is the `subprocess` module starting the Git program as a string, for the helper's own code, with a plain environment that sets `GIT_NO_REPLACE_OBJECTS=1` and gives `GIT_GRAFT_FILE` an absolute path under a file.
  - **Dynamic code.** `exec`, `compile`, an import of `importlib`, and the reaches into the hook's own state (`gc.get_objects` and kin, `sys.settrace`, `sys.setprofile`) are refused:
    - wherever the proof's own code asks for them, the helper included;
    - while the pin is decided, whoever issues them.
  - **Replacement.** A proof function's `__code__` or defaults cannot be replaced, at any time.
  - **Refusals.** Each refusal is written to standard error first, then raised as an `AuditRefusal`, which is a `Refusal` (exit 2). It names the proof's line.
  - **The census** stays as a fast lint, now also refusing dynamic code as an attribute (`inspect.builtins.exec`) and inside the helper. It runs the proof from its texts under the hook in a fresh interpreter (`ctrl_pin.exercised`) and reports each refusal at its line.
  - **Docs.** README, docstrings and PR body attribute the guarantee to the hook and state the scope.
- `aca5e8afc`. Two fixes found on self-review, after the first replicas started; those were stopped and rerun here.
  - The hook knew `ctrl_pin.py`'s code only through its `sys.audit(PROOF_EVENT)` registration, which a plant rebinding `sys.audit` first would skip. It now also knows the proof's code by its two files, fixed at install. The registration still covers a copy run under another name, which is R585-9's probe.
  - Each of the hook's 17 rules now has a control that only it refuses. Deleting any one rule makes at least one control escape, on CPython 3.12.3 and on 3.14.7.
  - The stated scope now spells out the CPython 3.12.3 limit (open risks).

Standing controls. 30 controls, each the proof run under the hook with one bypass planted, each ending before any build in the hook's named refusal at a line of the plant. Five cannot name a line of the plant: they are refused for the program, the setting, or the filename the plant gave its code.
- **The five earlier controls:** computed name, dashed program, aliased import, `os.system`, `exec` of a string. Round 9's runner and two environment controls are kept.
- **R584-9's escapes:** the helper's name rebound by attribute assignment in each module (E2b, E6), and `os.walk` rebound (E7).
- **R585-9's escapes:** `inspect.builtins.exec`, `eval` and `compile`; `pkgutil.importlib.import_module`; and `exec`, `eval` and `compile` inside the helper.
- **One per further rule:**
  - the Git program by its path with the helper's environment;
  - a refusal caught and ignored;
  - a library's `eval` while deciding (`collections.namedtuple`);
  - code filed under another name (`code.replace`);
  - an import of `importlib.metadata`;
  - the registration skipped by rebinding `sys.audit`;
  - a thread start;
  - `stack_pin.__code__` replaced;
  - `gc.get_objects`;
  - `sys.settrace`;
  - the Git program rebound;
  - the environment with `type`, `dict`, `isinstance` and `any` rebound in the module.

The unmodified proof passes as a control of its own. That makes 58 pin controls, up from 35. The README's figure moves with them, and the figure check holds it.

Validation. CI-parity means Ubuntu 24.04, its CPython 3.12.3, gcc 13.3, GNU make 4.3 under `MAKEFLAGS=w`, GoogleTest 1.14.0, clang 18 and cmake 3.28, on four CPUs, in fresh clones at `aca5e8af`.
- `firmware-boundary`'s step: PASS in 671 s (37 % of 30 min, beside two other containers). 2822 compiled sources of 3053, 0 findings; 105 boundary, 58 pin and 4 figure controls, 0 misbehaved.
- `firmware-verilator`'s step: PASS in 481 s (20 % of 40 min). 816 of 916, 0 findings; 6 boundary, 58 pin and 4 figure controls, 0 misbehaved.
- `firmware-unit`'s steps: every step rc 0, 1974 s (73 % of 45 min, beside the two other replicas).
  - The firmware gate's 845 verdict lines are byte-identical to rounds 4 to 10 (`mutants: 471 of 471 caught`). Its process installs the hook when it imports `ctrl_build`, and builds and runs exactly as before.
  - The store passed 435 tests; the coverage self-test caught 29 of 29; `fw_coverage.py --check` PASS (30 files), the table identical.
- The docs job's 54 commands: all rc 0, including `check_py_idiom.py` (every ratchet held), `check_em_dash.py --base be607527` (36 added lines, 0 findings), `docs_check.py`, `ci_events.py --check` and `--selftest`, and `ci_scope.py --selftest`.
- Images: 35 of 35 ELF hashes are identical to round 10 and dev `aef7ac66` (manifest sha256 `de8ae063…`).
- Make's readings of every Makefile builder are byte-identical to `be607527`'s. Every non-hook pin control prints the same verdict line as at `be607527`.
- The reviewers' probes ran unmodified at the head (their scripts' sha256 equal to their manifests). Each ends in the runtime refusal:
  - R585-9's `census_matrix.py`: `88 cases, 88 passed, 0 escaped`. These are its 66 forms plus the 30 controls.
    - Of its 13 escapes at `be607527`, 9 now end in the hook's refusal.
    - The other 4 end in the lint's: `pkgutil.importlib` with nothing started, and `__import__` and `import importlib` in the helper. An import of a module already loaded raises no audit event, so the hook cannot see them alone.
  - R585-9's `dynamic_launch_probe.py`: the planted copy, run as a script, is refused at its `inspect.builtins.exec` line (`the pin proof's audit hook refused: …:922 asks for compile in the pin proof`) and exits 1. So the probe's assertion that the child ran fails; the child never ran.
  - R584-9's rebinding probe (`make_rebind_mutants.py`, `rebind_runtime_probe.py`):
    - E1b, E2b, E6 and E7 each give `<file>:<adapter's line> starts git (subprocess.Popen) while the pin proof runs, not by the helper`, in the census and from `stack_pin()`, which raises `AuditRefusal`.
    - The clean copy reports 0 runner starts.
  - R585-8's `census_probe.py` and R584-8's twelve mutants also end in the hook's refusal or their own control's.
    - M8 to M11 are refused at their own lines.
    - M5 passes, as before.
    - Run all together, R584-8's in-place edits reuse a stale `.pyc`, so each mutant was run alone.
- Every entry point: 85 of 85 refused, naming the changed file.

Acceptance criteria: unchanged and met. The pin, the RV32 images (byte-identical), the boundary with its planted controls, coverage and every campaign's kills are as before. The launch route of the pin proof is held at run time by the hook, with the scope stated.

Open risks/questions:
- **The CPython 3.12.3 limit.** It falls within the ruling's native-code limit, but it is material on the hosted interpreter.
  - On CPython 3.12.3, `_posixsubprocess.fork_exec` raises no audit event. `subprocess` and `multiprocessing` call it.
  - `subprocess` raises its own event from Python just before that call. So code that calls `fork_exec` itself, or rebinds `sys.audit`, starts a process the hook never sees there. `scripts/limit_probe.py` shows this: `[]` on 3.12.3, refused as `_posixsubprocess.fork_exec` on 3.14.7.
  - Guarding `sys.audit` alone was tried. It would not close the route, because `fork_exec` stays reachable directly.
  - CPython 3.14 audits `fork_exec` itself. Moving the hosted job's Python to 3.14 is a CI change outside this lane.
- **Replacing the decision.** The hook judges the decision `ctrl_build.py` defines. Replacing the decision's code is refused, but a gate that called another function bound in `stack_pin`'s name would not be running it. Every gate imports `stack_pin` by name when it loads.
- **The helper's environment (pre-existing since round 9; outside this assignment and not raised by a review).** The helper's environment is the caller's plus the two settings. So a Git variable the caller sets (`GIT_DIR`, `GIT_INDEX_FILE`, `GIT_CONFIG_*`) reaches Git. Noted for an Issue if wanted.
- **Limits stated in the docs:**
  - what Git itself starts;
  - code above the helper in `ctrl_build.py`, which runs before the hook is installed;
  - processes the two modules start while the proof is not running: the build functions, `run`, and `ctrl_pin.py`'s tool runs.
- **Suggestions and residue.** R584-9-S1 (the lint's `IndexError`) and S2 are optional and not taken. The residue items go to #495: R584-8-RES-1, R585-8-RS1, R584-7-RES1 / R585-7-RS1, and R585-9's RES-1 wording.
- **Headroom.** `firmware-unit`'s headroom is #716's.

Evidence: `HANDOFF.md`, Round 11 (commits, the hook's file:line table, the limit, the self-review, the control table and the hook-rule campaign, probes, gates), with logs and scripts under `round11/` in the author packet.
