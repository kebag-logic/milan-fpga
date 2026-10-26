[R702] NEGATIVE - exact head 6d2b77bb3bfb8e2fbd30db56613c8c3b5ea0ef44

Round R702-5, external cleared-context review of PR #795 (issue #665, lane S1). Tree `e7648d5aa4f16cc7b6fe7a37f9c76d622325320b`. This is a delta round: the previously reviewed head was `d33a5adc`. I judged `d33a5adc..6d2b77bb` (6 commits, 17 files: the AECP core and face writer, `aecp_mutants.py`, `test_aecp.cpp`, `ctrl_memory.py` and its test, a comment in `mailbox.yaml`, and docs), together with every named prior finding. Scope comes from the issue body and the S1 rulings and decisions on #665: 6409739310, 6410169666, 6410301079, 6412739248, 6421238472 and 6425357821.

Summary: three MINOR findings and three RESIDUE items are open. The round-5 model largely does what ruling 6421238472 asks: it undoes a waiting change, answers IN_PROGRESS, then sends one final response; ASAN and a mutation spot-check both hold up. The ledger at 57.5 RAMB36 is reproduced and arithmetically consistent. One read path still shows an unacknowledged F value, and two properties of the new model have no test that can fail.

## Findings

### F1 - MINOR - Conformance, RTL (architecture/interface contract), Robustness, Tests, Docs - `sw/firmware/ctrl/aecp/aecp.c:483-501`, `aecp_commands.c:598-603`; `docs/ARCHITECTURE_HW_SW_SPLIT.md:56`, `docs/design/MAILBOX_SPLIT.md` "Acknowledged state is the only truth a controller sees" - ENTITY_AVAILABLE and a refused LOCK_ENTITY report the lock released before LOCK_HELD=0 is acknowledged

- **Authority.** Ruling 6421238472 item 3 says every read path shows only acknowledged F state, and that while a publication is pending, reads report the last acknowledged value. `LOCK_HELD` (`aecp_lock_held_o`) is an F value; the datapath gates host map edits on it (`hdl/milan/milan_datapath.sv:1325`, `:5012`, `:5024`, `:8167`). The head's own docs state the invariant without exception: `ARCHITECTURE_HW_SW_SPLIT.md:56` says "Acknowledged state is the only state a controller sees, in responses, reads and notifications."
- **Evidence.** At expiry, `asynchronous()` clears `a->locked` and `a->lock_owner` immediately and publishes the release. Only the notification waits for `applied` (`a->unlocked`). ENTITY_AVAILABLE (command 2) reads `a->locked` and `a->lock_owner` directly. My probe `receipts/probe-release-reads-core-if1.log` (script `scripts/probe_release_reads.cpp`, run by `scripts/run_arm.py`) uses the core's `applied` port held false across the expiry:
  - `PROBE control-locked ENTITY_AVAILABLE status=0 flags=2 lock_owner=1020304050607081` (the control: a held lock reads as locked)
  - `PROBE after-expiry core_locked=0 unlocked_pending=1`
  - `PROBE pending-release ENTITY_AVAILABLE status=0 flags=0 lock_owner=0`
  - `PROBE pending-release foreign LOCK_ENTITY status=10 locked_id=0`

  So the probe fails its two acknowledged-state assertions. The existing test `Core.ALockExpiryIsNotifiedOnceThePlatformAppliedTheRelease` checks only the notification and the refusal of changes, so it cannot see this.
- **Impact.** While the datapath has not taken the release, a controller is told the entity is unlocked, with no owner. The datapath still holds the lock, and every change that controller then attempts is refused ENTITY_MISBEHAVING. The window is the late-acknowledgement window (unbounded if the datapath never acknowledges). This is the read-path counterpart of the notification defect that round 4's F2 asked to fix.
- **Required outcome.** Either:
  - while an expiry's release is unacknowledged, every read and refusal reports the last acknowledged lock (locked, by its owner); or
  - the owner or manager rules this window accepted, and the "At a lock's expiry" text in `MAILBOX_SPLIT.md`, `ARCHITECTURE_HW_SW_SPLIT.md:56` and the PR body's limits state it by name.

  In either case a test pins the chosen behaviour.
- **RTL attribution.** As in round 4, RTL is attributed through its interface-contract remit: the firmware-to-datapath `applied` contract for the F value `LOCK_HELD`. No HDL hold-logic defect is alleged.
- **Verification.** Rerun `scripts/probe_release_reads.cpp` unmodified, appended to the head's `test_aecp.cpp`, at one and two interfaces. Under the first option it passes. Under the second, the named test and the docs state the observed values.

### F2 - MINOR - Tests - `sw/firmware/ctrl/aecp/aecp.c:599` (`a->response_interface = a->held_interface;`), `sw/firmware/ctrl/test/test_aecp.cpp` (no waiting command on interface 1) - the final response's egress interface at two interfaces is untested

- **Authority.** AGENTS.md section 6, Tests: "Each new test can fail for the defect it claims to detect". The S1 assignment (6409739310 item 3) requires state per AVB interface, tested at two interfaces.
- **Evidence.** A disposable mutant replaces the restore with `a->response_interface = 0;`. The whole app arm at two interfaces still passes (`receipts/mutant-held-interface-not-restored.out`: `rc=0 ESCAPED failing=[]`; script `scripts/review_mutants.py`). My probe `scripts/probe_held_interface.cpp` shows the mutant is observable and the head is correct:
  - at the head: `PROBE final status=0 egress=1` (passes, `receipts/probe-held-interface-head-if2.log`);
  - on the mutant: `egress=0` while carrying interface 1's source MAC (fails, `receipts/probe-held-interface-mutant-if2.log`).

  The helper `ask()` checks the frame's source MAC (held bytes), never the `Send` port's interface argument. Every waiting-command test asks on interface 0.
- **Impact.** A regression that sends a waiting command's final SUCCESS or ENTITY_MISBEHAVING out of the wrong port would pass every gate. The controller on the other link would then never receive its final response after IN_PROGRESS.
- **Required outcome.** A named test, with a plant in `aecp_mutants.py`, covers a change that waits after being asked on interface 1 while another interface's command is answered meanwhile. It checks the final response's egress interface.
- **Verification.** The new plant (the restore removed or forced to 0) is caught by its named test at two interfaces.

### F3 - MINOR - Tests, Conformance - `sw/firmware/ctrl/aecp/aecp.h:117-120` (`AECP_WAIT_MS`), `docs/design/MAILBOX_SPLIT.md` (final response "within the 120 ms cadence"), `docs/reference/FR_NFR.md:363` - the claimed IN_PROGRESS-to-final bound has no test that fails when it is exceeded

- **Authority.**
  - Issue #665, rules: "Each protocol states its firmware service-latency bound per response path and tests it."
  - Ruling 6421238472 item 1: "State the IN_PROGRESS cadence and the bound, with clauses."
  - The head states that the final response follows IN_PROGRESS within IEEE 1722.1-2021 9.3.2.6's 120 ms, "so no second IN_PROGRESS is owed".
- **Evidence.** A disposable mutant sets `#define AECP_WAIT_MS 130u`. The whole app arm at two interfaces passes (`receipts/mutant-wait-bound-past-cadence.out`: `rc=0 ESCAPED`). Every timing assertion is written relative to the constant (`ms+=AECP_WAIT_MS-1`, `mbx_model_advance_ms(&fabric,AECP_WAIT_MS)`), so no gate ties the constant to the clause. The campaign's `waiting-times-out-early` plant only halves the bound.
- **Impact.** The bound a reviewer must rely on for the 120 ms cadence and the 240 ms response deadline is enforced only by the constant's current value. Raising it past 120 ms would silently owe a second IN_PROGRESS that the firmware never sends.
- **Required outcome.** A test fails when the final response could leave more than 120 ms after its IN_PROGRESS, including the service bound the PR body adds (`AECP_WAIT_MS` plus the service bound). The test is expressed in absolute milliseconds against the clause, not in terms of `AECP_WAIT_MS`, and a plant raising the constant past the cadence is caught.
- **Verification.** The 130 ms mutant above is caught by a named test.

### RES1 - RESIDUE - `sw/firmware/ctrl/test/test_aecp.cpp:713-714` - a reviewer ID and round in a source comment, new in this delta (introduced by `bd0b7ff1`)

- The comment reads "reads are answered (R701-4 F2; IEEE 1722.1-2021 7.4.15.1)". It violates the owner's 2026-10-15 comment rule.
- **Exact fix:** "reads are answered (#665; IEEE 1722.1-2021 7.4.15.1)."

### RES2 - RESIDUE - `docs/ARCHITECTURE_HW_SW_SPLIT.md:110` and `sw/firmware/ctrl/aecp/aecp_face.h:16` - "fails, changing nothing" overstates what happens to the datapath

- Both overstate the case where the datapath acknowledges late. Ruling 6425357821 item 2 accepts, and `MAILBOX_SPLIT.md` names, a window in which the datapath holds the undone value until it takes the republished block.
- **Exact fix, `ARCHITECTURE_HW_SW_SPLIT.md:110`:** "otherwise the command fails and the core keeps the values in force; the datapath ends at them too (see [the undone value after a failed change](design/MAILBOX_SPLIT.md#the-firmwares-writer))."
- **Exact fix, `aecp_face.h:16`:** "else it fails and the core keeps the values in force".

### RES3 - RESIDUE - `docs/design/SPLIT_CONTROL_MEMORY.md` section 5 - the 224 B list of `sram` is incomplete

- The sentence "All 224 B of `sram` are the core's state: the held response (`AECP_HELD_BYTES`, 122 B), the four recorded values, and the wait's deadline and requester" omits the noted change kind, type and index, the held interface and length, and the three flags.
- **Exact fix:** "All 224 B of `sram` are the core's new state: the held response (`AECP_HELD_BYTES`, 122 B) with its length, interface and requester, the four recorded values, the noted change, the wait's deadline and three flags."

### SUGGESTIONS (non-blocking)

- **S1, `aecp_commands.c:28-36` (`aecp_keep`).** It saturates silently at `AECP_KEPT`, and it copies `n` bytes into `was[8]` with no check that `n <= 8`. Every current caller fits: at most 8 bytes, and at most 4 records with the shipped single-configuration model. But a model with more ENTITY copies than the comment at `aecp.h:123-127` assumes would leave a recorded change partly undone, with no signal. A load-time refusal in `aecp_init`, or an assertion, would make the assumption executable.
- **S2, `aecp_commands.c:55-56` (lines 55 and 56 are both empty).** There are two consecutive blank lines (the author has noted this).
- **S3, `sw/litex/ctrl_memory.py:206-207`.** The `Ledgered` reason string carries issue-comment IDs. It is a runtime string, not a comment, so it is outside the comment rule. Naming the decision (D3) and the rulings by date would read better in tool output.
- **S4, the 1x1 one-interface shipping point.** The linked-image receipt shows 88 B of `rom` before its next granule. The next firmware lane will probably move it by half a tile, and the ledger could say so.

## Probes, gates and receipts at this head (mine)

| What | Result | Receipt |
|---|---|---|
| Evidence packet `3bda7dff` `review-evidence/665s1-r1`: `author-r5/**` against `MANIFEST.json` | 189 of 189 hashes match, 0 unlisted. The packet commit is **unsigned** (GitHub verification: `unsigned`), so the integrity is the manifest's alone | this report |
| AECP app arm with AddressSanitizer, 1 and 2 interfaces (all 97 tests) | 97/97 and 97/97, no sanitizer report (the held-response `memcpy` into 122 B: every waiting handler fixes its body at 16, 4, 12/8, 84 or 5 B) | `receipts/app-if1-asan.log`, `receipts/app-if2-asan.log` |
| F1 probe, core, 1 interface | control passes, pending-release reads fail (above) | `receipts/probe-release-reads-core-if1.log` |
| F2 probe at the head and on the mutant, 2 interfaces | head passes (egress 1), mutant fails (egress 0) | `receipts/probe-held-interface-*.log` |
| Four disposable mutants (whole app arm, 2 interfaces) | `owed-change-not-refused` caught (3 tests), `record-not-reset` caught (3 tests), `held-interface-not-restored` ESCAPED (F2), `wait-bound-past-cadence` ESCAPED (F3) | `receipts/mutant-*.out` |
| `test_ctrl_memory.py` under LiteX's interpreter (home paths in the receipt redacted to `<home>`) | 0 failures. The ledger holds 57.5, the override plans its point at 57.5, and is refused at 58.0, without the override, through `add_ctrl_memory`, on the three other points and on an unknown name. The first run under the system interpreter stopped at `import migen`, an environment issue, not a finding | `receipts/test-ctrl-memory.log` |
| Ledger arithmetic, `SPLIT_CONTROL_MEMORY.md` section 5 against the author's `linked-images.txt` and `head-*.plan.txt` | every row matches (+1,056 B `rom` and +224 B `sram` against `989c9f53`; 6,432 to 6,528 B and 336 B against `e76a755a`; 1,096 B before 58.0; 952 B to 57.0; 119,608 B after both compactions). The other three points are at 37.0, 40.5 and 50.5 | author receipts (packet) |
| `gen_mailbox.py --check` (the `mailbox.yaml` delta is comment-only) | 0 findings, rc 0 | `receipts/gen-mailbox-check.txt` |
| Docs gates subset: `docs_check.py`, `check_em_dash.py --base e76a755a`, `check_doc_style.py`, `DOC_MAP.gen.py --check`, `check_feature_status.py`, `check_todo_ownership.py`, `check_wire_accountability.py --self-test` | 7 of 7 rc 0 | `receipts/docs-gates-subset.txt` |
| Exact-head hosted check runs (read-only) | 49 success, 1 skipped (`Physical gPTP (nightly and manual)`, not hardware proof), 5 in progress at read time (4 Verilator shards and fail-fast). `rtl-fast`, `publication-census`, `firmware-unit`, `firmware-aecp-mutants` and the Yosys jobs succeeded | `receipts/hosted-checks-6d2b77bb.txt` |
| Clone restored | `HEAD`, index digest, gitlinks and status identical to the baseline. The probe-created ignored outputs (bytecode caches, `sw/builder/out/`, `configs/generated/*.hex`) were removed, and every submodule is clean | `receipts/baseline-tree-state.txt`, `receipts/final-tree-state.txt`, `receipts/removed-bytecode-caches.txt` |

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1, F3) | `aecp.c:288-391`, `:446-610`; `aecp_commands.c` (lock check, `aecp_keep`, the six `AECP_WAITS` handlers); `aecp.h:100-127`; ruling 6421238472 items 1-6 and ruling 6425357821 items 1-3; `ctrl_memory.py:199-209` against ruling 6425357821 item 1 | R702-5 | `6d2b77bb3bfb8e2fbd30db56613c8c3b5ea0ef44` |
| RTL | UNCLEAN (F1, architecture/interface contract only; the HDL sub-check is clean) | The delta touches no `hdl/`, `tb/`, `syn/` or generated file (`git diff d33a5adc..6d2b77bb --stat`). The `mailbox.yaml` change is comment-only, with `gen_mailbox.py --check` at 0 findings. The datapath consumers of `aecp_locked` (`milan_datapath.sv:1325`, `:1673`, `:5012`, `:5024`, `:8167`, `:9372`) were read for F1's impact. The `applied` contract (`aecp.h:100-127`, `aecp_face.c:72-136`) and `mbx_face_commit` (`mbx.c:281-296`) were also read. Commit holding, decode, tags, reset, widths and coalescing are unchanged since the previous round's head | R702-5 | `6d2b77bb3bfb8e2fbd30db56613c8c3b5ea0ef44` |
| Robustness | UNCLEAN (F1) | The held-response bound (`AECP_HELD_BYTES` against each handler's `*bytes`) under ASAN at 1 and 2 interfaces; `transmit()` and `aecp_ready()` preventing response overwrite; `mbx_face_commit` FULL/BAD semantics against `applied()` while waiting; expiry during a wait; a second command during a wait | R702-5 | `6d2b77bb3bfb8e2fbd30db56613c8c3b5ea0ef44` |
| Tests | UNCLEAN (F1, F2, F3) | `test_aecp.cpp:711-857` and the new Face tests; `aecp_mutants.py` (round-5 plants); four own mutants; `test_ctrl_memory.py` and the author's ledger plants (`ledger-plants/summary.txt`) | R702-5 | `6d2b77bb3bfb8e2fbd30db56613c8c3b5ea0ef44` |
| Docs | UNCLEAN (F1) | `ARCHITECTURE_HW_SW_SPLIT.md:53-58`, `:104-112`; `MAILBOX_SPLIT.md:1239-1305` and the verification rows; `SPLIT_CONTROL_MEMORY.md` sections 3, 5 and 6; `FR_NFR.md:363`, `:374`; `aecp_face.h`; the live PR body (limits, timing, the three probe fixtures) | R702-5 | `6d2b77bb3bfb8e2fbd30db56613c8c3b5ea0ef44` |

## Prior findings at this head

I read these after my own pass and verdict. The reviewer probes were rerun by the author at `4e3aab32`; `sw/firmware/` is unchanged from there to this head. Each probe's sha256 in `author-r5/a680f/receipts/at-4e3aab32/probes/probe-hashes.txt` equals the published reviewer copy in the same packet's `MANIFEST.json`:

- `delta_probes.py` `01d60e9f…`
- `probe_ack.py` `bfaee807…`
- `late_ack_notify_probe.py` `a8d51f4b…`
- `response_probe.py` `9d018fe7…`

| Prior finding | Status at this head | Evidence |
|---|---|---|
| R702-4-F1 (MAJOR: getters, descriptor views and notifications present unapplied state after a failed SET) | **Resolved for every command change**. Its expiry read path remains, narrowed into the new **F1** | The waiting change is undone (`aecp.c:370-384`, `:582-606`, `swap`, `aecp_keep`), and the face writes nothing while it waits (`aecp_face.c:79`). Rerun of my unmodified probe, at 1 and 2 interfaces: `REVIEW getter: status=0 returned=0 last_acknowledged=0`, and no `REVIEW notification` line with the unacknowledged offset. The only failures are the fixture's first-frame status check (`test_aecp.cpp:1960` of the probe copy: expected 10, got 9, IN_PROGRESS by ruling 6421238472 item 1), as the PR body states. Permanent tests: `Core.AChangeThePlatformHasNotAppliedWaitsUndoneAndIsAnsweredOnce` (getter, READ_DESCRIPTOR, second command, each of the six commands timing out with the whole core state unchanged) and `Face.APendingChangeIsAnsweredOnceTheDatapathTakesIt`. Plants include `waiting-change-not-undone`, `face-publishes-while-a-change-waits` and `in-progress-reports-the-request` |
| R702-4-F2 (MAJOR: the automatic-unlock LOCK_ENTITY notification can be lost) | **Resolved** | `aecp.c:483-501` keeps `unlocked` until `applied`, then notifies once. Rerun of my unmodified probe at 1 and 2 interfaces: `REVIEW unlock recovery: applied=1 notifications=1 registered=1`, and `ReviewAutomaticUnlockMustBeNotifiedAfterRecovery` passes. Permanent tests: `Core.ALockExpiryIsNotifiedOnceThePlatformAppliedTheRelease` (including a full ring) and `Face.ALockThatExpiresWhileAChangeWaitsIsNotifiedOnceTaken`. Plants: `late-lock-release-never-notified`, `unapplied-lock-release-notified` and `waiting-expiry-not-deferred`. The notification is fixed; the read path during the same window is F1 |
| R701-4-F1 (MAJOR: a late-acknowledged change answers ENTITY_MISBEHAVING but still takes effect, and no controller is notified) | **Resolved** under ruling 6421238472, with ruling 6425357821 item 2 accepting the datapath window. Its "reads report the last acknowledged value during the hold" requirement is met for commands and not for the expiry (F1) | A failed change stays undone in the core, and the face is given the values in force. `MAILBOX_SPLIT.md` "The undone value after a failed change" and the PR body's limits name the window. Rerun of the unmodified `late_ack_notify_probe.py`: `PROBE held: core_identify=0 get_control_identify=0 datapath_identify=255`, then `PROBE after: datapath_identify=255 owed0=0 unsolicited_set_control=1`. That is, an acknowledgement within the bound is done and announced |
| R701-4-F2 (MINOR: a refusal echoes the request instead of the current fields) | **Resolved** | Every refusal goes through `aecp_foreign_lock` (`aecp_commands.c:18-21`), and each handler writes its current fields before or at its lock check: `stream_info` at `:323-338`, `lock` at `:490`, `control` at `:501`, `scalar` at `:265-268`, `configuration` at `:163`, `names` at `:213`. `Core.AChangeThePlatformHasNotAppliedPromisesNothing` compares the bytes, and the `refusal-reports-the-request` plant is in the campaign. My F1 probe shows the refused LOCK_ENTITY carrying the core's current `locked_id` (0). That is consistent with this rule; what the core holds there is F1's subject |
| R701-4-S1 (SUGGESTION: the image's `main` exits on an unacknowledged initial publication) | Unchanged, non-blocking | `ctrl_aecp_image.c:132-133` still returns 6. It stays a placement-switch boot-path item |
| R701-4-S2 (SUGGESTION: wording) | Partly taken, optional | `MAILBOX_SPLIT.md` now says "the 39 reads of 21 of the 25 class-D nets (4 are unread)". `census_ports.py:50` still reads "the #637 restore (#637)" |
| R702-3-F1 / R701-3-F1 (MAJOR: SUCCESS before an unacknowledged commit) | **Resolved** | Closed in round 4 except the part retained as R702-4-F1, which is resolved above. Rerun of the unmodified `probe_ack.py`: `response_status=10 core_identify=0 mailbox_identify=255`, so no SUCCESS promises the unwritten value. The mailbox's 255 is the accepted late-acknowledgement window. The unmodified `response_probe.py` passes at 1 and 2 interfaces |
| R702-3-F2, R701-3-F2, R702-3 and R701-3 residue | **Resolved** (round 4); not reopened | The delta touches only the commit-failure comment block of `mailbox.yaml` (`:444-449`); `gen_mailbox.py --check` reports 0 findings at this head |

R702-4 raised no RESIDUE or SUGGESTION.

## Real limits

- I did not rebuild the four RV32 images. The figures rest on the author's packet receipts (ELF hashes identical at `9e370841`; `sw/firmware/` is unchanged since `4e3aab32`) and on my arithmetic check.
- I did not rerun the whole firmware self-test, `aecp_mutants.py`, the census, the mbx bench, Yosys, OOC, `test_builder.py`, `behave`, the all-fabric export digest or all 69 docs gates. The delta since `4e3aab32` is docs, `ctrl_memory.py` and its test only, so the author's `4e3aab32` receipts stand for the rest, and hosted exact-head jobs corroborate them.
- The packet commit is unsigned; I verified its integrity only against its own manifest.
- Physical calibration was NOT RUN, and field skips are not hardware proof. The face block's datapath side and its CDC are unconnected until the placement switch (accepted limit).

## Pending manager duties

- Rule on F1 (fix, or accept the window and name it).
- Carry RES1 to RES3 to the residue checklist.
- Confirm the 4 in-progress hosted Verilator shards and fail-fast at this head.
- Build and validate the current-dev merge candidate on `dev-soft-core` (source base `e76a755a`; live dev `76de691e`) with the builder and native banks, and act, at the merge turn.

R702-5 FINISHED
