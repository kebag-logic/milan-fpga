# Round 6 receipts (#1003, head `9c62539365fea8316dae2b9fd7c68defeff5cb31`)

About 613 KB of text in total; no file is over 200 KB (the largest is the hosted judge's log, 140 KB). Local runs
were on the 96-vCPU VM in the session pool 64-95 (no `cpu_ranges.py pick` range was free), with hosted budgets
and no compiler cache.

## hosted/

- `all-jobs-60-runs.txt`: every hosted job's slowest and mean window, and how often it exceeded 1276 s, over the
  successful jobs of the 60 successful runs among the last 120 (collected 01:4x CET). It is the source of
  REPORT §9 finding 1.
- `fb-phases.tsv`: the fourteen `firmware-boundary` jobs of runs 45147231523-45481508222, phase by phase, read
  from each log (each builder's seconds, the builders' span, images, judgement, the step, the job).
- `figures-1003.txt`: the three new jobs' figures and projections from those phases.
- `whole-step-45481508222.log`: the last complete whole-step hosted log, with escape codes stripped.
- `run-9c625393/`, the four runs at the head:
  - `all-jobs-table.tsv`: every job of the four runs (84), with minutes and factors.
  - `capture-0.log`, `capture-1.log`, `judge.log`: the three new jobs' hosted logs.
  - `hosted-whole-vs-judge.diff`: the judge's step output against 45481508222's, normalised.
  - `runner-minutes.txt`: firmware-boundary before and after.
  - `workers-vs-projection.txt`: the 26 Verilator workers against round 5's deal.
  - `suite-compare-45481508309-vs-45528738040.txt`: round 5's comparison tool over both runs' suite logs.
  - `milan_dp-gptp*.old/new.txt`: the two differing case outputs.
  - `status.log`: the poller's minute-by-minute run states.

## local/

- The whole step at `96df313f` (`base.*`, 1893 s). The replica at `6a8260e3`: `s1-leg0.*` 901 s, `s1-leg1.*`
  671 s, `s1-judge.*` 336 s. `*.size` holds each capture's bytes (as made, and after the artifact-like copy) and
  its file count.
- `whole-vs-judge.diff`: the normalised comparison. Its only difference is the eight builder lines.
- `s1-judge-leg0-only.*`: the judge given leg 0's capture alone. It exits 2 and names leg 1's builders.

## negative/

Each `--leg` refusal (`leg-*.log`, `out-*.log`, exit 2), and `leg-builders.log`, which holds the leg assignment
and the stray-name and empty-leg refusals. `leg-no-rv32.log` is the mistaken run of REPORT §8, which was killed;
it is not a refusal.

## gates/

- `summary-9c625393.txt`: 37 commands, all rc 0, at the head in a clean clone.
- `summary-04eb7f9b-first.txt`: the first run before the amend, with `check_py_idiom` rc 1 (`check_py_idiom.log`).
- `ci_events-selftest-new-arms.txt`: the new arms of the self-test and its final line.

## tools/

The scripts these came from:

- `fbrun.sh`, `splitrun.sh`, `mkclone.sh`, `gates.sh`: the local arms;
- `jobdur.sh`, `fbphases.py`, `poll.sh`, `hostedtable.py`: the hosted data;
- `prbody.py`, `pr-hosted.md`, `section.md`: the PR body and report sections;
- `hosted_compare5.py.from-round5`: round 5's tool, unchanged.
