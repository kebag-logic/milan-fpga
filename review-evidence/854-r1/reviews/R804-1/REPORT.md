[R804] NEGATIVE - exact head e87f2179f8d84b3eb89dea0148bb63d64319bc38

# External independent review R804-1: issue #854 / PR #862

- Head: `e87f2179f8d84b3eb89dea0148bb63d64319bc38`, tree `39de20bda38e32990e0d7482773da768ef9cf54c`, a single commit on source base `ac0a01e354d20f5ecac1569c4e7afb3abcbf6f36`, which is also the live `dev` tip.
- Role: external reviewer, cleared context, working in its own detached clone.
- How the task was reconstructed:
  - AGENTS.md, CONTRIBUTING.md and docs/README.
  - The #854 body and every #854 comment: the lane-open, TAKEN and REVIEW READY comments.
  - The PR #862 body. Its two comments are review-start notices only.
  - Authorities: `third_party/verilog-axis/rtl/axis_fifo.v` at `48ff7a7e`, `docs/design/AREA_BUDGET.md`, `docs/testing/PP_SHADOW_BASELINE_RECIPE.md` and `docs/reference/REGISTER_MAP.md`.
  - The diff `ac0a01e3..e87f2179`.
  - Public evidence `review-evidence/854-r1` at `d4c77810`. Only the area receipts under `author/receipts/area/` were fetched. The author handoff file was not read.
- Prior public review findings: none. When this round finished, PR #862 had no review, no review comment, and no comment except the two review-start notices. Nothing is carried in to resolve or retain.

## Verdict basis

The RTL change is correct and its test is strong.

- `drop_evt_w` counts the FIFO's own one-cycle `status_overflow`, gated by a register that the same last beat writes. So it counts each kept control frame the FIFO drops exactly once, and never a kept frame that commits, a refused frame, or a runt.
- The counter saturates at 255 and holds.
- At the head, `[DR]` passes in every leg that runs it. The six planted arms are all caught. Six of seven further reviewer arms are caught too; the seventh is equivalent in this build.
- An independent runt probe in an `RXFILT_P=0` build confirms the runt exclusion.

The verdict is NEGATIVE for one reason: the authoritative area policy is not met (F1). By the PR's own statement this merge moves the shipping image. Yet only one of the route endpoint's three directives was routed, the two standalone endpoints (whose top is the changed `KL_pp_shadow`) were never measured, the baseline is not re-recorded, and no decision exempting the merge is on record.

## Findings

### F1: MAJOR, lenses Conformance and Docs. A merge that moves the shipping image without re-recording or a recorded exemption

- **Where:** `docs/design/AREA_BUDGET.md:591-594`; `syn/ooc/pp_resource_baseline.json:5`, `:451`, `:470-482` and `:928-940`, unchanged at the head; PR #862's "Area" section and its "Known limitations" item 3.
- **Authority:** `AREA_BUDGET.md:591-594`:
  > Outside the Mark II exception below, a merge moving the shipping image records its own re-baseline … Its PR measures the three endpoints again on its merge result and writes them with `record --write` … So growth under a tolerance cannot pile up unrecorded across merges.
- **Evidence:**
  - The PR body says the change moves the shipping route, because on `dev` the counter was constant and could be removed.
  - #854 is a defect fix, not a Mark II lane, so the D7 exception does not apply.
  - Only the ExtraPostPlacementOpt route was run, judged alone with `--shipping-selection`. Judging that route alone is legitimate in itself: the shipping 1x1 recipe's directive is ExtraPostPlacementOpt (`sw/litex/build.sh:378-381`, `AREA_BUDGET.md:550`).
  - The `ooc-1x1` and `ooc-8x8` endpoints both synthesize `-top KL_pp_shadow`, the module this diff changes. Neither was measured.
  - `record --write` was not run.
  - The PR leaves the re-record "to a separate decision", but neither #854 nor #862 records one. The 2026-11-06 maintainer decision that #845 relied on shows deferral does need a recorded decision.
- **Is the reported delta attributable to this diff?** Only in part.
  - The route delta (+106 LUT, +13 FF, -9 slices, WNS -0.044 ns, WHS -0.004 ns) compares an ExtraPostPlacementOpt route with record 15's selected AltSpreadLogic_high route. The PR body says so itself.
  - Timing at the same directive moved the other way. Record 15's own note (`pp_resource_baseline.json:451`) gives its ExtraPostPlacementOpt route as WNS +0.112 ns; the head's route at that directive is +0.166 ns. So the -0.044 ns is the directive change, not this RTL.
  - The share that can be attributed comes from the gate's sub-block table (`receipts/fetched_author_area/check-route-1x1.log`): wrapper +35 LUT / +10 FF and `ctl_fifo` +1 LUT / +1 FF.
  - That share fits the RTL: an 8-bit saturating counter that is no longer constant, `last_kept_r`, and the FIFO's `overflow_reg`.
  - Processor blocks this diff does not touch also moved (for example `u_pp` +27 LUT and `u_pp/u_listener` +19 LUT). That is placement and optimization movement, and `AREA_BUDGET.md` counts such movement against the change anyway.
- **Should the baseline be re-recorded?** Yes, under the policy as written, unless a maintainer or manager records an exemption.
- **Impact:**
  - The next PR that moves the image will be gated against record 15. It will inherit this PR's growth, and its standalone endpoints will absorb a `KL_pp_shadow` change no one measured.
  - The baseline record's `measured` notes would describe a tree that is no longer `dev`.
  - This is a process and record defect, not a wording one: it changes a generated artifact and gate evidence.
- **Required outcome:** one of the following.
  - (a) Measure the three endpoints on the merge result (the route set of all three directives, plus `ooc-1x1` and `ooc-8x8`), write them with `pp_resource_gate.py record … --write`, and add the matching area-page and findings entries, as earlier re-baselines did.
  - (b) Get a public maintainer or manager decision exempting this merge from re-recording, and cite it in the PR.
- **Verification:** for (a), `pp_resource_gate.py check-baseline` passes at the merge tree, and the JSON diff's `measured` notes name #854. For (b), the decision is linked from #862, and the area section cites it.

### S1: SUGGESTION, lenses Tests and Robustness. The runt exclusion is untested in the configuration where it matters

- **Where:** `hdl/milan/KL_pp_shadow.sv:862-871`; `tb/verilator/pp_shadow/README.md:182`; `sw/builder/endstation_builder.py:412` (`--no-rx-mac-filter` maps to `RXFILT_P`).
- **Evidence:**
  - With the default `RXFILT_P=1`, the filter drops every one-beat frame whatever `promisc_i` says (`hdl/ieee8021q/filtering/rx_mac_filter.sv:236-244`). So in the suite's build no runt can reach the tap. That confirms the narrowed scope: runts are not graded.
  - The reviewer arm `counts-runts` adds `FW_HEAD0` to `last_kept_r`. It survives the committed `[DR]`, and in this build it is an equivalent mutant (`receipts/reviewer_mutants_core.log`).
  - In a reviewer build with `-GRXFILT_P=0`, the probe offered 100 runts, each behind a 16-byte kept frame, after a 100-frame fill. The head RTL passed: 157 FIFO overflows, 108 kept frames lost, count 108. The same arm was KILLED there with count 157 against 108 expected (`receipts/runt_probe_rxfilt0.log`, `receipts/runt_probe_sim_main.diff`).
- **Judgement:**
  - The narrowed scope still meets every Required item of #854: the count comes from the FIFO's own overflow indication and saturates at 255; a self-checking overflow test requires frames lost to equal the count; and a mutant that removes the count is caught.
  - Runts are not a Required item, and the narrowing was published with its reason.
  - The RTL behaves correctly for runts at this head.
  - So this is optional, and it does not affect any lens's coverage.
- **Optional outcome:** a `[DR]` runt leg built with `-GRXFILT_P=0`. The probe shows this is cheap: one `-G` on the existing base build.

### R1: RESIDUE, PR body only. The "317 checks" figure belongs to a leg that does not run `[DR]`

- **Where:** the "Status" and "How to validate" gate table rows in PR #862's body; the same text is in the REVIEW READY comment on #854.
- **The text:** "`pp_shadow`: 317 checks, 0 failures, with the `[DR]` figures above".
- **Why it is wrong:** 317 is the `pending` leg's tally (`--pending-only`), and that leg does not run `[DR]`. `[DR]` runs in base (730 checks), vid73 (730) and crf (770), as `receipts/pp_shadow_full.log` shows (lines 535, 1366 and 2208).
- **Classification:** wording only. No measurement or verdict changes.
- **Exact fix:** "`pp_shadow`: base 730, vid73 730, crf 770 and pending 317 checks, 0 failures; `[DR]` runs in base, vid73 and crf with the figures above".

### R2: RESIDUE, README prose. The drain rate is overstated

- **Where:** `tb/verilator/pp_shadow/README.md:174`, "a 4,096-byte FIFO that drains one byte a cycle". The PR body's limitation item 1 and the REVIEW READY comment say the same.
- **Why it is wrong:**
  - The serializer loads a word in one idle cycle and then emits its bytes, so it drains eight bytes every nine cycles (`hdl/milan/KL_pp_shadow.sv:943`, `:960-971`).
  - The harness comment gets this right (`tb/verilator/pp_shadow/sim_main.cpp:2040`, "drains one word every nine cycles").
  - The claim that the burst outruns the drain still holds.
- **Exact fix:** "into a 4,096-byte FIFO that the serializer drains eight bytes every nine cycles, one byte a cycle while it holds a word". Make the same substitution in the PR text.

## Answers to the review focus

1. **Exactly once per kept frame lost, never for a kept frame.**
   - In `axis_fifo.v:261-284`, `overflow_reg` defaults to 0 every cycle. It rises once, on the clock edge of a dropped frame's last beat, whether the frame was dropped for `full && DROP_WHEN_FULL`, for `full_wr`, or because a drop was already in progress. A frame that commits raises `good_frame_reg` or `bad_frame_reg`, never `overflow_reg`.
   - `last_kept_r` (`KL_pp_shadow.sv:867-873`) is written on that same last beat. It is set for `FW_BODY`, or for `FW_HEAD1 && accept_w`. It is cleared for a runt (`FW_HEAD0`) and for a refused frame (`FW_HEAD1`, where `!accept_w` forces last and bad).
   - So in the strobe cycle, `drop_evt_w = ff_overflow_w & last_kept_r` (`:874`) reads the classification of exactly the frame that overflowed. A frame ending in that same cycle updates `last_kept_r` only at the next edge.
   - Executable evidence:
     - burst: 31 lost, count 31;
     - refused burst: 158 overflows, 69 kept frames lost, count +69;
     - `counts-refused-at-head1` and `counts-refused` both KILLED;
     - `current-state-not-registered` KILLED, with count 0: an unregistered state read misses every loss;
     - `counts-kept-frames-not-losses` KILLED.
2. **Saturation at 255.** `KL_pp_shadow.sv:1638`. `[DR]` loses 392 frames and the count reads 255 before and after 8,000 idle cycles. `wraps`, `saturates-at-254` and `counts-two` were all KILLED.
3. **The burst really overflows, and the expected count is derived.**
   - The processor's RX has no ready: `rx_valid_i = ser_busy_r` (`KL_pp_shadow.sv:949`, `:1322`), and `ff_ready_w = ~ser_busy_r` (`:943`).
   - The harness offers 100 × 64 B + 8 × 16 B at one beat a cycle (`sim_main.cpp:2046-2070`).
   - It derives the losses from the serializer's own byte stream, through read-only probes (`tap_sample`, `sim_main.cpp:1966`; `drops_probes.vlt`). Every handed frame must match an offered frame, whole and in order. Lost = offered − handed. The counter is never an input to the expectation.
   - The check `handed >= 64` (4,096 / 64) does pin the depth: `axis_fifo`'s depth is a power of two (`axis_fifo.v:137`), and at the next smaller size, 2,048 B, about 43 frames would pass.
4. **The six arms.** `make drops-mutant`: rc 0, with all six KILLED by their named checks and the clean control passing (`receipts/drops_mutant.log`). Each arm's plant was read in `drops_mutant.py:37-62` and matches the README table.
5. **Runts.** Confirmed from the RTL (`rx_mac_filter.sv:236-244`; `milan_datapath.sv:3294-3336`, where `rx_axis_fabric` feeds the tap through the filter when `RXFILT_P != 0`). The narrowed scope meets every Required item; see S1.
6. **Area.** See F1.
7. **Docs and register map.** These match the RTL:
   - the banner (`KL_pp_shadow.sv:72-75`) and the port comment (`:752`);
   - the register map: the `PP_DIAG[15:8]` row (`REGISTER_MAP.md:2456`, "control frames lost to a full ingress FIFO") and the prose at `:2469-2472`: count taken from the FIFO's own overflow indication, one per control frame lost, saturating at 255;
   - the CSR read `{tx_frames, rx_drops, rx_frames[7:0]}` (`milan_csr.sv:2278`, wired at `milan_datapath.sv:3083` and `:9791`);
   - TESTING.md's `[DR]` sentence (`:748`) and the README section (apart from R2).
   - Owner comment rule: the scan of the added lines found no bench lane label, lane name, review round, reviewer ID or comment ID in any source comment. No RESIDUE.

## Reviewer-run gates at the exact head

| Gate | rc | Result | Receipt |
|---|---:|---|---|
| `make -C tb/verilator/pp_shadow run` (all four legs; pinned Verilator 5.050, identity checked) | 0 | base 730, vid73 730, crf 770, pending 317 checks, 0 failures; `[DR]`: 108 offered, 77 handed out, 31 lost, count 31; refused burst 69 kept lost, count +69, 158 overflows; flood 392 lost | `receipts/pp_shadow_full.log` (home paths redacted) and `.rc` |
| `make drops-mutant` (`drops_mutant.py`, on a byte-identical copy of the head) | 0 | `PASS: [DR] catches every arm (6 of 6); clean control passes` | `receipts/drops_mutant.log` and `.rc` |
| Reviewer arms (`scripts/reviewer_mutants.py … core`) | n/a | control PASS; KILLED: `head1-only`, `counts-refused-at-head1`, `saturates-at-254`, `counts-two`, `current-state-not-registered`, `counts-kept-frames-not-losses`; SURVIVED (equivalent in this build): `counts-runts` | `receipts/reviewer_mutants_core.log`, `receipts/probe_logs/core_*` |
| Runt probe, `-GRXFILT_P=0` (`scripts/runt_probe_patch.py` and `reviewer_mutants.py … runt`) | n/a | head RTL PASS (100 runts, 157 overflows, 108 kept lost, count 108); `counts-runts` KILLED (count 157) | `receipts/runt_probe_rxfilt0.log`, `receipts/runt_probe_sim_main.diff`, `receipts/probe_logs/runt_*` |
| `scripts/lint_rtl.py --check` (pinned Verilator) | 0 | `LINT GATE: PASS (89 violation(s) <= ratchet 89 …)`; the only `KL_pp_shadow` entry, `:259` SYNCASYNCNET, predates this diff | `receipts/lint_rtl.log` |
| `scripts/pp_srcs.py --check` | 0 | pass | `receipts/pp_srcs.log` |
| `scripts/measure_test_evidence.py --check` | 0 | pass | `receipts/measure_test_evidence.log` |
| `scripts/docs_inventory.py --check` | 0 | `documentation inventory: OK` | `receipts/docs_inventory.log` |
| `git diff --check ac0a01e3 e87f2179` | 0 | no output | `receipts/diff_check.log` |
| `syn/yosys/run.sh --mode elaborate --no-structural --top KL_pp_shadow` (head copy) | 0 | 1 of 1 tops pass | `receipts/yosys_elab_KL_pp_shadow.log` |
| Restoring the clone | n/a | HEAD and tree are the head's; the index tree equals the HEAD tree; 0 tracked blobs differ in the worktree; the six gitlinks are as pinned; submodule worktrees are clean; nothing untracked or ignored is left | `receipts/restore_verify.txt` |

## Lens coverage and ledger

| Lens | CLEAN/UNCLEAN | Artifacts examined | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1) | #854 Required items, each checked against `KL_pp_shadow.sv:857-874`, `:915`, `:1631-1638` and `axis_fifo.v:217`, `:261-284`; `AREA_BUDGET.md:550`, `:591-594`; `pp_resource_baseline.json:451`; `receipts/fetched_author_area/check-route-1x1.log` | R804-1 | e87f2179f8d84b3eb89dea0148bb63d64319bc38 |
| RTL | CLEAN | `KL_pp_shadow.sv:792-874` (FSM, accept, `last_kept_r`, `drop_evt_w`), `:880-922` (FIFO parameters, overflow port), `:943-972` (serializer, no ready), `:1631-1645` (saturating counter); `axis_fifo.v:137`, `:200-217`, `:261-305`, plus its reset block; `milan_datapath.sv:3083`, `:3294-3336`, `:9791`; `milan_csr.sv:2278`; lint and the one-top elaboration; the area sub-block table (resource effect understood: +36 LUT / +11 FF attributable) | R804-1 | e87f2179f8d84b3eb89dea0148bb63d64319bc38 |
| Robustness | CLEAN (S1 is a suggestion) | refused frames at a full FIFO (`sim_main.cpp:2072-2101`); runts: unreachable at `RXFILT_P=1` (`rx_mac_filter.sv:236-244`) and correct at `RXFILT_P=0` (runt probe); saturation and hold (`sim_main.cpp:2103-2111`); reset: `last_kept_r` and the FIFO share the reset, and the FIFO clears `overflow_reg` and `drop_frame_reg` there; one-cycle strobe alignment with a following frame (item 1); oversize kept frames (`full_wr`) are also counted as lost, which matches the "frames lost" contract | R804-1 | e87f2179f8d84b3eb89dea0148bb63d64319bc38 |
| Tests | CLEAN (S1 is a suggestion) | `sim_main.cpp:89-99`, `:163`, `:200`, `:1956-2112`, `:4732`; `drops_probes.vlt`; `drops_mutant.py:1-138`; Makefile `:96`, `:118`, `:204-208`; the full suite run, drops-mutant, 7 reviewer arms, the runt probe | R804-1 | e87f2179f8d84b3eb89dea0148bb63d64319bc38 |
| Docs | UNCLEAN (F1; R1 and R2 are residue and do not count against the lens) | `REGISTER_MAP.md:2456`, `:2461-2472`; `TESTING.md:748`; `tb/verilator/pp_shadow/README.md:14`, `:165-199`; `KL_pp_shadow.sv:72-75`, `:752`, `:857-865`; the PR #862 body; #854 TAKEN and REVIEW READY; the owner comment-rule scan of the added lines; `AREA_BUDGET.md:591-594` (the baseline and area pages are not current) | R804-1 | e87f2179f8d84b3eb89dea0148bb63d64319bc38 |

## Real limits

- No Vivado route or standalone synthesis was run in this round. The area figures and the sub-block table are the author's published receipts (`receipts/fetched_author_area/`, fetched from `review-evidence/854-r1/author/receipts/area/` at `d4c77810`). F1 rests on those receipts and on policy text, not on a reviewer measurement.
- Not re-run here, because the brief does not allow full banks: the 65-suite sweep, firmware, builder, behave, and the `docs.yml` steps. Their source-head evidence is only the author's published gate receipts. Of those inputs, the diff touches only `KL_pp_shadow.sv` and pp_shadow test files. A behave feature mentions `KL_pp_shadow` only for its GET_COUNTERS gather face, which this diff leaves alone.
- The Yosys elaboration used the host's Yosys 0.66, not the CI-pinned Yosys. Treat it as a smoke check only.
- This review does not include, and must not be read as, a manager source bank.
- The `RXFILT_P=0` runt build is a reviewer-only probe, not a committed test.
- Physical calibration was NOT RUN. Simulation and field skips are not hardware proof.
- Hosted CI at the head, from a snapshot taken while this round ran (`receipts/hosted_checkruns_snapshot.tsv`): 31 completed with success, 1 skipped by design (Physical gPTP, nightly or manual only), and 24 still queued or in progress, among them Verilator shards, Yosys shards and firmware jobs. Nothing is claimed for contexts that had not finished.

## Pending manager duties

- Settle F1: either a recorded exemption decision, or the three-endpoint re-record on the merge result.
- Validate the current-dev merge candidate (builder and native banks) at the merge turn. The source base `ac0a01e3` equals the live `dev` tip.
- Accept hosted contexts and act evidence on the exact head.
- Carry R1 and R2 to the residue checklist.
- Re-review is needed at any new head. F1's outcome (a) would change the baseline record and the area documentation, which un-covers Docs and Conformance for that commit.

R804-1 FINISHED
