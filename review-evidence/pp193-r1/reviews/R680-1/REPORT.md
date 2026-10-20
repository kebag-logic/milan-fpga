[R680] NEGATIVE - exact head 6ddfcda4c3170b8f463c8623833f7541ca8c1faf

The ordinary shared-stream cases pass, but the fix does not maintain one applicant identity when a parked Leave's StreamID becomes wanted by another sink. A complete SRP datapath probe emits two VectorAttributes for that value, including Lv while the current sink declares Ready. One index order leaves the peer unregistered. F1 is MAJOR; F2 and F4 are MINOR documentation findings. F3 is wording-only RESIDUE. All five lenses were applied independently.

Reviewed tree: `45faa5d3bd449cc0d8f8bee77f186d5e0c73022c`. Base: `21601694880efdfc4be3028afa3525fbc8f29c03`. The three author commits end at `788425db609204234282ea655be2452649622cba`; the reviewed merge also contains processor main `08023123ae2df5d802d20a9bb22cd063942845cd` (#192). No source fixes, commits, GitHub writes, or other checkout edits were made.

Reconstruction followed the supplied AGENTS instruction, absence of repository AGENTS.md/CONTRIBUTING.md, `docs/README.md`, the frozen issue body and public decisions, architecture/interface authorities, full diff/history, then public executable evidence. The [assignment](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/193#issuecomment-6289596705), [STOP ruling](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/193#issuecomment-6290012163), and [manager answers](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/193#issuecomment-6299223806) were read in full. Supporting authorities included issues #188/#189, `docs/00_MILAN_COMPLIANCE_REVIEW.md` (REQ-ACMP-018/022 and REQ-SRP-001…006), architecture 02/07/10, and `hdl/README.md`.

**F1 — MAJOR — Conformance, RTL, Robustness, Tests. Parked and live applicants can transmit the same value independently.**

- Location: `hdl/srp/KL_srp_listener_fsm.sv:568`, `:574`, `:784`, `:925`; uncovered intersection of the #188 and #193 tests.
- Cause: `mbr_w` excludes every parked applicant, and `same_w` groups only matcher StreamIDs. A pending applicant for a parked StreamID is therefore invisible to another sink that declares that value. Both remain eligible for the transmit walk.
- Reproduction: register stream A on sink 1 and let its applicant reach QA; withdraw sink 1 and settle it on B before the next transmission, parking A's owed Leave; settle sink 0 on A and register its Talker Advertise before that transmission. Sink 0 reports Ready and its Talker registered. The next MRPDU carries New Ready for A followed by Lv Ready for A. Reversing the two indices carries Lv followed by New instead; it still violates uniqueness and causes a deregistration during processing.
- Raw wire, higher-index parked slot (47 bytes):

```
01 80 c2 00 00 0e 0a 0b 0c 0d 0e 0f 22 ea 00
03 08 00 1a
00 01 11 22 33 44 55 66 00 01 00 80
00 01 11 22 33 44 55 66 00 01 b4 80
00 00 00 00
```

The repeated FirstValue is `1122334455660001`; `00 80` encodes New/Ready and `b4 80` Lv/Ready. The independent parser sees two values, one Lv, and a final peer state of MT, while the current sink's declaration remains Ready. Both the FSM-interface probe and the decoder/FSM/encoder/slot-pool probe fail in both index orders: [FSM receipt](parked-probe.log), [wire receipt](parked-wire-probe.log). Inputs use ordinary public control/receive faces; no internal-state forcing or RTL edit is involved.

Authority: IEEE 802.1Q-2018 §10.7.7, the §35.2.6 NOTE, and §35.1.2.2; the frozen owner-election ruling; Milan §4.2.7.2.2's immediate deregistration on Lv. This is an incomplete fix of the one-applicant invariant, not a claim that the parked-value problem first appeared in these commits.

Impact: a newly wanted stream can lose reservation until its next declaration, and one MRPDU contains conflicting declarations for one attribute value.

Required outcome: preserve a single applicant identity across live and parked values. Renewed demand for the parked value must not coexist with a stale outgoing Lv. Preserve the genuine last-declarer #188 obligations when no other sink declares the old value. Add committed coverage of both index orders, byte-exact uniqueness and uninterrupted peer registration, with named KILLED controls.

Verification: run `run-parked-probe.py` and `run-parked-wire-probe.py` against the candidate after adapting their explicit revision guard; require one value, zero Lv, peer IN while the new sink declares. Retain passing normal handover, type-sum, and owed-Leave controls.

**F2 — MINOR — Docs. The PR's accepted area result omits its measured sink count.**

Artifact: [PR #198 body](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/pull/198), Behaviour paragraph beginning “In the parent's out-of-context synthesis”. The manager answer explicitly requires the OOC figure **with its sink count**, plus a 1x1 figure only if measured.

The numerical delta is accurate: public OOC receipts give 56,501 → 57,538 LUT and 26,332 → 26,382 FF; LUTRAM/RAM/DSP/carry are unchanged. The published invocation is `KL_pp_shadow` without a shape override; its public defaults are `N_STREAM_IN_P=8`, `N_STREAM_OUT_P=8` (`public-KL_pp_shadow.sv:195`, `public-run_ooc.sh:23`, `public-env-parent.sh`). The PR does not state that measured shape.

Impact: readers cannot distinguish the accepted eight-sink cost from the shipped 1x1 cost. Required outcome: add the verified input/output shape beside the measurement and say the 1x1 figure was not measured in this packet. No new synthesis is required for this finding. Verification: compare the corrected PR wording against the invocation/defaults and both OOC receipts. This is measurement provenance, so it is not wording-only RESIDUE.

**F3 — RESIDUE — Docs. New source comments contain bench labels.**

Locations: `tb/srp_top/sim_main.cpp:2996` (`SW.`) and `:3110` (`SW3:`). These are new instances in the reviewed delta, contrary to the owner's 2026-10-15 source-comment rule. Existing labels, including the already-present `G7c` label, are not newly attributed here.

Exact fix: replace `// ==== SW. sinks on one stream share one Listener declaration (#193) =====` with `// Sinks on one stream share one Listener declaration (issue #193).`; remove the `SW3: ` prefix from the comment at line 3110. Keep test assertion identifiers and findings-page labels unchanged. Impact is wording-only; verification is a diff scan of new source comments. This does not make any lens unclean and belongs on the residue checklist.

**F4 — MINOR — Docs, Conformance. Two new test comments cite FailureInformation as authority for the Listener type sum.**

Locations: `tb/srp_stream_fsms/sim_main.cpp:1592` and `tb/srp_top/sim_main.cpp:3112`. Both attach §35.2.2.8.7 to the Ready + AskingFailed = ReadyFailed claim. That clause concerns FailureInformation, as documented in [IEEE maintenance material](https://www.ieee802.org/1/files/public/docs2015/cc-cgunther-maint-150-0315-v03.pdf). The frozen acceptance and the correctly updated architecture at `docs/architecture/10_srp_engine.md:631` instead identify §35.1.2.2 and Table 35-14 of §35.2.4.4.3.

Impact: the new tests' conformance rationale points to the wrong authority even though their expected FourPacked value is correct. Required outcome: replace `§35.2.2.8.7` in these two comments with `§35.1.2.2; §35.2.4.4.3, Table 35-14`, retaining §35.2.6 for the in-place change. Verification: inspect the corrected citations against the frozen requirement and architecture. The correction changes a clause claim, so the owner's definition excludes RESIDUE. See [authority notes](clause-authorities.txt).

**Reviewer-owned lens ledger**

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN — F1, F4 | #193 frozen body/rulings; #188/#189; REQ-ACMP-018/022, REQ-SRP-005; architecture 10 §6.4; normal and parked-value packet traces; type-sum citations | R680-1 | 6ddfcda4c3170b8f463c8623833f7541ca8c1faf |
| RTL | UNCLEAN — F1 | full diff/history; listener owner_map, app_arb, handover, park and walk; encoder repeated-value handling; per-sink registrar/output paths; merged #192 wiring | R680-1 | 6ddfcda4c3170b8f463c8623833f7541ca8c1faf |
| Robustness | UNCLEAN — F1 | both unbind orders, three sinks, rider rebind, mid-walk handover, consecutive controls; 12 additional broadcast/control/tx collisions; parked-value reuse in both index orders | R680-1 | 6ddfcda4c3170b8f463c8623833f7541ca8c1faf |
| Tests | UNCLEAN — F1 | independent table model, wire builder/parser and peer registrar; 1,403 + 5 focused checks; 21 selected mutation controls; new failure reproductions; public merged notification receipts | R680-1 | 6ddfcda4c3170b8f463c8623833f7541ca8c1faf |
| Docs | UNCLEAN — F2, F4 | docs/README conventions; architecture 02/07/10; test READMEs; PR body; public area receipts and measured-shape provenance; source-comment delta | R680-1 | 6ddfcda4c3170b8f463c8623833f7541ca8c1faf |

**Positive evidence and its limits**

| Check | Evidence and result |
|---|---|
| Normal ownership, quiet riders, both teardown orders, three sinks, rebind, type sum, walk mark | Exact-head `srp_stream_fsms`: 1,403 PASS, 0 FAIL; [receipt](srp_stream_fsms-suite.log). Tests use an independent Table 10-3 model. |
| Normal one-vector wire encoding, peer registration, ReadyFailed | Exact-head `srp_top share`: 5 PASS, 0 FAIL; [receipt](srp_top-share.log). The test compares complete frames against its independent builder; [35-byte Ready and ReadyFailed captures](wire-witness.log) preserve the passing bytes. |
| Same-clock control/handover with periodic, received Listener LeaveAll, and tx opportunity | [Additional probe](handover-pairs.log): 12 PASS. A disposable fault drops transferred deferred broadcasts: [control](handover-control.log), 9 named failures, KILLED. A second [Join-message fault](handover-join-control.log) kills all 12 checks. |
| New controls and re-anchored #188 controls | [Scoped campaign](controls.log): 3 positive runs plus 27 arm trials, 30/30 PASS; all 21 distinct selected controls KILLED, including all 12 new controls and all 9 re-anchored controls. Walk arms cover 1x1, 2x2, 3x5, 9x9. |
| Registrar, EVT_TK_* and GET_RX_STATE remain per sink | Registrar plane unchanged in the author delta; own `dcl_r` is exported per sink while only the wire uses the OR sum. Existing per-sink matcher/registration checks pass. ACMP/event-router read paths were inspected; no independent full processor run is claimed. |
| No interface/register-map expansion | Listener and processor-top port/parameter declaration tokens match base; architecture 07 unchanged. See [scope receipt](scope-integrity.txt). The #192 merge removes an internal notification signal, not a processor-top port. |
| Published broader source validation | Public receipts at 67b90c17 report 1,030,284 suite checks and 196/196 SRP campaign checks, coverage 113/113. SRP RTL and both SRP test directories are byte-identical from that revision to this exact head. At 788425db the relocated FailureInformation control is detected; public scratch-merge receipts report 10,721 processor-top checks and all 23 notification controls detected. These are author receipts, with their recorded revisions, not a manager source bank. |

The [public evidence tree](https://github.com/kebag-logic/milan-fpga/tree/f4be75344d6ea8267f5fcd02e3644cd403066c04/review-evidence/pp193-r1) supplied executable receipts only; no private author handoff or other reviewer's report was used. All 103 selected downloaded receipts match their published Git blobs ([audit](evidence-integrity.txt)). The earlier equivalent FailureInformation mutant at 67b90c17 is explicitly superseded by the relocated control at 788425db and its passing scratch-merge campaign.

The independent verdict and five-lens ledger were written before the prior-findings audit. The subsequent public query found two review-start comments, zero submitted reviews, and zero inline review comments; therefore no prior public FINDINGS were available to retain or resolve ([audit](prior-findings-audit.txt)).

Exact-head hosted execution was inspected separately. At the recorded snapshot, both workflow runs had completed successful documentation and portability jobs, while suite jobs were still in progress. No skipped or pending context is counted as executed proof; no overall hosted acceptance is claimed. See [timestamped status](hosted-summary.txt). The manager owns hosted/act acceptance.

**Limits, integrity, and pending manager duties**

This review ran focused SRP suites and disposable probes only. No full processor/parent/gPTP/portability/builder bank, hardware, physical calibration, or routing run was executed. Physical calibration is NOT RUN; field skips are not hardware proof. The full IEEE/Milan publication corpus was not independently re-audited: the frozen public requirements and repository interface authorities govern this review, with public IEEE material used to check the citation defect.

All disposable trees and builds are under `scratch/`, excluded from publication. Independent builds ran concurrently with separate logs/return-code receipts, using at most 16 build workers; every command remained foreground-owned and was reaped before completion. No heavy physical-design build was run.

The isolated source checkout never needed restoration: all probes used archived copies. Final byte/mode/index verification checks all 692 tracked blobs, the exact HEAD/tree, and a clean working tree. This processor tree contains zero gitlinks, so there are no nested required submodule pins to restore. See [integrity receipt](source-integrity.txt) and [tracked inventory](tracked-blobs.txt).

The manager must obtain fixes and independent re-review for open findings, carry F3 on the residue checklist, and validate the final current-dev merge candidate with the builder and native banks at the merge turn. Source base 21601694 and live dev `78ca9bdf104819265588726bce4322696c38b8c2` are distinct contexts. No manager source bank exists at this exact head and none is inferred. Publish the final candidate receipts on the PR; check the shipped route-1x1 resource result at adoption. Accepted OOC area is not reopened by this review.

Collection scripts record the child build/test return code in the corresponding `.rc` file; expected failing probes are not passing tests. Portable entry scripts accept the isolated clone path as their first argument and keep output beside themselves. `MANIFEST.sha256` lists every publishable receipt, script, probe source and supporting artifact with paths relative to this packet. `scratch/` is never published.

R680-1 FINISHED
