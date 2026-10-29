[A693b]

## Contents

- **[Status](#status)** -- REVIEW READY at the head below; `803-adopt-gptp-f97c1803` -> `dev`.
- **[Linked Issue / roles](#linked-issue--roles)** -- The task, the gPTP issues that close after the bench re-run, and roles.
- **[Description](#description)** -- The adoption (round 1) and the round 2 answers to R727-1 and R728-1.
- **[Authoritative references](#authoritative-references)** -- The clauses, the donor PRs and the gate rules.
- **[How to get into the same state](#how-to-get-into-the-same-state)** -- Checkout, submodules and tools.
- **[How to validate](#how-to-validate)** -- The gate commands and the expected results.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** -- What this lane did not change, and the open decision.
- **[Definition of Done](#definition-of-done)** -- The merge bar from CONTRIBUTING.md.

## Status

**REVIEW READY** at `2b1565fd9095d6ec8be514849ba9b92b8f4c5b31`; `803-adopt-gptp-f97c1803` -> `dev` (`5fcec84b`). Round 2 answers the two round-1 reviews (R727-1, R728-1, both NEGATIVE on MINOR only) as the round 2 ruling on #803 directs. At this head:

- The full parent sweep: 64 / 64 suites, 2,191,421 checks, 0 in-suite failures, 0 timed out, as four shard units (round 1: 2,191,417; the four added checks are the two in each `gptp` leg).
- `milan_dp` `gptp` and `gptp-lat` legs: 202 / 202 each (200 before; the two added checks are the ones round 2 adds).
- The physical gPTP leg (`milan_dp_gptp`) against its new 6,900 s deadline, no override: 205 checks, 0 failures over 17.992742740 simulated seconds; 5,391 s on this loaded host, 78.1 % of the deadline.
- Every round-2 check fails under its planted defect, and both reviewer probes, which survived at `fb182b19`, are now killed: 19 (defect, leg) rows, 19 killed.
- The docs workflow under GNU Make 4.3: 44 steps, 42 run all rc 0, 2 skipped by rule; the LiteX builder leg, the Markdown gates on CPython 3.12 and the no-git gates rc 0.
- No synthesis or firmware input changed since `fb182b19`, so round 1's Vivado, Yosys, lint, xvlog and rtl-fast results stand (route-1x1 +481 LUT against the record, tolerance 500; WNS +0.333 ns).

One owner decision is open, on slice headroom (Known limitations).

## Linked Issue / roles

Relates to #803

Relates to FPGA-gPTP issues 87, 88, 89, 90 and 91 (in the gPTP repository): they close after the bench re-run, once this is in an image and the in-house gPTP scenarios pass on the test machine.

Executor: `[A693]` (round 1), `[A693b]` (round 2)
Internal cleared-context reviewer: `[R<n>]` (round 1: `[R727]`)
External reviewer: `[R<n>]` (round 1: `[R728]`)

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

The engine's one port change, authorised in #803, is `pub_path_o`: eight entries from entry 0 (`[8*64-1:0]`), where it carried seven after the grandmaster. `KL_gptp_shadow.pub_path_o` widens with it, and the `gptp_shadow` test wrapper adds `pub_path_head_o`. No top-level port, parameter or register change.

| Commit | Change |
|---|---|
| `1d68756c` | `gptp-processor` gitlink `55680bff` -> `f97c1803` (first-parent: FPGA-gPTP PR 92 `3426089a`, PR 93 `f97c1803`) |
| `a701de12` | FPGA-gPTP PR 92's parent test patch (sha256 `b53944d5...`), applied whole with `git apply --index` |
| `3ef8d86d` | FPGA-gPTP PR 93's companion (`3a3db518...`), applied whole: `KL_gptp_shadow` publishes eight entries from entry 0; `milan_datapath` serves GET_AS_PATH entry 0 from the engine head (IEEE 1722.1-2021 7.4.41.2) and its Table 5.22 comparator watches entry 0; `REGISTER_MAP.md` 0x7DC and `REGISTER_MAP_CLASSES.md`; tsn_fuzz fixtures; gptp_shadow and milan_dp rows |
| `cf188b2b` | Pin-derived records through their generators (ROM ledger row, pin table, both diagrams, 18 donor links, port census header) |
| `ab73efa1` | Statements the companions left on the retired rules: the loss page, the feature ledger's AS_PATH trigger, the milan_dp README, a CSR harness comment |
| `46588545` | `TEST_RESULTS.md` regenerated at this tree (675 pass) and the campaign README's current tally |
| `5e7e120f` | The loss page's new sentence split to the concise-style limit |
| `fb182b19` | The adoption record: the pin page's #803 section and the changelog entry |

### Round 2: the answers to R727-1 and R728-1

| Commit | Finding | Change |
|---|---|---|
| `63a8e123` | F1 (both reviews; Tests, Robustness) | The GET_AS_PATH in-flight cut arm now holds the captured response at its count beat, inside the processor's bounded gather wait, while the empty path commits: the publication lands after the first-count snapshot and before the first path-entry request, and a new check asserts exactly that ordering. The in-flight response's count, entry 0 and (new) entry 1 must stay wholly old. The arm comment now states what the arm proves |
| `40896b8a`, `2b1565fd` | S1 (both reviews; Tests) | The #207 full-queue window is pop-free: a second real Pdelay_Req waits at the queue head behind the first one's response claim, so dispatch cannot run a stale entry while the level is forced full. Both queue pointers are graded equal before and after the window, and the level is restored to its own value |
| `a5a4af26` | F2 (R727-1; Docs), R1 | The pin page and the changelog state the true scope (above). "Its shipping route meets timing at +0.333 ns WNS" |
| `acbbe973` | slice figures (ruling item 6) | `AREA_BUDGET.md`'s slice sentence gives the head's route: 15,843 slices placed, 7 of 15,850 free. Its next sentence, that further growth needs an owner decision, is unchanged |
| `d6404184` | physical deadline (ruling item 5) | The nightly and manual physical job: suite deadline 5,400 -> 6,900 s, job 120 -> 145 min (template and generator), with its pinned contracts and docs |

The GET_AS_PATH snapshot had no check because the processor gathers every entry about 13 cycles after the first-count capture, while the cut's publication commits about 460 cycles after its Announce: the gather had finished before the path changed. At this head the count beat is held 474 cycles and no path-entry request precedes the commit. The RTL comment beside `asp_resp_entry_w` ("Its in-flight cut must complete PUBLISH after the count snapshot but before the first path-entry request") is now true as written; no RTL changes in round 2.

### Every new check fails for its defect

Each defect is planted alone in a clean clone, the leg is rebuilt from scratch, and every named check must print FAIL; a clean pass in the same clone first prints no FAIL at all.

| Defect | Where | At `fb182b19` | At this head: the FAIL line printed (both `gptp` and `gptp-lat` legs) |
|---|---|---|---|
| none (clean) | - | 200 checks: 200 PASS, 0 FAIL | 202 checks: 202 PASS, 0 FAIL |
| GET_AS_PATH entry 0 from the live head, not the snapshot (R727-1 M9, R728-1 M5) | `milan_datapath.sv` | survives, 200 / 200 | `in-flight response remains wholly old GM got 02a1b2fffec3d4e5 exp 00aaccfffe010204` |
| GET_AS_PATH entries 1..7 from the live path (R727-1 M9b, R728-1 M5b) | `milan_datapath.sv` | survives, 200 / 200 | `in-flight response remains wholly old: ends with thisClock got 0000000000000000 exp 02a1b2fffec3d4e5` |
| GET_AS_PATH count served live | `milan_datapath.sv` | - | `in-flight response remains wholly old count two got 0000000000000001 exp 0000000000000002` |
| the cut without its count-beat hold (harness control) | `sim_gptp.cpp` | - | `empty path commits after first-count snapshot, before entry gather got 0000000000000000 exp 0000000000000001` |
| the #207 window without the queued Pdelay_Req (harness control) | `sim_gptp.cpp` | - | `the full-queue window pops and pushes no event got 0000000000000000 exp 0000000000000001`; three stale pops (`rp 1->0`), after which seven checks of the later #88 arm fail too |

Round 1's eleven `milan_dp` defects (five parent RTL reverts, the #207 arm's own control and five donor texts) were re-planted at this head: 11 of 11 killed on every named check. Round 1's gptp_shadow, tsn_fuzz, phc_step and physical rows are unaffected by round 2 (none of their inputs changed) and stand.

### Resources against the current record

Unchanged from round 1: no synthesis input changed since `fb182b19`. Measured through the baseline recipe and checked with `pp_resource_gate.py check` against the committed record:

| Endpoint | Gate | LUT record -> this head (delta, tolerance) | FF (delta, tolerance) | Other |
|---|---|---|---|---|
| `route-1x1` | rc 0, PASS | 51,259 -> 51,740 (+481, 500) | 53,208 -> 53,391 (+183, 600) | slices 15,835 -> 15,843 (+8, 80); RAMB36 74, RAMB18 27, DSP 13 unchanged; WNS +0.236 -> +0.333 ns, WHS +0.028 -> +0.020 ns |
| `ooc-1x1` | rc 0, PASS | 23,828 -> 23,845 (+17, 250) | 20,000 -> 20,000 | RAMB and DSP unchanged |
| `ooc-8x8` | rc 0, PASS | 32,467 -> 32,530 (+63, 316) | 28,220 -> 28,222 (+2, 339) | RAMB and DSP unchanged |

route-1x1 moves +0.94 % in LUTs, under the assignment's 2 % stop. Against dev's own route this adoption adds **+310 LUT, +155 FF, +20 slices**, leaving 7 of 15,850 slices free.

### The physical leg's deadline

Re-projected at this head by the suite README's own method (the scenario is unchanged at 899,637,137 cycles): 5,347 to 5,484 s hosted, 99.0 to 101.6 % of the former 5,400 s suite deadline. A worst case of at most 80 % needs at least 6,855 s; the deadline is now 6,900 s (77.5 to 79.5 %). The job keeps its 30 minutes for setup and upload, so it permits 145 minutes. Only the nightly and manual `physical-gptp` job changes; the generated workflow diff is that job's `timeout-minutes` line.

## Authoritative references

- #803, its assignment comment and its round 2 ruling; R727-1 and R728-1 on this PR.
- IEEE 802.1AS-2011 with Cor1-2013 and Cor2-2015: 10.3.10.2.1 a)-d), 10.3.11 and Figure 10-13, 10.3.12.1.1, 11.2.15 and Figure 11-8.
- IEEE 1722.1-2021 7.4.41.2 (GET_AS_PATH response: count paired with path_sequence); Milan v1.2 Table 5.22 (AS_PATH notification trigger).
- FPGA-gPTP PRs 92 and 93; their parent-companion sections define what the parent adopts.
- `docs/reference/REGISTER_MAP.md` (the GET_AS_PATH snapshot, 0x7DC, 0x7E8), `docs/reference/SUBMODULES.md` (the #803 section), `docs/design/GM_LOSS_RECOVERY.md`, `docs/design/AREA_BUDGET.md`, `docs/testing/CI_WORKFLOWS.md` (the physical job), `tb/verilator/milan_dp/README.md` (the deadline projection).

## How to get into the same state

```sh
git fetch origin
git checkout --detach 2b1565fd9095d6ec8be514849ba9b92b8f4c5b31
git submodule update --init gptp-processor protocol-processor third_party/verilog-axis third_party/lwSRP third_party/tsn-c-stack
git -C gptp-processor rev-parse HEAD
```

Expected: `f97c18035be6ef5345e5af27db2124c5697c1b40`. Tools: Verilator 5.050, sv2v v0.0.12, Yosys 0.66, GNU Make 4.3, tsn-gen at `rtl.yml`'s `TSN_GEN_REV`, Vivado 2026.1 for the resource endpoints.

## How to validate

```sh
make -C tb/verilator/milan_dp gptp
make -C tb/verilator/milan_dp gptp-lat
make -C tb/verilator/gptp_shadow
make -C tb/verilator/tsn_fuzz ptp
make -C tb/verilator/gptp_plane phc-step
VERILATOR_JOBS=4 scripts/run_all_suites.sh /tmp/physical-logs --physical-gptp
scripts/run_all_suites.sh /tmp/sweep-logs
python3 scripts/ci_gate_workflows.py --check
python3 scripts/ci_events.py --check
python3 scripts/measure_test_evidence.py --check
python3 scripts/check_doc_style.py
python3 scripts/docs_check.py
```

To see a reviewer probe fail, plant one at a time and rebuild the leg:

```sh
sed -i 's/asp_served_entry_w = asp_resp_head_r;/asp_served_entry_w = asp_live_head_w;/' hdl/milan/milan_datapath.sv
make -C tb/verilator/milan_dp gptp
git checkout hdl/milan/milan_datapath.sv
sed -i 's/asp_served_entry_w = asp_resp_path_r\[/asp_served_entry_w = asp_live_path_w[/' hdl/milan/milan_datapath.sv
make -C tb/verilator/milan_dp gptp
git checkout hdl/milan/milan_datapath.sv
```

Expected result / pass criteria:

- The `milan_dp` legs print `202 checks: 202 PASS, 0 FAIL` (`gptp` and `gptp-lat`), with `[cut] count beat held 474 cycles; commit seen 1; path-entry request before the commit 0` and `[#207] full-queue window: level 1, rp 1->1, wp 2->2`.
- The first probe prints `FAIL in-flight response remains wholly old GM`; the second `FAIL in-flight response remains wholly old: ends with thisClock`.
- `gptp_shadow` prints `325 checks: 325 PASS, 0 FAIL`; `tsn_fuzz ptp` prints `675 pass, 0 fail, 0 known gaps`; `phc-step` passes with its mutation arm.
- The physical leg passes 205 checks with 0 failures inside its 6,900 s deadline (here 5,391 s with no `SUITE_TIMEOUT` override).
- The sweep tally reports 64 suites and 0 in-suite failures.
- The workflow, CI-event, test-evidence and documentation gates print OK.

## Known limitations / out of scope

- **Slice headroom: an owner decision.** `docs/design/AREA_BUDGET.md` now states the head's route, 7 of 15,850 slices free, and keeps its sentence that the next growth on the shipping image needs its own owner decision. This adoption adds 20 slices over dev's own route. The resource gate passes and the #803 stop (route-1x1 above 2 %) is not reached; the acceptance of these slices is recorded on #803 when the owner rules, before merge.
- **The physical leg's hosted deadline** is a projection until a hosted run of the current scenario completes; the suite README records it.
- FPGA-gPTP 87 to 91 stay open until an image with this pin passes the in-house gPTP scenarios on the test machine. No image was built or flashed here.
- No processor change: `protocol-processor` stays at `ed211803`. VERSION is unchanged; the release step owns the bump.
- Not changed, already stale before this lane: the tsn_fuzz README's dated N10 to N15 pass counts, the milan_dp README's dated per-leg count table, and the roadmap's 0x0055 AS_PATH landing note.

## Definition of Done

- [ ] Linked Issue acceptance criteria are satisfied (all consumer gates rc 0 at this head; the owner's slice acceptance and the bench re-run remain)
- [x] New or changed behavior has self-checking tests (each new check fails under its planted defect)
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
