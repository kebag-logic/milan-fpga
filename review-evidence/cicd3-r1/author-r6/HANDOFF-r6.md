# [A839] CICD improvement — round 6 handoff

Status (2026-11-25 04:10 CET): STOPPED at the ruling's stop condition, with the ruled work done and proved hosted.
`firmware-boundary` is split, and its three jobs took 13.2, 14.1 and 5.5 minutes hosted with the whole run's
verdict. All four runs at the head are green. But two other rtl-fast jobs still exceed 30 minutes on ordinary
runners. Neither is in the ruling: `firmware-control-mutants` took 38.8 min (factor 1.39) and `publication-census`
37.2 min (1.12). ETA: needs a manager decision on those jobs (finding 1) and on `milan_dp`'s two differing
receipts (finding 2). Nothing of mine is running.

**Head**

- milan-fpga `cicd-3` = `9c62539365fea8316dae2b9fd7c68defeff5cb31`, one commit on round 5's `96df313f`.
- **Pushed** at 02:50 CET, only to trigger the hosted run. `push-privacy-check.py . 96df313f…` reported 0
  private lines first, and the command ran bare.
- No re-run: all four runs passed on their first attempt. No comments posted, no PR body edited, nothing
  merged.

**Results**

1. **The ruling, applied** (`9c625393`).
   - `firmware-boundary`'s builders run in `firmware-boundary-capture`, two matrix legs, each under a capture of
     its own (`ctrl_boundary.py --leg K/2 --capture-out`, `ctrl_runs.LEGS`): leg 0 the control gate's build,
     leg 1 the other five builders.
   - `firmware-boundary` downloads both captures and judges them with the unchanged `--capture` path, with
     every control.
   - The aggregate requires the legs. `ci_events.py` pins both jobs, the matrix, the need and both 30-minute
     limits, with six new arms caught.
   - Projections by the workers' method: 921, 749 and 399 s, against 1276. The whole job projected 1765 s.
2. **Same verdict.**
   - Locally, a replica of the three jobs at one checkout path printed the whole step's lines, except the
     eight builder lines.
   - Hosted, the judge printed run 45481508222's counts (`4032 … of 4325`, 112/192/4 controls, `PASS`). It
     differs from that run only in the builder lines and a random sysroot name.
   - The judge given one leg's capture alone is refused by name.
3. **Hosted at the head** (runs 45528738040, 45528738009, 45528738049, 45528737977, all green).
   - Leg 0 took 13.2 min. Leg 1 took 14.1 min on a slow runner (1.54 × the median of the same builders).
     The judge took 5.5 min.
   - **Over 30 minutes:** `firmware-control-mutants` 38.8 (1.39 × its median, 0.99 × its slowest earlier
     window) and `publication-census` 37.2 (1.12 ×, 0.84 ×). The four watchers span their runs.
   - The slowest Verilator worker took 27.7 min (shard 1/26, 1.33 × its projection). The 26 workers took 389.0
     job-minutes (round 5 projected about 385). Leg A took 14.1 min.
4. **Runner-minutes (firmware-boundary).**
   - Before: 1461 s on average (1528 s at the previous head, 26 billed minutes).
   - After: 1968 s (+35 %, 35 billed minutes). At mean runner speed it would be 1630 s (+12 %). The family's
     wall span fell from 25.5 to 22.6 minutes.
5. **Gates.** 37/37 at the head in a clean clone. The `ci_events.py --selftest` ran 5967 arms.

**For the manager**

- **Decision: the other jobs over the bound** (REPORT §9.1). Over 60 runs these exceed 1276 s at their slowest:
  - rtl-fast: `publication-census` (2657 / mean 1922 s), `firmware-control-mutants` (2357 / 1841),
    `firmware-unit`, `firmware-aecp-mutants`, `firmware-srp-mutants`, `firmware-verilator`;
  - docs: `docs-gates-0`, `-2`;
  - elaborate: `elaborate-gates-1`, `-4`, `-0`.

  The first two exceed 30 minutes on ordinary runners. Rule which are in #1003's scope; each needs its own split.
  The watchers cannot fit 30 minutes by construction, so they need an explicit exception.
- **Decision: `milan_dp`'s `gptp` and `gptp-lat` receipts** (REPORT §6, §9.2).
  - Both pass. One diagnostic line changed between runs 45481508309 and 45528738040: `[#207] full-queue window:
    … rp 0->0, wp 1->1` became `rp 1->1, wp 2->2`.
  - Round 5's local 8-leg pieces printed the old value, so the cause is not established.
  - This blocks #998 acceptance 1 for that suite. It needs a task to reproduce it.
- **Note:** round 5's report missed most of the jobs in the first decision; I read only one rtl-full run's jobs
  then.

**Said plainly**

- One mistaken local check started a real leg-0 build in the lane checkout. I killed it within about a minute.
  Its bytecode was logged, then removed, and no tracked file changed.
- One misplaced artifact download (a `cd` that held for one of two parallel commands) wrote `new/` into the
  lane. I moved it out with `mv`. I ran `rmdir` on my own empty scratch directory to make room, and logged that
  only after doing it.
- `ci/image/tool-inventory.json` and `exec-audit-receipt.json` name firmware-boundary's old step indices. No
  hosted workflow checks them, and this host refuses the inventory check at the base head too.
- Not run: the act replay, the full serial sweep.

**Written:** REPORT.md (with every job's minutes in its appendix), PR-BODY-1003.md (full replacement),
receipts/INDEX.md (about 613 KB of text, no file over 200 KB). Scratch: /data-2/milan/tmp/cicd-a839, 9.9 GB of 40.

STOP: the hosted run at 9c625393 is green and firmware-boundary's three jobs fit (13.2, 14.1, 5.5 min), but two rtl-fast jobs outside the ruled split still exceed 30 minutes on ordinary runners — firmware-control-mutants 38.8 min (runner factor 1.39 against its median) and publication-census 37.2 min (1.12) — and milan_dp's gptp/gptp-lat receipts differ from the previous run (cause open)
