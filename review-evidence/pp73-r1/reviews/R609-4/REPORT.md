[R609] POSITIVE - exact head 4029dc5de2a0a540d6a015c747319fbee7abba2e

External independent delta review of issue #73 / PR #174, round R609-4. Tree `33ec74ea7812208d7648475763816bc14a80bc8a`; original source base `2cbed0a987c1e68402658d69459ab7e5aa571adc`; preceding reviewed head `15981b511370a8cfb58ec023fae27f8a800c058c`. The delta is one commit. All five lenses are CLEAN. No BLOCKER, MAJOR or MINOR remains in the reviewed scope.

The [round-4 ruling](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/73#issuecomment-6112358948) is satisfied by construction. Membership is checked, the shared-entry exemption applies only to non-SUCCESS answers, echo-hide fails by name, and the registry and generated references agree. R609-3's earlier POSITIVE scope is unchanged. Three verdict-neutral coverage suggestions and the manager's historical wording-residue duty are retained below.

The review started from the [public assignment](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/pull/174#issuecomment-6114258109). No repository AGENTS.md or CONTRIBUTING.md, or ancestor AGENTS.md, was present. The supplied command-wrapper instruction, repository/HDL README and `docs/README.md` were read first. Next came the [issue acceptance](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/73), [frozen lane scope](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/73#issuecomment-6100509798), public Mark II decision, and round-two through round-four rulings. Requirements and interface authorities examined include REQ-VER-002/GAP-11, architecture 02, 06 F06.14 and its realized inventory, 09 sections 1/7/8.10, and public parent Rule 12. The project's status-code transcription was examined; copyrighted specification PDFs were not independently re-audited.

The base-to-head diff and history were reconstructed before public executable evidence was examined. Detailed independent examination focused on the round-4 commit and its consumer paths. The base diff contains 31 files; the round-4 delta contains 11. No production RTL, ROM generator, observer stimulus, recorded observation, build rule or workflow changes in this delta. The independent verdict and five-lens ledger were written to `receipts/independent-verdict.md` before any prior public review findings were read. All six earlier public findings comments were then reconciled. No private author material, management checkout, lane scratchpad or separate reviewer report file was read.

The ruling is supported by these exact-head artifacts and reviewer-owned results:

| Required outcome | Implementation and verification |
|---|---|
| Shared membership, otherwise refusal by name | `scripts/aecp_gate/table.py:169` checks list/member shape, first-entry ownership and use by at least two command rows, with explicit `shared_entries` as the other permitted route. Command entry lists already reject repeats. `aecp_commands.json:44` explicitly declares BADARG and NSUPPE shared. Independent probes accept implicit shared TIZ4NS and explicitly shared EAVL; reject private EAVL, private secondary RDESCENT, an unknown name, an owned entry used elsewhere, and removal of either required declaration. See `independent-echo-probes.log`. |
| Non-SUCCESS exemption only | `rom.py:336` and `record.py:326` both test status before permitting shared-entry echo. A command whose response rule itself specifies echo continues to follow that rule. Independent numeric and symbolic SUCCESS probes fail; existing non-SUCCESS shared echoes pass. |
| Exact echo-hide plant | `selftest.py:44,60` NOPs EAVL's three body fields and appends EAVL to `echo_entries`. The independent file-copy reproduction fails with `schema: echo_entries: EAVL ... nor listed in shared_entries` (`echo-hide-gate.log`). |
| Explicit sharing and re-recording cannot hide SUCCESS drift | `plants.py:62,149` adds ROM, numeric-observation and symbolic-observation controls. Independently declaring EAVL shared, generating its shortened ROM and sweeping the engine yields a named ENTITY_AVAILABLE SUCCESS failure. Re-recording still fails; the fresh gate reports both `decode:` and `rom:` size failures (`echo-shared-rerecord.log`, `echo-shared-fresh-gate.log`). |
| Held registry and regenerated references | `aecp_fields.json:694` names consumer/check/probe. There are 62 fields: 30 held within their scope and 32 held to nothing. The docstring, 09 §8.10 and REQ-VER-002 Arch match the registry. F06.14 and those three references are byte-identical after regeneration. The actual published PR field reference passes. |
| Standing tests protect the guards | Normal and optimized self-tests each catch 231/231 defects, including all 30 held-field mutations. Independently disabling membership classification, ROM SUCCESS restriction and observed SUCCESS restriction separately makes the self-test fail by the intended name (`guard-disabled-*.log`). |

Reviewer execution used focused checks and disposable trees under `scratch/`. Independent campaigns ran concurrently under foreground supervisors, with every child waited for. The scoped simulator identified itself as version 5.050 before use. The build used `make -j16`, with compilation limited to 12 workers alongside lightweight checks. No full processor/parent/gPTP/synthesis/builder bank, hardware run, shared install or container CI run was performed.

| Reviewer check | Result | Receipt |
|---|---|---|
| Clean gate and actual PR reference | 31 commands, 84 entries, 41 generated rows; rc 0 | `receipts/gate-pr-reference.log` |
| Normal and optimized self-tests | 231/231 named plants in each mode | `receipts/gate-selftest.log`, `gate-optimized.log` |
| Independent boundaries | 14 PASS, 0 FAIL | `receipts/independent-echo-probes.log` |
| Focused engine suite | 585,760 trials; zero timeouts; 176 PASS, 0 FAIL | `receipts/suite-baseline.log`, `observed-baseline.json` |
| Shortened shared EAVL sweep | 585,760 trials; zero timeouts; observed, re-record and fresh-gate verdicts fail by command name | `receipts/echo-shared-*.log`, `observed-echo-shared.json` |
| Regeneration | Four generated references unchanged byte for byte | `receipts/regeneration-identity.txt` |
| Focused documentation checks | Links, requirement/module matrices, parameters, IDs and figures pass | `receipts/focused-doc-checks.log` |
| Production source and ROMs | Production HDL unchanged; both ROMs identical at original base, round-3 head and exact head | `receipts/production-rtl-identity.txt`, `rom-identity.json` |
| Python delta structure | Seven touched modules, 100 functions; no inspected length/signature/documentation violations | `receipts/python-delta-structure.json` |
| Final preservation | 610 tracked entries, working bytes/modes and index match; clean detached exact head/tree; zero required gitlinks | `receipts/integrity-after.json` |

`receipts/validation-summary.json` records 23 execution receipts matching expected return codes, including intentionally failing mutations. Two initial reviewer setup assertions were corrected and only the affected campaigns repeated: membership disabling initially also removed shape validation, and the production-source query initially included the testbench wrapper. Details are in `receipts/execution-notes.txt`; neither was treated as a source defect. The Python structure check is a focused approximation, not the parent's budget gate.

ROM SHA256 values at all three revisions:

- `ucode.hex`, 26,624 bytes: `518b900c4a5650902c3ea9125941e434857ba2f379b6c92268a67fef459d37f8`.
- `ltn_rom.hex`, 6,138 bytes: `23cc67eeadc7ecad8c9ceb7f9391095b64ada44d4e0f3a232ce82a2a69e7e956`.

Prior findings were read after the independent verdict and ledger, including [R608-3](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/pull/174#issuecomment-6112257211) and [R609-3](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/pull/174#issuecomment-6112326328). These dispositions apply at the exact head; earlier broad execution is attributed to its covering round, not presented as a round-4 rerun.

| Prior ID | Disposition at 4029dc5d |
|---|---|
| R608-3-F1 — MINOR; Robustness, Tests, Docs | **RESOLVED.** Membership and non-SUCCESS requirements are implemented. Exact echo-hide and stronger explicit-sharing/post-record probes fail by name. The registry's held claim and generated references match enforcement. |
| R608-1-F1 — decode/dispatch | **RESOLVED; unchanged from R609-3.** Behavioral observation and q1/q2 standing controls remain intact. Fresh focused observations and input digests pass. No source-text decode inference was substituted. |
| R609-1-F1 — response/command sizes | **RESOLVED within disclosed scope; unchanged from R609-3.** Fixed/variable/stub checks, floors and standing size controls remain. Current self-test passes; the delta strengthens SUCCESS-size enforcement. ACQUIRE_ENTITY and REGISTER_UNSOLICITED_NOTIFICATION retain the disclosed command-cdl/echo-only limit. |
| R608-1-F2 — real-file generator inputs | **RESOLVED; unchanged.** File-copy and generator-alone plants execute in the current self-test. |
| R608-1-F4 / R609-1-F2 — ROM prerequisites | **RESOLVED; unchanged.** All three generator-using suite rules retain the command-table prerequisite. |
| R608-1-F3 / R609-1-F3 — doubled plurals | **RESOLVED; unchanged.** Stored plural units render directly; regenerated F06.14 is identical and passes. |
| R608-2-F1 — echo per | **RESOLVED; unchanged.** Exact accepted-offset gcd and half-record/multiple-record controls remain; the held-field drift is caught. |
| R608-2-F2 — status/oversize exemptions | **RESOLVED by the authorized declaration option; unchanged.** Common status, engine status and oversize remain explicitly held to nothing, with conditional status claims. |
| R608-2-F3 — generator refusals | **RESOLVED; unchanged.** Identity/entries and MVU opcode validation remain; normal and optimized self-tests pass. |
| R609-2-F1 — documented GDI semantics | **RESOLVED; unchanged.** Opcode, optional rtl and optional gdi remain semantic; identity/rendering fields are distinguished. Standing semantic drifts are caught. |
| R609-1-S1; R609-1-S2 | **RESOLVED.** Fixed status-code authority and named documented-row validation remain protected. |
| R608-1-S2 / R609-1-S3 | **RESOLVED.** Explicit generator refusals survive optimization. |
| R608-1-S1 / R609-1-S4 | **RESOLVED.** Export reference and semantic GDI correction remain current. |
| R608-2-S2 — undigested inputs | **RESOLVED; unchanged.** Descriptor validators and shared harness remain in the swept-input digest inventory. |
| R608-2-R1 / R609-2-R1; R608-3-R1 / R609-3-R1 | Quoted wording is **corrected in the current PR body**. The ruling's historical residue transfer to parent #495 remains a manager duty below. |
| R608-3-S1; R608-2-S1 / R608-3-S2; R608-2-S3 / R608-3-S3 | **RETAINED**, verdict-neutral, detailed below. |
| Manager Python-rule addendum | **Resolution unchanged.** Focused delta structure is clean; published author parent-budget receipts pass. Final candidate validation remains the manager's. |

Retained observations have no unclean lens:

- **R608-3-S1 — SUGGESTION — Tests, Robustness.** Artifact: `tb/aecp_cmds/sim_main.cpp:306`, unchanged count-one lengths `{24,28}`. Authority/evidence: public R608-3 count1-overlength finding and unchanged bounded stimulus. Impact: count-one acceptance above its records is outside the observer's semantic guarantee after re-recording. Optional required outcome: retain count-one cdl 36 as well as 24/28. Verification: an overlength-acceptance mutation fails by command name after re-recording. This round does not claim that coverage.
- **R608-2-S1 / R608-3-S2 — SUGGESTION — Tests, Robustness.** Artifact: `tb/aecp_cmds/sim_main.cpp:397`. Authority/evidence: prior public MVU-byte probe and unchanged skipped wrong-byte cases. Impact: wrong protocol-ID bytes at @22 and @24 are unswept. Optional required outcome: flip every protocol-ID byte independently. Verification: a weakened comparison fails semantically after re-recording, beyond the digest check.
- **R608-2-S3 / R608-3-S3 — SUGGESTION — Tests, Docs.** Artifacts: `tb/aecp_cmds/aecp_cmds_wrap.sv:164,256`, stimulus templates and 09 §8.10. Authority/evidence: lock-held/deadline inputs remain tied low; the sweep omits a bound-only running split and nonzero descriptor index. Impact: these outcomes remain outside its guarantees. Optional required outcome: name the examples in the limits or add stimuli. Verification: documentation matches the stimulus, or named controls demonstrate each added outcome.
- **R608-3-R1 / R609-3-R1 — RESIDUE — Docs; historical manager carry only.** Artifact: earlier published PR-body quotations in those public findings. Authority: round-4 ruling assigns R1 to parent #495 at merge. Impact: publication-status prose only; no measurement, generated artifact, test, verdict or conformance claim changes. Exact historical fix: replace “The round-3 measurements below are local; its new commits have not been pushed.” with “The round-3 measurements below were run locally at the stated commits.” Delete the separate sentence “The new commits have not been pushed.” Verification: the current PR body already has the corrected wording; the manager records archival disposition in #495. No GitHub text was edited by this review.

Public execution evidence comes from the immutable [published packet](https://github.com/kebag-logic/milan-fpga/tree/0cc8f8f5c9d3d6318f864d76c5a662f06b6eb689/review-evidence/pp73-r1). Seventy-three selected author receipts were fetched and verified against immutable Git blob IDs (`receipts/public-author-selected.json`). Final identity and final export receipts bind 610 source blobs to `4029dc5d`; earlier bookkeeping SHA files are not substituted for that identity. Author receipts report five source gates passing, original suite records unchanged, nine existing campaign pairs unchanged under stated normalization, 16 command controls plus golden/restored records matching, and byte-identical converted production source and engine elaboration. Those wider banks and elaboration were **not rerun by this reviewer**. Selected raw receipts are under `receipts/public-author-r4/`.

The exact-head [hosted push run](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/actions/runs/38178399598) has executed, successful documentation and portability jobs. The documentation log includes 231/231 plants and the clean command gate. At inspection, suites was still in progress; its simulator-build step was skipped after cache use, and subsequent campaign steps had no passing conclusion. No exact-head pull_request execution was established in the queried snapshot; the older pull_request run is not evidence for this source head. A hosted pull_request run tests the processor merge context. This detached source does **not** contain processor main `6d536868ee2a4762ab307d5ed51ff09c01130942`, confirmed by ancestry rc 1. Hosted acceptance remains the manager's.

The reviewer-owned ledger is:

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Frozen acceptance and round-4 ruling; REQ-VER-002/GAP-11; membership classification; status boundary; field registry/export scope | R609-4 delta; R609-3 scope retained | 4029dc5de2a0a540d6a015c747319fbee7abba2e |
| RTL | CLEAN | Unchanged production HDL; three-revision ROM identity; observer dispatch/response path; fresh 585760-trial suite; shortened-ROM sweep | R609-4 delta; R609-3 scope retained | 4029dc5de2a0a540d6a015c747319fbee7abba2e |
| Robustness | CLEAN | Private/unknown/shared membership probes; numeric/symbolic SUCCESS checks; three disabled guards; refusal after re-recording | R609-4 | 4029dc5de2a0a540d6a015c747319fbee7abba2e |
| Tests | CLEAN | 231 plants in normal/optimized modes; 30 held-field drifts; echo-hide file plant; observer/raw records; CI wiring | R609-4 delta; R609-3 broader controls retained | 4029dc5de2a0a540d6a015c747319fbee7abba2e |
| Docs | CLEAN | docs/README; 06 generated table; 09 sections 7/8.10; compliance Arch; generated docstring; actual PR reference; limits | R609-4 | 4029dc5de2a0a540d6a015c747319fbee7abba2e |

Real limits remain: the observer's opcode range ends at 0x007F and its length sweep at cdl 100; unswept outcomes and GDI ceilings are not proven. Common/engine status and oversize exemptions remain declared. Shared-entry explanations are not behavior proofs. ROM walking holds sizes/statuses/lock/notification, not field values or order. Golden-model generation, stimulus generation, ACMP transition/timing generation and parent firmware consumption remain outside the frozen delivery. Physical calibration **NOT RUN**; field skips are not hardware proof.

No manager source bank runs at this exact head, and none is claimed or inferred. Source validation is distinct from the final current-dev merge candidate: original source base `2cbed0a987c1e68402658d69459ab7e5aa571adc`, assigned live parent dev `09c7231eca343607c97c0d66abebb2553688712c`. At the merge turn the manager builds that candidate, validates builder/native banks and applicable parent evidence-reader/style dispositions, verifies gitlinks and processor-main integration, and links receipts on the PR. The manager also owns hosted/act acceptance, the independent-review completion bar, #495 residue disposition, the parent export-consumer follow-up and publication.

The clone was never mutated by a probe. Final tracked bytes, modes and index match the exact assigned tree; this processor repository contains no submodule gitlinks. That does not substitute for the parent's candidate gitlink check. No source fix, commit, push, GitHub write, merge, author contact, delegation, privileged action or hardware access occurred. Portable scripts and raw receipts are listed by packet-relative SHA256 in `MANIFEST.sha256`; `scratch/` is disposable and excluded. Only listed files and this report are publication material.

R609-4 FINISHED
