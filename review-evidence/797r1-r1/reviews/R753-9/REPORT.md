[R753] POSITIVE - exact head b74ef924ca8558efdd42b72d99c3beb39eeaf24c

Round R753-9 is a cleared-context composition acceptance review of PR #825 (issue #797, the generated register reference). The merge-train candidate is `b74ef924ca8558efdd42b72d99c3beb39eeaf24c`, tree `f2003f0f80a8591333c786fd904a4605db6c21d5`. Its parents are live dev `ac0a01e354d20f5ecac1569c4e7afb3abcbf6f36` and PR head `06c89f1d48c73ec1977791f2a2c4f99579ae4853`. The two source reviews of the PR head are R753-8 (PR comment 6721151633) and R754-8 (PR comment 6721199245), both POSITIVE at `06c89f1d`. This round judges only what composing that head with dev adds.

**Why POSITIVE:** the composition is a clean, mechanical merge. `git merge-tree --write-tree ac0a01e3 06c89f1d` reproduces the candidate tree byte for byte, so the candidate adds no hand edits. Only one file is changed on both sides: `docs/DOCUMENTATION_AUDIT.md`. That file is generated, and the generator reports it fresh on the candidate. All other dev-side changes come from PR #852 (protocol-processor pin `92100657` -> `044cb25f`, area records, the crflic bench, and docs). None of them reaches an input of this PR's generator, gates or tests. Every gate that reads a shared or interacting artifact passes on the candidate. The signed local-CI manifest verifies and names this candidate and head, and all 50 coverage entries are ok. No BLOCKER, MAJOR, MINOR or RESIDUE is raised. One retained SUGGESTION is restated below, together with what this composition shows about it.

## Composition: what both sides change

Merge base `0a75aa774b89ac89351700f63dd8cbb89694af6c` (receipt `receipts/overlap.txt`).

- **Dev side (PR #852, 20 files):** `CHANGELOG.md`, `docs/DOCUMENTATION_AUDIT.md`, `docs/design/AREA_BUDGET.md`, `docs/design/MARK_II_AREA_PLAN.md`, the `submodule_boundaries` diagram (drawio/svg/png plus `PNG_MANIFEST.json`), `docs/findings/234_PP_SHADOW_AREA_BASELINE.md`, `docs/findings/README.md`, `docs/integration/INTEGRATION_GUIDE.md`, `docs/reference/SUBMODULES.md`, `docs/testing/TESTING.md`, the `protocol-processor` gitlink, `syn/ooc/pp_resource_baseline.json`, `syn/yosys/rom_digests.tsv`, and `tb/verilator/milan_dp/{Makefile,README.md,crflic_mutants.py,sim_crf_licence.cpp}`.
- **PR side (267 files):** the register generator and its modules under `scripts/register_*.py` and `scripts/gen_register_reference.py`, `scripts/register_descriptions.json`, `scripts/register_map_soc.json`, `docs/reference/REGISTER_MAP.md`, `REGISTER_MAP_CLASSES.md`, `docs/diagrams/regmap/**`, `scripts/docs_inventory.json`, `scripts/ci_events.py`, `scripts/check_doc_style.py`, `sw/builder/test_builder.py`, `docs/testing/MILAN_V12_AUDIT_2026-08-16.md`, and `docs/DOCUMENTATION_AUDIT.md`.
- **Textual overlap: `docs/DOCUMENTATION_AUDIT.md` only.** Dev changes one cell: the INTEGRATION_GUIDE row gains `802.1Q`. The PR changes the counts and removes the 15 fixed D0 rows. The candidate carries both changes (`docs/DOCUMENTATION_AUDIT.md:277` keeps `802.1Q`, and the `:313` REGISTER_MAP row keeps only D0-057). `docs_inventory.py --check` reports `docs/DOCUMENTATION_AUDIT.md is fresh` on the candidate (533 lines), so the merged bytes match what the generator writes from the merged inventory and pages.

## Semantic interactions examined

| Interaction | What the composition could break | Result on the candidate | Evidence |
|---|---|---|---|
| Generated documentation audit (`docs_inventory.py` + `docs_inventory.json`) | Dev's page edits change derived columns, and the PR removes inventory entries | fresh | `receipts/docs_inventory_check.log` rc 0; `docs_inventory_selftest` rc 0 |
| Register reference freshness (RTL fingerprint, SoC extract, diagrams) | The PP pin bump or dev RTL changes would make `REGISTER_MAP.md` or `rtl_fingerprint.txt` stale | fresh: 203 registers, 34 modules, 240 files; selftest 61/61 | `receipts/gen_register_reference_check.log`, `..._selftest.log` rc 0. The fingerprint covers only parent files (`hdl/common/csr/milan_csr.sv`, two generated `.svh`, `hdl/milan/milan_datapath.sv`), and dev changes no `hdl/`, `sw/`, `configs/`, `avdecc/` or `scripts/` file |
| SoC extract `scripts/register_map_soc.json` (not gated without an export; see S1) | The PP pin could change the export's top-level parameters, `csr.csv` or the `aem_desc.json` windows | not affected | In the PP diff `9210065..044cb25`, the only RTL file is `hdl/srp/KL_srp_encoder.sv`. No added or removed `input`, `output`, `parameter` or `module` line exists anywhere in it. Dev's CHANGELOG entry states "No top-level port, parameter or register changes." The manager-builder bank ran at this candidate (48 commands, all exit 0) |
| `sw/builder/test_builder.py::test_lwsrp_reset_words_match_rtl` (PR changes the regex to the new summary-row layout) | A dev page could reintroduce the old row shape | passes | `receipts/test_lwsrp_reset_words.log` rc 0 (gate 18a, 6 registers) |
| Cross-page links and anchors into the rewritten `REGISTER_MAP.md` | Dev's new prose in SUBMODULES, INTEGRATION_GUIDE, AREA_BUDGET or findings links to an anchor the rewrite removed | none broken: dev's added lines contain no `REGISTER_MAP` reference; 598 cross-page fragment links reproduced | `receipts/gen_toc_anchors.log`, `gen_toc_check` rc 0, `gen_toc_selftest` rc 0, `docs_check` rc 0 |
| CI event inventory (`ci_events.py`, which the PR changes to count both docs-check steps) | Dev workflow changes would shift step counts | dev changes no workflow; all four workflow sha256 are identical at head and candidate | `ci_events --check` OK (2215 items), `--selftest` rc 0; manifest `definitions.candidate == definitions.head` |
| Style gates (`check_doc_style.py`, which the PR changes) over dev's new pages | The PR's new style rule rejects a dev page | passes | `receipts/doc_style.log` rc 0, selftest rc 0 |
| Em-dash on added lines | Lines added by either side | 0 findings over 5779 added lines in 8 pages against dev; passes against the source head | `receipts/em_dash_vs_dev.log`, `em_dash_vs_source.log` rc 0 |
| Docs gate without git metadata | Composition under a filesystem walk | 0 findings across 215 md files | `receipts/nogit_docs_check.log` rc 0 (tree from `git archive HEAD`) |
| Other docs gates (paths, feature status, submodule docs and boundaries diagram, PNG manifest, DOC_MAP, memory map, CI gate workflows, evidence pins) | Dev's diagram and SUBMODULES changes against the PR's inventory | all rc 0 | `receipts/{doc_paths,feature_status,submodule_docs,submodule_boundaries_check,diagram_pngs,doc_map_check,memory_map_check,ci_gate_workflows,ci_evidence_pins}.log` |

Comment rule: the merge commit adds no bytes beyond the two parents (merge-tree identity), so the composition adds no source comment and no lane, round or reviewer label.

## Signed local CI (owner 2026-10-14)

Receipt: `receipts/signed_manifest_verify.txt`; fetched files under `evidence/local-ci/` (from `review-evidence/797r1-r1/local-ci/06c89f1d` at `8134bb0b`).

1. `allowed_signers` holds one key, principal `milan-local-ci`, namespace `milan-local-ci`, fingerprint `SHA256:dRI12tvJkhueTEGqsRutn2L+dT/5qqOCsCVzBU5CI7k`. This matches the required fingerprint.
2. `ssh-keygen -Y verify -f allowed_signers -I milan-local-ci -n milan-local-ci -s manifest.json.sig < manifest.json` printed `Good "milan-local-ci" signature`, rc 0. `manifest.json` sha256 is `637dfa5a87f6a40a08a59c425b8b0054aebd19fffbfbbad744c2ab4fcad786a3`, as stated.
3. The subject names candidate `b74ef924…`, candidate parent `ac0a01e3…`, candidate tree `f2003f0f…`, head `06c89f1d…`, head tree `40c99b22…` (checked against `git rev-parse 06c89f1d^{tree}`) and PR 825. `result` is `success`. All 50 coverage entries are `ok: true`: 49 are mapped to act and 1 is `not-run` (`rtl/physical-gptp`, which runs only on the schedule and on manual dispatch). act replayed head `06c89f1d` with exit 0: 70 jobs succeeded and 1 was skipped, the same nightly physical-gPTP job. The banks ran on the candidate: `manager-builder` 48/48 exit 0 and `full-native` 5/5 exit 0. I did not rerun any of these; no claim needed falsifying.

## Findings

### S1 - SUGGESTION - Robustness, Tests, Docs - `scripts/register_map_soc.json`; `scripts/gen_register_reference.py:20-24,43-44` - the SoC extract's staleness is still checked only when a builder export is supplied

- **Status:** retained from R753-7 S1 / R754-7 S1 (optional; the PR body says it is not taken).
- **This composition:** this is the case the suggestion describes. A predecessor (#852) moved a submodule pin, and `--check` without `--soc-from` cannot tell whether the extract is still true. I closed the question by inspection, not by a gate: the PP delta changes no top-level port or parameter, and the parent's export inputs are untouched.
- **Impact:** none at this candidate. A later pin that does change a window or parameter would pass every hosted gate.
- **Optional outcome:** a cheap guard, for example a recorded digest of the export inputs that `--check` can compare without running a build.

No other new finding. **Wording residue:** none in the composition delta.

## Prior public findings at this head

| Prior finding | Status at `b74ef924` | Evidence |
|---|---|---|
| R753-7 F1 (MINOR; Conformance, Docs): fixed D0 rows still listed as open | Resolved (by R753-8 and R754-8 at `06c89f1d`); it holds after composition | `docs/DOCUMENTATION_AUDIT.md:313` keeps only D0-057; `docs_inventory --check` fresh |
| R754-7 S3 (SUGGESTION): D0 owner closes the fixed rows | Resolved; it holds | same |
| R753-7 S1 / R754-7 S1 (SUGGESTION): extract staleness not gated | Retained, optional (S1 above) | see S1 |
| R753-7 S2 / R754-7 S2 (SUGGESTION): MAC_ADDR hold only in the notes | Retained, optional | dev side changes neither `REGISTER_MAP.md` nor `register_descriptions.json` |
| R753-7 S3 (SUGGESTION): `verified_pages` keeps "D0" | Retained, optional | `scripts/docs_inventory.json` not changed by dev |
| R753-6 S1, S2; R754-6 S1, S2; R753-5 S1; R754-4 S1, S2 (SUGGESTION) | Retained, optional | files not changed by dev |
| R753-8 RES1 (RESIDUE): `verify_docs_yml.md:82` names `gate_41.log` but `.log.tail` is published | Retained on the residue checklist (evidence-page wording, outside the tree) | not part of the candidate tree |
| R753-7 RES1 / R754-7 RES1, R754-7 RES2, R753-3 RES2 and RES3, R754-3 R1 (RESIDUE) | Retained on the residue checklist, as R754-8 carried them | not changed by the composition |
| R753-8 S4 (SUGGESTION): the inventory removal rule depends on review alone | Retained, optional | `scripts/docs_inventory.py` not changed by either side since the source head |

No prior BLOCKER, MAJOR or MINOR is open or reopened.

## Per-lens results

```text
[R753] PASS Conformance - docs/DOCUMENTATION_AUDIT.md:277,313; scripts/register_map_soc.json; protocol-processor 9210065..044cb25 hdl/srp/KL_srp_encoder.sv - the composition touches this lens only through the generated audit and the extract's inputs; the audit is fresh with both sides' edits, the 15 fixed rows stay removed, and the PP pin changes no top-level port, parameter or register the extract records; issue #797 acceptance items still hold on the candidate (audit lists every page with a status, all docs gates green)
[R753] PASS RTL - git diff --name-only 0a75aa77..ac0a01e3 (no hdl/ file); docs/diagrams/regmap/rtl_fingerprint.txt - the PR changes no RTL; the only RTL delta in the composition is the PP encoder internals behind an unchanged port list, which the CSR fingerprint does not cover and the register generator does not read; gen_register_reference --check fresh (203 registers); the source RTL lens is covered by R753-8 and R754-8 at 06c89f1d
[R753] PASS Robustness - receipts/nogit_docs_check.log; receipts/gen_register_reference_selftest.log (61/61); S1 analysis - generator refusal and selftest controls run on the composed inputs; no-git filesystem walk is clean; the extract-staleness path is retained as optional S1 and is not exercised by this composition
[R753] PASS Tests - sw/builder/test_builder.py test_lwsrp_reset_words_match_rtl (receipts/test_lwsrp_reset_words.log); ci_events --check/--selftest; docs_inventory/gen_toc/check_doc_style selftests; signed manifest banks at b74ef924 - the PR's changed test and selftest counts hold against dev's pages and unchanged workflows; manager-builder 48/48 and full-native 5/5 at this candidate
[R753] PASS Docs - docs/DOCUMENTATION_AUDIT.md (merged, fresh); gen_toc --verify-anchors (598 links); docs_check; check_em_dash --base ac0a01e3 and --base 06c89f1d; check_doc_style; check_doc_paths; submodule_boundaries.gen.py --check; check_diagram_pngs - the one overlapping page composes to the generator's bytes; dev's new prose has no link into the rewritten register page; all docs gates green
```

## Reviewer-owned ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | merged `docs/DOCUMENTATION_AUDIT.md`, `scripts/docs_inventory.json`, `scripts/register_map_soc.json` inputs vs the PP pin delta; source content covered by R753-8 and R754-8 | R753-9 (composition); R753-8 and R754-8 (source) | `b74ef924ca8558efdd42b72d99c3beb39eeaf24c`; source at `06c89f1d48c73ec1977791f2a2c4f99579ae4853` |
| RTL | CLEAN | composition has no parent RTL delta; PP encoder port list unchanged; CSR fingerprint fresh. Source RTL scope covered by R753-8 and R754-8 | R753-9 (composition); R753-8 and R754-8 (source) | `b74ef924…`; source `06c89f1d…` |
| Robustness | CLEAN (S1 optional) | generator selftest 61/61; no-git docs walk; extract-staleness analysis | R753-9 (composition); R753-8 and R754-8 (source) | `b74ef924…`; source `06c89f1d…` |
| Tests | CLEAN | `test_lwsrp_reset_words_match_rtl`; `ci_events` check/selftest; inventory, TOC and style selftests; signed banks at the candidate | R753-9 (composition); R753-8 and R754-8 (source) | `b74ef924…`; source `06c89f1d…` |
| Docs | CLEAN | merged audit, anchors, links, em-dash against both parents, style, paths, diagrams | R753-9 (composition); R753-8 and R754-8 (source) | `b74ef924…`; source `06c89f1d…` |

## Limits

- I ran no builder export, so `gen_register_reference.py --check --soc-from` was not run on this candidate. The extract's currency rests on inspecting the PP diff and the parent export inputs, plus the manager-builder bank (whose argv is recorded only as hashes, so I cannot name which commands it ran).
- I ran no full simulation, Yosys or builder bank (not allowed). Simulation and build evidence at the candidate is the signed manifest's banks, and act evidence is a replay of the source head, not of the candidate. Both workflow definition sets are identical.
- I inspected no hosted run at the candidate. Physical calibration was NOT RUN; the nightly physical-gPTP job is skipped and is not hardware evidence.
- The gates that need the pinned Markdown renderer and wavedrom ran from a private virtual environment in scratch, installed from `tools/markdown/requirements.txt` (with hashes) and `wavedrom==2.0.3.post3`, as the docs workflow pins them. The interpreter was the host Python 3.14.9.

## Pending manager duties

- Hosted and act acceptance at the merge turn; the merge itself needs explicit maintainer authorization.
- Post-merge containment, and closing issue #797's register-reference area as the issue's lane plan requires.
- Carry the retained RESIDUE items listed above to the residue checklist.

## Integrity

After the gates, the worktree and index equal HEAD (`git status --porcelain` is empty). The gitlinks are `protocol-processor 044cb25f`, `gptp-processor 1616fc8f`, `third_party/lwSRP 08ee86e8`, `third_party/tsn-c-stack 70936b77` and `third_party/verilog-axis 48ff7a7e`, and their checkouts match. `external` is not initialized, as delivered (`receipts/integrity.txt`). I applied no probe edits.

Reproduce: `scripts/composition_check.sh <clone-at-b74ef924> <python-with-pinned-docs-deps> <out-dir>`.

R753-9 FINISHED
