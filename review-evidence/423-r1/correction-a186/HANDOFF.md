# A186 handoff: issue #423 / PR #519, correction round for R244-1

Author: A186 (sole implementation author for this round). This is author evidence,
not a review verdict. R251 (internal) and R244 (external) own the findings, their
lens assignments and every resolution decision.

## Identity

| Item | Value |
|---|---|
| Lane | `$LANES/423-retained-redundant-replay`, branch `423-retained-redundant-replay` |
| Reviewed head (R244-1) | `4671e582cfa4bba4809b9e3a354ce5b6eb967f99`, tree `afc8eadb3e9f6611dfb62347580b49dc721d25c0` |
| Live dev merged in | `483a133ed08867ea0d300d2b4a027b5b48a4282f` |
| Merge commit | `e1e0f97974180190c8e0c2a28877eb2b8f326c7d`, tree `12dcd757ec2ecba56b57138ad999c51cf0e60eb2` (equal to the `git merge-tree --write-tree` prediction; no conflict) |
| **Corrected head** | **`bb4be4d389f738b3b2fc3fa4123f2a1e8789bd34`**, tree **`ab96af335f1428770a1a96c0345a9f55278ad25b`** |
| Base for the head | `git merge-base HEAD origin/dev` = `483a133e...` (live dev is an ancestor) |
| Worktree / index | clean; index equals HEAD; no flagged index entries; no stash; 857 tracked blobs hash-verified |
| Gitlinks | identical at HEAD, `4671e582` and `483a133e`: `gptp-processor` `c1b61743...`, `protocol-processor` `424c688f...`, `third_party/verilog-axis` `48ff7a7e...`, `external` `efeb541a...` (uninitialized, as at start) |
| Pushed? | No. No push, PR edit, merge, Docker/act or hosted run was performed. |

Commits after the reviewed head, oldest first (one-line subjects, no trailers):

| Commit | Subject | Scope |
|---|---|---|
| `e1e0f979` | Merge live dev 483a133e into the issue 423 lane | dev-side only: `docs/ENDSTATION_BUILDER.md`, `sw/builder/endstation_builder.py`, `sw/builder/test_builder.py`; no overlap with the PR diff (receipts/01-merge-dev.txt, 00-pre-merge.txt) |
| `1a43ba80` | Copy mutation sources as bytes so an ASCII parent runs the self-test | R244-B |
| `e4354566` | Carry Git filename and patch bytes to Git without the filesystem codec | R244-A, R244-D |
| `bb4be4d3` | Kill the retention guard and replay distinctness mutants with real-history controls | R244-C |

An intermediate `9dde528c` existed only locally; `bb4be4d3` amends its test
docstring (2 lines). Its receipts are kept under `receipts/superseded-9dde528c/`
and are not final evidence.

## Per-finding resolution (author claims; reviewer-owned)

| Finding | Root cause | Change | Evidence at `bb4be4d3` |
|---|---|---|---|
| **R244-A** MAJOR | Git filenames and patch text went Git bytes -> `os.fsdecode` -> str argv / `os.fsencode`; Big5 maps `a1 fe` to a character that re-encodes as `a2 41`, so a lookup addressed another name and absence equalled absence. | New `scripts/merge_containment_git.py`: `git_bytes` (argv may be bytes; stdout raw) and `git_text` (filesystem-codec text; output that does not re-encode to identical bytes returns `RC_LOSSY_OUTPUT` = 256 and no text). Every Git-derived filename now stays bytes from Git output to Git argv: touched-path arm (`_path_scoped_verdict`), `_commit_paths`/`_same_patch_postimage` (H and the linear arm), `_differing_paths`, and T (`_retained_at_tip`, `_tree_entry`, whose returned name is compared with the enumerated bytes). Patch bytes go raw from `git show` to `patch-id` stdin. Other decoded Git output (refs, remotes, graft path, OIDs) is refused when it does not round-trip, so it becomes UNKNOWN or a refusal, never a pass. The checker and replay module import the shared transport (the replay module's duplicate `_git_bytes` is now that import). | Big5 redundant-merge probe: `UNKNOWN`/1 naming `'\xa1\xfe.txt'` in Big5, UTF-8 mode, strict UTF-8, Latin-1 and ASCII (was `contained`/0 in Big5). Big5 linear probe: `STRANDED`/1 in all five (was `contained`/0 in Big5). `receipts/probes-head-bb4be4d3.txt` vs `receipts/baseline-e1e0f979/02-baseline-probes.txt`. |
| R244-A controls | No control ran under a non-injective codec. | Default self-test (`merge_containment_selftest_locale.py`): (1) an in-process control on every host replaces the filesystem codec of the transport, checker and replay modules with a Big5 pair and runs all name controls plus `git_text` refusal checks; (2) fresh Big5 and strict UTF-8 child processes beside the existing UTF-8-mode, ASCII and Latin-1 ones (installed locale or disposable `localedef`; otherwise `NOT RUN`). Names add `a1 fe`; trees carry unchanged aliases `e9.txt` and `a2 41.txt`; blob content includes `a1 fe` so patch transport is exercised. | Removing the fix fails the default self-test: `lossy-git-bytes`, `restore-4671-replay-transport`, `restore-4671-patch-transport`, `drop-lossy-output-guard` all FAIL, and all still FAIL with no `localedef` on `PATH` (Latin-1/Big5 children `NOT RUN`, in-process control kills them). `receipts/mutations-head-bb4be4d3.txt`. |
| R244-A docs | CONTRIBUTING, `_git` docstring and PR text over-claimed. | CONTRIBUTING step 7 (5 lines replaced by 10): filenames and patches reach Git again as their original bytes; other output that does not re-encode exactly counts as a failed command; ASCII byte-literal diagnostics; in-process Big5 plus five fresh processes; `NOT RUN` semantics. Transport docstrings restore the "(rc, stdout) ... Never raises on a non-zero rc" contract. PR text: `PR-BODY.md`. | docs, em-dash (54 added lines, 0 findings), TOC, doc-style, doc-paths gates pass (`receipts/gates-head-bb4be4d3/`). |
| **R244-B** MINOR | `mutation_cases` copied sources with `read_text`/`write_text` (locale codec); the checker has non-ASCII bytes. | Bytes I/O; edit strings encoded as ASCII; mutant stdout decoded with `errors="backslashreplace"`. | ASCII parent 678/678 (was crash at 147 on the reviewed head). Restoring text I/O under an ASCII parent crashes again at 147 (`restore-text-source-copies`). Also: commit `1a43ba80` alone gives 455/455 under ASCII (`receipts/development/`). |
| **R244-C** MINOR | Named guards had no killing control. | Retention controls with verdict + exit (+ named path): `hostile-rename-undone` and `hostile-gitlink-reset` under repository `diff.renames=copies`, `diff.ignoreSubmodules=all` and `diff.external`; `symlink-ancestor-clean-merge` (symlink ancestor whose target bytes merge cleanly, so only the ancestor type rule refuses); `merge-base-one-real-base` (contained) and `merge-base-two-real-bases` (UNKNOWN), an injection of real object IDs so every later measurement succeeds; `distinct-linear` and `distinct-merge` (add, remove, add again with one replay: STRANDED/1). | `single-base-dropped`, `retention-renames-folded`, `retention-submodules-default`, `ancestor-regular-guard`, `distinct-replay-dropped` all FAIL the default self-test. Reviewer histories (`probe_guards`) give the same head/mutant table as R244-1. |
| **R244-D** MINOR | STRANDED notes joined decoded names and printed them to a strict UTF-8 stdout. | `path_label` quotes exact name bytes as an ASCII bytes literal in every locale; used by STRANDED `paths differing:` and T's UNKNOWN notes. Control: each child runs the CLI with three targets through a real stdout and asserts stream codec/error handler, verdict order, empty stderr, ASCII output and every name label. | Multi-target probe prints `contained`, `STRANDED`, `contained` and the summary in all five locales (baseline crashed after the first target under strict UTF-8 and Big5). `restore-raw-differing-names` and `restore-decoded-unknown-labels` FAIL the self-test. |

Material decision (published in the TAKEN comment): the pre-existing STRANDED
note now quotes every name (`paths differing: 'ctl', 'mod.txt'`), matching T's
UNKNOWN notes; ASCII names in UNKNOWN notes are unchanged (actual PR62 text is
byte-identical). No in-repository consumer parses this text (`git grep`).

Two original content-module arms (`path-enumeration-error-*`,
`path-comparison-error-*`) inject failures into the path arm; their injection
target moved from `mc._git` to `mc._git_raw` because those measurements now run
there. Names, inputs and assertions are unchanged.
`receipts/development/selftest-before-injection-retarget.out` shows the old
target no longer reached the measurement (4 FAIL lines, verdict contained/0).
These are 4 of the 145 original assertions; the code of the other 141 is untouched.

## Prior findings (no regression claimed; reviewer-owned)

| Finding | Status at `bb4be4d3` |
|---|---|
| F1 (R251-1) | Published reproducer re-run with its head archive taken at `bb4be4d3`: linear `STRANDED`/1 and merge `UNKNOWN`/1 naming `'\xc3\xa9.txt'` in UTF-8 and Latin-1 (`receipts/f1-published-examples-head-bb4be4d3/`; the printed label "head-df53dfa1" is the probe's fixed text). Non-injective codecs are now covered too (R244-A). |
| F2 (R251-1) | Default self-test owns UTF-8-mode, ASCII, Latin-1, strict UTF-8 and Big5 child processes plus the in-process Big5 control, with byte-defined names, aliases, positives, negatives, entry/postimage/patch checks and `NOT RUN` reporting. |
| F3 (R251-2) | Latin-1 parent 678/678. The raw-name fixture and exact path assertion are retained; the expected label is now derived from the exact bytes (locale-independent) rather than from the parent's codec. |

## Validation at `bb4be4d3` (all local, author-run)

Reproduce everything with `sh scripts/reproduce.sh bb4be4d389f738b3b2fc3fa4123f2a1e8789bd34`
(3 min, at most 8 parallel jobs). Summary files and raw outputs:

| Receipt | Result |
|---|---|
| `receipts/gates-head-bb4be4d3.txt`, `gates-head-bb4be4d3/` | 24 commands, all exit 0. `check_merge_containment.py --selftest` 678/678 under default, UTF-8 mode, strict UTF-8, ASCII, Latin-1 and Big5 parents (no `NOT RUN`); `docs_check`, `check_em_dash --base 483a133e` and `--selftest`, `check_doc_style`, `check_doc_paths`, `gen_toc --check`/`--verify-anchors`, `check_feature_status`, `check_py_idiom` (long module 10 <= 10) and `--selftest`, `check_hygiene --check` and `--selftest`, `measure_naming`, `measure_fail_fast`, `measure_test_evidence`, `check_todo_ownership`, `git diff --check` against live dev and against `4671e582`. |
| `receipts/mutations-head-bb4be4d3.txt`, `mutations-head-bb4be4d3/` | 28 probes on the archived head: 7 controls PASS (6 parent locales, plus default with no `localedef`: 564/564 with Latin-1/Big5 `NOT RUN`); 18 mutants/restorations (12, and 6 of them again with no `localedef`) FAIL the self-test as required; 3 survivors listed under Limits. |
| `receipts/probes-head-bb4be4d3.txt`, `probes-head-bb4be4d3/results.json` | R244-1 Big5 merge/linear and multi-target probes, five locales. |
| `receipts/probe-guards-head-bb4be4d3.txt` | Reviewer's guard histories; adapted copy also copies `merge_containment_git.py` into each mutant directory (one added line, `scripts/probe_guards_adapted.py`). |
| `receipts/actual-pr61-pr62-head-bb4be4d3.txt` | Actual gPTP processor PR62 `UNKNOWN`/1 at `f0f1c055` and `c1b61743` naming `'tb/tsngen/mutants.py'`, `'tb/verilator/gaskets/mutants.py'` (same text as the reviewed head); PR61 `contained`/0 at both. The four decision patch hashes reproduce (`d3d164b3...` twice, `fa20a251...` twice). |
| `receipts/integrity-head-bb4be4d3.json` | ALL_OK: head/tree, 857 root blobs, index equals HEAD, empty status, three required submodules at their gitlinks with 214/222/103 files hash-verified. |

Default self-test population: 678 = 455 at the reviewed head + 210 locale rows
(5 children x 57 + 54 in-process, replacing 3 x 43) + 13 retention rows.
Standalone wall time about 29-31 s here (R244-1 measured 21 s at the reviewed head).

## Limits and open items (not claimed resolved)

- Surviving mutants that R244-1 measured but did not raise: `entry-name-check`
  (with exact-byte argv and a literal pathspec `ls-tree` returns that name or
  nothing, so the check is defense in depth), `entry-full-tree` (matters only
  from a subdirectory, where the pre-existing arms are already cwd-relative:
  R244-1 O-1), `conflict-style-override-dropped` (a conflicted merge already
  fails the no-op test). T's `--no-ext-diff`/`--no-textconv` have no observable
  effect on a `--name-only` enumeration; the hostile control asserts no driver,
  textconv, filter or external diff ran.
- Git-derived ref and remote names remain text. Under a non-injective codec a
  name that does not round-trip is refused (UNKNOWN, or rc 2 for the
  no-operand branch), not measured as bytes. Only the no-operand HEAD case is
  controlled. The graft-file path follows the same rule.
- Labels from command-line refs and from GitHub JSON in `--merged-prs` are
  printed as given; not changed and not measured here.
- Only Big5 is exercised as a non-injective codec; the transport does not use a
  codec for filenames, and the `git_text` refusal is a generic round-trip test.
- R244-1 O-1 (subdirectory invocation of the pre-existing arms) is unchanged and
  out of scope; R244 recommended a new Issue.
- Reviewer probe harness notes: R244-1 `probes/mutate.py` restoration edits
  target code that no longer exists; `scripts/mutate_head.py` holds the
  equivalents for this head. `probes/probe_guards.py` needs the new module
  copied (see above).
- Not run (manager-owned): full parent Verilator, PP, gPTP, Yosys and builder
  banks, trusted act replica, hosted checks, current-dev candidate validation,
  hardware. No processor pin, ratchet, product, RTL or firmware change.

## Packet contents

- `HANDOFF.md` (this file), `PR-BODY.md` (proposed body; the PR was not edited),
  `REVIEW-READY.md` (the posted comment), `taken.md` (the posted TAKEN comment).
- `scripts/`: `reproduce.sh`, `run_gates.py`, `mutate_head.py`, `run_probes.py`,
  `actual_history.sh`, `probe_guards_adapted.py`,
  `locale_transport_probe_adapted.sh` (one line: `HEAD_SHA` overridable), and
  `r244-probes/` (unchanged public copies with `SHA256SUMS`, taken from
  `review-evidence/423-r1/reviews/R244-1/probes` and
  `review-evidence/423-r1/review/R244-interrupted` at `2dab142f`).
- `receipts/`: final evidence named `*-head-bb4be4d3*`; `00-pre-merge.txt`,
  `01-merge-dev.txt`; `baseline-e1e0f979/` (R244-A/B/D reproduced before the
  fix); `development/` and `superseded-9dde528c/` (not final evidence).
- `MANIFEST.sha256` covers every file above. `scratch/` (disposable locales,
  fixtures, source archives) was deleted before stopping.
