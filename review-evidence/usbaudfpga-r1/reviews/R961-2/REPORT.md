[R961] NEGATIVE - exact head 0f7402ee97d347352b8c3d613033c440ee55986a

# R961-2: internal independent re-review of PR #1024 (issue #1021), rounds 4-5

- Exact head `0f7402ee97d347352b8c3d613033c440ee55986a`, tree `1196d35e1d54bfcdef7882a35e081f3779c20bab` (verified in the clone).
- Previously reviewed head `75db86a926a9f4d2f7734246eac06a8f58c57bac` (R961-1). Delta reviewed: `75db86a9..0f7402ee`.
- Contract: kebag-logic/usb-audio `docs/AUDIO-FPGA.md` at merged `9e5ef16cfbbcc26722bfef56081b992a5e8fc89f`. That commit is identical to usb-audio `main`.
- Reconstruction used public state only, in this order: AGENTS.md and CONTRIBUTING.md; docs/README.md; issue #1021 (body; the issue has no comments); the PR body; the contract; the diff and history; the author packet `d96d07a8:review-evidence/usbaudfpga-r1/author-r5`; and exact-head hosted check runs.
- Prior findings (R961-1 comment 7211465999, external R962-1 comment 7211310116, manager disposition 7211331886) were read only after my own pass over the delta and my probes.
- All five lenses were applied.
- **Verdict: NEGATIVE.** Every round-1 finding (F1 to F5) is closed at this head. Two new MINOR findings are open:
  - **N1 (Docs):** the merge's register-reference refresh regresses the documented behaviour of the writable latency registers.
  - **N2 (Tests):** three ordering defects in the new transition and acknowledgement windows survive every shipped test.

## Scope reconstruction

**Acceptance criteria** (issue body, frozen):
1. Both directions at 8x8, bit-exact, with no gaps or duplicates over a long run, and a planted defect for each interface rule.
2. The Arty route meets every corner, the cost is stated, and the ALINX images are identical.
3. A bench loopback.

Criterion 3 is not claimed (the PR says "Relates to #1021"), which is correct.

**Delta topology.** The first-parent history after `75db86a9` is:
- `e6d56c1e`: merges dev `71bad8c0` (PR #1017 and #1019).
- Five audio commits, `36d2d1d7` to `573fe2bf`.
- `0e321fa6`: merges the network head `b4a1df4a`.
- Three post-merge corrections: `9a3bd0f8`, `3f9b4858` and `0f7402ee`.

**Classification of the 207 delta files** (`delta-classes.tsv`, script `scripts/classify_delta.py`):

| Origin | Files |
|---|---:|
| Byte-identical network import | 112 |
| Dev import | 37 |
| Shared import | 6 |
| Audio-own | 29 |
| Own changes to files the network or dev side also changed | 23 |

**Network content.** All 33 protected network entries match `b4a1df4a`: 31 files are identical and 2 were deleted on both sides. I recomputed them from the receipt's hashes (`network-identity-recheck.txt`). Per the brief, #1020's content was not re-reviewed.

**Conflict resolution** (`merge-resolution.tsv`, script `scripts/merge_resolution.py`). I redid the three-way merge, with base `cc49123d`, ours `573fe2bf` and theirs `b4a1df4a`, for all 54 paths changed on both sides:
- 18 resolve cleanly and equal the head.
- 25 are identical on both sides.
- The 11 remaining resolutions were each checked by hand:
  - The audio port group moved with the network side's extraction into `scripts/solution_ports.py:137-141`.
  - The duration table extracted to `scripts/suite_durations.py` is value-identical to the pre-merge table: 69 suites, and the same provisional set (`scripts/durations_equal.py`).
  - The five report helpers moved to `burst_report.py` have AST-identical bodies (`scripts/func_equal.py`).
  - `ctrl_loop.h` and the service-budget files differ from the network head only in wording ("Linux-host" became "host", "CPU/sys" became "CPU and system"). No budget value changed.
  - The truncations in the merge commit (`AAF_LATENCY_TAPS.md`, `run_all_suites.sh`, `measure_test_evidence.py`, `suite_shards.py`) are fully restored at the head.
  - `REGISTER_MAP.md` is the exception, and it is N1.

## Findings

### N1 MINOR: the register reference now contradicts the writable-latency RTL it documents

- **Lenses:** Docs.
- **Artifacts:**
  - `docs/reference/REGISTER_MAP.md:1046-1068`, the PTP_INGRESS_LAT and PTP_EGRESS_LAT words;
  - `docs/reference/REGISTER_MAP.md:3327-3340`, GPTP_LAT;
  - the commit that rewrote them, `0f7402ee` ("Refresh the register reference after the shared datapath merge");
  - their prose source, `scripts/register_descriptions.json:1611-1622` and `:3270`.
- **Authority and evidence** (`receipts/register-reference.txt`):
  - At this head the CSR RTL implements runtime-writable corrections: `hdl/common/csr/milan_csr.sv:122-129` (#829, `GPTP_LAT_WRITABLE_P`) and `:1594-1596` (reset to the configured correction).
  - `configs/endstation_arty_split.yaml:228` enables them (`latency_writable: true`), and `sw/builder/endstation_builder.py:5369` emits `GPTP_LAT_WRITABLE_P = 1`.
  - The network head's page says "Scratch unless `gptp.latency_writable` enables the plane's runtime correction", "With `gptp.latency_writable`, `0x540` and `0x544` change the applied pair" and "The Arty split resets to 1409/100 ns (#829)".
  - `0f7402ee` regenerated the page from `register_descriptions.json`, which never received that prose. The head now says "Readable inert scratch" and "no timestamp-correction consumer reads the word at this VERSION", with no mention of the option (0 occurrences of `latency_writable`).
  - I ran `gen_register_reference.py --check` with the pinned `wavedrom` on exported trees. It reports `fresh` at this head and `STALE (2 files)` at `b4a1df4a`. So the gate turned green by dropping correct prose: the generator's input is stale, and the network side had hand-maintained the page.
  - This is a register-contract claim in an authoritative generated reference, so it is not RESIDUE. CONTRIBUTING's docs rule says obsolete documents must not be restored and changed contracts must be reflected.
- **Impact:**
  - A firmware or integration reader is told that `0x540` and `0x544` are inert, and that GPTP_LAT is constant, on the Arty split build.
  - On that build those words apply the runtime correction and reset to the configured pair (1409/100 ns). `sw/firmware/ctrl/plat` relies on this.
- **Required outcome:**
  - The prose source (`scripts/register_descriptions.json`) states the writable-latency behaviour, so the regenerated page carries it again. That covers: which bits apply, the reset to the configured correction, GPTP_LAT reading the applied pair, and the Arty split reset values.
  - `gen_register_reference.py --check` passes on that source.
  - The root is shared with the network lane, whose own head is stale on this check. The manager decides which lane carries the fix. Either way, the merged head must not carry the inert-scratch text for a build that enables writes.
- **Verification:**
  - `--check` returns `fresh` at the new head.
  - `grep latency_writable docs/reference/REGISTER_MAP.md` finds the option at the 0x540, 0x544 and 0x7F0 entries.

### N2 MINOR: three ordering defects in the epoch and transition windows survive every shipped test

- **Lenses:** Tests.
- **Artifacts:**
  - `hdl/milan/usbaudio/KL_usbaudio_media.sv:64-69`: the deferred playback transition added for F3, its acknowledgement gate and the playback-consumption guard;
  - `hdl/milan/usbaudio/KL_usbaudio_bridge.sv:241-243`: the published epoch is the snapshot's epoch;
  - `tb/verilator/usbaudio/media_tb.sv:123-143` and `tb/verilator/usbaudio/epochs_tb.sv:157-200`.
- **Authority:**
  - AUDIO-FPGA.md (9e5ef16) lines 166-167: on a new playback epoch, flush and prefill before exposing that epoch's frames. Line 120: no uncounted gaps.
  - Lines 140-142 and 173-175: apply the new capture state before echoing it, and acknowledge it in status before emitting a new capture packet.
  - AGENTS.md section 6, Tests: each new test can fail for the defect it claims to detect. `USB_AUDIO_PATH.md` says the checks "cover ... both acknowledgement gates" and that state "waits until the pair walk finishes".
- **Evidence.** I planted single-line defects (`scripts/probe_mutants.py`, `receipts/reviewer-probes-results.json`, `receipts/reviewer-probes-2-results.json`). Clean controls of both benches pass. Every probe built, and none was counted as a detection on a build failure. Three survive both `media_tb` and `epochs_tb`:

  | Probe | Edit | Media bench | Epochs bench |
  |---|---|---|---|
  | p8 | `playback_ready_o` drops `!playback_changed_w` (`media.sv:68`) | PASS (survives) | PASS (survives) |
  | p9 | `ack_valid_o` drops `state_boundary_w` (`media.sv:66`) | PASS (survives) | PASS (survives) |
  | p7 | `published_epoch_r <= applied_epoch_r` (`bridge.sv:243`) | n/a | PASS (survives) |

  - A directed probe (`scripts/probe_transition_tb.sv`, `receipts/probe-transition.log`) shows that p8 and p9 are real defects and that the head is correct. In the probe, a playback epoch change arrives during a pair walk with that epoch's first frame already at the FIFO head.
    - Head: the change is deferred 6 cycles, nothing is consumed or acknowledged, and the frame is still held after the change applies. PASS.
    - p8: the new epoch's first frame is consumed and discarded during the deferral, a silent loss (`CHECK PROBE_NEW_EPOCH_FRAME_LOST`).
    - p9: six acknowledgements are pushed before the state applies (`CHECK PROBE_ACK_WHILE_DEFERRED`).
  - p7 publishes an epoch the host never received. This happens when a status record is snapshotted with the old epoch, held by status backpressure across the capture-epoch acknowledgement, and then completed. `epochs_tb.sv:178` stalls status only while no record is in flight, so it never builds this case.
  - Round 4 made the p8 and p9 windows reachable. Before it, `state_ready_o` waited only for acknowledgement room, a rare event. Now every playback change that lands within six cycles of a grid event, or during the walk, is deferred. In the integrated bridge, a record carrying the new epoch's PCM follows its state within that time.
- **Impact:** the guards are correct today, but a regression in any of them would ship undetected:
  - p8 would silently lose the first frame of each new playback epoch, which breaks the bit-exact requirement of criterion 1;
  - p9 would acknowledge a capture epoch before the media domain applied it;
  - p7 would open capture before the acknowledging status reached the host.
- **Required outcome:** one or both benches must add the following stimulus, and each of the three edits above must then fail a named runtime check:
  - a deferred playback transition presented with the new epoch's frame already queued and with acknowledgement room, checking that the frame is retained and later played, with no gap, and that no acknowledgement precedes application;
  - a status record held by backpressure across a capture-epoch application, checking that capture stays closed until a record carrying the new epoch completes.
- **Verification:** rerun `scripts/probe_mutants.py` with p7, p8 and p9, or add them to `transport_mutations.py`. All three must be CAUGHT with clean baselines.

### R1 RESIDUE: broken links in the author handoff (evidence packet only)

- **Artifacts:** `review-evidence/usbaudfpga-r1/author-r5/REVIEW-READY.md` and `HANDOFF-r5.md` at `d96d07a8`.
- **Evidence:**
  - Both files link `receipts/r5/review-response.md` and `receipts/INDEX.md`. The packet has `receipts-r5/review-response.md` and no `INDEX.md` under `author-r5`.
  - The receipts themselves are bound by `MANIFEST.json`: 367 entries, 0 hash mismatches, 0 unlisted files.
- **Exact fix:** change the links to `receipts-r5/review-response.md`. Either drop "the receipt index binds the evidence" or link `../MANIFEST.json`.

### Suggestions (optional; they do not affect coverage)

- **S5** (Tests): `tb/verilator/usbaudio/transport_mutations.py:296` and `mutations.py:113` dropped their per-run `timeout=` in round 4.
  - Each bench has its own `$fatal` watchdog (for example `epochs_tb.sv:201`). But a plant that hangs the simulator before the watchdog now stalls the whole campaign until the job deadline, instead of reporting that one plant.
  - Consider a generous per-run bound, recorded as TIMEOUT and never as CAUGHT.
- **S1, S2 and S3** from R961-1 remain optional, as the author records:
  - S1: the accepted word in the GPIF write path.
  - S2: the delivery-guard width.
  - S3: the cleanup-ledger options.

## Prior findings at this head

| Finding | Status | Evidence at this head |
|---|---|---|
| R961-1 F1 MAJOR (three gates fail) | **Closed** | `receipts/f1-gates.log`: `check_solution_docs.py` OK (17 exhaustive port groups), `docs_inventory.py --check` fresh, `test_clock_contract.py -k test_tap_clock_docs` passed, `docs_check.py` 0 findings. Also `check_port_contracts.py --selftest` 88/88, `suite_shards.py --selftest` PASS, `lint_rtl.py --check` PASS at 89 <= ratchet 89, module matrix current (`receipts/lint-matrix.log`). No gate was weakened: no budget, ratchet or waiver file changed in an own commit; the suite timeouts are additions (audio 900 s, shorter than the 1800 s fallback); the timeout-contract string gained the 900 entry and kept every other entry; the 44-step receipt names the `docs.yml` sha256 that I recomputed (`97ca93b0...`). |
| R961-1 F2 MAJOR (bridge epoch wiring untested) | **Closed** | The three plants that survived in round 1 (applied gate, abort tie-off, status echoing the bus epoch) and the two new bridge plants are each CAUGHT by name in `epochs_tb` (`receipts/delta-plants-results.json`). New residual gaps in the same area are N2. |
| R961-1 F3 MINOR (grid frame lost on playback change) | **Closed** | `media.sv:62-69,111-119` defers application until the walk completes, and a coincident event walks silence. This conforms to "no partial-frame insertion" (AUDIO-FPGA.md:117-120). `media_tb.sv:123-143` covers all eight offsets. `media_grid_transition` and `media_walk_transition` are CAUGHT; my p1 (boundary ignores the tick) is CAUGHT by `MEDIA_EVERY_GRID_SNAPSHOT`. |
| R961-1 F4 MINOR (long-run clock wording) | **Closed** | `USB_AUDIO_PATH.md:137-148` matches `duplex.cpp:120-121` (bus every 4 steps, media every 2) and `:152` (6 frames every 6,250 bus cycles). The receipt's `conditions` field states the same. |
| R961-1 F5 RESIDUE (contract citation) | **Closed** | `USB_AUDIO_PATH.md:4-5`, `configs/endstation_arty_usbaudio.yaml:6` and the PR body cite `9e5ef16`. |
| R961-1 S4 (watchdog test wording) | **Closed** | `USB_AUDIO_PATH.md:115-117`. |
| R962-1 F1 MAJOR (raw route reports) | **Resolved for the text reports** | `author-r5/receipts-r5/physical-reports`: all 44 reports match `route-report-manifest.json`. I read the four corner reports directly: setup +0.006 ns (Slow), hold +0.052 ns (Fast), pulse +1.389 ns, 0 failing endpoints. 13/13 bus-skew groups MET. `check_timing` shows 0 unconstrained internal pins; the only unconstrained ports are inherited board ports and the forwarded `usbaudio_pclk`. Recomputed from the utilization reports: +2,197 LUTs, +5,911 registers, +8 BRAM tiles, +755 slices, +0 DSP, and 14,864/15,850 = 93.78% slices. The binary checkpoint and the ALINX payload bytes remain unpublished by the manager's disposition. The payload receipt records identical programming data for both profiles (3,825,788 bytes). |
| R962-1 F2 MAJOR (execution exception) | **Disposed by the manager** (7211331886) | Not a lens finding of mine. The current packet logs removals in advance and uses the lane scratch (`execution.json`). |

## Executed evidence (this round)

All simulation used the pinned simulator: `--version` reports `5.050 2026-07-01 rev v5.050`, which matches the workflow's `VERILATOR_VERSION: v5.050`. Runs were on an exported copy of the head tree, and the source was never mutated.

| Run | Result | Receipt |
|---|---|---|
| Default audio regression (`check.py --jobs 4`) | PASS, rc 0, 3 min 08 s wall (394 s CPU, host load about 74). Includes 21 valid / 22 refused parameter controls, `epochs`, both storage widths, the short duplex (48,192 checks, 0 failures) and 12 representative plants. | `receipts/default-regression.log` |
| Delta plants (5 bridge, 2 frame-preservation, 2 media epoch) | 9/9 CAUGHT by name; baselines `epochs` and `media` PASS | `receipts/delta-plants-results.json` |
| Reviewer probes, batch 1 and 2 | Caught: p1, p2, p3, p4, p5, p6. Survived: p7, p8, p9 (N2) | `receipts/reviewer-probes-results.json`, `receipts/reviewer-probes-2-results.json` |
| Directed transition probe | Head PASS; p8 and p9 FAIL by name | `receipts/probe-transition.log` |
| F1 gates and related gates | All rc 0 | `receipts/f1-gates.log`, `receipts/lint-matrix.log` |
| Register reference check | Head `fresh`; network head `STALE` (N1) | `receipts/register-reference.txt` |
| Merge-resolution replay, network identity, delta classification | As in Scope | `merge-resolution.tsv`, `network-identity-recheck.txt`, `delta-classes.tsv` |
| Evidence packet integrity | `MANIFEST.json` 367/367 hashes match; 44/44 physical reports match their manifest | (re-derivable from the packet) |
| Clone integrity after probes | 2,068 tracked files, 0 blob or mode mismatches; index tree equals head tree; status empty; six gitlinks unchanged | `receipts/clone-integrity.txt` |

The million-frame run was not repeated. Its harness changed only in a comment line (`duplex.cpp:3`). The R961-1 rerun at `75db86a9` reproduced the author's log digest `413b59ca...9091`, and this round's receipt carries the same digest.

## Clean-lens evidence

[R961] PASS Conformance - `hdl/milan/usbaudio/KL_usbaudio_media.sv:62-69,111-119,161-182`, `KL_usbaudio_bridge.sv:126-130,229-259`, `author-r5/receipts-r5/physical-reports/*` - checked the delta against AUDIO-FPGA.md 9e5ef16 lines 107-178 and against criteria 1 and 2:
- whole-frame playback across state changes and silence on a coincident event;
- independent epochs;
- capture fence, apply-then-acknowledge ordering, and the published-status gate;
- the Arty route at every reported corner, with the cost recomputed from raw reports;
- ALINX programming-data identity per the receipt.
Criterion 3 is correctly left open.

[R961] PASS RTL - `hdl/milan/usbaudio/*.sv` delta (parameter guards, port renames, the deferral boundary), the `milan_datapath.sv` three-way merge (clean and equal to the head), the raw CDC, bus-skew and check_timing reports - checked:
- no CDC primitive changed;
- every guard is an elaboration-time `$error` that the 22 invalid controls trigger by name;
- the deferral cannot cancel a walk (emit and tick checked at application);
- the redundant clears at `media.sv:166-169` are harmless;
- `lint_rtl.py --check` PASS at the ratchet.

[R961] PASS Robustness - `receipts/probe-transition.log`, `receipts/reviewer-probes-*.json`, `tb/verilator/usbaudio/epochs_tb.sv:172-197` - checked these paths at the head:
- a transition during a walk, with the next epoch's frame queued: held, not consumed, not acknowledged early;
- capture change during partial interval and partial render frame: abandoned, drained and fenced;
- ordinary stall: the word is retained;
- invalid parameters: refused before simulation;
- status backpressure: capture stays closed until the acknowledgement.

Tests is UNCLEAN under N2. Docs is UNCLEAN under N1.

## Reviewer-owned ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | AUDIO-FPGA.md 9e5ef16:107-178 against the `media.sv` and `bridge.sv` deltas; criteria 1-2 evidence: plants, the default regression, 44 raw physical reports recomputed, the ALINX receipt | R961-2 | 0f7402ee97d347352b8c3d613033c440ee55986a |
| RTL | CLEAN | `hdl/milan/usbaudio/*.sv` delta; `milan_datapath.sv` merge replay; CDC, skew and check_timing reports; lint ratchet | R961-2 | 0f7402ee97d347352b8c3d613033c440ee55986a |
| Robustness | CLEAN | Directed transition probe; reviewer probes p1-p9; `epochs_tb` stall, partial-interval and partial-frame paths; parameter refusals | R961-2 | 0f7402ee97d347352b8c3d613033c440ee55986a |
| Tests | UNCLEAN (N2) | `media_tb.sv`, `epochs_tb.sv`, `transport_mutations.py`, `mutations.py`, `check.py`, `parameters_test.py`, `Makefile`; 9 delta plants; 9 reviewer probes; F1 gates | R961-2 | 0f7402ee97d347352b8c3d613033c440ee55986a |
| Docs | UNCLEAN (N1) | `USB_AUDIO_PATH.md`, `CI_WORKFLOWS.md`, `REGISTER_MAP.md` plus the generator and its prose source, generated audit and matrices, the YAML comment, the PR body, the author packet (R1) | R961-2 | 0f7402ee97d347352b8c3d613033c440ee55986a |

RESIDUE R1 does not affect coverage. The manager carries it to the residue checklist.

## Real limits

- No synthesis, implementation, or ALINX payload comparison was run here. The route is judged from the published text reports. The checkpoint and payload bytes are receipt-only, by the manager's disposition.
- **Two timing models, not four.** "Four corners" is two timing models (Slow and Fast) times two temperature settings. The 0 C and 85 C reports carry identical slack, and the grade file says so.
- **Narrow setup margin.** The +0.006 ns setup margin belongs to that single recorded route.
- **Disabled Arty comparison.** It first missed setup by 0.008 ns and passed (+0.002 ns) after physical cleanup. It is a cost baseline, not this PR's shipping claim.
- Not run here: the builder bank, the Yosys bank, the full parent banks, the 44-step docs workflow and the million-frame duplex. For these I rely on the author's receipts, which I verified by hash.
- **Hosted evidence at this head has no executed code verdict.**
  - The first failure was `firmware-aecp-mutants (1)`, an infrastructure failure: the package mirror returned 403 during dependency resolution, and the campaign step was skipped (`receipts/hosted-aecp-mutants-failure.txt`).
  - Fail-fast then cancelled the Verilator shards and the aggregations. The snapshot is 68 cancelled, 14 failure, 15 success, 1 skipped (`receipts/hosted-check-runs.tsv`).
- The em-dash renderer gate was not run. This report contains no U+2014.

## Pending manager duties

- No manager source bank exists at this head, and none is claimed or inferred.
- **The merge-turn candidate is the manager's.**
  - The PR's base branch is `dev-soft-core`.
  - The branch already merged dev `71bad8c0`, which is newer than the stated source base `4df125b8`.
  - The stated live dev `e275d795` (2026-11-17) is not a descendant of `4df125b8` in this clone's remote refs.
  - The candidate base therefore needs confirming before validation.
- Hosted and local-replica acceptance belong to the manager: rerun after the infrastructure failure.
- Choose the owning lane for N1, whose root also exists at the network head.
- Bench acceptance (criterion 3) and physical calibration were NOT RUN, and field skips are not hardware proof.
- Concurrent network operation still requires A2 wiring.

R961-2 FINISHED
