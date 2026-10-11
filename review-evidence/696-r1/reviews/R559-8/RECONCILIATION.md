# Prior public findings at aa980479

This ledger is part of R559-8. It applies to `aa980479aafd1d72c72015707fa6618b5aa47cb1` only. The independent diff pass and an initial verdict/ledger were written before reading prior reports. Original findings, their public URLs, authorities and verification requests are preserved in [prior-finding-extracts.md](prior-finding-extracts.md). Original lens assignments are retained; grouped duplicates use the union of their lenses.

## Resolved findings

| IDs | Original severity; all lenses | Evidence and required outcome at this head |
|---|---|---|
| R558-9-F1 | MINOR; Docs | `docs/design/MARK_II_AREA_PLAN.md:695,696,947` now identifies #645/#647's historical record and #696's replacement. The exact requested sentences are present. `composition-wording.diff` contains these three replacements. `record-vs-lane-routes.log` shows historical base equality and both lanes passing against both records. The conflicting identity of the current gate record is resolved. |
| R558-9-R1 | RESIDUE; Docs | The exact replacements at plan `:706,968` name M2 and M6 as the lanes that do not re-record acceptance. |
| R558-7-F1 | MINOR; Tests | `tb/verilator/maap/sim_main.cpp:433-440` checks the echoed requested start for a PROBE starting below this station. Current campaign `m2_echo_overlap_start` fails that named assertion. The requested-start/overlap-start blind spot is closed. |
| R559-6-F1 | MINOR; Tests, Conformance | Public scope decision 6102832618 explicitly narrows the first-draw criterion to seed pairs a power of two apart and blocks 1..8. `sim_main.cpp:1089-1138,1189-1275` names sampled pairs accurately and establishes the stated property from the RTL maps. No all-arbitrary-high-half-pairs promise remains. |
| R559-6-F2 | MINOR; Tests, Docs | `sim_main.cpp:1189-1275` checks all offset words and carry runs after deriving the maps; `MAAP_FABRIC.md:110-117,257-273` states the scope. Current campaign catches both row mutations, nonlinearity and rank dependence at their named checks. The linearity sampling limit remains disclosed. |
| R558-6-F1 | MINOR; Conformance, RTL, Robustness, Tests | `KL_maap.sv:146-203,337-339` uses the stepped first-draw folds. Unit and real-datapath first-offset plants fail named assertions in `maap-suite.log`. Raw low-seed-bit first allocation is no longer accepted. |
| R558-5-F1 | MINOR; Docs | `AREA_BUDGET.md:379` and plan `:655-656` date the 50,267 baseline and explicitly name #696's 50,013 replacement/current comparison anchor. |
| R558-3-F1 = R559-3-F1 | BLOCKER; Conformance, Robustness, Tests | `tb/verilator/maap/integration.mk:8-24` clears inherited `MAKEFLAGS` for both nested captures and forwards the compilation bound explicitly. Empty-source and nonexistent-source guards remain. These bytes are unchanged from the reviewed source; current integration and all six campaign datapath rows build and grade successfully. The original hosted-shape failure is resolved in the code. This round used Make 4.4.1 and does not substitute for the manager's exact-head hosted acceptance. |
| R558-1-F1 | MINOR; Docs | `MAAP_FABRIC.md:161-173` dates 441/340 at the M3 step, 445/340 at the earlier merge and 490/340 at the first-draw step. Historical published OOC results corroborate the merge figures. No old figure is presented as a measurement of this composed head. |
| R559-1-F1 | MINOR; Tests | `sim_main.cpp:836-872` holds the link down longer than a walk and asserts loss is no event. Current `m5_restart_on_link_loss` is caught at this named check. |
| R559-1-F2 | MINOR; Docs | Plan `:110-147` matches all 66 LUT inventory cells in the three committed records (`record-policy-delta.json`). The `:56` timing-floor wording follows the replacement record. |
| R559-1-F3 | MINOR; Docs, Tests | `sim_main.cpp:59` and its zero-seed test/banner, and `MAAP_FABRIC.md`'s zero-seed paragraph, name `02:00:00:00:00:00` with clock zero. Both zero-seed mutants are caught. |
| R559-1-R1/R2/R3 | RESIDUE; Docs | Area attribution, remaining-deviations wording and `docs/findings/README.md:25`'s #696 record date remain corrected. R559-1-R1 overlaps R558-1-F1; the latter's stronger classification was respected above. |
| R558-7-R1; R559-6-R1 | RESIDUE; Docs | `MAAP_FABRIC.md:116,257-273` and the PR's fold-guarantee paragraph distinguish words from pool-folded blocks and fixed pairs from universal assertions. |
| R558-1-S1 | SUGGESTION; Docs | Plan `:56` gives the binding floor correctly. Applied. |
| R559-1-S2 | SUGGESTION; Tests, Docs | The current PR integration command uses `(cd "$WORK/integration" && ./maap_integration)`. The working-directory advice is applied; the reviewer also ran from the build directory. |
| R558-7-S1 = R559-6-S1 | SUGGESTION; Tests | The unstepped probe-fold defect now fails the every-carry-run first-probe assertion in the default campaign. Applied. |
| Empty-list half of R558-3-S1 = R559-3-S1 | SUGGESTION; Robustness, Tests | `integration.mk:16-18` rejects an empty derived list. Applied; directory half retained below. |

## Retained wording residue

These are prose-only qualifications. Their historical figures remain correct, and fixing them changes no measurement, verdict, executable artifact, clause/conformance claim or privacy rule. They therefore remain RESIDUE under the owner rule, with no unclean lens. The manager should retain them on the residue checklist.

### R558-2-R1 = R559-2-R1 — RESIDUE — Docs

- Artifact/evidence: `docs/design/MARK_II_AREA_PLAN.md:66-67,317,1086`. The explicitly dated baseline section links to the live record file; the planning ledger and M0 row use “current”. Plan `:110-117,656` already distinguishes the actual current record from retained planning figures.
- Authority: dated historical evidence must be attributable; original public findings linked above.
- Impact: ambiguous historical wording only.
- Exact outcome: replace the source sentence with “Source: the three `record` objects of [`pp_resource_baseline.json`](../../syn/ooc/pp_resource_baseline.json) as stored at dev `5603c353`; #696's record has since replaced them (see [Current processor inventory](#current-processor-inventory)).” Replace `:317` with “The [current ledger](#ledger) starts from the 50,267 route figure of the #645/#647 record.” In `:1086`, replace “Adopted processor pin and current three-endpoint record” with “Adopted processor pin and the #645/#647 three-endpoint record”.
- Verification: read the qualifiers with their baseline headings; run the documentation gates. No figure changes.

### R558-5-R1 — RESIDUE — Docs

- Artifact/evidence: `docs/design/AREA_BUDGET.md:370,387`; plan `:668`. M0s-scoped sentences say records/policy remain unchanged, beside #696's re-record. Their subject is M0s.
- Authority: original finding 6097253076; historical lane attribution.
- Impact: a reader may take a lane-scoped sentence as page-wide.
- Exact outcome: replace each of the three sentences with “M0s changes no acceptance record, schema or policy value.”
- Verification: reread those paragraphs and run documentation gates; preserve all figures and gate policy.

### R558-4-R1 = R558-6-R1 — RESIDUE — Docs

- Artifact/evidence: PR #706 body, “Status” and “How to get into the same state”, in `public-evidence/pr-body.json`. The author source is still `32582421`, while the appended “Composition repair” correctly names `a7291311` and `aa980479`.
- Authority: original stale-head finding, reapplied to the distinction between author source evidence and composition. These commands remain valid for reproducing the named author source.
- Impact: source-validation instructions can be mistaken for the latest composed checkout. No source test tally is changed or promoted to composed-head evidence here.
- Exact outcome: start Status with “Author source validation is GREEN locally at `32582421bbf095a7b5a7d4b953c4d737b86fe54b`; the composed review head is `aa980479aafd1d72c72015707fa6618b5aa47cb1` (see Composition repair).” Prefix the reproduction commands with “These commands reproduce the author source-validation state at `32582421`; composition validation is recorded separately.”
- Verification: reread both sections and the composition appendix together; preserve source receipt attribution and commands.

### R559-7-R1 — RESIDUE — Docs

- Artifact/evidence: PR #706 body, last “Known limitations” bullet still says hosted checks/local replica need a pushed head, though this head is published and contexts exist.
- Authority: original finding 6103915710; public hosted snapshot.
- Impact: stale workflow wording only; no assertion of successful execution.
- Exact outcome: “Hosted checks run at the pushed head `aa980479`; hosted and local-replica acceptance belongs to the manager.”
- Verification: compare the sentence with the PR head and manager's acceptance receipts.

## Retained suggestions

All rows below are SUGGESTION, optional, and affect no lens's clean status. Their authority is the original public finding and the indicated executable/documented contract. No optional escaped probe is represented as a new probe run in this round. Source bytes remain unchanged, and the observations remain applicable.

| IDs | All lenses | Artifact and evidence; impact | Optional outcome and verification |
|---|---|---|---|
| R559-1-S1 | Tests | `tb/verilator/maap/mutants.py`, `sim_main.cpp` linearity samples: the trap-state plant targets an explicitly sampled state. It proves detection there, not at every possible nonlinear trap. | Add a distinct out-of-sample trap if stronger sampling is desired; require its named rejection. Structural linearity review remains necessary. |
| R559-1-S3 | RTL, Docs | `KL_maap.sv` first-enable seed path and clock parameter; source timing evidence is for the shipping 50 MHz image. Non-shipping 100 MHz support is not established by that evidence. | If such a build is supported, qualify its timing or document the 50 MHz assumption. No current-head timing run is claimed. |
| R559-1-S4 | Tests | `tb/verilator/maap/mutants.py` enforces #686 categories but lacks an equivalent M1-M8 coverage guard. Existing 63 defects all grade now. | Add a guard against removal of an item's last plant; demonstrate that removing one category fails it. |
| R558-3-S1/R559-3-S1 directory half; R558-4-S1/R559-4-S1 | Robustness, Tests | `integration.mk:19-21` uses `wildcard`, which admits a directory. Elaboration still fails and the campaign cannot count that as a killed defect. Diagnostic quality only. | Reject directories at the guard; verify a directory entry gives the guard's own error. |
| R558-3-S2 = R559-4-S2 | Tests | `mutants.py` does not force the old hosted Make 4.3/unavailable-jobserver shape in a local 4.4.1 run. | Add a meaningful 4.3 regression capture with inherited `w` and unusable jobserver; verify clean source/flag capture. Hosted acceptance stays with the manager. |
| R558-4-S2 | Docs | `integration.mk:8-10`'s explanatory comment omits the unavailable-jobserver condition. Fix is correct. | Name that condition explicitly; verify wording against the original reproduction. |
| R559-5-S1 | Tests, Docs | Area plan/budget record claims have no repository prose-to-record gate. This round's two record audits pass. Future stale composition can still require review to detect. | Add a record-table/anchor comparison gate; show a restored stale anchor fails. |
| R558-6-S1 | Tests | `KL_maap.sv:272,282,480`, `MAAP_FABRIC.md:71-72`: own-count snapshot substitution escapes, while mid-frame reconfiguration is explicitly outside the contract. | Add a snapshot assertion if that implementation detail is to be preserved; make the live-count plant fail it. |
| R558-6-S2 | Docs | `MAAP_FABRIC.md:118-125`, C `maap.c:226-243`, processor `11_maap_engine.md:103,135-147`: fabric holds validity through link loss; other placements withdraw/release. Fabric behavior is the ruled contract. | Add a sentence distinguishing placement behavior; compare all three documents. |
| R558-7-S2 = R559-6-S3 | Tests | `KL_maap.sv:337-339`, `MAAP_FABRIC.md:110`: later Begin! uses the running generator, but a repeated first-fold plant remains ungraded and is disclosed. | Assert appropriate consecutive Release!/Begin! draws at a frozen clock; require the plant's named rejection. |
| R559-6-S2 | Robustness, Tests | `KL_maap.sv:193-198,337-339`: random pool clipping with counts above eight is ungraded; gap predates #696 and is disclosed. | A separate task can drive the clip region with larger blocks and reject fixed-eight clipping. |
| R558-8-S1 | Docs | `docs/testing/TESTING.md:606`: suite index omits #696's real-datapath arm. `mutants.py` visibly runs it. | Add: “Since #696 its default target also builds the real `milan_datapath` CSR-to-MAAP path (`sim_integration.cpp`) and plants its M3, M4 and M5 datapath defects there.” Verify against default make. |
| R559-7-S1 | Tests, Robustness | `KL_maap.sv:464-466,332,203`; `MAAP_FABRIC.md:124,52-55,99`: fresh range after link return, count-zero supplied-bound rejection, and announce draw bit selection are correct but individually ungraded. | Add focused assertions for those intended details; require corresponding plants to fail named checks. None is an unmet acceptance item. |

There is no retained open BLOCKER, MAJOR or MINOR at the reviewed head.
