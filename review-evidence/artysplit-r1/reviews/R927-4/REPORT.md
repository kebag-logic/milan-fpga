[R927] NEGATIVE - exact head 011aaa6f080321e0a89f915720ebb3ee14807a16

# R927-4: narrow evidence re-review of PR #1004 (relates to #878)

Head `011aaa6f080321e0a89f915720ebb3ee14807a16`, tree `5b11a07de8c4f69999277424aa8d9b704c297a96`. This is the same source head as R927-3; no source changed. The only change under review is the evidence republication at `0cad829e1af15b9c96b0ef3d10d109b9721154c5` (parent `3fc4a9d0`). That commit's message is "Republish 27 census observation parts byte-exact (a decimal cycle count was misread as a hex payload by the scrub)".

- **R927-3 F1 is CLOSED at its cause.** The published census extract is now byte-exact, and the unmodified head regrader reproduces everything the finding asked for:
  - `PASS cases=147` with `RESULT: PASS cross-case ...`, exit 0.
  - The control without `srp-bound` is refused by the #977 disposition line, exit 1.
  - Both logs equal the author's own logs. The regrade log is byte-identical, and the control log differs only in three traceback path prefixes.
- **The verdict stays NEGATIVE for one reason only:** R927-3 F2 (MINOR, `Tests` and `Docs`, the empty `builder-split.log`) is still open at this head and evidence. The brief carries it to the integration round, but carrying a finding does not close it (AGENTS.md section 7). `Tests` and `Docs` therefore stay unclean.
- **The external review's R928-3-F2 and F3 are still open.** The code they name is unchanged at this head. They are carried to the integration round.
- **This round adds no new MINOR or higher finding.** It adds one RESIDUE (RS-3) and retains RS-1 and RS-2.

## 1. Republication: original == published for every census-extract file

**Receipt:** `receipts/publication-check.log`, produced by `scripts/verify_publication.py` on the evidence extracted from `0cad829e`, with the parent `MANIFEST.json` taken from `3fc4a9d0`.

| Check | Result |
|---|---|
| `author-r8/receipts/FILES.tsv` (reassembled from its one part, whose hash and size match `FILES.manifest.json`) against the bytes on disk | 814 rows, 0 differ or missing. The only unlisted file is `INDEX.md`, which is unlisted by design |
| Publisher `MANIFEST.json` entries under `author-r8/receipts/census-extract/` | 762 entries for 762 files on disk. For every entry, `original_sha256 == published_sha256 == sha256(disk)` and equals that file's `FILES.tsv` row. 0 mismatches. `path_redacted: true` on 0 entries |
| `MANIFEST.json` entries changed between `3fc4a9d0` and `0cad829e` | Exactly 27, the same 27 files R927-3 listed. Each was `path_redacted: true` with `published != original` and is now `false` with `published == original`. No entry was added or removed |
| Evidence tree diff `3fc4a9d0..0cad829e` | 28 files (the 27 parts plus `MANIFEST.json`), +83/-83 lines. Nothing else in the evidence tree changed |
| Extract size (`receipts/extract-size.txt`) | 762 files, 1,434,762,896 bytes, largest 13,999,999, none at or over 14,000,000. This equals the PR body's "Reproduce and inspect" figures |

On a sample changed line in `valid-destinations/srp-talker/observations.log.part0004.txt`, the scrubbed tokens (for example `1423232384`) and the republished tokens (for example `1464264284`) are equal-length decimal counts. That is consistent with the stated cause, a decimal count misread as a payload and rewritten in place. It also matches R927-3's recorded symptom, a one-poll difference in `srp-talker`'s `/passes/polls/passes`.

## 2. Regrade of the published extract with the unmodified head regrader

**Regrader identity (`receipts/regrader-identity.txt`):** the worktree blob of `tb/verilator/ctrl_service_budget/receipt_regrade.py` equals `HEAD:` (`51bebf62...`), as do those of `kept_grade.py`, `census_extract.py`, `grade.py`, `run.py` and `arty_grade.py`. The clone status, including ignored files, is empty.

**How it ran:** both runs used `python3 -B -E -s <head>/tb/verilator/ctrl_service_budget/receipt_regrade.py <dir>` and ran concurrently. `-B` stops the run from writing bytecode into the clone, and the evidence is read as data only.

| Run | Input | Result | Receipt |
|---|---|---|---|
| Published extract | `0cad829e:review-evidence/artysplit-r1/author-r8/receipts/census-extract` as published | **exit 0.** 147 `PASS <case>: complete grade reproduced`, including `valid-destinations/srp-talker`, the case that gave `grade differs` in R927-3. Then `RESULT: PASS cross-case costs, record classes, held-egress ledger and owner bounds` and `RESULT: PASS cases=147 worst_pass_cycles=142775` | `receipts/regrade-published.log`, `.rc` |
| Control (the lane's recipe) | A hard-linked copy of the published extract in which only `census.json` is rewritten, without the `none/srp-bound` row. All files are kept (`scripts/make_control.py`, `receipts/control-build.log`: 147 to 146 cases, `none/srp-bound` files kept) | **exit 1, refused in the cross-case step.** All 146 cases reproduce first. Then: `REFUSED #977 (https://github.com/kebag-logic/milan-fpga/issues/977): srp-kept and srp-bound are graded together on one image, this run graded srp-kept alone`. It also prints the three `srp-kept` SRP apply lines that the disposition no longer owes, and `owner model or case count differs from the published qualification`, followed by `ValueError: cross-case qualification failed` | `receipts/regrade-control.log`, `.rc` |
| Against the author's logs | `author-r8/receipts/proofs/extract-regrade.log` and `extract-control.log` | The regrade log is **byte-identical** (`diff` rc 0). The control log differs only on three traceback `File "..."` path prefixes (`$SOURCE` in the author's copy against this clone's path), with the same line numbers 214, 208 and 141 | `receipts/compare-author-proofs-raw.txt`, `compare-author-proofs.txt` |

The refusing line comes from `kept_grade.py:246-248` (`Disposition.__init__`, when only one of `OWED_KINDS` ran). `receipt_regrade.py:106-110` and `:136-141` turn it into `REFUSED` and a failed `qualify`.

**The integrity check is not vacuous.** R927-3's per-case run, on the scrubbed bytes of these 27 files, gave 24 `part integrity failure` results (published at `review-evidence/artysplit-r1/reviews/R927-3/receipts/percase-public.summary`). So the same check that now passes was shown to refuse the altered bytes. A fresh single-file fault probe for this round was not run (see Real limits).

## 3. Prior findings at this head

| Finding | Status at `011aaa6f` / evidence `0cad829e` | Cause-level evidence |
|---|---|---|
| **R927-3 F1** MINOR (`Conformance`, `Tests`, `Docs`): the published census extract does not regrade | **CLOSED** | Every part of R927-3's verification is now met. The inventory gives `RESULT: PASS listed=814` (`INDEX.md` aside). The regrader exits 0 with 147 PASS and the cross-case PASS. The no-`srp-bound` copy is refused with the #977 line. The cause, a length-preserving publication rewrite, is reversed: original == published for all 762 files. The PR body's "Reproduce and inspect" and Definition-of-done claims are now true of the published packet (RS-3 asks only that the PR body pin the evidence commit) |
| **R928-3-F1** (external; the same publication defect, rated MAJOR there) | Its stated verification is **met on public bytes** at `0cad829e`, by the runs in section 2. Closing it is the external reviewer's call | "the unmodified current regrader must reproduce all 147 grades and the cross-case step from the published archive; the missing-`srp-bound` copy must reach and fail the named disposition condition": both hold. No transformation remains to record, because published == original |
| **R927-3 F2** MINOR (`Tests`, `Docs`): the receipt cited for "generated outputs unchanged" is empty | **OPEN (carried to the integration round)** | `author-r8/receipts/gates/builder-split.log` is still 0 bytes at `0cad829e`. `recipes/gates8.sh` still has no builder step. The underlying claim remains true by R927-3's own `receipts/builder-split-identity.txt` |
| **R928-3-F2** (external; extractor part-limit boundary) | **OPEN (carried to the integration round)** | `census_extract.py:59,63` writes parts "of at most PART_LIMIT" bytes. `:120` self-regrades with `limit=PART_LIMIT`, and `receipt_regrade.py:46` refuses `len >= limit`. Unchanged at this head. It is inert for this extract (largest part 13,999,999). This is R927-3 SG-1 in my ledger |
| **R928-3-F3** (external; an overlong line prevents progress) | **OPEN (carried to the integration round)** | `census_extract.py:63-71` is unchanged: when `rfind` returns -1, `end` becomes 0 and the loop never advances. It is inert for this extract (longest observation line 48,411 bytes). This is R927-3 SG-2 in my ledger |
| R927-3 RS-1, RS-2 | **Retained (residue checklist)** | `census_extract.py:11` and `README.md:217` are unchanged at the head. `author-r8/receipts/INDEX.md:5` still reads "Prepared locally; nothing has been posted or pushed." at `0cad829e` |
| R927-3 SG-1 to SG-6 and the retained optional items | Retained as optional, unchanged | No source change |

## Findings

No new BLOCKER, MAJOR or MINOR. The only open MINOR is R927-3 F2, carried above.

### RESIDUE

- **RS-3 (new; PR body, wording only).** "Reproduce and inspect" (PR body line 111) says "`receipts/census-extract/` in this round's packet" and pins no evidence commit. The earlier publication at `7ae7427b` (and `3fc4a9d0`) carries the scrubbed bytes, which do not regrade. So a reader following an older evidence link reproduces the failure, not the claim.
  - Exact fix: replace "(`receipts/census-extract/` in this round's packet)" with "([`receipts/census-extract/`](https://github.com/kebag-logic/milan-fpga/tree/0cad829e1af15b9c96b0ef3d10d109b9721154c5/review-evidence/artysplit-r1/author-r8/receipts/census-extract), republished byte-exact at evidence `0cad829e`; earlier publications of 27 of its parts were altered by the archive scrub and do not regrade)".
  - Why RESIDUE: it changes no measurement, figure, verdict, test, code or claim, and the claim is already true of the current packet.
- **RS-1 and RS-2** are retained from R927-3 with the exact fixes given there.
- **No new source-comment instance** of a lane label, review round, reviewer ID or comment ID: this round has no source delta.

### SUGGESTION

- **SG-7 (new).** Add a short republication note to `author-r8/receipts/INDEX.md` or the PR, naming `0cad829e`, the 27 files and "original == published". The record of this correction then sits beside the extract and not only in an evidence commit message. Optional: `MANIFEST.json` already proves it.

## Lens results at this head

```text
[R927] PASS Conformance — evidence 0cad829e: review-evidence/artysplit-r1/author-r8/receipts/census-extract + MANIFEST.json; receipts/regrade-published.log, regrade-control.log, publication-check.log — 147 grades and the cross-case step reproduce from public bytes; the no-srp-bound control is refused by the #977 disposition (kept_grade.py:246-248); R927-3 F1's Conformance half closed
[R927] PASS RTL — no source delta since R927-3 at the same head (receipts/regrader-identity.txt, clone-restore.txt: tree 5b11a07d, index = HEAD) — R927-3's RTL coverage at 011aaa6f retained; the evidence republication touches no RTL, image or build input
[R927] PASS Robustness — no source delta; census_extract.py:59-71,120 and receipt_regrade.py:46,192 unchanged at the head — R927-3's Robustness coverage retained; R928-3-F2/F3 (external ledger) remain open in this code and are carried to the integration round
[R927] MINOR Tests — author-r8/receipts/gates/builder-split.log (0 bytes at 0cad829e) — R927-3 F2 open (carried); F1's Tests half closed by receipts/regrade-published.log and regrade-control.log
[R927] MINOR Docs — author-r8/receipts/INDEX.md "Gates at the head" citing the empty builder-split.log — R927-3 F2 open (carried); F1's Docs half closed (the PR body figures 762 / 1,434,762,896 / 13,999,999 equal receipts/extract-size.txt); RS-1, RS-2 and RS-3 are residue only
```

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Published census extract and `MANIFEST.json` at evidence `0cad829e`; head regrader and `kept_grade.Disposition`; author `proofs/extract-regrade.log`, `extract-control.log`; PR body "Reproduce and inspect" | R927-4 | 011aaa6f080321e0a89f915720ebb3ee14807a16 |
| RTL | CLEAN | Retained: delta path list, post-route reports r7/r6, builder outputs (R927-3); no source delta since | R927-3 | 011aaa6f080321e0a89f915720ebb3ee14807a16 |
| Robustness | CLEAN (own ledger; external R928-3-F2/F3 open under this lens in the external ledger) | Retained: `receipt_regrade.py` limit and integrity paths, `census_extract.py` (R927-3); unchanged at head | R927-3 | 011aaa6f080321e0a89f915720ebb3ee14807a16 |
| Tests | UNCLEAN (R927-3 F2) | Public regrade and control replays, author proof logs, `gates/builder-split.log`, `recipes/gates8.sh` | R927-4 (not covering) | 011aaa6f080321e0a89f915720ebb3ee14807a16 |
| Docs | UNCLEAN (R927-3 F2) | Live PR body; `author-r8/receipts/INDEX.md` at `0cad829e`; evidence commit message; extract size figures | R927-4 (not covering) | 011aaa6f080321e0a89f915720ebb3ee14807a16 |

## Real limits

- **No fresh fault probe.** A single-file probe, putting one republished part's pre-republication bytes back into a disposable copy, was not run in this session. The integrity check's ability to refuse those bytes rests on R927-3's published per-case run (24 refusals on the same 27 scrubbed files), not on a new run.
- **The manager's replay is not public.** The brief reports PASS cases=147, PASS cross-case and the control refusal, but at query time no manager comment on #1004 or #878 since R927-3 published it. The two comments newer than R927-3 are the two review-start lines. The public record of the republication is evidence commit `0cad829e` (its message and `MANIFEST.json`). This round's own replays above are the evidence relied on.
- **Republication proves equality, not original content.** The publisher's `original_sha256` equals the author's `FILES.tsv` hashes and the bytes on disk. That shows the published bytes are the author's inventoried bytes, not that the author's inventory equals the unpublished round-7 traces. As stated in the regrader's docstring, the full-log hash is provenance only.
- **No manager source bank** ran at this head, and none is claimed. Source execution evidence is the author's published gate receipts plus the reviewer replays listed here.
- **Physical calibration NOT RUN.** Field skips are not hardware proof.
- **Hosted state.** At query time the head had 0 hosted check runs, a combined status of `pending` with 0 contexts, and the PR was not a draft. No hosted job executed at this exact head, and none is accepted here.

## Pending manager duties

- Integration round (merge of current `dev-soft-core`; live dev `e275d7950ef3385753e6a15d2e191ba855b171ed`, source base `854bd7236792ce1adbd10c43b13a6a5002ad3bb6`). It must close R927-3 F2 (a non-empty receipt showing identical generated outputs at `4adfa9dc` and the head) and resolve R928-3-F2/F3 (one inclusive/exclusive part-size contract across writer, self-check, CLI and docs; refuse an overlong line; controls for both).
- The current-dev merge-candidate validation (builder and native banks), with receipts linked on the PR.
- Hosted and local-replica acceptance at the final head.
- Residue checklist: RS-1, RS-2, RS-3.
- Maintainer merge authorization and post-merge containment.

## Reproduction (this packet)

- The evidence was fetched read-only (`git fetch --depth=1`, then `--deepen=1`) into a scratch bare repository. `git archive 0cad829e review-evidence/artysplit-r1/{MANIFEST.json,author-r8}` was extracted under `scratch/`.
- `python3 -I scripts/verify_publication.py <artysplit-r1> <parent MANIFEST.json from 3fc4a9d0>` writes `receipts/publication-check.log`.
- `python3 -I scripts/make_control.py <census-extract> <copy>` builds the hard-linked control. Only its `census.json` is rewritten, and the source extract is untouched.
- `python3 -B -E -s <head>/tb/verilator/ctrl_service_budget/receipt_regrade.py <census-extract | copy>` writes `receipts/regrade-published.log` and `regrade-control.log`.
- The clone was verified after the runs (`receipts/clone-restore.txt`):
  - HEAD `011aaa6f`, and the index tree equals the HEAD tree `5b11a07d` (2001 entries).
  - `diff-index` and `diff-files` are clean, and status including ignored files is empty.
  - The six gitlinks in the index equal HEAD.
  - No interpreter cache was written.

R927-4 FINISHED
