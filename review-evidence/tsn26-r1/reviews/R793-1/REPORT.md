[R793] NEGATIVE - exact head 3d57262c3614740244de40c40f667908ce6310f7

# R793-1: independent internal review of kebag-logic/tsn-c-stack PR #28 (issue #26)

- Exact head: `3d57262c3614740244de40c40f667908ce6310f7`, tree `3509cc6f61d6d6de89eb92f9aae9831b698d6368` (verified in the clone: `receipts/clone-state.txt`).
- Source base: `70936b77dc41981e192438388cd0aced69954f18`. Delta: one commit, 16 files, +801/-106.
- PR text says "Relates to #26". The parent's harness row needs the parent to bind its ready hook in a separate parent PR. This review accepts that scope.
- Verdict: NEGATIVE, on one open MINOR (F1). The code, conformance argument, docs contract, mutation claims, memory figures and cost figures all reproduce. F1 is a test-evidence gap: the PR says two command types are checked for an answer after redelivery, but the suite only checks that they are declined.

## Reconstruction order followed

1. CONTRIBUTING.md (the repository has no AGENTS.md), docs/ index (ARCHITECTURE, PORTING, REQUIREMENTS, TESTS, TRACEABILITY, VERIFICATION).
2. Issue #26: body and acceptance list. Its comments contain only the author's TAKEN and REVIEW READY markers; no maintainer comment narrows the scope.
3. PR #28 body and the public review-start comment. Linked authorities: ACMP-12 (new) and ACMP-09/03/08/02/PORT-01; IEEE 1722.1-2021 8.2.4, 8.2.5, Tables 8-1 and 8-3; Milan v1.2 5.5.2.3, 5.5.3.5, 5.5.4, Tables 5.26, 5.32, 5.34, 5.36, 5.43, 5.45, 5.47, 5.48.
4. `git diff 70936b77..3d57262` and history.
5. Public author evidence at milan-fpga `5d529acd`, `review-evidence/tsn26-r1`: all 16 files hash-verified against its MANIFEST.json.
6. Prior public review findings: none exist on PR #28 (0 review comments, 0 reviews; the only PR comment is the review-start notice) or on issue #26. There is nothing to resolve or retain.

## Answers to the focus questions

1. **Is declining and redelivering a conforming answer, and is the bound documented?** Yes.
   - In the core, every command addressed to this entity that is taken produces exactly one `respond()`. The room check now sits in `acmp_rx` (`src/acmp.c:1061`, `:1073`), before `talker_command`/`listener_command` act. A taken command therefore always gets its owed slot: `transmit` can return LOST only for the BIND_RX's own follow-on probe, which is recovered as before.
   - The served command receives its specified Milan response, not an error status. IEEE 1722.1-2021 Table 8-3 has no full-queue status, and `COULD_NOT_SEND_MESSAGE` belongs to a Listener's own command to a Talker.
   - The bound and its behaviour are stated in `docs/PORTING.md:74-91`: 8 × 80 = 640 bytes, the decline and redelivery order, the readiness query, the pass count, and the 200 ms budget made a port obligation. They are also in ACMP-12 (`docs/REQUIREMENTS.md`), `docs/ARCHITECTURE.md` and CHANGELOG.
   - This is the "deferred" option the issue allows. It holds only for ports that keep declined frames; the docs and PR state that a port ignoring the return value still loses the command.
2. **Does a declined command change no state, and is it answered in order and in time?** Yes.
   - The decline path runs `enter()` (which clears the per-entry `now_read` clock cache), then the frame checks, decode, one compare and `busy_declined++`. It returns before `finish`, so it makes no port call.
   - `DeclinedUnbindChangesNothingUntilItIsTaken` compares the whole instance, masking only those two fields.
   - `HeldEgressDefersTheCommandBehindTheOwedSet`: a 60 ms hold, then the answer 69 ms after arrival (= 60 + 9 one-ms passes) against the 200 ms of Milan Table 5.26. All nine answers leave in order. Passed in both of my suite runs.
3. **Is every command type covered, each per-command plant killed by exactly one test?**
   - Decline: yes, all 7 types.
   - Plants: all 22 new plants plus the updated `acmp-full-queue-acts` are CAUGHT (410/410 campaign). Run unfiltered on the full 106-test ACMP suite, each of the 7 per-command plants fails exactly one test (`receipts/full-suite-killers.txt`). All 23 failure sets match the author's escape evidence (`receipts/escape-evidence-crosscheck.txt`).
   - Answered after redelivery: committed tests cover only 5 of 7 types. BIND_RX and GET_TX_STATE are checked for the decline only, so the PR's "do the same for each of the other six" overstates the evidence. My disposable probe shows that behaviour is correct (F1).
4. **Memory and cost table matches the receipts?** Yes, exactly.
   - I rebuilt the published harness against exported base and head trees. All four measurement ELFs have the author's sha256 and byte-identical outputs: worst step 7882 → 7899 (+17) at rv32i -O3 and 24374 → 24381 (+7) at rv32im -Os; declined command 197 and 344; `acmp_rx_ready` 9.
   - `sizeof(struct acmp)` is 5064 B (RV32) and 5072 B (x86-64), and the owed set 640 B, on both base and head.
   - The Release smoke ELF is byte-identical to the author's base and final receipts. `.text` and `acmp.c` object text match (Release 34856 → 35752 and 18053 → 18213; Debug 45460 → 46928 and 20729 → 20869).
5. **Effect of the `busy_drops` → `busy_declined` rename on consumers:**
   - In this repository it is complete: header, source, tests, mutations, PORTING counter row, the port-contract checker and CHANGELOG; `grep` finds `busy_drops` only in the CHANGELOG entry that records the rename.
   - The semantics change too: each declined offer counts, so one command can count more than once. The rename makes any outside consumer fail to compile instead of silently misreading the counter, which is the right failure mode.
   - Outside this repository, the parent's mutant fragment still names `busy_drops` and must change when it adopts this. That belongs to the parent PR (pending).
   - The return type of `acmp_rx` changes from `void` to `bool`. Existing in-repo callers that ignore it (`examples/entity_roundtrip.c:242`, `examples/rv32/smoke.c:254-268`) never reach the bound.

## Findings

### F1: MINOR (Tests, Docs). The PR claims answered-after-redelivery coverage for BIND_RX and GET_TX_STATE, but the suite checks only their decline
- **Where:**
  - `tests/test_acmp.cpp:1097` (`AcmpCore.A19AFullQueueDeclinesTheCommandBeforeItActs`).
  - PR #28 body, "How to validate": "`AcmpOwed.TalkerCommandsBehindTheOwedSetAreAnsweredInTime`, `AcmpOwed.DeclinedUnbindChangesNothingUntilItIsTaken` and `AcmpCore.A19AFullQueueDeclinesTheCommandBeforeItActs` do the same for each of the other six command types."
  - The same claim is in the author's published handoff acceptance table.
- **Authority and evidence:**
  - Issue #26 acceptance asks that the further command be "answered, deferred or refused, within its 1722.1 timeout after the egress returns". The focus asks whether every command type is covered.
  - "The same" refers to the preceding bullet: fill, decline, state unchanged, release after 60 ms, specified answer within 200 ms, in order.
  - A19 fills the set and checks that BIND_RX and GET_TX_STATE return `false`, leave sink 1 UNBOUND, make no port call and count 2. It never releases the egress or redelivers, and asserts no BIND_RX_RESPONSE (Milan Table 5.32) or GET_TX_STATE_RESPONSE (Table 5.47).
  - No other committed test redelivers a declined BIND_RX or GET_TX_STATE. `A19AProbeWithoutRoomIsLostAndRecovered` covers a BIND_RX taken at 7 owed, but not after a decline.
  - Reviewer probe (`scripts/probe_redelivery.cpp`, `receipts/probe-redelivery.txt`): both are answered SUCCESS after redelivery, BIND_RX at 69 ms and GET_TX_STATE at 70 ms, in arrival order. So the behaviour is correct; the committed evidence is missing.
- **Impact:**
  - For two of seven command types, the "answered after the hold, within timeout, in order" property is asserted only in PR text, not by any test.
  - A later change could break service of a redelivered BIND_RX or GET_TX_STATE, for example by reserving a second slot wrongly or mishandling a re-offered GET_TX_STATE, and no ACMP-12 test would fail.
  - This is an evidence claim about tests, not pure wording, so under the owner rule it is not RESIDUE.
- **Required outcome (one of):**
  - (a) Preferred: add assertions, for example in an `AcmpOwed` test like the probe, that deliver a declined BIND_RX and GET_TX_STATE again after the hold. Assert their Table 5.32 and 5.47 responses within `kCommandTimeoutMs` and in arrival order, and list the test as an ACMP-12 killer of `owed-bind-rx-drop-restored` and `owed-get-tx-state-drop-restored` (TESTS/TRACEABILITY regenerated).
  - (b) Correct the PR text (and the published handoff) to say that A19 checks only the decline for these two types, and name the evidence for their service after redelivery.
- **Verification:**
  - `python3 scripts/validate.py --work <w> --jobs 16 --graphs` (test-inventory, traceability and mutation rc 0).
  - `python3 scripts/mutation.py --work <w> --select owed- --jobs 16` (all CAUGHT).
  - For (a), the new test fails when the redelivered BIND_RX or GET_TX_STATE answer is removed.
  - For (b), the PR text no longer claims an answer check that A19 does not make.

### S1: SUGGESTION (Robustness, Docs). A redelivered BIND_RX always loses its first probe
- **Where:** `src/acmp.c:296-307` and `:719-744`, `docs/PORTING.md:74-91`.
- **Evidence:**
  - A declined command is retaken as soon as one slot frees, so a BIND_RX is always taken at 7 owed. Its response takes the last slot, and its PROBE_TX_COMMAND is LOST: `probes_lost` = 1 in the reviewer probe, and the author's `bind_rx_owed_behind_7_probe_lost` step shows the same.
  - The probe is retried only after TMR_NO_RESP (200 ms). That is conformant (Milan v1.2 5.5.3.5.16) and existing ACMP-09 behaviour, but it adds about 200 ms to stream setup after every held-egress episode.
- **Suggestion:** state this in the owed-bound section, or let BIND_RX wait until two slots are free.

### S2: SUGGESTION (Robustness, Docs). Say when to redeliver relative to timer service
- **Where:** `docs/PORTING.md:79`; `src/acmp.c:296` (an owed probe from `acmp_timer_expired` takes any free slot).
- **Evidence (code reading):** if a port services `acmp_timer_expired` between the `acmp_poll` that freed a slot and the redelivery, a timer probe can take that slot, and the kept command is declined again. This is bounded by the probe timers, so it is not a livelock, but it adds passes the 200 ms budget does not count.
- **Suggestion:** say "deliver the kept frame right after the accepting `acmp_poll`, before timer service", as the test port model does.

No RESIDUE. The comment rule was checked over the delta's added lines: new source comments carry only requirement and clause IDs (`REQ: ACMP-12`, Milan and IEEE clause tags), with no bench lane labels, lane names, rounds, reviewer IDs or comment IDs.

## Lens results

| Lens | Result | Artifact-specific evidence |
|---|---|---|
| Conformance | CLEAN | Every taken own command gets one specified response (code reading of `listener_command`, `talker_command`, `bind`, `unbind`, `get_rx_state`). Decline before any state change. No error status invented (Table 8-3). The 200 ms of Milan Table 5.26 is met in tests (69 ms) and in the reviewer probe for BIND_RX and GET_TX_STATE (69 and 70 ms). Clause numbering is the 2021 edition; the issue's 8.2.2 is the 2013 numbering. Clause text was judged from repository citations and the clause content cited by the author, not re-read from the standards (see limits). |
| RTL | CLEAN | No HDL in the delta, so Verilator was not used. Applied to the bare-metal RV32 target: `baremetal.py` rc 0 (Debug and Release, QEMU smoke includes `acmp_owed_smoke`). Release ELF byte-identical to the author's final receipt, and the base Release ELF to the author's base receipt. Core object hashes identical. Two plants (`owed-listener-drop-restored`, `owed-ready-ignores-full`) each make the RV32 smoke exit nonzero and fail the gate (`receipts/rv32-plants/`). |
| Robustness | CLEAN | Bounded memory, unchanged (640 B owed set; `sizeof` 5064/5072 B, base = head). A declined offer costs 197 or 344 instructions instead of 5408 or 16522. Re-entry returns `false` and counts `reentries`, not `busy_declined`. Malformed, foreign and probe-response frames are still taken. Repeated offers are idempotent apart from the counter. Port receive-ring depth is documented as the port's. S1 and S2 are suggestions only. |
| Tests | UNCLEAN (F1) | 410/410 plants CAUGHT. Each per-command plant has exactly one full-suite killer (106 tests). Coverage 795/795 lines and 400/400 branches for `acmp.c`. GCC and Clang-sanitizer suites 8/8. Gap: no committed test checks the answer to a declined-then-redelivered BIND_RX or GET_TX_STATE. |
| Docs | UNCLEAN (F1) | PORTING contract, ACMP-12 requirement and record, TRACEABILITY, TESTS, VERIFICATION (406 + 4 plants), ARCHITECTURE and CHANGELOG are accurate against the code and receipts; the port-contracts gate passes. The PR text overstates the A19 coverage (F1). |

## Executed evidence (this review, exact head)

All commands ran from the clone at exact head with the pinned GoogleTest 1.14.0, clang-tidy 18.1.3 and clang-18 lexer (`scripts/env.sh`).
- `validate.py --jobs 16 --graphs`: **28/28 gates rc 0** (`receipts/validate/rc-all.txt`, `gates.json`). This includes the mutation campaign 410 CAUGHT / 0 ESCAPED / 0 ERROR, coverage `acmp.c` 795/795 and 400/400, static analysis rc 0 with clang-tidy 18.1.3, sanitizers, privacy, traceability, test inventory, port contracts and graphs (4 rendered).
- `baremetal.py --jobs 16`: rc 0, Debug and Release (`receipts/rv32/`).
- Cost and memory reproduction: `scripts/measure.sh` and `scripts/sizes.c` (`receipts/measure/`, `receipts/sizes.txt`, `receipts/image-sizes.txt`).
- Full-suite killer matrix: `scripts/full_suite_killers.py` (`receipts/full-suite-killers.*`).
- Disposable probes run in exported copies only: `scripts/run_probe_redelivery.sh` and `scripts/rv32_plant_smoke.sh`.
- Hosted CI at the exact head, inspected only (`receipts/hosted-checks.txt`): push run `42465161105` quality and bare-metal success, every step executed; PR run `42465171643` quality and bare-metal success. Hosted and act acceptance belong to the manager.
- The clone was restored and verified after the probes: worktree and index equal HEAD, index tree = `3509cc6f…`, 98 files all mode 100644, no gitlinks required or present, zero untracked or ignored files (`receipts/clone-state.txt`).

## Reviewer ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `src/acmp.c` (acmp_rx, room, transmit, respond, listener/talker handlers, bind/probe), `include/acmp.h`, ACMP-12 in REQUIREMENTS/requirements.json, PORTING owed-bound section, issue #26 acceptance, PR clause argument, reviewer redelivery probe | R793-1 | 3d57262c3614740244de40c40f667908ce6310f7 |
| RTL | CLEAN | `examples/rv32/smoke.c` `acmp_owed_smoke`, `cmake/rv32.cmake`, `scripts/baremetal.py`, RV32 ELF and object hashes (base and head), two RV32 plant runs | R793-1 | 3d57262c3614740244de40c40f667908ce6310f7 |
| Robustness | CLEAN | decline and re-entry paths, owed-set memory, instruction counts (4 reproduced measurement ELFs), `sizeof` on both targets, receive-ring ownership text | R793-1 | 3d57262c3614740244de40c40f667908ce6310f7 |
| Tests | UNCLEAN (F1) | `tests/test_acmp.cpp` (A19 rewrite, AcmpOwed fixture and five tests), `tests/mutations.json` (22 new plants plus 1 updated), coverage ratchet, full validate run, full-suite killer matrix, author escape evidence cross-check | R793-1 | 3d57262c3614740244de40c40f667908ce6310f7 |
| Docs | UNCLEAN (F1) | PORTING, REQUIREMENTS, requirements.json, TRACEABILITY, TESTS, VERIFICATION, ARCHITECTURE, CHANGELOG, `scripts/check_port_contracts.py`, `scripts/requirement_records.py`, PR body, comment-rule scan of added lines | R793-1 | 3d57262c3614740244de40c40f667908ce6310f7 |

## Real limits

- The Clang sanitizer arm ran with the host Clang 23. The pinned Clang 18 cannot parse the host's GCC 16 C++ standard library, so it was used only as the lexer the gates call. CI's Ubuntu 24.04 Clang 18 arm is covered by the hosted run, not by this review.
- My first validation attempt aborted early because `clang-18` was not on PATH (a setup error: six lexer-dependent gates failed with "No such file or directory"). That run was discarded unpublished, and the full kit was rerun from a clean work directory with all 28 gates rc 0.
- Debug ELF byte counts depend on the build path (debug info), so the PR's Debug ELF bytes (141440 → 144192) were not reproduced; mine are 142320 → 144376. Debug `.text` and object text match exactly.
- The IEEE 1722.1-2021 and Milan v1.2 texts were not available here. Clause content (8.2.4, 8.2.5, Tables 8-1 and 8-3, Milan Table 5.26 and response tables) was judged from the repository's existing citations, the code's per-response clause tags and the author's quoted clause content, not re-read from the standards.
- The parent's harness row ("an ACMP command behind the owed input") has no answer time. It needs the parent PR that binds the ready hook, so issue #26 stays open by design.
- Physical calibration was NOT RUN. No hardware was used, and field skips are not hardware proof.
- No manager source bank runs at this head, and none is claimed or inferred here. Source-head execution evidence is the author's published receipts plus this review's own runs above.

## Pending manager duties

- Build and validate the current-dev merge candidate (source base 70936b77 against live dev 0a75aa774b89ac89351700f63dd8cbb89694af6c; builder and native banks) at the merge turn, and link those receipts on the PR.
- Own hosted and act acceptance (the PR run showed success at inspection).
- Track the parent PR: bind the parent's ACMP receive-ready hook to `acmp_rx_ready` (or keep declined frames), rename `busy_drops` in its mutant fragment, then measure the harness row.
- Obtain the second independent positive review after F1 is resolved, and carry S1 and S2 as optional suggestions.

R793-1 FINISHED
