[A470] REVIEW READY

Round 3 for PR #627 (Refs #451, bench lane B4, the timing item), under the round-3 assignment 5925502698. It answers R422-2 F1 (5925427751) and takes R422-2 S1. Docs only, with no bench access.

Commit: `ae98b30b04e95f38df784ba490da208c57534303` on `b4-bench-1001`, tree `bae15aec6847292bd50025203035e3b902bdac79`. It is one commit on `c39312b4` and five on dev `e4b771f9`, with a one-line subject, no body and no trailers. Local only: not pushed, and the PR is not edited. The updated PR body is in the lane packet `b4-a470`.

Changed:
- **R422-2 F1**, `docs/findings/451_TDM8_TIMING_SOC_BOARD.md:350-352` (was `:350-351`). The sentence now reads "The talker also ended 60.0 s before the unbind, on the controller host's clock, because the stalled capture held the SoC board's console until its deadline."
  - It replaces "58.7 s", which subtracted the talker's end record (controller host's clock) from the unbind event (the orchestrating host's clock).
  - Both stamps are now from the controller host: the talker's `end` record at t 1790828918.128055 and the unbind command's start record at t 1790828978.166264, 60.038 s apart.
  - Only that paragraph's last two lines are re-wrapped, into three. `docs/findings/README.md` is unchanged.
- **The PR body** (packet copy; not committed text):
  - The head line names `ae98b30b` as five commits, and a fifth commit bullet is added.
  - A one-line "Round 3" note is added before "Round 2". The `[A468]` first line and the "Refs #451" line are kept, with no closing keyword.
  - The round-2 R422-1 S2 line now agrees with the page: the talker ended before the unbind, and round 3 states the interval on one clock, 60.0 s on the controller host's clock.
  - **R422-2 S1**: the Verdicts table's FSYNC row mirrors the page's verdict cell (`:36`). It reads "47,997.947 Hz on the SoC board's uncalibrated clock": -42.8 ppm against 48 kHz, -10.64 ppm of it the plan, and the remaining -32.1 ppm the DUT oscillator's error relative to the SoC board's clock, unsplit and unquantified. Its evidence cell equals the page's, less the closing "See [Frequencies]" anchor link.

No measured figure or verdict changes.

Validation:
- **Interval.** The R422-2 packet's `talker_unbind_interval.py`, run on the round-1 packet's `runs/timing-long`, gives `interval_controller_clock_s` 60.038 and `interval_mixed_clocks_s` 58.655, equal to the R422-2 receipt. The round-1 tools show which host stamps each record: `run_timing.py` stamps `events.jsonl` on the orchestrating host; `aaf_talker.py` and `avdecc_ro.py` stamp the talker log and `ctl-*.jsonl` on the controller host.
- **Measurement tables byte-identical.**
  - All 12 page tables at `ae98b30b` are IDENTICAL to `c39312b4`, with the same SHA-256 each (round 2's proof tool, unchanged). The table hashes equal round 2's new-side hashes.
  - A plain `diff` of every table line in the two revisions (89 lines each) is empty, and `cmp` is equal.
  - The whole-page `diff` is the one paragraph, `350,351c350,352`, and nothing else.
  - The rendered and source cell counts are byte-identical to round 2's receipt (`cmp` equal).
  - PR body: the only table line that differs is the FSYNC verdict row (S1). The body's 5 tables have the same rendered cell counts as round 2's receipt (`cmp` equal).
- **Gates at `ae98b30b`.** All 13 invocations rc 0, unpiped, from the physical `/data` lane path. The Markdown gates ran in the pinned Markdown environment.
  - `scripts/docs_check.py` (0 findings across 182 md files) and `scripts/check_doc_style.py`;
  - `scripts/gen_toc.py --check`, and `--verify-anchors` (283 links);
  - `scripts/check_em_dash.py --base e4b771f9` (0 findings over 394 added lines in 2 pages);
  - `scripts/check_doc_paths.py` (861 paths) and `scripts/ci_scope.py --selftest` (PASS);
  - `scripts/check_baremetal_only.py --check` (0 findings across 951 files) and `scripts/check_feature_status.py --self-test` (46/46, 0 findings);
  - `git diff --check`, also against `e4b771f9`, `35a60c8d` and `c39312b4`.
- **Token scan of the lane packet.** 0 private names, and 0 agent tool or model names. The only identifier hit is the DUT's public entity ID.

Acceptance criteria (5925502698): met.
- The interval is one the packet supports on a single clock: 60.0 s, on the controller host's clock.
- The PR body's matching line agrees, and R422-2 S1 is taken.
- Nothing else changes, and every measurement table is byte-identical.
- The docs gates return rc 0.

Open risks/questions: none new.
- R422-2 notes that every lens examined the page, so all five lenses need covering again at `ae98b30b`. The diff `c39312b4..ae98b30b` is this one paragraph of one page (3 insertions, 2 deletions), which R422-2 says a confirmation would cover.
- R423-2 S1 (the optional NVM-sequence clarification at `:59-61`) is not taken, because the assignment names only R422-2 S1.
- Push, hosted checks, candidate-merge validation and the owner items (USB re-attach, the 1,016 unmatched clusters, closing #451 by hand) stay with the manager and the owner. No issue state change or review approval is claimed.
