[A681c]

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

**Round 3: every finding of R703-2 and R704-2 is fixed at its cause, and both points are re-measured.** The harness now measures the whole defined load: the load's service, the fan-out at registration capacity and the owed row's full population. The soft core is slower than round 2 reported. The rows still miss T_svc = 10 ms, so owner decision D4's STOP into S2b stands.

- The self-test passes 81 checks and catches 52 of 52 mutants (51 and 36 in round 2).
- Both reviewers' probes were rerun unmodified. R703-2's source mutants N6, N8 and N10 are now caught. R704-2's SRP-omission plant now fails two named checks. Each reviewer's capacity and owed probe reproduces the published figure to the cycle.
- Three full-harness controls are caught: `slow-adp-rx`, `slow-adp-shutdown` and `as-built`.
- Every gate is rc 0 at the head, and behave passes 406/406 scenarios.

`665-s2-cpu-budget` -> `dev-soft-core`, head `f887663852d118e810ef690c3dd5cf9fe2292588` (one commit on round 2's `cd3525c3`).

## Linked Issue / roles

Relates to #665 (lane S2). Not every acceptance item is met: the rows miss T_svc (D4), and one RESIDUE item stays with the manager (see Known limitations).
Relates to #397 (re-opened by the Mark II decisions).

Executor: `[A681c]`
Internal cleared-context reviewer: `[R703]`
External reviewer: `[R704]`

## Description

The round-3 assignment is [issuecomment-6420330377](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6420330377). Every change is under `tb/verilator/ctrl_service_budget/`. No shipping RTL, SoC, firmware, CI, workflow or other doc file changes. The testbench and build code are unchanged, so round 2's attested builds still reuse.

| Finding | What changed |
|---|---|
| R703-2 F1: SRP serviced and reported | For each loaded channel, the grader grades the window's first and last record from its receive commit to the end of the pass that released it. A record never released is a measured row marked never released: its time is a lower bound, and it fits neither T_svc nor the ceiling. A window's longest pass is the composed maximum only if the window released its whole load; otherwise the window names the records left. |
| R703-2 F2: fan-out at registration capacity | A new `aecp-fanout` group registers the firmware's `AECP_REGISTRATIONS` (16) controllers on every interface. A controller outside them then sends every state-changing command the image notifies, and each fan-out ends at the last of 16 or 32 recipients: SET_NAME, SET_CLOCK_SOURCE, SET_CONTROL (identify), REMOVE/ADD_AUDIO_MAPPINGS, SET_SAMPLING_RATE, LOCK_ENTITY acquired and released. The answering-ports arm adds SET_CONFIGURATION, SET_STREAM_INFO, output map edits and BIND_RX's GET_STREAM_INFO notice. The per-recipient cost is reported. |
| R704-2 F1: the owed row's population | The owed row carries the 12 admitted ACMP commands: seven owed, the input, and four behind it. Its response must follow exactly the seven owed responses, by sequence_id and in order. The grader derives each composed row's population from the mailbox contract alone. The self-test restates those loads and counts every composed window's real stimulus against them, so omitting SRP, MAAP or ACMP work fails named checks. |
| R703-2 F3: self-protection | Synthetic windows put the longest pass neither first nor last and the run's worst pass last, and a window is checked against a defined load one record smaller. R703-2's N6, N8 and N10 fail named checks. |
| R704-2 F2: path counting | The SHUTDOWN control is an instance of `adp.shutdown`. SHUTDOWN 1x1 is now 1 path, 2 instances; 8x8 is 2 paths, 3 instances. A check runs on the real groups. |
| RESIDUE R703-2 R1-R5 | The README wording is applied as given; the `(d58c8e22)` mutant suffixes are now `(earlier rule)`. |

Two defects surfaced while re-measuring, and both are now graded:

- **The ACMP core drops the commands it cannot owe.** The ring admits 12 GET_RX_STATEs, but the core holds at most `ACMP_OWED_MAX` = 8 responses (tsn-c-stack `acmp.h`; `room()` counts a busy drop). With the egress held, the commands behind the owed input are taken and never answered. At 1x1, all four are never answered in both arms; at 8x8, two of the four. Each is a path reported as never answered (unbounded).
- **The idle-pass minimum was the pass the script's end cuts short.** That pass is now excluded. The 8x8 idle pass is 3.14 to 3.71 ms (round 2 printed a 2.04 ms floor in arm A and 0.14 ms in arm B).

Re-measured (CPU 50 MHz, bus 100 MHz). Unchanged groups were regraded from their recorded logs on the attested builds; their scripts are byte-identical. `backlog-owed` was run again and `aecp-fanout` is new:

| Figure | 1x1, one interface | 8x8, two interfaces |
|---|---|---|
| Paths missing T_svc (instances), arm A | 22 of 81 (58 of 141) | 60 of 129 (102 of 182) |
| Composed maximum (load released), A and B | 14.81 ms | 27.84 ms |
| Longest pass of a window whose SRP load is never released (A, lower bound) | 31.32 ms | 44.19 ms |
| Worst pass, A | 31.32 ms | 59.79 ms |
| SRP's records under the composed load | never released in arm A's bound-talker windows (at least 568 to 628 ms); elsewhere first 66-84 ms, last up to 186 ms | never released likewise (at least 584 to 659 ms); elsewhere first 131-144 ms, last up to 341 ms |
| SET_NAME fan-out at capacity | 11.33 ms (16 recipients) | 20.68 / 22.98 ms (32) |
| Every other fan-out at capacity, arm A | 7.77 to 8.58 ms | 12.39 to 16.39 ms |
| BIND_RX's GET_STREAM_INFO notice, arm B | 14.80 ms | 25.79 / 28.92 ms, over the 24 ms ceiling |
| A response with 7 frames owed ahead (12 ACMP) | 126.29 ms | 161.10 ms |
| The four commands behind it | none answered | two answered (176.52, 188.27 ms), two never |
| An event behind 15 others | 15.49 ms | 44.65 ms |
| An ACMP command behind a full acmp ring | 63.30 ms | 108.71 ms |
| An ENTITY_AVAILABLE behind the adp ring (observed) | 67.93 ms | 83.51 ms |
| The same, its bucket refilling (observed) | 88.33 ms | 118.81 ms |
| SHUTDOWN -> ENTITY_DEPARTING | 0.58 ms | 0.58 / 1.17 ms |

Decision input, corrected:

- **D4 (a)**: per-pass CPU work sets the time.
  - `srp_mbx.c:441-451` admits an SRP record only when no tick is owed and no event is pending. The mailbox ticks every 10 ms, so whenever every pass is over 10 ms (arm A after a bind), SRP takes nothing.
  - A notification costs 11,800 to 20,400 CPU cycles a recipient, sent one after another in one pass.
  - `memset` and `memcpy`, lwSRP's `mrp_mad`, AECP's polls and software multiply and divide are the rest.
  - A cap that keeps passes under the tick also ends SRP's starvation.
- **D4 (b)**: the event, ACMP and MAAP backlogs are ring room, and ADP, AECP and SRP are observed at their burst. Every loaded channel's last record misses T_svc. The ACMP ring's room (12) exceeds the core's owed responses (8).
- **D3**: unchanged. A flash-window read costs 15 to 29 times a block RAM fetch, and the hot set is at least 42,080 B (1x1) and 43,060 B (8x8).

## Authoritative references

- `docs/reference/FR_NFR.md` 3.4.1: markers, "the last required recipient's commit ends a notification fan-out", "backlog ... consume this budget", TX-ring backpressure; H-NOTIFY in 3.4.2.
- `docs/design/MAILBOX_SPLIT.md:495-502`, `:645-657`, `:753-758`.
- `sw/mailbox/mailbox.yaml` (token buckets, ring words, the event ring); `hdl/milan/mailbox/KL_mbx_rx.sv` (admission).
- `sw/firmware/ctrl/aecp/aecp.h` (`AECP_REGISTRATIONS`), `aecp.c` (`transmit`, the retry), `aecp_commands.c`; `sw/firmware/ctrl/srp/srp_mbx.c:441-451`; `sw/firmware/ctrl/loop/ctrl_loop.c` (`service_rx`); tsn-c-stack `acmp.h` (`ACMP_OWED_MAX`) and `acmp.c` (`room`).
- IEEE 1722.1-2021 7.5.2 (unsolicited notifications), 7.4.2.1, 7.4.15.1, 7.4.45.1; Milan v1.2 5.4.5.2, Table 5.22, Table 5.26.
- Owner decisions D3, D4 and D5 (issuecomment-6409738976).

## How to get into the same state

```sh
git fetch origin
git checkout 665-s2-cpu-budget
git submodule update --init third_party/tsn-c-stack third_party/lwSRP
```

Use the capture prerequisites (`tb/verilator/nvm_capture_cpu/README.md#run`): the product LiteX tree and its virtual environment first on `PATH`, the pinned RV32 SDK, Verilator, `LITEX_ENV_CC_TRIPLE`, `PYTHONHASHSEED=0`, `COURSIER_MODE=offline` and `SBT_OPTS=-Dsbt.offline=true`. Keep build directories outside the checkout.

## How to validate

```sh
python3 -B tb/verilator/ctrl_service_budget/run.py --self-test
python3 -B tb/verilator/ctrl_service_budget/run.py --point 1x1 --build-dir /tmp/budget-1x1 --record-budget-findings
python3 -B tb/verilator/ctrl_service_budget/run.py --point 8x8 --build-dir /tmp/budget-8x8 --record-budget-findings
python3 -B tb/verilator/ctrl_service_budget/run.py --point 1x1 --build-dir /tmp/budget-1x1-ports --variant answering-ports --groups acmp-cmd,acmp-noresp,acmp-notk,acmp-disc,backlog,backlog-adp,backlog-owed,aecp-fanout --record-budget-findings
python3 -B tb/verilator/ctrl_service_budget/run.py --point 1x1 --build-dir /tmp/budget-1x1-shutdown --variant shutdown-entry --record-budget-findings
python3 -B tb/verilator/ctrl_service_budget/run.py --point 1x1 --build-dir /tmp/budget-slow-adp --mutation slow-adp-rx
python3 -B tb/verilator/ctrl_service_budget/run.py --point 1x1 --build-dir /tmp/budget-slow-shutdown --variant shutdown-entry --mutation slow-adp-shutdown
python3 -B tb/verilator/ctrl_service_budget/run.py --point 1x1 --build-dir /tmp/budget-as-built --cpu-regions as-built
cd tests && behave
```

Expected result / pass criteria:

- The self-test prints `self-test: 0 failures` with 81 `PASS` and 52 `MUTANT caught` lines, rc 0.
- The 1x1 run prints `18 groups graded, 0 refusals, 58 T_svc misses (58 of 141 probe instances, 22 of 81 paths)`, rc 0.
- The 8x8 run prints `17 groups graded, 0 refusals, 102 T_svc misses (102 of 182 probe instances, 60 of 129 paths)`, rc 0.
- The 1x1 answering-ports run prints `8 groups graded, 0 refusals, 41 T_svc misses (41 of 68 probe instances, 18 of 44 paths)`, rc 0.
- Each figure repeats to the cycle. Each run's `table.md` lists the composed windows, their release and every record never released.
- The shutdown arm prints `2 groups graded, 0 refusals, 0 T_svc misses (0 of 2 probe instances, 0 of 1 paths)`, rc 0.
- The controls print `CONTROL slow-adp-rx caught`, `CONTROL slow-adp-shutdown caught` and `CONTROL as-built caught: an instruction access fault (cause 1)`, rc 0 each.
- behave: 14 features, 406 scenarios, 1977 steps passed.

## Known limitations / out of scope

- The rows miss T_svc: S2b (a per-pass work cap in `ctrl_loop`) follows under D4. This PR repairs no service path. The SRP starvation, the ACMP drop and the per-recipient cost are measured and reported here; whether they become Issues or S2b scope is the manager's decision.
- RESIDUE R-4 (one sentence in `docs/testing/TESTING.md`) is not applied. That file is in the release lanes' file map, which split lanes stay out of, so it is left for the residue checklist.
- A composed window closes three quiet passes, or 500 ms, after its row is served. A record still unreleased then is reported with the time it had waited by the run's end, a lower bound.
- A record's service ends at the end of its releasing pass; lwSRP may keep a record for replay and finish it later.
- In arm A the fixture's stream observation reports unavailable, so SET_CONFIGURATION, SET_STREAM_INFO, an output map edit and BIND_RX's GET_STREAM_INFO notice complete only in the answering-ports arm. At 8x8 the image's input maps have capacity 0.
- The lock expiry's notice (60 s) and the counter pushes are not run.
- The ADP, AECP and SRP backlog rows are observed at their burst; the refill leg is one sample of sustained arrivals.
- SHUTDOWN is measured through a labelled test-only entry. START_STREAMING is not run.
- Ends are mailbox commits: no wire, ingress, egress or network time; flash erase and program waits are zero; no DDR3 or datapath.
- The linked image addresses placeholder devices; #791 and #723 are open.
- The self-test is portable, but no CI job runs it yet (that registration is a CI change).
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
