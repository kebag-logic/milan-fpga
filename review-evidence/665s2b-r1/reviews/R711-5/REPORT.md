[R711] NEGATIVE - exact head d930ea98f75be96f1062217d62bccd24dd291265

# R711-5: internal review of PR #810 (#665 S2b), delta a3f23bba..d930ea98 (rounds 15, 15 continued, 15 continued (2) and 16)

Head `d930ea98f75be96f1062217d62bccd24dd291265`, tree `76a51c452dc5f631981c40dcb95880460d24101d`. Source base `a68536fa`. Live dev `cc204c6f` is the manager's merge-turn candidate. It is not reviewed here.

## Verdict in one paragraph

Most of what round 16 measured checks out against its receipts. Every figure I recomputed from the raw results matches `ctrl_loop.h`, `aecp.h`, section 13 and the REVIEW READY:
- 600 head groups, 0 refusals, 0 of 1,489,645 work passes over the share;
- the least row margin, 0.235 ms;
- the notice rows and every pass class.

The image-identity receipt shows the legs' images are the head's, byte for byte. The prior round's findings (R711-4-F1/F2, R712-4-F1/F2 and their RESIDUEs) are resolved at their causes.

The verdict is NEGATIVE on two MAJOR findings, both about bounds the rulings required **by construction**:
- **F1.** SRP's 18 ms is met by measurement, not derived from the constants. Round 16's ruling item 1 requires the derivation. The author discloses this as an open question for the manager, and no decision is recorded. By the constants, the composed burst's last SRP record is bounded at about 34 ms. Its least measured margin, 0.235 ms, is below the layout swing the ruling names, summed over the sixteen passes the record waits.
- **F2.** THE RETRY's bound, and the derivations that depend on it, do not hold once two or more retried notices are held together.
  - A round builds one notice, and a probe shows each later notice costs two more passes under sustained input. So the second of two notices whose ports answer together is committed up to 8 + 14 = 22 ms after the answer, against 20 ms.
  - The probe shows aged-retry passes two passes apart. `CTRL_LOOP_RETRY_AGE_MS`'s comment states "at least a millisecond and the age" apart, and the probe falsifies that.
  - A second probe shows each queued notice puts two passes ahead of an aged MRPDU build. The 44 ms `CTRL_LOOP_TX_MS` derivation does not count them.
  - The aged-retry spacing is also an input to `CTRL_LOOP_SRP_MS`'s pass-class statement.

Three SUGGESTIONs follow. There is no new RESIDUE.

## Method

**Context, in this order:**
1. `AGENTS.md` and `CONTRIBUTING.md`.
2. The manager's rulings on #665:
   - issuecomment-6620376502 (round 15 continued);
   - issuecomment-6630265194 (round 15 continued (2));
   - issuecomment-6634982529 (round 16).
3. The round 16 REVIEW READY (issuecomment-6673169386).
4. FR_NFR.md 3.4.1:
   - "Backlog, preemption, state access and saved-state service consume this budget."
   - "No extra budget is granted at timer arm, expiry or retry."
   - "The last required recipient's commit ends a notification fan-out."
5. `git diff a3f23bba..d930ea98`, read by file:
   - firmware: `ctrl_loop.c/.h`, `aecp.c/.h`, `aecp_mbx.c/.h`, `srp_mbx.c`;
   - tests and plants: `test_aecp.cpp`, `test_port_loop.cpp`, `loop_step_mutants.py`, `aecp_retry_mutants.py`, `srp_transmit_mutants.py`;
   - harness: `notice_window.py`, `build.py`;
   - docs: sections 13 and 14.
6. The history of the 29 commits since `a3f23bba`.
7. The published evidence `review-evidence/665s2b-r1/author-r16` at `cd93800c`.

I read the prior public review findings on this PR, R711-4 (issuecomment-6611420126) and R712-4 (issuecomment-6611570890), only after my own pass over the diff.

**Evidence integrity** (`receipts/evidence-verify.txt`, `scripts/verify_evidence.py`):
- All 609 `author-r16/` files match `MANIFEST.json`'s `published_sha256`.
- None is unlisted, and 65 are redacted copies.
- The legs ran on `12e5ec56` (firmware `65a56d02`). `git diff 12e5ec56..HEAD` changes only these things that reach an image:
  - comments;
  - `CTRL_LOOP_SRP_MS`, a macro read only by a `_Static_assert`;
  - that `_Static_assert` (`srp_mbx.c:31`);
  - the build-beside-records plant's text in `build.py`.
- `receipts/gates/image-identity.log` (HEAD d930ea98, DIRTY 0) reports "9 of 9 images the same" for the head, arm B, notice, control and heavier-step images.

**Recomputed from raw results** (`receipts/recomputed-rows.txt`, `scripts/recompute_rows.py`):
- **The notice-group rows**, for every leg, match `tables/notice-rows.md`, section 13 and `aecp.h`. For example, at 8x8/2if the SRP longest-held record is 16.48 to 17.11 ms (15.98 to 16.46 with the drafts, 16.58 to 17.10 at struct-ends), and the retried notice is 12.54 to 12.99 ms (12.47 to 13.51 with the drafts).
- **The least margin outside the egress-held `backlog-owed` group** is 0.235 ms: 17.765 ms in `N-A8`, `backlog-adp@verify-aged1-7.service.srp.last.if1`.
- **The leg totals**: 600 groups in the twelve head legs, and 1,489,645 work passes with the struct-ends and 8x8/1if legs. Every leg has 0 refusals and 0 passes over the share.
- **The budget misses** are only `backlog-owed`'s egress-held paths, as before.
- **The pass-class figures** in `ctrl_loop.h` match `tables/pass-classes.md` (head layout, both arms, with and without the drafts):
  - records: 190,420 / 116,176;
  - events: 140,363 / 52,247;
  - none: 171,351 / 128,083;
  - whole-step: 97,806 / 97,378;
  - whole: 12,571 / 9,610;
  - idle: 118,647 / 106,887;
  - every class at least 9,580 cycles under the share; at struct-ends, records is 189,156.

**Reproduced at the head:**
- `run.py --self-test` on a byte copy of the head (`receipts/harness-selftest.log`, rc 0): "self-test: 0 failures", 151 `MUTANT caught`.
- Those include the notice grader mutants (`a retried notice later than its bound is a budget finding only`, `... held to its ceiling, not its bound`, the age-less plant judged as a budget control, `the port answers before the load`) and the two transmit grader mutants.
- The published log for this gate is cut to its first 40 and last 120 lines, so this run is the whole-log check.

**Firmware plants, from the published shard logs:**
- THE RETRY's 19 loop plants (`retry-age-ignored`, `retry-aged-pass-takes-input`, `retry-age-before-the-step-age`, ...) and AECP's retry plants (`retry-in-the-bursts-pass`, `retry-round-before-the-owed-notice`, ...) are caught by name.
- So are THE TRANSMIT's 24 loop plants and THE TICK's cap's 2.

**Probes P1 and P2** (`receipts/probe-method.txt`, `probe-test_aecp.diff`, `probe-two-notices.log`, `probe-aged-build-behind-notices.log`, `scripts/run_aecp_mailbox_arm.py`):
- Both ran in a disposable byte copy of the head, with four probe tests appended to `test_aecp.cpp`'s Mailbox fixture: the real `aecp.c`, `aecp_mbx.c` and `ctrl_loop.c` on the mailbox model, with the model clock advanced by the 2 ms share each pass.

**Hosted checks:** `receipts/hosted-checks-snapshot.txt` was taken while the review ran.
- Completed: `wire-accountability`, `verilator-lint`, `full-ci-gate` and one `Prepare pinned Yosys`, all success; `Physical gPTP` was skipped.
- The Verilator and Yosys shards, the firmware jobs and the docs gates were queued or in progress.
- Those contexts are not evidence here. The manager owns hosted and act acceptance.

**After the probes** (`receipts/clone-state-after.txt`):
- The clone is at `d930ea98`, tree `76a51c45`, with 0 status lines, and its worktree and index match HEAD.
- The six submodule gitlinks are unchanged.
- The only change to the clone is the evidence commit's objects, fetched read-only. No tracked byte, mode or index entry changed.

## The rulings, item by item

1. **THE RETRY** (rulings 6620376502 and 6630265194).
   - **Met:**
     - `ctrl_loop.c:203-211` takes an aged retry as the whole next pass, after THE STEP's age check (`:187-201`).
     - `CTRL_LOOP_RETRY_MS = 4 + 3 x 2 = 10` is derived from the constants (`ctrl_loop.h:265`).
     - `aecp_mbx.c:174` holds 8 + 10 ≤ 20 at compile time.
     - The harness row (`notice_window.py`), the `retry-ageless` control (RA-1 and RA-8, 8 of 8 caught), the grader mutants and the firmware plants are all in place.
     - The single retried notice is 12.30 to 13.51 ms, against 20.
   - **Not met** for notices queued behind one another (**F2**).
2. **The SRP lever** (ruling 6634982529, item 1).
   - **Met:**
     - The last SRP record is within 18 ms at both points, with and without the drafts.
     - No other channel's row passes its bound at either point.
     - `CTRL_LOOP_SRP_MS` is stated beside `CTRL_LOOP_STEP_AGE` and `CTRL_LOOP_RETRY_MS` (`ctrl_loop.h:296-315`).
     - The `transmit-beside-records` control is caught (TB-8, 8 of 8).
   - **Not met:** "derive its bound from the constants" (**F1**).
3. **Every pass class in cycles, at least 6,490 under the share, at both layouts.** Met, as recomputed above. The class no group stages, an aged build's pass, is bounded by composition (**S1**).
4. **Re-measured at the head.** Met. The legs are the head's images. The struct-ends layout ran the subset the author discloses.
5. **Restated from this head's figures.** The figures match. Some statements in `ctrl_loop.h`, `aecp.h` and section 13 do not hold for queued retried notices (**F2**).
6. **Round 15's GATES at the committed head.**
   - Met as published:
     - `gates/lane/summary.txt` gives rc 0 for all 25 lane gates on a clean clone at `d930ea98` (`clone.log`: 0 changed paths);
     - behave: 508 scenarios passed;
     - `test_builder.py`: "ALL GATES PASS EXCEPT 2 NOT RUN";
     - `fw_coverage.py`: PASS (38 files);
     - the store's gate: 455 tests, 121 of 121 planted defects;
     - the four firmware shards: `test_ctrl_firmware: PASS`.
   - I re-executed only the harness self-test.

## Findings

### R711-5-F1 - MAJOR - Conformance, RTL, Robustness - SRP's 18 ms is not derived from the constants, and its measured margin is below the layout swing over the passes it waits

**Where:**
- `sw/firmware/ctrl/loop/ctrl_loop.h:296-315` (`CTRL_LOOP_SRP_MS`), which says: "This bound does not count the composed burst's passes ... sixteen, more than the nine it counts at THE SHARE, so that row fits by those passes' measured cost";
- `docs/design/SPLIT_CONTROL_MEMORY.md` section 13 (THE TRANSMIT);
- the REVIEW READY's first open question.

**Authority:**
- Ruling issuecomment-6634982529:
  - item 1: "Choose the construction by pass class and derive its bound from the constants, as THE STEP and THE RETRY are";
  - its first point: "The 18 ms SRP bound ... holds under every admitted input. The input buckets bound each channel's burst so that the bounds can be proven when the bursts arrive together";
  - its second point: "A pass that fits by less than that [6,490 cycles] fits by chance."
- FR_NFR.md 3.4.1 (SRP/MRP: min(T_svc, C) = 18 ms).

**Evidence:**
- **The constants.**
  - The composed burst's 32 SRP records at 8x8/2if are taken two a pass (D4(b)), in sixteen passes.
  - At THE SHARE that is 32 ms, plus the given-whole passes `CTRL_LOOP_SRP_MS` admits among them (an aged build, an aged step, aged retries): about 34 ms by the author's own statement.
  - Nothing bounds the cost of an SRP drain pass below the share.
- **The measurement.**
  - The row fits by measurement: at most 17.106 ms in the notice groups, 17.765 ms in `N-A8 backlog-adp@verify-aged1-7`.
  - The least margin is 0.235 ms. The ruling's layout swing, 6,490 cycles a pass, is 0.065 ms at 100 MHz. Summed over the sixteen passes the last record waits, it is about 1.04 ms, more than four times that margin.
  - Only one other layout was measured, and on a subset: X4-A8's least margin is 0.457 ms, in a different group.
- **No decision.** The author raised it for the manager (issuecomment-6673169386, Open risks). No ruling on it appears on #665 or #810 before this review began (issuecomment-6673772470).

**Impact:**
- The one family bound round 16 was opened for has no proof under every admitted input.
- A layout, compiler or data change that adds a few percent to SRP's drain passes could put the row past 18 ms. Only a full re-measure would show it, and no constant or compile-time check holds the line.
- This is the "fits by chance" condition the ruling names, at row level.

**Required outcome:** one of the following.
- A construction from which the composed burst's last SRP record is ≤ 18 ms by the constants. Examples:
  - SRP records taken ahead of the other channels' burst records once past a stated age, so that the nine counted passes cover them;
  - enough SRP records a pass, with a stated cycle bound for that pass class;
  - a stated, checked per-pass cost bound for an SRP drain pass that makes 16 such passes, plus the given-whole passes, ≤ 18 ms.
- Or a public manager decision that accepts a measurement-based fit for this row, with the margin rule it must keep. For example, a least margin at least the layout swing times the passes waited, measured at both layouts.

Whichever is chosen, `CTRL_LOOP_SRP_MS` and section 13 state it.

**Verification:**
- The bound reads off the constants, or a `_Static_assert` holds it.
- The 8x8 rows are re-measured at both layouts.
- Or the decision comment is linked from the PR.

### R711-5-F2 - MAJOR - Conformance, RTL, Robustness, Tests, Docs - THE RETRY's 18 ms, its aged-pass spacing, and THE TRANSMIT's 44 ms do not hold with two or more retried notices held together

**Where:**
- `sw/firmware/ctrl/aecp/aecp.h:21-33`: "committed to every recipient within CTRL_LOOP_RETRY_MS ... 8 + 10 = 18 ms, under any input, a backlog ... included ... That holds while nothing waits ahead of its round: ... each notice owed ahead of it costing it its own round and the pass that sends it".
- `sw/firmware/ctrl/loop/ctrl_loop.h:241-246` (`CTRL_LOOP_RETRY_AGE_MS`): "A round leaves no retry held, unless it built a notice ... so the pass after an aged retry's is an ordinary one, and the next aged retry comes at least a millisecond and the age later."
- `ctrl_loop.h:278-295` (`CTRL_LOOP_TX_MS`): "the five after it at most, an aged retry's pass, an ordinary one, an aged step's ..., another ordinary one, and the build's own".
- `ctrl_loop.h:296-315` (`CTRL_LOOP_SRP_MS`): "the aged retries' passes, at least a millisecond and CTRL_LOOP_RETRY_AGE_MS apart".
- Section 13 (`SPLIT_CONTROL_MEMORY.md:1800`): "A retried notice is now inside its 20 ms under any input, by construction."
- Code: `aecp.c:631` `scan` (returns at the first notice built), `aecp.c:746` `aecp_retry`, `round_waits`, `aecp.c:763` `aecp_retry_aged`; `ctrl_loop.c:203-223`.

**Authority:**
- Ruling issuecomment-6630265194, item 1: "From its port's answer, a retried notice is built and committed within 20 ms under every input, backlog and input that leaves no pass empty included ... by pass class and not a cycle estimate."
- FR_NFR.md 3.4.1: "Backlog ... consume[s] this budget"; "No extra budget is granted at ... retry."
- Ruling issuecomment-6634982529, item 1: each channel's bound, with the retried notice's 20 ms among them.
- I note that the ruling said items 1 and 2 of round 15 continued (2) "stand as met". The "nothing waits ahead" clause was already in `aecp.h` at `d0eef1cb`. That acceptance did not test this case, and the clause narrows the ruling's "under every input".

**Evidence:**
- **Code.**
  - `scan` returns at the first notice it builds.
  - Every other due retry stays held, with `retry_since` still at its earliest time.
  - `round_waits` blocks the next round, and `aecp_retry_aged`, while that notice is owed.
  - The notice is sent by the next ordinary pass's poll. The pass after it finds the remaining retry already aged, so it is again a pass given whole to an aged retry.
  - Events whose notices failed in the same scan share one backoff sequence, so they come due together. A face block that is held or resetting (round 15's ruling) fails every such notice at once.
- **P1** (`receipts/probe-two-notices.log`): two GET_STREAM_INFO notices (STREAM_INPUT 0, STREAM_OUTPUT 0) are due together, the port then answers, an event comes before every pass, and each pass takes 2 ms.
  - The aged retries' passes start at +4 and +8 ms, two passes apart, not "at least a millisecond and the age".
  - The notices are committed in the passes starting at +6 and +10 ms: **two more passes for the second**.
  - THE RETRY's own pass accounting is 4 ms of age, the running pass, the round's pass and the send pass. On it, the k-th notice is committed within 10 + 4(k − 1) ms of the shared due time.
  - With the spacing's 8 ms, the second notice is up to **22 ms** after its port's answer, the third 26 ms, against 20.
- **P2** (`receipts/probe-aged-build-behind-notices.log`): a held THE TRANSMIT build that reports aged, under input that leaves no ordinary pass to it.
  - The aged build's pass is the 1st, 3rd and 5th pass with 0, 1 and 2 retried notices held (sequences `T`, `RET`, `RERET`).
  - The aged-retry check comes before the aged-transmit check, and an aged retry's pass is not ordinary. So each queued notice puts two passes ahead of the build.
  - `CTRL_LOOP_TX_MS`'s seven-pass count allows one aged retry's pass.
  - The same spacing is what `CTRL_LOOP_SRP_MS` relies on to count the given-whole passes among an SRP record's wait.
- **Measured evidence does not cover it.** Each `notice-retried-k` group binds one stream and so has one retried notice (`notice_window.py`). The firmware tests (`Mailbox.AgedRetryTakesAPassOfItsOwn`, `Core.HeldRetryAgesFromItsEarliestTimeWhenTheRoundCouldTakeIt`) hold three retries, but time only the first round.
- The measured cost of an aged retry's pass is small (12,571 cycles). So this is a gap in the stated bounds by construction, which is the contract the rulings set, more than a measured miss.

**Impact:**
- The notification bound of FR_NFR 3.4.1 can be exceeded by construction for the second and later of several retried notices, the case a held or resetting datapath produces.
- Three header statements the round's derivations rest on are false in that case:
  - THE RETRY's aged-pass spacing;
  - THE TRANSMIT's 44 ms, and so the 176 ms JoinTime arithmetic;
  - `CTRL_LOOP_SRP_MS`'s count of aged-retry passes.
- No row or test stages the case, so no gate would see a regression.

**Required outcome:**
- A construction under which every retried notice is committed within 20 ms of its port's answer, with k notices held together under input that leaves no pass empty. Examples:
  - a round that builds every notice whose port answers;
  - an age read per notice that takes its build and send into fewer passes;
  - a stated bound on k with a derivation that holds it.
- The aged-retry spacing, `CTRL_LOOP_TX_MS` and `CTRL_LOOP_SRP_MS`'s given-whole pass count re-derived for the same case.
- `aecp.h`, `ctrl_loop.h` and section 13 corrected to match, without the "while nothing waits ahead" narrowing of a bound the ruling states "under every input".
- Or a public manager decision that scopes the 20 ms to the first notice of a group, with FR_NFR.md 3.4.1 updated to say so.

**Verification:**
- A firmware test, with a plant, in which two or more retried notices answer together under sustained input. Each must be committed within the stated bound in model time, and the aged build must take its pass within `CTRL_LOOP_TX_MS`.
- A harness `notice-retried` variant with two notices, graded per notice against 20 ms at both points.
- P1 and P2, re-run at the fixed head, show the restated spacing.

### Suggestions (optional; no verdict effect)

- **S1 - Tests - the aged-build pass class is unmeasured.**
  - No group stages a pass given whole to an aged build. Its worst case is a composition: 171,351 + 12,571 = 183,922 cycles.
  - The composition uses the head layout's heaviest round. The struct-ends layout's round is 13,186 cycles, which gives 184,537, still 15,463 under the share.
  - Suggestion: a harness control or group that holds every pass to records or centiseconds for more than `CTRL_LOOP_TX_AGE` ticks, so that the class is measured. Or state the composition with the worse of the two layouts' rounds.
- **S2 - Docs - the 32x32 estimate's ACMP row.**
  - THE TICK's cap moves the estimate's last ACMP record under the measured line to 21.6 ms (+1.6), as the author discloses.
  - The estimate is not a bound claim of this PR. Section 14 could add this row to "What the estimate leaves to the owner", so that the cap's cost at scale is recorded beside the AECP and SRP rows already over.
- **S3 (retained from R711-4 S1 and R712-4 SUGGESTION-2) - the step's room is not gated on its cost.**
  - The longest step is 0.97 ms against `NVM_STEP_US` = 1.0 ms.
  - The store's plants gate the room check (`step_ignores_room`, `step_needs_more_room`), but no check holds a measured step's cost to `NVM_STEP_US`.

### RESIDUE

None new.
- **Comment rule:** the delta's added C, H, C++, Python, linker-script and hot-list lines carry no bench lane label, lane name, review round, reviewer ID or issue-comment ID. I scanned the raw diff of 2,841 added lines.

## Prior public findings at their causes

| Finding (round 14, head a3f23bba) | Status at d930ea98 | Evidence |
|---|---|---|
| R711-4-F1 = R712-4-F1: an aged step lands among a window's records; N = 2's reason and the least margin | Resolved | Windows opened at the age limit and one short of it are staged (`-aged2-`, `-aged1-` groups, both arms, with and without the drafts). `CTRL_LOOP_STEP_AGE`'s comment (`ctrl_loop.h:230-240`) now states the aged step among the records and the least margin, 0.235 ms, which I recomputed. |
| R711-4-F2: a change's worst case with a save in flight | Resolved | `nvm_store.h:16-38` states 22.15 s beside a save in flight. `save-second` is durable 22,110.071 ms after its change at 8x8 (stated 22,150) and 6,029.841 ms at 1x1 (stated 6,070) (`N-A8/regrade.log`, `N-A1/run.log`). |
| R712-4-F2: the age test cannot tell centiseconds from dispatches | Resolved | The plant `step-age-counts-dispatches` is in `loop_step_mutants.py:131-133` and caught in the published shard. |
| R711-4 RESIDUE-1 = R712-4 RESIDUE-1 (section 14's S bullet) | Resolved | `SPLIT_CONTROL_MEMORY.md:2046` reads as the exact fix. |
| R711-4 RESIDUE-2 (`test_nvm_more.cpp` list) | Resolved | `test_nvm_more.cpp:17-20` is as the exact fix. |
| R711-4 RESIDUE-3 (0.97 / 0.96 ms) | Resolved | 0.97 ms in `nvm_store.h:97`, `ctrl_loop.h:121,237` and `ctrl_nvm/README.md:268`. |
| R712-4 RESIDUE-2 (the age's definition) | Resolved | `SPLIT_CONTROL_MEMORY.md:1442` reads "since it last ran or owed nothing". |
| R711-4 S2 = R712-4 SUGGESTION-1 (a real part's figure) | Taken | `nvm_store.h`: "3.26 s a save at 8x8/2if" on the part of `SAVED_STATE_FASTCONNECT.md` 9.4. |
| R711-4 S1 = R712-4 SUGGESTION-2 (the step's room) | Retained as S3 | Optional. |
| R711-4 S3 = R712-4 SUGGESTION-3 (`capture_coherence` memory) | Outside this PR | Optional; for a new Issue. |

## Reviewer-owned completion ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1, F2) | Rulings 6620376502, 6630265194 and 6634982529 against `ctrl_loop.h:217-315`, `aecp.h:16-49`, `aecp_mbx.c:172-175`, `srp_mbx.c:26-34` and FR_NFR.md 3.4.1; `tables/notice-rows.md` and `pass-classes.md`, recomputed | R711-5 | d930ea98f75be96f1062217d62bccd24dd291265 |
| RTL | UNCLEAN (F1, F2) | `ctrl_loop.c:138-271`: pass order, the aged step, retry and transmit checks, `ordinary`, `tx_pass`, `rx_cap`, overflow and initial values. `aecp.c` `arm` (`:176-215`), `scan` (`:631`), `aecp_retry` (`:746`), `aecp_retry_aged` (`:763`) and `round_waits`. `aecp_mbx.c` attach order and refusals. P1 and P2. | R711-5 | d930ea98f75be96f1062217d62bccd24dd291265 |
| Robustness | UNCLEAN (F1, F2) | Several retried notices answering together (P1, P2). The composed burst at both layouts (X4-A8, X4-NT8). Attach refusal paths (`Mailbox.TimerIdentityAndAttachRefusals`). A round before AECP opens. Re-entry refusals (`CrossInstanceInputsAreRefusedInsideRealCallbacks`, 17 entries). | R711-5 | d930ea98f75be96f1062217d62bccd24dd291265 |
| Tests | UNCLEAN (F2) | `test_aecp.cpp:1565-1635` and `:2176-2266`, `test_port_loop.cpp` (L18, L19), the plant tables (`plants/planttable.md`, shard logs), `notice_window.py`, `selftest_notice.py`, and the harness self-test re-run (151 caught, 0 failures). No test or row has two or more retried notices. | R711-5 | d930ea98f75be96f1062217d62bccd24dd291265 |
| Docs | UNCLEAN (F2) | `ctrl_loop.h` and `aecp.h` statements; `SPLIT_CONTROL_MEMORY.md` sections 13 (`:1797-2033`) and 14 (`:2034-2150`) against `tables/*.md` and `estimate-32x32.md`; the README deltas (AECP, SRP, gtest, harness, store); the prior RESIDUE fixes | R711-5 | d930ea98f75be96f1062217d62bccd24dd291265 |

## Real limits

- I re-executed no full gate bank, sweep, builder, behave, boot run or harness leg. All of those are the author's published receipts at the head, which I spot-checked for integrity and recomputed from their raw results.
- I re-executed the harness self-test, and probes P1 and P2 on the host firmware model.
- P1 and P2 use the host mailbox model with the clock stepped by the 2 ms share. They show pass counts and orderings, not CPU cycles. F2 is a finding about bounds by construction. I made no claim that a measured row exceeds its bound.
- The struct-ends layout ran the subset the author discloses (the notice groups and arm A's window and save groups).
- I did not read the 43 kB PR body line by line.
- Physical calibration was not run. Field skips are not hardware proof.
- Hosted contexts at the head were mostly queued or in progress when I took the snapshot. They are not evidence here.

## Pending manager duties

- Decide or route F1's open question: is SRP's 18 ms to be met by construction from the constants, or by measurement with a stated margin rule?
- Decide F2's scope: is the retried notice's 20 ms owed to every notice held together, or does FR_NFR 3.4.1 change?
- The current-dev merge candidate (builder and native banks) at the merge turn, on live dev `cc204c6f`.
- Hosted and act acceptance of the exact head.
- Carrying S1 to S3 to the suggestion list.

R711-5 FINISHED
