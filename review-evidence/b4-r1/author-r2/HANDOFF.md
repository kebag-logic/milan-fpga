# B4 round 2 handoff: [A469], PR #627 wording fixes

Status: DONE, REVIEW READY posted on #451 (see "Public comments"). Local commit only: not pushed, PR not edited.

- Lane: `$LANES/b4-bench-1001`, branch `b4-bench-1001`.
- Start head: `35a60c8d6ee742216f98232c85926b435ab01b91` (round 1).
- New head: `c39312b4871c8cc3ca604eb7c57f4b0b45d914e0`, tree `d9b3febc6f776dce41435775941fe960f1e1b6f1`. It is one commit on `35a60c8d`, with a one-line subject, no body and no trailers.
- Assignment: issue #451 comment 5925185587.
- Round-1 reviews: PR #627 comments 5925175550 (R422-1) and 5925182051 (R423-1). Both NEGATIVE on wording only.
- No bench access, no lock taken, no NAS write, no push, no PR edit, no existing comment edited or deleted.

## The change

One file: `docs/findings/451_TDM8_TIMING_SOC_BOARD.md`. Line numbers are at `c39312b4`. `docs/findings/README.md` (the index row) is unchanged (`git diff --quiet 35a60c8d HEAD -- docs/findings/README.md` rc 0).

| Item | Finding | Page lines | Change |
|---|---|---|---|
| 1 | R422-1 F1 | `:116-117` | "921.6 MB at full length" (600 s) becomes "967.7 MB at the full 630 s" (630 s x 1,536,000 B/s = 967.68 MB) |
| 2 | R422-1 F2, R423-1 S1 | `:36` | Verdict cell: "47,997.947 Hz on the SoC board's uncalibrated clock". Evidence cell: -42.8 ppm against 48 kHz; -10.64 ppm is the plan; the remaining -32.1 ppm is the DUT oscillator's error relative to the SoC board's clock, unsplit and unquantified; +-0.12 ppm granularity |
| 2 | R422-1 F2, R423-1 S1 | `:244-250` | "the sum of both boards' clock errors" becomes the signed relative error: about the DUT oscillator's error minus the SoC board clock's, since a fast SoC board clock lowers the measured fs. No reference splits it, and neither board's own error is quantified |
| 2 | R422-1 F2, R423-1 S1 | `:315-320` | fs bullet: "shown on the SoC board's clock, which is not calibrated"; -42.8 ppm from 48 kHz, -10.64 ppm of it the plan, the remaining -32.1 ppm the DUT oscillator's error relative to the SoC board's clock, not split and not quantified per board. "48 kHz at the board's accuracy" is gone |
| 3 | R423-1 F1 | `:303-314` | "A one-bit offset either way would break every class of word check" becomes the checks each direction trips. Early: tag checks and ordinal steps (channels 0 to 3 wrong tags, channels 4 to 7 above 8 and invalid in every frame, every step doubled); torn, low byte and zero words clean. Late: tag, low-byte and torn-frame checks (channel 0 tag 0 in every frame, ordinal bit 0 in the low byte of every odd frame, other channels wrong tags, every frame torn); only zero words clean |
| 4 | R422-1 S1 | `:61` | "every identity value equals that page's" |
| 4 | R422-1 S2 | `:350` | "about 55 s" becomes "58.7 s" before the unbind |
| 4 | R423-1 S2 | `:154-157`, `:303-305` | The one bit of data delay is the McASP driver's mapping of the `dsp_a` format in the hardware description, not a register readback; the lane's rules allowed no direct read of a McASP register |
| 4 | R423-1 S3 | `:16-18`, `:97-99` | The owner logged the console in as root; the root shell was confirmed with `id` (uid 0), and no credential was typed or stored. The Method's list of SoC reads adds the shell's identity check (`id` and `tty`) |

No measured figure changes. "48 kHz within the SoC board's clock accuracy" appears in no verdict and nowhere on the page.

Wording notes:

- The assignment says "device tree". The page says "hardware description", its existing term, because `scripts/check_baremetal_only.py` refuses the other spelling in any tracked file.
- "The DUT oscillator's error relative to the SoC board's clock, unsplit and unquantified" is the assignment's wording. The body text spells "unsplit and unquantified" out as "not split between the two boards, and neither board's own error is quantified".

## Evidence for the figures

- **967.7 MB.** The capture command in `b4-a468/runs/timing-long/soc-capture.log` has `-d 630`. 630 s x 8 x 4 B x 48,000 = 967,680,000 B. This equals R422-1's `full_630s_MB: 967.68`.
- **58.7 s.** The talker's `end` record in `b4-a468/runs/timing-long/controller-logs.txt` is at t = 1790828918.128055. The `unbind` event in `events.jsonl` is at t = 1790828976.782734. The difference is 58.65 s.
- **One-bit offsets.** `tools/offset_probe.py` synthesizes the first-light pattern as a TDM8 line and runs each case through the packet's own decoder, `b4-a468/tools/decode_capture.py` (SHA-256 `cfb7121b589fe231e139012646fe567b76022e694e08d3bb89d8a7481bda2568`, equal to R423-1's). Ordinals start at 0x7f00, so bit 15 changes inside the run, and the sequence carries one repeat and one skip. Receipt: `receipts/offset-probe.json`.
  - Aligned: PASS shape, steps +1 with the one repeat and the one skip.
  - One bit early: torn 0; 0 words with a nonzero low byte; 0 zero words; channels 0 to 3 tags 2/3, 4/5, 6/7 and 8 (9 is invalid); channels 4 to 7 invalid in all 4,096 frames; steps 4,093 x +2, the repeat 0, the skip +4.
  - One bit late: torn 4,096 of 4,096; 16,384 low-byte words (8 channels x 2,048 odd frames); 0 zero words; channel 0 tag 0 in all 4,096 frames; the other channels tags 1, 1, 2, 2, 3, 3, 4; no steps (every frame torn).
  - Both round-1 probes (`receipts/probe_bit_offset.txt` in the R423-1 packet and `receipts/shift-probe.txt` in the R422-1 packet) agree.

## Byte-identical table proof

Page, `35a60c8d` against `c39312b4`:

- `tools/table_proof.py` (receipt `receipts/table-proof.txt`) finds 12 tables in each revision. Tables 2 to 12 are IDENTICAL, with the same SHA-256 each: identity, both framing tables, `timing-run`, `timing-channels`, the ordinal steps, `timing-fs`, the event timeline, bench as left, and both artifact-hash tables. Table 1, the verdict table, differs only in the FSYNC row (old line 35, new line 36).
- A plain `diff` of every `|` line in the two revisions (receipt `receipts/table-lines.diff`, 89 lines each) is one changed line, `6c6`, the FSYNC verdict row, and nothing else.
- Rendered and source cell counts (`gates/table-451_TDM8_TIMING_SOC_BOARD.txt`, round 1's `table_render_check.py` in the pinned Markdown environment, rc 0) are byte-identical to round 1's receipt (`cmp` equal).

PR body, round 1 against round 2:

- A plain `diff` of every `|` line (receipt `receipts/pr-body-table-lines.diff`) shows only the five added lines of the new Round 2 probe table. Every round-1 table in the body is unchanged.
- Rendered cell counts are constant in all 5 tables (`receipts/pr-body-table-render.json`, ok true).

## Gates at `c39312b4`

All 12 invocations rc 0, unpiped, from the physical `/data` lane path (`gates/gates.txt`, one output file per gate). The Markdown gates used `$VALIDATION_TOOLS/md-venv-40cdefe08ebd/bin/python`.

| Gate | Result |
|---|---|
| `scripts/docs_check.py` | 0 findings across 182 md files |
| `scripts/check_doc_style.py` | OK |
| `scripts/gen_toc.py --check` | OK |
| `scripts/check_em_dash.py --base e4b771f9` | 0 findings over 393 added lines in 2 pages |
| `scripts/check_doc_paths.py` | 861 paths resolve |
| `scripts/ci_scope.py --selftest` | PASS |
| `scripts/check_baremetal_only.py --check` | 0 findings across 951 files |
| `scripts/check_feature_status.py --self-test` | 46/46, 0 findings |
| `git diff --check` | clean |
| `git diff --check e4b771f9 HEAD` | clean |
| `git diff --check 35a60c8d HEAD` | clean |
| `scripts/gen_toc.py --verify-anchors` | 283 links |

`git status --porcelain` after the gates: empty (`gates/status-after.txt`).

## Token scan

Run over every file in this directory just before REVIEW READY, and again after the final manifest:

- **Private names.** 0 hits. The patterns were loaded at run time from round 1's private redaction map: 54 literal patterns and 1 regex covering the bench and controller host names, interface names, account name, MACs, addresses, the peer's and grandmaster's identifiers, and home paths. None was copied into any file. Generic patterns found no MAC, IPv4 or IPv6 link-local address, home path or interface name. The only EUI-64-shaped hit is the DUT's public entity ID `020000fffe000001` in PR-BODY.md, which the redaction rule retains.
- **Agent tool and model names.** 0 hits, with a case-insensitive scan that ran inline and is not saved to a file.
- **Absolute home paths in PR-BODY.md.** None.
- **Closing keywords in PR-BODY.md.** None. Its first line is still the `[A468]` line, and its third line is still the "Refs #451" line.

## Public comments

- TAKEN: #451 comment 5925194601 (`TAKEN.md`; the read-back `TAKEN.readback.md` is equal but for the trailing newline).
- REVIEW READY: #451 comment 5925296626, posted at head `c39312b4` (`REVIEW-READY.md`; the read-back `REVIEW-READY.readback.md` is equal but for the trailing newline).

## For the manager

- Push `c39312b4` to PR #627, and replace the PR body with `PR-BODY.md`. Its new "Round 2" section is placed before "Verdicts". Its head line now names `c39312b4` as four commits, and it adds a fourth commit bullet. Nothing else in the round-1 body changed.
- R422-1 notes that every lens examined the page, so this commit leaves all five lenses to be covered again at `c39312b4`.
- Hosted and act checks start only after the push. Run the candidate-merge validation at the merge turn.
- The owner items are unchanged: re-attach the SoC board's USB function on the bench host; decide on the 1,016 unmatched clusters; close #451 by hand after merge (`Refs` only).

## Files in this directory

| Path | What |
|---|---|
| `HANDOFF.md` | This file |
| `PR-BODY.md` | The updated PR body |
| `TAKEN.md`, `TAKEN.readback.md` | The TAKEN comment and its read-back |
| `REVIEW-READY.md`, `REVIEW-READY.readback.md` | The REVIEW READY comment and its read-back |
| `MANIFEST.sha256` | SHA-256 of every other file here |
| `tools/offset_probe.py` | The one-bit-offset probe through the packet decoder |
| `tools/table_proof.py` | The per-table identity proof |
| `receipts/` | `offset-probe.json`, `table-proof.txt`, `table-lines.diff`, `pr-body-table-lines.diff`, `pr-body-table-render.json` |
| `gates/` | `gates.txt`, `gate-1.txt` to `gate-12.txt`, `status-after.txt`, `table-451_TDM8_TIMING_SOC_BOARD.txt` |

Scratch (`/tmp/a469-probe`) holds only the two page revisions and their table-line extracts. The probe's raw files were deleted after each decode. No toolchain, virtualenv, tree export or file over 200 KB is in this directory.

## Final state

- REVIEW READY: #451 comment 5925296626 at `c39312b4871c8cc3ca604eb7c57f4b0b45d914e0`. The session stops here.
- Lane worktree: clean, HEAD `c39312b4`, nothing pushed.
- Bench: untouched in this round. No lock was taken.
