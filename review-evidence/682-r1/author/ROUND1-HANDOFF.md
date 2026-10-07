
The following evidence belongs to the previous head and is retained as history; it is not round-2 validation.

# Issue 682 author handoff

Role: [A554], executor. Reviewers: [R520] internal, [R521] external.
Status: STOP / blocked at `1e99ad217f0747c33e03238f7d1c633c07ce572c`. Items 1-5 are complete. Full acceptance fails the render campaign at 28/32 (rc 2); fresh builds reproduce all four failed cases with committed inputs stable. Issue #682 has no exception for open #657. The worktree and processor checkout are clean; six one-line commits are retained locally. No review-ready claim is made.
Public STOP: https://github.com/kebag-logic/milan-fpga/issues/682#issuecomment-6028310880
Branch: `682-pp-pin-2ad2f845`.
Base: `bd884631684ccf5060339efa92263d5c3e5c262c`.
Origin verified: `https://github.com/kebag-logic/milan-fpga.git`.
Assignment: https://github.com/kebag-logic/milan-fpga/issues/682#issuecomment-6018127147
The explicit assignment authorizes execution; the board still shows Backlog.

## Ordered status

1. Pin complete. Only the processor gitlink changes, from `ead8036035affd53ef4b29979190f2f4f67084c0` to `2ad2f845dd583f8310075fa2380cb60a04fd091a`. It was fetched from the assigned public upstream and checked out detached after verifying the submodule's top-level directory. The processor top is byte-identical at both pins: 237,956 bytes, SHA-256 `84d89afb652b3db646fd86a13e301c9de89005607b9d8fa896eb38f365a0e170`.
2. Both supplied patches applied without context repair. The initial xvlog check returned zero with no finding in 81 parent, 46 protocol-processor and six gPTP files. The final-head repeat also returns zero with no findings.
3. Pin-derived records regenerated and repeated byte-identically. Test-evidence dispositions are unchanged: 72/77 no-mutant, 10/10 unseeded, zero unexplained readers, three wall-clock cases, 60 default suites and 99 inventory entries.
4. Combination E recorded through the repository generator. Both standalone syntheses and the clean image synthesis and implementation have successful process receipts. All three endpoint checks and the policy check return zero at the committed head. Policies are unchanged.
5. Saved capture receipt passes at the committed head. Firmware source digest is unchanged, so remeasurement is not required.
6. Blocked. The full render mutation campaign returns rc 2, 28/32, matching #657. A fresh unmodified epoch build reproduces four T30 CRF failures with committed inputs stable. The supplied notification patch passes its direct 421-check target. The broad parent sweep was then cancelled through its repository process owner after 10/60 suites passed; rc 143 is a cancellation, not a gate result. The remaining parent bank steps and section 5 bitstream/manifest completion were not started. All three routes completed with rc 0 and fully routed, error-free nets; ExtraTimingOpt passes the numerical slack floor at every corner, but route-only checkpoints do not qualify complete images.
7. Remote dev is `79b086d44eb62d007d38e18f5618b98e8e2a33e6`: 32 commits beyond the assigned base, with no overlapping changed paths. `dev-comparison.json` records the complete file list and fetch receipt. This execution request forbids merge and rebase, so item 7 remains with the manager. Incoming changes include `KL_aaf_packetizer.sv`, firmware/NVM sources and the suite driver: no-path-overlap is not validation. Integration must recheck resource input digests, apply the re-baseline rule where inputs changed, recheck the capture source digest and remeasure if required, and rerun affected gates.

## Patch hunk mapping

| Patch | Parent hunk | Processor change answered |
|---|---|---|
| `parent-adoption-148-6c22d3ca.patch` | `tb/verilator/milan_dp/sim_nxn.cpp:964`, comment and loop at line 973 | PR 159 moves the counter-notification spacing stamp from selection toward each job send. The later frame can cross a 10 ms observation boundary; the harness now completes an in-progress frame for at most 2,048 additional cycles. |
| `parent-adoption-22-28f9666f.patch` | `scripts/xvlog.budget:33` | PR 162 moves existing declarations before use in the originator and RX validator. The two retired finding identities leave the processor section empty. |

Both patches applied without context repair. No expectation, parent RTL, firmware or interface was edited.

## Parent-visible changes

| Processor PR | Parent-visible result |
|---|---|
| [156](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/pull/156), C11 | Documentation now describes the landed byte interfaces, TX backpressure, synchronous reset and whole FCS-good RX frames. Parameter/timing ID and figure checks strengthen donor documentation validation. No interface change. |
| [159](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/pull/159), 148 | GET_COUNTERS spacing follows every waiting job through grant; supplied frame-completion harness patch is required. No port, parameter or register change. MAC stalls after grant remain a disclosed wire-spacing limit. |
| [160](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/pull/160), 134 | Registrar expiry followed by same-cycle reception preserves expiry for Lv/LeaveAll and renewal for New/Join. No parent interface change; manager repeats withdrawal cycles after merge. |
| [161](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/pull/161), 158 | A held DEREGISTER waits for the notification round boundary, preserving later jobs. Its target and contents stay the same; delivery may be later. No port, parameter or register change. |
| [162](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/pull/162), 22 | Declaration ordering only; supplied parent budget patch removes two findings. Synthesis warning count remains this adoption's obligation. |
| [164](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/pull/164), 42 | Test-only Domain/link notification coverage; the parent continues to own the GET_AVB_INFO mapping words. No RTL, port, parameter or register change. |

The six PR bodies were read from public state. No private transcript was used.

## Pin-derived record map

| Record | Regeneration and result |
|---|---|
| `syn/yosys/rom_digests.tsv:15` | `bash syn/yosys/ooc.sh --record-rom-digests`; two new pin rows, unchanged ROM contents |
| `docs/reference/SUBMODULES.md:25` | Repository index pin reader plus existing parsed table metadata; processor pin updated |
| `docs/diagrams/submodule_boundaries.drawio`, `.svg`, `.png` and `PNG_MANIFEST.json` | `python3 docs/diagrams/submodule_boundaries.gen.py`; diagram pin and raster digest updated |
| `scripts/port_docs.budget:21` | `python3 scripts/check_port_contracts.py --write-budget`; census header refreshed, identities unchanged |
| `syn/ooc/pp_resource_baseline.json` | `python3 syn/ooc/pp_resource_gate.py record <report-directory> --endpoint <route-1x1, ooc-1x1 or ooc-8x8> --write`; all three repeated records are identical, with unchanged policies |
| Naming budget | `python3 scripts/measure_naming.py --write-budget`; identical output |


The ROM contents stay unchanged: LTN SHA-256 `23cc67eeadc7ecad8c9ceb7f9391095b64ada44d4e0f3a232ce82a2a69e7e956`; microcode SHA-256 `518b900c4a5650902c3ea9125941e434857ba2f379b6c92268a67fef459d37f8`. Two new ledger rows bind them to the new pin. There is no dedicated pin-page writer; its table was derived using the repository's `gitlink_pins()` index reader and parsed table metadata. The diagram raster was visually checked. The port census header changes from 1,940 to 2,077 parent ports; processor count 1,759 and all ratchets are unchanged. Naming remains byte-identical at 95 identities. `current-records.json` binds all 16 changed parent files and the gitlink to the committed head.

## Resource baseline E

| Endpoint | LUT | FF | Slice | RAMB36 / RAMB18 | BRAM tiles | DSP | CARRY4 | WNS / WHS, ns |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Routed 1x1 image | 49,888 | 54,267 | 15,805 | 74 / 27 | 87.5 | 14 | 3,385 | +0.101 / +0.031 |
| Standalone 1x1 | 23,179 | 19,779 | n/a | 16 / 3 | 17.5 | 8 | 1,494 | -3.562 / +0.159 |
| Standalone 8x8 | 30,135 | 27,380 | n/a | 21 / 5 | 23.5 | 8 | 1,889 | -2.278 / +0.159 |

Standalone timing is an ungated synthesis estimate. Routed timing is the acceptance result. All 101,135 routable nets are routed with zero routing errors. The routed processor wrapper has 23,094 LUT and 18,784 FF; the enclosing datapath has 41,356 LUT and 43,038 FF. The device has 45 unused slices. LUT use is 78.69%; the separate 60% area objective remains unmet by 11,848 LUT and is still tracked by the existing redesign work.

The generated flow now records the opt-in `--single-thread-synthesis` setting (`set_param synth.maxThreads 1`). The default generated output remains byte-identical. The existing six-argument preparation interface is preserved. CLI controls and all 34 baseline mutants pass, including ignored-flag and default-on defects. This is a flow change, so comparison with baseline D correctly returns diagnostic rc 2, NOT COMPARABLE. Those diagnostics are not acceptance gates. The old and new numeric rows are preserved in the authoritative finding; the raw delta is not attributed solely to the processor pin because intervening parent changes and the synthesis worker setting also differ.

The clean measurement used unchanged RTL inputs from `2a97d4e8874a90a620d2b9234620eff9aec57bcb`. Final-head endpoint checks verify those same input digests at `1e99ad217f0747c33e03238f7d1c633c07ce572c`. `effective-recipes.json` records byte-identical regeneration and the shipping-export digests; `resource-recording-receipts.json` records each generator command, repeated recording and check. `resource-artifacts.json` records sizes and SHA-256 for the large reports, logs and checkpoints retained outside this packet.

### Synthesis declaration warnings

`synth-86901.md` and `synth-86901.json` report all 46 directly read protocol-processor design files, each with zero Synth 8-6901 warnings in clean image synthesis and both standalone runs. The 52-file pinned-source xvlog census consists of these 46 files plus six gPTP files. Each synthesis separately has one parent warning for `crft_emit_en_w` at `hdl/milan/milan_datapath.sv:3168`. Processor issue #22 therefore meets its zero-count closure condition; no globally warning-free claim is made. The PR 162 diff was also inspected manually: it only relocates bare logic declarations in the originator and RX validator; it does not replace a declaration initializer with a continuous assignment. No xelab gate is claimed.

## Capture check

`python3 scripts/check_nvm_capture.py` exits 0 at `1e99ad217f0747c33e03238f7d1c633c07ce572c`. The firmware source hash, harness hashes, census, clocks and both timing arms match the saved receipt. Maxima: 1x1 at 50 MHz 3.96728 ms; 8x8 at 50 MHz 13.86484 ms; 8x8 at 100 MHz 10.42973 ms. The 8x8 acceptance limit is 24.5 ms. This validates retained measurements; it is not a new simulator timing measurement.

## Three-directive timing

| Placement directive | Minimum WNS, ns | Minimum WHS, ns | Status |
|---|---:|---:|---|
| ExtraPostPlacementOpt | +0.101 | +0.031 | All corners pass |
| AltSpreadLogic_high | -0.857 | +0.008 | Setup fails; not selected |
| ExtraTimingOpt | +0.334 | +0.021 | Best; all corners pass |

Default Slow 0/85 C corners are +0.101 / +0.085 ns; Fast 0/85 C corners are +1.492 / +0.031 ns. AltSpreadLogic_high Slow corners are -0.857 / +0.102 ns; Fast corners are +1.326 / +0.008 ns. The default's worst setup path is the CPU DMA write bridge, 21 logic levels and 9.871 ns data delay. ExtraTimingOpt Slow 0/85 C corners are +0.334 / +0.056 ns; Fast 0/85 C corners are +1.633 / +0.021 ns. Its worst setup path runs from `milansoc_write_w_buffer_level0_reg[0]/C` to `storage_10_dat1_reg[20]/D`, with 14 logic levels and 9.296 ns data delay. AltSpreadLogic_high fails in the processor notify-to-transmit-arbiter cone (`wr_ix_r_reg[0]/C` to `slot_r_reg[1]/D`), with 42 levels and 20.907 ns data delay. `timing-directives.json` retains the five worst setup and two worst hold paths, all corner values, utilization and report digests for every directive. The resource baseline remains the prescribed ExtraPostPlacementOpt cell; it is distinct from selection of the best timing directive. The acceptance floor is best-directive WNS at least +0.03 ns and WHS at least zero at every corner.

The route-only records establish slack but do not yet qualify complete images under BUILDING.md section 5. The prepared continuation opens each final routed checkpoint, reuses the shipping-generated report and bitstream tail, and performs no synthesis or placement. Its unexecuted plan runs the repository constraint-log gate, generates the flash layout through `layout_from_soch.py`, and verifies the bitstream/AEM binding through `check_gptp_owner_pair.py`. No result is claimed for that plan. Existing compiled software and AEM bytes are retained and hashed.

The completed route reports have zero no-clock and unconstrained internal endpoints. They disclose 46 input ports with no input delay under false-path constraints and 87 output ports with no output delay. CDC diagnostics remain visible, including ten CDC-10 critical rows in the best directive; positive slack does not discharge them. All four Ethernet/system-Milan clock pairs carry an 8 ns Max Delay Datapath Only constraint with positive slack and no unsafe clock pair. No emitted 12-4739, 20-1307 or 12-5201 diagnostic occurs in any completed implementation. AltSpreadLogic_high emits Route 35-39 for its setup failure. The full critical-warning census and all four slack metrics per corner are retained in `signoff-details.json`. Slow/Fast use fixed speed models; the 0 C and 85 C power-temperature endpoint reports repeat those models rather than applying temperature interpolation.

## Gate table

All rows below belong to full head `1e99ad217f0747c33e03238f7d1c633c07ce572c`; each row displays its unambiguous prefix. There are 85 completed or cancelled command records: 82 return zero, the full render campaign returns 2, its fresh four-case diagnostic returns 1, and the deliberately cancelled parent sweep returns 143. Return zero is a process result, not a claim that intentionally unrun arms were covered.

The processor sweep passes 33 suites and 1,028,250 checks. The gPTP contract/tests/lint command passes. BDD passes 14 features, 404 scenarios and 1,968 steps with no skips. The focused notification target passes 421 checks. The original synthesis sweep reports 58/58 tops and both structural gates; its two shared-header consumers pass fresh repeats, followed by passing three-top elaboration. All 49 literal documentation workflow steps use GNU Make 4.3. The host builder returns zero with two unrun arms: the ineffective MAKEFLAGS mutation under this Make version and the absent historical calibration report. The documentation job’s restricted builder environment reports 16 unrun arms; its separate compiler-absent controls report three unrun arms by design. Installed-environment checks do not erase those recorded dispositions.

`GATE-COMMANDS.md` gives every exact shell command, working directory, full head, return code, log digest and size; `gate-receipts.json` is the structured equivalent. The capture receipt is recorded separately above. `partial-parent-sweep.json` and `acceptance-cancellation.json` preserve the 10 completed suites and cancellation. The complete-image plan, parent tally, physical-gPTP simulation, NVM lint/quick, LiteX driver controls and four LiteX simulations were not run after the blocker was confirmed.

| Gate | Head | Make version | rc |
|---|---|---|---:|
| markdown 01: markdown-docs | `1e99ad217f07` | GNU Make 4.3 | 0 |
| markdown 02: markdown-toc-controls | `1e99ad217f07` | GNU Make 4.3 | 0 |
| markdown 03: markdown-anchor-check | `1e99ad217f07` | GNU Make 4.3 | 0 |
| markdown 04: markdown-toc-check | `1e99ad217f07` | GNU Make 4.3 | 0 |
| parent 01: render-full | `1e99ad217f07` | GNU Make 4.3 | 2 |
| parent 02: parent-sweep-cancelled | `1e99ad217f07` | GNU Make 4.3 | 143 |
| patch 01: notification-patch | `1e99ad217f07` | GNU Make 4.3 | 0 |
| processors 01: processor-sweep | `1e99ad217f07` | GNU Make 4.3 | 0 |
| processors 02: gptp | `1e99ad217f07` | GNU Make 4.3 | 0 |
| processors 03: bdd | `1e99ad217f07` | GNU Make 4.3 | 0 |
| processors 04: builder-elaboration | `1e99ad217f07` | GNU Make 4.3 | 0 |
| resources 01: route-1x1 | `1e99ad217f07` | GNU Make 4.3 | 0 |
| resources 02: ooc-1x1 | `1e99ad217f07` | GNU Make 4.3 | 0 |
| resources 03: ooc-8x8 | `1e99ad217f07` | GNU Make 4.3 | 0 |
| resources 04: policy | `1e99ad217f07` | GNU Make 4.3 | 0 |
| stable-header 01: yosys-stable-header | `1e99ad217f07` | GNU Make 4.3 | 0 |
| stable-header 02: fast-elaboration-stable-header | `1e99ad217f07` | GNU Make 4.3 | 0 |
| stable-header 03: render-four-cases-stable-header | `1e99ad217f07` | GNU Make 4.3 | 1 |
| synthesis 01: lint | `1e99ad217f07` | GNU Make 4.3 | 0 |
| synthesis 02: pp-sources | `1e99ad217f07` | GNU Make 4.3 | 0 |
| synthesis 03: scope | `1e99ad217f07` | GNU Make 4.3 | 0 |
| synthesis 04: yosys | `1e99ad217f07` | GNU Make 4.3 | 0 |
| synthesis 05: yosys-tally | `1e99ad217f07` | GNU Make 4.3 | 0 |
| synthesis 06: fast-elaboration | `1e99ad217f07` | GNU Make 4.3 | 0 |
| synthesis 07: dp-source-controls | `1e99ad217f07` | GNU Make 4.3 | 0 |
| synthesis 08: ooc-tcl-controls | `1e99ad217f07` | GNU Make 4.3 | 0 |
| synthesis 09: baseline-controls | `1e99ad217f07` | GNU Make 4.3 | 0 |
| synthesis 10: baseline-mutants | `1e99ad217f07` | GNU Make 4.3 | 0 |
| synthesis 11: baseline-reports | `1e99ad217f07` | GNU Make 4.3 | 0 |
| synthesis 12: resource-controls | `1e99ad217f07` | GNU Make 4.3 | 0 |
| synthesis 13: resource-mutants | `1e99ad217f07` | GNU Make 4.3 | 0 |
| synthesis 14: resource-baseline | `1e99ad217f07` | GNU Make 4.3 | 0 |
| synthesis 15: dp-sources | `1e99ad217f07` | GNU Make 4.3 | 0 |
| synthesis 16: yosys-ooc-controls | `1e99ad217f07` | GNU Make 4.3 | 0 |
| synthesis 17: yosys-cache-controls | `1e99ad217f07` | GNU Make 4.3 | 0 |
| vendor 01: xvlog | `1e99ad217f07` | GNU Make 4.3 | 0 |
| docs-workflow 01: Build the validated HDL reference | `1e99ad217f07` | GNU Make 4.3 | 0 |
| docs-workflow 02: Install the python gate dependencies | `1e99ad217f07` | GNU Make 4.3 | 0 |
| docs-workflow 03: Install the pinned Markdown renderer | `1e99ad217f07` | GNU Make 4.3 | 0 |
| docs-workflow 04: Install diagram gate dependencies | `1e99ad217f07` | GNU Make 4.3 | 0 |
| docs-workflow 05: Link health, wording, dead-reference and local-info gate | `1e99ad217f07` | GNU Make 4.3 | 0 |
| docs-workflow 06: Added-line em-dash gate | `1e99ad217f07` | GNU Make 4.3 | 0 |
| docs-workflow 07: Concise audience documentation gate | `1e99ad217f07` | GNU Make 4.3 | 0 |
| docs-workflow 08: Audience diagram no-drift gate | `1e99ad217f07` | GNU Make 4.3 | 0 |
| docs-workflow 09: Product solution source-fact gate | `1e99ad217f07` | GNU Make 4.3 | 0 |
| docs-workflow 10: Verified submodule documentation gate | `1e99ad217f07` | GNU Make 4.3 | 0 |
| docs-workflow 11: HDL timing diagram no-drift gate | `1e99ad217f07` | GNU Make 4.3 | 0 |
| docs-workflow 12: Published diagram PNG gate | `1e99ad217f07` | GNU Make 4.3 | 0 |
| docs-workflow 13: Milan feature-status consistency gate | `1e99ad217f07` | GNU Make 4.3 | 0 |
| docs-workflow 14: Traceability matrix no-drift gate | `1e99ad217f07` | GNU Make 4.3 | 0 |
| docs-workflow 15: Fetch the builder source dependencies | `1e99ad217f07` | GNU Make 4.3 | 0 |
| docs-workflow 16: Imported gPTP documentation gate | `1e99ad217f07` | GNU Make 4.3 | 0 |
| docs-workflow 17: Code-quality measurement self-tests | `1e99ad217f07` | GNU Make 4.3 | 0 |
| docs-workflow 18: Install the pinned sv2v release | `1e99ad217f07` | GNU Make 4.3 | 0 |
| docs-workflow 19: Bare-metal scope gate | `1e99ad217f07` | GNU Make 4.3 | 0 |
| docs-workflow 20: Install and verify the pinned RV32 SDK | `1e99ad217f07` | GNU Make 4.3 | 0 |
| docs-workflow 21: Compiler-absent firmware controls | `1e99ad217f07` | GNU Make 4.3 | 0 |
| docs-workflow 22: End-station builder gates | `1e99ad217f07` | GNU Make 4.3 | 0 |
| docs-workflow 23: NVM record-space gate | `1e99ad217f07` | GNU Make 4.3 | 0 |
| docs-workflow 24: Capture measurement census and clock gate | `1e99ad217f07` | GNU Make 4.3 | 0 |
| docs-workflow 25: Saved-state writer gate | `1e99ad217f07` | GNU Make 4.3 | 0 |
| docs-workflow 26: SoC source-list gate (Vivado would fail 40 min in without this) | `1e99ad217f07` | GNU Make 4.3 | 0 |
| docs-workflow 27: RTL source-list drift gate | `1e99ad217f07` | GNU Make 4.3 | 0 |
| docs-workflow 28: Boundary-unit naming ratchet | `1e99ad217f07` | GNU Make 4.3 | 0 |
| docs-workflow 29: Port contract gate | `1e99ad217f07` | GNU Make 4.3 | 0 |
| docs-workflow 30: Fail-fast ratchet | `1e99ad217f07` | GNU Make 4.3 | 0 |
| docs-workflow 31: TODO ownership gate | `1e99ad217f07` | GNU Make 4.3 | 0 |
| docs-workflow 32: Test-evidence ratchet | `1e99ad217f07` | GNU Make 4.3 | 0 |
| docs-workflow 33: Mechanical hygiene ratchet | `1e99ad217f07` | GNU Make 4.3 | 0 |
| docs-workflow 34: SystemVerilog idiom gate | `1e99ad217f07` | GNU Make 4.3 | 0 |
| docs-workflow 35: C and C++ idiom gate | `1e99ad217f07` | GNU Make 4.3 | 0 |
| docs-workflow 36: Python idiom gate | `1e99ad217f07` | GNU Make 4.3 | 0 |
| docs-workflow 37: Shell idiom gate | `1e99ad217f07` | GNU Make 4.3 | 0 |
| docs-workflow 38: CI event and SHA contract gate | `1e99ad217f07` | GNU Make 4.3 | 0 |
| docs-workflow 39: Local act runner contract gate | `1e99ad217f07` | GNU Make 4.3 | 0 |
| docs-workflow 40: Doc cited-path gate | `1e99ad217f07` | GNU Make 4.3 | 0 |
| docs-workflow 41: Archive integrity gate | `1e99ad217f07` | GNU Make 4.3 | 0 |
| docs-workflow 42: Per-page contents gate | `1e99ad217f07` | GNU Make 4.3 | 0 |
| docs-workflow 43: AEM store generator self-test | `1e99ad217f07` | GNU Make 4.3 | 0 |
| docs-workflow 44: Sweep/build shape gate | `1e99ad217f07` | GNU Make 4.3 | 0 |
| docs-workflow 45: Deploy shape gate | `1e99ad217f07` | GNU Make 4.3 | 0 |
| docs-workflow 46: Entity shape gate | `1e99ad217f07` | GNU Make 4.3 | 0 |
| docs-workflow 47: Fetch the engine authority the builder derives from | `1e99ad217f07` | GNU Make 4.3 | 0 |
| docs-workflow 48: Advertised-vs-emitted gate (green since 2026-07-28, item 00) | `1e99ad217f07` | GNU Make 4.3 | 0 |
| docs-workflow 49: Strip git metadata, then run the docs gate | `1e99ad217f07` | GNU Make 4.3 | 0 |

## Execution and retained evidence

The worktree and every gate use the physical `/data` path. New simulation campaigns use the pinned Verilator 5.050. Concurrency is limited to two simulator builds, with `make -j8`, `VERILATOR_JOBS=2` and at most four campaign workers. Vendor invocations hold `$VIVADO_LOCK`; no heavy campaign runs alongside them. `/data` free space is monitored against the 30 GB floor.

The unit has a 12 GiB hard limit and a runtime 7 GiB MemoryHigh limit. The first excluded synthesis attempt reached 9.65 GiB before termination; this operating-limit excursion is not hidden. No OOM event occurred. A second attempt completed synthesis but was terminated during implementation under memory pressure. A first checkpoint restart lost its launch session without a receipt. A subsequent checkpoint route completed, but its synthesis process had been interrupted, so that route is provisional only. The accepted evidence is the later clean two-process synthesis and implementation, each rc 0. Their logs and checkpoint hashes are recorded separately. Removed large provisional checkpoints and temporary directories have recorded sizes and digests in the external cleanup receipt.

Large build products, exports and environments stay outside this packet under `$VALIDATION_STORAGE/682-a554`. Each packet file is limited to 200,000 bytes. `runtime-links.json` records the temporary ROM and builder output links required by the retained measurement inputs; these links were removed for the clean handoff and their removal is recorded in `worktree-cleanup.json`. Recreate only those recorded links to recheck the retained resource reports. The earlier `generated-record-hashes.json` predates explanatory prose; use `current-records.json` for the committed records.

The full-acceptance supervisor returns 1: its original documentation child failed before the corrected 49-step retry, and the parent bank was later cancelled after the render blocker was confirmed. No aggregate green result is claimed.

The first documentation job refused reference generation because Git emitted diagnostics for an unmounted object alternate and an inaccessible image configuration directory. Read-only mounts of the public object databases and a normal per-user configuration path corrected the environment; the literal workflow commands are unchanged. The failed attempt is retained separately. A launch-only rc 126 (non-executable wrapper) was corrected by invoking the script with Bash before any campaign ran.


### Shared generated-header dependency and confirmed blocker

The builder rollback controls temporarily rewrite `hdl/common/csr/gen/lwsrp_csr_defaults.svh`. The documentation workflow builder and host builder overlapped source consumers, so the original `milan_csr` and `milan_datapath` synthesis results and render result are not used alone as evidence of immutable committed input. The parent sweep and bank coordinators were briefly paused, the builder completed, and the header was verified byte-identical to HEAD before resumption. `parent-pause.json` records the pause, resumption and header digest. Fresh synthesis of both affected tops and fresh three-top elaboration return zero. Resource measurements preceded the overlap and are unaffected.

`render-recheck.py` imports the repository campaign and rebuilds the four failed cases through its existing recipes. It verifies the committed CSR bytes before each build and after each run. `render-recheck.json` binds the run logs, build logs, test variants and executables by digest and size:

| Fresh case | Checks | Failed assertions | Run rc | Campaign meaning |
|---|---:|---:|---:|---|
| Unmodified epoch mode | 127 | 4 | 1 | Clean control fails |
| Acknowledgement-level arrival skew | 127 | 4 | 1 | Clean control fails |
| Serial-reset-level arrival skew | 127 | 4 | 1 | Clean control fails |
| Uncounted-repeat mutant | 58 | 0 | 0 | Mutant survives |

All three clean cases fail the same four T30 CRF recentre assertions: settled-grid trigger once, recentre pulse once, stage executes once, and no second recentre after the settled event; each observes zero where one is expected. The surviving mutant fails no assertion. The full repository inventory remains 28/32, rc 2. This matches the cases in open [#657](https://github.com/kebag-logic/milan-fpga/issues/657), although the current clean leg has 127 checks rather than the older issue’s 114. No base checkout was made and no causal attribution to this pin is claimed.

Issue #682 requires every gate to pass and contains no exception for #657. The previous adoption’s exception does not clear this one. No render source, expected result, inventory or acceptance criterion was changed. The broad sweep was cancelled through its repository-owned process supervisor, which returned 143 and explicitly reported no completed sweep result. All campaign processes have ended. `diagnostic-cleanup.json` records removal of 804,200,156 bytes of diagnostic build intermediates; all four executables and their evidence logs remain outside the packet.

## Remaining work and boundaries

Full acceptance is blocked by #657. A published scope decision or the existing issue’s repair is needed before this adoption can meet its all-green criterion. Bitstream/manifest completion, the remaining 50 default suites, parent tally, physical-gPTP simulation, NVM lint/quick and the four LiteX simulations remain uncompleted. The final dev comparison is recorded; integration is prohibited in this session. Stop on an additional processor-parent interface change, non-reproducible generated record or failed best-directive timing. Independent review, hosted checks, publication, merge validation and post-merge hardware work remain outstanding. No push, PR mutation, merge, rebase, firmware edit, processor source edit or hardware access is authorized here.

## Commits

1e99ad217 Rebaseline adopted processor resources and timing
d02c2a3ea Record optional synthesis worker cap in baseline recipes
2a97d4e88 Tighten adoption documentation wording
fcaabb227 Refresh processor pin records and parent integration notes
166c2185e Adapt parent frame capture and declaration budget to processor pin
7bbb53d79 Adopt protocol processor main 2ad2f845 for issue 682
