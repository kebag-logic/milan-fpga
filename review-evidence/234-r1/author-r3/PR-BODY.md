[A516]

## Contents

- **[Status](#status)** -- Green/WIP/blocked, test tally, and `branch` -> `dev`.
- **[Linked Issue / roles](#linked-issue--roles)** -- Public task, executor, and independent reviewers.
- **[Description](#description)** -- What changed and why.
- **[Round 2](#round-2)** -- Each R446-1 and R447-1 finding, what answers it and the evidence.
- **[Round 3](#round-3)** -- Each R446-2 and R447-2 finding, the one baseline validator, ASCII counts, and the self-audit of every read.
- **[Authoritative references](#authoritative-references)** -- Requirements/specification clauses and docs.
- **[How to get into the same state](#how-to-get-into-the-same-state)** -- Copy-pasteable checkout/dependency/environment commands.
- **[How to validate](#how-to-validate)** -- Exact reviewer commands and expected result.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** -- What this deliberately does not do, and why.
- **[Definition of Done](#definition-of-done)** -- The merge bar from [CONTRIBUTING.md](../CONTRIBUTING.md).

## Status

REVIEW READY, round 3: 43/43 touched local gates rc 0 under GNU Make 4.3; gate self-test 181 arms, 122/122 shipped mutants killed; every probe both reviewers published in rounds 1 and 2 rerun unchanged, results tabled below -- `234-area-baseline` -> `dev`. Head `b5894838d6c47180ac4169e7d52dd746f461af21` (four commits on round 2's `0feff20f`). No RTL, processor or interface change; no Vivado run in rounds 2 or 3.

## Linked Issue / roles

Relates to #234
Relates to #229

Executor: `[A516]`
Internal cleared-context reviewer: `[R446]`
External reviewer: `[R447]`

## Description

Issue #234's first step under epic #229: the authoritative baseline, the 1x1 ranking, the budget and a resource-regression gate.

| Piece | Change |
|---|---|
| `docs/findings/234_PP_SHADOW_AREA_BASELINE.md` | New. Vivado baseline of the current head (A: dev `1269cdaf`, processor `631eeb34`) and of the next adoption (B: processor `ddb3119d` with the C8 and P2 parent patches, a scratch tree). Integrated 1x1 route, standalone 1x1 and 8x8 synthesis at the build's 50 MHz clock, per-sub-block LUT/FF/RAMB/DSP/CARRY4, storage mapping with source lines, Yosys reconciliation, the 1x1 reduction ranking and run receipts. Round 2: B's standalone movement on one named partition, A's route status recorded as clean, the lever issues #230 and #639. |
| `docs/design/AREA_BUDGET.md` | New section: NFR-RES-01's 60 % LUT target against the measured image, the owner's 2026-10-03 decision, the gate's policy table and where it runs. Contents separator switched to `--` (CONTRIBUTING 6.1). |
| `syn/ooc/pp_resource_gate.py`, `_selftest.py`, `_mutants.py` | New gate. Reads one recipe measurement directory into a record (identity, input digest, figures, sub-blocks) and judges it against the recorded baseline. `check` exits 0 within tolerance; 1 for a material regression only, an incomplete route included; 2 for every input it cannot judge (not comparable, an unreadable measurement, an unusable baseline), always with its reason; no input reaches a traceback. `check` and `check-baseline` both read the baseline file through one validator first: strict JSON (no `NaN`, `Infinity` or overflowing number), then every field of the recorded shape. Every report count is read as ASCII digits. `check-baseline` exits 0 or 2 and holds every endpoint's policy to the budget's policy table. 181 planted arms; 122 enforcement-removal mutants, each killed. |
| `syn/ooc/pp_baseline_rank.py` | Round 3: the hierarchy parser the gate reads sub-blocks through skips only the column-head row and refuses any other table row whose counts are not ASCII digits (it used to skip such a row silently). Identical output on all seven real reports. |
| `syn/ooc/pp_resource_baseline.json` | New. A's three endpoints (`route-1x1`, `ooc-1x1`, `ooc-8x8`), written only by `record --write`, plus policy (tolerances about 1 %, zero for RAMB/DSP, WNS at least +0.030 ns and WHS at least 0, 121.5-tile BRAM ceiling). Unchanged in round 2. |
| `syn/ooc/pp_baseline.py`, `pp_baseline_mutants.py` | `--integrated-clock`: the standalone clock from the bound `CLK_HZ_P` instead of the fixed 10 ns (default unchanged); one self-test function and four killed mutants. |
| `docs/testing/PP_SHADOW_BASELINE_RECIPE.md` | The new flag, the elaboration route to 8x8 parameters, and the gate commands and exit-code contract. Round 3: the route status report has no header and is read from the run directory, so each measurement uses a fresh directory (the bank deletes nothing). |
| `.github/workflows/rtl-fast.yml`, `scripts/ci_events.py` | The gate's self-test, mutants and `check-baseline` join the existing OOC step; the pinned step list moves with them. No new job, runner or tool. |
| `scripts/ci_scope.py`, `docs/testing/CI_WORKFLOWS.md` | Round 2: the gate now reads `docs/design/AREA_BUDGET.md`, so the classifier files it as gate-read (its self-test derives that list and refused the change until it was added). A change to the budget page alone runs the step that checks it. |
| `docs/findings/README.md` | Round 2: indexes `234_PP_SHADOW_AREA_BASELINE.md` and `PP_SHADOW_BASELINE.md`. |

Headline figures (A / B):

| Measurement (A / B) | LUT | FF | Slice | RAMB36 / RAMB18 | DSP | CARRY4 | WNS / WHS ns |
|---|---:|---:|---:|---:|---:|---:|---:|
| Shipping route, whole image | 50,128 / 50,753 | 59,006 / 59,014 | 15,815 / 15,827 | 79 / 27 both | 14 | 3,405 / 3,423 | +0.063 / +0.036; +0.101 / +0.036 |
| Standalone wrapper 1x1, 20 ns | 24,343 / 24,505 | 25,344 / 25,470 | - | 21 / 3 both | 8 | 1,623 / 1,638 | estimate only |
| Standalone wrapper 8x8, 20 ns | 31,562 / 31,390 | 33,929 / 33,844 | - | 26 / 5 both | 8 | 2,001 / 2,016 | estimate only |

The image uses 79.07 % of the LUTs and 99.78 % of the slices (35 free). Two buffers still spill into flops at 1x1: the notification registry (2,048 FF, against its own distributed-RAM attribute) and the SRP timer-arm FIFOs (2,304 FF). Ranked levers (registry, SRP FIFOs, timer-arm queues, #230 sharing, throttle stamps) estimate about 5,600 FF and 3,600 LUT; #233 is not needed for placement headroom.

Gate on real data at this head: A's three endpoints exit 0, and A's route status reads complete (105,566 of 105,566 routable nets fully routed, 0 nets with routing errors). B exits 1 on the route (+625 LUT over the 500-LUT tolerance; 366 of them outside the wrapper, where no RTL changed; its route status is complete too) and 0 on both standalone endpoints (+162 / -172 LUT). A's 1x1 control at 10 ns exits 2 (standalone clock identity).

Decisions (manager rulings 5967852698 and the owner decision 5967924270 on #234):

1. NFR-RES-01 (at most 60 % LUT) is 12,088 LUT short at dev; #229's 30 % non-CPU milestone is exceeded by the wrapper alone. The 121.5-tile ceiling and the gate tolerances are accepted as working policy (manager ruling). The allocation went to the owner, who ruled on 2026-10-03: NFR-RES-01 stays at 60 %, met by a redesign in milestone "Optimisations Mark II" (#640) after Instrument verification; until then the gate holds every resource at its recorded value.
2. Criterion 1 is judged at the declared 50 MHz shipping clock and is met (manager ruling).
3. The Vivado half of the gate runs in the manager's merge bank for every PR that changes RTL, the processor pin or the build recipe (manager ruling).
4. The next adoption needs a reviewed re-baseline of the route, and two `syn/yosys/rom_digests.tsv` rows for `ddb3119d` that its patches do not carry.
5. The child issues are #232 (levers 1 and 5), #230 (levers 4 and 2) and #639 (levers 3 and 6), in that order (manager ruling).

## Round 2

The round answers R446-1 and R447-1 on PR #638, both NEGATIVE on MINOR findings only, under the round-2 assignment on #234 (5968015720). Commits: `9b1d3537` (the gate, its self-test, mutants, recipe and policy table; the classifier) `5c92caca` (the partition, the rulings, the owner decision, the findings index) and `0feff20f` (two findings sentences: the gate reads each route status report at every check rather than storing it). Every probe below is the reviewer's published script from the review evidence branch, rerun unchanged at this head unless marked adapted.

| Finding | Severity, lens | Answer | Evidence at this head |
|---|---|---|---|
| R446-1 F1: a non-finite slack passes the timing floor | MINOR Conformance, Robustness, Tests | `timing()` refuses, with exit 2 and a named reason, a slack that is `inf` or `nan` and a summary whose TNS or THS total endpoints are absent or zero. Arms: WNS `nan`; WNS and WHS `inf`; zero timed endpoints. Mutants `finite slack` and `timed endpoints` killed. | `probe_gate_cli.py`: WNS `nan` rc 2; `inf` with 0 endpoints rc 2. That line prints BAD because the probe's literal expectation is 1; F1 accepts 2 and the assignment requires 2. The other 116 of 117 cases are as expected. |
| R446-1 F2: claimed refusals without an arm | MINOR Tests | Arms for the design, the design state and each of the eight `FLOW` commands; standalone RAMB36 and DSP growth; WNS and WHS at their floors; a fall of exactly the tolerance; BRAM tiles at the ceiling. Each has a shipped mutant. | `probe_gate_mutants.py`: 23 of 23 killed, control passes. |
| R446-1 F3: "net 101 LUTs and 95 FFs" mixes partitions | MINOR Docs | Both pages name one partition: the own logic of every instance the gate record lists outside `u_nvm_port`, 51 terms. Net +79 LUTs and +93 FFs; absolute 391 LUTs and 121 FFs. The processor top's own logic is stated as one of the terms: -23 LUTs, +107 FFs, its `armq_r` timer-arm queues (1,153 to 1,260 flops). | `reconcile.py` unchanged: 2 mismatches, both its hard-coded round-1 sentences; the second asserts +95 FF on a partition whose records give -12, so no prose can satisfy it. Adapted copy (diff published; only those two checks re-pointed at the round-2 sentences): 0 mismatches. |
| R446-1 R1 to R3 | RESIDUE Docs | Taken. R1 and R2 cover the same `AREA_BUDGET.md` lines as R447-1's first RESIDUE in slightly different words; R447-1's line-by-line wording is used and carries all of R446-1's content. R3 taken exactly. | `AREA_BUDGET.md` headroom table and "Where the gate runs"; findings ranking table. |
| R446-1 R4 | RESIDUE Docs | Taken in this body: decisions 1 to 5 above. | This body. |
| R446-1 S1 to S5 | SUGGESTION | All taken: one exit-code contract (S1, item 2); `check-baseline` requires the route ceiling and equals the budget table (S2, item 5); "re-baseline recommended" (S3, item 6; the policy stays growth-only); the findings index (S4); arms for header uniqueness, a single generated top and the decimal count format (S5). | Self-test and mutant campaign. |
| R447-1 MINOR 1: malformed baseline entries exit 1 by traceback | MINOR Robustness, Tests | A missing, non-JSON or endpoint-less baseline, an endpoint without a complete record, a gated figure without a tolerance, a ceiling naming no figure and a wrong-shape image manifest each exit 2 with a named reason. `check-baseline` lists a missing record and an unknown ceiling figure as problems. 13 `check` and 20 `check-baseline` arms run through `main()`. | `probe_cli.py`: 54 of 54 as documented. |
| R447-1 MINOR 2: the self-test misses disabled checks | MINOR Tests | Arms and mutants for standalone RAMB36 and DSP gating, the refusal exit status, the kind read from the directory and the ceiling, floor and fall boundaries. | `extra_mutants.py`: 18 of 18 killed, control passes. |
| R447-1 MINOR 3: the route endpoint never reads routing completion | MINOR Robustness | The route endpoint reads the run's one `*_route_status.rpt`. Unrouted nets, routing errors or routable nets not fully routed exit 1; a missing, duplicated or unreadable report exits 2. Nine route arms and two command-line arms; A's real route status reads complete. | `probe_route_status.py`: clean exit 0, 37 unrouted nets exit 1. |
| R447-1 MINOR 4: the movement figures mix partitions | MINOR Docs | As R446-1 F3. | `partition_check.py`: its complete-partition line (+79 LUT, 391 absolute, +93 FF) and its processor-top line (-23 LUT, +107 FF) equal the prose in both pages; a mechanical comparison reports 0 mismatches. |
| R447-1 RESIDUE 1 | RESIDUE Docs | Taken exactly. | `AREA_BUDGET.md`. |
| R447-1 RESIDUE 2 | RESIDUE Docs | Taken exactly for items 2 and 3 and the limitations bullet. Item 1 states the owner decision of 2026-10-03 instead of "the allocation needs the owner's ruling", which it postdates. | This body. |
| R447-1 suggestions 1 and 2 | SUGGESTION | Taken as items 5 and 4. | As above. |

Also from the assignment: `AREA_BUDGET.md` cites the owner decision where it said the allocation "needs an owner decision". `check-baseline` derives the policy comparison from the budget's table, which now holds one value per cell; no value changed, so the STOP on accepted values did not apply. Other probes rerun at this head: `check_tables.py` 49 groups, 0 mismatches; `replay_records.py` A 0, 0, 0, B 1, 0, 0, the 10 ns control 2; `probe_pr_mutant_reasons.py` 84 of 84 killed by an arm assertion, none by a crash.

## Round 3

The round answers R446-2 and R447-2 on PR #638, both NEGATIVE on MINOR findings only, under the round-3 assignment on #234 (5968718943). Both reviews found one class: inputs the gate read without validating their shape. The round closes the class rather than the listed cases. Commits: `d54f6180` (the validator, the ASCII counts, the route status rows, arms and mutants), `b38bb06d` (the contract, the stale-report note and R1 in the docs), `2b98e485` (the budget page's contract sentence scoped to `check`) and `b5894838` (a shipped mutant for the timed-endpoint boundary, whose reviewer mutant no longer applies). No Vivado run.

| Finding | Severity, lens | Answer | Evidence at this head |
|---|---|---|---|
| R446-2 F1: a route status report without its routable-net rows reads complete | MINOR Conformance, Robustness, Tests | `routing()` requires exactly one `routable nets`, one `fully routed nets` and one `nets with routing errors` row; anything else exits 2, naming the label and how many rows it has. Arms remove the routable row, the fully routed row, both rows, and add a second routable row; the mutants relaxing the presence and the uniqueness requirement, and the one dropping the fully routed label, are killed. | R446-2's `probe_route_status.py`: both CONTRACT cases rc 2, 15 of 16 as expected (the 16th is S1, declined). R447-2's `probe_route_real.py` on A: "both routable rows missing" rc 2. |
| R446-2 F2: the policy pin is proven only for tolerance cells | MINOR Tests | The fixture's WNS floor is 0.03, not 0. Arms: a budget floor and a budget ceiling the baseline does not hold, a baseline policy figure the table lacks, a timing summary without its endpoint columns; each with a shipped mutant. | R446-2's `probe_extra_mutants.py`: all four named mutants KILLED, control passes. |
| R446-2 F3, R447-2 MINOR 1: malformed record fields exit 1 by traceback or pass `check-baseline` | MINOR Conformance, Robustness, Tests, Docs | One validator, `load()`, run by `check` and `check-baseline` before any field is used. Strict JSON: `NaN`, `Infinity` and a decimal that reads as infinity are refused. Then every endpoint: a record with every field; a known kind; an identity with exactly the recorded keys and types; a sha256 hex input digest; exactly the kind's recorded figures, each a number and not a bool; scopes of non-negative integer `LUT FF RAMB36 RAMB18 DSP CARRY4` counts; every tolerance, floor and ceiling a table of numbers; no unknown field. Any deviation exits 2 with the endpoint and the reason. `judge()` runs only on a baseline the validator accepted. 25 malformed-baseline arms, each through `main()` by both commands; a killed mutant per check. | R446-2's `probe_malformed_record.py`: 0 cases not exit 2, no traceback. R447-2's `probe_contract.py`: every edited case rc 2 in both columns, no traceback; the control keeps `check` rc 1 and `check-baseline` rc 0. |
| R447-2 MINOR 2: absent net rows read complete; a superscript count escapes as a traceback | MINOR Conformance, Robustness, Tests | As F1, and the class closed in every parser: each count is read through `[0-9]+` (route status, timed endpoints, utilization, the hierarchy report), never `str.isdigit()` or `\d`; the slack through `-?[0-9]+\.[0-9]+`; budget cells through `[0-9]`. Arms plant a superscript and other-script digits in each; mutants reverting each guard are killed. | R447-2's `probe_route_real.py`: A 15 of 15 (superscript rc 2, both rows missing rc 2); B 14 of 15, the 15th being B's own +625 LUT (rc 1), as in R447-2's receipt. |
| R447-2 SUGGESTION, R446-2 S2: the route status report is not bound to the run | SUGGESTION | Recipe note: the report has no header and is read from the run directory, so a stale report from an earlier build there would be read; each measurement uses a fresh directory, and the bank deletes nothing. | `PP_SHADOW_BASELINE_RECIPE.md`, "Resource gate". |
| R446-2 R1 | RESIDUE Docs | Taken exactly: "-23 LUTs and +107 FFs; the 107 FFs are its timer-arm queues." | `AREA_BUDGET.md`. |
| R446-2 S1: the wholly unrouted layout | SUGGESTION | Not taken (assignment): exit 2 fails closed. | R446-2's route probe still prints that case BAD (want 1, got 2). |
| R446-2 S3: B's `armq_r` census | SUGGESTION | Published in the packet: `armq_r` flip-flops at 1x1, A 1,153 and B 1,260 (+107), counted by name in each run's cell census, whose sha256 matches the run receipts; 8x8 and route rows too. | Author packet, round 3 evidence. |

The exit-code contract as it now holds, in `AREA_BUDGET.md`, the recipe and this body: `check` exits 0 within tolerance, 1 for a material regression only, and 2 for every input it cannot judge, always printing its reason; no input reaches a traceback. `check-baseline` exits 0 or 2.

Every probe both reviewers published in rounds 1 and 2, rerun unchanged at this head:

| Reviewer | Probe | rc | Result at `b5894838` | Reading |
|---|---|---:|---|---|
| R446-1 | `probe_gate_cli.py` | 1 | 117 cases, 1 not as expected | That one is `inf` slack with 0 endpoints: rc 2 against the probe's literal want of 1; R446-1 F1 allowed 2 and the round-2 assignment required it, as in round 2. |
| R446-1 | `probe_gate_mutants.py` | 0 | 21 killed, 0 survived, control passes, 2 not applied | Not applied because round 3 rewrote the line: `count format accepts any decimal` (the pattern is now `[0-9]`; shipped `count format decimals` covers it) and `check_baseline: recorded figure below floor` (re-indented when the policy checks lost their `try`; shipped `baseline floor value` covers it). Both shipped mutants are killed. |
| R446-1 | `probe_pr_mutant_reasons.py` | 0 | 119 of 119 ARM | Every shipped gate mutant is killed by an arm assertion. |
| R446-1 | `reconcile.py` | 1 | 2 mismatches | Both are its hard-coded round-1 sentences, as in round 2; R446-2's `partition_rederive.py` re-derives the round-2 partition (0 mismatches). |
| R447-1 | `probe_cli.py` | 0 | 54 of 54 as documented | |
| R447-1 | `extra_mutants.py` | 0 | 17 killed, 0 survived, 1 not unique | `baseline floor value`: the same re-indented line; the shipped mutant of that name is killed. |
| R447-1 | `probe_route_status.py` | 0 | clean report exit 2; 37 unrouted nets exit 2 | Its invented report has no `routable nets` or `fully routed nets` row, which item 2 now refuses with 2 (round 2: 0 and 1). |
| R447-1 | `partition_check.py` | 0 | complete partition +79 LUT / 391 / +93 FF; `u_pp` own logic -23 / +107 | Equal to the prose; its last line is its fixed round-1 text. |
| R447-1 | `replay_records.py` | 0 | A 0, 0, 0; B 1, 0, 0; 10 ns control 2 | |
| R447-1 | `check_tables.py` | 0 | 49 groups, 0 mismatches | |
| R446-2 | `partition_rederive.py` | 0 | 0 mismatches over 10 sentences | R1's rewording keeps "-23 LUTs and +107 FFs". |
| R446-2 | `probe_extra_mutants.py --jobs 12` | 0 | control passes; F2's four KILLED; 8 KILLED, 2 not applicable, 1 note | Not applicable: `timed endpoints at zero accepted` (its span held `isdigit()`; shipped `timed endpoint boundary` added and killed) and `check skips the ceiling list` (re-indented; shipped `baseline route ceiling` killed). |
| R446-2 | `probe_malformed_record.py` | 0 | 0 of 8 cases not exit 2; 16 runs, no traceback | |
| R446-2 | `probe_policy_pin.py` | 0 | 105 of 105 | |
| R446-2 | `probe_route_status.py` (A) | 1 | 15 of 16 | Both CONTRACT cases rc 2. The 16th is S1, the wholly unrouted layout: want 1, got 2, declined by the assignment. |
| R447-2 | `classify_mutants.py` | 0 | 96 ARM, 23 ESCAPED, 0 CRASH, 0 survived, of 119 | Each ESCAPED mutant removes a refusal, so its escaped exception is the defect the arm's exit-2 contract names. |
| R447-2 | `partition_r2.py` | 0 | 51 terms; +79 / 391 LUT; +93 / 121 FF; `u_pp` -23 / +107 | |
| R447-2 | `probe_contract.py` (A) | 0 | 13 edited cases rc 2 in both columns, no traceback | Control: `check` rc 1 (MATERIAL REGRESSION), `check-baseline` rc 0. |
| R447-2 | `probe_policy.py` | 0 | 107 of 107 | |
| R447-2 | `probe_route_real.py` (A) | 0 | 15 of 15 | Superscript count rc 2; both net rows missing rc 2. |
| R447-2 | `probe_route_real.py` (B) | 0 | 14 of 15 | The 15th is B's real report: rc 1 for B's +625 LUT, wanted 0, as in R447-2's own receipt. |
| R447-2 | `real_data.sh` | 0 | A 0, 0, 0; 10 ns 2; B 1, 0, 0 | |
| R447-2 | `run_gates.sh` | 0 | 31 of 31 jobs rc 0 | Make 4.3 first on `PATH`. R447-1's `run_gates.sh` is the same list less four jobs. |

Self-audit (assignment item 4): every `int()`, `float()`, subscript and `.get()` the gate applies to content read from a file, and the validation in front of it. Line numbers are in `syn/ooc/pp_resource_gate.py` unless marked "rank" (`syn/ooc/pp_baseline_rank.py`, `hierarchy()`). "R3" marks a place this round fixed. Every measurement read is inside `record()` or `routing()`, which map `OSError`, `ValueError` (a decoding error included), `KeyError`, `IndexError`, `TypeError` and `RecursionError` to exit 2; the baseline read is in `load()` and the budget read in `check_baseline()`, both mapped the same way.

| # | Site | Data | Operation | Validation in front |
|---:|---|---|---|---|
| 1 | `pp_resource_gate.py:424` | baseline file | `json.loads` | R3: `parse_constant=constant` refuses `NaN`/`Infinity`/`-Infinity`; `parse_float=finite` refuses a decimal that reads as infinity; `OSError`, `ValueError`, `RecursionError` -> exit 2 (`:425-426`) |
| 2 | `:364` | baseline number text | `float(text)` | only text JSON's number grammar accepted reaches `parse_float`; `math.isfinite` after it (`:365`) |
| 3 | `:427`, `:431` | baseline top level | `.get("endpoints")`, `["endpoints"]` | `isinstance(baseline, dict)` short-circuits first; `:427-428` refuse a missing or non-object table |
| 4 | `:429` | baseline top-level keys | `set(baseline)` | R3: unknown keys refused (`:430`, `:432-433`) |
| 5 | `:382` | endpoint | `.get("record")` | `isinstance(entry, dict)` in the same expression |
| 6 | `:388` | record | `base["kind"]`, `["identity"]`, `["figures"]`, `["scopes"]` | R3: `isinstance(base, dict)` `:383`; every `RECORD` key present `:385-387` |
| 7 | `:392` | endpoint keys | `set(entry)` | entry is a dict (`:382-383`); R3: unknown keys refused `:393-394` |
| 8 | `:397` | identity | `identity[key]` | R3: `:395` requires a dict with exactly the `IDENTITY` keys (elif chain) |
| 9 | `:399` | identity flow, clock | iterate `identity[key]` | R3: `:397` requires both to be lists; items must be `str` |
| 10 | `:401` | input digest | `base["inputs_sha256"]`, `re.fullmatch` | R3: key present (`:385`); `isinstance(..., str)` before the match; 64 lower-case hex digits |
| 11 | `:403` | kind | `ROWS[kind]` | R3: `isinstance(kind, str) and kind in GATED` `:389`; `GATED` and `ROWS` have the same keys |
| 12 | `:404-407` | figures | `sorted(figures)`, `.values()` | R3: dict with exactly the kind's recorded figure set; every value a number, not a bool (finite by row 1) |
| 13 | `:408-412` | scopes | `.values()`, `sorted(counts)` | R3: dict of dicts with exactly `SCOPE` keys; every count `type(count) is int` and `>= 0` |
| 14 | `:414-416` | tolerance, floor, ceiling | `entry.get(field, {})`, `.values()` | R3: `isinstance(..., dict)` first; every value a number, not a bool (finite by row 1) |
| 15 | `:439` | validated endpoint | `entry["record"]["kind"]`, `["figures"]` | `load()` (rows 1-14) runs before `entry_problems()` in both commands (`:522`, `:531`, `:487`) |
| 16 | `:441`, `:448` | kind | `GATED[kind]`, `CEILINGS[kind]` | row 11 |
| 17 | `:442` | tolerance | `.get("tolerance", {}).get(figure, -1) >= 0` | row 14: a dict of numbers; absence reads -1 and is refused |
| 18 | `:446` | floor, figures | `figures[figure]`, `entry["floor"][figure]` | row 12: the timing figures are recorded; `:444` refuses an absent floor first (elif) |
| 19 | `:451-455` | ceiling, figures | `.get("ceiling", {})`, `figures[figure]` | row 14; `:452` refuses a ceiling naming no recorded figure first (elif) |
| 20 | `:296-304` | baseline record, candidate | `entry["record"]`, `base[...]`, `candidate[...]` | baseline: rows 1-15 and `entry_problems()` (`:531-533`); candidate: built by `record()` with every key (`:254-256`) |
| 21 | `:299-300` | identities | `base["identity"][key]`, `candidate["identity"].get(key)` | iterates the baseline's own keys; `.get` tolerates a missing candidate key (reads `None`, a change) |
| 22 | `:309-310` | figures | `GATED[base["kind"]]`, `base["figures"][figure]`, `candidate["figures"][figure]` | kinds equal (`:297`); both hold exactly the kind's figure set (row 12; `record()`) |
| 23 | `:315`, `:336`, `:338` | policy | `entry["tolerance"][figure]`, `entry["floor"][figure]` | `entry_problems()` in `main()` (`:531-533`) refuses a missing or negative tolerance and a missing floor |
| 24 | `:317-320` | ceiling | `entry.get("ceiling", {})`, `candidate["figures"][figure]` | row 19 (every ceiling names a recorded figure); candidate has the same figure set |
| 25 | `:353-354` | scopes | `.get(key, {})`, `.get("LUT", 0)`, `f"{lut:+d}"` | row 13 (integer counts, so `:+d` cannot raise); candidate counts are `int` from `hierarchy()` |
| 26 | `:102` | report header | `hits[0]` | `len(hits) != 1` refused `:100-101` |
| 27 | `:111` | utilization row | `cells[0]`, `cells[1]` | `len(cells) >= 2` `:110` |
| 28 | `:113-114` | utilization | `ROWS[kind]`, `seen.get(label, set())` | kind from `kind_of()` (exactly one recipe script, `:239-242`); `:115` refuses anything but one value |
| 29 | `:120` | utilization count | `float(value)` / `int(value)` | R3: `re.fullmatch(r"[0-9]+(\.5)?", value)` `:118` (was `\d`, which takes non-ASCII decimal digits) |
| 30 | `:129` | timing report | `blocks[1]` | `len(blocks) != 2` refused `:127` |
| 31 | `:133-134` | timing summary | `lines[heads]`, `lines[heads + 2]` | `heads is None or heads + 2 >= len(lines)` refused `:131` |
| 32 | `:135`, `:137-138` | timing columns | `names[0]`, `names[4]`, `values[0]`, `values[4]` | same condition: `len(names) != len(values) or len(names) < 5` is tested first |
| 33 | `:140` | timed endpoints | `int(value)` | R3: `COUNT.fullmatch(value)` (`[0-9]+`) in the same `and` (was `str.isdigit()`); `not paths` refuses absent columns |
| 34 | `:142` | slack | `float(values[0])`, `float(values[4])` | R3: `SLACK.fullmatch` (`-?[0-9]+\.[0-9]+`) `:137` (was `float()` then `isfinite`, which takes `1_0` and non-ASCII digits) |
| 35 | `:150` | recipe script paths | `path.parents[2]` | R3: `len(path.parents) > 2` in the same filter (was an `IndexError` caught by `record()`) |
| 36 | `:160` | located sources | `generated[0]`, `repository[0]` | `len(...) != 1` refused `:152-153` |
| 37 | `:171` | roots | `roots[0]` | the three-tuple `:160` builds; no file content indexes it |
| 38 | `:180` | image manifest | `json.loads` | `ValueError`, R3: `RecursionError` -> exit 2 (`:257`); values are only hashed, so `NaN` cannot reach a number |
| 39 | `:181-182` | manifest entries | `image.get("path")`, `image.get("sha256")` | `isinstance(images, list)`, `isinstance(image, dict)` short-circuit first |
| 40 | `:184-185` | manifest entries | `row["path"]`, `image['path']`, `image['sha256']` | `:181-183` refuse anything but a list of objects with string `path` and `sha256` |
| 41 | `:197` | tool header | `tool[1]` | `tool is None` refused `:192-193` |
| 42 | `:206` | cell census | `lines[0]` | `not lines` tested first in the same condition |
| 43 | `:212`, `:216`, `:233`, `:253` | CARRY4 counts | `carry[""]`, `carry.get(...)` | `carry` starts as `{"": 0}` (`:208`); file content only adds keys |
| 44 | `:223` | kind | `ROOTS[kind]` | row 28 |
| 45 | `:231` | hierarchy key | `key.split("/", 1)[1]` | `"/" in key` in the same expression |
| 46 | `:232` | hierarchy row | `counts[name]` | `hierarchy()` builds every row from `zip(FIELDS, ..., strict=True)` (rank `:42`), so all eight names exist |
| 47 | `:242` | recipe scripts | `kinds[0]` | `len(kinds) != 1` refused `:240-241` |
| 48 | `:248` | kind | `SCRIPTS[kind]` | row 28 |
| 49 | `:269` | route status reports | `reports[0]` | `len(reports) != 1` refused `:266-267` |
| 50 | `:276` | route status count | `int(value)` | R3: `COUNT.fullmatch(value)` `:274` (was `str.isdigit()`, so `²` reached `int()` as a traceback) |
| 51 | `:278-282` | route status rows | `counts.get(label, [])`, `sum(...)` | R3: exactly one `routable nets`, one `fully routed nets` (`:277-279`) and one `nets with routing errors` row (`:280-281`) |
| 52 | rank `:26-28` | hierarchy report | `split("|")[1:-1]`, `fields[2]` | slice cannot raise; `len(fields) != 10` tested first |
| 53 | rank `:30` | hierarchy row | `fields[2:]` | R3: every count cell must be `[0-9]+` or the row is refused (`ValueError` -> exit 2); only the `Total LUTs` head row is skipped (was: any row whose third cell failed `str.isdigit()` was skipped silently) |
| 54 | rank `:32`, `:34` | hierarchy row | `fields[0]` | row 52 |
| 55 | rank `:42` | hierarchy count | `int(value.strip())` | R3: row 53 |
| 56 | `:489` | budget page | `read_text()` | `OSError`, `ValueError` -> a named problem, exit 2 (`:490-491`) |
| 57 | `:467` | budget lines | `lines[starts[0] + 2:]` | `len(starts) != 1` refused `:464-465` |
| 58 | `:471-474` | budget row | `cells[0]`, `name[1]` | `split` yields at least one cell; `name is None` and the cell count refused `:472-473` |
| 59 | `:480` | budget cell | `float(value[1])` | R3: `re.fullmatch(r"([+-]?[0-9]+(?:\.[0-9]+)?)(?: ns)?", cell)` `:476` (was `\d`); a cell too long to be finite reads as infinity, which no strict-JSON baseline value equals, so the pin refuses it |
| 60 | `:486`, `:496-502` | baseline, table | `["endpoints"]`, `endpoints[name]`, `entry.get(field, {})`, `table[name][field]`, `.get(figure)` | `load()`; `:493-495` skip a name not on both sides; every table row holds all three fields (`:474`) |
| 61 | `:525-546` | baseline | `baseline["endpoints"]`, `.get(args.endpoint)`, `setdefault(...)["record"]`, `[args.endpoint]` | `load()`; `check` needs a known endpoint (`:527-529`, else argparse exits 2 with its usage) |

No place was found without a guard after the R3 fixes. The one failure outside the contract is the environment's: `record --write` failing to write the baseline file (`:544`), which is not an input.

## Authoritative references

- #234, its [lane assignment](https://github.com/kebag-logic/milan-fpga/issues/234#issuecomment-5966260488), [round-2 assignment](https://github.com/kebag-logic/milan-fpga/issues/234#issuecomment-5968015720) and [round-3 assignment](https://github.com/kebag-logic/milan-fpga/issues/234#issuecomment-5968718943); the [manager rulings](https://github.com/kebag-logic/milan-fpga/issues/234#issuecomment-5967852698) and the [owner decision](https://github.com/kebag-logic/milan-fpga/issues/234#issuecomment-5967924270); #229 workstream 1; #230, #232, #233, #639, #640.
- NFR-RES-01, `docs/reference/FR_NFR.md`.
- `docs/testing/PP_SHADOW_BASELINE_RECIPE.md`, `docs/findings/PP_SHADOW_BASELINE.md` (#231, #587).
- `docs/integration/BUILDING.md` section 5 (WNS at least +0.03 ns, WHS at least 0).
- `syn/yosys/README.md`, "The cells= record" (no checked-in Yosys cell baseline).
- `docs/testing/CI_WORKFLOWS.md`, the gate-read pages of the change classifier.

## How to get into the same state

```sh
git fetch origin 234-area-baseline
git switch --detach b5894838d6c47180ac4169e7d52dd746f461af21
git submodule update --init third_party/verilog-axis protocol-processor gptp-processor
```

The measurements follow `docs/testing/PP_SHADOW_BASELINE_RECIPE.md` with Vivado 2026.1 build 6511674; B additionally needs the processor at `ddb3119d` and the two parent-adoption patches applied in a scratch tree.

## How to validate

```sh
python3 syn/ooc/pp_resource_gate.py --selftest
python3 syn/ooc/pp_resource_gate_mutants.py
python3 syn/ooc/pp_resource_gate.py check-baseline
python3 syn/ooc/pp_baseline.py --selftest
python3 syn/ooc/pp_baseline_mutants.py
python3 scripts/ci_scope.py --selftest
python3 scripts/ci_events.py --check
```

Expected result / pass criteria: every command exits 0; the gate self-test reports 181 arms, the mutant campaigns report every mutant failing and the control passing (122 for the gate), and `check-baseline` reports 3 endpoints. With Vivado, `pp_resource_gate.py check <dir> --endpoint route-1x1|ooc-1x1|ooc-8x8` on a fresh measurement of this head exits 0, and the route prints "route status: complete".

## Known limitations / out of scope

- No RTL change: every ranked lever is a processor change for its own lane (STOP rule of the assignment).
- The Vivado half of the gate runs in the manager's merge bank for every PR that changes RTL, the processor pin or the build recipe (manager ruling).
- No Yosys-based hosted ratchet is proposed: the Yosys gate's documentation records a deliberate decision against a checked-in cell baseline, Yosys does not predict Vivado and has no timing, and the hosted Yosys top is the 8-stream default, not the shipping shape.
- Savings in the ranking are estimates; only matched before-and-after routes measure them, and no slice saving is claimed.
- B was measured from a scratch tree; its ROM digest rows for `ddb3119d` were recorded only there.
- The raw Vivado reports stay in the scratch run directories; their SHA-256 values are in the run receipts.
- The route status report's wholly unrouted layout (R446-2 S1) is not special-cased: a report without its fully routed row exits 2, which fails closed (round-3 assignment).
- `record --write` does not catch a failure to write the baseline file; that is the environment, not an input, and `check` never writes.
- `scripts/act_ci.py --selftest` is not in the local gate table: AGENTS.md section 5 lets the candidate's copy run it only inside the disposable CI job boundary. Round 1's table ran it on the host; round 2 does not. This PR does not change `scripts/act_ci.py`.
- No bitstream, hardware, flashing or bench result.

## Definition of Done

- [ ] Linked Issue acceptance criteria are satisfied
- [ ] New or changed behavior has self-checking tests
- [ ] Required local verification bar passes
- [ ] Self-test evidence is posted in a PR comment
- [ ] No undocumented requirement or interface change remains
- [ ] Internal cleared-context review is positive
- [ ] External review is positive
- [ ] Blocking and major findings are fixed and re-reviewed
- [ ] No review round remains in flight
- [ ] Candidate merge result is validated per [CONTRIBUTING.md](../CONTRIBUTING.md)
- [ ] Documentation is updated where needed
- [ ] Post-merge containment will be checked before the Issue moves to Done
