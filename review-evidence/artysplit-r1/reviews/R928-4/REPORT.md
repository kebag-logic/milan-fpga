[R928] NEGATIVE - exact head 011aaa6f080321e0a89f915720ebb3ee14807a16

External independent evidence re-review R928-4 of [PR #1004](https://github.com/kebag-logic/milan-fpga/pull/1004), relating to [#878](https://github.com/kebag-logic/milan-fpga/issues/878). Source tree: `5b11a07de8c4f69999277424aa8d9b704c297a96`.

**The census publication defect is resolved.** The repaired public extract reproduces all 147 grades and the cross-case qualification. Removing only `none/srp-bound` from its index reaches the required #969/#977 refusal. The overall verdict remains NEGATIVE because the two unchanged extractor defects and the empty generated-output receipt remain open for integration. No new defect was found in the publication repair.

## Scope and authority

This is the requested narrow re-review of R928-3-F1 / R927-3-F1, at the same source head as round 3. It does not renew full source, native-bank, builder-bank or hardware qualification. Unchanged artifacts retain their earlier verdicts under the later-round rule; deferral does not clear an open finding.

I read the repository contract and documentation map, #878's acceptance and public scope decisions, relevant requirements and interfaces, original-base tooling diff and history, then public execution evidence. The independent verdict and five-lens ledger were written before consulting the internal round-3 findings. Prior findings were reconciled after the independent pass. No other round-4 review, private author material or management scratchpad was read.

Relevant authorities are REQUIREMENTS.md REQ-VER-01/03/04, FR_NFR.md 3.4.1, CLOCK_DOMAINS.md:104-117, SPLIT_CONTROL_MEMORY.md section 15, the service harness README:208-226 and 793-830, `receipt_regrade.py`, and `kept_grade.py:235-275`. Public decisions fix the [entity shape](https://github.com/kebag-logic/milan-fpga/issues/878#issuecomment-7096503672), [80 MHz clock](https://github.com/kebag-logic/milan-fpga/issues/878#issuecomment-7097204685), [held-egress treatment](https://github.com/kebag-logic/milan-fpga/issues/878#issuecomment-7097474930), and [conditional registration disposition](https://github.com/kebag-logic/milan-fpga/issues/969#issuecomment-7116192252). Selected public authority text is retained in `receipts/public-scope.json`.

The [acceptance ruling](https://github.com/kebag-logic/milan-fpga/issues/878#issuecomment-7153532537) accepts endpoint counters as the item-5 capture substitute and permits PR #1004 to proceed on its own gates. It keeps #878 open for the offset measurement through #1007. [#1022](https://github.com/kebag-logic/milan-fpga/issues/1022) continues to own the Arty registration cost after #977; reproducing the conditional qualification does not discharge that debt.

Here **P** is [the public evidence at 0cad829e1af15b9c96b0ef3d10d109b9721154c5](https://github.com/kebag-logic/milan-fpga/tree/0cad829e1af15b9c96b0ef3d10d109b9721154c5/review-evidence/artysplit-r1), **E8** is `P/author-r8/receipts`, and **C** is `E8/census-extract`.

## R928-3-F1 / R927-3-F1: CLOSED

Original severity/lenses: external MAJOR, internal MINOR; Conformance, Tests, Docs. This also closes the retained census-replay portion of R928-2-F1 / R928-1-F1.

Artifacts: `P/MANIFEST.json`; `E8/FILES.manifest.json` and `FILES.tsv.part0001.txt`; `C/FILES.json`, `census.json`, all case manifests and observation parts; `receipt_regrade.py:38-89,96-148,176-214`; `kept_grade.py:239-275`.

Evidence:

- All 762 census files satisfy **original SHA256 = published SHA256 = downloaded SHA256**. None is marked redacted. All 759 case-file entries and all 147 case-manifest hashes verify. The complete author inventory also verifies: 814 listed files, with INDEX.md outside that inventory by design.
- The evidence commit changes only the outer manifest and the 27 observation files. Its observation diff restores 32 decimal timestamp tokens on 29 SPAN lines; no other tokens change. Every restored span has end minus start equal to 64 cycles. All 27 restored files match the original hashes already recorded before publication. The repair changes neither expected grades nor grading code.
- The first previously failing observation, `answering-later/notice-retried-0/observations.log`, now hashes to `c0b0d98f768a9741d075a873a62246bc8db056a110c14da3e0e91baed7e0632b`. The formerly differing `valid-destinations/srp-talker` case now reproduces its complete original grade, including its poll-pass count.
- The qualification hash remains `076e7cc7c4f560605b3421be531a044dacafb17e7e99251ef5bbf4b65eb9a09e`. Its census source head remains `74f942be516b84915f7d982fe1e3c65b497c227a`; that is the author's execution evidence, not a newly executed source bank at the review head.
- The unmodified current regrader exits 0: `RESULT: PASS cases=147 worst_pass_cycles=142775` and `RESULT: PASS cross-case costs, record classes, held-egress ledger and owner bounds`. At 80 MHz the longest pass is 1.7846875 ms. The entire replay output also equals the published author proof byte for byte (SHA256 `8bee049c709e6317d6688690e34a1950e3f6066a4b7dea89e6036c752175a4d5`; `receipts/proof-comparison.json`). This is conditional qualification: OWED lines remain owed and held-egress misses remain recorded misses.
- The control removes only the `none/srp-bound` entry from `census.json`. All 761 other files remain byte-identical, including the bound case's files. It reproduces the remaining 146 case grades and exits 1 at cross-case qualification, explicitly refusing: `srp-kept and srp-bound are graded together on one image, this run graded srp-kept alone`. A case-count refusal also appears, but the required pairing-condition refusal is independently present. It does not fail early on integrity or grade mismatch.

The required outcome of F1 is therefore met by the public bytes themselves, without a metadata-rebinding diagnostic or a relaxed comparison.

| Check | Result | Publishable receipts |
|---|---|---|
| Outer/inner/full author inventories | PASS; 762 census files, 759 case mappings, 147 manifests, 814 author files | `receipts/audit.log`, `.rc` |
| Publication repair | 27 files, 29 lines, 32 decimal tokens restored | `receipts/publication-delta.diff`, `.log` |
| Unmodified complete regrade | Exit 0; 147 grades and cross-case PASS | `receipts/regrade.log`, `.rc` |
| Missing-bound preparation | Only one index entry removed; 761 other files unchanged | `receipts/control-preparation.log`, `.rc` |
| Missing-bound replay | Exit 1; 146 grades, named #977 condition refusal | `receipts/missing-bound.log`, `.rc` |
| Source preservation and signatures | Bytes/modes/index/gitlinks PASS; evidence commit unsigned | `receipts/source-integrity.log`, `.rc` |
| Unchanged open causes | Exact source hashes; builder receipt remains empty | `receipts/carried-checks.json` |

## Findings retained for integration

**R928-3-F2 - MINOR - Robustness, Tests, Docs - inclusive part-size boundary remains inconsistent.**

Artifact: `tb/verilator/ctrl_service_budget/census_extract.py:58-74,120`; `receipt_regrade.py:46,192`. Authority/evidence: the writer promises and can emit 14,000,000-byte parts, but `case()` passes that number as the reader's exclusive limit. The CLI adds one. The source head is unchanged; the [round-3 finding and boundary receipt](https://github.com/kebag-logic/milan-fpga/pull/1004#issuecomment-7214832065) remain applicable. Impact: valid exact-limit inputs and multipart inputs with an exact-limit first part fail extraction. Required outcome: consistent size semantics in writer, extractor self-check, CLI and documentation. Verification: exact-limit and multipart exact-limit controls must round-trip and reproduce their grades. This round did not rerun the unchanged boundary probes. Still OPEN.

**R928-3-F3 - MINOR - Robustness, Tests - overlong lines still prevent forward progress.**

Artifact: `tb/verilator/ctrl_service_budget/census_extract.py:63-71`. Authority/evidence: no newline in the candidate part makes `rfind()` return -1, hence `end=0`; the loop does not advance and repeatedly writes empty parts. The unchanged cause and prior bounded `[0, 0, 0]` write probe remain applicable. Impact: malformed input can consume unbounded files/inodes. Required outcome: terminate with explicit refusal or a supported lossless partition, advancing on every nonempty-input iteration. Verification: bounded controls for an overlong/missing-newline line, both initially and after a completed part. No unbounded probe ran here. Still OPEN.

**R927-3-F2 - MINOR - Tests, Docs - the cited generated-output receipt remains empty.**

Artifacts: `E8/gates/builder-split.log`; `E8/INDEX.md` “Gates at the head”; `E8/recipes/gates8.sh`; `E8/gates/gates8.rc`; PR validation claim. Authority/evidence: the receipt is still 0 bytes, SHA256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`, and neither the recipe nor status file has a builder step. This independently retains the [internal finding](https://github.com/kebag-logic/milan-fpga/pull/1004#issuecomment-7214980720). Impact: the cited artifact cannot substantiate generated-output identity. Required outcome: publish command, compared heads, output hashes/diff and exit code, or cite an existing adequate public comparison. Verification: the cited nonempty receipt must show the comparison between `4adfa9dc` and `011aaa6f`. No builder bank was run here. Still OPEN.

These are not relabelled as suggestions or cleared by moving them to integration. They keep their attributable lenses unclean. No additional MINOR/MAJOR/BLOCKER was found in this evidence-only delta.

## Earlier finding dispositions carried at this head

No source commit or dependency changed after the prior exact-head review. These closures are carried, not newly rerun banks.

| Prior finding | Disposition | Unchanged cause-level evidence |
|---|---|---|
| R928-1-F1 / R928-2-F1 census and paired identity | CLOSED | Census replay closes above; E8 paired native/ELF/stimulus identities retain their round-3 closure. |
| R928-2-F2 routed comparison | CLOSED, carried | E8 post-route reports and checkpoint/image hashes are untouched; both report 33,015 LUT and the comparison delta remains 0. |
| R927-2-F1 Arty debt ownership | CLOSED as raised, carried | Section 15 and #1022 still explicitly own the Arty cost after #977; the cost itself remains owed. |
| R927-2-F2 / R927-1-F6 qualification pointer/hash | CLOSED | README:208-211 still names the installed 147-case qualification; its hash independently verifies again. |
| R928-1-F2 source chronology | CLOSED, carried | Previously corrected source comments are unchanged; this repair adds no source comment. |
| R928-1-F3 / R927-1-F1 acceptance and closure | CLOSED as scope findings, carried | Public acceptance ruling still separates PR acceptance from #878's outstanding offset line. |
| R927-1-F2/F3 inventory and idiom | CLOSED, carried | Identical source tree and exact-head prior gate coverage; no generated source or helper change in this round. |
| R927-1-F4/F5 MII guard and console truncation | CLOSED, carried | Firmware, tests, mutations and interface contracts are identical to the prior reviewed head. |

## Wording residues and optional items

The publication repair does not change the following carried wording:

- **R928-3-RS1 - RESIDUE - Docs.** `P/author-r7/receipts/INDEX.md:128-130`: replace “ELF, flash image and stimulus is identical” with “ELF and stimulus are identical; these non-XIP variants produce no separate flash image”. The paired identity already records null flash images. Check the explanatory text only; do not alter measurements.
- **R927-3-RS-1 - RESIDUE - Docs.** `census_extract.py:11` and service README:217: say FILES.json maps every **case file**, not every file written. The docstring should add that `census.json` is new and `published-qualification.json` is copied. The inventory has 759 case entries; the three top-level files are outside it. This wording change must not imply a new integrity check.
- **R927-3-RS-2 - RESIDUE - Docs.** `E8/INDEX.md:5`: delete “Prepared locally; nothing has been posted or pushed.” The archive is published. This changes no result or provenance hash.

No source comment was added in this publication delta, so it introduces no new prohibited lane/review chronology. The three residues do not unclean a lens.

Prior optional items remain optional and unchanged: timing-directive tie-break alignment; general receipt refusal controls; binding the copied qualification into the extractor inventory; fuller second-step build provenance; versioned derivation recipes; an earlier public anchor for the reference checkpoint; the signed-width guard; obsolete inventory wording; harness configuration naming; and the older Arty flash-part descriptions outside this delta. The concrete extractor boundary/non-progress defects are the required F2/F3 above. Earlier closed findings and adopted suggestions retain the dispositions recorded in R928-3 and R927-3 because neither their artifacts nor dependencies changed. No new optional item is introduced by this repair.

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #878/#969 rulings; FR_NFR 3.4.1; section 15; 147 complete grades; cross-case model; required missing-bound refusal; resolved F1 | R928-4 | `011aaa6f080321e0a89f915720ebb3ee14807a16` |
| RTL | CLEAN, carried | Identical source tree; CLOCK_DOMAINS.md:104-117; original-base history; tracked bytes/modes/index and required gitlinks; unchanged image/clock/CDC/interface coverage | R928-3, preserved by R928-4 | `011aaa6f080321e0a89f915720ebb3ee14807a16` |
| Robustness | UNCLEAN: R928-3-F2/F3 | `census_extract.py:58-74,120`; reader limit; current full/missing-bound replays; unchanged boundary and malformed-input causes | R928-4 applied; no clean covering round | `011aaa6f080321e0a89f915720ebb3ee14807a16` |
| Tests | UNCLEAN: R928-3-F2/F3, R927-3-F2 | Public inventories and unchanged regrader; replay/control logs; extractor causes; empty builder receipt and absent recipe/status entry | R928-4 applied; no clean covering round | `011aaa6f080321e0a89f915720ebb3ee14807a16` |
| Docs | UNCLEAN: R928-3-F2, R927-3-F2 | README part-size claim; P/MANIFEST and E8 inventories/index; public reproduction claims; missing builder evidence | R928-4 applied; no clean covering round | `011aaa6f080321e0a89f915720ebb3ee14807a16` |

All five lenses were applied to this delta and its dependencies. RTL coverage is explicitly carried, not a claim of new RTL simulation.

## Reproduction, limits and manager duties

Run from the exact-head source checkout. Set `PACKET` to this report's directory. All disposable material stays under its `scratch/` directory. Fetching the evidence commit is read-only with respect to source files.

```sh
git fetch --no-tags --filter=blob:none origin 0cad829e1af15b9c96b0ef3d10d109b9721154c5
python3 -B "$PACKET/fetch_evidence.py" . "$PACKET/scratch/evidence-new"
python3 -B "$PACKET/audit_evidence.py" . "$PACKET/scratch/evidence-new"
python3 -B "$PACKET/audit_delta.py" . "$PACKET/receipts"
TMPDIR="$PACKET/scratch" python3 -B tb/verilator/ctrl_service_budget/receipt_regrade.py "$PACKET/scratch/evidence-new/author-r8/receipts/census-extract"
python3 -B "$PACKET/prepare_control.py" "$PACKET/scratch/evidence-new/author-r8/receipts/census-extract" "$PACKET/scratch/control-new"
TMPDIR="$PACKET/scratch" python3 -B tb/verilator/ctrl_service_budget/receipt_regrade.py "$PACKET/scratch/control-new"
python3 -B "$PACKET/check_source.py" .
```

`python3 -B "$PACKET/verify_results.py" "$PACKET"` checks both saved replay logs/statuses and writes `receipts/replay-summary.json`. The normal replay must return 0; the control must return 1 with the named pairing refusal. Commands executed in this round ran as foreground processes; the two independent replay processes overlapped, each with its own raw log and status. No build or simulation was started.

- The evidence commit contains no commit signature, and no detached signature was supplied for the scoped packet. Hashes and Git objects were verified; cryptographic signer authentication is **not established**. Original-log hashes cannot authenticate bytes omitted by the published extract. The publisher's privacy-rule implementation was outside this review; its repaired output was verified.
- No manager source bank exists at this head and none is inferred. Source execution evidence is the author's published receipts, identified at `74f942be5`, with unchanged source inputs as carried from the prior review. This round only recalculates grades from observations.
- The [manager's round-7 image bench report](https://github.com/kebag-logic/milan-fpga/pull/1004#issuecomment-7214908085) is public evidence, not hardware work performed by this reviewer. It identifies the unchanged round-7 image and preserves the capture/offset limitations. Physical calibration is **NOT RUN**; field skips are not hardware proof. No physical requirement is newly discharged here.
- The integration round must fix and re-review all three retained findings and reconcile the residues. The manager owns exact-head hosted/act acceptance, distinguishing executed jobs from skipped contexts. This report makes no new hosted-green claim.
- The manager must build and validate the final current-dev merge candidate, including required builder/native banks, and link its receipts. Source comparison base `854bd7236792ce1adbd10c43b13a6a5002ad3bb6` is distinct from supplied live dev `e275d7950ef3385753e6a15d2e191ba855b171ed`; this report does not validate their merge.
- Two independent positive reviews, clean reviewer-owned coverage, no in-flight review, maintainer merge authorization and post-merge containment remain required. Keep #878 open for the offset line and #1022 for owed registration work.
- No source fixes, commits, pushes, GitHub writes, external contact, full banks, hardware operations, host orchestration or other-checkout edits were performed. Final integrity verification checks all 1,995 parent tracked blobs, the complete index, and all five required initialized submodules; the uninitialized `external` gitlink is unchanged. No source restoration was needed.
- Only REPORT.md and files listed in MANIFEST.sha256 are publishable. Extracted evidence, controls and temporary grading files remain under `scratch/` and are excluded.

R928-4 FINISHED
