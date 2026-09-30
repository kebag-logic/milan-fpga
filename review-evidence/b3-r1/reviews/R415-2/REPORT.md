[R415] POSITIVE - exact head a66996aae46bc4a3eb2d8a4822d12d5186aa04eb

# R415-2: external review of PR #624 (#617 acceptance 4, #451 USB Audio capture), round 2

- **Head.** `a66996aae46bc4a3eb2d8a4822d12d5186aa04eb`, tree `e45645cd5599cbfad06d0dc44e11c2a35caee56e`.
  - It is one commit on my round-1 head `6dfa64a7`, with a one-line subject, no body and no trailers.
  - Against dev `ec0cc0c1df7d7ab3e25d973958f53f0074393d2c` the PR is documentation only: the two new findings pages and `docs/findings/README.md`.
  - The round-2 commit changes 3 files, +51 -14. No gitlink, RTL, test or tooling change.
- **Context.** The review ran in a cleared context. I rebuilt it from these public sources:
  - AGENTS.md and CONTRIBUTING.md;
  - the #617 body and acceptance;
  - the round-2 assignment and index ruling (#617 comment 5904487454);
  - the #495 residue record (5904489402);
  - REGISTER_MAP `0x920` and SAVED_STATE_SNAPSHOT_OWNERSHIP sections 6.1 and 11;
  - the #606 page's identity readback;
  - `git diff 6dfa64a7..a66996aa` and `ec0cc0c1..a66996aa`;
  - the public evidence at `b3-review-evidence` tip `c721867b7ec772b0bfc928962979f3b32c4bb0d8` (`review-evidence/b3-r1/author`, `author-r2` and `MANIFEST.json`).
- **Independence.**
  - I wrote my verdict and ledger (`receipts/independent-verdict.txt`, 05:32:06Z) before I read any other reviewer's report.
  - After that I read R414-1's public findings, and I resolve them below.
  - I read no private author material, and I did not open `review-evidence/b3-r1/reviews/`.
- **Verdict: POSITIVE.**
  - All five lenses are clean at this head.
  - Every round-1 finding and suggestion of mine is resolved, and so are R414-1's three MINOR findings.
  - Two new SUGGESTIONs (N1, N2) are optional.

## Round-1 items against this head

| Item | Result | Evidence at `a66996aa` |
|---|---|---|
| R415-1 F1 MINOR (index) | **RESOLVED** | `docs/findings/README.md:12-13` has one row per new page, directly after the first-light row they follow up, in file-name order. That is the placement PR #622 used for 606 and 608 after the 75 row. `:11`: the first-light row keeps its old text as an exact prefix. Its State adds the `ec0cc0c1` DIN re-run (0 torn, linked) and the USB Audio capture FAIL (linked), as ruled. 11 of 12 old rows are byte-unchanged. Both pages are now reachable from the index (`receipts/findings-index.txt`). The four older unindexed pages are recorded on #495 (5904489402), per the ruling |
| R414-1 F2 MINOR (McASP0 rate) | **RESOLVED** | I re-derived the rate with my own `scripts/mcasp_rx_rate.py` over the four published status logs (input hashes equal the author's receipt). Chan1 Edge deltas are 18,942 and 18,957. The consistent bracket, same uptime read to same uptime read, is 75.78 s and 75.83 s, giving 249.960 and 249.993 periods/s (47,992.4 and 47,998.7 frames/s). The page states this at `451_USB_AUDIO_CAPTURE.md:126-127,129-133`. The old 250.7 is reproduced only by the short cross-pairing (75.57 s); the long pairing gives 249.3. Restarts: Level delta 5 and 5. The packet `HANDOFF.md` step 5 is corrected in the published overlay `author-r2/packet/HANDOFF.md:30`, with a deviation line at `:62` (`receipts/mcasp-rx-rate.txt`) |
| R414-1 F3 MINOR (packet locator) | **RESOLVED** | `617_DIN_FRAME_COHERENCE_BENCH.md:275-278` and `451_USB_AUDIO_CAPTURE.md:216-219` name `review-evidence/b3-r1/author/` on `b3-review-evidence`. All 6 tool-hash rows on the two pages match the files there. 4 of the 5 raw-artifact rows are in `RAW-ARTIFACTS.json` with equal size and hash (135 entries); the fifth is N2. The four `author/MANIFEST.sha256` differences are exactly the archiver's recorded path redactions: original hash equals the manifest, published hash equals the file (`receipts/locator-check.txt`, `manifest-redaction-check.txt`) |
| R415-1 S1 (torn-count scope) | **RESOLVED** | `617:105-112` states that the rule reads only pattern words, so the whole-recording count covers frames that carry them, which are the region's. `:158-167` names the edge frames as graded by inspection. Re-derived from `grade.json`: the region is 45,588 to 3,405,623. Outside the region, 1,191,588 frames hold 9,532,704 words (`ffffff00` 9,526,486, other 1, zero 6,217), and none is a pattern word. The edge frames 45,587 and 3,405,624 match the page, and so does the 777-frame tail (`receipts/edge-frames.txt`). Wording nit: N1 |
| R415-1 S2 (identity chain) | **RESOLVED** | `617:54-58`: VERSION `0x00020060`, AEM CRC32 `93742dd2`, entity `020000fffe000001` and ROM CRC32 `acad92b9` equal the #606 page's `13eda870` readback (`606_FIRST_BIND_MEASUREMENT.md:48-52`). Only the payload CRC differs (`d178f19a` against `d84bce7b`). `:60-63`: the build's own payload CRC is not in the packet. Confirmed: `author/identity/` holds only the console readback `d178f19a` |
| R415-1 S3 (`nvm_pend`) | **RESOLVED** | `617:244-252`. One wire, confirmed against the authority and the RTL. REGISTER_MAP `0x93C` says `[22]` `nvm_pend` is "the same wire `PP_STAT[11]` carries". In the RTL, `KL_nvm_backend.sv:587` puts `pend_w` at bit 22 of the status word, and `:796` drives `nvm_pend_o = pend_w`. That signal passes through `KL_pp_shadow.sv:1031` and `milan_datapath.sv:7720,2747` to `milan_csr.sv:2225` (`PP_STAT[11]`). The consequence is correct: section 11 row `0x60`-`0x7F` says "nvm_pend 1 from the first actual write until reset; never durable, and never written", and section 6.1 gives the durable reading as (backed 1, dirty 0, stale 0) AND pend 0. The end state is `restore/dut-end.txt:9-10`: `VD_OK` seq 235/236, `dirty=0`, `pend=1`, commits 6 |
| R415-1 S4 (frame 1,632) | **RESOLVED** | `author-r2/packet/summary/usb-long-frame-1632.json` and `summary.json` publish `016ec820` through `086ec8c0`: one ordinal `0x6ec8`, tags 1 to 8 in order, low bytes `0x20` to `0xc0` rising, all below one 24-bit LSB. That matches `451:140-143`, and `first_non_silent_frame` 1632 equals the round-1 grade summary. I drove the published `usb_frame_words.py` (`0f4bb562...`) on a synthetic capture: 9 of 9 checks pass. It returns the published words and split, the byte offset and previous-silent flag, and it refuses a wrong SHA-256 and an out-of-range frame. It reports a rotated frame as not in order (`receipts/frame-words-probe.txt`) |
| R414-1 S1, S2, S3 (suggestions) | Retained as optional | S1: the build's payload CRC is still unpublished, a manager duty. S2: the `nvm_pend` part is done; the bind-pair attribution of the six commits and the inherited SLIP and RAIL counters are not stated. S3 (attribution wording) was not assigned. None affects coverage |

## Frozen content and hygiene

- **Measurement tables.** `receipts/table-identity.txt` compares tables block by block, `6dfa64a7` against `a66996aa`:
  - `617_DIN_FRAME_COHERENCE_BENCH.md`: 12 of 12 tables are byte-identical, including the acceptance table (`:16` still reads "0 in the whole 4,551,624-frame recording", qualified by the method paragraph).
  - `451_USB_AUDIO_CAPTURE.md`: 7 of 8 tables are byte-identical. The bridge-side table differs in exactly one character in each of two rows (`7` to `0`), which is the rate correction item 2 requires.
- **Rendering.** All 21 tables render with a constant column count in source and render. The check includes a negative control, and it replaces my round-1 check, which could not fail (`receipts/table-cells.txt`).
- **Links.** The 9 relative links added in round 2 resolve, anchors included (`receipts/anchor-check.txt`).
- **Privacy.** The 51 added lines contain no IPv4 or MAC address, no absolute path, no email, no agent tool or model name and no lane-private packet name (`receipts/privacy-scan.txt`).
- **Keywords.** The PR body says `Refs #617`, `Refs #451` only, with no closing keyword. `closingIssuesReferences` is empty, and the PR head equals the reviewed head.
- **Docs gates, rc 0 at the head** (`receipts/gates/`):
  - Pinned Markdown environment (requirements SHA-256 `40cdefe0...`):
    - docs_check: 0 findings, 181 files;
    - check_doc_style;
    - gen_toc `--check`;
    - check_em_dash `--base ec0cc0c1`: 0 findings, 512 added lines;
    - check_doc_paths: 860 paths;
    - check_feature_status `--self-test`;
    - ci_scope `--selftest`.
  - check_baremetal_only `--check` ran under the system interpreter. It needs a YAML library that the pinned Markdown environment lacks, and the first attempt was an environment refusal, not a finding.
  - `git diff --check` against `ec0cc0c1` and against `6dfa64a7`.

## Findings

**N1 SUGGESTION (Docs):** `docs/findings/617_DIN_FRAME_COHERENCE_BENCH.md:159`.
- **Evidence.** The line reads "The edge frames, 45,587 before the region and the 777 transition frames after it". It is parallel to a count ("the 777 transition frames"), so "45,587" reads as a count. Zero-based, 45,588 frames precede the region (`receipts/edge-frames.txt`). The next bullet ("Frame 45,587, just before the region") shows that the frame index is meant.
- **Impact.** A reader can take an off-by-one count from the qualifying sentence. No figure is wrong.
- **Suggested outcome.** Write "frame 45,587, just before the region, and the 777 transition frames after it".
- **Verification.** Reading the page.

**N2 SUGGESTION (Docs):** `617_DIN_FRAME_COHERENCE_BENCH.md:275-278` and `451_USB_AUDIO_CAPTURE.md:216-219`.
- **Evidence.**
  - The locator names only `author/`, as item 3 prescribed. The round-2 corrections sit in the sibling `review-evidence/b3-r1/author-r2/packet/`: the rate-corrected HANDOFF, the frame-1,632 words and the rate receipt. At the named path, `author/HANDOFF.md:30` still reads 250.7 periods/s.
  - The sentence "`RAW-ARTIFACTS.json` indexes every raw file" is narrower than the artifact table above it. The SoC-built DIN pattern period (2,097,152 B, `b6a92e97...`) is not in `RAW-ARTIFACTS.json`; its size and hash are in `author/runs/din-long/events.jsonl` and `din-long-lock.txt` (`receipts/locator-check.txt`).
- **Impact.** A cold reader who follows the locator meets the superseded rate and does not find the S4 words. The page's own figures are unaffected.
- **Suggested outcome.** Name the round-2 overlay beside `author/`, and say where the pattern period's identity is recorded. A manager-side note on the evidence branch would also do.
- **Verification.** Open the named paths.

No BLOCKER, MAJOR or MINOR is open.

## Ledger (reviewer-owned)

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #617 acceptance 4 unchanged in substance: the tables are byte-identical to the round that confirmed it (`table-identity.txt`). Assignment 5904487454 items 1 to 7, each checked at its `path:line` above. Index ruling: rows, order and first-light State (`findings-index.txt`). Identity items against `606_FIRST_BIND_MEASUREMENT.md:48-52` and `author/identity/`. PR body: Refs only, `closingIssuesReferences` empty | R415-2 | `a66996aae46bc4a3eb2d8a4822d12d5186aa04eb` |
| RTL | CLEAN | No RTL, gitlink or tooling in the diff (`git diff --stat`, `clone-integrity.txt`). The one new RTL claim (one wire) was traced: `KL_nvm_backend.sv:587,790,796`, `KL_pp_shadow.sv:958,1024,1031`, `milan_datapath.sv:2747,7720`, `milan_csr.sv:670,2225`, and REGISTER_MAP `0x93C`/`0x924` | R415-2 | `a66996aae46bc4a3eb2d8a4822d12d5186aa04eb` |
| Robustness | CLEAN | The rate under all four uptime pairings (consistent 250.0 against a cross-pair spread of 249.3 to 250.7, `mcasp-rx-rate.txt`). Region edges, the outside-region census and the 777-frame tail (`edge-frames.txt`). The next-lane NVM consequence against section 6.1's durable reading, section 11 row `0x60`-`0x7F`, and `restore/dut-start.txt:10` / `dut-end.txt:10` | R415-2 | `a66996aae46bc4a3eb2d8a4822d12d5186aa04eb` |
| Tests | CLEAN | The executable evidence. My rate script reproduces the page. The published `usb_frame_words.py` passes a 9-check synthetic probe with negative controls (`frame-words-probe.txt`). Tool and raw hashes and both manifests were checked against the published packet (`locator-check.txt`, `manifest-redaction-check.txt`). The table-cell check now has a negative control that fires. Hosted contexts at the head: the executed ones succeeded, except `docs-check`, which was still in progress at 05:33Z (mine passed locally); `verilator-*`, `yosys-*`, the shards and Physical gPTP were skipped by the docs-only selector, and a skip is not evidence (`hosted-check-runs.txt`) | R415-2 | `a66996aae46bc4a3eb2d8a4822d12d5186aa04eb` |
| Docs | CLEAN (N1 and N2 are suggestions) | Every added line of `6dfa64a7..a66996aa` read against its source. The findings index and inbound links. Anchors (`anchor-check.txt`). Ten docs gates (`gates/gates-summary.txt`). Rendered table cells. The privacy scan. The PR body | R415-2 | `a66996aae46bc4a3eb2d8a4822d12d5186aa04eb` |

## Real limits

- **Raw captures.** They are not public, so I re-read none of their bytes. The frame-1,632 words rest on the published tool, which checks the capture's SHA-256 against the page. I probed that tool on synthetic data, not on the raw file.
- **Manager banks.** I did not find the manager's source, static, builder and native bank receipts in the named evidence tree at `c721867b`, which holds only `author`, `author-r2`, `reviews` and `MANIFEST.json`. I rely on the brief for them. They are not needed for a documentation-only diff.
- **Simulator.** The scoped simulator path named for this round does not exist on this host (`receipts/simulator-note.txt`). No simulation ran, and none was needed: no RTL changed.
- **Not run.** Physical calibration, the continuity check and scope measurements are NOT RUN. A field skip is not hardware proof.
- **Clone.** The clone was verified at the exact head afterwards (`receipts/clone-integrity.txt`): tree and index `e45645cd`, `ls-files -s` digest equal to the HEAD tree digest, no untracked or ignored file, and the gitlinks unchanged (`external` efeb541a, `gptp-processor` 5dce647a, `protocol-processor` c951a9ff, `third_party/verilog-axis` 48ff7a7e).

## Pending manager duties

- Hosted acceptance at this head, including the in-progress `docs-check` context. Local-replica acceptance.
- The final current-dev candidate build at the merge turn. Source base and live dev are both `ec0cc0c1`.
- Merge only with maintainer authorization and the second independent positive review.
- Optionally act on N1 and N2, and on R414-1's retained suggestions. Publish the `ec0cc0c1` build's payload CRC32 when it is available.
- After landing, close #617 by hand, since the PR says Refs only. Acceptance 1 to 3 landed with PR #618, and 4 is shown here. Keep #451 open: the USB-path FAIL, the playback direction, continuity, scope and the calibrated items.
- The four older unindexed findings pages stay on #495.

R415-2 FINISHED
