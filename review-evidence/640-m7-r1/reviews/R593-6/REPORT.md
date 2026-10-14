[R593] POSITIVE - exact head 7fb3664b9b53d0c4caa4b64415dd9cc3e850e4b0

R593-6, external independent delta review of issue #640 / PR #713. Tree `540ed6c59e0004185e682f28be9bb5b42e584f09`; donor `e4869fd0c42889b2ac806587cc5c78afb1c33461`. No open BLOCKER, MAJOR or MINOR remains in this assigned delta. Wording residues and optional suggestions remain explicitly retained below. This source-review verdict is not merge authorization or closure of issue #640.

The [round-six scope decision](https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-6164557611) permits the count correction, optional stale-denominator example and PR publication wording only. The frozen [M7 assignment](https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-6097272538), issue acceptance, `REQUIREMENTS.md:144,305`, `MARK_II_AREA_PLAN.md:563`, `GPTP_PLANE.md:39` and submodule interface map remain authoritative. The issue's eventual 38,040-LUT target is not this intermediate lane's claimed result.

The source-base comparison `e8454e2751d05b02ee8e5a571857589ab358ab86..7fb3664b9b53d0c4caa4b64415dd9cc3e850e4b0` and first-parent history were reconstructed, including the earlier merge of dev `fa8209889411e8ca95757174c981f720dbcd95a2`. The judged delta is `4c5d70b50230fbd5da347852d39daf7f23b3df0b..7fb3664b9b53d0c4caa4b64415dd9cc3e850e4b0`: exactly one commit and one documentation file, three additions and three deletions. No RTL, interface, requirement, workflow, test, generated file or gitlink changes. Earlier rounds stand for all untouched artifacts. `receipts/independent-verdict.md` records the independent verdict and ledger before any prior reviewer report or finding was read.

The corrected sentence at `docs/testing/CI_WORKFLOWS.md:1322` says the worker matrix size is six for Verilator and four for Yosys. Those values agree with `.github/workflows/rtl.yml:161,162,426,463,464,602` and `scripts/ci_events.py:2237,2299`. The requested literal grep is preserved in `receipts/document-expect-grep.txt`; no stale `--expect 5` remains. At lines 1337-1338, seven workers, stale total six and omitted shard 6/7 correctly describe `_m_shard_denominator_stale` at `scripts/ci_events.py:5256`.

The current PR body contains both exact R593-4-D1 replacement sentences and qualifies the executor's no-push/no-edit history. Its status still calls the now-published round-six head local/unpushed. The implementation wording request is applied; the remaining publication refresh is retained under the original residue ID, with an exact fix below.

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Scope decision 6164557611; `CI_WORKFLOWS.md:1322`; `rtl.yml:161,426,463,602`; `count-probe.log`; one-file scope proof. Both documented expectations match the executable contract. | R593-6 delta; unchanged substantive scope retains R593-5 | `7fb3664b9b53d0c4caa4b64415dd9cc3e850e4b0` |
| RTL | CLEAN | `delta.patch`, `delta-stat.txt`, `source-range-map.txt`, `identity.log`. No RTL, clock/reset, CDC, index, latency, interface or donor change exists in this delta. | R593-6 delta; merged implementation retains R593-4, carried through R593-5 | `7fb3664b9b53d0c4caa4b64415dd9cc3e850e4b0` |
| Robustness | CLEAN | `CI_WORKFLOWS.md:1337`; `ci_events.py:3249,3341,5256`; `count-probe.log`. The seven/six fixture and stale aggregate expectation are independently rejected by named checks. | R593-6 delta; unchanged M7 robustness retains earlier coverage | `7fb3664b9b53d0c4caa4b64415dd9cc3e850e4b0` |
| Tests | CLEAN | `focused-checks.json`, three raw gate logs/rc files, `count-probe.log`; unchanged workflow and test bytes. Baseline passes; both targeted negative controls fail for their claimed defects. | R593-6 delta; unchanged scheduling and table campaigns retain R593-5 | `7fb3664b9b53d0c4caa4b64415dd9cc3e850e4b0` |
| Docs | CLEAN | `CI_WORKFLOWS.md:1322,1337`; literal grep; current PR body; published round-six handoff; hosted docs job/step records. R592-5-F1 is corrected. Wording residues remain non-blocking under the owner rule. | R593-6 | `7fb3664b9b53d0c4caa4b64415dd9cc3e850e4b0` |

The inherited R593-5 head is `4c5d70b50230fbd5da347852d39daf7f23b3df0b`; R593-4's merged-implementation head is `412e3f6c8c402bce63e94c291d2782b5579aaa1d`. This ledger advances only the independently examined delta to the current head. It does not claim fresh full-bank or hardware coverage.

| Local command/probe | Result | Receipt |
|---|---|---|
| `python3 scripts/docs_check.py` | rc 0; zero findings, 207 Markdown files, 1299 scrubbed text files; 23/23 scrub and 4/4 routing controls | `receipts/docs-check.log`, `.rc` |
| `python3 scripts/ci_events.py --check` | rc 0; 2175 contract items across four workflows and the policy document | `receipts/ci-events-check.log`, `.rc` |
| `python3 scripts/check_doc_style.py` | rc 0; 22 current documents | `receipts/doc-style.log`, `.rc` |
| `python3 scripts/count_probe.py <clone>` from this packet | rc 0; six/four matrix lengths, singleton totals and aggregate expectations agree; current prose agrees | `receipts/count-probe.log`, `.rc` |
| In-memory stale denominator | Existing fixture makes seven workers with total six; checker rejects the denominator by name | Same probe receipt |
| In-memory aggregate `--expect 6` changed to `--expect 5` | Checker rejects the stale expectation by name; no files changed | Same probe receipt |
| `git diff --check 4c5d70b5 HEAD` and raw identity audit | rc 0; exact bytes, modes, complete index and required gitlinks verified | `receipts/source-range-map.txt`, `identity.log`, `identity.rc` |

The three gates ran concurrently inside one foreground driver, which awaited every child. The targeted negative controls ran sequentially in memory. The prose-style gate's inventory excludes this CI policy page; its green result is not claimed as direct coverage of the edited sentences. Direct count/fixture inspection supplies that evidence. No full CI self-test, simulation build or bank was run this round.

The [published author evidence](https://github.com/kebag-logic/milan-fpga/tree/6252d8ee3320b92b493c94cae56741ca90f0a15e/review-evidence/640-m7-r1) was read after the independent diff pass. Its round-six handoff and [REVIEW READY](https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-6164684520) report the three requested gates and additional whitespace/em-dash checks passing. The handoff's complete published bytes match the archive manifest's `published_sha256`; that manifest explicitly distinguishes path-redacted publication bytes from original bytes. `receipts/author-evidence-identity.json` records the binding. The underlying author raw logs are not in that public directory: the handoff publishes their sizes/hashes and results. Those are author-reported receipts, supplemented here by independently executed focused gates. No manager source bank at this exact head exists or is inferred.

Hosted documentation evidence was read directly from [run 38538854496](https://github.com/kebag-logic/milan-fpga/actions/runs/38538854496), associated with this exact published head. Its checkout is synthetic merge `2d3f68ef648b90bf528dd90cd4b4f04a0fc0e75d`, with ordered parents dev `fa8209889411e8ca95757174c981f720dbcd95a2` and this head. The merge tree equals reviewed tree `540ed6c59e0004185e682f28be9bb5b42e584f09` (`receipts/hosted-merge.json`). This is exact-tree hosted evidence, not the manager's final merge candidate.

| Hosted docs context or step | Observed state | Evidence |
|---|---|---|
| `docs-check-no-git` | Executed successfully; zero findings, 22/22 scrub controls and 4/4 routing controls. Inventory parity explicitly skipped because Git metadata was removed. | Job 115768354765; raw selected checkout/result lines in `hosted-job-115768354765-excerpt.log` |
| `wire-accountability` | Executed successfully; 77 checks, zero findings | Job 115768355110; selected raw log in `hosted-job-115768355110-excerpt.log` |
| `docs-check`: link/wording/privacy step 9 | Executed successfully | Job 115768354809, `hosted-docs-jobs.json` |
| `docs-check`: added-line em-dash step 10 | Executed successfully | Same job/receipt |
| `docs-check`: concise documentation step 11 | Executed successfully | Same job/receipt |
| Overall `docs-check` | Still in progress at the recorded snapshot; end-station builder gates step 27 running; CI event/SHA step 43 pending | Same job/receipt; no overall docs success claimed |

The hosted RTL snapshot has a successful selector and four successful synthesis workers, six simulation workers still running, and physical gPTP explicitly skipped. It supplies no completed simulation aggregate or hardware proof. Hosted acceptance and any later results remain the manager's responsibility. Completed-job logs were successfully captured after enabling literal escape-sequence output; an initial download attempt was refused by the local client's output filter, not by a CI gate. Full downloaded logs remain unpublished under `scratch/`; the selected receipts preserve the actual output lines.

Prior public findings were read only after the independent verdict and ledger were written. Findings from all ten earlier public PR review comments were examined; there are no separate submitted review bodies or inline findings. [R592-5](https://github.com/kebag-logic/milan-fpga/pull/713#issuecomment-6164547737), [R593-5](https://github.com/kebag-logic/milan-fpga/pull/713#issuecomment-6164540846), and the earlier finding excerpts are retained as receipts. No other current-round review was used.

| Prior finding | Disposition at this head | Basis |
|---|---|---|
| R592-5-F1, MINOR, Docs | Resolved | Correct six/four sentence at line 1322, workflow comparison and focused negative probe |
| R592-5-S1, SUGGESTION, Docs | Resolved | Seven/six and shard 6/7 now match the existing fixture |
| R592-4-F1, BLOCKER, Tests/Conformance; R593-4-F1, MAJOR, Conformance/Tests | Remain resolved | R593-5/R592-5 scheduler, partition, preflight and hosted resolutions; all executable artifacts unchanged here |
| R593-4-F2, MINOR, Docs | Remains resolved | README still says TX 25 and results two; harness unchanged from the reviewed correction |
| R592-1-F1, MINOR, Tests | Remains resolved | Depth-two coverage and result-write-index control unchanged; earlier corrected-head execution stands |
| R593-2-F1, MINOR, Tests/Docs | Remains resolved | Eleven-column census, declared one-valued columns and generated table unchanged |
| R592-1-F2 = R593-1-R-02, RESIDUE, RTL/Docs | Remain resolved | Corrected stale-word and beat-depth comments unchanged |
| R592-1-F3 = R593-1-R-01, RESIDUE, Docs | Remain resolved | Individual exclusion reasons and untaken timestamp-FIFO option remain at plan lines 728-729 |
| R592-1-F5, RESIDUE, Docs | Remains resolved going forward | Later evidence distinguishes engine 33, gaskets four and generator three; original prose stays historical |
| R592-1-F4, SUGGESTION, Tests; R593-1-S-01, SUGGESTION, Tests; R593-2-S-01, SUGGESTION, Tests | Remain resolved | Decode test, declared ledger tag and actual-enable reporting unchanged |
| R593-2-R-01, RESIDUE, Docs; R592-2-RES1, RESIDUE, Docs | Remain resolved | Invalid detached-branch command absent; body no longer calls the PR a draft |
| R593-4-D1, RESIDUE, Docs | Exact wording applied; publication refresh retained | Current body still labels the new published head local/unpushed; precise fix below |
| R592-3-RES1; R592-3-RES2; R593-3-R-01 | Retained, RESIDUE | Unchanged wording; exact fixes below |
| R593-1-S-02; R593-1-S-03; R592-2-S1; R593-3-S-01; R592-4-S1 | Retained, SUGGESTION | Unchanged optional limits; details below |

Retained findings preserve their original IDs and all attributed lenses. They are not newly expanded scope.

- **R593-4-D1 | RESIDUE | Docs | PR #713 Status, reproduction and Round 6.** Authority/evidence: the requested replacement sentences are present, but the API head is published `7fb3664b` while Status names `4c5d70b5` and calls round six pending publication. Impact: publication wording only; no measurement, test, contract or review verdict changes. Exact fix: set the published parent to `7fb3664b9b53d0c4caa4b64415dd9cc3e850e4b0`; replace the pending-publication sentence with “Round 6 is published at the parent revision above and awaits review completion.” Delete “The Round 6 continuation remains local until publication.” Replace the Round 6 continuation line with “Published parent: `7fb3664b9b53d0c4caa4b64415dd9cc3e850e4b0`.” Replace its final status sentence with “The status names the published Round 6 parent.” Keep the exact checkout sentence and qualified executor history. Verification: compare the refreshed body with the API head and unchanged donor pin. Manager residue checklist; Docs remains clean.
- **R592-3-RES1 | RESIDUE | Tests, Docs | `tb/verilator/gptp_tables/README.md:10`, `gptp_tables_wrap.sv:15`.** Authority/evidence: result-reference strobe/`ok` at wrapper lines 410-414 read resolution logic using the converted ledger head; separate ledger lockstep at lines 424-428 grades it. Impact: overbroad independence wording only. Exact fix: after “from signals the change did not touch”, append “except that the result queue's write strobe and `ok` bit come from the plane's resolution logic, which reads the ledger's converted head port; the ledger lockstep grades that port in every cycle the ledger holds an entry, which includes every resolution”. Verification: compare both sentences with the unchanged wrapper; no oracle or verdict changes.
- **R592-3-RES2 | RESIDUE | Docs | `docs/design/MARK_II_AREA_PLAN.md:713`.** Evidence: the adjacent table correctly gives 74/73 bits narrowing to 69. Impact: ambiguous prose beside correct figures. Exact fix: “Their function, depths and read latency are unchanged; only the two frame FIFOs' stored byte-enable fields narrow, as the table shows.” Verification: agreement with the unchanged table; no measurement changes.
- **R593-3-R-01 | RESIDUE | Tests, Docs | `tb/verilator/gptp_tables/Makefile:63`.** Evidence: the executable mutation list and README contain four declaration controls. Impact: stale comment label only. Exact fix: replace “and two wrong declaration” with “and four wrong declaration”. Verification: compare with `declaration_missing`, `declaration_wrong_value`, `declaration_many_valued`, `declaration_stray`; executable controls remain unchanged.
- **R593-1-S-02 | SUGGESTION | Tests | `tb/verilator/gptp_tables/README.md:76`.** Evidence/impact: coverage remains cumulative; a silent post-reset segment can pass. Required disclosure is present. Optional outcome: after #714's underlying fix, require useful activity per reset segment; verify a silent segment fails by name. Filing #714 is not claimed to resolve the defect.
- **R593-1-S-03 | SUGGESTION | RTL, Robustness | `hdl/ieee8021as/gptp_plane/KL_gptp_shadow.sv:271`.** Evidence/impact: unchanged guard permits widths the classifier/gearbox cannot serve; this predates M7. Optional outcome under #495: refuse unsupported widths or make the paths generic. Verification: supported and unsupported elaboration cases.
- **R592-2-S1 | SUGGESTION | Tests | `hdl/ieee8021as/gptp_plane/KL_gptp_txret.sv:637`, suite README ledger row.** Evidence/impact: full-ledger guard unchanged; the suite reaches three of eight, leaving that boundary untested. Optional outcome: full-ledger stimulus and named guard mutation. Verification: reach the boundary and kill that mutation.
- **R593-3-S-01 | SUGGESTION | Docs | donor `docs/MANAGER.md:72`.** Evidence/impact: unchanged M7 figures lack a direct M7 evidence link. Optional outcome: link the published measurement at its original revision. Verification: open the link and compare the figures/revision.
- **R592-4-S1 | SUGGESTION | Docs | `syn/yosys/rom_digests.tsv:32`.** Evidence/impact: correct but inert donor `6b5a4282` row remains unchanged. Optional outcome: remove it or retain the historical row as the public ruling allows. Verification: generated ledger and current pinned digest stay correct.

Limits and pending manager duties:

- This round ran only the authorized focused checks and in-memory probes. No full parent/processor/synthesis/builder banks, source fixes, commits, pushes, GitHub writes, merges, author contact, sub-agents, containers, host orchestration, shared installs or hardware actions occurred.
- Physical calibration NOT RUN. Physical-job skips and field skips are not hardware proof. Historical area/timing values retain their original `e8454e27`/`49e1ce48` limits; no route or baseline re-record was performed.
- The manager owns hosted/local-replica acceptance, completion of the still-running contexts, independent verdicts, no-review-in-flight confirmation and donor-before-parent landing. This review does not replace those gates.
- The manager builds the final candidate from then-live dev at the merge turn, runs builder/native banks and links the receipts. The source base `e8454e2751d05b02ee8e5a571857589ab358ab86` and observed live dev `fa8209889411e8ca95757174c981f720dbcd95a2` are distinct. Hosted synthetic-merge tree equality does not discharge this duty.
- Selector step 3 remains the recorded manager follow-through: replace provisional duration/new-worker overhead using the successful hosted measurement procedure, with new evidence and review for any artifacts changed. Earlier optional coverage suggestions and the four residue entries remain on their respective checklists.
- Explicit merge authorization, post-merge containment, the post-merge daily area measurement and overall issue acceptance remain pending.

Final integrity verification compares all 1323 parent blobs and 1046 initialized dependency blobs against their committed raw bytes and executable modes, checks every complete stage-zero index, verifies all six root gitlinks and every initialized checkout, and confirms the exact parent/head/tree and clean worktree. The unused `external` checkout remains uninitialized; its gitlink is verified. No tracked bytes needed restoration because probes changed only in-memory copies.

Portable reproduction: `python3 scripts/run_checks.py <clone> <receipt-directory>`, `python3 scripts/count_probe.py <clone>` and `python3 scripts/verify_identity.py <clone>`. `scripts/capture_public.py` retrieves read-only public API responses. `MANIFEST.sha256` enumerates the publication set with packet-relative paths; `REPORT.md` is included. Full inherited diff, full downloaded logs, public-comment staging and disposable material remain under unpublished `scratch/`. Selected public excerpts are identified as excerpts; local gate and probe logs are raw command output.

R593-6 FINISHED
