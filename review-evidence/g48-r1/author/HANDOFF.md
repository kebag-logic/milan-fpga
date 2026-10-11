# Documentation lane #48

Status: REVIEW READY. All acceptance items and documentation proofs are complete.

Head: `7cc9c492145dd9e7c5c0e1d4695a261ea8025850`.
Commit: `docs: align parent integration ownership at ac2c5e77`.

## Checkout

Branch: `g48-readme`. Base: `bd466e60074539a7147e3d1613c9dcb0f93e2544`.
Origin and initial clean state verified.
Parent reference: `dev` at `ac2c5e77`; resolved to `ac2c5e77bba1c0ae20ce2f69f711a1d17ead94a5` through git. The cloned dev branch resolves to that same object.

## Scope and stop conditions

Documentation only. Preserve option-off behavior and visible issue-linked gaps.
Stop if RTL, script, or test changes are required. No parent modifications or publication.

## Changes and parent evidence

Five Markdown pages updated. No RTL, scripts, tests, or diagrams changed.
The base already stated default-on; this lane supplies exact parent citations,
explicit fabric ownership, safe option-off behavior, and issue-linked gaps.

| Donor location | Parent evidence at the pinned object |
| --- | --- |
| `README.md:21` | `hdl/milan/milan_datapath.sv:73` |
| `README.md:22` | `docs/design/GPTP_PLANE.md:6` |
| `README.md:23` | `docs/design/GPTP_PLANE.md:49` |
| `docs/INTEGRATION.md:10` | `hdl/milan/milan_datapath.sv:73` |
| `docs/INTEGRATION.md:12` | `docs/design/GPTP_PLANE.md:6` |
| `docs/INTEGRATION.md:14` | `docs/design/GPTP_PLANE.md:48` |
| `docs/INTEGRATION.md:16` | `docs/design/GPTP_PLANE.md:49` |
| `docs/INTEGRATION.md:18` | `docs/design/GPTP_PLANE.md:43-44` |
| `docs/INTEGRATION.md:35` | `docs/ARCHITECTURE_HW_SW_SPLIT.md:165` |
| `docs/INTEGRATION.md:37` | `README.md:167-170` |
| `docs/INTEGRATION.md:41` | `hdl/milan/milan_datapath.sv:7614-7624` |
| `docs/INTEGRATION.md:42` | `hdl/milan/milan_datapath.sv:2850-2858` |
| `docs/INTEGRATION.md:43` | `hdl/milan/milan_datapath.sv:2850-2852` |
| `docs/INTEGRATION.md:44` | `README.md:167-170` |
| `docs/INTEGRATION.md:45` | `README.md:167-170` |
| `docs/INTEGRATION.md:46` | `README.md:167-170` |
| `docs/INTEGRATION.md:47` | `README.md:167-170` |
| `docs/MANAGER.md:18` | `hdl/milan/milan_datapath.sv:73` |
| `docs/MANAGER.md:19` | `docs/design/GPTP_PLANE.md:6` |
| `docs/MANAGER.md:20` | `docs/ARCHITECTURE_HW_SW_SPLIT.md:165-175` |
| `docs/MANAGER.md:109` | `docs/guides/gptp/MANAGER.md:33-35` |
| `docs/MANAGER.md:111` | `docs/design/GPTP_PLANE.md:350-366` |
| `docs/MANAGER.md:113` | `docs/design/GPTP_PLANE.md:363-366` |
| `docs/MANAGER.md:121` | `docs/design/GPTP_PLANE.md:43-44` |
| `docs/MANAGER.md:122` | `docs/design/GPTP_PLANE.md:49` |
| `docs/SOURCE_EVIDENCE.md:36` | `hdl/milan/milan_datapath.sv:73` |
| `docs/SOURCE_EVIDENCE.md:37` | `docs/design/GPTP_PLANE.md:6` |
| `docs/SOURCE_EVIDENCE.md:38` | `docs/ARCHITECTURE_HW_SW_SPLIT.md:165-175` |
| `docs/history/v1/PROJECT_STATUS.md:22` | `hdl/milan/milan_datapath.sv:73` |
| `docs/history/v1/PROJECT_STATUS.md:23` | `docs/design/GPTP_PLANE.md:6` |
| `docs/history/v1/PROJECT_STATUS.md:24` | `docs/ARCHITECTURE_HW_SW_SPLIT.md:165-175` |

## Default-off search

Current maintained Markdown has no default-off or default-disabled claim.
The raw search returned 1 (no matches); the absence check returned 0.

```sh
rg -n -i -U --glob '*.md' --glob '!docs/history/**' '\bdefaults?[\s-]+(?:off|disabled)\b|\b(?:off|disabled)[\s-]+by[\s-]+default\b' .
```

All historical matches occur in `docs/history/v1/PROJECT_STATUS.md`:
line 20 is the new dated forward note; line 35 preserves the old default-off
statement. The 2026-08-31 archive date and original narrative remain unchanged.
The current note is dated 2026-10-11.

Four planted scratch-document mutants were rejected: `defaults off`,
`default-off`, `disabled by default`, and a wrapped `defaults` / `off`.
Each mutant produced a match (raw search 0; absence check 1).
The scratch fixture was removed; no repository page was mutated.
Evidence: [default-off search](validation/default-off-search.log).

A broader manual review of default, ownership, comparison, and option-off
wording found no additional maintained page requiring an integration change.

## Documentation gates

All rows ran at `7cc9c492145dd9e7c5c0e1d4695a261ea8025850`. Each command had its own log and return-code file.
Independent commands ran concurrently under a foreground wait; all completed.
No command was piped. Temporary directories were outside the repository.

| Gate | Return code | Result | Evidence |
| --- | --- | --- | --- |
| `make -j16 docs` | 0 | All six documentation commands passed | [Log](validation/make-docs.log), [rc](validation/make-docs.rc) |
| `make -j16 diagrams-check` | 0 | Both diagram commands passed | [Log](validation/make-diagrams-check.log), [rc](validation/make-diagrams-check.rc) |
| `python3 scripts/check_docs.py` | 0 | 11 current pages; 17 historical pages | [Log](validation/docs.log), [rc](validation/docs.rc) |
| `python3 scripts/check_docs.py --selftest` | 0 | 10 arms | [Log](validation/docs-selftest.log), [rc](validation/docs-selftest.rc) |
| `python3 scripts/check_source_evidence.py` | 0 | 20 exact anchors; zero findings | [Log](validation/source-evidence.log), [rc](validation/source-evidence.rc) |
| `python3 scripts/check_source_evidence.py --selftest` | 0 | 7 arms | [Log](validation/source-evidence-selftest.log), [rc](validation/source-evidence-selftest.rc) |
| `python3 scripts/generate_diagrams.py --check` | 0 | 9 pinned assets; 3 source-bound PNGs | [Log](validation/diagrams.log), [rc](validation/diagrams.rc) |
| `python3 scripts/generate_diagrams.py --selftest` | 0 | 10 arms | [Log](validation/diagrams-selftest.log), [rc](validation/diagrams-selftest.rc) |

`git diff bd466e60 HEAD --check` also returned 0.
Existing self-tests include their planted negative controls.
No repository check, script, or test was added or changed.

## Parent citation proof

All 31 ownership-related parent source citations resolve through git at
`ac2c5e77bba1c0ae20ce2f69f711a1d17ead94a5`, covering 14 distinct file/line targets.
Each selected excerpt was read and checked against its documented claim.
The source parameter is at line 73; the issue's earlier line 89 is stale.

The one-off citation audit returned 0. In-memory mutants for the previous
revision, stale line 89, missing source file, and an incorrect default-off
source construct each returned failure (1). No production files were mutated.
Evidence: [citation results](validation/parent-citations.log).

The pre-existing historical measurement link in `docs/MANAGER.md:70`
intentionally retains its original evidence revision. It is not an ownership
citation and was not changed.

## Gap and navigation changes

| Donor location | Change | Parent context and tracking |
| --- | --- | --- |
| `README.md:32`, `README.md:34` | Pin note and option-off navigation | `hdl/milan/milan_datapath.sv:73`; `docs/design/GPTP_PLANE.md:49` |
| `README.md:50`, `docs/MANAGER.md:104` | Receive fix remains in review | Parent `docs/guides/gptp/MANAGER.md:48`; donor #35 and open PR #80 |
| `README.md:51`, `docs/MANAGER.md:105` | Donor asymmetry/calibration/tuner work stays open | Parent `docs/design/GPTP_PLANE.md:362-366`; donor #58 |
| `README.md:52`, `docs/MANAGER.md:106` | Physical acceptance still owed | Parent `docs/guides/gptp/MANAGER.md:35`; parent #117 |
| `README.md:53`, `docs/MANAGER.md:107` | Timestamp calibration/split incomplete | Parent `docs/design/GPTP_PLANE.md:365`; parent #64 and #488 |
| `README.md:55`, `docs/INTEGRATION.md:49` | Route readers to current gap table | Parent `docs/guides/gptp/MANAGER.md:33-35`; donor manager risks |
| `docs/INTEGRATION.md:20`, `docs/MANAGER.md:28`, `docs/SOURCE_EVIDENCE.md:40` | Record the exact parent revision | Parent object resolved through git; citations above |
| `docs/MANAGER.md:115` | Live tuning remains outside the product contract | Parent `docs/design/GPTP_PLANE.md:366`; donor #58 |
| `docs/history/v1/PROJECT_STATUS.md:20` | Add forward note while preserving dated history | Parent `hdl/milan/milan_datapath.sv:73`, `docs/design/GPTP_PLANE.md:6`, `docs/ARCHITECTURE_HW_SW_SPLIT.md:165-175`; closed donor #13 |
| `docs/history/v1/PROJECT_STATUS.md:25` | Link current guidance and physical acceptance | Parent `docs/guides/gptp/MANAGER.md:35`; parent #117 |

Current issue states were read from their public records. Donor #35 is open
with its fix in PR #80 review; #58 is open. Parent #117, #64, and #488 are open.
Parent #116 is closed; that digital transition does not close #117.
Physical acceptance means one DUT against the reference peer. The old
archived two-board description is not a new acceptance claim.

## Acceptance

| Item | Result |
| --- | --- |
| Current README and all current integration-default pages match the parent | Met; five Markdown pages changed, including one historical forward note |
| Fabric product ownership and verification-only option-off are unambiguous | Met; pinned source citations and explicit safe-value table |
| Option-off behavior remains documented | Met; TX bypass, CSR PHC controls, zero publication, `tu=1`, inert writes |
| Donor and hardware gaps remain visible | Met; #35, #58, parent #117, #64, and #488 remain explicit |
| Documentation-only scope | Met; no RTL, script, test, diagram, or generated-file change |

## Review boundaries

The lane does not adopt a donor revision in the parent. The parent clone is
unchanged and has no new commit. No hardware or bench access occurred.
The documentation proof does not claim runtime or physical acceptance.
The donor and parent working trees are clean. No jobs remain running.

## Output inventory

`validation/` contains only small text logs, return codes, and the tested head.
`ARTIFACTS.sha256` records output sizes and SHA-256 values.
No package installation, environment, tree export, or large file is included.

## Completion

TAKEN posted on issue #48 (comment 6105899652).
Local commit and all exact-head documentation gates completed.
Configured author identity matches the requested identity, verified with
`git log -1 --format='%an %ae'`.
[PR body](PR-BODY.md) is prepared for a new processor pull request.
Publication is limited to the required issue status comment; no push or PR action.
No STOP condition encountered.
Final issue status: `[A600] REVIEW READY` with the head recorded above.
The issue comment is the final publication step; the commit remains local.
