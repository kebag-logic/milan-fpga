[A560]

# F4 handoff

Relates to #665. Branch: `665-f4-srp` -> `dev`.
Round 7 REVIEW READY locally at `f74b9403b330ce316eeec6f724846f16def98443`.
One new commit: `Bound SRP receive allocation retries by original arrival`.
Parent: `cce554f64f6bdab1f6d26e5c4d7b46d54d228c52`, the published Round 6 head of PR #690.
The Round 7 commit is not pushed. No review verdict or finding closure is claimed.

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
