[R794] NEGATIVE - exact head 3d57262c3614740244de40c40f667908ce6310f7

# R794-1: external independent review of kebag-logic/tsn-c-stack PR #28 (issue #26)

- Exact head `3d57262c3614740244de40c40f667908ce6310f7`, tree `3509cc6f61d6d6de89eb92f9aae9831b698d6368`. Source base `70936b77dc41981e192438388cd0aced69954f18`. The delta is one commit: 16 files, +801/-106, a one-line subject with no body.
- Scope accepted as published: "Relates to #26", not "Closes". The parent's harness row needs the parent to bind its receive-ready hook, which is a separate parent PR.
- Verdict: **NEGATIVE**, on one open MINOR (F1, Tests and Docs).
  - The code, the conformance argument, the docs contract, the memory and cost figures, the mutation claims and both targets all reproduce at this head.
  - F1: the PR says that, for BIND_RX and GET_TX_STATE, the tests show the deferred command is answered after the egress returns. The suite only shows that these two are declined. A reviewer probe shows both are in fact answered in 69 ms, so the fix is to add the assertions.

## Reconstruction order

1. `CONTRIBUTING.md` (the repository has no `AGENTS.md`) and the docs index: ARCHITECTURE, PORTING, REQUIREMENTS, TESTS, TRACEABILITY, VERIFICATION and COVERAGE.
2. Issue #26:
   - Body and acceptance: the command is answered, deferred or refused within its timeout after the egress returns; a planted silent-drop mutant is caught; the parent harness row gets an answer time.
   - Comments: only the author's TAKEN and REVIEW READY markers. No maintainer comment narrows the scope.
3. PR #28 body and the public review-start comment.
4. Authorities: ACMP-12 (new), ACMP-09, ACMP-08, ACMP-03, ACMP-02 and PORT-01; IEEE 1722.1-2021 8.2.4, 8.2.5, Tables 8-1 and 8-3; Milan v1.2 5.5.2.3, 5.5.3.5 and 5.5.4, Tables 5.26, 5.32, 5.34, 5.36, 5.43, 5.45, 5.47 and 5.48.
5. `git diff 70936b77..3d57262` and history.
6. Public evidence, milan-fpga `5d529acd`, `review-evidence/tsn26-r1`:
   - All 17 files were fetched.
   - Every published sha256 matches its `MANIFEST.json` entry. Two files are path-redacted, as the manifest declares.
7. Hosted checks at the exact head.

Disclosure: the read-only listing of PR comments I used to find the review-start comment printed the first lines of the other reviewer's report. Those lines were its verdict line and a one-sentence summary of its finding. I read nothing further of that report until this verdict and ledger were written. F1 below comes from my own reading of `deliver()` and the A19 test, and from my own probe.

## What the change does (verified in source)

- `src/acmp.c:1061-1063` and `:1073-1075`: with all `ACMP_OWED_MAX` (8) slots owed, a talker or listener command addressed to this entity returns `false`. This happens after the frame checks and decode, but before `talker_command`, `listener_command` or `finish`. So there is no port call, no publish, no persist, no change notification and no timer re-arm.
- `room()` (`src/acmp.c:327-334`) now counts `busy_declined`. The two inner `room()` tests in `listener_command` and `talker_command` were removed. `acmp_rx` is the single decline point.
- Malformed frames return `true` (`:1050`). Foreign commands, probe responses and unknown messages return `true` after `finish` (`:1094`). Refused re-entry returns `false` (`:1045`).
- `acmp_rx_ready` (`:1037-1040`) is `!in_port && owed_count < ACMP_OWED_MAX`. That is exactly the complement of the two decline conditions, so a `true` answer guarantees `acmp_rx` takes the frame.
- Each served command emits exactly one response through `respond()`. Because `room()` guarantees one free slot, the response can never be `LOST`. A BIND_RX taken with exactly one free slot still loses its first probe, as on main (see S1).

## Lens results

### Conformance: CLEAN

- **(1) Decline and redeliver answers the issue.**
  - IEEE 1722.1-2021 8.2.4 and 8.2.5 answer every received command through `txResponse`. Table 8-3 has no status for a full output queue.
  - The PR's reading of `COULD_NOT_SEND_MESSAGE` is consistent with the clause structure the repository cites. That status belongs to a Listener whose own command to a Talker could not be sent.
  - Holding the command at ingress and serving it normally gives the Milan-specified response, for example SUCCESS for GET_RX_STATE in UNBOUND (Table 5.34). An error frame would not leave sooner while the egress is held.
  - The bound and its behaviour are stated in `docs/PORTING.md:74-91`: 8 × 80 = 640 bytes, the decline, the redelivery order, the readiness query, the pass count `ACMP_OWED_MAX` + 1, and the 200 ms budget that the port's hold plus delay must meet. They are also stated in ACMP-12 (`docs/REQUIREMENTS.md`).
- **(2) Ordering and timing.**
  - The answer leaves 69 ms after arrival for a 60 ms hold, in the pass after the eight frames owed ahead of it. All nine answers leave in order.
  - Reviewer hold sweep (`receipts/probe-owed.txt`): hold 0/60/131/191/192 ms gives answers at 9/69/140/200/201 ms. The core adds exactly `ACMP_OWED_MAX` + 1 passes, and the docs place the hold budget on the port.
  - Re-entry and readiness semantics are consistent with the existing PORT-01 contract.
- Limit: the standards texts are not in the clone. Clause numbers and titles were checked against the repository's own clause usage (`include/acmp.h`, `docs/REQUIREMENTS.md`) and the PR's reasoning, not against the published PDFs.

### RTL (core implementation and targets): CLEAN

This repository has no HDL. The lens was applied to the C core and both build targets.

- Hosted (Linux x86-64), my own run of `scripts/validate.py --jobs 8` at the exact head: 27/27 gates rc 0 (`receipts/validation/gates.json`).
  - GCC Debug build and tests; Clang address and undefined-behaviour sanitizers; static analysis with clang-tidy 18.1.3 (CI's version) and cppcheck 2.22.0; boundary, comments, port contracts, traceability, privacy; mutation; mutation controls.
  - The graphs gate was not run (see limits).
- Bare-metal RV32 (`scripts/baremetal.py`): Debug rc 0 and Release rc 0, and both smoke logs end "ADP, ACMP and MAAP smoke checks: rc 0".
  - The Release ELF sha256 `a9fad2c0…f356` is byte-identical to the author's receipt.
  - The Debug ELF differs only in bytes, because debug info embeds the build path. `.text` matches.
- Hosted CI at the exact head (`receipts/hosted-checks.txt`): the push and pull_request runs both executed the `quality` and `bare-metal` jobs, and every step concluded success. None was skipped.
- **(4) Memory and cost**, reproduced independently:
  - Struct sizes, measured on both targets at base and head with a compile-time size probe (`scripts/sizes.sh`, `receipts/struct-sizes.txt`):

    | Quantity | x86-64 base → head | RV32 base → head |
    |---|---|---|
    | Owed array | 640 → 640 | 640 → 640 |
    | One owed entry | 80 → 80 | 80 → 80 |
    | `owed_head` and `owed_count` | 4 + 4 → 4 + 4 | 4 + 4 → 4 + 4 |
    | `sizeof(struct acmp)` | 5072 → 5072 | 5064 → 5064 |

  - Instructions retired: I rebuilt the published harness against base and head with my own script (`scripts/measure_cost.sh`) and ran it under QEMU `-icount shift=0`. All four outputs (rv32i -O3 and rv32im -Os, base and head) are byte-identical to the author's result files. That includes the worst measured step 7882 → 7899 (+17) and 24374 → 24381 (+7), 197 and 344 for a declined command, 9 for `acmp_rx_ready`, and the `acmp.c` object text 18053 → 18213 and 10697 → 10689 (`receipts/cost/`).
  - Image sizes (`receipts/rv32-image-sizes.txt`):
    - Release ELF 46552 → 47512 bytes, `.text` 34856 → 35752.
    - Debug `.text` 45460 → 46928.
    - `acmp.c` object text: Release 18053 → 18213, Debug 20729 → 20869.

### Robustness: CLEAN

- A declined command changes no state. In my probe (`DeclineByteImage`), a whole-instance byte image taken before and after a declined UNBIND_RX for a bound sink, with no field masked, shows exactly two changed bytes:
  - `busy_declined`, as documented;
  - the per-entry scratch flag `now_read`. `enter()` clears it on every entry and only `now()` reads it, within the same entry, so it carries no state between calls.
- Repeated offers each count and change nothing else (`RepeatedOffersEachCount`: 3 offers give `busy_declined` 3, no calls).
- A declined command for an unknown listener unique ID is answered LISTENER_UNKNOWN_ID after redelivery.
- Liveness: the owed set drains only through `acmp_poll` accepting a frame, and nothing on the receive path consumes a slot without the port. While the egress is held, nothing can leave. There is no deadlock: declining depends only on egress progress.
  - A port that runs a timer between `acmp_poll` and redelivery can let a DELAY-expiry probe take the freed slot. The command is then declined once more and taken on the next pass. Order is preserved, and the extra delay is bounded by one pass per expiring sink.
- **(5) Rename and consumers.**
  - In-repository consumers were all updated: the header, the PORTING counter row and `scripts/check_port_contracts.py`. `busy_drops` now appears only in the CHANGELOG line that records the rename.
  - Parent firmware at live dev `0a75aa77`, read-only: every `acmp_rx` call site uses the call as a statement (`acmp_mbx.c:111`, `acmp_walk.cpp`, `test_acmp_nvm.cpp`, `test_maap_mbx.cpp`), so the `void` → `bool` change compiles there unchanged.
  - The only parent reference to the renamed field is the mutant fragment at `sw/firmware/ctrl/test/acmp_mutants.py:452-453`. It no longer matches once the gitlink moves. The AECP `busy_drops` is a different counter.
  - The parent already has `ctrl_loop_set_rx_ready`, so the deferred harness row is reachable without further core changes.

### Tests: UNCLEAN (F1)

- **(3) Per-command plants.**
  - My own full mutation campaign at the exact head gives 410 CAUGHT, 0 ESCAPED, 0 ERROR. That is 406 core plants and 4 generated configuration plants; all 22 new `owed-*` plants and the updated `acmp-full-queue-acts` are CAUGHT (`receipts/validation/mutation-summary.txt`).
  - I applied each of the 7 per-command plants on its own (`scripts/plant_probe.py`, `receipts/per-command-plants.json`). Each fails exactly one test of the full ACMP suite, and each escapes with rc 0 when that one test is excluded. This matches the author's escape evidence.
  - The RV32 smoke check kills both `owed-get-rx-state-drop-restored` and `owed-listener-drop-restored`, with smoke code 92 (the `acmp_owed_smoke` decline check) in Debug and Release (`receipts/rv32-plant-exit-codes.txt`).
  - Coverage: `src/acmp.c` 795/795 lines and 400/400 branches, with no new exclusion.
- Gap (F1): BIND_RX and GET_TX_STATE are only asserted to be declined. No test redelivers them and checks their answer.

### Docs: UNCLEAN (F1, PR text only)

- The PR body's "How to validate" claims answered-after-redelivery coverage that two command types lack (F1). That is a test-evidence claim, not pure wording, so it is not RESIDUE.
- PORTING "ACMP owed bound", ACMP-12 in `REQUIREMENTS.md` and `requirements.json`, the generated TRACEABILITY and TESTS rows, VERIFICATION (406 core plants and the RV32 smoke row), ARCHITECTURE and CHANGELOG are consistent with the code and with each other. The port-contracts gate enforces the critical phrases.
- Comment rule: the new source comments are `REQ:` tags and clause citations only. No bench lane label, lane name, review round, reviewer ID or issue-comment ID was added to source, tests, scripts or docs. The commit is a one-line subject.

## Findings

### F1: MINOR (Tests, Docs). Deferred BIND_RX and GET_TX_STATE are never shown to be answered

- **Where:**
  - `tests/test_acmp.cpp:1097-1113` (`A19AFullQueueDeclinesTheCommandBeforeItActs`).
  - The PR body, "How to validate": "`TalkerCommands…`, `DeclinedUnbind…` and `A19AFullQueueDeclinesTheCommandBeforeItActs` do the same for each of the other six command types".
- **Evidence:**
  - "The same" means: fill the owed set, decline the command, release the egress after 60 ms, and check an in-order answer within 200 ms.
  - A19 offers BIND_RX and GET_TX_STATE once each and asserts only `false`, an UNBOUND sink, no calls and a count of 2. It never releases the egress, never redelivers and never looks for a BIND_RX_RESPONSE or GET_TX_STATE_RESPONSE.
  - The other five command types are checked for an answer after redelivery. GET_RX_STATE, UNBIND_RX and PROBE_TX are also offered directly while the owed set is full. DISCONNECT_TX and GET_TX_CONNECTION are queued behind the declined PROBE_TX by `deliver()` (`:2572-2578`) and are declined again during redelivery.
  - Reviewer probes on a disposable copy (`receipts/probe-owed.txt`):
    - A declined BIND_RX is answered SUCCESS with count 1 (Milan Table 5.32) 69 ms after arrival.
    - A declined GET_TX_STATE is answered SUCCESS with the source stream (Table 5.47) 69 ms after arrival.
  - So the behaviour is right, but the suite does not pin it. The PR's test claim, and the issue's "every command answered", rest on assertions for 5 of the 7 command types.
- **Impact:**
  - BIND_RX is the costliest command and the only one whose redelivery also changes probing (S1). Its deferred answer is the one most worth pinning.
  - A future change to the redelivery path could regress these two command types without any ACMP-12 test failing.
  - The PR body overstates the evidence.
- **Required outcome:**
  - Add, in the `AcmpOwed` fixture, assertions that a declined BIND_RX and a declined GET_TX_STATE are answered after `release_after_hold()`, with their Milan Table 5.32 and 5.47 fields, within 200 ms and in order. Then update TESTS and TRACEABILITY.
  - Alternatively, extend the existing per-command tests to cover them.
  - Correct the PR sentence so that it matches what each test asserts.
- **Verification:** the new assertions pass at the new head. Each should be killed by a plant that serves the command while the owed set is full, or that loses the redelivered answer. Re-run the `owed-` mutation selection.

### S1: SUGGESTION (Robustness, Docs). A deferred BIND_RX always loses its first probe

- `src/acmp.c:822-853` with `:292-313`. A port that follows the contract redelivers right after `acmp_poll` frees one slot.
- A redelivered BIND_RX is then served with exactly one free slot. The response takes the slot, and the first PROBE_TX is `LOST`: `probes_lost` 1, state PRB_W_RESP, no probe sent until TMR_NO_RESP (200 ms) expires. The retry then goes out and the state moves to PRB_W_RESP2 (`receipts/probe-owed.txt`).
- The same happens on main for any BIND_RX at 7 owed, and PORTING:69 states the general recovery. So this is not a regression. But the new contract makes it the normal outcome for every deferred BIND_RX: binding settles at least 200 ms later and its retry is already used.
- Consider declining a new binding until two slots are free, or say this explicitly in "ACMP owed bound".

### S2: SUGGESTION (Robustness; parent-integration note). Name the parent's `busy_drops` mutant fragment

- The integration note in the PR body does not mention that the parent's `sw/firmware/ctrl/test/acmp_mutants.py:452-453` matches on `busy_drops`. When the parent moves its gitlink, that fragment must change in the same parent PR.
- Naming it in the PR's integration note would help the parent author. The author's published handoff already records it.

### S3: SUGGESTION (Robustness, Docs). Say when to redeliver relative to timer service

- `docs/PORTING.md:79` says the port delivers the kept frame again "after `acmp_poll` accepts an owed frame".
- A port that services `acmp_timer_expired` between that poll and the redelivery can let a timer probe take the freed slot. The command is then declined again (see Robustness).
- This is bounded, keeps order and is not a livelock, but it adds passes to the 200 ms budget.
- Consider "deliver the kept frame right after the accepting `acmp_poll`, before timer service", which is what the test port model does.

## Prior public review findings at this head

I read these only after the verdict and ledger above were written. They come from the internal reviewer's R793-1 report on this PR, at this same head.

| Prior item | Status at 3d57262 | Basis |
|---|---|---|
| F1 MINOR (Tests, Docs): answered-after-redelivery is claimed but not tested for BIND_RX and GET_TX_STATE | **Retained** as this report's F1 | I reached it independently from the A19 and `deliver()` code and confirmed it with my own probe. After reading the prior report, I added Docs to the lenses, for the PR-text claim. |
| S1 SUGGESTION: a redelivered BIND_RX always loses its first probe | **Retained** as S1 | Reproduced by my probe: `probes_lost` 1, no PROBE_TX until NO_RESP expiry, then PRB_W_RESP2. |
| S2 SUGGESTION: say when to redeliver relative to timer service | **Retained** as S3 | My Robustness analysis reached the same bounded re-decline case independently. I adopted the suggestion wording after reading the prior report. |

The prior report records no RESIDUE, and none was found here.

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Issue #26 acceptance; PR text; ACMP-12; PORTING "ACMP owed bound"; `src/acmp.c:322-334, 813-1003, 1036-1095`; cited IEEE 1722.1-2021 and Milan v1.2 clauses (as used in the repository); hold-sweep and answer-field probes | R794-1 | 3d57262c3614740244de40c40f667908ce6310f7 |
| RTL (C core, both targets) | CLEAN | `validate.py` 27/27 rc 0; `baremetal.py` Debug/Release rc 0; Release ELF byte-identical; struct sizes on both targets; instruction counts byte-identical (4 builds); image and object sizes; hosted push and PR runs, all steps success | R794-1 | 3d57262c3614740244de40c40f667908ce6310f7 |
| Robustness | CLEAN | Unmasked byte image of a decline; repeated offers; unknown sink; liveness and timer-ordering analysis; parent consumers at `0a75aa77` (read-only) | R794-1 | 3d57262c3614740244de40c40f667908ce6310f7 |
| Tests | UNCLEAN (F1) | `tests/test_acmp.cpp` delta; `tests/mutations.json` (22 new, 1 changed); full campaign 410/410; 7 per-command plants applied singly, sole killer and escape reproduced; RV32 smoke under 2 plants; coverage 795/795 and 400/400 | R794-1 | 3d57262c3614740244de40c40f667908ce6310f7 |
| Docs | UNCLEAN (F1, PR text) | PORTING, REQUIREMENTS, `requirements.json`, TRACEABILITY, TESTS, VERIFICATION, ARCHITECTURE, CHANGELOG; PR body; comment-rule scan of every added line; commit message | R794-1 | 3d57262c3614740244de40c40f667908ce6310f7 |

## Real limits

- No standards PDFs were available. Clause numbers and titles were judged from the repository's citations and the PR's reasoning.
- The graphs gate (Mermaid) was not run: the renderer is not installed on this host. It is a rendering gate with no bearing on this delta's behaviour.
- The sanitizer build used the host Clang 23.1.4. Static analysis used clang-tidy 18.1.3, CI's version. The author notes that the host's clang-tidy 23 differs from CI's 18: their base gate run returned 1 with 23 and 0 with 18.
- Hosted CI was inspected only through its job and step conclusions. Its logs and artifacts were not downloaded.
- No physical calibration or hardware was run. Field skips are not hardware proof.
- I did not run the parent harness, a parent build or any manager source bank, and I infer none.

## Receipts and reproduction

- Every published file is listed in `MANIFEST.sha256`.
- Absolute host locations in the copied gate logs are replaced by `<PACKET>`, `<CLONE>`, `<TOOLS>` and `<HOME>`. Nothing else in those logs was changed.
- Scripts (set `TOOLS` to the pinned toolchain prefix first):
  - `scripts/run_gates.sh CLONE WORK RECEIPTS JOBS`: the validation kit and the bare-metal gate, run concurrently.
  - `scripts/measure_cost.sh TREE OUT ISA OPT MEASURE_C [-DLANE]`: builds and runs the published instruction-count harness.
  - `scripts/sizes.sh TREE OUT`: struct sizes on both targets.
  - `scripts/run_probes.sh HEAD_TREE WORK OUT`: appends `scripts/probe_owed.inc` to a disposable copy, then builds and runs the probes.
  - `scripts/plant_probe.py TREE WORK OUT NAME…`: applies plants singly and records the killing tests.
  - `scripts/rv32_plant.sh HEAD_TREE WORK PLANT OUT`: runs the RV32 smoke check under one plant.
- Clone integrity after all probes (`receipts/clone-state.txt`):
  - HEAD and tree are exact.
  - The index tree equals the head tree, the worktree equals the index and HEAD, and there are no untracked or ignored files.
  - All 98 tracked entries are mode 100644. The repository tracks no gitlinks.
  - The bytecode cache my gate run created under `scripts/` was removed.

## Pending manager duties

- Validate the current-dev merge candidate (source base 70936b77, live dev 0a75aa774b89ac89351700f63dd8cbb89694af6c) with the builder and native banks at the merge turn, and link those receipts.
- Hosted and act acceptance belong to the manager.
- The parent PR that binds `ctrl_loop_set_rx_ready` to `acmp_rx_ready` must also update `acmp_mutants.py:452-453` (S2) and re-measure the harness row "an ACMP command behind the owed input". Until then #26 stays open, as the PR intends.
- After F1 is addressed, a re-review at the new head.
- Carry S1–S3 as optional suggestions.

R794-1 FINISHED
