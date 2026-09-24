[A286] Local validation evidence

Head: `b068763c849a18096b0f46cf9b18e0f904e4d708`.
Base: `ffcbd33de70278ae34b533dcbadde0b36c8cba13`.
All commands ran in the foreground from the candidate worktree.
No gate output was piped.

The final compiler-free full builder run exited 0.
Gate 1b refused 249/249 mutations and accepted 35/35 firmware edits,
4/4 Makefile edits, and elaborated 46/46 RTL mutation variants.
Its audit records zero gate 1b firmware compiler invocations.
The final pinned-SDK full builder run also exited 0.
Gate 1b refused 304/304 mutations and accepted 38/38 firmware edits,
4/4 Makefile edits, and elaborated 46/46 RTL mutation variants.
Its audit records 513 gate 1b firmware compiler invocations.
The final input hashes match the clean committed tree.

`run-builder.py` runs `sw/builder/test_builder.py` as `__main__`.
SDK mode passes `--require-rv32`, verifies the existing pinned SDK,
and maps only the settled absolute compiler selector to that SDK.
This follows the assigned manager driver without changing HOME or PATH.
Absent mode hides all three cross candidates and preserves native probes.
Full-bank host harnesses still compile as native harnesses.
Neither mode creates or installs a compiler, environment, or tree copy.

Reproduce the full runs from this worktree:

```sh
python3 <packet>/run-builder.py absent --tag full-absent
python3 <packet>/run-builder.py sdk --tag full-sdk
```

The public hostile cases are reconstructed directly in `run-builder.py`.
Their source is evidence commit `c8598794c48d70a98a59bcdced03904aa139bc60`:
`review-evidence/408-r1/reviews/R272-1/scripts/cases_r3.py` and
`review-evidence/408-r1/reviews/R273-1/scripts/make_more_cases.py`.
R273-S3 comes from the same round's `scripts/make_cases.py` (H8).
Temporary fetched evidence was deleted after reading.

The probe runs execute the real `assert_boot_contract` in memory.
They return before the suite's corpus loops and use disposable output roots.
The disabled runs replace only the new per-mode assertion closure.
Every hostile case is refused by its named rule when enabled,
and accepted by the rest of the whole contract when disabled.
R273-S3 remains accepted in both modes, enabled or disabled.
These are recorded in `probe-{sdk,absent}{,-disabled}.json`.

```sh
python3 <packet>/run-builder.py sdk --probe --tag probe-sdk
python3 <packet>/run-builder.py sdk --probe --disconnect --tag probe-sdk-disabled
python3 <packet>/run-builder.py absent --probe --tag probe-absent
python3 <packet>/run-builder.py absent --probe --disconnect --tag probe-absent-disabled
```

Required static gates all exit 0 at the stated head.
`run-static.py` records exact argv, environments and exits in `static-results.json`:

- `python3 -B scripts/docs_check.py`
- `GIT_DIR=/tmp/544-no-git-metadata python3 -B scripts/docs_check.py`
- `python3 scripts/check_baremetal_only.py --check`
- `python3 scripts/check_em_dash.py --base ffcbd33de70278ae34b533dcbadde0b36c8cba13`
- `python3 scripts/check_doc_style.py`
- `python3 scripts/gen_toc.py --check`
- `python3 scripts/check_doc_paths.py`
- `python3 scripts/check_py_idiom.py`
- `git diff --check`
- `git diff --check ffcbd33de70278ae34b533dcbadde0b36c8cba13 HEAD`

The no-git documentation run selects the actual filesystem inventory fallback,
without deleting worktree metadata or exporting a tree.
The Contents and em-dash gates use the existing shared documentation environment.
The default interpreter lacked the pinned renderer dependency.

`compare-retained.py` verifies all 15 original table definitions, additions,
accepted-case updates and the rejection grader unchanged and in order.
The current implementation adds five statements to that population.

Development failures retained for transparency:
`full-sdk-1.log` found an incomplete new rename fixture; corrected.
`full-sdk-2.log` found the new casted-address escape; corrected.
`full-sdk-3.log` passed an intermediate version (304/304, 37/37 plus 4/4).
The final runs supersede those development receipts.

Declared skips are not claimed as coverage.
Both full modes lack the gate 11 resource-calibration report.
The compiler-free mode also declares the missing compiler instruments NOT RUN.
No hosted CI, independent review, hardware, push, PR mutation or merge occurred.
