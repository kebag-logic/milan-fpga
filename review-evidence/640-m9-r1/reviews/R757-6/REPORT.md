[R757] POSITIVE - exact head 3f5fea241e8dacd976798ca817c67e55096cf1aa

# R757-6: internal cleared-context review of PR #828 (issue #640), round 6

- Head `3f5fea241e8dacd976798ca817c67e55096cf1aa`, tree `e2600e7d503b92f793cd48cad8c9fd47fb645f7b`.
- Delta: `270866ec..3f5fea24`, two one-line commits with no bodies or trailers, on `docs/design/MARK_II_STREAM_ENGINES.md` only (SE below): 10 lines added, 4 removed, mode unchanged. No code, generator, gate, configuration or gitlink.
- Source base and live dev: `1f29f189279f9fc0132f4918e47342b87d22f33a`, read from the remote (`receipts/live_dev.txt`).
- Taken as given: the manager's ruling on R758-5-F1. The short-margin behaviour stays open by ruling and is not a finding here.

## Verdict

POSITIVE. No BLOCKER, MAJOR or MINOR is open.

- All six focus checks hold.
- One RESIDUE item (RR11) and three SUGGESTIONS are recorded.
- The delta breaks nothing from earlier rounds, so the earlier lens results on untouched text stand.

## Findings

### RR11 RESIDUE - RTL, Robustness, Docs - SE:627; SE:1173 requirement cell; PR body, known limitations "Short margin on both networks" - the lapse sentence omits "both networks"

- **Authority and evidence:** the lapse depends on the next packet's first copy. A short margin on the slower network alone never reaches rule 2.
  - The linked probe's own control shows it: "primary 60 to 180 us latency, secondary 10 to 50 us margin" gives 1 anchor and 0 shifts.
  - My probe agrees: with one network at 150 to 200 µs and the other at 10 to 50 µs, either way round, there is 1 anchor and 0 shifts at all three rates (`receipts/probe_short_margin_r6.out`, section C).
  - R758-5-F1 words this correctly in its evidence ("a packet's first copy"). Its prescribed sentence is shorter, and the author applied that sentence as written.
- **Why RESIDUE:** item 3's title and verification both already say both networks, and the sentence overstates the limit rather than hiding it. No rule, register, figure, test or clause claim changes.
- **Impact:** a reader of SE:627 alone could think one slow network lapses the head.
- **Exact fix:**
  - SE:627: "With both copies' margins under 125 µs, every head lapses." (10 words, so it stays within the style limit.)
  - SE:1173: "A margin under 125 µs on both networks lapses the head before the next packet".
  - PR line: "a margin under 125 µs on both networks lapses the head every packet".
- **Verification:** read the three lines against section C of the receipt.

### Suggestions (optional, for lane 6's handoff)

- **S14 - Tests, Robustness - SE:1173 verification: add an arm near and across 125 µs.** The 10 to 50 µs arm is well clear of the threshold. Near it the threshold moves with the conversion error and drift. My stress model uses rail-to-rail error at every packet:

  | Margin on both networks | Anchors in 2,000 packets | Phases with a shift (48 / 96 / 192 kHz) |
  |---|---:|---:|
  | 110 to 120 µs | 2,000 | 17 / 33 / 64 |
  | 124.0 to 124.9 µs | 1,400 to 1,479 | 11 / 21 / 43 |
  | 125.2 to 126.0 µs | 510 to 564 | 8 / 18 / 37 |
  | 100 to 150 µs | 454 to 558 | 17 / 33 / 64 |
  | 130 to 140 µs | 1 | 0 / 0 / 0 |

  So "every packet" is exact away from the threshold, and a mixed band still shifts without lapsing every packet. Case H has such bands for tu only.
- **S15 - Tests - SE:1173: the lane should define "shift" when it states the limit.** SE:628 speaks of copies, and one packet's copies land at most one sample apart, because 2.744 µs is under the 5.208 µs sample period at 192 kHz (section F). The probe counts packet-to-packet steps. Under rail-to-rail error between consecutive packets, a step reaches 2 samples at 192 kHz (section A). That swing is a stress assumption, not a measured behaviour, and no page text is wrong.
- **S16 - Tests, Docs - SE:1173: name the model the linked probe imports.** The probe imports `merge_model` unconditionally, and its pinned link does not lead to that file. It runs with `review-evidence/640-m9-r1/author-r4/evidence/model/merge_model.py`, which reproduces the published output byte for byte. The handoff says so; the page does not.

## Focus checks

1. **Conditioned claims hold.** SE:624 and SE:660 hold under a valid head.
   - Section D ran margins of 150 to 200 µs and 1,800 to 1,950 µs, first arrival interleaved, conversion error up to 2.744 µs, at 48, 96 and 192 kHz over 64 grid phases. It found 0 shifts and 0 unwritten samples, including with 1 % loss on each network.
   - The only own-time placement left is the anchor, which SE:625 states.
   - The other touched pages carry no copy of either claim. A search of the area plan, FR_NFR, both architecture pages, REQUIREMENTS and docs/README finds no copy.
   - The clause text was not opened. SE:660 rests on the Annex D.2 quotation in the author's handoff.
2. **The margin text is correct against the rules, with RR11 as its one wording gap.**
   - The chain SE:672 (a passed time is invalid), rule 2 at SE:647 and SE:653 (the head takes its copy's time) gives the lapse.
   - Section A shows 2,000 anchors in 2,000 packets across the 10 to 50, 50 to 100 and 110 to 120 µs bands.
   - Interleaving is the cause: section E shows 0 shifts with one network first or alone, each still with 2,000 anchors, and section F shows copies at most one sample apart.
   - The phase counts of 17, 33 and 64 of 64 match the probe exactly, from a separately written implementation.
   - My re-run of the linked probe is byte-identical to its published output, sha256 `cd30fc2c...` (`receipts/probe_margin_rerun.out`).
3. **Item 3 is a verifiable requirement.**
   - SE:1173 states the requirement, leaves the allowed shift to the lane, and carries the setup exactly as assigned: clean copies on both networks, 10 to 50 µs before their time, first arrival interleaved, 48, 96 and 192 kHz, every grid phase. The test fails on a shift beyond what the lane states.
   - 766 and 383 appear on the page only at SE:1173, labelled "the probe's result, not a design figure", and in the PR body only in the Round 6 row. The PR limitation line says the PR states none.
   - Both pinned links resolve at `f9cfe08c`, an ancestor of the evidence tip `4c29abbd`, and their digests equal the evidence tree's.
   - Output section A prints 766 and 383 at each rate.
4. **The PR's known limitations gained the line.** See `receipts/check_delta_r6.txt`; the wording is RR11's.
5. **Residue applied exactly.**
   - RR8: SE:1185 and the PR Round 5 row match my exact fix, and read correctly against case G at SE:1205.
   - R758-5-R1: its text differs from RR8's and means the same. Both make the requirement cover the pair arms, so it is closed by RR8's wording.
   - RR9: SE:647 matches, and agrees with WMAP at SE:825. "clears the map" has 0 hits.
   - RR10: the `07f8eb91` row ends "The tu text left in round 5."
6. **Nothing else changed.**
   - The stat shows one file, +10 and -4. The rule table differs only in rule 2's action wording, with no condition change.
   - No register line changed. Every number new to the diff belongs to item 3 or its links.
   - The PR body's Round 3 note "(round 6 conditions this on a valid head)" goes beyond the assignment. It is disclosed in the handoff and the body, and it is correct.
   - The live PR body equals the packet's `PR-BODY.md`, apart from one trailing newline.
   - The docs gates I ran at this head all exit 0; see Gates below.

## Prior findings at this head

| Finding | Result |
|---|---|
| R758-5-F1 MINOR | Closed by its second outcome, per the manager's ruling: SE:624, :627-628, :630, :660, :1173 and the PR limitation. RR11 is wording on the sentence F1 prescribed |
| R758-5-R1 RESIDUE | Closed with RR8's wording |
| R757-5 RR8, RR9, RR10 | Closed, applied exactly |
| R757-5 S8, S10 to S13; R758-5 S1 to S4 | Optional, not taken; no effect on coverage |
| R757-5 S9 | Optional and still real. It is the one-network form of the lapse with packet-to-packet jitter. Item 3 names both networks as assigned, so S9 has no owner on the page and stays with the manager's handoff. SE:665 is unchanged by this delta |

## Gates

Run at this head from the clean clone, concurrently, with the pinned renderer and the pinned wavedrom package in a scratch environment. Logs and rc files are in `receipts/gates/`.

| Gate | rc | Result |
|---|---:|---|
| `docs_check.py`, on the clone and on an exported tree without git | 0, 0 | 0 findings, 213 pages |
| `check_em_dash.py --base 1f29f189` and `--selftest` | 0, 0 | 0 findings over 1,754 added lines in 7 pages |
| `check_doc_style.py` and `--selftest` | 0 | OK |
| `gen_toc.py --selftest`, `--verify-anchors`, `--check` | 0 | 152 pages OK |
| `check_doc_paths.py` | 0 | 1,084 paths resolve |
| `check_baremetal_only.py --check` and `--selftest` | 0 | PASS, 867 arms |
| `check_archive.py`, `check_gptp_docs.py`, `check_solution_docs.py`, `check_submodule_docs.py`, with `--selftest` | 0 each | OK |
| `DOC_MAP.gen.py`, `timesync_chain.gen.py`, `submodule_boundaries.gen.py`, `check_diagram_pngs.py`, `gen_wavedrom.py` with its three `--check` runs | 0 each | current |
| `check_feature_status.py --self-test`, `gen_module_matrix.py --check` | 0 each | 0 findings; 80 modules |
| `git diff --check` against the merge base | 0 | no output |

The first pass used the system interpreter. `check_em_dash.py` and `gen_toc.py` then exited 2, and `gen_wavedrom.py` exited 1, because their packages were missing. They pass with the pinned packages, and those are the logs kept here. The clone is byte-exact afterwards (`receipts/clone_restore_check.txt`).

**Author's packet.** `author-r6` matches the published manifest: 115 of 115 published digests match, and 114 of 114 `SHA256SUMS` entries match their recorded originals. Direct `SHA256SUMS` checks fail on 14 files, and the manifest marks exactly 14 as path-redacted. All 50 rc files read 0. Spot checks of the builder legs, em dash and bare-metal logs match the PR table. Other gates are taken from that packet, not re-run: HDL reference, SDK, NVM, ratchets, idioms, builder legs, CI events, act runner, wire accountability and the imported gPTP docs. The delta touches nothing they read beyond page text.

## Lens results

```text
[R757] PASS Conformance - SE:624-630, :647, :660, :1173, :1185 at this head - conditioned claims and TU-4 against the rule table, case G and R758-5-F1's outcome; RR11 recorded; clause text not opened
[R757] PASS RTL - SE:647, :653, :672, :824-827 at this head - lapse, re-anchor and map restart against the register definitions and receipts/probe_short_margin_r6.out; no register changed; the delta has no RTL file
[R757] PASS Robustness - receipts/probe_short_margin_r6.out sections A to F - margin bands, one-network short margin, loss, every grid phase of 64, all three rates; short-margin behaviour open by ruling; S14 recorded
[R757] PASS Tests - SE:1173 verification cell, receipts/probe_margin_rerun.out, author-r6 packet - setup as assigned, fail condition stated, linked probe reproduced byte for byte; S15 and S16 recorded
[R757] PASS Docs - SE delta, live PR body, receipts/check_delta_r6.txt, receipts/gates/ - exact text of every closure, links, size stated only as the probe's result; RR11 recorded
```

## Ledger (reviewer-owned)

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | SE:624-630, :647, :660, :1173, :1185, :1205; R758-5-F1 outcome; AP:276 and other touched pages searched | R757-6 | 3f5fea241e8dacd976798ca817c67e55096cf1aa |
| RTL | CLEAN | SE:647, :653, :672, :824-827; `receipts/probe_short_margin_r6.out`; stat shows no RTL in the delta | R757-6 | 3f5fea241e8dacd976798ca817c67e55096cf1aa |
| Robustness | CLEAN | `receipts/probe_short_margin_r6.out` sections A to F; re-run of the linked probe | R757-6 | 3f5fea241e8dacd976798ca817c67e55096cf1aa |
| Tests | CLEAN | SE:1173 verification; `receipts/probe_margin_rerun.out`; `author-r6` gate receipts against the manifest; gate self-tests in `receipts/gates/` | R757-6 | 3f5fea241e8dacd976798ca817c67e55096cf1aa |
| Docs | CLEAN | SE delta; live PR body Round 3, Round 5, Round 6, commit rows and known limitations; `receipts/check_delta_r6.txt`; `receipts/gates/` | R757-6 | 3f5fea241e8dacd976798ca817c67e55096cf1aa |

## Real limits

- **Evidence type:** every probe result comes from a page-derived model, not an implementation. The figures measure no real talker or network. Rail-to-rail error at every packet is a stress assumption.
- **My probe:** its first run had a floating-point artefact at grid phase 0, which showed shifts in the non-interleaved arms. I added the rounding guard the linked probe also uses and re-ran it. The kept receipt is the corrected run, whose worst-case count of 807 shifts differs from the linked probe's 766 because the models differ. That is why the page's choice to label 766 as the probe's result is right.
- **Standards:** I did not open their text. No copy is in the repository.
- **Round scope:** as briefed, this judges the delta. I did not re-derive the issue's acceptance criteria or re-review untouched text. Earlier lens results on that text are carried, not re-earned.
- **Reading order:** I read R758-5's report only after writing a draft verdict, whose digest is in `receipts/draft_sha256.txt`. Two things reached me earlier:
  - A listing of recent PR comments at the start showed the first 1,400 characters of the last eight, including the opening summaries of R758-4 and R758-5.
  - The author's handoff, which the brief requires, quotes R758-5-F1 and R1.
  The draft's verdict and findings did not change after the read. I cannot show that those earlier summaries had no influence.
- **Gate coverage:** I did not run the builder legs or the wider bank, as instructed. Their evidence is the author's self-recorded packet.
- **Hosted runs:** at my last look this head had 12 check runs queued and 2 in progress, with none finished (`receipts/hosted_checks.txt`). I draw no evidence from them.
- **Hardware:** physical calibration and bench work were NOT RUN. Field skips are not hardware proof.

## Pending manager duties

- Carry RR11 to the residue checklist.
- Carry S9, S14, S15 and S16 to lane 6's handoff. S9 has no owner on the page.
- Own hosted and act acceptance at the exact head, and the current-dev merge candidate with its builder and native banks.
- Obtain the external review's verdict at this head. Merge still needs two independent positive reviews and explicit maintainer authorization.

R757-6 FINISHED
