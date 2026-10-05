[R494] POSITIVE - exact head 79571006b803a4ab4af65358f0d87bc3af73180e

# R494-1: internal independent review of PR #161 (issue #158)

- Repository: Mister-M-alt/protocol-processor-control-plane-avb-milan, PR #161, branch `pp158-dereg-round`.
- Exact head `79571006b803a4ab4af65358f0d87bc3af73180e`, tree `be060640b23bb505b75debc192d7d36505fbe5dd` (verified in the
  review clone). Source base `main` `054d01c79e59c3f80454ad9cdefd8e914b540bb4`. Merged main `21c6f709` (C11).
- Review start: PR #161 comment 5999676619. Round R494-1, cleared context, own clone, no contact with the author or the
  other reviewer.
- Scope read, in order: the repository has no AGENTS.md or CONTRIBUTING.md (none tracked). Then `docs/README.md`, issue #158
  (body, assignment 5991577974, STOP 5997973952, area ruling 5997990838, REVIEW READY 5999645465), the PR body, and
  `docs/architecture/06_aecp_engine.md` section 7 (the registry and notification authority, with Milan Table 5.22 and
  §5.4.2.21 as cited there). Then the diff `054d01c7..79571006` and its history (5343cd7, 27992ce, 3dbc229, e3c9f0b, merge
  7957100), and the public evidence `kebag-logic/milan-fpga@877208b6:review-evidence/pp158-r1` (MANIFEST.json, HANDOFF.md,
  PR-BODY.md, five parent-adoption patches). Every published sha256 matches MANIFEST.json (`receipts/env.txt`).
- Prior public review findings on PR #161: none exist at this head. The PR has no review, no review comment, and no
  issue comment except the two review-start notices.

## Verdict

POSITIVE. The fix is one logic line, `KL_aecp_notify.sv:1253`: `if (dh_v_r)` becomes `if (dh_v_r && !em_active_r)`. A
DEREGISTER drained mid-round is now held to the round's boundary, so the round's `em_*` state is never overwritten mid-round.
Each issue acceptance item and each check the assignment asked for holds at the exact head, verified by this reviewer's own
runs:

| Check asked for | Result at the head (reviewer's own run) | Receipt |
|---|---|---|
| Red at `main` and green at the head, for a GET_COUNTERS round and a non-counter round | Head `tb/aecp_notify`: 45 of 45 pass, rc 0. Main's RTL under the head bench, and 5343cd7 exactly: rc 2, `41 checks, 3 failures` (DR1 GET_COUNTERS/TIME_LIMITED, DR2 SET_NAME/failed CA retry, DR3); DR1b and DR2b pass on main | `receipts/bench/aecp_notify-{head,red-main,red-5343}.log` |
| The no-restore mutant fails | `dereg_mid_round_no_hold` (main's rule) KILLED: fails DR1, DR2, DR3 | `receipts/camp/notify_mutants/dereg_mid_round_no_hold.log` |
| The targeted controller's own DEREGISTER semantics are kept | DR1b and DR2b pass: C alone, once, kind 0, 0000:0, sequence_id 1. The reviewer's 3-row probe adds P1 to P3 (seq 1 and seq 0 cases, two drains in one round): all pass. `dereg_lost_at_round_end` KILLED | `receipts/bench/probe-head.log` |
| The stamp follow carries through the DEREGISTER job (R477-1 S2) | DR3: D's next GET_COUNTERS at 32508, 1,004 ms after D's send at 31504 (window 32504 to 32512). `dereg_pending_stops_follow` KILLED (31512). Probe P5 (3 rows, last job waits 1.5 s): next round 1,004 ms after the round's last send | `receipts/bench/aecp_notify-head.log`, `probe-head.log` |
| Area: own logic -3 LUT / +2 FF; +50 whole-OOC variance recorded only (ruling 5997990838) | The per-row table adds up exactly. Only `u_notify`'s RTL changed between base and the measured head. See C-AREA below | `receipts/lane-notify-rtl.diff`, `receipts/focused/*` |
| Every mutation arm plants at the head (476 + 96) | 476 of 476 (277 patches through `git apply --check`, plus notify/d3/acmp arms through each driver's own `plant()`) and 96 of 96. At `054d01c7` and `21c6f709`: 473 + 96. The arm lists differ only by the three new controls. 54 of 54 notify-planting arms plant the same design at base and head | `receipts/plant-check-*.log`, `receipts/planted-identity.log` |
| Main merge 21c6f709 (C11) is comment-only in RTL | Tree `be060640` equals `git merge-tree` of the two parents (a clean auto-merge, no evil merge). Lane and C11 patch-ids are unchanged (`7fee3918...`, `dd11bb40...`). Comment-stripped preprocessor output of the three C11 RTL files and `tb/tx_slots/sim_main.cpp` is byte-identical, and the RTL line counts are unchanged | `receipts/c11-comment-only.log` |

## Lens results

### Conformance (CLEAN)
- Milan Table 5.22 ("sent only to this controller") and §5.4.2.21 (per-entry sequence_id) are kept.
  - The held DEREGISTER still goes to the latched `dh_eid_r`/`dh_mac_r` with `dh_seq_r`, kind `PP_UNS_DEREG_C` and
    0000:0 (`KL_aecp_notify.sv:1258-1267`).
  - Its write-back still only clears `dh_v_r` and writes no row (`:1464-1465`), so a row reused during the hold is not
    corrupted.
  - Graded by DR1b/DR2b and probe P1-P3.
- Every remaining controller of the round now receives the round's notification, every field intact. This holds for both
  drain sources (TIME_LIMITED expiry: DR1; failed CONTROLLER_AVAILABLE retry: DR2) and for counter and command rounds.
- #148's one-second GET_COUNTERS rule holds from the round's last send (DR3, P5).
- Only the timing of the DEREGISTER moves. Its residual (a re-registration inside the hold window receives the stale
  DEREGISTER) is disclosed in the PR body. See SUGGESTION S1.

### RTL (CLEAN)
- The one-term gate is correct.
  - While `em_active_r`, `N_IDLE` takes the round's next job (`wk_ix_r <= em_ix_r`, `:1318`) with the round's `em_*`
    unchanged.
  - When the round ends (`em_active_r` cleared at `:1430` or `:1470`), the DEREGISTER arm is checked before any new claim.
    The branch above it, `pd_any_w && !dh_v_r` (`:1247`), stays blocked while the DEREGISTER is held, and `rgy_new_w`
    claims no round.
  - There is no deadlock: the round is bounded by `N_CTRL_P` rows.
  - Reset clears `dh_v_r` (`:1013`).
  - `amap_busy_o` (`:958`) already covers the round through `em_active_r`.
- No port, parameter or register changed: the diff is one condition plus comments.
- Focused lint, with `lint_hdl.sh`'s exact command and the pinned Verilator 5.050: `KL_aecp_notify` and
  `protocol_processor_top` are LINT OK at head and main.
- Yosys `synth_xilinx` of the module alone at default parameters (a proxy, not the area authority): FDRE 1732 to 1732, and
  the LUT count does not grow.

### Robustness (CLEAN)
- Edge cases beyond the committed two-row bench were probed with `N_CTRL_P`=3 (`scripts/probe/`):
  - P1: a hold across two remaining jobs.
  - P2: a drain of a not-yet-served row. That row receives only its DEREGISTER (seq 0), and the others keep the round.
  - P3: two drains in one SET_NAME round. The second drain waits for the first DEREGISTER, as disclosed. Both DEREGISTERs
    carry their own seq 1, and the arguments stay 2/3.
  - P4: a re-registration during the hold. The round stays intact, and the stale DEREGISTER arrives 8 ms after the
    re-registration, as disclosed.
  - P5: the stamp follow.
- Head: 9 of 9 pass. The same probe on main's RTL: 6 failures (`receipts/bench/probe-main-rtl.log`).
- `tb/pp_top` (six builds) at the head: 10,444 of 10,444, rc 0.

### Tests (CLEAN)
- Section DR has 11 checks: five named plus six REGISTER checks. DR1 reproduces the issue's probe trace on main (C seq 1
  DEREGISTER, then D kind 0 0000:0 seq 0).
- The checks accept either order, so they grade semantics, not the chosen fix.
- The notify campaign at the head (`--jobs 6`): 56 of 56 KILLED, 7 goldens PASS. The records match the PR and READMEs:
  - the three new controls fail DR1/DR2/DR3, DR3, and DR1b/DR2b;
  - the three TW controls add DR3 at 31512.
- The ctr campaign (`--jobs 3`): control PASS, 17 of 17 KILLED.
- The other arms that plant into the notify RTL were also run: `aecp_mutants --only fanout-never-ends` (control PASS,
  KILLED) and `d3_mutants --only registry_survives_reset lock_survives_reset` (2 of 2 KILLED, golden PASS).

### Docs (CLEAN, with one RESIDUE)
- 06 section 7 (`:887-889`), the RTL banner (`:126-130`), the `tb/aecp_notify` and `tb/pp_top` READMEs, and 09 section 8.4
  ("five of the notification block's": FT, IX, TS, TW, DR) agree with the RTL and with the reviewer's runs. This covers
  every ms figure, the 11-check count, "all thirteen KILLED" (13 rows), and 56 of 56.
- Every line reference in the PR body matches the head.
- The 68-flop save/restore estimate checks out: 4 + 4 × 16 bits for `em_kind_r`, `em_dt_r`, `em_di_r`, `em_arg0_r`,
  `em_arg1_r`.
- Docs gates at the head, run in a disposable clone: links (1,168), matrix (115 REQ, 17 GAP), modmatrix (94 rows,
  0 untested), params (28), ids (selftest 30; 531 files, 91 IDs), figures (selftest 17; 3 + 18 + 5), stale and lint (41
  Mermaid + 18 WaveDrom) all rc 0.
- One wording defect is recorded as RESIDUE R1.

### C-AREA: attribution check
- The per-row table adds up exactly:
  - rows: -1 + 121 + 44 + 30 + 19 + 14 + 6 + 2 + 2 - 5 - 5 - 4 - 1 - 8 - 10 - 15 - 16 - 17 - 27 - 79 = +50 LUT;
  - `u_pp` -4 FF, plus `KL_pp_shadow` own -2 FF, gives the whole delta of +50 / -6;
  - the sub-rows of `u_srp` (+30), `u_dispatch` (+19) and `u_aecp` (-5) add up too.
- `git diff --stat 054d01c7 e3c9f0b -- hdl` names only `hdl/aecp/KL_aecp_notify.sv`. So every LUT increase sits in rows
  whose RTL is unchanged, and the changed row (`u_notify`) moves -1 / -3.
- The module-alone figures (2,474/1,280 to 2,471/1,282) give -3 / +2, inside 40 LUT / 60 FF.
- The PR body states both figures, as the ruling requires.
- C11 changes no synthesis input (comment-only, verified), so not re-measuring after the merge is justified.
- Limit: this host has no Vivado, and the raw `baseline_hierarchy.rpt` reports are not in the public evidence. The figures
  themselves are the author's measurement. They were checked for consistency, not reproduced.

## Findings

| ID | Severity | Lenses | Location | Authority / evidence | Impact | Required outcome | Verification |
|---|---|---|---|---|---|---|---|
| R1 | RESIDUE | Docs | `docs/architecture/09_verification.md:316` (DR row) | The bench (`tb/aecp_notify/sim_main.cpp:664-668`) and its README hold the round's job after the drain (D's) for the TX slot. "the drained row's next job" names the drained controller C instead, and "that controller" then has no clear antecedent | Prose only: no figure, check or claim changes | Replace "and with the drained row's next job held for the TX slot the next counter round still waits a second from that controller's send" with "and with the round's job after the drain held for the TX slot the next counter round still waits a second from that job's send" | Read the row against `sim_main.cpp:664-702` |
| S1 | SUGGESTION | Conformance, Docs | `docs/architecture/06_aecp_engine.md:887-889`; `KL_aecp_notify.sv:1248-1250` | Probe P4: C re-registers at ms 60210 and receives the held DEREGISTER at ms 60218. The PR body's "What remains" discloses this. `main` had the same ordering in a one-job window | A controller can briefly believe it is deregistered while its row is live. The window is now the rest of a round | Optionally record this residual and the delayed second drain in 06 section 7 rather than only in the PR body. The maintainer could later withdraw a held DEREGISTER when the same tuple re-registers. The drain comment's "a little late" could say "up to the round's end" | Doc read; `receipts/bench/probe-head.log` P4 |
| S2 | SUGGESTION | Tests | `tb/aecp_notify` section DR (`N_CTRL_P`=2) | With two rows, every hold is one job long, and the drained row is always already served | Coverage only: the reviewer's 3-row probe passes at the head and fails on main | Optionally add P2 (an unserved row drained) and P3 (two drains in one round) style checks in a 3-row build | `scripts/probe/probe_main.cpp`, `receipts/bench/probe-*.log` |

No BLOCKER, MAJOR or MINOR finding is open. RESIDUE R1 goes to the manager's residue checklist with the exact fix above.

**Carried scope finding, read after this review's own pass and verdict.** PR #159's review R477-1, item S2 (SUGGESTION,
Robustness and Conformance), was carried to #158. It asked that #158's fix keep the GET_COUNTERS stamp following through an
interleaved DEREGISTER job, graded by a TW-style check. It is **resolved at this head**:
- the hold leaves no DEREGISTER job inside a round, so the follow at `:1449` runs for every job of the round;
- DR3 is the TW-style check (passes at the head, fails on main);
- the control `dereg_pending_stops_follow` plants S2's hazard and is KILLED by DR3.

## Reviewer-owned ledger

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | issue #158 acceptance and the ruling; 06 section 7 (Milan Table 5.22, §5.4.2.21); `KL_aecp_notify.sv:1191-1474`; DR1b/DR2b; probe P1-P5 | R494-1 | 79571006b803a4ab4af65358f0d87bc3af73180e |
| RTL | CLEAN | lane diff (`receipts/lane-notify-rtl.diff`); FSM `N_IDLE`/`N_EMIT_*`/`N_DRAIN`; focused lint; Yosys proxy; C11 comment-only check; merge-tree identity; area table arithmetic | R494-1 | 79571006b803a4ab4af65358f0d87bc3af73180e |
| Robustness | CLEAN | 3-row probe at head vs main RTL; `tb/pp_top` 10,444; parked-drain, withdrawal, row-reuse and reset paths | R494-1 | 79571006b803a4ab4af65358f0d87bc3af73180e |
| Tests | CLEAN | `tb/aecp_notify` red/green (head, main RTL, 5343cd7); notify 56/56 + 7 goldens; ctr 17/17 + control; aecp fanout-never-ends; d3 2/2; plant 476 + 96; planted identity 54/54 | R494-1 | 79571006b803a4ab4af65358f0d87bc3af73180e |
| Docs | CLEAN (RESIDUE R1 carried) | 06 section 7, RTL banner, `tb/aecp_notify` and `tb/pp_top` READMEs, 09 section 8.4, PR body line references and figures; docs gates (links, matrix, modmatrix, params, ids, figures, stale, lint) | R494-1 | 79571006b803a4ab4af65358f0d87bc3af73180e |

## Real limits
- Not run, by rule: the full `scripts/run_suites.sh` bank (33 suites), the full lint and Yosys banks, and the parent
  consumer set of 17. Lint was run for the changed module and the top only, and Yosys for the module alone.
- Not run: `make wavedrom-check`, because it bootstraps a Python venv in the tree. The other `make check` targets ran.
- Not run: the d3, aecp, aecp_dispatch, acmp, gsi, name_wr, adp and maap campaigns as a whole. Only their arms that plant
  into `KL_aecp_notify.sv` ran.
- No Vivado on this host. The OOC 1x1 figures are checked for arithmetic and attribution, not reproduced. The raw
  hierarchy reports are not published.
- Parent consumer at dev `28f9666f`: the reviewer only checked that `parent-adoption-148-6c22d3ca.patch` applies
  (`git apply --check` clean against the files fetched at `28f9666f`) and is not yet in dev. The c8, c10 and p2-p1 patches
  do not forward-apply, and the 232 patch reverse-applies, which fits #661 having brought those adaptations into dev. No
  consumer gate was run.
- Hosted CI at the exact head, as of review end: `docs-gates` and `portability` completed with success (runs 37348944062 and
  37348936371, jobs executed, none skipped). `suites` was still in progress in both runs. No physical calibration, no
  hardware, and field skips are not hardware proof.

## Pending manager duties
- Final current-dev candidate at the merge turn (source base `054d01c7`, live dev `28f9666f`, only the 148 bench patch),
  with the consumer gates.
- Hosted/act acceptance, including the two `suites` jobs still running at review end.
- Carry RESIDUE R1 to the residue checklist. Decide on S1 and S2 (optional).
- Merge requires the second independent review (R495) and the full completion bar.

## Reproduction (portable scripts under `scripts/`)
- `scripts/bench_red_green.sh REPO SCRATCH OUT VERILATOR`: DR red/green at the head, main's RTL, and 5343cd7.
- `scripts/campaign.sh` / `scripts/campaign_path.sh REPO SCRATCH OUT {VERILATOR|BINDIR} DRIVER JOBS`: a campaign from a
  `git archive` of the head.
- `scripts/plant_check.py TREE`; `scripts/planted_identity.py BASE_TREE HEAD_TREE LANE_DIFF`.
- `scripts/c11_comment_only.sh REPO SCRATCH VERILATOR`; `scripts/focused_lint_yosys.sh TREE OUTPREFIX VERILATOR`;
  `scripts/pp_top_make.sh`; `scripts/probe/run_probe.sh TREE OUTLOG VERILATOR`.
- Tools: Verilator 5.050 (pinned wrapper, identity verified with `--version`; sha256 in `receipts/env.txt`). Absolute host
  paths in receipts are replaced by `$PACKET`, `$CLONE`, `$TOOLS`, `$HOME` and `$VERILATOR_IMAGE`.
- After the probes, the review clone was verified at exact head `79571006` with tree `be060640`. The index entries (modes,
  blobs, paths) equal the HEAD tree, the worktree equals the index, and `status --porcelain --ignored` is empty. The
  repository tracks no submodule gitlinks (0 mode-160000 entries). Every probe ran in disposable extractions under the
  packet's `scratch/`.

R494-1 FINISHED
