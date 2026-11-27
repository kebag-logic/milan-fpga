[R961] NEGATIVE - exact head 75db86a926a9f4d2f7734246eac06a8f58c57bac

# R961-1: internal independent review of PR #1024 (issue #1021)

- Exact head `75db86a926a9f4d2f7734246eac06a8f58c57bac`, tree `2e369a1b046f89e354d02fa7b465b5bcb787293b`; source base `4df125b8c11f0e1706b3c1e489f3e66a5d856b18` (24 commits).
- Contract: kebag-logic/usb-audio `docs/AUDIO-FPGA.md` as merged at `9e5ef16cfbbcc26722bfef56081b992a5e8fc89f` (PR #9).
- Reviewed in a cleared context from public state only: AGENTS.md, CONTRIBUTING.md, docs/README.md, issue #1021 (body; it carries no comments), the PR body and comments, the contract, the diff and history, the published evidence tree `63928dd4:review-evidence/usbaudfpga-r1/author`, and exact-head hosted check runs.
- Prior review reports in that tree were read only after the verdict and the ledger below were written.
- All five lenses were applied.
- The verdict is NEGATIVE. Two MAJOR and two MINOR findings are open: the head fails three repository gates, and the bridge's capture-epoch fence and acknowledgement wiring has no test that can catch a defect in it.

## Scope reconstruction

- **Delta topology.** The branch merges PR #1020's head `cc49123d` (`2d4c5930`), then adds the audio transport. The 22 files #1020 changes are byte-identical at this head to their #1020 blobs (`receipts/network_identity.txt`, 22/22 SAME). The audio-owned delta is 42 files (`receipts/audio_files.txt`). The network files were not re-reviewed here; they belong to #1020.
- **Acceptance criteria** (issue body, frozen):
  1. Simulation of both directions at 8x8, bit-exact, with no gaps or duplicates over a long run, and a planted defect for each interface rule.
  2. The Arty route meets every corner, the cost is stated, and the ALINX images are identical.
  3. Bench loopback.
- Criterion 3 is not claimed ("Relates to #1021"). That is correct.

## Findings

### F1 MAJOR: three repository gates fail at this head

- **Lenses:** Docs, Tests.
- **Artifacts:**
  - `hdl/milan/milan_datapath.sv:400-413` (fourteen new `usb_*` ports);
  - `docs/AAF_LATENCY_TAPS.md:18-26`;
  - `docs/DOCUMENTATION_AUDIT.md`;
  - new `configs/endstation_arty_usbaudio.yaml` and `docs/design/USB_AUDIO_PATH.md`.
- **Evidence:**
  - `python3 scripts/check_solution_docs.py` reports `FAIL (14 findings)`, one "unclassified RTL port" for each new `usb_*` datapath port. It passes at `2d4c5930` (`receipts/solution_docs.txt`).
  - `sw/builder/test_clock_contract.py:test_tap_clock_docs` reports "tap clock table differs from the configurations": the configured-tap table has no row for the new configuration. It passes at `2d4c5930` (`receipts/tap_clock_docs.txt`).
  - `python3 scripts/docs_inventory.py --check` reports `STALE (368 lines differ)`. It is fresh at the base and at `2d4c5930`, and stale from `cb139f14` (`receipts/docs_inventory.txt`, `receipts/docs_inventory_history.txt`).
  - The hosted exact-head jobs that ran these gates failed for the same reasons (`receipts/hosted_docs_gate_failures.txt`): `docs-gates-0` (job 140338094584) and `docs-gates-2` (job 140338094721).
  - The other hosted failures are aggregation and ownership steps over cancelled shards (`receipts/hosted_failed_steps.txt`, `receipts/hosted_check_runs.tsv`). So no exhaustive Verilator or Yosys result exists at this head.
  - The published validation (`r3-validation.md`, row "Source idiom and documentation") reports PASS, but its gate set did not include these three.
- **Impact:** merging lands `dev` red on mandatory documentation and builder gates. The builder leg stops at its first failure, so the builder tests after `test_tap_clock_docs` are unobserved at this head.
- **Required outcome:**
  - classify the fourteen ports in the solution documentation;
  - add the `endstation_arty_usbaudio` row to the configured-tap table;
  - regenerate the documentation audit;
  - then show the documentation workflow gates and the builder gates passing at the new head.
- **Verification:** the three commands above return 0, and hosted `docs-gates-*` pass at the new head.

### F2 MAJOR: the bridge's capture-epoch fence and acknowledgement wiring is untested

- **Lens:** Tests.
- **Artifacts:**
  - `hdl/milan/usbaudio/KL_usbaudio_bridge.sv:126` (`capture_abort_o`), `:246` (status echoes `applied_epoch_r`) and `:252-253` (capture enable gated on the applied and published epochs);
  - `tb/verilator/usbaudio/duplex.cpp:52-53` and `:195` (epochs fixed at 1 for the whole run).
- **Authority:** AUDIO-FPGA.md:138-144 and :172-175. The FPGA must abandon the partial interval, reset to channel zero and apply the new capture state before echoing the epoch. Only a matching published acknowledgement opens capture.
- **Evidence:** `scripts/probe_bridge_mutants.sh` planted four single-line defects in a copy of the bridge. It ran every shipped harness that instantiates the bridge (duplex at the default-regression window, and `levels_tb`). Result in `receipts/probe_bridge_mutants.txt`:

  | Planted defect | Result |
  |---|---|
  | Applied-epoch gate removed from the capture enable | Passes every harness |
  | `capture_abort_o` tied low (no packetizer or bus fence) | Passes every harness |
  | Status echoes the bus-side epoch before the media domain applies it | Passes every harness |
  | Published-status gate removed | Caught (`CAPTURE_ACK_BEFORE_DATA`) |

  - The 70 named campaign plants target leaf modules. The bridge carries only the three level-launch plants.
  - The leaf tests (`packet_tb`, `media_tb`) drive `fence_i` and the acknowledgement as stimulus. So a missing or misordered bridge fence cannot fail any test.
  - Neither the long run nor the default duplex ever changes an epoch.
- **Impact:** the explicitly acknowledged capture-epoch boundary is a core interface rule. A regression in its integration would release unfenced or old-epoch capture packets, and no test would notice. The rule's wiring is unproven by test, although I read the RTL as correct today.
- **Required outcome:** an integrated test, at bridge level or wider, that performs capture-only and playback-only epoch changes mid-stream (including during a partial capture interval). It must check abandonment, the channel-zero restart, the media-applied acknowledgement order and the published-status gate. Each of the three surviving plants above must fail it by name.
- **Verification:** re-run the probe; all four plants must be caught.

### F3 MINOR: a playback state change on a grid event or during the pair walk drops that event's whole frame, uncounted

- **Lenses:** Conformance, RTL, Robustness, Tests.
- **Artifacts:**
  - `hdl/milan/usbaudio/KL_usbaudio_media.sv:105`: `!playback_changed_w` suppresses the grid event;
  - `KL_usbaudio_media.sv:154-163`: `state_take_w` with a new playback epoch clears `emit_r`, truncating a walk in progress;
  - `hdl/milan/milan_datapath.sv:1585`: the capture mapper's `tick_i` is `usb_capture_tick_i` alone in the audio build.
- **Authority:**
  - AUDIO-FPGA.md:113-114 and :117-120: a complete frame on every grid event, and no uncounted gaps;
  - `docs/design/USB_AUDIO_PATH.md:56-57` ("Before priming or while inactive, the mapper receives whole silent frames on the media grid").
- **Evidence:** `scripts/probe_media_grid_tb.sv` (output in `receipts/probe_media_grid.txt`). A playback epoch change applied 0 to 6 cycles after a grid event loses that event's `capture_tick_o`, in 7 of 8 offsets. The probe ends with 20 grid events and 13 snapshots, while `gaps=0` and `error=0`.
  - At the 50 MHz media clock this is about 7 of 1,042 cycles for each playback epoch change. Records arrive with no phase relation to the grid, so the case is reachable in the integrated design.
  - `media_tb.sv` applies every state change away from the grid, so no test covers it.
- **Impact:** the AVB talker path misses one mapper snapshot. The talker stream is one frame short at that grid instant, with no counter and no sticky error.
- **Required outcome:** every grid event yields exactly one whole-frame walk and snapshot, whatever the state changes. One way is to defer a playback epoch application until the walk completes and walk silence for that event. Otherwise the miss must be counted as a gap with sticky error. Add a test that applies playback state at every offset of the grid event and the walk.
- **Verification:** the probe reports `EVERY_GRID_SNAPSHOT`, and a named test fails on the current behaviour.

### F4 MINOR: the long-run harness's clock description is inaccurate

- **Lenses:** Docs, Tests.
- **Artifacts:**
  - `docs/design/USB_AUDIO_PATH.md:125` ("independent bus, media and oscillator clocks");
  - `tb/verilator/usbaudio/duplex.cpp:118-121` (bus edge every 4 steps, media every 2: a fixed 1:2 ratio and phase);
  - `duplex.cpp:151-152` (six frames every 6,250 bus cycles, the oscillator grid's exact rate).
- **Evidence:** only the oscillator is incommensurate. The bus-to-media crossings never see phase drift. Playback supply and consumption are exactly matched, with no 5-frame or 7-frame intervals. `levels_tb.sv` uses 20/26 ns clocks, but only for the level synchronizers.
- **Impact:** a reader of the design document and the PR body takes the million-frame result as covering bus/media phase drift and rate mismatch, and it covers neither. This corrects a claim about what a test covers, so it is not RESIDUE.
- **Required outcome:** either state the actual conditions, or let the duplex drift the bus clock against the media clock and vary record sizes under a supply that tracks the grid.
- **Verification:** the text matches `duplex.cpp`, or a drifting run passes.

### F5 RESIDUE: the contract citation is the pre-merge revision

- **Lenses:** Docs (residue checklist; it does not affect coverage).
- **Artifacts:** `docs/design/USB_AUDIO_PATH.md:4` and the PR body cite `47e6bbc9`; `configs/endstation_arty_usbaudio.yaml:6` cites `ae4b11bd`.
- **Evidence:** the merged `9e5ef16` differs from `47e6bbc9` only in the FX3 link-failure paragraph, AUDIO-FPGA.md:246-257 (`receipts/contract_47e6bbc9_vs_9e5ef16.diff`). The FPGA duties and the digest `0xffdc84ff` are identical at all three revisions.
- **Exact fix:** in `docs/design/USB_AUDIO_PATH.md:4` and the PR body, replace the link with `https://github.com/kebag-logic/usb-audio/blob/9e5ef16cfbbcc26722bfef56081b992a5e8fc89f/docs/AUDIO-FPGA.md`, labelled "USB audio #9 as merged, 9e5ef16". In the YAML comment, write "at 9e5ef16cfbbcc26722bfef56081b992a5e8fc89f".

### Suggestions (optional; they do not affect coverage)

- **S1** (RTL, Robustness): `KL_usbaudio_gpif.sv:61,82,127-129`. A capture word is latched, and SLWR# asserted, on `capture_valid_i` sampled in `CHECK_S`. `capture_ready_o` then asserts in `WRITE_S` without re-checking valid. The bridge's valid includes `locked_o`, which can fall on watchdog expiry or media-lock loss. When it does, a word reaches the FX3 that the packetizer will send again. The contract's re-epoch after a validity loss masks this today. Make the accepted word the written word.
- **S2** (Conformance, Robustness): `KL_usbaudio_reference.sv:41-44`. The 0.75 to 1.25 ms delivery guard is tighter than the contract's firmware spacing (under 2 ms plus transfer, AUDIO-FPGA.md:259-263). Any delivery jitter above ±0.25 ms drops lock for a full 1.024 s window. It is disclosed as a desk bound; consider making it a parameter tied to the bench measurement.
- **S3** (Tests): the cleanup-ledger options in `tb/verilator/usbaudio/check.py:21-40`, `mutations.py`, `transport_mutations.py:223-260` and `Makefile:13` encode a lane procedure that no other harness carries. Consider removing them.
- **S4** (Docs): `USB_AUDIO_PATH.md:105`. Qualify "Boundary tests accept 2.9 ms and refuse 3 ms" with the test's condition (`reference_tb.sv:104-107`): source-clock timestamps are held at 1 ms. In the integrated design, a record 2.9 ms late is refused by the delivery guard.

## Clean results within otherwise unclean lenses (evidence for the ledger)

- **Conformance.** The duties in AUDIO-FPGA.md:107-144, 164-178, 182-281 and 285-306 are implemented, except F3:
  - record header, digest, flags and length checks (`KL_usbaudio_record.sv:81-101`);
  - interval structure (`KL_usbaudio_ingress.sv:49-54`);
  - continuity, delta and 3 ms own-clock watchdog (`KL_usbaudio_reference.sv:28-53`);
  - E << (16-K) (`KL_usbaudio_feedback.sv:42`);
  - status layout and sequence (`KL_usbaudio_status.sv:38-46`);
  - packet rules (`KL_usbaudio_packet.sv:73-100`);
  - 32-bit retention through the render queue, mapper and packetizer, with AAF `bit_depth` 32 already set (`KL_aaf_packetizer.sv:533`; IEEE 1722-2016 7.3.4);
  - digest `0x84ff` and window 13 match the merged generated package.
- **RTL.**
  - CDC uses only vendored async FIFOs, a 48-bit Gray counter with a skew bound, and two-flop level synchronizers launched from registers (`KL_usbaudio_bridge.sv:70-87`, `sw/litex/usbaudio_cdc.tcl`).
  - Resets assert asynchronously and release on local edges in every domain.
  - New-epoch frames cannot overtake their state in the media domain, because the state write precedes the first PCM write by a bus cycle.
- **Build exclusion and identity.** `usbaudio_build.py:21-24` rejects audio with network, and audio on non-Arty boards. The shared blocks default to 24 bits. The source hashes cited by the ALINX lineage match this head (`receipts/head_source_sha256.txt`).

## Executed evidence

All runs used Verilator 5.050 (pinned binary, identity checked; `--version` reports `5.050 2026-07-01 rev v5.050`).

| Run | Result | Receipt |
|---|---|---|
| Default audio regression (`check.py`) | PASS, rc 0 | `receipts/runs/default_regression.log` |
| Full-window duplex, 1,000,000 frames, window 13 | PASS: 37,419,648 checks, 0 failures, 999,993 capture frames, feedback `0x00060000`, 1 reference loss. Log sha256 `413b59ca...9091` equals the author's recorded digest. | `receipts/runs/duplex_window13_1000000.log` |
| Transport defect campaign | 46/46 CAUGHT, 5/5 baselines PASS | `receipts/runs/transport_defects_results.json` |
| Protocol defect campaign | 24/24 CAUGHT | `receipts/runs/protocol_defects_results.json` |
| Render-queue harness, 24 and 32 bits | PASS, 39 checks each | `receipts/runs/render_queue_{24,32}.log` |
| RTL lint ratchet; SV, Python, C++ and shell idiom gates; `docs_check.py`; doc style; feature status; submodule docs; entity shape; SoC sources; wire accountability; gPTP docs | PASS | `receipts/lint_rtl.txt`, `receipts/idiom_*.txt`, `receipts/docs_check.txt`, `receipts/focused_doc_gates.txt` |
| Solution docs, tap-clock table, documentation inventory | FAIL (F1) | see F1 |
| Bridge plants (F2), media-grid probe (F3) | see findings | `receipts/probe_*.txt` |

## Prior review findings, reconciled at this head (read after the verdict above)

- **Earlier internal-review round at `ba2a66f7`.** Its three earlier findings are pad placement, combinational launch and suppressed hold. I find all three **resolved at this head**:
  - `usbaudio_pack.tcl` and the packing grader's 55 endpoints with twelve controls pass in the default regression;
  - `KL_usbaudio_bridge.sv:70-73` registers the levels, and the three launch plants are caught;
  - `usbaudio_timing.xdc:12-13` keeps an ordinary `set_max_delay`, not `-datapath_only`, so the hold check stays.
- **Internal review at this head, MAJOR execution-compliance finding** (`r3-cleanup-exception.md`). This concerns the author lane's procedure, not the repository delta. I can neither verify nor resolve it from public artifacts. I **retain it** as open for maintainer disposition, and it is not one of my lens findings.
- That round's Tests and Docs PASS lines do not cover F1 and F2, which are new here.

## Reviewer-owned ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F3) | AUDIO-FPGA.md at 9e5ef16 against the record, ingress, reference, feedback, status, packet, media and bridge RTL; AAF storage path; IEEE 1722-2016 7.3.4 | R961-1 | 75db86a926a9f4d2f7734246eac06a8f58c57bac |
| RTL | UNCLEAN (F3) | All twelve `hdl/milan/usbaudio/*.sv`; the shared AAF, mapper and render-queue diffs; `milan_datapath.sv`; `usbaudio_soc.py`; timing and CDC constraints | R961-1 | 75db86a926a9f4d2f7734246eac06a8f58c57bac |
| Robustness | UNCLEAN (F3) | Malformed, epoch, backpressure, reset, watchdog and loss paths, plus the media-grid probe | R961-1 | 75db86a926a9f4d2f7734246eac06a8f58c57bac |
| Tests | UNCLEAN (F1, F2, F3, F4) | Every harness in `tb/verilator/usbaudio`, both campaigns, the full duplex, the render-queue harness, the bridge plants, the repository gates | R961-1 | 75db86a926a9f4d2f7734246eac06a8f58c57bac |
| Docs | UNCLEAN (F1, F4) | `USB_AUDIO_PATH.md`, `docs/README.md`, the generated audit, the tap table, the solution docs, the PR body, the evidence receipts | R961-1 | 75db86a926a9f4d2f7734246eac06a8f58c57bac |

## Limits and pending manager duties

**What this review could not check:**
- The raw timing, packing and utilization reports are not in the published evidence; only their hashes are. So setup +0.002 ns, hold +0.018 ns and pulse +1.389 ns are checked against the route receipt (`r3-arty-route.json`), not the report bytes.
- The +0.002 ns margin is specific to that single recorded artifact (one physical attempt, not a directive sweep). The two junction settings are one delay model each, not four libraries; the receipt says so.
- No synthesis, implementation or ALINX payload comparison was run here.
- The em-dash gate was not run: its pinned renderer is not installed. A direct scan of the added lines finds no U+2014.
- The builder bank, the Yosys bank and the full parent banks were not run (out of scope).

**What remains for the manager and maintainer:**
- No manager source bank exists at this head. The merge-turn current-dev candidate validation is the manager's (live dev `e275d795`).
- Hosted and act acceptance belong to the manager. At this head the hosted run has executed failures and cancelled shards (F1).
- Bench acceptance (criterion 3) and physical calibration were NOT RUN, and skips are not hardware proof.
- The disposition of the execution-compliance exception is the maintainer's.

**Clone state:** verified after the probes. Every tracked blob and mode equals the index (2,034 files, 0 mismatches), the index tree equals the head tree, the status is empty, and the six gitlinks are unchanged (`receipts/clone_integrity.txt`).

R961-1 FINISHED
