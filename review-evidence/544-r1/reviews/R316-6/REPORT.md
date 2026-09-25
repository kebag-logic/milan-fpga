[R316] POSITIVE - exact head 7ddbbdc9be73728b239718c8976261c7e0ad0563

R316-6, independent composition review of issue #544 / PR #558. Tree: `a1813edb60d34073859f67b388a1e10d76cc86c3`. The composed tree introduces no defect beyond the reviewed sources. All five lenses are CLEAN. No new finding, and no open BLOCKER, MAJOR or MINOR within the frozen composition scope. Previously published optional suggestions remain below.

This accepts the assigned composition, not a future merge result or release. The [public review start](https://github.com/kebag-logic/milan-fpga/pull/558#issuecomment-5825863332) identifies this head. Its immediate parent is `59e7f5fd76786faa673b4522018f4e9590d294d0`; its reviewed source parent is `8383e929fab3ff57a768c88b8b1ff9b568afcf14`. The source fork is `ffcbd33de70278ae34b533dcbadde0b36c8cba13`.

I reconstructed the repository contract, documentation map, issue and public decisions, relevant requirements/interfaces, then the diff and history, then executable evidence. I completed the independent pass and wrote my own positive verdict and five-lens ledger before opening prior review bodies. Their subsequent reconciliation did not change the verdict. No private author material, private management material, or other local review packet was read.

The governing acceptance is [issue #544](https://github.com/kebag-logic/milan-fpga/issues/544), including decisions [5823832945](https://github.com/kebag-logic/milan-fpga/issues/544#issuecomment-5823832945), [5824093785](https://github.com/kebag-logic/milan-fpga/issues/544#issuecomment-5824093785), and [5825016512](https://github.com/kebag-logic/milan-fpga/issues/544#issuecomment-5825016512). Relevant authorities are `REQUIREMENTS.md` sections 1, 3 and 8; `docs/reference/REGISTER_MAP.md`; `docs/overview/ARCHITECTURE.md`; and the boot-order, editing-contract and cost-table sections of `docs/integration/BAREMETAL_FIRMWARE.md`.

**Composition and interactions examined**

The complete diff `59e7f5fd..7ddbbdc9` changes exactly two files. Both overlap the two predecessors stated in the assignment:

| File | dev(387b) predecessor | #501 predecessor | Composition result |
|---|---|---|---|
| `sw/builder/test_builder.py` | `e1333a14`, including source commit `a9636e0f`: PHC reference counts, media re-base/restart pins and controls | `2ab66c9d`, including source `b5ee412c`: census constants use MAPIN/MAPOUT_ENTRIES | Both predecessor changes and #544 identity protection retained |
| `docs/integration/BAREMETAL_FIRMWARE.md` | Media re-base/restart cost-table rows and control explanation | Generated map-entry names in saved-state documentation | All rows and explanations retained without duplicate or stale headings |

History/diff checks found no direct path overlap with queued #548 or #546. Raw three-way merging each shared file from the source fork, reviewed source and candidate parent reproduces its candidate bytes exactly, without conflict resolution. The four identity-check helper ASTs are unchanged from the source review. The source patch and candidate-parent patch also have the same stable patch identity. See [composition receipt](receipts/composition.log) and [complete candidate diff](receipts/candidate.diff).

Semantic interactions were checked beyond filename overlap:

- #501 changes the firmware consumed by the whole-unit identity scan and census. All 32 census entry keys agree with the composed firmware; no old cluster key remains in that census dictionary. The composed production firmware passes the real compiled boot contract. Record-space checks and their negative controls pass across five shipped shapes, including dynamic output-map capacity and generated record-table checks.
- #387 changes the RTL-facing portion of the same boot-contract function. The composed `media_rebase_p_w`, `mcr_restart_p_w` and render expressions agree with `hdl/milan/milan_datapath.sv:3111`, `:3143` and `:6031`. Eight targeted structural mutations retain their named refusals in each compiler mode.
- #548 changes nearby CSR comments; the identity address and default remain at `hdl/common/csr/milan_csr.sv:717` and `:1942`. The compiled read and guard still bind to these values. #546's surrounding media changes introduce no new #544 hardware delta.
- Workflow/record pins, suite inventory, generated module matrix, feature-status/boot-order registry, source-list policy, documentation tables, contents and anchors pass their candidate gates. The #544 delta itself changes no workflow, registry, firmware, RTL or gitlink.

**Focused execution and evidence**

All final commands exited zero. Commands and complete outputs are in the individual receipts; portable reproduction instructions are in [REPRODUCE.md](REPRODUCE.md).

| Check | Candidate result | Receipt |
|---|---|---|
| Focused boot contract with verified pinned SDK | 15/15 cases; production census executed | `focused-boot-sdk-final.log` |
| Focused boot contract without an RV32 compiler | 15/15 cases; compiled census explicitly did not run | `focused-boot-absent-final.log` |
| Documentation inventory modes | Git: zero findings, 23/23 scrub arms; filesystem: zero findings, 22/22, inventory-parity arm explicitly skipped | `docs.log`, `docs-no-git.log` |
| Contents and cross-page anchors | 107 contents pages; 173 fragment links reproduced | `toc.log`, `anchors.log` |
| Added-line em-dash gate against candidate parent | Zero findings; 339/339 controls | `em-dash.log` |
| Workflow contract and self-test | 1647 contract items; 2188 self-test arms | `ci-events.log`, `ci-events-selftest.log` |
| NVM record-space and self-test | Zero findings across five configurations; negative controls refused | `nvm-record-space.log`, `nvm-record-selftest.log` |
| Feature status, suite tally, module matrix | All passed; 46/46 feature controls; 69-module matrix current | `feature-status.log`, `suite-tally.log`, `module-matrix.log` |
| Documentation paths/style, Python idiom, bare-metal and derived sources | All passed | `doc-paths.log`, `doc-style.log`, `python-idiom.log`, `baremetal-only.log`, `pp-sources.log` |
| Whitespace and final exact-tree audit | Passed | `diff-check.log`, `final-tree-audit.log` |

Each focused mode checks the composed production firmware, the authorized discarded-mask read, the fifth existing fence form, both published macro spellings and their individual disconnected-check controls, and eight predecessor structural refusals. The standalone harness loads candidate code in memory and returns its helpers before the complete corpus bank. It redirects only the output directory and compiler selector; production assertions remain intact. This is focused coverage, not a full builder-bank run or RTL elaboration. No RTL compiler was used in this round.

Two initial harness setup attempts failed before a product verdict: resolving the SDK selector's symlink discarded the executable basename required by its wrapper; an empty absent-mode selector also omitted the host compiler needed for explicit stand-down. The harness was corrected to preserve the selector spelling and retain host compiler candidates in absent mode. Both initial receipts are retained as `focused-boot-sdk.log` and `focused-boot-absent.log`; the `-final` receipts carry the successful candidate results. No repository source changed.

The SDK was installed only under packet scratch and verified against archive SHA-256 `d42680e926542595c4c87629d33f5f90aac1e9a964c8955089e0514caa01b78f`; see `sdk-install.log`.

The [public source evidence](https://github.com/kebag-logic/milan-fpga/tree/4c97887dc83f46703b8d767dec671afcb9ebe206/review-evidence/544-r1) was inspected after the independent diff pass. The two source-run manifests identify `8383e929...`, exit zero, and unchanged source inputs. Their four recorded input hashes were checked against that commit's Git blobs. Their full-bank verdicts retain one NOT RUN group with compilation and two without; physical calibration is among the missing evidence. See `public-source-evidence.log`. These source receipts are not relabeled as candidate bank receipts. The assignment reports manager-owned full static/builder and native banks passing at the composition head; those banks were not rerun here.

**Prior public findings, disposition at this head**

Source coverage comes from [R316-5](https://github.com/kebag-logic/milan-fpga/pull/558#issuecomment-5825681469) and [R317-5](https://github.com/kebag-logic/milan-fpga/pull/558#issuecomment-5825847618), both POSITIVE at `8383e929fab3ff57a768c88b8b1ff9b568afcf14`. The unchanged helpers, retained fixtures and focused candidate checks preserve their dispositions:

| Prior ID | Severity and ALL attributable lenses | Disposition/evidence at composition head |
|---|---|---|
| R316-1 F1/F2 | MAJOR; Conformance, RTL, Robustness, Tests, Docs | RESOLVED in compiled mode. Absence/escape and interval-asm rules remain unchanged at `test_builder.py:5170`, `:5280`; source re-reviews cover the named wrapper/output rows. |
| R317-1 F1 | MAJOR; Conformance, Robustness, Tests, Docs | RESOLVED. Macro/plain wrapper and asm rows and their controls remain intact. |
| R316-1 F3 | MINOR; Conformance, Robustness, Tests, Docs | RESOLVED by the authorized compiler-free bound and pinned examples; `BAREMETAL_FIRMWARE.md:503`, `:1470` and the COST line retain the disclosure. |
| R317-1 F2 | MINOR; Conformance, Robustness, Docs | RESOLVED by the same header-paste/alias/apply disclosure and mode-specific fixtures. |
| R316-2 F1 | MAJOR; Conformance, Robustness, Tests, Docs | RESOLVED within the boot unit. Exact whole-unit allowlist and W01-W03 necessity controls remain; `test_builder.py:5237`, `:5259`, `:12213`, `:16218`. Linked-object effects remain an authorized unproved boundary. |
| R317-2 S1 | SUGGESTION; Robustness, Docs | ADDRESSED by the unit-wide rule and explicit out-of-unit boundary. |
| R316-2 F2; R317-2 F1 | MINOR; union Conformance, Robustness, Tests, Docs | RESOLVED. Compiler-free protection is explicitly an open class of NOT RUN spellings in prose, table and COST, with representative fixtures retained. |
| R316-1 F4 | SUGGESTION; Robustness | RETAINED optional; disclosed and pinned C16/C17 behavior, detailed below. |
| R316-2 S1; R317-2 S2; R317-1 S1/R317-2 S3 | SUGGESTION; lenses detailed below | RETAINED without changing severity. |
| R272/R273 original macros | Inherited issue acceptance cases | RESOLVED in both modes; this round reran both spellings and effective disconnections. |
| R273-S3, verifier `#else` deletion | Explicit frozen-scope exclusion | RETAINED unchanged, not represented as fixed. Source reviews measured acceptance in both modes; relevant verifier code and disclosure remain. |

No finding was moved to another issue to claim clean coverage. Rounds R316-3/R317-3 and R316-4/R317-4 were publicly voided and supply no coverage.

The following are retained source suggestions, not new composition defects:

- **R316-1 F4 - SUGGESTION - Robustness.** Artifact: `test_builder.py:12301`, `BAREMETAL_FIRMWARE.md:503`. Authority/evidence: later scope decisions permit explicit NOT RUN disclosure for C16/C17. Impact: parenthesized/indirect writes remain accepted without compilation. Required outcome, optional: separately scoped broader fallback protection if desired. Verification: preserve the disclosed mode split and compiled refusal.
- **R316-2 S1 / R316-5 S1 - SUGGESTION - Conformance, Docs.** Artifact: `test_builder.py:5211`. Authority/evidence: decision 5824093785 says complete call arguments; unchanged exclusions admit alternate keyword-operator spellings recorded as N04/N06. Impact: additional harmless unevaluated cast-rvalue forms are accepted. Required outcome, optional: align exclusions or describe the lexical boundary. Verification: rerun the published N04/N06 controls while preserving authorized forms.
- **R317-2 S2 / R316-5 S2 - SUGGESTION - Conformance, Robustness, Tests, Docs.** Artifact: `test_builder.py:5184`, `:5204`. Authority/evidence: parent tracking handles parentheses and can admit an initializer element as a call-argument shape; source reviews record the four-case compound-literal set. Impact: an additional harmless cast-rvalue context is accepted, without an established sample write. Required outcome, optional: distinguish brace/bracket parents or document the lexical reading. Verification: preserve the legitimate call and rerun the unchanged four-case set.
- **R317-1 S1 / R317-2 S3 / R316-5 S3 - SUGGESTION - Tests.** Artifact: `test_builder.py:12164`. Authority/evidence: memory/string destination fixtures pass the sample value as an address, rather than its object's address. Impact: labels imply a sample write although the absence rule correctly refuses an occurrence. Required outcome, optional: label these as occurrence/cost controls. Verification: retain their named refusals and genuine address-taking cases.

**Reviewer-owned completion ledger**

Each row records whether composition touches that lens. Unchanged source behavior is covered by the named source rounds at their actual source head, not falsely banked at the composition head.

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN; composition touches shared boot-contract inputs | Issue decisions; `test_builder.py:4485`, `:5280`, `:11343`; firmware `:1438`; both focused receipts verify acceptance and predecessor retention | R316-6 | 7ddbbdc9be73728b239718c8976261c7e0ad0563 |
| RTL | CLEAN; no #544 hardware delta; composition touches structural test scope | `milan_csr.sv:717`, `:1942`; `milan_datapath.sv:3111`, `:3143`, `:6031`; eight structural refusals per mode; source-list and exact gitlink audit. Unchanged source hardware/interface scope is covered by the source reviews | R316-6 composition; R316-5 and R317-5 unchanged source scope | 7ddbbdc9be73728b239718c8976261c7e0ad0563; source: 8383e929fab3ff57a768c88b8b1ff9b568afcf14 |
| Robustness | CLEAN; composition touches combined refusal paths | `assert_boot_contract`; original macro disconnections; PHC/media extra-reader and gated-port controls; NVM capacity/negative-control receipts | R316-6 | 7ddbbdc9be73728b239718c8976261c7e0ad0563 |
| Tests | CLEAN; shared test function and inventories touched | `sw/builder/test_builder.py`; `scripts/focused_boot.py`; 30 focused case outcomes; unchanged source helper ASTs; `ci_events` check/selftest; suite tally and record-space selftest | R316-6 | 7ddbbdc9be73728b239718c8976261c7e0ad0563 |
| Docs | CLEAN; shared guide, table and cross-page references touched | `BAREMETAL_FIRMWARE.md:429`, `:1454`, `:1797`, `:1844`; both documentation inventories; TOC/anchors, paths, em-dash, feature status, generated matrix; public source evidence | R316-6 | 7ddbbdc9be73728b239718c8976261c7e0ad0563 |

**Real limits and pending manager duties**

- This review ran focused tests and static composition gates only. It did not run full parent, processor, gPTP, Yosys or builder banks; hardware, Docker, local workflow replicas and hosted acceptance were not exercised. No hosted job, executed or skipped, is counted as evidence here. Calibration NOT RUN and field skips are not hardware proof.
- The compiler-backed claim stops at the measured boot unit and its census-header boundary. Separately linked library, BIOS and startup objects remain unread. Compiler-free protection remains intentionally weaker; NOT RUN is not a pass.
- The manager must refresh current dev, construct the final candidate at the merge turn, and validate that exact result. The assigned live-dev reference `0755923d983218ca6ca9db6891a558cbe6425b8d` is distinct from this train's first-parent chain; this review does not assert an unmeasured future tree is identical.
- The manager owns publication, full bank evidence, hosted/local-replica acceptance, review counting and remaining rounds, explicit merge authorization, post-merge containment, and issue/project completion. This includes assessing the procedural caveat publicly recorded in R316-5. No GitHub write, source fix, commit, push, merge, author contact or delegated review occurred here.
- Final byte/mode/index audit matched all 889 parent blobs and the three required submodule populations: protocol processor `09f9bf3846511f8388d995126502ed92eaa65213`, gPTP processor `e5dcea6e351abff18a27a00f8e345f3251bdbd8f`, and verilog-axis `48ff7a7e2ef782cf778d47910cf85835c64b1bce`. Optional `external` remains uninitialized. No source restoration was necessary; all probe modifications were in memory, and disposable files stayed under packet `scratch/`.

Only REPORT.md and files listed in MANIFEST.sha256 are publishable. Scratch is excluded.

R316-6 FINISHED
