[R462] POSITIVE - exact head c725be12d7ea6bf96f1b64e3a56416f0d4defd6c

# R462-3: internal independent review of processor PR #155 / milan-fpga #639, round 3 (merge of `main` `b0a74196`)

- **Exact head:** `c725be12d7ea6bf96f1b64e3a56416f0d4defd6c`, tree `0bb7199a3caf38df44071cac4e2d56fef89f1b7c`, in a detached clone. The PR's `headRefOid` on GitHub is the same commit.
- **Source base:** `5c71928ad2bf1a854a5538d69b77214dfdf1697f`. Processor `main` at this round is `b0a74196` (PR #157).
- **Verdict: POSITIVE.**
  - There is no open BLOCKER, MAJOR or MINOR.
  - One new RESIDUE (R1), a wording slip in a README. One new SUGGESTION (S1).
  - Every prior public finding is resolved, or is carried as a residue or suggestion that does not block (see "Prior public findings").
- **Order of work:**
  1. Scope was reconstructed from the issue body, the manager's assignment comments and the author's REVIEW READY comments.
  2. Then the RTL, test and doc diff, and the history.
  3. Then my own runs and probes.
  4. Prior public review findings were read only after that pass.

## 1. Scope, from the frozen acceptance

These come from issue #639's body, plus the assignment comments 5976100204, 5981052216 and 5983576287:

| # | Acceptance / scope rule | Status at this head |
|---|---|---|
| A1 | Lever 3 (`armq_r`, the top's timer arm-port queues) and lever 6 (`rec_ram_r`, the listener records, 5 RAMB36) are each measured before and after with the #234 recipe | **Met for the PR** (Section 3, Conformance). The published Vivado reports match the PR body figure for figure. The lane RTL at this head is byte-identical to the measured `9eebc61` except one comment. |
| A2 | No lost function: every suite and campaign that reads the blocks passes at the same counts | **Met.** Pre-existing counts are unchanged. The added checks (RS +123, AQ +4) account for every count that moved. |
| A3 | The resource gate's baseline is re-recorded in the same reviewed change | **Not in this PR, by a public decision.** The gate's baseline lives in the parent. The PR therefore says "Relates to milan-fpga#639", not "Closes", as the assignment allows. This is a pending manager duty at adoption (Section 7). |
| A4 | No port, parameter or register change, and no protocol-visible timing change, without a STOP | **Met.** `git diff b0a74196 c725be1 -- hdl/` touches only the two files, with no `input`, `output`, `inout` or `parameter` line. Snapshot word 24 still reads `{arm_drop_r, mrp_drop_w}` (`protocol_processor_top.sv:4774`). The cycle behaviour is identical (Section 3, RTL). |
| A5 | Touch only the top's arm-queue logic and the listener-record storage | **Met.** The main..head `hdl/` delta is `protocol_processor_top.sv:2962-3058` (the arm mux) and `KL_pp_acmp_listener.sv:381-413, 746, 1034, 1067, 1072` (the record RAM). |
| A6 | Round 2b: merge `main` `b0a74196` `--no-ff`, resolve nothing silently, re-run the affected gates, and keep the docs agreeing | **Met.** `git merge-tree --write-tree 1cba30c9 b0a74196` = `0bb7199a`, the head tree. Lane RTL vs `1cba30c` differs only by #157's classifier hunk. My runs reproduce the union counts (Section 3, Tests). |

## 2. Findings

| ID | Severity | Lenses | Where | Authority / evidence | Impact | Required outcome | Verification |
|---|---|---|---|---|---|---|---|
| R1 | RESIDUE | Docs | `tb/pp_top/README.md:2038` (section AQ) | It reads "Every harness model runs the model at every clock edge from its first reset (`ArmQueueModel`, in `H::step`)". `sim_main.cpp:1539-1542` shows each harness `H` stepping its own `aq` model, so "harness model" is a slip for "harness". | Wording only. No figure, check, count or claim changes. | Exact fix: replace "Every harness model runs the model" with "Every harness runs the model". | Read the sentence after the edit. |
| S1 | SUGGESTION | Docs | `docs/guides/hdl-engineer.md:96-101` | The paragraph gives the reason for an asynchronous read as "because their consumer needs the entry in the cycle it asks", and lists the listener records under it. Its next sentence says the listener walk still spends its read-issue state. For the records, the reason is shedding the read register so that the memory fits distributed RAM (`KL_pp_acmp_listener.sv:386-394`). | None. The following sentence gives the true timing. | Optional: say that the listener records are read asynchronously to drop the read register, not because their consumer needs the entry in the same cycle. | Read §3.1. |

There is no other finding.

## 3. Lenses

### Conformance: CLEAN

- **Lever figures (A1).** I fetched the published reports read-only from milan-fpga `28663f5a`, `review-evidence/pp639-r1/author-r1/vivado/{base,head}/{route-1x1,ooc-1x1,ooc-8x8}`. Extract: `receipts/vivado-figures-extract.txt`.

  | Endpoint | LUT | FF | RAMB36 | RAMB18 | Other |
  |---|---|---|---|---|---|
  | Route | 51,434 -> 51,152 | 59,691 -> 58,598 | 79 -> 74 | 27 / 27 | Slice 15,847 -> 15,803; 0 nets with routing errors in both |
  | Standalone 1x1 | 24,930 -> 24,648 | 25,465 -> 24,278 | 21 -> 16 | 3 / 3 | |
  | Standalone 8x8 | 32,584 -> 32,154 | 34,211 -> 32,858 | 26 -> 21 | 5 / 5 | |

  Each figure equals the PR body's table.
- **The measured RTL is the RTL under review.**
  - I compared the `hdl/` change lines of `5c71928a..9eebc61` (the measured head) with those of `b0a74196..c725be1`.
  - They are identical except the ring banner comment (`protocol_processor_top.sv:3012-3014`, R462-1 S1, comment only).
  - The round-2b merge brings in only PR #157's GET_DYNAMIC_INFO classifier hunk, outside both levers. So the lever figures stand without a new Vivado run, as the round-2b assignment states.
- **Widths.** `ARM_W_C = 1 + TMR_AW_C + 8 + 32` is 47 at 1x1 and 48 at 8x8. This matches the reported `4 x 47` and `4 x 48` RAM32M mappings. The banner's "1,152 flops" is a post-optimisation census, which is below 8 x 4 x 47 = 1,504 RTL bits.
- **The 100 MHz criterion is judged at the declared 50 MHz (#565).** The routed head meets 50 MHz (WNS/WHS +0.093/+0.036 ns per the PR, from the published sign-off set). No protocol timer value or ordering changes.
- **No Milan or IEEE clause claim changes.** The arm drain order, the per-face order, drop-newest and the saturating counter are the banner's contract (`protocol_processor_top.sv:2937-2944`), unchanged.

### RTL: CLEAN

**Arm-port rings** (`protocol_processor_top.sv:2987-3058`):
- **Write index.** It is `hd + cnt[1:0]` (`:3023`). For `cnt < 4` this is the slot after the survivors, whether or not the face pops: the shift queue's `mid` relative to the advanced head. For `cnt == 4` a push is accepted only with a pop (`push_ok` tests `mid != 4`, `:3000`), and `cnt[1:0] = 0` writes the leaving head. The read is asynchronous (`:3029`) and the port captures it at the same edge (`:3046-3047`), so the overwrite is read-before-write, as in the shift queue.
- **Head index.** `hd` advances only on a pop (`:3049`). `cnt` is updated exactly as before (`:3054-3055`).
- **Reset.** Reset clears `hd` and `cnt`, not `mem_r`. An entry is read only when `cnt > 0`, and only after a push wrote it.
- **Writes during reset.** `mem_r` writes are not reset-gated, but they are unobservable because `cnt` is 0 after the reset edge.
- **Equivalence probe.** Removing `hd`'s reset is equivalent, as the ring is head-relative. My probe `ring_hd_not_reset` passes, as predicted.

**Listener records** (`KL_pp_acmp_listener.sv:381-413, 744-751, 1032-1081`):
- `rec_rd_w` is consumed only in X_STRT_AP and X_LATCH (`:1051-1054`, `:1072-1074`).
- Those states are entered only from X_STRT_RD and X_RDREC (`:1034`, `:1067`), which are entered only from X_IDLE (`:953`, `:989`, `:997`, `:1007`).
- `sink_r` is assigned only in X_IDLE and in reset (`:828`, `:949-1012`).
- `recwr_en_w` is true only in X_INIT, X_PRELOAD and X_WB (`:744-745`), never in the issue states.
- So the asynchronous read in the consuming cycle equals what the removed register sampled one edge earlier. The record write mirror (`:759-765`) and the debug taps read the write bus, which is unchanged.
- **Equivalence probe.** `rec_read_at_write_addr` (reading at `recwr_addr_w`, equal to `sink_r` outside X_INIT) passes, as predicted.

**Interfaces and lint.**
- No port or parameter changes (A4).
- Scoped lint of both changed tops, with `lint_hdl.sh`'s flags and file set under the pinned Verilator 5.050: `LINT OK` for both (`receipts/lint-two.log`, rc 0).

### Robustness: CLEAN

- **Full-queue path.**
  - My one-line plants, which are not in the committed campaign, are each caught (`receipts/probes.json`):
    - a push lost when its own face pops (`ring_pop_blocks_write`: AQ2 and AQ3);
    - a full face reading past its head (`ring_full_reads_next`: AQ3, 15,712 edges);
    - an arm stored from the neighbour face (`ring_stores_neighbour`);
    - notify-monitor drops not counted (`drop_ignores_face7`: AQ3, 78,212 edges). This also shows the lowest-priority face's drop path is reached.
  - These cover simultaneous drops, saturation (`armq_drop_skip_sat`), reset with arms queued and arms offered in reset (AQ4's reach line).
- **Reset sweep.**
  - The record RAM has no reset, so the X_INIT sweep is its only one.
  - `sweep_skips_last_sink` and `sweep_skips_sink0` are both KILLED: 7 failures each, by the pre-existing "init sweep zeroed all 8 records" check and by RS.
  - Out-of-range sinks never reach X_RDREC or X_STRT_RD (`:952`, `:1006`, `:1018`, and the uid check at `:976`), so the asynchronous read is never consumed out of range.
- **Pre-existing drop-counter behaviour.** It counts one per clock however many faces overrun. It is unchanged, and the PR and section AQ record it as out of scope, as the no-behaviour-change rule requires. It is not a finding of this lane.

### Tests: CLEAN

All runs are at the exact head, with the pinned Verilator 5.050 (identity printed `Verilator 5.050 2026-07-01 rev v5.050`). Each ran with its own log and rc file in `receipts/`.

**`tb/pp_top` `make run`, six builds:** rc 0, **10435 checks: 10435 PASS, 0 FAIL**.
- The builds: default 9,947 (HZ 189, AQ 4/4), fixture 20, identify 178, line 231, timebase 56, defaults 3 (TD 3).
- This is the union the round-2b record states: 1cba30c's 10,420 plus PR #157's 15.

**`tb/acmp_listener`:** rc 0, 3111/3111.

**On `main`'s RTL.** Head benches over `main` `b0a74196`'s two files (`scratch/mainrtl`):
- `tb/acmp_listener`: 3111/3111, so RS passes on `main`.
- `--arm-queue-only`: `AQ: 4 checks, 0 failures`.
  - The traffic line reads 71,258,305 edges, 8,270 arms, 28, 4,288, 0, equal to `README.md:2046-2050`.
  - The drive line reads 90,172 / 88,003; 18,778 / 48,239 / 3,636 / 5,594 / 12,481; 352,294 in 80,719; 78,930; 4,096; 36 / 366. It equals the README's table (`:2080-2086`) and the head's own drive line.
  - So AQ grades behaviour the change kept.

**The committed ACMP campaign, unchanged (`--jobs 6`):** rc 0, **33 of 33 KILLED, four goldens PASS**.
- Every arm's failing count equals its README record (`receipts/acmp-campaign-counts.txt`):
  - `armq_*`: 72, 3, 12, 3, 3, 1, 1, 1, 1;
  - `rec_*`: 645 of 3080, 1, 91, 25, 37;
  - the guard controls: of 3107 and 3111.
- The first attempt, with the default shared `/tmp`, was interrupted from outside this review. Its driver and its wrapper disappeared, and its temporary extract was removed mid-golden. I re-ran the same committed driver with `TMPDIR` under my scratch (`scripts/campaign.sh`). The interrupted log is kept as `receipts/head-acmp-campaign-attempt1-interrupted.log`.

**AQ's design.**
- `ArmQueueModel` (`sim_main.cpp:723`) is an independent eight-deque model, stepped at every edge of every harness (`:1539-1542`).
- It compares the full port word, its valid and the drop counter, including the held port value when valid is low.
- The drive (`:13892`) forces the faces' own nets and holds the timer input idle (`pp_top_wrap.sv:925`). It is the default build's last stimulus: `run_arm_queue` is the last section in `main`, and no build after it runs AQ.
- AQ4 fails if the drive stops reaching a state.

### Docs: CLEAN (R1 recorded as RESIDUE, S1 as a suggestion)

- **Checked against the RTL and my runs:**
  - 09 §8.8 (`09_verification.md:392-403`);
  - `tb/pp_top/README.md` section AQ (`:2022-2112`) and the ACMP controls paragraph (`:1996-2003`): "fourteen controls", "all 33 KILLED", the four goldens;
  - `tb/acmp_listener/README.md:96-117`: 3111; RS is +123; the five controls and their counts;
  - 07 §6 (`07_memory_maps.md:926-929`), 08 §3's arm-port bullet, and `hdl-engineer.md` §3.1 (`:96-106`);
  - the RTL banners (`protocol_processor_top.sv:3004-3017`, `KL_pp_acmp_listener.sv:381-394`).
- No stale description of either structure as a shift queue, a sync-read record RAM or a read register remains in `docs/`, `hdl/` or `tb/`. `git grep` finds no `armq_r` or `rec_rdata_r`.
- No #639 text points at an unpublished bench.
- **PR body.** The opening ("`main` merged four times ... thirteen commits, head `c725be12`") matches `git log --first-parent` (13 commits, 4 merges). The round-2b tables match my runs (10,435; AQ on `main` `b0a74196`; acmp 33/33). Its Vivado table matches the published reports.

## 4. Prior public findings on this PR, resolved or retained at this head

I read these after my own pass, runs and probes.

| Finding | Severity | Status at `c725be12` | Evidence |
|---|---|---|---|
| R462-1 F1: the rings' full-queue path had no committed or reproducible check | MINOR | **RESOLVED** (still holds after the merge) | The AQ drive is unchanged by the merge (`git diff 1cba30c c725be1 -- tb/pp_top/sim_main.cpp` touches no AQ line). The coverage is re-measured here, and `armq_write_refused`, `armq_write_wrap_hi`, `armq_full_pop_refuses` and `armq_drop_skip_sat` are each KILLED by AQ3 in my campaign run. |
| R462-1 S1: name the source of "1,153 flops" | SUGGESTION | **RESOLVED** | `protocol_processor_top.sv:3012-3014` |
| R463-1 F1: 09 §8.8 said the benches were "recorded in the issue's pull request" | RESIDUE | **RESOLVED** | The sentence is gone. `git grep` for "recorded in the issue's pull request", "unpublished" and "lockstep" in the lane's doc and test files finds nothing. |
| R463-1 S1: three ring defects passed every committed check | SUGGESTION | **RESOLVED** | Write-on-offer and full-pop-refuses are KILLED in-tree. My `ring_full_reads_next` plant (a misread on the full path) is KILLED by AQ3. |
| R462-2 R1: the PR body's opening described an old head | RESIDUE | **RESOLVED** | The body now names four merges, thirteen commits and head `c725be12`, which matches the history. |
| R463-2-R1: the author's round-2 lockstep evidence README gives two wrong commands | RESIDUE | **RETAINED as residue** (outside the processor tree; on the manager's residue checklist) | The evidence archive is not part of this head. Nothing in the PR changes it. |
| R463-2-S1: the "1,152" census is not in the published Vivado receipts | SUGGESTION | **RETAINED** (optional) | The published `base/ooc-1x1` set still has no cell census. The comment is otherwise consistent (Conformance). |
| R463-2-S2: AQ4's reach is summed over faces | SUGGESTION | **RETAINED** (optional) | It is unchanged at this head. My `drop_ignores_face7` probe shows the lowest-priority face's drop path is reached and graded today. |

## 5. Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Issue #639 acceptance and assignments; the main..head `hdl/` diff (ports, parameters, snapshot word 24); published Vivado utilization and route-status reports (`28663f5a`) against the PR body; measured-vs-head RTL comparison | R462-3 | `c725be12d7ea6bf96f1b64e3a56416f0d4defd6c` |
| RTL | CLEAN | `protocol_processor_top.sv:2937-3058`; `KL_pp_acmp_listener.sv:381-413, 744-765, 820-1081`; merge-tree identity; scoped lint of both tops; two equivalence probes | R462-3 | `c725be12d7ea6bf96f1b64e3a56416f0d4defd6c` |
| Robustness | CLEAN | Full-queue, drop, saturation and reset paths: six kill probes and two equivalence probes; out-of-range sink paths; the pre-existing drop rule | R462-3 | `c725be12d7ea6bf96f1b64e3a56416f0d4defd6c` |
| Tests | CLEAN | `tb/pp_top` six builds (10,435); `tb/acmp_listener` (3,111); both on `main`'s RTL; the committed ACMP campaign (33/33 and four goldens, counts equal to the records); `sim_main.cpp:723-820, 1539-1542, 13892-13990`; `pp_top_wrap.sv:487-510, 897-967`; `acmp_mutants.py` | R462-3 | `c725be12d7ea6bf96f1b64e3a56416f0d4defd6c` |
| Docs | CLEAN (R1 RESIDUE) | 07 §6, 08 §3, 09 §8.8, `hdl-engineer.md` §3.1, both suite READMEs, RTL banners, the PR body | R462-3 | `c725be12d7ea6bf96f1b64e3a56416f0d4defd6c` |

## 6. Real limits

- **Not run by me, by assignment:**
  - `run_suites.sh` (the full processor bank), `make check`, `gen_matrix --check`, the full `syn/yosys/run.sh` and lint banks;
  - the other campaigns (aecp, notify, d3, ctr, aecp_dispatch, gsi, name_wr, adp, maap);
  - the parent consumer set, Vivado, act and hardware.

  For these, this review relies on the manager's source, static, builder and native banks at this head, as the assignment states. Within the processor, I ran the suites and the campaign that read the two changed blocks.
- **Hosted checks.** At review time, the exact head's `docs-gates` and `portability` jobs had completed with success. Its two `suites` jobs (push and pull_request) were still in progress (`receipts/hosted-check-runs.txt`). I did not wait on or judge them; the manager owns hosted acceptance.
- **Simulator.** All simulation used Verilator 5.050 only. No event-driven simulator was used. Uninitialised `mem_r` and record entries are argued unobservable from the RTL; this was not checked under X-propagation.
- **Vivado.** No Vivado run. The area figures are the author's published round-1 reports, checked against the PR body and tied to this head by RTL comparison.
- **Lockstep benches.** The author's published lockstep benches were not re-run here. Prior rounds re-ran them; this round relies on the in-tree AQ and RS checks and my probes.
- **No calibration or field evidence.** Physical calibration was NOT RUN. Field skips are not hardware proof.

## 7. Pending manager duties

1. **A3.** Re-record the resource gate's baseline in the parent when the pin is adopted (#638's rule). Issue #639 cannot close on this PR alone, which correctly says "Relates".
2. **Hosted acceptance** of the exact head's in-progress `suites` jobs.
3. **The final current-dev candidate** at the merge turn: source base `5c71928a`, live dev `6c22d3ca`. The parent's xvlog budget depends on #232's adoption line being applied first, as the PR body says.
4. **Residue checklist.** Add R1 (`tb/pp_top/README.md:2038`, "Every harness model runs the model" -> "Every harness runs the model"). Carry R463-2-R1.

## 8. Receipts

- `receipts/SUMMARY.txt`: one-screen summary.
- Run logs, rc files and campaign records:
  - `receipts/head-pp_top-run.{log,rc}`, `receipts/head-acmp_listener.{log,rc}`;
  - `receipts/mainrtl-acmp_listener.{log,rc}`, `receipts/mainrtl-aq.{log,rc}`;
  - `receipts/head-acmp-campaign.{log,rc}`, `receipts/acmp-campaign/` (the driver's `results.json` and per-arm logs), `receipts/acmp-campaign-counts.txt`.
- Probes: `receipts/probes.json`, `receipts/probes/*.log` (from `scripts/probe.py`).
- Lint: `receipts/lint-two.{log,rc}`.
- Other checks: `receipts/clone-integrity.txt`, `receipts/vivado-figures-extract.txt`, `receipts/hosted-check-runs.txt`.
- Scripts: `scripts/` (`COMMANDS.md` gives the order). In published receipts, the pinned toolchain's install prefix is replaced by `<PINNED_VERILATOR_ROOT>`.
- **Clone integrity after all work.**
  - HEAD `c725be12…` and tree `0bb7199a…`.
  - `git status --porcelain --ignored` is empty.
  - The index equals the HEAD tree (mode, blob, path).
  - Every tracked file's bytes hash to its HEAD blob, and exec bits match the HEAD modes.
  - The repository has no submodule gitlinks (no mode-160000 entries, no `.gitmodules`).
  - No probe touched the clone: all probes ran in `git archive` extracts under the packet's scratch.

R462-3 FINISHED
