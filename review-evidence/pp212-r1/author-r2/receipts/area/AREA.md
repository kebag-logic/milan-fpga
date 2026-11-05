# Area, the processor's yosys flow (area.sh: sv2v, yosys 0.66 synth_xilinx -family xc7 -flatten)

## Base a9e84b66, round-1 head 04856e48, round-2 head a2fce43

| shape | LUT base / r1 / head | INV | FF | RAM | CARRY4 | head - base (LUT, FF) | head - r1 (LUT, FF) |
|---|---|---|---|---|---|---|---|
| listener_n2 | 4532 / 5471 / 5892 | 443 / 651 / 645 | 933 / 1493 / 1456 | 0 / 0 / 0 | 79 / 113 / 122 | +1360, +523 | +421, -37 |
| listener_n8 | 9839 / 15026 / 16029 | 1509 / 2363 / 2384 | 2963 / 5103 / 4952 | 32 / 32 / 32 | 103 / 185 / 176 | +6190, +1989 | +1003, -151 |
| srp_top_2x2 | 11475 / 12690 / 13193 | 2811 / 2944 / 2875 | 4812 / 5372 / 5334 | 114 / 114 / 114 | 457 / 491 / 500 | +1718, +522 | +503, -38 |
| srp_top_8x8 | 23046 / 27399 / 28193 | 3483 / 4411 / 4037 | 9236 / 11376 / 11224 | 179 / 179 / 179 | 506 / 588 / 579 | +5147, +1988 | +794, -152 |

Base and round-1 figures reproduce round 1's receipts exactly. The head's four stat files are
byte-identical to those of `r2dl13` below (the head tree differs from it in two comments only).

## The 13-bit deadline decision (R769-1 S2 / R770-1 S1): round-2 changes without (`r2`) and with it (`r2dl13`)

| shape | r2 LUT, FF | r2dl13 LUT, FF | change |
|---|---|---|---|
| listener_n2 | 6205, 1494 | 5892, 1456 | -313 LUT, -38 FF |
| listener_n8 | 15898, 5104 | 16029, 4952 | +131 LUT, -152 FF |
| srp_top_2x2 | 13260, 5372 | 13193, 5334 | -67 LUT, -38 FF |
| srp_top_8x8 | 28276, 11376 | 28193, 11224 | -83 LUT, -152 FF |

`KL_srp_top` is smaller at both shapes in LUT and FF, so it was taken. The listener alone at 8 sinks
measures +131 LUT, within this flow's LUT noise (below); its FF figure is -152.

## Attribution and noise: `r2` with one arm patch planted (KL_srp_top 2x2; listener 2 where run)

| variant | planted arm(s) | srp_top_2x2 LUT, FF | listener_n2 LUT, FF |
|---|---|---|---|
| r2 | (none) | 13260, 5372 | 6205, 1494 |
| vA | unarmed-publishes-latency | 12994, 5372 | 6030, 1494 |
| vB | rebind-same-not-kept | 12807, 5372 | 5754, 1494 |
| vC | pt-link-flush-dropped + unarmed-link-flush-dropped | 13188, 5372 | 5995, 1494 |
| vD | unarmed-indicates + unarmed-fail-chg + unarmed-unregistered | 13176, 5372 | 6154, 1494 |
| vE | unarmed-registrar-deaf | 13209, 5372 | 6349, 1494 |
| vF | keep-ignores-vlan | 13110, 5372 | not run |
| vG | keep-ignores-da | 12936, 5372 | not run |
| vH | keep-latency-strobe-dropped | 13316, 5372 | not run |
| vI | keep-declares-seed-type | 12965, 5372 | not run |

The flip-flop figure is exact. The LUT figure is not: `keep-ignores-vlan` removes a 12-bit compare per sink
(about 8 LUT) and moved it by -150; `keep-latency-strobe-dropped` removes a 32-bit zero test per sink
(about 11 LUT) and moved it by +56. So differences of up to about 300 LUT at this shape are not
measurements of the edit; the shipping image's fit is the Vivado route's to decide.
