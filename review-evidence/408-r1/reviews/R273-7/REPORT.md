[R273] NEGATIVE - exact head 991d59653ff82ccf73ef4df9477de1df8c8c5964

Round R273-7, external independent review of PR #535 (#408 and #409), correction round 5 (`991d5965` on `4a56ef08`, tree `07df25436405c718275b0238d02e1caeb85aec2a`). Source base `759da623072358afdb0e9d570a7b4b6a788492c9`.

The round does what its assignment asks:

- The closure table now holds 23 positions and 6440 cells. Every cell is either refused or agrees with the pinned GCC, and the one exception is named and fails closed.
- The new cells can fail.
- The invalid-UTF-8 wording is honest at all four sites.
- The page uses one round-numbering scheme.

One MINOR stays open. A fourth code comment still states the unscoped proof claim that round five scoped at the three listed sites. That leaves Docs UNCLEAN, so the verdict is NEGATIVE. No protection gap was found.

## Reconstruction

I read the following in order: AGENTS.md, CONTRIBUTING.md, docs/README.md, and the #408 and #409 bodies (acceptance 1-5). Then the manager decisions on #408:

- 5758649507: remaining scope.
- 5798077836: bundle lane.
- 5811522505: round 3, close the grammar to S.
- 5813535416: round 4, character allowlist and generated closure table.
- 5815136430: the BOM refusal stands, and invalid UTF-8 in a comment is refused although GCC accepts it, with the page stating the cost.
- 5816286265: the round-5 assignment. R272-5 F1 option (b), R273-6 F1 at four sites, R272-5 S1.

After those I read the author's REVIEW READY 5818553202 and `git diff 759da623..991d5965` (three files: `sw/builder/test_builder.py`, `docs/integration/BAREMETAL_FIRMWARE.md`, `docs/testing/CI_WORKFLOWS.md`). I focused on `git diff 4a56ef08..991d5965`: 186+/26- in test_builder.py and 83+/44- in the page. Last came the executable evidence below.

I read prior review findings only after my verdict and findings were fixed in `receipts/verdict-before-prior-findings.txt`.

## Findings

### R273-7 F1 - MINOR - Docs - `sw/builder/test_builder.py:11291-11295`: an unscoped closure-proof claim survives at the gate's call site

**Artifact.** This is the comment directly above `subset_note = assert_subset_refuses()`, `lexer_note = ...` and `closure_note = assert_character_closure()` (`:11296-11298`):

> "on the spellings S admits the readers every rule stands on read a directive exactly where the pinned GCC does (#408); and at the character level every byte in every position is refused by S or read as GCC reads it (round four)."

`git blame` shows lines 11294-11295 come from `4a56ef08` (round four). At that head the comment was at `:11134`. Round five left it unchanged.

**Authority and evidence.**

- Round-5 assignment (#408 comment 5816286265), item 1: the proof sentences "state the positions the table actually holds". Refusal of a character outside the allowlist is position-independent. "Agreement at any position the table does not hold rests on the lexer corpora".
- R272-5 F1 (MINOR) was raised against exactly this sentence class, "every byte in every position", at `:5108` and the page's cost row. Round five fixed those sites (`:5226-5248`, `:5557-5569`, page `:322-356` and `:1367`). This sentence is the same phrase at a site nobody listed, so the sweep is incomplete.
- The claim is false as literally stated. My out-of-table probe (`receipts/closure-extend-summary.txt`, Parts B/C, byte-identical to round four's) holds S-admitted cells where the readers and GCC differ:
  - 29 cells in the gap between `#ifdef` and its name, e.g. `#ifdef!FOO`, plus 3 more: GCC refuses the file while the readers read names.
  - 4 cells, `#` then CR/LF pairs: the readers refuse and GCC reads.
  - None is at a position the table holds.
- Every one of those cells fails safe. A file GCC refuses does not build, and a reader refusal refuses the firmware. So this is a proof claim wider than the proof, not a protection gap.

**Impact.** The call site is where a maintainer reads what the three checks guarantee. It tells them the closure table is a regression net for every character position. Round five spent its assignment making the other three sites say the opposite, so the file now contradicts itself on the claim R272-5 F1 raised.

**Required outcome.** The comment at `:11291-11295` states the scope the corrected sites state:

- refusal outside the allowlist is position-independent;
- agreement is measured at the table's 23 positions;
- elsewhere, agreement is bounded by the two lexer corpora.

The spelling-level "exactly where the pinned GCC does" either carries the same corpora bound or refers to where it is stated. No behaviour change.

**Verification.**

- `grep -n "every byte in every position\|every position" sw/builder/test_builder.py docs/integration/BAREMETAL_FIRMWARE.md` finds no unscoped claim.
- The static documentation checks listed below still exit 0.
- A comment-only diff needs no gate re-run beyond what the manager requires for a new head.

### R273-7 S1 - SUGGESTION - Docs - `docs/integration/BAREMETAL_FIRMWARE.md:349-354` and the cost table: the null directive

The page names the lone `#` at the end of the file as the one fail-closed table cell. A null directive anywhere else is refused the same way, on the directive-set pin, at dev and here in both modes (`receipts/probes/nulldir-*.json`: cases N2-N5 are REFUSED on "the firmware's preprocessing directives are pinned, and '#' is not one of them"). This is pre-existing and does not change in this PR. The cost row "No `#pragma`, `#line`, `#undef` or `#include_next` ..." could name it. Optional; it does not affect coverage.

## Prior public findings at this head

| Finding | Disposition | Evidence at 991d5965 |
|---|---|---|
| R272-5 F1 MINOR (closure scope stated as every position; the table held nine) | **Resolved at its three listed sites, by option (b).** `_CLOSURE_POSITIONS` (`:2774-2839`) holds 23 positions: the nine plus B1-B14. `_CLOSURE_KEPT` (`:2871`) holds 6440 letters. The page `:322-356`, the S comment `:5226-5236` and the lexer-bound comment `:5557-5569` are scoped. "each position a lexing difference moves a directive" is gone. **A residue at a fourth site is raised as R273-7 F1.** | Gate in both modes: 6440/6440, 23 positions (`receipts/gate1b/head-*.log`). One-file-per-call re-measure: 0 record mismatches (`receipts/closure-extend-summary.txt`). |
| R273-6 F1 MINOR (invalid UTF-8 refusal justified as GCC parity) | **Resolved.** Four sites now say the pinned GCC accepts such a byte in a comment or literal, and that S refuses it by decision, fail-closed, as a cost: page `:306`, the cost row `:1367` (remedy: save as UTF-8), the refusal message `:5283-5290` and the S comment `:5236-5248`. No "GCC reads it as UTF-8 too" wording remains (grep). | Re-measured on the pinned GCC: block comment, line comment, string and char literal all give rc 0 at `-E` and `-S`, and warn only under `-Winvalid-utf8` (`receipts/gcc-invalid-utf8.txt`). The gate's mutation "a byte that is not UTF-8, in a comment" stays pinned (280/280, 222/222). |
| R272-5 S1 SUGGESTION (two round-numbering schemes) | **Addressed.** `:1518-1630` uses PR #535's correction rounds throughout, and each ledger paragraph names its commits. I checked those against `git log`: one `75066c16 d8abee3e ef903457`, two `8fd74a99 479a2175 8e12d31f`, three `11b1b86c`, four `4a56ef08`. Other "round N" mentions on the page are explicitly tagged #410. | `git log 759da623..HEAD` and the page. |
| R273-6 S1 SUGGESTION ("every byte in every position") | Subsumed by R272-5 F1 above. The residue is R273-7 F1. | As above |
| Earlier rounds: R272-4 F1 = R273-5 F1 MAJOR, R273-4 F1 BLOCKER, R272-3 F1 MAJOR, R272-2 F1 BLOCKER, R273-3 F1/F2, R272-1 F1-F4, R273-1 F1 | **Resolved, retained.** The round-5 delta does not touch their mechanisms, and every probe case built for them keeps its verdict and pin. | 338 whole-firmware cases × both modes: 0 verdict and 0 pin changes against round four (`receipts/probes-vs-round4.txt`). Round-two gate probe unchanged. Allowlist disconnect: 12/12 fail in both modes, as before. |

## Lens ledger (reviewer-owned)

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Assignment 5816286265 items 1-3 against `_CLOSURE_POSITIONS` `:2774-2839` (23 positions, B1-B14 templates), `_CLOSURE_READERS_REFUSE` `:2970-2977`, `assert_character_closure()` `:5998-6082`, and the four invalid-UTF-8 sites. #408/#409 acceptance 4: 280/280 mutations with the SDK, 222/222 absent, count ≥163, 29/29 + 4/4 accepted edits, 1845/1845 spellings, exit 0 in both modes. Acceptance 1-3 and 5: gate 1b PASS, 0 NOT RUN, 467 compiles (SDK); PASS, 1 NOT RUN, 0 compiles (absent) (`receipts/gate1b/`). "No change to what the gate accepts or refuses": 338 cases, 0 changes. | R273-7 | 991d59653ff82ccf73ef4df9477de1df8c8c5964 |
| RTL | CLEAN | `git diff --name-status 759da623..991d5965` touches no `hdl/` or `sw/firmware/` file. Gate 1b's RTL part at this head, run with the pinned Verilator 5.050 on PATH: 46/46 RTL mutation variants elaborated as the real milan_datapath/milan_csr tops, with the malformed-RTL self-test refused, in both modes (`receipts/gate1b/head-*.log`, `receipts/verilator-identity.txt`). | R273-7 | 991d59653ff82ccf73ef4df9477de1df8c8c5964 |
| Robustness | CLEAN | Out-of-table positions (closure_extend Parts B/C, 8442 cells): 0 cells where both sides read names and differ, and every disagreement fails safe, byte-identical to round four. Boundary probe: 32 spellings, 0 holes. Subset probe: 24 spellings, 0 holes. The lone `#` at end of file is refused by the readers and the directive-set closure. A null directive at end of file, mid-file and with trailing blanks is refused at dev and here in both modes (`nulldir-*`). Invalid UTF-8 is refused in comments and literals, and GCC's acceptance was re-measured. BOM and extended-character cases are unchanged. | R273-7 | 991d59653ff82ccf73ef4df9477de1df8c8c5964 |
| Tests | CLEAN | Independent one-GCC-call-per-cell re-measure of all 6440 cells: 0 record mismatches and 0 outside-vs-allowlist mismatches. The split is 3647/226/246/1/2546, matching the gate print. New-cell sensitivity (`receipts/new-cells-probe.log`): four reader defects each pass both lexer corpora and the nine-position table, and fail only the 23-position table: the author's U+00A0 splice blank, and three of mine (a C23 digit-separator quote, a `*`-blanks-`/` closer, and a backslash that does not escape `"`). A fifth, NUL dropped from splice blanks, is caught by both the corpora and a new cell. Named-refusal controls (`receipts/named-refusal-controls.json`): emptying the name, adding a name the readers do not refuse, and a directive-set closure admitting a nameless directive each fail `assert_character_closure()`; the last trips through the message pin. The U+00B7 negative control is present. | R273-7 | 991d59653ff82ccf73ef4df9477de1df8c8c5964 |
| Docs | **UNCLEAN** (F1) | Page `:302-356` (S rows, closure paragraph), `:1367` (cost row and remedy), `:1518-1630` (round ledger, round-five paragraph), `:1672`. Code comments at `:2717-2773`, `:2970-2977`, `:5226-5248`, `:5283-5290`, `:5557-5569`, `:5998-6008` and **`:11291-11295` (F1)**. Gate print `:15990-16003` and `:15826-15835`. Static checks all exit 0: `docs_check.py`, `check_baremetal_only.py --check` and `--selftest`, `check_em_dash.py --base 759da623`, `check_doc_style.py`, `gen_toc.py --check`, `check_doc_paths.py`, `check_py_idiom.py`, `git diff --check`, `test_firmware_compiler.py --selftest` (`receipts/static-checks.log`). | R273-7 | 991d59653ff82ccf73ef4df9477de1df8c8c5964 |

## Executed evidence (all at 991d5965, foreground)

- **SDK.** Pinned Bootlin `riscv32-ilp32d--glibc--stable-2025.08-1`, archive sha256 `d42680e9...b78f`, installed fresh into scratch and verified by `scripts/ci_rv32_sdk.py --verify-only` (`receipts/sdk-verify.log`). GCC 14.3.0.
- **Verilator.** `<pinned-tool-bin>/verilator` reports "Verilator 5.050 2026-07-01 rev v5.050" (`receipts/verilator-identity.txt`).
- **Gate 1b** (`test_firmware_compiler.py`), both rc 0:
  - SDK mode: GATE 1b PASS, 0 NOT RUN, 467 compiles, 280/280.
  - Absent mode: PASS, 1 NOT RUN, 0 compiles, 222/222.
  - Closure: 6440/6440 in 23 positions (3647 allowlist, 226 closes, 246 other S, 1 named reader refusal, 2546 read). Re-measured on riscv32-linux-gcc with the SDK; "NOT re-measured" without it.
- **Round-four probes, byte-identical** (`receipts/probes-unchanged-vs-r273-6.txt`, 54 files):
  - 10 case files × 2 modes: 338 cases, 0 verdict and 0 pin changes.
  - subset_probe 24/0 holes; boundary_probe 32/0 holes, identical.
  - regex_audit: 197 calls, identical except line numbers.
  - lexer_oracle: 1845 spellings, 0/0 mismatches, identical.
  - closure_extend: Part A 6440 cells re-measured; Parts B/C unchanged cell for cell, 8442 cells. It exits 1 on the raw HOLE count, which is classified in the summary.
  - Round-two gate probe: identical except the compile count, 86 → 147, which is the larger closure re-measure.
  - Allowlist disconnect: 12/12 fail in both modes, identical.
  - round3 lexer_probe: the same pre-existing extractor `NameError`.
- **Round-five probes (new)**, under `probes/round5/`:
  - `new_cells_probe.py`, `named_refusal_controls.py`, the null-directive cases, `closure_summary.py`, `compare_pins.py`;
  - the command record is `probes/round5/RUN.sh`.
- **Clone.** Restored and verified: HEAD, tree, index hash, the worktree equal to HEAD with no untracked or ignored files, blob hashes and modes of the three changed files, and the four submodule gitlinks (`receipts/clone-state-before.txt` = `receipts/clone-state-after.txt`).

## Real limits

- My mutation probes run the gate's own `assert_lexer_matches_compiler()` and `assert_character_closure()`, extracted unmodified, on disposable patched copies. I did not run the whole gate per mutation. The author's claim that the U+00A0 widening passes the whole gate with nine positions is not re-run here.
- The Part B/C positions are a chosen set, not exhaustive. Agreement at positions outside the 23 remains bounded by the corpora, as the corrected sites say.
- Everything ran on one local x86_64 host. Physical calibration was NOT RUN, and field skips are not hardware proof.
- Hosted checks at 991d5965 when I read them (`receipts/hosted-checks-at-review.txt`): rtl-fast, docs-check, Verilator shards 0-3/5, Yosys shards 0-3/4 and the others succeeded. Verilator shard 4/5 was still in progress. The physical gPTP context was skipped, which is not execution. Accepting these is the manager's call.
- The candidate merge against live dev `573f0052` was not built by me.

## Pending manager duties

- Route F1 (MINOR, Docs, comment-only) to a correction. After the correction, Docs must be re-covered at the new head. The other four lenses are banked at 991d5965, but only for artifacts that a comment-only change leaves untouched.
- Build and validate the current-dev candidate merge (source base `759da623`, live dev `573f0052`).
- Accept the hosted and act evidence at the final head, including Verilator shard 4/5.
- Update the PR body.
- Publish this packet: REPORT.md and the files in MANIFEST.sha256.

R273-7 FINISHED
