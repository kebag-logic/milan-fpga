[A605]

# Lane 726 handoff

Status: Round 3 REVIEW READY for independent re-review.
Final local head: `e893e4d13d99eb5ba00745f0f5cf74ee847972c2`.
Base: `c6bd08c6f52632c6d33d834ce842ac3cf63f29cc`.
Branch: `726-stream-counters`; review object: PR #729.
Round 3 starts at published head `37944f8ac9d1a2212a3a32f36d921434ea0cbdeb`.
Its five commits remain local; this resume performs no push or PR edit.
Executor: [A605]. Independent reviewers: [R628] and [R629].
Earlier sections retain historical evidence. The Round 3 section below gives
current dispositions, final receipts and the remaining acceptance limits.

## Authority and scope

Issue #726, assignment 6125784157, and rulings 6125741685 and 6126028604
were read in full. The second ruling resumes the parent lane and preserves
the processor scheduler. IEEE 1722.1-2021 7.4.42.2.5, Tables 7.157/7.159,
define packet totals; Milan Table 5.4 supplies talker-start reset and
5.4.5.2 Table 5.22 supplies notification spacing.
The original STOP packet and isolated scheduler reproduction in this directory
are retained as historical evidence; the second ruling supersedes that blocker.

The origin URL and initial head matched the assignment. No submodule source
or gitlink changed. No hardware, bench, flashing, push, PR edit, merge or rebase
operation occurred in the author execution recorded here. The reference-peer reset comparison, physical link cadence
and controller display remain merge-turn work. This packet is evidence for
review, not a claim that the repository's complete merge bar is satisfied.

## Round 1 changed files

Line numbers in this section refer to the Round 1 head.

| File:line | Change and purpose |
|---|---|
| `hdl/ieee1722/avtp/KL_talker_diag_ctx.sv:207` | Increment FRAMES_TX for every emitted AVTPDU; start-edge reset at line 248 preserves a simultaneous first packet. MR/TU interval rules remain. |
| `hdl/ieee1722/crf/KL_crf_rx.sv:487` | Count every accepted CRF AVTPDU and raise dirty; retain bind reset and unbind preservation. |
| `hdl/ieee1722/avtp/KL_avtp_rx_monitor_ctx.sv:324` | Widen pending FRAMES_RX batch to 32 bits; remove saturation at line 1167; healthy commit and TV/TNV updates raise dirty at lines 949 and 982. |
| `hdl/ieee1722/avtp/KL_avtp_rx_monitor.sv:18` | Clarify the flat diagnostic model versus the shipping context engine and current ruling. |
| `tb/verilator/tkdiag/sim_main.cpp:197` | Packet-total expectations; per-packet dirty assertions at line 589. |
| `tb/verilator/crf_rx/sim_main.cpp:133` | Reference model and burst, dirty and reset expectations follow packet totals; explanatory comment corrected at line 484. |
| `tb/verilator/avtp_rxmon/sim_main_nx.cpp:799` | Require healthy update and commit pulses on the correct descriptors; keep inactive rows quiet. Packet-total comment corrected at line 527. |
| `tb/verilator/avtp_rxmon/sim_lockstep.cpp:166` | Retain every historical dirty event while independently testing the added events; seed at line 393 now actually crosses 32-bit wrap. |
| `tb/verilator/milan_dp/sim_crf_licence.cpp:1002` | Compare CRF total to emitted PDU census, allowing the existing single in-flight packet. |
| `tb/verilator/milan_dp/sim_nxn.cpp:93` | Connect the counter fixture and observation hooks. At line 2548, pause input briefly while pending updates drain before the existing unbind-order probe; resume after its response. |
| `tb/verilator/milan_dp/stream_counters.hpp:9` | Real parent MAC census, reset/wrap, receive batch boundary, per-descriptor/recipient windows and measured service delay. |
| `tb/verilator/milan_dp/stream_counters.py:1` | Both geometries, baseline reproduction, eight isolated parent plants and named-check omission controls. |
| `tb/verilator/milan_dp/stream_counter_f5.cpp:1` | Both descriptor geometries through the unchanged firmware mailbox/core, two recipients and delayed TX completion. |
| `tb/verilator/milan_dp/stream_counter_f5.py:1` | Build the mailbox fixture and two isolated deadline plants with omission controls. |
| `tb/verilator/milan_dp/Makefile:636` | Include standing parent checks in the normal suite; separate F5 and mutation targets at line 666. |
| `docs/reference/REGISTER_MAP.md:148` | Current counter law, reset/dirty semantics and CRF raw-versus-per-run distinction; further entries at lines 869, 919 and 963. |
| `sw/firmware/ctrl/aecp/README.md:55` | Packet law and measured cadence reference. Firmware implementation is unchanged. |
| `docs/testing/726_STREAM_COUNTERS.md:1` | Authoritative methods, before/after measurements, limits, commands and mutation table. |
| `docs/testing/MILAN_V12_AUDIT_2026-08-16.md:218` | Replace the obsolete at-most-only closure claim with the current ruling and evidence. |
| `docs/README.md:92` | Add the measurement document to the documentation map. |
| `docs/findings/117_GPTP_SILICON_EVIDENCE.md:4` | Dated ruling note; historical measurements retained. |
| `docs/findings/394_387_E1_SWITCH_CYCLES.md:4` | Dated ruling note; historical measurements retained. |
| `docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md:4` | Dated ruling note; historical measurements retained. |
| `docs/findings/667_TALKER_START_BENCH.md:4` | Dated ruling note; historical measurements retained. |
| `docs/findings/B14_BENCH_5603C353.md:4` | Dated ruling note; historical measurements retained. |
| `docs/history/v1/reference/PROTOCOL_TRACEABILITY.md:320` | Pin an archived source anchor to the base revision after the live file shortened. |

## Counter and notification measurements

The parent fixture runs the parser, counter producers, descriptor arbiter,
processor and response memory. It observes completed frames at the parent MAC.
Both geometries register two recipients and exercise every AAF and CRF row.
Protocol time is compressed to 1000 cycles/ms with the 50 MHz parameter
retained and simulation clocks running together. This is not physical timing.

`parent-before-1.csv`, `parent-before-8.csv`, `parent-after-1.csv` and
`parent-after-8.csv` retain each descriptor, recipient and fixed window.
Type 5 means Stream Input; type 6 means Stream Output; recipient 0/1 means
first/second controller. Index 1 is CRF at shipping shape; index 8 at largest.
There are 40 recorded row-windows at shipping shape and 180 at largest.

| Shape | Rows including CRF | Steady input row-windows before -> after | Steady output row-windows before -> after | After minimum / maximum gap | Maximum measured service |
|---|---|---|---|---|---|
| Shipping TDM8 | 2 inputs + 2 outputs, two recipients | 12: all 0 -> all 1 | 12: all 1 -> all 1 | 1000.996 / 1001.867 ms | 3.263 ms |
| Largest TDM32 | 9 inputs + 9 outputs, two recipients | 54: all 0 -> all 1 | 54: all 1 -> all 1 | 1000.982 / 1012.029 ms | 14.058 ms |

Five fixed windows are recorded; windows 2 through 4 are graded.
Windows 0 and 1 retain startup and are not graded. Some input rows are empty:
shipping input 0/recipient 0 has bins 1,0,1,1,1; the other input rows have
0,1,1,1,1. Largest input 0 has 1,0,1,1,1 for both recipients; other input rows
have 0,1,1,1,1. Output rows have 1,1,1,1,1. Therefore this evidence establishes
the stated finite steady-window result, not one completion in every startup
window or for every possible window phase. This limitation remains explicit
for review; no broader acceptance claim is made.

Every measured pair is at least 1000 ms apart. The gap check allows only
1000 ms plus that descriptor's measured dirty-and-eligible to final-recipient
MAC-tail service delay. There is no extra timer-phase allowance. The existing
AVB_INTERFACE producer and #60 throttle are unchanged; their integration
checks still pass. Maximum registered-controller fanout was not measured.

| Shape/output | Base FRAMES_TX | MAC AVTPDUs | Corrected FRAMES_TX |
|---|---:|---:|---:|
| Shipping AAF 0 | 5 | 799 | 799 |
| Shipping CRF 1 | 5 | 101 | 101 |
| Largest AAF 0 through 7, each | 5 | 800 | 800 |
| Largest CRF 8 | 5 | 101 | 101 |

The fixture drains each run before comparing totals. Further phases cover
restart and 32-bit wrap using actual emitted packets. Each input receives
500 packets; GET_COUNTERS confirms the total, unbind preservation and zero
at rebind. Seeding an AAF pending batch with 65,534 and receiving three real
packets must publish 65,537. The monitor lockstep case independently checks
0xFFFFFFFA + 11 = 5. The baseline reproduction fails 20 and 90 checks;
its drivers exit zero only when those expected defects are reproduced.
Clean parent fixtures pass 98 and 427 checks respectively.

`mailbox-1.csv` and `mailbox-8.csv` retain all F5 row-windows. The unchanged
core/adapter delivers one notification in each of five windows to both
recipients at both geometries. Minimum spacing is 1000 ms, maximum gap
1002 ms with a measured 2 ms TX stall. The check permits that stall plus
one polling millisecond. It does not measure processor instruction timing.

## Planted defects and omission controls

Every new plant is applied to an isolated parent or firmware copy. Each
planted executable exits 1 with its named assertion group failing; the driver
then reruns that same plant with only that group omitted and requires exit 0.
A crash, build failure or unrelated assertion failure is not detection.
All ten drivers exit 0. These controls use the committed implementation and
check fixture; omission is a runtime test control, not a repository edit.

| Check/group | Plant | Named failures | Same plant without its check |
|---|---|---:|---|
| TX packet census/restart/wrap, `TX` | `tx-interval`: count occupied intervals | 6 | 86 checks, 0 failures, exit 0 |
| RX packet total, `RX` | `rx-interval`: CRF counts occupied intervals | 1 | 89 checks, 0 failures, exit 0 |
| Start reset, `TX_RESET` | `tx-reset`: retain previous TX total | 4 | 94 checks, 0 failures, exit 0 |
| AAF bind reset, `RX_RESET` | `aaf-reset`: retain previous receive total | 1 | 94 checks, 0 failures, exit 0 |
| CRF bind reset, `RX_RESET` | `crf-reset`: retain previous receive total | 1 | 94 checks, 0 failures, exit 0 |
| AAF batch boundary, `RX` | `rx-saturation`: saturate at 65,535 | 1 | 89 checks, 0 failures, exit 0 |
| Notification windows/gap, `CADENCE` | `late`: suppress parent input events | 12 | 66 checks, 0 failures, exit 0 |
| Notification spacing, `RATE` | `rate`: halve parent timer divisor | 32 | 66 checks, 0 failures, exit 0 |
| F5 windows/gap, `CADENCE` | Firmware `late`: advance deadline 2000 ms | 32 assertions | One test, 0 failures, exit 0 |
| F5 spacing, `RATE` | Firmware `rate`: advance deadline 500 ms | 48 assertions | One test, 0 failures, exit 0 |

Retained evidence names `plant-<variant>__run.log` and
`plant-<variant>__escape.log`, plus `f5-<variant>__run.log` and
`f5-<variant>__escape.log`. `ROUND2-ARTIFACTS.tsv` supplies sizes and SHA-256.
The existing unbind campaign still catches all five ordering/counter/push
plants after the fixture's setup change; the six licence plants also remain
caught. The response-order assertions were not relaxed. The source pause
is bounded below the receive silence timeout and ends after the response.

## Validation commands and results

Use CPython 3.12.3, Verilator 5.050, the repository's pinned Python dependencies,
and existing C++ test dependencies. Set TMPDIR and SCRATCH to disk storage,
VERILATOR to the pinned executable, and use at most two simultaneous builds
with two compiler workers. No gate output was piped. All listed completed
gates exit 0; incomplete setup attempts are identified separately below.

```sh
make -C tb/verilator/tkdiag
make -C tb/verilator/crf_rx
make -C tb/verilator/avtp_rxmon
make -C tb/verilator/aaf
make -C tb/verilator/crf_tx
make -C tb/verilator/milan_dp
make -C tb/verilator/milan_dp counters-f5 counters-mutants
make -C tb/verilator/milan_dp unb-mutants crflic-mutants
syn/yosys/run.sh --top KL_avtp_rx_monitor_ctx --top KL_crf_rx --top KL_crf_tx --top KL_aaf_packetizer
syn/yosys/run.sh --top milan_datapath
python3 scripts/pp_srcs.py --check --selftest
python3 scripts/check_soc_sources.py
python3 scripts/check_rtl_source_lists.py --selftest
python3 scripts/check_rtl_source_lists.py
python3 scripts/check_nvm_capture.py
python3 scripts/lint_rtl.py --check
python3 scripts/xvlog_gate.py --check
python3 scripts/docs_check.py
python3 scripts/check_doc_style.py
python3 scripts/gen_toc.py --check
python3 scripts/check_em_dash.py --base c6bd08c6
python3 scripts/check_doc_paths.py
git diff --check
```

The datapath recipe was executed in shorter foreground steps from its own
Makefile dry-run command list. DATAPATH-RESULTS.md records each result.
The initial aggregate build and several short-deadline audio-clock attempts
are incomplete, not passes. The original audio-clock executable completed in a persistent foreground
session with short polling calls, exit 0: media_aclk: 193 checks, 0 failures.
An optional two-thread performance experiment was stopped without a verdict.
No stimulus, clock ratio, assertion or test duration was reduced.

The receiver suites are complete at the final source text. The CRF aggregate
rerun reached its short deadline during the final mutation case after all
functional legs passed; the separate complete mutation campaign exits zero.
The licence and unbind campaigns were also split without changing checks.
All changed regression sources match the final committed tree.

| Completed gate | Evidence/result |
|---|---|
| Talker diagnostics | 99 unit checks; existing mutation campaign 5 controls, all pass. |
| CRF RX | 14,287 unit, 2,201 discontinuity, 69 talker-step checks; 10 mutation checks, all pass. |
| AVTP monitor | Flat/context and both lockstep geometries pass; existing 5 mutation controls pass. |
| AAF | Complete suite including 34,020 startup checks and startup plants passes. |
| CRF TX | 127 checks, no failures. |
| Full parent recipe | All legs complete in foreground steps, including media_aclk: 193 checks, 0 failures; render campaign 6/6 controls passes. |
| Parent notify | 423 checks, no failures, including #60 and unbind ordering. |
| Parent CRF licence | 416 checks, no failures; all six plants detected. |
| Parent unbind campaign | All five plants detected, including delayed response, missed/double unlock, extra interruption and missing push. |
| New parent/F5 checks | Both geometries and all ten plants/escapes pass as tabulated above. |
| Source lists | Processor inventory, SoC inventory, strict RTL closure and 50/50 closure self-tests pass. |
| HDL lint and vendor parser | Ratchet passes; parser reports 0 findings across 81 parent and 52 processor files. |
| Open synthesis | Counter-related tops and full milan_datapath closure pass, including tied-input and observer-purity checks. |
| Documentation | All five gates pass; committed em-dash scan covers 211 added lines in 11 Markdown files. |
| Saved-state capture guard | Pass; runtime firmware and capture inputs unchanged. |
| Whitespace | git diff --check exits 0. |

The full repository scripts/run_all_suites.sh sweep and every unrelated open-
synthesis top were not run. No hosted CI, PR validation, independent review,
candidate merge or post-merge evidence is claimed. Those remain required by
CONTRIBUTING before a PR is marked validated or merged.

## Shipping image area and timing

The shipping configuration is endstation_ax7101_1x1_tdm8, part
xc7a100tfgg484-2, commercial grade. Generated design arguments use
AreaOptimized_high synthesis, ExploreArea optimization,
ExtraPostPlacementOpt placement, and AggressiveExplore physical/route
optimization. The final build used one worker under the exclusive lock.
Image build and routed-checkpoint reporting both exit 0.

| Stage | LUT | Delta from supplied dev baseline | FF | BRAM tiles |
|---|---:|---:|---:|---:|
| dev c6bd08c6 supplied reference | 49,392 | 0 | Not supplied | Not supplied |
| Candidate synthesis | 51,990 | Not comparable to final baseline | 53,509 | 87.5 |
| Candidate placed | 49,426 | +34 | 53,378 | 87.5 |
| Candidate routed | 49,427 | +35 | 53,378 | 87.5 |

BRAM is 74 RAMB36 plus 27 RAMB18. The final +35 LUT result is below the
+200 STOP threshold. Overall routed WNS is +0.451 ns, WHS +0.036 ns,
WPWS +0.264 ns, TNS/THS zero. Slow reports show WNS +0.451 ns and
WHS +0.102 ns; Fast reports show WNS +1.683 ns and WHS +0.036 ns.
All negative-slack reports contain no timing paths. Reports at 0 C and 85 C
record commercial endpoints; endpoint temperature is operating/power metadata,
not an independent timing model. Slow/Fast timing models provide the corners.
No constrained timing or capture bound missed. check_timing reports zero
unconstrained internal endpoints, zero unclocked registers and zero loops.
It also reports 46 input ports exempted by false paths and 87 output ports
without output-delay constraints. The reported slack covers constrained paths;
this lane does not establish missing external I/O timing bounds.

The bitstream is 3,825,992 bytes, SHA-256
`abc33ed1b81c3fc11e0751e770cc8ccbcc68006badef41e4b309bb14b6c932b8`.
The routed checkpoint is 107,885,680 bytes, SHA-256
`b5b2b1ca30fe88a80650a08a4bd93b9661a14fd87424cc51c004649b47757f03`.
Neither large artifact is copied here. `IMAGE-ARTIFACTS.tsv` records every
report's size/hash and points to retained reports no larger than 200,000 bytes.
`implementation-inputs.json` records the measured RTL/config hashes.

The image was elaborated through the repository builder, then its generated
Tcl ran under Vivado 2026.1. The effective elaboration command was:

```sh
python3 sw/litex/milan_soc.py --board ax7101 --milan-clk-freq 50e6 --gtx-tx-invert --floorplan --eth-port e1 --no-i2s-playback --no-render-lpf --num-streams 1 --audio-interface tdm8 --audio-interface-master --audio-interface-render 8 --talker-wire-chans 8 --loopback-lane --fabric-gptp --gptp-ingress-lat-ns 656 --gptp-egress-lat-ns 219 --cpu vexiiriscv --software-profile baremetal --xlen 32 --full --with-spiflash --flashboot baremetal --timing-opt --l2-bytes 0 --uart-baudrate 115200 --cpu-count 1 --entity-gen-dir configs/generated/endstation_ax7101_1x1_tdm8 --synth-directive AreaOptimized_high --opt-directive ExploreArea --place-directive ExtraPostPlacementOpt --vivado-max-threads 1 --output-dir "$SCRATCH/image"
cd "$SCRATCH/image/gateware"
setsid nohup flock $VIVADO_LOCK vivado -mode batch -source alinx_ax7101.tcl > "$SCRATCH/image-run.log" 2>&1 &
```

Use the existing LiteX Python environment and generated shipping descriptors.
The recorded run used absolute source/output paths and a launcher which also
recorded its return code; the commands above use reviewer-selected paths.
The generated Tcl's hash is retained with the image artifacts. Final routed
area was read from open_checkpoint of the generated route checkpoint and
report_utilization; this is distinct from the pre-route utilization report.

## Capture, cleanup and limitations

No firmware C implementation changed, so the saved-state capture was not
re-measured. Its guard passes and the input contract is unchanged. The new
F5 fixture exercises the unchanged core/adapter independently.

Early descriptor-generator imports created six ignored bytecode files under
the processor descriptor directory. Those generated artifacts were removed;
no source or gitlink changed. Parent bytecode caches and a temporary builder
output symlink were removed. Later commands disable bytecode writing.
An initial multi-worker image attempt exceeded the requested working-memory
budget and was aborted; the retained single-worker run used an 8.5 GB soft
limit. The original unlimited soft limit has been restored. Initial setup failures and the timed-out aggregate build are retained
as incomplete attempts, never counted as passes.

The legacy bench classifier in tb/tools/torture_campaign.py and
counters_contract_milan.feature still contains the two historical readings.
It was inspected but not changed. The merge-turn comparison must apply the
current packet ruling, not accept an interval result through that legacy
classification. This lane performed no bench measurement.

Remaining review focus: startup-window coverage, finite duration and two-
recipient scope, coalesced receive publication, and the reference-peer reset
comparison. Independent reviewers must decide the five-lens completion ledger.
The PR body uses Relates to #726 because complete acceptance is not claimed.


Final audit: the worktree is clean; all changed regression sources match the
committed files and the image input hashes match the same RTL/configuration.
The final comment-only commit does not change the measured image. Every
foreground validation process and every image process has finished.


## Round 2 after review

Resumed at acadfacd52c6daabf892d6ebe99da11ca06748cb.
The configured remote and clean lane match the assignment.
R628-1-F1 through F4 and R629-1-F01 are accepted.
R629-1-F02 removes stale PR status prose.

Planned steps: update the bind-era contract and reset controls;
add output cadence measured with only FRAMES_TX changing;
correct the suite notes and executable receive-counter law.
Each step will receive local validation and a new commit.
No RTL, firmware implementation or submodule change is planned.

Final validation, controls, measurements and file references follow below.
The recorded image input hashes match this head.
No hosted success is claimed before the new head is published.

### Round 2 step 1

Commit: 4e0fae3c8d88dca53d8e702b420d703828e99cff.
`tests/steps/counters_contract_steps.py:613` checks ten bind resets
and the six retained anomaly flags. Bind-only and lock checks remain.
The complete behavior gate passes: 404 scenarios, zero failures.
The reviewer's focused reproduction also passes.
Eight source-string plants fail by name: six retained flags,
FRAMES_RX reset removal, and reset on both binding edges.
Each escapes when its specific era check is omitted.
The source file itself is never mutated by these controls.

### Round 2 completed corrections

F3 commit: 54c63e509. The four suite passages now describe packet totals.
All five documentation gates pass, including the committed em-dash scan.
F4 commit: 7287a8284. The law table and rate grader require per-AVTPDU RX.
Single-snapshot packet identity remains diagnostic because publication is coalesced.
The full behavior suite passes 405 scenarios; grader self-tests pass 78 tests.
The rate-law plant fails its specific assertion.
Omitting that assertion lets the same in-memory plant escape.

F2 clean frames-only checks pass at both geometries: 110 and 481 checks.
All output TU/MR wire bits are clear; their counters remain zero.
Each output starts once and never stops during the measured windows.
The output-event plant produces 16 OUTPUT_CADENCE failures, then escapes
with that group omitted. All nine parent plants and both mailbox plants have completed.
The uncertain baseline runs reproduce named TX/RX/CADENCE failures only:
20 at shipping shape and 90 at largest shape. Both drivers return zero.
All source-list gates and the saved-state capture guard pass.
No production RTL, firmware implementation or submodule input changed.

### Round 2 final changes

The final head is `37944f8ac9d1a2212a3a32f36d921434ea0cbdeb`.
All eight changed files are tests, test drivers or documentation.
`ROUND2-SOURCES.tsv` records each committed file's size and SHA-256.

| Finding | File:line at final head | Result |
|---|---|---|
| F1 / F01 | `tests/steps/counters_contract_steps.py:602`, `:620`, `:629` | All ten counters and six anomaly flags must reset on bind. The bind-only edge and lock assertions remain. |
| F2 | `tb/verilator/milan_dp/stream_counters.py:68`, `:92`, `:165`, `:182` | Add the missing-output-event plant and frames-only condition. Baseline requires TX, RX and CADENCE failures exclusively. |
| F2 | `tb/verilator/milan_dp/stream_counters.hpp:47`, `:120`, `:155` | Observe each packet's TU/MR bits, assert the output conditions, and grade OUTPUT_CADENCE separately. |
| F2 | `tb/verilator/milan_dp/Makefile:667`, `:677` | Both conditions and both geometries run in the standing counter target; the new plant joins the campaign. |
| F2 | `docs/testing/726_STREAM_COUNTERS.md:66`, `:70`, `:144`, `:164` | Identify every output condition, record the additional measurements and require named baseline groups; include the behavior gate. |
| F3 | `tb/verilator/milan_dp/README.md:465`, `:499`, `:587`, `:1158` | Correct all four passages to per-AVTPDU totals, current wire census and CRF wrap. Preserve historical numbers. |
| F4 | `tests/features/counters_contract_milan.feature:42`, `:312`, `:410` | Correct trap 3 and the law table; add a flowing-stream interval-rate rejection. |
| F4 | `tb/tools/torture_campaign.py:302`, `:442`, `:508` | Apply Table 7.157 to receive-rate grading. Keep single-snapshot inequality diagnostic because publication is coalesced. |
| F02 | `PR-BODY.md:14` | Delete the stale sentence in the local proposed PR body. The remote PR was not edited. |

The optional S1 and S2 changes were not taken. No production RTL,
firmware implementation, descriptor configuration or submodule changed.
The receive-law correction does not redesign the historical cross-device
interval-comparison helpers. Those helpers are not packet-count acceptance
oracles under this ruling; the updated per-counter grader is the F4 check.

### Round 2 checks and planted controls

All completed gate and campaign drivers return zero.
`ROUND2-GATES.tsv` records commands, working directories, times and results.
The full behavior gate was repeated on the final committed head:
14 features, 405 scenarios, 1,971 steps, zero failures or skips.
The reviewer reproduction passes one focused bind-era scenario.
The bench grader passes all 78 self-tests.

| Check | Plant | Detection | Escape with its check omitted |
|---|---|---|---|
| Bind-era pending state | Remove each of the six anomaly clears | Each names its retained flag | Each passes remaining era checks |
| Bind-era counter reset | Remove each of the ten counter clears | Each names the surviving counter | Each passes remaining era checks |
| Bind-only reset edge | Change rise detection to either edge | Names the invalid reset edge | Other era checks pass |
| Flowing-window RX law | Restore per-interval FRAMES_RX in the grader | Named FRAMES_RX PASS-versus-FAIL assertion | Same plant passes when only the verdict assertion is omitted |
| Packet TX | `tx-interval` | 6 TX failures | 86 checks, zero failures |
| Packet RX | `rx-interval` | 1 RX failure | 89 checks, zero failures |
| TX start reset | `tx-reset` | 4 TX_RESET failures | 94 checks, zero failures |
| AAF bind reset | `aaf-reset` | 1 RX_RESET failure | 94 checks, zero failures |
| CRF bind reset | `crf-reset` | 1 RX_RESET failure | 94 checks, zero failures |
| AAF pending batch | `rx-saturation` | 1 RX failure | 89 checks, zero failures |
| Input cadence | `late` | 12 CADENCE failures | 66 checks, zero failures |
| Rate limit | `rate` | 32 RATE failures | 66 checks, zero failures |
| Output cadence, FRAMES_TX only | `tx-nodirty` | 16 OUTPUT_CADENCE failures | 94 checks, zero failures |
| Mailbox cadence | Firmware-copy `late` | 32 CADENCE assertions | One test passes |
| Mailbox rate | Firmware-copy `rate` | 48 RATE assertions | One test passes |

The 17 era controls modify source strings supplied to the actual contract
checks. They do not simulate RTL and do not edit the checkout. The rate-law
control changes only the loaded grader's table. Their portable scripts are
`review-round2/review-round2__era_controls.py` and
`review-round2/review-round2__law_controls.py`, each taking a checkout path.
The parent and mailbox plants are compiled isolated copies. Each runtime
plant exits 1 with only its named failures, then exits 0 with that group
omitted. Builds, crashes and unrelated failures never count as detection.

| Gate | Final result |
|---|---|
| Parent uncertain condition | Shipping 98 checks; largest 427; all pass |
| Parent frames-only condition | Shipping 110 checks; largest 481; all pass |
| Baseline reproductions | 20 / 90 named TX, RX and CADENCE failures; drivers pass |
| Parent mutation campaign | All nine detection/omission pairs pass |
| Unchanged mailbox path | Both shapes and both deadline plants pass |
| Behavior and bench grader | 405 scenarios and 78 self-tests pass |
| Source inventories | Processor inventory/self-test, SoC and strict RTL closure pass; closure self-test 50/50 |
| Lint | Ratchet passes, 90 findings at the existing budget |
| Documentation | All five gates pass, including the final committed em-dash scan |
| Capture guard | Pass; production capture inputs unchanged |
| Whitespace | Working-tree and base-to-head diff checks pass |

Counter targets were executed through their exact driver commands in
foreground steps with retained scratch builds. No gate output was piped.
Use the commands in PR-BODY.md; the ledger records the concrete executions.
The whole unrelated parent recipe and full repository sweep were not rerun:
Round 2 does not change their source, production inputs or suite recipes.
The original affected unit/integration and image evidence remains retained.

### Round 2 per-descriptor notification measurements

`ROUND2-WINDOWS.csv` retains 660 individual descriptor/recipient/window rows.
The baseline and original clean condition are `uncertain`: each AAF and CRF
output stamps TU=1 and MR=0. The added `frames-only` condition clears the two
talker uncertainty inputs in scratch, then observes the actual emitted bits.
Every AAF output and the CRF output has TU/MR counters zero, wire TU/MR zero,
STREAM_START=1 and STREAM_STOP=0 during measurement. The packet count is the
only output counter changing during steady windows.

| Shape / direction | Descriptor indices | Recipients | Baseline uncertain, each steady window | Corrected uncertain | Corrected frames-only |
|---|---|---|---:|---:|---:|
| Shipping inputs | AAF 0, CRF 1 | Both | 0 | 1 | 1 |
| Shipping outputs | AAF 0, CRF 1 | Both | 1 | 1 | 1 |
| Largest inputs | AAF 0 through 7, CRF 8 | Both | 0 | 1 | 1 |
| Largest outputs | AAF 0 through 7, CRF 8 | Both | 1 | 1 | 1 |

| Shape | Graded rows/windows | Minimum gap | Maximum gap | Maximum service |
|---|---:|---:|---:|---:|
| Shipping, either corrected condition | 24 | 1000.996 ms | 1001.867 ms | 3.263 ms |
| Largest, either corrected condition | 108 | 1000.982 ms | 1012.029 ms | 14.058 ms |

Every row retains windows 0 and 1; only 2 through 4 are graded.
Each pair respects the 1000 ms rate limit. Every maximum gap is bounded by
1000 ms plus that descriptor's measured service, without a phase allowance.
The firmware rows retain one notification per window at both shapes,
1000 ms minimum and 1002 ms maximum, with the existing 2 ms stall.
These are finite simulations with two recipients and compressed protocol time.
They do not establish physical-link or maximum-fanout acceptance.

### Round 2 area, capture and execution limits

All five recorded image input hashes and sizes match the final checkout.
The complete RTL/configuration/firmware/gitlink delta from acadfacd is empty.
No new synthesis, implementation or capture measurement was triggered.

| Shipping image | LUT | Delta against dev c6bd08c6 | FF | BRAM tiles |
|---|---:|---:|---:|---:|
| Supplied dev reference | 49,392 | 0 | Not supplied | Not supplied |
| Retained routed image, inputs unchanged | 49,427 | +35 | 53,378 | 87.5 |

The retained constrained-path WNS/WHS remain +0.451/+0.036 ns.
The existing external-I/O timing limitations above remain explicit.
No area, timing or capture STOP condition arose in this round.
The capture guard passes; no firmware implementation changed.

The requested 9 GB working-memory target was missed briefly when the lint
worker pool overlapped two mutation builds: sampled peak 11,298,734,080 bytes.
The service recorded zero OOM events or kills. Every affected command completed
with rc 0; subsequent work was kept light while the last batch completed.
There were never more than two simultaneous simulation builds, each using
two compiler workers. No background implementation run was started.

The new head is local only. The hosted behavior job and aggregate must be
rerun after authorized publication; no hosted success is claimed here.
This round performed no push, PR edit, rebase, merge, submodule change,
hardware access, flashing or bench action. All foreground work has finished.
Independent re-review and its five-lens ledger remain reviewer-owned.
The reference-peer reset comparison, physical cadence and controller display
remain merge-turn evidence. PR-BODY.md therefore retains Relates to #726.

`REVIEW-ROUND2-ARTIFACTS.tsv` records raw sizes/hashes and published extracts.
Extracts replace checkout and scratch roots with neutral path placeholders.
Oversized logs and generated build artifacts are hash-only entries.
No installed dependencies, build trees or large files were copied here.

## Round 3 after review

Final local head: `e893e4d13d99eb5ba00745f0f5cf74ee847972c2`. The branch and remote match the assignment.
The worktree and all initialized submodules are clean. All gitlinks retain
those at `c6bd08c6`. Assignment 6131008329 accepts R628-2-F1/F2 and
R629-2-F01; all three source corrections and RS1-RS5 are implemented.
Independent re-review remains required; this is execution evidence, not approval.

### Round 3 commits and changes

| Commit | Change |
|---|---|
| `b73f63b69` | Boundary-unit documentation, evidence-reader disposition and fixture idioms. |
| `692916b07` | Per-AVTPDU cross-device grading and unpublished-zero snapshot handling. |
| `30d92e7ec` | RS1-RS5 wording, including COUNTERS bit 3, value 8. |
| `ed34d0cad` | A measured duration is required before certifying packet-rate flow. |
| `e893e4d13` | Complete workflow receipts are part of counter-validation reproduction. |

All commits use the configured identity, one-line subjects and no trailers.

| Finding | File:line | Implemented change |
|---|---|---|
| F1 | `hdl/ieee1722/avtp/KL_avtp_rx_monitor_ctx.sv:187` | Restores one-clock-cycle and one-second boundary units. |
| F1 | `scripts/measure_test_evidence_readers.py:127` | Declares isolated source plants and independent MAC/window expectations. |
| F1 | `tb/verilator/milan_dp/stream_counters.py:32` | Annotates and documents four public functions. |
| F1 | `tb/verilator/milan_dp/stream_counter_f5.py:21` | Annotates and documents the entry point. |
| F1 | `tb/verilator/milan_dp/stream_counters.hpp:30` | Owns mutable fixture state and splits setup, measurement, notification, reset, restart and batch checks; simulated cycles remain unchanged. |
| F1 | `tb/verilator/milan_dp/stream_counter_f5.cpp:41` | Splits the multi-declarator. |
| F1 | `docs/testing/726_STREAM_COUNTERS.md:187` | Requires every workflow result, pinned dependencies and explicit skipped arms. |
| F2 | `tb/tools/torture_campaign.py:732` | Both stream directions are packet-count sources; findings identify each interval-rate side. |
| F2 | `tb/tools/torture_campaign.py:796` | Pair and concurrent-flow verdicts require measured duration for positive packet-rate claims. |
| F2 | `tb/tools/torture_campaign.py:1429` | Cross-device and concurrent-flow assertion contracts follow the ruling; historical identifiers remain compatible. |
| F2 | `tests/steps/torture_plan_steps.py:295` | Requires the packet-law assertion beside the pair comparison. |
| F2 | `tb/tools/torture_campaign.py:4323` | Standing pair and concurrent-flow cases cover each interval-rate side. |
| F3 | `tb/tools/torture_campaign.py:326` | Unpublished zero RX is INFO, without division by zero. |
| F3 | `tb/tools/torture_campaign.py:4116` | Standing zero-publication regression retains settled and no-evidence behavior. |
| F3 | `tests/features/counters_contract_milan.feature:197` | Three-packet startup and settled snapshots enter the behavior contract. |
| F2/F3 | `docs/testing/726_STREAM_COUNTERS.md:165` | Documents both packet laws, measured windows and startup publication. |
| RS1 | `sw/firmware/ctrl/aecp/README.md:59` | COUNTERS is bit 3, value 8. |
| RS2 | `tb/verilator/milan_dp/README.md:500` | Uses per-run counter reset wording. |
| RS3 | `tb/verilator/crf_rx/sim_main.cpp:617`; `tb/verilator/avtp_rxmon/sim_main_nx.cpp:18` | Separates packet totals from unchanged anomaly intervals. |
| RS4 | `hdl/ieee1722/avtp/KL_talker_diag_ctx.sv:68` | Wraps the design-note banner. |
| RS5 | `tb/tools/torture_campaign.py:4100` | Removes superseded law wording from self-test descriptions. |

No ratchet budget changes. No firmware implementation, clock, reset interface,
submodule source or pin changes in Round 3. Optional review suggestions remain
outside these required corrections; no required finding is deferred.

### Round 3 validation and planted controls

[ROUND3-DOCS-GATES.md](ROUND3-DOCS-GATES.md) names all 81 executable commands
from the three documentation-workflow jobs, each with rc 0 and a receipt.
It includes all later gates after the four formerly failing ratchets.
The dependency receipts verify runtime 3.12.3, the hash-locked parser and
Markdown packages, diagram dependencies, the workflow converter archive and
binary, and the pinned SDK archive. No output was piped through a filter.
Hosting checkout/cache/upload actions are not claimed as local executions.

The builder's complete foreground-observed result is rc 0 with 19 explicitly
NOT RUN environment-dependent arms. These are optional elaboration, a local
calibration report, and one platform-dependent mutation. The documentation
job requires the pinned firmware compiler, which ran; it does not require
those optional elaboration arms. This result is not a full elaboration-bank
claim. The candidate runner's offline self-test ran only inside a disposable
CI job, without host orchestration or credentials.

The final commit adds six documentation lines only. All affected documentation
gates were rerun after that commit. The builder's exported source bytes match
its `ed34d0ca` input head; no builder input changes in the final commit.

| Check | Result |
|---|---|
| Behavior contract | 14 features, 406 scenarios, 1,977 steps; zero failures or skips. |
| Counter grader | 80 self-tests pass. |
| Unchanged cross-device reviewer probe | 32,000/32,000 over 4 s PASS; 4/32,000 and 4/4 FAIL with findings against the interval-rate sides. |
| Unchanged receiver-backed reviewer probe | TV=3/TNV=0/RX=0 gives INFO; published RX=3 gives PASS. |
| Focused native units | Talker 99; CRF receiver 14,287; AAF NxN 119; lockstep N=1 and N=8 each 36; zero failures. |
| Existing unit campaigns | Talker 5/5, AAF lockstep 5/5 and CRF 10/10 pass. |
| Parent windows | Uncertain 98/427 checks and frames-only 110/481 checks pass at shipping/largest shapes. |
| Original-source controls | Baseline drivers pass with 20/90 required TX, RX and CADENCE failures. |
| Parent and mailbox campaigns | All nine parent and both mailbox detection/omission pairs pass. |
| Source inventories | Processor inventory/self-test, SoC and strict RTL closure pass; closure self-test 50/50. |
| Lint | Ratchet passes, retaining the existing 90 findings without budget increase. |
| Capture guard | Pass; firmware implementation and capture inputs unchanged. |
| Whitespace | Both working-tree and base-to-head checks return 0. |

| Standing check | Plant | Detection with check | Escape at this source head without its check |
|---|---|---|---|
| Zero-publication snapshot | Restore `if frx and total > frx` | One named SNAPSHOT failure | 79 remaining self-tests pass. |
| Cross-device and concurrent packet rate | Suppress interval-rate side findings | Named XSIDE and MULTI failures | 78 remaining self-tests pass. |
| Flowing-window RX law | Restore interval semantics in its law table | Named FRAMES_RX verdict failure | Remaining assertions pass. |
| TX packet total | `tx-interval` | 6 TX failures | 86 checks, zero failures. |
| RX packet total | `rx-interval` | 1 RX failure | 89 checks, zero failures. |
| Talker-start reset | `tx-reset` | 4 TX_RESET failures | 94 checks, zero failures. |
| AAF bind reset | `aaf-reset` | 1 RX_RESET failure | 94 checks, zero failures. |
| CRF bind reset | `crf-reset` | 1 RX_RESET failure | 94 checks, zero failures. |
| Full-width pending batch | `rx-saturation` | 1 RX failure | 89 checks, zero failures. |
| Input cadence | `late` | 12 CADENCE failures | 66 checks, zero failures. |
| Notification spacing | `rate` | 32 RATE failures | 66 checks, zero failures. |
| Output packet-only cadence | `tx-nodirty` | 16 OUTPUT_CADENCE failures | 94 checks, zero failures. |
| Mailbox cadence | Firmware-copy `late` | 32 CADENCE assertions | Remaining test passes. |
| Mailbox rate limit | Firmware-copy `rate` | 48 RATE assertions | Remaining test passes. |

The grader controls alter isolated loaded functions; they never edit the tree.
Parent and mailbox controls compile isolated source copies. Every runtime
plant must exit 1 with only its named failures, then exit 0 with that check
omitted. Build failures, crashes and unrelated failures never count as kills.
The prior 17 bind-era omission controls remain in the Round 2 packet; neither
their checked implementation nor their standing assertions changed this round.

### Round 3 per-descriptor notification measurements

[ROUND3-WINDOWS.csv](ROUND3-WINDOWS.csv) retains 660 individual rows with every
descriptor, recipient and window. Both output conditions reproduce the prior
measurements exactly after the fixture refactor. Both recipients are graded.

| Shape / descriptors | Direction | Baseline uncertain, every steady window | Corrected uncertain | Corrected frames-only |
|---|---|---:|---:|---:|
| Shipping AAF 0 and CRF 1 | Input | 0 | 1 | 1 |
| Shipping AAF 0 and CRF 1 | Output | 1 | 1 | 1 |
| Largest AAF 0 through 7 and CRF 8 | Input | 0 | 1 | 1 |
| Largest AAF 0 through 7 and CRF 8 | Output | 1 | 1 | 1 |

| Shape | Graded row-windows per corrected condition | Minimum gap | Maximum gap | Maximum service |
|---|---:|---:|---:|---:|
| Shipping | 24 | 1000.996 ms | 1001.867 ms | 3.263 ms |
| Largest | 108 | 1000.982 ms | 1012.029 ms | 14.058 ms |

Each maximum is bounded by 1000 ms plus that descriptor's measured service.
Only windows 2-4 are graded; windows 0-1 remain recorded startup transients.
Baseline outputs carry TU=1, so their notifications also reflect TU changes.
In frames-only runs the emitted TU/MR bits and their counters are zero, with
one start and no stop; FRAMES_TX is the only changing output counter.
The mailbox path retains 1000-1002 ms gaps and one notification per window,
including its 2 ms output stall. The #60 interface throttle is unchanged.
These finite, compressed-time, two-recipient simulations do not prove physical
cadence, maximum fanout or an indefinite fixed-window guarantee.

### Round 3 image, capture and interruption disposition

Round 3 changes only comments in two HDL files. The image-input audit compares
the recorded bytes and their hashes, preserving strings while removing comments,
empty lines and line-edge whitespace for code comparison. Both changed HDL
inputs compare equal; the other three measured inputs are byte-identical.
Firmware implementation, configuration, SoC glue and gitlinks are unchanged.
The final recovery therefore does not restart the interrupted, redundant image
run. That unfinished run supplies no area or timing verdict.

| Shipping routed image | LUT | Delta against dev c6bd08c6 | FF | BRAM tiles |
|---|---:|---:|---:|---:|
| Supplied dev baseline | 49,392 | 0 | Not supplied | Not supplied |
| Retained image, synthesis code unchanged | 49,427 | +35 | 53,378 | 87.5 |

The retained recipe and timing limitations are recorded in the image section
above. Constrained-path WNS/WHS remain +0.451/+0.036 ns; this does not supply
missing external-I/O constraints. No area, constrained timing, capture or
submodule STOP condition arose. No firmware implementation changed, so no
capture re-measure was triggered; `check_nvm_capture.py` passes.

The 21:56 host disk-full interruption is external, not a gate verdict. The
builder container survived and completed; foreground waiting recovered rc 0.
Its final log supersedes the earlier host timeout and container setup refusals.
The initial converter mismatch was detected and corrected by using the exact
workflow release archive and binary. The final dependency receipt verifies both.
The HDL-reference generator initially refused a nonempty output directory during
recovery; a fresh output directory passed. No generator or gate was weakened.

Before interruption, a sampled 9,784,709,120-byte memory peak exceeded the
requested target; no OOM was reported. That remains an execution limitation.
Recovery sampled below 3.2 GB. The previous service's temporary soft limit does
not apply to this new service; the current limit remains unchanged. There were
at most two concurrent simulation builds, with two compiler workers each.
All recovery commands and lane-owned jobs finished before handoff.

### Round 3 evidence and remaining work

`ROUND3-GATES.tsv` and `ROUND3-DOCS-GATES.md` list the complete documentation
workflow. `ROUND3-ARTIFACTS.tsv` records raw and published sizes and hashes.
Receipts replace local roots with neutral variables. Files over 200,000 bytes
are represented by hashes and clearly named terminal extracts. No toolchain,
installed dependency, source export or oversized file is stored in this packet.

Public probe hashes prove that both reviewer scripts ran unchanged.
The packet's `review-round3/grader_controls.py` takes a checkout path.
Reviewers can reproduce its named detections and omission escapes directly.
The prior source and image receipts remain labelled historical evidence.

No push, PR creation/edit, rebase, amend, merge, submodule edit, hardware action,
flashing or bench access occurred in this resume. REVIEW READY is the sole new
issue comment. Hosted reruns and local hosted-workflow replication require the
maintainer's publication step; no hosted success at this unpublished head is
claimed. The full current-dev candidate bank, independent five-lens review and
merge authorization remain required. Physical link cadence, reference-peer
reset comparison and controller display remain merge-turn acceptance evidence.
PR-BODY.md retains `Relates to #726`.
