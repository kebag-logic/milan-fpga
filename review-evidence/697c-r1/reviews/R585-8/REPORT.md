[R585] NEGATIVE - exact head feed95bbb6429e5af0ee3f0a24c531777279e9de

External independent review R585-8 of issue #697 / PR #705. Tree: `434e9291e6ceb5bd32bcd63fd13f257ed6d82bed`. All five lenses were applied. One new MINOR remains open; one publishing-status RESIDUE is recorded. The two previous rounds' replacement-object and README-count defects are resolved at this head.

The current pin proof refuses the examined substitutions correctly. The remaining defect is in the newly mandated census: its search for literal program names does not enforce the ruling that every Git process uses the helper.

Reconstruction and scope

I read AGENTS.md / CONTRIBUTING.md, docs/README.md, the issue body and public scope decisions, then requirements and interface authorities. These included REQUIREMENTS.md, docs/reference/SUBMODULES.md, the mailbox contract, firmware documentation, and the pinned stack's architecture/porting contracts. The [lane assignment](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6091228902), [pin ruling](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6092176555), and [round-9 ruling](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6107732413) govern this review.

I reconstructed `8b61b70902f3ebf118e56967277e2686731081bd..feed95bbb6429e5af0ee3f0a24c531777279e9de`, separating inherited F5 changes through `aef7ac66` from this lane. The focused delta is the three commits after `4cab445aa2475903b6cf8b87566d2c8a1e15e391`: `2d24214d`, `107aab30`, and `feed95bb`. Only `ctrl_build.py`, `ctrl_pin.py`, `ctrl_boundary.py`, and the firmware README change in that delta.

Public executable evidence was read from [the supplied evidence commit](https://github.com/kebag-logic/milan-fpga/tree/5209b0ecaed3917de031ecd6320a0465ae30cbf5/review-evidence/697c-r1) and the [round-9 source-validation comment](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6108314179). No private author material was read. I wrote my independent verdict and ledger before reading prior public reviewer findings, then reconciled those findings and replayed their prescribed probes. No parallel review report was read.

R585-8-F1 - MINOR - Conformance, Robustness, Tests, Docs

**Artifact:** `sw/firmware/ctrl/test/ctrl_pin.py:111`, especially the `ast.Constant` search at line 128; `ctrl_build.py:249`; `sw/firmware/ctrl/README.md:175`; PR #705 Status's claim that the census refuses any Git command started outside the helper.

**Title:** The census accepts a helper bypass when the executable comes from a computed name.

**Authority/evidence:** The round-9 ruling requires a census that fails if a pin-proof module starts Git other than through the helper. It explicitly rules this class by construction. The implemented census examines string/byte constants and the helper's environment; it does not check the process-launch route.

The portable [census probe](scripts/census_probe.py) changes only an in-memory copy of the proof's `ls-tree` call, saving that copy in unpublished scratch:

```python
# Current call:
tree = git(stack, "ls-tree", "-r", "-t", "-z", "--full-tree", pin)
# Mutant:
tree = run([git.__name__, "-C", str(stack), "ls-tree", "-r", "-t", "-z", "--full-tree", pin])
```

`git.__name__` evaluates to the executable name, but introduces no matching string constant. The exact-head census returns `[]`. Executing the mutant against disposable stack clones accepts both a replacement tree and a replacement commit hiding changed `src/adp.c`. The unchanged proof refuses both by name. [Raw result](receipts/census-probe.log), exit 0 meaning reproduction completed.

The README and source-validation comment disclose computed names as a limitation. No public scope decision accepts that exception to the round-9 ruling. The PR Status nevertheless describes an unrestricted census refusal. This affects a test guarantee and an acceptance claim, so it is not RESIDUE.

**Impact:** The new census can declare a bypass clean and does not provide the assigned structural protection against reintroducing replacement-object trust. No escaping Git call was found in the unmodified proof. Its current replacement controls do detect this particular mutant, so this finding does not claim that the complete self-test would accept that mutant or that the published source was built from altered bytes. These limits keep severity MINOR.

**Required outcome:** Enforce the helper-only process route for the pin-proof modules without depending solely on literal executable spelling. Add a planted bypass with a computed executable and require the census itself to refuse it. Keep the clean proof accepted and align the public census claim with the enforced contract. A narrower contract would require an explicit public scope decision.

**Verification:** Repeat `census_probe.py` after the change: its mutant must produce a named census refusal. Re-run the current literal-bypass/environment controls, replacement-tree/commit controls, and affected entry-point checks. Re-review the corrected head.

R585-8-RS1 - RESIDUE - Docs

**Artifact:** PR #705 body, current round-9 Status paragraph.

**Authority/evidence:** The PR API names the assigned published head and its hosted runs have completed. The paragraph still ends with `not pushed; REVIEW READY`.

**Impact:** Stale publishing-state wording only; no figure, measurement, test or conformance claim changes.

**Exact required fix:** Replace `not pushed; REVIEW READY` with `published; REVIEW READY` in that paragraph. The old round-8 and round-7 instances have been corrected; the round-8 hosted-ruling link is present.

**Verification:** Read the updated Status paragraph. Carry this recurrence of R584-7-RES1 / R585-7-RS1 to the manager's residue checklist under #495. It does not affect the verdict or ledger.

Evidence and acceptance

| Check | Result | Artifact |
|---|---|---|
| Current helper routing | Every current Git call in the two proof modules uses `ctrl_build.git`. Its subprocess receives `GIT_NO_REPLACE_OBJECTS=1` and `GIT_GRAFT_FILE=/dev/null/no-grafts`. The census's general enforcement remains F1. | `ctrl_build.py:180-202,242-249`; `ctrl_pin.py`; [focused controls](receipts/focused-controls.log) |
| Disk/tree identity | Direct Git-format blob hashing of disk bytes bypasses attributes/filters. Whole-tree comparison includes paths, directory/file/link kinds, executable modes and blobs; only the root `.git` is excluded. | `ctrl_build.py:205-260`; same receipt |
| Standing pin controls | 30/30 expected, including clean clone, replacement tree, replacement commit, graft plus edit, clean filter, mode, type, whole-tree LICENSE edit, hidden edit, census and target guards. | [focused-controls.log](receipts/focused-controls.log) |
| Every affected entry point | 17 entry points x five states = 85/85 named refusals, exit 2. States: replacement tree, replacement commit, graft plus edit, clean filter, mode. | [entrypoints.log](receipts/entrypoints.log); [portable runner](scripts/entrypoint_clone.py) |
| Prescribed previous probes | R584-7 step 3 REFUSED; R585-7 replacement control REFUSED, clean/restored controls accepted. | [R584 replay](receipts/prior-r584-probe.log), [R585 replay](receipts/prior-r585-probe.log) |
| README population | 96 firmware defects + 8 passing controls + shared base = 105; five simulation defects + base = 6; 30 pin controls. All four figure mutations refused by name. | `ctrl_boundary.py:406-441,503-512`; [focused-controls.log](receipts/focused-controls.log) |
| Moved C/header code | All seven files token-identical to `aef7ac66`; surviving `mbx_wire.h` change is comment-only. No HDL, synthesis or mailbox-contract change from source base. Existing processor, gPTP, axis and lwSRP gitlinks unchanged. | [structure.log](receipts/structure.log), [script](scripts/structure_audit.py) |
| Image preservation | All 35 published ELF manifest rows are byte-identical at dev `aef7ac66`, round 8 and round 9. Each manifest hashes to `de8ae063d8046a72b90cf180b5d1dcf129c43400cd7f139a2ea26a897c86ebd0`. No image-builder or product-source change in round 9. | Same receipt; `public/images-*.sha256` |
| Stack's own boundary | Independent `--selftest --jobs 4` PASS, including dependency and object-symbol controls. | [stack-boundary.log](receipts/stack-boundary.log) |
| CI/document wiring | `ci_events.py --check` and submodule-doc gate rc 0. Required firmware jobs and submodule fetches remain wired into the aggregate. | [ci-events.log](receipts/ci-events.log), [submodule-docs.log](receipts/submodule-docs.log) |
| Author source receipts | Exact-head boundary runs report 105/6 boundary, 30 pin and four figure controls, all expected. Published coverage remains 30 files; 845 firmware verdict lines and 471/471 kills are reported unchanged. Unit steps were executed at `107aab30`, with no loaded-module change afterward, as explicitly disclosed. | `public/logs/bjob-final.log`, `vjob-final.log`, `cov-head.txt`, `ujob-head.outer`; linked source-validation comment |
| Final checkout integrity | Parent's 1266 tracked blobs/modes and index exactly match HEAD. All five required initialized submodules match their gitlinks and canonical bytes/modes/index. No hidden-index flags or replacement refs; parent status empty. | [checkout-integrity.log](receipts/checkout-integrity.log) |

The first entry-point runner mistakenly supplied `--jobs` to a driver without that option. Its five argument-parser failures are preserved in [entrypoints-initial-error.log](receipts/entrypoints-initial-error.log). Removing that reviewer-runner option yielded all 85 named refusals. No repository change was made.

A graft changes ancestry, which this proof does not query. The graft-plus-edit control establishes refusal with that state present; it alone cannot prove sensitivity to removing the graft environment setting. The explicit environment census control covers that setting. Clean replacement/graft metadata is not prohibited outright.

Source acceptance for the selected pin, code move, image preservation, coverage and build integration remains supported by the examined source and published receipts. Round-9 census acceptance is incomplete because of F1. No manager source bank at this head is claimed or inferred.

Hosted evidence, inspected read-only

The PR was open and ready at the exact assigned head. [rtl-fast](https://github.com/kebag-logic/milan-fpga/actions/runs/38134026815), [docs](https://github.com/kebag-logic/milan-fpga/actions/runs/38134026929), [elaborate](https://github.com/kebag-logic/milan-fpga/actions/runs/38134026860), and [rtl-full](https://github.com/kebag-logic/milan-fpga/actions/runs/38134026900) concluded success. Job/step results are retained in [hosted-evidence.txt](receipts/hosted-evidence.txt).

The firmware-boundary job executed and reported 2822 compiled sources / 3049 invocations, zero findings, 105 boundary + 30 pin + four figure controls, zero misbehaved. The firmware-verilator job executed and reported 816 / 912, zero findings, six + 30 + four controls, zero misbehaved. Firmware-unit executed successfully. Five simulation shards and four synthesis shards executed successfully; both long aggregates passed. Physical gPTP was **skipped**. Its context supplies no physical evidence. Hosted and local-replica acceptance remains the manager's duty.

Prior public findings at this head

These dispositions follow the independent pass. For unchanged boundary artifacts, I checked current implementation and exact-head source/hosted control receipts; I did not repeat every historical campaign. `B` below means the exact-head published `public/logs/bjob-final.log`; `V` means `public/logs/vjob-final.log`; `P` means this review's `receipts/focused-controls.log` and `entrypoints.log`.

| Prior IDs | Disposition at this head | Current evidence |
|---|---|---|
| R584-7-F1; R585-7-F1 | RESOLVED as reported; new census obligation has F1 above | Canonical helper, P, both prescribed probes |
| R584-7-F2; R585-7-F2 | RESOLVED | Correct 96 and live population/figure mutations |
| R584-1-F1; R585-1-F2 | RESOLVED | Differential and mailbox guards, P |
| R584-1-S1; R585-1-S1 | RESOLVED for TSN stack | Whole-tree raw hashes, hidden-edit/script/filter controls, P |
| R585-1-F1; R584-1-S2 | RESOLVED | Actual-compile modes and stack-test dependencies; `ctrl_boundary.py`, B |
| R584-2-F1; R585-2-F1 | RESOLVED | Image-shape and C++ dependency controls, `ctrl_runs.py`, B/V |
| R584-2-F2; R585-2-F2 | RESOLVED | `run-if2` prerequisite, poisoned target and missing-prerequisite controls, P |
| R584-2-S1; R585-2-S1 | RESOLVED | Split-argument compiler expansion, B |
| R584-3-F1; R585-3-S2 | RESOLVED | Differential C++ builder captured, V |
| R585-3-F1 | RESOLVED under public headroom ruling | Boundary separated from unit job; executed exact-head hosted jobs |
| R585-3-S1; R584-3-S1 multi-word part; R584-4-F2; R585-4-F1 | RESOLVED | Actual compiler argument/dependency capture; computed/split/make controls, B |
| R584-4-F1 | RESOLVED | Computed/copied/generated C++ controls, B/V |
| R584-5-F1; R585-5-F1 | RESOLVED | Driver, response-file and forced-input controls, B |
| R584-5-F2 | RESOLVED | Required simulation job, both AECP references and V1-V3 controls, V |
| R584-6-F1; R585-6-F1; R585-6-F2 | RESOLVED | Store-source and per-compile include resolution; N1/Q7 controls, B |
| R584-6-S1 | RESOLVED | Firmware README documents dependency on stack test fakes |
| R584-6-S2 | RESOLVED | Executable mode comparison and its planted control, P |
| R585-5-S2 | RESOLVED | Dependency output replaces the previous silent header-text cap |
| R585-2-S2 | RETAINED SUGGESTION | Alternate `--stack` still uses default `STACK_TESTS`; default route is pinned |
| R585-5-S1; R584-5-S3 | RETAINED documented optional limit | Isolated Python / shell helper absolute compiler capture limits, firmware README |
| R584-3-S1 remainder | Forced-header concern superseded; ignored-pin-error static check RETAINED SUGGESTION | Real dependency output; poisoned target controls supplement static prerequisite analysis |
| R584-4-S2; R585-4-S1; R584-5-S2 | RETAINED SUGGESTION under #716 | Shared unit-job headroom is outside this lane per comment 6107349992 |
| R584-4-S1; R585-4-S2; R584-5-S1; R585-5-S3; R585-6-S1; R584-7-S1 | RETAINED optional documentation refresh where not already applied | CI page's figures name their historical heads accurately |
| R584-2-R1; R585-1-R1-R5; R585-2-RS1-RS3; rounds 3-6 RS1 items | Historical wording corrected/superseded | Current PR body, public links and evidence; ADP porting reference |
| R584-7-RES1; R585-7-RS1 | Old quoted phrases corrected; new round-9 recurrence RETAINED as R585-8-RS1 | Current PR Status |

Reviewer-owned completion ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN: F1 | Issue decisions; REQUIREMENTS.md; `ctrl_build.py:183-260`, `ctrl_pin.py:111-145`; structural/image evidence | R585-8 | feed95bbb6429e5af0ee3f0a24c531777279e9de |
| RTL | CLEAN | Source-base and round-9 diffs; unchanged `hdl/`, `syn/`, mailbox contract and processor pins; `tb/verilator/mbx/Makefile:40-115`; source/include/link routing; published images | R585-8 | feed95bbb6429e5af0ee3f0a24c531777279e9de |
| Robustness | UNCLEAN: F1 | Raw-tree proof, named refusals across 85 entry-point cases, 30 controls, both earlier probes, census mutant | R585-8 | feed95bbb6429e5af0ee3f0a24c531777279e9de |
| Tests | UNCLEAN: F1 | `ctrl_pin.py:111-145,315-524`; `ctrl_boundary.py:406-441,503-512`; current controls and mutation receipts; source/hosted evidence | R585-8 | feed95bbb6429e5af0ee3f0a24c531777279e9de |
| Docs | UNCLEAN: F1 | Firmware README:148-189, correct population and disclosed limitation; unqualified PR Status census claim; CI/submodule docs and source-evidence limits | R585-8 | feed95bbb6429e5af0ee3f0a24c531777279e9de |

[R585] PASS RTL - `receipts/structure.log`, `tb/verilator/mbx/Makefile:40`, and `public/images-head.sha256` - no changed RTL, clock/reset, CDC, width, ordering or backpressure implementation in this delta; imported C semantics and link inputs remain preserved against the frozen no-behavior-change scope. This is delta coverage, not a new whole-product certification.

The independent pre-reconciliation ledger marked Docs clean based on the repository's explicit limitation. Examination of the current PR's unrestricted census claim adds Docs to F1 in this final ledger. No external review verdict is used as evidence for that classification.

Limits and pending manager duties

- Independent execution was focused: pin/census/figure controls, entry-point refusals, prior probes, stack boundary, structure and CI/doc checks. Full `ctrl_boundary.py --selftest` builder runs were assessed from exact-head author and hosted receipts, not launched locally. Full parent, processor, gPTP, synthesis and builder banks were not run.
- Images were not relinked here. The 35-row equality is an independently checked comparison of public source receipts, supported by the unchanged image inputs in this delta. Coverage/campaign totals beyond focused controls are attributed to public source evidence, not a new local campaign.
- The scoped simulation compiler identity was verified as version 5.050 before inspection/probes. No heavy RTL build, privileged operation, shared installation, local workflow container, host orchestrator/self-test, hardware access, source fix, commit, push or GitHub write was performed. Disposable clones and objects stayed under packet `scratch/`. Foreground executions completed; no work is left running.
- Physical calibration **NOT RUN**. Field skips and the skipped physical hosted job are not hardware proof.
- The manager must obtain the corrected-head re-review, accept hosted/local-replica evidence, and validate the final merge candidate against current dev. Source base is `8b61b70902f3ebf118e56967277e2686731081bd`; live dev supplied for the merge turn is `6bfeeb132fa0b1ad8a5b957446c66a498e633af7`. The manager owns the candidate builder/native banks and publication of their receipts. This report neither runs nor approves that candidate.
- Merge authorization, all independent reviews complete, reviewer-accepted coverage, post-merge containment, authoritative-document updates and issue/project completion remain manager duties. Carry RS1 to #495. An open MINOR keeps the affected lenses unclean.

Only MANIFEST.sha256-listed receipts/scripts and this report are publishable. Raw local-path output, when normalized for publication, is retained under unpublished `scratch/raw/`; the only normalization is the packet path to `$PACKET`. Public downloads are unchanged.

R585-8 FINISHED
