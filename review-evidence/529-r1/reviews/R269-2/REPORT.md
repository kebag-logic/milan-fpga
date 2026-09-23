[R269] NEGATIVE - exact head 535701a06128d54c7f0f161e1c061fa02d4d1342

Round R269-2. External cleared-context re-review of issue #529 / PR #534, correction round 1.

- Base `ede8d48ecd7c7f589a14b957951f040d92c99c70`.
- Head `535701a06128d54c7f0f161e1c061fa02d4d1342`, tree `8c62c1a118b6bdacc0cf9b39d2cbdc633717630f`.
- Gitlinks, unchanged from base:
  - protocol-processor `424c688fa2205b934a7689a58f2aa766420f2326`;
  - gptp-processor `c1b617435824929a790739ea8585c3fe1a328cc0`;
  - third_party/verilog-axis `48ff7a7e2ef782cf778d47910cf85835c64b1bce`.
- History: six one-line commits with no trailers, linear on the base.
  - The correction round is `a51d5164` (harness) and `535701a0` (docs), on `f8155775`.
  - `git diff f8155775..HEAD -- hdl` is empty.

## Summary

- **The RTL is correct at this head.**
  - All ten `KL_crf_rx` Table 5.16 outputs are bound to the root wires REGISTER_MAP names.
  - The row serves them at their IEEE Table 7-157 quadlets under `0xF3F`, which is Milan v1.2 Table 5.16 exactly.
  - The dirty pulse reaches the processor as {STREAM_INPUT, `N_STREAMS`}.
- **The correction round fixes what it was asked to fix.**
  - R269-1 F1 = R268-1 F1 (permuted bindings) is resolved. I built my own generator, independently of the author's. All 45 pairwise exchanges at the instance turn both of their own quadlets red, on nxn and on nxn8. Two rotations do the same.
  - R268-1 F2 (stuck push) and F3 (stale opening status) are resolved.
  - The signature-arm overclaim is gone.
- **One new MINOR finding, F1 (Tests, Docs).** Criterion 3's evidence paragraph still claims more than its checks prove.
  - It says the bind edge reaches the arbiter "as {STREAM_INPUT, `N_STREAMS`} and as nothing else".
  - The check compares only the STREAM_INPUT bitmap.
  - Two mutants that also raise a second descriptor survive on nxn, nxn8 and notify.
  - A one-line stronger check passes at head on all four broad legs and kills both.
- **Six SUGGESTIONs (S1-S6).** They do not affect lens coverage.
- **Verdict NEGATIVE.** F1 is open under Tests and Docs. Conformance, RTL and Robustness are covered clean at this head.

## Reconstruction

These were read in order, before any other reviewer's material:

1. AGENTS.md, CONTRIBUTING.md and docs/README.md.
2. Issue #529:
   - the body;
   - the A10 assignments (A204, and A216 for this correction round);
   - the A204 TAKEN and REVIEW READY comments;
   - the A216 REVIEW READY comment.
3. The frozen acceptance: REGISTER_MAP closure criteria 1-4 at base `ede8d48e`.
4. The authorities, from the standards texts:
   - Milan v1.2 5.3.8.10 (Table 5.6 and its reset sentences) and 5.4.2.25 (Table 5.16);
   - IEEE 1722.1-2021 7.4.42.2 (Tables 7-156 and 7-157).
   - Receipt `05` holds the derived mapping.
5. The interfaces:
   - the `KL_crf_rx` port list and engine;
   - the GET_COUNTERS gather face and the Table 5.22 arbiter in `milan_datapath.sv`;
   - `KL_aecp_notify.sv:437-447` (STREAM_INPUT index < `N_STREAM_IN_P` = `ACMP_SINKS_C`).
6. `git diff ede8d48e..535701a0`, per commit.
7. Public executable evidence:
   - the author's packet `review-evidence/529-r1/correction-a216` at `9f799fe0`, read for MUTATION-RESULTS.md only;
   - the exact-head hosted check runs.
8. Prior public review findings (R269-1, R268-1). They were read after my independent pass over the diff and after my own mutation campaign. See "Prior public findings".

## Finding

### F1 - MINOR - Tests, Docs

```text
[R269] MINOR Tests, Docs - docs/reference/REGISTER_MAP.md:897-903; tb/verilator/milan_dp/README.md:513-514,524-526; tb/verilator/milan_dp/sim_nxn.cpp:3464-3472,1315-1325 - criterion 3's evidence claims more than its checks prove
```

**Requirement and evidence**

- AGENTS.md section 6 asks two things:
  - Tests: "Each new test can fail for the defect it claims to detect".
  - Docs: the PR must carry enough evidence for a cold reviewer.
- The A10 assignment for this round asks for docs claims "narrowed to what the tests prove".
- **The arbiter claim.**
  - REGISTER_MAP.md:898-899 says the bind edge reaches the arbiter "as {STREAM_INPUT, `N_STREAMS`} and as nothing else".
  - README.md:513-514 says the same with "alone". The harness comment at sim_nxn.cpp:3464-3467 says it too.
  - The check at sim_nxn.cpp:3469-3472 clears and compares only `pp_ctr_evt_sin_seen`. It never looks at the STREAM_OUTPUT, AVB_INTERFACE or CLOCK_DOMAIN observers, which the harness already keeps (sim_nxn.cpp:563-566).
- **Surviving mutants.** Two reviewer mutants add a second tuple and keep the CRF row's own one (receipts `mutants/ve-also-*.diff`):
  - `ve-also-ckd`: the CRF pulse also raises CLOCK_DOMAIN 0.
  - `ve-also-sout`: the CRF pulse also raises STREAM_OUTPUT `N_STREAMS`.
  - Both survive with 0 failures at nxn 1705, nxn8 3133 and notify 145 (`digests/mut/ve-also-*`).
- **A stronger check is feasible.** The probe adds one line: after the bind edge, none of the three other observers is set (receipt `33-h-nothing-else.harness.diff`).
  - It passes at head on nxn 1706/0, nxndv 1708/0, nxn8 3134/0 and nxn4c 1706/0.
  - It kills both mutants on nxn and on nxn8 (`digests/probe-nothing-else/`).
- **The same paragraph also overclaims the notification.**
  - REGISTER_MAP.md:900-901 and README.md:524-526 say the push reaches both controllers "byte-identical from the body on to the solicited answer".
  - `[NOTIFY-CRF]` compares only B's copy (sim_nxn.cpp:1315-1325). A's copy is only counted.
- The wording predates this round (it is present at `f8155775`). It survived a round whose stated scope was this class of claim.

**Impact**

- The register map is the stable-ABI authority, and it states a guarantee the gate does not provide.
- Suppose the arbiter wiring regressed so that a CRF counter change also raised another descriptor. Every controller would then get unsolicited GET_COUNTERS for a descriptor whose counters did not change. The gates named as criterion 3's evidence would stay green.
- The RTL at this head does not do that. The defect is in the evidence statement, not the product.

**Required outcome**

- Every sentence in criterion 3's evidence, the README paragraph and the harness comment is true of the checks that run. Either of these is enough:
  - strengthen the checks, for example the one-line observer check above, and compare A's copy too; or
  - narrow the wording to "as no other STREAM_INPUT index" and "B's copy byte-identical".

**Verification**

- Rebuild nxn and nxn8 against `ve-also-ckd` and `ve-also-sout` with `scripts/mutants.py` and `scripts/campaign.sh`.
  - If the check is strengthened, each must turn a named check red.
  - If the wording is narrowed, re-read REGISTER_MAP.md:897-903, README.md:510-530 and sim_nxn.cpp:3464-3472 against the check.
- The unmutated head stays green on every broad leg and on notify.
- Rerun `docs_check.py` and `check_em_dash.py --base ede8d48e`.

## Suggestions

These do not affect coverage.

- **S1 - Robustness, Tests (retained: R269-1 S1 = R268-1 S2). No leg exercises `crf_sink: false`.**
  - No tracked config disables the sink, so `g_ctr_no_crf_dirty` and the constant-false `ctr_crf_w` are never run.
  - My builder-generated 4x4 no-sink shape (4 sinks, 5 sources) lint-elaborates with 0 errors (receipts `50-*`).
  - The harness C++ cannot build against it: the simulator drops the unread CRF tally wires the harness names.
- **S2 - Tests (retained: R269-1 S2). The release floor is still 990 ms.**
  - `sim_nxn.cpp:1345` checks `>= 990 ms`. The section header at `:1062` says "RELEASED after >= 1000 ms".
  - Measured: 997 ms on the stamp.
- **S3 - Docs (retained: R269-1 S3). Config comments still point at B4.**
  - `configs/endstation_arty_4x4.yaml:103`, `endstation_arty_8ch.yaml:139` and `endstation_ax7101_8x8.yaml:153` still say runtime gaps are graded in "the current audit B3 and B4". B4 is closed.
- **S4 - Tests (retained: R268-1 S1). The round-robin resume offset survives.**
  - My `vd-rr-sout` resumes at the output just served instead of the next one. It stays green on nxn and notify.
  - It only matters when that output re-pulses on the very next cycle, so it is equivalent in practice. The no-starvation property is still ungraded.
- **S5 - Tests, Docs (new). The event arm's silence constants are mirrored literals.**
  - `kCrfSilenceCyc = 10000000` and `kFabricMsCyc = 100000` (sim_nxn.cpp:3607-3608) restate `CLK_FREQ_HZ_P / 10` and `MILAN_CLK_FREQ_HZ / 1000`.
  - A leg at another fabric clock fails closed: the unlock would not land in the window. So this is not a false-green risk.
  - Passing them from the recipe, the way `MS_CYC_TB` already is, would keep them from drifting.
- **S6 - Docs (new, manager-owned text). The PR body contradicts itself about closing #529.**
  - PR body "Known limitations" says "`Relates to #529 (...)` closes the issue at merge".
  - GitHub records no closing reference for PR #534 (receipt `60-pr-linkage.json`). #529 stays open, as the Linked Issue section says.
  - The sentence looks like a replacement artefact and should be reworded.

## Prior public findings

| Prior item | Disposition at this head | Evidence |
|---|---|---|
| R269-1 F1 MAJOR (Conformance, Tests, Docs): permuted `KL_crf_rx` binding undetectable | **RESOLVED** | See the four sub-rows below. |
| - the event arm | | New arm at sim_nxn.cpp:3578-3624. Real PDUs and the engine's timeout move the ten to 2, 1, 3, 4, 5, 6, 7, 8, 9 and 21. |
| - the 45 exchanges | | My independently generated exchanges are byte-identical to the author's 45 (receipt `21`). Each is red at both of its own quadlets in the event arm, on nxn and on nxn8: 90 of 90 runs (receipt `20`). |
| - mx1-mx4 | | mx1-mx4 are my `vx-mr_cnt-tu_cnt`, `vx-cnt_locked-cnt_unlocked`, `vx-late_cnt-early_cnt` and `vx-cnt_locked-cnt_intr`. All red on both legs. |
| - docs overclaim | | The signature arm is now described as grading the gather mux only (REGISTER_MAP.md:879-882, README.md:509-510, sim_nxn.cpp:3424-3428). |
| R268-1 F1 MINOR (same defect) | **RESOLVED** | p1, p2 and p3 are the same exchanges as mx2, mx3 and mx1. p4 = `vx-cnt_locked-cnt_intr` and p5 = `vx-fmt_err-late_cnt`. All red on nxn and nxn8. |
| R268-1 F2 MINOR: `[NOTIFY-CRF]` cannot fail for a row that keeps pushing | **RESOLVED** | See the two sub-rows below. |
| - the new checks | | New quiet checks at sim_nxn.cpp:1346-1353. |
| - the stuck-pending mutant | | My `vd-clear-stuck` (the same edit as R268 `r3`) is red on notify: 4 pushes against 2, to B and to A. The head passes 145/0 with the CRF row pushed 997 ms apart. |
| R268-1 F3 MINOR: REGISTER_MAP opening status lists the CRF bank as a gap | **RESOLVED** | REGISTER_MAP.md:31-35 now says it is served and pushed since #529. |
| R269-1 S1 / R268-1 S2: `crf_sink: false` unexercised | RETAINED (S1) | Receipts `50-*`. |
| R269-1 S2: 990 ms floor | RETAINED (S2) | sim_nxn.cpp:1345 against :1062. |
| R269-1 S3: config comments cite B3 and B4 | RETAINED (S3) | The three yaml lines are unchanged. |
| R269-1 S4: frozen criteria paraphrased | **RESOLVED** | REGISTER_MAP.md:876-913 quotes criteria 1-4. I compared each quote with base `ede8d48e` and they are word for word. |
| R269-1 S5 / R268-1 S3: `Closes #529` with the silicon item open | **RESOLVED** | The PR now says "Relates to #529", with no closing reference (receipt `60`). S6 covers a leftover sentence. |
| R268-1 S1: round-robin no-starvation ungraded | RETAINED (S4) | `vd-rr-sout` survives. |

The author's disclosure is already an open Issue: #541 covers the `KL_crf_rx` banner and the `CRF_CTRL` row saying a validation error unlocks the sink. The event arm does not depend on either reading, because its rejected PDUs come before the first lock.

## Focus items

**Every one of the ten bindings is discriminated.**

- The event arm starts a fresh era: the lever drops, then rises, which wipes all ten.
- One PDU is injected per 400 cycles, against the leg's 256-cycle observation interval. So each interval counter moves once per PDU.
- I traced the plan by hand through `KL_crf_rx.sv:343-549`. It gives:
  - MEDIA_LOCKED 2 (locks at P13 and P21);
  - MEDIA_UNLOCKED 1 (the silence);
  - STREAM_INTERRUPTED 3 (gaps of 2, 3 and 2);
  - SEQ_NUM_MISMATCH 4 (those three plus a gap of 1);
  - MEDIA_RESET 5 (P6-P10 toggle; P14 re-seeds after the silence);
  - TIMESTAMP_UNCERTAIN 6 (P14-P19);
  - UNSUPPORTED_FORMAT 7;
  - LATE 8 (P1-P8);
  - EARLY 9 (P9-P17);
  - FRAMES_RX 21.
- The run matches the trace exactly, on all four broad legs.
- No two counts are equal, and a `static_assert` enforces that. So any exchange is two wrong quadlets.
- The campaign agrees:
  - 45/45 exchanges red at their own quadlets on nxn and on nxn8;
  - both rotations red;
  - quadlet-level mutants red: level for count, duplicate, 9/10 exchange, 16-bit slice, zero-tied, row removed.

**The `[NOTIFY-CRF]` timed check.**

- At head, on notify: pushed to A and B; SUCCESS, cdl 148, `0xF3F`; B's copy byte-identical to the solicited answer; withheld at 900 ms; released once; 997 ms apart; then no third push in 2 s, to B or to A.
- `vd-clear-stuck` is red at exactly the two quiet checks.
- `vd-nodirty` and `vd-to-idx0` are red at all 10 checks.

**Docs claim only what the tests prove, except F1.**

- These claims were checked against runs:
  - "every `[CTRS-CRF]` check runs on the 4x4, divergent 4x4, 8x8 and shipping Arty 4x4 legs": 72 on each (receipt `11`);
  - the criterion 2 statements;
  - the mutation list in criterion 4 and the README: row removed, quadlets permuted, 16-bit slice, tv pair claimed, dirty removed, CRF row for AAF, AAF guard for CRF, one tally unwired, pending never cleared. Each is red with my own mutant.
  - the 45 exchanges on the 4x4 and 8x8 legs.
- Also accurate: the compliance matrix row 5.4.2.25 and 5.4.5.1/.2, audit B4, FR_NFR, the roadmap, the builder page, REGISTER_MAP_CLASSES and the CHANGELOG.
- The CHANGELOG's +1,134-cell figure is the author's round-0 synthesis. It was not reproduced.

**The harness shortcut is acceptable.**

- What it does:
  - `sim_nxn.cpp:3609` writes the engine's own `tout_r` to 1 ms (100,000 cycles) short of its 10,000,000-cycle limit.
  - The last millisecond, plus 10 %, runs for real.
  - No Table 5.6 tally and no root wire is written.
- Probes:
  - Replacing the write with the real 100 ms gives the same 1705/0 on nxn, in 38 s instead of 6 s (receipt `30-h-realsilence.harness.diff`, `digests/base/31-*`).
  - Deleting only the write turns 4 checks red, both unlock checks included (`digests/base/32-*`). The arm cannot pass without the engine's own unlock.
- Why it is sound:
  - During the skipped time, no PDU arrives and every interval flag is clear, so nothing observable is skipped.
  - A leg at another fabric clock fails closed (S5).
  - Every exchange involving MEDIA_UNLOCKED is red on both legs.

## Clean-lens evidence

```text
[R269] PASS Conformance - hdl/milan/milan_datapath.sv:3511-3552,5467-5500,7206-7301; receipts 05, 11, 60; Milan v1.2 5.3.8.10 Table 5.6, 5.4.2.25 Table 5.16; IEEE 1722.1-2021 Tables 7-156/7-157; frozen criteria at ede8d48e - mask, offsets, wrap, era reset, Table 5.22 limit, NO_SUCH_DESCRIPTOR, each frozen criterion
[R269] PASS RTL - hdl/milan/milan_datapath.sv:1785-1796,3312-3314,3327-3352,3511-3552,5431-5501,7184-7301; hdl/ieee1722/crf/KL_crf_rx.sv (receipt 12, token-equal to base); receipts 40, 50 - clock/reset, widths, mux priority, guard, arbiter arithmetic, both shape branches
[R269] PASS Robustness - milan_datapath.sv:3524-3526,3547-3552,7230-7301; KL_crf_rx.sv:429-468,480-506,559-610; receipts 20 (vg-*, vd-*), 50, digests/base/31-32 - malformed input, bounds, wrap, era reset, repeated pulses, config-dependent shape
```

**Conformance.**

- `0xF3F` is the sum of the Table 5.16 bit values.
- Quadlets 0-5 and 8-11 are the Table 7-157 offsets. TIMESTAMP_VALID and TIMESTAMP_NOT_VALID read zero, unclaimed.
- 32-bit wrap: at the root through real PDUs for FRAMES_RX and STREAM_INTERRUPTED. All seven engine tallies are plain `+32'd1`.
- Reset on not-bound to bound: the bind-edge wipe, checked from signatures to zero.
- No reset on unbind: `KL_crf_rx.sv:559` keys the wipe on the rising edge only.
- `en_i` follows descriptor N's own bind state: `acmpl1_bound = acmpl_bound_v_w[CRF_SNK_IDX_C]` (milan_datapath.sv:5000-5003).
- Table 5.22: at most once per second, then quiet, on the timed leg.
- Undeclared N+1: NO_SUCH_DESCRIPTOR with the empty body.
- Frozen criteria 1-4 are met at the root. The silicon acceptance item is post-merge by the A10 decision, and #529 stays open for it.

**RTL.**

- Clock and reset: one domain (`axis_clk`), no new crossing. The new state is the widened pending vector, reset to `'0` at :7278.
- Widths:
  - `32'(ctrq_index_r) == CRF_SNK_IDX_C` is a full 16-bit exact compare, with no aliasing;
  - `{crf_dirty_p_w, avtprx_dirty_p_w}` is `PP_CTR_SIN_N_C` wide;
  - the round-robin width follows `PP_CTR_EVT_N_C`.
- Mux: the CRF arm is disjoint from the AAF arm (`<` against `==` on N). `vg-no-type`, `vg-sin-le` and `vg-crf-first-noidx` are red.
- Arbiter index arithmetic: `vd-sout-off` and `vd-avb-pick` are red through existing `[CTRS-OUT]` / `[CTRS2]` / `[NOTIFY]` checks.
- The processor accepts index < `ACMP_SINKS_C`.
- `KL_crf_rx` is comment-only against base.
- Lint: `lint_rtl.py --check` 90 <= 90. `check_port_contracts`, `check_sv_idiom` and `check_cpp_idiom` pass (receipt 40).
- The no-sink shape lint-elaborates clean (receipt 50).

**Robustness.**

- Malformed PDUs: 7 rejects are counted as UNSUPPORTED_FORMAT only.
- Minimum and maximum:
  - from reset, all ten read 0;
  - wrap from 0xFFFFFFFF;
  - the 16-bit index cannot alias.
- Ordering: gaps of 1 and of 2 or more; the era wipe clears the interval flags.
- Reset during activity: the bind edge overrides a same-cycle timeout (`KL_crf_rx.sv:606`, engine unchanged).
- Repeated pulses: a re-pulse while pending is absorbed. The release clears the pending bit and the row goes quiet.
- Reads have no side effects: the row is a pure mux.
- Feature-disabled: an unbound sink does not count; the no-sink shape elaborates (S1 notes it is not run).

**Unclean lenses.** Everything else examined under them was clean.

- Tests (F1):
  - the event arm, wrap arm, signature arm, isolation and reset checks;
  - `[NOTIFY-CRF]`;
  - 68 generated mutants (67 plus a marked control), 123 mutant runs and 4 baseline legs;
  - harness probes h-realsilence, h-nopoke and h-nothing-else.
- Docs (F1):
  - CHANGELOG.md; REGISTER_MAP.md:31-35, 136-142, 841-913; REGISTER_MAP_CLASSES.md;
  - MILAN_COMPLIANCE_MATRIX.md; FR_NFR.md; the roadmap; ENDSTATION_BUILDER.md; audit B4 and item 7;
  - the milan_dp README; the `KL_crf_rx` and `milan_datapath` comments;
  - `scripts/port_docs.budget`;
  - receipt 40 docs gates.

## Ledger (reviewer-owned)

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Milan v1.2 5.3.8.10/Table 5.6, 5.4.2.25/Table 5.16; IEEE 1722.1-2021 Tables 7-156/7-157; `milan_datapath.sv:3511-3552,5467-5500,7206-7301`; `KL_aecp_notify.sv:437-447`; frozen criteria at `ede8d48e`; receipts 05, 11, 60 | R269-2 | 535701a06128d54c7f0f161e1c061fa02d4d1342 |
| RTL | CLEAN | `milan_datapath.sv:1785-1796,3312-3352,3511-3552,5431-5501,7184-7301`; `KL_crf_rx.sv` (receipt 12); receipts 40, 50 | R269-2 | 535701a06128d54c7f0f161e1c061fa02d4d1342 |
| Robustness | CLEAN | `milan_datapath.sv:3524-3552,7230-7301`; `KL_crf_rx.sv:429-610`; receipts 20, 50, digests/base | R269-2 | 535701a06128d54c7f0f161e1c061fa02d4d1342 |
| Tests | UNCLEAN (F1) | `sim_nxn.cpp:1059-1063,1278-1355,3277-3624`; receipts 10-11, 20-22, 30-33, digests (138 runs) | R269-2 | 535701a06128d54c7f0f161e1c061fa02d4d1342 |
| Docs | UNCLEAN (F1) | REGISTER_MAP.md, README.md:502-535, the docs set above, the PR body; receipts 40, 60 | R269-2 | 535701a06128d54c7f0f161e1c061fa02d4d1342 |

## Probes

All probes used the pinned simulator 5.050 (receipt 00).

- At most 8 jobs ran at once, in a disposable copy of the exact head.
- `scripts/leg.py` takes each leg's recipe from the Makefile's own `run` line.
- It overrides only `DP_SRC`, `VERILATOR_JOBS` and the object directory.

| Leg | Head | Reviewer mutants (killed / run) | Notes |
|---|---|---|---|
| nxn (4x4) | 1705/0, 72 `[CTRS-CRF]` | exchanges 45/45; rotations 2/2; row 8/8; guard 4/4; arbiter 4/6; extra-tuple 0/2 | Arbiter survivors: `vd-clear-stuck` (red on notify) and `vd-rr-sout` (S4). Control `vg-ctl-marked` 1705/0. |
| nxn8 (8x8) | 3133/0, 72 | exchanges 45/45; extra-tuple 0/2 | |
| nxndv | 1707/0, 72 | - | |
| nxn4c | 1705/0, 72 | - | |
| notify (timed) | 145/0, 10 `[NOTIFY-CRF]` | arbiter 4/6; extra-tuple 0/2 | Arbiter survivors: `vd-sout-off` (red on nxn) and `vd-rr-sout`. |

Harness probes on nxn:

- real 100 ms silence: 1705/0;
- the shortcut removed with no added time: 4 red;
- the stronger observer check: green on all four broad legs, red for both extra-tuple mutants on nxn and nxn8.

Reviewer-side static probes, in the scratch copy (receipt 40), all exit 0. These are not the manager's bank:

- `check_em_dash --base ede8d48e`: 0 findings over 153 added lines;
- `docs_check`, `check_feature_status`, `gen_toc --check`;
- `check_port_contracts`, `check_sv_idiom`, `check_cpp_idiom`;
- `lint_rtl --check`: 90 <= 90.

Hosted, exact head, read only (receipt 61):

- 22 check runs: 21 success and 1 skipped ("Physical gPTP (nightly and manual)").
- All seven required contexts are success.
- The five Verilator shards and four Yosys shards executed. They are not no-op skips.
- Acceptance of hosted and act evidence belongs to the manager.

## Real limits

- **Not run by this reviewer:**
  - milan_dp obj_dir (main), nolpf, prune, ax1x1, aclk, gptp, gptplat and the render mutants;
  - pp_shadow, milan_dp_render, crf_rx and behave;
  - xvlog, `check_rtl_source_lists`, `gen_module_matrix --check` and the builder bank;
  - Yosys, synthesis and timing;
  - act;
  - hardware.
- **The resource figure is the author's.** No timing evidence exists for the added answer arm.
- **Probe scope.**
  - The shortcut-equivalence run was on nxn only. The other broad legs run the same harness code at the same fabric clock.
  - The no-sink shape was lint-elaborated, not simulated.
  - `vd-rr-sout` is judged near-equivalent by reasoning, not by a stimulus.
- **The host disk filled once during the campaign, from outside this round.**
  - One mutant build failed for lack of space. It was rerun.
  - Every result reported here comes from a completed build and run.
- **Physical calibration NOT RUN.** Field skips are not hardware proof. No silicon or controller verdict exists for this head.
- **The manager's banks were not seen.** The source static/builder and native banks for this head are not seen here, and nothing here infers them.

## Pending manager duties

- Publish the source static/builder and native bank results for this head.
- Accept the hosted and act evidence.
- Build and gate the final current-dev candidate at the merge turn. The source base is `ede8d48e`; live dev is `26d855a9`.
- Re-flash silicon and obtain the la_avdecc Milan-compatible verdict, then close #529. PR #534 does not close it.
- Reword the PR body sentence in S6.
- Re-review F1's fix at a new head.
  - Tests and Docs must be re-covered there.
  - A change to `milan_datapath.sv` would also re-open Conformance, RTL and Robustness.
- Track #541 (the banner / `CRF_CTRL` unlock wording) separately.

## Clone restoration

- No tracked file in the review clone was edited. Every build, mutant and probe ran in a disposable copy under the packet's scratch directory.
- `scripts/verify_clone.py` (receipt 99) confirms, from the bytes on disk:
  - HEAD and tree are the exact ones;
  - the index write-tree equals the HEAD tree, over 868 stage-0 records;
  - there are 0 assume-unchanged or skip-worktree flags;
  - there are 0 tracked blob byte or mode mismatches;
  - there is no untracked or ignored residue;
  - the three required gitlinks are mode 160000 at their pins, with matching checkout HEADs and clean worktrees.

## Reproduce

1. Copy a clean clone at the head, with the three submodules, and generate the suite's hex files (`make -n run` lines 1-4 in `tb/verilator/milan_dp`).
2. `python3 scripts/mutants.py <clone>/hdl/milan/milan_datapath.sv <scratch>/mut`
3. `VERILATOR=<pinned 5.050> scripts/campaign.sh <copy> <scratch>/mut <logs> 8 < list`. Each list line is `<mutant-id|base> <leg>`.
4. `python3 scripts/summarize.py <scratch>/mut <logs> summary.md`, then `python3 scripts/digest.py`.
5. Shape probe: `python3 scripts/nocrf_elab.py <copy> <builder out>/<shape> <obj> <log>`.
6. Harness probes: apply `receipts/30-*.diff` or `receipts/33-*.diff` to a copy and run `scripts/leg.py`.

Full run logs stay with the reviewer. Each digest records its full log's sha256. Every published file is listed in `MANIFEST.sha256`.

R269-2 FINISHED
