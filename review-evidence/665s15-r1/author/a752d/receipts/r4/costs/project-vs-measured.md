The 32x32/2if image: `ctrl_app.elf` SHA-256 `2e47b49efd9262d3dc1628c355ee646e24a2b758ae550c12ee8bb07c6e2facae`.

| Cost | S2b 1x1/1if, us | S2b 8x8/2if, us | S2b projected 32x32/2if, us | measured 32x32/2if, us (most cycles, instances) | error of S2b's, us | round 2 measured, us |
|---|---:|---:|---:|---:|---:|---:|
| `record.srp` | 250 | 395 | 892.1 | 1085 (102,945, 70) | -192.9 | 1085 |
| `record.aecp` | 200 | 255 | 443.6 | 2245 (213,463, 148) | -1801.4 | 2245 |
| `record.acmp` | 280 | 430 | 944.3 | 2365 (224,785, 127) | -1420.7 | 2505 |
| `record.adp` | 105 | 230 | 658.6 | 1920 (182,813, 54) | -1261.4 | 1955 |
| `record.maap` | 90 | 125 | 245.0 | 615 (58,305, 30) | -370.0 | 615 |
| `event.ADP` | 100 | 110 | 144.3 | not measured: S2b's eventcost.py figure, from its own head's event records; not run here | | |
| `event.ACMP` | 170 | 340 | 922.9 | not measured: S2b's eventcost.py figure, from its own head's event records; not run here | | |
| `event.MAAP` | 160 | 215 | 403.6 | not measured: S2b's eventcost.py figure, from its own head's event records; not run here | | |
| `event.AECP` | 60 | 95 | 215.0 | not measured: S2b's eventcost.py figure, from its own head's event records; not run here | | |
| `event.TICK` | 35 | 40 | 57.1 | not measured: S2b's eventcost.py figure, from its own head's event records; not run here | | |
| `event.GM` | 35 | 35 | 35.0 | not measured: S2b's eventcost.py figure, from its own head's event records; not run here | | |
| `event.LINK` | 135 | 180 | 334.3 | not measured: S2b's eventcost.py figure, from its own head's event records; not run here | | |
| `centisecond` | 120 | 390 | 1315.7 | 1470 (139,926, 7,354) | -154.3 | 1470 |
| `events_none` | 25 | 30 | 47.1 | not measured: as events | | |
| `rebuild` | 290 | 690 | 2061.4 | 7215 (687,033, 41) | -5153.6 | 7240 |
| `polls_least` | 49 | 146 | 478.6 | not measured: as events: parts.py records the least polls of a pass that took a record, read at service_rx | | |
| `events` | 195 | 405 | 1125.0 | not measured: parts.py cuts a pass's events at ctrl_loop's service_rx, which this base's image inlines | | |
| `base` | 155 | 280 | 708.6 | not measured: graded by S2b round 22's poll_grade.py on its own head's loop, which this base does not carry | | |
| `item.withdraw` | 90 | 245 | 776.4 | not measured: as base | | |
| `item.rebuild` | 290 | 630 | 1795.7 | not measured: as base | | |
| `item.walk` | 20 | 60 | 197.1 | not measured: as base | | |
| `item.reclaim` | 25 | 35 | 69.3 | not measured: as base | | |
| `item.retained` | 250 | 395 | 892.1 | not measured: as base | | |
| `item.mrpdu` | 405 | 1215 | 3992.1 | not measured: as base | | |
| `item.acmp` | 65 | 185 | 596.4 | not measured: as base | | |
| `item.aecp` | 225 | 340 | 734.3 | not measured: as base | | |
