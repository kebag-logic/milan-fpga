https://github.com/kebag-logic/milan-fpga/pull/519#issuecomment-5782234201
[R251] NEGATIVE - exact head b911c11671cae329a99f5e413133b4bf6357fa7f

Round R251-2, 2026-09-22. Cleared-context internal Codex review of issue #423 / PR #519. Tree: `4dd73d4c4f2ff352e65703d476dcd44494ffdb8e`. Actual source-validation base: `52711029f374650dc93830d5ea28e81cb5c8f410`.

The original false-containment defect and missing regression coverage are corrected. F1 and F2 are resolved at this head, retaining their original classifications and lens ownership below. One separate MINOR remains: an established path assertion fails when the **parent of the default self-test** uses Latin-1. Production containment correctly refuses that fixture; the assertion compares the wrong Unicode representation of its raw filename. Under the repository's completion rule, this open MINOR leaves Conformance, Robustness and Tests unclean. No merge approval is given.

This round covers the whole corrected PR's bounded G1/H/T implementation, existing-arm preservation, filename correction, tests and authoritative wording. It does not rely on another implementation reviewer's approval. Public contracts, source objects and executable evidence were used; no private author/reviewer transcript or scratchpad was read. Nothing was published, committed, pushed or changed in the source checkout. No other agent, hardware, full native/builder bank, Docker/act, host-side candidate runner or privileged operation was used.

The authority chain reconstructed was `AGENTS.md`, `CONTRIBUTING.md`, `docs/README.md`, `REQUIREMENTS.md` including REQ-VER-04, [issue #423](https://github.com/kebag-logic/milan-fpga/issues/423), its [frozen G1/H/T decision](https://github.com/kebag-logic/milan-fpga/issues/423#issuecomment-5777210218), the referenced public R242 design matrix, `docs/reference/SUBMODULES.md`, relevant verification/architecture boundaries, the PR diff/history, and public executable receipts. The [R251-1 findings](https://github.com/kebag-logic/milan-fpga/pull/519#issuecomment-5780883992) were the correction contract; the [R251-2 assignment](https://github.com/kebag-logic/milan-fpga/pull/519#issuecomment-5781826629) expands this review to all five lenses across the bounded PR. Raw public bodies and source diffs are in `raw/`.

[R251] MINOR Tests, Robustness, Conformance - scripts/merge_containment_selftest_retention.py:77; :35; :119 - F3: The default self-test falsely fails its raw-filename diagnostic assertion under a Latin-1 parent process.

Authority/evidence: the settled decision requires preservation of the existing controls and execution through the default self-test. R251 F2 also required keeping the raw-byte/CRLF/literal-path controls. `CONTRIBUTING.md:240` onward records default-selftest ownership and filesystem-encoding coverage. The fixture writes `raw-\udcff` as UTF-8/surrogateescape at line 35, creating literal bytes `72 61 77 2d ff`. At lines 119-123 it passes that original Python string to `_check`; line 77 requires `repr(path)` in the diagnostic. The corrected implementation decodes the same bytes with the actual filesystem encoding. Under `iso8859-1` its diagnostic correctly names `'raw-ÿ'`, while the assertion searches for the different string spelling `'raw-\udcff'`.

Measured evidence at this exact head:

| Execution | Result |
|---|---|
| Default self-test, ordinary UTF-8 parent | 455 assertions pass, exit 0 |
| Default self-test, fresh verified `iso8859-1` parent | 454 pass, 1 fails, exit 1 |
| Original `_path_and_format_cases`, previous head `df53dfa116b34816db0193230ad9833e67bf46dd`, UTF-8 / Latin-1 | 22/22 / 22/22 |
| Same unchanged path controls, corrected head, UTF-8 / Latin-1 | 22/22 / 21/22 |

The sole failing full-suite assertion is `retention-literal-revert-'raw-\udcff'-path`. The immediately preceding assertion still receives the required `UNKNOWN / 1`. The corresponding positive fixture remains `contained / 0` through raw retention. Independent byte round trips show `os.fsencode(os.fsdecode(b'raw-\xff')) == b'raw-\xff'`; the production diagnostic is not evidence of lost path bytes.

Raw receipts: `raw/parent-latin1-selftest.{json,stdout,stderr}`, and `raw/parent-locale-focused/{previous,corrected}-{utf-8,iso8859-1}/result.json`. Each focused receipt includes the actual encoding, all 22 comparisons and the captured production CLI output. `scripts/check_parent_locale.py` recreates the comparison and optionally the complete failing default invocation with `--full`; the comparison driver's exit 0 means it reproduced the expected failure matrix, not that the corrected Latin-1 self-test passed.

Impact: a supported filesystem-encoding environment gets a false failure from the required default gate, despite correct containment. `scripts/run_all_suites.sh:249` consumes that nonzero self-test result and aborts. This is a test portability regression, not another false containment success; hence MINOR rather than BLOCKER or MAJOR. All three attributable lenses are recorded because the defect is an assertion error, depends on runtime configuration, and fails the preserved-control acceptance obligation.

Required outcome: preserve the byte-defined fixture and its exact path assertion, while making the expected diagnostic representation consistent with those bytes in the actual process encoding. The full default self-test must pass under the measured UTF-8 and Latin-1 parents. Do not skip/remove the raw-name assertion or weaken any containment verdict.

Verification: rerun `scripts/check_parent_locale.py` against the correction and require both current-head path populations to pass 22/22; run the complete default self-test in both actual encodings. Retain the original negative examples, retained positive examples, patch-byte checks and four restoration detections. A later source change needs a new review; this report does not approve a prospective fix.

The original finding dispositions are:

| Original finding and unchanged ownership | Disposition at b911c11671cae329a99f5e413133b4bf6357fa7f | Evidence |
|---|---|---|
| F1 BLOCKER, Conformance / Robustness, R251 | RESOLVED | Both original false passes now refuse in UTF-8 and Latin-1; direct path/postimage, retention enumeration, entry and returned-name checks preserve original bytes. |
| F2 MAJOR, Tests / Conformance, R251 | RESOLVED for its original missing-regression-coverage defect | The default suite owns actual UTF-8/ASCII/Latin-1 child controls with raw names, aliases, positives, negatives, entry/postimage and patch checks; all four independent single-site restorations are detected. F3 records the separate remaining parent-locale assertion defect; it does not downgrade F2 or clear the affected lenses. |

F1 resolution artifacts: `scripts/check_merge_containment.py:94-102` uses `os.fsdecode` for shared Git output; `:160` supplies the matching `os.fsencode` patch inverse. `_commit_paths`, `_same_patch_postimage`, `_path_scoped_verdict`, `_differing_paths` and `active_graft_error` retain that representation when forwarding paths. `scripts/merge_containment_replay.py:127` uses filesystem decoding for net-changed names and `:72` validates returned name bytes with filesystem encoding. Raw subprocess output avoids universal-newline conversion. These uses match the documented filesystem encoding/error-handler pair in [Python's os API](https://docs.python.org/3/library/os.html#os.fsdecode).

`scripts/run_public_examples.py` re-executes the immutable original public shell fixture. Only its source-head selector and displayed head label change to this review head; its fixture histories and base remain intact. The source and base results are:

| Original example | Corrected source, UTF-8 | Corrected source, Latin-1 | Base, both encodings |
|---|---|---|---|
| Never-landed linear edit | STRANDED / 1 | STRANDED / 1 | STRANDED / 1 |
| Replay followed by reverted non-ASCII edit | UNKNOWN / 1 | UNKNOWN / 1 | STRANDED / 1 |

Restoring the source filename content in each disposable history supplies six additional positive controls: linear and redundant-merge shapes in UTF-8, ASCII and Latin-1 all return `contained / 0`. Each merge positive explicitly names the raw-retention fallback. Receipts are `raw/public-examples/` and `raw/public-examples-run.*`.

`scripts/transport_probe.py` independently builds raw `mktree` records rather than using the production decoder or committed fixture constructors. All 29 checks per encoding pass in fresh `utf-8`, `ascii` and `iso8859-1` processes, 87 checks total. Names include `c3 a9`, invalid `ff`, euro and four-byte musical-symbol UTF-8 sequences, and literal pathspec/control/newline characters. An unchanged distinct `e9` alias exists beside the changed `c3 a9` name. Repository-directory bytes are also non-ASCII. The probe checks original bytes in Git arguments, unequal postimages, exact entries, retention's unproved-path list, graft-file pathname transport, malformed/aliased returned-record refusal, and four complete CLI histories. Actual Git arguments and outputs are saved in `raw/transport/*-gitcalls.json`.

The patch probe captures the actual `patch-id` input and compares it with raw `git show` output after the helper's existing trailing-LF removal. Embedded CRLF and invalid bytes are preserved exactly; this does not claim that the helper stopped stripping its pre-existing trailing LF terminators. Blob retention continues to compare complete raw bytes. The first independent probe attempt used the RTK text wrapper as its invalid-byte argv oracle and got an empty lookup for the raw filename `b"raw-\xff.txt"`; that attempt failed. The corrected oracle passes raw byte argv directly to native Git from Python. Both scripts/receipts remain in `raw/transport-initial*` and `raw/transport/`; the first attempt is not passing coverage or a source finding. Every shell invocation still used RTK.

F2 resolution artifacts: `scripts/merge_containment_selftest.py:132-137` invokes locale controls from the default owner. `scripts/merge_containment_selftest_locale.py:22-43` creates raw tree records, `:52-71` supplies distinct histories and the unchanged alias, `:86-135` asserts the actual encoding and measured outcomes, and `:150-178` starts fresh processes and reports unavailable Latin-1 support as NOT RUN. In this review all three encodings executed. No NOT RUN result is counted as coverage.

`scripts/run_restorations.py` changes one conversion site at a time in disposable source copies and executes the full default self-test. Shared decoding, patch inverse, retention decoding and returned-name validation restorations each exit 1. The unmodified source exits 0 under the same ordinary parent environment. Raw logs are in `raw/restorations/`; `precise-failure-index.json` identifies actual FAIL lines. Some decoder restorations make a locale child raise on an unencodable name, which the parent correctly counts as a failed process assertion. No mutant was credited merely for completing, and no production source was edited.

The broader G1/H/T review produced these results:

| Contract portion | Examined artifacts and executed evidence | Result |
|---|---|---|
| Existing arms and order | `check_merge_containment.py:529-590`; `raw/function-preservation.json`; base/head self-test comparison | Ancestry, touched-path and linear historical arms run before the new fallback. Their helpers are structurally unchanged except the deliberately corrected shared transport. All original 145 assertion names/results/order are preserved under the normal parent environment. |
| G1 exact shape | `merge_containment_replay.py:37-57`; public matrix rows 3, 21-29; default guard mutations | Exactly one source-only merge, exactly two ordered parents, sole direct parent relation and equal merge/second-parent trees. Multiple/distant/reversed/unrelated/octopus/resolution shapes retain refusal. |
| H exact replay | `check_merge_containment.py:153-235`; matrix rows 17-20; byte/postimage probes | Every non-merge source commit consumes a distinct candidate with verbatim patch identity and matching touched-path postimages. Missing work, whitespace differences and repeated-location mismatch refuse. |
| T current retention | `merge_containment_replay.py:60-135`; matrix rows 1-16; retention type/mode/path controls | One merge base; no rename folding; mode/kind/OID identity includes absence. Otherwise only the allowed regular-blob/mode relation reaches raw merging. Both clean exit and byte-identical tip output are required. |
| Failure boundaries | `merge_containment_replay.py:137-159`; `merge_containment_selftest_retention.py:183-229`; executed default log | Missing objects, failed/malformed measurements, storage errors, no/multiple merge bases and binary merge errors remain non-success. G1/H declines preserve existing results; unproved T names paths and returns UNKNOWN. |
| Raw merge/configuration boundary | `merge_containment_replay.py:79-112`; retention controls `:85-179`; default/public matrices | Symlinks, gitlinks and nonregular types need exact identity. Tests cover absence, modes, CRLF, literal/invalid names and hostile drivers/textconv/filter configuration. Configured driver marker files are not created. |
| Bounded alignment evidence | `merge_containment_selftest_retention.py:135-152`; public repeated-block and partial-revert rows; guard mutation for tip equality | Executed repeated-block controls refuse their lost-work cases and keep positives. No general alignment or semantic-preservation theorem is claimed. |

Git documents clean/conflicted/error outcomes for the three-way operation and warns that alignment can cause mismerges; this review accepts only the settled bounded byte-level criterion, not arbitrary semantic preservation. The implementation passes no ours/theirs/union option and uses raw temporary blob files. [Git merge-file documentation](https://git-scm.com/docs/git-merge-file).

`scripts/run_public_matrix.py` uses the unchanged published 31 fixture builders and frozen expectations, adapting only the helper interface for component observations. It reproduces all 31 original source/target OID pairs exactly and asserts verdicts and exits. The required distant-extension positives pass; adjacent extensions and later lost-work cases stay UNKNOWN; G1/H failures stay STRANDED; existing linear revert/adjacent-extension controls stay contained. The normal default run also executes all ten published guard mutations through 25 targeted changed-verdict assertions. Evidence: `raw/public-matrix/matrix.json`, `raw/public-matrix/existing-arm-preservation.json`, `raw/selftest.stdout`.

Actual public donor history was independently reconstructed read-only from the registered gPTP submodule's stored objects. `scripts/reconstruct_history.py` verifies the ordered `f27b455` parents, its tree identity with `9790ac7`, both exact original/replay patches and touched-path postimages. The issue's SHA-256 values reproduce with `git diff --no-ext-diff --no-textconv --no-renames <parent> <commit>`:

| Original / replay pair | Exact patch SHA-256 |
|---|---|
| `9790ac736e6d10301ad814ffdf73dbe37b59768b` / `20927af74752620b2ad0f973e8be3203994b5547` | `d3d164b309e376ea06a3734e8452dd5668c4721d0462dc0656af05d6b3c155b3` |
| `3db86812096830fada2f5f276fa5f4d9f37d1d14` / `5602e70bb4cf70c2e0e39e846e26925e27659e32` | `fa20a2516a4d866a859506c5396779fb98bbafe943e4de2651e9ec252bca996f` |

At **both** `f0f1c055ee5226f08e656c27cb1bf4c355be11ae` and `c1b617435824929a790739ea8585c3fe1a328cc0`, actual PR62 has G1/H true and T unproved for `tb/tsngen/mutants.py` and `tb/verilator/gaskets/mutants.py`. The corrected CLI is UNKNOWN / 1; the base is STRANDED / 1. PR61 remains contained / 0 under both versions. These are measured outcomes, not a donor audit waiver. [Issue #514](https://github.com/kebag-logic/milan-fpga/issues/514) alone owns the broader existing historical-retention policy. Full raw commit, patch, entry and CLI receipts are in `raw/history/`.

[R251] PASS RTL - raw/source-diff.txt; raw/changed-paths.txt; docs/reference/SUBMODULES.md:13; scripts/check_merge_containment.py:529 - The exact base-to-head diff changes CONTRIBUTING and seven Python checker/test files only. No RTL, CDC/reset/timing, wire protocol, firmware interface, workflow scheduling or gitlink changes are present. Product-hardware lenses are therefore inapplicable to the change. The tooling call order, 0/1/2 plus self-test cleanup-3 interface, and suite-consumer boundary were examined; F3 is the test expectation defect recorded above.

[R251] PASS Docs - CONTRIBUTING.md:209-258; scripts/check_merge_containment.py:44-58; docs/README.md:41; raw/issue423.json; raw/pr519.json - The final wording matches the settled narrow G1/H/T rule, mode restriction, no-driver/raw-byte boundary, historical/current-retention distinction, deliberate unresolved PR62/adjacent histories, #514 ownership and NOT RUN limits. Exact patch-hash reproduction is provided. Public evidence identifies its source and base and does not supply final-candidate or hardware proof. Focused `docs_check.py`, Python idiom and exact base/head whitespace checks pass; receipts are `raw/docs.*`, `raw/python-idiom.*`, `raw/whitespace.*`.

This is the reviewer-owned completion ledger. All five lenses were applied in this round to the exact head named in every row. Clean coverage is banked only where no finding remains under that lens.

| Lens | Covering/review round | Exact examined head | Status |
|---|---|---|---|
| Conformance | R251-2 | b911c11671cae329a99f5e413133b4bf6357fa7f | NOT CLEAN: F3 MINOR open; F1/F2 resolved |
| RTL | R251-2 | b911c11671cae329a99f5e413133b4bf6357fa7f | CLEAN, with product-hardware inapplicability evidenced above |
| Robustness | R251-2 | b911c11671cae329a99f5e413133b4bf6357fa7f | NOT CLEAN: F3 MINOR open; F1 resolved |
| Tests | R251-2 | b911c11671cae329a99f5e413133b4bf6357fa7f | NOT CLEAN: F3 MINOR open; original F2 coverage defect resolved |
| Docs | R251-2 | b911c11671cae329a99f5e413133b4bf6357fa7f | CLEAN |

AC1-3's bounded implementation/history expectations are reproduced. AC4 is not complete: the parent-locale self-test finding remains, the external review is outstanding, and this source review cannot complete the manager's remaining integration/CI/merge duties.

Public full-gate evidence was downloaded from immutable commit `bdd708eb8a5548f8ab1a011b8402b715f5a00ff5`, restricted to source/native artifacts and necessary factual reproduction inputs. Every one of 256 selected blobs independently hashes to its tree-listed Git blob ID; `raw/evidence-verification.json` also records SHA-256. The complete source ledger and raw logs under `public/corrected-source2/manager/` report **49/49 static/builder commands and five native commands exiting 0**, bound to this source and actual base `52711029...`. The native logs show 55/55 parent suites, the portability gate, both pinned processor groups, and 316 passing behavior scenarios. These are manager executions inspected as public evidence, not executions performed by this reviewer. The separately reproduced Latin-1 parent failure qualifies the passing default-environment claim; it does not relabel those measured passes as failed runs.

Physical calibration gate 11 is explicitly NOT RUN. Four parent field/freshness skips executed zero checks. The xvlog log reports four existing ratcheted processor findings, not a finding-free donor. None is hardware proof. Scoped Verilator 5.050 appears in the public native receipts; this reviewer did not need or execute Verilator. No Actions/run/check API, `gh run`, `gh pr checks` or `statusCheckRollup` was inspected. Public explicit PR metadata was read only to verify the published head.

R244 external Opus remains required and pending availability; it is not replaced or waived. Manager trusted-replica/hosted evidence collection and final current-dev candidate work remain outside this review's completed evidence. GitHub's recorded PR base OID is not relabeled as the validation base. Authorized merge, post-merge containment, final hosted evidence and Closed/Done obligations remain pending. A source review is not candidate-merge validation.

Final tracked integrity passed independently of Git status: all **856 root blobs** match committed bytes, kind and executable mode; every root index record matches HEAD and stage 0. The three required submodules are real registered directories at the root gitlinks; their tracked files and indexes were independently verified:

| Submodule | Exact gitlink/HEAD | Verified tracked files |
|---|---|---:|
| third_party/verilog-axis | 48ff7a7e2ef782cf778d47910cf85835c64b1bce | 214 |
| protocol-processor | 424c688fa2205b934a7689a58f2aa766420f2326 | 222 |
| gptp-processor | c1b617435824929a790739ea8585c3fe1a328cc0 | 103 |

`raw/final-integrity.json` and `raw/integrity-comparison.json` show identical before/after head/tree, tracked bytes/kinds/modes, raw index hashes, index entries and clean status for root and required submodules. Optional `external` stays uninitialized under the documented exclusion. Final explicit PR metadata still names this published head.

Tools: Python 3.14.7, Git 2.55.0, glibc localedef 2.44, RTK 0.43.0. Scratch locale data and all mutated Git histories/source copies were confined to new temporary directories. At most four probe/fixture workers overlapped; no eight-job limit was approached. Factual reproduction instructions are in `REPRODUCE.md`. This report, scripts and raw receipts contain no private reasoning and are delivered for manager publication only.

R251-2 FINISHED
