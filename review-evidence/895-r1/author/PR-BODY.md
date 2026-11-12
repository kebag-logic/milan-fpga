[A775]

## Contents

- **[Status](#status)** — REVIEW READY at the head below; the gate pass, the loads and the ROM ledger.
- **[Linked Issue / roles](#linked-issue--roles)** — Public task, executor, and independent reviewers.
- **[Description](#description)** — The validity gate, the declarations and withdrawals, the tests and plants, the costs, the ledger.
- **[Authoritative references](#authoritative-references)** — Requirements/specification clauses and docs.
- **[How to get into the same state](#how-to-get-into-the-same-state)** — Checkout, submodules and environment.
- **[How to validate](#how-to-validate)** — Exact reviewer commands and expected result.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** — What this does not do, and the items for a decision.
- **[Definition of Done](#definition-of-done)** — The merge bar from [CONTRIBUTING.md](../CONTRIBUTING.md).

## Status

REVIEW READY at `d023b77a7bf677205e45195e0e1f0daf80d1a4d4` (`895-talker-redeclare` -> `dev-soft-core`): base `66f71326`, #810's round 29 heads `7f50ee6a` and `b2d39235` merged by one merge commit each, then this lane's commits. No rebase, no force, no amend. No RTL, mailbox-contract, tsn-c-stack, lwSRP or donor change; the tsn-c-stack submodule stays at `715589c` (#810's). The PR lands after #810.

The full gate pass ran once, on clean clones of this head; every gate passed:
- **Workflows:** every `run:` step of `rtl-fast.yml`, `rtl.yml`, `elaborate.yml` and `docs.yml`, the four a pull request to `dev-soft-core` triggers, each job on its own fresh clone. 139 steps ran, all rc 0; 226 are not run, each with its stated reason; 0 bad. All 28 job trees were clean after.
- **Firmware:** the self-test passes, with 0 escapes in its campaigns: control 696 of 696 caught, AECP 227, SRP 392 (this lane's 28 Talker plants among them).
- **Coverage and boundary:** `fw_coverage.py --check` and the TSN stack boundary both pass.
- **Harness:** the CPU budget harness at both points in every arm, below.
- **Other gates:** `test_builder.py --require-rv32`, `behave` (508 scenarios), the split boot simulation and its self-test, and `git diff --check` all pass.

- **Acceptance 1 and 2** (Milan v1.2 4.3.3.1, 5.3.7.4; IEEE 802.1Q-2018 35.2.2.8): a source declares nothing until its SRP parameters are valid, then at once, on its own interface, at MAAP's base + n; it withdraws when validity lapses; an unchanged destination comes back at once and a changed one two LeaveAllTime periods after the Leave. The boot-time Talker Failed is gone.
- **Acceptance 3**: 9 unit tests at 1x1/1if and 8x8/2if and 3 composition tests at 8x8/2if; 28 planted Talker defects, each killed by its named test on its words at both points; `fw_coverage.py --check` at 100 % of `srp_mbx.c` (724/724 lines, 653/653 branches) and `ctrl_app_srp.c` (89/89, 72/72).
- **Acceptance 4**: 1x1/1if **0.488** at the pin and **0.486** with tsn-c-stack#32, each within 0.70 (`load_grade.py --check` exits 0). 8x8/2if 0.817 and 0.768, reported against 0.75: over by 0.067 and 0.018, as it was before this change (0.816 and 0.767). The least row margin by measurement is 9.733 ms at 8x8/2if (arm A) and 11.255 ms at 1x1/1if.
- **Acceptance 5**: every ROM ledger point holds. The platform's 8x8/2if image plans 60.0 RAMB36 (ledgered 60.0, cap 60.5), recording 4.0 RAMB36 = 16,384 B of cold code owed to S14. The size fixture's 8x8/2if image plans 58.0; its point is ledgered at 58.5, its cap, because the CPU budget harness's `answering-every-port` arm of that image plans 58.5. Every other point is at or under 53.0.
- **Acceptance 6** (hardware) is the bench lane's.

## Linked Issue / roles

Relates to #895
Relates to #810 (merged here; this PR lands after it)
Relates to #896 (its trigger, examined below; its fix is its own)
Relates to #665

Executor: `[A775]`
Internal cleared-context reviewer: to be assigned
External reviewer: to be assigned

## Description

### Validity and its feed

A destination is valid when MAAP holds the interface's range with no conflict, and a PROBE_TX_COMMAND for the output was answered in the last 15 s or a matching Listener is registered (Milan v1.2 4.3.3.1). That is ACMP's `acmp_declaring`, which the MAAP adapter already publishes per interface as its DA gate (`maap_mbx.c` `published_gate`). The composition's delivery poll (`ctrl_app_srp.c`) hands each interface's gate and range base to SRP every pass (`srp_mbx_gate`). SRP records the change, gives each valid source the destination base + n (Milan v1.2 5.5.4.1), and owes THE TRANSMIT's declarations. The entry calls no lwSRP function, makes no mailbox access, and refuses before attach and on reentry. DA_GATE is read from RAM, so **no mailbox contract change**.

### Declarations and withdrawals (`srp_mbx.c` `declare_sources`, in THE TRANSMIT's pass)

| Source | SRP |
|---|---|
| not valid | declares nothing (no boot-time Talker Failed) |
| valid | declares at once: Talker Advertise when admitted (75 % of the link), else Talker Failed, code 1; on its own interface only |
| validity lapses (no probe for 15 s and no Listener, or MAAP loses or restarts the range) | withdraws: LICENCE closed, then `TALKER_DECL` and `IDLE_SLOPE` drop it, then the Leave of its declared type |
| destination changes while valid | withdraws the old destination first |
| valid again, same destination | declares at once (35.2.2.8: the same FirstValue) |
| valid again, changed destination | declares once `SRP_REDECLARE_CS` (2 x 1000 cs + a JoinTime + THE TRANSMIT's bound) has passed since the Leave's request |
| admission changes | swapped in place, the new type joined first; a refused join keeps the declared type |
| link reset | the new participants hold a source whose destination moved; an unchanged one declares at once |

The unit fixture has no gate: `srp_mbx_config.sources_valid` declares every source from creation, so the existing SRP suites run unchanged. `srp_bounds.h` restates THE TRANSMIT's publications within the poll's terms.

### Tests and planted defects

| Suite | Point | Covers |
|---|---|---|
| `srp_talker.cpp` (`Talker.*`, 9) | 1x1/1if, 8x8/2if | allocation, nothing before valid, lapse and withdrawal, unchanged and changed destination, a change while valid, admission swaps, reset, the entry, a refused declaration |
| `test_acmp_mbx.cpp` `SrpGate.*` (`srp_gate.hpp`, 3) | 8x8/2if | through ADP, ACMP, MAAP and SRP: a probe and its 15 s expiry; a registered Listener past the window; a range lost to a peer's ANNOUNCE (MAAP restarts), the new range's base + n declared only after the hold-off |

`srp_talker_mutants.py` plants 28 defects, one a rule, each refused by its named test on its own words, in the two-interface campaign at 8x8/2if and the one-interface campaign at 1x1/1if. 16 existing SRP plants are re-anchored on the new `declare_sources`.

### The CPU budget harness

A `valid-destinations` arm (`talker_window.py`) makes the fixture's ACMP source port the platform's in a scratch copy. Its `srp-talker` group probes every source, then waits past the 15 s window. Its `srp-talker-loss` group probes every source, then a peer takes each interface's range. Each probe is a row on its interface, with a JoinTime's wait, as the `srp` group's Domain row states. Every pass is held to THE TRANSMIT's stated build cost and to the per-pass share.

On the simulated wire, at both points:
- nothing is declared before the first probe;
- each source's Advertise carries MAAP's base + n on its own interface;
- the window's end withdraws each source 15.0 to 15.2 s after its probe;
- the loss withdraws each source at the interface's next transmit opportunity;
- nothing follows a Leave, and no Talker Failed appears at any time.

### Costs, fed to the load gate's tables

The legs are every group of arm A and of the `answering-every-port` arm, both `valid-destinations` groups, and arm B's `aecp` group, at both points. They show 0 refusals, no work pass over the share and no pass over its stated cost. Arm A's 7 budget misses (7 of 945 and 7 of 996 probe instances) are the merged head's seven, which tsn-c-stack #26 holds.

The new work:
- **The gate's hand-off** is in the polls' base. Its most is 15,078 and 27,578 CPU cycles, each 422 under `poll_grade.py`'s 155 and 280 us, which are unchanged.
- **The hold-off countdown** is in a centisecond's consumers, at most 19,596 cycles at 8x8/2if, under the 510 us stated.
- **The declaration and withdrawal passes** are THE TRANSMIT's builds, under `ctrl_loop.h`'s costs.

The table rule, unchanged: each cost is the larger of the measurement and the committed table's. It moves:
- MAAP's record, at a range lost to a peer's ANNOUNCE: 90 to 115 and 130 to 150 us.
- AECP's timer slot at 1x1/1if: 60 to 65 us.
- A TICK at 8x8/2if: 40 to 45 us.
- With tsn-c-stack#32 only: the polls' base 155 to 160 and 285 to 290 us; at 1x1/1if, ACMP's owed frame 120 to 125 and the registrar walk 20 to 25 us.

The load moves 0.001 to 0.003, and no row of the flip check changes its verdict. 1x1/1if R4 goes 66.12 to 66.77 ms; it was red before. `SPLIT_CONTROL_MEMORY.md` section 13 is restated.

### ROM

| Point | Fixture rom / sram, B | Fixture RAMB36 | Platform rom / sram, B | Platform RAMB36 |
|---|---:|---:|---:|---:|
| 1x1/1if | 108,872 / 45,568 | 38.5 | 113,936 / 46,576 | 39.5 |
| 1x1/2if | 110,664 / 56,976 | 41.5 | 115,760 / 58,032 | 43.0 |
| 8x8/1if | 122,400 / 86,464 | 51.5 | 127,504 / 87,456 | 53.0 |
| 8x8/2if | 124,136 / 112,624 | 58.0 (ledgered 58.5) | 129,288 / 113,632 | 60.0 (ledgered 60.0) |

The fixture's `answering-every-port` arm at 8x8/2if needs 112,688 B of `sram`, 48 B past the 112,640 that 58.0 holds. This change adds 48 B of RAM there: SRP's interface struct grows 624 to 640 B (8-byte aligned), its config by 4 B, and the hold-off counters take 18 B. The ruling's cuts (16-bit masks moved out of the interface struct, one hold-off counter an interface, no config flag) recover about 30 B. So the point is ledgered at 58.5, its cap, as the ruling provides. `ctrl_memory.py`, `ctrl_memory_ledger.py`, `test_ctrl_memory.py` and `SPLIT_CONTROL_MEMORY.md` sections 3 and 5 are updated.

### #896

#896 correlates every false Listener withdrawal with churn on the board's own failed talker stream. At the base, every source declared Talker Failed (code 2, no destination) on every interface from creation, and never re-declared after MAAP allocated. At this head a source declares nothing until valid, and then a Talker Advertise with its destination. So the standing Talker Failed that the trigger correlates with is gone in #878's configuration.

The mechanism is untouched: `capture()`, its `withdrawn` flag and the Listener path are unchanged, and a transient empty read on another stream's churn can still become a Leave. #896 keeps its host replay and its fix.

## Authoritative references

- Milan v1.2 4.3.3.1 (a valid destination), 5.3.7.2 and 5.3.7.4 (a Stream Output's Talker attribute), 5.5.4.1 (base + n).
- IEEE 802.1Q-2018 35.2.2.8 (no changed FirstValue; two LeaveAllTime periods; the same FirstValue at once), 35.2.2.8.7 and Table 35-6 (FailureInformation, codes 1 and 2), 10.7.4.1 (the jointimer's transmit opportunities), Table 10-7 (JoinTime 20 cs, LeaveAllTime 1000 cs).
- IEEE 1722-2016 Annex B: Table B.7 (rAnnounce! in DEFEND, Restart!), B.3.6.4 (compare_MAC), B.3.5.3.
- [`sw/firmware/ctrl/srp/README.md`](../sw/firmware/ctrl/srp/README.md), [`docs/design/MAILBOX_SPLIT.md`](../docs/design/MAILBOX_SPLIT.md) (`TALKER_DECL`), [`docs/design/SPLIT_CONTROL_MEMORY.md`](../docs/design/SPLIT_CONTROL_MEMORY.md) sections 3, 5 and 13, [`tb/verilator/ctrl_service_budget/README.md`](../tb/verilator/ctrl_service_budget/README.md) (the `valid-destinations` arm).
- The ruling of 2026-11-12 on #895 (issuecomment-6824623445), maintainer-delegated.

## How to get into the same state

```sh
git fetch origin
git checkout --detach d023b77a7bf677205e45195e0e1f0daf80d1a4d4
git submodule update --init protocol-processor gptp-processor third_party/lwSRP third_party/tsn-c-stack third_party/verilog-axis
# the CPU budget harness's prerequisites (its README, "Run and reproduce"): the product LiteX tree's environment,
# the pinned RV32 SDK on PATH, Verilator 5.050, COURSIER_MODE=offline, SBT_OPTS=-Dsbt.offline=true
export PYTHONHASHSEED=0 LITEX_ENV_CC_TRIPLE=riscv32-buildroot-linux-gnu
```

## How to validate

```sh
python3 -B sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test
python3 -B sw/firmware/gtest/fw_coverage.py --check
python3 -B tb/verilator/ctrl_service_budget/load_grade.py --check
python3 -B tb/verilator/ctrl_service_budget/flip_grade.py --check          # exits 1 by design (#890, #894)
python3 -B sw/litex/test_ctrl_memory.py
python3 -B tb/verilator/ctrl_service_budget/run.py --point 1x1 --build-dir <scratch>/vd-1x1 --variant valid-destinations
python3 -B tb/verilator/ctrl_service_budget/run.py --point 8x8 --build-dir <scratch>/vd-8x8 --variant valid-destinations
python3 -B tb/verilator/ctrl_service_budget/run.py --point 1x1 --build-dir <scratch>/a-1x1 --record-budget-findings
python3 -B tb/verilator/ctrl_service_budget/run.py --point 8x8 --build-dir <scratch>/a-8x8 --record-budget-findings
python3 sw/builder/test_builder.py --require-rv32
(cd tests && behave --no-capture -f plain)
git diff --check 66f713267f201d1a00d7f711e04b3a996d804dee HEAD
```

Expected result / pass criteria:

- Every `run:` step of `rtl-fast.yml`, `rtl.yml`, `elaborate.yml` and `docs.yml` is rc 0 or not run with its reason. In this pass, 139 steps ran rc 0 and 226 were not run: hosted orchestration, installs this host carries, and `rtl.yml`'s full sweep, which an RTL change would need and this lane makes none.
- `test_ctrl_firmware.py --require-rv32 --self-test`: `test_ctrl_firmware: PASS`, every planted defect caught (control 696, AECP 227, SRP 392; 0 escaped).
- `fw_coverage.py --check`: `firmware coverage: PASS (39 files)`, `srp_mbx.c` 724/724 lines and 653/653 branches, `ctrl_app_srp.c` 89/89 and 72/72.
- `load_grade.py --check`: rc 0, `HELD 1x1/1if at the pin: the load 0.488` and `with tsn-c-stack#32: the load 0.486`, ceiling 0.70. `--selftest`: 25 of 25 planted controls refused.
- `flip_grade.py --check`: rc 1 by design (8x8/2if over 0.70; R4 at both points and R5, R6 at 8x8/2if, as before this change). `--selftest`: 131 of 131.
- `test_ctrl_memory.py`: `RESULT: PASS`; the size fixture's 8x8/2if point plans at 58.5 and the platform's at 60.0, each by name.
- The harness, `valid-destinations` arm: 0 refusals, 0 of 5 and 0 of 20 budget misses, no work pass over the share. The Talker rows reach at most 199.4 of 220 ms.
- The harness, arm A: 0 refusals; 7 of 945 and 7 of 996 misses, the merged head's seven (tsn-c-stack #26); no pass over the share or over its stated cost.
- How this pass ran the harness at the head: each arm's point was built there. Its image's loadable bytes equal the measurement build's, and its Verilog is identical but for comments. One group per arm was re-run, with a log byte-identical to the measured one, and every measured group was regraded rc 0 by the head's graders.
- `test_builder.py --require-rv32` and `behave` (508 scenarios, 2,330 steps) pass.
- `git diff --check` is clean against the base and #810's merged head.

## Known limitations / out of scope

- **Hardware** (acceptance 6): one stream each way with the reference peer, every counter checked at both ends, is the bench lane's.
- **The split boot simulation** (`tb/verilator/ctrl_split_boot`) boots the platform image with an idle datapath and no frame input, so the wire evidence comes from the CPU budget harness's split SoC simulation. There the fixture's source port is made the platform's, which reports the same base + n.
- **For a decision, recorded and not resolved here:**
  - A Domain adoption re-declares every declared source in place with a changed vlan_identifier, a FirstValue field 35.2.2.8 does not let a Talker change either. This is unchanged and outside #895; to be proposed as an issue.
  - The datapath has one stream window, interface 0's (`ctrl_plat.c`). Pre-existing.
- **A change of behavior a reviewer should see:** each source is now declared on its own interface only; before, every interface declared every source.
- **Thin margins, unchanged by this lane's bounds:**
  - the polls' base at both points, 422 cycles under `poll_grade.py`'s;
  - the 1x1/1if registrar walk, 1,987 cycles against 2,000, in arm A's `srp` group. This change does not touch the walk.
- 8x8/2if's load is over 0.75 at the pin and with tsn-c-stack#32, as before this change; its flip is #890's.

## Definition of Done

- [x] Linked Issue acceptance criteria are satisfied (1 to 5 here; 6 is the bench lane's)
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
