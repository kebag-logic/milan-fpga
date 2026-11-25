# [A839] round 5 receipts (text only, no file over 200 KB)

Raw outputs, clones and builds stay in the lane's scratch, /data-2/milan/tmp/cicd-a839/r5/. Everything a reviewer
needs to re-check a figure in REPORT.md is here.

File formats:

- `time` lines are `/usr/bin/time` lines: wall, user and sys, then `rc=`.
- `start` and `end` are epoch seconds.
- `head` is the commit an arm ran.

| Path | What it holds | REPORT section |
|---|---|---|
| measure/progress.txt | Every timed arm, in completion order: arm letter, job, wall/user/sys, rc. Arms A/B on 24-31, C/D on 8-15, G/H on 56-63 | 2 |
| measure/times.txt | Per arm: head, start, end, time | 2 |
| measure/media_phase-case-spans.txt | Each `cases` case's log birth, modification and span in one `make -C tb/verilator/media_phase` | 2, 3.1 |
| smoke/times.txt, smoke/progress-*.txt | The five new pieces through `ci_suite_pieces.py run` (arms E on 0-3, F on 4-7), at the work-in-progress tree before the print-order fix | 2 |
| smoke/*.log, smoke/*.json | Those pieces' logs and case receipts | 2 |
| smoke/verdicts-vs-run-45481508309.txt | Their combined verdict lines and counted tallies against run 45481508309's whole-suite logs: IDENTICAL, SAME | 2 |
| determinism/settle-1.txt, settle-2.txt | `make settle-control` twice at the head: byte-identical | 3.1 |
| figures.txt | Every new piece's figure and its derivation (tools/figures.py) | 3.2 |
| deal-26.txt | The dealer at 26 workers: every worker's projection and pieces (tools/deal.py) | 4 |
| gates/summary-96df313f.txt, gates/tails-96df313f.txt, gates/*.log | The 37 gate commands at the head in a clean clone; the last lines of each log; three full logs | 6 |
| gates/summary-bf86e3cd-first.txt, gates/check_py_idiom-bf86e3cd-first.txt | The first gate run before the amend, with its idiom failure | 6 |
| gates/budget-plants.txt | Nine planted defects in the budget rule and figures (tools/budget_plants.py) | 6 |
| hosted/runs-96df313f.tsv | The four runs the push triggered, and their states | 7 |
| hosted/run-45514146494-jobs.txt | rtl-full at the head: every job's minutes from the jobs API (queued-then-cancelled jobs counted as never run) | 7 |
| hosted/sibling-runs-96df313f.txt | rtl-fast, elaborate and docs at the head: every job, its result and times | 7 |
| hosted/firmware-boundary-steps.txt | `firmware-boundary`'s steps in runs 45481508222, 45457005513 and 45514146566: the timed-out step against its two predecessors | 7 |
| hosted/shard-4-of-26-excerpt.txt, hosted/rtl-full-watcher-excerpt.txt | The one worker that ran (`capture_coherence__0`, cancelled) and the watcher's cancellation | 7 |
| hosted/runner-minutes-estimate.txt | Before (run 45481508309) and the projected after | 8 |
| tools/ | This round's scripts: meas.sh, meas-*.sh, piece_smoke.sh, smoke-all.sh, mkclone.sh, plan.py, deal.py, figures.py, fill_docs.py, budget_plants.py, gates.sh, hosted_fetch.sh, fetch_joblogs.sh, hosted_jobs5.py, hosted_compare5.py (used for the smoke verdicts), speed_index5.py (prepared for a complete run, unused) | all |
