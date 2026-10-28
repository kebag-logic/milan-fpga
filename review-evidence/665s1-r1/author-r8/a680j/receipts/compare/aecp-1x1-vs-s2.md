# aecp group, arm A, 1x1: S2's final regrade beside this head

reference: 665s2-a681e/receipts/head-regrade/A1/table.md (sha256 a835c98b8bb61393...)
this run: A1/results/table.md (sha256 3a9094eda37b4ff5...)

reference rows 25, this run 25, common 25
| Probe | ref cycles | ref ms | ref verdict | ref pass cycles | ref accesses | cycles | ms | verdict | pass cycles | accesses | d ms | d accesses |
|---|---:|---:|---|---:|---:|---:|---:|---|---:|---:|---:|---:|
| aecp.entity_available.if0 | 224,574 | 4.491 | fits | 281,637 | 57 | 199,533 | 3.991 | fits | 256,807 | 51 | -0.500 | -6 |
| aecp.get_avb_info.if0 | 225,726 | 4.515 | fits | 282,789 | 53 | 200,805 | 4.016 | fits | 258,079 | 48 | -0.499 | -5 |
| aecp.get_configuration.if0 | 221,120 | 4.422 | fits | 278,179 | 53 | 195,950 | 3.919 | fits | 253,220 | 47 | -0.503 | -6 |
| aecp.get_counters.if0 | 245,872 | 4.917 | fits | 302,935 | 86 | 248,194 | 4.964 | fits | 305,468 | 92 | +0.047 | +6 |
| aecp.get_name.if0 | 234,665 | 4.693 | fits | 291,728 | 70 | 209,569 | 4.191 | fits | 266,843 | 64 | -0.502 | -6 |
| aecp.lock_entity.if0 | 197,776 | 3.956 | fits | 270,477 | 66 | 208,381 | 4.168 | fits | 281,333 | 78 | +0.212 | +12 |
| aecp.mvu_get_milan_info.if0 | 124,768 | 2.495 | fits | 181,831 | 50 | 125,604 | 2.512 | fits | 182,878 | 51 | +0.017 | +1 |
| aecp.read_descriptor.t0.i0.c0.if0 | 257,171 | 5.143 | fits | 314,234 | 124 | 258,032 | 5.161 | fits | 315,306 | 125 | +0.018 | +1 |
| aecp.read_descriptor.t1.i0.c0.if0 | 216,609 | 4.332 | fits | 273,668 | 73 | 217,470 | 4.349 | fits | 274,740 | 74 | +0.017 | +1 |
| aecp.read_descriptor.t10.i2.c0.if0 | 239,468 | 4.789 | fits | 296,531 | 74 | 214,139 | 4.283 | fits | 271,413 | 68 | -0.506 | -6 |
| aecp.read_descriptor.t12.i0.c0.if0 | 236,487 | 4.730 | fits | 293,546 | 71 | 211,655 | 4.233 | fits | 268,925 | 65 | -0.497 | -6 |
| aecp.read_descriptor.t13.i0.c0.if0 | 310,400 | 6.208 | fits | 367,459 | 166 | 311,673 | 6.233 | fits | 368,943 | 167 | +0.025 | +1 |
| aecp.read_descriptor.t14.i0.c0.if0 | 201,335 | 4.027 | fits | 258,394 | 52 | 201,801 | 4.036 | fits | 259,071 | 52 | +0.009 | +0 |
| aecp.read_descriptor.t15.i0.c0.if0 | 201,044 | 4.021 | fits | 258,103 | 51 | 201,905 | 4.038 | fits | 259,175 | 52 | +0.017 | +1 |
| aecp.read_descriptor.t2.i0.c0.if0 | 224,564 | 4.491 | fits | 281,623 | 83 | 225,425 | 4.508 | fits | 282,695 | 84 | +0.017 | +1 |
| aecp.read_descriptor.t20.i24.c0.if0 | 243,237 | 4.865 | fits | 300,296 | 75 | 244,780 | 4.896 | fits | 302,050 | 76 | +0.031 | +1 |
| aecp.read_descriptor.t26.i0.c0.if0 | 247,660 | 4.953 | fits | 304,719 | 81 | 249,460 | 4.989 | fits | 306,730 | 82 | +0.036 | +1 |
| aecp.read_descriptor.t36.i0.c0.if0 | 241,937 | 4.839 | fits | 298,996 | 73 | 216,982 | 4.340 | fits | 274,252 | 68 | -0.499 | -5 |
| aecp.read_descriptor.t5.i1.c0.if0 | 224,263 | 4.485 | fits | 281,326 | 82 | 225,124 | 4.502 | fits | 282,398 | 83 | +0.017 | +1 |
| aecp.read_descriptor.t6.i1.c0.if0 | 250,655 | 5.013 | fits | 307,718 | 89 | 252,132 | 5.043 | fits | 309,406 | 90 | +0.030 | +1 |
| aecp.read_descriptor.t9.i0.c0.if0 | 242,152 | 4.843 | fits | 299,215 | 78 | 217,316 | 4.346 | fits | 274,590 | 73 | -0.497 | -5 |
| aecp.register_unsolicited.if0 | 123,766 | 2.475 | fits | 180,352 | 46 | 124,622 | 2.492 | fits | 181,419 | 47 | +0.017 | +1 |
| aecp.set_name.if0 | 240,454 | 4.809 | fits | 345,233 | 106 | 248,464 | 4.969 | fits | 359,918 | 127 | +0.160 | +21 |
| aecp.unknown_command.if0 | 221,061 | 4.421 | fits | 278,124 | 53 | 195,777 | 3.916 | fits | 253,051 | 47 | -0.505 | -6 |
| aecp.unlock_entity.if0 | 197,404 | 3.948 | fits | 270,094 | 65 | 208,002 | 4.160 | fits | 280,915 | 77 | +0.212 | +12 |
