[A583] STOP

Round 12 for PR #705 ([assignment](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6114400461)), answering R584-10. The assignment's STOP condition is met on item 1: "STOP if the dev merge cannot keep both sides' CI guarantees". No merge commit was made. Items 2 and 3 do not depend on the merge; they are done and validated as three new commits on `aca5e8af`, with no rebase or amend. Not pushed.

Head: `adb936049165dc82e8832e79329984108eb1480f`

## Item 1: why the merge stops

- **F-INT changed the core this lane moved.** Dev `09c7231e` holds PR #704 (#665 F-INT PR 1). Its commits `5a50b2045` and `7c583daac` change ACMP's core and core tests:
  - `sw/firmware/ctrl/acmp/acmp.c` gains a `publish` port, called before every frame an entry sends and first in `finish`;
  - `acmp.h` gains `struct acmp_ports.publish`, the `published_*` fields and the PUBLISHED BEFORE PROMISED contract;
  - `test/test_acmp.cpp` and `test/acmp_fake.hpp` test it.

  Dev's adapter sets the port (`acmp_mbx.c`: `m->ports.publish = port_publish;`). Dev's `ctrl_mutants.py` adds 11 `pub-acmp-*` plants in `acmp/acmp.c`. ADP, MAAP, `wire.h` and their tests did not change on dev.
- **No tsn-c-stack commit has the port.** It is not in `include/acmp.h` on any remote branch (main `98dc9e3` included), and not in `git log --all -S published_stream`. No tsn-c-stack PR or Issue carries it; #9 describes a published binding for the Linux daemon, not this core port.
- **The trial merge** (scratch clone) stops in 13 conflicts:
  - modify/delete on exactly `acmp/acmp.c`, `acmp/acmp.h`, `test/acmp_fake.hpp` and `test/test_acmp.cpp`;
  - content conflicts in `rtl-fast.yml`, `ci_events.py`, `CI_WORKFLOWS.md`, `SUBMODULES.md`, the submodule diagram's four files and `tb/verilator/mbx/Makefile`.
- **With the deletions kept**, so the core is the pinned stack's (`1a9f651c`), dev's adapter does not compile: `acmp_mbx.c:98:17: error: 'struct acmp_ports' has no member named 'publish'`. With dev's `acmp.h` in front, the same compile is rc 0.
- **No resolution keeps both sides:**
  - keeping dev's `acmp.c`/`acmp.h` restores the copies the lane removed (acceptance 2) and the boundary refuses them;
  - keeping the stack's core and dropping the port changes firmware behaviour and the images against dev, and drops F-INT's acceptance and its 11 plants;
  - the pin cannot move, since no tsn-c-stack commit carries the port and this lane may not push there.
- **A way on, for a decision:**
  1. F-INT's ACMP core change (both commits' `acmp.c`/`acmp.h` hunks and its `test_acmp.cpp`/`acmp_fake.hpp` cases) lands in tsn-c-stack by its own PR.
  2. This lane then moves the pin to that commit, with the byte-identical-cores diff against dev's `acmp.c`/`acmp.h` at `09c7231e`.
  3. It retargets the 11 plants to `tsn-c-stack/src/acmp.c` and merges dev.

  PR #724 touches the same CI files; whichever merges second resolves.

## Items 2 and 3: what changed

- `6b03a8870` (item 3): Git is given only the proof's own environment.
  - **The allowlist.** Git's whole environment is `ctrl_build.GIT_ENVIRONMENT`: `GIT_NO_REPLACE_OBJECTS=1`, the graft file under `/dev/null`, `GIT_CONFIG_NOSYSTEM=1`, `GIT_CONFIG_GLOBAL=/dev/null`, and nothing inherited (no `PATH`, `HOME` or `LANG`; Git falls back to its own paths). This is the idiom of `act_ci.git_environment`.
  - **The judge.** The hook judges the mapping passed (`environment_judge`, bound when the hook is installed).
    - It must be a plain `dict`, or on 3.14's `fork_exec` a list of `bytes` entries with each key once.
    - Every key and value must be a plain `str`, checked before any lookup, so no `__eq__`, `__hash__` or `encode` of a crafted object runs.
    - Then both settings are required, with the round-11 words.
    - Then the proof's own environment, key for key. The refusal names the key, never an inherited value.
  - **Four hook plants**, each refused at the helper's line: the caller's environment given to Git again; `GIT_DIR` added; a key that compares equal to `GIT_NO_REPLACE_OBJECTS` but reaches Git as another (the crafted key the assignment describes); a value `"1"` that encodes as `0`.
  - **17 standing controls** (`ctrl_pin_env.py`). Each sets variables in the environment of the interpreter that runs the proof on a stack clone. Each is held: the verdict is the clone's own, and Git starts no program they name.
    - The repository: `GIT_DIR` (a repository whose HEAD and gitlink are a commit holding an edit), `GIT_INDEX_FILE` (an index whose gitlink is `pin~1`, the clone checked out there), `GIT_WORK_TREE` and `GIT_COMMON_DIR`.
    - The object store: `GIT_OBJECT_DIRECTORY`, and `GIT_ALTERNATE_OBJECT_DIRECTORIES` (the clone's objects, its own store emptied).
    - The replacement refs: `GIT_REPLACE_REF_BASE`.
    - The configuration: `core.fsmonitor` naming a recorder through `GIT_CONFIG_COUNT`, `GIT_CONFIG_PARAMETERS`, `GIT_CONFIG_GLOBAL`, `GIT_CONFIG_SYSTEM`, `HOME` and `XDG_CONFIG_HOME`. Git runs that program when it reads the index.
    - Clean filters: one through `GIT_CONFIG_COUNT` (the assignment's control) and one through `GIT_ATTR_SOURCE`. Each would turn the edit back into the pinned blob, and the setup checks that it does.
    - Every variable at once on the pinned clone, which is accepted.
    - The judge given `fork_exec` entries with a key twice.
  - **79 pin controls**, up from 58, with the README's figure.
- `a3992e545` (item 2): the README, `ctrl_pin.py`'s docstring (THE THREAT MODEL) and the PR body state the ruling's model in place of "native code is the remaining limit".
  - The model is the state the proof reads: files and modes, Git's object store, refs, configuration and attributes, and the inherited environment.
  - The proof's own modules are reviewed source, outside the model; the hook is defence in depth.
  - What the hook does not see is still stated: `ctypes`, extension modules, `fork_exec` on 3.12.3, what Git starts, and code above the helper.
- `adb936049`: found by the boundary replicas at `a3992e54`, which refused every captured builder. The capture's own audit hook (`ctrl_capture.HOOK`, installed first) writes `CTRL_CAPTURE_FROM` into every start's environment. That one name is now let through as a plain `str`, since Git does not read it, and every other extra key is still refused.

## Evidence

- **The escape at `aca5e8af`, now closed.** With `aca5e8af`'s helper environment (mutant H22 below), 13 of the 17 controls escape:
  - `GIT_DIR` is accepted at another commit (`tsn-c-stack at c017579b…`), and so is `GIT_INDEX_FILE` (`at 74445d28…`);
  - `GIT_WORK_TREE`, `GIT_COMMON_DIR`, `GIT_OBJECT_DIRECTORY` and `GIT_ALTERNATE_OBJECT_DIRECTORIES` change the verdict;
  - each configuration route runs the recorder.

  A direct probe runs the command-line pin check with one variable inherited. At `aca5e8af`, `GIT_INDEX_FILE` gives exit 0 `tsn-c-stack at 74445d28…` and `GIT_DIR` gives exit 0 at an edited commit. At the head both are refused (exit 2, the true verdict).
- **The hook-rule campaign.** Each rule is deleted in turn in a disposable clone at the head: H1 to H17 (round 11's), plain `str` (H18), exact environment (H19), `fork_exec` entries (H20), the helper inheriting the caller's environment, alone and with H19 (H21 to H23), and the capture exemption (H24). Each is CAUGHT, 24 of 24, on CPython 3.12.3 and 3.14.7, with the unmodified proof clean.
- **CI-parity replicas** (Ubuntu 24.04, its CPython 3.12.3, gcc 13.3, GNU make 4.3 under `MAKEFLAGS=w`, GoogleTest 1.14.0, clang 18, cmake 3.28), four CPUs each, fresh clones at `adb93604`:
  - `firmware-boundary`'s step: PASS in 655 s. 2822 compiled sources of 3053, 0 findings; 105 boundary, 79 pin and 4 figure controls, 0 misbehaved.
  - `firmware-verilator`'s step: PASS in 470 s. 816 of 916, 0 findings; 6, 79 and 4 controls, 0 misbehaved.
  - `firmware-unit`'s steps: every step rc 0 in 1952 s. The firmware gate's 845 verdict lines are byte-identical to rounds 4 to 11 (`mutants: 471 of 471 caught`, `test_ctrl_firmware: PASS`); the store passed 435 tests; the coverage self-test caught 29 of 29; `fw_coverage.py --check` PASS (30 files), the table byte-identical.
- **The docs job**, 53 of 54 rc 0: `ci_events.py --check` and `--selftest`, `ci_scope.py --selftest`, `check_py_idiom.py` (every ratchet held), `check_em_dash.py --base aca5e8af` (19 added lines, 0 findings) and `docs_check.py` among them. The one failure is `check_rtl_source_lists.py --selftest`, which fails 2 of 50 under `MAKEFLAGS=w`. It fails identically at `aca5e8af` and at dev `09c7231e`, and passes 50 of 50 at the head without `MAKEFLAGS`; no file it reads changed.
- **Images:** all 35 ELF hashes are identical to round 11 and to dev `aef7ac66` (manifest sha256 `de8ae063…`).
- **Entry points:** every entry point refuses each of five disguises (85 of 85), and the clone is clean afterwards.

## Open, for the manager

1. The STOP above: how F-INT's ACMP core change reaches tsn-c-stack before this lane merges dev.
2. Two routes inside the stated model, found this round. Neither is the inherited environment, so both are published here, not fixed (AGENTS.md section 4). The probe is against the head.
   - **A forged tree object in the stack's object store.** The pinned `src/` tree's loose object is overwritten with a tree holding an edit of `src/adp.c`, and the same edit is made on disk. `stack_pin` then ACCEPTS `1a9f651c`. Git 2.43 and 2.56 read subtrees for `ls-tree -r` without checking their hash; `git fsck` reports `hash mismatch 34150e38…`. One fix is to rebuild each tree from the listing and check its hash, failing closed (R584-8-S1's direction).
   - **The repository's own `core.fsmonitor`.** Set in a checkout's `.git/config`, its program is run by Git twice while the decision reads the index; the check still exits 0. `-c core.fsmonitor=false` on the helper's command line closes it, as `act_ci.git_prefix` does.
3. `check_rtl_source_lists.py --selftest` under `MAKEFLAGS=w` fails at dev `09c7231e` too. If the hosted docs job runs that way, dev is red; this is outside this lane.
4. Carried:
   - R584-9-S1 stays optional and not taken.
   - R584-8-RES-1, R585-8-RS1, R584-7-RES1 / R585-7-RS1 and R585-9's RES-1 wording go to #495.
   - `firmware-unit`'s headroom stays #716's.
