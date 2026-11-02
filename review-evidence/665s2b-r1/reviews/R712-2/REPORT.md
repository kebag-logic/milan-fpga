[R712] NEGATIVE - exact head c954b8a91e720f87d2dfa9294c8501058dc55df3

External independent review R712-2: issue #665, PR #810 (`665-s2b-cycles` into `dev-soft-core`), round 12. Head `c954b8a91e720f87d2dfa9294c8501058dc55df3`, tree `5e2989e8c7a2f72a1f1a7009d2132f4319017fd2`, source base `a68536fa`. The previous verdict from this reviewer was on `f884c7e9`.

I judged the whole change against `a68536fa`. I read the lane's own delta since `f884c7e9` in full: `f884c7e9..668126b3`, the merge `8b448143`, and `8b448143..c954b8a9`. All five lenses were applied.

## Verdict

The CPU clock move is correct, and so are its crossings, the boot simulation and the out-of-context timing receipt. Every composed row and pass figure the PR publishes recomputes exactly from the raw results, at both points, in both arms, with and without the drafts. The harness changes model the product more truly. The SRP two-pass reset is bounded, ordered and tested. The three merge fixes keep both sides. Every finding from the previous round is resolved at this head.

The verdict is NEGATIVE for two open MINOR findings:

- **F1:** the per-pass share is bounded only for the staged groups. The saved-state store's read-back step is centisecond tick work. The loop runs it in the same pass as the record work, with no joint bound. The author derives a 2.67 ms pass from this but does not bound or stage it. The step is 0.80 ms at 8x8 in the measured save groups, not the 0.70 ms the derivation uses, so that pass is about 2.77 ms. Frozen acceptance item 6 and round 12 item 3 require every pass within the share.
- **F2:** the gPTP assumption's figure "added to any row" omits the servo runs that its own table charges.

Neither finding says that a measured row exceeds its family bound.

## Authority read

- AGENTS.md, CONTRIBUTING.md (by reference), docs/README.md.
- FR_NFR 3.4.1 and 3.4.2, NFR-SCOUT-01 and -03.
- From #665:
  - the issue body;
  - the S2b assignment (issuecomment-6414297191, items 3, 6 and 7);
  - the no-clock-increase decision (-6488028169);
  - the T_svc = 20 ms decision with min(T_svc, ceiling) (-6495692075);
  - the clock correction (-6508196970);
  - round 11 (-6508235352);
  - the 100 MHz decision and round 12 (-6514866239);
  - the hold (-6515668991);
  - the TAKEN comment (-6563800676) and the REVIEW READY comment (-6569635407).
- The PR body.
- The interface documents the diff touches: `ctrl_loop.h` (THE SHARE), `srp_bounds.h`, `nvm_store.h`, `MAILBOX_SPLIT.md`, `SPLIT_CONTROL_MEMORY.md` sections 11 to 14, the harness README, `SAVED_STATE_FASTCONNECT.md` section 9 and DR2a.
- The public evidence tree at `e62d1256` (`review-evidence/665s2b-r1/author-r12` and `author-r12-results`). All 498 files match their published sha256 in `MANIFEST.json`: 0 bad, 0 missing, 0 unlisted (`receipts/evidence-manifest-check.txt`). The evidence commit carries no signature (`%G?` = N), so its integrity rests on the manifest hashes only.

## Findings

### R712-2-F1 - MINOR - Conformance, RTL (architecture), Robustness, Tests, Docs - the per-pass share does not bound the saved-state store's tick work

**Where:**
- `sw/firmware/ctrl/plat/ctrl_plat.c:258`: `nvm_store_service` is registered as a centisecond tick.
- `sw/firmware/ctrl/loop/ctrl_loop.c:106-110`: `dispatch_ticks` runs, in the same pass as the events, the receive records and the polls, up to `CTRL_LOOP_TICKS_PER_PASS` = 16 centiseconds (`ctrl_loop.h:114`).
- `sw/firmware/ctrl_nvm/nvm_store.h:60-64`: `NVM_READ_BYTES`, "0.7 ms of the 2.0 ms".
- `ctrl_loop.h:55-77`: THE SHARE, "no pass may exceed 2.0 ms ... Every slice serves that share".
- `docs/design/SPLIT_CONTROL_MEMORY.md:1314` and `:1318`.
- The PR body, "A pass no group stages".

**Authority:**
- S2b acceptance (issuecomment-6414297191, items 3 and 6): "No pass may exceed a stated share", and acceptance includes "every pass within the per-pass share".
- Round 12 item 3 (-6514866239): "Bound those passes' work so that every pass fits the share and every row still fits. If no split fits both, STOP with the figures."
- `ctrl_loop.h` states the share as the loop's contract.

**Evidence:**
- The read-back step is now 128 bytes. That is bounded per centisecond, not per pass. Nothing in the loop or the store defers a step out of a pass that has already taken its records.
- The author derives the coincidence and publishes it as an open risk ("1.97 + 0.70 = about 2.67 ms ... derived, not measured; the rows' margin holds it").
- The same document says, at `:1314`, that "every row the CPU decides and every pass fits at both points". The PR status repeats this, qualified as "measured".
- In the author's own raw results, N-A8 (8x8/2if, arm A, all groups), the worst pass of `acmp-notk` and of `acmp-noresp` is a store read-back step beside lwSRP's periodic MRP work. In each, `nvm_flash_litespi` takes 79,626 CPU cycles and `mrp_mad` about 38,000 (`receipts/store-step-in-pass.txt`, `receipts/flash-in-groups.txt`). So an 8x8 step costs **0.80 ms**; 0.70 ms is the 1x1 figure (70,531 cycles).
- The composed windows' heaviest 8x8 pass is 1.966 ms (`backlog-adp`, N-A8). With one step it would be about **2.77 ms**, 0.77 ms over the share.
- No backlog group contains a save: `load_flash` in each is the boot's constant 160 byte loads. So the share gate (`share.py`, `share_misses`) cannot see this pass.
- A centisecond count above 1 in one pass would run as many steps in that pass.

**Impact:**
- The frozen per-pass criterion is met only for the staged compositions.
- A save's blank check or verify that coincides with a record burst, which is an ordinary product sequence (a persisted change, then a controller burst within the save), produces a pass over the share. The documents state that no pass exceeds the share.
- The rows are not shown to fail: 15.96 + 2 × 0.80 = 17.56 ms is within 18 at two steps per row window. But `:1318`'s "the least margin, 2.04 ms, is more than a few such steps" is not right at 0.80 ms a step: 2.04 ms covers two steps, not three.

**Required outcome:** one of these.
1. Bound a pass's tick work jointly with its record work, so that every pass fits 2.0 ms with a save in progress. For example:
   - the store takes a read-back step only in a pass whose other work leaves room;
   - or the loop caps tick-consumer work per pass, and the rest resumes later, still bounded.
2. Or obtain a public amendment of the per-pass criterion that names the replacement bound, with its derivation and the row margin it consumes.

In either case, correct `:1314`, `:1318`, `ctrl_loop.h`'s claim, the `nvm_store.h` comment and the PR body to the 8x8 step cost.

**Verification:**
- A harness group in which a save's blank check or verify overlaps the heaviest backlog window, at 8x8/2if, both arms. It reports 0 passes over the share, or over the amended bound.
- Its rows are graded as before.
- A planted defect fails it: the step back to a whole page, or the deferral removed.

### R712-2-F2 - MINOR - Docs - the gPTP assumption's per-row figure leaves out the servo runs its own table charges

**Where:** `docs/design/SPLIT_CONTROL_MEMORY.md:1409-1410` and the PR body's gPTP paragraph ("1.6 ms on a row, 0.8 ms on a pass").

**Evidence (`receipts/gptp-arith.txt`):**
- The table charges 46 frames and 16 servo runs a second at 40,000 cycles each. That gives 2.48 % (1.24 to 6.20 %), which is correct.
- The row addition is "four frames in a window of up to 87 ms". That is the average frame rate alone, 46 × 0.087 s = 4.0 frames, so 1.6 ms.
- With the servo runs the same basis gives 5.39 units, so **2.16 ms**.
- An average count is not a bound for "any row". One Sync and Follow_Up on each port with their two servo runs is 6 units, so **2.40 ms**.
- Against the 8x8/2if last SRP record:
  - 15.96 + 1.6 = 17.56 ms is within 18;
  - 15.96 + 2.4 = 18.36 ms is over 18.
  So a reader who uses the published figure with the published 2.04 ms margin reaches the opposite conclusion.
- The pass addition (two records, 0.8 ms) likewise omits a servo run (1.2 ms). The section's other conclusions hold with it: S pass 4.9 ms; U pass 9.1 ms; Pdelay turnaround 9.8 ms under S and 18.1 ms under U, against 15 ms.

The figure is labelled an assumption, and that labelling is correct. The defect is that the figure disagrees with its own stated basis. It changes a published figure, so it is not RESIDUE.

**Required outcome:**
- State the per-row and per-pass additions from the table's own units, frames and servo runs.
- Say whether each is a mean or a bound.
- Say what it does to the 8x8/2if margins.

**Verification:** the two cells and the PR paragraph recompute from the table's rows.

### RESIDUE-1 (wording only; no verdict effect) - `tb/verilator/ctrl_service_budget/README.md:108`

The text says arm B "runs three of the four backlog rows ... without `backlog-adp-refill`, so its composed maximum is partial". This round's arm B runs (N-B1, N-B8, D-B1, D-B8) ran all four backlog groups, and their composed maximum is not partial (N-B8 `composed_maximum`: `windows` 4, `partial` false).

Exact fix: "Run with `--groups` naming three backlog rows, as S2's runs did, its composed maximum is partial; the 100 MHz runs of section 13 take all four."

### SUGGESTION-1 - `docs/design/SPLIT_CONTROL_MEMORY.md:1334-1353` - the S column's slope crosses arms

- The 1x1/1if column is the worst of arms A and B: AECP last 10.02, which is arm B.
- The 8x8/1if point is arm A only.
- So S's slope runs from arm B to arm A.
- With arm A at both ends, S for the last AECP record is 26.2 ms (+6.2) on arm A's 8x8/2if, or 27.0 ms (+7.0) on the worst arm. The table gives 25.8 ms (+5.8) (`receipts/estimate32-recompute.txt`).
- No verdict changes, and U and L are exact.
- Suggest that S use one arm at both ends of the slope, or that the text say it does not.

### SUGGESTION-2 - `sw/firmware/ctrl_nvm/README.md:229-231`, `SPLIT_CONTROL_MEMORY.md:1303` - give a save's read-back time in absolute terms

- "Twice as many ticks" is correct. A slot image of at most 8,192 B makes the read-back up to 2 × 64 centisecond ticks, 1.28 s, where it was 0.64 s. At 1x1 (4,764 B) it is 0.76 s, where it was 0.38 s.
- No split-firmware save deadline exists in the tree. DR2a says the debounce windows "supply no unconditional durability bound". `T-NVM-COMMIT-TIMEOUT`'s `commit_worst_ms` (`scripts/nvm_shape.py:120-124`) models the read-back at SPI bit rate, not one step a centisecond.
- So nothing is breached. A reader should still be told the absolute figure and that the commit-timeout model does not describe the split store's stepping.

## The six judgements requested

1. **The split CPU on `sys`, with the datapath clock unchanged.** Clean.
   - The wiring:
     - `milan_soc.py:3183-3207`: `CTRL_CPU_CD`, and `ctrl_cpu_domain`, which refuses anything else.
     - `:3279-3283`: `cpu_cd` and `cpu_clk_freq`; the all-fabric CPU keeps `milan`.
     - `:3324`: `with_cpu_clk` is false on `sys`, so the CPU has no `cpu_clk` port.
     - `:3468-3475`: `cpu_clk` and `cross_cpu_memory_ports` exist only off `sys`.
   - So the crossing is removed, not left degenerate. `MILAN_CLK_FREQ_HZ`, the PHC and the datapath keep `milan_clk_freq` (`:3539`, `:3729`). The mailbox's millisecond tick is on `sys` (`:3011-3013`).
   - `test_soc_options.py:299-346`: six killed controls, including a split CPU on `milan` being refused.
   - The boot simulation builds through `ctrl_cpu_cd` and refuses a CPU clock of its own (`boot_soc.py:80-86`). Its UART duties are graded at T_svc 20 ms. Author receipts: 1x1 24.660 ms, 8x8 64.271 ms, plants 2 of 2.
   - The out-of-context receipt (`area/ooc-sys-10`):
     - single clock `sys_clk` at 10 ns, `with_cpu_clk` false;
     - WNS +1.605, WHS +0.070, TNS and THS 0;
     - 8,709 of 8,709 nets routed, no unclocked or unconstrained internal endpoints;
     - the CPU 3,543 LUTs and 5,643 FFs, 6 RAMB36 and 7 RAMB18 = 9.5 tiles.
   - The input and output ports are unconstrained in this out-of-context run, and the documents call it an upper bound. The routed image is lane S9's.
2. **Rows and passes.** Clean.
   - Every leg records `cpu_cd` sys, `cpu_hz` 100,000,000 and `sys_hz` 100,000,000, and `cpu_cycles` equals `sys_cycles` in every probe.
   - Every row's bound is min(budget, ceiling): 20 ms, and 18 ms for SRP.
   - `scripts/table_rows.py` recomputes every cell of the PR's row and share tables from `results.json`, for N-A1/B1/A8/B8 and D-A1/B1/A8/B8 (`receipts/table-rows.txt`). Every cell matches.
   - Worst rows of each family at 8x8/2if:
     - AECP last 15.156 (N-B8);
     - SRP last 15.959 (N-B8) against 18, margin 2.04;
     - ACMP last 7.985;
     - ADP last 5.851 (owed window);
     - MAAP last 5.836;
     - the three owed rows over, as recorded (tsn-c-stack #26).
   - The share: 0 work passes over in every leg. The longest are 1.9664 (N-A8) and 1.9153 (N-B8). Arm A over all groups: 0 of 7,837 at 1x1 and 0 of 8,477 at 8x8.
   - No refusals.
   - The pass the measurement cannot see is F1.
3. **The SRP two-pass link change.** Clean.
   - `srp_mbx.c:773-812`: `reset_interface` closes licences and withdraws `TALKER_DECL` in the pass that takes the change, then destroys the participants and sets `reopen_polls` = 1.
   - `:851-857`: the next poll builds; the deferring poll returns owed, so the loop runs on.
   - `:479-483`: SRP receive waits while any interface reopens. It is bounded at two passes, and the record waits rather than being refused.
   - The withdrawal is neither delayed nor lost, and no withdrawal is reordered after a build, consistent with IEEE 802.1Q-2022 clause 35's withdraw-on-link-change.
   - A pass of link edges builds once.
   - The publication term moves 3 writes from the event to the poll, and the poll term still funds 5. I recomputed `MAILBOX_SPLIT.md`'s new figures exactly: 1,293 to 1,269 (8 × 3); the four table rows with (passes + 1) × 24; access times floored.
   - Tests: `srp_app.cpp` `LinkChangeBuildsTheNewParticipantsOnTheNextPass` and `LinkEdgesOfOnePassBuildOnce`, and six planted defects (`srp_reopen_mutants.py`). Hosted `firmware-srp-mutants` passed at this head.
   - The store's 128-byte read-back cannot lose, delay past a deadline or reorder a save: the step logic is unchanged and only its size halved (SUGGESTION-2). Its pass cost is F1.
4. **The harness changes.**
   - **Uncached flash window:** a truer model. The product applies `milan_soc.ctrl_uncached_flash` (`:3228-3247`, applied at `:3523`). The harness now does too, and refuses a build whose window differs from its arm's (`build.py:605-613`). Self-test: two mutants.
   - **AECP pacing:** this hides no load. The frames past the bucket's burst were refused by the filter and never reached the CPU. Only the single-command groups are paced (`scenario.py:474-482`, `:610`). The burst stays in the backlog groups (`admission.aecp.at_once` 16). Self-test: a mutant.
   - **Drained-ring opening:** harsher, not softer. With k records held, the coalescing grandmaster source commits fewer events. A drained ring gives the defined population of 15 of 15, and `check_load` refuses anything else.
   - The `events` wait counts the 16-bit `EVT_TAIL` through its wrap, consistent with `grade.unwrapped`. Self-test: `opening_checks`, and four mutants.
   - The 1x1, 4 KiB hybrid-XIP run has no refusals (`receipts/table-rows-other.txt`).
5. **Section 14.**
   - `scripts/estimate32.py` reproduces every U, L and S cell (`receipts/estimate32-recompute.txt`).
   - The excesses, the gPTP load (2.48 %) and the S and U passes (4.5 and 8.7 ms) are correct. So are the Pdelay figures (9.0 and 17.3 ms), the RV32IM 1x1 margin (0.02 ms) and 3,543 − 3,249 = 294 LUTs.
   - Labels: the 32x32 figures are an estimate, the one-CPU arms are measured (with the scratch RV32I arm labelled), and gPTP is an assumption.
   - Defects: F2, and SUGGESTION-1.
6. **The three merge fixes keep both sides.**
   - The boot simulation keeps S3's checks, and its CPU is on `sys`.
   - The platform image is built with the split hart's flags and audits (`ctrl_plat_image.py`). The ledger is restated at the measured 19,944 B (test_ctrl_memory passed). The hot-list check added in `99f51950` and removed in `bc50a190` was not on either side, so its absence is disclosed, not a loss.
   - The MAAP plant table moved out of `ctrl_mutants.py` content-identical: all 10 plants, and the text compares equal.

## Lens results

| Lens | Result at `c954b8a9` | Examined |
|---|---|---|
| Conformance | UNCLEAN: F1 | Acceptance items 3, 6 and 7 against the recomputed tables; min(T_svc, ceiling) on every probe; IEEE 802.1Q-2022 clause 35 behaviour of `srp_mbx.c:773-857`; the owner's clock decision against `milan_soc.py` |
| RTL (and architecture) | UNCLEAN: F1, architecture part only | Hardware clean: `milan_soc.py:3183-3324` and `:3468-3475`; `boot_soc.py:72-99`; `KL_mbx_dma.sv:169-177`; OOC `timing.rpt`, `route.rpt` and `route_hier.rpt`. Architecture: `ctrl_loop.c:89-158` against `ctrl_loop.h:55-114`, the share contract broken by tick work |
| Robustness | UNCLEAN: F1 | The two-pass reset under repeated edges, failed re-creation and the receive gate; store steps under accumulated centiseconds; the mover lengths 4092 to 4095 (bench D10) |
| Tests | UNCLEAN: F1, no group stages a save inside a composed window | Harness self-test mutants (`selftest_mutants.py:435-448`, `selftest_maximum.py:86-138`); `srp_app.cpp:322-370`; `srp_reopen_mutants.py`; the `nvm_mutants.py` `read_back_a_whole_page` plant; `test_nvm_write.cpp:657-659`; `test_soc_options.py:299-346`; the mover bench and its plants, which I re-ran |
| Docs | UNCLEAN: F1, F2; RESIDUE-1 | `SPLIT_CONTROL_MEMORY.md` 1238-1424; `MAILBOX_SPLIT.md` 743-783 and 1111-1118; `ARCHITECTURE_HW_SW_SPLIT.md:66-67`; the SRP, store and harness READMEs; the PR body; the comment-rule scan of the delta's source files (no new label, round, reviewer or comment ID) |

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1) | Recomputed row and share tables; `srp_mbx.c`; `milan_soc.py` CPU clock; acceptance items | R712-2 | c954b8a91e720f87d2dfa9294c8501058dc55df3 |
| RTL | UNCLEAN (F1, architecture) | `milan_soc.py` clock wiring; `boot_soc.py`; `KL_mbx_dma.sv`; OOC receipt; `ctrl_loop.c`/`.h` share contract | R712-2 | c954b8a91e720f87d2dfa9294c8501058dc55df3 |
| Robustness | UNCLEAN (F1) | Two-pass reset paths; store step under ticks; mover boundary lengths | R712-2 | c954b8a91e720f87d2dfa9294c8501058dc55df3 |
| Tests | UNCLEAN (F1) | Harness self-test and mutants; SRP, store and SoC-option tests and plants; mover bench (re-run, 21 of 21 plants) | R712-2 | c954b8a91e720f87d2dfa9294c8501058dc55df3 |
| Docs | UNCLEAN (F1, F2); RESIDUE-1 | `SPLIT_CONTROL_MEMORY.md` 11-14; `MAILBOX_SPLIT.md`; READMEs; PR body; comment scan | R712-2 | c954b8a91e720f87d2dfa9294c8501058dc55df3 |

## Prior public findings at this head

I read these only after my draft verdict and ledger were written: my own R712-1 and the internal round R711-1, both at `f884c7e9`. I read no review of this head before writing this report.

| Prior finding | Status at `c954b8a9` | Evidence |
|---|---|---|
| R711-1 F1 BLOCKER, rows fit only at a CPU clock the product does not run | **Resolved** | Owner decision of 2026-10-30. The product CPU is on `sys` (judgement 1). Every leg's clock record reads `sys` / 100 MHz, and the harness refuses any other. |
| R711-1 F2 = R712-1-F1 MINOR, mover length wrap at 4093 to 4095 | **Resolved** | `KL_mbx_dma.sv:176` sums in 13 bits. Bench D10 covers 4092 to 4095 in both directions, with a CPU access and recovery after. I re-ran it with Verilator 5.050: 420,827 checks, 0 failures (`receipts/dma-bench.log`). The plant `length-sum-wraps` is caught. |
| R711-1 F3 MINOR, three mover properties unguarded | **Resolved** | The plants `error-burst-continues`, `fill-during-cpu-answer` and `held-partial-write-widened` are each caught by a named check. Mover campaign: 21 of 21 caught (`receipts/dma-mutants.log`). |
| R711-1 F4 MINOR, firmware mover arm untested | **Resolved** | `test_mbx_dma_driver.cpp` is built with `CTRL_MBX_DMA_BASE` (`ctrl_arms.py:212-215`). Ratchet: `mbx.c` 330/330 lines and 164/164 branches; `mbx_dma.h` 10/10 and 4/4. Plants in `mbx_dma_mutants.py`. Hosted `firmware-unit` and `firmware-control-mutants` passed. |
| R712-1-F2 MINOR, per-pass share unmet and ungraded | **Resolved for its cause.** The residue of the same criterion is the new F1. | The share is asserted separately from the rows (`share.py`, `selftest_share.py`, the over-share plant). 0 passes over in every measured leg. |
| R711-1 RESIDUE R1 (`ctrl_mem.c:7`), R2 (`mbx_wire.h:62-64`), README "RV32I" | **Resolved** | `ctrl_mem.c:7-8` names the cacheless RV32I core it was written for. `mbx_wire.h:63` reads "the mailbox window is uncached". README:133 reads RV32IM on `sys`. |

## Execution evidence (this round)

- The evidence-tree manifest is verified (`receipts/evidence-manifest-check.txt`).
- I recomputed from raw results:
  - `receipts/table-rows.txt`, `receipts/table-rows-other.txt`, `receipts/recompute-rows.txt`;
  - `receipts/estimate32-recompute.txt`;
  - `receipts/flash-in-groups.txt`, `receipts/store-step-in-pass.txt`;
  - `receipts/gptp-arith.txt`.
- I ran the mover bench and its plant campaign on an exported copy of the head, with Verilator 5.050 (the identity is checked: `Verilator 5.050 2026-07-01 rev v5.050`): `receipts/dma-bench.log` rc 0, and `receipts/dma-mutants.log`, 21 of 21, rc 0.
- Hosted check runs at the exact head: 56 completed with success, and one skipped, `Physical gPTP (nightly and manual)`, which is not hardware evidence (`receipts/hosted-check-runs.tsv`). Acceptance of the hosted and replica results is the manager's.
- I ran no harness build, sweep, firmware bank or Vivado run. For those I relied on the author's published gate receipts (`author-r12/receipts/gates/TABLE.md`, all rc 0).

## Real limits

- I did not run the CPU budget harness: the product LiteX tree is not available to this reviewer. The row and pass figures are verified as computations from the author's published raw results, not by rebuilding the images. The image identities are taken from `image-identity.txt` and each leg's `build.json`.
- F1's 2.77 ms pass is derived from two measured passes, as the author's 2.67 ms is. No run stages the coincidence.
- I did not re-run the out-of-context timing. Its receipt is internally consistent; the routed split image is lane S9's.
- Physical calibration was NOT RUN, and field skips are not hardware proof.
- I could not find in the tree a normative 0.5 s deadline for a split-firmware save. Section 3 of the judgements and SUGGESTION-2 state what exists.

## Pending manager duties

- The current-dev merge candidate (source base `a68536fa`, live dev `1f29f189279f9fc0132f4918e47342b87d22f33a`): builder and native banks, and their receipts on the PR.
- Hosted and replica acceptance at the merge head.
- Disposition of F1: a fix, or a public amendment of the share criterion.
- Carrying RESIDUE-1 to the residue checklist.

## Integrity

`scripts/verify_checkout.py` → `receipts/checkout-integrity.log`:
- head and tree exact;
- the index equals the commit tree, 1,531 entries;
- 0 assume-unchanged or skip-worktree flags;
- 0 byte or mode mismatches over every tracked file;
- the status is empty.

Required submodule gitlinks, each equal to its checked-out head:

| Submodule | Gitlink |
|---|---|
| protocol-processor | a9e84b66d4cd0c331c8d6f2c1a71a62fcc824645 |
| gptp-processor | 135afd043309369a87ddbc8d6550aff8ec52a157 |
| third_party/lwSRP | 08ee86e812a0eb5e1dc6cd61b494d8baf3491348 |
| third_party/tsn-c-stack | 70936b77dc41981e192438388cd0aced69954f18 |
| third_party/verilog-axis | 48ff7a7e2ef782cf778d47910cf85835c64b1bce |

Probe copies and builds stay in this packet's unpublished `scratch/`. No source fixes, commits, pushes or GitHub writes were made. `MANIFEST.sha256` lists every publishable file.

R712-2 FINISHED
