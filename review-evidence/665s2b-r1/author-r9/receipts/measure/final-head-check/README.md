# A fresh build at the head reproduces a measured group

`run.py --point 1x1 --groups backlog --record-budget-findings` with `CSB_CPU_HZ=100000000`, from a clean clone at `bf1773c0` with the same labelled profiling variant as the legs (round 8's `harness-profile-cumulative.patch`), arm A, a fresh build.

- `1 groups graded, 0 refusals, 0 budget misses (0 of 12 probe instances, 0 of 12 paths)`;
- its `backlog.log` is byte-identical to leg N9-A1's (`cmp`), sha256 `6002eb0425c9ee0bbbf0fb590a4aab130bd1faca52932ce5b9aa75b23b1eaeaa`;
- its image is byte-identical to N9-A1's, sha256 `f3d8ffedc4c42f7758bd6a5175238c5f99bb0b45d03cbcfaf45b5bfd8435c45c`.
