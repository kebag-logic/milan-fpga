# aecp group, arm A, 8x8: S2's final regrade beside this head

reference: 665s2-a681e/receipts/head-regrade/A8/table.md (sha256 599f196187b5fd5d...)
this run: A8/results/table.md (sha256 c77c89dcfdb58bde...)

reference rows 39, this run 39, common 39
| Probe | ref cycles | ref ms | ref verdict | ref pass cycles | ref accesses | cycles | ms | verdict | pass cycles | accesses | d ms | d accesses |
|---|---:|---:|---|---:|---:|---:|---:|---|---:|---:|---:|---:|
| aecp.entity_available.if0 | 249,962 | 4.999 | fits | 360,902 | 51 | 244,005 | 4.880 | fits | 360,662 | 53 | -0.119 | +2 |
| aecp.entity_available.if1 | 288,329 | 5.767 | fits | 397,872 | 56 | 245,193 | 4.904 | fits | 360,465 | 51 | -0.863 | -5 |
| aecp.get_avb_info.if0 | 295,784 | 5.916 | fits | 370,724 | 48 | 347,065 | 6.941 | fits | 370,067 | 49 | +1.025 | +1 |
| aecp.get_avb_info.if1 | 260,573 | 5.211 | fits | 370,125 | 45 | 292,029 | 5.841 | fits | 369,870 | 47 | +0.630 | +2 |
| aecp.get_configuration.if0 | 741,103 | 14.822 | MISS T_svc | 429,227 | 60 | 383,739 | 7.675 | fits | 430,173 | 62 | -7.147 | +2 |
| aecp.get_configuration.if1 | 284,520 | 5.690 | fits | 357,532 | 46 | 279,241 | 5.585 | fits | 357,277 | 48 | -0.105 | +2 |
| aecp.get_counters.if0 | 328,487 | 6.570 | fits | 383,452 | 80 | 324,347 | 6.487 | fits | 384,302 | 87 | -0.083 | +7 |
| aecp.get_counters.if1 | 310,723 | 6.214 | fits | 420,382 | 85 | 269,059 | 5.381 | fits | 384,105 | 85 | -0.833 | +0 |
| aecp.get_name.if0 | 352,412 | 7.048 | fits | 463,357 | 99 | 291,032 | 5.821 | fits | 407,753 | 73 | -1.227 | -26 |
| aecp.get_name.if1 | 260,314 | 5.206 | fits | 370,756 | 62 | 293,023 | 5.860 | fits | 370,896 | 65 | +0.654 | +3 |
| aecp.lock_entity.if0 | 415,903 | 8.318 | fits | 414,858 | 73 | 278,633 | 5.573 | fits | 411,905 | 90 | -2.745 | +17 |
| aecp.lock_entity.if1 | 409,460 | 8.189 | fits | 428,393 | 92 | 438,952 | 8.779 | fits | 463,489 | 116 | +0.590 | +24 |
| aecp.mvu_get_milan_info.if0 | 175,890 | 3.518 | fits | 287,415 | 52 | 170,304 | 3.406 | fits | 287,120 | 54 | -0.112 | +2 |
| aecp.mvu_get_milan_info.if1 | 176,594 | 3.532 | fits | 286,816 | 49 | 171,752 | 3.435 | fits | 286,923 | 52 | -0.097 | +3 |
| aecp.read_descriptor.t0.i0.c0.if0 | 308,462 | 6.169 | fits | 419,415 | 125 | 302,859 | 6.057 | fits | 419,161 | 127 | -0.112 | +2 |
| aecp.read_descriptor.t0.i0.c0.if1 | 309,523 | 6.190 | fits | 419,147 | 123 | 302,964 | 6.059 | fits | 418,892 | 125 | -0.131 | +2 |
| aecp.read_descriptor.t1.i0.c0.if0 | 304,685 | 6.094 | fits | 415,178 | 80 | 299,216 | 5.984 | fits | 415,252 | 82 | -0.110 | +2 |
| aecp.read_descriptor.t1.i0.c0.if1 | 305,789 | 6.116 | fits | 415,313 | 78 | 300,162 | 6.003 | fits | 415,780 | 80 | -0.113 | +2 |
| aecp.read_descriptor.t10.i9.c0.if0 | 303,905 | 6.078 | fits | 378,116 | 69 | 298,272 | 5.965 | fits | 414,502 | 77 | -0.113 | +8 |
| aecp.read_descriptor.t12.i0.c0.if0 | 264,885 | 5.298 | fits | 375,226 | 65 | 259,120 | 5.182 | fits | 374,964 | 67 | -0.116 | +2 |
| aecp.read_descriptor.t13.i0.c0.if0 | 374,850 | 7.497 | fits | 448,860 | 160 | 367,799 | 7.356 | fits | 448,993 | 163 | -0.141 | +3 |
| aecp.read_descriptor.t14.i7.c0.if0 | 288,349 | 5.767 | fits | 401,741 | 59 | 283,654 | 5.673 | fits | 402,268 | 61 | -0.094 | +2 |
| aecp.read_descriptor.t15.i7.c0.if0 | 254,607 | 5.092 | fits | 366,939 | 52 | 248,871 | 4.977 | fits | 366,677 | 54 | -0.115 | +2 |
| aecp.read_descriptor.t2.i0.c0.if0 | 310,358 | 6.207 | fits | 420,854 | 121 | 305,599 | 6.112 | fits | 421,369 | 123 | -0.095 | +2 |
| aecp.read_descriptor.t2.i0.c0.if1 | 276,870 | 5.537 | fits | 386,540 | 82 | 270,996 | 5.420 | fits | 386,285 | 84 | -0.117 | +2 |
| aecp.read_descriptor.t20.i71.c0.if0 | 311,494 | 6.230 | fits | 388,308 | 70 | 306,391 | 6.128 | fits | 424,042 | 78 | -0.102 | +8 |
| aecp.read_descriptor.t26.i0.c0.if0 | 279,743 | 5.595 | fits | 392,458 | 75 | 274,736 | 5.495 | fits | 392,196 | 77 | -0.100 | +2 |
| aecp.read_descriptor.t36.i0.c0.if0 | 313,215 | 6.264 | fits | 389,334 | 71 | 308,080 | 6.162 | fits | 389,467 | 74 | -0.102 | +3 |
| aecp.read_descriptor.t5.i8.c0.if0 | 347,097 | 6.942 | fits | 387,250 | 83 | 343,524 | 6.870 | fits | 387,383 | 86 | -0.072 | +3 |
| aecp.read_descriptor.t6.i8.c0.if0 | 314,051 | 6.281 | fits | 424,778 | 90 | 309,656 | 6.193 | fits | 425,483 | 92 | -0.088 | +2 |
| aecp.read_descriptor.t9.i0.c0.if0 | 269,182 | 5.384 | fits | 379,768 | 72 | 263,625 | 5.272 | fits | 379,506 | 74 | -0.112 | +2 |
| aecp.register_unsolicited.if0 | 295,637 | 5.913 | fits | 322,322 | 54 | 305,794 | 6.116 | fits | 322,664 | 56 | +0.203 | +2 |
| aecp.register_unsolicited.if1 | 243,277 | 4.866 | fits | 322,957 | 52 | 238,167 | 4.763 | fits | 323,151 | 54 | -0.103 | +2 |
| aecp.set_name.if0 | 373,683 | 7.474 | fits | 574,214 | 114 | 399,996 | 8.000 | fits | 636,986 | 156 | +0.526 | +42 |
| aecp.set_name.if1 | 376,217 | 7.524 | fits | 578,124 | 147 | 372,189 | 7.444 | fits | 579,520 | 149 | -0.080 | +2 |
| aecp.unknown_command.if0 | 282,639 | 5.653 | fits | 393,659 | 54 | 276,851 | 5.537 | fits | 393,658 | 56 | -0.116 | +2 |
| aecp.unknown_command.if1 | 284,265 | 5.685 | fits | 394,012 | 52 | 279,221 | 5.584 | fits | 394,512 | 54 | -0.101 | +2 |
| aecp.unlock_entity.if0 | 280,323 | 5.606 | fits | 377,791 | 66 | 346,221 | 6.924 | fits | 411,882 | 90 | +1.318 | +24 |
| aecp.unlock_entity.if1 | 305,942 | 6.119 | fits | 390,914 | 85 | 335,233 | 6.705 | fits | 425,006 | 109 | +0.586 | +24 |
