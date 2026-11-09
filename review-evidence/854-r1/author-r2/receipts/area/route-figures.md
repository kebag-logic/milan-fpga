# Route set at the merge commit, post-route figures per directive

| Directive | LUT | FF | Slice | Free | RAMB36 / RAMB18 | DSP | Slow_0C WNS / WHS | Slow_85C | Fast_0C | Fast_85C | Routing errors |
|---|---:|---:|---:|---:|---|---:|---|---|---|---|---:|
| ExtraPostPlacementOpt | 53534 | 54850 | 15820 | 30 | 74 / 27 | 15 | 0.166 / 0.050 | 0.166 / 0.050 | 1.633 / 0.032 | 1.633 / 0.032 | 0 |
| AltSpreadLogic_high | 53513 | 54847 | 15846 | 4 | 74 / 27 | 15 | 0.147 / 0.102 | 0.147 / 0.102 | 1.525 / 0.036 | 1.525 / 0.036 | 0 |
| ExtraTimingOpt | 53512 | 54847 | 15846 | 4 | 74 / 27 | 15 | 0.127 / 0.102 | 0.127 / 0.102 | 1.525 / 0.036 | 1.525 / 0.036 | 0 |

Reports read (not copied):

- `ExtraPostPlacementOpt/baseline_utilization.rpt`: sha256 `0dc66d791e300d69781baff047e7ffbfe663e39f4dbca38135f386c26e6123e9`, 13365 bytes
- `ExtraPostPlacementOpt/alinx_ax7101_route_status.rpt`: sha256 `f3034a5c052c7f770508daa35ffe43629dde34652b0971316ab9251dc5173966`, 651 bytes
- `ExtraPostPlacementOpt/alinx_ax7101_signoff_Fast_0C_timing.rpt`: sha256 `7c4701ec243360de4283b8343579787744d0ac578607da67680d2d0eca94a7c5`, 1316604 bytes
- `ExtraPostPlacementOpt/alinx_ax7101_signoff_Fast_85C_timing.rpt`: sha256 `76c411934d9ab0485d9c0253a7a8ac91b77bc6f78c92b3c6a8a26683f5774206`, 1316605 bytes
- `ExtraPostPlacementOpt/alinx_ax7101_signoff_Slow_0C_timing.rpt`: sha256 `78766895aedfab8fa22c7ed1bdddbcf812b106f09e5749177dfe61b02935ce02`, 1356618 bytes
- `ExtraPostPlacementOpt/alinx_ax7101_signoff_Slow_85C_timing.rpt`: sha256 `a84d811423cb4636eb53f7acb58132f9fdb8dea282a4893e940f8cb16b5d5565`, 1356619 bytes
- `ExtraPostPlacementOpt/alinx_ax7101_signoff_all_timing.rpt`: sha256 `d8f1aea85f25208f116d11a7e80c0272fca748d37510c5b360f8433828e60826`, 1359987 bytes
- `ExtraPostPlacementOpt/alinx_ax7101_signoff_check_timing.rpt`: sha256 `f37a10cfa21f5a197cbb4e5b6dae61e4cea50cd78eadb11b912d28370f70be4f`, 4828 bytes
- `AltSpreadLogic_high/baseline_utilization.rpt`: sha256 `4c9eadd8359c1fe60f77fd9895c44e25fb638d39d0bb59632607a8bf152d3d76`, 13365 bytes
- `AltSpreadLogic_high/alinx_ax7101_route_status.rpt`: sha256 `21d10db021ea184041053d280e61fe1e45a2835d855e30ce8141b8a4318e7b9d`, 651 bytes
- `AltSpreadLogic_high/alinx_ax7101_signoff_Fast_0C_timing.rpt`: sha256 `840f88218104dc1bc9d50b3ed2fe24184e9dc864466973822a09403061d01f7f`, 1303424 bytes
- `AltSpreadLogic_high/alinx_ax7101_signoff_Fast_85C_timing.rpt`: sha256 `42c6988d641aaf865fee06b86f7be2fb43764f63416111b8d60379dd1c0806c6`, 1303425 bytes
- `AltSpreadLogic_high/alinx_ax7101_signoff_Slow_0C_timing.rpt`: sha256 `9dfe7c53c41991e9200c99340ffe15bca098b6aff6a604168de6b48a1bcd5cb0`, 1353230 bytes
- `AltSpreadLogic_high/alinx_ax7101_signoff_Slow_85C_timing.rpt`: sha256 `a4379a01f85c2f7add6a022e7c0eee6a872707b1ad8ffed27eaa0af01d137dc3`, 1353231 bytes
- `AltSpreadLogic_high/alinx_ax7101_signoff_all_timing.rpt`: sha256 `51603531ff591a235daca795c465a37587be6fa1c7b165c7a9c877ec66eb85f3`, 1354776 bytes
- `AltSpreadLogic_high/alinx_ax7101_signoff_check_timing.rpt`: sha256 `d97894f73b0c65adc9516bafa0678a8386feefd97e04f706b30e580a4dad8d05`, 4828 bytes
- `ExtraTimingOpt/baseline_utilization.rpt`: sha256 `b063d9eca24da6e51061e7d7a78bb97222c693b1f80a20af2f11e89c1613c9db`, 13365 bytes
- `ExtraTimingOpt/alinx_ax7101_route_status.rpt`: sha256 `6b28d36797ee7ec9485c418d82fbf085d0ed7b6c963213ccad0ce7a69fdea866`, 651 bytes
- `ExtraTimingOpt/alinx_ax7101_signoff_Fast_0C_timing.rpt`: sha256 `1b3833260a894118a28b96aa4790a5d17f088844fb2593f60529b0be54a58ce1`, 1313006 bytes
- `ExtraTimingOpt/alinx_ax7101_signoff_Fast_85C_timing.rpt`: sha256 `5d8a1564804467b6644f12c9317836928831384231d82f07d4c6736988cfeef4`, 1313007 bytes
- `ExtraTimingOpt/alinx_ax7101_signoff_Slow_0C_timing.rpt`: sha256 `b24531eb8729273e7a401394f11c17abd52fec8e4117e81f0a4f5285309fcfcc`, 1368678 bytes
- `ExtraTimingOpt/alinx_ax7101_signoff_Slow_85C_timing.rpt`: sha256 `99beefc8fdb4529213c36e94ed4be22cb3647ec3568a299ad124014782800803`, 1368679 bytes
- `ExtraTimingOpt/alinx_ax7101_signoff_all_timing.rpt`: sha256 `9226ea1234e7a2291c8aa1aeec86f5ea2d4ee64ee088db53ef6792b9beda9a50`, 1370176 bytes
- `ExtraTimingOpt/alinx_ax7101_signoff_check_timing.rpt`: sha256 `66fa833fc8c0c549daadfd8298b12844193725c52520e0d49287466e15614843`, 4828 bytes
