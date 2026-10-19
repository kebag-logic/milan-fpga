[R658] NEGATIVE - exact head 07c6c72fce79e705bcf28a70071497d0ce7040e4

External independent review R658-1 of issue #763 / PR #766.
Base: `e9cbb676d7fdd6539aa408e5dfe38870a4ae1a5f`.
Head tree: `c70d7afe29d34724474bfc05053fe3cb43801026`.

The new firmware test and both required mutants work at the intended
`endstation_ax7101_1x1_tdm8` shape. No production firmware, RTL, record format,
or gitlink changes occur in the four-file diff. Two MINOR findings remain:
new stale generated inventory entries and an overstated mutation count.
Under this review's completion rule, either prevents a positive verdict.

Reconstruction followed the repository contract and documentation index, then
the issue and public decisions, saved-state authorities, the two commits and
exact diff, and finally public executable evidence. No private author material
or another reviewer's report informed this verdict and ledger.

The [scope ruling](https://github.com/kebag-logic/milan-fpga/issues/763#issuecomment-6257040042)
says "both A and B" and "#763 closes on B. #637 closes on the board."
The firmware test gap is the acceptance subject here. The shipping map writer,
restore and cold-cycle acceptance remain #637's obligations. The ruling preserves
the existing record format; a row-count format change would violate this scope.

Findings

**R658-1-F1 - MINOR - Conformance, Tests, Docs**

Artifact: `ci/image/tool-inventory.json:148` and `:149`, following changes at
`sw/firmware/ctrl/test/aecp_arms.py:20` and
`sw/firmware/ctrl/test/aecp_mutants.py:508`.

Authority/evidence: `docs/testing/CI_IMAGE.md:765` requires reviewing script
changes and refreshing workflow provenance whenever inputs change. The inventory
still hashes both AECP scripts as their base versions. Independent
`inventory-provenance.json` identifies four stale inputs: two inherited entries
and these two newly stale entries. With the checksum-pinned parser available,
`python3 scripts/ci_tool_inventory.py --check` exits 2 with
`REFUSED: tool inventory differs from workflow installation requests`
(`inventory-check.log`, `inventory-check.rc`, `parser-setup.log`). Published
author receipts acknowledge the same drift. No public scope ruling waives the
provenance requirement for these new changes.

Impact: generated provenance does not describe the reviewed test scripts.
`ci/image/build.py:211` invokes this check before image preparation. Repairing
only the inherited drift would still leave this PR's two inputs invalid.
This does not change firmware behavior, but the affected gate and generated
contract are not clean. Omission from PR workflows does not remove the consumer.

Required outcome: refresh the generated inventory after reviewing the changed
inputs, explicitly accounting for inherited drift, so it matches the reviewed
source. Do not classify the new mismatch as inherited.

Verification: run the pinned-parser inventory generation/check, inspect the
diff and reproduce the check at the corrected head. Confirm the AECP hashes
match their source bytes and installation requests/tool pins have not changed
unintentionally. Re-review affected lenses.

**R658-1-F2 - MINOR - Tests, Docs**

Artifact: [PR #766, Status](https://github.com/kebag-logic/milan-fpga/pull/766),
the [REVIEW READY evidence](https://github.com/kebag-logic/milan-fpga/issues/763#issuecomment-6258557430),
and published `author/receipts/round-b/gates/test_ctrl_firmware/summary.txt`.

Authority/evidence: the PR and issue report "939 planted controls caught".
The published extract contains 939 top-level `[ok]` lines, but 61 are ordinary
`[ok] arm ...` outcomes, including normal model, entity, RV32 and application
runs. The remaining lines comprise 520 control-source mutant runs, 78 AECP
mutant runs, 278 SRP mutant runs and two dependency-pin refusal controls.
Thus it records 876 source-mutant executions, plus two pin controls, not 939
planted controls. `public-gate-audit.json` and `audit_artifacts.py` reproduce
the classification against the current AECP table and gate execution order.
The summary also mislabels all 939 lines as campaign lines. AGENTS.md requires
reproducible evidence; the Tests lens requires claimed negative coverage to be real.

Impact: the published measurement overstates planted-control executions by
counting ordinary passing arms. The gate's PASS and both new mutants remain
supported. This is a numerical evidence claim, so the wording-only RESIDUE
exception does not apply.

Required outcome: correct the PR, issue evidence and receipt summary, then
regenerate affected indexes/manifests. One accurate replacement is:
"Firmware gate PASS; 876 source-mutant executions caught and two pin-refusal
controls passed; 61 normal arm outcomes passed (939 top-level `[ok]` lines)."
Alternatively omit the aggregate count while retaining named evidence.

Verification: derive the count from classified outcomes and verify corrected
public text, summary and receipt hashes agree. No source fix or repeat of the
complete firmware bank is needed for this correction.

**R658-1-F3 - RESIDUE - Docs**

Artifact: PR #766 Status and Linked Issue / roles.

Authority/evidence: the body still says "two commits, not yet pushed" and both
reviewer roles are "to be assigned". The head is published and the public
review-start comments assign both reviewers.

Impact: stale narrative only; no measurement, test, verdict or requirement claim
changes. This does not make a lens unclean.

Exact fix: replace "two commits, not yet pushed" with "two commits at published
head `07c6c72f`"; replace the role placeholders with the assignments already
recorded in the public review-start comments. Do not imply approval.

Verification: compare the body with the published head and assignments.

Independent lens results

* Conformance: `test_aecp.cpp:250` follows MATERIALIZATION 8.3/V3g and FASTCONNECT
  6.1. Both iterations remove mappings using command 45, check an empty set and
  a seven-row non-default opposite set, commit, require magic `0x1722` and an
  all-UNUSED payload, reset defaults and boot retained media. This implements
  the issue's Milan 5.3.9.1/5.3.10.1 persistence test scope. The format is
  untouched. Functional acceptance is met; F1 leaves the engineering provenance
  requirement open.
* [R658] PASS RTL - `aecp_arms.py:13`, `aecp_mutants.py:501`, `aecp_nvm.c:53`,
  `ctrl_nvm/nvm_store.c:292` and `:497` - the sibling-store path selects the same
  store in a checkout and the isolated planted store in a campaign. The actual
  campaign CLI detects each new mutant. No clock, reset, CDC, layout, ABI,
  production-source or gitlink change occurs. The shipping gap is independently
  supported by `protocol-processor/hdl/aecp/KL_aecp_nvm_writer.sv:119` and `:397`,
  `hdl/milan/KL_pp_shadow.sv:929`, and MATERIALIZATION's status paragraph.
* [R658] PASS Robustness - `test_aecp.cpp:194`, `:250`, `:288`, `:322`,
  `aecp_nvm.c:60`, `aecp_state.c:71`, and `ctrl_nvm/host/nvm_fmodel.c:43` - clean
  NVM checks cover malformed entries/holes, refusal, storage bounds, empty-map
  restoration and reset. Each new directional case starts blank, proves the
  default reset and compares saved non-default bytes after commit and reboot.
  Both mutants fail with traces for types 14 and 15. Flash power-on preserves
  media while clearing device state; store boot clears its own state. Geometry
  limits below are not expanded into a production claim.
* Tests: complete application binaries pass at one and two interfaces (74 tests
  each). The actual campaign CLI catches both new defects. Isolated plants
  reproduce the named failures. Without the new test, the store plant passes
  all 73 other application tests; the owner plant still fails the existing
  framing/empty-set test. The shipping-shape NVM suite passes with address
  instrumentation (8 tests). F1 and F2 remain open.
* Docs: `sw/firmware/ctrl/aecp/README.md:4`, `:100`, `:133` and the PR distinguish
  opt-in firmware from the shipping image. New text describes framed UNUSED
  records and the planted sibling store correctly. New source comments state
  behavior/reason with #763 and the test's Milan clauses, and add no bench labels,
  lane names, reviewer identities, round labels or issue-comment IDs. The public
  manifest lists exactly its 55 files; all 52 receipt files verify against their
  published hashes; all 51 non-index receipt rows match membership, size and
  hash. F1/F2 remain open; F3 is wording residue only.

Reviewer-owned completion ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1) | #763 ruling; MATERIALIZATION 8.3; FASTCONNECT 6.1; test_aecp.cpp:250; CI_IMAGE.md:767; inventory-check.log | R658-1, applied; no clean coverage | 07c6c72fce79e705bcf28a70071497d0ce7040e4 |
| RTL | CLEAN | exact four-file diff; aecp_arms.py:13; aecp_mutants.py:501; aecp_nvm.c:53; nvm_store.c:292; KL_aecp_nvm_writer.sv:397 | R658-1 | 07c6c72fce79e705bcf28a70071497d0ce7040e4 |
| Robustness | CLEAN | test_aecp.cpp:194/250/288/322; aecp_state.c:71; nvm_fmodel.c:43; clean/planted logs; geometry probes | R658-1 | 07c6c72fce79e705bcf28a70071497d0ce7040e4 |
| Tests | UNCLEAN (F1, F2) | clean-app-if1/2.log; campaign-owner/store.log; owner/store-named.log; public-gate-audit.json; inventory-check.log | R658-1, applied; no clean coverage | 07c6c72fce79e705bcf28a70071497d0ce7040e4 |
| Docs | UNCLEAN (F1, F2) | AECP README; PR/issue evidence; CI_IMAGE.md:767; inventory-provenance.json; receipt-index-audit.json; public-gate-audit.json | R658-1, applied; no clean coverage | 07c6c72fce79e705bcf28a70071497d0ce7040e4 |

Reproduction and receipts

All builds and plants reside under this packet's `scratch/`. Commands ran as
foreground processes; independent checks ran concurrently with at most three
four-job compilation processes. No source fixes, commits, pushes, GitHub writes,
shared installs, hardware, containers or full RTL/builder banks were performed.
The scoped RTL compiler was not used.

Portable scripts accept a checkout and packet path:

```sh
rtk proxy python3 focused.py CHECKOUT PACKET clean
rtk proxy python3 focused.py CHECKOUT PACKET owner
rtk proxy python3 focused.py CHECKOUT PACKET store
rtk proxy python3 focused.py CHECKOUT PACKET shapes
rtk proxy python3 shape_isolation.py CHECKOUT PACKET
rtk proxy python3 audit_public.py PACKET
rtk proxy python3 audit_artifacts.py CHECKOUT PACKET
rtk proxy python3 verify_checkout.py CHECKOUT PACKET
```

The first three modes exit 0, including expected mutant failures. Exploratory
`shapes` exits 1, explained below. `.rc` files record actual test results,
including expected exit 1 under plants. `audit_public.py PACKET` verifies public
receipt hashes; its inputs are GitHub's contents manifest and recursive tree
at evidence revision `c262f8de6c498f412312ad3abd96437c9d25e594`.

The unchanged `sw/firmware/ctrl/test/aecp_mutants.py` CLI was also run with
`--shard 58 78` and `--shard 59 78`, each with separate `--output` under
`PACKET/scratch/`. Both exit 0, retaining the complete table's census controls.
The CLI has no jobs option and uses four compilation jobs.

Local docs scrub, feature-status, document-style, TOC, added-em-dash and firmware
shard gates pass. Markdown dependencies were installed only in `scratch/venv/`.
The inventory check used `CI_IMAGE_SHFMT` pointing to the authenticated parser
under `scratch/`; its substantive refusal is recorded after satisfying setup.

The [published packet](https://github.com/kebag-logic/milan-fpga/tree/c262f8de6c498f412312ad3abd96437c9d25e594/review-evidence/763-r1)
provides the author's firmware PASS/extract, store suites (435 tests), coverage
ratchet, RV32/tally/shard controls, both boundary halves and docs results. I
inspected these and independently reproduced the focused checks above. The
full firmware log is not published; its hash and filtered extract are. I did
not inspect that unpublished full log or rerun the complete firmware bank.
Published store-gap logs report all six store binaries passing under the
payload-erasure plant.

Limits and pending manager duties

* Persistence execution is the shipping 1x1 fixture, not every configuration.
  `aecp_arms.py:117` selects that shape for application runs; the five-shape loop
  runs image tests. Exploratory `Nvm.*` runs fail on the other four shapes: the
  three alternate board configurations lack an output-map pool, and the 8x8
  shape has zero-capacity/default input maps. Isolating the new test produces
  explicit geometry assertions, not successful persistence evidence. The
  unchanged older framing test also crashes when forced onto the zero-capacity
  8x8 fixture. These runs do not extend the narrowed acceptance or establish
  a regression in its normal gate. Raw results are retained. No all-shape
  persistence claim is banked.
* Source-head execution evidence belongs to the author. No manager source bank
  ran at this head. The manager must build and validate the current-dev merge
  candidate, including builder and native banks, and link receipts at the merge
  turn. The supplied live-dev/base value is not a future merge guarantee.
* `hosted-checks.json` is one exact-head observation, not hosted acceptance.
  The AECP-mutant context succeeded; firmware, docs and exhaustive jobs were
  still running or queued. Physical gPTP was skipped. Required aggregate
  completion and local replication acceptance remain the manager's duties.
* Physical calibration: NOT RUN. Field skips and simulation are not hardware
  proof. #637 retains the shipping writer/restore and cold-cycle acceptance.
  This review claims neither board repair nor Milan release closure.
* At reconstruction and again after this verdict/ledger were written, the PR
  contained two review-start comments, no formal reviews and no inline findings
  (`public-review-state.json`). There were no prior public findings to resolve
  or retain. Start notices are not positive verdicts.
* Resolve F1/F2; carry F3 to the residue checklist; obtain corrected-head review
  coverage and the other independent verdict; finish candidate/hosted evidence;
  then perform only an authorized merge and containment. This report does not
  authorize merging.

`checkout-integrity.json` verifies all 1,422 parent tracked blobs' raw bytes and
modes, the index against HEAD, and all five required submodules' gitlinks,
tracked bytes, modes and indexes. The unused external gitlink is unchanged and
uninitialized. The checkout is clean. `MANIFEST.sha256` lists publishable
receipts and scripts; `scratch/` is excluded.

R658-1 FINISHED
