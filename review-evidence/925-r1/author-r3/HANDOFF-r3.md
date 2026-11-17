# Lane 925, round 3: handoff ([A790])

Status: REVIEW READY at 5f625090; scoped verification complete with the manager-assigned #914 statement exceptions and #927 route disposition recorded below. No active helper units. The single round 3 [REVIEW READY comment](https://github.com/kebag-logic/milan-fpga/issues/925#issuecomment-6939437010) is published and verified against REVIEW-READY-COMMENT.md.

## 1. Scope

Round 3, from the manager's resume of 22:12 and its addition of 22:3x:

- R850-1 F1 (MAJOR): a change the receive filter's copy makes owes its declaration's transmission, whatever follows
  in the MRPDU.
- R850-1 F2 (MAJOR): a StreamID's latest Talker kind kept for the lifetime of its retained registrations, per
  stream, not per binding; the fallback test and plant replaced; the README aligned.
- R849-1 F1 (MINOR): the clauses (802.1Q-2018 35.1.2.1, 35.2.6 and its NOTE, Milan v1.2 5.3.8.5, the ruling
  #925 issuecomment-6930043105) and the processor's leave difference in srp/README.md's comparison.
- R849-1 F2 (MINOR): each New in turn decides, with R849-1's `r849-renew-not-recorded` plant caught by name.
- R849-1 F3 (SUGGESTION): an in-place rebind carries the latest.
- R849-1 F4 (RESIDUE): the report-local label removed from srp_mbx.cpp.

## 2. Commits (on 09a948d4, nothing pushed)

- `6e4d9c1a` the SRP change (filter hold, `stream_kinds`, the held table), tests, plants, srp/README.md
- `44265574` the memory ledger record (ctrl_plat at every point; 8x8/2if 61.0 by the owner's 2026-11-15 decision)
- `eccfe556` the Failed New test from a two-kind state; the other-interface test built at two interfaces only
- `0b1f57b3` the Failed New after an Advertise New beside the Failed; the no-latest plant
- `7a2def7c` a docstring wrap (the Python idiom gate)
- `5f625090` srp_mbx.c's ratchet line, 768/768 and 695/695 (the head)

## 3. Design

- F1: `interested_msrp` calls `hold(i)` when its copy moves a sink's `desired` (srp_mbx.c). hold() calls no lwSRP
  function, so it is safe inside the filter; the final declaration is still made by THE TRANSMIT from the final state.
- F2: `srp_sink.stream_kinds` (the walk's kinds for the StreamID whatever destination and VID) and a global table
  `srp_mbx.held[SRP_HELD_STREAMS]` of `{stream_id, interface, latest_kind}`, `held_count` live:
  - stored at a final unbinding (by null identity or by another identity) with `stream_kinds == 3`;
  - taken by the interface's next binding of the StreamID (latest and `stream_kinds = 3`);
  - released by a leave indication of either kind for it (lwSRP indicates every registration's end, its leave
    timer's too, whatever the filter answers: mrp_mad.c reg_event / on_leave_timer) and by the interface's reset.
  - Bound: each registration is an lwSRP attribute instance (> 64 B, so a medium or large block), and a StreamID is
    held only while both of its own are registered, so entries <= (MEDIUM + LARGE) / 2: 16, 32, 40, 81 by point.
    The full-table guard is unreachable with the SRP pool; a white-box test covers it (Failed, as no latest is known).

## 4. Evidence (receipts under receipts/)

| Gate | Head | Result | Receipt |
|---|---|---|---|
| test_ctrl_firmware --require-rv32 --self-test --shard 0/4 (suites) | 5f625090 | rc 0, PASS, 79 arms | firmware/fw0.log |
| shard 1/4 (control mutants) | 5f625090 | rc 0, 716 of 716 caught | firmware/fw1.log |
| shard 2/4 (AECP mutants) | 5f625090 | rc 0, 299 caught, 0 escaped | firmware/fw2.log |
| shard 3/4 (SRP mutants both counts, lwSRP pin) | 5f625090 | rc 0, 465 caught, 0 escaped (441 - 20 + 44) | firmware/fw3.log |
| fw_coverage --check | 5f625090 | rc 0, PASS (39 files); srp_mbx.c 768/768, 695/695 after its 3 exclusions | firmware/cov-check.log |
| fw_coverage --write (to read the counts) | 7a2def7c | rc 0; srp_mbx.c's line taken; the three AECP lines it also rewrites are stale at the base (round 1), not taken | firmware/cov-write-7a2def7c.log |
| R850-1 run_reproduce / run_probes / run_rebind, 1 and 2 interfaces | 7a2def7c | rc 0 each (six driver invocations, eight suite runs) | reviewers/r850-1/ |
| R849-1 r849_drive.py probes, 1 and 2 | 7a2def7c | rc 0 (22 and 23 tests); with r849-renew-not-recorded rc 1 (caught) | reviewers/r849-1/ |
| R849-1 r849_drive.py mutants, 1 and 2 | 7a2def7c | 26 caught; r849-unknown-withdraws ESCAPED: its named test is the fallback R850-1 F2 removes (the same plant text is feedback-latest-unknown-withdraws, caught) | reviewers/r849-1/ |
| feedback-latest-* and held-latest-* plants | 7a2def7c | 1 if: 21 caught (the 2 held-latest- are two-interface only); 2 if: 23 caught | plants/ |
| plat_ledger.py | worktree = 44265574 | rc 0, every point PASS | ledger/ |
| test_ctrl_memory.py | worktree = 44265574 | rc 0, 0 failures | ledger/ |
| flip_grade --check --point 1x1/1if; load_grade --check | 5f625090 | rc 0 each; identical to round 1/2 | graders/ |
| docs.yml replay (every job) | 5f625090 | 61 steps rc 0, 34 setup/hosted-only with reasons, 0 bad | workflows/docs-* |
| rtl-fast firmware-unit, changes replays | 5f625090 | 6 + 2 steps rc 0, 4 + 1 setup/hosted-only, 0 bad | workflows/rtl-fast-* |
| route exports vs round 2 | 7a2def7c | netlists equal apart from dates and the comment tree; ROM contents only; integrated scripts identical | images/ |
| plat_ledger.py and test_ctrl_memory.py, repeated on final clean clone | 5f625090 | rc 0 each, all points PASS | ledger/*-final.log |
| Release firmware vs base 16ba667d, both shapes | 5f625090 | rc 0, bios.bin and stripped ELF byte-identical | images/release-identity.txt |
| Final-head budget image relink, both shapes | 5f625090 vs 7a2def7c | rc 0, both ELFs byte-identical | images/final-budget-image-identity.txt |
| elaborate.yml replay (every job) | 5f625090 | rc 0; 10 executable steps, 36 setup/hosted-only steps not run with reasons, 0 bad; peak memory 5.9 GiB | workflows/elaborate-* |
| budget 1x1 | 7a2def7c, final image identical | rc 0; 96 groups, 0 refusals, 0/137530 share overruns; SRP and transmit rows within; same 7 backlog-owed misses | budget/1x1-1if-summary.md |
| budget 8x8-1if | 7a2def7c, final image identical | rc 1 only for #914 statement categories: 81 base, 2 ACMP item, 4 declined offer; 95 groups, 0 refusals, 0/247150 share overruns; SRP and transmit within | budget/8x8-1if-summary.md |

## 5. Run history

- 22:3x resumed after the host restart; no helper unit ran; the tree held header edits only (kept, finished).
- 23:0x-23:3x code, tests, plants; dev arms and both reviewers' scripts pass on the worktree.
- 23:2x plat_ledger FAIL (KEY at every point, 8x8/2if 61 tiles); ledger raised under the owner's 2026-11-15
  decision; plat_ledger and test_ctrl_memory PASS.
- 23:3x coverage on 44265574 failed in its run (the GTEST_SKIP the harness counts as a failure, fixed in eccfe556);
  again at 7a2def7c: rc 0, srp_mbx.c 768/768 695/695; ratchet recorded at 5f625090.
- 23:4x route exports at 7a2def7c equal round 2's apart from ROM contents at both routed shapes.
- budget 1x1 unit started on 80-87 at 7a2def7c; 8x8/1if on 88-95.
- Usage-limit resume: tree clean at 5f625090, six commits ahead. Both budget units were active under their 10 GiB caps, with no rc yet; neither was counted as passed. All completed firmware and docs units have recorded rc 0. No round 3 REVIEW READY posted (five #925 comments, latest is the manager ruling).
- Release firmware rebuilt at 5f625090 in a fresh clone: bios.bin and stripped ELF identical to 16ba667d at both shapes.
- Final-head platform ledger and memory controls repeated in that clean clone: rc 0. Both budget images relinked at 5f625090 and compare byte-identical to the measured units' 7a2def7c images.

- Final-head elaborate workflow replay started during the budget runs to cover the memory-planning change. The existing pinned environment is reused; each job starts from a fresh clone and every run step is verified against its rc or a stated hosted-only reason.

## 6. Changes by file and line (5f625090)

| File:line | Reason |
|---|---|
| `sw/firmware/ctrl/srp/srp_mbx.c:195` | Correct clauses and document the manager ruling. |
| `sw/firmware/ctrl/srp/srp_mbx.c:210` | Find and release ordering retained for an unbound StreamID; either registration ending releases it. |
| `sw/firmware/ctrl/srp/srp_mbx.c:398` | Preserve transmission work when the receive filter changes desired. |
| `sw/firmware/ctrl/srp/srp_mbx.c:659` | Carry stream order through another binding or an in-place replacement; take a retained entry. |
| `sw/firmware/ctrl/srp/srp_mbx.c:688` | Keep the order after the final binding ends while both registrations remain. |
| `sw/firmware/ctrl/srp/srp_mbx.c:916` | The registrar walk records StreamID-wide presence independently of the binding destination/VID. |
| `sw/firmware/ctrl/srp/srp_mbx.c:954` | Clear the walk accumulator before rebuilding it. |
| `sw/firmware/ctrl/srp/srp_mbx.c:1104` | Reset discards retained entries only for its own interface. |
| `sw/firmware/ctrl/srp/srp_mbx.h:35` | Binding copy of the StreamID registrations. |
| `sw/firmware/ctrl/srp/srp_mbx.h:119` | Bounded per-stream retained ordering, allocated after the frame buffers. |
| `sw/firmware/ctrl/srp/README.md:246` | Rule, clauses, retained-order lifetime and test scope. |
| `sw/firmware/ctrl/srp/README.md:496` | Record the release processor leave difference. |
| `sw/firmware/ctrl/test/srp_mbx.cpp:1383` | Reference walk now checks stream_kinds. |
| `sw/firmware/ctrl/test/srp_mbx.cpp:1815` | Replacement, rebinding, lifetime, interface and idle-timer regressions. |
| `sw/firmware/ctrl/test/srp_feedback.hpp:81` | Inspect Listener Ready frames alongside the ACMP wire response. |
| `sw/firmware/ctrl/test/srp_kind_mutants.py:41` | Named plants for each new rule and corrected clause record. |
| `sw/firmware/gtest/coverage.ratchet:36` | Record 768/768 lines and 695/695 branches; no exclusion added. |
| `sw/litex/ctrl_memory.py:267` | Raise the measured 8x8/2if ledger entry to 61.0 under the owner rule. |
| `sw/litex/ctrl_memory_ledger.py:36` | Record measured platform sizes and test the new entry with refusal half a tile above. |
| `sw/litex/test_ctrl_memory.py:232` | Keep boundary fixtures capable of reaching half a tile above the raised entry. |
| `docs/design/SPLIT_CONTROL_MEMORY.md:148` | Record memory growth, ROM by shape and S14 debt. |
| `sw/firmware/ctrl/plat/README.md:110` | Keep platform memory claims aligned with measurements and owner rule. |

## 7. Checks and their planted defects

All listed plants are caught at both interface counts except the two `held-latest-` plants, which require two interfaces. See receipts/plants/ and the complete firmware SRP shard. The existing reference-walk check is extended; the table includes every new check and its failing words.

| Plant | Named check | Failing words |
|---|---|---|
| `feedback-latest-failed-first` | `SrpTalkerKinds.AnAdvertiseNewReplacesARegisteredFailedWithinAJoinTime` | an Advertise New replaces the registered Failed |
| `feedback-latest-walk-failed-first` | `SrpTalkerKinds.AnAdvertiseNewReplacesARegisteredFailedWithinAJoinTime` | an Advertise New replaces the registered Failed |
| `feedback-latest-advertise-only` | `SrpTalkerKinds.AFailedNewReplacesARegisteredAdvertiseWithinAJoinTime` | a Failed New replaces the registered Advertise |
| `feedback-latest-decides-unregistered` | `SrpTalkerKinds.LeaveOfEitherKindLeavesTheOtherDeciding` | the latest leaves: the other decides |
| `feedback-latest-earliest-decides` | `SrpTalkerKinds.CoincidentRegistrationsInOneMrpduFollowTheirOrder` | Failed then Advertise in one MRPDU |
| `feedback-latest-not-carried` | `SrpTalkerKinds.ABindingMadeLaterTakesTheLatestFromAnyBindingOfTheStream` | the shared declaration stays Ready, not ReadyFailed |
| `feedback-latest-matching-only` | `SrpTalkerKinds.ABindingMadeLaterTakesTheLatestFromAnyBindingOfTheStream` | a later binding takes the latest registration |
| `feedback-latest-renew-not-recorded` | `SrpTalkerKinds.EachNewInTurnDecidesWhileBothAreRegistered` | a Failed New beside the Advertise decides again |
| `feedback-latest-unknown-withdraws` | `SrpTalkerKinds.AFullHeldTableHoldsNothingMore` | no latest known: Failed |
| `feedback-latest-not-carried-in-place` | `SrpTalkerKinds.ABindingMadeLaterTakesTheLatestFromAnyBindingOfTheStream` | one in place too |
| `feedback-latest-filter-holds-nothing` | `SrpTalkerKinds.AReplacementBeforeAMessageThatChangesNothingIsDeclaredWithinAJoinTime` | a New before a message that changes nothing |
| `feedback-latest-filter-holds-nothing-acmp` | `SrpFeedback.AnAdvertiseNewBeforeAnUnchangedDomainUpdatesBothWireViews` | Listener Ready on the wire within a JoinTime |
| `feedback-latest-not-held` | `SrpTalkerKinds.AFinalUnbindingKeepsTheLatestWhileBothStayRegistered` | a final unbinding keeps the latest registration |
| `feedback-latest-held-not-taken` | `SrpTalkerKinds.AFinalUnbindingKeepsTheLatestWhileBothStayRegistered` | a final unbinding keeps the latest registration |
| `feedback-latest-held-for-another-stream` | `SrpTalkerKinds.AFinalUnbindingKeepsTheLatestWhileBothStayRegistered` | another StreamID takes none of it |
| `feedback-latest-held-with-one-kind` | `SrpTalkerKinds.AHeldStreamEndsWithEitherRegistrationOrAReset` | one kind registered holds nothing |
| `feedback-latest-held-past-a-leave` | `SrpTalkerKinds.AHeldStreamEndsWithEitherRegistrationOrAReset` | a registration's end or a reset ends the hold |
| `feedback-latest-held-past-a-reset` | `SrpTalkerKinds.AHeldStreamEndsWithEitherRegistrationOrAReset` | a registration's end or a reset ends the hold |
| `held-latest-any-interface` | `SrpTalkerKinds.AStreamIsHeldForItsOwnInterface` | another interface's binding takes none of it |
| `held-latest-reset-any-interface` | `SrpTalkerKinds.AStreamIsHeldForItsOwnInterface` | another interface's reset leaves it |
| `feedback-latest-stream-kinds-kept` | `HeldRegistrationsAreWhatAWalkCopiesAfterEveryStep` | holds what a walk copies |
| `feedback-latest-filter-failed-first` | `SrpFeedback.AWithdrawalInsideOneMrpduRetainsTheLatestKind` | the latest kind precedes the withdrawal |
| `feedback-latest-acmp-failed-first` | `SrpFeedback.AdvertiseNewOverARegisteredFailedUpdatesTheSettledWireView` | current kind reaches ACMP |

Reviewer plant `r849-renew-not-recorded` is also caught by that exact name at both interface counts in `receipts/reviewers/r849-1/mutants-if*.log` and in the probe runs. `r849-bind-copy-skipped-for-self` is caught too. The reviewer driver still selects removed test `ABindingThatSawNeitherRegistrationTakesFailedFirst` for `r849-unknown-withdraws`, so its unchanged legacy campaign reports that selection as an escape. Its identical production mutation is now checked by `feedback-latest-unknown-withdraws` against the unreachable full-table guard; no retained-registration exception remains.

## 8. Timing and scope of the evidence

The R850-1 reproductions observe the replacement declaration at model delay 0 ms for both directions, with and without the trailing Domain, at each interface count. The phase sweep covers 200 phase/direction combinations per interface count and the independent event-order model covers 216 traces per count. Those host-model checks and the idle-timer regressions pass within the configured join interval; they do not measure physical acceptance. The Listener Ready within one second bench check remains the manager's gating run, outside this assignment's permitted access.

The receive filter returns before lwSRP processes an ignored unbound Talker (`third_party/lwSRP/src/core/mrp_mad.c:998`), so an ignored New cannot silently change a held stream's registrations. Timer dispatch snapshots the registration state before returning (`sw/firmware/ctrl/srp/srp_mbx.c:110`), so final unbinding sees the post-expiry `stream_kinds`. No submodule change is needed.

Routes remain misses at the base, owed to #927 under the manager ruling. Eight historical per-directive/base signoff receipts are copied into `receipts/routes-prior/`; no route was run in round 3. `receipts/images/round2-vs-round3-route-exports.txt` records equal netlists apart from generated comments and equal integrated scripts at the two routed shapes. ROM contents differ. RAMB36 allocations at those shapes remain 43.0 and 56.0; no new routed LUT/FF area is claimed.

Historical route minima over all recorded corners, ns (all are misses at the base, owed to #927):

| Shape / directive | WNS | WHS | Receipt |
|---|---:|---:|---|
| 1x1-AltSpreadLogic_high | +0.177 | +0.023 | `receipts/routes-prior/1x1-AltSpreadLogic_high.txt` |
| 1x1-ExtraPostPlacementOpt | +0.024 | +0.036 | `receipts/routes-prior/1x1-ExtraPostPlacementOpt.txt` |
| 1x1-ExtraTimingOpt | +0.008 | +0.023 | `receipts/routes-prior/1x1-ExtraTimingOpt.txt` |
| 8x8-AltSpreadLogic_high | +0.215 | +0.014 | `receipts/routes-prior/8x8-AltSpreadLogic_high.txt` |
| 8x8-ExtraPostPlacementOpt | +0.011 | +0.034 | `receipts/routes-prior/8x8-ExtraPostPlacementOpt.txt` |
| 8x8-ExtraTimingOpt | +0.171 | +0.014 | `receipts/routes-prior/8x8-ExtraTimingOpt.txt` |
| base-1x1-ExtraPostPlacementOpt | +0.208 | +0.014 | `receipts/routes-prior/base-1x1-ExtraPostPlacementOpt.txt` |
| base-1x1-ExtraTimingOpt | +0.260 | +0.014 | `receipts/routes-prior/base-1x1-ExtraTimingOpt.txt` |

## 9. Final CPU measurements and disposition

`python3 -B tb/verilator/ctrl_service_budget/run.py --point <point> --build-dir <dir> --record-budget-findings --record-share-findings --jobs 7`, at `1x1` and `8x8-1if`: 96/95 groups, zero refusals and zero share overruns in 137530/247150 work passes. All SRP and THE TRANSMIT rows are within bounds; SRP record apply peaks 237.99/222.20 us against 280 us, and timer-driven MRPDU response peaks 1.87123/2.62353 ms against the measured row's 20 ms bound. No late, absent or unresolved timer work; join intervals 189.053–190.070 / 188.316–190.122 ms against 181–239 ms. Both shapes retain the same seven pre-existing backlog-owed misses, with no new missed path.

The 1x1 run is rc 0. The 8x8 run is rc 1 only for #914's per-shape statements under #925 issuecomment-6908876793: 81 polls-base, two ACMP-item and four declined-offer records, versus 77/3/4 in round 2. Their peaks changed from 244.99/66.56/25.22 us to 270.00/63.91/21.96 us; measurement + 5%, rounded upward to 5 us, gives 285/70/25 us, against the existing 225/55/20 us statements. These remain #914's statement work; no approved bound or source cost statement is changed here. Every measured cost delta and its rounded value is recorded in the packet's two budget summaries, including decreases and costs not directly staged by these groups.

| Measured item | 1x1/1if round 2 -> round 3, us | Rounded new value, us | 8x8/1if round 2 -> round 3, us | Rounded new value, us | Existing statement, us |
|---|---:|---:|---:|---:|---:|
| SRP record apply | 250.78 -> 237.99 | 250 | 218.16 -> 222.20 | 235 | 280 |
| One MRPDU build | 560.00 -> 514.50 | 545 | 427.65 -> 424.73 | 450 | 735 |
| Polls base | 213.22 -> 190.32 | 200 | 244.99 -> 270.00 | 285 | 225 |
| ACMP item | 43.55 -> 49.22 | 55 | 66.56 -> 63.91 | 70 | 55 |
| ACMP declined offer | 13.69 -> 17.11 | 20 | 25.22 -> 21.96 | 25 | 20 |

The larger existing statements for SRP's record and THE TRANSMIT remain conservative. The table's rounded values are the rule applied to these runs, not a silent reduction of statements that also cover other arms. The complete cost table is in each summary; no cost with a nonzero measured delta is omitted there.

Receipts: `receipts/budget/1x1-1if-summary.md`, `8x8-1if-summary.md`, `comparison-audit.txt`, both complete `*-table.md` row tables, both full run logs, and the `*-artifacts.txt` size/SHA-256 manifests. These record all seven backlog misses and all 87 statement records without suppression. The manifests identify the round 2 comparison inputs too. `receipts/INDEX.md` is generated from the files present.

Completion: the budget units have recorded rc 0/1 as above and the elaboration replay rc 0; no unit is left running. The final source tree is clean at 5f625090. No push, PR edit, merge, route, or bench operation was performed in this resume. Corrected-head review and the physical acceptance run remain the manager's next steps.

Publication: exactly one round 3 `[A790] REVIEW READY` comment at the link above. Its body matches the packet. The manager owns the push, PR update and evidence archive.
