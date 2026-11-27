Status: F2–F5 have local corrections and evidence; F1 remains open because two inherited failures require changes to protected network files. This is executor evidence, with no review verdict or clean-lens ledger.
Candidate: `573fe2bf1c7463f3320682e6ceffa692c56f2ee1`.

The [internal review](https://github.com/kebag-logic/milan-fpga/pull/1024#issuecomment-7211465999), [external review](https://github.com/kebag-logic/milan-fpga/pull/1024#issuecomment-7211310116) and [manager disposition](https://github.com/kebag-logic/milan-fpga/pull/1024#issuecomment-7211331886) were read in full. The branch first merged `71bad8c0b973a15ee5f993a74f893ff7ff947c33` through merge commit `e6d56c1e90906d945e47e509e6ad13e7a25f81e7`.

| Finding | Local outcome | Evidence |
| --- | --- | --- |
| F1, MAJOR | The original port classification, clock table and stale inventory failures are fixed. Full workflow commands found additional suite registration, parameter-contract, naming, source-header parsing and test-evidence failures; these are fixed without raising acceptance budgets. Two failures remain in protected network files. | `repository-gates.json`; unapplied `proposed-network-fixes.patch` |
| F2, MAJOR | A bridge-level test exercises independent capture and playback epoch changes, applied-state and published-status boundaries, a partial capture interval under backpressure, discarded old-epoch trailing beats, and channel-zero restart. | `epochs_tb.sv`; five named bridge defects in `defect-controls.json` |
| F3, MINOR | Preserve every grid frame. A playback change waits for the current pair walk to finish; a coincident grid emits a complete zero frame and applies the change at the following idle boundary. No partially emitted frame is cancelled. | `KL_usbaudio_media.sv`; every grid/pair-walk offset in `media_tb.sv`; both grid/walk defects caught |
| F4, MINOR | The million-frame run uses fixed 1:2 bus/media clocks with an incommensurate oscillator. It no longer claims two independently phased bus/media clocks. The epoch integration test separately uses 20 ns and 26 ns clocks. | `duplex.cpp`; `USB_AUDIO_PATH.md`; `epochs_tb.sv` |
| F5, residue | The authoritative citation now names the merged interface at `9e5ef16`. The later contract change adds device-side recovery wording and no new FPGA duty beyond the implemented three-ms watchdog. | [Merged interface](https://github.com/kebag-logic/usb-audio/blob/9e5ef16cfbbcc26722bfef56081b992a5e8fc89f/docs/AUDIO-FPGA.md); audio configuration and design documentation |

The five new bridge plants are `bridge_applied_epoch`, `bridge_capture_abort`, `bridge_packet_fence`, `bridge_status_epoch`, and `bridge_published_epoch`. Each reaches its named runtime assertion. The two frame-preservation plants, `media_grid_transition` and `media_walk_transition`, both reach `MEDIA_EVERY_GRID_SNAPSHOT`.

The 2.9 ms watchdog acceptance is measured on the FPGA clock while the submitted USB timestamp advances one bus interval. Exactly 3 ms expires and is refused. This distinction also resolves the clock-description ambiguity noted beside the watchdog test.

The three optional suggestions concerning accepted-word validity, the reference delivery guard and helper options remain suggestions. No change or closure is claimed for them. The prior cleanup exception was disposed by the manager; it is historical, not a new round-4 blocker. Current physical reports accompany the route manifest with only identifying metadata removed.

Remaining F1 failures are `gate_31`, the receive-copy parameter `MAX_LEN_P` lacking the documented octet unit in its name, and `gate_45`, the missing contents list in `USB_NET_PATH.md`. The prepared patch changes those two artifacts only. Neither is applied without an exception to the instruction to preserve the network files.
