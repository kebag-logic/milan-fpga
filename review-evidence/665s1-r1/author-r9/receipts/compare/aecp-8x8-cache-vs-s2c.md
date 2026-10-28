# aecp group, arm A, 8x8, split cache: S2c's run (PR #796, firmware e76a755a) beside this head

reference: 665s2c-a685/receipts/runs/P8-64x1/table.md (sha256 ad8e03df960f69ea...)
this run: runs/A8/results/table.md (sha256 7761689016e3d57d...)

reference rows 39, this run 39, common 39
| Probe | ref cycles | ref ms | ref verdict | ref pass cycles | ref accesses | cycles | ms | verdict | pass cycles | accesses | d ms | d accesses |
|---|---:|---:|---|---:|---:|---:|---:|---|---:|---:|---:|---:|
| aecp.entity_available.if0 | 146,256 | 2.925 | fits | 227,538 | 58 | 124,767 | 2.495 | fits | 206,667 | 53 | -0.430 | -5 |
| aecp.entity_available.if1 | 146,102 | 2.922 | fits | 227,414 | 56 | 146,224 | 2.924 | fits | 228,169 | 58 | +0.002 | +2 |
| aecp.get_avb_info.if0 | 131,126 | 2.623 | fits | 212,378 | 47 | 209,250 | 4.185 | fits | 213,079 | 50 | +1.562 | +3 |
| aecp.get_avb_info.if1 | 130,919 | 2.618 | fits | 212,201 | 45 | 152,215 | 3.044 | fits | 234,160 | 54 | +0.426 | +9 |
| aecp.get_configuration.if0 | 123,040 | 2.461 | fits | 204,289 | 47 | 144,857 | 2.897 | fits | 226,765 | 56 | +0.436 | +9 |
| aecp.get_configuration.if1 | 122,833 | 2.457 | fits | 204,115 | 45 | 122,723 | 2.454 | fits | 204,657 | 47 | -0.003 | +2 |
| aecp.get_counters.if0 | 159,225 | 3.184 | fits | 240,507 | 87 | 159,719 | 3.194 | fits | 241,644 | 94 | +0.010 | +7 |
| aecp.get_counters.if1 | 137,419 | 2.748 | fits | 218,731 | 78 | 138,200 | 2.764 | fits | 220,148 | 85 | +0.016 | +7 |
| aecp.get_name.if0 | 130,882 | 2.618 | fits | 212,134 | 64 | 130,764 | 2.615 | fits | 212,664 | 66 | -0.003 | +2 |
| aecp.get_name.if1 | 220,615 | 4.412 | fits | 212,215 | 63 | 130,553 | 2.611 | fits | 212,487 | 64 | -1.801 | +1 |
| aecp.lock_entity.if0 | 145,009 | 2.900 | fits | 239,004 | 73 | 167,747 | 3.355 | fits | 261,010 | 97 | +0.455 | +24 |
| aecp.lock_entity.if1 | 123,704 | 2.474 | fits | 226,792 | 85 | 167,740 | 3.355 | fits | 268,831 | 116 | +0.881 | +31 |
| aecp.mvu_get_milan_info.if0 | 139,672 | 2.793 | fits | 631,635 | 274 | 110,174 | 2.203 | fits | 192,085 | 60 | -0.590 | -214 |
| aecp.mvu_get_milan_info.if1 | 110,432 | 2.209 | fits | 191,692 | 56 | 110,082 | 2.202 | fits | 192,027 | 58 | -0.007 | +2 |
| aecp.read_descriptor.t0.i0.c0.if0 | 179,650 | 3.593 | fits | 260,932 | 132 | 179,754 | 3.595 | fits | 261,679 | 134 | +0.002 | +2 |
| aecp.read_descriptor.t0.i0.c0.if1 | 179,281 | 3.586 | fits | 260,595 | 130 | 179,413 | 3.588 | fits | 261,357 | 132 | +0.002 | +2 |
| aecp.read_descriptor.t1.i0.c0.if0 | 156,513 | 3.130 | fits | 237,792 | 80 | 134,794 | 2.696 | fits | 216,705 | 75 | -0.434 | -5 |
| aecp.read_descriptor.t1.i0.c0.if1 | 134,863 | 2.697 | fits | 216,147 | 71 | 134,586 | 2.692 | fits | 216,519 | 73 | -0.005 | +2 |
| aecp.read_descriptor.t10.i9.c0.if0 | 134,891 | 2.698 | fits | 216,143 | 68 | 134,626 | 2.693 | fits | 216,540 | 70 | -0.005 | +2 |
| aecp.read_descriptor.t12.i0.c0.if0 | 154,887 | 3.098 | fits | 236,166 | 72 | 155,014 | 3.100 | fits | 236,936 | 74 | +0.002 | +2 |
| aecp.read_descriptor.t13.i0.c0.if0 | 174,536 | 3.491 | fits | 255,785 | 160 | 174,271 | 3.485 | fits | 256,182 | 162 | -0.006 | +2 |
| aecp.read_descriptor.t14.i7.c0.if0 | 128,455 | 2.569 | fits | 209,704 | 52 | 128,190 | 2.564 | fits | 210,101 | 54 | -0.005 | +2 |
| aecp.read_descriptor.t15.i7.c0.if0 | 150,495 | 3.010 | fits | 231,774 | 59 | 128,705 | 2.574 | fits | 210,616 | 54 | -0.436 | -5 |
| aecp.read_descriptor.t2.i0.c0.if0 | 139,720 | 2.794 | fits | 220,969 | 84 | 161,256 | 3.225 | fits | 243,178 | 93 | +0.431 | +9 |
| aecp.read_descriptor.t2.i0.c0.if1 | 160,939 | 3.219 | fits | 242,253 | 89 | 139,247 | 2.785 | fits | 221,180 | 84 | -0.434 | -5 |
| aecp.read_descriptor.t20.i71.c0.if0 | 141,641 | 2.833 | fits | 222,890 | 69 | 163,202 | 3.264 | fits | 245,124 | 78 | +0.431 | +9 |
| aecp.read_descriptor.t26.i0.c0.if0 | 165,116 | 3.302 | fits | 246,395 | 82 | 143,323 | 2.866 | fits | 225,234 | 77 | -0.436 | -5 |
| aecp.read_descriptor.t36.i0.c0.if0 | 141,851 | 2.837 | fits | 223,100 | 71 | 141,586 | 2.832 | fits | 223,497 | 73 | -0.005 | +2 |
| aecp.read_descriptor.t5.i8.c0.if0 | 140,082 | 2.802 | fits | 221,334 | 83 | 139,817 | 2.796 | fits | 221,731 | 85 | -0.006 | +2 |
| aecp.read_descriptor.t6.i8.c0.if0 | 162,183 | 3.244 | fits | 243,465 | 90 | 140,393 | 2.808 | fits | 222,307 | 85 | -0.436 | -5 |
| aecp.read_descriptor.t9.i0.c0.if0 | 201,380 | 4.028 | fits | 217,408 | 73 | 135,633 | 2.713 | fits | 217,547 | 74 | -1.315 | +1 |
| aecp.register_unsolicited.if0 | 88,387 | 1.768 | fits | 169,183 | 48 | 88,583 | 1.772 | fits | 170,082 | 50 | +0.004 | +2 |
| aecp.register_unsolicited.if1 | 87,926 | 1.759 | fits | 169,128 | 45 | 88,128 | 1.763 | fits | 170,017 | 47 | +0.004 | +2 |
| aecp.set_name.if0 | 214,401 | 4.288 | fits | 307,441 | 108 | 216,570 | 4.331 | fits | 367,213 | 156 | +0.043 | +48 |
| aecp.set_name.if1 | 197,297 | 3.946 | fits | 334,076 | 147 | 197,953 | 3.959 | fits | 332,727 | 149 | +0.013 | +2 |
| aecp.unknown_command.if0 | 143,882 | 2.878 | fits | 225,164 | 54 | 122,557 | 2.451 | fits | 204,457 | 49 | -0.427 | -5 |
| aecp.unknown_command.if1 | 144,128 | 2.883 | fits | 225,440 | 52 | 122,346 | 2.447 | fits | 204,280 | 47 | -0.436 | -5 |
| aecp.unlock_entity.if0 | 145,033 | 2.901 | fits | 238,977 | 73 | 145,943 | 2.919 | fits | 239,157 | 90 | +0.018 | +17 |
| aecp.unlock_entity.if1 | 123,684 | 2.474 | fits | 226,707 | 85 | 167,944 | 3.359 | fits | 268,826 | 116 | +0.885 | +31 |
