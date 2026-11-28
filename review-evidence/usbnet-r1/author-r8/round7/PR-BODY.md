The USB network path copies permitted frames and injects rate-limited best-effort traffic while preserving endpoint priority. Arty status LEDs follow the [fabric-level ruling](https://github.com/kebag-logic/milan-fpga/pull/1020#issuecomment-7213370880): LD2 means any media-locked input or open output transmit gate; LD3 means internal selection or a locked selected source. There is no firmware LED register or LED code in the control image.

This update merges #1004's 100 Mb/s qualification and adds the [required injection envelope](https://github.com/kebag-logic/milan-fpga/pull/1020#issuecomment-7216971645): one longest injected frame before every busy period, with the measured shipping-chain handshake. The live queue delays mailbox tails, so free-space tests and completion readers include the injected traffic.

Qualification is blocked. All 159 cases across eight images completed, retaining the unchanged rule and dispositions. The derived owner row remains a fixed point, and the complete wire bound is 644.981 us against 1000 us. However, last AECP delivery in the held-egress case is 62.03635 ms against its unchanged 61.99 ms ledger. The 46.35 us excess remains a failure. No bound or ledger entry was relaxed.

Control ELF and map-header identity passes for Arty and both ALINX configurations at the same dependency pins. The shipping handshake measures 257.5 ns across 512 cases, stated as 260 ns. USB/LED tests, 72 existing planted defects, both shipping-handshake defects, 18 injection controls and the existing shaper regressions pass. Keeping the dependency's documentation inventory byte-identical also leaves its freshness gate failing on the two USB pages.

Board observations, attachment integration, broader candidate gates and independent review remain open. Existing whole-image crossing and external-I/O limitations remain. No physical release or issue completion is claimed.

Relates to #1011
Relates to #1018
