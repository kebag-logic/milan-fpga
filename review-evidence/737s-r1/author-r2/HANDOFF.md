# HANDOFF — [A727c] issue #737 round 2 (continued), PR #836

Lane: $LANES/737-elab-split, branch 737-elab-split, origin https://github.com/kebag-logic/milan-fpga.git. Base dev e61a4afa.
Start head 6a38c330 (items 1-2 by [A727b]). **Final head e180ba30eccc4ee7c3c699d88973816bdc953caa** (3 commits over 6a38c330). PR #836 is still at aa3e2d85: nothing pushed.
Unit milan-737-a727c-r.service, CPUs 96-111. The leg runs ran in my own transient units milan-737-a727c-leg{0,1,2} (CPUAffinity 96-111, MemoryMax 9G), one after another; each exited before the next started.
Scratch $VALIDATION_STORAGE/737-a727c. Receipts: receipts/ beside this file (each gate's .log and .rc; logs over 200 KB recorded as .log.ref with size and sha256).
Authority: round 2 ruling issuecomment-6596926489; STOP ruling option (B) issuecomment-6608788472.
The previous session of this author was cut by a server error at 17:05 after posting TAKEN. The tree was clean at 6a38c330, so this session started item 3 from scratch.

## Status
- [x] TAKEN posted (previous session, 16:04 UTC): issuecomment-6608888683 (text receipts/taken.md). Not posted again.
- [x] item 3 (R768-1-F3), option (B): commit 0eb3f57e
- [x] item 4 (R767-1-F2): commit 39e3e00f
- [x] item 5 (R767-1-R1; R767-1-S1, R768-1-S1 to S3): commit e180ba30
- [x] item 6: the three re-derived legs run locally (8 of 8 PASS once) and the dropped-simulation control, at e180ba30
- [x] gates at e180ba30 (table below)
- [x] REVIEW READY posted (see the last line)

Commits (one per item, one-line subject, no body, no trailers):
- 0eb3f57e Keep the four shared builder caches off the LiteX workers, so only the builders restore and save them, and state the cold per-run cost the LiteX projections already carry (#737)
- 39e3e00f State that the elaboration projection excludes runner queueing and record run 41583428850's queued spans against #737 acceptance 1, which stays open under concurrency (#737)
- e180ba30 Say the LiteX union names the simulation or the leg, mark its repeated-simulation branch as defence in depth, refuse a boolean runner exit and a LiteX leg on a builder worker, and re-pin the leg runner (#737)

## Findings and changes (file:line at e180ba30)

| Finding | Item | Change |
|---|---|---|
| R768-1-F3 | 3 | `scripts/ci_gate_workflows.py:45-50` `BUILDER_CACHES` names the four shared caches (`Cache verified sv2v archive`, `Cache the pinned pip downloads`, `Cache the Scala toolchain`, `Cache the generated CPU metadata`). `:440-456` `builder_caches()` runs after `install_workflows` (which adds the sv2v cache) and before the runtime instrumentation (`:463`). Each builder worker (0, 1) and each LiteX worker (2 to 4) must carry each of the four exactly once, or generation is refused with `<job>: the builders' shared cache steps are missing or repeated`. It then removes them from workers 2 to 4, so they neither restore nor save them. Verilator's cache, the apt cache for its build, `Cache exact Python downloads` and the RV32 SDK cache are untouched. Template contract text: `.github/ci-templates/elaborate.yml:218-223` (at the CPU metadata cache) and `:344-348` (at the LiteX aggregate). Generated: `.github/workflows/elaborate.yml` loses 12 steps (4 on each LiteX worker), plus step-id renumbering; `ci_gate_workflows.py --check` rc 0. Tests: `scripts/ci_litex_legs_selftest.py:150-152` asserts that builders carry all four and LiteX workers none. `:162-175` `cache_controls()` plants a builder without its CPU metadata cache and a LiteX worker repeating it; both are refused by name (g13 log lines 184-185). Mutation: making `builder_caches` a no-op fails that assertion (receipts/m01-cache-drop-mutation.txt). Docs: `docs/testing/CI_WORKFLOWS.md:1689-1706` (mechanism, race evidence, Verilator kept, act trust set unchanged, per-run cost) and `:3141-3149` (why the LiteX projections hold). Not changed: `scripts/act_ci.py`, `scripts/ci_events.py`, `scripts/ci_tool_inventory.py` (receipts/g19). |
| R767-1-F2 | 4 | `docs/testing/CI_WORKFLOWS.md:3214-3226`: the 1745 s projection, like every one there, excludes runner queueing. Run 41583428850 did not meet #737 acceptance 1: measured from the first job start, gates-3 ended at 1882, `elaborate` at 2306 and `Collect CI manifest` at 2824. The cause was queueing (gates-3 waited 1268 s, the aggregate 388), beside docs, fast and full RTL workflows (full with 19 shards). Three legs add one concurrent runner per head, but queueing is account-level, so three legs are kept and acceptance 1 under concurrency stays open on #737. `:1677-1678`: the 973 budget sentence says "runner queueing excluded". The `LEG_BUDGET` comment already said so (`scripts/ci_litex_legs.py:53`). |
| R767-1-R1 | 5 | `docs/testing/CI_WORKFLOWS.md:1683` now reads "are each refused, naming the simulation or the leg" (exact text). The paragraph's lines are rewrapped (`:1683-1687`). |
| R768-1-S2 | 5 | APPLIED. `scripts/ci_litex_legs.py:171-172` comment: the `repeated` branch is defence in depth, reached only if the per-leg selection check is weakened. The manager noted it costs one comment. |
| R768-1-S3 (exit half) | 5 | APPLIED. `scripts/ci_litex_legs.py:165`: a receipt `exit` that is not an `int` (boolean `False`) is refused. Plant at `scripts/ci_litex_legs_selftest.py:90` ("a boolean runner exit", refused "LiteX leg 0: the runner exited False", g13 log line 266). Reason: it is in the same file whose pin is refreshed anyway, and it costs one comparison. |
| R768-1-S3 (`--only a,` half) | 5 | DECLINED. Reason: the fix is in `scripts/run_litex_sims.sh`, which would need a new content pin and image-table review for an input the generated step never produces (`ci_litex_legs.py` builds the `--only` list itself). |
| R767-1-S1 (disjoint workers) | 5 | APPLIED. `scripts/ci_gate_workflows.py:129-131`: generation is refused with `a LiteX leg shares a worker with a builder leg` when a LiteX worker is also a builder worker (the #737 failure shape, mutant S23). Plant at `scripts/ci_litex_legs_selftest.py:155-159` (`LITEX_WORKERS` patched to `(2, 3, 1)`, g13 log line 186). Docs `CI_WORKFLOWS.md:1665`. |
| R767-1-S1 (`--only` with three or more members; FAIL-row arm; name the extra simulation) | 5 | DECLINED. Reason: the first two are `run_litex_sims.sh --selftest` arms, and that script would need a new pin. Each mutant they target (S1, S5) is already refused by the runtime union and the aggregate verifier, naming the simulation. Naming the extra simulation would change a refusal message that R1's agreed text now describes accurately ("the simulation or the leg"). |
| R767-1-S1 (S21, the leg runner's exit) and R768-1-S1 (a sandbox arm through `run()`, the aggregate's `rglob`) | 5 | DECLINED. Reason: an offline arm needs a stub-interpreter sandbox around the real runner, which is new test infrastructure outside this round. Each mutant is refused at runtime by the union by name, and this round's real leg runs and verify controls (g09 to g11) exercise `run()` and the aggregate's collection end to end. |

## Item 3: per-run cost, and the LiteX projections with it

- Cost: no LiteX worker restores the four caches, so every LiteX run downloads the sv2v archive, the pip pins and sbt, and generates its CPU metadata cold. `test_ctrl_memory` takes 280 s with cold metadata, against about 110 s warm (100 to 113 s inside the old aggregate). That is about 170 s on worker 4 per run.
- Why the projections already carry it:
  - Every `SECONDS` value comes from run 41583428850's leg receipts, and no LiteX leg there had CPU metadata. Workers 2 and 4 missed the key. Worker 3 restored the 202-byte empty entry worker 2 had saved (receipts of [A727b], hosted/run-41583428850-cache-lines.txt).
  - The cold setups of workers 2 and 4 in that run were 94 and 131 s, with every download missed. Both are inside the one 143 s setup figure.
  - So 607 / 586 / 666 s (Verilator restored) is now each LiteX worker's warm case, and 1018 / 997 / 1077 s its cold case. No stated bound changes, as the STOP ruling expected.
- Builders: they now win the save race for their keys, so on a later run with the same key gates-0/1 should restore a non-empty `Cache the generated CPU metadata`. The manager's second hosted run is to show this; it is not shown here.
- ci_events `--selftest` arms fell from 5579 to 5507. The 72 missing arms are exactly the removed steps: 4 caches x (3 cache arms + 3 step arms) x 3 LiteX workers, with renumbering (receipts/g03-arm-diff.txt).
- The act sandbox still accepts the workflow (`validate_workflow_sandbox` returns None, receipts/g19). The trusted action set is unchanged.
- The tool-cache isolation windows still compute for all five workers (receipts/toolcache-windows.txt).

## Per-leg timing (measured and derived)

Partition (`python3 scripts/ci_litex_legs.py legs`, receipts/g05-litex-legs.log), unchanged from [A727b]:

| Leg | Worker | Members (hosted `SECONDS`) | Hosted leg s | Local leg command s (g06-g08) | Local per member s | Derived warm s (143+3+leg) | Derived cold s (+411) | Margin cold to 1620 / 1800 |
|---|---|---|---:|---:|---|---:|---:|---:|
| 0/3 | elaborate-gates-2 | gptp_tx_timestamp 461 | 461 | 528 | 527 | 607 | 1018 | 602 / 782 |
| 1/3 | elaborate-gates-3 | cpu_memory_port_cdc 70, gmii_rx_capture 0, pp_boot_bus_freeze 25, pp_mem_bridge 14, retained_cdc_storage 331 | 440 | 398 | 87, 1, 30, 14, 265 | 586 | 997 | 623 / 803 |
| 2/3 | elaborate-gates-4 | ctrl_memory 280, soc_timing_cuts 240 | 520 | 690 | 142, 548 | 666 | 1077 | 543 / 723 |

The local runs were made cold for CPU metadata, like a LiteX worker now. Before leg 0, the one generated metadata file in the scratch venv was moved aside, and before leg 2 none was present. Local differs from hosted: Python 3.14 (hosted 3.12), host Verilator 5.052 (hosted pinned 5.050), shared host, 16 CPUs. So local seconds are evidence that each member runs and passes once, not bounds. `test_soc_timing_cuts` took 548 s locally against 240 s hosted alone (355 to 534 s inside the old aggregate); [A727b]'s caveat stands that one hosted run defines `SECONDS`.

Hosted spans of run 41583428850 (from [A727b]'s receipts/hosted, first job start = 0): gates-2 end 587 (span 585), gates-4 end 1229 (span 1226), gates-0 end 1303 (span 1254), gates-1 end 1204 (span 1183), gates-3 queued 1268 and end 1885 (span 616), `elaborate` queued 388 and end 2309, manifest end 2827. Measured from the first job start as the ruling states: 1882 / 2306 / 2824.

Other workers: gates-0 projection 1475 (measured max 1254), gates-1 1240, builder leg 1 869 to 1119. Item 3 changes none of them: it removes steps only from workers 2 to 4.

## Item 6: union and dropped-simulation control (at e180ba30, real local receipts)

- g09 `ci_litex_legs.py union` over the three real receipts: `litex: 8 simulations exactly once, each a pass` (rc 0).
- g10a: `test_pp_boot_bus_freeze` dropped from leg 1's receipt. rc 1: `LiteX legs refused: LiteX leg 1 did not run its selection exactly once: test_pp_boot_bus_freeze`. g10b restored: rc 0.
- g11a: `ci_gate_receipts.py verify --workflow elaborate` (the aggregate's "Require every gate exactly once"). It uses the real LiteX receipts, production-recorded step receipts and stand-in builder receipts (receipts/verify_control.py, round 1's assembler; needs in receipts/g11-env.txt). rc 0: `elaborate: 5 source gates exactly once; all worker jobs successful`. g11b dropped: rc 1, `gate evidence refused: LiteX leg 1 did not run its selection exactly once: test_pp_boot_bus_freeze`. g11c restored: rc 0.
  - My first g11 attempt omitted `CI_GATE_NEEDS` and refused on the missing variable (a harness error). It was rerun under the same labels, so those rc files are the rerun's.
- Real leg receipts: receipts/litex-leg-{0,1,2}.json.

## Records touched

| Record | Touched | How / why |
|---|---|---|
| .github/workflows/elaborate.yml | yes | regenerated by `scripts/ci_gate_workflows.py`; `--check` rc 0 |
| ci/image/command-table.json:13614 | yes | `scripts/ci_litex_legs.py` re-pinned to d50df7b2... after reviewing the 2-line change. The other pins of this PR match the head blobs; `ci_gate_workflows.py` and `ci_litex_legs_selftest.py` are not pinned (receipts/pins-check.txt) |
| scripts/act_ci.py, scripts/ci_events.py, scripts/ci_tool_inventory.py | no | unchanged since 6a38c330 (receipts/g19); option (B) needs no trust-set change |
| ci/image/tool-inventory.json | no | names only workers 0 and 1 already, and is masked by unrelated drift, as round 1 states |
| docs/testing/TESTING.md | no | names no cache or timing figure |

## Gate table (at e180ba30; logs and rc in receipts/)

| Gate | rc | s |
|---|---:|---:|
| g01 python3 scripts/ci_gate_workflows.py --check | 0 | 0 |
| g02 python3 scripts/ci_events.py --check (2199 items) | 0 | 1 |
| g03 python3 scripts/ci_events.py --selftest (2199 items, 5507 arms; log 354 KB, see .ref) | 0 | 218 |
| g04 scripts/run_litex_sims.sh --selftest | 0 | 2 |
| g05 python3 scripts/ci_litex_legs.py legs (461 / 440 / 520) | 0 | 0 |
| g06 leg 0: `python3 scripts/ci_litex_legs.py run 0 --receipt <scratch>/litex-leg-0.json -- scripts/run_litex_sims.sh <scratch>/logs-0` | 0 | 528 |
| g07 leg 1 (same command, leg 1) | 0 | 398 |
| g08 leg 2 (same command, leg 2) | 0 | 690 |
| g09 ci_litex_legs.py union over the real receipts | 0 | 0 |
| g10a control: simulation dropped from leg 1 (expected refusal) | 1 | 0 |
| g10b control restored | 0 | 0 |
| g11a/b/c aggregate verify: real / dropped (expected refusal) / restored | 0 / 1 / 0 | 1 |
| g12 git diff --check e61a4afa HEAD | 0 | 0 |
| g13 python3 scripts/ci_gate_workflows_selftest.py | 0 | 15 |
| g14 python3 scripts/ci_litex_legs_selftest.py | 0 | 0 |
| g15 / g15b check_py_idiom.py and --selftest | 0 / 0 | 5 / 6 |
| g16 / g16b check_sh_idiom.py and --selftest | 0 / 0 | 0 / 0 |
| g17 cd tests && behave --no-capture -f plain (508 scenarios; log 235 KB, see .ref) | 0 | 4 |
| g18 python3 scripts/ci_scope.py --selftest | 0 | 27 |
| g19 act_ci.validate_workflow_sandbox(elaborate) accepts; act/events/inventory scripts unchanged | 0 | 0 |
| d05 d06 d07 d33 d36 d37 d40 d42 d47 d50 (docs workflow run steps that read the changed docs, template and scripts) | all 0 | 7/3/0/1/11/0/0/11/33/8 |

The docs workflow is unchanged since e61a4afa (`git diff e61a4afa HEAD -- .github/workflows/docs.yml .github/ci-templates/docs.yml` is empty), so round 1's extracted step bodies were reused (copied to scratch).
- d38 is exactly g02 + g03.
- d39 (`act_ci.py --selftest`) was not run on the host: the candidate's copy may run it only inside the CI job boundary.
- Python: the scratch copy of round 1's docs venv (CPython 3.14, PyYAML, behave). The LiteX legs used the scratch copy of round 1's LiteX venv, with the patch series already applied, and host sbt, Java and Verilator.

## Real limits

- The non-empty builder restore of `Cache the generated CPU metadata` can only be shown by the manager's second hosted run at the pushed head.
- On LiteX workers the step "Keep the generated CPU netlist arguments for the next run" still copies into a local directory that nothing saves. It is harmless, and removing it was outside "the four cache steps".
- Local leg seconds are not hosted bounds; see the timing note.
- Acceptance 1 under concurrency stays open on #737 (manager's decision).

REVIEW READY posted: issuecomment-6610087462 (head e180ba30eccc4ee7c3c699d88973816bdc953caa); text in receipts/review-ready.md
