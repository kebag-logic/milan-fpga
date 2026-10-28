# aecp group, arm A, 1x1, split cache: S2c's run (PR #796, firmware e76a755a) beside this head

reference: 665s2c-a685/receipts/runs/P1-64x1/table.md (sha256 256e2705a68b67b4...)
this run: runs/A1/results/table.md (sha256 0a025d4ce792cb7b...)

reference rows 25, this run 25, common 25
| Probe | ref cycles | ref ms | ref verdict | ref pass cycles | ref accesses | cycles | ms | verdict | pass cycles | accesses | d ms | d accesses |
|---|---:|---:|---|---:|---:|---:|---:|---|---:|---:|---:|---:|
| aecp.entity_available.if0 | 106,118 | 2.122 | fits | 143,920 | 51 | 108,270 | 2.165 | fits | 147,152 | 52 | +0.043 | +1 |
| aecp.get_avb_info.if0 | 107,035 | 2.141 | fits | 144,899 | 46 | 124,962 | 2.499 | fits | 163,844 | 54 | +0.358 | +8 |
| aecp.get_configuration.if0 | 119,071 | 2.381 | fits | 156,994 | 53 | 121,981 | 2.440 | fits | 160,860 | 54 | +0.059 | +1 |
| aecp.get_counters.if0 | 118,050 | 2.361 | fits | 155,852 | 80 | 121,167 | 2.423 | fits | 160,049 | 86 | +0.062 | +6 |
| aecp.get_name.if0 | 112,354 | 2.247 | fits | 150,156 | 64 | 114,449 | 2.289 | fits | 153,331 | 65 | +0.042 | +1 |
| aecp.lock_entity.if0 | 105,274 | 2.105 | fits | 152,840 | 66 | 114,585 | 2.292 | fits | 162,809 | 77 | +0.187 | +11 |
| aecp.mvu_get_milan_info.if0 | 70,264 | 1.405 | fits | 108,066 | 51 | 72,384 | 1.448 | fits | 111,209 | 52 | +0.043 | +1 |
| aecp.read_descriptor.t0.i0.c0.if0 | 139,427 | 2.789 | fits | 177,229 | 125 | 141,675 | 2.833 | fits | 180,557 | 126 | +0.044 | +1 |
| aecp.read_descriptor.t1.i0.c0.if0 | 116,368 | 2.327 | fits | 154,167 | 73 | 118,598 | 2.372 | fits | 157,477 | 74 | +0.045 | +1 |
| aecp.read_descriptor.t10.i2.c0.if0 | 114,786 | 2.296 | fits | 152,588 | 68 | 117,003 | 2.340 | fits | 155,885 | 69 | +0.044 | +1 |
| aecp.read_descriptor.t12.i0.c0.if0 | 113,429 | 2.269 | fits | 151,228 | 65 | 115,607 | 2.312 | fits | 154,486 | 66 | +0.043 | +1 |
| aecp.read_descriptor.t13.i0.c0.if0 | 169,146 | 3.383 | fits | 207,069 | 166 | 172,109 | 3.442 | fits | 210,988 | 167 | +0.059 | +1 |
| aecp.read_descriptor.t14.i0.c0.if0 | 107,902 | 2.158 | fits | 145,701 | 52 | 110,119 | 2.202 | fits | 148,998 | 53 | +0.044 | +1 |
| aecp.read_descriptor.t15.i0.c0.if0 | 107,966 | 2.159 | fits | 145,765 | 52 | 110,183 | 2.204 | fits | 149,062 | 53 | +0.045 | +1 |
| aecp.read_descriptor.t2.i0.c0.if0 | 135,660 | 2.713 | fits | 173,583 | 90 | 138,512 | 2.770 | fits | 177,391 | 91 | +0.057 | +1 |
| aecp.read_descriptor.t20.i24.c0.if0 | 131,841 | 2.637 | fits | 169,764 | 75 | 134,915 | 2.698 | fits | 173,794 | 76 | +0.061 | +1 |
| aecp.read_descriptor.t26.i0.c0.if0 | 119,639 | 2.393 | fits | 157,438 | 75 | 121,856 | 2.437 | fits | 160,735 | 76 | +0.044 | +1 |
| aecp.read_descriptor.t36.i0.c0.if0 | 116,359 | 2.327 | fits | 154,158 | 67 | 118,537 | 2.371 | fits | 157,416 | 68 | +0.044 | +1 |
| aecp.read_descriptor.t5.i1.c0.if0 | 120,873 | 2.417 | fits | 158,675 | 83 | 123,090 | 2.462 | fits | 161,972 | 84 | +0.045 | +1 |
| aecp.read_descriptor.t6.i1.c0.if0 | 121,040 | 2.421 | fits | 158,842 | 83 | 123,218 | 2.464 | fits | 162,100 | 84 | +0.043 | +1 |
| aecp.read_descriptor.t9.i0.c0.if0 | 130,996 | 2.620 | fits | 168,922 | 78 | 133,925 | 2.679 | fits | 172,807 | 79 | +0.059 | +1 |
| aecp.register_unsolicited.if0 | 83,954 | 1.679 | fits | 121,496 | 53 | 87,061 | 1.741 | fits | 125,616 | 54 | +0.062 | +1 |
| aecp.set_name.if0 | 131,823 | 2.636 | fits | 196,056 | 106 | 139,949 | 2.799 | fits | 209,113 | 127 | +0.163 | +21 |
| aecp.unknown_command.if0 | 104,123 | 2.082 | fits | 141,925 | 47 | 106,236 | 2.125 | fits | 145,118 | 48 | +0.043 | +1 |
| aecp.unlock_entity.if0 | 105,305 | 2.106 | fits | 152,851 | 66 | 114,830 | 2.297 | fits | 162,929 | 78 | +0.191 | +12 |
