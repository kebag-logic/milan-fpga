[A298] TAKEN
Branch: 443-render-csr; base 0755923d983218ca6ca9db6891a558cbe6425b8d.
Executor: [A298]. Reviewers: [R320] internal and [R321] external, per assignment.
Authoritative references: REQ-CSR-01/02; REGISTER_MAP.md verdict legend and claim rule; KL_render_setpoint tap contract; manager decision on item 4.
Interpreted scope: items 1, 2, 3 and 5 only. Claim the free debug-group word 0x8DC as RENDER_STAT: [7:0] selected listener fill in events, [8] prefill, [9] converged, [15:10] reserved zero, [31:16] global saturating rail count. The existing STRM_SEL listener index selects the per-stream fields; talker and out-of-range selections read zero. Reset is 0x00000100 for a present listener; an absent stage supplies structural zero. No STREAM_INTERRUPTED change.
Validation plan: AXI-Lite reads against actual taps through milan_dp, including prefill, fill, convergence, a rail, a stage-absent control and a wrong-field mutant; touched legs and default sweep in recorded chunks; milan_dp_render; base/head synthesis counts; builder and requested documentation/style/RTL gates.
Blockers: none. Local commit and review artifacts only; no push or PR operations.
