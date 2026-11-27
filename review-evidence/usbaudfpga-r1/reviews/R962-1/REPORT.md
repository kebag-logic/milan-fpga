[R962] NEGATIVE - exact head 75db86a926a9f4d2f7734246eac06a8f58c57bac

Round R962-1, external independent review of issue #1021 / PR #1024. All five lenses were applied. Two MAJOR findings remain open: one public-evidence deficiency and one retained execution-compliance finding. No functional RTL defect was established. This is a completed review, not merge approval or completion of issue #1021.

Tree: `2e369a1b046f89e354d02fa7b465b5bcb787293b`. Reviewed range: `4df125b8c11f0e1706b3c1e489f3e66a5d856b18..75db86a926a9f4d2f7734246eac06a8f58c57bac`, including its 24 commits and the network merge. The imported network contribution is exactly 22 files from `cc49123d2db1e01e80859efa10f8da43a01344ef`; all 22 retain identical blobs. The common-base diff includes those imports, so “network unchanged” means unchanged from that imported revision, not absent from the common-base diff.

Reconstruction followed the assigned order: repository operating rules and documentation map; [issue #1021](https://github.com/kebag-logic/milan-fpga/issues/1021), PR scope and public comments; requirements and interfaces; source diff/history; then [published evidence at 63928dd4](https://github.com/kebag-logic/milan-fpga/tree/63928dd4afd403a81949f8e633fd76a701412c91/review-evidence/usbaudfpga-r1/author). The issue API returned no comments; the PR conversation contained the two manager review-start notices, with no review submissions or inline findings. No manager source bank was found or inferred. The independent verdict and ledger were written before reading the earlier review reports inside the public evidence packet. No private author material or other active review report was consulted.

The governing companion interface is [AUDIO-FPGA.md at merged main 9e5ef16](https://github.com/kebag-logic/usb-audio/blob/9e5ef16/docs/AUDIO-FPGA.md). Compared with the PR's cited `47e6bbc9`, its difference explains firmware link-recovery handling; the FPGA record layouts, three-millisecond watchdog, epoch fence and status duties are unchanged. The physical constraints were compared with that repository's pinned `docs/bringup/WIRING.md` and `TIMING.md`. Product authorities include REQUIREMENTS.md, especially REQ-CSR-03, and the media-clock/interface contracts linked by docs/README.md. IEEE 1722-2016 AAF and Milan v1.2 media-clock requirements remain the governing product context; no new physical compliance claim is made here.

[R962] MAJOR Conformance, RTL, Tests, Docs - R962-1-F1 - public evidence `author/receipts/r3-arty-route.json`, `r3-arty-crossings.json`, `r3-arty-cost.json`, `r3-alinx-payloads.json` - Raw physical-acceptance artifacts are not publicly available for this review.

Authority/evidence: issue #1021 acceptance criterion 2 requires all-corner routing, stated cost and identical ALINX images. AGENTS.md requires reconstructible public evidence; CONTRIBUTING.md section 3 requires reproducible timing evidence. The published packet contains measurements, recipes and hashes. Of the 33 reports listed by the route receipt, only the pad-placement report's bytes are present, under `r3-arty-packing.txt` (also the identical earlier packing text). The other 32 raw reports, routed checkpoint and complete image pairs are absent, and the reproduction pages supply no durable download location. See [public artifact inventory](receipts/public-artifact-inventory.json), including digest aliases rather than filename matching alone.

The summaries report minimum setup +0.002 ns, hold +0.018 ns and pulse slack +1.389 ns, with zero failing endpoints, 83,063 routed nets and 13 passing skew groups. Their arithmetic gives +2,592 LUTs, +5,861 registers, +454 slices and +8 block-RAM tiles; I recomputed those differences. The pad report's digest matches the recorded artifact. Those checks do not inspect the actual worst paths, unconstrained endpoints, exceptions, CDC reports or the complete ALINX payloads. The earlier review's statement that it inspected them is not a replacement for an independent artifact inspection. [Crosscheck receipt](receipts/evidence-crosscheck.json).

Impact: criterion 2 cannot be independently cleared from the permitted public state, particularly the narrow setup margin and shipping-image identity. This is an evidence deficiency, not a demonstrated timing failure or proof that the measured margin is false.

Required outcome: publish or durably link the recorded timing, operating-condition, exception/constraint, CDC, skew, route and utilization artifacts, along with the complete programming-image comparison inputs and source/input closure needed to verify them. Include the named checkpoint or an equivalent inspectable implementation bundle. Preserve technical content when removing private location metadata, and bind original/published bytes with hashes.

Verification: match the recorded hashes; inspect setup, hold, pulse, unconstrained paths and exception scope for both speed models at the declared temperature settings; verify finite flag-pair setup/hold and crossing bounds; recompute routed cost against the matched baseline; compare both complete ALINX programming payload pairs. The two temperature settings are not four independent timing libraries. A future current-dev candidate result is separate from validating this recorded source artifact.

[R962] MAJOR Conformance - R962-1-F2 (retained prior R2 finding) - public evidence `author/receipts/r3-cleanup-exception.md:1` and `r3-internal-review.md` - The disclosed execution exception has no public disposition.

Authority/evidence: the earlier public review explicitly classifies the missing advance-removal records and wrong temporary root as MAJOR Conformance. The author disclosure says randomized temporary names were not retained and the audited rerun cannot satisfy the original advance-logging instruction. The PR retains STOP language. No subsequent disposition appears in the inspected public issue/PR state. I retain the finding and its reviewer-assigned lens; I did not inspect private operational records.

Impact: full execution compliance and completion remain unestablished. This does not invalidate the functional measurements or prove source corruption.

Required outcome: retain the disclosure and STOP status until the responsible authority explicitly disposes of the unmet execution requirement. Missing advance records cannot be recreated retrospectively. Rewording the disclosure or repeating a successful check does not resolve this finding.

Verification: inspect the public disposition and its precise completion consequences against the existing exception and prior finding. No claim of complete cleanup compliance may be based solely on the rerun.

The applied source checks and their practical limits are recorded below. Paths refer to the reviewed head.

| Duty / lens application | Examined artifacts and result |
|---|---|
| Playback/state framing and independent epochs | `KL_usbaudio_record.sv:79`, `KL_usbaudio_ingress.sv:51`, `KL_usbaudio_bridge.sv:122`, `KL_usbaudio_media.sv:155`: complete record staging, fixed frame geometry, reserved flags/digest checks, declared-length draining, immutable completion, independent epochs and playback prefill. Invalid, truncated/reset and stalled records are exercised. |
| Interval reference and explicit feedback | `KL_usbaudio_ingress.sv:77`, `KL_usbaudio_clock.sv:15`, `KL_usbaudio_reference.sv:28`, `KL_usbaudio_feedback.sv:29`: first-word Gray timestamp, complete-parse qualification, count/sequence wrap and continuity, raw-field consistency, 256/625 delta conversion, 512 oscillator ticks per frame and K=13 scaling. No FLAGA/PCM/PCLK-derived nominal feedback substitution. Physical qualification defaults off. |
| Watchdog and loss | `KL_usbaudio_reference.sv:45`, `reference_tb.sv:98`: own-clock expiry at three milliseconds, last pre-expiry value retained, coincident replacement refused, invalid reference cannot also seed a replacement window, subsequent full qualification required. Delivery bounds and watchdog are independent tests. All five watchdog plants were caught. |
| Capture framing and status fence | `KL_usbaudio_media.sv:64`, `KL_usbaudio_packet.sv:36`, `KL_usbaudio_bridge.sv:222`, `KL_usbaudio_status.sv:36`: stream-zero ordered frame assembly, no partial publication, prefill, maximum seven-frame intervals, ordinary stall retention, epoch abandonment, media acknowledgement and completed status before new capture output. State-only reads continue while inactive. |
| Status scheduling and bus ownership | `KL_usbaudio_gpif.sv:53`, `KL_usbaudio_bridge.sv:225`, `gpif_tb.sv:50`: ten immutable little-endian status words, sequence wrap, final-word packet end, status opportunities between audio service, blocked-status fairness, phased read sampling, turnaround and asynchronous pad shutdown. Socket readiness remains a necessary deadline assumption. |
| CDC, reset and diagnostics | `KL_usbaudio_crossing.sv:23`, `KL_usbaudio_reset.sv:12`, `KL_usbaudio_bridge.sv:65`, `usbaudio_soc.py:26`, `usbaudio_cdc.tcl:4`: whole-frame/state FIFOs, common session reset with local release, registered level launches, Gray delay/skew bounds, separate atomic bus/media diagnostic snapshots. FIFO saturation, gaps, incomplete frames and source-level hazards have runtime checks. Physical CDC implementation evidence remains F1. |
| All subslot bits and AVB integration | `KL_chan_map_capture.sv:638`, `KL_aaf_packetizer.sv:540`, `KL_render_queue.sv:492`, `milan_datapath.sv:1563`, `milan_datapath.sv:8569`: 32-bit selection only for audio, ordered mapper pairs and delayed snapshot, endian handling through AAF and render storage, explicit stream/channel selection, unchanged 24-bit default. Both widths pass; three independent low-byte-loss plants fail the real storage oracles. |
| Build scope and documentation | `usbaudio_build.py:14`, `usbaudio_soc.py:120`, `configs/endstation_arty_usbaudio.yaml`, generated shape header, `USB_AUDIO_PATH.md:9`: Arty 8x8/48 kHz shape, split placement, exclusive audio/network selection until A2, disabled delegation, separate arm/qualification controls and explicit bench limits. No added process-lane/reviewer labels were identified in reviewed source comments. |

Reviewer-owned execution evidence:

| Execution | Result / receipt |
|---|---|
| Default bounded audio regression | PASS, including twelve packing-grader negative controls, protocol/reference/media/packet/bus/source-level cases, both storage widths, short-window duplex and seven representative defects. [Runtime excerpt](receipts/default-runtime.txt). |
| Protocol campaign | 24/24 named runtime detections; no build failure counted. [Results](receipts/protocol-raw/results.json); individual raw run logs alongside. |
| Transport campaign | 46/46 named runtime detections; five unmutated baselines PASS. [Results](receipts/transport-raw/results.json); individual raw run logs alongside. |
| Render queue, 24-bit and 32-bit | 39 checks, zero failures at each width. [24-bit](receipts/render24-runtime.txt), [32-bit](receipts/render32-runtime.txt). |
| Independent low-byte-loss probes | Mapper fails `CAPTURE_STORAGE_ALL_BITS`; packetizer fails `AAF_STORAGE_ALL_BITS`; render fails 12 of 39 checks including byte-exact placement. All compile successfully. [Probe results](receipts/storage-probes.json), raw `probe-*.log` receipts. |
| Final checkout integrity | PASS: 2,034 superproject blobs checked directly, matching modes and index; all four required submodules match pins, raw blobs, modes and indexes; all 22 network files identical. [Final audit](receipts/checkout-final.json). |

The short duplex rerun checks 1,000 playback and 971 capture frames after startup, 48,192 checks with zero failures. Its K=5 window is explicitly shortened. The author's separate K=13 million-frame receipt states 1,000,000 playback / 999,993 capture frames, 37,419,648 checks, zero failures and one intentional initial reference discontinuity. I inspected that harness and receipt but did not rerun the million-frame workload or claim it was my execution. Neither run is a physical loopback or a complete board-level simulation: bridge transport, bus scheduling and shared AAF storage are exercised by separate harnesses.

The scoped simulation executable reported release 5.050, revision v5.050. Independent campaigns ran concurrently with four build jobs each; the three supplemental probes used two jobs each. Peak requested compilation concurrency was 16. No physical build ran. Every foreground orchestration command completed before finalization. Disposable source copies and builds remain under `scratch/`; the reviewed source was never mutated. Portable reproduction scripts are `run_checks.py`, `probe_storage.py`, `audit_checkout.py` and `package_receipts.py`. Pass evidence excludes the reviewer setup errors disclosed in `receipts/setup-notes.txt`. Combined build-log hashes and runtime extraction provenance are retained in `receipts/runtime-provenance.json`; published campaign runtime logs are byte-for-byte copies.

Prior public finding reconciliation, performed after the independent verdict/ledger:

- The early missing-reference-source objection is addressed by the now-merged socket-3 interval contract and the implemented parser/estimator. It is not a claim that physical delivery variation is qualified.
- A2 remains unwired; mutually exclusive options prevent physical socket aliasing. Concurrent networking is not accepted.
- The former 24-bit-only storage limitation is addressed by the optional full-width paths and independently killed low-byte probes.
- Prior address-pad packing, combinational status launches and suppressed flag-pair hold findings have source corrections present (`selected_socket_r`, registered launch levels, ordinary stage-to-stage hold analysis). Their behavioral checks pass. The actual routed closure is reported by the author and earlier review; independent physical reinspection remains blocked by F1.
- The earlier two-millisecond watchdog and early feedback-loss defects are corrected and their exact named controls pass here.
- The earlier map-normalization and executable-helper wording corrections are present in `r2-reproduction.md`; no repeat wording finding was identified. Their underlying image/route measurements still need the artifacts named in F1.
- The prior R2 MAJOR execution finding is retained as F2. Earlier positive technical ledgers do not clear it or substitute for this review's missing raw artifacts.

Reviewer-owned completion ledger:

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN: F1, F2 | merged AUDIO-FPGA.md; REQUIREMENTS.md; all record/reference/epoch/status duties above; acceptance and exception receipts | R962-1 | 75db86a926a9f4d2f7734246eac06a8f58c57bac |
| RTL | UNCLEAN: F1 | twelve audio RTL modules; three AAF storage modules; datapath wiring; board clocks, resets, constraints and physical receipts | R962-1 | 75db86a926a9f4d2f7734246eac06a8f58c57bac |
| Robustness | CLEAN | protocol/reference/media/packet/gpif/levels harnesses; full defect campaigns; reset, malformed input, stalled sockets, independent epochs and watchdog boundaries | R962-1 | 75db86a926a9f4d2f7734246eac06a8f58c57bac |
| Tests | UNCLEAN: F1 | default suite, 24 protocol / 46 transport defects, width checks, independent storage plants, million-frame harness, public artifact inventory | R962-1 | 75db86a926a9f4d2f7734246eac06a8f58c57bac |
| Docs | UNCLEAN: F1 | issue/PR public scope, USB_AUDIO_PATH.md, merged interface and harness authorities, evidence reproduction/identity/route receipts | R962-1 | 75db86a926a9f4d2f7734246eac06a8f58c57bac |

[R962] PASS Robustness - `tb/verilator/usbaudio/reference_tb.sv:98`, `media_tb.sv:80`, `packet_tb.sv:52`, `gpif_tb.sv:50`, `protocol_tb.sv:118`, `levels_tb.sv:25` - Applied boundary, malformed-input, epoch, backpressure, clock-loss and reset checks against the frozen interface; their baselines and named defect controls pass at the reviewed head.

Real limits and pending manager duties:

The exact-head hosted snapshot contains 96 checks: 12 success, 16 failure, 67 cancelled, one skipped. Among required contexts, `wire-accountability` and `docs-check-no-git` succeed; `rtl-fast` is cancelled; `docs-check`, `elaborate`, `verilator-suites` and `yosys-portability` fail. A skipped context is not executed validation. This snapshot does not diagnose the underlying failures or attribute them to this patch. [Snapshot](receipts/hosted-snapshot.json). Hosted/local workflow acceptance belongs to the manager; none is claimed here.

No full parent, processor, gPTP, synthesis-portability or builder bank was run by this reviewer. Source execution evidence is the author's published receipts plus the focused checks above. There is no manager source-head bank. The final candidate against live dev `e275d7950ef3385753e6a15d2e191ba855b171ed` is distinct from source base `4df125b8c11f0e1706b3c1e489f3e66a5d856b18`; the manager must construct, validate and publish receipts for the actual current-dev candidate at the merge turn. Any changed lens scope requires renewed coverage.

The manager must resolve F1/F2, complete protected checks and required workflow acceptance, obtain clean independent review coverage, validate the merge candidate, obtain explicit maintainer merge authorization, and perform post-merge containment. This review makes no GitHub write and authorizes no merge. Issue #1021 remains open through its bench acceptance: measured interval variation under load, physical bus timing, coordinated reset/arm, capture-DMA fencing, host binding and long bidirectional bit-exact loopback. Physical calibration was NOT RUN; field skips are not hardware proof. Concurrent network operation additionally needs A2 wiring.

R962-1 FINISHED
