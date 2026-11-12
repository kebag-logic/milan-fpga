[A767] REVIEW READY

Commit: `6eacd76d5f596a88a537dcb4fb5b39a5a2284c3c` on `tsn-c-stack-pin-715589c`, one documentation commit on the merge `8bc1dfc0`. No merge, rebase, force or amend; nothing is pushed. This round answers the [A10] round-5 ruling on R829-4 (issuecomment-6830569282). It changes no code, test or generated file.

Changed:
- **F1.** `SPLIT_CONTROL_MEMORY.md:380` and the PR body now state each region's smallest margin at the merge:
  - 288 B of `rom`, at the platform's 1x1/2if;
  - 16 B of `sram`, at the platform's 8x8/2if, whose next granule would plan 59.5 against the 59.0 its override holds.

  R829's `headroom.py`, run on this lane's round-4 receipts, reproduces both minima; its output is identical to the reviewer's.
- **F2.** `tb/verilator/ctrl_service_budget/README.md:44` and `:114` now name `ctrl_memory.LEDGERED` for the size fixture's 8x8 plan, instead of 57.5. `git grep -n '57\.5'` on that README finds only `:791`'s 57.56 ms, a timing figure.
- **F3, the real provenance of `coverage.ratchet`.** No tree change.
  - At `0fb66211` itself, the generator already measures `nvm_store.c` 459/459 and `ctrl_app_aecp.c` 165/165, one line more in each than `0fb66211`'s committed ratchet (458/458, 164/164). R829-4 reports hosted CI measuring the same.
  - So the merge's `--write` records dev's current measurement. The pin move and the composition change neither file's instrumentation.
  - Round 4's REVIEW READY (issuecomment-6829628610) said the generator at `0fb66211` reproduced dev's ratchet, and called the extra line a composition effect. That was wrong. The check that produced it filtered `git diff` for `+`/`-` lines, which this host's shell wrapper does not print, so it saw none.
  - The corrected receipt (the real diff, under a correction header) and a provenance account are in the round-5 packet. Round 4's HANDOFF note is marked corrected.
- **RES-2** (the same paragraph as F1): `SPLIT_CONTROL_MEMORY.md:366` and the PR body name the four PRs `0fb66211` carries since `1d6bf555`. They are #874, #880 (the saved-state format, with the split's KLJ3 stage, #823), #889 and #888; KLJ3's commit `755f8393` first arrives with #880.
- **RES-3** (the same stale 57.5 as F2): the PR body's S2b line, in the reviewer's exact text.
- **To #495, as ruled:** RES-1 and RES-4 (source strings), RES-5, and S1 to S4.

Validation (a clean clone of `6eacd76d`):
- Every `run:` step of `docs.yml`: 64 rc 0, 31 not run with a stated reason, 0 bad. Its three pinned-SDK steps are rc 0, and the Python idiom gate holds at 10 long modules.
- `git diff --check` against the merge base `0fb66211`: rc 0.
- Every other gate is round 4's at `8bc1dfc0`: 150 rc 0, 215 not run, 0 bad, and the control campaign 586 of 586. The delta from there is these two pages.

Acceptance criteria: F1, F2 and F3 are met as the ruling states them.

Open risks/questions: none new. The S2b STOP ruling (issuecomment-6831583372) ledgers 58.5 for S2b's own composed fixture; this head's fixture is measured at 58.0 and ledgered there.
