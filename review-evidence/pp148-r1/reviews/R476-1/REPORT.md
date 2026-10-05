[R476] NEGATIVE - exact head bed5f47785839800bb640d7c747f5435f84ab5a3

# R476-1 internal independent review: processor issue #148 / PR #159

- Repository: Mister-M-alt/protocol-processor-control-plane-avb-milan, PR #159, branch `pp148-notify-spacing`.
- Exact head `bed5f47785839800bb640d7c747f5435f84ab5a3`, tree `1bc22d81da063fc5288627a54c2cca502808a826` (verified in the isolated clone).
- Source base `07b1469ddf1e2a54e4a42cac06c41f084ecffd6c`. The merges of `b0a74196` (#157) and `ead80360` (#155) are part of the head.
- Review start: PR #159 comment 5988345432.

**Verdict: NEGATIVE.** One MINOR is open (R476-1-F1, lenses RTL and Docs): a stale RTL comment on the selection stamp still states the pre-#148 rule. Everything else is in order:

- The fix is correct and minimal.
- Both new sections are red at main and green at head.
- Every planted mutant is killed.
- The merges are true unions.
- The area is inside the stop.
- The parent bench change is right and bounded.
- The PR does not worsen #158.

Two SUGGESTIONs are recorded. They do not affect the verdict.

## 1. Reconstruction (order followed)

1. **Contributor guidance.**
   - The repository has no `AGENTS.md` or `CONTRIBUTING.md` at this head (`git ls-files`).
   - The contributor rules are in `README.md`, `docs/README.md` (conventions, single-source rules), `docs/guides/hdl-engineer.md` (banners are primary) and `hdl/README.md`.
2. **Frozen acceptance and scope.**
   - Acceptance (issue #148 body):
     1. Spacing is measured send to send and is never less than the clause's bound.
     2. A check is red today, with a mutant that restarts the spacing at selection.
     3. The existing notification suites and campaigns stay green.
   - Manager comment 5982500256 (assignment): smallest change; no port, register or parameter change; scope is counter notifications only; area stop at 40 LUT / 60 FF; parent set of 17.
   - Manager comments 5985998608 and 5986055260: round 1b, i.e. merge `b0a74196`, then `ead80360`, and re-measure over the union.
   - Executor REVIEW READY 5988331719 and the PR body.
3. **Authorities** (read in local text extractions; hashes in `receipts/environment.txt`).
   - **Milan v1.2 §5.4.5.2, Table 5.22.** GET_COUNTERS is "Sent when one of the counters is updated, with the restriction of not sending more than one unsolicited notification per descriptor per second". §5.4.5.1 defines one notification as the fan-out of one message per registered controller.
   - **IEEE 1722.1-2021 §7.5.2.** Lists GET_COUNTERS among the commands that generate unsolicited notifications. It contains no rate limit, so the one-second bound comes from Milan Table 5.22 alone. The PR, the RTL comment (`:1439`) and 08 F08.1 (`T-CTR-NOTIF`) all cite Table 5.22. The issue body's "§7.5.2 rate-limit" wording is the issue's, not the PR's.
   - **08 §3.** All protocol timers have 1 ms resolution.
   - **Recorded project decision on the one-tick tolerance** (`tb/pp_top/README.md:2406-2410`, "review R420-1 S4, retained"). It counts the limiter on the 1 ms timebase: rounds are at least 1,000 ticks apart, which in core clocks is at most one tick short of a second.
4. **Diff and history.**
   - `git diff 07b1469d..bed5f477`: 26 files.
   - The lane's own delta against the merged main `ead80360` is 9 files, +341 -41.
   - HDL: only `hdl/aecp/KL_aecp_notify.sv`, +9 -1.
   - First-parent chain: `abbe55b`, `82e1664`, `5f458aa`, `221fd63`, `a369cdd`, then merge `415a9fd`, merge `4ed463b`, then `bed5f47` (README only).
5. **Public evidence.**
   - Location: kebag-logic/milan-fpga `1de9179a`, `review-evidence/pp148-r1`.
   - Every one of the 216 `MANIFEST.json` entries matches its `published_sha256`, with no unlisted and no missing files.
   - The executor's receipts were read for the gates I did not re-run (section 6).
6. **Prior public findings.**
   - At this head the PR has no review comments and no reviews, and the issue has no review findings. Nothing earlier had to be resolved or retained.
   - The other reviewer's concurrent report was not read before this verdict and ledger were written.

## 2. What the fix does (RTL reading, `hdl/aecp/KL_aecp_notify.sv`)

- **`:469`, `:1043`, `:1297`.** New register `em_ctr_ix_r` holds the claimed round's descriptor slot. It is `CTX_W_C` bits wide, 3 bits at the 1x1 binding (N_STREAM_IN_P = 2, N_STREAM_OUT_P = 2, so 6 slots). It is reset with the other `em_*` registers and latched at the claim.
- **`:1443`, the new stamp line.** In `N_EMIT_WAIT`: `if (em_kind_r == PP_UNS_CTRS_C) ctr_last_r[em_ctr_ix_r] <= now_ms_i;`.
  - The stamp follows the clock while a counter job waits for the engine and the TX slot.
  - It holds the ms of the job's retirement, `core_done_w`.
  - The engine raises `uns_done_o` at `A_FREE`, after `A_TXW` sees `txreq_uns_ready_i`, which is `arb_gnt_w[LANE_AECP_UNS_C]` (`protocol_processor_top.sv:4481`).
  - The arbiter's grant starts the frame and streams it with no preemption (`KL_pp_tx_arbiter.sv` banner).
  - So "send" means the TX grant, as the PR states. The residual about a MAC stall after the grant is disclosed accurately.
- **Window check.** `:1099-1101` is unchanged. The next round of a descriptor is pended at the first ms with `now - ctr_last >= 1000`, so it starts at least 1,000 ticks after the previous round's last grant. Each controller's frame in round n is no later than that last grant, so per-controller spacing follows.
- **Mutual exclusion.**
  - The selection stamp (`:1302`, `N_IDLE`) and the new stamp (`N_EMIT_WAIT`) are written in mutually exclusive FSM states.
  - The new stamp writes only when `em_kind_r` is GET_COUNTERS. That kind is set only at a GET_COUNTERS claim, together with `em_ctr_ix_r`, so no stale slot is ever written.
  - The DEREGISTER single-shot path rewrites `em_kind_r`, which stops the stamp.
  - The `ctr_sent_r` valid bit is still set in the claim cycle, so the "stamp read only once valid" invariant (`:399-402`) holds.
- **No port, parameter or register change.** The module header is unchanged. The executor's provenance receipt says the port and parameter declarations are byte-identical to `07b1469d`. The parent port gate reads 1,759 ports at both base and head.
- **Scope statement holds.**
  - `ctr_last_r` is read and written only on the GET_COUNTERS path.
  - IDENTIFY_NOTIFICATION's spacing is a separate path. `gen_ident` `:800-814` schedules each frame from its departure (`dep_w` uses `uns_tx_busy_i`) with a +1 ms margin.
  - No other Table 5.22 kind is rate-limited.
  - So no other notification kind shares this code path.

## 3. Executed evidence (this review)

Every run used the pinned Verilator 5.050 (identity checked with `--version`), in disposable extractions of the exact head under the packet's `scratch/`. The "main RTL" tree is the head's benches with `07b1469d`'s `KL_aecp_notify.sv`. That file is byte-identical at `ead80360`, so it is also main's RTL after #155 and #157.

| Run | Main RTL | Head | Receipt |
|---|---|---|---|
| `tb/aecp_notify` `make run`, section TW | rc 2. FAIL TW1: next round at ms 3005, want 3600-3608. FAIL TW2: ms 6508, want 7504-7512. | rc 0. TW1 at 3603, TW2 at 7507. 30 + 4 checks, 0 failures. | `receipts/sections2/*-aecp_notify.*` |
| `tb/pp_top` `--spacing-only`, section CS | rc 1. CS2a passes at 99,994. FAIL CS2b at 99,854 and CS2c at 99,590, want ≥ 99,900. | rc 0. 115,077 / 115,070 / 115,077. CS: 9 checks, 0 failures. | `receipts/sections2/*-pp_top-spacing.*` |
| `notify_mutants.py`, all 53 arms, `--jobs` 6-10, in four chunks | n/a | 53 of 53 KILLED, every golden PASS (aecp_notify run and identify, originator, pp_top notify-only, spacing-only, identify-only, identify build) | `receipts/campaigns/head-notify-*.log`, `receipts/campaigns/results/` |
| The six new #148 controls | n/a | `counter_spacing_from_selection`: CS2b, CS2c. `_tw`: TW1, TW2. `counter_stamp_at_send_only`: TW2. `counter_stamp_first_job_only`: TW1, TW2 (TW2 at 7503 vs ≥ 7504). `counter_limit_500ms_cs`: CS2a-c at 75,504. `registry_holds_15_cs`: CS1 x3 and CS2a-c. All KILLED. | `receipts/campaigns/results/head-counter_*.log`, `head-registry_holds_15_cs.log` |
| `counter_limit_500ms` record | n/a | 7 failing checks (ST2b x5, ST3, ST3b), as the PR says | `receipts/campaigns/results/head-counter_limit_500ms.log` |
| `ctr_mutants.py --jobs 5` | n/a | control PASS, 17 of 17 KILLED. `ctr-notify-one-window` at 4 failures, as the PR says. | `receipts/campaigns/head-ctr.log` |
| `--arm-queue-only`, section AQ | rc 0, 8,270 arms issued | rc 0, 8,273 arms issued. Every other AQ figure is identical. | `receipts/aq/` |
| #158 probe (the executor's published diff) | `[x]` trace: job 1 GET_COUNTERS to C, then DEREGISTER (kind 0) to C seq 1 and to D seq 0 | identical trace; rc 0 with TW green | `receipts/probe-158/` |
| `lint_hdl.sh`; `make check`; `gen_matrix.py --check` | n/a | rc 0. Lint: 41 of 41 `LINT OK`. `make check`: 1,136 links, 115 REQ, 17 GAP, 94 rows, 0 untested, 28 parameters. | `receipts/static/head-*` |
| Merge trees | n/a | See below | `git merge-tree --write-tree` |

Merge trees:

- **`415a9fd`** (parents `a369cddd`, `b0a74196`): the tree equals git's clean auto-merge, `64d2c466…`.
- **`4ed463b`** (parents `415a9fdd`, `ead80360`):
  - The only conflict is `tb/pp_top/sim_main.cpp`.
  - The resolution differs from the conflicted auto-merge only by keeping both flags: `spacing_only` and `aq_only`, and `|| spacing_only || aq_only`.
  - `git diff ead8036 4ed463b -- tb/pp_top/sim_main.cpp` is exactly the lane's 4-line `--spacing-only` delta.
- **`4ed463b..bed5f47`**: changes only `tb/pp_top/README.md`.
- **Union counts** (`suite-union.tsv`, with matching suite logs):
  - Suites go from 1,021,627 at `ead80360` to 1,021,640 at head. The +13 is TW +4 and CS +9.
  - `ead80360` is exactly +142 over `07b1469d`.
  - My runs reproduce the aecp_notify 34 and the CS 9.

Reviewer probes and controls (disposable, never applied to the clone):

- **One controller, full timebase** (`scripts/probe_tick.py`, the fifth build at 1 ms = 1,000 clocks; `receipts/probe-tick/`).
  - Two GET_COUNTERS rounds to one controller, the first pulsed SHIFT clocks after a ms tick.
  - Main RTL: every shift is under a second, from 999,009 to 999,999 clocks.
  - Head: shift 0 gives 999,999 and shift 50 gives 999,949. Shifts 100 to 990 give 1,000,899 to 1,000,009.
  - Reading: the head improves on main and stays inside the recorded one-tick tolerance (at least 1,000 ticks; at most one tick short of a second in clocks). So this is not a finding.
- **Reviewer controls through the lane's own driver** (`scripts/reviewer_mutants.py`; `receipts/campaigns/reviewer-mutants*.log`, `results/out-reviewer*-results.json`):
  - `r476_stamp_slot0_*`, the stamp written to slot 0: KILLED by TW1/TW2 and by CS2a-c.
  - `r476_window_999_*`, the window compare at 999: SURVIVED TW, CS and ST at head, and SURVIVED ST at main RTL too. See S1.
  - `r476_stamp_any_kind_*`, the kind guard dropped: SURVIVED TW and ST. See S2.
- **Area cross-check, not the gating recipe** (`scripts/yosys_notify_area.sh`, `receipts/static/yosys/`).
  - `KL_aecp_notify` alone at the 1x1 generics, sv2v and Yosys `synth_xilinx`.
  - FDRE +3, matching the executor's Vivado module-alone +3 FF.
  - LUT +207, MUXF7 +135, MUXF8 +82. Vivado module-alone gave -34 LUT.
  - Yosys maps the extra stamp write port differently. The stop is defined on Vivado OOC 1x1 with #638's recipe, so this figure is context only.

## 4. Findings

### R476-1-F1 - MINOR - lenses: RTL, Docs

- **Where:** `hdl/aecp/KL_aecp_notify.sv:1299-1300`.
- **Authority:**
  - Issue #148: the title, and acceptance 1, "measured from the send of the first round to the send of the next".
  - The module's own banner at `:133-136` ("their one-second limit runs from a round's last send") and the new comment at `:1439-1442`.
  - `docs/guides/hdl-engineer.md:10-14`: the module's `//!` comments carry the design rationale and are the project's primary source. The inline comment at `:1299` now contradicts the banner it sits under.
  - The PR body §2: the selection stamp "closes the window between the round's selection and its first job".
- **Evidence:**
  - Directly above the selection stamp (`:1301-1302`), the comment still reads: "Measure the one-second limit from emission selection, not from the possibly much earlier pending instant."
  - At this head the limit no longer runs from selection. The `N_EMIT_WAIT` stamp overwrites it until the round's last send: TW1 at ms 3603 at head vs 3005 at main, and CS2a-c at 115,0xx clocks.
  - The comment therefore states, as the design rule, exactly the behaviour #148 removes.
  - The lane updated the bench's matching comment (`5f458aa`, "ST's comment drops the selection stamp") but not this one.
- **Impact:**
  - No logic effect.
  - A maintainer reading the claim branch is told that the limiter measures from selection. That contradicts the banner and the `:1439` comment eight lines apart, and invites deleting the `:1443` line as redundant.
  - The `counter_spacing_from_selection` control would catch that deletion, but the source should not argue for it.
  - The fix changes RTL source bytes, which the PR's byte-identity claims hash ("notify RTL is byte-identical to that measured head"), so it is not prose-only residue.
- **Required outcome:** reword `:1299-1300` so it describes the selection stamp as provisional. For example: the stamp written at the claim keeps the window shut until the round's first job reaches `N_EMIT_WAIT`, whose stamp then follows each job to its send, so the limit runs from the round's last send (issue #148). No logic change.
- **Verification:**
  - `git diff` against this head touches only comment lines of `KL_aecp_notify.sv`.
  - The sv2v output of the module is byte-identical before and after (sv2v drops comments).
  - `./scripts/lint_hdl.sh` is 41 of 41 OK.
  - `tb/aecp_notify` `make run` and `tb/pp_top --spacing-only` pass.

### R476-1-S1 - SUGGESTION - lens: Tests

- **Where:**
  - TW's lower bounds: `tb/aecp_notify/sim_main.cpp`, `round_waits_for_tx`, `c2.ms >= sent1 + 1000` and `c4.ms >= sent3 + 1000`.
  - CS and ST2b: `tb/pp_top/notify_phases.hpp`, `1000L * MS_CYC - MS_CYC`.
- **Evidence:**
  - A limiter one tick short (`>= 32'd999` at `:1101`) passes TW, CS and ST at head.
  - TW lands it at sent + 1002 against a bound of sent + 1000; the head lands at sent + 1003, so 3 cycles of the pick and walk latency are slack.
  - CS sees about 115,000 clocks against a bound of 99,900, because a 16-row round is about 15,000 clocks.
  - At main the same control passes ST2b too, at exactly 99,900, so this gap predates the PR.
  - So no check holds the limiter at the recorded decision's own 1,000 ticks.
- **Suggestion:**
  - Tighten TW's lower bound to the exact latency (sent + 1003), or grade the pend instant.
  - Or add a one-row CS variant, where the gap sits near 100,000 clocks.
  - Plant `window_999` as a control that must fail.

### R476-1-S2 - SUGGESTION - lens: Tests

- **Where:** `hdl/aecp/KL_aecp_notify.sv:1443`, the kind guard on the new stamp line.
- **Evidence:**
  - Dropping `if (em_kind_r == PP_UNS_CTRS_C)` survives TW and ST at head.
  - Without the guard, every later non-counter round re-stamps the last counter round's slot, and delays that descriptor's next counter notification by up to a second.
- **Suggestion:** add a TW-style check that a non-counter round sent after a counter round does not delay the next counter round, and plant the unguarded edit as its control.

### Not findings (examined and accepted)

- **Sub-second wire gap at one controller.** The head shows 999,949 clocks of 1,000,000 at the full timebase. This is within the recorded one-tick tolerance (decision R420-1 S4, 08 §3), and the head never makes rounds less than 1,000 ticks apart. I do not re-open that decision.
- **Area.**
  - The executor's Vivado OOC 1x1 receipts (`vivado/ooc1-{base,head}`) give base 23,448 LUT / 20,968 FF and head 23,434 / 20,969, so -14 LUT and +1 FF, inside the 40 / 60 stop.
  - The u_notify hierarchy row moves +41 LUT and +1 FF. Five rows whose RTL is unchanged move -55. The PR discloses both.
  - The head was measured at `5f458aa`. `KL_aecp_notify.sv` is identical between `5f458aa` and `bed5f47` (empty `git diff`). The lane's whole HDL delta over merged main is that one file.
- **Parent adoption patch `parent-adoption-148-6c22d3ca.patch`.**
  - Judged against `tb/verilator/milan_dp/sim_nxn.cpp` at dev `6c22d3ca`.
  - `drain_tx` now continues past `cyc` only while `cur` (a frame in progress, local to the call) is non-empty, with a hard bound of `cyc + 2048` cycles. A frame of at most 1,514 bytes at 8 bytes per beat needs at most 190 beats.
  - `cur` clears at `tlast`, so the loop ends at the first frame boundary after the window. It never starts a new frame and keeps no state across calls.
  - Every caller paces itself on `uns_log_cycle`, which the extra cycles advance, so no window's accounting drifts.
  - The only behaviour change: a frame that began inside a window is logged instead of being split and dropped across two calls. The executor's probe shows exactly that at head: A's second push, 48 bytes cut.
  - The patch is right and bounded. At base, the patch can change a result only if a frame straddles a window edge. The executor's receipt says every base leg line is identical with and without the patch; I did not re-run it (section 6).
- **#158** (a DEREGISTER drained mid-round corrupts the round). It is out of scope and not graded here.
  - This PR does not make it worse: my re-run of the published probe gives identical job traces at main RTL and at head.
  - By construction, the DEREGISTER single-shot rewrites `em_kind_r`, which stops the new stamp. `ctr_last_r` then holds the last real counter send.
- **AQ +3 ADP timer arms.** Reproduced: 8,270 at main RTL and 8,273 at head, both rc 0, every other AQ figure identical. This is consistent with the executor's explanation (U9's update now 18 ms later shifts later PRNG draws). Nothing was weakened.

## 5. Reviewer-owned ledger

| Lens | Status | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Milan v1.2 §5.4.5.1, §5.4.5.2 Table 5.22; IEEE 1722.1-2021 §7.5.2 (no rate limit); 08 F08.1 `T-CTR-NOTIF` and §3; the recorded one-tick decision; `KL_aecp_notify.sv` `:1099-1101`, `:1295-1302`, `:1438-1451`; engine `uns_done_o` / arbiter grant; scope (`gen_ident` departure path); TW, CS and probe-tick at main and head | R476-1 | bed5f47785839800bb640d7c747f5435f84ab5a3 |
| RTL | UNCLEAN (F1) | the +9 -1 diff; reset, claim, emit and withdrawal paths; DEREGISTER interplay; identify face sharing; no port, parameter or register change; area receipts; Yosys cross-check | R476-1 | bed5f47785839800bb640d7c747f5435f84ab5a3 |
| Robustness | CLEAN | withdrawal (`rgy_new_w`) mid-wait; DEREGISTER single-shot and #158 probe at main and head; reset (`em_ctr_ix_r` reset, `ctr_sent_r` valid bit); 32-bit ms wrap in the unchanged subtract; parent `drain_tx` bound and statelessness; AQ side effect | R476-1 | bed5f47785839800bb640d7c747f5435f84ab5a3 |
| Tests | CLEAN (S1, S2 suggestions) | TW and CS source; red at main and green at head, executed; 53 of 53 notify and 17 of 17 ctr KILLED, executed; 7 reviewer controls; suite and campaign union receipts; phase-sweep receipts (main: 144 of 200 starts below the bound, at 27-98 of every 100; head: minimum 115,036) | R476-1 | bed5f47785839800bb640d7c747f5435f84ab5a3 |
| Docs | UNCLEAN (F1) | 06 §7 (`:892-898`); 09 §8 rows CS and TW; `tb/aecp_notify/README.md`; `tb/pp_top/README.md` (CS, ST limits, mutation tables, seven sections); module banner `:133-136`; inline comments `:1299-1300` and `:1439-1442`; PR body line references (`:469`, `:1043`, `:1297`, `:1443`, `:136`, `:1299-1302`, `:1099-1101` all verified) | R476-1 | bed5f47785839800bb640d7c747f5435f84ab5a3 |

## 6. Real limits

- **Vivado was not run.** No Vivado is on this host. The OOC 1x1 delta is taken from the executor's public receipts, which are internally consistent. My only area run is a Yosys module-alone cross-check, which is not the gating recipe.
- **Banks not re-run** (they are the manager's):
  - full `./scripts/run_suites.sh` (about 42 min);
  - Yosys `syn/yosys/run.sh`;
  - the aecp, acmp, d3, aecp_dispatch, gsi, name-write, ADP and MAAP campaigns;
  - the six-build `pp_top` totals.
  - For these I relied on the public round-1b receipts: compare files, suite union, and logs with rc 0.
- **What I did run:** the gates the fix touches, namely TW, CS, AQ, the notify and ctr campaigns with their goldens (`--notify-only`, `--identify-only`, the identify build, `tb/originator`, `counters`), lint, `make check` and `gen_matrix --check`.
- **Parent consumer set not executed** (parent banks are not allowed here). Gate 15 and the adoption patch were judged from source at dev `6c22d3ca` and from the executor's receipts. "Changes nothing at base" was not re-run.
- **Hosted checks were read only.** At `2026-10-05T05:42Z`, `docs-gates` and `portability` had completed successfully and `suites` was still in progress. The manager owns hosted and act acceptance.
- **No hardware.** Physical calibration was NOT RUN. Field skips are not hardware proof.
- **Spec text** was read from local text extractions (hashes in `receipts/environment.txt`).

## 7. Pending manager duties

- Return R476-1-F1 to the executor. Its verification is the comment-only diff plus the checks listed in F1. S1 and S2 are optional.
- Build the final current-dev candidate at the merge turn (source base `07b1469d`, live dev `e6172750`), with the parent consumer set and all five adoption patches, including gate 15.
- Hosted and act acceptance at the final head, including the `suites` job that was in progress here.
- Keep #158 open and separate. This PR does not change it.

## 8. Clone restoration

- The review clone is at exact head `bed5f477`, tree `1bc22d81`.
- `git status --porcelain --ignored` is empty, with a clean index and worktree.
- The index and the HEAD tree (mode, blob, path) hash the same, `b2157860…`.
- The repository has no gitlinks (no submodules), so there is no submodule pin to check.
- One stray file appeared during the review: the Yosys probe's ABC history file, `abc.history`, written into the clone root. It was removed, and the clean state was re-verified (`receipts/environment.txt`).

R476-1 FINISHED
