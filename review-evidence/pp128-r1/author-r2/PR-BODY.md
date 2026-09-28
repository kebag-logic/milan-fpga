[A395] Closes #128

Retry refused ACMP destination-address allocations automatically in fair 100 ms
rounds. Enabled sources acquire a late-available address before the first listener
probe; absent and out-of-range allocations remain honest, paced failures. Command
service stays bounded, obsolete grants are discarded and released, and ports,
parameters and conflict/PCP backoff are unchanged.

## Round 2

Fix the declaration order and remove a redundant retry-clear term. Document the
consumer-visible paced-round behavior. Add consecutive-command, same-round
restart, release-fairness, demand-path and exact-edge cancellation regressions.
Remove the mutation runner's host deadline and record equivalent terms explicitly.

Validation: all 33 suites pass (1,015,055 checks), including every ACMP and SRP
suite; full lint, documentation, portability and figure entry points return 0.
The campaign kills 56 defects, retains four equivalent controls, and witnesses all
50 retry assertion sites. The real parent-shim harness returns first-probe success
at `cc7c911e933aed4bfc9324eb5da473ae73bef618` after one retry period plus the bounded sweep.
The parent declaration check passes with its four pre-existing findings. The parent
evidence check passes with the proposed reader disposition added in scratch;
without that parent row it reports only the known missing disposition.

Parent pin-adoption reconciliation:

- [H]: `pp_shadow [H]` must allow one `T-ACMP-DA-RETRY` round plus the source sweep before requiring a new accepted/refused ALLOC_DA. A PROBE_TX inside an already attempted round does not force another allocation. Observe an accepted request, its refusal, the closed DA gate, an honest status-3 probe response and continuing command service; do not require a probe-caused request within 4000 fixed-time cycles.
- [I]: `pp_shadow [I]` must associate each allocation response with the source index of its accepted request and compare that source's DA with KL_maap base + source index. Every enabled in-block source auto-acquires, including CRF source 1; a single global last_da is not necessarily source 0's grant.

DUT-reader disposition for the parent's table:
`"protocol-processor/tb/acmp_talker/retry_mutants.py": "mutation campaign; plants named defects in a scratch copy and requires named assertion failures from completed cycle-bounded simulations; reads no expected behavior from RTL",`

The parent lane owns these table/test edits and the pp_shadow reruns. No parent
source or processor/parent port interface changes are included here.
