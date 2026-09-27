[R343] POSITIVE - exact head e04234e115cfdcaace393ae62ba68562d47834c6

# R343-2: external independent review of processor issues #125 / #122, PR #126 (round 2, delta)

- Repository: Mister-M-alt/protocol-processor-control-plane-avb-milan.
- Head `e04234e115cfdcaace393ae62ba68562d47834c6`, tree `39ef4afe919b40c7b5c66f4be340ae20fae7b197`; the PR head matched this commit when I read it at the start and at the end.
- Delta judged: `1d249e6e..e04234e1`, one docs-only commit, `docs/architecture/07_memory_maps.md` (+21/-15) and `docs/guides/integrator.md` (+5/-3) (`receipts/delta-1d249e6-e04234e.diff`). My round-1 review (R343-1) covered `493e5e4b..1d249e6e` in full. The full PR diff is in `receipts/pr126-full-493e5e4-e04234e.diff`.
- Role: external reviewer, cleared context, isolated detached clone. Review start: PR #126 comment 5854109710.
- **Verdict: POSITIVE.** No MINOR, MAJOR or BLOCKER is open, and all five lenses are CLEAN. There is one new SUGGESTION (R343-2-S1), about pre-existing text outside the delta. My round-1 MINOR and all round-1 suggestions from both reviewers are closed at this head.

## Reconstruction

1. **Conventions.** This repository has no AGENTS.md or CONTRIBUTING.md. I used `docs/README.md` in their place, plus the Milan v1.2 target and the "printed = PDF − 7" rule (`docs/00_MILAN_COMPLIANCE_REVIEW.md:50`). Gates come from `.github/workflows/hdl.yml` and `Makefile`.
2. **Frozen scope.** Issue #125 body, acceptance items 1-4; issue #122 body; assignment comments 5853861179 and 5853864238; round-2 decision 5854030459; executor ready notice 5854096496; PR comment 5853945556 (#584 pointer) (`receipts/issue125-comments.json`, `receipts/pr126-comments.json`).
3. **Authority.** Parent `docs/reference/PP_DESCRIPTOR_OWNERSHIP.md` at `e0920d77162284d8da52ffaf13a973e451e44f90` (blob `ba9674d4…`, copy in `receipts/parent-PP_DESCRIPTOR_OWNERSHIP-e0920d77.md`), read at `:23-39` and matrix rows `:56-68`. Milan v1.2, §5.3.1, §5.3.3.1 and §5.3.3.8, extracted by me.
4. **Diff and history.** `e04234e1` has one parent, `1d249e6e`, which has one parent, `493e5e4b`. Only two `.md` files change. `hdl`, `tb`, `scripts`, `syn`, `.github`, `Makefile`, the packer and its example JSON have the same object ids at base, round 1 and head (`receipts/no-code-change.txt`).
5. **Public evidence.**
   - `kebag-logic/milan-fpga@64e5bbde…/review-evidence/pp125-r1` holds only round-1 author files.
   - The `pp125-review-evidence` branch at `0b448a50` adds the round-1 review packets and the round-2 author packet (`author-r2`).
   - I found no manager bank receipts in either location (see Limits).
6. **Prior public review findings.** I read them only after my own pass over the delta (`receipts/authority-side-by-side.md` was written first): R342-1 (5854021294) and R343-1 (5854028198). PR #126 has 0 formal reviews and 0 inline comments (`receipts/pr126-reviews.json`, `receipts/pr126-review-comments.json`). I did not read any round-2 report from another reviewer.

## Prior findings: resolution at this head

| Finding | Status at `e04234e1` | Evidence |
|---|---|---|
| **R343-1-M1** (MINOR) = R342-1-F1: §3.1 stated parent authority for only four classes | **CLOSED** | `07:100-107` now states the parent `:36-38` split for every L1-L10 obligation. Checked rule by rule in the next section and `receipts/authority-side-by-side.md`. |
| R343-1-S1: "three per-source vectors" referent | CLOSED | `integrator.md:257-258` names `cfg_src_en_i`, `cfg_src_iface_i`, `cfg_stream_id_i`. These are the three flat vectors at `protocol_processor_top.sv:211-213`, sliced `[W*s +: W]` at `KL_acmp_talker.sv:375,380` and bit-indexed (W=1) at `:619,1065`. |
| R343-1-S2: cite Milan §5.3.3.1 | CLOSED | `integrator.md:242` "(Milan v1.2 §5.3.3.1, printed p. 25)"; L9 clause column `07:132` "Milan v1.2 §5.3.1, §5.3.3.1". Clause and page verified (`receipts/clause-citation.txt`). |
| R343-1-S3 = R342-1-S2: #584 link; `number_of_maps` wording | CLOSED | `07:80-84`: "dynamic mapping sets `number_of_maps` to zero; it does not relax the cluster count … the parent owns the D8 product correction under milan-fpga#584". The link resolves to kebag-logic/milan-fpga#584, which is open and titled for the §5.3.3.8 zero-cluster defect (`receipts/external-links.txt`). |
| R342-1-S1: "the generic checks above" referent | CLOSED | `07:140-141` "the generic packed-image checks listed in the §3.1 introduction" refers to the list at `07:94-98`. |

## Focus verification

### 1. Every L1-L10 rule has one stated authoritative layer, identical to the parent page

The processor text at `07:100-107` has three parts:
- It makes parent shipping checks authoritative for "all generated model content, including every L1–L10 model obligation below". It then lists: L1 partition and cardinalities (including F07.2 minima), L2 multi-level ordering, L3, L4, L5, L6 construction and list shape, L7, L8, L9 identity and evolution, L10 offset/count/length, and ADP maxima.
- It makes "All processor semantic checks, including those retained or added under #60" defence in depth.
- It makes generic packer checks authoritative for packed-image acceptance, "including L2's index density".

These three sentences match parent `:36-38` sentence for sentence. The decision's wording (5854030459) is reproduced in full, and only the six generic structural items at `07:90-98` stay processor-owned (parent `:31-32`).

Rule by rule against the "Authoritative enforcement and evidence" column of parent rows `:58-68`:

| Rule | Parent authoritative column | Processor stated layer | Result |
|---|---|---|---|
| L1 | Parent | Parent | Match. |
| L2 | Processor R (duplicates, gaps) + Parent C/T (two-level ordering) | Ordering: parent. Density: packer. | Match, with the same split as the parent row. |
| L3-L10 and ADP maxima | Parent | Parent | Match; L5 also matches the parent's "processor density is only supporting evidence". |

- **No rule without a layer.** No rule is left without a layer, and no sub-obligation has two.
- **No processor semantic authority.** The processor claims authority for no semantic rule.
- **Remaining references are consistent.** `#89` (`07:116-117`, `:142-143`) and the `#38`/`#39` open obligations fall under "All processor semantic checks … defence in depth", so they do not contradict the split.
- **Enumeration detail.** For L6 and L10 the list names only part of the rule: it omits the gPTP-chain restriction and the full-word entry. The umbrella "every L1–L10 model obligation" still covers both, as in the parent. I record this as an observation, not a finding.

### 2. Packer enforcement statements are still true at `493e5e4b`

The delta changes only the wording of the enforcement sentence. The packer blob `3d835531…` is identical at base, round 1 and head.

| Probe run | Result | Receipts |
|---|---|---|
| R342's probe, `probe_packer_claims.py` (sha256 `f5ca7619…`, matches R342-1's published manifest), run unchanged against the exact-head checkout | **18/18 OK** | `receipts/packer-claims-head.tsv`, `receipts/packer-claims-probe.log` |
| Same probe against a `git archive` export of `493e5e4b` | **18/18 OK** | `receipts/packer-claims-base.tsv` |

The head TSV is byte-identical to R342-1's published `packer-claims.tsv` and to the round-2 author `PACKER-CLAIMS.tsv`. What the probe shows:
- **Refused:** configuration gaps, per-type gaps, duplicate keys, name binding, the 577-byte line-buffer bound, and body/key type and index disagreement in both `fields` and `bytes` form.
- **Accepted, with the mutated bytes present in the image:** L10 offset, count and length mutations, and the L6 list `[1,0]`.

Discrimination, all on scratch copies:

| Mutant | R342's probe | My round-1 bank (20 rows; 0 mismatches at head, identical to the R343-1 published log) |
|---|---|---|
| M1 (body/key check removed) | exactly the 4 body/key rows flip (14/18) | 4 mismatches |
| M2 (L6/L10 refusals added) | exactly the 4 L10 rows and the L6 row flip (13/18) | 7 mismatches (the six "not enforced" rows plus the 576-byte padding row, as explained in R343-1) |

Receipts: `receipts/packer-claims-mutant-*.{tsv,log}`, `receipts/probe_packer_*.log`. The existing packer unit tests `tb/desc_store/test_gen_desc_image.py` ran 6 tests, all OK (`receipts/test_gen_desc_image.log`).

### 3. The Milan v1.2 §5.3.3.1 citation is correct

I extracted page 32 of the local Milan v1.2 PDF myself (sha256 `6bb902be…`). The page footer is printed p. 25, and 32 − 7 = 25 agrees with the repository rule. §5.3.3.1 ENTITY says: "The entity_model_id field shall be a valid EUI-64 (neither all zeros nor all ones)."

§5.3.1 (printed p. 24) carries only the model-change note. So the L9 column "§5.3.1, §5.3.3.1" cites evolution and validity correctly. The extracted text stays in unpublished scratch; `receipts/clause-citation.txt` holds the one-sentence citation only.

### 4. No code change

Only the two documentation files differ (`receipts/no-code-change.txt`).

### 5. Docs gates and link checks pass

All nine gates returned rc 0, with non-vacuous counts (`receipts/docs-gates.log`):

| Gate | Count |
|---|---|
| check-links | 917 links |
| check-matrix | 115 REQ / 17 GAP |
| check-integrator-params | 24/24/24 |
| render-wavedrom `--check` | 18 blocks |
| `make stale` | — |
| gen_matrix `--check` | 92 rows, 0 untested |
| lint-diagrams | 41 mermaid + 18 wavedrom |
| `git diff --check` `493e5e4b..e04234e1` | — |
| `git diff --check` `1d249e6e..e04234e1` | — |

check-links covers only relative links. I resolved the external targets separately with read-only API calls (`receipts/external-links.txt`):
- milan-fpga#584 is open;
- the #122 comment 5853884588 exists;
- #38, #39, #60 and #89 are open, with the stated scopes;
- the parent page at `e0920d77` exists.

## Findings

### R343-2-S1 SUGGESTION - Conformance, Docs - `docs/00_MILAN_COMPLIANCE_REVIEW.md:306,403,406-410` (pre-existing, outside the delta)

- **Evidence.** The traceability matrix's Arch column still names "model lint", or "config/ID regs + model lint", as the architecture element for REQ-ADP-003 and REQ-MDL-002/005/006/007/008/009. It does not say whose lint it is. After this round, `07:100-107` makes parent shipping checks authoritative for those rules and processor semantic checks defence in depth.
- **Impact.** A matrix reader could still take processor model lint to be the covering element. No behaviour is affected. The text predates the PR, and issue #125's acceptance scopes the contract text to 07 §3.1 and integrator §6.
- **Optional outcome.** When #60 is worked, have these Arch cells say "parent shipping checks (processor lint: defence in depth, #60)", or point them to 07 §3.1.
- **Verification.** Reread the listed rows against `07:100-107`; `scripts/check-matrix.py` still rc 0.

No MINOR, MAJOR or BLOCKER findings.

## Per-lens results

```text
[R343] CLEAN Conformance - 07:78-143 and integrator.md:241-259 vs PP_DESCRIPTOR_OWNERSHIP.md@e0920d77 :23-39/:58-68, decision 5854030459, Milan v1.2 §5.3.1/§5.3.3.1/§5.3.3.8 (own extraction) - one authoritative layer per L1-L10 obligation, same as the parent; citation correct; S1 is a suggestion only
[R343] CLEAN RTL - no HDL/tb/syn change (object ids identical); RTL-facing delta claim traced: cfg_src_en_i/cfg_src_iface_i/cfg_stream_id_i at protocol_processor_top.sv:211-213 -> KL_acmp_talker.sv:375,380,619,1065 use the [W*s +: W] convention the guide states
[R343] CLEAN Robustness - enforcement statements re-measured at head and at a 493e5e4b export: R342 probe 18/18 each; R342 probe and round-1 bank both flip exactly the expected rows under mutants M1/M2
[R343] CLEAN Tests - packer unit tests 6/6 OK; probe banks and mutation discrimination; docs-only delta needs no new test
[R343] CLEAN Docs - delta text, referents, links (relative gate plus external resolution), nine docs gates rc 0, whitespace clean on both ranges; S1 suggestion only
```

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | 07 §3.1 `:78-143`; integrator §6 `:226-259`; parent ownership page `e0920d77` `:23-39`, `:56-68`; decision 5854030459; Milan v1.2 PDF pp. 31, 32, 34 (own extraction); `receipts/authority-side-by-side.md`, `clause-citation.txt`, `external-links.txt` | R343-2 (delta), on R343-1 full review | `e04234e115cfdcaace393ae62ba68562d47834c6` |
| RTL | CLEAN | `receipts/no-code-change.txt`; `protocol_processor_top.sv:183-213,1651-1655,1980-1982`; `KL_acmp_talker.sv:375-380,619,1065` | R343-2 | `e04234e115cfdcaace393ae62ba68562d47834c6` |
| Robustness | CLEAN | `packer-claims-{head,base}.tsv` (18/18 each); `packer-claims-mutant-*`; `probe_packer_head.log` (20/0); `probe_packer_mutant_*` | R343-2 | `e04234e115cfdcaace393ae62ba68562d47834c6` |
| Tests | CLEAN | `test_gen_desc_image.log` (6 OK); probe and mutation receipts; author-r2 `PACKER-CLAIMS.tsv` byte-identical to reviewer run | R343-2 | `e04234e115cfdcaace393ae62ba68562d47834c6` |
| Docs | CLEAN (S1 suggestion) | delta diff; `docs-gates.log` (9 gates rc 0); external link resolution; referent checks | R343-2 | `e04234e115cfdcaace393ae62ba68562d47834c6` |

## Real limits

- **No RTL simulation.** The designated pinned simulator path `$VALIDATION_STORAGE/372-manager-candidate1/pinned-tool-bin/verilator` does not exist on this host; its parent directory is absent too. I did not substitute any other build, so I ran no RTL simulation. The RTL lens rests on unchanged object ids and source tracing. For a docs-only delta that is adequate, but it is not executed RTL evidence.
- **Manager banks not visible.** No manager bank receipts (full static/builder and native banks at this head) are in `pp125-r1@64e5bbde`, the `pp125-review-evidence` branch at `0b448a50`, or the issue and PR comments. I rely on the assignment's statement that they passed. I did not run full parent, processor, gPTP, Yosys or builder banks; they are excluded.
- **Hosted checks at the exact head** (`receipts/hosted-checks-e04234e1.txt`, read 08:19Z and 08:21Z):
  - docs-gates: success on both push and pull_request;
  - portability: success on both push and pull_request;
  - suites: still `in_progress` on both runs;
  - combined status: `pending` with 0 statuses.

  I did not wait for or accept these results.
- **Standard text.** I extracted only the cited pages, and I publish only a one-sentence citation.
- **Wavedrom venv.** The wavedrom gate created an ignored `.venv-wavedrom/` in the clone. The reproduction script removes it.
- **Out of scope.**
  - Physical calibration was NOT RUN.
  - Field skips are not hardware proof.
  - Multi-configuration behaviour remains unproven by anyone; the parent emits one configuration per image.
  - The parent D8 zero-cluster defect is unchanged and stays with milan-fpga#584.
- **Parent page staleness (not a processor defect).** Parent `PP_DESCRIPTOR_OWNERSHIP.md:59` still says the packer accepts body/key disagreement (F7). Processor `07:97-98` correctly states the `493e5e4b` refusal, and the probe measures it.
- **Clone integrity** (`receipts/clone_integrity.txt`):
  - HEAD and tree are exact, and the index tree equals the HEAD tree;
  - 249 tracked entries re-hash with 0 blob or mode mismatches;
  - 0 non-`H` index flags;
  - 0 status lines, including ignored files;
  - 0 gitlinks and no `.gitmodules`, so no submodule gitlinks apply.

  A negative control on a scratch clone with one byte changed was detected (rc 1).

## Pending manager duties

- Hosted acceptance at the exact head, including completion of both `suites` runs. The manager owns hosted and act acceptance.
- Publish or link the source static/builder and native bank receipts for this head.
- Build the final current-dev candidate at the merge turn (source base `493e5e4b`, live dev `e0920d77`), as distinct from this source validation.
- Merge needs two independent positive reviews and the full completion bar. Also: containment, board state, and closing #125/#122 as the PR states.
- Parent follow-through: milan-fpga#584 (D8 zero-cluster inputs); the stale F7 wording at parent `PP_DESCRIPTOR_OWNERSHIP.md:59`; F6/#577.
- Optional: route R343-2-S1 to #60.

## Reproduction

```
# fetch round-1 public probe scripts into <packet>/scratch/r1pub/{R342-1,R343-1}/scripts from
#   kebag-logic/milan-fpga@0b448a509c4aeec6847a09cbc5cf9ee827d7717c review-evidence/pp125-r1/reviews/
scripts/run_all.sh <processor checkout at e04234e1> <packet dir>
scripts/verify_clone.sh <checkout> e04234e115cfdcaace393ae62ba68562d47834c6 39ef4afe919b40c7b5c66f4be340ae20fae7b197
```

R343-2 FINISHED
