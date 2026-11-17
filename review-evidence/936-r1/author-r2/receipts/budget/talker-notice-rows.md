Original file: <scratch>/r2/final/talker-notice-rows.md
Original size: 9949 bytes
Original sha256: 2ff7de57bb10faa6f7e767395a60da21cea53305941995082f2fb0c5d22c5b18

# The talker-notices arm: every row, per run

Each row is the harness's own grade (`results.json`, `run.py --variant talker-notices`) on a fresh clean clone of the final head `d1aa4c44`. Times in system cycles at 100 MHz; elapsed from the event's mailbox RX commit to the last required recipient's commit (FR_NFR.md 3.4.1); bound min(T_svc, 24 ms) = 20 ms (`notify`).

## 1x1/1if, unplanted

- Clone: `d1aa4c44`, dirty 0. Image: `ctrl_app.elf` sha256 `ec6f006694a16da7`; simulator `18d9768144d47ce7`; variant `talker-notices`, mutation `none`.
- Run: {'paths': 2, 'path_misses': 0, 'instances': 16, 'instance_misses': 0}; refusals 0; budget misses 0; rc 0.

| Row | Event | Event committed, sys | Recipients | Last recipient committed, sys | Elapsed, ms | Bound, ms | Verdict |
|---|---|---:|---:|---:|---:|---:|---|
| `talker-notice-0.declared.if0` | PROBE_TX (ACMP RX commit) | 300000965 | 16 | 300530646 | 5.297 | 20 | within |
| `talker-notice-0.withdrawn.if0` | ANNOUNCE (MAAP RX commit) | 360000955 | 16 | 360559486 | 5.585 | 20 | within |
| `talker-notice-1.declared.if0` | PROBE_TX (ACMP RX commit) | 300100141 | 16 | 300788856 | 6.887 | 20 | within |
| `talker-notice-1.withdrawn.if0` | ANNOUNCE (MAAP RX commit) | 360100131 | 16 | 360564919 | 4.648 | 20 | within |
| `talker-notice-2.declared.if0` | PROBE_TX (ACMP RX commit) | 300200141 | 16 | 300757136 | 5.570 | 20 | within |
| `talker-notice-2.withdrawn.if0` | ANNOUNCE (MAAP RX commit) | 360200131 | 16 | 360723208 | 5.231 | 20 | within |
| `talker-notice-3.declared.if0` | PROBE_TX (ACMP RX commit) | 300300141 | 16 | 300756493 | 4.564 | 20 | within |
| `talker-notice-3.withdrawn.if0` | ANNOUNCE (MAAP RX commit) | 360300131 | 16 | 360721440 | 4.213 | 20 | within |
| `talker-notice-4.declared.if0` | PROBE_TX (ACMP RX commit) | 300400141 | 16 | 300831616 | 4.315 | 20 | within |
| `talker-notice-4.withdrawn.if0` | ANNOUNCE (MAAP RX commit) | 360400131 | 16 | 360863436 | 4.633 | 20 | within |
| `talker-notice-5.declared.if0` | PROBE_TX (ACMP RX commit) | 300500141 | 16 | 300849003 | 3.489 | 20 | within |
| `talker-notice-5.withdrawn.if0` | ANNOUNCE (MAAP RX commit) | 360500131 | 16 | 360878035 | 3.779 | 20 | within |
| `talker-notice-6.declared.if0` | PROBE_TX (ACMP RX commit) | 300600141 | 16 | 300868285 | 2.681 | 20 | within |
| `talker-notice-6.withdrawn.if0` | ANNOUNCE (MAAP RX commit) | 360600131 | 16 | 360902162 | 3.020 | 20 | within |
| `talker-notice-7.declared.if0` | PROBE_TX (ACMP RX commit) | 300700141 | 16 | 300904430 | 2.043 | 20 | within |
| `talker-notice-7.withdrawn.if0` | ANNOUNCE (MAAP RX commit) | 360700131 | 16 | 360918814 | 2.187 | 20 | within |

## 8x8/1if, unplanted

- Clone: `d1aa4c44`, dirty 0. Image: `ctrl_app.elf` sha256 `b8d11ef552b38ffb`; simulator `953aca3448a5be1d`; variant `talker-notices`, mutation `none`.
- Run: {'paths': 2, 'path_misses': 0, 'instances': 16, 'instance_misses': 0}; refusals 0; budget misses 0; rc 0.

| Row | Event | Event committed, sys | Recipients | Last recipient committed, sys | Elapsed, ms | Bound, ms | Verdict |
|---|---|---:|---:|---:|---:|---:|---|
| `talker-notice-0.declared.if0` | PROBE_TX (ACMP RX commit) | 300000965 | 16 | 300542901 | 5.419 | 20 | within |
| `talker-notice-0.withdrawn.if0` | ANNOUNCE (MAAP RX commit) | 360000955 | 16 | 360756249 | 7.553 | 20 | within |
| `talker-notice-1.declared.if0` | PROBE_TX (ACMP RX commit) | 300100141 | 16 | 300827737 | 7.276 | 20 | within |
| `talker-notice-1.withdrawn.if0` | ANNOUNCE (MAAP RX commit) | 360100131 | 16 | 360760828 | 6.607 | 20 | within |
| `talker-notice-2.declared.if0` | PROBE_TX (ACMP RX commit) | 300200141 | 16 | 300778031 | 5.779 | 20 | within |
| `talker-notice-2.withdrawn.if0` | ANNOUNCE (MAAP RX commit) | 360200131 | 16 | 360757666 | 5.575 | 20 | within |
| `talker-notice-3.declared.if0` | PROBE_TX (ACMP RX commit) | 300300141 | 16 | 300778031 | 4.779 | 20 | within |
| `talker-notice-3.withdrawn.if0` | ANNOUNCE (MAAP RX commit) | 360300131 | 16 | 360757153 | 4.570 | 20 | within |
| `talker-notice-4.declared.if0` | PROBE_TX (ACMP RX commit) | 300400141 | 16 | 300855332 | 4.552 | 20 | within |
| `talker-notice-4.withdrawn.if0` | ANNOUNCE (MAAP RX commit) | 360400131 | 16 | 360758710 | 3.586 | 20 | within |
| `talker-notice-5.declared.if0` | PROBE_TX (ACMP RX commit) | 300500141 | 16 | 300878554 | 3.784 | 20 | within |
| `talker-notice-5.withdrawn.if0` | ANNOUNCE (MAAP RX commit) | 360500131 | 16 | 360881828 | 3.817 | 20 | within |
| `talker-notice-6.declared.if0` | PROBE_TX (ACMP RX commit) | 300600141 | 16 | 300902561 | 3.024 | 20 | within |
| `talker-notice-6.withdrawn.if0` | ANNOUNCE (MAAP RX commit) | 360600131 | 16 | 360929780 | 3.296 | 20 | within |
| `talker-notice-7.declared.if0` | PROBE_TX (ACMP RX commit) | 300700141 | 16 | 300924649 | 2.245 | 20 | within |
| `talker-notice-7.withdrawn.if0` | ANNOUNCE (MAAP RX commit) | 360700131 | 16 | 360961687 | 2.616 | 20 | within |

## 1x1/1if, plant declared-notice-dropped

- Clone: `d1aa4c44`, dirty 0. Image: `ctrl_app.elf` sha256 `cebd77923bcd8c49`; simulator `1ec1007fe9a3b758`; variant `talker-notices`, mutation `declared-notice-dropped`.
- Run: {'paths': 0, 'path_misses': 0, 'instances': 0, 'instance_misses': 0}; refusals 16; budget misses 0; rc 0. `CONTROL declared-notice-dropped caught: 16 of 16 talker-notice row(s) with no notice (talker-notice-0.declared...`

| Row | Event | Event committed, sys | Recipients | Last recipient committed, sys | Elapsed, ms | Bound, ms | Verdict |
|---|---|---:|---:|---:|---:|---:|---|
| `talker-notice-0.declared.if0` | PROBE_TX (ACMP RX commit) | 300000965 | 0 of 16 | - | - | 20 | no end: no notification |
| `talker-notice-0.withdrawn.if0` | ANNOUNCE (MAAP RX commit) | 360000955 | 0 of 16 | - | - | 20 | no end: no notification |
| `talker-notice-1.declared.if0` | PROBE_TX (ACMP RX commit) | 300100141 | 0 of 16 | - | - | 20 | no end: no notification |
| `talker-notice-1.withdrawn.if0` | ANNOUNCE (MAAP RX commit) | 360100131 | 0 of 16 | - | - | 20 | no end: no notification |
| `talker-notice-2.declared.if0` | PROBE_TX (ACMP RX commit) | 300200141 | 0 of 16 | - | - | 20 | no end: no notification |
| `talker-notice-2.withdrawn.if0` | ANNOUNCE (MAAP RX commit) | 360200131 | 0 of 16 | - | - | 20 | no end: no notification |
| `talker-notice-3.declared.if0` | PROBE_TX (ACMP RX commit) | 300300141 | 0 of 16 | - | - | 20 | no end: no notification |
| `talker-notice-3.withdrawn.if0` | ANNOUNCE (MAAP RX commit) | 360300131 | 0 of 16 | - | - | 20 | no end: no notification |
| `talker-notice-4.declared.if0` | PROBE_TX (ACMP RX commit) | 300400141 | 0 of 16 | - | - | 20 | no end: no notification |
| `talker-notice-4.withdrawn.if0` | ANNOUNCE (MAAP RX commit) | 360400131 | 0 of 16 | - | - | 20 | no end: no notification |
| `talker-notice-5.declared.if0` | PROBE_TX (ACMP RX commit) | 300500141 | 0 of 16 | - | - | 20 | no end: no notification |
| `talker-notice-5.withdrawn.if0` | ANNOUNCE (MAAP RX commit) | 360500131 | 0 of 16 | - | - | 20 | no end: no notification |
| `talker-notice-6.declared.if0` | PROBE_TX (ACMP RX commit) | 300600141 | 0 of 16 | - | - | 20 | no end: no notification |
| `talker-notice-6.withdrawn.if0` | ANNOUNCE (MAAP RX commit) | 360600131 | 0 of 16 | - | - | 20 | no end: no notification |
| `talker-notice-7.declared.if0` | PROBE_TX (ACMP RX commit) | 300700141 | 0 of 16 | - | - | 20 | no end: no notification |
| `talker-notice-7.withdrawn.if0` | ANNOUNCE (MAAP RX commit) | 360700131 | 0 of 16 | - | - | 20 | no end: no notification |

## 1x1/1if, plant declared-notice-delayed

- Clone: `d1aa4c44`, dirty 0. Image: `ctrl_app.elf` sha256 `25a65fe50ddbde68`; simulator `b33307a2e16db70d`; variant `talker-notices`, mutation `declared-notice-delayed`.
- Run: {'paths': 2, 'path_misses': 2, 'instances': 16, 'instance_misses': 16}; refusals 0; budget misses 16; rc 0. `CONTROL declared-notice-delayed caught: 16 of 16 talker-notice row(s) with their notice later than its bound (...`

| Row | Event | Event committed, sys | Recipients | Last recipient committed, sys | Elapsed, ms | Bound, ms | Verdict |
|---|---|---:|---:|---:|---:|---:|---|
| `talker-notice-0.declared.if0` | PROBE_TX (ACMP RX commit) | 300000965 | 16 | 302967153 | 29.662 | 20 | OVER |
| `talker-notice-0.withdrawn.if0` | ANNOUNCE (MAAP RX commit) | 360000955 | 16 | 362958274 | 29.573 | 20 | OVER |
| `talker-notice-1.declared.if0` | PROBE_TX (ACMP RX commit) | 300100141 | 16 | 303156918 | 30.568 | 20 | OVER |
| `talker-notice-1.withdrawn.if0` | ANNOUNCE (MAAP RX commit) | 360100131 | 16 | 362962392 | 28.623 | 20 | OVER |
| `talker-notice-2.declared.if0` | PROBE_TX (ACMP RX commit) | 300200141 | 16 | 303173371 | 29.732 | 20 | OVER |
| `talker-notice-2.withdrawn.if0` | ANNOUNCE (MAAP RX commit) | 360200131 | 16 | 363159503 | 29.594 | 20 | OVER |
| `talker-notice-3.declared.if0` | PROBE_TX (ACMP RX commit) | 300300141 | 16 | 303172368 | 28.722 | 20 | OVER |
| `talker-notice-3.withdrawn.if0` | ANNOUNCE (MAAP RX commit) | 360300131 | 16 | 363061508 | 27.614 | 20 | OVER |
| `talker-notice-4.declared.if0` | PROBE_TX (ACMP RX commit) | 300400141 | 16 | 303265867 | 28.657 | 20 | OVER |
| `talker-notice-4.withdrawn.if0` | ANNOUNCE (MAAP RX commit) | 360400131 | 16 | 363257290 | 28.572 | 20 | OVER |
| `talker-notice-5.declared.if0` | PROBE_TX (ACMP RX commit) | 300500141 | 16 | 303262513 | 27.624 | 20 | OVER |
| `talker-notice-5.withdrawn.if0` | ANNOUNCE (MAAP RX commit) | 360500131 | 16 | 363364513 | 28.644 | 20 | OVER |
| `talker-notice-6.declared.if0` | PROBE_TX (ACMP RX commit) | 300600141 | 16 | 303357202 | 27.571 | 20 | OVER |
| `talker-notice-6.withdrawn.if0` | ANNOUNCE (MAAP RX commit) | 360600131 | 16 | 363366241 | 27.661 | 20 | OVER |
| `talker-notice-7.declared.if0` | PROBE_TX (ACMP RX commit) | 300700141 | 16 | 303374260 | 26.741 | 20 | OVER |
| `talker-notice-7.withdrawn.if0` | ANNOUNCE (MAAP RX commit) | 360700131 | 16 | 363364274 | 26.641 | 20 | OVER |

