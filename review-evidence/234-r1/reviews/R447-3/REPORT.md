[R447] NEGATIVE - exact head b5894838d6c47180ac4169e7d52dd746f461af21

# R447-3 external review: issue #234 / PR #638, round 3

- Head `b5894838d6c47180ac4169e7d52dd746f461af21`, tree `c2f454c490913470a1609bb66a9e82aa89c395a7`, source base dev `1269cdafb4bb964c757baae0f0c5a932d43f540b`.
- Round 3 is `0feff20f..b5894838`: 4 one-line commits, 6 files (the gate, its self-test and mutants, `pp_baseline_rank.py`, `AREA_BUDGET.md`, the recipe). There is no `hdl/` or gitlink change and no baseline-JSON change (`receipts/diff_scope.log`).
- **Verdict NEGATIVE: three MINOR findings are open.**
  - F1 and F2: the round's own contract, "any deviation exits 2 ... nothing reaches a traceback", still has two ways through. A baseline can still produce exit 1 by traceback.
  - F3: six refusals the round claims are not killed by any arm.
  - Every listed case from both round-2 reviews is resolved. Neither F1 nor F2 changes a real measurement's verdict: both fail closed with a non-zero exit. But each gives exit 1, the status reserved for a material regression, through a traceback on a baseline input.
- Lenses:
  - RTL is covered clean.
  - Conformance, Robustness and Docs are unclean under F1 and F2.
  - Tests is unclean under F1, F2 and F3.
- One RESIDUE: a packet file the PR body calls published is absent. I re-derived and digest-bound the figure it carries, so no figure is in doubt.
- My verdict and ledger were written without reading R446-3 (5969323709) or the archive commit `3ce83293`. I read the R446-2 and R447-2 findings only after my own pass over the round-3 diff.

## Inputs, in order

1. AGENTS.md and CONTRIBUTING.md (as loaded), and the docs map.
2. Issue #234's body and comments:
   - the lane assignment (5966260488);
   - the rulings (5967852698) and the owner decision (5967924270);
   - the round-2 assignment (5968015720);
   - the **round-3 assignment (5968718943)**;
   - round-3 REVIEW READY (5969184448).
3. `git diff 0feff20f..b5894838` in full, the commit history, and `git diff 1269cdaf..b5894838` by name. Then the PR body's Round 3 section and its 61-site self-audit table.
4. Public evidence:
   - `43ad8362:review-evidence/234-r1` (the round-1 records and run receipts);
   - the author round-3 packet at `6616a09d:review-evidence/234-r1/author-r3`, by path listing and the files named below;
   - the A/B measurement directories, read only.
5. Exact-head hosted check runs and the `yosys-elaboration` job log.
6. After my own pass: R447-2 (my round 2) and R446-2 (5968664092).

## Findings

```text
[R447] F1 MINOR Conformance, Robustness, Tests, Docs - syn/ooc/pp_resource_gate.py:394, :396, :430, :433, :494, :525, :538, :547 (shape_problems/load/check_baseline messages, main() print sites) and :357 (scope_deltas); docs/design/AREA_BUDGET.md:190; docs/testing/PP_SHADOW_BASELINE_RECIPE.md:456, :462; gate docstring :22-24 - a baseline string holding a JSON-escaped lone surrogate turns the validator's own refusal into exit 1 by traceback
Requirement/evidence: round-3 assignment item 1: "Any deviation exits 2 with a named reason, and nothing reaches a traceback." AREA_BUDGET.md:190: "Exit 2 always prints its reason, and no input reaches a traceback". The recipe at :456 says exit 1 is a material regression, "nothing else". Python's json module accepts the escape "\ud800" as a one-character string. The validator inserts endpoint names, unknown field names and scope names raw into its messages. main() then prints them to the real stdout, where a lone surrogate cannot be encoded. receipts/probe_text.log runs the real CLI as a subprocess against the real A route:
  - B: an unknown endpoint field named "\ud800". load() detects it, but printing the refusal raises: check rc 1 TRACEBACK UnicodeEncodeError; check-baseline rc 1 TRACEBACK.
  - C: an unknown file field named "\ud800": check rc 1 TRACEBACK; check-baseline rc 1 TRACEBACK.
  - A: an extra endpoint named "\ud800" (a copy of route-1x1): check rc 0; check-baseline rc 1 TRACEBACK where 2 is due ("only the baseline names it").
  - D: a sub-block scope named "\ud800" with valid counts: load() and check-baseline accept it (rc 0). check on A's real route crashes in scope_deltas' print: rc 1 TRACEBACK where the verdict was PASS.
  - E (control): an ordinary non-ASCII endpoint name "réroute" is refused normally, rc 2.
  The self-test cannot see this. Its cli() helper (pp_resource_gate_selftest.py:459-467) redirects stdout into an io.StringIO, which accepts surrogates.
Impact: an unusable baseline is reported with the material-regression status by traceback. That is the 1-versus-2 misrouting this round was assigned to close as a class. It fails closed, and no measured figure is misjudged. Triggering it needs an escape a hand edit or a tool could write. json.dumps writes exactly this escape for such a string, and the gate's own record --write uses json.dumps.
Required outcome: every message the gate prints is encodable for any string JSON can carry, for example names printed through repr()/ascii() or a stdout error handler. Alternatively, load() refuses a string that is not encodable. Either way, cases A to D exit 2 (A and D: check-baseline 2; D: check 0, or 2 if refused), never by traceback. An arm drives at least one case through a real stdout, a subprocess or an encoding-strict stream, with a killed mutant.
Verification: probe_text.py <checkout> <A route dir> <scratch> reports no TRACEBACK and no rc 1 in cases A to D; the control and E are unchanged.
```

```text
[R447] F2 MINOR Conformance, Robustness, Tests, Docs - syn/ooc/pp_resource_gate.py:362-367, :375-377, :406-407 (finite/number accept any int), :310-314 and :341 (judge/verdict_for subtract an int figure from a float); docs/design/AREA_BUDGET.md:195; docs/testing/PP_SHADOW_BASELINE_RECIPE.md:468 - a recorded timing figure written as a long integer literal passes load() and check-baseline, then crashes judge() with exit 1
Requirement/evidence: round-3 assignment item 1: "Every gated figure is a finite number"; "judge() runs only on a validated baseline"; nothing reaches a traceback. AREA_BUDGET.md:195: "NaN, Infinity or a number too large to be finite is not strict JSON here", and the recipe at :468 says the same. parse_float=finite refuses 1e400. The same JSON number written as the 401-digit integer literal 1000...0 goes through parse_int and is accepted. It is a finite int but not representable as a float. receipts/probe_bigint_B.log uses the real B route, whose inputs differ from the baseline's, so judge() runs:
  - control: check rc 1 (B's +625 LUT); check-baseline rc 0;
  - WNS_ns 1e400: rc 2 and rc 2 (refused as designed);
  - WNS_ns 10**400 as an integer literal: check rc 1 TRACEBACK OverflowError "int too large to convert to float"; check-baseline rc 0 "baseline PASS";
  - WHS_ns 10**400: the same.
  receipts/probe_bigint.log shows the A route never reaching judge() (identical inputs, refused rc 2), so the crash needs a candidate with changed inputs, which is every real use.
Impact: the hosted guard (check-baseline) accepts a baseline that the merge bank's check then reports as exit 1 by traceback, read as a material regression. It fails closed. This is the integer half of the overflow case the round closed only for decimals.
Required outcome: a recorded figure, tolerance, floor or ceiling that is not representable as a finite float is refused with exit 2 by load(), in both commands. One way is to bound ints or to check math.isfinite(float(value)) under an OverflowError guard. An arm and a killed mutant cover it.
Verification: probe_bigint.py <checkout> <B route dir> <scratch>: both 10**400 cases give rc 2 in both columns with no TRACEBACK; the control is unchanged.
```

```text
[R447] F3 MINOR Tests - syn/ooc/pp_resource_gate_selftest.py (ROUTE_ARMS, MALFORMED, AUDIT_ARMS); syn/ooc/pp_resource_gate_mutants.py - six refusals the round claims are made by correct code but killed by no arm
Requirement/evidence: round-2 item 4 and round-3 item 1: every claimed refusal has an arm and a killed mutant. receipts/extra_mutants_r3.log runs 13 reviewer mutants against the shipped 181-arm self-test. The control passes, 5 are killed and 8 survive. These six survive against a refusal the PR body or self-audit claims:
  1. "routing-error row may repeat": the PR body says the reader requires exactly one 'nets with routing errors' row, "anything else exits 2". There is an arm for an absent row, none for two rows.
  2. "undecodable route status escapes": the self-audit preamble says routing() maps ValueError, "a decoding error included", to exit 2. No arm plants a non-UTF-8 report.
  3. "undecodable budget page escapes": self-audit row 56 claims "OSError, ValueError -> a named problem, exit 2". Only the OSError path (an absent page) has an arm.
  4. "only TNS endpoints counted": the round-2 contract says a TNS or THS Total Endpoints of 0 exits 2. The "no timed endpoint" arm zeroes both columns, so dropping THS from the check survives.
  5. "standalone clock items unchecked": load() claims the identity's types and a "flow or standalone clock" list of text. Only flow has an arm.
  6. "identity may hold extra keys": load() claims "exactly the recorded keys". Only a missing key has an arm.
  At the head the code is correct for all six, and receipts/probe_gaps.log drives each through the real CLI:
  - duplicate error row: rc 2;
  - non-UTF-8 route status: rc 2;
  - non-UTF-8 budget page: check-baseline rc 2;
  - THS endpoints 0 with TNS 179432: rc 2;
  - standalone clock [5]: rc 2 in both commands;
  - an extra identity key: rc 2 in both commands.
Impact: a later edit can remove any of these six refusals with the hosted self-test and mutant campaign still green. The six are mostly at boundaries; no current verdict is wrong.
Required outcome: each of the six has an arm through main() and a shipped mutant that the self-test kills.
Verification: extra_mutants_r3.py <checkout> <scratch>: mutants 1 to 6 KILLED, control passes.
```

```text
[R447] RESIDUE R1 Docs - PR #638 body, Round 3 table row "R446-2 S3"; author packet 6616a09d:review-evidence/234-r1/author-r3 - "Published in the packet" names a file the archived packet does not hold
Evidence: the author's HANDOFF (author-r3/HANDOFF.md:484) and REVIEW READY receipt name `evidence/round3/armq-census.tsv`. The archived packet tree at 6616a09d (and at the later 3ce83293) holds no such path. The figure itself holds: receipts/armq_count.log counts armq_r FD* cells in each run's baseline_cells.tsv, A 1,153 and B 1,260 at 1x1, and each census sha256 equals the published 43ad8362 author/receipts/run-receipts.json.
Exact fix: either the manager adds `evidence/round3/armq-census.tsv` under review-evidence/234-r1/author-r3/, or the PR body row's evidence cell reads "Re-derivable: count armq_r FD* cells in each run's baseline_cells.tsv, whose sha256 is in 43ad8362 author/receipts/run-receipts.json (A 1,153, B 1,260)."
```

```text
[R447] SUGGESTION S1 Robustness - syn/ooc/pp_resource_gate.py:424 - duplicate JSON keys are accepted silently
The docs call the read "strict JSON", yet a duplicated key keeps its last value. receipts/probe_text.log case F: a first "LUT": 99999 ahead of the recorded tolerance gives rc 0 and rc 0. No verdict changes, because check-baseline pins the effective (last) policy value. But a reviewer reading a baseline diff may see the shadowed first copy. An object_pairs_hook that refuses duplicates would close it.
```

```text
[R447] SUGGESTION S2 Tests - pp_resource_gate.py:411, pp_baseline_rank.py:30 - two unclaimed edges have no arm
receipts/extra_mutants_r3.log: "bool scope counts accepted" and "hierarchy counts end early" survive. A JSON true as a scope count is refused today (type is int), but no arm says so. The hierarchy's other-script arms plant only the third cell. Neither changes a verdict, since scopes are reported, never gated, and a fullwidth digit has the same value.
```

## Prior findings at this head

| Prior finding | State at b5894838 | Evidence (this round) |
|---|---|---|
| R447-2 F1: contract not total (malformed record fields; superscript route count) | **RESOLVED for every listed case. The class is retained, narrowed, as F1 and F2.** | `receipts/reruns/r2_probe_contract.log`, unchanged: 13 edited cases each rc 2 in both columns, no traceback. The control keeps check rc 1 and check-baseline rc 0. In `r2_probe_route_real_A.log` the superscript count gives rc 2. Two traceback paths remain for baseline input (F1, F2). |
| R447-2 F2: absent net rows read complete | **RESOLVED** | `pp_resource_gate.py:277-281`. `r2_probe_route_real_A.log`: 15/15, with "both routable rows missing" at rc 2. `r2_probe_route_real_B.log`: 14/15; the 15th is B's own +625 LUT at rc 1, as in R447-2. Arms "without both net rows", "without its fully routed row" and "a second routable row" exist, and mutants "routable and routed rows present/single" and "fully routed row required" are killed (`receipts/gates/gate_mutants.log`). |
| R447-2 SUGGESTION: stale route status | **RESOLVED** | Recipe :459-460 states the risk and the fresh-directory rule. |
| R446-2 F1: route status without net rows | **RESOLVED** | As R447-2 F2. |
| R446-2 F2: policy pin proven for tolerances only | **RESOLVED** | Fixture floor 0.03 (`_selftest.py:29`, `:36`). There are arms for a floor cell, a ceiling cell, a JSON figure the table lacks, and a summary without its endpoint columns. Shipped mutants "budget comparison of every policy field", "budget comparison of baseline-only figures", "budget floors read" and "timed endpoint columns" are all killed. |
| R446-2 F3: malformed record fields exit 1 | **RESOLVED for its listed cases; the class continues as F1/F2** | Validator `load()` at `:421-434`, with 25 MALFORMED arms through both commands. The hosted job at the exact head logs each one (`receipts/hosted_gate_excerpt.log`). |
| R446-2 R1 | **RESOLVED** | AREA_BUDGET.md:170 carries the exact fix text. |
| R446-2 S1: wholly unrouted layout | Declined by the assignment; it fails closed (rc 2). No finding. | - |
| R446-2 S2: stale report | **RESOLVED** | Recipe :459-460. |
| R446-2 S3: B's `armq_r` census | **Figure verified; the file is absent from the packet (RESIDUE R1)** | `receipts/armq_count.log`. |
| R447-1 and R446-1 findings | Resolved at round 2; no regression | My round-1 probes, rerun unchanged (table below). |

## My round-1 and round-2 probes, rerun unchanged at this head

| Probe | rc | Result | Reading |
|---|---:|---|---|
| r1 `probe_cli.py` | 0 | 54 of 54 as documented | |
| r1 `extra_mutants.py` | 0 | 17 killed, 0 survived, 1 not unique | `baseline floor value` was re-indented when the policy checks lost their `try`. The shipped mutant of the same name is killed. |
| r1 `probe_route_status.py` | 0 | clean exit 2; 37 unrouted exit 2 | Its invented report has no net-count rows, which round 3 refuses by design (R447-2 F2's fix). |
| r1 `partition_check.py` | 0 | complete partition +79 / 391 / +93; `u_pp` -23 / +107 | Equals the prose. The trailing "documented:" line is fixed round-1 text. |
| r1 `replay_records.py` | 0 | A 0/0/0; B 1/0/0; 10 ns 2 | |
| r1 `check_tables.py` | 0 | 49 groups, 0 mismatches | |
| r2 `classify_mutants.py` | 0 | 96 ARM, 23 ESCAPED, 0 CRASH, 0 survived of 119 | It covers the 119 gate-file mutants; the 3 rank mutants are killed in the shipped campaign. Each ESCAPED mutant removes a refusal, so the escaped exception is the defect the arm's exit-2 contract names. |
| r2 `partition_r2.py` | 0 | 51 terms; +79/391 LUT; +93/121 FF; `u_pp` -23/+107 | |
| r2 `probe_contract.py` (A) | 0 | 13 of 13 cases rc 2 in both columns | |
| r2 `probe_policy.py` | 0 | 107 of 107 | |
| r2 `probe_route_real.py` A / B | 0 / 0 | 15/15; 14/15 | The B miss is B's own +625 LUT. |
| r2 `real_data.sh` | - | A 0, 0, 0; 10 ns 2; B 1, 0, 0 | `receipts/real/` |
| r2 `run_gates.sh` | - | 31 of 31 jobs rc 0 | `receipts/gates/`, GNU Make 4.3 first on PATH, built from the release tarball (sha256 e05fdde4...). |

## Clean lens and lens coverage

```text
[R447] PASS RTL - receipts/diff_scope.log (git diff --name-status 1269cdaf..b5894838: 15 files, 0 under hdl/, gitlinks 631eeb34 / 5dce647a / 48ff7a7e unchanged per receipts/restore_check.log); real A/B baseline_cells.tsv armq_r FD* counts 1,153 / 1,260 at 1x1, census digests equal to 43ad8362 run-receipts.json (receipts/armq_count.log) - no RTL, interface or clock/reset change to judge; the round's one RTL-facing claim (AREA_BUDGET.md:170, the processor top's +107 FFs are its timer-arm queues) holds in both measured netlists
```

These checks found nothing beyond F1 to F3:

- **Conformance:**
  - The acceptance criteria are unchanged from the rulings. Criterion 1 is met at 50 MHz (A +0.063/+0.036 ns, B +0.101/+0.036 ns).
  - Criterion 4's hosted half executed at the exact head: job 111203168912 `yosys-elaboration`, head_sha b5894838, success. It logs "181 arms PASS", "all 122 mutants fail" and "baseline PASS: 3 endpoints".
  - Real data through the head's CLI: A route, 1x1 and 8x8 rc 0, with "route status: complete". B route rc 1 (+625 LUT over 500). B 1x1 and 8x8 rc 0. The 10 ns control rc 2.
  - `judge()` is reached from `main()` only after `load()` (`:522`), `entry_problems()` (`:531-533`), `record()` and `routing()`.
- **Robustness:**
  - Count parsers: every report count goes through `[0-9]+` and the slack through `-?[0-9]+\.[0-9]+`. That covers utilization `:118`, timed endpoints `:140`, route status `:274`, hierarchy rank `:30` and budget cells `:476`, each with an other-script arm.
  - The three route-status rows are each required exactly once (`:277-281`; probes above).
  - The hierarchy change refuses a non-count row and is output-neutral on all seven real reports. `receipts/hier_compare.log`: the old (0feff20f) and new parsers give byte-identical `hierarchy()` and `ranking()` dumps on A route, A 1x1, A 1x1-10ns, A 8x8, B route, B 1x1 and B 8x8; 0 differ.
  - Self-audit spot checks against the code, all as tabled: rows 2, 8, 11, 17, 18, 21, 25, 35, 40, 46, 53, 59 and 61. The sites the table misses are print encoding (F1) and the implicit int-to-float conversion in `judge()` (F2).
- **Tests:**
  - Self-test 181 arms PASS; campaign 122 of 122 killed with the control passing (`receipts/gates/`).
  - The new arms assert reason text as well as status.
  - Gaps are F1 (no real-stdout arm), F2 and F3, plus S2.
- **Docs:**
  - AREA_BUDGET.md:189-196 and recipe :456-470 state the contract as designed. They are true except for "no input reaches a traceback" and the "too large to be finite" sentence (F1, F2).
  - The R1 wording, the stale-report note and the rank note (recipe :242) are correct.
  - `check-baseline` passes, and probe_policy is 107/107, so the policy table and JSON still agree.

## Ledger (reviewer-owned)

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1, F2) | Round-3 assignment 5968718943 items 1-5 against `pp_resource_gate.py:362-434, 506-548`; rulings 5967852698 / 5967924270; real A/B CLI runs (`receipts/real/`); `probe_text.log`, `probe_bigint*.log`; hosted job 111203168912 | R447-3 | `b5894838d6c47180ac4169e7d52dd746f461af21` |
| RTL | CLEAN | `diff_scope.log` (no hdl/ or gitlink change); gitlinks in `restore_check.log`; A/B `baseline_cells.tsv` armq_r counts with digests bound to run-receipts.json | R447-3 | `b5894838d6c47180ac4169e7d52dd746f461af21` |
| Robustness | UNCLEAN (F1, F2) | `pp_resource_gate.py:97-287, 362-503`; `pp_baseline_rank.py:22-45`; `probe_text`, `probe_bigint`, `probe_gaps`, `hier_compare` on 7 real reports; R1/R2 route and contract probes | R447-3 | `b5894838d6c47180ac4169e7d52dd746f461af21` |
| Tests | UNCLEAN (F1, F2, F3) | `pp_resource_gate_selftest.py` (181 arms, `cli()` :459-467); `pp_resource_gate_mutants.py` (122, classified 119); `extra_mutants_r3.log` (13 reviewer mutants, 8 survive); R1 `extra_mutants` 17/17 applicable | R447-3 | `b5894838d6c47180ac4169e7d52dd746f461af21` |
| Docs | UNCLEAN (F1, F2) | `AREA_BUDGET.md:170, 186-196`; recipe :242, :453-472; gate docstring :22-30; PR body Round 3 and its self-audit table; author-r3 packet tree | R447-3 | `b5894838d6c47180ac4169e7d52dd746f461af21` |

## Real limits

- No Vivado or Yosys run. The A/B directories (author run storage, not public) were read only: through the CLI, through symlink mirrors with one planted file, and by counting census rows. Their digests bind to the published run receipts.
- F1's trigger is a JSON escape, not a field failure seen in a real baseline. F2's trigger is a hand-written integer literal. Both are judged on the round's own contract wording, not on likelihood.
- The planted route-status and timing variants copy the real reports' layout. The duplicate-row and THS-zero layouts are synthetic.
- Not run, as instructed: full parent/PP/gPTP/Yosys/builder banks, act and `act_ci --selftest`, hardware.
- Hosted contexts as read (`receipts/hosted_check_runs.tsv`; time in `hosted_check_runs.read_at`):
  - Succeeded: rtl-fast, yosys-elaboration, docs-check-no-git, wire-accountability, full-ci-gate, bdd-conformance, verilator-lint, all four Yosys shards, and Verilator shards 0 and 3.
  - In progress: docs-check, elaborate, and Verilator shards 1, 2 and 4.
  - Not yet listed: the `verilator-suites` and `yosys-portability` aggregates.
  - Skipped: "Physical gPTP". A skip is not hardware proof.
- Physical calibration was NOT RUN. There is no bitstream, hardware or bench result.
- After the probes the clone is at the exact head: tree and index equal `c2f454c4`, 0 tracked changes, 0 untracked or ignored entries, the touched blobs and modes equal the index, and the gitlinks are as required (`receipts/restore_check.log`).

## Pending manager duties

- Hosted and act acceptance of the exact head, including docs-check, elaborate, the remaining Verilator shards and the two long aggregates.
- RESIDUE R1 to the residue checklist if it is not taken in a round.
- The Vivado comparison in the merge bank for any candidate that changes RTL, the processor pin or the build recipe (ruling (b)).
- Final current-dev candidate validation at the merge turn: source base `1269cdaf`, live dev `bbf704ec`.

R447-3 FINISHED
