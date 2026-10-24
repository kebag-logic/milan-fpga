# #773 item 1: AAF capture-to-wire latency per shape (derived)

Ps = 1e9/48000 = 20,833.3 ns. Term A, the PDU's later frames: (SAMPLES_PER_FRAME_C - 1) x Ps = 5 x Ps = 104,166.7 ns.

## 1x1 (TDM8 master, 50 MHz)

- B, marker latency (DOM_MARK_LAT_NS_C): closing pair 3 of 4, 256 bit periods at 12,288,000 Hz = 20,833 ns, + 1 write cycle at 24,576,000 Hz = 41 ns, + 4.5 read cycles = 90 ns: **20,964 ns**
- C, capture age (close -> the walk's snapshot tick): aligner lock band [256, 785] cycles (keep-off 256 of a 1041-cycle tick) = 5,120.0..15,700.0 ns at a settled lock; 0..1042 cycles before one
- D, walk: tick -> talker t's last pair = 4 + LB_PAIRS_C (4) + slot x (GAP_CYC_P + 2 = 26) cycles
- E, packetizer: last pair -> first SEND beat = 4 (+3 CRD for t > 0) + np (24) cycles; 30 beats to tlast
- F, arbiters (crf_dp_mux, adp_tx_mux): combinational, 0 cycles when no other frame is in flight and the MAC is ready

| talker | last slot | A + B ns | D walk cyc | E first/last beat cyc | hand-over (last beat) - M, age min .. max ns | first beat - M, age min ns |
|---:|---:|---:|---:|---:|---:|---:|
| 0 | 3 | 125,130.7 | 86 | 28 / 57 | 133,110.7 .. 143,690.7 | 132,530.7 |

Shape range at a settled lock, no interference: **133,110.7 .. 143,690.7 ns**; before a lock (age up to 1042 cycles), last talker: 148,830.7 ns. Over 125,000 ns by 8,110.7 .. 18,690.7 ns.

Whole media periods covering the settled-lock maximum: ceil(143,690.7 / Ps) = 7 periods = 145,833.3 ns.

CRF output: hand-over - its stamped event = marker latency + 3 (first beat) .. 10 (last beat) cycles = 21,024.0 .. 21,164.0 ns, plus any AAF PDU in flight at crf_dp_mux (up to 30 beats = 600.0 ns) and any control frame at adp_tx_mux.

## 8x8 (TDM32 master on 98.304 MHz, 50 MHz)

- B, marker latency (DOM_MARK_LAT_NS_C): closing pair 3 of 4, 256 bit periods at 49,152,000 Hz = 5,208 ns, + 1 write cycle at 98,304,000 Hz = 10 ns, + 4.5 read cycles = 90 ns: **5,308 ns**
- C, capture age (close -> the walk's snapshot tick): aligner lock band [256, 785] cycles (keep-off 256 of a 1041-cycle tick) = 5,120.0..15,700.0 ns at a settled lock; 0..1042 cycles before one
- D, walk: tick -> talker t's last pair = 4 + LB_PAIRS_C (1) + slot x (GAP_CYC_P + 2 = 26) cycles
- E, packetizer: last pair -> first SEND beat = 4 (+3 CRD for t > 0) + np (24) cycles; 30 beats to tlast
- F, arbiters (crf_dp_mux, adp_tx_mux): combinational, 0 cycles when no other frame is in flight and the MAC is ready

| talker | last slot | A + B ns | D walk cyc | E first/last beat cyc | hand-over (last beat) - M, age min .. max ns | first beat - M, age min ns |
|---:|---:|---:|---:|---:|---:|---:|
| 0 | 3 | 109,474.7 | 83 | 28 / 57 | 117,394.7 .. 127,974.7 | 116,814.7 |
| 1 | 7 | 109,474.7 | 187 | 31 / 60 | 119,534.7 .. 130,114.7 | 118,954.7 |
| 2 | 11 | 109,474.7 | 291 | 31 / 60 | 121,614.7 .. 132,194.7 | 121,034.7 |
| 3 | 15 | 109,474.7 | 395 | 31 / 60 | 123,694.7 .. 134,274.7 | 123,114.7 |
| 4 | 19 | 109,474.7 | 499 | 31 / 60 | 125,774.7 .. 136,354.7 | 125,194.7 |
| 5 | 23 | 109,474.7 | 603 | 31 / 60 | 127,854.7 .. 138,434.7 | 127,274.7 |
| 6 | 27 | 109,474.7 | 707 | 31 / 60 | 129,934.7 .. 140,514.7 | 129,354.7 |
| 7 | 31 | 109,474.7 | 811 | 31 / 60 | 132,014.7 .. 142,594.7 | 131,434.7 |

Shape range at a settled lock, no interference: **117,394.7 .. 142,594.7 ns**; before a lock (age up to 1042 cycles), last talker: 147,734.7 ns. Over 125,000 ns by -7,605.3 .. 17,594.7 ns.

Whole media periods covering the settled-lock maximum: ceil(142,594.7 / Ps) = 7 periods = 145,833.3 ns.

CRF output: hand-over - its stamped event = marker latency + 3 (first beat) .. 10 (last beat) cycles = 5,368.0 .. 5,508.0 ns, plus any AAF PDU in flight at crf_dp_mux (up to 30 beats = 600.0 ns) and any control frame at adp_tx_mux.

## CRF Equation (14) at the two offsets

- TTmax = 125,000 ns: ceil(TTmax / Ps) = 6 periods, applied 125,000 ns: round-up 0 ns
- TTmax = 2,000,000 ns: ceil(TTmax / Ps) = 96 periods, applied 2,000,000 ns: round-up 0 ns
