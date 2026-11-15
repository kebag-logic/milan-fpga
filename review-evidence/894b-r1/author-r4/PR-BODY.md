[A781]

## Contents

- **[Status](#status)**: round 4 answers both round 3 reviews, the held-egress rows are held to their ledger by a tracked grader, no image moves, and `894-8x8-1if` -> `894-tiers`.
- **[Linked Issue / roles](#linked-issue--roles)**: #894 and #872, with the executor and reviewers.
- **[Description](#description)**: each round 3 finding and what answers it, the regrade, the images, and what rounds 1 to 3 changed.
- **[Authoritative references](#authoritative-references)**: the rulings and clauses.
- **[How to get into the same state](#how-to-get-into-the-same-state)**: the commands to check out the branch.
- **[How to validate](#how-to-validate)**: the reviewer's commands and their expected results.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)**: what stays open, reported or left for a decision.
- **[Definition of Done](#definition-of-done)**: the merge bar.

## Status

**Both round 3 reviews are answered at their cause, and no image moves.** Head `98c0b62be911f5cff7a03ebfee7f837c23847d14`, four commits on round 3's `716a8ae7`. `894-8x8-1if` -> `894-tiers` (PR #914 is stacked on #902, which is open; `894-tiers` at `9606b3a9` is not merged here).

- **R844-1-F1 (MAJOR) is fixed in the tree.** A measured instance of any of the seven held-egress rows above its ledger figure now fails acceptance, by as little as one bus cycle, and no row is waived by its name. The rule is a tracked grader beside the others, `tb/verilator/ctrl_service_budget/egress_ledger.py`, with its self-test. The packet's acceptance gate delegates to it.
  - Controls: the unchanged ledger passes. For each of the seven rows, one bus cycle over its figure, and 36.76 ms over, each exits nonzero naming the row. R844-1's two probe inputs both fail now.
  - Round 3's six 8x8/1if legs are regraded with the fixed gate: PASS. All seven rows are under their ledger figures, at the most each logged figure can be.
- **R844-1-R1 and R843-1-R1 (residue) are fixed.** No added source comment, docstring or check description in `7398ec0a..98c0b62b` carries an issue-comment ID or review-round wording. This packet's scan prints 0 lines, and so does R844-1's own audit.
- **R843-1-S1 (suggestion) is taken.** `aecp.h` refuses, in THE SHAPES' words, a unit that charges a refused attempt without the shape's table in force. `test_aecp.cpp` asserts that each host arm's contract is at its own interfaces. Each has a control that fails in its words.
- **Every image is byte-identical to `716a8ae7`'s**, by the sha256 of each ELF and of its loadable bytes, at each step and at the head on a clean clone. So the sweep and the 8x8/1if measurement carry by that identity (see [The images](#the-images-and-what-carries)).
- **The full pass at the head is clean**, each part on its own clean clone of `98c0b62b`:
  - **Every hosted job step** of rtl-fast, rtl, elaborate and docs verifies: 139 run, 226 not run with a reason, 0 bad. In the first run, one LiteX simulation (`test_soc_timing_cuts`) hit its 900 s wall clock under host load, a result unknown and not a failure; its job ran again on a fresh clone and passed.
  - **The firmware campaigns** caught 716, 277 and 345 plants, with 0 escaped. The AECP campaign's 277 include the two new rows.
  - **The lane gates**: 59, of which 55 exit 0 and the four that exit 1 by design do so. They include the harness self-test (879 checks, 259 mutants caught), the ledger's self-test, both comment scans (0 lines) and 16 diff-check bases.
  - **The load** is 0.711 of 0.75 at 8x8/1if, and 0.513 and 0.509 at 1x1/1if.
  - **The images** are all identical, and `counters-f5` passes.

## Linked Issue / roles

Relates to #894
Relates to #872

Executor: `[A781]`
Internal cleared-context reviewer: `[R<n>]` (to be assigned; round 3's was `[R843]`, R843-1)
External reviewer: `[R<n>]` (to be assigned; round 3's was `[R844]`, R844-1)

## Description

### Round 4: the findings of round 3's reviews

| Finding | Severity, lens | What answers it | Evidence |
|---|---|---|---|
| R844-1-F1: larger held-egress misses still pass the published acceptance gate | MAJOR; Conformance, Robustness, Tests | `egress_ledger.py` in the tree holds each of the seven rows to section 13's ledger figure. A measured instance over it fails, by one bus cycle or more, whatever its name, and so does any other budget miss, a ledger row not measured, or any instance not measured. The packet gate `gate_r4.py` delegates both decisions to it. | `egress_ledger.py --selftest`: 30 controls in process and as a process, 8 mutants caught (the earlier rule, a row waived by its name, among them). `gate_controls.py` against `gate_r4.py`: 20 of 20, the 14 per-row plants included. Round 3's six legs regraded: PASS. |
| R844-1's note on the unmeasured input (not a finding) | none | An instance not measured now fails the grader and the gate, rather than resting on the harness's completeness check alone. | The "required.cpu.row" probe input exits 1 naming it. |
| R844-1-R1: issue-comment IDs and review wording in new source comments | RESIDUE; Docs | 55 added lines reworded in 25 files. Each ruling is cited by the issue, its subject and its item: #894's shape ruling, held-egress ruling, retry-cost ruling and map-keying ruling. Section 13 maps the four names to their links. | The scan of `7398ec0a..98c0b62b` prints 0 lines, and R844-1's `source_comment_audit.py` prints 0 lines. The commit changes no code: every C/H/C++ token stream is identical, and every Python syntax tree is identical without its docstrings, except five printed check descriptions. Every image is identical. |
| R843-1-R1: the same rule, 55 lines | RESIDUE; Docs, RTL, Tests | The same change. `poll_grade.py`'s "round 2 ruling" is gone with its ID. | The same scans. |
| R843-1-S1: `AECP_ATTEMPT_US` names a header it does not include, and the two-interface core arms compile at the one-interface contract | SUGGESTION; RTL, Robustness | (1) `aecp.h` has a guarded `#error` naming THE SHAPES. (2) `test_aecp.cpp` has `static_assert(MBX_N_IF == AECP_TEST_INTERFACES)`, and `aecp_arms.core_arm` gives a two-interface arm with no mailbox group its own interfaces' contract. | (1) The AECP campaign's two new build rows are refused in the `#error`'s words. (2) A planted two-interface core arm at the tracked contract is refused in the assertion's words. The core arm at two interfaces on its own contract passes 83 of 83 tests. |

#### R844-1-F1: the held-egress rows held to their ledger

**What was wrong.** Round 3's gate printed each held-egress row's difference from its ledger figure but never failed one, and it excluded the seven rows from the new misses by name, whatever their size. #894's held-egress ruling, item (a), says a new or larger miss fails the leg. Nothing in the tree held that rule either: `run.py --record-budget-findings` records every miss and fails none.

**Where the rule lives now.** It decides acceptance of every 8x8/1if measurement, the next one after the sync onto #902's merge included, so it is a tracked grader with its self-test: `tb/verilator/ctrl_service_budget/egress_ledger.py`.
- **The ledger** (`LEDGER`) is section 13's table at 8x8/1if, the one point that has one. The self-test holds it to that table, row for row and figure for figure, so the two cannot drift. The table now names both service rows by their full probe names and calls its column "Ledger, ms".
- **A larger miss.** A measured instance of a ledger row over its figure fails. The comparison is in 10 ns units, one cycle of the 100 MHz bus and the resolution of a grade's figure. A row never released or answered fails too, since its time is only a lower bound.
- **A new miss.** A budget miss of any other row fails. So do a ledger row with no measured instance and any instance not measured.
- **Its inputs** are the harness's own output: a results directory's group grades, exact to 10 ns, or a run's log. A log's `BUDGET` lines name every instance over its budget to 1 us, so a row read there is held at the most its printed figure can be, and one printed at its ledger figure fails. A log must end in its run's summary, with no refusal and one `BUDGET` line per budget miss.

The fourth commit holds the grader's self-test helpers to the Python idiom gate. The full pass's first run of the lane gates found three findings there, which a run on the working tree had missed while the file was still untracked.

**The packet gate.** `gate_r4.py` is round 3's gate, its groups and criteria, with the held-egress rows and every budget miss decided by the tree's `egress_ledger`. The rest of the gate stays in the packet because it aggregates the legs' own verdicts (run.py's exit status and its STATED, JOINS and END lines) into the lane's report tables; each failure it adds beyond the ledger is one the harness already makes in each leg.

**Controls.** Each runs as its own process, so the exit status is the verdict.

| Input | Result |
|---|---|
| The unchanged ledger, each row at its figure | exit 0 |
| Section 13's published measurement | exit 0 |
| Each of the seven rows one bus cycle over its figure (for example `backlog.owed.if0` at 63.24001 ms) | exit 1, "- the ledger: backlog.owed.if0 (backlog-owed): 63.24001 ms, over its ledger figure 63.24 ms by 0.00001 ms: a larger miss" |
| Each of the seven rows 36.76 ms over its figure | exit 1, naming the row |
| R844-1's larger-egress input (`backlog.owed.if0` at 100.0 ms) | exit 1, naming the row |
| R844-1's unmeasured input | exit 1, "required.cpu.row (backlog-owed): not measured" |
| A leg by its log alone: the published figures; and a row printed 1 us over its figure | exit 0; exit 1 naming the row |

The grader's self-test refuses eight mutants, each by its own control: the earlier rule (a ledger row waived by its name whatever its size), a grade read at 1 us, a row at its figure failing, a new miss waived, a row with no instance passing, a log's figure read as exact, a figure a hundredth over section 13's, and a row's name taken in any group.

**The regrade of round 3's legs.** Round 3's measurement ran six 8x8/1if legs at `d8629751`: arm A in four parts, the `answering-every-port` arm and `aecp-largest-notice`, 112 groups. Their group grades were not kept after round 3; their logs were, and they are published with host paths replaced. Each log's `BUDGET` lines name every instance over its budget. So the fixed gate reads those lines and the legs' own lines, and the tracked grader reads the logs directly too.

| Row the egress decides | Logged, ms | At most, ms | Ledger, ms |
|---|---:|---:|---:|
| `backlog.owed.if0` | 63.083 | 63.0835 | 63.24 |
| `backlog.owed_behind0.if0` | 63.305 | 63.3055 | 63.47 |
| `backlog.owed_behind1.if0` | 63.526 | 63.5265 | 63.69 |
| `backlog.owed_behind2.if0` | 63.747 | 63.7475 | 63.91 |
| `backlog.owed_behind3.if0` | 63.969 | 63.9695 | 64.20 |
| `backlog-owed.service.acmp.last.if0` | 62.025 | 62.0255 | 62.18 |
| `backlog-owed.service.aecp.last.if0` | 61.680 | 61.6805 | 61.83 |

- **Result: PASS.** All seven are under their ledger figures, every summary shows 0 refusals, and every leg ended rc 0. The seven are arm A's first part's only budget misses (7 `BUDGET` lines for its 7 misses). The other five legs have none.
- **Not regraded from the logs**: the rows the CPU decides, the queued notices, the largest command, the joins, slices and rounds. The fix does not change how any of those is decided, and round 3's receipt of them stands.
- **Not regraded with this gate**: round 3's 1x1/1if and 8x8/2if legs, which are #902's and are held to #902's criteria (the ledger is 8x8/1if's), and the `transmit-aged` control, which is caught by design.

#### R844-1-R1 and R843-1-R1: the source-comment rule

Every added line in `7398ec0a..HEAD` that cited a ruling by its comment ID now cites the issue, the ruling's subject and its item:
- `#894's shape ruling`, item (a) or (b) (THE SHAPES, the slice cap, the 8x8/1if gate);
- `#894's held-egress ruling`, items (a), (b)(i) to (iv) and (c) (the held-egress rows, the per-shape costs, the single source);
- `#894's retry-cost ruling`, item 1 (THE RETRY's round costs per shape);
- `#894's map-keying ruling`, item 1 (the direct index's key domain).

Section 13 maps the four names to their discussion links, which documentation may carry. Every C, C++ and header file keeps its line count. The commit changes no code, as `ast_same.py` shows by comparing every changed file's tokens or syntax tree, apart from five check descriptions that only lose their ID. `rows_grade.py`'s one line is the docstring of its own shape keying.

#### R843-1-S1: THE SHAPES' table at the charge, and each host arm's contract at its interfaces

- **The guard.** Every unit includes `aecp.h` before the table, and most charge nothing, so a plain `#ifndef` beside the define would break every core unit. C also cannot test a name at a later use. So the unit that charges a refused attempt says so: `aecp.c` includes `ctrl_loop.h` first, then defines `AECP_CHARGES_ATTEMPTS`, then includes `aecp_internal.h`. `aecp.h` then fails a unit that says so without the table in force:
  `#error "THE SHAPES: a unit that charges a refused attempt (AECP_ATTEMPT_US) has no shape's table (ctrl_loop.h) in force"`.
  The define stays the one `#define AECP_ATTEMPT_US CTRL_LOOP_RETRY_ATTEMPT_US` that `shape_costs.retry_findings` requires.
  - **Its controls** are two AECP campaign rows, read by the campaign's compile-refusal reader. `attempt-charged-without-the-shapes` drops the include, and `attempt-charged-before-the-shapes` puts it after `aecp.h`. Each is refused in those words.
- **The assertion.** `test_aecp.cpp` asserts `MBX_N_IF == AECP_TEST_INTERFACES`, "THE SHAPES: the host arm's mailbox contract (MBX_N_IF) is not at its interfaces (AECP_TEST_INTERFACES)". `aecp_arms.core_arm` gives a two-interface arm with no mailbox group the generated two-interface contract (`srp_arms.prepared`'s), as the mailbox arms already have.
  - The debug arm keeps the tracked contract. Its test configures one interface whatever the arm's count, and has no assertion.
  - Only command-line arms reach that case; every job's arms were already at their interfaces' contract.
  - **Its control** is a planted two-interface core arm at the tracked contract, refused in the assertion's words. At its own contract, `Core.*` passes 83 of 83.

#### The images, and what carries

The eight images are the size fixture and the platform at 1x1/1if, 1x1/2if, 8x8/1if and 8x8/2if. They were built from a clean clone of `716a8ae7` this round, reproducing round 3's receipt exactly, and then again after each step:

| Step | Result against `716a8ae7` |
|---|---|
| 1: the comments reworded | all 8 identical, ELF and loadable bytes |
| 2: with the guard, the include order and the assertion | all 8 identical |
| The head `98c0b62b`, on a clean clone (the full pass's) | all 8 identical; the platform image at 8x8/1if 56.0 RAMB36 |

**So the sweep and the 8x8/1if measurement carry.**
- The firmware the sweep builds is these images' sources, and only comments changed in the one changed header the `mbx` suite compiles (`ctrl_loop.h`).
- The harness graders changed only in comments, docstrings and check descriptions.
- The new grader is a reader of the harness's output.

The host suites and campaigns that compile the changed test sources run again in the full pass.

### Earlier rounds

**Round 3** (#894's retry-cost ruling) keyed THE RETRY's round costs on the shape: each listed shape states `CTRL_LOOP_RETRY_COLD_US` and `CTRL_LOOP_RETRY_ATTEMPT_US`, with 8x8/1if at 165 and 25 us, its measured line plus 5 %. `AECP_ROUND_COLD_US` and `AECP_ATTEMPT_US` are those names, and the core reads the table at compile time. Measured once on the new image (112 groups, 1,680 instances):

| Row (bound, ms) | Worst measured, ms |
|---|---:|
| AECP (20) | 4.693 |
| ACMP, ADP, MAAP (30) | 6.813, 5.897, 6.020 |
| SRP (90) | 10.284 |
| MRPDU (49) | 3.578 |
| The first queued notice (20) | 2.259 |
| The last queued notice (130), of 40 | 26.195 |
| The largest legal command, the paced R4L row (238) | 2.442 |

- THE RETRY's 2,455,411 rounds were each within their statement.
- The joins were 186.687 to 190.705 ms, within 181.0 to 239.0.
- The load was 0.711 of 0.75, and the platform image 56.0 RAMB36.
- The only budget misses were the seven held-egress rows, now held by `egress_ledger.py`.

**Round 2** (#894's held-egress ruling) made several things the shape's own:
- the MRPDU row's budget, `CTRL_LOOP_TX_BOUND_MS`, 49 ms;
- an SRP record's cost, 345 us at 8x8/1if;
- the polls' costs;
- the notices a reset leaves, 12 at 1x1/1if and 40 at 8x8/1if, none dropped;
- the direct-index key domain, with the shape header its single source.

It merged #902's heads `5b264bf2` and `7398ec0a`.

**Round 1** (#894's shape ruling, item (b)) made 8x8/1if the flip's other point. It added THE SHAPES and the 8x8/1if slice of 1,475 us, within 1,600 us.

## Authoritative references

- **R844-1-F1's authority:** [#894's held-egress ruling](https://github.com/kebag-logic/milan-fpga/issues/894#issuecomment-6871343905), item (a): the rows stay recorded misses by their names, and a new or larger miss fails the leg.
- **The other rulings:**
  - [the shape ruling](https://github.com/kebag-logic/milan-fpga/issues/894#issuecomment-6867393730), items (a) and (b);
  - [the retry-cost ruling](https://github.com/kebag-logic/milan-fpga/issues/894#issuecomment-6878014227), item 1;
  - [the map-keying ruling](https://github.com/kebag-logic/milan-fpga/issues/894#issuecomment-6870437042), item 1;
  - [the egress ruling](https://github.com/kebag-logic/milan-fpga/issues/894#issuecomment-6867990126) (MRPDU 49 ms, paced R4L 238 ms, the harness join gate 181.0 to 239.0 ms).
- **#872:** [the second-hart trigger](https://github.com/kebag-logic/milan-fpga/issues/872#issuecomment-6862464924), as the held-egress ruling restates it.
- **#665:** the attempt cost's definition (`aecp.h`), and [the 8x8/2if cold-start exception](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6842347916), which is unchanged.
- **The requirements:** FR_NFR.md 3.4.1, which charges TX backpressure to the service budget; SPLIT_CONTROL_MEMORY.md section 13 (the ledger).
- **The review reports:** R844-1 and R843-1, on `894-review-evidence` (`review-evidence/894b-r1/reviews/`).

## How to get into the same state

```sh
git fetch origin 894-8x8-1if
git switch --detach 98c0b62be911f5cff7a03ebfee7f837c23847d14
git submodule update --init --recursive
```

## How to validate

```sh
python3 -I tb/verilator/ctrl_service_budget/egress_ledger.py --selftest
python3 -I tb/verilator/ctrl_service_budget/egress_ledger.py --point 8x8-1if <round 3's six leg logs>
python3 -I tb/verilator/ctrl_service_budget/shape_costs.py --check --selftest
python3 -B tb/verilator/ctrl_service_budget/run.py --self-test
python3 -B sw/firmware/ctrl/test/aecp_arms.py --output <dir> --core --interfaces 2
python3 -B sw/firmware/ctrl/test/aecp_mutants.py --output <dir>
git diff --unified=0 7398ec0aeea468d92ff642a03a06e291a0cd58d1 HEAD -- . ':!*.md' | grep '^+' | grep -c -E 'issuecomment-|[Rr]ound [0-9]'
```

Expected result / pass criteria:

- **The ledger's self-test** passes its 30 controls, both in process and as a process, and catches 8 of 8 mutants.
- **The six round 3 logs** pass: all seven rows are within their figures.
- **The table of shapes** passes, with its controls refused.
- **The harness self-test** passes with 0 failures.
- **The core arm at two interfaces** passes 83 of 83 on its own contract.
- **The AECP campaign** ends with no escape, its two new build rows included.
- **The scan** counts 0.

## Known limitations / out of scope

- **`894-tiers` at `9606b3a9` (#902, round 12) is not merged here.** By instruction, the manager syncs after #902 merges. That sync needs a fresh byte-identity base, an 8x8/1if measurement and a full pass, each graded with `egress_ledger.py`. This round's coverage is banked against `98c0b62b` only.
- **A new Issue is due for `Mailbox.ARoundFillsWhatItsPassHasLeft` at 8x8/1if.** It fails since at least `7398ec0a` (`adapter.yields` 3 where it expects 0). It stays out of the 8x8/1if selection. This round does not alter it.
- **1x1/1if's SRP record** measured 26,086 cycles in round 1, over its 250 us. Its slices hold and its image is held byte-identical, so it stays left for a decision.
- **What R843-1 recorded as limits, unchanged:**
  - k = 3 refused attempts is never measured at 8x8/1if; its statement has about 13 % headroom over the line.
  - No in-tree gate derives a stated cost from its measurement. Only "stated at least measured" is enforced, by the harness.
- **The guard covers the unit that says it charges.** A future unit that uses `AECP_ATTEMPT_US` without saying so still gets the compiler's undeclared-name error, which names `CTRL_LOOP_RETRY_ATTEMPT_US`. C offers no way to test a name at a later use.
- **The ledger is 8x8/1if's.** Section 13 has none for 1x1/1if or 8x8/2if, whose held-egress rows are #902's and are held there. The grader refuses a point with no ledger.
- **Reported, not held, owed to #872** (unchanged from round 3): 8x8/1if's rows by every source; the load with every AECP command the largest legal one, 0.993; and two passes of `aecp-largest-notice` over THE SHARE.
- **Physical calibration was not run.** Local CPU simulation is not hardware proof.

## Definition of Done

- [x] Linked Issue acceptance criteria are satisfied (round 4's four items; round 3's measurement carries by image identity)
- [x] New or changed behavior has self-checking tests
- [x] Required local verification bar passes (the full pass at the head: see the REVIEW READY comment)
- [ ] Self-test evidence is posted in a PR comment
- [x] No undocumented requirement or interface change remains
- [ ] Internal cleared-context review is positive
- [ ] External review is positive
- [ ] Blocking and major findings are fixed and re-reviewed
- [ ] No review round remains in flight
- [ ] Candidate merge result is validated per [CONTRIBUTING.md](../CONTRIBUTING.md)
- [x] Documentation is updated where needed
- [ ] Post-merge containment will be checked before the Issue moves to Done
