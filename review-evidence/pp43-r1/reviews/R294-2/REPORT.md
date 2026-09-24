[R294] POSITIVE - exact head a14ef8b4787b5309dd9ab472e82ae2b4a3fdbb72

# R294-2 independent review: PR #111 (issues #43, #49), round 2

- Repository: Mister-M-alt/protocol-processor-control-plane-avb-milan
- Exact head: `a14ef8b4787b5309dd9ab472e82ae2b4a3fdbb72`, tree `71081cc12048a81b920dc48b9a508e3b120b96e3`. HEAD, HEAD^{tree} and the index write-tree match in the review clone (`receipts/clone-integrity.txt`).
- Source base: `939c143333d11e2378a514f1c7b6abd4c3259bfd`. Reviewed diff `939c143..a14ef8b`: 26 files, +1264/−130. Round-2 delta `5771578..a14ef8b`: three commits (`f28e90b` RTL, tests and docs; `68ad935` OOC recipe shape argument and area record; `a14ef8b` test only).
- Role: internal reviewer, cleared context, own detached clone. I made no source edits, commits, pushes or GitHub writes.

## Verdict

**POSITIVE.** At this head I have no open MINOR, MAJOR or BLOCKER finding. Every round-1 finding, mine and the other reviewer's, is resolved (§4).

- A changed FailureInformation now only raises a notification. On the wire it never re-declares the Listener.
- A re-bind that flips STREAMING_WAIT notifies exactly once.
- The selector-0 sample-and-hold is gone, and F06.13 states the bound that replaces it.
- The area follow-ups are in, and the published numbers match the reports.

My round-1 probes P1 and P2 pass unchanged. My round-1 mutant `notify-every-write` is killed unchanged. My four mutants whose sites were removed by design are correctly accounted for (§3.3).

I record four SUGGESTIONS (S1 to S4). None of them affects the verdict.

## 1. What was reconstructed

1. **Guidance.** The repository has no AGENTS.md or CONTRIBUTING.md at this head. Its conventions come from `README.md` (gates: `run_suites.sh`, `lint_hdl.sh`, `make check`), `docs/README.md` (the single-source rules: status names in F02.10, lineage in F06.13), and `docs/guides/hdl-engineer.md`: synchronous reset, the 1W1R storage rule, "count, never swallow", and the listener as a ROM walker.
2. **Frozen acceptance.** Taken from the bodies of #43 and #49 and the manager's seam decision (issue #43 comment 5813138046, the same text on #49): both selectors are served inside the processor, and there are no new ports. Response-level states: DISABLED, PASSIVE, ACTIVE with acmpsta 7, COMPLETED, and acmpsta 0 outside PROBING_ACTIVE. Each sink reports its own Failed code and 64-bit bridge, cleared on withdrawal, across two sinks. Solicited equals unsolicited. Mutants: fields tied to zero, wrong sink, old integrator path.
3. **Round-2 decision** (issue #43 comment 5814505442, [A255]):
   - rebind started/stopped notification with a response test and a retained mutant;
   - a separate FailureInformation-change strobe with no MRP New and no TK_REGISTERED, plus a wire-level test;
   - the sample-and-hold removed, owners read live, the bound documented in F06.13 and the registers saved reported;
   - the bridge gated once after the index mux, the compare done on the hit sink only, and both OOC shapes reported;
   - an index-guard test, portable CPU affinity, and `dbg_recwr` documented.
4. **Authorities.** Milan §5.3.8.6/.7/.8, Table 5.22, and §5.5.3.5.x through F05.3, as the repository cites them. The repository's F02.10, F06.13, 06 §7 and 10 §6.4. IEEE 802.1Q MRP applicant and registrar semantics as cited in `KL_srp_listener_fsm.sv`. The engine face contract at `KL_aecp_engine.sv:432,450` ("HOLD the beat (not a ready)").
5. **Diff and history.** I read every hunk of `939c143..a14ef8b`, and also the unchanged consumers the new code depends on: the notification intake and clear at `KL_aecp_notify.sv:758,987`, the listener write bus at `KL_pp_acmp_listener.sv:738-765`, and the X_WB pulse at `:1418-1422`.
6. **Public evidence.** The `author-r2` directory at `kebag-logic/milan-fpga@87b38a25/review-evidence/pp43-r1`. I read the gate, mutant, probe and area receipts, and the reviewer-mutant wrapper `reviewer-mutants/drive.py`. I did not open that packet's `reviews/` directory. I also read the manager and author comments on #43 and #111. Hosted runs are in §6.

## 2. Findings

No MINOR, MAJOR or BLOCKER finding is open at this head.

### R294-2-S1: SUGGESTION. The top's internal-selector wait mask is load-bearing but no test exercises it

- **Lenses:** Tests, Robustness.
- **Where:** `hdl/top/protocol_processor_top.sv:3092` (`aecp_gsi_wait_w = !gsi_internal_w && gsi_wait_i`). The harness drives `gsi_wait_i` only while `gsi_req_o` is high (`tb/pp_top/sim_main.cpp:1507-1514`).
- **Authority:** The engine documents `gsi_wait_i` as "HOLD the beat (not a ready)" and qualifies it with its own request (`KL_aecp_engine.sv:450,1978`). An integrator may therefore leave HOLD high between beats. 06 §6.2 (`06_aecp_engine.md:221`) promises that selectors 5 and 7 "ignore external wait/data".
- **Evidence:**
  - Reviewer mutant `r2-internal-honours-external-wait` removes the mask. It SURVIVES the GI phase (`receipts/r2-mutants-3/results.json`).
  - Probe W (`scripts/probe_idle_wait.sh`) models an integrator that holds HOLD high whenever no request is up. The head passes 488/0 (`receipts/probe-w-idle-wait-head.log`). With the mask removed, the result is 97 failures of 158 (`receipts/probe-w-idle-wait-mask-removed.log`).
- **Impact:** The RTL is correct today, but a regression in the mask would pass every retained check.
- **Suggested outcome:** Add the idle-HOLD integrator mode to the GI harness, or a retained mutant killed by such a check.

### R294-2-S2: SUGGESTION. The index guard's boundary (index = N_STREAM_IN_P) is not tested

- **Lenses:** Tests.
- **Where:** `protocol_processor_top.sv:3099`. GI INDEX-GUARD queries only index 9 (`tb/pp_top/gsi_internal.hpp:261-265,354`).
- **Evidence:** Reviewer mutant `r2-index-guard-off-by-one` (`<` becomes `<=`) SURVIVES (`receipts/r2-mutants-1`). The guard itself is correct. Probe Q4 queries index 8 of the ten-input image while sink 0 is COMPLETED and gets zero internal fields; sink 0 reads pbsta 3 as the control (`receipts/probe-q-head.log`).
- **Suggested outcome:** Also query index N_STREAM_IN_P, with the aliased sink 0 non-zero as the control.

### R294-2-S3: SUGGESTION. `bnd_was_r` is called load-bearing, but no unit check pins it

- **Lenses:** Tests, Docs.
- **Where:** `hdl/acmp/KL_pp_acmp_listener.sv:338-342` ("The bound-before half is load-bearing").
- **Evidence:** Reviewer mutant `r2-strt-chg-bound-before-removed` SURVIVES both `tb/acmp_listener` (2544/0) and GI (`receipts/r2-mutants-3`).
  - At the top it is equivalent: a fresh bind also moves pbsta from DISABLED to ACTIVE in the same X_WB write, so the two terms OR into one frame.
  - At the module level it does break the pulse's own contract. The pulse would fire on an undefined-to-started step, which Milan §5.3.8.7 says is not a started/stopped change.
- **Suggested outcome:** Add a unit check that a fresh bind from UNBOUND without STREAMING_WAIT raises no `act_strt_chg_o`. Alternatively, soften the comment.

### R294-2-S4: SUGGESTION. The coherence bound could name who receives the follow-up

- **Lenses:** Docs.
- **Where:** F06.13, "Coherence bound" (`docs/architecture/06_aecp_engine.md:312`).
- **Evidence:** The bound is sound as written, because the notification clears a pending bit when it selects an emission (`KL_aecp_notify.sv:987`). A change after that selection therefore re-arms another emission. That follow-up reaches only registered controllers. A solicited reader that is not registered keeps the one mixed response until its next poll.
- **Suggested outcome:** Add half a sentence saying so.

## 3. Evidence at this head

### 3.1 Suites and gates (pinned simulator, verified: wrapper sha256 `905795b9…e92f`, `Verilator 5.050 2026-07-01 rev v5.050`; `receipts/tool-identity.txt`)

| Run | Result | Receipt |
|---|---|---|
| GI focused (`make gsi-build`, `--gsi-internal-only`) | 488 checks, 0 failures | `head-gsi-internal-only.log` |
| pp_top full (`make`) | 1948 PASS, 0 FAIL | `head-pp_top.log` |
| srp_stream_fsms | 1087/0 | `head-srp_stream_fsms.log` |
| srp_top | 259/0 | `head-srp_top.log` |
| acmp_listener | 2544/0 | `head-acmp_listener.log` |
| aecp_notify | 10/0 | `head-aecp_notify.log` |
| Scoped lint with the repository flags: top at default, 1x1 and 8x8; SRP listener, SRP top and ACMP listener at default and at one sink; AECP engine | 10 of 10 OK | `scoped-lint.txt` |
| `gen_matrix.py --check` and `make check` | OK (92 rows, 0 untested; links 846) | `docs-gates.txt` |
| `git diff --check` over the base-to-head diff | rc 0 | (command output, §8) |

The measured counts match the PR body and the suite READMEs.

### 3.2 My round-1 probes, re-run unchanged (`scripts/probe_srp_redeclare.sh`, `scripts/probe_top_redeclare.sh`)

- **P1, unit, head:**
  - `changed-failure: fcode=9 bridge=bbbb0000dddd reg_strobes=0`
  - `changed-failure next tick pushes=0`
  - The unchanged refresh is silent.
  - The suite gives 1087/0. Base is identical (1068/0).
  - This was the required verification for my round-1 F1.
- **P2, top, head:**
  - `changed-failure: 0 listener declaration(s) for sink 0`
  - The unchanged window shows only the periodic JoinMt (event 3).
  - GI gives 488/0.

### 3.3 My round-1 mutants, and the four sites removed by design

Run unchanged, `scripts/extra_mutants.py` stops at its first entry: `srp-failure-strobe-removed: expected 1 site(s), found 0` (`receipts/extra-mutants-unchanged.txt`). My round-2 driver `scripts/r2_mutants.py` imports that list byte for byte (Part A) and adds my own re-expressions (Part B).

| Round-1 mutant | Site at head | Judgement | Re-expression (mine) | Result |
|---|---|---|---|---|
| `notify-every-write` | unchanged | still meaningful | — (run unchanged) | KILLED, GI BIND-TIMEOUT |
| `srp-failure-strobe-removed` | gone | removed by design: the change term left `ind_reg_w` for its own strobe | `r2-srp-failure-notify-dropped-at-top` (strobe dropped at the top's OR) | KILLED, GI FAILED-REFRESH unsolicited |
| `sel4-integrator-byte` | gone (renamed `_r` to `_w`) | same behaviour, site moved | `r2-sel4-integrator-byte` | KILLED, GI RESET failure code |
| `index-guard-removed` | gone (guard now on the live reads) | same behaviour, site moved | `r2-index-guard-removed`; also `r2-index-guard-after-narrowing` (compares the narrowed index, the aliasing form) | both KILLED, GI INDEX-GUARD sink 9 |
| `live-unsampled-fields` | gone | moot: live reads are now the design, by manager decision | none | — |

**The author's wrapper** (`author-r2/reviewer-mutants/drive.py`):

- It imports the reviewer's script as published.
- It keeps every entry whose site still exists byte for byte.
- It reports gone sites, and re-expresses them only under a `~translated` name.
- Its three translations match my own independent choices in edit and intent. Its "moot" judgement for the live-read mutant is right.
- Its receipts show the same verdicts as mine.

I accept the wrapper as a faithful re-application.

The other reviewer's probes (R1, R2, R3) and its `sink-index-guard-removed` mutant are that reviewer's material, so I did not run them. The same behaviours are covered here by my own runs:

- the re-bind notification: GI REBIND-SW and probe Q1;
- no Listener New: P2, probe Q2 and GI FAILED-REFRESH wire;
- no leak: GI MISSING and probe Q4 (the sample registers that could have leaked no longer exist);
- the index guard: my two guard mutants.

The author's public receipts show R1 = 1 notification, R2 = 0 New, R3 no leak, and `sink-index-guard-removed` killed.

### 3.4 Retained mutant runner, re-run by me (`tb/pp_top/gsi_mutants.py` unchanged, three slices via `scripts/run_retained_slice.py`)

All 13 are killed by their named checks, and golden and restored pass in every slice (`receipts/retained-mutants-s{1,2,3}.txt`). The runner copies only sources into a temporary tree, and a compile failure never counts as a kill.

### 3.5 My round-2 mutants (Part B; `receipts/r2-mutants-{1,2,3,4}/results.json`)

| Mutant | Bench | Result |
|---|---|---|
| `r2-fchg-code-compare-only` / `r2-fchg-bridge-compare-only` | GI, srp_stream_fsms, srp_top | KILLED by srp_stream_fsms L3 (GI and srp_top change both fields) |
| `r2-fchg-lowest-candidate-only` (only the compared sink strobed) | GI, srp_stream_fsms | KILLED by L9 (shared stream) |
| `r2-fchg-candidate-includes-mt` | GI, srp_stream_fsms | SURVIVED. Equivalent at the response level: settle and teardown zero `rtype_r`, so an MT sink is excluded by type as well. The only divergence is an extra change strobe on the same cycle as a fresh REGISTERED strobe, and both OR into one notify term. Not a finding. |
| `r2-fail-code-ungated` | GI, srp_stream_fsms, srp_top | KILLED in all three |
| `r2-bridge-gate-other-sink` | GI | KILLED, DISTINCT-1 bridge |
| `r2-internal-req-leaks` | GI | KILLED, internal-seam counter |
| `r2-status-view-stale-on-write` | GI | KILLED |
| `r2-strt-chg-trigger-dropped-at-top` | GI | KILLED, REBIND-SW |
| `r2-desc-type-ignored` (STREAM_OUTPUT intercepted) | full pp_top | KILLED, G2 STREAM_OUTPUT[1] byte-exact |
| `r2-internal-honours-external-wait` | GI | SURVIVED, see S1 |
| `r2-index-guard-off-by-one` | GI | SURVIVED, see S2 |
| `r2-strt-chg-bound-before-removed` | GI, acmp_listener | SURVIVED, see S3 |

### 3.6 My own behaviour probes (`scripts/probe_q.py`; `receipts/probe-q-head.log`, `receipts/probe-q-basehybrid.log`)

**Q1: re-bind variants from a SETTLED sink.** Each row gives the unsolicited count, the value it carries, and the solicited read that agrees with it.

| Step | Result |
|---|---|
| same talker, STREAMING_WAIT on (A6 short-circuit) | 1 (COMPLETED, SW=1) |
| repeat | 0 |
| same talker, SW off | 1 (SW=0) |
| another talker, SW on | 1 (ACTIVE, SW=1: the pbsta and started changes coalesce into one frame) |
| another talker, SW kept | 0 |
| another talker, SW off | 1 (ACTIVE/0, SW=0: the started pulse alone) |
| unbind | 1 (DISABLED) |

Exactly one frame appears whenever a visible field changes, and none otherwise.

**Q2: two sinks settled on the same stream.** A fresh Failed gives 1 per sink (code 7, full bridge), and the Listener New is declared. A changed code and bridge give 1 per sink with the new values and 0 Listener New in 600 ms. A bridge-only change gives 1 per sink and 0 New. An unchanged refresh gives 0. This exercises the one-comparator design at the response level.

**Q3: the stated residual.** A latency-only Advertise refresh gives 0 unsolicited at head. The base RTL under the same bench also gives 0. So the residual predates this PR. It is tracked as issue #113 ("A latency-only Talker refresh updates GET_STREAM_INFO without an unsolicited notification"). I accept it as outside this PR's scope.

**Q4:** see S2.

The patched GI phase still passes 501/0 at head. On the base hybrid it fails the GI checks, as expected: base asks the integrator for selectors 5 and 7.

### 3.7 Area and timing (published Vivado OOC reports, `author-r2/area`)

The `util.rpt` totals I extracted match `syn/ooc/README.md`:

| Shape | Base LUT / FF | Head LUT / FF | Delta | Round-1 delta |
|---|---|---|---|---|
| 8x8 | 28,092 / 30,354 | 28,326 / 31,064 | +234 / +710 | +640 / +784 |
| 1x1 | 20,978 / 23,446 | 21,245 / 23,674 | +267 / +228 | +185 / +299 |

- BRAM is unchanged: 24 at 8x8, 16.5 at 1x1.
- The top's own registers fall by 81 against round 1, which matches the removed sample.
- The new paths meet the 10 ns clock: into the gather-answer register +4.831 ns, from the bridge latch +5.968 ns (`cand-8x8-paths`).
- The worst post-synthesis path is the same pre-existing `u_notify/ctr_pend_r → u_event_router/sel_r CE` path in base and head. It is −9.524 ns in base and −10.089 ns in head (33 and 35 logic levels).
- The recipe is documented as area-only. That path's violation predates this PR and is not attributable to it with the evidence available.
- The remaining FF are the owned state kept alive by the new readers: the bridge latch, the decoder capture, and the 8-bit view per sink. That is consistent with my round-1 attribution.

## 4. Prior public review findings (read after my independent pass)

My own verdict and ledger were settled before I opened the other reviewer's round-1 report. The file write of that draft failed on a precondition in the same step in which that report was opened, so the draft was not on disk first. The verdict and ledger below are unchanged from that draft. The concurrent round-2 report of the other reviewer was not read.

| Finding | At this head | Evidence |
|---|---|---|
| R294-1-F1 MAJOR (changed FailureInformation re-declares the Listener with New) | **RESOLVED** | The separate `evt_tk_fail_chg_o` (`KL_srp_listener_fsm.sv:464-480,735`) feeds only `stri_events` (`protocol_processor_top.sv:3141`). It has no router or ACMP consumer (grep), and `ind_reg_w` is back to fresh registration or type swap. P1 and P2 pass. Unit L2 and srp_top D check it, GI checks the wire, and the retained `failure-change-redeclares` mutant is killed. 10 §6.4 and F10.5 document it. |
| R294-1-S1 (sample untested; prove or drop) | **RESOLVED (dropped)** | Owners are read live; F06.13 states the bound; −81 FF at 8x8. |
| R294-1-S2 (index guard untested) | **RESOLVED** | GI INDEX-GUARD; the retained and my two guard mutants are killed. The boundary is left as S2 here. |
| R294-1-S3 (OOC shape argument; decoder copy) | **RESOLVED / not taken** | `protocol_processor_ooc.tcl` takes a shape; the 1x1 numbers are recorded. The decoder copy is declared out of scope in the PR body. |
| R295-1-F1 MAJOR (a rebind from ACTIVE/0 no longer notifies started/stopped) | **RESOLVED** | The `bind_act_r` exclusion is removed (`KL_pp_acmp_listener.sv:1418-1422`). GI REBIND-SW, unit RV8b/d, and the retained `rebind-started-trigger-removed` mutant is killed. Probe Q1 covers the other re-bind paths. The listener comment, the top comment and 06 §7 are corrected. |
| R295-1-F2 MINOR (same defect as R294-1-F1) | **RESOLVED** | as R294-1-F1 |
| R295-1-F3 MINOR (sample area-bearing and untested) | **RESOLVED (removed by manager decision)** | as R294-1-S1 |
| R295-1-S1 (index-guard test) | **RESOLVED** | as R294-1-S2 |
| R295-1-S2 (gate once, compare on the hit sink) | **RESOLVED** | `protocol_processor_top.sv:3099-3104`, `KL_srp_listener_fsm.sv:464-480`; SRP listener −353 LUT at 8x8 against round 1 |
| R295-1-S3 (Linux-only affinity) | **RESOLVED** | `tb/pp_top/gsi_mutants.py` guards the calls with `hasattr` |
| R295-1-S4 (`dbg_recwr` functional) | **RESOLVED** | documented as functional at `KL_pp_acmp_listener.sv:230-235` |

There are no review submissions or inline comments on PR #111.

## 5. Lens results (each with its own artifacts)

- **Conformance: CLEAN.**
  - Field lineage:
    - failure code: SRP `fcode_r`, gated to FAILED (`KL_srp_listener_fsm.sv:849`), then the selector-4 byte (`:3112`), then response byte 72;
    - bridge: the raw `fsysid_r`, gated once on the addressed sink's FAILED after the index mux (`:3101`), then selector 5, then bytes 74 to 81;
    - `{pbsta, acmpsta}`: the listener record write bus (one writer), then `lstn_gsi_status_r`, then selector 7, then byte 90.
  - Table 5.22 input triggers: the committed status compare, the started/stopped pulse under a live binding, SRP registration and unregistration, and the FailureInformation change (`:3132-3142`). Probes Q1 and Q2 show one frame per visible change and none otherwise.
  - The only stated residual (latency) predates this PR and is tracked in #113.
  - No MSRP side effect: P2 and Q2.
  - Every acceptance row is covered by GI at head.
- **RTL: CLEAN.**
  - The single-comparator invariant holds. Hits need an armed sink with the exact triple, settle and teardown reset the registrar and zero its latch, and every registered candidate sees identical events (`KL_srp_listener_fsm.sv:405-410,722-765`).
  - The listener pulse and the status compare both register off the X_WB write (`KL_pp_acmp_listener.sv:738-739,1418`, `protocol_processor_top.sv:3061-3074`), so they land in the same cycle.
  - Only GET_STREAM_INFO uses selectors 4, 5 and 7 (`gen_ucode.py:1044-1051`); the other kind-0 gathers use 1, 3 and 15.
  - Scoped lint is clean at 1x1 and 8x8. The area figures are verified.
- **Robustness: CLEAN.**
  - The missing-descriptor zero body (retained mutant killed), and reset over erased NVM.
  - The index guard is on the full index, including the boundary (Q4).
  - The live reads hold no stale state, so the old sample-leak class is gone.
  - The coherence bound depends on the pending-clear at selection (`KL_aecp_notify.sv:758,987`), which I verified.
  - The wait mask is correct under an idle-HOLD integrator (probe W). S1 is a test gap, not a defect.
- **Tests: CLEAN (S1 to S3 are suggestions).**
  - GI covers 488 checks, including REBIND-SW, FAILED-REFRESH wire, INDEX-GUARD and two sinks.
  - Unit sections cover srp_stream_fsms L1-L9, srp_top D and acmp_listener RV8.
  - 13 of 13 retained mutants are killed, and I re-ran them.
  - I ran 18 reviewer mutants: 1 round-1 mutant unchanged, plus 17 of my own or re-expressed. 14 are killed, 1 is equivalent, and 3 are suggestion-level survivors.
  - The unit READMEs record the mutations.
- **Docs: CLEAN (S3 and S4 are suggestions).**
  - F02.10 has the internal rows and a new `TK_FAILURE_CHANGE` catalog row marked "NOT routed".
  - F06.13 has the lineage and the coherence bound.
  - 06 §7 states the trigger set once, and §6.2 points to it.
  - 10 §6.4 and F10.5 have the self-transition.
  - The integrator guide §8 is updated.
  - The tb READMEs match the measured counts.
  - The syn/ooc README matches the reports.
  - `make check` passes.

## 6. Hosted evidence at the exact head (inspected; hosted acceptance is the manager's)

The workflow `hdl` ran twice: push run 36014290258 and pull_request run 36014295669, both `success` (`receipts/hosted-runs.txt`). In each, the jobs suites, docs-gates and portability executed and succeeded. The only skipped step is "Build Verilator v5.050", a cache hit and not a gate.

## 7. Reviewer-owned ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #43/#49 acceptance, seam and [A255] decisions; F02.10, F06.13, 06 §6.2/§7, 10 §6.4/F10.5; `stri_events`, SRP registrar, listener X_WB; probes P1, P2, Q1-Q4 (head and base hybrid); issue #113 | R294-2 | a14ef8b4787b5309dd9ab472e82ae2b4a3fdbb72 |
| RTL | CLEAN | full HDL diff 939c143..a14ef8b; `KL_aecp_notify` intake and clear; `gen_ucode` selector use; scoped lint (10 elaborations incl. 1x1/8x8); published Vivado util/timing reports | R294-2 | a14ef8b4787b5309dd9ab472e82ae2b4a3fdbb72 |
| Robustness | CLEAN | missing descriptor, reset, index guard and boundary (Q4), live-read bound versus notify pending-clear, idle-HOLD integrator (probe W), single-comparator invariant | R294-2 | a14ef8b4787b5309dd9ab472e82ae2b4a3fdbb72 |
| Tests | CLEAN (S1-S3) | `gsi_internal.hpp`, sim_main harness, `gsi_mutants.py` (13/13 re-run), srp_stream_fsms L, srp_top D, acmp_listener RV8; six suites re-run; 18 reviewer mutants (1 round-1 unchanged, 17 own or re-expressed) | R294-2 | a14ef8b4787b5309dd9ab472e82ae2b4a3fdbb72 |
| Docs | CLEAN (S3, S4) | 02, 06, 10 architecture diffs; integrator guide §8; tb READMEs (pp_top, srp_stream_fsms, srp_top, acmp_listener); syn/ooc README and tcl; in-RTL comments; `make check`, `gen_matrix --check` | R294-2 | a14ef8b4787b5309dd9ab472e82ae2b4a3fdbb72 |

## 8. Real limits

- **Banks.** I did not run the full processor banks (`run_suites.sh`, `lint_hdl.sh`, yosys portability), any parent or gPTP bank, the builder, Vivado, or any container job. For those I rely on the manager's exact-head source validation, the published evidence and the hosted runs.
- **Shape coverage.** Response-level tests run only at the 8-sink shape. 1x1 is covered here only by lint elaboration and by the published synthesis.
- **Area and timing.** These are post-synthesis OOC estimates, not routed timing or hardware qualification.
- **Specification text.** The PDFs are not in the repository; conformance rests on the clauses as the repository cites them.
- **Other reviewer's probes.** Its round-1 probes and mutant were not run by me (see §3.3).
- **Diff check.** `git diff --check` was run on the clone. Its rc 0 is recorded here, not as a separate receipt.
- **Build logs.** Build logs stay in the packet but are not in the manifest. They contain local paths and no verdict content.
- **Physical calibration NOT RUN.** Field skips are not hardware proof.

## 9. Pending manager duties

- The parent consumer gates, with this head as the processor gitlink at the new parent dev, are manager receipts. I did not re-run them.
- The final current-dev candidate at the merge turn: source base `939c143`, live dev `59b816708852472da6ed4576386c30ebd5f8f839`.
- Hosted and act acceptance.
- Parent #508 adoption: the integrator gather for input selectors 5 and 7 becomes unused. The integrator's MSRP_FAILURE_VALID and other validity flags must stay coherent with `srp_tk_reg_state`, and the selector-4 destination MAC is still the integrator's.
- Issue #113 (latency-only refresh) stays open, as stated.
- Merge still requires the second independent positive review.

## 10. Reproduction

Every script takes an extracted tree (`git archive`) and never touches a checkout. The pinned simulator is reached through `scripts/verilator8`, which appends `-j 8`.

| Script | Purpose |
|---|---|
| `scripts/probe_srp_redeclare.sh <tree> <log>` | P1 (unchanged from round 1) |
| `scripts/probe_top_redeclare.sh <tree> <log>` | P2 (unchanged) |
| `scripts/extra_mutants.py <tree> <scratch> <out> <verilator>` | round-1 mutants (unchanged) |
| `scripts/r2_mutants.py <tree> <scratch> <out> <verilator> [names]` | round-1 list byte for byte, plus own mutants |
| `scripts/run_retained_slice.py <tree> <start> <stop> <out> <verilator>` | the PR's retained runner, unchanged, by slice |
| `scripts/probe_q.py <tree> [--base-hybrid]` | Q1-Q4, then `make gsi-build` and `--gsi-internal-only` |
| `scripts/probe_idle_wait.sh <tree> <log> [mutate]` | probe W |
| `scripts/scoped_lint.sh <tree>` | scoped lint |
| `scripts/clone_integrity.sh <clone> <head> <tree>` | integrity |

After all probes, the review clone was verified identical to the exact head (`receipts/clone-integrity.txt`):

- HEAD `a14ef8b`; tree and index write-tree `71081cc`.
- The worktree is clean, with no modified, untracked or ignored files.
- All 240 tracked entries re-hash to their blob and mode.
- The repository has no gitlinks (mode 160000 count 0), so there are none to verify.

R294-2 FINISHED
