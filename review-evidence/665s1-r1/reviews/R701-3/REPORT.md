[R701] NEGATIVE - exact head 44d95625bde2c46d7070c090fc29ed0ba85ab64a

Independent internal review, R701-3, issue #665 / PR #795. Tree: `2b5b52bb8d0c1b43d8ce9ef24684d3a5374acde3`. Source base: `e76a755a`. All five lenses were independently applied. This is a source review, not merge acceptance.

The firmware acknowledges successful state changes when their face publication is still owed. That violates the frozen write/apply-before-response requirement. The verification summary also reports superseded test measurements. These leave this head unclean.

## Findings

### F1 — MAJOR — Conformance, RTL, Robustness, Tests, Docs

**Artifact:** `sw/firmware/ctrl/aecp/aecp_face.c:75` (`publish`, especially lines 77-79 and 95-100); `sw/firmware/ctrl/test/test_aecp.cpp:1966`; `docs/design/MAILBOX_SPLIT.md:1230`.

**Authority/evidence:** Frozen assignment item 3 and the manager's commit-acknowledgement ruling; `docs/ARCHITECTURE_HW_SW_SPLIT.md:55` explicitly requires state-apply acknowledgements before responses promising that state (Milan v1.2 5.4.5.2; IEEE 1722.1-2021 7.5.2). `mailbox.yaml:445` repeats that promise. `publish` returns without writing anything when an interface is busy or owed. On commit timeout it sets `owed` and returns through a void `changed` callback; neither case prevents the command's SUCCESS response. The existing `Face.ALateCommitIsOwedAndPublishedAgainWhole` test sends IDENTIFY=255 without acknowledgement, then IDENTIFY=0 while the first commit remains held. Both `receive` calls require SUCCESS, while the test explicitly requires no second commit. The second promised value was not even written. The initial response also lacks the required acknowledgement. `ctrl_app_open_aecp` similarly opens AECP after an unacknowledged initial publication.

**Impact:** A controller can receive SUCCESS while the datapath still holds the preceding setting. Retrying in the application's poll does not repair ordering already broken on the wire. The same publisher serves settings, formats, lock state and restore publication. The current timeout test endorses this failure instead of detecting it; the documentation's unconditional ordering claim is false on this supported failure path. The RTL lens is attributable through its architecture/interface-contract remit: the end-to-end apply-acknowledgement contract is broken even though the mailbox's hold/refusal logic itself behaves as specified.

**Required outcome:** Propagate or retain the pending apply outcome so no successful response or dependent notification promises an unapplied value. Preserve bounded service and recovery, and keep AECP closed until the initial publication is acknowledged. Define and test the bounded failure outcome without silently relaxing the frozen acceptance criterion. Update the timeout documentation and tests accordingly.

**Verification:** `receipts/response-order-probe.txt` reproduces this at the reviewed head: the added assertion sees 255, expects 0, and the named timeout test fails. The five application-face tests in the same run pass. The unmodified nine Face tests pass (`receipts/face-tests.txt`). Reproduce by applying `scripts/response_probe.py` to a disposable copy and running the named timeout test. Add regressions for an absent acknowledgement, a second command while owed, partial acknowledgement at two interfaces, and opening while the initial commit is unacknowledged. Re-run the relevant firmware mutation and coverage gates. The normal acknowledged path and lock-expiry ordering already have useful checks.

### F2 — MINOR — Docs

**Artifact:** `docs/design/MAILBOX_SPLIT.md:1264`, `:1265`, `:1271`.

**Authority/evidence:** The changed census and bench are dependencies of these verification rows. The census row still claims 118 plants and 31 rules, whereas this head has 138 arms and 43 rules. The bench row still claims 402 checks per adapter and 404 at two interfaces; published executed results are 523/568 and 530/575. The model row still claims 389 checks against 402, whereas the two-interface model now runs 488. The new face tests and twelve census rules are absent from this summary even though nearby new prose describes them.

**Impact:** A cold reviewer gets contradictory numerical evidence for the same head. These are test measurements, so this is not wording-only RESIDUE under the owner's rule.

**Required outcome:** Bring all affected verification rows into agreement with the actual controls and their scope, or remove volatile counts and link to the exact runnable evidence. Distinguish common adapter checks from additional adapter-specific checks.

**Verification:** Compare the revised rows with the census and mailbox receipts; run the documentation gates.

### W1 — RESIDUE — Docs

**Artifacts:** New source comments/docstrings at `hdl/milan/mailbox/KL_mbx_evt.sv:19`; `sw/firmware/ctrl/aecp/aecp.h:71`; `sw/firmware/ctrl/aecp/aecp_face.h:3`; `sw/firmware/ctrl/app/ctrl_app_aecp.h:39`; `sw/firmware/ctrl/mbx/mbx.h:125`; `sw/firmware/ctrl/test/aecp_mutants.py:469`; `sw/firmware/ctrl/test/test_aecp.cpp:1718`; `sw/litex/ctrl_memory.py:24`; `sw/litex/milan_soc.py:2687`; `sw/mailbox/census_plants.py:564`; `sw/mailbox/census_ports.py:6`, `:10`, `:15`, `:53`; `sw/mailbox/census_selftest.py:20`; `sw/mailbox/mailbox.yaml:63`, `:430`, `:815`; `sw/mailbox/mailbox_face.py:5`; `sw/mailbox/publication_census.py:112`; `tb/verilator/mbx/mutants.py:481`; `tb/verilator/mbx/suite.hpp:100`; `tb/verilator/mbx/suite_face.hpp:5`.

**Authority/evidence:** The owner's source-comment rule forbids issue-comment IDs in newly added source commentary. These comments introduce assignment/ruling/comment IDs such as `6409739310` and `6410169666`. The new comment headings in `tb/verilator/mbx/suite_face.hpp:217`, `:240`, `:334`, `:402`, `:476`, `:538`, `:586`, `:656` also prefix their behaviour descriptions with test-row labels F1 through F10; line 706 refers to T0.

**Impact:** Wording hygiene only; no change to the described behaviour, requirements or measured results is requested.

**Exact fix:** Remove the numeric assignment/ruling/comment references from those comments, retaining issue IDs (`#665`, `#637`), contract 2.3, applicable standards clauses, and the actual behaviour/reason. Remove the F-number prefixes from the listed comment headings; replace “T0 has failed” with “the request-open assertion has failed”. Leave executable diagnostic labels unchanged. In the census explanation replace the opening ruling reference with “The split placement removes the whole wrapper (#665)” and retain the named exclusion and its acceptance item. Preserve earlier unchanged comments under their existing tracking issue. This finding does not clear or dirty a lens.

## Reviewer-owned coverage ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts and result | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN | Issue assignment and three scope rulings; REQUIREMENTS; split architecture; YAML 2.3; census classification; firmware face and app publisher. F1 violates apply-before-response. | R701-3 | 44d95625bde2c46d7070c090fc29ed0ba85ab64a |
| RTL | UNCLEAN | `mailbox_face.py` generated decode/storage/commit/windows, `KL_mbx.sv`, `KL_mbx_evt.sv`, generated package, `ctrl_mailbox_face_ports`; held requests and settings, tags, timeout, reset, coalesced pending events, both adapters. No new live clock crossing is connected. F1 breaks the architecture's end-to-end apply-acknowledgement contract. | R701-3 | 44d95625bde2c46d7070c090fc29ed0ba85ab64a |
| Robustness | UNCLEAN | Census unmapped/G-wire plants; window wrong tags, timeouts, partial strobes and event coalescing; planner override refusals; firmware held commit. F1 remains on the missing-acknowledgement path. | R701-3 | 44d95625bde2c46d7070c090fc29ed0ba85ab64a |
| Tests | UNCLEAN | Census plants and rule-removal implementation; mailbox positive controls and mutation campaign; `test_aecp.cpp` and firmware mutants; branch ratchet and published gate receipts. F1's timeout test requires the wrong outcome. | R701-3 | 44d95625bde2c46d7070c090fc29ed0ba85ab64a |
| Docs | UNCLEAN | `MAILBOX_SPLIT.md`, `MAILBOX_CONTRACT.md`, `SPLIT_CONTROL_MEMORY.md`, architecture changes, public task/PR and executable receipts. F1's ordering claim and F2's stale measurements remain; W1 is wording-only. | R701-3 | 44d95625bde2c46d7070c090fc29ed0ba85ab64a |

RTL sub-check evidence: `sw/mailbox/mailbox_face.py:310`, `hdl/milan/mailbox/KL_mbx_evt.sv:321`, `sw/litex/milan_soc.py:2645` — inspected held payload qualifiers, reset, matching-tag acceptance, bounded window waits, simultaneous post/change preservation, and idle unconnected integration against contract 2.3. These checks found no separate HDL defect; they do not bank the architecture lens while F1 is open. Actual sys-to-datapath crossing and physical operation remain placement-switch acceptance, not demonstrated here.

## Evidence and limits

### Scope reconstruction and prior findings

Read the repository operating contract, CONTRIBUTING and documentation map, then the issue's frozen assignment and public decisions, linked requirements/interfaces, source diff and history, and finally executable evidence. The assignment is issue comment 6409739310; controlling clarifications are 6410169666 (G terminals and map-writer exclusion), 6410301079 (supported all-fabric placement), and 6412739248 (one named 57-tile exception). The implementation is fifteen commits from `e76a755a`. No previously reviewed implementation head or prior clean ledger was available to inherit on this PR, so the whole source delta was independently examined, with generated artifacts examined through their generator and crosschecks.

The verdict and ledger were written before checking prior public review bodies. The fetched PR state contains two public review-start comments, zero reviews and zero inline comments; there is no prior reviewer finding body on PR #795 to resolve or retain (`receipts/prior-findings.txt`). The author's three recorded gate discoveries were checked at their causes: unknown event types no longer enter the counted-event decoder (`mbx.c`); the face timing bench bounds a request that never opens (`suite_face.hpp`); and the port census is in the stack boundary's non-compiling input list (`ctrl_configs.py`). None is being treated as a prior positive review.

### Executed and inspected evidence

The public evidence tree is [50eb576c, review-evidence/665s1-r1](https://github.com/kebag-logic/milan-fpga/tree/50eb576c296d80307eac7c3064129440642d823d/review-evidence/665s1-r1). All 301 manifest entries match their published SHA-256 values. The supplied evidence commit reports signature status `N`, and no detached signature/key was supplied: this verifies content integrity, not signer authentication. No private author handoff or another reviewer's report was used to derive the verdict.

| Check | Evidence and result |
|---|---|
| Every port, every shape | The independent census check passes all six shapes: 217 ports, C=25, F=28, R=34, E=6, M=14, G=110. G ends: seven CSR inputs, twenty memory outputs, four shim inputs, no wire end; 27 excluded map-writer nets. `census_ports.py` names the amr exclusion, follows only ruled terminals, and records the placement switch's obligation to remove the exclusion and pass without it. |
| Independent source plants | `scripts/census_probes.py` adds an unclassified wrapper output, then routes the G debug-time output into `o_mac_tx_en`. Both are refused by their intended rule; `receipts/census-probes.txt`, rc 0. |
| Census self-test | Independent `--check --selftest --jobs 6` passes: 138 arms and all 43 rules proved by removal, rc 0 (`receipts/census.txt`). The separate published receipt reports 992 seconds locally. Local elapsed time is not a hosted-job duration. |
| Additive contract and regeneration | Existing YAML keys/list entries retain their values except version minor 2→3; new fields are additive. `gen_mailbox.py --check --crosscheck --selftest` passes, including the two-interface variant; checked generated RTL/package, C header and reference document. `receipts/generator.txt`, rc 0. |
| Clock-domain contract | The contract requires qualified payloads and approved handshakes; F holds through acknowledgement, all four R windows specify 64-cycle bounds. Current `CtrlMailbox` names outputs and ties incoming face signals idle. It connects no new sys↔milan crossing. Thus no implemented CDC path is being certified; the placement switch must implement and test it. |
| Mailbox positive controls | Completed resumed `make` receipt includes both adapters, co-simulation and two-interface checks. Fresh `make -j16 ... run-if2` passes 530 Wishbone, 575 AXI4-Lite and 488 host-model checks. See `receipts/resumed-mbx.log` and `receipts/mbx-if2.txt`. |
| Mailbox mutations | Independent full campaign catches 199/199, rc 0 (`receipts/mbx-mutants.txt`), matching the published campaign. Field misrouting, early answer, event loss and lost coalesced-state arms each fail their named check through both adapters. |
| Firmware | Fresh unmodified Face tests pass; application-face checks pass alongside the deliberately failing F1 assertion. LOCK_ENTITY and expiry both call `AECP_CHANGE_LOCK`; notification handling reaches Table 5.22 and the core's per-descriptor holdoff. The published exact-head four firmware shards all pass, including 528/528 control mutants and the AECP campaign. Coverage is 100% in 31 ratcheted files, including 144/144 face branches, with no changed exclusion logic/list. Coverage does not cure F1's wrong oracle. |
| Memory exception | Fresh `test_ctrl_memory.py` passes. The independent rerun of the published override probe catches 11/11 defects, including dropping either the shape or interface discriminator, using the override by default, admitting another point, and exceeding 57. `receipts/memory-litex.txt`, `receipts/ledger-mutants.txt`. |
| Image ledger | Public final linked spans plan 37.0, 40.5, 50.0 and 57.0 RAMB36 equivalents. Only the 8x8/two-interface point is one tile over, explicitly owed to S14. The default planner/build still refuses it. Checked the four plan receipts and independently sorted BSS symbols for each point. These are planned figures, not fresh mapped results. The shared runtime lacks stack protection as publicly ruled; target runtime remains separate work. |
| Mailbox area | Published OOC utilization has 5,515 LUT and 7,632 FF, versus 3,585 and 4,114; 1 RAMB36 and 10 RAMB18 remain unchanged. The ledger reports the +1,930 LUT/+3,518 FF honestly. Receipt timing is +0.123 ns at 10 ns for the named recipe. Relevant RTL is unchanged since that measured commit. This is neither whole-image timing nor hardware proof. |
| All-fabric and VERSION | Independently hashed resumed base/head exports: normalized digests match for all five shipped configs, over 3,875 files each excluding the run log. Raw bytes differ in stamps, archive metadata and hierarchy comments; no raw-directory identity is claimed. This follows `MAILBOX_SPLIT.md`'s stated normalization method. Arty exports use the documented 100 MHz substitution because the base also refuses 83.333 MHz. `milan_datapath.sv`, CSR VERSION 0x0002_0060 and `.github/` are unchanged. |
| Broader public gates | Inspected docs-gate, lint, mailbox OOC/elaboration, builder and behave receipts: documentation gates pass; 406 behave scenarios pass. The exact-head four-shard sweep totals 64/64 suites, 2,191,124 checks, zero failures. Four field/freshness skips contribute no checks. The builder's physical calibration arm is explicitly NOT RUN. No prohibited broad bank was rerun here. |

The independent generator and memory test initially encountered local setup errors (unpinned default frontend; system interpreter without the integration package). Corrected-environment receipts are separate from those setup refusals. Three inherited duplicate campaigns from the interrupted session were found still running and terminated; their incomplete logs are not counted as passes. The completed resumed export and mailbox positive-control receipts were retained.

### Integrity, real limits and manager duties

`receipts/checkout-integrity.txt` verifies all 1,448 candidate tracked blobs by raw hash, file modes and index, plus the populated submodules' own tracked bytes/modes/index and exact gitlinks. The optional `external` gitlink remains unpopulated. Probe source changes were confined to disposable trees; the candidate source was not edited. No commits, pushes, GitHub writes or hardware operations were made.

The hosted check snapshot is not an overall acceptance decision. The exact-head publication-census job completed successfully from 13:13:15 to 13:35:21 UTC: 1,326 seconds, or 49.1% of its 45-minute timeout, below the 60%/27-minute limit (`receipts/hosted-snapshot.txt`). This is a measured hosted duration, separate from the 992-second author-local receipt and the contention-affected independent rerun. Skipped physical contexts and field campaigns provide no hardware evidence.

No manager source bank exists at this head, and none is inferred here. The manager owns hosted/local-replica acceptance and, at the merge turn, the current-dev candidate's builder/native validation and receipts. The source base `e76a755a` is distinct from live dev `76de691e5625cc4ea2f9a19def9e07c1183a14ee`. This source review does not validate that merge candidate. Before merge: resolve F1 and F2 and re-review their lenses at the corrected head, obtain the external review, complete exact-head hosted acceptance including the census time budget, validate the current-dev candidate, and perform the required post-merge containment. The placement switch still owes actual crossings and exclusion-free split elaboration; S14 still owes the excess tile before the default flip.

R701-3 FINISHED
