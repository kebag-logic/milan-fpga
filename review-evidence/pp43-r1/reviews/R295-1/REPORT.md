[R295] NEGATIVE - exact head 5771578784c77e945980c78faa52f3e54bcf5e2d

# R295-1 independent external review: PR #111 (issues #43, #49)

- Repository: Mister-M-alt/protocol-processor-control-plane-avb-milan
- Exact head: `5771578784c77e945980c78faa52f3e54bcf5e2d`, tree `8f898477a082ea32bf33533cf3ec8c8bd109363a` (verified in the clone: HEAD, HEAD^{tree} and the index write-tree all match; worktree clean, no ignored or untracked files; this repository has no gitlinks)
- Source base: `939c143333d11e2378a514f1c7b6abd4c3259bfd`. Reviewed diff: `939c143..5771578`, 15 files, +684/-73
- Reviewer role: external, cleared context, own detached clone. No source edits, commits, pushes or GitHub writes were made.

## Verdict

**NEGATIVE.** The processor now serves the input selectors correctly: selector 5 (the full 64-bit failure bridge ID), selector 7 (pbsta/acmpsta) and the selector 4 failure-code byte all come from the SRP registrar and the committed ACMP listener record. No top-level port was added. I reproduced all eight retained mutants, and the response-level acceptance list in the manager's seam decision is covered.

However, the change also rewrote the STREAM_INPUT notification trigger set and the SRP registration indication. Each rewrite has a side effect that the PR does not document or test, and both side effects are demonstrated below by a probe run on the base and on the head:

- **F1 (MAJOR).** A rebind to a different talker while the sink is ACTIVE with acmpsta 0 no longer raises a GET_STREAM_INFO notification, even when it changes the started/stopped state. That is a Milan Table 5.22 trigger that the base emitted.
- **F2 (MINOR).** A changed FailureInformation now re-declares the Listener attribute with an MSRP New on the wire.
- **F3 (MINOR).** The sample-and-hold registers are area-bearing and documented as a contract, but no test covers them: a transparent mutant survives both the focused bank and the full default bank.

## 1. Reconstruction (in the prescribed order)

1. **Guidance.** The repository has no `AGENTS.md` or `CONTRIBUTING.md` at this head (checked with `git ls-files`). Its conventions come from `README.md` (the gates are `run_suites.sh`, `lint_hdl.sh` and `make check`) and `docs/README.md`: the single-source rules (F02.10 holds the status names, F06.13 the lineage), and editing a figure requires `make check`.
2. **Frozen acceptance.** From the bodies of issues #43 and #49 and the manager's seam decision (issue #43 comment 5813138046, the same text on #49 as 5813138341):
   - both selectors are served inside the processor;
   - there are no new top-level ports;
   - response-level states come from the real state machines: DISABLED, PASSIVE, ACTIVE with acmpsta 7, COMPLETED, and acmpsta 0 outside PROBING_ACTIVE;
   - each sink shows its own Talker Failed code and 64-bit bridge, cleared on withdrawal, across two sinks;
   - solicited and unsolicited responses are equal;
   - mutants cover fields tied to zero, the wrong sink and the old integrator path;
   - parent consumer gates stay green.
3. **Authorities used.**
   - Milan clauses as the repository documents cite them: §5.3.8.6 and §5.3.8.8, Table 5.22, §5.5.3.5.x through the F05.3 listener matrix, and the started/stopped trigger quoted in `KL_pp_acmp_listener.sv:1039-1046`.
   - The repository's own contract text: F02.10, F06.13, 06 §7 and 10 §6.4.
   - IEEE 802.1Q MRP applicant semantics as cited in `KL_srp_listener_fsm.sv`.
   - The specification PDFs are not in the repository, so spec text is taken as quoted there.
4. **Diff and history.** Two commits: `0452c49` (the implementation) and `5771578` (a runner annotation). Every hunk was read in full.
5. **Public evidence.**
   - The evidence packet at `kebag-logic/milan-fpga@5d49561f/review-evidence/pp43-r1`. I listed the full tree (`receipts/public_evidence_tree.txt`) and used the base and candidate utilization reports and the mutant results. The manager's REVIEW READY comment is on issue #43 (id 5813813612).
   - Hosted checks at the exact head: suites, docs-gates and portability each completed with success in two workflow runs (`receipts/hosted_checks.txt`). All six jobs executed; none were skipped.
6. **Prior public findings.** PR #111 has two comments, both review-start notices (R294-1 and R295-1). There are no reviews and no review comments. Issues #43 and #49 carry only the decision and REVIEW READY comments. **There are no prior public FINDINGS to resolve or retain at this head.** I checked this after my own pass.

## 2. Field lineage (state owner, then selector, then response byte)

| Field | State owner | Path at head | Response |
|---|---|---|---|
| msrp_failure_code (input) | `KL_srp_listener_fsm.fcode_r[s]`, gated to 0 unless `tk_reg_state==FAILED` (`:808`) | `KL_srp_top.snk_fail_code_o` → `srp_snk_fail_code_w` → `gsi_fail_code_r` (sampled at the selector 0 beat, `protocol_processor_top.sv:3088-3107`) → selector 4 bits [15:8] (`:3113`) | byte @72 (AECPDU @52+6) |
| msrp_failure_bridge_id (input) | `fsysid_r[s]`, gated the same way (`:809`) | `snk_fail_bridge_o` (previously `_nc_w`) → `srp_snk_fail_bridge_w` → `gsi_fail_bridge_r` → selector 5 (`:3114`) | bytes @74..@81 |
| pbsta / acmpsta | ACMP listener record RAM (`pbsta`, `acmpsta`) | record write bus `dbg_recwr_*` → `lstn_gsi_status_r[sink]` (`:3057-3068`) → `gsi_status_r` → selector 7 (`:3115`) | byte @90 |
| Integrator isolation | — | `gsi_req_o = aecp_gsi_req_w && !gsi_internal_w`, and the wait is masked for selectors 5 and 7 (`:3084-3086`) | the harness counter `gsi_internal_leaks` stays 0 |
| Missing descriptor | descriptor store | `gsi_missing_w` suppresses the request and zeroes the data (`KL_aecp_engine.sv:1827-1832, :2015`) | full zero body |

The index guard is checked on the full 16-bit index before narrowing (`:3101`). A gather-watchdog void (`gxf_fail_r`) voids the response. Probe R3 confirmed that a voided gather followed by a query of another sink leaks no failure data at this head.

## 3. Findings

### F1: MAJOR. A rebind from an ACTIVE/acmpsta-0 state no longer notifies, even when started/stopped changes

- **Lenses:** Conformance, RTL, Tests, Docs.
- **Location:**
  - `hdl/top/protocol_processor_top.sv:3125-3134`: the `lstn_disc_arm_w`, `lstn_disc_disarm_w`, `lstn_act_settle_w` and `lstn_act_teardown_w` terms were replaced by `lstn_gsi_changed_r`.
  - `hdl/acmp/KL_pp_acmp_listener.sv:1417-1427`: `act_strt_chg_o` still excludes bind walks (`!bind_act_r`) "because those already push from their own discovery/teardown terms". Those terms no longer exist.
  - Comment at `protocol_processor_top.sv:3516-3518` ("also covering bound and settled transitions").
  - `docs/architecture/06_aecp_engine.md:242-244`.
- **Authority:**
  - Milan Table 5.22 lists the started/stopped state of a Stream Input as a GET_STREAM_INFO notification trigger (quoted at `KL_pp_acmp_listener.sv:1039-1046` and `:1412-1421`).
  - F05.3 row "BIND_RX new/different source": PWD, PWR and PW2 all go to PWR via A9, A2, A4 and A5, so the committed pbsta/acmpsta stays ACTIVE/0 and `lstn_gsi_changed_r` cannot fire.
  - A2 re-derives `f_started` from STREAMING_WAIT (`:1196`), and the integrator folds the published started view into the GET_STREAM_INFO flags (F06.13 row "BOUND, STREAMING_WAIT").
- **Evidence:** reviewer probe R1 (`scripts/r295_probe.hpp`, `receipts/probe_head.log`, `receipts/probe_base.log`). The sink is bound, and then rebound to a different talker inside T-ACMP-CMD with STREAMING_WAIT set.

  | Tree | Notifications on the rebind | `aecp_strm_started_o` |
  |---|---|---|
  | base `939c143` | 2 | 1 → 0 |
  | head | 0 | 1 → 0 |

  The head check `R295 R1: rebind that changes started/stopped raises a GET_STREAM_INFO notification` FAILS. None of the existing 1856 default checks, the 416 GI checks or the retained mutants exercise this row.
- **Impact:** A registered controller keeps a stale started/stopped (STREAMING_WAIT) view after a controller rebinds a probing sink to another talker. This regresses a Milan "shall" notification that the base emitted. The PR's docs and comments claim coverage that the RTL does not provide.
- **Required outcome:** Every committed change of a GET_STREAM_INFO-visible input field raises the notification again. Possible fixes include including the started/bound bits in the compared committed view, restoring the bind terms, or dropping the `!bind_act_r` exclusion with a de-duplication argument. Correct the listener comment, the top comment and 06 §7. Add a response-level test (rebind from PWR with a STREAMING_WAIT flip gives exactly one unsolicited response carrying the new value) and a retained mutant that removes the new trigger.
- **Verification:** Rerun probe R1 (`scripts/run_probe.sh <tree> <simulator> <log>`) and expect ≥1 notification. The new GI check must fail under the retained mutant.

### F2: MINOR. A failure-information change is signalled through the registration indication, which also re-declares the Listener with New on the wire

- **Lenses:** Conformance, RTL, Robustness, Tests, Docs.
- **Location:**
  - `hdl/srp/KL_srp_listener_fsm.sv:428-434`: `ind_reg_w` now also fires on a changed code or bridge.
  - `:532-535`: `ind_reg_w` sets `decl_pend_r = D_DECLARE_C`, and the applicant then applies `AE_NEW_C` (`:473`).
  - `:694`: `evt_tk_registered_o` is re-raised, then routed through the event router to the ACMP listener (`protocol_processor_top.sv:2813`), where SOK's EVT_TK_REGISTERED cell is "—" in F05.3.
  - `docs/architecture/10_srp_engine.md:307-311`, which describes only the notification.
- **Authority:** In 802.1Q MRP, a New event re-announces a declaration as new. The Listener's declaration type (AskingFailed) does not change when only the Talker's FailureInformation changes. The base re-declared only on a fresh registration or a type swap (`10 §6.4`).
- **Evidence:** reviewer probe R2 (`receipts/probe_*.log`). After settle and a first Talker Failed:

  | Tree | Listener New frames after a changed FailureInformation | After an unchanged refresh |
  |---|---|---|
  | base | 0 | 0 |
  | head | 2 | 0 |

  The head check `R295 R2: a changed FailureInformation does not re-declare the Listener with New` FAILS. The GI bank checks only the AECP side of this path.
- **Impact:** Extra MSRP New traffic and propagation are generated upstream each time the failure information along the path changes. Spurious TK_REGISTERED events reach the event router and the ACMP listener. None of this is documented or tested. The notification only needed a notify strobe.
- **Required outcome:** Choose one:
  - Separate a failure-information-changed strobe that feeds only the GET_STREAM_INFO notify path, with no applicant re-declaration and no ACMP event. Add a wire-level test that no Listener New follows a changed FailureInformation.
  - Or cite the authority that requires the re-declaration, document it in 10 §6.4, and test it at the wire.
- **Verification:** Probe R2 shows 0 New frames at a fixed head. Existing GI `FAILED-REFRESH` still notifies, and the reviewer mutant `srp-failure-change-strobe-removed` still kills it.

### F3: MINOR. The sample-and-hold state is area-bearing and documented as a contract, but is not verified

- **Lenses:** Tests, RTL, Docs.
- **Location:** `hdl/top/protocol_processor_top.sv:3071-3107`: `gsi_sampled_r`, `gsi_fail_code_r`, `gsi_fail_bridge_r` and `gsi_status_r`, 81 FF independent of the stream shape. `docs/architecture/06_aecp_engine.md:312-320` ("Sampling: … captures … together when selector 0 is accepted, then holds that sample").
- **Evidence:** Reviewer mutant `sample-transparent` resamples live values every cycle and never holds (`receipts/r295_mutants/results.json`, `receipts/r295_mutants_full/results.json`). It SURVIVES both the GI bank (416 checks, 0 failures) and the full default build (1856 checks, 0 failures).
- **Impact:** These registers are copies of state owned by the SRP registrar and the listener view (Section 4). Their only purpose is keeping one response coherent with the selector 0 flags beat, and nothing tests that property. Under the owner's low-area directive, unproven duplicated state is not acceptable, and the documented contract has no executable evidence.
- **Required outcome:** Choose one:
  - Add a response-level test in which the SRP failure information or the probing status changes between the selector 0 beat and selectors 4/5/7 of one gather (for example, the integrator holds selectors 1-3 while a Failed attribute arrives). The test must show that the response is internally coherent, and a retained mutant must kill a transparent sample.
  - Or remove the hold, read the owners live, and amend 06 F06.13.
- **Verification:** The `sample-transparent` mutant is killed by a named check, or the registers are gone and the docs no longer claim sampling.

### Suggestions (do not affect the verdict)

- **S1 (Tests).** The `sink-index-guard-removed` mutant survives the GI bank. The descriptor image never carries a STREAM_INPUT index ≥ `N_STREAM_IN_P`. The guard is correct by inspection, but consider adding one image entry beyond the shape to pin it.
- **S2 (RTL, area).** SRP `u_listener` grows by +808 LUT / +512 FF at 8x8. The FF are the previously pruned `fsysid_r`. The LUT come mostly from per-sink 64-bit `msrp_fail_bridge_o` gating and per-sink 72-bit change comparators. Gating once after the index mux, and comparing only on the hit sink, would reduce the cost. `u_decoder` gains +128 FF: `sysid_r` plus the `evt_failure_system_id_o` copy, both now unpruned.
- **S3 (Tests, portability).** `tb/pp_top/gsi_mutants.py:93` calls `os.sched_setaffinity`, which exists only on Linux.
- **S4 (Docs, RTL).** `dbg_recwr_*` now carries functional status. Consider renaming it or documenting it as a functional port.

## 4. Area judgement (owner directive: keep area low)

From the public 8x8 OOC reports (`receipts/area_delta.txt`, produced by `scripts/area_delta.py`):

| Contributor | dLUT | dFF | Necessary? |
|---|---|---|---|
| SRP listener `fsysid_r` plus gating and comparators | +808 | +512 | The storage is owned state that selector 5 needs (it was previously pruned). The LUT cost is reducible (S2). |
| SRP decoder (bridge capture pipeline, unpruned) | +96 | +128 | Needed on the event path. It holds two 64-bit copies (S2). |
| Top: listener status view (8x8 + 8 changed) | — | +72 | A small view of owned RAM state, written only from the record write bus. Acceptable. |
| Top: sample-and-hold | — | +81 | Duplicates owned state and is unverified (F3). |
| Other modules | about −264 net | +0 | Synthesis noise (admission −291, originator −79, rx_validator −55). |
| **Total** | **+640** | **+784** | |

The author's attribution of most of the FF to previously pruned per-sink bridge state is confirmed: 512 of the 784 FF. The +640 LUT headline understates the feature's direct cost. The SRP listener and decoder alone add +904 LUT, partly hidden by unrelated synthesis variance.

**Estimated shipping 1x1 cost (analytic, not synthesized):**

| Component | FF | LUT |
|---|---|---|
| Sample (shape-independent) | 81 | — |
| Decoder (shape-independent) | 128 | ~96 |
| `fsysid_r` for one sink | 64 | ~100 (SRP listener, 1/8 of the 8x8 delta) |
| Status view and changed bit | 9 | — |
| Top answer mux | — | ~70-100 |
| **Total** | **≈ 280** | **≈ 270-300** |

About 30% of the 1x1 FF delta is the unverified sample (F3). The top elaborates lint-clean at 1x1 with the pinned simulator (`receipts/focused_lint.log`).

## 5. Tests and mutants (reproduced)

- **Author runner.** `tb/pp_top/gsi_mutants.py` with the pinned simulator (identity: `--version` reports `5.050 2026-07-01 rev v5.050`; wrapper sha256 `905795b9…e92f`). The golden run passes 416/0. All 8 mutants are killed by their named checks, and the restored run passes (`receipts/author_mutants.stdout`, `receipts/author_mutants/*-run.log`, `results.json`).
- **Reviewer mutants** (`scripts/r295_mutants.py`):

  | Mutant | Bank | Result | Check |
  |---|---|---|---|
  | `srp-failure-change-strobe-removed` | GI | KILLED | FAILED-REFRESH unsolicited |
  | `status-compare-removed` | GI | KILLED | 91 failures |
  | `desc-type-ignored` | full | KILLED | G2 STREAM_OUTPUT byte-exact |
  | `sample-transparent` | GI and full | SURVIVED | F3 |
  | `sink-index-guard-removed` | GI | SURVIVED | S1 |

  The golden full default build passes 1856/0. The fixture build accounts for the remainder of the author's 1876.
- **Acceptance mapping, all met by GI at head:**
  - DISABLED after unbind;
  - ACTIVE then PASSIVE after bind with no talker (Milan 5.5.3.5.3 and 5.5.3.5.29, per F05.3 UNB→PWR via A4 and A5; the issue's "PASSIVE after bind" is reached after backoff);
  - ACTIVE with acmpsta 7 after a double timeout;
  - COMPLETED after settle;
  - acmpsta 0 in every observed non-ACTIVE state;
  - code 7/11 and two distinct 64-bit bridges on sinks 0 and 1;
  - Advertise replacement and withdrawal clear both fields;
  - solicited and unsolicited bodies are byte-equal;
  - a missing descriptor gives a zero body;
  - reset over erased NVM;
  - no integrator request for input selectors 5 or 7.

  The gaps are the rows in F1, F2 and F3.
- **Existing-suite edits** (sim_main: `GI-isolation`, `refresh_source0`, `run_ms(4500)`). These exist because probe timeouts now notify, which Table 5.22 requires. The edits isolate unrelated phases and weaken no assertion that I could identify.

## 6. Docs single-source

- F02.10 gains an "internal" row. F06.13 is the lineage and sampling home, and the integrator guide §8 links to it. There are no duplicated values.
- 06 §7, the top-level notify comment and the listener comment are now inaccurate (F1). 10 §6.4 omits the re-declaration side effect (F2). The F06.13 sampling paragraph is unverified (F3).
- The `make check` docs gate is taken from the manager's evidence and the hosted docs-gates job (success). I did not re-run it.

## 7. Reviewer-owned ledger

| Lens | Status | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1, F2) | F05.3 matrix and A-actions; Table 5.22 trigger set vs `stri_events`; Milan §5.3.8.6/.8 field placement @72/@74/@90; 802.1Q applicant path in `KL_srp_listener_fsm.sv`; probes R1 and R2 on base and head | R295-1 | 5771578784c77e945980c78faa52f3e54bcf5e2d |
| RTL | UNCLEAN (F1, F2, F3) | `protocol_processor_top.sv:3046-3134`, `KL_aecp_engine.sv` gather, missing and watchdog paths, `KL_srp_listener_fsm.sv` registrar and applicant, `KL_pp_acmp_listener.sv` write-back and preload; focused lint of 4 modules plus top at 1x1 (0 findings); 8x8 area deltas and 1x1 estimate | R295-1 | 5771578784c77e945980c78faa52f3e54bcf5e2d |
| Robustness | UNCLEAN (F2) | gather-watchdog void and cross-sink leak (probe R3 clean); reset and preload paths of the status view; index guard; wire side effects of the new indication (R2) | R295-1 | 5771578784c77e945980c78faa52f3e54bcf5e2d |
| Tests | UNCLEAN (F1, F2, F3) | `gsi_internal.hpp` (416 checks) and full default build (1856); 8 author mutants reproduced; 6 reviewer mutants (2 survivors); probes R1, R2 and R3 | R295-1 | 5771578784c77e945980c78faa52f3e54bcf5e2d |
| Docs | UNCLEAN (F1, F2, F3) | 02 F02.10, 06 §6.2, F06.13 and §7, 10 §6.4, integrator guide §8, tb/pp_top README, syn/ooc README and tcl, in-RTL comments | R295-1 | 5771578784c77e945980c78faa52f3e54bcf5e2d |

## 8. Real limits

- I ran no synthesis. Area comes from the public 8x8 reports, and the 1x1 figures are an analytic estimate.
- There was no 1x1 simulation, only a 1x1 lint elaboration. The pp_top bench is fixed at 8 sinks.
- I did not re-run the full suite bank, `make check`, the full lint bank or any parent consumer gate (not permitted, or already covered by manager receipts). I re-ran only pp_top (GI-only and the default build) and focused lint.
- Probe R2 measures what the processor puts on the wire. It does not model how a bridge reacts to the extra New.
- Specification PDFs are not in the repository; spec text was taken as the repository quotes it.
- Physical calibration was NOT RUN, and field skips are not hardware proof.

## 9. Pending manager duties

- The parent consumer gates with this head as the processor gitlink at parent dev `fa65182adfe2eae15d1a2dbb15e40fb0594b5d66`. The author's evidence used an isolated copy of parent `3eaee03f`, and the designated-checkout pin guards refused with rc 2.
- The final current-dev candidate build at merge (source base `939c143`).
- Hosted/act acceptance (the six exact-head hosted jobs I inspected all executed with success).
- A second independent positive review after F1-F3 are resolved.

## 10. Receipts

All published receipts and scripts are listed in `MANIFEST.sha256`. Local build logs contain host paths and are not published.

R295-1 FINISHED
