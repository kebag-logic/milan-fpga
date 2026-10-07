[A560]

# F4 handoff

Relates to #665. Branch: `665-f4-srp` -> `dev`.
Round 8 REVIEW READY at `a6e6916826448f81de2b779ca61a87a9f8c47278`.
All 102 final recorded invocations exit 0; all validation jobs have finished. No review verdict or finding
closure is claimed. The Round 7 history below describes that earlier head.

## Round 8

Assignment: [issue comment 6045716528](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6045716528).
Verified the remote URL and clean published Round 7 head against PR #690 before
fetching the assigned dev commit. The `--no-ff` merge is
`a6e6916826448f81de2b779ca61a87a9f8c47278`, with ordered parents:

- `f74b9403b330ce316eeec6f724846f16def98443` (Round 7);
- `d8b355fe0f41d49dca6cae1cd8b3826e2edde364` (assigned dev, F3 merged).

The existing configured identity was used, with a one-line subject and no
body or trailers. No push, PR edit, rebase or amend was performed.
This remains partial work, **Relates to #665**. Reviewers own new-head verdicts,
finding closure and the lens ledger; earlier positive verdicts are historical.

### Round 8 changes with file locations

Imported F3 code, mailbox contract, RTL and tests are the assigned dev content.
The Round 8 resolutions and additions are listed here; no new mailbox or RTL
change was needed beyond that import.

| File:line | Change |
| --- | --- |
| `sw/firmware/ctrl/app/ctrl_app_srp.c:12` | Keep optional ACMP enabled when SRP opens its receive/filter and IRQ bits beside ADP, MAAP, events and tick. |
| `sw/firmware/ctrl/app/ctrl_app.h:17` | State attach order; three disjoint one-shot slot ranges remain, while SRP shares the tick. |
| `sw/firmware/ctrl/app/ctrl_app.h:69` | Retain the three-module bound separately; derive four-module `CTRL_APP_PASS_MAX` with shared event reads counted once. |
| `sw/firmware/ctrl/srp/srp_bounds.h:1` | Explicit worst-path SRP mailbox transaction bound, including refused receive and the two transmit opportunities per poll. |
| `sw/firmware/ctrl/test/test_acmp_mbx.cpp:936` | Actual SRP fixture attachment and full-ring stimulus in F3's U6/F6 suite, with separate SRP and existing ACMP/MAAP progress checks. |
| `sw/firmware/ctrl/test/test_acmp_mbx.cpp:1032` | Three/four bound equations and measured per-pass check. |
| `sw/firmware/ctrl/test/test_acmp_mbx.cpp:1081` | Idle wait wakes only for an SRP record, followed by receipt; exact four-channel mask and attach/tick order at line 1145. |
| `sw/firmware/ctrl/mbx/mbx.c:117` and `mbx.h:82` | Import F3's bound-talker filter API while retaining F4's receive-readiness API; no further mailbox change. |
| `sw/firmware/ctrl/test/ctrl_arms.py:37` | Retain F3's ACMP, two-interface, differential and saved-state arms alongside F4's lwSRP pin and debug behavior. |
| `sw/firmware/ctrl/test/ctrl_reuse.py:33` | Import the pinned processor ACMP stimulus slices while retaining F4 reuse checks. |
| `sw/firmware/gtest/README.md:167` | Keep both lanes' evidence and inherited exclusion rules; the merge adds no new exception. |
| `sw/firmware/ctrl/test/srp_arms.py:38` | F3 NVM include and the shared U6/F6 arm with actual SRP, for both interface counts. |
| `sw/firmware/ctrl/test/test_ctrl_firmware.py:127` | Include four-module arm in coverage and positives; preserve both inherited campaign slicing interfaces and run new plants at IF=1 as well. |
| `sw/firmware/ctrl/test/ctrl_mutants.py:541` | Preserve F3's complete naming audit and table; reuse scratch compilation locations without changing plant assertions. |
| `sw/firmware/ctrl/test/acmp_review_mutants.py:1` | Existing F3 three-module bound plants follow its renamed macro. |
| `sw/firmware/ctrl/test/srp_mutants.py:611` | Six new behavior-checked four-module plants, each exercised at IF=1/2. |
| `sw/firmware/ctrl/test/srp_app.cpp:29` | Initialize the merged F3 application configuration shape. |
| `sw/firmware/ctrl/test/ctrl_image.py:1` | Preserve F3's linked auditor unchanged from assigned dev. |
| `sw/firmware/ctrl/test/ctrl_srp_image.py:1` | Keep F4's linked auditor under a distinct name; require retained ACMP code/storage as well as SRP. |
| `sw/firmware/ctrl/test/ctrl_image.c:60` | Supply ACMP configuration/environment in the four-module linked fixture. |
| `sw/firmware/ctrl/README.md:120` | Composition, bounds, test scope and separate linked-image recipes. |
| `sw/firmware/ctrl/srp/README.md:38` | Refused counts attempts; line 64 matches the header's “completes or expires”; F3 presence and remaining binding-port integration are explicit. |
| `docs/design/MAILBOX_SPLIT.md:715` | Four-module bounds table and conditional T_svc statement. |
| `sw/firmware/gtest/coverage.ratchet:5` | Repository generator combines F3/F4 coverage into 22 fully covered files; inherited exclusions retained. |

### Round 8 tests and planted defects

`AcmpMailbox.U6AdpAcmpAndMaapShareTheLoopOnDisjointSlotsWithEveryChannelOpen`
and `AcmpMailbox.F6WithMaapComposedEveryPassStaysWithinTheThreeWayBound`
retain their F3 names and run in both the original three-module arms and the
new four-module arms. The unchanged three-module assertions remain active.
The following plants compile and must fail their specified observable.

| Test / check | Plant | Interface counts |
| --- | --- | --- |
| U6 exact IRQ mask | `four-way-srp-irq-missing` | 1, 2 |
| U6 idle SRP-only wake and receipt | `four-way-srp-wake-missing` | 1, 2 |
| U6 exact receive/filter enable | `four-way-acmp-enable-lost` | 1, 2 |
| U6 rejects an unrelated enabled IRQ | `four-way-unbound-irq-enabled` | 1, 2 |
| F6 bound includes the SRP pass | `four-way-bound-drops-srp` | 1, 2 |
| F6 shared event reads counted once | `four-way-bound-duplicates-events` | 1, 2 |

The full control table contains 469 plants and the SRP table 108, plus two
pin-refusal controls. All six new plants run again at IF=1. The complete mapping
of test, plant, modified artifact and required failure is `ROUND8-TESTS.md`.
The full campaign exits 0: all 469 control and 108 SRP plants, the six
additional IF=1 plants and both pin controls are caught.

The four-module transaction bounds are 3,128 accesses at IF=1 and 3,977 at IF=2.
`ACMP_MBX_PASS_MAX` already includes ADP; adding MAAP and SRP removes two extra
copies of the eight shared event-record reads. At the assumed 1 us/access,
only IF=1's event envelope fits 10 ms. These are conditional host transaction
bounds, excluding CPU work and integrator callbacks. The separate SRP backlog
can wait behind owed output and events; the ACMP pass counts are not a claimed
SRP delivery deadline. Disjoint ADP/ACMP/MAAP slots and SRP's shared tick are
checked together in U6.

### Round 8 coverage table

The repository generator wrote the ratchet, and an independent `--check`
passes. No new exclusion was introduced by the merge; the inherited F3/F4
exclusion rules are retained.

| File | Lines | Branches | After existing exclusions |
| --- | ---: | ---: | --- |
| `sw/firmware/ctrl/acmp/acmp.c` | 734/734 | 342/342 | 100% / 100% |
| `sw/firmware/ctrl/acmp/acmp_mbx.c` | 73/73 | 26/26 | 100% / 100% |
| `sw/firmware/ctrl/acmp/acmp_nvm.c` | 38/38 | 10/10 | 100% / 100% |
| `sw/firmware/ctrl/adp/adp.c` | 204/204 | 95/95 | 100% / 100% |
| `sw/firmware/ctrl/adp/adp_mbx.c` | 83/83 | 38/38 | 100% / 100% |
| `sw/firmware/ctrl/app/ctrl_app.c` | 42/42 | 40/40 | 100% / 100% |
| `sw/firmware/ctrl/app/ctrl_app_srp.c` | 12/12 | 8/8 | 100% / 100% |
| `sw/firmware/ctrl/loop/ctrl_loop.c` | 101/101 | 62/62 | 100% / 100% |
| `sw/firmware/ctrl/maap/maap.c` | 209/209 | 140/140 | 100% / 100% |
| `sw/firmware/ctrl/maap/maap_csr.c` | 39/39 | 18/18 | 100% / 100% |
| `sw/firmware/ctrl/maap/maap_mbx.c` | 98/98 | 60/60 | 100% / 100% |
| `sw/firmware/ctrl/mbx/mbx.c` | 189/189 | 74/74 | 100% / 100% |
| `sw/firmware/ctrl/mbx/mbx_wire.h` | 15/15 | 12/12 | 100% / 100% |
| `sw/firmware/ctrl/plat/mbx_plat_mmio.c` | 10/10 | 0/0 | 100% / 100% |
| `sw/firmware/ctrl/port/ctrl_debug.c` | 19/19 | 6/6 | 100% / 100% |
| `sw/firmware/ctrl/port/ctrl_pool.c` | 99/99 | 60/60 | 100% / 100% |
| `sw/firmware/ctrl/port/shlan_port.c` | 22/22 | 6/6 | 100% / 100% |
| `sw/firmware/ctrl/srp/srp_mbx.c` | 469/469 | 438/438 | 100% / 100% |
| `sw/firmware/ctrl/wire/wire.h` | 10/10 | 2/2 | 100% / 100% |
| `sw/firmware/ctrl_nvm/nvm_klj2.c` | 198/198 | 106/106 | 100% / 100% |
| `sw/firmware/ctrl_nvm/nvm_store.c` | 434/434 | 259/259 | 100% / 100% |
| `sw/firmware/ctrl_nvm/plat/nvm_flash_litespi.c` | 100/100 | 63/63 | 100% / 100% |

### Round 8 gate table

All 102 final recorded invocations exit 0. All jobs have finished. The builder
reports one unavailable calibration report as NOT RUN; the compiler-absent
control intentionally skips compiled instruments. The separate pinned-SDK
audit has zero NOT RUN and 2,146 actual firmware compiler invocations.

| Gate | Evidence / command | Status |
| --- | --- | --- |
| Firmware IF=1/2 and full F0-F4 campaigns | `test_ctrl_firmware.py --require-rv32 --self-test --jobs 4` | rc 0; all positives, 469 control plants, 108 SRP plants, six additional IF=1 plants and two pin controls |
| Coverage writer and checker | `fw_coverage.py --write/--check --jobs 4` | Both rc 0; 22 files, 100% after inherited exclusions |
| Focused four-module suites | Full AcmpMailbox and SrpApp at IF=1/2 | rc 0 |
| NVM full campaign | `test_ctrl_nvm.py --require-rv32 --self-test --jobs 4` | rc 0; five shapes, 435 tests and all 109 plants |
| Linked images | `ctrl_image.py`; `ctrl_srp_image.py`, both shapes and IF=1/2 for SRP | rc 0; pinned RV32 compiler |
| Image auditor controls | `ctrl_image_selftest.py --require-rv32` | rc 0; 33 controls |
| Harness controls | coverage selftest, RV32 selftest and tally mutants | All rc 0; 28, 17 and 18+18 controls respectively |
| Protocol differentials | ADP, ACMP and SRP arms; `maap_differential.py --self-test` | Positive arms pass; MAAP rc 0 with 12 positives and 16 plants |
| Mailbox integration | Committed tracked scratch export, pinned HDL compiler, inner build jobs 8 | rc 0; WB 382, AXI 427, cosim 32, IF=2 WB 384 / AXI 429 / model 369; all five plants |
| Builder documentation steps | Builder required-RV32 bank, compiler selftest, compiler-absent audit | All rc 0; builder calibration report explicitly NOT RUN, compiler-absent instruments explicitly NOT RUN |
| Pinned SDK compiler audit | `test_firmware_compiler.py --sdk-destination "$SDK" --audit ...` | rc 0; verified pinned SDK, 2,146 compiler invocations, zero NOT RUN |
| Documentation bank | 75 commands; final HDL-reference invocation replaces dirty-tree attempt | All 75 final individual commands rc 0 |
| Final documentation checks | Docs, style, wire accountability, CI scope, diff check and no-Git archive | All rc 0 |

`ROUND8-GATES.md` and its JSON receipt bind every final command to its log,
exit code, duration, byte count and SHA256. Superseded development attempts are
listed separately. Long jobs use independent log/rc files and bounded foreground
waits; all finished before publication. Products live outside the source tree.

### Round 8 linked size

| Shape / IF | Text | Read-only | BSS | Stack | RAM span | Delta Round 7 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 1x1 / 1 | 43400 | 2878 | 22888 | 8192 | 77376 | +14688 |
| 1x1 / 2 | 44724 | 2878 | 34248 | 8192 | 90064 | +14800 |
| 8x8 / 1 | 43352 | 2878 | 37640 | 8192 | 92080 | +14704 |
| 8x8 / 2 | 44704 | 2878 | 63752 | 8192 | 119536 | +14816 |

Bytes, including alignment. The same verified runtime inputs from earlier
rounds are used. ACMP is now reachable in this fixture. The reserved stack is
not a whole-call-chain proof; these fixtures are not booted shipping images.
The independent inherited F3 image auditor and its 33 controls also pass.
Its 1x1/8x8 totals are 46,664/57,020 bytes, excluding stack and including
saved-state storage with ADP/ACMP/MAAP. The four-module fixture above excludes
saved-state storage. The two profiles are separate measurements, not a combined
shipping-image budget.

### Round 8 integrity and remaining work

The lwSRP gitlink remains `9197193e47a6bb1c45a56d90a18c1784123aba44`;
no dependency edit or local commit was required. No new RTL, mailbox register-map,
default placement or shipping-image change was made beyond merging assigned dev.
The all-four application attaches SRP after compose/restore/open, before the
first service pass. The integrator's ACMP environment still owns binding-port
delivery and retries; live stream/MAAP updates and fabric licence output remain
target integration. This round does not claim hardware timing or a complete
issue #665 implementation.

The manager owns publication, protected hosted checks, trusted local replication,
independent review and the lens ledger, candidate validation, merge authorization
and post-merge containment. `ROUND8-INTEGRITY.json` records the clean source and submodules, unchanged
separate dependency clone, exact merge parents, matching configured identity,
one-line commit and zero running jobs. Forty-eight ignored gate products were
moved from the source tree to disk scratch. Peak service memory was
8,805,326,848 bytes, below 9 GB; final free disk space was
168,841,261,056 bytes, above the 30 GB floor. Completed artifact
pages were released from cache as needed without modifying file contents.
`ROUND8-SOURCE.json` hashes all 70 merge-delta files and identifies 49 as
byte-identical assigned-dev imports. `ROUND8-SIZES.json` binds linked artifacts
and verified runtime inputs. `ROUND8-MANIFEST.json` seals this round's packet.
No packet file exceeds 200000 bytes; no toolchain, installed environment, package
or tree export is included. Large artifacts are represented by size and SHA256.
Public [REVIEW READY receipt](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6046592070) posted after all jobs finished.

The following Round 7 sections remain historical evidence.

## Round 7

Assignment: issue comment 6040189958. R532-6-F1 found that a wire-valid record
could fill the finite pool with its own Domains and retain itself indefinitely,
blocking other interfaces and binding calls. The adapter now discards a continuing
allocation refusal after 1000 ms from the original mailbox arrival, at the next
eligible receive attempt. A queued record gets no fresh window. Failed participant
recreation checks the same bound. Successful recovery takes precedence over discard;
pending events, ticks and owed output retain their ordering.

`rx_discarded` counts an expired record once, independently of `received` and
`malformed`. The policy uses one periodic interval and does not extend the 10 ms
service budget. The bound is conditional on an eligible retry; an independent
permanent TX stall still cannot guarantee delivery. Earlier applied attributes
remain and MRP refresh/aging recover the lost suffix. Matching reset and destroy
still cancel the retained record. The original eleven receive tests are unchanged.

R532-6-F2 is addressed by twelve linked measurements, with deltas against the
lane base and Round 5 and object/symbol attribution below. R532-6-S1 is addressed
by the README's pending-event wording and statement that every valid Class A
Domain value is retained. Manager corrections for R532-6-R1 and R533-6-F1/R1 are
preserved in `PR-BODY.md`: it identifies the candidate accurately and retains the
four-command tracked mailbox-export recipe and pinned compiler argument.

R533-6 resolved the earlier MAJOR at the previous head. R532-6 was NEGATIVE on
this newly fixed defect; independent re-review of this candidate remains owed.
Earlier round history is in `ROUND6-HANDOFF.md` and its linked evidence. The
current contract and measurements in this Round 7 handoff supersede old status,
publication and unbounded-retention wording.

## Changes with file locations

| File:line | Round 7 change |
| --- | --- |
| `sw/firmware/ctrl/srp/srp_mbx.c:18` | Define the 1000 ms original-arrival recovery limit. |
| `sw/firmware/ctrl/srp/srp_mbx.c:388` | Unsigned elapsed-time expiration, clear the record and count discard once. |
| `sw/firmware/ctrl/srp/srp_mbx.c:415` | Expire an already-aged record on its first refusal; no new window after queueing. |
| `sw/firmware/ctrl/srp/srp_mbx.c:655` | Check the same bound on failed participant recreation and eligible retry; successful application wins. |
| `sw/firmware/ctrl/srp/srp_mbx.h:80` | Add `rx_discarded`; binding contract at line 97 permits retry after expiration. |
| `sw/firmware/ctrl/srp/README.md:35` | State that every valid Class A Domain value is retained. |
| `sw/firmware/ctrl/srp/README.md:85` | Use pending-event wording; document exact limit, ordering, counters and loss recovery. |
| `sw/firmware/ctrl/srp/README.md:203` | Describe real-pool flood, boundary, wrap and bound-removal tests. |
| `sw/firmware/ctrl/test/srp_rx_retry.cpp:23` | Wire-valid multi-Domain and service helpers; six regressions start at line 277. |
| `sw/firmware/ctrl/test/srp_mutants.py:575` | Twelve named behavioral plants; original ninety remain. |
| `sw/firmware/gtest/coverage.ratchet:19` | Generator raises SRP measured coverage to 469 lines / 438 branches. |

## Tests and planted defects

| Test and source line in `sw/firmware/ctrl/test/srp_rx_retry.cpp` | Planted defect(s) | Observable |
| --- | --- | --- |
| `OversizedValidRecordExpiresOnceAndReleasesOtherInterfaceAndBinding:277` | `receive-retention-unbounded`, `receive-retention-short`, `receive-retention-late`, `receive-discard-uncounted`, `receive-discard-malformed`, `receive-discard-as-success` | 150 valid Domains exceed the actual pool; retained at 999 ms, discarded once at 1000 ms, later-interface withdrawal and binding proceed, received/malformed stay distinct. |
| `QueuedRefusalKeepsOriginalArrivalDeadlineAcrossClockWrap:307` | `receive-queue-renews-deadline`, `receive-first-refusal-never-expires` | Aged queued record expires on first refusal, including clock wrap. |
| `RecoveryAtDeadlineStillAppliesTheCompleteRecord:324` | `receive-expiry-precedes-recovery` | Storage recovered at the deadline applies the whole record without discard. |
| `RetainedDeadlineCrossesClockWrapWithoutEarlyDiscard:337` | `receive-deadline-not-modular` | Unsigned elapsed time retains at 999 ms and expires at 1000 ms across wrap. |
| `FailedRecreationCannotRetainInputBeyondItsDeadline:352` | `receive-recreate-never-expires` | Missing participant cannot retain input indefinitely; fresh input works after recreation. |
| `DomainFloodCannotDelayLaterRapidLeave:374` | `receive-flood-unbounded` | Sixty valid Domain records drain; a later leave revokes within one simulated millisecond. |

All six new cases pass at IF=1 and IF=2. The twelve new plants fail their required
behavioral observable at both counts; the full 102-plant SRP campaign passes at
IF=2. `ROUND7-TESTS.md` maps every SRP plant to its test, source line and required
failure. `ROUND6-CONTROL-TESTS.md` maps the unchanged 196 control/MAAP plants,
all rerun in this round. Build failures are not accepted as detection evidence.

Unmodified R532 HOL probes pass for N=2,12,20,30,150 at both interface counts;
the N=30/150 cases release the later withdrawal within the five-second LeaveTime.
The new boundary regression observes release at exactly 1000 ms. R532 flood
probes show no pending record after drain, then `revoked_after_ms=0` for the later
withdrawal at both counts. The unchanged four-case R533-5 probe reports
`active=0 received=2 malformed=0 stops=1`; all six independent retry probes also
pass. Probe source files are the public `reviews/R532-6/scripts` artifacts.
`round7-receipts/probes-final.log` retains the complete normalized output.

## Coverage table

The repository generator wrote the ratchet; a separate `--check` passes.
No exclusion was added or changed. Counts below are after existing exclusions.
SRP increases from 459/459 lines and 432/432 branches to 469/469 and 438/438.

| File | Lines | Branches | After existing exclusions |
| --- | ---: | ---: | --- |
| `sw/firmware/ctrl/adp/adp.c` | 204/204 | 95/95 | 100% / 100% |
| `sw/firmware/ctrl/adp/adp_mbx.c` | 83/83 | 38/38 | 100% / 100% |
| `sw/firmware/ctrl/app/ctrl_app.c` | 31/31 | 20/20 | 100% / 100% |
| `sw/firmware/ctrl/app/ctrl_app_srp.c` | 10/10 | 6/6 | 100% / 100% |
| `sw/firmware/ctrl/loop/ctrl_loop.c` | 101/101 | 62/62 | 100% / 100% |
| `sw/firmware/ctrl/maap/maap.c` | 209/209 | 140/140 | 100% / 100% |
| `sw/firmware/ctrl/maap/maap_csr.c` | 39/39 | 18/18 | 100% / 100% |
| `sw/firmware/ctrl/maap/maap_mbx.c` | 98/98 | 60/60 | 100% / 100% |
| `sw/firmware/ctrl/mbx/mbx.c` | 177/177 | 68/68 | 100% / 100% |
| `sw/firmware/ctrl/mbx/mbx_wire.h` | 15/15 | 12/12 | 100% / 100% |
| `sw/firmware/ctrl/plat/mbx_plat_mmio.c` | 10/10 | 0/0 | 100% / 100% |
| `sw/firmware/ctrl/port/ctrl_debug.c` | 19/19 | 6/6 | 100% / 100% |
| `sw/firmware/ctrl/port/ctrl_pool.c` | 99/99 | 60/60 | 100% / 100% |
| `sw/firmware/ctrl/port/shlan_port.c` | 22/22 | 6/6 | 100% / 100% |
| `sw/firmware/ctrl/srp/srp_mbx.c` | 469/469 | 438/438 | 100% / 100% |
| `sw/firmware/ctrl/wire/wire.h` | 10/10 | 2/2 | 100% / 100% |
| `sw/firmware/ctrl_nvm/nvm_klj2.c` | 198/198 | 106/106 | 100% / 100% |
| `sw/firmware/ctrl_nvm/nvm_store.c` | 434/434 | 259/259 | 100% / 100% |
| `sw/firmware/ctrl_nvm/plat/nvm_flash_litespi.c` | 100/100 | 63/63 | 100% / 100% |

## Gate table

All 99 final recorded invocations exit 0. `ROUND7-GATES.md` expands every command,
environment and duration; `ROUND7-GATES.json` distinguishes original log hashes
from normalized retained logs. Development attempts are recorded separately in
`ROUND7-DEVELOPMENT.json`. The compiler-absent run and builder bank remain
manager-owned under issue comment 6036016117; this packet claims no new pass
for those operations.

| Gate | Exact command / receipt entry | Result |
| --- | --- | --- |
| Firmware host/RV32 and campaigns | `test_ctrl_firmware.py --require-rv32 --self-test --mutation-shard I 3 --jobs 4`, I=0,1,2 | Three rc 0; 196 control/MAAP plants, 102 SRP plants and two pin controls caught; five entity shapes, walk/differential included |
| Independent probes | `python3 "$PACKET/round7-helpers/probes.py"` | rc 0; R532 HOL/flood/retry and R533-5 unchanged probes plus lane receive/timing at IF=1/2 |
| New plants at IF=1 | `python3 "$PACKET/round7-helpers/new_plants_if1.py"` | rc 0; all twelve detected at required behavioral observable |
| Coverage | `fw_coverage.py --write --jobs 4`; `fw_coverage.py --check --jobs 4` | Both rc 0; all 19 files 100% after unchanged exclusions |
| Harness controls | `fw_coverage.py --selftest`; `fw_rv32_selftest.py --require-rv32`; `tally_selftest.py --mutants` | All rc 0; 28 coverage arms, 17 target controls, 18 tally arms and 18 plants |
| NVM firmware | `test_ctrl_nvm.py --require-rv32 --jobs 4` | rc 0; 435 tests across five shapes |
| Mailbox generation/integration | `gen_mailbox.py --check`; tracked export and four-command recipe in PR body | Both rc 0; Wishbone 316, AXI 361, IF=2 316/361, model 316, cosim 13; five plants |
| MAAP differential | `maap_differential.py --self-test --keep "$SCRATCH/maap-diff"` | rc 0; 12 positives and 16 plants |
| Dependency profiles | `python3 "$PACKET/round7-helpers/upstream_positive.py"` | rc 0; OFF/ON, 87 unit cases and three behavior scenarios each |
| Linked sizes | `python3 "$PACKET/round7-helpers/images.py"` | rc 0; twelve links, identical verified runtime inputs |
| Documentation bank | `docs-00` through `docs-74` in `ROUND7-GATES.md` | All 75 rc 0 |
| Additional documentation | Final docs/style, docs selftest, wire accountability, CI scope, no-Git archive and feature checks, diff check | All rc 0; archive has one expected no-inventory skip |

## Linked size

Values are bytes. Spans include alignment and an 8192-byte stack reservation;
these fixtures are not booted images or whole-call-chain stack proofs.

| Shape / IF | Text | Read-only | BSS | Stack | RAM span | Delta lane base | Delta Round 5 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1x1 / 1 | 33560 | 2846 | 18072 | 8192 | 62688 | +43936 | +8096 |
| 1x1 / 2 | 34792 | 2846 | 29424 | 8192 | 75264 | +56016 | +9424 |
| 8x8 / 1 | 33500 | 2846 | 32824 | 8192 | 77376 | +58624 | +8096 |
| 8x8 / 2 | 34744 | 2846 | 58928 | 8192 | 104720 | +85472 | +9424 |

The Round 5 delta includes imported MAAP composition and the retained receive
record. MAAP and its application wiring add 5036/5368 text bytes at IF=1/2.
MAAP application state grows by 1104/2172 BSS bytes, its allocation fixture by
8/16, and the one shared retained mailbox record by 1528. Pools and runtime
inputs remain unchanged. `ROUND7-SIZE.md` gives the exact twelve-link table,
object attribution and reproduction; `ROUND7-SIZES.json` records artifact sizes
and SHA256 hashes. Round 7 alone adds 112–128 bytes of linked span and no BSS.

## Integrity and remaining work

The parent, four initialized submodules and separate dependency clone are checked
for clean tracked and untracked state in `ROUND7-INTEGRITY.json`. Gate-created
ignored scratch is moved out of the source tree. Peak service memory was
4351004672 bytes; final free disk space was 129892544512 bytes, within both
resource limits. `ROUND7-SOURCE.json` binds the
six changed files to the committed head. `ROUND7-MANIFEST.json` hashes this round's
packet. No packet file exceeds 200000 bytes; large logs and binary artifacts are
represented by hash and size. No installed package, toolchain, environment or
source export is stored in the packet.

The public lwSRP pin remains `9197193e47a6bb1c45a56d90a18c1784123aba44`.
No dependency edit or commit was required. F3 is absent from the assigned F2 base,
so ACMP binding calls remain owed. Live stream/MAAP updates and the fabric licence
output remain target integration. Timing remains a conditional host envelope;
original arrival is retained, and an 11 ms exhaustion or TX stall still fails
the 10 ms service predicate. Physical scheduling/timing remains unproven.
The all-fabric default, shipping image, RTL, submodule pins and register map are
unchanged by Round 7. Full processor-only SRP suites were not rerun; the selected
firmware walk and wire differential were.

The manager owns publication, hosted gates, trusted local replication, independent
reviews and their lens ledger, candidate merge validation, merge authorization
and post-merge containment. No push, PR edit, merge, rebase, amend, hardware access
or flashing was performed in this round. REVIEW READY is implementation evidence,
not approval or completion of the repository's merge bar.
