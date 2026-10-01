[A469] REVIEW READY

Round 2 for PR #627 (Refs #451, bench lane B4, the timing item), under the round-2 assignment 5925185587. It answers R422-1 (5925175550) and R423-1 (5925182051). Docs only, with no bench access.

Commit: `c39312b4871c8cc3ca604eb7c57f4b0b45d914e0` on `b4-bench-1001`, one commit on `35a60c8d` and four on dev `e4b771f9`. One-line subject, no body, no trailers. Local only: not pushed, and the PR is not edited. The updated PR body, with a new "Round 2" section, is in the lane packet `b4-a469`.

Changed: `docs/findings/451_TDM8_TIMING_SOC_BOARD.md` only. The index row is unchanged. Line numbers are at `c39312b4`.
- **R422-1 F1** (`:116-117`): the full-length recording is 967.7 MB, for the 630 s the capture was set to (630 s x 1.536 MB/s).
- **R422-1 F2 and R423-1 S1** (`:36`, `:244-250`, `:315-320`):
  - The verdict cell reads "47,997.947 Hz on the SoC board's uncalibrated clock".
  - The verdict row and the fs bullet state that fs is -42.8 ppm from 48 kHz on an uncalibrated clock. -10.64 ppm of that is the plan. The remaining -32.1 ppm is the DUT oscillator's error relative to the SoC board's clock, unsplit and unquantified.
  - The Frequencies paragraph gives that as the signed relative error: about the DUT oscillator's error minus the SoC board clock's, since a fast SoC board clock lowers the measured fs.
  - "48 kHz within the SoC board's clock accuracy" and "48 kHz at the board's accuracy" are gone from the page.
- **R423-1 F1** (`:303-314`): the "every class of word check" sentence is replaced by the checks each direction trips, as the Framing paragraph details.
  - One bit early trips the tag checks and the ordinal steps. Torn frames, the low byte and zero words stay clean.
  - One bit late trips the tag, low-byte and torn-frame checks. Only zero words stay clean.
- **R422-1 S1** (`:61`): "every identity value equals that page's".
- **R422-1 S2** (`:350`): the talker ended 58.7 s before the unbind (talker end record 1790828918.128 against the unbind event 1790828976.783).
- **R423-1 S2** (`:154-157`, `:303-305`): the one bit of data delay is the McASP driver's mapping of the `dsp_a` format in the hardware description (the page's existing term), not a register readback. The lane's rules allowed no direct read of a McASP register.
- **R423-1 S3** (`:16-18`, `:97-99`): the root shell was confirmed with `id` (uid 0), and no credential was typed or stored.

No measured figure or other verdict changes.

Validation:
- **Measurement tables byte-identical.** 11 of the page's 12 tables are identical to `35a60c8d`, with the same SHA-256 each. The verdict table differs only in the FSYNC row the assignment names. A plain `diff` of every table line in the two revisions (89 lines each) shows that one row (`6c6`) and nothing else. Rendered and source cell counts are byte-identical to round 1's receipt. Every round-1 table in the PR body is unchanged; the body adds one probe table.
- **One-bit-offset wording.** A synthesized TDM8 line runs through the packet's own decoder (SHA-256 `cfb7121b…`), with ordinals crossing bit 15 and one repeat and one skip.
  - Early: torn 0, 0 low-byte words, 0 zero words, channels 4 to 7 invalid in all 4,096 frames, and steps doubled.
  - Late: torn 4,096, 16,384 low-byte words, 0 zero words, and channel 0 tag 0 in every frame.
  - This matches both round-1 probes.
- **Gates at `c39312b4`.** All 12 invocations rc 0, unpiped, from the physical `/data` lane path, with the Markdown gates in the pinned Markdown environment:
  - `scripts/docs_check.py` (0 findings) and `scripts/check_doc_style.py`;
  - `scripts/gen_toc.py --check`, and `--verify-anchors` (283 links);
  - `scripts/check_em_dash.py --base e4b771f9` (0 findings over 393 added lines);
  - `scripts/check_doc_paths.py` (861 paths) and `scripts/ci_scope.py --selftest`;
  - `scripts/check_baremetal_only.py --check` (0 findings) and `scripts/check_feature_status.py --self-test` (46/46);
  - `git diff --check`, also against `e4b771f9` and `35a60c8d`.
- **Token scan of the lane packet.** 0 private names. The only identifier hit is the DUT's public entity ID.

Acceptance criteria (the round-2 assignment items 1 to 4): all met, as listed under Changed, with the measurement tables byte-identical and no bench access.

Open risks/questions: none new. Every round-1 lens examined the page, so all five lenses need covering again at `c39312b4`. Push, hosted checks and the owner items (USB re-attach, the 1,016 unmatched clusters, closing #451 by hand) stay with the manager and the owner. No issue state change or review approval is claimed.
