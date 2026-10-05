[A543] TAKEN
Branch: `653-b12-bench` from dev `fa450d301805881ad713b67521477bf042ddadfd`.
Assignment: https://github.com/kebag-logic/milan-fpga/issues/653#issuecomment-5993102892
Executor: [A543]. Reviewers: [R498] internal, [R499] external.
Authoritative references: #653 in full; PR #659; `docs/findings/653_DISCONNECT_ORDER_BENCH.md`; Milan v1.2 Sections 5.3.8.10 and 5.4.5; IEEE 1722.1-2021 counter and connection-management clauses.
Interpreted scope: identity first on the booted dev `bbf704ec` image. Build the named VLAN controller-library fork (`a71ffa99`) and apply the application rule at `a13db9d9`. Record the prescribed holds and push phases in both directions, including exposed CRF streams, with at least five cycles per hold and direction. Capture each cycle at the DUT link, correlate response status, notification order, and library state. Run both ten-minute sequence windows with two-second polls. Record and restore bindings, formats, maps and clock sources, with readbacks.
Validation: raw-byte tap decoding against the earlier decoder; per-cycle and sequence tables; the assigned documentation gates on the physical worktree path.
STOP conditions: failed identity or required bench precondition; incompatible listener format; a proven DUT order or status defect. Findings only; no implementation fix.
Blockers: none established; identity and bench prerequisites pending.
