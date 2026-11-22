[R884] NEGATIVE - exact head f15b3a7d2bf1ba84d14140a4cda8a193d2e6b1c9

Round R884-1. Independent pass completed before consulting prior public findings. Tree 44de68bf9dfc3534963fc1e11a6a86477c669ff1; diff base 59b098841b1e2826aaf7a38b557faa5345f91c82. All five lenses applied. Four open MAJOR findings prevent approval. Public evidence reconciliation additionally found one MINOR verdict-reporting defect (F5).

## Findings

### R884-1-F1 — MAJOR — Conformance, RTL, Robustness, Tests, Docs
Artifact: hdl/milan/mailbox/KL_mbx_cdc.sv:481; sw/firmware/ctrl/host/mbx_model.c:1409; docs/design/GPTP_SOFTWARE.md:95.

GEN publication can tear while a preceding crossing is in flight. The crossing remembers the generation but reads the live register bank when it can send; it does not retain the bank committed by that generation. A sequential bus-like stimulus commits GEN 1, commits GEN 2 while GEN 1 is in flight, then writes the low GM word for an uncommitted next update. The actual crossing delivers GEN 2 with GM 2222222233333333 instead of committed 2222222222222222. The control with no subsequent partial write delivers both correct banks.

Authority/evidence: mailbox.yaml:421 and :448, generated MAILBOX_CONTRACT.md:262, REQ-PTP-07, and issue #884 ruling item 7 require a GEN-committed whole snapshot. publication.log and publication-control.log exercise the real RTL. The host model snapshots immediately at the GEN write, so the closed-loop snapshot assertions at tb/verilator/gptp_sw/sim_main.cpp:676 do not exercise this failure. GPTP_SOFTWARE.md:95-99 claims atomic crossing and correspondence to firmware answers that the RTL does not preserve under this ordering.

Impact: consumers can observe a GM identity never published by firmware, paired with another generation's health/domain/discontinuity fields; firmware answers and fabric state disagree.

Required outcome: retain a coherent committed bank throughout queuing and crossing; later uncommitted writes must not alter any delivered generation. Preserve the documented interface guarantee, and align executable integration evidence with the actual crossing.

Verification: run run_publication.py against the corrected source; both control and overlapping-update cases must pass. Add coverage for queued commits, partial writes, generation wrap and reset with a transfer outstanding.

### R884-1-F2 — MAJOR — Conformance, RTL, Robustness, Tests
Artifact: sw/firmware/ctrl/gptp/gptp.c:636 and :932; sw/firmware/ctrl/test/test_gptp.cpp:541.

Raw Sync messages indefinitely postpone the synchronization timeout even when no Follow_Up completes a pair. The probe first establishes asCapable and one valid pair, then supplies Sync every 120 ms without Follow_Up. After 720 ms, both priority1=248 and priority1=255 remain SLAVE with sync_ok=1, sync_used=1, rto_sync=0.

Authority/evidence: IEEE 802.1AS-2020 10.2.8.2.1(c), Figure 10-4 and 11.2.14 tie renewed synchronization information to the completed two-step reception; Milan v1.2 4.2.6.2.3 bounds syncReceiptTimeout at 337.5–562.5 ms. REQ-PTP-08 requires loss of synchronization to reach time validity. protocol.log contains both cases. The Announce timeout test keeps the master alive with Sync alone and therefore reinforces this incorrect assumption.

Impact: a failed two-step master can leave stale synchronization advertised indefinitely. The firmware-to-fabric health architecture consequently fails to invalidate time on this loss path.

Required outcome: refresh the synchronization receipt deadline only on usable synchronization information; independently expire pending Follow_Up state and propagate loss to the publication/role required for the configured port.

Verification: run run_protocol.py with both master-capable and slave-only configurations; continuous Sync and Announce with missing Follow_Up must not suppress the timeout. Preserve the separate Announce timeout test using complete valid pairs.

### R884-1-F3 — MAJOR — Conformance, RTL, Robustness, Tests
Artifact: sw/firmware/ctrl/gptp/gptp.c:358 and :698; sw/firmware/ctrl/test/test_gptp.cpp:395.

Three successive multi-responder exchanges do not cease Pdelay requests when the second responder arrives after the first responder's Follow_Up. Completion clears multi_run before the late response increments it. The probe supplies this ordering three times: multi_run is 1 after every exchange and ceased remains false.

Authority/evidence: Milan v1.2 4.2.6.2.5 requires ceasing after responses from multiple clock identities to each of three successive requests, irrespective of this arrival order. protocol.log reproduces three requests with distinct responders. The existing test exercises a second responder before completion only.

Impact: Pdelay requests continue on the non-AVB multi-responder segment the cease rule is intended to contain. This is an incomplete protocol state transition, not merely a missing assertion.

Required outcome: classify successive request exchanges without erasing the previous multi-responder run before the current exchange's response window can establish its outcome. Count distinct clock identities and resume only under the specified conditions.

Verification: the late-second-responder case in run_protocol.py must cease by the third request; retain the existing early-second-responder case and cover a clean intervening exchange, duplicate responses, and the permitted link/timer resume conditions.

### R884-1-F4 — MAJOR — Conformance, Robustness, Tests
Artifact: sw/firmware/ctrl/gptp/gptp.c:652 and :765.

A 44-byte Follow_Up without its mandatory 32-byte information TLV is accepted as a usable synchronization pair. The receiver substitutes zero cumulativeScaledRateOffset when the TLV is absent or invalid, then disciplines time and asserts sync_ok. The probe observes sync_used=1 and sync_ok=1 for that truncated message.

Authority/evidence: IEEE 802.1AS-2020 11.4.4.1/Table 11-10 and 11.4.4.2.2 require the Follow_Up information TLV; 11.2.14.2.1 derives synchronization data from it. protocol.log supplies a selected-master Sync followed by the short Follow_Up. This is not Ethernet padding: the declared PTP messageLength is 44.

Impact: malformed synchronization messages become valid measurements with invented rate information and can mark time synchronized.

Required outcome: validate the required Follow_Up structure and information TLV before consuming the pair or changing the servo/health publication.

Verification: reject absent, truncated and malformed required TLVs without servo updates or a renewed synchronization deadline; retain acceptance of complete valid messages and any permitted additional TLVs.

### R884-1-F5 — MINOR — Tests, Docs
Artifact: PR #966 body, Evidence / Local gates; public author-r2/receipts/round2b/gates/SUMMARY.txt, xvlog row.

The PR describes the 73 gates as “All PASS”, but the published summary contains 73 rc=0 entries including an explicitly SKIPPED xvlog gate because the executable was unavailable. Its receipt explicitly distinguishes a skip from a pass.

Authority/evidence: CONTRIBUTING.md verification requirements and the review contract require executed checks to be distinguished from skips. public-review-state.json preserves the PR claim; public-evidence.log preserves the contradictory gate result. This affects a verification verdict, so it is MINOR rather than wording-only RESIDUE.

Impact: a cold reader is told the front-end check executed successfully at this head when that receipt proves no such execution.

Required outcome: correct the public gate accounting to identify the skipped check and its reason. Any replacement execution must be linked to its actual head; the manager retains responsibility for deciding acceptance of required gates.

Verification: compare the corrected PR evidence table with every entry in the pinned summary; an exit-zero skip must remain labelled SKIPPED.

## Reviewer-owned coverage ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1–F4) | gptp.[ch], gptp_mbx.c, mailbox.yaml, IEEE 802.1AS-2020 10/11, Milan v1.2 4.2.6, #884 scope rulings | R884-1 | f15b3a7d2bf1ba84d14140a4cda8a193d2e6b1c9 |
| RTL | UNCLEAN (F1–F3) | KL_gptp_tsu.sv, KL_ctrl_split.sv, KL_mbx_cdc.sv, KL_mbx_evt.sv, milan_datapath.sv, firmware protocol state transitions | R884-1 | f15b3a7d2bf1ba84d14140a4cda8a193d2e6b1c9 |
| Robustness | UNCLEAN (F1–F4) | protocol.log, publication.log/control, test_gptp.cpp, timestamp FIFO/reset/credit paths and flood receipts | R884-1 | f15b3a7d2bf1ba84d14140a4cda8a193d2e6b1c9 |
| Tests | UNCLEAN (F1–F5) | test_gptp.cpp, gptp_mutants.py, gptp_sw/sim_main.cpp, mbx_model.c, service-budget harness and published gate receipts | R884-1 | f15b3a7d2bf1ba84d14140a4cda8a193d2e6b1c9 |
| Docs | UNCLEAN (F1, F5) | GPTP_SOFTWARE.md, MAILBOX_CONTRACT.md, REGISTER_MAP.md, FR_NFR.md, SPLIT_CONTROL_MEMORY.md and public handoff/evidence | R884-1 | f15b3a7d2bf1ba84d14140a4cda8a193d2e6b1c9 |

## Scope and independent examination

The review reconstructed AGENTS.md, CONTRIBUTING.md, docs/README.md, issue #884 and its frozen acceptance/scope decisions, linked requirements and interface authorities, then the specified diff and commit history. The controlling scope is the [2026-11-21 ruling](https://github.com/kebag-logic/milan-fpga/issues/884#issuecomment-7067495546) and [round 2b ruling](https://github.com/kebag-logic/milan-fpga/issues/884#issuecomment-7072401468), implementing #872's software-ownership decision. The older flexPTP-only/no-Vivado proposal does not supersede those decisions. The actual IEEE 802.1AS-2020, IEEE 802.1AS-2011 and Milan v1.2 texts were consulted; no draft or newer Milan version replaces those authorities.

Conformance examination covered the BMCA vector comparison and selected-master filtering; Announce/path-trace encoding and loop rejection; slave and grandmaster two-step operation; initiator/responder timestamp pairing; neighborRateRatio and three-sample median; asCapable acquisition, fifth-lost-response handling and multi-response cease; PI recurrence, step thresholds and rate clamp. For the stated PI recurrence, gKp=0.64 and gKi=0.16 give z²−1.2z+0.36=(z−0.6)² before fixed-point rounding. The servo's step/slew handling was compared with the documented #75 contract. These checks do not excuse F2–F4.

RTL/architecture examination covered the TSU's ingress subtraction and egress reconstruction (426 ns GMII / 3,770 ns MII), observer seal and guard, FIFO ordering, ingress trailer ownership in KL_ctrl_split, uncoalesced TIMESTAMP credit return, reset paths, narrowed status decode, CSR PHC ownership, and the software-owner build guards. The protocol state-machine failures F2/F3 also belong to the RTL-and-architecture lens under AGENTS.md's overlapping-lens rule. F1 is an actual crossing failure reproduced with independent 100 MHz source and 50 MHz destination clocks; the probe drives the crossing's register-bank face directly, not a complete processor/Wishbone boot. It establishes an interface failure, not the frequency of that ordering in current firmware.

The admission table derives seven records per interface from the seven received message kinds and interval argument, and mailbox_model scales it by interface count; it is not a hard-coded fit to the held egress row. The event and adapter identify interfaces, with no hart-zero routing premise. The plane sources and processor gitlink remain present; --sw-gptp removes their elaboration and keeps timestamp/PHC hardware. One product MAC and the deferred second MAC are explicit.

Documentation examination compared GPTP_SOFTWARE.md, FR_NFR.md, REGISTER_MAP.md, MAILBOX_CONTRACT.md, SPLIT_CONTROL_MEMORY.md and the build/test maps with source and published receipts. Generated mailbox files and the register reference independently regenerate cleanly. The source-comment rule was checked against added source lines; no new prohibited review-round/identity/issue-comment/bench-lane label was identified. No RESIDUE is claimed.

## Executed review checks and reproducibility

Run scripts from this packet with the checkout as their first argument; all generated builds/probe binaries belong under packet `scratch/`. `VERILATOR` may select the pinned executable. The reviewed executable identified itself as Verilator 5.050, revision v5.050. No source fix or source mutation was made in the checkout. The existing mutant driver uses disposable copies.

| Command / receipt | Observed result |
|---|---|
| `python3 -B run_checks.py <checkout>` / core-mutants.log | Baseline passed; 25/25 planted defects caught with `--jobs 8` |
| Same driver / tsu.log | `make -j16 run`, inner build limited to 4 jobs; 36 checks, zero failures |
| Same driver / mailbox-generation.log | `gen_mailbox.py --check --crosscheck --selftest`: zero findings/failed controls |
| Same driver / register-generation.log | Initial environment refusal, rc=2: missing wavedrom dependency; not a source failure |
| `python3 -B run_core_arms.py <checkout>` / core-arms.log | 34 host tests and 4 RV32IM audit checks passed; text 11,674 bytes, data/BSS zero; no float/libm/64-bit divide helper |
| `<scoped-python> -B run_register.py <checkout>` / register-generation-scoped.log | Fresh: 203 registers, 34 modules, 240 files. Scoped environment uses wavedrom==2.0.3.post3, installed only beneath scratch |
| `python3 -B run_protocol.py <checkout>` / protocol.log | Expected failing regression probe: four failed assertions, representing F2 in two configurations, F3 and F4; valid-pair setup controls pass |
| `python3 -B run_publication.py <checkout>` / publication-control.log, publication.log | Control passes; partial next update causes a torn committed bank and assertion failure (F1) |
| `python3 -B audit_public_evidence.py <checkout>` / public-evidence.log | Reads/hash-identifies selected receipts from the pinned public evidence commit; no execution of those author banks is claimed |
| `python3 -B verify_integrity.py <checkout>` / integrity.log | Exact head/tree, all tracked blob bytes/modes and stage-zero indexes match; five required submodule heads/bytes/indexes match; superproject status empty |

The first campaign ran independent checks concurrently within the requested process limit; all foreground processes were awaited. The protocol/publication nonzero return codes are the reproduced findings, not infrastructure failures. The publication assertion abort is recorded as return code -6; the controlling script returns 1. The host baseline and positive publication control distinguish those failures from general setup/build failures.

## Published evidence assessed, with its limits

The source execution evidence is the [author packet at dc64b04a](https://github.com/kebag-logic/milan-fpga/tree/dc64b04aef437e6b15071781f08c62a077827262/review-evidence/gptpsw-r1). Both author-r1 and author-r2 handoffs were examined, including round 2b. Selected raw receipts and their source hashes are identified in public-evidence.log.

- The four full-sweep result files bind execution to f15b3a7d, each exit zero; the published suite accounting is 67/67. The 73-entry docs/idiom/fast summary must retain its explicit xvlog skip (F5).
- Yosys portability records 64 tops at 62fcd154; firmware gate shards, census and harness self-test are also at that parent. The only subsequent commit changes tb/verilator/gptp_sw/Makefile. This is ancestor evidence for unchanged artifacts, not a fresh execution of those banks at f15b3a7d. The changed closed-loop target has its own final-head receipts, including 14 killed mutants.
- The closed-loop receipt records 48 checks with two modeled peers, both slave and grandmaster roles. Its flood records 490 received stamped event messages, zero unstamped, zero egress records lost, lock at 2.9 seconds and worst subsequent offset 95 ns. Its mailbox model does not establish real GEN-crossing integrity (F1).
- The 8x8/1if held ledger passes all seven rows: acmp.last.if0=62.53484 ms against 62.62 ms. Turnaround is 0.186 ms at 1if and 0.266 ms at 2if against the 10 ms project bound; Milan permits 15 ms. The published composed maxima are 1.638/1.633 ms, within the retained 2 ms share. The 2if ledger comparison is explicitly unresolved at its owner; it is not a finding of this PR.
- The S2→S3 synthesis comparison supports a whole-design saving of 3,049 FF from narrowing. Memory debt is ledgered at 59.0, 64.0 and 62.0 RAMB36 under the owner-approved loose-BRAM rule; the non-gPTP platform entry is 58.5. These are not claims of fitting the old 56-tile budget.
- The published 8x8/1if software route receipts at 62fcd154 show WNS/WHS +0.230/+0.015 ns and +0.205/+0.013 ns, satisfying the stated #818 floor. No physical build or route was rerun by this review.

## Prior findings and pending duties

Only after the independent verdict and five-lens ledger were written were the PR body, merged discussion timeline, submitted reviews and inline review threads fetched. The timeline contains the two public review-start notices; submitted reviews and inline threads are empty. There are no prior public findings to resolve or retain at this snapshot. public-review-state.json records that public state. Issue comments provide the scope decisions and earlier author evidence; no manager source-bank execution at this exact head is claimed or inferred.

This is source review, not merge acceptance. The manager must publish this packet, obtain fixes and a new independent review at the corrected head, preserve the two-review requirement, validate the eventual current-dev merge candidate and publish its builder/native receipts. The specified live-dev tip e275d7950ef3385753e6a15d2e191ba855b171ed is distinct from this source base; this review does not validate that candidate. Hosted/act acceptance remains the manager's duty; this reviewer neither ran act nor accepted hosted contexts.

The census GPTP_SW_EN_P shape is owed to the census owner before onward merge, and the second MAC remains #962. Bench slave/grandmaster A/B qualification remains owed; the fabric plane must remain buildable until its condition is met. Physical calibration is NOT RUN, field skips are not hardware proof, and modeled oscillator/PHY behavior is not measured hardware performance. No bench-qualification or 2if-ledger finding is charged to this PR.

No prohibited full bank, hardware operation, source commit/push, GitHub write, author contact, or other-checkout edit was performed. REPORT.md and the files listed in MANIFEST.sha256 are the publishable packet; scratch is excluded.

R884-1 FINISHED
