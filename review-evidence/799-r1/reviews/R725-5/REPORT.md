[R725] POSITIVE - exact head 865c2f9d82f2394b3453f36ccf92c49317a7fddd

# R725-5: internal cleared-context delta review of PR #802 (issues #799, #790)

Head `865c2f9d82f2394b3453f36ccf92c49317a7fddd`, tree `04f8447119946dbc1fb2760fbf9f1b74e6f07b7f`. This round reviews the delta over `9e57d4af`, where R725-4 was NEGATIVE on one Docs MINOR (F1) and recorded two RESIDUE items (R1, R2).

**Verdict: POSITIVE.**

- F1, R1 and R2 are closed at their cause.
- The delta changes no code, workflow or figure.
- Every gate named in the brief is rc 0 at this head (reviewer-run).
- All five lenses are clean.
- Four new RESIDUE items (wording only) and one SUGGESTION are recorded for the residue checklist.
- One earlier RESIDUE, RES-2 (R726-2), has come back in the PR body. It is recorded as RES-A.

## Delta scope

`git diff 9e57d4af 865c2f9d --stat` (`receipts/delta.stat`, full diff `receipts/delta.diff`) lists two files:

- `docs/testing/CI_WORKFLOWS.md`, +17/-15: the #799 schedule paragraph (`:477-495`) and the `--expect` sentence (`:1506`).
- `scripts/suite_shards.py`, +2/-2: comment lines `:76` and `:154` only.

Nothing under `hdl/`, `tb/`, `sw/`, `docs/design/` or `.github/` changed, and no gitlink moved (`git diff --quiet` over those paths, rc 0). `receipts/figures-9e57d4af-865c2f9d.txt` parses `SUITE_SECONDS` and `PIECE_SECONDS` at both heads and finds no differing entry. The delta commit is one line with no trailers.

## Checks run at this head (reviewer-run, this clone, each rc the command's own)

| Check | Command | Result | Receipt |
|---|---|---|---|
| Python idiom ratchet | `python3 -I scripts/check_py_idiom.py`; `--selftest` | rc 0, rc 0. `long module: 10 <= 10`, `over-long line: 0 <= 0`. `suite_shards.py` has 1000 lines | `receipts/gates/check_py_idiom*.{log,rc}` |
| Planner | `python3 -I scripts/suite_shards.py --selftest` | rc 0, `selftest: PASS`, 44 ok lines; worker 0/19 at 1615 s, bound 1620 s | `receipts/gates/suite_shards_selftest.*` |
| Event contract | `python3 scripts/ci_events.py --check` | rc 0: `OK (2199 contract item(s) across 4 workflow files and docs/testing/CI_WORKFLOWS.md)` | `receipts/gates/ci_events_check.*` |
| Workflow generator | `python3 scripts/ci_gate_workflows.py --check` | rc 0 | `receipts/gates/ci_gate_workflows_check.*` |
| docs_check | `python3 -I scripts/docs_check.py` (pinned renderer) | rc 0: 0 findings across 210 md files and 1421 scrubbed text files | `receipts/gates/docs_check.*` |
| Doc style | `python3 -I scripts/check_doc_style.py`; `--selftest` | rc 0, rc 0: `documentation style: OK (23 current documents)` | `receipts/gates/check_doc_style*.*` |
| Em dash | `python3 -I scripts/check_em_dash.py --base 97aab1d0` (pinned renderer; base = merge-base of the head and live dev `5fcec84b`, as the workflow's pull_request arm computes it) | rc 0: 0 findings over 401 added lines in 18 changed pages, arms 339/339 | `receipts/gates/check_em_dash.*`, `em_dash_base.txt` |
| TOC | `python3 -I scripts/gen_toc.py --check`; `--verify-anchors` | rc 0, rc 0: 149 pages; 540 cross-page anchors reproduced | `receipts/gates/gen_toc_*` |
| F1 grep | `grep -rnE -- '--expect 17\|[0-9]+/17\b\|seventeen' docs/testing` | 4 lines, all historical or unrelated (see F1) | `receipts/f1-grep.txt` |
| Reach | `scripts/reach.sh <repo> 97aab1d0 865c2f9d` (changed SV sources, parent and processor `ed211803..f65c8ff7`, against non-comment Makefile lines, plus listed delegations) | see R1 | `receipts/reach.txt` |
| Figure set | `scripts/figures.py <repo> 97aab1d0 865c2f9d` and `9e57d4af 865c2f9d` | 15 suites changed since base; none since `9e57d4af` | `receipts/figures-*.txt` |
| Restore | rev-parse, porcelain including ignored files, `ls-files -s` digest against `ls-tree -r HEAD`, gitlinks | HEAD and tree as stated; 0 porcelain lines after removing my `scripts/__pycache__`; index digest equals the HEAD-tree digest; worktree equals HEAD. Gitlinks: processor `f65c8ff7`, gPTP `55680bff`, verilog-axis `48ff7a7e`, lwSRP `08ee86e8`, tsn-c-stack `70936b77`, external `efeb541a` (not initialised) | `receipts/restore_verify.txt` |

Note on the two `*_isolated-flag` receipts: my first runs of `ci_events.py --check` and `ci_gate_workflows.py --check` used `python3 -I`. That flag drops the script directory from `sys.path`, so both failed with `ModuleNotFoundError` on their sibling modules. The workflow runs them without `-I`, and run that way both are rc 0. The failed runs are kept for transparency. They are not a finding.

The pinned renderer was installed into a disposable venv from `tools/markdown/requirements.txt` with `--require-hashes`: `cmarkgfm==2025.10.22`, `html5lib==1.1` and their pinned dependencies, on CPython 3.14.8, the interpreter that file names for the recording host.

## Prior findings at their cause

### F1 (R725-4, MINOR, Docs): CLOSED

- `docs/testing/CI_WORKFLOWS.md:1506` now reads "`--expect 19` for Verilator, `--expect 4` for Yosys".
- This matches `.github/workflows/rtl.yml:622` (`--expect 19`) and `:867` (`--expect 4`).
- The F1 grep returns only four lines (`receipts/f1-grep.txt`):
  - `CI_WORKFLOWS.md:471` and `:561`: #781's history;
  - `:480`: run 40740015218's worker 6/17;
  - `TESTING.md:405`: the unrelated count of milan_dp commands.
- `ci_events.py --check` stays rc 0.

### R1 (R725-4, RESIDUE, Docs/Conformance): CLOSED

**The figure set.** At `CI_WORKFLOWS.md:479-486` and in the PR body's "Figures" bullet, the set is now described as "the suites of the ruled #799 replay": those whose Makefile compiles a source this PR changes, plus `maap`, `csr`, `nvm_backend` and `nvm_cosim`. `media_phase` keeps 1400 s, `milan_dp_gm_steps` keeps its higher 926 s, and `follow_ring` is at 1493 s. I checked that rule against my own re-derivation of the reach:

- `receipts/reach.txt` shows these suites name a changed source on a non-comment Makefile line: `aaf`, `aaf_audio_loop`, `capture_coherence`, `chmap_capture`, `follow_ring`, `mbx`, `media_phase`, `milan_dp`, `milan_dp_mclk`, `milan_dp_render` and `tdm`.
- Two more suites reach a changed source through `milan_dp`:
  - `pp_shadow` through `DP_SRCS := $(shell ... -C ../milan_dp print-srcs)` (`tb/verilator/pp_shadow/Makefile:108`);
  - `milan_dp_gm_steps` through `$(MAKE) -C ../milan_dp gmstep`.
- `maap`, `csr`, `nvm_backend` and `nvm_cosim` compile none of the changed sources (`KL_maap.sv`, `milan_csr.sv`, `KL_nvm_backend.sv`, and the processor NVM and ACMP-shadow files).
- `receipts/figures-97aab1d0-865c2f9d.txt` lists exactly 15 changed suites:
  - the reached suites, minus the two stated as kept (`media_phase`, `milan_dp_gm_steps`);
  - plus the four named re-measured suites;
  - with `follow_ring` at 1493 s.

The stated rule now describes the replaced set exactly.

**Other R1 points.**

- "lengthens" became "changes the windows of" (`:479`), which is consistent with `mbx` 82 -> 73.
- The source comment `suite_shards.py:76-77` uses the shortest form R725-4 prescribed. One residual inexactness in it is recorded as RES-C below. It is new wording residue, not a reopening of R1.

### R2 (R725-4, RESIDUE, Docs): CLOSED

`suite_shards.py:154` now reads: "#781 and #799 add three regular 45-minute workers; all 19, the dedicated last one too, carry the 122 s allowance." This is faithful to three sources:

- `rtl.yml:144`: `timeout-minutes: ${{ matrix.shard == 18 && 60 || 45 }}`, so index 18 is the 60-minute dedicated worker and 0-17 are regular.
- The base comment at `97aab1d0`: "#781: a seventeenth worker ... at the same 45-minute limit". So #781 added one regular worker, and #799 adds two.
- The table `WORKER_OVERHEAD_SECONDS = (122,) * 19`.

The line is 116 columns, and the idiom gate reports 0 over-long lines.

### Earlier findings (from R725-4's carried table), at this head

| ID | Origin | Status at `865c2f9d` |
|---|---|---|
| F1, F2 | R725-1/R726-1, R725-2 (MINOR, Docs) | Still resolved: `docs/design/` and `sw/` are not in the delta |
| R1, R2 (earlier) | R725-1, R726-1 (RESIDUE) | Still resolved: the delta's comments carry no issue-comment ID (`receipts/restore_verify.txt` scan), and the PR body still says `Closes #790` |
| R3 / RES-1 | R725-3, R726-2 (RESIDUE, Docs) | Retained for the residue checklist: `sw/mailbox/mailbox.yaml:65` is still 105 columns, and the file is not in the delta |
| RES-2 | R726-2 (RESIDUE, Docs) | **Reopened as RES-A**: the PR body's reproduction "expected state" again names a head other than the published one |
| S1, S3 | R725-1/R726-1, R726-2 (SUGGESTION) | Retained, optional, untouched |
| S2 | R725-2 | Superseded by R3/RES-1 |
| S4 | R725-4 (SUGGESTION, Tests) | Retained, optional: the allowance is unchanged and has no arm tying it to measured overhead |

### Does the delta reopen anything R725-4 found clean?

No.

- **Conformance, RTL, Robustness and Tests** were covered clean at `9e57d4af`. They depend on the planner tables, the generated workflow and the hosted windows, and none of those changed. This round ran the planner selftest, the generator check and the event contract again, and all are rc 0.
- **Docs:** the only Docs artifacts the delta touches are the two places that carried F1 and R1, plus the two comment lines.

## Findings (this round)

### RES-A - RESIDUE - Docs - PR #802 body, "How to get into the same state" - the expected head is the previous one

- **Authority/evidence:**
  - The "Status" section says the PR is ready at `865c2f9d82f2394b3453f36ccf92c49317a7fddd`.
  - The reproduction block runs `git rev-parse HEAD`, then states: "The expected state: ... head `9e57d4af1196a2e61f7e8010078c2c12b9b41587`".
  - R726-2's RES-2 asked for these two to agree, and R725-4 found them agreeing at `9e57d4af`.
- **Impact:** A reproducer at the published head sees a mismatch at step 2. This is wording only: no measurement, figure or verdict depends on it.
- **Exact fix:** Change the expected head to `865c2f9d82f2394b3453f36ccf92c49317a7fddd`, or name the current PR head generically.
- **Verification:** Both places in the PR body name the same SHA.

### RES-B - RESIDUE - Docs - PR #802 body, "Gates" table, the `9e57d4af` docs row - "below" should be "above"

- **Evidence:** The `9e57d4af` "Docs gates, GNU Make 4.3" row reads "as the `ca39dc1b` row below". The `ca39dc1b` docs row is the earlier row in the table (body line 132 against 140 in `receipts/pr802-body.md`).
- **Impact:** A reader looks in the wrong direction. Wording only.
- **Exact fix:** "as the `ca39dc1b` row above".
- **Verification:** Read the table order.

### RES-C - RESIDUE - Docs - `scripts/suite_shards.py:76` - the comment names one of the two kept figures

- **Evidence:**
  - The comment says "the ruled replay set (see CI_WORKFLOWS.md), except media_phase, carries its largest window in runs 40724689169 and 40740015218".
  - The page it points to (`CI_WORKFLOWS.md:485`) names two kept figures. `milan_dp_gm_steps` is also kept, at 926 s, above its largest window in those runs (696 s, per R725-4's measurement).
- **Impact:** Read alone, the comment says that `milan_dp_gm_steps`, a reached suite, carries a run window. Wording only: the figure is unchanged and is the conservative one.
- **Exact fix:** `#: #799: the ruled replay set (see CI_WORKFLOWS.md), except media_phase and milan_dp_gm_steps, carries its`. That is 107 columns, and the line count is unchanged.
- **Verification:** `check_py_idiom` stays rc 0 at 1000 lines.

### RES-D - RESIDUE - Docs - `docs/testing/CI_WORKFLOWS.md:483` - PR-relative wording in a durable page

- **Evidence:** "those whose Makefile compiles a source this PR changes". This is the page's only "this PR" (`grep -nE '\bthis PR\b'`). The surrounding paragraph says "the adoption" or "#799's" everywhere else. After merge, "this PR" has no referent on the page.
- **Impact:** A later reader cannot tell which change is meant without the history. Wording only.
- **Exact fix:** "those whose Makefile compiles a source the adoption changes", reflowed if wanted.
- **Verification:** The docs gates stay rc 0.

### S5 - SUGGESTION - Docs - PR #802 body, "Gates" table - no row at the published head

- **Evidence:** The newest gate rows are at `9e57d4af`. The `865c2f9d` delta touches the CI policy page, which `ci_events.py --check` reads, and two comment lines of an idiom-ratcheted module.
- **Status:** This round's receipts show those gates rc 0 at `865c2f9d`, so no claim is false.
- **Suggestion (optional):** Add a one-line row stating the gates re-run at `865c2f9d`, or say that the head differs from `9e57d4af` only in documentation and comments.

### Comment rule (delta source comments)

The two changed comment lines (`suite_shards.py:76`, `:154`) carry issue IDs (#781, #799), run IDs and a page name. They show no bench lane label, lane name, review round, reviewer ID or issue-comment ID. A pattern scan of the added lines is clean.

## Lenses applied this round

| Lens | Result | Evidence |
|---|---|---|
| Conformance | PASS | Closing refs: `Closes #790`, and #799 only "Relates to", with the stated reason. Ruling 6481160473, option B: no timeout, bound, allowance or check changed in the delta (`receipts/delta.stat`). The figure set equals the ruled replay set (`receipts/figures-97aab1d0-865c2f9d.txt` against `receipts/reach.txt`). `CI_WORKFLOWS.md:1506` matches `rtl.yml:622,867` |
| RTL | PASS | `receipts/delta.stat`: no `hdl/`, `tb/` or gitlink change. The `rtl.yml:144` timeout arm matches the new `suite_shards.py:154`. R725-3/R726-2 RTL coverage at ancestor `4f3ebffb`, re-banked by R725-4 at `9e57d4af`, stands, since nothing in scope was touched |
| Robustness | PASS | `receipts/figures-9e57d4af-865c2f9d.txt` is empty and the planner code is unchanged, so R725-4's capacity replay (0 of 19 workers at limit) still holds. The planner selftest is rc 0 at this head |
| Tests | PASS | No test or gate changed. `suite_shards.py --selftest`, `check_py_idiom.py --selftest` and `check_doc_style.py --selftest` are rc 0, and `ci_events.py --check` and `ci_gate_workflows.py --check` are rc 0 (`receipts/gates/`) |
| Docs | PASS | `CI_WORKFLOWS.md:477-495, 1500-1512`, `suite_shards.py:76-77, 154`, PR #802 body. F1, R1 and R2 are closed. `docs_check`, `check_doc_style`, `check_em_dash` (pinned renderer) and `gen_toc --check/--verify-anchors` are rc 0. RES-A to RES-D are residue only |

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | PR #802 body (Linked Issue, Figures, Workers); ruling issuecomment 6481160473; `receipts/figures-97aab1d0-865c2f9d.txt`; `receipts/reach.txt`; `CI_WORKFLOWS.md:1506` against `rtl.yml:622,867` | R725-5 | `865c2f9d82f2394b3453f36ccf92c49317a7fddd` |
| RTL | CLEAN | `receipts/delta.stat` (no `hdl/`, `tb/` or gitlink); `rtl.yml:144`; `suite_shards.py:154-155` | R725-5 (RTL artifacts last changed before `9e57d4af`; R725-4 coverage there carries) | `865c2f9d82f2394b3453f36ccf92c49317a7fddd` |
| Robustness | CLEAN | `receipts/figures-9e57d4af-865c2f9d.txt` (empty); `receipts/gates/suite_shards_selftest.log` | R725-5 | `865c2f9d82f2394b3453f36ccf92c49317a7fddd` |
| Tests | CLEAN | `receipts/gates/*selftest*`, `ci_events_check.log`, `ci_gate_workflows_check.log` | R725-5 | `865c2f9d82f2394b3453f36ccf92c49317a7fddd` |
| Docs | CLEAN | `docs/testing/CI_WORKFLOWS.md:466-495, 1500-1512`; `scripts/suite_shards.py:76-77, 154`; `receipts/pr802-body.md`; `receipts/f1-grep.txt`; `receipts/gates/docs_check.log`, `check_doc_style.log`, `check_em_dash.log`, `gen_toc_check.log` | R725-5 | `865c2f9d82f2394b3453f36ccf92c49317a7fddd` |

## Real limits

- **No Verilator suite, sweep, full docs workflow, builder leg or `behave` was run at this head.** The delta changes no simulated source and no test. For those, the author's `9e57d4af` receipts are the source-head evidence, and the head differs from `9e57d4af` only in one docs page and two comment lines.
- **No hosted results at this head.** When I checked, the hosted runs were all unfinished: rtl-full 40786271081 pending, docs 40786271316 in progress, rtl-fast 40786271055 queued, elaborate 40786271072 in progress (`receipts/hosted-runs-865c2f9d.json`). I claim no hosted result.
- **The reach mapping is approximate.** It matches Makefile source names and checked delegations (`milan_dp print-srcs`, `gmstep`). It is not a full include-graph extraction. `milan_dp_gm_steps`'s 696 s window is taken from R725-4's measurement and was not re-measured here.
- **No manager source bank exists at this head, and none is claimed.** Physical calibration was NOT RUN, and field skips are not hardware proof.

## Pending manager duties

- Hosted and act acceptance at this exact head, especially that rtl-full's 19 Verilator workers finish under their limits.
- The current-dev merge candidate (builder and native banks) at the merge turn, from source base `97aab1d0` onto live dev `5fcec84b`.
- Carry RES-A, RES-B, RES-C and RES-D, and the retained R3/RES-1, to the residue checklist.
- Confirm that keeping `milan_dp_gm_steps` at 926 s is intended (the R725-4 note; the page now states it explicitly).
- The pre-existing figure growth (`mmcm_servo`, `aaf_clock_meter`, `crf_rx`, `avtp_rxmon`) and #804 stay outside this PR, as ruled.

R725-5 FINISHED
