[A827] Shard the firmware-boundary CI job

Closes #980

## Why

`rtl-fast`'s `firmware-boundary` job ran 21 to 24 minutes against its 30-minute limit. It exceeded the limit on PR #961, and `ci_fail_fast.py` then cancelled every workflow on that head. The limit stays at 30 minutes. This PR shards the job instead.

## What changes

- **Shards.** The `--without verilator` compile set is cut into units: one per run of each known builder (`ctrl_configs.BUILDERS`). The control gate's run is cut into two by its new `--build-part 0/2` and `1/2`. `ctrl_configs.SHARDS` assigns each unit to exactly one of three shards, balanced on measured unit times. Every run checks the table and refuses, by name, a unit no shard builds or two shards build.
- **Shard jobs.** `firmware-boundary-shards` is a matrix whose jobs are named `firmware-boundary shard 0/3` to `2/3`. Each runs `ctrl_boundary.py --require-rv32 --without verilator --shard k/3 --capture-out <capture>`: it builds its units under its own capture and judges nothing. It uploads only the capture's `records.jsonl`, `manifest.jsonl` and `text/`. The capture's wrappers link the SDK's tools, so they are not uploaded.
- **Aggregate.** `firmware-boundary` keeps its name. It needs every shard, downloads the three captures and runs `ctrl_boundary.py --require-rv32 --selftest --without verilator --shards 3 --capture ...`. It requires each unit's run in exactly one capture, refusing by name a unit with no run, one with two runs and a run that is no unit's. It then judges the captures as one capture, with the controls, the pin and figure controls and the stack's own self-test, once. Because the judgement runs over the union, the RV32 target set and `held()` see the same compile set as the unsharded run.
- **Verdict.** A failed shard skips `firmware-boundary`, and the `rtl-fast` verdict now also requires `firmware-boundary-shards`. The required contexts (`rtl-fast` and the others in the `dev` ruleset) are unchanged.
- **Self-test.** `--selftest` gains four shard controls: the table with a unit dropped, the table with that unit in two shards, the captures with that unit's run dropped, and the captures with it repeated. Each must be refused naming the unit. `test_ctrl_firmware.py --build-part` first proves, through the live dispatch, that its parts build every suite of the default build-only run once. It also refuses a planted dropped and a planted duplicated suite.
- **AECP arms.** `aecp_arms.all_arms` is now `arms_in_order()`, run in order. Its calls are identical to before (18 normal, 9 coverage), and it can now split across parts: it was 334 s of the control gate's build.
- **Fail-fast watcher sees the raw skipped-matrix names.**
  - **The defect.** The runner evaluates every `${{ }}` in an env value, YAML quotes included, and the watcher job has no matrix. So the raw name `firmware-boundary shard ${{ matrix.shard }}/${{ matrix.total }}` reached the watcher as `firmware-boundary shard /`. On a run that skipped the matrix unexpanded, the watcher then stopped observing.
  - **The fix.** The generator now writes the watcher's job lists with JSON's `\u0024` for each `$` that opens an expression. `json.loads` decodes that to the exact raw name.
  - **Identity.** The generator and the watcher both refuse an unexpanded name that equals an expanded one.
  - **`rtl`'s matrices.** The same change fixes `rtl.yml`'s `Verilator shard` and `Yosys shard` keys, which had the same defect before this PR.
- **Generated workflows and contract.** The workflows are generated. The template `.github/ci-templates/rtl-fast.yml` and the generator changed, and `scripts/ci_gate_workflows.py` regenerated `.github/workflows/rtl-fast.yml` and `rtl.yml`. `ci_fail_fast`'s expected jobs and the per-job runtime evidence now cover each shard. `scripts/ci_events.py` records both jobs' step lists, the shard matrix's `strategy`, the verdict's new result and the RV32 pins.
- **Docs.** `docs/testing/CI_WORKFLOWS.md` (the job list, the design, the measured times and the skipped-matrix escape), `sw/firmware/ctrl/README.md` and the module docstrings.

## Evidence

Local runs used a shared host, with every builder at its own four jobs as on the hosted runner.

| Run | Local wall |
|---|---|
| shard 0/3: control gate part 0/2, store, RV32 self-test | 462 s |
| shard 1/3: control gate part 1/2, reset entry | 393 s |
| shard 2/3: coverage gate, F5 at both shapes | 449 s |
| judging run over the three captures, upload-shaped | 259 s; 250 s at `b7b35193` |
| unsharded control gate build (whole) | 714 s; its parts 358 s and 392 s |

- **Unsharded hosted reference.** Run 45071981993 took 1273 s for the step: builds 1063 s (control gate 603 s, coverage gate 309 s, store 86 s), judgement 210 s. Local builds took 1.19 times as long, which projects each shard at about 8 minutes with setup and the judging job at about 5.
- **Unit union.** The judging run requires all 8 units once across the 3 captures.
- **Source union.** The whole control-gate build and its two parts compile the same 1262 distinct sources, with their dependency lists: none missing, none extra.
- **Plants.**
  - Judging without shard 2's capture refuses, naming the coverage gate and both F5 runs.
  - Judging with shard 0's capture twice refuses, naming each of its units.
  - A table with a unit dropped, or in two shards, refuses before building.
  - The four shard controls are `[ok]`.
- **Watcher runtime control.** `ci_fail_fast_selftest.py` reads each committed workflow and evaluates the watcher's env the way a job with no matrix evaluates it, before it watches. Each raw matrix is skipped unexpanded and one job is still running, then that job fails. The watcher must wait through the first read, report the failure on the second with no observer error, and leave cancellation to every sibling intact.
  - Given the unescaped form, the control finds the watcher stopped after one read. It does so for `rtl` and `rtl-fast`, and also for those two files as committed before this fix.
  - A generator plant whose unexpanded matrix name equals another job's name is refused.
- **Gates.** These pass at the head: `ci_gate_workflows.py --check`, `ci_events.py --check` and `--selftest`, every CI scheduling self-test, `check_wire_accountability.py --self-test`, the docs, doc-path, doc-style, em-dash, hygiene, TODO, shell and Python idiom gates, `docs_inventory.py --check` and `act_ci.py --selftest`.

## Open

- **Hosted timing not yet measured.** The hosted run on this PR, with each shard's time, is the remaining acceptance item. A docs-only run, where the shard matrix skips unexpanded, would also confirm on hosted that `ci-fail-fast` reports no observer error.
- **Local replica.** The replica is owed at the pushed head.
- **Image inventories not regenerated.** `ci/image/tool-inventory.json` and `ci/image/command-table.json` need the CI image's pinned shell parser, and no hosted job checks them.
- **Runner time.** Runner time goes from one job of about 22 minutes to three of about 8 plus one of about 5. The critical path falls to about 13 to 14 minutes.
