[A279] TAKEN
Branch: 548-ctlr-diag-zero
Base: 573f0052a0e4412e81f0845438fcec2086ce5d55
Authoritative references: REQ-CSR-01/05; REGISTER_MAP.md verdict legend; the manager decision in https://github.com/kebag-logic/milan-fpga/issues/548#issuecomment-5821224656.
Interpreted scope: STRUCTURAL ZERO for CTLR_DIAG (0x6F4), correcting the register row, paragraph, group gloss, RTL comments and silicon-evidence interpretation. Add one AXI-Lite zero check after the existing timed controller-monitor traffic in milan_dp. No functional RTL change. No notification-leg mutant runner exists; record a nonzero diagnostic mutation against that same build recipe separately.
Validation plan: timed notification leg plus its nonzero mutation; default milan_dp sweep; both documentation CI inventory modes and all gates listed in the assignment. Commit locally; no push or PR mutation.
Executor: [A279]. Reviewers: [R308] internal, [R309] external.
Blockers: none.
