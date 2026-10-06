[R523] POSITIVE - exact head 021b9c1fb966e9a1a4acef6b5233edd3518f32a0

External independent review, round R523-1, issue #665 / PR #685, lane FC.
Tree: `b7c103aaffff9a48f7c05436372875c5d94331c7`.
Reviewed delta: `6714181d0c8a16e2983f85b724f4d688f5111835..021b9c1fb966e9a1a4acef6b5233edd3518f32a0` (35 files, six commits).
All five lenses were applied independently. No BLOCKER, MAJOR or MINOR finding remains from this review. One prose-only RESIDUE is recorded below. This is source review approval, not approval of a current-dev merge candidate or physical release.

The contract was reconstructed from AGENTS.md, CONTRIBUTING.md, docs/README.md, [issue #665](https://github.com/kebag-logic/milan-fpga/issues/665), the [frozen FC assignment](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6021509373), the [owner decision](https://github.com/kebag-logic/milan-fpga/issues/664#issuecomment-6014311316) and [approval](https://github.com/kebag-logic/milan-fpga/issues/664#issuecomment-6015500032), then REQUIREMENTS.md:58 and FR_NFR.md:322, :328, :403, :413. The mailbox design and generated interface were read before the implementation evidence. The independent diff pass preceded the published handoff and any PR findings reconciliation.

[R523] PASS Conformance - `sw/mailbox/mailbox.yaml:193`, `:234`, `:415`, `:455`; `hdl/milan/mailbox/KL_mbx_rx.sv:149`; `tb/verilator/mbx/suite.hpp:946` - The seven match tuples implement the owner's six table rows, including the additional ACMP own-unicast tolerance. Each multicast address is paired with its own EtherType/subtype. AECP uses target at byte 18 with mask 0x5555 and controller at byte 26 with mask 0xAAAA, including the CONTROLLER_AVAILABLE response with unrelated opposite identity. Tagged frames match neither a tuple nor a control EtherType; untagged AAF/CRF have no channel. The mismatch definition is independent of channel enable and identity refusal. Generated SV, header and reference page are byte-consistent with the generator; major 2 prevents older firmware silently omitting own-MAC setup. The normative acceptance table is the approved repository authority; the listed standards clauses are its traceability references.

[R523] PASS RTL - `hdl/milan/mailbox/KL_mbx_rx.sv:130`, `:249`, `:265`, `:368`, `:384`; `hdl/milan/mailbox/KL_mbx.sv:133`, `:181`, `:209`, `:460`, `:476`; `sw/litex/milan_soc.py:2475`, `:3293` - Destination capture completes before byte-14 classification. The first accepted byte latches the interface; the own-MAC mux grants no own tuple for an absent interface. The ten flattened tuples index five channels correctly. The mismatch latch clears between frames and reset, its counter updates once at the terminal decision and saturates at 65535, and ERR joins the existing sticky path. New registers use the existing clock and synchronous reset, without a new crossing. Ring publication and backpressure remain on the existing path; token accounting logic and parameters are unchanged. Both bus adapters, their top-level ports, and the default-off SoC guard are unchanged. The mailbox sources are added only under that guard.

[R523] PASS Robustness - `tb/verilator/mbx/suite.hpp:1002`, `:1060`, `:1090`, `:1122`, `:1148`; `hdl/milan/mailbox/KL_mbx_rx.sv:192`, `:343`; `boundary_probe.cpp`; `boundary-probe.log` - The shipped suite checks separate tuple/identity failures, unsupported interface index, closed channels, repeated failures, rewriting own-MAC, counter read-only/reset behavior, independent rate exhaustion, ring limits and existing bus stalls/reset cases. The independent two-interface probe checks all 48 destination bits on each interface, cross-interface destinations with differing high and low words, AECP identities one byte short and exactly complete, all three declared TPIDs and nested tags, and lengths 1 through 15 interleaved with valid frames. It drives the new counter through 65534, 65535 and a further frame, verifies a write cannot clear it, and checks reset clears the programmed MACs and the nonzero counter. All 1048 assertions pass through each adapter and the model. No new ingress-abort/timeout contract is claimed.

[R523] PASS Tests - `tb/verilator/mbx/frames.hpp:26`, `suite.hpp:946`, `mutants.py:66`, `:120`, `:172`; `sw/firmware/ctrl/test/ctrl_mutants.py:45`, `:343`; `test_unit_driver.cpp:137`, `test_port_loop.cpp:464`, `:590`, `test_unit_seams.cpp:95`; `sw/firmware/gtest/coverage.ratchet` - The frames encode the approved wire constants independently of the generated match table. Q0 provides a positive control for every row, Q1-Q10 check the required individual refusals and observations, and the same suite runs on both adapters and the host model. All 67 RTL plants are caught by their named checks after clean controls. All 17 new firmware/model plants plus the re-pointed composition plant are caught (18/18). The two re-pointed RTL arms still omit subtype/second tuple and fail C0/C3 respectively; the composition arm still binds the pool late and fails U1. The fixture census reproduces 137/137 at base and 186/186 at head; it does not independently establish when the executor ran the pre-edit audit. Native firmware tests, the freestanding target compile, tally self-tests and coverage self-tests pass. Coverage remains 100% of measured lines and branches on 14 files after the same 14 exclusion rows; the checker and exclusion definitions did not change.

[R523] PASS Docs - `docs/design/MAILBOX_SPLIT.md:67`, `:153`, `:481`, `:547`; `docs/reference/MAILBOX_CONTRACT.md:45`, `:200`, `:327`; `sw/firmware/ctrl/README.md:51`; `sw/firmware/gtest/README.md:162`; `tb/verilator/mbx/README.md:58`; PR #685 body - The interface, version boundary, register masks, two-sided AECP, test inventory and default-off placement agree with the examined code and executed focused checks. The OOC resource table agrees with the published measurement summary and is explicitly a switch-on out-of-context result. Full product integration and physical timing remain outside this lane. The requirement-status sentences reserved for the manager are not a finding of this PR.

Reviewer-owned coverage ledger:

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | REQUIREMENTS.md:58; FR_NFR.md:322, :328, :403; mailbox.yaml:415; KL_mbx_rx.sv:149; generator.log | R523-1 | 021b9c1fb966e9a1a4acef6b5233edd3518f32a0 |
| RTL | CLEAN | KL_mbx_rx.sv:130, :249, :265, :384; KL_mbx.sv:133, :181, :476; milan_soc.py:3293; mbx-suite.log | R523-1 | 021b9c1fb966e9a1a4acef6b5233edd3518f32a0 |
| Robustness | CLEAN | suite.hpp:1002, :1090, :1122, :1148; boundary_probe.cpp; boundary-probe.log | R523-1 | 021b9c1fb966e9a1a4acef6b5233edd3518f32a0 |
| Tests | CLEAN | suite.hpp:946; mutants.py:172; ctrl_mutants.py:343; test_unit_driver.cpp:137; firmware-coverage.log; fixture-audit.log | R523-1 | 021b9c1fb966e9a1a4acef6b5233edd3518f32a0 |
| Docs | CLEAN | MAILBOX_SPLIT.md:153, :481, :547; MAILBOX_CONTRACT.md:327; mbx/README.md:58; public handoff sections 2, 5-9; PR body | R523-1 | 021b9c1fb966e9a1a4acef6b5233edd3518f32a0 |

Finding R523-1-R1:

- Severity: RESIDUE.
- All attributable lenses: Docs.
- Artifact: PR #685 body, Contents lines 5-12 and Status line 16 in `pr-body-punctuation.json`.
- Authority/evidence: CONTRIBUTING.md section 6.1 forbids U+2014 in new branch text, including Contents separators. These nine occurrences are prose punctuation only.
- Impact: wording-rule residue; no measurement, figure, verdict, test, code, generated artifact, conformance/clause claim or privacy rule changes.
- Required outcome: replace each of those nine U+2014 separators with the ASCII string `--`; preserve every adjacent word, link and number.
- Verification: scan the revised PR body for U+2014 and confirm zero occurrences and no other content change. The manager carries this on the residue checklist. This leaves Docs CLEAN under the owner rule.

Executed receipts (every command has a log, command record and rc file):

| Receipt prefix | Result |
|---|---|
| generator; generator-selftest | 0 findings; 14 output and 12 contract plants detected, two-interface generation passes and four-interface variant refuses |
| mbx-suite | 285/0 Wishbone; 330/0 AXI4-Lite; 13/0 firmware co-simulation; two-interface 285/0, 330/0 and model 285/0 |
| rtl-mutants | Both controls pass; 67/67 caught, including the five quick plants |
| firmware-native | Model, port, ADP, unit, reused walk, all five entity shapes and target cross-compile pass |
| firmware-mutants | 18/18 selected plants caught; this review does not claim to have re-executed the other 75 firmware plants |
| firmware-coverage; coverage-selftest | Ratchet passes, 14 files, unchanged exclusions; 28/28 controls |
| tally-selftest | 18/18 cases and 18/18 listener plants |
| boundary-probe | 1048/0 each on two-interface Wishbone, AXI4-Lite and model; saturation exercised through actual frames |
| fixture-audit | 137 base / 186 head fixtures plant; patch census has no mailbox references |
| integrity-before; integrity-after | Exact tracked bytes, modes and index, including all three required submodule pins |

`replay.py`, `static_checks.py`, `run.py`, `simulator.py`, `filter_mutants.py`, `boundary_probe.py`, `boundary_probe.cpp`, `fixture_audit.py` and `integrity.py` are the portable receipt/probe drivers. Commands ran in foreground. The simulator identity is recorded in `simulator-identity.json`. Path-only redactions of local compiler support paths in two logs are recorded in `redaction-receipt.json`; their originals remain in `scratch/raw-receipts`. Builds and mutation trees remain exclusively under `scratch/`; they are not publishable. The main suite used `make -j16` with nested compilation bounded, and the mutation driver used an explicit job count. Concurrent campaigns were bounded to at most 16 compiler workers; no vendor implementation run was launched.

Limits and pending manager duties:

- The [public packet at 8faa1b7a](https://github.com/kebag-logic/milan-fpga/tree/8faa1b7a6a0bad3e0e552a85fd009e3a55c79b1b/review-evidence/665fc-r1) contains the published handoff, PR body and receipt digests. Its tree snapshot contains no underlying raw bank, export or area logs. Their published summary was read; private lane material was not used. The assignment reports the manager's full source static/builder and native banks passing. This review independently reproduces the focused receipts above, not those full banks or physical measurements. Publish/link the manager's exact-head receipts as part of merge evidence.
- Default-off exclusion is confirmed structurally. The reported export comparison covers both AX configurations at shipping settings and the three Arty configurations at 100 MHz because the base and head both fail PLL selection at 83.333 MHz. This is not a newly measured shipping bitstream identity or a physical timing claim. The OOC totals (2730 LUT, 2852 FF; delta +89/+115) are reported measurements, not rerun here.
- `hosted-checks.json` is an observation, not hosted acceptance. At that snapshot the firmware, lint, behavior, wire and no-Git docs jobs and four synthesis shards had executed successfully; several other jobs were still running and the Physical gPTP job was skipped. No all-green hosted aggregate or hardware pass is claimed. The manager owns current hosted/local-replica acceptance and must distinguish skipped contexts from executed jobs.
- Source base `6714181d` is not the live-dev candidate. The manager must construct and validate the actual candidate against current dev (assignment tip `6a05347d`), settle both independent reviews, wait until no review remains in flight, obtain the required merge authorization, and perform post-merge containment. This review makes no merge-tree, current-dev or post-merge claim.
- Update REQUIREMENTS.md:93-94 and FR_NFR.md:427, :599 at the merge turn as assigned. Refresh the PR's historical local-only status with the published head and hosted evidence; retain the stated source/physical limits.
- The datapath tap is still idle behind the default-off switch. F2-F5 integration, real service latency, physical calibration (NOT RUN), field skips and hardware acceptance remain unproven by these simulations. Redundancy and a production per-interface entity model are not enabled here.
- The optional `external` submodule was uninitialized. Its gitlink is verified; no claim is made about absent contents. The required protocol, gPTP and stream-library submodule checkout bytes, modes, indices and pins are verified.

Public prior-findings reconciliation: `prior-findings.json` was fetched after the independent verdict and ledger were written. PR #685 had two manager review-start comments, zero submitted reviews and zero inline review comments at that snapshot. There were no published prior review findings on this PR to resolve or retain. No other reviewer report was used to set this verdict.

R523-1 FINISHED
