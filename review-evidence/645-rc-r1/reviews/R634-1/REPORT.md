[R634] NEGATIVE - exact head 2639eecf3f94aa1a8be5c922058a05f0a48b1933

# R634-1: internal cleared-context review of PR #742 (#645 bind round)

- Head `2639eecf3f94aa1a8be5c922058a05f0a48b1933`, tree `c0bece4c6943bee323b9a72c4e677abdda840004`, source base `f62602531d415d6c1cae1374a3cc2938faf54049`.
- Scope reconstructed from: AGENTS.md / CONTRIBUTING.md; issue #645 body; the B17 ruling (6186940255), the B17 report (6187529947), the design round (6187595500), TAKEN (6187650593) and REVIEW READY (6192046983); `MEDIA_CLOCK_FOLLOWING.md` (settle recentre), `TIME_SYNC.md`, `REGISTER_MAP.md` (`SLIP_LB`), `AREA_BUDGET.md`; the diff `f6260253..2639eecf` (2 commits, 12 files); the author packet `review-evidence/645-rc-r1` at `a86dc902` and the B17 packet `review-evidence/645-b17-r1`.
- Prior public review findings on PR #742: none. At the time of this review the PR carried only the two review-start comments, so nothing is resolved or retained from earlier rounds.
- Verdict: NEGATIVE, for two MINOR findings. The RTL change is correct and confined. The B17 reproduction and its removal by the arm reproduce exactly at this head. The open items are a B17 bound the docs and harness overstate, and a residual slip that the stated limits do not describe.

## What was confirmed (author evidence, then falsification at this head)

| Check | Result | Evidence |
|---|---|---|
| Replay parameters come from B17 | All 40 `kB17` values (first-PDU delay, first-burst time and peak, largest later burst; ten cycles) re-derived independently from `645-b17-r1/author/summary/cNN.json` under B17's stated burst rule (more than 20 us, grouped under 1 ms): 10/10 MATCH. The mean slope of 1.538 us/PDU matches `author/b17/burst.txt` (1.468 to 1.664). The lateness envelope of 0 to 5 us lies within B17's p99.9 of 4.4 to 6.1 us. | `receipts/b17_params_check.txt`, `scripts/b17_params_check.py` |
| Reproduction first: dev's datapath fails | The base datapath (`f6260253`) running the head harness, B17 cycles 5, 4 and 9: each slips +2 dups at its first burst (+0.10, +3.20 and +1.28 s after the bind, inside B17's slip intervals 0.066 to 0.643, 3.103 to 3.681 and 1.045 to 1.946 s). rc 1. The author's base campaign is 0/32 (`campaign/base/driver.log`). | `receipts/runs/base_bind.log` |
| Arm removes it | The head default `bind` leg: 30 checks, 0 failures. One arm +0.002 ms after the first PDU, one settle recentre 2,047.65 to 2,047.70 ticks later, one render recentre, `SLIP_LB` +0/+0. Under CRF following: no arm, and the reported +2 slip. My rerun of `sweep-bind` is 32/32, and its table matches the author's exactly: 169 inside, 6 out-of-window slips, 0 after the ring acts. | `receipts/runs/head_bind.log`, `receipts/runs/sweep_bind.log`, `receipts/sweep_bind_rerun_summary.txt` |
| RTL confined | The only `hdl/` change is `hdl/milan/milan_datapath.sv:6584-6644`: comments, `settle_bind_wait_r`, `settle_bind_pdu_w`, `settle_bind_arm_w` gated by `!follow_sel_r`, and one OR term in `settle_arm_w`. Fire, ceiling, steady, recovery and the `render_recentre_p_w` fan-out are unchanged. No port, register field or parameter changes. The PDU qualifier (`lb_tap_tvalid_w` = tvalid && tready, `tlast`, `tuser == s`) is the capture crossbar's PRIME term (`KL_chan_map_capture.sv:951-961`, `lb_ok_w` :691). The bind edges are the stream table's registered `bind_rise_o`/`bind_fall_o` (`KL_stream_table.sv:142-155`), on the same `axis_clk`. With `LOOPBACK_P = 0`, `lb_tap_tvalid_w` folds to 0 (`milan_datapath.sv:6410`). | diff, source reads |
| Arm edge behaviour | My two-stream probe of the extracted block: a rise and a `tlast` in the same cycle do not arm, and the next `tlast` does. Another stream's PDU does not arm. Two binds, or a pending source change plus a bind, give one action, and each arm restarts the dwell (fires 2,047 to 2,050 ticks after the last arm). A bind under following whose first PDU comes after a switch to INTERNAL arms. Reset clears the wait. Recorded, not a finding: a fall in the same cycle as the first `tlast` still arms one (benign) recentre, while the capture un-primes on that flush. | `receipts/bind_arm_edges.txt`, `scripts/bind_arm_edges.py` |
| Controls | `settle_control.py` at head: PASS at 6.25, 25, 50 and 100 MHz. `make mutants`: 15/15 caught, each by its named check: 12 in the first invocation and 3 in the second. The second invocation was needed because my first probe tree lacked `tb/verilator/chmap_capture`; that was my omission, and the three were then caught. NO-BIND-ARM fails "no SLIP_LB change across the cycle" in cycles 5, 4 and 9. BIND-RISE fails it in 4 and 9. FOLLOWING-ARM fails "[BIND-FOLLOW] ... armed no settle recentre". The author's 8 controller plants are 8/8 (`controls/sc_plants/plants.log`). | `receipts/runs/settle_control.log`, `receipts/runs/mutants.log`, `receipts/runs/mutants_lrc.log` |
| Existing suites unchanged | Outside `tb/verilator/follow_ring` the diff touches no test. The b8/pullin legs' checks are unchanged: the sim changes are the bind case, `tx_ns` (identical to the old expression when nothing is bound) and the bind-fall queue model. The author's receipts are rc 0, tally 52,122 checks / 0 failures across 11 suites, plus the physical gPTP leg 197/0 (`author/tally/tally.txt`, `author/suites/*.rc`). | diff stat, author receipts |
| Area | `author/area/*.vivado.util.txt`: 1x1 73 to 76 LUT and 93 to 94 FF (+3/+1). Loopback off (the shipping 8x8, `configs/endstation_ax7101_8x8.yaml:248` `loopback_lane: false`): 73/93 to 73/93 (0/0). A non-shipping 8x8 with the lane: +12/+8 (stated in HANDOFF). | author area receipts |
| Wall clock | 857.648 / 800.859 = 1.0709; 1114.2 s (`TESTING.md:336`) x 1.0709 = 1193.2 s, 66.8 s under 1260 s and 246.8 s under 1440 s. Stated as a projection with hosted acceptance owed. | `author/wallclock/result.txt` |
| Docs gates | Rerun at head: `docs_check.py`, `check_doc_style.py` and `check_doc_paths.py` rc 0, and `git diff --check` rc 0. `gen_toc.py --check` and `check_em_dash.py` could not run here (the pinned Markdown renderer is not installed in this clone). The author's receipts for both are rc 0 at head (`author/gates/gen_toc_check.log`, `check_em_dash.log`, 0 findings over 118 lines). | `receipts/doc_gates.txt` |
| Evidence integrity | Every published hash in the author packet's `MANIFEST.json` matches, and no file is unlisted. The 22 files whose hashes differ from `author/MANIFEST.sha256` are exactly the 22 marked `path_redacted`. | review computation |

## Findings

### R634-1-F1 MINOR (Conformance, Tests, Docs): B17 does not support the 10 us lower bound on the primed margin

- **Where:** `docs/design/MEDIA_CLOCK_FOLLOWING.md:1287` ("above 10 us, since nothing that late slipped it") and `:1342-1343` ("At the bench that margin was above 10 us"). `tb/verilator/follow_ring/sim_main.cpp:59-60` and `:171-174` (`kB17MarginLoUs = 10.0`, "no PDU over 10 us late slipped the ring before its first burst"). The window check that uses it is at `:1310`. The PR body and REVIEW READY say "B17 bounds the primed margin to 10 to 24.565 us".
- **Authority and evidence:** B17's analyser lists only PDUs more than 10 us late (`645-b17-r1/author/tools/ana_b17.py:51`, `LATE_US = 10.0`). In every cycle that list holds nothing before the first burst (`receipts/b17_params_check.txt`). B17 therefore shows only that the largest pre-burst lateness was at most 10 us. The ring survived that unknown maximum, so the margin is bounded below by it, not by 10 us. A lower bound needs a late PDU that did not slip the ring. The same paragraph already gives a valid one: a 30.26 us burst after the slip passed, so the margin was above 30.26 - 20.83 = 9.43 us. The "10 us" bound inverts the inference.
- **Impact:** The ring margin that B17 measured on the bench, and the window that defines "in-window" for the reproduction and its claims, are overstated. With the supported 9.43 us bound the author's 169/151 split is unchanged: no run in the grid has a lower edge in [9.43, 10). So no recorded outcome changes. But the bench-safety sentence and the harness constant rest on an unsupported figure.
- **Required outcome:**
  - The design, the harness comment and the PR text state the lower bound B17 does support (9.43 us from the later-burst argument, or the measured pre-burst maximum if it is extracted from the B17 captures), with its derivation, and drop "since nothing that late slipped it".
  - `kB17MarginLoUs` either takes the supported value or is stated as a deliberately conservative classification threshold, with its reason.
- **Verification:** A reader can reproduce the stated bound from `c05.json`/`c0N.json`. If the constant changes, `sweep-bind` is rerun and the inside/outside counts are restated.

### R634-1-F2 MINOR (Conformance, Robustness, Tests, Docs): in-window binds still slip one pair before the recentre acts; the stated limit misses it

- **Where:** the arming-window limit, `docs/design/MEDIA_CLOCK_FOLLOWING.md:1338-1344`. It says six out-of-window binds slip, "at the two phases that prime the ring nearest its empty edge", and implies in-window binds hold. The PR body and REVIEW READY say "Every one of the 169 in-window binds held" and "no in-window bind slipped". The campaign grid is `tb/verilator/follow_ring/sweep.py` (`bind`, 16 phases) through `Makefile` `sweep-bind`.
- **Evidence:** I reran the head harness (pinned Verilator 5.050) on grids finer than the author's 16 phases:
  - **32 phases at 0 to 5 us** (`sweep.py bind --phases 32 --jitter-us 5`): 31/32 runs pass. `bind_j5_p27` (phase 0.84375, seed 672) fails "[BIND] B17 cycle 7 at INTERNAL: no SLIP_LB change across the cycle got=1 exp=0". The harness itself classes that bind as inside B17's window (primed margin 19.04 to 24.16 us). `SLIP_LB` moves +1 dup, i.e. one pair, half the +2 frame unit and a shape B17 never showed, 0.127 ms after the first PDU. The arm and the recentre are still one each, with no slip after the ring acts.
  - **Deterministic, and pre-existing:** a rerun gives the same result. Dev's datapath under the identical command shows the same +1 at the same instant, then its +2 burst slip (`receipts/points/p27_32phase_cycle7_{head,base}.log`). The arm neither causes nor removes it, because it falls in the 42.7 ms before the recentre acts.
  - **Dense cycle-7 scan** (128 phases x {0, 0 to 5 us}, 256 binds): two more in-window one-pair dups, at 0.8906 (18.24 to 23.36 us) and 0.9297 (17.44 to 22.56 us). Both are +1 dup 0.13 to 0.25 ms after the first PDU (`receipts/points/dense_bind_j5_p114.log`, `dense_bind_j5_p119.log`). The scan tool hit my 590 s cap (`receipts/runs/sweep_dense.rc` 124). The 21 unfinished points were then run directly with the same arguments, and all 256 have results (`receipts/sweep_dense_cycle7_summary.txt`).
  - **Out-of-window slips are wider than stated:** on the 32-phase grid they fall at four phases (0.78 to 0.875), 19 binds, up to 2.5 ms after the first PDU, and up to 2.9 ms on the dense grid (`receipts/sweep_32phase_summary.txt`).
  - Across the 899 INTERNAL binds I ran at this head (the default leg and the three sweeps), no slip fell after the ring acted.
  - Mechanism: not established by this review. The one-pair form points at pair-asymmetric commit and pop timing around priming in the unchanged capture crossbar. A harness-stimulus artefact is not excluded.
- **Impact:** The PR's stated limits describe the residual risk as confined to binds priming under 10 us at the edge phases. But a bind inside the window can still move `SLIP_LB`, by one pair, before the recentre acts. That is exactly the observable the post-merge bench repeat of B17's ten binds grades as #645's acceptance. Measured incidence among in-window binds is about 1 %: 1 of 141 on the 32-phase grid and 2 of 132 on the dense grid, all with 0 to 5 us of lateness. The limit as written would lead a reader to treat such a bench reading as unexplained.
- **Required outcome:**
  - The design's limit text, the PR body and the test plan describe this residual: in-window binds can take a one-pair dup within the arming window; it is pre-existing on dev's datapath and not removed by the arm. Give the measured incidence and phases.
  - The out-of-window statement is either qualified as a result of the 16-phase grid or restated over a finer grid.
  - The priming-time one-pair dup becomes a new public Issue: mechanism, whether it is DUT or harness, and whether the loopback pairs leave lockstep. It is not silently absorbed here.
  - Optional: a campaign grid that includes these phases.
- **Verification:**
  - `Vfollow_ring --case bind --bind-phase 0.843750 --jitter-us 5 --seed 672 --any-phase --dwell-s 0.5` on head and on dev's datapath reproduces the +1 (cycle 7).
  - The updated text matches `receipts/sweep_32phase_summary.txt` and `receipts/sweep_dense_cycle7_summary.txt` or the author's own finer campaign.
  - The new Issue is linked from the limit.

### R634-1-S1 SUGGESTION (Docs): cite the current area headline

REVIEW READY and HANDOFF measure the +3 LUT against the `route-1x1` row (`AREA_BUDGET.md:170`, 50,267 LUT, 12,227 over). The page's current headline is #696's 50,013 LUT, 11,973 over (`AREA_BUDGET.md:124`, `:386`). Both rows exist, and the delta's conclusion is unaffected (3/11,973 = 0.025 %). Cite the current headline, or say why the older route row is used.

## Reviewer ledger (round R634-1)

| Lens | Status | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1, F2) | Issue #645 acceptance; design round 6187595500 items 1 to 4; B17 report and packet `645-b17-r1/author/summary/c01..c10.json`; `sim_main.cpp:140-175`, `:1264-1400`; the base and head bind runs; `sweep-bind` rerun; the 32-phase and dense sweeps | R634-1 | 2639eecf3f94aa1a8be5c922058a05f0a48b1933 |
| RTL | CLEAN | `hdl/milan/milan_datapath.sv:6579-6706` (arm, settle FSM, fan-out) against `KL_chan_map_capture.sv:691,951-961,1104-1123` and `KL_stream_table.sv:142-155`; `milan_datapath.sv:1196,1311-1314,1610-1629,6409-6413`; `receipts/bind_arm_edges.txt`; `settle_control` at four rates; the author's area, lint (90 <= 90) and xvlog (0) receipts. F2's mechanism lies in unchanged capture RTL outside this diff; the changed RTL does what the ruling says. | R634-1 | 2639eecf3f94aa1a8be5c922058a05f0a48b1933 |
| Robustness | UNCLEAN (F2) | Phase and lateness boundaries (my 32-phase and 256-point grids); same-cycle rise/`tlast`, fall/`tlast`, other stream, re-arm while pending, reset, following-to-INTERNAL (`receipts/bind_arm_edges.txt`); `LOOPBACK_P = 0` fold | R634-1 | 2639eecf3f94aa1a8be5c922058a05f0a48b1933 |
| Tests | UNCLEAN (F1, F2) | `tb/verilator/follow_ring/{sim_main.cpp,mutants.py,settle_control.py,sweep.py,Makefile,follow_ring_wrap.sv}` diffs; 15/15 mutants; 8/8 plants; the base and head reproductions; a sweep-bind rerun matching the author's table | R634-1 | 2639eecf3f94aa1a8be5c922058a05f0a48b1933 |
| Docs | UNCLEAN (F1, F2) | `docs/design/MEDIA_CLOCK_FOLLOWING.md:1090,1187-1188,1264-1344,1627,1873-1875`; `TIME_SYNC.md:386,497-498`; `REGISTER_MAP.md:1878`; `TESTING.md:271,301-365` and the `follow_ring` row of the suite table; `scripts/measure_test_evidence_readers.py`; PR body; REVIEW READY | R634-1 | 2639eecf3f94aa1a8be5c922058a05f0a48b1933 |

## Real limits of this review

- Not rerun here: the eleven-suite bank, the physical gPTP leg, Yosys, the vendor parser, the builder tests, and the area synthesis. These rest on the author's receipts at `4e6b5398` with the RTL and harness unchanged since. No manager source bank ran at this head, and none is inferred.
- Not falsified: the physical gPTP leg's later startup and reset recentres (input PDUs 9,822 and 95,986), which the author says are consistent with the bind arm restarting a pending dwell. My edge probe confirms that a bind arm restarts a pending dwell. No base run of that leg exists.
- `gen_toc.py --check` and `check_em_dash.py` could not run in this clone (renderer absent). The author's rc 0 receipts stand.
- Hosted contexts at this head, as read at the time of this review: several were still in progress, including Verilator shards 0 to 5, Yosys shard 0, elaborate and docs-check. Physical gPTP was skipped, not executed. The completed ones were successes (`receipts/hosted_check_runs.tsv`). This is not hosted acceptance.
- Physical calibration was NOT RUN. No hardware was touched, and field skips are not hardware proof.
- After the probes, the clone is byte-exact at head: tracked blobs, modes and index equal the tree `c0bece4c`, the six gitlinks are unchanged, and there are no untracked files (`receipts/clone_integrity.txt`).

## Pending manager duties

- Exact-head hosted acceptance, including the `follow_ring` window against 1260 s, and act/hosted ownership.
- The current-dev merge candidate (source base `f6260253`, live dev `65617779`) with the builder and native banks.
- After merge, the bench repeat of B17's ten binds, which is #645's acceptance. Read any one-pair `SLIP_LB` +1 against F2.
- Carry S1 if wanted. Publish this report.

R634-1 FINISHED
