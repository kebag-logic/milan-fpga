[R487] POSITIVE - exact head 3048222541ea6be725417ba0cd957607f0b821cb

R487-3, external independent source review of issue #661 / PR #663. Tree: `a640b146eb68632f2d9ca153639ba2683b172b0a`. All five lenses are CLEAN for the assigned scope. No BLOCKER, MAJOR or MINOR remains open. R487-2 F1 and R1 are resolved. Two previously recorded RESIDUE items and three SUGGESTION items remain unchanged.

The review reconstructed the operating contract, documentation map, frozen issue scope and public decisions, requirement/interface authorities, source-base diff and history, then public executable evidence. The independent verdict and ledger were recorded in `receipts/independent-pass.md` before reading prior findings or another reviewer's report. Only public material and this isolated checkout were used.

This is a delta review with the assigned R487-2 verdicts retained for unchanged artifacts. The sole parent is `3880c1eb6e2f927a07f98150d5b05a228f8f4efd`. Exactly two regular files change, each by one replaced line: `docs/reference/FR_NFR.md` and `docs/findings/README.md`. Every other tree entry, including RTL, firmware, tests, configurations, generated records and gitlinks, is identical. See `receipts/docs-delta.diff` and `receipts/provenance.json`.

The changed requirement was checked directly against IEEE Std 1722.1-2021 Section 6.2.2.15, PDF page 54. `receipts/standard-authority.json` identifies the local standard by SHA-256; its text is not redistributed. FR-DISC-01 at `docs/reference/FR_NFR.md:173` now requires the clause's increment following each ENTITY_AVAILABLE and zero reset on ENTITY_DEPARTING or a power cycle. The existing advertisement and valid_time obligations remain. Replacing the inaccurate state-change formulation conforms the requirement to the standard; it grants no exception or relaxation. The [public manager decision](https://github.com/kebag-logic/milan-fpga/pull/663#issuecomment-5994059536) explicitly records that correction, satisfying the public-decision requirement.

The requirement agrees with `docs/reference/REGISTER_MAP.md:1032`, the saved-state statement at `docs/design/SAVED_STATE_MATERIALIZATION.md:1036`, and the pinned processor's reset/increment branches at `protocol-processor/hdl/adp/KL_adp_engine.sv:702`. The outgoing frame captures the current index at line 905; the completion branches increment after AVAILABLE and reset after DEPARTING. No implementation or test was changed to obtain this agreement.

The #649 row at `docs/findings/README.md:26` contains R487-2 R1's exact requested sentence. It distinguishes the original measurement's accepted 235-name shape from #652's later generation-time refusal. That agrees with `docs/findings/649_RESOURCE_MAP_AND_SENSITIVITY.md:26` and `:604`, without changing a measurement, figure, result or conformance claim. `receipts/public-evidence-audit.json` records the exact-text check.

Executed focused checks, all exit 0:

| Check | Result and receipt |
|---|---|
| `scripts/docs_check.py`, plus `--selftest` | Zero findings across 189 Markdown / 987 text files; 23 scrub and 4 routing controls pass. `receipts/docs-check.log`, `receipts/docs-scrub-controls.log` |
| `scripts/check_doc_style.py`, plus `--selftest` | 22 current documents and controls pass. `receipts/doc-style.log`, `receipts/doc-style-controls.log` |
| `scripts/gen_toc.py --check` | 131 annotated pages, 17 below threshold; no drift. `receipts/contents.log` |
| `scripts/check_em_dash.py --base 506d91db` and `--base fa450d30` | Zero findings; 339/339 controls in each run. `receipts/em-dash-source.log`, `receipts/em-dash-dev.log` |
| `scripts/check_doc_paths.py` | 912 cited paths resolve, 1 allowlisted; 10 line anchors valid. `receipts/doc-paths.log` |
| `scripts/check_wire_accountability.py --self-test` | 77 checks, zero findings; both acceptance controls and planted missing-master/fill refusals pass. `receipts/wire-accountability.log` |
| `scripts/check_feature_status.py --self-test` | Zero findings; 46/46 controls. `receipts/feature-status.log` |
| `git diff --check 506d91db..HEAD` | Clean. `receipts/diff-whitespace.log` |
| `python3 tb/tools/avtp_wire_truth.py --self-test` | 25 tests pass, including the four departure/reset/repeat cases. `receipts/wire-truth.log` |

The eleven-command documentation/check bank ran concurrently with six foreground child slots and completed before its coordinator returned. Every command has a separate log and return-code file; exact arguments and durations are in `receipts/focused-results.json`. No compilation, long bank or new mutation campaign was needed for this two-line delta.

The evidence boundary matters: `scripts/check_wire_accountability.py:96` cites FR_NFR.md in explanatory text; it does not open or parse that file and does not test ADP index semantics. Its successful run establishes its advertised-width checks and controls. The requirement's semantics were checked against the standard, interface statements and unchanged ADP implementation. The separate wire-truth test exercises a full availability cycle, departure with index zero, a repeated AVAILABLE after reset, and a nonzero repeat after departure. It is not a complete ADP state-machine or hardware proof.

Prior public findings were reconciled after the independent pass:

| Prior item and lenses | Disposition at this head | Evidence |
|---|---|---|
| R487-2 F1, MINOR, Conformance/Docs | RESOLVED | Public decision 5994059536; FR-DISC-01:173 checked directly against Section 6.2.2.15; related implementation and documentation agree |
| R487-2 R1, RESIDUE, Docs | RESOLVED | Exact requested sentence in findings/README.md:26; linked historical finding agrees |
| R487-1 F1, MINOR, Conformance/Tests/Docs | REMAINS RESOLVED | Five earlier corrected statements and production checker unchanged from R487-2; 25-test wire self-test passes here |
| R487-1 F2 and R486-1 F1, MINOR, Docs | REMAIN RESOLVED | Current body passes the repository privacy scrub and uses portable placeholders; corrected public historical copy also passes its privacy scrub |
| R486-1 F2, MINOR, Docs | REMAINS RESOLVED | Current body says 212; fresh repository-parser census returns 212 at both pins; manager comment 5991634080 supersedes the historical count |
| R486-1 R1, RESIDUE, Docs | REMAINS RESOLVED | Current body retains published-branch fetch and detached-checkout instructions |
| R486-1 R2/R3, RESIDUE, Docs | RETAINED | Unchanged artifacts and exact fixes below |
| R486-1 S1; R487-1 S1/S2, SUGGESTION | RETAINED | Optional outcomes below; no severity downgrade or new blocking defect |

Current-body evidence is `receipts/pr-body.md` and `receipts/public-evidence-audit.json`. The frozen `0010a410` archive predates the privacy correction; it is not presented as corrected. The later public copy at `8c01f837` has placeholders, including `<account>` in its historical selector recipe. The current body supersedes that recipe with a description of the required revision. See `receipts/corrected-published-body-audit.json`.

Retained findings, with their existing classifications:

- **R486-1 R2 | RESIDUE | Docs | `docs/reference/SUBMODULES.md:148`.** Authority/evidence: the D3 header at `SAVED_STATE_MATERIALIZATION.md:15` explicitly says name pending is not yet transferred, while this summary uses present tense. Impact: ambiguous summary wording only. Exact required fix: “Not yet adopted: a later parent lane (D3 section 18.3, lane 3) moves name pending to `d3_unflushed_o`; until then the sticky term stays.” Verification: compare the revised summary with the D3 header. No behavior or conformance claim changes.
- **R486-1 R3 | RESIDUE | Docs | `docs/reference/PP_DESCRIPTOR_OWNERSHIP.md:333`.** Authority/evidence: F5's explanation omits the explicit lint waiver already declared in `configs/endstation_ax7101_8x8.yaml:275`. Impact: incomplete explanation of packing permission; the recorded conformance debt remains. Exact required addition: “The 8x8 configuration's `model_lint_waivers` entry (L1 `port-cluster-minimum`, STREAM_PORT_INPUT 0 to 7, #584) lets the default lint pack it; the packer refuses the waiver once any of those ports passes. The waiver is not a conformance claim.” Verification: compare with the configuration and default lint, preserving the existing conformance position.
- **R486-1 S1 | SUGGESTION | Docs, RTL | `docs/findings/234_PP_SHADOW_AREA_BASELINE.md:38`.** Authority/evidence: the table shows standalone 8x8 WNS moving from -1.947 to -4.095 ns; the page already distinguishes this estimate from routed timing. Impact: a reader may overlook that limitation. Optional outcome: identify the fall and the owner of an integrated 8x8 route. Verification: retain the exact figures and distinguish standalone estimates from routed evidence.
- **R487-1 S1 | SUGGESTION | Tests | `tb/verilator/nvm_cosim/Makefile:50`.** Authority/evidence: the parent co-simulation's producer set does not include `KL_aecp_nvm_writer`; the D3 page leaves parent name adoption open. Impact: name write/restore/rollback integration has static compatibility evidence only. Optional outcome: exercise the real writer and backend in the assigned name-persistence lane. Verification: write, clear state, restore and roll back with fault-sensitive checks.
- **R487-1 S2 | SUGGESTION | Robustness, Tests | `protocol-processor/hdl/aecp/desc/model_rules.py:115`; `protocol-processor/hdl/aecp/ucode/gen_ucode.py`.** Authority/evidence: the lint's 144/8 literals agree with the consumer today; the retired parent checker derived them from that consumer. Impact: future independent edits could drift. Optional outcome: add a processor-side consistency tie. Verification: changing either consumer bound must fail the consistency check. Tests is also attributable, as recorded in the subsequent internal review; no present mismatch is claimed.

Reviewer-owned ledger. Each lens was applied to the final delta and its affected artifacts; unaffected R487-2 coverage stands under the assignment. CLEAN here does not mean that unrelated product debt or physical release obligations have been discharged.

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Issue #661 acceptance/decisions; FR_NFR.md:173; IEEE 1722.1-2021 6.2.2.15; REGISTER_MAP.md:1032; processor ADP reset/completion branches | R487-3, unaffected R487-2 retained | 3048222541ea6be725417ba0cd957607f0b821cb |
| RTL | CLEAN | receipts/docs-delta.diff and provenance.json; KL_adp_engine.sv:702,905,953; unchanged runtime/interface trees and required gitlinks | R487-3, unaffected R487-2 retained | 3048222541ea6be725417ba0cd957607f0b821cb |
| Robustness | CLEAN | avtp_wire_truth_selftest.py:347 reset/repeat boundary cases; ADP reset branches; receipts/wire-truth.log; unchanged prior failure controls | R487-3, unaffected R487-2 retained | 3048222541ea6be725417ba0cd957607f0b821cb |
| Tests | CLEAN | check_wire_accountability.py:458 controls; actual cited-document use at :96; focused-results.json; wire-truth.log; unchanged test tree | R487-3, unaffected R487-2 retained | 3048222541ea6be725417ba0cd957607f0b821cb |
| Docs | CLEAN | Both changed rows; linked #649 finding:26,604; public decision and current PR body; documentation gate receipts; prior dispositions | R487-3, unaffected R487-2 retained | 3048222541ea6be725417ba0cd957607f0b821cb |

Public evidence and real limits:

- All 20 files in the specified [frozen public packet](https://github.com/kebag-logic/milan-fpga/tree/0010a410b0150c2c7043142fb64036a7d2655799/review-evidence/661-r1) match its published manifest. All 30 recorded source blobs match the recorded round-1 commit. This is round-1 evidence, not new execution at this head. The [round-2 public statement](https://github.com/kebag-logic/milan-fpga/issues/661#issuecomment-5993741847) and current body identify later results at `3880c1eb`. The assignment reports the manager's full source banks passed at the present head; those banks were not independently rerun here. This report's new executed evidence is the focused set above.
- No full parent, processor, gPTP, synthesis or builder bank, route, vendor run, local workflow replica or container operation was performed. Prior resource/capture verdicts stand: the route's +0.108/+0.036 ns and the capture's 13.86484 ms are retained measurements, not new measurements at this head. No raw implementation checkpoint was inspected. #657 remains the authorized unchanged 28 PASS / 4 FAIL exception; it is not a clean campaign. #656's exception remains retired.
- The exact-head hosted snapshot in `receipts/hosted-snapshot.json` has `rtl-fast` successful, four synthesis shards successful, and several long jobs still running. `docs-check` and `elaborate` were in progress. Job-step records confirm execution and success of wire-accountability and docs-check-no-git. The physical gPTP job is skipped with no executed steps. Pending or skipped contexts are not counted as executed passing evidence. Hosted and local-replica acceptance remain manager duties.
- Physical calibration: **NOT RUN**. No hardware, flash or soak. Field-generator skips, historical-calibration absence, simulation and timing reports are not hardware proof. The four field/freshness skips and two builder NOT RUN arms remain excluded from coverage.
- Source base is `506d91dbeeba585d72d2e80d92fca799c719f8ee`; the live dev read remained `fa450d301805881ad713b67521477bf042ddadfd`. This is source approval, not final current-dev candidate validation.
- Before/after integrity receipts match. They prove 1,011 parent blobs, 558 processor blobs, 104 gPTP blobs and 214 axis blobs byte-for-byte, with executable modes and exact index entries. Required gitlinks are `ead8036035affd53ef4b29979190f2f4f67084c0`, `5dce647ab5a01a6ecff9a982b22e3a4a1d946d3d`, and `48ff7a7e2ef782cf778d47910cf85835c64b1bce`. The unused historical external gitlink remains unchanged and uninitialized. No source fixes, commits, pushes, merges, GitHub writes, author contact or other-checkout edits occurred.

Pending manager duties: publish this packet; obtain the required independent positives and leave no review in flight; carry R486-1 R2/R3 to the residue checklist and retain the three optional suggestions. Accept the exact-head hosted/local-replica evidence with its real execution limits. At the merge turn, construct and validate the final candidate against then-current dev and update the PR's status/replay head and evidence accordingly. Merge only with explicit maintainer authorization. Perform post-merge containment and the assigned flash/soak work before completing issue/project closure.

Portable replay commands and dependency setup are in `REPLAY.md`. `MANIFEST.sha256` enumerates the report, scripts and publishable receipts by relative path. Raw standard extraction, downloaded API originals, dependency environment and temporary bytecode are confined to `scratch/`, excluded from publication.

R487-3 FINISHED
