[A325] #567 handoff

Status: committed local author handoff; all 31 final gate results have rc 0. Independent review remains pending. The public ROM-ledger acceptance conflict is unresolved.

Head: `1912c0472635ea174f1a2e2de2f3c96d09f55e9b`
Branch: `567-pp-pin-0922e434`
Base: `7eb3b0d4a6987fd2e93ffc3b5be125267df7f53a`
Processor: `990f96526bb89356c963a260ebbdcf2a77e6623a` -> `0922e43408f891fc0b84a84691df86b4fd0f1c0d`
Executor: [A325]. Independent reviewers: [R326] internal, [R327] external.
Assignment: https://github.com/kebag-logic/milan-fpga/issues/567#issuecomment-5844866743

## Change list

| File:line | Change |
|---|---|
| `protocol-processor:1` | Advance only the gitlink to the assigned merged processor pin. |
| `docs/reference/SUBMODULES.md:25` | Current full pin. |
| `docs/reference/SUBMODULES.md:44` | Adoption notes, inventory invocation, unchanged ROM inputs and ledger conflict. Remove the repaired MVU enable-name conflict from the conflict table. |
| `tb/verilator/milan_dp/README.md:520` | Current adopted-pin reference; retain historical measurements and source links. |
| `CHANGELOG.md:34` | Adoption entry and generated Contents entry. |
| `docs/diagrams/submodule_boundaries.drawio:1` | Regenerated master with current pin text. |
| `docs/diagrams/submodule_boundaries.svg:29` | Regenerated vector render. |
| `docs/diagrams/submodule_boundaries.png:1` | Regenerated bitmap; visually inspected with direct exports. |
| `docs/diagrams/PNG_MANIFEST.json:10` | Regenerated source and raster digests for this diagram only. |

## Evidence

| Claim | Evidence | Result |
|---|---|---|
| Expected repository and lane | Origin URL, branch and base checks | Correct origin; assigned branch at assigned base before changes. |
| Processor HDL unchanged | `git -C protocol-processor diff --stat 990f9652 0922e434 -- hdl/`; `source-evidence.json` | Empty diff; both HDL trees are `d8879608b8fae8c06a505d7d5d485a97903a5766`. |
| ROM sources and images unchanged | Identical processor HDL trees; both generators read only their own constants. The newly built shadow-suite images match the previous pin's recorded SHA-256 values (`source-evidence.json`). | Acceptance 2 applies: ledger not re-recorded. |
| Parent RTL unchanged | `git diff 7eb3b0d4a6987fd2e93ffc3b5be125267df7f53a -- hdl/` | Empty diff. |
| Complete processor inventory | `parameter-inventory.log` | 24 top, 24 guide, 24 diagram parameters; PASS. |
| Parent parameter bindings | `PARAMETERS.md`; `hdl/milan/KL_pp_shadow.sv:1057` | All 14 explicit bindings exist in the inventory and pass through; 10 parameters retain unchanged processor defaults. |
| Shadow integration | `pp-shadow.log` | Three default configurations; 402 checks each, zero failures. |
| NVM behavior and controls | `nvm-firmware.log`, `nvm-capture.log` | Five shapes pass; every planted NVM defect rejected. |
| Documentation export | `docs-check.log`, `docs-check-no-git.log` | Git and filesystem modes pass. |
| CI policy and controls | `ci-events-check.log`, `ci-events-selftest.log` | PASS; 1,655 contract items, 2,197 control arms. |
| Hardware-language analysis | `xvlog.log`, `rtl-lint.log` | Ratchets pass: four existing processor parse findings; 90 existing lint findings. Budgets unchanged. |
| Behavior suite | `behave.log` | 344 scenarios, 1,739 steps; zero failed or skipped. |
| Generated diagram | `VISUAL.md`, diagram gates | Committed render, direct master export and A4 print inspected; current pin legible. |
| Source population | `rtl-source-lists.log` | All four consumer lists cover the 106-file closure; six existing processor synthesis-top omissions remain recorded. |
| Submodule cleanliness | `git submodule foreach --quiet --recursive 'git status --short'` | No tracked or untracked changes in active submodules. Unused external import remains uninitialized. |

## Gate table

Commands ran in the foreground without pipelines. Individual validation timeouts were four hours. `run_gates.py` records return codes and logs; `builder_modes.py` runs the complete `sw/builder/test_builder.py` in each requested mode. The SDK mode remaps only the existing absolute compiler selector to the supplied read-only SDK, preserving other arguments; `--require-rv32` remains enforced. Absent mode hides the three cross-compiler candidates and retains normal host probes. Neither changes the tests or the installed compiler.

| Gate command | rc | Evidence |
|---|---|---|
| `python3 protocol-processor/scripts/check-integrator-params.py` | 0 | `parameter-inventory.log` |
| `python3 sw/firmware/nvm_hosttest/test_nvm_firmware.py --self-test` | 0 | `nvm-firmware.log` |
| `python3 scripts/check_nvm_capture.py` | 0 | `nvm-capture.log` |
| `python3 scripts/check_baremetal_only.py --check` | 0 | `baremetal-only.log` |
| `python3 -B scripts/docs_check.py` | 0 | `docs-check.log` |
| `python3 scripts/ci_events.py --check` | 0 | `ci-events-check.log` |
| `python3 scripts/ci_events.py --selftest` | 0 | `ci-events-selftest.log` |
| `python3 scripts/check_em_dash.py --base 7eb3b0d4a6987fd2e93ffc3b5be125267df7f53a` | 0 | `em-dash.log` |
| `python3 scripts/check_doc_style.py` | 0 | `doc-style.log` |
| `python3 scripts/gen_toc.py --check` | 0 | `toc-check.log` |
| `python3 scripts/gen_toc.py --verify-anchors` | 0 | `toc-anchors.log` |
| `python3 scripts/check_doc_paths.py` | 0 | `doc-paths.log` |
| `python3 docs/traceability/gen_module_matrix.py --check` | 0 | `module-matrix.log` |
| `python3 scripts/xvlog_gate.py --check` | 0 | `xvlog.log` |
| `python3 scripts/check_rtl_source_lists.py` | 0 | `rtl-source-lists.log` |
| `python3 scripts/check_sv_idiom.py` | 0 | `sv-idiom.log` |
| `python3 scripts/lint_rtl.py --check` | 0 | `rtl-lint.log` |
| `python3 scripts/check_cpp_idiom.py` | 0 | `cpp-idiom.log` |
| `python3 scripts/check_py_idiom.py` | 0 | `py-idiom.log` |
| `python3 scripts/check_port_contracts.py` | 0 | `port-contracts.log` |
| `python3 scripts/measure_naming.py --check` | 0 | `naming.log` |
| `python3 scripts/measure_test_evidence.py --check` | 0 | `test-evidence.log` |
| `cd tests && behave --no-capture -f plain` | 0 | `behave.log` |
| `git diff --check` | 0 | `diff-check.log` |
| `python3 scripts/check_submodule_docs.py` | 0 | `submodule-docs.log` |
| `python3 docs/diagrams/submodule_boundaries.gen.py --check` | 0 | `submodule-diagram.log` |
| `python3 scripts/check_diagram_pngs.py` | 0 | `diagram-pngs.log` |
| `python3 -B scripts/docs_check.py` (filesystem mode, no Git metadata) | 0 | `docs-check-no-git.log` |
| `python3 builder_modes.py sdk` | 0 | `builder-sdk.log` |
| `python3 builder_modes.py absent` | 0 | `builder-absent.log` |
| `make -C tb/verilator/pp_shadow` | 0 | `pp-shadow.log` |

## Setup and bounded evidence

Run the helpers from the candidate checkout, locating `builder_modes.py` and `run_gates.py` in this evidence directory. `final-gates.json` binds their results to the committed head. The no-Git gate uses a disposable metadata-free export under `/tmp`, removed after execution; no tree export or build environment resides in this directory.

The full absent-compiler builder passed with all three cross candidates hidden. Its two NOT RUN arms are gate 1b's compiled firmware instruments and gate 11's absent calibration report. Compiler-dependent mutations are skipped in this mode, not counted as rejected. The SDK run covers the compiler instruments.

The full SDK builder passed with 855 audited compiler invocations. Its one NOT RUN arm is gate 11's historical resource calibration, because the required place-utilization report is absent. This is not firmware or parameter coverage, and no calibration result is claimed.

The repository's hash-locked Markdown dependencies were installed in `/tmp/567-a325-venv`, outside the evidence directory. The first TOC regeneration refused missing `html5lib`; regeneration and all subsequent renderer gates passed after setup.

The first no-Git export omitted empty submodule directories and produced five broken directory links. The export harness was corrected to retain those directories, matching a checkout without initialized submodules; no repository source was changed for this. The corrected filesystem-mode check passed. Initial evidence is retained in `docs-check-no-git-initial-export.log` and `no-git-initial-export-results.json`.

No exhaustive synthesis, hosted CI, hardware execution, independent verdict or merge readiness is claimed. This lane is the assigned local author handoff only.

## Open acceptance conflict

Acceptance 2 allows ROM digest re-recording only when processor ROM sources change. They do not change here, so `syn/yosys/rom_digests.tsv` remains byte-identical to the base (SHA-256 `359113b6300ef27b6914c56c1e3c810b43fe06eef3a41fe2fb1fe43a6d9f63b1`).

The separate OOC path requires exact-pin rows at `syn/yosys/ooc.sh:464`; no rows exist for `0922e434`. Leaving the ledger unchanged therefore prevents that path from accepting the pin. A public acceptance decision is required before changing the ledger. The issue disclosure is https://github.com/kebag-logic/milan-fpga/issues/567#issuecomment-5844889430. No waiver or successful OOC result is inferred.

## Acceptance disposition

| Criterion | Disposition |
|---|---|
| 1: pin, current references, regenerated diagram, changelog | Met. |
| 2: conditional ROM re-recording | Met literally: sources and generated images unchanged; ledger unchanged. |
| 3: parent gates and processor inventory | Assigned gate set passes. Broader OOC acceptance remains unresolved because the new pin lacks digest rows. |
| 4: no parent RTL change | Met; empty parent HDL diff. |

## Handoff boundary

The scoped commit is local, with a clean worktree and clean active submodules. `PR-BODY.md` is prepared for subsequent publication. `REVIEW-READY.md` contains the final issue comment; posting it to #567 is the final authorized action. No push, PR action, merge, additional checkout, hardware operation or donor source edit was performed. Independent review and the public ROM-ledger decision remain outstanding.
