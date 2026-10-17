[R643] NEGATIVE - exact head 6aaec5dfc45e84c8842f3f31f76910bfa91a96e1

Round R643-1, issue #177 / PR #182. Tree `5f7ae4960def91d88b3c4c053a94c021c1d3e955`; source base `22c139a4323bc96c779d13e3f6774480c5fb9b75`. All five lenses were applied independently. One open MINOR concerns an incorrect protocol-field claim in the architecture documentation. No runtime defect was found. A separate source-comment RESIDUE does not affect lens cleanliness or the verdict.

The independent verdict and ledger were recorded in `independent-pass.txt` before public prior-findings reconciliation. No other reviewer's report was read. The issue comments, PR comments, submitted reviews and inline review comments contained no prior public FINDINGS to resolve or retain at the final scan (`prior-findings-scan.json`).

**R643-1-F1 — MINOR — Conformance, Docs.** Artifact: `docs/architecture/06_aecp_engine.md:897`.

The new length-guard explanation says a command under cdl 16 “has no whole descriptor_type”. At cdl 14 and 15, the two-byte descriptor_type is complete; the descriptor_index is missing or partial. The four-byte target, comprising both fields, is what requires cdl 16. Evidence: the engine captures descriptor_type at payload offsets 0 and 1 (`hdl/aecp/KL_aecp_engine.sv:3631`), while `tb/pp_top/sim_main.cpp:5692` supplies those two bytes and correctly expects BAD_ARGUMENTS. This is the IEEE 7.4.40.1 command shape cited by the section and frozen acceptance. The `gavb-floor-14` mutant is killed by the truncated-index case (`dispatch/gavb-floor-14.log`).

Impact: the normative architecture gives the wrong protocol-field rationale for the boundary. A reader could infer that descriptor_type itself needs four payload bytes. Runtime behavior and the cdl 16 threshold are correct. This is MINOR rather than RESIDUE because correcting it changes a factual protocol/conformance claim, not merely its phrasing.

Required outcome: replace the parenthesis with exactly “a command under cdl 16 lacks the complete descriptor_type/descriptor_index pair and answers `BAD_ARGUMENTS`”. Verification: check the two 16-bit fields against IEEE 7.4.40.1 and the parser; retain the cdl 16 floor and short-command check. No RTL change is required.

**R643-1-R1 — RESIDUE — RTL, Tests, Docs.** Artifacts: newly added or rewritten comment text in `hdl/aecp/KL_aecp_engine.sv:1288`; `tb/pp_top/aecp_dispatch_mutants.py:44`; `tb/pp_top/sim_main.cpp:5591`, `:5634`, `:5636`, `:5705`, `:11146`.

The reviewed delta adds bench labels such as M9, V1b, V5 and section V to source comments. The owner's 2026-10-15 rule excludes these labels and requires behavior/reason with issue and requirement references. This finding covers new comment text only. Existing review-history wording, including “two review rounds”, is not newly attributed to this PR; existing residue belongs to #746.

Impact: source-comment policy violation only. Diagnostic strings, check names, code, measurements and verdicts need no change. The owner's explicit source-comment classification makes this RESIDUE; it leaves no lens unclean.

Required exact wording changes:

| Comment location | Replacement wording |
| --- | --- |
| engine:1288, within the updated refusal-site explanation | Replace “tb/pp_top's M9 table” with “the non-AEM command sweep”; append “(issue #177, REQ-AEM-023)” to the explanation. |
| dispatch driver:44, three-line comment | “Issue #177, REQ-AEM-023 and REQ-NET-001: use a real AVB_INTERFACE target to expose a missing message-type guard; other descriptor types must return the command-sized NOT_IMPLEMENTED echo.” |
| sim_main.cpp:5591, three-line comment | “Issue #177, REQ-AEM-023 and REQ-NET-001: exercise GET_AVB_INFO dispatch with constant gather data, independently of earlier test state; include the existing GET_AS_PATH boundary checks.” |
| sim_main.cpp:5634, three-line comment | “Issue #177, REQ-NET-001: IEEE 7.4.40.1 defines the type and index; padding to cdl 20 preserves the normal SUCCESS response.” |
| sim_main.cpp:5705 | “Issue #177, REQ-AEM-023: GET_AVB_INFO on any other descriptor type returns NOT_IMPLEMENTED.” Keep the following behavioral explanation. |
| sim_main.cpp:11145, five-line comment | “Issue #177, REQ-AEM-023 and REQ-NET-001: the focused dispatch run exercises command reflection, non-AEM message guards and GET_AVB_INFO on a freshly booted model. The default run exercises the same checks in its main timeline, so no check is counted twice.” |

Add `REQ-AEM-023` beside issue #177 in the new engine-arm comment at `hdl/aecp/KL_aecp_engine.sv:3387` and guard-stimulus comment at `tb/pp_top/sim_main.cpp:3406`. Verification: inspect added source-comment lines for prohibited labels and missing trace references; preserve compiled code and diagnostic strings. Findings pages, README inventories and PR text may retain labels.

**Authority and scope reconstruction.** The supplied AGENTS instruction and referenced command policy were read first. This checkout has no repository AGENTS.md or CONTRIBUTING.md. `docs/README.md`, root README, `hdl/README.md`, the [frozen issue and assignment](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/177), then linked requirement/interface authorities preceded the independent diff pass. The latter covered the compliance matrix and decision item 12, REQ-AEM-023 and REQ-NET-001, architecture 02 §4.3 and 06 §§6.10/8.2, the command table and verification contract. The one-commit diff/history preceded the [published author evidence](https://github.com/kebag-logic/milan-fpga/tree/9d301680a42cd2d736a5d16085cc84a2480a7128/review-evidence/pp177-r1), PR text and manager comments. The [public review start](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/pull/182#issuecomment-6241839068) fixes this head and the independence boundary.

The owner chooses NOT_IMPLEMENTED for the invalid type; the standard is not claimed to mandate that status. Compliance item 12 records IEEE 7.4.40.1, 7.4.40.3, Table 7-141, 9.3.5.3.3 and Milan v1.2 5.4.2.23. Response sizing follows the existing command-reflection contract: cdl is 12 plus the original command payload, excluding Ethernet minimum-frame padding. Wrong-type cases at cdl 16 and 20 compare complete Ethernet frames.

**Independent lens examinations.** Conformance found status choice and sizing consistent with frozen acceptance, but retains F1. RTL traced `UPC_NOTIMPL_C` plus `echo_r=1`, `A_RUN` retaining `pld_cmd_r`, the RX-slot payload source and zero-length response-buffer seal. `E_NOTIMPL` performs no gathers; retaining `gavb_r` does not consume the gather face. The full-width comparison, length-before-type order, and unchanged `UPC_GAVB_C`/descriptor-locate path preserve SUCCESS and missing-index NO_SUCH_DESCRIPTOR. Runtime edits are confined to the GET_AVB_INFO arm; the other RTL hunk is a comment. Command-model/test updates are appropriate consumers. Ports, parameters and register maps do not change. Base/head generated ROMs are byte-identical.

Robustness independently examined short commands, padded valid and wrong-type commands, existing/absent wrong-type targets, neighboring types, high-byte aliases 0x0109/0x8009, 0xFFFF and non-AEM guards. The full-frame oracle covers status, echo, addresses, identities, sequence and length. Tests checked every new assertion's sensitivity: reverting status kills all 13 wrong-type rows; refusing padding kills the new padded-success check; dropping the message guard kills the altered non-AEM stimulus. Other mutants isolate echo sizing, full-width typing, success, missing-index behavior and the length floor. Docs checked the clause trace, generated table/record, bench descriptions and static gates, retaining F1 and R1.

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
| --- | --- | --- | --- | --- |
| Conformance | UNCLEAN | issue #177; compliance item 12; architecture 06 §§6.10/8.2; field parser; F1 | R643-1 | 6aaec5dfc45e84c8842f3f31f76910bfa91a96e1 |
| RTL | CLEAN | engine diff and echo/seal paths; E_NOTIMPL/E_GAVB; registry; ROM comparison; R1 residue | R643-1 | 6aaec5dfc45e84c8842f3f31f76910bfa91a96e1 |
| Robustness | CLEAN | type/length/existence boundaries; high-byte aliases; message guards; dispatch logs | R643-1 | 6aaec5dfc45e84c8842f3f31f76910bfa91a96e1 |
| Tests | CLEAN | full-frame checks; 9 dispatch mutants; decode controls; published gate inventory; R1 residue | R643-1 | 6aaec5dfc45e84c8842f3f31f76910bfa91a96e1 |
| Docs | UNCLEAN | conventions; compliance clauses; command model/record; bench README; static gates; F1 and R1 | R643-1 | 6aaec5dfc45e84c8842f3f31f76910bfa91a96e1 |

**Executed reviewer evidence.** Pinned simulator identity 5.050 was verified before use. Independent campaigns ran concurrently under a foreground coordinator: three dispatch jobs, two decode jobs, two compiler workers per build and inherited `make -j16`. All temporary source copies/builds were under packet `scratch/`. No full bank was run.

| Execution | Result | Receipt |
| --- | --- | --- |
| Dispatch positive control | 947 checks, 0 failures: 716 dispatch and 231 existing response checks | `dispatch/control-aecp-dispatch.log` |
| Nine issue-specific dispatch mutants | All KILLED by named checks; failure counts 14, 13, 13, 13, 2, 16, 1, 2, 1 in declared order | `dispatch/results.json`, individual logs |
| Decode golden/restored controls | Each 585,760 trials, 0 timeouts; 176 checks, 0 failures | `decode/golden-*.log`, `decode/restored-*.log` |
| Decode wrong-status mutant | Build/sweep complete; named GET_AVB_INFO failure; campaign rc 0 | `decode/results.json`, individual logs |
| Focused documentation gates | rc 0: command model/selftest, links, matrices, requirement tags, parameters, IDs, figures, staleness | `docs-recheck.log`, `docs-recheck.rc` |
| ROM comparison | Identical 2048 words; SHA-256 `518b900c4a5650902c3ea9125941e434857ba2f379b6c92268a67fef459d37f8` | `rom-comparison.json` |
| Restoration audit | All 627 tracked blobs, modes and index entries match; clean status; no processor submodule gitlinks | `checkout-audit.json` |

The initial documentation invocation used an exported tree without a Git index and failed inventory discovery (`docs.log`/`docs.rc`). Re-running the same targets in the indexed checkout passed. The initial coordinator's aggregate exit was nonzero solely for this setup error, not a source failure. `run-focused.py` now uses the indexed source for those read-only gates and supports a fresh `--output` directory. `audit-checkout.py` reproduces the byte/mode/index check. Disposable probes never modified this checkout.

**Public evidence and limits.** All four published evidence files match their published manifest hashes (`evidence-hash-verification.json`). The author reports full processor gates at base/head, respectively 1,029,951 and 1,029,964 suite checks, and all 17 scratch-parent consumer gates. This is author-reported source-head evidence: the public packet contains the handoff, hash inventory and parent classification patch, not the indexed raw gate logs themselves. Broad runs were not independently reproduced here. The parent run used `7d79ffb26308ac51eaeeab6ec43d798d057ae0cd`, with the disclosed uncommitted reader-classification patch at both ends. It is not validation of current dev `e9cbb676d7fdd6539aa408e5dfe38870a4ae1a5f` merged with this change. Public parent gitlink snapshots are retained; no parent checkout/gitlink was modified.

At the final exact-head hosted snapshot, both runs had successful documentation and portability jobs; suites remained in progress. The cached simulator-build steps were skipped; documentation and portability execution steps completed. Pending suite/mutation steps are not counted as executed or passed. See `check-runs-final.json` and `hosted-jobs-*.json`. Hosted/act acceptance remains with the manager.

The copyrighted standards were unavailable in this repository and were not independently retrieved; interpretation was checked against the frozen public owner decision and repository authorities. No hardware access, physical calibration, full parent/processor/timing/synthesis/builder bank, source fix, commit, push, GitHub write, author contact or delegation occurred. Physical calibration NOT RUN and field skips provide no hardware proof. No manager source bank at this head is claimed or inferred.

Pending manager duties: resolve F1 and obtain the required review disposition for any changed head; carry R1 to the residue checklist; validate the final current-dev merge candidate with required builder/native banks and publish receipts; complete hosted/act acceptance and verify adopted submodule pins and classifications. The older scratch-parent pass does not replace these duties.

Only REPORT.md and files enumerated in MANIFEST.sha256 are publishable. Everything under scratch/ is disposable and excluded.

R643-1 FINISHED
