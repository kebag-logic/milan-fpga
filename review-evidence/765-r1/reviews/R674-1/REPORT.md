[R674] POSITIVE - exact head 75db4b57cff47bb614d14dead084649a4c2aa2a3

External independent review, round R674-1, issue #765 / PR #769. Tree: `f974f88ec16ad996db74419f368fd247f6883813`. All five lenses were applied. No BLOCKER, MAJOR or MINOR finding remains from this review. One wording-only RESIDUE is recorded below. This is a source review verdict, not merge authorization or hardware qualification.

The review was reconstructed from the repository contract and documentation index, [issue #765](https://github.com/kebag-logic/milan-fpga/issues/765), its [STOP ruling](https://github.com/kebag-logic/milan-fpga/issues/765#issuecomment-6268149013), and its [round-1c assignment](https://github.com/kebag-logic/milan-fpga/issues/765#issuecomment-6292906653). The normative checks used Milan v1.2 4.4.2.2, 5.3.8.10 Table 5.6, 5.4.2.25 Table 5.16, 6.4 and Table 6.2, plus IEEE 1722-2016 7.3 and I.2.4/I.2.4.1. The local specification copies were read directly; their contents are not redistributed.

The requested `4191b098..75db4b57` diff and history were examined. Comparison with merged dev `78ca9bdf104819265588726bce4322696c38b8c2` separates the #765 changes from the inherited #762 and #763 changes. `cc71db3a`, `2f33a9ce` and `4605409b` remain ancestors. Merge `7f84892a` has parents `4605409b` and `78ca9bdf`; the final commit adapts the stimulus without changing the stopped-input counter expectations.

Prior-findings reconciliation: after the independent diff pass and writing this review's own verdict and ledger, the public PR surfaces were checked again. They contain two review-start comments, zero submitted reviews and zero inline review comments. There are no prior public review findings on this PR to resolve or retain. No other reviewer's report was read.

[R674] PASS Conformance - `hdl/ieee1722/avtp/KL_avtp_rx_monitor_ctx.sv:497`, `hdl/ieee1722/crf/KL_crf_rx.sv:323` - current-format rejection matches the assigned clauses.

The AAF comparison reads all ten channel bits: PDU `fsh[49:40]` against current format `[31:22]`. Subtype, encoding, nominal rate, bit depth and sparse-mode checks remain. Zero channels remain rejected. IEEE I.2.4 requires `ut=0` for a current format; advertising a family does not authorize accepting a different current channel count. `M_PDEC_S` rejects before the accept pulse, channel shadow, sequence state and accepted-PDU events update. The interval event machinery counts UNSUPPORTED_FORMAT. The stack harness observes both accept verdicts and depacketizer output.

CRF matching now depends on frame pulse, enable and stream identity; subtype belongs in `w_fmt_ok`. A non-CRF subtype therefore sets the unsupported-format interval flag, without accepting a PDU, refreshing the timeout, advancing sequence/rate history, or immediately dropping an established lock. The parser at `avtp_stream_parser.sv:183-208` supplies only admitted stream subtypes. The integration connects its raw parse pulse at `milan_datapath.sv:5871`.

[R674] PASS RTL - `KL_avtp_rx_monitor_ctx.sv:530-1216`, `KL_crf_rx.sv:339-650`, `hdl/milan/milan_datapath.sv:6308` - state logic and stopped-input wiring are retained.

The source audit proves each receiver's module declaration and ports unchanged relative to merged dev. Everything downstream of the AAF format comparator and CRF format comparator is byte-identical to that dev version. The entire `milan_datapath.sv` is byte-identical, including `.stopped_i(acmpl_stopped_v_w[N_STREAMS-1:0])`. Thus #762's silence-expiry and accepted-gap rules were preserved, not reimplemented. A format reject cannot enter either receiver's accepted-gap interruption path. An eventual real silence timeout remains a distinct event.

The #765 delta adds combinational comparisons, with no new state, reset, CDC, port, parameter, configuration, submodule pin or CSR-decode change. REGISTER_MAP changes describe the existing format-error field; its address and bit allocation do not change. The broader stacked diff includes #762's already-merged stopped input port, which is not a #765 interface addition.

The published route receipt records 49,857 LUT against 49,613, or +244 within the 500 tolerance; FF 52,291, slices 15,738, RAMB36/RAMB18 74/25 and DSP 14. WNS is +0.137 ns and WHS +0.024 ns, with all 99,152 routable nets routed and zero routing errors. These are inspected author measurements under the recorded route-1x1 recipe, not measurements rerun by this reviewer. The earlier +545 STOP was not accepted or used to re-record the baseline.

[R674] PASS Robustness - `tb/verilator/avtp_rxmon/sim_main_nx.cpp:902`, `tb/verilator/crf_rx/sim_main.cpp:1516`, `crf-boundaries.log` - wrong format, recovery, foreign identity and stopped-state behavior checked.

The AAF cases exercise matching 8-channel traffic, 2 versus 8 channels, 264 versus 8 channels, changing the LCTX current format, stream 0's independent `fmt0_i` source, rejected-payload suppression and sequence continuity after a reject. Existing reset/queue and stopped-input boundary tests remain in the public sweep evidence.

An additional disposable CRF probe exercises all seven parser-admitted non-CRF subtypes (0, 1, 2, 3, 5, 6, 7), each while started and stopped. Each rejected PDU deliberately carries a sequence gap of 17 and otherwise valid CRF fields, so the subtype term must reject it. The probe checks no interruption, no acceptance, retained lock, one format-error interval and subsequent sequence continuity. It passes 17,694 checks with zero failures. Existing unit checks also cover disabled/foreign streams, silence, STOP/START edges and reset.

[R674] PASS Tests - `tb/verilator/avtp_rxmon/format_mutants.py:42`, `tb/verilator/crf_rx/mutants.py:69`, `tb/verilator/milan_dp/sim_nxn.cpp:6761`, published `round1c/dp762-mutants/` - named defects are detected.

Independent execution used the verified scoped compiler identity, disposable source archives and at most sixteen compiler workers. Both campaigns ran concurrently in a foreground-owned process. No repository source was edited.

| Reviewer execution | Result | Receipt |
|---|---|---|
| AAF format campaign | Clean control and five mutants: 6/6 | `aaf-format-mutants.log`, `.rc` |
| CRF receiver campaign | Three controls and eighteen mutants: 21/21 | `crf-mutants.log`, `.rc` |
| Additional CRF subtype/STOP probe | 17,694 checks, zero failures | `crf-boundaries.log`, `.rc` |
| Source and public-evidence audit | PASS | `evidence-audit.log` |
| Raw checkout/index/submodule verification | PASS | `tree-integrity.log` |

The AAF mutants respectively restore the family-only compare, truncate the high channel bits, invert matching, fix the current count at eight, and suppress stream 0's channel-word load. Each fails its named UF check. The CRF `aaf_ignored`, `aaf_accepted` and `crf_rejected` mutants fail FMT-b3, FMT-b1 and FMT-a1 respectively. Compiler failures and abnormal exits do not count as catches.

The eleven earlier datapath stimulus adaptations preserve their assertions. `sim_main.cpp` and `sim_prune.cpp` derive stream 0's channel count from the selected shape header; `sim_nxn.cpp` uses GET_STREAM_FORMAT for input 0 and the harness-written LCTX format for other inputs. The counter and unbind generators adjust payload length consistently. The prune leg explicitly retains padding for the pre-existing short-frame limitation.

The final [762-DP] adaptation uses `rx_chans(0)` and `max(400, aaf_bytes(ch0))`; its STOP/START, lock, sequence and interruption expectations are unchanged. Published receipts show the meaningful stopped-gap SEQ_NUM_MISMATCH +1 and stopped-silence MEDIA_UNLOCKED +1, with STREAM_INTERRUPTED +0; after START, MEDIA_LOCKED, SEQ_NUM_MISMATCH and STREAM_INTERRUPTED each move +1.

The published wiring campaign contains clean controls of 201/0 on `obj_dynmap` and 1983/0 on `obj_nxn4c`, plus three caught plants per shape. Tie-zero and the shifted sink slice fail the stopped gap and silence checks; the bound-level plant fails the started-gap check. The three elaborated-parameter lines hash to `d2094321fbb6f594ec13bbc5332fa7f2a284a663700daf5605f08e908eaf5e6f` in all four dynmap runs. The published nxn4c files are 200-line tails: they verify failure totals, while the driver log and SUMMARY.tsv preserve the named failure sets. No independent datapath rebuild or wiring mutation run is claimed here.

[R674] PASS Docs - `docs/reference/FR_NFR.md:172,271`, `docs/reference/MILAN_COMPLIANCE_MATRIX.md:190`, `docs/reference/REGISTER_MAP.md:861`, `docs/design/MEDIA_CLOCK_FOLLOWING.md:315,458`, `docs/testing/TESTING.md:614,625` - changed behavior and test boundaries are documented.

FR-STR-03 explicitly requires count and discard, and the live compliance row replaces the family-only claim without rewriting the archived v1 evidence. The source comment gives the current Milan/IEEE basis. The flat monitor's deliberate difference and the lockstep reference's copied comparator are disclosed; the independent UF oracle and mutants establish the new behavior. The source-comment delta introduces no bench lane label, review-round identifier, reviewer identity or issue-comment ID. Inherited instances outside the delta remain outside this review's wording finding.

Finding R674-1-RES1: RESIDUE; lens Docs; artifact [PR #769 body](https://github.com/kebag-logic/milan-fpga/pull/769), Contents list.

- Authority/evidence: CONTRIBUTING.md section 6.1 prohibits newly written U+2014. Eight Contents entries in the PR body use that separator.
- Impact: wording-only house-style residue. No measurement, clause interpretation, test, code, generated artifact, privacy rule or verdict changes.
- Required outcome: replace the ` — ` separator in each of the eight Contents entries with ` - `, keeping labels, links and descriptions unchanged.
- Verification: the PR body contains no U+2014. The manager can carry this exact edit on the residue checklist; it does not leave Docs unclean.

Reviewer-owned completion ledger:

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Receiver comparators and reject paths; Milan/IEEE clauses; FR-STR-03; UF/FMT checks | R674-1 | 75db4b57cff47bb614d14dead084649a4c2aa2a3 |
| RTL | CLEAN | Both receiver interfaces and state logic; datapath stopped input; CSR/config/gitlink diff; route receipt | R674-1 | 75db4b57cff47bb614d14dead084649a4c2aa2a3 |
| Robustness | CLEAN | UF high-bit/current-format/recovery cases; CRF subtype/STOP probe; reset and boundary evidence | R674-1 | 75db4b57cff47bb614d14dead084649a4c2aa2a3 |
| Tests | CLEAN | Both executed mutation campaigns; eleven stimulus adaptations; [762-DP] source, driver and receipts | R674-1 | 75db4b57cff47bb614d14dead084649a4c2aa2a3 |
| Docs | CLEAN | FR_NFR, compliance matrix, register map, media-clock design, TESTING, datapath README and PR body; wording residue only | R674-1 | 75db4b57cff47bb614d14dead084649a4c2aa2a3 |

Evidence attribution and limits:

- The [public author receipt set](https://github.com/kebag-logic/milan-fpga/tree/94c54c2b87397c78f43c5cad7a7778660cf9e7be/review-evidence/765-r1/author/receipts/round1c) supplies the full source-head gates. All 873 extracted receipt files, including their index, match the published manifest hashes. Hash equality establishes publication integrity, not independent execution of every gate.
- The two sweep receipts total 63 suites and 2,187,823 checks, zero failures/timeouts. The sweep itself declares four absent-generator field/freshness skips; those skipped arms ran nothing. A separate exact-head field campaign records AAF/AVTP 164/0 and gPTP 677/0 with freshness checks.
- The author also publishes 58/58 synthesis-portability results, xvlog zero findings, 32 static/docs gates, unbind mutations and the builder union. The builder records 103 gates exactly once but explicitly excludes gate 11's absent historical report calibration arm. Physical calibration: NOT RUN. These gates and simulated field campaigns provide no hardware proof.
- There is no manager source bank at this head, and none is inferred. The manager owns hosted/local-workflow acceptance. This review does not treat skipped hosted contexts as executed jobs and makes no independent hosted-gate acceptance claim.
- Full parent, processor-native, builder, synthesis and routing banks were not rerun by this reviewer. Hardware was not used. The existing short-frame depacketizer timing limitation, nonzero inputs' LCTX-only current-format path, absent samples-per-frame comparison and flat test-instrument difference are disclosed public scope limits; this verdict does not certify those broader behaviors.
- The manager still must construct and validate the final merge candidate against current dev, publish its builder/native-bank receipts, reconcile required hosted/local-workflow results, obtain the other independent verdict, resolve the wording checklist, obtain merge authorization, and perform post-merge containment before closing the issue.

Reproduction: run `run-focused.py <clone> <packet> <scoped-compiler>`, then `run-boundaries.py <packet>`. `audit-evidence.py <clone> <packet>` expects the specified public evidence tree extracted beneath `scratch/`; `verify-tree.py <clone>` hashes every tracked blob and checks modes, stage-0 index entries and populated submodule pins. Compiler identity is in `compiler-identity.log`. Disposable builds and specification text remain under `scratch/`, excluded from publication. The optional legacy `external` checkout remains uninitialized; its gitlink is verified. All five populated submodules have exact pinned bytes and index entries.

R674-1 FINISHED
