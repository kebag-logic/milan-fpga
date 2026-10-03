[R455] POSITIVE - exact head 77299b4fca1ec3268f0997c55a51d84955bbfeca

Round R455-2: external independent review of PR #646 (issue #629, bench lane B8), docs only, in a cleared context.

- Head `77299b4fca1ec3268f0997c55a51d84955bbfeca`, tree `7e2d8d743998466358ae92abae1e62d372d33c62`.
- Full lane diff `40714c1bd166c2a05f9607a861e8550c705d183a..77299b4f`, stacked on PR #644: `docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md` and one row of `docs/findings/README.md`. No gitlink changed.
- Round-2 delta `4fb5125a..77299b4f`: one commit, one file, +109/-47, all inside the section "Dev bbf704ec, 2026-10-03: lane B8".
- Evidence: branch `629-b8-review-evidence`, pinned at `36ee6d8adca255ad5228c4258a3186a5f0cbc574`, under `review-evidence/629-b8-r1/`. The first publication `5bad6a43` was compared against it.

**Verdict basis.** No BLOCKER, MAJOR, MINOR or RESIDUE finding is open at this head, and all five lenses are clean. Every round-1 finding is resolved, and none got worse. Every figure the round adds re-derives from the published packet at the pin. No item verdict changed. The page still has item 1 NOT RUN, item 2 PASS for AAF to CRF and CRF to AAF, #645 repeated for INTERNAL to AAF, item 3 as declared, and item 4 PASS.

## Sources, in order

1. `AGENTS.md`, `CONTRIBUTING.md` (sections 4 to 6, and the 6.1 em-dash rule) and `docs/README.md`.
2. Issue #629 round-2 assignment and manager ruling (issuecomment-5971696657), and the review-start notice (PR #646 issuecomment-5971812964).
3. Authorities the delta cites:
   - `docs/reference/REGISTER_MAP.md` 0x8D4/0x8D8 (:1843-1868) and 0x8DC (:2006-2053);
   - `docs/design/SAVED_STATE_FASTCONNECT.md` 9.1 (:1055-1090);
   - `hdl/ieee1722/aaf/KL_render_setpoint.sv` (:60-95, :550-668);
   - the page's own B7 section "the DUT's INTERNAL media clock" (:1038-1059).
4. The diffs `4fb5125a..77299b4f` and `40714c1bd..77299b4f`, and the commit history.
5. Published evidence at `36ee6d8a` and `5bad6a43`, and the round-2 archive `d6cc650f` (`author-r2/`), read for privacy and the 79-file count only.
6. Only after the independent pass: the round-1 findings R455-1 (5971688498) and R454-1 (5971692149), and the PR body at this head.

## Independent re-derivation at the pin

- **Hash rows.** All 46 rows of "B8: artifact hashes" verify at `36ee6d8a` (`receipts/hash_rows_36ee6d8a.txt`, `scripts/verify_hash_rows.py`).
  - Each of the 33 evidence rows matches the file under `author/` in size and SHA-256, and equals `MANIFEST.json`'s `published_sha256`.
  - The three identity verdicts are byte-equal.
  - Each of the 13 raw rows appears as a size and hash pair in `RAW-ARTIFACTS.json`.
  - `grade_b8.py`: 27,959 bytes, `77949fd1...`. Its as-run `330c14cd...` is `MANIFEST.json`'s `original_sha256`, with the note "R455-1 F4: capture channel count masked (top-only)". The as-run hashes of `run_b8.py`, `b8_tone.py` and `tone_play_b8.sh` are in `redaction.json`.
  - Probe: the same check run against `5bad6a43` fails on the `grade_b8.py` row (size, SHA and manifest), so the check can fail (`receipts/probe_hash_rows_vs_5bad6a43.txt`).
- **Publication claims.**
  - `36ee6d8a`'s parent is `23d35c4b`, so the mask went on top with no force-push.
  - The only `author/` file it changed is `grade_b8.py`: 252 of 252 author manifest entries, one changed.
  - Exactly eight `restore/controller-*` and `restore/host-*` records carry publication-time path redaction.
  - The published `redaction.json` has 78 entries and does not list `grade_b8.py`. The round-2 lane copy at `d6cc650f` (`author-r2/redaction.json`) has 79 and lists `330c14cd...` and `77949fd1...`. This matches the page (:1795, :1826-1831).
  - The SW and CRFLL `events.jsonl` hold their capture files' hashes. The proof recording, the full grades and `boot-console.jsonl` are hashed only in `RAW-ARTIFACTS.json`. Both records withhold `cap-all.raw`'s size.
- **CRF window** (`receipts/rederive_round2.txt`, `scripts/rederive_round2.py`).
  - Polls: 798 in the segment, 797 in `lockloss.json`, and `polls_missing_a_word` = [618].
  - Timing: the events' window spans 420.03 s. 19,261,920 frames were captured (401.29 s) and `capture_lost_frames` is 899,009 (18.73 s). Together they make 420.02 s.
  - Stall clusters 1 to 3 follow read gaps of 4.12, 4.37 and 9.77 s and lost 18.69 s. They start at 270.9, 284.1 and 285.5 s of captured audio, or 270.9, 288.7 and 294.7 s counting the frames lost before each.
  - Signatures: clusters 1 and 3 are off the 48 n + 12 signature. Cluster 2 is on it, with steps [2172, -23776].
- **#645.** The binds end 2.006 s before the set.
  - Prefill was left at -1.90 to -1.40 s.
  - `SLIP_LB` read 416 at -1.40 to -0.90 s and 418 at -0.90 to -0.07 s, with skips 0. The two slips are at most 1.33 s apart, within 1.94 s of the binds' end.
  - At 5.92 ppm a frame slips every 3.52 s. B7's table gives +5.92 ppm at :1048.
  - The page now states these as data and gives no cause (:1584-1594).
- **`pend`.**
  - Every NVM read before the cycle reads `pend=1`: the two PC reads and nine reads from the identity, restore and run files. `dirty=0` and `commit_busy=0` at the saved read.
  - After the cycle, `pend` reads 0 after the boot, 1 after the restore's first commit, and 0 in the post-boot identity and at the end.
  - `nvm_pend` matches `SAVED_STATE_FASTCONNECT.md:1067`, and the anchor `#91-the-bits` resolves.
- **Six post-boot dups.** `SLIP_LB` reads `0x00000006` at all three post-boot polls and at the end (`restore/dut-end2.txt`), and `RENDER_STAT` rails read 0. REGISTER_MAP :1867 supports "a lane never fed counts nothing".
- **Render path live.** `proof.json`: channels 0 to 3 are non-zero (range -2 to +1 LSB), and channels 4 to 7 have 0 non-zero words.
- **RTL claims.**
  - `SLIP_TDM` is `0x8D8` (REGISTER_MAP :1868).
  - An underrun (`pop_dry_w`, :567-572) sets prefill and clears converged, as a short-queue recentre does (:591-597).
  - An underrun raises `underruns_o` (:657), never `rails_o` (`rail_p_w`, :645 and :664), and `RENDER_STAT` exposes no underrun count (:2026-2034, :2053).
  - The page's "cannot tell the two apart" (:1535-1542) is correct.
- **Docs gates at the head:** all exit 0 (`receipts/gates/summary.txt`).
  - `docs_check.py`, `check_doc_style.py`, `check_doc_paths.py`, `check_feature_status.py` and `git diff --check`.
  - `gen_toc.py --check` and `check_em_dash.py --base 40714c1bd...`, both run under the pinned renderer, which was installed with hashes in a private scratch environment. The em-dash gate reports 609 added lines and 0 findings.
- **Privacy, value-blind** (`scripts/derive_mask_tokens.py`, `scripts/privacy_scan.py`). The masked token was taken from the `5bad6a43` to `36ee6d8a` diff of `grade_b8.py` and never printed. The scan counts three things: the token within 40 characters of a channel word, any sample-format-name shape, and any "layout/decode hidden" claim.
  - The B8 section and the round-2 added lines have 0 token hits and 0 format names. The one "hidden" hit is :1803-1804, which says the decode is *not* masked.
  - Packet at the pin: 0 token hits near a channel word in the external capture's tools. The four "near" hits are `timeout -k` values in lock wrappers. Every format-shape hit is the SoC board's 8-channel McASP0 path (`hw:0,0`), not the external capture.
  - Probe: the scan flags the `5bad6a43` grader at line 39, and not the `36ee6d8a` grader.
  - Round-2 archive `author-r2`: 0 token and 0 format hits. The "hidden" hits are statements that the decode stays readable.

## Round-1 findings at this head

| Round-1 finding | State at `77299b4f` | Evidence |
|---|---|---|
| R454-1 F1 (MAJOR) = R455-1 F4 (MINOR): channel count in published `grade_b8.py` | RESOLVED | Masked top-only at `36ee6d8a`. The page row :1856 is the retained file `77949fd1...`, 27,959 B, "as run `330c14cd...`". The value-blind scan is clean at the pin and flags `5bad6a43`, and the page says that commit stays in history (:1817-1821) |
| R454-1 F2 (MINOR): page implied the layout was hidden; decode readable | RESOLVED per ruling 5971696657 | :1797-1806 says the format name and channel count are masked and the decode (byte width, byte order) is not, and links the ruling. No B8 line claims the layout is hidden. The snippet-size reason now says "channel count" (:1774-1775) |
| R454-1 F3 = R455-1 F1: 19.0 s and the stall signature | RESOLVED | :1621-1635, :1758-1760 and PR body row "B-CRF repeated" read 18.7 s / 899,009 frames, with the basis named, and 18.69 s for the stall clusters. Positions are given on both bases. Two clusters are off the signature, and the third is on it with the 23,776-frame repeat. All re-derive |
| R454-1 F4 = R455-1 F2: where the evidence is | RESOLVED | :1306-1310 and :1811-1832: the branch, the full pin, the label-to-path mapping with an example, `MANIFEST.json`'s two hashes, the eight path-masked records, and the source of each row. All 46 rows verify there. The PR body's Evidence paragraph matches |
| R455-1 F3: cause asserted for the #645 pre-set slips | RESOLVED | :1584-1594 gives the times, counts, spacing and 3.52 s period, and says "this lane gives no cause for them". :1721-1728 offers the six post-boot dups as untimed data, with no mechanism |
| R455-1 S1: `pend=1` | ADOPTED | :1679 and :1700-1701; re-derived above |
| R455-1 S2: render path live | ADOPTED | :1384-1387; re-derived above |
| R455-1 S3: `mr` limit | ADOPTED | :1761-1762 |
| R454-1 R1: `0x8D8` label | APPLIED | :1421-1422 uses a working relative link to the 0x8D4 section that holds both words |
| R454-1 R2: raw-record wording | APPLIED | :1770-1775, as given, plus the channel-count reason |
| R454-1 R3: "no command sent" | APPLIED | :1303 and :1684, as given |

None got worse. The round added no new claim that fails against its evidence.

## Findings

No BLOCKER, MAJOR, MINOR or RESIDUE finding.

```text
[R455] SUGGESTION Docs - docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md:1794-1796, :1828-1829 - S1: say where the 79-entry lane redaction record is published
Requirement/evidence: at the pin, the published author/redaction.json lists 78 files. The 79th,
  grade_b8.py, is recorded in MANIFEST.json, and the page explains this at :1826-1831. The
  79-entry copy is published later, at d6cc650f author-r2/redaction.json, which the page cannot
  name without a later pin.
Impact: none on any figure or verdict. A cold reader at the pin counts 78 + 1.
Optional change: when the next round re-pins, name author-r2/redaction.json, or write
  "79 (78 in the published redaction.json, and grade_b8.py in MANIFEST.json)".
Verification: the count reconciles at the named pin.
```

## Lens results (exact head `77299b4f`)

```text
[R455] PASS Conformance - 629_MEDIA_CLOCK_FOLLOWING_BENCH.md:1291-1304, :1584-1606, :1732-1745 - item verdicts and acceptance unchanged by round 2; each matches the assignment ruling (5971696657 items 1-6) and the declared behaviour in REGISTER_MAP 0x8D4/0x8D8/0x8DC and SAVED_STATE_FASTCONNECT 9.1; #645 carries data only, and no requirement claim moved
[R455] PASS RTL - hdl/ieee1722/aaf/KL_render_setpoint.sv:567-572,:591-597,:645,:657,:664; REGISTER_MAP.md:1867-1868,:2026-2053 - the delta's RTL statements (SLIP_TDM at 0x8D8; underrun and short-queue recentre leave the same prefill/converged trace with no rail; underrun count not in RENDER_STAT; an unfed ring counts nothing) match the RTL and the register map; no HDL in the diff
[R455] PASS Robustness - packet@36ee6d8a summary/crfll/{grade,lockloss}.json, summary/sw/switches.json, runs/pc/*, restore/dut-end2.txt - the boundary and failure records (the missing-word poll, multi-second host stalls, stall-cluster signatures, pre-set slips, pend across a cold cycle, residual dups after reset) are stated as recorded, with no unsupported cause; re-derived in receipts/rederive_round2.txt
[R455] PASS Tests - receipts/hash_rows_36ee6d8a.txt, receipts/rederive_round2.txt, receipts/probe_* - every bench figure the round adds re-derives from the pinned packet; the hash check fails against 5bad6a43 and the privacy scan flags the 5bad6a43 grader, so both checks can fail; no executable test changed in the diff (docs only)
[R455] PASS Docs - 629_MEDIA_CLOCK_FOLLOWING_BENCH.md:1267-1868; receipts/gates/summary.txt; receipts/privacy_scan_*.txt - evidence pointer, masking statement, hash rows and wording match the pinned evidence and the ruling; all seven docs gates exit 0; value-blind scan finds no capture channel count or format name on the page, in the pinned packet or in the round-2 archive; PR body consistent with the page
```

## Ledger (reviewer-owned)

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | B8 verdict and acceptance tables :1291-1304, :1732-1745; ruling 5971696657; REGISTER_MAP 0x8D4-0x8DC; SAVED_STATE_FASTCONNECT 9.1 | R455-2 | `77299b4fca1ec3268f0997c55a51d84955bbfeca` |
| RTL | CLEAN | `KL_render_setpoint.sv` :60-95, :550-668; REGISTER_MAP :1843-1868, :2006-2053; diff has no HDL, gitlinks unchanged | R455-2 | `77299b4fca1ec3268f0997c55a51d84955bbfeca` |
| Robustness | CLEAN | `grade.json`, `lockloss.json`, `switches.json`, `pc.json`, NVM reads, post-boot polls and end read at `36ee6d8a` | R455-2 | `77299b4fca1ec3268f0997c55a51d84955bbfeca` |
| Tests | CLEAN | 46 hash rows at `36ee6d8a`; round-2 re-derivation; two fault probes against `5bad6a43` | R455-2 | `77299b4fca1ec3268f0997c55a51d84955bbfeca` |
| Docs | CLEAN | B8 section :1267-1868; seven docs gates; privacy scans of the page, the pinned packet and `author-r2`; PR body at the head | R455-2 | `77299b4fca1ec3268f0997c55a51d84955bbfeca` |

## Real limits

- This is a docs-only delta review. No bench, hardware or physical calibration was run (physical calibration NOT RUN), and the bench data are taken as recorded in the packet. The raw files stay on the bench host and were not examined. Their hashes were matched to the packet's records only.
- The privacy scan is value-blind and shape-based. It derives the channel count from the published mask diff. It looks for format names by pattern only, since the capture's format name is not available to the reviewer, so a format named outside those shapes would not be caught.
- `5bad6a43`, with the unmasked grader line, stays in the evidence branch's history by the manager's choice of a top-only mask. The page says so (:1820-1821).
- The pinned `RAW-ARTIFACTS.json` gives the snippet-size reason as "the capture's layout", where the page says "channel count". That is evidence text at the pin, not a page claim. It does not say the decode is hidden.
- Hosted checks at this head, as observed: these completed with success: `rtl-fast`, `changes`, `docs-check-no-git`, `elaborate`, `wire-accountability`, `bdd-conformance` and `full-ci-gate`. `docs-check` was still in progress. These were SKIPPED, not executed: `verilator-suites`, `yosys-portability`, `verilator-lint`, `yosys-elaboration`, the shard jobs and Physical gPTP (`receipts/hosted_check_runs_77299b4f.tsv`). A skipped context is not evidence.
- The clone stayed at the exact head: tree equal, no status lines, index and worktree clean, gitlinks unchanged (`receipts/clone_integrity.txt`). No file in the clone was modified.

## Pending manager duties

- Confirm hosted acceptance at the exact head, including the in-progress `docs-check`, and run the act replica. These belong to the manager.
- Build and validate the final candidate merge against live dev `546437243e87eb5a78783a9e3cd5d1badcc3423e`. PR #644 is stacked underneath. This is distinct from the source validation reviewed here.
- Get the second independent positive and an explicit maintainer authorization before any merge. Carry S1 at the manager's discretion.

R455-2 FINISHED
