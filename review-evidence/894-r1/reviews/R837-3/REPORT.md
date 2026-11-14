[R837] NEGATIVE - exact head dd01b0afef87037ec485cd49b40a26b542854bdd

# R837-3: internal independent delta review of PR #902 (issue #894), round 8

Head `dd01b0afef87037ec485cd49b40a26b542854bdd`, tree `4d7787fe81c9a90177d98e1afff98f216cb3b140`. The delta is the 9 commits from round 7's `8a3791e4` (`8ba93f26` .. `dd01b0af`; 29 files, +745/-251). Authority: the round-8 ruling, #894 issuecomment-6867990126 (items 1 to 6 and its STOP triggers), building on 6858269025, 6862465874 and 6867393730. Evidence: the author packet `review-evidence/894-r1/author-r8` at `183cd03d` and REVIEW READY 6870102413. All five lenses were applied. Prior findings were read only after my own pass over the diff.

## Verdict

**NEGATIVE.** Two MINOR findings are open:

- **R837-3-1 (MINOR; RTL, Robustness, Tests, Docs).** The map table's linear-work bound rests on a hash precondition. The code says that precondition holds "as every configuration has", but it holds only for the five checked-in configurations. The builder admits geometries where legal keys share slots. There, the real firmware does 935 slot visits for an accepted 63-mapping ADD, against the 126 the stated bound allows. Nothing checks the precondition at build time.
- **R837-3-2 (MINOR; Docs).** Four statements in the harness README and the design doc still give the pre-ruling values: R4L's paced bound as 240 ms, the pace rule without its R4L condition, and stale load figures.

Everything else the ruling asked for is met at this head, and I reproduced the parts that carry figures:

- the egress allowance is derived in code (49, 238, and 181.0 to 239.0);
- the pace count matches the whole-millisecond gate;
- P = 7 holds;
- the join grader has no horizon;
- the map rewrite does not change behaviour;
- the 975 µs record is restated;
- no STOP trigger fires.

Every MAJOR from round 7 (R837-2-1, R838-2-F1, R838-2-F2) is resolved at its cause for the shipped configurations. R838-2-F2's cause survives only in the builder-admitted geometries of R837-3-1, at reduced severity.

## STOP triggers (ruling 6867990126)

| Trigger | Result at this head | Evidence |
|---|---|---|
| No P up to 11 holds txL ≤ 49 with R4L ≤ 238 | **Not hit.** P = 7 holds: txL 47.98, R4L 173.37. `paced_rows.choice` returns 7, and the header states 7. | `receipts/flip_check_1x1.txt`, `receipts/pace_choice.txt`; packet `receipts/model/pace-table-P1-13.txt` |
| Last queued notice over 140 ms | **Not hit.** It is 125.84 ms, within its 130 ms bound. | `receipts/flip_check_1x1.txt` |
| An image over its cap | **Not hit.** Every image grows by +176 B of rom with no tile change. 8x8/1if platform is 56.0 of 56 (129,208 of 131,072 B). The 1x1/1if fixture is 110,584 of 110,592 B. | packet `receipts/images/every-image-final.txt` |
| A map-command behaviour change | **Not hit.** See item 3 below. The definition test is byte-unchanged and passes. All 10 `Core.*Map*` tests pass, plain and under ASan. | `receipts/aecp_core_maps.txt`, `receipts/aecp_core_maps_asan.txt` |
| The collision case's pass over THE SHARE at 1x1/1if | **Not hit.** 0 of 103 work passes are over 200,000 cycles in the 1x1 `aecp-largest-notice` leg. | packet `receipts/gates/harness-head-builds.txt` (H-L1L) |

## What I checked, per ruling item

1. **Egress counted.**
   - `ctrl_loop.h:342-343` defines `CTRL_LOOP_T_INGRESS_MS` and `CTRL_LOOP_T_EGRESS_MS` (1 each).
   - `ctrl_loop.h:360` defines `CTRL_LOOP_TX_BOUND_MS (240u - 10u * CTRL_LOOP_JOIN_CS - CTRL_LOOP_T_EGRESS_MS)` = 49.
   - `paced_rows.py:43-44` derives `PACED_BOUNDS` = 238.
   - `join_grade.py:27-33` derives 181.0 to 239.0 and keeps the wire range at 180.0 to 240.0.
   - `mrpdu_grade.py:35` derives `LATE_MS` = 49 from the same header.
   - My run at the head prints `PACED_BOUNDS {'R4L': 238} TX_BUDGET_MS 49 LATE_MS 49 join 181.0 239.0` (`receipts/pace_choice.txt`).
   - The egress-free derivation is planted and refused (`rows_tiers.py:937-940`; rows_tiers self-test 971/971, `receipts/rows_tiers_selftest.txt`).
   - FR_NFR 3.4.1 states the split's figures at `FR_NFR.md:373`, `:381`, `:383`, `:415` (49 ms; 950 to 1050 ms; 9.96 to 15.04 s; 281 ms) and `:424-426`.
2. **The pace count.**
   - `paced_rows.edits` (`:54`) = ceil((w + 1) / P).
   - I traced the gate: `aecp_mbx.c:155-158` reads `core.now`, the latest `now()` read (`aecp.c:31-38`). The stamp is that read as the record is taken (`aecp_maps.c:347`). So floor(t[k+1]) ≥ floor(t[k]) + P.
   - My own gate simulation (`scripts/gate_probe.py`) has a sub-ms phase sweep and edits always waiting. It agrees with `edits()` at all 156,000 window×pace points (0.01 to 120 ms, P 1 to 13). The old rule undercounts at 37,620 of them (`receipts/gate_probe.txt`).
   - `flip_grade` now includes `count_findings` in its row findings. The flip self-test refuses 555 of 555 plants (`receipts/flip_selftest.txt`).
3. **Map commands.** I read `aecp_maps.c:86-417` against the version at `8a3791e4`.
   - Every refusal path still returns BAD_ARGUMENTS. NO_RESOURCES and SUCCESS are reached only when every turn passes.
   - An ILLEGAL mapping now ends the table at its own turn. Before, it was refused at that same turn by `topology()`. Earlier turns read their port (`idle()`) in the same order. `legal()` reads descriptors only.
   - A REMOVE's differing values are chained at the key's first entry. Equal values of a non-first value become separate chain entries, but `look()` marks every equal entry `match` and removes through the first entry with copies left. So the number of rows removed per value, and their order, are unchanged.
   - BARRED and FOUND marking is equivalent.
   - `memset` covers `slot`, `next`, `rep`, `flags` and `copies`. `next` holds index + 1 ≤ 176 < 256, and `AECP_MAP_PAGE` (176) < `MAP_SLOTS` (256) is statically asserted, so `place()` terminates.
   - My work-arm run reproduces the author's 24 MAP WORK lines exactly: the 63-mapping collision costs 127 visits against a bound of 128 (`receipts/aecp_work.txt`).
   - The 21 map plants are listed as caught in the packet's `receipts/item3/map-plants.txt`.
   - The collision and conflict edits are in `aecp-largest-notice` (`long_notice.py:48-90,123-130`).
   - The record: 92,766 × 1.05 = 974.0 µs, rounded up to 975 (packet `receipts/model/measured-inputs-final-pass.txt`).
   - **The stated limitation (hash precondition): see R837-3-1.**
4. **The join grader.**
   - `mrpdu_grade.resolve` (`:79-111`) has no horizon. Its outcomes are released, empty, late (> 49 ms after the run-out), absent (no build, and the log runs past 49 ms) and unresolved. Late and absent fail the run (`run.py:170-178`).
   - My run of all 822 harness self-test checks at the head passes, the eight join checks among them. All 13 `joins:` mutants are caught, including the earlier 100 ms horizon rule, the T_egress-free range and the owed-frame plant (`receipts/join_mutants.txt`).
   - The head legs (packet `harness-head-builds.txt`) total 57 intervals over 14 group runs, 185.468 to 190.059 ms. Three are the planted control C-R1's, leaving 54 in 13 unplanted runs. No run-out is late, absent or unresolved.
   - Round 7's logs re-graded give 57 intervals at 185.645 to 190.025 ms. The timer-to-MRPDU rows are 1.292, 2.245 and 3.440 ms (packet `receipts/item4/`).
5. **Docs and residue.** R838-2-F3 and R837-2-3/4/5 are resolved as listed (table below). Further instances of the same stale-figure class are R837-3-2.

**Full-pass receipts.**
- The sweep: 4 of 4 shards exit 0, 65 suites, 0 failures.
- Unit rcs: every W-* job is 0.
- Lane summary: 41 gates at 0. The four that exit 1 are 8x8/2if reports, by design.
- One LiteX simulation (`test_soc_timing_cuts`) hit its 900 s wall clock under load: exit 92, UNKNOWN, never a pass. It passed 8 of 8 when re-run alone, with the same timeout, on a clean clone of the same head (`elaborate-gate_19-first-run.txt`, `-rerun.txt`). The delta touches no LiteX or RTL source; its only `sw/litex` change is a ledger reason string in `ctrl_memory.py`, whose own test passed in both runs. **I accept the rerun as local evidence** for a delta-independent step. Hosted acceptance remains the manager's.
- The packet: 66 published files, each matching `MANIFEST.json` (`receipts/packet_check.txt`). The two path-redacted scripts differ from `INDEX.md` as expected (see S1).

## Findings

### R837-3-1 MINOR - RTL, Robustness, Tests, Docs - the map table's linear bound rests on a hash precondition that the builder does not keep and nothing checks

**Artifacts**
- `sw/firmware/ctrl/aecp/aecp_maps.c:137-141` and `:189` (`place`);
- `sw/firmware/ctrl/aecp/README.md:199-207` ("as at every configuration");
- `sw/firmware/ctrl/test/test_aecp.cpp:2613-2672` (`Core.MapEditWorkIsLinearInItsMappings`);
- `sw/builder/endstation_builder.py:1467` (at most 16 streams per direction) and `:1473` (channels 1..32).

**Authority and evidence**
- Ruling item 3 requires bounded work for refused and accepted legal-length commands. #904 and ruling 6848507008 require one decode and O(n) checking "without rescans".
- The comment's own condition is "distinct for every key of a port with one stream of up to 256 channels, or up to nine streams or clusters of up to 28 channels each, as every configuration has".
  - That is true of the five `configs/*.yaml` (at most 8 streams of 8 channels).
  - The builder accepts up to 16 streams per direction of up to 32 channels each.
  - An output port's key may name any STREAM_OUTPUT of the configuration (`legal()`, `aecp_maps.c:91`).
- In such geometries, keys share slots, and linear probing walks other keys' slots again. That is the rescanning that R838-2-F2 removed.
  - The model (`scripts/hash_probe.py`, which mirrors `place()`) gives, for an accepted ADD of 63 distinct legal keys: 959 visits at 16×8; 935 at 8×32; 1,501 at 16×32; 287 at 10×8. The bound is 2(n + R) = 126; n(n+1)/2 is 2,016.
  - **Real firmware** (`receipts/hash_probe_firmware_8x8.txt`): the 8x8 image, its eight STREAM_OUTPUTs' formats widened to 32 channels, and the ADD of `receipts/hash_keys_8x32.txt` give `935 visits (2 (n + R) 126); held 63`. The command is accepted. The probe is disposable, is planted by `scripts/plant_hash_probe.py`, and has been removed.
- Correctness under collision is tested (`Core.MapKeysThatShareASlotAreTheirOwn`, `test_aecp.cpp:2589`). The work bound is not.
  - The work test widens only stream 0, and its keys are one stream's channels. So by construction they never share a slot, and the test cannot fail for this case.
  - No generator, static assertion or test checks the precondition for a built model.

**Impact**
- For every shipped point the bound holds and the 975 / 1,555 µs records stand.
- A configuration the builder accepts gets map-command work up to about 7 to 12 times the stated linear bound, close to the n(n+1)/2 that R838-2-F2 refused. The source and the README tell its integrator the bound holds there.

**Required outcome.** One of:
- (a) **Enforce the precondition.** The model generator (`aecp_entity.py` / `aecp_shape.py`) or a build-time check refuses a model whose legal keys are not hash-distinct at any port: every STREAM_OUTPUT's channels for an output port, every cluster channel for an input port. Plant a colliding geometry (for example 8 stream outputs × 32 channels) and show it refused.
- (b) **Remove the dependence.** Make the work linear for any legal key set.
- (c) **Scope it publicly.** Get a decision restricting the bound to the checked-in configurations. Restate the comment and the README to say so: name the builder's wider range, give the worst case (a lookup passing up to every held key's slot), and track the gap in an issue.

**Verification**
- (a): the check refuses the planted geometry and passes the five configurations.
- (b): the work arm, run with a colliding geometry, stays within 2(n + R).
- (c): the decision link and the restated text.

### R837-3-2 MINOR - Docs - R4L's paced bound, the pace rule and the load figures stated at pre-ruling values

**Artifacts**
- `tb/verilator/ctrl_service_budget/README.md:183`: R4L "kept tier 1's 20 ms until THE PACE, under which its commands are paced edits and its bound the 240 ms response time, `paced_rows.PACED_BOUNDS`". `PACED_BOUNDS` is `{'R4L': 238}` at this head. The same line cites the 30 ms rows to "the owner's decision of 2026-11-13" (issuecomment-6843318273, the question). FR_NFR and SPLIT_CONTROL_MEMORY now cite the ruling 6844175391.
- `tb/verilator/ctrl_service_budget/README.md:185`: "The tree's pace must be the model's, the smallest whole ms at most 13 that holds txL at 1x1/1if". `paced_rows.choice` also requires R4L ≤ 238 ms (`paced_rows.py:130`).
- `docs/design/SPLIT_CONTROL_MEMORY.md:2355`: "Under THE PACE R4L's commands are paced edits, and its bound is the 240 ms response time". This is present tense; the table row above it and the new section say 238.
- `docs/design/SPLIT_CONTROL_MEMORY.md:2470` ("What is left"): "0.822 at the pin ... and 0.770 in the column with tsn-c-stack #32; within it at 1x1/1if, 0.501 at the pin and 0.499 in the second column". The load gate at this head gives 0.792 and 0.752 at 8x8/2if, and 0.513 and 0.509 at 1x1/1if (packet `receipts/gates/lane-load_check.txt`; `lane-flip_check_exits_1.txt:4,33`). These figures came in during this PR (`5bea2597`), and the delta edited this bullet.

**Impact.** The harness's own README and the design document give a reader a different R4L bound, pace rule and load than the code and the gates hold. This is the class of R837-2-3 and R838-2-F3, in files and lines those findings did not list.

**Required outcome**
- Each line states the head's value: R4L's paced bound 238 ms, which is 240 less T_ingress and T_egress; the pace rule "holds txL within its bound and R4L within 238 ms"; and the loads 0.792 / 0.752 and 0.513 / 0.509, or the bullet marked as the state at a named earlier head.
- The README's 30 ms citation links to 6844175391.

**Verification.** A grep of each line against `paced_rows.PACED_BOUNDS`, `paced_rows.choice` and `load_grade.py --check`. The docs gates pass.

### R837-3-R1 RESIDUE - Docs - `long_notice.py:19-21`'s description of the collision edits

- "two collisions, REMOVEs whose every mapping is the row's key with another value" is not accurate: both payloads include the row's own value (`legal_values` puts it first, `long_notice.py:69`), and `collision_indices` at 1x1/1if ends at the first index the geometry refuses.
- **Exact fix:** "two collisions, REMOVEs of MAPPINGS mappings of the row's key: one over distinct indices of the value's first field, which the port's geometry refuses at its first illegal index, and one over the key's legal values in turn, the row's own among them".
- This changes no code, measurement or figure.

### Suggestions (optional)

- **S1 - Docs - the packet index** (carried from R837-2 S2). `INDEX.md` lists `A10-RULING.md`, which is not published. It does not list itself. The two path-redacted scripts differ from their indexed bytes (`receipts/packet_check.txt`). Generate the index from the published files.
- **S2 - Tests - when "late" starts** (`mrpdu_grade.py:84`). A run-out is late more than `LATE_MS` after the timer's callback. The bound, though, runs from the centisecond that owes the MRPDU, which is earlier, so the classification is slightly lenient. The timer-to-MRPDU rows do measure from the deadline (all within 20 ms). Timing from the owed centisecond, or saying it is timed from the callback, would make the two agree.
- **S3 - Tests - the ACMP decline bound** (carried from R837-2 S1). It would return about 0.48 ms to txL's 1.02 ms margin.
- **S4 - Evidence - H-81N's receipt** shows rc=1 with no reason line. It is the 8x8/1if follow-on lane's point, out of this PR's scope, but its reason would let a cold reader tell a build failure from a gate failure.

## Prior findings at this head

| Finding | Status at `dd01b0af` | Evidence |
|---|---|---|
| R837-2-1 MAJOR: the 50 ms MRPDU bound left no room for T_egress | **Resolved at cause.** 49 and 238 are derived, the join gate is 181.0 to 239.0, the egress-free derivation is planted and refused, and FR_NFR 3.4.1 is amended. | `ctrl_loop.h:342-360`; `paced_rows.py:43`; `join_grade.py:33`; `receipts/pace_choice.txt`; `FR_NFR.md:373,381,415,424-426` |
| R837-2-2 MINOR: the pace count `1 + floor(w/P)` | **Resolved.** ceil((w+1)/P) is held to a gate simulation with the old rule planted. My independent simulation finds 0 mismatches. | `receipts/gate_probe.txt`; `paced_rows.py:54-82,176-190` |
| R837-2-3 MINOR: stale figures and the question cited for the ruling | **Resolved as listed:** `FR_NFR.md:415` (49 ms, 950 to 1050 ms, 9.96 to 15.04 s), `MAILBOX_SPLIT.md:390` (0.9 ms), `ctrl_loop.h:205-209` (130 ms), SPLIT_CONTROL_MEMORY R4 (marked "before #894's tiers"), and the two 30 ms citations (6844175391). Further instances of the class: R837-3-2. | grep at head |
| R837-2-4 RESIDUE: issue-comment IDs in source | **Resolved.** No new ID or review-round label in any added non-doc line. The one remaining hit (`ctrl_mutants.py:834`) is pre-existing and tracked by #746. `ctrl_memory.py:260`'s "S14" is carried from existing text. | scan of the delta's added lines |
| R837-2-5 RESIDUE: the planted run in the count; the pre-restatement receipt | **Resolved.** The REVIEW READY gives 54 intervals in 13 unplanted runs plus 3 in C-R1's, and names the final rows' receipt. | 6870102413 |
| R838-2-F1 MAJOR: late join intervals vanished past the 100 ms horizon | **Resolved at cause.** `resolve` has no horizon and five outcomes; 291 and 500 ms fail as late; absent and unresolved are told apart; the old rule is planted and caught; published intervals are re-graded. | `receipts/join_mutants.txt`; packet `receipts/item4/` |
| R838-2-F2 MAJOR: quadratic collision path in the map rewrite | **Resolved for every checked-in configuration.** One slot per key, a REMOVE's values chained, the table ending at an illegal mapping, and no behaviour change. The counting control refuses n(n+1)/2 at 8, 16, 32 and 63. The collision and conflict cases are in the record (975 µs). **Its cause survives in builder-admitted geometries outside the hash's stated range: R837-3-1 (MINOR).** | `receipts/aecp_work.txt`, `receipts/aecp_core_maps*.txt`, `receipts/hash_probe_firmware_8x8.txt` |
| R838-2-F3 MINOR: numeric contracts in FR_NFR, the AECP README and MAILBOX_SPLIT | **Resolved.** | `FR_NFR.md:415`; `aecp/README.md:120`; `MAILBOX_SPLIT.md:390` |
| R838-2-R1 / R2 RESIDUE | **Resolved.** | as R837-2-4 and R837-2-5 |

## Reviewer-owned completion ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Ruling 6867990126 items 1 to 6 and its STOP list, against: `ctrl_loop.h:328-363`; `aecp_mbx.h:38-52`; `paced_rows.py:35-190`; `tier1_rows.py:209-240`; `join_grade.py:1-82`; `mrpdu_grade.py:1-118`; `FR_NFR.md:370-426`. My flip check 1x1/1if PASS with every row within its bound (`receipts/flip_check_1x1.txt`). `paced_rows.choice` = 7 = the stated pace (`receipts/pace_choice.txt`). The load at 1x1/1if is 0.513 / 0.509 (packet `lane-load_check.txt`). No finding under this lens. | R837-3 | dd01b0afef87037ec485cd49b40a26b542854bdd |
| RTL | UNCLEAN (R837-3-1) | `aecp_maps.c:86-417` (behaviour neutrality, widths, termination, memset scope); `aecp_mbx.c:155-158` and `aecp.c:31-38` (the pace gate's clock); `ctrl_loop.h` constants; the stack-frame report path (`fw_rv32.stack_frames`, report only). No HDL in the delta. | R837-3 | dd01b0afef87037ec485cd49b40a26b542854bdd |
| Robustness | UNCLEAN (R837-3-1) | Refused and accepted maximum-length edits: collision, conflict, illegal, shared slot (`test_aecp.cpp:2585-2672`; `long_notice.py:48-130`). The 1023-channel shared-slot case. The builder-geometry probe (`receipts/hash_probe_firmware_8x8.txt`). Grader outcomes past the old horizon, absent and unresolved, owed frames (`selftest_polls.py:248-337`). | R837-3 | dd01b0afef87037ec485cd49b40a26b542854bdd |
| Tests | UNCLEAN (R837-3-1) | My runs at the head: `Core.*Map*` 10/10, plain and ASan; the work arm 1/1 with counts identical to the author's; harness self-test checks 822/822 and `joins:` mutants 13/13 caught; flip self-test 555/555; rows_tiers self-test 971/971; gate simulation 0 mismatches. The definition test byte-unchanged. | R837-3 | dd01b0afef87037ec485cd49b40a26b542854bdd |
| Docs | UNCLEAN (R837-3-1, R837-3-2; RESIDUE R837-3-R1) | `FR_NFR.md:370-426`; `SPLIT_CONTROL_MEMORY.md:2340-2475`; `MAILBOX_SPLIT.md:390`; `aecp/README.md:120,193-215`; `srp/README.md:238`; `ctrl_service_budget/README.md:141-190`; every comment and docstring in the delta (comment-rule scan). | R837-3 | dd01b0afef87037ec485cd49b40a26b542854bdd |

## Real limits

- Physical calibration was NOT RUN, and no hardware was used. Field skips are not hardware proof. The join intervals on the wire are the bench gate's (S12b), still owed.
- I did not re-run the full banks, the sweep, the harness legs or the hosted job steps. Those figures are the author's published receipts, which I verified against the manifest and spot-checked. Hosted CI does not run on split PRs, and I make no claim about a manager source bank at this head.
- The hash model gives a greedy lower bound on the worst case. The firmware probe confirms it for one geometry (8×32) by widening formats in the 8x8 image's fixture. I did not build a full 16-stream or 32-channel builder configuration.
- No gate bounds the call-chain stack. The edit table grows by 176 B on the stack. The built images exercise it in the largest-notice legs, and the sram figures are unchanged.
- The LiteX `test_soc_timing_cuts` first-run UNKNOWN is resolved only by a local rerun on its own.
- The 8x8/1if and 8x8/2if legs that exit 1 are outside this PR's 1x1/1if bar (ruling 6867393730 (a), and 6867990126 item 6; #910). I did not judge them.

## Pending manager duties

- Route R837-3-1. Either the author enforces or removes the hash precondition, or a public scope decision restricts the bound to the checked-in configurations. Then re-review RTL, Robustness, Tests and Docs at the resulting head.
- Route R837-3-2 for a doc fix and re-review of Docs. Carry R837-3-R1 to the residue checklist.
- Validate the current-dev merge candidate (source base `66f71326`, live dev `b7d69295`) with the builder and native banks, and link the receipts. Own hosted and act acceptance.
- Ruling item 6: the 8x8/1if lane takes the 49 and 238 ms bounds after the merge and checks 1x1/1if byte-identity. #908 and #910 stay open on their own terms.

## Packet

`MANIFEST.sha256` lists every receipt and script. All of them can be re-run against a clone at the exact head; paths go in as arguments. The clone was restored after the probes: the index tree equals the head tree, 1,619 tracked files match in blob and mode, and every gitlink is unchanged (`receipts/restore_check.txt`).

R837-3 FINISHED
