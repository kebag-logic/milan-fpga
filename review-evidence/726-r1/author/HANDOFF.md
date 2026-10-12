[A605]

# Lane 726 handoff

Status: REVIEW READY for independent review. All affected checks complete; acceptance and merge limitations are listed below.
Head: `acadfacd52c6daabf892d6ebe99da11ca06748cb`.
Base: `c6bd08c6f52632c6d33d834ce842ac3cf63f29cc`.
Branch: `726-stream-counters`. Two local commits; no push or PR action.
Implementation: `7b491e595e87078a06524c88605624913221131b`. The final commit only corrects two test comments.
Executor: [A605]. Independent reviewers: [R628] and [R629].

## Authority and scope

Issue #726, assignment 6125784157, and rulings 6125741685 and 6126028604
were read in full. The second ruling resumes the parent lane and preserves
the processor scheduler. IEEE 1722.1-2021 7.4.42.2.5, Tables 7.157/7.159,
define packet totals; Milan Table 5.4 supplies talker-start reset and
5.4.5.2 Table 5.22 supplies notification spacing.
The original STOP packet and isolated scheduler reproduction in this directory
are retained as historical evidence; the second ruling supersedes that blocker.

The origin URL and initial head matched the assignment. No submodule source
or gitlink changed. No hardware, bench, flashing, push, PR, merge or rebase
operation occurred. The reference-peer reset comparison, physical link cadence
and controller display remain merge-turn work. This packet is evidence for
review, not a claim that the repository's complete merge bar is satisfied.

## Changed files at the head

Line numbers below refer to the committed head.

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
