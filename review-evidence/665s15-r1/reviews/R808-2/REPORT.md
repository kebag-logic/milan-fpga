[R808] NEGATIVE - exact head 936e0a566867aa648fb48e772a26fec99e3619c9

# R808-2: external review of PR #864 (issue #859, S15 32x32 shape), round 4 delta

**Reviewed:** head `936e0a566867aa648fb48e772a26fec99e3619c9`, tree `c8da5b75caa0d7666437e0f4f905f8dd64934a46`. Delta `7aa6ef0c..936e0a56` (5 commits, 14 files) inside `1d6bf555..936e0a56`.

**Read, in order:** AGENTS.md and CONTRIBUTING.md; the #859 body and the assignment (issuecomment-6723527155); the round 4 ruling (issuecomment-6746289265) and the owners comment (issuecomment-6746307340); the REVIEW READY at this head (issuecomment-6754805021); the PR body; the delta and its history. Then the author's published packet `review-evidence/665s15-r1/author/a752d` at `92efa492`. The prior public findings (R808-1, R807-1) were read only after my own pass over the delta.

**Verdict: NEGATIVE.** Every ruling item for round 4 is met, and every prior finding but one is resolved. The one still open is the 33-sink ACMP owed-release alias (R808-1-F1 / R807-1-F1). Its documentation half is resolved. Its code half is still in the image this PR builds: the pin is still `70936b77`. The ruling itself gives the fix to round 5 (the pin move), and a finding moved to another issue is not resolved (AGENTS.md section 7). So it holds the Conformance, RTL, Robustness and Tests lenses unclean at this head.

The decode defect the author found is real, and the fix is correct at every layout this PR produces. The block decodes do not share the ring decode's bound form, so they are not a defect now (see section 2).

## 1. Ruling items, one by one

| Item | Result | Evidence |
|---|---|---|
| 1. Census row and PR body state what the RV32 image at the pin does; owner tsn-c-stack#31 replaces #653 | **Met (documentation).** The code defect is retained as F1 | `docs/design/SHAPE_32X32_CENSUS.md:194`, `:260`; PR body Round 4 item 1. The cited lines hold at the pin: `acmp.h:400` `uint32_t release`, `acmp.c:816`/`:871` `1u << k` (in `bind_response`/`unbind`), `:310`/`:1225` `(release >> k)` (in `transmit`/`acmp_poll`). My own RV32I `-Os` compile of the pinned `acmp.c` at `ACMP_MAX_SINKS=33u` emits a register-count `sll` in `bind_response` and `srl` in `transmit` and in the poll loop. That corroborates the claim, though it uses the host cross compiler, not the pinned SDK. tsn-c-stack#31 is OPEN; its PR #33 is OPEN at `c6013804` (the donor is not reviewed here) |
| 2. ACMP transmit ring sized from the census rule; self-test arm; `--check` 0 drift; 32x32 point re-run; receive shortfalls owned by #865 | **Met** | `sw/mailbox/gen_mailbox.py:259` (`acmp_tx_words`: 33 x 20 = 660 words, so 1,024), `:268` (`with_tx_ring`), `:307` (`shape_variant`). My run: `--check --crosscheck` "0 finding(s)", `--selftest` "0 arm(s) failed". Three in-process mutants (ring unsized, short-ring refusal removed, pre-fix bounded decode) each turn `--selftest` red. All five shipped configs' `--variant-shape` outputs are byte-identical between `7aa6ef0c` and head. Only the 32x32 variant differs, in 13 lines, all of them the ACMP transmit ring. Author M32 run at this head: 17 groups, 0 refusals. #865 is OPEN and the census rows `:238`, `:240`, `:263` link it. The PR body's "Ring items" line lists what is met and what is owed |
| 3. Census owners (AEM ROM store and figures, TDM8 probe, crossed limits to #866, hook harness and F5, guard citation) | **Met** | `SHAPE_32X32_CENSUS.md` section 2 AEM rows; figures re-derived by me from the builder's `AEM_ROM_BYTES_C`: 4,527 / 11,753 / 41,465 B. The TDM8 refusal text matches the author's `r4/shape/aem_rom_probe.log`. #866 is OPEN and names all five items. Section 5 gives the hook harness and F5 reasons; `hooks_build.py:37` is its `POINTS`. The guard is at `hdl/milan/milan_datapath.sv:5354-5358` at head |
| 4. `record.*`, `rebuild`, `centisecond` re-measured at the round 4 image's hash, beside S2b's projection with the error | **Met** | PR body table. The image SHA-256 `2e47b49e…` is the same in the M32 and I32 legs (the I32 leg is DIRTY only by its testbench instrumentation). I recomputed all 7 rows: projection = the line through (2, 1x1) and (16, 8x8) evaluated at 64; stated = most cycles x 1.05 / 100, rounded up to 5 us; error = projected − measured. All 7 match, and the cycle counts match `r4/costs/parts-32x32.json`. #859 stays open for the costs this base cannot measure ("Relates to #859") |
| 5. Residue and suggestions | **Met** | `endstation_builder.py:201` reads `#: at that shape (#859).` The census `:249` uses the README's term. `SPLIT_CONTROL_MEMORY.md` section 8 is given at `41f963d5` with the image hash (the same image as head). Gate 39 plants `srp.rtl_table`: my run shows 3/3 red. The `simulation identity` rule, its row (`SPLIT_CONTROL_MEMORY.md:86`), its arm and its mutant: author receipt `lane-r4b/ctrl_memory.log:70`, `:153`, PASS. The short-layout compile arm: my `--selftest` shows both static assertions refusing it |

## 2. The decode defect found in this round

- **Real, and fixed correctly.** `mailbox_skeleton.py:524-532` (`_ring_decode`) drops the upper bound only for a ring ending at the window's top.
  - Evidence in the RTL: at 15 bits, `AW2_C'(0x7000 + 4*1024)` is 0.
  - My own lint of the 32x32 variant with the pre-fix bound restored reports `%Warning-UNSIGNED … Comparison is constant due to unsigned arithmetic` at the restored line. The variant as generated and the tracked `KL_mbx.sv` lint with 0 warnings (`receipts/lint-*.log`).
  - The author's run at `81521a8a` refused three groups; at this head the run refuses none.
  - `--crosscheck` (`gen_mailbox.py:124`) catches the wrapping bound (`receipts/crosscheck-probe.log` (b)).
- **The other register blocks are not a defect, now or latently, for this reason.** The bound-talker, publication and face decodes do not use `off_w < AW2_C'(BASE + SIZE)`. They decode relative to their base: `off_w >= BASE && (rel >> $clog2(STRIDE)) < N_IF && entry < N` (`hdl/milan/mailbox/KL_mbx.sv:228-230`, `:266-268`, `:301-302`), with `rel = off_w - BASE` taken in `AW2_C` bits. That form cannot wrap for a block that ends at the window's top. Every other `AW2_C'(… + …)` in the file is an equality decode inside the register space. The REVIEW READY's open risk, "the skeleton's block decodes … use the same bound form as the rings", is therefore inaccurate (R808-2-N4, RESIDUE).
- Two narrower edges of the fix remain. They are recorded as SUGGESTIONs N1 and N2.

## 3. Findings

### R808-2-F1 (= R808-1-F1, R807-1-F1, retained, narrowed) - MAJOR - Conformance, RTL, Robustness, Tests

- **Where:** `third_party/tsn-c-stack/src/acmp.c:310`, `:816`, `:871`, `:1225` and `include/acmp.h:400` at pin `70936b77`. They are reached by `sw/firmware/ctrl/test/ctrl_srp_image.py` (`acmp_sizing`, `-DACMP_MAX_SINKS=33u`) in the 32x32 image `2e47b49e…`.
- **Authority/evidence:**
  - C11 6.5.7p3.
  - Milan v1.2 5.5: a change notice waits only behind its own owed response.
  - AGENTS.md section 7: a finding moved to another issue is not resolved.
  - The ruling's item 1: "S15 round 5 syncs onto that pin … rebuilds the 32x32 image … checks the disassembly", and "this is a donor fix, not a decision to accept it".
  - At this head the pin is unchanged. The author's own `r4/donor/probes/probe-pin.log` still reports `acmp.c:816:31: runtime error: shift exponent 32`, with rc 1.
  - My RV32I compile shows the register shifts.
- **What changed since round 1:** the documentation half is resolved. The census (`:194`, `:260`) and the PR body describe the alias correctly, name tsn-c-stack#31 (PR #33) as owner, and drop the closed #653.
- **Impact:** the firmware this PR builds and measures at 32x32 still executes a shift by 32. Sinks 0 and 32 each hold the other's change notices. No test at the shape reaches it, because no harness script binds a sink past 1.
- **Required outcome:** as the ruling sets it. The 32x32 image is built on a tsn-c-stack pin whose mask follows `ACMP_MAX_SINKS` (round 5's sync onto the pin move), and the census row and PR body are updated to match.
- **Verification:** R807-1's `acmp_mask_probe.sh` exits 0 at the head's pin. The disassembly of `bind_response` and `transmit` in the rebuilt image shows a word-indexed mask. The 32x32 point is re-run. The probe on index 32 (R808-1-F8) passes.

### R808-2-N1 - SUGGESTION - Tests, RTL

- **Where:** `sw/mailbox/gen_mailbox.py:124-143` (`ring_decode_findings`).
- **What happens:** the cross-check tests only that each ring's first and last word fall inside its decode. A decode that wrongly drops its upper bound for a ring below the top still passes. In my probe, the 32x32 variant with the event ring's upper bound removed gives `crosscheck: []` (`receipts/crosscheck-probe.log` (c)). The decode values are also taken from the contract, not from the constants named in the RTL text. The tracked shapes are protected by `--check`'s byte comparison; the generated variants are not.
- **Suggested:**
  - Also require the first word past each ring (when it lies below the window's top) to fall outside its decode.
  - Optionally, lint the shape variant with `UNSIGNED` as an error: that is how the pre-fix bound is flagged.

### R808-2-N2 - SUGGESTION - RTL, Robustness

- **Where:** `sw/mailbox/mailbox_skeleton.py:528` (`if end == contract.window_bytes`), together with `mailbox_model.load`.
- **What happens:** dropping the bound is correct only because the window is a power of two, and `load()` does not require one. A contract with `window_bytes: 0x7800` loads, its decode is still 15 bits wide, and a ring placed at that window's top is emitted with no upper bound. The decode then also claims `0x7800..0x7ffc`, and the cross-check finds nothing (`receipts/window-probe.log`). No layout this PR builds reaches this case: the window is the contract's `0x8000`.
- **Suggested:** either drop the bound only when `end == 1 << AW2_C bits`, or have `load()` refuse a window that is not a power of two.

### R808-2-N3 - SUGGESTION - Tests

- **Where:** `tb/verilator/ctrl_service_budget/grade.py:37` (`tx_rings`), `run.py:265`, `scenario.py:804-815` (the owed row's admitted bursts).
- **What happens:** only the 53-minute 32x32 run exercises the new path: reading transmit records from the point's layout, and the chunked owed row. No harness self-test arm grades a log at a non-contract layout, so a regression to the default `TX_RING` would not be caught by `run.py --self-test`.
- **Suggested:** one self-test arm that grades a synthetic record stream at the 32x32 layout, with that mutant planted.

### R808-2-N4 - RESIDUE - Docs (wording in the REVIEW READY's open risks; not in the repository or the PR body)

- **Where:** issuecomment-6754805021, "Open risks/questions".
- **Exact fix:** replace "the skeleton's block decodes (publication, face, bound-talker) use the same bound form as the rings; no layout places a block at the window's top, and they are unchanged" with "the skeleton's block decodes (publication, face, bound-talker) bound each access by interface index relative to the block's base, so they do not wrap at the window's top; they are unchanged". Carry the corrected sentence into the next handoff.

### R808-2-N5 (= R808-1-F8, retained) - SUGGESTION - Tests

No harness script touches index 32. The ruling gives this probe to round 5.

No new comment-rule instance was found in the delta. I scanned every added non-markdown line in `7aa6ef0c..936e0a56` for lane labels, rounds, reviewer IDs and comment IDs: 0 hits. The one instance from round 1 is removed.

## 4. Prior public findings at this head

| Finding | Status | Evidence |
|---|---|---|
| R808-1-F1 MAJOR / R807-1-F1 MAJOR | **RETAINED** as R808-2-F1 (documentation half resolved) | section 3 |
| R808-1-F2 MAJOR / R807-1-F2 MINOR | RESOLVED | ring sized from the rule, self-test arms and mutants, 0 drift, point re-run, #865 linked, ring items listed in the PR body |
| R808-1-F3 MINOR / R807-1-F3 MINOR | RESOLVED | AEM ROM row with re-derived figures and the TDM8 probe; owners #866 (OPEN) and #865; hook harness and F5 reasons; guard `:5354-5358` checked at head; #394 replaced |
| R807-1-F4 MINOR | RESOLVED | cost table at image `2e47b49e…`, arithmetic recomputed; #859 stays open for the rest |
| R808-1-F4 SUGGESTION / R807-1-S1 | RESOLVED | `SPLIT_CONTROL_MEMORY.md` section 8 at `41f963d5` with the image hash |
| R808-1-F5 RESIDUE / R807-1-R1 | RESOLVED | `endstation_builder.py:201` |
| R808-1-F6 RESIDUE | RESOLVED | census `:249` |
| R808-1-F7 SUGGESTION | RESOLVED | `gen_mailbox.py:327` (`firmware_refusal`) and its two arms, my `--selftest` run |
| R808-1-F8 SUGGESTION | RETAINED as N5 | given to round 5 |
| R807-1-S2 SUGGESTION | RESOLVED | gate 39 plant (my run, 3/3 red); `simulation identity` rule, row, arm and mutant (author receipt) |
| Executor's round 2 MINOR (gate numbering) | still RESOLVED | gate 41 passes with its plant in my run |

## 5. Clean results and lens coverage

| Lens | Result | What was checked |
|---|---|---|
| `Conformance` | UNCLEAN (F1) | Every ruling item (section 1). Milan v1.2 5.5.2.3 sizing: 33 x 20 = 660 words, giving 1,024 words and 51 records (`gen_mailbox.py:259`, variant `mbx_contract.h:1153-1155`). The owed-frame alternative is not a build-time form (`acmp.h:164`, no `#ifndef`) |
| `RTL` | UNCLEAN (F1) | `mailbox_skeleton.py:524-532`, `KL_mbx.sv:228-302`, `:975-1136`. 32x32 variant lint: 0 warnings; the pre-fix mutant: 1 `UNSIGNED`. Relative block decodes. `with_tx_ring` placement against `_check_contract` |
| `Robustness` | UNCLEAN (F1) | Window-top boundary (`receipts/crosscheck-probe.log`, `window-probe.log`). Short ring refused (`shape_findings`, mutant `norefuse` caught). Shipped variants unchanged (`receipts/variant-identity.txt`) |
| `Tests` | UNCLEAN (F1: no test reaches sink 32) | My gates (section 6). Mutants `unsized`, `norefuse` and `bounded` caught by `--selftest`. Gate 39 3/3, gate 41 1/1. Harness self-test 0 failures |
| `Docs` | CLEAN | Census `:3-4`, `:30`, AEM rows, `:194`, `:228-263`. `MAILBOX_SPLIT.md:120-139`. `SPLIT_CONTROL_MEMORY.md:86`, `:396-406`. `ctrl_service_budget/README.md:58-59`. PR body Round 4. Residue N4 is wording only and does not un-cover the lens |

## 6. Executed by this review (clone at the exact head, verified clean)

| Gate | Result |
|---|---|
| `gen_mailbox.py --check --crosscheck` | rc 0, "0 finding(s)" |
| `gen_mailbox.py --selftest` | rc 0, "0 arm(s) failed" |
| `test_builder.py --gates test_control_placement_key,test_simulation_shape_option,test_shipped_shape_outputs_unchanged` | rc 0, "ALL GATES PASS" (gate 39 3/3, gate 41 1/1) |
| `ctrl_service_budget/run.py --self-test` | rc 0, "self-test: 0 failures" |
| `check_py_idiom.py` and its `--selftest` | rc 0 |
| `docs_check.py`, `check_doc_paths.py` | rc 0 |
| `git diff --check 1d6bf555 HEAD` | rc 0 |
| `test_ctrl_memory.py`, `test_soc_options.py` | **NOT RUN here**: `migen` is absent in this environment. The author's receipts at this head show PASS (`r4/lane-gates/lane-r4b`) |
| Probes | AEM ROM figures, variant identity against `7aa6ef0c`, RV32 disassembly, variant lint, cross-check probe, window probe, three self-test mutants |

The mailbox Verilator bench (`tb/verilator/mbx` `run-if2`) cannot take the 32x32 layout: its own static assertion refuses it (`suite.hpp:72`), so it was not used as a probe.

**Hosted, at the exact head:** 68 check runs succeeded, including `rtl-fast`, `verilator-suites`, `yosys-portability`, `elaborate`, `docs-check` and the firmware jobs. One was skipped: Physical gPTP (nightly/manual), which is not hardware proof (`receipts/hosted-checks.tsv`). Hosted and act acceptance stay with the manager.

**After the probes:** HEAD and tree are as stated; index == HEAD tree for 1,551 entries (mode, blob, path); the worktree is clean with 0 untracked or ignored files. The submodule gitlinks equal their checkouts and the submodule worktrees are clean (`receipts/clone-verify.txt`).

## 7. Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1) | ruling items 1-5; census; `gen_mailbox.py:259-307`; `acmp.h:157-164`, `:400`; `acmp.c:310`, `:816`, `:871`, `:1225`; PR body Round 4 | R808-2 | `936e0a566867aa648fb48e772a26fec99e3619c9` |
| RTL | UNCLEAN (F1) | `mailbox_skeleton.py:524-560`; `KL_mbx.sv:228-302`, `:975-1136`; 32x32 variant `KL_mbx.sv:1044`; lint receipts; RV32 disassembly | R808-2 | `936e0a566867aa648fb48e772a26fec99e3619c9` |
| Robustness | UNCLEAN (F1) | window-top and non-power-of-two window probes; short-ring refusal; variant identity across 6 configs | R808-2 | `936e0a566867aa648fb48e772a26fec99e3619c9` |
| Tests | UNCLEAN (F1) | `--selftest` arms and 3 mutants; gates 39/41; harness self-test; `grade.py:37`, `run.py:265`, `scenario.py:804-815`; author M1/M8/M32/I32 receipts | R808-2 | `936e0a566867aa648fb48e772a26fec99e3619c9` |
| Docs | CLEAN | `SHAPE_32X32_CENSUS.md`, `MAILBOX_SPLIT.md:120-139`, `SPLIT_CONTROL_MEMORY.md:86`, `:393-406`, `ctrl_service_budget/README.md:58-59`, PR body | R808-2 | `936e0a566867aa648fb48e772a26fec99e3619c9` |

## 8. Real limits

- `test_ctrl_memory.py` and `test_soc_options.py` were not run here (no `migen`); author receipts are relied on. No firmware image was built here. The RV32 corroboration uses the host cross compiler at the image's `-Os -march=rv32i` flags, not the pinned SDK.
- The 32x32 harness point (53 min) and the cost legs were not re-run. I checked the published receipts' hashes (814 of 814 `a752d` files match `MANIFEST.json`), their heads and image hashes, and the arithmetic. The 32x32 harness point is recorded, not graded.
- S2b round 22's per-cost figures (`s2b-costs-final.json`) were taken as published and not traced to #810's head.
- The donor tsn-c-stack PR #33 was not reviewed beyond its existence and head.
- Physical calibration was NOT RUN, and field skips are not hardware proof. No manager source bank runs at this head; none is claimed.

## 9. Pending manager duties

- Round 5 under the ruling: the pin move to tsn-c-stack `main` with PR #33, the probe on index 32, a rebuilt 32x32 image, its disassembly, and a re-run of the point. After that, re-review F1 at the new head.
- Carry N4 to the residue checklist.
- Validate the current-dev merge candidate (source base `1d6bf555`, live dev `123f57a9`) at the merge turn, and own the hosted and act acceptance.

R808-2 FINISHED
