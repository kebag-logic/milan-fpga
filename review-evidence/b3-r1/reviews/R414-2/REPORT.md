[R414] POSITIVE - exact head a66996aae46bc4a3eb2d8a4822d12d5186aa04eb

# R414-2: internal independent re-review of PR #624 (issue #617 acceptance 4, issue #451 USB Audio capture)

- **Head:** `a66996aae46bc4a3eb2d8a4822d12d5186aa04eb`, tree `e45645cd5599cbfad06d0dc44e11c2a35caee56e`.
  - It is one documentation commit on my round-1 head `6dfa64a7506a8660a70d77eaa7c96c5de2886f5d`, and two commits on dev `ec0cc0c1df7d7ab3e25d973958f53f0074393d2c`.
  - `git diff --stat 6dfa64a7..a66996aa`: 3 files, +51 -14, all under `docs/findings/`.
  - Both commit messages are one line with no body or trailers.
- **Round R414-2, cleared context.** Reconstructed from:
  - AGENTS.md, CONTRIBUTING.md (sections 2, 3 and 6) and docs/README.md;
  - the #617 body and every #617 comment, in particular the B3 assignment 5903384996 and the round-2 assignment 5904487454 (items 1-7, with the index ruling);
  - the PR #624 body;
  - the diff and history;
  - the published evidence at `c721867b7ec772b0bfc928962979f3b32c4bb0d8`: branch `b3-review-evidence`, `review-evidence/b3-r1/author/` and `author-r2/`.
- **Order:** I made my own pass over the diff first. After it I read my own round-1 report (R414-1). I read the other reviewer's round-1 report only after this verdict and ledger were written; see [Prior findings](#prior-public-findings-resolved-or-retained).

## Verdict summary

Every round-1 finding is resolved at this head, and every assignment item is met:

- **F1, the findings index:** resolved as ruled.
- **F2, the McASP0 rate:** resolved. The rate re-derives with my round-1 script, byte-identical.
- **F3, the packet locator:** resolved. All six tool-hash rows on the two pages match `author/tools`.
- **Assignment items 4 to 7** (R415-1 S1 to S4) are each true against the published data or the RTL.

The measurement tables are byte-identical to round 1, except the two McASP0 rate cells that item 2 requires. The PR says `Refs #617` and `Refs #451` only, and no closing keyword appears anywhere. No private names appear. The docs gates return rc 0 in the pinned Markdown environment.

Two new SUGGESTIONs and three carried optional items remain. None affects coverage, so every lens is covered clean and the verdict is POSITIVE. #617 acceptance 4 stays met, with the measured figures unchanged.

## Findings

No BLOCKER, MAJOR or MINOR finding is open at this head.

### S1: SUGGESTION (Docs). The edge-frame sentence reads "45,587" as a count

- **Where:** `docs/findings/617_DIN_FRAME_COHERENCE_BENCH.md:159-160`: "The edge frames, 45,587 before the region and the 777 transition frames after it".
- **Evidence:**
  - Packet `author/runs/din-long/grade.json` gives `region.first_frame` 45,588. So 45,588 frames precede the region.
  - The edge frame meant is the single frame 45,587. The page's own `:164` and the PR body ("frame 45,587 and the 777 transition frames") say so. Next to "the 777 transition frames", the sentence reads as a count off by one.
- **Impact:** wording only. The census behind the sentence is exact (`receipts/r2-claims.txt`).
- **Suggested outcome:** "frame 45,587, just before the region, and the 777 transition frames after it".

### S2: SUGGESTION (Docs). The pages name the round-1 packet only; the round-2 corrections sit beside it unnamed

- **Where:** `617_DIN_FRAME_COHERENCE_BENCH.md:275-278` and `451_USB_AUDIO_CAPTURE.md:216-219`.
- **Evidence:**
  - The named location, `review-evidence/b3-r1/author/`, is the immutable round-1 archive. Its `HANDOFF.md:30` still reads "McASP0 RX 250.7 periods/s".
  - The corrected handoff, the rate receipt and frame 1,632's eight words (the data behind `451_USB_AUDIO_CAPTURE.md:140-143`) are only in `review-evidence/b3-r1/author-r2/packet/`.
- **Why not MINOR:**
  - Every statement on both pages is correct, and item 3's ruled locator is met word for word.
  - The corrected files sit in the sibling directory, under the same path prefix and branch. `review-evidence/b3-r1/MANIFEST.json` indexes them with hashes, and all 32 match (`receipts/evidence-integrity.txt`).
  - The PR body names them as published beside the round-1 packet.
- **Suggested outcome:** a future edit names `author-r2/packet/` next to `author/` as the round-2 corrections.

### Carried optional items from R414-1 (not taken; no coverage effect)

- **R414-1 S1, the identity chain.** The page now states the limit exactly (`:54-63`). Tying `d178f19a` to the `ec0cc0c1` build artifact stays a manager option.
- **R414-1 S2, the residuals.** The `nvm_pend` consequence is now stated (`:244-252`, via item 6). Two points remain unstated:
  - the inherited monotonic counters (SLIP_LB, SLIP_TDM, RENDER_STAT rails);
  - that the six commits are the binding records.
- **R414-1 S3, the USB attribution wording.** Not taken.

## Round-1 findings and assignment items, judged at this head

| Item | Source | Result at `a66996aa` | Evidence |
|---|---|---|---|
| 1. Index | R414-1 F1 (and R415-1 F1), ruling 5904487454 | **Resolved.** `README.md:12-13` add one row per new page. They sit directly after the first-light row they follow, in file-name order, which is the placement PR #622 used for its 606 and 608 rows after `75_` (`d76763733`). `:11` keeps its first-light text byte-for-byte and appends only the pointer to the `ec0cc0c1` DIN re-run (0 torn) and the USB Audio FAIL, in the form of PR #622's `75_` row. No other index line changes | `git diff 6dfa64a7..a66996aa -- docs/findings/README.md`; prefix check in this round; `receipts/anchor-check.txt` |
| 2. McASP0 rate | R414-1 F2 | **Resolved.** `451_USB_AUDIO_CAPTURE.md:126-127` read 250.0 periods/s. `:129-133` state the consistent bracket: 18,942 and 18,957 periods, 75.78 s and 75.83 s, 47,992 and 47,999 frames/s. My round-1 `mcasp_rx_rate.py` (sha256 `8e242c67…d173`, byte-identical) gives 249.96 and 249.99 periods/s from the published logs, with a restart delta of 5 each. The corrected packet `HANDOFF.md:30,62` is in `author-r2/packet/` and matches its manifest | `receipts/mcasp-rx-rate.txt`, `receipts/evidence-integrity.txt` |
| 3. Locator | R414-1 F3 | **Resolved.** Both pages name `review-evidence/b3-r1/author/` on branch `b3-review-evidence`. All six tool-hash rows on the two pages equal the files there (five distinct tools) | `receipts/evidence-integrity.txt` part 1 |
| 4. Torn count qualified | R415-1 S1 | **Met and true.** `617_DIN_FRAME_COHERENCE_BENCH.md:105-112` describes `grade_617.py`'s `torn()` exactly: it counts only words with a zero low byte, non-zero, and tag 1 to 8. The census holds: 1,191,588 outside frames × 8 = 9,532,704 words, of which 9,526,486 are `ffffff00`, 6,217 are zero (6 + 776 × 8 + 3) and 1 is `fffff000`. None is a pattern word. `:158-167` names the edge frames as graded by inspection (wording: S1) | `receipts/r2-claims.txt` S1 rows |
| 5. Identity items | R415-1 S2 | **Met and true.** VERSION `0x00020060`, AEM CRC32 `93742dd2`, entity `020000fffe000001` and ROM CRC32 `acad92b9` equal `606_FIRST_BIND_MEASUREMENT.md:48-52`. Only the QSPI payload CRC32 differs: `d178f19a` against `d84bce7b`. The packet holds `d178f19a` only as read (`author/identity/console-identity.txt:22`) and no build-side payload CRC, as `:61-63` says | this round's reads of both pages and a packet search |
| 6. `nvm_pend` as one wire | R415-1 S3 | **Met and true, down to the RTL.** `KL_nvm_backend.sv:790,796` gives `pend_w` = `nvm_pend_o`, and `:587` puts `pend_w` at status bit 22. `KL_pp_shadow.sv:1031` connects it to `milan_datapath.sv:7720` → `:2747`, and `milan_csr.sv:2224-2225` places it at `PP_STAT[11]`. Map writes set `KL_pp_shadow.sv:947-955`'s `aecp_live_pend_r`, which clears only on reset. `SAVED_STATE_SNAPSHOT_OWNERSHIP.md` §11 row `0x60`-`0x7F` says the same, as does `REGISTER_MAP.md` at `PP_STAT`/`PP_NVM_STAT` (durable reading needs pend 0). On the bench only PP_STAT bit 11 and PP_NVM_STAT bit 22 move, together; the end state reads dirty 0 and VD_OK, with commits 0 → 6 and seq 229/230 → 235/236. The next-lane consequence (reset first) follows | `receipts/r2-claims.txt` S3 rows; `receipts/anchor-check.txt` |
| 7. Frame 1,632 words | R415-1 S4 | **Met in the packet.** `author-r2/packet/summary/usb-long-frame-1632.json` and `summary.json` carry `016ec820 … 086ec8c0`: tags 1 to 8 in order, one ordinal `0x6ec8`, low bytes `20 38 50 68 78 90 a8 c0`, previous frame silent. That is consistent with `451_USB_AUDIO_CAPTURE.md:140-143,156`. The raw capture is not public (limits) | `receipts/r2-claims.txt` S4 rows |
| Tables byte-identical | ruling 5904487454 | **Met.** In the #617 page all 85 table lines are identical. In the #451 page 37 of 39 are; the other two are exactly item 2's rate cells (`250.7` → `250.0`). The `summary.json` change is additions only | this round's `diff` of `grep '^\|'` lines at both heads |
| Closing keyword | CONTRIBUTING §2, assignment | **Met.** The PR body says `Refs #617` and `Refs #451`. `closingIssuesReferences` is empty. The closing-keyword scan finds 0 hits over the diff, both commit messages and the PR body; a planted control fires | `receipts/public-text-scan.txt` |
| Private names | CONTRIBUTING §6, assignment rules | **Met.** `docs_check.py` reports 0 findings with a 23/23 scrub self-test. My shape scan (addresses, MACs, host paths, e-mail, tool and model tokens) finds 0 hits in the diff, commits and PR body. In the published round-2 packet it finds only generic `/tmp/` staging paths | `receipts/gates/`, `receipts/public-text-scan.txt`, `receipts/author-r2-text-scan.txt` |
| Docs gates | assignment | **rc 0**, all eleven: `docs_check`, `check_doc_style`, `gen_toc --check`, `check_em_dash --base ec0cc0c1` (0 findings over 512 added lines), `check_doc_paths` (860 paths), `ci_scope --selftest`, `check_baremetal_only --check`, `check_feature_status --self-test` (46/46), and `git diff --check` plain, against `ec0cc0c1` and against `6dfa64a7` | `receipts/gates/gates-summary.txt` |

## Lens results (clean lenses in the finding format)

- `[R414] PASS Conformance` — `docs/findings/README.md:11-13`, `617_DIN_FRAME_COHERENCE_BENCH.md:14-20,54-63,105-112,158-167,239-252,275-278`, `451_USB_AUDIO_CAPTURE.md:124-133,216-219`, against:
  - the round-2 assignment 5904487454 (items 1-7 and the index ruling);
  - #617 acceptance 4 (measurement tables unchanged);
  - the PR body's `Refs` lines.

  Receipts: `mcasp-rx-rate.txt`, `r2-claims.txt`, `evidence-integrity.txt`, `public-text-scan.txt`. No open finding under this lens.
- `[R414] PASS RTL` — no RTL in the diff. The new text makes register and RTL claims, checked against:
  - `hdl/milan/KL_nvm_backend.sv:587,790,796`;
  - `hdl/milan/KL_pp_shadow.sv:947-958,1024-1031`;
  - `hdl/milan/milan_datapath.sv:2747,7720`;
  - `hdl/common/csr/milan_csr.sv:2221-2228`;
  - `docs/reference/REGISTER_MAP.md` `PP_STAT` (`0x924`) and `PP_NVM_STAT` (`0x93C`) rows;
  - `docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md` §11.

  One wire, sticky until reset, maps never written: all confirmed.
- `[R414] PASS Robustness` — the round-2 text on frames that mix pattern words with zero or idle words, and on the state across reset. Checked against:
  - `author/tools/grade_617.py:40-42` (`torn()` ignores zero and idle words);
  - `grade.json` `outside_region_words` and `edge_frames` (a full census, with one non-pattern word);
  - `author/restore/dut-start.txt:3,10` and `dut-end.txt:3,9-10` (pend 0 → 1; the durable reading returns only after a reset and an accepted window load, per `SAVED_STATE_SNAPSHOT_OWNERSHIP.md` §4 and §6.1).

  Receipt: `r2-claims.txt`, with a negative control that fails as required.
- `[R414] PASS Tests` — the evidence behind every changed figure:
  - my round-1 `mcasp_rx_rate.py` reproduces the corrected rate;
  - the grading tools are unchanged: their hashes equal the pages and round 1;
  - the round-2 manifest differs from round 1 only by 2 re-hashed and 3 added files, each matching;
  - my own checkers (`anchor_check.py`, `public_text_scan.py`, `check_r2_claims.py`) each carry a negative control that fails as required.

  Receipts: `mcasp-rx-rate.txt`, `evidence-integrity.txt`, `anchor-check.txt`, `public-text-scan.txt`, `r2-claims.txt`. F2, the round-1 Tests finding, is resolved.
- `[R414] PASS Docs` — `docs/findings/README.md`, both pages at this head, and the PR body. Gates rc 0 (`receipts/gates/`). All 9 relative links added this round resolve with their anchors under the pinned renderer (`anchor-check.txt`, with negative controls). F1 and F3 are resolved. S1 and S2 are optional wording and locator suggestions only.

## Reviewer-owned completion ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | assignment 5904487454 items 1-7 against `README.md:11-13` and both pages; table byte-identity; PR body `Refs`; `mcasp-rx-rate.txt`, `r2-claims.txt`, `evidence-integrity.txt`, `public-text-scan.txt` | R414-2 | `a66996aae46bc4a3eb2d8a4822d12d5186aa04eb` |
| RTL | CLEAN | `KL_nvm_backend.sv:587,790,796`; `KL_pp_shadow.sv:947-958,1024-1031`; `milan_datapath.sv:2747,7720`; `milan_csr.sv:2221-2228`; `REGISTER_MAP.md` `PP_STAT`/`PP_NVM_STAT`; `SAVED_STATE_SNAPSHOT_OWNERSHIP.md` §11 | R414-2 | `a66996aae46bc4a3eb2d8a4822d12d5186aa04eb` |
| Robustness | CLEAN | `grade_617.py:40-42`; `grade.json` outside-region census and edge frames; `dut-start.txt`/`dut-end.txt` NVM words; snapshot contract §4 and §6.1; `r2-claims.txt` with its negative control | R414-2 | `a66996aae46bc4a3eb2d8a4822d12d5186aa04eb` |
| Tests | CLEAN | `mcasp_rx_rate.py` reproduction; tool hashes; round-2 manifest delta; `anchor_check.py`, `public_text_scan.py` and `check_r2_claims.py` with negative controls | R414-2 | `a66996aae46bc4a3eb2d8a4822d12d5186aa04eb` |
| Docs | CLEAN | `gates/gates-summary.txt` (11 gates rc 0); `anchor-check.txt`; privacy scans; `README.md`; both pages; PR body | R414-2 | `a66996aae46bc4a3eb2d8a4822d12d5186aa04eb` |

All five lenses are banked at the exact head. That head is the merge candidate's source tip, and the only commit after my round-1 head touches no RTL, test or tool.

## Prior public findings, resolved or retained

My own round-1 findings (R414-1 F1, F2 and F3) are resolved, as in the table above. My R414-1 S1 to S3 are optional; their status is under Findings.

I did not read the other reviewer's round-1 report (R415-1) before this verdict and ledger. Its items reached this pass through the manager's public item list: F1 as item 1, and S1 to S4 as items 4 to 7. Each is judged above as resolved or met. The section after the ledger records my reading of R415-1 after this verdict.

### After the verdict: R415-1 read and reconciled

R415-1 at `c721867b:review-evidence/b3-r1/reviews/R415-1/REPORT.md` holds F1 (MINOR, Docs) and S1 to S4. They are exactly the manager's items 1 and 4 to 7, and nothing else is open in it.

| R415-1 item | Status at `a66996aa` |
|---|---|
| F1, index rows | Resolved (item 1) |
| S1, whole-recording count | Taken: `:105-112` and `:158-161` |
| S2, identity chain | Taken: `:54-63` |
| S3, `nvm_pend` and the as-left slots | Taken: `:239-252`, including the point that `dirty=0` means the slots hold the as-left, unbound state |
| S4, frame 1,632's words | Taken in the packet |

Two details were checked against this head:

- **S1's acceptance-table wording.** It also names the acceptance-table line `:16` ("0 in the whole 4,551,624-frame recording"). That line sits in a measurement table the ruling freezes. The qualification is carried by the method text it points to, which satisfies the ruling.
- **S1's "778 transition frames".** That count is frame 45,587 plus the page's 777. It agrees with `grade.json` and with this head.

The PR's other comments are the manager's four review-start notices. PR reviews: none. This reading changes no finding, lens or verdict above.

## Real limits

- **Raw recordings.** The raw captures are not public: the DIN pcap, the DOUT capture and both USB captures. So:
  - frame 1,632's words are checked for consistency with the page and the published summary, not re-read from `usb-long.raw`;
  - the census figures come from the published `grade.json`.
- **Round-1 archive integrity.** `author/MANIFEST.sha256` lists four files whose published bytes differ from their listed hashes: `REVIEW-READY.md`, `REVIEW-READY.readback.md`, `gates/gates.txt` and `identity/controller-preflight.txt`.
  - This is round-1 packet state, unchanged by this commit.
  - `identity/controller-preflight.txt` is listed in `author/redaction.json`. I did not trace the other three in this round.
  - The round-2 files match both manifests.
- **No simulation.** The diff is documentation only, and no suite was needed or run. The scoped simulator was not used, so its identity was not checked.
- **Hosted checks at this head, read 2026-09-30T05:31Z and again at 05:34Z** (`receipts/hosted-check-runs.txt`):
  - Executed and passed: `changes`, `rtl-fast`, `docs-check-no-git`, `elaborate`, `bdd-conformance`, `wire-accountability` and `full-ci-gate`.
  - `docs-check` was still in progress, so it is not evidence here. My local docs gates cover its content.
  - Skipped for docs-only scope: `verilator-suites`, `verilator-lint`, `yosys-portability`, `yosys-elaboration`, their shard templates, and `Physical gPTP`. A skipped context is not evidence.
- **Physical proof.** Calibration, scope and continuity were NOT RUN. The bench figures are the operator's, not reviewer hardware proof.

## Pending manager duties

- Confirm hosted `docs-check` at `a66996aa` completes green, and own hosted and act acceptance.
- Build and validate the final current-dev candidate at the merge turn. Source base and live dev are both `ec0cc0c1df7d7ab3e25d973958f53f0074393d2c`.
- The merge also needs the second independent review's verdict at this head, and the full completion bar.
- Optionally:
  - take S1 and S2 in a later edit;
  - tie `d178f19a` to the `ec0cc0c1` build artifact (R414-1 S1).
- After merge, issue 617 needs a manual close. Acceptance 4 is met here, and 1 to 3 landed with PR #618; the PR says `Refs`, so the merge leaves it open.
- #451 stays open for the USB Audio FAIL, the playback direction, continuity, scope and the calibrated items.

## Receipts and scripts (listed in MANIFEST.sha256)

- `scripts/`: `mcasp_rx_rate.py` (round-1 script, byte-identical), `evidence_integrity.py`, `check_r2_claims.py`, `anchor_check.py` and `public_text_scan.py`.
- `receipts/`: `gates/*.txt` (eleven gate outputs and `gates-summary.txt`), `mcasp-rx-rate.txt`, `evidence-integrity.txt`, `r2-claims.txt`, `anchor-check.txt`, `public-text-scan.txt`, `author-r2-text-scan.txt`, `hosted-check-runs.txt` and `clone-integrity.txt`.
- **Clone state after the round:**
  - The clone is at the exact head; worktree, index and ignored files are clean.
  - The index tree equals the `HEAD` tree `e45645cd`, and the `ls-files -s` digest equals the `ls-tree` digest.
  - The gitlinks are unchanged: `external` efeb541a, `gptp-processor` 5dce647a, `protocol-processor` c951a9ff, `third_party/verilog-axis` 48ff7a7e.
  - One ignored `scripts/__pycache__/`, created by the gate run, was removed.

R414-2 FINISHED
