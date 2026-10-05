[R500] POSITIVE - exact head d763fce6f3e48fa9c468aaa835653befb8382d06

# R500-4: internal cleared-context review of PR #669 (#665 lane F1), round 4

- **Head:** `d763fce6f3e48fa9c468aaa835653befb8382d06`, tree `554ad4cb05ffbf9d794813990a8dfb58ec44624d`. These are three one-line commits on `9412006b`: `f1cf5c08` (code and suite), `c2e33963` and `d763fce6` (module page).
- **Source base:** `fa450d301805881ad713b67521477bf042ddadfd`. Live dev is `28f9666f`, which the lane has already merged (`e2000ef9`).
- **Reconstructed from public state only, in this order:**
  1. AGENTS.md and CONTRIBUTING.md;
  2. docs/README.md;
  3. #665: the body, lane assignment 5993775541, round assignments 5996009284 and 5997929153 (decisions 1 and 2), and the round-4 assignment 5999350068;
  4. the executor's TAKEN and REVIEW READY comments for round 4 (5999489236, 6000120843);
  5. FASTCONNECT sections 6.2 and 7, and the shapes' `board.constraints.sys_clk_hz`;
  6. the diff `9412006b..d763fce6` inside `fa450d30..d763fce6`, the PR body at this head, the hosted checks at this head, and the evidence tree linked in the review start.
- **Order of reading:** prior review findings (R500-3, R501-3 and the round-1 and round-2 dispositions) were read only after my own pass over the delta.

All five lenses were applied, and no BLOCKER, MAJOR, MINOR or RESIDUE is open. Both round-3 MAJORs are resolved at this head:
- R501-3-F1: a refusal now stands only on two reads of the same bytes;
- R500-3-F1: the port now converts clocks exactly at every shipped shape's clock.

Two new SUGGESTIONs are recorded, and three earlier ones are retained.

## Findings at this head

| ID | Severity | Lenses | Title |
|---|---|---|---|
| R500-4-S1 | SUGGESTION | Tests | The RV32 arm's undefined-symbol rule admits the stack-protector symbols as if they were libgcc helpers |
| R500-4-S2 | SUGGESTION | Docs | The module page's exact-repeat limit gives "every boot read" as its example. Any two of a boot's reads that return the same wrong bytes are enough |
| R500-3-S1 (second half) | SUGGESTION, retained | Robustness, Docs | Whether to narrow the hold is still an owner question. The first half (state the permanent hold) is RESOLVED |
| R500-3-S2 | SUGGESTION, retained | Robustness | How HELD with changes outstanding maps onto FASTCONNECT 9.2's flags at integration |
| R500-1-S1 | SUGGESTION, retained | Tests | The lane gate still runs in no hosted workflow |

### R500-4-S1: SUGGESTION. Lens: Tests

**Artifact:** `sw/firmware/ctrl_nvm/test/nvm_rv32.py:71`, `stray = sorted(s for s in undefined - defined if s not in LIBC_OK and not s.startswith("__"))`, with `RV32_FLAGS` at `:26`.

**Evidence:**
- `receipts/probe_rv32_clock.log`: the pinned SDK compiler, with the arm's own flags, emits `__stack_chk_guard` and `__stack_chk_fail` as undefined symbols in all three objects. It does so because the compiler enables the stack protector by default.
- The arm passes them under its "libgcc helper" prefix rule. They are libc or SSP symbols, not libgcc.
- The 64-bit conversion added this round needs `__udivdi3`, `__umoddi3` and `__muldi3`. Those are real libgcc helpers.
- This predates round 4 (`nvm_klj2.c` shows the same symbols) and does not hide a heap or stdio symbol.

**Impact:** the arm's docstring says it "fails on any undefined symbol that is not a C-library memory function or a libgcc helper". That is broader than what it enforces. An image whose build keeps the protector on and supplies no guard would fail at link time, and this arm would not say so.

**Optional outcome:**
- Build the arm with `-fno-stack-protector`, as a bare-metal image normally is, or replace the prefix rule with an explicit libgcc allow-list;
- report the helpers the store needs.

**Verification:** the arm's undefined-symbol list at each shape names only the memory functions and the listed helpers.

### R500-4-S2: SUGGESTION. Lens: Docs

**Artifact:** `sw/firmware/ctrl_nvm/README.md:443-449`, and the matching "Known limitations" bullet in the PR body.

**Evidence:** `receipts/probe_mutants.log`, probe `model_repeats_first`. The fault model in a scratch copy was changed to XOR 8, then 16, then 8. Under the head's store, the third read agrees with the first, the refusal stands, and the next commit loses a saved value on a clean reboot (86 findings). This follows the stated rule that two reads of the same bytes are content. The page's first sentence, "Two reads of a slot that return the same bytes are taken as its content", is accurate. Its example ("the same way on every boot read") is narrower than the exposure.

**Optional outcome:** for example, "A fault that returns the same wrong bytes on any two of a boot's reads of a valid slot, without the port reporting it, therefore looks like a refusal." No code change is suggested: the rule is the one the round-4 assignment chose.

## Round-4 assignment (5999350068), graded item by item

### Item 1: a refusal stands only on two reads of the same bytes (R501-3-F1). RESOLVED.

**Code.** All references are to `sw/firmware/ctrl_nvm/nvm_store.c`.
- `:134-149` `struct nvm_read` and `nvm_take`: every port read of a slot read feeds its delivered bytes into a CRC-32 (init 0xffffffff) and adds them to the byte count. A failed port read adds nothing and gives UNREAD.
- `:156-195` `nvm_slot_read`: the digest covers exactly the bytes the verdict is judged on:
  - the 40 header bytes for a header verdict;
  - header plus container on the in-stage path;
  - header, every chunk, the trailer and the re-read stage on the streamed path.
- **Equal counts mean equal paths.**
  - The in-stage path reads 40 + img_len bytes, and the streamed path reads 40 + img_len + stage bytes. A streamed container has img_len above the stage size, so no streamed read can match the count of an in-stage read.
  - Within one path, equal counts therefore mean equal img_len, which means the same address sequence. Comparing digests is comparing the same bytes.
- `:208-217` `nvm_agrees`: a read agrees when any earlier read has the same verdict, digest and count. The comparison is pairwise against every earlier read, not only the previous one.
- `:228-247` `nvm_slot_check`:
  - OK stands on one read.
  - Any other verdict stands only on agreement.
  - A disagreeing read after the first is counted in `read_faults` (`:242-243`).
  - A port failure is counted and does not use up a judged slot (`:236-239`).
  - At most `NVM_READ_TRIES` = 3 reads (`nvm_store.h:72`), then `nvm_unread` (`:200-204`), which sets the `unread` bit. `nvm_store.c:455` then sets phase HELD.
  - The index `n` stays at or below `i`, which is below 3, so `seen[3]` is never overrun. The stack cost is 36 bytes.
- **CRC-32 claim.** The README claims (`:450-453`) that one- and two-bit differences and bursts of up to 32 bits are always detected. That holds for this polynomial at this length: Hamming distance at least 3 far beyond 106,048 bits (8x8). Because the digest is linear, two reads of equal count differ in digest exactly when their XOR leaves a non-zero remainder.

**Standing check.** `read_disagreement` (`test/nvm_checks_write.py:573`, using `_authority_case` at `:500`) runs on the flash-model port at every shape:
- the valid slot as A and as B, with the other blank;
- SEQ 1, 5, 0x80000000 and 0xFFFFFFFF;
- the fault at header byte 0 and at body offset 0x100;
- XOR 8/16 then clean: applied, `read_faults` = 1, COMPLETE, sequence + 1;
- XOR 8/16/32: UNREAD, HELD, BLANK, console refused, nothing erased or programmed;
- each case then goes through a change, a clean reboot, a commit and a clean reboot, comparing every saved value.

That is 32 cases per shape. The fault model's new `read-vary-at` (`host/nvm_fmodel.c:204-205`) is consumed only by reads that cover the byte.

**Planted defect.** `refusal_by_verdict` (`test/nvm_mutants.py:184`) is caught. My own run of it lists every finding (`receipts/probe_mutants.log`): 188 findings, of which 76 are lost or mismatched state on a reboot, spread evenly over all four SEQs (16 each). So the kill rests on lost saved values, not only on the fault counter. A reviewer variant that drops only the digest comparison (`agree_without_digest`) is also caught, with 188 findings.

**HELD is reported and cannot wedge silently.** `receipts/probe_held_report.log` covers 1x1 and 8x8, slot A and slot B. With three differing reads, then a change, 10 s of service, a console commit and 1 s more, each case shows:
- phase 10 (HELD), the matching `unread` bit, terminal BLANK, AECP released once;
- `read_faults` 2, `dirty` 1, `commit_refused` 1, 0 erases and 0 programs;
- 110,000 service steps taken, so the loop keeps running.

The module page (`README.md:206-209`) states that such a slot holds the writer on every boot.

### Item 2: exact conversion at every shape's clock (R500-3-F1). RESOLVED.

**Code.** References are to `plat/nvm_flash_litespi.c` unless stated.
- `:70` `LS_HZ` is the clock in 64 bits.
- `:75` `nvm_flash_litespi_call_ticks = (uint32_t)(LS_CALL_US * LS_HZ / 1000000u)` is exact. It is published at `plat/nvm_flash_litespi.h:18`.
- `:100` `ls_late` compares the wrap-safe 32-bit difference with it.
- `:259` `ls_now_us` returns whole seconds, plus the remainder times 10^6 divided by the clock:
  - the remainder is below the clock, so the product stays under 10^14;
  - the result equals floor(ticks x 10^6 / Hz) exactly, with no 64-bit overflow for any tick count.
- The whole-MHz static assertion and `LS_TICKS_PER_US` are gone. Both 100 MHz stand-ins (`host/stubs/generated/soc.h` and `test/rv32/generated/soc.h`) are deleted, and nothing in the tree still refers to them.

**Independent arithmetic** (`probes/probe_tick_math.c`, `receipts/probe_tick_math.log`): the head's expressions, copied verbatim (confirmed by fixed-string match), against 128-bit exact floor:
- 2,000,009 tick counts each, edges included, up to 2^64 - 1;
- clocks 83,333,000, 100,000,000, 83,333,333, 12,345,679 and 1,000,000;
- 0 mismatches;
- deadline 166,666 clocks at 83.333 MHz and 200,000 at 100 MHz; the truncating form gives 166,000;
- one counter wrap is 51,539,813 us at 83.333 MHz.

**Per-shape clock.**
- `test/nvm_bench.py:226` `sys_clock` takes the config's `sys_clk_hz` and holds it to the builder's emitted `--sys-clk-freq`, or to `milan_soc.py`'s 100e6 default (`sw/litex/milan_soc.py:3353`, `sw/builder/endstation_builder.py:4834-4835`).
- `soc_header` (`:185`) writes it.
- The host model's `timer0` counts that clock exactly (`host/litespi_model.c:224`).
- The RV32 arm compiles against the same `gen` directory.

**My runs** (`receipts/suite_*.log`, rc 0 each):
- `endstation_arty_current`, `_arty_4x4` and `_arty_8ch` print `clock=83333000 Hz` and `rv32 at 83333000 Hz`;
- both AX7101 shapes print 100000000;
- 42 checks per shape, 0 failed.

`receipts/probe_rv32_clock.log` compiles the port, the store and the codec for RV32I with `-Werror` at both clocks, all rc 0. That is R500-3-F1's verification.

**Checks.**
- `port_clock` (`test/nvm_checks_write.py:394`) asserts the built clock equals the config's and the deadline equals `LS_CALL_US * Hz // 10^6` (166,666 at the Arty shapes). Over 120 s, which spans at least two wraps, port time must match model time to 2 us.
- `time_base` places its window across the shape's own wrap (`:384`) and asserts the change lands inside it.

**Planted defect.** `ticks_per_us_truncated` (`test/nvm_mutants.py:352`) is graded at `endstation_arty_current` and is caught by `port_clock` and `time_base` (`receipts/selftest.log:80`, deadline 166,000 against 166,666). My own split variants are both caught (`receipts/probe_mutants.log`):
- deadline truncation alone fails `port_clock`;
- time-base truncation alone fails `port_clock` and 7 `time_base` assertions.

### Item 3: merge dev. Nothing to merge.

Dev is still `28f9666f`, already merged.

### R500-3-R1 (RESIDUE): RESOLVED.

`README.md:102-109` carries the exact replacement wording.

## Prior public findings: resolved or retained at this head

| Finding | Disposition at d763fce6 |
|---|---|
| R501-3-F1 MAJOR | RESOLVED (item 1 above) |
| R501-2-F1 MAJOR (retained at round 3 through R501-3-F1) | RESOLVED together with R501-3-F1. Signalled failures, silent flips, aliasing and now differing silent corruptions either use a clean read or HOLD the writer. `authority_unknown` and `read_disagreement` are green on all five shapes |
| R500-3-F1 MAJOR | RESOLVED (item 2 above) |
| R500-3-R1 RESIDUE | RESOLVED (exact wording applied) |
| R500-3-S1 SUGGESTION | First half RESOLVED (`README.md:206-209` and the PR body state the hold on every boot). Second half (the narrower hold) RETAINED for the owner |
| R500-3-S2 SUGGESTION | RETAINED. In HELD, `stale` is still 0 with `dirty` 1 (`receipts/probe_held_report.log`) |
| R500-1-S1 SUGGESTION | RETAINED. `test_ctrl_nvm.py` is still in no hosted workflow |
| R500-2-F1 to F4, R500-2-S1, R501-2-F2, R501-2-F3 | Resolved at round 3 by both round-3 reviews. The delta touches only the boot read loop, the port's clock and their tests. The 82-defect self-test, which keeps each of their planted defects, is green at this head (`receipts/selftest.log`) |
| R500-1-F1 to F6, R501-1-F1 to F4 | Resolved at round 2 and confirmed at round 3. There is no regression: their planted defects are still in the 82 and all are caught |

## Lens results at this head (clean-lens evidence)

```text
[R500] PASS Conformance — nvm_store.c:134-247, plat/nvm_flash_litespi.c:70-100,259, configs/endstation_*.yaml sys_clk_hz — round-4 items 1-2 against 5999350068 and decision 2 (5997929153): agreement by verdict+count+CRC-32 over every delivered byte, re-read within NVM_READ_TRIES, UNREAD->HELD; exact conversion at 83,333,000 and 100,000,000 Hz, deadline 166,666/200,000 clocks, no static assertion; every shape built and graded at its own clock (suite_*.log, probe_tick_math.log)
[R500] PASS RTL — no HDL in the lane diff; firmware architecture: nvm_store.c:228-247 loop bound and seen[] index, :455 HELD terminal phase; plat/nvm_flash_litespi.c:75,100,259 widths (no 64-bit overflow for any tick count, call_ticks fits 32 bits, wrap-safe 32-bit deadline difference); RV32I -Werror builds at both clocks (probe_rv32_clock.log); nvm_store.h and plat header contracts unchanged except the published const
[R500] PASS Robustness — read_disagreement 32 cases x 5 shapes; probe_held_report.log (HELD reported, loop alive 110,000 steps, console refused, no media effect, 1x1/8x8, A/B); interleaved port failure keeps the judged-read index (nvm_store.c:236-239); counter wrap at 51.5 s (time_base); powercut on every shape; model_repeats_first documents the any-pair rule (S2)
[R500] PASS Tests — selftest.log: 42 checks at 1x1 then 82/82 planted defects caught, ticks_per_us_truncated at 83,333,000 Hz; probe_mutants.log: refusal_by_verdict killed by 76 state-loss findings, agree_without_digest, deadline_only_truncated and timebase_only_truncated all caught; check_port_counts.log 42 = 29 both + 8 model + 5 LiteSPI, every check named by a defect; S1 is optional
[R500] PASS Docs — sw/firmware/ctrl_nvm/README.md diff 9412006b..d763fce6 (lines 13-15, 28, 70-109, 141-162, 206-209, 329-345, 353-416, 432-458) and PR body at this head checked against code and my runs (static-size table equals rv32 lines of suite_*.log; 2,189/2,190 us maxima; 42/29/8/5; 82 defects); docs/README.md:73 row current; gates rc 0 (receipts/gates/); S2 is optional
```

## Reviewer-owned completion ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #665 body, 5993775541, 5997929153 (decisions 1 and 2), 5999350068; FASTCONNECT 6.2 and 7; `nvm_store.c:134-247,455`; `plat/nvm_flash_litespi.c:32-100,259`; `configs/endstation_*.yaml` `sys_clk_hz`; `endstation_builder.py:4834-4835`; `milan_soc.py:3353`; `suite_*.log`; `probe_tick_math.log` | R500-4 | d763fce6f3e48fa9c468aaa835653befb8382d06 |
| RTL | CLEAN | No HDL in the lane diff (`git diff --stat fa450d30..d763fce6`; round-4 delta under `sw/firmware/ctrl_nvm/` only). Firmware architecture: boot read loop bound and index, HELD terminal phase, 64-bit widths and the wrap-safe deadline, `nvm_store.h:54,72,101-106`, `plat/nvm_flash_litespi.h:18`; RV32I builds at both clocks (`probe_rv32_clock.log`) | R500-4 | d763fce6f3e48fa9c468aaa835653befb8382d06 |
| Robustness | CLEAN | `read_disagreement` and `authority_unknown` on 5 shapes; `probe_held_report.log`; `probe_mutants.log` (`model_repeats_first`); `time_base` wrap at each shape's clock; `powercut` on every shape | R500-4 | d763fce6f3e48fa9c468aaa835653befb8382d06 |
| Tests | CLEAN (S1 optional) | `test/nvm_checks_write.py:384,394,500,573,739-753`, `test/nvm_mutants.py:184,352`, `test/nvm_bench.py:185,226`, `test/test_ctrl_nvm.py` self-test routing, `test/nvm_test.c` (`--clock`, summary), `host/litespi_model.c:224`, `host/nvm_fmodel.c:204`; `selftest.log` (82 of 82); `probe_mutants.log`; `check_port_counts.log` | R500-4 | d763fce6f3e48fa9c468aaa835653befb8382d06 |
| Docs | CLEAN (S2 optional) | `sw/firmware/ctrl_nvm/README.md` (whole round-4 diff), header comments in the four changed sources, PR body at this head, `docs/README.md:73`; `receipts/gates/` docs_check, check_em_dash (bases 28f9666f and fa450d30), gen_toc `--check` and `--verify-anchors`, check_doc_style, check_doc_paths, `git diff --check`, all rc 0 | R500-4 | d763fce6f3e48fa9c468aaa835653befb8382d06 |

## Executed evidence (all at d763fce6, all rc 0)

**Lane suite** (`scripts/run_lane_suite.sh`): one process per shape with `--require-rv32`, five `receipts/suite_*.log` files.
- 42 checks each, 0 failed.
- Longest call: 210 us nominal; 2,189 us stalled (2,190 us at `arty_4x4`).
- The RV32 text, bss, stage, payload and chunk sizes equal the module page's table row for row.

**Self-test** (`scripts/run_selftest.sh`, foreground): the 1x1 shape, then all planted defects. Result: "OK across 1 shape(s), 42 checks, and all 82 planted defects reddened". The background self-test arm of `run_lane_suite.sh` ended without writing a result, and this foreground re-run replaces it.

**Focused companion gates** (`scripts/run_gates.sh`, `receipts/gates/`):
- the shipping writer's host test with `--self-test`;
- `check_nvm_capture.py`;
- `check_nvm_record_space.py` and its `--self-test`;
- the C/C++ idiom, Python idiom, hygiene and bare-metal scope (`--check`) gates;
- `docs_check`, `check_doc_style`, `check_doc_paths`;
- `check_em_dash` against both bases, `gen_toc --check` and `--verify-anchors`;
- `git diff --check fa450d30..HEAD`.

**Reviewer probes** (`probes/`): `probe_tick_math.c`, `probe_mutants.py` (5 probes, all as expected), `probe_rv32_clock.py`, `probe_held_report.py`.

**Integrity** (`receipts/integrity_after_probes.log`):
- the clone is at the exact head and tree, with an empty `--ignored` porcelain;
- the index (mode, blob, path) digest equals the HEAD tree digest;
- the gitlinks are `gptp-processor` 5dce647a, `protocol-processor` ead80360, `third_party/verilog-axis` 48ff7a7e, each worktree at its gitlink and clean, and `external` uninitialised;
- probe-created bytecode caches were removed.

## Real limits

- Physical calibration NOT RUN. There was no hardware, no real power cut and no real flash. Field skips are not hardware proof.
- No image links the store yet (F0's switch is unmerged). The CPU time of a step is still unmeasured, including the two 64-bit divisions `ls_now_us` now makes per service step. On RV32 those are libgcc calls (`__udivdi3`, `__umoddi3`). The module page claims only a floor for CPU work, so no stated figure is contradicted.
- The host link model charges 0.64 us per byte (a 12.5 MHz request). `sw/litex/milan_soc.py:2699` and `:2711` note an effective clock of about 20.8 to 25 MHz. That makes the model conservative for the deadline. It is unchanged this round.
- The CRC-32 digest misses a disagreement with probability about 2^-32 outside the guaranteed classes. A fault that returns the same wrong bytes twice is read as content (stated, and see S2).
- Not run by this reviewer (forbidden or out of scope): the builder bank; the full parent, PP, gPTP and Yosys banks; act and hosted runs; `test_builder.py`.
- **Hosted contexts at this head** (`receipts/hosted_checks_snapshot.tsv`):
  - complete and successful: rtl-fast, changes, full-ci-gate, bdd-conformance, verilator-lint, docs-check-no-git, wire-accountability, yosys-elaboration, Yosys shards 0-3 and Verilator shard 3/5;
  - still in progress when sampled: docs-check, elaborate, and Verilator shards 0, 1, 2 and 4;
  - skipped: Physical gPTP.
- The public evidence tree linked in the review start (`38e93660`, `review-evidence/665f1-r1`) holds only round-1 (`215c3c0b`) author logs. I did not find a public receipt for the manager's source banks at this head; I relied on my own runs above.

## Pending manager duties

- Publish this packet. Reconcile with R501-4.
- Own hosted and act acceptance: wait for the in-progress hosted contexts at this head.
- Build and validate the final current-dev candidate (source base `fa450d30`, live dev `28f9666f` or its successor) at the merge turn.
- Publish, or point to, the head-specific source/builder/native bank receipts.
- Carry these as optional: R500-4-S1 and S2; R500-3-S1's narrower hold, for the owner; R500-3-S2, for integration; R500-1-S1, a hosted workflow for the lane gate.
- Carry the executor's raised items: the shipping writer's VD_REC/VD_LEN parity gap, and #671.

## Reproduction

```sh
scripts/run_lane_suite.sh <clone> <packet>          # five shapes
scripts/run_selftest.sh  <clone> <packet>           # 1x1 + 82 planted defects
scripts/run_gates.sh     <clone> <packet> <python-with-pinned-markdown-renderer>
cc -std=c11 -O2 -DCONFIG_CLOCK_FREQUENCY=83333000 probes/probe_tick_math.c -o tm && ./tm
python3 probes/probe_mutants.py     <clone> <scratch>
python3 probes/probe_rv32_clock.py  <clone> <scratch> <rv32-gcc>
python3 probes/probe_held_report.py <clone> <scratch>
```

R500-4 FINISHED
