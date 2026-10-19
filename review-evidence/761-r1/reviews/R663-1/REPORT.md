[R663] NEGATIVE - exact head 4191b0987d1313abc86c747ad6a9c3c0963f17da

# R663-1: internal cleared-context review of PR #767 (Closes #761, #762)

- Head `4191b0987d1313abc86c747ad6a9c3c0963f17da`, tree `5c21b067fcad3e7ff7017190f088c7ae0528b807`; two commits on dev `e9cbb676d7fdd6539aa408e5dfe38870a4ae1a5f`: `f443ed9b` (#761) and `4191b098` (#762). Both commit messages are one line with no trailers.
- I reconstructed the task from AGENTS.md, the bodies of issues #761 and #762, the assignment (issue #761, comment 6256482625), the executor's TAKEN and REVIEW READY comments, the PR body, the diff `e9cbb676..4191b098`, the published evidence tree `9020398b:review-evidence/761-r1`, and the exact-head hosted check runs.
- No earlier review finding exists on this PR. At my start the PR had one comment, the review-start notice, and no reviews or review comments. So nothing is carried over to retain or resolve.
- All five lenses were applied at this head. The verdict is NEGATIVE because of one open BLOCKER and two open MINORs.

## Findings

### F1 BLOCKER: a required docs gate is red at this head because the change grew the mclk case inventory past 32

- **Lenses:** Tests, Docs.
- **Where:**
  - The failing control is `scripts/ci_case_receipts_selftest.py:172`.
  - The commands run as `.github/workflows/docs.yml:434-449` (gate_50, "CI scheduling and evidence controls").
  - The cause is `tb/verilator/milan_dp_mclk/mclk_mutants.py:181-184`, the new mutants 17 and 18.
- **Authority and evidence:**
  - The selftest reads the mclk driver's inventory (`DRIVER`, `:20`). It requires `receipts.partition(names, "0/32")` to be refused, and `scripts/ci_case_receipts.py:51` refuses only when the shard count exceeds the case count.
  - At base the driver lists 31 cases. At this head it lists 34, because the PR added mutants 17 and 18 and the `crfloss` leg (`receipts/mclk_inventory_counts.txt`). So the control is now accepted, and the selftest fails.
  - Hosted job `docs-gates-0` (job 117907490702) executed at this head and failed with `AssertionError: receipt control accepted: shard 0/32` (`receipts/hosted_docs-gates-0_failed_step_tail.txt`). Fail-fast then cancelled every other hosted gate (`receipts/hosted_checkruns_4191b098.tsv`). The same job succeeded at dev `e9cbb676`.
  - Locally I ran all 14 gate_50 commands (`scripts/ci_controls_step.sh`, `receipts/ci_controls/`):
    - At head, 13 commands give rc 0. Only `ci_case_receipts_selftest` fails (rc 1).
    - At base, `ci_case_receipts_selftest` gives rc 0 ("31 driver cases").
  - Assignment item 3 requires every gate the change touches to return rc 0. The author's 42 static gates (`author/receipts/final-static/gates.tsv`) do not include gate_50's commands. The REVIEW READY comment and the PR body still state "Required local verification bar passes".
- **Impact:**
  - The PR cannot merge, because `docs-check` refuses the head.
  - At every head that carries this, fail-fast cancels the exhaustive `verilator-suites`, `yosys-portability` and `rtl-fast` contexts. So no exact-head hosted RTL evidence can exist.
  - The published verification claim is false for one touched gate.
- **Required outcome:**
  - Every gate_50 command returns rc 0 at the new head.
  - The over-shard negative control still refuses a shard count larger than the driver's real inventory. It must not be removed or loosened into a vacuous form.
  - The PR evidence records the gate_50 step.
- **Verification:**
  - Run `scripts/ci_controls_step.sh <tree> <out> head` at the new head and expect all 14 at rc 0.
  - Exact-head hosted `docs-gates-*` and `docs-check` must succeed. The cancelled exhaustive contexts must then execute.

### F2 MINOR: the two receive engines disagree on a bound, STOPPED input whose talker falls silent, and the docs claim they behave alike

- **Lenses:** Conformance, Robustness, Docs.
- **Where:**
  - AAF engine: `hdl/ieee1722/avtp/KL_avtp_rx_monitor_ctx.sv:904-905`.
  - CRF sink: `hdl/ieee1722/crf/KL_crf_rx.sv:552-556`.
  - Stop gate: `hdl/milan/milan_datapath.sv:6264-6287`.
  - Docs: `docs/reference/MILAN_COMPLIANCE_MATRIX.md:131` and `docs/reference/REGISTER_MAP.md:873-877`.
- **Authority and evidence:**
  - Milan v1.2 5.3.8.10 Table 5.6 counts STREAM_INTERRUPTED for any interruption of playback "other than a Controller Unbind". Under 5.3.8.7, a stopped input already discards its AVTPDUs.
  - The CRF sink never counts a timeout while stopped (`en_i && !stop_i`, `KL_crf_rx.sv:556`). This is pinned: my probe dropping `!stop_i` is caught by `crf_rx [ST-c3]` (`receipts/probes/probes_1.log`).
  - The AAF engine has no stop input (ports `:123-225`). It sits upstream of the 5.3.8.7 discard (`milan_datapath.sv:6268-6287`: "`KL_avtp_rx_monitor_ctx` sits upstream of this gate"). Its new mark is set for any bound stream (`bound_i[s] && !bind_fall_i[s]`, `:905`).
  - So a bound, STOPPED AAF input whose talker stops for 100 ms now unlocks and counts STREAM_INTERRUPTED. The CRF input in the same state counts nothing. I established this by RTL reading; it is not simulated.
  - The compliance matrix states the silence law holds "on the AAF and CRF inputs alike".
  - REGISTER_MAP excludes "the timeout of a stopped input" and then says "The AAF inputs' `KL_avtp_rx_monitor_ctx` keeps the same two causes".
  - The PR's known limitations name only the CRF half of the stopped case.
- **Impact:** for the same controller sequence (STOP_STREAMING_INPUT, then the talker falls silent), GET_COUNTERS reports a different STREAM_INTERRUPTED depending on the input's type. A conformance-matrix claim is wrong for that state.
- **Required outcome:**
  - One stated law for a bound-and-stopped input's silence across both engines, or the asymmetry recorded as a decision beside the stopped-input question the executor already raised.
  - The matrix row and the REGISTER_MAP paragraph state what each engine actually does.
- **Verification:**
  - Re-read the RTL and docs at the corrected head.
  - If behaviour changes, a test grades the stopped-then-silent case for each engine.

### F3 MINOR: the unbind-on-a-pending-silence law is graded only against a copy of the implementation

- **Lenses:** Tests, Docs.
- **Where:**
  - Rule stated at `hdl/ieee1722/avtp/KL_avtp_rx_monitor_ctx.sv:890-892`.
  - Sweep at `tb/verilator/avtp_rxmon/sim_lockstep.cpp:515-542`.
  - Claim at `tb/verilator/avtp_rxmon/reference/KL_avtp_rx_monitor_ctx_ref.sv:9-10` ("#762 itself is graded by count in the harness's [SI] cases, never against this copy"), with the same claim at `sim_lockstep.cpp:38-44`.
- **Authority and evidence:**
  - AGENTS section 6, Tests lens: "Tests do not merely reproduce implementation assumptions". The frozen M6 reference now carries the same #762 lines as the engine.
  - Probe `aaf_eng` removes `:892` (an unbind clears a pending silence mark) in the engine only. It is caught only by `[LS] SI sweep` and `[GC] SI sweep`, the cycle comparison against the mirrored copy.
  - Probe `aaf_both` makes the same edit in the engine and the reference. All 53 checks then pass at N=1 and at N=8 (`receipts/probes/aaf_both.N1.log`, `.N8.log`, `planted_edits.diff`).
  - The sweep's oracle accepts any mix: at most one count per trial (`:534`) and `0 < counted < trials` (`:540`). So it cannot tell which order counts.
- **Impact:**
  - A change to the stated law that is mirrored into the reference passes every check.
  - The published claim that #762 is graded independently of the copy is untrue for this rule.
- **Required outcome:**
  - A count oracle that does not depend on the mirrored reference grades the boundary outcome at each sweep point: the unbind arrives before the watchdog fires, while its unlock walk is pending, or after the walk. The law at each point is the one decided.
  - The `aaf_both` edit is killed by an `[SI]` check.
- **Verification:** run `scripts/probes.py <tree> <work> aaf_both` and expect CAUGHT by an `[SI]` check.

### S1 SUGGESTION: no dynamic grader for the new edge's clock-source gate

- **Lens:** Tests.
- **Where:** `hdl/milan/milan_datapath.sv:3247-3250`. The gating contract is stated at `:3195-3198`.
- **Evidence:**
  - Probe `mclk_ungated` moves the lock-gain request outside `crf_clk_selected_r`. It passes mclk legs A, B and C (55, 51 and 32 checks, `receipts/probes/mclk_ungated.*.log`).
  - The builder's exact-initializer pin (`sw/builder/test_builder.py:11379-11385`) refuses that text statically. So this is not open.
- **Suggested change:** add a row in which the CRF sink re-locks while INTERNAL or an AAF source is selected and no request is raised, with an ungated mutant.

No RESIDUE.

## Lens coverage, with the evidence for what is clean

**Conformance: UNCLEAN (F2).** Apart from F2, the acceptance criteria are met, as follows:

- **#761, either edge requests a restart.** `milan_datapath.sv:3247-3250` uses `tkd_crflk_q_r ^ crf_locked_w`, still under `crf_clk_selected_r`. The received-mr echo and the AAF-meter terms are unchanged.
- **Return toggles once.** The mclk `crfloss` row requires exactly one request and one `mr` toggle per output on the return. I reproduced it: 34/34, with mutants 17 (gain edge dropped) and 18 (loss edge dropped) caught by their named checks (`receipts/suites/mclk.log`).
- **No double toggle on a fast loss and return.**
  - Lock edges are at least 8 accepted PDUs apart (`KL_crf_rx.sv:594-600` settle, `:545-577` timeout, `:640-644` unbind).
  - The received-mr reference re-seeds at the silence and at the bind (`:573`, `:654-659`). A stopped sink's toggles update the reference without echoing (`:482`, `:605`). So the first PDUs of a return cannot raise an echo.
  - `KL_media_clock_restart.sv` merges a request landing on a pending one (#387).
- **#762, each cause counts as specified, in both engines:**
  - A silence counts once: crf_rx `[762-a]`, avtp_rxmon `[SI]`, nx `[G6-762]`, and milan_dp `[CTRS-CRF]` STREAM_INTERRUPTED = 3 at the root (`milan_dp_nxn.log`, 1,968 checks, 0 failures).
  - The resume adds nothing: `[762-b]`, `[SI]`.
  - A gap counts once: `[SI]`, `[5t-e2]`.
  - An unbind counts nothing: `[UNB-a6]`, `[UNB-d5]`, `[SI]`, and the root `[UNB]` U3/U4 with STREAM_INTERRUPTED 0 on AAF and CRF (`milan_dp_notify.log`, 423 checks, 0 failures).
- **MEDIA_LOCKED / MEDIA_UNLOCKED unchanged:** the `[SI]` MEDIA_UNLOCKED checks, C1 in mclk, `[UNB-d2]` to `[UNB-d4]`.
- **No register-map, top-level port or parameter change.** The diff touches no port or parameter, and `REGISTER_MAP.md:873-877` is prose only.

**RTL: CLEAN.** Covering round R663-1 at `4191b098`. I read the following against IEEE 1722-2016 4.4.4.3 and Milan Table 5.6:

- `milan_datapath.sv:3206-3250`. `tkd_crflk_q_r` resets to 0 in the same `axis_resetn` domain as `KL_crf_rx` (`:5866`), so reset release raises no gain edge.
- `KL_crf_rx.sv:543-577` and `:630-644`. The timeout count is exclusive of `w_ev_si_w` because the started timeout branch implies no accept. An unbind on the timeout edge counts nothing.
- `KL_avtp_rx_monitor_ctx.sv:880-909`, `1051-1076` and `1125-1141`:
  - `sil_si_r` is cleared on reset, at the walk's end, on unbind and at the bind-era wipe.
  - The STREAM_INTERRUPTED RMW enters `M_INC_S` with `inc_rd_q_r`, `w11_mode_r` and `bind_zero_r` all 0, and yields to PDU pressure through the existing single park slot.
  - A parked remainder dies with the era.
- No CDC is added.
- Lint gate: PASS, 90 <= ratchet 90 (`receipts/suites/lint.log`).
- route-1x1 from the author's receipts (`author/receipts/route/cand`):
  - WNS +0.161 ns (>= +0.03) and WHS +0.036; fully routed; `pp_resource_gate.py check` rc 0.
  - LUT 49,411 (-202), FF 52,297, SLICE 15,751 (+26).
  - The worst path is in the SoC CPU.
  - The base route equals the record. The route's submodule list matches the head's gitlinks.

**Robustness: UNCLEAN (F2).** The other examined paths are clean:

- Reset during activity: the shared reset domain, plus `[H4]` and the soak `[SO]` at N=1 and N=8.
- Unbind and timeout on one edge (`[UNB-d5]`), and an unbind swept across the silence unlock (`[SI]` sweep: one unlock each, never two counts).
- Rebind wipe (`ctx:1138`, `:1141`).
- A stopped CRF sink: probe `crf_stop` is caught by `[ST-c3]`.
- The 8-listener shape (`lockstep N=8`).
- A fast loss and return, as described under Conformance.

**Tests: UNCLEAN (F1, F3).** My reproductions at this head, under the identified 5.050 simulator (`receipts/verilator_identity.txt`):

| Suite or leg | Result |
|---|---|
| crf_rx | 14,291 + 2,201 + 69 checks, 0 failures; mutants 15/15, including all four #762 mutants |
| avtp_rxmon | flat 97 and nx 121 checks, 0 failures; lockstep 53/53 at N=1 and at N=8; lockstep mutants 8/8, including the silence, gap and unbind mutants |
| milan_dp_mclk | campaign 34/34 (`receipts/suites/`) |
| milan_dp nxn | 1,968 checks, 0 failures |
| milan_dp notify | 423 checks, 0 failures |
| milan_dp base | 236 checks, 0 failures |
| milan_dp ax1x1 | 233 checks, 0 failures |

Each new #762 and #761 mutant is caught by its named check.

**Docs: UNCLEAN (F1, F2, F3).** The other examined artifacts are clean:

- `MEDIA_CLOCK_FOLLOWING.md:1397-1409` and `:1649`, `GM_LOSS_RECOVERY.md:179`, `BAREMETAL_FIRMWARE.md:1612`, `MILAN_COMPLIANCE_MATRIX.md:217`, `TESTING.md:614` and `:645`, and the mclk README mutant table all match the RTL and the measured runs.
- Source-comment rule: the comments added in the delta state behaviour with issue and clause IDs. A scan of every added line found no bench lane label, lane name, review round, reviewer ID or issue-comment ID in source (the only issue-comment links are existing #602 ruling links in docs).
- Receipts index: `author/receipts/INDEX.md` matches its files, 170 listed and 170 present with sizes and SHA-256 equal (`receipts/receipts_index_check.log`). The evidence `MANIFEST.json` matches 175/175 (`receipts/evidence_manifest_check.log`).

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F2) | issues #761/#762 acceptance; `milan_datapath.sv:3247-3250`; `KL_crf_rx.sv:545-600,640-659`; `KL_avtp_rx_monitor_ctx.sv:880-909,1051-1076`; mclk `crfloss` row; `[SI]`, `[762-*]`, `[UNB-*]`, `[CTRS-CRF]`, root `[UNB]` U3/U4 | R663-1 | 4191b0987d1313abc86c747ad6a9c3c0963f17da |
| RTL | CLEAN | `milan_datapath.sv:3206-3250,5866`; `KL_crf_rx.sv:543-644`; `KL_avtp_rx_monitor_ctx.sv:880-909,1051-1141`; `KL_media_clock_restart.sv` merge; lint log; route-1x1 receipts | R663-1 | 4191b0987d1313abc86c747ad6a9c3c0963f17da |
| Robustness | UNCLEAN (F2) | stopped state (both engines); reset; unbind/timeout same edge; unbind sweep; rebind wipe; N=8; probe `crf_stop` | R663-1 | 4191b0987d1313abc86c747ad6a9c3c0963f17da |
| Tests | UNCLEAN (F1, F3) | gate_50 commands at head and base; crf_rx, avtp_rxmon, mclk, milan_dp nxn/notify/base/ax1x1 runs; probes `aaf_eng`, `aaf_both`, `crf_stop`, `mclk_ungated` | R663-1 | 4191b0987d1313abc86c747ad6a9c3c0963f17da |
| Docs | UNCLEAN (F1, F2, F3) | matrix `:131,:217`; `REGISTER_MAP.md:873-877`; `MEDIA_CLOCK_FOLLOWING.md`; `TESTING.md`; mclk README; reference/lockstep claims; PR body and REVIEW READY; receipts INDEX and MANIFEST | R663-1 | 4191b0987d1313abc86c747ad6a9c3c0963f17da |

## Real limits

- **Not run by me:**
  - the full 63-suite sweep, the builder bank, Yosys, xvlog, the route-1x1 Vivado run, and the full gm-step mutant campaign (the author ran the last at `f443ed9b`; the #762 commit does not touch its datapath anchors).
  - For these I examined the author's receipts only.
- **F2 rests on RTL reading.** The AAF stopped-then-silent behaviour was not simulated.
- **Base comparison of gate_50.** My base clone had no submodules, so three base commands failed for that environmental reason (`receipts/ci_controls/ci_controls.base.*.log`). The F1 command passed at base, and hosted `docs-gates-0` succeeded at `e9cbb676`.
- **Hosted runs used the merge ref, not the source head.** The hosted runs at this head validated merge ref `42b5f1c0`. Only `docs-gates-0` executed to a root failure; every other red context is fail-fast fallout.
- **No hardware.** Physical calibration was NOT RUN, and builder gate 11 is NOT RUN (author receipt). Neither is hardware proof.
- **No manager source bank** runs at this exact head, and none is claimed or inferred.

## Pending manager duties

- Hosted and act acceptance at the corrected head. After F1 is fixed, the cancelled `verilator-suites`, `yosys-portability` and `rtl-fast` contexts must execute.
- The current-dev merge-candidate validation (builder and native banks) at the merge turn.
- Re-review at the head that answers F1 to F3. Any commit touching these artifacts un-covers the RTL lens's examined scope as well.

R663-1 FINISHED
