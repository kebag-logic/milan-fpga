[R688] POSITIVE - exact head 01fc54756f1ffb0a3aa836681215e8321ee7e86c

R688-3 external independent documentary re-review of issue #774 / PR #778.

The public correction resolves R688-2-F1, and the PR role lines resolve R688-2-R1. No open BLOCKER, MAJOR or MINOR remains. All five lenses are CLEAN. The optional unequal-AAF-width suggestion remains optional.

Scope and provenance

This round judges the documentary changes since R688-2 at the same source head. Public PR metadata was fetched twice: its headRefOid (returned as head_sha) remains `01fc54756f1ffb0a3aa836681215e8321ee7e86c`; the PR body was unchanged between those reads. The local commit resolves to tree `7d8822f99d37284635fc34101123477e0c89846c`, also the R688-2 reviewed tree. Source base is `a032c6d6e3775f145349d5a495c1e1ad12294936`. There is no source delta since that review.

Reconstruction followed AGENTS/CONTRIBUTING, docs/README, issue body and frozen assignment, requirements and interface authorities, source diff/history, then public executable evidence. The independent diff pass preceded reading R688-2's public findings. No private author material or another reviewer's report informed this verdict. Code, test and gate coverage carries from R688-2 under the assigned later-round rule; this report does not claim a fresh execution of those banks.

Authorities: [frozen assignment](https://github.com/kebag-logic/milan-fpga/issues/774#issuecomment-6379902807), REQUIREMENTS.md section 2, CONTRIBUTING.md sections 2/3/6, AGENTS.md sections 6/7, `protocol-processor/docs/guides/integrator.md:328-337`, `docs/traceability/ieee8021q.md:154`, and their Milan 4.3.3.2 Table 4.4 / IEEE 802.1Q 35.2.2.8.4 references.

Resolved findings

- **R688-2-F1; MINOR; Tests, Docs; RESOLVED.** Artifact: [correction comment 6385747770](https://github.com/kebag-logic/milan-fpga/issues/774#issuecomment-6385747770), explicitly correcting REVIEW READY comment 6385545886. It says: “Five planted faults against the unchanged step are caught, and the clean control passes: six checks total.” Published `author-r2/scripts/round2/bdd_frame_mutants.py:26-35` defines exactly those six cases. `author-r2/receipts/round2/bdd/frame_mutants.log:1-7` records one clean pass, five catches, and six checks with zero failures; its rc is zero. The faults change data length, header length, tagged-frame length, the integer cast, and the arithmetic expression. The correction removes the previously overstated negative-control count. Required outcome and verification are satisfied by the explicit superseding correction and the one-to-one case/result comparison in `packet-check.log`; no new mutation is required.
- **R688-2-R1; RESIDUE; Docs; RESOLVED.** Artifact: PR body, “Linked Issue / roles,” captured in `pr.json`. It now says `Internal cleared-context reviewer: [R687]` and `External cleared-context reviewer: [R688]`, matching the public assignments. The exact requested administrative correction is present. No residue remains from this item.

Retained optional finding

- **R687-1-S1; SUGGESTION; Tests; RETAINED.** Artifacts: `hdl/milan/milan_datapath.sv:9057` and `tb/verilator/milan_dp/sim_crf_licence.cpp:1269-1277`. Both required shapes give the AAF talkers equal widths, so an AAF-only substitution of talker 0's value is not distinguished. The correct per-source index remains present, and the frozen required all-source substitution is caught through CRF on both shapes. Impact: optional coverage for unequal per-talker configuration. Optional outcome: configure one AAF talker's channel count differently and grade its independently calculated TSpec. Verification: an AAF-only slot-0 substitution should fail. This suggestion does not leave a lens unclean.

Prior findings carried at their causes

The [R688-2 report](https://github.com/kebag-logic/milan-fpga/pull/778#issuecomment-6385742647), preserved in `prior-and-start.json`, explicitly resolved the earlier items at this same head. Their cause artifacts remain byte-identical:

| Prior item | Status | Unchanged cause artifact |
|---|---|---|
| R687-1-F1; BLOCKER; RTL, Tests | RESOLVED, carried | `KL_crf_tx.sv:235` uses the supported 32-bit size cast; BDD feature and step unchanged; published behave receipt passes 406 scenarios |
| R687-1-F2; MINOR; Docs | RESOLVED, carried | SRP-10 cites the clause without the edition token; regenerated MODULE_MATRIX and README-tests carry 4.3.3.2 |
| R687-1-F3; MINOR; Tests | RESOLVED, carried | command-table.json contains the changed script digest, new runtime and both build forms; separate baseline inventory drift remains a manager item |
| R687-1-R1; RESIDUE; Docs | RESOLVED, carried | `ieee8021q.md:103` describes per-source frame geometry |
| R687-1-S1; SUGGESTION; Tests | RETAINED | Optional unequal-width coverage recorded above |

R688-1 was stopped without a verdict and contributes no coverage. After this verdict and ledger were written, the original R687-1 public finding sections were read directly. Their F1/F2/F3/R1/S1 requirements agree with the dispositions above; no additional unresolved item was found.

Applied lenses and reviewer-owned ledger

Each row records a PASS with its examined artifacts and authority. The documentary delta changes neither the source artifacts nor their dependencies. Tests and Docs are re-covered here after resolving the public evidence defect.

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Issue #774 frozen formula/shape acceptance; processor integrator :328-337; shadow :301/:1284; CRF :235/:248; datapath :9053-9058; wire receipts still show CRF 29 and AAF 217. No new protocol or clause claim in the documentary correction. | R688-2, carry verified R688-3 | 01fc54756f1ffb0a3aa836681215e8321ee7e86c |
| RTL | CLEAN | CRF :227-248; shadow per-source vector; datapath g_pp_maxf and :9407; exact tree/index/blob verification. Combinational mapping, widths and framing unchanged; no clock/reset/handshake delta. | R688-2, carry verified R688-3 | 01fc54756f1ffb0a3aa836681215e8321ee7e86c |
| Robustness | CLEAN | Source guard :1675-1694; harness :1274-1328; CRF and declaration receipts; six BDD case definitions and result lines. No change to malformed-input, refusal, reset, disabled-feature or backpressure coverage. | R688-2, carry verified R688-3 | 01fc54756f1ffb0a3aa836681215e8321ee7e86c |
| Tests | CLEAN | Published bdd_frame_mutants.py CASES versus frame_mutants.log and rc; correction 6385747770; unchanged Makefile/harness/mutation driver; gate-spotchecks.log. Five negative controls plus one clean control are accurately claimed. | R688-3, with R688-2 executable coverage carried | 01fc54756f1ffb0a3aa836681215e8321ee7e86c |
| Docs | CLEAN | Current issue correction and complete PR body in issue.json/pr.json; prior finding reconciliation; source diff/history and unchanged generated documentation. Roles are concrete; current numerical claims inspected do not overstate evidence. No new source-comment wording exists in this round. | R688-3 | 01fc54756f1ffb0a3aa836681215e8321ee7e86c |

Verification and evidence limits

- `verify_packet.py` verifies 734 receipt files across the archive's author and author-r2 receipt directories against published_sha256 at evidence commit `4484c29cd1224098b5b0d4576cc5d8e4897b4836`. It also verifies the selected script, matches all six case definitions to their result lines, and checks the correction, roles and head/tree. See `packet-check.log` and the unchanged selected raw files under `published-receipts/`.
- The archive has no embedded signature and supplies no detached signature. Hash consistency is verified; signer authentication is not claimed.
- `gate-spotchecks.log` contains attributed excerpts from published source receipts: behave 406 passed; crflic 427/0; tspec8 61/0; crf_tx 129/0; mutation campaign verdicts; docs and native fast-replica results. One initial lookup used the full mutation-log name; the archive publishes its verdict extract and digest/size instead. The completed spot-check uses that extract, not an unavailable full log.
- Remaining source gate coverage carries exactly as R688-2 recorded: the sweep at 0d4b4620, synthesis/route at 2a0085dd, and exact-head documentary/native-replica evidence. The PR's detailed tables retain those evidence heads and carry explanations. The docs count is 44 recorded steps, including two explicit skips, not 44 executed successes. The PR enumerates five BDD faults and a clean pass without claiming a sixth fault.
- `verify_checkout.py` verifies all 1,441 superproject tracked blobs plus six gitlinks, full index entries, modes and populated submodule bytes/indexes against their pins. All four required submodules and the additional lwSRP checkout pass. Optional external is uninitialized. The checkout is clean. No source edits or mutation executions occurred in this round.
- Physical calibration was NOT RUN. Field skips and simulation are not hardware proof. Full standards texts and full build/simulation/synthesis banks were not independently rerun here. No manager source bank is claimed.

Pending manager duties

The manager owns exact-head hosted/act acceptance, including distinguishing executed jobs from skipped contexts. This round does not infer a hosted pass. Validate the final current-dev merge candidate with the required builder and native banks and link its receipts at the merge turn; source validation does not replace that step. Complete independent review, ensure no review remains in flight, obtain merge authorization, then perform post-merge containment and Issue/Project completion. Pre-existing inventory regeneration remains separate manager work. No GitHub writes, commits, pushes, merge, hardware operation or forbidden bank was performed by this review.

R688-3 FINISHED
