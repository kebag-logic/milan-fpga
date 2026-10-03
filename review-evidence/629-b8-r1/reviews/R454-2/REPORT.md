[R454] POSITIVE - exact head 77299b4fca1ec3268f0997c55a51d84955bbfeca

R454-2: internal, cleared-context independent review of issue #629 / PR #646 (bench lane B8). Docs only.

- **Head:** `77299b4fca1ec3268f0997c55a51d84955bbfeca`, tree `7e2d8d743998466358ae92abae1e62d372d33c62`.
- **Full diff:** `40714c1bd166c2a05f9607a861e8550c705d183a..77299b4f`, stacked on PR #644. It changes two Markdown files, `docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md` and `docs/findings/README.md`. No HDL, and no gitlink changes.
- **Round-2 delta:** `4fb5125a..77299b4f`, one commit. It touches only the lane B8 section (+109/-47; `receipts/round2.diff`).
- **Evidence:** branch `629-b8-review-evidence`, pinned at `36ee6d8adca255ad5228c4258a3186a5f0cbc574`, under `review-evidence/629-b8-r1/`. I also read the round-2 redaction record at `d6cc650f` (`author-r2/redaction.json`).

**Verdict basis.** No BLOCKER, MAJOR or MINOR finding is open, so all five lenses are clean at this head.

- **Round 1:** every round-1 finding of R454-1 and R455-1 is resolved on the page.
- **Residue:** one wording residue remains, RES-1. It is in the PR body, not the page.
- **Suggestions:** two optional ones, S1 and S2.
- **Verdicts:** no verdict changed. The 31 `Verdict`, `Result` and `Judgement` cells and verdict lines of the B8 section are identical at `4fb5125a` and at this head (`receipts/verdict-cells.txt`).

## Sources read, in order

1. AGENTS.md and CONTRIBUTING.md: section 2 (commits and the bench suite) and section 6 (wording and privacy).
2. `docs/README.md`.
3. Issue #629: its body and frozen acceptance, and the [A10] B8 assignment, ruling and round-2 assignment (issuecomment-5970760794, -5970994127, -5971696657). The round-2 assignment carries the manager's ruling on the capture decode. Also the [A521] REVIEW READY posts (-5971525043, -5971786989).
4. Authorities touched by the delta:
   - `docs/reference/REGISTER_MAP.md:1843-1868`: `SLIP_LB` at `0x8D4`, `SLIP_TDM` at `0x8D8`, and "a lane never fed counts nothing".
   - The `0x8DC` `RENDER_STAT` field table. Its fields are fill, prefill, converged and rails; there is no underrun field.
   - `hdl/ieee1722/aaf/KL_render_setpoint.sv:66,91,207,657`: `underruns_o` is a stage tap and is not mapped.
   - `docs/design/SAVED_STATE_FASTCONNECT.md:1055-1067` (9.1, `nvm_pend`) and `:1220`.
5. The PR #646 body and the diff history.
6. The published packet at `36ee6d8a`. I compared it with `5bad6a43`, the first publication, and with `d6cc650f`, the round-2 redaction record.
7. Only after my own pass: R454-1 (PR comment 5971692149) and R455-1 (5971688498).

## Independent checks at this head

All the receipts named here are in this packet. Every script can fail: `receipts/negative-controls.txt` holds five planted mutations, and each one is caught.

- **Hash rows** (`scripts/check_b8_rows.py`, `receipts/check-b8-rows.txt`). All 33 evidence rows equal their files at `36ee6d8a` in bytes and SHA-256, and equal `MANIFEST.json`'s `published_sha256`. All 13 raw rows are in `RAW-ARTIFACTS.json` at the pin. The three `identity*/identity-verdict.txt` files are equal.
- **`grade_b8.py` row** (page :1856). It shows 27,959 bytes and `77949fd1...`. That equals the pin's published file, and `MANIFEST.json` gives `original_sha256` `330c14cd...`, the "as run" prefix on the page.
  - The pinned `redaction.json` has 78 entries and no `grade_b8.py`, which the page discloses at :1828-1829.
  - The round-2 `redaction.json` (`d6cc650f`) adds exactly `tools/grade_b8.py` (`330c14cd` to `77949fd1`) and changes no other entry: 79 entries (`receipts/redaction-r2-check.txt`).
- **The masking commit** (`36ee6d8a`). It changes one line of `tools/grade_b8.py` and `MANIFEST.json`, and no other packet file. In the manifest the only changed entry is `grade_b8.py`; the other new entries are the R455-1 archive. `5bad6a43` is an ancestor, so nothing was force-pushed.
  - Exactly eight `restore/controller-*` and `restore/host-*` records are `path_redacted`, as the page says (:1821-1824).
- **The other three masked tools.** For `run_b8.py`, `b8_tone.py` and `tone_play_b8.sh`, `MANIFEST.json` has original equal to published. The pinned `redaction.json` holds their as-run hashes, and the `run_b8.py` prefix `efd07d51` matches the page.
- **Privacy, value-blind** (`scripts/privacy_scan.py`, `receipts/privacy-scan.txt`, `privacy-format-tokens.txt`, `privacy-literal-and-decode.txt`, `privacy-selfscan.txt`). No value is written anywhere in this packet.
  - The channel-count phrase is taken from the line `36ee6d8a` removed. It has 0 hits in the page and in the packets at `36ee6d8a` and `d6cc650f`. The positive control (the pre-mask `grade_b8.py`) is caught.
  - Sample-format-name shapes: the packet has one distinct token. It is the SoC-side TDM token the page already carried at the base (B6 :118), and it appears only in the SoC and McASP0 logs and tools. The B8 section has none.
  - The only capture-and-channel phrases are McASP0's eight-channel TDM recording, which the page states.
  - No retained tool states the masked integer beside a channel word.
  - The decode constructs stay readable (`grade_b8.py` 5, `run_b8.py` 8, `b6_thdn.py` 4), as the ruling requires.
  - The `cap-all.raw` sizes are withheld in `RAW-ARTIFACTS.json`, with a digit-free reason, and the `full-snippet` events carry frames, not bytes.
  - The B8 section never uses the word "layout".
- **Figures added or changed in round 2** (`scripts/derive_round2_figures.py`, `receipts/derive-round2-figures.txt`).
  - **CRF window.** The events span 420.026 s. 19,261,920 frames were captured (401.29 s) and `capture_lost_frames` is 899,009 (18.729 s); the two sum to 420.02 s.
  - **Stall clusters.** Read gaps 4.12, 4.37 and 9.77 s. They lost 18.69 s. They start at 270.9, 284.1 and 285.5 s on the captured basis, and at 270.9, 288.7 and 294.7 s counting earlier losses.
  - **Signature.** Clusters 1 and 3 are off it. Cluster 2 is on it: one skip of 2,172 frames (48 n + 12) and a -23,776-frame repeat. All nine clusters pass the 1 ms + 2 % rule.
  - **Polls.** The window has 798 polls; poll 618 missed a word, leaving 797.
  - **#645 timeline.** The binds end 2.006 s before the set, and prefill clears at -1.900 to -1.399 s. The two slips fall at -1.399 to -0.899 and -0.899 to -0.068 s, with no skips. The last ends 1.939 s after the binds; the two are at most 1.331 s apart. The ACQUIRE slip is at 2.134 to 2.634 s, and the post-LOCKED slip 2.015 to 3.016 s after the first LOCKED read. A steady 5.92 ppm offset slips once every 3.519 s.
  - **`pend`.** It reads 1 at every NVM read before the cycle (identity, resume, SW, CRFLL, as-found, saved). It reads 0 after the boot, 1 after the restore's first commit and 0 at the end (`restore/dut-end2.txt`).
  - **Post-boot `SLIP_LB`.** 6 at all three post-boot polls and at the end read (`receipts/pc-slip-lb.txt`).
  - **Tone proof.** The render-path claim matches `summary/proof/proof.json`: channels 0 to 3 carry 239,680 to 260,360 non-zero samples, and channels 4 to 7 carry 0.
- **Links** (`scripts/check_fragments.py`, `receipts/fragments.txt`). All 34 in-page and relative fragment links in the section resolve. The four issue-comment links point at comments that exist on #629.
- **Gates at this head**, in a private environment with the pinned Markdown lock (`receipts/gates/summary.txt`). All 12 are rc 0:
  - `docs_check.py`, `check_doc_style.py`, `gen_toc.py --check` and `--verify-anchors`;
  - `check_em_dash.py --base 40714c1b`, `check_doc_paths.py`;
  - `ci_scope.py --selftest`, `check_baremetal_only.py --check` and `--selftest`, `check_feature_status.py --self-test`;
  - `git diff --check` from `40714c1b` and from `4fb5125a`.

## Round-1 findings, judged at this head

| Round-1 item | Status | Evidence at `77299b4f` |
|---|---|---|
| R454-1 F1 (MAJOR): capture channel count in `grade_b8.py` | RESOLVED | Masked at `36ee6d8a`. The page row (:1856) carries the retained hash with "masked; as run `330c14cd...`". The as-run hash is in `MANIFEST.json` at the pin and in the round-2 `redaction.json`. The value-blind scan finds no count |
| R454-1 F2 (MINOR): layout claimed hidden while the decode is readable | RESOLVED | The page follows the ruling (5971696657) at :1802-1806: the format name and channel count are masked, and the decode (byte width and order) is not. "Layout" no longer appears in the section |
| R454-1 F3 = R455-1 F1 (MINOR): 19.0 s | RESOLVED | :1621-1635 and :1758-1760 give 18.73 s and 899,009 frames with their basis, and the 18.69 s for the stall clusters. Both time bases are named. Two clusters are off the signature and the third is on it, with its repeat. The PR body's row matches |
| R454-1 F4 = R455-1 F2 (MINOR): where the evidence lives | RESOLVED | :1306-1310 and :1811-1832 give the branch, the full pin, the label-to-path mapping, `MANIFEST.json`'s two hashes, the first publication at `5bad6a43`, and the eight path-masked records. They also say where each evidence and raw row is recorded. The PR body's Evidence paragraph matches |
| R455-1 F3 (MINOR): a cause the data excludes | RESOLVED | :1584-1600 give the two slips, their intervals and separation, no skips, and the 3.52 s steady-offset period. They are "recorded here and not analysed; this lane gives no cause". The remaining "the servo locks frequency only (#632)" states the design's declaration. It is not offered as the slip's mechanism |
| R455-1 F4 (MINOR): privacy, the channel count | RESOLVED | Same as R454-1 F1 |
| R454-1 R1 (`0x8D8`) | RESOLVED | :1421-1422 |
| R454-1 R2 (raw-record sentence) | RESOLVED | :1770-1775, verbatim |
| R454-1 R3 ("no state-changing command") | RESOLVED on the page; carried for the PR body | Page :1303 and :1684. R3 named only the page lines. The PR body's item-4 row still says "with no command sent", which is RES-1 below |
| R454-1 S1, S2, S4; R455-1 S1, S2, S3 | Taken | :1535-1542 and :1563-1564; :1721-1728; :1618-1619; :1679 and :1700-1701; :1384-1387; :1761-1762 |
| R454-1 S3 (container interface name in evidence) | Not taken (optional) | It is on the evidence branch, outside this diff. It stays a SUGGESTION and affects no lens |

## Findings

No BLOCKER, MAJOR or MINOR finding.

```text
[R454] RESIDUE Docs - PR #646 body, "What happened" table, row "4. Saved selection across a power cycle" - RES-1: the PR body keeps "with no command sent"
Requirement/evidence: R454-1 R3, applied on the page at :1303 and :1684 ("no state-changing
  command sent"). The PR body's row still reads "the servo read LOCKED with no command sent",
  while GET_CLOCK_SOURCE, the format, the RX state, the counters and the NVM were read first.
Impact: wording only. It changes no measurement, figure, verdict or privacy statement.
Required outcome (exact fix): in that row, replace "the servo read LOCKED with no command sent"
  with "the servo read LOCKED with no state-changing command sent".
Verification: the PR body row reads as the page's :1303.
```

## Suggestions (optional, no lens effect)

- **S1, :1793-1796 and :1826-1829.** At the pin, `redaction.json` holds 78 entries and no `grade_b8.py`. The page's "79 packet files" and "the lane packet's `redaction.json` records both of its hashes from round 2 on" are true of the round-2 record. That record is published, at `629-b8-review-evidence` `d6cc650f`, `review-evidence/629-b8-r1/author-r2/redaction.json`, but the page does not point to it. Naming that path would let a cold reader check the 79 directly. The as-run hash is already checkable at the pin through `MANIFEST.json`, and the page discloses the 78/79 difference, so no claim is false.
- **S2, :1823-1824.** "`MANIFEST.json` alone records their two hashes" holds for the original-to-published pair. For the four `restore/host-*.txt`, though, the pinned `redaction.json` also records the original as its retained hash. "`MANIFEST.json` alone records their published hash" would be exact.

## Reviewer-owned ledger

| Lens | Status | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Page :1267-1868 (delta :1300-1832) against #629's frozen acceptance, the B8 assignment and ruling, the round-2 assignment (5971696657) and SAVED_STATE_FASTCONNECT 9.1. The acceptance table :1732-1745 is unchanged and "Refs #629" is correct. The `pend` row and the #645 paragraph are re-derived (`receipts/derive-round2-figures.txt`). The verdict cells are identical to round 1 (`receipts/verdict-cells.txt`) | R454-2 | 77299b4fca1ec3268f0997c55a51d84955bbfeca (evidence 36ee6d8a) |
| RTL | CLEAN | No HDL in the diff (`git diff --stat`, gitlinks unchanged; `receipts/clone-integrity.txt`). The delta's RTL-facing claims checked: REGISTER_MAP.md:1867-1868 (`0x8D8`; an unfed lane counts nothing), the `0x8DC` field table (no underrun field), KL_render_setpoint.sv:66,91,207,657 (underrun re-enters prefill; `underruns_o` unmapped), SAVED_STATE_FASTCONNECT.md:1067 (`nvm_pend`) | R454-2 | 77299b4fca1ec3268f0997c55a51d84955bbfeca |
| Robustness | CLEAN | Capture-stall loss and cluster signatures (`summary/crfll/grade.json`, `runs/crfll/events.jsonl`, `lockloss.json`); #645 pre-set and post-LOCKED slips (`summary/sw/switches.json`); post-boot dups (`runs/pc/poll-post-relock-noaction.jsonl`, `restore/dut-end2.txt`); NVM `pend` through the cycle (`runs/pc/events.jsonl`, the NVM status lines) | R454-2 | 77299b4fca1ec3268f0997c55a51d84955bbfeca (evidence 36ee6d8a) |
| Tests | CLEAN | The evidence claims the page certifies: 33 evidence and 13 raw rows (`receipts/check-b8-rows.txt`); the masking commit's scope and the redaction records (`receipts/redaction-r2-check.txt`); the tone-proof render claim (`summary/proof/proof.json`). Each checker is shown able to fail (`receipts/negative-controls.txt`). 12 gates rc 0 (`receipts/gates/`) | R454-2 | 77299b4fca1ec3268f0997c55a51d84955bbfeca (evidence 36ee6d8a) |
| Docs | CLEAN (RES-1 carried; S1, S2 optional) | The section and its delta, the README row, the PR body, the masking statement against the ruling, the evidence pointer, links (`receipts/fragments.txt`), docs gates, and value-blind privacy over the page and the packets at `36ee6d8a` and `d6cc650f` (`receipts/privacy-*.txt`) | R454-2 | 77299b4fca1ec3268f0997c55a51d84955bbfeca (evidence 36ee6d8a) |

```text
[R454] PASS Conformance - docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md:1300-1832 at 77299b4f; evidence 36ee6d8a summary/sw/switches.json, runs/pc/events.jsonl - round-2 wording and figures change no verdict (receipts/verdict-cells.txt); pend row matches SAVED_STATE_FASTCONNECT 9.1; #645 data stated without a cause; Refs #629 per the frozen acceptance
[R454] PASS RTL - docs/reference/REGISTER_MAP.md:1867-1868 and the 0x8DC table, hdl/ieee1722/aaf/KL_render_setpoint.sv:66,91,207,657 - 0x8D8, the unfed-lane rule and the unexposed underrun count are as the page now states; no HDL in the diff
[R454] PASS Robustness - evidence 36ee6d8a summary/crfll/grade.json, summary/sw/switches.json, runs/pc/* - stall loss 18.73 s and clusters 18.69 s, slip intervals, post-boot dups and pend re-derived exactly
[R454] PASS Tests - receipts/check-b8-rows.txt, receipts/negative-controls.txt, receipts/redaction-r2-check.txt - 46 rows hold at the pin; the checkers fail on planted mutations
[R454] PASS Docs - docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md:1306-1310,1768-1832; receipts/gates/summary.txt; receipts/privacy-scan.txt - masking statement follows 5971696657, pointer complete, 12 gates rc 0, no private value; RES-1 is PR-body wording only
```

## Real limits

- **Raw bench files are not published, by design.** I re-derived from the lane's published summaries, event logs and status records. I did not re-run any grade from raw captures or polls.
- **No hardware, no banks.** I ran no hardware, no full parent, PP, gPTP, Yosys or builder bank, no act and no simulation. The diff contains no RTL.
- **Physical calibration NOT RUN.** Printed precision is not calibrated accuracy. Field and hosted skips are not hardware proof.
- **Hosted contexts at the exact head, read at review time** (`receipts/hosted-checks.txt`):
  - success: `rtl-fast`, `changes`, `elaborate`, `bdd-conformance`, `wire-accountability`, `docs-check-no-git`, `full-ci-gate`;
  - in progress: `docs-check`;
  - skipped, not executed: `verilator-suites`, `yosys-portability`, the Verilator and Yosys shards, `verilator-lint`, `yosys-elaboration`, "Physical gPTP".
  The combined commit status was pending. The manager owns hosted and act acceptance.
- **The privacy scan is value-blind and pattern-based.** It covers the masked phrase in a channel context, format-name shapes and capture-channel phrasing. Every structural hit was read without writing a value.
- **The clone was restored after the gates.** I removed the `scripts/__pycache__` the gate runs created. The status then has 0 entries, ignored files included; the index tree equals `7e2d8d74...`; and the four submodule gitlinks are unchanged, with clean checkouts (`receipts/clone-integrity.txt`).

## Pending manager duties

1. Carry RES-1 to the residue checklist.
2. Carry the INTERNAL-to-AAF data (page :1567-1606) and the untimed post-boot dups (:1721-1728) to #645. The lane posts nothing there.
3. Lane B7's published `grade_b7.py` states the same capture channel count. It is outside this diff and needs its own masking.
4. Evidence-side wording, outside this diff: at the pin, `RAW-ARTIFACTS.json`'s note and the `cap-all.raw` `bytes_withheld` reasons still say the size "would state the capture's layout". The page no longer claims that, so whether to align the evidence is the manager's choice.
5. Merge PR #644 first, since this branch stacks on `40714c1b`. Then build and validate the current-dev candidate against live dev `546437243e87eb5a78783a9e3cd5d1badcc3423e`.
6. Hosted acceptance at the exact head: `docs-check` was still in progress.
7. Merging needs the second independent positive review (R455-2) and maintainer authorization.

R454-2 FINISHED
