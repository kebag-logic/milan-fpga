[R835] NEGATIVE - exact head 62298ab5cbfeb7056e4567f70e69d578201c75e0

# R835-3: cleared-context internal review of PR #901 (issue #895), delta round 5

- **Head:** `62298ab5cbfeb7056e4567f70e69d578201c75e0`, tree `71f9951455c31270524f6931cf621c21af6a82cf`, base `dev-soft-core` (merge-base `cec88385`).
- **Delta reviewed:** `18300f6e` (round 2) to `62298ab5`.
  - Round 3's lane commits `e9011df6`..`9e30c2c3`: #905's SRC_SID writer, the names patch, the 8 B state, the names-runs test and the docs.
  - Round 4's sync merges `cd6d79b6`, `a93fceae` and `91c3fc0e`. For these I checked only this lane's conflict resolution and recomputed figures, not #902's own code.
  - Round 5's six commits `0d2662c0`..`62298ab5`.
- **Authority:** #895's acceptance 1-5 as amended by issuecomment-6840463408, and the round-4 ruling issuecomment-6876349305, items 1-4 and its STOP triggers. Acceptance 6 (hardware) is out of scope.

**Verdict: NEGATIVE.** One MAJOR and one MINOR are open. Both are in the restated cost tables. Every ruling item the lane was given is applied as written. Every row reproduces. The ledger, the hold-off, the idiom commit and the gate receipts all check out.

- **F1 (MAJOR):** the head's own cost receipt puts the 1x1/1if polls' base 10 µs over the cost the tables state. The round-5 restatement did not cover it. At its rule figure, the slice rule picks 950 µs instead of the built 900 µs, and the tree's own control then refuses the tree. That is a STOP trigger the ruling names.
- **F2 (MINOR):** the same kind of omission at 8x8/2if for AMAP_LIVE_WRITE. It only moves a reported row.

---

## Findings

### R835-3-F1 — MAJOR — Conformance, RTL, Tests, Docs — the 1x1/1if polls' base is stated at 205 µs against a measured 20,456 cycles (215 µs by the rule); at its rule figure the slice rule leaves the built design

- **Where:**
  - `tb/verilator/ctrl_service_budget/poll_grade.py:87` (`STATED_US = {1: dict(base=205, ...`);
  - `tb/verilator/ctrl_service_budget/load_grade.py:184` (`STATED_US_DONOR['1x1/1if']['base']: 205`);
  - the claims built on them: `docs/design/SPLIT_CONTROL_MEMORY.md:2536-2537,2541`; PR body "every other `load_grade.py` cost within"; REVIEW READY issuecomment-6880958086 "Measured costs … each within the restated tables".
- **Evidence:**
  - **The measurement.** The author's round-5 receipt `author-r5/receipts/costs/1x1/costs.txt` line 1 reads `1x1/1if base most 20,456 CPU cycles, stated 215 us; R5-A1-view/acmp-cmd`. Round 4's `author-r4/receipts/costs/G1/costs.txt` gives the same.
  - **Same quantity as `poll_grade`'s base.** Section 13 (`SPLIT_CONTROL_MEMORY.md:2466`) names `acmp-cmd` as the base's heaviest leg. It derived today's 205 µs from 19,159 cycles on `da1869a3` by the rule (measurement + 5 %, rounded up to 5 µs).
  - **The head has moved it.** It is +1,297 cycles (+6.8 %) over that figure. By the same rule the base is 215 µs.
  - **The table under-states it.** Stated 205 µs is 20,500 cycles, 44 cycles (0.2 %) above the raw measurement, so the harness's raw `STATED` check passes. It is below the rule figure every restated cost is held to.
  - **The precedent.** Ruling item 2 restated the 1x1/1if TICK from 45 to 50 µs. 45 µs was also above that TICK's raw measurement (43.85 µs) and below its rule figure. The base is in the same position.
  - **Why it was missed.** The lane's drift survey compared only `load_grade.py`'s keys (PR body: "every other `load_grade.py` cost within"). `poll_grade.py`'s base, which feeds every pass's cost (`events_none + base`, `rows_tiers.py`), was not compared. My comparison of every cost key against both tables is `receipts/costs-vs-stated.txt`. Apart from the ruled AECP record, this base is the only 1x1/1if cost whose rule figure is over what is stated.
- **Probe:** `scripts/probe_base215.sh`, `receipts/graders-head/`, `receipts/probe-base215/`. The only edit is `base=205` -> `215` in `poll_grade.py` (`receipts/probe-base215/poll_grade.diff`).

  | Check (1x1/1if) | Head as committed | Base at its rule figure, 215 µs |
  |---|---|---|
  | `flip_grade.py --check --point 1x1/1if` | PASS: txL 47.86, last 127.08, ACMP 28.85 | PASS: txL 48.09, last 127.76, ACMP 29.02 |
  | `paced_rows.choice` | 9 ms | 9 ms |
  | `load_grade.py --check` | PASS, 0.515 / 0.511 | PASS, 0.515 / 0.511 |
  | `rows_tiers.slice_choice` / `ruled` / built | 900 (+0.0225) / 900 / 900 | **950 (+0.0176) / 950 / 900** |
  | `tier_grid.py --point 1x1/1if` CHOSEN | slice 900 µs | **slice 950 µs** |
  | `rows_tiers.py --selftest` | 971 of 971, rc 0 | **969 of 971, rc 1**: `ESCAPED the built design's slice not the rule's`, `ESCAPED THE PACE's edits counted 1 + floor(w / P)` |

- **Impact:**
  - At the cost the tree's own rule assigns, the tree's own gate refuses it: the built slice is not the rule's. The ruling lists "`tier_grid.py` not holding the built design" as a round-5 STOP trigger.
  - The head's claims rest on a cost 0.2 % above its measurement. These are the slice rule choosing 900 µs, "`tier_grid.py` holds the built design", acceptance 4 composed, and section 13's closing summary.
  - The REVIEW READY already notes that 5-10 µs cost moves flip the slice choice (950 at #894's two costs, 900 at the restated ones). This cost is in the same position.
  - The pace control's planted earlier rule also escapes at the rule cost. So that control's detection depends on this margin.
  - Whether #902's own head measures the same base was not determinable from public evidence. Either way, the figure is this head's.
- **Required outcome:**
  - State the 1x1/1if polls' base by the rule at this head's measurement, in `poll_grade.py` and in the `STATED_US_DONOR` column.
  - Alternatively, publish the base's heaviest value as `poll_grade.held` reports it at this head, if it differs from the cost parser's 20,456.
  - Re-run the flip check, the pace rule, `tier_grid.py` and `rows_tiers.py --selftest`.
  - Survey every stated table the rows read against the legs' measurements by the rule (`poll_grade.STATED_US`, `rows_tiers.DATAPATH_US`, `ctrl_loop.h`'s pass costs), not only `load_grade.py`'s.
  - If the slice rule then takes 950 µs against the built 900, that is the ruling's STOP trigger. Publish it for a decision rather than choosing an interpretation.
  - Correct section 13's costs bullet and closing summary, the PR body and the REVIEW READY to match.
- **Verification:**
  - `scripts/costs_vs_stated.py` over the new cost receipts shows no stated cost below its rule figure, the ruled AECP record apart.
  - `rows_tiers.py --selftest` and `tier_grid.py --point 1x1/1if` agree with the stated slice at the restated tables.

### R835-3-F2 — MINOR — Conformance, Tests — the 8x8/2if AMAP_LIVE_WRITE cost is stated at 25 µs against a head measurement of 2,426 cycles (30 µs by the rule)

- **Where:** `tb/verilator/ctrl_service_budget/rows_tiers.py:100` (`'8x8/2if': {... 'AMAP_LIVE_WRITE': 25}`).
- **Evidence:**
  - `author-r5/receipts/costs/8x8/events.json` gives `AMAP_LIVE_WRITE most_cycles 2426`, i.e. 24.26 µs, or 25.47 µs with the 5 %. Rounded up to 5 µs that is 30, over the 25 stated.
  - Section 13 states this cost from #902's `datapath-events` group: 22.65 µs at 8x8/2if.
  - The round-1 parser's measure may not be #902's quantity. At 1x1/1if it reads 23.18 µs where #902's group read 25.51 µs. So whether a defect exists is unsure, but it is not a wording question.
  - Round 5 restated 8x8/2if's other four drifts but did not check `DATAPATH_US`.
- **Impact:**
  - The 8x8/2if rows are reported, not held, so no held verdict moves.
  - Acceptance 4 asks for the 8x8/2if rows "by measurement". A cost stated under its head measurement plus 5 % makes those reported rows optimistic.
- **Required outcome:** do one of the following, and state the result in section 13:
  - show the `datapath-events` group's AMAP_LIVE_WRITE at this head at most 23.80 µs (25 / 1.05) at 8x8/2if;
  - or restate it by the rule, and report the 8x8/2if rows again.
- **Verification:** the group's measurement at this head is published against `DATAPATH_US`.

### RESIDUE

- **R835-3-RS1 — RESIDUE — Docs.** The PR #901 body, lines 41-42, says "Internal cleared-context reviewer: to be assigned / External reviewer: to be assigned". R835-3 has publicly started (PR #901 issuecomment-6881026642).
  - Exact fix: "Internal cleared-context reviewer: `[R835]` (R835-3, started issuecomment-6881026642)". The external line is updated when an external review starts.

### SUGGESTIONS (optional; none affects coverage)

- **R835-3-S1 — Robustness — `sw/firmware/ctrl/maap/maap_mbx.c` `maap_mbx_start`/`declaring`.**
  - The written mark `maap_mbx_start` sets counts as "written since it last opened" for a source that has never opened.
  - So a stream_id the source port changes after start and before the source's first opening is not written again. `F905AStreamIdChangedWhileClosedIsWrittenBeforeTheGateReopens` covers only a change after an opening.
  - This cannot happen on the platform today: `ctrl_plat.c` `stream_id()` is the entity MAC and the output's unique ID, both constant.
  - Optional: state that invariant beside the mark, or add the case to the test.
- **R835-3-S2 — Tests — the harness's raw `STATED` check.**
  - It compares a measurement with the stated cost without the rule's 5 %. A stated cost can therefore pass the legs while sitting under its rule figure, which is F1's case.
  - Optional: have a cost audit (as `scripts/costs_vs_stated.py` here) read the legs' cost receipts against every stated table at each re-measure.
- **R835-3-S3 — Docs.** `SPLIT_CONTROL_MEMORY.md:519-529` titles its table "on #894's tiers `7398ec0a`" but states the deltas "Against #894's head `5b264bf2`".
  - Optional: compare against `7398ec0a`, or say that its images equal `5b264bf2`'s.
- **R835-2-S2 (retained) — Docs, evidence process.** In the author-r5 packet the same four logs again fail their `INDEX.md` hashes. Each is 8 or 12 B shorter, consistent with a host-path scrub run after the INDEX was generated (`receipts/author-r5-index-check.txt`).
  - The files are `gates/workflows/docs__docs-gates-{1,2}__gate_25_{0,1}.log` and `gates/workflows/elaborate__elaborate-gates-{0,1}__gate_15_{0,1}.log`.
  - The archive's `MANIFEST.json` matches every published file (857 of 857, `receipts/manifest-verify.txt`), so the evidence itself is intact.
  - Optional: regenerate INDEX after the scrub.
- **Retained, code unchanged:**
  - R836-1 S2 (D-to-E-to-D hold-off identity, `srp_mbx.c`);
  - R836-1 S3 (admission-swap wire order);
  - R835-1-S1 = R835-2-S3 (hold-off wake-up at 8x8/2if).
- **R835-2-S1 (retained, re-checked against the composition).** This concerns a refused withdrawal's licence window. Under THE TIERS a resumed slice skips the first declarations pass and builds only the MVRP participant (`srp_mbx.c:1236-1260`). Its post-build declarations therefore meet no MSRP frame owed, and the MSRP Leave there is taken. No new path to a refused Leave with `vlan_sent` set appears. The suggestion to state the invariant stands.

---

## The eight focus checks

1. **R836-2's findings.** Each is resolved at this head; see the table below.
2. **Ruling issuecomment-6876349305, applied in order: costs, pace, tx.**
   - `0d2662c0` (item 2) restates the 1x1/1if AECP timer slot from 65 to 75 and the TICK from 45 to 50, in both columns. At 8x8/2if it restates AECP's slot (105 -> 115, donor 110 -> 115), the TICK (40 -> 55, donor 85 kept), `events_none` (30 -> 35) and MAAP's record (150 -> 155). The AECP record is kept at 235 (item 3).
   - `c2622f79` (item 1) moves `AECP_PACE_MS` from 8 to 9 (`aecp_mbx.h:56`).
   - `b3a5ed99` (item 1) moves `CTRL_LOOP_TX_MS` from 30 to 34 (`ctrl_loop.h:366`). Both controls' planted figure moves from 29 to 33 (`flip_grade.py:175`, `rows_tiers.py:934`).
   - `8238156d` (item 4) applies the ROM entry.
   - Each item is applied exactly as ruled. At the stated tables the slice rule takes the built 900 µs (`receipts/graders-head/ruled.log`), but F1 shows that choice rests on an unrestated cost.
3. **Every 1x1/1if row by every source.**
   - Reproduced at the head, byte-for-byte as the PR states (`receipts/graders-head/flip-1x1.log`): R4 12.96, R5 73.46, R6 69.35, first 14.59, last 127.08, R4L 203.48, ACMP 28.85, ADP 27.20, MAAP 27.29, tx 33.20, txL 47.86, each within its bound.
   - The load gate passes at 0.515 at the pin and 0.511 with tsn-c-stack#32 (`load_grade.log`). With every notice the largest legal one it is 0.694. The pass's base is excluded from the load, so F1 does not move it.
4. **The restated costs against their measurements.** Each restated cost is at or above its head measurement by the rule (`receipts/costs-vs-stated.txt`). Two unrestated costs are not: F1 and F2. The AECP record (281.73 µs measured, 235 stated) is the known, ruled case and is not a finding.
5. **The hold-off is derived, not typed.**
   - `SRP_REDECLARE_CS` is `2u*1000u + SRP_JOIN_CS + (CTRL_LOOP_TX_MS+9u)/10u` (`srp_mbx.c:35`), with `SRP_JOIN_CS` equal to `CTRL_LOOP_JOIN_CS` (19). That gives 2,023 cs at one interface and 2,029 at two.
   - `srp_talker.cpp:55` derives `kHoldOffMs` from the same macros: 20,230 and 20,290 ms.
   - The test's assertion is the independent lower bound, `adv >= leave + 20,000` (`:313`, `:348`).
6. **The ROM ledger.**
   - `ctrl_memory.py` sets the platform entry to 60.5 and the refusal to 61.0.
   - In `ctrl_memory_ledger.py`, `OWN`, `HELD`, every `REFUSED` case and the planted ledgers move consistently. The planted ledgers are "entry at 61.0" and "fixture at the platform's 60.5".
   - Docs arithmetic checks: 131,256 B against 133,120 leaves 1,864 B, and 4.5 RAMB36 is 18,432 B.
   - Author receipts: `gates/lane/ctrl_memory.log` (`test_ctrl_memory: 0 failure(s)`, the mapper override at 60.5 and three mutants caught) and the ledger tables in the PR.
   - `test_ctrl_memory.py` was not re-run here (no LiteX/migen in the reviewer environment).
7. **`10cd5472` is behaviour-preserving.**
   - Both versions of `srp_talker_mutants.defects()`, built with a recording builder, give 34 plants, identical tuple for tuple and in order (`receipts/plants-equal-10cd5472.txt`).
   - `build.py` parses to an identical AST, 1,003 -> 1,000 lines (`receipts/build-py-ast-10cd5472.txt`).
   - `srp_gate.hpp` only splits one declaration into three.
8. **The full pass and the sweep (author receipts).**
   - The packet's `MANIFEST.json` verifies 857 of 857 files across author-r3r/r4/r5.
   - The lane gates ran at `62298ab5` on clean clones with 0 changed paths, all rc 0 except the two 8x8/2if flip checks, which are rc 1 by design. `py_idiom` and `cpp_idiom` are within their ratchets.
   - Workflows: `verify-table.md` reports 139 steps ran, 226 not run, each with a reason, and 0 bad.
   - Sweep: 4 shards at the head, 15+17+17+16 = 65 suites, 0 failed, each exit 0. Each shard clone has 0 tracked changes after. `tsn_fuzz` was rerun with the pinned tsn-gen and passes.
   - The CPU budget harness: `legs/summary.txt` shows 0 refusals, 0 `STATED`, and arm A at 7 of 950 and 7 of 994 misses (the ruled held-egress rows). All 1,091 join intervals fall between 185.905 and 190.192 ms, within 181-239.

## Prior findings at this head

| Finding | State | Evidence at `62298ab5` |
|---|---|---|
| R836-2-F1 MINOR (live PR body stale) | **CLOSED** | The live body read back at head `62298ab5`, not draft, equals `author-r5/PR-BODY.md` except one trailing byte. It states REVIEW READY at the head, acceptance 4 by the ruling with the acceptance box unchecked, 34 plants and the current campaign counts. F1 above concerns the costs it reports, not staleness. |
| R836-2-RS1 RESIDUE (introduction scope) | **CLOSED** (superseded) | The round-2 introduction no longer stands. The live round-5 body keeps the analytical tables and the measured legs apart. |
| R835-2-RS1 RESIDUE (`srp_bounds.h` parenthetical) | **CLOSED** | `srp_bounds.h:54` reads the exact fix: "(a join or an adoption refused for storage; a withdrawal it meets after a refused build stays owed)". |
| R835-2-S1 | retained (re-checked) | See SUGGESTIONS. |
| R835-2-S2 | retained | Same four logs in author-r5. |
| R835-2-S3 (= R835-1-S1) | retained | Not taken; the `talker-hold-off-never-ends` plant still covers the row. |
| R835-2-S4 | closed | Nothing was owed. |
| R836-1 S2, S3 | retained | The `srp_mbx.c` delta touches only `SRP_JOIN_CS`, a comment and THE TIERS' `transmit(most)`. |
| Round-1 F2-F5, RS1, RS2 (closed at round 2) | stay **CLOSED** | Not reopened. The F4 and F5 code and tests are unchanged apart from the TIERS merge, and the head's SRP campaign catches the Talker plants at both points (`gates/excerpts/firmware-srp-mutants-step9-tail.txt`, `test_ctrl_firmware: PASS`). |

## Lens results (clean lenses in findings format)

- `[R835] MAJOR Conformance, RTL, Tests, Docs — tb/verilator/ctrl_service_budget/poll_grade.py:87, load_grade.py:184 — F1`
- `[R835] MINOR Conformance, Tests — tb/verilator/ctrl_service_budget/rows_tiers.py:100 — F2`
- `[R835] PASS Robustness — sw/firmware/ctrl/srp/srp_mbx.c:270-340 (refused-withdrawal Leave, licence closed first), :1179 (poll licence rule), :1230-1270 (transmit(most) resume), sw/firmware/ctrl/maap/maap_mbx.c declaring/sid_owed/publish_sid/maap_mbx_start (SRC_SID only while DA_GATE is clear, low word then high from one read, the mark spent at opening), sw/firmware/ctrl/mbx/mbx.c mbx_pub_src_sid (bounds refusal), SrpGate.F905A* (sw/firmware/ctrl/test/srp_gate.hpp:196-300), sw/litex/ctrl_memory_ledger.py REFUSED/planted at 60.5/61.0 — the resumed slice's post-build declarations meet no MSRP frame owed, and no new path reopens a lapsed licence; S1 is optional`
- Conformance, RTL, Tests and Docs were also applied clean apart from F1 and F2:
  - **Conformance:** ruling items 1-4 in order, acceptance 1-3 and 5 regression-held by the 34 plants at both points, every 1x1/1if row and the load reproduced.
  - **RTL:** no HDL in the lane delta (`receipts/pins-and-hdl.txt`), no submodule pin moved, `CTRL_LOOP_TX_MS`/`SRP_REDECLARE_CS` widths and rounding checked.
  - **Tests:** the controls' planted 33, plants identical across `10cd5472`, the hold-off horizon derived.
  - **Docs:** FR_NFR 3.4.1's pace and SRP rows (`FR_NFR.md:383,415`), `ctrl_loop.h`, `aecp_mbx.h` and `load_grade.py` comments, the SRP and platform READMEs, and section 5's ROM arithmetic. No lane label, round, reviewer ID or comment ID appears in any added source comment (`git diff 7398ec0a HEAD` over C/C++/Python).

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1 MAJOR, F2 MINOR) | ruling 6876349305 items 1-4 and triggers; acceptance 1-5 as amended; `aecp_mbx.h:56`, `ctrl_loop.h:366`, `load_grade.py:140-190`, `poll_grade.py:87`, `rows_tiers.py:99-100,709-715,878-884`; flip, pace, tier_grid, load and ruled reproduced; costs receipts against tables | R835-3 | `62298ab5cbfeb7056e4567f70e69d578201c75e0` |
| RTL | UNCLEAN (F1 MAJOR) | lane delta has no HDL; firmware architecture constants (`CTRL_LOOP_SLICE_US` against the slice rule, `CTRL_LOOP_TX_MS`, `AECP_PACE_MS`, `SRP_REDECLARE_CS`); `maap_mbx.c`/`mbx.c` SRC_SID sequencing; `transmit(most)` resume | R835-3 | `62298ab5cbfeb7056e4567f70e69d578201c75e0` |
| Robustness | CLEAN (S1 SUGGESTION) | refused withdrawal under resume; licence rule; SRC_SID mark and wait; ledger refusals | R835-3 | `62298ab5cbfeb7056e4567f70e69d578201c75e0` |
| Tests | UNCLEAN (F1 MAJOR, F2 MINOR) | `srp_talker.cpp:52-55`; `srp_gate.hpp`; `srp_talker_mutants.py` (34 identical); controls at 33; `rows_tiers.py --selftest` at head (971/971) and at the rule base (969/971); legs and sweep receipts | R835-3 | `62298ab5cbfeb7056e4567f70e69d578201c75e0` |
| Docs | UNCLEAN (F1 MAJOR; RS1 RESIDUE; S3) | `SPLIT_CONTROL_MEMORY.md:138-171,270-323,519-529,2409-2441,2532-2557`; `FR_NFR.md:383,415`; plat and SRP READMEs; `ctrl_loop.h`/`aecp_mbx.h`/`load_grade.py` comments; live PR body; REVIEW READY issuecomment-6880958086 | R835-3 | `62298ab5cbfeb7056e4567f70e69d578201c75e0` |

## Real limits

- **Not re-run here:**
  - No firmware build, gtest, mutation campaign, RV32 link (`plat_ledger.py`), harness leg or Verilator suite.
  - `test_ctrl_memory.py` needs LiteX/migen, which this environment lacks. Its result is the author's receipt.
- **What I ran:** the graders were run here on a `git archive` export of the head with the tsn-c-stack and lwSRP submodule exports. They are pure Python and read the tree. The review clone is unchanged: its worktree and index equal HEAD and the gitlinks equal the head's (`receipts/clone-integrity.txt`).
- **F1's measurement** is the author's cost-parser receipt. The parser itself is not in the round-5 packet, and the raw leg logs do not print the heaviest base. The required outcome allows `poll_grade.held`'s own figure to decide it.
- **The evidence archive** commit `689125c2` is unsigned. Integrity rests on its `MANIFEST.json` (857/857 verified) and on the four known INDEX mismatches.
- **No manager source bank at this head** is claimed or inferred. Physical calibration is NOT RUN. Field skips are not hardware proof. Acceptance 6 is not reviewed.
- **Hosted contexts at the exact head,** read-only at review time: `changes`, `bdd-conformance`, `full-ci-gate` and `wire-accountability` succeeded. Physical gPTP is skipped (nightly/manual). The Verilator shards, firmware, docs and elaborate jobs were queued or in progress, and the combined status was pending. These are executed, skipped and pending contexts, not a verdict.

## Pending manager duties

- Route F1 and F2 to the author. If F1's restatement makes the slice rule leave 900 µs, that is the ruling's STOP trigger, and it needs a decision.
- Ask #902 whether its own head measures the same 1x1/1if polls' base.
- Post the #909 note (ruling item 2).
- The exact-head hosted contexts and act.
- The current-dev candidate (source base `cec88385`, live dev `b7d692952305e4e0e132abb8f99c339eeb17a873`) with its builder and native banks.
- Re-sync and recompute when #902 restates the AECP record (KNOWN, not a finding).
- Carry RS1 to the residue checklist.
- #906 and #907 stay pre-existing.

R835-3 FINISHED
