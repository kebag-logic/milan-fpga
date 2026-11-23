[R878] POSITIVE - exact head 64117b77cb9e5c421717835b5be032b5905c447d

External source review R878-3 of issue #948 / PR #959. Tree `0c58762aaf41530ba148e99969f04bfaa3404f17`. Delta `64e55a59e09339114926c2600056c3ad8b33b9b4..64117b77cb9e5c421717835b5be032b5905c447d`: three commits, ten files, examined in whole-PR context `15168e14..64117b77`. All five technical lenses are CLEAN. No open BLOCKER, MAJOR or MINOR was found. One new wording-only RESIDUE and the existing optional S1 remain. The review-order limitation below must accompany use of this verdict.

Scope follows the [fan-out ruling](https://github.com/kebag-logic/milan-fpga/issues/948#issuecomment-7061889923), issue body/public takeover, [round-three evidence](https://github.com/kebag-logic/milan-fpga/issues/948#issuecomment-7086526466), and [#818's route floor](https://github.com/kebag-logic/milan-fpga/issues/818). Authorities examined include AGENTS.md, CONTRIBUTING.md, docs/README.md, REQUIREMENTS.md, FR-STR-03, dataplane/interface descriptions and changed module interfaces. Unchanged code retains prior verdicts; changed scheduling and its dependencies were examined again. Firmware, mailbox contracts, budget inputs and submodule gitlinks are untouched by this delta.

**Prior findings at this head**

| Finding | Severity / attributable lenses | Disposition and verification |
|---|---|---|
| R877-2-F1 | MINOR / RTL, Robustness, Tests, Docs | RESOLVED at its cause. Monitor `:362`, `:486`, `:500`, `:1047`, `:1176` widen both pending tallies, suppress all three PDU dispatch paths while urgent, and retain drain-cycle pulses. Original `plant_tap_bubbles.py` passes every FO10 check at all eight inputs. FO15 reconciles 150 accepted PDUs per input to 46 ordered deliveries and 104 drops. Three-bit idle-only and six-bit idle-only plants both fail FO15 by name. |
| R877-2-F2 | MINOR / Docs | RESOLVED. `docs/testing/TESTING.md:706` names 81, 66, 99, 60, 93, 70 and 63 octets, matching `sim_fanout.cpp:706` and remainders 1-7. These payload sizes are distinct from total Ethernet frame sizes. |
| R877-2-RS1 | RESIDUE / Tests | RESOLVED. `sim_fanout.cpp:704` points to FO14's eight-to-ten-beat cases without the stale enqueue limitation. |
| R877-2-RS2 | RESIDUE / Docs | RESOLVED. TESTING `:706` and walkthrough `:175` measure three cycles from the tap's eighth beat and name the register stages. |
| R877-2-RS3 | RESIDUE / Docs | RESOLVED in current PR: a fixed three-cycle shift register carries each beat's valid. The old round-2b receipt is historical, not the current contract. |
| R877-2-RS4 | RESIDUE / Docs | RESOLVED. PR attributes +0.017/+0.024 ns hold and stricter-floor failures to round 2b, and separately discloses current exceptions. |
| R877-2-RS5 | RESIDUE / Docs | RESOLVED. Depacketizer header `:29` and datapath README `:1893` are reflowed. |
| R878-2-R1 | RESIDUE / Docs | RESOLVED. PR role lines identify internal R877 and external R878. |
| R878-1-F1 | MINOR / Docs | Remains RESOLVED. Walkthrough diagram/rows show enqueue, completion mask and per-input STOP; `MEDIA_CLOCK_FOLLOWING.md:444` names the followed match bit. Connections are unchanged. |
| R878-1-F2 | MAJOR / RTL, Robustness, Tests, Docs; accepted scope also checked under Conformance | Remains RESOLVED. Frame-size rejection, whole-frame truncation discard and hold-only tail completion are unchanged. Current FO11-FO14 and DT1-DT5 pass, including gaps/stalls. Changed scheduling preserves ordered payload/drop reconciliation. |
| R877-1-F1 | MINOR / Tests, Robustness | Remains RESOLVED. FAN STOP/START tests and `fan_stop_plant.py` are unchanged. Current published twin/STOP receipts catch shared and one-index plants by their required names. |
| R877-1-R1 | RESIDUE / Docs | Remains RESOLVED: TESTING's missing sentence break is present. |
| R877-1-S1 | SUGGESTION / RTL | Remains IMPLEMENTED: depacketizer `:204`, `:293` explain valid/pointer qualification of unreset data. |
| R877-2-S1 | SUGGESTION / RTL, Robustness | RETAINED, optional; details below. |

**Applied lenses**

[R878] PASS Conformance - `standards-check.txt`; `KL_avtp_rx_monitor_ctx.sv:60`, `:725`; `milan_datapath.sv:3933`, `:3996`; `aecp_face.c:231` - checked primary Milan v1.2 5.3.8.10/Table 5.6 and IEEE 1722.1-2021 7.4.42.2/7.4.42.2.4 locally. Standard counters are unsigned 32-bit wrapping values. LCTX w11 is a separate vendor diagnostic, absent from GET_COUNTERS quadlets 0-11 and the 0xFFF validity mask. Its two 16-bit sums wrap independently. Six-bit pending accumulators are internal batching state; urgent drainage prevents defensive saturation from losing reachable events. Fan-out, format, STOP and media-clock behavior retain their reviewed contracts. Both selected shapes meet #818.

[R878] PASS RTL - `KL_avtp_rx_monitor_ctx.sv:356`, `:486`, `:500`, `:998`, `:1047`, `:1176`; reference `:325`; `published-fit-audit.txt` - inspected widths, reset, RAM arbitration, dispatch suppression and subtraction/addition precedence. Urgency preserves the in-service bundle and remaining mask while the counter transaction uses the shared RAM. Drain completion returns to idle without requiring another frame or output-ready edge. No new crossing exists. The reference receives the same correction, so lockstep alone cannot prove it; FO15's independent oracle and two killing plants do. The unchanged three-cycle tap contract still passes input-gap tests.

[R878] PASS Robustness - `sim_fanout.cpp:845`, `sim_depkt.cpp:465`; `control.log`, `bubbles.log`, `direct-control-{0,16}.log`, `direct-bubbles-{0,16}.log` - exercised eight-input overflow, intra-frame gaps, minimum/non-whole-beat payloads, tagged/untagged traffic, subsequent-frame recovery, masks, output stalls and held input beats. Original FO10 reconciles 30 accepted PDUs per input. FO15 exceeds the accumulator's capacity in total drops and independently grades delivery tallies. Untouched reset/STOP/malformed-frame conclusions retain prior coverage and current published regression support. This is scoped simulation evidence, not exhaustive proof over interface violations.

[R878] PASS Tests - `fanout_mutants.py:151`, `sim_fanout.cpp:845`, `sim_depkt.cpp:465`, `run_probes.py`, `run_direct.py`; public failing-first and current suite receipts - inspected stimulus-derived byte/order/index oracles, fail exits and named mutation checks. Tests-first commit precedes the RTL fix; the published prior-RTL run fails 31 FO15 checks. Independent rebuilt mutants prove widening alone is insufficient. Original bubble script was applied verbatim to its original bench with current production RTL. No assertion was weakened for a pass.

[R878] PASS Docs - TESTING `:706`, walkthrough `:175`, depacketizer header, datapath README `:1893`, `measure_test_evidence_readers.py:98`, current issue/PR and packet - checked sizes, delay origin, counter terminology, mutation inventory, route exceptions and roles. Added-source scan found no new bench label, lane name, reviewer identity, review-round or issue-comment ID. Local docs check: zero findings across 223 Markdown and 1,916 text files, 23/23 scrub controls, 4/4 routing controls. Remaining publication-tense wording is R1 below.

**Independent executions**

| Receipt | Result |
|---|---|
| `control.log` | 1,253 checks, zero failures. Each input in FO15: 150 accepts, 46 exact ordered payloads, 104 drops. |
| `bubbles.log` | Original probe: every FO10 check passes; each input totals 30. Overall exit 1: one FO4 UNSUPPORTED_FORMAT check reads 2 versus 1 because the slower feed spans two observation intervals. This known timing effect is retained, not presented as an overall pass. |
| `plant3.log`, `plant6.log` | Expected exit 1; 31 and 17 failed checks respectively, including the named FO15 conservation failure. |
| `direct-control-0.log`, `direct-control-16.log` | 375 checks, zero failures each; DT5 grades 584 whole-frame cases per lead. |
| `direct-bubbles-0.log`, `direct-bubbles-16.log` | Original direct gap probe: 374 checks, zero failures each. |
| `docs-check.log` | Zero findings. |
| `checkout-integrity.txt` | Parent 1,941 tracked blobs/modes and index match HEAD. Five initialized submodules match gitlinks and pinned bytes/index. Original clone clean. |

Portable drivers and the original bubble script are included. Four foreground-owned builds ran concurrently with four compiler jobs each, maximum 16. No heavy implementation build, shared installation, source fix, commit, push, GitHub write, hosting action or hardware operation occurred. Scoped simulator identity is in `tool-identity.txt`. Build logs preserve their content with machine paths redacted; disposable trees remain under scratch.

**Published evidence and physical fit**

The [public packet](https://github.com/kebag-logic/milan-fpga/tree/9330a4a9f596d8914d9f52ebf426147568d8b438/review-evidence/948-r1) has 656 manifest entries, including 126 author-round-three entries: all published hashes match. Its commit has no embedded cryptographic signature. This verifies content integrity at the named commit, not signer authentication. `audit_packet.py`, `packet-audit.txt`, `published-gates-audit.txt` and `published-fit-audit.txt` preserve the checks.

Paths below are relative to `author-r3/receipts/`:

- `rtl/avtp_rxmon-suite-64117b77.log.gz`: flat 97, stack 218, lockstep 116/119, context-format 96, fan-out 1,253, depacketizer 375 at each lead all pass. Campaigns catch 13 lockstep, 12 format, 4 context-format, 23 fan-out and 11 depacketizer plants, with passing controls.
- `sweep/milan_dp-64117b77-excerpt.txt.gz`: rc=0, 14,154 checks, zero in-suite failures, including completed 6/6 render mutation phase. This closes the previous interrupted-phase evidence concern. Full log is identified by hash/size, not supplied here.
- Clock receipts support 173 checks and 36 campaign cases; smaller affected suites report 548,216 checks. `twin/twin-gate-64117b77.log.gz` records zero findings, completed ordinary/map/fan-out controls and plants, both STOP plants caught by name and final rc=0.
- `gates/`: docs 104/104, lint 89 within 89, front-end zero findings, touched-top synthesis monitor 12,097/depacketizer 54,392 cells with tied-input/tap-purity passes. Separate generated AAF campaign: 164 passes and fresh results. Four ordinary-sweep field/freshness skips executed nothing.
- `rtl/dt5-plant/`: data-delay-freeze control 584/584, plant 0/584, exit 1, named whole-frame failure. This additional packet probe is not counted among the eleven repository plants.

All six route recipes name `64117b77`. `gates/source-identity.txt` records both route-source clones at that head with all ten delta files equal to candidate blobs, and identifies suite/twin clones likewise. The only functional production RTL delta is the monitor; depacketizer changes are comment reflow. Build rc=0 and image-identity agreement are recorded for all six. This supports routes of the head's RTL, not reuse of the previous monitor route. Actual routed binaries/netlists were not reproduced or independently rehashed here; published raw-artifact hashes and author source-identity receipts support those large originals.

Recipe: split 50 MHz, one interface, corresponding TDM shape, xc7a100tfgg484-2, AreaOptimized_high synthesis, ExploreArea optimization, eight implementation threads and named placement directive. No explicit seed is recorded; this is measured-route evidence, not a deterministic reroute claim.

| Shape / directive | Slow WNS/WHS ns | Fast WNS/WHS ns | LUT / FF / slices | #818 floor |
|---|---|---|---|---|
| 8x8 ExtraPostPlacementOpt, selected | +0.272 / +0.044 | +1.526 / +0.013 | 44,103 / 51,272 / 15,691 | PASS |
| 8x8 ExtraTimingOpt | +0.152 / +0.102 | +1.660 / +0.036 | 44,099 / 51,270 / 15,708 | PASS |
| 8x8 AltSpreadLogic_high | +0.102 / +0.102 | +1.660 / +0.036 | 44,072 / 51,269 / 15,646 | PASS |
| 1x1 ExtraPostPlacementOpt, selected | +0.193 / +0.102 | +1.636 / +0.036 | 32,768 / 42,805 / 13,989 | PASS |
| 1x1 ExtraTimingOpt | +0.054 / +0.102 | +1.687 / +0.036 | 32,765 / 42,804 / 14,297 | PASS |
| 1x1 AltSpreadLogic_high, unselected | +0.020 / +0.102 | +1.687 / +0.023 | 32,778 / 42,804 / 14,299 | FAIL |

Both temperatures at each corner were checked. #818 selects the best route meeting setup >= +0.030 ns and hold >= 0 at every corner; both shapes pass, no STOP. Selected 8x8's stricter both-+0.030 failure remains rc=1. Unselected 1x1 also fails the applicable floor. Neither failure is erased. BRAM is 94/79.5 tiles and DSP 13 at 8x8/1x1. Selected LUT/FF/slice deltas against archived train: +1,118/+279/-7 and +54/+177/+296. These are whole-build measurements, not causal attribution of every area change to the monitor.

**Remaining findings**

R878-3-R1 - RESIDUE - Docs - PR #959, Status and checkout/publication wording.

Authority/evidence: the PR names published head `64117b77` but says the correction is committed locally “for the manager to push” and conditions checkout on that future push. Impact: stale tense only; head, measurements, clauses and verdict are unchanged. Exact required fix: replace the local/pending-push sentence with `The correction is published on 948-rx-fanout at 64117b77cb9e5c421717835b5be032b5905c447d.` Remove the pending-push qualifier from checkout instructions. Verification: compare those lines with the published head and public round-three start notice. Docs stays clean; carry on the residue checklist.

R877-2-S1 - SUGGESTION, retained - RTL, Robustness - `KL_aaf_rx_depacketizer.sv:263`, `:403`, `:435`.

Authority/evidence: enqueue later than the fixed three-cycle contract can allocate a verdict entry after its frame's fate was recorded, leaving it unresolved. Impact: a future latency-contract violation could stop readout until reset. Current parser/monitor satisfies the contract; FO14/FAN/direct-gap tests exercise it. Optional required outcome if adopted: fail safely on late enqueue or assert the latency relationship. Verification: delay enqueue beyond the contract and require bounded drop/recovery or an explicit assertion failure. PR discloses the limitation; no lens is unclean.

**Reviewer-owned ledger**

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Primary counter clauses, GET_COUNTERS mapping, diagnostic wrap arithmetic, fan-out/STOP contract, #818 receipts | R878-3 | 64117b77cb9e5c421717835b5be032b5905c447d |
| RTL | CLEAN | Monitor urgency/dispatch/drain/reset, reference delta, frame/queue interface, route/source-identity receipts | R878-3 | 64117b77cb9e5c421717835b5be032b5905c447d |
| Robustness | CLEAN | Original FO10 bubble probe, FO15 overflow, DT1-DT5 at both leads, current STOP/twin receipts | R878-3 | 64117b77cb9e5c421717835b5be032b5905c447d |
| Tests | CLEAN | Scoreboards, two killing plants, tests-first history, published receive/datapath/twin results | R878-3 | 64117b77cb9e5c421717835b5be032b5905c447d |
| Docs | CLEAN; R1 wording residue | TESTING, walkthrough, headers/README, source-comment scan, counter description, PR/issue/packet | R878-3 | 64117b77cb9e5c421717835b5be032b5905c447d |

**Real limits and pending manager duties**

Review-order limitation: prior public finding comments were retrieved after the independent source pass, but retrieval exposed their surrounding earlier-round reports before this round's written verdict and ledger existed. This does not meet the requested written-verdict-before-other-report sequence. No other round-three report, private author material or lane scratchpad was read. The manager must decide whether this technical review can count toward the independent-review bar; this report does not waive that procedural deviation.

This is source-head review, not merge authorization or completion of the current-dev candidate. No manager source bank exists at this head; none is claimed or inferred. Source base `15168e14` was not replaced by live dev `e275d7950ef3385753e6a15d2e191ba855b171ed`. Manager duties: then-current-dev merge candidate and builder/native banks; protected hosted/act acceptance; any additional independent review required by the limitation above; final ledger, residue cleanup, explicit merge authorization and post-merge containment. Hosted jobs were not independently inspected; no skipped context counts as execution.

Full parent/processor/timing-plane/portability/builder banks and physical implementation were not rerun. Broader source-gate/route conclusions rely on published receipts. Physical calibration was NOT RUN. Simulation, route reports and field skips provide no hardware/audio proof. Original bubble probe's interval-sensitive failure stays visible; its conclusion is restricted to repaired FO10. Overload may defer PDU service and cause earlier admission-ring refusal as disclosed; tests reconcile accepted PDUs, not all offered traffic.

Only MANIFEST.sha256-listed receipts/scripts and REPORT.md are publishable. Scratch contains disposable builds/specification extracts and is excluded. Original tracked bytes/modes/index and initialized gitlinks pass verification. All foreground-owned campaigns completed.

R878-3 FINISHED
