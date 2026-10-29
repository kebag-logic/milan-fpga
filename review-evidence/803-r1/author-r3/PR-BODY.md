[A693c]

## Contents

- **[Status](#status)** -- REVIEW READY at the head below; `803-adopt-gptp-f97c1803` -> `dev`.
- **[Linked Issue / roles](#linked-issue--roles)** -- The task, the gPTP issues that close after the bench re-run, and roles.
- **[Description](#description)** -- The adoption (rounds 1 and 2) and the round 3 merge of dev after #802.
- **[Authoritative references](#authoritative-references)** -- The clauses, the donor PRs and the gate rules.
- **[How to get into the same state](#how-to-get-into-the-same-state)** -- Checkout, submodules and tools.
- **[How to validate](#how-to-validate)** -- The gate commands and the expected results.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** -- What this lane did not change, and the open decision.
- **[Definition of Done](#definition-of-done)** -- The merge bar from CONTRIBUTING.md.

## Status

**REVIEW READY** at `e06ade312a80eb578579365134ab797cda90622b`; `803-adopt-gptp-f97c1803` -> `dev` (`e78472ff`). Round 3 merges dev `e78472ff` (PR #802, the sixth processor adoption, processor `f65c8ff7`) into the head both reviews found POSITIVE (`2b1565fd`, R727-2 and R728-2), as the round 3 ruling on #803 directs. No rebase and no force: `2b1565fd` stays an ancestor. At this head:

- The combined route passes the resource gate against the record committed at `e78472ff`: route-1x1 51,801 LUT (-211, tolerance 500), 53,760 FF (+53), 15,834 slices (+54, tolerance 80), **16 of 15,850 slices free**, WNS +0.303 ns, WHS +0.028 ns. ooc-1x1 and ooc-8x8 equal the record in every figure.
- The full parent sweep: 64 / 64 suites, 2,191,694 checks, 0 in-suite failures, 0 timed out, as four shard units; the `milan_dp` `gptp` and `gptp-lat` legs print 202 / 202 each.
- The physical gPTP leg against its 6,900 s deadline, no override: 205 checks, 0 failures over 17.992742740 simulated seconds (899,637,137 cycles, unchanged by the merge). The README projection stays 77.5 to 79.5 % of the deadline, within the 80 % bound.
- The rtl-fast workflow, every job its aggregate needs: success, 12 / 12 jobs; `behave` 14 features, 495 scenarios, 2,288 steps passed.
- The docs workflow under GNU Make 4.3: 44 steps, 42 run all rc 0, 2 skipped by rule; the LiteX builder leg, the Markdown gates on CPython 3.12 and the no-git gates rc 0.
- Yosys 60 / 60 tops; lint 89 within its ratchet of 89; xvlog 0 findings; the builder, idiom, pin-record and generator gates rc 0.
- The CI planner holds: `suite_shards.py --selftest` passes and the ownership step passes on all 19 workers. This PR changes no `milan_dp` case, so no leg re-deals and no worker figure moves.

One owner decision is open, on slice headroom (Known limitations).

## Linked Issue / roles

Relates to #803

Relates to FPGA-gPTP issues 87, 88, 89, 90 and 91 (in the gPTP repository): they close after the bench re-run, once this is in an image and the in-house gPTP scenarios pass on the test machine.

Executor: `[A693]` (round 1), `[A693b]` (round 2), `[A693c]` (round 3)
Internal cleared-context reviewer: `[R727]` (rounds 1 and 2)
External reviewer: `[R728]` (rounds 1 and 2)

## Description

### The adoption (round 1)

FPGA-gPTP main `f97c1803` carries five clause fixes against IEEE 802.1AS-2011 with Cor1 and Cor2, the edition Milan v1.2 profiles:

| FPGA-gPTP issue | FPGA-gPTP PR | Behaviour the parent now sees | Clause |
|---|---|---|---|
| 89 | 92 | A grandmaster whose Sync stops for 375 ms is aged while gmPresent holds; with no other peer this station becomes grandmaster then. A priority1 255 grandmaster stays elected and its timeout clears sync only | 10.3.11, Figure 10-13 with Cor1 |
| 90 | 92 | asCapable clears at the fifth consecutive lost Pdelay response, not the fourth | 11.2.15, Figure 11-8 RESET |
| 91 | 92 | A second Pdelay_Resp for the outstanding request resets the exchange; the interval counts as lost | Figure 11-8 |
| 88 | 93 | Only a) to c) disqualify an Announce; a path count other than stepsRemoved+1 and a head other than the grandmaster are accepted; the path is copied as received, head included, plus thisClock; an empty TLV gives `{thisClock}` | 10.3.10.2.1 a)-d) |
| 87 | 93 | An Announce without a path trace TLV writes no pathTrace, so the previous one stays | 10.3.10.2.1 d), 10.3.12.1.1 |

The engine's one port change, authorised in #803, is `pub_path_o`: eight entries from entry 0 (`[8*64-1:0]`), where it carried seven after the grandmaster. `KL_gptp_shadow.pub_path_o` widens with it, and the `gptp_shadow` test wrapper adds `pub_path_head_o`. No top-level port, parameter or register change. `milan_datapath` serves GET_AS_PATH entry 0 from the engine head (IEEE 1722.1-2021 7.4.41.2) and its Milan v1.2 Table 5.22 comparator watches entry 0.

| Commit | Change |
|---|---|
| `1d68756c` | `gptp-processor` gitlink `55680bff` -> `f97c1803` |
| `a701de12`, `3ef8d86d` | FPGA-gPTP PR 92's parent test patch and PR 93's companion, each applied whole with `git apply --index` |
| `cf188b2b` .. `fb182b19` | Pin-derived records through their generators; stale statements; `TEST_RESULTS.md`; the adoption record |

### Round 2 (R727-1, R728-1)

| Commit | Change |
|---|---|
| `63a8e123` | The GET_AS_PATH in-flight cut lands after the first-count snapshot and before the first path-entry request, and a check asserts that ordering; the in-flight response's count, entry 0 and entry 1 stay wholly old |
| `40896b8a`, `2b1565fd` | The #207 full-queue window is pop-free; both queue pointers are graded unmoved |
| `a5a4af26`, `acbbe973` | The pin page and changelog state the true scope; the slice-headroom sentence |
| `d6404184` | The nightly physical job: suite deadline 6,900 s, job 145 min, through the workflow generator |

### Round 3: the merge of dev `e78472ff`

| Commit | Change |
|---|---|
| `6fc0c214` | Merge of dev `e78472ff` (parents `2b1565fd`, `e78472ff`). Git conflicted exactly in the files the ruling lists. `CHANGELOG.md` and `docs/reference/SUBMODULES.md` keep both adoption entries (the pin table carries gPTP `f97c1803` and processor `f65c8ff7`; the #803 section now says the processor stays at `f65c8ff7`); `RUNNING_TESTS.md` keeps the 6,900 s deadline and the nineteen workers; `AREA_BUDGET.md` keeps dev's table (the record) and both sides' sentences. `syn/yosys/rom_digests.tsv` was regenerated by `syn/yosys/ooc.sh --record-rom-digests` (the result is the union of both sides' rows), and the boundary diagram, its PNG and the manifest by `docs/diagrams/submodule_boundaries.gen.py`. No generated file was resolved by hand. `milan_datapath.sv` and `rtl.yml` merged without conflict; the workflow equals its generator's output |
| `e06ade31` | The combined route's figures in the adoption record and the slice-headroom sentence |

### Resources on the combined tree

Measured through the baseline recipe at the merge and checked with `pp_resource_gate.py check` against the record committed at `e78472ff` (the twelfth record, #799, under the owner decision of 2026-10-28). That record is dev `e78472ff`'s own route: its measured commit `8b76de69` and `e78472ff` share every synthesis input, and the #799 route checked against it matched in every figure.

| Endpoint | Gate | LUT record -> this head (delta, tolerance) | FF (delta, tolerance) | Other |
|---|---|---|---|---|
| `route-1x1` | rc 0, PASS | 52,012 -> 51,801 (-211, 500) | 53,707 -> 53,760 (+53, 600) | slices 15,780 -> 15,834 (+54, 80): 16 of 15,850 free; RAMB36 74, RAMB18 27, DSP 13 unchanged; WNS +0.440 -> +0.303 ns, WHS +0.036 -> +0.028 ns; fully routed |
| `ooc-1x1` | rc 0, PASS | 24,346 -> 24,346 (0, 250) | 20,404 -> 20,404 (0, 250) | RAMB and DSP unchanged |
| `ooc-8x8` | rc 0, PASS | 34,156 -> 34,156 (0, 316) | 29,782 -> 29,782 (0, 339) | RAMB and DSP unchanged |

This adoption's share against dev's own route is **-211 LUT, +53 FF, +54 slices** and -0.137 ns of WNS. In the placed hierarchy `KL_gptp_shadow` moves -169 LUT and +119 FF; the +119 FF equals round 1's measurement over the earlier dev route. Untouched blocks move by placement (`KL_pp_shadow` -313 LUT, the CSR block +211), as earlier rebaselines record. The ooc tops instantiate none of the files this adoption changes.

### The CI shard plan

The six case-partitioned suites' inventories are byte-identical at dev `e78472ff` and at this head (`milan_dp` 24 cases). This PR changes checks inside the `gptp` and `gptp-lat` cases and the scheduled physical suite, not a case, so the nineteen-worker projection is dev's and no figure changes.

### The physical leg's deadline

Re-projected at this head by the suite README's method. The merged scenario still runs 899,637,137 cycles, so the projection is unchanged: 5,347 to 5,484 s hosted, 77.5 to 79.5 % of the 6,900 s deadline, within the 80 % bound. The 145-minute job keeps 53.6 to 55.9 minutes of margin. The method scales by cycles, so the merged model's per-cycle cost was checked too. Both heads' physical simulations ran together under one load, each on its own CPU. Over the same simulated interval this head took 0.981 times the wall time of `2b1565fd`. The README and both timeouts are unchanged.

## Authoritative references

- #803, its assignment comment and its round 2 and round 3 rulings; R727-1, R728-1, R727-2 and R728-2 on this PR.
- IEEE 802.1AS-2011 with Cor1-2013 and Cor2-2015: 10.3.10.2.1 a)-d), 10.3.11 and Figure 10-13, 10.3.12.1.1, 11.2.15 and Figure 11-8.
- IEEE 1722.1-2021 7.4.41.2 (GET_AS_PATH response); Milan v1.2 Table 5.22 (AS_PATH notification trigger).
- FPGA-gPTP PRs 92 and 93; PR #802 (#799) for the processor pin, the twelfth resource record and the nineteen workers.
- `docs/reference/SUBMODULES.md` (the #799 and #803 sections), `docs/design/AREA_BUDGET.md` (the record and the slice limit), `docs/testing/CI_WORKFLOWS.md` (the shard plan and the physical job), `tb/verilator/milan_dp/README.md` (the deadline projection).

## How to get into the same state

```sh
git fetch origin
git checkout --detach e06ade312a80eb578579365134ab797cda90622b
git submodule update --init gptp-processor protocol-processor third_party/verilog-axis third_party/lwSRP third_party/tsn-c-stack
git -C gptp-processor rev-parse HEAD
git -C protocol-processor rev-parse HEAD
```

Expected: `f97c18035be6ef5345e5af27db2124c5697c1b40` and `f65c8ff7c673aaa8e2ea8da654f081ddb13588d8`. Tools: Verilator 5.050, sv2v v0.0.12, Yosys 0.66, GNU Make 4.3, tsn-gen at `rtl.yml`'s `TSN_GEN_REV`, Vivado 2026.1 for the resource endpoints.

## How to validate

```sh
git merge-base --is-ancestor 2b1565fd9095d6ec8be514849ba9b92b8f4c5b31 HEAD
git merge-base --is-ancestor e78472ffde3da5eeecd4f00e27dcf58a24bfcfdf HEAD
bash syn/yosys/ooc.sh --record-rom-digests
git diff --exit-code syn/yosys/rom_digests.tsv
python3 docs/diagrams/submodule_boundaries.gen.py --check
python3 scripts/check_submodule_docs.py
python3 scripts/ci_gate_workflows.py --check
python3 scripts/ci_events.py --check
python3 scripts/suite_shards.py --selftest
scripts/run_all_suites.sh --ci-pieces --shard 1/19 --list
python3 syn/ooc/pp_resource_gate.py check-baseline
python3 scripts/check_doc_style.py
python3 scripts/docs_check.py
make -C tb/verilator/milan_dp gptp
scripts/run_all_suites.sh /tmp/sweep-logs
VERILATOR_JOBS=4 scripts/run_all_suites.sh /tmp/physical-logs --physical-gptp
```

Expected result / pass criteria:

- Both ancestry checks exit 0: the branch was merged, not rebased.
- The ledger is unchanged after re-recording; the diagram and submodule checks print OK; the workflow, CI-event and planner checks pass; worker 1's list holds `tsn_fuzz`.
- The `milan_dp` `gptp` leg prints `202 checks: 202 PASS, 0 FAIL`.
- The sweep tally reports 64 suites and 0 in-suite failures; the physical leg passes 205 checks inside its 6,900 s deadline.
- The resource endpoints, measured by `docs/testing/PP_SHADOW_BASELINE_RECIPE.md`, pass `pp_resource_gate.py check` with the figures above.

## Known limitations / out of scope

- **Slice headroom: an owner decision.** The combined route leaves 16 of 15,850 slices free; this adoption adds 54 over dev's own route. `docs/design/AREA_BUDGET.md` states it and keeps its sentence that the next growth on the shipping image needs its own owner decision. The resource gate passes, and no stop condition of the round 3 ruling is reached.
- **The physical leg's hosted deadline** is a projection until a hosted run of the current scenario completes.
- FPGA-gPTP 87 to 91 stay open until an image with this pin passes the in-house gPTP scenarios on the test machine. No image was built or flashed here.
- VERSION is unchanged; the release step owns the bump.

## Definition of Done

- [ ] Linked Issue acceptance criteria are satisfied (all consumer gates rc 0 at this head; the owner's slice acceptance and the bench re-run remain)
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
