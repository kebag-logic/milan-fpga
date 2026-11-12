[R829] NEGATIVE - exact head 6eacd76d5f596a88a537dcb4fb5b39a5a2284c3c

Round R829-5 is a delta review of PR #892 (issue #665, the tsn-c-stack pin move). It covers the change from `8bc1dfc0`, where round R829-4 (#892 issuecomment-6830563250) was NEGATIVE on three MINOR findings, to `6eacd76d` (tree `9b1d0afb9598f6e2cf73b436e9ddd1d36f75ff0c`). The delta is one documentation commit.

**Verdict.** The verdict is NEGATIVE on one MINOR finding, F3-R, under the Tests and Docs lenses.
- F1 and F2 are closed: the head's planner reproduces the margins, and the README check returns what the ruling asked for.
- Part of F3 is closed: the real provenance of `coverage.ratchet` is now stated in public.
- Part of F3 is still open. The ruling (#665 issuecomment-6830569282) said "The corrected receipt goes in the round 5 packet", and it is not there:
  - The published receipt still carries the false annotation.
  - Three round-5 texts say a corrected receipt was published.

No code, test, generated artifact or measurement is wrong at this head. Conformance, RTL and Robustness are clean.

## Reconstruction (public state only)

- **Authority.** I read the following, in this order:
  - `AGENTS.md` sections 3 and 5 to 8, and CONTRIBUTING's review bar, via `AGENTS.md`;
  - the round-5 ruling, #665 issuecomment-6830569282 ("docs and evidence only … No code, test or generated-artifact change. Gates: the docs gates and `git diff --check` on a clean clone of the final head. Then R829 alone, as a delta review");
  - the owner's flip-ROM decision, issuecomment-6824896581 (the fixture's 8x8/2if may plan 58.0, cap 58.5; the platform's 60.0, cap 60.5; every other point 56 or fewer);
  - the STOP ruling for the S2b lane, issuecomment-6831583372, saved as `receipts/ruling-6831583372.md`. It concerns #810's composed fixture, not this head.
- **Author evidence.**
  - REVIEW READY #665 issuecomment-6832030626, saved as `receipts/review-ready-live.md`. It matches the packet copy except for one trailing blank line.
  - Archive `c0e0f81048e3c07503c44022f18e67b7644d1ac2` on `tsnpin-review-evidence`, in `review-evidence/tsnpin-r1/author-r5` and the `author-r4` receipts it cites.
  - The live PR body, saved as `receipts/pr-body-live-at-review.md`.
- **Delta.** `git diff 8bc1dfc0..6eacd76d` and `git diff 1d6bf555..6eacd76d --stat`.
- **Order.** I read prior public findings on this PR only after my own pass over the delta. Since R829-4 there is no other review round on #892 or #665 (`gh api` comment listing, 2026-11-12).

## The assignment's checks

### (1) F1: both regions' smallest margins — CLOSED

- **Doc.** `docs/design/SPLIT_CONTROL_MEMORY.md:380` now reads: "The smallest margins at the merge are 288 B of `rom`, at the platform's 1x1 with two interfaces, and 16 B of `sram`, at the platform's 8x8 with two interfaces, whose next granule would plan 59.5 against the 59.0 its override holds."
- **PR body.** Live line 82 states the same two minima. Its line "One byte past those 16 B plans 59.5 … past the 59.0 its override holds" is correct.
- **Reproduction.** `python3 -I scripts/headroom.py <head clone> author-r4/receipts/round4` runs the head's `ctrl_memory.banks`, and gives `receipts/headroom.txt`:
  - Its first 17 lines are byte-identical to R829-4's `headroom.txt` and to the author's `author-r5/receipts/round5/headroom.txt`.
  - "merge: smallest spare of any region: (16, 'platform-merge/8x8-if2', 'sram') smallest rom spare: (288, 'platform-merge/1x1_tdm8-if2')".
- **The 59.5 claim.** My script adds a next-granule computation that the script did not have in round 4:
  - `platform-merge/8x8-if2 sram +17 B -> 59.5 tiles (now 59.0)`;
  - `platform-merge/1x1_tdm8-if2 rom +289 B -> 42.5`.
- `ctrl_memory.py:251-253` holds the platform's point at 59.0, so the "against the 59.0 its override holds" clause is right.

### (2) F2: the harness README's ledger figure — CLOSED

- `tb/verilator/ctrl_service_budget/README.md:44` now says the point "may plan past the 56-RAMB36 budget to the tiles `ctrl_memory.LEDGERED` holds for it".
- `:114` says the plan "is held to the ledgered point's tiles in `ctrl_memory.LEDGERED` (`split_soc.ledgered_plan`)".
- Both named anchors exist at the head: `ctrl_memory.py:246` `LEDGERED`, `split_soc.py:456` `def ledgered_plan`, and `build.py:179` `LEDGERED_POINTS`.
- `git grep -n '57\.5'` on the README returns only `:791`, a 57.56 ms timing figure (`receipts/f2-check.txt`).
- Naming the dictionary rather than restating the number also survives the 58.5 that #810's STOP ruling plans for its own composed fixture.

### (3) F3: `coverage.ratchet` provenance — PARTLY CLOSED; the receipt part is retained as F3-R

**Closed:** the provenance itself is now stated correctly in public. It matches the measurement and the hosted record from round 4:
- REVIEW READY, the F3 bullet;
- `author-r5/receipts/round5/coverage-provenance.txt`, points 1 to 4;
- live PR body line 57;
- `author-r5/HANDOFF.md:81`, marked corrected.

The figures, in `receipts/f3-check.txt`:
- At `0fb66211`, the generator measures `ctrl_app_aecp.c` 165/165 and `nvm_store.c` 459/459 (`author-r4/.../fw_coverage-write-at-0fb66211.log:34,51`).
- `0fb66211`'s committed ratchet says 164/164 and 458/458.
- The head's ratchet says 165/165 and 459/459.

**Open:** the corrected receipt that the ruling required is not in the published packet. See F3-R.

### (4) Scope and docs gates — PASS

- **Scope** (`receipts/delta-scope.txt`):
  - `git diff --name-status 8bc1dfc0 6eacd76d` lists two modified Markdown files, `docs/design/SPLIT_CONTROL_MEMORY.md` and `tb/verilator/ctrl_service_budget/README.md`. Both are 100644 to 100644.
  - No code, test, generated artifact or gitlink changed. The six gitlinks are the head's.
  - The commit message is one line with no trailers.
  - `git diff --check` gives rc 0 against both `0fb66211` and `8bc1dfc0`.
- **Docs gates on a clean clone** of `6eacd76d` (`scratch/clean`, never published):
  - The clone was made with `git clone --no-checkout` plus a checkout of the exact SHA.
  - `gptp-processor`, `protocol-processor`, `lwSRP` and `tsn-c-stack` were initialised at the head's gitlinks.
  - All eleven gates give rc 0 (`receipts/logs/docs_gates.txt` and `docs_*.log`): `docs_check.py`, `check_feature_status.py`, `check_doc_style.py`, `check_gptp_docs.py`, `DOC_MAP.gen.py --check`, `check_solution_docs.py`, `submodule_boundaries.gen.py --check`, `check_submodule_docs.py`, `check_nvm_klj3.py`, `check_nvm_format_32x32.py` and `check_wire_accountability.py`.
  - The clone's status was empty afterwards.
- **First attempts.** These ran before the submodules were initialised. Three gates refused with "the gptp-processor submodule is not checked out" or "the protocol-processor submodule is not checked out". Those logs are kept as `*.no-submodule.*` and `*.no-pp-submodule.*`. This is the environment, not a defect.
- **Author's docs run.** The author's run of `docs.yml` at `6eacd76d` is in `author-r5/receipts/round5/gates-6eacd76d`, and all 155 `author-r5` files verify (below).

### Author packet integrity

`receipts/author-packet-manifest-check.txt`, from `scripts/verify_author_packet.py`:
- `author-r5/` has 155 entries in `MANIFEST.json`: 0 missing, 0 hash mismatches, 0 unlisted.
- `author-r4/` has 479 entries: 0 missing, 0 mismatches, 0 unlisted.
- The archive commit `c0e0f810` carries no signature (0 `gpgsig` headers), the same as round 4 (R829-4 S4). Integrity rests on the manifest.

### RES-2 and RES-3, taken on the same lines — CLOSED

- **RES-2.** `SPLIT_CONTROL_MEMORY.md:366` and PR body line 57 name #874, #880, #889 and #888.
  - That matches `git log --first-parent 1d6bf555..0fb66211`: `764482b4` #874, `8b1bdfaf` #880, `38967e26` #889 and `0fb66211` #888.
  - KLJ3's `755f8393` (#823) first arrives with #880's merge, as the new text says (`receipts/res2-dev-range.txt`).
- **RES-3.** PR body line 165 carries round 4's exact text ("this head's ledger holds that point at 58.0 …").

## Findings

### F3-R — MINOR — Tests, Docs — `review-evidence/tsnpin-r1/author-r4/receipts/round4/fw_coverage-write-at-0fb66211-diff.txt` (archive `c0e0f810`); `author-r5/receipts/round5/coverage-provenance.txt:6`; `author-r5/HANDOFF.md:16`; REVIEW READY #665 issuecomment-6832030626 (F3 bullet, "The corrected receipt …") — the corrected coverage receipt was not published, and three texts say it was

This is R829-4 F3, retained and narrowed. The provenance is now correct; only the receipt part remains open.

**Authority.**
- R829-4 F3's required outcome: "The receipt's annotation is corrected or replaced."
- The round-5 ruling, issuecomment-6830569282: "The corrected receipt goes in the round 5 packet."

**Evidence** (`receipts/f3-check.txt`):
- The published receipt is still blob `71248a0d5aabf024f88cd5a8be35768949c13373` at `c621aff3`, `1e33fa18` and `c0e0f810`.
- It still reads "(empty: the generator at 0fb66211 writes dev's committed ratchet unchanged)" under a stat of "2 insertions(+), 2 deletions(-)".
- The `MANIFEST.json` entry for it still hashes to that unchanged content.
- `author-r5` contains no copy of the receipt, corrected or otherwise. Its non-gate files are `HANDOFF.md`, `PR-BODY.md`, `coverage-provenance.txt`, `diff-check.*`, `headroom.txt`, `INDEX.md`, `PR-BODY-round4.md`, `review-ready-comment.md` and `tools/headroom.py`.
- Yet three texts say the correction exists:
  - `coverage-provenance.txt:6` cites "round4/fw_coverage-write-at-0fb66211-diff.txt, corrected";
  - `HANDOFF.md:16` says round 4's file "carries the real diff under a correction header";
  - REVIEW READY says "The corrected receipt (the real diff, under a correction header) … [is] in the round-5 packet".

**Impact.**
- A cold reader who opens the cited receipt finds the refuted claim, with nothing beside it to say so.
- The round-5 evidence then misstates what was published. That is a claim about an evidence artifact, not about wording.
- No measurement, gate or tracked value is wrong. The ratchet at the head equals the generator's measurement.

**Required outcome.** The published evidence carries the corrected receipt, as the ruling says. Either of these meets it:
- add the real `git diff` of `coverage.ratchet` at `0fb66211`, under a correction header, to `author-r5/receipts/round5/` and list it in `MANIFEST.json`;
- or re-archive `author-r4`'s receipt with its manifest entry updated.

The three citing texts must then name a file that exists. Alternatively, they stop claiming a corrected receipt and `coverage-provenance.txt` states that it supersedes the round-4 annotation. That alternative still leaves the false annotation unmarked, so prefer the first.

**Verification.**
- `scripts/verify_author_packet.py` passes on the new archive.
- The named file shows `ctrl_app_aecp.c` 164 -> 165 and `nvm_store.c` 458 -> 459, matching `fw_coverage-write-at-0fb66211.log:34,51` and `git show 0fb66211:sw/firmware/gtest/coverage.ratchet`.

**Delta.** No tree change is needed, and the source head need not move.

### Residue and suggestions

- **No new RESIDUE in the delta.**
  - The two edited pages are design and harness documentation, not source comments.
  - The lane names they carry (S7, S2, S14) follow the existing practice of those pages.
  - Neither page adds an issue-comment ID.
- **Carried to #495 by the ruling, and still in the tree.** This is the manager's residue checklist, not a lens defect:
  - RES-1: `sw/litex/ctrl_memory.py:249`, "the owner's 6824896581".
  - RES-4: `tb/verilator/ctrl_service_budget/scenario.py:312`, "MAILBOX_SPLIT.md:649-661".
  - RES-5: the live PR body's SDK sentence, now at line 63.
  - S1 to S4 of R829-4. S4 is the unsigned archive, which applies equally to `c0e0f810`.
- **SUGGESTION S5 (no lens).**
  - **Where:** `author-r5/receipts/round5/review-ready-comment.md`.
  - **What:** the packet copy differs from the posted comment by one trailing blank line. That is harmless, but a byte-identical copy (or a recorded sha256 of the posted body) would let a reader check the match mechanically.

## Prior public findings: resolved or retained at this head

| Prior finding | State at `6eacd76d` | Evidence |
|---|---|---|
| R829-4 F1 (MINOR, Docs) | **CLOSED** | `SPLIT_CONTROL_MEMORY.md:380`; PR body line 82; `receipts/headroom.txt` |
| R829-4 F2 (MINOR, Docs) | **CLOSED** | README `:44`, `:114`; `receipts/f2-check.txt` |
| R829-4 F3 (MINOR, Tests and Docs) | **Provenance CLOSED; receipt part RETAINED as F3-R** | `receipts/f3-check.txt` |
| R829-4 RES-2, RES-3 | **CLOSED** | `receipts/res2-dev-range.txt`; PR body lines 57 and 165 |
| R829-4 RES-1, RES-4, RES-5, S1 to S4 | carried to #495 by the ruling; still present | `ctrl_memory.py:249`; `scenario.py:312`; PR body line 63 |
| R829-2 F1 = R830-2 N1; R829-2 F2; R829-3 RES-B; R829-2 RES1 to RES3 | **CLOSED**, and they stay closed: the delta touches none of their artifacts | `receipts/delta-scope.txt` |
| Older optional suggestions (R829-2, R830-2, R830-3, R829-3) | retained as optional; their scope is untouched | — |

## Lens results at `6eacd76d5f596a88a537dcb4fb5b39a5a2284c3c`

```text
[R829] PASS Conformance — SPLIT_CONTROL_MEMORY.md:366-385; sw/litex/ctrl_memory.py:246-255; receipts/headroom.txt; receipts/res2-dev-range.txt — the new section-5 text checked against the owner's decision 6824896581 and LEDGERED (fixture 58.0 <= 58.0/58.5, platform 59.0 <= 60.0/60.5); both margins and the 59.5 next-granule plan recomputed with the head's planner; dev's four PRs checked against first-parent history; ctrl_memory.py byte-identical to 8bc1dfc0
[R829] PASS RTL — receipts/delta-scope.txt — the delta is two Markdown files (100644), with no hdl/, .sv/.v, syn/, SoC builder or gitlink change; RTL is byte-identical to 8bc1dfc0, which R829-4 found to carry no RTL against 0fb66211
[R829] PASS Robustness — receipts/delta-scope.txt; ctrl_memory.py:246-261; split_soc.py:456; build.py:179-184 — the fail-closed ledger override and its refusals are unchanged; the README now points at the mechanism (LEDGERED and ledgered_plan) instead of a number that can go stale, which is robust to #810's planned 58.5
[R829] UNCLEAN Tests — F3-R: the coverage receipt the ruling required is not published (author-r4/.../fw_coverage-write-at-0fb66211-diff.txt is unchanged at blob 71248a0d; there is no copy in author-r5), while three round-5 texts cite it as corrected. Otherwise clean: no test or generated file changed in the delta (receipts/delta-scope.txt); the ratchet at the head equals the generator's measurement (receipts/f3-check.txt)
[R829] UNCLEAN Docs — F3-R (above). Otherwise clean: SPLIT_CONTROL_MEMORY.md:366,380 and ctrl_service_budget/README.md:44,114 are correct against LEDGERED and the receipts; PR body lines 57, 58, 82 and 165 are correct; the eleven docs gates give rc 0 on a clean clone (receipts/logs/docs_gates.txt); git diff --check gives rc 0
```

## Reviewer-owned ledger

| Lens | CLEAN / UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | owner decision 6824896581; ruling 6830569282; `SPLIT_CONTROL_MEMORY.md:366-385`; `ctrl_memory.py:246-255`; `receipts/headroom.txt`; `receipts/res2-dev-range.txt` | R829-5 | `6eacd76d5f596a88a537dcb4fb5b39a5a2284c3c` |
| RTL | CLEAN | `receipts/delta-scope.txt` (no RTL in the delta); R829-4's diff against `0fb66211` (no RTL) | R829-5 | `6eacd76d5f596a88a537dcb4fb5b39a5a2284c3c` |
| Robustness | CLEAN | `ctrl_memory.py:246-261`; `split_soc.py:456`; `build.py:179-184`; `receipts/delta-scope.txt` | R829-5 | `6eacd76d5f596a88a537dcb4fb5b39a5a2284c3c` |
| Tests | UNCLEAN (F3-R) | `receipts/f3-check.txt`; `author-packet-manifest-check.txt`; `delta-scope.txt` | R829-5 | `6eacd76d5f596a88a537dcb4fb5b39a5a2284c3c` |
| Docs | UNCLEAN (F3-R) | the two edited pages; live PR body; REVIEW READY (live and packet copies); `author-r5` HANDOFF and receipts; `receipts/logs/docs_gates.txt` | R829-5 | `6eacd76d5f596a88a537dcb4fb5b39a5a2284c3c` |

F3-R needs no tree change. Once the corrected receipt is published and the citing texts name it, Tests and Docs can be re-covered at this same head by checking the evidence alone.

## Real limits

- **No images linked by me.** The margins rest on the author's round-4 `*.size.json` receipts, which the manifest verifies, recomputed with the head's planner. `ctrl_memory.py` is byte-identical to `8bc1dfc0`.
- **Only docs and evidence gates run.** I did not rerun the firmware, campaign, coverage or Verilator banks. The delta changes nothing they depend on, so their R829-4 results at `8bc1dfc0` carry by scope, not by fresh execution.
- **Hosted CI not finished.** At review time hosted checks on `6eacd76d` were mostly queued or in progress: 33 not concluded, 1 success, 1 skipped (`receipts/hosted-check-runs-6eacd76d.tsv`). I claim no hosted result for this head.
- **No manager source bank** runs at this head, and I infer none.
- **No physical evidence.** No physical calibration was run, and no hardware evidence exists for this PR.
- **Unsigned archive.** The evidence archive commit carries no signature. Integrity is by manifest only.
- **Clean clone.** It was made locally from this review clone. Its submodules were fetched with this clone's module objects as reference, and its checks were made at the head's gitlinks.

## Pending manager duties

- Answer F3-R: publish the corrected receipt, then hand Tests and Docs back for an evidence-only re-cover at the same head.
- Own hosted and act acceptance for `6eacd76d`. The hosted checks were not finished at review time.
- At the merge turn, build and validate the current-dev candidate on live dev `b7d692952305e4e0e132abb8f99c339eeb17a873` (source base `1d6bf555`), with builder and native banks.
  - Order this PR against #810's STOP ruling (issuecomment-6831583372), which moves `ctrl_memory.LEDGERED`'s fixture point to 58.5 on S2b's line.
  - Whichever lands second re-measures and restates the key and the section-5 text.
- Carry RES-1, RES-4, RES-5 and S1 to S5 on the #495 residue checklist.

R829-5 FINISHED
