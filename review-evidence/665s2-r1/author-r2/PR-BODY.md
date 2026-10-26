[A681b]

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

**Round 2: every finding of R703-1 and R704-1 is fixed at its cause, and both points are re-measured.** The measured rows still miss T_svc = 10 ms, so owner decision D4's STOP into S2b stands, as round 1 reported.

- The self-test passes 51 checks and catches 36 of 36 mutants; R703-1's twelve source mutants, adapted to this round's code, are all caught.
- Three full-harness controls are caught: `slow-adp-rx`, `slow-adp-shutdown` and `as-built`.
- Every gate is rc 0 at the head, and behave passes 406/406 scenarios.

`665-s2-cpu-budget` -> `dev-soft-core`, head `cd3525c3ddcbdb5d78bf8fccdab354c468926997` (one commit on round 1's `d58c8e22`).

## Linked Issue / roles

Relates to #665 (lane S2). Not every acceptance item is met: the rows miss T_svc (D4), and one RESIDUE item stays with the manager (see Known limitations).
Relates to #397 (re-opened by the Mark II decisions).

Executor: `[A681b]`
Internal cleared-context reviewer: `[R703]`
External reviewer: `[R704]`

## Description

The round-2 assignment is [issuecomment-6415127884](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6415127884). Every change is under `tb/verilator/ctrl_service_budget/`; no shipping RTL, SoC, firmware, CI, workflow or other doc file changes.

| Finding | What changed |
|---|---|
| R703 F1, R704 F1: the load | Every backlog group's composed window now carries every receive channel's admitted burst at once, MAAP and SRP included: ADP 8, ACMP 12, AECP 16, MAAP 7 (conflicting PROBEs of each interface's announced range) and SRP 32 records, with 15 GM events. The grader refuses a window whose committed population is not that load. The owed-frame row runs under the load too. |
| | The README states each channel's admission from its token bucket and ring: the event, ACMP and MAAP rows are at ring room, a bound; the ADP, AECP and SRP rings take their burst, fewer records than they hold, so those rows are observed. A refill leg measures the ADP row with the bucket's refill-rate arrivals up to ring room. Each probe reports the records ahead of it. |
| R703 F3, R704 F2: the fan-out | A notification ends at the last required recipient's commit: every (controller, interface) registered must receive the unsolicited response of the command's type and descriptor; a missing recipient, or a controller outside the set, is refused. |
| R703 F2: protection | Every clock conversion is one grader method; the fixture now has a composed window, and the oracle pins each row's pass bound, the worst pass and the composed maximum. 36 named mutants cover the markers, the fan-out, every conversion, the pass bound, the composition, the deadlines, the run's exit status, the regrade, reuse and the tables; each mutant marked `(d58c8e22)` restores round 1's rule. |
| R703 F5, R704 F3: reuse | Reuse and regrade attest every run input: the image, its runtime archives, every ROM `.init` file, the SoC Verilog, the generated mailbox, the CPU netlist and RAM models, and the firmware source trees. A changed, missing, unrecorded or unresolved input is refused. |
| R703 F6, R704 F4: silent drops | A selected group whose script or log is absent, or whose script is stale, is refused by name, and the run exits 1. |
| R703 F7, R704 F5: SHUTDOWN | Measured through a labelled `shutdown-entry` arm (a scratch fixture poll disables ADP once), from `adp_mbx_set_enable`'s entry to each interface's ENTITY_DEPARTING, with a planted control. |
| R703 F4: tables | Each path is reported at its worst instance across groups; misses are counted per path and per probe instance. |
| RESIDUE, suggestions | Lane labels removed from source comments; README wording per R-2 and R-3; `WIRE` parsed in print order; timed-out waits listed; flash ratio stated as 15 to 29 times. |

The receive-commit rule changed with evidence: `KL_mbx_rx` takes no byte of a frame before the previous frame's verdict (`rx_ready_o` only in `RECV_S`), and every commit observed follows its frame's last byte by 4 bus cycles. So a commit belongs to the newest pending frame, and round 1's 64-cycle heuristic could misattribute a refused frame; a check plants exactly that.

Re-measured (CPU 50 MHz, bus 100 MHz):

| Figure | 1x1, one interface | 8x8, two interfaces |
|---|---|---|
| Paths missing T_svc (instances) | 10 of 61 (11 of 78) | 37 of 106 (45 of 125) |
| Worst pass | 31.32 ms | 59.79 ms |
| Composed maximum, arm A / B | 31.32 / 14.81 ms | 44.19 / 27.84 ms |
| An event behind 15 others | 15.49 ms | 44.65 ms |
| An ACMP command behind a full acmp ring | 63.30 ms | 108.71 ms |
| An ENTITY_AVAILABLE behind the adp ring at its burst (observed) | 67.93 ms | 83.51 ms |
| The same, its bucket refilling (observed) | 88.33 ms | 118.81 ms |
| A response with 7 frames owed ahead | 125.79 ms | 151.92 ms |
| SHUTDOWN -> ENTITY_DEPARTING (test-only entry) | 0.58 ms | 0.58 / 1.17 ms |
| SET_NAME, 8x8 if1, two recipients | - | 8.39 ms (round 1 graded the first: 7.93) |

Decision input, corrected:

- **D4 (a)**: per-pass CPU work still sets the time. The 1x1 composed maximum pass, 1.57 M cycles, is `memset` 0.98 M (the AECP retry rebuilding responses), AECP 0.17 M and the mailbox driver 0.13 M; at 8x8 lwSRP's `mrp_mad` adds 0.43 M.
- **D4 (b)**: the event, ACMP and MAAP backlogs are bounded by ring room; ADP, AECP and SRP are not bounded by their burst. The loop takes at most two records of a channel a pass (one AECP record here), and passes under the load are 1.5 to 31 ms at 1x1. So a smaller ring or bucket removes whole passes from the ring rows, but no row fits T_svc while one pass can exceed it.
- **D3**: a flash-window read costs 15 to 29 times a block RAM fetch; the hot set is at least 42,080 B (1x1) and 43,060 B (8x8).

## Authoritative references

- `docs/reference/FR_NFR.md` 3.4.1: markers, the last required recipient ends a fan-out, W + T_svc.
- `docs/design/MAILBOX_SPLIT.md:495-502`, `:645-657`, `:753-758` (rows), `:453-470` (A1 to A4).
- `sw/mailbox/mailbox.yaml` (token buckets, ring words, the range filter); `hdl/milan/mailbox/KL_mbx_rx.sv` (admission, `rx_ready_o`).
- IEEE 1722.1-2021 7.5.2 (unsolicited notifications), 6.2.5.2.2 (ENTITY_DEPARTING); IEEE 1722-2016 B.3.6.6 (DEFEND); Milan v1.2 Table 5.54.
- Owner decisions D3, D4 and D5 (issuecomment-6409738976); the round-1 assignment (issuecomment-6409745905).

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
python3 -B tb/verilator/ctrl_service_budget/run.py --point 1x1 --build-dir /tmp/budget-1x1-shutdown --variant shutdown-entry --record-budget-findings
python3 -B tb/verilator/ctrl_service_budget/run.py --point 1x1 --build-dir /tmp/budget-slow-adp --mutation slow-adp-rx
python3 -B tb/verilator/ctrl_service_budget/run.py --point 1x1 --build-dir /tmp/budget-slow-shutdown --variant shutdown-entry --mutation slow-adp-shutdown
python3 -B tb/verilator/ctrl_service_budget/run.py --point 1x1 --build-dir /tmp/budget-as-built --cpu-regions as-built
cd tests && behave
```

Expected result / pass criteria:

- The self-test prints `self-test: 0 failures` with 36 `MUTANT caught` lines, rc 0.
- The 1x1 run prints `17 groups graded, 0 refusals, 11 T_svc misses (11 of 78 probe instances, 10 of 61 paths)`, rc 0; the 8x8 run `16 groups graded, 0 refusals, 45 T_svc misses (45 of 125 probe instances, 37 of 106 paths)`, rc 0. Each figure repeats to the cycle.
- The shutdown arm prints `2 groups graded, 0 refusals, 0 T_svc misses`, rc 0.
- The controls print `CONTROL slow-adp-rx caught`, `CONTROL slow-adp-shutdown caught` and `CONTROL as-built caught: an instruction access fault (cause 1)`, rc 0 each.
- behave: 14 features, 406 scenarios, 1977 steps passed.

## Known limitations / out of scope

- The rows miss T_svc: S2b (a per-pass work cap in `ctrl_loop`) follows under D4. This PR repairs no service path.
- RESIDUE R-4 (one sentence in `docs/testing/TESTING.md`) is not applied: that file is in the release lanes' file map, which split lanes stay out of. It is left for the residue checklist.
- The ADP, AECP and SRP backlog rows are observed at their burst; the refill leg is one sample of sustained arrivals, not a bound.
- SHUTDOWN is measured through a labelled test-only entry; the linked image never disables ADP. START_STREAMING is not run (the fixture leaves its port empty).
- Ends are mailbox commits: no wire, ingress, egress or network time; flash erase and program waits are zero; no DDR3 or datapath.
- The linked image addresses placeholder devices; #791 (the split SoC's region decode) and #723 (the stack-protector runtime) are open.
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
