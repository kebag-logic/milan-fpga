# [A839] CICD improvement — round 5 handoff

Status (2026-11-25 01:45 CET): STOPPED at the ruling's stop condition. The code is done, pushed and locally proved:
37/37 gate commands pass, and 8/9 planted budget defects are refused. The hosted proof is missing. Run 45514146494
at the head was cancelled before any Verilator worker finished, because rtl-fast's `firmware-boundary` reached its
30-minute limit on a runner at least 1.21× as slow, and the fail-fast watchers cancelled the head's runs. ETA:
needs a manager decision (re-run authorisation); a re-run then takes about 1 hour plus the report. Nothing of mine
is running.

**Head**

- milan-fpga `cicd-3` = `96df313f4e3d8a54b8378357645e744ea86c594c`, two commits on round 4's `45d5c35a`:
  - `feb03206`: follow_ring and media_phase as CI cases; follow_ring's two thread-printing drivers print in a
    fixed order;
  - `96df313f`: the 1276-second budget; `milan_dp` and `capture_coherence` at eight legs, `follow_ring` two,
    `media_phase` three; 26 workers; the figures.
- **Pushed** at 00:56 CET, only to trigger the hosted run. `push-privacy-check.py . 45d5c35a…` reported 0 private
  lines first. The command ran bare.
- No comments posted, no PR body edited, nothing merged, nothing re-run.

**Results**

1. **The ruling, applied.**
   - Every regular worker now projects 1199-1275 s against 1276 s (1800 / 1.41). The two heaviest have 1 s of
     margin.
   - Round 4's "five pieces" was six: it missed `media_phase` at 1400 s. `capture_coherence__1` also exceeded
     the budget with the allowance.
   - Each new piece's figure is its old leg's hosted figure times a measured local wall ratio. Every leg was
     measured, on 4-CPU bookings with hosted budgets and no compiler cache.
2. **Leg A (`milan_dp_mclk__0`) is the one worker over.**
   - It projects 1530 s (about 36 minutes on a 1.41× runner), and it is indivisible (#737).
   - Splitting `milan_dp_mclk` to eight legs was measured: only −7 %, still over, and four more builds. So
     `milan_dp_mclk` keeps four legs, and leg A keeps #737's exception.
3. **Verdicts.**
   - The five new pieces passed locally. Their combined verdict lines and counted tallies equal run 45481508309's
     whole-suite logs: `follow_ring` 97 checks, `media_phase` 386.
   - The serial runs are unchanged (`make -n run`).
   - The receipts of the other re-dealt suites could not be compared hosted (no worker finished).
4. **Runner-minutes.**
   - Before: 353.8 Verilator job-minutes (run 45481508309).
   - After: projected about 385 (+9 %). This is not measured.
5. **Gates.** 37 commands, all rc 0. Rounds 3 and 4 called the same 35-command list "36"; this round adds
   `check_sweep_shape.py` and `suite_tally.py --selftest`.

**For the manager**

- **Decision: re-run.** Authorise a re-run of run 45514146494 (or of all four runs of the head) to get the
  hosted proof. The cancelling job is `firmware-boundary`, not this change. It passed in 1304-1549 s in the last
  eleven rtl-fast runs, and was cut at 1819 s here. A re-run can draw a slow runner for it again.
- **Decision: leg A.** It cannot meet 30 minutes on a 1.41× runner by splitting. The options are to accept #737's
  exception as stated, or to open work to shorten the leg or move to a faster runner class.
- **Note: 26 workers queue.** They queue behind the head's other workflows when runners are scarce; 25 waited
  31 minutes tonight.
- **Note: `milan_dp__1` and worker 24's 1-second margins.** They rest on local ratios; their first hosted windows
  should replace the figures.

**Said plainly**

- The hosted run proves nothing about the new deal: one worker ran 14.7 minutes and was cancelled.
- The jobs API gives queued-then-cancelled jobs a `started_at` at queue time. My first table read them as
  30.9-minute jobs. They never ran; the saved table counts them as 0.
- Five fast gate commands (about 5 s) ran on CPUs of my own smoke arm while it measured `media_phase__2`.
- The smoke pieces ran before the print-order fix (the Makefiles equal the head's).
- Removals were logged to disk-cleanup.log before each `rm`: round 4's 3.2 GB of build clones, a stray
  `__pycache__` in the lane, a one-line log.

**Written:** REPORT.md, PR-BODY-1003.md (full replacement), receipts/INDEX.md (372 KB of text, no file over
200 KB). Scratch: /data-2/milan/tmp/cicd-a839/r5, 9.2 GB of 40 (whole lane directory).

STOP: hosted run 45514146494 at 96df313f was cancelled before any Verilator worker finished — rtl-fast's firmware-boundary exceeded its 30-minute limit on a runner at least 1.21x as slow (step cut at 1743 s against 1446 s), and the head's fail-fast watchers cancelled every run; a re-run needs authorisation
