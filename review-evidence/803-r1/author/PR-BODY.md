[A693]

## Contents

- **[Status](#status)** -- REVIEW READY at the head below; `803-adopt-gptp-f97c1803` -> `dev`.
- **[Linked Issue / roles](#linked-issue--roles)** -- The task, the gPTP issues that close after the bench re-run, and roles.
- **[Description](#description)** -- The gitlink, both companions, the review fixes, the records and the resource delta.
- **[Authoritative references](#authoritative-references)** -- The clauses, the donor PRs and the gate rules.
- **[How to get into the same state](#how-to-get-into-the-same-state)** -- Checkout, submodules and tools.
- **[How to validate](#how-to-validate)** -- The gate commands and the expected results.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** -- What this lane did not change, and the open decision.
- **[Definition of Done](#definition-of-done)** -- The merge bar from CONTRIBUTING.md.

## Status

**REVIEW READY** at `fb182b19925b9ea24443d48d0e71b656de52b8ae`; `803-adopt-gptp-f97c1803` -> `dev` (`5fcec84b`). Every consumer gate #803 lists is rc 0 at this head:

- The full parent sweep: 64 / 64 suites, 2,191,417 checks, 0 in-suite failures, 0 timed out. Among them `milan_dp` (its `gptp` and `gptp-lat` legs 200 / 200 each), `milan_dp_gm_steps` 202, `gptp_shadow` 325 and `tsn_fuzz` 897, whose `ptp` campaign passes 675 with its results file fresh.
- The physical gPTP leg (`milan_dp_gptp`): 205 checks, 0 failures, over 17.992742740 simulated seconds.
- The rtl-fast workflow, every job: success, behave 495 scenarios.
- Yosys: 60 / 60 tops.
- RTL lint and xvlog: within ratchet, 0 xvlog findings.
- The four idiom gates pass.
- The docs workflow under GNU Make 4.3: 44 steps, 42 run all rc 0, 2 skipped by rule.
- All three resource endpoints pass against the current record.

One owner decision is open, on slice headroom (Known limitations).

## Linked Issue / roles

Relates to #803

Relates to FPGA-gPTP issues 87, 88, 89, 90 and 91 (in the gPTP repository): they close after the bench re-run, once this is in an image and the in-house gPTP scenarios pass on the test machine.

Executor: `[A693]`
Internal cleared-context reviewer: `[R<n>]`
External reviewer: `[R<n>]`

## Description

FPGA-gPTP main `f97c1803` carries five clause fixes against IEEE 802.1AS-2011 with Cor1 and Cor2, the edition Milan v1.2 profiles:

| FPGA-gPTP issue | FPGA-gPTP PR | Behaviour the parent now sees | Clause |
|---|---|---|---|
| 89 | 92 | A grandmaster whose Sync stops for 375 ms is aged while gmPresent holds; with no other peer this station becomes grandmaster then. A priority1 255 grandmaster stays elected and its timeout clears sync only | 10.3.11, Figure 10-13 with Cor1 |
| 90 | 92 | asCapable clears at the fifth consecutive lost Pdelay response, not the fourth | 11.2.15, Figure 11-8 RESET |
| 91 | 92 | A second Pdelay_Resp for the outstanding request resets the exchange; the interval counts as lost | Figure 11-8 |
| 88 | 93 | Only a) to c) disqualify an Announce; a path count other than stepsRemoved+1 and a head other than the grandmaster are accepted; the path is copied as received, head included, plus thisClock; an empty TLV gives `{thisClock}` | 10.3.10.2.1 a)-d) |
| 87 | 93 | An Announce without a path trace TLV writes no pathTrace, so the previous one stays | 10.3.10.2.1 d), 10.3.12.1.1 |

The engine's one port change, authorised in #803, is `pub_path_o`: eight entries from entry 0 (`[8*64-1:0]`), where it carried seven after the grandmaster. No parameter changes; the source set is unchanged.

| Commit | Change |
|---|---|
| `1d68756c` | `gptp-processor` gitlink `55680bff` -> `f97c1803` (first-parent: FPGA-gPTP PR 92 `3426089a`, PR 93 `f97c1803`) |
| `a701de12` | FPGA-gPTP PR 92's parent test patch (sha256 `b53944d5...`), applied whole with `git apply --index`: the gptp_plane, milan_dp, physical-rate and tsn_fuzz benches expect the fifth lost response and the Sync receipt ageing |
| `3ef8d86d` | FPGA-gPTP PR 93's companion (`3a3db518...`), applied whole: `KL_gptp_shadow` publishes eight entries from entry 0; `milan_datapath` serves GET_AS_PATH entry 0 from the engine head (IEEE 1722.1-2021 7.4.41.2) and its Table 5.22 AS_PATH comparator watches entry 0; `milan_csr` port comments; `REGISTER_MAP.md` 0x7DC and `REGISTER_MAP_CLASSES.md`; tsn_fuzz fixtures; gptp_shadow and milan_dp rows |
| `cf188b2b` | Pin-derived records through their generators: the ROM ledger row (`gptp_ucode.hex` `b21b244f...`, equal to the donor's own image), the pin table, the boundary and time-sync diagrams, 18 FPGA-gPTP donor links, and the port census header (`hdl 2121 -> 2158`, dev's drift since #771; this lane adds no port) |
| `ab73efa1` | Review fixes, statements the companions left reading the retired rules: the loss page (Sync timeout split by gmPresent, the fifth lost response), the feature ledger's AS_PATH trigger, the milan_dp README (five unanswered intervals; the physical leg's deadline projection re-scaled to the longer scenario), and a CSR harness comment |
| `46588545` | `TEST_RESULTS.md` regenerated at this tree (675 pass; only the date stamp differs from the companion's) and the campaign README's current tally |
| `5e7e120f` | The loss page's new sentence split to the concise-style limit |
| `fb182b19` | The adoption record: the pin page's #803 section and the changelog entry |

Both companions apply cleanly, no fuzz. Every pre-image equals dev's except `docs/testing/TESTING.md` and `README.md`, which dev moved after the companions' base and which apply by context. No top-level port, parameter or register-map change beyond what the companions carry: `milan_datapath` keeps its ports, `milan_csr` changes comments, the register map changes text only, and VERSION is unchanged.

### Every new check fails for its defect

Each defect is planted alone in a clean clone, the suite is rebuilt from scratch, and every named check must print FAIL; a clean pass in the same clone first prints no FAIL at all. Parent defects revert the companion RTL one property at a time; engine defects are the donor's own planted texts, taken by name from its mutation arm.

| Suite | Clean | Defects planted | Killed on every named check |
|---|---|---:|---:|
| `gptp_shadow` (325 checks) | 0 FAIL | 7 | 7 |
| `milan_dp` `gptp` leg (200 checks) | 0 FAIL | 11 | 11 |
| `tsn_fuzz` `ptp` (675 checks) | 0 FAIL | 2 | 2 |
| `gptp_plane` `phc-step` | 0 FAIL | 1 | 1 |
| physical-rate leg (`milan_dp` `ax1x1gptp`) | (the clean leg below) | 2 | 2 |

| Defect | Where | What fails, in the suite's own words (first named check) |
|---|---|---|
| P1 path generation ignores entry 0 | `KL_gptp_shadow.sv` | `entry-0-only change spends one path generation got ...5 exp ...6`; milan_dp `entry-0-only change advances generation once` |
| P2 entry 0 not published | `KL_gptp_shadow.sv` | `published path head is the received head got 0 exp <GM>`; milan_dp `#88 post-cut response is {thisClock}` |
| P3 GET_AS_PATH entry 0 is the grandmaster again | `milan_datapath.sv` | `#87 TLV-less GM switch: GET_AS_PATH entry 0 is still GMID` and three more |
| P4 AS_PATH notification ignores entry 0 | `milan_datapath.sv` | `entry-0-only change emits one GET_AS_PATH push` |
| P5 CSR face takes entries 0..6 | `milan_datapath.sv` | `#88 GET_AS_PATH entry 1 is the parent` and two more |
| P6 a full event queue refuses uncounted | engine | `a full queue moves only the event count` (the rewritten #207 arm) |
| D1 TLV-less Announce publishes `{thisClock}` (87) | engine | `TLV-less selected PathTrace keeps its count got 1 exp 4`; milan_dp `TLV-less fabric publication keeps the path count` |
| D2 the 2020 rule: empty without a TLV (87) | engine | `TLV-less selected PathTrace keeps its count`; milan_dp `#87 TLV-less GM switch: GET_AS_PATH keeps count five` |
| D3 received head replaced by the grandmaster (88) | engine | `path headed elsewhere publishes the received head`; milan_dp `#88 GET_AS_PATH entry 0 is the received head` |
| D4 path-head refusal restored (88) | parser | `better vector, path-trace head is not the announced grandmaster (10.3.10.2.1): adopted`; shadow and milan_dp count three |
| D5 path-count refusal restored (88) | parser | `better vector, one path-trace hop against stepsRemoved 1 (10.3.10.2.1): adopted` and both drop-counter checks |
| D6 empty-path refusal restored (88) | parser | `empty PathTrace publishes count one`; milan_dp `empty PathTrace serves count one` |
| D7 / X7 asCapable at the fourth loss (90) | microcode generator | `asCapable falls at the fifth unanswered request after a crossing exchange got=4 exp=5`; physical `five unanswered Pdelay intervals elapsed` (loss after 4.999 s) |
| X8 Sync timeout only clears sync-ok (89) | microcode generator | physical `the 375 ms Sync timeout makes this station grandmaster`; `375 ms Sync timeout asserts tu in the synchronised master role got=0x1 exp=0x3` |

### Resources against the current record

Measured through the baseline recipe (single-worker synthesis, Vivado 2026.1, one run at a time) and checked with `pp_resource_gate.py check` against the committed record (the 2026-10-23 record at dev `e5b480a3` plus #770):

| Endpoint | Gate | LUT record -> this head (delta, tolerance) | FF (delta, tolerance) | Other |
|---|---|---|---|---|
| `route-1x1` | rc 0, PASS | 51,259 -> 51,740 (+481, 500) | 53,208 -> 53,391 (+183, 600) | slices 15,835 -> 15,843 (+8, 80); RAMB36 74, RAMB18 27, DSP 13 unchanged; WNS +0.236 -> +0.333 ns, WHS +0.028 -> +0.020 ns |
| `ooc-1x1` | rc 0, PASS | 23,828 -> 23,845 (+17, 250) | 20,000 -> 20,000 | RAMB and DSP unchanged |
| `ooc-8x8` | rc 0, PASS | 32,467 -> 32,530 (+63, 316) | 28,220 -> 28,222 (+2, 339) | RAMB and DSP unchanged |

route-1x1 moves +0.94 % in LUTs, under the assignment's 2 % stop. This adoption's own share, against dev's own route at the same RTL as the base (the nightly area measurement of dev `97aab1d0`, the same shipping directive; its figure for the record's own dev equals the record exactly): **+310 LUT, +155 FF, +20 slices** (dev 51,430 / 53,236 / 15,823). The remainder, +171 LUT, is dev's drift since the record. In the placed hierarchy `KL_gptp_shadow` grows +251 LUT / +119 FF: entry 0 and its compare in the plane's own logic (+231 / +64), the engine +55 FF, and the parser -65 / -80 with the strict PathTrace rules retired. The standalone endpoints synthesize `KL_pp_shadow`, which instantiates none of the changed RTL, so their small moves are dev's drift.

The route has 101,739 of 101,739 nets routed and 0 routing errors, and IOB packing passes 21, fails 0 (1 inert, `eth0_rx_er`). Every corner meets: Slow +0.333 / +0.050 ns, Fast +1.638 / +0.020 ns.

## Authoritative references

- #803 and its assignment comment.
- IEEE 802.1AS-2011 with Cor1-2013 and Cor2-2015: 10.3.10.2.1 a)-d), 10.3.11 and Figure 10-13, 10.3.12.1.1, 11.2.15 and Figure 11-8.
- IEEE 1722.1-2021 7.4.41.2 (GET_AS_PATH response: count, path_sequence); Milan v1.2 Table 5.22 (AS_PATH notification trigger).
- FPGA-gPTP PRs 92 and 93; their parent-companion sections define what the parent adopts.
- `docs/reference/SUBMODULES.md` (the #803 section), `docs/reference/REGISTER_MAP.md` 0x7DC, `docs/design/GM_LOSS_RECOVERY.md`, `docs/design/AREA_BUDGET.md` (the resource gate and its slice note), `docs/testing/PP_SHADOW_BASELINE_RECIPE.md`.

## How to get into the same state

```sh
git fetch origin
git checkout --detach fb182b19925b9ea24443d48d0e71b656de52b8ae
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
python3 scripts/check_gptp_docs.py --with-submodule
python3 scripts/check_submodule_docs.py
bash syn/yosys/ooc.sh --record-rom-digests
git diff --exit-code syn/yosys/rom_digests.tsv
python3 syn/ooc/pp_resource_gate.py check-baseline
```

Expected result / pass criteria:

- The `milan_dp` legs print `200 checks: 200 PASS, 0 FAIL` (`gptp` and `gptp-lat`).
- `gptp_shadow` prints `325 checks: 325 PASS, 0 FAIL`.
- `tsn_fuzz ptp` prints `675 pass, 0 fail, 0 known gaps` and its artifact freshness passes.
- `phc-step` passes with its mutation arm.
- The physical leg passes 205 checks with 0 failures. On a loaded host it can need `SUITE_TIMEOUT` above its 5,400 s budget; here it took 5,494 s.
- The sweep tally reports 64 suites and 0 in-suite failures.
- Both documentation gates are OK at the f97c1803 gitlink.
- The ROM ledger regenerates byte-identically.
- `check-baseline` passes 3 endpoints.
- `pp_resource_gate.py check` passes route-1x1 (+481 LUT, tolerance 500), ooc-1x1 (+17) and ooc-8x8 (+63) against the record.

## Known limitations / out of scope

- **Slice headroom: an owner decision.** `docs/design/AREA_BUDGET.md` records 15 free slices on the shipping image and says the next growth needs its own owner decision. This adoption adds 20 slices over dev's own route, leaving 7 of 15,850. The resource gate passes and the #803 stop (route-1x1 above 2 %) is not reached, so no record was rewritten and the area pages are unchanged.
- **The physical leg's hosted deadline.** The fifth-lost-response rule makes the scenario one Pdelay interval longer. Re-scaled as the suite README derives it, the hosted projection is 99.0 to 101.6 % of the 5,400 s budget; the README now states this. The hosted record already shows one timeout of this suite, and the workflow policy assigns its scheduling to a follow-up.
- FPGA-gPTP 87 to 91 stay open until an image with this pin passes the in-house gPTP scenarios on the test machine. No image was built or flashed here.
- No processor change: `protocol-processor` stays at `ed211803`. VERSION is unchanged; the release step owns the bump.
- Not changed, already stale before this lane: the tsn_fuzz README's dated N10 to N15 pass counts, and the roadmap's 0x0055 AS_PATH landing note.

## Definition of Done

- [x] Linked Issue acceptance criteria are satisfied (all consumer gates rc 0; the gPTP issues close after the bench re-run)
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
