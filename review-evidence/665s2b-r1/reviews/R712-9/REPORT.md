[R712] NEGATIVE - exact head 325514224bcc356a6b43843f1003c2323f09de25

# R712-9: external cleared-context delta review of PR #810 (#665 Mark II split, stage S2b), round 30

- **Head.** `325514224bcc356a6b43843f1003c2323f09de25`, tree `a3ca67b9b69d9de4ef9da684e56082c4a05d3bae`.
- **Delta.** From round 29's `b2d39235` (R711-8 and R712-8, both NEGATIVE) to this head.
- **Public start.** #810 issuecomment-6850243281.

## Verdict

**NEGATIVE, on two MINOR findings.** Both are in the Docs lens. There is no BLOCKER and no MAJOR. The Conformance, RTL, Robustness and Tests lenses are covered clean at this head.

- **R712-9-F1 (MINOR, Docs).** The sync merge `32551422` kept this branch's side of `SPLIT_CONTROL_MEMORY.md` over `dev-soft-core`'s correction `6eacd76d`. At `:455` the document therefore still names a "tightest point" of 288 B of `rom`. Its own table at `:450` gives a smaller margin: 16 B of `sram` at the platform's 8x8/2if.
- **R712-9-F2 (MINOR, Docs).** Section 13 `:2322` states the least row margins "at this head". The new `:2330` bullet points to them as round 30's ("the rows' least above"). They are round 29's figures, and this head's own round-30 receipts contradict both arm-A figures: 8x8/2if has an AECP record at 8.162 ms of margin, not 8.973, and 1x1/1if one at 9.992 ms, not 11.006.

Everything the round's rulings asked of code, gates and stated costs checks out against the receipts and against my own probes:
- **The mover fix.** It tracks the CPU's request to `KL_mbx`'s answer, and the new bench case fails on the old pairing.
- **Stated costs and the retry search.** The stated costs hold every leg's tally. The retry search holds 22 ms at 185 us and fails at 186.
- **The two gates.** The load gate holds 1x1/1if at 0.501, and the ledger gate catches its 7 plants.
- **The merges.** Both resolve their conflicts from the composed tree, and neither hides a protocol or mailbox-contract change.

## How this round was reviewed

1. **Authority, read first.**
   - AGENTS.md and the CONTRIBUTING.md bar.
   - The ruling on round 29 (#665 issuecomment-6828629878, items 1 to 6).
   - The three STOP rulings: 6831583372, 6835550732 and 6842347916.
   - The owner decisions 6824896581 (option A: platform 60.0 with a 60.5 cap, fixture 58.0 with a 58.5 cap) and 6845315282 (8x8 is a must, 2if optional).
   - The REVIEW READY, 6848807388.
   - Copies of all of these are in `receipts/gh/`.
2. **The delta.** I read it in three parts:
   - `b2d39235..70e30d7b`: items 1 to 3, 21 files.
   - The merge `187eeed8` and the merge `32551422`, each as a re-merge diff against the automatic merge.
   - `187eeed8..5bea2597`: the three STOP rulings, 26 files.
3. **Prior findings.** I read round 29's findings only after this pass.
4. **Evidence.**
   - The author's packet `review-evidence/665s2b-r1/author-r30` at archive `8d591986`: all 820 files verify against `MANIFEST.json`'s published sha256, with none missing, none differing and none unlisted.
   - Its `final-5bea2597` receipts apply to this head byte for byte. `git rev-parse 5bea2597^{tree}` = `HEAD^{tree}` = `a3ca67b9`, and the head merge's tree is its first parent's.
5. **My own probes.** Each probe ran on a `git archive` copy under the packet's scratch directory. Their receipts are in `receipts/`, their recipe in `scripts/r712-9-probes.sh`. The clone was left at the head's bytes (`receipts/clone-integrity-after.txt`).

## The seven questions

### (1) Round-29 findings at this head

| Finding | Status | Evidence at this head |
|---|---|---|
| R712-8-F1 = R711-8 F1 (MINOR): the composed tree refuses its own platform 8x8/2if image | **Closed** | See below. |
| R712-8-F2 = R711-8 F2 (MINOR): the SRP comparison cut's control escapes | **Closed** | See below. |
| R712-8 S1 = R711-8 S1: rule windows off SRP's 2 ms grid | Taken | `rows_grade.py:346` `rule_windows` adds each solved row's W and R4's edge at ±1 us. `probe_r712_rules`/`probe_r711_rules` rc 0; the "W less two records" plant is refused. |
| R712-8 S2: full completion queue, last frame committed before REFUSED | Taken | `test_mbx_dma_driver.cpp:443` T7, plant `mbx_dma_mutants.py:62` caught (control mutants 698/698, `probe_r712_fan`). |
| R712-8 S3, S4 | Moved by ruling to #894 | Not this lane's; nothing to check here. |
| R712-8 S5: `--check` refuses swapped columns | Taken | `load_grade.py:348` `unbound()` is in `findings()`. `binding_controls` (`:515`) plants a swap, a dropped column and an equal copy. `--selftest` 25 of 25 (my run, `receipts/load-selftest-head.log`). |
| R712-8 S6: publication | Manager | The `author-r30` index verifies (above). |
| R712-8 S7: expiry row names the pin move's kill through `also` | Taken | `acmp_mutants.py:784`. |
| R711-8 S2 (RETAINED_ROWS reading) | Unchanged by ruling item 5 | Still published as an open risk. |
| R711-8 S4 = R711-7 S2 (lost notice re-sent under a persistent mover ERR); F-HOOKS | Moved by ruling item 6 | #900 and #899 are open. |
| R712-8 RES-1 (live PR body is round 28's) | **Retained** | This round's RES-1. |

**R712-8-F1 = R711-8 F1, closed.**
- `ctrl_memory.py:251-266` holds `platform-8x8-two-interfaces` at 60.0, keyed `nvm_stage` 13,594 and `ctrl_plat` 20,288. It cites the owner decision, with refusal at 60.5. The size fixture is at 58.5 per STOP-1.
- `ctrl_memory_ledger.py:49-64` holds the same, with arms at 59.0 and 60.5.
- Section 5 (`:264-272`) and section 3 (`:137-143`) state the decision with its link. No "until a ruling" or "56 at every point" text is left.
- The new gate `plat_ledger.py` links the platform image at all four points with each point's override. At this head it plans 39.5 / 43.0 / 53.0 / 59.5 against 56 / 56 / 56 / 60.0, all PASS, and its self-test reports "7 of 7 as required": `stale-key`, `past-its-tiles`, `stale-key-past-its-tiles`, `stale-record`, `budget-under-a-point`, `override-not-taken`, `override-unlinked` (`final-5bea2597/lane/plat_ledger.log:23-30`).

**R712-8-F2 = R711-8 F2, closed.**
- `run.py:593` `reference_run` and `:623` `reference_verdict` hold the control to this image's own unplanted run of `notice-every-2`, by `poll_items.REFERENCE_MARGIN_PERCENT = 5` (`:137`).
- At this head it is caught: 34,551 planted against 30,989 unplanted, 11.5 % dearer, with 0 refusals (`final-5bea2597/harness/controls/ctl-srp-compared-by-memcmp-5bea2597.log`).
- Six self-test mutants hold the mechanism (`selftest_mutants.py`): no margin, its own run, refusals ignored, the wrong variant, the planted build's place, and held to the stated cost.
- README `:1424-1428` and section 13 `:2281` state it, and both are true at this head.
- No stated cost was lowered. My re-run of the table derivation against the head reports every table "unchanged" (`receipts/tables30-rerun-at-head.txt`).

### (2) Both merges

**`187eeed8` (PR #892's round-4 head `8bc1dfc0`, carrying `dev-soft-core` `0fb66211`).** The re-merge diff is in `receipts/merge-187eeed8-remerge-diff.txt`. These are its resolutions:

- **Code: `nvm_store.c` `nvm_mark`.** This branch's `id` parameter now goes through `dev-soft-core`'s `nvm_open_set(&nvm.dirty, id)`. Both sides' behaviour is kept. The matching `nvm_mutants.py` arm is retargeted to the merged text.
- **Code: `ctrl_split.ld` and `ctrl_split_hot.txt`.** Both drop `nvm_any`, a change outside any conflict. It is justified and documented: the KLJ3 count is inlined, so a hot name with no section refuses the link (§5 `:467`).
- **`coverage.ratchet`.** The figures are re-measured on the merged tree. `fw_coverage.py --check` passes over 39 files.
- **`ctrl_memory.py`, `ctrl_memory_ledger.py` and `test_ctrl_memory.py`.**
  - `dev-soft-core`'s KLJ3 stage key (13,594) is kept with this branch's `ctrl_plat` (20,288) and the owner's 60.0.
  - `dev-soft-core`'s `ctrl_memory_ooc.py` sentence is kept.
- **`split_soc.py`.** The docstring is merged from both sides.
- **Docs.** Each resolution follows the composed tree:
  - No `main_ram`, from `dev-soft-core`, with this branch's uncached `spiflash`.
  - The NVM README's blank-check step at 128 bytes, which is the head's `NVM_READ_BYTES = NVM_FLASH_PAGE / 2` (`nvm_store.h:93`), not `dev-soft-core`'s 256.
  - The harness README keeps this branch's `slow-adp-*` control text, and `slow-adp-shutdown` is still documented there (`:1447-1448`).
- **No contract change.** The merge adds no protocol or mailbox-contract change. `gen_mailbox` and its self-test pass, and so do the census and the split CDC (`final-5bea2597/lane`, workflow logs).

**`32551422` (`dev-soft-core` `e5f88a8e`).**
- `e5f88a8e`'s only content over the merge base `8bc1dfc0` is `6eacd76d`: two lines in `SPLIT_CONTROL_MEMORY.md` and two in the harness README.
- The resolution keeps this branch's side of all four lines, and the merged tree equals `5bea2597`'s, as claimed.
- **The harness README lines.** This branch's text ("58.5 RAMB36", `:49` and `:247`) is true at this head, so nothing is lost.
- **The `SPLIT_CONTROL_MEMORY.md` lines.** `dev-soft-core`'s correction of the margin statement is dropped, and the kept text is false. That is **R712-9-F1**.

### (3) The record mover fix

**The rule.** `KL_mbx.sv:1424` answers `(host_req_i && !reg_rd_w) || rd_q_r`, so a register read is answered two cycles after its request and anything else one. `KL_mbx_wb` pulses `host_req_o` once and then holds `busy_r` until the answer. Against that port:
- `cpu_wait_r <= cpu_issue_w || (cpu_wait_r && !host_ack_i)` (`KL_mbx_dma.sv:407`) holds from the issue to the answer for any latency. No second latency is hard-coded.
- `cpu_ack_o = host_ack_i && cpu_wait_r` (`:240`) routes the answer to the CPU.
- The mover's own requests, ring reads and beats, are gated on `!cpu_wait_r`, including the answer's cycle (`:200-201`, `:212`, `:271`). So the mover never issues while a CPU request is in flight, and never in its answer cycle.

**Ordering and reset.**
- A start in the cycle of a CPU issue is held off until the answer, and the mover then moves its own bytes.
- `pend_r` and `cpu_wait_r` are exclusive: the CPU cannot pulse while it waits.
- `cpu_wait_r` resets to 0.
- CDC is unaffected: the mover is a single clock domain on `clk_i`.

**Bench, plants and probes.**
- The bench answers as `KL_mbx` does as merged (`dma_main.cpp:268`). It checks that no request reaches the port while one awaits its answer, the answer's cycle included (`:251`). D11 (`:665`) covers a register read alone, held behind a transfer, and in the cycle a transfer starts, in both directions.
- My run at this head: 520,041 checks, 0 failures (`receipts/run-dma-head.log`), the same count as the author's sweep (`suites-1/mbx.log:39`).
- 24 of 24 plants are caught at `--jobs 16` (`receipts/dma-mutants-head.log`). Among them, `cpu-answer-one-cycle` restores exactly the old pairing, `cpu_wait_r <= cpu_issue_w`.
- **My own falsification.** I built the pre-fix `KL_mbx_dma.sv` from `187eeed8` against the head's bench. It fails 40 checks: D11 ×9, D4 ×22, D10 ×8 and D8 ×1, the CPU's register read never answered (`receipts/run-dma-old-rtl-new-bench.log`).

**Gate receipts at this tree (`final-5bea2597/workflows`).**
- Lint: the ratcheted whole-tree gate is at 89 ≤ 89.
- CDC: `split_cdc_check.py --selftest` passes, 13 checks and 0 failures.
- Yosys elaboration: 3 of 3 integration-heavy tops pass. The portability shard has `KL_mbx_dma` as PASS with 2,295 cells (`rtl__yosys-shards-3-4__ci_step_12.log:34`).
- The mailbox suite passes, 12 of 12 mbx mutants.

**Area.** `synth_xilinx` of the mover alone gives 704 → 704 flops and 484 → 487 LUTs (`rtl-fix/area/SUMMARY.txt`). This is within "its own few flops", and no route was run.

**The split boot gate.** It passes at 1x1/1if, 8x8/1if and 8x8/2if, with 3 of 3 plants and 8 of 8 placement and 6 of 6 native controls (`final-5bea2597/lane/boot_*.log`).
- At 8x8/2if it links with the platform's override (`boot_soc.py:73`, `run.py` `--ledgered-point`).
- At `a4faefd4`, before the fix, it fails at 1x1 with "mailbox contract mismatch; entity disabled" (`resume-mover-ack/boot-a4faefd4-1x1.log:18`). So the gate can fail for the defect.

### (4) The stated costs

**Trigger 1.** The author's tally (`ruling3/trigger1-rounds-by-n-k.txt`, `tools/tally_rounds.py`) takes every round through the harness's own parse, `round_grade.rounds`, by n and k.
- I re-derived the dearest rows' arithmetic (cycles / 100 − 365n − 34k): GN8 n=0 k=2 gives 248.16 − 68 = 180.16 us; k=4 gives 304.73 − 136 = 168.73; n=1 k=0 gives 402.89 − 365 = 37.89.
- At 1x1, GN1 n=0 k=1 gives 92.62 − 34 = 58.62 against 85.
- No leg's implied cold cost is over 183.1 us at 8x8/2if, nor over 85 us at 1x1/1if.
- The fresh-build F-legs give the same tally (`trigger2-rounds-fresh-8x8.txt`).
- k=0 and k=1 rounds stay at or under 81.41 us, which is the case the ruling's rationale asked about.

**Trigger 2.**
- **Fresh 8x8 build (`6c284a97`).** No firmware-stated round or pass given whole is over its cost there.
- **Polls base.** The STATED lines on that build are all grader-table items: a pass's polls base of at most 30,659 cycles, the figure the third STOP already disclosed.
- **Rebuild item.** The other STATED line is GA8's rebuild item of 65,390 cycles, which the ruling names for restatement.
- **At this head.** Those items are restated (325 and 690 us), and every regrade of all six legs prints no STATED line and 0 refusals, each rc 0 (`final-5bea2597/harness/X-*-regrade.log`).
- **Byte-compares.** Each leg's image ELF and `objcopy -O binary` and a sample group log are byte-identical to the measured build.

**Trigger 3, the retry search.**
- I ran `ctrl_retry_search.py` at this head and it passes: at 2if the first notice is at 22 ms and the last at 62 ms, at 1if at 16 / 22 ms (`receipts/retry-search-head.txt`).
- On a copy with `AECP_ROUND_COLD_US` 186 at 2if it fails: "the first notice at 2 interface(s): 28 ms over AECP_QUEUED_FIRST_MS" (`receipts/retry-search-probe-cold-186.txt`).
- The arithmetic 185 + 5×34 + 1,215 + 365 + 65 = 2,000 checks.
- `AECP_QUEUED_FIRST_MS`, `FIRST_ALLOWED_MS` and `AECP_ATTEMPT_US` are unchanged in the delta.

**The firmware constants.**
- `CTRL_LOOP_BUILD_PASS_US` 1,010 and `CTRL_LOOP_BUILD_ONE_PASS_US` 430 at 1x1 (`ctrl_loop.h:270-271`) are the rule's figures from 96,033 and 40,700 cycles.
- The 1x1 image is byte-identical before and after (`ruling3/S-GA1-compare.txt`), so they are header-only, as the ruling said.

**The margin exception.** It is stated, with its expiry at the 8x8/2if flip and #890's 176.1 us, in all three places: `aecp_mbx.h:21-27`, `FR_NFR.md` 3.4.1 `:372-374` and `SPLIT_CONTROL_MEMORY.md:2178-2180`. The figures check: 185 / 180.16 = 1.027, and 176.1 × 1.05 = 184.9.

**`test_aecp.cpp:2436`.** The firm cap's test now leaves room for one notice past the cap. This strengthens it: `retry-firm-uncapped` escaped at `6c284a97` and is caught with the change (`ruling3/aecp-mutants-shard2-*.txt`, workflow log `firmware-aecp-mutants`).

### (5) The 1x1/1if load gate and the restated tables

**The gate.** I ran `load_grade.py --check` at this head and it passes. It holds 1x1/1if at 0.501 at the pin and 0.499 with tsn-c-stack#32, against 0.70, and its output is byte-identical to the author's receipt (`receipts/load-check-head.log`). `--selftest` refuses 25 of 25.

**The tables.**
- I re-ran the author's derivation `tables30.py` against the head's committed tables, on a copy of the round's tallies (`ruling3/costs/G1`, `G8`). Every table comes out unchanged.
- The head's `load_grade.STATED_US`, `STATED_US_DONOR` and `poll_grade.STATED_US` (`poll_grade.py:63`) are therefore the fixed point of every leg's tally under the stated rule. A few spot checks:

  | Item | Most measured, cycles | Stated, us |
  |---|---:|---:|
  | Polls base, 1x1/1if | 19,159 | 205 |
  | Polls base, 8x8/2if | 30,659 | 325 |
  | Walk | 3,026 | 35 |
  | Rebuild | 65,390 | 690 |
  | Build, 8x8/2if | 176,761 | 1,860, under the stated 1,995 |
  | Build of one, 8x8/2if | 108,478 | 1,140, under the stated 1,215 |

- `poll_grade`'s ACMP item at 1x1 is 120 while the donor column's is 125. That follows each table's documented rule: `poll_grade` is restated only when a measured instance is over it.

### (6) The ledger gate and the four cost controls

**`plat_ledger.py --self-test`.** See (1): 4 of 4 points pass, and 7 of 7 controls are as required.

**The four cost controls.** All four are caught at this tree (`final-5bea2597/harness/controls`, each rc 0):

| Control | Caught on | Measured | Against |
|---|---|---:|---:|
| `notice-fan-out-as-it-was` | an AECP item | – | – |
| `polls-rebuild-in-the-base` | a polls base | – | – |
| `polls-rebuild-twice` | a rebuild item | – | – |
| `srp-compared-by-memcmp` | its own unplanted run | 34,551 | 30,989 |

On the fresh 8x8 build (`6c284a97`) the first three measured 31,933 against 27,000, 74,295 against 28,000 (32,500 restated) and 109,171 against 63,000 (69,000 restated), as section 13 states.

### (7) The full pass at the final head

- **Clean clones.** The clones were at `5bea2597` with 0 changed paths (`lane/clone-*.log`), and every workflow job's tree-after is clean.
- **Workflows.** `verify-table.md` has 139 steps at rc 0 and 226 NOT RUN, each with its reason, and none bad.
- **Lane gates.** All are rc 0 except the three flip checks, which exit 1 by design.
- **Sweep.** It has 65 suite logs, with no `failures: [1-9]`, `RESULT: FAIL` or `ESCAPED` in any of them.
- **Harness.** The six legs and four controls are rc 0.
- **Hosted checks.** At the exact head, 16 hosted checks have succeeded, 1 was skipped and 30 are queued or in progress (`receipts/gh/hosted-checks-325514224b.tsv`). These belong to the manager.

## Findings

### R712-9-F1 - MINOR - Docs - `docs/design/SPLIT_CONTROL_MEMORY.md:455` (and `:442`) - the sync merge `32551422` drops `dev-soft-core`'s correction of the pin move's smallest margins and keeps a false "tightest point"

**Authority and evidence**
- The brief for this round: "both merges: every conflict resolved from the composed tree, no side's behaviour dropped".
- `dev-soft-core` `6eacd76d` (in `e5f88a8e`) replaced "The tightest point is now the platform's 1x1 with two interfaces, 288 B of `rom` before its next granule" with "The smallest margins at the merge are 288 B of `rom`, at the platform's 1x1 with two interfaces, and 16 B of `sram`, at the platform's 8x8 with two interfaces, whose next granule would plan 59.5 against the 59.0 its override holds."
- It also named #874 and #880 beside #889 and #888 in the `0fb66211` sentence.
- The merge `32551422` resolved both lines to this branch's side (`receipts/merge-32551422-remerge-diff.txt`).
- This head's `:455` still says "its tightest point is the platform's 1x1 with two interfaces, 288 B of `rom` before its next granule".
- The document's own table at `:450` disproves it. The platform's 8x8/2if `sram` need is 114,672 B, and `GRANULE_BYTES` is 2,048 (`ctrl_memory.py:51`), so ceil(114,672 / 2,048) × 2,048 − 114,672 = 16 B. That is smaller than the 288 B of `rom` at 1x1/2if (112,352 B in 112,640).

**Impact**
- The authoritative ledger document misstates which margin was smallest at the pin move's merge, and by a factor of 18.
- Once this branch lands in `dev-soft-core`, its resolution replaces the corrected text there. A fix `dev-soft-core` already took is silently reverted.

**Required outcome**
- `:455` states both regions' smallest margins at that merge, as `e5f88a8e` does: 288 B of `rom` at the platform's 1x1/2if, and 16 B of `sram` at the platform's 8x8/2if.
- `:442` names what `0fb66211` carries as `dev-soft-core` does: #874, #880 (with KLJ3, #823), #889 and #888.
- Or a maintainer rules the paragraph's wording otherwise.

**Verification**
- `git diff e5f88a8e <fix> -- docs/design/SPLIT_CONTROL_MEMORY.md` shows no loss of `6eacd76d`'s two statements.
- The 16 B follows from `:450` and `GRANULE_BYTES`.

### R712-9-F2 - MINOR - Docs - `docs/design/SPLIT_CONTROL_MEMORY.md:2322`, `:2330` - the least row margins "at this head" are round 29's, and this head's round-30 receipts contradict them

**Authority and evidence**
- The ruling on the third STOP (#665 issuecomment-6842347916): re-grade on fresh builds at this head's image, then restate.
- `:2322` says "with the least margin at this head an AECP record's: 6.246 ms in the `answering-every-port` arm ... and 8.973 ms in arm A (11.027 ms, ... a save's verify window opened at the age limit) at 8x8/2if, and at 1x1/1if 9.080 ms in the arm ... and 11.006 ms in arm A (round 29's legs, on the composed image; ...)".
- The delta rewrote `:2330` to "The margins at this head (round 30's legs, ...): the rows' least above".
- 8.973 and 11.006 are exactly round 29's `AGED` least margins (`author-r29/receipts/legs/GA8-regrade2.log:10`, `GA1-regrade2.log:10`).
- At this head, round 30's regrades of the same arm read:
  - 8x8/2if: "the least margin 8.162 ms, backlog-adp@program-aged2-7.service.aecp.last.if1 at 11.838 ms" (`final-5bea2597/harness/X-GA8-regrade.log:10`; the same in `ruling3/legs-head-F-GA8.txt:10`).
  - 1x1/1if: "the least margin 9.992 ms, backlog-adp@verify-aged2-5.service.aecp.last.if0 at 10.008 ms" (`X-GA1-regrade.log:10`).
- So at this head arm A's least AECP-record margin is at most 8.162 ms (8x8/2if) and at most 9.992 ms (1x1/1if). Both are smaller than the figures stated for "this head".
- The answering-every-port arm's figures (6.246 and 9.080 ms) are not re-derivable from any round-30 receipt.

**Impact**
- The section that states what holds at the merge candidate overstates the least margin of an AECP record by 0.81 ms at 8x8/2if and 1.01 ms at 1x1/1if.
- The new `:2330` cites these figures as round 30's.
- #894's tier work and the 8x8/2if flip read these margins.

**Required outcome**
- `:2322` states this head's least margins from round 30's legs: both arms at both points, each with its group and instance. Where an arm's figure is not re-derived, it says so, and does not call round 29's figures "at this head".
- `:2330` points only at figures from round 30's legs.

**Verification**
- Each margin in `:2322` matches a round-30 receipt at a head whose tree is `a3ca67b9`: the `AGED` lines of `X-GA8-regrade.log` and `X-GA1-regrade.log`, and the published arm figures of the round-30 GN legs.

### Suggestions (optional, do not affect coverage)

- **S1 (Robustness, RTL), `KL_mbx_dma.sv:185-196`.** The mover's own requests still take their answer the cycle after: `hold_r` gives the ring's word one cycle. That is `KL_mbx`'s rule for ring reads and writes, and the new comment states it. But `ring_base_i` is a free CSR (`milan_soc.CtrlMailboxDma.cfg`). A base programmed into the register space would make each receive word stale register data, with nothing refusing it. Refusing such a start, or stating that the driver owes it, would close it. This is pre-existing and not part of the delta's defect.
- **S2 (Tests), `boot_soc.py:73` and `plat_ledger.py:61`.** The platform image's override per point is stated twice: `PLATFORM_LEDGERED` and `POINTS`. One should be derived from the other, or a check should hold them equal, so the boot gate and the ledger gate cannot link different overrides.
- **S3 (Docs, evidence), `final-5bea2597/harness/X-*-compare.txt`.** Every byte-compare lists five differing build inputs: `gateware/sim.v`, both runtime archives, `flash_port.json` and `tree:firmware`. The images and samples are identical, so nothing is lost. But the receipts do not say why `sim.v` and `flash_port.json` differ, which I expect is embedded build paths. One line saying so would let a cold reader trust the compare.
- **S4 (Docs), `tb/verilator/ctrl_split_boot/README.md:125`.** "A gate at every sync" and `plat_ledger.py` are lane gates that no workflow or script runs. Their only trigger is this README and the brief. Naming them in the lane's gate list, the `lane_gates` recipe the manager runs, would keep them from being skipped at a later sync.

### Residue (wording only)

- **RES-1 (live PR #810 body), retained from R712-8 RES-1.** The published body is still round 28's text: it opens `[A683zm]`, its Status reads "round 28's seven items", and it has no round-29 or round-30 section (`receipts/gh/pr810-body-live.md`).
  - **Exact fix:** publish `review-evidence/665s2b-r1/author-r30/PR-BODY.md` (archive `8d591986`) as the PR body.
- **Comment rule.** No added source comment in the delta carries a lane label, round label, reviewer ID or issue-comment ID.
  - "owed to S14", "lane S14" and two ruling IDs appear only inside `ctrl_memory.LEDGERED`'s reason strings.
  - Those strings are data the ruling asked for ("stated as ROM debt owed to S14"), on lines whose text was already there (tracked by #746).

## Reviewer-owned ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | The round-29 ruling's items 1-6 and STOP rulings 1-3 against: `ctrl_memory.py:251-266`, `ctrl_memory_ledger.py:49-64`, `aecp_mbx.h:21-29`, `ctrl_loop.h:270-271`, `FR_NFR.md:372-374`, `SPLIT_CONTROL_MEMORY.md:137-143,264-272,2178-2180`; my retry search at the head and at cold 186; my load gate run (0.501 ≤ 0.70); trigger 1-4 receipts; the owner decisions 6824896581 and 6845315282 (8x8/1if boot and ledger points present) | R712-9 | `325514224bcc356a6b43843f1003c2323f09de25` |
| RTL | CLEAN | `KL_mbx_dma.sv:158,200-213,240,271,397-418` against `KL_mbx.sv:1405-1439` and `KL_mbx_wb.sv`; `milan_soc.py:3053-3110`; the re-merge diff of `187eeed8` (`nvm_store.c`, the link script); area `rtl-fix/area/SUMMARY.txt`; lint, CDC and Yosys receipts in `final-5bea2597/workflows/logs` | R712-9 | `325514224bcc356a6b43843f1003c2323f09de25` |
| Robustness | CLEAN | Reset, start-in-the-issue-cycle and held-request ordering in `KL_mbx_dma.sv` (D8, D11); `flash.hpp:116` span refusal (my plant `receipts/flash-test-plant-fixed-span.log`); `save_window.py:80` refusing an ambiguous header; `run.py:593` refusing a mismatched reference build; `plat_ledger.py` controls. S1 is optional. | R712-9 | `325514224bcc356a6b43843f1003c2323f09de25` |
| Tests | CLEAN | `dma_main.cpp:251,268,665` and `dma_mutants.py:94-104` (my 520,041 checks; 24/24; the old RTL failing 40); `flash_test.cpp` (my 19/19); `test_aecp.cpp:2436` with `retry-firm-uncapped` caught; `test_mbx_dma_driver.cpp:443` T7 and its plant; `selftest_mutants.py` reference arms; `load_grade.py:348,515`; `rows_grade.py:346`; `plat_ledger.py:218` controls; boot plants; my `tables30.py` fixed-point re-run | R712-9 | `325514224bcc356a6b43843f1003c2323f09de25` |
| Docs | **UNCLEAN** | `SPLIT_CONTROL_MEMORY.md` §3, §5, §13 (`:442,455,2281,2299,2322,2330`), `MAILBOX_SPLIT.md:304-312`, `FR_NFR.md` 3.4.1, the harness README (`:49,247,1415-1428`), the mbx README (`:27-43`), the split boot README (`:125-137`); live PR body. **R712-9-F1 and R712-9-F2 are open.** | R712-9 | `325514224bcc356a6b43843f1003c2323f09de25` |

## Real limits

- **No full leg run.** I re-ran no harness leg. The per-group logs behind the trigger-1 tally are not published, so I checked the tally's tool (`tools/tally_rounds.py`, the harness's own `round_grade.rounds`), its arithmetic, and its consistency with every head regrade (no STATED line, rc 0), not each round.
- **Helper exits.** `final-5bea2597/dispatch.txt` shows helper units exiting rc 1: GA1-h2, F-GA8-h1, F-GA8-h3 and F-GA8-h4. They are consistent with the then-unrestated rebuild item (`legs-head-F-GA8.txt`: "STATED adp-link ... 65,390", rc 1), but no per-helper receipt states their cause.
- **Not re-run by me.** The full sweep and the workflow jobs are the author's receipts, checked by spot reads. So are the boot gate and `plat_ledger.py`: they need the RV32 SDK and LiteX environment.
- **Timing.** No place-and-route was run for the mover; the area is from Yosys alone.
- **Hardware.** Physical calibration is NOT RUN, and field skips are not hardware proof.
- **Manager source bank.** No manager source bank was run at this head, and I claim none.

## Pending manager duties

- Publish this report and the packet's listed receipts.
- Publish `author-r30/PR-BODY.md` as PR #810's body (RES-1).
- Hosted and act acceptance of the exact head: 30 checks were still queued or in progress at review time.
- The candidate merge onto live `dev-soft-core` `b7d69295` and its builder and native banks. The source base is `e5f88a8e`.
- Route R712-9-F1 and R712-9-F2 to the author for one docs-only commit. After it, the Docs lens must be covered again at the new head.

## Publishable files

Every receipt is listed in `MANIFEST.sha256`, with paths relative to this packet. `scratch/` is not published.

R712-9 FINISHED
