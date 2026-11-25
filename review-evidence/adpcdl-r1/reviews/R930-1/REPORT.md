[R930] NEGATIVE - exact head e0b144904e57c96928f1dd3fca36a00df42f6ed3

Two open MINOR findings prevent approval. The production comparison implements the frozen scope, and no production-code failure was found. The findings concern a regression-test boundary and the published evidence's privacy.

Scope and independence

Reviewed issue [#37](https://github.com/kebag-logic/tsn-c-stack/issues/37), PR [#38](https://github.com/kebag-logic/tsn-c-stack/pull/38), head e0b144904e57c96928f1dd3fca36a00df42f6ed3, tree 2b5890f3cbb82b2415f7fa50151db3acc550e282, against base 69bac7cd52815d2ae223a5a3aa6d022a1f1d35de. History contains one commit and ten changed files. The supplied repository instructions, CONTRIBUTING.md, README.md, architecture, port contract, requirements and verification guidance were read before the independent diff pass. There is no tracked AGENTS.md or docs/README in this source tree.

The issue body freezes rejection/counting below 56, acceptance from 56 upward using the existing prefix, the unchanged 82-byte minimum and unchanged transmit value. No issue comments supplied additional scope. The two public PR comments examined are review-start notices. The independent verdict and ledger were written before checking prior review submissions. No prior public FINDINGS or submitted reviews were found; there are none to resolve or retain in this round. No other reviewer report or private author material was consulted. The author packet was read only at its published commit.

Findings

F1 — MINOR — Tests, Robustness

- Artifact: tests/test_adp.cpp:820–825, AcceptsLongControlDataLength.
- Authority/evidence: issue #37 acceptance criterion 1 requires the longer lengths with surplus present and absent; docs/PORTING.md:129 gives the readable-buffer contract. The test allocates 26 + declared_length bytes, then reuses that allocation for both length 82 and full-length calls. Thus the first surplus byte remains readable in both calls.
- Impact: a read beyond the supplied 82-byte boundary escapes the new regression even with memory instrumentation. A disposable control that reads frame[82] only when control_data_length exceeds 56 passes all 44 existing ADP tests. The independent guarded-buffer test detects that same control at the injected read. This is a test weakness, not an observed overread in the submitted production code.
- Required outcome: make the absent-surplus arm use an actual 82-byte allocation, independently of the longer allocation, preserving all lengths, targets, receive configurations and valid_time cases. Retain a boundary-sensitive check under memory instrumentation.
- Verification: run_boundary.py and boundary_probe.cpp reproduce the evidence. physical-boundary.log records the unchanged head passing 61,440 cases: all 2,048 field values, five configurations, two valid_time settings and three targets. overread-existing-suite.log records 44 passing tests for the faulty copy; overread-physical-boundary.log records the expected failure. The injected read is recorded in overread-control.diff. Its failure is a sensitivity probe, not one of the six registered named-assertion catches. Recheck that the strengthened suite detects this control and the unchanged core passes.

F2 — MINOR — Docs

- Artifacts: [author/HANDOFF.md:27](https://github.com/kebag-logic/milan-fpga/blob/f10f0bd446909328a5996e2f1ee6794a3b70c43b/review-evidence/adpcdl-r1/author/HANDOFF.md#L27) and [author/REVIEW-READY.md:3](https://github.com/kebag-logic/milan-fpga/blob/f10f0bd446909328a5996e2f1ee6794a3b70c43b/review-evidence/adpcdl-r1/author/REVIEW-READY.md#L3).
- Authority/evidence: tsn-c-stack CONTRIBUTING.md excludes host locations from public documents; the review's public-safe rule and the parent contribution guide require publication hygiene. Both published documents contain concrete local work locations. public-location-audit.json identifies the blobs and lines without repeating the locations.
- Impact: the public review packet discloses local workspace information unrelated to reproducing its evidence. This touches privacy and cannot be classified as wording RESIDUE.
- Required outcome: replace the HANDOFF location-bearing sentence with “The source checkout, consumer probe and disposable build outputs are local artifacts; published receipts are in receipts/.” Remove the absolute checkout-location phrase from REVIEW-READY, retaining the branch, base and head identifiers. Have the manager handle the already-published copies under the publication policy.
- Verification: inspect the corrected public artifacts and run the publication privacy check over the entire packet, including prose, logs and scripts. Preserve usable relative artifact references and exact commit identities.

Conformance evidence

The standards themselves were inspected, not only the PR's paraphrases. Their PDF identities are recorded in standards-identities.json; the standards and extracted text are not republished.

| Authority | Independent check and conclusion |
|---|---|
| [IEEE 1722.1-2021](https://standards.ieee.org/ieee/1722.1/6670/), 6.2.2.6, printed p.49 | The field describes the octets after entity_id and its transmitted value is 56. The PR correctly distinguishes this format value from an explicit receive rejection instruction. |
| Same edition, 6.2.7.1.3, printed p.61 | rcvdDiscover is described by receipt of ENTITY_DISCOVER; this definition adds no control-length condition. |
| [Milan v1.2](https://avnu.org/resource/milan-specification/), 5.6.3.1 and Table 5.50, pp.102–103 | Discovery delivery is selected by zero/local entity_id. The stated clauses do not add a longer-length rejection rule. |
| Same edition, Table 5.51 and 5.6.3.5.4, p.104 | DOWN and DELAY ignore the event; WAITING stops the advertisement timer and starts the normal random delay. |
| [IEEE 1722-2016](https://standards.ieee.org/ieee/1722/5979/), 4.4.5.4, p.28 | The field is an 11-bit payload length, also constrained by the sender's frame MTU. It does not specify a receiver rejection of longer ADP here. The 2047 case is robustness testing, not a claim that such a complete frame is a conforming standard-MTU transmission. |

The broader receive tolerance and defensive minimum are the project's frozen policy. These clauses do not expressly require accepting an extended ADPDU; the PR explicitly acknowledges that limit. No external conformance procedure is used as an authority.

Implementation, receive states and RTL boundary

src/adp.c:311–328 changes only the masked comparison from != to <, plus one clause reference. The 0x07FF mask still excludes valid_time. Short-circuit evaluation checks the actual 82-byte minimum before header reads. Rejections increment discarded once; target rejection, version, EtherType, subtype and message-type checks are unchanged. No length-based copy, allocation or iteration was introduced. The fixed discovery fields remain within the retained prefix. Callback re-entry handling precedes parsing and is unchanged.

The five exercised configurations are disabled DOWN; enabled DOWN with link down; startup DELAY; DELAY with an owed advertisement; and WAITING. Short fields preserve all storage except the counter and invoke no port callbacks. Long discoveries for zero/local entity_id preserve inactive/delaying state; WAITING stops the old timer, draws a normal delay and enters DELAY without immediate transmission. The original short-frame tests still cover every actual size 0–81. Existing re-entry, backpressure, departure and timing tests also pass.

include/adp.h is unchanged: ADP_CONTROL_DATA_LENGTH remains 56 and ADP_FRAME_BYTES remains 82. adp_build still writes those values. No other ADP production path, public layout, callback signature, ACMP implementation or MAAP implementation changes.

The source PR contains no RTL or submodule changes. For the consumer check, the author-tested parent is 5de21ff3661436ea5598718aca36934361e35340; the evidence publication commit f10f0bd446909328a5996e2f1ee6794a3b70c43b is a separate snapshot. Both identities were kept distinct.

At the author-tested parent, hdl/milan/KL_ctrl_split.sv:108–125 classifies using destination, EtherType and subtype; hdl/milan/mailbox/KL_mbx_rx.sv:433–458 classifies before the control-length bytes and imposes its configured capacity at :592. The mailbox contract still limits ADP frames to 128 bytes. Thus complete 57/84/102-length cases fit; longer complete frames can be dropped upstream even though the portable core accepts their readable prefix. This pre-existing transport bound is outside #37.

The parent's protocol-processor pin is 801ef2283ec793e35a2590fc6593c90313a64041. Its hdl/packet_engine/KL_pp_rx_validator.sv:263,295–296 separately requires the declared payload plus 12 bytes. That all-fabric path remains distinct from the split mailbox path and is not proven by the portable-core change. No RTL simulation or hardware result is claimed.

Consumer patch

The published parent-consumer.patch passes a clean application check against its stated 5de21ff3 parent, without offsets; see consumer-patch-check.log. Its two files replace rejection of 57/2047 with the short-field checks, preserve valid_time masking coverage, add mailbox acceptance for 57/84/102 with short/full reported frame sizes, and update the changed comparison anchors and named assertion targets. The exact-56 case still has a refusing plant. The patch changes tests and defects only; it must accompany the later pin bump.

The published unmodified-consumer failure is the expected obsolete exact-length expectation. The published patched consumer arms pass. consumer-plants.log is not a green complete campaign: its selected eleven defects are caught, but the reported exit 1 also reflects 141 tests not named by that subset. The packet labels that limitation. The manager must reconcile against the actual pin-bump candidate and its full registration.

Tests, coverage and documents

Independent foreground orchestration ran three campaigns concurrently with at most fifteen worker jobs; all disposable builds and fault copies stayed under scratch/. The tracked source was never edited.

| Local check | Result and receipt |
|---|---|
| Host build and all ten registered suites | PASS; host.log, host.rc |
| Instrumented build and all ten registered suites | PASS; sanitizers.log, sanitizers.rc |
| Six registered length defects | 6 CAUGHT, 0 ESCAPED, 0 ERROR; six-plants.log and six-plants-results.json |
| Physical buffer boundary | 61,440 cases PASS on the exact core; physical-boundary.log |
| Extra faulty-copy sensitivity | Existing 44 tests PASS; protected boundary FAIL as expected; overread-*.log |
| Coverage | 100% lines/branches after unchanged exclusions; host.log |
| Traceability and generated test inventory | PASS; 186 declarations, 464 registered instances, 484 plants; host.log |
| Consumer patch application | PASS against stated parent; consumer-patch-check.log |

The six defects separately remove the minimum check, lower it to 55, include valid_time in the comparison, restore equality, require the surplus in the buffer, and reject 56. Each is caught in all five registered state instances by its specified assertion. Counts are consistent: one prior plant removed, six added; 480 core plus four configuration plants. Only the focused six were rerun here.

Coverage is not overstated: raw ADP coverage is 205/207 lines and 97/104 branches; the inherited unreachable-state exclusions yield 100%, and none excludes adp_rx. The published adp_rx receipt executes every receive line and both outcomes of the changed comparison (1120 rejections, 157 continuations). The ratchet and exclusion register are unchanged.

All changed prose and JSON were examined. ADP-01, PORTING, REQUIREMENTS, CHANGELOG, TESTS, TRACEABILITY and the documented plant count agree with the change. The generated-document gates pass. New source/test trace comments introduce no bench labels, lane names, review rounds, reviewer IDs or issue-comment IDs. The new citations are to standards. F2 remains the publication defect.

The author's exact-head source receipts report all 28 Linux steps green, 484/484 plants caught, and Debug/Release RV32 checks green. Those are author source receipts, not a manager source bank. The exact-head hosted [run 45677945438](https://github.com/kebag-logic/tsn-c-stack/actions/runs/45677945438) reports completed successful quality and bare-metal jobs, including executed validation steps; neither is a skipped context. public-status.json records the inspected metadata. Hosted/replica acceptance remains manager-owned.

Reviewer-owned ledger

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Standards above; issue #37; ADP-01; adp_rx and transmit encoding | R930-1 | e0b144904e57c96928f1dd3fca36a00df42f6ed3 |
| RTL | CLEAN | No RTL delta; parent split/mailbox ingress, capacity contract, processor validator, consumer patch | R930-1 | e0b144904e57c96928f1dd3fca36a00df42f6ed3 |
| Robustness | UNCLEAN | Five receive configurations, exact-size short inputs, re-entry/backpressure tests, physical boundary and surviving control; F1 | R930-1 | e0b144904e57c96928f1dd3fca36a00df42f6ed3 |
| Tests | UNCLEAN | Split tests, six defects, full local core suites, coverage, registration, generated tables, author receipts; F1 | R930-1 | e0b144904e57c96928f1dd3fca36a00df42f6ed3 |
| Docs | UNCLEAN | All ten changed files, PR text, requirements/interface authorities, published author packet; F2 | R930-1 | e0b144904e57c96928f1dd3fca36a00df42f6ed3 |

Limits, restoration and pending duties

The review does not replace final current-dev candidate validation. The source base is 69bac7cd52815d2ae223a5a3aa6d022a1f1d35de; the supplied live dev is e275d7950ef3385753e6a15d2e191ba855b171ed. The author's earlier equal-tree trial is not evidence about that final candidate. No manager source bank is claimed.

The manager must publish the review, resolve and re-review the open findings, obtain the required independent approvals, validate the final candidate including builder/native banks, link its receipts on the PR, reconcile the consumer patch with the later pin bump, and own hosted/replica acceptance and merge containment. None of those actions was performed here.

No full parent, processor, timing, synthesis or builder banks were run. No shared installation, hardware operation, remote write, source fix, commit, push or merge was performed. Physical calibration NOT RUN. Field skips and host execution are not hardware proof.

integrity-before.json and integrity-after.json verify all 100 tracked blobs byte-for-byte, their executable modes, the index tree, clean status, and the exact supplied head/tree. This source repository has no gitlinks. Public parent gitlinks were recorded separately; no parent checkout or submodule was modified. MANIFEST.sha256 enumerates the publishable receipts and scripts. scratch/ is excluded from publication.

R930-1 FINISHED
