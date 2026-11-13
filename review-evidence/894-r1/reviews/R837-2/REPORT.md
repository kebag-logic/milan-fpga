[R837] NEGATIVE - exact head 8a3791e44533d6b1cc26d486d0b18e7d83470dc1

# R837-2: internal independent review of PR #902 (issue #894), round 7

- **Head:** `8a3791e44533d6b1cc26d486d0b18e7d83470dc1`, tree `3387d98b5f115d86cbb60ac303d5271d697e4584`, detached clean clone.
- **Base:** dev-soft-core `cec88385` (#810), merged into the lane as `ccb47e39`.
- **Delta judged:** the round-1 head `12180198` to this head. The PR's own diff is `cec88385..8a3791e4`, 82 files. Round 7's 20 commits on `ccb47e39` were read line by line.
- **Authority read:** AGENTS.md and the #894 issue body, then the rulings in the order given:
  - the delegated decisions 6813855717, 6814835849, 6839847820 and 6840564634;
  - the owner question 6843318273, the ruling on it 6844175391 and its confirmation 6844947317;
  - the round rulings 6845846512, 6848507008 and 6857835707;
  - Step 0 (6857903645), the contingent ruling 6858269025 and its amendment 6862465874;
  - REVIEW READY 6867318907.
- **Evidence read:** the author packet `review-evidence/894-r1/author-r7` (archives `123ee8af`, `6f321a99`).
- **Prior findings:** read only after my own pass over the diff.

## Verdict

**NEGATIVE.** One MAJOR and two MINOR findings are open.

- **R837-2-1 (MAJOR).** The MRPDU bound is 240 ms less the armed join time, 50 ms. That leaves no room for the 1 ms egress allowance that FR_NFR 3.4.1 puts inside every normative timer bound. Counted, txL (49.99 ms) is over the 49 ms that remains. The requirement and the rulings conflict, and a decision must be recorded.
- **R837-2-2 (MINOR).** THE PACE's count of edits in a window, `1 + floor(w / P)`, is not what the firmware's whole-millisecond gate guarantees, which is `ceil((w + 1) / P)`.
  - The figure at this head does not change: txL is 49.99 ms under either count, and 6 ms is still the smallest pace.
  - The rule is still unsound. It undercounts at P = 4, 8, 9 and 11, and the ruling requires occurrence bounds proven from the firmware.
- **R837-2-3 (MINOR).** Round 7's moves left stale figures in authoritative documents and one source comment. This includes a regression of round 1's MAILBOX_SPLIT slice finding.

**Verified and holding:**
- The 1x1/1if flip check, rerun here: every row within its bound.
- The +5 % rule on every txL term I traced.
- #908's levers a and b.
- The O(n) rewrite of the map commands for #904.
- THE PACE: edits are held, never dropped, and R4L is 158.34 ms against 240.
- The 725 us build-of-one restatement.
- The join-interval gate and its plants.
- The ROM ledger, the 1x1/1if load and the firmware suite.
- Every round-1 finding except R837-1-3, which has regressed (see R837-2-3).

## Checks of the round's focus items

| Item | Result | Evidence |
|---|---|---|
| Every 1x1/1if row by every source within its bound | **Holds at the stated costs.** R4 12.82/20, R4L 158.34/240, ACMP 28.35/30, ADP 26.76/30, MAAP 26.88/30, first 14.50/20, R5 72.71/90, R6 68.62/90, last 125.84/130, tx 29.78/50, txL 49.99/50 | `receipts/flip_grade.py_--check_--point_1x1_1if.txt` (my own run, exit 0); `flip_grade.py --selftest` 555 of 555 refused; `rows_tiers.py --selftest` 969 of 969 refused |
| txL's terms, each its most measured value plus 5 % | **Holds for every term traced.** Each is ceil5(measured × 1.05) or above it: ACMP send 4,744 cycles → 50 us; a declined offer 1,589 → 20; the largest notice 34,359 → 365; the largest record 89,126 → 940; a build of one 68,951 → 725; datapath 31.96/29.06/23.33 us → 35/35/25. The polls' base at `ccb47e39` is 18,881 cycles at most, and 1.05 times that is 198.3 us, under the stated 205 | `poll_grade.py:67-90`, `rows_tiers.py:94-131`; packet `receipts/harness/m1-backlog-owed.txt`, `receipts/attribution/base-kinds-variants.txt` (V0), `receipts/gates/harness-head-builds.txt` (H-J1 build 68,951); `receipts/rows_tiers_terms_1x1.txt` |
| #908 lever a (ACMP's item itemised) | **Holds.** Model-only: no firmware file outside the tests changed in round 7 (`git diff --stat ccb47e39..HEAD -- sw/firmware/ctrl/acmp …` is empty). The occurrence bound of two declines a send and one is a valid upper bound, and the plant is caught (316 declines against a bound of 25). A tighter bound is available (S1) | `acmp_mbx.c:107-187`; packet `receipts/harness/control-acmp-redelivered-every-poll.txt` |
| #908 lever b (the polls' base attributed) | **Holds.** The register read is 2 cycles (V0 18,881 against V1 18,879). The hot list is 203 (against V2 18,678). The rest is 4,389 (against V3 14,287), consistent with about 4,400 | packet `receipts/attribution/base-kinds-variants.txt`, `memory-latency.txt` |
| #908 lever c (placements) | **Reverted, none taken.** `ctrl_split.ld` and `ctrl_plat` are equal to `ccb47e39`. Existing AECP and loop tests are unchanged in round 7 (`git diff ccb47e39..HEAD -- test_aecp.cpp test_port_loop.cpp` is empty) | `git diff --stat ccb47e39..HEAD -- sw/firmware/ctrl/plat` (empty) |
| #904's O(n) map-command rewrite is behaviour-neutral | **Holds on reading.** Old and new code are equivalent check by check: the topology read in turn; an earlier conflict for ADD; the port's own rows (FOUND, BARRED); other output owners for both commands; repeat counting; NO_RESOURCES; REMOVE taking the first equal rows one per occurrence. The 4,000-edit test's oracle is an independent restatement of the definition (`test_aecp.cpp:2471-2575`), and 16 mutants plant the rewrite and THE PACE (`aecp_map_mutants.py`) | `aecp_maps.c:75-219`, `:264-388` against `cec88385`'s; the firmware suite passes here (`receipts/fw_unit.txt`) |
| THE PACE through AECP's rx-ready gate, held never dropped; R4L within 240 ms | **Holds.** The gate is in the ready callback (`aecp_mbx.c:154-158`), so the record stays in its ring. The edit is stamped at its take (`aecp.c:424`, `aecp_maps.c:331`). It is open from boot (`aecp_mbx.c:142`). R4L is 158.34 ms, of which the pace is 150.000 = 15 × (6 + 2 × 2). The count rule for txL is R837-2-2 | `paced_rows.py:44-77`; `receipts/pace_truncation_probe.txt` |
| The 725 us build of one, from the srp group's measurement | **Holds.** 68,951 cycles × 1.05 = 724.0 → 725 us. The static check holds: 725 ≤ 900 (`ctrl_loop.c:201-202`). `item.mrpdu` follows at 725 in both tables. At 8x8/2if, 147,613 → 1,550 us, over the 1,300 us slice: reported, refuted, stated at 1,215 | `ctrl_loop.h:309-322`; `poll_grade.py:89`; `load_grade.py:169`; packet H-J1, H-J8 |
| The join-interval gate (52 intervals, 185.7-190.0 ms) and its planted defect | **Holds.** The harness self-test passes here with 0 failures and 239 mutants caught, the five join checks and the earlier rule's plant among them. The 52 intervals come from 14 runs, one of which is the planted control C-R1; without it there are 49 in 13 runs (R837-2-5). The range is 185.668 (H-J8) to 190.025 ms (H-L1A, H-L1L, H-L1O, H-J1) | `receipts/harness_selftest_summary.txt`; packet `receipts/gates/harness-head-builds.txt` |
| The ROM ledger | **Holds.** 8x8/2if fixture 59.0, ledgered 59.0 by 6844175391's fallback. 8x8/2if platform 60.0 ≤ 60.5. Every other point ≤ 56: 8x8/1if platform 56.0, 1x1/1if fixture 40.5 and platform 42.5 | `ctrl_memory.py:243-262`, `ctrl_memory_ledger.py:32-76`; packet `receipts/images/every-image-final.txt` (at `11c586a8`; no firmware source outside the tests changed after it) |
| The 1x1/1if load at most 0.70 | **Holds:** 0.513 at the pin and 0.509 with tsn-c-stack#32 | `receipts/load_grade.py_--check.txt` (my own run, exit 0) |
| The slice, the pace and the queued bound are the rules' own | **Hold.** `slice_choice` gives 900 us (least margin +0.0002), `ruled` 900; the pace choice is 6; the queued bound has no statements and 0 controls escaped | `receipts/slice_pace_queued_at_head.txt` |
| Every FR_NFR 3.4.1 amendment cites its ruling | **Mostly.** The 30 ms rows cite the owner question 6843318273, not the ruling 6844175391 or its confirmation 6844947317 (part of R837-2-3) | `FR_NFR.md:373-390` |
| 8x8/1if reported, not held; 8x8/2if's 1,550 us build reported | **As stated.** The 8x8-1if legs exit 1 (H-81L, H-81A, H-81N, H-J81). H-J8 exits 1 on the refuted build | packet `receipts/gates/unit-rcs.txt`, `harness-head-builds.txt` |

## Findings

### R837-2-1 MAJOR - Conformance, Docs - the 50 ms MRPDU bound leaves no room for FR_NFR's egress allowance inside the 240 ms JoinTime ceiling

**Artifacts**
- `sw/firmware/ctrl/loop/ctrl_loop.h:334-348`: `CTRL_LOOP_TX_BOUND_MS (240u - 10u * CTRL_LOOP_JOIN_CS)`, "from the centisecond that owes an MRPDU to its commit".
- `tb/verilator/ctrl_service_budget/rows_tiers.py:106` (`TX_BUDGET_MS`).
- `docs/reference/FR_NFR.md:424-426`:
  - line 424: "Normative timer bounds include service and egress effects where applicable";
  - line 425: "at the split's 190 ms (above), 50 ms";
  - line 426: "The SRP bound, 20 ms, and the 1 ms egress allowance below take 21 ms of that slack and leave 19 ms".
- `FR_NFR.md:441-450`: `T_egress`, 1 ms, from a record's commit to the wire.

**Evidence**
- lwSRP arms the join timer at a commit, and the timer runs out at most 190 ms later (19 centiseconds).
- THE TRANSMIT's MRPDU is then committed within txL, 49.99 ms by every source.
- `T_egress` then allows up to 1 ms more before the frame leaves.
- So a participant's join interval on the wire can reach 190 + 49.99 + 1 ≈ 241 ms. That is past Milan v1.2 Table 4.3's 240 ms maximum.
- The contingent ruling 6858269025, item 4, holds the bench capture to that maximum on the wire.
- Line 426 is the requirement's own accounting of that slack. It was written for the 20 ms bound and was not restated when line 425 was (`158265c2`).
- The rulings derive the bound as "240 minus the armed value" (6858269025 item 3; at 20 cs, 6844175391's 40 ms) without addressing `T_egress`.
- The harness's join gate measures commit to commit (`join_grade.py:3-12`), so it cannot see egress.
- If egress is counted, the MRPDU bound at 19 cs is 49 ms, and txL (49.99 ms) fails it. Under the contingent ruling, that case goes back to the owner.

**Impact:** the 1x1/1if flip passes under a bound that the requirement's own rule makes 1 ms too generous. A worst-case join interval on the wire can exceed Table 4.3's maximum, which the ruling's wire check is meant to refuse.

**Required outcome:** under AGENTS.md section 2, the conflict between FR_NFR 3.4.1's egress rule and the rulings' derivation is published and decided. Either:
- the MRPDU rows' bound counts `T_egress`, derived in code from the armed value and the allowance, with the consequence for txL handled as the contingent ruling directs; or
- a ruling states that the bound is commit-side only, with its basis, and FR_NFR 3.4.1 lines 424-426 and the srp README state that exclusion.

In both cases line 426 states the split's figures.

**Verification:**
- The ruling's link is in FR_NFR 3.4.1.
- `grep -n "leave 19 ms" docs/reference/FR_NFR.md` no longer states the 20 ms bound for the split.
- `flip_grade.py --check --point 1x1/1if` is re-run against the decided bound.

### R837-2-2 MINOR - Conformance, Tests - THE PACE's count of edits in txL's window is not the firmware's whole-millisecond bound

**Artifacts**
- `tb/verilator/ctrl_service_budget/paced_rows.py:6-9`, `:44-51` (`record`): "in a window of w ms at most 1 + floor(w / P) of AECP's arrivals are edits".
- `sw/firmware/ctrl/aecp/aecp_mbx.c:154-158`: `ready` compares `core.now - core.edited_ms >= AECP_PACE_MS`, both reads of the 1 ms `MBX_REG_NOW_MS`.
- `aecp_maps.c:331` stamps `edited_ms` with the millisecond in which `aecp_rx` took the record (`aecp.c:424`).

**Evidence**
- The gate guarantees floor(t[k+1]) ≥ floor(t[k]) + P, not t[k+1] ≥ t[k] + P. Two edits can be taken just over P − 1 ms apart, and N edits span more than P(N − 1) − 1 ms.
- A window of w ms therefore holds up to ceil((w + 1) / P) edits. That count differs from the model's wherever w mod P is over P − 1.
- Reviewer probe `scripts/pace_truncation_probe.py`, `receipts/pace_truncation_probe.txt`: it patches only `paced_rows.record` in memory.
  - At this head's P = 6, txL is 49.99 ms under both counts, and 5 ms still fails (57.01). The gate's result and the chosen pace are unchanged.
  - The model undercounts txL at P = 4 (59.91 against 66.50), 8 (47.03 against 47.73), 9 (44.96 against 47.03) and 11 (43.40 against 44.96).
- Ruling 6857835707 item 4 requires that each itemised occurrence bound be proven from the firmware.
- `paced_rows.controls` plants no window with w mod P over P − 1.

**Impact:** with a margin of 0.01 ms, the gate's proof of txL rests on a rule the firmware does not guarantee. The rule happens to give the right count at this head's window. A later cost or pace change can pass a txL that the firmware exceeds.

**Required outcome:**
- The model counts the edits the firmware's gate allows: ceil((w + 1) / P), or another bound derived from the gate's arithmetic and stated with it.
- Alternatively, the gate guarantees a real P ms between takes.
- A control plants the earlier rule at a window where the counts differ.
- FR_NFR 3.4.1 (line 383) and `aecp_mbx.h:38-47` state the bound as proven.

**Verification:**
- `flip_grade.py --check --point 1x1/1if` and `rows_tiers.py --selftest` pass.
- The new control is refused.
- The probe's two columns agree for every P.

### R837-2-3 MINOR - Docs - stale figures after round 7's moves, and one amendment citing the question rather than its ruling

**Artifacts**
- `docs/reference/FR_NFR.md:415` (SRP/MRP row, third and fourth columns) still states:
  - "an MRPDU a timer owes 40 ms ... JoinTime's 200 ms plus it within Table 4.3's 240 ms";
  - "at 1x1/1if it is committed within 40 ms of the centisecond";
  - "960 to 1040 ms, and 9.97 to 15.03 s".

  The tree holds 50 ms after a 190 ms join timer, and `ctrl_loop.h:343-346` states ±50 ms. The 3.4.1 prose at line 381 says 50, so the requirement contradicts itself.
- `docs/design/MAILBOX_SPLIT.md:390`: "slice from the pass's start (0.8 ms at one interface, 1.3 ms at two)". The tree's slice is 900 us (`ctrl_loop.h:276`, `dec9f1d7`).
  - This is a regression of R837-1-3 and R838-1 F5, which were fixed at the 800 us value.
- `sw/firmware/ctrl/loop/ctrl_loop.h:205-208` (THE TIERS): "the last queued notice at 125 ms (#665, decision D)". At 1x1/1if it is 130 ms (`aecp_mbx.h:64`).
- `docs/design/SPLIT_CONTROL_MEMORY.md:2457` ("What is left"): "at 1x1/1if R4 by every source is 74.83 ms against tier 1's 20 ms, a finding for the flip and #894's".
  - The text is inherited from the base, but this PR's tiers make it false: R4 is 12.82 ms.
- `docs/reference/FR_NFR.md:374` and `docs/design/SPLIT_CONTROL_MEMORY.md:2355`: "the [owner's decision of 2026-11-13](…#issuecomment-6843318273), option A".
  - 6843318273 is the owner question.
  - The decision is the delegated ruling 6844175391, confirmed by the owner in 6844947317.

**Impact:**
- The authoritative requirement and design documents state bounds and a slice that the tree does not hold.
- One FR_NFR 3.4.1 amendment cites the question it was answering, not the ruling.

**Required outcome:**
- Each listed line states the tree's value: 50 ms after 190 ms with its ±50 ms periodic and LeaveAll spans; 0.9 ms; 130 ms at 1x1/1if; R4 12.82 ms, or the bullet marked as the state before #894.
- The two 30 ms citations link to 6844175391, with 6844947317 optional.

**Verification:**
- A grep of each line.
- The docs gates (`docs_check`, the em-dash and idiom gates) pass.

### R837-2-4 RESIDUE - Docs - new issue-comment IDs in source comments (owner rule 2026-10-15)

**Artifact:** `receipts/comment_rule_new_ids.txt`, 15 lines this PR adds:
- `aecp_mbx.h:44` and `:58`;
- `ctrl_loop.h:265` and `:330`;
- `ctrl_memory.py:260` (a ledger note string);
- `flip_grade.py:174`, `join_grade.py:3`, `load_grade.py:235`, `notice_window.py:61`, `queued_bound.py:3-4`, `rows_tiers.py:106`, `run.py:184`, `selftest_notice.py:88`, `selftest_polls.py:242`, `tier1_rows.py:179`.

`ctrl_memory.py:253` is existing text, tracked by #746.

**Exact fix:** replace each `issuecomment-NNN` with the ruling's name and date, for example:
- "#894's contingent ruling of 2026-11-13, item 3";
- "#894's amendment of 2026-11-13 to its contingent ruling, item 2";
- "#894's ruling of 2026-11-13 on the tier-1 rows, item 2".

No code, figure or claim changes. `selftest_notice.py:88` is a check's message string, so its output text changes with it.

### R837-2-5 RESIDUE - Docs - REVIEW READY's interval count includes a planted run; the packet's "final" model receipt is pre-restatement

**Artifacts**
- #894 issuecomment-6867318907: "52 intervals in 14 group runs over 1x1, 8x8 and 8x8-1if".
  - One of the 14 is the planted control C-R1 (`--mutation acmp-redelivered-every-poll`, 3 intervals).
  - The unplanted legs give 49 intervals in 13 runs, with the same range.
- Packet `receipts/model/rows-1x1-final.txt`: rows at `2953091e` (last 117.19, txL 49.70), before the 725 us restatement. The final rows are in `receipts/gates/lane-flip_check_1x1.txt`.

**Exact fix:** in the next public comment, say "49 intervals in 13 unplanted group runs (52 with the planted control's)". Name the model receipt "rows at 2953091e, before the build-of-one restatement".

### Suggestions (optional)

- **S1 - Tests - a tighter ACMP decline bound.** `redeliver` returns at its first decline (`acmp_mbx.c:157-175`), and `on_rx_ready` keeps the loop from offering while a command is kept (`:122-128`). So the firmware allows at most one decline a send, plus one, against the model's two a send and one (`rows_grade.acmp_items`). In txL the term is 0.980 ms (49 declines). The tighter bound proven from the same lines would return about 0.48 ms to txL's 0.01 ms margin.
- **S2 - Docs - the packet index.** `INDEX.md` lists five files that are not published (the four ruling copies and `STOP-COMMENT.md`), and `scripts/collect.sh` and `scripts/index.py` differ from their indexed bytes (`receipts/packet_index_check.txt`; 118 rows match). Regenerate the index from what is published, so a cold reviewer can check every row.
- **S3 - Tests - the join gate's sample.** Each 1x1 group run sees three join intervals. A longer group, or one that stresses tier 1 across many join run-outs, would make the harness side of item 4 stronger while the bench capture is owed.
- **R837-1-8 (round 1) - the behave layer is an offline model.** Not re-checked; it remains optional.

## Prior findings at this head

| Finding | Status at `8a3791e4` | Evidence |
|---|---|---|
| R837-1-1 MAJOR: R4 did not count notices longer than a slot | **Resolved.** Each slot holds the largest legal AECPDU (`AECP_OWED_BYTES 552u`, `aecp.h:257`). R4L counts every command as the largest legal one, and txL every notice; both are held by the flip check | rulings 6840564634 item 2, 6844175391; `rows_tiers.py:118-131`; `receipts/flip_grade.py_--check_--point_1x1_1if.txt` |
| R837-1-2 MAJOR: the MRPDU over 20 ms, the requirement "an open decision" | **Resolved by ruling.** The compile-time check is restored at 1x1/1if (`ctrl_loop.c:203-204`); the bound is the MRP budget's (40 ms, now 50 ms at 19 cs); "open decision" is gone from FR_NFR. The egress gap in that derivation is new: R837-2-1 | rulings 6840564634 item 1, 6844175391, 6858269025 item 3 |
| R837-1-3 MINOR: MAILBOX_SPLIT's slice figure | **Regressed:** fixed at 0.8 ms, stale at 0.9 ms (R837-2-3) | `MAILBOX_SPLIT.md:390` |
| R837-1-4 MINOR: "an owner question" on decided 8x8/2if rows | **Resolved:** no match in the six artifacts | `grep -n "owner question"` over them |
| R837-1-5 MINOR: the Domain adoption claim where a slice makes one MRPDU | **Resolved:** both cases are stated, and a test runs a poll between the slices | `srp/README.md:239-240`, `srp_mbx.c:1095-1098`, `srp_mbx.cpp:1598` |
| R837-1-6 RESIDUE: review-round identifiers in source | **Resolved:** no "round 23" in source. A different identifier class is new (R837-2-4) | grep of `sw/firmware/ctrl` and `tb/verilator/ctrl_service_budget` |
| R837-1-7 SUGGESTION: `least_margin` ranked unsolved rows above solved ones | **Resolved:** an unsolved row is −1 | `rows_tiers.py:686-691` |
| R838-1 F1 MAJOR: other tier-1 channels' rows | **Resolved:** ACMP, ADP and MAAP last-record rows held at 30 ms | ruling 6844175391; `tier1_rows.py`; flip receipt |
| R838-1 F2 MAJOR: the MRPDU bound held by measurement alone | **Resolved:** compile-time check and model rows tx and txL (see R837-2-1) | `ctrl_loop.c:203`; `rows_tiers.py` |
| R838-1 F3 MINOR: no test of the poll reporting a longer notice still owed | **Resolved** (`6f3c5353`: test and mutant) | `test_aecp.cpp`, `aecp_owed_mutants.py` |
| R838-1 F4 MINOR: `round_one` kept from a pass given whole | **Resolved** (`59ef9b46`: test and mutant) | `test_port_loop.cpp`, `loop_step_mutants.py` |
| R838-1 F5 MINOR: MAILBOX_SPLIT slice | **Regressed** (as R837-1-3) | R837-2-3 |
| R838-1 F6 MINOR: the order of the other tier-1 channels | **Resolved** | `MAILBOX_SPLIT.md:385-389` against `ctrl_loop.c:291-305` |
| R838-1 F7 MINOR: the SRP Domain claim at one MRPDU a slice | **Resolved** (as R837-1-5) | as above |
| R838-1 RS1 RESIDUE: review rounds in source comments | **Resolved** (as R837-1-6) | as above |

## Reviewer-owned completion ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (R837-2-1, R837-2-2) | The #894 acceptance and every ruling listed above. FR_NFR.md 3.4.1 (`:365-450`). `ctrl_loop.h:253-360` (`CTRL_LOOP_JOIN_CS`, `CTRL_LOOP_TX_BOUND_MS`, slice, build costs) against Milan v1.2 4.2.7.1.1 Table 4.3 and IEEE 802.1Q-2018 10.7.11. `aecp_mbx.h:38-64`, `aecp_mbx.c:142-158` (THE PACE) against IEEE 1722.1-2021 9.3.2.6. `aecp_maps.c:75-388` against 1722.1-2021 7.4.45/7.4.46 and Milan 5.4.2.27/28. `queued_bound.py`, `join_grade.py`, `paced_rows.py`; my flip, load and probe receipts | R837-2 | 8a3791e44533d6b1cc26d486d0b18e7d83470dc1 |
| RTL | CLEAN | No HDL in `cec88385..8a3791e4`. `ctrl_loop.c:162-336`: tiers, slices, `rx_left`, `holds`, `round_of`, `slice_end`; round 7 changes only constants. Static checks `ctrl_loop.c:199-204`: 900 ≤ SHARE − margin, 725 and 250 ≤ 900, TX_MS 30 ≤ 50 at one interface. `CTRL_LOOP_BUILD_MOST` is 1 at 900 < 1,010. `aecp_maps.c` `struct edit` sizes and the `MAP_SLOTS` table (fewer than 256 held, so every walk ends; `uint8_t` copies ≤ 63). The pace gate's `uint32_t` wrap arithmetic (`aecp_mbx.c:157`). `acmp_mbx.c:107-187`. `srp_mbx.c:27-30`. Round 1's RTL finding is resolved | R837-2 | 8a3791e44533d6b1cc26d486d0b18e7d83470dc1 |
| Robustness | CLEAN | Map edits with repeats, conflicts, other owners, a running stream, NO_RESOURCES and illegal mappings (the 4,000-edit oracle, `test_aecp.cpp:2471-2575`). A refused edit before its checks paces nothing (`pace-a-refused-edit`); the pace is open at boot. A held record stays in its ring (rx-ready). The kept ACMP command's decline bound (`acmp_mbx.c:107-187`). Every slice overrun at 8x8/1if and 8x8/2if is reported by the harness (H-81*, H-J8, rc 1) and documented, not hidden. Integer-ms boundaries of the pace (the model side is R837-2-2, Conformance and Tests). The images within their caps at every point | R837-2 | 8a3791e44533d6b1cc26d486d0b18e7d83470dc1 |
| Tests | UNCLEAN (R837-2-2) | My runs at the head: the firmware suite (`receipts/fw_unit.txt`, PASS), the harness self-test (0 failures, 239 mutants caught, 0 escaped), `flip_grade --selftest` 555/555, `rows_tiers --selftest` 969/969, `queued_bound.controls` 0 escaped. Read: `aecp_map_mutants.py`, `selftest_polls.py` join checks, the SRP tests' JoinTime derivation (`srp_mbx.cpp:291-307`, `:733-748`, `:1523-1530`, `:1697-1705`; `srp_latency.cpp:85-91`; `srp_rx_retry.cpp:383-389`; `srp_walk.cpp:71-90`), none weakened. The author's mutation campaign receipts (W-fw-control, W-fw-aecp, W-fw-srp, rc 0) | R837-2 | 8a3791e44533d6b1cc26d486d0b18e7d83470dc1 |
| Docs | UNCLEAN (R837-2-1, R837-2-3; RESIDUE R837-2-4, R837-2-5) | FR_NFR.md 3.4.1 (`:365-450`, the SRP row `:415`). SPLIT_CONTROL_MEMORY section 13 (`:2355-2368`, "The contingent moves" `:2432-2442`, "What is left" `:2444-2460`). MAILBOX_SPLIT.md `:380-394`. `aecp/README.md`, `srp/README.md:230-245`, `ctrl_service_budget/README.md:170-190`. `ctrl_loop.h` and `aecp_mbx.h` comments. The PR body at the head, REVIEW READY 6867318907, the packet INDEX | R837-2 | 8a3791e44533d6b1cc26d486d0b18e7d83470dc1 |

## Real limits

- **The CPU budget harness legs were not re-run.** They need the split SoC build. Every measured cost and every harness leg exit here is the author's published receipt at this head (`receipts/gates/harness-head-builds.txt`, `unit-rcs.txt`).
  - I checked those receipts against the stated costs and the +5 % rule, but I did not falsify them by a fresh measurement.
  - The polls' base at the head itself is not in the packet; the margin check uses `ccb47e39`'s V0, and firmware code is unchanged since then.
- **The firmware mutation campaigns** (control, AECP, SRP) were not re-run; I rely on the author's receipts. I ran the firmware suite without `--self-test`.
- **Hosted CI** does not run on split PRs. I inspected no hosted context, and no manager source bank exists at this head.
- **No hardware or bench.** Physical calibration was NOT RUN, and the join-interval wire capture is not made. Field skips are not hardware proof.
- **8x8/1if and 8x8/2if** rows by every source were read from the receipts only, as the round reports them.

## Pending manager duties

- Obtain and record the decision R837-2-1 asks for: whether the MRPDU bound counts `T_egress`, and if so what happens to txL.
- The flip check's bench capture of join intervals on the wire (ruling 6858269025 item 4) is owed and needs bench access.
- 8x8/2if's build of one is refuted (1,550 us against the stated 1,215, over its 1,300 us slice). This needs an owner decision and a new Issue.
- 8x8/1if's per-point slice (the STOP) needs a decision.
- Validate the current-dev merge candidate at the merge turn (source base `66f71326`, live dev `b7d69295`), with the builder and native banks.
- The PR body says "Relates to #894". The Issue's closure and move to Done are by hand, or the body needs `Closes #894` before merge.
- Carry R837-2-4 and R837-2-5 to the residue checklist.
- #908 stays open under its own terms: last notice ≤ 125 ms and txL ≤ 40 ms at 20 cs.

## Packet

- `REPORT.md` (this file).
- `MANIFEST.sha256` lists every publishable receipt and script.
- `scripts/pace_truncation_probe.py`: portable, `python3 -I pace_truncation_probe.py TREE`; it reads the tree and patches the model in memory only.
- `receipts/`: my own runs at the head (flip check and self-tests, load, the txL terms, slice, pace and queued rules, the firmware suite, the harness self-test summary, the probe), the packet index check, the comment-rule scan, and the restore check.
  - The clone is byte-exact after the probes: worktree and index equal HEAD, no untracked or ignored paths, every submodule gitlink and checkout at its recorded commit with nothing changed.

R837-2 FINISHED
