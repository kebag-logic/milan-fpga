[A761c]

## Contents

- **[Status](#status)** — Green/WIP/blocked, test tally, and `branch` -> `dev-soft-core`.
- **[Linked Issue / roles](#linked-issue--roles)** — Public task, executor, and independent reviewers.
- **[Description](#description)** — What changed and why.
- **[Authoritative references](#authoritative-references)** — Requirements/specification clauses and docs.
- **[How to get into the same state](#how-to-get-into-the-same-state)** — Copy-pasteable checkout/dependency/environment commands.
- **[How to validate](#how-to-validate)** — Exact reviewer commands and expected result.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** — What this deliberately does not do, and why.
- **[Definition of Done](#definition-of-done)** — The merge bar from [CONTRIBUTING.md](../CONTRIBUTING.md).

## Status

Round 7 at `d3e61e37`: round 6's `33b0d03a` (R821-6 NEGATIVE on one MINOR, F1-R6) and one commit of Markdown and comments: the polls table's round-22 figure for the retained retry restored, `285 (250)`, and three comments rewrapped with their words unchanged. No firmware image changes (sha256, below), so round 5's legs and final pass and round 6's gates carry, and the gates the touched files feed ran again at `d3e61e37`. Round 5's results stand: REBOOT's record ordinary (125 us of 240), every 1x1/1if row within its bound, the last queued notice 134.74 of 135 ms, the load 0.520, the slice 950 us and the pace 8 ms by their rules; the platform's 8x8/2if image at 60.5 RAMB36, reported. `665-s11-aecp-reboot` -> `dev-soft-core`.

## Linked Issue / roles

Relates to #871 (not closed: acceptance item 1 is met for six of its eight items, see below)
Relates to #665

Executor: `[A761c]` (rounds 2 to 7; round 1 was `[A761]`)
Round 5's reviews: R821-5 (NEGATIVE, F1) and R822-5 (POSITIVE) at `d3566d44`
Round 6's delta review: R821-6 (NEGATIVE, F1-R6) at `33b0d03a`
Round 7's delta reviewer: `[R821-7]`, from `33b0d03a` to `d3e61e37`

## Description

The split's AECP REBOOT (#665 S11): the firmware's AECP owner answers it, and the platform's reset port starts the reset #787 chose (PR #822, already on `dev-soft-core`).
Rounds 2 to 4 made the window from the SUCCESS to the reset the processor's (REQ-FWX-001) and proved it per channel; round 4's head `049f0e4d` met the bar (R821-4 and R822-4 POSITIVE).
Round 5 is the maintainer's ruling #665 issuecomment-6894152131, item 1: #881 joins the flip train, starts on #902's review head, measures REBOOT's record in a tracked answering-ports group, and surveys every stated table over every 1x1/1if leg.

**Round 7, item by item (the manager's ruling on R821-6 at `33b0d03a`).**

| Item | Done | Evidence |
|---|---|---|
| F1-R6: the polls table's parenthesis is round 22's by its legend, so the retained row reads `285 (250)`; the round 6 row below says so too | yes | `SPLIT_CONTROL_MEMORY.md:2238`: `285 (250) \| 365 (395)`. Against `git show 8684993388:docs/design/SPLIT_CONTROL_MEMORY.md`, all 11 parentheses of the table equal round 22's figures (`receipts/round22-parentheses.txt`) |
| RS-R6-1: three layout-only rewraps | yes | `test_plat_boot.cpp:188` the last two lines joined; `poll_grade.py:72` refilled with the next line; `ctrl_plat.h:38-42` rewrapped to its neighbours' 78 columns. Each file's text, comment markers aside, is identical to `33b0d03a`'s by sha256 (`receipts/text-identity.txt`) |
| Markdown, comments and whitespace only; no firmware image changes | none changes | the size fixture's and the platform's split images at 1x1/1if and 8x8/1if: 8 of 8 files byte-identical to `33b0d03a`'s and `d3566d44`'s by sha256 (`receipts/identity/`) |
| S-R6-1 | out of scope | the manager opens its own issue |

**Round 7's gates at `d3e61e37`**, on clean clones: whitespace against the merge base and `33b0d03a`, the Python and C++ idiom gates, `docs_check.py` and `check_doc_style.py`, rc 0; `docs.yml`, every `run:` step: 64 ran rc 0, 31 not run with a stated reason, 0 bad; `rtl-fast` `firmware-unit`, every step rc 0 (it compiles and runs `test_plat_boot.cpp`, the platboot arms at one and two interfaces; the control-plane suites PASS, the saved-state suites OK over 5 shapes and 526 tests, `fw_coverage.py --check` PASS, 39 files). Every other gate carries: the commit changes Markdown, comments and whitespace only, and every image is byte-identical.

**Round 6, item by item (the manager's ruling on R821-5 and R822-5 at `d3566d44`).**

| Item | Done | Evidence |
|---|---|---|
| R821-5 F1, option (a): restate `poll_grade.STATED_US[1]['retained']` to 285 by its rule, its docstring's figures and SPLIT_CONTROL_MEMORY's polls row, `285 (250)` since round 7 (round 22's figure in parentheses, as the table's legend states) | yes | `poll_grade.py:70` and `:91`; `SPLIT_CONTROL_MEMORY.md:2238`. At 1x1/1if the polls' `retained`, both load columns' `item.retained` and `record.srp` are each 285 (`receipts/pass/lane/retained_equal.log`); at 8x8/2if all are 365. `selftest_polls.py`'s checks 33 of 33; `flip_grade.py --check --point 1x1/1if` and `load_grade.py --check` rc 0 (R821-5's `model_gates.sh` list, all rc 0) |
| Survey every stated table for any other figure stated twice with different values | yes, none | `statement_survey.py` (below; `receipts/survey/`) |
| R821-5 RS-1 | yes | `test_plat_boot.cpp:187`: `(ADepartingTheRingRefusedHoldsTheReset)` for `(B18)` |
| R821-5 RS-2 | yes | `REBOOT_RESET.md:315` and `:316`: "in `aecp_reboot_mutants.py`, which `aecp_mutants.py` plants"; `test_plat_boot.cpp:76`, `plat_mutants.py:265` and the same reference in B20's comment, `test_plat_boot.cpp:982`: "in aecp_reboot_mutants.py" |
| R822-5-R1 (and R821-4 RS-A / R822-4 RES-A) | yes | `plat_mutants.py:259-265`: B20, B19 and B23 named `NoOtherChannelTransmitsAfterTheDeparting`, `NoFrameOfAnyChannelIsTakenFromTheSuccess` and `TheGateHoldsWhileTheResponseCannotBeHandedOver`; the comment's first part is RS-1's line, which now names the test |
| R822-5-R2 (R822-4 RES-B) | yes | `REBOOT_RESET.md:316`: "SUCCESS. Its three layers each carry one: the loop's stop" |
| R822-5-R3 (R822-2 R2) | yes | `REBOOT_RESET.md:297` and `plat/README.md:89` as the residue gives the sentence; `ctrl_plat.h:38`: "and, from ADP's shutdown, ADP until the port", within its line |
| No firmware image may change | none changes | the size fixture's and the platform's split images at 1x1/1if and 8x8/1if, linked at `d3566d44` and `33b0d03a` against one map and runtime: the 8 files (each image's ELF and loadable binary) byte-identical by sha256 (`receipts/identity/`) |

**The statement survey** (`statement_survey.py`, run at `33b0d03a`, `d3566d44` and `41ca9f87`): every cost each stated table gives at 1x1/1if and 8x8/2if (`load_grade`'s pin and donor columns, `poll_grade.STATED_US`, the pass costs `ctrl_loop.h` states and `whole_grade` reads, `rows_grade.ROW_COSTS`, `rows_tiers`' `DATAPATH_US`, `LONG_NOTICE_US` and `LONG_RECORD_US`, `edit_rows`), each beside every other table's figure for the same cost, and each documented derivation (a retained retry at the SRP record's cost, `CTRL_LOOP_SRP_UNIT_US` at the dearer column's `record.srp`, the longest notice at the polls' `aecp_long`, the paced class at its dearest member). At `d3566d44` the one conflict among the pin's tables was F1, the retained retry 280 against 285, and its derivation failed; at `33b0d03a` none. Every other figure stated twice with two values sets the donor column (`STATED_US_DONOR`, measured on tsn-c-stack#32's image, its docstring's rule) against the pin's, and each is the same at #902's head `41ca9f87`:

| Point | Cost | Pin's tables | Donor column |
|---|---|---:|---:|
| 1x1/1if | `event.ACMP` | 185 | 170 |
| 1x1/1if | `event.MAAP` | 165 | 170 |
| 1x1/1if | `record.acmp` | 280 | 265 |
| 1x1/1if | `record.adp` | 105 | 100 |
| 8x8/2if | `build` | 1,995 (`ctrl_loop.h`, `whole_grade`) | 2,035 |
| 8x8/2if | `event.ACMP` | 350 | 210 |
| 8x8/2if | `event.AECP` | 105 | 110 |
| 8x8/2if | `event.TICK` | 40 | 85 |
| 8x8/2if | `item.reclaim` | 35 (`poll_grade`) | 40 |
| 8x8/2if | `record.acmp` | 440 | 305 |
| 8x8/2if | `record.adp` | 240 | 125 |

**Round 5, item by item (the ruling #665 issuecomment-6894152131, item 1, as the manager relayed it).**

| Item | Done | Evidence |
|---|---|---|
| Merge #902's review head `41ca9f87`, keeping both sides' behaviour | yes | `6cfdf650`; the conflicts below. Every plant of both sides is caught by name: the AECP campaign's REBOOT rows 15 of 15 and the platform's 23 of 23 by their drivers, and every campaign and suite in the final pass |
| Measure REBOOT's record, accepted and refused, in a tracked answering-ports group at 1x1/1if, report 8x8/2if, held as an ordinary record by the rule; `record_classes.py` names it | yes | the `aecp-reboot` group (`reboot_group.py`), in the answering-ports arm, whose patch list gives the fixture a reset port; `record_classes.py` holds every REBOOT record as ordinary and refuses a pass without an accepted and a refused one (14 of 14 controls). Figures below |
| The survey of every stated table by the rule over every 1x1/1if leg (arm A, the answering-every-port arm, the answering-ports arm) | yes | `compare_point.py` over every leg, each line naming its leg: four costs over, all restated (below); on the rebuilt image only the class lines are over, which `record_classes.py` holds |
| Restate anything over by the rule, then the pace, slice and bound rules | yes | `7653571f`: SRP's record 285 us and the drain's unit with it, AECP's ordinary record 240, the paced class 305, a pass's events' fixed part 40, the last queued notice's bound 135 ms by `queued_bound.py` (its row 134.74); the slice rule still chooses 950 us (`tier_grid.py`, 4 of 420 hold), the pace rule 8 ms |
| STOP on: the last queued notice over 140 ms; any other 1x1/1if row over its bound; the load over 0.70; REBOOT's record over the ordinary class | none holds | 134.74 ms; every row within its bound (below); 0.520; 125 us of 240 |
| Report every image's ROM; an image past its entry is not a stop | reported | the table below; the platform's 8x8/2if entry raised to 60.5 (`24e63089`), debt owed to S14 |

**The merge's conflicts and the composition** (`6cfdf650` and after).

| Where | Both sides kept |
|---|---|
| `aecp.h` | `aecp_config`: #902's owed-notice queue, then `reboot`; `struct aecp`: `edited_ms`, then the REBOOT's state |
| `aecp.c` `aecp_ready` | #902's queue-slot term and the REBOOT's `a->reboot == 0u` |
| `aecp.c` `aecp_tx_complete` | the REBOOT's `tx_done`, then #902's awaited-list walk. Completions still come per cookie in ring order (`aecp_mbx.c` poll), and the poll drains the owed queue before the REBOOT is due |
| `ctrl_plat.c` | the reset port's flag and #902's queue |
| the AECP tests, mutants, `ctrl_configs.py`, the gtest exclusions, `split_soc.py`, both design documents | both sides' rows, the REBOOT's in `aecp_reboot_mutants.py` (`9447702a`) |
| `milan_soc.py` (semantic) | #902's record mover took CSR bank `n_locs - 3`, the REBOOT port's; the port moved to `n_locs - 4`. The split SoC's `csr.csv` at 1x1 against `41ca9f87`'s: only `ctrl_reboot` added, at `0xf000e000` |
| `aecp_retry` (semantic, `b4b0c3eb`) | THE RETRY's round came in from `dev-soft-core` and could start a notice after the SUCCESS, which only `aecp_poll` held. `round_waits` now holds an accepted REBOOT; the core test's check "THE RETRY's round starts no notification after a REBOOT's SUCCESS" and the defect `reboot-retries-after-its-success` |
| the platform boot tests (`7072343a`, `88b0fcd1`) | B15 and B17 take THE STEP's pass as #902's B10 does; B18's ADP ring and B23's AECP ring are set from the boot's first read, for the driver that reads a ring's tail only when its room is short (`mbx.c:551`); B18 full for exactly its SHUTDOWN's sends and its next poll's, so `plat-reboot-departing-owed-ignored` is caught |
| the REBOOT simulation (`a3e45e68`, `20e08ceb`, `cb0fc679`) and #902's queue defect (`d3566d44`) | its flash device held to the map's KLJ3 journal, as the budget harness since #902's `da1869a3`; the early-reset plant fires in the take of every AEM_COMMAND REBOOT, before AECP's handler, since a plain response is committed in the record's own turn; `owed-round-beside-the-queue`'s anchor carries the REBOOT's `round_waits` term, so it plants one site again |
| the idiom ratchets (`9447702a`) | the REBOOT's defects and group in modules of their own, `build.py`'s comment rewrapped, B18's flags declared apart |

**REBOOT's record** (the answering-ports arm's `aecp-reboot`; by the rule: the cycles at the CPU clock, plus 5 %, rounded up to 5 us).

| REBOOT | 1x1/1if, held (ordinary 240 us) | 8x8/2if, reported (ordinary 265 us) |
|---|---:|---:|
| SUCCESS, its notice owed to every registration | 11,467 cycles, 125 us | 8,664, 95 |
| ENTITY_LOCKED | 10,511, 115 | 10,742 and 10,658, 115 |
| BAD_ARGUMENTS, short | 9,870, 105 | 10,727 (115) and 10,033 (110) |
| NO_SUCH_DESCRIPTOR, ENTITY 1 | 9,407, 100 | 10,007 (110) and 9,724 (105) |
| NOT_SUPPORTED, STREAM_INPUT | 9,291, 100 | 9,876 and 9,973, 105 |

At 8x8/2if the figures are interface 0's, then interface 1's; both images give the same cycles.

**The survey and the restatements.** The REBOOT's code grows hot functions (`aecp_command` +124 B, `aecp_rx` +36, `aecp_poll` +36, `aecp_tx_complete` +28, `aecp_ready` +12) and `aecp_retry_aged`, fourth in the hot order, shrinks 28 B, so the hot code after it moves and the fetch cache's conflicts with it. Over every 1x1/1if leg four costs were over their statements by the rule, each restated in both `load_grade` columns or its own table (`7653571f`):

| Cost | Measured, CPU cycles | By the rule | Was | Where |
|---|---:|---:|---:|---|
| `record.srp` (and `item.retained`, and `CTRL_LOOP_SRP_UNIT_US`, which `load_grade.py --check` holds to it) | 26,865 | 285 | 280 | arm A `backlog-adp@blank-aged1-2` (26,366 in #902's E1) |
| `record.aecp`, the ordinary class | 22,531 | 240 | 235 | a SET_NAME in the answering-every-port arm's `notice-burst-0` (22,236 in #902's) |
| `events_none` | 3,627 | 40 | 30 | the answering-every-port arm's `notice-burst-1` (2,020 at #902's head) |
| the paced class (`edit_rows.EDIT_RECORD_US`) | 28,750 | 305 | 300 | the answering-ports arm's accepted SET_CONFIGURATION (28,376 at #902's) |

With them the bound rule restates `AECP_QUEUED_MS` at 135 ms (`aecp_mbx.h`, its row 134.74), and the notice windows run their load to it (`notice_window.RUN_MS`, `935dacf2`). Every one-interface leg ran again on the rebuilt image (the SRP unit's immediate is the only image change, at equal sizes): on it the compare's only over lines are #894's class lines (the largest legal notice, held by `LONG_NOTICE_US`; the paced records, held by `record_classes.py` at 305 of 305).

The rows at 1x1/1if by every source, the built design (`flip_grade.py --check --point 1x1/1if`, RESULT PASS):

| R4 | R5 | R6 | First queued | Last queued | R4L | ACMP | ADP | MAAP | tx | txL |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 13.23 of 20 | 74.81 of 90 | 72.88 of 90 | 14.69 of 20 | 134.74 of 135 | 188.51 of 238 | 29.22 of 30 | 27.53 of 30 | 27.65 of 30 | 33.66 of 49 | 48.75 of 49 |

The load at the pin is 0.520 (0.516 with tsn-c-stack#32), under 0.70.

**Every image's memory** (`plat_ledger.py` for the platform's, `ctrl_srp_image.py` for the size fixture's, against the shape's split SoC export):

| Point | Fixture `rom` / `sram`, B | Fixture RAMB36 | Platform `rom` / `sram`, B | Platform RAMB36 | `ctrl_plat`, B |
|---|---:|---:|---:|---:|---:|
| 1x1, one interface | 111,392 / 55,216 | 41.0 | 117,276 / 56,352 | 43.0 | 17,664 |
| 1x1, two interfaces | 112,680 / 57,376 | 42.5 | 118,604 / 58,464 | 43.5 | 19,136 |
| 8x8, one interface | 124,896 / 96,304 | 54.5 | 130,828 / 97,392 | 56.0 | 18,304 |
| 8x8, two interfaces | 126,160 / 113,232 | 59.0, its entry | 132,140 / 114,288 | **60.5, past its 60.0** | 20,416 |

The platform's images take 1,796 to 1,836 B more `rom` than at #902's head, and `ctrl_plat` 128 B more at every point. Its 8x8/2if entry is raised to 60.5 at its measured `ctrl_plat` (`24e63089`), ROM debt owed to S14 by the owner's decision of 2026-11-15 (#665 issuecomment-6892332745); the restatements change no image size.

**Acceptance (#871).** Unchanged from round 4 but for the CPU simulation's figures, now at the split CPU's 100 MHz on the bus clock:

| # | Item | Evidence | Met |
|---|---|---|---|
| 1 | After the reset, the eight Milan state items restored, ADP inside its valid time, the binding restored (#396's power-area checks), in the CPU simulation | `tb/verilator/ctrl_reboot`: the #396 grader PASS over the stream format, presentation time offset, channel mappings, clock source, entity names, object name and the binding; the first ENTITY_AVAILABLE 454.192 ms after the reset, 4,808.775 ms after the REBOOT command, of the 20,000 ms valid time; host test B15 | **Six of the eight items and the binding**, as before: the configuration and the sampling rate cannot leave their defaults at the shipping shape |
| 2 | The response on the wire before the reset fires; a mutant firing the reset before the response leaves fails | ORDER: SUCCESS 0.129 ms, notification 0.219, ENTITY_DEPARTING 0.528, the port 0.543 after the command; plant `reset-before-the-response` caught on its words; host defect `plat-reboot-before-the-response`; AECP defect `reboot-due-before-its-frames-complete` | yes |
| 3 | A mutant that ignores the request fails | plant `request-ignored`, `plat-reboot-ignored`, `reboot-never-accepted` | yes |
| 4 | A REBOOT during a journal write leaves a state the boot replay accepts, never half-applied; a planted mutant that tears the write fails | JOURNAL: the REBOOT 62 bus cycles after the write's erase, 14 page programs after it, the drain durable (851.0 ms, the KLJ3 journal's), every item back after the reset; the cut's replay reads the saved snapshot whole; control `replay-mixed`; plant `write-torn`, `plat-reboot-stops-the-store`; host B16 | yes |
| 5 | REBOOT of a descriptor other than the ENTITY answered as 7.4.43 states | REFUSE as before; `Core.RebootRefusalsLeaveTheEntityInService`, B13; plant `any-descriptor-type` | yes |

Rounds 2 to 4's item tables are in this PR's history (round 4's body); their evidence stands at `049f0e4d`, and round 5's gates below cover the merged head.

## Authoritative references

- #871 and its rulings; plan S11 and decision D9 of #665; the maintainer's ruling #665 issuecomment-6894152131 (item 1) and the owner's decision #665 issuecomment-6892332745 (ROM).
- #902 (#894) at `41ca9f87`: its REVIEW READY #894 issuecomment-6893619187 and rulings issuecomment-6883864236, -6886633874, -6888782796 (the record classes, the SRP unit's derivation, the slice rule).
- REQ-FWX-001; protocol-processor `docs/architecture/06_aecp_engine.md` section 6.11.
- IEEE 1722.1-2021 7.4.43 (Figure 7-68, 7.4.43.1, 7.4.43.2), 7.5.2, 9.3.2.6, Table 7-126; Milan v1.2 5.4.5.1, 5.4.5.2, 5.6.3.3.
- `docs/design/REBOOT_RESET.md` section 8, `docs/design/SPLIT_CONTROL_MEMORY.md` sections 3, 5 and 13, `docs/reference/FR_NFR.md` 3.4.1, `tb/verilator/ctrl_service_budget/README.md` (REBOOT; record classes).

## How to get into the same state

```sh
git clone https://github.com/kebag-logic/milan-fpga.git
cd milan-fpga
git fetch origin 665-s11-aecp-reboot
git checkout d3e61e37
git submodule update --init third_party/verilog-axis protocol-processor gptp-processor third_party/lwSRP third_party/tsn-c-stack
```

The CPU budget harness and the CPU simulations need the product LiteX tree, the pinned RV32 SDK, Verilator and the offline CPU generator, as `tb/verilator/ctrl_service_budget/README.md` lists them.

## How to validate

```sh
python3 -B tb/verilator/ctrl_service_budget/run.py --point 1x1 --build-dir /tmp/b1 --variant answering-ports \
  --groups aecp-fanout,aecp,aecp-largest-notice,aecp-reboot --record-budget-findings --record-share-findings
python3 -I tb/verilator/ctrl_service_budget/record_classes.py /tmp/b1/results          # REBOOT held: 125 us of 240
python3 -I tb/verilator/ctrl_service_budget/record_classes.py --selftest               # 14 of 14 refused
python3 -B tb/verilator/ctrl_service_budget/flip_grade.py --check --point 1x1/1if    # RESULT PASS; last 134.74 of 135
python3 -B tb/verilator/ctrl_service_budget/tier_grid.py --point 1x1/1if             # 4 of 420 hold; the built 950 us chosen
python3 -B tb/verilator/ctrl_service_budget/load_grade.py --check                    # 0.520 and 0.516, PASS
python3 -B tb/verilator/ctrl_split_boot/plat_ledger.py --build-dir /tmp/ledger       # PASS; 8x8-if2 60.5 RAMB36
python3 -B tb/verilator/ctrl_reboot/run.py --build-dir /tmp/reboot --self-test --jobs 3   # PASS; 12 of 12
git diff --stat 33b0d03a d3e61e37      # round 7: one commit, four files
git diff --stat d3566d44 33b0d03a      # round 6: one commit, seven files
git diff --stat 049f0e4d d3e61e37      # rounds 5 to 7 on round 4's accepted head
git diff --stat 41ca9f87 d3e61e37      # this lane's whole delta on #902's review head
```

**Round 6's gates at `33b0d03a`**, each on a clean clone, every one the round's files feed (`poll_grade.py`, the comments of `test_plat_boot.cpp`, `plat_mutants.py` and `ctrl_plat.h`, three Markdown files):

| Gate | Result |
|---|---|
| R821-5's `model_gates.sh` list: `flip_grade.py --check --point 1x1/1if`, `load_grade.py --check` and `--selftest`, `record_classes.py --selftest`, `flip_grade.py --selftest`, the rules | rc 0: RESULT PASS, the last queued notice 134.74 of 135; the load 0.520 (0.516); 26 of 26; 14 of 14; 585 of 585; last 134.74 ruled 135 stated 135, pace 8, no statement off, no control escaped |
| `rows_tiers.py --selftest`; `tier_grid.py --point 1x1/1if` | 1,033 of 1,033; the built 950 us chosen |
| The polls checks (`selftest_polls.py`); the retained retry against the load gate | 33 of 33; 285 in `poll_grade`, both load columns and `record.srp` |
| The statement survey | RESULT PASS, 0 conflicts; the 11 donor-column differences above |
| The CPU budget harness's self-test, `run.py --self-test` (its polls checks read `poll_grade.STATED_US`) | 0 failures, 246 of 246 mutants caught |
| `rtl-fast` `firmware-unit`, every `run:` step (it compiles and runs `test_plat_boot.cpp`, the platboot arms at one and two interfaces) | every step rc 0: the control-plane suites PASS, the saved-state suites OK over 5 shapes and 526 tests, `fw_coverage.py --check` PASS (39 files) |
| `docs.yml`, every `run:` step | 64 ran rc 0, 31 not run with a stated reason, 0 bad |
| Whitespace against the merge base, `d3566d44` and `41ca9f87`; the Python and C++ idiom gates; `docs_check.py`, `check_doc_paths.py`, `check_doc_style.py`, `check_em_dash.py`, `gen_toc.py --check` and `--verify-anchors` | rc 0 |
| Image identity, the fixture's and the platform's split images at 1x1/1if and 8x8/1if | 8 of 8 files byte-identical to `d3566d44`'s |

The rest of round 5's pass carries. The images the REBOOT and boot simulations and the builder link include `ctrl_plat.h`, whose change is a comment within its line, and are byte-identical (above); `plat_mutants.py` and `test_plat_boot.cpp` changed in comments only, so the control campaign plants the same rows into the same code (its platboot arms ran again in `firmware-unit`); the sweep reads none of the round's files.

**Round 5's final pass** (each on its own clean clone; the head each ran at is named), which carries to `33b0d03a`: no firmware image changes, and the gates round 6's files feed ran again (above). Round 5's head was `d3566d44`. After `57daf4ff` the lane changed only the REBOOT simulation's plant and its README (`20e08ceb`), their comments (`cb0fc679`) and one AECP mutant row's anchor (`d3566d44`), so each gate that runs one of those files ran again after it, and every other carries (`receipts/model/files-7653571f-to-final.txt`). The other firmware jobs import the AECP table (`test_ctrl_firmware.py:150`) but plant its rows only in the AECP shard, which ran at `d3566d44`:

| Gate | Head | Result |
|---|---|---|
| The four-shard Verilator sweep, each shard on its own picked range (64-71, 40-47, 0-7, 88-95) | `57daf4ff` | 65 of 65 suites, 2,713,040 checks, 0 in-suite failures, 0 timed out; each shard rc 0 (3,916, 3,830, 4,350 and 3,317 s); the suite-cancellation preflight PASS on each; `milan_dp`'s `[FACE] commit to BUSY clear: 2 polls` |
| Every `run:` step of `rtl-fast`, `rtl` and `elaborate` (`run_wf.py`, each job its own clone; `verify_wf_r5.py`) | `57daf4ff`, `20e08ceb`, `d3566d44` | 88 ran rc 0, 167 not run with a stated reason, 0 bad. `firmware-boundary` and `firmware-verilator`, which run the REBOOT simulation's builder, at `20e08ceb`; `firmware-aecp-mutants` at `d3566d44` |
| The firmware campaigns | `57daf4ff`, `d3566d44` | control 738 of 738 caught; SRP PASS; AECP 314 of 314 at `d3566d44` (at `57daf4ff` it refused `owed-round-beside-the-queue`, whose anchor the REBOOT's `round_waits` term had moved: fixed by `d3566d44`, every one of the 314 anchors now one site); firmware-unit: the control suites PASS, the saved-state suites OK over 5 shapes and 526 tests, `fw_coverage.py --check` PASS (39 files) |
| `docs.yml`: every `run:` step | `cb0fc679` | 64 ran rc 0, 31 not run with a stated reason, 0 bad |
| Whitespace against the merge base, `049f0e4d` and `41ca9f87`; the Python and C++ idiom gates; `docs_check.py` | `d3566d44` | rc 0 |
| The model: `tier_grid.py`, `rows_tiers.py --selftest` (1,033 of 1,033), `load_grade.py --selftest` (26 of 26) and `--check` (0.520, 0.516), `flip_grade.py --selftest` (585 of 585) and `--check --point 1x1/1if` (PASS), `record_classes.py --selftest` (14 of 14), the pace and bound rules (8 ms, 135 ms, no statement off, no control escaped), `ctrl_hot.py` (206 entries in order), `gen_mailbox.py`, `lint_rtl.py`, `test_soc_options.py`, `test_ctrl_memory.py`, `plat_ledger.py` (PASS), `check_baremetal_only.py`, `check_em_dash.py` | `cb0fc679` | rc 0 but the four that exit 1 by design, as at #902: `rows_tiers.py --terms` and `flip_grade.py --check` over both points, with `--design as-built` at 1x1/1if, and at 8x8/2if |
| `record_classes.py` over every leg (arm A's halves, the answering-every-port arm, the answering-ports arm at 1x1/1if and 8x8/2if) | the legs' | RESULT PASS |
| The stated-table survey over every 1x1/1if leg on the rebuilt image | the legs' | the class lines only |
| The harness self-test, `run.py --self-test` | `57daf4ff` | 0 failures, 246 of 246 mutants caught |
| The hooks self-test; the saved-state target's self-test; `behave`; the datapath twin | `57daf4ff` | 28 of 28, 96 of 96 mutants; 73 checks, 0 failures; 15 features, 511 scenarios; rc 0 |
| The split boot simulations: 1x1, 8x8, native controls, plants | `57daf4ff` | rc 0 |
| The REBOOT simulation, plain and `--self-test` | `20e08ceb` | PASS (0 findings); 12 of 12 plants and controls on their own words |
| `test_builder.py --require-rv32`; its gate 1b alone with GNU Make 4.4.1 | `20e08ceb`; `d3566d44` | all gates pass but two not run, as in round 2: gate 1b's `MAKEFLAGS += -e` mutation under make 4.3 (it passes alone under 4.4.1) and gate 11's calibration, which needs a Vivado place report; gate 1b alone: ALL GATES PASS |
| The saved-state store's campaign, `test_ctrl_nvm.py --self-test` | `20e08ceb` | OK over 5 shapes, 526 tests, all 144 planted defects reddened |

**The legs.** Arm A (96 groups, two interleaved halves on one build), the answering-every-port arm (16 groups), the answering-ports arm (`aecp-fanout`, `aecp`, `aecp-largest-notice`, `aecp-reboot`), the 8x8/2if REBOOT leg and the redelivery control, first at `24e63089` (the survey) and again on the rebuilt image: arm A at `7653571f`, every other leg at `935dacf2`. Arm A's 96 group scripts are byte-identical at `d3566d44` (`receipts/model/armA-identity.txt`), and no firmware or harness build file changed after either head. 0 refusals in every leg; arm A's 7 budget misses are `backlog-owed`'s held-egress rows (ruling 6871343905 (a)), as at #902's head; 0 of 141,068 passes over THE SHARE.

Receipts: `round5/receipts/` (logs sanitized of host paths; files over 200 KB listed by size and sha256 in each `LARGE.tsv`; `INDEX.md`).

## Known limitations / out of scope

- **The platform's 8x8/2if image plans 60.5 RAMB36**, past its 60.0 entry; the entry is raised to it as ROM debt owed to S14 (the owner's decision of 2026-11-15). The image must still fit the device and meet timing, which the flip's builds hold.
- **Margins at 1x1/1if are small:** txL 0.25 ms, the last queued notice 0.26 ms, ACMP 0.78 ms. A further hot-code move could put a cost over again; every merge of this train reruns the survey.
- **`CTRL_LOOP_SRP_UNIT_US` is restated in `sw/firmware/ctrl/loop/ctrl_loop.h`.** This lane's standing scope keeps out of `ctrl/loop/`; the constant is the load gate's `record.srp` by #894's ruling issuecomment-6886633874, which `load_grade.py --check` enforces, and the round's ruling requires the restatement, so this one rule-derived constant is the only `ctrl/loop/` change.
- **The answering-ports arm's patch list gives the fixture a reset port** (`.reboot=true`); arm A's fixture stays without one, so its REBOOT is NOT_IMPLEMENTED and only arm B measures an accepted one, as for SET_CONFIGURATION.
- **8x8/1if** has no REBOOT leg: that point is #914's, measured once at the composed head.
- **This head syncs again on #898's** (the manager relays); its stated tables are surveyed again there.
- Unchanged from round 4: the CPU simulation builds no datapath; the PHY hold is simulated for 50 of its 3,500 ms; the configuration and the rate are read back, not graded; the transmit gate has no CPU-simulation plant (host B20 holds it); `quiet-without-the-face-poll` (R821 S2) still escapes; R821 S4 not taken; the split boot simulation's hash seed is its owner's.

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
