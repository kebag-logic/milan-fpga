[R625] POSITIVE - exact head f1b2489f5b1c929e81eeae79a469b2b27c47e340

All five lenses are CLEAN for the B16/B16b/B16c findings-only scope of issue #629 / PR #725. No BLOCKER, MAJOR, MINOR or new RESIDUE remains. Earlier findings and residues are resolved below. This verdict does not close issue #629 or authorize a merge.

The reviewed tree is `635001816412f045f479ec4776fe641969a48815`. The complete diff from `c20c85bd` changes only `docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md` and `docs/findings/README.md`. Here, `findings:N` means the former file at line N, `index:N` means the latter, and `packet/` means `author-r10/` in the [published evidence at 5775cfa78dc9250ea1b689fc2cfa8e20c41281bb](https://github.com/kebag-logic/milan-fpga/tree/5775cfa78dc9250ea1b689fc2cfa8e20c41281bb/review-evidence/629-b16-r1). Reviewer receipts are relative to this report.

Reconstruction followed AGENTS.md / CONTRIBUTING.md, docs/README.md, the issue's frozen acceptance and public decisions, linked requirements and interface authorities, the full diff and history, then executable evidence. An independent verdict and five-lens ledger were written before reading earlier public review findings. No other reviewer's report supplied that independent verdict. The later reconciliation used the public PR comments. The formal-review and inline-comment collections were empty when checked.

Scope authorities include the [B16 assignment](https://github.com/kebag-logic/milan-fpga/issues/629#issuecomment-6117305187), [B16b ruling](https://github.com/kebag-logic/milan-fpga/issues/629#issuecomment-6117672835), [B16c peer-INTERNAL exception](https://github.com/kebag-logic/milan-fpga/issues/629#issuecomment-6118365090), [diagnostic-expectation decision](https://github.com/kebag-logic/milan-fpga/issues/629#issuecomment-6132293481), and [round-10 assignment](https://github.com/kebag-logic/milan-fpga/issues/629#issuecomment-6134101205). Technical authorities were REQUIREMENTS.md, `docs/reference/FR_NFR.md:252`, `:253`, the bench acceptance and limits in `docs/design/MEDIA_CLOCK_FOLLOWING.md`, and `docs/reference/REGISTER_MAP.md:1870`, `:1871`, `:2076`, `:2139`.

[R625] PASS Conformance - findings:2287, :2423, :2673, :2829, :3198, :3244, :3331; index:15; packet/runs, packet/summary and packet/r2 - the measurements and qualifications satisfy the authorized findings scope and preserve the unrun acceptance terms.

- B16's loopback did not form. The second run contains two outgoing PROBE_TX/CONNECT_TX commands and no corresponding response. Independent timestamp subtraction gives 99.616 ms and 299.631 ms from the unbind command. The findings and current PR body use that origin and do not claim a DUT audio-transport defect.
- B16b distinguishes the four capture points and their finite overlap. B0 has 169 floor blocks out of 300, floor medians -123.98/-123.95 dB, and all-block medians -123.95/-122.80 dB. The degraded runs split at block 45. Recording starts about 06:38:05.2, including the two-second playback lead, about 26 seconds after binding. Of 131 degraded blocks, 23 lie wholly inside the shared 34.1136-second sample comparison; attribution of the other 108 is explicitly inference in the findings, index and PR body.
- B-CRF and B-AAF each have 300/300 floor blocks and no reported discontinuity. Each has 596 complete window polls reading LOCKED. The state-read brackets are 2.585-3.161 s and 6.602-7.180 s, bounded by the last ACQUIRE poll's start and first LOCKED poll's end. The four point-(a) medians in the exact replacement at findings:3244 independently recompute to -123.98/-123.97 and -123.98/-123.98 dB; every worst block is -123.93 dB.
- The positive controls exclude the two silent pre-playback blocks and the transition block. The external capture counts reproduce as 11/13 wholly playing floor blocks for `pts2` and 303/303 for B0 and each following case. The published tap counts are included in the passing figure rows.
- All eight clock-source SET operations have successful matching readbacks, including both DUT and peer restorations in each following case. All nine run snapshots restore the recorded formats, bindings, maps and clock sources. Each lane census has 44 equal reads out of 45, excluding its start record; the differing read is live propagation delay. The first counter marks are 20.019/20.016 s after selection and 6.005/6.004 s before recording, as stated.
- All four B6 terms are stated at findings:3198. The timed ratio is NOT RUN, with no decision replacing it. Direction B's INTERNAL mismatch control is also NOT RUN; B0's peer followed the DUT. The peer-INTERNAL exception is restricted to B-CRF/B-AAF. Source routing and clock changes outside the lane are attributed to their source, with state comparisons bounded to their common entries.

These arithmetic and restoration checks are independently recorded in `receipts/receipt-audit.json`; they do not import the figure checker's expressions. They use published reduced receipts, not a new hardware capture.

[R625] PASS RTL - complete two-file diff and history; REGISTER_MAP:1870, :1871, :2076, :2139; packet/r2/bcrf-poll-trace.tsv and baaf-poll-trace.tsv - documented DUT observations agree with the unchanged interfaces and register semantics.

No implementation, interface, generated hardware artifact, configuration or gitlink changes in this diff. Both 710-row poll traces were examined against the state, signed trim and slip-counter definitions. The selected-source indices agree with FR-CLK-03/04. Complete measured windows stay LOCKED; TDM slip words remain zero; loopback slip transitions occur in IDLE before selection or ACQUIRE, with none after LOCKED in the measured interval. Static nonzero loopback counters are not described as cleared counters or saturated-counter proof. The page records status bit 4 as observed but not analysed. This is a review of the claimed observations, not an implementation-wide RTL revalidation.

[R625] PASS Robustness - packet/tools/check_b16_figures.py:2712, :2760, :2780, :2859, :2888; findings:4134, :4297, :4426; controls and probe receipts - malformed markup, source extents, missing positions and dropped digits fail with usable diagnostics.

The reader uses the repository's hash-locked documentation parser and HTML parser. It judges visible inline text, applies the closed node allowlist, and refuses other constructs at the first covered line reached by their actual extent. Exact generator markers are the only raw-markup exception. Whole-quote/whole-link exemptions and handwritten comment/markup stripping are absent from this reading path. Digit coverage is per character; row claims and keyword-bound identifiers are distinct. Joined units, unusual whitespace, signs, leading decimals, exponents and unfamiliar direct unit words cannot silently become identifiers.

The round-10 start-position rule refuses the whole block when a relevant node or enclosing structure lacks a valid start. A separate comparison requires each covered block's rendered digit multiset to equal the digits judged. The 15 parser-output mutations meet all expectations, including lost, duplicated and substituted digits and missing starts on other node kinds. The parser-extents audit meets all 37 earlier and 22 zero-position cases. The unchanged autolink probe passes its original page and rejects all 14 altered cases. Email forms refuse the introduction at line 18, section paragraphs at line 2301, and the index at line 15, as required by the first-covered-line rule; positioned later-line forms name their figure at line 2302. The probe's label FAILED_OTHERWISE denotes these receipt-backed block refusals, not an escape.

My 23 additional probes all reject at their edited line, write both receipts and produce no checker traceback. They include Unicode numerals, a NUL separator, a keycap sequence, a linked image, a collapsed-reference image, entities, raw tags, short comments, an address after code, and emphasis. See `probe_independent.py` and `receipts/independent-probes.json`.

[R625] PASS Tests - packet/tools/check_b16_figures.py and r10_figures_spec.py; receipts/figures-rows.tsv, figures-coverage.tsv, controls-r3.json through controls-r10.json, and all fifteen *probe-rerun.json receipts - baseline figures, defect sensitivity and historical outcomes are reproducible at this head.

The unchanged page passes all 1,960 rows. It accounts for 15,597 digits: 12,988 in row-claimed figures and 2,609 in identifiers, with zero uncovered digits and zero markup refusals. Both output TSVs are byte-equal to the published outputs. The rebuilt checker is byte-identical, 199,268 bytes, SHA-256 `a9f36f9d9ff3bfd6c7f7ce86f64ef1ac9531f1cf594d68d3a06437f8e8d0e540`.

| Unchanged control runner | PASS / total | Interpretation at this head |
|---|---|---|
| Round 3 | 5 / 5 | All pass |
| Round 4 | 7 / 8 | Superseded link-label diagnostic |
| Round 5 | 21 / 22 | Same inherited diagnostic |
| Round 6 | 38 / 39 | Same inherited diagnostic |
| Round 7 | 48 / 50 | Link-label diagnostic and literal comment inside code |
| Round 8 | 73 / 73 | All standing expectations pass |
| Round 9 | 97 / 97 | All standing expectations pass |
| Round 10 | 117 / 117 | All standing expectations pass |

Historical failures remain explicit. Decision 6132293481 accepts precisely those two diagnostic changes; both altered pages still exit 1, name the digit at its source line and write receipts. No historical runner was rewritten to claim a pass.

All fifteen published review probe scripts were rerun unchanged, with their hashes verified by the runner. In particular: R625-3 detects 7/7, R624-4 detects 8/8, R625-4 detects 12/12; both independent line-3200 mutations fail the affected row; the multiline-comment probe returns [0,1,1]; the short-comment probe returns [0,1,1,1,1,1]. That last frozen script itself exits 1 because its final assertion deliberately states the old defective result; its six check outcomes are the required corrected result. R624-7's image forms reject; all four R625-7 index markup cases write both receipts without exceptions; R624-8's `<pre>` from the line above is refused as `MARKUP ...:18 html_block`. The appended footnote moves to line 4604 at this longer page. The 172 further published forms meet all stated expectations: 134 reject and 38 pass under the documented model.

Earlier exploratory probes retain their stated limits. R624-5's 21/25 detections leave the colon-separated identifier and three digitless phrases outside the rule. R624-6's broader expectations for four forms do not all pass; allowed follower words and the invisible list marker account for their retained results. These are not concealed as universal rejection. Exact observations are in the unchanged probe receipts.

Focused local checks passed: `git diff --check c20c85bd HEAD`, documentation structure, style, generated contents, added em-dash policy and document paths. `receipts/commands.json` records commands, return codes and durations; each command has a log and return-code receipt. The published source-head gate record separately contains 14 successful entries, including interpreter identity checks, at this exact head. That is author evidence; it is not a manager source bank.

[R625] PASS Docs - findings:2608, :3426, :3764, :4201, :4343, :4426; index:15; current PR title/body; publication manifests - the public account, evidence locations, privacy limits and amended expectations match their receipts.

The location paragraph names the evidence branch, pinned commits, historical author directories and manifest, including the added later rounds. The historical round-4 manifest has the stated 1,680 entries and SHA-256 `8d417d54b13a264484bfcb0b69f8a643e5cd3bf2819294cea201242a2f67f034`; its 66 figure-table hash rows match the published files. The current manifest has 7,731 entries; all 937 author-r10 published file hashes match, original hashes agree with the author's manifest, and all 114 current page hash rows match original hashes, published hashes, bytes and sizes. Path-redacted files are distinguished explicitly. See `receipts/historical-evidence.json`, `evidence-receipt.json` and `receipt-audit.json`.

Neutral reduced receipts expose extrema, timestamped slip transitions with servo states, source meters and bounded state comparisons. The two poll reductions and twelve source reads are bound to raw hashes; the extraction procedure is published. Withheld raw source reads and mapping were not regenerated. The reviewed additions and PR summary name the peer and external capture by role and contain no host paths. The title distinguishes graded B0 from the following cases at the path's floor. The current body retains “99.6 ms after the unbind command” and the historical “line 4426” locator; it also uses the corrected statuses/verdicts/named-lines wording. `receipts/public-claims.json` records those public claims and their provenance.

Earlier public findings were reconciled after the independent pass. Every row below is a current-head determination; no defect was closed merely by moving it to another issue.

| Earlier ID(s) | Original attributable lenses | Current disposition and evidence |
|---|---|---|
| R624-1-F1; R625-1-F3 | Conformance, Tests, Docs | RESOLVED: B0 floor medians, interrupted runs and playback-adjusted recording start; findings:2673, :2788; receipt-audit.json |
| R624-1-F2; R625-1-F4 | Conformance, Tests, Docs | RESOLVED: all four B6 terms with timed ratio NOT RUN; findings:3198; index and PR body |
| R625-1-F1 | Conformance, Tests, Docs | RESOLVED: 23 observed degraded blocks versus 108 inferred beyond overlap; findings:2829, :3259; index and body; independent arithmetic |
| R625-1-F2; R624-1-S2 | Tests, Docs | RESOLVED / TAKEN: neutral reduced receipts, raw hashes and extraction procedure; findings:3426; packet/r2 |
| R624-1-R1/R2; R625-1-R1/R2 | Docs | RESOLVED: exact title and counter-mark wording; public-claims.json; findings:3040, :3172; receipt-audit.json timing |
| R624-1-S1; R625-1-S1; R624-2-S2; R625-2-S1; R625-3-S1 | Docs | TAKEN: 44/45 reads excluding the header; findings census statements; independent census comparison |
| R625-2-F1 | Conformance, Tests, Docs | RESOLVED: exact point-(a) replacement at findings:3244; four medians and worst values recomputed |
| R624-2-F1 | Robustness, Tests, Docs | RESOLVED: playing-block counts exclude silent/start blocks; independent 11/13 and 303/303 counts |
| R624-2-F2 | Tests, Docs | RESOLVED: state-read brackets use the preceding poll's start; both traces independently decoded |
| R624-2-R1/R2/R3 | Docs | RESOLVED: common-entry limits, qualified pre-selection slip attribution, explicit missing INTERNAL mismatch control; findings:2788, :3214, :3261 and body |
| R624-2-S1 | Docs | TAKEN: status bit 4 recorded without analysis; findings:3341 |
| R624-3-F1; R624-5-F3 | Docs | RESOLVED: branch, pins, round directories and manifest at findings:2608; both publication audits |
| R625-3-F1 | Conformance, Robustness, Tests, Docs | RESOLVED: quoted/linked figures covered; unchanged 7/7 probe and own quote/link probes |
| R624-4-F1; R625-4-F1 | Conformance, Robustness, Tests, Docs | RESOLVED: per-digit coverage and unit/spelling forms; unchanged 8/8 and 12/12 probes |
| R624-4-S1 | Docs | TAKEN: opening pointers include subsequent rounds; findings:2289 |
| R624-5-F1 | Conformance, Tests | RESOLVED: each case reads its own receipt. Numerator and denominator mutations each fail their own line-3200 row; unchanged values properly remain OK |
| R624-5-F2 | Conformance, Robustness, Tests, Docs | RESOLVED: unfamiliar direct unit words reject under the closed follower rule; unchanged escape probe and own furlongs probe |
| R624-5-R1 | Docs | RESOLVED: exact channel/step/round and issue-number wording; findings:3764, :3770 and body |
| R624-5-S1; R624-6-S1 | Tests, Robustness | TAKEN as documented limits: approximate quantities after allowed follower words and other out-of-model phrases; self-probe receipts |
| R624-6-S2 | Docs | Technical condition satisfied: the two affected line-3200 rows fail separately under their own receipt mutations. Any optional manager acknowledgement is administrative |
| R625-5-F1; R625-6-F1 | Conformance, Robustness, Tests, Docs | RESOLVED: multiline/short comments and tags refuse at their lines; unchanged probes, with the frozen assertion exit recorded above |
| R624-7-F1; R625-7-F1 | Conformance, Robustness, Tests, Docs | RESOLVED: image forms refuse; four index cases have named diagnostics, receipts and no traceback |
| R624-8-F1 | Conformance, Robustness, Tests, Docs | RESOLVED: actual HTML-block extent reaches the first covered line; unchanged edge probe refuses at line 18 |
| R624-8-S1 | Docs, Tests | TAKEN as stated limits: emoji shortcodes and link-title tooltips; findings:4401 |
| R625-8-F1 | Conformance, Tests, Docs | RESOLVED by decision 6132293481, applied beside historical outcomes; findings:4201, :4230, :4343 and body; old failures retained |
| R624-9-F1 | Conformance, Robustness, Tests, Docs | RESOLVED: missing source starts refuse whole blocks; rendered digit conservation is independent; unchanged autolink probe, 117 controls, 15 reader mutations and 22 zero-position cases |
| R624-9-R1; R625-9-R1 | Docs | RESOLVED: statuses/verdicts/named-lines wording and historical line 4426; public-claims.json |
| R625-9-F1 | Docs | RESOLVED: delay origin is unbind; independent 99.616 ms subtraction and current public body |

Reviewer-owned completion ledger:

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Frozen issue rulings; FR_NFR:252-253; findings:2287, :2829, :3198, :3244; packet/runs, summary, r2; receipt-audit.json | R625-10 | f1b2489f5b1c929e81eeae79a469b2b27c47e340 |
| RTL | CLEAN | Complete two-file diff/history; REGISTER_MAP:1870, :1871, :2076, :2139; both poll traces; checkout-integrity.json | R625-10 | f1b2489f5b1c929e81eeae79a469b2b27c47e340 |
| Robustness | CLEAN | Checker:2712, :2760, :2780, :2859, :2888; 117 controls; fifteen prior probes; 172 further forms; 23 own probes; reader-controls.json; parser-extents.json | R625-10 | f1b2489f5b1c929e81eeae79a469b2b27c47e340 |
| Tests | CLEAN | 1,960 rows and per-digit coverage; controls r3-r10; unchanged probe hashes/results; rebuilt checker; focused gates and published source gates | R625-10 | f1b2489f5b1c929e81eeae79a469b2b27c47e340 |
| Docs | CLEAN | Full findings diff; index:15; PR title/body; location paragraph; reduced receipts; both publication manifests; public decisions and prior-finding reconciliation | R625-10 | f1b2489f5b1c929e81eeae79a469b2b27c47e340 |

Reproduction uses the repository's hash-locked documentation environment. `run_checks.py REPO AUTHOR_PACKET OUTPUT --jobs 8` runs the baseline, historical/current controls, fifteen review probes, further forms, reader mutations, parser extents and focused gates, awaiting every child. `probe_independent.py REPO AUTHOR_PACKET OUTPUT` runs the additional probes. `audit_receipts.py REPO AUTHOR_PACKET MANIFEST OUTPUT` independently checks publication, arithmetic, timing and restores. `verify_checkout.py REPO OUTPUT_JSON` checks tracked blob bytes, modes, index and required submodule pins. Auxiliary commands and return codes are in `receipts/auxiliary-commands.json` and adjacent receipts. Paths in receipts use neutral placeholders. Disposable trees are excluded from publication; MANIFEST.sha256 lists every publishable receipt and script.

Final containment is clean. All 1,291 parent tracked blobs and all tracked blobs in the three required submodules match their committed bytes and modes; every index matches its tree. Required gitlinks and checked-out heads are `gptp-processor` at `5dce647ab5a01a6ecff9a982b22e3a4a1d946d3d`, `protocol-processor` at `2ad2f845dd583f8310075fa2380cb60a04fd091a`, and `third_party/verilog-axis` at `48ff7a7e2ef782cf778d47910cf85835c64b1bce`. Parent and required-submodule status are clean. The two optional uninitialized gitlinks were verified in the parent index/tree, not populated. No source edit, commit, push, external write or bench action was performed. All child commands completed.

Limits remain real. No raw capture was re-recorded or re-graded; independent arithmetic starts from published per-block and poll reductions. Withheld source data cannot be regenerated from this public packet. The check follows the pinned parser's visible-text model, retains the expressly stated follower/phrase limits, compares digit multisets rather than positions, and may conservatively refuse a block whose isolated rendering differs from page context. These limits are stated on the page and exercised in retained probes. No new physical calibration was run. Field skips and an unrun INTERNAL mismatch control are not hardware proof, and the timed-ratio term remains NOT RUN.

The manager still owns hosted/local-replica acceptance, distinguishing executed jobs from skipped contexts, the other independent review, and final merge authorization. There is no manager source bank at this exact head, and none is claimed here. Author source-head receipts are distinct from the current-dev merge candidate. At the merge turn the manager must construct and validate that candidate against then-current dev (the supplied live tip is `d5858bbee328cf8d2c39a99ec14203f5d0ddd123`), run the required builder/native banks, publish their receipts on the PR, ensure no review remains in flight, and complete the repository's post-merge containment and issue/project duties where applicable. This report supplies only the R625-10 review verdict and ledger.

R625-10 FINISHED
