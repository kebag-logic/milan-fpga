# R246-1 independent verdict and ledger, written before reading any prior review finding
Written (UTC): 2026-09-25T20:56:19Z
Head: f36b40ddb5bf7fa5b12bba47d136e0b9d429403c

Verdict: NEGATIVE

Findings (independent):
- F1 MAJOR [Conformance, Docs]: the stated shared tracked-header write by the five sim_nxn legs does not occur at this head. The builder, invoked from the suite directory with ../../../configs/<cfg>.yaml, derives cfg source tb/verilator/milan_dp/../../../configs/<cfg>.yaml, so _write_shape_copies writes the shape header into the private -o directory. Real pooled run: all five grouped legs emitted their image; no tracked header mtime or byte changed. The PR replaces the accurate sim_nxn.cpp comment ("touches nothing tracked") with an inaccurate one, and repeats the claim in sim_pool.py, README.md and TESTING.md. The #517 shared-header decision premise conflicts with executable evidence.
- F2 MINOR [Tests]: test_sim_pool_backpressure.py verdict is nondeterministic: (a) torn ledger read race (JSONDecodeError in child-exit controls, 3 of 20 full runs); (b) 12 of 28 controls fail when the test inherits SIGINT ignored (asynchronous list in a non-interactive shell); the sibling test normalizes signal state, this file does not.
- S1..S4 SUGGESTION [Tests/Robustness]: pool tests not wired into any gate; four narrow claims survive mutation (late signal, duplicate leg, stale log removal, stdin); clean target keeps obj_legs; hard-coded 28 and an in-repo-absent outer guard in the backpressure docstring.

Ledger (independent):
| lens | state | covering round | head |
| Conformance | UNCLEAN (F1) | R246-1 | f36b40dd |
| RTL | CLEAN | R246-1 | f36b40dd |
| Robustness | CLEAN | R246-1 | f36b40dd |
| Tests | UNCLEAN (F2) | R246-1 | f36b40dd |
| Docs | UNCLEAN (F1) | R246-1 | f36b40dd |
