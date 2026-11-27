Status: desk work complete and internally reviewed; ready for external review. Bench acceptance remains open.
ETA: desk handoff ready now; bench timing is not estimated.

Candidate: `ba2a66f72db495bd7c48700d46688de08a6c2c61` on `usbaudfpga`. Local commits only. Nothing pushed or posted. No hardware action performed.

Both eight-channel directions preserve all 32 subslot bits through whole-frame crossings. Shared queue storage remains 24-bit by default. The bridge implements synchronized reset release, capture packetization and epoch fencing, the 20-byte status record, periodic status scheduling, and qualified interval-record feedback from the disciplined media oscillator without sample-rate conversion. The contract is USB audio #9 at `ae4b11bdaf3e84faa46a9ce32b641f65716b0ed2`.

The optional Arty audio and network selections work separately and reject a combined image. Audio uses sockets 0 and 3, plus status socket 1, on A1:A0. All 22 network-attachment files match #1020's pinned revision. Concurrent network traffic still requires A2 wiring.

The current million-frame run passes: 1000000 playback frames, 999993 capture frames after startup, 37419648 checks, zero failures and no gaps or duplicates after comparison begins. All 24 protocol and 42 transport defect controls reach their named failures. Default-width loopback integration passes 155604 checks. Source, style, documentation and punctuation checks pass within their recorded scopes.

The selected Arty route passes all four requested corner reports. Minimum setup slack is +0.005 ns; minimum hold is +0.040 ns; minimum pulse-width slack is +1.389 ns. All 55 pad endpoints, all 13 crossing-skew constraints, registered source launches and finite flag-pair setup/hold pass independent review. All 83196 routable nets are routed with zero errors. Design-rule warning categories and counts match the baseline. The narrow setup margin applies to this exact routed artifact.

Final routed cost over the matched audio-disabled split profile: +2636 LUTs, +5849 registers, +466 slices, +8 block-RAM tiles, +11 pads, +3 global clock buffers and +1 clock manager. DSP and PLL counts are unchanged. The image occupies 14986 of 15850 slices (94.55%). The control clock remains 100 MHz; media and external bus clocks remain 50 MHz. Firmware is linked against each selection's own stable register and flash maps.

Arty programming data: 3326900 bytes, SHA-256 `81e86ad9d94be07b9b3f7c8cbcbecbbc13c4348304508772660137b1eeac1a55`. The complete data extracted from the container equals the flash output byte for byte.

Both ALINX shipping profiles have byte-identical complete programming data, 3825788 bytes each. Single-stream SHA-256: `379154b150173c369cc6aa45f25063a581362b3086bd800c05f208311aff2031`; eight-stream SHA-256: `e5deca48b039d8c89de687f79ee20def5e24a9210bea8d073eeacb8c1f0142c7`. Only container time metadata differs. Firmware, initialized memories, descriptors and constraints match. All reported corners pass on both sides; later changes are outside the ALINX input closure.

[R1] POSITIVE internal desk review covers Conformance, RTL, Robustness, Tests and Docs at the full candidate head. Earlier pad-placement, source-launch and suppressed-hold findings are fixed and rechecked. Failed route attempts remain in the receipts. Two queued explorations were cancelled before execution after closure; neither supplies evidence.

External review, protected checks and merge validation remain separate. Desk work does not discharge interval-delivery qualification, coordinated arming, electrical verification, capture-DMA fencing, host binding or sustained hardware duplex. The qualification control defaults clear. [#1021](https://github.com/kebag-logic/milan-fpga/issues/1021) remains open until the bench.

Two known round-2 cleanup violations remain explicit: an early generated-library cleanup, and automatic temporary-directory removal during preliminary leaf mapping. The latter hid its directory names, so literal paths are unavailable. Both were recorded retrospectively and are not claimed as compliant. Other known removals were recorded first. Round-1 cleanup limitations remain historical facts.

See [receipts/INDEX.md](receipts/INDEX.md).
