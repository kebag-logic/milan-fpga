# [A839] CICD improvement — round 7 handoff

Status (2026-11-25 05:20 CET): DONE, review ready, at the unchanged head `9c625393`. ETA: none, nothing of mine is
running. Finding 2 has its cause: **the base moved between the two hosted runs.** It is neither nondeterminism
nor the change, so neither branch (a) nor (b) of the ruling applied.

- No issue was filed (that was for (a) only).
- Nothing needed fixing (that was (b)), so there was no commit and no push.
- Nothing was posted.

Finding 1's ruling is written into the PR body with the #1008 link.

**Head**

- milan-fpga `cicd-3` = `9c62539365fea8316dae2b9fd7c68defeff5cb31`, unchanged. The lane is clean. Its one
  `git fetch origin dev-soft-core` moved only the remote-tracking ref.

**Finding 2: the cause**

- **Different inputs.** A `pull_request` run tests the head merged into the base's tip.
  - Run 45481508309 tested `45d5c35a` into `2509db68`.
  - Run 45528738040 tested `9c625393` into `e608f8d8`, which is PR #995, merged 18 minutes before that run. #995
    re-pins `gptp-processor` from `1616fc8f` to `1213ac5b`.
  - The worker logs and every receipt's `head` field say so.
  - The two merge trees differ in the PR's 18 files and in #995's 25, and in nothing else.
- **The line.** `sim_gptp.cpp:1893` prints the gPTP engine's 2-bit event-queue pointers, the events queued and
  taken since reset modulo 4, at the #207 full-queue window. Its check is relative. `1213ac5b` changes what the
  gPTP program queues before that arm, which shifts the pointers by one.
- **Deterministic for its input.** The two cases ran 40 times:
  - in six trees: the base alone, the head and the pre-change head, each on both bases;
  - directly, under three CPU loads (28 runs), and in CI pieces under the 4-leg and the 8-leg deal (12 runs).

  Each pin gave one output per case every time, and its sha256 equals the hosted receipt's `output_sha256` for
  that pin. Within each base, both binaries and all their inputs are byte-identical across the base, the head and
  the pre-change head.
- **Against one base, no `milan_dp` receipt changes**, with or without this change, under either deal. Nothing is
  masked.
- **Round 6 also missed `gptp_shadow`.** Its verdict lines (11 → 15) are #995's too (326 → 424 checks, four new
  mutants). The hosted Yosys shards' and `split-cdc`'s high factors are explained as well: #995's ROM invalidated
  the Yosys result cache, and the workflow change rebuilt Yosys once.

**For the manager**

- **Decision (optional): a hosted same-base comparison.** None exists: `dev-soft-core` has no push run of
  rtl-full, and the only later PR run on `e608f8d8` was cancelled. Getting one would need a push or a re-run,
  which this round's rules did not allow. The local same-base evidence is tied to the hosted runs by tree ids and
  output digests. Say if you want it hosted.
- **Method note:** any future run-to-run receipt comparison on this PR must first check that both runs' merge
  bases are equal, by reading a receipt's `head`.

**Said plainly**

- I started round L as four sequential units and stopped them within a second, to run it two per CPU instead.
  Their partial files were truncated and rewritten by the new units, and every round-L output is complete.
- Builds used the shared compiler cache (about 15 s each). The comparisons use the binaries' own digests.
- No removal under `/data` or `/data-2`. One stray copy in my own `/home` output directory was removed after a
  `cmp`. Scratch `r7` is 9.2 GB in twelve trees, kept for re-runs; the lane's scratch totals about 19 GB of 40.
  `/data-2` is at 93 %.
- Not run: the act replay, the full serial sweep.

**Written:** REPORT.md, PR-BODY-1003.md (full replacement; not posted), REVIEW-READY.md (not posted),
receipts/INDEX.md (65 KB of text).

REVIEW READY 9c62539365fea8316dae2b9fd7c68defeff5cb31
