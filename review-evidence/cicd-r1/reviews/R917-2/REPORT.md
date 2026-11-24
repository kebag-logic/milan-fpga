[R917] POSITIVE - exact head fcbc31f3807a2a7353ab19bfe5aa7f3e56e58c0f

# R917-2: narrow internal re-review of PR #1001 (Relates to #998)

Head `fcbc31f3807a2a7353ab19bfe5aa7f3e56e58c0f`, tree `6aa4a42135fc7615a344aba1935eac8133bdf54b`, base
`300da99beed5bb1c77e4b04af0bb4f9369856e0d` (train head, base branch `dev-soft-core`). No code changed since R917-1:
the PR head is still `fcbc31f3` (`receipts/pr_head_check.txt`), and the clone is clean at that head and tree with
every submodule at its gitlink (`receipts/clone_state.txt`). This round re-checks only the evidence delta: the
`author-r1b` correction packet at `kebag-logic/milan-fpga@0a9f8c0a965ac5cdc1646d668fad7b147ed66857:review-evidence/cicd-r1/author-r1b/`
and the edited PR body. Every other part of R917-1 stands.

**Verdict: POSITIVE.** All four claims I was asked to check recompute from correctly attributed receipts. R917-1-F1,
R918-1-F2 and the figure part of R918-1-F1 are resolved. No MINOR, MAJOR or BLOCKER is open. There are four
SUGGESTIONs, which do not affect coverage.

## 1. Packet integrity

- I fetched the 33 files that bear on this round from the evidence commit `0a9f8c0a` (branch `cicd-review-evidence`):
  all 11 `author-r1b` files, the round-1 `author/receipts/{ccache,budget}`, `author/PR-BODY.md` and the R917-1 ccache
  receipts. All 33 match `MANIFEST.json` `published_sha256`, with 0 mismatches. None is marked `path_redacted`, and
  for each one `original_sha256` equals `published_sha256` (`receipts/r1b_figures.txt` line 1,
  `receipts/fetched_evidence.sha256`).
- The evidence commit and its two parents are not signature-verified on GitHub (`verified: false, unsigned`).
  Integrity therefore rests on the manifest hashes at an immutable commit SHA. That is a limit, not a finding (see 6).
- Re-staging is byte-exact. Round-1 `ccache/nocc.time`, `cold.time` and `cold.stats` equal
  `author-r1b/.../avtp_rxmon/{nocc.time,cold.time,cold.stats}`, and round-1 `ccache/warm.time` equals
  `author-r1b/.../crf_rx-mutants/warm.time`. This confirms what was wrong in round 1: two avtp_rxmon files and one
  crf_rx file were filed under one name. The two newly published files, crf_rx `nocc.time` and `cold.time`, use the
  same labelled format as crf_rx's `warm.time` (`<run> W wall U user S sys`). The avtp_rxmon files use the unlabelled
  form, so the two campaigns can be told apart from the files themselves.

## 2. The four claims checked

`scripts/r1b_figures.py <packet>/review-evidence/cicd-r1` writes `receipts/r1b_figures.txt`:

| Claim (PR body / CORRECTIONS.md) | Receipts | Recomputed | Result |
|---|---|---|---|
| crf_rx 23 mutants, CPU -47 % cold | `crf_rx-mutants/{nocc,cold}.time` user 497.96 -> 262.00 | -47.39 % | matches |
| crf_rx mutants, -54 % warm | `crf_rx-mutants/{nocc,warm}.time` user 497.96 -> 229.32 | -53.95 % | matches (CORRECTIONS -53.9 %, PR -54 %) |
| crf_rx "results identical", 23/23 in each run | `crf_rx-mutants/{nocc,cold,warm}.log` | 23 `[PASS]` cases in each run, 0 other case lines, tally `checks: 23 failures: 0`. The three logs are byte-identical (sha256 `fb31108c...941f5b`), so all 23 verdict lines and their named-rejection lines are identical | matches |
| avtp_rxmon -65 % cold | `avtp_rxmon/{nocc,cold}.time` user 1587.52 -> 547.52 | -65.51 % | matches |
| -O3 budget: "L1d misses 5-15 % lower in three paired runs (median 8.8 %)" | `budget/{base,base-2,base-3}.perf` vs `budget/tbO3{,-2,-3}.perf`, field `L1-dcache-load-misses:u` | 14.51 / 8.83 / 5.38 %, median 8.83 % | matches the three raw pairs (14.5 / 8.8 / 5.4 %) |
| -O3 budget: CPU -2.5..-5 % (unchanged) | same files, `task-clock:u` | 4.87 / 2.61 / 2.50 % | matches |

I also checked the crf_rx figures against an independent run. My R917-1 round ran the crf_rx mutant campaign through
ccache at this exact head, in a private cache, as a separate run on this host (`R917-1/scripts/ccache_probe.sh`). It
gave user CPU -47.92 % cold and -50.85 % warm. Its two logs, minus the make echo line and the trailing `rc=` line,
are byte-identical to the re-staged `nocc.log` (`receipts/independent_corroboration.txt`). The re-staged logs are
therefore the head's real mutant-campaign output, and the cold figure reproduces to within 0.6 points. The warm
figure is in the same direction, 3 points smaller. That is consistent with paired-run noise on this host, and the
PR's "-54 % warm" is the attributed receipt's own value.

The edited PR body changes only three things (`receipts/pr_body_diff.txt`): the `Relates to #998` lines, the ccache
row and the -O3 row. The ccache row now reads "crf_rx's 23 mutants: CPU -47 % on a cold cache (-54 % warm), results
identical; avtp_rxmon -65 % cold (receipts re-attributed in the `author-r1b` packet)". The -O3 row reads "CPU
-2.5..-5 %, L1d misses 5-15 % lower in three paired runs (median 8.8 %), output md5-identical". Both agree with the
table above. "CPU" in the ccache row is user CPU, as in the CORRECTIONS table's "Change (user)" column. Without the
round's rounding the range is 5.4-14.5 %, so "5-15 %" is honest. No other row, figure or claim moved. The tracked
delta carries none of the corrected figures: the only figure in the source, the `build.py` comment
"2.5-5 % less CPU ... the same output", was already correct. The commit subjects ("47 % less CPU, the same results";
"2.5-5 % less CPU") are also consistent with the receipts.

## 3. Prior findings, resolved or retained at this head

- **R917-1-F1 (MINOR, Docs): L1d -7..-9 % does not match `budget/*.perf`. RESOLVED.** The PR body now states the
  receipts' figures (section 2). `author-r1b/CORRECTIONS.md` names the superseded statement and publishes the three
  pairs. The round-1 `author/REPORT.md:137` and `:218` still say 7-9 %, but that packet is immutable published
  evidence and the correction layer explicitly supersedes it (S4).
- **R918-1-F2 (MINOR): L1d 7-9 % vs the three pairs. RESOLVED** on the same evidence. R918-1's own table equals mine
  to the rounding.
- **R918-1-F1 (MINOR): ccache receipts mis-attributed. RESOLVED for every figure and output claim the PR body makes.**
  The crf_rx and avtp_rxmon receipts are now separately named, and every figure recomputes. The crf_rx output
  comparison is published in full, and my independent exact-head run corroborates it. That finding's required outcome
  also asked for "the actual commands, revision/variant identity". The re-staged files carry neither, and
  `author/REPORT.md:179` still states a crf_rx cold-cache hit rate of 66 % with no attributed stats file. Neither
  leaves a PR-body claim unsupported, and my head run measured 64.35 % (74/115). I record them as S1-S3 so that the
  issuing reviewer, who owns the closure of R918-1-F1, sees them in one place.
- **R917-1 RESIDUE R1 (stale comments in `tb/verilator/crf_rx/sim_main.cpp`) stays as recorded in R917-1.** No code
  changed, and it was wording-only residue.

## 4. Findings

No BLOCKER, MAJOR, MINOR or RESIDUE in this round's delta. The PR-body edit adds no lane labels or round IDs to
source; the comment rule concerns source comments, and the source did not change.

**R917-2-S1 - SUGGESTION - lenses: Tests, Docs - `author-r1b/receipts/ccache/avtp_rxmon/logs.sha256`.**
Evidence: the no-cache and cold avtp_rxmon logs have different hashes and sizes (395792 vs 396078 bytes), and only
their hashes are published. The receipts therefore show the -65 % figure but not that the cached build kept every
avtp_rxmon verdict. The PR body does not claim avtp_rxmon output identity, so nothing it states is unsupported. The
log directory is named `runs/ccrx/`, which reads like crf_rx.
Impact: none on any stated claim. A reader could infer an identity that has not been shown.
Suggested outcome: publish the avtp_rxmon verdict and tally lines for both runs (they are small) and their
comparison, or state that only timing is claimed for avtp_rxmon.
Verification: `diff` of the two verdict extracts.

**R917-2-S2 - SUGGESTION - lenses: Tests, Docs - `author-r1b/receipts/ccache/*/*.time`.** The re-staged receipts carry
no command line, cache directory policy or tree identity. The crf_rx logs also lack the `python3 mutants.py` make echo
that a raw `make -C tb/verilator/crf_rx mutants` log contains. That suggests they were captured from the driver
rather than through make.
Impact: provenance has to be inferred. For crf_rx my independent run fills the gap; for avtp_rxmon nothing does.
Suggested outcome: a `cmd` receipt per campaign, giving the command, the `OBJCACHE`/`CCACHE_DIR` setting and the
tree SHA.

**R917-2-S3 - SUGGESTION - lenses: Docs - `author/REPORT.md:179` ("even a cold cache hits 66 % of compiles").** The
only published `cold.stats` is avtp_rxmon's (71.59 %), so the crf_rx 66 % has no attributed receipt. My exact-head run
gave 64.35 % (74/115). The figure is not in the PR body or any tracked file.
Suggested outcome: a CORRECTIONS addendum that publishes the crf_rx cold stats, or cites this round's 64 %, or
withdraws the figure.

**R917-2-S4 - SUGGESTION - lenses: Docs - `author/REPORT.md:137,218`, `author/receipts/INDEX.md:16`.** The immutable
round-1 packet still carries the superseded L1d range and the old single-name ccache mapping.
`author-r1b/CORRECTIONS.md` supersedes both, but nothing in the round-1 files points to it.
Suggested outcome: the merge-turn evidence index or the final PR evidence comment names `author-r1b/CORRECTIONS.md`
as superseding those lines.

## 5. Reviewer-owned completion ledger

| Lens | Status | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #998 AC1 figure claims vs `author-r1b/receipts/ccache/{crf_rx-mutants,avtp_rxmon}/*.time`, `budget/{base,tbO3}{,-2,-3}.perf`; live PR body rows 2-3; R917-1 coverage of the diff carried (no code change) | R917-1, re-confirmed R917-2 | fcbc31f3807a2a7353ab19bfe5aa7f3e56e58c0f |
| RTL | CLEAN | R917-1 port-default census, top-input write scan and scope tables carried; the delta is evidence-only and touches no RTL, harness or build input (`receipts/clone_state.txt`) | R917-1 (carried, R917-2 confirmed no change) | fcbc31f3807a2a7353ab19bfe5aa7f3e56e58c0f |
| Robustness | CLEAN | R917-1 coverage carried (`run_all_suites.sh:121-133`, ccache absent/failing path, mutant drivers); unchanged at this head | R917-1 (carried, R917-2 confirmed no change) | fcbc31f3807a2a7353ab19bfe5aa7f3e56e58c0f |
| Tests | CLEAN | crf_rx `{nocc,cold,warm}.log` 23/23 byte-identical; independent exact-head mutant run vs r1b logs (`receipts/independent_corroboration.txt`); `budget/outputs.md5`; R917-1 suite identities carried | R917-1, re-confirmed R917-2 | fcbc31f3807a2a7353ab19bfe5aa7f3e56e58c0f |
| Docs | CLEAN | live PR body (`receipts/pr1001_body_live.md`, `pr_body_diff.txt`); `author-r1b/CORRECTIONS.md`; `build.py:778-779` comment; commit subjects; TESTING.md 169-178 carried from R917-1 | R917-2 | fcbc31f3807a2a7353ab19bfe5aa7f3e56e58c0f |

## 6. Limits and pending manager duties

- Limits:
  - Narrow round: I checked only the four claims named in the brief, plus the prior findings at their cause.
  - I ran no suites, builds or mutation probes this round. The crf_rx corroboration reuses my own R917-1 exact-head
    run.
  - Nothing independently reproduces the avtp_rxmon timing or output identity.
  - The evidence commit is unsigned. Integrity rests on the `MANIFEST.json` hashes at commit `0a9f8c0a`.
  - Issue #998 has no comments, and no separate manager evidence comment on the PR covers this delta. The correction
    evidence is the `author-r1b` packet and the PR-body edit (PR updated 2026-11-24T12:49:30Z).
  - I do not claim or infer any manager source bank at this head.
  - Physical calibration was NOT RUN. Field skips are not hardware proof.
  - I inspected no hosted or act acceptance this round.
- Pending manager duties:
  - Obtain the second independent positive review: the external re-review of R918-1-F1/F2, which owns the closure of
    its own findings, with S1-S3 offered as input.
  - Validate the current-dev merge candidate, from source base `300da99b` against live dev `e275d795`, with the
    builder and native banks, and link the receipts on the PR.
  - Hosted/act acceptance at the exact head.
  - Merge only with explicit maintainer authorization; then post-merge containment and the #998 close-out.
  - Carry R917-1 R1 and any S-items taken up to the residue checklist.

R917-2 FINISHED
