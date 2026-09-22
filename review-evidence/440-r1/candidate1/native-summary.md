[A10] CURRENT-DEV CANDIDATE FULL NATIVE BAR COMPLETE

Candidate 0e8cd2325a0d3b15201907372d708428a61044fd, tree c23dff6c0eafdf5ae89bb3e8a9416c55533a2332, combines current dev ec34fcdee0ca9ffa63564a9af8ad70a3a618de29 with frozen reviewed head 9d6109ccf924c03308cb8aa202ce68a435cd4f8d. All 43 static/builder commands and all five native commands passed on this candidate. Both validation checkouts' 851 parent file blobs/modes and all three required submodule populations match their committed pins; their index trees and tracked state are clean.

The parent sweep passed 55 suites and 2,118,264 checks with zero failures. Yosys portability and structural gates passed. The pinned PP sweep passed 14,903 checks; the gPTP processor complete make target passed; behave passed 14 features, 316 scenarios and 1,515 steps. Four declared field-campaign skips ran zero checks, and builder calibration gate 11 remains NOT RUN. No hardware evidence is inferred.

Complete specifications, logs, per-suite/Yosys results, and both integrity receipts are archived. The complete PR delta is unchanged on the new dev and touches paths disjoint from #505. Source-head proof at its old base remains separately attributed.

Both independent reviews and required exact-head hosted jobs are already positive/passing. Trusted ready act replication remains in progress. After it completes, a fresh live preflight and actual merged-tree/post-merge checks remain required.
