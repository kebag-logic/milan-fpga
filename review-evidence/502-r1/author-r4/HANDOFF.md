# Round 3 handoff

Issue: [#502](https://github.com/kebag-logic/milan-fpga/issues/502). PR: [#579](https://github.com/kebag-logic/milan-fpga/pull/579). Role: author.

Assignment: [round 3](https://github.com/kebag-logic/milan-fpga/issues/502#issuecomment-5854008765).

Commit: `867a2e38a4e3231545a0a24b97d1e5612a6659fe`. Parent: `5d4cf33e3709c35d4f5bc90d3c5a2334ef3bfd8e`.
Branch: `502-pending-live-write`. Exactly one new commit, with a one-line subject and no body or trailers.
Remote verified: `https://github.com/kebag-logic/milan-fpga.git`.

Status: all four assignment items addressed; all assigned gates return 0. Independent re-review remains required.

## Changes

| File:line | Change |
| --- | --- |
| `CHANGELOG.md:39` | Actual parent phase-5 writes raise pending; unchanged records raise nothing. |
| `docs/reference/SUBMODULES.md:61` | The parent's actual-write enable supplies the map trigger. |
| `docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md:1263` | The table reports pending from the first actual write. |
| `tb/verilator/pp_shadow/sim_main.cpp:1459` | Durable-baseline, two-record ADD refusal controls for both map directions; status 7, empty map, no live storage change and both pending bits clear. |
| `tb/verilator/pp_shadow/README.md:91` | Documents the partial-refusal controls. |
| `PR-BODY.md:41` (delivery file) | Full replacement body with Round 3, current evidence and the stale publication sentence removed. |

The commit changes five repository files. RTL, submodule pins and submodule sources are unchanged. `PR-BODY.md` is the separate replacement body for the manager.

## Finding table

| Finding | Reviewer severity and lenses | Resolution and evidence |
| --- | --- | --- |
| R328-2 F1 / R329-2 F1 | MINOR, Docs | Changelog and pin history identify the actual-write trigger. All documentation gates pass. |
| R328-2 S1 | SUGGESTION, Tests and Robustness | Committed partial-refusal controls kill P4 in both legs through named pending checks. |
| R328-2 S2 | SUGGESTION, Docs | Ownership row says actual write. Replacement PR body removes the stale sentence. |
| R329-2 S1 | SUGGESTION, Docs | Replacement PR body removes the stale publication sentence. |

These are author resolutions, awaiting reviewer acceptance. No review verdict or completion ledger is claimed.

## P4 result

The unchanged public `r328_2_dp_mutants.py` removes the phase-5 qualifier.
It runs against a `git archive` export of `867a2e38a4e3231545a0a24b97d1e5612a6659fe`.

| Leg | Result | Named committed checks |
| --- | --- | --- |
| Static output | KILLED, 2 failures | `K12 partial refusal input sticky_pending_PP_STAT` and `K12 partial refusal input sticky_pending_PP_NVM_STAT` |
| Dynamic output | KILLED, 4 failures | Both input checks above, plus `K12 partial refusal output sticky_pending_PP_STAT` and `K12 partial refusal output sticky_pending_PP_NVM_STAT` |

The default suite passes 591 + 591 + 591 + 295 checks, zero failures.
The unchanged multi-record reviewer probe passes 327 checks on shipping RTL. Its P4 run fails the named committed controls and the independent probe controls.

Both parent-pulse scripts cover 24 mutant legs. P1/D1 survive only where output edits are absent. P5, E1 and E2 remain expected equivalence controls. Every other applicable defect is killed. No build error or refused anchor counts as a kill.

## Gate table

Repository gates ran in `$LANES/502-pending-live-write`, in the foreground without pipelines. Verilator reports 5.052; a temporary wrapper only caps `-j 0` at eight jobs. Markdown checks use the hash-locked dependencies in `tools/markdown/requirements.txt`, installed under temporary storage.

| Command | rc | Result |
| --- | --- | --- |
| `make -C tb/verilator/pp_shadow` | 0 | 591 + 591 + 591 + 295 checks; 0 failures |
| `make -C tb/verilator/pp_shadow pending-mutant` | 0 | Clean control passes; late-mark mutant killed by K10/K12 |
| `python3 r328_2_dp_mutants.py <archive> <scratch> P4_no_phase5` | 0 | P4 killed in both legs |
| `python3 r328_2_dp_mutants.py <archive> <scratch> P1_in_only P2_out_only P3_unqualified P5_no_context P6_tied_low E1_no_beat E2_priority_dropped S1_shadow_ignores_input` | 0 | Remaining 16 legs as expected |
| `python3 r329_dp_mutants.py <archive> <scratch>` | 0 | Six legs as expected |
| `python3 r328_2_multirec_probe.py <archive> <scratch>` | 0 | Shipping control: 327 checks, 0 failures |
| `python3 r328_2_multirec_probe.py <archive> <scratch> <P4-datapath> P4` | 0 | Script succeeds; mutant simulation intentionally fails |
| `python3 scripts/lint_rtl.py --check` | 0 | Ratchet passes |
| `python3 scripts/measure_test_evidence.py --check` | 0 | Evidence ratchet passes |
| `python3 scripts/docs_check.py` | 0 | Git mode passes |
| `GIT_DIR=/dev/null python3 scripts/docs_check.py` | 0 | No-Git mode passes |
| `python3 scripts/check_em_dash.py --base 831f94f4` | 0 | Passes |
| `python3 scripts/check_doc_style.py` | 0 | Passes |
| `python3 scripts/gen_toc.py --check` | 0 | Passes |
| `python3 scripts/gen_toc.py --verify-anchors` | 0 | Passes |
| `python3 scripts/check_doc_paths.py` | 0 | Passes |
| `git diff --check` | 0 | Passes |
| `git diff --check 831f94f4 HEAD` | 0 | Passes |
| `git diff --check 5d4cf33e HEAD` | 0 | Passes |

## Reproduction and receipts

Scratch root: `/tmp/502-a349-eq2yv5on`. The archive is `archive/`; reviewer scripts are under `public/review-evidence/502-r1/reviews/`. The two parent-pulse campaigns write `r328-mutants/` and `r329-mutants/`; the probe writes `r328-probe/`. Exact commands and exit codes are retained in `reviewer-runs.json` and `gates.json` under scratch.

Public scripts were fetched from `502-review-evidence` at `f253e95decd2dfcaa1bc4a8ddff074c07bfa37e8`, extracted with `git show`, and run byte-for-byte unchanged. `reviewer-script-hashes.txt` records the public paths and SHA-256 digests, including the imported external reviewer helper.

The archive and its three required dependencies were exported from their exact commits. Isolated indexes support source-list queries; no additional checkout was used. All 911 parent blobs and all 566 dependency blobs match their archived commits. Mutants substitute copied RTL only; the archive's shipping sources remain unchanged.

Compact receipts accompany this handoff. Large build logs, binaries, tree exports and installed dependencies remain in temporary storage. Every delivery file is below 200 KB.

## Delivery and limits

The commit remains local and the working tree is clean. `PR-BODY.md` awaits manager application. The issue REVIEW READY comment is the final action. Independent re-review, publication, hosted validation and merge remain with the manager.

Round 3 reruns only the assigned gates. Full sweep, builder and synthesis figures in the replacement body are explicitly identified as round-2 evidence. No new hardware or timing evidence is claimed.
