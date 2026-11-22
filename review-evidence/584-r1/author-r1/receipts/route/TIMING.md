# #818's floor (WNS >= +0.030 ns setup, WHS >= 0 ns hold, every signoff corner) on the recipe's three placement directives, the 8x8/1if split image of 92fd1635 (inputs equal to the head's: artifacts-routed-vs-head.txt), 16 threads, signoff.py

| Directive | Slow_85C WNS/WHS | Slow_0C | Fast_85C | Fast_0C | Floor | LUT | FF | BRAM tiles | Slices | flip image LUT / BRAM |
|---|---|---|---|---|---|---:|---:|---:|---:|---|
| ExtraPostPlacementOpt | +0.123/+0.102 | +0.123/+0.102 | +1.636/+0.015 | +1.636/+0.015 | met | 44610 | 53065 | 99 | 15667 | 42985 / 94.5 |
| AltSpreadLogic_high | +0.363/+0.102 | +0.363/+0.102 | +1.636/+0.036 | +1.636/+0.036 | met | 44191 | 53066 | 99 | 15668 | 43102 / 94.5 |
| ExtraTimingOpt | +0.207/+0.102 | +0.207/+0.102 | +1.636/+0.036 | +1.636/+0.036 | met | 44224 | 53066 | 99 | 15694 | 43096 / 94.5 |

Best of three: AltSpreadLogic_high (+0.363 ns setup, +0.036 ns hold at the worst corner). The floor is met at every corner on all three directives.
The flip image columns are the bench-gated 8x8/1if image's routes on the same directives (PR #960's head), for the growth: the render crossbar, the render queue and the render master that the first TDM render channel brings into the 8x8.
