[R425] NEGATIVE - exact head e29d12b1d5ee858eaf4684aaa8dc6647f6309857

Round R425-2, external independent review of PR #628 (Refs #117, acceptance box 4, the audio continuity row; bench lane B5, evidence only). Exact head `e29d12b1d5ee858eaf4684aaa8dc6647f6309857`, tree `7d56900c21c8ddefb7f95e9830b598201caf4231`, base dev `e4b771f93ee870fb2a93f8360b8677bb0b3e2a3b`. Round 2 is one docs-only commit on the round-1 head `bf9e5d82a401d167a8ffc786677a19dc7aac0cf2`: `docs/findings/117_AUDIO_CONTINUITY.md` (+111 -36) and its index row in `docs/findings/README.md`.

Reconstructed from: AGENTS.md, CONTRIBUTING.md (sections 2, 6, 6.1), docs/README.md; #117 body; the B5 assignment (#117 comment 5925737609) and the round-2 assignment 5926598386 (items 1 to 4); TAKEN 5926614985 and REVIEW READY 5927093074; `avdecc/aem_descriptors.py:103` and `:579-591`, `docs/ENDSTATION_BUILDER.md:522-533` (IEEE 1722.1 7.2.16 AUDIO_CLUSTER signal fields), `docs/design/TIME_SYNC.md:169,478`; the diff `e4b771f9..e29d12b1` and `bf9e5d82..e29d12b1`; the public evidence branch `b5-review-evidence` at `1116f856f881190471e5320de869b9095a1a0537`, which contains `ef3a709151f9bdbd4718c0783d0b8991ede7fd36` (round-1 packet `review-evidence/b5-r1/author`) and adds the round-2 author packet `review-evidence/b5-r1/author-r2`. My own pass over the diff and every figure was completed before I read the round-1 reviews (`receipts/verdict_written_at.txt`); the other round-2 review was not read.

## Verdict summary

The round-2 restatement does what the assignment asked, and the page's attribution figures are right: every figure re-derives exactly, by the author's tool and by an independent reviewer implementation, from the derived read record whose SHA-256 the page states (`2183d57f...`). R424-1 F1, R424-1 F2 and R425-1 F1 are resolved; R425-1 F2 is resolved in the page's content. 14 of 15 tables are byte-identical, the PR says Refs #117 only, the public text is clean, and all docs gates are rc 0.

Two MINOR findings keep the verdict NEGATIVE:

- **R425-2-F1.** The derived read record as published (`author-r2/receipts/a-long-reads.u16`) is not the record the page hashes. The archive step masked 3 bytes of it (`MANIFEST.json`: `path_redacted: true`), so the published copy hashes to `8897abce...`. The author's `b5_attrib.py figures` refuses it unmodified. The figures re-derive only after the reviewer undoes the mask. This breaks R425-1 F2's own condition, re-derivation from published inputs, although nothing in the page is wrong.
- **R425-2-F2.** This keeps R425-1 F3 open in a narrower form. The Direction B reason says the clusters' source "is not visible over AEM", and the summary row says no known signal reaches the peer's talker channels without an instrument or wiring change. But AEM names a cluster's source in the AUDIO_CLUSTER descriptor's own `signal_type`/`signal_index`/`signal_output`, and that descriptor was never read, as the page's next paragraph states. The wording the page uses is the wording my round-1 F3 proposed, so this corrects my own earlier required outcome, not the author's compliance with it.

Neither finding changes any PASS/FAIL/NOT RUN cell; "FAIL as measured" stands.

## Findings

### R425-2-F1 MINOR - Conformance, Tests, Docs - the published derived read record is not the hashed one

- Artifact: `docs/findings/117_AUDIO_CONTINUITY.md:191-194`, `:401-405`; public `b5-review-evidence@1116f856:review-evidence/b5-r1/author-r2/receipts/a-long-reads.u16` (blob `0fbea6efe617c8e67b05b926d280a8a61e4d7a63`), `a-long-reads.json`, `author-r2/MANIFEST.sha256:8`, `review-evidence/b5-r1/MANIFEST.json` (entry `author-r2/receipts/a-long-reads.u16`).
- Authority/evidence: the page states that the round 2 packet holds "the window's derived read record: 131,540 bytes, SHA-256 `2183d57f...`", and that every figure comes from it. #117 box 5 requires exact hashes, and R425-1 F2 required each figure to re-derive from published inputs. The published 131,540 bytes hash to `8897abce393078140112a1a86c5c732953d4a43f9cbf5847fff885ca0d244abc`. `MANIFEST.json` records `original_sha256 2183d57f...`, `published_sha256 8897abce...`, `path_redacted: true`.
  - The record holds one run of three 0x23 bytes, at byte offset 114032, covering reads 57016 and 57017 (`receipts/mask_probe.txt`).
  - The published differences sum to 660,150,189 us, which is 896 us short of the `elapsed_us_record` of 660,151,085 us.
  - Run unmodified on the published inputs, `b5_attrib.py figures` refuses with an `AssertionError` at its record-hash check (`receipts/author_figures_unmodified.txt`). That fail-closed behaviour is correct.
  - With only the hash check bypassed, two outputs differ from the published `attribution.txt` (`receipts/author_figures_bypass_vs_published_attribution.diff`):
    - the boundary reading becomes 117,609.1 frames, not 117,652.1;
    - the clear-position control gains a spurious tenth group of -43.3 frames at reads 57005..57021, so the page's "9 places" (`:219`) no longer re-derives.
  - In a disposable area, exactly one 3-byte replacement both restores the record's own elapsed time and hashes to `2183d57f...`. On that reconstruction, the unmodified author tool reproduces the published `attribution.txt` byte for byte (`receipts/author_figures_on_reconstruction.txt`). So the mask is the only difference. The reconstructed bytes and the search are not published here.
  - The same archive step also changed `author-r2/receipts/gates/gates.txt`, a text path substitution that is recorded and harmless.
- Impact: a cold reviewer who follows the page gets a record whose hash disagrees with the page, and a tool that refuses it. The page's figures are correct, but at this head the published evidence cannot show it without undoing an archival edit. The masked bytes are capture timing data, so masking them protects nothing.
- Required outcome: the public archive carries `a-long-reads.u16` byte-identical to SHA-256 `2183d57f0646cf94405b95aea5547b83f5ff0b9190ac0bd1bdcc87760c919961`, with binary receipts excluded from the text redaction. Failing that, the archive and the page state the mask and its effect. Either way, `b5_attrib.py figures` must reproduce the published `attribution.txt` unmodified from published inputs. No change to the page's figures is required.
- Owner: the archive step, which the manager owns. The PR head's text is not at fault.
- Verification: `sha256sum` of the republished record, then `tools/r425_run_author_figures.py <author-r2> <author>` without `--bypass-record-hash` completes, and its output equals `receipts/attribution.txt`.

### R425-2-F2 MINOR - Conformance, Docs - the Direction B reason still asserts an AEM fact the walk did not read (R425-1 F3, narrowed)

- Artifact: `docs/findings/117_AUDIO_CONTINUITY.md:24` (summary Evidence cell, unchanged from round 1), `:337-343`, set against `:345-351` on the same page.
- Authority/evidence: IEEE 1722.1 7.2.16. In the repository's words (`docs/ENDSTATION_BUILDER.md:531-533`), "AUDIO_CLUSTER (7.2.16): the `signal_type`/`signal_index` fields tie clusters into that signal chain". The repository's own cluster builder writes those fields (`avdecc/aem_descriptors.py:579-591`).
  - The page reasons: "Its AUDIO_UNIT declares no external or internal port and no routing element, so what feeds those clusters is not visible over AEM. A known signal ... would therefore need an instrument or wiring change." Line 24 states as fact: "No known signal reaches the peer's talker channels without an instrument or wiring change."
  - The next paragraph (`:345-351`) and `author-r2/receipts/records.txt` show that no AUDIO_CLUSTER descriptor was read. All 20 walk reads used type 0x0010 and answered NO_SUCH_DESCRIPTOR.
  - The AUDIO_UNIT counts I re-checked (`records.txt` section 2, layout verified against 7.2.3) exclude external ports, internal ports and routing elements as sources. They do not exclude a source named directly in the clusters' own signal fields, for example one of the stream input port's clusters. If a cluster named such a source, the peer's talker would carry a known signal without any wiring change.
  - So the AEM statement that would answer the question exists and was not obtained. "Not visible over AEM" is an inference, and the page itself says the descriptor was never read.
  - This is the wording my R425-1 F3 required outcome proposed, and the author followed it. The defect is in that proposal.
- Impact: NOT RUN stays correct under the lane rule, which says to run only if a known signal can be put on the talker channels without a wiring change. But the page records as observed that no such signal exists, and the one descriptor that could contradict this was never read. A later lane could skip Direction B on that statement.
- Required outcome: the reason and the line 24 Evidence cell state what was observed: the port's four clusters, the map drawing only from them, and no external port, internal port or routing element declared. They also state that the clusters' own source fields were not read, because of the walk defect, so it was not established whether a known signal can reach the peer's talker channels without an instrument or wiring change. The NOT RUN verdict cell is unchanged. Whether this may touch the summary table is the manager's call, since round 2 froze it to figure corrections. Alternatively, a later read-only AUDIO_CLUSTER read with type 0x0014 settles it.
- Verification: re-read `:24` and `:337-351` at the corrected head against `records.txt` and 7.2.16.

### Suggestions (non-blocking; no lens affected)

- **S1 - Docs - `:242-248`, `:388-390`.** Of the 121 off-stall clusters, 22 step by 1 ms. Clear positions show 7 such groups in about 3,239 independent floor windows, a base rate of about 0.0022 per window. At that rate about 0.26 of 121 clusters would step by chance, against the 22 observed (`receipts/rederive_reconstructed_record.txt`). So the 1 ms steps concentrate at these skips: they coincide with a capture-delivery timing event, and they are not background. The page's "not attributed" conclusion stands. Stating the coincidence would keep a reader from treating the 22 like the 7 clear-position steps.
- **S2 - Docs - `:22`, README row.** "Skips of 60 frames or more are stall-aligned capture-path loss" covers all 239. The body says 236 of 239 are stall-aligned, and the other three sit in intervals stretched by roughly their own duration. The shorthand is the assignment's wording and is not misleading; "236 of 239 stall-aligned" would be exact.
- **S3 - Tests - `:217-218`.** The step estimator is linear in an additive plant, so the planted 6, 12 and 24-frame recoveries are by construction the same distribution as the unplanted step at those positions (`attribution.txt`, three identical rows). The control confirms where the guard windows sit, not detection power. The page claims nothing more, and the Limits bullet at `:388` states the model assumption.

## Item-by-item judgment (round-2 focus)

**R424-1 F1 and R425-1 F1, the attributions: RESOLVED.**

- Skips of 60 frames or more are stall-aligned capture-path loss (`:222-231`).
  - With a stall defined as a read interval over 15 ms (`grade_a.py:84`, `STALL_MS = 15.0`), the record holds 220 stalls, 18.80 to 28.09 ms each. 236 of the 239 skips fall one or two reads after one (lags 130 at one read, 106 at two).
  - Each stall is followed by exactly one skip of 240 frames or more. The three unaligned skips of 72, 78 and 108 frames sit in intervals of 11.76 to 12.11 ms.
- The 2-to-59 class splits as the page says (`:233-248`), with the same stall definition.
  - 284 skips (5,386 frames) fall in the 222 clusters that hold a skip of 60 frames or more. Their deficit steps sum to 116,137.6 frames against 115,314 skipped.
  - 237 skips (1,790 frames) fall in 121 clusters with no stall. The nearest stall is at least 17 reads away (median 67), so "away from any stall" holds.
  - Of those 121 clusters, 0 step by the frames skipped, 95 stay within 3 frames, 22 step by 1 ms and 4 match neither.
  - My independent floor implementation gives the same split at window widths 7 and 11. At widths 16 and 21, 0 clusters still match their skips, the 22 one-millisecond steps are stable, and 1 or 7 clusters move from "none" to "other". The "not attributed" conclusion holds at every width.
- The page does not overstate the class: it attributes none of it. On understatement, see S1.
- The 1.266 s drops are attributed "by inference", with the capture's input named as the alternative, at `:250-266`, in Limits `:379-383`, in summary rows `:22` and `:25`, and in the index row.
- The summary and index rows match the body.

**R425-1 F2, reproducible figures: RESOLVED in content; the published-input condition is broken by the archive (R425-2-F1).** All figures re-derive independently (`receipts/rederive_reconstructed_record.txt`):

| Figure | Re-derived value |
|---|---|
| 236 of 239 | 236 of 239 |
| Stall recurrence | 220 stalls, median spacing 3.0011 s, range 2.990 to 3.020 s ("3.00 s (2.99 to 3.02 s)") |
| Stall excess | 109,069.3 frames against 109,928 |
| Count drift from `window_time` | 660.151102 s × 48 kHz less 31,569,600 = 117,652.9 frames, "117,653" |
| Boundary reads | 117,652.1 frames |
| Slip rate | median 60,768 frames between events, 1.2660 s, 16.46 ppm |
| Six-frame multiples | 507 and 354 |
| Shares of frames | 0.370% and 0.347% |
| Whole-run zero frames | 226,230 + 261,671 + 6 + 2,919,589 = 3,407,496 (from `a-long-wholerun.json`) |

- The dropped 0.8 and 17.3 ppm, 16.4 ppm, 115,614 and "2.99 s" appear nowhere in the tree at the head (`git grep`). The PR body mentions them only as dropped or corrected.

**R425-1 F3, Direction B: PARTLY RESOLVED.**

- The walk-defect record is correct. The walk read clusters as 0x0010 and maps as 0x0014, where `avdecc/aem_descriptors.py:103` gives 0x0014 and 0x0017, and it read external ports one too high.
- Every cluster read was type 0x0010 and answered NO_SUCH_DESCRIPTOR. No map read was sent, because both ports declare 0 static maps.
- The published `b5_records.py` reproduces `records.txt` byte for byte on the round-1 packet and this clone.
- The reason's "not visible over AEM" stays open in narrowed form as R425-2-F2.

**R424-1 F2, controller tool revision: RESOLVED.**

- The page (`:432-439`) states that the revision cannot be established, and gives the start snapshot `24208ef2...` (8,642 B).
- The start survey at 06:14:57.463 carries no audio-unit walk. The survey at 06:16:07.727, 70.3 s later, carries one.
- The end snapshot `47b7387a...` (9,842 B) is a re-staged copy: both files carry a 06:44 mtime in `restore/controller-end.txt`.
- `run_a.py` hashes no staged agent (`:185-189`).
- Neither what was recorded nor what was not is overstated.

**Tables: CONFIRMED.**

- 15 tables and 119 table lines at both commits; 14 are byte-identical (`receipts/table_identity_r425.txt`).
- The summary verdict table changes only cell index 2, the Evidence cell, of the continuity row and the "#117 audio continuity row" row. Both Verdict cells are unchanged.
- The tool table is unchanged; the new tools' hashes (`f1d9b2ba...`, `c68ecf7b...`) are given in prose and equal the published files.

**PR and public text: CONFIRMED.**

- The PR body says "Refs #117" with no closing keyword. Both commit messages are one line with no trailers or keywords.
- A structural scan (`tools/r425_public_scan.py`) and a private list of vendor, product, host and tool names (kept out of this packet) were run over the page, the 447 added lines, the commit messages and the PR body. The structural scan matches only stream-format codes and the DUT's own entity and stream IDs. The private list has no hit; its only hits in the index file are three pre-existing rows naming the DUT board.
- No capture channel number or channel map is given. "The SoC board's McASP0" and the INTERNAL clock-source selections are unchanged round-1 text that the assignment sanctions.

**Docs gates: rc 0 at the head** (`receipts/gates/gates.txt`), run in a private hash-pinned Markdown environment:

- `docs_check.py`;
- `check_doc_style.py`;
- `gen_toc.py --check` and `--verify-anchors`;
- `check_em_dash.py --base e4b771f9` (0 findings over 447 added lines) and `--selftest`;
- `check_doc_paths.py`;
- `ci_scope.py --selftest`;
- `check_baremetal_only.py --check`;
- `check_feature_status.py --self-test`;
- `git diff --check e4b771f9 e29d12b1`.

## Prior public review findings at this head

| Finding | Status at e29d12b1 |
|---|---|
| R424-1 F1 (MINOR) | Resolved |
| R424-1 F2 (MINOR) | Resolved |
| R425-1 F1 (MINOR) | Resolved |
| R425-1 F2 (MINOR) | Resolved in content; publication condition carried as R425-2-F1 |
| R425-1 F3 (MINOR) | Walk-defect part resolved; reason part retained, narrowed, as R425-2-F2 |

R424-1's suggestions S1 to S3 are not findings and are not judged here.

## Reviewer-owned lens ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (R425-2-F1, R425-2-F2) | `117_AUDIO_CONTINUITY.md:18-27,190-266,335-355,373-446` against #117 boxes 4-5, assignments 5925737609 and 5926598386 items 1-4, IEEE 1722.1 7.2.3/7.2.16 via `avdecc/aem_descriptors.py:103,579-591` and `docs/ENDSTATION_BUILDER.md:522-533`; `author-r2/receipts/records.txt`, `restore/controller-*.txt`, `restore/peer-descs-2.jsonl` | R425-2 | e29d12b1d5ee858eaf4684aaa8dc6647f6309857 |
| RTL | CLEAN | no RTL in the diff (`git diff --stat e4b771f9..e29d12b1`: two Markdown files); the round-2 lines add no DUT-behaviour claim; the unchanged beat claim checked against `docs/design/TIME_SYNC.md:169,478` (-10.64 ppm, 1.958 s) and the re-derived repeat spacing 93,989-93,992 | R425-2 | e29d12b1d5ee858eaf4684aaa8dc6647f6309857 |
| Robustness | CLEAN | analysis edge and failure paths: the fail-closed record-hash check in `b5_attrib.py` (refuses the masked record), window-edge clusters (0), floor-parameter sweep at 4 widths (`receipts/rederive_reconstructed_record.txt`), behaviour on the masked versus original record (`receipts/author_figures_bypass_vs_published_attribution.diff`), double-period slip and beat spacings, and the zero-frame placement sums in `a-long-wholerun.json` | R425-2 | e29d12b1d5ee858eaf4684aaa8dc6647f6309857 |
| Tests | UNCLEAN (R425-2-F1) | `author-r2/tools/b5_attrib.py` (unmodified: refuses the published record; on the reconstructed record: output equals `attribution.txt`), `b5_records.py` (rerun equals `records.txt`), reviewer `tools/r425_rederive.py` (independent), `tools/r425_tables.py`; receipts under `receipts/` | R425-2 | e29d12b1d5ee858eaf4684aaa8dc6647f6309857 |
| Docs | UNCLEAN (R425-2-F1, R425-2-F2) | `docs/findings/117_AUDIO_CONTINUITY.md` (all 447 lines), `docs/findings/README.md:20`, PR #628 body, commit messages; docs gates rc 0 (`receipts/gates/`); public-text scans (`receipts/public_scan.txt`) | R425-2 | e29d12b1d5ee858eaf4684aaa8dc6647f6309857 |

## Real limits

- The raw capture, the raw read-time file and the raw pair are not public. The derived record, the window event list and `a-long-wholerun.json` are taken as derived receipts. The whole-run integrity counts sum consistently: 35,948,690 valid + 3,407,496 zero = 39,356,186. They are not recounted from samples.
- The floor test rests on its stated model: a frame lost after sampling delays every later read. The stall clusters support that model in aggregate (116,138 against 115,314); no single cluster tests it.
- All rates are on the bench host's uncalibrated clock. Physical calibration NOT RUN. No hardware, bench, instrument or console was touched, and field skips are not hardware proof.
- The figures were verified against a reconstruction of the published record (R425-2-F1), not against a byte-exact public copy.
- No RTL changed, so the scoped simulator was not used. No parent, PP, gPTP, Yosys or builder bank was run.
- The Markdown lock was installed into a private virtual environment under this packet's scratch area; no shared install was made.
- Hosted contexts at the head were read only (`receipts/hosted_checks.txt`). Executed and successful: `rtl-fast`, `bdd-conformance`, `changes`, `docs-check-no-git`, `elaborate`, `full-ci-gate`, `wire-accountability`. Skipped by the docs-only scope: `verilator-lint`, `verilator-suites`, `yosys-elaboration`, `yosys-portability`, the shard matrices and Physical gPTP. `docs-check` was in progress, and the combined status was pending when read.

## Pending manager duties

- R425-2-F1: republish `author-r2/receipts/a-long-reads.u16` byte-identical to `2183d57f...`, keeping binary receipts out of the text redaction, or record the mask in the archive and on the page.
- R425-2-F2: route it to an executor, and decide whether the line 24 Evidence cell may change.
- Hosted and act acceptance at the exact head, including the in-progress `docs-check`.
- The current-dev candidate build at the merge turn (source base and live dev both `e4b771f93ee870fb2a93f8360b8677bb0b3e2a3b` at review time).
- Publishing this report and the files listed in `MANIFEST.sha256`.

## Clone integrity

The review clone stays at `e29d12b1d5ee858eaf4684aaa8dc6647f6309857`, tree `7d56900c21c8ddefb7f95e9830b598201caf4231`.

- Worktree and index are clean, with nothing untracked or ignored.
- The 981 index entries (mode, blob, path) equal the HEAD tree.
- The gitlinks are unchanged: external `efeb541ae5fe`, gptp-processor `5dce647ab5a0`, protocol-processor `b2db3a970ced`, third_party/verilog-axis `48ff7a7e2ef7` (`receipts/clone_integrity.txt`).
- No probe edited the clone.

R425-2 FINISHED
