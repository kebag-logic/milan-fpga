https://github.com/kebag-logic/milan-fpga/pull/519#issuecomment-5780883992
[R251] NEGATIVE — exact head df53dfa116b34816db0193230ad9833e67bf46dd

Round R251-1, 2026-09-22. Independent, narrowly scoped source review of literal Git filename bytes across Python decoding and subprocess argument encoding. Base: `52711029f374650dc93830d5ea28e81cb5c8f410`. Both published examples establish regressions: the candidate returns success for missing work under Latin-1 where the base refuses it. The two findings below remain open.

This report uses public source, the public contract and published executable evidence. No private author/reviewer session was consulted. The prior R251 execution supplied no verdict; this assessment does not replace the separate external review. It is neither whole-PR approval nor merge authorization. No source was modified, and no commit, push, publication, external-system test or other agent was run.

The governing sources are [Issue #423](https://github.com/kebag-logic/milan-fpga/issues/423), its [settled G1/H/T decision](https://github.com/kebag-logic/milan-fpga/issues/423#issuecomment-5777210218), `CONTRIBUTING.md:209-238`, and the authority map in `docs/README.md`. The issue's missing-work refusal and preservation of existing arms govern the linear example; H's matching postimages and T's raw current retention govern the replay example. REQ-VER-04 is the linked general requirement; it does not replace these specific acceptance criteria. The [published examples](https://github.com/kebag-logic/milan-fpga/pull/519#issuecomment-5780555701) and [retry assignment](https://github.com/kebag-logic/milan-fpga/pull/519#issuecomment-5780709303) define this assessment. Public bodies and API receipts are archived beside this report.

The measured results are:

| Fixture | Candidate, UTF-8 | Candidate, Latin-1 | Base, UTF-8 | Base, Latin-1 |
|---|---|---|---|---|
| Never-landed linear edit | STRANDED / 1 | **contained / 0, incorrect** | STRANDED / 1 | STRANDED / 1 |
| Redundant-merge replay, then non-ASCII edit reverted | UNKNOWN / 1 | **contained / 0, incorrect** | STRANDED / 1 | STRANDED / 1 |

The first fixture has one source commit and unrelated target work. It requires no policy about later reversions: the edit never landed. The second has the selected redundant merge, two historical replays, a reverted non-ASCII edit and a distant retained extension in `mod.txt`. At the candidate it must fail T and report UNKNOWN. The base has no G1/H/T fallback and reports STRANDED. Issue #514's separate linear historical-retention policy cannot justify either false pass.

The unmodified [public reproducer](https://github.com/kebag-logic/milan-fpga/blob/48b46b254f3eb1e60b75be6ed1a3821fe6594a00/review-evidence/423-r1/reviews/R251-1/receipts/locale_transport_probe.sh), downloaded from immutable public commit `e8de92935be878a2774c0689150f259df4d2d667`, reproduced all eight published results. [Raw reproduction output](https://github.com/kebag-logic/milan-fpga/blob/48b46b254f3eb1e60b75be6ed1a3821fe6594a00/review-evidence/423-r1/reviews/R251-1/receipts/reproduced/stdout.bin), [shell trace](https://github.com/kebag-logic/milan-fpga/blob/48b46b254f3eb1e60b75be6ed1a3821fe6594a00/review-evidence/423-r1/reviews/R251-1/receipts/reproduced/stderr-xtrace.bin) and [execution metadata](https://github.com/kebag-logic/milan-fpga/blob/48b46b254f3eb1e60b75be6ed1a3821fe6594a00/review-evidence/423-r1/reviews/R251-1/receipts/reproduced/execution.json) preserve the execution. Its exit 0 means the probe completed, not that the candidate passed.

[R251] BLOCKER Conformance — scripts/check_merge_containment.py:100; scripts/merge_containment_replay.py:126 — F1: Filename decoding changes the literal path passed to Git and certifies missing work.

[R251] BLOCKER Robustness — scripts/check_merge_containment.py:188; scripts/check_merge_containment.py:473; scripts/merge_containment_replay.py:61 — F1: The same filename produces false containment when filesystem encoding changes.

Requirement/evidence: Issue #423 AC3 and the settled decision require refusal of missing work, matching touched-path postimages, preservation of existing arms, and nonzero UNKNOWN when current retention is unproved. `CONTRIBUTING.md:219-238` records H and T. Under Python filesystem encoding `iso8859-1`, Git's filename bytes `c3 a9 2e 74 78 74` decode through UTF-8 to U+00E9 followed by `.txt`; subprocess then encodes that string as `e9 2e 74 78 74`. These are different literal filenames. `surrogateescape` does not prevent the conversion because `c3 a9` is valid UTF-8.

Measured result: the CLI results above match the published counterexamples. Additional direct measurements in [candidate Latin-1 observations](https://github.com/kebag-logic/milan-fpga/blob/48b46b254f3eb1e60b75be6ed1a3821fe6594a00/review-evidence/423-r1/reviews/R251-1/receipts/focused/sites-head-latin1.stdout) show `_same_patch_postimage('pr', 'pr^') == (True, None)` while a raw-byte literal diff of the actual filename exits 1. Under UTF-8 and at the base under Latin-1 the helper returns `(False, None)`. In the merge fixture, `_tree_entry` returns `None` for ancestor, target and source under Latin-1, and `_retained_at_tip` returns an empty unproved-path list. The file actually exists in all three trees. The raw [Git-call receipts](https://github.com/kebag-logic/milan-fpga/blob/48b46b254f3eb1e60b75be6ed1a3821fe6594a00/review-evidence/423-r1/reviews/R251-1/receipts/focused/sites-head-latin1.gitcalls.jsonl) record argv bytes, output bytes and exits.

Impact: `_path_scoped_verdict` compares the wrong absent pathname and interprets Git's successful empty comparison as equality. The shared H/postimage helper can similarly ignore unequal content. The new T proof reads absence at the wrong pathname and accepts `tip == branch == None`, omitting the reverted work. `--literal-pathspecs` prevents pathspec interpretation but cannot repair changed filename bytes. This is a false success from a required containment check, not just misleading display text.

Required outcome: every Git-derived filename must preserve its exact bytes through subsequent Git arguments and entry validation, independently of Python's filesystem encoding. Use a consistently reversible byte/path representation; a raw-byte path or a coordinated filesystem decode/encode pair can provide that property. Preserve raw patch bytes and the current fail-closed policy. Fixing only the new retention loop leaves the earlier false pass intact; fixing only the shared helper leaves the new retention conversion inconsistent. No source fix was attempted here.

Verification: both candidate negative fixtures must meet the required verdict/exit matrix below in fresh UTF-8 and Latin-1 Python processes. The postimage helper must reject the measured unequal files. Tree-entry lookup must return their actual entries, and T must name the unproved original pathname. Re-review the corrected exact head.

The complete conversion inventory within the two reviewed files is:

| Site at the reviewed head | Role and required consistency |
|---|---|
| `check_merge_containment.py:98-100` | Git output bytes are explicitly decoded with UTF-8/surrogateescape. String arguments on the next subprocess call instead use filesystem encoding. This introduced the regression versus the base's locale text decoding in these examples. |
| `check_merge_containment.py:169-189` | `_commit_paths` consumes that decoded NUL list; `_same_patch_postimage` resubmits the strings as literal filenames. This affects both existing linear replay and new H. |
| `check_merge_containment.py:451-474` | The existing touched-path arm consumes the same decoded NUL list and resubmits it to literal `diff --quiet`. This is the first published false pass. |
| `merge_containment_replay.py:126-129` | Independent UTF-8/surrogateescape decoding of net-changed path bytes feeds T's three tree lookups. This must use the same reversible filename representation. |
| `merge_containment_replay.py:30-33,61-64` | `_git_bytes` preserves output bytes but still passes string argv through subprocess filesystem encoding. Empty `ls-tree` output means absence only if the queried filename bytes were correct. |
| `merge_containment_replay.py:71` | Returned raw name bytes are checked against hard-coded UTF-8/surrogateescape encoding of the path. This comparison must match the actual argv bytes. Supplying `os.fsdecode(original_bytes)` to the unchanged function under Latin-1 reaches the real file but raises `_MeasurementError`, demonstrating why a decode-only correction is incomplete. |
| `check_merge_containment.py:154-159` | Patch text uses `_git` and explicitly encodes back with UTF-8/surrogateescape. This pair currently preserves its represented bytes; it is **not** the filename failure. Any change to the shared decoder must keep this inverse pairing correct or use a separate raw patch transport. Do not restore newline-normalizing text transport. |

Other consumers of the shared result deserve consistent treatment: `check_merge_containment.py:118-122` uses Git's reported graft-file pathname in `open`, and `:514-521` obtains filenames for diagnostics. They inherit the decoder choice; no additional graft-related failure is claimed or tested here. ASCII decoding of patch-ID fields (`check_merge_containment.py:161`) and tree metadata (`merge_containment_replay.py:68`) handles ASCII protocol fields, not filename bytes, and is unaffected. The temporary merge-file paths are created by Python, not decoded from Git's filename output.

[R251] MAJOR Tests — scripts/merge_containment_selftest_retention.py:115-132 — F2: Existing filename controls do not detect the locale transport regression.

[R251] MAJOR Conformance — scripts/merge_containment_selftest_retention.py:119 — F2: Required literal/non-UTF-8 boundary coverage omits the valid multibyte path that loses byte identity.

Requirement/evidence: the settled decision requires bounded controls for literal and non-UTF-8 paths, preservation of existing behavior, and assertions of both verdict and exit. `AGENTS.md` section 6 requires tests that can fail for the claimed defect and coverage of configuration-dependent behavior.

Measured result: the exact candidate's `_path_and_format_cases` passes **22/22 assertions under UTF-8 and 22/22 under Latin-1**, while both negative CLI fixtures fail their contract under Latin-1. [UTF-8 receipt](https://github.com/kebag-logic/milan-fpga/blob/48b46b254f3eb1e60b75be6ed1a3821fe6594a00/review-evidence/423-r1/reviews/R251-1/receipts/focused/existing-path-format-head-utf8.stdout) and [Latin-1 receipt](https://github.com/kebag-logic/milan-fpga/blob/48b46b254f3eb1e60b75be6ed1a3821fe6594a00/review-evidence/423-r1/reviews/R251-1/receipts/focused/existing-path-format-head-latin1.stdout) contain each assertion. The path list tests ASCII magic/control characters and an undecodable `ff` byte. It does not include the valid UTF-8 `c3 a9` name. Invalid UTF-8 bytes can survive via surrogateescape in both locales while valid UTF-8 characters are re-encoded differently. The fixture's `_tree` writer at `:35` also assumes UTF-8 for its supplied strings; cross-locale fixtures must explicitly establish their intended Git filename bytes.

Impact: these green controls do not protect either the changed shared transport or the new proof against this measured environment change.

Required outcome: add bounded, self-checking subprocess tests that establish the child's actual filesystem encoding and create known raw Git filename bytes. Cover both earlier touched-path/postimage consumers and T; test the returned-name check as well as path enumeration. The existing default self-test must own the regression controls. Report an unavailable locale explicitly instead of claiming that the differing-encoding case ran. Keep the established raw-byte/CRLF/literal-path controls.

Verification: the following are required candidate outcomes, asserted as both text and exit where applicable:

| Control | UTF-8 filesystem encoding | Latin-1 filesystem encoding |
|---|---|---|
| Published never-landed linear edit | STRANDED / 1 | STRANDED / 1 |
| Published replay with reverted non-ASCII edit | UNKNOWN / 1, identify unproved path | UNKNOWN / 1, identify original unproved path |
| Linear fixture with exact source content retained | contained / 0 | contained / 0 |
| Redundant-merge fixture with source content retained and distant extension | contained / 0 through raw-retention fallback | contained / 0 through raw-retention fallback |
| `_same_patch_postimage` on the measured unequal file | `(False, None)` | `(False, None)` |
| Entry lookup for existing `c3 a9 ...` pathname | Actual mode/kind/OID | Same mode/kind/OID; not absence or encoding-validation error |
| Git filename bytes through decoding, argv and validation | Original bytes exactly | Original bytes exactly |

Include an unchanged `e9 ...` filename alongside changed `c3 a9 ...` to distinguish aliasing from absence, raw invalid-UTF-8 names, and valid UTF-8 characters unencodable directly in Latin-1. The byte transport must preserve those names or produce an explicit non-success measurement refusal; it must never silently prove a different pathname. Preserve exact patch/CRLF/blob bytes and literal metacharacters. The current direct encoding observation for UTF-8 euro-sign bytes produces `UnicodeEncodeError` under Latin-1; this is a transport observation, not an additional full CLI finding.

Four retained positive CLI controls were also measured, one per shape and locale; all pass at the candidate. The merge positives explicitly report the raw-retention fallback. Their [commands and outcomes](https://github.com/kebag-logic/milan-fpga/blob/48b46b254f3eb1e60b75be6ed1a3821fe6594a00/review-evidence/423-r1/reviews/R251-1/receipts/positive-controls/execution.json) and individual raw stdout/stderr are preserved. These positives are controls, not evidence that the two negative cases are acceptable.

[R251] PASS RTL — receipts/diff-paths.txt; receipts/source-diff.txt — The exact base-to-head diff contains workflow prose and Python containment code/tests only. No RTL, hardware interface, timing/CDC or processor-pin change is in this assignment; those checks are inapplicable here.

[R251] PASS Docs — CONTRIBUTING.md:209-238; scripts/check_merge_containment.py:44-58; decision423.md; published-example.md — The authoritative wording distinguishes historical replay from the new current-retention requirement and explicitly requires UNKNOWN/nonzero when T is unproved. The public contract and executable example are sufficient to reconstruct this scoped defect. F1 violates the documented behavior; weakening that behavior is not a documentation fix. This does not validate all broader PR evidence claims.

All five lenses were applied within this assignment. The ledger is scoped to this filename review; it does not bank whole-PR coverage for unexamined behavior.

| Lens | Round | Exact examined head | Result |
|---|---|---|---|
| Conformance | R251-1 | df53dfa116b34816db0193230ad9833e67bf46dd | NOT CLEAN: F1 and F2 open |
| RTL | R251-1 | df53dfa116b34816db0193230ad9833e67bf46dd | CLEAN within scope; hardware changes inapplicable as evidenced above |
| Robustness | R251-1 | df53dfa116b34816db0193230ad9833e67bf46dd | NOT CLEAN: F1 open |
| Tests | R251-1 | df53dfa116b34816db0193230ad9833e67bf46dd | NOT CLEAN: F2 open |
| Docs | R251-1 | df53dfa116b34816db0193230ad9833e67bf46dd | CLEAN within scope; artifacts cited above |

Reproduction commands, from any directory on this review host:

```sh
rtk proxy python3 $WORKSPACE_HOME/milan-fpga-management/2026-09-22/423-locale-r251-retry/run_published.py
rtk proxy python3 $WORKSPACE_HOME/milan-fpga-management/2026-09-22/423-locale-r251-retry/run_focused.py
rtk proxy python3 $WORKSPACE_HOME/milan-fpga-management/2026-09-22/423-locale-r251-retry/run_positive_controls.py
rtk proxy python3 $WORKSPACE_HOME/milan-fpga-management/2026-09-22/423-locale-r251-retry/verify_integrity.py
```

Measured exits are respectively **0, 1, 0, 0**. The second command intentionally asserts the contract and fails: [eight assertions, two failures](https://github.com/kebag-logic/milan-fpga/blob/48b46b254f3eb1e60b75be6ed1a3821fe6594a00/review-evidence/423-r1/reviews/R251-1/receipts/focused/regression-assertions.json). Its per-command JSON records argv, cwd, locale settings and exit; paired `.stdout`/`.stderr` files preserve raw output. `filename_checks.py` additionally records subprocess argv byte encodings and raw Git outputs. Run the sequence from its first command to obtain new temporary repositories; the positive-control command adds a branch in those repositories and is intended once per fresh sequence.

All work ran serially (one job, below the eight-job limit). Python was 3.14.7, Git 2.55.0 and glibc localedef 2.44. A newly allocated temporary directory held the extracted head/base scripts, two fixture repositories and scratch `en_US.ISO-8859-1` locale. Python UTF-8 mode and locale coercion were explicitly disabled; each child recorded `utf-8` or `iso8859-1` as appropriate. Installed locales were not changed. Git history mutations were confined to new temporary fixture repositories; source-checkout Git operations were read-only. No full parent, synthesis, processor or builder test bank was run or claimed.

Final integrity is recorded in [final-integrity.json](https://github.com/kebag-logic/milan-fpga/blob/48b46b254f3eb1e60b75be6ed1a3821fe6594a00/review-evidence/423-r1/reviews/R251-1/receipts/final-integrity.json). Root HEAD is exactly `df53dfa116b34816db0193230ad9833e67bf46dd`, with clean status; all 855 tracked root files match their committed blob bytes and modes. Required submodules are registered at the exact root gitlinks, have clean status, and are real directories. Their tracked bytes/modes were independently hashed, without relying on index flags:

| Required submodule | Exact revision | Verified tracked files |
|---|---|---:|
| third_party/verilog-axis | 48ff7a7e2ef782cf778d47910cf85835c64b1bce | 214 |
| protocol-processor | 424c688fa2205b934a7689a58f2aa766420f2326 | 222 |
| gptp-processor | c1b617435824929a790739ea8585c3fe1a328cc0 | 103 |

The optional `external` submodule remains uninitialized, as at session start; `CONTRIBUTING.md:338-353` excludes it from the required three. Installed locale listings are unchanged. The report and receipts contain factual conclusions and executable evidence only.

R251-1 FINISHED
