[R244] NEGATIVE - exact head 4671e582cfa4bba4809b9e3a354ce5b6eb967f99

Round R244-1, external cleared-context review of issue #423 / PR #519.
Exact head `4671e582cfa4bba4809b9e3a354ce5b6eb967f99`, tree
`afc8eadb3e9f6611dfb62347580b49dc721d25c0`, source base
`52711029f374650dc93830d5ea28e81cb5c8f410`. All five lenses were applied
independently at this head. One MAJOR and three MINOR findings are open, so all
five lenses are UNCLEAN.

Reconstruction order: AGENTS.md, CONTRIBUTING.md (2.1 step 7), docs/README.md,
REQUIREMENTS.md REQ-VER-04, the issue body and the
[settled G1 + H + T decision](https://github.com/kebag-logic/milan-fpga/issues/423#issuecomment-5777210218),
the manager's issue/PR evidence comments, the full base-to-head diff and its four
commits, then executable evidence. The independent-pass findings were written to
`receipts/independent-pass-draft.md` before any prior finding was read. After
that, only the finding sections of the two prior NEGATIVE rounds were read, to
settle F1/F2/F3 (see "Prior findings" below). The prior POSITIVE reports and
reviewer evidence folders were not read.

## Findings

### R244-A - MAJOR - Conformance, RTL, Robustness, Tests, Docs

`scripts/merge_containment_replay.py:60-65,72,127`;
`scripts/check_merge_containment.py:93-101`; `CONTRIBUTING.md:242`; PR #519
body, first paragraph. Title: under a filesystem codec that does not round-trip,
a Git filename reaches Git's argv as different bytes, and the new arm
reports `contained`/0 for work the tip reverted.

- **Authority/evidence:**
  - Decision 5777210218 requires: "unsupported measurements cannot become a
    pass", "literal and non-UTF-8 paths", and "Any failed or unmeasurable
    retention check remains nonzero UNKNOWN".
  - Prior F1 set this required outcome: "every Git-derived filename must
    preserve its exact bytes ... independently of Python's filesystem
    encoding ... it must never silently prove a different pathname".
  - `CONTRIBUTING.md:242` states "Git filenames retain their original bytes
    across filesystem encodings".
  - The `_git` docstring says it decodes "reversibly".
  - The PR body says filename bytes "are preserved across filesystem encodings
    in both existing checks and the new fallback".
- **What the code does:** `os.fsdecode`/`os.fsencode` are inverse only when the
  process codec is injective. Python's `big5` and `big5hkscs` codecs map
  distinct byte pairs to one character. For example, `a1 fe` decodes and
  re-encodes as `a2 41`. `receipts/probe-codec-roundtrip.txt` records 4 such
  pairs for `big5` and 12 for `big5hkscs`. glibc lists `zh_TW BIG5` and
  `zh_HK BIG5-HKSCS` as supported locales.
  - `_retained_at_tip` decodes the enumerated name (`:127`).
  - `_tree_entry` passes the resulting string as argv (`:62-63`).
  - Empty `ls-tree` output is then taken as absence (`:64-65`).
  - The returned-name check at `:72` runs only when an entry exists, so it
    never sees the mis-addressed lookup.
- **Measured** (`probes/probe_big5.py`, `receipts/probe-big5.txt`): the history
  is one exact redundant merge. The source edits `a1 fe 2e 74 78 74` and `ctl`.
  Both commits are replayed exactly, then the tip reverts the named file and
  extends `ctl` far from the hunk.

  | Checker | Process encoding | Result |
  |---|---|---|
  | Head | UTF-8 | `UNKNOWN`/1, naming `'\udca1\udcfe.txt'` |
  | Head | `big5` (disposable `localedef` of zh_TW.BIG5) | `contained`/0, "raw no-op retention" |
  | Base 52711029 | `big5` | `STRANDED`/1 |

  In the Big5 run, all three `ls-tree` lookups address `a2 41 2e 74 78 74`,
  which exists in none of the trees, so absence equals absence.
- **Existing arms:** the same transport also leaves the unchanged touched-path
  arm reporting `contained`/0 for stranded linear work on such a name at both
  base and head (`probes/probe_big5_linear.sh`,
  `receipts/probe-big5-linear.txt`). That exposure predates this PR, but it
  contradicts the PR body's "both existing checks" claim.
- **Impact:** a false containment success, the one outcome the checker exists
  to prevent. It is a regression from STRANDED at the base, reached only
  through the new fallback. The precondition is narrow: a non-injective
  process codec plus an affected character in a changed filename.
- **Required outcome:**
  - Every Git-derived filename reaches Git as its original bytes, or the
    measurement fails closed as UNKNOWN. Either works:
    - carry names as bytes end to end (POSIX `subprocess` accepts bytes argv);
    - refuse any name whose decode/encode round trip is not the identity.
  - Absence may be concluded only for a lookup of the enumerated bytes.
  - The CONTRIBUTING sentence, the `_git` docstring and the PR body claim only
    what is proved. The docstring also lost its "(rc, stdout), never raises"
    return contract.
- **Verification:**
  - Rerun `probes/probe_big5.py` under zh_TW.BIG5: head must give `UNKNOWN`/1
    naming the original path, or an explicit measurement refusal. It must never
    give `contained`/0.
  - A default-self-test control must exercise a non-injective codec (for
    example a disposable Big5 locale reported NOT RUN when unavailable, or a
    direct transport check under such a codec), and must fail when the
    transport is lossy.

### R244-B - MINOR - Tests, Robustness, Conformance

`scripts/merge_containment_selftest_mutations.py:46-47,58-59`. Title: the
default self-test crashes under an ASCII-encoded parent process, where the base
self-test passes.

- **Authority/evidence:**
  - The decision requires "Preserve all existing 145 self-test arms".
  - `--selftest` and the full suite must execute the new controls.
  - The PR itself treats ASCII as a supported filesystem encoding: its locale
    child runs `LC_ALL=C PYTHONUTF8=0 PYTHONCOERCECLOCALE=0`.
- **Measured:**
  - Head, same environment: 147 assertions print ok, then
    `UnicodeDecodeError: 'ascii' codec can't decode byte 0xc2` in
    `mutation_cases`. Exit 1 (`receipts/mutations/control-ascii-parent.out`).
    `read_text()` decodes `check_merge_containment.py` with the locale
    encoding, and that file has 6 non-ASCII bytes. `write_text` has the same
    dependency.
  - Base 52711029, same environment: 145/145, exit 0
    (`receipts/selftest-base-ascii-parent.out`).
  - Head passes 455/455 under the ordinary UTF-8 parent and under a Latin-1
    parent (`receipts/mutations.json`: `control-default`,
    `control-latin1-parent`).
- **Impact:** the required gate fails in a supported encoding environment,
  aborting `run_all_suites.sh`. This is fail-closed, not a false containment
  result. It is the same class as prior F3 in a different file with a
  different cause.
- **Required outcome:**
  - Source copies in the self-test preserve exact bytes (bytes I/O or explicit
    UTF-8), and the complete default self-test passes under an ASCII parent as
    the base does.
  - Keep the Latin-1 and UTF-8 parent results.
- **Verification:**
  `LC_ALL=C PYTHONUTF8=0 PYTHONCOERCECLOCALE=0 python3 scripts/check_merge_containment.py --selftest`
  must pass, and the UTF-8 and Latin-1 parent runs must stay green.

### R244-C - MINOR - Tests

These guards have no killing control:

- `scripts/merge_containment_replay.py:116-118` (single merge base);
- `scripts/merge_containment_replay.py:120-122` (retention diff flags);
- `scripts/merge_containment_replay.py:104-106` (ancestor type rule);
- `scripts/merge_containment_selftest_retention.py:157-182` (hostile
  configuration) and `:217-231` (graph faults);
- `CONTRIBUTING.md:221-225`.

Title: documented T guards survive mutation of the full default self-test, and
two of the surviving mutants produce false containment on real histories.

- **Authority/evidence:** AGENTS section 6 Tests: "Each new test can fail for
  the defect it claims to detect". The decision requires boundary controls for
  "symlink/gitlink/type changes ... and hostile configuration". CONTRIBUTING
  documents T as requiring "exactly one merge base", "unfolding renames", and
  that "The ancestor must be absent or a regular blob".
- **Measured:** each probe copies `scripts/`, applies one literal edit, and runs
  the unmodified default owner (`probes/mutate.py`, `receipts/mutations.json`,
  `receipts/mutations/*.out`). Five mutants still pass 455/455:

  | Mutant | Behaviour on a real history (`probes/probe_guards.py`, `receipts/probe-guards.txt`) |
  |---|---|
  | `--no-renames` dropped from the retention diff | Rename `a.txt`→`b.txt`, tip later restores `a.txt`: head gives `UNKNOWN`/1 naming `'a.txt'`; the mutant gives `contained`/0. |
  | `--ignore-submodules=none` dropped | With `diff.ignoreSubmodules=all` configured and the tip resetting gitlink `sub`: head gives `UNKNOWN`/1 naming `'sub'`; the mutant gives `contained`/0. The hostile-configuration control does not set this key. |
  | `len(bases) != 1` weakened to `not bases` | The `merge-base --all` injection returns fabricated object IDs whose later `diff` fails anyway, so the control cannot see the rule. |
  | Ancestor removed from the regular-type rule | No behavioural difference on the probed symlink history (the raw merge conflicts). |
  | Distinctness (`candidates.remove(match)`) dropped from the pre-existing H helper | T backstops it inside the new arm. |
- **Impact:** a later edit can silently reintroduce a false containment
  success that no test catches. The code at this head is correct for these
  cases.
- **Required outcome:** self-checking controls that assert verdict and exit
  and fail when each documented T guard is removed:
  - rename unfolding;
  - hostile `diff.ignoreSubmodules` (and `diff.renames`);
  - the single-merge-base rule, isolated through a real criss-cross history
    or an injection whose later measurements succeed;
  - the ancestor type rule where it is observable.
- **Verification:** rerun `probes/mutate.py` with `retention-renames-folded`,
  `retention-submodules-default` and `single-base-dropped`. Each must fail the
  default self-test, while `control-default` stays green.

### R244-D - MINOR - Robustness, Tests

`scripts/check_merge_containment.py:513-521,585-586,902-903`;
`scripts/merge_containment_selftest.py:79-85`;
`scripts/merge_containment_selftest_locale.py:105,157`. Title: in an ordinary
UTF-8 locale, a STRANDED verdict that names a non-UTF-8 filename raises
`UnicodeEncodeError` before printing and aborts the remaining report.

- **Authority/evidence:**
  - The decision requires "literal and non-UTF-8 paths" controls with verdict
    text and exit asserted.
  - AGENTS section 6 Tests: "Real integration wiring is tested where
    practical".
  - The PR body claims preserved filename handling "in both existing checks
    and the new fallback".
- **What the code does:**
  - `_git` now yields surrogate-escaped strings.
  - `_differing_paths` joins them raw into the note.
  - `_report` prints the note to a strict UTF-8 stdout, which is Python's
    default outside UTF-8 mode.
- **Measured** (`LC_ALL=en_US.UTF-8 PYTHONUTF8=0`):
  - `--base main aa-ok pr zz-later` prints `contained aa-ok`, then a traceback
    at the STRANDED print. `zz-later` is never assessed and no summary prints.
    Exit 1 (`receipts/probe-multitarget-print.out`,
    `receipts/probe-utf8-locale-print.out`).
  - The base crashed earlier for the same input, while decoding, so the exit
    status is not a regression.
- **Why the tests miss it:** the default self-test captures `main()` output in
  `StringIO` (`merge_containment_selftest.py:83-85`, `locale.py:105`), and its
  UTF-8 child runs in UTF-8 mode (`locale.py:157`). No control reaches a real
  strict UTF-8 stdout. The new arm's UNKNOWN notes use `repr` and are
  unaffected.
- **Impact:**
  - The STRANDED verdict and path names are lost.
  - In `--merged-prs` or multi-branch mode, every later tip goes unreported.
  - Fail-closed exit, not a false pass.
- **Required outcome:**
  - Verdict and diagnostic printing never fails for any Git filename bytes in
    the default locale.
  - A control runs the CLI against a real process stdout under an ordinary
    UTF-8 locale with a non-UTF-8 differing path.
- **Verification:** rerun the multi-target probe. All three targets must be
  reported, with exit 1 because of the stranded tip.

## Prior findings at this head

| Prior finding | Disposition at 4671e582 | Evidence |
|---|---|---|
| F1 (R251-1, BLOCKER, Conformance/Robustness): filename decoding changed literal paths | **RETAINED IN PART.** The measured UTF-8/ASCII/Latin-1 instance is resolved. Its stated required outcome ("independently of Python's filesystem encoding ... never silently prove a different pathname") is still violated under a Big5 codec; that remainder is open as R244-A. | 43/43 locale assertions per child encoding, including the `c3 a9` name beside an unchanged `e9` alias (`receipts/selftest-head.out`). Restoring the pre-b911 transport fails the default self-test in all three forms tried: `restore-pre-b911-all`, `restore-git-utf8-only` and `restore-replay-utf8-only` each fail `locale-ascii-process` and `locale-iso8859-1-process`; `restore-base-text-git` crashes the self-test with exit 1. |
| F2 (R251-1, MAJOR, Tests/Conformance): no locale regression coverage | **RESOLVED** for its original defect. Coverage stops at codecs that round-trip; that gap is part of R244-A. | The default owner runs fresh UTF-8, ASCII and Latin-1 children with byte-defined `mktree` names, positives, negatives, entry/postimage/patch checks and exact path assertions. Latin-1 ran through a disposable `localedef` in this round. |
| F3 (R251-2, MINOR, Tests/Robustness/Conformance): Latin-1 parent assertion | **RESOLVED.** The separate ASCII-parent crash is recorded as R244-B. | Latin-1 parent: 455/455, exit 0. Restoring `repr(path)` fails exactly one assertion, `retention-literal-revert-'raw-\udcff'-path`, under a Latin-1 parent. Under a UTF-8 parent that restoration stays green, as expected for a parent-locale defect (`receipts/mutations.json`). |

## Verified at this head (supporting results within the unclean lenses)

- **G1:** matches the decision (`merge_containment_replay.py:37-57`): exactly
  one source-only merge, two ordered parents, P2's sole parent is P1, and
  tree(M) = tree(P2). The actual donor merge `f27b455` has parents
  `7fa64e9`, `9790ac7`; `9790ac7`'s sole parent is `7fa64e9`; both trees are
  `cf1818d9`.
- **H:** reuses the unchanged whitespace-exact helper. Arm order is preserved:
  ancestry, touched path, linear patch-id, then the new fallback
  (`check_merge_containment.py:540-586`).
- **T:** the identity, mode and raw-merge rules match CONTRIBUTING 221-232.
  Only rc 0 plus byte-equal tip output proves retention. rc outside 0-127
  raises a measurement error.
- **Existing arms preserved:** the 145 base assertion names are identical at
  head (`receipts/base-arms.txt` = `receipts/head-orig-arms.txt`). New:
  44 replay, 25 mutation, 112 retention and 3×43 locale assertions. 455 total,
  21 s wall time.
- **Actual gPTP processor PR62:** `UNKNOWN`/1 at both `f0f1c055` and
  `c1b61743`, naming `tb/tsngen/mutants.py` and
  `tb/verilator/gaskets/mutants.py`; the base gives `STRANDED`/1. PR61-like
  `9790ac7` stays `contained`/0 at both targets (`receipts/pr62-actual.txt`,
  `receipts/pr61-actual.txt`).
- **Patch hashes:** the CONTRIBUTING command reproduces all four decision
  hashes under isolated configuration (`receipts/patch-hash-repro.txt`).
- **Bounded alignment probe** (`probes/probe_alignment.py`): 10,272
  revert-constructed single-hunk cases over a 3-line alphabet. 9,879 were
  refused. All 393 acceptances are byte-consistent with the source hunk
  retained under one non-overlapping edit, and 0 are true mis-merges. This is
  bounded evidence, not a proof.
- **Docs gates:** the em-dash gate over the base..head diff reports 0
  findings on 49 added lines (`receipts/em-dash.txt`). The Python idiom
  ratchet passes (`receipts/py-idiom.txt`).

## Out-of-scope observation (pre-existing, unchanged arm; recommend a new Issue)

O-1 affects `scripts/check_merge_containment.py:474-475` and `:189-190`.
Running the checker from a repository subdirectory makes the literal pathspecs
cwd-relative. The touched-path arm then compares non-existent paths and
reports `contained`/0 for stranded linear work, at base 52711029 and at head
alike (`probes/probe_subdir.sh`, `receipts/probe-subdir-{base,head}.txt`).
This PR's T uses `ls-tree --full-tree` and is not the cause. It is not counted
against this head's lenses.

## Reviewer-owned lens ledger

| Lens | Status | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (R244-A, R244-B) | Decision 5777210218 vs `merge_containment_replay.py:37-159`; `check_merge_containment.py:524-586`; `CONTRIBUTING.md:204-255`; actual PR62/PR61 at both targets; patch-hash reproduction; 145-arm preservation | R244-1 | 4671e582cfa4bba4809b9e3a354ce5b6eb967f99 |
| RTL (architecture/interface) | UNCLEAN (R244-A) | Diff scope: CONTRIBUTING plus 7 Python files; no HDL, CDC/reset/timing, firmware, workflow or gitlink change. `_git` contract `check_merge_containment.py:93-101`; replay module interface `merge_containment_replay.py:15-16,138-159`; exit contract `:78-82,886-917`; `_tree_entry` absence contract `:60-65` | R244-1 | 4671e582cfa4bba4809b9e3a354ce5b6eb967f99 |
| Robustness | UNCLEAN (R244-A, R244-B, R244-D) | Measurement and failure paths `merge_containment_replay.py:24-35,79-95,114-153`; fault controls `retention.py:185-231`; Big5, ASCII-parent, UTF-8-print, subdirectory and alignment probes | R244-1 | 4671e582cfa4bba4809b9e3a354ce5b6eb967f99 |
| Tests | UNCLEAN (R244-A, R244-B, R244-C, R244-D) | Default self-test 455/455 (`receipts/selftest-head.out`); 19 mutation/restoration/parent-locale probes (`receipts/mutations.json`); `merge_containment_selftest_{replay,retention,locale,mutations}.py` | R244-1 | 4671e582cfa4bba4809b9e3a354ce5b6eb967f99 |
| Docs | UNCLEAN (R244-A) | `CONTRIBUTING.md:204-255`; module docstring `check_merge_containment.py:44-57`; `_git` docstring `:94`; PR #519 body; em-dash and idiom gates | R244-1 | 4671e582cfa4bba4809b9e3a354ce5b6eb967f99 |

No lens is banked clean by this round. After a correction, every lens needs
covering again at a head that includes the change.

## Hosted and manager evidence inspected (not executed by this reviewer)

- **Hosted check runs at the exact head** (`receipts/head-check-runs.txt`,
  metadata only; logs not read):
  - 21 successful runs. All seven required contexts succeeded. Verilator
    shards 0-4 and Yosys shards 0-3 actually executed, and both aggregates
    succeeded.
  - 5 cancelled runs, each superseded by a later successful run of the same
    job name.
  - 1 skipped run: "Physical gPTP (nightly and manual)", which is outside the
    required aggregates.
- **Manager source ledger at this head**
  (`review-evidence/423-r1/corrected-source3/manager` at `2738c16f`; only
  `results.json` and `source.json` were read): 49/49 static/builder commands
  exit 0, including `check_merge_containment.py --selftest`, `docs_check`,
  `check_em_dash --base 52711029` and `gen_toc`. The five native groups exit
  0. These are manager executions, not this round's.

## Real limits of this round

- Not run by this reviewer: the full parent, PP, gPTP, Yosys or builder banks,
  Docker/act, the host replica, hardware, or Verilator. The pinned Verilator
  identity was therefore not needed or checked. Physical calibration is NOT
  RUN; field skips are not hardware proof.
- The Big5 result used a disposable `localedef` output and fixed-byte plumbing
  fixtures. Big5-HKSCS and other codecs were measured at the codec level only
  (`receipts/probe-codec-roundtrip.txt`), not through the CLI.
- Mutation coverage is the 19 listed probes. The alignment probe is bounded
  (a single hunk, a 3-line alphabet and 10,272 evaluated cases).
- Hosted evidence was check-run metadata only. Manager evidence was read from
  public summaries, not re-executed.
- Tooling: Python 3.14.7, Git 2.55.0. At most 8 parallel jobs.

## Pending manager duties

- Publish this report.
- Route R244-A..D to the author lane. Re-review the corrected exact head with
  all five lenses; nothing here approves a prospective fix.
- File a new Issue for O-1.
- Before merge, all of the following remain required:
  - the trusted local replica and protected hosted contexts on any new head;
  - two independent positives;
  - final current-dev candidate validation (source base 52711029, live dev
    483a133e at review start);
  - authorized merge, post-merge containment, and Closed/Done.

## Reproduction

All paths are relative to this output directory; `<clone>` is a checkout at
the exact head.

- Base scripts:
  `git -C <clone> archive 52711029f374650dc93830d5ea28e81cb5c8f410 scripts | tar -x -C base-src`
- Disposable locales:
  `localedef --no-archive -i zh_TW -f BIG5 tmp/locales/zh_TW.BIG5`
  `localedef --no-archive -i en_US -f ISO-8859-1 tmp/locales/en_US.ISO-8859-1`
- Big5 probe:
  `python3 probes/probe_big5.py build tmp/big5fx`
  `LOCPATH=tmp/locales LC_ALL=zh_TW.BIG5 PYTHONUTF8=0 PYTHONCOERCECLOCALE=0 python3 probes/probe_big5.py run tmp/big5fx <clone>/scripts/check_merge_containment.py`
  Run it with `GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null`, and compare
  with `PYTHONUTF8=1` and with `base-src/scripts/...`.
- `probes/probe_big5_linear.sh tmp/big5lin`, then run either checker with
  `--no-fetch --base main pr` in that directory.
- `python3 probes/mutate.py <clone> .` (needs `tmp/locales/en_US.ISO-8859-1`).
- `python3 probes/probe_guards.py <clone> tmp/guards`
- `probes/probe_subdir.sh <checker> tmp/subdir-probe`
- `python3 probes/probe_alignment.py 24000 8 tmp`
- `python3 probes/codec_roundtrip.py`
- `python3 probes/integrity.py <clone> 4671e582cfa4bba4809b9e3a354ce5b6eb967f99 afc8eadb3e9f6611dfb62347580b49dc721d25c0`

Raw receipts contain absolute local paths from this host; neutralize them
before publication.

## Final integrity

`receipts/final-integrity.json` (exit 0):

- HEAD `4671e582cfa4bba4809b9e3a354ce5b6eb967f99`, tree
  `afc8eadb3e9f6611dfb62347580b49dc721d25c0`.
- All 856 tracked root blobs match their committed bytes and modes by direct
  hashing.
- The index equals HEAD at stage 0, and porcelain status is empty.
- Required submodules are real directories at their root gitlinks, with clean
  status and tracked files hash-verified:

  | Submodule | Revision | Files |
  |---|---|---|
  | third_party/verilog-axis | 48ff7a7e2ef782cf778d47910cf85835c64b1bce | 214 |
  | protocol-processor | 424c688fa2205b934a7689a58f2aa766420f2326 | 222 |
  | gptp-processor | c1b617435824929a790739ea8585c3fe1a328cc0 | 103 |

- Optional `external` is uninitialized, as at start.
- No clone file was edited. All fixtures, source copies and locales were built
  under this output directory and later removed; logs and receipts are kept.
  The PR62 reconstruction used a separate bare repository borrowing the gPTP
  submodule's objects read-only.

R244-1 FINISHED
