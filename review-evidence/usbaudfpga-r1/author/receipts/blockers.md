# Integration blockers

Relates to [#1021](https://github.com/kebag-logic/milan-fpga/issues/1021).
The firmware interface is [usb-audio #9](https://github.com/kebag-logic/usb-audio/pull/9).
The shared network path is [#1020](https://github.com/kebag-logic/milan-fpga/pull/1020).

1. **USB interval qualification remains undefined.** AUDIO-FPGA.md requires an independently validated interval reference. The pinned firmware sends state records on transitions. Playback records follow application queue service. The capture-only probe observes no socket 3 record over 8192 service turns. FLAGA is a readiness level across buffered DMA, rather than an explicit interval counter. A queue-service qualification rule must account for buffering, stalls, capture-only operation and inactive alternates. Neither a PCLK divider nor a testbench-generated pulse proves that rule. The component estimator exposes the required input without inventing a source.
2. **The shared-bus address assignment is incomplete.** NETWORK.md assigns sockets 5 and 6, requiring A2. WIRING.md assigns A1 and A0 only. NETWORK.md explicitly leaves the extra assignment and its physical validation outstanding. The existing network tap remains terminated at its bus boundary. No pin or bus ownership has been silently changed.

The next decision must provide a qualified interval source and the shared address assignment. This is not a request to access hardware. Any physical validation remains separate bench work.

The existing 24-bit render storage is an additional implementation task, rather than an external decision. It must gain an optional 32-bit path before the integrated bridge can preserve every subslot bit. This work has not been done.
