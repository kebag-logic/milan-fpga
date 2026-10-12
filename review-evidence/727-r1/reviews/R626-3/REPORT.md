[R626] POSITIVE - exact head 2c2f336979e4fdb1da444f041f37551e2c9175df

Round R626-3 is the internal cleared-context review of issue #727 / PR #728. It is a full review at the exact head, plus the round-2 delta `a57d384d..61296ea1` and the round-3 delta `61296ea1..2c2f3369`.

- Head `2c2f336979e4fdb1da444f041f37551e2c9175df`, tree `4c0af06c96b3c3809b22f86d9280d50e603c3237`.
- Source base `c6bd08c6f52632c6d33d834ce842ac3cf63f29cc`, which equals live `dev`.
- Diff `c6bd08c6..2c2f3369`: `scripts/suite_shards.py` (+782/-78), `docs/testing/CI_WORKFLOWS.md` (+36/-19) and `docs/testing/TESTING.md` (+7/-3).
- Eleven commits, each one line with no trailers and none a merge (`receipts/commit_messages.txt`).
- Lenses applied: Conformance, RTL, Robustness, Tests, Docs.

**Verdict.** POSITIVE. No BLOCKER, MAJOR or MINOR is open at this head.

- One retained RESIDUE (R1, the `rtl.yml` comment routed to #495).
- Two new SUGGESTIONs (S1, S2).
- Every prior public finding is resolved or retained below.
- This source-review verdict does not discharge hosted acceptance 3 and does not authorize a merge.

## Context reconstructed

**Governing documents.** AGENTS.md, CONTRIBUTING.md (section 2 commits and lanes, section 3 verification bar), and `docs/README.md` (map: testing guide, CI workflow policy).

**Issue #727.**
- Body: acceptance 1-4.
- Lane assignment 6121794007, TAKEN 6121909841, REVIEW READY 6122246247.
- Round-2 decision 6126048117, REVIEW READY 6126250528.
- Round-3 decision 6126613714, REVIEW READY 6127235765.

**PR #728.** The body at the head was read. It is open, not a draft, base `dev`, `headRefOid` = the reviewed head.

**Authorities read.**
- `.github/workflows/rtl.yml`:
  - `:136-140`, the comment;
  - `:147-157`, `verilator-shards`: `timeout-minutes: 120`, `shard: [0, 1, 2, 3, 4]`, `total: [5]`;
  - `:208-223`, the ownership step;
  - `:364`, the physical job's self-test;
  - `:421`, `--expect 5`.
- `scripts/run_all_suites.sh`:
  - `:168-189`, selection;
  - `:245-253`, `suite_timeout`;
  - `:291-296`, the selector preflight;
  - `:390` and `:406-425`, the `shard:`, verdict and `suites:` lines;
  - `:447-457`, `main`.
- `scripts/ci_events.py`: `CANONICAL_OWNERSHIP_SCRIPT` `:1921-1933`, the canonical verifier `:2188-2196`, and the self-test fixtures `:5099-5345`.
- `scripts/test_suite_cancellation.py:87-89`.
- `scripts/suite_tally.py:398`.
- `scripts/measure_test_evidence.py:680,817`.
- `docs/testing/{CI_WORKFLOWS,TESTING,RUNNING_TESTS}.md`.
- `tb/verilator/milan_dp/README.md:442`.

**History.** `git diff c6bd08c6..2c2f3369` and its history were read, and the selector at head was read in full (`:1-948`).

**Public evidence.**
- `dfdd39ff:review-evidence/727-r1/author{,-r2,-r3}`: the directory listings, read for orientation only. Every figure in this report was re-derived by the reviewer.
- `reviews/R626-1/scripts/mutate.py`: sha256 `571bd0aa...fcfc031`, equal to its `MANIFEST.sha256` entry, run unmodified.
- The prior review findings on PR #728 (R626-1, R627-1, R626-2, R627-2) were read only after this round's independent pass over the diff, probes and walkthrough was complete.

**Hosted logs.**
- Fetched with the docstring's own commands: dev run 38217650945 (event `schedule`, head `c6bd08c6`, all five Verilator jobs `success`).
- #696 run 38208503834, job 114677344710 (head `26e2748f`, worker 1/5, cancelled at 120 min).
- PR run 38262957309 at the round-2 head `61296ea1` (same split).
- sha256 values are in `receipts/hosted_log_sha256.txt`.

## Prior public findings at this head

| Prior ID | Disposition at 2c2f3369 | Evidence |
|---|---|---|
| R626-1/F1 = R627-1-F1 (MINOR, Tests): no arm detects a change to the 60 % figure | RESOLVED | `scripts/suite_shards.py:723-730`. `expected = {minutes: minutes * 36 ...}` is computed without `bound_seconds` or `HEADROOM_PERCENT`, and compared with the bound each planted `rtl.yml` applied. At head: `{116: 4176, 117: 4212, 120: 4320}`. Under R626-1's `mutate.py` (driver copy added, see Tests), `headroom-75-percent`, `headroom-100-percent` and `bound-formula-div10` each give rc 1, and the only failure is that arm ESCAPED (5400 / 7200 / 43200 s at 120). `tree-head` gives rc 0. The reviewer's own `headroom-75`, `headroom-100`, `bound-formula-div10` and `bound-formula-hour` give the same result (`receipts/probe_r626_3.txt`). |
| R626-1/R1 = R627-1-R1 (RESIDUE): provenance sentence | RESOLVED | `docs/testing/CI_WORKFLOWS.md:192-194` names `maap`'s #696 pull-request run as the one exception. |
| R627-1-R2 (RESIDUE, PR body warm caches) | RESOLVED | PR body: "Overheads assume warm Verilator and Yosys caches; worker 1's overhead includes the tsn-gen build." |
| R626-1/R2 = R626-2/R1 (RESIDUE): `rtl.yml:136` "four hashed workers" | RETAINED as R1 below | The round-2 decision keeps `rtl.yml` byte-unchanged (acceptance 2) and routes it to #495. #495's checklist does not carry it yet. |
| R626-1/S1 = R626-2/S2 (SUGGESTION): `in_checkout()` forced False skips the head arms | RESOLVED | `:800-808`. A copy may skip only with none of `rtl.yml`, `tb/verilator` or the driver beside it. Under the mutant, both R626-1's `head-arms-skipped` and the reviewer's `in-checkout-forced-false` give rc 1 with `FAIL head: ... would skip its head arms ...`. `test_suite_cancellation.py` (the renamed-copy caller) still exits 0. |
| R626-1/S2 (SUGGESTION): zero duration and mirrored worker count | RESOLVED | `:704-707` and `:732-739`. The `zero-duration-allowed` and `worker-count-mirrored-5` mutants each give rc 1 with their arm ESCAPED. |
| R626-2/F1 (MINOR, Docs + Robustness): a new suite is refused, and the remedy the gate names cannot cure it | RESOLVED | The docstring new-suite steps are at `:54-87`, and the refusal at `:239-244` names them. TESTING.md `:513-519` states the precondition. The reviewer followed the steps word for word on a planted suite (see Conformance item 6). `--selftest`, `ci_events.py --check`/`--selftest` and the serial preflight all exit 0. |
| R626-2/S1 (SUGGESTION): determinism across processes | RESOLVED | `:863-881` `seeded_selftest`. The `tie-by-hash` (reviewer) and `nondeterministic-tie` (R626-1) mutants each give rc 1 with `FAIL the 5 --shard lists printed under hash seeds 1 and 2 ...`. |
| R626-2/R2 (RESIDUE, PR body line 36) | RESOLVED | PR body line 36 reads "The serial `0/1` selection needs no table and is unchanged; the sweep's preflight runs `--selftest`, which needs every suite in the table." |
| R627-2 | POSITIVE with no new finding | Nothing to resolve. Its retained items are the ones above. |

## Findings

### R1 - RESIDUE - Docs - `.github/workflows/rtl.yml:136-137` - comment still says "four hashed workers" (retained from R626-1/R2 = R626-2/R1)

**Evidence.** The hash rule is gone (`scripts/suite_shards.py:255-301`), but the comment still describes it. Acceptance 2 and the round-2 decision item 4 keep `rtl.yml` byte-unchanged in this PR, and route the comment to #495. Issue #495 (the residue checklist) does not list it yet.

**Impact.** Comment-only wording. No workflow key, command, figure, gate or verdict depends on it, and the executed configuration is correct.

**Exact fix.** Replace "four hashed workers" with "four workers balanced by measured hosted time (#727)".

**Verification.** A comment-only diff of `rtl.yml`, and `ci_events.py --check` exits 0. The manager carries it to #495.

### S1 - SUGGESTION - Docs - `scripts/suite_shards.py:63-82` (new-suite step 2) - the step that adds a worker does not name the documents that state the worker count

**Evidence.** Step 2 names every code pin that an added worker moves. Following it in the walkthrough left the following prose saying five workers, or naming shard 4/5 as `milan_dp`'s:

- `docs/testing/CI_WORKFLOWS.md:183-184`, `:206` and `:2320`;
- `docs/testing/TESTING.md:518`;
- `tb/verilator/milan_dp/README.md:442`.

`ci_events.py --check` still passed (1822 items; `receipts/new-suite-walkthrough/replay.txt`), so no gate reads that count from the prose.

**Impact.** A lane that follows step 2 literally can land a six-worker workflow with five-worker documentation. AGENTS.md section 5's general duty ("update authoritative documentation when behavior or architecture changes") already covers this, so it is optional.

**Option.** Add one bullet to step 2 naming those pages.

### S2 - SUGGESTION - Tests - `scripts/suite_shards.py:817`, `:821-826` - the head's `provisional_problems` call can be removed without any arm failing

**Evidence.** With `provisional = provisional_problems(driver)` replaced by `provisional = []`, the self-test exits 0 (`receipts/probe_r626_3.txt`, case `provisional-head-call-deleted`). The function itself is well covered: four planted arms at `:768-794` escape under each of the reviewer's four function mutants. At this head `PROVISIONAL_SUITES` is empty, so the head call checks nothing yet, and the executor already disclosed this.

**Impact.** A future change carrying a provisional figure other than `suite_timeout`'s would be caught only if the head call survives.

**Option.** Route the head check through a helper that the planted arms also call.

## Per-lens results

[R626] PASS Conformance - `scripts/suite_shards.py:128-205` (tables), `:255-301` (split), `:304-329` (rtl.yml reader), `:390-408` (gate), `:1-87` (docstring) at 2c2f3369. Receipts: `receipts/remeasure.txt`, `recheck_split.txt`, `refresh_verbatim_38217650945.out`, `lists/`, `serial_0of1_base_vs_head.txt`, `selftest_head.txt`, `selftest_head_py312.txt`, `assignment_across_rounds.txt`, `new-suite-walkthrough/`. `git diff --quiet c6bd08c6 HEAD -- .github` has rc 0. Checked against #727 acceptance 1, 2 and 4, assignment steps 1-5, round-2 items 1-4 and round-3 items 1-5:

1. **Every figure re-derives.** `remeasure.py` is the reviewer's own parser: Decimal timestamps, and it does not import the selector. On the five worker logs of dev run 38217650945 it reproduces all 62 `SUITE_SECONDS` entries and `WORKER_OVERHEAD_SECONDS = (83, 115, 80, 93, 80)` exactly, with `maap` taken from #696's job 114677344710.
   - The `maap` window is 06:40:57.0569333 to 07:03:51.2344068 = 1374.1774735 s, and ceil gives 1375. Dev's own window was 185 s, as the comment at `:128-131` says.
   - The issue's "about 1,380 s" is consistent with this window.
2. **The refresh procedure runs as written.** The docstring block at `:34-43` was extracted byte for byte and run (`receipts/refresh_verbatim.sh`, rc 0). Its `--measure` output equals the committed tables, except `maap` = 185, which the docstring holds back by design (`:50-52`).
3. **Deterministic, disjoint and complete.**
   - `--shard I/5 --list` gives 15, 16, 14, 16 and 1 suites.
   - Their union equals the 62-suite `--list` inventory, with no suite twice.
   - An independent re-implementation gives the same five lists: pins and the dedicated suite first, then longest first to the least-loaded worker, with lexical and lower-worker ties.
   - The lists are byte-identical to rounds 1 and 2, and so are the tables.
4. **Owners, bound and unchanged surfaces.**
   - 4/5 is exactly `milan_dp`, `tsn_fuzz` is in 1/5, and `chmap_capture` is in 3/5. These are the arms `rtl.yml:220-222` proves.
   - The predictions are 4204 / 4205 / 4203 / 4205 / 2877 s against 4320 s (60 % of `timeout-minutes: 120`, read from `rtl.yml`).
   - Under the old SHA-256 rule with the same table, worker 1/5 comes to 7504 s (125.1 min).
   - Five workers remain, and `rtl.yml` is unchanged.
   - The serial `--shard 0/1` and `--physical-gptp` selections hash identically to base (`cad83149...` and `db90def6...`).
5. **Acceptance 1's three fail-closed cases.**
   - A missing duration: planted suite, rc 1. `--shard 0/5 --list` gives rc 2.
   - A worker over 60 %: `timeout-minutes` 116 gives rc 1, and 117 gives rc 0.
   - Table/inventory disagreement: a removed suite gives rc 1.

   The `maap` 1375 s figure is in the prediction.
6. **Round 3: the new-suite steps work verbatim.** This was run in a disposable clone of the head with a planted `tb/verilator/zz_new_suite` (`receipts/new-suite-walkthrough/`; `new_suite_walkthrough.sh` replays it from `steps.diff`).
   - **Before step 1.** `--selftest` gives rc 1, and the refusal names the steps.
   - **Step 1.** `suite_timeout` has no own arm, so the provisional figure is 1800 s and the suite is named in `PROVISIONAL_SUITES`. `--selftest` prints `ok head provisional figures {'zz_new_suite': 1800}` and gives rc 1, with workers 0-3 at 4628-4730 s.
   - **Step 2, as worded.**
     - `rtl.yml`: matrix `shard` + 5, `total: [6]`, `--expect 6`, ownership arm `5)`.
     - `ci_events.py`: the canonical ownership script and verifier.
     - In its self-test, each asserted shard list gains index 5, and each asserted or planted Verilator count or index goes up by one, including the expected finding `--expect 4` becoming `--expect 5`.
     - In the selector: landmark `milan_dp: 5`, and overhead 115 inserted before the last.

     Result: `--selftest` rc 0 on CPython 3.14.7 and 3.12.13, with six workers at 3746-3747 s and 2877 s. `ci_events.py --check` rc 0 (1822 items), `--selftest` rc 0 (1822 items, 2530 arms).
   - **Lists.** The six lists cover the 63 suites once each, and 5/6 is `milan_dp` alone.
   - **Serial preflight.** All eight preflight gates pass (rc 0). This used a driver copy ending at `run_preflight_gates`, so no suite ran.
   - **Step 3** needs the change's own hosted run, and was not executed.

Round-2 and round-3 decision items are all met:

- the 36 s arm;
- the zero-duration and six-worker plants;
- the R1/R2 wording;
- docstring steps 1-3;
- the arm reading `suite_timeout` from the script (`:336-382`);
- the refusal naming the steps (`:239-244`);
- the TESTING.md precondition;
- the PR body line 36 fix;
- S1/S2 taken;
- `rtl.yml` unchanged.

[R626] PASS RTL - `git diff --quiet c6bd08c6 HEAD -- hdl tb .github syn` (rc 0) and gitlinks unchanged (`receipts/integrity_after_probes.txt`). Interface contracts examined at 2c2f3369: `scripts/run_all_suites.sh:168-189,291-296`, `scripts/suite_tally.py:398`, `scripts/measure_test_evidence.py:680,817`, `scripts/test_suite_cancellation.py:87-89`, `scripts/ci_events.py:1921-1933,2188-2196`, `.github/workflows/rtl.yml:208-223,364`.

- No HDL, testbench, workflow, synthesis or submodule artifact changed, so no clock, reset, CDC, width or FSM artifact is in scope.
- The selector's architecture and interface contracts hold:
  - one suite per line in lexical order;
  - `parser.error` (exit 2) on any selection error, which the driver turns into exit 2;
  - `sweep_suites`/`discover_suites` unchanged for the tally readers;
  - the `--selftest` command line that `ci_events.py` pins is unchanged;
  - `--physical-gptp` is unchanged.
- `ci_events.py --check` (1821 items) and `--selftest` (2530 arms) exit 0 at head.
- Resource and latency effects:
  - `--selftest` takes 0.7 s wall, including ten `--shard` subprocesses;
  - the hosted worker's ownership step runs it once before any suite.

[R626] PASS Robustness - `receipts/probe_r626_3.txt` (38 cases: 26 source mutants, 11 tree/table plantings, 1 head control), `receipts/r626-1-mutate-*.txt`, `receipts/new-suite-walkthrough/`, `receipts/drift_38262957309.txt`; `scripts/suite_shards.py:234-252,304-382,433-476,645-661,797-811` at 2c2f3369.

- Each of these fails closed (rc 1) with a named line:
  - an unmeasured suite, a removed suite, or a zero duration;
  - `gptp_plane` +500 s;
  - `timeout-minutes` 116, a second `timeout-minutes` in the job, an expression-valued timeout, or `total: [6]`;
  - a missing `rtl.yml`, or a missing driver;
  - a `suite_timeout` arm of another shape;
  - a provisional figure of 1799 s;
  - `in_checkout()` forced False in a checkout.
- These do not fail, and should not:
  - `timeout-minutes` 117;
  - a step-level `timeout-minutes`;
  - `maap` = 1380 (4207 s maximum).
- A sharded selection refuses a table/inventory disagreement with exit 2, while the serial 0/1 and physical selections need no table.
- `--measure` refuses a FAIL/TIMEOUT result, a log without a `shard:` line, and a short count. A truncated log measures its suites but gives no overhead.
- The driver's verdict and summary formats (`run_all_suites.sh:390,406-425`) match the reader's regexes.
- The head is deterministic across processes: `PYTHONHASHSEED` 1 and 2 subprocess lists equal the in-process selection.
- Configuration-dependent behavior: at six workers the pins, the dedicated worker and the bound all re-derive (walkthrough).

[R626] PASS Tests - `scripts/suite_shards.py:515-906` at 2c2f3369; `receipts/selftest_head.txt` (15 `[ok]` planted arms, 0 ESCAPED/FAIL, rc 0), `receipts/probe_r626_3.txt` (38/38 as expected), `receipts/r626-1-mutate-unmodified.txt` and `receipts/r626-1-mutate-driver-added.txt`, `receipts/head_gates.txt`.

- **Each assigned gate case has a control that escapes under its mutant.**
  - Missing duration made free: both the inventory arm and the sharded-selection arm are ESCAPED.
  - Stale check deleted: the stale arm is ESCAPED.
  - 60 % of `rtl.yml`'s timeout: the mirrored-120 mutant makes the 116-minute arm and the 36 s arm ESCAPED; the 75 %, 100 %, `//10` and `*60` mutants make the 36 s arm ESCAPED.
  - Planted heavy duration: `>=`, overhead dropped and mean-only each escape their arm.
- **Round 3's arm reads the script.**
  - With `driver_timeouts` mirrored to 1800, the `*`-arm-planted-at-1860 control is ESCAPED.
  - With named arms ignored, the own-arm-at-1920 control is ESCAPED.
  - With the comparison removed, all three escape.
  - When a name with no figure is let through, its arm is ESCAPED.
- **Pins, dedicated worker, determinism and the reader.**
  - Pins dropped or moved, the dedicated worker dropped, a tie-break by `hash` and the three `--measure` mutants each FAIL their arm.
- **R626-1's `mutate.py`.**
  - Run unmodified, 28 cases give rc 1 with `FAIL head: [Errno 2] ... run_all_suites.sh`, and one reports DRIFT. The round-3 selector reads the driver, and that harness predates it, so this is harness drift that fails closed.
  - With one added line copying the driver (`shutil.copy2(head / "scripts/run_all_suites.sh", ...)`), the round-2 required cases behave as required and `tree-head` gives rc 0.
  - Its `missing-duration-free` case reports DRIFT, because it targets the old refusal text. The reviewer's equivalent case covers it.
- **Head gates.** All exit 0 at head:
  - `ci_events.py --check`/`--selftest`, `test_suite_cancellation.py`, `suite_tally.py --selftest`;
  - `check_py_idiom.py`, `measure_naming.py --check`, `measure_fail_fast.py --check`, `check_hygiene.py --check`, `check_todo_ownership.py`, `measure_test_evidence.py --check`;
  - `git diff --check c6bd08c6 HEAD`.
- **Surviving mutants.** One tie-break mutant survives, and is equivalent in effect: equal predictions go to the higher worker, which is still deterministic. S2 is the other survivor.

[R626] PASS Docs - `docs/testing/CI_WORKFLOWS.md:183-215,325-331`, `docs/testing/TESTING.md:513-524`, and the `scripts/suite_shards.py:1-87` docstring at 2c2f3369. Also the PR #728 body, and `receipts/head_gates.txt` (docs gates).

- Each sentence was checked against the code:
  - the measured-time split and its longest-first rule;
  - the refusals of a missing and a stale duration;
  - the 60 % bound read from `rtl.yml`;
  - one dev run plus the `maap` exception;
  - the new-suite steps;
  - the pins, the dedicated worker and the ownership step;
  - the #621 history line, now in the past tense with #727's replacement.
- "104 minutes" for dev worker 1/5 matches its "Run this exhaustive suite shard" step, 07:26:47-09:11:07 = 104.3 min. The job itself took 105.1 min.
- TESTING.md's precondition matches `run_all_suites.sh:291-296` and `rtl.yml:213-214`.
- No obsolete document was restored.
- Docs gates at head, all rc 0:
  - `docs_check.py`;
  - `check_doc_style.py`;
  - `check_doc_paths.py`;
  - with the pinned renderer, `gen_toc.py --check` and `--verify-anchors`, `check_em_dash.py --base c6bd08c6` (0 findings over 43 added lines) and `--selftest`.
- R1 is retained RESIDUE and S1 is optional. Neither leaves this lens unclean.

## Reviewer-owned completion ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `scripts/suite_shards.py:1-205,255-408`; hosted logs of runs 38217650945 and 38208503834; `receipts/remeasure.txt`, `recheck_split.txt`, `refresh_verbatim_*`, `lists/`, `new-suite-walkthrough/` | R626-3 | 2c2f336979e4fdb1da444f041f37551e2c9175df |
| RTL | CLEAN | Full diff (no HDL/tb/workflow/syn/gitlink change); selector caller contracts in `run_all_suites.sh`, `suite_tally.py`, `measure_test_evidence.py`, `test_suite_cancellation.py`, `ci_events.py`, `rtl.yml` | R626-3 | 2c2f336979e4fdb1da444f041f37551e2c9175df |
| Robustness | CLEAN | `receipts/probe_r626_3.txt` (tree plantings and refusals), `r626-1-mutate-*.txt`, `new-suite-walkthrough/`, `drift_38262957309.txt` | R626-3 | 2c2f336979e4fdb1da444f041f37551e2c9175df |
| Tests | CLEAN | `scripts/suite_shards.py:515-906`; `receipts/selftest_head*.txt`, `probe_r626_3.txt`, `r626-1-mutate-*.txt`, `head_gates.txt` | R626-3 | 2c2f336979e4fdb1da444f041f37551e2c9175df |
| Docs | CLEAN (R1 RESIDUE retained, S1 optional) | `docs/testing/CI_WORKFLOWS.md:183-215,325-331`, `docs/testing/TESTING.md:513-524`, selector docstring, PR body; docs gates in `receipts/head_gates.txt` | R626-3 | 2c2f336979e4fdb1da444f041f37551e2c9175df |

## Real limits

- **No suite was run.** No Verilator suite, serial sweep past its preflight, Yosys run, `act` replica or hosted job was run by this review. The serial preflight was run only in the planted walkthrough clone, through a driver copy that stops at `run_preflight_gates`.
- **The table is one hosted sample.** It is one dev run plus #696's window. The four balanced workers keep 115-117 s (2.7 %) against 72 min.
  - Round-2 head PR run 38262957309 has the same split (`receipts/drift_38262957309.txt`):
    - worker 0/5 took 4230 s (70.5 min) against 4204 s predicted;
    - 2/5 took 4158 s (69.3 min);
    - 1/5 took 3066 s, because `maap` ran 187 s on this branch;
    - 4/5 took 3009 s (50.1 min) against 2877 s, with `milan_dp` +4.3 %.
  - Worker 3/5 of that run ended `failure` at 5706 s with the annotation "The hosted runner lost communication with the server". Its log is unavailable (HTTP 404), and its run step was still in progress, so neither its duration nor the cause can be attributed from public evidence.
- **Exact-head hosted evidence is incomplete.** At 2026-10-12T17:37Z, the exact-head run 38283356358 had all five Verilator workers in progress (`receipts/hosted_exact_head_snapshot.txt`).
- **The new-suite walkthrough covered steps 1-2 only.** Step 3 needs the change's own hosted run. The `ci_events.py` self-test edits followed the docstring's general wording. One planted stale denominator (`_m_shard_name_stale`, "3") was left unchanged and still passes.
- **Only the shared PyYAML was used.** CPython 3.14.7 (system) and 3.12.13 were used. The docs gates used an existing pinned-renderer environment (html5lib 1.1), with nothing installed.
- **No manager source bank** ran at this head, and none is claimed. Physical calibration was NOT RUN, and no hardware proof is implied.

## Pending manager duties

- **Hosted acceptance 3.** Every Verilator worker of the exact-head (or merge-candidate) rtl-full run must take at most 72 min, with predicted versus measured values per worker recorded on the PR. Worker 3/5's lost runner on run 38262957309 needs a measured re-run of that worker at this split.
- **Act replica and gates.** The `act` replica, exact-head `verilator-suites` / `yosys-portability`, and the current-dev merge-candidate validation (builder and native banks).
- **R1.** Carry R1 to the #495 checklist.
- **Reconciliation and merge.** Reconcile both independent ledgers (R627-3 is in flight), obtain explicit maintainer merge authorization, perform post-merge containment, and close #727 and move it to Done.

## Reproduction

The scripts are in this packet:

- `remeasure.py SELECTOR JOBS_META LOG... --extra-maap LOG`
- `recheck_split.py SELECTOR RTL_YML LISTDIR`
- `probe_r626_3.py CHECKOUT WORKDIR --jobs 16`
- `drift.py SELECTOR JOBS_META LOG...`
- `new_suite_walkthrough.sh CHECKOUT HEAD STEPS_DIFF WORKDIR`

After the probes, the review clone was verified at exact head (`receipts/integrity_after_probes.txt`):

- `write-tree` = `4c0af06c...`;
- worktree and index equal HEAD;
- all 1300 tracked blobs and modes match;
- gitlinks `third_party/verilog-axis` `48ff7a7e`, `protocol-processor` `2ad2f845`, `gptp-processor` `7dda9c3b` are at their pins.

R626-3 FINISHED
