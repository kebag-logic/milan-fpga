[R744] POSITIVE - exact head 6d1d038343e1f0a6b2027cce857a33528b8c2ac7

# R744-3: delta review of PR #211 (issue #210 documentation sweep), round 3

- **Reviewed head:** `6d1d038343e1f0a6b2027cce857a33528b8c2ac7`, tree `dafc0c31e941eb3bf7106fa4da39c1415a9afc6c`. This is four commits on top of the round-2 head `0ea635ea` (`d77a94b`, `208de11`, `506afbe`, `6d1d038`), with no rebase. Base is main `a9e84b66`.
- **Delta:** 11 files, +81/−42. Markdown in 10 of them, plus the gate script `scripts/check-doc-inventory.py`. No RTL, generator, generated file, test source or workflow is touched.
- **Scope basis:** the #210 issue body (scope, rules, acceptance). The manager's round-3 instruction: remove the banner count, link 06 §8, and sweep the PR's changed pages once for restated counts. The PR metadata, at this head only. The author's round-3 published packet. My own prior reports, R743-2 and R744-2. No other reviewer's report was read before this verdict and ledger were written.

## Verdict

R743-2 F1 is resolved at its cause. The concept page's banner no longer counts the µISA. It names the `ucpu_op_e` enum and links the 06 §8 heading, and the inventory gate derives that heading's count and table from the enum. The extended gate is neither broken nor vacuous:
- All 13 drifts I planted fail: a fake op in the table, a wrong heading count, a count restated on the heading line, the old banner, a true-count banner, a current-page count, an enum change, a dropped 09 §7 row, a dropped defining file, dropped link targets and dropped anchors.
- The clean head passes `make check` (rc 0).
- The round-2 gate passes the old banner, so the extension is what catches it.

Every count the round changed now links its defining Makefile, script, enum or state machine, or no longer counts. I checked each replaced count against its source, and each was true at `0ea635e`, as the PR says.

No BLOCKER, MAJOR or MINOR is open. Three new wording-only RESIDUE items and one carried RESIDUE item are recorded below, with suggestions. This verdict does not claim hosted or act acceptance and does not authorize a merge.

## Prior findings at this head

| Finding | Disposition at `6d1d038` |
|---|---|
| **R743-2 F1** (MINOR; Docs, RTL): the concept banner said "29-operation ISA", but the enum declares 30 | **Resolved.** At `IEEE_1722_1_Hardware_Protocol_Processor.md:18` the banner now reads "a different ISA, the `ucpu_op_e` enum in [`hdl/aecp/ucpu_pkg.sv`]; [06 §8](…#8-µcode-architecture) lists it…". No count remains. `hdl/aecp/ucpu_pkg.sv:49-88` declares 30 members, ending `OP_SHIFT_R = 5'd29`. 06 `:1427` says "µISA (30 operations)", and the gate holds it to the enum (probes M2, M8). The banner's anchor is link-checked (probe M13 fails when the heading is renamed). The optional hardening I offered in R743-2 was also done: the gate now holds the banner (probes M4, M5). `git grep` finds µISA counts only at 06 `:1427` (derived) and in two retired-page bodies: concept `:1098` "~20–30 instructions" (the original plan) and 10 `:536` (history). |
| R743-2 S1 (SUGGESTION): `target_findings` reads only the first `check:` line | **Retained as a suggestion.** The code is unchanged (`scripts/check-doc-inventory.py:91`). The PR body now discloses this under "Not fixed here". |
| R743-2 S2 (SUGGESTION): the 06 spelling is taken from an upper-case comment | **Retained as a suggestion.** Unchanged. It fails closed. |
| R743-2 S3 (SUGGESTION): mutant provenance in the PR body | **Resolved.** The body now names the clone for each round: "a disposable clone of exactly `6d1d038`" for round 3, and `06c934b` for round 2, reproduced at `0ea635e`. |
| R744-2 RES1 (RESIDUE): `tb/adp_engine/README.md:330`, "(review R406-1 F-1)" | **Retained as RESIDUE.** The line is still present. It is one of the 156 R-labels the PR body lists under "Not fixed here" and the reason for "Refs" rather than "Closes". |
| R743-1 S1 to S4 (SUGGESTION) | **Retained as suggestions.** The delta does not touch them. |

## Findings, residue and suggestions at this head

### R744-3-RES1: RESIDUE (Docs, Tests). The gate's coverage is described more broadly than its matcher
- **Where:**
  - `scripts/check-doc-inventory.py:18` and `:117` (docstrings: "a µISA operation count stated on any current page …", "stated anywhere but the heading");
  - `docs/INVENTORY.md:12`;
  - `docs/architecture/09_verification.md:138` ("no other current page … states a µISA operation count");
  - the PR body's Gates bullet ("fails on a µISA operation count stated on any current page").
- **Evidence:** `UISA_COUNT` (`:113`) is a per-line pattern. It needs `ISA` and `<digits>[- ](operation|operations|ops)` on the same physical line. In `receipts/plant-6d1d038.tsv`, four restatements pass with rc 0:
  - G1: the count hard-wrapped to the next line (these pages wrap at about 90 columns);
  - G2: "30 µISA operations";
  - G3: "thirty-operation ISA";
  - G4: "30 instructions".
- **Why RESIDUE, not MINOR:**
  - F1's required outcome was the banner text, which is fixed. Holding the banner in the gate was optional.
  - The gate catches the class as it actually occurred (M3 to M6).
  - My independent grep finds no current restatement that escapes the gate at this head.
  - The defect is that the description is broader than the behaviour. Correcting the description changes no test, figure or verdict.
- **Exact fix:** at each place listed above, say that the gate fails on "a line that names the ISA beside a count of operations (for example `29-operation ISA`, `µISA (30 operations)`)". Alternatively, take up S1 below so that the existing wording becomes true.
- **Verification:** reread the four places listed above. If S1 is taken up, G1 to G4 fail.

### R744-3-RES2: RESIDUE (Docs). A model count in 09 §8.6 was missed by the sweep
- **Where:** `docs/architecture/09_verification.md:399`: "the run-wide checks hold under all nine models".
- **Evidence:** this round replaced "nine device models" in 09 §8.6's prose with a link to `MODELS` in `tb/nvm_port/measure_figures.py:500`. The same section's table row still counts the set. The count is true: `MODELS` has nine entries. This is the class the manager asked the sweep to remove, and the PR body says the sweep covered "device-model … counts in 09 §8.4 and §8.6".
- **Exact fix:** "… the run-wide checks hold under every model of the figures gate's `MODELS`".
- **Verification:** `grep -n 'nine model' docs/architecture/09_verification.md` returns nothing, and `make links` passes.

### R744-3-RES3: RESIDUE (Docs). A bound count was missed in the `tb/nvm_port` README
- **Where:** `tb/nvm_port/README.md:777`, the heading "### Three bounds (issue #15)", and its cross-reference at `:21` ("see "Three bounds" below").
- **Evidence:** the set is the Makefile's `TMO`, `TMO_ALT` and `TMO_MIN` (`tb/nvm_port/Makefile:17-19`). The count is true. This round linked those variables at `:17` and replaced the README's other build and bound counts. The PR body says the sweep covered bound counts in this README. The section body enumerates the values, but the heading and its cross-reference count them without doing so.
- **Exact fix:** retitle the heading to "### The suite's bounds (issue #15)", and update `:21` to "see "The suite's bounds" below".
- **Verification:** reread both lines. The reference is quoted text, not a link, so the link gate is unaffected.

### Suggestions (do not affect the verdict)
- **R744-3-S1 (Robustness, Tests):** match per paragraph rather than per line: join each run of non-blank lines before applying `UISA_COUNT`. Accept a count on either side of the µISA word, and accept `instructions` and `opcodes`. G1 to G4 in `scripts/plant.sh` are ready-made self-test fixtures. Spelled-out numbers can stay out of scope if the description says so.
- **R744-3-S2 (Docs, PR text):** the PR body's round-3 sweep table could list RES2 and RES3, or state the sweep's limits as it already does for kept tallies.
- **Carried:** R743-2 S1 and S2, and R743-1 S1 to S4, as above.

The delta adds no new lane, bench, review or comment-ID label. I grepped the added lines for review IDs, lane terms and comment IDs and found none.

## Lens evidence (delta, artifact-specific)

- **Conformance:**
  - The delta changes no clause citation or normative statement. Its changed lines are gate prose, count wording and links.
  - #210 rule "Values live in one table and are linked, never copied": every count replaced this round now points at its defining file (table below). The two missed instances are RES2 and RES3, both true.
  - Acceptance "every document has a status": the inventory gate passes, with 63 files.
  - Acceptance "the docs gates pass": `make check` rc 0 here.
  - The unchanged clause content keeps R744-2's coverage and limits.
- **RTL (source fidelity):**
  - The banner names the enum that `hdl/aecp/ucpu_pkg.sv:49-88` declares, with 30 members.
  - Each replaced count was checked against its source:

    | Replaced count | Source |
    |---|---|
    | `tb/acmp_nvm` and `tb/adp_engine`: two builds | `run` with `NR != 2` |
    | `tb/dyn_state`: 2x2 and 1x1 | `run` |
    | `tb/nvm_port`: three suite builds | `TMO`, `TMO_ALT`, `TMO_MIN`, plus `FUZZ_TMOS`, `BUILDS` |
    | `tb/srp_top`: four store shapes | `STORE_SHAPES = 1x1 2x2 3x5 9x9` |
    | `tb/srp_admission`: five shapes | `shapes`: N = 1, 2, 3, 5, 8 |
    | `tb/timer_map`: ten shapes | `LEGAL` (10 entries); `SI_TBL_C`, `SO_TBL_C [0:9]` |
    | the figures gate: nine models | `MODELS` (9 entries) |

    All were true at `0ea635e`, as the PR body says.
  - The new wording ("393 checks in each suite build", "once at each of `TMO`, `TMO_ALT` and `TMO_MIN`", "one build at each of 100, 37 and 20") matches `tb/nvm_port/Makefile:17-56`.
  - No RTL is changed.
- **Robustness (gate):**
  - The change to `restated_uisa` holds its matches on every inventoried page, holds only the opening quote block on retired pages, and on 06 strips exactly the derived heading before matching.
  - The planted-drift campaign (`receipts/plant-6d1d038.tsv`) has 22 rows:
    - 13 drifts (M1 to M6, M8 to M14): all fail.
    - 3 head controls (self-test, inventory, links): all pass.
    - 1 retired-body control (M7): passes.
    - 1 cross-check (R2): the round-2 gate passes the old banner.
    - 4 rows record the matcher's limits (G1 to G4). These feed RES1 and S1.
  - The harness marks a mutation that failed to apply as `APPLY-FAILED`, so an unapplied mutation cannot pass for a clean result. My first run hit this and was corrected. No row in the published receipt is `APPLY-FAILED`.
- **Tests:**
  - `--selftest` reports 30 cases (25 caught, 5 clean), matching the PR body.
  - `make check` at the exact head on a disposable clone: rc 0, 50 s (`receipts/make-check-6d1d038.log`).
  - The author's round-3 packet is consistent with this. Its eight downloaded files match the published SHA-256 values in the archive's `MANIFEST.json` (`receipts/author-r3-packet-verify.txt`). Its `rc.txt` reports rc 0 for every gate at base and head. Its `nvm-inputs-{0ea635e,6d1d038}.json` are byte-identical (same SHA-256), which supports the claim that the `tb/nvm_port` figures gate's README inputs are unchanged.
- **Docs:**
  - All 10 changed Markdown files were read in the delta.
  - The links gate passes, and it is not vacuous for the new links: M11 to M14 each fail.
  - The srp_top anchor was renamed together with its heading, and it resolves.
  - The README start-here and guide-table rewording ("others", "every guide") is accurate.
  - The `make check` comment now points at 09 §7, which the gate derives.
  - The inventory rows for the concept page and `tb/nvm_port` match their pages.
  - RES1 to RES3 are wording residue.

## Reviewer-owned ledger

| Lens | Verdict | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #210 rules and acceptance; delta clause-free; replaced counts linked; unchanged clauses per R744-2 | R744-3 delta; R744-2 and R744-1 for unchanged pages | 6d1d038343e1f0a6b2027cce857a33528b8c2ac7 |
| RTL | CLEAN | `ucpu_pkg.sv` enum against the banner and 06 heading; suite Makefiles, `shape_elab.sh`, `timer_map_wrap.sv`, `measure_figures.py` against every replaced count; no RTL in the delta | R744-3 | 6d1d038343e1f0a6b2027cce857a33528b8c2ac7 |
| Robustness | CLEAN | `restated_uisa`, `UISA_COUNT`, retired-banner span, 06 heading strip; 22-row planted-drift campaign; matcher limits (RES1, S1) | R744-3 | 6d1d038343e1f0a6b2027cce857a33528b8c2ac7 |
| Tests | CLEAN | self-test (30 cases); `make check` rc 0; author round-3 receipts hash-verified; NVM input identity | R744-3 | 6d1d038343e1f0a6b2027cce857a33528b8c2ac7 |
| Docs | CLEAN (RESIDUE recorded) | all 10 changed Markdown files; banner and anchor; links gate; count sweep (`receipts/count-sweep-grep.txt`); RES1 to RES3 and carried R744-2 RES1 | R744-3; R744-2 for unchanged pages | 6d1d038343e1f0a6b2027cce857a33528b8c2ac7 |

## Limits and pending manager duties

- **No manager source bank** runs at this exact head, and none is claimed or inferred. Source-head execution evidence is the author's published gate receipts, plus my own `make check` and probes. No parent, PP, gPTP, Yosys, builder, timing or synthesis bank was run. No Verilator suite was run here: the delta changes no suite or RTL source.
- **Archive commit not signed:** the evidence archive commit `a397e609` is unsigned, according to GitHub's commit verification. Integrity rests on the archive's `MANIFEST.json` hashes, which match for every file I downloaded.
- **Hosted status** at the head (`receipts/hosted-check-runs-6d1d038.tsv`, read-only):
  - `docs-gates` and `portability` completed with success, each twice.
  - `suites` was still in progress when queried. That job carries `make -C tb/nvm_port figures`, which I did not run.
  - The manager owns hosted and act acceptance.
- **Standards texts:** complete adopted-edition texts were not re-obtained. The delta makes no clause claims.
- **Physical calibration:** NOT RUN. Field skips and simulation are not hardware proof.
- **Manager duties still open:**
  - hosted and act acceptance at this head, including the `suites` job;
  - the second independent review;
  - carrying RES1 to RES3 and R744-2 RES1 to the residue checklist;
  - validating the actual current-dev merge candidate (source base `a9e84b66`, live dev `1e80128f0a467b58bf884b7d9bf62e013a2fb141`) with the builder and native banks at the merge turn.
- **Restoration:** the review clone was never modified. Probes ran on a disposable clone, since deleted. `receipts/restore-verify.txt` records:
  - HEAD and tree are exact;
  - the index tree equals the HEAD tree;
  - the stage blobs and modes equal `ls-tree -r HEAD`;
  - there are 0 porcelain lines;
  - there are 0 gitlinks, so this repository needs no submodule gitlinks.

R744-3 FINISHED
