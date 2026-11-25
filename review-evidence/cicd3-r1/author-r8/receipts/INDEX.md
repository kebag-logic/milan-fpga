# Round 8 receipts (#1003, head `b0f2bc1a784d9f006204491c883ac2b1783e970a`)

About 1.2 MB in total. Most of it is the 37 gate logs and the piece logs.

## Where the local runs ran

- The host is the 96-vCPU VM. Builds used the shared compiler cache.
- follow_ring pieces: CPUs 48-55, booked with `cpu_ranges.py pick`, in unit `milan-cicd-a839j-frpiece`.
- Gates: the session pool, CPUs 80-95, in unit `milan-cicd-a839j-gates`, because no other range was free.
- Hosted poll: unit `milan-cicd-a839j-poll`.

## gates/

- `summary`: the 37 commands at `b0f2bc1a` in a clean clone (`r8/wt/gates`), each with rc, seconds and the last line of
  its log. All are rc 0.
- `<name>.log`: each command's full output.
- `ci_events_selftest.log` lines 2866-2872: the seven boundary-leg arms, all caught.

## probe/

- `at-9c625393.txt`: R923-2's make probe, unmodified, at the old head. It reproduces the finding: head 1 warning, `make
  -n run` DIFFERS.
- `at-222362ff47.txt`: the probe at the fix commit: IDENTICAL, 0 warnings.
- `final-b0f2bc1a78.txt`: the probe at the head under make 4.4.1 (`--jobserver-style=pipe`) and make 4.3, IDENTICAL and
  0 warnings under both. It ends with both `make -n run` digests.
- `make43.txt`: the make 4.3 probe at `9c625393` (head 1 warning, DIFFERS) and at `222362ff` (0, IDENTICAL).
- `at-*/`, `make43-*/`: each probe's `make-n-run.{base,head}.txt` and `small-pullin-{pipe,make43}.{base,head}.txt`.
- `plant.txt`: the three planted disabled-cancellation configurations and the contract checks' verdicts on each.
- `r924-probe-at-b0f2bc1a78.txt`: R924-2's `probe_cancellation.py`, unchanged, failing at the head as expected (rc 1).
- `r8-probe-at-b0f2bc1a78.txt`: the inverse probe passing, with both planted findings quoted.

## local/

- `fr-fr/`, `fr-old/`: follow_ring's two CI pieces at `b0f2bc1a` and at `9c625393`. Each holds the receipt, log and
  `/usr/bin/time` line for both pieces, and `head`.
- `follow_ring-receipts.txt`: the three case receipts. They are equal in both trees and equal to hosted run
  45528738040's.
- `progress`: the unit's own summary lines.

## hosted/

- `runs.txt`: the four runs at the head, their job count and the set of job states.
- `merge-c5327b25.txt`: the merge the runs tested. Its parents are `e608f8d8` and `b0f2bc1a`.
- `compare-45528738040-vs-45550366428.txt`: every suite's receipts and verdict lines, against the previous head's
  rtl-full on the same base. 8/8 and 65/65 are identical.
- `minutes-b0f2bc1a.tsv`: every job's seconds and minutes, with factors against 64 earlier runs. A job over 1800 s is
  marked `OVER`.
- `workers-vs-projection.txt`: the 26 workers against round 5's projections, with the previous head's seconds.
- `verilator-cache-miss.txt`: the jobs that built Verilator or Yosys from source at this head.
- `judge-45550366444-verdict.txt`: `firmware-boundary`'s `ctrl_boundary` lines.
- `status.log`: the poll's minute-by-minute run states.

## tools/

- `follow_ring_make_probe.reviewer-original.sh`: R923-2's probe as published, sha256 `7f72a73f…`.
- `follow_ring_make_probe.sh`: the same probe, with its head list taken from `PROBE_REVS` (a one-line diff).
- `follow_ring_make_probe_make43.sh`: the make 4.3 variant, without `--jobserver-style=pipe`.
- `probe_cancellation_r8.py`: the inverse of R924-2's cancellation probe.
- `frpiece.sh`: the piece runner.
- `gates.sh`: round 6's gate list, pointed at r8.
- `mkclone.sh`: the shared clone at a given revision.
- `env.sh`: the environment.
- `poll.sh`: the hosted poll.
