[R878] POSITIVE - exact head 64e55a59e09339114926c2600056c3ad8b33b9b4

External independent review R878-2 of issue #948 / PR #959. Tree: `ee8f0eb03b6f360cd507678ef029970ec43afc95`. Source range: `15168e14..64e55a59`; this round judges the delta from `4ceba3d40e3b94e9bda2407e64ef906c283b63a4` and every named prior finding at its cause. All five lenses are CLEAN. No BLOCKER, MAJOR or MINOR remains from this review. One wording-only RESIDUE is recorded below.

The independent source pass and provisional ledger were written before reading the previous public findings. No other round-2 review informed this verdict. Unchanged code retains its earlier lens conclusions; changed dependencies, particularly the frame verdict and depacketizer, were examined again. No original-checkout source edits, commits, pushes, GitHub writes, author contact, hardware operations, full banks or hosting operations were performed.

Scope authorities: [the fan-out ruling](https://github.com/kebag-logic/milan-fpga/issues/948#issuecomment-7061889923), the public issue/takeover, [round-2 acceptance and evidence](https://github.com/kebag-logic/milan-fpga/issues/948#issuecomment-7075385669), [round-2b acceptance and evidence](https://github.com/kebag-logic/milan-fpga/issues/948#issuecomment-7080201967), and [PR #959's recorded scope decisions](https://github.com/kebag-logic/milan-fpga/pull/959). Repository authorities examined include AGENTS.md, CONTRIBUTING.md, docs/README.md, REQUIREMENTS.md, FR-STR-03, the architecture and integration contracts, and the module interfaces. The relevant primary Milan v1.2 and IEEE 1722-2016 clauses were checked locally; see `standards-check.txt`. This is the established v1.2 contract, not a substitution of a newer specification.

**Prior findings: disposition at this head**

| Finding | Prior severity / attributable lenses | Disposition and verification |
|---|---|---|
| R878-1-F1 | MINOR / Docs | RESOLVED. `docs/fpga/DATAPLANE_WALKTHROUGH.md:157` now shows enqueue, done/accepting mask and each stopped input removed. `docs/design/MEDIA_CLOCK_FOLLOWING.md:444` names the followed match-vector bit and followed index, retaining the highest index for diagnostics. Both match the actual datapath connections. |
| R878-1-F2 | MAJOR / RTL, Robustness, Tests, Docs; the accepted extension also requires Conformance | RESOLVED at its two causes. The monitor rejects off-size PDUs separately per input before any payload transfer. The depacketizer retains the last stored word until a hold-only tail transfers with tlast. Direct and real-stack probes were rerun, with subsequent valid-frame recovery, tagged tails and stalls. Details below. The PR explicitly records that the defect predates #948 and was found by review. |
| R877-1-F1 | MINOR / Tests, Robustness | RESOLVED. `tb/verilator/milan_dp/sim_nxn.cpp:8213` and `:8302` exercise STOP and START of each of two inputs sharing one stream. The original public probeB shared-gate plant was rerun: four failures among 4,073 checks, including both required named failures for the still-started input. The stopped input still counts FRAMES_RX and START restores delivery. |
| R877-1-R1 | RESIDUE / Docs | RESOLVED. `docs/testing/TESTING.md:706` now has the missing sentence break, “and passes. Its fan-out leg”. |
| R877-1-S1 | SUGGESTION / RTL | IMPLEMENTED. `hdl/ieee1722/aaf/KL_aaf_rx_depacketizer.sv:295` explains the unreset RAM/data registers and the reset pointers/valid flags that prevent unwritten data being consumed. The new delay stages have the corresponding qualification at `:205`. |

The manager's additional short-frame ruling is satisfied by the reviewed change. Public `receipts/probe/probe_minframe2.cpp` and `receipts/round2b/probe/minframe2-four-revisions.txt` use each revision's receive stack: the shortest observed delivered frame is 98 octets at `15168e14`, 82 at `4ceba3d4` and `e8252323`, and the Ethernet minimum at this head. These are the author's historical measurements, not new base executions by this reviewer. The current short-frame behavior was independently exercised here. The one-channel 48 kHz Base payload is 24 octets; its frames are 62 untagged and 66 tagged, excluding FCS.

**Applied lenses**

[R878] PASS Conformance - `hdl/ieee1722/avtp/KL_avtp_rx_monitor_ctx.sv:548`, `:577`, `:1083`; `hdl/milan/milan_datapath.sv:7903`; `standards-check.txt` - checked the changed acceptance against Milan v1.2 4.4.2.2, 5.3.8.7, Table 5.6 and 6.4, and IEEE 1722-2016 4.4.4.10, Table 9, 7.3.5 and I.2.4.1. The input's channel count and samples-per-frame determine its required payload size. INT16, INT24 and 32-bit encodings use two, three and four octets. The verdict also compares the received encoding with the configured encoding, so using the received encoding in the preceding multiplication does not permit an incorrect format through. An off-size PDU raises UNSUPPORTED_FORMAT, omits that input from the accepting mask, and preserves the established discarded-PDU sequence behavior. FO11 proves different frame sizes on two inputs sharing a stream. STOP remains a bitwise per-input delivery mask. No firmware, mailbox, budget-input or processor-pin change occurs in the full source range.

[R878] PASS RTL - `hdl/ieee1722/aaf/KL_aaf_rx_depacketizer.sv:158`, `:177`, `:232`, `:307`, `:400`, `:503`, `:568`, `:690`; monitor `:1083` - checked the three-cycle tap delay, valid qualification, tap-side eighth-beat attribution, same-cycle enqueue/fate updates, truncation accounting, tail retention and replay/release. The next frame cannot reach its eighth accepted beat before the previous frame's delayed end is attributed. The stored eighth beat samples `tq_r || enq_tap_w`, including a pulse arriving that cycle. `te_r` and the current allocation address distinguish an earlier pulse from a same-cycle pulse. Input gaps advance the delay in clock cycles without inventing accepted beats. Output stalls preserve data, tag and tlast, and the frame's storage is released only after its last input's pass. No new clock crossing is introduced. The 22-bit frame-size product holds the maximum 1023 x 1023 x 4 without overflow; the wire length is extended before comparison. The published synthesis and placed-route results support the changed logic, within the limits below.

[R878] PASS Robustness - `tb/verilator/avtp_rxmon/sim_depkt.cpp:311`, `:325`, `:371`, `:395`; `sim_fanout.cpp` FO8-FO14; `stack-discard.log`, `prior-depkt.log`, `depkt-gaps.log`, `fanout-gaps.log`, `probeB.log` - checked malformed size, truncated final bytes, every tail remainder, unqueued/zero-accept frames, short frames, multiple masks and inputs, back-to-back traffic, overflow/drop attribution, random and final-beat stalls, producer gaps, reset during pending replay and recovery. The independent discard probe observes every payload beat: tagged and untagged 65-octet off-format PDUs transfer zero beats, count UNSUPPORTED_FORMAT at both inputs and leave no partial payload. The following valid PDU reaches each input with exact bytes and its own boundary/tag. The original direct probe now measures 64 octets as 8 beats/1 tlast and 65 as 9 beats/1 tlast. The retained independent replay/reset probe passes 37,000 checks across 72 combinations, including long frames and timestamp lead.

[R878] PASS Tests - `tb/verilator/avtp_rxmon/depkt_mutants.py`, `fanout_mutants.py`, `Makefile`; `tb/verilator/milan_dp/fan_stop_plant.py`, `Makefile`, `sim_nxn.cpp:8302`; `published-gate-audit.txt` - inspected the independent byte/order/tag scoreboards, fail exits and named mutation checks. The new size comparison is tested beyond the identically updated lockstep reference: FO11 varies samples-per-frame between inputs; the plants remove the size comparison, substitute input 0's format, and mis-size 16/24-bit samples. The tail and short-frame causes have dedicated plants. Published failing-first receipts fail on the preceding RTL, then pass at this head. The new source stimulus matches each declared format; assertions were not weakened to accommodate an invalid stimulus. The shared-gate probe now fails the specific STOP checks it previously escaped.

[R878] PASS Docs - `docs/fpga/DATAPLANE_WALKTHROUGH.md:157`, `:173`, `:174`; `docs/design/MEDIA_CLOCK_FOLLOWING.md:444`; `docs/fpga/FPGA_DESIGN.md:269`, `:297`; `docs/testing/TESTING.md:706`; `docs/reference/REGISTER_MAP.md:2001`; PR #959 - checked changed interfaces, delay, padded tails, truncation/drop counters, tests and evidence against the implementation. The diagram's edge and media-clock field table now describe the real connections. The register description and its generator input agree. The local docs, inventory and em-dash checks pass. The added-source-comment scan found no new bench lane label, lane name, review round, reviewer ID or issue-comment ID. Test function names using “round” describe stimulus batches. One PR role-label residue remains below.

**Independent executions and raw receipts**

| Receipt | Result |
|---|---|
| `fanout.log` | 1,205 checks, zero failures; FO1-FO14 including short, mixed-input and off-format traffic. |
| `depkt-0.log`, `depkt-16.log` | 374 checks each, zero failures; 2,760 DT2 cases and 960 DT4 cases each. |
| `prior-tail.log` | Original direct 64/65-byte probe: respectively 8/9 output beats, one tlast each. |
| `stack-tail.log` | Original real-stack 65-byte stimulus: zero accepts and zero completed outputs at both bound inputs. Its old “deliver four” oracle intentionally exits 1, with 12 failures; this is retained raw and is not represented as a passing test. |
| `stack-discard.log` | Separate oracle for the manager's required discard behavior: 34/34, including zero transferred beats, per-input unsupported-format counts and next-valid-PDU recovery. |
| `prior-depkt.log` | 37,000 checks, 72 combinations, zero failures; payload, masks, timestamp lead, stalls and reset/recovery. |
| `depkt-gaps.log`, `fanout-gaps.log` | Additional producer-gap variants: 374/374 and 996/996. The depacketizer variant also retains random/final-beat consumer stalls. |
| `probeB.log`, `probeB-caught.txt` | Original shared-gate plant: expected exit 1, 4/4,073 failures. Both named surviving-input STOP checks caught; the other two are their total-output checks. |
| `docs-check.log`, `docs-inventory.log`, `em-dash.log` | Zero findings; inventory fresh; em-dash controls 339/339. |
| `checkout-integrity.txt` | Exact parent tree, 1,941 parent blobs, modes and index; required initialized submodules match their gitlinks and all pinned bytes. Original clone clean. |

Commands and adaptations are preserved in the portable `run_*.py` scripts and probe sources. `prepare_clone.py` creates the disposable clone beneath packet scratch; `run_focused.py` takes that scratch clone and runs three foreground-owned concurrent chains with at most 16 compiler jobs combined. The scoped executable's version and hash are recorded in `tool-identity.txt`. No campaign is left running.

**Public executable evidence and physical fit**

The [public evidence packet](https://github.com/kebag-logic/milan-fpga/tree/463845aade1ba97e40e11ffcf279e56925e37581/review-evidence/948-r1) was checked against all 456 `published_sha256` manifest entries, including 238 author round-2 entries: zero mismatches. The commit contains no embedded signature; this review verifies hash consistency with the named public commit and does not claim cryptographic signer authentication. `audit_evidence.py` reproduces the checks and extracts the reviewed gate/route receipts.

The following paths are relative to `author-r2/receipts/round2b/` in that packet:

- `rtl/avtp_rxmon-suite-64e55a59.log.gz`: flat, stack, context-format and N=1/N=8 lockstep pass; 21 fan-out and 11 depacketizer defects caught, plus their controls and the existing 13/12/4 campaigns.
- `sweep/milan_dp-64e55a59-excerpt.txt.gz`: 14,148 checks and zero in-suite failures before the final mutation phase; the parent run nevertheless ends `rc=124` at 7,200 seconds. `sweep/render_mutants-64e55a59.log` independently records both prebuilt clean modes returning 0 and all four rebuilt defects returning 1 with their named failures: 6/6, end-of-run recorded. This supplies the interrupted phase's evidence; it does not rewrite the sweep timeout as rc=0. The prebuilt selection is visible, while reuse of identical binaries is supported by the author's publication, not an independent binary-hash comparison here. The full 3,167,761-byte sweep log is identified by hash in the excerpt, not supplied in this packet.
- The other affected-suite receipts and summary show the eight smaller suites at 548,216 checks and zero failures; the clock suite passes its 36 cases. Four declared field/freshness skips executed nothing. The separate AAF generator campaign reports 164 pass and fresh results; the gPTP field skip remains a skip.
- `twin/twin-gate-64e55a59.log.gz`: zero twin findings, the map/ordinary twin controls and plants, zero fan-out failures, four named fan-out plant catches, and both STOP plants caught by name. These are source-head author receipts, not manager bank executions.
- `gates/`: 104/104 documentation steps, lint 89 within 89, front-end zero findings; synthesis of the two changed tops reports monitor 12,034 cells and depacketizer 54,392, with tied-input and tap-purity gates passing. This is touched-top evidence, not the full current-dev portability bank.

All six `fit/` recipes, four-corner signoffs, identity checks, utilization and hierarchy deltas were examined. Builds use the split 50 MHz, one-interface configuration, the corresponding TDM shape, AreaOptimized_high synthesis, ExploreArea optimization, the listed placement directive and eight implementation threads. No explicit placement seed is recorded; these are measured routes, not a deterministic reroute claim. Every build has `build.rc=0` and a passing image-identity statement.

| Shape / directive | Slow WNS/WHS ns | Fast WNS/WHS ns | LUT / FF / slices | Delta vs round 2, same directive |
|---|---|---|---|---|
| 8x8 ExtraPostPlacementOpt, selected | +0.339 / +0.060 | +1.636 / +0.017 | 45,161 / 51,215 / 15,706 | +1,103 / +80 / +191 |
| 8x8 ExtraTimingOpt | +0.174 / +0.051 | +1.641 / +0.024 | 45,113 / 51,213 / 15,131 | +1,357 / +81 / +30 |
| 8x8 AltSpreadLogic_high | +0.114 / +0.100 | +1.641 / +0.036 | 45,164 / 51,214 / 15,130 | +1,373 / +80 / +40 |
| 1x1 ExtraPostPlacementOpt | +0.046 / +0.102 | +1.641 / +0.036 | 32,870 / 42,838 / 13,746 | +253 / +170 / +302 |
| 1x1 ExtraTimingOpt | +0.115 / +0.102 | +1.687 / +0.036 | 32,920 / 42,842 / 14,217 | +270 / +172 / -78 |
| 1x1 AltSpreadLogic_high, selected | +0.139 / +0.102 | +1.687 / +0.036 | 32,918 / 42,843 / 14,216 | +268 / +173 / -88 |

Both 0 C and 85 C results were checked. All meet #818's WNS >= +0.030 ns and WHS >= 0; no STOP is triggered. Some raw signoff receipts return 1 for the separately tested stricter both-+0.030 threshold. Those return codes remain unchanged and do not contradict the applicable #818 floor. BRAM is 94 tiles at 8x8 and 79.5 at 1x1; DSP count is 13. The depacketizer's round-2b increment is +80 FF at each build, +29..40 LUT at 8x8 and +75..80 at 1x1. Larger total LUT movements are present in unchanged hierarchies, including control and timing-plane logic. The hierarchy evidence supports their location, not a causal claim that thread count alone explains them. No RTL outside the depacketizer changes from `e8252323` to this head. These receipts are not hardware calibration or a physical audio proof.

**Remaining finding**

R878-2-R1 - RESIDUE - Docs - PR #959, “Linked Issue / roles”.

Authority/evidence: the body still says internal and external reviewers are `[R<n>] (to be assigned)`, while its public review-start comments assign R877 and R878. Impact: stale role wording only; the public assignment already exists and no acceptance, measurement, code, test, clause claim or privacy rule changes. Exact required wording: `Internal cleared-context reviewer: [R877]` and `External reviewer: [R878]`. Verification: compare the edited two lines with the two public review-start notices. This does not make a lens unclean; the manager may carry it on the residue checklist. No new suggestions are outstanding.

**Reviewer-owned completion ledger**

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Monitor frame-size verdict; bitwise STOP mask; primary format/STOP clauses; scope rulings; FO11/FO14 and discard receipts | R878-2 | 64e55a59e09339114926c2600056c3ad8b33b9b4 |
| RTL | CLEAN | Depacketizer delay/attribution/queues/tail; monitor product and verdict; replay/reset probe; synthesis and route receipts | R878-2 | 64e55a59e09339114926c2600056c3ad8b33b9b4 |
| Robustness | CLEAN | DT1-DT4, FO8-FO14; direct/stack tail, discard, gaps, stalls, reset and shared-STOP probes | R878-2 | 64e55a59e09339114926c2600056c3ad8b33b9b4 |
| Tests | CLEAN | Scoreboards and new mutation/STOP recipes; original probeB rerun; failing-first and exact-head published gate receipts | R878-2 | 64e55a59e09339114926c2600056c3ad8b33b9b4 |
| Docs | CLEAN, R1 wording residue only | Walkthrough diagram/rows, media-clock table, FPGA_DESIGN, TESTING, register description, PR and issue evidence, local docs checks | R878-2 | 64e55a59e09339114926c2600056c3ad8b33b9b4 |

**Real limits and pending manager duties**

This verdict is source-head review, not merge authorization or completion of the current-dev candidate. No manager source bank exists at this head and none is claimed or inferred. The source base remains `15168e14`; live dev `e275d7950ef3385753e6a15d2e191ba855b171ed` was not substituted for it. The manager owns the then-current-dev merge candidate, builder/native banks, protected hosted/act acceptance, receipt publication, the independent second verdict, the final ledger, explicit merge authorization and post-merge containment. Hosted jobs were not independently inspected in this round; no skipped hosted context is counted as execution.

Full parent, processor, timing-plane, builder and portability banks were not run here. Route, full-suite, twin and mutation-bank conclusions beyond the focused reruns rely on the identified published receipts. Physical calibration was NOT RUN. Field skips and simulation passes provide no hardware proof; the shared-stream bench case remains a manager duty. USER/reserved sample-size semantics remain outside advertised formats. The new three-cycle contract depends on the parser/monitor registering and is explicitly documented and mutation-tested.

Only MANIFEST.sha256-listed files and this report are for publication. Disposable clones, builds, generated probe copies and specification extracts are under scratch and are excluded. Final original-checkout byte/mode/index and required-gitlink checks pass. All foreground-owned commands have completed.

R878-2 FINISHED
