[R712] NEGATIVE - exact head e7e2b7444a9859b058deff0d9edb575f2fb1946f

# R712-6: external review of PR #810 (#665 Mark II split, stage S2b)

- Head `e7e2b7444a9859b058deff0d9edb575f2fb1946f`, tree `66cc0030d8c01411c7e648fb93a5a1a649885489`, target `dev-soft-core`. The merge base is `1d6bf555`, which descends from source base `a68536fa`. The PR's own content is `git diff 1d6bf555...e7e2b744`: 158 files, +17,533/-1,464.
- The previous R711/R712 rounds were at `d930ea98`. Since then the lane added 41 commits and the `dev-soft-core 1d6bf555` merge `d6252b84`. I reviewed the whole PR, weighting the parts that changed since then. Code untouched since `d930ea98` keeps its earlier lens result unless something it depends on changed.
- Authority, rebuilt from public state in this order: AGENTS.md; CONTRIBUTING.md section 3; the #665 body; the S2b rulings of rounds 4, 8, 23, 24, 25, 26 and 27 (issuecomment-6460942408, -6492443864, -6732443213, -6734415848, -6751196896, -6779973927, -6788828284); the owner decisions D (issuecomment-6759183115, -6759193032, -6759197512); #882, #890 and #891; FR_NFR.md 3.4.1. Then the diff and its history, the round 27 author packet (archive `5e9acdd8`, `review-evidence/665s2b-r1/author-r27`), and the hosted check runs at this exact head.
- I applied all five lenses. I read prior review findings only after my own pass and verdict draft.

Verdict: **NEGATIVE**. Three findings are MINOR and open: F1, F2 and F3. Together they leave all five lenses unclean. No finding is BLOCKER or MAJOR. The round 27 work is sound in itself:
- the #882 response checks;
- the flip check and its controls;
- the load model;
- the not-committed SRP cut, which the manager accepts;
- the gate receipts.

The findings are:
- a gate-reading conflict that needs a decision (F1);
- a fault-path regression from round 21's record-mover pipelining, which my probe confirms (F2);
- one misattributed figure in section 13 (F3).

## Findings

### R712-6-F1 - MINOR - Conformance, Tests - `tb/verilator/ctrl_service_budget/load_grade.py:159`, `:89`, `:320-337` - the merge gate holds 1x1/1if on the column graded with tsn-c-stack#32, not at this tree's pin

**Authority and evidence**
- `GRADED = STATED_US_DONOR` (`:159`). `findings()` grades `CEILING = {'1x1/1if': 0.70}` on `table or GRADED` (`:320-337`). So `load_grade.py --check` holds 1x1/1if at 0.450, the column with tsn-c-stack#32 applied in a scratch build. The merging tree's own pin, 0.463, is only reported (`receipts/load_grade_check.txt`).
- The round 27 ruling, item 6, reads 8x8/2if at the pin, because the donor is frozen and this tree's pin does not move. `flip_grade.py` does that (`COLUMN = load_grade.STATED_US`).
- This review's brief asks that 1x1/1if also be graded at the pin, not at a donor's "graded with" column.
- The round 25 ruling, item 3 (issuecomment-6751196896), says "the gate is graded on the donor column". No later ruling restates that for 1x1/1if.
- So the published rulings and the brief disagree. AGENTS.md section 2 asks for that kind of conflict to be published for a decision, not settled privately by the reviewer.

**Probe** (`scripts/probe_pin_1x1.py`, `receipts/probe_pin_1x1.txt`): in memory only, I raised the pin column's 1x1/1if `record.acmp` to 2000 us. A WALK cost may legitimately differ between the columns.
- The pin load becomes 0.807, over the 0.70 ceiling.
- `findings()` stays empty. The merge gate passes a tree whose own 1x1/1if load is over its ceiling.
- None of the gate's 23 controls or the flip check's six covers a pin-only rise at 1x1/1if.

**Impact**
- At this head both columns pass (0.463 at the pin), so today's merge outcome is unaffected.
- But the gate that holds 1x1/1if "for merge" does not hold what merges. A later change that raises a WALK cost only at the pin would pass it.

**Required outcome**, either of:
- the merge gate holds 1x1/1if at the pin as well as with tsn-c-stack#32 (each column at most 0.70), with a planted pin-only rise refused by name; or
- a public manager ruling that the merge gate for 1x1/1if is the donor column, despite round 27 item 6's reason, linked from `load_grade.py`'s docstring and section 13.

**Verification**
- `load_grade.py --check` reports and holds 1x1/1if at the pin.
- `--selftest` refuses the pin-only plant.
- Or the ruling is linked.

### R712-6-F2 - MINOR - Conformance, RTL, Robustness, Tests - `sw/firmware/ctrl/mbx/mbx.c:511-529` and `:542-544`, `sw/firmware/ctrl/aecp/aecp_mbx.c:29`, `sw/firmware/ctrl/aecp/aecp.c:630-646`, `sw/firmware/ctrl/mbx/mbx.h:181-189` - the pipelined record mover reports a move's ERR against a record that did not make it

**Background.** Round 21's cost cut `a5f05f8948` (after `d930ea98`) split `mbx_tx_send` into `mbx_tx_begin` and `mbx_tx_commit`. The mover's move now overlaps the next recipient's addressing. `mbx_tx_commit` calls `mbx_dma_wait()` whenever `CTRL_MBX_DMA_BASE` is defined (`:519-523`), whether or not this record started a move. The mover's ERR flag is sticky until the next accepted start (`hdl/milan/mailbox/KL_mbx_dma.sv:296-300`). At `d930ea98`, `mbx.c:513-516` checked ERR only on the aligned path, for the record that moved.

1. **Word-loop records after an ERR.** After one move ends in ERR, every record whose frame is off a word goes through the word loop and starts no move. It is still refused `MBX_STATUS_BAD` and not committed, and so is each later such record, until an aligned frame's move clears the flag. This holds on every channel: ADP, ACMP and MAAP send through `mbx_tx_send`.
   - Probe (`scripts/probe_dma_sticky_err_test.cpp`, run with `scripts/run_unit_arm.py` on a scratch copy; `receipts/probe_dma_sticky_err.txt`): after a failed aligned send, `mbx_tx_send(buffer + 1, 61)` returns BAD twice and TX_HEAD stays at 100, not 118.
   - Every other `unit` arm test passes ("1 FAILED TEST", the probe's).
   - The header's own contract, "a record the move failed, as mbx_tx_send" (`mbx.h:189`), now also catches records the move never touched.
2. **A notice's fan-out under an ERR.**
   - When recipient n's move fails, the failure is returned by recipient n+1's `mbx_tx_begin` (`:542-544`). `fan_out` then marks the notice owed and resumes at n+1 (`aecp.c:630`, `:646`). Recipient n was counted sent, and its `sequence_id` advanced (`aecp.c:640`), but it is never resent.
   - `fan_end` discards the last move's result (`(void)mbx_tx_commit`, `aecp_mbx.c:29`). A failed last recipient is likewise dropped, and the notice's completion is recorded as if it were sent.
   - Before the cut, the failing record's own call returned BAD. `fan_out` then resumed at that same recipient.

**Impact**
- The ERR path is reached only by an error response on the mover's memory port, or a refused start. It is a fault path, not normal traffic.
- On it, the cut changes protocol behaviour. A registered controller silently misses an unsolicited notice (IEEE 1722.1-2021 7.5.2; Milan v1.2 5.4.5) whose sequence_id was spent.
- A channel whose frames are off a word is refused until another channel's aligned move clears the flag.
- No test exercises a word-loop record or a fan-out after a failed move. `T2AMoveEndingInErrorIsNotCommitted` covers only aligned frames.

**Required outcome**
- A record's commit judges only the move that record started. A word-loop record never inherits an earlier ERR.
- A failed move is reported, or retried, for the record it carried. In a fan-out, the recipient whose move failed is the one the notice resumes at.
- `fan_end` does not discard its commit's result.
- The behaviour is stated in `mbx.h`.

**Verification**
- A driver test: an ERR, then a word-loop record, which must commit.
- An AECP test: a fan-out whose k-th recipient's move fails sends that recipient again.
- A named plant for each in the mutant campaigns.

### R712-6-F3 - MINOR - Docs - `docs/design/SPLIT_CONTROL_MEMORY.md:2138` - the not-committed cut's ROM growth is attributed to the wrong image

**Evidence**
- Section 13 says: "The cut also adds 152 B, which takes arm A's image with tsn-c-stack #32 over the 8x8/2if ledger (122,936 B in 122,880)".
- The receipts show:
  - +152 B at the pin (`GA8` 122,328 B to `QA8` 122,480 B);
  - +160 B for arm A with tsn-c-stack#32 (`D8` 122,776 B to `QD8` 122,936 B; `author-r27/receipts/baseline/D8-leg.log`, `receipts/cut/heaviest-records.txt`).
- HANDOFF.md, PR-BODY.md and the REVIEW READY comment state both figures, or the +160 B, correctly.
- The fix changes the figure quoted for the image the sentence names, so I record this as MINOR, not RESIDUE.

**Impact.** The authoritative design document misstates the measured ROM growth of the image the sentence is about. The conclusion is unchanged (over the ledger either way).

**Required outcome.** The sentence reads, for example: "The cut also adds 152 B at the pin and 160 B with tsn-c-stack #32, which takes arm A's image with tsn-c-stack #32 over the 8x8/2if ledger (122,936 B in 122,880)".

**Verification.** Section 13 against `receipts/cut/heaviest-records.txt` and the baseline D8 leg's ROM bytes.

### RESIDUE-1 - wording only, source comments - new instances of issue-comment IDs and review-round labels (owner comment rule)

The owner comment rule: comments state behaviour and reasons with issue and requirement IDs, never issue-comment IDs or review rounds. Existing instances are tracked by #746. The new instances in this PR (`receipts/residue_scan_pr.txt`, 31 added lines) are:
- `tb/verilator/ctrl_service_budget/flip_grade.py`: 3 lines in its docstring and its control comment, added in round 27;
- `tb/verilator/ctrl_service_budget/load_grade.py`: 18 lines, its docstring, `CEILING`, the controls; 4 of them added in round 27;
- `tb/verilator/ctrl_service_budget/poll_grade.py`: 4 lines, "the round 22 ruling", "the round 19 ruling", "the round 21 ruling", issue-comment IDs;
- `tb/verilator/ctrl_service_budget/poll_items.py`: 4 lines;
- `tb/verilator/ctrl_service_budget/selftest_polls.py`: 1 line.

**Exact fix.**
- Drop each `issuecomment-NNNN` and each "the round N ruling" from these comments, keeping the issue and the decision's substance. For example, `(#665 issuecomment-6788828284, items 4 and 6)` becomes `(#665: 8x8/2if is held by the flip check at the pin, #890)`, and `(#665 issuecomment-6751196896, item 4)` becomes `(#665: the 0.70 ceiling, option D)`.
- No behaviour or text outside the comments changes.
- (`plat_mutants.py`'s "B10" is a test-case identifier that predates the PR, `ctrl_mutants.py:615` at `1d6bf555`. It is not a lane label.)

### RESIDUE-2 - wording only, PR body - the round 26 section's "The load at this head" table describes round 26's gate

- Under "### Round 26 (the cuts, at `0b37f3d2`; unchanged by round 27)", the block headed "**The load at this head** (`load_grade.py --check`)" gives 8x8/2if a 0.70 ceiling, graded at 0.719 by `load_grade.py --check`.
- At this head that gate no longer holds 8x8/2if. The Round 27 section's table states the head correctly.

**Exact fix.** Head the round 26 block "**The load at round 26's head `0b37f3d2`** (`load_grade.py --check` as it then stood)", or delete it in favour of the Round 27 table.

### Suggestions (optional, do not affect coverage)

- **S1. A named plant for `ctrl_pool`'s in-place link** (`sw/firmware/ctrl/port/ctrl_pool.c:124`, `:192`, cut `61fef2bb`). The cut has no plant of its own.
  - My plant, a freed block linked to NULL (`scripts/probe_pool_link_plant.txt`), is caught by 4 SRP arms (`receipts/probe_pool_link_cut_arms.txt`).
  - The same arms pass at head bytes (`receipts/probe_pool_control_head_arms.txt`).
  - So the behaviour is guarded. A named row in `ctrl_mutants.py` would keep it that way.
- **S2.** `answers.py:105`'s comment on `UNKNOWN = 0x3FF0` explains the 14-bit decode it works around. Cite #891 there, so the workaround is removed when #891 lands.
- **S3. Publish the mutant logs whole.** The AECP and SRP mutant campaigns are published as 201-line tails (`rtl-fast__firmware-{aecp,srp}-mutants__ci_step_9.log.tail`). The 220 and 340 `[ok]` counts the handoff states cannot be checked from the archive; the tails show 50 and 110 lines, rc 0 and `test_ctrl_firmware: PASS`. Publishing the whole logs, or their `[ok]` count lines, makes the counts checkable.
- **S4. #882.** The PR body carries no `Closes #882`, and #882 is open while the REVIEW READY marks its three items met. Close it by hand at merge, or add the keyword.
- **S5.** Shard 3 of the author's sweep left ` M hdl/ieee1722/avtp/doc/TEST_RESULTS.md` (`gates/sweep/shard-3-tree-after.txt`). A suite rewrites a tracked file. This is outside this PR's scope; consider an issue.

## The brief's checks

**1. Firmware cost cuts since the previous reviewed head, against the mailbox contract and the protocol.** Each was read against its clause and its plant.
- **AECP notice built once, addressed per recipient** (`4606967266`, `aecp.c:565-654`).
  - `address()` writes exactly the bytes the old `put48`/`put48`/`put64`/`put16` calls wrote: 0-5, 6-11, 26-33 and 34-35.
  - The mask walk resumes at the stopped recipient. The requester is excluded (IEEE 1722.1-2021 7.5.2; Milan v1.2 5.4.5.1).
  - Eight plants in `aecp_fan_mutants.py`; 220 `[ok]` with rc 0 per the handoff, tail only (S3).
- **SRP `same()`** (`61fef2bb`, `srp_mbx.c:54-70`). An exact byte-equality replacement of `memcmp(...) == 0` at all six sites, with three plants (`srp_compare_mutants.py`). The pool link change in the same commit: S1.
- **SRP retry only after a change, one a centisecond** (`dbd57a7a`, `srp_mbx.c:1010-1040`). It matches round 25 item 1: `moved` and `ctrl_pool_returned` are captured at the refusal, `retry_spent` is reset by the tick, and the 1 s give-up is unchanged. It has tests (`srp_rx_retry.cpp`) and plants (`srp_retry_mutants.py`). `load_grade.RETRY_RULE` reads the lines.
- **The loop's rounds, THE DRAIN, THE TICK's cap and channel rotation** (`a5f05f89` to `e5f02c54`, `ctrl_loop.c`). The static asserts hold `CTRL_LOOP_SRP_MS` = 18 ms and `CTRL_LOOP_TX_MS` = 20 ms at or under T_svc (`ctrl_loop.c:195-200`), and `AECP_QUEUED_MS` at or under its ceiling (`aecp_mbx.c:180`). The mutant files are `loop_step_mutants.py` and `ctrl_mutants.py`.
- **The record mover's pipelining** (`a5f05f89`): F2.
- **The flash page copy** (`50b3a948`): read; the store's mutants are in `nvm_mutants.py`.
- **Round 27 itself changes no firmware, RTL, contract or submodule.** `git diff --stat 0b37f3d2 e7e2b744 -- sw hdl third_party protocol-processor gptp-processor` is empty.
- **`sw/mailbox/mailbox.yaml`** is unchanged in the delta.

**2. The load model.**
- Each `rec.<ch>` term is cost / `refill_ms`, from `mailbox.yaml` (`load_grade.py:264`).
- SRP's retries come at the tick rate (`:266`).
- AECP's owed frame is costed by what each source sends (`:270-271`).
- The timers come at their expiry rates, GM from IEEE 802.1AS-2011's intervals, and builds per JoinTime (IEEE 802.1Q-2018 Table 10-7).
- Each term has a docstring source, held by `unsourced()`.
- My own `--check` and `--selftest` match the author's byte for byte, apart from my rc lines: 1x1/1if 0.463 at the pin and 0.450 graded; 8x8/2if 0.815 and 0.719; 32x32/2if 2.150 and 1.659; 23 of 23 controls (`receipts/load_grade_*.txt` against `author-r27/receipts/load/`).
- Is 1x1/1if graded at the pin? No: F1.

**3. #882.**
- `answers.py` reads each field at its frame offset:
  - AEM `command_type` at byte 36, the u bit masked;
  - MVU's after its protocol_identifier, at 42;
  - ACMP `message_type` at 15, its status at 16 >> 3, and its sequence_id at 62 (`grade.response_sequence`);
  - the status tables, IEEE 1722.1-2021 Table 7-141 and Table 8-3.
- GET_AVB_INFO is `0x0027`, descriptor_type 9 and index 0, control_data_length 16 (7.4.40.1).
- Every response row states its type and status. Rows that are refusals are named. `run.unstated` refuses an unstated row.
- My subset run of `answer_checks` and `ceiling_checks`, with each round 27 mutant against only those checks (`scripts/selftest_r27_subset.py`, `receipts/harness_selftest_r27_subset.log`):
  - 47 checks pass;
  - all 14 round 27 mutants are caught, the GET_AS_PATH plant among them;
  - the 9 "escapes" in that log are older `run:`/`load:` mutants aimed at checks outside the subset, expected there.
- D1 (SUCCESS asserted in arm B only) is disclosed. Arm B's aecp group is a gate leg.

**4. `flip_grade.py`.**
- `--check` exits 1 with "OVER 8x8/2if: the load 0.815 at the pin is over the flip ceiling 0.70".
- `--selftest` refuses 6 of 6, the over-ceiling and within-ceiling pair among them (`receipts/flip_grade_*.txt`).
- It reads `load_grade.STATED_US`, the pin.
- No workflow runs it (`git grep` finds no reference in `.github/`), as round 27 item 4 requires ("apart from the merge gates").
- Note: no workflow runs `load_grade.py --check` either. The CPU budget harness is a local gate whose receipts the lane publishes.

**5. The round 27 deviation.**
- `receipts/cut/q1.diff` applies cleanly to the head (`git apply --check`, `ctrl_mem.c` and `srp_mbx.c`), and none of it is in the tree.
- Its measurement is in `heaviest-records.txt` and the QA8, QN8 and QD8 logs (QD8 refused by the ledger, rc 1).
- I confirm the deviation's facts. The manager accepts it.

**6. The gates.**
- The packet: all 600 entries of `MANIFEST.json` under `author-r27/` match their published sha256. 4 logs were rewritten for publication and record both hashes. One helper, `assemble_pr.py`, is withheld with its hash recorded (`receipts/packet_manifest_verify.txt`, `receipts/packet_index_verify.txt`).
- The workflow step table: 139 steps at rc 0, 226 not run (each with a reason), 0 bad.
- The firmware jobs: control mutants "672 of 672 caught"; `firmware-unit` PASS, coverage "PASS (38 files)"; `ctrl_boundary: PASS` in both boundary jobs.
- The AECP and SRP mutant runs that ended 11:05 died with their job clones removed (`FileNotFoundError`). They were re-run to rc 0 and the failed outputs set aside, as the handoff discloses.
- The sweep: 15 + 17 + 17 + 16 = 65 suites, 2,613,726 checks, 0 failures, each shard at `e7e2b744`.

## Prior public findings at this head

| Finding (at `d930ea98`) | At `e7e2b744` | Evidence |
|---|---|---|
| R712-5-F1 = R711-5-F1, MAJOR: SRP's 18 ms met by measurement, not the constants | Resolved | THE DRAIN: `CTRL_LOOP_SRP_PASSES = 1 + 2 x CTRL_LOOP_SRP_DRAINS` = 9, so `CTRL_LOOP_SRP_MS` = 18 ms. Static asserts at `ctrl_loop.c:196`, `:199` and `:200` (`SRP_DRAINED >= MBX_CH_SRP_RATE_BURST`). FR_NFR.md 3.4.1's SRP row is now 20 ms, owner 2026-11-06, by construction. README `:77` states nine passes as the deepest wait. |
| R712-5-F2, MAJOR: THE TRANSMIT holds a timer-driven MRPDU 44 ms | Resolved | `CTRL_LOOP_TX_PASSES` = 1 + `WHOLE_RUN` + 3 + `MBX_N_IF` = 10 at two interfaces, so `CTRL_LOOP_TX_MS` = 20 ms. Static assert at `ctrl_loop.c:198`. `mrpdu_grade.py` times each join, periodic and LeaveAll MRPDU from its TICK to its commit. The plant `transmit-aged` and the selftest rows are at README `:1275-1278`. |
| R712-5-F3 = R711-5-F2, MINOR/MAJOR: the retried-notice bound covers only the first of several notices | Resolved | Notices are taken in rounds (`a5f05f89`). Every queued notice is bounded by `AECP_QUEUED_MS`, derived in `aecp_mbx.h:37-47` and held to `AECP_QUEUED_CEILING_MS` (25 ms at 1if, 70 ms at 2if) by a static assert (`aecp_mbx.c:180`), within option D's 125 ms last-queued-notice tier. The PR body discloses that THE DRAIN's derived pass count gives 74 ms at 8x8/2if against 70 ("What does not hold"). I record that as a flip-time limit, not as this finding. |
| R712-5 RESIDUE-1: ragged wraps in `ctrl_loop.h` | Resolved | `ctrl_loop.h` was rewritten in `a5f05f89`. No line is over 120 columns, and no short orphan line follows a full comment line. |
| R711-1..4 and R712-1..4 findings | Carried resolved by R711-5 and R712-5 at `d930ea98` | Nothing in the delta touches their artifacts in a way that reopens them, from what I spot-checked: the step age, the save in flight, `nvm_store.h`. |
| R711-5 and R712-5 suggestions (the aged build's class, struct-ends, the step's room, flash part) | Optional, not re-litigated | |

## Lens ledger (reviewer-owned)

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1 MINOR, F2 MINOR) | The round 4, 8, 23-27 rulings and decision D; #882's acceptance, met; #890; FR_NFR.md 3.4.1 rows at `:395`; `answers.py` against IEEE 1722.1-2021 7.4.40.1, Tables 7-141 and 8-3, Milan v1.2 5.4.3.1; `aecp.c:565-654` against 7.5.2 and Milan 5.4.5.1; `srp_mbx.c` retry against round 25 item 1; `load_grade.py:241-286` against `mailbox.yaml`; `flip_grade.py` against round 27 items 4 and 6 | R712-6 | `e7e2b7444a9859b058deff0d9edb575f2fb1946f` |
| RTL | UNCLEAN (F2 MINOR) | `hdl/milan/mailbox/KL_mbx_dma.sv:280-380` (ERR set and clear, the refused start), unchanged since `d930ea98` (`git log d930ea98..HEAD -- hdl` empty); the driver-to-mover contract in `mbx.c:480-584` and `plat/mbx_dma.h`; `ctrl_loop.c` pass classes and static asserts; the `d6252b84` merge's combined diff (generated docs only) | R712-6 | `e7e2b7444a9859b058deff0d9edb575f2fb1946f` |
| Robustness | UNCLEAN (F2 MINOR) | The mover's ERR path through `mbx_tx_begin`/`commit`, `fan_out` and `fan_end`, probed (`receipts/probe_dma_sticky_err.txt`); the SRP retained retry's give-up; the pool link under a cut free list, probed (`receipts/probe_pool_*`); the fan-out's resume after FULL | R712-6 | `e7e2b7444a9859b058deff0d9edb575f2fb1946f` |
| Tests | UNCLEAN (F1 MINOR, F2 MINOR) | `selftest_answers.py`, the round 27 mutants in `selftest_mutants.py:442-469` (run: 14 of 14 caught); `load_grade.controls` and `flip_grade.controls` (run, 23/23 and 6/6); `test_mbx_dma_driver.cpp` (no test of a word-loop record after ERR); `aecp_fan_mutants.py`, `srp_compare_mutants.py`, `srp_retry_mutants.py`; the author's sweep and workflow receipts | R712-6 | `e7e2b7444a9859b058deff0d9edb575f2fb1946f` |
| Docs | UNCLEAN (F3 MINOR; RESIDUE-1 and RESIDUE-2 do not leave it unclean) | `SPLIT_CONTROL_MEMORY.md` section 13 round 27 text (`:2136-2140`) against the receipts; `ctrl_service_budget/README.md`'s flip and #882 sections against the code; the PR body against the head; FR_NFR.md 3.4.1 | R712-6 | `e7e2b7444a9859b058deff0d9edb575f2fb1946f` |

## Real limits

- **The full harness self-test.** I did not re-run `run.py --self-test` to completion; it went past the foreground limit (`receipts/harness_selftest.log`, rc 124 at 590 s). I ran the round 27 subset (above) and rely on the author's `lane/harness_selftest.log.tail` for the rest.
- **The full host firmware suite and the mutant campaigns.** I did not re-run them. A whole-suite attempt hit the same limit with no output (`receipts/probe_pool_link_cut.log`). My firmware evidence is the targeted arms (port, lwSRP, srp at 1 and 2 interfaces, unit) plus the author's published receipts.
- **No CPU budget harness simulation.** I did not run any harness simulation (no LiteX build). The row and cost figures are the author's receipts, which I checked against the gate's own output.
- **Physical calibration.** NOT RUN. Field skips are not hardware proof.
- **Hosted checks at this exact head carry no code verdict.**
  - `docs-gates-0` failed at "Install diagram gate dependencies" on a DNS failure resolving the runner's apt mirror (`receipts/hosted_docs_gates_0_failed_step.txt`).
  - The rest were cancelled by fail-fast, or failed in aggregator steps ("Require every gate exactly once").
  - So `rtl-fast`, `verilator-suites` and `yosys-portability` have no exact-head evidence.
- **No manager source bank** runs at this head, and I claim none.

## Pending manager duties

- Hosted and act acceptance at the exact head, after a re-run of the infrastructure-failed hosted workflows.
- The merge-turn current-dev candidate build against live dev `fa6c094b`, with the builder and native banks.
- A decision on F1 (which column the 1x1/1if merge gate reads).
- Acceptance of the round 27 deviation D2, which the brief records as accepted.
- Opening the flip-gate issue: #890 is open.
- Closing #882 (S4).
- The owner memo the round 27 tripwire requires.
- Carrying RESIDUE-1 and RESIDUE-2 to the residue checklist.
- #891 (14-bit AEM command_type at `aecp.c:428`) is noted as found and out of scope: the mask predates this PR (`a008ea92`, an ancestor of `1d6bf555`).

## Probe hygiene

Probes ran only in a scratch copy, `scratch/pool-probe`. Its plants are reverted, and it is never published.

In the review clone:
- I removed only the `__pycache__` directories my runs had created.
- After the probes the clone matches `e7e2b744`: tree `66cc0030`, index tree equal, 0 blob byte mismatches, 0 mode mismatches, no flagged index entries, no untracked or ignored files (`receipts/restore_verify.txt`).
- All five checked-out gitlinks are at their pins and clean. `external` is not initialised in the clone, as at the start.

R712-6 FINISHED
