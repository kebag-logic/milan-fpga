# aecp group, arm A, 8x8: this lane's cacheless run (665s1-a680j, at 0eda061a, before the merge) beside this head's split-cache run

reference: 665s1-a680j/receipts/runs/A8/results/table.md (sha256 c77c89dcfdb58bde...)
this run: runs/A8/results/table.md (sha256 7761689016e3d57d...)

reference rows 39, this run 39, common 39
| Probe | ref cycles | ref ms | ref verdict | ref pass cycles | ref accesses | cycles | ms | verdict | pass cycles | accesses | d ms | d accesses |
|---|---:|---:|---|---:|---:|---:|---:|---|---:|---:|---:|---:|
| aecp.entity_available.if0 | 244,005 | 4.880 | fits | 360,662 | 53 | 124,767 | 2.495 | fits | 206,667 | 53 | -2.385 | +0 |
| aecp.entity_available.if1 | 245,193 | 4.904 | fits | 360,465 | 51 | 146,224 | 2.924 | fits | 228,169 | 58 | -1.980 | +7 |
| aecp.get_avb_info.if0 | 347,065 | 6.941 | fits | 370,067 | 49 | 209,250 | 4.185 | fits | 213,079 | 50 | -2.756 | +1 |
| aecp.get_avb_info.if1 | 292,029 | 5.841 | fits | 369,870 | 47 | 152,215 | 3.044 | fits | 234,160 | 54 | -2.797 | +7 |
| aecp.get_configuration.if0 | 383,739 | 7.675 | fits | 430,173 | 62 | 144,857 | 2.897 | fits | 226,765 | 56 | -4.778 | -6 |
| aecp.get_configuration.if1 | 279,241 | 5.585 | fits | 357,277 | 48 | 122,723 | 2.454 | fits | 204,657 | 47 | -3.131 | -1 |
| aecp.get_counters.if0 | 324,347 | 6.487 | fits | 384,302 | 87 | 159,719 | 3.194 | fits | 241,644 | 94 | -3.293 | +7 |
| aecp.get_counters.if1 | 269,059 | 5.381 | fits | 384,105 | 85 | 138,200 | 2.764 | fits | 220,148 | 85 | -2.617 | +0 |
| aecp.get_name.if0 | 291,032 | 5.821 | fits | 407,753 | 73 | 130,764 | 2.615 | fits | 212,664 | 66 | -3.206 | -7 |
| aecp.get_name.if1 | 293,023 | 5.860 | fits | 370,896 | 65 | 130,553 | 2.611 | fits | 212,487 | 64 | -3.249 | -1 |
| aecp.lock_entity.if0 | 278,633 | 5.573 | fits | 411,905 | 90 | 167,747 | 3.355 | fits | 261,010 | 97 | -2.218 | +7 |
| aecp.lock_entity.if1 | 438,952 | 8.779 | fits | 463,489 | 116 | 167,740 | 3.355 | fits | 268,831 | 116 | -5.424 | +0 |
| aecp.mvu_get_milan_info.if0 | 170,304 | 3.406 | fits | 287,120 | 54 | 110,174 | 2.203 | fits | 192,085 | 60 | -1.203 | +6 |
| aecp.mvu_get_milan_info.if1 | 171,752 | 3.435 | fits | 286,923 | 52 | 110,082 | 2.202 | fits | 192,027 | 58 | -1.233 | +6 |
| aecp.read_descriptor.t0.i0.c0.if0 | 302,859 | 6.057 | fits | 419,161 | 127 | 179,754 | 3.595 | fits | 261,679 | 134 | -2.462 | +7 |
| aecp.read_descriptor.t0.i0.c0.if1 | 302,964 | 6.059 | fits | 418,892 | 125 | 179,413 | 3.588 | fits | 261,357 | 132 | -2.471 | +7 |
| aecp.read_descriptor.t1.i0.c0.if0 | 299,216 | 5.984 | fits | 415,252 | 82 | 134,794 | 2.696 | fits | 216,705 | 75 | -3.288 | -7 |
| aecp.read_descriptor.t1.i0.c0.if1 | 300,162 | 6.003 | fits | 415,780 | 80 | 134,586 | 2.692 | fits | 216,519 | 73 | -3.311 | -7 |
| aecp.read_descriptor.t10.i9.c0.if0 | 298,272 | 5.965 | fits | 414,502 | 77 | 134,626 | 2.693 | fits | 216,540 | 70 | -3.272 | -7 |
| aecp.read_descriptor.t12.i0.c0.if0 | 259,120 | 5.182 | fits | 374,964 | 67 | 155,014 | 3.100 | fits | 236,936 | 74 | -2.082 | +7 |
| aecp.read_descriptor.t13.i0.c0.if0 | 367,799 | 7.356 | fits | 448,993 | 163 | 174,271 | 3.485 | fits | 256,182 | 162 | -3.871 | -1 |
| aecp.read_descriptor.t14.i7.c0.if0 | 283,654 | 5.673 | fits | 402,268 | 61 | 128,190 | 2.564 | fits | 210,101 | 54 | -3.109 | -7 |
| aecp.read_descriptor.t15.i7.c0.if0 | 248,871 | 4.977 | fits | 366,677 | 54 | 128,705 | 2.574 | fits | 210,616 | 54 | -2.403 | +0 |
| aecp.read_descriptor.t2.i0.c0.if0 | 305,599 | 6.112 | fits | 421,369 | 123 | 161,256 | 3.225 | fits | 243,178 | 93 | -2.887 | -30 |
| aecp.read_descriptor.t2.i0.c0.if1 | 270,996 | 5.420 | fits | 386,285 | 84 | 139,247 | 2.785 | fits | 221,180 | 84 | -2.635 | +0 |
| aecp.read_descriptor.t20.i71.c0.if0 | 306,391 | 6.128 | fits | 424,042 | 78 | 163,202 | 3.264 | fits | 245,124 | 78 | -2.864 | +0 |
| aecp.read_descriptor.t26.i0.c0.if0 | 274,736 | 5.495 | fits | 392,196 | 77 | 143,323 | 2.866 | fits | 225,234 | 77 | -2.629 | +0 |
| aecp.read_descriptor.t36.i0.c0.if0 | 308,080 | 6.162 | fits | 389,467 | 74 | 141,586 | 2.832 | fits | 223,497 | 73 | -3.330 | -1 |
| aecp.read_descriptor.t5.i8.c0.if0 | 343,524 | 6.870 | fits | 387,383 | 86 | 139,817 | 2.796 | fits | 221,731 | 85 | -4.074 | -1 |
| aecp.read_descriptor.t6.i8.c0.if0 | 309,656 | 6.193 | fits | 425,483 | 92 | 140,393 | 2.808 | fits | 222,307 | 85 | -3.385 | -7 |
| aecp.read_descriptor.t9.i0.c0.if0 | 263,625 | 5.272 | fits | 379,506 | 74 | 135,633 | 2.713 | fits | 217,547 | 74 | -2.559 | +0 |
| aecp.register_unsolicited.if0 | 305,794 | 6.116 | fits | 322,664 | 56 | 88,583 | 1.772 | fits | 170,082 | 50 | -4.344 | -6 |
| aecp.register_unsolicited.if1 | 238,167 | 4.763 | fits | 323,151 | 54 | 88,128 | 1.763 | fits | 170,017 | 47 | -3.000 | -7 |
| aecp.set_name.if0 | 399,996 | 8.000 | fits | 636,986 | 156 | 216,570 | 4.331 | fits | 367,213 | 156 | -3.669 | +0 |
| aecp.set_name.if1 | 372,189 | 7.444 | fits | 579,520 | 149 | 197,953 | 3.959 | fits | 332,727 | 149 | -3.485 | +0 |
| aecp.unknown_command.if0 | 276,851 | 5.537 | fits | 393,658 | 56 | 122,557 | 2.451 | fits | 204,457 | 49 | -3.086 | -7 |
| aecp.unknown_command.if1 | 279,221 | 5.584 | fits | 394,512 | 54 | 122,346 | 2.447 | fits | 204,280 | 47 | -3.137 | -7 |
| aecp.unlock_entity.if0 | 346,221 | 6.924 | fits | 411,882 | 90 | 145,943 | 2.919 | fits | 239,157 | 90 | -4.005 | +0 |
| aecp.unlock_entity.if1 | 335,233 | 6.705 | fits | 425,006 | 109 | 167,944 | 3.359 | fits | 268,826 | 116 | -3.346 | +7 |
