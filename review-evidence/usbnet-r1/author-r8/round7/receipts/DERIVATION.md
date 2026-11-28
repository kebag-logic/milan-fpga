# Complete measured derivation

The inherited rule and dispositions are unchanged. This table reports the complete census, including its failure.

| Cost | Measured maximum (us) | Rule (us) | Witness |
|---|---:|---:|---|
| base | 223.23750 | 235 | none/save-burst |
| build | 981.40000 | 1035 | none/srp |
| build_one | 626.46250 | 660 | arm-two/srp |
| centisecond | 148.06250 | 160 | none/srp-bound |
| event.AMAP_LIVE_WRITE | 14.10000 | 15 | none/datapath-events |
| event.AS_PATH_CHANGED | 25.02500 | 30 | none/datapath-events |
| event.AVB_INFO_CHANGED | 25.00000 | 30 | none/datapath-events |
| event.GM | 36.70000 | 40 | answering-every-port/notice-burst-3 |
| event.LINK | 191.61250 | 205 | none/srp-kept |
| event.TICK | 43.81250 | 50 | none/backlog-adp@program-aged2-6 |
| event.TIMER#0 | 86.63750 | 95 | arm-declaring/aecp-fanout |
| event.TIMER#1 | 163.58750 | 175 | none/save-bind-in-verify-late |
| event.TIMER#2 | 153.20000 | 165 | none/acmp-noresp |
| event.TIMER#3 | 79.90000 | 85 | answering-every-port/notice-burst-1 |
| events_none | 36.82500 | 40 | none/srp-bound |
| item.acmp | 53.20000 | 60 | arm-a/backlog-owed |
| item.acmp_declined | 17.48750 | 20 | none/backlog-owed |
| item.acmp_kept | 81.21250 | 90 | arm-a/backlog-owed |
| item.aecp | 187.83750 | 200 | none/aecp-fanout |
| item.aecp_long | 363.01250 | 385 | declaring-outputs/aecp-largest-notice |
| item.mrpdu | 0.00000 | 0 | arm-a/aecp-largest-notice |
| item.rebuild | 238.57500 | 255 | none/backlog |
| item.reclaim | 15.98750 | 20 | arm-two/srp |
| item.record | 278.26250 | 295 | none/backlog-adp@program-aged2-6 |
| item.retained | 0.00000 | 0 | arm-a/aecp-largest-notice |
| item.walk | 24.47500 | 30 | arm-two/srp |
| item.withdraw | 88.68750 | 95 | none/srp-kept |
| paced.44 | 290.28750 | 305 | arm-declaring/aecp-fanout |
| paced.45 | 316.60000 | 335 | none/aecp-fanout |
| paced.6 | 308.92500 | 325 | declaring-outputs/aecp-fanout |
| record.acmp | 232.53750 | 245 | none/save-bind-in-erase |
| record.adp | 116.08750 | 125 | none/acmp-disc |
| record.aecp.long | 1048.87500 | 1105 | none/aecp-largest-notice |
| record.aecp.other | 273.32500 | 290 | declaring-outputs/aecp-outputs |
| record.aecp.paced | 316.60000 | 335 | none/aecp-fanout |
| record.maap | 116.96250 | 125 | valid-destinations/srp-talker-loss |
| record.srp | 283.17500 | 300 | none/backlog-adp@verify-aged2-6 |
| share | 1793.73750 | 1885 | answering-every-port/notice-every-7 |
| step | 1008.71250 | 1060 | none/backlog-adp@program-aged2-4 |
| tx.aecp.long | 363.01250 | 385 | declaring-outputs/aecp-largest-notice |
| tx.aecp.notice | 193.43750 | 205 | answering-every-port/notice-burst-6 |
| tx.aecp.response | 44.68750 | 50 | none/save-bind |

| Queued (ms) | Pace (ms) | Slice (us) | Pace rule | Queued rule | ACMP (ms) | txL (ms) | Last (ms) | Owner findings |
|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 125 | 1 | 350 | 10 | None | 29.58 | 114.31 | 245.46 | OWNER txL: 114.31 ms exceeds 49 ms; OWNER last: 245.46 ms exceeds 140 ms |
| 125 | 2 | 350 | 10 | None | 29.36 | 114.31 | 245.46 | OWNER txL: 114.31 ms exceeds 49 ms; OWNER last: 245.46 ms exceeds 140 ms |
| 125 | 3 | 350 | 10 | None | 29.13 | 114.31 | 245.46 | OWNER txL: 114.31 ms exceeds 49 ms; OWNER last: 245.46 ms exceeds 140 ms |
| 125 | 4 | 650 | 10 | None | 29.34 | 82.81 | 156.94 | OWNER txL: 82.81 ms exceeds 49 ms; OWNER last: 156.94 ms exceeds 140 ms |
| 125 | 5 | 650 | 10 | None | 29.29 | 67.78 | 156.59 | OWNER txL: 67.78 ms exceeds 49 ms; OWNER last: 156.59 ms exceeds 140 ms |
| 125 | 6 | 700 | 10 | None | 29.3 | 57.68 | 145.93 | OWNER txL: 57.68 ms exceeds 49 ms; OWNER last: 145.93 ms exceeds 140 ms |
| 125 | 7 | 950 | 10 | 130 | 29.54 | 54.97 | 125.83 | OWNER txL: 54.97 ms exceeds 49 ms |
| 125 | 8 | 950 | 10 | 130 | 29.5 | 53.32 | 125.74 | OWNER txL: 53.32 ms exceeds 49 ms |
| 125 | 9 | 950 | 10 | 130 | 29.5 | 49.84 | 125.69 | OWNER txL: 49.84 ms exceeds 49 ms |
| 125 | 10 | 1250 | 10 | 125 | 29.84 | 48.9 | 117.58 | none |
| 125 | 11 | 1250 | 10 | 125 | 29.79 | 48.9 | 117.54 | none |
| 125 | 12 | 1250 | 10 | 125 | 29.79 | 48.9 | 117.49 | none |
| 125 | 13 | 1250 | 10 | 125 | 29.79 | 48.09 | 117.45 | none |
| 130 | 1 | 350 | 10 | None | 29.58 | 114.31 | 245.46 | OWNER txL: 114.31 ms exceeds 49 ms; OWNER last: 245.46 ms exceeds 140 ms |
| 130 | 2 | 350 | 10 | None | 29.36 | 114.31 | 245.46 | OWNER txL: 114.31 ms exceeds 49 ms; OWNER last: 245.46 ms exceeds 140 ms |
| 130 | 3 | 350 | 10 | None | 29.13 | 114.31 | 245.46 | OWNER txL: 114.31 ms exceeds 49 ms; OWNER last: 245.46 ms exceeds 140 ms |
| 130 | 4 | 650 | 10 | None | 29.34 | 82.81 | 156.94 | OWNER txL: 82.81 ms exceeds 49 ms; OWNER last: 156.94 ms exceeds 140 ms |
| 130 | 5 | 650 | 10 | None | 29.29 | 67.78 | 156.59 | OWNER txL: 67.78 ms exceeds 49 ms; OWNER last: 156.59 ms exceeds 140 ms |
| 130 | 6 | 700 | 10 | None | 29.3 | 57.68 | 145.93 | OWNER txL: 57.68 ms exceeds 49 ms; OWNER last: 145.93 ms exceeds 140 ms |
| 130 | 7 | 900 | 10 | None | 29.45 | 54.88 | 144.91 | OWNER txL: 54.88 ms exceeds 49 ms; OWNER last: 144.91 ms exceeds 140 ms |
| 130 | 8 | 950 | 10 | 130 | 29.5 | 53.32 | 125.74 | OWNER txL: 53.32 ms exceeds 49 ms |
| 130 | 9 | 950 | 10 | 130 | 29.5 | 49.84 | 125.69 | OWNER txL: 49.84 ms exceeds 49 ms |
| 130 | 10 | 950 | 10 | 130 | 29.5 | 48.19 | 125.6 | none |
| 130 | 11 | 950 | 10 | 130 | 29.45 | 48.19 | 125.56 | none |
| 130 | 12 | 950 | 10 | 130 | 29.45 | 48.19 | 125.51 | none |
| 130 | 13 | 950 | 10 | 130 | 29.45 | 47.37 | 125.51 | none |
| 135 | 1 | 350 | 10 | None | 29.58 | 114.31 | 245.46 | OWNER txL: 114.31 ms exceeds 49 ms; OWNER last: 245.46 ms exceeds 140 ms |
| 135 | 2 | 350 | 10 | None | 29.36 | 114.31 | 245.46 | OWNER txL: 114.31 ms exceeds 49 ms; OWNER last: 245.46 ms exceeds 140 ms |
| 135 | 3 | 350 | 10 | None | 29.13 | 114.31 | 245.46 | OWNER txL: 114.31 ms exceeds 49 ms; OWNER last: 245.46 ms exceeds 140 ms |
| 135 | 4 | 650 | 10 | None | 29.34 | 82.81 | 156.94 | OWNER txL: 82.81 ms exceeds 49 ms; OWNER last: 156.94 ms exceeds 140 ms |
| 135 | 5 | 650 | 10 | None | 29.29 | 67.78 | 156.59 | OWNER txL: 67.78 ms exceeds 49 ms; OWNER last: 156.59 ms exceeds 140 ms |
| 135 | 6 | 650 | 10 | None | 29.25 | 57.63 | 156.36 | OWNER txL: 57.63 ms exceeds 49 ms; OWNER last: 156.36 ms exceeds 140 ms |
| 135 | 7 | 700 | 10 | None | 29.25 | 54.68 | 145.75 | OWNER txL: 54.68 ms exceeds 49 ms; OWNER last: 145.75 ms exceeds 140 ms |
| 135 | 8 | 700 | 10 | None | 29.21 | 53.03 | 145.66 | OWNER txL: 53.03 ms exceeds 49 ms; OWNER last: 145.66 ms exceeds 140 ms |
| 135 | 9 | 950 | 10 | 130 | 29.5 | 49.84 | 125.69 | OWNER txL: 49.84 ms exceeds 49 ms |
| 135 | 10 | 950 | 10 | 130 | 29.5 | 48.19 | 125.6 | none |
| 135 | 11 | 950 | 10 | 130 | 29.45 | 48.19 | 125.56 | none |
| 135 | 12 | 950 | 10 | 130 | 29.45 | 48.19 | 125.51 | none |
| 135 | 13 | 950 | 10 | 130 | 29.45 | 47.37 | 125.51 | none |
| 140 | 1 | 350 | 10 | None | 29.58 | 114.31 | 245.46 | OWNER txL: 114.31 ms exceeds 49 ms; OWNER last: 245.46 ms exceeds 140 ms |
| 140 | 2 | 350 | 10 | None | 29.36 | 114.31 | 245.46 | OWNER txL: 114.31 ms exceeds 49 ms; OWNER last: 245.46 ms exceeds 140 ms |
| 140 | 3 | 350 | 10 | None | 29.13 | 114.31 | 245.46 | OWNER txL: 114.31 ms exceeds 49 ms; OWNER last: 245.46 ms exceeds 140 ms |
| 140 | 4 | 400 | 10 | None | 29.05 | 78.92 | 235.45 | OWNER txL: 78.92 ms exceeds 49 ms; OWNER last: 235.45 ms exceeds 140 ms |
| 140 | 5 | 650 | 10 | None | 29.29 | 67.78 | 156.59 | OWNER txL: 67.78 ms exceeds 49 ms; OWNER last: 156.59 ms exceeds 140 ms |
| 140 | 6 | 650 | 10 | None | 29.25 | 57.63 | 156.36 | OWNER txL: 57.63 ms exceeds 49 ms; OWNER last: 156.36 ms exceeds 140 ms |
| 140 | 7 | 650 | 10 | None | 29.2 | 54.63 | 155.92 | OWNER txL: 54.63 ms exceeds 49 ms; OWNER last: 155.92 ms exceeds 140 ms |
| 140 | 8 | 700 | 10 | None | 29.21 | 53.03 | 145.66 | OWNER txL: 53.03 ms exceeds 49 ms; OWNER last: 145.66 ms exceeds 140 ms |
| 140 | 9 | 950 | 10 | 130 | 29.5 | 49.84 | 125.69 | OWNER txL: 49.84 ms exceeds 49 ms |
| 140 | 10 | 950 | 10 | 130 | 29.5 | 48.19 | 125.6 | none |
| 140 | 11 | 950 | 10 | 130 | 29.45 | 48.19 | 125.56 | none |
| 140 | 12 | 950 | 10 | 130 | 29.45 | 48.19 | 125.51 | none |
| 140 | 13 | 950 | 10 | 130 | 29.45 | 47.37 | 125.51 | none |

Derived load: 0.5013971140350877. Retry terms (us): [130, 30, 230].

| Held-egress row | Measured (ms) | Frozen ledger (ms) | Result |
|---|---:|---:|---|
| backlog.owed.if0 | 62.71981 | 62.94 | PASS |
| backlog.owed_behind0.if0 | 62.86221 | 63.08 | PASS |
| backlog.owed_behind1.if0 | 63.00366 | 63.22 | PASS |
| backlog.owed_behind2.if0 | 63.14499 | 63.36 | PASS |
| backlog.owed_behind3.if0 | 63.28611 | 63.51 | PASS |
| backlog-owed.service.acmp.last.if0 | 61.99278 | 62.21 | PASS |
| backlog-owed.service.aecp.last.if0 | 62.03635 | 61.99 | FAIL |

Qualification findings:

- none/backlog-owed: forbidden: {'probe': 'backlog-owed.service.aecp.last.if0', 'row': 'AECP record released under the composed load, last', 'family': 'aecp', 'interface': 0, 'path': ['service.aecp.last', 0], 'start_sys': 218288657, 'wait_ms': 0.0, 'ring': 'aecp', 'ahead': 15, 'in_window': True, 'starved': False, 'pass_cycles': 116720, 'pass_instr': 26279, 'pass_mbx_accesses': 107, 'pass_fetch_share': 0.373, 'pass_fetch_wait_share': 0.2141, 'pass_regions': {'rom': [301, 0, 0], 'mbx': [0, 63, 44], 'csr': [0, 322, 77]}, 'pass_modules': {'ctrl_mem': 30070, 'aecp': 29371, 'mbx': 27850, 'acmp': 6470, 'aecp_commands': 4565, 'ctrl_loop': 4500}, 'end_sys': 223251565, 'sys_cycles': 4962908, 'cpu_cycles': 4962908, 'ms': 62.03635, 'passes': 16, 'budget_ms': 20.0, 'ceiling_ms': 24.0, 'within_budget': False, 'within_ceiling': False, 'status': 'measured'}
- egress-ledger
