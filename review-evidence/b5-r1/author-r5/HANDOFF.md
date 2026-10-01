# B5 round 5 handoff ([A478])

Status: REVIEW READY at `e5ad118783c2ff96e13f1d794f10bf2b63741282`, local only. It is not pushed, and the PR is not edited. The manager pushes the head and applies `PR-BODY.md`.

- PR: #628 (bench lane B5, #117 acceptance box 4, the audio continuity row).
- Assignment: #117 comment 5929901339 ([A10] round 5, with rulings 1 to 4).
- Reviews answered: R424-4 (PR #628 comment 5929893902, one MINOR and two suggestions) and R425-4 (PR #628 comment 5929883759, four MINOR and two suggestions).
- Branch `b5-bench-1001`: parent `e216dfe4f0cab7b0c7352d7973acb4d33c157f70`, base dev `e4b771f93ee870fb2a93f8360b8677bb0b3e2a3b`. One commit with a one-line subject, no body and no trailers.
- Archive pin: `9006c78e354d5a2f244fd606c55790a825304bd3`, the tip of the remote branch `b5-review-evidence` when checked.
- TAKEN: #117 comment 5929915474 (`taken-url.txt`). REVIEW READY: #117 comment 5930172204 (`review-ready-url.txt`).
- No bench access, no lock, no NAS write, no push, no PR edit, no comment edited or deleted.

## Change (file:line, at `e5ad1187`)

`docs/findings/117_AUDIO_CONTINUITY.md` only (+23 -12). The index row `docs/findings/README.md` is byte-identical.

| Item | Where | What |
|---|---|---|
| 1, R425-4 F1 | `:493`, `:495`, `:498` | The Bytes cells of the three every-channel rows read `withheld`: `a-long` 10 s, `diag1` 25 s, and the as-found 3 s capture. Their SHA-256 cells are unchanged. These are the only table cells changed. |
| 1 | `:471-472` | "each identified by size and SHA-256" becomes "each identified by SHA-256, and all but the every-channel captures by size too". The next line is reflowed. |
| 1 and 3 | `:524-526` | "the masked `RAW-ARTIFACTS.json` keeps every raw file's size and SHA-256" was false at `9006c78e`. It now reads: keeps every raw file's SHA-256, and every size but the every-channel captures', which it withholds, as the table above does. |
| 2, R424-4 F1 = R425-4 F3 | `:521-523` | "Of these, `b5_attrib.py` and `b5_round3.py` read only the `a-long` `summary.json`, and both still reproduce their receipts byte for byte at the pinned commit." `events.jsonl` is no longer named there. |
| 3 | `:461-463` | The pin and the tree link move from `8e6be432` to `9006c78e354d5a2f244fd606c55790a825304bd3`. |
| 5, R424-4 S1 | `:14-22` | The header lists round 4: [A476], its assignment 5928569912 and the stream-count ruling 5929406675. It also lists round 5: [A478] and its assignment 5929901339. |

`PR-BODY.md` (item 4, R425-4 F4) is rewritten in `.github/PULL_REQUEST_TEMPLATE.md`'s sections.

- Kept: the `[A472]` first line, and the "Refs #117" line under Linked Issue / roles. There is no closing keyword.
- Sections: Status (`:18`), Linked Issue / roles with the roles (`:28`), Description with the result table (`:41`), the Round 2 to Round 4 sections (`:62`, `:84`, `:108`), a new Round 5 section (`:140`), Authoritative references (`:167`), How to get into the same state (`:178`), How to validate (`:194`), Known limitations / out of scope (`:221`) and Definition of Done (`:233`).
- Item 2 in the body: Round 4 item 1 (`:113`) now says that, of the lane packet's label-masked files, both tools read only `summary.json` (corrected in round 5).
- Two historical statements are annotated: the round 4 pin (`:112`, re-pinned in round 5) and the round 4 raw-index sentence (`:122`, which held at `8e6be432`).
- Round 4's "the manager's call" on the format channel counts (`:137`) now records ruling 1.
- The Result paragraph says "an external audio capture records the peer's output". It drops two adjectives the old body carried, so it states less than the page and adds nothing.

## Reproduction from the new pin alone

`receipts/repro_at_9006c78e.txt`, written by `tools/b5_repro.py`. It runs `git archive` of `author/`, `author-r2/` and `author-r3/` at `9006c78e` into a fresh scratch directory outside this one, and nothing else is used. Result: PASS.

- 207 extracted files, 207 manifest entries in those directories: 0 mismatched against `published_sha256`, and 0 missing. 18 are `path_redacted`.
- Step 1: `gunzip -kf a-long-reads.u16.gz` takes the masked copy (`8897abce…`, equal to its `published_sha256`) to `2183d57f0646cf94405b95aea5547b83f5ff0b9190ac0bd1bdcc87760c919961`, 131,540 bytes. That equals the page's hash and the manifest's `original_sha256`.
- Step 2: `b5_attrib.py figures author author-r2/receipts` exits rc 0 with empty stderr. Its output, `18ebbfc1…`, equals `attribution.txt` byte for byte.
- Step 3: `b5_round3.py figures author author-r2/receipts` exits rc 0 with empty stderr. Its output, `9fa0f027…`, equals `round3_figures.txt` byte for byte.
- Open trace: each command is run again under a Python audit hook on `open`, with output equal to the plain run.
  - `b5_attrib.py` opens `author-r2/receipts/a-long-reads.json`, the restored `a-long-reads.u16`, `author/summary/a-long/summary.json` and `author/summary/a-long/continuity-events.csv`.
  - `b5_round3.py` opens the same files plus `author/restore/peer-descs-2.jsonl`.
  - The masked input read is `summary.json` only. `events.jsonl` is not opened. The masked read-record copy is replaced by step 1 before either tool runs.
- Pin to pin: the masked set in the three directories is unchanged from `8e6be432` (18 files). Only the published bytes of 7 already-masked `author/` files changed: `RAW-ARTIFACTS.json`, and the `console.txt` and `events.jsonl` of `a-long`, `diag1` and `cap-test1`. Their `original_sha256` values are unchanged.

## Hash and raw-index checks at `9006c78e`

- `receipts/hash_check.txt`: the round 4 tool `b5_hash_check.py`, unchanged (`3c71273c…`), run from the round 4 packet. Result: PASS, 20 of 20 cited SHA-256 values, 0 problems.
  - 3 are `original_sha256` of `path_redacted` files: `run_a.py`, `grade_a.py` and the read record.
  - 7 are unmasked tool files whose published blob matches.
  - 10 are quoted in published files: 8 raw files, the pattern period and the controller's start snapshot.
- `receipts/raw_index_check.txt`: `tools/b5_raw_index_check.py`. Result: PASS.
  - Every numeric artifact row's size equals its `RAW-ARTIFACTS.json` entry, and the three `withheld` rows meet withheld entries.
  - Every withheld entry is an every-channel capture, by its `cap-all-` path or by the page row's label.
  - Pin to pin: all 19 entries keep their SHA-256 and path in order. 15 sizes are equal, 4 are withheld, and none changed otherwise. No size is printed.

## Capture-size derivation check

`receipts/size_derive_check.txt`, written by `tools/b5_size_derive_check.py`. The capture's channel count is derived in memory from the page at `e216dfe4` and is never printed or written. Every byte size is tested against each stated duration in the same file, exactly and as a whole multiple of 3 bytes times that count.

- Power check: on the page at `e216dfe4` it flags exactly the old `:483`, `:485` and `:488`. The planted control hits both tests.
- At `e5ad1187`: 0 unexplained hits on the page, the index row and `PR-BODY.md`. The one whole-multiple match, `:496`, is the `cap-test1` graded pair, a two-channel file whose size is a whole multiple of its own 6 bytes per frame.

## Table proof (the measurement tables are byte-identical)

`receipts/table_identity.txt`, written by `tools/b5_table_proof5.py`. It prints no old table text, because older revisions hold the withheld sizes and the withdrawn peer counts. Every table is compared by SHA-256 and by a literal `diff` of its lines, and the rc and output line count are printed.

- `e216dfe4` to `e5ad1187`: 15 tables and 119 table lines at both heads. 14 of 15 tables are byte-identical, with `diff` rc 0: the summary verdict table, every measurement table (2 to 12), the Restore table (13) and the tool table (15).
- Table 14, Artifact hashes, differs in three cells only. Rows 5, 7 and 10, column 2 (Bytes), go from a numeric cell to `withheld`. With the Bytes column cut out, its literal `diff` is empty (rc 0).
- `bf9e5d82` (round 1) to `e5ad1187`: tables 2 to 12 and 15 are byte-identical. Table 1 differs in the three Evidence cells that rounds 2 to 4 changed, table 13 in the Restore stream-state cell that round 4 changed, and table 14 in the three Bytes cells only.
- `docs/findings/README.md` is byte-identical to `e216dfe4`.

## Public-text scans (token scan)

Three scans, run over this directory as finally written (before the scan receipts and `MANIFEST.sha256`; `review-ready-url.txt` and `REVIEW-READY.readback.md` were added after posting, and the readback equals the scanned `REVIEW-READY.md` but for one trailing newline), the lines added by `e216dfe4..e5ad1187` (round 5) and `e4b771f9..e5ad1187` (the whole PR, so the whole page), and both ranges' commit messages. Every scan prints labels and places only, and each runs a planted positive control in memory before it scans.

- **Label scan** (`receipts/token_scan.txt`, the round 4 tool `b5_scan.py`, unchanged). It holds 17 private literals: every value the archive mask replaced, recovered from the local lane packet, and the local host names. It adds 11 labelled patterns: vendor, link type, clock-topology word, agent tool or model name, account name, capture channel number, SoC product, USB bus position, MAC, home directory and interface name. The word lists were passed on stdin and are written nowhere.
  - Result: 0 hits in the round 5 range and in this directory.
  - The whole-PR range has 1 hit, `:424`. That is round 1 text (`bf9e5d82`, by blame) in the frozen Restore table's DUT synchronization row: the DUT's own gPTP state, which round 4 recorded at `:415`.
- **Stream-count scan** (`receipts/count_scan.txt`, the round 4 tool `b5_count_scan.py`, unchanged). The peer's counts are derived in memory from the local lane packet. None of the hits is a peer count.
  - `:85`: the DUT's own stream state count, kept as in round 4.
  - `:252` and `PR-BODY.md:68`: the round 2 and 3 phrase about the capture's reads around a stall, as round 4 classified it.
- **Withheld-value scan** (`receipts/withheld_scan.txt`, `tools/b5_withheld_scan.py`). It covers the 4 withheld sizes, as digits and with commas, and the capture's channel count before a channel noun, as digits and as a word. All are derived in memory.
  - Result: 0 hits in both ranges and in this directory.
  - Power check: on `e4b771f9..e216dfe4` it hits the old `:483`, `:485` and `:488`.
- **Hand check of the diff.** The added lines name no host, peer, switch, instrument, interface or account. They state no wiring, channel map, capture layout or clock topology, and no peer stream, stream port, stream state or cluster count. The same holds for the commit subject and every file here.

## Gates (all rc 0 at `e5ad1187`, from `$LANES/b5-bench-1001`, none piped)

`receipts/gates/gates.txt` lists each command and its rc, with its output in `gate-<n>.txt`. The worktree was clean before and after.

1. `docs_check.py`: 0 findings across 182 md files and 953 scrubbed text files.
2. `check_doc_style.py`: OK.
3. `gen_toc.py --check`: OK.
4. `check_em_dash.py --base e4b771f9`: 0 findings over 553 added lines in 2 pages.
5. `check_doc_paths.py`: OK, 861 cited paths resolve.
6. `scripts/ci_scope.py --selftest`: PASS.
7. `scripts/check_baremetal_only.py --check`: OK.
8. `scripts/check_feature_status.py --self-test`: 46 of 46.
9. `git diff --check`.
10. `git diff --check e4b771f9 HEAD`.
11. `git diff --check e216dfe4 HEAD`.
12. `gen_toc.py --verify-anchors`: 283 links.

Gates 1 to 5 and 12 ran with the pinned Markdown environment's Python. Gates 6 to 8 ran with `python3`.

## For the manager

- **Archive residuals at `9006c78e`.** Two archive receipts still carry the `diag1` every-channel size, the one row the mask commit left in them: `author-r4/receipts/raw_index_check.txt:9` and `reviews/R424-4/receipts/hash_check.txt:7`. No other archive file at `9006c78e` holds a withheld size (literal scan, in memory). The page's reproduction does not read either file.
- **Not taken.** R425-4 S2 is not among the round 5 items: naming `author-r2/` and `author-r3/` `gates/gates.txt` among the masked files. The page cites no hash of either. R424-4 S2 is the manager's, and rulings 2 to 4 answer it.
- **The body as last applied** still says both tools read `events.jsonl`, until `PR-BODY.md` is applied.
- **Hosted checks and the act replica** have not run at `e5ad1187`, because the head is not pushed.

## Limits

- No bench access and no new measurement. Every figure comes from published inputs or is unchanged.
- The scans' labelled patterns are finite lists, so a clean result covers those classes only. The private literals cover the archive mask and the local host names.
- The derivation check tests byte sizes against stated durations. It cannot see a size the text does not state.

## Files

| File | What |
|---|---|
| `TAKEN.md`, `TAKEN.readback.md`, `taken-url.txt` | the posted TAKEN |
| `REVIEW-READY.md`, `REVIEW-READY.readback.md`, `review-ready-url.txt` | the posted REVIEW READY |
| `PR-BODY.md` | the PR body to apply |
| `tools/b5_repro.py` | steps 1 to 3 from one archive commit alone, with the manifest check and the open trace |
| `tools/b5_size_derive_check.py` | the capture-size derivation check |
| `tools/b5_raw_index_check.py` | the artifact table against `RAW-ARTIFACTS.json` |
| `tools/b5_table_proof5.py` | the table proof, with no old table text printed |
| `tools/b5_withheld_scan.py` | the withheld-value scan |
| `receipts/repro_at_9006c78e.txt` | the reproduction and the open trace |
| `receipts/hash_check.txt` | the 20 cited hashes at `9006c78e` |
| `receipts/raw_index_check.txt` | the raw-index check, and the pin-to-pin raw-index comparison |
| `receipts/size_derive_check.txt` | the derivation check, with its power check |
| `receipts/table_identity.txt` | the table proof against `e216dfe4` and `bf9e5d82` |
| `receipts/token_scan.txt`, `receipts/count_scan.txt`, `receipts/withheld_scan.txt` | the three scans |
| `receipts/gates/` | the gate outputs at `e5ad1187` |
| `MANIFEST.sha256` | the SHA-256 of every other file here |

Every file here is under 200 KB. No toolchain, virtual environment or tree export is kept here. The archive extraction and the table lines were written to a scratch directory outside it, and that directory is removed at the end.
