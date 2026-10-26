### 1x1

5 of 30 paths and 5 of 30 probe instances miss T_svc.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| entity_available | 0 | `aecp.entity_available.if0` (aecp) | 4.491 (5.633) | fits | 0 aecp | 1 | 0 |
| get_avb_info | 0 | `aecp.get_avb_info.if0` (aecp) | 4.515 (5.656) | fits | 0 aecp | 1 | 0 |
| get_configuration | 0 | `aecp.get_configuration.if0` (aecp) | 4.422 (5.564) | fits | 0 aecp | 1 | 0 |
| get_counters | 0 | `aecp.get_counters.if0` (aecp) | 4.917 (6.059) | fits | 0 aecp | 1 | 0 |
| get_name | 0 | `aecp.get_name.if0` (aecp) | 4.693 (5.835) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp.lock_entity.if0` (aecp) | 3.956 (5.410) | fits | 0 aecp | 1 | 0 |
| MVU GET_MILAN_INFO | 0 | `aecp.mvu_get_milan_info.if0` (aecp) | 2.495 (3.637) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (312 B) | 0 | `aecp.read_descriptor.t0.i0.c0.if0` (aecp) | 5.143 (6.285) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (106 B) | 0 | `aecp.read_descriptor.t1.i0.c0.if0` (aecp) | 4.332 (5.473) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (86 B) | 0 | `aecp.read_descriptor.t10.i2.c0.if0` (aecp) | 4.789 (5.931) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (72 B) | 0 | `aecp.read_descriptor.t12.i0.c0.if0` (aecp) | 4.730 (5.871) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (452 B) | 0 | `aecp.read_descriptor.t13.i0.c0.if0` (aecp) | 6.208 (7.349) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t14.i0.c0.if0` (aecp) | 4.027 (5.168) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t15.i0.c0.if0` (aecp) | 4.021 (5.162) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (148 B) | 0 | `aecp.read_descriptor.t2.i0.c0.if0` (aecp) | 4.491 (5.632) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (90 B) | 0 | `aecp.read_descriptor.t20.i24.c0.if0` (aecp) | 4.865 (6.006) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (113 B) | 0 | `aecp.read_descriptor.t26.i0.c0.if0` (aecp) | 4.953 (6.094) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (82 B) | 0 | `aecp.read_descriptor.t36.i0.c0.if0` (aecp) | 4.839 (5.980) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t5.i1.c0.if0` (aecp) | 4.485 (5.627) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t6.i1.c0.if0` (aecp) | 5.013 (6.154) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (102 B) | 0 | `aecp.read_descriptor.t9.i0.c0.if0` (aecp) | 4.843 (5.984) | fits | 0 aecp | 1 | 0 |
| register_unsolicited | 0 | `aecp.register_unsolicited.if0` (aecp) | 2.475 (3.607) | fits | 0 aecp | 1 | 0 |
| set_name | 0 | `aecp.set_name.if0` (aecp) | 5.216 (6.905) | fits | 0 aecp | 1 | 0 |
| unknown_command | 0 | `aecp.unknown_command.if0` (aecp) | 4.421 (5.562) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp.unlock_entity.if0` (aecp) | 3.948 (5.402) | fits | 0 aecp | 1 | 0 |
| an ACMP command behind a full acmp ring | 0 | `backlog.acmp_command.if0` (backlog) | 63.304 (70.047) | MISS ceiling | 11 acmp | 1 | 1 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog.adp_available.if0` (backlog-adp) | 67.932 (81.835) | MISS ceiling | 7 adp | 1 | 1 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | 0 | `backlog.adp_available_refill.if0` (backlog-adp-refill) | 88.334 (107.649) | MISS ceiling | 4 adp | 1 | 1 |
| an event behind 15 others | 0 | `backlog.event.if0` (backlog) | 15.487 (29.108) | MISS T_svc | 15 events | 1 | 1 |
| a response with 7 frames owed ahead of it | 0 | `backlog.owed.if0` (backlog-owed) | 125.789 (129.811) | MISS ceiling | 7 acmp | 1 | 1 |

| Path | Probe | CPU cycles | ms | T_svc (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| an event behind 15 others | `backlog.event.if0` | 774,336 | 15.487 | 10 | 200 | MISS T_svc | 715,146 | 355 | 0.879 |
| an ACMP command behind a full acmp ring | `backlog.acmp_command.if0` | 3,165,192 | 63.304 | 10 | 20 | MISS ceiling | 475,100 | 216 | 0.884 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog.adp_available.if0` | 3,396,608 | 67.932 | 10 | 20 | MISS ceiling | 1,565,803 | 365 | 0.889 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | `backlog.adp_available_refill.if0` | 4,416,715 | 88.334 | 10 | 20 | MISS ceiling | 1,520,863 | 303 | 0.890 |
| a response with 7 frames owed ahead of it | `backlog.owed.if0` | 6,289,466 | 125.789 | 10 | 20 | MISS ceiling | 475,611 | 190 | 0.881 |
| register_unsolicited | `aecp.register_unsolicited.if0` | 123,766 | 2.475 | 10 | 24 | fits | 180,352 | 46 | 0.881 |
| READ_DESCRIPTOR (312 B) | `aecp.read_descriptor.t0.i0.c0.if0` | 257,171 | 5.143 | 10 | 24 | fits | 314,234 | 124 | 0.887 |
| READ_DESCRIPTOR (106 B) | `aecp.read_descriptor.t1.i0.c0.if0` | 216,609 | 4.332 | 10 | 24 | fits | 273,668 | 73 | 0.886 |
| READ_DESCRIPTOR (148 B) | `aecp.read_descriptor.t2.i0.c0.if0` | 224,564 | 4.491 | 10 | 24 | fits | 281,623 | 83 | 0.886 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t5.i1.c0.if0` | 224,263 | 4.485 | 10 | 24 | fits | 281,326 | 82 | 0.886 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t6.i1.c0.if0` | 250,655 | 5.013 | 10 | 24 | fits | 307,718 | 89 | 0.888 |
| READ_DESCRIPTOR (102 B) | `aecp.read_descriptor.t9.i0.c0.if0` | 242,152 | 4.843 | 10 | 24 | fits | 299,215 | 78 | 0.888 |
| READ_DESCRIPTOR (86 B) | `aecp.read_descriptor.t10.i2.c0.if0` | 239,468 | 4.789 | 10 | 24 | fits | 296,531 | 74 | 0.888 |
| READ_DESCRIPTOR (72 B) | `aecp.read_descriptor.t12.i0.c0.if0` | 236,487 | 4.730 | 10 | 24 | fits | 293,546 | 71 | 0.888 |
| READ_DESCRIPTOR (452 B) | `aecp.read_descriptor.t13.i0.c0.if0` | 310,400 | 6.208 | 10 | 24 | fits | 367,459 | 166 | 0.889 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t14.i0.c0.if0` | 201,335 | 4.027 | 10 | 24 | fits | 258,394 | 52 | 0.885 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t15.i0.c0.if0` | 201,044 | 4.021 | 10 | 24 | fits | 258,103 | 51 | 0.886 |
| READ_DESCRIPTOR (90 B) | `aecp.read_descriptor.t20.i24.c0.if0` | 243,237 | 4.865 | 10 | 24 | fits | 300,296 | 75 | 0.887 |
| READ_DESCRIPTOR (113 B) | `aecp.read_descriptor.t26.i0.c0.if0` | 247,660 | 4.953 | 10 | 24 | fits | 304,719 | 81 | 0.888 |
| READ_DESCRIPTOR (82 B) | `aecp.read_descriptor.t36.i0.c0.if0` | 241,937 | 4.839 | 10 | 24 | fits | 298,996 | 73 | 0.888 |
| get_configuration | `aecp.get_configuration.if0` | 221,120 | 4.422 | 10 | 24 | fits | 278,179 | 53 | 0.888 |
| entity_available | `aecp.entity_available.if0` | 224,574 | 4.491 | 10 | 24 | fits | 281,637 | 57 | 0.888 |
| get_name | `aecp.get_name.if0` | 234,665 | 4.693 | 10 | 24 | fits | 291,728 | 70 | 0.888 |
| get_counters | `aecp.get_counters.if0` | 245,872 | 4.917 | 10 | 24 | fits | 302,935 | 86 | 0.889 |
| get_avb_info | `aecp.get_avb_info.if0` | 225,726 | 4.515 | 10 | 24 | fits | 282,789 | 53 | 0.887 |
| unknown_command | `aecp.unknown_command.if0` | 221,061 | 4.421 | 10 | 24 | fits | 278,124 | 53 | 0.888 |
| MVU GET_MILAN_INFO | `aecp.mvu_get_milan_info.if0` | 124,768 | 2.495 | 10 | 24 | fits | 181,831 | 50 | 0.881 |
| set_name | `aecp.set_name.if0` | 260,812 | 5.216 | 10 | 24 | fits | 345,233 | 106 | 0.882 |
| lock_entity | `aecp.lock_entity.if0` | 197,776 | 3.956 | 10 | 24 | fits | 270,477 | 66 | 0.885 |
| unlock_entity | `aecp.unlock_entity.if0` | 197,404 | 3.948 | 10 | 24 | fits | 270,094 | 65 | 0.885 |

Bounded waits that timed out (the probe is graded on what the log holds):

- `backlog-adp`: wait quiet TIMEOUT
- `backlog-adp`: wait quiet TIMEOUT
- `backlog-adp`: wait quiet TIMEOUT
- `backlog-adp`: wait quiet TIMEOUT
- `backlog-adp-refill`: wait quiet TIMEOUT
- `backlog-adp-refill`: wait quiet TIMEOUT
- `backlog-adp-refill`: wait quiet TIMEOUT
- `backlog-adp-refill`: wait quiet TIMEOUT
