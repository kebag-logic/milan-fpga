[R342] POSITIVE - exact head e04234e115cfdcaace393ae62ba68562d47834c6

# R342-2 independent internal review: processor PR #126 (issues #125 and #122), round 2

- Repository: Mister-M-alt/protocol-processor-control-plane-avb-milan.
- Exact head `e04234e115cfdcaace393ae62ba68562d47834c6`, tree `39ef4afe919b40c7b5c66f4be340ae20fae7b197`. It matches `refs/heads/125-ownership-contract` and `refs/pull/126/head`. It is one docs-only commit on `1d249e6e18a91c16a2620904483634548b0414a6`, which sits on base `493e5e4bf58a6146bf9310194d71c72e18610704`.
- Assignment: issue #125 decision comment 5854030459. Review start: PR #126 comment 5854107167.
- Scope: this is a delta review of `1d249e6e..e04234e1`. My round-1 review (R342-1, PR comment 5854021294) covered `1d249e6e` in full, and the round-1 CLEAN results for RTL, Robustness and Tests carry forward because the code subtrees are byte-identical.
- Verdict: **POSITIVE**. No MINOR, MAJOR or BLOCKER finding is open. §3.1 now gives each L1–L10 rule the same authoritative layer as the parent page. Every packer enforcement statement is still true at `493e5e4b` (probe 18/18 OK). The Milan v1.2 §5.3.3.1 citation is correct. No code changed. All docs gates, including `check-links`, return 0. R342-1-F1 is **closed**. One new SUGGESTION (R342-2-S1) does not affect the verdict.

## Reconstruction

1. **Contribution rules.** This repository has no AGENTS.md or CONTRIBUTING.md at the head. The author conventions are in `docs/README.md`: the single-source rules, the citation rule "printed = PDF − 7" and the reading order. The gates are in `.github/workflows/hdl.yml` (job `docs-gates`) and `Makefile` (`check`).
2. **Frozen scope and acceptance.**
   - Issue #125 body: acceptance items 1–4.
   - Assignment 5853861179 and its correction 5853864238.
   - Round-2 decision 5854030459: the same split as parent :36-38 for every L1–L10 rule, plus items 2–5.
   - Author ready notice 5854096496.
   - PR #126 body, including its Round 2 section, and the manager comment 5853945556 (the parent correction is kebag-logic/milan-fpga#584).
3. **Authorities.**
   - Parent `docs/reference/PP_DESCRIPTOR_OWNERSHIP.md` at `e0920d77162284d8da52ffaf13a973e451e44f90`, fetched read-only. Its sha256 is `ad9bb61f…6bf6d8`, identical to the blob I compared in round 1.
   - Milan v1.2 PDF pp. 31–32 and IEEE 1722.1-2021 p. 82, which I extracted myself.
   - kebag-logic/milan-fpga#584 and processor issues #38, #39, #60 and #89, all OPEN (`receipts/external-links.txt`).
4. **Diff and history.** `1d249e6e..e04234e1` touches two files, +26/−18 (`receipts/diff-1d249e6e..e04234e1.patch`). `493e5e4b..e04234e1` has two commits, touches the same two files, and changes nothing else.
5. **Public evidence.**
   - kebag-logic/milan-fpga `64e5bbde…` `review-evidence/pp125-r1` holds only the round-1 author files and their MANIFEST.json, all at `1d249e6e`. It holds nothing for `e04234e1`, and no manager bank receipts; see Limits.
   - The manager's evidence comments on the issue and the PR are the ones listed in step 2.

## Focus items

| # | Question | Result | Evidence |
|---|---|---|---|
| 1 | Does every L1–L10 row have one stated authoritative layer, identical to parent :23-38 and rows :58-68? | **Yes.** `07_memory_maps.md:100-107` restates parent :36-38. **Parent** is authoritative for L1 partition/cardinalities (including the F07.2 minima), L2 multi-level ordering, L3, L4, L5, L6, L7, L8, L9, L10 and the ADP maxima. **Processor** semantic checks, including any retained or added under #60, are defence in depth. **Generic packer** checks are authoritative for packed-image acceptance, including L2 index density. L2 is the only split row, and parent row :59 splits it the same way: processor **R** for duplicates and gaps, parent **C/T** for multi-level ordering. No text in §3.1 (:78-143) gives the processor authority for a semantic rule. The L6/L10 rows state consumer reliance only. :140-143 keeps the packer gaps open under #89 and parent F6, which matches parent :67. | `receipts/authority-side-by-side.md` |
| 2 | Are all packer enforcement statements still true at `493e5e4b`? | **Yes, 18/18 OK** with the unchanged round-1 probe (sha256 `f5ca7619…c8d5`), both at this head and on an export of `493e5e4b`. The two TSVs are identical to each other and to the round-1 receipt. The packer requires indices dense from 0 per (configuration, type) (`gen_desc_image.py:342-344`), which supports "including L2's index density". Discrimination re-checked on scratch copies: removing the density check makes the probe exit 1 (a crash on the gap mutant, `receipts/mutation-density-removed.log`); removing the body/key check gives exactly the 4 body/key MISMATCH rows (`receipts/mutation-bodykey-removed.tsv`). | `receipts/packer-claims-head.tsv`, `receipts/packer-claims-493e5e4b.tsv`, mutation receipts |
| 3 | Is the §5.3.3.1 citation correct? | **Correct.** Milan v1.2 PDF p. 32 is printed p. 25 (the footer reads "5.3. Entity model 25"). Under "5.3.3.1 ENTITY" it says the entity_model_id field "shall be a valid EUI-64 (neither all zeros nor all ones)". §5.3.1 (printed p. 24) carries the rule that a changed model reports a new ID. The L9 column "Milan v1.2 §5.3.1, §5.3.3.1" (:132) therefore cites both halves of L9, and integrator :242 cites the validity half with the right page. The reworded `number_of_maps` sentence (:80-81) matches IEEE 1722.1-2021 §7.2.13 (PDF p. 82): dynamic-mapping entities "set the number_of_maps field to zero (0)", and number_of_clusters is a separate field. | `receipts/clause-check.md` |
| 4 | Is there any code change? | **None.** The `hdl`, `tb`, `scripts`, `syn`, `.github` and `Makefile` object ids are identical at `493e5e4b`, `1d249e6e` and `e04234e1`. `--name-status` lists only `docs/architecture/07_memory_maps.md` and `docs/guides/integrator.md`. | `receipts/diff-1d249e6e..e04234e1.patch` |
| 5 | Do the docs gates and check-links pass? | **All rc 0.** check-links (917 links), check-matrix (115 REQ, 17 GAP), check-integrator-params (24/24/24), render-wavedrom --check (18 blocks), make stale, lint-diagrams (41 mermaid + 18 wavedrom), gen_matrix --check (92 rows, 0 untested), `git diff --check` on `493e5e4b..e04234e1` and on `1d249e6e..e04234e1`, and the body/key unit tests (6 OK). `check-links.py` skips http(s) targets (`:70`), so I resolved the new external targets separately: milan-fpga#584 is OPEN and is the D8 owner, and the #122 comment 5853884588 exists. | `receipts/gates-head/`, `receipts/external-links.txt` |

## Prior public review findings at this head

I read these only after my own pass; see the ordering note under Limits. All of them were taken in decision 5854030459.

| Finding | Status at e04234e1 | Evidence |
|---|---|---|
| R342-1-F1 (MINOR, my round-1 finding): §3.1 stated parent authority for four classes only | **Closed** | `07_memory_maps.md:100-107` now matches parent :36-38 for every rule; see focus item 1 |
| R343-1-M1 (MINOR), which is the same defect as F1, and the parent review suggestion R331-1 S4 it absorbed | **Resolved** | same evidence as F1; each rule has one layer, identical in both documents |
| R342-1-S1: ambiguous "generic checks above" | **Resolved** | :140-141 "the generic packed-image checks listed in the §3.1 introduction" |
| R342-1-S2 = R343-1-S3: link #584; `number_of_maps` wording | **Resolved** | :80-84 link [milan-fpga#584] and read "dynamic mapping sets `number_of_maps` to zero; it does not relax the cluster count"; clause re-verified |
| R343-1-S1: which three per-source vectors | **Resolved** | `integrator.md:257-258` names `cfg_src_en_i`, `cfg_src_iface_i` and `cfg_stream_id_i`. These are the top ports at `protocol_processor_top.sv:211-213`, with widths N, 2N and 64N, consistent with `[W*s +: W]` |
| R343-1-S2: cite §5.3.3.1 | **Resolved** | `integrator.md:242`; L9 clause column :132; clause verified |

No review bodies or inline review comments exist on PR #126 (0 and 0 at 08:20Z).

## Findings

### R342-2-S1 — SUGGESTION — the compliance-matrix clause for REQ-ADP-003 does not cite §5.3.3.1

- **Lenses:** Conformance, Docs.
- **Location:** `docs/00_MILAN_COMPLIANCE_REVIEW.md:306`. This line is not part of this PR's diff and is unchanged since the base.
- **Evidence:** REQ-ADP-003 ("entity_model_id valid EUI-64 (≠0, ≠all-1s); changes when static model changes") cites "Milan §5.6.2, §5.3.1". L9 (`07_memory_maps.md:132`) and the integrator guide (`:242`) now cite Milan v1.2 §5.3.3.1 for the validity half, which is where the clause actually states it (`receipts/clause-check.md`).
- **Impact:** The requirement row and the rule row cite different clauses for the same obligation. It does not affect behaviour or the ownership contract.
- **Suggested outcome:** In a later docs change, add §5.3.3.1 to REQ-ADP-003's clause column. It is not required for #125/#122 acceptance.
- **Verification:** Re-read `00_MILAN_COMPLIANCE_REVIEW.md:306` against the extracted §5.3.3.1 text; `scripts/check-matrix.py` rc 0.

No MINOR, MAJOR or BLOCKER finding is open.

## Lens evidence

- **Conformance:** CLEAN.
  - I compared each rule row against parent :23-39 and :58-68 (`receipts/authority-side-by-side.md`).
  - I extracted Milan v1.2 PDF pp. 31–32 and IEEE p. 82 myself; the file hashes are in `receipts/clause-check.md`. Both are correct: §5.3.3.1 (validity, printed p. 25) and §5.3.1 (evolution). The `number_of_maps` rewording is faithful to §7.2.13 and does not weaken the §5.3.3.8 minimum. The #584 target is the parent issue whose acceptance fixes D8.
  - The processor claims authority for no semantic rule, as the decision requires.
- **RTL:** CLEAN.
  - The `hdl` subtree is byte-identical at `493e5e4b`, `1d249e6e` and `e04234e1` (`6bc47f4b…`).
  - The doc's RTL-facing names still match the source: `entity_model_id_i`, `talker_sources_i`, `listener_sinks_i` and `identify_index_i` (`protocol_processor_top.sv:183-190`), and the three `cfg_src_*` / `cfg_stream_id_i` vectors with their widths (`:211-213`).
  - I ran no RTL simulation; nothing in the delta needs one.
- **Robustness:** CLEAN.
  - The packer boundary claims were re-measured at this head and at `493e5e4b`: accepted controls, single changes, and byte-survival checks for the semantic non-enforcement rows.
  - The probe still discriminates: both disposable scratch mutations fail it.
- **Tests:** CLEAN. This is docs-only, so no test change is required. `tb/desc_store/test_gen_desc_image.py` passes (6 OK). The tests the round-2 gates require are the ones run above.
- **Docs:** CLEAN.
  - All gates rc 0 and whitespace is clean on both ranges.
  - The external targets resolve.
  - The integrator anchor `#31-descriptor-tree` still resolves.
  - The prose now matches the PR body's Round 2 section.
  - One SUGGESTION (S1).

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | parent PP_DESCRIPTOR_OWNERSHIP.md@e0920d77 :23-39, :58-68; `07_memory_maps.md:78-143`; `integrator.md:241-259`; Milan v1.2 PDF pp. 31–32; IEEE 1722.1-2021 PDF p. 82; milan-fpga#584; `receipts/authority-side-by-side.md`, `receipts/clause-check.md` | R342-1 (1d249e6e in full) + R342-2 (delta) | e04234e115cfdcaace393ae62ba68562d47834c6 |
| RTL | CLEAN | subtree/object ids at 493e5e4b, 1d249e6e and e04234e1; `hdl/top/protocol_processor_top.sv:183-190,211-213` | R342-1 + R342-2 | e04234e115cfdcaace393ae62ba68562d47834c6 |
| Robustness | CLEAN | `hdl/aecp/desc/gen_desc_image.py:209-235,336-347`; `receipts/packer-claims-head.tsv`, `receipts/packer-claims-493e5e4b.tsv` (18/18 each); `receipts/mutation-*.{diff,tsv,log}` | R342-1 + R342-2 | e04234e115cfdcaace393ae62ba68562d47834c6 |
| Tests | CLEAN | `tb/desc_store/test_gen_desc_image.py` (6 OK, `receipts/gates-head/gate-packer-body-key-tests.log`); unchanged probe script | R342-1 + R342-2 | e04234e115cfdcaace393ae62ba68562d47834c6 |
| Docs | CLEAN (S1 suggestion only) | `receipts/diff-1d249e6e..e04234e1.patch`; `receipts/gates-head/` (11 logs, all rc 0); `receipts/external-links.txt`; PR body Round 2 section | R342-1 + R342-2 | e04234e115cfdcaace393ae62ba68562d47834c6 |

## Real limits

- **Ordering disclosure.** I decided the verdict and ledger at the end of my independent pass. My first attempt to save that draft failed on a file-write precondition. In the same step a heading-only index of the other reviewer's round-1 comment was listed. I then saved the draft unchanged (POSITIVE, all lenses CLEAN), and only after that read the comment in full. Nothing I read changed a result: every round-1 item was already addressed at this head and is listed above.
- **Verilator.** The designated Verilator 5.050 path (`$VALIDATION_STORAGE/372-manager-candidate1/pinned-tool-bin/verilator`) does not exist on this host. I ran no RTL simulation. The RTL lens rests on byte-identical code subtrees and on reading the source.
- **Manager banks.** The public evidence tree `review-evidence/pp125-r1` at `64e5bbde` contains only round-1 author files at `1d249e6e`. It holds no receipts for the manager's source static/builder and native banks at this head, so I rely on the manager's statement that they passed. I ran no full parent, processor, gPTP, Yosys or builder bank (not allowed).
- **Hosted checks.** At the exact head, read at 2026-09-27T08:20:01Z: `docs-gates` succeeded (both runs) and `portability` succeeded (both runs). Both `suites` runs were still `in_progress` (`receipts/hosted-check-runs.tsv`). Hosted and act acceptance belong to the manager.
- **Hardware.** Physical calibration was NOT RUN; field skips are not hardware proof. This change is docs-only and has no hardware claim.
- **Wavedrom gate.** It ran with a scratch virtual-environment interpreter (wavedrom 2.0.3.post3), so nothing was installed into the checkout or shared locations.
- **Spec text.** Standard text in the receipts is limited to short clause citations. The full page extractions stay in unpublished scratch.

## Pending manager duties

- Confirm that both exact-head `suites` runs completed successfully, and own hosted/act acceptance.
- Build and validate the final current-dev candidate at the merge turn. The source base is `493e5e4b`; live dev is `e0920d77162284d8da52ffaf13a973e451e44f90`. That validation is separate from this source review.
- Obtain the second independent review at this exact head before merge.
- Keep the parent D8 correction tracked under kebag-logic/milan-fpga#584. Once #126 closes #122, the processor text points there.
- Optionally schedule R342-2-S1.

## Reproduction

```
scripts/run_docs_gates.sh <checkout> <out-dir> 493e5e4bf58a6146bf9310194d71c72e18610704 e04234e115cfdcaace393ae62ba68562d47834c6 [python-with-wavedrom]
python3 -B scripts/probe_packer_claims.py <checkout> <out.tsv>        # exit 0 = 18/18 OK
scripts/verify_tree_bytes.sh <checkout> e04234e115cfdcaace393ae62ba68562d47834c6 39ef4afe919b40c7b5c66f4be340ae20fae7b197
```

Tree integrity after all probes (`receipts/tree-integrity.txt`): 249 tracked entries match their head blob bytes and modes, the index equals HEAD, there are no stray files, and there are 0 gitlinks (this repository has no submodules). All probes and mutations ran on read-only imports or on scratch exports, never on the review clone.

R342-2 FINISHED
