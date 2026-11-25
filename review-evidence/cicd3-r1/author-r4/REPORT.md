# [A839] CICD improvement, round 4: the staging lock domain, shard 1's minutes, and the engine passes as make jobs

**Summary.** Two PRs, one branch each, nothing of mine pushed except `cicd-3` to trigger its hosted run (privacy
check passed, recorded below).

| # | Item | Result | Commit |
|---:|---|---|---|
| 1 | #1003: one lock domain per staging slot; stage root proved | The lock is the slot directory's own inode, so any TMPDIR, alias or user meets one lock. The root is proved (owner, mode, no link, inside the resolved base, atomic `mkdir`) or refused with its reason. 17 self-test controls, six with independent processes; 10/10 planted defects caught; both reviewers' collisions reproduced at the previous head and gone at this one; five drivers' logs identical, warm hits 100 %. | `d95e95e8` |
| 2 | #1003: shard 1's 38.6 min | **Runner speed.** Same-host A/B: the head ran shard 1's pieces faster than the base at equal instructions. Hosted: the same suites' identical builds took 1.36-1.41× as long. Shard 1 was the heaviest worker even at the base because of a stale figure: `milan_dp` leg 1 measured 995 s against 508. Figures re-keyed from two complete hosted runs; shard 1 16.1 min at the head. **Open:** shard 17 ran 30.7 min on a 1.41× runner (decision for the owner). | `59f4f478`, `45d5c35a` |
| 3 | FPGA-gPTP #112: honour the caller's job budget | Each pass is a make job; `run` replays them from four `run::` rules, so make's own messages, `-s`, `-i`, `-k` and signal names are the serial run's. Fail-fast and QUIT taken. `passes-test` (63 checks) in `all`; 9/9 planted defects caught. Real harness: 453 → 221 s and 653 → 221 s at `-j4` in two concurrent pairs, `-j1` the serial time; transcripts IDENTICAL at matching flags. | `661e4c3` |
| 4 | Proof sets at the new heads | #1003: 36/36 gates in a clean clone; hosted run green, receipts 24/24 and verdict sets 83/83 identical to both earlier runs. FPGA-gPTP: `make docs`, `make lint`, `passes-test`, real-harness clean and planted-abort pairs. | — |

Heads: milan-fpga `cicd-3` = `45d5c35a4470057966a72c0e85e49af1921152a0` (six commits on PR #1001's `fcbc31f3`);
FPGA-gPTP `engine-run-passes-at-once` = `661e4c3a45904d2d8f3e061c67103a945651d9ff` (two commits on main `1213ac5`),
in /data-2/milan/tmp/cicd-a839/r3/fpga-gptp, not pushed.

Host: AMD EPYC 9554P VM, 96 vCPU (siblings 2k, 2k+1), load 57-92 this round. `cpu_ranges.py pick` found no free
range all evening (0-63 booked by other units), so every arm ran in the session pool 64-95 on CPUs named in each
receipt, as round 3 did when no range was free. Pinned Verilator 5.050, g++ 16.2.1, ccache 4.14.1 (the shared
cache only; `CCACHE_DIR` never set), GNU make 4.4.1. Long runs were this session's `milan-cicd-a839f-*` units,
polled from the foreground; none is left running.

## 1. One lock domain, a proved root (`d95e95e8`, R924-1-F1, R923-1-F1)

### 1.1 What changed (`scripts/mutant_stage.py`, TESTING.md)

- **The lock is the slot.**
  - A holder `mkdir`s the slot (0700) if it is absent and `lstat`s it.
  - It opens the directory with `O_DIRECTORY|O_NOFOLLOW` and takes `flock(LOCK_EX|LOCK_NB)` on that inode.
  - It then re-checks that the path still names that inode. If the previous holder removed it meanwhile, it
    retries.

  Every caller that names one physical directory, through any TMPDIR, any spelling of the parent or any user,
  meets the same lock. The round-3 lock files lived under a TMPDIR- and uid-named directory and were keyed by the
  path string: that was both findings.
- **Slots.**
  - A slot `lstat`s as another user's: it is never touched, and the next slot is tried.
  - A file or link in a slot's name, left by this user: it is unlinked.
  - A taken slot is emptied entry by entry, following no link.
- **The root.**
  - It is `<realpath(TMPDIR)>/milan-mutant-stage-<uid>`, created by one `os.mkdir(root, 0o700)`.
  - It is then checked by `lstat`: a directory, not a link, owned by the caller, with no group or other write. It
    is opened `O_NOFOLLOW`, and `fstat` against `lstat` and `realpath(root) == root` rule out a swap.
  - The resolved TMPDIR must be owned by the caller or root, and sticky if others may write it.
  - A root that fails is refused, and the reason goes to stderr. The driver then stages at `tempfile.mkdtemp`, as
    the base did: correct and cold, with no CCACHE_BASEDIR set.
  - An earlier 0755 root (round 3 created them so) is tightened to 0700 through the open descriptor.
- **The docs.** The docstring and TESTING.md say all this, cite Issue #998 / REQ-VER-01 / REQ-VER-04
  (R924-1-R1), and name the in-tree `milan_dp` drivers' path (R923-1-R1).

### 1.2 Controls and evidence

| Evidence | Result | Receipt |
|---|---|---|
| `--selftest` at the head | 17 controls PASS, 0.7 s. Six use independent holder processes that all hold at once: six drivers racing for one slot; two in-tree drivers under different TMPDIRs; a TMPDIR and a link to it, and a parent and a link to it; another user's live slot (holder sees itself as another uid). Root controls: symbolic link, mode 0777, a file, a foreign owner (a root in the sticky, root-owned `/tmp`, holder as an unused uid), a non-sticky world-writable TMPDIR, an earlier 0755 root holding a `locks` file. | staging/selftest-45d5c35a.txt |
| Each control can fail | 10 planted defects, each removing one protection, each fails `--selftest`. Among them: the round-3 lock domain (the TMPDIR/uid-named lock files), TMPDIR not resolved, a foreign slot taken, each root check removed, emptying that follows a link. | staging/selftest-plants.txt |
| The findings, old head against new | `tools/stage_probe.py`, independent processes, the cross-user holders a **real other uid** (100000, through a user namespace). At 13e6d869: COLLISION for in-tree under two TMPDIRs and for a TMPDIR alias; a real second user raises PermissionError; symlinked, writable, foreign-owned and non-sticky-base roots ACCEPTED; a `locks` file raises. At `d95e95e8`: every holder isolated; the four bad roots REFUSED with their reasons; the `locks` file harmless. | staging/probe-summary.txt, probe-*.jsonl |
| The reviewer's own probes | R923-1's `stage_root_probe.py` and `stage_alias_probe.py` on both heads: the alias case "same physical slot … True; survived: False" becomes "False; True". The writable and symlinked roots stage at a private random directory, each with its reason. | staging/reviewer-r923-probes-old-vs-new.txt |
| The drivers | Five drivers, each twice at 13e6d869 and twice at 45d5c35a, through the shared cache (hits from each run's `CCACHE_STATSLOG`): tcam, rx_filter binding, avtp_rxmon depkt, crf_rx and milan_dp's in-tree `split_mutants.py`. Every log is IDENTICAL to the old head's first. Warm hits: 16/16, 8/8, 48/48, 115/115, 858/858. First run in the new checkout: 15/16, 7/8, 46/48, 100/115 (round 3's harness residue), 858/858. | mutants/summary.txt |
| Lifecycle | `gptp_shadow/test_mutant_lifecycle.py` PASS | gates/ |

## 2. Shard 1's 38.6 minutes (R923-1-F2)

### 2.1 Attribution

- **Hosted, identical builds.**
  - Shard 1's eight small suites build the same models with the same flags in both runs. Their Verilator build
    walls rose 1.36-1.40× (base run 45383854694 against run 45457006166).
  - Their suite windows rose 1.22-1.61×, and the job 1.41×.
  - milan_dp__1's builds rose 1.62× and its window only 1.32×, so its start-order gain survived a slower runner.
  - capture_coherence__3 has no build report; its window doubled.

  (hosted/shard1-per-suite.txt, hosted/speed-index-base-vs-13e6d869.txt)
- **Same host, same booking.** Shard 1 replicas of base `fcbc31f3` and head `13e6d869` ran concurrently, each on
  2 whole cores, with hosted budgets and no ccache. All ten logs and both piece receipts are IDENTICAL.

  | | base | head |
  |---|---:|---:|
  | job | 1855.5 s | 1693.4 s |
  | capture_coherence__3 | 421 s | 398 s |
  | milan_dp__1 | 1115 s | 962 s (−13.7 %) |
  | instructions | 26.195 T | 26.213 T |

  The same was done for shard 18, since `mclk_mutants.py` is one of the staged drivers: base 1185 s, head
  1073 s, instructions equal, log and nine receipt cases IDENTICAL (ab/summary.txt).
- **Conclusion.**
  - Neither the start order nor the preflight move made shard 1 slower: on one host the head is faster.
  - The 38.6 minutes is that job's runner.
  - What left no room for a slower runner was the dealer's figure for `milan_dp` leg 1: 508 s, against 995 s
    measured at the base. An inventory change had re-targeted the legs (#804); leg 3's 1307 s belonged to the
    case set now on leg 1. So the dealer put leg 1 beside capture_coherence__3 and eight more suites, and shard 1
    was the heaviest worker even at the base, at 27.3 minutes.

### 2.2 The fix (`59f4f478`)

- **The refresh.** CI_WORKFLOWS.md's own rule is "refresh them from the next complete hosted run". All 38 worker
  logs of runs 45383854694 and 45457006166 were measured with `suite_shards.py --measure`, the larger window of
  the two kept.
  - The four `milan_dp` legs: 1309 / 1313 / 275 / 399.
  - Raised where a window exceeded the figure: `milan_dp_mclk` leg 0 to 1408, `capture_coherence` legs 1 and 3
    to 1195 and 724, `maap` leg 0 to 377.
  - Nine whole suites raised: `avtp_rxmon` 73 → 455, `mbx` 73 → 232, `gptp_txts`, `render_queue`, `tdm_render`,
    `aaf_latency_taps`, `aaf`, `tsn_fuzz`, `mac_rmon`.
  - No figure lowered outside `milan_dp`'s re-keyed legs, so #781's and #799's deliberate margins stay.
- **The projection.**
  - The dealer's worst projection is unchanged: 1615 s, on worker 0 (`follow_ring` alone), 185 s inside
    30 minutes.
  - Every figure is now at or above every window of the two runs. On those windows the worst regular worker
    takes 1549 s with the 122 s allowance; before the refresh it was 2383 s (worker 1).
  - CI_WORKFLOWS.md's per-worker table and leg-A sentence are updated.
  - `suite_shards --selftest` and `ci_suite_pieces_selftest` (≤ 1620 / ≤ 2160) pass.

  (hosted/new-figures-projection.txt, hosted/deal-check-old-figures-on-old-runs.txt)

### 2.3 Hosted run at the head (run 45481508309, `45d5c35a`)

Pushed at 21:30 CET after `push-privacy-check.py . 13e6d869…` reported 0 private lines (`13e6d869..45d5c35a`).
rtl-full, rtl-fast, docs and elaborate are all green. `verilator-suites` and `yosys-portability` are success.

| Verilator workers | minutes |
|---|---|
| 0-1, 3-6, 8-16, 18 | 12.7-21.6 (shard 1: **16.1**) |
| 7 (`capture_coherence__1` + `mbx`) | 25.3, runner index 1.31 |
| 2 (`capture_coherence__0` alone) | 27.4, no build to index; its window 1618 s against a 1436 s figure |
| **17** (`milan_dp_mclk__2` + `milan_dp_render__0/1`) | **30.7**, runner index 1.41; `milan_dp_mclk__2` 1051 s against 608/636 in the two earlier runs |

- **Identity.** All 24 piece receipts and all 83 suite verdict sets are IDENTICAL to both earlier runs'
  (hosted/artifact-identity.txt).
- **Runner index.** Per job, the median ratio of the same suites' build walls against the base run
  (hosted/run-45481508309-speed-index.txt).
- **The watcher.** "Fail fast across this head" lasted the run, 58.5 minutes (109.1 at the base); it waits, it
  does no work.

**The open decision.** Dealing cannot give a 30-minute margin against a 1.41× runner:

- A regular worker would need to project at most about 1277 s with its allowance.
- Five indivisible pieces exceed that alone: `follow_ring` 1493, `capture_coherence__0` 1436,
  `milan_dp_mclk__0` 1408, `milan_dp__1` 1313 and `milan_dp__0` 1309.
- The total needs about 22 such workers.

It is the owner's choice:

- split those suites further and add workers, at a cost in runner-minutes;
- or accept "within 30 minutes on a runner of the base run's speed" as the bound.

I did not re-run jobs to draw a faster runner: that would show nothing about margin, and this round's
authorisation covered the push.

### 2.4 Wording (`45d5c35a`)

- R924-1-R1: the three remaining comment blocks cite Issue #998, REQ-VER-01 and REQ-VER-04.
- R923-1-R2: CI_WORKFLOWS.md says the watcher cancels only on a push or a same-repository pull request.
- R923-1-R3: the PR body.

## 3. FPGA-gPTP: the engine passes as make jobs (`661e4c3`; R925-1 F1-F5, R926-1 01-04)

### 3.1 Design

- **Pass targets.** `engine-pass0…3` are targets, so make's `-j` and a parent's jobserver schedule them.
  `pass_run.py run`:
  - writes the image, then runs the pass as the serial line did: pass 0's simulator directly, passes 1-3 through
    the serial line's own `cd DIR && …` under `/bin/sh`;
  - captures standard output and standard error apart;
  - records the exit status, or the signal and the core flag;
  - always exits 0.
- **The four `run::` rules.** Make processes double-colon rules in order, each with its prerequisites.
  - Rule 1 builds.
  - Rule 2 depends on the four passes and replays pass 0.
  - Rules 3-5 replay passes 1-3, each as `replay-gen N` (the generator's stderr and status), then `replay N`
    (banner, output, ending).

  So every message make prints names `run`. `-i` makes make print `(ignored)` after each failing pass's own
  output and continue, as the serial recipe did. A replayed signal re-raises itself, so make names it.
- **`-k`.** Make goes on to the next `run::` rule after a failure, where the serial recipe had stopped. So a
  replay after a failure (the build's, or an earlier pass's marker) prints nothing and exits 0, unless `-i` is
  in effect.
- **Fail fast (F5).** Unless `-i` is in effect, a failing pass marks itself and sends SIGUSR1 to later passes'
  wrappers, which TERM their simulators. A later pass that has not started sees the mark and never starts.
- **Signals (F4).**
  - INT, TERM, QUIT and HUP to a wrapper are forwarded to its simulator and every process below it, read from
    `/proc`, in case `/bin/sh` does not exec it. The wrapper then dies of the same signal.
  - The simulators are no longer async children of a non-interactive shell, so QUIT is no longer ignored.
- **Read failures (R926-02).** A kept transcript that cannot be printed fails its line with a diagnostic.
- **Progressive printing is not done.** Make runs a double-colon rule's prerequisites only after the earlier
  rules, so printing pass N before pass N+1 finishes would serialise them. This is disclosed in the PR body.

### 3.2 Evidence

| Evidence | Result | Receipt |
|---|---|---|
| `passes_test.py` (`make passes-test`, in `all`) | 63/63 PASS, 96 s. 50 transcript comparisons against the serial recipe: ten plans (clean, failing pass at 0/1/3, two failing, SIGSEGV/SIGABRT/SIGKILL, refused image, failed build) under none/`-s`/`-i`/`-k` at `-j4` and none at `-j1`, standard output and standard error apart. Out-of-order completion proved. Budget at `-j1/-j2/-j4`, and a parent `-j3` with two hogs reaching but never exceeding 3. Fail-fast at `-j4`/`-j1`. Five signal cases leave no simulator. An unreadable transcript fails with its diagnostic. | gptp/passes_test-661e4c3.txt |
| Planted defects | 9/9 caught. The previous commit's shape (all four passes in one job) fails exactly the budget checks: 4 at once at `-j1` and `-j2`, 6 in a 3-job parent. The others: `-s` echo, `-i`, `-k` suppression, signal as 128+n, no fail-fast, print failure ignored, no forwarding, streams merged. | gptp/passes_test-plants.txt |
| Real harness, clean | Base `-j4` 453.3 s against head `-j4` 221.3 s (concurrent); base 653.0 s against head 221.4 s and 181.4 s (second pair). `-j1`: 460.6 s against 477.0 s. Instructions +0.29 % at `-j4`, +0.04 % at `-j1`. CPU seconds +20-30 % at `-j4`, at lower IPC on a loaded host. Transcripts IDENTICAL at matching flags (171 lines at `-j4`, 170 at `-j1`). | gptp/summary.txt |
| Real harness, planted abort in pass 1 | Both at `-j4`: identical but for the recipe line number (`Makefile:55` → `:74`), `Aborted (core dumped)`, exit 2; 228.4 s against 154.9 s. | gptp/summary.txt |
| Gates | `make docs` (after shortening lines to its 10-word rule) and `make lint` pass. | gptp/docs-gate.log, lint-gate.tail |

What differs from the serial recipe (all in the PR body):

- the recipe line numbers;
- on INT or TERM, one make line per running pass target instead of one for `run`, and no partial pass output
  (exit status the same);
- one extra core record, from the replaying `python3`, where `core_pattern` pipes cores;
- output only after the passes finish;
- a caller must give `-j4` (or four jobserver slots) to get the passes at once.

**For the native bank, the last item matters:** `make -C gptp-processor all` without `-j` now takes the serial
time. Give it `-j4`, or run it under the bank's jobserver.

One earlier measurement was void and is not used. Its two head arms shared one clone, so their builds and
records collided. Their transcripts still compared IDENTICAL, but every timing was re-measured with one clone per
arm.

## 4. Gates and suites run at the new heads

- milan-fpga `45d5c35a`, clean clone, round 3's gate list: 36/36 rc 0 (gates/summary-45d5c35a.txt), including:
  - `test_suite_cancellation.py` (85 s);
  - `ci_events.py --selftest` (5755 arms);
  - the gptp_shadow lifecycle test;
  - `check_em_dash --base fcbc31f380` (91 added lines in 2 pages).
- Suites the changes touch: the five staged drivers (§1.2), shard 1 and shard 18 replicas (§2.1), and every
  suite hosted at the head (§2.3).
- Not run: the full serial sweep and the act replay. The milan_dp__0 piece measurement was not re-run:
  `ci_make_cases.py` changed by one comment line since round 3.

## 5. Findings for their own Issues

1. **Hosted runner speed spread, about 1.4×**, measured by identical builds: 3 of 19 jobs in this head's run, and
   shard 1 in the previous one. With 19 workers and five indivisible pieces of 1309-1493 s, no deal holds a
   30-minute margin against it (§2.3).
2. **`WORKER_OVERHEAD_SECONDS` is conservative now.** With the preflight moved out, the head's workers spent
   14-81 s outside their suites against the 122 s allowance. Lowering it needs a measured change of its own.
3. **The capture_coherence legs exceed their figures on slow runners** (leg 0 1618 s against 1436). The figures
   are hosted maxima of two runs; three or more runs would make them sturdier.
4. Round 3's open findings stand: unpinned units defeat placement; the harness cross-checkout residue; the idiom
   gate reads only tracked files; the CI tool inventory.
