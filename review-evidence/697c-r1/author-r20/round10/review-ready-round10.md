[A583] REVIEW READY

Round 10 for PR #705 ([assignment](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6112358746)), answering R584-8 and R585-8. Two new commits on `feed95bb`, no rebase or amend; not pushed.

Commit: `be607527eaac84cfc8d7456167b070a22228345b`

Changed:
- `65115fced` (R584-8-F1 / R585-8-F1). The census now holds the launch route, read from the syntax trees of the pin proof's modules (`ctrl_build.py`, `ctrl_pin.py`), whatever program a call names. The round-9 spelling check is gone.
  - Only the helper `ctrl_build.git` names a process-launch facility. It imports `subprocess` in its own body and returns its own result type, so no module-level `subprocess` name exists.
  - Outside the helper, in both modules, the census refuses any reference to a process-launch facility, by import, alias, name or attribute:
    - the `subprocess`, `pty` and `asyncio.subprocess` modules and their members;
    - `os.system`, `os.popen`, `os.exec*`, `os.spawn*`, `os.posix_spawn*`, `os.fork`, `os.forkpty`, `os.startfile`;
    - asyncio's `create_subprocess_exec` and `create_subprocess_shell`.

    An attribute with one of those names is refused on any object, so `os` reached through another module is refused too.
  - It also refuses:
    - `eval`, `exec`, `compile`, `__import__`, `importlib`, `builtins`;
    - `getattr`, `setattr`, `delattr`, `vars`, `globals`, `locals`;
    - an attribute that begins with an underscore (but `__name__`), a frame's attributes, and `sys.modules`;
    - a wildcard import.
  - Where the pin is decided (`stack_gitlink`, `stack_pin` and the command line's `main`), every name is followed through `ctrl_build.py`'s own functions, classes and constants. Each name must be in a fixed vocabulary that starts no process: a few names of `os`, `hashlib`, `stat`, `pathlib` and `argparse`, and builtins and attributes of the proof's own values.
    - So the decision reaches no process but through the helper, by any route.
    - `ctrl_build.run`, the harness's runner, which every reviewer mutant uses, is refused there, naming the line and why.
  - The census also refuses `ctrl_build.py` without the helper, or with the helper's name bound again, as well as the environment check from round 9.
  - `ctrl_pin.py`'s tool runs (`make`, the gates its controls run) now go through `fw_gtest.run`, as `ctrl_build.run` always has. Make's database and dry-run readings of every Makefile builder are byte-identical to `feed95bb`'s, and every non-census pin control prints the same verdict.
  - There are now eight census controls (35 pin controls, up from 30). The README's figure moves with them, and the figure check holds it. Each is refused by name at its planted line:
    - a Git command run by the harness's runner (round 9's);
    - a computed name (`git.__name__`, R585-8's exact mutant);
    - a dashed program (`git-ls-tree`);
    - an aliased import (`from subprocess import run as r`);
    - `os.system` (added to `ctrl_pin.py`, outside the decision);
    - `exec` of a string;
    - the helper's environment without each of its two settings. These two are now found by the setting's name, so another finding cannot hide them.
  - The clean proof has no finding.
- `be607527e`. Wording only, found on rereading. "Only the helper starts a process" overclaimed, since the build functions and tool runs start processes through `fw_gtest.run`. The README and docstrings now say the helper alone *names a facility*. Every replica and probe below ran again at this head.

Validation. CI-parity means Ubuntu 24.04, CPython 3.12.3, gcc 13.3, GNU make 4.3 under `MAKEFLAGS=w`, GoogleTest 1.14.0, clang 18 and cmake 3.28, on four CPUs, in fresh clones at `be607527`.
- `firmware-boundary`'s step: PASS in 728 s (40 % of 30 min, beside two other containers). 2822 compiled sources of 3053, 0 findings; 105 boundary, 35 pin and 4 figure controls, 0 misbehaved.
- `firmware-verilator`'s step: PASS in 498 s (21 % of 40 min). 816 of 916, 0 findings; 6 boundary, 35 pin and 4 figure controls, 0 misbehaved.
- `firmware-unit`'s steps: every step rc 0, 2215 s (82 % of 45 min, beside the two other replicas).
  - The firmware gate's 845 verdict lines are byte-identical to rounds 4 to 9 (`mutants: 471 of 471 caught`).
  - The store passed 435 tests; the coverage self-test caught 29 of 29; `fw_coverage.py --check` PASS (30 files), the table identical.
- The docs job's 54 commands: all rc 0. These include `ci_events.py --check` (1902) and `--selftest` (2610 arms), `ci_scope.py --selftest`, `check_py_idiom.py` (every ratchet held), `check_em_dash.py --base feed95bb` (19 added lines, 0 findings) and `docs_check.py`.
- Images: 35 of 35 ELF hashes are identical to round 9 and dev `aef7ac66` (manifest sha256 `de8ae063…`).
- The reviewers' probes ran unmodified (sha256 equal to their manifests), at `feed95bb` and then at the head:
  - R585-8's `census_probe.py`: first `mutant census findings: []` and `REPRODUCED`. At the head the census names `ctrl_build.py:260 stack_pin names run, which the pin decision may not reach (…:105 the value of run names fw_gtest.run, …)`, and the probe stops with `AssertionError: Probe no longer reproduces the census escape`.
  - R584-8's `proof_mutants.py` M8 and M11: first `census findings: []` for both. At the head the census names `ctrl_build.py:260` (M8) and `ctrl_build.py:210` (M11), and each exits 1.
    - All twelve mutants at the head: each is caught by its own control or by the census, as R584-8 tabled. M5 passes every control, as R584-8 reported.
    - Where a mutant replaces a census control's anchor, that control reports `anchor occurs 0 times` by name.
  - Round 9's two probes still print `REFUSED`.
- Every entry point, under the five disguises of round 9: 85 of 85 refused, naming the changed file.
- 28 further planted forms are each named by the census at their line. Among them are `__import__`, `importlib`, `getattr` with a computed name, `os.popen`, `os.execvp`, `os.posix_spawn`, `pty.spawn`, `asyncio.create_subprocess_exec`, `fw_gtest.run` directly, `shutil.os.system`, `sys.modules`, a generator's frame globals, a rebinding of the helper's name, a lambda parameter shadowing `run`, and the runner as a default argument.

Acceptance criteria: unchanged and met. The pin, the RV32 images (byte-identical at every shape), the boundary in both directions with its planted controls, coverage (same denominator) and every campaign's kills are as before. The census now holds the launch route by construction where the pin is decided, and refuses each assigned facility module-wide.

Open risks/questions:
- One reading to rule on. `ctrl_build.py` is also the firmware's shared builder: its build functions and `run`, like `ctrl_pin.py`'s tool runs, start processes through `fw_gtest.run`.
  - The census does not count another module's function as a facility. It refuses such a function only where the pin decision would reach it. Two planted forms show this: the runner called in `legacy_stack`, and `fw_gtest.run` in `ctrl_pin.mirror`. Neither is seen.
  - Such a process cannot change what the decision reads.
  - Making "only the helper starts a process" literal means moving those functions out of the two modules. That changes the boundary gate's builder model (`BUILDER_NAMES`, `PART_OF`, the plants) and is not taken here.
- The decision's vocabulary is fixed, so a change there that uses a new name fails the census until the name is added. M5b's `path.stat()` and M6's `.items` are named this way.
- The helper and its environment are held by the module-wide rule, the environment check and the replacement controls, not by the vocabulary.
- The census reads the modules as written. Code elsewhere that rebinds their names at run time is not seen, and neither is a route of Python's own that none of the refused names opens.
- R584-8-F1's alternative asked for a dashed Git *string* to be named. The ruling holds the route instead: a dashed string that is never launched is not a finding.
- S1 to S3 are optional and not taken. RES-1 and RS1 go to #495; `PR-BODY.md` applies RS1's exact wording, and its round-10 Status names no push state.
- `firmware-unit`'s headroom is #716's.

Evidence: `HANDOFF.md`, Round 10 (commits, file:line table, control, form and probe tables, gates), with logs under `round10/logs/` in the author packet.
