[A702e]

## Contents

- **[Status](#status)** — What is measured, what passes, and `665-s5-hooks` -> `dev-soft-core`.
- **[Linked Issue / roles](#linked-issue--roles)** — Public task, executor, and independent reviewers.
- **[Description](#description)** — What changed and why.
- **[Authoritative references](#authoritative-references)** — Requirements/specification clauses and docs.
- **[How to get into the same state](#how-to-get-into-the-same-state)** — Checkout, submodules and environment.
- **[How to validate](#how-to-validate)** — Exact reviewer commands and expected result.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** — What is not measured, and the rulings that leave it.
- **[Round 2](#round-2)** — What each review item became, and the evidence for it.
- **[Round 3](#round-3)** — The mutants on their own rules, the rest of the grading rules, and the amended-bounds wording.
- **[Round 4](#round-4)** — The supersede rule's path term, the mutant that named a rule it did not vary, and one check of the rule table.
- **[Definition of Done](#definition-of-done)** — The merge bar from [CONTRIBUTING.md](../CONTRIBUTING.md).

## Status

REVIEW READY at `c73be9b9`, `665-s5-hooks` -> `dev-soft-core`. The harness passes its gates and every plant is caught; the measurement does not meet S5's bound under the composed load on this firmware base. Every verdict is against the bounds in the tree at this PR's base; the amended bounds of the decisions of 2026-11-06 are a column for information, and this harness re-grades when #810 merges.

- **The harness:** self-test 28 of 28 checks and 96 of 96 mutants, each failing on the rule it names (the audit and its limits are under Round 4); all 16 plants (a late service and an ordering defect per hook) caught by their own words, a late plant on the path it delays. A no-op `counters-late` escapes, rc 1.
- **The four runs at the product clock** (CPU 100 MHz on `sys`, bus 100 MHz; 1x1 and 8x8, idle and answering arms): each rc 0, regraded at `26ba56e1` rc 0, 145 / 164 / 207 / 240 paths, 0 refusals, 0 ordering findings, 0 fits under the layout swing. `3f8caae5`, `d7cb56ef` and `c73be9b9` change only the self-test and the README, so nothing was re-measured.
- **Alone:** every hook within its bound at both points and on both arms (H-COUNTERS on the answering arm only, where it runs), but H-COUNTERS' ALL push: 27.58 ms at 1x1 and 218.71 ms at 8x8 as one path. Per descriptor, 2 of 5 rows at 1x1 and 18 of 19 at 8x8 are over 20 ms, each descriptor's own fan-out taking about 2.7 ms and about 5.9 ms: the rest of its row is the queue ahead of it.
- **Under the composed load:** every hook over its bound at both points and on both arms (H-COUNTERS on the answering arm only, where it runs), but H-DISC at 1x1 on the answering arm (14.03 ms). The four ACMP commands behind the owed one are never answered, and on the idle arm SRP takes no record in the ADP backlog windows: the CPU budget harness's two starvations, on the platform image. S2b's (#810) firmware cuts are not merged at this base. S5's acceptance "each hook within its bound" stays open on #665: these misses are measured results, and closing them is the work of the owners [the round 2 ruling](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6677495623) names.
- **Gates:** the firmware self-test (4 shards), the CPU budget harness at both points, the end-station builder, the TSN stack boundary gate in both modes without an `OUTSIDE` entry, and 98 docs, scope, idiom and CI gates with `cd tests && behave`: all rc 0, at the heads listed under Round 2. The self-test, the reviewers' probes, the docs gates and the privacy check ran again at `3f8caae5` (Round 3) and `c73be9b9` (Round 4). The code merged onto `dev-soft-core` `a68536fa` in a scratch clone passes the self-test and a full 1x1 idle run: rc 0, the same findings by path and verdict, every hook's worst equal to two decimals but H-NOTIFY's, 59.37 against 59.38. Trial merges with #810 and #812 have no conflict.
- No RTL, firmware or shared harness file changed, and no file outside `tb/`: `ctrl_configs.py` equals its base again.

## Linked Issue / roles

Relates to #665

Executor: `[A702]`, round 2 `[A702b]`, round 3 `[A702d]`, round 4 `[A702e]`
Internal cleared-context reviewer: `[R<n>]`
External reviewer: `[R<n>]`

## Description

A new sibling harness, `tb/verilator/ctrl_service_hooks/`, measures the eight NFR-SCOUT-03 hooks of FR_NFR.md 3.4.2 on the split placement's core: H-ADP, H-DISC, H-ACMP (its commit part), H-AECP, H-NOTIFY, H-COUNTERS, H-MAAP and H-SRP.

| Commit | Piece | What and why |
|---|---|---|
| `86392bd2` | `tb/verilator/ctrl_service_hooks/hooks_soc.py` | The CPU budget harness's split SoC, built from its own parts (`split_soc.py`, imported read only), with the Milan CSR window answered in gateware from a register file: ID, VERSION, the split boot simulation's seeded words, write-back and the TOD snapshot. The platform image reads and writes that window at boot. Two face arms: `idle`, exactly the CPU budget harness's (the formal arm), and `answering`, a labelled test arm whose CTR and GSI windows answer at `wait_cycles - 1`, the last cycle `KL_mbx` accepts, and whose counter-change event the testbench drives. The CPU clock is named, `sys` (100 MHz, the product's, by default) or `milan` (50 MHz, history), since `fa925043`. |
| `86392bd2` | `hooks_build.py` | The image is `ctrl_plat_image.py`'s, linked unmodified, against the platform's fixture map and then the SoC's own `csr.csv`, as the split boot simulation links it; at 8x8 with two interfaces it is the ledgered `platform-8x8-two-interfaces`. The testbench is the CPU budget harness's `sim_main.cpp`, copied into the build directory with anchored additions (the `ctrchg` step and its pads; a line per CPU store into the CSR window), each anchor found exactly once. A plant is a scratch copy of the firmware's tree with its edits, never the checkout. Every input is hashed into `build.json`; a reuse or a regrade is refused when one changed. |
| `86392bd2` | `hooks.py` | The eight hooks: their families, normative clauses, ordering obligations, ordering checks and plants. The bound is min(T_svc = 20 ms, the family's ceiling) plus any normative wait. The groups this harness adds: the counter push alone and under the composed load (answering arm), a fan-out under the composed load, the ADP and ACMP ordering instances, H-DISC's aging, and one late group per hook. Each log is graded by the CPU budget harness's grader, read through a parse that takes this harness's own lines off first. |
| `86392bd2` | `run.py`, `hooks_selftest.py`, `README.md` | The runner (points, clocks, arms, plants, reuse, regrade) and its tables; the portable self-test; the README. |
| `86392bd2` | `sw/firmware/ctrl/test/ctrl_configs.py` | One `OUTSIDE` entry for `hooks_build.py`, removed by `bc7ceb2f` (below). |
| `f5bf3677` | `hooks.py`, `hooks_selftest.py` | H-DISC's check ends its window at the interface's next ADP record, tagged or not; a development plant escaped the earlier rule. |
| `b2d4ea80` | `hooks.py` | H-NOTIFY's ordering plant keeps the solicited response aside: the notification loop rewrites the response buffer in place. |
| `4a0b3d16`, `e4d2a867` | `hooks.py`, `hooks_selftest.py` | The aging group answers each sink's PROBE_TX before its valid_time 1 ENTITY_AVAILABLE, one interface at a time, so the arm measured is that record's. |
| `3c514839` | `hooks.py`, `hooks_selftest.py` | The composed windows open a full refill after the registrations, so every bucket admits its burst at the 100 MHz CPU too. |
| `fa925043` | `hooks_soc.py`, `hooks_build.py`, `run.py`, `hooks.py`, `hooks_selftest.py` | **The product clock, 100 MHz on `sys`** (owner, 2026-10-30): the CPU clock is a named choice, `sys` by default and `milan` labelled history; plants build at `sys`. **H-DISC's undecided instances:** the sink's TMR_DELAY (0 to 1000 ms) can run past the next ADP record, so a window without a PROBE_TX decides only when longer than 1040 ms. **NARROW:** a path within its bound by fewer than 6,490 CPU cycles, the layout swing of the 2026-11-04 ruling, is a finding. The late plants' spin is doubled for 100 MHz. Four new mutants and one renamed (31 in all). |
| `eef3d97a` | `README.md` | The results at the product clock: the four runs (both points, both arms), the 16 plants, the findings by hook, the 50 MHz figures as History, the composed burst's scope (ruling of 2026-11-04, item 1), and the hooks table's reference to the split's ownership rule as a link, which the docs gate requires. |
| `bc7ceb2f` | `hooks_build.py`, `ctrl_configs.py` | The harness takes the firmware tree's path from the split boot harness, so the boundary gate's search by text does not list it, and the `OUTSIDE` entry goes: `ctrl_configs.py` equals its base. |
| `d5add6f9` | `hooks.py`, `run.py`, `hooks_selftest.py`, `README.md` | Each late plant names the path it delays, and only a finding on that path catches it. The held push's row and each hook's summary are pinned, with mutants, and `3f8caae5` closes what that left unpinned. The ALL push is reported as one path and per descriptor. The amended bounds are a column for information. |
| `78415f7a` | `run.py`, `hooks_selftest.py` | An escaped late plant says which path was not found. |
| `26ba56e1` | `README.md` | The results of round 2: the four runs, the plants, the per-descriptor tables and the amended column. |
| `3f8caae5` | `hooks_selftest.py`, `README.md` | Two mutants that stopped short of their rule now reach it, a third was reshaped and did not, as Round 4 corrects, and the held push's row and the summary's narrow boundary are pinned: 94 mutants. The README says which rows the amended bounds move. |
| `d7cb56ef` | `hooks_selftest.py`, `README.md` | The supersede rule's path is held by a row of another path, its table by a path the table does not name, each with its own mutant, and the mutant that clears every refusal is named for what it does: 96 mutants. |
| `c73be9b9` | `hooks_selftest.py`, `README.md` | Two more mutants named for what they do, found by the one check of the rule table. |

S2's and S3's harness files are not edited: lanes S2b and S4 both edit the CPU budget harness's testbench, SoC and build, so this harness imports them read only and adds its pieces beside them.

## Authoritative references

- FR_NFR.md 3.4.1 (the service budget, the per-family ceilings) and 3.4.2 (the hook rows); NFR-SCOUT-03.
- #665 issuecomment-6513150371 (this lane's assignment), issuecomment-6495692075 (T_svc = 20 ms; min(T_svc, ceiling)), issuecomment-6508196970 (the product clock was then 50 MHz, with 100 MHz a labelled variant), superseded by issuecomment-6514866239 (owner, 2026-10-30: the split CPU clock is 100 MHz, on `sys`; S5 grades there and its 50 MHz figures become history); issuecomment-6634982529 (item 1: the composed burst with a grandmaster change at the load's first instant and every bucket full is in the SRP row's scope; item 2: a fit by less than the 6,490-cycle layout swing fits by chance); issuecomment-6630265194 (the retried notice's row is S2b's).
- #665 issuecomment-6677495623 (the round 2 ruling and assignment), issuecomment-6681686082 (the maintainer's decisions of 2026-11-06, which amend the SRP and queued-notice bounds on #810), issuecomment-6682851386 (grade against the bounds at this PR's base and mark them so, the amended bounds as one column for information, both H-COUNTERS row kinds stay; 16 controllers per AVB interface, Milan v1.2 5.3.4.2).
- #665 issuecomment-6692737899 (the round 3 ruling and assignment).
- #665 issuecomment-6694276050 (the round 4 ruling and assignment).
- #664, ruling of 2026-10-06, item 4: ordering is tested apart from the budget.
- Milan v1.2 5.6.3.5, 5.6.4, Table 5.54, 5.5.2.3, Table 5.26, 5.4.5.2, Table 5.22, 5.3.7.7, 5.3.8.10, 4.3.3.1, 4.2.7.1.1, Table 4.3.
- IEEE 1722.1-2021 6.2.2.5, 6.2.2.16, 7.4.42, 7.5.2, 9.3.2.6; IEEE 1722-2016 B.3.4.2, B.3.6.6, Table B.8; IEEE 802.1Q-2018 10.7.11, Table 10-7.
- `docs/ARCHITECTURE_HW_SW_SPLIT.md` section 1 (every face value before the response that promises it); `docs/design/MAILBOX_SPLIT.md` (contracts 2.2 and 2.3); `tb/verilator/ctrl_service_budget/README.md`; `tb/verilator/ctrl_split_boot/README.md`.

## How to get into the same state

```sh
git fetch origin 665-s5-hooks
git checkout 665-s5-hooks
git submodule update --init external protocol-processor gptp-processor third_party/lwSRP third_party/tsn-c-stack third_party/verilog-axis
```

The build needs the CPU budget harness's prerequisites (`tb/verilator/ctrl_service_budget/README.md`, Run and reproduce): the product LiteX tree with its patches, the pinned RV32 SDK first on `PATH`, `LITEX_ENV_CC_TRIPLE` set to its prefix, Verilator, `PYTHONHASHSEED=0`, `COURSIER_MODE=offline` and `SBT_OPTS=-Dsbt.offline=true`. The self-test needs Python and PyYAML only.

## How to validate

```sh
python3 -B tb/verilator/ctrl_service_hooks/run.py --self-test
python3 -B tb/verilator/ctrl_service_hooks/run.py --point 1x1 --build-dir /tmp/hooks-1x1 --record-findings
python3 -B tb/verilator/ctrl_service_hooks/run.py --point 8x8 --build-dir /tmp/hooks-8x8 --record-findings
python3 -B tb/verilator/ctrl_service_hooks/run.py --point 1x1 --arm answering --build-dir /tmp/hooks-1x1-answering --record-findings
python3 -B tb/verilator/ctrl_service_hooks/run.py --point 8x8 --arm answering --build-dir /tmp/hooks-8x8-answering --record-findings
python3 -B tb/verilator/ctrl_service_hooks/run.py --plant notify-order --build-dir /tmp/hooks-plant-notify-order
python3 sw/firmware/ctrl/test/ctrl_boundary.py --require-rv32 --selftest --without verilator
python3 sw/firmware/ctrl/test/ctrl_boundary.py --require-rv32 --selftest --only verilator
```

Every command runs at the product clock, the CPU at 100 MHz on `sys`; `--cpu-clock milan` gives the 50 MHz history figures.

Expected result / pass criteria:

- the self-test: `ctrl_service_hooks self-test: 28 of 28 checks pass; 96 of 96 mutants caught`, exit 0;
- each point: exit 0 with `--record-findings`, 0 refusals and no `FINDING ORDER` line; the paths over their bounds listed as `FINDING LATE`, and those within it by less than the layout swing as `FINDING NARROW`; `table.md` and `results.json` in the results directory;
- each plant: `PLANT <name> caught: <LATE|ORDER> <hook>: ...`, exit 0, a late plant's finding naming the path it delays. The 16 names are `{adp,disc,acmp,aecp,notify,counters,maap,srp}-{late,order}`;
- the boundary gate: `ctrl_boundary: PASS`, exit 0, in both modes, with no `OUTSIDE` entry for this harness.

## Known limitations / out of scope

- **Ends are mailbox commits.** Ingress, egress, wire departure and the network are not measured, so each margin is what remains for them, not a wire proof. ACMP's wire round trip and MAAP's egress are lane S8's.
- **The bounds.** Every verdict is against the bounds in the tree at this PR's base (ruling 6682851386). The amended bounds are a column for information: SRP at 20 ms, and the queued notice's ceiling on the ALL push's rows, 20 ms at 1x1 and 60 ms at 8x8. The bound derived under that ceiling is #810's. The column applies the ceiling to those rows alone, the ones the round 2 ruling ties to the queued-notice question: an assumption, stated in the README, for #810's re-grade to settle.
- **The firmware base.** `dev-soft-core` as it is (`5b5f4336`; the branch merges cleanly onto `a68536fa`). S2b's (#810) firmware cuts are not merged, so the composed misses are the hooks' before; no rebase, since S2b has not merged (assignment item 3).
- **The CPU's crossing.** The CPU runs at 100 MHz behind this base's crossing to the bus; the product wiring of the 100 MHz decision clocks it from `sys` with no crossing. That wiring reaches this harness with S2b, so these figures include the crossing's latency.
- **The answering arm** answers CTR and GSI only, at the contract's slowest. It is a labelled test arm, not the datapath (S6 connects the real one). The idle arm, the formal one, never answers a window, so AECP's change notices retry each millisecond after a bind there.
- **The retried change notice's row** (the 2026-11-04 ruling on S2b) is S2b's firmware and harness; neither arm here switches from unanswered to answering, so it is not measured.
- **The layout swing** (6,490 CPU cycles) is taken from the 2026-11-04 ruling, item 2, not measured here; no path of the four runs is within it of its bound.
- **Not run:** SHUTDOWN, every Table 5.54 cell, received validities of 10 and 31, reset and timer wrap, CPU stalls, both bus adapters, flash erase and program waits, lock expiry and the Identify spacing. The hook rows' filter checks are lane FC's (`tb/verilator/mbx`).
- **The plants** run at 1x1 and the product clock only. The 50 MHz figures are history, not re-measured at the head (`--cpu-clock milan` gives them).

## Definition of Done

- [ ] Linked Issue acceptance criteria are satisfied: **not all.** Every hook is measured at both points and both arms at the product clock, alone and under the composed load, against min(T_svc, ceiling) with its margin; ordering is checked apart from the budget; each hook's late and ordering plants are caught. But S5's acceptance that each hook is within its bound holds alone only, and not for H-COUNTERS' ALL push; under the composed load every hook misses but H-DISC at 1x1 answering, on this firmware base. It stays open on #665 by the round 2 ruling (Status)
- [x] New or changed behavior has self-checking tests
- [x] Required local verification bar passes
- [ ] Self-test evidence is posted in a PR comment
- [x] No undocumented requirement or interface change remains
- [ ] Internal cleared-context review is positive
- [ ] External review is positive
- [ ] Blocking and major findings are fixed and re-reviewed
- [ ] No review round remains in flight
- [ ] Candidate merge result is validated per [CONTRIBUTING.md](../CONTRIBUTING.md)
- [x] Documentation is updated where needed
- [ ] Post-merge containment will be checked before the Issue moves to Done

## Round 2

Relates to #665.

Head `26ba56e1`: four commits on `eef3d97a`, no rebase. It answers [the round 2 assignment](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6677495623) on reviews R783-1 and R784-1, with [the answer on grading](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6682851386).

| Item | What changed | Evidence |
|---|---|---|
| 1. The `counters-late` plant (R783-1 F1, R784-1 F-1) | Each late plant names the path it delays, and only a finding on that path catches it, so `counters.all`'s unplanted miss no longer catches `counters-late`. The self-test runs `run.main` on all 16 plants with no plant applied: each must print `ESCAPED` and exit 1, and with its own finding each must be caught. | A no-op `counters-late` through the real build and simulation: `PLANT counters-late ESCAPED: LATE H-COUNTERS: counters.first.if0 not found`, rc 1. The real plant: caught on `counters.first.if0`, 81.819 ms. R784-1's vacuity probe: `ESCAPED`, rc 1. The catch rules on the real unplanted runs: 0 of 16 match. |
| 2. Grading rules (R784-1 F-2) | Checks for the rules of `held_row` and `summary`, with mutants across them, each failing its named check. R783-2 F1 found some unpinned, which Round 3 closes. | R784-1's three extra mutants each fail a named check. The audit of all 94 mutants at `3f8caae5` is under Round 3: this row's audit of 79 was wrong about three of them. |
| 3. `ctrl_configs.py` (R783-1 F2) | `hooks_build.py` takes the firmware tree's path from the split boot harness, so the boundary gate's search by text does not list it. The `OUTSIDE` entry is gone: `ctrl_configs.py` equals its base. | `ctrl_boundary.py --require-rv32 --selftest` rc 0 in both modes without the entry. No file outside `tb/verilator/ctrl_service_hooks/` differs from the base. Trial merges with #812, #810 and `dev-soft-core`: no conflict. |
| 4. H-COUNTERS per descriptor | `counters.all.t<type>.i<index>` rows beside `counters.all`, from the same change to that descriptor's last push. | README, Results. 5 rows at 1x1, 19 at 8x8. |
| Grading | Every verdict stays against the bounds in the tree at this PR's base, marked so in each table. One column gives the amended bounds, for information, and no verdict, finding or count reads it. No numerical grading rule changed. | Self-test check `the amended column grades nothing`, eight mutants, which hold verdicts and `LATE` findings; the column's only readers are `table` and `amended_cell`. For information, the amended bounds would change no hook's verdict: no H-SRP path lies between 18 and 20 ms, and the ALL push as one path stays over its ceiling at both points. Per descriptor, four 8x8 rows would move inside the 60 ms ceiling: `t5.i1` to `t5.i4`, 21.70 to 57.15 ms. As one path the ALL push is 27.58 against 20 and 218.71 against 60. |

All 732 paths of round 1's four runs are unchanged to the CPU cycle, with the same verdicts. The new runs add only the 24 per-descriptor rows.

The review's wording items are applied: R783-1 R1 and R2 (R784-1 RESIDUE-1), R784-1 RESIDUE-2 and RESIDUE-3 (R783-1 S4), and R784-1 S-2, so `hooks_selftest.py` runs directly.

**One defect found beyond the assignment.** Auditing why each mutant fails showed that two round 1 mutants, `H-DISC: the sink's PROBE_TX_COMMAND is never recognised` and `H-AECP: no face commit is recognised`, passed only because their check's setup crashed, so neither had exercised its rule. Both now fail on the rule.

**Assumption for the maintainer.** The amended column applies the queued notice's ceiling to the ALL push's rows only, the rows the round 2 ruling ties to the queued-notice question, and gives the ceiling because the derived bound is #810's. Any other notification path keeps its bound in that column. It grades nothing either way.

**Suggestions not taken,** as they are outside the four assigned items: R783-1 S1's cases P2, P3, P4 and P9, which still escape the self-test, and P6, which escaped at round 1 too; S2, S3 (R784-1 S-1), S5 and S6; and R784-1 S-3. R783-1 S1's P1 and P12 are closed by items 2 and 4.

**Where each gate ran in round 2.** The code's last change was `78415f7a`; `26ba56e1` changes only the README. At `26ba56e1`, in clean clones: the self-test, both boundary modes, the firmware self-test, the builder, the 98 docs gates with `cd tests && behave`, and a regrade of all four runs, which checks every input's digest. At `78415f7a`: the 16 plants, the no-op control and the CPU budget harness at both points. At `d5add6f9`: the four runs; `78415f7a` changes only an escape's printed line after it.

## Round 3

Relates to #665.

Head `3f8caae5`: one commit on `26ba56e1`, no rebase. It answers [the round 3 ruling](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6692737899) on reviews R783-2 and R784-2. Grading stays as ruled in [the answer on grading](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6682851386).

**No figure or verdict changed, and nothing was re-measured.** The commit changes `hooks_selftest.py` and the README alone. `run.py`, `hooks.py`, `hooks_build.py` and `hooks_soc.py` equal `26ba56e1`, so run.py's graded output is unchanged and the 732-path measurement was not rerun. The head's code re-renders all four published `table.md` byte for byte.

| Item | What changed | Evidence |
|---|---|---|
| 1. Mutants (R784-2 F-1) | `aging: the window opens before the arm` keeps the real group and moves only the marks. `amended: the column grades a path` leaves `bound_ms` as written and moves only a verdict. A new `amended: a finding reads the column` moves only `LATE` findings. | R784-2's `rule_probes.py`, unedited: with the arm rule deleted the aging mutant escapes (93 of 94); with both grades-nothing assertions deleted both amended mutants escape (92 of 94). Unaltered, 94 of 94. |
| 2. Grading rules (R783-2 F1) | The held push's row reports the service it was graded on; a push never sent records no cycles, W or margin; the labels of both rows are pinned, and the margin to five decimals. The summary's narrow count is tested at a slack of exactly 6,490 and at 6,489, and the check asserts those two slacks. `README.md:206` now says only what is pinned. | R783-2's `source_mutants.py`, unedited: `hp-row-ms-zero`, `hp-ms`, `s-narrow-le`, `hm-cycles`, `hm-wait` and `hm-margin` are all killed, each on its own assertion, with `hm-group`, `hm-path`, `hm-interface`, `hm-family` and `hp-margin-round`. 48 of 58 killed, up from 37. |
| 3. Amended-bounds wording (R783-2 F2 = R784-2 F-2) | R783-2's sentence, in the README and in this body's Grading row. Then, plainly: that is the whole difference between the two readings of the ALL push. Read as one path nothing moves; read per descriptor, those four rows do. | `amended_audit.py` and `amended_table.py` list exactly `counters.all.t5.i1` to `t5.i4`, on the 8x8 answering run, and no other row. No H-SRP path lies between 18 and 20 ms. |
| R784-2 RESIDUE-1 | "leaves" is now "is committed": the figure is a mailbox commit. | `README.md:469`. |

**The audit, of all 94 mutants.** It records the assertion each mutant fires. Each fails on the rule it names, by an assertion and not by an exception. "The rule it names" is a judgement, so the audit compares what fires against a table written by reading each mutant beside its check, published with the receipts for a reviewer to dispute. Run on the previous head's self-test, the same audit flags exactly three mutants, so it can fail. It also deletes each fired assertion in memory and runs the mutant again: 91 of the 94 escape once the assertions holding them are gone, 59 of them after one deletion. The other three end in an exception instead, downstream of the deleted rule, and each one's first assertion is its rule. **Corrected by Round 4:** "each fails on the rule it names" was true of 93 of these 94. The audit compares what fires with a written table, so it could not see the row below, whose name its mutant did not vary.

**A third mutant, which neither review named.** `supersede: any later group supersedes a refusal` failed the positive control and never reached the rule it names: with that control deleted it escaped, so `only by its own path` had no mutant holding it. This is the class R784-2 F-1 describes, so the audit sentence would have been false without it. The mutant now supersedes every refusal, fails on `other interface` and then `another path`, and the old table edit stays under its own name, `supersede: the table names another group`, holding the positive control. **Corrected by Round 4:** this did not reach the rule. R783-3 F1 and R784-3 F-1 show the mutant cleared every refusal with no regard to any row, varied no group, and left the path term of the rule with no holder.

**Why the verdict mutant moves only SRP.** R784-2's D2 reads the column at two interfaces. That shape reaches the rule, but it does not escape probe C: the table's `NO` for the 40 ms row is a third assertion that catches it. Loosening that pin would weaken a test, so it stays, and the mutant reads the column at one interface instead, where only SRP's verdict moves. D2 itself still fails on `the amended bounds graded a path`. With only the verdict assertion deleted, the mutant still fails on `LATE`, as a finding follows from its verdict; deleting both is what lets it escape, as probe C does.

**Suggestions.** Taken, because the same edit covers them: R783-2 S4, which is the F-1 fix, and R783-2 S5's first half = R784-2 S-3, a clause in the sentence RESIDUE-1 edits. The rest stay out, as ruled: R783-2 S1, S2, S3 and S5's `KeyError`; R784-2 S-1, S-2 and S-4. So `a-slack-reads-column`, `a-exit-reads-column`, `a-loaded-queued`, `p-counters-probe-all` and `c-whole-last` still survive. The README claims none of them: it says no path's verdict and no `LATE` finding reads the column, which is what the check pins. The other five survivors are the ones R783-2 lists as no defect.

**Where each gate ran.** At `3f8caae5`, in clean clones: the self-test, through `run.py` and directly; both reviewers' probes and source mutants; the audit; 98 docs, scope, idiom and CI gates, among them `git diff --check` and `cd tests && behave` (1977 steps passed), rc 0 with the tree clean after each; and the privacy check, over the lane's whole diff and this body. Not run again: the four runs, the 16 plants and the no-op control, the firmware self-test, the CPU budget harness, the builder, the boundary gate and the candidate merge. They are outside this round's gate set and the commit changes only the self-test and the README, so their receipts stand at the heads listed under Round 2.

## Round 4

Relates to #665.

Head `c73be9b9`: two commits on `3f8caae5`, no rebase. They answer [the round 4 ruling](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6694276050) on reviews R783-3 and R784-3, which report one finding, the same one. Grading stays as ruled in [the answer on grading](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6682851386).

**No figure or verdict changed, and nothing was re-measured.** The commits change `hooks_selftest.py` and the README alone. `run.py`, `hooks.py`, `hooks_build.py` and `hooks_soc.py` equal `3f8caae5`, so the rule at `run.py:141` is as reviewed, the published runs regrade the same, and all four `table.md` re-render byte for byte.

| Ruling item | What changed | Evidence |
|---|---|---|
| A case with a row of another path | `check_superseded` has a case where `hooks-disc-aging` measured ENTITY_AVAILABLE on interface 1 and left TMR_NO_ADP unmeasured there too. Both refusals stay and nothing is superseded. That is the shape the check's docstring names, so the same edit covers R784-3 S-3. | The path term dropped from `run.py:141` now fails `another path`: `sup-no-path` in R783-3's `source_probe.py`, `sup-any-path` in R784-3's `r3_probes.py`, both unedited. |
| A mutant that fails on it | `supersede: a row of another path supersedes a refusal` goes through the rule as written, with `run.py` unchanged: each row of the table's group is read as the table's path, so the rule's comparison of paths compares nothing. | It fires `another path`. With that assertion deleted, it alone escapes (R783-3's `deletion_probe.py`). |
| `any later group` | Renamed, the ruling's second option: `supersede: every refusal is superseded`. It clears every refusal with no regard to any row, so it fires `other interface`, then `a path the table does not name`, then `another path`, and escapes only with all three deleted. | `mutant_audit.txt`, its chain. |
| The rule table, the README row and the PR sentence | All three match. Round 3's two paragraphs that said the mutant reached its rule are corrected in place. | `mutant_rules.json`, `README.md:234-237`, Status and Round 3 above. |
| The remaining rule table, once | Below. | `rule_table_check.md`, `source_twins.txt`. |

**The old `another path` case.** Both reviews show it could not fail for what it was labelled: its refused path, `acmp.bind_rx`, stopped at the table lookup before any row was compared. The new case takes those words. Relabelling the old case alone would have repeated the defect, because a mutant of the table still met a row of another path. So it is now `a path the table does not name`, with a row of its own path in the named group on the same interface, and only the table stops it. `supersede: the table names a second path` fails on it, and with it deleted that mutant alone escapes. R783-3's `sup-second-entry`, which survived, is now killed, and R784-3's `sup-table-any-path` fails this assertion where only a sibling mutant caught it before.

**The one check of the rule table.** R784-3 is right that the audit cannot see a name its mutant does not vary, so the check is not the audit again. I read all 96 names beside each mutant and what it fires, published row by row for a reviewer to dispute. The finding's defect also has a mechanical form: a mutant caught while the rule it names can lose a term at the source with nothing failing. Only a mutant that wraps a rule's output can step past that rule, and 58 of the 96 do. Each has a twin, the same defect made in the rule's own source.

- **Result:** 61 twins, the 58 and three read hardest by name. 60 fail the mutant's own assertion, 1 fails another and none survives.
- **It can fail:** run at `3f8caae5` on the finding's own path term, the method reports `TWIN SURVIVES`, rc 1, so it would have found this finding. The audit, on a copy with `another path` deleted, reports that mutant `ESCAPED`, rc 1.
- **Two more names, renamed to what they do**, as the ruling's remedy: `bound: the margin is not recorded` records a margin, of -160 from a timeout of zero, and is now `bound: the margin is taken from a timeout of zero`. `held missing: its finding is dropped` leaves a generic `LATE ... never served` finding, and is now `held missing: its finding by name is dropped`.
- **One row disclosed, not changed:** `buckets: the window opens right after the registrations`. The name is true: the wait goes to 0, so the groups do open right after. It fires the half of the rule about the wait's length, because the group's own assertion compares against the same mutated value. Its twin removes the wait and fails that assertion, so the rule is held, but no mutant fires it.

That is the one check, and I stopped there.

**What this leaves, plainly.**

- Deleting `other interface` alone lets nothing escape: `every refusal is superseded` falls through to the next case. The interface term is held by that assertion directly, as dropping it at the source fails it, but no single-term mutant holds it.
- The group term has no assertion of its own. Dropped at the source, the self-test fails because `the table names another group` escapes, as both reviews found. The rename was the ruling's other option, so no case varies the group.
- 48 `expect` statements are fired first by no mutant, down from 49 and mostly direct pins. They are not rows of the rule table, so this check did not audit them.
- "Each failing on the rule it names" stays a judgement, and the published table is what a reviewer disputes.

**Two trials that no longer apply.** R783-3's `supersede_fix_check.py` and R784-3's `fix_feasibility.py` patch the pre-fix text, which this change replaced, so each stops on its own anchor check, rc 1. Their case is now in the tree, and `sup-no-path` and `sup-any-path` show it working.

**Suggestions and the residue.** R783-3's R1 is applied in the Grading row, in its exact words. Taken, because the same edit covers them: R784-3 S-3; R783-3 S3, in substance, under a name that says no row is needed at all; and R783-3 S4, in the audit script, which the `ESCAPED` control needs. The rest stay out, as ruled: R783-3 S1 and S2, R784-3 S-1 and S-2.

**Where each gate ran.** At `c73be9b9`, in clean clones: the self-test, through `run.py` and directly; both reviewers' probes and source mutants from rounds 2 and 3, unedited, but for the two trials above; the audit and the twins, with their controls; 98 docs, scope, idiom and CI gates, among them `git diff --check` and `cd tests && behave` (1977 steps passed), rc 0 with the tree clean after each; and the privacy check, over the lane's whole diff and this body. Not run again: the four runs, the 16 plants and the no-op control, the firmware self-test, the CPU budget harness, the builder, the boundary gate and the candidate merge. They are outside this round's gate set and the commits change only the self-test and the README, so their receipts stand at the heads listed under Round 2.

