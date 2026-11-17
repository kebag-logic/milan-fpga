[R857] POSITIVE - exact head 81c9a1a0c84bbb1da633db641d623d253dcb092a

# R857-2: internal cleared-context review of PR #938 (issue #920), round 3 delta

- **Head:** `81c9a1a0c84bbb1da633db641d623d253dcb092a`, tree `b5e316ba63147a33e70caf0093e41d0538e046a8`. The clone was checked at both before and after this round.
- **Delta:** `bd252db1..81c9a1a0`, one commit, tests only (`receipts/delta-raw.txt`):
  - `sw/firmware/ctrl_nvm/test/nvm_mutants.py` (+5);
  - `sw/firmware/ctrl_nvm/test/test_nvm_write.cpp` (+42 / -2).
- **Verdict:** POSITIVE. Both prior MINOR findings (R857-1 F-1 and F-2) are resolved at this head. No BLOCKER, MAJOR or MINOR finding is open.
- **Recorded, non-blocking:** one new wording RESIDUE (R-1) and three SUGGESTIONs. Prior residues are retained below.

## Reconstruction (public state only)

- **Workflow authorities:** AGENTS.md sections 5 to 7 and CONTRIBUTING.md.
- **Issue #920 body:**
  - scope items 1 to 3;
  - acceptance item 3: "the load within 0.70 (1x1) and 0.75 (8x8)".
- **Manager rulings on #920:**
  - issuecomment-6910219988: the 8x8/1if routes miss at the base and are owed to #927; the stated-cost lines are #914's.
  - issuecomment-6935243271 (F-2): the acceptance is amended to "the load within 0.70 at 1x1/1if, and within 0.75 at 8x8/1if by #914's gate at the composition; 8x8/2if's load is owed to #890". The PR body must state both figures and this disposition.
- **REVIEW READY:** #920 issuecomment-6936474208.
- **PR body:** PR #938 as published, head `81c9a1a0`, not draft.
- **Author packet:** `review-evidence/920-r1/author-r3` at archive `45180d44`. This is the live tip of `920-review-evidence`.
- **Order of reading:** I read the prior reviews' findings (R857-1 issuecomment-6935233068 and R858-1 issuecomment-6933421808) only after my own pass over the diff.

## Checks against the brief

### (1) F-1: the resets of the two new flags

**Plants caught by name.** `nvm_mutants.py:373-376` registers two plants:
- `next_now_not_reset` removes `nvm.next_now = 0;` (`nvm_store.c:540`). It names `first_change_after_flight` (`test_nvm_write.cpp:235`).
- `rewound_not_reset` removes `nvm.rewound = 0;` (`nvm_store.c:536`). It names `retry_after_rewind` (`test_nvm_write.cpp:252`).

I ran the store suite's self-test on a clean clone of this head (`receipts/store_selftest.log`, rc 0). It printed `OK across 5 shape(s), 566 tests, and all 154 planted defects reddened`, with:
- `self-test OK: next_now_not_reset caught by first_change_after_flight`;
- `self-test OK: rewound_not_reset caught by retry_after_rewind`.

**The tests against the code** (`nvm_store.c:531-541, 636-675, 896-959`):

`first_change_after_flight`:
- The test sets a record during SEAL, so `nvm_mark` sets `next_now`. The second save then starts at once.
- After a 5 s idle and a mark, a change must erase 1,000 to 1,050 ms later, which is DR2a's window.
- If `next_now` survives its capture, `nvm_idle`'s `due` is true at the first idle step. The window is skipped, and the check fails.

`retry_after_rewind`:
- Save 1 walks again for `behind`, which leaves `rewound = 1`.
- A failed attempt's backoff then changes `a`, a record in flight.
- With the reset removed, the retry's `nvm_takes(a)` is false. The retry's `nvm_capture_begin` clears `dirty_armed` and `next_now`, so nothing would ever start a save for `a=6`.
- The checks `dirty == 0`, `ok == 2` and the restored value `a=6` all fail. That is the loss after a power cut that R857-1 F-1 described.

The plant's failure line, `retry after a rewind must capture the backoff change`, confirms it.

**The robustness gap is closed.** Both reset paths now fail by name when removed.

**The case-4 part.** The author narrowed the claim rather than add a variant (`test_nvm_write.cpp:158` and `:191`). The new claim, "the walk again takes a new record ahead of the cursor", is still more than the case shows:
- **The probe.** `receipts/probe-case4.diff` is planted on a clean copy of this head. After the capture has walked again, it refuses a change to a record no capture holds, and leaves it for the next save. `next_now` starts that save at once.
- **The result.** The shipping 1x1 shape `endstation_arty_current` passes 110 tests with 0 failures (`receipts/probe_case4.log`, rc 0). `capture_joins` is among them.
- **The branch is reached.** A trap at the probe branch (`receipts/probe-fire-over-case4.diff`) crashes only `Ports/NvmBoth.capture_joins/model` with signal 4 (`receipts/probe_fire.log`). Of the cases there, only case 4 marks a record no capture holds after a walk again.
- **So the case cannot tell the walk again's take from the next save's.** Both end in two saves with the same restored values.
- **The disposition is R-1 RESIDUE, not MINOR:**
  - R857-1 F-1 accepted a narrowed claim as the outcome.
  - The behaviour stays durable either way: the probe keeps every durability check green.
  - The exact fix is text only: one comment line and one case label. It changes no check, code or figure.

### (2) F-2: the 8x8 load criterion

The PR body's "Load acceptance, amended by the ruling on F-2" section quotes the amended line word for word and links issuecomment-6935243271. It states three figures:
- **1x1/1if: 0.517 of 0.70.** It matches the packet's `receipts/gates/load-grade.log` (`HELD 1x1/1if at the pin: the load 0.517, its ceiling 0.70`, `RESULT: PASS`).
- **8x8/1if: graded by #914's gate at the composition, 0.735 of 0.75 at #914's head.** I fetched the linked #894 issuecomment-6934688411. It reads "at 8x8/1if, the load is 0.735 at the pin against 0.75". The PR body correctly calls this prior evidence for #914, not a composition result for this head.
- **8x8/2if: 0.798 at the pin, the base's and owed to #890.** It matches `load-grade.log` (`8x8/2if | 0.798 | 0.756`).

This round moves no load term, because the firmware is unchanged (see (3)).

**F-2 is resolved for the PR.** The issue body's acceptance item 3 is not edited; the amendment lives in the ruling comment. That is a manager duty, listed below.

### (3) No firmware change beyond tests

- **Source identity.** `git diff --raw bd252db1 81c9a1a0` lists only the two test files, mode 100644 kept.
- **Gitlinks.** All six (external, gptp-processor, protocol-processor, lwSRP, tsn-c-stack, verilog-axis) are identical at both heads.
- **Image builds.** No image build consumes `sw/firmware/ctrl_nvm/test/`. The only references outside it are CI and test drivers (`git grep`).
- **Author receipt.** `receipts/gates/image-identity.txt` shows 16 of 16 IDENTICAL: eight ELFs and eight loadable binaries, rebuilt on clean clones of both heads.
- **I did not rebuild the images.** The source identity is enough to falsify any change, and none exists.

So the harness, routes and sweep carry. KNOWN, not findings: the timing floor is #818's, and this round ran on the usage fallback.

### (4) Store suite, coverage and docs on a clean clone

Every run used a fresh clone of the head, with its submodules checked out at the gitlinks.

| Gate | Result | Receipt |
|---|---|---|
| `test_ctrl_nvm.py --require-rv32 --self-test --jobs 16` | rc 0; 566 tests at 5 shapes, 154 of 154 plants caught | `receipts/store_selftest.log`, `.rc` |
| `fw_coverage.py --check --jobs 12` | rc 0; `firmware coverage: PASS (39 files)`; `nvm_store.c` 508/508 lines, 311/320 branches, 100.00 % under the exclusions; `aecp_nvm.c` 100.00 % | `receipts/coverage.log`, `.rc` |
| Docs and source gates for the delta's file types | rc 0 each: `check_cpp_idiom`, `check_py_idiom`, `check_hygiene --check`, `check_todo_ownership`, `docs_check`, `check_doc_paths`, `check_doc_style`, `measure_naming --check`, `measure_test_evidence --check`, `measure_fail_fast --check`; and, with the pinned Markdown renderer, `check_em_dash --base bd252db1`, `gen_toc --check`, `gen_toc --verify-anchors` | `receipts/light_gates.log` |

Two notes on the docs gates:
- `check_em_dash` and `gen_toc` first refused, with rc 2, for want of the renderer. They passed once it was supplied. That is an environment step, not a finding.
- The author's full five-job docs run (`receipts/gates/docs.log` `FINAL rc=0`; `docs-verify.md`) was spot-checked by section and agrees.

**Comment rule (owner 2026-10-15).** The delta's added lines carry no lane label, review round, reviewer ID or issue-comment ID. They cite only #920 and the decision-register IDs DR2a and DR2c. My scan of the added lines found no match.

## Findings

### R-1 RESIDUE: case 4's narrowed claim still says the walk again takes the new record

- **Lenses:** Tests, Docs.
- **Where:**
  - `sw/firmware/ctrl_nvm/test/test_nvm_write.cpp:158`: "the walk again also takes a new record ahead of it".
  - `sw/firmware/ctrl_nvm/test/test_nvm_write.cpp:191`: the case label "the walk again takes a new record ahead of the cursor, one the capture took is the next save's".
  - The REVIEW READY and the PR body: "Case 4's wording now claims only the record ahead of the rewound cursor that it exercises".
- **Authority:** AGENTS.md section 6 (Tests): each test can fail for the defect it claims to detect. R857-1 F-1's required outcome: "the case's claim narrowed to what it shows".
- **Evidence:** the probe and trap in check (1) above. The case passes when the walk again refuses that record and the next save takes it.
- **Impact:** a reader is told the case pins the walk again's take. It pins only that the record is saved, by this save or the next. There is no durability gap, because the store still writes the record at once.
- **Exact fix (text only):**
  - Line 158: "...so one save holds every change; a new record marked on the walk again is saved, by this save or the next."
  - Line 191: `"a new record marked on the walk again is saved, one the capture took is the next save's"`.
  - Drop "that it exercises" from the PR body sentence, or reword it to match.
- **Verification:** read the two lines. Re-running the suite is unnecessary, because only text changes.

### S-1 SUGGESTION: let case 4 show the walk again's take, if it is meant to be pinned

- **Lens:** Tests.
- **Where:** `test_nvm_write.cpp:191-194`.
- **The point:** if the take itself should be pinned, case 4 could dump the slots after the first commit and require `ahead` in that container. `receipts/probe-case4.diff` could then be registered as a named plant. This is optional: the ruling's durability target holds without it.

### S-2 SUGGESTION: the store README's write-back inventory names no #920 test

- **Lens:** Docs.
- **Where:** `sw/firmware/ctrl_nvm/README.md:562-599`.
- **The point:** the list names no #920 case. That covers `capture_joins` and `busy_steps` from round 1, and now `first_change_after_flight` and `retry_after_rewind`. One bullet would do, for example "#920: the capture's join and walk again, the next save at the first idle step, the step a pass, and both flags' resets". This was the state before this round too.

### S-3 SUGGESTION: one packet INDEX row does not match its bytes

- **Lens:** Docs (evidence packet; manager publication).
- **Where:** `review-evidence/920-r1/author-r3/INDEX.md`, row `receipts/reproduction/package.py`.
- **The mismatch:** the row records 2,380 B, but the archived blob is 2,388 B (sha256 `7cf037771d18765cbea8fc111c9907feea645f39680a106125cc9be4c13c2a7a`). The other 184 rows match (`receipts/packet-index-verify.txt`).
- **A second problem:** the published `package.py` has its own scrub patterns scrubbed (for example `re.sub(r'<home>/\s]+', ...)`), so it does not run as published.
- **No gate result depends on it.** Optionally, regenerate the row and note that the script is a sanitized record.

## Prior public findings at this head

| Finding | Status at `81c9a1a0` | Evidence |
|---|---|---|
| R857-1 F-1 MINOR (Tests, Robustness): new flags' resets untested | **Resolved.** Both reset plants are caught by name. The case-4 wording is carried as R-1 RESIDUE. | `store_selftest.log`; check (1) |
| R857-1 F-2 MINOR (Conformance, Docs): 8x8 load criterion | **Resolved in the PR.** The amended line, 0.517/0.70, the 8x8/1if grading by #914's gate (0.735/0.75 at #914's head) and 0.798 owed to #890 are all stated with links. The issue body edit is a manager duty. | PR body; `load-grade.log`; #894 issuecomment-6934688411 |
| R857-1 R-1 / R858-1-F1 RESIDUE: issue-comment ID in source comments | **Retained,** untouched by the delta: `test_nvm_write.cpp:155`, `save_burst.py:5`, `run.py:374` | `git grep issuecomment-6899740728` |
| R857-1 R-2 RESIDUE: the stated reason for no join control | **Retained** in source (`save_window.py:72`, harness `README.md:129`). The PR body's table now uses the corrected wording. | head source |
| R857-1 S-1 SUGGESTION: the step a pass relies on no WFI | Retained, optional | n/a |

## Reviewer-owned ledger

All five lenses were applied at this head. Code the delta does not touch keeps the prior lens verdicts R857-1 and R858-1 at `bd252db1`, because the delta changes nothing they depend on; see check (3).

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Issue #920 acceptance item 3 against ruling issuecomment-6935243271. The PR body's load section against `receipts/gates/load-grade.log` and #894 issuecomment-6934688411. Ruling issuecomment-6910219988 (routes owed to #927). The ruling's mechanisms are unchanged, since `nvm_store.c` is identical to `bd252db1`. | R857-2 | `81c9a1a0c84bbb1da633db641d623d253dcb092a` |
| RTL | CLEAN | `receipts/delta-raw.txt`: tests only, with no `hdl/`, `syn/`, firmware, mailbox or builder file. Six gitlinks identical. No image consumer of `ctrl_nvm/test/`. `receipts/gates/image-identity.txt`: 16/16 IDENTICAL. The state machine (`nvm_store.c:531-559, 636-675, 896-959`) was re-read for the new tests' preconditions. | R857-2 | `81c9a1a0c84bbb1da633db641d623d253dcb092a` |
| Robustness | CLEAN | Reset paths of `rewound` and `next_now` (`nvm_store.c:536,540`), now caught by name. Retry, backoff and `dirty_armed` interplay (`nvm_idle`, `nvm_capture_begin`, `nvm_mark`) traced for `retry_after_rewind`. Refused-join probe: durability holds. | R857-2 | `81c9a1a0c84bbb1da633db641d623d253dcb092a` |
| Tests | CLEAN (R-1 residue, S-1) | `test_nvm_write.cpp:154-271`, `nvm_mutants.py:352-394`. Store suite 566/154 (`store_selftest.log`). `fw_coverage --check` 39 files (`coverage.log`). Probe `probe-case4.diff` (110/110 pass) and trap (`capture_joins` only). | R857-2 | `81c9a1a0c84bbb1da633db641d623d253dcb092a` |
| Docs | CLEAN (R-1 residue, S-2, S-3) | No doc file in the delta. `ctrl_nvm/README.md:345-352, 562-599`. `gtest/README.md:329` (`next_now` clearing, still true). `SPLIT_CONTROL_MEMORY.md:2753-2756`. PR body and REVIEW READY. 13 gates rc 0 (`light_gates.log`). Author docs receipts spot-checked. Packet INDEX (`packet-index-verify.txt`). | R857-2 | `81c9a1a0c84bbb1da633db641d623d253dcb092a` |

## Real limits of this round

- **Hosted CI:** there is no hosted run at this exact head. The commit lists 0 workflow runs and 0 check runs, and the combined status is `pending` with 0 contexts. Nothing hosted is claimed.
- **No manager source bank** ran at this head, and none is claimed. This round's execution evidence is my own focused runs plus the author's published receipts.
- **Not re-run:** the save harness, the AECP arms, the routes and the full sweep. The firmware and gateware are byte-identical to `bd252db1`, so their round-2 evidence carries by source identity.
- **Docs:** I ran 13 delta-relevant gates, not the full five-job docs workflow. That workflow is the author's receipt, spot-checked here.
- **Probe scope:** the probe ran at the shipping 1x1 shape only. That binary runs both the model and LiteSPI ports.
- **Evidence archive:** commit `45180d44` carries no cryptographic signature (GitHub: `unsigned`). Its integrity was checked by the packet INDEX's SHA-256 rows, 184 of 185 matching (S-3).
- **Not shown:** I did not separately show that the restoration check also fails under `rewound_not_reset`. The trace says it does, but the self-test prints only the first failure.
- **Hardware:** physical calibration NOT RUN. No bench or hardware run is claimed, and field skips are not hardware proof.

## Pending manager duties

- **Issue body.** Edit #920's body acceptance item 3 to the amended line of issuecomment-6935243271, or record that the ruling comment stands as the amendment.
- **Composition grading.** Grade 8x8/1if by #914's gate at the composition, and build the current-dev merge candidate (live dev `6b66f66d`) with its builder and native banks.
- **#919 sync.** Sync onto #919's review head, per ruling item 4.
- **Hosted and act acceptance.** Run them on the exact head and on the candidate.
- **Bench qualification.** Run the persistence scenario three times at each shape, reporting last-response-to-durable.
- **Residue checklist.** Carry R857-2 R-1, R857-1 R-1 / R858-1-F1 and R857-1 R-2.
- **Optional.** S-1 to S-3.

## Run index

All runs used disposable clones under the scratch directory. That directory is not published.

- `receipts/store_selftest.log`, `.rc`: the store suite with every plant.
- `receipts/coverage.log`, `.rc`: firmware coverage `--check`.
- `receipts/light_gates.log`: the 13 docs and source gates.
- `receipts/probe-case4.diff`, `receipts/probe_case4.log`, `.rc`: the refused-join probe.
- `receipts/probe-fire-over-case4.diff`, `receipts/probe_fire.log`, `.rc`: the trap where the probe fires.
- `receipts/delta-raw.txt`: the delta's paths and modes.
- `receipts/packet-index-verify.txt`: the packet INDEX check (`scripts/verify_index.py`).
- `receipts/tree-integrity.txt`: the review clone's index, blobs, modes and gitlinks against HEAD after every probe, and the gate clone's clean state.
- `scripts/probe_case4.sh`, `scripts/verify_index.py`: portable reproductions.

R857-2 FINISHED
