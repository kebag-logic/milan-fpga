[R584] NEGATIVE - exact head aca5e8afc58a12ca050cd4c4c5f1c7c02c9ff783

Internal independent review R584-10 of issue #697 / PR #705, round 11 delta: two commits on `be607527` (`d32ceac87`, `aca5e8afc`). Tree `0f0c668d5a92b8e0640c7653bb12b479a8019409`.

All five lenses were applied. RTL and Tests are clean. One MINOR finding is open: R584-10-F1, under Conformance, Robustness and Docs. No RESIDUE is new in this round. The four residue items carried from earlier rounds stay with the manager.

Every item the round-11 ruling assigns was confirmed at this head:
- The hook is installed before the first Git call.
- Each standing control ends in the hook's named refusal before any build.
- The clean proof passes.
- The reviewers' probes end in the runtime refusal.
- The texts attribute the guarantee to the hook.
- No compiled input changed.

The open finding concerns the hosted CPython 3.12.3. There, a pure-Python rebinding that the texts document still keeps a process start from reaching the hook. The texts file this route under the ruling's native-code limit, but the ruling does not cover it. That classification needs a ruling.

## Order of reconstruction

1. `AGENTS.md`, `CONTRIBUTING.md`, `docs/README.md`.
2. Issue #697:
   - the body and its frozen acceptance;
   - the owner decisions of 2026-10-09 (MIT licence, own repository `tsn-c-stack`, submodule consumption, byte-identical images);
   - the round-10 ruling (comment 6112358746);
   - the round-11 ruling (comment 6113306444).
3. The delta `be607527..aca5e8af`:
   - `sw/firmware/ctrl/test/ctrl_build.py`
   - `ctrl_pin.py`
   - `ctrl_boundary.py`
   - `sw/firmware/ctrl/README.md`
4. The PR body at this head.
5. Executable evidence, run by this round.
6. Only after this round's own pass: the R584-9 and R585-9 findings and their published probes, whose sha256 matched their published manifests.

## Findings

### R584-10-F1 - MINOR - Conformance, Robustness, Docs - on the hosted CPython 3.12.3, a pure-Python rebinding keeps a process start from the hook, and the texts file it under the native-code limit without a ruling

- **Artifact:**
  - `sw/firmware/ctrl/README.md:175` and `:183-185`;
  - `sw/firmware/ctrl/test/ctrl_pin.py:37-43` (THE HOOK);
  - `ctrl_build.py:228-325` (`audited`);
  - PR body, Round 11 row 2 and "Open, for the manager" (a).
- **Authority/evidence:**
  - The [round-11 ruling](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6113306444) moves the guarantee to run time because "an audit hook cannot be removed once added, so a later rebinding cannot switch it off". It names exactly one remaining limit: "native code (`ctypes`, extension modules)".
  - On the hosted interpreter, CPython 3.12.3, the `subprocess` module raises its launch event from Python code: `sys.audit("subprocess.Popen", ...)` at `subprocess.py:1534` and `:1823`. Its built-in `_posixsubprocess` holds no `_posixsubprocess.fork_exec` audit event (0 occurrences in 3.12.3's libpython, 1 in 3.14.7's module; `receipts/py3123_launch_audit_facts.txt`).
  - The README (`:185`), the docstring (`ctrl_pin.py:40-42`) and the PR body therefore state, correctly, that on the runner's interpreter "code that ... rebinds `sys.audit`" starts a process the hook never sees.
  - That route is not native code. It is the same class as the rebinding the ruling moved to run time to close, on the interpreter the hosted gates use.
  - The texts place it under "Native code is the remaining limit" (`README.md:183-185`). The PR body's open question (a) says it is "within the stated extension-module limit". That is the author's own reading of the ruling's scope; no maintainer has accepted it.
  - The README's "So no later rebinding of a name changes how it judges an event" (`:175`) is accurate only in the narrow sense. On 3.12.3 the rebinding stops the event from reaching the hook at all.
  - Under `AGENTS.md` section 2, such a conflict is published and decided, not settled by an interpretation.
  - The author did publish it. The decision is still open at this head.
- **Impact:**
  - No present defect: the unmodified proof starts only the helper's Git (the clean probe shows 0 runner starts).
  - On the hosted runner, however, the guarantee the ruling asked for does not hold against a planted rebinding of the interpreter's audit entry point, which is a pure-Python, one-line change.
  - The texts present the stated limit as the ruling's own, so a reader takes the hosted guarantee to be wider than it is.
  - This is a scope and conformance question, not wording alone, so it is not RESIDUE.
- **Required outcome:** one of these, recorded publicly:
  - (a) a maintainer ruling that accepts, on the hosted CPython 3.12, this Python-level route as part of the guarantee's stated limit. The texts may then stand as written, or name the route as accepted by that ruling.
  - (b) the route is closed, inside the lane or under its own Issue (for example, the hosted interpreter). A standing control that rebinds the audit entry point must then end in the hook's refusal on the hosted interpreter.
  - This review does not prescribe the design.
- **Verification:**
  - for (a), the ruling's link, and the texts consistent with it;
  - for (b), the new control `[ok]` on CPython 3.12.3 at the corrected head, with the other 58 pin controls unchanged.

### Retained SUGGESTION

- **R584-9-S1 - SUGGESTION - Robustness** - `ctrl_pin.py:508-509`: with the helper's name bound only by assignment, `census()` still indexes `defs[0]` and raises `IndexError`, so the census fails closed with a traceback. This is optional; it does not affect the verdict.

## What was confirmed at this head

| Ruling item | Result | Receipt |
|---|---|---|
| Hook installed before the first Git call, and kept | `@audited` runs `sys.addaudithook` when the helper is defined (`ctrl_build.py:324`, `:328`). Nothing above it calls Git (`GIT = shutil.which("git")` starts nothing). The hook cannot be removed. | source; `receipts/pin_controls_py3123_pyyaml.log` |
| Launch events refused unless the helper starts the resolved Git with both settings | `LAUNCH_EVENTS` (`ctrl_build.py:209-211`), `unlike` (`:276-304`). Each judged property has a control that only it fails: the program (`/usr/bin/true`), each setting, the builtins rebound. | `pin_controls_py3123_pyyaml.log`, `hook_mutants_py3123.log` |
| Dynamic-code events refused, the helper included | `DYNAMIC_EVENTS` and the `importlib` import (`:313-318`). `exec`, `eval` and `compile` inside the helper are each refused at `ctrl_build.py:333`. | same |
| Every R584-9 / R585-9 escape and the earlier bypasses run as standing controls, ending in the named refusal before any build | 30 `HOOK_PLANTS` (`ctrl_pin.py:243-321`), plus the unplanted proof: 31 of 31 `[ok]` on 3.12.3 and on 3.14.7. 25 are refused at the plant's line, as the README states; the other 5 by program, setting or name. | `pin_controls_py3123_pyyaml.log`, `pin_controls_py3147.log` |
| Clean proof passes | `stack_pin` `1a9f651c…` accepted; census findings 0; "the pin proof as the checkout holds it, under its audit hook" `[ok]`. | same |
| R585-9 `census_matrix.py` | Unmodified (sha256 equal to its manifest): `RESULT: 88 cases, 88 passed, 0 escaped`, rc 0. | `r585-9_census_matrix_py3123.log` |
| R585-9 `dynamic_launch_probe.py` | Unmodified: the planted child is refused (`AuditRefusal … ctrl_pin_probe.py:922 asks for compile in the pin proof`). The probe's assertion that the outside process ran fails, rc 1. | `r585-9_dynamic_launch_py3123.log` |
| R584-9 rebinding probe | Unmodified `make_rebind_mutants.py` and `rebind_runtime_probe.py`, on disposable clones. E1b, E2b, E6 and E7 each end in `AuditRefusal … starts git (subprocess.Popen) while the pin proof runs, not by the helper`, in the census and from `stack_pin()`, rc 1. The clean copy: 0 runner starts, rc 0. | `r584-9_rebind_*_py3123.log` |
| README, docstring and PR body attribute the guarantee to the hook and name native code as the limit | Yes (`README.md:172-191`, `ctrl_pin.py:11-47`, PR body Round 11 and Status). The 3.12.3 classification is F1. | source, PR body |
| Works on CPython 3.12.3 | 58 of 58 pin controls `[ok]`, census 0, 0 misbehaved. The first run had one `[ESCAPED]` arm (the AECP wire comparison, "no pin verdict"). That was this host's standalone 3.12.3 lacking PyYAML (`ModuleNotFoundError: yaml`), which the hosted jobs install with pip. With PyYAML on its path, the rerun is clean. | `pin_controls_py3123.log`, `aecp_wire_py3123_direct.log`, `pin_controls_py3123_pyyaml.log` |
| No image byte changed | The delta changes only `README.md`, `ctrl_boundary.py` (docstring), `ctrl_build.py` and `ctrl_pin.py`. In `ctrl_build.py`, only the imports, the new hook block and the helper changed (`executable=GIT`; argv unchanged). No build function, C/H source, linker input, Makefile or gitlink changed. RV32 images were not rebuilt in this round. | `receipts/delta_scope.txt` |

The controls can fail. Each mutant below weakens the hook in place; the hook arms then run, and the file is restored byte for byte.

| Mutant | Arms escaping (of 31) |
|---|---|
| H0, none | 0 |
| H1, never installed | 30 |
| H2, launches unjudged | 15 |
| H3, dynamic code unjudged | 13 |
| H4, the `GIT_NO_REPLACE_OBJECTS` check removed | 2 |
| H5, any program from the helper | 1 |
| H6, code replacement unjudged | 1 |

Receipt: `receipts/hook_mutants_py3123.log`.

Threads: only `ctrl_boundary.py` runs a worker thread beside the pin calls. Its one process start is made before the main thread's pin controls run. The README documents the any-thread rule (`:176`), so this is not a finding.

## Prior findings at this head

| Prior finding | Status | Evidence |
|---|---|---|
| R584-9-F1 (helper or vocabulary name rebound by attribute assignment) | RESOLVED. The guarantee is now the hook's. E1b, E2b, E6 and E7 end in the runtime refusal. E2b, E6 and E7 are standing controls. | `r584-9_rebind_*`; control lines "the helper's name rebound…", "os.walk … rebound" |
| R585-9-F1 (dynamic code through attributes, and inside the helper) | RESOLVED. 88 of 88 matrix cases. The dynamic-launch child is refused. `inspect.builtins.exec`/`eval`/`compile`, `pkgutil.importlib.import_module`, and `exec`/`eval`/`compile` inside the helper are standing controls, each `[ok]`. | `r585-9_*`; `pin_controls_py3123_pyyaml.log` |
| R584-9-S1 | RETAINED SUGGESTION (`ctrl_pin.py:508-509`) | source |
| R584-9-S2 (launch routes outside the named facilities) | RESOLVED by the stated limit. The texts now name `ctypes`, extension modules, `_posixsubprocess.fork_exec` and `multiprocessing`, and the hook judges `os.fork` and the other audited starts. | `README.md:183-186` |
| R584-8-RES-1 | RETAINED RESIDUE for #495. `README.md:231` still reads `runs it, with GoogleTest and GoogleMock 1.14.0:`, and its exact fix is unchanged. | source |
| R585-8-RS1; R584-7-RES1 / R585-7-RS1; R585-9's residue wording | RETAINED for the manager's #495 checklist | — |
| Earlier rounds' resolved findings (replacement objects, graft, filter, mode, figure, bench prerequisites) | Still RESOLVED: those controls are `[ok]` at this head on both interpreters. | `pin_controls_py3123_pyyaml.log`, `pin_controls_py3147.log` |

## Per-lens results

[R584] UNCLEAN Conformance - `ctrl_build.py:199-336`, `ctrl_pin.py:11-47,243-321`, `README.md:172-205`, PR body Round 11 - Every ruling item is met (table above). F1 is open: the scope classification of the hosted 3.12.3 route.

[R584] PASS RTL - `receipts/delta_scope.txt` - The delta holds no HDL, clock, reset, CDC, mailbox ABI, firmware source, build flag or image input. All six gitlinks are identical at `be607527` and `aca5e8af`.

[R584] UNCLEAN Robustness - `ctrl_build.py:228-325`, `receipts/py3123_launch_audit_facts.txt` - Malformed, rebinding, dynamic-code, thread, code-replacement and environment plants are all refused on both interpreters. F1 is the remaining hosted-interpreter route.

[R584] PASS Tests - `ctrl_pin.py:243-321,470-487,803-835`, `receipts/pin_controls_py3123_pyyaml.log`, `pin_controls_py3147.log`, `hook_mutants_py3123.log`, the R585-9 and R584-9 probe receipts:
- 58 of 58 pin controls pass on 3.12.3 and on 3.14.7.
- Each hook-weakening mutant makes at least one control escape.
- The prior probes end in the refusal.
- The README's 58, 30 and 25 match the code.

[R584] UNCLEAN Docs - `README.md:175,183-185`, `ctrl_pin.py:37-43`, PR body Round 11 row 2 and open question (a) - F1's classification. The other texts are accurate. `docs_check.py` reports 0 findings. `check_em_dash.py --base be607527` with the pinned renderer reports 0 findings over 36 added lines. `check_py_idiom.py` holds every ratchet (`receipts/docs_*`).

## Reviewer-owned ledger

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1) | Round-11 ruling items against `ctrl_build.py:199-336`, `ctrl_pin.py:11-47,243-321`, `README.md:172-205`, PR body; 58 controls; R585-9 and R584-9 probes | R584-10 | aca5e8afc58a12ca050cd4c4c5f1c7c02c9ff783 |
| RTL | CLEAN | `receipts/delta_scope.txt` (4 files, none HDL; gitlinks unchanged) | R584-10 | aca5e8afc58a12ca050cd4c4c5f1c7c02c9ff783 |
| Robustness | UNCLEAN (F1) | `audited` (`ctrl_build.py:228-325`); 30 plants on two interpreters; rebinding probes; 3.12.3 launch-audit facts; the thread rule against `ctrl_boundary.py:488-497` | R584-10 | aca5e8afc58a12ca050cd4c4c5f1c7c02c9ff783 |
| Tests | CLEAN | `HOOK_PLANTS`, `exercised`, `planted`, `census_arms`; 58 of 58 on 3.12.3 and 3.14.7; hook mutants H1-H6; prior probes | R584-10 | aca5e8afc58a12ca050cd4c4c5f1c7c02c9ff783 |
| Docs | UNCLEAN (F1) | `README.md:172-205,231`; `ctrl_pin.py:11-47,84-110`; `ctrl_boundary.py:77-85`; PR body; docs, em-dash and idiom gates | R584-10 | aca5e8afc58a12ca050cd4c4c5f1c7c02c9ff783 |

## Real limits

- This round ran no manager source bank, builder bank or native bank. It ran:
  - the pin proof, its census and its 58 pin controls;
  - focused hook mutants;
  - the published prior probes;
  - the docs gates.
- It did not run the firmware gate, the coverage ratchet, the mutation campaigns, the full boundary self-test or the RV32 image builds. Image identity is argued from the delta's file scope, not rebuilt.
- The source-head execution evidence for those is the author's published gate receipts, which this round did not re-execute.
- CPython 3.12.3 here is a standalone build, not the hosted Ubuntu interpreter. PyYAML was added on its path from the pure-Python package, as the hosted jobs install it with pip.
- Hosted CI: at 2026-10-11T22:05:40Z the head had 0 check runs, 0 workflow runs and a combined status of `pending` with 0 contexts (`receipts/hosted_state.txt`). No hosted evidence exists at this head yet.
- Physical calibration was NOT RUN. Field skips are not hardware proof.

## Pending manager duties

- Rule on F1:
  - accept the hosted-3.12 Python-level route as part of the stated limit;
  - or require it closed, in-lane or under its own Issue.
  - Then obtain re-review of the resulting head.
- Exact-head hosted acceptance (`rtl-fast`, `verilator-suites`, `yosys-portability` and the firmware jobs) once runs exist at this head.
- The current-dev merge candidate. Source base is `8b61b70902f3ebf118e56967277e2686731081bd`; live dev is `09c7231eca343607c97c0d66abebb2553688712c`. The candidate's builder and native banks run at the merge turn.
- Carry R584-8-RES-1, R585-8-RS1, R584-7-RES1 / R585-7-RS1 and R585-9's residue wording to #495.
- The author's open note (b): the helper's environment passes the caller's Git variables through. It predates this round and lies outside this assignment; it may become an Issue if wanted.

## Checkout integrity

- HEAD is `aca5e8afc58a12ca050cd4c4c5f1c7c02c9ff783`, and both the worktree tree and the index tree are `0f0c668d5a92b8e0640c7653bb12b479a8019409`. There are 0 status lines.
- The hook mutants restored `ctrl_build.py` byte for byte (`restored True`).
- The `tsn-c-stack` and `lwSRP` submodules were initialised at their recorded gitlinks (`1a9f651c`, `9197193e`). Every submodule is at its gitlink (`receipts/integrity_final.txt`).
- Rebinding mutants ran only on disposable clones under `scratch/`.

R584-10 FINISHED
