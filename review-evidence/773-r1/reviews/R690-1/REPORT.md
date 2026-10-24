[R690] NEGATIVE - exact head 13d8f1e84920aac1dc3e76fb6406c44a744d8145

External independent review, round R690-1, issue #773 / PR #779.
Base: a032c6d6e3775f145349d5a495c1e1ad12294936.
Reviewed tree: c4df5628be0a6d6823915aa2421e1a96d724e55b.

The stamping arithmetic implements the public ruling. Two MINOR findings remain: an unconditional buffering bound excludes startup, and the required complete sweep has no successful receipt for this head. No functional RTL defect was established in the reviewed shipping shapes. All five lenses were applied independently.

Authorities examined: AGENTS.md, CONTRIBUTING.md, docs/README.md, REQUIREMENTS.md; [issue #773](https://github.com/kebag-logic/milan-fpga/issues/773), the [STOP figures](https://github.com/kebag-logic/milan-fpga/issues/773#issuecomment-6380097334), and [ruling (b)](https://github.com/kebag-logic/milan-fpga/issues/773#issuecomment-6380110812); IEEE 1722-2016 4.3.3 Equation (1), 4.3.5, 4.4.4.9, 10.7 Equation (14), 10.8; Milan v1.2 4.4.2.1, 5.3.7.6, 5.4.2.9 and 5.4.2.10.2. The standards were read directly. Interface authorities included docs/overview/ARCHITECTURE.md, docs/integration/INTEGRATION_GUIDE.md and docs/design/MEDIA_CLOCK_FOLLOWING.md. All six commits and the complete base-to-head delta were examined. Public executable evidence was examined after the independent diff pass. No private author material was used.

**R690-1-F1 — MINOR — Conformance, Docs**

- Artifact: `docs/design/MEDIA_CLOCK_FOLLOWING.md:1853`, `docs/reference/MILAN_COMPLIANCE_MATRIX.md:191`; corroborating `tb/verilator/capture_coherence/sim_dp.cpp:548` and `capture_dp.log`.
- Authority/evidence: the ruling requires the latency bound and default-offset render margin to be stated. The new prose claims a PDU arrives at most 2,038,676 ns ahead at 1x1; the matrix claims at most 2,054,392 ns across the shapes. The exact-head datapath run reports 2,059,807 ns, including DP-band-true+2/+4. These first PDUs use the live-PHC fallback before the domain grid is live. The same document acknowledges that case at lines 1871-1873, but its universal bound and queue margin exclude it. This comparison uses the document's zero-additional-transit assumption and its named datapath hand-over oracle.
- Impact: the published maximum and unconditional 513.3 us 1x1 margin are not established. This is a numerical proof claim, not wording residue. The observed case remains within 2.126 ms; no buffer overflow was observed. Using the documented queue ceiling and five later sample periods, its conservative remaining 1x1 margin is 2,656,119 - 2,059,807 - 104,167 = 492,145 ns.
- Required outcome: distinguish grid-live/frame-based bounds from startup/fallback bounds, derive the latter for both shipping shapes, and update the matrix and unconditional margin claims. Retain the true statement that the default offset fits. This finding requests no source behavior change.
- Verification: reconcile every `[HOLD]` maximum with the stated domain of its bound and recalculate last-event queue margins. Derived-only 8x8 evidence remains allowed.

**R690-1-F2 — MINOR — Conformance, Tests, Docs**

- Artifact: public evidence commit `8f1028e5a0fb979b3c6c33496655dd15059825eb`, `review-evidence/773-r1/author/receipts/round1b/final/sweep/shard-2/results.json`, `sweep/spec.json`, and `sweep/aaf_alone_13d8f1e8/`; summarized in `evidence-audit.log`.
- Authority/evidence: ruling (b), item 4 requires the complete sweep in four shards; CONTRIBUTING.md sections 2.1 and 3 require successful local gates and exact-candidate validation before merge. The published sweep at bf2d96f98a27fb1ec7143673ad714e51ab9b3862 passed 63/64 suites, with shard 2 returning 1. The sole later change fixes the AAF planting pattern; the AAF-only run at this head passes, including 8/8 controls. That verifies the isolated repair, but is not a successful complete sweep receipt for this head.
- Impact: the full-sweep acceptance item remains open. This is an evidence-completion finding, not a prediction that unchanged suites regress. Neither a planned manager run nor queued hosted workflows supplies an executed result. The PR Status section says every gate passes at this head, contradicted by its own table; that gate-verdict claim also belongs to Docs and is not wording residue.
- Required outcome: publish a successful complete four-shard sweep for the final reviewed head. A complete run on the final merge candidate can discharge this for an identical tree if both identities and tree equality are recorded; it must actually execute and pass. Correct the PR status until then. Do not describe 63/64 plus an isolated repair run as an already completed exact-head sweep.
- Verification: all shards succeed, all expected suites are accounted for, the AAF startup mutation succeeds, and receipts bind commands, head/tree, return codes and results. Re-review the completed evidence. No full bank was run by this reviewer, as instructed.

**Conformance and RTL examination.** `KL_aaf_packetizer.sv:238-266,779-785`, `KL_media_if_latency_pkg.sv:153-171`, and `milan_datapath.sv:1258-1320,1459-1531` derive the AAF estimate from SAMPLES_PER_FRAME_C and the fixed delay by ceiling division of the integration and packetizer terms. The existing stamp adder adds the lead once. No copied 166,667 ns constant controls the product path. Signed span arithmetic handles the inner TDM32 close. The raw offset bank/readback is unchanged; AAF stamps the offset as set, modulo 2^32 as 4.4.4.9 requires.

`KL_crf_tx.sv:299-318,540-546` and `milan_datapath.sv:7438-7446` add TC in the existing 64-bit sum. Offset conversion and carry are unchanged. GET_STREAM_INFO retains its existing semantics: AAF as set, CRF as applied by the pre-existing rounding path. This delta adds neither lead nor TC to the reported offset.

| Derived term | 1x1 TDM8 | 8x8 TDM32 |
|---|---:|---:|
| Marker latency | 20,964 ns | 5,308 ns |
| Capture age bound | 1,043 cycles | 1,043 cycles |
| Last-pair walk | 86 cycles | 811 cycles |
| Packetizer pipeline | 57 cycles | 60 cycles |
| AAF hand-over after crossing estimate, ready MAC | 23,851 ns | 22,755 ns |
| Fixed delay | 2 Ps | 2 Ps |
| AAF total lead | 166,667 ns | 166,667 ns |
| CRF path | 21,164 ns | 5,508 ns |
| CRF TC | 2 Ps / 41,667 ns | 1 Ps / 20,834 ns |

The 8x8 derivation includes the one LOOP pre-walk pair despite LOOPBACK_P=0, all 32 slots, the last talker's three extra context reads, and the 8-channel packet ceiling. The 104-cycle spacing between talkers exceeds unstalled shared-emitter service. Marker/write/read, capture age, walk, packetizer, event register and CRF serializer are accounted for. `bounds.log` independently reproduces the numbers. The elaboration boundary accepts exactly 125 us and refuses the next required period under the repository's error policy (`guard-*.log`).

**Arbitration and reference plane.** Examined `041b7922b`, `milan_datapath.sv:1482-1494,8707-8745,8924-8946`, `hdl/ieee17221/adp/adp_tx_arbiter.sv:100-170`, and `sw/litex/milan_soc.py:1753-1807,1861`. Removing frame-ahead waits from the rounded term preserves the ruled 23.8/22.7 us reference. A bounded wait can fit in unused spare, but Equation (1) still applies to actual ownership transfer; TUmax does not waive stalls.

The quoted 3,960/4,400 ns waits are 64-bit fabric serialization at 50 MHz, not Ethernet serialization. One maximum tagged frame including preamble and IFG occupies 12,336 ns at 1 Gbit/s, individually below all four spares: 17,816 / 18,912 ns AAF and 20,503 / 15,326 ns CRF. The MAC has a 512-beat store-and-forward buffer and its crossing, so one already-owned frame is distinct from an arbitrary ready-low interval. This does not prove unrestricted aggregate backpressure. In particular, blindly adding independent fabric-wait and wire-frame maxima would exceed the 8x8 CRF spare. The result stays scoped to the named hand-over boundary and traffic assumptions; it is not a physical launch/calibration proof.

**Robustness examination.** Constant additions introduce no state, reset, CDC or handshake change. LEAD_P/TC_P default off preserves standalone consumers. Startup fallback, acquisition phases, INTERNAL drift, low-word AAF wrap arithmetic, CRF carry and delay refusal were examined. The exact-head datapath run covers both offsets, startup, eight CRF phases per offset, drift and placed engagements. `[WIRE]` and `[HOLD]` grade startup; `[GRID]` intentionally waits nine live frames for AAF. `[PIN]` remains tied to decoded media data and slot instants, with the new whole-period lead removed. No robustness defect was established within this scope. True-clock 8x8 is derived only, not simulated.

**Independent exact-head execution.** Commands are preserved in `run_focused.py`, `run_controls.py`, `check_bounds.py`, `evidence_audit.py` and `audit_tree.py`; raw results accompany them. Independent checks ran concurrently with bounded worker counts, in disposable scratch builds.

| Check | Result | Receipt |
|---|---|---|
| Full capture_coherence datapath leg, make -j16 dp, internal build jobs 8 | 847 checks, zero failures | capture_dp.log/.rc |
| Seven new controls, --jobs 4 | 7/7 caught by their named checks | controls.log/.rc; control-01..07.json/.rc |
| Behavior suite from tests | 14 features, 406 scenarios, 1,977 steps pass | behave.log/.rc |
| Lint | 89/89, pass | lint.log/.rc |
| Rational shape arithmetic and delay boundary | Both shapes agree; 125 us accepts, next period refuses | bounds.log/.rc; guard-*.log |
| Public receipt hashes | 148 verified against publication envelope | evidence-audit.log/.rc |
| Raw source/index/gitlinks | Exact match | tree-audit.log/.rc |

The datapath run reproduces AAF margin 17,823..59,807 ns, CRF margin 20,503 ns and maximum hold 2,059,807 ns. Its clean run is the positive control for the mutations. The driver requires each named failed assertion; unrelated failure or a crash does not count.

| Control | Named failure observed |
|---|---|
| AAF lead removed | WIRE upper, GRID AAF, PIN |
| AAF delay one period short | WIRE upper, GRID AAF |
| AAF stamp 125 us late | WIRE lower, HOLD |
| CRF TC removed | WIRE upper, GRID CRF |
| CRF TC one period short | WIRE upper, GRID CRF |
| CRF stamp 125 us late | WIRE lower |
| AAF required delay beyond 125 us | Named build refusal |

The AAF pattern repair uniquely removes the offset operand and leaves the lead operand. `milan_dp/sim_nxn.cpp:8657-8877` exercises command/readback and both hand-over bounds at 2 ms, 1 ms, 2,010,000 ns and 125 us. Its period search at test clocks is weaker than a shipping-shape derivation; it is not used here as physical 8x8 proof. `media_phase/ofs_wrap.sv` intentionally leaves lead/TC off to isolate unchanged offset arithmetic; integrated coverage resides in the datapath legs.

**Published evidence and phase preservation.** [Evidence directory](https://github.com/kebag-logic/milan-fpga/tree/8f1028e5a0fb979b3c6c33496655dd15059825eb/review-evidence/773-r1). The published-hash envelope accounts for redaction; all 148 indexed receipts verify. At bf2d96f9, unchanged RTL/test inputs support synthesis 60/60, TDM8-render controls 31/31, pull-in 19 legs with zero failures and GM-step controls 23/23. These are predecessor-head receipts, not newly executed head receipts. The phase detector, aligner target and listener presentation RTL are unchanged. The live-grid 513.3/492.4 us margins follow the stated arithmetic; F1 concerns extending them to startup.

The documentation run records 44 steps: 41 successes, two named skips and an em-dash invocation failure due to base lookup. Its direct rerun against a032c6d6 passes; no-git checks have separate passing receipts. At this head the author reports lint, front-end parsing, Python idioms and docs_check passing. Exact-head implementation receipts report route-1x1 LUT +102, FF +7, SLICE -11, unchanged memories/DSP, WNS +0.040 ns and WHS +0.021 ns. WNS clears the +0.030 ns floor by 0.010 ns. Both out-of-context shape comparisons are unchanged. These are the stated recipe's results, not hardware proof.

**Documentation examination.** Changelog, design authority, compliance matrix and testing table were checked against code and receipts. No new prohibited bench-lane/reviewer/round/comment identifiers were found in added source comments. Existing provenance was not relabeled as new residue. No RESIDUE or SUGGESTION finding is raised. F1 changes a figure/proof claim and is MINOR under the owner rule.

Reviewer-owned ledger:

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN: F1, F2 | Issue ruling; cited standards; packetizer:238-266; CRF:299-318; design:1853; public sweep | R690-1, applied but not clean | 13d8f1e84920aac1dc3e76fb6406c44a744d8145 |
| RTL | CLEAN | packetizer:238-266,779-785; CRF:299-318,540-546; latency package:153-171; datapath:1258-1531,7438-7446; capture walk:1371-1445; mux/MAC bindings above | R690-1 | 13d8f1e84920aac1dc3e76fb6406c44a744d8145 |
| Robustness | CLEAN | capture_coherence/sim_dp.cpp:250-316,548-644; startup fallback; AAF wrap/CRF carry; guard-*.log; capture_dp.log | R690-1 | 13d8f1e84920aac1dc3e76fb6406c44a744d8145 |
| Tests | UNCLEAN: F2 | capture_coherence Makefile, mutants.py:269-291, sim_dp.cpp; aaf/start_mutants.py:32; milan_dp/sim_nxn.cpp:8657-8877; published sweep/campaigns; focused receipts | R690-1, applied but not clean | 13d8f1e84920aac1dc3e76fb6406c44a744d8145 |
| Docs | UNCLEAN: F1, F2 | CHANGELOG.md:47; MEDIA_CLOCK_FOLLOWING.md:1781-1890; MILAN_COMPLIANCE_MATRIX.md:191,227; TESTING.md capture_coherence row; PR Status; public evidence index/envelope | R690-1, applied but not clean | 13d8f1e84920aac1dc3e76fb6406c44a744d8145 |

Prior-finding reconciliation: after writing the independent verdict and ledger, the PR reviews, inline threads and discussion were fetched. There were zero submitted reviews, zero inline review threads and two discussion comments, both public review starts. Therefore there are no prior public review findings to resolve or retain at this snapshot. The PR body was checked then; its overall gate-pass claim corroborates F2 and adds Docs attribution without changing the verdict. `public-state.json` preserves the snapshot. No other reviewer's report was read.

Limits and pending manager duties: no full parent/processor/synthesis/builder bank, hosting replica, shared installation, hardware operation, source fix, commit, push, merge or GitHub write was performed. Physical calibration is NOT RUN. Field skips and desk passes are not hardware proof. Hosted snapshot: rtl-full/docs/rtl-fast queued, elaborate in progress; neither skipped nor merely emitted contexts are executed evidence. Hosted acceptance remains the manager's responsibility. No manager source-head bank exists or is inferred. The manager must publish final current-dev candidate identities and complete native/builder/local and hosted acceptance, resolve/re-review these findings, obtain both independent positive reviews, then perform any authorized merge and containment. This report supplies no merge authorization.

Raw tracked bytes, executable modes, index records and required submodule gitlinks match the reviewed head. Disposable builds and standard-text extractions stay under scratch/ and are not publishable. Receipt output is retained verbatim except execution-location prefixes recorded by original/published hashes in path-redactions.json. The approved compiler identity was checked before the builds and is recorded in compiler-identity.json. For portable replay, set REVIEW_VERILATOR to the approved executable, then pass a clean initialized clone path to the supplied scripts; run_controls.py additionally requires --jobs 4. Only REPORT.md and files listed in MANIFEST.sha256 belong to the publication packet.

R690-1 FINISHED
