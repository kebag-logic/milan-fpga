[R589] POSITIVE - exact head 5c6f50eefa4c5545f052ec843363ace5e7936e8a

Independent pass R589-1, issue #708 / PR #754. Tree d4b0e17fdf530ddb2ca8ec8c3986bcc4a9189254, reviewed against source base 734eb780dc93896a5961cd95180f79475a401650. All five lenses have been applied. No open BLOCKER, MAJOR or MINOR found. One wording-only RESIDUE is recorded below. This verdict covers the source adoption, not merge authorization or hardware qualification.

[R589] PASS Conformance - sw/firmware/ctrl/test/acmp_walk.cpp:432; protocol-processor/hdl/acmp/KL_pp_acmp_listener.sv:679; protocol-processor/hdl/acmp/KL_acmp_talker.sv:1301 - compared the corrected fields directly with Milan v1.2 Table 5.36, 5.5.3.5.30 step 2, 5.5.4.2 step 1 and Table 5.44, and IEEE 1722.1-2021 8.2.1.5/Table 8-3. Successful UNBIND clears both talker identifiers, discovered retry retains status, lock refusal is 16, and invalid DISCONNECT source is TALKER_UNKNOWN_ID. The overview in 5.5.2.7 defers to the detailed procedure. The actual standards were read; processor expectations were not treated as their authority.

[R589] PASS RTL - protocol-processor/hdl/top/protocol_processor_top.sv:1037, :3532, :4449; hdl/milan/KL_pp_shadow.sv:1079; protocol-processor/hdl/aecp/KL_aecp_notify.sv:774; protocol-processor/hdl/packet_engine/KL_pp_tx_arbiter.sv:161 - reviewed the six changed processor RTL files and their parent bindings. The parent keeps one-interface defaults, retains its 12-bit VID face while internal wire/state fields retain 16 bits, and introduces no new parent clock, reset or CDC boundary. The registered withdraw mask resets to zero and is used consistently by queue removal and pre-start abort. Parallel arbiter ranking retains priority and lowest-index tie handling. Saved-name adoption adds tests/docs, not a further RTL delta. Focused listener, talker, arbiter and notification executions passed.

[R589] PASS Robustness - protocol-processor/tb/acmp_listener/field_cases.hpp:41; protocol-processor/tb/aecp_notify/Makefile:69; sw/firmware/ctrl/test/acmp_walk.cpp:432 - exercised full VLAN 0xF123, original-controller acceptance after rebind, new-controller rejection, byte-identical probe retry, lock refusal without binding mutation, invalid-source response, reset, stalls and arbitration cases. Notification SC1/SC2 each exercised both owner orderings for coincident expiry/cancellation and the following failure window; no extra live deregistration occurred. The old-answer control fails LD1, LD2 and LD3. These are bounded simulation results, not a physical/network qualification claim.

[R589] PASS Tests - scripts/measure_test_evidence_readers.py:21; protocol-processor/tb/name_state/mutants.py:68; protocol-processor/tb/name_state/sim_main.cpp:13; sw/firmware/ctrl/test/acmp_walk.cpp:432 - the public parent-name patch applies exactly in reverse. The classified driver plants defects in disposable source copies, requires completed runs and named value failures, and uses fixed semantic inventories rather than deriving expected values from RTL. The changed ACMP walk retains raw bytes and records. Its current model passes 127 tests; the prior-pin model fails ten tests: eight UNBIND states, one discovered-retry state and lock refusal. The focused RTL suites total 4,676 checks with zero failures (3,167 listener; 1,376 talker; 66 arbiter; 67 notification).

[R589] PASS Docs - docs/reference/SUBMODULES.md:188; docs/design/MAILBOX_SPLIT.md:775; docs/findings/234_PP_SHADOW_AREA_BASELINE.md:36; syn/ooc/pp_resource_baseline.json; docs/diagrams/submodule_boundaries.png - checked the public scope rulings, current pin map, clarified single-interface historical AECP reference, raw comparison contract, and resource-record arithmetic. The pin page and boundary generator check pass; the diagram was visually inspected. Port and naming generators reproduce committed bytes, both ROMs reproduce their recorded digests, and resource policy/flow identity is unchanged at every endpoint. The wording-only source-comment residue below does not invalidate this lens under the owner's rule.

ID R589-1-R1; severity RESIDUE; lenses Docs; artifact sw/firmware/ctrl/test/acmp_walk.cpp:64.
Authority/evidence: the newly added comment line ends `first, so it governs (#665, comment 6030067436).` The owner's 2026-10-15 source-comment rule excludes issue-comment IDs. The neighboring paragraph already identifies the normative clauses.
Impact: wording-only process-reference residue. It changes no measurement, figure, verdict, test expression, executable code, generated artifact, conformance statement or clause claim, and discloses no private identity.
Required outcome/exact fix: replace that line with `//        first, so it governs (#665; processor #168).` Retain the surrounding clause citations.
Verification: inspect the added source-comment delta for forbidden process identifiers; no behavior change or test rerun is needed for this text-only correction.

Reviewer-owned completion ledger:

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Issue #708 frozen acceptance and rulings; cited Milan/IEEE clauses; acmp_walk.cpp; processor listener/talker/package | R589-1 | 5c6f50eefa4c5545f052ec843363ace5e7936e8a |
| RTL | CLEAN | Six-file processor RTL delta; KL_pp_shadow.sv bindings; three resource records and published input manifests | R589-1 | 5c6f50eefa4c5545f052ec843363ace5e7936e8a |
| Robustness | CLEAN | field_cases.hpp; listener/talker/arbiter suites; notification SC1/SC2; old-answer control | R589-1 | 5c6f50eefa4c5545f052ec843363ace5e7936e8a |
| Tests | CLEAN | acmp_walk.cpp and raw control logs; parent-name patch; name_state fixture/oracle/mutant classifier | R589-1 | 5c6f50eefa4c5545f052ec843363ace5e7936e8a |
| Docs | CLEAN | SUBMODULES; MAILBOX_SPLIT; firmware READMEs; area baseline/budget/plan; generated diagram and records | R589-1 | 5c6f50eefa4c5545f052ec843363ace5e7936e8a |

Independent verdict and ledger were written before consulting another review report. Prior-public-finding reconciliation and final integrity receipts follow in the completed report.
