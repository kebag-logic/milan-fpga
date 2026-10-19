[R658] POSITIVE - exact head 07c6c72fce79e705bcf28a70071497d0ce7040e4

External independent review R658-2, issue #763 / PR #766.
Base: `e9cbb676d7fdd6539aa408e5dfe38870a4ae1a5f`.
Tree: `c70d7afe29d34724474bfc05053fe3cb43801026`.

All five lenses are CLEAN for the narrowed PR scope. No R658 MINOR, MAJOR or BLOCKER remains open within that scope. This head is identical to R658-1: this round reviews the public scope decision and corrected evidence, retaining unaffected source coverage. One new wording residue appears below. This is a review verdict, not merge authorization or a claim that the inventory gate now passes.

Reconstruction followed AGENTS.md, CONTRIBUTING.md, docs/README.md, the frozen issue and public decisions, saved-state authorities, the exact four-file diff and two-commit history, then published receipts. Earlier R658 findings were read only after the independent diff pass. No private author material, management checkout or another reviewer's report informed this verdict and ledger.

**Disposition of every R658-1 finding**

* **R658-1-F1, previously MINOR, Conformance/Tests/Docs: discharged from this PR by explicit scope ruling, not repaired in source.** The [manager's option (c)](https://github.com/kebag-logic/milan-fpga/pull/766#issuecomment-6259476788) assigns the complete inventory refresh and lock re-record to #737. The [tracking comment](https://github.com/kebag-logic/milan-fpga/issues/737#issuecomment-6259477028) names exactly `sw/firmware/ctrl/test/aecp_arms.py`, `sw/firmware/ctrl/test/aecp_mutants.py` from #766, `scripts/check_doc_style.py` from #753, and `scripts/measure_test_evidence_readers.py` from #754. It requires one generated refresh on dev containing #766, two byte-identical cold builds for the lock, and inclusion of the inventory check in the gate set. Independent SHA-256 comparison finds exactly those four stale rows; only the two AECP paths intersect this PR's changed inventory inputs. The four-file diff adds no installation request and changes no image recipe, lock, production source, workflow or other inventory input. `ci/image/build.py:144` includes the inventory in recipe inputs. Published before/after receipts show recipe `712f7b38...` becoming `1e5e36f7...`, inventory check 2 becoming 0, and lock check 0 becoming 2. The mismatch remains real and tracked; the explicit ruling removes it from this PR's acceptance. Moving an ordinary unresolved code defect would not establish clean coverage. `exec-audit-receipt.json` remains a historical observation, as ruled.
* **R658-1-F2, previously MINOR, Tests/Docs: resolved.** Every top-level outcome in the published gate extract was independently counted against campaign source names: 520 control-source + 78 AECP + 278 SRP = **876 source-mutant executions**, plus **2 dependency-pin refusal controls** and **61 normal arm outcomes** = **939 top-level `[ok]` lines**. The PR body, corrected `author-r2/receipts/round-b/gates/test_ctrl_firmware/summary.txt`, both classification receipts, and [Round 2 STOP correction](https://github.com/kebag-logic/milan-fpga/issues/763#issuecomment-6259463748) agree. The original historical claim is explicitly superseded. Both new mutants remain caught, and the gate ends `test_ctrl_firmware: PASS`. The refreshed receipt index and publication hashes verify. No bank rerun is needed for this evidence-only correction.
* **R658-1-F3, previously RESIDUE, Docs: resolved.** The live PR body says “two commits at published head `07c6c72f`” and names both assigned reviewers. Neither old placeholder remains. Assignments do not imply approval. `Closes #763` is present, as directed.

**R658-2-R1 - RESIDUE - Docs**

Artifact: [PR #766 body](https://github.com/kebag-logic/milan-fpga/pull/766), Status, Linked Issue / roles, Known limitations, and Round 2 decision-request prose; captured in `receipts/pr766.json`.

Authority/evidence: option (c) is settled, but the body still opens “BLOCKED on a decision,” says “Until the Round 2 decision lands,” calls the refresh “held for the Round 2 decision,” and ends “Decision needed on F1, one of”. The count and R658-1-F3 replacements are already correct.

Impact: stale narrative about a decision already recorded publicly. Correcting it changes no inventory measurement, source, acceptance ruling or review verdict. This is wording residue under the supplied rule.

Required outcome / exact fix: replace the opening with “In review at published head `07c6c72f`; the inventory refresh and lock re-record are assigned to #737 by the option (c) ruling.” Replace the pending-decision and “only relates” sentences with “Closes #763 on the narrowed firmware-test scope; #637 retains board acceptance.” Describe the current inventory mismatch as tracked under #737. Label the STOP and options as historical, superseded by the linked ruling. Preserve the failing inventory result and pending merge checks; do not turn an unchecked verification item into a claimed pass.

Verification: compare the edited body with comments 6259476788 and 6259477028, retain the corrected count, and confirm no test or gate result was rewritten. The manager carries this fix to the residue checklist. No other new finding or suggestion arose.

**Independent lens results**

[R658] PASS Conformance - `test_aecp.cpp:250`, FASTCONNECT section 6.1, MATERIALIZATION section 8.3/V3g, issue #763 ruling 6257040042 and PR ruling 6259476788 - framed UNUSED payloads represent valid empty sets; erasure includes the header. The test exercises REMOVE_AUDIO_MAPPINGS in both directions, commits through the store, resets defaults, boots retained media and compares the non-default opposite set. The record format and shipping code remain unchanged. #763 closes on the firmware test gap; #637 owns shipping writer/restore and cold-cycle acceptance. F1's scope disposition was checked against its exact tracked cause.

[R658] PASS RTL - `receipts/source.diff`, `aecp_arms.py:20`, `aecp_mutants.py:501`, `aecp_nvm.c:53` and `ctrl_nvm/nvm_store.c:292` - no production RTL, clock/reset, CDC, ABI, layout or gitlink change. The sibling-store selection resolves to the same store in the checkout and the isolated planted copy in the campaign. Same-head R658-1 coverage remains applicable; the evidence and scope delta changes none of these dependencies.

[R658] PASS Robustness - `test_aecp.cpp:250`, `ctrl_nvm/host/nvm_fmodel.c:43`, published `round-b/new-mutants/*.log` and `clean-arm/app-if1-Nvm.log` / `app-if2-Nvm.log` - both directional iterations start blank, assert defaults before restoration, then distinguish empty from non-default saved state. Power-on clears device state while preserving flash bytes. Both plants reach the intended assertion with type 14 and 15 traces and completed failing verdicts. The clean NVM arms pass eight tests at each interface count. No source delta invalidates prior malformed-input, refusal and reset coverage.

[R658] PASS Tests - `receipts/delta-audit.json`, published `round-b/gates/test_ctrl_firmware/extract.log`, corrected summary, `round-2/count/*.json`, new-mutant logs/results - the numerical correction is independently reproduced with no unaccounted outcome. Focused negative receipts fail on the named observable, not just compilation. Unchanged store-plant gap evidence and R658-1 execution retain their force. Inventory scope is explicit rather than represented as a passing test. No campaign was rerun in this evidence-only round.

[R658] PASS Docs - `sw/firmware/ctrl/aecp/README.md:100` and `:133`, `receipts/source.diff`, PR body, #763 correction, #737 tracking and corrected receipt index - documentation describes framed-empty behavior and isolated store mutation. Added source comments state behavior/reason with #763; the test cites the Milan clauses. No new bench label, lane name, reviewer identity, review-round or issue-comment ID appears in source comments. F2/F3 are corrected; remaining decision-request prose is R658-2-R1 only.

Reviewer-owned ledger:

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #763 scope; FASTCONNECT 6.1; MATERIALIZATION 8.3; test_aecp.cpp:250; option (c); #737; delta-audit.json | R658-2 | 07c6c72fce79e705bcf28a70071497d0ce7040e4 |
| RTL | CLEAN | source.diff; aecp_arms.py:20; aecp_mutants.py:501; aecp_nvm.c:53; nvm_store.c:292 | R658-1 retained; R658-2 dependency check | 07c6c72fce79e705bcf28a70071497d0ce7040e4 |
| Robustness | CLEAN | test_aecp.cpp:250; nvm_fmodel.c:43; clean-arm and new-mutant logs | R658-1 retained; R658-2 evidence spot-check | 07c6c72fce79e705bcf28a70071497d0ce7040e4 |
| Tests | CLEAN | delta-audit.json; gate extract/summary; count receipts; new-mutant logs/results; #737 ruling | R658-2 | 07c6c72fce79e705bcf28a70071497d0ce7040e4 |
| Docs | CLEAN | AECP README:100/133; source.diff; PR body; issue correction; #737; receipt index | R658-2 | 07c6c72fce79e705bcf28a70071497d0ce7040e4 |

**Prior public findings reconciliation after writing this verdict and ledger**

Only after the independent verdict and ledger above were written, the other prior public review's findings were read at [6259255660](https://github.com/kebag-logic/milan-fpga/pull/766#issuecomment-6259255660). R657-1-F1 (MINOR, Conformance/Tests) is discharged for this PR by its expressly permitted public-assignment alternative and the same option (c)/#737 evidence above. R657-1-R1 (RESIDUE, Docs) is resolved by the corrected published-head status wording. R657-1-S1 (SUGGESTION, Docs, README:105) remains optional: explicitly repeat that the owner is opt-in and #637 owns shipping maps. R657-1-S2 (SUGGESTION, Tests, aecp_mutants.py:358) remains optional: add a writer-side all-UNUSED-skipping mutant. Neither suggestion leaves a lens unclean; neither was silently counted as implemented. The earlier review's “939 controls caught” narrative is not used as a measurement here; the corrected source receipts and independent count above supersede that aggregate. Formal reviews and inline review comments were empty at this round's final read. No further public finding remains unaccounted for.

**Evidence, reproducibility and limits**

The publication at `687310c882ef2f6275650ac267018e682e5bf7b2` supplies author receipts. Verified 52 original and 105 corrected receipt files against `MANIFEST.json`; all 104 non-index corrected receipt entries match membership, size and hash. These are publication-byte checks. The evidence commit verification endpoint reports `unsigned`, with no signature or payload (`receipts/evidence-signature.json`); signer authentication is not claimed. The full 333,913-byte gate log is unpublished: its SHA-256 is recorded, and its top-level outcome extract is available. This round audits that extract, not the unpublished full log. The published full-log/extract classifications agree.

Portable read-only reproduction, with the evidence commit fetched into CHECKOUT:

```sh
rtk proxy python3 audit_delta.py CHECKOUT PACKET
rtk proxy python3 verify_checkout.py CHECKOUT PACKET
```

Both commands exited 0. JSON, logs and exit receipts are included. No source mutation or build was needed. The integrity audit verifies 1,422 parent blobs and 1,072 required submodule blobs byte-for-byte, including file kinds, executable modes, indexes and registered gitlinks. All five required submodules remain pinned; the unused external gitlink remains unchanged and uninitialized. The checkout is clean. Only manifest-listed files and REPORT.md are publishable; scratch is excluded.

Prior source coverage is limited to the normal 1x1 TDM8 application fixture. Five-shape image/store receipts do not prove this new AECP persistence test on all five shapes. R658-1's out-of-fixture geometry limits remain limits. Physical calibration NOT RUN; simulation and field skips are not hardware proof. #637 retains cold-cycle acceptance.

No manager source bank ran at this head. Source execution evidence belongs to the author. The manager still owns the current-dev merge candidate, builder/native banks and linked receipts, hosted contexts and local replication acceptance, independent-review completion, authorized merge and post-merge containment. This round does not inspect hosted completion and claims no execution from skipped contexts. The supplied source base and live-dev value both equal `e9cbb676d7fdd6539aa408e5dfe38870a4ae1a5f`; validate the actual merge-turn state. The inventory refresh and two-cold-build lock re-record remain #737 duties. Carry R658-2-R1 as wording residue.

R658-2 FINISHED
