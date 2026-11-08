# Route set at the merge commit, post-route figures per directive

| Directive | LUT | FF | Slice | Free | RAMB36 / RAMB18 | DSP | Slow_0C WNS / WHS | Slow_85C | Fast_0C | Fast_85C | Routing errors |
|---|---:|---:|---:|---:|---|---:|---|---|---|---|---:|
| ExtraPostPlacementOpt | 53383 | 54837 | 15848 | 2 | 74 / 27 | 15 | 0.112 / 0.063 | 0.112 / 0.063 | 1.465 / 0.036 | 1.465 / 0.036 | 0 |
| AltSpreadLogic_high | 53428 | 54837 | 15829 | 21 | 74 / 27 | 15 | 0.210 / 0.069 | 0.210 / 0.069 | 1.520 / 0.036 | 1.520 / 0.036 | 0 |
| ExtraTimingOpt | 53402 | 54838 | 15829 | 21 | 74 / 27 | 15 | 0.018 / 0.091 | 0.018 / 0.091 | 1.520 / 0.036 | 1.520 / 0.036 | 0 |

Reports read (not copied):

- `ExtraPostPlacementOpt/baseline_utilization.rpt`: sha256 `5abf1768ffb19f50ea33987151bbc44032a38820d2ec2fd64f2163bd203164f5`, 13365 bytes
- `ExtraPostPlacementOpt/alinx_ax7101_route_status.rpt`: sha256 `1ebf28df8180df38671c23fc3fbb5ded2dacb4121931fcaa075ec9b1f05d8807`, 651 bytes
- `ExtraPostPlacementOpt/alinx_ax7101_signoff_Fast_0C_timing.rpt`: sha256 `eff5ed5ceabba64f29dc4cf3e61a0765051c2d0d078554ff97736b3bc5196ad6`, 1274216 bytes
- `ExtraPostPlacementOpt/alinx_ax7101_signoff_Fast_85C_timing.rpt`: sha256 `f3b77a7d1f40510f5edde9e72bdc5cecc8068144d1817e5855166800a208de30`, 1274217 bytes
- `ExtraPostPlacementOpt/alinx_ax7101_signoff_Slow_0C_timing.rpt`: sha256 `010305fbc7d16e94859a786dd7c128385b354970b47332e20ffa51b4984e8258`, 1352881 bytes
- `ExtraPostPlacementOpt/alinx_ax7101_signoff_Slow_85C_timing.rpt`: sha256 `cc7e468cb18019e28458396384d09bac5470ba7139a2ccdbefcb03bf77504ed4`, 1352882 bytes
- `ExtraPostPlacementOpt/alinx_ax7101_signoff_all_timing.rpt`: sha256 `b933907a3d2d5f7fb4e4ddedcaba9265d9d87d94f6499b441fa0a4e141e7bca9`, 1356110 bytes
- `ExtraPostPlacementOpt/alinx_ax7101_signoff_check_timing.rpt`: sha256 `ed0462a13b455420b65cfbe81f60d04cb9eb75ff944ce1a3244cf545cca9ea14`, 4828 bytes
- `AltSpreadLogic_high/baseline_utilization.rpt`: sha256 `9cf94e8fcfa5048c40b8fff27a6a87f0d7c9be2182c06bff8a9ad92c785c99b5`, 13365 bytes
- `AltSpreadLogic_high/alinx_ax7101_route_status.rpt`: sha256 `b4518d254da128413ba44df2f6585c1f7a3c90b7e83f587f5ba9655286aef53d`, 651 bytes
- `AltSpreadLogic_high/alinx_ax7101_signoff_Fast_0C_timing.rpt`: sha256 `1a7160e41ee308c6db98324aa20c555f4d6a90749075b515c71559c6b1c3c5b3`, 1311289 bytes
- `AltSpreadLogic_high/alinx_ax7101_signoff_Fast_85C_timing.rpt`: sha256 `716a54186707badcd325e90fd01c87ac2e9504991eefb04088ed0cabf975f67e`, 1311290 bytes
- `AltSpreadLogic_high/alinx_ax7101_signoff_Slow_0C_timing.rpt`: sha256 `d4f96f7f71721bbb6c878b0cb47be5f0e32fa409dadfedfcee878b562b4b0d88`, 1370348 bytes
- `AltSpreadLogic_high/alinx_ax7101_signoff_Slow_85C_timing.rpt`: sha256 `6607a196e11d44f24e449a64259bfc26376293c4fce773e3dbee8dbb5c9f509e`, 1370349 bytes
- `AltSpreadLogic_high/alinx_ax7101_signoff_all_timing.rpt`: sha256 `bfd0569e0229209fc63033a980353b648532097e6c4a4bb41d96217e1b333359`, 1370890 bytes
- `AltSpreadLogic_high/alinx_ax7101_signoff_check_timing.rpt`: sha256 `ecd3fbe7b84d429e514740b02e29743fcd8e4975b2cb6616470e3c18b84e2280`, 4828 bytes
- `ExtraTimingOpt/baseline_utilization.rpt`: sha256 `fd7624324f8b7efb9e5d67a632d559a100798ea4517aee83db66a74b95832d9e`, 13365 bytes
- `ExtraTimingOpt/alinx_ax7101_route_status.rpt`: sha256 `2efec174cb0ca119449954504854b693304608aec2bb73366d8473ec1d5c01dc`, 651 bytes
- `ExtraTimingOpt/alinx_ax7101_signoff_Fast_0C_timing.rpt`: sha256 `0e834bb24f783f2ed80a5b8a9aa5b2617e817faf98c0f06fca7188955f745687`, 1297075 bytes
- `ExtraTimingOpt/alinx_ax7101_signoff_Fast_85C_timing.rpt`: sha256 `3b2f6b30cb93e139ff43826b0a63571205152c14c5168b649a12e41cb501fbf5`, 1297076 bytes
- `ExtraTimingOpt/alinx_ax7101_signoff_Slow_0C_timing.rpt`: sha256 `3db35998c3f1935ce1ca12e84dfcd084f9f8b921ad1f6df8049a6c24f236b651`, 1348785 bytes
- `ExtraTimingOpt/alinx_ax7101_signoff_Slow_85C_timing.rpt`: sha256 `3e5336bfea35ced0f0e5881d3e1059c815f6974697de63ff91391885e3784267`, 1348786 bytes
- `ExtraTimingOpt/alinx_ax7101_signoff_all_timing.rpt`: sha256 `96efc9c8b82e4e4ee05525f557306886ac6dedb709ee5bcf8fc651dbd88a8bd7`, 1348853 bytes
- `ExtraTimingOpt/alinx_ax7101_signoff_check_timing.rpt`: sha256 `1c308ae47cd94cedc54390a986efc1e046b8d900b424fcc2168c7fc8b5f67c09`, 4828 bytes
