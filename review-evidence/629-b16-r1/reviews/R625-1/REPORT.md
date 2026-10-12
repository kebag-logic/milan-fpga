[R625] NEGATIVE - exact head e20fd2820a9c6b9effabc529a742e732263fafa8

Round R625-1, external independent review of issue #629 / PR #725.
Tree: `6299ec05fc1085b62defe945c9dc5c426e54d055`.
Source comparison: `c20c85bd..e20fd2820a9c6b9effabc529a742e732263fafa8`.

All five lenses were independently applied. Four MINOR findings remain open:
two found independently, and two retained after public-finding reconciliation.
Neither alleges a DUT implementation defect. Both affect evidence claims,
so neither qualifies as wording-only RESIDUE.

This independent verdict and ledger were written before consulting other
reviewers' findings. The three-commit diff changes two Markdown files only:
the dated findings and their index. It changes no RTL, firmware, executable
test, configuration, generated image or gitlink. The measured image is dev
`5603c353`, distinct from this documentation head.

## Scope and authorities

Read in the assigned order: `AGENTS.md`, `CONTRIBUTING.md`, `docs/README.md`,
the [issue contract](https://github.com/kebag-logic/milan-fpga/issues/629),
the [B16 assignment](https://github.com/kebag-logic/milan-fpga/issues/629#issuecomment-6117305187),
the [B16b ruling](https://github.com/kebag-logic/milan-fpga/issues/629#issuecomment-6117672835),
and the [B16c exception](https://github.com/kebag-logic/milan-fpga/issues/629#issuecomment-6118365090).
Technical authorities examined: `REQUIREMENTS.md` section 8;
`docs/reference/FR_NFR.md:252` (FR-CLK-03/04);
`docs/design/MEDIA_CLOCK_FOLLOWING.md:1661` and its clause findings;
`docs/overview/ARCHITECTURE.md:72`;
`docs/reference/REGISTER_MAP.md:1870`, `:2082`, `:2139`;
and `docs/testing/TESTING.md:924`.

Evidence paths below are relative to `author-r1/` in the immutable
[published packet](https://github.com/kebag-logic/milan-fpga/tree/724b0974304beddc80fcf5512061c8a588a76cfd/review-evidence/629-b16-r1).
All 471 publication hashes verified. All 92 newly documented hash/size rows
match retained files or the raw-artifact inventory. Inventory agreement
verifies the citation, not unavailable capture bytes.

## Findings

### R625-1-F1 - MINOR - Conformance, Tests, Docs

**Artifact:** `docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md:3157`;
also PR #725 body, B16b result, and the absolute upstream-attribution summary
in `docs/findings/README.md:15`.

**Finding:** B0's comparison assigns all 131 degraded blocks to the peer's
talker, although only 39 complete one-second blocks were captured there.

**Authority/evidence:** The B16b ruling requires stage attribution. The page
says the talker stream already held 131 off-floor blocks which reached the
DUT output unchanged. `summary/b0-2/a-peer-tap.json` contains 1,919,610 frames,
39.992 seconds, and 39 complete blocks per tone.
`summary/b0-2/c-b9-grade.json` contains 14,400,000 frames, 300 blocks,
169 at the floor, and 131 degraded blocks. That count belongs to point (c).
`summary/b0-2/align-a-c.json` establishes equality for 1,637,452 frames,
34.1136 seconds. The earlier B16b paragraph correctly says later blocks
are assigned upstream by their kind without sample comparison; the later
comparison and PR summary drop that qualification.

**Impact:** A measured output count becomes an unsupported input observation.
This overstates the duration of stage isolation and excludes later DUT or
network contributions more strongly than the retained data allows. The
central B0 measurements and observed overlap remain valid.

**Required outcome:** Keep 131 as the count at (c). State which upstream
impairments are directly demonstrated within the tap overlap, and label
attribution outside it as inference. Apply this consistently to the findings,
index and PR body. No hardware rerun is needed to correct the claim.

**Verification:** Reconcile those texts with the three receipts above.
`receipts/audit.json`, field `b0_attribution_boundary`, records the independently
checked counts and coverage.

### R625-1-F2 - MINOR - Tests, Docs

**Artifacts:** `docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md:3098`,
`:3123`, `:3168`, and its B16/B16b source-state sections;
published `runs/bcrf/events.jsonl`, `runs/baaf/events.jsonl`,
`RAW-ARTIFACTS.json`, and the publication manifest.

**Finding:** Several precise following and source-state figures lack a
reproducible public measurement receipt.

**Authority/evidence:** The review contract requires each figure to match a
receipt; `AGENTS.md` sections 1 and 6 require public, reconstructible evidence.
The following table states trim and stream-rate extrema, and the next
paragraph places individual slips at 2.66, 2.65 and 5.68 seconds. Published
poll summaries retain counts, first/last values and the number of distinct
values. `tools/run_b16c.py:457` confirms this reduction: extrema and individual
transition timestamps are not emitted. The two `poll-run.jsonl` histories
are hash-listed but absent from the public packet. In contrast, the summaries
do support 596/596 LOCKED and the constant 30 ns meter field.

Source-meter levels and state comparisons also have narrative claims without
measurement files in the packet: for example, -38.5/-14.0 dBFS, four changes
among 1,255 common entries, and B16c's comparison over 668 common entries.
The manager's routing-change ruling supports outside-lane attribution; it
does not supply those readings.

**Impact:** A cold reviewer cannot independently check these exact figures
or individual slip timing. This is an evidence gap, not an assertion that
the measurements are false.

**Required outcome:** Publish neutral reduced receipts containing extrema,
timestamped slip transitions with associated servo states, and the source
meter/state comparisons. Bind them to the retained raw hashes and provide
the extraction/check procedure. Omit peer/capture identities, layout details,
addresses and host paths. Alternatively, narrow the affected statements to
what the currently published receipts establish.

**Verification:** Each retained figure must reproduce from public records.
`receipts/provenance.json` inventories available records and demonstrates
that different trim extrema can produce the same first/last/distinct summary.

### R625-1-F3 - MINOR - Conformance, Tests, Docs

**Artifacts:** `docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md:2735`,
`:2765`, `:2625`, `:2650`. Retains R624-1 F1 after checking its primary evidence.

**Authority/evidence:** The every-figure requirement is unmet in three places.
`summary/b0-2/c-b9-grade.json` gives floor medians -123.98/-123.95 dB,
not -123.98 on both tones. Its degraded-block inventory splits the claimed
43-54 run into 43-44 and 46-54: block 45 is at the floor. Finally,
`runs/b0-2/events.jsonl` launches the remote capture action at 06:38:03.2,
24 seconds after binding, but `tools/run_b16.py:277` plays for two seconds
before recording. The recording therefore begins about 06:38:05.2,
26 seconds after binding. The B16c timing already includes that lead.

**Impact:** The narrative floor, block inventory and recording start disagree
with their receipts. The corrected delay still exceeds the 20-second wait;
these corrections do not reverse the main audio result.

**Required outcome:** Use the two distinct B0 floor medians, split the block
range, and distinguish command launch from recording start with its two-second
lead. Preserve the correct existing numerical tables.

**Verification:** Check all four locations against the grade JSON, event
timestamps and run source. `receipts/prior-findings-reconciled.json` records
the independently checked values and exact degraded ranges.

### R625-1-F4 - MINOR - Conformance, Tests, Docs

**Artifact:** `docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md:3112`.
Retains R624-1 F2 after checking its primary authority.

**Authority/evidence:** `docs/design/MEDIA_CLOCK_FOLLOWING.md:1671` requires
B CRF to meet B6. The findings' B6 rule at line 324 has four terms:
LOCKED, counted ratio within 0.5 ppm, timed-ratio interval containing zero,
and no listener discontinuities. The new section calls only three terms
"lane B6's terms" and says all are met. It acknowledges the timed ratio was
not measured, and line 3227 substitutes the counted ratio without citing
a public decision to change that criterion.

**Impact:** The B-CRF conformance statement omits an unexecuted acceptance term.
The measured counted ratio is useful evidence but cannot silently replace
the timed-ratio term.

**Required outcome:** State all four terms and mark the timed ratio NOT RUN;
report the other three as met. Alternatively, cite an explicit public scope
decision allowing the substitution for this mode.

**Verification:** Read the revised judgement against the four-term B6 rule,
the design row and any cited decision. No timed-ratio receipt currently exists.

### R625-1-R1 - RESIDUE - Docs

**Artifact:** PR #725 title. Retains R624-1 R1.
**Authority/evidence:** B0 is an INTERNAL case; the detailed result already
distinguishes its 169 floor blocks from the following cases' 300.
**Impact:** The headline compresses those distinct cases inaccurately; the
fix changes no detailed measurement, numerical result or acceptance decision.
**Exact fix:** `Record bench lanes B16, B16b and B16c: Direction B's B0 graded, and B-CRF and B-AAF graded at the path's floor (#629)`.
**Verification:** Compare the revised title with the existing grade tables.

### R625-1-R2 - RESIDUE - Docs

**Artifacts:** `docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md:2971`, `:3096`.
Retains R624-1 R2.
**Authority/evidence:** `window-mark-0` precedes the capture by about six
seconds (`tools/run_b16c.py:680`, `:687`). The retained counter readings and
their values stay the same.
**Impact:** The first mark is labelled as being at the window's start.
**Exact fix:** At line 2971: "Read GET_COUNTERS and GET_CLOCK_SOURCE of both
entities 20 s after the DUT's set, about 6 s before the window, then at its
middle and 15 s before its end, and after it." At line 3096 use
"DUT CLOCK_DOMAIN LOCKED / UNLOCKED, before the window and near its end".
**Verification:** Compare the labels against event timestamps; alter no values.

### R625-1-S1 - SUGGESTION - Docs

**Artifacts:** `tools/census_cmp.py`, `restore/census-*.jsonl` and the
findings' census labels. Retains R624-1 S1.
**Authority/evidence:** The 46 entries include one header, leaving 45 reads.
**Impact:** The current count is correct under the script's definition, but
"reads" may be clearer for readers.
**Optional outcome:** Say "44 of 45 reads equal" when excluding the header.
**Verification:** Remove only the `type=start` record when recomputing the count.

## Lens results

**Conformance - UNCLEAN, F1/F3/F4.** Checked staged STOP/resume decisions, the
binding-format rule, selection and teardown against the frozen assignments.
`summary/loop2/acmp-peer-tap.json` supports B16's two CONNECT_TX commands
200 ms apart without a response; both loopback runs record zero peer-stream
PDUs. B16b stops before creating circular following. B16c uses the authorized
peer INTERNAL exception only for B-CRF/B-AAF. The INTERNAL mismatch control
remains NOT RUN and #629 remains open. Stage attribution needs F1's correction.

[R625] PASS RTL - `docs/overview/ARCHITECTURE.md:72`,
`docs/reference/REGISTER_MAP.md:1870`, `:2082`, `:2139`, and the complete
two-file diff - checked architectural ownership and measurement decoding.
Selection 0/1/2, servo state 4, signed trim units and `0x001e0007` meter
semantics agree with the interfaces. No implementation/interface changes
exist, and no new RTL execution is claimed. F1/F2 concern the evidence,
not changed RTL behavior.

[R625] PASS Robustness - `runs/{loop1,loop2,b0}/events.jsonl`,
`runs/{bcrf,baaf}/ctl.jsonl`, `restore/census-*.jsonl`,
`tools/run_b16c.py:595`, `:707`, and `controls/b16c-dryrun-*.json` - examined
failed loopback, busy-capture exclusion, refused set, absent lock, controller
loss, deadline teardown and restoration order. The eight published dry-run
outcomes and wrapper deadline receipt were inspected, not rerun. The empty
incident capture is explicitly ungraded. All eight actual B16c SETs have
successful matching GET source fields in controller transcripts. DUT listeners
end unbound; peer AAF/CRF bindings, formats, maps and source are restored.
Each of the three censuses independently compares 45/46 equal, differing
only in live propagation delay. Focused corruption/boundary controls pass.

**Tests - UNCLEAN, F1/F2/F3/F4.** Independently checked block arithmetic, floor
classification, alignment coverage and 20 numerical point-table rows from
public JSON. B0 gives -123.95/-122.80 dB medians at (c), 169/300 floor blocks.
B-CRF/B-AAF give 300/300 floor blocks, zero reported events and
-123.98/-123.97 dB medians at (c). Direct sample comparisons cover about
34 seconds within each 300-second audio window. Both following records have
596 LOCKED polls; acquisition is bracketed at 2.657-3.161 and 6.680-7.180
seconds. This reconciles receipts and exercises analysis controls; it is
not a re-grade of unavailable physical recordings.

**Docs - UNCLEAN, F1/F2/F3/F4.** Examined both changed files, PR body, identity/gate
receipts, source attribution and limits. Added text preserves neutral
peer/capture roles and host-path privacy. Documentation, style, path,
contents, anchor, em-dash and whitespace checks pass. Requirements and
compliance status are not silently promoted. The four open findings
must be corrected or supported. R1/R2 remain wording residues.

## Reviewer-owned coverage ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN: F1/F3/F4 | Issue/rulings; findings; B6 four-term criterion; loopback decode; clock exchanges | R625-1 applied; no clean coverage | e20fd2820a9c6b9effabc529a742e732263fafa8 |
| RTL | CLEAN | Complete diff; architecture media-clock boundary; register-map slip, meter and servo fields | R625-1 | e20fd2820a9c6b9effabc529a742e732263fafa8 |
| Robustness | CLEAN | Loopback/incident events; teardown; eight published dry-run receipts; raw clock exchanges; restore censuses; independent controls | R625-1 | e20fd2820a9c6b9effabc529a742e732263fafa8 |
| Tests | UNCLEAN: F1/F2/F3/F4 | Manifest; point/grade/alignment JSON; control functions/receipts; poll summaries; B6 criterion | R625-1 applied; no clean coverage | e20fd2820a9c6b9effabc529a742e732263fafa8 |
| Docs | UNCLEAN: F1/F2/F3/F4 | Both changed files; PR body; author gate receipts; independent documentation checks | R625-1 applied; no clean coverage | e20fd2820a9c6b9effabc529a742e732263fafa8 |

## Executed verification

Portable scripts accompany this report. Supply candidate and immutable public
packet locations as arguments. No host path is embedded in these receipts.

| Check | Result and receipt |
|---|---|
| `audit_receipts.py` | PASS; `receipts/audit.json` and `.rc`. Receipt consistency; findings recorded separately |
| `audit_restore.py` | PASS; `receipts/restore.json` and `.rc`. Censuses and raw SET/GET fields |
| `audit_provenance.py` | Completed; `receipts/provenance.json` and `.rc`. Establishes F2's limits |
| Published offline controls | PASS: presence 8/8, alignment 6/6, loop decoder 1/1, B6 7/7, B9 20/20; JSON/log/rc receipts |
| `probe_controls.py` | PASS 6/6; `receipts/independent-controls.json`. High-byte corruption, forced hash collisions, channel swap, overlap boundary and degraded-block inventory |
| Seven documentation/whitespace checks | Final rc 0; `receipts/checks.json`, `checks-retry.json` and per-check logs |
| Exact-head source integrity | PASS; `integrity-initial.json` equals `receipts/integrity-final.json`. 1,291 candidate blobs and 880 required-submodule blobs verified, with modes, index entries and pins unchanged |

Three initial renderer-dependent checks exited 2 because the reviewer driver
resolved the disposable environment launcher to its system executable.
Preserving the launcher path corrected that setup error. Initial failures
remain in the receipts. Checks ran concurrently within a foreground driver,
at most six processes, with numerical-library threads limited to one.
No source edit, commit, hardware access, full source bank, privilege or
remote write occurred. Temporary fixtures/dependencies stay under `scratch/`.

The author's `gates/b16c/results.json` names this exact head and contains
14 successful entries, including two environment-version checks. These are
documentation/source-policy receipts. There is no manager source-bank run
at this head, and none is inferred.

The read-only snapshot `receipts/hosted.json` records successful `rtl-fast`,
`bdd-conformance`, `wire-accountability` and `docs-check-no-git`.
`elaborate` succeeds while its substantive elaboration steps skip.
Exhaustive simulation/synthesis aggregates and the physical job skip.
`docs-check` was still running at observation. These observations do not
supply manager acceptance or substitute execution evidence.

## Prior public findings

After writing the independent verdict and ledger, read all PR discussion,
review and inline-review entries. There were three discussion comments,
zero formal reviews and zero inline comments. One newly published
[review](https://github.com/kebag-logic/milan-fpga/pull/725#issuecomment-6119236428)
contained findings. Every item is dispositioned here at the unchanged head:

| Public item | Disposition at this head |
|---|---|
| R624-1 F1, MINOR, Conformance/Docs | Retained as F3; primary grade, block and timing receipts checked; Tests also applies |
| R624-1 F2, MINOR, Conformance/Docs | Retained as F4; four-term criterion and missing measurement independently checked; Tests also applies |
| R624-1 R1, RESIDUE, Docs | Retained as R1 with exact title fix |
| R624-1 R2, RESIDUE, Docs | Retained as R2 with exact label fixes |
| R624-1 S1, SUGGESTION, Docs | Retained as optional S1 |
| R624-1 S2, SUGGESTION, Tests | Overlaps independently written F2. This review retains MINOR under Tests/Docs because the assigned every-figure/public-receipt requirement makes the missing evidence required. It also identifies the absent source-meter/state receipts |

No prior item is claimed resolved. `receipts/prior-findings.json` records
the public inventory; `receipts/prior-findings-reconciled.json` records the
primary-evidence recheck and the pre-reconciliation report digest.

## Limits and pending manager duties

Raw audio/tap recordings and poll histories remain privately retained and
hash-listed. This review did not access them. F2 identifies detailed claims
the available summaries cannot reconstruct. Outside-lane source routing and
clock changes remain attributed to that source, not to DUT behavior.

Each following case has one 300-second run on one DUT/reference-peer pair.
The INTERNAL mismatch control was NOT RUN on this image. Physical calibration
was NOT RUN. Printed precision, desk controls and skipped physical contexts
provide no calibrated hardware or release-campaign proof.

The manager must publish this packet, arrange corrections and independent
re-review of affected lenses, obtain both required independent positives,
and ensure no review remains in flight. This is no merge authorization.
Hosted/local-replica acceptance remains the manager's duty.
Carry R1/R2 to the residue checklist; S1 remains optional.

Source validation is separate from final current-dev candidate validation.
At the merge turn the manager must combine this reviewed source lane
(base `c20c85bd`) with then-current dev (provided live tip
`c6bd08c6f52632c6d33d834ce842ac3cf63f29cc`), run the required builder and native
banks, publish exact-candidate receipts, and complete containment after an
authorized merge. This report supplies no candidate-bank result. Issue
#629's remaining acceptance, including the missing mismatch control, stays open.

R625-1 FINISHED
