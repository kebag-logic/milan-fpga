# A179 factual policy-correction handoff

Issue: https://github.com/kebag-logic/milan-fpga/issues/517
Decision: https://github.com/kebag-logic/milan-fpga/issues/517#issuecomment-5781783857
TAKEN: https://github.com/kebag-logic/milan-fpga/issues/517#issuecomment-5781842453

Final local source head: `5874895eb817ed41c0f8be4eb427ad3315c29844`
Final source tree: `45a2a9b2b108a932db49d9ec595ff4b3f18a2b3e`
Parent / original benchmark source: `7ab1c8d0ad073fbc1977c455dea89b7b318d4e52`
Parent tree: `790849ab7fcf7c712c77fe051bb5fb6a45d830c2`
Branch: `517-bounded-simulation-pool`
Commit: `Bound simulation host-tool policy masks to their source contexts`

One correction commit, one line, no trailers. The source is clean and unpublished.
The live remote branch still points to `483a133ed08867ea0d300d2b4a027b5b48a4282f`;
local status is ahead by the existing implementation commit plus this correction.

## Correction and public authority

Only `scripts/check_baremetal_only.py` changed: 138 added lines. Five file-pinned
mask entries recognize exact process-control contexts in the suite runner,
its process tests and README. Masks remove only the allowed token, preserving
other policy text on the line. No file is excluded. No global term or path is
allowed. Existing inventory, protected product-document handling, prohibitions,
configuration parsing and old selftests are unchanged.

`policy-scope-proof.json` proves the original executable AST is identical after
removing only the five new entries, two private fixture/control helpers and one
selftest registration. The new positives are 20 literal source lines, covering
21 original findings; `committed-integrity.json` proves all 20 lines exist
verbatim in the original source. They are not generated from mask regexes.

New controls cover wrong-file copies, unrelated same-file text, extra same-line
copies, protected product docs, full path spellings without their context,
altered paths in the same call, longer prohibited terms, and extra T/R/S/H/K/O
prohibitions. The mixed OS/path refusal message tests both policy classes.

## Validation and failure disposition

Raw argv, cwd, source identity, exit, timing and output are in `raw/*.json` and
`raw/*.log`; `COMMANDS.md` indexes them. Receipts before the commit name the
then-current parent HEAD and working checker status/hash where recorded. They
are working-tree controls, not falsely labelled clean-commit executions.
The final committed checker SHA-256 is
`66a51849d055edd852dbda5f29d1463911181e775d0ed0edda4dd3f3ce799d0c`.

| Check | Result / receipt |
|---|---|
| Original source --check | exit 1, 21 findings / 827 files; `baseline-check` |
| Original --selftest | exit 0, 342 arms; `baseline-selftest` |
| Committed correction --check | exit 0, 0 findings / same 827 files; `committed-check` |
| Committed correction --selftest | exit 0, 601 arms, no skips; `committed-selftest` |
| Disposable mask mutations | 10/10 rejected with exit 2 and expected named controls; `mutation-probes`, `mutations/` |
| Unchanged runner controls | exit 0, 17/17; `runner-controls` |
| Unchanged phase controls | exit 0, 24/24; `phase-controls` |
| Tally and suite ownership selftests | exit 0; `tally-controls`, `ownership-controls` |
| Python idiom, docs, hygiene, evidence, fail-fast, TODO ownership | all exit 0; corresponding raw receipts |
| Committed whitespace and em-dash | exit 0; 57/57 em-dash controls, no Markdown changed |
| Full tracked-byte/mode/index and required-submodule proof | exit 0; `committed-integrity` |
| Existing policy/control preservation | exit 0; `policy-scope-proof` |

The local original failure log is byte-identical to the manager's immutable
[command 29 failure](https://github.com/kebag-logic/milan-fpga/tree/6d68faf6720e2af0cb96ab64984e7bcf77a3e758/review-evidence/517-r1/source-first-failure).
Both the original log and partial manager ledger are retained in `public/`.
Those original banks remain partial, not PASS, and do not clear this head.
This correction resolves the 21 policy findings under the public decision.

A preliminary draft passed 580 controls and the full check. Adding a stronger
boundary probe then failed with exit 2: the first prose mask could remove the
`Linux` prefix of `Linuxptp`. `preliminary-boundary-probe.log` retains the failure.
The final mask adds a token boundary and retains that regression arm. Final
601-arm and committed-head results pass. No failed receipt was overwritten.
The ten intentional mutations are expected failures, not source failures:
remove each of the five masks; globally broaden the runner OS token; broaden
the test process path; swallow the runner line; permit a wrong-file copy; and
permit a full process path without its context. Each fails its intended control.

## Source, benchmark and ratchet identities

All 853 parent tracked file bytes/modes and the index match the final commit.
Exactly the policy checker differs from the parent commit. The parent source
proof and complete per-file hashes are in `committed-integrity.json`.
All 13 tracked `.budget` files are byte-identical to the parent. No ratchet grew
or was rewritten. The checker and all other policy artifacts outside this
bounded change retain their existing contracts.

The five explicitly benchmarked artifacts are byte-identical to their originals:

| File under tb/verilator/milan_dp | Git blob | SHA-256 |
|---|---|---|
| sim_pool.py | `761ec858c7ad23abb81d215122de3c5d260e653e` | `de372fe49f6b6c3f3dce717a0179b6b3b3b57cac1bab08fd3fec615b80997914` |
| test_sim_pool.py | `ab93e2c5bfa37474320b1f40fd7cb71cc45e7704` | `fe07e1dbe0fb76fc1215beed4a5f4e975e14f38af246b0e5a5f6d27da383bada` |
| Makefile | `5266b593f66f15e6b0d2bc00cfc1e9713e254da8` | `cc2ebdc0fca19597636142eeb76211682d9c226ebf118bc010cfa81be869afb1` |
| sim_nxn.cpp | `5866a1b5beef2c268495e759755f6192526229d6` | `271fb2c908173d75625f72234d2c05670ee80f15ee97b6772469ef65d7ba06ab` |
| README.md | `d5b6cb89e9bee722b611490e99cf483d324e9705` | `4a73d13bd01cf13bf2bedbc8abb24636b87b68851125359485f7f28bdf50ffaa` |

Every other parent source file, including build recipes, harnesses, generators,
render controls, workflows and tracked generated headers, is also unchanged.
Required submodule HEADs, index entries and pinned bytes/modes are proven with
`GIT_NO_REPLACE_OBJECTS=1`, independent of status/index flags:

- protocol-processor: `424c688fa2205b934a7689a58f2aa766420f2326`, 222 files.
- gptp-processor: `c1b617435824929a790739ea8585c3fe1a328cc0`, 103 files.
- third_party/verilog-axis: `48ff7a7e2ef782cf778d47910cf85835c64b1bce`, 214 files.
- external: unchanged gitlink `efeb541ae5fe1e078332d8462dca2fc2d9cb8db5`, remains
  uninitialized, is not consumed by these gates and is not claimed validated.

The [original public author evidence](https://github.com/kebag-logic/milan-fpga/tree/30fc230e8df8ca32499c6e1bd294bfe0cdb38983/review-evidence/517-r1/author)
retains attribution to `7ab1c8d0ad073fbc1977c455dea89b7b318d4e52` and its original
tree. Its reported cold 1136.415 -> 1099.401 seconds and warm 987.247 -> 943.330
seconds are the original author's measurements, not measurements of the correction
head. No new benchmark, full suite or speed claim was produced by A179.

## Remaining responsibilities

The bounded policy correction is complete and ready for independent review.
#517 is not complete and no approval or clean review lens is claimed.
The root manager still owns the complete fresh parent/PP/gPTP/Yosys/builder
banks, trusted act, exact-head hosted gates and dedicated-worker comparison,
current-dev final candidate validation and post-merge containment. R245 internal
Codex and R246 external Opus remain independent, with their required reviews
pending. Acceptance criteria are unchanged. Source publication and merge remain
with the manager under their separate authorization.

No full banks, Docker/act, privilege escalation, shared install, hardware action,
processor-pin change, other-checkout edit, source push, PR, merge or additional
agent occurred. The separate frozen static-validation clone was not accessed.
No private earlier conversation or reasoning trace was read. The public archived
handoff and original public failure records were the evidence sources.
Focused commands used at most eight jobs; no simulation build bank was launched.

`MANIFEST.sha256` covers all handoff artifacts except itself. `scripts/` contains
the raw-command recorder, exact byte/index/submodule proof, policy preservation
proof, public-evidence capture and disposable mutation driver. Mutation patches
and per-probe argv/exits/output are retained. The mutation driver requires a
fresh output directory for reproduction and never edits the source checker.

Public correction handoff: https://github.com/kebag-logic/milan-fpga/issues/517#issuecomment-5782013463
