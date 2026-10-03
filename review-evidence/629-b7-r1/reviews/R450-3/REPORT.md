[R450] POSITIVE - exact head 40714c1bd166c2a05f9607a861e8550c705d183a

# R450-3: internal re-review of PR #644 (issue #629, bench lane B7), round 3

- **Head:** `40714c1bd166c2a05f9607a861e8550c705d183a`, tree `ed3acf57d5c485168cfdf0e0e3aafae4a2382da1`. That is three commits on dev `bbf704ecc3ef2e9cdd4cfdb72ec085e7428d1352`: `4eee41a5`, `f4eb39d3` and `40714c1b`.
  - Each commit message is one line with no body and no trailers (`receipts/commits.txt`).
  - Across the PR, only `docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md` and `docs/findings/README.md` change (`receipts/diffstat_base_head.txt`).
- **Round-3 delta (`f4eb39d3..40714c1b`):** the findings page only, +58/-31. It is docs only, with no code, RTL, test, generated file or gitlink.
  - `receipts/delta-round3.masked.diff` holds the delta. The diff's two removed occurrences of the capture format are replaced by `<capture-format>`.
- **Evidence examined:** branch `629-b7-review-evidence`, fetched read-only:
  - `95448218` (first publication), and `d36de704` and `c6ad37e7` (the two masking commits);
  - the page's pin, `c6ad37e7`;
  - the tip `8516e544`, which adds only `author-r3/HANDOFF.md`, `author-r3/PR-BODY.md` and the publication manifest;
  - the chain `95448218 -> d36de704 -> c6ad37e7 -> 8516e544` is linear ancestry, so there was no force-push (`receipts/evidence_branch_history.txt`).
- **Context, in this order:**
  1. AGENTS.md and CONTRIBUTING.md section 6;
  2. docs/README.md;
  3. #629's body;
  4. the lane B7 assignment (5969106115), the round-2 assignment (5970119417), the round-3 assignment and privacy ruling (5970598673), and [A519] REVIEW READY (5970681269);
  5. the PR body and the review-start comment (5970698692);
  6. `docs/design/TIME_SYNC.md:385` and "Switching sources" in `docs/design/MEDIA_CLOCK_FOLLOWING.md` (:1035);
  7. the diff and history, then the evidence.
- **Prior findings:** R450-2 (5970571369) and R451-2 (5970594456) were read only after this round's own pass over the delta and the evidence.

## Independent checks at this head

Every check ran against the published artifacts, not against the page's prose. The scripts and receipts are listed in `MANIFEST.sha256`.

| Round-3 claim (page line) | Check | Result |
|---|---|---|
| The page, the findings index, the PR body and the published evidence at `c6ad37e7` state neither the capture's sample format nor its channel count (:596, :1175) | `scripts/mask_analysis.py` recovers the two private spans from the masking commits' own diffs. It writes them only to an unpublished scratch file and labels them `SPAN1` (the channel count) and `SPAN2` (the format). `scripts/privacy_scan.py` derives 10 patterns from them, including the bare tokens, number-with-channel forms, the file-name form, the `-c` argument, the format's digit-bearing parts, and a bit or byte depth near "capture". It prints pattern IDs, paths and line numbers only | **Holds.** 0 hits in the page and the index at `40714c1b`, in the live PR body, in `author-r3/`, and in all 481 files of `review-evidence/629-b7-r1` at `c6ad37e7`, reviews included. The positive controls fire: 4 hits on the round-2 page, 50 at `d36de704` and 64 at `95448218` (`receipts/privacy_scan.txt`). Over the whole `docs/` tree, the PR's only change is the removal of the format from lane B6's row (`receipts/privacy_scan_docs_tree.txt`). The remaining 17 generic-pattern hits are identical at base and head, in files outside the diff, and none is a value token |
| `d36de704` masked the channel count in the docstrings of four tools, and the format in the docstrings of `run_b7.py` and `run_b6.py` and in their code, as the capture command's format argument (:1220-1223) | `receipts/mask_analysis.txt`: the hunks of `d36de704^..d36de704`, each line classed as docstring or code | **Holds.** `SPAN1` is in the docstrings of `grade_b6.py:6`, `grade_b7.py:26`, `run_b6.py:13` and `run_b7.py:30`. `SPAN2` is in the docstrings of `run_b6.py:13` and `run_b7.py:30`, and in code at `run_b6.py:457` and `run_b7.py:516`. Read at `c6ad37e7`, both code lines are the capture command's format argument. The commit touches nothing else but the publication manifest |
| `c6ad37e7` masked the channel count in the capture file's name, in 19 files: `RAW-ARTIFACTS.json`, `runs/<case>/events.jsonl` and `runs/<case>-lock.txt` for seven runs, and the code of the same four tools (:1224-1227) | The same receipt, for `c6ad37e7^..c6ad37e7` | **Holds.** 19 packet files: `RAW-ARTIFACTS.json` (7 lines); 7 `events.jsonl` and 7 `-lock.txt` (a0, a1, a2, b0, bcrf, baaf, smoke-baaf); and, all in code, `grade_b6.py:75`, `grade_b7.py:99`, `run_b6.py:150` and `run_b7.py:191`. The only other file is the publication manifest. Only `SPAN1` is removed |
| The redaction pass had masked the channel count in the tools only in the channel-count assignment of `run_b7.py` and `run_b6.py`, and the format nowhere (:1215-1218) | Placeholders in the four tools at `95448218`; the four tool entries in `redaction.json` | **Holds.** `<capture-channels>` appears only at `run_b7.py:87` and `run_b6.py:68` (`NCH, CAP_L, CAP_R = ...`), and there is no `<capture-format>`. `grade_b7.py` and `grade_b6.py` were masked for the tone-channel identifiers, so "four tools name the external capture's channel layout" (:1203) also holds. `redaction.json` has 227 entries |
| Both commits were added on top with no force-push (:1229-1230) | `git merge-base --is-ancestor` along the chain; the tip `8516e544` | **Holds** |
| The pin is `c6ad37e7`; all 45 hash rows hold there; neither commit changed any other cited file (:1209, :1232-1238) | `scripts/check_page_hashes.py` at `c6ad37e7` and at `d36de704`. It checks: the 19 raw rows against each run's `events.jsonl` "raw-file" records and `RAW-ARTIFACTS.json`; the 7 full-grade rows against `RAW-ARTIFACTS.json` only; the 17 evidence rows against blob bytes, SHA-256 and `MANIFEST.json` `published_sha256`; and the two masked tools against `redaction.json` `original_sha256`. It also compares each cited evidence blob with `95448218` | **45 rows, 0 problems at both commits** (`receipts/page_hashes_c6ad37e7.txt`, `receipts/page_hashes_d36de704.txt`). Every non-masked evidence file is byte-identical to `95448218`. Five planted faults are each caught as 1 problem, and the unmodified copy gives 0 (`receipts/hash_check_fault_probes.txt`). The faults were a raw hash, a raw byte count, an evidence hash, a tool hash and a masked tool's as-run hash |
| R450-2 RES-2: each run's `events.jsonl` records every raw file of its run, among them the three per case and the tone loop (:1167-1168) | `runs/a0` and `runs/baaf` `events.jsonl` at `c6ad37e7` | **Holds.** Each has 7 `raw-file` records, among them `cap-lr.raw`, `cap-ts.bin`, `samples.txt` and `serve/tone.raw` (1,536,000 B, `566d3dfa...`) |
| B0: "the DUT answered the mark's next command, GET_COUNTERS on STREAM_OUTPUT 0 (seq 22913), and its other three, at once" (:946-947) | `runs/b0/ctl.jsonl`, seq 22905 to 22919 (`receipts/b0_mark1_ctl.txt`) | **Holds.** Seq 22912 is `counters-dut-36-0` (CLOCK_DOMAIN 0): TIMEOUT after 1.0007 s, not retried. Seq 22913 is `counters-dut-6-0`, payload descriptor type `0006` (STREAM_OUTPUT 0). The DUT's other three GET_COUNTERS (22914 STREAM_OUTPUT 1, 22916 STREAM_INPUT 0 and 22917 STREAM_INPUT 1) each answered SUCCESS in 0.1 to 0.2 ms |
| R451-2 S3: no B0 criterion used that mark, and the one CLOCK_DOMAIN criterion, in B-AAF, reads the first and the last mark (:950-953) | `tools/b7_tables.py:68-86` and `summary/verdicts.json` at `c6ad37e7`; the marks in `runs/b0` and `runs/baaf` `events.jsonl` (`receipts/marks_b0_baaf.txt`) | **Holds.** B0 has one check, "counted ratio beyond 2 ppm". B-AAF's CLOCK_DOMAIN check compares `window-mark-0` with `window-mark-2`. Each window has exactly marks 0, 1 and 2 |
| R451-2 S2: the 6 dups lie between the DUT's read before the binds and the window's first read, 1 s into the window, in an interval that holds both binds, the set, and the 20 s in which the servo locked (:985-988, :714, :1132) | 0x8D4 decoded per `tools/b7_decode.py:13,73-75` from every `runs/baaf/dut-*.txt` (`receipts/slip_lb_baaf.txt`); the binds, set and window from `events.jsonl` | **Holds.** The read before the binds is 380, at 15:37:47.44 CEST. The binds follow at 47.60 and 47.75, and the set at 47.75. The window starts at 15:38:07.85, 20.1 s after the set. `window-0` reads 386 at +1.1 s, and `window-1` 388 at +31 s. The count holds at 388 through `window-20` and after the window, and reads 390 after the lock loss |
| R451-2 RESIDUE-1: the 32,768-tick bound is cited to TIME_SYNC's clock-source settle row (:991-994) | `docs/design/TIME_SYNC.md:385` | **Holds.** The row reads "under CRF or AAF following: ... or engaged for 32768 ticks". The relative link resolves (`check_doc_paths.py`) |
| R451-2 S1: the order supersedes the 14:50 record's heading in `author/HANDOFF.md` and the `grade_b7.py` docstring, and `author-r2/HANDOFF.md` at the pin carries the corrected heading (:760-764) | `author/HANDOFF.md:66`, `tools/grade_b7.py:10` and `author-r2/HANDOFF.md:85` at `c6ad37e7`; a search of the packet for the superseded wording | **Holds as far as it goes.** The packet holds more as-run texts with the superseded claim than the two it names (R450-3 RES-1 below) |
| R451-2 RESIDUE-2: the round-3 handoff says "11 live AECP descriptors byte-equal, plus the CLOCK_SOURCE 3 absence check" | `author-r3/HANDOFF.md:76` at `8516e544`; `identity/identity-verdict.txt` | **Holds.** There are 12 `aecp-` checks: 11 byte-equal, and 1 absence check (CLOCK_SOURCE 3, `NO_SUCH_DESCRIPTOR`). No "12 live" remains in `author-r3/` |
| R450-2 RES-3: the PR body's "Round 2" table is renumbered | The live PR body | **Holds.** Items 1 to 9, with no duplicate. The live PR body equals `author-r3/PR-BODY.md` |
| No case verdict changed | `scripts/verdict_figure_delta.py`: every table cell with a verdict word, and the multiset of figures, at `f4eb39d3` against `40714c1b` | **Holds.** 30 of 30 verdict cells are identical (`receipts/verdict_figure_delta_r3.txt`). The only figures removed are the format's digits (in two rows) and the old "STREAM_INPUT 0,". Every figure added (22913, 19 files, seven runs, 1 s, 20 s, 6) is verified above |
| Docs gates at this head | `docs_check.py`, `check_doc_style.py`, `gen_toc.py --check`, `gen_toc.py --verify-anchors`, `check_em_dash.py --base bbf704ec` and `check_doc_paths.py`, in a disposable environment installed from `tools/markdown/requirements.txt` with `--require-hashes` (cmarkgfm 2025.10.22, html5lib 1.1); `git diff --check` over the worktree, `bbf704ec..HEAD` and `f4eb39d3..HEAD` | **All 9 rc 0** (`receipts/gates/`). `docs_check`: 0 findings, scrub self-test 23/23. `check_em_dash`: 0 findings over 577 added lines, arms 339/339. 307 anchors reproduced, and 895 doc paths resolve |
| Hosted contexts at this head | Check runs of `40714c1b`, read once (`receipts/hosted_checkruns_40714c1b.tsv`) | Executed with SUCCESS: `rtl-fast`, `docs-check-no-git`, `full-ci-gate`, `bdd-conformance`, `wire-accountability`, `elaborate` and `changes`. `docs-check` was still in progress when read. SKIPPED, not executed: `verilator-suites`, `yosys-portability`, `verilator-lint`, `yosys-elaboration`, both shard templates and "Physical gPTP (nightly and manual)". The PR is not a draft |

## Findings

No BLOCKER, MAJOR or MINOR is open at this head.

## RESIDUE

Each item is wording only. It changes no measurement, figure, verdict, test, code, generated artifact, conformance or clause claim, and touches no privacy rule. Each goes to the residue checklist with its exact fix.

- **R450-3 RES-1 (lens Docs): `docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md:760-762`, "The order below supersedes two as-run texts that say otherwise".**
  - The published packet at `c6ad37e7` holds more texts with the superseded claim than the two named:
    - step 9 of `author/HANDOFF.md:35`: "14:50, before any graded case";
    - the docstring at `author/tools/b7_tables.py:8`: "fixed before any case ran";
    - `author/PR-BODY.md:11`;
    - `author/REVIEW-READY.md:12` and its `.readback.md` copy.
  - The page's order is correct, and it is what a reader is told to follow. The undercount only leaves those texts unnamed.
  - **Exact fix.** Replace this sentence:

    > The order below supersedes two as-run texts that say otherwise: that record's heading in the published `author/HANDOFF.md`, "before any case ran", and the docstring of `grade_b7.py`, "each fixed before any graded case".

    with this one:

    > The order below supersedes every as-run text that says otherwise: in the published `author/HANDOFF.md`, that record's heading, "before any case ran", and its step 9; the docstrings of `grade_b7.py`, "each fixed before any graded case", and `b7_tables.py`; and the round-1 `author/PR-BODY.md` and `author/REVIEW-READY.md`.
- **R450-3 RES-2 (lens Docs): the PR body's "Evidence" section, "Neither changed a file the page's evidence table cites, and the raw rows are recorded unchanged."**
  - Both `d36de704` and `c6ad37e7` changed the published `tools/run_b7.py` and `tools/grade_b7.py`, which the evidence table cites. Their rows are the as-run `original_sha256`, so every row still holds (0 problems above).
  - The page's own sentence at :1235-1236 says "any other file", and it is correct.
  - **Exact fix:** "Apart from `run_b7.py` and `grade_b7.py`, whose rows are their as-run hashes in `redaction.json`, neither changed a file the page's evidence table cites, and the raw rows are recorded unchanged."

## SUGGESTIONS

- **S1 (privacy, outside this diff, for the manager): lane B6's own published evidence still carries the capture's sample format.**
  - The page's lane B6 section is already on dev, and this PR does not change it. That section pins `b6-review-evidence` at `422dcf91`.
  - At that pin, and at the branch's tip `b23b7dd9`, `review-evidence/b6-r1/author/tools/run_b6.py` carries the format token twice: at :13 (docstring) and :457 (the capture command's format argument). That is the same text `d36de704` masked in the B7 packet's copy.
  - The scan's one other hit there, `HANDOFF.md:72`, is a generic-pattern match on a sample-value range, not a value token. The channel count gives 0 hits there (`receipts/privacy_scan_b6_evidence.txt`).
  - The round-3 ruling's evidence scope is `c6ad37e7`, so this does not bear on this PR's lenses. Under the same ruling, it needs the same top-only masking on `b6-review-evidence`, or a public Issue.
- **S2 (Docs).** At :1232-1233, "except the two masked tools" follows a paragraph that names four masked tools. Writing "except `run_b7.py` and `grade_b7.py`, the two masked tools this table cites" would remove the ambiguity.
- **R450-2 S1 to S4.** These stay untaken, and they are optional: they were outside the round-3 assignment.
  - R450-2 S4 is the instrument class in `author-r2/HANDOFF.md:47`, unchanged at the tip (same blob `761fb60e`).
  - The round-3 ruling names only the channel count and the format, so it does not cover S4, and S4 remains the manager's privacy call.

## Prior public findings at this head

| Item | Status at `40714c1b` | Evidence |
|---|---|---|
| R450-2 F1 (a) = R451-2 F1 (MINOR): private capture values public | **Resolved** | The format is gone from :1175 (B7) and from :596 (B6, authorised by the round-3 assignment). The channel count is masked in the evidence at `c6ad37e7`. A value-blind scan finds 0 in the page, the index, the PR body, `author-r3/` and all of `review-evidence/629-b7-r1` at `c6ad37e7`, and its controls fire. The handling of `95448218` and `d36de704` is stated (:1229-1230). Lane B6's separate evidence branch is outside this scope (S1 above) |
| R450-2 F1 (b) = R451-2 F2 (MINOR): the masking misdescribed | **Resolved** | :1215-1227 and the PR body match `receipts/mask_analysis.txt` file by file, docstring against code |
| R451-2 F3 = R450-2 RES-1: B0's next command | **Resolved**, the exact sentence plus the seq | :946-947, against `runs/b0/ctl.jsonl` |
| R450-2 RES-2 | **Resolved**, exactly | :1167-1168 |
| R450-2 RES-3 | **Resolved** | The PR body's "Round 2" items run 1 to 9 |
| R451-2 RESIDUE-1 | **Resolved** | :993-994; the link resolves to `TIME_SYNC.md:385` |
| R451-2 RESIDUE-2 | **Resolved** in the round-3 handoff | `author-r3/HANDOFF.md:76`. The round-1 comment and the round-1 and round-2 handoffs are historical and were not edited, as the assignments require |
| R451-2 S1 | Taken | :760-764, with an undercount (R450-3 RES-1) |
| R451-2 S2, S3 | Taken; both accurate | `receipts/slip_lb_baaf.txt`, `receipts/marks_b0_baaf.txt`, `b7_tables.py:68-86` |
| R450-2 S1 to S4 | Not taken (optional) | Outside the round-3 assignment |

## Ledger (reviewer-owned)

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | 30 verdict cells identical between `f4eb39d3` and `40714c1b`, the #629 acceptance table :1129-1137 among them (`receipts/verdict_figure_delta_r3.txt`). "Refs #629" in the PR body. Round-3 ruling items 1 to 5 against the page, the PR body and `author-r3/`. Descriptor type 0x0006 (STREAM_OUTPUT) at seq 22913 in `runs/b0/ctl.jsonl`. The settle bound against `TIME_SYNC.md:385` | R450-3 | 40714c1bd166c2a05f9607a861e8550c705d183a |
| RTL | CLEAN | No HDL, generated file or gitlink in `bbf704ec..40714c1b` (`receipts/diffstat_base_head.txt`; gitlinks in `receipts/clone_integrity.txt`). The round-3 register statements: 0x8D4 `SLIP_LB`, decoded per `b7_decode.py:13,73-75` from the 8 cited `runs/baaf/dut-*.txt` reads (`receipts/slip_lb_baaf.txt`). The recentre bound against `TIME_SYNC.md:385` | R450-3 | 40714c1bd166c2a05f9607a861e8550c705d183a |
| Robustness | CLEAN | The B0 timeout path: seq 22905 to 22919, no retry, and the status and rtt of the commands that followed (`receipts/b0_mark1_ctl.txt`). The S2 interval and the slip timeline across the binds, set, window and lock loss (`receipts/slip_lb_baaf.txt`, `receipts/marks_b0_baaf.txt`). S3 against `b7_tables.py:68-86` and `summary/verdicts.json`. History retention of the masked publication: linear ancestry (`receipts/evidence_branch_history.txt`) | R450-3 | 40714c1bd166c2a05f9607a861e8550c705d183a |
| Tests | CLEAN | 45 hash rows at `c6ad37e7` and `d36de704`, 0 problems, and 5 planted faults each caught (`receipts/page_hashes_*.txt`, `receipts/hash_check_fault_probes.txt`). The privacy scan, with three positive controls firing (`receipts/privacy_scan.txt`). The verdict criteria in `b7_tables.py` against `verdicts.json`. 9 docs gates rc 0 at the head (`receipts/gates/`). Hosted runs at the exact head (`receipts/hosted_checkruns_40714c1b.tsv`) | R450-3 | 40714c1bd166c2a05f9607a861e8550c705d183a |
| Docs | CLEAN (RES-1 and RES-2 go to the residue checklist) | The whole round-3 delta (`receipts/delta-round3.masked.diff`). The B7 hash and packet section :1164-1260, against `receipts/mask_analysis.txt`. The live PR body (`receipts/pr644_body_snapshot.json`). `author-r3/HANDOFF.md` and `PR-BODY.md` at `8516e544`. `docs/findings/README.md`, unchanged since round 1. Privacy scans of the page, the index, the PR body, the packet and the `docs/` tree | R450-3 | 40714c1bd166c2a05f9607a861e8550c705d183a |

All five lenses are covered clean at this exact head.

## Real limits

- **Raw files.** The captures, timing samples and full grades are not published. The raw and grade rows were checked against the packet's records (`events.jsonl`, `RAW-ARTIFACTS.json`), not against bytes. No audio was re-decoded, and no tool was re-run on raw data.
- **Masked tools.** `run_b7.py` and `grade_b7.py` cannot be run as published. Their as-run hashes were checked against `redaction.json`. Their as-run byte counts (32,321 and 27,057) have no public record.
- **Privacy scan.** It is pattern-based, so a value written in a form none of the 10 patterns covers would escape it. The three positive controls show that the patterns fire on the forms that were actually published.
- **Hosted.** `docs-check` was in progress when read. The Verilator and Yosys contexts are SKIPPED by the docs-only scope, so they are not execution evidence. The manager owns hosted and local-replica acceptance.
- **Hardware and calibration.** Physical calibration is NOT RUN, and no hardware was touched. Field skips are not hardware proof. No simulation, builder, Verilator or Yosys bank was run in this round.
- **Order of reading.** Before the prior findings were read, this round triaged four false-positive scan hits by printing 100-character, digit-masked windows from four JSON receipts in the R450-1 and R450-2 archives on the evidence branch. Those windows held path and comment text. No finding was taken from them.

## Pending manager duties

- Carry R450-3 RES-1 and RES-2 to the residue checklist.
- S1: decide the format token on lane B6's evidence branch, by top-only masking or a public Issue. Also decide R450-2 S4.
- Hosted and local-replica acceptance at the exact head, including the final `docs-check` result.
- At the merge turn, the final current-dev candidate validation (source base `bbf704ecc3ef2e9cdd4cfdb72ec085e7428d1352`; live dev `bbf704ecc3ef2e9cdd4cfdb72ec085e7428d1352` at review start). This is distinct from this source review.
- The second (external) positive review at this head, and maintainer merge authorisation.

## Receipts

All paths are relative to this packet and listed in `MANIFEST.sha256`.

- **Scripts:**
  - `scripts/mask_analysis.py` and `scripts/privacy_scan.py`. Both are value-blind; the private spans live only in an unpublished scratch file.
  - `scripts/check_page_hashes.py`
  - `scripts/verdict_figure_delta.py`
- **Receipts:**
  - Masking and privacy: `receipts/mask_analysis.txt`, `privacy_scan.txt`, `privacy_scan_docs_tree.txt` and `privacy_scan_b6_evidence.txt`.
  - Hash rows: `page_hashes_c6ad37e7.txt`, `page_hashes_d36de704.txt` and `hash_check_fault_probes.txt`.
  - Run records: `b0_mark1_ctl.txt`, `marks_b0_baaf.txt` and `slip_lb_baaf.txt`.
  - Verdicts and diff: `verdict_figure_delta_r3.txt`, `verdict_figure_delta_r1_to_r3.txt`, `delta-round3.masked.diff`, `diffstat_base_head.txt`, `diffstat_round3.txt` and `commits.txt`.
  - Evidence branch: `evidence_branch_history.txt`.
  - Hosted: `hosted_checkruns_40714c1b.tsv`, `hosted_status_40714c1b.txt` and `pr644_head.txt`.
  - PR body: `pr644_body_snapshot.json`.
  - Gates: `gates/`.
  - Clone state: `clone_integrity.txt`.
- **Clone state:** the clone is at exact-head bytes (`receipts/clone_integrity.txt`).
  - The write-tree, `ed3acf57...`, equals the HEAD tree.
  - The index equals HEAD, and the worktree equals the index.
  - 994 of 994 tracked blobs and modes match.
  - `git status --porcelain --ignored` is empty. This round's gate runs had created `scripts/__pycache__/`, which was removed.
  - Gitlinks: external `efeb541a` (uninitialised), gptp-processor `5dce647a`, protocol-processor `631eeb34` and verilog-axis `48ff7a7e`.
  - The only repository-side change is the read-only fetch of the two evidence branches.

R450-3 FINISHED
