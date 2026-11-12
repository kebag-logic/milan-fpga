[R829] POSITIVE - exact head 6eacd76d5f596a88a537dcb4fb5b39a5a2284c3c

Round R829-6 checks the evidence only for PR #892 (issue #665, the tsn-c-stack pin move). The head is the one R829-5 reviewed: `6eacd76d5f596a88a537dcb4fb5b39a5a2284c3c`, tree `9b1d0afb9598f6e2cf73b436e9ddd1d36f75ff0c`. R829-5 (#892 issuecomment-6834290267) was NEGATIVE on one MINOR finding, F3-R, under Tests and Docs. Since then the source has not changed. One evidence archive commit has been added: `b47ec49c1cc34466dc4bd802250674ccf01adedb`, "Publish the corrected round 4 coverage receipt (R829-5 F3-R)". It is contained in `b3523a6a57e913ee6e1976c37cf8e3fdc7f2bcf8`.

**Verdict.** The verdict is POSITIVE.
- F3-R is closed at its cause:
  - the published receipt now carries the real `git diff` of `coverage.ratchet` at `0fb66211`, under a correction header;
  - its manifest entries match;
  - the three round-5 texts that cite it are now true.
- No other finding is open.
- Conformance, RTL and Robustness carry forward unchanged from R829-5 at this same head. Nothing they depend on has changed.
- Tests and Docs are re-covered clean at this head.

## Scope and order

- **Same head, unchanged tree** (`receipts/head-integrity.txt`):
  - HEAD is `6eacd76d…`, tree `9b1d0afb…`, and `gh api pulls/892` reports the same head.
  - The worktree and index equal HEAD, and `git status --porcelain` is empty.
  - The six gitlinks are unchanged: external `efeb541a`, gptp-processor `135afd04`, protocol-processor `a9e84b66`, lwSRP `08ee86e8`, tsn-c-stack `715589c1`, verilog-axis `48ff7a7e`.
  - Since `8bc1dfc0` the head changes only `docs/design/SPLIT_CONTROL_MEMORY.md` and `tb/verilator/ctrl_service_budget/README.md`, the same two pages as in R829-5.
- **What changed in the evidence.** From `c0e0f810` (the round-5 author archive R829-5 reviewed) to `b47ec49c`, exactly three files changed:
  - `author-r4/receipts/round4/fw_coverage-write-at-0fb66211-diff.txt`, rewritten;
  - `author-r5/receipts/round5/fw_coverage-write-at-0fb66211-diff.txt`, new;
  - `MANIFEST.json`, one entry re-hashed and one entry added.

  From `b47ec49c` to `b3523a6a` only the R829-5 review archive was added. No `author-*` file is touched there.
- **The live comments I read** (all read-only):
  - the manager's evidence note, #665 issuecomment-6834296040;
  - the review start, #892 issuecomment-6834313518;
  - REVIEW READY, #665 issuecomment-6832030626. Its live body is byte-identical to R829-5's capture (`receipts/review-ready-live.md`).
- **Prior finding.** The only prior public finding to settle at this head is my own R829-5 F3-R. I read it after the independent checks below, and I resolve it below.

## F3-R: corrected coverage receipt — CLOSED

**1. The receipt carries the real diff, under a correction header.** See `receipts/receipt-check.txt`, produced by `scripts/check_receipt.py`.
- Lines 1 to 3 are a `#` header. The header says the file is corrected in round 5, says round 4's note read the diff as empty and that it is not, and names the two files that are one line higher. The old false annotation, "(empty: …)", is gone.
- The body is a real unified `git diff`. Its index line is `7dc8a5df96..7f3d0792de`:
  - `7dc8a5df96` matches `git rev-parse 0fb66211:sw/firmware/gtest/coverage.ratchet`, which is `7dc8a5df968dc8575d2d0d6854d8a3ac01dcd298`.
  - Applied with `patch` to that blob, the body yields blob `7f3d0792ded263596b9ff76c5fbd2ca95fa226d7`. That is the post-image id the diff names, so the hunks are genuine and complete. The applied image is kept as `receipts/ratchet-0fb66211-with-receipt-applied.txt`.
- It shows exactly two changed rows, `ctrl_app_aecp.c` 164/164 -> 165/165 and `nvm_store.c` 458/458 -> 459/459. Both branch counts are unchanged.

**2. It matches `fw_coverage-write-at-0fb66211.log`.**
- I compared every one of the log's 35 measured rows with the applied image. Lines covered/total and branches covered/total agree on all 35, and the image has no extra rows.
- Neither file contradicts the other in any row, not only in the two rows named.

**3. It matches hosted CI.** See `receipts/hosted-job.json`, `receipts/hosted-job-coverage-lines.txt` and `receipts/hosted-vs-receipt-rows.txt`.
- I fetched the log of hosted job `130955656991` (`firmware-unit`, run `43149571870`, conclusion success) myself. It ran at `55cb2491`, whose tree `3b4b1b9fb64fb7be69a1ec16f0740149fbd383a4` is identical to `0fb66211`'s.
- Its final `fw_coverage --check` table, built with GCC 13.3, reads `ctrl_app_aecp.c 165/165` and `nvm_store.c 459/459` lines, and `firmware coverage: PASS (35 files)`. This agrees with the receipt and confirms `coverage-provenance.txt:7`.
- Across all 35 rows, the hosted table differs from the receipt's image in two places outside what the receipt claims:
  - `srp_mbx.c` lines: hosted 542/542; 543/543 in the receipt and in `0fb66211`'s committed ratchet;
  - `ctrl_app_aecp.c` branches: hosted 126/126; 124/124 in the receipt.

  Both differences are GCC 13.3 against GCC 16.2 counting the same 100 % differently. The `srp_mbx.c` row is dev's own committed value, which this PR does not touch, and the hosted gate compares fractions and passed. No round-5 text claims these rows agree with the hosted run. This is a limit, not a finding (see S1).

**4. The manifest hashes match.** See `receipts/author-packet-manifest-check.txt`, produced by `scripts/verify_author_packet.py` on the extracted `b3523a6a` archive.
- `author-r4/`: 479 entries listed; 0 missing, 0 hash mismatches, 0 unlisted.
- `author-r5/`: 156 entries listed, which is R829-5's 155 plus the new copy; 0 missing, 0 mismatches, 0 unlisted.
- Both receipt copies have sha256 `6a7cda0a258817f462298c4fbb1b401151b0cfa27d6c1b205329c5b98b434773`. Both `MANIFEST.json` entries give that value as their original and published hash, with `path_redacted: false`. The two copies are byte-identical.
- The archive commits `b47ec49c` and `b3523a6a` carry no signature (0 `gpgsig` headers). Integrity rests on the manifest, as in earlier rounds.

**5. The three citing texts are now true.** See `receipts/citing-texts.txt`. These texts are byte-identical to the versions R829-5 read. What changed is that the file they cite now exists in the corrected form.
- `author-r5/receipts/round5/coverage-provenance.txt:6` cites "round4/fw_coverage-write-at-0fb66211-diff.txt, corrected". That file now carries the correction. True.
- `author-r5/HANDOFF.md:16` says round 4's file "carries the real diff under a correction header". True.
- REVIEW READY (#665 issuecomment-6832030626), F3 bullet: "The corrected receipt (the real diff, under a correction header) … [is] in the round-5 packet". The copy is in `author-r5/receipts/round5/`. True.

F3-R's required outcome named two options. The manager took both: the `author-r4` receipt was re-archived with its manifest entry updated, and a copy was added to `author-r5/` and listed. Each verification step R829-5 named passes. F3-R, and R829-4 F3 beneath it, are resolved.

## Findings

No BLOCKER, MAJOR or MINOR finding is open. There is no RESIDUE in this delta:
- No source comment changed; the source tree is unchanged.
- The receipt header names a review finding ("R829-4 F3"). That is evidence text, not source, and is allowed there.

**S1 — SUGGESTION — Docs, Tests — `author-r5/receipts/round5/coverage-provenance.txt:7`.**
- The line says hosted CI measures "the same" two figures. That is true.
- A reader comparing the whole table would also see that the hosted GCC 13.3 run counts `srp_mbx.c` at 542/542 lines and `ctrl_app_aecp.c` at 126/126 branches, against 543 and 124 on this host. Both are 100 %, and `--check` compares fractions.
- Optional: one sentence saying that line and branch totals differ by compiler would forestall the question.
- This changes no claim, so it is optional, and it can go on the #495 checklist with R829-5's suggestions.

## Prior findings at this head

| Finding | Status at `6eacd76d` | Evidence |
|---|---|---|
| R829-5 F3-R (MINOR, Tests and Docs) | CLOSED | sections 1 to 5 above |
| R829-4 F3 (retained by R829-5 as F3-R) | CLOSED | the same; provenance was already closed in R829-5 |
| R829-4 F1, F2 and RES-2, RES-3 | Closed in R829-5; the tree has not changed since | R829-5 report |
| RES-1, RES-4, RES-5 and S1 to S5 from earlier rounds | Carried to #495 as ruled. They are wording or optional and do not affect lens coverage | R829-5 pending duties |

## Reviewer-owned ledger

| Lens | CLEAN / UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Carried from R829-5, with the head and tree unchanged (`receipts/head-integrity.txt`). R829-5's artifacts: owner decision 6824896581; ruling 6830569282; `SPLIT_CONTROL_MEMORY.md:366-385`; `ctrl_memory.py:246-255` | R829-5 (still valid in R829-6) | `6eacd76d5f596a88a537dcb4fb5b39a5a2284c3c` |
| RTL | CLEAN | Carried from R829-5. There is no RTL in the head's delta from `8bc1dfc0`, and the tree and gitlinks are unchanged (`receipts/head-integrity.txt`) | R829-5 (still valid in R829-6) | `6eacd76d5f596a88a537dcb4fb5b39a5a2284c3c` |
| Robustness | CLEAN | Carried from R829-5 (`ctrl_memory.py:246-261`, `split_soc.py:456`, `build.py:179-184`); tree unchanged | R829-5 (still valid in R829-6) | `6eacd76d5f596a88a537dcb4fb5b39a5a2284c3c` |
| Tests | CLEAN | `receipts/receipt-check.txt` (patch applies to `0fb66211`'s blob, post-image `7f3d0792`, all 35 rows equal to the log); `receipts/hosted-vs-receipt-rows.txt`; `receipts/hosted-job-coverage-lines.txt`; `receipts/author-packet-manifest-check.txt`; head ratchet rows (`ctrl_app_aecp.c` 165/165, `nvm_store.c` 459/459) | R829-6 | `6eacd76d5f596a88a537dcb4fb5b39a5a2284c3c` |
| Docs | CLEAN | `receipts/citing-texts.txt` (`coverage-provenance.txt:6`, `HANDOFF.md:16`, REVIEW READY F3 bullet); `receipts/review-ready-live.md`; the corrected receipt in `author-r4` and `author-r5` at `b3523a6a`; `MANIFEST.json` entries. The two edited pages and the docs gates are carried from R829-5, with the tree unchanged | R829-6 (with the R829-5 docs gates) | `6eacd76d5f596a88a537dcb4fb5b39a5a2284c3c` |

All five lenses are covered clean at `6eacd76d5f596a88a537dcb4fb5b39a5a2284c3c`.

## Real limits

- **Evidence-only round.** I ran no firmware, coverage, campaign, Verilator, Yosys or docs gate in this round. The source is unchanged since R829-5, so the R829-5 docs gates and the R829-4 bank results at `8bc1dfc0` still apply because nothing they test has changed, not because they were run again.
- **The coverage measurement was not repeated by me.** The host measurement at `0fb66211` is the author's published log. It is corroborated by an independent hosted run on the identical tree, whose log I fetched myself.
- **Hosted CI on `6eacd76d` has not finished.** At review time: 4 success, 1 skipped (the physical gPTP nightly), 6 in progress, 34 queued (`receipts/hosted-check-runs-6eacd76d.tsv`). I claim no hosted result for this head; hosted and act acceptance is the manager's.
- **No manager source bank** runs at this head, and I infer none.
- **No physical evidence.** No physical calibration was run. Skipped field contexts are not hardware proof.
- **Unsigned archives.** The evidence archive commits are unsigned. Integrity rests on the manifest only.
- **Probes.** I made no probes or mutations and no edits to this clone. Restoring the tree was therefore not needed, and the clone was verified clean at the end.

## Pending manager duties

- Own hosted and act acceptance for `6eacd76d`. Most hosted contexts were still queued or running.
- At the merge turn, build and validate the current-dev candidate on live dev `b7d692952305e4e0e132abb8f99c339eeb17a873` (source base `1d6bf555`), with the builder and native banks.
  - Order this PR against #810's STOP ruling (issuecomment-6831583372) on `ctrl_memory.LEDGERED`'s fixture point.
  - Whichever lands second re-measures and restates the key and the section-5 text.
- Carry these on the #495 residue checklist: RES-1, RES-4, RES-5, the earlier S1 to S5, and this round's S1.
- Publish this packet: `REPORT.md` and the files listed in `MANIFEST.sha256`.

R829-6 FINISHED
