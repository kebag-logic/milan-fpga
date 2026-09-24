[R277] NEGATIVE - exact head 0f003fab3303858ba4db955ad3c0512e67a8018b

Round R277-5 is the external independent review of issue #387 / PR #555, round 3 (acceptance 3, datapath half).

- Head: `0f003fab3303858ba4db955ad3c0512e67a8018b`, tree `c8af797b92f6961339b6f51b8349c09a48cd7faf`.
- Whole PR: `57456af96b3127b9d309a995bbbd35a6113ce52d..0f003fab`, 12 commits, 28 files.
- Round-3 delta: `a21cd358..0f003fab`, one commit, 12 files.

Sources were read in this order:

1. AGENTS.md and CONTRIBUTING.md.
2. docs/README.md.
3. The issue body and its decisions: 5606198212 part b, 5794731090, 5802264260, 5810378282, 5818091077, 5819379503 and 5820240308, plus the assignment 5820585975.
4. The linked docs.
5. The diff and its history.
6. The manager's published evidence at `afb421cf` (`review-evidence/387b-r1/author-r3`).
7. The exact-head hosted runs.
8. Executable evidence this reviewer ran.

The verdict and ledger were written down before any other reviewer's findings for round 2 were read (`receipts/verdict_ledger_before_prior_findings.txt`). No finding changed after that reading.

**Summary.** Every round-2 finding from this reviewer and from the other reviewer is closed at this head, and the delta changes no functional RTL. One MINOR finding is open, under Docs only: the deadline raise did not reach four places that still state the old 2700 s `milan_dp` budget as current, two of them the testing authorities docs/README.md routes readers to. Lenses covered: Conformance, RTL, Robustness, Tests, Docs.

## Findings

### F1 MINOR - Docs - `docs/testing/TESTING.md:166-167`, `docs/testing/RUNNING_TESTS.md:79`, `tb/verilator/milan_dp_gptp/README.md:31`, `tb/verilator/milan_dp/render_mutants.py:37` - the old 2700 s `milan_dp` budget is still stated as current

- **Authority and evidence.**
  - Decision 5820240308 raises the `milan_dp` deadline to 3600 s. `scripts/run_all_suites.sh:245` now declares `${SUITE_TIMEOUT:-3600}`, and `measure_test_evidence.py:718` pins that value.
  - Four places still state the old budget as the current one (`receipts/stale_budget_grep.txt`):
    - `TESTING.md:166-167`: "The default driver permits 1800 seconds per suite, and 2700 seconds for `milan_dp`. That figure is the suite's measured hosted worst case plus a stated margin (#444)."
    - `RUNNING_TESTS.md:79`: "... except `milan_dp`, which has 2700 seconds (#444)."
    - `milan_dp_gptp/README.md:31`: "The historical `milan_dp` suite has its own 2700-second budget (#444)."
    - The `render_mutants.py:37` docstring: "per-suite guard, suite_timeout = 2700 s (#444)".
  - docs/README.md:78-79 and :101 route "Choose verification layers", "Plan verification" and "Run complete gates" to `TESTING.md` and `RUNNING_TESTS.md`. This PR itself edits `TESTING.md` (:267, :501) and did not update :166.
  - AGENTS.md section 6, Docs lens: "Changed contracts are reflected in authoritative docs."
  - The two `CI_WORKFLOWS.md` mentions (:167, :185) are correctly historical and are not part of this finding.
- **Impact.**
  - Two testing authorities contradict the runner and `CI_WORKFLOWS.md` about the deadline that turns a slow `milan_dp` run into a red context (exit 92). They also give the basis as #444's worst-case measurement, which decision 5820240308 replaced.
  - A reader who sizes a shard or judges a timeout from `TESTING.md` or `RUNNING_TESTS.md` gets 900 s less than the real budget and the wrong authority.
  - No gate catches this. `docs_check.py` and the runner contract passed.
- **Required outcome.** No current page or runner docstring states 2700 s as the `milan_dp` budget. Each such statement gives 3600 s under decision 5820240308, or points to `CI_WORKFLOWS.md`. Historical sentences stay marked as history.
- **Verification.** `git grep -n 2700 -- docs scripts tb` at the corrected head returns only the historical lines in `CI_WORKFLOWS.md` and the selftest's planted mutation (`measure_test_evidence_selftest.py:294`). The docs gates still pass.

### S1 SUGGESTION - Docs - `docs/testing/CI_WORKFLOWS.md:166` - "Two runs timed out 1 s and 13 s early"

The replaced text said the two runs were killed at the 1800 s deadline, 1 s and 13 s short of finishing. The new sentence reads as if the runs timed out before the deadline. Something like "Two runs hit the deadline 1 s and 13 s before they would have finished" keeps the record.

### S2 SUGGESTION - Tests - `tb/verilator/milan_dp/sim_aclk.cpp:1394-1411`

- The new `RENDER-SETTIME` checks can fail. This reviewer's planted datapath copies break them (`receipts/settime_render_controls.txt`):
  - with the settime removed from the render trigger only, all 4 checks fail;
  - with a second, late settime pulse, the two pulse checks fail.
- The omission control is not committed to any runner. The author's control is an evidence-only script, `author-r3/settime_render_control.py`.
- A `render_mutants.py` or `gmstep_mutants.py --all` arm would keep that proof in the tree. This is optional: the assignment took the settime check as "if cheap".

## What was checked, per lens (artifact at this head)

- `[R277] PASS Conformance - hdl/milan/milan_datapath.sv:3110-3113,:6026-6028; hdl/ieee1722/avtp/KL_media_clock_restart.sv:213-257; tb/verilator/milan_dp/sim_gmstep.cpp (gmstep 48/48); sim_aclk.cpp:1394-1411 - against IEEE 1722-2016 4.4.4.3 and 10.4.3 as quoted in the tree, Milan Table 5.4 MEDIA_RESET, decision part b, owner step policy 5794731090, rulings 5802264260 items 1-2, 5818091077, 5819379503 item 1, aligner decision 5810378282, and decision 5820240308.`
  - The step set is unchanged since round 2: `media_rebase_p_w = eff_ptp_adjust_w | cfg_ptp_cmd_load`. It joins `mcr_restart_p_w` with no clock-source gate. The CRF disruption and echo stay gated. The render trigger is `media_rebase_p_w | src_recentre_p_r`.
  - At this head:
    - gmstep passes 48/48 (`receipts/gmstep.log`).
    - option-off (233/0) and ax1x1 (230/0) grade one `mr` toggle per commanded step and one MEDIA_RESET for the settime, at INTERNAL (`receipts/option_off.log:489,514-515`, `receipts/ax1x1.log`).
    - The new `RENDER-SETTIME` grades one render pulse and one counted re-base for a software settime (`receipts/aclk_full_clean.log`, 143/0).
  - Decision 5820240308 is implemented as decided:
    - 3600 s in the runner and its contract;
    - hosted shard `timeout-minutes: 120` (`.github/workflows/rtl.yml:152`);
    - the budget, the exact-head sample of the time (2459.9 s) and the day's spread (1296-2460 s) recorded in `CI_WORKFLOWS.md:159,172-191` and in the PR.
  - The aligner decision is untouched: no aligner, grid, NCO or servo file is in the PR diff.
- `[R277] PASS RTL - git diff a21cd358..0f003fab -- hdl/ (KL_render_setpoint.sv:120-121, KL_media_clock_restart.sv:236-237) and the whole-PR RTL (milan_datapath.sv:3062-3160,:5979-6028; KL_media_clock_restart.sv:196-259; KL_crf_tx.sv comments) - comment-only proof of the delta, and re-validation of the whole-PR RTL at the head.`
  - The round-3 delta under `hdl/` is comments only. With comments stripped and whitespace normalised, both files hash identically at `a21cd358` and `0f003fab`, and no non-comment line changed (`receipts/hdl_delta_comment_only.txt`).
  - The new `KL_media_clock_restart.sv:236-237` comment matches the logic. A non-streaming talker in its stop cycle skips the merge line and takes `~mr_o`, then tracks it through the `!streaming_i` branch. The `KL_render_setpoint.sv:120-121` summary now matches the banner (:81-89) and the port spec.
  - Whole-PR RTL, re-validated at the head:
    - `lint_rtl.py --check` passes, 90 <= 90 (`receipts/lint_rtl_check.txt`).
    - `check_rtl_source_lists.py` passes.
    - Round-2 analysis of NBA order, widths and clock domain carries, because the functional bytes are unchanged.
- `[R277] PASS Robustness - scripts/probe_mcr_property.cpp + receipts/probe_mcr_property_head.txt, receipts/probe_mcr_mutants.txt, receipts/option_off.log, receipts/ax1x1.log, receipts/aclk_full_clean.log - request storms, bursts, source changes, report latency 0/1/3, the feature-off shape, the INTERNAL clock, and a settime in the middle of a live stream.`
  - My round-2 property probe, re-run unchanged against the head engine, is clean on 36/36 runs. It checks one toggle per unmerged need, no lost or spurious toggle, the 8-PDU hold, and MEDIA_RESET equal to the toggles.
  - The probe still kills the dev engine and five planted engines, so it can fail.
  - The settime inserted into the true-ratio leg before the grid phases disturbs none of them: the full leg is 143/0, and `render_mutants.py` is 6/6 with its positive legs passing.
- `[R277] PASS Tests - tb/verilator/milan_dp/gmstep_mutants.py:186-198; scripts/run_all_suites.sh:238-249; scripts/measure_test_evidence.py:716-724; scripts/measure_test_evidence_selftest.py:294; sim_aclk.cpp:1394-1411,1552; tkdiag - freshness under nested GNU make 4.3/4.4.1 for both positive legs, the budget contract's teeth, and the new settime check's teeth.`
  - **Freshness.** `repro_gmstep_freshness.sh`, run unchanged under GNU make 4.3 inside a parent `make -C` recipe, prints `is_fresh: True`. Its own diagnostic line still shows the `make[1]: Entering directory` chatter, which proves the condition was reproduced (`receipts/repro_gmstep_freshness.txt`).
  - **Both positive legs.** `freshness_nested_probe.sh` checks gmstep and option-off under make 4.3 and 4.4.1, with a plain parent and with a `-w` parent. A fresh binary gives True. One RTL file of `print-srcs` made newer gives False, which proves the source list is parsed, not only the two inputs that are always added. After the mtime is restored, the result is True again (`receipts/freshness_nested_probe.txt`).
  - **The whole inventory, nested.** `gmstep_mutants.py --all`, run nested under make 4.3, gives 13/13 with no `[INFO] ... rebuilt` line (`receipts/gmstep_mutants_all_nested_make43.log`).
  - **Hosted, exact head.** Candidate `875b57ad` = head merged onto live dev `573f0052`. Its shard 4/5 log has no rebuild line, and the three acceptance controls are caught (`receipts/hosted_head_suite_extract.txt`).
  - **Budget contract.** `measure_test_evidence.py --check` and its selftest exit 0. `runner_contract()` flags 3600 -> 2700, 3600 -> 3599 and a hard-coded `TMO` (`receipts/runner_contract_teeth.txt`). `suite_timeout` evaluates to 3600, 5400 and 1800, and an explicit override is respected (`receipts/suite_timeout_eval.txt`).
  - **tkdiag.** 96/96, and `mcr_mutants.py` 5/5 (`receipts/tkdiag_make.log`).
  - **Settime check teeth.** See S2.
- `[R277] MINOR Docs - docs/testing/TESTING.md:166-167 (+3) - F1.` Also applied, with no further finding:
  - `FPGA_DESIGN.md:169-180`, `MILAN_V12_ROADMAP.md:356-362` and `MILAN_COMPLIANCE_MATRIX.md:120` now scope the selection verdict to the CRF triggers. They state that a PHC step toggles `mr` whatever the selection and that MEDIA_RESET counts it, consistent with `REGISTER_MAP.md:124-131` and the RTL.
  - `CI_WORKFLOWS.md:156-191`: all four cited windows reproduce exactly from the cited jobs with `milan_dp_window.py`, run unchanged (`receipts/milan_dp_window_cited.txt`).
  - The suite README (:244, :436-438, :864) matches.
  - The PR body cites decisions 5819379503 and 5820240308, and the three passages I flagged as stale in round 2 are gone.
  - Gates: `docs_check.py` reports 0 findings. `check_em_dash.py --base 57456af9` gives 0 findings over 175 added lines. `gen_toc --check`, `check_doc_style`, `check_doc_paths` and `check_gptp_docs` pass (`receipts/static_docs_gates.txt`). The em-dash and TOC checks ran in an isolated scratch venv built from `tools/markdown/requirements.txt`.

## Reviewer-owned ledger

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | datapath `:3110-3113,:6026-6028`; `KL_media_clock_restart.sv`; gmstep 48/48; option-off 233/0 and ax1x1 230/0 `mr`/MEDIA_RESET checks; `RENDER-SETTIME`; decision 5820240308 against runner, workflow and pages | R277-5 | 0f003fab3303858ba4db955ad3c0512e67a8018b |
| RTL | CLEAN | `hdl/` delta (comment-only proof); `KL_media_clock_restart.sv:196-259`; datapath re-base, restart and render wiring; `lint_rtl --check`; `check_rtl_source_lists` | R277-5 | 0f003fab3303858ba4db955ad3c0512e67a8018b |
| Robustness | CLEAN | property probe 36/36 and its 6/6 kills; option-off, ax1x1 and full true-ratio legs; `render_mutants.py` 6/6 | R277-5 | 0f003fab3303858ba4db955ad3c0512e67a8018b |
| Tests | CLEAN | `gmstep_mutants.py` freshness (repro unchanged, both legs nested under make 4.3/4.4.1, stale case); `--all` 13/13 nested; hosted exact-head shard 4/5 log; budget contract and selftest with planted changes; tkdiag 96/96 + 5/5; `RENDER-SETTIME` with omission and double controls | R277-5 | 0f003fab3303858ba4db955ad3c0512e67a8018b |
| Docs | UNCLEAN (F1) | `FPGA_DESIGN.md`, roadmap, compliance matrix, `REGISTER_MAP.md`, `CI_WORKFLOWS.md` (windows reproduced), `TESTING.md`, `RUNNING_TESTS.md`, suite READMEs, `render_mutants.py` docstring, banners, PR body; docs gates | R277-5 | 0f003fab3303858ba4db955ad3c0512e67a8018b |

Tests is CLEAN on the committed checks. S2 is a SUGGESTION and does not affect coverage.

## Round-2 findings from this reviewer (R277-4, at `a21cd358`)

| Finding | Disposition at `0f003fab` | Evidence |
|---|---|---|
| F1 MINOR Tests: `is_fresh()` read `make[1]:` chatter as paths under nested GNU make 4.3 | **Closed** | `gmstep_mutants.py:191` runs `--no-print-directory -s`. The unchanged repro prints `is_fresh: True` inside the parent recipe under 4.3. Both positive legs are fresh when fresh and stale when stale, under plain and `-w` parents. The hosted exact-head log has no rebuild line. |
| F2 MINOR Docs, Tests: the margin recorded was not the head's, and was under the 10% trigger | **Closed** | Decision 5820240308 raises the budget to 3600 s, implemented in `run_all_suites.sh:245`, the contract and its selftest. `CI_WORKFLOWS.md` records the `a21cd358` sample (2459.9 s) and the spread. The workflow allows 120 min. At this head, hosted: **2454.1 s, 9785 checks, 1145.9 s = 31.8% of 3600 s** (`receipts/milan_dp_window_head.txt`), above the 10% re-split level. The other statements of the budget are F1 above. |
| S1 Docs: the PR body predates decision 5819379503 | Closed | The PR body cites 5819379503 and 5820240308. The stale passages are gone. |
| S2 Tests: no check fails without the `streaming_i[t]` term | Closed as offered (comment) | `KL_media_clock_restart.sv:236-237` states why the term is there. The assignment allowed "a tkdiag arm or comment". |

## Prior public findings from the other reviewer (R276-5, at `a21cd358`)

These were read after the verdict and ledger above were drafted.

| Finding | Disposition at `0f003fab` | Evidence |
|---|---|---|
| F1 MINOR Tests, Docs: exact-head margin 8.9% of 2700 s | **Closed** | The same as my F2 above. |
| F2 MINOR Docs: `FPGA_DESIGN.md` gated the whole `mr` machinery on the selection | **Closed** | `FPGA_DESIGN.md:169-180`; the matrix at :120 and the roadmap at :356-362 are scoped the same way. |
| S1 Docs: PR body decision citations | Closed | See above. |
| S2 Docs: `KL_render_setpoint.sv:120` summary | Closed | :120-121 now reads "a PHC step or a settled clock-source change". |
| S3 Tests: no simulation leg issues a settime and counts a re-base | Closed | `sim_aclk.cpp:1394-1411` runs in the sweep, both locally and hosted. It can fail (S2 above). |

## Judgments requested by the assignment

- **3600 s deadline and contract: implemented.** The runner, contract, selftest, `CI_WORKFLOWS.md`, suite README and PR agree. The hosted shard allows 120 minutes. At the a21cd358 sample, shard 4/5 took 42.5 min in total, of which `milan_dp` was 41 min. Other pages still state 2700 s (F1).
- **Freshness under GNU make 4.3 nesting: fixed** for both positive legs, locally and on the hosted exact-head log.
- **Documentation scope corrections: done**, and consistent with the RTL and `REGISTER_MAP.md`.
- **PR body citations, `KL_render_setpoint` summary, `KL_media_clock_restart` comment: done**, and accurate.
- **Settime re-base render check: present, in the sweep, and able to fail.** An omission control fails all four checks, and a double-pulse control fails the two pulse checks. The control is not committed (S2).
- **Delta: no functional RTL change and no regression.** gmstep 48/0, option-off 233/0, ax1x1 230/0, true-ratio 143/0, `render_mutants` 6/6, `--all` 13/13, tkdiag 96/96 + 5/5. Hosted `rtl-full`, `rtl-fast`, `elaborate` and `docs` all succeed at this head.
- **Whole PR at this head:** conformant to decision part b and every later ruling. The only open item is F1.

## Real limits

- Physical calibration was NOT RUN. Acceptance 4, the #117 two-board handover, is not evidenced, and field skips are not hardware proof.
- Not run here, by the round's rules: the full `milan_dp` `run` sweep as one recipe, the builder, PP, gPTP and Yosys banks, `run_all_suites.sh`, act/Docker, and hardware. The sweep's other legs rest on the manager's source banks, the author-r3 chunked sweep (44 commands, 9785 checks; its tested inputs match the head bytes, `receipts/author_tested_inputs_vs_head.txt`) and the exact-head hosted shard 4/5 (9785 checks, 0 failures).
- The hosted `pull_request` runs build GitHub's merge of the head onto **live dev `573f0052`** (TARGET_SHA `875b57ad`, parents `573f0052` and `0f003fab`), not onto the source base `57456af9`. Those runs are evidence for that merge, not the manager's own candidate build.
- The time figures are one hosted sample per head. `milan_dp_window.py` is the other reviewer's published round-2 script, run byte-unchanged. Its margin columns are against its fixed 2700 s, so the 3600 s margin is computed on the next line of the receipt.
- The property probe models the talker-to-feed path. It does not elaborate the packetizers.
- IEEE and Milan clauses were read as quoted in the tree and the decisions. No standards document was available on this host.
- This reviewer did not run a GNU make other than 4.3 and 4.4.1.

## Pending manager duties

- Route F1 (Docs MINOR) to a correction round, then re-review.
- Build and validate the final current-dev candidate (source base `57456af9`, live dev `573f0052`) at the merge turn.
- Accept hosted and act results on that candidate. At this head, the `verilator-suites` and `yosys-portability` aggregators succeeded, and the Physical gPTP job was skipped by design (nightly and manual).
- Obtain two independent positive reviews and a reviewer-owned five-lens ledger at the merge candidate.
- After merge: acceptance 4 on the #117 bench, and post-merge containment.

## Clone integrity

- The review clone is at `0f003fab3303858ba4db955ad3c0512e67a8018b`, tree `c8af797b92f6961339b6f51b8349c09a48cd7faf`, with no untracked or ignored entries.
- All 883 tracked blobs were re-hashed with `--no-filters` and match HEAD, modes included.
- The index writes the HEAD tree: 887 entries, all at stage 0.
- `gptp-processor` (`e5dcea6e`), `protocol-processor` (`09f9bf38`) and `third_party/verilog-axis` (`48ff7a7e`) are at their gitlinks with clean worktrees. `external` is uninitialised, as at the start, and is not a required submodule (`receipts/clone_integrity.txt`).
- Every build, planted copy and mtime probe ran in a disposable clone under `scratch/`, which is not published.

## Receipts

Every file below is listed in `MANIFEST.sha256`. Local paths are replaced by `<packet>`, `<scratch>`, `<scratch-src>`, `<pinned-tool-bin>` and `$HOME`.

- `scripts/`:
  - `repro_gmstep_freshness.sh`: my round-2 repro, byte-unchanged.
  - `milan_dp_window.py`: the other reviewer's round-2 window script, byte-unchanged.
  - `freshness_nested_probe.sh`: both legs, fresh and stale, nested.
  - `settime_render_controls.sh`: the `RENDER-SETTIME` omission and double controls.
  - `probe_mcr_property.cpp`, `run_probe_mcr_property.sh`, `probe_mcr_mutants.py`: my round-2 property probe, byte-unchanged.
- `receipts/`, local runs:
  - `repro_gmstep_freshness.txt`, `freshness_nested_probe.txt`, `gmstep_mutants_all_nested_make43.log`;
  - `gmstep.log`, `option_off.log`, `ax1x1.log`, `aclk_full_clean.log`, `render_mutants.log`, `settime_render_controls.txt`;
  - `tkdiag_make.log`, `probe_mcr_property_head.txt`, `probe_mcr_mutants.txt`;
  - `measure_test_evidence_check.txt`, `measure_test_evidence_selftest.txt`, `runner_contract_teeth.txt`, `suite_timeout_eval.txt`;
  - `hdl_delta_comment_only.txt`, `lint_rtl_check.txt`, `static_docs_gates.txt`, `stale_budget_grep.txt`.
- `receipts/`, hosted evidence and records:
  - `milan_dp_window_cited.txt`, `milan_dp_window_head.txt`, `hosted_jobs_head.txt`;
  - `hosted_head_suite_milan_dp.log`, `hosted_head_suite_TARGET_SHA`, `hosted_head_suite_extract.txt`;
  - `author_tested_inputs_vs_head.txt`, `verdict_ledger_before_prior_findings.txt`, `tool_identity.txt`, `clone_integrity.txt`.

R277-5 FINISHED
