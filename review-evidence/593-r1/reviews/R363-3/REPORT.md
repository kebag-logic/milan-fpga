[R363] POSITIVE - exact head 7a051e618677ecd907ed04b086afbdfe374b4336

# R363-3: external independent re-review of PR #601 (issue #593)

- **Head:** `7a051e618677ecd907ed04b086afbdfe374b4336`, tree `11b049b34313cb1a23a0a4578e3d77086e5413e4`.
  - The round-3 delta is one commit on `68e801b2`. The PR has three commits on base `6d5ebd7357c1e468e446f18a61527c5be6118a04`.
  - All three commit messages are one line with no trailers (`receipts/diff_scope.txt`).
- **Scope reconstructed from:**
  - AGENTS.md, CONTRIBUTING.md and docs/README.md;
  - the #593 body, assignment 5858876858 and scope note 5858887057;
  - the round-2 assignment 5859221324 and the round-3 assignment 5859532913;
  - the #602 ruling 5859297355;
  - REQ-VER-06, TESTING 6d and GM_LOSS_RECOVERY.md;
  - then the diffs `6d5ebd73..7a051e61` and `68e801b2..7a051e61`, and the executor's public REVIEW READY 5859666788 and PR body.
- **Diff scope:** the delta touches 5 files: REQUIREMENTS.md, GM_LOSS_RECOVERY.md, TESTING.md, the planner and the mutation driver. The whole PR touches those plus the plan feature and its steps. No HDL, firmware, builder, `scripts/` or gitlink path changed (`receipts/diff_scope.txt`).
- **Verdict basis:** I applied all five lenses at this head.
  - Every round-3 item is met, and both of my round-2 findings are resolved.
  - No BLOCKER, MAJOR or MINOR is open. Four SUGGESTIONs follow; none affects coverage.

## Round-3 items at this head

| # | Item | Result | Evidence |
|---|---|---|---|
| 1a | `tu` uses the two-sided model. The 0.25 s minimum is decided only when `2R < 0.25 s`, and a clear at the GM instant always FAILs; otherwise NOT RUN | Met | Limit: `tb/tools/torture_campaign.py:3327-3328` (`0.25 / 2`), used by the single entry `:3578-3591` and the history `:3631-3635`. Minimum: `:3610`, `:3614` (`clear + R < GM + 0.25` FAILs). Probe P1: a true instant clear, observed anywhere in `[0, R]`, gives FAIL on both oracles over 132 values of R below 0.125 s, and never PASS. Probe P2a/P2b: over a ±R error grid, PASS implies `d >= 0.25 - 2R` and a minimum FAIL implies `d < 0.25` (`receipts/probe_properties.out`). Probe P4: R = 0.125, 0.2 and 0.25 give NOT RUN, even with an empty history. |
| 1b | The 0.5 s clear bound uses the same model; a PASS admits no true hold beyond 0.5 s + R | Met | `:3604-3606`, `:3616`: `clear + R <= last + 0.5 + R`, i.e. `h <= 0.5`. Probe P3: no PASS with `h + R > 0.5 + R` over the grid. P3b/P3c: at R = 0.1, h = 0.5 PASSes and h = 0.5000001 FAILs. P3d/P3e: measured from the last discontinuity. |
| 1c | One derivation, stated consistently in TESTING 6d, REQ-VER-06 and the assertion text | Met | REQUIREMENTS.md:305-314, TESTING.md:1024-1037 and the assertion text `:3425-3430` state the same chain: `h` within `d ± R`; minimum `h + R >= 0.25` gives `d >= 0.25 - 2R`; require `2R < 0.25`; limit 0.125 s with equality refused; upper `h + R <= 0.5 + R`, i.e. `h <= 0.5`, gives `d <= 0.5 + R`. There is no extra ceiling (REQUIREMENTS.md:313, TESTING.md:1032). The older sentences ("clears within 0.5 seconds plus stated observation resolution", `clear + R >= last_GM_change + 0.25`) agree with it. `latest_clear_s` and `deadline_s` are defined at TESTING.md:1036-1037 and match `:3604-3613`. |
| 1d | Self-tests on both sides of each boundary, and the limit pinned by a killed mutant | Met | `test_release_tu_two_sided_boundaries` (`:5768`) covers the 0.249/0.2/0.125 NOT RUN cases, 0.124/0.124999 FAIL, both sides of `h + R = 0.25`, and both sides of `h = 0.5` at three resolutions. `test_release_deciding_resolution` (`:5751`) covers 0.124999/0.125/0.125001. Driver mutant "tu resolution restored to one-sided limit" (`tb/tools/torture_release_mutants.py:527`) is killed. My mutants T1 (limit 0.1249), T2 (0.25), M11r, M29 and M30 are killed as well (`receipts/probe_mutants.tsv`, `receipts/r3_reanchored_mutants.txt`). |
| 2 | Every added check, both GM-history boundaries and every new assertion text pinned by a killed mutant; survivors listed | Met at check level (S1-S3 list the residual survivors) | Driver: 132/132 killed (`receipts/mutants.out`). GM-history boundaries `:3645`, `:3648-3649`: my round-2 M01 and M04 are now KILLED by `test_release_tu_history_boundaries` (`:5800`) (`receipts/r2_reviewer_mutants_at_r3head.txt`). Mechanical probe over every comparison operator and resolution term in the six `#593` oracle functions, every assertion fragment of both soak clauses, and 27 targeted mutants: 111 killed, 11 survived (`receipts/probe_mutants.tsv`). Every non-equivalent check is pinned by a killed removal mutant (`receipts/removal_probe.txt`). Each survivor is classified in S1-S4 (`receipts/witness_r3.txt`). |
| 3 | The #602 ruling is stated and cited; the text says plainly that the current image fails the step-only check until #602's RTL lands | Met | REQUIREMENTS.md:280-283, TESTING.md:936-939 and GM_LOSS_RECOVERY.md:155 link comment 5859297355. Each says the current image still toggles `mr` on a PHC step, so a soak containing one fails, until #602's RTL change lands. That claim is true at this head: `hdl/milan/milan_datapath.sv:3134-3137` still ORs `media_rebase_p_w` into `mcr_restart_p_w`. The oracle's `allowed` set (`:3690`) has no PHC or GM kind; round-2 mutant M17 (PHC accepted) is killed. |
| 4a | Reset wording fixed | Met | TESTING.md:969-974: a decrease is reported as a counter reset (Table 5.4 resets it at talker start), it fails the soak, and "Even an explained talker restart interrupts the continuous soak". This is consistent with REQUIREMENTS.md:278, the assertion text `:3402`, the `soak.continuous-duration` rule `:3376-3378` and the oracle's FAIL `:3718-3720`. |
| 4b | Every NOT RUN verdict records `resolution_limit_s` | Met | Limits now sit in `detail` before any return (`:3578-3580`, `:3630-3631`, `:3763-3768`). Probe P5 enumerates 45 paths: 16 single-interval `tu`, 12 history and 17 `mr`, covering every NOT RUN branch plus FAIL and PASS. Every one carries `resolution_limit_s` and `observation_resolution_s` (`receipts/probe_properties.out`). The pinning of this metadata is partial; see S1. |
| - | PR #586's arms and mutants still pass | Met | All 25 #586 mutants are present: 22 verbatim, and 3 re-anchored with the same named test. All are killed in the 132 run (`receipts/pr586_mutant_retention.txt`). All 54 #586-era tests are present. Six have changed since base (`receipts/pr586_test_retention.txt`); each change is a decided tightening or the SKIP→NOT RUN rename, and none is weakened. The delta's one #586 row change, (0.76, R = 0.01) PASS→FAIL, is the item-1b upper-bound decision. |
| - | No firmware, RTL or builder change | Met | `receipts/diff_scope.txt`; gitlinks equal at base and head (`receipts/clone_integrity.txt`). |

## Findings

No BLOCKER, MAJOR or MINOR finding.

**S1 - SUGGESTION - Tests - `tb/tools/torture_campaign.py:5816-5863` (`test_release_resolution_evidence`), `:3600`, `:3775-3776`, `:3784-3786` - the resolution-metadata contract is pinned on only some paths.**
- The test's docstring says "Every refusal path retains the measured resolution and deciding limit". It exercises 10 single-interval, 9 history and 6 `mr` refusals.
- Three mutants that strip `detail` survive the unchanged self-test (`receipts/probe_mutants.tsv` T22-T24; `receipts/witness_r3.txt`):
  - the uncorrelated-`tu` FAIL (`:3600`);
  - the `mr` invalid-record NOT RUN (`:3775-3776`);
  - the `mr` missing-capture-window NOT RUN (`:3784-3786`).
- The head is correct today (probe P5, 45/45), and no verdict changes. TESTING.md:955 and :1034 do promise the fields on every verdict.
- Suggested outcome: extend the test to those paths, or narrow its docstring.

**S2 - SUGGESTION - Tests, Robustness - `tb/tools/torture_campaign.py:3670`, `:3686` - two input-validation boundaries are unpinned. Each check itself is pinned by a killed removal mutant (`receipts/removal_probe.txt` R1, R3).**
- **T18 (`pdu_index < 0` → `< -1`).** A contiguous trace whose indices start at -1 moves from NOT RUN (head) to PASS (mutant). The grading of such a trace depends only on index differences, so the mutant's PASS is not unsound. It does accept a malformed record.
- **`:3686` (`<` → `<=`).** Equal consecutive PDU timestamps move from PASS (head) to NOT RUN (mutant). This is fail-safe.
- Neither can create a false release PASS on well-formed evidence. A one-line self-test row at each boundary would pin them.

**S3 - SUGGESTION - Tests - `tb/tools/torture_campaign.py:3645`, `:3793` - two defence-in-depth terms have no observable pin.**
- **`:3645` `clear_s <= start_s`.** Removing it, or flipping it to `<`, is verdict-equivalent: the nested `check_release_tu` refuses the same intervals, with 0 differences over 108 inputs.
- **`:3793` `capture_start_s >= capture_end_s`.**
  - The other span terms already force `start < end` unless the MEDIA_RESET reads run backwards by more than 1 s + R.
  - On such input the mutant changes NOT RUN to FAIL, and it can never reach PASS, because the unordered reads return NOT RUN.
- Listed for completeness under item 2. No change is needed.

**S4 - SUGGESTION - Tests, Docs - `tb/tools/torture_campaign.py:3407`, `:3419-3421` - four `soak.tu-within-holdover` fragments are unpinned. All of them predate this PR (PR #586 text).**
- The fragments are:
  - "; Milan v1.2 Annex B.1/B.1.1 / IEEE 1722-2016 4.4.4.7: ";
  - "implements 0.25-0.5 s; B.1's 5 s media-clock holdover is ";
  - "not a tu bound; ";
  - "periodic healthy samples alone cannot prove this; ". This PR only added the trailing "; ".
- Every fragment that this PR added to either soak clause is killed.
- Out of this PR's "new assertion text" scope. It could be a follow-up if the manager wants the whole clause pinned.

Observation, no finding: `docs/design/GM_LOSS_RECOVERY.md:156` (the Talker MEDIA_RESET row, "Counts that one toggle") still describes the #387 step-only MEDIA_RESET. The #602 ruling supersedes that, and its deliverable 2 names this row. The round-3 assignment scoped only the "Outgoing `mr`" row, which is correct.

## My round-2 findings at this head (R363-2, comment 5859530073)

| Finding | Status | Evidence |
|---|---|---|
| F1 MINOR: GM-history boundaries `:3640-3641`/`:3637` (old lines) unpinned | **Resolved** | M01 (drops the `start - R` allowance) and M04 (touching intervals) are KILLED by `test_release_tu_history_boundaries` (`receipts/r2_reviewer_mutants_at_r3head.txt`). Driver controls "history GM assignment drops start allowance / excludes start boundary / includes clear boundary" and "history accepts touching intervals" are killed. My rerun of all 28 round-2 mutants gives 24 killed and 4 anchor errors. The 4 are re-anchored as M07r, M11r, M13r and M28r, and all are killed (`receipts/r3_reanchored_mutants.txt`). |
| F2 MINOR: #602 text stale | **Resolved** | Item 3 above. |
| S1: early NOT RUN verdicts omit `resolution_limit_s` | **Resolved** (taken) | Probe P5 45/45. My round-2 residual probe now reports the limit present on both paths it flagged (`receipts/r2_residual_probe_at_r3head.txt`). The residual pinning gap is the new S1. |
| S2: the 0.25 s-limit minimum was failable, not tight | **Resolved by decision** | The manager adopted the two-sided model. My round-2 witness (R = 0.24 s, clear 10 ms after the GM change), which was PASS, is now NOT RUN. |

My round-2 probe rerun at this head meets 55/59 cases (`receipts/r2probe_at_r3head.txt`). The 4 unmet cases, I3a-I3d, carry the superseded round-2 limit `resolution_limit_s = 0.25`. Three of them already have the verdict the round-3 decision requires. I3b (R = 0.2499) is now NOT RUN, as the decision requires. The rest are unchanged.

I read the other reviewer's round-2 findings (R362-2, comment 5859529549) only after writing the verdict and ledger above. I rechecked each with my own equivalent probes and mutants, rebuilt from the public comment alone (`r362_2_recheck.py`, `receipts/r362_2_recheck.txt`):

| Finding | Status | Evidence |
|---|---|---|
| R362-2 F1 MINOR: `tu` limit did not decide the minimum | **Resolved** | I3e (R 0.249, clear 0.002), I3f (0.2, 0.06) and I3g (0.125, 0.13) are NOT RUN on both oracles. I3h (0.124, 0.124) is FAIL. A mutant restoring the 0.25 limit is killed (T2, M29, and driver `:527`). |
| R362-2 F2 MINOR: survivors C06, C07, C09, C10, C19, C34, C35, T05/T21, T13/T25 (and uncounted C38) | **Resolved** | All 12 of my equivalent mutants are KILLED by named tests. |
| R362-2 F3 MINOR: #602 text stale | **Resolved** | Item 3. |
| R362-2 S1: reset wording | **Resolved** | Item 4a (TESTING.md:973). |

The round-1 findings of both reviewers were resolved at round 2. They stay resolved: the rerun of my round-2 probe differs only in the superseded limit.

## Commands run at the exact head (foreground)

| Command | Result | Receipt |
|---|---|---|
| `python3 -B tb/tools/torture_campaign.py --self-test` | 78 tests OK, rc 0 | `receipts/selftest.err`, `receipts/selftest.rc` |
| `python3 -B tb/tools/torture_release_mutants.py` | 132/132 killed, source unchanged, rc 0 | `receipts/mutants.out`, `receipts/mutants.rc` |
| `python3 -B -m behave tests/features/torture_campaign_plan.feature -f progress` | 87 scenarios / 356 steps passed, rc 0 | `receipts/behave_plan.txt` |
| `python3 -B -m behave tests/features --tags=@torture -f progress` | 232 passed, 172 skipped, rc 0 | `receipts/behave_torture_tier.txt` |
| `git diff 6d5ebd73 7a051e61 --check`, `git diff 68e801b2 7a051e61 --check`, `docs_check.py`, `check_doc_style.py`, `check_doc_paths.py`, `check_feature_status.py --self-test`, `check_py_idiom.py`, `check_hygiene.py`, `check_todo_ownership.py` | rc 0 | `receipts/doc_gates.txt` |
| `check_em_dash.py --base 6d5ebd73`, `gen_toc.py --check`, `gen_toc.py --verify-anchors` | rc 2: cannot judge, because the pinned Markdown renderer is not installed. Substitute: no U+2013/U+2014 in added lines | `receipts/doc_gates.txt`, `receipts/emdash_substitute.txt` |
| `probe_properties.py` (P1-P6) | 61/61 met, rc 0 | `receipts/probe_properties.out`, `.rc` |
| `probe_mutants.py` (8 jobs) | 111 killed, 11 survived, all classified | `receipts/probe_mutants.tsv` |
| `witness_r3.py`, `removal_probe.py` | as cited in S1-S3 | `receipts/witness_r3.txt`, `receipts/removal_probe.txt` |
| `r2scripts/probe_r2.py`, `r2scripts/reviewer_mutants.py`, `r3_reanchored.py`, `r2scripts/residual_probe.py` | as tabled above | `receipts/r2*`, `receipts/r3_reanchored_mutants.txt` |
| #586 retention (inline comparisons of base vs head mutant tuples and test-method source) | 25/25 mutants; 54/54 tests present, none weakened | `receipts/pr586_*.txt` |
| `r362_2_recheck.py` (after verdict) | I3e-I3h met; 12/12 killed | `receipts/r362_2_recheck.txt` |
| `clone_integrity.sh` | clean | `receipts/clone_integrity.txt` |

## Ledger (reviewer-owned)

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Round-3 items 1-4 against `tb/tools/torture_campaign.py:3327-3328`, `:3568-3661`, `:3690`, `:3763-3776`, `:3826`. The #593 decisions, round-3 assignment 5859532913 and #602 ruling 5859297355 (IEEE 1722-2016 §4.4.4.3/§4.4.4.7, Milan v1.2 Annex B.1.1/B.1.2, Table 5.4). `receipts/probe_properties.out` (P1-P4), `receipts/r2probe_at_r3head.txt` | R363-3 | 7a051e618677ecd907ed04b086afbdfe374b4336 |
| RTL | CLEAN | `receipts/diff_scope.txt`: no HDL, firmware, builder, `scripts/` or gitlink change. `hdl/milan/milan_datapath.sv:3134-3137`: the RTL fact the new #602 text relies on ("current image still toggles") is true. The datapath change belongs to #602. | R363-3 | 7a051e618677ecd907ed04b086afbdfe374b4336 |
| Robustness | CLEAN | `check_release_tu`, `check_release_tu_history`, `_release_mr_records_valid`, `_release_mr_toggles`, `_release_media_resets`, `check_release_mr` (`:3568-3804`). Checked: None, NaN, inf, negative and coarse resolution at and around 0.125 s; zero-length, touching, malformed and unordered intervals; GM at start − R, at clear and uncovered; empty histories; negative and gapped PDU indices; short, silent and zero-length captures; unordered reads. Probe P5/P6 and `receipts/witness_r3.txt`. S2 is advisory. | R363-3 | 7a051e618677ecd907ed04b086afbdfe374b4336 |
| Tests | CLEAN | `test_release_tu_two_sided_boundaries` `:5768`, `test_release_tu_history_boundaries` `:5800`, `test_release_resolution_evidence` `:5816`, `test_release_deciding_resolution` `:5751`, `test_release_assertion_text` `:5474`, `test_release_mr_plan_contract` `:5686`, `test_release_mr_record_boundaries` `:5865`. `tb/tools/torture_release_mutants.py` (132/132). `receipts/probe_mutants.tsv`, `receipts/removal_probe.txt`, `receipts/r2_reviewer_mutants_at_r3head.txt`, `receipts/r3_reanchored_mutants.txt`, `receipts/pr586_*.txt`, `receipts/behave_*.txt`. S1-S4 are advisory. | R363-3 | 7a051e618677ecd907ed04b086afbdfe374b4336 |
| Docs | CLEAN | `REQUIREMENTS.md:262-318`, `docs/testing/TESTING.md:915-1062`, `docs/design/GM_LOSS_RECOVERY.md:147-157`, assertion texts `:3390-3430`, PR body Round 3. `receipts/doc_gates.txt`, `receipts/emdash_substitute.txt` | R363-3 | 7a051e618677ecd907ed04b086afbdfe374b4336 |

## Limits

- **Three documentation gates not run.** `check_em_dash.py` and `gen_toc.py --check`/`--verify-anchors` could not run, because the pinned Markdown renderer is absent and installs are not allowed. The substitute scan of added lines found no U+2013/U+2014. The executor reports rc 0 for all documentation gates at this head.
- **Public evidence packet.** The linked tree `59efc9fa` `review-evidence/593-r1` is the executor's round-1 packet at `95bea7cf`, committed 19:27Z. I found no published packet for `7a051e61`. The manager's source static/builder and native bank results at this head are taken from the assignment and are not independently located. My reruns above are the executable evidence I rely on.
- **Scope of runs.** Not run:
  - the full parent, PP, gPTP, Yosys and builder banks;
  - `ci_scope.py --selftest` and `check_baremetal_only.py`, which are the manager's bank;
  - Docker/act and the host runner;
  - hardware.

  The scoped simulator was not used, because no RTL changed.
- **Hosted checks, sampled 20:56:51Z** (`receipts/hosted_checks.txt`):
  - success: rtl-fast, verilator-lint, bdd-conformance, docs-check-no-git, full-ci-gate, yosys-elaboration, Yosys 0-3, Verilator 3, wire-accountability, changes;
  - in progress: docs-check, elaborate, Verilator 0, 1, 2 and 4;
  - skipped: "Physical gPTP". A skipped context is not execution evidence. The manager owns hosted/act acceptance.
- **Source validation only.** This is not the current-dev candidate, which the manager builds at the merge turn from live dev `8bc97021`. No physical calibration or bench evidence exists; field skips are not hardware proof.
- **Clone integrity.** After all probes, HEAD, tree and index-tree equal the stated head. There are no tracked blob or mode mismatches, and no untracked, ignored or flagged files. The four gitlinks equal base and head. `gptp-processor`, `protocol-processor` and `third_party/verilog-axis` are checked out at their gitlinks; `external` is not initialised (`receipts/clone_integrity.txt`).

## Pending manager duties

- Collect the second positive review and publish the completion ledger. A later commit inside any lens's scope un-covers that lens.
- Decide whether S1-S4 and the GM_LOSS_RECOVERY MEDIA_RESET-row observation (owned by #602) get follow-up work.
- Accept the hosted and act results at this head, including the in-progress Verilator shards and docs-check.
- Build and validate the current-dev candidate at the merge turn.
- Obtain explicit maintainer authorization before any merge.

R363-3 FINISHED
