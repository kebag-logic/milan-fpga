# Every route recorded in rounds 1 and 2, regraded against #818's floor (+0.030 ns setup and 0 ns hold at every signoff corner, on the best of the recipe's three directives; #665 issuecomment-6930885185). Worst slack over the four corners each route's signoff.txt records.
command: floor818.py round1/receipts/route round2/receipts/route

| Round | Image | Directive | Worst setup, ns | Worst hold, ns | Meets #818 |
|---|---|---|---:|---:|---|
| round1 | split1 | ExtraPostPlacementOpt | +0.128 | +0.036 | meets |
| round1 | split1 | ExtraTimingOpt | +0.067 | +0.036 | meets |
| round1 | split1 | AltSpreadLogic_high | +0.399 | +0.036 | meets |
| round1 | split8 | ExtraPostPlacementOpt | -0.595 | +0.036 | no (setup) |
| round1 | split8 | ExtraTimingOpt | +0.014 | +0.036 | no (setup) |
| round1 | split8 | AltSpreadLogic_high | +0.140 | +0.036 | meets |
| round2 | release | ExtraPostPlacementOpt | +0.108 | +0.016 | meets |
| round2 | release | ExtraTimingOpt | +0.071 | +0.014 | meets |
| round2 | release | AltSpreadLogic_high | +0.209 | +0.016 | meets |
| round2 | split1 | ExtraPostPlacementOpt | +0.189 | +0.036 | meets |
| round2 | split1 | ExtraTimingOpt | +0.196 | +0.036 | meets |
| round2 | split1 | AltSpreadLogic_high | +0.118 | +0.036 | meets |
| round2 | split8 | ExtraPostPlacementOpt | -0.595 | +0.036 | no (setup) |
| round2 | split8 | ExtraTimingOpt | +0.014 | +0.036 | no (setup) |
| round2 | split8 | AltSpreadLogic_high | +0.140 | +0.036 | meets |

round1 split1: best of three MEETS #818 (3 of 3 directives meet)
round1 split8: best of three MEETS #818 (1 of 3 directives meet)
round2 release: best of three MEETS #818 (3 of 3 directives meet)
round2 split1: best of three MEETS #818 (3 of 3 directives meet)
round2 split8: best of three MEETS #818 (1 of 3 directives meet)
