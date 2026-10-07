[R474] POSITIVE - exact head 2525eae9567865a8bc741901914bdf5a1caf2c26

# R474-3: internal cleared-context delta review of PR #672 (Closes #645, #647), round 2d

- **Head and tree.** Head `2525eae9567865a8bc741901914bdf5a1caf2c26`, tree `a0545d5d4f4e098464fbd6a6a7a21fb4c735a423`. Source base `fea346e76c2a57ed5cd131af8fc68dfeff57f877`. Live dev at the head's second parent: `e21c1ca024d37ea188ad15b5c8f9c2dae18628df`. Gitlinks: protocol-processor `ead80360`, gptp-processor `5dce647a`, verilog-axis `48ff7a7e` (`external` is not initialised in this clone, as at the start).
- **Delta under review** (`886e1620..2525eae9`):
  - `2d9f995b`: `pop_dup_w` excludes `pop_hold_w`; a standing `[LRC]` case; controls HELD-DUP and STARVED-HELD-DUP; two `MEDIA_CLOCK_FOLLOWING.md` test-plan rows.
  - `3eee12dc`: R474-2-R1 in `TIME_SYNC.md` and R474-2-R2 in `REGISTER_MAP.md`.
  - `701b8332` and `2525eae9`: `--no-ff` merges of dev `d51b373a` and `e21c1ca0`.
- **Reconstruction order.**
  1. AGENTS.md, CONTRIBUTING.md (sections 3 and 6), docs/README.md.
  2. The #645 body.
  3. The rulings that bound this round: 6032466525 (round 2d), 6041375798 (T1: timing is #691, not this lane), and the scope rulings 6009767440 and 6010634115.
  4. The `[A531] STOP` comment 6041331463.
  5. The delta diff and history, and the full PR footprint against live dev (38 files).
  6. The author packet `review-evidence/645-r1/author-r2d/` (HANDOFF, PR-BODY, area and campaign receipts) and the PR body.
  7. Prior public reviews R474-2 (6032462363) and R475-2 (6031787384), read only after my own pass, probes and lens results were complete. No current parallel review was read.
- **Verdict: POSITIVE.**
  - R474-2-F1 is fixed at this head, under my own execution.
  - Every lens was applied to the delta and is clean.
  - No BLOCKER, MAJOR or MINOR is open.
  - Four wording residues go to the manager's checklist: two new, two carried from R475-2. Three R474-2 suggestions are retained unchanged.
  - The timing gate (IOB pack on `eth0_rx_dv`, #691) is excluded from this round by ruling 6041375798, and is not judged here.

## What the change does, judged against the contract

`KL_chan_map_capture.sv:896-897` now reads `pop_dup_w = pop_visit_w && q_primed_r && q_fed_r && (pop_cnt_w == '0) && !pop_hold_w`.

- **Fan-out.** `pop_dup_w` has exactly one reader, `dup_sum_w` (`:969`), which feeds `lb_dup_cnt_o` (`:1089`). Pops (`pop_act_w`, `:886-887`, which already excluded `pop_hold_w`), hold decrement (`:1083`), drops, the read bank and the wire are untouched. So the change can move only the dup half of `SLIP_LB`.
- **No masking of a genuine slip.** On a held walk the pair's output is the repeat of `lb_hold_r` whatever the queue fill. So every repeat on a held walk is one of the declared `act_hold_r` repeats, and none is extra. Once the hold reaches zero, a starved fed pair counts again with no grace. My probe PR2 (below) shows the cumulative dups per walk as `0 0 0 0 0 1 3`.
- **Contract.** This now matches ruling 6032466525 item 1 ("A settle hold must never move either SLIP_LB counter"), ruling 6009767440 ("the slip counters stay unchanged"), `REGISTER_MAP.md:1870` and the module header (`:250-252`, "neither counter moves").

## Findings at this head

No BLOCKER, MAJOR or MINOR is open.

### R474-3-R1 RESIDUE: the follow_ring mutation driver's docstring under-counts its capture plants

- **Lenses:** Docs (wording only).
- **Where:** `tb/verilator/follow_ring/mutants.py:6-11`.
  - The docstring says the arm has "one on the loopback ring's own recentre (a planted COPY of KL_chan_map_capture.sv through CMAP_SRC)".
  - The driver now plants four capture copies: OVERSHOOT through follow_ring's recipe, and SINGLE-DROP, HELD-DUP and STARVED-HELD-DUP through chmap_capture's (`:75-76`).
  - The usage line (`:6`) omits `--select`.
- **Why wording only:** the docstring changes no code path, check, measurement or verdict. The per-mutant paragraphs below it (`:36-44`) are correct.
- **Exact fix:**
  - Replace "and one on the loopback ring's own recentre (a planted COPY of KL_chan_map_capture.sv through CMAP_SRC)" with "and four on the loopback ring (planted COPIES of KL_chan_map_capture.sv through CMAP_SRC: OVERSHOOT in follow_ring, SINGLE-DROP, HELD-DUP and STARVED-HELD-DUP in chmap_capture)".
  - Make the usage line `mutants.py [--mdir DIR] [--jobs N] [--select NAME ...]`.

### R474-3-R2 RESIDUE: TESTING.md names five of follow_ring's twelve controls

- **Lenses:** Docs (wording only).
- **Where:** `docs/testing/TESTING.md:514`. It reads "then `mutants.py`: the settle recentre never pulsing, reaching the render stage only, firing on the aligner's band ..., W1 ..., and OVERSHOOT ..., each failing a named check".
  - The driver has twelve controls.
  - The authoritative test-plan row (`MEDIA_CLOCK_FOLLOWING.md:1545`) lists all twelve, including this round's HELD-DUP and STARVED-HELD-DUP.
  - This index row predates this round. It was not updated in round 2b or here.
- **Why wording only:** the index row is a summary; no gate, figure or claim of coverage depends on it.
- **Exact fix:** after "each failing a named check", add: "; the full list of twelve, with the check each must fail, is the controls column of the [test plan](../design/MEDIA_CLOCK_FOLLOWING.md#settle-recentre)". The anchor is already used on that row.

### Carried, not new

- **R475-2-R1 RESIDUE (PR body Status), retained with an updated exact fix.**
  - The Status paragraph still says "This head is local until the manager publishes it; it then awaits independent re-review". The head is published (`refs/pull/672/head` = `2525eae9`).
  - It also still states the timing remedy as a recommendation, while ruling 6041375798 has taken T1 as #691.
  - Exact fix: replace those two sentences with "This head is published and awaits independent re-review. The timing gate waits on #691 (ruling 6041375798); this lane merges dev and re-runs the sweep after it lands."
- **R475-2-R2 RESIDUE (`MEDIA_CLOCK_FOLLOWING.md:1086` locator), retained unchanged.** The parenthetical still reads `g_settle_recentre` where it locates the #386 trigger, `g_src_recentre` (`milan_datapath.sv:6533`). This round did not touch it.

## Prior public findings at this head

| Prior finding | Status | Evidence at this head |
|---|---|---|
| R474-2-F1 MINOR: a settle-held walk on a still-empty pair counts a dup | **RESOLVED** | See the four points below this table. |
| R474-2-R1 RESIDUE: TIME_SYNC omits the recovery-window residual | **RESOLVED (meaning preserved; split text accepted)** | See the note below this table. |
| R474-2-R2 RESIDUE: "dropped event" | **RESOLVED verbatim** | `REGISTER_MAP.md:1870` reads "held pops or dropped events count in neither half". |
| R474-2-S1 SUGGESTION: quiet-band floor not pinned to the shipped constant | **Retained (SUGGESTION)** | `settle_control.py` and `quiet_distributions.py` are unchanged since `886e1620`. |
| R474-2-S2 SUGGESTION: no standing shipping-clock quiet or latency evidence | **Retained (SUGGESTION)** | Unchanged since `886e1620`. |
| R474-2-S3 / R474-1-S2 SUGGESTION: physical leg can pass with no decision | **Retained (SUGGESTION)** | `sim_ax1x1gptp.cpp:1101` unchanged. |
| R475-2-R1, R475-2-R2 RESIDUE | **Retained** | See "Carried, not new". |
| R474-1 F1-F4, R475-1 F1-F3 | Resolved in round 2, as both round-2 reviews recorded. | Not reopened: the delta touches none of the artifacts they concern, except `KL_chan_map_capture.sv`'s dup term, and the full-side and span checks still pass (785/0; SINGLE-DROP is caught). |

**R474-2-F1 evidence:**
- RTL `KL_chan_map_capture.sv:896-897`.
- The new `[LRC]` case passes at the head (785/0) and fails on the round-2c term.
- My probes PR1 and PR2 pass at the head and fail on the round-2c term.
- STARVED-HELD-DUP and HELD-DUP are caught by every named check.

**R474-2-R1 note.**
- The exact sentence I proposed in R474-2 exceeds `check_doc_style.py`'s limits for `TIME_SYNC.md`; this round's text passes the gate (`receipts/G_doc_style.log`).
- `TIME_SYNC.md:489-495` states three things:
  - a recentre follows each change;
  - a pull-in starting outside a previous action's recovery gets one;
  - a pull-in starting inside that recovery is the declared residual, and outside it nothing moves the stage.
- That is the content of `MEDIA_CLOCK_FOLLOWING.md:1135-1149`, and line 495 is my wording verbatim.
- "that recovery" refers back across a paragraph break. That is stylistic only and not a finding.

## Independent execution at this head

The tool identity is in `receipts/Z_tool_identity.txt`: Verilator 5.050 through the pinned wrapper. Exact commands are in `scripts/r474_commands.sh`.

| Run | Result | Receipt |
|---|---|---|
| `chmap_capture` (RTL + netlist leg) | 785 checks, 0 failures; `[NC]` 20/0 | `receipts/A_chmap_head.log` |
| Capture controls SINGLE-DROP, HELD-DUP, STARVED-HELD-DUP (lane driver; every named check must fail) | 3/3 caught. HELD-DUP fails the new case, `LRC: no recentre moved the dup counter` and `SPAN: no action counted as a duplicate`. STARVED-HELD-DUP fails the new case and the `[LRC]` counter check. | `receipts/B_mut_capture.log`, `receipts/mutants/` |
| follow_ring controls NO-ARM, NO-RECOVERY, HIGH-ARM, QUIET-ARM, NO-SETTLE, RENDER-ONLY, EARLY, W1, OVERSHOOT | 9/9 caught (12/12 with the above) | `receipts/E_mut_follow_ring.log`, `receipts/mutants/` |
| follow_ring `make run` (b8 set and both switches, pullin, small pulls, settle control at four rates) | All PASS. b8: 1 slip set-to-settle (bound 3), 0 after, margin +5.545..+5.560 ticks, render on the law. Switches: 0 slips, drift under 0.1 tick. Pull-in on the law with 0 loopback slips. Small pulls 10/10. Settle control 4/4 rates. | `receipts/C_follow_ring_run.log` |
| Reviewer probe PR1: eight channels (four pairs), zero left, decision beat only, then a walk | Head: pulsed 0 dups at the walk and 0 dups / 0 skips through the five holds; unpulsed control 3 dups (pairs 1 to 3), so the walk lands before their first commits. Round-2c term: pulsed 3 dups (FAIL). | `receipts/D_probe_head.run.log`, `receipts/D_probe_prefix.run.log` |
| Reviewer probe PR2: no over-suppression after the hold | Head: cumulative dups per walk `0 0 0 0 0 1 3` with 0 skips. Five held walks count nothing; then pair 1 starves (+1), then both pairs starve (+2). Round-2c term: `1 2 3 4 5 6 8` (FAIL). | same |
| Round-2c term against the head suite | Only `LRC: that held walk on a still-empty pair counts no dup` and `LRC: no recentre moved the dup counter` fail among the standing checks. No pre-existing check catches it, so the new case is the one that detects it. | `receipts/D_probe_prefix.run.log`, `receipts/probe_prefix_plant.diff` |
| `capture_coherence` run leg | 20,832 checks, 0 failures | `receipts/F_capture_coherence.log` |
| `media_grid_align` (with its three negative controls) | 45/0; three controls RED as required | `receipts/F_media_grid_align.log` |
| `lint_rtl.py --check` | PASS (90 <= ratchet 90) | `receipts/G_lint_rtl.log` |
| `check_doc_style.py`, `docs_check.py` | OK (22 documents); 0 findings, scrub self-test 23/23 | `receipts/G_doc_style.log`, `receipts/G_docs_check.log` |
| `check_em_dash.py` | Cannot judge: the pinned renderer is not installed here. A scan of the delta's added Markdown lines finds no U+2014. | `receipts/G_em_dash.log` |
| Merge audit | `701b8332` and `2525eae9` each record exactly the automatic `merge-tree` result of their parents. The merges change only `sw/firmware/**`, `tb/verilator/mbx/Makefile` and `docs/design/MAILBOX_SPLIT.md`; no HDL. The PR footprint against live dev stays 38 files. | `receipts/H_merges.log` |
| Author area receipt | Judged as published: `cmc_head.sv` sha256 `2b07955b` equals the head's `KL_chan_map_capture.sv`; `cmc_base.sv` `7f21dd43` equals dev's. +113 LUT / +78 FF, conservative +119 / +82, against 120 / 120. | `author-r2d/round2d/area-ooc/comparison.json` at `65b9e8ee` |
| Author campaign receipt | Judged as published: 128/128 and 32/32 byte-identical to round 2c; quiet JSON identical. This is consistent with the change's sole fan-out being the dup counter. | `author-r2d/round2d/campaigns/campaign-compare.json` at `65b9e8ee` |
| Hosted, exact head (read only, snapshot 2026-10-07T16:03Z) | Success: rtl-fast, changes, bdd-conformance, docs-check-no-git, firmware-unit, full-ci-gate, verilator-lint, wire-accountability, yosys-elaboration, Yosys 4/4, Verilator shard 3/5. **In progress:** docs-check, elaborate, Verilator shards 0, 1, 2 and 4. **Skipped, not executed:** Physical gPTP. | `receipts/I_hosted_checks_2525eae9.tsv` |

## Lens results

```text
[R474] PASS Conformance - hdl/ieee1722/aaf/KL_chan_map_capture.sv:885-897,969,1083-1090; rulings 6032466525 item 1, 6009767440, 6041375798; REGISTER_MAP.md:1870 - held walks never move either SLIP_LB half (probes PR1/PR2, [LRC] 785/0); genuine starvation after the hold still counts; pops/holds/drops/wire unchanged; timing excluded by ruling
[R474] PASS RTL - hdl/ieee1722/aaf/KL_chan_map_capture.sv:877-913,963-969,1076-1104 - single fan-out of pop_dup_w (dup_sum_w only); no width, reset, flush or same-cycle effect; lint ratchet 90<=90; merges carry no HDL (merge-tree equality)
[R474] PASS Robustness - reviewer probes PR1 (four pairs, three still empty), PR2 (stream stops at the decision beat: hold then starvation), round-2c term fails both; capture_coherence 20832/0; media_grid_align 45/0 with 3 controls; flush and first-beat [LRC] cases pass
[R474] PASS Tests - tb/verilator/chmap_capture/sim_main.cpp:1706-1801 (new case with no-pulse reachability control); tb/verilator/follow_ring/mutants.py:68-127,141-175 (all-named-checks kill rule) - 12/12 controls caught; the round-2c term survives every pre-existing check and is caught only by the new case
[R474] PASS Docs - MEDIA_CLOCK_FOLLOWING.md:1545-1546; TIME_SYNC.md:486-495; REGISTER_MAP.md:1870; KL_chan_map_capture.sv:894-895; PR body round-2d section; author-r2d HANDOFF - claims match my runs (785 checks, controls, probe P1 result, area hashes); R474-3-R1/R2 and the carried R475-2 residues are wording only
```

## Reviewer-owned completion ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #645 acceptance; rulings 6032466525, 6041375798, 6009767440, 6010634115; `KL_chan_map_capture.sv:885-897, 969, 1083-1090`; `REGISTER_MAP.md:1870`; `TIME_SYNC.md:486-495` against `MEDIA_CLOCK_FOLLOWING.md:1135-1149`; probes PR1/PR2 | R474-3 | 2525eae9567865a8bc741901914bdf5a1caf2c26 |
| RTL | CLEAN | `KL_chan_map_capture.sv:195-255, 801-1104` (pop, hold, dup, drop, counter, flush, reset); lint ratchet; merge-tree audit of `701b8332` and `2525eae9` (no HDL) | R474-3 | 2525eae9567865a8bc741901914bdf5a1caf2c26 |
| Robustness | CLEAN | PR1 (four pairs, three still empty); PR2 (stream stops after the decision beat); round-2c term against both; `[LRC]` flush, unprimed and first-beat cases; `capture_coherence`; `media_grid_align` | R474-3 | 2525eae9567865a8bc741901914bdf5a1caf2c26 |
| Tests | CLEAN | `chmap_capture/sim_main.cpp:1706-1801`; `follow_ring/mutants.py` (12 controls, all-checks kill rule); follow_ring `make run`; reviewer probes on head and on the round-2c term | R474-3 | 2525eae9567865a8bc741901914bdf5a1caf2c26 |
| Docs | CLEAN (RESIDUE R474-3-R1, R474-3-R2, R475-2-R1, R475-2-R2 carried) | `MEDIA_CLOCK_FOLLOWING.md:1086, 1135-1149, 1545-1546`; `TIME_SYNC.md:486-495`; `REGISTER_MAP.md:1870`; `TESTING.md:514`; `follow_ring/mutants.py:4-44`; PR body; author-r2d HANDOFF and receipts; doc style and docs_check gates | R474-3 | 2525eae9567865a8bc741901914bdf5a1caf2c26 |

**Scope of this ledger.** This is a delta round.
- Every lens was applied to every artifact the delta changes, at this head.
- The artifacts outside the delta are byte-identical to `886e1620`, which R474-2 covered. Its NEGATIVE ledger there was unclean only because of F1, which is now resolved. R475-2 covered the same head CLEAN.
- The two dev merges add no artifact in any lens's lane scope beyond firmware, `mbx` and one mailbox design note. Those are outside #645, and their own PR's review covers them.

## Real limits

- **No hardware or bench claim.** Physical calibration was NOT RUN. Field skips and skipped hosted contexts (Physical gPTP) are not evidence. #645's bench repeat of the INTERNAL-to-AAF and AAF-to-CRF switches is still open.
- **Timing not judged.** The BUILDING.md section 5 sweep fails at the IOB-pack check on `eth0_rx_dv` at this head. Ruling 6041375798 assigns that to #691 and excludes it from this round. A later delta must re-run timing after #691 merges.
- **Not re-run by me:**
  - the full parent, PP, gPTP, Yosys and builder banks;
  - the 128-phase arrival and 32-run pull-in campaigns (judged from the author's byte-identical comparison);
  - the area OOC (judged from the published receipts and input hashes);
  - the physical `milan_dp` legs, the render pull-in and the LAW-boundary leg.
- **Em-dash gate** could not run (renderer absent). A manual scan of the added lines replaces it.
- **Evidence link.** The assignment's evidence link pins `6efdd244`, which predates the round-2d packet. I read `author-r2d/` at the evidence branch head `65b9e8ee`, which descends from `6efdd244`. Fetching that branch added objects and `FETCH_HEAD` to this clone's Git metadata only; no tracked content changed.
- **Hosted runs in progress.** Some hosted runs were still in progress at my snapshot. I infer no hosted success from local success.

## Pending manager duties

- Carry R474-3-R1, R474-3-R2, R475-2-R1 (updated fix above) and R475-2-R2 to the residue checklist.
- Land #691, merge dev into this lane, re-run the BUILDING.md section 5 timing sweep, and have the resulting delta reviewed.
- See the exact-head hosted runs that were still in progress through to completion (docs-check, elaborate, Verilator shards 0, 1, 2, 4), plus act acceptance.
- Build and validate the final current-dev candidate at the merge turn.
- Reconcile with the companion external review, and obtain two independent POSITIVE reviews with an all-lens ledger at the merge candidate.
- Obtain explicit maintainer merge authorization, then run post-merge containment.
- Run the #645 and #647 physical bench repeats. "Closes #645/#647" must not discharge them.

## Restoration

- No source edit, commit, push or GitHub write was made. All plants and probes ran in disposable copies under this packet's `scratch/`. Suite builds used `MDIR`/`NETDIR` there too.
- `scripts/verify_checkout.py` passed (`receipts/Z_checkout_verify.json`):
  - 1,178 tracked blobs, with bytes and modes equal to the index;
  - the index tree equals HEAD's tree, `a0545d5d`;
  - gitlinks protocol-processor `ead80360`, gptp-processor `5dce647a` and verilog-axis `48ff7a7e` match their checkouts, and their worktrees are clean (`receipts/Z_submodule_status.txt`);
  - `external` is uninitialised, as it was before the review;
  - `git status --porcelain --ignored` is empty.
- Local paths in the receipts are normalised to `<clone>`, `<packet>` and `$HOME`.

R474-3 FINISHED
