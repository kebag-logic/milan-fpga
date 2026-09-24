[A284]

Closes #116

The parent rejects seven unexplained arbiter ties, two port comments that
suggest units their names do not carry, and three mutation runners with host
deadlines. Add rationale directly above both literal-bound `u_nvm_arb`
connection runs, reword the two comments, and preserve the admission latency
figure in ordinary prose above its assignment. Remove the three deadlines;
the selected campaigns terminate through finite variants, cycle limits and
unchanged decoder/timer progress. Per-file termination arguments are in
[HANDOFF.md](HANDOFF.md).

Only the five requested files change. RTL tokens remain identical, and the
three runners retain every verdict requirement. The full suite bank has the
same 33 suites, 1,008,919 checks and zero failures before and after. All five
admission shapes and all four mutation campaigns have identical check counts
and verdict tables; [COMPARISON.md](COMPARISON.md) records every row.

Every repository CI gate, the complete documentation check, lint and
portability checks returned 0. The three parent gates each returned 1 at
`a8f8ce810ddba1816cd129d0afcd71e6e02ade1b` and 0 at the candidate, with their
rules and budgets unchanged. All requested parent idiom, frontend, source,
documentation and integration checks passed; integration has the same 371
checks, zero failures and named verdicts at both pins. Exact commands and exit
statuses are in the accompanying
validation records linked from [HANDOFF.md](HANDOFF.md).

Processor head: `a43d07668ff03efc299fbbf2a3891f2aa90255f7`.
Parent gitlink-only commit: `ea96db3246d34dbf3ece2d1aca2a9aaf24596216` (local).
