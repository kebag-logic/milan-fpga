[R791] POSITIVE - exact head e6d27f3a188286a5d5e30094e07453e2bbea1945

# R791-3: internal cleared-context review of PR #853 (#665 S6a, the placement switch), round 3

- Head `e6d27f3a188286a5d5e30094e07453e2bbea1945`, tree `dafb16a180a647ac96d7901125b25cd896d2b1f1`. Target `dev-soft-core`, ready (not draft).
- Delta reviewed: `526f937c..e6d27f3a`, five commits. My round 2 report was at `526f937c`.
- Source base `a9d69c77`.
- 10 files changed: 4 docs pages, `syn/ooc/pp_placement.py`, and 5 files of the split bench under `tb/verilator/milan_dp/`.
- `git diff --name-only 526f937c..HEAD -- hdl configs sw protocol-processor gptp-processor` is empty. **No RTL file changed.**
- Evidence: the author's round 3 receipts at evidence commit `d13c2b09` (`review-evidence/665s6-r1/author-r3`). I checked all 354 `author-r3/` files against `MANIFEST.json`: 354 match, 0 differ, 0 missing, 0 unlisted.
- I also ran my own runs and probes, listed below.

## Verdict summary

- **POSITIVE.** All five lenses are clean at this head.
- **Round 2's one open MINOR is fixed** as its verification step requires. That is R791-2-F1, the same finding as R792-2 F-1.
- **R791-2's five suggestions were taken.** Each does what it claims. Where a claim could be falsified, I re-ran it or probed it.
- **New this round:** no BLOCKER, MAJOR, MINOR or RESIDUE. There are three suggestions, which do not affect any lens.

## Prior findings at this head

| Prior finding | Status at e6d27f3a | Evidence |
|---|---|---|
| R791-2-F1 = R792-2 F-1 (MINOR, Conformance, Docs): `f0-f4` presented as live where it is defined | **Fixed** | See the detail below the table. |
| R791-2-S1 (Tests): runts during a full FIFO | **Taken, and it bites** | See the detail below the table. |
| R791-2-S2 (Tests): the datapath's own drop wiring | **Taken, and it binds the net** | See the detail below the table. |
| R791-2-S3 (Docs): labels and comment IDs on the docs pages | **Taken** | See the detail below the table. |
| R791-2-S4 (Tests): bench net units | **Taken** | `tb_split_top.sv:104,119,196,204`: `pub_idle_slope_bps`, `fw_pt_offset_ns`, `d_idle_slope_bps`, `d_pt_offset_ns`, with all 8 bindings renamed. The bench builds and passes 71/0. |
| R791-2-S5 (Tests): CDC message naming | **Taken** | See the detail below the table. |
| R791-2 note: `check_solution_docs.py:184` reformat | **Stated** | The PR body says it is a format-only change, outside the lane's own lines, with no behaviour change. |
| Round 1 findings R791-F1 to F7, and R792 D-1, R-1, R-2, R-3 | **Still fixed** | The delta touches none of their artifacts except the bench nets (S4) and the doc labels (S3). Both keep the round 2 resolution. My delta scan of added lines finds no new label or ID. |

**R791-2-F1 = R792-2 F-1.**
- `syn/ooc/pp_placement.py:14-17`, above `PLACEMENTS`, says that `f0-f4` is ruled dead (#665). It gives the reason, says not to select or extend it, and says it is removed at the flip together with the all-fabric placement.
- `:47`, at the `f0-f4` branch of `limits()`, says the same in short form.
- Both cite #665 only. They name no stage, lane or comment ID.
- `docs/testing/PP_SHADOW_BASELINE_RECIPE.md:192`, the row, now reads "(ruled dead, #665)". `:195-199`, the paragraph, says the same. `:214`, the recipe, says it is kept only until the flip and is not run.
- This matches ruling issuecomment-6715535566 item 5, which I re-read: "ruled dead. Say so where it is defined. It is removed at the flip (S13), together with the all-fabric placement."
- "The flip" is defined at `docs/ARCHITECTURE_HW_SW_SPLIT.md:6-9`.
- `pp_placement_selftest.py` is unchanged in the delta, and I ran it at head: rc 0. `pp_baseline.py --selftest` (which imports it) passes every placement check (receipts/pp-placement.log).

**R791-2-S1, runts during a full FIFO.**
- `sim_split.cpp:572` adds a 24-byte frame. `:588` is the guard `[TAP] the burst leaves the FIFO full to its last word`, which reads `u_tap.rx_fifo.full`. That signal is `axis_fifo.v:200`, which means no word of room.
- `:589-592` sends 8 one-beat runts, then checks `[TAP] ...nor the one-beat runts a full FIFO turns away`.
- **P1:** without the 24-byte frame, the guard FAILs. That is 1 failure of 71, which matches the author's receipt (receipts/probe-p1-no-24-byte.log).
- **P2:** without the frame and the guard, the runt-counting arm survives at 70 checks and 0 failures (receipts/probe-p2-runt-without-fill.log). So the fill and the guard together are what make the runt check bite.
- With them in place, the arm is caught in my campaign run (`split_mutants.py:129`).

**R791-2-S2, the datapath's own drop wiring.**
- `check_dp_drops` (`sim_split.cpp:620-635`) runs last (`:652`). It probes `p_rx_drops = u_dp.pp_rx_drops_w` (`tb_split_top.sv:82,367`). That is the net `milan_csr` reads into `PP_DIAG` (`milan_datapath.sv:3189`).
- It checks that the count reads 0, then sends a 100-frame burst at the MAC. It requires lost > 0 and handed + lost = 100. My run gives 58 handed out and 42 counted lost.
- The tie-off arm (`split_mutants.py:134`) is caught in my campaign run. The "reads 0" check alone could not catch that arm; the burst can.

**R791-2-S3, labels and comment IDs on the docs pages.**
- `ENDSTATION_BUILDER.md:1073`, `MAILBOX_SPLIT.md:1332,1363,1378-1380,1403,1756-1757` and `SPLIT_CONTROL_MEMORY.md:4,167` no longer carry "F-INT PR 2" or a comment ID.
- I checked the reasons that replace the IDs against the rulings:
  - 6088423771 decision 1 says the engines cannot be placed one at a time, so the whole wrapper goes with the parent `KL_maap` once AECP is on the core. `:1378-1380` matches.
  - 6554243203 says a face-block level "is the expected end state and is decided in that lane". `:1756-1757` matches. See SG1.

**R791-2-S5, CDC message naming.**
- `split_cdc_check.py:175-181` adds `flop_name`. It uses a non-port alias of the Q net. When the net has only a port's name, it reads "driving <port>". When the net has no name, it falls back to the cell.
- `:183-190` (`label_of`) and `:200` (the sink label) use it.
- The two plants' required words changed:
  - `:266` is now `flop driving m_link_up_o (sys) reads d_link_up_i (dp)`.
  - `:274` is now the whole line `output m_ctr_ans_data_o (sys) reads u_ctr.ans_r (dp)`.
- My `make split-cdc`: 253 sinks clean, and the control plus all 12 plants are refused, 13/13 (receipts/split-cdc.log). Both new messages appear in that log as required.

## Findings (this round)

No BLOCKER, MAJOR, MINOR or RESIDUE.

### Suggestions (optional, no lens effect)

- **R791-3-SG1 (Docs) - `docs/design/MAILBOX_SPLIT.md:1756-1757` - "decided in that lane".**
  - The phrase is accurate: it is ruling 6554243203's own wording, and "that lane" refers to S11 (#665) in the same sentence.
  - But it brings the lane concept onto a design page, where a reader may not know which lane is meant.
  - Possible wording: "...gives the request its carrier; a face-block level is the expected end state, to be decided there (#665)."
- **R791-3-SG2 (Tests) - `tb/verilator/milan_dp/sim_split.cpp:620-635` - the drop count is read at the net, not through the register.**
  - `check_dp_drops` binds `pp_rx_drops_w`, which is what S2 asked for.
  - The `PP_DIAG[15:8]` mapping in `milan_csr` (`milan_datapath.sv:3189`) is shared with the all-fabric build and is not exercised by the split leg.
  - A later leg that reads `PP_DIAG` through the contract's register path would bind the last step of the path.
- **R791-3-SG3 (Tests, readability) - `tb/verilator/milan_dp/split_cdc_check.py:179-181` - which port name is used.**
  - When a Q net aliases more than one port and no internal name, `flop_name` uses the alphabetically first port.
  - That is deterministic, but a one-line note in the docstring would say so.

## Clean results, with evidence (per lens)

```text
[R791] PASS Conformance - syn/ooc/pp_placement.py:14-17,47; docs/testing/PP_SHADOW_BASELINE_RECIPE.md:192,195-199,214; issuecomment-6715535566 item 5; issuecomment-6088423771 decision 1; issuecomment-6554243203; docs/ARCHITECTURE_HW_SW_SPLIT.md:6-9 - the ruled-dead f0-f4 is stated where it is defined and on the recipe page, with the ruling's removal point; each replaced docs ID's reason matches its ruling; PLACEMENTS and limits() are unchanged in behaviour (pp_placement_selftest rc 0, pp_baseline --selftest rc 0)
[R791] PASS RTL - git diff 526f937c..e6d27f3a -- hdl configs sw protocol-processor gptp-processor (empty); author-r2 vs author-r3 gates/ident-head.json (6 shapes, every digest equal) and author-r3 identity-compare.log (head = base a9d69c77 on 6 shapes) - no RTL or configuration input changed; KL_ctrl_split.sv:183-191 (last_kept_r/drop_p_w) read against the new runt arm, and axis_fifo.v:200 (full) against the bench probe tb_split_top.sv:379; the round 2 RTL verdict stands
[R791] PASS Robustness - sim_split.cpp:565-635 at head - full FIFO to the last word with one-beat runts refused and uncounted (guard at :588, P1 and P2 show it is needed); datapath tap overflow under a MAC burst with conservation (handed + lost = 100) and a zero baseline; 16-bit frame-count wrap handled by the cast at :629; leg ordering: check_dp_drops runs last and its zero baseline holds after every earlier leg
[R791] PASS Tests - receipts/split-leg.log (71 checks, 0 failures), receipts/split-mutants.log (control + 24 of 24 caught, each by its named check), receipts/split-cdc.log (13/13, 253 sinks), receipts/probe-p1-no-24-byte.log (guard FAILs, 1 of 71), receipts/probe-p2-runt-without-fill.log (runt arm survives without fill, 70/0) - every new check can fail for the defect it claims; the two new arms are caught; the changed plant words are held and each plant is still refused
[R791] PASS Docs - tb/verilator/milan_dp/README.md:109,1134,1137,1139-1144; docs/design/MAILBOX_SPLIT.md:1332,1363,1378-1380,1403,1431-1434,1756-1757; docs/design/SPLIT_CONTROL_MEMORY.md:4,167; docs/ENDSTATION_BUILDER.md:1073; PP_SHADOW_BASELINE_RECIPE.md:192-214; PR #853 body lines on F1 and on check_solution_docs.py - counts (24 arms, 11 on encoding/tap/drop counts, 12 CDC plants, 71 checks) match the code and my runs; no stale "twenty-two" or "66 checks" remains; added lines carry no lane, round, reviewer or comment-ID label (scan of 526f937c..HEAD added lines); source comments cite #665 only
```

## Measurements and identity, checked against receipts

| Claim (author receipt) | My result at e6d27f3a |
|---|---|
| Split leg: 71 checks, 0 failures; TAP burst of 109 frames, 65 handed out, 44 lost; MAC burst of 100 frames, 58 handed out, 42 lost | The same (receipts/split-leg.log, pinned Verilator 5.050, rc 0) |
| Split mutants: control passes, 24 of 24 caught | The same, rc 0, 364 s (receipts/split-mutants.log) |
| CDC: 253 sinks, 13 of 13 | The same, rc 0 (receipts/split-cdc.log) |
| The leg without the 24-byte frame fails the guard (1 of 71) | The same (P1, receipts/probe-p1-no-24-byte.log; make rc 2 because the binary exits 1) |
| All-fabric identity: 6 shapes, head = base, equal to round 2's | I did not re-dump; no input changed. The author's head digests equal round 2's on all 6 shapes, and `identity-compare.log` shows head = base `a9d69c77`. |
| `pp_placement_selftest.py`: rc 0, unchanged | Unchanged in the delta; rc 0 (receipts/pp-placement.log) |

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `pp_placement.py:14-17,47`; recipe page `:192-214`; rulings 6715535566 item 5, 6088423771 decision 1, 6554243203; `ARCHITECTURE_HW_SW_SPLIT.md:6-9`; placement self-tests | R791-3 | e6d27f3a188286a5d5e30094e07453e2bbea1945 |
| RTL | CLEAN | empty RTL/config delta; six-shape identity receipts (head = base = round 2); `KL_ctrl_split.sv:183-191`; `axis_fifo.v:200`; `milan_datapath.sv:3189,10107` | R791-3 (delta), resting on R791-2 for unchanged RTL | e6d27f3a188286a5d5e30094e07453e2bbea1945 |
| Robustness | CLEAN | `sim_split.cpp:565-635`; probes P1, P2; mutant arms `split_mutants.py:129,134` | R791-3 | e6d27f3a188286a5d5e30094e07453e2bbea1945 |
| Tests | CLEAN | split leg 71/0; mutants 24/24; CDC 13/13; P1; P2; author receipts (354 files hash-verified) | R791-3 | e6d27f3a188286a5d5e30094e07453e2bbea1945 |
| Docs | CLEAN | milan_dp README; `MAILBOX_SPLIT.md`; `SPLIT_CONTROL_MEMORY.md`; `ENDSTATION_BUILDER.md:1073`; `PP_SHADOW_BASELINE_RECIPE.md`; PR body; added-line label scan | R791-3 | e6d27f3a188286a5d5e30094e07453e2bbea1945 |

Some artifacts are untouched since `526f937c`, or since `6584b7bf` for round 1's artifacts. They keep their prior lens verdicts, R791-2 and R791-1. That covers:
- the builder gates 23m and 23n;
- the SoC split tables;
- the `KL_mbx_cdc` and `KL_mbx_cdc_window` RTL;
- the population tool;
- the export identity.

## Real limits

- **No manager source bank runs at this head, and I claim none.** The source-head execution evidence is:
  - my focused runs above;
  - the author's hash-verified receipts;
  - the hosted checks.
- **Hosted, polled 2026-11-08T08:46:52Z** (receipts/hosted-check-runs.tsv):
  - 14 succeeded;
  - 1 was skipped (the physical gPTP job, which runs nightly or by hand);
  - 30 were queued or in progress, including the Verilator shards, `firmware-boundary`, `publication-census`, `docs-gates-0`, `elaborate-gates-0/1` and `yosys-elaboration`.
  - None had failed. This is not hosted acceptance.
  - This PR targets `dev-soft-core`, so no act run applies.
- **Not re-run by me:**
  - the six-shape identity dump (its inputs are unchanged);
  - the author's replay of the hosted jobs;
  - the builder and firmware banks;
  - the full sweep;
  - the Vivado placement;
  - the other reviewers' probe scripts (the author reports them unchanged and passing).
- **Tool versions differ for the CDC check.** My `split-cdc` ran with sv2v v0.0.13 and Yosys 0.66. The author ran sv2v 0.0.12. The results are identical: 253 sinks, 13/13.
- **No physical runs.** Physical calibration NOT RUN. No hardware run. Field skips are not hardware proof.
- **Where the probes ran.** All builds and probes ran in a disposable copy of the clone under the packet's `scratch/`, which is not published.
- **The review clone was not modified**, and I verified it afterwards (receipts/clone-integrity.txt):
  - HEAD is `e6d27f3a`;
  - `write-tree` equals the HEAD tree `dafb16a1`;
  - status is empty, with 0 untracked and 0 ignored entries, and `diff-index` is empty;
  - the submodule gitlinks are as at HEAD. `external` is uninitialized, as it was at the start.

## Pending manager duties

- **Hosted acceptance.** Confirm that the 30 queued and in-progress contexts finish green at the exact head: `rtl-fast`, `verilator-suites` and `yosys-portability`.
- **The merge candidate.** At the merge turn, build and validate the current-dev merge candidate, from source base `a9d69c77` and live dev `0a75aa77`. That is distinct from this source-head review.
- **Carried from round 2**, still open outside this lane:
  - the public Issue for `KL_pp_shadow`'s identical uncounted drop (R791-F4's follow-up);
  - `sw/firmware/ctrl/plat/README.md:137` (S2b);
  - the seven split-leg paths the reviewers' mutants pass (S6b).
- **Stale text next to this round's edit.** Route `docs/testing/PP_SHADOW_BASELINE_RECIPE.md:206-208` ("At `7c1b52be` ... idle ... STOP"). It is not this round's.
- **R792-2's unassigned suggestions** S-1 to S-6: route them, or record them as declined.

## Receipts (paths relative to this packet; listed in MANIFEST.sha256)

- `receipts/split-leg.log`, `.rc`: `make -C tb/verilator/milan_dp split`, pinned Verilator 5.050.
- `receipts/split-mutants.log`, `.rc`: `make split-mutants`, 24 arms.
- `receipts/split-cdc.log`, `.rc`: `make split-cdc`.
- `receipts/pp-placement.log`, `.rc`: `pp_placement_selftest.py`; `pp_baseline.py --selftest`.
- `receipts/probe-p1-no-24-byte.log`, `.rc`: P1.
- `receipts/probe-p2-runt-without-fill.log`, `.rc`: P2.
- `receipts/hosted-check-runs.tsv`: exact-head check runs, read only.
- `receipts/clone-integrity.txt`: the review clone after the probes.
- `scripts/r791_3_probes.sh`: a portable re-run of all of the above on a copy of the clone.

R791-3 FINISHED
