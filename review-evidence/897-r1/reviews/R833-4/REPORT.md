[R833] POSITIVE - exact head f098f893d57e0fa3ec95a7e459313c5cfe4f4224

# R833-4: evidence-only re-check of PR #898 (issue #897), round 3 head unchanged

- **Head under review:** `f098f893d57e0fa3ec95a7e459313c5cfe4f4224`, tree `3cdb680fe1bd3729d441c02160e69c20f2ac707a`. Both were verified in the clone. The head is unchanged since R833-3.
- **Evidence archive:** branch `897-review-evidence` at `ed8af0f4`. The receipts commit is `69b998fb`, on round 3's packet `b4ae9cfc`.
- **Scope:** this round only re-checks R833-3 F1, which was the sole open finding (MINOR, Tests and Docs). No code is re-reviewed. R833-3's other lens results stand, because nothing they depend on has changed: the head, the tree and the packet's `INDEX.md` are all the same bytes.
- **Verdict:** POSITIVE. F1 is resolved.
  - All 11 indexed receipts are now published, and each matches its `INDEX.md` size and sha256.
  - They support every GET_AS_PATH per-word and notice-round figure that `SPLIT_CONTROL_MEMORY.md` section 13 states at this head.
- **New findings:** three SUGGESTIONs (S3 to S5), none blocking. R833-3's RESIDUE (R1 to R3) and SUGGESTIONs (S1, S2) are retained unchanged.

## 1. Reconstruction

- **Contract:** AGENTS.md sections 6 and 7. Coverage is banked per lens against a commit. An open MINOR leaves its lenses unclean.
- **Prior round:** R833-3's archived report (`review-evidence/897-r1/reviews/R833-3/REPORT.md` at `ed8af0f4`).
  - F1's required outcome: publish the 11 receipts listed at `author-r3/receipts/INDEX.md:550-560`, so that their bytes match the INDEX or a recorded redaction. No source commit is needed.
  - I read that report only after my own pass over the 11 files and section 13 (sections 2 and 3 below).
- **What the receipts commit changed:** `git diff --name-status b4ae9cfc9f 69b998fb99` adds exactly the 11 files and modifies only `MANIFEST.json`.
  - `INDEX.md` is blob `59e80d6b38e6f1ce6d2b03aa9b72604ebb52bd73` at both `b4ae9cfc` and `ed8af0f4`, so the index R833-3 read is the index I checked against (`receipts/clone_restore.txt`).
- **Head check:** the clone's worktree and index equal `HEAD`, the index writes tree `3cdb680f`, and the six gitlinks are as at the head (`receipts/clone_restore.txt`). `external` is uninitialised in this clone; its gitlink `efeb541a` is unchanged.

## 2. The 11 receipts: bytes against `INDEX.md`

Command: `python3 -I scripts/verify_scratch_receipts.py <archive>/review-evidence/897-r1/author-r3`. Receipt: `receipts/verify_scratch_receipts.txt`.

| Receipt (`receipts/harness/scratch/`) | Size | sha256 = INDEX row |
|---|---:|---|
| `cl-path.diff` | 3793 | OK `e6965d6b...aca2d6` |
| `cl-rows.diff` | 728 | OK `7f18d7f0...bc5b34` |
| `cl-span.diff` | 1033 | OK `24fd9bb7...4883ca` |
| `flip-1x1-build730.log` | 1186 | OK `5dd736c4...614a4f` |
| `pN1-notice-burst-0-mbx_win_read.txt` | 1581 | OK `2394d3a1...677dbc` |
| `pN1-notice-every-0-mbx_win_read.txt` | 1530 | OK `b2a9ff43...3807c7` |
| `path_round.txt` | 418 | OK `cb50743c...10d6d4` |
| `sA1-aecp-mbx_win_read.txt` | 98 | OK `5754dc94...4dbac3` |
| `sA1-datapath-events-mbx_win_read.txt` | 833 | OK `a79b6c59...98f43c78` |
| `summary-pN1.txt` | 6406 | OK `a7ee6dfa...076be8` |
| `summary-sA1.txt` | 3494 | OK `29ac94ff...1566f5` |

- **Result:** listed 11, present 11, bad 0, no unlisted file, rc 0.
- **Manifest:** `MANIFEST.json` has 11 entries for these files, none `path_redacted`, each with `published_sha256` equal to `original_sha256`.
- **Prior verifier:** R833-3's own `verify_packet.py`, re-run over the archive at `ed8af0f4`, reports `manifest author-r3 entries 615 verified 615` and `INDEX rows 593 not published 0` (`receipts/verify_packet_ed8af0f4.txt`).
- **Privacy:** the 11 files contain no host path or identity. Build paths read `<scratch>/...` (`receipts/scratch_receipts_scan.txt`).

## 3. Do they support section 13's GET_AS_PATH figures at `f098f893`?

The figures are at `docs/design/SPLIT_CONTROL_MEMORY.md:2481-2489`, under "GET_AS_PATH through the face". `scripts/recompute_path_figures.py` recomputes each one from the published bytes; it reported 22 checks OK and 0 bad (`receipts/recompute_path_figures.txt`).

| Section 13 claim (line) | Published evidence | Result |
|---|---|---|
| Unanswered (arm A, test SoC never answers): "378 to 796 CPU cycles a word" (2486) | `sA1-aecp-` and `sA1-datapath-events-mbx_win_read.txt`: 19 `mbx_win_read` spans, least 378, most 796 | holds |
| Arm A: "no round over its stated cost (`round_grade.py`)" (2486) | `summary-sA1.txt`: rc 0, "0 budget misses", no `STATED` line. At the head, `run.py:143-170` turns every `round_grade` over-cost round into a `STATED` line, and `run.py:811-819` passes those lines into the verdict | holds |
| Answered, scratch `answering-every-port` arm: `path` reads the count and eight entries and answers the eight (2486) | `cl-path.diff`: `p_path` makes one kind-2 count read, then `min(cap, 8)` entry reads, and answers `k` entries | holds |
| The round that builds it: 46,397 (`notice-every-0`) and 47,490 (`notice-burst-0`) CPU cycles; eight entries 3,032; admitted 59,500, a cold start and two notices (2486) | `path_round.txt`: 46,397 and 47,490, both "8 entry reads (3032 cycles), 2 notices, 0 refused attempts; admitted at 59500". The pN1 extracts reproduce the 8 entry reads, their 3,032 cycles and the most per entry (386). 59,500 = (`AECP_ROUND_COLD_US` 85 + 2 x `AECP_NOTICE_US` 255) x 100, and those constants are at `aecp_mbx.h:28-29` at the head | holds (see S3 on the round half's raw inputs) |
| "in both groups no round, notice or pass is over its bound" (2486) | `summary-pN1.txt`: rc 0, "0 budget misses (0 of 35 probe instances, 0 of 7 paths), 0 of 2775 work passes over" the share, no `STATED` line, and all 24 `NOTICE` lines `within`. Its longest THE RETRY round is 48,228, against the 90,000 slice | holds, independently of `path_round.txt` |
| "the most a word took (877 cycles)" (2487) | The count read's most is 877 in both pN1 extracts; it is the largest span in all four extracts | holds |
| Record estimate: "about 19,950 cycles, 200 us", against `record.aecp` 235 us (2487) | Inputs: 11,655 (`harness/measure/record_spans.txt`, `get_avb_info.if0`), 877 (above), 60 (`harness/measure/mbx_read.txt`, `.../7/60`). 11,655 + 8 x 877 + 16 x 60 = 19,631, and with 18 data words (R833-3 R2) 19,751. Before the 64 B copy, both are under 23,500 | holds |
| `AS_PATH_CHANGED` 30.02 us, and 30.64 / 23.34 for the other two events, against 35 / 35 / 30 (2485) | `harness/measure/eventcost-hA1.json` (published since `b4ae9cfc`): 30.64, 30.02, 23.34. `rows_tiers.py:99` holds 35 / 35 / 30 at the head | holds (see S4) |
| Flip check: "txL 48.09 ms within 49" (2489) | `gates/lane/flip_check_1x1.log:16` and `early/flip_check_1x1-head.log:15` both read 48.09 | holds |

Context checks:

- **`flip-1x1-build730.log` (txL 48.10) is not a section 13 figure.** It is the what-if run with `CTRL_LOOP_BUILD_ONE_PASS_US` set to 730 (`cl-rows.diff`), which the PR body and REVIEW READY describe ("the rows solved at 730 us still pass"). Its RESULT is PASS, which agrees with my R833-3 probe and with S1.
- **The measured tree is the reviewed code.**
  - Both summaries name `HEAD e45981f8... DIRTY`. That commit is an ancestor of `f098f893`, and the dirt is the published scratch diffs.
  - The preimage blobs in those diffs match the head: `build.py` is `a9f72f3d2b` and `ctrl_loop.h` is `5d75589a60` at both `e45981f8` and `f098f893`.
  - The only firmware change in `e45981f8..f098f893` is `aecp_maps.c`. It changes comments, splits `MAP_SLOTS` into named macros of the same value, and moves a `_Static_assert`. It generates no code, and R833-3 recorded every image byte-identical.
- **R833-3's own verification step 2 was mis-specified, and I correct it here.** It asked that `path_round.py` "over the published pN1 logs" print the two rounds. The published pN1 files are `mbx_win_read` extracts, not whole logs. Re-run over them, `path_round.py` reproduces the entry and count reads exactly but prints no round line (`receipts/path_round_inputs.txt`).
  - F1's required outcome was publication matching the INDEX, and that is met.
  - The round figures rest on the hash-bound `path_round.txt`, the published tool and scratch arm, and the harness's own independent round grading (row 5 above).
  - I therefore count F1 as resolved, and record the reproducibility residual as S3.

## 4. Findings

### F1 (R833-3) - MINOR - Tests, Docs - RESOLVED at this head

- **Where:** `SPLIT_CONTROL_MEMORY.md:2486-2487`; archive `author-r3/receipts/INDEX.md:550-560`.
- **Evidence:** sections 2 and 3. All 11 files are published, they match the INDEX byte for byte, the archive reports `not published 0`, and every figure they carry recomputes.
- **Verification:** `receipts/verify_scratch_receipts.txt`, `receipts/verify_packet_ed8af0f4.txt`, `receipts/recompute_path_figures.txt`.

### S3 - SUGGESTION - Tests, Docs (new)

- **Where:** archive `author-r3/receipts/harness/scratch/path_round.txt`; `author-r3/scripts/path_round.py`.
- **Evidence:** `path_round.py` derives each round from `ctrl_loop:round_of` SPAN lines and `aecp_command` / `aecp:finish` CALL lines. The published pN1 files hold only `mbx_win_read` SPANs (0 `round_of` or CALL lines). The whole pN1 logs are neither published nor hash-listed (`gates/large/` names none), so only the tool's output carries the exact 46,397 and 47,490.
- **Impact:** a cold reviewer cannot re-derive the two round figures from published bytes. Their bound ("no round over its bound") is independently supported by `summary-pN1.txt`'s grading, and no figure is in doubt.
- **Optional outcome:** publish an excerpt of the two pN1 group logs holding the `round_of` SPANs and the `aecp_command` / `aecp:finish` CALLs, or record the whole logs' sha256 in `gates/large/`. `path_round.py 0000ef90 <excerpts>` would then reprint `path_round.txt`.

### S4 - SUGGESTION - Tests (new)

- **Where:** archive `author-r3/receipts/harness/measure/eventcost-hA1.json`, key `AMAP_LIVE_WRITE.stated_us`.
- **Evidence:** the receipt says `stated_us: 25`. The head's `rows_tiers.py:99` and `SPLIT_CONTROL_MEMORY.md:2354` and `:2485` state 30 at 1x1/1if. The copied `eventcost.py` apparently carries a pre-direct-index table.
- **Impact:** none on any claim. 23.34 is within both 25 and 30. A reader comparing the receipt with the doc sees two different stated costs.
- **Optional outcome:** in a later packet, have the tool read `rows_tiers.DATAPATH_US` from the tree.

### S5 - SUGGESTION - Docs (new)

- **Where:** archive `author-r3/receipts/harness/measure/record_spans.txt`.
- **Evidence:** all four rows are labelled `builds/aecp.log`, and they carry `get_avb_info.if0` as 11,655, 11,685, 10,201 and 10,982. Section 13 cites 11,655 as arm A's, but the receipt does not say which build each row is.
- **Impact:** none on the conclusion. Using the largest row, 11,685, the estimate moves by 30 cycles and stays about 200 us, under 235.
- **Optional outcome:** label each row with its build (head or base, and shape).

### Retained from R833-3, unchanged at this head

The head and the doc are byte-identical to R833-3's.

- **R1 RESIDUE (Docs):** `SPLIT_CONTROL_MEMORY.md:488` and `:2483` say "at the merge of `894-tiers` `5b264bf2`". Fix as R833-3 states.
- **R2 RESIDUE (Docs):** `:2487`, "their answers' two data words each". Replace with "the nine answers' two data words each (18 reads)". The now-published 877 makes the 18-read sum 19,751 before the copy, so the figure is unaffected.
- **R3 RESIDUE (Docs, PR body only):** the reviewer lines in the PR body. For this round, also name R833-4 as F1's re-check at `f098f893`.
- **S1 SUGGESTION (Conformance, Docs):** 725 vs 730 us, routed to #894/#902's owner. `flip-1x1-build730.log` now publishes the author's own 730 us PASS as well.
- **S2 SUGGESTION (Docs):** the INDEX is not regenerated after the 4 redactions. Unchanged: the 11 new files needed no redaction.
- **Other prior findings:** the R834-1 and R833-1/-2 items tabled in R833-3 section 6 keep the status R833-3 gave them. R833-1 S1 (the answering arms' path stand-ins answer an empty sequence) stays a SUGGESTION. Its measured answer, the scratch arm, is now published.
- **Comment rule:** no source delta in this round, so there is no new comment residue.

## 5. Per-lens results at `f098f893`

- `[R833] PASS Conformance` — `SPLIT_CONTROL_MEMORY.md:2481-2489` against the receipts in section 3; `aecp_mbx.h:28-29`; `rows_tiers.py:99`. No code is re-reviewed, and R833-3's Conformance coverage stands at this same head.
- `[R833] PASS RTL` — no artifact changed. The head, the tree and the gitlinks are identical (`receipts/clone_restore.txt`), so R833-3's RTL coverage stands.
- `[R833] PASS Robustness` — no artifact changed. The 730 us what-if is now published (`flip-1x1-build730.log`, RESULT PASS), and R833-3's coverage stands.
- `[R833] PASS Tests` — the 11 receipts are verified by sha256 against `INDEX.md:550-560` (`receipts/verify_scratch_receipts.txt`). Every figure they carry is recomputed (`receipts/recompute_path_figures.txt`). `run.py:143-170, 811-819` was read to confirm that the summaries' rc 0 implies round grading. F1 is resolved; S3 and S4 are SUGGESTIONs.
- `[R833] PASS Docs` — section 13's GET_AS_PATH claims are each tied to a published receipt (section 3), and the archive reports `not published 0`. F1 is resolved; R1 to R3 are RESIDUE, and S2, S3 and S5 are SUGGESTIONs.

## 6. Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | merged `aecp/`, `app/`, `ctrl_plat.c` diff; campaign logs; flip check (R833-3). Section 13 GET_AS_PATH figures against receipts (R833-4) | R833-3, re-confirmed R833-4 | f098f893d57e0fa3ec95a7e459313c5cfe4f4224 |
| RTL | CLEAN | file set `7398ec0a..f098f893` (no `hdl/`), gitlinks, `KL_gptp_engine.sv:781-785`, sweep shards (R833-3); gitlinks unchanged (R833-4) | R833-3 | f098f893d57e0fa3ec95a7e459313c5cfe4f4224 |
| Robustness | CLEAN | `plat_ledger.log`, `fixtures.log`, `images.txt`, `sram-layout.txt`, 730 us probe (R833-3); `flip-1x1-build730.log` (R833-4) | R833-3 | f098f893d57e0fa3ec95a7e459313c5cfe4f4224 |
| Tests | CLEAN | the 11 `harness/scratch/` receipts by sha256 against `INDEX.md:550-560`; recomputed figures; `run.py` round grading; `path_round.py` re-run; R833-3's suite and campaign evidence | R833-4 | f098f893d57e0fa3ec95a7e459313c5cfe4f4224 |
| Docs | CLEAN (RESIDUE R1-R3; SUGGESTION S2, S3, S5) | `SPLIT_CONTROL_MEMORY.md:2354, 2481-2489` against receipts; archive `MANIFEST.json`/`INDEX.md` (`not published 0`); R833-3's doc and PR-body review | R833-4 | f098f893d57e0fa3ec95a7e459313c5cfe4f4224 |

All five lenses are banked against `f098f893`. No commit lies between the covering rounds and this head.

## 7. Real limits

- **Evidence-only round.** I did not re-run the harness, the scratch arms, the campaigns, the suites or the sweep.
- **Round figures not independently re-measured.** The exact 46,397 and 47,490 rest on the author's hash-bound `path_round.txt`. Their bound is corroborated by the harness's own grading (S3).
- **Not signed.** The packet is verified by hash against its INDEX and manifest, not by signature.
- **No manager source bank.** None ran at this head, and none is claimed. Source-head execution evidence is the author's published receipts. Hosted CI does not run on split PRs.
- **No current-dev candidate built.** The candidate (source base `7f50ee6a`, live dev `b7d692952305e4e0e132abb8f99c339eeb17a873`) was not built by me.
- **No hardware.** Physical calibration was NOT RUN. Field skips are not hardware proof.
- **No probes.** This round used no Docker, act or hardware, and made no source edits. The clone was verified unchanged at the end.

## 8. Pending manager duties

- Carry R1 to R3 to the residue checklist, and update the PR body (R3, now naming R833-4 as well).
- At the merge turn:
  - build and validate the current-dev merge candidate (builder and native banks), and link its receipts on the PR;
  - confirm that #902's merge into `dev-soft-core` leaves the composition as reviewed (`7398ec0a` plus the merge commit).
- Route S1 (725 vs 730 us) to #894/#902's owner. S3 to S5 are optional for a later packet.
- Merge authorization remains the maintainer's.

R833-4 FINISHED
