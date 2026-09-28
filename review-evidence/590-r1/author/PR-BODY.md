[A385]

Closes #590
Closes #592
Relates to #599

Queued Milan commands and long validation walks now provide heartbeat opportunities, retaining the 250 ms rate limit. Wipe yields between slot erases. Capture copies use aligned words inside closed records and bytes at their edges. Firmware reads PHY state over MDIO and publishes link, speed and duplex through the existing status CSR; a brief latched loss and its recovery are resolved in the same poll.

All six capture arms pass 16 captures each at processor pin `16be6768`. The worst 8x8 interval is 13.23262 ms at 50 MHz against 24.5 ms; the labelled 100 MHz comparison is 9.94948 ms. The 50 MHz result gains 11.06984 ms of margin over the previous 24.30246 ms receipt. The receipt binds the measured firmware and processor. Both shapes pass all five service plans with continuous backing and a largest observed heartbeat gap of 322.47112 ms. The derived publication period is at most 250 ms, using a 125 ms eligibility interval plus measured service reserve.

The byte-only control restores the old copy cost. Missing-copy, missing-traffic, missing-publication, delayed-recovery and dispatch-removal controls are detected. Simulation checks actual MAC_STATUS and fabric link counters; both queued plans and the device-wait plan show one down/up cycle per shape.

Required local gates return zero at `792a57b092efaee8920f344faacb7675c8e163bd`: both compiler modes of the full builder bank, all-shape host tests including Arty, firmware census, capture receipt, service checks, CI scope, source and documentation checks, and whitespace. The builder's existing physical-utilization calibration remains explicitly unrun because its report is absent; the absent-compiler mode also records its intentional instrument omission. The only builder edit is the authorized fixture count change from 2 to 4.

The physical switch-cycle rerun remains #599 acceptance 4 after merge. Independent review is pending.
