[A826] ROUND 6 - REVIEW READY

Head: c413d33abe016f5c1e44bdaa1e0354cfe4ab6d99. Branch: pf-loopbram-1. PR #987 into dev-soft-core; issue #979.
Delta from the reviewed head 9acb9b828b29aba71bd51303a4836f86c2278267.
Replays read the final merge 79d350657a5966306c87a607ffc3e52ecf6abc05 (tree ecaf54ccedc2f1fcdd4806dd3c0d510a202e273b):
this head merged into dev-soft-core 2509db684b58b920e215b0d5d327b4a845bac3f4, the base of the failing hosted merge.
No push, issue/PR comment, merge, board, bench or test-machine access occurred.

## Commits since 9acb9b82

| Commit | Subject |
|---|---|
| 42c0d6368f9d166cff9780afb2358628b851af64 | Import the descriptor generators inside the loopback test so builder --list runs without submodules |
| 243516da306747c5dcd757f78750385b289926e2 | Register the loopback suites at their own 300 s suite timeouts as provisional figures |
| c413d33abe016f5c1e44bdaa1e0354cfe4ab6d99 | Pin the loopback suites' timeout arms in the runner evidence contract |

Changed: `sw/builder/test_input_loopback.py`, `scripts/suite_shards.py`, `scripts/run_all_suites.sh`,
`scripts/measure_test_evidence.py`, `docs/testing/TESTING.md`; 28 insertions, 15 deletions
([source binding](receipts/source-binding.json.txt)). No RTL, configuration, submodule or workflow byte changed.

## Hosted CI failure at 9acb9b82 - FIXED at its cause

Hosted run 45434456591 (docs) and 45434456617 (elaborate) on the PR merge `7bfae19`.
Two jobs failed in "Require every gate exactly once": `docs-check` (138601303963) and `elaborate` (138602447405).
Each raised `CalledProcessError: ['/usr/bin/python3', 'sw/builder/test_builder.py', '--list'] returned non-zero
exit status 2` from `scripts/ci_builder_legs.py:59` `inventory()`.

The cause chain:

1. Both aggregate jobs check out with `submodules: false` and run no submodule step
   ([docs-check excerpt](receipts/hosted--job-138601303963.excerpt.txt),
   [elaborate excerpt](receipts/hosted--job-138602447405.excerpt.txt)). Every gates job initializes the submodules
   it needs before it runs the builder; the two aggregates only read receipts and the inventory.
2. This PR's `sw/builder/test_builder.py` imports `test_input_loopback` in its `__main__` block, before
   `_gate_run_list()` answers `--list`.
3. At 9acb9b82, `sw/builder/test_input_loopback.py` imported `aem_assemble`, `aem_specs`, `gen_aem_store`,
   `gen_aemi_image` and `gen_desc_image` at module scope.
4. `gen_aemi_image` refuses at import with exit 2 when `protocol-processor/hdl/aecp/desc` is absent:
   "gen_aemi_image: the protocol-processor submodule is not checked out".

So the exit status 2 is the generator's own refusal, not argparse. The Python version (3.12 against 3.14) and
pyyaml have no bearing. The `--list` runs that returned 0 were in checkouts with the submodule present.

The fix: the generator imports now sit inside `image()` and `test_input_loopback_contract()`, the two functions that
use them. A comment there says why. That is the pattern the existing builder tests already follow, for example
`sw/builder/test_declarations.py:41` and `:437`. The test's assertions and fixtures are byte-for-byte unchanged.

### Proof ([log](receipts/repro--repro.log.txt), [script](receipts/tools--repro.sh.txt), [verify step wrapper](receipts/tools--verify.sh.txt))

The verify step was run exactly as the job writes it: `python3 scripts/ci_gate_receipts.py verify --workflow <wf>
--root <downloaded artifacts> --head <checkout HEAD> --output <file>`, with `CI_GATE_NEEDS` naming every worker job
as successful. It used Python 3.12 with pyyaml 6.0.2 and the artifacts downloaded from the hosted runs.

| Tree | Submodules | `test_builder.py --list` | docs verify | elaborate verify |
|---|---|---|---|---|
| hosted merge 7bfae19 | none, as hosted | exit 2, the generator's refusal | exit 1, the hosted traceback | exit 1, the hosted traceback |
| hosted merge 7bfae19 | protocol-processor present | exit 0, sha256 acc4d933... | exit 0: 45 source gates exactly once | exit 0: 5 source gates exactly once |
| final merge 79d35065 | none, as hosted | exit 0, sha256 acc4d933..., byte-identical | not runnable without receipts at this head | not runnable without receipts at this head |

The second row shows that every other check in both verify steps passes on the hosted receipts.
Those checks cover leg counts, schema, head/tree binding, the template digest, every gate outcome and the builder
and simulation unions. So the `--list` exit is the only cause.
The third row shows that the inventory step now succeeds where the hosted job runs it, and produces the same
114-gate inventory the hosted receipts were checked against. `ci_builder_legs.partition()` of it is legs [1, 113].
The builder driver runs the moved gate at the final merge: `test_input_loopback_contract` PASS, with a driver
receipt carrying the same 114-name inventory ([log](receipts/driver-input-loopback.log.txt),
[receipt](receipts/driver-input-loopback.json.txt)). `python3 sw/builder/test_input_loopback.py` also passes at the
lane head ([log](receipts/lane--loopback-standalone.log.txt)).

`verilator-suites` "expected 19 shard directories, found 9" is fallout from the fail-fast job, not a separate defect.
At 7bfae19, every suite shard, the Yosys shards and six rtl-fast jobs were cancelled; none failed on its own.

## R909-3-N1 MINOR: new suites not registered under the planner's new-suite contract - CLOSED

Manager decision (option a): register both suites at the driver's `suite_timeout` figure in `PROVISIONAL_SUITES`,
and add a worker if the self-test then requires one.

**Material assumption, for the manager and reviewer to confirm.** Neither suite had its own `suite_timeout` arm, so
the driver's figure for each was the `*` arm's 1800 s. Registered at 1800 s, the self-test failed 18 of 19 workers.
It is not satisfiable by adding workers: a worker holding one 1800 s suite predicts 1800 + 122 = 1922 s, above the
1620 s regular bound at any worker count. So both suites now have their own arm in `scripts/run_all_suites.sh`, 300 s
each, and that is the figure registered. This is how the contract's only other provisional suite, `reboot_ctrl`, was
registered: a0e555a7 added its 300 s arm and its provisional 300 s figure together.

| Check at c413d33a | Result |
|---|---|
| `suite_timeout` arms | `input_loopback` 300, `input_loopback_dp` 300, `reboot_ctrl` 300, any other suite 1800 ([log](receipts/lane--timeout-arms.log.txt)) |
| `SUITE_SECONDS` / `PROVISIONAL_SUITES` | both 300, both provisional with `reboot_ctrl`; the self-test's provisional check confirms each equals its arm |
| `python3 scripts/suite_shards.py --selftest` | `selftest: PASS`. Largest regular worker 1615 s (worker 0, `follow_ring`, unchanged), bound 1620 s; workers 12 and 13 predicted 1563 s and 1560 s ([log](receipts/lane--planner-selftest.log.txt)) |
| Worker added | none: the self-test passes at 19 |
| 19 shard listings | 19 of 19 exit 0. `input_loopback_dp` is on shard 12 with `milan_dp_render__2` and `csr`; `input_loopback` on 13 with `pp_shadow__2` and `nvm_cosim`; each once; union equals the unsharded selection ([log](receipts/lane--shard-lists.log.txt)) |
| Cold runs within the arm (`make -C tb/verilator/<suite>`, four pinned CPUs, load average about 206) | `input_loopback` 34.2 s, PASS (79587 and 76017 checks); `input_loopback_dp` 98.0 s after its build directory was removed, PASS (16173 and 122549 checks) ([leaf](receipts/cold-input_loopback.log.txt), [parent](receipts/cold-input_loopback_dp.log.txt)) |
| Runner evidence contract (`measure_test_evidence.py`) | The pinned `suite_timeout` block gains the two arms, as a0e555a7 did for `reboot_ctrl`. Any other budget change is still refused; `--check` and `--selftest` (105 of 105) pass |

`docs/testing/TESTING.md` now states that both figures are provisional at their 300 s arms, why the `*` arm cannot
be the figure, and the cold runs behind the margin. It also says that measured hosted windows replace both figures
after the first hosted run of a head that carries them; per the decision, that replacement is the next round's.
`scripts/run_all_suites.sh`'s header lists the 300 s defaults. `scripts/suite_shards.py` stays at 999 lines.

## Validation at the final merge 79d35065

| Gate | Result |
|---|---|
| docs.yml replay, 43 of 46 gate steps, each as written in its job ([table](receipts/INDEX.md#docs-workflow-replay-at-the-final-merge), [results](receipts/docswf2--results.json.txt)) | 43 of 43 exit 0; merge tree clean after each. It includes the no-git docs gate and wire accountability. It covers test-evidence, the Python, C/C++ and shell idiom gates, fail-fast, contents and inventory, entity shape, CI scheduling and evidence controls, the CI event and SHA contract and the local act runner contract |
| rtl.yml "Prove specialized suite ownership", shards 0-18, and "Prove physical suite selection" ([log](receipts/rtl-ownership.log.txt)) | 19 of 19 and 1 of 1 pass; 85 owned entries, no duplicate |
| Builder inventory as `ci_builder_legs.inventory()` calls it, no submodules | 114 gates, legs [1, 113], byte-identical to the hosted inventory |
| Builder driver, `--gates test_input_loopback_contract --require-rv32` | PASS |
| Lane head: tally self-test, suite cancellation, `ci_suite_workflows.py --check`, `ci_gate_workflows.py --check` | all exit 0 |

The replay tool runs a chosen row of `docs.yml`'s `run:` steps with `bash -e` and the job's budgets, in the final-merge
worktree ([tool](receipts/tools--wfreplay.py.txt)). Its submodules match the docs gates jobs: protocol-processor,
gptp-processor, verilog-axis and tsn-c-stack. `PIP_CONSTRAINT` is unset, so each step's install is a no-op against
the pre-provisioned local environment. The event is `pull_request` with base `dev-soft-core`, so the added-line
gate judged 640 added lines in 13 pages against 2509db68, as hosted would. The no-git job runs in an exported copy.

## Not run, and why

The session ran foreground commands only, each limited to ten minutes, and the local act runner refuses a head
that is not the PR's pushed head. So the following did not run this round:

- docs: the two builder legs (round 5's local runs took 1702 s and 1094 s).
- docs: "Compiler-absent firmware controls". Its `--selftest` command passed. Its `--absent` command alone was
  stopped at 595 s ([log](receipts/docswf2--030-split.log.txt)); it ran 4.5 minutes hosted. It imports `test_builder`
  as a module, so the driver's `__main__` imports never run, and it reads none of this round's changed bytes. It
  passed hosted at 7bfae19.
- elaborate: gates 0-4 (the builder legs with elaboration, and the three simulation legs).
- rtl-fast: the jobs cancelled at 7bfae19: firmware-unit, publication-census, firmware-control-mutants,
  firmware-srp-mutants, firmware-boundary and yosys-elaboration. None has completed hosted for this PR.
- rtl: the 19 suite shards, the suite aggregate and yosys-portability; the sweep driver over shards 12/19 and
  13/19, now the owners of the new suites, each about 20 minutes.
- An exact-head verify step with fresh receipts. That needs every gates job at one head, so it is owed to the
  hosted run, or to `act_ci.py --pr 987`, after the manager pushes this head.

## Open risks and questions

- Confirm the 300 s arms as the reading of the N1 decision (see the assumption above).
- Tests: no self-check was added that `test_builder.py --list` runs without submodules. Only the hosted
  aggregate guards that property today. Suggested as a new issue rather than widening this one.
- The rtl-fast jobs above have never completed hosted for this PR.

Closure labels here are the author's dispositions; each finding is cleared only by its reviewer.
This is author evidence, not a reviewer verdict or a clean-lens ledger.
