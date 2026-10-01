# B4 round 3 handoff: [A470], PR #627 talker-to-unbind interval

Status: DONE, REVIEW READY posted on #451 (comment 5925580411). Local commit only: not pushed, PR not edited.

- Lane: `$LANES/b4-bench-1001`, branch `b4-bench-1001`.
- Start head: `c39312b4871c8cc3ca604eb7c57f4b0b45d914e0` (round 2).
- New head: `ae98b30b04e95f38df784ba490da208c57534303`, tree `bae15aec6847292bd50025203035e3b902bdac79`. It is one commit on `c39312b4` and five on dev `e4b771f9`, with a one-line subject, no body and no trailers.
- Assignment: issue #451 comment 5925502698.
- Round-2 reviews: PR #627 comments 5925427751 (R422-2, NEGATIVE on one MINOR, F1) and 5925499736 (R423-2, POSITIVE).
- No bench access, no lock taken, no NAS write, no push, no PR edit, no existing comment edited or deleted.

## The change

One file: `docs/findings/451_TDM8_TIMING_SOC_BOARD.md`. `git diff --raw c39312b4 HEAD` lists only it (mode 100644, blob `7c3f54673` to `dde50cd9c`). `docs/findings/README.md`, the index row, is unchanged (`git diff --quiet c39312b4 HEAD -- docs/findings/README.md` rc 0).

| Item | Finding | Page lines | Change |
|---|---|---|---|
| 1 | R422-2 F1 | `:350-352` at `ae98b30b` (was `:350-351`) | "The talker also ended 58.7 s before the unbind, because ..." becomes "The talker also ended 60.0 s before the unbind, on the controller host's clock, because the stalled capture held the SoC board's console until its deadline." The paragraph's last two lines are re-wrapped into three. No other line changes |

Whole-page diff (receipt `receipts/page.diff`):

```text
350,351c350,352
<   58.7 s before the unbind, because the stalled capture held the SoC
<   board's console until its deadline. Both counters clear only on reset.
---
>   60.0 s before the unbind, on the controller host's clock, because the
>   stalled capture held the SoC board's console until its deadline. Both
>   counters clear only on reset.
```

The page states this interval nowhere else (a search for `unbind`, `ended` and `58.` finds only this sentence, the capture-end lines, and the unrelated `:362` note).

## Evidence for 60.0 s

- The R422-2 packet's `scripts/talker_unbind_interval.py`, run read-only on the round-1 packet's `runs/timing-long`, prints `interval_controller_clock_s` 60.038 and `interval_mixed_clocks_s` 58.655. The controller's record of each command leads the orchestrator's event for it by 1.359 to 1.384 s. All of this equals R422-2's `receipts/talker_unbind_interval.json`.
- Which host stamps which record, from the round-1 packet's tools:
  - `run_timing.py:54-55`: `event()` stamps `events.jsonl` with `time.time()` on the orchestrating host.
  - `aaf_talker.py:40` and `avdecc_ro.py:54`: the talker log and the `ctl-*.jsonl` records are stamped with `time.time()` on the controller host, where both run over ssh (`run_timing.py:64-65`).
- Single-clock interval: the talker's `end` record (`controller-logs.txt:141`, t 1790828918.128055) against the unbind command's start record (`ctl-unbind.jsonl` line 1, t 1790828978.166264). That is 60.038 s, given as 60.0 s.
- The round-2 figure, 58.7 s, was the talker's end record against the orchestrator's `unbind` event (`events.jsonl:13`, t 1790828976.782734): two hosts' clocks.

## The PR body

`PR-BODY.md` in this directory, against round 2's (`c2247ff4...`, which equals the live PR body but for a trailing newline):

| Line now | Change |
|---|---|
| 5 | The head line names `ae98b30b04e95f38df784ba490da208c57534303` as five commits on dev `e4b771f9` |
| 11 | A fifth commit bullet, for `ae98b30b` (round 3) |
| 13 | The one-line "Round 3" note, before "Round 2": the executor, the assignment, R422-2 F1, the page's `:350-352` and the new interval, the matching line, the FSYNC row (R422-2 S1), and no measured figure or page table change |
| 29 | The round-2 R422-1 S2 line agrees with the page: "The talker ended before the unbind, not "about 55 s" before it. Round 3 states the interval on one clock: 60.0 s, on the controller host's clock (R422-2 F1)." |
| 71 | R422-2 S1: the Verdicts table's FSYNC row mirrors the page's `:36`. The verdict cell is byte-equal to the page's ("47,997.947 Hz on the SoC board's uncalibrated clock"). The evidence cell is byte-equal to the page's, less the closing " See [Frequencies](#frequencies)" anchor link and the period before it. The dropped "crystal tolerance (tens of ppm) not included" is covered by "unquantified", as on the page |

Kept: the `[A468]` first line and the "Refs #451" line (line 3). No closing keyword (`close`, `fix` or `resolve` with `#N`): none. No absolute home path. No em or en dash. No attribution footer.

Not taken: R423-2 S1 (the optional NVM-sequence clarification at `:59-61`), because the assignment names only R422-2 S1 and says nothing else changes.

## Byte-identical table proof

Page, `c39312b4` against `ae98b30b`:

- `tools/table_proof.py` (round 2's tool, copied unchanged: SHA-256 `a47b898c746eb65e8d0f5d76424511be90e087fa00678631acfa251d48d38169` in both places) finds 12 tables in each revision. All 12 are IDENTICAL, with the same SHA-256 each; `changed tables: 0` (receipt `receipts/table-proof.txt`). The per-table hashes equal round 2's new-side hashes in its `table-proof.txt`. Tables 11 and 12 (the artifact-hash tables) move down one line, from 373 and 380 to 374 and 381, because the paragraph above them gained a line.
- A plain `diff` of every `|` line in the two revisions (89 lines each) is empty, rc 0 (receipt `receipts/table-lines.diff`, 0 bytes). `cmp` of the two extracts is equal. The round-1 extract at `35a60c8d` is also 89 lines.
- The rendered and source cell counts (`gates/table-451_TDM8_TIMING_SOC_BOARD.txt`, round 1's `table_render_check.py` in the pinned Markdown environment, rc 0) are byte-identical to round 2's receipt (`cmp` equal). Round 1's tool was run read-only from its packet (SHA-256 `57c5d6a804f3718b25dd0fd6d50104db0c2d3f4fdb8d3967448aa88fcea9ce5a`).

PR body, round 2 against round 3:

- A plain `diff` of every `|` line (receipt `receipts/pr-body-table-lines.diff`) is one changed line, `11c11`, the FSYNC verdict row (R422-2 S1), and nothing else. The per-run measurement tables and every other row are unchanged.
- The rendered cell counts are constant in all 5 tables (`receipts/pr-body-table-render.json`, ok true), and the receipt is byte-identical to round 2's (`cmp` equal).

## Gates at `ae98b30b`

All 13 invocations rc 0, unpiped, from the physical `/data` lane path (`gates/gates.txt`, one output file per gate). The Markdown gates used `$VALIDATION_TOOLS/md-venv-40cdefe08ebd/bin/python`. Bytecode writing was off (`PYTHONDONTWRITEBYTECODE=1`).

| Gate | Result |
|---|---|
| `scripts/docs_check.py` | 0 findings across 182 md files |
| `scripts/check_doc_style.py` | OK |
| `scripts/gen_toc.py --check` | OK |
| `scripts/check_em_dash.py --base e4b771f9` | 0 findings over 394 added lines in 2 pages |
| `scripts/check_doc_paths.py` | 861 paths resolve |
| `scripts/ci_scope.py --selftest` | PASS |
| `scripts/check_baremetal_only.py --check` | 0 findings across 951 files |
| `scripts/check_feature_status.py --self-test` | 46/46, 0 findings |
| `git diff --check` | clean |
| `git diff --check e4b771f9 HEAD` | clean |
| `git diff --check c39312b4 HEAD` | clean |
| `scripts/gen_toc.py --verify-anchors` | 283 links |
| `git diff --check 35a60c8d HEAD` | clean |

`git status --porcelain --ignored` after the gates (`gates/status-after.txt`) shows one ignored entry, `scripts/__pycache__/`. It predates this session: created at 04:40:45Z and last written at 04:42:03Z, before this round's first command. This round's gates (05:46Z) did not write to it, and it was left as found. Tracked and untracked status is empty.

## Token scan

Run over every file in this directory just before REVIEW READY, and again after the final manifest:

- **Private names.** The patterns were loaded at run time from round 1's private redaction map, held outside every packet. None was copied into any file. Generic patterns covered MACs, IPv4 addresses, IPv6 link-local addresses, EUI-64 and clock-identity shapes, home paths and interface names. Result: see "Scan result" below.
- **Agent tool and model names.** A case-insensitive scan that ran inline and is not saved to a file. Result: see below.

Scan result, over all 27 files here before REVIEW READY plus the commit message and the page's added lines. The rescan after the final manifest covered all 29 files (adding `REVIEW-READY.readback.md` and `MANIFEST.sha256`) with the same result:

- **Private names: 0 hits.** 49 distinct literal patterns (54 entries, as round 2 counted them) and 1 regex from the map. The generic patterns found no MAC, IPv4 or IPv6 link-local address, colon-form EUI-64, home path or interface name. The only EUI-64-shaped hit is the DUT's public entity ID `020000fffe000001` in `PR-BODY.md`, which the redaction rule retains. The rescan also finds it in this file, in this sentence.
- **Agent tool, model and account names: 0 hits.** The case-insensitive scan's 7 raw matches are all the gPTP protocol name (`gPTP` in `PR-BODY.md:103`; `gptp-processor` and `gptp_plane` in `gates/gate-6.txt`), not a model name.
- **Absolute home paths in `PR-BODY.md`: none.** **Closing keywords: none.** Its first line is still the `[A468]` line, and its third line is still the "Refs #451" line.

## Public comments

- TAKEN: #451 comment 5925511375 (`TAKEN.md`; the read-back `TAKEN.readback.md` is equal but for the trailing newline).
- REVIEW READY: #451 comment 5925580411, posted at head `ae98b30b` (`REVIEW-READY.md`; the read-back `REVIEW-READY.readback.md` is equal but for the trailing newline).

## For the manager

- Push `ae98b30b` to PR #627, and replace the PR body with `PR-BODY.md`.
- R422-2 notes that every lens examined the page, so this commit leaves all five lenses to be covered again at `ae98b30b`. The diff `c39312b4..ae98b30b` is one paragraph of one page (3 insertions, 2 deletions), which R422-2 says a confirmation would cover.
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
| `tools/table_proof.py` | The per-table identity proof (round 2's, unchanged) |
| `receipts/` | `table-proof.txt`, `table-lines.diff`, `page.diff`, `pr-body-table-lines.diff`, `pr-body-table-render.json` |
| `gates/` | `gates.txt`, `gate-1.txt` to `gate-13.txt`, `status-after.txt`, `table-451_TDM8_TIMING_SOC_BOARD.txt` |

Scratch (`/tmp/a470-tables`) holds only the three page revisions, their table-line extracts and the two PR-body table extracts; `/tmp/a470-live-body.md` is the live PR body as read. No toolchain, virtualenv, tree export or file over 200 KB is in this directory.

## Final state

- REVIEW READY: #451 comment 5925580411 at `ae98b30b04e95f38df784ba490da208c57534303`. The session stops here.
- Lane worktree: clean, HEAD `ae98b30b`, nothing pushed. The PR #627 head is still `c39312b4`.
- Bench: untouched in this round. No lock was taken.
