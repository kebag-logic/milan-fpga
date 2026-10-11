[R585] NEGATIVE - exact head 4cab445aa2475903b6cf8b87566d2c8a1e15e391

External independent review, R585-7, issue #697 / PR #705. Tree: `52c4164caae5e10e56f80313b5e556827da30d94`.

Two MINOR findings remain: the shared stack pin check accepts altered bytes when a Git tree replacement is installed, and the firmware README understates the negative-control population. No current protocol or RTL behavior defect was found. All five lenses were applied. This is not merge approval.

## Scope and reconstruction

The review followed AGENTS.md and CONTRIBUTING.md, docs/README.md, the issue body and public decisions, linked requirements and interfaces, the requested diff and history, then public executable evidence. An independent provisional verdict and five-lens ledger were written before opening prior public review findings. No other reviewer's evidence packet or private author material was consulted.

The controlling scope is the [consumer-lane assignment](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6091228902), with the [pin interpretation](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6092176555): consume the already imported MIT stack as a pinned submodule, remove duplicate cores and core tests, preserve platform behavior and image bytes, hold both dependency directions, and retain coverage and mutation detection. The separate repository import and later ADP behavior fix are outside this lane. `acmp_nvm.c`, AECP and the FPGA platform remain here. lwSRP remains separately pinned and licensed.

The requested `8b61b70902f3ebf118e56967277e2686731081bd..4cab445aa2475903b6cf8b87566d2c8a1e15e391` diff and history include the intervening AECP/F5 dev merge. The [public round-2b decision](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6093389868) requires retaining that work and comparing integrated images/coverage against `aef7ac66605c4404900ce04cbaaeff88e41bb880`. I used that distinction when identifying migration changes; the requested original diff was not replaced by a narrower diff.

Authorities examined include REQUIREMENTS.md's bare-metal ownership and placement rules; docs/overview/ARCHITECTURE.md; the hardware/software split and mailbox interface documents; control and coverage READMEs; the pinned stack's public headers, README and porting contract; docs/reference/SUBMODULES.md; and docs/testing/CI_WORKFLOWS.md. No IEEE or Milan clause changes in this migration, and this review makes no new protocol-certification claim.

Later public decisions matter to the result:

- [Round 2](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6092628778) requires actual file hashes against the gitlink, including scripts/CMake and edits hidden from status. F1 is against that requirement.
- [Round 6](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6102039501) permits documented compiler-capture exceptions. The shell-path probe below is such an accepted limit.
- [Round 7](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6104711137) makes actual compiled sources and their dependency outputs the population. The store and platform-header regressions are now caught.
- [Round 8](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6105928035) separates boundary builds from the suites. The [latest budget ruling](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6107349992) accepts this lane's two new jobs and assigns remaining firmware-unit headroom to #716. It is not reopened here.

## Findings

### R585-7-F1 - MINOR - Conformance, Robustness, Tests, Docs

**Artifact:** `sw/firmware/ctrl/test/ctrl_build.py:225` (`stack_pin`'s `git ls-tree`), `ctrl_pin.py:248` (standing pin controls), `sw/firmware/ctrl/README.md:164` (content-proof claim).

**Title:** A replacement tree changes the pin check's expected bytes while HEAD still names the required pin.

**Authority/evidence:** The round-2 decision requires comparison with the gitlink's blob hashes, and `stack_pin` promises that every gate builds the pinned stack or none. Its Git subprocesses inherit replacement-object behavior. `ls-tree` can therefore describe substituted objects instead of the canonical gitlink's tree. CONTRIBUTING.md:474 explains this same hazard for the separate xvlog gate and explicitly disables replacement objects there; that is corroborating repository precedent, not a claim that this firmware gate is xvlog.

`pin_probe.py` reproduces this in a disposable clone, without creating a commit:

1. The unmodified stack at `1a9f651cdf7846b8e10ac246a6ef6916960fbb92` is accepted.
2. Changing `include/adp.h` from `ADP_ADVERTISE_MS 5000u` to `9000u` is normally refused by name.
3. A Git replacement maps the original include tree `2c46991181d8eec39f2b6c054b328f15b5c07073` to a tree containing the altered blob. HEAD remains the required pin.
4. The compiler reads `ADP_ADVERTISE_MS 9000u`, and `stack_pin` accepts the checkout as the required pin. Reading the original object with replacement disabled still yields the original bytes.
5. Removing the replacement and restoring the header restores clean acceptance.

Receipt: [pin-probe.log](pin-probe.log). Exit 0 means the reproduction completed; its `ESCAPED` line is the defect. All 20 existing pin controls pass in [selected-controls.log](selected-controls.log), demonstrating that they do not detect this case.

**Impact:** A checkout with a replacement ref can build changed stack code while reporting that it proved the published pin. Every entry point using the shared helper inherits the gap. This does not show that the published source receipts used altered code: the actual review checkout and required submodules were independently verified against canonical objects. Severity is MINOR because the escape requires this local Git state and no such state or changed source exists at the published head.

**Required outcome:** Git operations contributing to the expected pin/tree proof must read canonical objects irrespective of replacement refs. A standing control must alter a real tree or commit through Git replacement, retain the required HEAD, and require a named refusal before any build. The existing content-proof claim must then hold.

**Verification:** Re-run `python3 -B pin_probe.py <checkout> <packet>/scratch`; the replacement case must be refused while the clean case passes. Re-run the source-owned pin and affected entry-point controls. Include a replacement tree as well as any replacement-commit control chosen by the implementation.

### R585-7-F2 - MINOR - Docs

**Artifact:** `sw/firmware/ctrl/README.md:151`; `sw/firmware/ctrl/test/ctrl_plants.py`; `ctrl_boundary.py:372`.

**Title:** The firmware-side self-test contains 96 negative controls, not 95.

**Authority/evidence:** Acceptance 4 requires current gate documentation. The README states 95 defects and eight passing controls after a shared base. `PLANTS` contains 109 entries: 101 negative and eight passing. Five negative entries belong to the Verilator run. Thus the firmware run is **96 negative + eight passing + one shared base = 105**. `structure_check.py` inventories the population; the published `round8/logs/bjob-final.log` reports 105 boundary controls and zero misbehaved. `controls()` selects that population by scope.

**Impact:** The authoritative numeric account disagrees with code and its receipt. This changes a figure, so it is MINOR under this review's rule, not prose RESIDUE.

**Required outcome:** Replace `95 defects` with `96 defects` at README line 151, preserving the eight passing controls and separately described shared base/five Verilator controls.

**Verification:** Count `PLANTS` by `needs` and empty/nonempty `needle`; reconcile 105 for firmware, six for the Verilator-only run, and 110 for a combined run with one shared base.

### R585-7-RS1 - RESIDUE - Docs

**Artifact:** PR #705 body, Status and final Known limitations bullet, snapshot examined during this round.

**Title:** Publishing-status prose still says the already published round needs a push.

**Authority/evidence:** The PR API reports the assigned published head, and its hosted runs have finished. This is stale publishing-status wording only.

**Impact:** A reader can mistake historical preparation text for current publishing state.

**Exact fix:** In the Status paragraph for `4cab445aa2475903b6cf8b87566d2c8a1e15e391`, replace `not pushed; REVIEW READY` with `published; REVIEW READY`. In the final round-8 Known limitations bullet, replace `its hosted figures need a push` with `its hosted run is linked in the manager's round-8 ruling`, linking issue comment `6107349992`. Delete the equivalent `not pushed` phrase from the historical round-7 Status paragraph. These edits change no reported figures or verdicts.

**Verification:** Read those three phrases after the body update. This item affects neither verdict nor lens cleanliness.

## Independent evidence and acceptance

All disposable builds, captures, copied trees and Git objects stayed in `scratch/`. Independent checks ran concurrently through foreground coordinators, within the 16-job cap; none was left running. Publishable command output substitutes only local checkout/scratch/home prefixes where applicable. Original local-path outputs remain in unpublished scratch. `public-evidence/` files are unmodified public downloads; `sources.json` records URLs and hashes.

| Check | Result and receipt | What it establishes |
|---|---|---|
| Seven moved C/header files | Token-identical, including literals; [structure.log](structure.log), [structure_check.py](structure_check.py) | ADP/ACMP/MAAP and wire semantics preserved. The only surviving first-party production C/H change after the inherited dev merge is a token-identical comment change in `mbx_wire.h`. |
| RTL and pins | No HDL or processor-pin change; lwSRP, processor, gPTP and axis pins unchanged | No changed CDC, reset, datapath, width or backpressure implementation in this lane. |
| Control firmware suite | `test_ctrl_firmware.py --require-rv32 --jobs 4 --build-dir <scratch>/ctrl`: PASS, 317 s; [ctrl-suite.log](ctrl-suite.log) | Host and RV32 functional arms, including integrated AECP, execute successfully. This invocation did not run the full mutation campaigns. |
| Coverage | `fw_coverage.py --check --jobs 4 --keep <scratch>/coverage`: PASS, 30 files, 267 s; [coverage.log](coverage.log) | 100% after documented exclusions for every measured file, including the stack and store. |
| Coverage controls | `fw_coverage.py --selftest`: 29/29; [coverage-selftest.log](coverage-selftest.log) | Reader detects planted drops and stale/mismatched exclusions; new stack paths are measured and tests/examples excluded. |
| Donor boundary | `third_party/tsn-c-stack/scripts/check_boundary.py --selftest --jobs 4 --work <scratch>/stack-boundary`: exit 0, 19 s; [stack-boundary.log](stack-boundary.log) | Compiler dependency/object-symbol checks and positive/negative controls pass independently. |
| Focused dependency controls | 17 selected controls all expected; [selected-controls.log](selected-controls.log), [selected_controls.py](selected_controls.py) | N1/store reach and Q7/platform `stdbool.h` shadow refused through the real image compile function. Shape conditions, patsubst, mid-string modes, driver/response/imacros forms and generated/copied C++ inputs detected. Two clean controls pass. |
| Standing pin controls | 20/20 expected, same receipt | Edited core/test/script/CMake, hidden edit, extra header, other revision, differential/AECP guards and standalone mailbox targets refused. F1 is a separate escaping control. |
| Independent small boundary probe | Public header passes; firmware-to-private and stack-to-platform reads fail; direct absolute compiler bypass recorded; [boundary-probe.log](boundary-probe.log) | Both directions work on independent minimal inputs. Absolute compilation through a shell escapes recording, as the public decision and README permit. |
| CI/doc consistency | `ci_events.py --check`: 1902 items; submodule/decoded diagram checks pass | New required-job/aggregate wiring and six documented gitlinks agree. Diagram also visually inspected. |
| Public image receipts | 35 dev/head manifest rows byte-identical; [public-evidence-comparison.log](public-evidence-comparison.log) | Published source evidence supports byte preservation at all shipped shapes/compositions. These images were not independently relinked here. |

The focused dependency script exercises actual compilation and dependency judgment. It does not replace the required-builder-population check; that wiring was read and its complete execution assessed from author receipts and the exact-head hosted job. Its first invocation failed because the reviewer script referenced a nonexistent `Deps.rc` attribute. The script was corrected and every selected control rerun successfully. [selected-controls-initial-error.log](selected-controls-initial-error.log) preserves that attempt; it is not a repository finding.

The ratchet's `srp_mbx.c` row changes from 515/515 to 514/514 without lowering the enforced fraction (`fw_coverage.compare`). The same published compiler measures 514/514 in both dev and head receipts, while this review's newer compiler measures 515/515. The source is unchanged. No lost covered statement or weakened exclusion was found. Moved ratchet rows retain their counts at their new paths.

The table holds 471 parent control mutants. Path/anchor migration and the two changed killer strings were inspected against moved code/tests. The public round-8 receipt reports identical 845 verdict lines and 471/471 detected, preserved AECP/SRP results, 435 store tests, unchanged coverage and 35 image hashes. These are the author's published source-validation receipts, including explicitly identified earlier heads whose loaded artifacts are unchanged here. They are not a manager source bank. Full mutation campaigns were not independently repeated.

Acceptance 1, 3 and 5 have supporting source, structural and public executable evidence. Acceptance 2's dependency rules work on the examined compiles, but mandated pin assurance is incomplete (F1). Acceptance 4 preserves the examined coverage/build integration, but standing pin coverage and documentation need F1/F2 resolved.

## Prior public findings: disposition at this head

All prior findings were read after the independent pass. These dispositions use current artifacts and this round's evidence. Historical prose fixes were assessed against the current PR body; new stale publishing-status phrases are RS1 above.

| Prior IDs and public round | Disposition | Current artifact/evidence |
|---|---|---|
| R584-1-F1; R585-1-F2 ([round 1](https://github.com/kebag-logic/milan-fpga/pull/705#issuecomment-6092623741)) | RESOLVED: differential/mailbox entry points call the guard before builds | `maap_differential.py`; mailbox Makefile:79,82,91,115; own 20 pin controls. New F1 is a different weakness in the guard. |
| R585-1-F1; R584-1-S2 (promoted) | RESOLVED for the assigned actual-compile population: modes and stack tests judged | Recorder and `ctrl_boundary.py:211`; standing plants, complete published receipts and own dependency controls. |
| R584-1-S1; R585-1-S1 (promoted) | Original hidden-edit/script/CMake/extra-file cases RESOLVED; canonical-byte claim incomplete under NEW F1 | `ctrl_build.py:211`, `ctrl_pin.py:248`; own controls and replacement probe. lwSRP's separate status-based check remains optional/outside this submodule scope. |
| R584-2-F1; R585-2-F1 ([round 2](https://github.com/kebag-logic/milan-fpga/pull/705#issuecomment-6094869698)) | RESOLVED: actual image shapes and C++ reaches replace synthetic C-only/1-by-1 assumptions | `ctrl_runs.image_runs`, `ctrl_boundary.targets/findings_of`; own shape/C++ controls; public image manifests. |
| R584-2-F2; R585-2-F2 | RESOLVED: standalone `run-if2` pinned | Makefile:115; poisoned standalone and missing-prerequisite controls passed. |
| R584-2-S1; R585-2-S1 (promoted) | RESOLVED: split arguments go to the compiler's expansion | `ctrl_expand.py`, recorder; standing split-argument plants and own representative driver controls. |
| R584-3-F1; R585-3-S2 ([round 3](https://github.com/kebag-logic/milan-fpga/pull/705#issuecomment-6095873264)) | RESOLVED: differential C++ input captured where its builder runs | `ctrl_configs.BUILDERS`, workflow:350, differential replay control; published Verilator boundary receipt and executed job. |
| R585-3-F1 ([round 3](https://github.com/kebag-logic/milan-fpga/pull/705#issuecomment-6096142856)) | RESOLVED under latest ruling: jobs finish and boundary capture leaves unit job | Workflow:247,311,350; exact-head durations below; shared remaining headroom assigned to #716. |
| R585-3-S1 (promoted); R584-3-S1 multi-word part; R584-4-F2; R585-4-F1 ([round 4](https://github.com/kebag-logic/milan-fpga/pull/705#issuecomment-6097795358)) | RESOLVED: actual compiler arguments replace static spelling inference | Capture/expansion/recorder; own patsubst and f-string controls; standing foreach/no-space/split/computed controls. |
| R584-4-F1 ([round 4](https://github.com/kebag-logic/milan-fpga/pull/705#issuecomment-6097725381)) | RESOLVED: compiled inputs/dependencies hold computed and generated text | Own wildcard, iterdir, f-string include and copied-template controls detect prohibited C++ header. |
| R584-5-F1; R585-5-F1 ([round 5](https://github.com/kebag-logic/milan-fpga/pull/705#issuecomment-6102035089)) | RESOLVED: compiler reads response, long-option, preprocessor and forced-file forms | Own `-Wp`, `-Xpreprocessor`, both long define forms, response and imacros controls; expansion/recorder. |
| R584-5-F2 ([round 5](https://github.com/kebag-logic/milan-fpga/pull/705#issuecomment-6101961588)) | RESOLVED: required Verilator job captures mailbox, differential and both AECP references | Known builders, `aecp_wire.py --every`, workflow:350, V1/V2/V3 plants; six-control public receipt and executed job. |
| R585-5-S1; R584-5-S3 | RETAINED DOCUMENTED OPTIONAL LIMIT: isolated Python, shell/compiled helper absolute compiler paths | README and round-6 decision. Own shell probe reproduces it; direct Python bypass is detected. No current builder using the escaping route found. |
| R585-5-S2 (promoted) | RESOLVED: old silent 256-header truncation removed by actual dependencies and refusal on failed/incomplete output | Recorder collection/capacity/error paths, `ctrl_capture.Source.error`, `ctrl_configs.expanded`; no silent 256-entry stop remains in the examined path. |
| R584-6-F1; R585-6-F1; R585-6-F2 ([round 6](https://github.com/kebag-logic/milan-fpga/pull/705#issuecomment-6104708471)) | RESOLVED: store population and per-compile include resolution are compiler-derived | `ctrl_boundary.py:211`; own N1/Q7 image-compile controls refused by name. |
| R584-6-S1 | RESOLVED | README:103 documents reliance on `tests/acmp_fake.hpp`. |
| R584-6-S2 | RETAINED SUGGESTION: executable mode not checked by `stack_pin` | `ctrl_build.py:237` checks symlink type/bytes, not executable bit. Current callers run scripts through interpreters. This review's integrity check verifies modes. |
| R585-2-S2, carried through rounds 3-6 | RETAINED SUGGESTION: alternate `--stack` still uses default `STACK_TESTS` in AECP arms | `aecp_arms.py`, `ctrl_build.STACK_TESTS`; default invocation pins the tree it uses. |
| R584-3-S1 remainder | Forced-header constant concern SUPERSEDED by dependency output; static ignored-pin-error check remains OPTIONAL | Actual `-include` dependencies recorded. Static prerequisites alone do not reject ignored errors; mandatory poisoned-target controls exercise failure. |
| R584-4-S1/S2; R585-4-S1/S2; R584-5-S1/S2; R585-5-S3; R585-6-S1 | Hosted-budget documentation UPDATED; shared unit headroom RETAINED under #716 | CI_WORKFLOWS budget section, current workflow and durations. Added boundary runtime removed from unit job. |
| R584-2-R1; R585-1-R1..R5; R585-2-RS1..RS3; R585-3-RS1; R584-4-RS1; R585-4-RS1; R584-5-RS1; R585-5-RS1; R584-6-RS1; R585-6-RS1 | Prior quoted version-specific wording corrected or superseded; new publishing-status instances are RS1 above | Current body uses public links and past hosted results without the cited duplicates, scopes act self-test to a disposable boundary, and ADP exclusion rows cite the porting guide. Evidence now exists at the supplied public commit. |

## Exact-head hosted evidence

[hosted-jobs.json](hosted-jobs.json) records read-only observations of runs at the assigned `head_sha`. These jobs executed successfully; success is not inferred from a skipped aggregate:

| Job | Result | Duration |
|---|---|---|
| [firmware-boundary](https://github.com/kebag-logic/milan-fpga/actions/runs/38124499476/job/114426026743) | success; boundary step executed | 13:34 of 30:00 |
| [firmware-verilator](https://github.com/kebag-logic/milan-fpga/actions/runs/38124499476/job/114426026831) | success; boundary step executed; cached simulator used | 10:31 of 40:00 |
| [firmware-unit](https://github.com/kebag-logic/milan-fpga/actions/runs/38124499476/job/114426026755) | success; firmware, store and coverage steps executed | 34:41 of 45:00 |
| [rtl-fast](https://github.com/kebag-logic/milan-fpga/actions/runs/38124499476/job/114432085405) | success | aggregate |
| [verilator-suites](https://github.com/kebag-logic/milan-fpga/actions/runs/38124499487/job/114434697947) | success; five workers and ownership/SHA/log reconciliation executed | aggregate |
| [yosys-portability](https://github.com/kebag-logic/milan-fpga/actions/runs/38124499487/job/114434725512) | success; four workers and SHA/inventory reconciliation executed | aggregate |

Docs and elaborate also succeeded. Some shard steps were skipped according to their partition, and simulator compilation was skipped on cache hits. **Physical gPTP calibration: NOT RUN**; its nightly/manual job was skipped. Field skips and simulated results are not hardware proof. Hosted/act acceptance remains the manager's duty.

## Reviewer-owned lens ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1) | Frozen issue scope/decisions; REQUIREMENTS.md; stack headers/porting contract; token proof; image manifests; `ctrl_build.py:211` | R585-7 applied; no clean coverage banked | 4cab445aa2475903b6cf8b87566d2c8a1e15e391 |
| RTL | CLEAN | Requested diff/history; unchanged HDL/processor gitlinks; mailbox contract; build source/link order; image builders; structure/integrity receipts | R585-7 | 4cab445aa2475903b6cf8b87566d2c8a1e15e391 |
| Robustness | UNCLEAN (F1) | Boundary/capture/expansion/recorder; N1/Q7/generated-input controls; pin controls; replacement and bypass probes | R585-7 applied; no clean coverage banked | 4cab445aa2475903b6cf8b87566d2c8a1e15e391 |
| Tests | UNCLEAN (F1) | Migrated tests/mutation tables; functional arms; coverage and controls; boundary plants; pin controls; public source receipts and executed jobs | R585-7 applied; no clean coverage banked | 4cab445aa2475903b6cf8b87566d2c8a1e15e391 |
| Docs | UNCLEAN (F1, F2) | Control README:151,164; coverage README/ratchet; submodule map/diagram; CI policy/workflow contract; issue and PR claims | R585-7 applied; no clean coverage banked | 4cab445aa2475903b6cf8b87566d2c8a1e15e391 |

[R585] PASS RTL - requested diff, `structure.log`, `integrity.log`, mailbox interface authorities - relocation/build integration preserve the examined RTL/reset/CDC/width/backpressure interfaces; no RTL or processor-pin change is introduced by this lane.

The other four lenses were fully applied but cannot be clean with F1/F2 open. SUGGESTION and RESIDUE items do not affect this ledger.

## Limits, restoration and manager duties

- This is source review plus focused execution. No full parent, processor, gPTP, Yosys or builder bank was run here. No hardware, Docker/act, host act orchestrator/self-test, shared install, source fix, commit, push, GitHub write, author contact or sub-agent was used.
- The assigned simulator identity was verified as 5.050; no independent simulator suite ran here. `environment.txt` records native compiler/test-library versions. Native coverage differs in one line count from the published older compiler, as explained above.
- There is **no manager source bank at this exact head**. Source validation is the author's published receipts plus the focused independent checks above. Neither substitutes for the final current-dev merge candidate.
- `verify_checkout.py` reads canonical objects with replacement disabled and checks actual bytes, executable/symlink modes and index entries. It checks HEAD/tree, all six root gitlinks, the five required populated submodule HEADs and their tracked bytes/modes/index, and absence of replacement refs/unexpected index flags. [integrity.log](integrity.log): PASS for 2,282 tracked blobs across the checkout and required submodules. The probe replacement was removed from its disposable clone. The source checkout has no tracked changes.
- The manager must obtain fixes and independent re-review of F1/F2, carry RS1 to the residue checklist, and maintain the reviewer-owned exact-head ledger. Changes affecting a lens invalidate its coverage until reviewed at a containing head.
- At merge, the manager must validate the current-dev candidate, with source base `8b61b70902f3ebf118e56967277e2686731081bd` and stated live dev `ac2c5e77bba1c0ae20ce2f69f711a1d17ead94a5` (or its then-current successor), run required builder/native banks, and link receipts on the PR. Hosted/act acceptance, the other independent review, no rounds in flight, explicit maintainer merge authorization, post-merge containment and issue closure remain pending duties.

Only REPORT.md and files listed in MANIFEST.sha256 are publishable. `scratch/` is excluded.

R585-7 FINISHED
