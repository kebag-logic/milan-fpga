[R861] NEGATIVE - exact head 7cfb8a0499941e56682f0c2f63326d120f5b7d9e

Round R861-1, internal cleared-context review of PR #944 for issue #936 (the split AECP sends no unsolicited GET_STREAM_INFO notice when the split's Talker declares or withdraws). Head `7cfb8a0499941e56682f0c2f63326d120f5b7d9e`, tree `eb5a313b02b3669d9529500c0369c62dca697b50`, nine commits on dev-soft-core `70f4056f`. All five lenses were applied. Two findings are open, so the verdict is NEGATIVE. The first is this round's MINOR R861-F1 (RTL, Robustness, Tests). The second is the parallel external round's MAJOR R862-1-F1 (Conformance, Robustness, Tests, Docs), which this round retains at this head (see the addendum). Two wording-only items are recorded as RESIDUE.

The verdict and ledger were first written from this round's own pass. At that point Conformance and Docs were clean, and judgement 3 below read "not a merge-blocking gap". R862-1 was read only after that and is retained in the addendum, which leaves every lens UNCLEAN. The NEGATIVE verdict is the same either way.

## Verdict summary

- **The trigger rule is correct.** `declare_sources` records each source whose declaration changed against what it last published. That covers a declaration, a withdrawal, an Advertise/Failed swap (only once lwSRP makes it) and an adopted Domain's other VID. It records nothing for periodic declarations, for a Domain that keeps its VID, or for a reset that declares an unchanged source again. I found no missed trigger and no duplicate notice.
- **The record and its delivery are correct.** The SRP delivery takes the record into `ctrl_app.srp_noticed`, and an attach clears it. The bridge raises `aecp_changed(6, n, 1)` for each recorded source, so the notice goes to both registered controllers. The twin reproduces this.
- **Every plant is caught by its own test's words**, in both SRP campaigns and in the AECP campaign. The twin's new capture plant and its re-aimed plant are refused by their stated words.
- **One defect.** The bridge's poll runs before the SRP delivery poll that fills the record, and neither poll reports the record as owed. So the pass that takes it reports nothing to do. On a platform that defines `CTRL_MBX_WFI`, the loop would then sleep with the notice owed (R861-F1). The shipped split image defines no `CTRL_MBX_WFI` and never sleeps, so today's product is not affected. The documented loop contract is still broken, and no test can see it.
- **One acceptance gap, retained from R862-1 (MAJOR).** No CPU-budget row times the new notice from a real declaration change to its last recipient's commit, though the frozen acceptance asks for it.

## Findings

### R861-F1 MINOR (RTL, Robustness, Tests): a pass that takes SRP's record reports nothing to do, so the loop may sleep with a STREAM_OUTPUT notice owed

- **Where.**
  - `sw/firmware/ctrl/app/ctrl_app_srp.c:66`: the SRP delivery ORs each interface's `noticed` into `app->srp_noticed`, then returns only its sinks' `pending` (`:120`).
  - `sw/firmware/ctrl/app/ctrl_app_aecp.c:206`: the bridge consumes `srp_noticed`. Its `deliver` was added by `ctrl_app_compose_aecp`, which the platform calls first (`sw/firmware/ctrl/plat/ctrl_plat.c:238`). `ctrl_app_attach_srp` adds the SRP delivery poll later (`ctrl_plat.c:282`). The unit App fixture composes in the same order.
- **Authority.** `sw/firmware/ctrl/loop/ctrl_loop.h:24-30`: "a poll returns true while its module still owes output ... Only a pass that handled nothing and owes nothing sleeps in mbx_hal_wait()". FR_NFR 3.4.1 (`docs/reference/FR_NFR.md`): "Events start at their occurrence", and the last recipient's commit ends a notification fan-out, against min(T_svc, 24 ms) = 20 ms. The issue's acceptance asks for the notice "within AECP's notice bounds".
- **Evidence.** A disposable probe (`scripts/probe_record_across_sleep.patch`, `scripts/run_probe.sh`, receipt `receipts/probe_record_across_sleep.txt`) adds one App test at this head. It runs the loop to idle, sets SRP's record for source 0, and then calls `ctrl_loop_service` one pass at a time:
  - At both shapes (if1, if2), pass 0 returns 0 with `srp_noticed=1` and no notice sent. `ctrl_loop_step` would call `mbx_hal_wait()` at that point.
  - Pass 1 sends both notices.
  - The PR's own `App.SrpDeclarationChangeIsItsStreamOutputsNotice` passes in the same build. It runs 20 passes whatever each pass returns (`test_aecp.cpp:514`), so it cannot detect this.
- **Impact.**
  - With `CTRL_MBX_WFI` defined, the record waits for an unrelated wake: the next centisecond TICK while SRP keeps ticks on, or any input. That adds up to 10 ms to a path whose bound starts at the declaration, and no harness row times that path. This is a supported configuration (`mbx_plat_mmio.c:16-22`; the `wait-without-wfi` plant and the `-DCTRL_MBX_WFI=ctrl_test_wfi` arm).
  - The product split image defines no `CTRL_MBX_WFI` (`sw/firmware/ctrl/plat/ctrl_plat_console.h:25`), so today's image only loses one pass. No product image is shown to miss a bound.
- **Required outcome.**
  - No loop pass reports itself idle while SRP's STREAM_OUTPUT record, or the notice raised from it, is still owed. The design is the executor's choice, for example: the SRP delivery reports the record owed, or the record is raised in the pass that takes it.
  - A test that can fail for this defect: it steps passes until the loop reports idle (as `settle()` does) and requires the notice committed by then, with a plant that restores the current behaviour.
- **Verification.** Rerun the probe: no pass returns 0 before both notices are sent. The new test and plant are caught in the AECP campaign.

### R861-RES1 RESIDUE (Docs): the dest-MAC owed row still says no issue owns it

- **Where.** `tb/verilator/milan_dp/README.md:1382` reads "#665 (no issue owns it yet)". `tb/verilator/milan_dp/twin_compare.py:488` reads "#665 (a split datapath defect; no issue owns it yet)". The PR body says the same.
- **Why.** #943 ("Split: GET_STREAM_INFO answers stream_dest_mac 0 for a declaring STREAM_OUTPUT") now owns it. It was opened 2026-11-17T16:02Z, after the head was committed. The text is only a label: it changes no row value, grade or plant word.
- **Exact fix.** Replace both owner texts with `#943`, and the PR body's "no issue owns it yet" with "#943".

### R861-RES2 RESIDUE (Docs): a new source comment names a lane

- **Where.** `sw/litex/ctrl_memory.py:247`, a new comment line: "... as debt owed to S14) raises #894's 59.0 ...". The owner's comment rule (2026-10-15) says source comments never show lane names. The same delta adds "debt owed to S14" in the reason string at `:270`. That is a data string, not a comment, so it is noted only. Existing instances are #746's.
- **Exact fix.** Change "as debt owed to S14" in the comment to "as debt owed to the hybrid XIP work (#665 decision D3)".

## Lens coverage

Each line names what was examined at the head under review.

[R861] Conformance, applied; no finding on this round's own pass, UNCLEAN after the addendum — `sw/firmware/ctrl/srp/srp_mbx.c:262-357` (declare_sources), `:655-697` (srp_mbx_gate), `:900-960` (change_domain, create_participants), `ctrl_app_aecp.c:203-214`, `aecp.c:528-545`, `protocol-processor/hdl/top/protocol_processor_top.sv:3679-3684`, `notice_window.py:128`, twin captures. Checked against Milan v1.2 5.4.5.1, 5.4.5.2 and Table 5.22, IEEE 1722.1-2021 7.5.2 and 802.1Q-2018 35.2.2.8:
- **Declaration changes and VID.** Each declaration change is noticed. A VID move notices every kept declared source on its interface only, including a reset to the default Domain's VID 2. A swap is noticed only once made.
- **Failure fields.** A Talker Failed's code cannot change while declared: `allocated` is only ever set (`srp_mbx.c:680-686`), and every valid source is allocated before it declares. The failure bridge ID is the interface MAC.
- **What the notice carries.** `aecp_changed(6, n, 1)` is STREAM_OUTPUT n's GET_STREAM_INFO event (supported mask 9). It is raised once per recorded source and fans out to every registered controller.
- **Against the release processor.** It raises STREAM_OUTPUT notices at the talker gate's open/close and at a Listener-registration change. The second is out of #936's stated scope and listed for #943. The PR covers the first, plus swap and VID.
- **Twin.** At this head the split sends the fabric's four STREAM_OUTPUT 0 notices to the same two controllers, each 4 ms after the fabric's (5005 vs 5001 ms, 20005 vs 20001 ms; `receipts/twin_output0_notice_times.txt`).
- **Harness acceptance.** The STREAM_OUTPUT GET_STREAM_INFO notice is one of the notices the harness's `answering-*` arms hold (`notice_window.py:128`). Their rows were reported within bounds at both points in the author's receipts.

R861-F1 is not attributed here: no product image sleeps, and on the polling loop the hop costs one pass.

After the addendum, Conformance is UNCLEAN at this head under the retained R862-1-F1: the frozen acceptance asks the harness to show this notice's rows, and none does. The behavioural results above stand.

[R861] UNCLEAN RTL — `ctrl_app_srp.c:60-120`, `ctrl_app_aecp.c:178-229`, `ctrl_plat.c:238-282`, `ctrl_loop.c:249-347` and `ctrl_loop.h:20-30`, `srp_mbx.h:83-91`, `ctrl_app.h:99-101`. R861-F1 is open. Otherwise:
- the state widths are correct (32-bit masks over `CTRL_SRP_SOURCES` < 32, and the VID is 16-bit);
- the record is cleared exactly once per take;
- no reentry is possible: `aecp_changed` is called from the bridge poll, outside AECP's entry;
- the struct growth matches the ledger.

[R861] UNCLEAN Robustness — R861-F1 is configuration-dependent: it only bites with `CTRL_MBX_WFI` defined. Otherwise checked:
- a refused join or swap is noticed once it is made (`Talker.TypeSwapIsNoticed`, run);
- a refused Leave keeps the source declared, so it is not noticed until the Leave is taken;
- a failed creation returns before the record;
- a reset re-declaring an unchanged source records nothing (`Talker.ResetNoticesNothingUnchanged`);
- a recomposition clears the record (`SrpGate.F936A...`, its plant caught).

[R861] UNCLEAN Tests — R861-F1: no test steps the loop to idle on this path (`test_aecp.cpp:514`, 20 blind passes). Otherwise all of these were run here, and each passed or was caught by its own test's words:
- 12 `talker-notice-*` plants, 24 of 24 caught across both SRP campaigns (`receipts/fw_shard3.log`: 445 caught, PASS);
- 4 `app-output-notice-*` plants (`receipts/fw_shard2.log`: 303 caught, PASS);
- shard 0, the firmware suites and RV32 builds (`receipts/fw_shard0.log`: PASS);
- the twin: 1 finding, the known stale `split-talker-failed` row (`receipts/twin.log`, `twin_report.json`);
- the twin plants `output-notice-dropped` and `vanished-owed`, refused by their stated words in both comparisons (`receipts/twin_notice_plants.txt`; its "self rc" lines are a pipeline's rc, not the gate's).

`make twin-plants` stops at the known stale `srp-plus-k` plant (`receipts/twin_plants.log`), so the four AECP plants were run one at a time.

[R861] Docs, applied; no finding beyond RESIDUE on this round's own pass, UNCLEAN after the addendum — `sw/firmware/ctrl/srp/README.md:244-271`, `sw/firmware/ctrl/aecp/README.md:98-101`, `tb/verilator/milan_dp/README.md:1380-1442`, `docs/design/SPLIT_CONTROL_MEMORY.md:134-148, 269-276, 544-575`, `docs/design/MARK_II_AREA_PLAN.md:1088`, `tb/verilator/ctrl_service_budget/README.md:49`, `sw/litex/ctrl_memory.py:243-284`, `ctrl_memory_ledger.py`. Checked against the code and the owner's block-RAM-loose decision (#665 issuecomment-6892332745):
- the SRP README states the trigger rule as coded;
- the ledger figures add up (`receipts/ledger_consistency.txt`). 59.0 holds 126,976 B, and the two harness arms need 156 B and 16 B more, so 59.5. The fixture has 152 B spare. The ledger test's HELD table equals `ctrl_memory.LEDGERED`;
- the twin README matches the row and the plants;
- no obsolete text was restored.

Only RESIDUE (RES1, RES2) from this round's own pass.

After the addendum, Docs is UNCLEAN at this head under the retained R862-1-F1: the PR and the REVIEW READY mark the CPU-budget acceptance "Met" without a row for this notice.

## Completion ledger (reviewer-owned)

This is the final ledger, after the addendum. No lens has a clean covering round at this head.

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (R862-1-F1 retained and open; clean on this round's own pass before the addendum) | `srp_mbx.c` declare_sources, srp_mbx_gate, change_domain and create_participants; `ctrl_app_srp.c`; `ctrl_app_aecp.c`; `aecp.c` aecp_changed; `protocol_processor_top.sv:3679-3684`; twin captures; `notice_window.py:128`; FR_NFR 3.4.1 | R861-1 applied; no clean covering round | 7cfb8a0499941e56682f0c2f63326d120f5b7d9e |
| RTL | UNCLEAN (R861-F1 open) | `ctrl_app_srp.c`, `ctrl_app_aecp.c`, `ctrl_plat.c`, `ctrl_loop.c/.h`, `srp_mbx.h`, `ctrl_app.h`; probe receipt | R861-1 applied; no clean covering round | 7cfb8a0499941e56682f0c2f63326d120f5b7d9e |
| Robustness | UNCLEAN (R861-F1 and R862-1-F1 open) | refused join, swap and Leave paths, reset, recomposition, the WFI configuration | R861-1 applied; no clean covering round | 7cfb8a0499941e56682f0c2f63326d120f5b7d9e |
| Tests | UNCLEAN (R861-F1 and R862-1-F1 open) | `srp_talker.cpp`, `srp_gate.hpp`, `test_aecp.cpp`, `srp_talker_mutants.py`, `aecp_mutants.py`, `twin_compare.py`, `twin_plants.py`, `Makefile`; shards 0, 2 and 3; twin; four twin plants | R861-1 applied; no clean covering round | 7cfb8a0499941e56682f0c2f63326d120f5b7d9e |
| Docs | UNCLEAN (R862-1-F1 retained and open; RESIDUE RES1 and RES2; clean on this round's own pass before the addendum) | SRP and AECP READMEs, the twin README, SPLIT_CONTROL_MEMORY, MARK_II_AREA_PLAN, the budget README, the ctrl_memory ledger, the PR's acceptance claims | R861-1 applied; no clean covering round | 7cfb8a0499941e56682f0c2f63326d120f5b7d9e |

## Judgements asked of this round

1. **The 1x1/1if held-egress growth (+0.13 to 0.15 ms on the seven `backlog-owed` rows): not a defect of this PR.**
   - Those rows are the base's ruled misses behind the scenario's 60 ms egress hold. The egress ledger grades them, not the 20 ms bound (#936 issuecomment-6938589620), and the ledger refuses 1x1/1if.
   - The growth is consistent with the extra work this PR is obliged to do: STREAM_OUTPUT notices queued behind the hold. At 8x8/1if the ledger PASSes them.
   - I did not run the harness, so these figures are the author's receipts.
   - Whether 1x1/1if needs its own figure is for the egress-ledger owner (#894 item 3). It is recorded below as a manager duty, not a finding.
2. **The 8x8/1if `valid-destinations` STATED rounds (21 retry rounds at 11,922 to 12,537 cycles against the stated 11,900): not a defect of this PR.**
   - 8x8/1if states 1x1/1if's costs and reports each cost past them by design (`tb/verilator/ctrl_service_budget/README.md:49`). The base already reports such lines there.
   - The rounds are AECP's existing scan, retrying a STREAM_OUTPUT GET_STREAM_INFO attempt that this arm's fixture never answers. They stay within 11,900 at 1x1/1if (at most 9,015), and every row in the arm is within its 220 ms bound.
   - A figure for this round at 8x8 belongs to #894, the 8x8 owner.
3. **The notice row the harness does not time: yes, a gap that must be closed before merge.** This judgement was revised after reading R862-1.
   - My pre-read judgement was "not, on its own, merge-blocking". The reasoning was that the notice, from its raise to its last commit, is one the `answering-*` arms already hold (`notice_window.py:128`), and the hop from SRP's record to the raise costs one pass on a polling loop.
   - I now hold that this reasoning does not meet the frozen acceptance. The issue asks that "the CPU service-budget harness shows the notice rows within their bounds", the bullet after "within AECP's notice bounds" for this notice. FR_NFR 3.4.1 starts the bound at the event's occurrence.
   - The untimed hop is exactly where this round's own R861-F1 lives, so leaving it unmeasured is not harmless.
   - R862-1 also shows the existing `answering-every-port` STREAM_OUTPUT notices are injected through `aecp_changed`, with their timing starting at the observation's answer. They bypass the new record and both delivery polls.

## Prior public review findings

There were no prior public review findings on this PR before this round. The parallel external round R862-1 (published as PR comment 6953846656 at the same exact head) was read only after this report's verdict and ledger had been written. It is resolved in the addendum below.

### Addendum: R862-1 findings at this head

- **R862-1-F1 MAJOR (Conformance, Robustness, Tests, Docs): RETAINED, open at this head.**
  - Reason: issue #936's frozen acceptance asks the CPU service-budget harness to show this notice's rows within their bounds.
  - No row times a real Talker declaration or withdrawal through SRP's record and the bridge to the last registered controller's commit. The PR marks the criterion "Met" anyway.
  - This round's R861-F1 shows that the untimed handoff carries a configuration-dependent wait the existing rows cannot see.
  - Required outcome and verification as R862-1 states them.
  - This round's lens attribution follows the finding's own reviewer.
- **R862-1-R1 RESIDUE (Docs): RETAINED.** It is the same item as R861-RES2 (`sw/litex/ctrl_memory.py:247`). Either exact fix satisfies both.
- **R862-1-R2 RESIDUE (Docs): RETAINED.** It is the same item as R861-RES1. R861-RES1 also names the printed owner label at `twin_compare.py:488`, which is not a predicate.
- **Where the two rounds differ.** R862-1 banks RTL clean, and this round does not. R861-F1 is a demonstrated contract breach (`receipts/probe_record_across_sleep.txt`), so RTL stays UNCLEAN here.

## Real limits

- **Not run by me.** The CPU service-budget harness. Every harness figure above is the author's published receipt, as is the release-image byte identity with the base.
- **Not run here (needs migen).** `sw/litex/test_ctrl_memory.py`. Only the ledger tables' consistency and arithmetic were checked.
- **Also not run.** `fw_coverage.py`, the docs jobs, `plat_ledger.py`, `firmware-control-mutants`, the shard-1 suites, and the verilator-suites shards.
- **No hosted check runs exist at this exact head** (the check-runs API returned 0). Hosted and act acceptance are the manager's.
- **Not hardware proof.** Physical calibration was not run, and field skips prove nothing about hardware. No manager source bank ran at this head, and none is inferred.
- **The probe composes a planted record.** It sets `ifs[0].noticed` directly in the unit App composition rather than driving a real declaration through a gate. The code path from the take onward is the shipped one.
- **Link down.** I did not establish what the split's STREAM_OUTPUT answer shows during a link-down, which this PR deliberately does not notice. The answer's fields are #943's.

## Pending manager duties

- Carry RES1 and RES2 to the residue checklist.
- Route the 1x1/1if held-egress figures and the 8x8/1if retry-round figure to their owners (#894).
- Build and validate the current-dev merge candidate at the merge turn (live dev `e275d795`), and publish its receipts.
- Resolve the stated text conflicts with PRs #935 and #932 at the flip train's composition.
- Re-review after R861-F1 and R862-1-F1 are fixed, with every lens re-covered at the fixing head.
- If the executor disputes the acceptance reading behind R862-1-F1, record an owner decision on that reading.

## Publishable receipts

All are listed in `MANIFEST.sha256`. Home-directory paths in the logs are rewritten as `$HOME`. Disposable trees under `scratch/` are not published.

R861-1 FINISHED
