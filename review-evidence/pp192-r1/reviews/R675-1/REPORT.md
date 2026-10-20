[R675] POSITIVE - exact head 807b673e59ebff33378b7a78d13f34b8eccd64aa

# R675-1: internal independent review of PR #197 (Refs #192)

- Repository: Mister-M-alt/protocol-processor-control-plane-avb-milan, PR #197, branch `192-started-notify`.
- Exact head `807b673e59ebff33378b7a78d13f34b8eccd64aa`, tree `9b90a6cf899ac333c7413f1219ee4bf378f7b52d`, verified in the isolated clone (receipt `receipts/clone-state.txt`).
- Source base is `24c7f853`. The five author commits run `aa5d28f`..`21855f6c`. The manager merge `807b673e` brings in processor main `21601694` (#188/#189).
- Review start: PR #197 comment 6297120477. Assignment: issue #192 comment 6284522415.
- Prior public review findings on this PR: none. At review time, PR #197 had no reviews and no review comments. Its only issue-thread comments were the two review-start notices. The issue thread has the assignment, TAKEN and REVIEW READY only. There is nothing to resolve or retain.

## Verdict

POSITIVE. At the exact head, every started/stopped change of a bound Stream Input raises exactly one GET_STREAM_INFO notification to every registered controller, and the START/STOP_STREAMING requester is not excluded. A change that meets another cause of the same input before that input's round is claimed coalesces into one notification carrying the final state.

- The generated F06.14 rows and the docs match the RTL.
- The bench cases kill both the author's planted controls and four independent reviewer mutants.
- The manager merge is patch-identical to the author delta, and the check tally adds up exactly over main `21601694`.
- The parent adoption patch changes only the G9 rows that pinned the defect.
- No top-level port, parameter or register-map change.

There are no open MINOR, MAJOR or BLOCKER findings. Two RESIDUE wording items and two SUGGESTIONs are below.

## How the review was reconstructed

1. Repository conventions. There is no AGENTS.md or CONTRIBUTING.md in this repository. I used `docs/README.md` (IDs, single-source rules, citation style, editing workflow, and `make check` as the commit gate).
2. Frozen scope. The issue #192 body defines the required behaviour (Milan v1.2 5.4.5.2 last paragraph, Table 5.22; 5.4.2.19, 5.4.2.20; 5.4.5.1) and its "Done when" list. The manager assignment 6284522415 adds: hook into the `stri_events` OR, #181 coalescing, the A+B suite case, the coincidence case, an event-not-driven mutant KILLED, docs and campaign records, and a STOP on any top-level port, parameter or register-map change.
3. Authorities in the tree. These are the listener's started/stopped face and write-back (`hdl/acmp/KL_pp_acmp_listener.sv`), `stri_events` in `hdl/top/protocol_processor_top.sv`, the round claim and exclusion logic in `hdl/aecp/KL_aecp_notify.sv`, F06.14 and 06 §7, and REQ-NOT-003. I had no Milan or IEEE text locally. Clause wording is taken from the issue's frozen text and the repository's own quotations (see Limits).
4. Diffs. I read `git diff 24c7f853..807b673e`, the author delta `24c7f853..21855f6c`, the merge delta `21601694..807b673e` and the #188/#189 HDL delta `24c7f853..21601694`.
5. Public evidence. I read milan-fpga `fca476ec` `review-evidence/pp192-r1` (author receipts, PR-BODY, the adoption patch) and the PR's executed-gate tables. I then ran my own focused runs at the exact head.

## Findings

| ID | Severity | Lenses | Location | Authority / evidence | Impact | Required outcome | Verification |
|---|---|---|---|---|---|---|---|
| R675-1-RES-1 | RESIDUE | Docs | PR #197 body, opening line and "## The change" table | The body says "Branch `192-started-notify` from main `24c7f853`, five commits; head `21855f6c`". The published head is `807b673e`, the manager merge of main `21601694` on top of `21855f6c`. The gate tables' "Head" column correctly means `21855f6c`. | Wording only. A reader may take `21855f6c` for the PR head. No measurement, verdict or claim changes, because the gates did run at `21855f6c`. | Replace with: "Branch `192-started-notify` from main `24c7f853`: five author commits to `21855f6c`, then a merge of processor main `21601694` (#188/#189); published head `807b673e`. The gates below ran at `21855f6c`." | Read the PR body. |
| R675-1-RES-2 | RESIDUE | Docs | parent adoption patch `parent-adoption-milan_dp-gsi-g9.patch`, `tb/verilator/milan_dp/README.md` G9 row | The new row ends "(processor #192)" and names no clause. The patch's own `sim_nxn.cpp` comments cite Milan 5.4.5.2, Table 5.22 and 5.4.5.1 (`receipts/parent-adoption-check.txt`). | Wording only, in a prose table. No check or count changes. | End the row with "(Milan Table 5.22, 5.4.5.1; processor #192)". | Re-read the patch hunk at README line 654. |
| R675-1-SUG-1 | SUGGESTION | Tests | adoption patch, `sim_nxn.cpp` `gsi_g9_stop_streaming_excludes_the_requester()` | After the patch, G9 also requires the requester to receive the GET_STREAM_INFO. | Only the name now under-describes the leg. | Optional: rename it when the parent adopts the pin, for example `gsi_g9_stop_streaming_and_its_started_change`. | Not required. |
| R675-1-SUG-2 | SUGGESTION | Tests | `tb/acmp_nvm` | With the defect as reported planted (`&& !src_strq_r`), `tb/acmp_nvm` still passes (rc 0), while the oracle sees 3 unpulsed changes (`receipts/probes-sensitivity/`). The pulse is graded end to end in `tb/pp_top` GI and G7f, which kill it. | None at this head. The unit bench simply does not grade `act_strt_chg_o`. | Optional, outside #192: a unit check of the pulse in `tb/acmp_listener` or `tb/acmp_nvm`. | Not required. |

## Lens results

### Conformance: CLEAN

**Trigger.** `hdl/top/protocol_processor_top.sv:3585-3589`: the per-input term is `(32'(lstn_act_sink_w) == k && lstn_act_strt_chg_w)`. The former `!lstn_act_strt_cmd_chg_w` exclusion and its listener port are gone. The pulse (`hdl/acmp/KL_pp_acmp_listener.sv` X_WB) fires on a real change of `f_started` under a binding held before and after. That covers START/STOP_STREAMING, the 5.5.3.5.6 re-bind short-circuit and a BIND_NEW onto a bound sink. A bind or unbind (undefined ↔ defined, 5.3.8.7) is excluded, and the pbsta compare already notifies those. START/STOP on an unbound input changes nothing (X_STRT_AP, 5.4.2.19), so nothing is notified.

**Requester not excluded.** In `hdl/aecp/KL_aecp_notify.sv`, the round claim for a Stream Input GET_STREAM_INFO takes the generic arm, `em_excl_v_r <= 1'b0`, so no row is skipped (5.4.5.1, "if any"). The command's own class-9 response still excludes the requester (5.4.5.2) through the command queue arm.

**Coalescing.** Every cause sets the same `pe_sin_r[s]` bit until the round is claimed. A re-fire during the walk re-queues one final round (#181).

**Bench evidence at the exact head.**
- `GI STOP-BY-A` and `START-BY-A`: one byte-exact notification at A and at B, each at its own sequence_id. The command's own response reaches B once and A never, and nothing else is sent (4 frames).
- `STOP-WITH-REGISTRATION`: one notification per controller carrying STREAMING_WAIT and failure code 7. The registration premise holds.
- `G7f`/`G7g`: the sole registered requester receives the sink-1 GET_STREAM_INFO and nothing else.

**Merge with #189.** The merge composes without double or lost notifications. #189's SETTLED_RSV_OK REGISTERING_FAILED bookkeeping runs with `cellmut_r` clear, so it raises neither `act_notify_o` nor `act_strt_chg_o`. The top's live `evt_tk_failed` read feeds the listener only and does not touch `stri_events`. `STOP-WITH-REGISTRATION` exercises a Failed registration on a settled sink at the merged head and counts exactly 6 frames.

**Scope.**
- Ports and parameters: the declaration lines of `protocol_processor_top` hash identical at `24c7f853` and `807b673e` (252 lines). The removed `act_strt_cmd_chg_o` is a submodule port wired inside the top, and the repository has no remaining reference to it.
- Register map: no file in the register-map scope (07, the CSR sources) changed.

### RTL: CLEAN

**Listener.** The edit is local: one port, its two reset/default assignments and its X_WB assignment are removed. The kept `act_strt_chg_o` stays a one-clock pulse, cleared by default every cycle. The comment on why `strt_was_r`/`bnd_was_r` cannot be stale at X_WB still holds, since the delta adds no new X_WB entry.

**Top.** The term is combinational into the existing per-input OR, so it adds no width or index hazard. The sink compare is the pre-existing clamped `lstn_act_sink_w`.

**Merge.** `git diff 21601694 807b673e` has the same stable patch-id as `git diff 24c7f853 21855f6c` (`88f39c1e…`), with identical content. The auto-merge altered no hunk.

**Exact-head gates.**
- `scripts/lint_hdl.sh` rc 0.
- `make check` rc 0 in a disposable git checkout: F06.14 is regenerated and consistent, with 31 commands and 41 rows.
- `scripts/gen_matrix.py --check` rc 0.
- `scripts/check_upc_map.py` rc 0.

**Independent oracle.** A simulation-only monitor added to the listener requires that every record write keeping a sink bound while flipping `f_started` is followed by exactly one `act_strt_chg_o` pulse, and that no pulse comes without one.
- It reported 0 mismatches over 34 such changes in three benches: pp_top default 16, acmp_listener 15, acmp_nvm 3.
- None of these changes came from outside a walk write-back (preload or sweep).
- It is sensitive: with the defect as reported planted, it reports exactly the 3 command-driven changes in acmp_nvm as mismatches.

### Robustness: CLEAN

- **Extra notifications.** A state-changing START/STOP now yields two notifications of different kinds. They never coalesce with each other: the class-9 entry sits in the command queue, the GET_STREAM_INFO in `pe_sin_r`.
- **Commands while a round is pending.** The engine still takes no command while a notification is pending (documented in 06 §7 and the bench comments). That only delays the next command by one fan-out round, and nothing is lost.
- **Repeats and failures.** A repeat START/STOP, or one refused (locked, unbound), commits no change and so notifies nothing, because the pulse is gated on `cellmut_r` and a real bit change.
- **Duplicate cause.** A re-fire of a cause about 600 clocks later is caught as a second notification (reviewer mutant `started-pulse-repeated` KILLED).
- **Wrong sink.** Hard-wiring the sink is caught by G7f (`started-term-sink-0` KILLED).
- **Memory.** No OOM kill occurred in this review's runs. The unit reached its cap only through reclaimable page cache.

### Tests: CLEAN

**Exact head `807b673e`, pinned Verilator 5.050** (identity verified: `Verilator 5.050 2026-07-01 rev v5.050`).

| Run | Result |
|---|---|
| `tb/pp_top` (all seven builds) | rc 0, 10,721 checks, 0 FAIL |
| `tb/acmp_listener` | rc 0, 3,170 checks |
| `tb/acmp_nvm` | rc 0, 388 checks |
| `tb/aecp_cmds` | rc 0, 176 checks |
| `tb/timer_map` | rc 0, 1,360 checks |
| `tb/ucpu` | rc 0, 447 checks |
| `tb/pp_top/gsi_mutants.py --jobs 2` | rc 0: 23 detected by named checks; golden and restored PASS |

In the GSI campaign:
- `command-started-change-dropped` (the defect as reported) fails `GI STOP-BY-A … at A, the requester, got 0`.
- `started-trigger-removed` (the event not driven) fails the same row, `got 0`.
- `coincidence-hold-removed` (premise control) fails `GI STOP-WITH-REGISTRATION … got 2`.

**Merge composition.** `tb/pp_top` at processor main `21601694` gives rc 0 and 10,649 checks. The head's +72 equals the author's own +72 at `21855f6c` (10,634 → 10,706), so the merge loses and duplicates no check.

**Reviewer mutants**, all KILLED by named checks (`receipts/probes/probes.json`):

| Mutant | What it plants | Killed by |
|---|---|---|
| `gsi-round-excludes-requester` | the Stream Input GET_STREAM_INFO round skips the last command's requester | `GI STOP-BY-A … at A, the requester` |
| `started-only-on-stop` | only started→stopped pulses | `GI START-BY-A … at A, the requester` |
| `started-pulse-repeated` | a delayed duplicate cause | `GI STOP-BY-A … exactly one` |
| `started-term-sink-0` | the term hard-wired to sink 0 | `G7f` |

**Records.** The README's GSI control table has 23 rows for 23 campaign variants. The README's dated 2026-10-02 measurement of 20 variants is a historical record.

### Docs: CLEAN (RESIDUE R675-1-RES-1, R675-1-RES-2 carried)

- F06.14 rows 0x0022/0x0023 are generated from `aecp_commands.json` and agree (`make check`).
- F06.13 BOUND/STREAMING_WAIT, 06 §7's Stream Input trigger paragraph and its START/STOP note, the 06 command-coverage row and REQ-NOT-003 in 00 all state the new behaviour with clauses: the requester is included, the command's own response is separate, and the coalescing holds.
- `tb/pp_top/README.md` describes the GI step and its three controls accurately.
- No stale "suppressed or excluded" statement remains in `docs/`, `hdl/` or `tb/`.
- **Comment rule.** The added source comments state behaviour and reason with issue and clause IDs. They carry no bench lane label, lane name, review round, reviewer ID or issue-comment ID. "Round" in the delta always means a notification round, and A/B name bench controllers. No new RESIDUE.

## Parent adoption patch

`parent-adoption-milan_dp-gsi-g9.patch` (sha256 `5ed1656c…`) applies cleanly to milan-fpga dev `e26f1816`. It touches only `tb/verilator/milan_dp/README.md` (1/1 lines) and `sim_nxn.cpp` (8/4 lines). The changes are:
- the G9 table row;
- the G9 summary comment and banner;
- G9's `gsi_ck_pushes(..., 1, 0)` → `(..., 1, 1)`, with its label.

These are exactly the rows that pinned the defect. The author's parent receipts show those two G9 rows failing at head without the patch (`got=0x1 exp=0x0` for A and B) and all 17 gates rc 0 with it (notify leg 423 → 424 checks). The code comments cite 5.4.5.2, Table 5.22 and 5.4.5.1. The README row's citation is RESIDUE R675-1-RES-2. I did not execute the parent gates.

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | issue #192 body and assignment; listener started face and X_WB; top `stri_events`; notify round claim and exclusion; #189 bookkeeping and live Failed read; port and parameter hash; GI and G7f/G7g rows at head | R675-1 | 807b673e59ebff33378b7a78d13f34b8eccd64aa |
| RTL | CLEAN | listener, top and `acmp_nvm_wrap` deltas; merge patch-id equality; lint_hdl, make check, gen_matrix, upc_map at head; started/stopped oracle and its sensitivity control | R675-1 | 807b673e59ebff33378b7a78d13f34b8eccd64aa |
| Robustness | CLEAN | coalescing and re-queue path, separate command-queue path, repeat and refused commands, duplicate-cause and wrong-sink mutants, memory events | R675-1 | 807b673e59ebff33378b7a78d13f34b8eccd64aa |
| Tests | CLEAN | `gsi_internal.hpp` GI step, `sim_main.cpp` G7f/G7g, `gsi_mutants.py` at head (23/23), pp_top at head (10,721) and at main 21601694 (10,649), 4 reviewer mutants, author receipts at 21855f6c/42c6a5e | R675-1 | 807b673e59ebff33378b7a78d13f34b8eccd64aa |
| Docs | CLEAN | 06 F06.14, F06.13, §7, command-coverage row; 00 REQ-NOT-003; `tb/pp_top/README.md`; `aecp_commands.json`; source-comment rule scan of the delta; PR body; adoption patch | R675-1 | 807b673e59ebff33378b7a78d13f34b8eccd64aa |

## Real limits

- No Milan v1.2 or IEEE 1722.1 text was available to this review. Clause meanings (5.4.5.1 "if any", 5.4.5.2 last paragraph, Table 5.22, 5.4.2.19/20, 5.3.8.7) are taken from the issue's frozen text and the repository's quotations, not re-read from the standards.
- At the exact head I ran only the focused suites above and the GSI campaign. I did not run `scripts/run_suites.sh` (the full bank), the d3, notify, acmp, aecp, aecp_dispatch, ctr, name, maap, adp, aecp_cmds or elab_guards campaigns, or Yosys. Their only execution evidence is the author's receipts at `21855f6c`, and at `42c6a5e` for notify (a docs-only difference). The merge delta is patch-identical, but the merged tree was not run under those campaigns.
- I did not run the parent consumer gates. The author's receipts are at gitlink `21855f6c` on dev `e26f1816` plus three scratch patches, not at `807b673e`. I checked the adoption patch for clean application and scope only.
- The oracle covers the record writes the three benches reach (34 bound changes). It is not a proof over all reachable sequences.
- Hosted checks on `807b673e` at the time of reading: docs-gates and portability success, suites in progress (`receipts/hosted-checks-807b673.txt`). That is not acceptance, and the manager owns hosted/act acceptance.
- Physical calibration NOT RUN. No hardware was used, and field skips are not hardware proof.

## Pending manager duties

- Validate the current-dev merge candidate (source base `24c7f853`, live dev `78ca9bdf104819265588726bce4322696c38b8c2`) with the builder and native banks, and link the receipts on the PR.
- Carry the parent G9 adoption patch with the pin adoption; this PR is "Refs #192". The parent consumer gates are the open "Done when" item of #192.
- Hosted/act acceptance at the merge turn.
- Carry R675-1-RES-1 and R675-1-RES-2 to the residue checklist.

## Receipts

Listed in `MANIFEST.sha256`. Host paths are masked (`<packet>`, `<scratch>`, `<clone>`, `<toolroot>`, `<home>`, `<data>`, `<tmp>`). The scripts in `scripts/` reproduce every run:
- `extract.sh` extracts the exact head;
- `focused.sh` runs the suites and gates;
- `gsi_campaign.sh` runs the bench's own campaign;
- `probes.py` runs the reviewer mutants and oracle;
- `mask.sh` masks host paths.

`make check` needs a git checkout and was run in a disposable local clone at the exact head. A first run of it in a non-git extraction failed on `git ls-files` and is superseded, not published.

R675-1 FINISHED
