[R342] NEGATIVE - exact head 1d249e6e18a91c16a2620904483634548b0414a6

# R342-1 independent internal review: processor PR #126 (issues #125 and #122)

- Repository: Mister-M-alt/protocol-processor-control-plane-avb-milan
- Exact head `1d249e6e18a91c16a2620904483634548b0414a6`, tree `13f98a7f404d96a78947f75c1a7ef2f30c8e8b26`. The head has one docs-only commit on base `493e5e4bf58a6146bf9310194d71c72e18610704`.
- Assignment: issue #125 comments 5853861179 and 5853864238. Review start: PR #126 comment 5853959011.
- Verdict: **NEGATIVE**, from one open MINOR (R342-1-F1). The #122 clause disposition is correct. Every packer enforcement statement is true at `493e5e4b`. The integrator guide §6 rules are correct. No code changed. All docs gates pass. The only problem is the §3.1 authority split: it is narrower than the parent contract it cites.

## Reconstruction

1. Contribution rules. There is no AGENTS.md or CONTRIBUTING.md in this repository at the head. I read the author conventions in `docs/README.md` (single-source rules, citation rule "printed = PDF − 7", reading order) and the gates in `.github/workflows/hdl.yml` and `Makefile`.
2. Frozen scope and acceptance. Issue #125 body: acceptance items 1–4, plus the scope clause "does not assign descriptor semantics to 'model lint' without saying who implements which check". Issue #122 body. Manager assignment 5853861179, including the #122 decision rule, and correction 5853864238, which says to extract only the cited pages. Manager PR comment 5853945556 (parent fix tracked as kebag-logic/milan-fpga#584).
3. Authorities. Parent `docs/reference/PP_DESCRIPTOR_OWNERSHIP.md` at `e0920d77162284d8da52ffaf13a973e451e44f90` (sha256 `ad9bb61f…6bf6d8`). The #509 handoff "Processor contract wording" (public, kebag-logic/milan-fpga `6ddca010…` `review-evidence/509-r1/author/HANDOFF.md`). Processor issues #38, #39, #60 and #89 (scope bodies read). Milan v1.2 PDF pages 31, 32, 34 and 35. IEEE 1722.1-2021 pages 50, 81 and 82.
4. Diff `493e5e4b..1d249e6e`: two files, +62/−2 (`receipts/diff-493e5e4b..1d249e6e.patch`). History: one commit, parent `493e5e4b`.
5. Public evidence: kebag-logic/milan-fpga `64e5bbde…` `review-evidence/pp125-r1`. It has six author files plus MANIFEST.json, and all six published hashes match my re-hash. The author's gate outputs are byte-for-byte the same as mine. The tree holds no manager bank receipts; see Limits.
6. Prior public review findings on PR #126: none. At review start the PR had 0 reviews and 0 inline comments, and both PR comments were manager notices. A re-check after this verdict was drafted found only a second review-start notice and the head unchanged. Nothing needs to be resolved or retained.

## Focus items

| # | Question | Result | Evidence |
|---|---|---|---|
| 1 | Clause reading for #122 | **Correct.** Milan v1.2 §5.3.3.8 (printed p. 27, PDF p. 34) says: "Each Stream Port Input of a Configuration shall contain at least one AUDIO_CLUSTER descriptor." The requirement is unconditional per port and applies to outputs as well. IEEE 1722.1-2021 §7.2.13 Table 7-23 (pp. 81–82) defines number_of_clusters (offset 12) separately from number_of_maps (offset 16). Dynamic-mapping entities set only number_of_maps to 0. Neither clause waives the minimum; Milan also governs over IEEE. STOP was the right call. F07.2 keeps `1..*` (`07_memory_maps.md:70–71`), and the parent correction stays with milan-fpga#584 (open). | `receipts/clause-and-authority-check.md` |
| 2 | Packer "enforces / does not enforce" statements at `493e5e4b` | **All true.** The packer refuses: configuration gaps (`gen_desc_image.py:450`), per-type index gaps (`:344`), duplicate keys (`:230`), bad name bindings (`:239–290`), the line-buffer bound (`:325`, 576 accepted / 577 refused), and body/key type and index mismatches in both `fields` and `bytes` form (`:216–222`). It accepts, with the mutated bytes preserved in the image: L10 offset 143, count 9, count/length mismatch both ways, and the L6 list `[1,0]`. The repository contains no model lint: `check-matrix.py` and `lint-diagrams.sh` do not evaluate descriptors. #89's acceptance covers exactly the L10 and L6 packer refusals. | `receipts/packer-claims.tsv` (18/18 OK); mutation receipts |
| 3 | Ownership text vs parent page @e0920d77; the R331-1 S4 question | Construction/refusal, ownership≠implementation, processor generic duties, the loader/conversion/shipping limits, D8, F6 and F7 all match. **The authority sentence does not match.** Parent :36 makes parent shipping checks authoritative for *all generated model content*. §3.1 (:99–103) limits that authority to four enumerated classes, and for L1 partition/cardinalities, L3, L4, L5, L7 and L8 it names no authoritative layer. Answer to the S4 question: yes, the omission misleads. Raised as **R342-1-F1 (MINOR)**. | `receipts/clause-and-authority-check.md` |
| 4 | Integrator guide §6 `entity_model_id_i` rule | **Correct.** The port feeds only the ADPDU (`KL_adp_engine.sv:859`), while ENTITY bytes come from the image, so the "same identity" rule is a real integrator obligation. Zero and all-ones are invalid per Milan §5.3.3.1. Evolution with exclusions is per IEEE §6.2.2.8, which lists exactly those exclusions. The stream-count maxima match Milan §5.3.3.1. The unconditional primary-IDENTIFY rule matches the fixed ADP capability `0x0000C588` (`pp_adp_pkg.sv:53`), which sets AEM_IDENTIFY_CONTROL_INDEX_VALID. All four ports exist (`protocol_processor_top.sv:183–190`). | source reads; clause receipt |
| 5 | No code change; gates | Only `docs/architecture/07_memory_maps.md` and `docs/guides/integrator.md` changed. The `hdl`, `tb`, `scripts`, `syn` and `.github` subtree ids are identical at base and head. Gates, all rc 0: check-links (917 links, including the new `#31-descriptor-tree` anchor), check-matrix, check-integrator-params, render-wavedrom --check, make stale, lint-diagrams (41 mermaid + 18 wavedrom), gen_matrix --check (92 rows, 0 untested), `git diff --check` on the range, and the existing body/key tests (6 OK). | `receipts/gates/` |

## Findings

### R342-1-F1 — MINOR — §3.1 states the parent's authority for only four semantic classes; L1/L3/L4/L5/L7/L8 have no stated authority

- **Lenses:** Conformance, Docs.
- **Location:** `docs/architecture/07_memory_maps.md:99–103` (authority sentence), `:109–115` (#60 listed as "model-rule coverage" and the rule table introduced as "model obligations").
- **Authority / evidence:**
  - Parent `PP_DESCRIPTOR_OWNERSHIP.md@e0920d77`, lines 23 and 36–38: "Parent shipping checks are authoritative for generated model content. Retained processor semantic checks provide defence in depth. Generic packer checks remain authoritative for packed-image acceptance."
  - Parent rule-matrix rows :58–65 give L1/L3/L4/L5/L7/L8 to parent construction and refusals. Parent follow-ups F2/F3/F4 cover L4 and L6. Parent row :244 reads "Existing L1/L2/L3/L5/L7/L8 debt: PP60, with parent semantic allocation above".
  - The four classes in §3.1 come from parent :27–29, which introduces them with "These include". §3.1 turns that into an exhaustive list after a colon and puts it in place of the broader :36 authority.
  - Issue #125 scope: "does not assign descriptor semantics to 'model lint' without saying who implements which check".
  - Processor #60 is titled "Entity-model lint L1-L8 … does not exist: add it to gen_desc_image.py or re-scope". §3.1 lists it as an open obligation with no owner split.
  - Probes: the processor packer accepts an L1/F07.2 zero-cluster input port, the L4 buffer floor violation and L9 invalid IDs (`receipts/packer-claims.tsv`). So only parent checks refuse L3/L7 violations today (parent :60, :64).
- **Impact:** A reader of the processor contract (another consuming product, or a processor maintainer working #60) can take L1/L3/L4/L5/L7/L8 to be processor-authoritative model lint. That is the opposite of the reviewed #509 allocation, where processor semantic checks are only defence in depth. The integrator guide link (`docs/guides/integrator.md:251–253`) promises that §3.1 "identifies the parent shipping checks". Yet the parent's existing L3/L7 refusals and the L4 follow-ups are not identified. The section also narrows the parent page it cites as its authority.
- **Required outcome:** §3.1 states the same split as parent :36–38 for every rule. Parent shipping checks are authoritative for generated model content: the four named classes plus L1 partition/cardinalities (including the F07.2 minima), L2 multi-level ordering, L3, L4, L5, L7 and L8. Processor-retained semantic checks, including any future #60 lint, are defence in depth. Generic packer checks are authoritative for packed-image acceptance. One sentence is enough, or a per-rule owner note; the L1–L10 rows themselves stay unchanged.
- **Verification:** Re-read §3.1 against parent :23–38 and matrix rows :58–68. Docs gates rc 0 (`scripts/run_docs_gates.sh`). `scripts/probe_packer_claims.py` still 18/18 OK, since no packer statement should change.

### R342-1-S1 — SUGGESTION — ambiguous referent "the generic checks above"

- **Lenses:** Docs.
- **Location:** `docs/architecture/07_memory_maps.md:135`. The paragraph comes right after the L1–L10 table, so "the generic checks above" can be read as the table rules.
- **Suggestion:** Write "the generic packed-image checks listed in the §3.1 introduction". This does not affect the verdict.

### R342-1-S2 — SUGGESTION — name the parent tracking issue for the D8 conflict

- **Lenses:** Docs.
- **Location:** `docs/architecture/07_memory_maps.md:81–83`. The note links the #122 disposition but not kebag-logic/milan-fpga#584, which the manager recorded as the owner of the product correction.
- **Suggestion:** Add the #584 link so the conflict note points at its owner-tracked record. This does not affect the verdict.

## Lens evidence

- **Conformance:** I extracted the cited pages myself (clauses and quotes in the receipt) and confirmed the §5.3.3.8 quote and page number. number_of_maps=0 does not waive the minimum. IEEE §6.2.2.8 exclusions, Milan §5.3.3.1 identity and maxima, and §5.3.3.10 IDENTIFY are all correctly cited. I compared the ownership contract line by line with the parent page. UNCLEAN because of F1.
- **RTL:** No RTL change (identical `hdl`/`tb` subtree ids `6bc47f4b…`/`32efe44f…`). I checked the doc's RTL-facing claims against source: the ADP serialization of `entity_model_id_i`, `talker_sources_i`, `listener_sinks_i` and `identify_index_i` (`KL_adp_engine.sv:859–871`); the fixed entity capabilities (`pp_adp_pkg.sv:53`); and the SET_SAMPLING_RATE / SET_CLOCK_SOURCE preconditions in 06 §6.4 (`06_aecp_engine.md:363–364`), which still agree with L6/L10 as documented. CLEAN.
- **Robustness:** Packer boundaries probed with accepted controls and single changes: line buffer 576/577, body/key type and index in both input forms, configuration and index gaps, duplicates, name binding. Semantic non-enforcement probed with byte-survival checks. Two disposable mutations of a scratch packer copy both flipped the expected rows: removing the body/key check gives 4 MISMATCH, and adding an L10 offset check gives 1 MISMATCH. So the probe discriminates in both directions. CLEAN.
- **Tests:** No test change is required or made (docs-only). The existing `tb/desc_store/test_gen_desc_image.py` passes (6 tests). The acceptance-relevant enforcement claims are covered by `receipts/packer-claims.tsv`, and my results match the author's eight L6/L10 observations. CLEAN.
- **Docs:** All docs gates rc 0. Anchors and links resolve: `#31-descriptor-tree`, the #122 comment 5853884588, the parent blob at short SHA `e0920d77` (resolves through the API), and #38/#39/#60/#89 (open). The AUDIO_UNIT extent `144 + 4 × count` matches F07.3 and IEEE §7.2.3. The loader, conversion and shipping limits match parent :67, :104–110 and :156–158. UNCLEAN because of F1. S1 and S2 are suggestions only.

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (R342-1-F1) | Milan v1.2 PDF pp. 31/32/34/35; IEEE 1722.1-2021 pp. 50/81–82; parent PP_DESCRIPTOR_OWNERSHIP.md@e0920d77; #509 handoff wording; 07 §3.1 :56–137; integrator §6 :226–253 | R342-1 | 1d249e6e18a91c16a2620904483634548b0414a6 |
| RTL | CLEAN | subtree ids base vs head; `KL_adp_engine.sv:110,859–871`; `pp_adp_pkg.sv:53`; `protocol_processor_top.sv:183–190,1651–1658`; `06_aecp_engine.md:363–364` | R342-1 | 1d249e6e18a91c16a2620904483634548b0414a6 |
| Robustness | CLEAN | `gen_desc_image.py` (whole file); `receipts/packer-claims.tsv`; `receipts/mutation-bodykey-removed.tsv`; `receipts/mutation-l10-offset-added.tsv` | R342-1 | 1d249e6e18a91c16a2620904483634548b0414a6 |
| Tests | CLEAN | `tb/desc_store/test_gen_desc_image.py` run (6 OK); `tb/desc_store/Makefile`; author ENFORCEMENT-PROBES.txt vs own probe | R342-1 | 1d249e6e18a91c16a2620904483634548b0414a6 |
| Docs | UNCLEAN (R342-1-F1; S1, S2 suggestions) | full diff; `receipts/gates/` (10 gates rc 0); link and anchor targets; parent limits cross-check | R342-1 | 1d249e6e18a91c16a2620904483634548b0414a6 |

## Real limits

- The designated Verilator 5.050 path (`$VALIDATION_STORAGE/372-manager-candidate1/pinned-tool-bin/verilator`) does not exist on this host. The only Verilator present is an unpinned 5.052 system install, and I did not use it. I ran no RTL simulation. The RTL lens rests on byte-identical `hdl`/`tb` subtrees plus source reading.
- The public evidence tree `review-evidence/pp125-r1` at `64e5bbde` contains only author files. I found no receipts there for the manager's source static/builder and native banks, so I rely on the manager's statement that they passed. I ran no full parent, processor, gPTP, Yosys or builder bank, and no donor or patched parent consumer bank (not allowed; the manager runs them).
- Hosted checks at the exact head, read at review time: docs-gates success (push and PR) and portability success (push and PR). Both `suites` runs were still in progress (`receipts/hosted-check-runs.tsv`). Hosted and act acceptance belong to the manager.
- The wavedrom freshness gate ran with a scratch-venv interpreter (wavedrom 2.0.3.post3) so that nothing was installed in the checkout. Physical calibration was NOT RUN; field skips are not hardware proof.
- The current-dev merge candidate (source base `493e5e4b`, live dev `e0920d77`) is separate from this source validation and was not built by me.

## Pending manager duties

- Route R342-1-F1 to the author. Re-review is needed at any new head.
- Hosted `suites` completion and hosted/act acceptance at the exact head. Confirm the manager bank receipts are published.
- Donor and patched parent consumer banks. Build the current-dev candidate at the merge turn.
- The second independent review (external). Merge needs two independent positives and the full completion bar.
- The parent D8 correction stays with kebag-logic/milan-fpga#584. This PR does not close that discrepancy.

## Tree integrity after probes

All probes ran on scratch copies or read the checkout without writing. Afterwards: 249 tracked entries re-hashed with matching blob bytes and modes; index equals HEAD; no untracked, ignored or modified entries; 0 gitlinks and no `.gitmodules`, so no submodule gitlinks apply (`receipts/tree-integrity.txt`).

## Reproduction

```
scripts/run_docs_gates.sh <checkout> <out-dir> [python-with-wavedrom]
python3 -B scripts/probe_packer_claims.py <checkout> <out.tsv>
scripts/verify_tree_bytes.sh <checkout> 1d249e6e18a91c16a2620904483634548b0414a6 13f98a7f404d96a78947f75c1a7ef2f30c8e8b26
```

R342-1 FINISHED
