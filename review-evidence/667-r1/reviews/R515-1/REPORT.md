[R515] NEGATIVE - exact head 41bc9dac031526c1fd637ff1e801d3c6dc1260b4

Round R515-1. External independent review of issue #667 / PR #680.
Tree: `1a233401c2f5d585b7a0a2d1a7db16daff6d29b6`.
All five lenses were applied. One MAJOR acceptance/evidence finding remains.
No defect was found in the eight-line startup RTL change.

The startup checks pass and reject all eight planted defects. The finding
concerns carrying the #657 exception across the dev merge: the published
head is byte-identical to the current dev render baseline, but differs from
the assigned base used by the frozen ruling and retained comparison.

## Scope and reconstruction

The authorities were AGENTS.md, CONTRIBUTING.md, docs/README.md, the public
issue body and scope decisions, REQUIREMENTS.md, the linked timing/interface
documents, and the primary IEEE 1722-2016 and Milan v1.2 documents. Their PDF
identities are recorded in [authority-identities.json](receipts/authority-identities.json).

- [Assignment 6011846710](https://github.com/kebag-logic/milan-fpga/issues/667#issuecomment-6011846710)
  defines the red reproduction, first-sample timestamp, mutation preservation,
  regression and own-area requirements. The post-flash bench repeat belongs
  to the manager.
- [Ruling 6012843714](https://github.com/kebag-logic/milan-fpga/issues/667#issuecomment-6012843714)
  permits the existing #657 results only with the specified base equality.
- [Public evidence at 90d0bcbf](https://github.com/kebag-logic/milan-fpga/tree/90d0bcbfb83ee4f5d47edadd734acd1e1056759b/review-evidence/667-r1)
  was read after the independent source pass. All 19 published files match
  the publication manifest.

The requested `423ac5d9..41bc9dac` diff and history were examined, separating
the startup delta from inherited #658 and B13 changes. The published head
has parents `5d6164a2` and `bd884631`. Against the dev parent, seven paths
change. The six non-table paths exactly preserve the author's bytes; the
reader table is exactly dev's table plus the author's unchanged startup
entry. No other merge resolution was found. See [evidence-audit.json](receipts/evidence-audit.json).
Inherited map initialization and render-harness changes were checked for
their interaction with startup and the exception; this is not a replacement
review of the entire earlier #658 implementation.

The independent verdict and ledger were written before checking prior PR
findings. PR #680 then had zero submitted reviews, zero inline comments,
and only the two review-start conversation comments. There were no earlier
public review findings on this PR to resolve or retain. No other reviewer's
report or private author material was used.

## Finding

**R515-1-F1 | MAJOR | Conformance, Tests, Docs**

**Artifact:** PR #680 validation section; public
`author/render-comparison.json` at evidence commit `90d0bcbf`;
`tb/verilator/milan_dp_render/sim_tdm8_render.cpp:1875` and `:1892`;
[epoch-base-head.diff](receipts/epoch-base-head.diff).

**Title:** The retained render exception does not establish the frozen
base-equality condition at the published head.

**Authority/evidence:** Ruling 6012843714 requires byte-identical clean-leg
stdout and the same remaining checks/mutants. Its retained 32-run comparison
correctly names author head `5d6164a2`, not reviewed head `41bc9dac`.
Fresh builds of the complete assigned base and complete published head
both return 1 with the same four failed assertions, but produce:

| Render `--epoch-only` input | Checks / failures | Bytes | SHA-256 |
|---|---|---|---|
| Assigned base `423ac5d9` | 114 / 4 | 3745 | `7876a3a277df5e06a9381e502249b9638b7a4e04ec676fefba207150b41d4007` |
| Published head `41bc9dac` | 127 / 4 | 3746 | `3ef42e34ca3874e90fd2929f869dd0f37343e04b9cb2cb0c5f294262448c1c6b` |
| Dev render closure `bd884631` | 127 / 4 | 3746 | `3ef42e34ca3874e90fd2929f869dd0f37343e04b9cb2cb0c5f294262448c1c6b` |

The changed output includes descriptor bursts (3 to 5), INTERNAL
commit-to-pin measurements (37..194 to 49..199 cycles), the reported walk,
CRF law margins, and reset placement. This is not purely prose and cannot
be RESIDUE. The four failed assertion lines themselves are byte-identical:
[epoch-failure-lines.json](receipts/epoch-failure-lines.json).

An additional controlled build used the head render closure with the exact
dev packetizer substituted. The relevant HDL, harness, recipes, configuration,
generators and gitlinks otherwise equal dev. Its complete output equals
the published head byte-for-byte:
[epoch-dev-comparison.json](receipts/epoch-dev-comparison.json).
This isolates the observed difference to inherited dev changes; it does
not demonstrate a startup-fix RTL regression.

**Impact:** The original 32-run comparison remains valid historical source
evidence, but cannot be reported as the frozen comparison for this exact
head. The same four failures alone do not prove the required unchanged
measurements and other campaign results. Source validation and final
candidate validation remain separate obligations.

**Required outcome:** Publish an explicit disposition of the changed
comparison baseline after the dev merge. If the exception is to be carried
against `bd884631`, record that decision and the complete current-base/head
campaign comparison, retaining every result and any survivor. Keep the
original comparison labeled with its actual author head. This finding
does not request reverting #658 or altering an assertion to regain equality.

**Verification:** Re-review the public disposition and all 32 per-run
stdout/return-code/campaign judgments for its named baseline and exact
candidate. The focused current-dev equality is already established here;
the full campaign was not re-executed by this reviewer.

## Lens results and executable evidence

**Conformance:** The implemented timestamp behavior agrees with IEEE
1722-2016 4.3.2, 4.4.4.5, 4.4.4.9, 7.3.5 and 7.5. Normal-mode AAF
requires `tv=1` and a valid presentation timestamp for the first sample
frame, common to all its channels. The assignment's 5.4.4 concerns IEC
61883 encapsulation and 7.3.4 concerns bit depth; the public issue and PR
correct that citation without changing the required behavior. Milan v1.2
4.4.2.1 and Table 5.6 support the stated buffering/counter interpretation.
F1 leaves acceptance coverage unclean.

The base root cause is `KL_aaf_packetizer.sv:314` (unconditional admission
of an enabled owned pair), `:712` (last pair advances the sample count),
`:720` (timestamp capture needs sample zero and pair zero), and `:651`
(emission reads retained TCTX w4). Disable clears accumulation at `:734`
without refreshing that timestamp. Enabling after pair zero therefore
publishes a partial first sample with an old timestamp. The next epoch
refreshes it normally. The public initial red probe and the reviewer base
run both reproduce a signed first step of -494821316 ns, followed by
+125000 ns steps. The 3.8-second disabled interval explains the negative
signed modulo-2^32 step; it is not a measured backward PHC adjustment.

**[R515] PASS RTL - `hdl/ieee1722/aaf/KL_aaf_packetizer.sv:318`, `:591`,
`:715`, `:734`, `:742` - per-talker admission and existing timestamp path.**
The new flag remains clear until that talker's owned pair zero. Reset and
disable clear it; disabled admission and capture are mutually exclusive.
Before first acceptance the sample count remains zero, so the existing
PHC-plus-offset write is acquired with the first complete sample. The
serializer, `tv` encoding, ports, register map, parameters, clock domains
and write-port priority are unchanged. Per-talker indexing and mixed-width
slot ownership were also exercised independently.

**[R515] PASS Robustness - `tb/verilator/aaf/sim_start.cpp:75`, `:151`,
`:207`; [multi_start.cpp](scripts/multi_start.cpp) - restart, wrap, stalls
and stream isolation.** The standing sweep covers cold starts, disable,
reset while enable remains high, three pair spacings, phase boundaries,
three PHC origins, timestamp wrap, sequence wrap and bounded stalls.
Missing packets and incomplete or reordered payload rows fail checks.
The added independent probe exercises eight talkers, 2/4/6/8-channel
partitions, distinct presentation offsets, 48 cases / 384 stream starts,
4,224 PDUs and 202,752 checks, all passing. It includes reset with all
enables held high and stalls seven clocks in nineteen. These are bounded
stall checks, not an indefinite downstream blockage claim.

**Tests:** The expected sample times come from injected samples and the
stimulus clock; they are not obtained from internal timestamp registers.
Every first PDU is graded. The mutation driver requires exit 1 and the
named assertion; compile failure or a crash cannot count as a catch.
The default AAF target includes the startup checks and controls. The
reader-table move preserves its classification and passes the policy gate
and its 101-check self-test. F1 leaves the complete render evidence unclean.

| Reviewer execution | Result | Receipt |
|---|---|---|
| Exact-head startup and eight controls | 34,020 checks; 486 starts; 4,860 PDUs; 8/8 caught; rc 0 | [startup-head.log](receipts/startup-head.log) |
| Same startup harness, exact base packetizer | 33,804 checks; 864 failures; expected make rc 2 / executable rc 1 | [startup-base.log](receipts/startup-base.log) |
| Independent eight-talker probe | 202,752 checks; zero failures; rc 0 | [multi-run.log](receipts/multi-run.log) |
| Existing flat talker | 27 checks; zero failures; rc 0 | [flat receipt](receipts/aaf_talker_i2s-run.log) |
| Existing NxN/golden comparison | 42 checks; zero failures; rc 0 | [NxN receipt](receipts/aaf_nx_wrap-run.log) |
| Assigned-base/head render epoch | Same four failures, unequal complete output | [comparison](receipts/epoch-comparison.json) |
| Current-dev/head render epoch | Same complete output | [comparison](receipts/epoch-dev-comparison.json) |
| Reader policy and self-test; diff whitespace | All rc 0 | [policy](receipts/reader-check.log), [self-test](receipts/reader-selftest.log), [whitespace rc](receipts/diff-check.rc) |

The public pre-edit search covers the added RTL lines, patch population,
and existing exact-text campaign tables. Its planting inventory records
render, licence, stream-info, unbind, GM-step and mclk sites. The eight
new controls were all compiled and killed in this review.

**Docs:** `docs/design/TIME_SYNC.md:501` and `tb/verilator/aaf/README.md:13`
accurately describe pair-zero admission, the timestamp oracle, sweep
dimensions and boundary limits. The README correctly separates a modeled
post-bind enable from an ACMP exchange and physical capture. The PR labels
the earlier author head and distinguishes synthesis area from timing;
F1 concerns its acceptance evidence after the published merge.

## Retained broad evidence and area

The public `GATES.json` and handoff report 60/60 default suites,
2,184,191 checks, 58/58 portability tops and both aggregates at rc 0 for
author head `5d6164a2`. They identify completed replacements for cancelled
or invalid setup attempts. The mclk receipt is indexed in
`RESUME-ARTIFACTS.json`. The explicit campaigns, 81 boundary rounds,
native banks, builder-required arms and static checks are recorded there.
These are reviewed public summaries and artifact indexes, not a claim
that this reviewer independently executed those banks. The assignment
also reports manager source static/builder and native validation at the
published head; that does not replace final current-dev candidate evidence.

The public area rows give packetizer 868 to 864 LUT and 1344 to 1344 FF:
own delta -4 LUT / 0 FF, within 40/40. The packetizer has no child
hierarchy to subtract. Complete datapath is +77 LUT / +14 FF; the unchanged
processor subtree contributes +91 LUT. Excluding both processor subtrees
gives -14 LUT / +14 FF. The arithmetic and retained shipping 1x1 OOC
recipe were checked. No synthesis was repeated, and these figures are
not routed timing or an area measurement of a later merge candidate.

## Reviewer-owned ledger

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN: F1 | Issue assignment/ruling; IEEE timestamp clauses; packetizer first-sample path; exact epoch comparison | R515-1, applied | 41bc9dac031526c1fd637ff1e801d3c6dc1260b4 |
| RTL | CLEAN | KL_aaf_packetizer.sv:318, :591, :715, :734, :742; slot/TCTX/serializer paths; merge and area audit | R515-1 | 41bc9dac031526c1fd637ff1e801d3c6dc1260b4 |
| Robustness | CLEAN | sim_start.cpp:75, :151, :207; start_mutants.py:24; multi_start.cpp and completed receipts | R515-1 | 41bc9dac031526c1fd637ff1e801d3c6dc1260b4 |
| Tests | UNCLEAN: F1 | AAF Makefile:22; sim_start.cpp:113; start_mutants.py:51; policy/legacy/multi/epoch receipts; published gate indexes | R515-1, applied | 41bc9dac031526c1fd637ff1e801d3c6dc1260b4 |
| Docs | UNCLEAN: F1 | TIME_SYNC.md:501; AAF README:13; PR validation section; public GATES.json and render-comparison.json | R515-1, applied | 41bc9dac031526c1fd637ff1e801d3c6dc1260b4 |

## Limits and manager duties

- Resolve F1 publicly and obtain a new verdict for its affected lenses.
  The original #657 failures and surviving uncounted-repeat control remain
  open under their explicit exception; they were not silently called fixed.
- This source review does not validate the manager's final current-dev
  candidate. Build and gate that candidate, retain its tree/base identities,
  finish hosted/local workflow acceptance, and complete the independent
  review bar before any authorized merge.
- [hosted-checks.json](receipts/hosted-checks.json) is a point-in-time read:
  several jobs were still running, all four portability shards had succeeded,
  and the physical-rate context was skipped. No skipped context is counted
  as executed evidence. Hosted/local workflow acceptance belongs to the
  manager; neither local workflow orchestration nor its self-test was run.
- The reviewer did not run full parent, processor, portability or builder
  banks, synthesis, hardware or flashing. Optional physical calibration is
  NOT RUN; field skips and physical-rate simulation are not hardware proof.
- After merge and flash, repeat B13's 100 binds and inspect initial PDUs
  and listener EARLY/LATE counters. The desk reproduction identifies a
  matching mechanism, not absolute bench gPTP correlation or an incidence
  rate. Complete post-merge containment and the issue's final state afterward.

All probes used disposable sources/builds under this packet's `scratch/`.
Independent builds were joined by foreground drivers, with at most sixteen
compiler workers; no synthesis ran. No source fixes, commits, pushes,
GitHub writes, hardware operations, other checkout edits or delegation
were performed. Exact tracked blobs, kinds, executable modes and index
entries were checked independently of status flags, including the three
required registered submodules:
[tree-integrity.json](receipts/tree-integrity.json).

Portable drivers are in `scripts/`; raw command outputs and return codes
are in `receipts/`. Installation and checkout path prefixes in build logs
are redacted; all three render simulation stdout files retain their exact
raw bytes. Only files listed by `MANIFEST.sha256` and this report
are publication inputs. Disposable trees and primary-document extractions
are excluded.

R515-1 FINISHED
