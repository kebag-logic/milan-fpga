[R239] POSITIVE - exact head 059c3a60b8290873ed9fd14673f9981e8af754ce

Round R239-1, external cleared-context review of kebag-logic/milan-fpga issue #372 / PR #518, started by PR comment 5788891478. Head `059c3a60b8290873ed9fd14673f9981e8af754ce`, tree `600468436fb9435a6b15c41db0156e5304848cb6`, sole parent `60c5225fe5f93209bf313c51b7a722f25f9aaa7d`, source base `52711029f374650dc93830d5ea28e81cb5c8f410`.

Verdict basis: no BLOCKER, MAJOR or MINOR is open at this head. All five lenses were applied at this head and are covered clean. The three MINOR Docs findings of the earlier R239 round at `60c5225f` (F1, F2, F3) are RESOLVED at this head. Four new SUGGESTIONs (S1 to S4) and the three earlier SUGGESTIONs are optional and do not affect coverage.

Label note: the earlier R239 round at `60c5225f` (PR comment 5779875386, NEGATIVE) used the same round label, R239-1. In this report, "R239-1" means this external round at `059c3a60`.

## 1. What was read, in order

1. AGENTS.md, CONTRIBUTING.md, docs/README.md, REQUIREMENTS.md (REQ-VER-01/02/04).
2. Issue #372: its body, the settled scope decision (comment 5776353888), the takeover and REVIEW READY comments, the bounded correction assignment (5780262565), and the manager's validation comments.
3. The interface authority: `hdl/common/axis_mux_rr_2in_1out.sv` and its product instance at `hdl/ieee8021as/ptp_timestamp/ptp_ts_top.sv:404`.
4. The diff `52711029..059c3a60` (12 files, +2270/-7) and its history. That history is the author commit `5bbf2953`, the validation merge `60c5225f` and the docs correction `059c3a60`.
5. Harness plumbing: `tb/common/verilator_harness.hpp` (usage), `scripts/suite_tally.py`, `scripts/run_all_suites.sh`, the `rtl.yml` shard and timeout policy.
6. Public executable evidence: the manager packet `a2d658e0/review-evidence/372-r1/corrected-source2/manager`, the exact-head hosted check runs and the hosted shard-2 suite log.

I wrote my own verdict and ledger to `INDEPENDENT_PASS.md` before reading any prior review finding (timestamp: `receipts/prior_findings_read_at.txt`). Only after that did I read the earlier R239 findings and the R240-1 and R240-2 reports. My independent verdict did not change.

Not read: author lane material, private scratchpads, and any other management directory.

## 2. Identity and change extent

- HEAD and tree are exact. `git diff --raw 52711029 059c3a60` lists 12 paths, all mode 100644:
  - 5 added: three SVA files, `mux_sva_main.cpp`, `sva_campaign.py`;
  - 7 modified: `ASSERTIONS.md` is new, and four doc indexes, the Makefile and one line block in `measure_test_evidence.py` change.
- No path under `hdl/`, `syn/`, `sw/` or `third_party/` changes, and no gitlink changes.
- The correction commit `60c5225f..059c3a60` changes four paths only: `ASSERTIONS.md`, `TESTING.md`, `tb/verilator/README.md` and the banner of `mux_sva_main.cpp`.
  - The harness bytes from line 36 to EOF are identical at both heads: 39,374 bytes, sha256 `88da057b...8bce6339`.
  - `tb/common/`, the Makefile, `sva_campaign.py`, `scripts/` and `hdl/` are unchanged by the correction.
- `sim_main.cpp` and the Makefile `run` recipe, VFLAGS and SRCS are unchanged from the base.
- Pinned tool: the selector `<pinned>` (sha256 `905795b9...`) runs `<layer>/usr/bin/verilator` with `VERILATOR_ROOT` in the same layer.
  - `--version` is `Verilator 5.050 2026-07-01 rev v5.050`.
  - `verilator_bin` sha256 `44898b22...` equals the manager's recorded binary digest.
  - 123/123 regular package files match the package mtree; 4 manual pages are absent (`receipts/tool_mtree.txt`).

## 3. Execution evidence produced by this round

All builds used `<pinned>` with at most 8 jobs, confined to CPUs 0-7. They ran in a disposable scratch copy `<scratch>` of the exact head plus `third_party/verilog-axis` at its gitlink. Static gates ran in a separate local clone. Nothing ran in the review clone.

| Execution | Result | Receipt |
|---|---|---|
| `make -C tb/verilator/ptp_ts VERILATOR=<pinned>`, legacy `-j 0` overridden to `-j 8` | exit 0, 112 s; `suite_tally --verdict` 0; tally 495 = 92 + 170 + 171 + 62, 4 tallies, 0 failures | `receipts/suite_full.log`, `suite_full_cmd.txt` |
| Rerun `make mux-sva sva-campaign` after probes | exit 0, 96 s; 170 / 171 / 62; 80 raw row logs kept | `receipts/rerun_mux_sva_campaign.log`, `receipts/campaign_raw/` |
| Default error limit, stimulus fault | exit 1 after `Verilog $stop` and the named assertion line | `receipts/probes/default_error_limit.log` |
| Bad `+scenario`, `+stimulus_fault=s2_...`, `+seed=12x` | exit 2 each | this report (command outputs) |
| 13 independent DUT mutants, none in the campaign | 13/13 fail the default run (exit 1). 12 are named by an assertion at the first failing edge. `last_served_frozen` is caught by the scoreboard alternation check only, as designed. | `receipts/probes/mutants/summary_dut.txt`, `dut/*/` |
| 13 full weakenings, one per property kind, run through the campaign rows written for it | 13/13 make their rows fail (exit 1, "properties named: none") | `receipts/probes/mutants/summary_weaken*.txt` |
| Partial weakenings | TDATA stability narrowed to bit 0 survives 5 rows; `ai_payload` without its TDATA compare survives; dropping the s1 half of `ap_grant_only_to_requester` is caught | same |
| Bind onto the product mux in the original `ptp_ts_top` leg (probe only) | build 0, run 0, `ptp_ts: 92 checks, 0 failures`. Scope `TOP.ptp_ts_top.axis_tx_rx_ts_switch_rr.u_sva` gives 21/21 pairs non-vacuous (min 8). The warning set is identical to the base leg; 0 warnings come from the SVA files. | `receipts/probes/top_bind_*` |
| Tool-semantics probe | Covered in the paragraph below this table | `receipts/probes/semantics/` |
| Upstream v5.050 `Changes`, fetched read-only | Section 5.038: "Change `--assert` to be the default" | `receipts/verilator_v5.050_Changes.txt` (sha256 `71f0d607...`) |
| Static gates in a local clone | 21 invocations, all exit 0 on final run. Six first refused (exit 2) for missing submodules in that clone; after initialising the three required pins from the review clone, they exit 0. Both receipts are kept. | `receipts/static/SUMMARY.txt`, `01..21.log` |

The static gates are: `docs_check`, `gen_toc --check` and `--verify-anchors`, `check_em_dash --base 52711029`, `check_doc_style`, `check_doc_paths`, the SV, C++, Python and shell idiom gates, `measure_test_evidence --check`, `suite_tally --selftest`, `check_hygiene --check`, `git diff --check 52711029 059c3a60` and `sva_campaign.py --list`. The evidence ratchet reads 74 <= 77 and 0 <= 0 unexplained readers; no budget was widened.

The tool-semantics probe measured these behaviours on the pinned tool:
- A build with and without `--assert` produces an identical action trace, so assertions are on by default.
- At the first edge, `$past(one) == 1` and `$stable(one)` fail for a constant `one = 1'b1`.
- An attempt that completes on a reset edge is skipped: no action runs.
- An attempt that starts on a reset edge passes vacuously at release, with flag 0.
- A pass action runs at every running edge.
- `assume` fails like `assert`.
- `cover` produces 0 actions without `--coverage-user` and 8 with it.
- `$assertvacuousoff` leaves the trace identical.

Disclosures:
- The three weakening probes for TDATA, TKEEP and TLAST stability were first written as `$stable(x)` -> `1'b1`. That leaves the signal unused, so `-Wall` refused the build, and the campaign then graded stale clean binaries. Those rows are recorded as invalid and superseded by `v2_*` tautology rewrites that keep the signal referenced. This is what S4 describes.
- The first full run's per-row campaign logs were deleted by my own later `--only` probe runs (`sva_campaign.py:535`). That is the earlier round's retained suggestion. The first run's verdict table is in `suite_full.log`; complete raw row logs come from the rerun.

## 4. Earlier findings at this head

[R239] RESOLVED F1 - MINOR, lens Docs - `docs/testing/ASSERTIONS.md:85-89`, `:152-165`, `:187-192` - reset and first-edge past semantics
Evidence: the text now says:
- an attempt completing on a reset edge is skipped;
- an attempt starting on a reset edge passes vacuously with flag 0;
- `rst_n` must stay inside the witness flag's `$past`;
- the first-edge previous value is 0 regardless of declared initial value.
My independent semantics probe reproduces every one of those statements on the pinned tool (`receipts/probes/semantics/run_assert.log`, edges 0, 3, 5).

[R239] RESOLVED F2 - MINOR, lens Docs - `docs/testing/TESTING.md:443`, `tb/verilator/README.md:51`, `tb/verilator/ptp_ts/mux_sva_main.cpp:15-19`, `docs/testing/ASSERTIONS.md:198-203` - witness grading
Evidence: all four now state 15 equality, 2 floor and 4 presence checks. That matches `witness_expectations()` (`mux_sva_main.cpp:925-946`) and the printed witness tables of both widths in `receipts/suite_full.log`. The banner change touched a Tests and Robustness artifact, so both lenses were re-applied at this head (section 6).

[R239] RESOLVED F3 - MINOR, lens Docs - `docs/testing/ASSERTIONS.md:293-294` - formal-tool claims
Evidence: the section now reads only "Only simulation ran. No formal tool has read these properties." The unmeasured construct-support and flow-behaviour claims are gone.

Earlier SUGGESTIONs are RETAINED unchanged as SUGGESTIONs. The code is unchanged, and all three are tracked in the #495 residue checklist:
- Tests: width 8 cannot see TKEEP forwarding defects (`mux_sva_main.cpp:104-109`).
- Robustness: `--only` deletes every retained campaign log (`sva_campaign.py:535`, reconfirmed by my own runs).
- Robustness: an empty `+seed=` is accepted (exit 0, default seed; reconfirmed).

## 5. New findings from this round

No BLOCKER, MAJOR or MINOR. Four SUGGESTIONs:

[R239] SUGGESTION S1 Tests - `tb/verilator/ptp_ts/mux_sva_main.cpp:262`, `:264`; `tb/verilator/ptp_ts/sva_campaign.py:151-154`; `tb/common/sva/axis_stream_source_sva.sv:74`; `tb/common/sva/axis_mux_rr_2in_1out_sva.sv:179-182` - the campaign pins one defect per property, so some narrowed properties still pass it
Authority/evidence: CODE_QUALITY Rule 8 as the guide applies it. Two narrowed properties pass every campaign row written for them:
- TDATA stability narrowed to bit 0 (`$stable(tdata_i & TDATA_WIDTH_P'(1))`) passes all five rows, because the stimulus faults flip bit 0 only (`receipts/probes/mutants/weaken/v2_tdata_stable_bit0_only/`).
- `ai_payload_forwarded_on_transfer` without its TDATA compare passes, because its only campaign mutant is a TKEEP defect (`weaken/payload_no_tdata/`).
The shipped properties do catch TDATA and TLAST forwarding defects (`dut/wrong_tdata_source_s1`, `dut/tdata_bit0_flip_s0`, `dut/wrong_tlast_source_s0`). The guide disclaims completeness (`docs/testing/ASSERTIONS.md:300-301`).
Impact: a later edit that narrows one of these properties would pass the suite unnoticed.
Required outcome (optional): flip the MSB, or every bit, in the TDATA and TKEEP stimulus faults, and add one TDATA or TLAST forwarding mutant for `ai_payload_forwarded_on_transfer`.
Verification: rerun `probe_mutants.py ... weaken v2_tdata_stable_bit0_only` and `weaken payload_no_tdata`. Both must report `INFO-caught`.

[R239] SUGGESTION S2 Tests, Robustness, Docs - `docs/testing/ASSERTIONS.md:296-299`; `hdl/ieee8021as/ptp_timestamp/ptp_ts_top.sv:404`; `tb/verilator/ptp_ts/Makefile:74`; `tb/common/sva/axis_stream_source_sva.sv:60` - the product mux instance can be bound, but the suite does not do it
Authority/evidence: the settled scope keeps the original `run` leg unchanged, and the guide records this as a limit, so this is not a defect. A probe compiled that leg with the unchanged checker and bind plus a witness stub. The bind reached `TOP.ptp_ts_top.axis_tx_rx_ts_switch_rr.u_sva`, all 21 pairs were non-vacuous on product traffic, and nothing fired over the original 92 checks. Reuse elsewhere needs an `axis_sva_witness` DPI definition; a missing one fails at link time, not silently.
Impact: the representative module is checked standalone only; its one product integration carries no assertion today.
Required outcome (optional): a follow-up issue to bind the checker in the `ptp_ts_top` leg, and a guide sentence saying every build that compiles a checker must define `axis_sva_witness`.
Verification: `sh scripts/top_bind_probe.sh <scratch> <pinned> <dir>` reproduces the result.

[R239] SUGGESTION S3 Docs - `docs/testing/ASSERTIONS.md:152-153`, `:6-8`, `:67-72`; `docs/testing/TESTING.md:443` - evidence durability and three precision nits
Authority/evidence: AGENTS section 2 says a cold reviewer reconstructs from GitHub and the repository.
- The reset and first-edge facts cite a commit on `372-review-evidence`, a branch that is not protected and never merges.
- The page says every behaviour "was measured on" 5.050. The "before 5.038" clause is an upstream changelog fact; it is true, but it is not a 5.050 measurement.
- TESTING.md groups the unused-path control with those whose "detection check must fail", but that control runs no stimulus fault.
Impact: the link can rot if the branch is cleaned up. The prose itself states the probe, so the facts stay reproducible.
Required outcome (optional): commit the small probe in-tree, or protect the evidence ref. Attribute the 5.038 clause to the changelog, and scope the TESTING.md wording to three of the four controls.
Verification: re-read the lines; `docs_check`, `gen_toc --check`, `check_em_dash --base`.

[R239] SUGGESTION S4 Robustness - `tb/verilator/ptp_ts/sva_campaign.py:243-245`, `:316`, `:329`, `:415-416`; `docs/testing/ASSERTIONS.md:257-260` - the campaign run by hand can grade stale binaries
Authority/evidence: the clean, stimulus and unused-path rows run whatever `obj_dir_mux_sva_w{8,64}/Vmux_sva` exists. They do not check that it was built from the current sources. In my first weakening probes, `make mux-sva` failed while older binaries remained, and those rows passed on them. `make` and the sweep are unaffected: `sva-campaign: mux-sva` (`Makefile:92`) rebuilds first and stops on a build failure.
Impact: only a developer running the documented `sva_campaign.py --only ...` by hand, after editing a checker, can get a stale verdict.
Required outcome (optional): the campaign rebuilds or stamp-checks the clean binaries, or the guide says to run `make mux-sva` first.
Verification: edit a checker so its build fails, then run a stimulus row directly. The row must fail.

## 6. Clean lenses

[R239] PASS Conformance - issue #372 comment 5776353888; `tb/common/sva/axis_stream_source_sva.sv:63-89`; `tb/common/sva/axis_mux_rr_2in_1out_sva.sv:109-187`; `tb/common/sva/axis_mux_rr_2in_1out_bind.sv:31-58`; `tb/verilator/ptp_ts/Makefile:44-97`; `receipts/suite_full.log` - every in-scope item of the settled contract and the three acceptance criteria, at this head
- Stalled TVALID is held and TDATA, TKEEP and TLAST are stable until the handshake. This is the Arm IHI0051A 2.2 obligation as the settled scope cites it. It is enforced on s0, s1 and m, with the owner in the instance name.
- Grant exclusivity, legal state, grant only to a requester, ownership held until the TLAST handshake, release after TLAST and reset release are each a named property. Four deferred immediate laws cover forwarding.
- The checker is bound by module name to the unmodified mux.
- The checks run in the existing `ptp_ts` default target (`all: run mux-sva sva-campaign`), under the same suite name. That suite is still in shard 2/5, and no workflow, global flag or budget changes.
- AC1 is met: 170/171 checks pass at w8/w64.
- AC2 is met: 62/62 campaign rows pass, plus 13/13 independent mutants and 13/13 full weakenings.
- AC3 is met: the guide covers every required topic, and F1 to F3 are resolved.
- Product RTL and the three required pins are unchanged.

[R239] PASS RTL - `tb/common/sva/axis_mux_rr_2in_1out_bind.sv:31-58`; `tb/common/sva/axis_mux_rr_2in_1out_sva.sv:121-187`; `tb/common/sva/axis_stream_source_sva.sv:53-89`; `hdl/common/axis_mux_rr_2in_1out.sv:52-126` (unchanged blob); `receipts/probes/top_bind_*`, `semantics/` - binding, widths, reset and sampling of the real bound instance
- The bind resolves `state` and the enum literals in the target scope. It reached both the standalone top (`TOP.axis_mux_rr_2in_1out.u_sva` plus three sub-scopes) and, in the probe, the product instance.
- Widths follow `TDATA_WIDTH`. 8 and 64 build under `-Wall` without `-Wno-fatal`, and 12 is refused by `gen_guard_tdata_width`.
- `disable iff`, reset-edge and first-edge behaviour match the checker's witness design on the pinned tool.
- The checker drives nothing, and there is one clock, so no CDC applies.
- The SVA files are in no synthesis or source list: `check_rtl_source_lists` passes in the manager bank, and hosted Yosys passes.
- The house style holds: SPDX and banner, `default_nettype`, `//!` ports, typed `_P` parameter, `_w` wires, named blocks.

[R239] PASS Robustness - `tb/verilator/ptp_ts/mux_sva_main.cpp:161-282`, `:612-637`, `:671-696`, `:758-784`, `:873-921`; `tb/verilator/ptp_ts/sva_campaign.py:289-300`, `:411-480`; `receipts/probes/`, `receipts/suite_full.log` - reset during activity, backpressure, malformed input, configuration and lost coverage
- These scenarios run at both widths and pass:
  - reset while stalled on a middle beat and on a TLAST beat;
  - seeded random reset;
  - 4-cycle and 5-cycle stalls;
  - valid gaps with poison payload;
  - simultaneous offers.
- Malformed plusargs exit 2. At the default limit an assertion stops the run with exit 1, and at a raised limit with exit 3. Watchdogs are counted in DUT cycles.
- These controls are refused: `--no-assert`, the mistyped bind, the swapped ports and the unused path. The width-12 build is refused by the checker's own message.
- The banner-only change leaves the executable suffix byte-identical.
- The optional items are S4 and the two retained Robustness suggestions.

[R239] PASS Tests - `tb/verilator/ptp_ts/mux_sva_main.cpp:348-418`, `:713-740`, `:925-977`; `tb/verilator/ptp_ts/sva_campaign.py:93-161`, `:289-300`; `scripts/measure_test_evidence.py:620-623`; `receipts/probes/mutants/`, `receipts/hosted/suite-logs-2/ptp_ts.log` - defect sensitivity, independence and accounting
- Every property kind fails by its own name on a campaign defect.
- A full weakening of each of the 13 kinds makes its campaign rows fail.
- 13 independent DUT mutants are all detected.
- The scoreboard reads ports only and catches round-robin defects with no property firing.
- 15 witness pairs match the harness's own port counts exactly (w64 `u_m_dut` 228/228, `u_s0_stimulus` 625/625), 2 meet floors, and 4 are present.
- The 495-check tally is accounted in section 3 and matches the manager and hosted logs.
- Counting 62 campaign verdicts as checks follows the `render_setpoint` and `tcam` precedent. They are labelled as campaign checks, and no assertion evaluation is counted.
- The optional items are S1, S2 and the retained width-8 TKEEP suggestion.

[R239] PASS Docs - `docs/testing/ASSERTIONS.md:1-301`; `docs/testing/TESTING.md:443`; `tb/verilator/README.md:51`; `docs/README.md:82`; `docs/guides/VERIFICATION_DEVELOPER.md:95`; `receipts/static/` - accuracy against execution
- F1 to F3 are resolved.
- Every tool claim I probed matches the pinned tool or the upstream changelog.
- The example failure line reproduces exactly: `[6000]`, `u_s0_stimulus.ap_tvalid_held_until_handshake`.
- The reproduction commands work.
- The limits section is explicit.
- The docs gates exit 0: 0 em-dash findings against base `52711029`.
- The optional item is S3.

## 7. Reviewer-owned ledger

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | settled scope 5776353888; the three SVA files; Makefile; suite log | R239-1 (external, this round) | 059c3a60b8290873ed9fd14673f9981e8af754ce |
| RTL | CLEAN | bind, checker, source checker; unchanged mux; product-instance probe; semantics probe | R239-1 (external, this round) | 059c3a60b8290873ed9fd14673f9981e8af754ce |
| Robustness | CLEAN (S4 and two earlier suggestions optional) | harness source, reset and backpressure scenarios, usage exits, campaign controls, suffix identity | R239-1 (external, this round) | 059c3a60b8290873ed9fd14673f9981e8af754ce |
| Tests | CLEAN (S1, S2 and one earlier suggestion optional) | campaign 62 rows; 13 independent mutants; 13 full plus 3 partial weakenings; witness tables; tallies (local, manager, hosted) | R239-1 (external, this round) | 059c3a60b8290873ed9fd14673f9981e8af754ce |
| Docs | CLEAN (F1 to F3 resolved; S3 optional) | ASSERTIONS.md, TESTING.md, both indexes, harness banner; semantics probe; upstream changelog; docs gates | R239-1 (external, this round) | 059c3a60b8290873ed9fd14673f9981e8af754ce |

No finding was moved to another issue to obtain this result. A later commit touching a lens's artifacts un-covers that lens.

## 8. Evidence not produced by this round (inspected read-only)

- **Manager packet `a2d658e0/.../corrected-source2/manager`.**
  - Builder: 48 commands specified, 48 executed. Every executed command string equals its spec, all exit 0, and head/base are `059c3a60`/`52711029` (`receipts/manager/builder_ledger_summary.txt`).
  - Native: 5 groups specified, 5 executed, all exit 0 (`native_ledger_summary.txt`):
    - the parent sweep: 55/55 suites, 2,118,667 checks;
    - Yosys;
    - the protocol-processor suites;
    - the gPTP suites;
    - behave: 14 features, 316 scenarios, 1515 steps.
  - Its `ptp_ts` log tallies 92/170/171/62.
  - The four declared `tsn_fuzz` field and freshness skips ran nothing and contribute 0 checks. Builder calibration gate 11 is NOT RUN.
  - I did not rerun any full bank.
- **Hosted, exact head.** There are 22 check runs: 21 completed with success, and 1 completed as skipped (`Physical gPTP (nightly and manual)`, outside the required set).
  - All seven required contexts succeeded: `rtl-fast`, `docs-check`, `docs-check-no-git`, `wire-accountability`, `elaborate`, `verilator-suites`, `yosys-portability`.
  - All 5 Verilator and 4 Yosys shards executed and succeeded.
  - The shard-2 artifact's `TARGET_SHA` is `024defe0`, the hosted merge of `059c3a60` into dev `483a133e`. Its `ptp_ts.log` tallies 495 with 62/62 rows on Verilator 5.050.
- **Trusted local replica.** The manager reports PASS at `059c3a60` over `483a133e` (PR comment 5782950052). I did not inspect or run it; the manager owns it.

## 9. Real limits

- The evidence is finite, two-state, zero-delay, single-clock simulation at widths 8 and 64. There is no formal proof, no X-propagation, no CDC and no timing claim.
- Bound-assertion coverage of the product instance was shown only by my probe; the suite does not bind it (S2).
- My tool identity rests on the package's own mtree in the same layer. I did not repeat signature verification of the package archive.
- I did not re-read the Arm IHI0051A document. The section 2.2 attribution is taken from the settled scope and matches the standard handshake-stability rules.
- Physical calibration is NOT RUN, and the field skips are not hardware proof. No hardware was used.

## 10. Pending manager duties

- Final current-dev candidate validation at the merge turn. The source evidence is over `52711029`; live dev is `483a133e`.
- Deciding whether the two-positive merge bar is met. The earlier internal positive, R240-2, and this external round are both at `059c3a60`.
- Explicit maintainer merge authorization, no review in flight, post-merge containment, and issue Closed/Done.
- Disambiguating the repeated round label "R239-1" when publishing.
- Optional: a follow-up for S2; S1, S3 and S4 at the maintainers' discretion. The earlier suggestions stay on #495.

## 11. Integrity of the review clone

`receipts/integrity_review_clone_final.txt` (also the midpoint receipt), from `scripts/verify_integrity.py`:
- HEAD and tree are exact.
- 857/857 tracked blobs match by bytes, kind and mode.
- The index equals the HEAD tree, with stage-0 records only.
- There are 0 assume-unchanged or skip-worktree entries.
- There are 0 untracked or ignored paths.
- `third_party/verilog-axis`, `protocol-processor` and `gptp-processor` are checked out at their gitlinks (`48ff7a7e`, `424c688f`, `c1b61743`) and are clean.
- Object replacement was disabled during verification.
- All builds, mutants and probes ran in `<scratch>` or the local clone only.

Placeholders:
- `<clone>` is the review clone.
- `<scratch>` is the disposable exact-head copy under this output directory, in `work/`.
- `<pinned>` is the scoped selector.
- `<layer>` is the package root it executes.

Scripts and their usage: `scripts/README.md`. Receipt hashes: `MANIFEST.sha256`.

R239-1 FINISHED
