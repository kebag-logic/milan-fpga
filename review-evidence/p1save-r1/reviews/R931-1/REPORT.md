[R931] NEGATIVE - exact head 166dfdc9fd2f22a9d2acd272bac4d1a5e3462f3e

Round R931-1, PR #1014 (Refs #1009, #876) on `dev-soft-core` `5de21ff3661436ea5598718aca36934361e35340`, 18 commits, tree `08861f5484fad777532ecd5faa89af199e18a87a`. Cleared context; reconstructed from the repository, #1009's body and its two rulings (7167783205, superseded by 7170938286), #876, #920, #1012, the diff and history, and the author packet. No other review of this PR was read; the comment index showed one other reviewer's first line and nothing else of it. No finding from an earlier round existed when this round started.

The core mechanism holds up: a torn delta frame is never applied, the authoritative slot is never written, the window arithmetic matches the ruling, and the planted campaign reproduces. Three MAJOR findings stand, on what the change breaks, what its gate does not hold, and what its tests do not see. Strict save-before-response (#1012) and the board items are not counted as defects.

## Findings

**R931-1-F1 MAJOR - Tests, Conformance, Docs** - `tb/verilator/nvm_split_target/target_cases.py:150`, `target_grade.py:329`, `README.md:102`: the split-target boot and restore campaign fails at this head.
- Authority/evidence: #1009 acceptance 2 (the affected campaigns pass, "boot and restore" among them). The `commit` case marks every record changed at boot, then sends SET_NAME and BIND_RX about 375 ms in, relying on one 1,000 ms window, and requires one erase. The binding records it marks now end the window at 100 ms. Run at 1x1 on base and head with the harness's own simulation; its own commit grade, applied to each finished run (`receipts/split_target_commit_1x1.txt`):
  - base: first erase at 1,045.7 ms, 1 erase, 14 pages, no finding;
  - head: erases at 145.8 and 491.6 ms, 2 erases, 28 pages; three findings (two blocks, not one; the container read holds neither the saved name nor sink 0's binding).
- Impact: the case fails, and the harness derives the `saved`, `torn` and `version` journals from it and refuses a container without the saved name, so the campaign cannot grade restore at this head. The harness is untouched by the diff, and no gate in the packet runs it. Its stated time model (`commit_ms`, "waits 1,000 ms after the first change") is also stale.
- Required outcome: the campaign passes at both its points, its case and documents matching the two windows, without weakening what `commit` requires of the container.
- Verification: the whole campaign, every case and control, at both points at the new head.

**R931-1-F2 MAJOR - Conformance, Robustness, Tests, Docs** - `sw/firmware/ctrl_nvm/nvm_store.c:1261-1292`; PR body ("always the new binding from the gate value on"); `docs/design/SPLIT_CONTROL_MEMORY.md:1924`: a bind that arrives in another save is not durable within 800 ms.
- Authority/evidence: ruling 7170938286 acceptance 1 (whole-commit path at most 800 ms) and 2 (always new from the gate value on). Every bind-timing gate starts from a store with no other save in flight. With the PR's own harness and grade at 8x8/1if, `BUDGET_FLASH_US=120000:500`, no other load, a SET_NAME on blank flash and a BIND_RX at that save's erase: `BIND r931-bind-flight: ... durable 890.730 ms after its response (sink 0; target 800 ms) ... OVER` (`receipts/r931-bind-flight-8x8-1if.txt`, the script and diff beside it). The bind waits out the rest of one whole commit, then needs a second. On a settled store the second is whole too, since the other slot lacks the name's record and the span from a binding to a name does not fit a frame (by the code; the host probe in `receipts/probe_store_tidy_and_inflight.txt` shows the two whole commits). The packet's own `save-flight` at 964.7 ms shows the same two-commit length. The board ran about 3 % above this model.
- Impact: naming an entity and binding within about 1.0 to 1.5 s is ordinary controller behaviour; a cut 800 to 890 ms after the response restores the old binding. The ruling's own next-window rule makes the wait inherent, so the breach may be an unstated condition of the gate rather than a wrong rule, but it is neither stated, measured nor ruled.
- Required outcome: the gate is met for a bind that arrives during any save, or the bound for that case is measured, stated in the documents and PR, and ruled on publicly. Either way a test holds the figure.
- Verification: a harness group for a bind in a whole save in flight at both points, plus a swept cut that starts inside another record's save.

**R931-1-F3 MAJOR - Tests, Robustness** - `sw/firmware/ctrl_nvm/test/test_nvm_delta.cpp:124,276,414`, `test_nvm_window.cpp:165,193`: defects that lose durable changes survive the whole suite.
- Evidence: the 189 planted defects all redden here too, but these reviewer mutants leave every check green (`scripts/r931_mutants.py`, `receipts/mut*.txt`):
  - `whole_commit_no_lag` (a whole commit records no lag, `nvm_store.c:1107`): survives at 1x1 and 8x8. The next frame omits what the whole commit saved.
  - `fail_forgets_span` (a failed attempt drops the span it took, `nvm_store.c:979`): survives at 1x1 and 8x8. The frame after the retry omits that change.
  - `tidy_fail_drops_inflight` (a failed full-room commit forgets a change that joined it): survives at 8x8. The change is never saved.
  - `reserve_one_frame` (a reserve of one largest frame, not two): survives at 8x8, because `room_reserve` takes the reserve from the header under test.

  The first two are not equivalent: two tests added to a disposable copy (`scripts/r931_kill_tests.py`) pass on the head and fail on both ("does not boot back": the frame's slot is refused at boot). The existing cases with a whole commit before a frame change the same record again, so the lag is never distinguishable from the save's own span. Line and branch coverage of 100 % does not see it.
- Impact: the lag is the invariant the frame format rests on; a regression in it reports a save durable that the next boot discards.
- Required outcome: tests that fail for each, with different records across whole-then-frame and retry-then-frame sequences, a change that joins a full-room commit that fails, and a reserve stated apart from the implementation.
- Verification: the four mutants planted in `nvm_mutants.py` and caught.

**R931-1-F4 MINOR - Conformance, RTL, Robustness, Tests** - `sw/firmware/ctrl_nvm/nvm_store.c:979-990` (and the claim at 973-978): DR2c is broken when a change joins a full-room commit that fails.
- Authority/evidence: `SAVED_STATE_MATERIALIZATION.md` DR2c: at most three firmware transaction attempts per unchanged captured work set, 1,000 ms apart. `nvm_idle` sets `tidy` and starts a capture; a change marked before its capture step joins it (`nvm_mark`). `nvm_fail` then returns early: no attempt counted, no backoff, `stale` not set, while the change stays in flight. Probe, 8x8 and 1x1, both ports (`receipts/probe_store_tidy_and_inflight.txt`): on the model port, failures at 5.8, 11.7, 1,017.5 and 2,023.3 ms after the change at 8x8: four attempts, the second 5.9 ms after the first; the same at 1x1.
- Impact: a narrow race plus a media fault gives a fourth attempt, one without spacing, and a claim not marked stale while an acknowledged change is out of every slot. "Leaves no work out of a slot" is false there.
- Required outcome: a full-room commit that took a change is an attempt under DR2c.
- Verification: a test of that sequence, with a planted defect.

**R931-1-F5 MINOR - Robustness, Conformance, Docs** - `docs/design/SAVED_STATE_FORMAT_32X32.md:394-396`, `nvm_store.c:444-452`: rolling back and forward loses the binding saved under the rolled-back image.
- Authority/evidence: the format page states rollback as supported. A minor 0 reader picks by container sequences alone, so its next save can take a sequence below the other slot's frames. Forward again, the frames win. Probe at the 4x4 shape, both ports: slot A minor 0 at 7 with the new binding, slot B container 6 and a frame to 8: the boot takes slot B and restores the pre-rollback binding (`receipts/probe_rollback_then_forward.txt`). One save after the rollback is enough; a second one heals it. `SAVED_STATE_FASTCONNECT.md` section 6.2 also limits a minor to added records, stated there for major 2.
- Impact: a durable, answered binding is lost silently and an older one restored.
- Required outcome: the forward boot does not prefer frames over a later minor 0 save, or the limitation is stated where rollback is claimed, with the minor rule for major 3.
- Verification: a test with both slots in that state.

**R931-1-F6 MINOR - Tests, Conformance** - author packet `receipts/gates.txt`, `measure.txt`: the CPU bounds were not executed at this head.
- Evidence: each point's run grades six groups (the store's saves). `save-held`, `save-starved`, `save-second`, the 72 staged save windows, and the notice, AECP, ACMP and shutdown rows have no receipt here, although a first bind now starts its save 900 ms earlier in every group that has one. #920's 5 s contract is stated under the contract's held load (ruling item 5 keeps it). What this round did run holds: the static load gate (0.512 at 1x1/1if against 0.70; 0.744 at 8x8/1if against 0.75, so also under the 0.76 named for this round; `receipts/load_grade.txt`), the 1x1/1if flip check, the tier model's 1,033 controls, and one staged window, `backlog-adp@blank-0` at 8x8/1if: 0 refusals, 0 budget misses, 0 of 340 passes over the share, longest step 0.803 ms (`receipts/window_backlog-adp_blank-0_8x8-1if.txt`).
- Required outcome: the full service-budget run at 1x1/1if and 8x8/1if at the new head, the notice bound of 140 ms, ACMP's 30 ms and THE SHARE among its rows.
- Verification: both runs' `results.json` and exit status.

**R931-1-F7 MINOR - Tests, Docs** - `tb/verilator/ctrl_service_budget/bind_save.py:196-213`: the bind grade does not hold what it states.
- Evidence: its text says a burst that left a save with an erase fails the run; nothing tests `erases` or `frames`. Over synthetic logs a `frame` group whose one save is whole, and a burst of whole saves, return no miss (`receipts/probe_bind_grade.txt`). A frame group that silently became whole passes wherever the whole commit takes under 250 ms. The results also do not record whether the flash times were modelled, so a run without them prints the same verdict line.
- Required outcome: each group fails unless its saves are of the kind it times, the burst's erases are graded as stated, and the run records the flash times it used.
- Verification: self-test mutants for each.

**R931-1-F8 MINOR - Docs** - figures and statements that are wrong at this head:
- `sw/firmware/ctrl_nvm/README.md:589` "81 checks in 136 tests: 55 on both ports" and `:762` "152 defects"; measured: 162 tests a shape (67 checks on both ports, the rest on one port, the codec or the mock) and 184 defects plus the five controls. The base's figures were stale and this change added to them.
- `sw/firmware/ctrl_nvm/README.md:774` "a flash model whose erase and program waits are zero": the bind figures above it model them.
- `docs/design/SPLIT_CONTROL_MEMORY.md:331`: "`LEDGERED` holds ... 64.5 ... 59.5 ... 61.5" is the pre-change ledger; the code holds 65.0, 60.0, 62.5 and 58.0.
- `tb/verilator/ctrl_service_budget/README.md:90` and `save_window.py:13-17,197-198`: the staged windows' save no longer waits out the SET_NAME's 1,000 ms window; their bind ends it 100 ms after itself.
- Required outcome: each corrected. Verification: the counts printed by the gate, the ledger test and the text agree.

**R931-1-F9 MINOR - RTL, Robustness, Docs** - `sw/firmware/ctrl_nvm/nvm_store.c:287-339,458-470`; `nvm_shape.h:162`; `README.md:291`: the boot cost of frames is not stated, measured or gated.
- Evidence: each applied frame re-judges the whole container (CRC-32 and every record's crc16), and the chosen slot's chain is walked again at the re-stage. The service-budget image of this head at 8x8/1if on the simulated split CPU (`receipts/boot_cost_8x8-1if.txt`): ready at 635.1 ms with two slots and no frame, 4,422.7 ms with both rooms full (16 frames each), 77 to 80 ms a frame on each of three walks. Eleven frames in each slot, about where an idle commit empties the room, add about 2.6 s by the same rate (not run). A slot whose frames end torn is read twice, which adds a walk. The documents state only that a boot reads at most 4,096 bytes more a slot.
- Impact: up to 3.8 s of boot with AECP held. It is inside the 20 s advertisement and 30 s restoration windows of REQUIREMENTS section 8, but seven times the restore without frames, and no gate sees it.
- Required outcome: the worst boot time is measured, stated and bounded by a gate, or the walk's cost reduced.
- Verification: a boot with full rooms at both shapes.

**R931-1-F10 MINOR - Conformance, RTL, Docs** - PR body, packet `receipts/images.txt`: fit evidence is incomplete against what is claimed.
- Evidence: the PR body says the routed difference (+1.0 tile at 8x8/1if, 98.5 to 99.5; +1.5 at 1x1/1if, 80.5 to 82; the same directive in each pair) is "recorded as S14 debt too". No tracked file records it; the ledger and `SPLIT_CONTROL_MEMORY.md` record the planned +0.5 only, and the difference is not attributed. Acceptance 5 asks fit and timing at both 8x8 points; the two-interface point has a planned figure and no routed image or timing.
- Required outcome: the routed difference attributed, or recorded where the debt is kept; the two-interface point's fit and timing shown or released by a public ruling. Raising the two-interface fixture entry to 62.5 is within the owner's rule and is not disputed.
- Verification: the ledger text and the routed utilisation agree.

**R931-1-F11 RESIDUE - Docs** - `sw/firmware/ctrl_nvm/host/nvm_fmodel.c:80`: the new function was inserted between `fm_other_slot` and its comment. Exact fix: move "The address a read-alias answers from: the same place in the other slot." to the line before `fm_other_slot`.

## Focus items checked and held

- Two-slot atomicity: a frame is applied only with a closing CRC, a matching `prev`, a newer sequence and a re-judged container; frames left by a partial erase cannot chain (their `prev` is older). The torn, full-area, previous-minor and 2509db68 tests pass at both AX7101 shapes; the other shapes have no old store by design.
- Window arithmetic: first change, not restarted, earliest end, the whole dirty set, the next window for a binding change in flight; 1,000 ms kept for the records below and above the block; the burst of 64 converges. Bind, unbind, and started/stopped reach the same binding record (`ctrl_app_aecp.c`).
- Swept cut 0 to 3 s: old or new, never neither, new from the gate, from a store with no other save in flight (see F2).
- Planted defects: the gate re-run here at five shapes, 826 tests, all 189 reddened, exit 0 (`receipts/store-selftest.log`).
- Memory: the ledger test passes at this head (0 failures). The images' firmware equals the final head's by the packet's identity receipt, and both chosen images meet the floors at every corner; not rebuilt here.
- Wear: a frame erases nothing; an idle commit follows about eleven frames a slot. No lifetime figure is published, and none is required by the ruling beyond the burst's counts.
- Comment and privacy rules: no new instance in the added lines; the documentation check passes.

## Ledger (reviewer-owned)

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1, F2, F4, F5, F6, F10) | #1009 rulings and acceptance, Milan v1.2 clauses as the ruling cites them, DR2a/DR2b/DR2c, `nvm_store.c` window and attempt paths, `ctrl_app_aecp.c` mark path | none clean | `166dfdc9fd2f22a9d2acd272bac4d1a5e3462f3e` |
| RTL | UNCLEAN (F4, F9, F10) | no HDL in the diff; the store's state machine (`nvm_step`, `nvm_fail`, `nvm_idle`, `nvm_chain`), `ctrl_memory*.py`, routed reports, boot cost on the split CPU | none clean | `166dfdc9fd2f22a9d2acd272bac4d1a5e3462f3e` |
| Robustness | UNCLEAN (F2, F3, F4, F5, F9) | torn, full-room, minor 0, read-fault, refused-slot and in-flight paths; host and split-CPU probes | none clean | `166dfdc9fd2f22a9d2acd272bac4d1a5e3462f3e` |
| Tests | UNCLEAN (F1, F2, F3, F4, F6, F7) | `test_nvm_delta.cpp`, `test_nvm_window.cpp`, `nvm_mutants.py`, `bind_save.py`, `save_burst.py`, their self-tests, `nvm_split_target` | none clean | `166dfdc9fd2f22a9d2acd272bac4d1a5e3462f3e` |
| Docs | UNCLEAN (F1, F2, F5, F7, F8, F9, F10) | `ctrl_nvm/README.md`, `SAVED_STATE_*`, `SPLIT_CONTROL_MEMORY.md`, budget and split-target READMEs, PR body | none clean | `166dfdc9fd2f22a9d2acd272bac4d1a5e3462f3e` |

## Limits

- Focused evidence only: no full parent, sub-processor, builder or synthesis bank, no routed build, no board. The host was heavily shared, so simulations were single groups: one staged window of 72, one bind-in-flight point (8x8/1if), one split-target case (1x1), one boot shape (8x8/1if). The author's 134.3, 561.5 and 155.3 ms figures were read, not re-run. The harness self-test, the coverage run, the platform ledger and the image builds were not re-run either.
- The split-target runs' own report writer was stopped while still grading; F1's verdict is its commit grade called directly on the two finished runs' journals and flash operations.
- F2's 890.7 ms is the harness's modelled flash, not the board. For F5 the rolled-back image's choice was read from the base's code; only the forward boot was run.
- Early builds and the planted campaign briefly ran more than 16 parallel compile jobs, because a harness build passes its own job count.
- Early in the round one over-broad process match ended a setup command of this round's own, and one file search across the host listed path names outside the review area; no such file was opened. Process matching was then anchored to this packet's paths. No other process is known to have been signalled.

## Pending manager duties

- A ruling on F2's condition (the bound for a bind in a save in flight) and on F10's two-interface fit and timing.
- Board items, stated as owed: BIND_RX response to durable at both shapes, the four power-cycle scenarios with one on a full-room commit; physical calibration NOT RUN.
- The current-dev merge candidate's builder and native banks; no hosted check was reported on this branch, and no manager source bank is claimed.
- Re-review at the corrected head: every lens is uncovered.

R931-1 FINISHED
