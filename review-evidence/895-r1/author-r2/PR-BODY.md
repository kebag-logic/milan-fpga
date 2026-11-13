[A775]

## Contents

- **[Status](#status)** — REVIEW READY at the head below; round 2's delta, the gate pass, acceptance 4 by the ruling.
- **[Linked Issue / roles](#linked-issue--roles)** — Public task, executor, and independent reviewers.
- **[Round 2](#round-2)** — Each item of the ruling of 2026-11-13 and what answers it.
- **[Acceptance 4: no regression beyond stated deltas](#acceptance-4-no-regression-beyond-stated-deltas)** — Every flip-gate figure, head against base.
- **[Description](#description)** — The validity gate, the declarations and withdrawals, the tests and plants, the costs, the ledger.
- **[Authoritative references](#authoritative-references)** — Requirements/specification clauses and docs.
- **[How to get into the same state](#how-to-get-into-the-same-state)** — Checkout, submodules and environment.
- **[How to validate](#how-to-validate)** — Exact reviewer commands and expected result.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** — What this does not do, and the items for a decision.
- **[Definition of Done](#definition-of-done)** — The merge bar from [CONTRIBUTING.md](../CONTRIBUTING.md).

## Status

REVIEW READY at `18300f6e5f0c63b2ebc81d6bbc243496034f638a` (`895-talker-redeclare` -> `dev-soft-core`), round 2: base `66f71326`, #810's round 29 heads `7f50ee6a` and `b2d39235` merged by one merge commit each, then this lane's commits. `665-s2b-cycles` read `b2d39235` at the round's start, before each set of legs and at 09:40 CET, before the gate pass started at 09:43. #810's round 30 REVIEW READY (`5bea2597`, on #665) came at 10:10 CET, after it, and the branch is now `32551422`, under review; by the ruling's item 6 (merge only a round 30 REVIEW READY before the gate pass) it is not merged here, and composing this lane with it is the next step after its review. No rebase, no force, no amend. No RTL, mailbox-contract, tsn-c-stack, lwSRP or donor change; the tsn-c-stack submodule stays at `715589c` (#810's). The PR lands after #810.

The full gate pass ran once, on clean clones of this head:
- **Workflows:** every `run:` step of `rtl-fast.yml`, `rtl.yml`, `elaborate.yml` and `docs.yml`, each job on its own fresh clone. 139 steps ran, all rc 0; 226 are not run, each with its stated reason; 0 bad. Every job tree was clean after.
- **The full Verilator sweep** (`scripts/run_all_suites.sh`, the 65 suites `rtl.yml`'s shards run) as four shard units on clones of this head: 65 suites, 0 in-suite check failures. 62 passed as run. `gptp_shadow`, `gptp_tables` and `mbx` failed only in their planted-defect scripts, which read `make`'s output and met its directory messages under the shard runner's `MAKEFLAGS=-j4` (`rtl.yml` sets `-jN --no-print-directory`); re-run on the same clone with CI's form, each passed (make rc 0, tally verdict rc 0), their plants caught (9, 26, and 7 and 21 controls). This lane changes no RTL.
- **Firmware:** the self-test passes, with 0 escapes in its campaigns: control 696 of 696 caught, AECP 227, SRP 398 (the 29 Talker plants at both points among them).
- **Coverage and boundary:** `fw_coverage.py --check` (39 files) and the TSN stack boundary both pass; the saved-state store gate, 455 tests.
- **Harness:** the CPU budget harness at both points in every arm, built at this head: each image's loadable bytes equal this round's measurement legs' builds, a sample group per arm is byte-identical to its measured log, and every measured group regrades rc 0 by the head's graders.
- **Other gates:** `test_builder.py --require-rv32`, `behave` (508 scenarios), the split boot simulation and its self-test, `test_ctrl_memory.py` and `git diff --check` all pass; `flip_grade.py --check` exits 1 at the head as at the base (below).

- **Acceptance 1 and 2** (Milan v1.2 4.3.3.1, 5.3.7.4; IEEE 802.1Q-2018 35.2.2.8): a source declares nothing until its SRP parameters are valid, then at once, on its own interface, at MAAP's base + n; it withdraws when validity lapses, and a Leave lwSRP refuses is kept owed until lwSRP takes it; an unchanged destination comes back at once and a changed one two LeaveAllTime periods after the Leave. The boot-time Talker Failed is gone.
- **Acceptance 3**: 11 unit tests at 1x1/1if and 8x8/2if and 3 composition tests at 8x8/2if; 29 planted Talker defects, each killed by its named test on its words at both points; `fw_coverage.py --check` at 100 % of `srp_mbx.c` (725/725 lines, 651/651 branches) and `ctrl_app_srp.c` (89/89, 72/72).
- **Acceptance 4**, stated by the ruling of 2026-11-13: no regression beyond stated deltas. The 1x1/1if long-window load is **0.488** at the pin and **0.486** with tsn-c-stack#32, each at most 0.70 (`load_grade.py --check` exits 0). Every other flip-gate figure is measured at this head and at the base [below](#acceptance-4-no-regression-beyond-stated-deltas), and its delta stated; they are the deltas the ruling accepted at `d023b77a`, unchanged.
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

## Round 2

The ruling of 2026-11-13 on #895 (issuecomment-6840463408) answers R835-1 (PR #901 issuecomment-6840458159) and R836-1
(issuecomment-6840411046), both NEGATIVE at `d023b77a`:

| Item | Finding | What answers it |
|---|---|---|
| 1 | R835-1-F1, R836-1 F1 (MAJOR): acceptance 4 stated "met" | Acceptance 4 is stated by the ruling ([below](#acceptance-4-no-regression-beyond-stated-deltas)): the 1x1/1if long-window load at most 0.70, and every other flip-gate figure measured at this head and at the base with its delta. It is never stated "met". |
| 2 | R835-1-F2, R836-1 F2 (a): section 13's 8x8/2if pass cost | `SPLIT_CONTROL_MEMORY.md` section 13's table carries `load_grade.py --check`'s figures at this head, the pass cost included. |
| 2 | R836-1 F2 (b): section 5's rom growth | Section 5 carries the eight images at this head and their growth over #810's round 29 head `b2d39235`, each linked at both commits: +944 to +1,064 B of `rom` (R836-1 measured the same at `d023b77a`; the page said 800 to 1,040), +16 to +64 B of `sram`, `ctrl_plat` +64 B. |
| 2 | R835-1-F3, R836-1 F3: the plant count | Round 1 stated 28 Talker plants; `d023b77a`'s table holds 26. This round adds 3, so this head's holds 29: `len(srp_talker_mutants.defects())`, and 58 `[ok] talker-` lines in the SRP campaign, 29 at each point. |
| 3 | R835-1-F4 (MINOR; R836-1 RS2): `srp_bounds.h`'s count | The argument states what the code does: IDLE_SLOPE and TALKER_DECL at most once a declarations pass, so at most twice on the interface THE TRANSMIT's call builds (its declarations after the build make what the first pass could not); SR_DOMAIN once for an adoption; LICENCE once for each licence a withdrawal closes; at most 5 + MBX_N_PUB_SOURCES writes an interface. `SRP_MBX_PUB_POLL_MAX` is unchanged. `Talker.TransmitPublishesWithinItsTermsAfterARefusedJoin` counts one call's writes with a refused join (2 and 2 on the built interface, 1 and 1 on the other, LICENCE 1, SR_DOMAIN 0); the plant `talker-transmit-publishes-past-its-terms` is caught at both points. |
| 4 | R835-1-F5 (MINOR): a refused withdrawal Leave | `declare_sources` reads `mrp_mad_leave`'s answer. Refused, the source stays declared (its `talkers` bit, so `TALKER_DECL` and `IDLE_SLOPE` too, as lwSRP still declares it), no hold-off starts, and the withdrawal is owed. THE TRANSMIT's next call starts with no frame owed (`transmit_aged`), so its first declarations take the Leave; the hold-off starts there. `Talker.RefusedWithdrawalIsWithdrawnOnceLwsrpTakesIt` runs the reviewer's sequence through the real reclaim, at both points, and reads the Leave on the wire; plants `talker-refused-withdrawal-forgotten` (round 1's code) and `talker-refused-withdrawal-not-owed` are caught at both points. No lwSRP change. |
| 4 | the Domain's own leave and join on that path (`change_domain`) | Confirmed by a probe test at both points, and **not fixed here**: it is not the same mechanism (below, Known limitations). For a separate issue. |
| 5 | R835-1-RS1, R836-1 RS1 | `ctrl_memory.py`'s ledger reasons carry `(#895)` alone, and "the cold-code move to flash owes" for the lane name. |
| 5 | R835-1-RS2 | The SRP README's Talker paragraph opens "A declared output's first declaration is ..." and qualifies code 2 "Without a DA gate (`sources_valid`)". Optional R835-1-S2 taken there: the hold-off reads two LeaveAllTime periods as twice the configured 1000 cs. S1 (an 8x8/2if wake-up plant) not taken. |
| 6 | the base | `665-s2b-cycles` read `b2d39235` at the round's start, before each set of legs and at 09:40 CET, before the gate pass started at 09:43. #810's round 30 REVIEW READY (`5bea2597`, on #665) came at 10:10 CET, after it, and the branch is now `32551422`, under review; by the ruling's item 6 (merge only a round 30 REVIEW READY before the gate pass) it is not merged here, and composing this lane with it is the next step after its review. The gate pass then ran once, on this head. |

The firmware changed (item 4), so every cost leg ran again on this round's firmware, and the load gate's tables were
fed from them by round 1's rule ([below](#costs-fed-to-the-load-gates-tables)).

## Acceptance 4: no regression beyond stated deltas

Acceptance 4 as amended by the ruling of 2026-11-13 (issuecomment-6840463408): **no regression beyond stated deltas.** The 1x1/1if long-window load stays at most 0.70, and every other flip-gate figure is measured at the head and at the base with its delta. The figures below other than the 1x1/1if load belong to #894 (the 1x1/1if rows by every source), #890 (the 8x8/2if load against 0.75) and tsn-c-stack #26 (the measured egress-held rows); the flip gate itself is judged at their composition with this change. Acceptance 4 is stated here by that ruling, not as met or unmet.

Graders: `load_grade.py --check` and `flip_grade.py --check`, run at this head and at the base `b2d39235` (#810 round 29). The load gate's tables did not move this round (every measurement of this round's legs is within the committed tables, in both columns), so the head's figures equal `d023b77a`'s to the last digit, and the deltas are the ones the ruling accepted there.

| Point | Figure | Ceiling or bound | Base `b2d39235` | Head | Delta | Owner |
|---|---|---|---:|---:|---:|---|
| 1x1/1if | long-window load at the pin | 0.70 (merge gate) | 0.486 | **0.488** | +0.002 | this lane: HELD, 0.212 under |
| 1x1/1if | the same with tsn-c-stack#32 | 0.70 (merge gate) | 0.483 | **0.486** | +0.003 | this lane: HELD, 0.214 under |
| 1x1/1if | R4 by every source | 20 ms | 66.12 ms | 66.77 ms | +0.65 ms | #894 (over at both) |
| 1x1/1if | R5 by every source | 90 ms | 35.95 ms | 36.24 ms | +0.29 ms | #894 (within at both) |
| 1x1/1if | R6 by every source | 90 ms | 28.67 ms | 28.92 ms | +0.25 ms | #894 (within at both) |
| 1x1/1if | first / last queued notice | 20 / 125 ms | 20.00 / 22.00 ms | 20.00 / 22.00 ms | 0 / 0 | #894 |
| 8x8/2if | long-window load at the pin | 0.75 (#890; `flip_grade.py` holds 0.70) | 0.816 | 0.817 | +0.001 | #890 (over at both) |
| 8x8/2if | the same with tsn-c-stack#32 | 0.75 | 0.767 | 0.768 | +0.001 | #890 (over at both) |
| 8x8/2if | R4 / R5 / R6 by every source | 20 / 90 / 90 ms | 346.15 / 144.15 / 135.80 ms | 347.69 / 144.53 / 136.15 ms | +1.54 / +0.38 / +0.35 ms | #894 (over at both) |
| 8x8/2if | first / last queued notice | 20 / 125 ms | 22.00 / 62.00 ms | 22.00 / 62.00 ms | 0 / 0 | #894 |

Rows by measurement (the CPU budget harness, split SoC, the CPU on `sys` at 100 MHz). The base's are #810 round 29's legs as the base tree's own `SPLIT_CONTROL_MEMORY.md` section 13 records them; the head's are this round's legs, every group of every arm at both points, on this head's firmware:

| Point | Figure | Base `b2d39235` | Head | Delta |
|---|---|---|---|---|
| 8x8/2if | arm A misses (probe instances, paths) | 7 of 996 (4 of 136) | 7 of 996 (4 of 136) | 0: the three rows tsn-c-stack #26 holds |
| 8x8/2if | `answering-every-port` misses; arm B `aecp` | 0 of 736; 0 of 39 | 0 of 736; 0 of 39 | 0 |
| 8x8/2if | least row margin, arm A | 8.973 ms | 9.718 ms | +0.745 ms |
| 8x8/2if | least row margin, `answering-every-port` | 6.246 ms | 7.879 ms | +1.633 ms |
| 8x8/2if | work passes over the 200,000-cycle share | 0 | 0 (heaviest 173,458 cycles) | 0 |
| 8x8/2if | `valid-destinations` (this lane's arm) | none | 0 of 20; least margin 20.767 ms | new |
| 1x1/1if | arm A misses | 7 of 945 (4 of 87) | 7 of 945 (4 of 87) | 0: tsn-c-stack #26 |
| 1x1/1if | least row margin, arm A / `answering-every-port` | 11.006 / 9.080 ms | 11.233 / 9.036 ms | +0.227 / -0.044 ms |
| 1x1/1if | `answering-every-port` misses; arm B; `valid-destinations` | 0 of 280; 0 of 25; none | 0 of 280; 0 of 25; 0 of 5 | 0 |

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
| a withdrawal's Leave lwSRP refuses (its participant holds an MRPDU the ring refused) | the source stays declared (`TALKER_DECL`, `IDLE_SLOPE`) and owed; THE TRANSMIT's next call, which starts with no frame owed, takes the Leave, and the hold-off starts there |

The unit fixture has no gate: `srp_mbx_config.sources_valid` declares every source from creation, so the existing SRP suites run unchanged. `srp_bounds.h` states THE TRANSMIT's publications within the poll's terms: IDLE_SLOPE and TALKER_DECL at most once a declarations pass, so at most twice on the interface the call builds, SR_DOMAIN once for an adoption, LICENCE once for each licence a withdrawal closes.

### Tests and planted defects

| Suite | Point | Covers |
|---|---|---|
| `srp_talker.cpp` (`Talker.*`, 11) | 1x1/1if, 8x8/2if | allocation, nothing before valid, lapse and withdrawal, unchanged and changed destination, a change while valid, admission swaps, reset, the entry, a refused declaration, THE TRANSMIT's publications counted in one call with a refused join, a withdrawal whose Leave lwSRP refuses (the Leave on the wire once lwSRP takes it) |
| `test_acmp_mbx.cpp` `SrpGate.*` (`srp_gate.hpp`, 3) | 8x8/2if | through ADP, ACMP, MAAP and SRP: a probe and its 15 s expiry; a registered Listener past the window; a range lost to a peer's ANNOUNCE (MAAP restarts), the new range's base + n declared only after the hold-off |

`srp_talker_mutants.py` plants 29 defects, one a rule, each refused by its named test on its own words, in the two-interface campaign at 8x8/2if and the one-interface campaign at 1x1/1if (round 1 stated 28; `d023b77a`'s table held 26, and this round adds `talker-transmit-publishes-past-its-terms`, `talker-refused-withdrawal-forgotten` and `talker-refused-withdrawal-not-owed`). 16 existing SRP plants were re-anchored on the new `declare_sources` in round 1, and four Talker plants and `srp_pub_mutants.REFUSAL_OWED` follow the withdrawal's new lines.

### The CPU budget harness

A `valid-destinations` arm (`talker_window.py`) makes the fixture's ACMP source port the platform's in a scratch copy. Its `srp-talker` group probes every source, then waits past the 15 s window. Its `srp-talker-loss` group probes every source, then a peer takes each interface's range. Each probe is a row on its interface, with a JoinTime's wait, as the `srp` group's Domain row states. Every pass is held to THE TRANSMIT's stated build cost and to the per-pass share.

On the simulated wire, at both points:
- nothing is declared before the first probe;
- each source's Advertise carries MAAP's base + n on its own interface;
- the window's end withdraws each source 15.0 to 15.2 s after its probe;
- the loss withdraws each source at the interface's next transmit opportunity;
- nothing follows a Leave, and no Talker Failed appears at any time.

### Costs, fed to the load gate's tables

The legs are every group of arm A and of the `answering-every-port` arm, both `valid-destinations` groups, and arm B's `aecp` group, at both points, run again this round on this head's firmware (`17ac263f`; later commits change docs and the coverage ratchet only). They show 0 refusals, no work pass over the share (the heaviest 173,458 cycles, 8x8/2if `notice-every-5`) and no pass over its stated cost. Arm A's 7 budget misses (7 of 945 and 7 of 996 probe instances) are the merged head's seven, which tsn-c-stack #26 holds.

The new work:
- **The gate's hand-off** is in the polls' base. Its most is 15,078 and 27,578 CPU cycles, each 422 under `poll_grade.py`'s 155 and 280 us, which are unchanged.
- **The hold-off countdown** is in a centisecond's consumers, at most 9,618 and 19,439 cycles, under the 130 and 510 us stated.
- **The declaration and withdrawal passes** are THE TRANSMIT's builds, under `ctrl_loop.h`'s costs.

The table rule, unchanged: each cost is the larger of the measurement and the committed table's. This round's legs move no cost in either column; against #810's round 29 tables, round 1's moves stand:
- MAAP's record, at a range lost to a peer's ANNOUNCE: 90 to 115 and 130 to 150 us.
- AECP's timer slot at 1x1/1if: 60 to 65 us.
- A TICK at 8x8/2if: 40 to 45 us.
- With tsn-c-stack#32 only: the polls' base 155 to 160 and 285 to 290 us; at 1x1/1if, ACMP's owed frame 120 to 125 and the registrar walk 20 to 25 us.

The load moves 0.001 to 0.003, and no row of the flip check changes its verdict ([acceptance 4](#acceptance-4-no-regression-beyond-stated-deltas)). `SPLIT_CONTROL_MEMORY.md` section 13 is restated at this head, its 8x8/2if pass at 320 us.

### ROM

| Point | Fixture rom / sram, B | Fixture RAMB36 | Platform rom / sram, B | Platform RAMB36 |
|---|---:|---:|---:|---:|
| 1x1/1if | 108,872 / 45,568 | 38.5 | 113,936 / 46,576 | 39.5 |
| 1x1/2if | 110,664 / 56,976 | 41.5 | 115,760 / 58,032 | 43.0 |
| 8x8/1if | 122,400 / 86,464 | 51.5 | 127,504 / 87,456 | 53.0 |
| 8x8/2if | 124,136 / 112,624 | 58.0 (ledgered 58.5) | 129,288 / 113,632 | 60.0 (ledgered 60.0) |

Each image linked at this head and at #810's round 29 head `b2d39235` from the same runtime archives and split SoC exports (`b2d39235`'s platform 8x8/2if image refused by its own 59.0 ledger, its sizes read from the refusal): this change adds 944 to 1,064 B of `rom` (the most at both 1x1 two-interface images), 16 to 64 B of `sram`, and 64 B of `ctrl_plat` at every point. These are the sizes round 1 linked: `17ac263f` keeps the image's layout after `declare_sources` at round 1's.

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
git checkout --detach 18300f6e5f0c63b2ebc81d6bbc243496034f638a
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
python3 -B tb/verilator/ctrl_service_budget/run.py --point 1x1 --build-dir <scratch>/n-1x1 --variant answering-every-port --record-budget-findings
python3 sw/builder/test_builder.py --require-rv32
(cd tests && behave --no-capture -f plain)
git diff --check 66f713267f201d1a00d7f711e04b3a996d804dee HEAD
```

Expected result / pass criteria:

- Every `run:` step of `rtl-fast.yml`, `rtl.yml`, `elaborate.yml` and `docs.yml` is rc 0 or not run with its reason. In this pass, 139 steps ran rc 0 and 226 were not run: hosted orchestration, installs this host carries, and `rtl.yml`'s hosted shard steps of the full sweep, which ran here instead as four shard units: 62 of 65 suites as run, the other three on a re-run with CI's `MAKEFLAGS` (above).
- `test_ctrl_firmware.py --require-rv32 --self-test`: `test_ctrl_firmware: PASS`, every planted defect caught (control 696, AECP 227, SRP 398, the 29 Talker plants at both points among them; 0 escaped).
- `fw_coverage.py --check`: `firmware coverage: PASS (39 files)`, `srp_mbx.c` 725/725 lines and 651/651 branches after the exclusions (651/654 before), `ctrl_app_srp.c` 89/89 and 72/72.
- `load_grade.py --check`: rc 0, `HELD 1x1/1if at the pin: the load 0.488` and `with tsn-c-stack#32: the load 0.486`, ceiling 0.70. `--selftest`: 25 of 25 planted controls refused.
- `flip_grade.py --check`: rc 1 by design (8x8/2if over 0.70; R4 at both points and R5, R6 at 8x8/2if, as before this change). `--selftest`: 131 of 131.
- `test_ctrl_memory.py`: `RESULT: PASS`; the size fixture's 8x8/2if point plans at 58.5 and the platform's at 60.0, each by name.
- The harness, `valid-destinations` arm: 0 refusals, 0 of 5 and 0 of 20 budget misses, no work pass over the share. The Talker rows reach at most 199.4 of 220 ms.
- The harness, arm A: 0 refusals; 7 of 945 and 7 of 996 misses, the merged head's seven (tsn-c-stack #26); no pass over the share or over its stated cost (no `STATED` line). The `answering-every-port` arm: 0 of 280 and 0 of 736, no `STATED` line (its 1x1/1if `notice-burst-5` is the group that failed the polls' base on this round's first firmware).
- How this pass ran the harness at the head: each arm's point was built there. Its image's loadable bytes equal the measurement build's, and its Verilog is identical but for comments. One group per arm was re-run, with a log byte-identical to the measured one, and every measured group was regraded rc 0 by the head's graders.
- `test_builder.py --require-rv32` and `behave` (508 scenarios, 2,330 steps) pass.
- `git diff --check` is clean against the base and #810's merged head.
- Every gate job's tree (28 workflow jobs, the three lane-gate clones and the eight harness clones) is clean at the head after its run.

## Known limitations / out of scope

- **Hardware** (acceptance 6): one stream each way with the reference peer, every counter checked at both ends, is the bench lane's.
- **The split boot simulation** (`tb/verilator/ctrl_split_boot`) boots the platform image with an idle datapath and no frame input, so the wire evidence comes from the CPU budget harness's split SoC simulation. There the fixture's source port is made the platform's, which reports the same base + n.
- **For a separate issue (found this round, not fixed here): the Domain's own leave and join on the refused path.** In the sequence R835-1-F5 describes (an adoption refused for storage before THE TRANSMIT's build, the ring refusing the MRPDU built, the adoption made after it), lwSRP refuses `change_domain`'s `mrp_mad_leave` of the old Domain and `mrp_mad_join` of the new one, both `(void)`. A probe test of that sequence (not committed; its source and logs in the lane's receipts) shows, at 1x1/1if and 8x8/2if, the adapter recording VID 3 adopted with nothing owed, while interface 0's MSRP Domain stays VID 2 on the wire for 25 s (28 declaring events, no Leave) and VID 3 is never declared. The ruling's condition for fixing it here (the same mechanism) does not hold: the adoption reserves the new VID with `mvrp_declare` before the Leave, then withdraws the old VID, commits `i->domain`, publishes `SR_DOMAIN` and re-declares every source. Keeping it owed after a refused Leave leaves the reserved VID declared, and a Domain that changes before the retry would leak it. A fix needs an ordering decision: reserve first and undo, or THE TRANSMIT not re-entering the declarations of an interface whose build left a frame owed (which would also cover the Talker's case).
- **For a decision, recorded and not resolved here:**
  - A Domain adoption re-declares every declared source in place with a changed vlan_identifier, a FirstValue field 35.2.2.8 does not let a Talker change either. This is unchanged and outside #895; to be proposed as an issue (R835-1 found none filed).
  - The datapath has one stream window, interface 0's (`ctrl_plat.c`). Pre-existing.
- **A change of behavior a reviewer should see:** each source is now declared on its own interface only; before, every interface declared every source.
- **The split image's measured costs follow its hot layout, and the thin ones move with it.** This round's first firmware (`e0398c40`) grew `declare_sources` by one instruction, which moved every hot function after it, the registrar walk's among them, by 4 B. Its legs failed two stated costs at 1x1/1if by the head's own graders (`run.py` exits 1): the registrar walk at 2,015 CPU cycles against `poll_grade.py`'s 2,000 (`srp` group, arm A), and a pass's polls' base at 16,141 against 15,500 (`notice-burst-5`, the `answering-every-port` arm), the cost spread over `maap_mbx:poll`, `aecp_mbx:poll` and `srp_mbx:poll`. The bounds are not changed. `17ac263f` makes `moved`, the hot function before `declare_sources`, one instruction shorter with the same value (`i->stale |= ...`), so every function after `declare_sources` sits at round 1's addresses again at both points (`nm`: only `moved`, `mvrp_declare`, `mvrp_attr_len` and `declare_sources` differ), and the legs ran again on it. Margins under bounds this lane does not change: the polls' base at both points, 422 cycles under `poll_grade.py`'s (15,078 and 27,578 cycles); the 1x1/1if registrar walk, 1,987 of 2,000 cycles in arm A's `srp` group, 13 under.
- 8x8/2if's load is over 0.75 at the pin and with tsn-c-stack#32, as before this change; its flip is #890's.

## Definition of Done

- [x] Linked Issue acceptance criteria are satisfied (1 to 3 and 5 here; 4 as the ruling of 2026-11-13 states it; 6 is the bench lane's)
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
