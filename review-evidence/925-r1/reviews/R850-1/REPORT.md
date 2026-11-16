[R850] NEGATIVE - exact head 09a948d46413ef3b3ab0fa11bf97c06323f9051f

Round R850-1, external independent review of issue #925 / PR #932. Two MAJOR findings remain. All five lenses were applied; none is clean because both findings cross the protocol, architecture, robustness, test and documentation contracts. No wording-only finding is promoted to a negative verdict.

Reviewed tree: a7ff40db6afec61b93243ede79af62dd9efd8cb7. Source delta: 16ba667d5fdb7b599b9d9459958fd0d7bb6bbdff to the exact head above, eleven files. The three implementation commits are followed by the no-file-change merge of 70f4056f384e12520ccae254fe26f6286fd39db6. HEAD and 1be0a6c4 have identical trees; 70f4056f and 16ba667d have identical trees.

**F1 - MAJOR - Conformance, RTL, Robustness, Tests, Docs - A trailing message loses the work needed to transmit the new Listener kind.**

Artifacts: sw/firmware/ctrl/srp/srp_mbx.c:357-369 and :899-910; sw/firmware/ctrl/test/srp_mbx.cpp:1855-1876; sw/firmware/ctrl/srp/README.md:251-252. The relevant architectural dependency is the unchanged transmit scheduler at srp_mbx.c:1243-1292.

Authority/evidence: [Issue #925](https://github.com/kebag-logic/milan-fpga/issues/925) requires the latest registered Talker kind to determine the declaration. Its [review-ready contract](https://github.com/kebag-logic/milan-fpga/issues/925#issuecomment-6929001329), the README and the new executable expectations claim Ready within one JoinTime. IEEE 802.1Q-2018 35.2.4/35.2.6 supply the scoped declaration/replacement model; Milan 4.3.3 and 5.5 govern the Listener and ACMP views.

A bound stream has a registered Failed and an AskingFailed declaration. After its transmissions become idle, receive an Advertise New followed by an unchanged Domain JoinIn in the same valid MRPDU. The filter for the Domain processes the preceding Talker event and writes desired=Ready and feedback_kind=Ready. The final registrar snapshot then compares Ready with Ready, sees no change and never calls hold(). New does not itself move this passive Talker Applicant into transmit work. The new Listener declaration waits for unrelated scheduled work.

The minimal reproduction receives the PDU at model time 1400 ms:
- With the trailing Domain: desired=2 and feedback=2, but declared=1 after 190 ms; the first Ready frame appears after 600 ms.
- Without that trailing message: the first Ready frame appears immediately.
- The reverse change also takes 600 ms with the trailing message.
- Both interface counts reproduce these results.
- The composed ACMP probe successfully queries GET_RX_STATE after 190 ms: REGISTERING_FAILED is clear while the Listener declaration remains AskingFailed.

Receipts: [reproduce-if1-srp_mbx.cpp.log](reproduce-if1-srp_mbx.cpp.log), [reproduce-if2-srp_mbx.cpp.log](reproduce-if2-srp_mbx.cpp.log), [reproduce-if1-test_acmp_mbx.cpp.log](reproduce-if1-test_acmp_mbx.cpp.log), [reproduce-if2-test_acmp_mbx.cpp.log](reproduce-if2-test_acmp_mbx.cpp.log). The wider phase sweep fails 124 of 200 direction/phase combinations per interface count; the independent 216 three-event order traces pass.

Impact: a legitimate multi-message MRPDU suppresses timely Listener output and leaves ACMP and the declared reservation inconsistent beyond the promised JoinTime. This is a scheduling omission, not a changed timer value. The observed 600 ms is not itself proof that the separate one-second physical acceptance fails.

Required outcome: retain declaration-transmission work when observation updates desired inside the receive filter, including an unchanged or ignored trailing message. Preserve atomic replacement, retained withdrawal ordering and final-state-only declarations within one MRPDU. Add regressions that reach an idle join timer and inspect both wire views. Update the timing/conformance claims only to what the corrected behavior proves.

Verification: run_reproduce.py must pass at one and two interfaces, including its no-trailing-message controls; run_probes.py must pass both the phase sweep and ordered-event model. The current negative probes fail by assertions, not compile errors.

**F2 - MAJOR - Conformance, RTL, Robustness, Tests, Docs - Rebinding loses the order of registrations that are still present.**

Artifacts: sw/firmware/ctrl/srp/srp_mbx.c:196-200, :608-637; sw/firmware/ctrl/test/srp_mbx.cpp:1945-1955; sw/firmware/ctrl/test/srp_kind_mutants.py:59-61; sw/firmware/ctrl/srp/README.md:253-256.

Authority/evidence: #925's most-recent-registration rule and the requested later-binding case. The manager's [scope decision](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6904832963) and [subsequent ruling](https://github.com/kebag-logic/milan-fpga/issues/925#issuecomment-6908876793) provide no exception for a retained registration after final unbind.

Register Failed, then Advertise New for the same bound stream. Ready is established and both registrations remain. Unbind the final sink, then bind it again without any intervening Talker change. The per-binding latest_kind has been destroyed, although lwSRP retains both attributes. The new binding has registered_kinds=3, latest_kind=0, desired=1, declared=1 and Failed feedback. The actual last registration is still Advertise.

Receipts: [rebind-if1.log](rebind-if1.log), [rebind-if2.log](rebind-if2.log). Both fail the desired, declared and feedback assertions. Existing positive tests confirm that retaining another binding preserves the order.

Impact: an unchanged available stream is presented as Failed solely because the last local binding was removed and recreated. The old priority defect remains for this order. This is an inherited limitation left unresolved by the new rule, not a newly introduced regression. It was candidly disclosed in the PR and REVIEW READY, but that disclosure does not amend the frozen scope. The new fallback test and its fault plant enforce the exception instead of checking the requested latest-kind behavior.

Required outcome: keep enough ordering information for the lifetime of the retained registrations, or obtain an explicit public maintainer decision changing this case's scope. Until then it remains an open finding. Align the test, plant and authoritative documentation with that outcome.

Verification: run_rebind.py must preserve Ready and Advertise feedback across final unbind/rebind at both interface counts, while still handling either kind leaving, registration expiry/reset and a binding to another identity. Keep the existing shared-binding positive controls.

**Reviewer-owned coverage ledger**

The RTL lens includes firmware architecture, state lifetime, scheduling and interface consistency; unchanged HDL does not exempt those changes.

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN, F1/F2 | #925 body and public decisions; srp_mbx.c:192,357,586,880; pinned lwSRP mrp_mad.c:617,990; release KL_srp_listener_fsm.sv:473,1148; wire reproduction receipts | R850-1 | 09a948d46413ef3b3ab0fa11bf97c06323f9051f |
| RTL | UNCLEAN, F1/F2 | srp_mbx.h:33; srp_mbx.c:412,608,899,1006,1243; ctrl_app_srp.c:89-110; raw eleven-file diff and unchanged mailbox/RTL/gitlinks; memory ledger | R850-1 | 09a948d46413ef3b3ab0fa11bf97c06323f9051f |
| Robustness | UNCLEAN, F1/F2 | srp_mbx.c receive/filter/snapshot/bind/reset paths; SrpFeedback existing withdrawal/reset/refusal tests; 216 ordered-event traces and 200 phase cases per interface count; final-unbind reproduction | R850-1 | 09a948d46413ef3b3ab0fa11bf97c06323f9051f |
| Tests | UNCLEAN, F1/F2 | srp_mbx.cpp:1803-1955; srp_feedback.hpp:112-144; srp_kind_mutants.py; srp_mutants.py:111; focused-if1/2.log and all named mutant receipts; coverage.ratchet and published cov.log | R850-1 | 09a948d46413ef3b3ab0fa11bf97c06323f9051f |
| Docs | UNCLEAN, F1/F2 | srp/README.md:245-259,480-484; SPLIT_CONTROL_MEMORY.md:135-147; PR body and #925 REVIEW READY; archived author receipts and their hash manifest | R850-1 | 09a948d46413ef3b3ab0fa11bf97c06323f9051f |

**Execution and evidence**

Independent focused execution:
- run_focused.py: rc 0 at both interface counts. Each runs all 80 srp_mbx tests at 1x1, all 21 SrpFeedback tests at 1x1, six SrpTalkerKinds tests at 8x8, and all 21 SrpFeedback tests at 8x8. Thus the eight new tests execute at both shapes and both interface counts.
- All ten new plants are caught by their named assertions at both interface counts, including the first plant restoring Failed-first precedence. The relocated failed-listener-ready plant is also caught: 22 catches, no escape. Raw logs are in mutations-if1/ and mutations-if2/.
- run_probes.py: rc 1 at each interface count, for F1's timer-phase test only; the 216 ordered-event traces pass. These traces check final kind and absence of wire flapping, and distinguish a real gap from continuous replacement.
- run_reproduce.py: rc 1 at each interface count, for F1's adapter and composed ACMP assertions.
- run_rebind.py: rc 1 at each interface count, for F2.
- flip_grade.py --check --point 1x1/1if and load_grade.py --check: rc 0. These re-evaluate the checked-in cost model; they are not fresh CPU measurements. Every held row is within bound, including last=136.65/140 ms and txL=48.58/49 ms; load is 0.517/0.514 against 0.70.
- git diff --check 16ba667d HEAD: rc 0.

Public source evidence was examined at immutable archive [aedb770f, review-evidence/925-r1](https://github.com/kebag-logic/milan-fpga/tree/aedb770f03cab800b4623c0c13fde672ce26f670/review-evidence/925-r1), using author-r1/receipts and author-r2/receipts only. All 529 receipt files match their published hashes; see public-evidence-integrity.json. This checks artifact integrity, not the truth of every assertion in a log.

The firmware receipts record suites PASS, control 716/716, AECP 299 and SRP 441 catches. The coverage receipt reports srp_mbx.c at 741/741 lines and 671/674 raw branches, 100% after the three standing exclusions, matching 671/671 in the ratchet. No exclusion changed here. Full coverage was inspected, not rerun.

The 1x1 CPU budget receipt records rc 0, 96 groups, zero refusals and no pass over the share among 129,813 passes. The 8x8/1if receipt records rc 1 from the polls-base, ACMP-item and declined-offer STATED lines: the per-shape statements assigned to #914 by the public ruling. Both report the seven pre-existing backlog-owed probe misses. SRP's measured record and walk costs are within their existing statements. No CPU bank was rerun.

The memory receipts support ROM +88 B at 1x1 and +32 B at 8x8. The four ctrl_plat sizes are 17,536 / 19,072 / 18,240 / 20,416 B. The 8x8/2if platform remains 60.5 RAMB36, with 114,288 B SRAM; 8x8/1if remains 56.0. The [2026-11-15 loose-BRAM decision](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6892332745) governs entries; fit and timing obligations remain. No memory cap was tightened or silently waived by this review.

The release-image hashes support identical loadable bios.bin and stripped ELF at both configurations. The route and budget relink receipt shows four identical image hashes between a9f0dbc0 and 09a948d4. The only intervening changes are a test line wrap and coverage counts. These are author measurements, not independent rebuilds.

The workflow receipts cover rtl-fast, elaborate and docs steps on clean clones. The earlier Python long-line failure at a9f0dbc0 was corrected and its docs job rerun at identical-tree 1be0a6c4. Hosted-only installation, recording and upload steps marked NOT RUN are not executed evidence. The sweep records 65 suites across four shards: 15/15, 14/17, 17/17, 16/16, with the three incomplete/failed shard-1 suites subsequently passing individually. The original gptp_shadow lifecycle timeout and two wall-clock cuts are not counted as passes. Cut runs without return codes are excluded.

The route receipts remain misses at the base, owed to #927, not findings here. Slow WNS / Fast WHS in ns: 1x1 +0.024/+0.036, +0.008/+0.023, +0.177/+0.023; 8x8 +0.011/+0.034, +0.171/+0.014, +0.215/+0.014 for the three recorded directives. The base's measured 1x1 holds are +0.014. No route was rerun.

The scoped clause reconstruction used REQUIREMENTS.md, the issue's specified authorities, the mailbox/interface documents, the pinned lwSRP contracts and the release processor. The JoinIn/JoinMt replacement distinction also agrees with the [IEEE working-group explanation of 35.2.6](https://www.ieee802.org/1/files/public/docs2011/at-cummings-multi-talkers-one-stream-0311-v2.pdf). That historical explanatory document is corroboration, not a substitute for the 2018 standard.

**Prior public findings and independence**

The independent verdict and ledger were written before reading the PR's merged public discussion. At the inspected snapshot, that discussion contained only the two review-start notices, with no prior review findings to clear or retain. No other reviewer's report was read. Replica F18 is fixed for the isolated New case, as the positive controls show; the broader requested behavior remains uncleared by F1/F2. No private author material or management checkout was read. No source fix, commit, push or GitHub write occurred.

**Integrity, reproduction and remaining duties**

integrity.json verifies raw blob bytes, executable/symlink modes and the entire stage-zero index against HEAD for the superproject and all five required initialized submodules. All match, with no errors: 1,633 superproject entries and 1,238 submodule entries. The external gitlink is unchanged and intentionally uninitialized. Every build, extracted receipt and probe copy is under scratch/. The source tree was never modified.

Reproduce from this packet, with REPO set to the detached source clone:

    python3 -B run_focused.py --repo "$REPO"
    python3 -B run_probes.py --repo "$REPO" --interfaces 1
    python3 -B run_probes.py --repo "$REPO" --interfaces 2
    python3 -B run_reproduce.py --repo "$REPO" --interfaces 1
    python3 -B run_reproduce.py --repo "$REPO" --interfaces 2
    python3 -B run_rebind.py --repo "$REPO" --interfaces 1
    python3 -B run_rebind.py --repo "$REPO" --interfaces 2
    python3 -B verify_integrity.py --repo "$REPO"
    python3 -B audit_public_receipts.py --repo "$REPO"

The focused driver runs two independent workers, each with eight compilation jobs; paired probes were also capped at sixteen in total. All foreground executions completed. No broad parent, processor, synthesis or builder bank, workflow replica, hardware access or shared installation was run.

Physical calibration NOT RUN; field skips and host-model timing are not hardware proof. The one-second bench scenario remains pending. #929, the two known 8x8 startup failures and host interruptions are not new findings.

There is no manager source bank at this head. Source evidence above is the author's published execution plus this review's focused checks. Hosted execution was not independently adjudicated here; hosted/act acceptance belongs to the manager. The manager must obtain corrected-head re-review or explicit scope resolution, complete the current-dev candidate builder/native banks against live dev (6b66f66d89cf25d2717687bcc2c3bf617685a99a as supplied), link its receipts, complete bench acceptance and the remaining review bar, then follow authorized merge and post-merge containment. This report does not validate that future candidate or authorize a merge.

R850-1 FINISHED
