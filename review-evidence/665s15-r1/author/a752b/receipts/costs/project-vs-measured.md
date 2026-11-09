| Cost | S2b 1x1/1if, us | S2b 8x8/2if, us | S2b projected 32x32/2if, us | this base 1x1/1if, us | this base 8x8/2if, us | projected from this base, us | measured 32x32/2if, us (most cycles, instances) | error of S2b's, us | error of this base's, us |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `record.srp` | 250 | 395 | 892.1 | 430 | 585 | 1116.4 | 1085 (103,103, 70) | -192.9 | +31.4 |
| `record.aecp` | 200 | 255 | 443.6 | 1150 | 1650 | 3364.3 | 2245 (213,588, 148) | -1801.4 | +1119.3 |
| `record.acmp` | 280 | 430 | 944.3 | 605 | 980 | 2265.7 | 2505 (238,297, 88) | -1560.7 | -239.3 |
| `record.adp` | 105 | 230 | 658.6 | 220 | 595 | 1880.7 | 1955 (186,065, 54) | -1296.4 | -74.3 |
| `record.maap` | 90 | 125 | 245.0 | 160 | 270 | 647.1 | 615 (58,188, 30) | -370.0 | +32.1 |
| `event.ADP` | 100 | 110 | 144.3 | | | | not measured: S2b's eventcost.py figure, from its own head's event records; not run here | | |
| `event.ACMP` | 170 | 340 | 922.9 | | | | not measured: as event.ADP | | |
| `event.MAAP` | 160 | 215 | 403.6 | | | | not measured: as event.ADP | | |
| `event.AECP` | 60 | 95 | 215.0 | | | | not measured: as event.ADP | | |
| `event.TICK` | 35 | 40 | 57.1 | | | | not measured: as event.ADP | | |
| `event.GM` | 35 | 35 | 35.0 | | | | not measured: as event.ADP | | |
| `event.LINK` | 135 | 180 | 334.3 | | | | not measured: as event.ADP | | |
| `centisecond` | 120 | 390 | 1315.7 | 1150 | 1460 | 2522.9 | 1470 (139,794, 5,624) | -154.3 | +1052.9 |
| `events_none` | 25 | 30 | 47.1 | | | | not measured: as events | | |
| `rebuild` | 290 | 690 | 2061.4 | 830 | 1930 | 5701.4 | 7240 (689,368, 104) | -5178.6 | -1538.6 |
| `polls_least` | 49 | 146 | 478.6 | | | | not measured: as events: parts.py records the least polls of a pass that took a record, read at service_rx | | |
| `events` | 195 | 405 | 1125.0 | | | | not measured: parts.py cuts a pass's events at ctrl_loop's service_rx, which this base's image inlines | | |
| `base` | 155 | 280 | 708.6 | | | | not measured: graded by S2b round 22's poll_grade.py on its own head's loop, which this base does not carry | | |
| `item.withdraw` | 90 | 245 | 776.4 | | | | not measured: as base | | |
| `item.rebuild` | 290 | 630 | 1795.7 | | | | not measured: as base | | |
| `item.walk` | 20 | 60 | 197.1 | | | | not measured: as base | | |
| `item.reclaim` | 25 | 35 | 69.3 | | | | not measured: as base | | |
| `item.retained` | 250 | 395 | 892.1 | | | | not measured: as base | | |
| `item.mrpdu` | 405 | 1215 | 3992.1 | | | | not measured: as base | | |
| `item.acmp` | 65 | 185 | 596.4 | | | | not measured: as base | | |
| `item.aecp` | 225 | 340 | 734.3 | | | | not measured: as base | | |
