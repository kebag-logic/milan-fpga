[R757] NEGATIVE - exact head e7310e94fff7188c5800a94c03a3f0e4c7c1c024

# R757-7: internal cleared-context review of PR #828 (issue #640), round 7

Scope: delta `3f5fea24..e7310e94` (2 commits, 3 pages, +24/-24), tree `0a9f7f6a5b8d385fc43116ba0035d384b125b8c7`. The owner's decisions of 2026-11-01 are taken as final and are not reviewed.

Path keys: SE = `docs/design/MARK_II_STREAM_ENGINES.md`, FR = `docs/reference/FR_NFR.md`, AP = `docs/design/MARK_II_AREA_PLAN.md`.

## Verdict

- **One MINOR blocks: R757-7-F1.** The delta makes "its published bound" the pass rule for NFR-LAT-03, and says the fewer-reservations bounds are published. They are not: the page publishes four example rows, eight-channel at 48 kHz only, and legal cases exceed all of them.
- A reachable case at 48 kHz totals **143.347 µs against the largest published 123.337 µs**. Six one-channel streams reach it using only starts and stops.
- The decision itself is not disputed. Only the bound it accepts has to exist.
- Assigned checks 2, 4, 5 and 6 hold. Check 3 holds apart from two wording residues. Check 1 holds for every case that has a published bound.
- Two RESIDUE items and two SUGGESTIONS are recorded.

## Findings

### R757-7-F1 MINOR - Conformance, RTL, Robustness, Tests, Docs - FR:306; SE:230-231, SE:404-409; AP:60; AP:255; PR body "Fewer reservations are worse" - no bound is published for fewer reservations, so the new pass rule cannot judge those cases

**Authority and evidence**

- FR:306 (new): "Those derived bounds are accepted and published" and "a case above 65 µs that stays inside its published bound is not a failure". SE:230-231 (new): "Derived bounds for mixed formats and fewer reservations are accepted. They stay published below."
- The owner's decision accepts "the derived bounds ... for fewer reservations". The author's handoff (line 51) reasons: "The bounds are upper limits, so such a measurement would contradict the analysis".
- That holds for the 16-reservation table, which has "at most" figures. It does not hold for fewer reservations:
  - SE:404-409 is headed "Running eight-channel streams at 48 kHz, no CRF" and gives four rows. No row or sentence calls any of them a maximum.
  - FR:306 quotes only "123.337 µs with three co-phased eight-channel streams". The PR body says the same.
  - SE:414 gives "about `(k - 1) x 125 / k` µs" for k co-phased streams. It states no largest k, and it does not cover unequal frames.
- Probe results, each reached under the exact phase rule by starts and stops. All totals use the page's own fixed terms:

| Rate | Running streams | Shaper wait, µs | Total, µs | Nearest published figure |
|---|---|---:|---:|---|
| 48 kHz | Six one-channel, phase 0 | 103.022 | **143.347** | 123.337 |
| 48 kHz | Two: eight-channel in phase 0, one-channel in phase 1 | 71.310 | 111.635 | 102.584 and 81.750 are the two-stream rows above 65 µs |
| 96 kHz | Four one-channel, phase 0 | 92.935 | 125.426 | No fewer-reservations row; the 16-reservation limit is 93.216 |
| 192 kHz | Two: six-channel, one-channel, three phases apart | 83.941 | at least 102.034, before the packetizer term | No fewer-reservations row; the 16-reservation limit is 100.825 |

- 48 kHz witness sequence: start N=1, then five N=8, then two N=1, then five N=8, then three N=1. That is 16 streams, placed `[1x6], [8,8] x 5`. Then stop every N=8.
- Calibration: the probe reproduces all four SE rows and the 53.085 µs mix to three decimals.
- The published model agrees. Its own `greedy_add` reaches the 48 and 96 kHz placements in the table, and its `lindley_wait` and event-exact `cbs_sim` give 103.022, 71.310 and 92.935 µs.

**Why the delta caused this, and why it is not wording**

- At `3f5fea24` the row said the requirement was "not met" and the reading was an open question, so 123.337 µs was only an illustration.
- The delta makes the published bound the acceptance line, so what was an example now has to be a limit. An earlier round's figure is not re-opened; its new use is.
- The fix adds a figure or a verification rule, so this is not RESIDUE.

**Impact**

- A case at 143 µs is either a false failure, because it is above every published figure, or undefined, because the requirement says nothing for a case with no published bound.
- The "A" half of the requirement's A,T does not cover this class. The derivation states it does not show the bound for these cases, and the published model searches 16 reservations.
- The figure placed before the owner understates the known worst case by at least 20 µs.
- Bench reach is narrower than the text suggests. FR:306 and SE:1159 name only one-format and mixed-format runs at 32x32, so no named bench run exercises fewer reservations. The defect is in the analysis half and in the published claim; no RTL exists yet.

**Required outcome** (either one)

- (a) Publish a derived upper bound for fewer reservations at each rate, over every reachable placement and base format. Cite it at FR:306, SE and in the PR body in place of the three-co-phased example. The 48 kHz figure cannot be below 143.347 µs.
- (b) State at FR:306 and SE:230-231 that the rows are examples and that no fewer-reservations bound is derived, and name who derives it. State what the bench does with a case above 65 µs that has no published bound. Keep "no connection is refused" either way.

The manager tells the owner the larger figure with either outcome. The decision is not re-opened.

**Verification:** re-run `scripts/probe_fewer_bound.py` and `scripts/crosscheck_published_model.py`. Each witness must fall inside a published bound, or must be covered by the stated rule for a case with none.

### RR12 RESIDUE - Docs - AP:276 - the lane 6 evidence cell reads as a 65 µs pass line

- **Authority and evidence:** the cell reads "65 µs taps on all talker streams". The target row and FR:306 now make 65 µs a target. AP:276 is the one repository line that reads as a limit with no "target" beside it. It names no pass rule, and the delta did not touch it.
- **Impact:** a lane reader could take 65 µs as lane 6's acceptance line.
- **Exact fix:** "Latency taps on all talker streams, against the 65 µs target".
- **Verification:** read the row against FR:306.

### RR13 RESIDUE - Docs - issue #640 body, "Acceptance (2026-10-31)" and "What 32x32 requires" - the frozen text still reads as binding

- **Authority and evidence:** the body says "Every talker stream meets the 65 µs target, measured on the bench", and "so the class-A shaper does not hold the last stream past the 65 µs target". The owner's decision comment on the same issue supersedes both, but the body does not say so. A cold reader checking section 7's "all acceptance criteria are met" would read mixed formats as unmet.
- **Impact:** the completion check depends on finding a later comment. No figure, test or requirement changes.
- **Exact fix (manager, on the issue body):** below the acceptance line add "Superseded for mixed formats and fewer reservations by the [owner decision of 2026-11-01](https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-6558021030): 65 µs is a target, per NFR-LAT-03."
- **Verification:** read the issue body.

### R757-7-S1 SUGGESTION - Tests, Docs - FR:306, SE:1159 - name the fewer-reservations case on the bench

The accepted bounds cover fewer reservations, but the named bench runs do not. If F1 takes outcome (a), one bench case at the largest derived placement would test that bound.

### R757-7-S2 SUGGESTION - Docs - FR:329, FR:339-340 - `T_svc` still reads as awaiting approval

- FR:340 says "Owner approval of this value is required before merge". The owner approved "the NFR-SCOUT-02/03/05 amendments", which may or may not include this value. Both lines are already on `dev` and the delta does not touch them, so this is out of scope and no finding.
- The manager can ask whether the approval covers `T_svc`.

## Assigned checks

| # | Check | Result | Evidence |
|---|---|---|---|
| 1 | NFR-LAT-03 states a target, bounds accepted, no connection refused, verification sound | Text as decided. Verification sound where a bound exists; **F1 where none does** | FR:306 reads "SHOULD be below 65 µs, and as short as possible", priority S (the file's key at FR:20), method A,T kept. The accepted and refused sentences match the decision. For one format and mixed formats at 16 reservations, the rule decides every case against the table's limits |
| 2 | Question 1 gone, decision stated once, tables unchanged, renumbered, pointers land | Holds | SE:1227-1248 numbers save bursts to engine headroom as 1 to 6. The decision appears once, SE:227-234; SE:389 links to it. Hashes of the 16-reservation and fewer-reservations tables match across both heads (`receipts/bounds_tables_sha.txt`). No numbered reference to a question exists in the docs. PR-body pointers land: open question 6 is engine headroom, and the save-bursts limitation is question 1 |
| 2a | The pointer left unchanged on purpose | Reasoning correct | SE:1148-1152 follows "A burst beyond S1" and refers to the save-bursts question, which stays open as question 1. It was never a pointer to the latency question. `#open-questions` appears only at SE:27 and SE:1152 |
| 3 | No line presents 65 µs as binding, or the mixed result as awaiting the owner | Holds in the repository, except RR12; issue body is RR13 | Searched docs, `REQUIREMENTS.md`, scripts and tests for 65 µs, "talker latency", "pin to wire" and "mixed". "Against 65 µs", "Not met" and `SE_TLAT_OVER` compare with the target and pass no judgement. No "MUST be below 65" remains, and no latency item remains in AP's open decisions |
| 4 | Area plan rows agree | Holds, with F1 inherited | AP:60 and AP:255 agree with FR:306 and SE:227-234 on target, the 16-reservation condition, acceptance and no refusal. "Bounds" in both carries F1. The earlier rule that "one format meets it" must carry "16 reservations" still holds at SE:19, SE:388, FR:306, AP:60 and AP:255 |
| 5 | Residue RR11 and R758-6-R1 | Both closed in substance, not verbatim | See "Prior findings" |
| 6 | Nothing else changed; docs gates pass | Holds | Three modified pages only, modes unchanged, two one-line commits with no body (`receipts/integrity_and_delta.txt`). Gates under Tests |

## Prior findings

- **RR11 (mine, round 6): resolved.** SE:636, SE:1183 and the PR limitation all now say both networks.
- **R758-6-R1 (other reviewer, round 6): resolved.** SE:637, SE:1183 and the PR limitation say the threshold is approximate and carries the conversion error. SE:1183 states the partial band, "within that error of 125 µs, only some packets lapse", which matches that report's arm A figures.
- **Not verbatim, and acceptable.** The two prescribed texts differ, so the author merged them and said so in the PR body. "Both copies' margins under about 125 µs" is equivalent to the other report's "first-copy margin", since the first copy has the larger margin. The word "about" carries its "well under".
- **Paragraph move at SE:639-640.** Both sentences are unchanged and "that case" still names the interleaving.
- **R757-2 RR1 row:** the PR body now records the renumbering correctly.
- **R757-6 S14 to S16 and R758-6 S1 to S4:** optional and not taken. They stay suggestions.
- Earlier rounds' findings are not re-opened. Apart from F1's change of what the 123.337 µs figure is used for, the delta breaks none of them.

## Lens results at this head

Each lens carries F1, so none is clean. What else each lens checked:

- `[R757] UNCLEAN Conformance - FR:306, SE:224-234 against issuecomment-6558021030 - target, acceptance and no-refusal text match the decision; the pass rule fails on cases with no bound (F1).`
- `[R757] UNCLEAN RTL - SE:182-217, SE:404-414, receipts/model/ - no RTL or register changed, and SE_TLAT_OVER keeps its meaning against the target; the phase rule's worst fewer-reservations latency is not bounded on the page (F1).`
- `[R757] UNCLEAN Robustness - SE "What the rule cannot prevent" and "Fewer reservations", receipts/model/probe_fewer_bound.out - legal start and stop sequences reach cases above every published row (F1). The SE:636-640 and SE:1183 margin text is correct against the prior receipts.`
- `[R757] UNCLEAN Tests - FR:306, SE:1159, scripts/probe_fewer_bound.py - the new verification sentence cannot decide this class, and no named bench run reaches it (F1). No executable test changed; gates pass.`
- `[R757] UNCLEAN Docs - FR:306, SE:230-231, AP:60, AP:255, PR body - the claim that the bounds are published is untrue for fewer reservations (F1). Links, anchors and numbering are correct.`

## Tests and gates

- **My runs at the head, all rc 0** (`receipts/gate_*`):
  - `docs_check.py`: 0 findings over 213 pages and 1,436 scrubbed files
  - `check_doc_style.py`, plus `--selftest`
  - `check_doc_paths.py`: 1,084 paths
  - `check_solution_docs.py`, `check_submodule_docs.py`, `check_gptp_docs.py`
  - `check_em_dash.py --base 1f29f189`: 0 findings over 1,754 added lines, using the hash-pinned renderer in a scratch environment
  - `gen_toc.py --check` and `--verify-anchors`: 579 links
  - `gen_module_matrix.py --check`: 80 modules
  - `check_feature_status.py`, `DOC_MAP.gen.py --check`
  - `git diff --check` against the base
- **Author's published gates:** all 50 `.rc` files under `author-r7/evidence/gates` read 0. `HANDOFF.md`, `PR-BODY.md` and `SHA256SUMS` match the published `MANIFEST.json` digests. The evidence commit's digests are the basis; I did not check for a signature. The live PR body matches the packet apart from one trailing blank line.
- **Probes:** `scripts/probe_fewer_bound.py` (seed 640; rc 0) and `scripts/crosscheck_published_model.py` (rc 0), outputs in `receipts/model/`.
- **Comment rule:** the delta touches prose tables and text only. It adds no source comment and no lane, round or reviewer label to a source comment.
- **Clone state:** no tracked file was modified. Head and tree match, the index and working tree match the head, and tracked blob and mode digests match between tree and index. All six gitlinks are recorded in `receipts/gitlinks.txt`. The only side effect of my runs was an ignored `scripts/__pycache__`, which I removed.

## Completion ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1) | FR:306, SE:224-234, the owner's decision comment, issue #640 body | R757-7 | e7310e94fff7188c5800a94c03a3f0e4c7c1c024 |
| RTL | UNCLEAN (F1) | SE:182-217, SE:404-414, SE:442, SE:754-757, probe and cross-check outputs | R757-7 | e7310e94fff7188c5800a94c03a3f0e4c7c1c024 |
| Robustness | UNCLEAN (F1) | SE:636-640, SE:1183, phase-rule witnesses, random walks at all three rates | R757-7 | e7310e94fff7188c5800a94c03a3f0e4c7c1c024 |
| Tests | UNCLEAN (F1) | FR:306 verification, SE:1159, gate receipts, author's gate rc files | R757-7 | e7310e94fff7188c5800a94c03a3f0e4c7c1c024 |
| Docs | UNCLEAN (F1) | The 3-page delta, SE and PR-body pointers, AP:60, AP:255, AP:276, PR body, gates | R757-7 | e7310e94fff7188c5800a94c03a3f0e4c7c1c024 |

RR12 and RR13 are RESIDUE and leave no lens unclean. Each lens must be covered again at the head that answers F1.

## Real limits

- The witnesses are lower bounds. I show cases above the published rows, not the true maximum at any rate. The random walks are a sample, not a search of every state.
- The 192 kHz search omitted N=8, so that rate's figure may be low. Its total also excludes the packetizer term, which the page treats as a queue at that rate.
- Totals use the page's fixed terms, including its estimates. Nothing here is a measurement.
- I did not re-run the builder legs, the bare-metal scope gate, the SDK or compiler steps, the gate selftests other than `check_doc_style`, or the wavedrom and PNG gates. Those rest on the author's rc files.
- Physical calibration was not run and field skips are not hardware proof. This is a documents delta.

## Pending manager duties

- Route F1 to the author, and tell the owner the larger figure.
- Carry RR12 to the residue checklist, and apply RR13 on the issue body.
- Own hosted and act acceptance. At read time the PR's checks showed 19 pass, 3 pending and 22 skipping. I draw no conclusion from them.
- Build and validate the current-dev merge candidate at the merge turn; no manager source bank exists at this head. Source base and live dev are both `1f29f189279f9fc0132f4918e47342b87d22f33a`.
- Obtain the second independent review. Merge needs explicit maintainer authorization.

R757-7 FINISHED
