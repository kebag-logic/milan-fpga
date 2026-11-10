[A683ze]

## Contents

- **[Status](#status)** — STOP at the head below: after items 1 to 3 of the round 25 ruling the long-window load is 0.747 at 8x8/2if, over its 0.70 ceiling, graded with tsn-c-stack#32; 0.453 at 1x1/1if; 32x32/2if reported, pending the owner.
- **[Linked Issue / roles](#linked-issue--roles)** — Public task, executor, and independent reviewers.
- **[Description](#description)** — Round 25, item by item; what holds at this head; the load table; where the round histories went.
- **[Authoritative references](#authoritative-references)** — Requirements/specification clauses and docs.
- **[How to get into the same state](#how-to-get-into-the-same-state)** — Checkout, submodules and environment.
- **[How to validate](#how-to-validate)** — Exact reviewer commands and expected result.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** — What is left, and the decisions for the owner.
- **[Definition of Done](#definition-of-done)** — The merge bar from [CONTRIBUTING.md](../CONTRIBUTING.md).

## Status

STOP at `3a1d14c21b6b484270a387bae1a7eedc7c0bc2d5`, seven commits on round 24's head `a30c9986` (`665-s2b-cycles` -> `dev-soft-core`). No merge, no rebase, no force, no amend.

The round 25 ruling (#665 issuecomment-6751196896) asks for 1x1/1if and 8x8/2if under the 0.70 ceiling in software. After its items 1 to 3, each source at its stated arrival bound and stated cost, graded with tsn-c-stack#32 (the load the pin move owes):
- **8x8/2if: 0.747**, 0.047 over: SRP's channel 0.243, AECP's owed frame 0.076, ACMP's records 0.061 (0.844 at this tree's pin);
- 1x1/1if: 0.453 (0.466 at the pin);
- 32x32/2if, reported, pending the owner: 1.659 (2.150 at the pin), 2.37x the compute it would need for 0.70.

The owner has since chosen for 32x32/2if (#665 issuecomment-6759183115 and its correction issuecomment-6759193032, option D, after this round's ruling): reported, not gated, with per-shape contract rates and owed to #859, and more compute to be done in #872, whose design round takes this round's factor, 2.37x. The decision leaves this round's assignment unchanged. The tree keeps the ruling's item 4 label, "pending the owner"; its wording follows the decision in the next round.

The ruling's first exit fires: "STOP if the load at 1x1/1if or 8x8/2if stays over 0.70 after items 1 to 3". Items 4 to 6 are committed or written as the ruling asks. The top three terms and what each would need are under [Round 25](#round-25). Item 1's basis holds, so its exit does not fire.

## Linked Issue / roles

Relates to #665

Executor: `[A683ze]`
Internal cleared-context reviewer: `[R711]`
External reviewer: `[R712]`

## Description

### Round 25

**The ruling** (issuecomment-6751196896, on [A683zd]'s STOP at `a30c9986`, issuecomment-6751120577): round 24's gate failed at 1.181 (8x8/2if) and 2.209 (32x32/2if), mostly SRP's retained retry. This round brings 1x1/1if and 8x8/2if under the ceiling in software: (1) the retry bounded by its source; (2) AECP's owed frame costed by what each source sends; (3) ACMP's per-sink walk as a donor change, tsn-c-stack#32, with the gate graded on it; (4) the ceiling at 1x1/1if and 8x8/2if, 32x32/2if reported; (5) two notes; (6) this body under 60,000 characters.

| Item | At this head |
|---|---|
| 1. SRP's retained retry, bounded by its source | `dbd57a7a`. A refused SRP record is retried only once a pool has returned a block (`ctrl_pool_returned`, counted at each return in `ctrl_pool.c`) or lwSRP has reported an Applicant or Registrar change of its interface (`srp_interface.moved`, set in `moved()`) since the refusal, and then at most once a centisecond (`retry_spent`, given back at each centisecond in `tick`). A refusal records what it saw (`apply_receive`). The 1 s give-up and "no other SRP record meanwhile" are unchanged. The basis is below. Four firmware tests at both interface counts, among them a refused record taken on the first pass after the pool frees. Nine plants (`srp_retry_mutants.py`), in the SRP campaign at two interfaces. Two existing plants of the retained receive (`receive-retry-passes-owed`, `receive-retention-short`) escaped under the rule; `3a1d14c2` gives their tests the centisecond and the millisecond that make them fail again. The load gate reads the rule's lines from the tree (`RETRY_RULE`): a copy of `srp_mbx.c` that retries with nothing changed, or every pass a change allows, leaves SRP's term with no source and fails the gate. To fit the 8x8/2if `answering-every-port` arm's ledger, `struct srp_mbx` ends with its two frame buffers |
| 2. AECP's owed frame, by source | `ca403b0c`. A record's owed frame is its response to one recipient, or a command's response with its notice to the registered controllers (at most 16 an AVB interface), whichever is larger, once a record. A registration's probe is its own frame, once its 250 ms retry (Milan v1.2 5.4.5.3). Each kind is measured from the AECP frames the traced legs committed; a probe, which no group stages, is stated at a response's cost. COUNTERS_CHANGED notices, which have a contract rate, are a new term at their holdoff. The single 32-recipient charge is gone, and a plant restoring it fails the gate |
| 3. ACMP's walk, tsn-c-stack#32 | `d32c196c`. The donor change is drafted in its own clone of the TSN stack, branch `32-acmp-dirty-walk`, one commit on `main`, not pushed; its handoff and its PR body, with the keyword line for tsn-c-stack#32, are in the evidence packet, and its four acceptance items are met. The gate states two columns, each measured on this tree's image: `STATED_US` at the pin, and `STATED_US_DONOR` with tsn-c-stack#32 applied at the pin in a scratch build. It grades the second, labelled as owed to the pin move (tsn-c-stack#28, tsn-c-stack#31 and tsn-c-stack#32); this tree's pin does not move. A plant that lowers a cost tsn-c-stack#32 does not move fails the gate |
| 4. The ceiling | `24e5d12a`. 0.70 at 1x1/1if and 8x8/2if. 32x32/2if is reported, labelled as pending the owner's choice (more compute, or per-shape contract rates), with the compute its graded load would need for 0.70. A plant that drops a held point's ceiling fails the gate |
| 5. Also found | `AECP_NOTICES_MOST` (40 at two interfaces, against 136 at 32x32/2if) is drafted for #866, unchanged here. The 8x8/2if `answering-every-port` arm's `rom` margin is in the ledger (`044107a5`, section 5): 12 bytes at `a30c9986`, 324 at this head, 132 over with tsn-c-stack#32 at the pin |
| 6. This body | 21,485 characters. The round histories (rounds 12 to 24) are in the evidence packet, `evidence/ROUND-HISTORIES.md` |

**Item 1's basis.** lwSRP refuses a receive (`-SHLAN_ERROR_NO_MEMORY`) only where an allocation fails: `get_or_create_attr` and `map_reserve` under `rx_on_attr` (`third_party/lwSRP/src/core/mrp_mad.c`). The allocations a replay asks for follow from five inputs, each of which holds or is counted while a record waits:
- The receive filter's answers, `interested_msrp` and `interested_mvrp`, read only the sources (fixed), the sinks' bindings and the Domain's VID. While a receive waits `srp_mbx_bind` refuses, and `transmit` makes no declaration and no Domain change.
- An attribute is created only by an allocation, which leaves the pool no larger. It is freed only by `mrp_reclaim` or a participant's destroy, each a block returned (`ctrl_pool_returned`).
- Every Applicant and Registrar state change goes through `deliver_event_changed` or the leave timer, each reported to the observer (`moved()`).
- An attribute's value changes only by a receive (only the retained one is taken meanwhile) or a declaration (none meanwhile).
- The pool's free blocks increase only by a return.

So a refusal is a function of the frame, the pool and the attributes' states. Equal counts and a clear flag bracket no change that could turn it, and no line was found that reads anything else.

**The load at this head** (`load_grade.py --check`):

| Point | Load at the pin | Load with tsn-c-stack#32 (graded, owed to the pin move) | Ceiling | Compute for 0.70 | Its three largest graded terms | A pass's own cost, us |
|---|---:|---:|---:|---:|---|---:|
| 1x1/1if | 0.466 | 0.453 | 0.70 | 1.00x | SRP's channel 0.150, ACMP's records 0.053, AECP's owed frame 0.049 | 180 |
| 8x8/2if | 0.844 | **0.747** | 0.70 | 1.07x | SRP's channel 0.243, AECP's owed frame 0.076, ACMP's records 0.061 | 275 |
| 32x32/2if | 2.150 | 1.659 | reported, pending the owner | 2.37x | SRP's channel 0.519, owed MRPDUs 0.299, THE TRANSMIT's builds 0.150 | 590 |

The costs tsn-c-stack#32 moves, stated, us (pin, then with tsn-c-stack#32): an ACMP record 280, 265 / 440, 305 / 980, 425 at 1x1/1if / 8x8/2if / 32x32/2if; an ADP record 105, 95 / 240, 125 / 735, 270; ACMP's timer slot 185, 165 / 350, 205 / 845, 330; ACMP's owed frame 65, 35 / 185, 40 / 665, 105; the polls' base 155, 155 / 280, 245 / 590, 570.

**What 8x8/2if would need** (0.747 against 0.70, 0.047 to find). Each of its three largest terms, alone:
1. **SRP's channel, 0.243**: its records 0.203 (405 us, one a 2 ms refill) and one retry a centisecond 0.041. It needs an SRP record, at whose cost the retry is stated, from 405 to 326 us (-20 %), or SRP's refill from 2 to 2.61 ms.
2. **AECP's owed frame, 0.076**: a command's notice to 32 recipients, 340 us once a record (0.068), and the registrations' probes 0.008. It needs a record's owed frame from 340 to 103 us (-70 %), or AECP's refill from 5 to 16.5 ms. A notice is owed only by a command that changed something, which has no contract rate of its own.
3. **ACMP's records, 0.061**, 305 us with tsn-c-stack#32 at one a 5 ms refill. It needs an ACMP record from 305 to 68 us (-78 %), or ACMP's refill from 5 to 22.4 ms.

Only the first closes it alone with a cut under a quarter of its cost. Two together can too: SRP's record -10 % with AECP's frame -35 % finds 0.048.

**32x32/2if** (reported, pending the owner): 1.659 with tsn-c-stack#32, 2.150 at the pin, 2.37x the compute for 0.70. tsn-c-stack#32 takes ACMP's records, owed frame and timer slot from 0.637 to 0.186 there (0.186 to 0.093 at 8x8/2if). What is left is led by SRP's channel (0.519, an SRP record 865 us) and THE TRANSMIT's builds (a build of both of an interface's MRPDUs 10,810 us) with their owed MRPDUs, stated at a build of one's cost (7,485 us; no group stages one), together 0.449. tsn-c-stack#32 moves neither.

### What holds at this head

The acceptance of this lane's assignment (S2b, #665: the split firmware within T_svc, cycle work in firmware, owner decision D4 a), read at this head:

- **The rows by measurement** (the CPU budget harness, every group of arm A and of the `answering-every-port` arm at 1x1/1if and 8x8/2if): every row is within its bound except the three egress-held paths (`backlog.owed`, `backlog.owed_behind0` to `3`, `backlog-owed.service.aecp.last`, tsn-c-stack#26): 6 misses of 996 probe instances in 93 groups at 8x8/2if, and of 945 in 94 groups at 1x1/1if. 0 refusals, no `STATED` line. The `answering-every-port` arm: 16 groups at each point, 0 misses of 736 and 280 probe instances, every queued notice within its bound.
- **The pass share** (2.0 ms): 0 of 267,921 work passes over it at 8x8/2if and 0 of 174,507 at 1x1/1if; 0 of 14,202 and 0 of 21,766 in the `answering-every-port` arm.
- **The bounds that hold by construction:** the first queued notice, 22 ms at 8x8/2if and 16 ms at 1x1/1if (THE RETRY's search); the last queued notice at 1x1/1if, 22 ms within its 25 ms ceiling; every pass's polls base and each heavy item within its stated cost (`poll_grade.py`), every round within its own (`round_grade.py`), and every pass given whole to a build or an aged step within its own (`whole_grade.py`), each a gate over every group at both points.
- **What does not hold:** R4, R5 and R6 by every source at either point, the last queued notice at 8x8/2if (74 ms against 70 at THE DRAIN's derived pass count), every row at 32x32/2if, and the long-window load at 8x8/2if (above). Round 23's tier design waits for a load under the ceiling.

### The round histories

Rounds 12 to 24's Description sections, and the decisions their Known limitations listed, are in this round's evidence packet, `evidence/ROUND-HISTORIES.md`, verbatim from round 24's body (the round 25 ruling, item 6).

## Authoritative references

- The round 25 ruling (#665 issuecomment-6751196896) and [A683zd]'s STOP it answers (issuecomment-6751120577); kebag-logic/tsn-c-stack#32 and its four acceptance items; tsn-c-stack#28 and tsn-c-stack#31, which the same pin move carries.
- The round 24 ruling (#665 issuecomment-6734415848) and the round 23 ruling (issuecomment-6732443213), where round 25 leaves them; S15's 32x32/2if simulation shape (#859, `665-s15-32x32` at `7aa6ef0c`).
- IEEE 802.1Q-2018 clause 10 for lwSRP's participant (10.7.4.1 and Table 10-7, JoinTime); Milan v1.2 Table 4.3.
- Milan v1.2 5.3.4.2 and 5.4.5.1 (at most 16 registered controllers an AVB interface, each notified), 5.4.5.2 and Table 5.22 (COUNTERS_CHANGED and its holdoff), 5.4.5.3 (the registration probe's 250 ms retry); `sw/mailbox/mailbox.yaml`, `counters_changed`.
- The protocol timers the arrival bounds cite: Milan v1.2 5.5.2.3 and Table 5.26, 5.6.3.5.3, 5.6.3.5.9 and Table 5.50, 5.6.4.1; IEEE 1722.1-2021 6.2.2.5; IEEE 1722-2016 B.3.4.2 and Table B.8; IEEE 802.1AS-2011 (+Cor1/Cor2) 10.7.2.2, 10.7.3.2 and 11.5.2.2, the edition Milan v1.2 profiles.
- `sw/mailbox/mailbox.yaml`, each channel's `rate` and `tick_ms`; `docs/design/SPLIT_CONTROL_MEMORY.md` section 5 (the ledger), section 13 (the polls by source and the long-window load) and section 14 (the 32x32/2if costs, measured); `tb/verilator/ctrl_service_budget/README.md`; `sw/firmware/ctrl/srp/README.md` (the retry's rule).
- `docs/reference/FR_NFR.md` 3.4.1 and 3.4.2; `sw/firmware/ctrl/loop/ctrl_loop.h` (THE SHARE, THE STEP, THE RETRY, THE TRANSMIT, THE TICK's cap); `sw/firmware/ctrl/aecp/aecp.h`.
- The earlier rounds' rulings and decisions are cited in `evidence/ROUND-HISTORIES.md`.

## How to get into the same state

```sh
git fetch origin
git checkout 3a1d14c21b6b484270a387bae1a7eedc7c0bc2d5
git submodule update --init protocol-processor gptp-processor third_party/lwSRP third_party/tsn-c-stack third_party/verilog-axis
```

The harness's prerequisites are in `tb/verilator/ctrl_service_budget/README.md`: the product LiteX tree, the pinned RV32 SDK and Verilator, with `COURSIER_MODE=offline` and `SBT_OPTS=-Dsbt.offline=true`.

## How to validate

```sh
python3 -B tb/verilator/ctrl_service_budget/load_grade.py --check
python3 -B tb/verilator/ctrl_service_budget/load_grade.py --selftest
python3 -B tb/verilator/ctrl_service_budget/run.py --self-test
python3 -B tb/verilator/ctrl_service_budget/run.py --point 8x8 --build-dir /tmp/budget-8x8 --record-budget-findings --record-share-findings
python3 -B tb/verilator/ctrl_service_budget/run.py --point 1x1 --build-dir /tmp/budget-1x1 --record-budget-findings --record-share-findings
python3 -B tb/verilator/ctrl_service_budget/run.py --point 8x8 --build-dir /tmp/budget-8x8-notice --variant answering-every-port --record-budget-findings --record-share-findings
python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --shard 0/4
make -C tb/verilator/milan_dp twin
```

Expected result at this head:
- `load_grade.py --check` prints the load table and exits 1: `OVER 8x8/2if: the load 0.747 is over its ceiling 0.70`. That is this STOP. `--selftest` exits 0: `load gate: 23 of 23 planted controls refused`.
- The harness self-test reports 0 failures, the load gate's checks among them; the firmware self-test runs as shards 0/4 to 3/4, and its SRP campaign holds the nine retry plants among its arms.
- The 8x8 and 1x1 runs: 0 refusals, no pass over the share, no `STATED` line, every row within its bound but the three egress-held paths; the 8x8 notice run builds (its arm's `rom` 122,556 bytes, within the ledger) with every queued notice within its bound.
- The twin: 0 findings.

The evidence at this head, each on a clean clone of it, never piped:

- **Every `run:` step of every job a pull request to `dev-soft-core` triggers** (`rtl-fast.yml`, `docs.yml`, `elaborate.yml`, `rtl.yml`, as for a ready pull request), each job on its own fresh clone: 139 steps rc 0, 226 not run with a stated reason, 0 bad. Among them:
  - the firmware self-test as its four shards: "mutants: 672 of 672 caught"; the AECP campaign's 212 arms and the SRP campaigns' 337 `[ok]`, the nine retry plants and the two re-caught plants among them;
  - `fw_coverage.py --check` (38 files);
  - `firmware-boundary` and `firmware-verilator` ("ctrl_boundary: PASS");
  - `bdd-conformance` (`cd tests && behave`: 508 scenarios, 2,330 steps).
- **The full sweep**, four shards: 65 of 65 suites, 2,613,726 checks, 0 failures. `capture_coherence` first timed out at its 2,400 s wall clock on a host near full load (result unknown, not a failure). Re-run alone, as the suite runner runs it, on four CPUs: PASS in 2,328 s, 21,721 checks. Every preflight passed.
- **The CPU budget harness** at 8x8/2if and 1x1/1if, every group of arm A and of the `answering-every-port` arm: rc 0 each, with the rows and the share [above](#what-holds-at-this-head). The groups ran at `ca403b0c`, whose images are byte-identical to this head's. At this head each leg was built afresh, a sample of its groups was re-simulated with byte-identical logs, and every group was regraded against the head's build.
- **The lane's gates**, rc 0 each:
  - `git diff --check` against the merge base `1d6bf555`;
  - the idiom, bare-metal and docs checks, and `ctrl_hot.py`;
  - the harness, hooks and NVM-target self-tests, and `test_ctrl_nvm.py --require-rv32 --self-test`;
  - `gen_mailbox.py --check --crosscheck` and `--selftest`, `lint_rtl.py`, `test_soc_options.py`, `test_ctrl_memory.py`, and `test_builder.py --require-rv32`;
  - the split-boot runs and their self-test, and `behave`.
- `load_grade.py --selftest`: 23 of 23 planted controls refused. `load_grade.py --check`: rc 1, `OVER 8x8/2if: the load 0.747 is over its ceiling 0.70`, this STOP.
- The twin: 0 findings.

## Known limitations / out of scope

- **Round 25's decisions, for the owner** ([Round 25](#round-25)):
  1. **8x8/2if is 0.047 over 0.70** after items 1 to 3, graded with tsn-c-stack#32. Each of its three largest terms alone would need: an SRP record 405 to 326 us, or SRP's refill 2 to 2.61 ms; a record's owed AECP frame 340 to 103 us, or AECP's refill 5 to 16.5 ms; an ACMP record 305 to 68 us, or ACMP's refill 5 to 22.4 ms. Or more compute: 1.07x.
  2. **32x32/2if** is reported, not gated: 1.659 with tsn-c-stack#32, 2.37x the compute it would need for 0.70. Decided since (option D, issuecomment-6759183115 and issuecomment-6759193032): per-shape contract rates for the flip, owed to #859, and the compute in #872.
  3. **The pin move** that carries tsn-c-stack#28, tsn-c-stack#31 and tsn-c-stack#32 owes the 8x8/2if `answering-every-port` arm 132 bytes of `rom`: with tsn-c-stack#32 the arm's image is 123,012 bytes, past its 122,880-byte granule. The graded column's costs that only that arm stages, a notice's among them, are the pin's.
- **`AECP_NOTICES_MOST`** caps the notices a datapath reset can leave pending at 40 at two interfaces whatever the shape, against 136 in the 32x32/2if model; the queued-notice bounds and their search are stated for 40. Drafted for #866; unchanged here.
- **A refused SRP record's give-up** past 1 s with a change pending waits at most the centisecond for the retry the change allows (`sw/firmware/ctrl/srp/README.md`).
- **No group stages** a retained record's retry, an owed MRPDU or a registration's probe: each is stated at the cost of the measured work that holds it (an SRP record, a build of one, a response).
- **The three egress-held rows** stay with tsn-c-stack#26.
- **The drafts** (lwSRP, tsn-c-stack) are measured staged and are not pinned here.
- **The platform image's hot list:** four entries name the size fixture's callbacks and place nothing in that image.
- **No fabric option outlives the switch-over:** nothing here adds one. The hybrid-XIP arm still misses T_svc on every path, so D3's rule stands.
- The earlier rounds' decisions for the owner and the manager are in `evidence/ROUND-HISTORIES.md`.

## Definition of Done

- [ ] Linked Issue acceptance criteria are satisfied (#665 stays open: this lane is one part of it)
- [x] New or changed behavior has self-checking tests (the retry's four firmware tests and nine plants; the load gate's 23 plants, each shown able to fail)
- [ ] Required local verification bar passes (this is a STOP: the load gate fails at this head by design; every other gate is listed above)
- [ ] Self-test evidence is posted in a PR comment
- [ ] No undocumented requirement or interface change remains (the load at 8x8/2if and the 32x32/2if choice await the owner; the pin move owes the arm's 132 bytes)
- [ ] Internal cleared-context review is positive
- [ ] External review is positive
- [ ] Blocking and major findings are fixed and re-reviewed
- [ ] No review round remains in flight
- [ ] Candidate merge result is validated per [CONTRIBUTING.md](../CONTRIBUTING.md)
- [x] Documentation is updated where needed (section 5: the arm's margin; section 13: the retry's rule, AECP's owed frame, the two columns and the ceiling; the harness and SRP READMEs)
- [ ] Post-merge containment will be checked before the Issue moves to Done
