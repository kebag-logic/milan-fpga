[A727c] REVIEW READY
Commit: e180ba30eccc4ee7c3c699d88973816bdc953caa (branch 737-elab-split, local; three commits over 6a38c330, one per item; PR #836 still shows aa3e2d85 until the maintainer publishes)
Changed:
- 0eb3f57e, item 3 (R768-1-F3, option (B)): `scripts/ci_gate_workflows.py` removes the four shared cache steps from `elaborate-gates-2` to `-4`: `Cache verified sv2v archive`, `Cache the pinned pip downloads`, `Cache the Scala toolchain` and `Cache the generated CPU metadata`. No restore and no save, so only the builders populate those keys. The LiteX workers keep the Verilator cache. Generation is refused unless every builder and LiteX worker carries each of the four exactly once first. The template contract text (`.github/ci-templates/elaborate.yml`, at the metadata cache and at the LiteX aggregate) says so, and the workflow is regenerated. The act runner's trusted action set is unchanged: `scripts/act_ci.py`, `scripts/ci_events.py` and `scripts/ci_tool_inventory.py` are untouched, and the act sandbox validation accepts the workflow. `docs/testing/CI_WORKFLOWS.md` states the per-run cost: every LiteX run generates its CPU metadata cold, so `test_ctrl_memory` takes 280 s against about 110 s warm. It also shows that the LiteX projections hold with that cost. Every member's seconds come from run 41583428850, where no LiteX leg had metadata, and the cold setups there (94 and 131 s) are inside the 143 s figure. So 607/586/666 s (Verilator restored) and 1018/997/1077 s (cold) stand.
- 39e3e00f, item 4 (R767-1-F2): the 1745 s projection excludes runner queueing. Run 41583428850's spans are recorded against #737 acceptance 1: `elaborate-gates-3` 1882 s, `elaborate` 2306 s, `Collect CI manifest` 2824 s, from the first job start. Queueing is named as the cause (gates-3 waited 1268 s, the aggregate 388 s). Three legs are kept, and acceptance 1 under concurrency stays open here.
- e180ba30, item 5: R767-1-R1's exact text ("are each refused, naming the simulation or the leg").
  - Applied: R768-1-S2 (defence-in-depth comment); the boolean-exit half of R768-1-S3 (refused, with a plant); the disjoint-worker assertion of R767-1-S1 (a LiteX leg on a builder worker is refused, with a plant). `ci_litex_legs.py` is re-pinned in `ci/image/command-table.json`.
  - Declined: the `run_litex_sims.sh` arms (R767-1-S1's three-member `--only` and FAIL row, R768-1-S3's trailing comma), because each needs a new content pin for that script and the runtime union refuses each by name. Also declined: an offline sandbox arm through `run()` (R768-1-S1, R767-1-S1's S21), which needs new stub-interpreter infrastructure; this round's real leg runs and verify controls exercise that path.
Validation (at e180ba30, 16 CPUs; each rc 0 unless noted):
- `python3 scripts/ci_gate_workflows.py --check`.
- `python3 scripts/ci_events.py --check`, and `--selftest` (2199 items, 5507 arms). That is 72 fewer than before, exactly the six arms of each of the 12 removed steps.
- `scripts/run_litex_sims.sh --selftest`; `ci_gate_workflows_selftest.py`; `ci_litex_legs_selftest.py`. Their new plants are refused: a builder without its metadata cache, a LiteX worker repeating it, a LiteX leg on a builder worker, a boolean exit. Making the cache removal a no-op fails the self-test.
- `python3 scripts/ci_litex_legs.py legs` gives 461 / 440 / 520.
- Each leg's own command, `python3 scripts/ci_litex_legs.py run N --receipt <dir>/litex-leg-N.json -- scripts/run_litex_sims.sh <dir>/logs-N`, run locally with cold CPU metadata. Each simulation PASS once:
  - leg 0, 528 s: `test_gptp_tx_timestamp` 527;
  - leg 1, 398 s: `test_cpu_memory_port_cdc` 87, `test_gmii_rx_capture` 1, `test_pp_boot_bus_freeze` 30, `test_pp_mem_bridge` 14, `test_retained_cdc_storage` 265;
  - leg 2, 690 s: `test_ctrl_memory` 142, `test_soc_timing_cuts` 548.
- `union` over the three real receipts: "litex: 8 simulations exactly once, each a pass".
- Control: `test_pp_boot_bus_freeze` dropped from leg 1's real receipt.
  - `union`: rc 1, "LiteX leg 1 did not run its selection exactly once: test_pp_boot_bus_freeze".
  - `scripts/ci_gate_receipts.py verify --workflow elaborate`: rc 1, "gate evidence refused: LiteX leg 1 did not run its selection exactly once: test_pp_boot_bus_freeze".
  - Restored, both pass.
- `ci_scope.py --selftest`; `check_py_idiom.py` and `check_sh_idiom.py` with their self-tests.
- The docs workflow's run steps that read the changed docs, template and scripts (link health, added-line em dash, concise audience, mechanical hygiene, Python and shell idiom, cited paths, per-page contents, CI scheduling and evidence controls, the no-git docs gates). The act runner self-test step was not run on the host.
- `cd tests && behave` (508 scenarios); `git diff --check e61a4afa HEAD`.
Acceptance criteria:
- #737 scope item 1 is met for the job timeout: the largest derived elaborate job is 1475 s against 2700 s.
- Every simulation runs exactly once and passes, proved by the union locally and by run 41583428850 hosted.
- No timeout is raised, no step is made conditional, and no simulation is dropped.
- Acceptance 1 (workflow inside 30 minutes) is met by the projection, runner queueing excluded. It was not met by run 41583428850 because of queueing, and under concurrency it stays open on #737.
Open risks/questions:
- Only the manager's second hosted run at the pushed head can show the non-empty `Cache the generated CPU metadata` restore on `elaborate-gates-0/1`.
- `SECONDS` comes from one hosted run.
- Local leg seconds come from a newer Python and Verilator on a shared host, so they are not bounds.
