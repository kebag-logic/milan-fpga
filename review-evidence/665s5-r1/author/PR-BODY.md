[A702]

## Contents

- **[Status](#status)** — What is measured, what passes, and `665-s5-hooks` -> `dev-soft-core`.
- **[Linked Issue / roles](#linked-issue--roles)** — Public task, executor, and independent reviewers.
- **[Description](#description)** — What changed and why.
- **[Authoritative references](#authoritative-references)** — Requirements/specification clauses and docs.
- **[How to get into the same state](#how-to-get-into-the-same-state)** — Checkout, submodules and environment.
- **[How to validate](#how-to-validate)** — Exact reviewer commands and expected result.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** — What is not measured, and the rulings that leave it.
- **[Definition of Done](#definition-of-done)** — The merge bar from [CONTRIBUTING.md](../CONTRIBUTING.md).

## Status

REVIEW READY at `eef3d97a`, `665-s5-hooks` -> `dev-soft-core`. The harness passes its gates and every plant is caught; the measurement does not meet S5's bound under the composed load on this firmware base.

- **The harness:** self-test 22 of 22 checks and 31 of 31 mutants; all 16 plants (a late service and an ordering defect per hook) caught by their own words.
- **The four runs at the product clock** (CPU 100 MHz on `sys`, bus 100 MHz; 1x1 and 8x8, idle and answering arms): each rc 0, regraded at the head rc 0, 145 / 159 / 207 / 221 paths, 0 refusals, 0 ordering findings, 0 fits under the layout swing.
- **Alone:** every hook within its bound at both points and arms, but H-COUNTERS' ALL push (27.58 ms at 1x1, 218.71 ms at 8x8).
- **Under the composed load:** every hook over its bound at both points and arms, but H-DISC at 1x1 on the answering arm (14.03 ms). The four ACMP commands behind the owed one are never answered, and on the idle arm SRP takes no record in the ADP backlog windows: the CPU budget harness's two starvations, on the platform image. S2b's (#810) firmware cuts are not merged at this base.
- **Gates:** the firmware self-test (4 shards), S2's harness at both points, the end-station builder, the TSN stack boundary gate, and 98 docs, scope, idiom and CI gates with `cd tests && behave`: all rc 0. The head merged onto `dev-soft-core` `a68536fa` in a scratch clone (which moves S2's split SoC: #799's `pub_src_sid_o`, #814's staged flash PHY) passes the self-test and a full 1x1 idle run: rc 0, the same findings by path and verdict, every hook's worst equal to two decimals.
- No RTL, firmware or shared harness file changed; one shared test file outside `tb/` (`ctrl_configs.py`, one `OUTSIDE` entry).

## Linked Issue / roles

Relates to #665

Executor: `[A702]`
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
| `86392bd2` | `sw/firmware/ctrl/test/ctrl_configs.py` | One `OUTSIDE` entry: the TSN stack boundary gate refuses a module that names the firmware's tree unless classified, and `hooks_build.py` names it. **The one shared file outside `tb/` this lane touches.** |
| `f5bf3677` | `hooks.py`, `hooks_selftest.py` | H-DISC's check ends its window at the interface's next ADP record, tagged or not; a development plant escaped the earlier rule. |
| `b2d4ea80` | `hooks.py` | H-NOTIFY's ordering plant keeps the solicited response aside: the notification loop rewrites the response buffer in place. |
| `4a0b3d16`, `e4d2a867` | `hooks.py`, `hooks_selftest.py` | The aging group answers each sink's PROBE_TX before its valid_time 1 ENTITY_AVAILABLE, one interface at a time, so the arm measured is that record's. |
| `3c514839` | `hooks.py`, `hooks_selftest.py` | The composed windows open a full refill after the registrations, so every bucket admits its burst at the 100 MHz CPU too. |
| `fa925043` | `hooks_soc.py`, `hooks_build.py`, `run.py`, `hooks.py`, `hooks_selftest.py` | **The product clock, 100 MHz on `sys`** (owner, 2026-10-30): the CPU clock is a named choice, `sys` by default and `milan` labelled history; plants build at `sys`. **H-DISC's undecided instances:** the sink's TMR_DELAY (0 to 1000 ms) can run past the next ADP record, so a window without a PROBE_TX decides only when longer than 1040 ms. **NARROW:** a path within its bound by fewer than 6,490 CPU cycles, the layout swing of the 2026-11-04 ruling, is a finding. The late plants' spin is doubled for 100 MHz. Four new mutants and one renamed (31 in all). |
| `eef3d97a` | `README.md` | The results at the product clock: the four runs (both points, both arms), the 16 plants, the findings by hook, the 50 MHz figures as History, the composed burst's scope (ruling of 2026-11-04, item 1), and the hooks table's reference to the split's ownership rule as a link, which the docs gate requires. |

S2's and S3's harness files are not edited: lanes S2b and S4 both edit the CPU budget harness's testbench, SoC and build, so this harness imports them read only and adds its pieces beside them.

## Authoritative references

- FR_NFR.md 3.4.1 (the service budget, the per-family ceilings) and 3.4.2 (the hook rows); NFR-SCOUT-03.
- #665 issuecomment-6513150371 (this lane's assignment), issuecomment-6495692075 (T_svc = 20 ms; min(T_svc, ceiling)), issuecomment-6508196970 (the product clock was then 50 MHz, with 100 MHz a labelled variant), superseded by issuecomment-6514866239 (owner, 2026-10-30: the split CPU clock is 100 MHz, on `sys`; S5 grades there and its 50 MHz figures become history); issuecomment-6634982529 (item 1: the composed burst with a grandmaster change at the load's first instant and every bucket full is in the SRP row's scope; item 2: a fit by less than the 6,490-cycle layout swing fits by chance); issuecomment-6630265194 (the retried notice's row is S2b's).
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
```

Every command runs at the product clock, the CPU at 100 MHz on `sys`; `--cpu-clock milan` gives the 50 MHz history figures.

Expected result / pass criteria:

- the self-test: `ctrl_service_hooks self-test: 22 of 22 checks pass; 31 of 31 mutants caught`, exit 0;
- each point: exit 0 with `--record-findings`, 0 refusals and no `FINDING ORDER` line; the paths over their bounds listed as `FINDING LATE`, and those within it by less than the layout swing as `FINDING NARROW`; `table.md` and `results.json` in the results directory;
- each plant: `PLANT <name> caught: <LATE|ORDER> <hook>: ...`, exit 0. The 16 names are `{adp,disc,acmp,aecp,notify,counters,maap,srp}-{late,order}`.

## Known limitations / out of scope

- **Ends are mailbox commits.** Ingress, egress, wire departure and the network are not measured, so each margin is what remains for them, not a wire proof. ACMP's wire round trip and MAAP's egress are lane S8's.
- **The firmware base.** `dev-soft-core` as it is (`5b5f4336`; the branch merges cleanly onto `a68536fa`). S2b's (#810) firmware cuts are not merged, so the composed misses are the hooks' before; no rebase, since S2b has not merged (assignment item 3).
- **The CPU's crossing.** The CPU runs at 100 MHz behind this base's crossing to the bus; the product wiring of the 100 MHz decision clocks it from `sys` with no crossing. That wiring reaches this harness with S2b, so these figures include the crossing's latency.
- **The answering arm** answers CTR and GSI only, at the contract's slowest. It is a labelled test arm, not the datapath (S6 connects the real one). The idle arm, the formal one, never answers a window, so AECP's change notices retry each millisecond after a bind there.
- **The retried change notice's row** (the 2026-11-04 ruling on S2b) is S2b's firmware and harness; neither arm here switches from unanswered to answering, so it is not measured.
- **The layout swing** (6,490 CPU cycles) is taken from the 2026-11-04 ruling, item 2, not measured here; no path of the four runs is within it of its bound.
- **Not run:** SHUTDOWN, every Table 5.54 cell, received validities of 10 and 31, reset and timer wrap, CPU stalls, both bus adapters, flash erase and program waits, lock expiry and the Identify spacing. The hook rows' filter checks are lane FC's (`tb/verilator/mbx`).
- **The plants** run at 1x1 and the product clock only. The 50 MHz figures are history, not re-measured at the head (`--cpu-clock milan` gives them).

## Definition of Done

- [ ] Linked Issue acceptance criteria are satisfied: **not all.** Every hook is measured at both points and both arms at the product clock, alone and under the composed load, against min(T_svc, ceiling) with its margin; ordering is checked apart from the budget; each hook's late and ordering plants are caught. But S5's acceptance that each hook is within its bound holds alone only, and not for H-COUNTERS' ALL push; under the composed load every hook misses but H-DISC at 1x1 answering, on this firmware base (Status)
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
