# Hosted image evidence (read-only gh api job logs, excerpts)

## job 96546610543
```
2026-08-20T19:02:14.0246556Z Image: ubuntu-24.04
2026-08-20T19:02:25.2821781Z Get:3 http://azure.archive.ubuntu.com/ubuntu noble/universe amd64 yosys amd64 0.33-5build2 [3222 kB]
sha256 eb06af482a13e7c0a234c090503514a0bce45af537dca88a2ba45f5ab9a94302 size 28128
```
## job 113696564335
```
2026-10-09T06:15:18.5761545Z Image: ubuntu-24.04
sha256 d7ae7e49d237e8da6c96be21fa2f7bdac33d61b3060d1fcd088bc7d37a678142 size 26560
```
## job 121179871493
```
2026-10-25T13:18:20.1125948Z Image: ubuntu-26.04
2026-10-25T13:18:43.3076512Z ERROR: Cannot install PyYAML==6.0.2 because these package versions have conflicting dependencies.
2026-10-25T13:18:43.3078743Z ERROR: ResolutionImpossible: for help visit https://pip.pypa.io/en/latest/topics/dependency-resolution/#dealing-with-dependency-con
sha256 3c095ed1cc60dad4588d7ce773324ff518180f5f1b2d329f2ed9a9be40342cdc size 57488
```

- job 96546610543: run 32406467657 (rtl, 2026-08-20), yosys-portability, the run the yosys_shards.py weights come from.
- job 113696564335: run 37892515345 (rtl-full, 2026-10-09), shard 0/5, the run docs/testing/TESTING.md measures.
- job 121179871493: run 40187576861 (docs, PR #783 head 91bf51e4), docs-check, the #784 failure.
