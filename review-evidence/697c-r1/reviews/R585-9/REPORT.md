[R585] NEGATIVE - exact head be607527eaac84cfc8d7456167b070a22228345b

R585-9 applied all five lenses. One open MINOR, R585-9-F1, leaves Conformance, Robustness, Tests and Docs unclean. RTL is clean for the reviewed delta. The prescribed computed-name and dashed-program probes now receive named census refusals. The new dynamic-code prohibition still has two holes.

Tree: `0ff64b4d0d26c7d6d737802cafacf3fde3356f04`. This is the independent external review of [PR #705](https://github.com/kebag-logic/milan-fpga/pull/705), following [the public review start](https://github.com/kebag-logic/milan-fpga/pull/705#issuecomment-6113151837). No source fix, commit, push, GitHub write, author contact or delegation occurred.

I loaded the operating contract, documentation index, [issue #697](https://github.com/kebag-logic/milan-fpga/issues/697), its public scope and pin decisions, and relevant requirements and interfaces. I examined the requested source-range inventory and history from `8b61b70902f3ebf118e56967277e2686731081bd`, separating the inherited F5 merge through `aef7ac66605c4404900ce04cbaaeff88e41bb880`. The focused delta comprises `65115fced` and `be607527e` after `feed95bbb6429e5af0ee3f0a24c531777279e9de`; it changes four files, recorded in [delta.diff](delta.diff). Relevant integration changes are in [integration.diff](integration.diff).

The independent verdict and ledger were written in [independent-verdict.md](independent-verdict.md) before reading prior public reviewer findings. Those findings were then reconciled and their required probes replayed. No current parallel review report or private author material was read.

**R585-9-F1 - MINOR - Conformance, Robustness, Tests, Docs**

**Artifact:** `sw/firmware/ctrl/test/ctrl_pin.py:224`, especially lines 229-250 and 333; `sw/firmware/ctrl/README.md:175`; `ctrl_pin.py:23`; PR #705 Round 10 and Status.

**Title:** The census accepts explicitly named dynamic code through attributes, and exempts dynamic code inside the helper.

**Authority/evidence:** The [round-10 ruling](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6112358746) requires the dynamic facilities `eval`, `exec`, `compile`, `__import__` and `importlib` to be refused in the two proof modules. The process-launch exception belongs to the helper; the dynamic-code prohibition is module-wide.

The census checks `DYNAMIC` for imports and bare `ast.Name` nodes. Its attribute branches check `LAUNCH_NAMES` and `REFLECTIVE`, but never `DYNAMIC`. Consequently each of these additions is accepted in either module, with no census finding:

```python
import inspect
inspect.builtins.exec("pass")
inspect.builtins.eval("1")
inspect.builtins.compile("pass", "<probe>", "exec")
```

`import pkgutil; pkgutil.importlib.import_module("os")` is also accepted. These specimens explicitly name prohibited facilities; they do not depend on an unnamed reflection route or external rebinding.

The [executable probe](dynamic_launch_probe.py) appends `inspect.builtins.exec(...)` to a disposable copy of `ctrl_pin.py`. Its string starts a harmless child which prints `OUTSIDE_HELPER_PROCESS_RAN`. The exact-head census returns `[]`, and the child executes successfully. [Raw receipt](dynamic-launch.log), probe exit 1 indicating the escape reproduced.

Separately, the exemption at line 229 skips every node of the helper, including dynamic-code nodes. Adding each of `eval('1')`, `exec('pass')`, `compile(...)`, `__import__('os')` and `import importlib` inside `ctrl_build.git` also returns `[]`. The [66-case matrix](census_matrix.py) records 53 expected results and 13 escapes: eight qualified-attribute cases across the two modules, and five helper-body cases. [Raw matrix](census-matrix.log).

**Impact:** The census can accept a future dynamic-code addition that launches outside the controlled helper, contrary to the assigned guard and its documentation. No such escaping call was found in the unmodified published proof. Its current Git calls still use the hardened helper; this does not show altered source bytes entering the published builds. That limits severity to MINOR. The defect concerns code, a test guarantee and an acceptance claim, so it is not RESIDUE.

**Required outcome:** Enforce the dynamic-code prohibition throughout both modules, including qualified attributes and the helper body. Preserve the helper's exception for the permitted process-launch facility. Add named controls for these two missed forms, keep the clean proof accepted, and keep the README, docstrings and PR contract aligned with the enforced rule. A narrower rule would need a public scope decision.

**Verification:** Both reviewer scripts must report named refusals for the escaped cases. The executable specimen must be rejected by the census before acceptance; the five helper-body specimens must be named too. The clean census, eight standing census controls, 35 pin controls and four figure controls must remain correct. Re-review the corrected head.

**R584-8-RES-1 - RETAINED RESIDUE - Docs**

**Artifact:** `sw/firmware/ctrl/README.md:212`, the standalone-suite instructions.

**Authority/evidence:** The [prior public finding](https://github.com/kebag-logic/milan-fpga/pull/705#issuecomment-6112278003) and round-10 ruling retain this wording item for the manager's #495 checklist. The example still leaves `<build directory>` unconstrained, while the whole-tree pin check refuses extra entries inside the submodule.

**Impact:** The prose omits the location constraint for the example build directory. This retained wording item changes no measurement, figure, verdict, test, code, generated artifact or conformance claim, and affects neither the verdict nor lens cleanliness.

**Exact required fix:** Replace `runs it, with GoogleTest and GoogleMock 1.14.0:` with `runs it, with GoogleTest and GoogleMock 1.14.0, from a build directory outside the submodule (the pin check refuses any file its pinned tree does not hold, a build directory inside it included):`.

**Verification:** Read the corrected instructions; the manager carries the item to #495. No repository edit was made here.

The independent checks and published evidence establish the following:

| Check | Result | Evidence |
|---|---|---|
| Current launch references | Clean census returns no finding. Direct launch-module imports, import aliases, OS launch attributes and asyncio subprocess forms are refused in both modules. Dynamic-code exceptions are F1. | [census-matrix.log](census-matrix.log); `ctrl_build.py:197`; `ctrl_pin.py:224` |
| Five required standing controls | Computed name, dashed program, aliased import, `os.system`, and string `exec` each refused at the planted line by the expected name. The existing runner bypass and both environment controls also pass. | [focused-checks.log](focused-checks.log); `ctrl_pin.py:153,631,653` |
| Whole-tree pin and entry guards | 35/35 controls correct, including clean clone, hidden edit, extra path, type, mode, replacement tree/commit, graft, filter, entry guards and poisoned Makefile targets. Make prerequisite census clean. | [focused-checks.log](focused-checks.log) |
| README figures | 96 firmware defects, eight passing controls, five simulation defects, 35 pin controls. All four wrong-figure plants refused. | Same receipt; `ctrl_boundary.py:410` |
| R584-8 M8 and M11 | Both mutant suites exit 1 with the census naming `ctrl_build.py:260` and `:210`, respectively. The outer campaign exits 0 after collecting results. | [summary](r584-replay/SUMMARY.txt), [M8](r584-replay/M8-dashed-ls-tree-outside-helper.log), [M11](r584-replay/M11-dashed-ls-files-outside-helper.log) |
| R585-8 computed-name probe | Census names the bypass at `ctrl_build.py:260`; the unchanged prior script exits 1 with `Probe no longer reproduces the census escape`. | [prior-r585.log](prior-r585.log) |
| Prior probe authenticity | All three downloaded scripts match their public manifest hashes; they ran unchanged. | [prior-probes-verified.txt](prior-probes-verified.txt) |
| Source preservation | Seven moved C/header files remain token-identical to `aef7ac66`; the surviving wire-header edit is comments only. HDL, synthesis, common bench code, mailbox contract and existing four dependency pins are unchanged from the source base. Round 10 changes no firmware/image input or pin. | [structure.log](structure.log), [portable check](structure_checks.py) |
| Image preservation | All 35 published ELF hash rows are identical for `aef7ac66`, `feed95bb` and this head. The three manifests share SHA-256 `de8ae063d8046a72b90cf180b5d1dcf129c43400cd7f139a2ea26a897c86ebd0`. This compares author receipts; it is not a local image rebuild. | [dev manifest](public/round2b/images-dev.sha256), [round 9](public/round9/images-head.sha256), [round 10](public/round10/images-head.sha256) |
| Source boundary evidence | Published source-head runs report 2822/3053 and 816/916 compiled/recorded populations; 105/6 boundary controls, 35 pin controls and four figure controls, zero misbehaved. | [firmware receipt](public/round10/logs/bjob-final.log), [simulation receipt](public/round10/logs/vjob-final.log) |
| Source regression evidence | Published unit steps all rc 0; 845 firmware verdict lines, 471/471 kills, coverage PASS over 30 files, and 85/85 entry-point refusals. Published make readings before/after are byte-identical. | [unit steps](public/round10/logs/ujob-final.outer), [verdicts](public/round10/logs/fw-verdicts-head.txt), [coverage](public/round10/logs/cov-head.txt), [entry points](public/round10/logs/entrypoints.log), [structure.log](structure.log) |
| CI/document wiring | 1902 CI contract items pass; submodule documentation matches six gitlinks. Published documentation receipt reports all commands successful. | [ci-events.log](ci-events.log), [submodule-docs.log](submodule-docs.log), [published docs receipt](public/round10/logs/docsjob-final.txt) |
| Final checkout integrity | All 1266 parent tracked blobs, kinds, executable modes and index entries match the assigned head. All five required submodules match their gitlinks and tracked bytes/modes/index. Parent status is empty. | [integrity-final.log](integrity-final.log), [verifier](verify_checkout.py) |

The M8/M11 replay also reports controls whose source anchors the mutant removed. Those anchor failures are not credited as the requested census detection; the census itself independently names both bypasses. The prior computed-name script deliberately executes its mutant after asking the census; that execution is not evidence that the boundary gate would ignore the census refusal.

The [public receipt provenance](public-receipt-provenance.json) verifies downloaded bytes against blobs in [the supplied evidence tree](https://github.com/kebag-logic/milan-fpga/tree/58407fa2ff2f4c11dbd7d1986ca0f3774bfec74a/review-evidence/697c-r1). The [source-validation comment](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6113121913) attributes these runs to this head. No manager source-head bank is claimed or inferred.

Prior public findings were reconciled after the independent verdict. For unchanged boundary behavior, the evidence is the current implementation and published exact-head boundary receipts, not a claim that every historical campaign was rerun locally. B and V mean the two source boundary receipts above; P means the independently executed focused checks.

| Prior IDs | Disposition at this head | Evidence |
|---|---|---|
| R584-8-F1; R585-8-F1 | RESOLVED for their reported dashed/computed bypasses; the new dynamic-code obligation has R585-9-F1 | Unchanged prior probes, named current census controls |
| R584-7-F1; R585-7-F1 | RESOLVED | Hardened helper and whole-tree proof; P replacement/tree/filter controls; published 85 entry-point refusals |
| R584-7-F2; R585-7-F2 | RESOLVED | Correct 96 and independently executed figure controls |
| R584-1-F1; R585-1-F2 | RESOLVED | Differential and mailbox pin guards; P |
| R584-1-S1; R585-1-S1 | RESOLVED for TSN stack; lwSRP suggestion remains optional | Whole-tree raw hashes and hidden-edit/script controls; P |
| R585-1-F1; R584-1-S2 | RESOLVED | Per-compile modes and stack-test dependencies; B; `ctrl_boundary.py:246` |
| R584-2-F1; R585-2-F1 | RESOLVED | Actual image-shape/C++ compiles and dependency controls; B/V |
| R584-2-F2; R585-2-F2 | RESOLVED | `run-if2` prerequisite and independently executed poisoned/missing-prerequisite controls; P |
| R584-2-S1; R585-2-S1 | RESOLVED | Split-argument compiler expansion and B |
| R584-3-F1; R585-3-S2 | RESOLVED | Differential C++ compile captured; V's dedicated control |
| R585-3-F1 | RESOLVED for the lane's added capture cost under the public budget ruling; exact-head hosted acceptance still pending | Capture split from unit job; B/V; issue comment 6107349992; no new workflow change in this delta |
| R585-3-S1; R584-3-S1 multi-word part; R584-4-F2; R585-4-F1 | RESOLVED | Compiler invocation/dependency capture, computed/split/make controls; B |
| R584-4-F1 | RESOLVED under the current recorded-compile population contract | Actual dependency capture; B/V; builder-owned/test-equipment limits stated |
| R584-5-F1; R585-5-F1 | RESOLVED | Driver, response-file and forced-input controls; B |
| R584-5-F2 | RESOLVED in wiring and source execution; hosted acceptance pending | Required simulation job, both AECP references, V1-V3; V; CI contract check |
| R584-6-F1; R585-6-F1; R585-6-F2 | RESOLVED | Store-source and per-compile resolution; N1/Q7 controls in B |
| R584-6-S1 | RESOLVED | README explicitly names tests' dependency on stack test fakes |
| R584-6-S2 | RESOLVED | Whole-tree executable-mode comparison and P's mode control |
| R585-5-S2 | RESOLVED | Dependency output replaced the former silent header-text cap |
| R585-2-S2 | RETAINED SUGGESTION | Alternate `--stack` still uses default `STACK_TESTS`; default route pinned |
| R585-5-S1; R584-5-S3 | RETAINED documented optional limit | Isolated interpreter/shell/compiled-helper absolute compiler paths; README |
| R584-3-S1 remainder | Forced-header concern superseded; ignored-pin-error static check RETAINED SUGGESTION | Actual dependencies; poisoned-target controls supplement static prerequisite check |
| R584-4-S2; R585-4-S1; R584-5-S2 | RETAINED SUGGESTION under #716 | Shared unit-job headroom outside this lane by issue comment 6107349992 |
| R584-4-S1; R585-4-S2; R584-5-S1; R585-5-S3; R585-6-S1; R584-7-S1 | RETAINED optional historical figure refresh where not already applied | CI page identifies the heads its figures describe; no exact-head hosted figures available here |
| R584-8-S1 | RETAINED SUGGESTION | Object-store corruption outside the ruled replacement/graft/filter class; no object-store integrity proof added |
| R584-8-S2 | RETAINED SUGGESTION | Replacement handling in image-base and processor-reference extraction outside pin-proof delta |
| R584-8-S3 | RETAINED SUGGESTION | `population()` counts all simulation plants; all five currently are defects |
| R584-2-R1; R585-1-R1-R5; R585-2-RS1-RS3; rounds 3-6 RS1 items | Historical wording corrected or superseded | Current PR body, public links, ADP porting citation and historical result wording |
| R584-7-RES1; R585-7-RS1; R585-8-RS1 | Exact publishing-state wording APPLIED; checklist duty retained | Round-9 Status says published; round-10 Status makes no push claim; round-8 ruling linked |
| R584-8-RES-1 | RETAINED RESIDUE | Exact fix above; manager's #495 duty |

[R585] PASS RTL - `delta.diff`, `structure.log`, `tb/verilator/mbx/Makefile:40`, published image manifests - no changed HDL, clock/reset/CDC, mailbox ABI, runtime firmware tokens, build flags or image inputs in this delta. The common runner change preserves its result fields; current Makefile prerequisite checks and published make readings agree. This is delta coverage, not fresh physical or full integration qualification.

The reviewer-owned completion ledger is:

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN: F1 | Issue acceptance and scope rulings; `ctrl_pin.py:224`; `ctrl_build.py:197`; matrix and source/image evidence | R585-9 | be607527eaac84cfc8d7456167b070a22228345b |
| RTL | CLEAN | `delta.diff`; `integration.diff`; `structure.log`; unchanged HDL/mailbox/pins; `tb/verilator/mbx/Makefile:40`; image manifests | R585-9 | be607527eaac84cfc8d7456167b070a22228345b |
| Robustness | UNCLEAN: F1 | `ctrl_pin.py:224`; executable dynamic-code probe; 35 pin controls; replacement/type/mode/filter and poisoned-target results | R585-9 | be607527eaac84cfc8d7456167b070a22228345b |
| Tests | UNCLEAN: F1 | `ctrl_pin.py:153,631,653`; `ctrl_boundary.py:410`; matrix; figure controls; unchanged prior probes; B/V receipts | R585-9 | be607527eaac84cfc8d7456167b070a22228345b |
| Docs | UNCLEAN: F1 | README:169-200; `ctrl_pin.py:11`; `ctrl_boundary.py:78`; PR Status/Round 10/limits; figure and submodule checks | R585-9 | be607527eaac84cfc8d7456167b070a22228345b |

Hosted evidence was inspected read-only at `2026-10-11T20:10:22Z`. The API returned zero workflow runs for the source head, zero check runs, zero commit statuses, and an empty PR check rollup. The PR is open and ready but reports `mergeable=false`, `mergeable_state=dirty`, with no merge commit. [Raw API receipt](hosted-state.json), [run list](hosted.json). There is no executed or skipped hosted context available to credit at this head. Earlier-head green jobs do not clear this head. Hosted and local-replica acceptance remains the manager's duty.

The recorded PR base is `aef7ac66605c4404900ce04cbaaeff88e41bb880`; live `dev` is `cfadd767a7ad47aaee68de655e1066cc000fb8a0`. Neither the recorded base nor source-head receipts constitute the final current-dev merge candidate. The manager must resolve that candidate, obtain its required builder/native bank receipts, link them on the PR, complete hosted/local-replica acceptance, obtain clean re-review of F1, and complete containment and issue/project closure after any authorized merge. No merge is authorized by this report.

Limits: this review ran focused checks and disposable probes, not the prohibited full parent, processor, synthesis or builder banks. No simulator build, shared installation, container runner, privileged operation or hardware access occurred. Physical calibration was **NOT RUN**. Field skips are not hardware proof. Image equality here is equality of published hash manifests, backed by unchanged image inputs and token checks; the reviewer did not rebuild the images. The census documents external-runner and runtime-rebinding limits. Those limits do not excuse the explicit prohibited names demonstrated in F1.

Portable reproduction, with `ROOT` the exact checkout and `PACKET` this directory:

```sh
python3 "$PACKET/census_matrix.py" "$ROOT"
python3 "$PACKET/dynamic_launch_probe.py" "$ROOT" "$PACKET/scratch/dynamic"
python3 "$PACKET/focused_checks.py" "$ROOT" "$PACKET/scratch/focused"
python3 "$PACKET/structure_checks.py" "$ROOT" "$PACKET"
python3 "$PACKET/verify_checkout.py" "$ROOT"
```

The first two exit 1 at this head because they expose F1. The next three exit 0. `run_receipt.py` records output and return codes separately and confines temporary files to packet scratch. Prior scripts and manifests are included under `prior-probes/`; the modifying R584 replay ran only in a separate disposable clone. Source bytes in the review clone were never modified. Only files listed in `MANIFEST.sha256`, plus this report, are publishable; scratch is excluded.

R585-9 FINISHED
