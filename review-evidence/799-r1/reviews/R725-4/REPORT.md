[R725] NEGATIVE - exact head 9e57d4af1196a2e61f7e8010078c2c12b9b41587

Round R725-4 is the internal independent review of PR #802 (issues #799 and #790), at tree `0cf9e82356e81449b3db45acc0d0732c175097b2`. It is a delta review over `4f3ebffb`, the head where R725-3 and R726-2 were POSITIVE. The delta is three commits that carry out the option-B ruling on #799 (2026-10-28T21:30:38Z). Source base `97aab1d0`; live dev `5fcec84b`.

The verdict is NEGATIVE on one Docs MINOR.

- **F1 (MINOR, Docs).** `docs/testing/CI_WORKFLOWS.md:1504` still says the Verilator aggregate passes `--expect 17`. The delta regenerated `rtl.yml` to `--expect 19` and updated every other worker count on the page, but missed this line.
- Every ruling item the delta was checked against holds, each reproduced from my own data, not from the handoff:
  - **(1)** The 18th and 19th workers come from the planner and the generator. `ci_gate_workflows.py --check` returns rc 0, and a hand edit is refused.
  - **(2)** Every changed figure equals its largest hosted window. I downloaded the 34 job logs of the two PR runs and measured them with the head's own `--measure`; the output is byte-identical to the author's receipts. `follow_ring` 1493 s reproduces from dev run 40460559108. `media_phase` is kept at 1400 s.
  - **(3)** Every timeout, the 60 % bound, the 122 s allowance and every check are unchanged.
  - **(4)** The 81 units are each owned exactly once across shards 0..18.
  - **(5)** The module stays at 1000 lines, and `check_py_idiom` returns rc 0.
  - **(6)** The PR body names all four pre-existing growth suites, says `Closes #790`, and does not close #799.
- Two new RESIDUE items:
  - **R1.** The stated rule for which figures were replaced does not match the table: four replaced suites compile no changed source, and one reached suite was kept.
  - **R2.** A source comment uses ambiguous worker ordinals.
- One new optional SUGGESTION (S4).
- All prior open items are resolved or retained below.

## Delta scope

`git diff 4f3ebffb 9e57d4af --stat` (`receipts/delta_stat.txt`) lists five files:

- `.github/workflows/rtl.yml`, +18/-15, generated.
- `docs/testing/CI_WORKFLOWS.md`, +65/-41.
- `docs/testing/RUNNING_TESTS.md`, +2/-2.
- `docs/testing/TESTING.md`, +4/-4.
- `scripts/suite_shards.py`, +23/-23.

There is no `hdl/`, `tb/`, gitlink, contract or generator change. The brief said "no docs change". In fact the delta does change three `docs/testing` pages, all CI-schedule prose, and I reviewed them under Docs.

## Checks run at this head (reviewer-run, this clone, each rc the command's own)

| Check | Command | Result | Receipt |
|---|---|---|---|
| Planner selftest | `python3 -I scripts/suite_shards.py --selftest` | rc 0, `selftest: PASS`, 44 ok lines. Includes `rtl.yml at 20 workers is refused…`, the 1621 s refusal, and worker 18/19 at 1110 s (bound 2160 s) | `receipts/suite_shards_selftest.{log,rc}` |
| Workflow generator | `python3 scripts/ci_gate_workflows.py --check`; `ci_gate_workflows_selftest.py`; `ci_workflow_plan_selftest.py` | rc 0 each (`gate workflow and union controls: PASS`; `workflow planner: all controls pass`) | `receipts/ci_gate_workflows_*`, `receipts/ci_workflow_plan_selftest.*` |
| Event contract | `python3 scripts/ci_events.py --check`; `--selftest` | rc 0, 2199 items across 4 workflow files and CI_WORKFLOWS.md; selftest PASS, 5258 arms | `receipts/ci_events_*` |
| Python idiom ratchet | `python3 -I scripts/check_py_idiom.py`; `--selftest` | rc 0 (`long module: 10 <= 10`); selftest 54/54 PASS. `suite_shards.py` has 1000 lines at both heads | `receipts/check_py_idiom*` |
| Shard listing | `scripts/run_all_suites.sh --ci-pieces --shard i/19 --list`, i = 0..18 | rc 0 each | `receipts/list-*.{log,rc}` |
| Ownership | `scripts/ownership.py` (the 19 lists against the planner's own expanded inventory) | 81 listed, 81 distinct, 0 duplicate, 0 missing, 0 extra. tsn_fuzz on 1, chmap_capture on 3, worker 18 owns only `milan_dp_mclk__0`. Limits 45 x 18 + 60 on 18; bounds 1620 and 2160 s. `OWNERSHIP PASS` | `receipts/ownership.txt` |
| Hosted re-measurement | `scripts/measure_runs.sh` downloads the per-job logs (read-only) for the 17 Verilator jobs of each run and applies the head's `suite_shards.py --measure` | Per-run outputs byte-identical to the author's `measure-40724689169.txt` and `measure-40740015218.txt` (`diff` empty). The union is listed in the receipt | `receipts/measure-head-tool.txt`, `receipts/hosted/*` (job lists and log sha256) |
| follow_ring source | the same, dev run 40460559108 (schedule, `97aab1d0`, success) | `follow_ring` 1493 s; worker overheads at most 110 s, inside the 122 s allowance | `receipts/measure-dev-40460559108.txt` |
| follow_ring at PR RTL | shard-6 logs of both PR runs | follow_ring started after `aes3` and was cut at 1356 s (run 40740015218, 45-min timeout) and 475 s (run 40724689169, fail-fast cancel). No PR-run window exceeds 1493 s | `receipts/hosted/log-digests-*.sha256` |
| Capacity replay | `scripts/replay.py`: the head's balance at 19, charged with the union windows (table figure where there is none: follow_ring, pair_fill) plus 122 s | 0 of 19 workers at or over their limit. Maximum 2000 s (worker 7) against 2700 s. Workers 7, 9, 11 and 16 are above 1620 s because of mmcm_servo, aaf_clock_meter, crf_rx and avtp_rxmon. Equal, worker for worker, to the author's capacity replay | `receipts/replay.txt` |
| Doc arithmetic | the same script | Regular work 24693 s against 16 x 1498 = 23968 s. Placements: media_phase on 5, follow_ring alone on 0, gptp_tables on 3. The projection table (`CI_WORKFLOWS.md:3080-3098`) equals the planner's per-worker load for every worker | `receipts/replay.txt`, `receipts/ownership.txt` |
| Driver inventories | `ci_suite_pieces.inventory(s)` for the six parents | 24, 34, 43, 66, 3, 4, as `CI_WORKFLOWS.md:454-455` now states | `receipts/driver-inventory.txt` |
| Reach | `scripts/reach.sh . 97aab1d0 9e57d4af` (changed SV sources, parent and processor range, against non-comment Makefile lines) | See R1 | `receipts/reach.txt` |
| Mutation probes | `scripts/probes.sh` on a disposable copy | All 7 planted defects refused, 0 escapes (details below) | `receipts/probes.txt`, `receipts/probes/` |
| Restore | `git rev-parse`, porcelain including ignored files, `ls-files -s` digest against `ls-tree -r HEAD`, gitlinks | HEAD and tree as stated; 0 porcelain lines; index digest = HEAD-tree digest; worktree = HEAD. Gitlinks: processor `f65c8ff7`, gPTP `55680bff`, verilog-axis `48ff7a7e`, lwSRP `08ee86e8`, tsn-c-stack `70936b77`, external `efeb541a` | `receipts/restore_verify.txt` |

### Mutation probes (`receipts/probes.txt`)

| Probe | Planted defect | Gate | rc |
|---|---|---|---|
| p0 | none (control) | selftest, `--check` | 0, 0 |
| p1 | overhead table at 18, workflow left at 19 | selftest (`describes 18 workers; rtl.yml runs 19`), `--check` | 1, 1 |
| p2 | hand-edited `rtl.yml` total 20 | selftest, `--check` | 1, 1 |
| p3 | `milan_dp__0` 1429 -> 1499 | selftest (`worker 0/19 predicted 1621 s`) | 1 |
| p4 | regular timeout 45 -> 46 by hand | `--check` | 1 |
| p5 | 17 workers, regenerated | `--check` 0, selftest | 1 |
| p6 | 18 workers (option A), regenerated | `--check` 0, selftest (workers at 1625 and 1626 s) | 1 |
| p7 | allowance 122 -> 100 | selftest | 0 (see S4) |

p5 and p6 show that, at the replaced figures, option B is the smallest worker count the 1620 s rule accepts.

## Findings

### F1 - MINOR - Docs - `docs/testing/CI_WORKFLOWS.md:1504` - the stated Verilator `--expect` is still 17

- **Authority/evidence:**
  - The delta changes `.github/workflows/rtl.yml:622` from `ci_events.py --require-target-sha --expect 17` to `--expect 19` (`receipts/delta_planner_workflow.diff`).
  - The CI policy page still says the aggregates pass "`--expect` the worker matrix size (`--expect 17` for Verilator, `--expect 4` for Yosys)".
  - The same commit (`46cb8956`) updated every other worker count on the page: lines 450, 506, 526, 675 and 2453, and the `0/19` and `18/19` commands at `:3272-3273`. `ci_events.py --check` does not cover this sentence, so the gate passes.
  - AGENTS.md section 6, Docs: "Changed contracts are reflected in authoritative docs."
- **Impact:** The authoritative page misstates a verifier argument that this PR changed. A reader checking the aggregate's shard-count refusal against the page would expect 17 shards.
- **Required outcome:** The sentence names `--expect 19` for Verilator, or names the worker matrix size without a literal. No other 17-worker literal may remain in `docs/testing`.
- **Verification:** `grep -rnE -- '--expect 17|[0-9]+/17\b|seventeen' docs/testing` returns only the historical lines (`CI_WORKFLOWS.md:471` and `:559` for #781, `:480` for run 40740015218's worker 6/17) and the unrelated `TESTING.md:405` count of milan_dp commands. `ci_events.py --check` stays rc 0.

### R1 - RESIDUE - Docs, Conformance - `scripts/suite_shards.py:76-77`, `docs/testing/CI_WORKFLOWS.md:479-484`, PR #802 body ("Status" and "Figures") - the stated selection rule does not match the replaced set

- **Authority/evidence:**
  - All three places describe the replaced figures by the same rule: "suites the f65c8ff7 processor adoption reaches"; "Every figure of a suite whose Makefile compiles a source the adoption changes"; "Each figure this PR's RTL reaches".
  - The changed SV sources are `KL_aaf_packetizer`, `KL_pp_shadow`, `KL_mbx(_pkg)`, `milan_datapath`, `tb_mbx_top`, and processor `KL_acmp_talker`, `KL_srp_talker_fsm` and `protocol_processor_top` (`receipts/reach.txt`). Against them:
    - `maap` (`KL_maap.sv` only), `csr` (`milan_csr.sv` and generated includes), `nvm_backend` (`KL_nvm_backend.sv`, sizer) and `nvm_cosim` (processor NVM and ACMP-shadow files only) compile none of these. Their figures were replaced anyway.
    - `milan_dp_gm_steps` builds `$(MAKE) -C ../milan_dp gmstep`, whose `$(SRCS)` includes `DP_SRC = milan_datapath.sv` (`tb/verilator/milan_dp/Makefile:132,235,488-490`). It is reached, but keeps 926 s against a largest PR-run window of 696 s.
  - The table equals, entry for entry, the replay set in the STOP comment, which the ruling adopts ("exactly as your replay did"). Every value is a real hosted window, and the kept `milan_dp_gm_steps` figure is the conservative one. So the figures are right; only the rule that describes them is inexact. The `CI_WORKFLOWS.md:479` claim that the adoption "lengthens the suites its sources reach" is also loose, since `mbx` went down (82 -> 73).
- **Impact:** A later re-measurement that follows the stated rule would replace a different set of figures. A reader would also infer that `maap`, `csr`, `nvm_backend` and `nvm_cosim` are reached by this PR's RTL.
- **Required outcome (exact fix):** In all three places, describe the set as what it is:
  - Proposed wording: "the suites of the ruled #799 replay: those whose Makefile compiles a source this PR changes, plus `maap`, `csr`, `nvm_backend` and `nvm_cosim`, re-measured in the same runs. `media_phase` keeps 1400 s, and `milan_dp_gm_steps` keeps its higher 926 s."
  - In the source comment, the shortest faithful form is: "#799: the ruled replay set (see CI_WORKFLOWS.md), except media_phase, carries its largest window in runs 40724689169 and 40740015218; follow_ring 1493 s, dev run 40460559108."
  - Replace "lengthens the suites its sources reach" with "changes the windows of the suites its sources reach".
- **Verification:** Read the three places against `receipts/reach.txt`. `check_py_idiom` stays rc 0, and the module stays at 1000 lines (a one-line comment swap).
- **Note:** Whether `milan_dp_gm_steps` should drop to 696 s is a figure decision, not wording. The ruling's two phrases ("every recorded figure this PR's RTL reaches" and "exactly as your replay did") disagree only on that suite. Keeping it is conservative and needs no change; it is listed under pending duties for the manager to confirm.

### R2 - RESIDUE - Docs - `scripts/suite_shards.py:154` - ambiguous worker ordinals in the allowance comment

- **Authority/evidence:** "#781 and #799 add workers 17 to 19 at the regular 45-minute limit and 122 s allowance." The 19th worker, index 18 (`rtl.yml:144`, `matrix.shard == 18 && 60 || 45`), is the dedicated media-clock worker at 60 minutes. What #781 and #799 added was regular capacity; the dedicated worker moved to the end.
- **Impact:** Read literally, the comment puts the dedicated worker at a 45-minute limit.
- **Required outcome (exact fix):** "#781 and #799 add three regular workers at the 45-minute limit; every worker, the dedicated last one included, carries the 122 s allowance."
- **Verification:** The comment matches `rtl.yml:144`. `check_py_idiom` stays rc 0, and the line count is unchanged.

### S4 - SUGGESTION - Tests - `scripts/suite_shards.py:155` (allowance), selftest - the 122 s allowance is not tied to measured overhead

Probe p7 lowers the allowance to 100 s and the selftest still passes. Measured worker overheads reach 110 s on dev run 40460559108 (`receipts/measure-dev-40460559108.txt`), so 100 s would understate them. The delta does not change the allowance, so this is optional and pre-existing. An arm could compare `WORKER_OVERHEAD_SECONDS` with the archived `--measure` overhead line.

## Prior public findings at this head

| ID | Origin | Severity, lenses | Status at 9e57d4af |
|---|---|---|---|
| F1, F2 | R725-1/R726-1, R725-2 | MINOR, Docs | **Still resolved.** `docs/design/` and `sw/mailbox/` are not in the delta. |
| R1, R2 (prior) | R725-1, R726-1 | RESIDUE | **Still resolved.** No issue-comment ID was added in the delta's source comments. The PR body says `Closes #790`. |
| R3 / RES-1 | R725-3, R726-2 | RESIDUE, Docs | **Retained, carried to the residue checklist.** `sw/mailbox/mailbox.yaml:65` is still 105 columns. The file is not in the delta. |
| RES-2 | R726-2 | RESIDUE, Docs | **Resolved.** The PR body "Status" and the reproduction "expected state" name `9e57d4af1196a2e61f7e8010078c2c12b9b41587`. |
| S1 | R725-1, R726-1 | SUGGESTION, Tests | **Retained, optional.** `tb/` is not in the delta. |
| S2 | R725-2 | SUGGESTION, Docs | **Superseded by R3/RES-1.** |
| S3 | R726-2 | SUGGESTION, Docs | **Retained, optional.** `docs/design/MAILBOX_SPLIT.md:817` is unchanged. |

## Comment rule (delta source comments)

The new comments are at `suite_shards.py:9`, `:22`, `:76-77`, `:154` and `:159-160`. They carry issue IDs (#781, #799, #804), hosted run IDs and the commit `f65c8ff7`. None shows a bench lane label, a lane name, a review round, a reviewer ID or an issue-comment ID. The PR body cites `issuecomment-6460917634`, which PR text is allowed to do.

## Lenses applied this round

- **Conformance: CLEAN.**
  - Ruling items (1) to (6) were checked as listed in the summary, each reproduced from my own data (the table and receipts above).
  - The PR body contains "Relates to #799" and "Closes #790", the title says "closes #790", and it explains why #799 stays open. The Known limitations section names `mmcm_servo`, `aaf_clock_meter`, `crf_rx` and `avtp_rxmon`.
  - R1 is wording only.
- **RTL: CLEAN.**
  - `receipts/delta_stat.txt`: no `hdl/`, `tb/` or gitlink entry.
  - The scheduling effects are understood: the 60-minute arm moved with the dedicated worker from shard 16 to shard 18 (`rtl.yml:144`), and the regular arm stays at 45.
  - Prior RTL coverage (R725-3 and R726-2 at `4f3ebffb`, R726-1 at `ca39dc1b`) stands, because nothing in its scope changed.
- **Robustness: CLEAN.**
  - Timeout and failure paths:
    - 0 of 19 workers reach their limit at measured windows.
    - The PR runs' partial follow_ring windows (1356 s and 475 s) stay under the 1493 s figure, and worker 0 holds follow_ring alone.
    - The 1621 s boundary, the 17- and 18-worker configurations, a hand-edited count and a hand-edited timeout are all refused (p1 to p6).
  - The four above-budget replays are pre-existing and disclosed.
- **Tests: CLEAN.**
  - The planner, generator, plan, event and idiom selftests are all rc 0.
  - Each delta-relevant arm can fail for the defect it claims to catch (p1 to p6).
  - The ownership proof covers all 81 units.
  - S4 is optional.
- **Docs: UNCLEAN.**
  - F1 is open.
  - Otherwise the three pages were checked against the planner: the projection table, the margins, 24693 against 23968, the placements, the driver counts, 988 and 1110 s, and the run IDs.
  - R1 and R2 are residue.

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `scripts/suite_shards.py:76-168` against `receipts/measure-head-tool.txt` and `measure-dev-40460559108.txt`; `ci_gate_workflows.py --check`; `receipts/ownership.txt`; `receipts/delta_planner_workflow.diff` (timeouts, 60 %, 122 s); PR #802 body (closing refs, Known limitations) | R725-4 | `9e57d4af1196a2e61f7e8010078c2c12b9b41587` |
| RTL | CLEAN | `receipts/delta_stat.txt` (no `hdl/`, `tb/` or gitlink); `rtl.yml:144` timeout arm; prior R725-3/R726-2 coverage at ancestor `4f3ebffb`, nothing in scope touched since | R725-4 (R725-3 at `4f3ebffb` stands) | `9e57d4af1196a2e61f7e8010078c2c12b9b41587` |
| Robustness | CLEAN | `receipts/replay.txt` (0 at limit), shard-6 hosted logs (`receipts/hosted/`), `receipts/probes.txt` p1-p6, dev overhead line | R725-4 | `9e57d4af1196a2e61f7e8010078c2c12b9b41587` |
| Tests | CLEAN | `receipts/suite_shards_selftest.log`, `ci_gate_workflows_selftest`, `ci_workflow_plan_selftest`, `ci_events_selftest`, `check_py_idiom_selftest`, `receipts/probes.txt` and `receipts/probes/` | R725-4 | `9e57d4af1196a2e61f7e8010078c2c12b9b41587` |
| Docs | UNCLEAN (F1) | `docs/testing/CI_WORKFLOWS.md:449-506, 513-527, 675, 1504, 2453, 3079-3105, 3271-3274`; `RUNNING_TESTS.md:89-95`; `TESTING.md:541-557`; PR #802 body; `receipts/driver-inventory.txt`, `receipts/reach.txt` | R725-4 | `9e57d4af1196a2e61f7e8010078c2c12b9b41587` |

## Real limits

- I ran no Verilator suite, sweep, docs workflow or `behave` at this head. The delta changes no simulated source; the author's docs-gate and `behave` receipts are the source-head evidence for those. I did run the generator, event, idiom and planner gates.
- Hosted runs at this head (rtl-fast 40782764992, rtl-full 40782764988, docs 40782764951, elaborate 40782764934) were still queued or in progress when I checked. I claim no hosted result at this head.
- `follow_ring` has no complete window at the PR's RTL. Its 1493 s figure is from dev, and the PR runs give only lower bounds (at most 1356 s).
- The re-measurement uses the per-job log API, rewritten to the `gh run view --log` line shape. The windows are byte-identical to the author's receipts, but both come from the same hosted logs.
- The reach mapping uses non-comment Makefile source names plus one checked delegation (`milan_dp_gm_steps`). It is not a full include-graph extraction.
- No manager source bank exists at this head, and none is claimed. Physical calibration was NOT RUN, and field skips are not hardware proof.

## Pending manager duties

- Hosted and act acceptance at this exact head, especially that rtl-full's 19 Verilator workers finish under their limits.
- The current-dev merge candidate (builder and native banks) at the merge turn, from live dev `5fcec84b`.
- Carry R1, R2 and R3/RES-1 to the residue checklist.
- Confirm that keeping `milan_dp_gm_steps` at 926 s is intended (R1 note).
- Route F1 to the executor.
- The pre-existing figure growth (`mmcm_servo`, `aaf_clock_meter`, `crf_rx`, `avtp_rxmon`) and #804 stay outside this PR, as ruled. The PR recommends a re-measurement issue, which the manager owns.

R725-4 FINISHED
