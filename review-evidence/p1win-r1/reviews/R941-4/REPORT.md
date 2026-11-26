[R941] POSITIVE - exact head 079c4fa1514be460949ddc28ae3277ea1873cb48

# R941-4: narrow receipts re-review of PR #1017 (Relates to #1009), same head as R941-2/R941-3

Head `079c4fa1514be460949ddc28ae3277ea1873cb48`, tree `be2122cbd487361b4ed8a99ff283565c1bec3eb2`. There is no code change since R941-3. Scope: R941-3-F1 (the si0 power-cycle case at 8x8/1if) and R941-3-RES1, judged against the round-4 author packet `review-evidence/p1win-r4/author` (evidence branch `p1win-review-evidence` at `0fc00475cc8f72934a6738e3e45616cf2fc17b3a`), the live PR body, and the manager's ruling (PR comment 7191672753, corrected by 7191857005).

## Summary

- **R941-3-F1 is resolved.** It is resolved by route 2 of its required outcome: a public manager ruling accepts the harness correction and the rerun, and the PR cites it. Most of route 1's receipts are also published:
  - the rerun's identity: head, image hashes, test revision `27734fa0`, environment, start and end times, rc;
  - the rerun's report as numbers;
  - the failing run's per-attempt outlet, return, withdraw, last-frame and probe times, which the diagnosis rests on.

  Every derived figure I recomputed matches its primary numbers, with one labelling exception (RES4).
- **The ruling's two points agree with the receipts.**
  - The cut is still issued at t+1.000 and the drain is 1.0 s.
  - The withdraw came 1.001 s after the power-off command returned.
  - The settle counted was a PROBE_TX_RESPONSE 8.15 s after the relay's power-on, so after this attempt's own power-on.
  - The verdict rule ("Talker declared before the settle") is unchanged.
- **The image is the head's in substance.** The bitstream was built at `8a4ad2c4`, and `8a4ad2c4..079c4fa15` changes six files. None of them is an HDL, SoC or gateware file. The one compiled file in the six is `nvm_store.h`, and its change is a comment with the same line count. The gitlinks are equal. Its hashes match round 1's image receipt.
- **R941-3-RES1 is resolved** with the exact prescribed text, at PR body line 78.
- **No finding blocks.** Four wording residues and five suggestions are listed below so they can all be absorbed in one pass.

## How I reconstructed this round

1. I read `AGENTS.md`, the review-start comment 7191872088, and the ruling and its correction.
2. Then I did my own pass over the round-4 packet.
   - I checked both manifests: `MANIFEST.json` gives original = published for all 7 files, and `sha256sum -c author/MANIFEST.txt` passes for all 6.
   - I diffed the live PR body against `PR-BODY.md`. They are identical apart from the leading `[A844]` line and blank lines, so the packet's line numbers are the live body's minus 2.
   - I checked the three `board/` receipts against each other, against round 2's `board/summary-8x8.txt` and `summary-1x1.txt`, against round 3's `cuts/cuts-8x8.txt` and `board/summary-8x8-input0.txt`, and against round 1's `receipts/win/images.txt`.
3. Only after that did I read R941-3's F1 and RES1 text, and I resolved them against what I had found.

## Evidence checked

| Claim | Receipt | Check |
|---|---|---|
| Rerun bound to the head | `si0-identity.txt:3,13-18,25-28` | Bitstream `aaf4a60a…` (3,825,992 B) and `ctrl_app.elf` `6c82d962…` are identical to round 1 `images.txt:37-38`, which records the 8x8 image built from a clean clone of `8a4ad2c4`: WNS +0.045, WHS +0.036, 45,973 LUTs. `receipts/image-equivalence.txt` covers `8a4ad2c4..079c4fa15`: 6 non-build files, one comment changed in `nvm_store.h` with the same line count, and all 6 gitlinks equal. The firmware rebuilt byte-identical at the head is the author's statement. I did not reproduce it: it needs the image's CSR and flash maps and runtime archives. |
| Test revision and environment | `si0-identity.txt:4-7,35-38` | `27734fa0` / tree `fc24bd8f`, matching the ruling. `CERT_CUT_HOLD_S=1.0` is unchanged. `CERT_POWER_DRAIN_S=1.0` is the ruling's item 1. |
| Times and rc | `si0-identity.txt:10-12,31-39` | The order holds: flash 10:58:41, boot 10:59:32.987, start 10:59:53, bind 11:00:30.218, power-on 11:00:42.845, cleanup 11:00:52.608, end 11:00:59.784. The epoch values convert to these wall times. rc 0, and "1 scenario passed" agrees with round 3's `summary-8x8-input0.txt`. |
| Rerun report figures | `si0-report.txt` | Recomputed in `receipts/receipt-arith.txt`. The matches are t-1.005, off t+1.551, on t+12.627, withdraw t+3.068 (1.001 s after the return, 1.286 s after the last frame), durable 1.196 s before the last frame, declaration 4.18 s after the relay's instant and 4.74 s after the test's reference, and probe response 3.974 s after the declaration. The bracket (48.8 ms) and first sample (0.079 s) are the same as round 3's summary line. |
| Failing-run diagnosis | `fail-8x8-input0.txt:9-20` | Recomputed: return after off 0.382, 0.441 and 0.595 s; last frame after return +37 ms and +1 ms (as the ruling's correction states) and −410 ms at attempt 3; graded probe 20.64, 20.63 and 21.56 s before the declaration. The cut offsets 1.488, 23.130 and 44.836 s equal round 3's `cuts-8x8.txt` cuts 28-30, whose attempts read RETRY ×3 and "FAIL at attempt 3". |
| "0.39 to 0.62 s over 36 graded cuts; 0.42 to 0.59 s over 8" | `fail-8x8-input0.txt:23-24`; PR body 166-167 | Reproduced from round 2's summaries as 0.386 to 0.619 and 0.424 to 0.586 (`receipts/lastframe-range.txt`). |
| "command returned 0.38 to 0.60 s after that instant" over 36 cuts | `fail-8x8-input0.txt:24`; PR body 167-168 | Stated, but not itemised in any public receipt. See S1. |
| Bind durable 0.579 s, 1.328 s before the last frame | PR body 173-174 | Round 2 `summary-8x8.txt`, sink line 28: 0.579 s, last frame 1.907, 1.328 s. |
| RES1 | PR body line 78 | Byte-for-byte R941-3's prescribed replacement. The diff from round 3's `PR-BODY.md` changes only that row and the si0 paragraphs. |

## Findings

No BLOCKER, MAJOR or MINOR.

**R941-4-RES1 RESIDUE - Docs - the direction of the probe.** The text is at `PR-BODY.md:169` (live 171), at `board/fail-8x8-input0.txt:17` and `:25`, and in the ruling 7191672753, item 2.
- **Evidence.** The DUT, as Listener, sends PROBE_TX_COMMAND and T answers with PROBE_TX_RESPONSE. The receipts' own table says so ("T's PROBE_TX_RESPONSE"), and so does `si0-report.txt:20` ("the DUT's probe, answered by T"). The prose reverses this: "the DUT … answered a probe", "the boot that answered it", "a probe the DUT answered".
- **Exact fix.**
  - PR body: "At attempts 1 and 2 the DUT, still up, sent a probe that T answered within 39 ms of the withdraw; that probe was the DUT's last frame."
  - Receipt row 17: "the boot that sent the probe".
  - Receipt line 25: "the DUT was still up at the withdraw and sent a probe, its last frame, that T answered within 39 ms of it".
  - For the ruling's own text (the manager's checklist): "counts as its settle only T's answer to a probe the DUT sent after that attempt's own power-on".

**R941-4-RES2 RESIDUE - Docs - where the drain is counted from.** The text is at `PR-BODY.md:176` (live 178), "after the cut it waits 1.0 s before the withdraw", and at `board/si0-identity.txt:36`, "the wait after the cut before T's withdraw". The ruling's item 1 has the same wording.
- **Evidence.** The withdraw came 1.001 s after the power-off command returned and 2.068 s after the cut was issued (`si0-report.txt:9,12-13`). So the 1.0 s drain is counted from the command's return.
- **Exact fix.** PR body: "after the power-off command returns it waits 1.0 s before the withdraw". Identity: "the wait after the power-off command returns, before T's withdraw".

**R941-4-RES3 RESIDUE - Docs - when attempt 3's probe came.** The text is at `PR-BODY.md:170-171` (live 172-173), "before that attempt's cut", and at `board/fail-8x8-input0.txt:26-27`, "after the attempt began and before its cut".
- **Evidence.** The same receipt's row 16 puts the probe at 44.438, which is 0.235 s *after* the cut was issued (44.203) and 0.398 s before the relay's power-off (44.836).
- **Exact fix.** In both places: "after that attempt's cut was issued and before the power went off".

**R941-4-RES4 RESIDUE - Docs - the power-on reference is not named.** The text is at `board/fail-8x8-input0.txt:19`: "(11.68 s after power-on)", "(11.63 s)" and "(11.56 s)".
- **Evidence.** Measured from the relay's power-on instant in row 18, the declarations are 11.071, 11.037 and 11.017 s after power-on (`receipts/receipt-arith.txt`). The stated figures are 0.543 to 0.609 s larger. That matches the lag of about 0.56 s between the test's power-on reference and the relay's instant that `si0-report.txt:16` gives, so the figures are measured from the test's reference and only the label is off. No PR claim uses them, and the graded comparison (20.64, 20.63 and 21.56 s) is correct.
- **Exact fix.** "(11.68 s after the test's power-on reference, 11.07 s after the relay's)", and likewise "(11.63 s; 11.04 s)" and "(11.56 s; 11.02 s)".

**R941-4-S1 SUGGESTION - Docs - the return range over 36 cuts is not itemised.** The text is at `PR-BODY.md:167-168` and `board/fail-8x8-input0.txt:24`.
- The PR's last-frame range over the 36 graded cuts reproduces from round 2's summaries, but the 36-cut range for the power-off command's return has no itemised public receipt.
- Its stated range, 0.38 to 0.60 s, is exactly the three input-0 attempts' 0.382 to 0.595, and the 0.595 is the ungraded cut 30.
- The range carries no conclusion: a 1.0 s drain exceeds the 0.62 s maximum last frame whatever the return time.
- Either publish each graded cut's return offset, or scope the sentence to "at the three attempts on input 0 the command returned 0.38 to 0.60 s after that instant".

**R941-4-S2 SUGGESTION - Docs - name the image's build commit.** The text is at `PR-BODY.md:181`, "The image: the head's".
- Add that the image was built at `8a4ad2c4`, and that `8a4ad2c4..079c4fa15` changes no HDL, SoC, gateware or compiled source beyond one comment of the same line count. I verified that in `receipts/image-equivalence.txt`.
- The PR body nowhere names the commit its images were built from.

**R941-4-S3 SUGGESTION - Docs - cite the ruling's correction.** At `PR-BODY.md:179`, link the ruling's correction (7191857005) beside the ruling. The PR already uses the corrected reference: last frames are measured from the relay's instant.

**R941-4-S4 SUGGESTION - Tests/Docs - explain the post-power-on declaration time.** At `board/fail-8x8-input0.txt:19` versus `si0-report.txt:18`:
- In the failing run, T's Talker declaration "at the DUT's first ENTITY_AVAILABLE" came about 11.0 s after the relay's power-on at every attempt. In the rerun it came 4.18 s after.
- Neither of the ruling's two changes evidently accounts for that difference, and the receipts do not say why.
- There is no risk to the verdict: PASS requires the declaration before the settle, so a later declaration can only produce RETRY, never a false pass.
- A sentence on its cause, for example the old test's wait for the first ENTITY_AVAILABLE, would close the question for a cold reader.

**R941-4-S5 SUGGESTION - Tests - say which change the rerun exercised.** At `si0-report.txt:10-12`:
- In the rerun the DUT's last frame (t+1.782) came 0.285 s before the power-off command returned (t+2.067). So the old withdraw-at-return would also have come after the board was down, and this rerun does not exercise the drain.
- The PR states only that the case passed under the corrected test. That is accurate, but the PR could say which change the pass exercised.

**Comment-rule scan.** There is no source delta this round, so no new source comment exists. The `[A844]` header and lane names in the PR body and packet are PR or packet text, which the rule allows.

## Prior public findings, resolved or retained at this head

| Finding | Disposition at 079c4fa1 |
|---|---|
| R941-3-F1 MINOR (Conformance, Robustness, Tests, Docs) | **Resolved**, by route 2 (ruling 7191672753, cited at `PR-BODY.md:179`), with most of route 1's receipts. The rerun is bound to the head's image and to test revision `27734fa0` with an unchanged cut hold. The report lines F1 asked for (bind, cut, verdict, post-power-on ENTITY_AVAILABLE and declaration, Asking Failed) are published. The diagnosis is restated on per-attempt receipts. Residual wording: RES1 to RES4. Optional: S1 to S5. |
| R941-3-RES1 RESIDUE (Docs) | **Resolved**, with the exact prescribed text (`PR-BODY.md:78`). |
| R941-2-F1, R941-2-RES1, RES2, S1, S2; R942-1-F1/F2; R941-1-RES1/S1/S2 | Carried as R941-3 disposed them (resolved or done). Nothing at this head changes them. |

## Lens results

[R941] PASS Conformance - `board/si0-identity.txt:33-38`, `board/si0-report.txt:5-25`, ruling 7191672753/7191857005, round 3 `cuts/cuts-8x8.txt` cuts 28-30 - issue criterion 2's fourth 8x8/1if scenario is now shown on input 0. The scenario is Talker Failed declared before the settle, with Asking Failed New 0.2 ms and REGISTERING_FAILED 1.9 ms after T's PROBE_TX_RESPONSE, inside the 1.0 s window. It ran under a ruled-on test revision with the cut hold unchanged at 1.0 s. RES1 to RES3 are wording only.

[R941] PASS RTL - `receipts/image-equivalence.txt` (`git diff --stat 8a4ad2c4..079c4fa15`, gitlinks at both) and round 1 `images.txt:24-38` - there is no RTL in the delta and no code change since R941-3's RTL coverage at this head. The rerun's bitstream is the routed `8a4ad2c4` image, whose HDL, SoC and gateware sources equal the head's.

[R941] PASS Robustness - `board/si0-report.txt:7-14` and round 2 `summary-8x8.txt` sink line 28 - restore after a power cut at si0 is now receipted. The store was idle at the bind and durable at t+0.586, 1.196 s before the last frame (rule 250 ms). The failing run's bind was durable 0.579 s after its response, 1.328 s before its last frame. The retries without a bind take no hold reading, as before.

[R941] PASS Tests - `board/si0-identity.txt:4-7,35-38`, `board/fail-8x8-input0.txt:9-20`, `receipts/receipt-arith.txt` - the correction is accepted publicly by the ruling, and its two points match the receipts: the drain counts from the power-off command's return, and the settle probe came after the attempt's own power-on. The verdict rule is unchanged, and stale settles in the failing run explain RETRY ×3. S4 and S5 are optional.

[R941] PASS Docs - live PR body = `author/PR-BODY.md` (plus the `[A844]` line); `README.md`, `REVIEW-READY.md`, `MANIFEST.json` and `MANIFEST.txt` (all hashes OK) - the si0 paragraphs state every figure for the case with a receipt (S1 asks for one aggregate to be itemised). RES1 of R941-3 is applied exactly. RES1 to RES4 of this round are wording only.

## Reviewer-owned completion ledger

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | ruling and correction; `si0-identity.txt`; `si0-report.txt`; `fail-8x8-input0.txt`; r3 `cuts-8x8.txt`; PR body 164-194 | R941-4 | 079c4fa1514be460949ddc28ae3277ea1873cb48 |
| RTL | CLEAN | `receipts/image-equivalence.txt`; r1 `images.txt`; no code delta since R941-3 (RTL clean there at this head) | R941-4 (R941-3 at the same head) | 079c4fa1514be460949ddc28ae3277ea1873cb48 |
| Robustness | CLEAN | `si0-report.txt`; r2 `summary-8x8.txt`/`summary-1x1.txt`; `receipts/lastframe-range.txt` | R941-4 | 079c4fa1514be460949ddc28ae3277ea1873cb48 |
| Tests | CLEAN | `si0-identity.txt` (revision, environment, rc); `fail-8x8-input0.txt`; `receipts/receipt-arith.txt` | R941-4 | 079c4fa1514be460949ddc28ae3277ea1873cb48 |
| Docs | CLEAN (RES1 to RES4 are residue only) | live PR body vs `PR-BODY.md`; packet `README.md`, `REVIEW-READY.md`, manifests | R941-4 | 079c4fa1514be460949ddc28ae3277ea1873cb48 |

## Probes and receipts (this packet)

- `scripts/lastframe_range.py` → `receipts/lastframe-range.txt`: the last frame after power-off for each graded cut, from round 2's summaries. It also records the sha256 of the summaries used.
- `scripts/receipt_arith.py` → `receipts/receipt-arith.txt`: recomputes the derived figures of `si0-report.txt` and `fail-8x8-input0.txt` from their own primary numbers.
- `receipts/image-equivalence.txt`: the diff `8a4ad2c4..079c4fa15`, the `nvm_store.h` hunk and the gitlinks at both commits.
- `receipts/clone-integrity.txt`: the clone after review is at HEAD and its tree, with 0 status entries, the index equal to HEAD and the worktree, and the 6 gitlinks unchanged. It also holds the packet's hash check.
- No source was edited and no build, simulation, bench, Docker or act runs were made.

## Real limits

- The qualification harness and the run logs are private. I did not see the correction's diff, as instructed. The receipts are the author's extractions of the private logs.
- I cannot verify the following:
  - the 13 files' mtime-based freeze;
  - the firmware rebuilt byte-identical at the head (it needs the image's CSR and flash maps and runtime archives);
  - the 36-cut return range (S1).
- The evidence commit `0fc00475` is not cryptographically signed, and neither are the earlier archive commits. Integrity rests on the two manifests, which verify.
- The rerun is one case on one board at one attempt, and it did not exercise the drain (S5). Physical calibration was NOT RUN. Field skips are not hardware proof.
- No manager source bank runs at this head. I did not inspect hosted contexts this round. Source-head execution evidence is the author's published gate receipts.

## Pending manager duties

- Validate the current-dev merge candidate at the merge turn: source base `c34e7d8b06739a22cc79997a9a1f4cbcd9bd0350`, live dev `e275d7950ef3385753e6a15d2e191ba855b171ed`, builder and native banks. Link its receipts on the PR.
- Hosted and act acceptance at the exact head.
- Carry R941-4-RES1 to RES4 to the residue checklist, including the ruling's own wording in RES1 and RES2.
- The PR's "Before it lands" items stay open: the boot comparison, and a decision on the board reading's resolution.
- Maintainer authorization for the merge.

R941-4 FINISHED
