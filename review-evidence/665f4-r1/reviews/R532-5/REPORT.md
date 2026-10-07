[R532] NEGATIVE - exact head 500b8f64443777685e6a54049d933476710d26f0

# R532-5: internal independent review of #665 / PR #690 (F4 SRP), round 5

- **Head:** `500b8f64443777685e6a54049d933476710d26f0`, tree `b1b7d3b1b9dcf7d8f3f7f299365392ebc1f17ed8`. The live PR head was re-read as this SHA. The reviewed delta is `6f7deea1..500b8f64`. Its context is the full lane diff from the FC r2 head `db9aa8c9b135b34ff3d070a979dee70440b37cc6`.
- **Assignment:** #665 comment 6037276691 (F4 round 5, lwSRP re-pin). Review start: PR comment 6038106325.
- **Independence:** this is a cleared-context session working in its own detached clone. I reconstructed the task from AGENTS.md/CONTRIBUTING.md, the issue body, the assignment, the author REVIEW READY comment (#665 6037833465), the public author packet `review-evidence/665f4-r1/author-r5/` (archive `0fc49330`), the diff, and my own executions. I opened prior review comments on PR #690 only after the findings and ledger below were fixed.
- **Outcome:** one open MAJOR finding, attributable to all five lenses. Two RESIDUE items and two SUGGESTION items are also recorded.

## Summary

The delta contains only the lwSRP gitlink and pin guard, four restaged exhaustion tests with one new fixture helper, and documentation/diagram updates. The production adapter (`srp_mbx.c/.h`), the pool sizing, the coverage ratchet and the exclusions are byte-identical to round 4.

All of the following were verified clean:
- The pin, the guard and the generated diagram.
- The full control firmware gate: 100/100 control mutants, 70/70 SRP plants, both pin-refusal controls and 38 arms.
- The coverage ratchet: 15 files at 100% with no new exclusion.
- An independent re-measurement of the linked composition, which matches the author's figures exactly.
- The documentation gates.
- The cross-pin necessity of the test restaging.

The re-pin does change a behaviour the adapter depends on. At `a4cbe41d`, every Registrar Join/Leave indication must first reserve a 64-byte propagation entry from the SRP pool, even on a single-port participant.
- If that reservation fails, `mrp_rx` returns NO_MEMORY and stops later attributes. The dependency's contract tells the caller to retry the payload.
- A LeaveTime expiry is deferred by 1 cs retries.

At the old pin, Leave processing allocated nothing. The adapter was not adapted. It counts the refused receive as `malformed` and discards it.

My probes show the effect with the pool exhausted:
- A peer's Listener Lv is lost. The Talker licence stays active, and it is still active 19.7 s after storage is released.
- The LeaveTime revocation is held past its 5 s deadline.

At the old pin, both revoke on time under the same exhaustion. The four fixtures that first exposed this receive refusal were restaged to complete reception before exhausting the pool. As a result, no test now exercises refusal at receive time.

## Findings

### R532-5-F1 | MAJOR | Conformance, RTL, Robustness, Tests, Docs | The re-pin makes receive-time Leave processing allocate. The adapter drops the refused Lv as malformed, so under exhaustion the Talker licence outlives the Milan rapid-leave and LeaveTime deadlines.

**Location**
- Adapter receive path: `sw/firmware/ctrl/srp/srp_mbx.c:373-377`. Any non-zero `mrp_rx` result becomes `++m->malformed` and the frame is consumed with no retry.
- Dependency at the pin:
  - `third_party/lwSRP/src/core/mrp_mad.c:543-551`: `map_reserve` allocates per port, including a one-port app.
  - `mrp_mad.c:645-660`: a failed reservation restores the prior Registrar state. For LEAVETIMER it re-arms 1 cs.
  - `mrp_mad.c:1094`: `mrp_rx` returns `map_error`.
  - `src/include/shish_lan/mrp.h:272-276` and `:360`: "Reservation failure preserves the prior value and state for receive retry ... Later attributes wait for that retry", and "A failed receive retry returns NO_MEMORY. Retry that payload after recovery."
- Documented commitments that no longer hold under exhaustion:
  - `sw/firmware/ctrl/srp/README.md:100-101`: "IN/rLv issues Lv and enters MT immediately. The corresponding Talker licence ... is revoked in that pass."
  - `:104`: "The original five-second deadline revokes the Talker licence."
  - `:38`: exhaustion "is counted and refused".
- Tests that route around the path: `sw/firmware/ctrl/test/srp_fixture.hpp:142-152` (`receive_before_poll`) and `srp_mbx.cpp:333/345/449/951`.
- Author claim: author-r5 `HANDOFF.md:12` ("no production adaptation was needed") and the PR body Round 5 ("no production adapter change is needed").

**Authority:**
- Assignment 6037276691 item 1: "Adapt the adapter only where the lwSRP API or behaviour requires it, and state each change."
- Milan v1.2 4.2.7.2.2 (MSRP rapid leave), as adopted by the lane's resolution of R532-1-F1/R533-1-F1.
- #608: the original LeaveTime deadline.
- The dependency's documented receive-retry contract (`mrp.h:360`).

**Evidence**

The probe is `scripts/srp_exhaustion_probe.cpp`, run with `scripts/srp_probe.py`. The same unchanged parent sources and tests were run against both pins. The old pin is `4134b577`, whose `src/` tree `e5a427af` equals the `f4-applicant-notes` base that the round-4 README records as equal to the old pin.

| Case (pool exhausted by holding every block) | New pin `a4cbe41d`, IF=1 / IF=2 | Old pin `4134b577`, IF=1 / IF=2 |
|---|---|---|
| Peer Listener Lv for an active Ready stream | Lv refused: `malformed+1`, `received+0`, licence stays active | Lv applied: `received+1`, licence revoked in that pass |
| After storage is released | Licence still active, revoked only after 19700 ms (LeaveAll + LeaveTime) | n/a: already revoked (0 ms) |
| Peer LeaveAll, then the 5 s LeaveTime elapses | Licence still active at 5.1 s, `stops=0`. It is revoked within 200 ms of release. | Licence revoked at the deadline, `stops=1` |

Receipts:
- New pin: `receipts/probes/exh-new-if1.log`, `exh-new-if2.log` (rc 1, 2/2 probe expectations fail).
- Old pin: `exh-old-if1.log`, `exh-old-if2.log` (rc 0).
- Struct sizes: `receipts/struct-sizes.txt`. Small-class blocks (2 per interface) are fully used by `mrp_app` (8 B) and ops copies (64 B) on RV32, so each 64-byte `mrp_map_work` draws on medium/large headroom.

Plant `A1` changes `receive()` so that NO_MEMORY is counted as received rather than malformed. It escapes the full adapter suite at the new head (`receipts/runs/plant-A1.log`, 53/53 pass). It also escaped the round-4 tests at the old pin (`plant-A1-r4tests-oldpin.log`), so no test classifies or recovers a refused receive.

**Impact**
- While the SRP pool is exhausted, a Listener withdrawal or a LeaveTime expiry no longer stops the Talker. The failure is fail-open: the licence stays active.
- The lost Lv is not recovered when storage returns. It waits for the next LeaveAll cycle, measured at about 20 s.
- The `malformed` counter attributes a local resource failure to the peer's frame.
- The handoff's statement that no adaptation was needed is not supported. The very symptom (receive refused before the adapter's allocation) was observed by the author and absorbed into the test staging.

**Reachability limit:** a wire-only Domain flood did not reproduce the lost Lv (`receipts/probes/flood-*.log`). A refused new MT instance is reclaimed, which leaves one free block when the Lv arrives. The rc 1 in those four logs is a probe mock-cardinality artifact that is identical at both pins; the printed state shows the Lv applied. The defect therefore needs complete exhaustion, which is the condition the lane's own suite treats as first-class and the README says is finite capacity. That limit is why this is MAJOR rather than BLOCKER.

**Required outcome:** under SRP pool exhaustion, a received Listener Lv must not be lost, and neither the rapid-leave revocation nor the LeaveTime revocation may stay fail-open beyond its documented deadline. Any of these would satisfy that:
- the adapter honours the dependency's NO_MEMORY retry contract (for example, retains the refused payload and retries it after reclaim);
- the adapter fails closed when a receive is refused;
- the pool keeps a reservation that registrations and declarations cannot consume, with a stated bound.

If the chosen behaviour is to accept the limitation, that must be a recorded maintainer decision, and `srp/README.md:38/100-104` must qualify the commitments. In every case:
- distinguish refusal from malformed input, or document why it is counted there;
- correct the "no production adaptation" claim in the handoff and PR body;
- add new-pin tests that refuse a receive by exhaustion and fail for the wrong behaviour.

**Verification**
- `scripts/srp_exhaustion_probe.cpp` (or the lane's equivalent) passes at IF=1/2 on the new pin, or its expectations match the recorded decision.
- Plant `A1` and a plant that drops the retained payload or skips the fail-closed path are caught by named tests.
- The full `test_ctrl_firmware.py --require-rv32 --self-test` and `fw_coverage.py --check` stay green.

### R532-5-R1 | RESIDUE | Docs | PR #690 body still describes the published head as local and unpublished (retains R532-2-R2)

`PR #690 body`, Status line 17, line 19, Round 5 line 44 and "How to get into the same state" line 55 still say:
- "REVIEW READY locally"
- "PR #690 already contains round-4 head `6f7deea1...`"
- "This new head awaits publication"
- "The manager publishes this test branch before its dependency PR"
- "After publication, set ..."

The head `500b8f64` is now the published PR head, and `f4-applicant-notes` is published at `ced667d8`.

Exact fix:
- Status: "Round 5 REVIEW READY: `665-f4-srp` -> `dev`, head `500b8f64443777685e6a54049d933476710d26f0` (published; fresh independent reviews in progress)."
- Delete "PR #690 already contains round-4 head ... This new head awaits publication and fresh independent review."
- Round 5: "Dependency branch `f4-applicant-notes` carries merge `ced667d8...` (lwSRP PR #15)."
- "How to get into the same state": "Set disk-scratch, documentation-environment and compiler locations for the local installation:".

This is wording only. It changes no figure, test or verdict.

### R532-5-R2 | RESIDUE | Docs | `sw/firmware/ctrl/srp/README.md:172-173` calls the notes merge local

The README says: "Its round-5 local merge adopts the current public dependency pin. The handoff records that local branch and its exact merge commit." `origin/f4-applicant-notes` is now `ced667d8ee35929ab5f9e77a1c5396e173a693d8`.

Exact fix: "Branch `f4-applicant-notes` now merges public `main` at `ced667d8` (lwSRP PR #15)."

This is wording only. Note 4/5 test execution itself is out of scope for this round, as stated in the assignment.

### R532-5-S1 | SUGGESTION | Docs | Stale dependency timer claim outside this PR's diff

`sw/firmware/gtest/README.md:416-420` says lwSRP's timer port keeps timers "with no removal" and that "F4 inherits that constraint". Both pins provide `shlan_timer_remove` (`third_party/lwSRP/src/ports/timer.c:37`), and `mrp_app_destroy` calls it (`mrp_mad.c:924-936`). The paragraph comes from `ddd1adfb5`, which is in the FC base and in live dev `e21c1ca0`, not in this lane's diff. Per AGENTS.md section 4 it belongs in a new Issue rather than in this lane.

### R532-5-S2 | SUGGESTION | Tests | Dependency-internal parse and indication changes have no adapter-level wire case

The following plants in a disposable copy of the pinned dependency escape both the adapter suite and the processor-wire walk:
- L1: drop the changed-value Join upgrade.
- L2: limit changed-value indication to IN.
- L5: disable higher-version skipping.
- L6: restore per-value skipping instead of whole-PDU rejection.

Receipts are `receipts/runs/plant-L{1,2,5,6}*.log`. The adapter is correctly insensitive to L1/L2: it polls `mrp_attr_visit` for Talker/Listener state, and Domain is keyed by full value (`msrp.c:385-387`). L5/L6 change which peer PDUs the adapter accepts, which is the dependency's own tested contract. One wire case each (a higher-version PDU accepted, and a PDU with one invalid value rejected as a whole and counted malformed) would pin the integrated behaviour. This is optional.

## Reviewer-owned lens ledger

| Lens | Result | Examined artifacts at this head | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (R532-5-F1 open) | Assignment 6037276691 items 1-4. lwSRP `4134b577..a4cbe41d` `src/` diff (headers: comments only, no signature change). `srp/README.md:87-121`. #608 and Milan rapid-leave tests (`srp_mbx.cpp:51/497/507/1011`) pass. L3 plant caught by `InListenerWithdrawalRevokesLicenceImmediately`/`InTalkerWithdrawalImmediatelyWithdrawsListener`. Exhaustion probes. | R532-5 | `500b8f64443777685e6a54049d933476710d26f0` |
| RTL | UNCLEAN (R532-5-F1 open) | `srp_mbx.c` (unchanged; error path `:373-377`). Dependency interface `mrp.h:265-362`. `mrp_mad.c` allocation sites `:484/543/888-890`. Pool classes `srp_mbx.h:86-90` against measured RV32/host struct sizes (`receipts/struct-sizes.txt`: attr 112->176 B, still medium; new 64 B work entry). Mailbox bench inputs identical across the delta (`receipts/mbx-input-delta.txt`, 0 lines). | R532-5 | `500b8f64443777685e6a54049d933476710d26f0` |
| Robustness | UNCLEAN (R532-5-F1 open) | Exhaustion at receive, poll and LeaveTime boundaries at both pins and IF=1/2. Wire-only Domain flood. Link-restart and refused-Domain cases (`srp_mbx.cpp:951`). Full suite at IF=1/2 in the gate. | R532-5 | `500b8f64443777685e6a54049d933476710d26f0` |
| Tests | UNCLEAN (R532-5-F1 open) | Cross-pin matrix: the round-4 tests fail exactly the 4 restaged tests at the new pin, and the round-5 tests pass 53/53 at the old pin (`receipts/runs/x-*.log`). Plant A2 (helper polls during receive) is caught by all four. Plant A1 escapes. Full gate: 100/100 control mutants, 70/70 SRP plants, 2 pin controls, 38 arms, rc 0, 437 s. Coverage `--check` rc 0, 15 files 100%, `coverage.ratchet` and `fw_coverage.py` untouched by the delta. | R532-5 | `500b8f64443777685e6a54049d933476710d26f0` |
| Docs | UNCLEAN (R532-5-F1 open; R1/R2 are RESIDUE) | `docs/reference/SUBMODULES.md:26/196-199`, `sw/firmware/ctrl/README.md:134-140`, `srp/README.md:166-173/219-220`, `docs/testing/CI_WORKFLOWS.md:54-58/2295-2307`, `gtest/README.md:397-400` and `rtl-fast.yml:238-283`, checked against the workflow. Diagram drawio/svg/png/manifest. 11 targeted gates plus `docs_check.py` rc 0 (`receipts/docs-gates.txt`, `runs/docs-check.log`). Live PR body and author-r5 HANDOFF. | R532-5 | `500b8f64443777685e6a54049d933476710d26f0` |

The following were verified clean within the unclean lenses:
- The lwSRP gitlink `a4cbe41d` is public `main`, and the guard `ctrl_arms.py:248-249` matches it.
- The linked composition was re-measured at both pins with one runtime (`receipts/linked-size.txt`, `receipts/size/*.json`):

  | Shape / IF | Old span (bytes) | New span (bytes) | Increase |
  |---|---:|---:|---:|
  | 1x1 / 1 | 53968 | 54592 | 624 |
  | 1x1 / 2 | 65216 | 65840 | 624 |
  | 8x8 / 1 | 68656 | 69280 | 624 |
  | 8x8 / 2 | 94656 | 95296 | 640 |

  All growth is in `.text`. `.bss` and `image_arena` are unchanged. These equal the author's published figures exactly.
- Shared bindings, link lifecycle, #608 and the Milan opt-in tests all pass at IF=1/2.

## Prior public findings at this head

| Finding | Disposition at `500b8f64` |
|---|---|
| R532-1-F1 / R533-1-F1 (Milan immediate leave) | RESOLVED in normal operation and retained: the opt-in (`msrp.c:411`, `mrp_mad.c:626`) and its tests pass, and plant L3 is caught. The exhaustion regression is new, recorded as R532-5-F1. |
| R533-1-F2 / R532-2-F1 (link lifecycle) | RESOLVED, retained. The adapter is byte-identical and the lifecycle tests pass at IF=1/2. |
| R533-1-F3 / R533-2-F1 (shared declaration) | RESOLVED, retained. The shared-binding tests and their plants pass or are caught. |
| R533-1-F4 (linked size) | RESOLVED, and independently re-measured at the new pin (exact match). |
| R532-1-F2 / R533-2-F2 (admission, ReadyFailed, notes 4/5) | RESOLVED, retained. The notes 4/5 suite moves to lwSRP PR #15 (out of scope). |
| R532-2-F2..F4, R532-3-F1/F2 | RESOLVED, retained. The artifacts are unchanged and their tests and plants pass or are caught in my gate run. |
| R532-1-S2 (LV/rJoinIn extra Join indication) | RESOLVED upstream by the re-pin: `mrp_mad.c:355/361` now give no indication for LV + rJoinIn, and changed values still indicate (`:631-634`). |
| R532-1-S1, R532-1-S3, R532-2-S1 | ADDRESSED, retained. |
| R532-1-R1, R532-1-R2, R532-2-R1, R532-3-R1 | RESOLVED, retained. |
| R532-2-R2 (publication wording) | RETAINED as RESIDUE R532-5-R1, with the updated exact fix. |

## Method notes and limits

The pin-equivalence and size-measurement method:
- **Old-pin equivalent:** `23d9a817` is no longer fetchable after the history rewrite. I used `4134b577`, whose `src/` tree equals the published `f4-applicant-notes` base `72209a53`, which the round-4 README stated has production sources equal to the old pin. The cross-pin matrix corroborates this: the round-4 tests pass at the old pin except where predicted.
- **Size runtime:** built from LiteX at the repository pin `a1e1c365`, plus the default-branch picolibc (`6a13ccce`, data `16ff442d`) and compiler-rt (`6eb76609`) data packages (`receipts/runtime-fetch.txt`). Absolute spans could depend on runtime revisions. They nevertheless equal the author's figures, and the delta is runtime-independent.

What was excluded, and why:
- **Contaminated run:** my first gate attempt was contaminated by a duplicate concurrent run in the same build directory. It is retained as non-final in `receipts/nonfinal/`, and only the clean rerun counts.
- **Walk with exported tree:** `walk-head-if2` was refused because an exported tree lacks Git metadata. The walk at head passed inside the full gate.
- **Wire-only reachability:** not demonstrated for F1 (see the finding).
- **Not run:**
  - the mailbox Verilator bank (inputs identical);
  - lwSRP's own suites and reversals (PR #15);
  - full parent/PP/gPTP/Yosys/builder banks;
  - the compiler-absent check;
  - any hardware.
  Physical calibration was not run, and field skips are not hardware proof.
- **Hosted evidence:** at 15:11 CEST the GitHub API reported 0 check runs and a pending combined status for this exact head. No hosted result is claimed.

## Pending manager duties

- Carry R532-5-F1 to the executor. Re-review the corrected head with all five lenses.
- Hosted `rtl-fast` / `firmware-unit` and the exact-head long gates, plus act replication.
- Builder bank and compiler-absent check (assignment 6037276691).
- Carry RESIDUE R532-5-R1/R2 to the residue checklist.
- Open the new Issue for R532-5-S1.
- Owed dev merge (F2 now in dev; F3 next), then candidate-merge validation against live dev `e21c1ca0` and post-merge containment.
- Publication of the lwSRP notes PR (#15).

## Receipts

All receipts are listed in `MANIFEST.sha256`:
- `scripts/` contains the drivers, probes, plants and runtime fetch.
- `receipts/runs/` holds final logs and `rc` files (rc file format: `<rc> <seconds>`).
- `receipts/probes/` holds the probe gtest logs.
- `receipts/size/` holds the size JSON files and runtime provenance.
- Also: `receipts/struct-sizes.txt`, `linked-size.txt`, `docs-gates.txt`, `delta-files.txt`, `mbx-input-delta.txt`, `integrity.txt` (clone byte-identical to the head, index flags clean, all four initialized gitlinks at their recorded commits and clean) and `sdk-install.log`.

R532-5 FINISHED
