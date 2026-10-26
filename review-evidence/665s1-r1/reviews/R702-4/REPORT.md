[R702] NEGATIVE - exact head d33a5adc60cd93b34be41dfacf94daaec9d059c2

External independent review R702-4, issue #665 / PR #795. Tree: `7e8fef6c536150dfcded5b34ae6edde2cd6165cf`. Two MAJOR findings remain. All five lenses were applied to the six-commit delta `44d95625..d33a5adc`; the previous review stands outside that delta. This is source review, not merge acceptance.

The new failure responses fix the successive SET commands and initial-open cases. They do not protect getters or asynchronous notifications carrying unapplied state. Automatic unlock also loses its required notification permanently after an acknowledgement timeout.

## Scope and authority

Reconstructed the repository operating contract, contribution rules and documentation map; issue body and frozen public decisions; requirements and interfaces; then base/delta history, changed sources and public execution evidence. Controlling decisions are the [assignment](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6409739310), [commit/port ruling](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6410169666), [permanent all-fabric placement](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6410301079), [memory exception](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6412739248), and [round-4 assignment](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6417644908).

Applied `REQUIREMENTS.md:49`, `docs/ARCHITECTURE_HW_SW_SPLIT.md:55`, `docs/reference/FR_NFR.md:363`, the YAML/generated mailbox contract, and linked interface/memory documents. The existing no-IN_PROGRESS policy permits the selected bounded failure path: ENTITY_MISBEHAVING within the service bound and IEEE 1722.1-2021 9.3.2.6 response deadline. This review does not require adopting IN_PROGRESS. It requires preserving the no-unapplied-promise rule and asynchronous notification obligations.

No private author material, management checkout, or current-round peer report was read. A PR metadata request unexpectedly bundled prior public review bodies before the independent diff pass; this incidental exposure is disclosed. Independent delta observations and a provisional verdict/ledger were written before deliberately reconciling those findings.

## Findings

### R702-4-F1 - MAJOR - Conformance, RTL, Robustness, Tests, Docs

**Artifacts:** `sw/firmware/ctrl/aecp/aecp.c:339`, `:348`, `:511`; `sw/firmware/ctrl/aecp/aecp_commands.c:310`; `sw/firmware/ctrl/test/test_aecp.cpp:2039`; `docs/design/MAILBOX_SPLIT.md:1255`.

**Authority/evidence:** Round-4 item 1 prohibits any response or notification promising an unapplied F value. The architecture requires acknowledgement before such a promise; IEEE 1722.1-2021 7.5.2 and Milan v1.2 5.4.5.2 govern notification ordering. The new guard checks state-changing command opcodes and their immediate notification flag. A getter does neither. Asynchronous GET_STREAM_INFO calls the getter and enables notification without checking application; its response overlays the core's tentative output offset.

Independent tests in `delta_probes.py`, at one and two interfaces, produce:

```text
REVIEW getter: status=0 returned=255 last_acknowledged=0 busy=1 owed=1
REVIEW notification: status=0 offset=4321 busy=1 owed=1
```

The first withholds acknowledgement, receives ENTITY_MISBEHAVING for SET_CONTROL(IDENTIFY=255), then receives SUCCESS/255 from GET_CONTROL; last acknowledged IDENTIFY was 0. The second registers a controller, withholds acknowledgement for SET_STREAM_INFO(offset=4321), then posts a stream-info change. Unsolicited GET_STREAM_INFO succeeds with 4321 while the commit remains held. Both use the actual adapter/mailbox model and unchanged production source. `delta-probes-if1.log` and `delta-probes-if2.log` contain the failing assertions. The permanent late-commit test explicitly requires the unsafe successful getter.

**Impact:** A failed SET is immediately presented as applied state through a getter or a separate notification. Fixing the original SET response does not repair this controller-visible ordering defect. RTL is attributable through its architecture/interface remit; no separate HDL hold-logic defect is alleged.

**Required outcome:** Getters, descriptor views and notifications carrying affected F state must preserve acknowledged-state ordering. While publication is pending, use an appropriate bounded failure/defer outcome or a coherent acknowledged view. Preserve required asynchronous work until it can be reported correctly. Align the tests and timeout description with this contract.

**Verification:** Both new getter/notification assertions must pass at one and two interfaces, alongside normal-path and timeout controls. Cover held, owed-but-free, partial acknowledgement, recovery and unrelated observations; rerun relevant mutations and coverage. This retains the unfulfilled part of R702-3-F1 and R701-3-F1.

### R702-4-F2 - MAJOR - Conformance, RTL, Robustness, Tests, Docs

**Artifacts:** `sw/firmware/ctrl/aecp/aecp.c:453`, `:462`; `sw/firmware/ctrl/test/test_aecp.cpp:2149`; `docs/design/MAILBOX_SPLIT.md:1264`; `sw/firmware/ctrl/aecp/README.md:68`.

**Authority/evidence:** Milan v1.2 5.4.2.2 and 5.4.5.2/Table 5.22 require unsolicited LOCK_ENTITY on automatic unlock. The pinned interface authority states this at `protocol-processor/docs/architecture/06_aecp_engine.md:803` and `:814`; see also `docs/reference/MILAN_COMPLIANCE_MATRIX.md:117`. This asynchronous obligation does not depend on a successful solicited response.

At expiry the core clears `locked`, attempts publication, then sets `notify = applied(a)`. A late application clears notification without retaining any obligation. Recovery cannot re-enter the expiry branch because `locked` is already false. The new permanent test explicitly expects zero notifications even after recovery.

The independent probe passes its no-premature-notification check, restores acknowledgements, verifies LOCK_HELD=0 on every interface and a still-registered controller, then services another 100 passes. Both interface counts report:

```text
REVIEW unlock recovery: applied=1 notifications=0 registered=1
```

**Impact:** A transient publication delay permanently hides automatic unlock from registered controllers. The changed application/notification contract breaks required behavior even after recovery. This is not wording residue or an acceptable consequence of refusing a SET.

**Required outcome:** Retain automatic unlock as owed notification work until its publication is acknowledged, then deliver it to the applicable registered controllers with correct flags, sequencing and ordering. Preserve the 60-second unlock and bounded service. Replace the expectation that recovery stays silent and correct the documentation.

**Verification:** `Face.ReviewAutomaticUnlockMustBeNotifiedAfterRecovery` must pass at both interface counts, including its no-early-notification control. Add permanent delayed/missing/partial-acknowledgement recovery and notification-backpressure coverage. RTL attribution is architectural; HDL behavior remains unchanged.

## Prior findings and original probes

| Prior item | Disposition at this head |
|---|---|
| R702-3-F1 / R701-3-F1 | Partially repaired, retained under F1. Timed-out SET returns status 10 without its immediate notification; a second SET is refused before changing state; initial publication gates open. Getter/asynchronous promises still violate the general contract. Unlock recovery is new F2. |
| R701-3-F2, stale measurements | Resolved. `MAILBOX_SPLIT.md:1298` records 138 arms/43 rules, common adapter counts 523/530, separate 45 AXI4-Lite checks, and model 488. Public executed receipts agree. |
| R702-3-F2, generated F1-store wording | Resolved. YAML says saved-state store; generated package/header/reference changes are that description only. Independent generator check/crosscheck/selftest passes. |
| R702-3-R1 / R701-3-W1, comment residue | Resolved. Listed assignment/ruling/comment IDs and face-test comment labels were removed; issue/requirement references and executable diagnostics remain. No new wording residue or optional suggestion is raised. |

`response_probe.py` and `probe_ack.py` are byte-identical to their published versions; hashes are in `published-summary.json`. Both ran unchanged on disposable test copies.

- `response_probe.py`: passes at one and two interfaces, rc 0. Its unchanged anchor now appears after recovery, checking the next successful change there.
- `probe_ack.py`: its substantive assertion, `successful response must not promise an unwritten F value`, passes. It observes `response_status=10 core_identify=255 mailbox_identify=255`, without another commit. Its two `receive` helpers still expect status 0, so that test fails only those helper assertions; its defect-detection wrapper exits 1. Both controls pass. The whole unmodified probe is not green. This expectation mismatch is not another product defect and does not reinstate the original successive-SET failure.

The assignment's literal request for both unmodified probes to pass has this qualification. The intended original assertion is satisfied; the three new assertions fail for the remaining product defects.

## Executed checks and public evidence

| Check | Result and scope |
|---|---|
| Independent focused firmware | 22 tests at each interface count: 19 existing tests pass; exactly three new assertions fail. Covers core guard, late/missing/partial acknowledgement, recovery ordering, initial open, application/store/events and service budget. `delta-probes-if1.log`, `delta-probes-if2.log`. |
| Independent regeneration | `gen_mailbox.py --check --crosscheck --selftest`: rc 0, zero failed arms. `generator.log`. Requested frontend identity verified as 5.050 before use. |
| Public receipt integrity | All 568 supplied manifest entries match SHA-256. `evidence-hashes.json`. No commit signature header or detached signature exists in the supplied packet: signer authentication could not be verified. |
| Coverage and mutations | Published 100% after existing exclusions across 31 files: `aecp.c` 372/372 lines, 318/318 branches; `aecp_face.c` 172/172, 148/148. No coverage-framework/exclusion delta. Four final campaign receipts contain 108 distinct caught defects. Coverage does not validate the wrong expectations above. |
| Census and mailbox | Public census: six shapes, 217 ports each, 138 arms/all 43 rules, rc 0, 949 seconds locally. Mailbox: 523/568 checks, 530/575 at two interfaces, model 488, cosimulation 32, 199/199 mutants. Relevant census/generator/bench changes are commentary only; broad campaigns were not repeated. |
| Receipt applicability | Firmware execution head `989c9f537f8b973fb4a5c97cad36abb35da1244a`; only five Markdown files change after it. Relevant hardware/test logic is unchanged after cited runs. Final documentation receipt has 69 zero-exit commands. `tree-integrity.json`, `published-summary.json`. |
| All-fabric export | Five published base/head normalized digests match, with no unclassified different/missing files. Export inputs are unchanged after the measured ancestor. This is documented stamp/archive/hierarchy normalization, not literal identity of timestamp-bearing raw directories. `published/export/export-digests.txt`. |
| Memory ledger | Final public plans match `SPLIT_CONTROL_MEMORY.md:153`: 37.0/40.5/50.5/57.0 RAMB36. Round 4 adds 392-400 ROM bytes and 16 SRAM bytes; 8x8/one-interface gains half a tile. Only authorized 8x8/two-interface remains one tile over, owed to S14, with 104 ROM bytes before 57.5. Default and other-point override refusals remain recorded. Five largest BSS objects agree. These are plans, not fresh mapped measurements. |
| Hardware/broad gates | No behavioral HDL/generator delta. Prior mailbox-only OOC area/timing stands, not whole-image/hardware proof. Public broader source gates/sweep have physical calibration NOT RUN and field campaigns skipped. No manager source bank is claimed or inferred. |

Evidence: [published packet at 2d88c87c](https://github.com/kebag-logic/milan-fpga/tree/2d88c87ca36b521ac875b6299c2a3204040e942b/review-evidence/665s1-r1), restricted to receipts/scripts, and [source review-ready comment](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6420795336). Private handoff material was not used.

## Reviewer-owned coverage ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN - F1, F2 | Frozen assignment; `FR_NFR.md:363`; architecture rule; `aecp.c:339`, `:453`, `:511`; response/notification/recovery probes | R702-4 | d33a5adc60cd93b34be41dfacf94daaec9d059c2 |
| RTL | UNCLEAN - F1, F2 (architecture/interface) | `aecp.h` applied contract; `aecp_face.c:77`, `:127`; application bridge; YAML commit contract; HDL/generator/bench comment-only comparisons | R702-4 | d33a5adc60cd93b34be41dfacf94daaec9d059c2 |
| Robustness | UNCLEAN - F1, F2 | Held/owed/partial acknowledgement; second command; initial open; timeout recovery; lock expiry; both-interface probes | R702-4 | d33a5adc60cd93b34be41dfacf94daaec9d059c2 |
| Tests | UNCLEAN - F1, F2 | `test_aecp.cpp:2039`, `:2149`; `aecp_mutants.py`; original probes; 19 controls pass beside three failures per interface count; coverage receipt | R702-4 | d33a5adc60cd93b34be41dfacf94daaec9d059c2 |
| Docs | UNCLEAN - F1, F2 | `MAILBOX_SPLIT.md:1255`, `:1264`, verification rows; `aecp/README.md`; YAML/regenerated descriptions; memory ledger; public task/PR/receipts | R702-4 | d33a5adc60cd93b34be41dfacf94daaec9d059c2 |

The HDL sub-check is clean: commit holding, decode, tags, reset, widths and coalescing logic did not change. The architecture lens cannot be banked while its changed end-to-end acknowledgement/notification contract is broken. Outside the delta, previous scope and limits stand.

## Integrity, limits and manager duties

`tree-integrity.json` verifies all 1,448 parent tracked blobs, executable/symlink modes, HEAD/tree/index and every tracked blob/mode/index tree in the five required initialized submodules against exact gitlinks. All match. Optional `external` remains uninitialized. No tracked bytes required restoration. Disposable probes/builds and unpublished evidence copies are under packet `scratch/`; published logs replace local paths with neutral placeholders.

Commands ran in foreground. Independent probe builds ran concurrently with at most eight compile workers, below 16. No full parent/processor/builder bank, synthesis, hardware, shared install, source fix, commit, push, GitHub write, merge, local workflow replica or host orchestrator was executed. The initial generator selftest used its own automatically removed temporary directory; no retained disposable tree exists outside packet scratch.

This round does not newly accept hosted jobs or skipped contexts. The manager owns exact-head hosted/local-replica acceptance and the census job's setup-plus-execution budget. The 949-second receipt is local time, not hosted duration. No signed manager source bank exists or is inferred.

Before merge: repair F1/F2 and re-review affected lenses, resolve the original-probe status qualification publicly, obtain independent positive reviews, validate the final current-dev candidate with manager builder/native banks and published receipts, then complete authorized merge and containment. Source base `e76a755a` and supplied live dev `76de691e5625cc4ea2f9a19def9e07c1183a14ee` differ; this review does not validate their merge result.

S6 still owes real datapath/clock-crossing wiring and removal of the named split-only map-writer exclusion. S14 owes the excess tile before default flip; target-runtime work remains separate. Physical calibration NOT RUN and field skips are not hardware proof. Issue #665 remains open.

Every publishable script/receipt is listed in `MANIFEST.sha256`; scratch is excluded.

R702-4 FINISHED
