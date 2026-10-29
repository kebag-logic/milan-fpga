# A fresh build at the head reproduces a measured group

`run.py --point 1x1 --groups backlog --record-budget-findings` with `CSB_CPU_HZ=100000000`, from a clean clone at `f884c7e9` with the same labelled profiling variant as the legs (`receipts/variants/harness-profile-merged.patch`), arm A, a fresh build.

- `1 groups graded, 0 refusals, 0 budget misses (0 of 12 probe instances, 0 of 12 paths)`;
- its `backlog.log` is byte-identical to leg N10-A1's (`cmp`), sha256 `157757bcaadf20eeda6a8dec9154b99af628a32801088001b39586f1064fa0d3`;
- its image is byte-identical to N10-A1's, sha256 `dc27389d3e8876f3d58b51bd2f097af931ade0e4f84f21dbbac4bd63b8be8b9a`.
