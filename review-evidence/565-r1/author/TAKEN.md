[A344] TAKEN
Branch: 565-8x8-clock at dev 831f94f4146cc45ec476f8c8dcf5afac7cd8eacf.
Authoritative references: assignment https://github.com/kebag-logic/milan-fpga/issues/565#issuecomment-5848231174; #559 decision https://github.com/kebag-logic/milan-fpga/issues/559#issuecomment-5831090112; BAREMETAL_FIRMWARE.md build contract.
Interpreted scope: declare the 8x8 Milan/CPU clock as 50 MHz, audit every consumer and unchanged configurations, remeasure all six capture arms, check ROM digests, and report the #231 baseline's clock dependencies without editing it. The system and audio clocks retain their existing contracts. Stop and report if either 8x8 50 MHz arm exceeds 24.5 ms.
Validation plan: full builder in compiler-present and compiler-absent modes; required documentation gates; capture input gate; lint; ROM digest check; default sweep chunks exercising 8x8; git diff --check.
Executor: [A344]. Internal reviewer: [R338]. External reviewer: [R339].
Blockers: none. Work remains local under the assignment; no push or PR operations.
