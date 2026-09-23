[A186] REVIEW READY
Commit: `bb4be4d389f738b3b2fc3fa4123f2a1e8789bd34`
Tree: `ab96af335f1428770a1a96c0345a9f55278ad25b`
Base: descends from live dev `483a133ed08867ea0d300d2b4a027b5b48a4282f` through merge `e1e0f97974180190c8e0c2a28877eb2b8f326c7d` (tree `12dcd757ec2ecba56b57138ad999c51cf0e60eb2`, equal to the pre-computed merge tree; dev-side paths are disjoint from the PR diff). Not pushed. Branch clean, index equals HEAD, all 857 tracked blobs hash-verified; gitlinks unchanged (gPTP processor `c1b61743`, PP `424c688f`, verilog-axis `48ff7a7e`).

Changed, three commits after the merge:
- `1a43ba80` (R244-B): the mutation harness copies sources as bytes.
- `e4354566` (R244-A, R244-D): new shared transport `scripts/merge_containment_git.py`. Filenames and patch text stay bytes from Git output to Git input in the touched-path arm, the H/linear patch and postimage helpers, the differing-path note and T. Other decoded Git output that does not re-encode to identical bytes returns a failed status, so it can only become UNKNOWN or a refusal. Path diagnostics are ASCII byte literals. Locale controls and CONTRIBUTING step 7 wording updated.
- `bb4be4d3` (R244-C): real-history controls for the named guards.

| Finding | Resolution (author claim; reviewer-owned) | Evidence at the commit |
|---|---|---|
| R244-A MAJOR | Byte transport for every Git-derived filename and patch; round-trip refusal for other decoded output. Permanent controls: an in-process Big5 filesystem codec on every host, plus fresh Big5 and strict UTF-8 processes beside UTF-8-mode, ASCII and Latin-1 (`NOT RUN` when locale data is missing). Docs and transport docstrings claim only this; PR text proposed in the packet. | Big5 redundant-merge probe: `UNKNOWN`/1 naming `'\xa1\xfe.txt'` (was `contained`/0). Big5 linear probe: `STRANDED`/1 (was `contained`/0). Same verdicts in all five locales. Restoring the lossy byte transport, the old T lookup, the old patch transport or dropping the output guard each fails the default self-test, also on a host without `localedef`. |
| R244-B MINOR | Byte-exact source copies; mutant output decoded with a replacement handler. | ASCII parent 678/678 (reviewed code crashed after 147). Restoring text copies crashes again under ASCII. |
| R244-C MINOR | Controls asserting verdict and exit: rename undone and gitlink reset under repository `diff.renames=copies`, `diff.ignoreSubmodules=all` and `diff.external`; a symlink ancestor whose bytes merge cleanly; one versus two real merge bases by injection (a single redundant merge cannot produce two); add/remove/add with one replay, linear and merge-shaped. | Dropping the single-base rule, `--no-renames`, `--ignore-submodules=none`, the ancestor type rule or replay distinctness each fails the default self-test. The reviewer's guard histories give the same table at this head. |
| R244-D MINOR | Names printed through `path_label`; each child drives the CLI with three targets through a real stdout. | Report complete (`contained`, `STRANDED`, `contained`, summary) under strict UTF-8, UTF-8 mode, ASCII, Latin-1 and Big5 (reviewed code aborted after the first target under strict UTF-8 and Big5). Restoring decoded labels fails the self-test. |
| F1/F2/F3 | Not regressed. | Published F1 examples: linear `STRANDED`/1, merge `UNKNOWN`/1 in UTF-8 and Latin-1. Default self-test passes under a Latin-1 parent with the byte-defined names and exact path assertions retained. |

Material decisions, as announced at takeover: the STRANDED `paths differing:` note now quotes names the same way as the UNKNOWN note (ASCII names in UNKNOWN notes, including actual PR62, are unchanged). Two original path-arm fault injections (4 of the 145 original assertions) now target `_git_raw`, where those measurements run; names, inputs and assertions are unchanged.

Validation, author-local at the commit, at most 8 parallel jobs:
- `python3 scripts/check_merge_containment.py --selftest`: 678/678 (455 prior + 210 locale + 13 retention) under default, UTF-8-mode, strict UTF-8, ASCII, Latin-1 and Big5 parents; nothing `NOT RUN`.
- `docs_check`, `check_em_dash --base 483a133e` (54 added lines, 0 findings) and `--selftest`, `check_doc_style`, `check_doc_paths`, `gen_toc --check`/`--verify-anchors`, `check_feature_status`, `check_py_idiom` (long module 10 <= 10) and `--selftest`, `check_hygiene --check`/`--selftest`, naming, fail-fast and test-evidence ratchets, TODO ownership, `git diff --check`: all exit 0.
- 28 mutation, restoration and parent-locale probes: 7 controls pass, 18 mutants fail as required, 3 survivors listed below.
- Actual gPTP processor PR62 stays `UNKNOWN`/1 at `f0f1c055` and `c1b61743` with the same note; PR61 stays `contained`/0; all four decision patch hashes reproduce.

Acceptance criteria: AC1-3 behavior is unchanged (G1/H/T, the 31-case matrix, ten guard mutations and all prior arms pass). AC4 still needs the complete local bar, trusted replica, hosted checks, current-candidate validation and cleared R251/R244 re-review of all five lenses at this head.

Open risks/questions:
- Survivors R244-1 did not raise: the returned-name check in `_tree_entry` (redundant with exact-byte argv), `--full-tree` (matters only from a subdirectory, where the older arms are already cwd-relative), the merge-file conflict-style override (a conflicted merge already fails). T's `--no-ext-diff`/`--no-textconv` have no effect on a `--name-only` listing.
- Git-derived ref and remote names stay text: refused, not measured, when they do not round-trip. Only the no-operand current-branch case is controlled. Only Big5 is exercised as a non-injective codec.
- R244-1 O-1 (subdirectory invocation) is unchanged and needs its own Issue.
- R244-1's own `probe_guards.py` must also copy the new transport module, and its `mutate.py` restoration edits target removed code; adapted equivalents are in the packet.
- Default self-test wall time is about 30 s here (21 s measured at the reviewed head).

Author packet for manager publication: HANDOFF.md, proposed PR-BODY.md (the PR was not edited), `reproduce.sh` with its scripts, and raw receipts. No push, PR edit, merge, act, hosted run, full native/processor/Yosys/builder bank, hardware or other-lane change. No self-approval.
