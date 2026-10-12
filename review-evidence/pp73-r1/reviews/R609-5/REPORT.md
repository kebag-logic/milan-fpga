[R609] POSITIVE - exact head 4bee75b2e647507a71ece50359fceb135c334757

External independent delta review of issue #73 / PR #174, round R609-5. Tree `6bca4f9099adb67e6ca3758f9738975bba32d2d4`; original source base `2cbed0a987c1e68402658d69459ab7e5aa571adc`. All five lenses are CLEAN. No open BLOCKER, MAJOR or MINOR remains. Two inherited wording residues and four optional suggestions are retained explicitly below.

The [round-5 ruling](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/73#issuecomment-6114909820) is satisfied. The merge preserves both gate sets and their rules, regenerates the command references consistently, holds the added observation check to execution tracing, and retains the round-4 failure controls. Source approval does not replace the manager's final current-dev candidate validation.

The review followed the [public assignment](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/pull/174#issuecomment-6116584442). No repository or ancestor AGENTS.md/CONTRIBUTING.md was found. The supplied command-wrapper instruction and `docs/README.md` were read first, then the [issue body](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/73), frozen lane scope, public Mark II decision and subsequent manager rulings. Authorities examined included REQ-VER-002/GAP-11, architecture 01/02, F06.14 and the realized inventory, verification sections 7/8.10/8.11, HDL conventions, the guard contract and public parent Rule 12. The project's status-code transcription was examined; copyrighted specification PDFs were not independently re-audited.

The base-to-head diff and history were reconstructed before public execution evidence. Detailed examination focused on the merge resolution and its consumer paths. The complete diff, round-5 diff and remerge comparison are retained. The independent verdict and five-lens ledger were written in [independent-verdict.md](receipts/independent-verdict.md) before reading any prior public reviewer findings or reports. Eight prior public findings comments were then reconciled. No private author material, management checkout or lane scratchpad was read.

**Merge and acceptance evidence**

| Required outcome | Examination and result |
|---|---|
| Required merge; no unrelated change | Parents are exactly `4029dc5de2a0a540d6a015c747319fbee7abba2e` and `6d536868ee2a4762ab307d5ed51ff09c01130942`. The remerge comparison contains only the three conflict files plus necessary section references, field-generator section number, observation wrapper/README/Makefile and refreshed record. [Merge audit](receipts/merge-audit.json) enumerates every path. |
| Both sides' targets and gates | `Makefile:10,15` retains `reqtags` and `aecpcmd`, including their self-tests. `.github/workflows/hdl.yml` retains executed trace checking, command controls and guard portability. `scripts/check-req-tags.py`, both tag helpers and both guard drivers are byte-identical to imported main. |
| Generated material reproduced | Deliberately damaged F06.14, gate docstring, verification registry and compliance Arch text were repaired by `check_aecp_commands.py --write`; a second generation was identical. Trace states and coverage records were independently recomputed with the unchanged trace gate's `read_rows/read_tags/row_states/check_records` functions: 115 rows, 101 traced, 8 waived, 6 needing no dynamic check. See [regeneration](receipts/regeneration.json) and [trace records](receipts/regenerated-trace-records.json). This establishes reproducibility/freshness, not an observation of the author's editing process. |
| New check satisfies tracing | `tb/aecp_cmds/check_observed.py:28` tags `ObservedCommands.test_sweep` as REQ-VER-002/DIR. The requirement remains a lint row, correctly recorded as `A; no check`; no invalid waiver was added. The fresh local run emitted the exact expected tag. The wrapper preserves output and status for passing and unreadable observations. Rechecking the author's actual complete-suite log and 226 evidence lines passes; removing this tag fails `DEAD TAG REQ-VER-002` by name. [Trace audit](receipts/trace-execution-audit.json), [wrapper parity](receipts/wrapper-parity.json). |
| Command model and RTL preserved | Table, registry and ROM generator equal round 4. All 46 production RTL files equal imported main. The recorded behavior equals round 4; only five digests changed for imported guard edits. Both generated ROMs equal original base, imported main and exact head. No new datapath/interface change is introduced. [ROM identity](receipts/rom-identity.json), [merge audit](receipts/merge-audit.json). |
| Guard checks and source gates | Reviewer `make -j16 check` passes; the focused guard suite passes 93/93 inventory and boundary checks. Published author portability receipts cover the second frontend; the imported guard rules are unchanged. |
| Round-4 controls remain effective | All 231 plants fail by their expected names, including 30 held-field plants, under normal and optimized execution. Fresh shortened-EAVL responses fail with no exemption, with the prohibited echo-hide membership, and with explicit shared membership, including after re-recording. Both permitted membership forms pass. Disabling membership, ROM SUCCESS restriction or observation SUCCESS restriction separately causes its named self-test failure. |

The reviewer-owned execution receipts are:

| Check | Result | Receipt |
|---|---|---|
| `make check` | rc 0; both gates and their self-tests executed | [make-check.log](receipts/make-check.log), matching `.rc` |
| Fresh observation suite | 585,760 trials, 0 timeouts; 176 PASS, 0 FAIL | [observed.log](receipts/observed.log) |
| Guard suite | 93 PASS, 0 FAIL | [guards.log](receipts/guards.log) |
| Behavioral campaign | 16/16 named failures; golden and restored PASS; every build and sweep completed | [controls/results.json](receipts/controls/results.json), per-variant raw logs |
| Field/refusal/size/echo plants | 231/231 with actual named diagnostics; 30 held fields included | [named-plants.json](receipts/named-plants.json), [optimized-selftest.log](receipts/optimized-selftest.log) |
| Fresh echo controls | All three variants rejected by membership or ENTITY_AVAILABLE response size | [echo/results.json](receipts/echo/results.json), raw generation/sweep/record/gate logs |
| Round-4 check-disable controls | Both legal membership forms pass; all three disabled checks fail by intended name | [round4-controls.json](receipts/round4-controls.json) |
| Actual PR field reference | Generated registry reference agrees, rc 0 | [pr-reference.log](receipts/pr-reference.log) |
| Preservation | 618 tracked files: exact bytes, modes and index; clean detached head; zero gitlinks | [integrity.json](receipts/integrity.json) |

Independent campaigns ran concurrently under foreground supervisors that awaited every child. Campaign drivers received `--jobs`; make used `-j16`; each compilation was limited to two workers. The scoped compiler identified itself as version 5.050 before use. Disposable trees and temporary files stayed under `scratch/`. One initial reviewer check-disable fixture removed shape validation too broadly; it was corrected to disable only membership. The original diagnostic and [setup explanation](receipts/probe-setup-note.txt) are retained; this was not a source defect.

**Prior public findings: disposition at this head**

The exact quotations and links are in [prior-public-findings.json](receipts/prior-public-findings.json). No prior blocking finding is silently waived.

| Prior ID | Disposition and verification |
|---|---|
| R608-1-F1 | RESOLVED: fresh behavioral decode/dispatch comparison; q1 and q2 independently fail by command name. |
| R609-1-F1 | RESOLVED within the publicly frozen scope: fixed/variable response rules, echo equality and command floors remain protected. GET_AUDIO_MAP 20/28 and header-NOP controls fail by name. Declared floor/unswept limits remain explicit rather than being counted as proof. |
| R608-1-F2; R608-2-F3 | RESOLVED: real-file generator-read defects and generator-alone missing-name/entries/nonhex-opcode cases are named; explicit refusals survive optimization. |
| R608-1-F4 / R609-1-F2 | RESOLVED: table prerequisites remain in pp_top, ucpu and aecp_cmds ROM rules; the first two rules are unchanged from the reviewed round-4 parent. |
| R608-1-F3 / R609-1-F3 | RESOLVED: stored plural units are rendered unchanged; regeneration reproduces the correct F06.14 rows. |
| R608-2-F1 | RESOLVED: accepted-offset gcd holds the echo record step exactly; both four-byte and sixteen-byte compiled controls fail by name. |
| R608-2-F2 | RESOLVED by authorized declaration: common_status, engine_status and oversize remain explicitly held to nothing; status claims retain their conditions. |
| R609-2-F1 | RESOLVED: documented opcode/rtl/gdi semantics are distinguished from identity/rendering; all three held-field plants fail semantically after F06.14 regeneration. |
| R608-3-F1 | RESOLVED by mandated construction: membership, non-SUCCESS scope, held registry entry and named echo-hide controls all reproduce. |
| R608-1-S1 / R609-1-S4; R609-1-S1/S2; R608-1-S2 / R609-1-S3; R608-2-S2 | TAKEN: explicit field reference, fixed status-code authority, documented-row shape, optimization-safe refusal and complete listed sweep-input digests remain present and tested. |
| R608-2-R1 / R609-2-R1; R608-3-R1 / R609-3-R1 | RESOLVED in the current PR wording; historical disposition still belongs in parent #495 at merge. |
| R608-4-R1/R2 | RETAINED as wording RESIDUE below. |
| R608-4-S1; R608-3-S1; R608-2-S1/S3 and later aliases | RETAINED as optional suggestions below. |

**Retained findings and suggestions**

**R608-4-R1 — RESIDUE — Docs.** Artifacts: `tb/aecp_cmds/README.md:69` and `docs/architecture/09_verification.md:581`. Evidence/authority: these inherited short prose descriptions omit the non-SUCCESS echo exception already defined at verification `:583`, in the generated registry and in `scripts/aecp_gate/rom.py:336` / `scripts/aecp_gate/record.py:326`. Impact is wording only: the governing exception and measured behavior are unchanged. Exact required fixes: append to the README sentence, replacing its terminal period, “; a non-SUCCESS answer of an `echo_entries` program may instead carry the command's own length.” Replace the verification sentence with “Every response and unsolicited body has the table's size, except that a non-SUCCESS answer of an `echo_entries` program may echo the command (the `echo_entries` row).” Verification: manager residue checklist checks these prose changes without changing generated material or the established contract.

**R608-4-R2 — RESIDUE — Docs.** Artifact: PR #174 body, Round 4 closing paragraph. Evidence: it still says “The publication-wording residue remains assigned to the merge manager under parent #495; no existing public text is edited.” The body already contains the round-3 corrections. Impact: historical publication wording only. Exact required replacement: “The round-3 wording residue (R608-3-R1 / R609-3-R1) is applied in this body; its record goes to parent #495 at merge.” Verification: manager checks the replacement and records the historical disposition. No public text was edited by this review.

**R608-4-S1 — SUGGESTION — Robustness, Tests.** Artifacts: `scripts/aecp_gate/table.py:169` and `hdl/aecp/ucode/aecp_fields.json:787`. The authorized explicit-shared route accepts an added shared key; the registry declares that trust. A deliberately widened shared list can permit a non-SUCCESS echo exemption. SUCCESS remains protected, as the fresh explicit-shared probe proves. Optional outcome: restrict single-owner shared keys or state this admission effect more explicitly and add its control. Verification: a false shared-key/non-SUCCESS-size plant is rejected, or its declared scope is tested. This is the literal permitted rule, not a round-5 regression.

**R608-3-S1 — SUGGESTION — Tests, Robustness.** Artifact: `tb/aecp_cmds/sim_main.cpp:306`, unchanged count-one lengths 24/28. Prior public evidence and source inspection establish that overlength count-one acceptance is outside the bounded observer's guarantee. Optional outcome: retain cdl 36 as well. Verification: an overlength-acceptance mutation fails by command name after re-recording.

**R608-2-S1 / R608-3-S2 — SUGGESTION — Tests, Robustness.** Artifact: `tb/aecp_cmds/sim_main.cpp:397`, unchanged MVU stimulus. Wrong protocol-ID bytes @22/@24 remain unswept, as the public earlier probe documents. Optional outcome: flip each byte independently and retain compiled controls. Verification: weakened comparisons fail semantically after re-recording, beyond an input-digest mismatch.

**R608-2-S3 / R608-3-S3 — SUGGESTION — Tests, Docs.** Artifacts: `tb/aecp_cmds/aecp_cmds_wrap.sv:164,256`, stimulus templates and verification section 8.11. Lock-held/deadline inputs are tied low; bound-only and nonzero-descriptor-index cases remain outside the sweep. Optional outcome: name these examples in the limits or add independent stimuli. Verification: the limits match the stimulus, or new named controls demonstrate each added outcome. These four suggestions do not make a lens unclean.

**Public evidence and real limits**

The immutable [published packet](https://github.com/kebag-logic/milan-fpga/tree/2d87396a55ba902af635ae139d24509dc607378e/review-evidence/pp73-r1) supplies wider author source evidence. Sixty-seven selected receipts match their immutable Git blob IDs; the author's execution-export digest list independently matches all 618 exact-head files. Author receipts report 1,029,951 full-suite checks with zero failures, 226 executed requirement tags, 18 existing campaign pairs passing and unchanged source-style budgets. These banks were not rerun here and are not manager source-bank results. The published raw engine elaboration matches merged main; original-base comparison uses only the stated source-location normalization. Original-base/raw-netlist byte identity is not inferred across the imported guard changes.

At 2026-10-12 02:36:40 UTC, [push run 38195249500](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/actions/runs/38195249500) has successful executed documentation and portability jobs. Its checkout log confirms the exact source head. [PR run 38195252851](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/actions/runs/38195252851) has the same completed jobs, but its checkout is synthetic merge `cda576a` onto processor main. Both suites jobs remain in progress; later checks have no passing conclusion. The compiler-build steps were skipped after cache use, not executed builds. Neither complete hosted acceptance nor the final parent candidate is established by these snapshots.

This is a delta review, not a repeat of every prior broad campaign or a fresh clause audit. The observer stops at opcode 0x007F and its stated cdl/template population; GDI ceilings and unswept outcomes are unproven. Common/engine statuses and oversize retain declared limits. ROM walking holds sizes/statuses/lock/notification, not field values/order. Golden-model/stimulus generation, ACMP/timing-table generation and parent firmware consumption are outside the frozen delivery. Physical calibration **NOT RUN**; field skips are not hardware proof.

**Reviewer-owned ledger**

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Frozen issue/rulings; REQ-VER-002/GAP-11; table/registry/export; merge resolution; scope and declared limits | R609-5 independent delta; prior resolved scope retained | 4bee75b2e647507a71ece50359fceb135c334757 |
| RTL | CLEAN | 46 production blobs versus main; guard diffs/boundaries; fresh dispatch/response observations; three-revision ROM identity; published elaboration | R609-5 | 4bee75b2e647507a71ece50359fceb135c334757 |
| Robustness | CLEAN | 231 named plants; 30 held fields; fresh echo variants; three disabled-check controls; 16 compiled mutants; exact restoration | R609-5 | 4bee75b2e647507a71ece50359fceb135c334757 |
| Tests | CLEAN | make check; 93 guards; 585760 trials/176 checks; golden/restored campaign; tag execution and omission; wrapper parity; CI paths | R609-5 | 4bee75b2e647507a71ece50359fceb135c334757 |
| Docs | CLEAN | docs/README; 00 Arch/Cov; 06 F06.14; 09 sections 8.10/8.11; field generator; trace records; actual PR reference; retained wording residues | R609-5 | 4bee75b2e647507a71ece50359fceb135c334757 |

**Pending manager duties and preservation**

No manager source bank runs at this exact head, and none is claimed or inferred. Source validation is distinct from the final current-dev candidate: original source base `2cbed0a987c1e68402658d69459ab7e5aa571adc`, assigned live dev `c20c85bddd4ec5a054be42b55fc291a3b4c7f7d8`. At the merge turn the manager builds that candidate, validates builder/native banks and applicable parent evidence-reader/style dispositions, verifies required parent gitlinks, and links receipts on the PR. The manager owns hosted/act acceptance, the independent-review completion bar, #495 residue disposition, the parent export-consumer follow-up and publication.

The source clone remained untouched by probes. Final working blob bytes, executable modes and index match the exact head/tree; this standalone processor contains no required submodule gitlinks. This does not replace parent-candidate gitlink verification. No source fix, commit, push, GitHub write, merge, author contact, delegation, privileged action, shared install or hardware run occurred. Scripts and raw receipts are listed by packet-relative SHA256 in `MANIFEST.sha256`; `scratch/` is excluded. Only listed files and this report are publication material. Reproduction instructions are in `scripts/REPRODUCE.txt`.

R609-5 FINISHED
