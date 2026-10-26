[R701] NEGATIVE - exact head d33a5adc60cd93b34be41dfacf94daaec9d059c2

Internal independent review R701-4, issue #665 lane S1 / PR #795 (base `dev-soft-core`), tree `7e8fef6c536150dfcded5b34ae6edde2cd6165cf`. This is a round-4 delta review of `44d95625..d33a5adc` (six commits by the round-4 executor), answering R701-3 and R702-3 under the round-4 assignment (issuecomment-6417644908). All five lenses were applied to the delta. Code the delta does not touch keeps its round-3 verdict unless the delta changes something it depends on.

The round-3 defect is fixed as stated. No command now answers SUCCESS, and nothing is notified, before the face commit is acknowledged. A second change while one is held is refused before it changes anything. AECP opens only after the initial publication is acknowledged. My unmodified round-3 probe passes at one and two interfaces. The verification rows, the regenerated contract text and the round-3 residue are all closed.

The chosen failure path brings a new MAJOR. A change whose acknowledgement is late gets ENTITY_MISBEHAVING but still takes effect, both in the core and later in the datapath. No registered controller is ever notified of it (FR-CTRL-03). There is also one MINOR about what the new refusal response carries.

## Findings

### R701-4-F1 — MAJOR — Conformance, Robustness, Tests, Docs

**Artifacts:** `sw/firmware/ctrl/aecp/aecp.c:348-353` (after a change, `applied` false turns the status into ENTITY_MISBEHAVING and drops `notify`, but leaves the core's change in place); `sw/firmware/ctrl/aecp/aecp.c:461-462` (lock expiry: `notify = applied(a)`, and nothing re-arms it); `sw/firmware/ctrl/test/test_aecp.cpp:2040`, `:2149` (the tests require a read of the held value and require that the release is never notified); `docs/ARCHITECTURE_HW_SW_SPLIT.md:107`; `docs/design/MAILBOX_SPLIT.md:1250-1256`, `:1264-1265`; `sw/firmware/ctrl/aecp/README.md` (the `applied` paragraph).

**Authority/evidence:**
- `docs/reference/FR_NFR.md:200` (FR-CTRL-03, M) says "state changes MUST emit unsolicited responses to registered controllers".
- The round-4 assignment item 1 says "no response or notification may promise an unapplied F value", and "a failed apply has a bounded, defined outcome".
- The chosen outcome reports failure for a change that is not undone. With the acknowledgement withheld, SET_CONTROL IDENTIFY=255 answers ENTITY_MISBEHAVING (status 10), and the core keeps IDENTIFY=255.
- A GET_CONTROL during the hold answers SUCCESS with 255, while the datapath has not acknowledged it (`test_aecp.cpp:2040` requires exactly this).
- When the acknowledgement returns, the poll publishes the interface whole and the datapath takes 255. No unsolicited SET_CONTROL is ever sent to the other registered controller.
- My probe `scripts/late_ack_notify_probe.py` shows this at one and two interfaces: `receipts/late-ack-probe-if1.txt` and `-if2.txt` both print `datapath_identify=255 owed0=0 unsolicited_set_control=0`, and the probe test fails.
- The lock-expiry path is the same: the lock is released in the core, LOCK_HELD falls when the datapath acknowledges, and no unlock notification is ever sent. `Face.AMissingAcknowledgementRefusesEveryChangeAndNotifiesNothing` asserts this at `test_aecp.cpp:2149` ("a release no response promised is still not notified").
- The executor's own REVIEW READY lists "A release or change applied by a late acknowledgement is not notified afterwards" as an open risk. That does not make it conformant.
- Several texts describe this wrongly:
  - The comment at `aecp.c:461`, "the release is notified only once the platform applied it", describes a deferred notification that does not exist.
  - `ARCHITECTURE_HW_SW_SPLIT.md:107`, "Without that acknowledgement the command fails", is not what happens: the command's change persists and is applied later.

**Impact:**
- The path is reached whenever the datapath does not acknowledge within `MBX_FACE_ACK_CYCLES` (64 cycles), for example while its domain is held in reset. A transient stall then leaves every registered controller's view of the entity stale with no end. Configuration, format, clock source, identify, name, maps and lock state can all change silently.
- The controller that sent the command is told it failed. If it relies on that, it believes the old value, while reads and the datapath carry the new one.
- The tests and twelve new plants pin this behaviour down as correct, so fixing it means changing them.

**Required outcome:**
- A failed apply must leave a consistent outcome. Either:
  - (a) a command that answers a failure leaves the entity's state unchanged, in the core and in what the datapath finally takes; or
  - (b) every state change that does take effect, including a lock release at expiry, is notified to registered controllers once its acknowledgement returns, and the documents stop calling it a failed command.
- During the hold, either reads report the last acknowledged value, or the issue records a decision that a GET reporting a held, not yet acknowledged value is not a "response that promises" it under item 1.
- The comment at `aecp.c:461`, `ARCHITECTURE_HW_SW_SPLIT.md:107`, `MAILBOX_SPLIT.md:1250-1265` and the aecp README describe the outcome actually implemented.

**Verification:**
- Apply `scripts/late_ack_notify_probe.py` to a disposable copy and run `aecp_arms.py --app [--interfaces 2] --filter 'Face.ReviewerProbe*'`. For (b) it must pass. For (a) the datapath must not end at 255, and no read may report 255.
- Add equivalent permanent tests for a late-acknowledged lock release, plus a plant for each.
- Re-run the AECP mutant campaign, `fw_coverage.py --check` and the probe of R701-3.

### R701-4-F2 — MINOR — Conformance, Tests, Docs

**Artifacts:** `sw/firmware/ctrl/aecp/aecp.c:339-344` (the refusal before a change copies the command's own body into the response); `sw/firmware/ctrl/test/test_aecp.cpp:736` (asserts "the refusal echoes its body"); `docs/design/MAILBOX_SPLIT.md:1260`; `sw/firmware/ctrl/aecp/README.md:66`.

**Authority/evidence:**
- The core's own response-content rules report current state on a refusal:
  - `aecp_commands.c:301`: "IEEE 7.4.15.1: report current fields even when the SET is refused", for SET_STREAM_INFO.
  - `aecp_commands.c:464`: LOCK_ENTITY always reports the current `lock_owner` in `locked_id`, including on ENTITY_LOCKED.
- The new refusal returns instead the proposed fields: the requested latency, format, rate, clock source, configuration, IDENTIFY value or name. LOCK_ENTITY returns the requester's own `locked_id` field rather than the controller that holds the lock.
- `Core.AChangeThePlatformHasNotAppliedPromisesNothing` asserts this echo for all ten commands.

**Impact:**
- While a commit is held, a controller that takes a refused SET's payload as the entity's current state, as the core's other refusal paths let it, records values that are not in force.
- A refused LOCK_ENTITY hides the lock holder.
- This is limited to the held-commit path, so it is MINOR.

**Required outcome:** The refusal carries what the same command's other refusals carry: current fields for SET_STREAM_INFO, current `locked_id` for LOCK_ENTITY, and the current values for the other SET commands. Alternatively, the issue records a decision with its clause for why echoing is conformant. Tests and documents must match.

**Verification:** `test_aecp.cpp:736` is changed to expect the current values, with a plant that echoes the body; run the AECP campaign and coverage.

### R701-4-S1 — SUGGESTION — Robustness

**Artifact:** `sw/firmware/ctrl/test/ctrl_aecp_image.c:132` against `sw/firmware/ctrl/app/ctrl_app_aecp.h:46` and `sw/litex/milan_soc.py:2689`.

The new contract says an unacknowledged initial publication "opens nothing ... and the call may be made again". The linked image's `main` treats that `false` as fatal: it returns 6 before `ctrl_loop_run`, which stops ADP and ACMP as well. At this head `CtrlMailbox` holds the datapath's acknowledgements idle ("a commit waits"), so this image could never start on today's split SoC. A datapath domain that leaves reset after the CPU would have the same effect later.

The image is a measurement build and the face is not yet connected (S6), so this is not blocking. The placement switch's boot path should retry `ctrl_app_open_aecp` from the loop rather than exit.

### R701-4-S2 — SUGGESTION — Docs (wording, optional)

- `sw/mailbox/census_ports.py:50` reads "applies the #637 restore (#637)". The parenthesis repeats the issue just named. Change it to "applies the #637 restore, so map persistence keeps one owner".
- The comment reflows in this delta left ragged lines that the next touch could re-wrap: `sw/firmware/ctrl/mbx/mbx.h:125-128`, `sw/mailbox/mailbox.yaml:64` and `sw/mailbox/publication_census.py:113`.
- `docs/design/MAILBOX_SPLIT.md:1298` says "the 39 reads of the 25 class-D nets". The census receipt says "25 class-D net(s) from the wrapper cell's ports, 4 unread; 39 read(s) of 21 class-D net(s)". Consider "the 39 reads of 21 of the 25 class-D nets (4 are unread)". Both numbers are already true, so this is optional precision.

No new comment in the delta carries a lane label, review round, reviewer ID or issue-comment ID. The remaining such IDs in the changed files predate this PR or are runtime reason strings (`census_ports.py:244`, `:267-268`; `ctrl_memory.py:206`), which the comment rule does not cover. So no RESIDUE is raised.

## Prior findings at this head

| Prior finding | Status at d33a5adc | Evidence |
|---|---|---|
| R701-3 F1 (MAJOR: SUCCESS before an unacknowledged commit; second value coalesced; AECP opened before the initial publication was acknowledged) | **Resolved as stated** | `aecp.c:339-353`, `aecp_face.c` `applied`/`open`/`poll`, `ctrl_app_aecp.c:237-254`. My unmodified `response_probe.py` (sha256 `9d018fe7…b9ddb`) passes 7 of 7 at one and two interfaces (`receipts/response-probe-if{1,2}.txt`). The reworked test asserts ENTITY_MISBEHAVING, no notification and no new commit for both held commands, then commit and acknowledgement before the next response, so it now checks ordering. The probe's anchor line now sits after recovery, so the held case is proved by the test's own assertions rather than by the probe. The failure outcome it chose is the new R701-4-F1. |
| R701-3 F2 (MINOR: stale verification rows) | **Resolved** | `MAILBOX_SPLIT.md` rows match the published receipts: 217 ports C25/F28/R34/E6/M14/G110; 138 arms (118 + 18 + 2 controls); 43 rule removals; 523/568 and 530/575, with the AXI4-Lite build's own 45 stated separately; model 488 of 530; quick plants 7 of 7. Face-block and AECP-face rows were added. |
| R701-3 W1 (RESIDUE: IDs and F-labels in new comments) | **Resolved** | Every listed instance was removed. `T0` became "the timing check". Grep at head: none remain in new comments. |
| R702-3 F1 (MAJOR, same defect) | **Resolved as stated**, same as R701-3 F1 | Its probe `probe_ack.py` belongs to the other reviewer's packet, which I may not read before my verdict. The published author-run log shows its own assertion holds (`response_status=10 core_identify=255 mailbox_identify=255`). Its fixture's SUCCESS precondition for both held commands fails, as item 1 now requires. See manager duties. |
| R702-3 F2 (MINOR: "F1 store" in contract text) | **Resolved** | `mailbox.yaml:511` reads "the firmware's saved-state store". Only that phrase moved in `KL_mbx_pkg.sv:409`, `mbx_contract.h:408` and `MAILBOX_CONTRACT.md:333`. `gen_mailbox.py --check --crosscheck` reports 0 findings and `--selftest` passes at head (`receipts/gen-check.txt`, `gen-selftest.txt`). |
| R702-3 residue list | **Resolved** | Every listed comment substitution is present. The census `(#637)` replacement follows that list exactly (see S2). |

Round-4 focus items:

1. **No promise of an unapplied value.**
   - Met for SUCCESS responses and notifications at command time.
   - The defer path is stated with its clause: a defined failure status, the no-IN_PROGRESS policy and the 240 ms bound (IEEE 1722.1-2021 9.3.2.6, `FR_NFR.md`).
   - Every refusal and the timed-out command are held to the 10 ms service bound by `Face.AMissingAcknowledgement…`.
   - No second value is coalesced, and AECP opens only once the initial publication is acknowledged.
   - **Not met** for the outcome of a timed-out commit: see F1.
2. **Tests.** Present for a delayed and a missing acknowledgement, a partial acknowledgement at two interfaces, a second change while held, recovery, lock expiry and the initial publication. They pass at both widths, 93 of 93 each (`receipts/aecp-arms-app-if{1,2}.txt`), and 12 new plants are caught (published 108 of 108). The tests that fix F1's and F2's behaviour as correct need to change with those findings.
3. **Verification rows and contract text.** They match, and the contract text was regenerated.
4. **Coverage, export and memory.**
   - Coverage is 100 % with no new exclusion: the published `fw_coverage.py --check` passes for 31 files, `aecp.c` 372/372 and 318/318, `aecp_face.c` 172/172 and 148/148. The delta adds no exclusion marker and leaves `fw_coverage.py` and the ratchet unchanged.
   - The all-fabric export is unaffected. The delta's `milan_soc.py` and `ctrl_memory.py` edits have identical Python ASTs (`receipts/python-comment-only.txt`), and its `hdl/` edits are comments in mailbox files the all-fabric build does not instantiate. The published base and `989c9f53` normalised digests are identical for all five configs, with no "different" or "missing" files. `989c9f53..d33a5adc` touches only documents.
   - The memory ledger changed only as stated. Every point gains 392 to 400 B of `rom` and 16 B of `sram`. 8x8 with one interface goes from 50.0 to 50.5. 8x8 with two interfaces stays at 57.0 with 104 B of headroom (118,784 − 118,680), and it is still refused without the override. The override is still refused at the other three points. All of this matches the published plans.

## Reviewer-owned coverage ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1, F2) | `aecp.c:43-62`, `:339-353`, `:425-465`; `aecp_commands.c:301`, `:445-465`; `aecp.h:93-109`; `aecp_face.c` `publish`/`applied`/`open`/`poll`; `ctrl_app_aecp.c:237-254`; `FR_NFR.md:200`; the round-4 assignment; both probes | R701-4 | d33a5adc60cd93b34be41dfacf94daaec9d059c2 |
| RTL | CLEAN | The delta's RTL edits are comments only: `KL_mbx_evt.sv:15-23`, and the regenerated description in `KL_mbx_pkg.sv:409`, confirmed by `gen_mailbox.py --check --crosscheck` and `--selftest` at head. `milan_soc.py` and `ctrl_memory.py` have identical ASTs. The face block's interface contract (`mailbox.yaml:440-462`, `ack_cycles: 64`) is unchanged and is now honoured end to end by the firmware: no response before the acknowledgement. Published at this head's RTL inputs: bench 523/568/530/575/488 and 199 of 199 mutants. Round 3's RTL lens was unclean only through R701-3 F1, which is resolved. | R701-4 | d33a5adc60cd93b34be41dfacf94daaec9d059c2 |
| Robustness | UNCLEAN (F1) | Timed-out, partial and missing acknowledgements; a second change while held; recovery; lock expiry during a hold; open retry (`AppFaceUnacknowledged`); service bound (`test_aecp.cpp:2080-2153`); `late_ack_notify_probe.py` | R701-4 | d33a5adc60cd93b34be41dfacf94daaec9d059c2 |
| Tests | UNCLEAN (F1, F2) | `test_aecp.cpp:711-758`, `:2016-2153`, `:2400-2431`; `aecp_wire_model.hpp:103`; `aecp_mutants.py` (12 new plants, published 108 of 108); my runs of 93 of 93 at both widths; the round-3 probe passing unmodified; coverage receipt | R701-4 | d33a5adc60cd93b34be41dfacf94daaec9d059c2 |
| Docs | UNCLEAN (F1, F2) | `ARCHITECTURE_HW_SW_SPLIT.md:106-108`; `MAILBOX_SPLIT.md:1220-1320`; `SPLIT_CONTROL_MEMORY.md` section 5; `aecp/README.md`; `ctrl/README.md`; `aecp.h`, `aecp_face.h`, `ctrl_app_aecp.h`; generated contract text; `docs_check.py` 0 findings at head | R701-4 | d33a5adc60cd93b34be41dfacf94daaec9d059c2 |

## Evidence and limits

- **Reconstruction.** I read AGENTS.md; the issue's lane S1 assignment, owner decisions and clarification, and the round-4 assignment; the executor's TAKEN and REVIEW READY comments; FR_NFR (FR-CTRL-03 and the AECP response rows); the delta diff and history; and the published round-4 receipts. The receipts sit at evidence commit `2d88c87c…` under `review-evidence/665s1-r1/author-r4`. I fetched 84 of them by blob id. Every one matches its git blob id and its `MANIFEST.json` `published_sha256` (`receipts/evidence-manifest-check.txt`).
- **Evidence signature.** The evidence commit itself is unsigned according to the API. No separate signature artifact was found for the round-4 packet.
- **Order of reading.** Prior reviewers' findings were read after my independent pass over the diff, from the public PR comments only. One limit: while searching the comments for evidence references, an automated filter printed the opening of the other reviewer's round-3 comment, whose F1 summary matches the assignment, before my findings were final. My findings above come from my own probes and source reading.
- **Gate heads.**
  - Firmware gates in the published evidence ran at `989c9f53`. `989c9f53..d33a5adc` changes only five documents, which I read.
  - The image ledger ran at `989c9f53` and the export at `989c9f53`.
  - The four-shard sweep ran at `a6519873`. I did not re-run it, because the firmware and RTL inputs are unchanged after `989c9f53`.
- **Docs gates.** `gen_toc.py --check` and `--verify-anchors` could not run here: the pinned Markdown renderer is not installed, and shared installs are not allowed (`receipts/gen-toc-*.txt`). The published docs-gate receipt (69 of 69 rc 0) is relied on for those two. `docs_check.py` ran clean at head.
- **Not run by me.** No census, mailbox bench, mutants, image link, Yosys, Vivado or export run was repeated. The delta does not change their inputs, beyond what my checks above cover. No manager source bank ran at this head, and none is claimed. Physical calibration was NOT RUN. Field skips are not hardware proof. The datapath side of the face is not connected until S6, so this review certifies neither the future wiring nor real acknowledgement timing.
- **Checkout integrity.** After the probes, `receipts/checkout-integrity.txt` confirms:
  - the head and tree;
  - all 1,448 tracked blobs, their modes and the index;
  - the five populated submodules at their gitlinks;
  - `external` as an unpopulated gitlink, as checked out;
  - no untracked files.

  All probe edits were made in a disposable copy and restored there. `scripts/verify_checkout.py` is the round-3 script with only its expected head updated.

**Pending manager duties:**
1. Record that `probe_ack.py`'s fixture precondition, SUCCESS for both commands while the acknowledgement is held, conflicts with item 1, so its literal "pass unmodified" cannot be met. Its own assertion holds.
2. Carry F1 and F2 to the next round. F1 may need an owner decision between outcomes (a) and (b), and on reads during a hold.
3. Hosted and act acceptance, and the current-dev candidate banks at the merge turn: source base `e76a755a`, live dev `76de691e`.

R701-4 FINISHED
