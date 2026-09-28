[A397] TAKEN
Branch: 602-phc-step-mr at 471892a9bcc2d26fdcfc19db01949ecea83c5e0f.
Authoritative references: #602 ruling 5859297355; round-3 assignment 5861304608; round-2 assignment 5860151273; IEEE 1722-2016 4.4.4.3, 4.4.4.7 and 10.4.3; Milan v1.2 B.1.1/B.1.2.
Interpreted scope: correct the firmware gate description, observe option-off adjtime through settling, and apply the accepted coincident-check, README and Makefile wording. RTL remains unchanged. Executor [A397]; reviewers [R366] and [R367].
Validation plan: delayed adjtime controls at 16 and 256 cycles plus existing controls; stale-document rescans; milan_dp and tkdiag suites; lint; datapath OOC at AX 1x1 and 8x8; full builder bank in both compiler modes; five-configuration identity; ci_scope, baremetal and docs gates; git diff --check. All required gates at the committed head.
Blockers: none.
