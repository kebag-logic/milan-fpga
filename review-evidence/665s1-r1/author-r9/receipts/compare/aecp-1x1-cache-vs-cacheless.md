# aecp group, arm A, 1x1: this lane's cacheless run (665s1-a680j, at 0eda061a, before the merge) beside this head's split-cache run

reference: 665s1-a680j/receipts/runs/A1/results/table.md (sha256 3a9094eda37b4ff5...)
this run: runs/A1/results/table.md (sha256 0a025d4ce792cb7b...)

reference rows 25, this run 25, common 25
| Probe | ref cycles | ref ms | ref verdict | ref pass cycles | ref accesses | cycles | ms | verdict | pass cycles | accesses | d ms | d accesses |
|---|---:|---:|---|---:|---:|---:|---:|---|---:|---:|---:|---:|
| aecp.entity_available.if0 | 199,533 | 3.991 | fits | 256,807 | 51 | 108,270 | 2.165 | fits | 147,152 | 52 | -1.826 | +1 |
| aecp.get_avb_info.if0 | 200,805 | 4.016 | fits | 258,079 | 48 | 124,962 | 2.499 | fits | 163,844 | 54 | -1.517 | +6 |
| aecp.get_configuration.if0 | 195,950 | 3.919 | fits | 253,220 | 47 | 121,981 | 2.440 | fits | 160,860 | 54 | -1.479 | +7 |
| aecp.get_counters.if0 | 248,194 | 4.964 | fits | 305,468 | 92 | 121,167 | 2.423 | fits | 160,049 | 86 | -2.541 | -6 |
| aecp.get_name.if0 | 209,569 | 4.191 | fits | 266,843 | 64 | 114,449 | 2.289 | fits | 153,331 | 65 | -1.902 | +1 |
| aecp.lock_entity.if0 | 208,381 | 4.168 | fits | 281,333 | 78 | 114,585 | 2.292 | fits | 162,809 | 77 | -1.876 | -1 |
| aecp.mvu_get_milan_info.if0 | 125,604 | 2.512 | fits | 182,878 | 51 | 72,384 | 1.448 | fits | 111,209 | 52 | -1.064 | +1 |
| aecp.read_descriptor.t0.i0.c0.if0 | 258,032 | 5.161 | fits | 315,306 | 125 | 141,675 | 2.833 | fits | 180,557 | 126 | -2.328 | +1 |
| aecp.read_descriptor.t1.i0.c0.if0 | 217,470 | 4.349 | fits | 274,740 | 74 | 118,598 | 2.372 | fits | 157,477 | 74 | -1.977 | +0 |
| aecp.read_descriptor.t10.i2.c0.if0 | 214,139 | 4.283 | fits | 271,413 | 68 | 117,003 | 2.340 | fits | 155,885 | 69 | -1.943 | +1 |
| aecp.read_descriptor.t12.i0.c0.if0 | 211,655 | 4.233 | fits | 268,925 | 65 | 115,607 | 2.312 | fits | 154,486 | 66 | -1.921 | +1 |
| aecp.read_descriptor.t13.i0.c0.if0 | 311,673 | 6.233 | fits | 368,943 | 167 | 172,109 | 3.442 | fits | 210,988 | 167 | -2.791 | +0 |
| aecp.read_descriptor.t14.i0.c0.if0 | 201,801 | 4.036 | fits | 259,071 | 52 | 110,119 | 2.202 | fits | 148,998 | 53 | -1.834 | +1 |
| aecp.read_descriptor.t15.i0.c0.if0 | 201,905 | 4.038 | fits | 259,175 | 52 | 110,183 | 2.204 | fits | 149,062 | 53 | -1.834 | +1 |
| aecp.read_descriptor.t2.i0.c0.if0 | 225,425 | 4.508 | fits | 282,695 | 84 | 138,512 | 2.770 | fits | 177,391 | 91 | -1.738 | +7 |
| aecp.read_descriptor.t20.i24.c0.if0 | 244,780 | 4.896 | fits | 302,050 | 76 | 134,915 | 2.698 | fits | 173,794 | 76 | -2.198 | +0 |
| aecp.read_descriptor.t26.i0.c0.if0 | 249,460 | 4.989 | fits | 306,730 | 82 | 121,856 | 2.437 | fits | 160,735 | 76 | -2.552 | -6 |
| aecp.read_descriptor.t36.i0.c0.if0 | 216,982 | 4.340 | fits | 274,252 | 68 | 118,537 | 2.371 | fits | 157,416 | 68 | -1.969 | +0 |
| aecp.read_descriptor.t5.i1.c0.if0 | 225,124 | 4.502 | fits | 282,398 | 83 | 123,090 | 2.462 | fits | 161,972 | 84 | -2.040 | +1 |
| aecp.read_descriptor.t6.i1.c0.if0 | 252,132 | 5.043 | fits | 309,406 | 90 | 123,218 | 2.464 | fits | 162,100 | 84 | -2.579 | -6 |
| aecp.read_descriptor.t9.i0.c0.if0 | 217,316 | 4.346 | fits | 274,590 | 73 | 133,925 | 2.679 | fits | 172,807 | 79 | -1.667 | +6 |
| aecp.register_unsolicited.if0 | 124,622 | 2.492 | fits | 181,419 | 47 | 87,061 | 1.741 | fits | 125,616 | 54 | -0.751 | +7 |
| aecp.set_name.if0 | 248,464 | 4.969 | fits | 359,918 | 127 | 139,949 | 2.799 | fits | 209,113 | 127 | -2.170 | +0 |
| aecp.unknown_command.if0 | 195,777 | 3.916 | fits | 253,051 | 47 | 106,236 | 2.125 | fits | 145,118 | 48 | -1.791 | +1 |
| aecp.unlock_entity.if0 | 208,002 | 4.160 | fits | 280,915 | 77 | 114,830 | 2.297 | fits | 162,929 | 78 | -1.863 | +1 |
