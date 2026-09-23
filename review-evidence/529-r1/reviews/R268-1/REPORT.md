[R268] NEGATIVE - exact head f815577559d4922c945dcf1436d4394ff2c10567

Round R268-1: the internal, cleared-context independent review of issue #529 / PR #534.

## Scope

- **Head:** `f815577559d4922c945dcf1436d4394ff2c10567`, tree `39ac12103fecf088ab5d19a494acbc43c2b35367`.
- **Source base:** `ede8d48ecd7c7f589a14b957951f040d92c99c70`. Four commits: `869da89e`, `2a798d19`, `d8340bd5`, `f8155775`.
- **Gitlinks:** unchanged. protocol-processor `424c688f`, gptp-processor `c1b61743`, third_party/verilog-axis `48ff7a7e`.
- **Lenses:** all five (Conformance, RTL, Robustness, Tests, Docs) were applied at this head.
- **Verdict:** NEGATIVE.
  - Three MINOR findings are open (F1, F2, F3).
  - They leave Conformance, Tests and Docs unclean.
  - No BLOCKER or MAJOR was found.
  - The RTL change itself is correct by inspection and by every executed check.

## Reconstruction order

1. AGENTS.md, CONTRIBUTING.md and docs/README.md.
2. Issue #529: the body, the A10 assignment, and the A204 TAKEN and REVIEW READY comments.
3. The frozen acceptance: the base docs/reference/REGISTER_MAP.md section "Closure criteria for the CRF Stream Input counter gap", items 1-4.
4. Authorities, read from the standards text:
   - Milan v1.2 5.3.8.10: Table 5.6 and its reset-on-bind sentence.
   - Milan v1.2 5.4.2.25: Table 5.16.
   - Milan v1.2 5.4.5.2: Table 5.22.
   - IEEE 1722.1-2021 7.4.42.2.4: Tables 7-156 and 7-157.
5. Interface authorities:
   - `KL_crf_rx` ports and banner.
   - The GET_COUNTERS gather face and the Table 5.22 descriptor arbiter in `milan_datapath.sv`.
   - The processor's counter-event map in `KL_aecp_notify.sv` and its descriptor-store miss rule.
6. `git diff ede8d48e..f8155775` and the four commits.
7. Public evidence:
   - The author packet `review-evidence/529-r1/author-a204` at `56531731` (RECEIPTS.md, mutation_receipt.txt).
   - The hosted check runs at the exact head.
8. Prior public review rounds on PR #534. The one prior round, R269-1, was read only after this report's verdict, findings and ledger were written (see "Prior public findings").

## What was verified correct

### Wire format

- **Mask.** `CTR_VALID_CRF_C = 0x00000F3F` (`hdl/milan/milan_datapath.sv:3523`).
  - It equals the sum of the ten bit values in Milan v1.2 Table 5.16: 0x1, 0x2, 0x4, 0x8, 0x10, 0x20, 0x100, 0x200, 0x400 and 0x800.
  - TIMESTAMP_VALID and TIMESTAMP_NOT_VALID are unclaimed and read zero.
- **Quadlet placement.** `ctr_crf_block` (`milan_datapath.sv:3528-3543`) places each counter at its IEEE 1722.1-2021 Table 7-157 offset:
  - @0 MEDIA_LOCKED, @4 MEDIA_UNLOCKED, @8 STREAM_INTERRUPTED, @12 SEQ_NUM_MISMATCH;
  - @16 MEDIA_RESET, @20 TIMESTAMP_UNCERTAIN, @32 UNSUPPORTED_FORMAT;
  - @36 LATE_TIMESTAMP, @40 EARLY_TIMESTAMP, @44 FRAMES_RX.
  - Quadlets 6, 7 and 12-31 answer zero.
- **Ten outputs.** All ten `KL_crf_rx` Table 5.16 outputs are connected (`milan_datapath.sv:5482-5500`).
  - Each wire name matches the engine port's documented meaning.
  - The mux reads each wire at the right quadlet.

### Counter laws

- **Wrap.** All seven engine tallies are plain 32-bit `+ 32'd1` incrementers with no saturation (`hdl/ieee1722/crf/KL_crf_rx.sv:431-439, 466, 487, 527`).
- **Reset on bind.** The en_i rising edge (the ACMP bind or the bench lever) wipes all ten, as Milan 5.3.8.10 requires.
- **Engine unchanged.** `KL_crf_rx.sv` differs from base in comments only. The comment-stripped preprocessor token streams are byte-equal (`receipts/crf_rx_comment_only.txt`).

### Descriptor scope

- **AAF rows unchanged.** `ctr_sin_w` and its block are untouched.
  - The CRF arm is disjoint from the AAF arm: the AAF arm takes index `< N_STREAMS`, the CRF arm `== N_STREAMS`.
- **Undeclared indices.** The descriptor store refuses them with NO_SUCH_DESCRIPTOR and a zero body before the gather face is consulted.
  - So mutant `r1_index_ge` (the CRF row answering every index `>= N`) is equivalent at the wire.
- **Shape without the CRF sink.** A builder-emitted `crf_sink: false` 4x4 shape elaborates cleanly.
  - It gets a 4-bit pending vector; the CRF shape gets a 5-bit one (`receipts/elab_shape_widths.txt`).

### Table 5.22 arbiter

- **Widening.** The STREAM_INPUT row widens by one only when the shape declares the CRF sink (`milan_datapath.sv:7206-7216`).
- **Index arithmetic.** The pick, clear and round-robin steps use the widened base consistently (`milan_datapath.sv:7240-7298`).
- **Processor side.** `KL_aecp_notify.sv:437` accepts STREAM_INPUT indices below `N_STREAM_IN_P`, which equals `ACMP_SINKS_C`. So {STREAM_INPUT, N} lands on a real row.

### Reproduced evidence

The suites below were rebuilt and run at this head with the pinned simulator. Its identity matches the author's record.

| Suite | Result |
|---|---|
| milan_dp obj_nxn | 1687/0, including 54 `[CTRS-CRF]` |
| milan_dp obj_nxndv | 1689/0 |
| milan_dp obj_nxn8 | 3115/0 |
| milan_dp obj_nxn4c | 1687/0 |
| milan_dp obj_notify | 143/0, including 8 `[NOTIFY-CRF]` |
| milan_dp obj_dir | 230/0, 1 guarded as at base |
| pp_shadow | 371/0 |

These gates were rerun and all pass:

- `lint_rtl.py --check` (90 <= 90);
- `check_port_contracts.py`, `check_sv_idiom.py`, `check_cpp_idiom.py`, `check_rtl_source_lists.py`;
- `gen_module_matrix.py --check`;
- `xvlog_gate.py --check` (0 `hdl/` findings);
- `check_em_dash.py --base ede8d48e` (0 findings over 121 added lines);
- `docs_check.py`.

The author's eight mutants all reproduce red, with the counts published in `RECEIPTS.md` (`receipts/mutants_author.txt`). The marked positive control passes at 1687/0 and 143/0.

## Findings

### F1 - MINOR - Conformance, Tests, Docs - seven of the ten root bindings are not discriminated by any check

- **Where.**
  - The seeding helper: `tb/verilator/milan_dp/sim_nxn.cpp:3315-3329` (`crf_tally`).
  - The check that uses it: `sim_nxn.cpp:3409-3422`.
  - The port map this change creates: `hdl/milan/milan_datapath.sv:5483-5496`.
  - The closure claim: `docs/reference/REGISTER_MAP.md:871-895`.
- **Authority.**
  - REGISTER_MAP closure criterion 4 asks for root-wire tests of controller decoding.
  - AGENTS.md section 6, Tests: "Each new test can fail for the defect it claims to detect", and "Tests do not merely reproduce implementation assumptions".
  - The harness itself says a permuted quadlet "fails here" (`sim_nxn.cpp:3409-3411`).
- **What the test grades.**
  - The signature arm seeds each tally through the root wire's own name.
  - It then reads the quadlet that the same wire feeds.
  - So it grades wire to quadlet, not engine output to wire.
- **Evidence.** Swapping two `KL_crf_rx` output bindings leaves the mux untouched, and every check stays green:

  | Mutant | Legs run | Result |
  |---|---|---|
  | `p1_bind_lock_unlock` | nxn, notify, nxn8, nxndv | all green |
  | `p2_bind_late_early` | nxn, notify, nxn8, nxndv | all green |
  | `p3_bind_mr_tu` | nxn, notify, nxn8, nxndv | all green |
  | `p5_bind_fmt_late` | nxn, notify | all green |

  Sources: `receipts/mutants_reviewer_b.txt`, `receipts/mutants_reviewer_b_otherlegs.txt`, `receipts/mutants_reviewer_c.txt`.
- **Which bindings are guarded.**
  - Guarded: FRAMES_RX, STREAM_INTERRUPTED and SEQ_NUM_MISMATCH. The wrap arm drives these with real PDUs, and `p4_bind_intr_lock` is red.
  - Unguarded: MEDIA_LOCKED, MEDIA_UNLOCKED, MEDIA_RESET, TIMESTAMP_UNCERTAIN, UNSUPPORTED_FORMAT, LATE_TIMESTAMP and EARLY_TIMESTAMP. Six of these seven are new connections in this change.
- **Current code.** The bindings at this head are correct by inspection. The defect is in the evidence, not the RTL.
- **Impact.**
  - A controller could read MEDIA_LOCKED as MEDIA_UNLOCKED, or LATE_TIMESTAMP as EARLY_TIMESTAMP, and no gate would notice.
  - `milan_datapath.sv:7158-7166` already records this class of port-map swap, for `cur_config` and `clk_src_index`.
  - REGISTER_MAP criterion 4, audit B4, compliance-matrix row 5.4.2.25 and the CHANGELOG all call the duty closed on this evidence.
- **Required outcome.**
  - Each of the ten quadlets is shown, at the root, to carry the named `KL_crf_rx` output.
  - One way is to drive the engine's own event for each counter. Another is to seed through the engine's state rather than the root wire's name.
  - Either way, every permutation of the port map must turn a named check red.
  - The REGISTER_MAP criterion-4 evidence and the milan_dp README mutation list then name the binding class.
- **Verification.**
  - Rerun `p1`, `p2`, `p3`, `p5` and the other pairings with `scripts/mutants.py`.
  - Each must be red on the broad legs.
  - The unmutated head must stay green.

### F2 - MINOR - Tests, Docs - `[NOTIFY-CRF]` cannot fail for a CRF row that keeps pushing every second

- **Where.**
  - The check: `tb/verilator/milan_dp/sim_nxn.cpp:1324-1345`.
  - The claim: `tb/verilator/milan_dp/README.md:514-519`, which says the limit "releases it once".
- **Authority.**
  - Milan v1.2 Table 5.22: GET_COUNTERS is sent when a counter is updated, at most once per descriptor per second.
  - AGENTS.md section 6, Tests: a new test must be able to fail for the defect it claims to detect.
  - The check is named "...and RELEASED exactly once after it".
- **Evidence.**
  - Mutant `r3_crf_pend_stuck` reverts the pending-clear loop bound that this change widened. At `milan_datapath.sv:7260`, `s < PP_CTR_SIN_N_C` goes back to `s < N_STREAMS`, so the CRF row's pending bit is never cleared.
  - That mutant passes every `[NOTIFY-CRF]` and `[CTRS-CRF]` check on nxn and notify (`receipts/mutants_reviewer_a.txt`).
  - This round added one check to a disposable harness copy: no further push without a further change (`receipts/probe_harness.diff`). The mutant then pushes the CRF row 4 times in 3.3 processor seconds (`receipts/probe_notify_repeat.txt`).
  - The unmutated control with the same added check pushes 2 times and passes 144/0.
  - The existing 900 ms / 1100 ms bracket cannot tell "released once" from "pushes every second forever".
- **Impact.** Suppose the one line that clears the CRF row's pending bit regresses.
  - GET_COUNTERS then goes to every registered controller once a second, with no counter change.
  - Every gate stays green.
- **Required outcome.**
  - The timed leg proves the row stays quiet after its release while nothing changes.
  - The README wording matches what is proven.
- **Verification.**
  - `r3_crf_pend_stuck` is red on `obj_notify`.
  - The head stays green.

### F3 - MINOR - Docs - the REGISTER_MAP opening status still lists the CRF counter bank as a remaining gap

- **Where.** `docs/reference/REGISTER_MAP.md:31-34` reads: "Remaining gaps include the root-level IDENTIFY indication, saved-state persistence, the declared CRF Stream Input's counter bank, and commands outside the served inventory."
- **Authority.**
  - AGENTS.md section 6, Docs: changed contracts are reflected in authoritative docs.
  - CONTRIBUTING.md section 6: status claims follow the ledger and the matrix.
- **Evidence.**
  - This change closes that gap on the same page, at `:138-141` and in the `0x738` group (`:840-895`).
  - The CHANGELOG, audit B4, the compliance matrix and FR_NFR also say it is closed.
  - The opening paragraph was not updated, so the authoritative register map now contradicts itself.
- **Impact.** A reader of the page's opening status is told that the CRF input serves no counters.
- **Required outcome.** The opening status paragraph agrees with the closure recorded below it.
- **Verification.**
  - Re-read `REGISTER_MAP.md:25-40` at the fixed head.
  - Rerun `docs_check.py` and `check_em_dash.py`.

### S1 - SUGGESTION - Tests - the arbiter's no-starvation property has no discriminating check

- **Evidence.**
  - Mutant `r6_rr_sout_old` resumes the round-robin at the STREAM_OUTPUT row just delivered, instead of the next one. It passes every leg.
  - This change edited that line.
  - The property it protects ("a continuously changing low index cannot starve a higher one", `milan_datapath.sv:7193-7195`) was already untested at base.
- **Suggestion.** A later arbiter test with one continuously re-pulsing source.

### S2 - SUGGESTION - Tests, Robustness - no suite leg elaborates a shape without the CRF sink

- **Evidence.**
  - `clocking.crf_sink: false` is a supported builder option, and the new `g_ctr_no_crf_dirty` branch exists for it.
  - No tracked config or leg elaborates it.
  - A disposable probe shows it elaborates cleanly (`receipts/elab_4x4_nocrf.log`), but nothing grades it.
- **Suggestion.** An elaboration-only or harness leg on such a shape.

### S3 - SUGGESTION - Conformance, Docs - `Closes #529` would close the issue before its silicon acceptance item

- **Evidence.**
  - Issue #529's acceptance includes "la_avdecc reports the entity Milan-compatible on silicon".
  - The A10 assignment publicly schedules that check after the merge. The PR ticks the acceptance box with that caveat.
  - The PR body's `Closes #529` would still close the issue at merge.
- **Suggestion.** Either record publicly that the silicon verdict is tracked in #117, or keep #529 open until it lands. This is listed under manager duties.

## Per-lens results at this head

```text
[R268] PASS RTL - hdl/milan/milan_datapath.sv:3511-3552,5438-5501,7184-7301; hdl/ieee1722/crf/KL_crf_rx.sv (token-equal to base); receipts/elab_shape_widths.txt - clock/reset, widths, arm disjointness, arbiter index arithmetic, both shape branches, resource effect
[R268] PASS Robustness - hdl/milan/milan_datapath.sv:3524-3526,7255-7274; receipts/probe_notify_repeat.txt; receipts/elab_4x4_nocrf.log; receipts/head_run_nxn.log - undeclared index, aliasing, reset and bind wipe, 32-bit wrap, pending absorption, no re-push at head, no-CRF shape, engine always present
[R268] MINOR Conformance, Tests, Docs - hdl/milan/milan_datapath.sv:5483-5496 with tb/verilator/milan_dp/sim_nxn.cpp:3315-3329,3409-3422 - seven of ten KL_crf_rx root bindings undiscriminated (F1)
[R268] MINOR Tests, Docs - tb/verilator/milan_dp/sim_nxn.cpp:1324-1345 - [NOTIFY-CRF] cannot fail for a row that keeps pushing every second (F2)
[R268] MINOR Docs - docs/reference/REGISTER_MAP.md:31-34 - opening status still lists the CRF counter bank as a remaining gap (F3)
```

### `[R268] PASS RTL`

Artifacts:
- `hdl/milan/milan_datapath.sv:3511-3552, 5438-5501, 7184-7301`;
- `hdl/ieee1722/crf/KL_crf_rx.sv` (token-equal to base).

Checked:
- **Clock and reset:** `axis_clk` only, no new crossing, and all new state is reset.
- **Widths:** the full 16-bit index compare; `PP_CTR_SIN_N_C`-wide vectors; the round-robin width against `PP_CTR_EVT_N_C`.
- **Mux priority:** the CRF arm is disjoint from the AAF, STREAM_OUTPUT, AVB_INTERFACE and CLOCK_DOMAIN arms.
- **Arbiter arithmetic:** the pick, clear and round-robin index steps.
- **Both shape branches** elaborate (`receipts/elab_shape_widths.txt`).
- **Resource effect,** understood by inspection: seven 32-bit tallies, one 12-way arm and one arbiter row.

### `[R268] PASS Robustness`

Artifacts:
- `milan_datapath.sv:3524-3526, 7255-7274`;
- `receipts/probe_notify_repeat.txt`, `receipts/elab_4x4_nocrf.log`, `receipts/head_run_nxn.log`.

Checked:
- Undeclared index N+1 is refused with a zero body.
- Large indices do not alias.
- The reset value is zero, and the not-bound-to-bound edge wipes the row.
- Both update laws wrap at 32 bits.
- Repeated dirty pulses are absorbed while pending.
- At head there is no re-push after release (the probe control).
- The no-CRF-sink shape elaborates.
- `KL_crf_rx` is present in every configuration.

### Unclean lenses

- **Conformance: UNCLEAN (F1).** Everything else under this lens checked clean:
  - the Table 5.16 mask and Table 7-157 offsets;
  - the 5.3.8.10 wrap and reset-on-bind rules;
  - the Table 5.22 rate limit;
  - the AAF rows and NO_SUCH_DESCRIPTOR.
- **Tests: UNCLEAN (F1, F2).**
- **Docs: UNCLEAN (F1, F2, F3).** Outside those findings, these are accurate against the code and the reproduced evidence:
  - the CHANGELOG, compliance matrix, FR_NFR and roadmap;
  - the builder page, REGISTER_MAP_CLASSES and audit B4;
  - the `KL_crf_rx` and `milan_datapath` comments.

## Reviewer-owned ledger

| Lens | Status | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1) | Milan v1.2 5.3.8.10 / Table 5.6, 5.4.2.25 / Table 5.16, 5.4.5.2 / Table 5.22; IEEE 1722.1-2021 Tables 7-156/7-157; `milan_datapath.sv:3511-3552, 5482-5500, 7206-7298`; `KL_aecp_notify.sv:437`; issue #529 criteria 1-4 | R268-1 | `f815577559d4922c945dcf1436d4394ff2c10567` |
| RTL | CLEAN | `milan_datapath.sv:3511-3552, 5438-5501, 7184-7301`; `KL_crf_rx.sv` token comparison; both shape elaborations | R268-1 | `f815577559d4922c945dcf1436d4394ff2c10567` |
| Robustness | CLEAN | `milan_datapath.sv:3524-3526, 7255-7274`; `receipts/probe_notify_repeat.txt`; `receipts/elab_4x4_nocrf.log`; `[CTRS-CRF]` isolation and wrap results | R268-1 | `f815577559d4922c945dcf1436d4394ff2c10567` |
| Tests | UNCLEAN (F1, F2) | `sim_nxn.cpp:1280-1345, 3271-3491`; 20 mutants and 1 control (`receipts/mutants_*.txt`); 7 reproduced suites | R268-1 | `f815577559d4922c945dcf1436d4394ff2c10567` |
| Docs | UNCLEAN (F1, F2, F3) | CHANGELOG.md; docs/reference/REGISTER_MAP.md, REGISTER_MAP_CLASSES.md, MILAN_COMPLIANCE_MATRIX.md, FR_NFR.md; docs/MILAN_V12_ROADMAP.md; docs/ENDSTATION_BUILDER.md; docs/testing/MILAN_V12_AUDIT_2026-08-16.md; tb/verilator/milan_dp/README.md; scripts/port_docs.budget; docs gates | R268-1 | `f815577559d4922c945dcf1436d4394ff2c10567` |

## Prior public findings

Order of work:

- The verdict, findings F1-F3 and S1-S3, and the ledger above were written before any other reviewer's material was read.
- The only prior public round on PR #534 is `[R269] NEGATIVE - exact head f815577559d4922c945dcf1436d4394ff2c10567` (R269-1, issue comment 5801131672, at the same head).
- The PR has no review objects or review comments.

Each R269-1 item, checked again at this head:

| R269-1 item | Disposition at this head |
|---|---|
| F1 MAJOR (Conformance, Tests, Docs): the root-wire tests cannot detect a permuted `KL_crf_rx` port binding | **RETAINED, not resolved.** Same defect as this round's F1, found independently. See the note below the table. |
| S1: `crf_sink: false` shape unexercised | **RETAINED** as a SUGGESTION. Same as this round's S2. |
| S2: the `[NOTIFY-CRF]` floor is 990 ms, while the timed-leg header (`sim_nxn.cpp:1061-1062`) says "released after >= 1000 ms" | **RETAINED** as a SUGGESTION. The header text is verified. This round's F2 concerns the other end of the same bracket: nothing is checked after the release. |
| S3: `configs/endstation_arty_4x4.yaml:103`, `endstation_ax7101_8x8.yaml:153`, `endstation_arty_8ch.yaml:139` still point runtime gaps at "the current audit B3 and B4" | **RETAINED** as a SUGGESTION. Verified. See the note below the table. |
| S4: the frozen REGISTER_MAP closure-criteria wording was replaced by paraphrases, and criterion 2's "compact" is gone | **RETAINED** as a SUGGESTION. Verified against the base text at `ede8d48e`. This round independently confirms the author's reading: `0xF3F` at the IEEE offsets, with only Table 5.17 compacting. The fix for F1 is a natural point to quote the frozen text beside the resolution. |
| S5: `Closes #529` with the silicon item still open | **RETAINED** as a SUGGESTION. Same as this round's S3. |

On R269-1 F1:

- This round reproduced it with `p1`, `p2` and `p3`, which are R269's `mx2`, `mx3` and `mx1`.
- This round extended it with `p5` (UNSUPPORTED_FORMAT/LATE_TIMESTAMP swap, green).
- Severity differs. This round grades it MINOR, because the RTL is correct and the gap is in the evidence. R269-1 grades it MAJOR.
- Either grade leaves Conformance, Tests and Docs unclean, and the required outcome and verification are the same.

On R269-1 S3: the comment is a pointer to where gaps are graded, not a claim that the CRF counter gap is open. That is why this round treats it as a SUGGESTION, unlike F3.

What this round adds beyond R269-1: F2 (the stuck-pending push) and F3 (the REGISTER_MAP opening status). They are open in addition to R269-1 F1.

## Receipts

Paths are relative to the packet root. `MANIFEST.sha256` lists every published file.

- `scripts/`: `state_receipt.sh`, `legs.mk`, `mutants.py`, `make_probe_harness.py`, `gen_nocrf_shape.py`, `elab_shape.sh`.
- `receipts/clone_state_before.txt` and `receipts/clone_state_after.txt` are identical. The review clone was never written; every build ran in a disposable copy.
- `receipts/tool_identity.txt`: the pinned simulator. Its wrapper and `verilator_bin` hashes equal the author's record.
- `receipts/head_*`: the reproduced suites.
- `receipts/gate_*`: the reproduced gates.
- `receipts/mutants_*.txt` and `receipts/mutants/<id>/`: the mutant summaries, each mutant's diff, and its compressed run logs.
- `receipts/probe_*`: the repeat-push probe.
- `receipts/elab_*` and `receipts/nocrf_adp_shape_defaults.svh`: the shape probes.
- `receipts/hosted_check_runs.tsv`: the exact-head hosted check runs, read only.

## Limits and pending manager duties

- **Not run here:**
  - the full suite sweep and the Yosys and builder banks;
  - milan_dp obj_gptp, obj_gptplat, obj_nolpf, obj_prune, obj_ax1x1 and obj_aclk, and the render mutants;
  - milan_dp_render, crf_rx and behave (crf_rx is token-equal to base);
  - act and hardware.
- **Synthesis:**
  - The +1,134 generic-cell delta is the author's figure. It was not reproduced here.
  - Physical timing and area were NOT RUN by anyone.
  - The change adds one priority arm to the registered GET_COUNTERS answer cone.
- **Hosted, exact head, read only:**
  - 21 of 22 check runs concluded success.
  - "Physical gPTP (nightly and manual)" was skipped. A skipped context is not evidence.
  - All seven required contexts concluded success.
  - Hosted and act acceptance belong to the manager.
- **Pending manager results:** the source static/builder and native banks for this head are still running. This report makes no claim about them.
- **Merge-turn candidate:** the final candidate against live dev `759da623` is separate from this source review. The manager builds and gates it.
- **Silicon:** Milan-controller confirmation on silicon (#117) is NOT RUN. Field skips are not hardware proof. See S3 for how #529 gets closed.
- **Probe scope:** the no-CRF-sink shape was elaborated only, not run. The repeat-push check exists only in a disposable harness copy; it is not committed evidence.
- **Re-review:** F1-F3 need a new head and a new round.
  - A fix touching `sim_nxn.cpp` or the docs un-covers Tests and Docs.
  - A fix touching `milan_datapath.sv` also un-covers RTL and Robustness.

R268-1 FINISHED
