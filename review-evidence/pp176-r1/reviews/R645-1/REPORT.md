[R645] NEGATIVE - exact head 29f58ad30a97327d92b50f17f49d085cd97066a5

The two supported forms share the intended validation and response behavior. One MAJOR acceptance gap remains: longer bodies are accepted and produce longer responses. This behavior also exists at base, but the frozen public assignment explicitly requires refusal of every other length. One comment-only RESIDUE is recorded separately.

Reviewed tree: `c6fbf3914e940bf129152ba341b80d686ba30247`. Source base: `22c139a4323bc96c779d13e3f6774480c5fb9b75`. The one-commit diff changes twelve files. There is no register-map, top-level port, parameter, or microprogram-byte change. All five lenses were applied independently. The independent verdict and ledger were written in `receipts/independent-verdict.md` before inspecting public prior-review results.

**Authority and scope**

The processor tree contains no AGENTS.md or CONTRIBUTING.md. The supplied operating instruction, public parent AGENTS.md / CONTRIBUTING.md, processor docs/README.md, and public parent docs/README.md supplied the review conventions. The frozen behavioral authority is [issue #176](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/176), especially the [public assignment](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/176#issuecomment-6236134563). Its owner decision accepts both IEEE editions; its next instruction says, “Any other length is still refused, exactly as today.” No subsequent public comment narrows that instruction to shorter lengths.

Local authorities examined: `docs/00_MILAN_COMPLIANCE_REVIEW.md:433` (REQ-AEM-009); `docs/architecture/01_overview.md:146` (direction restriction); `02_interfaces.md:401` (published presentation offset and streaming feedback); `06_aecp_engine.md:261`, `:493`, `:1230` (command table and behavior); `07_memory_maps.md:649` (offset row); `09_verification.md:184`, `:570`, `:611` (coverage and command-model limits); and `hdl/README.md` (consumption contract).

The clause baseline is IEEE 1722.1-2021 7.4.15.1, Figure 7-40 and its NOTE, IEEE 1722.1-2013 Figure 7.46, and Milan v1.2 5.4.2.9. The owner decision, rather than an inferred extension of the NOTE, authorizes accepting the legacy command. The explicit task contract supplies the exact-length rule used in this review. The final specification PDFs are not distributed in the checkout; public retrieval did not yield the complete final IEEE clause/NOTE. Consequently this report does not claim a fresh verbatim verification of that NOTE or claim that IEEE itself prohibits all longer commands. That limitation does not alter the directly demonstrated violation of the frozen project acceptance.

**Findings**

**R645-F1 | MAJOR | Conformance, RTL, Robustness, Tests, Docs**

Artifacts: `hdl/aecp/KL_aecp_engine.sv:3612` and `:3761`; `tb/aecp_cmds/sim_main.cpp:311`; `tb/aecp_cmds/decode.json:87`; `docs/architecture/06_aecp_engine.md:493`; PR #183, “What changes” and “Acceptance”; `receipts/head-length-probe.runtime.log` and `receipts/base-length-probe.runtime.log`.

Authority/evidence: the public assignment requires both exact body lengths, refusal of every other length, and a 2021-form response. The dispatch guard exempts the exact legacy form but otherwise rejects only `cdl < 96` or walked payload `< 84`. The response-length assignment preserves the incoming payload size for every nonlegacy echo. A valid output command with MSRP_ACC_LAT_VALID and latency 750000 therefore produces:

| Command body / cdl | Head response | Required by frozen acceptance |
|---|---|---|
| 48 / 60 | SUCCESS, cdl 96 | SUCCESS, cdl 96 |
| 84 / 96 | SUCCESS, cdl 96 | SUCCESS, cdl 96 |
| 85 / 97 | SUCCESS, cdl 97 | Refusal, cdl 96 |
| 128 / 140 | SUCCESS, cdl 140 | Refusal, cdl 96 |

Every cdl from 97 through 140 failed the reviewer-owned acceptance check. These 44 failures are also present at base. The new valid-flag templates exercise only 60 and 96; the generic longer probes carry unsupported flags, so the recorded green sweep does not exclude successful oversized commands. The updated documentation and PR narrow the rejection statement to lengths below 96, while also claiming the response is always the 2021 form. This is a behavioral acceptance conflict, not wording residue.

Impact: an unsupported body length enters the setter microprogram and receives an oversized successful response. The implementation and its tests do not establish the requested two-length contract. The issue remains incomplete even though this particular defect is inherited.

Required outcome: enforce the frozen exact-length contract, including the corresponding response size, and add valid-flag upper-bound refusal checks with planted mutants. Update the command record and authoritative documentation to the same contract. If retaining the existing longer-command behavior is intentional, obtain an explicit public owner scope resolution before re-review; the author’s PR wording alone cannot change frozen acceptance.

Verification: rerun `scripts/run_focus.py` against the corrected revision, with cdl 59/60/61 and 95/96/97 plus additional longer lengths; require correct refusal status, cdl 96 and no offset write for rejected shapes. Add a mutation that reopens the upper-length gate and require the new assertions to fail. Regenerate and check the observed-command record. The current probe provides a reproducer, not an assertion of a new regression relative to base.

**R645-F2 | RESIDUE | Docs**

Artifacts: newly added comments in `tb/pp_top/sim_main.cpp:8095`, `:8185`, `:8200`, `:8206`, `:8223`, `:8230`, `:8251`, `:8314`; new behavioral comment anchor `hdl/aecp/KL_aecp_engine.sv:803`.

Authority/evidence: the owner’s 2026-10-15 comment rule requires behavior and reason with issue and requirement IDs, without bench/lane labels. The new comments use W24/W25 row navigation and cite #176 without its requirement ID. Existing comments outside the delta remain outside this finding.

Impact: comment-only traceability and wording residue. This finding changes no logic, measurement, test assertion, figure, verdict or clause interpretation and does not independently make any lens unclean.

Exact correction: add `issue #176, REQ-AEM-009` to the new behavioral comment anchors. Replace `(W24g-W24l, issue #176)` with `(issue #176, REQ-AEM-009)` and drop `(W24m)`. Replace the new W24g-W24m banner and its “Run from W24...” navigation with “Exercise the legacy body and an unsupported short body; preserve the stored offset across the refusal checks (issue #176, REQ-AEM-009).” Remove the new W24g/W24g2/W24i-W24l/W24m/W25b3 comment prefixes; describe repeat-write, refusal, and streaming behavior directly. Replace “back to W24a’s value” with “back to the initial offset.” Keep executable names, assertion strings and findings tables unchanged. Any substantive correction of the length claim belongs to F1, not this residue.

Verification: review only added comment lines in the revised diff for issue/requirement traceability and forbidden navigation labels. No functional test is needed for this wording-only change. The manager carries it to the residue checklist.

**Reviewer-owned lens ledger**

| lens | CLEAN/UNCLEAN | examined artifacts and result | covering round | exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN | Issue #176 assignment; REQ-AEM-009; F06.14; command-body field offsets; both-form status and byte checks. F1 violates the explicit length contract. | R645-1 | 29f58ad30a97327d92b50f17f49d085cd97066a5 |
| RTL | UNCLEAN | Engine :803, :1562, :2576, :3612, :3707, :3761; discriminator capture/reset, walked-length bound, flags/latency dispatch order, response mux and length; unchanged generated ROM. F1 remains. | R645-1 | 29f58ad30a97327d92b50f17f49d085cd97066a5 |
| Robustness | UNCLEAN | cdl 12..140; complete/one-byte-short slots; poisoned legacy tail; zero/max/high-bit latency; empty/extra flags; streaming; invalid direction/index; state sequencing inspected. F1 accepts oversized input. | R645-1 | 29f58ad30a97327d92b50f17f49d085cd97066a5 |
| Tests | UNCLEAN | Exact-head command suite; top W24/W25 assertions; seven published mutation patches and named failures; independent boundary control and reserved-word mutant. F1 exposes missing upper-size valid-flag coverage. | R645-1 | 29f58ad30a97327d92b50f17f49d085cd97066a5 |
| Docs | UNCLEAN | docs/README, architecture 06/09, JSON field registry and generated copies, both suite READMEs, public PR and parent handoff. F1’s narrowed contract is substantive; F2 is nonblocking residue. | R645-1 | 29f58ad30a97327d92b50f17f49d085cd97066a5 |

RTL-specific scope result: the shared frame-byte and response-length changes are guarded by `si13_w`, which requires SET_STREAM_INFO and exactly cdl 60 / payload 48. No unrelated opcode arm changes. Payload length is bounded against the committed slot before recognition; latency capture settles before dispatch. Streaming refusal precedes flag and value validation. The legacy reserved word is suppressed before it could become 2021 `ip_flags`. No new register, clock domain or external interface is introduced. The generated base/head ROM hashes are identical: `518b900c4a5650902c3ea9125941e434857ba2f379b6c92268a67fef459d37f8`. These observations do not clear F1.

**Executed evidence**

| Reviewer-owned execution | Result | Receipt |
|---|---|---|
| Exact-head command-engine suite | 596404 trials; 176 PASS, 0 FAIL; rc 0 | `head-engine-suite.runtime.log` |
| Exact-head length/semantic probe | 143 checks; 44 failures, all cdl 97..140; rc 1 | `head-length-probe.runtime.log` |
| Same probe at base | 143 checks; 52 failures: same 44 plus eight legacy-form checks; rc 1 | `base-length-probe.runtime.log` |
| Both-form boundary/short-slot/poisoned-tail control | 16 checks, 0 failures; rc 0 | `head-edge-control.runtime.log` |
| Published reserved-word mutant replay | Four legacy complete-body byte checks fail; other twelve pass; rc 1 | `reserved-word-mutant.runtime.log` |
| Command-model/documentation gate and self-test | Gate passes; 231 planted defects caught by name | `command-doc-check.log`, `command-doc-selftest.log` |
| Microprogram entry-map check | 61 engine constants / 89 entry points agree | `upc-check.log` |
| Parent patch applicability | Clean at recorded parent base and stated live dev | `parent-patch-check.txt` |
| Final checkout integrity | All 618 tracked entries match raw blobs, modes and index; no gitlinks in processor tree | `final-integrity.txt` |

Receipts are under `receipts/`. The compiler identity was checked as the requested pinned 5.050 release before builds. Independent campaigns ran concurrently inside foreground orchestrators, each with its own log and rc file. The first group used three builds with four compiler jobs each; the second used two. Every build invocation used `make -j16` with the inner compiler build bounded to four jobs. There were no detached jobs, full processor/parent banks, hardware runs, source fixes, commits or remote writes.

Reproduction: run `scripts/run_focus.py --repo <processor-clone> --verilator <pinned-5.050-executable> --jobs 3`, then `scripts/run_edges.py` with the same arguments and `--jobs 2`. The scripts export the named revisions into packet-local scratch directories and change only disposable probe copies. `scripts/audit_checkout.py --repo <processor-clone>` verifies the original. `prepare_receipts.py` selects verbatim runtime result lines; build transcripts contain host-specific support paths and are not published. `runtime-provenance.json` records their original hashes and the selected runtime hashes. The per-campaign `.rc` files retain the actual process results.

The published [source evidence package](https://github.com/kebag-logic/milan-fpga/tree/6e9bd7b5239ba94797024b38a558026836bab76f/review-evidence/pp176-r1) was inspected after the independent diff pass. All thirteen file hashes match its published manifest. Its mutation results cover each changed/new top-level assertion:

| Check | Published mutant that fails it |
|---|---|
| W24g, W24g1, W24g2 | legacy body refused again |
| W24i, W24j, W24k, W24l | legacy body refused again |
| W24l2 | legacy latency uncaptured; flag gate opened |
| W24m, W24m1, W24m2 | any shorter body treated as legacy |
| W25b3 | legacy body refused again |

Additional published controls exercise echo length, tail leakage and reserved-word conversion. The reviewer independently replayed the reserved-word control against the boundary probe. The other published top-level mutation results and full source-gate tallies are author-owned evidence, not reviewer reruns or manager source-bank execution.

**Parent adoption and evidence limits**

The published `parent-adoption-milan_dp-67.patch` changes the old refusal expectation to SUCCESS/cdl 96 and supplies the already-stored 750000 offset, preserving the following readback expectation. It applies cleanly to public `sim_nxn.cpp` at both `7d79ffb26308ac51eaeeab6ec43d798d057ae0cd` and `e9cbb676d7fdd6539aa408e5dfe38870a4ae1a5f`. The public results report that this is the only behavioral test adaptation needed: unpatched head fails the two section #67 checks; patched head passes with the base per-leg tallies. No independent full parent suite was run.

It is not the only parent adoption work overall. The public handoff reports two other failures at both base and head: `measure_test_evidence.py --check` identifies the same three previously introduced readers, and `check_submodule_docs.py` identifies the changed pin and stale diagram. Their recorded rc values are 1 at both revisions and 0 at the old parent pin. Their log hashes differ; the public package contains their digest index and summarized failure signatures, not those complete logs. Thus the supported conclusion is identical reported failure causes, not independently verified byte-identical logs. Classification and pin documentation remain adoption duties. Two parent comments also retain the old legacy-refusal description (`tests/steps/aecp_engine_steps.py:186` and `tb/verilator/milan_dp/sim_nxn.cpp:6862`); carry their wording cleanup into adoption.

At the captured exact-head hosted snapshot, both workflow runs have completed documentation and portability jobs with actual successful execution steps. Both suite jobs remain in progress. Their cached-compiler build steps are skipped; those skips are not test results. `hosted-summary.json` preserves job identities, head, timestamps and step conclusions. Hosted/local-replica acceptance remains the manager’s responsibility.

No manager source bank exists or is inferred at this head. Source validation is the author’s published source-gate evidence plus the focused reviewer executions above. It is distinct from the manager’s future current-dev merge candidate. The source base is `22c139a4`; the stated live parent dev is `e9cbb676`. Builder and native candidate-bank receipts must be published at the merge turn. Concurrent engine work for #177/#178/#181 must be reconciled there, with the dispatch/microprogram-map checks rerun after any conflict resolution.

The final clause PDFs were not independently obtained in full. The review did not run exhaustive stalls/reset permutations, a separate legacy lock test, physical calibration, field validation, synthesis banks or timing closure. The published builder result includes one NOT RUN item. Physical calibration is NOT RUN; neither that result nor field skips constitute hardware proof.

**Prior findings and completion duties**

After the independent verdict and ledger were written, the public issue comments, PR conversation, review submissions and inline-review comments were fetched again. The snapshot contains three issue comments, two PR review-start comments, zero review submissions and zero inline comments. There are no prior public FINDINGS on this PR in that snapshot to resolve or retain. No other reviewer’s private report was read.

Before acceptance, resolve F1 and re-review the corrected exact head, carry F2 to the residue checklist, complete the parent patch/classification/pin-documentation work, obtain both independent positive reviews, and validate the manager-built current-dev candidate with published receipts. This negative source review clears no merge gate.

The original detached checkout was never edited. Final raw blob, executable-mode and stage-zero-index verification passes for all 618 entries at the required head and tree. This standalone processor contains no required submodule gitlinks; parent submodules were not checked out or modified. `MANIFEST.sha256` lists every publishable receipt and script. Disposable sources, builds and downloaded previews remain under `scratch/` and are excluded.

R645-1 FINISHED
