[A388] TAKEN
Branch: `602-phc-step-mr`, starting at `49012143b335ea48d6a71c441a05d0c1796887ff`.
Authoritative references: #602 ruling 5859297355, assignments 5859299480 and 5860151273, scope correction 5859621253; round-1 reviews R366-1 and R367-1.
Interpreted scope: correct current documentation and test narratives, make option-off checks event-relative, and add the coincident PHC-step/received-CRF restart scenario. RTL and the five configurations stay unchanged. Reviewers remain R366 and R367.
Validation plan: required datapath and restart-engine suites and controls, RTL lint, datapath OOC at 1x1 and 8x8, full builder bank in both compiler modes, CI-scope self-test, baremetal-only, documentation gates and diff hygiene at the committed head.
Blockers: none.
