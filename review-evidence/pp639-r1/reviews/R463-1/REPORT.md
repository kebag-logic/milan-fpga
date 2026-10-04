[R463] POSITIVE - exact head 9e8699105c126db7764820916a827ef0538bc4b2

# R463-1: external independent review of processor PR #155 (milan-fpga #639, area levers 3 and 6)

- Repository: Mister-M-alt/protocol-processor-control-plane-avb-milan, PR #155, branch `pp639-armq-lsnrec`.
- Exact head `9e8699105c126db7764820916a827ef0538bc4b2`, tree `8c9839731f0bfbda66d3d70c4b088115324d0c66`. Source base `5c71928ad2bf1a854a5538d69b77214dfdf1697f`.
- Role: external reviewer [R463], cleared context, isolated detached clone. The internal review ran separately; I did not read its output.
- Verdict: **POSITIVE**. All five lenses are CLEAN.
  - There is no open BLOCKER, MAJOR or MINOR.
  - One RESIDUE (F1, wording) and one SUGGESTION (S1) are recorded.
- Prior public review findings on PR #155: **none to resolve**. At review time the PR had 0 reviews and 0 inline review comments. Its comments are the review-start and evidence announcements only.

## 1. What was reconstructed, in order

1. **Contributor rules.** The processor repository has no AGENTS.md or CONTRIBUTING.md. Its rules are in `README.md`, `docs/README.md` (single-source rules, ID registries) and `docs/guides/hdl-engineer.md` §3 (storage and drop rules).
2. **Frozen acceptance:** the issue body plus the manager's lane assignment on milan-fpga #639.
   - Each lever is measured before and after with the #234 recipe, with no lost function. Every suite and campaign that reads the block passes at the same counts.
   - The gate baseline is re-recorded in the same reviewed change.
   - No port, parameter or register change without a STOP. Behaviour is identical, with timer expiry order and latency as today.
   - Equivalence is proven by a lockstep bench of main's block against the head's, with planted controls.
   - Timing is judged at the declared 50 MHz.
3. **Authorities**, all at the head:
   - the timer arm-port banner (`hdl/top/protocol_processor_top.sv:2925-2934`);
   - the listener's record-storage contract (`hdl/acmp/KL_pp_acmp_listener.sv:381-396`);
   - the drop rule in the HDL guide (§3.2);
   - snapshot word 24 in the operator guide;
   - the parent gate `syn/ooc/pp_resource_gate.py` and its baseline at dev `fea346e7`.
4. **Diff and history.** `git diff 5c71928a..9e869910` is 35 files. The lane's own part is `git diff 5c71928a..cfd62e8`: 12 files, +411/-45 (5 one-line commits).
   - The two `--no-ff` merges are `b845d01` (main `83999eba`) and `9e86991` (main `c050d971`).
   - The lane diff and main's diff each appear byte-identical across the merge, apart from index and hunk offsets. So both sides are kept.
   - Each merge tree equals `git merge-tree --write-tree` (`8c983973…`, `993fbd72…`), so nothing was hand-merged.
5. **Public evidence.**
   - milan-fpga `f0e730f8` (author packet) and `28663f5a` (Vivado receipts), `review-evidence/pp639-r1/`.
   - MANIFEST.json: 63 entries, 0 published-hash mismatches, no unlisted file.
   - The issue and PR comments.

## 2. Findings

| ID | Severity | Lenses | Where | Authority / evidence | Impact | Required outcome | Verification |
|---|---|---|---|---|---|---|---|
| F1 | RESIDUE | Docs | `docs/architecture/09_verification.md:391-393` | The sentence reads "Two benches of the issue's own compared `main`'s block with the new one in lockstep … ; they are recorded in the issue's pull request, not kept in `tb/`." But the PR records only the benches' **results**. The benches stay in the author's scratch: the published HANDOFF §4.1/§4.2 says "(scratch, not committed)" and §12 lists them under scratch evidence. Neither the PR nor `review-evidence/pp639-r1` holds them. | Wording only. A reader looking in the PR for the benches finds only their tallies. No figure, test, code or claim about behaviour changes. | Exact fix: replace "they are recorded in the issue's pull request, not kept in `tb/`" with "their results are recorded in the issue's pull request; the benches are not kept in `tb/`". | Read the sentence after the edit; `make check` stays green. |
| S1 | SUGGESTION | Tests | `tb/pp_top/sim_main.cpp:722` (`ArmQueueModel`); `tb/pp_top/acmp_mutants.py:164-168` | Committed traffic never fills a face: AQ coverage is 0 deep pushes, 0 fills and 0 drops (reproduced, §5.3). So three ring defects pass **every** committed check: (1) a write gated by the offer rather than its acceptance; (2) a write-first read on a full queue's pop-and-push; (3) a full queue that pops refusing the push. I planted (2) and (3) in the head and ran `--arm-queue-only`: `AQ: 2 checks, 0 failures` for both (receipts `receipts/logs/aqmut_*.log`). My lockstep kills all three in 32 of 32 runs (§5.1). | No defect at this head: the equivalence is established (§5.1). The ring's full-queue overwrite and its drop path are new code, though, and only out-of-tree lockstep guards them against regression. | Optional. Add a committed check that fills a face, for example a small standalone bench of the arm mux beside `ArmQueueModel`, so the full, overwrite and drop paths have an in-tree kill. | A committed control such as `write_refused` would then be KILLED in-tree. |

**Decision on whether a committed full-queue check is required: not required.** Reasons:

- The frozen acceptance names a lockstep bench with planted controls as the equivalence proof. It does not ask for an in-tree full-queue test.
- The repository already accepts out-of-tree lockstep receipts for equivalence. See `tb/acmp_talker/README.md:318-323`.
- Before this lane the shift queue's full path was equally unreached in-tree. The lane did not reduce coverage. It added AQ, which grades everything external traffic reaches and passes on main's RTL with identical coverage.
- The full and drop paths are proven equivalent at this head by an independent re-implementation of the lockstep, published in this packet (§5.1).

That makes it S1, not a MINOR.

Observation, not a finding of this PR: the drop counter rises once per clock however many faces overrun together. This is pre-existing, unchanged by the lane, and recorded as out of scope in the PR and in `tb/pp_top/README.md` section AQ. The issue's no-behaviour-change rule keeps it out of this lane.

## 3. Lens results

### 3.1 Conformance: CLEAN

- **No change at any port.**
  - The diff touches no port list of `protocol_processor_top` or `KL_pp_acmp_listener`. The added `dbg_aq_*` ports are on the bench wrapper `tb/pp_top/pp_top_wrap.sv` only.
  - No parameter changes.
  - The only register changes are internal storage: `armq_r` becomes `mem_r` plus `armq_hd_r`, and `rec_rdata_r` is removed. Neither is a software-visible register.
- **No protocol-visible timing change.** Both blocks are cycle-identical to main under lockstep (§5.1, §5.2). So timer arm order, arm latency, the drain priority, the drop counter (snapshot word 24) and every listener output are unchanged. Milan/IEEE behaviour and clause claims are therefore untouched, and the docs make no new clause claim.
- **Closing keyword.** "Relates to milan-fpga#639" is correct: the acceptance's gate re-baseline lives in the parent (`syn/ooc/pp_resource_baseline.json`). The PR states this, and §4 shows the re-baseline is needed.

### 3.2 RTL: CLEAN

- **Ring invariant** (`protocol_processor_top.sv:3006-3043`).
  - Entries `hd … hd+cnt-1 (mod 4)` hold the queue in order. A pop advances `hd`, and a push writes at `hd + cnt` (old count) whether or not the same clock pops.
  - After a pop and push the new tail is `(hd+1) + (cnt-1+1) - 1 = hd + cnt`, the slot written.
  - At `cnt = 4` with a pop, `cnt[1:0] = 0`, so the write lands on the leaving head. The asynchronous read returns the old entry before the edge, so the port register captures the leaving arm.
  - At `cnt = 4` without a pop, `push_ok` is false and nothing is written.
  - `arm_drain_pick`, `armq_mid_w`, `armq_push_ok_w`, the count update and `arm_drop_r` are unchanged lines.
- **Listener read** (`KL_pp_acmp_listener.sv:395, 746, 1050-1074`).
  - `rec_rd_w` is consumed only in X_LATCH and X_STRT_AP. Those are entered only from X_RDREC and X_STRT_RD (`:1034`, `:1067`), which X_IDLE enters (`:953`, `:989`, `:997`, `:1007`).
  - `sink_r` is written only in reset and X_IDLE.
  - `recwr_en_w` is true only in X_INIT, X_PRELOAD and X_WB (`:744-745`).
  - So the asynchronous read in the consuming cycle equals what the removed register sampled one edge earlier. Nothing else read `rec_rdata_r`: a tree-wide grep finds no remaining reference to `rec_rdata_r` or `armq_r`.
- **Inference, from the published synthesis logs.**
  - `g_armq[k].mem_r_reg | User Attribute | 4 x 47 | RAM32M x 8` for k = 0..7 (4 x 48 at 8x8).
  - `u_listener | rec_ram_r_reg | User Attribute | 2 x 376 | RAM32M x 63` (16 x 376 at 8x8).
  - At base, the records are `2 x 376(READ_FIRST) … | 1 | 5` block RAM.
- **Timing at 50 MHz.** Route WNS rises from +0.079 to +0.093 ns and WHS from +0.014 to +0.036 ns. The head's worst hold path ends at a ring RAM data input (`g_armq[4].mem_r_reg_0_3_24_29/RAMA/I`) and meets at +0.036 ns. Both builds meet the gate floors (WNS at least 0.03, WHS at least 0).
- **Lint.** `scripts/lint_hdl.sh` passes 41 of 41 modules with the pinned simulator, identity checked: 5.050, wrapper sha256 `905795b9…e79e92f`, equal to the author's.

### 3.3 Robustness: CLEAN

- **The ring entries are not reset; only the count and head are.**
  - My arm lockstep starts every unreset bit random. It takes mid-run resets of 1 to 4 clocks with offers still arriving, and saturates queues across resets. Result: 0 mismatches.
  - The probe `probe_head_unreset` (head index not reset) is equivalent, 0 of 32 runs differ, as the author also found: a ring may start anywhere.
- **The 16-bit drop counter saturates** at 0xFFFF. There were 21.0M saturated clocks across the 32 x 1M runs. The control `drop_wraps` is caught in 32 of 32 runs.
- **Full-queue pop-and-push overwrite:** 5,074,588 such clocks in 32 x 1M and 49,192,161 in 32 x 10M, with 0 mismatches. The control `read_write_first` diverges on exactly 5,074,588 clocks, so the bench exercises precisely that path.
- **Listener RAM.**
  - The array was unreset before and after; the X_INIT sweep is its only reset.
  - My listener lockstep: random initial state, 689 reset-asserted clocks at 1M and 5,369 at 10M, mid-run with records bound. 0 mismatches.
  - Committed RS reproduces 3,111 of 3,111 at the head and on main's RTL.
  - An out-of-range `sink_r` never reaches X_RDREC or X_STRT_RD, which are guarded at `:952`, `:976` and `:1006`. This is unchanged.
- **4-state simulation:** an unwritten ring entry or record is read only when its value is not consumed (pop needs `cnt != 0`; records are swept before X_IDLE).

### 3.4 Tests: CLEAN (S1 recorded)

See §5 for every run. Summary:

- I built independent lockstep benches for both structures, at the PR's counts and at ten times them.
- I reproduced the committed AQ and RS checks at the head and on main's RTL.
- Reproduced at their recorded counts: the ACMP campaign (29 of 29 KILLED, every arm's failing count as recorded), the full `tb/pp_top` suite (10,418 of 10,418) and `tb/acmp_listener` (3,111 of 3,111).
- The `tb/adp_engine` campaign returns identical verdict lines at the head and main. Its two flagged rows are the same at both, so they are independent of this lane.

### 3.5 Docs: CLEAN (F1 recorded as RESIDUE)

- The lane's prose is accurate against the RTL and the measurements:
  - the RTL comments in the top and the listener;
  - `tb/pp_top/README.md` section AQ and the ACMP controls paragraph;
  - `tb/acmp_listener/README.md` (3,111; RS; five controls with counts that match my campaign);
  - `docs/architecture/07_memory_maps.md` §6, `08_timing.md` §3, `09_verification.md` §8.8;
  - `docs/guides/hdl-engineer.md` §3.1.
- No stale "sync-read" or "shift queue" description of either structure remains.
- `make check` passes: 41 mermaid and 18 wavedrom blocks, 1,123 links, 115 REQ rows, 94 matrix rows with 0 untested, 28 parameters. `scripts/gen_matrix.py --check` also passes.
- F1 is the one wording residue.

## 4. Vivado figures, re-derived from the published runs

Script: `scripts/vivado_rederive.py`. Output: `receipts/gate/vivado_rederive.txt`. Inputs: milan-fpga `28663f5a` `review-evidence/pp639-r1/author-r1/vivado/` and the gate baseline at dev `fea346e7`. Every figure below equals the PR body and HANDOFF.

| Endpoint | LUT base → head | FF base → head | Slice | RAMB36 / RAMB18 | DSP | WNS / WHS ns |
|---|---|---|---|---|---|---|
| Route 1x1 (`endstation_ax7101_1x1_tdm8`) | 51,434 → 51,152 (-282); logic 49,158 → 48,450, memory 2,276 → 2,702 | 59,691 → 58,598 (-1,093) | 15,847 → 15,803 (-44) | 79/27 → 74/27 | 14 → 14 | +0.079/+0.014 → +0.093/+0.036 |
| Standalone 1x1 | 24,930 → 24,648 (-282) | 25,465 → 24,278 (-1,187) | - | 21/3 → 16/3 | 8 | estimate -2.059 → -0.743 |
| Standalone 8x8 | 32,584 → 32,154 (-430) | 34,211 → 32,858 (-1,353) | - | 26/5 → 21/5 | 8 | estimate -2.161 → -2.153 |

- **Route status:** routable nets 107,053 → 105,954, all fully routed, 0 routing errors at both. Global-iteration markers in the logs are 14 → 4 lines, consistent with the PR's "seven … two" iterations.
- **Per sub-block** (hierarchy reports; LUT (LUTRAM) / FF / RAMB36):
  - **Top's own logic `(u_pp)`:** route 390 (0) → 654 (218), FF 2,968 → 1,972. 1x1: 447 (0) → 769 (246), FF 3,167 → 2,034. 8x8: 465 (0) → 880 (256), FF 4,735 → 3,433.
  - **`u_listener`:** route 1,301 (0) → 1,496 (208), FF 1,106 → 1,055, RAMB36 5 → 0. 1x1: 1,434 → 1,557 (208), FF 1,106 → 1,051. 8x8: 1,630 → 1,668 (208), FF 1,128 → 1,079. So lever 6 costs +38 to +195 LUTs, as stated.
  - **Face engines at 1x1:** `u_notify` -201, `u_originator` -136, `u_adp` -109, `u_maap` -87 and `u_srp` -87 sum to the PR's -620.
  - **Wrapper `pp_shadow`, routed:** 24,485 (1,152) → 24,516 (1,578), FF 24,267 → 23,221, so +31 LUT and -1,046 FF.
  - **Census arithmetic:** 54 RAM32M + 1 RAM32X1D = 218 LUTRAM for the routed rings; 52 RAM32M = 208 for the records.
- **Gate** (`pp_resource_gate.py`, tolerances from the baseline at `fea346e7`).
  - **Head against base:** no regression on any endpoint. Improvements beyond tolerance, so "re-baseline recommended":
    - route: FF and RAMB36;
    - standalone 1x1 and 8x8: LUT, FF and RAMB36.
  - **Against the committed record (dev C):**
    - route: base LUT +667 > 500 (exit 1); head +385 (exit 0).
    - standalone 1x1: base LUT +598 and head +316, against 250.
    - standalone 8x8: base +1,028 and head +598, against 316.

    Both base and head exit 1 on the standalone endpoints. This matches HANDOFF §5.6 and is why the parent adoption must re-record the baseline (§7).
- **Measured revision:** base is processor `5c71928a`; head is processor `9eebc61`. `9eebc61`'s `protocol_processor_top.sv` (`ada29e74…`) and `KL_pp_acmp_listener.sv` (`f8bc590e…`) are byte-identical to the exact head's. The runs do not print a processor revision themselves. The mapping lines tie each run to its RTL: at head, `g_armq` and `rec_ram` map to RAM32M; at base, no ring and READ_FIRST block RAM. The merged main content (PR #152 comments, PR #153's notify) is outside both measurements by design.

## 5. Executed evidence (this reviewer)

### 5.1 Arm-port lockstep, independent re-implementation

Scripts: `scripts/armq_lockstep/{extract.py,armq_ls.sv,bench.cpp,run.sh,summarize.py}`.

- **Extraction.** The block is cut byte for byte from each top. It runs from the `// ====` line above "timer arm-port priority mux (banner)" to the line before the one above "PRNG draw-port owner mux (banner)". Block sha256: main `5ef541f1…`, head `d36e67ec…`.
- **Wrapping.** Each block is wrapped with the eight faces as inputs and the port and drop counter as outputs.
- **Stimulus.** Identical random arms go into both every clock, in phases: saturation, single face, drain, random rates, and long 70k-100k clock saturation to reach the counter's ceiling. Unreset state starts random, with random mid-run resets.
- **Comparison.** Outputs are compared after both edges. Both blocks are also graded against an independent eight-FIFO model.

| Configuration | Runs x cycles (slot widths 5, 6 = 1x1, 7 = 8x8, 8) | Lockstep mismatches | Model mismatches | Coverage |
|---|---|---|---|---|
| golden | 32 x 1,000,000 | **0** | 0 | 27,788,178 arms; 101,852,993 offers to a full face; 5,074,588 full-queue pop-and-push clocks; 8,332,452 counter rises; 21,017,132 saturated clocks; 441 reset-asserted clocks |
| golden soak | 32 x 10,000,000 | **0** | 0 | 277,041,909 arms; 1,035,983,245 offers to full; 49,192,161 full pop-and-push; 69,879,662 rises; 3,202 reset-asserted clocks |

The author's six controls and my four were planted in the head's block. Each is caught in 32 of 32 runs:

| Control | Mismatching clocks (32 x 1M) |
|---|---|
| `wr_at_head` | 23,584,759 |
| `wr_at_mid` | 24,514,073 |
| `head_stuck` | 28,212,070 |
| `read_tail` | 26,297,656 |
| `write_refused` | 1,487,206 |
| `ring_of_three` | 16,412,026 |
| `read_write_first` (own: write-first read of the overwritten head) | 5,074,588 |
| `full_pop_refuses` (own) | 11,619,340 |
| `drop_wraps` (own) | 21,016,825 |

The probe `probe_head_unreset` gives 0 mismatches (equivalent). Receipts: `receipts/armq/*/results.txt`, `receipts/armq/summary.txt`.

### 5.2 Listener lockstep, independent re-implementation

Scripts: `scripts/lsn_lockstep/{gen_wrap.py,bench.cpp,mutate.py,run.sh,summarize.py}`.

- **Setup.** Main's `KL_pp_acmp_listener` is renamed `_ref` and placed beside the head's. Every input is shared, and all 47 outputs plus `xs_r` are compared after every evaluation.
- **Inputs match the author's bench.** The renamed main listener's sha256 `7f6bed96…3292f`, the head's `f8bc590e…fec57fc` and the ROM `23cc67ee…` equal the hashes the author's HANDOFF records.
- **Emulated faces:** RX slots with sync read and free, the TX grant, the PRNG, a timer service that fires the armed deadlines, TK events, preloads, started/stopped requests and lock.
- **Settles.** The bench snoops the reference's own PROBE_TX commands and answers about 55 % of them with a matching PROBE_TX_RESPONSE, so streams settle.
- **Comparison window.** Comparison starts at the first reset edge, as section AQ does.

| Configuration | Runs x cycles (N_SINKS_P 1, 2 = 1x1, 3, 8, 9 = 8x8) | Mismatches | Coverage |
|---|---|---|---|
| golden | 40 x 1,000,000 | **0** | 716,275 txns; 537,296 X_LATCH and 331,428 X_STRT_AP record reads; 554,174 record writes; 47,552 probe responses; 25,872 settles; 19,826 expiries; 689 reset-asserted clocks |
| golden soak | 40 x 10,000,000 | **0** | 5,361,546 X_LATCH; 3,297,023 X_STRT_AP; 5,519,607 writes; 257,964 settles; 196,677 expiries; 5,369 reset-asserted clocks |

Controls, runs caught out of 40:

| Control | Runs caught | Note |
|---|---|---|
| `read_sampled_in_idle` | 40 of 40 | |
| `started_bit_unstored` | 40 of 40 | |
| `read_sink_zero` | 32 of 40 | the 8 missed runs are N = 1, where it is equivalent |
| `sweep_misaddressed` | 32 of 40 | the 8 missed runs are N = 1, where it is equivalent |
| `settled_vlan_bit_unstored` | 33 of 40 | caught at every N; seed-dependent, because the bit's value in a settled VLAN is random |

The two equivalence probes, `probe_write_first_bypass` and `probe_read_on_write_addr`, give 0 mismatches. They confirm that no record is written in a consuming cycle and that the write address equals `sink_r` outside X_INIT. Receipts: `receipts/lsn/*`.

### 5.3 Committed checks, campaigns and gates

Each ran on a `git archive` of the head, with the pinned simulator. All rc 0.

| Command | Tree | Result |
|---|---|---|
| `tb/acmp_listener` `make run` | head; head's tb on main's RTL (`c050d971` hdl, verified equal) | 3,111 of 3,111 PASS at both (RS included) |
| `tb/pp_top` `make gsi-build && ./obj_dir/Vpp_top_sim --arm-queue-only` | head; head's tb on main's RTL | `AQ: 2 checks, 0 failures` at both; coverage identical: 71,258,305 edges, 8,270 arms, 28 two-face clocks, 4,288 pass-through pushes, 0 deep, 0 fills, 0 drop clocks |
| `tb/pp_top` `make` (full five-build suite) | head | 10,418 of 10,418 PASS; AQ in the default run: 71,290,136 edges, 8,280 arms, 4,291 pass-through, zeros as recorded |
| `tb/pp_top/acmp_mutants.py --jobs 4` | head | 29 of 29 KILLED, four goldens PASS. Every arm's failing count equals its README record: the 14 `pp_top` arms of 43; the four earlier listener arms 93, 50, 40, 30; the issue #639 arms 645 of 3,080, 1, 91, 25, 37 of 3,111 and AQ-run counts 71, 2, 11, 2, 2 (`receipts/campaigns/acmp/`) |
| `tb/adp_engine/mutants.py --jobs 3` | head and main `c050d971` | both: 2 controls PASS, 41 KILLED; verdict lines identical. `cfg-valid-no-reset` fails 9 and `gate-enable-dropped-top` 7, with identical FAIL lines at both, so they are lane-independent. The README rows (5; 3) already note 9 and 7 in their text |
| two full-path controls in the committed AQ (`read_write_first`, `full_pop_refuses`) | head + plant | survive: `AQ: 2 checks, 0 failures` (S1) |
| `scripts/lint_hdl.sh`, `scripts/gen_matrix.py --check`, `make check` | head | 41 of 41; 94 rows, 0 untested; all gates OK |
| clone integrity after all work | review clone | HEAD, tree and index tree `8c983973…`; 0 porcelain lines including ignored; no gitlinks, and the processor repo has none (`receipts/clone_integrity.txt`) |

**Hosted, observed only (read-only, `receipts/gh/check_runs.tsv`).** At the exact head, `docs-gates` and `portability` completed with success in two workflow runs. `suites` was in progress in both at review time.

## 6. Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | issue #639 body and assignment; PR body; port lists of both modules in the diff; both lockstep benches (§5.1, §5.2); snapshot word 24 rule; closing keyword vs parent baseline location | R463-1 | 9e8699105c126db7764820916a827ef0538bc4b2 |
| RTL | CLEAN | `hdl/top/protocol_processor_top.sv:2925-3043`; `hdl/acmp/KL_pp_acmp_listener.sv:381-412, 744-770, 940-1074`; published synthesis mapping lines; route timing and hold path; lint 41/41 | R463-1 | 9e8699105c126db7764820916a827ef0538bc4b2 |
| Robustness | CLEAN | unreset RAM with random initial state and mid-run resets (both benches); drop-counter saturation; full pop-and-push overwrite; out-of-range sink guards; head-unreset probe | R463-1 | 9e8699105c126db7764820916a827ef0538bc4b2 |
| Tests | CLEAN (S1) | AQ and RS at head and on main's RTL; full `tb/pp_top`; `tb/acmp_listener`; ACMP campaign at record; ADP campaign head vs main; 19 lockstep controls and probes; 2 committed-AQ survivals | R463-1 | 9e8699105c126db7764820916a827ef0538bc4b2 |
| Docs | CLEAN (F1 RESIDUE) | both suite READMEs; 07 §6; 08 §3; 09 §8.8; HDL guide §3.1; RTL comments; PR body and HANDOFF figures against receipts; `make check`, `gen_matrix --check` | R463-1 | 9e8699105c126db7764820916a827ef0538bc4b2 |

## 7. Real limits and pending manager duties

**Limits**

- **Not run by me, as scope excludes it:**
  - `scripts/run_suites.sh` as a whole, `syn/yosys/run.sh`, the parent consumer set, and the builder or gPTP banks;
  - the Vivado runs themselves. The figures are re-derived from the published reports, not re-synthesised.
- **Campaigns not re-run:** notify, ctr, aecp, aecp_dispatch, d3, gsi, name_wr and maap. They are covered by the structural argument and the two lockstep benches. No mutation driver in the tree references text this lane removed (grep for `armq`, `rec_rdata_r`, `arm_drop_r`, `armq_mid_w` finds only `acmp_mutants.py`). Their recorded counts at this head rest on the author's runs and the manager's banks.
- **Manager bank receipts not found.** The manager's source, builder and native bank receipts at this head are said to be public. I did not find them in `review-evidence/pp639-r1` at `28663f5a` (the tip of `pp639-review-evidence`), and I did not use them.
- **The author's lockstep benches are unpublished, and I did not see them.** §5.1 and §5.2 are independent re-implementations. Lockstep is finite random simulation supporting the structural arguments in §3.2, not a formal proof. The listener bench's stimulus is my own emulation, with the coverage stated.
- **Concurrency.**
  - The twelve arm-lockstep configurations ran concurrently. Their simulator builds each used two compile threads, so for a few seconds at build time compile processes may have exceeded 16.
  - The ACMP campaign used `--jobs 4` while the suite Makefile's `-j 0` set each build's threads.
  - No Vivado ran.
- **No hardware.** Physical calibration was NOT RUN. No hardware or field evidence was used.

**Pending manager duties**

1. **Parent consumer set** of 17 at dev `fea346e76c2a57ed5cd131af8fc68dfeff57f877`, with the c8, p2-p1, c10 and 232 patches and this head. Gate 16 should now pass, since #643 is fixed at `fea346e7`. The author's run was at `241f9184`, where gate 16 failed identically at main.
2. **Re-record the gate baseline** in the parent adoption that moves the pin (#639 acceptance). Against the committed record, the head's standalone LUT exceeds tolerance (+316 > 250 at 1x1, +598 > 316 at 8x8). The gate recommends re-baselining on all three endpoints.
3. **Bank PR #153's xvlog finding** in the parent when the pin moves past `c050d971`, as the author notes.
4. **Hosted acceptance.** `suites` was still in progress at review time. The final current-dev candidate build happens at the merge turn: source base `5c71928a`, live dev `fea346e7`.
5. **Carry F1** to the residue checklist.

## 8. Reproduce

```sh
P=$REVIEWS/pp639-r463-1-packet; R=<processor clone at 9e869910>
bash $P/scripts/armq_lockstep/run.sh $R OUT_A            # optional 3rd arg: a control name from extract.py
bash $P/scripts/lsn_lockstep/run.sh  $R OUT_L            # optional 3rd arg: a control name from mutate.py
python3 $P/scripts/armq_lockstep/summarize.py OUT_A; python3 $P/scripts/lsn_lockstep/summarize.py OUT_L
python3 $P/scripts/vivado_rederive.py <milan-fpga 28663f5a>/review-evidence/pp639-r1 <milan-fpga fea346e7>/syn/ooc/pp_resource_baseline.json
```

`VERILATOR` overrides the simulator path, and `CYCLES` sets the cycles per run (default 1,000,000). Published build logs have the simulator's host install path replaced by `<PINNED_VERILATOR_ROOT>`. `receipts/REDACTED_PATHS.txt` lists the files where that was done.

R463-1 FINISHED
