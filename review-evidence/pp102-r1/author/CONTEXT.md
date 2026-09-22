# A180 author context

This author used the public issue bodies/comments for PP #102, #95 and #97,
the public parent #400 original finding, donor source/docs/workflows, and
immutable parent policy source. No private author or reviewer transcript was read.

## Public contract

- Issue: https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/102
- Ready/takeover: https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/102#issuecomment-5781900157
- TAKEN before the source edit: https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/102#issuecomment-5781920399
- Original finding: https://github.com/kebag-logic/milan-fpga/issues/400#issuecomment-5781426819
- Fixture binding: https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/95
- Fixture distinctness: https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/97

The manager-created branch is `102-pp-fixture-warning-flags`, and the user
confirmed Project 10 In progress. The author verified the branch and clean
base `f70ba36ecb634467e4b1c3f0dbf1239d1e12af57` before the edit. R252 internal
Codex and R253 external Opus remain separate mandatory reviews. The author
did not start reviews or approve this change.

## Reconstructed requirements

The common CFLAGS already contain both warning flags. Parent
`cflags_missing` deliberately requires both flags in every quoted CFLAGS
group, including the supplementary macro group on the same invocation.
The original result is a policy integration defect, not evidence of missing
effective compiler warnings. The fix repeats the flags in that one group.

PP #95 exposes the existing 16-bit SRP Domain default through the real top
while preserving shipping default 2 and runtime adoption/link behavior. The
default pp_top build has no parameter override and runs every section. The
verification fixture uses `5A3C` and runs DV alone. Its 16-bit wire value and
12-bit class-D value distinguish a missing binding from the child default.
The expected value comes from the Makefile variable, never DUT readback.
DV covers reset, LINK_UP declaration, GET_TX_STATE, bridge adoption,
LINK_DOWN restoration with no declaration while down, and LINK_UP declaration.

PP #97 requires fixture distinctness at both widths: default and `5A3C`
compile; `0002` refuses with both assertion messages; `1002` refuses with
the class-D message only. The existing compiler-locale isolation regression
is part of `fixture-guards`. This one-line change leaves those files,
assertions, scenarios, recipes, macro and fixture value byte-identical.
The historical dropped-binding and child-default mutation outcomes were read
from public #95/#97 context, not rerun or claimed as fresh author results.

## Policy and gates

Parent policy was read at immutable commit
`483a133ed08867ea0d300d2b4a027b5b48a4282f`: CONTRIBUTING sections 2/3,
the Rule 11 C++ warning policy in CODE_QUALITY, actual `cflags_missing`, and
the checker warning-flag controls. Its population refusal, per-group policy,
and ratchet remain unchanged. Policy and checker Git blobs plus SHA-256
identities are in `context/parent-policy-identity.json` and
`context/checker-inputs.json`. Imports used `-B`; the parent checkout was
read only.

Donor README, docs/README, HDL engineer guide, hdl/README, pp_top README,
root and pp_top Makefiles, fixture-guard scripts, verification and Domain
documentation, `.github/workflows/hdl.yml`, lint and suite runner were read.
The workflow pins Verilator v5.050; the scoped selector, intermediate wrappers,
and real ELF binary were verified before the build. Existing local tool
installations were consumed without edits. No container was started.

The build keeps the original recipe and passes its original VFLAGS via a
make command-line override with only `-j 0` replaced by `-j 8`.
Outer make is serial. `build.py`, `build-command.json` and the unfiltered
build log contain the exact recipe and environment. No scenario is skipped
by the author; the fixture running DV alone is the existing suite contract.

Full donor `run_suites.sh`, Yosys, historical nvm_port figures, hosted gates,
independent five-lens reviews, current-main candidate validation and
post-merge containment are manager-owned and pending. Parent #400/#403
acceptance and exact-only donor pin authorization remain unchanged.

## Evidence capture

All shell command strings begin with `rtk`, following the user-supplied
`$WORKSPACE_HOME/.codex/RTK.md`. Validation uses `rtk proxy` so raw logs retain
compiler commands, checks and failures. `commands.jsonl` records validation
argv, cwd, UTC start, elapsed duration, exit and raw-log path. Source edits
used `apply_patch`; only one source line changed. Evidence helpers and
artifacts live outside the donor checkout.

`source-manifest-*.json` records every tracked file's Git tree mode/kind/blob,
index stage/mode/blob and disk bytes/kind/mode, with raw index/tree exports.
`source-bytes/` stores every captured source byte sequence by SHA-256.
The donor has no gitlink dependency pins. Git identity reads explicitly use
`GIT_NO_REPLACE_OBJECTS=1`. Final checks compare tested bytes with committed
bytes and reject hidden source drift, mode changes, index changes or extras.

Before the evidence harness was created, read-only discovery read RTK.md,
checked ancestor/nested AGENTS files (none found), inspected branch/status,
base commit, repository file inventory, README/docs and public issue #102.
Those initial discovery commands had no failures. The captured base manifest
and subsequent public API logs independently preserve their material facts.
