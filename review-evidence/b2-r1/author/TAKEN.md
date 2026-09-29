[A440] TAKEN
Branch: `b2-bench-0929`, base `13eda870d1a6cf3f946fc228a98862366b08d102`.
Authoritative references: the [bench lane B2 assignment](https://github.com/kebag-logic/milan-fpga/issues/606#issuecomment-5885087413); #606, #608 and #75 with their [A10] decisions; PR #604 (the #75 reconnect method and findings page); PR #613 (processor `c951a9ff`); PR #620 (this image's identity gate); `docs/testing/TESTING.md` section 6b; the processor's talker DA gate (`T-SRP-DAFRESH`) and its Δ13 / LV + rLv registrar rules.
Interpreted scope:
1. Identity gate as lane B1 ran it; STOP on mismatch.
2. #606: five first binds of DUT Stream Output 1 (CRF) to the reference peer's CRF input 8. Each starts with no DUT Talker Advertise on the tap, reached by an unbind, the 15 s probe-freshness window and the MRP LeaveTime, never a DUT reset. Measured: `CONNECT_RX` response to first valid AVTP PDU against 1 s, the first DUT Talker Advertise and the bridge's first MRPDU. STOP and report the method if no fresh bind is reachable without a reset.
3. #608 and #75: 100 cycles of `DISCONNECT_RX`, 2 s, `CONNECT_RX` on the same pair, with the tap. Per cycle: the stop after the bridge's Listener withdrawal (one PDU period when it reaches an IN registrar), STREAM_START/STREAM_STOP deltas, any non-stop hold, and the restart and its growth.
4. Full restore, proved. Findings pages for #606 and for #608/#75 only; no other doc edits.
Validation plan: the nine assigned gates rc 0 at the committed head; raw capture sizes and SHA-256; offline replay of every bind and cycle.
Blockers: none known. The tap's capture prerequisite is checked under the bench lock.
