[R758] POSITIVE - exact head 3f5fea241e8dacd976798ca817c67e55096cf1aa

Round R758-6, issue #640 / PR #828, documentation only. Tree `e2600e7d503b92f793cd48cad8c9fd47fb645f7b`. Delta reviewed: `270866ec..3f5fea24`, two commits on one page, plus the PR body. `SE` below is `docs/design/MARK_II_STREAM_ENGINES.md`.

## Summary

- All five lenses are clean at this head. There is no open BLOCKER, MAJOR or MINOR.
- R758-5-F1 is closed by its second outcome, as the manager ruled. RR8, R758-5-R1, RR9 and RR10 are applied exactly.
- One new RESIDUE item: the margin sentence reads as an exact, per-copy threshold, and it is not one. That sentence is my own R758-5-F1 wording, applied as written. Its exact fix is below.
- Four optional SUGGESTIONS are for lane 6.
- The published probe re-runs byte-identical. Docs gates pass at the head, in the author's receipts and in my own subset.

## Focus checks

| # | Check | Result | Evidence |
|---:|---|---|---|
| 1 | Conversion-error and Annex D.2 claims hold under their condition | Holds | SE:624, SE:660. Arm D of `scripts/probe_margin_r6.py`: 0 placements with a wrong k, at both a short and a long margin, across 3 rates and 64 phases. Arm A: 0 shifts while the head stays valid (127.8 to 130 and 150 to 200 µs, 1 anchor). 0 lost packets in the published output. Every shift measured sits at a rule 2 anchor, which SE:625 excepts |
| 2 | Text on a margin under 125 µs, against the rules and the probe | Correct for the assigned band, with one wording residue (R758-6-R1) | SE:627-628, SE:1173 against rule 2 (SE:647) and SE:672. Margins of 10 to 50 µs: 2,000 anchors of 2,000. Partner copies never land more than 1 sample apart at any rate. Published controls: 0 shifts when the head stays valid |
| 3 | Item 3 is verifiable; its size appears only as the probe's result | Holds | SE:1173. The requirement is stated: the lane states its allowed shift and the listener stays within it. The verification carries the assigned setup word for word and a failure condition. 766 and 383 appear once on the page, in that row, marked "the probe's result, not a design figure". They match section A of the published output at all three rates |
| 4 | Known limitations gained the line | Holds | PR body, "Short margin on both networks". It names item 3 and states no figure |
| 5 | RR8/R758-5-R1, RR9, RR10 applied exactly | Holds | See "Prior findings" below |
| 6 | Nothing else changed; docs gates pass | Holds | `git diff --name-status 270866ec 3f5fea24` lists one modified file, +10/-4. The only rule-table change is rule 2's action wording. Commits have one-line subjects, with no body or trailer. Gates as listed under Tests |

## Findings

### R758-6-R1 RESIDUE - Docs, RTL, Robustness - SE:627, SE:1173, PR known limitations - the margin sentence reads as an exact, per-copy threshold

- **Authority/evidence:**
  - The lapse depends on the first copy of the next packet. It lapses when that copy arrives after the head's time. The head's time and the next copy's time each carry conversion error, so the threshold is 125 µs plus or minus that error, not exactly 125 µs.
  - Band results, `receipts/model/probe_margin_r6.out` arm A, margins on both networks:

    | Margin | Anchors of 2,000 | Reads against the sentence |
    |---|---:|---|
    | 10 to 50 µs | 2,000 | Holds |
    | 122.3 to 124.9 µs | 1,595 to 1,660 | Under 125 µs, yet not every packet lapses |
    | 125.1 to 127.6 µs | 260 to 335 | Over 125 µs, yet some packets lapse and shift |
    | 127.8 to 130 µs | 1 | No lapse |

  - Read per copy, the sentence also fails. SE:1173 defines margin per clean copy. With one network at 150 to 200 µs and the other at 10 to 50 µs, there is 1 anchor and 0 shifts (arm B). The published probe's fast-primary control shows the same.
- **Why RESIDUE:** the rules, registers, figures and item 3's 10 to 50 µs verification band do not change. The rule table still governs, and only the summary sentence is loose. The sentence is R758-5-F1's required text, so the author did as asked.
- **Impact:** a lane reader could take 125 µs as an exact boundary, or take one short network as enough to lapse the head.
- **Exact fix:**
  - SE:627: "A first-copy margin well under 125 µs lapses the head every packet."
  - SE:1173, replacing the second sentence: "A first-copy margin well under 125 µs lapses the head before the next packet, so rule 2 places every packet by its own time. Within the conversion error of 125 µs, only some packets lapse."
  - PR known limitations: "a first-copy margin well under 125 µs lapses the head every packet".
- **Verification:** read the three lines against arms A and B.

### Suggestions (optional, none blocks)

- **S1 - Tests, Robustness - SE:1173, SE:657, SE:1153: item 3's band starts at 10 µs, and the duplicate path changes below about 5 µs.** A partner can then arrive after the head's time has passed, so rule 2 writes the packet again and no duplicate is counted. Arm E, worst across 3 rates and 64 phases: 1,282 of 2,000 packets written twice at 0.1 to 2 µs, 86 at 2 to 5 µs, 0 at 5 to 10 µs and at 10 to 50 µs. This predates the delta and falls in the case the ruling hands to lane 6. Lane 6 could add an arm under 10 µs. Processing latency is not modelled.
- **S2 - Tests - SE:1173: the lane should say which shift it states.** Partner copies never land over 1 sample apart. Steps between consecutive packets can reach 2 samples at 192 kHz in the probe's independent per-packet jitter, because a 5.488 µs swing exceeds the 5.208 µs sample period: 1 step of 28,286 off-nominal steps, in each of the 10 to 50 and 100 to 120 µs bands. With a slowly varying error (arm C) only 1-sample steps appear. SE:628 stays true as written.
- **S3 - Robustness, Tests - SE:665: R757-5 S9 is retained.** It is the one-network form of the same lapse, and item 3 names both networks, as assigned. The published probe's jitter-free one-network control shows 0 shifts, which does not contradict S9's jittered arm. The manager should carry it to lane 6, as R757-5 asks.
- **S4 - Tests, Docs - SE:1153: the clean-copy row names no margin.** "Rendered samples equal the clean stream's" holds in my probes only above the lapse band (127.8 µs up). A pointer to item 3 would stop a lane reading the two rows as conflicting.

## Prior findings, resolved or retained

| Finding | State | Evidence at this head |
|---|---|---|
| R758-5-F1 | Closed by the second outcome, by ruling | SE:624 and SE:627-628 match the required text exactly. SE:660 carries the condition. Item 3 at SE:1173 and the PR limitation are present. The behaviour stays open by ruling, not as a finding |
| R757-5 RR8 | Closed, exact | SE:1185 and the PR Round 5 row match the exact fix word for word |
| R758-5-R1 | Closed | SE:1185 uses RR8's text, not R1's. They mean the same and case G still binds. As R1's reviewer I accept the substitution |
| R757-5 RR9 | Closed, exact | SE:647, consistent with `LCTX_MERGE` WMAP at SE:825. Arm D confirms the reason: clearing bit 0 writes the partner again, and bit 0 set gives 0 packets written twice |
| R757-5 RR10 | Closed, exact | PR commit row `07f8eb91` ends "The tu text left in round 5." |
| R757-5 S8 to S13, R758-5 S1 to S4 | Optional, not taken | S9 retained above as S3. The others stay as published |

The author also added "(round 6 conditions this on a valid head)" to the PR's Round 3 row, outside the assignment. It is disclosed in the handoff, correct, and history text only, so it is not a finding.

## Clean lens results

[R758] PASS Conformance - SE:624, SE:660, SE:647, SE:1173, SE:1185 at this head - conditions read against rule 2, head upkeep, F1's second outcome and the Annex D.2 quotation in the author's handoff; item 3 against the assigned setup

[R758] PASS RTL - SE:647, SE:672, SE:824-827 and `git diff --name-status 270866ec 3f5fea24` - no RTL or register in the delta; rule 2's new wording read against WMAP and exercised in arm D

[R758] PASS Robustness - `receipts/model/probe_margin_r6.out`, `receipts/model/probe_margin_r5_rerun.out` - margin bands around 125 µs, one short network, slow and independent error, margins under 10 µs; S1 and S3 recorded, both in the ruled case

[R758] PASS Tests - SE:1173 verification column; author-r6 `evidence/probe/`, `evidence/gates/`; my re-run byte-identical to `probe_margin_r5.out` - the item can fail for its stated defect: a lane stating a shift below the measured 1 sample fails on the probe's setup

[R758] PASS Docs - SE delta, live PR body (identical to author-r6 `PR-BODY.md`), `receipts/gates/`, anchors and pinned links - R758-6-R1 recorded as residue

## Evidence checked

- **Author packet:** all 115 author-r6 files match the published digests in `MANIFEST.json`. All recorded original digests match the packet's `SHA256SUMS`; the 14 files that differ from `SHA256SUMS` are the manifest's path-redacted ones. All 50 gate rc files read 0. The builder log names source revision `3f5fea24`. The evidence commit carries no signature, so this rests on digests alone.
- **Probe:** `probe_margin_r5.py` and `.out` at pinned commit `f9cfe08c` match the handoff's digests. My re-run against the published round-4 merge model is byte-identical. The page's links resolve at that commit.
- **Own gates at this head, `receipts/gates/`, all rc 0:** `docs_check`, em dash (0 over 1,754 added lines), doc style and its selftest, cited paths (1,084), contents with anchors, doc map, feature status, bare-metal scope (0 over 1,434 files), archive, traceability, `git diff --check` against the base. Em dash and contents first returned 2 because the pinned Markdown renderer was missing. They then passed in a disposable environment built from `tools/markdown/requirements.txt`.
- **Comment rule:** the delta touches no source comment. SE:1173's link path names a review round, the same form as item 2's existing pointer, on a design page, so the rule does not apply.
- **Restoration:** `git diff-index` rc 0, index equals tree for modes and blobs, head and tree as above, six submodule gitlinks unchanged and not populated. Ignored bytecode from my gate runs was removed.
- **Independence:** my preliminary verdict and ledger were written before I read the prior reports; the digest is in `receipts/draft_sha256.txt` and the draft is not published. What changed since: the prior-findings table was filled in, and arm E and S1 to S4 were added. The verdict and ledger did not change.

## Ledger

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | SE:624, :647, :660, :1173, :1185 against F1's second outcome and the handoff's Annex D.2 quotation | R758-6 | 3f5fea241e8dacd976798ca817c67e55096cf1aa |
| RTL | CLEAN | Delta name-status (no RTL); SE:647, :672, :824-827; probe arms A and D | R758-6 | 3f5fea241e8dacd976798ca817c67e55096cf1aa |
| Robustness | CLEAN | `probe_margin_r6.out` arms A, B, C, E; `probe_margin_r5_rerun.out` | R758-6 | 3f5fea241e8dacd976798ca817c67e55096cf1aa |
| Tests | CLEAN | SE:1173 verification; author-r6 probe and gate receipts; own probes and gates | R758-6 | 3f5fea241e8dacd976798ca817c67e55096cf1aa |
| Docs | CLEAN (R758-6-R1 residue) | SE delta; live PR body Round 6, Round 5, Round 3, commit row and limitations; `receipts/gates/`; links and anchors | R758-6 | 3f5fea241e8dacd976798ca817c67e55096cf1aa |

Text the delta does not touch keeps its prior lens verdict from R757-5 and R758-5; nothing in this delta changes what it depends on.

## Real limits

- Every result comes from page-derived models, not an implementation. Margins and error shapes are chosen stress arms, not measured networks.
- I did not open the standards' text. Annex D.2 rests on the author's quotation and the repository's records.
- I ran only the docs gates a page edit can affect. Builder legs, SDK and submodule-backed gates rest on the author's receipts. The clone has no submodules populated.
- Hosted checks at this head were still queued or in progress when I looked, so I claim no hosted result. No manager source bank runs at this head, and none is inferred.
- Physical calibration NOT RUN; field skips are not hardware proof. This round touched no hardware.

## Pending manager duties

- Accept hosted and local-replica evidence at the exact head.
- Build and validate the current-dev merge candidate at the merge turn (source base and live dev both `1f29f189`) and link its receipts.
- Add R758-6-R1 to the residue checklist.
- Carry S1 to S4 to lane 6, including R757-5 S9 as S3.
- Obtain the second required positive review and explicit merge authorization.

R758-6 FINISHED
