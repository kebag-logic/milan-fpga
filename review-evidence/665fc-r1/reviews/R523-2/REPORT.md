[R523] POSITIVE - exact head db9aa8c9b135b34ff3d070a979dee70440b37cc6

External independent review, round R523-2, issue #665 / PR #685. Tree `86d60d1102b4018b2d4be85864c80f29c5c88535`. All five lenses were independently reapplied to the full PR, `6714181d0c8a16e2983f85b724f4d688f5111835..db9aa8c9b135b34ff3d070a979dee70440b37cc6`, with focused execution of the seven-commit delta from `021b9c1fb966e9a1a4acef6b5233edd3518f32a0`. No BLOCKER, MAJOR or MINOR is open. The previous prose residue and two optional suggestions are retained below.

Reconstruction followed AGENTS.md / CONTRIBUTING.md, docs/README.md, the issue body and [FC assignment](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6021509373), the [round-2 decision](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6026839422) answering [F2's STOP](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6026825549), requirements and interface authorities, then the full diff/history and public evidence. Standards were checked directly in local PDFs. The independent verdict and ledger in `receipts/independent-verdict.md` were written before prior review findings were read. No private author material or another lane's checkout was used.

[R523] PASS Conformance - `sw/mailbox/mailbox.yaml:514`, `hdl/milan/mailbox/KL_mbx_rx.sv:157`, `sw/firmware/ctrl/host/mbx_model.c:303`, `REQUIREMENTS.md:58` - IEEE 1722-2016 B.2.1, printed page 154, sends DEFEND to the triggering PROBE's source MAC; Table B.1 on page 155 assigns DEFEND type 2. The amended row implements `(MAAP multicast) OR (receiving interface's OWN_MAC AND type 2)`, followed by the unchanged requested-range overlap term at byte 26. Multicast DEFEND remains accepted as the public decision requires. Own-unicast PROBE, ANNOUNCE and all thirteen reserved types, and foreign-unicast DEFEND, are dropped and counted once. A nonoverlapping own-unicast DEFEND fails identity after matching its tuple, so remains uncounted. Q0-Q11, the mutation results and independent prefix/type probes confirm these distinctions.

The whole-PR pass also checked ADP/ACMP multicast against IEEE 1722.1-2021 Table B.1, ACMP transmission against 8.2.1, AECP field meanings and defined message parity against 9.2.2.4/7/8, MVRP against IEEE 802.1Q-2018 Table 10-1, and CONTROLLER_AVAILABLE against Milan v1.2 5.4.5.3. Own-unicast ACMP is the owner's receive tolerance. Reserved AECP types retain the documented repository parity policy. Tagged traffic and untagged AAF/CRF remain excluded. No complete protocol-validation claim is made for this ingress filter.

[R523] PASS RTL - `hdl/milan/mailbox/KL_mbx_rx.sv:98`, `:130`, `:157`, `:225`, `:327`, `:365`, `:412`; `hdl/milan/mailbox/KL_mbx.sv:150`, `:181`, `:460` - Before byte 15 is accepted, three words occupy the four-word queue. Its acceptance enqueues the fourth and sets classification complete; the next cycle can drain while READY is low. Classification therefore needs no prior drain. End-at-byte-14 uses the current subtype and message type zero. Shorter frames use the existing unclassified termination path. The held subtype is overwritten before each subsequent classification. Channel selection, speculative write bounds, final header publication, reset, counter saturation and token accounting remain coherent. No clock crossing or external port is added. Both adapters and both interface-count variants pass their complete mailbox suites.

[R523] PASS Robustness - `tb/verilator/mbx/suite.hpp` Q1-Q11/D/T/H; `scripts/boundary_probe.cpp`; `receipts/boundary-0.log`, `boundary-1.log`, `boundary-model.log` - The suite checks separate tuple/identity failures, channel closure, rate exhaustion, ring bounds and per-interface matching. The independent probe checks every length 1-66 against every low-nibble type and multicast/own/foreign destinations, all 256 byte-15 values, both MRP tuples at lengths 14/15/16, and 65,540 counted frames followed by reset. Both adapters additionally check READY through the initial sixteen bytes, reset after prefixes 0-17, and a valid frame with gaps after every byte and exact payload readback. Results: 92,117 assertions through each adapter and 91,672 on the two-interface model, zero failures. Q11 recovery after byte-14 and byte-15 truncations also passes. No new timeout or ingress-abort guarantee is inferred.

[R523] PASS Tests - `sw/mailbox/mailbox_model.py:258`, `mailbox_emit.py:28`, `gen_mailbox.py:235`; `tb/verilator/mbx/mutants.py` round-2 table; `sw/firmware/ctrl/test/ctrl_mutants.py:396`; `receipts/focused-results.json` - All four generated outputs reproduce exactly through a disposable copy's `gen_mailbox.py --write`. Check/crosscheck is clean; the self-test catches 16 output and 15 contract defects, accepts the two-interface variant and refuses the overlapping four-interface variant. Tuple masks default to all types, unused tuples to zero, and the own DEFEND tuple to bit 2. The shared model/RTL suite executes group 21, Q11. All 81 RTL and 97 firmware-table anchors occur exactly once. This round executed fourteen new RTL arms, the re-pointed subtype arm and four model twins: every build succeeded and each run returned 1 with its named failing assertion. In particular, the repaired `model-tuple-msg-type-ignored` arm at this head compiles and fails Q11. Controls passed before mutation failures were credited.

| Executed mutation | Coverage | Required check observed failing |
|---|---|---|
| DEFEND tuple removed | Both adapters | Q11 own DEFEND delivery |
| Message type read one byte early | Both adapters and model | Q11 own DEFEND delivery |
| Classification before message type | Both adapters | Q11 own DEFEND delivery |
| Tuple message mask ignored | Both adapters and model | Q11 own PROBE rejection |
| Own/type refusal left uncounted | Both adapters and model | Q11 own PROBE counted once |
| DEFEND accepts any unicast | Both adapters and model | Q11 foreign DEFEND rejection |
| End-at-byte-14 never classifies | Both adapters | Q11 byte-14 truncation counted |
| Re-pointed subtype ignored | Wishbone, its table assignment | C0 ACMP classification |

The full-PR firmware additions were also reviewed: `mbx.c:101` writes the per-interface MAC through the HAL and reads the mismatch field; `ctrl_loop.c:71` writes identities before opening channels; `ctrl_app.c:25` supplies the entity MAC. Native model, port and unit controls pass. Coverage-ratchet changes add measured lines/branches without changing exclusions; the round-2 ratchet and production C are unchanged. Full coverage execution remains published author/manager and retained round-1 evidence, not a rerun claimed here.

[R523] PASS Docs - `REQUIREMENTS.md:58`; `docs/reference/FR_NFR.md:328`, `:409`, `:427`, `:599`; `docs/design/MAILBOX_SPLIT.md:156`, `:581`; generated `MAILBOX_CONTRACT.md`; mailbox and firmware READMEs - The destination/type rule, identity term, counters, byte boundary, status lines, test inventory and generated constants agree with the implementation. NFR-SCOUT-02 delegates the detailed table to NFR-SCOUT-08; it does not negate the MAAP message-type condition. Keeping 2.0 is consistent with reviewing the first unpublished major-2 release as one PR. Owner approval of the amended row remains a merge condition, not a finding.

Reported OOC totals change from 2,730 LUT / 2,852 FF to 2,745 LUT / 2,860 FF, delta +15/+8, with reported WNS +0.186 ns at 10 ns and unchanged block RAM/DSP use. The listed hierarchy has the same 20-LUT difference from the total before and after. The recipe and numbers agree with the [public round-2 packet](https://github.com/kebag-logic/milan-fpga/tree/6a0ea99cd26559b983c918cd79d023efb0fa10c9/review-evidence/665fc-r1/author-r2). Relevant HDL and the top are byte-identical between measurement head `dd86e68b` and this head. These are audited published measurements, not independently rerun measurements; the archive contains their digest inventory but not the raw reports.

Reviewer-owned ledger:

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | REQUIREMENTS.md:58; mailbox.yaml:514; primary clauses above; Q0-Q11; authority-evidence.json | R523-2 | db9aa8c9b135b34ff3d070a979dee70440b37cc6 |
| RTL | CLEAN | KL_mbx_rx.sv; KL_mbx.sv reset/register/wiring diff; package; both adapters/interface variants; source-invariants.json | R523-2 | db9aa8c9b135b34ff3d070a979dee70440b37cc6 |
| Robustness | CLEAN | suite.hpp Q1-Q11/D/T/H; boundary_probe.cpp; boundary-0/1/model.log | R523-2 | db9aa8c9b135b34ff3d070a979dee70440b37cc6 |
| Tests | CLEAN | gen_mailbox.py selftest; mutants.py; ctrl_mutants.py; focused-results.json; model/port/unit and cosim receipts | R523-2 | db9aa8c9b135b34ff3d070a979dee70440b37cc6 |
| Docs | CLEAN | REQUIREMENTS.md:58; FR_NFR.md:328/409/427/599; MAILBOX_SPLIT.md; MAILBOX_CONTRACT.md; READMEs; public handoff and PR body | R523-2 | db9aa8c9b135b34ff3d070a979dee70440b37cc6 |

The delta touches all five lenses, so none is banked solely from an old head. The [R523-1 ledger](https://github.com/kebag-logic/milan-fpga/pull/685#issuecomment-6026554466) at `021b9c1fb966e9a1a4acef6b5233edd3518f32a0` remains supporting coverage for unchanged artifacts: adapter RTL, top/register implementation, production firmware additions, coverage exclusions and default-off integration. Their unchanged scope was checked again; the table above owns the complete present-head result.

Prior public findings, explicitly retained or resolved:

- **R523-1-R1, RESIDUE, Docs; retained.** Artifact: PR #685 body lines 5-12 and 16, recorded in `receipts/prior-findings.json`. CONTRIBUTING.md 6.1 prohibits its nine U+2014 separators. Impact is punctuation only: no number, measurement, verdict, test, code, generated artifact, clause/conformance claim or privacy rule changes. Exact fix: replace those nine separators with ASCII `--`, leaving adjacent content unchanged. Verify zero U+2014 occurrences and an otherwise identical body. The manager carries this on the residue checklist; Docs remains CLEAN.
- **R522-1-S1, SUGGESTION, Tests and Robustness; retained.** Artifacts: `KL_mbx_rx.sv:177`, `:375`, `:412` and the suite's filter groups. The [prior review](https://github.com/kebag-logic/milan-fpga/pull/685#issuecomment-6026704364) requested permanent checks for saturation, a sub-15-byte frame immediately after a mismatch, and zero destination on an absent interface at reset MAC. The guards remain present; this round independently confirms saturation/reset. Impact is optional regression hardening, with no established current-head malfunction. Optional outcome: add those three permanent checks; verify each corresponding removed guard fails its named check.
- **R522-1-S2, SUGGESTION, Tests; retained.** Artifact: `gen_mailbox.py:_contract_arms`, `mailbox_model.py:_check_channels`. The self-test still plants C- and S-tag TPIDs but not `0x88E7`; the common membership refusal still includes all three declared TPIDs. Impact is optional fixture completeness. Optional outcome: add an `0x88E7` contract plant; verify it reports the TPID refusal.
- **F2 STOP 6026825549: resolved within this PR's assigned scope.** Own-unicast DEFEND now delivers, and the mutation results distinguish the relevant defects. This does not resolve the separate shipping allocator deviations described in the STOP or implement F2.

At reconciliation there were zero submitted reviews and zero inline review comments; the two round-1 verdicts were PR conversation comments. No previous blocking finding was silently dropped. Prior requirement-status merge duties are satisfied by this delta's status edits.

Executed evidence:

| Receipt | Result |
|---|---|
| compiler-identity | Required scoped simulator reports version 5.050, revision v5.050 |
| generator-check; generator-selftest; source-invariants | Zero findings; self-test controls behave as required; CLI regeneration exact |
| control-0/1; if2-control-0/1 | 316/0 and 361/0 on each interface-count variant |
| model-control; if2-model-suite | 22/0 test groups; 316/0 two-interface assertions |
| port-control; unit-control | 31/0; 23/0 plus 2/0 |
| focused-results.json | Fifteen selected RTL arms and four model twins caught; all controls green |
| boundary-0/1/model | 92,117/0, 92,117/0 and 91,672/0 |
| cosim | 13/0, firmware on RTL and model |
| plant-audit | All 81 RTL and 97 firmware/model anchors unique |
| integrity.json | Exact 1,141 superproject blobs, modes and index; required submodules: 558, 104 and 214 blobs, modes, indices and pinned heads |

Portable drivers are under `scripts/`; `replay.py` reproduces focused checks into a new packet directory. Campaigns ran concurrently within foreground processes, with at most three builds of four compiler workers. Co-simulation used `make -j16` with nested compilation bounded to four. Each executed case has a log and return-code receipt. Raw build diagnostics have path-only publication substitutions recorded in `receipts/redactions.json`; originals remain under unpublished `scratch/raw-receipts`. No source fix, commit, push, GitHub write, hardware action, shared install or vendor implementation run occurred. Probes used disposable copies; source files needed no restoration. Final direct byte/mode/index verification proves the requested head and required gitlinks.

Real limits and pending manager duties:

- This approves source head `db9aa8c9`, not the final current-dev candidate. The manager must build and validate that candidate against live dev, with assignment tip `79b086d44eb62d007d38e18f5618b98e8e2a33e6`, settle both independent rounds and perform the required merge/containment workflow after authorization.
- Obtain owner approval for the amended MAAP row before merge. Complete hosted and local-replica acceptance. The read-only `hosted-snapshot.json` shows some successful executed jobs, four successful synthesis shards, other jobs still running, and the physical job skipped; no complete hosted aggregate is asserted.
- The assignment supplies the manager's full source static/builder and native-bank pass. Public handoffs supply broader author results and digests. This reviewer did not rerun prohibited full parent, processor, synthesis or builder banks, nor complete 81/97 mutation campaigns or the coverage bank. Publish/link the manager's exact-head receipts as merge evidence.
- Default-off exclusion is structurally unchanged: `milan_soc.py:2555`, `:2590`, `:3295` load the contract/add the mailbox only under the default-false switch. Default-build source/configuration inputs, shipping firmware and submodule pins are unchanged across the full PR. No gateware export or shipping bitstream was independently rebuilt here. Across round 2 specifically, `KL_mbx.sv`, all register definitions, capacities, identity terms, token parameters and production firmware C are unchanged. Across the whole PR, new mailbox registers and firmware APIs are intentional; external top ports remain unchanged.
- OOC figures are published switch-on measurements with source lineage verified, not hardware proof. Physical calibration was NOT RUN; field skips are not hardware proof. The default-off datapath tap remains idle; F2-F5 integration, actual service latency, physical release acceptance and production redundancy remain outside this review's proof.
- The optional `external` submodule remains uninitialized; only its gitlink is verified. All three required submodules are verified against their pins and actual bytes.

R523-2 FINISHED
