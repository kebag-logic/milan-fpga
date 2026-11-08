[R792] POSITIVE - exact head e6d27f3a188286a5d5e30094e07453e2bbea1945

# R792-3: external review of PR #853 (#665 S6a, the placement switch), round 3

- Head `e6d27f3a188286a5d5e30094e07453e2bbea1945`, tree `dafb16a180a647ac96d7901125b25cd896d2b1f1`, PR base `dev-soft-core` at merge base `a9d69c77`. The PR is open and not a draft.
- Delta reviewed: `526f937c..e6d27f3a`, five commits and 10 files. The changes are docs, one comment in `syn/ooc/pp_placement.py`, and bench files: `sim_split.cpp`, `tb_split_top.sv`, `split_mutants.py`, `split_cdc_check.py` and the suite README.
- `git diff 526f937c..HEAD -- hdl/` is empty, so no RTL file changed in this round.
- Code the delta does not touch keeps its round-2 lens verdict (R792-2 at `526f937c`). Nothing it depends on changed.

## Verdict in one paragraph

Round 2 left one MINOR open: R791-2-F1, the same finding as R792-2 F-1. It is fixed as its verification step says.
- `pp_placement.py` says at `PLACEMENTS` (`:14-17`) and at the `f0-f4` branch of `limits()` (`:47`) that `f0-f4` is ruled dead and is removed at the flip together with the all-fabric placement. It cites `#665` only.
- The recipe page's row (`PP_SHADOW_BASELINE_RECIPE.md:192`), its paragraph (`:195-199`) and its recipe (`:214`) say the same.
- `pp_placement_selftest.py` is byte-unchanged and passes here.

All five of R791-2's suggestions were taken, and each holds up when tested:
- **S1:** with the 24-byte fill, the FIFO-full guard holds. Without the fill the guard fails, per the author's receipt. The runt arm is caught.
- **S2:** the 100-frame MAC burst binds `pp_rx_drops_w`. The tie-off arm is caught, and so are two mutants of my own.
- **S3:** the docs labels are replaced.
- **S4:** the bench nets carry their units.
- **S5:** the CDC check names a flop by its own net. The two plants' new required words are each still refused.

I re-ran the split leg (71 checks, 0 failures), the CDC self-test (13 of 13: the control and 12 plants) and both placement self-tests on a byte copy of the head. Every figure matches the author's receipts. All 20 author-r3 receipts I fetched match the published manifest hashes.

I found no BLOCKER, MAJOR or MINOR. There is one RESIDUE, a wording defect in a sentence this PR wrote. Round 2's own unassigned suggestions are carried below as suggestions.

## Prior findings, each resolved or retained at this head

| ID | Severity (round 2) | Status at `e6d27f3a` | Evidence |
|---|---|---|---|
| R791-2-F1 = R792-2 F-1 | MINOR (Conformance, Docs) | **Resolved** | `syn/ooc/pp_placement.py:14-17`: "f0-f4 is ruled dead (#665) ... removed at the flip together with the all-fabric placement". `:47`: "Ruled dead (#665); removed at the flip with all-fabric." `PLACEMENTS` and `limits()` behaviour are unchanged; the only diff lines are comments. `PP_SHADOW_BASELINE_RECIPE.md:192` row: "`f0-f4` (ruled dead, #665)". `:195-199` gives the same statement. `:214`: "kept only until the flip removes it; it is not run". The comment and the page cite `#665` only, with no comment ID, lane or stage. The author's `delta-label-scan.log` reports no match. Ruling issuecomment-6715535566 item 5 is satisfied. Here, `pp_placement_selftest.py` gives rc 0 and `pp_baseline.py --selftest` gives rc 0 (`receipts/placement-selftests.txt`). |
| R791-2-S1 (runts in a full FIFO) | SUGGESTION | **Taken** | `sim_split.cpp:572` adds a 24-byte frame, giving 109 offered: "[TAP] burst: 109 frames offered, 65 handed out, 44 counted lost". `:586-592` adds the guard `[TAP] the burst leaves the FIFO full to its last word` (`tb_split_top.sv:379`, `u_tap.rx_fifo.full`), then eight 8-byte runts with the count unchanged. The guard's power: with the 24-byte frame removed, the leg fails that guard alone (author `split-leg-without-24-byte-frame.log`: 108 offered, 1 failure of 71). That also shows that `full` asserts only with no word of room. Arm `a drop count that counts runts` (`split_mutants.py:129-133`) is caught by `[TAP] ...nor the one-beat runts a full FIFO turns away` (author `split-mutants.log`). R791-2's arm 1 is caught (author `r791-2-tap-mutant-1.log`, rc 0). |
| R791-2-S2 (datapath's own drop wiring) | SUGGESTION | **Taken** | `check_dp_drops` (`sim_split.cpp:617-635`) runs last. It checks that `p_rx_drops` (`= u_dp.pp_rx_drops_w`, `tb_split_top.sv:367`) reads 0, that it is greater than 0 after 100 back-to-back ADP frames at the MAC, and that handed + lost = 100. I measured 58 handed and 42 lost. The net feeds `milan_csr.sv:2278` `A_PP_DIAG` through `milan_datapath.sv:3189`. The tie-off arm (`split_mutants.py:134-138`) is caught by the check it names. My own mutants on copies were both caught: the count halved fails the conservation check (0x4f vs 0x64), and bit 0 stuck at 1 fails both reads-0 and conservation (`receipts/own-mutant-*.txt`). |
| R791-2-S3 (docs labels) | SUGGESTION | **Taken** | Each listed site now reads `(#665)` or gives the reason: `ENDSTATION_BUILDER.md:1073`; `MAILBOX_SPLIT.md:1332`, `:1363`, `:1378-1380`, `:1403`, `:1756-1757`; `SPLIT_CONTROL_MEMORY.md:4`, `:167`. At `:1756-1757`, "decided in that lane" is the wording of the ruling it replaces (issuecomment-6554243203: "is decided in that lane"), and the sentence names S11 (#665). The older IDs on those pages predate the PR and are not in S3's list. |
| R791-2-S4 (bench net units) = R792-2 S-1 | SUGGESTION | **Taken** | `tb_split_top.sv`: `pub_idle_slope_bps`, `fw_pt_offset_ns`, `d_idle_slope_bps`, `d_pt_offset_ns`, and all eight bindings. This is a rename only; the leg builds and passes. |
| R791-2-S5 (CDC message) | SUGGESTION | **Taken** | `split_cdc_check.py:175-181` `flop_name`: a non-port Q alias, otherwise "driving <port>", otherwise the cell. The output is deterministic, from a sorted list. The window plant now must and does report `output m_ctr_ans_data_o (sys) reads u_ctr.ans_r (dp)`. The LINK plant reports `flop driving m_link_up_o (sys) reads d_link_up_i (dp)`. Both are refused, along with the other 10 plants. The control gives 253 sinks clean (`receipts/split-cdc.txt`). |
| R792-2 S-2 (clock pin labelled by a temporary net) | SUGGESTION | Retained, not assigned | `label_of` still prints `{cell}.{port}` for primitives, and the clock-sink path is unchanged. |
| R792-2 S-3 (EDIT window, counter/face/GM events unexercised) | SUGGESTION | Retained | No change. |
| R792-2 S-4 (`KL_mbx_cdc_window.sv` request edge dropped past the wait bound) | SUGGESTION | Retained | No RTL change. |
| R792-2 S-5 (split WNS -0.021 ns, placed, not routed) | SUGGESTION | Retained | No RTL change, so the round-2 figure stands. |
| R792-2 S-6 (`split_mutants.py` run not bounded by wall clock) | SUGGESTION | Retained | `split_mutants.py:146`, `:149` `subprocess.run` still has no `timeout`. |

## Findings at this head

### R-1 RESIDUE (Docs): `docs/design/MAILBOX_SPLIT.md:1403-1404`, an incomplete sentence

- **Evidence.** The text reads "The map writer goes because the firmware's AECP owner holds the maps (#665). Its registers rest at reset, but the restore's hold, which is 0."
- The second sentence has no predicate for "the restore's hold". This PR wrote it (`61d680dd`), and this round edited the line (`31acb6d3`).
- The source comment it summarises (`milan_datapath.sv:5643-5645`) is complete: "Every register below then rests at its reset value, but the restore's hold, which is 0: no restore runs, so nothing holds the maps."
- **Impact.** This is wording only. It changes no figure, test, code or claim.
- **Exact fix.** "Every register rests at its reset value except the restore's hold, which is 0: no restore runs, so nothing holds the maps."
- **Verification.** Re-read `:1403-1404`. `check_doc_style.py` stays OK.

### Suggestions (optional, no lens effect)

- **S-A (Tests).** `check_dp_drops` reads the net `pp_rx_drops_w`, not `PP_DIAG` through the register read.
  - The `A_PP_DIAG` packing (`milan_csr.sv:2278`) is shared with all-fabric. A byte swap there would pass this leg.
  - A register read of `PP_DIAG[15:8]` after the burst would close this. The value is low, because the packing is not split-specific.
- **S-B (Docs, wrap only).** `MAILBOX_SPLIT.md:1756-1758` now wraps as "... until then the split ties `reboot_req_i` to" with "0." alone on the next line. Re-flowing the paragraph would fix it.

## Lens results, with evidence

```text
[R792] PASS Conformance - syn/ooc/pp_placement.py:14-17,:47; docs/testing/PP_SHADOW_BASELINE_RECIPE.md:192,:195-199,:214 - R791-2-F1/R792-2 F-1 checked against ruling issuecomment-6715535566 item 5 (ruled dead, removed at the flip with all-fabric, cite #665 only); PLACEMENTS/limits() behaviour unchanged (diff is comment-only); all-fabric identity on 6 shapes equal base vs head (author identity-compare.log, rc 0, digests equal to round 2's); no hdl/ change in the delta
[R792] PASS RTL - git diff 526f937c..e6d27f3a -- hdl/ (empty); milan_datapath.sv:10085-10109 (split ctrl_split binding the new probe reads), :3189 and milan_csr.sv:2278 (PP_DIAG packing), KL_ctrl_split.sv:186-188 (last_kept_r, the runt arm's site) - nothing the round-2 RTL verdict rests on changed; bench-only probes (tb_split_top.sv:367,:379) are read-only hierarchical taps
[R792] PASS Robustness - sim_split.cpp:566-614 (full FIFO to its last word, then one-beat runts, count unchanged), :617-635 (MAC burst, 100 frames at 8 B/cycle into a 1 B/cycle tap, conservation) - the runt-at-full and overflow-at-datapath paths are now exercised; guard power shown by the 108-frame receipt; saturation, refused-frame and reset paths unchanged from round 2
[R792] PASS Tests - split leg re-run 71/0 (receipts/split-leg.txt); split_mutants.py 24/24 incl. the two new arms (author split-mutants.log, manifest-verified); two own mutants caught (receipts/own-mutant-halved.txt, own-mutant-stuck1.txt); split_cdc_check.py --selftest 13/13 re-run with both changed required strings matched (receipts/split-cdc.txt); pp_placement_selftest.py unchanged and rc 0
[R792] PASS Docs - MAILBOX_SPLIT.md:1332,:1363,:1378-1380,:1403,:1429-1434,:1756-1757; ENDSTATION_BUILDER.md:1073; SPLIT_CONTROL_MEMORY.md:4,:167; PP_SHADOW_BASELINE_RECIPE.md:192-214; tb/verilator/milan_dp/README.md:109,:1134,:1137,:1139-1144 - counts (24 arms, 11 on encoding/tap/drop counts) match split_mutants.py; labels replaced; no new lane/round/reviewer/comment ID in source comments of the delta (pp_placement.py, sim_split.cpp, tb_split_top.sv, split_cdc_check.py, split_mutants.py read); R-1 is RESIDUE only
```

Comment rule: I read every new source comment in the delta. None carries a bench lane label, lane name, review round, reviewer ID or comment ID. "F0-F4" names the placement's engines and is not a lane label. "The flip" is the ruling's own term.

## Ledger (reviewer-owned)

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | ruling issuecomment-6715535566 item 5; `pp_placement.py:14-17,:47`; recipe page `:192-214`; author identity receipts (6 shapes, equal); `hdl/` diff empty | R792-3 | e6d27f3a188286a5d5e30094e07453e2bbea1945 |
| RTL | CLEAN | `hdl/` delta (empty); `milan_datapath.sv:3189,:10085-10109`; `milan_csr.sv:2278`; `KL_ctrl_split.sv:186-188`; bench taps `tb_split_top.sv:367,:379` | R792-3 (delta); R792-2 for the unchanged RTL | e6d27f3a188286a5d5e30094e07453e2bbea1945 |
| Robustness | CLEAN | `sim_split.cpp:566-635`; guard-power receipt; runt and tie-off arms; own mutants | R792-3 | e6d27f3a188286a5d5e30094e07453e2bbea1945 |
| Tests | CLEAN | split leg 71/0 (re-run); `split_mutants.py` 24/24 (author, manifest-verified); CDC 13/13 (re-run); placement self-tests (re-run); 2 own mutants caught | R792-3 | e6d27f3a188286a5d5e30094e07453e2bbea1945 |
| Docs | CLEAN (R-1 RESIDUE carried) | `MAILBOX_SPLIT.md`, `ENDSTATION_BUILDER.md`, `SPLIT_CONTROL_MEMORY.md`, `PP_SHADOW_BASELINE_RECIPE.md`, `tb/verilator/milan_dp/README.md` at the lines named above | R792-3 | e6d27f3a188286a5d5e30094e07453e2bbea1945 |

## What was executed

Everything ran at the exact head, on byte copies of this review's isolated clone. The clone itself was never modified.

- `make -C tb/verilator/milan_dp split` with the pinned Verilator 5.050, whose identity I checked with `--version`: rc 0, 71 checks, 0 failures. The tap burst was 109/65/44 and the MAC burst 100/58/42, identical to the author's `split-leg.log`.
- `split_cdc_check.py --selftest` with Yosys 0.66 and sv2v 0.0.13: rc 0, 13 of 13, 253 sinks clean.
- `syn/ooc/pp_placement_selftest.py` gave rc 0. `syn/ooc/pp_baseline.py --selftest` gave rc 0, and every placement check passed.
- Two own mutants of the split `pp_rx_drops_w` binding, the count halved and bit 0 stuck at 1 (`scripts/own_drop_mutants.py`): each rebuild failed the leg, with rc 2 from make and the checks shown in the receipts.
- Author-r3 receipts: I fetched 20 files (the handoff, the index and 18 gate logs or rc files) from evidence commit `d13c2b09`. All 20 match `published_sha256` in `review-evidence/665s6-r1/MANIFEST.json` (`receipts/author-r3-manifest-check.txt`).
- After the probes, the clone has an empty `git status`, `git diff HEAD` is clean, HEAD and tree are as above, and the submodule gitlinks are unchanged. Those are gptp-processor `135afd04`, protocol-processor `a9e84b66`, lwSRP `08ee86e8`, tsn-c-stack `70936b77` and verilog-axis `48ff7a7e`; `external` is not initialised, as at the start. The probe copies were deleted.

## Hosted evidence at review time (read-only, not a verdict)

This snapshot is in `receipts/hosted-checks-snapshot.txt`.
- 11 contexts had completed with success, including `changes`, `verilator-lint`, `firmware-unit`, `firmware-aecp-mutants`, `docs-gates-1`, `docs-check-no-git`, `wire-accountability` and `full-ci-gate`. One completed as skipped.
- 19 were in progress and 14 queued, including the Verilator shards, `firmware-boundary`, `firmware-verilator`, `docs-gates-0/2`, `elaborate-gates-0/1` and `yosys-elaboration`.
- No context had failed. The manager owns hosted acceptance.

## Real limits

- I did not re-run `split_mutants.py`, the hosted-job replay, the all-fabric identity dump, lint, the doc and idiom gates, or the reviewers' CDC and tap probe scripts. For those I relied on the author's manifest-verified receipts.
- My sv2v is 0.0.13, while the author used 0.0.12. The CDC self-test result is the same.
- No RTL changed, so the round-2 Vivado figures (post-placement estimate, not routed) stand. Timing closure is not known.
- Physical calibration was NOT RUN. Field skips are not hardware proof, and no hardware was used.
- No manager source bank runs at this head, and none is claimed or inferred. The PR targets `dev-soft-core`, so no act run applies.

## Pending manager duties

- Carry R-1 to the residue checklist.
- Open the Issue for `KL_pp_shadow`'s identical uncounted drop, required by R791-F4 and carried from round 2. A search at review time ("KL_pp_shadow drop", "PP_DIAG") found no such Issue; only #665 matched.
- Route `PP_SHADOW_BASELINE_RECIPE.md:206-208`, stale text that predates this PR and is not this round's, and `sw/firmware/ctrl/plat/README.md:137`, both carried.
- Confirm that the exact-head hosted run completes, in particular `firmware-boundary`, `firmware-verilator`, `rtl-fast`, `verilator-suites` and `yosys-portability`.
- Build and validate the current-dev merge candidate at the merge turn (source base `a9d69c77`, live dev `0a75aa774b89ac89351700f63dd8cbb89694af6c`), with the builder and native banks, and link its receipts.
- Obtain the second, internal positive review (R791-3) before merge, and obtain maintainer authorization for the merge.

R792-3 FINISHED
