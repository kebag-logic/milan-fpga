[R962] POSITIVE - exact head 0f7402ee97d347352b8c3d613033c440ee55986a

R962-2, external independent desk re-review of issue #1021 / PR #1024. All five lenses are CLEAN. No BLOCKER, MAJOR or MINOR remains in the reviewed scope. Optional suggestions and publication-link residue are recorded below. This verdict does not authorize merge or complete bench acceptance.

Tree: `1196d35e1d54bfcdef7882a35e081f3779c20bab`. Source base: `4df125b8c11f0e1706b3c1e489f3e66a5d856b18`. Re-review delta: `75db86a926a9f4d2f7734246eac06a8f58c57bac..0f7402ee97d347352b8c3d613033c440ee55986a`.

## Reconstruction and scope

I read the operating rules, CONTRIBUTING.md and documentation map; the [issue's frozen acceptance](https://github.com/kebag-logic/milan-fpga/issues/1021), public PR scope and manager decisions; requirements and the [merged audio contract at 9e5ef16](https://github.com/kebag-logic/usb-audio/blob/9e5ef16cfbbcc26722bfef56081b992a5e8fc89f/docs/AUDIO-FPGA.md); then the base diff, later-round delta and merge history. Executable evidence came from [the published packet at d96d07a8](https://github.com/kebag-logic/milan-fpga/tree/d96d07a8bfe91d12391acf37e888b4f47e527fbd/review-evidence/usbaudfpga-r1), specifically `author-r5` and `author-r3-route`. The issue API returned no comments; relevant decisions are on the PR. Neither private author material nor another current review was consulted. My independent verdict and ledger were written before reading the two prior public reviewer reports.

The branch imports network head `b4a1df4a0913d7a9b03c8ed0678a035ba2eda5d6`. All 33 protected entries agree: 31 identical files, including modes, and two matching deletions. I did not re-review that implementation. The shared datapath diff against that head retains the audio additions; inherited verification files and post-merge repairs were examined separately. The five extracted reporting functions have identical syntax trees to their preceding committed definitions. Existing coverage thresholds were not relaxed: the inherited saved-state coverage change raises fully covered lines/branches from 510/311 to 513/317.

Acceptance remains 8x8 bit-exact desk transport with planted defects, routed Arty cost/closure and unchanged ALINX payloads, followed by physical loopback. This PR explicitly relates to #1021; it does not claim physical loopback or close the issue. This review follows the assigned receipt-based later-round scope, retaining prior conclusions for untouched code whose dependencies did not change.

## Prior finding reconciliation

The [internal prior review](https://github.com/kebag-logic/milan-fpga/pull/1024#issuecomment-7211465999), [external prior review](https://github.com/kebag-logic/milan-fpga/pull/1024#issuecomment-7211310116) and [manager disposition](https://github.com/kebag-logic/milan-fpga/pull/1024#issuecomment-7211331886) are reconciled by finding ID. The author's response alone is not clearance.

| Prior finding | Disposition at this head | Cause-level evidence |
|---|---|---|
| R961-1 F1, MAJOR, Docs/Tests: three failing gates | RESOLVED | `scripts/solution_ports.py:138` classifies the fourteen audio ports; integration tables carry the group. `docs/AAF_LATENCY_TAPS.md:25` includes the audio configuration. Independent solution gate and 51 controls pass; actual `test_tap_clock_docs()` passes; inventory workflow body and 60 controls pass. All 44 published gate command hashes match checked-in run bodies, with zero recorded failures; builder legs cover all 115 cases exactly once. |
| R961-1 F2, MAJOR, Tests: missing capture-epoch integration controls | RESOLVED | `epochs_tb.sv:146` drives actual framed records through the bridge at 20/26 ns clocks. It stops media application, blocks status, changes capture during partial bus/render frames, verifies channel-zero restart, and separately changes playback. All five bridge plants independently failed their named runtime assertion here; baseline passes. |
| R961-1 F3, MINOR, Conformance/RTL/Robustness/Tests: lost grid snapshot | RESOLVED | `KL_usbaudio_media.sv:62` defers changed-playback state until the frame boundary; `:111` starts a complete silent frame for a coincident transition. An active walk finishes before state applies. `media_tb.sv:125` checks four pairs and one snapshot at all eight offsets, with no gap/error. Both old-behavior plants independently fail `MEDIA_EVERY_GRID_SNAPSHOT`. |
| R961-1 F4, MINOR, Docs/Tests: overstated clock independence | RESOLVED | `USB_AUDIO_PATH.md:129` and `duplex.cpp:3` state fixed 1:2 bus/media ratio and phase, matched rates and separate incommensurate oscillator. They exclude phase drift/rate mismatch from the million-frame claim. Epoch-harness clocks are described separately. |
| R961-1 F5, RESIDUE, Docs: pre-merge citation | RESOLVED | Design document, YAML line 6 and PR body cite merged `9e5ef16`. The fetched contract hash matches the published comparison receipt. |
| R962-1 F1, MAJOR, Conformance/RTL/Tests/Docs: unavailable raw physical evidence | RESOLVED for assigned published-receipt review | Historical text reports are now in `author-r3-route`; fresh reports and original/published hash mappings are in `author-r5/receipts-r5/physical-reports` and `route-report-manifest.json`. Actual timing, constraints, flag-pair setup/hold, skew, placement and resource evidence were inspected. The manager retains binaries outside publication and supplies identities. ALINX equality is accepted as the published paired-build receipt, not claimed as my own byte comparison. Limits below remain explicit. |
| R962-1 F2, MAJOR, Conformance: undisposed execution exception | RESOLVED BY AUTHORITY | Manager comment `7211331886` accepts the historical temporary-file exception, limits its scope, lifts STOP and requires subsequent temporaries inside scratch. This is a disposition, not retrospective reconstruction of advance records. |

Earlier pad-placement, registered-level-launch, synchronizer-hold, watchdog and full-subslot fixes remain present; this delta does not undo them. The 77-entry receipt matches the current 24 protocol and 53 transport plant names and named assertions exactly. Prior optional S4 is resolved too: the design document says watchdog-test timestamps remain one millisecond apart and distinguishes the delivery guard.

## Applied lenses

[R962] PASS Conformance - `KL_usbaudio_media.sv:62`, `KL_usbaudio_bridge.sv:130,227,255`, merged AUDIO-FPGA.md - Checked complete grid frames, independent epochs, media application before acknowledgement, completed status before capture, unchanged wire layouts and 32-bit retention. No conversion or physical qualification claim was introduced.

[R962] PASS RTL - `KL_usbaudio_media.sv:111,161`, bridge crossings/status at `:167,218,227`, `sw/litex/usbaudio_cdc.tcl:4`, `usbaudio_timing.xdc:13` - Reviewed handshakes, walk completion, resets, parameter guards and changed port wiring. Whole-frame crossings and registered launch levels remain intact. Actual flag-pair timing retains setup +0.624 ns under a 2 ns maximum and hold +0.324 ns. No broad timing exception was added by this delta.

[R962] PASS Robustness - `epochs_tb.sv:146`, `media_tb.sv:125`, `parameters_test.py:14`, `transport_mutations.py:23` - Applied independent-direction transitions, partial capture abandonment, ordinary stall retention, halted media application, withheld status, all grid/walk offsets and reprime. Seven relevant runtime defects were independently killed; both baselines pass. Published 21 accepted/22 refused parameter controls and retained loss/reset controls are source-bound evidence.

[R962] PASS Tests - `.github/workflows/docs.yml`, `check.py:29`, `transport_mutations.py:283`, `scripts/sv_ports.py:287`, `scripts/suite_shards.py:858` - Epoch tests run in the default regression. Campaigns require named runtime failure; build errors do not count. Attribute-parser controls cover declarations, wildcard events, comments and strings. Workflow hashes, builder union, repaired gate executions and scheduling controls pass without deleting checks or raising ratchets. Reporting-function extraction is structurally identical.

[R962] PASS Docs - `USB_AUDIO_PATH.md:3,51,129,174`, YAML line 6, tap table, integration port tables and public physical receipts - Checked clock conditions, transition behavior, merged authority, exclusions and physical limits. No new prohibited bench-lane or reviewer label was found in the audio-owned source-comment delta. Items below do not alter technical claims or clean coverage.

## Executed evidence

| Check | Result | Reviewer receipt |
|---|---|---|
| Five bridge epoch plants and baseline | 5 CAUGHT, baseline PASS | `epoch-controls-results.json`, `probe-runtime/epoch-controls/` |
| Two grid/walk plants and baseline | 2 CAUGHT, baseline PASS | `grid-controls-results.json`, `probe-runtime/grid-controls/` |
| Solution documentation workflow body | PASS; 51 controls | `gate_11.log` |
| Port-contract workflow body | PASS; 88 controls | `gate_32.log` |
| Test-evidence workflow body | PASS; 105 controls | `gate_35.log` |
| Documentation inventory workflow body | PASS; fresh 546-line inventory, 60 controls | `docs-inventory-workflow.log` |
| Actual configured-tap test | PASS | `tap-clock-docs.log` |
| Suite scheduling controls | PASS | `scheduling-controls.log` |
| Packet/source bindings | 152 file hashes, 32 audio entries, 33 network entries, 44 command bodies match | `packet-audit.json` |
| Physical summaries, builder union, extraction and plant inventory | PASS | `supporting-audit.json` |
| Final checkout integrity | 2,068 superproject files and four required submodules match bytes, modes and index | `checkout-final.json` |

The scoped simulator identity is recorded in `simulator-identity.json` (release 5.050). Independent campaigns ran concurrently with eight build jobs each, at most sixteen total. All foreground drivers joined their work. No physical build ran. Reproduction scripts are `run_probes.py`, `run_gate_followups.py`, `audit_packet.py` and `verify_checkout.py`; run them from the candidate clone, with scripts in the output directory. Pass the simulator path to `run_probes.py` if needed. Disposable products stay under `scratch/`.

The author's full-window receipt reports 1,000,000 playback frames, 999,993 capture frames, 37,419,648 checks and zero failures. Its published log digest matches. This is a matched-rate bridge run with startup/tail occupancy, not physical loopback or bus/media rate-mismatch evidence. I did not rerun that workload.

The fresh route's summaries agree with its receipt: Fast 0/85 C setup +1.358 ns, hold +0.052 ns, pulse +1.591 ns; Slow 0/85 C setup +0.006 ns, hold +0.128 ns, pulse +1.389 ns. All failing-endpoint and total-negative-slack columns are zero. Two temperature settings do not create four independent timing libraries. The pad report has 55 passes; 13 skew constraints and zero unconstrained internal endpoints agree with the receipt. Disclosed structural reset and inherited board-port diagnostics remain; timing closure does not mean warning-free design.

Cost differences recompute to +2,197 LUTs, +5,911 registers, +8 block-RAM tiles, +755 slices and zero extra DSPs, at 93.78% slice occupancy. ALINX receipts report equality of all 3,825,788 programming bytes per profile: `cb68aafe538751d1b2f233e672b772b1b2ab766542bde72492128284c0fc7ec4` for 1x1 and `46ddf70298affe60ed3f13ab465dee9fc3911129691610d1337d8b130ba67592` for 8x8. Only container metadata is excluded. These builds use fixed initialized memories and fresh wrappers, not newly linked production-software identity.

## Non-blocking findings

**R962-2-S1 - SUGGESTION - RTL, Robustness - `KL_usbaudio_gpif.sv:61,82,127` - Retain prior accepted-word suggestion.** Authority/evidence: R961-1 S1; transfer semantics are unchanged. A selected word can be written while packetizer valid falls on lock loss. Impact: possible duplication before the contract's validity-loss re-epoch discards the session. Optional outcome: accepted-word accounting agrees with the physical write. Verification: drop validity between selection and write and score the bus beat. It remains optional under the recovery contract.

**R962-2-S2 - SUGGESTION - Conformance, Robustness - `KL_usbaudio_reference.sv:45` - Retain prior delivery-bound suggestion.** Authority/evidence: R961-1 S2; the disclosed 0.75-1.25 ms source-timestamp guard is unchanged. Impact: variable firmware submission timing can require another qualification window. Optional outcome: tie a future configurable guard to measured hardware variation. Verification: measured late/bunched boundaries still refuse invalid observations and never substitute nominal feedback.

**R962-2-S3 - SUGGESTION - Tests - `tb/verilator/usbaudio/check.py:21`, `transport_mutations.py:247` - Retain helper-interface suggestion.** Authority/evidence: R961-1 S3; cleanup-ledger arguments remain in the harness interface. Impact: operational coupling complicates ordinary invocation. Optional outcome: simplify arguments while preserving isolated artifacts and cleanup accounting. Verification: default regression and campaign detection/refusal behavior remain unchanged.

**R962-2-S4 - SUGGESTION - Tests, Docs - `scripts/measure_test_evidence_readers.py:22,326` - Consolidate duplicate network reader key.** Authority/evidence: the dictionary defines `tb/verilator/usbnet/mutants.py` twice; the later description replaces the earlier. Both classify it as a mutation reader; the evidence gate passes. Impact: future explanation edits can target an inactive entry. Optional outcome: retain one complete description. Verification: classification and evidence-gate results remain identical.

**R962-2-R1 - RESIDUE - Docs - public `author-r5/HANDOFF-r5.md` and `REVIEW-READY.md` - Correct copied relative links.** Authority/evidence: publication uses `receipts-r5/`, while prose links retain `receipts/r5/` and absent local `receipts/INDEX.md`. Impact: navigation inconvenience; receipts are present and were located through the manifest. Exact outcome: replace `receipts/r5/review-response.md` with `receipts-r5/review-response.md`; replace `receipts/INDEX.md` with `receipts-r5/`, labelled “receipts directory”. Verification: links open existing public paths. This changes prose navigation only, with no measurement, verdict, test or contract change.

## Reviewer-owned completion ledger

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | issue #1021; merged AUDIO-FPGA.md; grid/state logic; bridge acknowledgement gates; physical receipt scope | R962-2 | 0f7402ee97d347352b8c3d613033c440ee55986a |
| RTL | CLEAN | hdl/milan/usbaudio/KL_usbaudio_media.sv:62; KL_usbaudio_bridge.sv:227; parameter guards; shared merge; raw route/flag/skew/packing reports | R962-2 | 0f7402ee97d347352b8c3d613033c440ee55986a |
| Robustness | CLEAN | epochs_tb.sv:146; media_tb.sv:125; parameter controls; seven independent defect catches; retained loss/reset controls | R962-2 | 0f7402ee97d347352b8c3d613033c440ee55986a |
| Tests | CLEAN | workflow bodies/source bindings; repaired gate executions; epoch/grid logs; 77-plant inventory; builder union; scheduling/extraction controls | R962-2 | 0f7402ee97d347352b8c3d613033c440ee55986a |
| Docs | CLEAN | USB_AUDIO_PATH.md; merged citation/config; tap table; integration port tables; fresh inventory; public evidence and limits | R962-2 | 0f7402ee97d347352b8c3d613033c440ee55986a |

## Real limits and pending manager duties

- This is source-head desk review. No manager source bank exists or is inferred. The manager validates the merge candidate against then-current `dev`, with builder/native banks and linked receipts. Assigned live-dev reference: `e275d7950ef3385753e6a15d2e191ba855b171ed`. Source evidence is distinct from candidate evidence.
- Full parent, processor, gPTP, portability and builder banks were not run here. Hosted/local workflow acceptance belongs to the manager. I did not poll hosted jobs or count skipped contexts as execution. Required contexts, independent review completion, maintainer authorization, candidate validation and post-merge containment remain mandatory.
- Physical calibration is NOT RUN. Field skips and desk tests provide no hardware proof. Physical interval variation, arming/reset, bus timing, DMA fencing, host binding and sustained bit-exact loopback remain open. Concurrent network use additionally needs A2 wiring.
- Checkpoint/programming binaries are retained by the manager under the stated publication policy. I inspected public reports and source/input/equality receipts; I did not load a checkpoint, reroute or compare the binary pairs independently. The +0.006 ns margin applies only to the recorded implementation and recipe.
- Evidence commit signature status is `N`: unsigned. Content hashes were verified; no cryptographic signature is claimed. Full raw build/gate logs are not all published: command hashes and receipts were verified, the full-window text was hash-checked, and focused executions provide independent runtime receipts. Default-run text is an excerpt, distinct from the full-log hash in `regression.json`.
- The supplemental 323-control reporting campaign stopped after 84 catches and is not treated as complete. Separate 77 audio controls and 44 workflow commands have completed published receipts. Reporting extraction was independently compared structurally.
- No source fix, commit, push, GitHub write, author contact, container execution, shared install or hardware action occurred. Final bytes/modes/index checks pass for source and required submodules. `external` remains uninitialized and is not a required gate input. Only manifest-listed files and this report are publishable; scratch is excluded. Path-only redactions retain original/published hashes in `receipt-provenance.json`.

R962-2 FINISHED
