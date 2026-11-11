[R711] NEGATIVE - exact head e7e2b7444a9859b058deff0d9edb575f2fb1946f

R711-6, internal cleared-context review of kebag-logic/milan-fpga PR #810 (issue #665, Mark II split stage S2b: the split firmware within T_svc). I reviewed the exact head `e7e2b7444a9859b058deff0d9edb575f2fb1946f` (tree `66cc0030d8c01411c7e648fb93a5a1a649885489`) on `dev-soft-core` `1d6bf555` (the merge base). Live `dev` is `fa6c094b`.

## Verdict

**NEGATIVE.** Four MINOR findings are open, and between them every lens is unclean. There is no BLOCKER and no MAJOR.

- **F1.** `load_grade.py --check`, the merge gate for 1x1/1if, holds 1x1/1if to the column measured with tsn-c-stack#32, not to the pin. A probe raises a pin-only cost until the pin load is 20.4, and the gate still prints `RESULT: PASS`.
- **F2.** Round 16's 6,490-cycle layout margin is not met at 8x8/2if (99 cycles short), and no ruling disposes of it.
- **F3.** Decision D's tier bounds (R4, R5, R6 by every source) do not hold at either gated point. 1x1/1if is now under the ceiling that round 24 named as the precondition for grading them. No gate and no issue holds the 1x1/1if flip to those bounds.
- **F4.** Four GNU attributes enter the "Portable C11" protocol and port code in this delta. The base has none, and the `-std=c11 -pedantic -Werror` builds do not catch them.

I also record one RESIDUE group (comment IDs and round numbers in new source comments) and one PR-body RESIDUE (the issue numbers #890 and #891 now exist). Five suggestions follow.

What holds, checked against code and receipts rather than the author's summary:
- #882 is fixed: every row that ends at a response states its type and status, and every refusal row is named.
- Both new firmware cuts keep the wire behaviour, and each has planted defects caught by my own campaign shards: the notice is built once and addressed per recipient, and SRP compares with `same`.
- SRP's retained-retry rule matches its stated basis.
- `flip_grade.py` refuses an over-ceiling row.
- Round 27 changed no firmware, so the deviation of a cut measured on a scratch image and not committed is as stated.
- The load model's terms read their sources.

## Method and scope

I reconstructed the task from public state in the order AGENTS.md section 6 gives:
- AGENTS.md, CONTRIBUTING.md and docs/README;
- the #665 body;
- the S2b lane definition (issuecomment-6414297191) and the rulings of rounds 9, 12, 16, 23, 24, 25, 26 and 27, plus decision D and its correction (issuecomment-6759183115, -6759193032);
- the PR body, which I read by sections;
- `git diff 1d6bf555..e7e2b744` (158 files) and `a68536fa..e7e2b744` (227 files, which includes the merged dev-soft-core PRs #812, #844, #853 and #861);
- the history: 50 first-parent commits since the last reviewed head `d930ea98`, 41 of them the lane's own non-merge commits;
- the author packet `review-evidence/665s2b-r1/author-r27` at archive `5e9acdd8`.

I wrote my own findings before I read any earlier review. I then read R711-5 and R712-5 (at `d930ea98`) to settle their findings at this head; they had closed every finding from rounds 1 to 4.

Under the token-economy rule:
- Firmware and RTL the delta does not touch keep their earlier lens verdict. `KL_mbx_dma.sv` and the lane's `milan_soc.py` changes are unchanged since `d930ea98`.
- I reviewed every lane-owned production firmware commit since `d930ea98` at its diff. These are `a5f05f89`, `44483eb9`, `9452c6c7`, `50b3a948`, `d00e5db1`, `e5f02c54`, `feee6824`, `bc98d727`, `dbd57a7a`, `46069672` and `61fef2bb`.
- I reviewed the `d6252b84` merge resolution in `milan_soc.py` (the record mover beside `KL_mbx_cdc`) with `--cc`.
- I read the round 27 harness change (`answers.py`, `grade.py`, `scenario.py`, `flip_grade.py`, `load_grade.py`, `selftest_mutants.py`) in full.

### Evidence integrity

- The packet's `MANIFEST.json` lists 600 `author-r27/` files. All 600 match their published sha256, none is missing and none is unlisted. Four are redacted, and their path-redacted logs are marked as such.
- The archive commit is not GPG-signed (`%G?` = N). Integrity rests on the manifest hashes.
- 196 `.rc` receipts were scanned. The only non-zero ones are:
  - `author-r27/receipts/gates/lane/flip_check_exits_1.rc` = 1, which is by design;
  - two runs in `author-r27/receipts/gates/workflows/killed-1107/` whose job clones were removed under them. The handoff says so, and both jobs were re-run to rc 0 (`dispatch3`).
- The baseline compares show each rebuilt leg's ELF and objcopy images identical to round 26's, with the group logs byte-identical (for example `author-r27/receipts/baseline/GA8-compare.txt`).

## Findings

### F1 - MINOR - Conformance, Tests, Docs - the merge gate holds 1x1/1if to the tsn-c-stack#32 column, not to the pin

**Where:**
- `tb/verilator/ctrl_service_budget/load_grade.py:159`: `GRADED = STATED_US_DONOR`.
- `:245`: `stated()` uses `table or GRADED`.
- `:327-336`: `findings()` grades `CEILING = {'1x1/1if': 0.70}` on that table.
- Docstring `:18-22`: "The gate is graded on the donor's column ... The pin's column is reported."
- `docs/design/SPLIT_CONTROL_MEMORY.md` section 13: "The load gate holds 1x1/1if, 0.250 under its ceiling". 0.250 is the margin on the donor column; at the pin it is 0.237.

**Authority:**
- The round 27 ruling (issuecomment-6788828284):
  - item 4 says `load_grade.py --check` gates 1x1/1if for merge;
  - item 6 freezes the donor and says the check is read "at the pin, not on the 'graded with' column".
- This review's brief asks that 1x1/1if be graded at the pin.
- The round 25 ruling, item 3 ("The gate is graded on the donor column, labelled as owed to the pin move"), predates the split and is the authority the code still follows.
- So round 27's pin rule and round 25's donor rule disagree for the merge gate, and no public text settles which one governs it after the split. Under AGENTS.md section 2, a conflict like this is published, not resolved privately.

**Evidence:**
- `scripts/probe_1x1_column.py` (receipt `receipts/probe_1x1_column.log`) raises a 1x1/1if cost in the pin column only. The costs raised are `record.acmp` and `event.ACMP`, both WALK costs, which the donor column may state lower.
  - With `record.acmp` raised, the load at the pin is 20.407. The merge gate's `findings()` is empty: `RESULT: PASS`.
  - With `event.ACMP` raised, the pin load is 1.461, and the gate also passes.
- `load_grade.py --selftest` (23 of 23) plants only the donor column for 1x1/1if (`controls()`, `over = base = GRADED`), so no control can see this.

**Impact:**
- The image that merges is the pin's: 0.463 at 1x1/1if, which is within 0.70 today.
- The merge gate is blind to any pin-only rise in the five WALK costs (`record.acmp`, `record.adp`, `event.ACMP`, `item.acmp`, `base`), because the donor column states them lower.
- A re-measure that raises one of them at the pin passes the merge gate whatever its size, while the merging image goes over the ceiling.

**Required outcome:**
- Either `--check` holds 1x1/1if at the pin (or at the larger of the two columns) and reports both, with a control that plants a pin-only rise and is refused;
- or a public manager decision records that the merge gate stays on the donor column after round 27, and the docstring and section 13 cite it.
- In either case, section 13's "0.250 under" names the column it is read on.

**Verification:**
- `probe_1x1_column.py` makes `findings()` non-empty for a pin-only raise;
- `load_grade.py --selftest` counts the new control;
- or the decision link is in the PR.

### F2 - MINOR - Conformance, RTL, Robustness - round 16's layout margin is not met at 8x8/2if, and no ruling disposes of it

**Where:**
- The heaviest 8x8/2if work pass, 193,609 cycles (`backlog`, arm A), is 6,391 cycles under the 2.0 ms share.
- The PR body states this ("Round 26's decisions ... 2. Round 16's margin at 8x8/2if") and so does section 13 (round 26's second finding).
- The author's receipts show the margin is consumed by layout alone: `author-r27/receipts/cut/heaviest-records.txt` has the same group moving -15,987 to +2,056 cycles between two images on unchanged harness input.

**Authority:**
- The round 16 ruling (issuecomment-6634982529), item 2: "The heaviest measured pass of each class, at both points, sits at least 6,490 cycles under the 2.0 ms share ... A pass that fits by less than that fits by chance."
- The round 26 STOP reported the shortfall. The round 27 ruling answers that STOP on load only and does not mention the margin.
- The flip-gate issue #890 is scoped to the long-window load.

**Impact:**
- At 8x8/2if a pass class fits the share "by chance" in the ruling's own words.
- A layout or compiler change of the size the author measured (7,620 cycles on one group) puts a pass over the 2.0 ms share. The only thing that would show it is a re-measure.
- No gate holds the 6,490 margin. The share gate holds 0 cycles of margin.

**Required outcome:**
- Restore the margin by construction (round 16's per-pass record cap for the records class, or another stated bound);
- or obtain a public ruling that restates or defers the margin at 8x8/2if, for example carried with the 8x8/2if flip on #890, and cite it in section 13.

**Verification:**
- The 8x8/2if heaviest pass is at least 6,490 cycles under the share at the head and the struct-ends layout;
- or the ruling is linked from the PR and section 13.

### F3 - MINOR - Conformance, RTL, Robustness, Docs - decision D's tier bounds are not in force, and nothing holds the 1x1/1if flip to them

**Where:**
- `docs/design/SPLIT_CONTROL_MEMORY.md:2073`: "By the response-time method, with the base and each item at its stated cost and arrival bound, R4, R5 and R6 still do not fit at either point".
- PR body, "What holds at this head": "What does not hold: R4, R5 and R6 by every source at either point, the last queued notice at 8x8/2if (74 ms against 70 ...)".
- The first queued notice is stated at 22 ms at 8x8/2if. Round 23 set tier 1 to "20 ms at every shape. The 8x8/2if 22 ms grant is not needed for them; report against 20."

**Authority:**
- Round 23 (issuecomment-6732443213), item 3: "The every-source count stays the bound. No row may be held by measurement alone."
- Round 24 (issuecomment-6734415848), item 6: grading the tier design "waits for a load under the ceiling".
- Decision D (issuecomment-6759183115): "The flip gates 1x1/1if and 8x8/2if under the 0.70 load ceiling, **with the tier bounds already in force**".

**Evidence:**
- At this head 1x1/1if is under the ceiling: 0.450 graded, 0.463 at the pin. That is the precondition round 24 named.
- No later ruling re-opens the grading.
- `flip_grade.py` holds only 8x8/2if's load.
- No issue, gate or check refuses a 1x1/1if flip while R4, R5 and R6 are held by measurement alone. The rows do hold by measurement: 6 misses of 945 at 1x1/1if, all three of them egress-held (tsn-c-stack#26).

**Impact:**
- Under decision D, the 1x1/1if flip would be admitted by the load gate alone, without the tier bounds the decision presumes in force.
- At 8x8/2if the bounds would stay unchecked once #890's load is met.

**Required outcome:**
- A public decision on whether the rows by every source must hold at 1x1/1if before this merge, or before each point's flip;
- and, for whichever it is, a gate or a blocking issue that holds each point's flip to R4, R5 and R6 by construction (round 23).

**Verification:** the decision link, and the issue or gate named in the PR body.

This is the carried cause of R711-5-F1/F2 and R712-5-F1/F2/F3 (below).

### F4 - MINOR - Conformance, RTL, Docs - GNU attributes enter the portable C11 protocol and port code

**Where:**
- `sw/firmware/ctrl/aecp/aecp.h:277`: `__attribute__((aligned(64)))`.
- `sw/firmware/ctrl/srp/srp_mbx.c:61, :942, :952`: `__attribute__((noinline))`.
- `sw/firmware/ctrl/port/ctrl_pool.c:22`: `typedef void *__attribute__((may_alias)) ctrl_pool_link`.
- The base `1d6bf555` has no `__attribute__` or `__builtin` in `sw/firmware/ctrl` outside the tests. All four arrived in this delta, in `a5f05f89` and `61fef2bb`.

**Authority:**
- #665 body: "Portable C (C11), no compiler intrinsics in protocol code", and "It must port to a hard core".
- `sw/firmware/ctrl/README.md:4`: "Portable C11 for the on-chip RISC-V, and for a hard core".

**Evidence:** the firmware builds with `-std=c11 -pedantic -Werror` (`ctrl_build.py:70`), which GCC accepts with these GNU extensions, so no gate sees them.

**Impact:**
- A non-GNU toolchain for the hard-core port rejects these lines.
- `may_alias` has no C11 equivalent. Without it, the pool's in-place link access through `void *` on the arena's bytes is the aliasing that `memcpy` avoided.
- Without `aligned(64)`, the response buffer loses the alignment the word-wide copies assume.

**Required outcome:**
- `_Alignas(64)` (C11) for the buffer;
- `noinline` and `may_alias` behind one platform macro with a portable fallback (the fallback for the link is `memcpy`), placed in a platform header outside protocol code;
- or an owner exemption recorded in the README.

**Verification:**
- `git grep __attribute__ -- sw/firmware/ctrl ':!*/test/*'` shows only the platform header;
- the firmware and harness costs are unchanged, or are re-stated.

### RESIDUE

Each item below is wording only. None changes a measurement, figure, verdict, test or code path, and none breaks a privacy rule.

- **RES-1 (comment rule, owner 2026-10-15).** New source comments in this delta show issue-comment IDs and review rounds. All are new since `d930ea98`.
  - **Issue-comment IDs:**
    - `tb/verilator/ctrl_service_budget/load_grade.py`: 18 lines, at `:10-14, :18, :28, :36, :86-88, :110, :174, :378-379, :402, :423-425, :436, :439`;
    - `flip_grade.py:3, :5, :80-81`;
    - `poll_grade.py:32, :57`;
    - `poll_items.py:19, :104, :108`.
  - **Review rounds:** "the round 22 ruling" and "the round 19 ruling ... the round 21 ruling":
    - `poll_grade.py:3, :38`;
    - `poll_items.py:3`;
    - `selftest_polls.py:3`.
  - The full list is in `receipts/residue_comment_ids.txt`.
  - **Exact fix:** replace each citation with the issue and the behaviour or clause it stands for. For example, "(#665 issuecomment-6751196896, item 4)" becomes "(#665: the 0.70 long-window ceiling at 1x1/1if)", and "the round 22 ruling, item 1" becomes "(#665: the polls by source)".
  - Keep the `load_grade.py` docstring's term-list layout. `documented()` parses its term names from `__doc__`, and the parenthetical text is safe to reword.
  - Existing instances outside this delta stay with #746.
- **RES-2 (PR body and docs).** Two issues now exist that the text still describes as future:
  - "The flip at 8x8/2if waits on the flip-gate issue the manager opens" (Status), "the flip-gate issue carries it" (Known limitations) and section 13's "the flip-gate issue". **Exact fix:** name #890.
  - "AEM command_type at or above `0x4000` ... a firmware finding for its own issue" (Known limitations, 4; Round 27 "Three findings"), and `answers.py:103-104`. **Exact fix:** name #891.

## Prior public findings at their causes

| Prior finding (at `d930ea98`) | At this head | Evidence |
|---|---|---|
| R711-5-F1 = R712-5-F1 (MAJOR): SRP's 18 ms met by measurement, not derived from the constants | **Superseded by ruling; cause carried as F3** | Round 23 replaced the 18 ms SRP bound with 90 ms (option B), round 24 item 6 deferred grading the rows, and round 27 item 4 defines REVIEW READY without them. Their derivation by every source still does not hold (`SPLIT_CONTROL_MEMORY.md:2073`), which is F3. |
| R711-5-F2 (MAJOR): THE RETRY's 18 ms, the aged-pass spacing and THE TRANSMIT's 44 ms with several retried notices held together | **Superseded by ruling; cause carried as F3** | `a5f05f89` and later replaced the mechanism: rounds sized by what the pass has left (`round_of`, `ctrl_loop.c`), a build given its own pass, and the queued-notice bounds of round 23 (first 20 ms, last 125 ms). The first queued notice is 22 ms at 8x8/2if, against tier 1's 20. The last is not held by construction at 8x8/2if. |
| R712-5-F2 (MAJOR): THE TRANSMIT can hold a timer-driven MRPDU 44 ms (176 ms for the fourth participant) | **Superseded by ruling; cause carried as F3** | SRP's bound is now 90 ms (round 23). `CTRL_LOOP_TX_MS` is restated in `ctrl_loop.h`, with `_Static_assert(CTRL_LOOP_TX_MS <= CTRL_LOOP_T_SVC_MS)`. R5 and R6 by every source do not hold (F3). |
| R712-5-F3 (MINOR): the retried-notice bound covers only the first of several notices | **Superseded by ruling; cause carried as F3** | Round 23 split the bound into first and last queued notice. The last queued notice at 8x8/2if is not held by construction (F3). |
| R712-5 RESIDUE-1: ragged wraps in `ctrl_loop.h:163-264` | **Resolved** | `a5f05f89` rewrote those paragraphs. No line in `ctrl_loop.h` is over 111 columns. |
| R711-5 S1 to S3, R712-5 suggestions | Not re-assessed | Optional. S3 (the step's room not gated on `NVM_STEP_US`) still applies: `50b3a948` restated the step's cost in `nvm_store.h:93-100` without a check. |

Rounds 1 to 4: R711-5 and R712-5 published every one of their findings as resolved at `d930ea98`. Nothing in this delta reopens them.

## Lens results with evidence

The five sections below cover Conformance, RTL, Robustness, Tests and Docs in turn. Each states what was checked clean before listing the open findings that leave the lens unclean.

### Conformance

**Unclean** (F1, F2, F3, F4). Checked clean:

- **(1) The firmware cuts in this delta keep the mailbox contract and the protocol behaviour.**
  - `46069672`, `fan_out` at `aecp.c:606-657`. The frame offsets match IEEE 1722.1-2021 9.2.1.1 and 7.5.2:
    - destination MAC 0-5, source MAC 6-11, controller_entity_id 26-33, sequence_id 34-35, the u bit at byte 36;
    - the requester is left out (Milan v1.2 5.4.5.1);
    - sequence is incremented only on a sent frame;
    - a backpressured recipient is re-addressed on resume (`k` is not advanced past the failed one).
  - `61fef2bb`: `same()` (`srp_mbx.c:61-70`) is an exact equality replacement for `memcmp(...) == 0` at all six call sites. The `ctrl_pool.c` link-in-place does the same reads and writes as the `memcpy` it replaces.
  - `dbd57a7a`: the retained retry (`srp_mbx.c:1015-1037`, `:595-600`, `:314`, `ctrl_pool.c:195`, `tick`) retries only after `moved` or `ctrl_pool_returned` changes, at most once a centisecond. The refusal records its own changes after `mrp_rx`. The 1 s give-up (`SRP_RX_RETRY_MS`) is unchanged.
  - `50b3a948`: the flash program window sends the same bytes (`ls_window(cmd, 4u + len)` after a copy).
  - None of these touches `sw/mailbox/` (`git log d930ea98..HEAD -- sw/mailbox` holds only the merged S6 commits).
  - The round 27 commits touch no firmware: `git diff --stat 0b37f3d2 HEAD` lists 12 harness and docs files.
- **(2) The load model.**
  - `load_grade.py:257-286`: each term is the stated cost over its source's period. `rec.<ch>` is one record per `mailbox.yaml` `refill_ms`; SRP is records plus retries at `tick_ms`; the timers run at their clauses' periods; GM runs at the 802.1AS intervals.
  - `period_controls` proves that each period is read (13 controls).
  - I reproduced it: `--check` rc 0 (`receipts/load_grade_py___check.log`), giving 1x1/1if 0.463 at the pin and 0.450 graded, and 8x8/2if 0.815 and 0.719.
  - The column issue is F1.
- **(3) #882.** Each AECP, MVU and ACMP probe states its type and status (`answers.py`). The grader finds the probe's own response by sequence_id:
  - ACMP at bytes 62-63 of a response (odd message_type);
  - AEM and MVU at 34-35 with the u bit clear (`grade.py:506-512`).
  - It checks the AEM command_type at 36 (& 0x7FFF), the MVU command_type at 42, the ACMP message_type at byte 15 & 0xF and the status at byte 16 >> 3. These match IEEE 1722.1-2021 9.2.1.2, 8.2.1 and Milan v1.2 5.4.3.1.
  - GET_AVB_INFO `0x0027` is sent on AVB_INTERFACE (descriptor_type 9) index 0.
  - Each refusal row's label carries `, refused <status>` (`author-r27/receipts/rows882.txt`), and `unstated()` refuses an unnamed refusal.
- **(4) The flip check.** `flip_grade.py` reads `STATED_US` (the pin) through `load_grade.load` and exits 1 at 0.815. `--selftest` gives 6 of 6, `--check` gives rc 1 (`receipts/flip_grade_py___*.log`). Its first control plants the row's own load against a ceiling 0.001 under it.
- **(5) The deviation.** The cut's `author-r27/receipts/cut/q1.diff` touches only `ctrl_mem.c` and `srp_mbx.c`. It is not in the tree, and its ledger refusal (`QD8`: "58 RAMB36 ... exceeds the 57.5") is receipted. The manager accepts this.
- **#891.** The `& 0x3fffu` at `aecp.c:428` is already in the base (`1d6bf555` line 341). It is not in scope and is now #891.

### RTL (and architecture)

**Unclean** (F2, F3, F4). Checked clean:
- **The merge `d6252b84`'s `CtrlMailbox`** (`sw/litex/milan_soc.py`, the `--cc` hunks at 3110-3260) wires the host side through the record mover (`c`/`h`) and the datapath side through `KL_mbx_cdc` and the two AXIS FIFOs, only with a `dp`. Without one it holds the datapath side idle as before.
- **The rest of the RTL and SoC is unchanged since `d930ea98`**: `KL_mbx_dma.sv`, and the lane's `milan_soc.py` except that merge. The earlier lens verdict holds there.
- **The loop's scheduling (`a5f05f89`, `ctrl_loop.c`):**
  - each pass's whole-pass classes are spaced by `whole_runs`;
  - the records sweep is bounded by the share deadline;
  - `_Static_assert`s hold THE SHARE's passes against the SRP and TX waits.

### Robustness

**Unclean** (F2, F3). Checked clean:
- Backpressure resume in `fan_out`, covered by the plants `notice-resumed-walk-from-the-row-start` and `notice-resumed-from-the-first-recipient`, both caught.
- A freed registration skipped, covered by `notice-to-a-freed-registration` (caught).
- The retained retry's give-up past 1 s.
- `ls_program`'s length guard (`len > LS_PAGE` refused before the 260-byte stack copy).

### Tests

**Unclean** (F1). Checked clean, all on this head in my own clones:

| Campaign | Result | Receipt |
|---|---|---|
| `firmware-unit` step: `test_ctrl_firmware.py --require-rv32 --self-test --jobs 4 --shard 0/4` | rc 0, `test_ctrl_firmware: PASS`, 67 `[ok]` | `receipts/fw_shard0.*` |
| `fw_coverage.py --selftest` then `--check --jobs 4` | rc 0, `firmware coverage: PASS (38 files)` | `receipts/fw_coverage.*` |
| `firmware-control-mutants`: `--shard 1/4` | rc 0, `mutants: 672 of 672 caught`, 672 `[ok]` | `receipts/fw_shard1.*` |
| `firmware-aecp-mutants`: `--shard 2/4` | rc 0, 220 `[ok]`, including all eight `aecp_fan_mutants.py` plants | `receipts/fw_shard2.*` |
| `firmware-srp-mutants`: `--shard 3/4` | rc 0, 340 `[ok]`, including the three `same` plants and the four retry plants (`no-retry-after-a-change`, `retry-without-a-change`, `retry-every-pass`, `retry-tick-never-set`) | `receipts/fw_shard3.*` |
| `test_ctrl_nvm.py --require-rv32 --self-test --jobs 4` | rc 0, `saved-state store gate (#665 F1): OK across 5 shape(s), 455 tests, and all 121 planted defects reddened` | `receipts/nvm.*` |
| The harness self-test, `run.py --self-test` | rc 0, `self-test: 0 failures`, 196 `MUTANT caught` lines, all 14 round 27 mutants among them | `receipts/harness_selftest.*` |
| `load_grade.py --selftest` / `flip_grade.py --selftest` | 23 of 23 / 6 of 6, both rc 0 | `receipts/*_selftest.*` |

The fourteen round 27 harness mutants (`selftest_mutants.py:442-469`) cover:
- a skipped status or type check;
- a response chosen by channel rather than by sequence_id;
- MVU read as AEM;
- unstated and unnamed refusals;
- the GET_AS_PATH plant;
- the flip's ceiling, column and pass-through.

### Docs

**Unclean** (F1: section 13's "0.250 under" read on the donor column; F3: the flip's preconditions). Checked clean:
- `docs_check.py`: rc 0, 0 findings over 217 md files and 1,555 scrubbed text files (`receipts/docs_check.*`).
- `check_py_idiom.py`: rc 0 (`receipts/py_idiom.*`).
- Section 13's round 27 paragraphs and the harness README state the split, the baseline, the cut and the refusal rows as the code and receipts show them.
- All lane commits since the base are one line, with no trailer.
- RES-1 and RES-2 are wording only.

## Suggestions (optional; no verdict effect)

- **S1 (Tests).** Run `load_grade.py --check --selftest` and `flip_grade.py --selftest` in a CI job. They are pure Python over the tree, PyYAML and the tsn-c-stack headers. Today no workflow runs them (`git grep load_grade .github` is empty), so "held for merge" rests on the lane's own pass.
- **S2 (Tests).** No arm measures GET_AVB_INFO, GET_COUNTERS or GET_STREAM_INFO with the face window answered, nor PROBE_TX answered SUCCESS. The author discloses this as D1. A later harness row would close it.
- **S3 (Tests).** The `ctrl_pool.c` link-in-place change has no plant of its own. The existing pool plants (`pool-free-leaks`, `pool-follows-a-cut-free-list`) cover the free list.
- **S4 (Tests).** `flip_grade.controls` items 5 and 6 compare module constants with literals. The harness mutants are what prove the semantics.
- **S5 (Docs).** In section 13's 8x8/2if row, the "three largest graded terms" are the donor column's, beside the pin load that the flip check holds. Listing the pin's terms (`srp` 0.219, `rec.acmp` 0.088, `item.acmp` 0.070) beside them would match the held figure.

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1, F2, F3, F4) | `aecp.c:606-673`, `srp_mbx.c:61-70, 560-645, 995-1045`, `ctrl_pool.c:16-22, 121, 189-195`, `nvm_flash_litespi.c:167-250`, `load_grade.py`, `flip_grade.py`, `answers.py`, `grade.py:506-700`, `scenario.py:425-470`, the rulings cited above | R711-6 | e7e2b7444a9859b058deff0d9edb575f2fb1946f |
| RTL | UNCLEAN (F2, F3, F4) | `d6252b84` `--cc` on `milan_soc.py`, `ctrl_loop.c` delta, `ctrl_loop.h` asserts, `aecp.h:277` | R711-6 | e7e2b7444a9859b058deff0d9edb575f2fb1946f |
| Robustness | UNCLEAN (F2, F3) | `fan_out` resume, retained retry, `ls_program` guard, `heaviest-records.txt` | R711-6 | e7e2b7444a9859b058deff0d9edb575f2fb1946f |
| Tests | UNCLEAN (F1) | own runs of shards 0 to 3, `fw_coverage`, the NVM gate, harness self-test, load and flip self-tests, `probe_1x1_column.py`, `selftest_mutants.py:442-469` | R711-6 | e7e2b7444a9859b058deff0d9edb575f2fb1946f |
| Docs | UNCLEAN (F1, F3) | `SPLIT_CONTROL_MEMORY.md` section 13 (round 27 diff), the harness README, the PR body, `docs_check.py`, `check_py_idiom.py` | R711-6 | e7e2b7444a9859b058deff0d9edb575f2fb1946f |

## Real limits

- **Not run by me:**
  - the full sweep, the Yosys banks, `docs.yml` and `elaborate.yml`'s jobs, `test_builder.py`, `ctrl_split_boot`, the twin, `split-cdc` and `bdd-conformance`;
  - the harness legs at either point, since I did not rebuild any image.
  For these I rely on the author's receipts, whose hashes I verified. I did not use Verilator.
- **My toolchain differs from CI's.** My campaigns ran on the host toolchain (GCC 16.2.1, gtest 1.18.0) with the pinned RV32 SDK, not on the CI image's.
- **Hosted evidence at this exact head is not green.** It has 17 success, 13 failure, 38 cancelled and 1 skipped (`receipts/hosted_check_runs.tsv`; the apt failure is in `receipts/hosted_docs_gates0_excerpt.txt`). The failures I opened are infrastructure: `docs-gates-0` failed with apt's "Temporary failure resolving 'azure.archive.ubuntu.com'" (exit 100), and the rest finished within seconds or were cancelled behind it. The manager owns hosted and act acceptance.
- **The clone is restored.** It is at the exact head bytes after my probes: tree, index, modes, no skip or assume flags, and the six gitlinks at their pinned revisions with every submodule clean (`receipts/restore_check.txt`). My campaigns ran in four disposable clones under the scratch directory.
- **Not in this review:** physical calibration, field skips and any hardware. No manager source bank runs at this head, and I claim none.

## Pending manager duties

- Rule on F1's column conflict (round 25 item 3 against round 27 item 6), F2's margin and F3's tier bounds for the flip.
- Carry RES-1 and RES-2 to the residue checklist.
- Validate the current-dev merge candidate (source base `a68536fa`, live dev `fa6c094b`) with its builder and native banks.
- Accept the hosted contexts at the final head.

R711-6 FINISHED
