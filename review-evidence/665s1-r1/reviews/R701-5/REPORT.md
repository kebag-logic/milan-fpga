[R701] NEGATIVE - exact head 6d2b77bb3bfb8e2fbd30db56613c8c3b5ea0ef44

Internal independent review R701-5, issue #665 lane S1 / PR #795 (base `dev-soft-core`), tree `e7648d5aa4f16cc7b6fe7a37f9c76d622325320b`. This round reviews the delta from round 4's reviewed head, `d33a5adc..6d2b77bb`. That is six commits: three firmware and test commits and a docs commit up to `4e3aab32`, then three ledger and docs commits answering ruling 6425357821. All five lenses were applied to the delta. Code the delta does not touch keeps its round-4 verdict.

The round-5 model works as the ruling 6421238472 asks. While a change of face state waits, the core holds it undone behind IN_PROGRESS, and every getter, READ_DESCRIPTOR and notification reports the values in force. It answers exactly once: SUCCESS then its notification, or ENTITY_MISBEHAVING with no notification. A lock expiry's notification is kept until its release is applied. All four round-4 findings (R701-4-F1/F2, R702-4-F1/F2) are resolved at their cause. The 57.5 RAMB36 ledger change follows ruling 6425357821 exactly. The undone-value window is named where that ruling asks.

One new MINOR keeps the verdict NEGATIVE. The delta now refuses every change while a change waits or the face is held. Through the MVU path, SET_SYSTEM_UNIQUE_ID answers NOT_IMPLEMENTED, not the ENTITY_MISBEHAVING that the contract and docs state. No test or plant sees this. Three wording residues and some optional suggestions follow.

## Scope reconstructed

- **Assignment.** Lane S1, issuecomment-6409739310. Its STOP conditions and gates still stand, refined by these rulings:
  - 6410169666, round 2;
  - 6410301079, the all-fabric placement stays permanent;
  - 6412739248, round 3 budget: one named point may plan over 56, owed to S14;
  - 6417644908, round 4;
  - 6421238472, round 5: acknowledged state is the only truth a controller sees;
  - 6425357821, on the round-5 STOP. Option (a): 8x8 with two interfaces may plan 57.5. Risk 1 is accepted and must be named in `MAILBOX_SPLIT.md` and the PR body. The three probe fixtures go in the PR body.
- **Authorities read.**
  - `AGENTS.md` and `CONTRIBUTING.md`;
  - `docs/ARCHITECTURE_HW_SW_SPLIT.md` section 1;
  - `docs/reference/FR_NFR.md`, the AECP rows;
  - `docs/design/MAILBOX_SPLIT.md`, "The firmware's writer" and the verification rows;
  - `docs/design/SPLIT_CONTROL_MEMORY.md` sections 3, 5 and 6;
  - `sw/firmware/ctrl/aecp/{aecp.h,aecp_face.h,README.md}`.
- **Evidence.** The published packet is at `3bda7dff` (`review-evidence/665s1-r1`). All 820 `MANIFEST.json` entries hash-match, with none unlisted. That commit carries no signature, so integrity rests on the manifest hashes, not on a signer. The executor's REVIEW READY is issuecomment-6425827814 and the STOP is 6425326942. Author receipts were read by section. Private handoff material was not used.

## Findings

### R701-5-F1 - MINOR - Conformance, RTL (architecture/interface contract; no HDL defect), Robustness, Tests, Docs

**Artifacts:**
- `sw/firmware/ctrl/aecp/aecp.c:272`: the MVU SET_SYSTEM_UNIQUE_ID guard `!aecp_foreign_lock(a)`. When it fails, the status stays at 1, NOT_IMPLEMENTED.
- `sw/firmware/ctrl/aecp/aecp_commands.c:18-21`: `aecp_foreign_lock` now returns true whenever `a->refusing`.
- `aecp.c:341`: `refusing` is set while a change waits, while an expiry is un-notified, or while `applied` is false.
- `aecp.c:366-368`: the ENTITY_LOCKED to ENTITY_MISBEHAVING mapping exists only on the AEM path.
- The contract text: `aecp.h:103-105` ("While it is false the lock check refuses every change, ENTITY_MISBEHAVING"), `docs/design/MAILBOX_SPLIT.md:1267-1271` ("Every other change ... answers ENTITY_MISBEHAVING") and `sw/firmware/ctrl/aecp/README.md:57-59`.

**Authority/evidence:**
- Ruling 6421238472 item 1 and the docs above define the refusal of a change during a wait as ENTITY_MISBEHAVING.
- The core implements SET_SYSTEM_UNIQUE_ID (`aecp.c:271-282`). Milan v1.2 5.4.4.2 is the clause, and `aecp/README.md:280` says "the core implements both".
- At `d33a5adc` the MVU path was not refused for an unapplied face, because `changes()` gated only AEM commands. The delta creates this behaviour.
- The probe `probes/probe_wait_refusals.cpp` was run on the real adapter and mailbox model at one interface (`receipts/probe-wait-refusals-if1.txt`):

```text
PROBE set_name status=10
PROBE mvu_set_system_unique_id status=1 (ENTITY_MISBEHAVING=10, NOT_IMPLEMENTED=1)
PROBE mvu_set_system_unique_id_after_failed_wait status=1
```

- SET_NAME, on the AEM path, is refused as documented. The MVU command answers NOT_IMPLEMENTED both during the wait and after a failed wait while the face is still held.
- `fw_coverage.py --check` reports `aecp.c` at 414/414 lines and 350/350 branches, and the campaign catches 128 of 128 plants. So this path is executed but never asserted.

**Impact:**
- A controller that sends SET_SYSTEM_UNIQUE_ID in a wait of up to 100 ms, or while the datapath has not taken a commit, is told the command does not exist. A controller may then stop using an implemented Milan command.
- The contract's single refusal status ("ENTITY_MISBEHAVING ... before it changes anything") is not true of every change path.
- The SYSTEM_ID change carries no face value (`aecp_face.c:109`). The refusal is the delta's choice, not a requirement of the face.

**Required outcome:** One of these, with the tests and docs matching:
- (a) The MVU change path, refused only because a change waits or the face is held (not because of another controller's lock), answers ENTITY_MISBEHAVING with the current `system_unique_id`, as the AEM refusals do.
- (b) SET_SYSTEM_UNIQUE_ID is exempt from the face refusal because it carries no face value. Then `aecp.h`, `MAILBOX_SPLIT.md` and the aecp README name the exemption.

**Verification:**
- A permanent test sends MVU SET_SYSTEM_UNIQUE_ID during a pending wait and after a failed wait, and checks the chosen status and body.
- A plant restoring status 1 is caught by that test.
- `probes/probe_wait_refusals.cpp` (or its permanent equivalent) passes at one and two interfaces.
- Re-run `aecp_mutants.py` (4 shards), `fw_coverage.py --check` and `aecp_arms.py --app` at both widths.

### R701-5-W1 - RESIDUE - Docs (source comment rule)

`sw/firmware/ctrl/test/test_aecp.cpp:713-714` was added in `bd0b7ff185`. Its comment reads "reads are answered (R701-4 F2; IEEE 1722.1-2021 7.4.15.1)", which puts a reviewer ID and finding ID in a source comment.

Exact fix: "reads are answered (#665; IEEE 1722.1-2021 7.4.15.1)."

### R701-5-W2 - RESIDUE - Docs

`docs/ARCHITECTURE_HW_SW_SPLIT.md:110` says "otherwise the command fails, changing nothing", and `sw/firmware/ctrl/aecp/aecp_face.h:16` says "else it fails, changing nothing". Under the window accepted by ruling 6425357821 item 2 (`MAILBOX_SPLIT.md:1285-1297`), the datapath holds the undone value from its late acknowledgement until it takes the republished block.

Exact fix:
- In ARCHITECTURE: "otherwise the command fails and the core keeps the values in force; the datapath may hold the undone value until it takes the republished block (see the face's writer)."
- In `aecp_face.h`: "else it fails and the core keeps the values in force (the datapath ends there once it takes the republished block)."

### R701-5-W3 - RESIDUE - Docs

`docs/design/SPLIT_CONTROL_MEMORY.md:176` says "All 224 B of `sram` are the core's state: the held response (`AECP_HELD_BYTES`, 122 B), the four recorded values, and the wait's deadline and requester." On RV32 those parts total about 198 B. The list leaves out the noted change (kind, type, index), the held response's interface and length, and the four flags.

Exact fix: "... the held response (`AECP_HELD_BYTES`, 122 B) with its interface, length and requester, the four recorded values, the noted change, the wait's deadline and its flags." The figure is unchanged.

### Suggestions (optional, non-blocking)

- **R701-5-S1 - Robustness.** `aecp_commands.c:28-36` and `aecp.h:121-133`:
  - `aecp_keep` silently drops a fifth record. A dropped record makes a failed change's rollback incomplete.
  - It also trusts `n <= sizeof was` (8).
  - The `AECP_KEPT` comment's "a further copy, which READ_DESCRIPTOR never reads" holds only if configuration 0's ENTITY copy comes first in model order.

  Shipped models have one configuration, so nothing is reachable today. A refusal in `aecp_init` of a model with more than two ENTITY copies, plus an `n` guard, would make the bound structural.
- **R701-5-S2 - RTL/Robustness.** `refuse()` (`aecp.c:105-112`) re-runs the held command with the held *response* body as its input. That is correct only because every `AECP_WAITS` handler's response echoes its command layout and reaches the lock check before reading request fields. Stating that invariant beside `AECP_WAITS`, or keeping the command body, would stop a future handler from breaking it silently.
- **R701-5-S3 - Docs.** The stray blank line at `aecp_commands.c:55-56`, which the executor noted. Remove it on the next firmware touch.
- **R701-5-S4 - Conformance (outside the delta).** A SET_SYSTEM_UNIQUE_ID under another controller's lock answers NOT_IMPLEMENTED, and `test_aecp.cpp:1616` codifies it. If Milan v1.2 5.4.4.2 requires ENTITY_LOCKED there, open an issue. That is not this lane's work.
- **R701-5-S5 - Docs.** `MAILBOX_SPLIT.md:1293-1294` cites "the review's outcome (a)" by PR comment 6421229873 as the authority for a design outcome. Citing ruling 6425357821 alone, which adopted it, keeps a review report out of the authoritative chain.
- **Carried, unchanged and outside the delta:**
  - R701-4-S1: the linked image's `main` exits when the initial publication is unacknowledged. This is owed to the placement switch.
  - R701-4-S2, first two bullets: `census_ports.py:50` "(#637)", and the ragged reflow lines.

## Prior findings at this head

| Prior item | Disposition | Evidence at `6d2b77bb` |
|---|---|---|
| R701-4-F1 (MAJOR: failed change still took effect, unnotified) | **Resolved**, option (a) | `aecp.c:370-384` holds and undoes the change. `aecp.c:582-606` either redoes it, answers SUCCESS and notifies, or keeps it undone and answers ENTITY_MISBEHAVING with no notification. `Face.ALateCommitIsOwedAndPublishedAgainWhole` asserts that the core stays undone, GET_CONTROL and READ_DESCRIPTOR show the value in force, there is one final ENTITY_MISBEHAVING and no notification, and the datapath ends at the value in force. The remaining window is accepted by ruling 6425357821 item 2 and named at `MAILBOX_SPLIT.md:1285` and in the PR body's limits. My round-4 probe, rerun unmodified (`receipts/r701-4-probe-rerun.txt`), ack-within-bound case: datapath 255, `unsolicited_set_control=1`. It fails only its first-frame status (IN_PROGRESS 9 against its 10), which ruling 6421238472 item 1 changed. |
| R701-4-F2 (MINOR: refusal echoed the request) | **Resolved** for the AEM path | Refusals go through the lock check. `Core.AChangeThePlatformHasNotAppliedPromisesNothing` compares each with its lock refusal, byte for byte, and LOCK_ENTITY reports the `locked_id` in force. The MVU path, newly refused by this delta, is the new F1. It is not a regression of F2's scope. |
| R701-4-S1, S2 | S1 carried. In S2, the third bullet is resolved (`MAILBOX_SPLIT.md:1330` now reads "the 39 reads of 21 of the 25 class-D nets (4 are unread)", which matches the census receipt). The first two bullets are carried. | - |
| R702-4-F1 (MAJOR: getters and notifications presented unapplied state) | **Resolved** | During a wait, nothing reads a tentative value: `swap()` undoes it, and `aecp_poll` returns before `asynchronous()`. `Face.APendingChangeIsAnsweredOnceTheDatapathTakesIt` covers GET_STREAM_INFO and a held stream notification. The author's unmodified rerun of `delta_probes.py` at `4e3aab32` printed `returned=0 last_acknowledged=0` and no stream notification while held. The firmware is byte-unchanged from `4e3aab32` to this head. |
| R702-4-F2 (MAJOR: automatic-unlock notification lost) | **Resolved** | `aecp.c:483-501` keeps `unlocked` until `applied`, then notifies once. `Core.ALockExpiryIsNotifiedOnceThePlatformAppliedTheRelease` and `Face.AMissingAcknowledgementFailsTheChangeAndRefusesEveryOther` pass in my runs. The author's rerun of `ReviewAutomaticUnlockMustBeNotifiedAfterRecovery` printed `applied=1 notifications=1 registered=1`. |
| R702-4 note: unmodified `probe_ack.py` not green | **Settled** by ruling 6425357821 item 3 | The PR body's table names the three fixtures, whose first frame is now IN_PROGRESS by design, and why. |

## Lens results (applied to the delta)

- **Conformance.**
  - The `AECP_WAITS` mask `0x01404142` decodes to command types 1, 6, 8, 14, 22 and 24: LOCK_ENTITY, SET_CONFIGURATION, SET_STREAM_FORMAT, SET_STREAM_INFO, SET_CLOCK_SOURCE and SET_CONTROL. These are exactly the commands that change an F field (`aecp_face.c:28-68`). SET_NAME and SET_SAMPLING_RATE reach the face only through `dyn_dirty`, which no controller reads.
  - The wait bound is 100 ms from the command (`aecp.c:381`), resolved at the next poll. That puts the final response inside 120 ms of the IN_PROGRESS and 240 ms of the command (`FR_NFR.md:363`), and `Core.A...WaitsUndone...` checks the bound at `AECP_WAIT_MS-1` and `AECP_WAIT_MS`.
  - The response precedes its notification, and the notification skips the requester (`aecp.c:448-478`, `:597-601`).
  - The saved-state store marks a record and latches the core's value later (`aecp_nvm.c:132-161`). So a failed change is re-marked with the values in force (`aecp.c:594`), and no undone value persists.
  - Unclean on F1.
- **RTL (architecture and interfaces).**
  - The delta changes no file under `hdl/`, `tb/` or `syn/`, and no generated file. `mailbox.yaml:447-449` is a comment, and `gen_mailbox.py --check` reports 0 findings.
  - The face's `applied` and `publish` keep the KL_mbx commit contract: a written commit is never withdrawn, nothing is written while a change waits, and owed interfaces are republished whole (`aecp_face.c:77-137`).
  - The wait's state set is `waiting`, `refusing`, `unlocked` and `kept`. Its transitions in `aecp_rx`, `aecp_poll` and `asynchronous` are complete: every path out of `waiting` sets the response and requester.
  - Unclean on F1, because the MVU path breaks the `aecp.h` port contract.
- **Robustness.**
  - Covered: a second change during a wait, a change on another interface, TX backpressure holding the final response (`room=false` in `Core.A...WaitsUndone...`), partial acknowledgement, a missing acknowledgement, and a lock expiry inside a wait.
  - AddressSanitizer at two interfaces is clean (`receipts/fw/aecp-arms-app-if2-asan.txt`).
  - `AECP_HELD_BYTES` (122) bounds every `AECP_WAITS` response: 16, 4, 12, 84, 8 and 5 body bytes.
  - Unclean on F1. See also S1.
- **Tests.**
  - Every ruling 6421238472 item-5 case has a named permanent test, and each ran green at both widths.
  - 24 new plants. The campaign catches 128 of 128 at this exact head (`receipts/aecp-mutants/`). The README's "50 defects" matches the table (`receipts/face-defect-count.txt`).
  - The `test_ctrl_memory.py` ledger arms and the three ledger plants were checked from the author's exact-head receipts: plants at 57.0 and at 58.0, and the override applied to any image, each turn the test red.
  - Unclean on F1: the MVU refusal path is executed but unasserted.
- **Docs.**
  - The `SPLIT_CONTROL_MEMORY.md` section 5 table matches `linked-images.txt` byte for byte: rom 104,360, 105,944, 118,080 and 119,736; sram 46,256, 57,648, 86,832 and 112,992.
  - Derived figures check out: +1,056 and +224 B per point; 1,096 B of rom to the next granule; 952 B to return to 57.0 (119,736 - 118,784); 235,520 B / 4,096 = 57.5.
  - The `FR_NFR.md:363` exception and the risk-1 paragraph are present. The PR body states the fixtures and the limits.
  - A docs-gate subset passed here: `docs_check`, `check_doc_style`, `check_em_dash --base e76a755a`, `DOC_MAP --check` and `check_feature_status`. The author's receipt has 69 of 69.
  - Unclean on F1; W1 to W3 are residue only.

Acceptance for the delta:
- The images plan 37.0, 40.5 and 50.5, within 56. 8x8 with two interfaces plans 57.5 by name, which is not over its ruled 57.5. No STOP condition is triggered.
- The `ctrl_memory.LEDGERED` change is read only by `plan(..., ledgered=)` (`ctrl_memory.py:338-354`). `add_ctrl_memory` (`milan_soc.py:2800`) names no override. So the all-fabric export inputs are unchanged by this delta, and round 4's export digest evidence stands.

## Reviewer-owned coverage ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN - F1 | `aecp.c:272`, `:341-384`, `:481-501`, `:582-606`; `aecp_commands.c:18-36`, `:129-165`, `:246-301`, `:303-376`, `:463-531`; `AECP_WAITS` decode; `FR_NFR.md:363`; rulings 6421238472 and 6425357821; probe receipt | R701-5 | 6d2b77bb3bfb8e2fbd30db56613c8c3b5ea0ef44 |
| RTL | UNCLEAN - F1 (architecture/interface; no HDL defect) | `aecp.h:100-133`, `:192-209`; `aecp_face.c:77-137`; no `hdl/`, `tb/`, `syn/` or generated change since `d33a5adc`; `mailbox.yaml:447-449` comment only; `gen_mailbox.py --check` | R701-5 | 6d2b77bb3bfb8e2fbd30db56613c8c3b5ea0ef44 |
| Robustness | UNCLEAN - F1 | wait, failed wait, held face, second command, backpressure and expiry paths; ASan run at two interfaces; `aecp_keep` bounds | R701-5 | 6d2b77bb3bfb8e2fbd30db56613c8c3b5ea0ef44 |
| Tests | UNCLEAN - F1 | `test_aecp.cpp:711-857`, `:2128-2245` and the Face wait tests; `aecp_mutants.py` (128 of 128, 4 shards); `fw_coverage.py --check`; `test_ctrl_memory.py` and ledger-plant receipts; prior-round probe rerun | R701-5 | 6d2b77bb3bfb8e2fbd30db56613c8c3b5ea0ef44 |
| Docs | UNCLEAN - F1 (W1 to W3 residue only) | `ARCHITECTURE_HW_SW_SPLIT.md:55-58`, `:104-111`; `MAILBOX_SPLIT.md:1239-1304`, `:1330`, `:1347`; `SPLIT_CONTROL_MEMORY.md` sections 3, 5 and 6; `aecp/README.md:52-76`, `:187-224`; `ctrl/README.md:602`; `aecp.h`; `aecp_face.h`; PR body | R701-5 | 6d2b77bb3bfb8e2fbd30db56613c8c3b5ea0ef44 |

To bank the lenses once F1 is fixed, re-run all five lenses on a head that contains the fix. That fix touches the firmware core, its tests and the docs.

## Executed here, and real limits

- **Executed here, all at the exact head:**
  - `aecp_arms.py --app` at one and two interfaces, and with ASan at two: 97 of 97 each.
  - `aecp_mutants.py`, 4 shards: 128 of 128.
  - `fw_coverage.py --check`: PASS, 31 files.
  - `gen_mailbox.py --check`: 0 findings.
  - The docs-gate subset above.
  - One reviewer probe, which found F1.
  - The round-4 probe, rerun unmodified.
  - Commands are listed in `receipts/commands.txt`.
- **Relied on from the author's receipts at this head, or at `4e3aab32` for firmware, which is byte-unchanged since:**
  - `test_ctrl_memory.py` under LiteX's interpreter. The system interpreter here has no migen, so my run refused at import: `receipts/litex/`.
  - The linked images at four points: not re-linked here, because they use the author's shared runtime. The figures were checked arithmetically against `linked-images.txt` and the plan receipts.
  - `behave`; the census; the mailbox bench; the four-shard Verilator sweep; `ctrl_boundary.py`; the full docs gates.
- **Not run:**
  - No full parent, PP, gPTP, Yosys or builder bank.
  - No `KL_mbx` OOC run. Round 4's OOC run stands, since no HDL changed.
  - No hardware. Physical calibration is NOT RUN, and field-campaign skips are not hardware proof.
- **Hosted, read-only snapshot at this head** (`receipts/hosted-check-runs.txt`): `rtl-fast` and 26 other jobs succeeded. Twenty jobs were in progress and three queued, including Verilator and Yosys shards. "Physical gPTP" was skipped. No job had failed. This is not acceptance.
- **No manager source bank** exists at this head, and none is claimed or inferred.
- **Integrity** (`receipts/checkout-integrity.txt`): after the probes, all 1,448 tracked blobs, modes and index entries equal HEAD. The five initialized submodules are at their gitlinks and clean, and the optional `external` is not initialized. Ignored bytecode left by subprocess builds was removed.

## Pending manager duties

- Carry F1 back to the executor. After the fix, both reviews must run again on the new head across all five lenses.
- Carry W1 to W3 to the residue checklist.
- Accept the exact-head hosted and act results: `verilator-suites` and `yosys-portability` were still running at this snapshot.
- Build and validate the current-dev merge candidate with the builder and native banks, and publish their receipts. The source base is `e76a755a`; live dev is `76de691e5625cc4ea2f9a19def9e07c1183a14ee`. This review does not validate that merge result.
- Carry the owed items: S6 wires the datapath side, which closes the undone-value window and drops the split-only map-writer exclusion; S14 owes 1.5 tiles at 8x8 with two interfaces before the flip.
- Issue #665 stays open.

R701-5 FINISHED
