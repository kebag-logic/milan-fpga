[A10] Acceptance obligation added from kebag-logic/milan-fpga #501 (PR #557, decision issue 501 comment 5823589125).

At the 8x8 shape, the output channel-map record grows to the stream-channel key space: 72 entries, so the record area is 12,634 bytes. Under the saved-state page's pessimistic copy model (`SAVED_STATE_SNAPSHOT_OWNERSHIP.md` section 18), a full capture copy then takes up to about 64 ms, against the parent backend's 50 ms grant hold (`KL_nvm_backend.sv` `T_HOLD_MS_P`), a margin of 0.78x. Safety holds, because a lapsed hold voids the capture and it is retried. Liveness under sustained controller activity is not established.

When this issue's writer materializes the audio maps:
1. Measure the actual capture-copy time at 8x8 on the product firmware.
2. Size the hold from that measurement, shape-derived if needed, with a stated margin, or show the existing 50 ms is enough.
3. Record the figure in UNRESOLVED 6 of that page.

The shipping 1x1 shape is unaffected.

