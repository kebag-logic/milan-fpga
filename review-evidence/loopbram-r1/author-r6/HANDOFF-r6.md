Status: REVIEW READY, with hosted exact-head evidence still owed (see "Not run" below)
ETA: complete; no author jobs remain. The owed evidence needs a push, which this session may not do.

[A826] Round 6, issue #979 / PR #987. Head c413d33abe016f5c1e44bdaa1e0354cfe4ab6d99 on pf-loopbram-1, target dev-soft-core.
Three local commits on 9acb9b828b29aba71bd51303a4836f86c2278267. Nothing pushed; no issue or PR comment; no bench.
No RTL, configuration, submodule or workflow byte changed this round.

## Hosted failure at 9acb9b82: cause and fix

- **Cause.** The hosted failures are the `docs-check` job (138601303963) and the `elaborate` job (138602447405).
  Both check out the PR merge `7bfae19` with `submodules: false`, and neither runs a submodule step.
  Their "Require every gate exactly once" step calls `ci_builder_legs.inventory()`, which runs
  `sw/builder/test_builder.py --list`.
  - This PR made the driver's `__main__` import `test_input_loopback` before it handles `--list`.
  - That module imported `gen_aemi_image` at module scope.
  - `gen_aemi_image` exits 2 when `protocol-processor` is not checked out ("the protocol-processor submodule is not
    checked out").
  - The Python version and pyyaml play no part. The local runs that returned 0 had the submodule present.
- **Fix** (42c0d636). `test_input_loopback.py` now imports the five descriptor generators inside the two functions
  that use them. This is the repository's existing pattern, as in `sw/builder/test_declarations.py:41` and `:437`.
  Nothing in the test changed except where it imports.
- **Proof** ([repro log](receipts/repro--repro.log.txt)), run on Python 3.12 with pyyaml against the hosted run's own
  downloaded receipts:
  - At `7bfae19` with no submodules, `--list` exits 2, and both verify steps fail with the hosted traceback.
  - At `7bfae19` with `protocol-processor` present, the same hosted receipts verify: docs has 45 gates exactly once,
    elaborate 5. So `--list` was the only cause.
  - At the final merge `79d35065` with no submodules, `--list` exits 0. Its 114-gate inventory is byte-identical
    (sha256 `acc4d933…`) to the one the hosted receipts were checked against. Its two legs are [1, 113].
- The `verilator-suites` failure ("expected 19 shard directories, found 9") was fail-fast fallout. Every shard,
  the Yosys shards and six rtl-fast jobs were cancelled, not failed.

## R909-3-N1 (MINOR): planner new-suite contract — CLOSED, with one decision to confirm

- Both suites are now in `PROVISIONAL_SUITES` at the driver's `suite_timeout` figure (243516da, c413d33a).
- **Decision for the manager to confirm.** The suites had no `suite_timeout` arm, so their figure was the `*` arm's
  1800 s. That cannot pass at any worker count: one 1800 s suite plus the 122 s overhead is 1922 s, above the 1620 s
  bound. The self-test failed 18 of 19 workers. So each suite got its own 300 s arm in `run_all_suites.sh`, which is
  exactly what `reboot_ctrl` did in a0e555a7. Its 300 s figure is now registered as provisional.
  - The cold runs took 34.2 s and 98.0 s at host load average about 206, so each arm keeps at least three times its
    slowest run.
- **No worker was added.** The self-test passes at 19: the largest worker is 1615 s (worker 0, unchanged).
  `input_loopback_dp` moved to worker 12 and `input_loopback` to worker 13.
- The test-evidence ratchet pins the `suite_timeout` block, so the two arms were added to it, as a0e555a7 did. It
  still refuses any other budget change. TESTING.md states the provenance. Replacing both figures with this change's
  own hosted windows is left for the next round, per the decision.

## Validation (final merge 79d35065 = this head merged into dev-soft-core 2509db68)

- docs.yml replay: 43 of its 46 gate steps ran and exit 0; the other three are listed under "Not run". The merge
  tree was clean after every step
  ([table](receipts/INDEX.md#docs-workflow-replay-at-the-final-merge)).
- rtl.yml: the ownership step passes for all 19 shards and the physical selection step passes. Each new suite is
  owned exactly once.
- Builder driver, the changed gate `test_input_loopback_contract`: PASS. The standalone test also passes.
- Planner self-test PASS; 19 shard listings exit 0. Test-evidence self-test (105 checks) and check PASS. Tally,
  cancellation and both workflow-generator checks PASS.

## Not run (foreground-only, 10 minutes per command; `act` needs the pushed head)

- **Docs:** builder legs 0 and 1 (locally about 1700 s and 1100 s). "Compiler-absent firmware controls": its
  `--absent` command alone exceeded 595 s. That step imports `test_builder` only as a module, so it reads none of
  this round's bytes. It passed hosted at `7bfae19`.
- **Elaborate:** gates 0 to 4, the builder legs with elaboration and the three simulation legs.
- **rtl-fast:** the jobs fail-fast cancelled at `7bfae19`: firmware-unit, publication-census,
  firmware-control-mutants, firmware-srp-mutants, firmware-boundary and yosys-elaboration. They have never
  completed hosted for this PR.
- **rtl:** the 19 suite shards and their aggregate; driver runs of shards 12/19 and 13/19, each about 20 minutes.
  yosys-portability.
- **Owed:** an exact-head verify with fresh receipts, after the manager pushes this head (hosted, or
  `act_ci.py --pr 987`).
- **Suggested follow-up issue** (not done, out of scope): a self-check that `test_builder.py --list` runs in a
  checkout without submodules. Today only the hosted aggregate catches this class of failure.

The two scratch merge worktrees were removed after the receipts were taken; `git worktree list` no longer names them.
They are rebuilt by merging c413d33a into dev-soft-core 2509db68. The rest of the scratch, `$SCRATCH` in the
receipts, is now `/data-2/milan/tmp/loopbram-a826-r6/scratch`. That covers the hosted artifacts, the 3.12
environment and the replay logs. No process from this session remains.

[Round-6 delta](REVIEW-READY.md) · [Full PR body](PR-BODY.md) · [Receipts](receipts/INDEX.md)

REVIEW READY c413d33abe016f5c1e44bdaa1e0354cfe4ab6d99
