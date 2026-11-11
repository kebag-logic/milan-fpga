[R814] POSITIVE - exact head 2128daad26b932feeed1ef2bde8f2774e8a51a31

# R814-3: external delta review of PR #874 (issue #867, Mark II split S7), round 3

Head `2128daad26b932feeed1ef2bde8f2774e8a51a31`, tree `9b067a62ffa66e2cb51303206cac6c7f85ba61c6`. It is one commit on round 2's `2131eff4`, the head R814-2 reviewed. The PR base is `dev-soft-core` `1d6bf555`, an ancestor of the head (`receipts/delta.txt`).

**Verdict: POSITIVE.** No BLOCKER, MAJOR or MINOR is open. All five lenses are clean at this head.
- The round 3 ruling (PR #874 issuecomment-6766550989), items 1 to 4, is met.
- R813-2's F-1 MINOR is resolved at its cause, and every prior RESIDUE is fixed.
- One new RESIDUE and three new SUGGESTIONs follow. None affects coverage.

## Scope reconstructed

- **Issue #867 acceptance 1 to 7, frozen.**
  - Item 5 was accepted under the test-only fixture (issuecomment-6760813135). Item 5 in the production composition is still owed, so the PR says "Relates to #867".
- **Rulings on the PR:**
  - round 2 (issuecomment-6763709522), with its follow-up option (a) (issuecomment-6765717898): `SVC_MS = 20` stays a cited literal until #810;
  - round 3 (issuecomment-6766550989), which scopes this delta:
    1. grade the Join interval only for frames the Join timer actually gated, read from lwSRP's state at its boundary, not from a time window, and grade a requested opportunity after an idle expiry by the "within JoinTime" rule;
    2. keep the existing refusals;
    3. add R813-2's off-grid case as committed controls at 16,280 and 16,240 ms;
    4. fix the wording residue.
- **Authorities:**
  - IEEE 802.1Q-2018 10.7.4.1, 10.7.11 and Table 10-7;
  - `docs/reference/FR_NFR.md` 3.4.1 (Milan v1.2 4.2.7.1.1 and Table 4.3: JoinTime 200 ms, 180 to 240 ms, and a point-to-point requested transmit opportunity within JoinTime);
  - lwSRP at the pinned gitlink `08ee86e8`: `src/core/mrp_mad.c:91-116` (port state layout), `:850-855` (`on_join_timer`), `:1410-1542` (`mrp_transmit`) and `src/ports/timer.c:25-36` (`shlan_timer_tick`).
- **The delta:** seven files (`receipts/delta.txt`). There is no HDL, no firmware C and no workflow file:
  - the bench: `srptx.hpp` and `twin_split.cpp`;
  - the grade and plants: `srptx_grade.py` and `srptx_plants.py`;
  - `Makefile`;
  - `tb/verilator/milan_dp/README.md` and `sw/firmware/ctrl/srp/README.md`.

## What was checked, per ruling item

1. **Attribution by what lwSRP did: holds.**
   - **The bench's model matches lwSRP.** Read against the pinned lwSRP:
     - Each successful transmit sets `join_wait = join_cs` and arms the Join timer (`mrp_mad.c:1539-1540`). Nothing else arms it.
     - `mrp_transmit` returns 0 with no prepared PDU while `join_wait` is set, or when nothing is pending (`:1421`, `:1479-1484`).
     - The Join expiry only clears `join_wait` (`:854`).
     - `shlan_timer_tick` calls the callback on the decrement to 0 (`timer.c:25-36`). So `cs == 0` is `join_wait == 0` for an armed timer, and the bench's `due` test (`cs == 1` before the tick, `srptx.hpp:599-613`) is the expiry.
     - `join_timer` is the third timer after `la_timer` and `pt_timer` (`mrp_mad.c:110-113`), so `la + 2` is right (`srptx.hpp:501-505`, `:538`). The committed `[BENCH]` arm "a field before lwSRP's Join timer" still refuses a changed layout (author receipt `srptx/make-srptx-mutants.txt`).
     - `periodic_owed` (`:833`) arises only with a prepared PDU, which is sent regardless of `join_wait`. So an idle poll (result 0, Join timer stopped) really holds no pending request, and the requested rule's bound is a valid lower bound on the request time.
   - **`poll()` (`srptx.hpp:516-525`)** does what the ruling asks:
     - it reads `join_stopped` before the poll;
     - it marks every record the poll produced;
     - it consumes `join_expired`;
     - it keeps `idle_us` as the last idle poll with the Join timer stopped.
   - **`srptx_grade.py` follows it.**
     - `join_intervals` (`:424-428`) takes only `after_join` frames, LeaveAll frames included.
     - The requested rule (`:349-359`) takes only frames with `idle_us`, excluding held spans.
     - `causes` (`:408-421`) is now called only from `measure_time` (`:438`). So `ATTRIBUTE_MS` serves the measurement only, as its comment now says.
   - **Completeness, from the author's `probes/attribution-compare.txt`.** In `wire`, 727 MSRP frames are 116 Join-gated + 610 requested + the first frame after reset. MVRP has the same shape. My clean control at 3 s shows the same thing: one "neither" per application, the first frame (`receipts/probe-join-gate-off.txt`).
2. **The refusals: hold.** All are in the author's receipts `srptx/make-srptx-plants.txt` and `srptx/make-srptx-mutants.txt` at this head, and `probes/r814-1-code-probe.txt`, which ran my role's round-1 probe unchanged:
   - `join-early-past-t-svc` and `join-interval-late` are refused by their own words;
   - `join-10cs` and `join-15cs` are refused by "... ms after the one before, outside JoinTime's range widened by T_svc (160 to 260 ms";
   - `requested-late` (221 ms) is refused, and `requested-within` (219 ms) is clean.
   - The ablation (`probes/ablate.txt`) shows each new path is necessary:
     - without the requested rule, `requested-late` escapes;
     - without the Join record, both Join plants escape;
     - the round-2 grade refuses `licence-16280` with R813-2 F-1's words.
3. **The off-grid controls: hold.**
   - `make srptx` runs `licence-16280` and `licence-16240` (`Makefile:995-1019`).
   - `srptx_plants.py:355-371` requires each run to:
     - grade clean;
     - apply the peer's LeaveAll at the named ms;
     - hold its case: a frame after an idle Join expiry that is not `after_join` and carries `idle_us` (`off_grid`, `:207-222`).
   - Both pass (`make-srptx-plants.txt:72-73`). Each answer is 1.044 ms after the stimulus and follows the Join expiry at 16,200.001 ms.
   - R813-2's `request_probe.py`, run unchanged, gives 0 findings at 280 and 240 (`probes/request-probe.txt`).
4. **Residue: fixed** (table below).

**Measurements and docs figures, cross-checked against `srptx/wire-report.json.txt`:**
- The README rows match the report exactly:

  | Application | JoinTime N | Egress N | Mean | Max | Periodic N |
  |---|---|---|---|---|---|
  | MSRP | 116 | 105 | -8.865 | 0.46 | 524 |
  | MVRP | 111 | 106 | -9.352 | 15.48 | 520 |

- `licence-16280` and `licence-16240` carry 69 MRPDUs each.
- Plants and controls: 26 plants, 4 controls and 2 off-grid controls, as `README.md:108` and the PR body state.
- `srptx/measured-diff-vs-round2.txt` lists the leaves that moved. Each is explained by the re-attribution in the PR body.

**The author's evidence packet:** commit `2ab1ccde`, `review-evidence/665s7-r1`.
- All 362 MANIFEST entries match by sha256, 81 of them under `author-r3`. No file is missing or unlisted (`receipts/evidence-packet-verify.txt`).
- Every round-3 receipt's first line names this head.
- The live PR body equals the published `author-r3/PR-BODY.md` plus a trailing line.

**My probe** (`scripts/run_probes.sh`, `scripts/gate_probe.py`, `receipts/probe-join-gate-off.txt`):
- **Toolchain.** Verilator 5.050, pinned, with its identity and sha256 in the receipt.
- **The arm.** It removes lwSRP's Join gate (`ps->join_wait = 0;` in a copy of `mrp_mad.c`, through `twin_fw.py --replace`). It is built and run through the tracked driver's own `build()` and `run()` helpers.
- **Results:**
  - `wire` to 3,000 ms: three MSRP frames in 3.3 us at ms 1, sent while the Join timer ran, and 0 findings.
  - `wire` to 40,000 ms: refused, 3 findings, all from the rate rule.
  - `licence`: refused, 1 rate-rule finding.
  - `hold`: refused, 104 rate-rule findings.
  - The clean control at 3 s grades clean.
- **What it shows.** The committed scenarios refuse this defect, through the rate rule only. See S-1.

**Comment rule:** the delta's added source lines name no lane, round, reviewer ID or comment ID. The scan finds 0 matches (`receipts/delta.txt`). The README `[TIME]` row's issuecomment link is documentation and is carried unchanged from round 2.

## Prior findings, resolved or retained at this head

| ID | Status | Evidence at `2128daad` |
|---|---|---|
| R813-2 F-1 (MINOR: a conformant requested opportunity after an idle Join expiry refused as a Join interval) | **RESOLVED at its cause** | The attribution is now lwSRP's boundary state, not a window (item 1 above). Committed controls at 16,280 and 16,240 ms are clean and hold their case. The round-2 grade refuses 16,280 (`probes/ablate.txt` section 1) |
| R813-2 R-1 / R814-2 R-1 (RESIDUE: PR body read as STOP) | **FIXED** | PR body `## Status`: "Round 3 at `2128daad`, ready for delta review", and option (a) is stated as ruled |
| R813-2 R-2 (RESIDUE: `ATTRIBUTE_MS` comment) | **FIXED, and true** | `srptx_grade.py:97-99`. `causes` is called only by `measure_time` (`:438`) |
| R814-2 R-2 (RESIDUE: garbled grade prose) | **FIXED** | Docstring `:20-22` and comment `:342` read as the exact fix |
| R814-2 R-3 (RESIDUE: rate window name) | **FIXED** | `README.md:1557` "1.5 x JoinTime less T_svc (280 ms)" |
| R814-2 S-1 (Join bound assumes the frame before armed the timer) | **RESOLVED** | Every transmit arms the Join timer (`mrp_mad.c:1540`), and only the frame the Join expiry released is graded. So the frame before is the one that armed it |
| R814-1 F-1, F-2 | stay resolved | The delta does not touch `SVC_MS` or the bounds. The 10 cs and 15 cs arms are still refused |
| R814-1 S-1 (timer `id` is a heap pointer), S-2 (fixture suffix unconditional), S-3 (no later reset) | retained, SUGGESTION | Untouched by the delta |
| R814-2 S-2 / R813-2 S-3, S-4 (rate and `[608]` boundary pairs; the rate rule has no code arm) | retained, SUGGESTION | My `join-gate-off` arm is the first code arm the rate rule kills, in `wire` to 40 s, `licence` and `hold`. It is a reviewer probe, not committed. See S-1 |
| R814-2 S-3, S-4; R813-2 S-1, S-2; R813-1's four SUGGESTIONs | retained, SUGGESTION / residue checklist | Untouched by the delta. R813-1's go to the merge residue checklist per the round 2 ruling |

## Findings

### R-1 RESIDUE: the requested and follow-up rules called "within JoinTime" where the bound is JoinTime + T_svc

- **Lenses:** Docs.
- **Where:**
  - `tb/verilator/milan_dp/srptx_grade.py:350`, comment: "and the frame leaves within JoinTime of it";
  - `tb/verilator/milan_dp/README.md:1557`, the `[TIME]` row: "the attribute's next message within JoinTime (220 ms)".
- **Evidence:** both rules grade against `JOIN_FOLLOW_MS = JOIN_MS + SVC_MS` = 220 ms (`srptx_grade.py:79`). The finding text says so ("past JoinTime + T_svc (220 ms"), and so does the same README row's requested clause ("within JoinTime + T_svc (220 ms)"). The module docstring (`:18-28`) is covered by its own "each bound widened by ... T_svc" and needs no change.
- **Impact:** wording only. No figure, check or output changes.
- **Exact fix:**
  - `:350` "... so the request came after it, and the frame leaves within JoinTime + T_svc of it".
  - `README.md:1557` "the attribute's next message within JoinTime + T_svc (220 ms)".
- **Verification:** read both lines. `make srptx-plants` is unchanged.

### S-1 SUGGESTION: a frame lwSRP sends with its Join timer running falls in neither Join rule

- **Lenses:** Tests, Robustness, Conformance.
- **Where:** `tb/verilator/milan_dp/srptx.hpp:516-525` (`poll()`) and `srptx_grade.py:342-359`.
- **Evidence:** a third class of frame is graded by neither Join rule: not `after_join`, and with no `idle_us` because `join_stopped` was false. Correct lwSRP never produces it, outside a retained-PDU retry, which only a hold produces. My `join-gate-off` arm produces exactly that class (`receipts/probe-join-gate-off.txt`):
  - three MSRP transmit opportunities in 3.3 us at boot, 0 findings in a 3 s run;
  - it is refused in every committed scenario, but only by the rate rule (no four in 280 ms).
- **Impact:** none at this head. The committed suite kills the arm, and 10.7.4.1's own rate limit is the normative rule that does it. A sparser gate defect, one early frame per 280 ms, would pass every rule.
- **Suggested outcome:**
  - The bench already sees the condition. Refuse an MRPDU that left lwSRP with its Join timer running and no prepared-PDU retry pending, outside a hold, either as `[TIME]` (10.7.4.1) or `[BENCH]`.
  - Optionally commit `join-gate-off` as a code arm. It also answers the carried "rate rule has no code arm" suggestion.

### S-2 SUGGESTION: grade a requested opportunity from its observable trigger where one exists

- **Lenses:** Tests, Conformance.
- **Where:** `tb/verilator/milan_dp/srptx_grade.py:349-359`. The author discloses this limit in the PR body's limits and in `README.md` ("The requested rule's bound is the last poll that sent nothing").
- **Evidence:** the adapter polls every millisecond. So `idle_us` trails the frame by at most 1.03 ms in every run (`srptx/join-figures.txt`). The rule therefore bounds the adapter-to-wire path, and lwSRP's own delay of a request is invisible to it.
- **Impact:** none at this head. lwSRP's scheduling is graded by the follow-up and rate rules.
- **Suggested outcome:** where the bench records the trigger, also bound egress from it to JoinTime + T_svc. Triggers it records today:
  - a periodic expiry (the 610 requested frames per application in `wire`);
  - the peer's stimulus in `applied` (the off-grid controls).

### S-3 SUGGESTION: `--peer-leave-all-ms` accepts any value

- **Lenses:** Robustness.
- **Where:** `tb/verilator/milan_dp/twin_split.cpp:511-525` (`srptx_args`), `:470-474`.
- **Evidence:**
  - The option is refused outside `licence`, which is good.
  - `std::stoul` is cast to `uint32_t` without a range check, so 4294967297 becomes 1.
  - A value at or after `kWithdrawMs` (18,000) turns the `[608]` case into a withdrawal before the LeaveAll. `srptx_plants.py` guards the two committed values only.
- **Impact:** a manual run can grade a scenario that no longer holds its case. The committed targets are unaffected.
- **Suggested outcome:** refuse a value outside the licence grant to `kWithdrawMs` window, or one above `UINT32_MAX`.

## Ledger (reviewer-owned)

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `srptx_grade.py:64-99`, `:342-359`, `:408-441` against round-3 ruling items 1 to 3, #867 item 3, IEEE 802.1Q-2018 10.7.4.1, 10.7.11, Table 10-7, `FR_NFR.md` 3.4.1; lwSRP `mrp_mad.c:91-116`, `:833`, `:850-855`, `:1410-1542`, `timer.c:25-36`; off-grid controls and `request_probe` receipts; S-1, S-2 | R814-3 | 2128daad26b932feeed1ef2bde8f2774e8a51a31 |
| RTL | CLEAN | `receipts/delta.txt`: no HDL, firmware C or workflow file in the delta. The datapath arm "the split's ACTIVE term held open" is still refused (`srptx/make-srptx-mutants.txt`). The bench C++ (`srptx.hpp:501-525`, `:529-545`, `:599-613`) was checked for pointer layout, pre-poll state read and expiry detection against lwSRP. HDL unchanged since R814-1's clean RTL lens at `5fb6904f` | R814-3 (delta); R814-1 (unchanged HDL) | 2128daad26b932feeed1ef2bde8f2774e8a51a31 |
| Robustness | CLEAN | `poll()` on error results and holds (`srptx.hpp:516-525`; `srptx_grade.py:235-241`, `:353-355`); the hold scenario's attribution counts; `twin_split.cpp:470-474`, `:511-528`; reviewer arm `join-gate-off` on `wire`, `licence` and `hold`; S-1, S-3 | R814-3 | 2128daad26b932feeed1ef2bde8f2774e8a51a31 |
| Tests | CLEAN | `srptx_plants.py:37-117`, `:194-222`, `:328-371` (26 plants, 4 controls, 2 off-grid controls); `srptx_mutants.py` (12 arms); author receipts `make-srptx*.txt`, `probes/ablate.txt`, `attribution-compare.txt`, `r814-1-code-probe.txt`, `request-probe.txt`; my probe and clean control; S-1, S-2 | R814-3 | 2128daad26b932feeed1ef2bde8f2774e8a51a31 |
| Docs | CLEAN (RESIDUE R-1 carried) | `tb/verilator/milan_dp/README.md:108` and `:1488-1702` (the obj_srptx section); `sw/firmware/ctrl/srp/README.md:381-388`; `Makefile:41-43`, `:995-1019`; the PR body against the receipts; the comment-rule scan; prior RESIDUE items verified fixed | R814-3 | 2128daad26b932feeed1ef2bde8f2774e8a51a31 |

## Real limits

- **Delta review.** Code the delta does not touch keeps its R814-1 and R814-2 verdicts. I did not re-run the full sweep, the firmware banks, the CI replay, `make twin`, `split`, `test_builder.py` or the budget harness. I also did not re-run `make srptx`, `srptx-plants` or `srptx-mutants` myself.
  - Source-head execution evidence for all of those is the author's published receipts (packet `2ab1ccde`, verified by hash, not re-executed).
  - My own execution is the `join-gate-off` arm on `wire` (3 s and 40 s), `licence` and `hold`, plus one clean control on `wire` at 3 s.
- **Time model.** The firmware takes no simulated time. `[TIME]` measures lwSRP's timers plus the RTL path and never exercises the T_svc it widens by.
- **Shape.** One interface at the AX7101 shape only.
- **Item 5.** It holds only under the published fixture. The production-composition run is owed (#867 stays open).
- **No manager source bank** runs at this head, and none is claimed or inferred here.
- **Hosted checks at the exact head** (`receipts/hosted-checks.txt`, read-only, at review time):
  - 5 succeeded;
  - 1 was skipped (Physical gPTP, nightly/manual), which is no execution and no hardware proof;
  - 39 were queued or in progress.
- **Hardware.** Physical calibration NOT RUN. No bench or hardware evidence exists; field skips are not hardware proof.
- **Restore.** The probes ran through the tracked driver into work directories outside the tree. The ignored build outputs they left in the clone were removed. `write-tree` equals `9b067a62`, with 0 index or worktree differences and 0 untracked or ignored entries. Five gitlinks match HEAD, and `external` is uninitialised as at the start (`receipts/restore-check.txt`).

## Pending manager duties

- The hosted and act acceptance at the exact head. 39 hosted contexts were still queued or in progress at review time.
- The current-dev merge candidate (builder and native banks) at the merge turn, on live `dev` `45c0b56c`, with its receipts linked on the PR.
- Carry R-1 to the residue checklist, with the retained SUGGESTIONs and R813-1's four.
- Keep #867 open for item 5 in the production composition, after #810, as ruled.
- The #495 residue line owned by #810: switch `SVC_MS` to the budget source.

R814-3 FINISHED
