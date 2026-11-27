Status: STOP. Implementation and validation are complete; two repository gates require unauthorized edits to protected network files.
ETA: blocked until the manager disposes the two-file ownership exception; the exact unapplied patch is included.

Candidate: `573fe2bf1c7463f3320682e6ceffa692c56f2ee1` on `usbaudfpga`. Live development at `71bad8c0b973a15ee5f993a74f893ff7ff947c33` was merged first. No push, public post or hardware action was performed.

All 44 workflow gate commands completed: 42 pass and 2 fail. The builder union accounts for all 114 gates; its optional historical calibration arm is explicitly not run. F2–F5 have corrections and reproducible local evidence. F1's three original failures are corrected, but the complete workflow exposes two inherited failures in files that must remain unchanged: the receive-copy length parameter lacks an octet unit in its name, and the network design lacks a contents list. [The exact proposed patch](receipts/r4/proposed-network-fixes.patch) remains unapplied pending an ownership exception.

Playback changes now preserve a complete frame at every grid and pair-walk offset. New bridge tests catch omitted applied-epoch gating, omitted capture abort, omitted packet fencing, premature acknowledgement and omitted published acknowledgement. The merged interface is cited at `9e5ef16`.

The full-window run passed 1,000,000 playback frames and 999,993 capture frames across all eight channels and all 32 bits: 37,419,648 checks, zero failures, no unexpected gaps or duplicates. All 77 named protocol/transport defects were caught, including five epoch-wiring defects and both frame-preservation defects. Parameter checks accept 21 legal configurations and refuse 22 invalid configurations.

The current audio RTL was freshly synthesized and routed. All four Arty corner reports pass. Minimum setup is **+0.006 ns**, compared with +0.002 ns previously; minimum hold is +0.016 ns and pulse-width slack +1.389 ns. All 55 audio pad registers pass placement checks. Routed cost over the matched disabled profile is +2,531 LUTs, +5,846 registers, +8 block-RAM tiles and +544 slices; no additional DSPs. Total slice occupancy is 95.04%. The narrow setup margin applies to the recorded artifact.

Both complete retained ALINX programming payload pairs were re-read and remain byte-identical. Their direct gateware inputs are unchanged. Physical comparisons use fixed retained initialized memories and generated wrappers: this does not claim freshly linked production software after the common firmware merge, a new ALINX route, or bench qualification.

All protected network implementation, construction and test files remain byte-identical. The shared generated documentation audit was refreshed as required by F1. Build tests retain mutual exclusion of audio and network selection.

The earlier cleanup exception is disposed by the [manager decision](https://github.com/kebag-logic/milan-fpga/pull/1024#issuecomment-7211331886). Round-4 temporary files use the lane scratch; removals are recorded before execution. Resource and gate details are in the [receipt index](receipts/INDEX.md).

The [review response](receipts/r4/review-response.md) distinguishes completed fixes from remaining failures. Independent re-review, protected checks, merge validation and bench acceptance remain outstanding. Relates to #1021 until the bench.
