Status: Corrections are committed and all requested desk validation passes. This records executor evidence, without a review verdict or clean-lens ledger.
Candidate: `0f7402ee97d347352b8c3d613033c440ee55986a`.

The [internal review](https://github.com/kebag-logic/milan-fpga/pull/1024#issuecomment-7211465999), [external review](https://github.com/kebag-logic/milan-fpga/pull/1024#issuecomment-7211310116) and [manager disposition](https://github.com/kebag-logic/milan-fpga/pull/1024#issuecomment-7211331886) remain the review inputs. The requested [network head](https://github.com/kebag-logic/milan-fpga/commit/b4a1df4a0913d7a9b03c8ed0678a035ba2eda5d6) was merged while preserving the preceding audio corrections. No ownership exception was taken.

| Finding | Local outcome | Evidence |
| --- | --- | --- |
| F1, MAJOR | The original three gate failures and both inherited network failures are corrected. The network fixes came from their owning branch. Merge-related scheduling, generated-reference, scope-wording and module-size failures were corrected without relaxing any gate. All 44 workflow steps and the 115-check builder union pass. | Repository gate receipt, builder union and network identity receipt |
| F2, MAJOR | Bridge tests cover independent playback and capture epoch changes, media application, partial capture abandonment under backpressure, old-epoch trailing beats, channel-zero restart, and acknowledgement publication before new capture traffic. All five named wiring defects are caught again. | `epochs_tb.sv`; `defect-controls.json` |
| F3, MINOR | Preserve the complete grid frame. A coincident playback transition emits a complete zero frame; a transition during the pair walk applies after the frame finishes. No partially emitted frame is cancelled. Both named frame-preservation defects are caught again. | `KL_usbaudio_media.sv`; `media_tb.sv`; `defect-controls.json` |
| F4, MINOR | The long-run description states a fixed 1:2 bus/media relationship with an incommensurate oscillator. The separate epoch test uses 20 ns and 26 ns clocks. | `duplex.cpp`; `USB_AUDIO_PATH.md`; `epochs_tb.sv` |
| F5, residue | The authoritative citation names the merged interface at `9e5ef16`. Its device-side recovery clarification adds no FPGA duty beyond the implemented three-millisecond watchdog. | [Merged interface](https://github.com/kebag-logic/usb-audio/blob/9e5ef16cfbbcc26722bfef56081b992a5e8fc89f/docs/AUDIO-FPGA.md) |

The five bridge plants are `bridge_applied_epoch`, `bridge_capture_abort`, `bridge_packet_fence`, `bridge_status_epoch`, and `bridge_published_epoch`. Each fails its named runtime assertion. The two frame-preservation plants, `media_grid_transition` and `media_walk_transition`, fail `MEDIA_EVERY_GRID_SNAPSHOT`.

The watchdog controls accept 2.9 ms measured on the FPGA clock while the USB timestamp advances one bus interval, and refuse exactly 3 ms. They remain part of the complete 77-defect campaign.

The three optional suggestions concerning accepted-word validity, the reference delivery guard and helper options remain suggestions. The historical cleanup exception remains disposed by the manager. Current physical reports accompany their manifest with identifying metadata removed and original hashes retained. Independent reviewers must re-review the corrected candidate.
