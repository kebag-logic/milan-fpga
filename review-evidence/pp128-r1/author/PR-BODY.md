[A395] Closes #128

Retry refused ACMP destination-address allocations automatically in fair 100 ms
rounds. Enabled sources acquire a late-available address before the first listener
probe; absent and out-of-range allocations remain honest, paced failures. Command
service stays bounded, obsolete grants are discarded and released, and the parent
interface and conflict/PCP backoff are unchanged.

Validation: all 33 simulation suites pass (1,014,990 checks), including every ACMP
and SRP suite. Lint, documentation, traceability, portability and full figure gates
pass. All 38 new assertion sites have killed-mutant witnesses across 28 mutations;
the updated integration checks also kill the removed-retry defect. The real parent
shim harness returns first-probe success after the documented acquisition bound.
