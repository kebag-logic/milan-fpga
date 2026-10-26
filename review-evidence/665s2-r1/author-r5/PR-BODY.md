[A681e]

## Contents

- **[Status](#status)** — Green/WIP/blocked, test tally, and `branch` -> `dev`.
- **[Linked Issue / roles](#linked-issue--roles)** — Public task, executor, and independent reviewers.
- **[Description](#description)** — What changed and why.
- **[Authoritative references](#authoritative-references)** — Requirements/specification clauses and docs.
- **[How to get into the same state](#how-to-get-into-the-same-state)** — Copy-pasteable checkout/dependency/environment commands.
- **[How to validate](#how-to-validate)** — Exact reviewer commands and expected result.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** — What this deliberately does not do, and why.
- **[Definition of Done](#definition-of-done)** — The merge bar from [CONTRIBUTING.md](../CONTRIBUTING.md).

## Status

**Round 5: both R703-4 findings are fixed, and R703-4-R1 is applied to this body.** No firmware changed, and nothing was measured again. Every figure is a regrade of round 3's logs, and every measured cycle count is unchanged. The rows still miss T_svc = 10 ms, so the measurement STOP stands; the [later owner decision](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6421463860) puts instruction-cache evaluation before firmware-only tuning.

- A run that leaves out a backlog row now names the row and labels its figure partial, in `results.json` and in `table.md`.
- Arm B runs three of the four backlog rows: `backlog`, `backlog-adp` and `backlog-owed`, without `backlog-adp-refill`. Its figure now reads "over 3 of 4 backlog windows, a partial figure (backlog-adp-refill not run)", and the README and this body say the same. Arm B was not re-measured.
- The self-test passes 87 checks and catches 62 of 62 mutants (84 and 57 in round 4).
- R703-4's own `r703_4_probes.py`, unmodified, now reports P3, P4, P5 and P7 caught, and its D1 demonstration names the rows not run and the partial label. P1, P2, P8 and P10 stay caught. P6 and P9 still escape; they are R703-4's optional suggestions S1 and S2.
- R703-3's `review_mutants3.py` and R703-2's `review_mutants2.py`, unmodified, give the same results as in round 4: 18 of 21 caught (G2, G3 and H3 escape) and 23 of 25 caught (N11 and N12 escape).
- A regrade of round 3's logs at this head, in six arms and three controls:
  - every log and every group's grade is byte-identical to round 4's regrade;
  - each `results.json` composed-maximum record gains only `rows`, `not_run` and `partial`;
  - each `table.md` is unchanged except arm B's composed-maximum line, which now reads partial.
- 96 local gates ran one at a time at this head, and every one is rc 0 with the tree clean after it:
  - the bare-metal scope gate (`scripts/check_baremetal_only.py --check`: 0 findings across 1431 files);
  - the docs workflow's check-mode commands and self-tests (the em dash gate: 0 findings over 643 added lines);
  - the compiler-absent control and the end-station builder gate, each with its one NOT RUN arm (the compiled census the absent mode hides, and a calibration build tree this host lacks);
  - the harness self-test;
  - `git diff --check`;
  - behave, 406/406 scenarios.
- The act runner's self-test is left to CI, which AGENTS.md requires of a candidate's copy.

`665-s2-cpu-budget` -> `dev-soft-core`, head `f58d049beb377c3f535628067022d4d5b51e8208` (two commits on round 4's `a66148f6`).

**The baseline for S2b and S2c** is arm A's composed maximum over every backlog window: at least 31.32 ms at 1x1 and at least 44.19 ms at 8x8. Those figures are lower bounds, because SRP's load is never released in the bound-talker windows. Compare them window by window, over the same four backlog rows, using the README's composed-window table.

- The figure over released windows only (14.81 / 27.84 ms) is not a baseline. A change that lets SRP be served adds windows to it, so its before and after would cover different windows.
- Neither is a partial figure. A re-measure that leaves out a backlog row now names that row, and its figure covers fewer windows than the baseline.

## Linked Issue / roles

Relates to #665 (lane S2). Not every acceptance item is met: the rows miss T_svc, and one RESIDUE item stays with the manager (see Known limitations).
Relates to #397 (re-opened by the Mark II decisions).

Executor: `[A681e]`
Internal cleared-context reviewer: `[R703]`
External reviewer: `[R704]`

## Description

The round-5 assignment is [issuecomment-6426822636](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6426822636). It answers R703-4; R704-3 stays positive. Every change is under `tb/verilator/ctrl_service_budget/`: `run.py`, `selftest.py`, `selftest_mutants.py` and the README. No shipping RTL, SoC, firmware, CI, workflow or other doc file changes. The grader, the scenario, the testbench and the build code are unchanged, so round 2's attested builds still reuse, and every group script and every group's grade is unchanged.

| Finding | What changed |
|---|---|
| R703-4-F1: a composed maximum over fewer than the four backlog rows was reported as the composed maximum, and arm B's was | `run.composed_maximum` now names the backlog rows a run did not include (`not_run`), with `rows` and a `partial` flag. `table.md` labels such a figure, for example "Composed maximum over 3 of 4 backlog windows, a partial figure (backlog-adp-refill not run): 740,260 CPU cycles (14.805 ms), backlog." A run of all four rows prints the line it printed before, so arm A's tables are unchanged. Arm B is not re-measured: adding `backlog-adp-refill` to it would be a new measurement that changes arm B's published figures. So the README and this body state arm B's coverage: `backlog`, `backlog-adp` and `backlog-owed`, without `backlog-adp-refill`, a partial figure. A named check covers arm B's three rows and one row alone. Its mutant drops the rule. |
| R703-4-F2: the check did not pin its own lower-bound rule or the published label | A new check has the longest window release its load while a shorter one does not, and asserts `lower_bound: True`; it fails under P7. The `results.json` record now comes from `run.summary`, which the run writes. A second new check requires that record to equal the expected one, and the table line rendered from it to match word for word. It covers three cases: a lower bound over every window, a partial figure, and both at once. It fails under P3, P4 and P5. Each check has its own mutants: one for the lower bound, and three for the table and `results.json`. |
| R703-4-R1 | The figures row is renamed "A recipient's cost, every fan-out, both arms (arm A in brackets)". |
| Found this round: two rows of the README's mutant table named the wrong check | Round 4's records-ahead check grades a synthetic window. Under `worst pass: the run's last pass is dropped` and `composition: the load is the stimulus's own declaration (earlier rule)`, that grade refuses before the checks the README named can run. The self-test counts a refusal as caught, so both mutants were caught at the round-4 head, but by that refusal. The two rows now name the refusal the self-test prints. All 62 rows of the table now match the self-test's output. |

Figures (CPU 50 MHz, bus 100 MHz), regraded from round 3's logs:

| Figure | 1x1, one interface | 8x8, two interfaces |
|---|---|---|
| Paths missing T_svc (instances), arm A | 22 of 81 (58 of 141) | 60 of 129 (102 of 182) |
| Composed maximum over every backlog window, arm A | at least 31.32 ms (backlog-adp), a lower bound | at least 44.19 ms (backlog-adp-refill), a lower bound |
| Over 3 of 4 backlog windows, arm B (`backlog`, `backlog-adp` and `backlog-owed`; `backlog-adp-refill` not run; a partial figure, not the composed maximum; each window released) | 14.81 ms (backlog) | 27.84 ms (backlog) |
| Over the windows that released their load only, arm A (not the composed maximum) | 14.81 ms | 27.84 ms |
| Worst pass, A | 31.32 ms | 59.79 ms |
| SRP's records under the composed load | never released in arm A's bound-talker windows (at least 568 to 628 ms); elsewhere first 66-84 ms, last up to 186 ms | never released likewise (at least 584 to 659 ms); elsewhere first 131-144 ms, last up to 341 ms |
| Every fan-out at capacity, arm A (16 / 32 recipients) | 7.77 to 11.33 ms (SET_NAME the longest) | 12.39 to 22.98 ms (SET_NAME the longest) |
| Every fan-out at capacity, arm B | 7.77 to 14.80 ms (BIND_RX's GET_STREAM_INFO notice the longest) | 12.39 to 32.78 ms (SET_STREAM_INFO on interface 1, over the 24 ms ceiling) |
| A recipient's cost, every fan-out, both arms (arm A in brackets) | 11,818 to 21,875 CPU cycles (11,818 to 20,358) | 11,786 to 22,030 (11,844 to 20,486) |
| A response with 7 frames owed ahead (12 ACMP) | 126.29 ms | 161.10 ms |
| The four commands behind it | none answered | two answered (176.52, 188.27 ms), two never |
| An event behind 15 others | 15.49 ms | 44.65 ms |
| An ACMP command behind a full acmp ring | 63.30 ms | 108.71 ms |
| An ENTITY_AVAILABLE behind the adp ring (observed) | 67.93 ms | 83.51 ms |
| The same, its bucket refilling (observed) | 88.33 ms | 118.81 ms |
| SHUTDOWN -> ENTITY_DEPARTING | 0.58 ms | 0.58 / 1.17 ms |

Decision input:

- **D4 (a)**: per-pass CPU work sets the time.
  - `srp_mbx.c:441-451` admits an SRP record only when no tick is owed and no event is pending. The mailbox ticks every 10 ms. Whenever every pass is over 10 ms, as in arm A after a bind, SRP takes nothing.
  - A notification costs 11,786 to 22,030 CPU cycles a recipient (11,818 to 20,486 in arm A). The notifications go one after another in one pass.
  - The rest is `memset` and `memcpy`, lwSRP's `mrp_mad`, AECP's polls, and software multiply and divide.
  - A cap that keeps passes under the tick also ends SRP's starvation.
- **D4 (b)**: the event, ACMP and MAAP backlogs are bounded by ring room. ADP, AECP and SRP are observed at their burst. Every loaded channel's last record misses T_svc. The ACMP ring's room (12) exceeds the core's owed responses (8).
- **D3**: unchanged. A flash-window read costs 15 to 29 times a block RAM fetch. The hot set is at least 42,080 B (1x1) and 43,060 B (8x8).

## Authoritative references

- `docs/reference/FR_NFR.md` 3.4.1:
  - the markers;
  - "the last required recipient's commit ends a notification fan-out";
  - "backlog ... consume this budget";
  - TX-ring backpressure.
- H-NOTIFY in `FR_NFR.md` 3.4.2.
- `docs/design/MAILBOX_SPLIT.md:495-502`, `:645-657`, `:753-758`.
- `sw/mailbox/mailbox.yaml`: token buckets, ring words, the event ring, and the receive and transmit rings' names. `hdl/milan/mailbox/KL_mbx_rx.sv`: admission.
- `scripts/check_baremetal_only.py`: the bare-metal scope gate (#259), run by `.github/workflows/docs.yml`.
- AECP firmware:
  - `sw/firmware/ctrl/aecp/aecp.h` (`AECP_REGISTRATIONS`);
  - `aecp.c` (`transmit`, the retry);
  - `aecp_commands.c`;
  - `sw/firmware/ctrl/test/ctrl_aecp_image.c` (`a_format`).
- SRP, the loop and ACMP:
  - `sw/firmware/ctrl/srp/srp_mbx.c:441-451`;
  - `sw/firmware/ctrl/loop/ctrl_loop.c` (`service_rx`);
  - tsn-c-stack `acmp.h` (`ACMP_OWED_MAX`) and `acmp.c` (`room`).
- IEEE 1722.1-2021 7.5.2 (unsolicited notifications), 7.4.2.1, 7.4.15.1 and 7.4.45.1; Milan v1.2 5.4.5.2, Table 5.22 and Table 5.26.
- Owner decisions D3, D4 and D5 (issuecomment-6409738976), and the cache-first decision (issuecomment-6421463860).

## How to get into the same state

```sh
git fetch origin
git checkout 665-s2-cpu-budget
git submodule update --init third_party/tsn-c-stack third_party/lwSRP
```

Use the capture prerequisites (`tb/verilator/nvm_capture_cpu/README.md#run`):

- the product LiteX tree, with its virtual environment first on `PATH`;
- the pinned RV32 SDK and Verilator;
- `LITEX_ENV_CC_TRIPLE`, `PYTHONHASHSEED=0`, `COURSIER_MODE=offline` and `SBT_OPTS=-Dsbt.offline=true`.

Keep build directories outside the checkout. The Markdown gates need the pinned renderer (`tools/markdown/requirements.txt`).

## How to validate

```sh
python3 scripts/check_baremetal_only.py --check
python3 -B tb/verilator/ctrl_service_budget/run.py --self-test
python3 -B tb/verilator/ctrl_service_budget/run.py --point 1x1 --build-dir /tmp/budget-1x1 --record-budget-findings
python3 -B tb/verilator/ctrl_service_budget/run.py --point 8x8 --build-dir /tmp/budget-8x8 --record-budget-findings
python3 -B tb/verilator/ctrl_service_budget/run.py --point 1x1 --build-dir /tmp/budget-1x1-ports --variant answering-ports --groups acmp-cmd,acmp-noresp,acmp-notk,acmp-disc,backlog,backlog-adp,backlog-owed,aecp-fanout --record-budget-findings
python3 -B tb/verilator/ctrl_service_budget/run.py --point 1x1 --build-dir /tmp/budget-1x1-shutdown --variant shutdown-entry --record-budget-findings
python3 -B tb/verilator/ctrl_service_budget/run.py --point 1x1 --build-dir /tmp/budget-slow-adp --mutation slow-adp-rx
python3 -B tb/verilator/ctrl_service_budget/run.py --point 1x1 --build-dir /tmp/budget-slow-shutdown --variant shutdown-entry --mutation slow-adp-shutdown
python3 -B tb/verilator/ctrl_service_budget/run.py --point 1x1 --build-dir /tmp/budget-as-built --cpu-regions as-built
python3 scripts/docs_check.py
python3 scripts/check_py_idiom.py
python3 scripts/check_em_dash.py --base e76a755afc0536453161e3cd33f6f4d2dcd7641f
python3 scripts/gen_toc.py --check
cd tests && behave
```

Expected result / pass criteria:

- The bare-metal gate prints `baremetal-only: OK (0 findings across 1431 tracked first-party file(s))`, rc 0.
- The self-test prints `self-test: 0 failures` with 87 `PASS` and 62 `MUTANT caught` lines, rc 0.
- Run summaries, each rc 0:
  - 1x1 run: `18 groups graded, 0 refusals, 58 T_svc misses (58 of 141 probe instances, 22 of 81 paths)`.
  - 8x8 run: `17 groups graded, 0 refusals, 102 T_svc misses (102 of 182 probe instances, 60 of 129 paths)`.
  - 1x1 answering-ports run: `8 groups graded, 0 refusals, 41 T_svc misses (41 of 68 probe instances, 18 of 44 paths)`.
  - Shutdown arm: `2 groups graded, 0 refusals, 0 T_svc misses (0 of 2 probe instances, 0 of 1 paths)`.
- Each figure repeats to the cycle. The 1x1 run's `table.md` ends its composed-window table with `Composed maximum over the 4 backlog windows: at least 1,565,803 CPU cycles (31.316 ms), backlog-adp, a lower bound (load unreleased in backlog-adp, backlog-adp-refill).`, then the released-only figure, 740,260 (14.805 ms).
- The 1x1 answering-ports run's `table.md` reads `Composed maximum over 3 of 4 backlog windows, a partial figure (backlog-adp-refill not run): 740,260 CPU cycles (14.805 ms), backlog.` Its `results.json` record has `"not_run": ["backlog-adp-refill"]` and `"partial": true`.
- The controls print `CONTROL slow-adp-rx caught`, `CONTROL slow-adp-shutdown caught` and `CONTROL as-built caught: an instruction access fault (cause 1)`, rc 0 each.
- Each listed docs gate is rc 0; the em dash gate reports 0 findings.
- behave: 14 features, 406 scenarios, 1977 steps passed.

## Known limitations / out of scope

- The rows miss T_svc, and this PR repairs no service path.
  - The [later owner decision](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6421463860) puts instruction-cache evaluation (S2c) before firmware-only tuning (S2b, a per-pass work cap in `ctrl_loop` under D4). Both re-base against the composed maximum over every backlog window.
  - The SRP starvation, the ACMP drop and the per-recipient cost are measured and reported here. Whether they become Issues or S2b scope is the manager's decision.
- RESIDUE R703-1 R-4 / R704-3-R1 (one sentence in `docs/testing/TESTING.md`) is not applied. That file is in the release lanes' file map, which split lanes stay out of, so it stays on the residue checklist.
- Arm B runs three of the four backlog rows and was not re-measured with `backlog-adp-refill`, so its figure over the backlog windows is partial, and is labelled so.
- R703-4's suggestions S1 to S3 are optional, outside the round-5 assignment, and not applied:
  - S1: fan-out recipients that commit out of registration order (P6 escapes);
  - S2: a record released on the bus cycle of a later record's commit (P9 escapes);
  - S3: R703-3's S1 to S3, carried (H3 escapes; the idle minimum's exclusion; R703-2's S1 to S3).
- A composed window closes three quiet passes, or 500 ms, after its row is served. A record still unreleased then is reported with the time it had waited by the run's end, a lower bound.
- A record's service ends at the end of its releasing pass; lwSRP may keep a record for replay and finish it later.
- In arm A the fixture's stream observation reports unavailable. So SET_CONFIGURATION, SET_STREAM_INFO, an output map edit and BIND_RX's GET_STREAM_INFO notice complete only in the answering-ports arm. At 8x8 the image's input maps have capacity 0.
- SET_STREAM_FORMAT is refused in both arms, whose format port answers unsupported, so its fan-out is not run.
- The lock expiry's notice (60 s) and the counter pushes are not run.
- The ADP, AECP and SRP backlog rows are observed at their burst; the refill leg is one sample of sustained arrivals.
- SHUTDOWN is measured through a labelled test-only entry. START_STREAMING is not run.
- Ends are mailbox commits: no wire, ingress, egress or network time. Flash erase and program waits are zero. There is no DDR3 and no datapath.
- The linked image addresses placeholder devices; #791 and #723 are open.
- The self-test is portable, but no CI job runs it yet; that registration is a CI change.
- Physical calibration was not run; nothing here is hardware evidence.

## Definition of Done

- [ ] Linked Issue acceptance criteria are satisfied
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
