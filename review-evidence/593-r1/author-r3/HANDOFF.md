# Round 3 handoff

Role: author [A384]. Issue #593, PR #601.
Status: assigned changes committed; all 35 required gates pass.
Head: `7a051e618677ecd907ed04b086afbdfe374b4336`.
Starting head: `68e801b2823f75e037152f7eb2ac4c5dcda5d919`.
Base: `6d5ebd7357c1e468e446f18a61527c5be6118a04`.
Branch: `593-mr-tu-soak`.
Remote verified: `https://github.com/kebag-logic/milan-fpga.git`.
Physical working directory: `$LANES/593-mr-tu-soak`.
Commit subject: `Tighten soak timing evidence and pin review boundaries`.
Independent re-review remains required; this handoff supplies evidence, not approval.

## Public contract

- [Issue and scope](https://github.com/kebag-logic/milan-fpga/issues/593)
- [Round 1 assignment](https://github.com/kebag-logic/milan-fpga/issues/593#issuecomment-5858876858)
- [Round 2 assignment](https://github.com/kebag-logic/milan-fpga/issues/593#issuecomment-5859221324)
- [Round 3 assignment](https://github.com/kebag-logic/milan-fpga/issues/593#issuecomment-5859532913)
- [Corrected mr/tu decision](https://github.com/kebag-logic/milan-fpga/issues/396#issuecomment-5857765949)
- [PHC-only ruling](https://github.com/kebag-logic/milan-fpga/issues/602#issuecomment-5859297355)
- [TAKEN](https://github.com/kebag-logic/milan-fpga/issues/593#issuecomment-5859541652)

Only the five assigned planner, mutation and documentation files changed in this
round. Firmware, RTL, builders and gitlinks are untouched. No push, PR edit,
merge, additional checkout or hardware operation was performed.
The current image still toggles mr on a PHC-only re-base. The gate rejects it;
#602 owns the RTL correction. Independent review and physical release evidence
remain separate obligations.

The cited PDF locations were read directly: IEEE 1722-2016 PDF pages 36-37
(4.4.4.3 and 4.4.4.7), Milan v1.2 PDF page 141 (Annex B.1.1/B.1.2),
and pages 40/44 (Tables 5.4/5.6). No standard extracts are included here.

## Assigned changes and proof

| Item | Change with file:line | Probe or mutation proving it | Result and receipt |
| --- | --- | --- | --- |
| F1: deciding tu resolution | `tb/tools/torture_campaign.py:3328`, `:3578`, `:3634`, `:3826` share the derived 0.125 s limit; equality is refused. `REQUIREMENTS.md:305`, `docs/testing/TESTING.md:1024`, assertion `tb/tools/torture_campaign.py:3425` state the two-sided derivation. | Internal I3e/I3f/I3g/I3h; `test_release_tu_two_sided_boundaries` at `:5768`; repository mutation `tu resolution restored to one-sided limit` at `tb/tools/torture_release_mutants.py:527`. | I3e/I3f/I3g NOT RUN, I3h FAIL. Below-limit instant-clear and both equality edges tested. Mutation KILLED. `round3-probes.log`, `gate-01.log`, `gate-02.log`. |
| F1: upper tu bound | `tb/tools/torture_campaign.py:3606`, `:3616` compares the latest possible true clear with the permitted true deadline. | `test_release_tu_two_sided_boundaries` tests observed holds 0.499999/0.5/0.500001 s at R=0, 0.001 and 0.124999 s, through both oracles. Mutations at `tb/tools/torture_release_mutants.py:531`, `:535`, `:539` remove the uncertainty term, exclude equality, or bypass the latest clear. | PASS/PASS/FAIL; all three mutations KILLED. `gate-01.log`, `gate-02.log`. The retained #586 deadline-resolution mutation is also KILLED. |
| F2: both GM assignment boundaries | Tests at `tb/tools/torture_campaign.py:5800` pin GM events at start-minus-R, inside that allowance, and at the previous interval's clear. Controls at `tb/tools/torture_release_mutants.py:556`, `:559`, `:562`. | Internal C06/C07 and S-C06/S-C07; external M01 and prior R1-M48h. | Short hold FAIL; next-interval assignment PASS. C06/C07/M01/R1-M48h KILLED. `internal-mutants.log`, `external-mutants.log`, `external-round1-reanchored.log`, `internal-witness-round3.log`. |
| F2: touching intervals | Test at `tb/tools/torture_campaign.py:5800`; mutation at `tb/tools/torture_release_mutants.py:565`. | Internal C09 and S-C09; external M04. | Touching intervals NOT RUN; separated intervals PASS. C09/M04 KILLED. Both review witness scripts distinguish pristine and mutant. |
| F2: negative history resolution and stated limit | Tests at `tb/tools/torture_campaign.py:5813`, `:5816`; controls at `tb/tools/torture_release_mutants.py:553`, `:568`. | Internal C10 and C19, with current anchors. | Negative resolution NOT RUN, including empty history; every tested verdict carries limit 0.125. Both KILLED. `review-reanchors-final.log`, `internal-witness-round3.log`. |
| F2: malformed mr evidence | `tb/tools/torture_campaign.py:5877` tests an empty stream ID and negative PDU indices. Controls at `tb/tools/torture_release_mutants.py:577`, `:580`. | Internal C34/C35 and S-C34/S-C35. | Both NOT RUN; both mutations KILLED. `internal-mutants.log`, `internal-witness-round3.log`. |
| F2: assertion text and prior key tokens | `tb/tools/torture_campaign.py:5474`, `:5686` pin full cause-window, mapping, missing-evidence, PHC/fabric and timing-derivation phrases. Matching controls at `tb/tools/torture_release_mutants.py:586`. | Internal T05/T21 (two-sided mr window), T13/T25 (PHC/fabric examples), all other internal text deletions and replacements; repository derivation-text mutants. | Every applied text mutation KILLED. `gate-02.log`, `review-reanchors-final.log`, `internal-witness-round3.log`. |
| F3: settled PHC-only ruling | `REQUIREMENTS.md:280`, `docs/testing/TESTING.md:936`, `docs/design/GM_LOSS_RECOVERY.md:155` cite ruling 5859297355, exclude PHC-only causes and state the current-image failure until #602's RTL change lands. | Both review F3/F2 documentation findings; internal I6 probes and external M17 reverse the permitted-cause rule. | Five PHC/GM cause kinds FAIL; M17 KILLED. `internal-probe.log`, `external-mutants.log`; documentation gates below all rc 0. |
| Taken reset wording suggestion | `docs/testing/TESTING.md:973` explains that even an explained talker restart interrupts the continuous soak. | Internal S1; existing I7d/I7e reset probes and C27/C28 reset mutations. | Resets FAIL as before; mutations KILLED. `internal-probe.log`, `internal-mutants.log`; doc-style gate rc 0. |
| Taken NOT RUN metadata suggestion | `tb/tools/torture_campaign.py:3578`, `:3630`, `:3764` construct `resolution_limit_s` before any refusal. `test_release_resolution_evidence` at `:5816` covers missing, nonfinite, negative, coarse, invalid and incomplete inputs. | External S1 residual probe; internal C17/C18/C19 with current metadata anchors; three repository metadata-removal mutations. | Both early-refusal residual cases retain their limit. All metadata mutations KILLED. `external-residual.log`, `gate-02.log`, `review-reanchors-final.log`. |

For observed hold h and true hold d, `h` lies within `d +/- R`.
The adopted minimum remains `h + R >= 0.25`, which certifies
`d >= 0.25 - 2R`; therefore `2R < 0.25` rejects any instant clear.
The upper check is `h + R <= 0.5 + R`, equivalent to `h <= 0.5`.
It cannot admit a true hold beyond `0.5 + R`. No practical ceiling was added.

One existing #586 test expectation is deliberately tightened by round 3:
a clear at 0.76 s following the last event at 0.25 s, with R=0.01,
now FAILs; it could represent a true hold of 0.52 s. The 0.75 s boundary
passes. Every #586 test method remains, and its 25 mutations remain present
and killed. `base-mutants-retained.log` reports 22 verbatim and three previously
re-anchored controls, zero lost.

## Review packet results and limits

The input packets under `$REVIEWS/593-r362-2-packet` and
`$REVIEWS/593-r363-2-packet` remained read-only. Mutation copies
live only under temporary scratch directories, outside this output directory.

- Unchanged internal round-2 driver: 54 KILLED, zero survivors, 13 invalid
  anchors. Unchanged external round-2 driver: 24 KILLED, zero survivors,
  four invalid anchors. Invalid anchors are not counted as kills.
- The external prior-round re-anchor driver reports 7/7 killed, including R1-M48h.
- `review_reanchors.py` retains review input mutations, updates the moved
  limit/metadata anchors, and restricts replacements to production text.
  This avoids changing assertions whose phrases also occur in tests.
  Exact old/new strings and named failures are retained in
  `review-reanchors.json`. Final result: 103 named KILLED, one CRASH-ONLY,
  zero surviving verdict mutations; rc 0 (`review-reanchors-final.log`).
- One old mutation, R1-M01r, removes the empty-match guard and then indexes
  `matches[0]`. It produces IndexError instead of a verdict. This is a
  CRASH-ONLY detection, not a named behavioral kill. The verdict-preserving
  R1-M01r-safe replacement accepts the uncaused toggle without that crash;
  R1-M01r-safe is KILLED by `test_release_mr_no_cause`;
  the repository's `mr uncorrelated toggle accepted` control is also KILLED.
- The unchanged internal probe prints four mismatches solely because it
  retains round-2 expectations at coarse resolutions: I3e/I3f/I3g expect
  FAIL and I3i expects PASS; all four now give NOT RUN as round 3 requires.
  The unchanged external probe reports I3a/I3c/I3d's old 0.25 s metadata
  and I3b's old accepted coarse resolution as mismatches.
  `round3_probes.py` grades those same inputs under the recorded ruling:
  internal 41/41, external 59/59, rc 0. Its overrides are explicitly listed.
- The internal witness script uses equivalent current anchors and distinguishes
  all eight original witness inputs. Its five text controls are killed.
  External witnesses distinguish M01 and M04 at this head.
- Earlier unassigned suggestions about counter under-counting and omitted GM
  provenance remain as recorded in `external-residual.log`. This assignment
  does not change their acceptance criteria.

Raw probe return codes and anchor errors are preserved in `reviews.json`.
They are not substituted for required gates. Early `pre-*` logs record
implementation checks, not committed-head qualification.

## Gate table

Every command below ran unpiped, in the foreground, from the physical working
directory above at `7a051e618677ecd907ed04b086afbdfe374b4336`. Every rc is 0.
`run_gates.py` invokes commands through `rtk proxy` with 1800-second limits.
Its environment sets `PYTHONDONTWRITEBYTECODE=1` and
`PYTHONPATH=/tmp/milan-593-markdown` for the existing pinned Markdown dependencies.
`gates.json` records command, working directory, exact head, rc, duration,
output size and SHA-256. No packages or toolchains are stored in this packet.

| Command (after `rtk proxy`) | Result | Receipt |
| --- | --- | --- |
| `python3 -B tb/tools/torture_campaign.py --self-test` | rc 0; 78 tests | [gate-01.log](gate-01.log) |
| `python3 -B tb/tools/torture_release_mutants.py` | rc 0; 132 KILLED | [gate-02.log](gate-02.log) |
| `python3 -B -m behave tests/features/torture_campaign_plan.feature -f progress` | rc 0; 87 scenarios | [gate-03.log](gate-03.log) |
| `python3 -B -m behave tests/features --tags=@torture -f progress` | rc 0; 232 scenarios, 172 out-of-tier skipped | [gate-04.log](gate-04.log) |
| `python3 scripts/ci_scope.py --selftest` | rc 0 | [gate-05.log](gate-05.log) |
| `python3 scripts/check_baremetal_only.py --check` | rc 0 | [gate-06.log](gate-06.log) |
| `python3 scripts/check_baremetal_only.py --selftest` | rc 0 | [gate-07.log](gate-07.log) |
| `git diff --check` | rc 0 | [gate-08.log](gate-08.log) |
| `git diff 6d5ebd7357c1e468e446f18a61527c5be6118a04 HEAD --check` | rc 0 | [gate-09.log](gate-09.log) |
| `python3 scripts/docs_check.py` | rc 0 | [gate-10.log](gate-10.log) |
| `python3 scripts/check_em_dash.py --base 6d5ebd7357c1e468e446f18a61527c5be6118a04` | rc 0 | [gate-11.log](gate-11.log) |
| `python3 scripts/check_em_dash.py --selftest` | rc 0 | [gate-12.log](gate-12.log) |
| `python3 scripts/check_doc_style.py` | rc 0 | [gate-13.log](gate-13.log) |
| `python3 scripts/check_doc_style.py --selftest` | rc 0 | [gate-14.log](gate-14.log) |
| `python3 scripts/check_feature_status.py --self-test` | rc 0 | [gate-15.log](gate-15.log) |
| `python3 scripts/check_doc_paths.py` | rc 0 | [gate-16.log](gate-16.log) |
| `python3 scripts/check_archive.py` | rc 0 | [gate-17.log](gate-17.log) |
| `python3 scripts/check_archive.py --selftest` | rc 0 | [gate-18.log](gate-18.log) |
| `python3 scripts/gen_toc.py --selftest` | rc 0 | [gate-19.log](gate-19.log) |
| `python3 scripts/gen_toc.py --verify-anchors` | rc 0 | [gate-20.log](gate-20.log) |
| `python3 scripts/gen_toc.py --check` | rc 0 | [gate-21.log](gate-21.log) |
| `python3 scripts/check_gptp_docs.py --with-submodule` | rc 0 | [gate-22.log](gate-22.log) |
| `python3 scripts/check_gptp_docs.py --selftest` | rc 0 | [gate-23.log](gate-23.log) |
| `python3 scripts/check_solution_docs.py` | rc 0 | [gate-24.log](gate-24.log) |
| `python3 scripts/check_solution_docs.py --selftest` | rc 0 | [gate-25.log](gate-25.log) |
| `python3 scripts/check_submodule_docs.py` | rc 0 | [gate-26.log](gate-26.log) |
| `python3 scripts/check_submodule_docs.py --selftest` | rc 0 | [gate-27.log](gate-27.log) |
| `python3 scripts/check_py_idiom.py` | rc 0 | [gate-28.log](gate-28.log) |
| `python3 scripts/check_py_idiom.py --selftest` | rc 0 | [gate-29.log](gate-29.log) |
| `python3 scripts/check_hygiene.py --check` | rc 0 | [gate-30.log](gate-30.log) |
| `python3 scripts/check_hygiene.py --selftest` | rc 0 | [gate-31.log](gate-31.log) |
| `python3 scripts/check_todo_ownership.py` | rc 0 | [gate-32.log](gate-32.log) |
| `python3 scripts/check_todo_ownership.py --selftest` | rc 0 | [gate-33.log](gate-33.log) |
| `python3 docs/traceability/gen_module_matrix.py --check` | rc 0 | [gate-34.log](gate-34.log) |
| `python3 -B tb/tools/torture_campaign.py --coverage-by-area --areas soak,power` | rc 0 | [gate-35.log](gate-35.log) |

## Handoff state

The assigned desk implementation and required gates are complete.
The PR body file is prepared locally for the maintainer.
Independent re-review, publication, hosted/local workflow acceptance and merge
remain with the maintainer. No release campaign or physical pass is claimed.
The prepared REVIEW READY comment names this exact local head.
The author stops after publishing it; the branch remains local.
