# #818's floor (WNS >= +0.030 ns setup, WHS >= 0 ns hold, every signoff corner) on the best of the recipe's three directives, the PR's own images (the gating recipe at 822e3af0, its inputs equal to 62477be4's), 16 threads, signoff.py
| Point | Directive | Slow_85C WNS/WHS | Slow_0C WNS/WHS | Fast_85C WNS/WHS | Fast_0C WNS/WHS | Floor | bitstream sha256 |
|---|---|---|---|---|---|---|---|
| 1x1/1if | ExtraPostPlacementOpt | +0.131/+0.102 | +0.131/+0.102 | +1.636/+0.036 | +1.636/+0.036 | met | `68e5308bf397df08` |
| 1x1/1if | ExtraTimingOpt | +0.002/+0.102 | +0.002/+0.102 | +1.660/+0.036 | +1.660/+0.036 | NOT met (setup) | `e52210f3d3bc6b64` |
| 1x1/1if | AltSpreadLogic_high | +0.046/+0.102 | +0.046/+0.102 | +1.660/+0.036 | +1.660/+0.036 | met | `b35c3fe916065d01` |
| 8x8/1if | ExtraPostPlacementOpt | +0.176/+0.102 | +0.176/+0.102 | +1.523/+0.036 | +1.523/+0.036 | met | `6a1ff1efca0a6474` |
| 8x8/1if | ExtraTimingOpt | +0.059/+0.102 | +0.059/+0.102 | +1.660/+0.036 | +1.660/+0.036 | met | `238b162ed4c71a66` |
| 8x8/1if | AltSpreadLogic_high | +0.150/+0.102 | +0.150/+0.102 | +1.660/+0.036 | +1.660/+0.036 | met | `03a6f3b12e80394b` |

Best of three: 1x1/1if ExtraPostPlacementOpt (+0.131 ns setup, +0.036 ns hold worst), 8x8/1if ExtraPostPlacementOpt (+0.176, +0.036): the floor is met at every corner at both points. 1x1/1if ExtraTimingOpt alone reads +0.002 ns setup at the slow corners, 0.028 ns under the floor; the floor is graded on the best of the three.
