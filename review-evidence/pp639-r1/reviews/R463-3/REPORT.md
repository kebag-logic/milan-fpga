[R463] POSITIVE - exact head c725be12d7ea6bf96f1b64e3a56416f0d4defd6c

# R463-3: external independent review of processor PR #155 (milan-fpga #639), round 2b

- **Head:** `c725be12d7ea6bf96f1b64e3a56416f0d4defd6c`, tree `0bb7199a3caf38df44071cac4e2d56fef89f1b7c`. Both were checked in the detached clone.
- **Source base:** `5c71928ad2bf1a854a5538d69b77214dfdf1697f`. The lane-only delta was read against processor `main` `b0a74196`, which is the head's second parent.
- **Scope:** derived from the issue's frozen acceptance and the manager's assignment comments, as set out in §1.
- **Verdict:** POSITIVE. No BLOCKER, MAJOR or MINOR is open. There is one new SUGGESTION. Three earlier items are retained: one RESIDUE and two SUGGESTIONs. All five lenses are CLEAN.

## 1. Scope reconstructed

The repository has no AGENTS.md or CONTRIBUTING.md. The authorities read were `README.md`, `docs/README.md` (single-source rules and editing workflow), `docs/guides/hdl-engineer.md` §2 and §3.1, and issue #639 with the manager's comments 5976100204, 5981052216 and 5983576287.

The acceptance, the rules and how this head meets each:

| Item | Source | At this head |
|---|---|---|
| Lever 3: the timer arm-port queues; lever 6: the listener records | issue body | Both are changed. The eight shift queues are now 4-entry distributed-RAM rings (`protocol_processor_top.sv:3004-3029`). The records are now distributed RAM with no read register (`KL_pp_acmp_listener.sv:382-396`, `:746`). |
| Each lever measured before and after with the #234 recipe | issue body | The published Vivado reports (evidence `author-r1/vivado/`) match every figure in the PR body (§3). |
| No lost function: every suite and campaign that reads the block still passes, at the same counts | issue body | `tb/pp_top` and `tb/acmp_listener` pass. The acmp, notify and AECP-TD campaigns pass at their recorded counts (§3). |
| Gate baseline re-recorded "in the same reviewed change" | issue body | Not in this PR. The baseline file lives in the parent, so the PR says "Relates to milan-fpga#639" and leaves the issue open for the pin adoption. This is a pending manager duty (§7), not a defect of this PR. |
| No port, parameter or register change without a STOP | issue body; 5976100204 | Met. The lane's `hdl/` diff touches no `input`, `output`, `parameter` or `localparam` line. Snapshot word 24 is unchanged. |
| No protocol-visible timing change; equivalence proven | 5976100204 | Met. The cycle-level argument is in §2 (RTL). AQ and RS pass on `main`'s RTL, and AQ's coverage there is identical to the digit. |
| Round 2b: merge `main` `b0a74196`; the union of both sides' records | 5983576287 | Met. `tb/pp_top` reads 10,435 checks = 9,947 + 20 + 178 + 231 + 56 + 3. HZ is 189. TD passes, and its TD arms are KILLED over the rings. |

## 2. Lenses

### Conformance: CLEAN
- **Ports and parameters.** `git diff b0a7419..HEAD -- hdl/` has no port, parameter or localparam line (`receipts/logs/`).
- **The arm port's contract.** The ring keeps the 4-entry depth, the fixed drain order and per-face order. It still drops the newest arm on overrun, and the counter still saturates at 0xFFFF and counts one per clock. Two of my probes confirm the grading of this contract: reversing the drain priority fails AQ2 and AQ3, and counting a two-face drop as two fails AQ3.
- **Records.** The record layout (F07.6) and the X_INIT sweep are unchanged.
- **Docs authority.** The new 08 §3 bullet carries no timing value, so the F08.1 single-source rule holds.

### RTL: CLEAN
- **The rings.** A push writes at `hd + cnt[1:0]`.
  - Without a pop, that is the slot after the survivors.
  - With a pop and `cnt < 4`, it equals `(hd+1) + mid`, so it is the same slot.
  - With a pop and `cnt == 4`, the index wraps to `hd`. The asynchronous read has already taken the leaving head, and the write lands at the edge.
  - A full face without a pop has `push_ok = 0`, so nothing is written.
  - Reset clears `hd` and `cnt`. A write taken during reset is unreadable until it is overwritten, so the unreset entries cannot be observed.
- **The listener.** `rec_rd_w` is consumed only in X_LATCH and X_STRT_AP (`:1050-1080`). Those states are entered only from X_RDREC and X_STRT_RD (`:1034`, `:1067`), whose cycles write no record: `recwr_en_w` is set only in X_INIT, X_PRELOAD and X_WB. `sink_r` changes only in X_IDLE. So the combinational read returns what the removed register sampled one edge earlier. No hierarchical reference to `rec_rdata_r` or `armq_r` remains in the tree.
- **Lint.** Both changed tops lint at 0 warnings with Verilator 5.050 (`receipts/logs/lint-focused.log`).
- **Mapping.** The published synthesis logs show `g_armq[k].mem_r_reg … 4 x 47 … RAM32M x 8`, and the base's `rec_ram_r` in block RAM.

### Robustness: CLEAN
- **Reset.** The head index is unreset-equivalent: probe `aq_hd_not_reset` passes AQ 4/4 with identical coverage. A reset taken with arms queued and offered is graded by AQ3 and reached by AQ4 (36 such resets, 366 arms offered).
- **Saturation and overrun.** Covered by `armq_drop_skip_sat` (KILLED) and by my two-face drop probe (fails AQ3).
- **Records.** RS grades the record RAM's only reset, read back through the RAM, and passes on `main`'s listener (`lsn_main_rtl`, 3,111/0).
- **Timing.** The route at 1x1 and 50 MHz has 0 routing errors and WNS/WHS +0.093/+0.036 ns.
- **One gap**, carried as S1: the ring's data path is never exercised above deadline bit 19.

### Tests: CLEAN (S1 SUGGESTION)
- **Suites.**
  - `make -C tb/pp_top` at the head: `10435 checks: 10435 PASS, 0 FAIL` (13 min).
  - `make -C tb/acmp_listener`: `3111 checks: 3111 PASS, 0 FAIL`.
- **ACMP campaign** (`acmp_mutants.py`, `--jobs 3`): 33 of 33 KILLED and the four goldens PASS. Every issue #639 arm fails exactly its recorded count:
  - `rec_*`: 645/3080, 1, 91, 25 and 37;
  - `armq_*`: 72, 3, 12, 3, 3, 1, 1, 1 and 1.
  - The four older listener controls fail 93/3111 and 50, 40 and 30 of 3107, as recorded.
- **Notify campaign:** 47 of 47 KILLED and the goldens PASS.
- **AECP TD arms over the rings:** the timer-defaults control PASSES. `td-lock-default-59s` and `td-tl-default-301s` are KILLED by TD1 and TD2.
- **AQ coverage** reproduces the README to the digit:
  - traffic: 71,258,305 edges and 8,270 arms;
  - the drive: 90,172 edges and 88,003 arms; pushes onto faces holding 0 to 4 arms of 18,778, 48,239, 3,636, 5,594 and 12,481; 352,294 refused arms in 80,719 drop clocks, 78,930 of them with several faces dropping; 4,096 drop clocks with the counter saturated.
  - AQ on `main`'s top gives the same figures.
- **Reviewer probes** (`probes.py`; results in `receipts/probes/`, `receipts/summary.txt`):

  | Probe | Result |
  |---|---|
  | cancel bit unstored | fails AQ2 and AQ3 |
  | deadline bit 0 unstored | fails AQ2 and AQ3 |
  | priority reversed | fails AQ2 and AQ3 |
  | faces 6 and 7 dropping together count two | fails AQ3 |
  | head index unreset (equivalent) | passes |
  | AQ on `main`'s top | passes |
  | RS on `main`'s listener | passes |
  | **deadline bit 21, 22 or 31 unstored** | **passes AQ 4/4 (S1)** |

  - `aq_drop_per_face` (faces 0 and 7) passes because it is equivalent: face 0 drains first every clock, so it can never hold two arms.
  - `lsn_rec_bit367_unstored` is informational. It passes because handle bit 7 is never set at the shipped shapes.

### Docs: CLEAN
- **Checked against the RTL and against my runs:**
  - 07 §6, 08 §3, 09 §8.8 and `hdl-engineer.md` §3.1 (`:96-106`; the guide's claims about `KL_aecp_ucpu` `rf_r`, the rings and the records match `ram_style` at `:159`, `:3019` and `:395`);
  - `tb/pp_top/README.md` section AQ (`:2022-`) and the ACMP controls paragraph;
  - `tb/acmp_listener/README.md` (3,111; RS; five controls);
  - the PR body's figures and its "How to validate" expectations.
- **Gates.** `make check` reports 41 mermaid and 18 wavedrom blocks, 1,136 links, 115 REQ rows, 94 matrix rows with 0 untested, and 28 parameters. `gen_matrix --check` passes. Both rc 0.
- **The PR body's opening** (`main` merged four times; thirteen commits; head `c725be12`) matches `git log --first-parent` and the PR's 13 commits.

## 3. Area evidence (published, round 1; RTL comment-only and merge-only since)

All figures match the published reports at milan-fpga `pp639-review-evidence` `36304086`, `review-evidence/pp639-r1/author-r1/vivado/`:

| Endpoint | LUT | FF | RAMB36 | Notes |
|---|---|---|---|---|
| Route, base -> head | 51,434 -> 51,152 | 59,691 -> 58,598 | 79 -> 74 | Block RAM tiles 92.5 -> 87.5; 0 routing errors in both |
| Standalone 1x1, base -> head | 24,930 -> 24,648 | 25,465 -> 24,278 | 21 -> 16 | |
| Standalone 8x8, base -> head | 32,584 -> 32,154 | 34,211 -> 32,858 | 26 -> 21 | |

Per sub-block at 1x1:
- the top's own logic: 447/3,167 -> 769/2,034 (LUT/FF), with 246 LUTRAM;
- the listener: 1,434 -> 1,557 LUT and 5 -> 0 RAMB36.

The head measured was processor `9eebc61`. The lane's `hdl/` has changed only by a comment since then (`2ff8183`). The merged `main` RTL belongs to other lanes. The adoption re-measures its own pin.

## 4. Findings

| ID | Severity | Lenses | Where | Authority / evidence | Impact | Required outcome | Verification |
|---|---|---|---|---|---|---|---|
| R463-3-S1 | SUGGESTION | Tests, Robustness | `tb/pp_top/sim_main.cpp:13916` (`dbg_aq_drv_deadline_i[k] = ++serial`) | The drive's serial stays below 2^20 (90,172 edges x 8 faces). The traffic phase's deadlines do not reach bit 21 either. Probes that drop deadline bit 21, 22 or 31 from the ring store pass AQ 4/4 and the whole `--arm-queue-only` run (`receipts/probes/aq_deadline_bit{21,22,31}_unstored.json`). Bit 0 and the cancel bit are caught. | None at this head. The ring stores whole words, and narrowing it fails zero-tolerance lint: `receipts/logs/lintprobe-ring-narrowed.log`, 2 width warnings, rc 1. A masked store of a high deadline bit, however, would mis-arm every timer once uptime passes 2^20 ms (about 17 min), and no committed check would see it. | Optional: draw the deadline's high bits at random per arm, for example `(rng() << 20) ^ serial`. The serial in the low bits still identifies each arm. | The three `aq_deadline_bit*` probes in `probes.py` then fail AQ3. |

## 5. Prior public findings at this head

I read these only after my own pass, verdict and ledger were written (`receipts/own-pass-before-prior-findings.md`).

| Prior finding | Severity | Status at `c725be12` | Evidence |
|---|---|---|---|
| R462-1 F1: no committed check of the rings' full-queue path | MINOR | RESOLVED (holds) | Section AQ is unchanged by the round-2b merge (`git diff 1cba30c..HEAD`: no AQ hunk). `armq_write_refused`, `armq_write_wrap_hi`, `armq_full_pop_refuses` and `armq_drop_skip_sat` are KILLED by AQ3 in my campaign, and AQ4's reach is reproduced. |
| R462-1 S1: name the source of "1,153 flops" | SUGGESTION | RESOLVED | Banner at `protocol_processor_top.sv:3012-3014`. |
| R463-1 F1: 09 §8.8 pointed at benches "recorded in the pull request" | RESIDUE | RESOLVED | 09 §8.8 (`:392-403`) cites only in-tree checks. |
| R463-1 S1: ring defects passing every committed check | SUGGESTION | RESOLVED | Same four KILLED arms as R462-1 F1. |
| R462-2 R1: PR body opening described an older head | RESIDUE | RESOLVED | The body now says `main` was merged four times, with thirteen commits, head `c725be12`. This matches the history. |
| R463-2-R1: the evidence `author-r2/lockstep/README.md` gives `sha256sum -c GENERATED.sha256` (a three-column file) and runs `build.sh`, which is published as mode 100644 | RESIDUE | RETAINED | Unchanged at evidence tip `36304086` (README lines 42, 44, 79, 81; both `build.sh` at mode 100644). Exact fix as R463-2 states: `awk '{print $1"  "$3}' GENERATED.sha256 \| sha256sum -c`, and `chmod +x build.sh` before `sh run_matrix.sh again`. Evidence wording only; for the manager's residue checklist. |
| R463-2-S1: publish the base 1x1 `armq_r` census behind "1,152" | SUGGESTION | RETAINED (optional) | The evidence tip holds no cell census. |
| R463-2-S2: report or require per-face reach in AQ4 | SUGGESTION | RETAINED (optional) | `sim_main.cpp:13984` still checks reach summed over faces. |

## 6. Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | issue #639 body; assignments 5976100204, 5981052216, 5983576287; the lane's `hdl/` diff for port/parameter lines; drain order, depth, drop and saturation rule (probes); PR keyword vs the parent baseline | R463-3 | c725be12d7ea6bf96f1b64e3a56416f0d4defd6c |
| RTL | CLEAN | `protocol_processor_top.sv:2935-3060`; `KL_pp_acmp_listener.sv:382-412, 743-770, 940-1080`; every write-enable and `sink_r` assignment; lint of both tops; published synthesis mapping lines | R463-3 | c725be12d7ea6bf96f1b64e3a56416f0d4defd6c |
| Robustness | CLEAN | reset paths (head unreset probe, AQ3/AQ4 reset reach, RS on head and main); saturation; full pop+push; 1x1 route status and timing; ring-narrowing lint probe | R463-3 | c725be12d7ea6bf96f1b64e3a56416f0d4defd6c |
| Tests | CLEAN (S1 SUGGESTION) | `tb/pp_top` six builds 10,435/0; `tb/acmp_listener` 3,111/0; acmp 33/33 + 4 goldens, every #639 arm at its record; notify 47/47; AECP TD control + 2 arms; 14 reviewer probes; AQ and RS on `main` RTL | R463-3 | c725be12d7ea6bf96f1b64e3a56416f0d4defd6c |
| Docs | CLEAN | 07 §6; 08 §3; 09 §8.8; HDL guide §3.1; `tb/pp_top/README.md` AQ and ACMP controls; `tb/acmp_listener/README.md`; RTL comments; PR body vs history and receipts; `make check`, `gen_matrix --check` | R463-3 | c725be12d7ea6bf96f1b64e3a56416f0d4defd6c |

## 7. Limits and pending manager duties

**Limits:**
- Not run: `run_suites.sh` and the other campaigns (ctr, aecp in full, aecp_dispatch, d3, gsi, name_wr, adp, maap). Neither were Yosys, the parent consumer set, the builder, Docker/act or any Vivado run, because these are bank runs outside this review's allowance. For them I rely on the manager's published banks at this head.
- Physical calibration: NOT RUN. No hardware was used. Field skips are not hardware proof.
- The area figures are the author's round-1 Vivado receipts at processor `9eebc61`, re-read, not re-run. The 8x8 endpoints are post-synthesis estimates. Only 1x1 was routed.
- I did not re-run the published lockstep benches in this round.

**Hosted CI at the exact head:** observed at 2026-10-04 22:16 UTC (`receipts/hosted-status.txt`).
- `docs-gates` and `portability`: completed and successful, for both the push and the pull_request events.
- `suites`: still in progress for both events (runs 37236793012 and 37236796378). No hosted suite verdict was available to this review.

**Pending manager duties:**
- Hosted and act acceptance, including the in-progress `suites` jobs.
- The final current-dev candidate on live dev `6c22d3ca`.
- The parent pin adoption, which must re-record the resource gate's baseline. That is issue #639's third acceptance item, and the reason the PR says "Relates".
- Carrying R463-2-R1 to the residue checklist.

**Clone integrity:** the clone was never edited. All probes ran on extracts under `scratch/`.
- 558 tracked blobs hashed from the work tree: 0 mismatches.
- Modes: 543 at 100644 and 15 at 100755, with 0 work-tree mode mismatches.
- The index digest is identical before and after.
- `git status --porcelain --ignored` is empty.
- There are no submodule gitlinks (mode 160000) in this repository.
- Receipt: `receipts/clone-integrity.txt`.

**Reproduction:** `sh run.sh CLONE OUT VERILATOR` with Verilator 5.050 (identity verified as `Verilator 5.050 2026-07-01 rev v5.050`). Then run `python3 summarize.py OUT`. Local paths in the published logs are redacted. `receipts/REDACTION.txt` lists the substitutions and each file's original digest.

R463-3 FINISHED
