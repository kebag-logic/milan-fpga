[R251] POSITIVE - exact head 4671e582cfa4bba4809b9e3a354ce5b6eb967f99

Round R251-3, 2026-09-22. Cleared-context internal Codex source review of kebag-logic/milan-fpga issue #423 / PR #519. Tree: `afc8eadb3e9f6611dfb62347580b49dc721d25c0`. Actual source-validation base: `52711029f374650dc93830d5ea28e81cb5c8f410`.

F3 is resolved at this exact head, retaining its original MINOR severity and all three lenses: Tests, Robustness and Conformance. F1 BLOCKER Conformance/Robustness and F2 MAJOR Tests/Conformance remain resolved. No new finding remains open. This is a positive internal source verdict. External R244 Opus, manager CI evidence, final current-dev candidate validation and the remaining merge obligations are still pending; this report does not complete them.

The review reconstructed `AGENTS.md`, `CONTRIBUTING.md`, `docs/README.md`, `REQUIREMENTS.md` including REQ-VER-04, the [issue's frozen acceptance and G1/H/T decision](https://github.com/kebag-logic/milan-fpga/issues/423#issuecomment-5777210218), linked public R242 criterion, `docs/reference/SUBMODULES.md`, `docs/overview/ARCHITECTURE.md`, the checker/suite interface, diff/history, and public executable evidence. The [R251-3 assignment](https://github.com/kebag-logic/milan-fpga/pull/519#issuecomment-5783269167), [R251-1 findings](https://github.com/kebag-logic/milan-fpga/pull/519#issuecomment-5780883992) and [R251-2 report](https://github.com/kebag-logic/milan-fpga/pull/519#issuecomment-5782234201) define this correction review. Authority snapshots, public bodies and exact diffs are under `raw/`; immutable public receipts are under `public/`. No private author/reviewer transcript or scratchpad was read.

Git-object proof, independently recorded in `raw/object-identity.json` and `raw/fix-diff.txt`, establishes:

- `b911c11671cae329a99f5e413133b4bf6357fa7f` is the direct parent, not merely a similarly named source.
- Of 860 tracked entries, 859 have identical path, mode, kind and object ID. The sole changed blob is `scripts/merge_containment_selftest_retention.py`, mode `100644`, from `1e95a499e314aa2b711cdcb0050cfde943df22a5` to `389a4bb65e552ed8a0e052672e07f46dc383c987`.
- Replacing the new expectation and its explanatory comment with the old expression reproduces the complete b911 blob byte-for-byte. No production code, fixture bytes, verdict expectation, assertion population or other file changes.
- Within that file, only `_check` changes. `_tree`, `_history`, `_path_and_format_cases`, entry/mode/type controls, alignment controls, failure controls, hostile-configuration controls and the default owner are unchanged.

The production checker, replay proof, locale controls, other tests, authoritative documentation, suite consumer and all gitlinks are identical to R251-2. I explicitly accept that round's clean RTL coverage at b911 and its clean authoritative-documentation coverage after examining the public report, supporting receipts and this ancestor/artifact proof. I also accept its clean results for the unchanged G1/H/T subscopes, without treating its three F3-affected lenses as previously clean. Fresh coverage below resolves those lenses at the current head. The unchanged external 31-case historical matrix was inspected, not re-executed to accumulate another round.

[R251] RESOLVED F3 (original MINOR; Tests, Robustness, Conformance) - `scripts/merge_containment_selftest_retention.py:35`, `:77`, `:79`, `:121`; `raw/parent-locales/` - the diagnostic expectation now follows the actual filesystem representation of the fixed filename bytes.

Authority/evidence: the frozen decision and F2 require preserving the literal/raw-name controls and running them through the default self-test. `_tree` writes `path.encode("utf-8", "surrogateescape")`; the raw-name fixture therefore creates bytes `72 61 77 2d ff`, independently of the parent's encoding. The former `repr(path)` expectation used `'raw-\udcff'`. In an actual `iso8859-1` process, production correctly names those same bytes as `'raw-ÿ'`. The new expression first reconstructs the fixture bytes and then uses `os.fsdecode`; the exact `repr(...) in output` assertion remains. This use matches [Python's filesystem decode/encode contract](https://docs.python.org/3/library/os.html#os.fsdecode).

Original impact: the mandatory self-test falsely failed despite a correct `UNKNOWN / 1` containment refusal. `scripts/run_all_suites.sh:250` consumes that result and aborts on failure. The required outcome was to correct the expectation while preserving the fixture, diagnostic assertion and containment verdicts. That outcome is met.

Verification: `scripts/check_parent_locale.py` starts fresh interpreters with UTF-8 mode and locale coercion explicitly disabled, asserts the measured filesystem encoding, captures every focused comparison and production CLI output, and checks raw `ls-tree` bytes. Latin-1 data is compiled into a disposable directory. A second disposable source copy restores the entire b911 retention blob, which the Git-object proof shows is exactly the original expression restoration.

| Source and measured parent encoding | Focused path controls | Full default assertions | Full exit |
|---|---:|---:|---:|
| Current, `utf-8` | 22/22 | 455/455 | 0 |
| Current, `iso8859-1` | 22/22 | 455/455 | 0 |
| Exact b911 assertion restored, `utf-8` | 22/22 | 455/455 | 0 |
| Exact b911 assertion restored, `iso8859-1` | 21/22 | 454/455 | 1 |

The restoration's sole failure is `retention-literal-revert-'raw-\udcff'-path`. Its preceding verdict remains `UNKNOWN / 1`; its positive control remains `contained / 0` through raw retention. All focused production CLI outputs are identical between current and restored copies for each encoding. Both copies write `7261772dff`, and filesystem decode/encode returns those exact bytes. This precisely reconstructs F3 as a test expectation failure, not a production false pass. Receipts: `raw/parent-locales/processes.json`, each child `result.json`, `process.json`, `focused.stdout/stderr`, and `full.stdout/stderr`.

[R251] RESOLVED F1 (original BLOCKER; Conformance, Robustness) - `scripts/check_merge_containment.py:94`, `:160`, `:169`, `:180`; `scripts/merge_containment_replay.py:61`, `:72`, `:127` - literal Git filename bytes remain preserved through arguments, postimages and retention.

Authority/evidence: AC3 and G1/H/T require refusal of missing work and unproved retention. The original failure decoded valid UTF-8 filename bytes `c3 a9` into U+00E9 and resubmitted them as different Latin-1 bytes `e9`, allowing proof of the wrong path. Production still uses filesystem decoding plus its matching encoding inverse, raw subprocess output, and exact returned-name validation. Those production blobs are identical to R251-2.

Original impact: missing or reverted work could return false `contained / 0`. Required outcome: exact filename-byte transport, correct postimage/entry measurements and nonzero refusal of both original counterexamples. Fresh verification re-executed the immutable original fixture, adapting only the selected head and its displayed label. Both never-landed linear examples return `STRANDED / 1`; both reverted redundant-merge examples return `UNKNOWN / 1`, under UTF-8 and Latin-1. The unchanged base returns `STRANDED / 1` for both shapes. Six retained positive controls, the two shapes under UTF-8/ASCII/Latin-1, return `contained / 0`; merge positives explicitly name raw retention. Receipts: `raw/public-examples/` and `raw/public-examples-run.*`.

The independent raw-tree transport probe also passes 29 checks in each of fresh `utf-8`, `ascii` and `iso8859-1` processes: 87 checks. It uses raw mktree records and native byte argv, with changed `c3 a9` and an unchanged distinct `e9` alias; invalid `ff`; euro and four-byte musical-symbol names; literal pathspec/control/newline bytes; and a non-ASCII repository directory. It checks exact argv bytes, unequal postimages, actual mode/kind/OID entries, unproved paths, malformed/aliased returned records, graft-path handling and four complete CLI histories. Exact patch-ID input equals raw Git output after the helper's existing trailing-LF removal; embedded CRLF and invalid bytes remain intact. This does not claim the pre-existing trailing-LF stripping changed. Receipts: `raw/transport/*-checks.json`, `*-gitcalls.json`, raw CLI output and `processes.json`.

[R251] RESOLVED F2 (original MAJOR; Tests, Conformance) - `scripts/merge_containment_selftest.py:132`, `scripts/merge_containment_selftest_locale.py:22`, `:52`, `:86`, `:150`; `raw/restorations/` - the default owner retains defect-detecting locale controls.

Authority/evidence: the frozen decision and AGENTS Tests lens require byte-defined fixtures, real process encodings, positives/negatives, unchanged controls and tests that detect their claimed defect. Original impact: 22 green path checks did not expose either Latin-1 false pass. Required outcome: the default suite owns the added locale population, while established raw-name/CRLF controls remain. Source identity proves no locale control was removed; the two current full defaults execute all 455 assertions, including actual UTF-8/ASCII/Latin-1 children. `raw/control-preservation.json` proves all 455 names/order match the R251-2 passing default and the first 145 match its archived original baseline population, in both current parents.

Four independent single-site restorations in disposable copies each cause the full default to exit 1:

| Restoration | Actual failed assertions | Outcome |
|---|---|---|
| Shared Git-output UTF-8 decoder | ASCII and Latin-1 child-process assertions | detected |
| Hard-coded UTF-8 patch inverse | four Latin-1 patch-byte assertions | detected |
| Retention's UTF-8 path decoder | ASCII and Latin-1 child-process assertions | detected |
| Hard-coded UTF-8 returned-name validation | Latin-1 child-process assertion | detected |

Some restored decoders make a child raise on an unencodable name; the default owner correctly treats that process failure as a failed assertion. `raw/restorations/precise-failure-index.json` counts actual `FAIL` prefixes, excluding the passing explanation containing the word `FAILS` and the final failure summary. The original public restoration driver and all raw output remain preserved.

Unavailable-locale handling was also executed, not mocked: a disposable PATH contains Git but neither `locale` nor `localedef`. The production `locale_cases` emits `NOT RUN locale-iso8859-1: localedef unavailable and no Latin-1 locale installed`, executes 86 passing UTF-8/ASCII assertions, and records zero Latin-1 assertions. No skipped population is counted as validation. This tests tool unavailability; it does not claim every possible localedef failure environment was simulated. Receipts: `raw/unavailable-locale/`.

The accepted unchanged coverage remains bounded:

| Scope | Actual examined artifacts and evidence | Accepted result |
|---|---|---|
| Existing arms and order | `check_merge_containment.py:529`; `public/reviews/R251-2/raw/function-preservation.json`; current original-145 comparison | Ancestry, touched-path and historical linear replay precede the final fallback; their historical policy remains unchanged. |
| G1 and H | `merge_containment_replay.py:37`; `check_merge_containment.py:153`; public R251-2 matrix rows 3, 17-29 | Exactly one two-parent merge, sole ordered parent relation and tree equality; distinct exact replay patches and postimages. Rejected shapes and missing work remain refused. |
| T and failure boundaries | `merge_containment_replay.py:60`; unchanged retention controls; public R251-2 matrix rows 1-16 | One merge base, raw net paths, mode/kind/OID identity or permitted regular-blob/mode relation with clean raw merge and exact tip equality. Absence, types, modes, CRLF, hostile configuration and measurement errors keep their bounds. |
| Repeated blocks and guard sensitivity | `merge_containment_selftest_retention.py:137`; `merge_containment_selftest_mutations.py:16`; current full defaults | Existing repeated-block controls and ten guard mutations still execute. This is bounded evidence, not a general semantic-preservation or alignment theorem. |
| Actual donor history | `public/reviews/R251-2/raw/history/history.json`, stored commit/raw-patch receipts; `raw/accepted-prior-evidence.json` | Seven commit objects and both patch pairs independently match the local donor objects. Prior PR62 `UNKNOWN / 1` evidence is accepted at both named target commits. |

The two original/replay patch SHA-256 values reproduce from `git diff --no-ext-diff --no-textconv --no-renames <parent> <commit>`: `d3d164b309e376ea06a3734e8452dd5668c4721d0462dc0656af05d6b3c155b3` for `9790ac7` / `20927af`, and `fa20a2516a4d866a859506c5396779fb98bbafe943e4de2651e9ec252bca996f` for `3db8681` / `5602e70`. The accepted R251-2 executions show G1/H true and T unproved for `tb/tsngen/mutants.py` and `tb/verilator/gaskets/mutants.py` at both `f0f1c055ee5226f08e656c27cb1bf4c355be11ae` and `c1b617435824929a790739ea8585c3fe1a328cc0`. PR62 remains UNKNOWN. These historical CLI executions were not repeated in R251-3. [Issue #514](https://github.com/kebag-logic/milan-fpga/issues/514) alone owns broader historical-retention policy. The frozen decision adopts only the bounded raw-merge criterion; [Git's merge-file documentation](https://git-scm.com/docs/git-merge-file) does not establish preservation of arbitrary semantic rewrites.

[R251] PASS Conformance - `scripts/merge_containment_selftest_retention.py:35`, `:77`, `:121`; frozen issue decision; `raw/control-preservation.json`; `raw/accepted-prior-evidence.json` - F3's byte-defined expectation now meets the preserved-control obligation; F1/F2 remain resolved, and unchanged G1/H/T acceptance is reconstructed and accepted as above.

[R251] PASS RTL - `raw/changed-paths.txt`, `raw/fix-diff.txt`, `raw/object-identity.json`; `scripts/check_merge_containment.py:529`; `scripts/run_all_suites.sh:250`; `docs/reference/SUBMODULES.md:13` - R251-2 clean coverage is accepted at its actual b911 head after whole-tree identity proof for this scope. The entire PR changes CONTRIBUTING and seven checker/test Python files. No RTL, reset/CDC/timing, wire protocol, firmware interface, workflow scheduling or gitlink changes exist. The tool's call order and 0/1/2 plus cleanup-3 consumer interface remain unchanged. Product-hardware review is inapplicable to this diff.

[R251] PASS Robustness - `scripts/merge_containment_selftest_retention.py:77`; `scripts/merge_containment_selftest_locale.py:150`; `raw/parent-locales/`, `raw/transport/`, `raw/unavailable-locale/` - Actual parent encodings, raw/alias names, negative and positive outcomes, faulty restorations and unavailable tools were exercised. F1 and F3 are closed; unchanged type/mode/configuration/error bounds are accepted from the identified R251-2 artifacts.

[R251] PASS Tests - `scripts/merge_containment_selftest.py:132`; `scripts/merge_containment_selftest_retention.py:77`; `raw/control-preservation.json`; `raw/restorations/precise-failure-index.json`; `raw/parent-locales/processes.json` - Every established assertion remains, the restored b911 expression detects precisely F3, and all four conversion restorations fail the default gate. F2/F3 are closed. Focused Python-idiom and exact base/head whitespace checks also pass (`raw/python-idiom.*`, `raw/whitespace.*`).

[R251] PASS Docs - `CONTRIBUTING.md:209`, `scripts/check_merge_containment.py:44`, changed test comment at `merge_containment_selftest_retention.py:77`, `raw/issue423-body.md`, `raw/pr519-comment-17.md`, `raw/manager-evidence-assessment.json` - R251-2 clean authoritative wording is explicitly accepted by identical blobs. Fresh review of the added comment and current public source/native claims finds them consistent with the measured correction, source/base identities, deliberate PR62 limitation, #514 ownership and NOT RUN limits.

This is the reviewer-owned current completion ledger. The inherited row names its actual covering head; no executor ledger is used. No MINOR, MAJOR or BLOCKER remains open under these source-review lenses.

| Lens | Actual covering round | Exact covering head | Current status and scope |
|---|---|---|---|
| Conformance | R251-3 | 4671e582cfa4bba4809b9e3a354ce5b6eb967f99 | CLEAN; fresh F3/F1/F2 checks plus explicitly accepted unchanged R251-2 subscopes |
| RTL | R251-2, explicitly accepted by R251-3 | b911c11671cae329a99f5e413133b4bf6357fa7f | CLEAN; ancestor and all artifacts in this scope unchanged; product-hardware inapplicability proved |
| Robustness | R251-3 | 4671e582cfa4bba4809b9e3a354ce5b6eb967f99 | CLEAN; actual locale/fault controls plus accepted unchanged boundaries |
| Tests | R251-3 | 4671e582cfa4bba4809b9e3a354ce5b6eb967f99 | CLEAN; fresh affected tests, full defaults and restoration detections |
| Docs | R251-3 | 4671e582cfa4bba4809b9e3a354ce5b6eb967f99 | CLEAN; current comment/evidence checked; unchanged authoritative wording inherits accepted R251-2 coverage at b911 |

AC1-3 are satisfied within the frozen bounded decision, supported by the named inherited historical evidence and fresh correction controls. AC4's source checks now pass, but AC4 and task completion remain pending the external review and manager integration/CI/merge obligations. Root A10 wrote this fix and cannot approve it. R244 Opus remains pending availability, is separately required and is not waived.

Public manager evidence was downloaded from immutable commit `2738c16fa8f75bbd9193105f1cb633729d2d736d`, limited to source/native receipts and public factual reproduction inputs. All 374 selected blobs independently hash to the tree-listed Git blob IDs; `raw/evidence-verification.json` also records SHA-256. The [current manager packet](https://github.com/kebag-logic/milan-fpga/tree/2738c16fa8f75bbd9193105f1cb633729d2d736d/review-evidence/423-r1/corrected-source3/manager) binds 49 static/builder commands and five native commands, each exit 0, to this source and actual base `52711029...`. Command inventories match their result records. Raw native logs record 55/55 parent suites, Yosys portability, both pinned processor groups and 316 passing behavior scenarios. These are inspected manager executions, not executions performed by this reviewer.

Limits in those receipts remain explicit: builder gate 11 did NOT RUN because its physical calibration report was unavailable (`manager-builder/49.log:251`); four parent field/freshness skips executed nothing (`full-native/01.log:61`); the xvlog pass retains four ratcheted processor findings (`manager-builder/34.log:1`). None supplies hardware proof. The manager's scoped Verilator 5.050 is recorded in its receipts. No Verilator execution was relevant to this expectation-only correction, and this reviewer did not invoke it.

The initial evidence-audit helper incorrectly required every successful command's log to be nonempty; the successful `git diff --check` log is correctly empty. That reviewer-helper assertion failed and was corrected to check the recorded exit and existence of the raw log. Both helper versions and receipts are preserved as `raw/evidence-assessment-initial*` and `raw/evidence-assessment.*`. This is not a source finding or a failed source gate.

Final tracked integrity matches the initial receipt exactly: 856 root blobs have committed bytes, file kinds and executable modes, and the full index matches HEAD at stage 0. Each required submodule is a real registered directory at its exact root gitlink with matching tracked files and index:

| Required submodule | Exact gitlink/HEAD | Verified tracked files |
|---|---|---:|
| third_party/verilog-axis | 48ff7a7e2ef782cf778d47910cf85835c64b1bce | 214 |
| protocol-processor | 424c688fa2205b934a7689a58f2aa766420f2326 | 222 |
| gptp-processor | c1b617435824929a790739ea8585c3fe1a328cc0 | 103 |

`raw/initial-integrity.json`, `raw/final-integrity.json` and `raw/integrity-comparison.json` include direct byte hashing, modes, kinds, raw index hashes and index-entry hashes rather than relying on status alone. Optional `external` remains outside the documented required population. Final explicit PR metadata still names the reviewed head. Its recorded base OID is not substituted for the actual source-validation base or a final current-dev candidate.

No Actions/run/check API, `gh run`, `gh pr checks` or `statusCheckRollup` was inspected. No full parent/PP/gPTP/Yosys/builder bank, Docker/act, candidate host orchestrator or its selftest, hardware, privilege, shared install, other agent or author contact was used. No source edit, commit, push or public comment/metadata mutation was made. Scratch source copies, fixture repositories and locale data were disposable. Focused work used at most six concurrent workers, within the eight-job limit. Tools: Python 3.14.7, Git 2.55.0, RTK 0.43.0 and glibc localedef 2.44. Reproduction instructions and script provenance are included.

Manager trusted-replica/hosted evidence and final current-dev candidate validation remain outside this source verdict. Authorized merge, post-merge containment, Closed/Done state and the external positive review are not claimed. This packet is delivered for faithful manager publication after terminal execution; the reviewer has not self-published.

R251-3 FINISHED
