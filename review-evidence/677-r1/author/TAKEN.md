[A556] TAKEN
Branch: `677-fw-fixes`, base `6714181d0c8a16e2983f85b724f4d688f5111835`.
Authoritative references: #677 acceptance, #678 manager ruling, assignment comment 6021510152, firmware public headers and FT coverage contract.
Interpreted scope: bound erased-record payload reads by loaded bytes; document the synchronous no-callback rule on all firmware ports and guard ADP re-entry, with regression and planted-defect evidence. Bare-metal firmware only; no RTL, default-build, or shipping-image changes.
Validation plan: firmware host gates, tally and coverage gates, both mutation campaigns, available RV32 builds, builder bank, docs gates; 100% branch ratchet with no new exclusions.
Executor: [A556]. Internal reviewer: [R524]. External reviewer: [R525].
Blockers: none identified during initial scope check.
