[R758] POSITIVE - exact head e7310e94fff7188c5800a94c03a3f0e4c7c1c024

Round R758-7, issue #640 / PR #828, documentation only. Tree `0a9f7f6a5b8d385fc43116ba0035d384b125b8c7`. Delta reviewed: `3f5fea24..e7310e94`, two commits, three files, +24/-24. Authority for the delta: the [owner decisions of 2026-11-01 13:35](https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-6558021030).

No BLOCKER, MAJOR or MINOR is open. One RESIDUE item and three SUGGESTIONS are recorded. The earlier lens results on untouched text stand, because the delta changes nothing they depend on.

Page labels: `FR` = `docs/reference/FR_NFR.md`, `SE` = `docs/design/MARK_II_STREAM_ENGINES.md`, `AP` = `docs/design/MARK_II_AREA_PLAN.md`.

## Focus checks

| # | Check | Result | Evidence |
|---:|---|---|---|
| 1 | NFR-LAT-03 states a target, bounds accepted, no connection refused, verification sound | Holds, with S1 and S2 | FR:306 reads "SHOULD be below 65 µs, and as short as possible", priority S (FR:20: S=SHOULD), and cites the decision. It reads "Those derived bounds are accepted and published, and no connection is refused because of them." It ends "a case above 65 µs that stays inside its published bound is not a failure." Every case the bench names has a published bound: see "Verification" below |
| 2 | Open question 1 gone, decision stated once, tables unchanged, renumbered, pointers land | Holds | `receipts/delta_check.txt`. With list numbers stripped, the only difference in the list is the removed block. Both bounds tables hash the same at both heads. The decision is stated once on the page, SE:227-234; SE:389 points to it. See "Pointers" below |
| 3 | No line presents 65 µs as binding or the mixed result as awaiting the owner | Holds, with R758-7-R1 | Search of every tracked Markdown page outside `review-evidence/` for 65 µs, and of all tracked files for NFR-LAT-03. The hits are FR:306, FR:612, SE, AP and three unrelated figures in `docs/design/MEDIA_CLOCK_FOLLOWING.md`. "Against 65 µs", "Met" and "Not met" read a figure against the target. `SE_TLAT_OVER` is a counter and fails nothing. The live PR body agrees |
| 4 | The area plan's rows agree | Holds | AP:60 and AP:255 both say target, met with one base format at 16 reservations per port, not met or exceeded by mixed formats and fewer reservations, bounds accepted. AP:255 adds "no connection is refused". AP:60 has no contrary text and links the same decision |
| 5 | RR11 and R758-6-R1 applied | Resolved in substance, not word for word | See "Prior findings". The two reports' exact texts conflict, so no single text could apply both. The author says so publicly in the handoff and the PR body |
| 6 | Nothing else changed; docs gates pass | Holds | `git diff --raw` lists three modified files, modes unchanged, no gitlink moved. Both commits have one-line subjects with no body or trailer. Gates are listed under "Gates and receipts" |

### Verification

The bench list in FR:306 and SE:1159 is all 32 talker streams, one format and mixed formats per port, so 16 reservations per port.

- **Mixed formats:** every rate has a published bound (SE:356-363).
- **One format at 16 reservations:** every published bound is below 65 µs, so a case above 65 µs here is above its bound and is not excused.
- **One format at 192 kHz, N=8:** the 16-reservation row stops at N=6, because only 14 eight-channel streams fit. From a fresh start, at every count from 1 to 14 streams, my probe stays below 65 µs even with the page's largest fixed terms. The worst is 64.145 µs at 11 streams (`receipts/probe/probe_192_one_format.out`).

So no case the bench names falls outside a published bound. Fewer-reservation setups reached by stops are not in that list. S1 records what a lane would find there.

### Pointers

- **SE:1151-1152, left unchanged by the author:** the author's reasoning is correct. The two sentences before it are about "A burst beyond S1", and the link goes to the section, where that case is now question 1, "Save bursts". The assignment named it as a pointer to the old question 1, and that reading was mistaken.
- **SE:389:** retargeted to `#talker-latency-budget`, which exists at SE:219.
- **AP:60:** its `#open-questions` link is gone.
- **FR:476:** "an open owner question there" still lands on Save bursts.
- **PR body line 279:** "open question 6" is Engine headroom at 192 kHz, SE list item 6.
- **Other references:** a search of the docs, REQUIREMENTS, CONTRIBUTING and AGENTS finds no other numbered reference to these questions. The area plan's "open decision" numbers are a separate list and did not move.

## Findings

### R758-7-R1 RESIDUE - Docs, Conformance - AP:276, Evidence column of lane 6 - "65 µs taps" reads as a limit the taps must show

- **Authority/evidence:** the owner decision says 65 µs is a target that does not bind every legal stream setup. FR:306 says the bench measures against the target and reports each case. AP:276 still reads "65 µs taps on all talker streams". The delta did not touch this line.
- **Why RESIDUE:** it is a label in an evidence cell. FR:306 governs, and no figure, test or claim changes.
- **Impact:** a lane reader could take lane 6's evidence to be 65 µs on all streams.
- **Exact fix:** AP:276: "Latency taps on all talker streams, reported against the 65 µs target; cable pulls; the [open design items](MARK_II_STREAM_ENGINES.md#open-design-items)".
- **Verification:** read the line against FR:306.

### Suggestions (optional, none blocks)

- **S1 - Conformance, Tests, Docs - FR:306, SE:230-231, SE:396-414: for fewer reservations, "its published bound" exists only for four rows.**
  - The page publishes four 48 kHz eight-channel rows and a formula for co-phased streams alone. It publishes no fewer-reservations figure at 96 or 192 kHz, and no ceiling over all such setups.
  - My start-and-stop search under the page's exact rule reproduces those four rows exactly. It also reaches setups with no row:

    | Rate | State reached | Wait | Estimated total | Nearest published figure |
    |---|---|---:|---:|---|
    | 48 kHz | Eight-channel in phase 2, two one-channel in phase 3 | 77.806 µs | 118.131 µs | 123.337 µs, not exceeded |
    | 96 kHz | Eight-channel in phase 5, one-channel in phase 6 | 88.965 µs | 121.456 µs | 93.216 µs, which is a 16-reservation bound |
    | 96 kHz | Two eight-channel in phase 0 | 62.361 µs | 94.852 µs | 93.216 µs, which is a 16-reservation bound |
    | 192 kHz | Eight-channel in phase 3, one-channel in phase 6 | 88.834 µs | at least 106.927 µs | 100.825 µs, which is a 16-reservation bound |

  - **Why not MINOR:** no statement on the page is false. These setups are not in the requirement's bench list, the requirement is a SHOULD, and no connection depends on them. No case the bench names is left undecided.
  - **Outcome if taken:** either publish a fewer-reservations ceiling, or state in FR:306 that a setup with no published row is reported against the target only. The first adds figures, so it needs a model run. Without either, a lane that runs such a setup can neither pass nor fail it, and could wrongly compare it with a 16-reservation bound.
  - **My search does not exceed 123.337 µs.** It is not exhaustive and this is not a proof of a ceiling.
- **S2 - Tests, Docs - FR:306: the row does not say what a case above its published bound means.** The handoff discloses this: the decision does not state it, so the row does not either. The bounds are upper limits, so such a measurement contradicts the derivation. A lane should record it that way. One sentence would settle it, if the owner wants it.
- **S3 - Docs - AP:270: lane 0's "Owner approval of the requirement text" could link the decision.** The approval has now been given. The cell is a dependency, not a claim that approval is pending, so nothing is wrong. Only the PR body records the approval.

## Prior findings

Read after my own pass; see "Independence" under "Real limits".

| Finding | State at this head | Evidence |
|---|---|---|
| R757-6 RR11: the lapse sentence omits "both networks" | Resolved | SE:636 "Both copies' margins", SE:1183 "on both networks", PR known limitations "on both networks". This is RR11's text with "about" added, and SE:636 reworded to stay at 10 words |
| R758-6-R1: the margin sentence reads as an exact, per-copy threshold | Resolved | SE:636-637 "about 125 µs" and "The threshold carries the conversion error, so it is approximate". SE:1183 "within that error of 125 µs, only some packets lapse". PR line says the same. "First-copy" and "well under" were not used; "on both networks" closes the per-copy reading and "about" closes the exact-threshold reading. The page's 2.744 µs error gives 122.256 to 127.744 µs, which matches my round-6 bands: partial lapse at 122.3 to 127.6 µs, none from 127.8 µs. The rule table (SE:657) still governs |
| R758-6 S1 to S4, R757-6 S14 to S16 | Retained, optional, not taken | Unchanged at this head. They stay for lane 6's handoff |
| Findings of rounds 1 to 5 | As R758-6 recorded them | The delta does not touch their text, apart from the lapse sentence above |

## Lens results

[R758] PASS Conformance - FR:306, SE:224-234, AP:60, AP:255 against issuecomment-6558021030 - target, bounds accepted and published, no connection refused, no restriction to one base format; R758-7-R1 recorded as residue; S1 recorded

[R758] PASS RTL - `receipts/delta_check.txt` (no RTL, generator or gitlink in the delta); SE:636-640 and SE:1183 against rule 2 at SE:657 - the reworded lapse text agrees with the rule table; no register or rule changed

[R758] PASS Robustness - SE:636-637, SE:1183 against my round-6 margin bands; `receipts/probe/probe_fewer_bound.out` - boundary band and one-network reading closed; the below-16-reservations boundary searched, S1 recorded

[R758] PASS Tests - FR:306 verification, SE:1159, `receipts/gates/`, author-r7 `evidence/gates/` - no case the bench names lacks a published bound; 192 kHz N=8 probed; S1 and S2 recorded. The change is documentation, so no test can fail for it beyond the gates

[R758] PASS Docs - the three changed pages, the live PR body, `receipts/delta_check.txt`, `receipts/gates/` - tables unchanged, list renumbered, pointers land, anchors and links resolve; R758-7-R1 recorded as residue

### Gates and receipts

- **My run at this head, all rc 0:**
  - `docs_check`: 0 findings, 213 Markdown files
  - `check_em_dash --base 1f29f189`: 0 findings over 1,754 added lines
  - `check_doc_style` and its selftest
  - `check_feature_status`
  - `check_baremetal_only --check` and its selftest
  - `gen_toc --selftest`, `--verify-anchors` and `--check`
  - `check_gptp_docs`
  - `check_solution_docs`
  - `DOC_MAP.gen.py --check`
  - `check_archive`
  - `check_doc_paths`: 1,084 paths
  - `gen_module_matrix --check`
  - `git diff --check 1f29f189 e7310e94`
- **Renderer:** the Markdown renderer was installed from the pinned, hash-checked list into a disposable environment.
- **Author packet, author-r7:**
  - All 113 published files match `published_sha256` in the evidence tree's `MANIFEST.json`.
  - The 16 files that differ from the packet's `SHA256SUMS` are the manifest's path-redacted ones, and their `original_sha256` values equal `SHA256SUMS`.
  - All 50 gate rc files read 0.
  - `gate_1_hdl_reference.log` names the head.
  - Builder leg 1 reads "ALL GATES PASS EXCEPT 16 NOT RUN", by its own rules, and those 16 are not evidence.
  - The evidence commit `e05c8af5` carries no signature, so this rests on digests alone.
- **PR body:** the live body equals the packet's `PR-BODY.md` apart from a final blank line.
- **Hosted, snapshot in `receipts/hosted_snapshot.txt`:** at exact head, `rtl-fast`, `docs-check`, `docs-check-no-git` and `docs-gates-0` to `docs-gates-2` had succeeded. Long contexts are skipped on this documentation-only head, so those skips are not execution evidence.
- **Clone state after the run:** HEAD and tree are exact; `git status`, including ignored files, is empty; index modes and blobs equal the head tree; the six gitlinks are unchanged (`receipts/delta_check.txt`).

## Ledger

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN (R758-7-R1 residue) | FR:306, FR:476, SE:224-234, SE:389, AP:60, AP:255, AP:276 against the owner decision | R758-7 | e7310e94fff7188c5800a94c03a3f0e4c7c1c024 |
| RTL | CLEAN | Delta name-status; SE:636-640, SE:657, SE:1183 | R758-7 | e7310e94fff7188c5800a94c03a3f0e4c7c1c024 |
| Robustness | CLEAN | SE:636-637, SE:1183; round-6 margin bands; `receipts/probe/` | R758-7 | e7310e94fff7188c5800a94c03a3f0e4c7c1c024 |
| Tests | CLEAN | FR:306 verification, SE:1159; `receipts/gates/`; author-r7 gate receipts; `receipts/probe/` | R758-7 | e7310e94fff7188c5800a94c03a3f0e4c7c1c024 |
| Docs | CLEAN (R758-7-R1 residue) | Three changed pages; live PR body; list, pointer and table checks in `receipts/delta_check.txt`; `receipts/gates/` | R758-7 | e7310e94fff7188c5800a94c03a3f0e4c7c1c024 |

Text the delta does not touch keeps its prior lens verdict from the earlier R758 rounds.

## Real limits

- **Scope:** this is a delta review, as assigned. I did not re-derive the bounds or the earlier rounds.
- **The search behind S1 is a random walk,** 300 walks of 300 steps per rate, no CRF. Totals add the page's fixed terms for that rate, using the 16-reservation terms. They are estimates, not measurements. At 192 kHz the lower figure leaves out packetizer delay; the 131.754 µs upper figure in the receipt adds the largest 16-stream packetizer term, which I do not expect with two streams.
- **Not run by me:** the builder legs, the SDK and firmware-compiler gates, the submodule documentation gates, the remaining ratchets and the docs-check union step. For those I rely on the author's receipts, apart from the union step, which the author also did not run.
- **Independence:** my verdict and pass were recorded in `receipts/own_pass_before_priors.txt` before I opened the R757-6 and R758-6 reports. Before that I had seen the author's packet and fragments of the PR body's closure rows, which quote the residue texts. I did not read any R757-7 text.
- **Clause texts:** none opened. The delta changes no clause claim.
- **Hardware:** physical calibration NOT RUN and field skips are not hardware proof. Every latency figure here is derived.

## Pending manager duties

- Carry R758-7-R1 to the residue checklist.
- Carry S1 to S3, with R758-6 S1 to S4, to lane 6's handoff.
- Build and validate the current-dev merge candidate. Live dev was `1f29f189` at this review.
- Accept the hosted and local-replica evidence.
- Confirm the second independent review. The other open owner decisions stay open, as the owner states.

R758-7 FINISHED
