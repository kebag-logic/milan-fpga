The USB network path copies permitted frames and injects rate-limited best-effort traffic while preserving endpoint priority. Arty status LEDs follow the [fabric-level ruling](https://github.com/kebag-logic/milan-fpga/pull/1020#issuecomment-7213370880): LD2 means any media-locked input or open output transmit gate; LD3 means internal selection or a locked selected source. The control image contains no LED register or LED handling.

The [held-egress ruling](https://github.com/kebag-logic/milan-fpga/pull/1020#issuecomment-7234489667) gives USB-network Arty its own ledger point under #894's rule. Each row uses the larger original Arty or injected measurement. The table is in `docs/design/USB_NET_PATH.md`; only its last AECP figure differs, at 62.14 ms. The original Arty and 8x8/1if ledgers remain unchanged. These remain seven recorded service-budget misses, bounded by their separate ledger.

All 159 retained traces across eight images regrade identically. Qualification passes at the USB point with no new or larger miss. The unchanged owner row gives load 0.501397, ACMP 29.84 ms, txL 48.90 ms and last notice 117.58 ms. The retained complete wire result is 644.981 us against 1000 us. Controls preserve the 62.03635-versus-61.99 rejection at the original Arty point and reject one cycle over 62.14 at the USB point. All 25 ledger mutations are detected; final documentation and inventory gates pass. Inventory regeneration is a separate commit.

Firmware, RTL, the queue model and scheduling costs are unchanged. The Arty and both ALINX control ELF/map-header comparisons remain byte-identical to #1004's same-pin builds. The other thirteen dependency files are unchanged. Previous simulation, filter and LED plants, injection controls and shaping evidence retain their exact inputs.

Board observations, attachment integration, physical-route qualification, broader candidate gates and independent review remain open. Existing whole-image crossing and external-I/O limitations remain. No physical release or issue completion is claimed.

Relates to #1011
Relates to #1018
