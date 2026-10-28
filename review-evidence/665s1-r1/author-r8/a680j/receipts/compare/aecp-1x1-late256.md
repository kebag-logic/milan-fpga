# aecp group, 1x1: this head beside the PROBE acknowledging at 256 bus cycles

reference: <work>/builds/A1/results/table.md (sha256 3a9094eda37b4ff5...)
this run: probe-ack256-1x1/results/table.md (sha256 dc8def9555d60052...)

reference rows 25, this run 25, common 25
| Probe | ref cycles | ref ms | ref verdict | ref pass cycles | ref accesses | cycles | ms | verdict | pass cycles | accesses | d ms | d accesses |
|---|---:|---:|---|---:|---:|---:|---:|---|---:|---:|---:|---:|
| aecp.entity_available.if0 | 199,533 | 3.991 | fits | 256,807 | 51 | 199,533 | 3.991 | fits | 256,807 | 51 | +0.000 | +0 |
| aecp.get_avb_info.if0 | 200,805 | 4.016 | fits | 258,079 | 48 | 200,805 | 4.016 | fits | 258,079 | 48 | +0.000 | +0 |
| aecp.get_configuration.if0 | 195,950 | 3.919 | fits | 253,220 | 47 | 195,950 | 3.919 | fits | 253,220 | 47 | +0.000 | +0 |
| aecp.get_counters.if0 | 248,194 | 4.964 | fits | 305,468 | 92 | 248,194 | 4.964 | fits | 305,468 | 92 | +0.000 | +0 |
| aecp.get_name.if0 | 209,569 | 4.191 | fits | 266,843 | 64 | 209,569 | 4.191 | fits | 266,843 | 64 | +0.000 | +0 |
| aecp.lock_entity.if0 | 208,381 | 4.168 | fits | 281,333 | 78 | 208,551 | 4.171 | fits | 281,503 | 79 | +0.003 | +1 |
| aecp.mvu_get_milan_info.if0 | 125,604 | 2.512 | fits | 182,878 | 51 | 125,604 | 2.512 | fits | 182,878 | 51 | +0.000 | +0 |
| aecp.read_descriptor.t0.i0.c0.if0 | 258,032 | 5.161 | fits | 315,306 | 125 | 258,032 | 5.161 | fits | 315,306 | 125 | +0.000 | +0 |
| aecp.read_descriptor.t1.i0.c0.if0 | 217,470 | 4.349 | fits | 274,740 | 74 | 217,470 | 4.349 | fits | 274,740 | 74 | +0.000 | +0 |
| aecp.read_descriptor.t10.i2.c0.if0 | 214,139 | 4.283 | fits | 271,413 | 68 | 214,139 | 4.283 | fits | 271,413 | 68 | +0.000 | +0 |
| aecp.read_descriptor.t12.i0.c0.if0 | 211,655 | 4.233 | fits | 268,925 | 65 | 211,655 | 4.233 | fits | 268,925 | 65 | +0.000 | +0 |
| aecp.read_descriptor.t13.i0.c0.if0 | 311,673 | 6.233 | fits | 368,943 | 167 | 311,673 | 6.233 | fits | 368,943 | 167 | +0.000 | +0 |
| aecp.read_descriptor.t14.i0.c0.if0 | 201,801 | 4.036 | fits | 259,071 | 52 | 201,801 | 4.036 | fits | 259,071 | 52 | +0.000 | +0 |
| aecp.read_descriptor.t15.i0.c0.if0 | 201,905 | 4.038 | fits | 259,175 | 52 | 201,905 | 4.038 | fits | 259,175 | 52 | +0.000 | +0 |
| aecp.read_descriptor.t2.i0.c0.if0 | 225,425 | 4.508 | fits | 282,695 | 84 | 225,425 | 4.508 | fits | 282,695 | 84 | +0.000 | +0 |
| aecp.read_descriptor.t20.i24.c0.if0 | 244,780 | 4.896 | fits | 302,050 | 76 | 244,780 | 4.896 | fits | 302,050 | 76 | +0.000 | +0 |
| aecp.read_descriptor.t26.i0.c0.if0 | 249,460 | 4.989 | fits | 306,730 | 82 | 249,460 | 4.989 | fits | 306,730 | 82 | +0.000 | +0 |
| aecp.read_descriptor.t36.i0.c0.if0 | 216,982 | 4.340 | fits | 274,252 | 68 | 216,982 | 4.340 | fits | 274,252 | 68 | +0.000 | +0 |
| aecp.read_descriptor.t5.i1.c0.if0 | 225,124 | 4.502 | fits | 282,398 | 83 | 225,124 | 4.502 | fits | 282,398 | 83 | +0.000 | +0 |
| aecp.read_descriptor.t6.i1.c0.if0 | 252,132 | 5.043 | fits | 309,406 | 90 | 252,132 | 5.043 | fits | 309,406 | 90 | +0.000 | +0 |
| aecp.read_descriptor.t9.i0.c0.if0 | 217,316 | 4.346 | fits | 274,590 | 73 | 217,316 | 4.346 | fits | 274,590 | 73 | +0.000 | +0 |
| aecp.register_unsolicited.if0 | 124,622 | 2.492 | fits | 181,419 | 47 | 124,622 | 2.492 | fits | 181,419 | 47 | +0.000 | +0 |
| aecp.set_name.if0 | 248,464 | 4.969 | fits | 359,918 | 127 | 248,634 | 4.973 | fits | 360,222 | 129 | +0.004 | +2 |
| aecp.unknown_command.if0 | 195,777 | 3.916 | fits | 253,051 | 47 | 195,777 | 3.916 | fits | 253,051 | 47 | +0.000 | +0 |
| aecp.unlock_entity.if0 | 208,002 | 4.160 | fits | 280,915 | 77 | 208,172 | 4.163 | fits | 281,085 | 78 | +0.003 | +1 |
