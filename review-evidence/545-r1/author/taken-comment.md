[A303] TAKEN
Branch: `545-crf-servo-slew`, base `5b73d3f47dfed519eb988c13d6beb1db664ef1e0`.
Executor: [A303]. Independent reviewers: [R300] internal, [R301] external.
Authority: assignment 5827358783, #387 decision 5816509317 with the assignment's citation correction, and FPGA-gPTP PR #76 integration contract at `5dce647a`.
Scope: adopt the reviewed pin; carry the policy level with effective-rate alignment; discard and count every overlapped CRF servo window while retaining PI and lock; add connected and mutation evidence, documentation and area comparison.
Validation: the assignment's focused suites, chunked default datapath sweep, builder, static/documentation/behavior gates, and repository OOC recipe. No publication or merge beyond issue comments is authorized.
Contract discrepancy: #387's historical 0.5 s maximum conflicts with the adopted engine contract, which explicitly has no timeout and can retain an active correction indefinitely. The implementation will retain discard protection for the whole exported level. The 100 us / 200 ppm, 0.5 s case is a simulation stimulus, not a maximum-duration claim; documentation will identify this distinction. No inferred detector or expiry timer will be introduced.
