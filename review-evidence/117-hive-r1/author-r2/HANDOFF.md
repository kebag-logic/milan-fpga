# Round 2 handoff

[A376] Author for PR #598, issue #117.

Status: STOP. Items 1-3 are committed and gated; item 4 requires an existing include inventory. Start head: `bcba79a50ecd2eca99db91c4f3802d888eaac7e4`.
Branch: `117-la-avdecc-enum`. No push is authorized.

Assignment: https://github.com/kebag-logic/milan-fpga/issues/117#issuecomment-5858871629

## Requested changes

| Item | Change and file:line | Finding satisfied |
|---|---|---|
| 1 | `docs/findings/117_GPTP_SILICON_EVIDENCE.md:652` pins the public packet at `557087b34479c9ba0f1fc1722b6e577a0ecc3998`; `:658` lists the three original dump hashes and the serial masking; `:688` connects Raw artifacts to B4 | R358-1 F1 / R359-1 F1 |
| 2 | `docs/findings/117_GPTP_SILICON_EVIDENCE.md:6`, `:30`, `:33`, `:55`, `:464`, `:469`, `:540` distinguish both image dates, retain the superseded FAIL, name #534/#529 and ancestry as the likely explanation, and list the three remaining NOT RUN rows | R359-1 F2 / R358-1 S1, S2 |
| 3 | `docs/findings/117_GPTP_SILICON_EVIDENCE.md:635` names all nine probe defines, the enabled and disabled compatibility options, default CMake provenance at `6d61a92e`, and the no-warnings condition | R358-1 S3 / R359-1 S2 |
| 4 | `PACKET-ADDENDUM.md:7` records the known include-path order and source revision; `:15` identifies the missing installed-header inventory. Contents and versions cannot be asserted from the allowed packets. An existing inventory was requested; this item is not satisfied | R359-1 S3 |

## Gate results

All commands ran from `$LANES/117-la-avdecc-enum`.
All eight gates returned rc 0 at committed head `ecd36018a29f605efe790d33dd50382aec9c1201`.
Receipts: `gate-1.txt` through `gate-8.txt`; machine-readable index: `gates.json`.
The first six gates use `/tmp/117-a376-markdown/bin/python3`;
the bare-metal gate uses system `python3` and its required `--check` mode.
All ran in the foreground with 600-second timeouts, without pipelines.

| Gate | Result |
|---|---|
| python3 scripts/docs_check.py | rc 0; gate-1.txt |
| python3 scripts/check_doc_style.py | rc 0; gate-2.txt |
| python3 scripts/gen_toc.py --check | rc 0; gate-3.txt |
| python3 scripts/check_em_dash.py --base 2a2a7bb6 | rc 0; gate-4.txt |
| python3 scripts/check_doc_paths.py | rc 0; gate-5.txt |
| python3 scripts/ci_scope.py --selftest | rc 0; gate-6.txt |
| python3 scripts/check_baremetal_only.py --check | rc 0; gate-7.txt |
| git diff --check | rc 0; gate-8.txt |

## Delivery

PR-BODY.md: Round 2 section updated; item 4 remains pending.
TAKEN: https://github.com/kebag-logic/milan-fpga/issues/117#issuecomment-5858883277
REVIEW READY: not posted; item 4 is incomplete.
STOP: https://github.com/kebag-logic/milan-fpga/issues/117#issuecomment-5858985706
Committed head: `ecd36018a29f605efe790d33dd50382aec9c1201`. Subject: `Reconcile issue 117 enumeration evidence and build provenance`.

## Evidence verification

`evidence-checks.txt` verifies all ten B4 table hashes against the pinned manifest and public bytes. Only the three named serial-masked entity dumps differ. All five existing NOT RUN table rows are unchanged. The nine probe defines match the recorded build. PR #534 merge ancestry was verified locally.

The pinned Markdown dependencies are installed outside this packet in `/tmp/117-a376-markdown`; no dependency tree or large file is retained here.

The committed diff also passed `git diff --check 2a2a7bb6..HEAD`. The worktree is clean.

## Required next input

Provide an existing inventory of `$HOME/la_avdecc-probe/include`, with header contents and versions or their pinned source revisions. The allowed build receipt and validation notes name the directory but do not inventory it. The directory is absent on this workstation. No bench host or private transcript was accessed.

Once supplied, complete `PACKET-ADDENDUM.md`, update the packet status, and post REVIEW READY at the committed head. No repository edit is expected for that packet-only item.
