[R451] POSITIVE - exact head 40714c1bd166c2a05f9607a861e8550c705d183a

R451-3, external independent review of issue #629 / PR #644 (bench lane B7), round 3. Head `40714c1bd166c2a05f9607a861e8550c705d183a`, tree `ed3acf57d5c485168cfdf0e0e3aafae4a2382da1`, base dev `bbf704ecc3ef2e9cdd4cfdb72ec085e7428d1352`. This is a delta review of round 3 (`f4eb39d3..40714c1b`, docs only) against R450-2, R451-2 and the round-3 assignment (issuecomment-5970598673). All five lenses were applied. Open findings: none at BLOCKER, MAJOR or MINOR. Two RESIDUE items and three SUGGESTIONs are recorded. No case verdict changed.

## Scope reconstructed

- **Contract:** AGENTS.md, CONTRIBUTING.md section 6 (privacy and wording), the #629 issue body, and the B7 lane assignment (5969106115).
- **Round-3 assignment (5970598673):** the manager rules that the external capture's channel count and sample format are private, with masking at `d36de704` and `c6ad37e7`, top-only.
- **Changed files:** the round-3 delta touches only `docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md` (+58/-31). The PR as a whole touches that page and `docs/findings/README.md`, which is unchanged since round 1. There is no HDL, test, script or generated artifact in the diff. The commit is one line with no trailer.
- **Evidence:** branch `629-b7-review-evidence`, pinned at `c6ad37e7`. The branch tip is `33f91426`, and `95448218`, `d36de704` and `c6ad37e7` are all its ancestors, so nothing was force-pushed. The round-3 author packet is `author-r3/` at `8516e544`, and the live PR body is byte-equal to `author-r3/PR-BODY.md`.
- **Order kept:** I completed my own pass over the diff before reading R450-2 (5970571369) and R451-2 (5970594456). I did not read R450-3.

## Round-2 findings: judgement at this head

| Finding | Status | Evidence at `40714c1b` |
|---|---|---|
| R451-2 F1 = R450-2 F1 (a): a private capture value on the page and in the pinned evidence | **Resolved** | The value-blind scan (`receipts/privacy_scan_c6ad37e7.txt`, rc 0) finds 0 channel-count and 0 format matches in four places: the page, the findings index, the lines this PR adds, and the lane's commit messages. It also finds 0 in the live PR body, `author-r3/PR-BODY.md`, `author-r3/HANDOFF.md`, and all 481 blobs of the evidence at `c6ad37e7` (paths included). The evidence tip `33f91426` (562 blobs) is also clean. Positive controls fire on the pre-mask history: 2 and 2 matches at `95448218`, and 7 matches in the capture name at `d36de704`. The only match tied to this PR is one format token on a line the PR **removes** (lane B6's dev row at :596, as the assignment authorised). The page states the handling of the already-public commits at :1229-1230 |
| R451-2 F2 = R450-2 F1 (b): the masking described | **Resolved** | :1214-1238 checked against `git show d36de704` and `git show c6ad37e7`. (1) At `95448218` the lane redaction masked the count only in the `NCH, CAP_L, CAP_R = ...` assignment of `run_b7.py`/`run_b6.py`, and the format nowhere. (2) `d36de704` masked the count in four docstrings, and the format in two docstrings plus the capture command's `-f` argument in code. (3) `c6ad37e7` masked the count in the capture-file name in 19 files: `RAW-ARTIFACTS.json`, 7 `events.jsonl`, 7 `-lock.txt`, and four tool code lines. "Four tools" at :1203 matches the 4 tool entries in `redaction.json`, out of its 227 files. The pin is `c6ad37e7` at :1209 |
| Hash rows at the new pin | **Hold, 45 of 45** | `scripts/check_hash_rows.py` → `receipts/hash_rows_c6ad37e7.txt`, 0 problems. The first 19 raw rows are raw-file records in `events.jsonl`, and the last 7 are only in `RAW-ARTIFACTS.json`. 17 evidence rows equal the published blob and `MANIFEST.json`'s `published_sha256`. The 2 masked tools equal `redaction.json`'s `original_sha256`, and the chain retained → MANIFEST original → published is consistent. The masking commits changed no cited file other than those two tools. `c6ad37e7` changed only the capture name in `RAW-ARTIFACTS.json`, `events.jsonl` and `-lock.txt`. The (bytes, sha256) set in `RAW-ARTIFACTS.json` is identical at `95448218` and at the pin. Mutation probes catch all three planted faults, and the unmutated page also passes at `d36de704`, `95448218` and the tip (`receipts/hash_checker_probes.tsv`) |
| R451-2 F3 = R450-2 RES-1: B0's next command | **Resolved** | :946-948 checked against `runs/b0/ctl.jsonl` lines 202-222. Seq 22912 is `counters-dut-36-0` (0x0024 CLOCK_DOMAIN) with TIMEOUT. Seq 22913 is `counters-dut-6-0`, which is STREAM_OUTPUT 0 (0x0006), and returned SUCCESS. The mark's other three DUT commands are seq 22914 (6-1), 22916 (5-0) and 22917 (5-1), all SUCCESS within 2 ms. Seq 22915 is the peer's. The text is R450-2 RES-1's exact sentence plus the seq. The times 15:20:58 and 15:25:57 CEST equal the records |
| R450-2 RES-2 | **Resolved** | :1166-1168 is the exact sentence. Each of the 7 captured runs' `events.jsonl` holds 7 raw-file records, equal to `RAW-ARTIFACTS.json`'s non-grade entries for that run, the tone loop among them |
| R450-2 RES-3 | **Resolved** | The PR body's "Round 2" table is numbered 1 to 9 with no duplicate |
| R451-2 RESIDUE-1: the 32,768-tick bound | **Resolved** | :993-994 cites `docs/design/TIME_SYNC.md`. Its "Clock-source settle" row (:385) reads "engaged for 32768 ticks", and the RTL agrees (`hdl/milan/milan_datapath.sv:6266`, `SRC_SETTLE_CEIL_C = 32768`; :6278-6279) |
| R451-2 RESIDUE-2 / R451-1 RESIDUE-2: 12 vs 11 | **Resolved as fixed** | `author-r3/HANDOFF.md` step 5 reads "11 live AECP descriptors byte-equal, plus the CLOCK_SOURCE 3 absence check", with 0 occurrences of "12 live". The as-run handoffs are not rewritten, as allowed |
| R451-2 S1 | **Taken; one text missed (RESIDUE-2 below)** | :760-764 names the heading at `author/HANDOFF.md:66` and the `grade_b7.py` docstring (:10), and `author-r2/HANDOFF.md:85` carries the corrected heading. The same packet's row 9 (`author/HANDOFF.md:35`, "before any graded case") is a third superseded text that the sentence does not count |
| R451-2 S2 | **Taken, true** | :985-988, :711 and :1129 checked against `runs/baaf/events.jsonl`. SLIP_LB (`0x8D4[15:0]`, REGISTER_MAP :1867) read 380 before the bind (15:37:47.540) and 386 at window-0 (15:38:09.038, 1.2 s after window start 15:38:07.854). That interval holds both binds (15:37:47.597 and :47.751), the set (:47.751) and the 20.1 s from the set to the window. The servo lock poll ended 15:37:55.847 |
| R451-2 S3 | **Taken, true** | :950-953 checked against `tools/b7_tables.py:37-101` and `summary/verdicts.json`. B0's only check is "counted ratio beyond 2 ppm" (5.924). The one CLOCK_DOMAIN-counter criterion is B-AAF's, reading `window-mark-0` and `window-mark-2`, which are the first and last of 3 marks |
| R450-2 S1-S4 | **Not taken (optional, outside the round-3 assignment)**; retained as suggestions | S4 (a device-class mention in `author-r2/HANDOFF.md`) is the manager's privacy-pass call, carried below |
| Round-1 findings (R450-1, R451-1) | **No regression** | The round-3 delta touches only the lines listed above. `receipts/verdict_cells_round3.txt` shows 0 verdict or judgement cells changed `f4eb39d3`→`40714c1b`; the only key change is the cap-lr row label |

**No case verdict changed.** Every verdict cell at the head is the same as before: Identity, Tools and B-CRF PASS; A0 and B0 PASS as a control; A1, A2 and B-AAF PASS; Direction B THD+N NOT RUN; lock loss observed as declared. The acceptance rows are unchanged in round 3. The only judgement change since round 1 is the Fabric row's narrowing in round 2 (`receipts/verdict_cells.txt`). The PR still says `Refs #629`.

## Findings at this head

**RESIDUE-1 - lens: Docs - PR body "Evidence" paragraph (live body line 46 = `author-r3/PR-BODY.md:46`)**
- **Evidence:** the body says "Neither changed a file the page's evidence table cites". Its own bullets (lines 43-44) say that both commits changed the code of `run_b7.py` and `grade_b7.py`. The evidence table cites both of those at page :1250-1251. The page says it correctly at :1235-1236: "Neither commit changed any other file this table cites". The hash rows hold (45 of 45).
- **Why RESIDUE:** this is wording only. No hash, measurement, verdict or redaction state changes, and the bullets above it state exactly what was masked.
- **Exact fix:** "Neither changed any other file the page's evidence table cites: the two masked tools' rows are their as-run hashes from `redaction.json`, and the raw rows are recorded unchanged."
- **Verification:** compare against `git show --name-only d36de704 c6ad37e7` and `receipts/hash_rows_c6ad37e7.txt`.

**RESIDUE-2 - lens: Docs - `docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md:760-762`**
- **Evidence:** the page says the order "supersedes two as-run texts that say otherwise": the heading and the docstring. The published `author/HANDOFF.md:35` (row 9, "Grading criteria fixed | 14:50, before any graded case") is a third.
- **Why RESIDUE:** this is wording only. The order and times the page gives are correct, and `author-r2/HANDOFF.md:54` corrects row 9.
- **Exact fix:** "The order below supersedes three as-run texts that say otherwise: that record's heading and its row 9 in the published `author/HANDOFF.md`, "before any case ran" and "before any graded case", and the docstring of `grade_b7.py`, "each fixed before any graded case"."
- **Verification:** grep "before any" in `author/HANDOFF.md` at `c6ad37e7`.

**S1 - SUGGESTION (to the manager; out of lane, already on dev) - lenses: Docs - lane B6's published packet, `b6-review-evidence` at the page's pin `422dcf91` (:621) and at the tip `b23b7dd9`**
- **Evidence:** the same value-blind scan finds the capture's **sample format**, but not the channel count, in two B6 tool files: `run_b6.py` (2) and `probe_attribution.py` (1). See `receipts/privacy_scan_b6_evidence_422dcf91.txt` and `..._b23b7dd9.txt`.
- **Why not this PR's finding:** this PR does not create, cite anew or change that packet. The page's B6 pointer is dev text that the diff does not touch, and the round-3 assignment scopes the evidence check to `c6ad37e7`. Under the 5970598673 ruling, though, the value is private.
- **Suggested outcome:** a top-only mask of lane B6's packet like `d36de704`, or a public Issue.

**S2 - SUGGESTION (new Issue; out of lane, already on dev) - lenses: Docs, RTL - `docs/design/MEDIA_CLOCK_FOLLOWING.md:311`**
- **Evidence:** this row cites `hdl/milan/milan_datapath.sv:6079-6126` for "#386 render recentre after a settled source change". At this head those lines are the stream-RX monitor and AAF depacketizer instantiation. The settle and recentre-arm logic is at :6255-6310 (`SRC_SETTLE_*`, `src_pend_r`).
- **Scope:** this PR only links the design page's "Switching sources" section, not that row.

**S3 - SUGGESTION - R450-2 S1-S4 carried as optional**
- They remain available. S4 is a privacy-pass item for the manager.

## Lens ledger (reviewer-owned)

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #629 acceptance rows (:1123-1144) and the PR's `Refs #629`, both unchanged in round 3 (`receipts/verdict_cells_round3.txt`). The B0 command identity against IEEE 1722.1 descriptor-type codes (0x0024 CLOCK_DOMAIN, 0x0006 STREAM_OUTPUT, 0x0005 STREAM_INPUT) in `runs/b0/ctl.jsonl` seq 22912-22917. The privacy contract (CONTRIBUTING section 6, ruling 5970598673) against the page, the PR body and the evidence (`receipts/privacy_scan_c6ad37e7.txt`) | R451-3 | 40714c1bd166c2a05f9607a861e8550c705d183a |
| RTL | CLEAN | There is no HDL in the diff (`git diff --name-only bbf704ec..HEAD`). The round-3 RTL-bearing claims were checked against the RTL and register map: the 32,768-tick bound (`hdl/milan/milan_datapath.sv:6264-6279`, `docs/design/TIME_SYNC.md:385`) and the SLIP_LB field and unit (`docs/reference/REGISTER_MAP.md:1867`) against `runs/baaf` reads 380/386/388/390. S2 is a dev-side line-reference suggestion | R451-3 | 40714c1bd166c2a05f9607a861e8550c705d183a |
| Robustness | CLEAN | The B0 timeout record: the composition of mark 1, no retry, the next mark answered, and the only non-SUCCESS (`runs/b0/ctl.jsonl`, `runs/b0/events.jsonl`). The independence of grading from the missing mark (`tools/b7_tables.py:37-101`, `summary/verdicts.json`, so a missing mark 2 would fail B-AAF rather than pass it silently). The 6-dup bracket and its interval contents (`runs/baaf/events.jsonl`) | R451-3 | 40714c1bd166c2a05f9607a861e8550c705d183a |
| Tests | CLEAN | 45 of 45 hash rows at `c6ad37e7`, with three mutation probes all caught and three other pins passing (`receipts/hash_rows_c6ad37e7.txt`, `receipts/hash_checker_probes.tsv`). The value-blind privacy scan's positive controls fire before masking (`receipts/privacy_scan_*.txt`). The docs gates at head all return rc 0 (`receipts/gates/rc.txt`) | R451-3 | 40714c1bd166c2a05f9607a861e8550c705d183a |
| Docs | CLEAN (RESIDUE-1, RESIDUE-2 carried) | Page :596, :711, :756-768, :943-953, :982-998, :1129, :1164-1261. The live PR body (`receipts/pr644_body_live.md`) and `author-r3/PR-BODY.md` / `HANDOFF.md` at `8516e544`. `docs/findings/README.md`, unchanged since `4eee41a5` | R451-3 | 40714c1bd166c2a05f9607a861e8550c705d183a |

## Validation run (all in the foreground at the exact head; the clone was restored and verified)

- **Documentation gates** (`scripts/run_doc_gates.sh` → `receipts/gates/`), using the pinned Markdown environment installed with `--require-hashes` from `tools/markdown/requirements.txt` (`receipts/gates_venv_freeze.txt`). Each returned rc 0:
  - `docs_check.py` (0 findings);
  - `check_doc_style.py`;
  - `gen_toc.py --check` and `--verify-anchors`;
  - `check_em_dash.py --base bbf704ec` (0 findings over 577 added lines);
  - `check_doc_paths.py`;
  - `ci_scope.py --selftest`;
  - `check_feature_status.py --self-test`;
  - `git diff --check` against `bbf704ec` and against `f4eb39d3`.
- **`check_baremetal_only.py`:** `--check` and `--selftest` returned rc 2 in that environment only because pyyaml is not installed there. They returned rc 0 with the host interpreter, which has pyyaml 6.0.3 (`*_systempy.log`).
- **Hosted contexts at the exact head** (`receipts/pr644_head_checkruns.tsv`, read when the report was written):
  - 7 executed and succeeded: `rtl-fast`, `full-ci-gate`, `changes`, `elaborate`, `bdd-conformance`, `wire-accountability` and `docs-check-no-git`;
  - 7 were skipped: `verilator-suites`, `yosys-portability`, `verilator-lint`, `yosys-elaboration`, the two shard matrices and `Physical gPTP`. Skipped contexts did not execute and are not evidence;
  - `docs-check` was **still in progress**, started 15:43:06Z.
- **Restore** (`receipts/restore_verification.txt`):
  - HEAD and tree are exact, the index tree equals the HEAD tree, and status is clean;
  - all 994 tracked blobs rehash equal, with 0 mode mismatches;
  - the 4 gitlinks are equal in HEAD and the index: `external` `efeb541a`, `gptp-processor` `5dce647a`, `protocol-processor` `631eeb34` and `third_party/verilog-axis` `48ff7a7e`;
  - the only repository change is two remote-tracking refs fetched for read-only evidence access.

## Real limits

- **Literal values only:** the privacy scan matches the two values in their literal and stated forms (number with a channel word, file-name form, `NCH`/`-c` assignments, number words, ALSA format token). It does not judge quantities a reader could derive from published byte counts. The pre-mask values also stay in public history at `95448218`/`d36de704` by the manager's top-only ruling, which the page states.
- **Masked tools' byte counts:** the as-run byte counts of the two masked tools (32,321 and 27,057) have no public record; only their hashes are checked.
- **No hardware:** there was no bench or hardware access. Every bench figure rests on the published run records, and physical calibration was NOT RUN. Skipped hosted contexts and field skips are not hardware proof.
- **Not run:** no RTL bank, builder bank or Verilator run was needed or run for this docs-only delta.

## Pending manager duties

- Hosted acceptance at the exact head: `docs-check` was still running when this report was written.
- Carry RESIDUE-1 and RESIDUE-2 to the residue checklist.
- Decide S1, lane B6's published packet still carrying the capture format, under the 5970598673 ruling, and R450-2 S4.
- Build and validate the current-dev merge candidate at the merge turn (source base and live dev are both `bbf704ec`). Merge requires two independent positive reviews and maintainer authorization.

R451-3 FINISHED
