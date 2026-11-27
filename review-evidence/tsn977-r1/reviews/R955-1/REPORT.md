[R955] NEGATIVE - exact head 5d03517f2ab42416654a8f2be2f71cfc51d82440

# R955-1 independent review: kebag-logic/tsn-c-stack PR #41 for kebag-logic/milan-fpga#977

- Exact head `5d03517f2ab42416654a8f2be2f71cfc51d82440`, tree `ea28576a2e51dde5c38be79be870c339f920460f` (branch `977-settle`).
- Base `main` `c3bff8f3dea03870ea7ae62965db360b509ee3b3`.
- Delta reviewed: `6390129` and `175cf9e` on `a795471c`, then the merge of `main` `c3bff8f3` (PR 40).
- Reviewer role: internal independent reviewer, cleared context, isolated detached clone.

## Verdict

**NEGATIVE**, on three MINOR findings in the Tests lens. Every other lens is clean.

- **Behaviour is identical.** At this head the ACMP core behaves exactly like the base core. Code reading shows this, and so does a base-versus-head differential written for this review. That differential compares every port and environment call, including full frame bytes, plus the saved records, reported views, `acmp_view` and `acmp_binding_latch`, for every sink after every entry. It covered 7 sink counts at 12 seeds each, at a 33-sink build and at the default 16-sink build.
- **The merge brings in only main's content.**
- **Both targets build and pass.**
- **The head's own mutation set is 512 of 512 caught.**

The problem is that several **new** paths have no killing test. Seven reviewer-planted defects at the new lines survive the whole suite. Run against the base core in the differential, each one diverges, so they are real escapes and not equivalent mutants:

- the persistence compare ignoring the unique ID, the Talker ID or the controller ID (F1);
- the publication and admission walks never loading the second mark word (F2);
- `view_of` dropping the new `streaming_wait` field copy (F3).

## Reconstruction

| Source | Read |
|---|---|
| Repository rules | `CONTRIBUTING.md` (the repository has no `AGENTS.md`), `README.md`, `docs/REQUIREMENTS.md`, `docs/PORTING.md`, `docs/VERIFICATION.md`, `docs/TESTS.md` and `docs/TRACEABILITY.md`. The relevant entries: ACMP-13 (changed-sink walk), MFCONN-04 (persist complete binding records), ACMP-10/05/09, the coverage ratchet, and "a regression needs a failing assertion and a runnable planted defect". |
| Frozen scope | Issue #977's body (acceptance of 2026-11-22) and the manager rulings of 2026-11-22, 11-23, 11-24, 11-25 and 11-26. Item 4 of the 2026-11-26 ruling: the stack branch goes through the stack's own review and merges, and #977 pins that merge commit, never the branch. |
| PR | The PR #41 body, which is identical to the packet's `PR-BODY-tsn.md` except for the title line. The PR's only two comments are review-start notices. |
| Evidence | milan-fpga `53ac1c2e` `review-evidence/tsn977-r1`. `HANDOFF-r8.md`, `PR-BODY-tsn.md` and `REVIEW-READY.md` match the sha256 values in `MANIFEST.json`. Branch `977-review-evidence` (`f7a322f9`) `review-evidence/977-r1` holds no stack-side gate receipts beyond the same `PR-BODY-tsn.md` (same blob). |
| Hosted runs at the exact head | Quality and bare-metal both succeeded for the `push` and `pull_request` events (runs 45942571101 and 45942567069). Every step executed and none was skipped (`receipts/hosted-jobs.txt`). |
| Prior public review findings | None. PR #41 has 0 reviews and 0 review comments, so nothing needed resolving or retaining. |

The authorities are IEEE 1722.1-2021 clause 8.2 (ACMP) and Milan v1.2 5.5: 5.5.3.5.3 bind, 5.5.3.5.5 unbind, 5.5.3.5.8 binding record, and Tables 5.22 and 5.34-5.39. The record and view layouts come from `include/acmp.h:256-293`.

## Findings

| ID | Severity | Lenses | Location | Authority / evidence | Impact | Required outcome | Verification |
|---|---|---|---|---|---|---|---|
| F1 | MINOR | Tests | `src/acmp.c:509-529` (`record_moved`), called at `src/acmp.c:572`; `tests/mutations.json` (persistence plants) | `record_moved` re-derives `record_of`'s 20-octet layout (`src/acmp.c:494-504`) by hand, so it is a second source of truth for the record. No test ties the two together field by field. The suite does not kill dropping the unique ID (`r-rec-drop-unique`, `r-rec-drop-p3`), the Talker ID (`r-rec-drop-talker`) or the controller ID (`r-rec-drop-controller`) from the compare. Each of these diverges from the base core within the first 50 entries of a run. The unique-ID and Talker-ID drops diverge at every sink count; the controller drop diverges at 6 of the 7 counts at the 33-sink build and at all 5 at the default build (`receipts/probes*-results.json`, `receipts/diff33-results.json`, `receipts/diff16-results.json`). The rule is CONTRIBUTING's "a regression needs a failing assertion and a runnable planted defect"; the requirements are MFCONN-04 and Milan v1.2 5.5.3.5.3 / 5.5.3.5.8. | The head is correct today. But a later edit can silently stop persisting a rebind that changes one field. Two cases depend only on this compare: a same-stream bind from a second controller (`src/acmp.c:920-926`), which changes only the controller ID, and a bind to another stream of the same Talker, which changes only the unique ID. After a reboot the sink would restore the old binding. | 1. Add assertions requiring `persist` and a saved record equal to `acmp_binding_latch` after each single-field rebind: controller only, unique ID only, Talker ID only. 2. Plant the three field drops in `tests/mutations.json`, each killed by its named assertion. A randomized property test comparing `record_moved` with `record_of` against `saved` is acceptable in place of item 1. | Re-run `scripts/probes_run.py` with `receipts/probes2.json`: `r-rec-drop-unique`, `r-rec-drop-talker` and `r-rec-drop-controller` must be KILLED. The mutation campaign must stay 0 escaped. |
| F2 | MINOR | Tests | `src/acmp.c:219-226` (`publish`) and `src/acmp.c:537-544` (`admit`), the second-word load `if (k % 32u == 0u) bits = a->dirty[k / 32u];`; `tests/mutations.json:8247` (`walk-marked-word-zero`) | The shared `marked()` helper was replaced by three inline copies of the word walk, and only the publication walk's copy keeps a plant (`walk-marked-word-zero`). The suite does not kill never reloading the mark word in `publish` (`r-publish-no-reload`) or in `admit` (`r-admit-no-reload`). The 33-sink walk test only compares two cores running the same code, so a defect that skips sink 32 on both sides escapes it. The `AcmpWide` tests do not assert sink 32's publication or admission. Both probes diverge from the base core at 33 sinks (`receipts/diff33-results.json`). Before this delta, a fault in `marked()` also broke the persist and report loop, which `AcmpWide` catches; that is why the finish copy's no-reload probe is killed. | With `ACMP_MAX_SINKS` above 32 (a supported build, and the reason the `acmp_wide` and `acmp_walk` arms exist), a defect in either copy would leave sinks 32 and up never published to the datapath or never admitted, and no gate would fail. | 1. Add absolute assertions at 33 sinks that sink 32's `publish` and `admit` calls are made: for example, an `AcmpWide` bind and settle of sink 32. 2. Plant the no-reload (or second-word) defect in `publish` and `admit`, each killed by its named assertion. 3. Update `docs/VERIFICATION.md`'s mutation count and description to match. | Re-run `scripts/probes_run.py` with `receipts/probes.json`: `r-publish-no-reload` and `r-admit-no-reload` must be KILLED. |
| F3 | MINOR | Tests | `src/acmp.c:455` (`v->binding.streaming_wait = s->binding.streaming_wait;`) | This field copy is new; before this delta, `v->binding = s->binding` copied the binding as one struct. No test reads `binding.streaming_wait` through `acmp_view`: the tests read `a.sinks[k].binding` directly. Dropping the line (`r-viewof-drop-binding-streaming_wait`) survives the suite and diverges from the base core in the reported view and in `acmp_view` (`receipts/diff*-results.json`). The authority is the view's binding item, Milan v1.2 5.3.8.3 (`include/acmp.h:284`). | An integrator reading a sink's binding through `acmp_view` would see STREAMING_WAIT cleared, and no gate would fail. | Assert `acmp_view(...).binding.streaming_wait` after a STREAMING_WAIT bind, and plant the dropped copy in `tests/mutations.json`, killed by that assertion. | `r-viewof-drop-binding-streaming_wait` must be KILLED. |
| R1 | RESIDUE | Docs | `docs/VERIFICATION.md:24` | The text says "two write or read word 0 for every sink". After the re-anchor, the read plant reads word 0 only in the publication walk. | Wording only; the sentence slightly overstates the plant's scope. No measurement, test or code changes. | Replace "and two write or read word 0 for every sink" with "one writes word 0 for every sink and one reads word 0 for every sink in the publication walk". If F2 adds plants, F2's documentation update supersedes this fix. | Read the line. |
| S1 | SUGGESTION | Docs | `CHANGELOG.md:5` | The entry says "an entry's completion was about 4,500 cycles at nine sinks". The PR body gives 40,948 cycles over nine completions, about 4,550 each, measured before the change. | None; the figure is approximate and the measured effect is reviewed on milan-fpga PR #993. | Optionally say "about 4,550 cycles a completion before this change". | n/a |

## Lens evidence

### Conformance: CLEAN (IEEE 1722.1-2021 8.2, Milan v1.2 5.5)

Code reading at the head:

- **The walks.** Loading each mark word once and shifting it gives `marked(k)` for every `k < n_sinks`, provided no mark is set during the walk. None is:
  - the bodies of `publish`, `admit` and the persist and report loop only call `p_publish`, `p_admit`, `p_persist` and `p_changed`;
  - each callback runs with `in_port` set, so a re-entrant entry is refused by `enter()` (`src/acmp.c:96-105`);
  - the const getters `acmp_view`, `acmp_binding_latch` and `acmp_change_pending` set no mark.

  The sinks visited, their order and the bound are unchanged, and marks past `n_sinks` are still ignored.
- **`record_moved(s)`** equals `!same_record(record_of(s), s->saved)` octet for octet:
  - octet 0: flags (VALID, STARTED, STREAMING_WAIT);
  - octet 1: zero;
  - octets 2-3: big-endian unique ID;
  - octets 4-11: big-endian Talker ID;
  - octets 12-19: big-endian controller ID;
  - every octet zero while unbound.

  When they differ, `record_of` writes `saved` before `p_persist`, as `memcpy` did before.
- **`view_moved(s, &s->reported)`** equals `!view_equal(view_of(s), &s->reported)`. It compares the same nine items with the same settled and registered gating. `view_of` now writes `s->reported` in place, after its `memset`, which gives the same values as assigning a local.
- **`view_of`** copies all four `acmp_binding` fields and all three `acmp_stream` fields (`include/acmp.h:256-268`). The only change in `acmp_view` output is that padding bytes are now always zero.
- **Unchanged code.** GET_RX_STATE replies (`src/acmp.c:973-992`) read the sink directly and are unchanged. So are restore and rollback (`src/acmp.c:1388-1424`), the other persistence paths.

Executed: the base-versus-head differential (`scripts/diff_gen.py` and `scripts/diff_run.py`). It is built from the head's own walk test:

- the base `a795471c` `src/acmp.c` (equal to `main` `c3bff8f3`'s) is compiled with an `old_` prefix;
- both cores receive identical random entries: binds and unbinds from two controllers, two Talkers and two unique IDs, GET_RX_STATE, probe responses, Talker commands, ADP, timers, SRP registration and kind changes, started changes, polls, transmit room, lock, restore and rollback;
- after every entry it requires identical full call traces, including frame bytes, plus identical saved records, reported views, `acmp_view`, `acmp_binding_latch` and `change_owed` for every sink.

Results:

- **33-sink build:** 1, 2, 8, 9, 16, 32 and 33 sinks, 12 seeds each, 4,000 to 10,000 entries per seed. **AGREE** (`receipts/diff33-results.json`).
- **Default 16-sink build:** 1 to 16 sinks. **AGREE** (`receipts/diff16-results.json`).
- **Sensitivity:** the seven escaped probes all diverge.

### RTL (implementation and targets): CLEAN

The delta has no HDL. This lens was applied to the C implementation as built for both required targets:

- **GCC 16.2.1:** `-Wall -Wextra -Werror` Debug with coverage builds; 10 of 10 test binaries pass (`receipts/gates/gcc-*`).
- **Sanitizer arm:** passes 10 of 10 (`receipts/gates/clanghost-*`), built with host Clang 23.1.5; see Limits.
- **Bare-metal RV32:** `scripts/baremetal.py` passes Debug and Release with no unresolved final symbols, and the QEMU smoke run passes (`receipts/gates/baremetal-results.json`).
- **Integer handling:** the new XOR and shift terms are integer-promoted without UB, and the shift amounts stay within width. The 33-sink arms pass under `-fsanitize=shift,undefined`.
- **Code size:** text at `-Os`, rv32i, grows by +488 B (11,432 to 11,920; `receipts/rv32-size.txt`). This matches the PR's stated delta; the absolute sizes differ with toolchain and flags.

### Robustness: CLEAN

- **Bounds:** the word index `k / 32u` stays below `ACMP_DIRTY_WORDS`, because `acmp_init` refuses `n_sinks > ACMP_MAX_SINKS` (`src/acmp.c:1106`).
- **Initialisation:** `saved` and `reported` are always initialised by `sink_reset` and `sink_settle`.
- **Clearing:** the word-by-word clear covers every word.
- **Re-entry:** callbacks cannot add marks during a walk, so caching the mark word is safe.
- **33 sinks:** the second-word paths run under the shift and UB sanitizer, and the differential agrees there.

### Tests: UNCLEAN (F1, F2, F3)

The head's own gates were reproduced from an extract of the exact-head tree with the pinned GoogleTest and GMock 1.14.0:

- **Mutation campaign:** 512 caught, 0 escaped, 0 errors (`receipts/gates/mutation-results.json`). The nine re-anchored plants each match exactly once and are killed.
- **Coverage:** `src/acmp.c` 877/877 lines and 468/468 branches; `src/adp.c` 215/217 and 95/102, 100 % after exclusions.
- **Source and metadata gates pass:** entity-golden, needles, comments, port-contracts, acmp-cache, license, traceability, privacy (with its self-test), coverage-controls, test-inventory and static-analysis (clang-tidy 18.1.3).

Reviewer probes: 77 mutants at the new lines (`receipts/probes.json`, `receipts/probes2.json`), run against the `acmp`, `acmp_wide` and `acmp_walk` arms.

- **Controls:** the unmutated control passes, and the planted control `acmp-nothing-persisted` is killed.
- **Escaped and non-equivalent (they diverge from the base core):** the F1, F2 and F3 probes.
- **Equivalent by design (ACMP-13):** the three every-sink walks, which agree with the base core.
- **Equivalent by invariant (agree with the base core):**
  - `r-rec-drop-p1`: `saved[1]` is only ever written by `record_of`.
  - Ungated unique and Talker IDs: unbind and reset zero the binding (`src/acmp.c:960`, `598`).
  - Ungated stream and registering-failed fields: `srp_stop` zeroes the stream and `tk_failed` (`src/acmp.c:768-769`).
  - View stream and bound terms: these changes always co-occur with a probing-status change, as in the base's `view_equal`.
- **Not run in the differential:** the single-octet drops other than p1, p3 and p19, and the ungated dest/vlan/controller probes. They are not classified individually; F1's required outcome covers the single-field class.

### Docs: CLEAN (R1 residue, S1 suggestion)

- The CHANGELOG entry and the PR body's claims match what was reproduced: gates, the 512/0 campaign, the coverage figures, the integration notes and the +488 B delta.
- No requirement, structure or public header changes, and there is no protocol change, so no update to `REQUIREMENTS.md` or `TRACEABILITY.md` is needed; the traceability and test-inventory gates pass.
- Comment rule (owner 2026-10-15): the delta's only new comments are two `// REQ: ACMP-13` tags (`src/acmp.c:475` and `:508`). There are no lane labels, lane names, rounds, reviewer IDs or comment IDs, so no new residue.
- Commit subjects are one line with no body, as CONTRIBUTING requires.

### Merge content: verified

The head's parents are `175cf9e` and `c3bff8f3`, with merge base `a795471c` (`receipts/merge-check.txt`).

- Git's automatic merge differs from the head tree only in `CHANGELOG.md`, its one conflict. `tests/mutations.json` is exactly the automatic merge.
- The head's `CHANGELOG.md` is main's file plus the branch's single line.
- Every other file main changed is at main's blob, and every other file the branch changed is at the branch's blob.
- No file changed by neither side differs from the base.
- `src/acmp.c` is the branch's blob, and main did not touch it.

## Ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `src/acmp.c` delta and its callers (walks, `record_moved`, `view_moved`, `view_of`, GET_RX_STATE, restore); `include/acmp.h`; base-versus-head differential at 33 and 16 sinks | R955-1 | 5d03517f2ab42416654a8f2be2f71cfc51d82440 |
| RTL | CLEAN | GCC `-Werror` build and tests; host-Clang sanitizer build and tests; RV32 Debug/Release freestanding link and QEMU smoke; rv32i `-Os` size; hosted bare-metal job | R955-1 | 5d03517f2ab42416654a8f2be2f71cfc51d82440 |
| Robustness | CLEAN | Mark-word bounds, re-entry guard, initialisation of `saved`/`reported`, clear loop, 33-sink sanitizer arms | R955-1 | 5d03517f2ab42416654a8f2be2f71cfc51d82440 |
| Tests | UNCLEAN (F1, F2, F3) | `tests/mutations.json` (512 plants, 9 re-anchored), mutation campaign 512/0, coverage, 77 reviewer probes, differential sensitivity | R955-1 | 5d03517f2ab42416654a8f2be2f71cfc51d82440 |
| Docs | CLEAN (R1 residue, S1 suggestion) | `CHANGELOG.md`, PR body, `docs/VERIFICATION.md`, `docs/TESTS.md`, `docs/TRACEABILITY.md`, `docs/REQUIREMENTS.md`, `docs/PORTING.md`, delta comments, commit subjects | R955-1 | 5d03517f2ab42416654a8f2be2f71cfc51d82440 |

## Real limits

- **Sanitizer compiler.** Here the sanitizer arm ran with host Clang 23.1.5, not the CI's Clang 18. The pinned Clang 18.1.3 cannot parse this host's GCC 16 libstdc++ headers (`receipts/gates/clang-build.log`).
- **Gates not run on this host, for the same reason:** the conditional-regions gate (`receipts/gates/conditionals.log`).
- **Gates not run here at all:** mutation-controls, assertion-templates, dependencies, boundary, entity-controls, registration-controls and graphs.
- **Hosted coverage of those gates.** The hosted quality job, which runs all of them with Clang 18, succeeded at the exact head. I inspected it but did not re-execute it.
- **Differential scope.** The differential is randomized over the walk test's generator, not exhaustive. Saved-record contents not reachable through restore are not exercised.
- **CPU figures.** The measured CPU figures (THE SETTLE, the registration term) and the image sizes are not reviewed here; they belong to milan-fpga PR #993.
- **No manager source bank.** No manager source bank runs at this head, and none is claimed or inferred. The author's stack-side receipts are textual claims in the PR body; I reproduced them independently.
- **No hardware.** Physical calibration was NOT RUN, and nothing here is hardware proof.

## Pending manager duties

- At the merge turn, validate the current-dev merge candidate (builder and native banks; source base `c3bff8f3dea03870ea7ae62965db360b509ee3b3`, live dev `e275d7950ef3385753e6a15d2e191ba855b171ed`) and link its receipts on the PR.
- Own hosted/act acceptance. The hosted quality and bare-metal jobs at this head were observed successful (runs 45942571101 and 45942567069).
- After F1-F3 are fixed at a new head, re-review at that head; this verdict covers `5d03517f` only.
- Per the 2026-11-26 ruling item 4 and the PR body, move milan-fpga #977's pin from this branch head to PR #41's merge commit on `main` once merged, then rebuild and re-measure there.
- Carry R1 to the residue checklist.

## Receipts

`MANIFEST.sha256` lists every published receipt and script.

- Gate logs and rc files: `receipts/gates/`
- Probes: `receipts/probes*.json`, `receipts/probes*-results.json`, `receipts/probes*-run.log`
- Differential: `receipts/diff-src/`, `receipts/diff*-results.json`, `receipts/diff*-run.log`
- Other receipts: `receipts/merge-check.txt`, `receipts/hosted-jobs.txt`, `receipts/rv32-size.txt`, `receipts/tools.txt`, `receipts/clone-integrity.txt`
- Scripts: `scripts/`

In the receipts, host paths are replaced by `<packet>`, `<clone>`, `<tools>` and `<slots>`. After the review the clone is still at the exact head: worktree and index match HEAD, 0 tracked blobs or modes differ, and the repository has no submodule gitlinks (`receipts/clone-integrity.txt`).

R955-1 FINISHED
