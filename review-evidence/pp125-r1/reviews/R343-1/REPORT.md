[R343] NEGATIVE - exact head 1d249e6e18a91c16a2620904483634548b0414a6

# R343-1: external independent review of processor issues #125 / #122, PR #126

- Repository: Mister-M-alt/protocol-processor-control-plane-avb-milan.
- Head `1d249e6e18a91c16a2620904483634548b0414a6`, tree `13f98a7f404d96a78947f75c1a7ef2f30c8e8b26`.
- Base `493e5e4bf58a6146bf9310194d71c72e18610704` (main); one docs-only commit.
- Diff: `docs/architecture/07_memory_maps.md` (+47/-2) and `docs/guides/integrator.md` (+15/-0). Receipt: `receipts/pr126.diff`.
- Role: external reviewer, cleared context, isolated detached clone.
- Reconstruction order:
  1. Repository conventions. The repository has no AGENTS.md or CONTRIBUTING.md at this head; `docs/README.md` sections 1-6 (citation, printed-page and single-source rules, editing gates) stand in for them.
  2. Issue #125 body and assignment comments 5853861179 and 5853864238; issue #122 body and STOP comment 5853884588; PR #126 body and comments (including the parent-fix pointer 5853945556).
  3. Authorities: parent `docs/reference/PP_DESCRIPTOR_OWNERSHIP.md` at `e0920d77`; parent #509 decision 5844867005; the public #509 handoff wording (`509-review-evidence`, `review-evidence/509-r1/author/HANDOFF.md`, "Processor contract wording"); the public parent review R331-1 (its S4); processor issues #38, #39, #60, #89, #123.
  4. The diff and history (#124 = `eb73496` + `11dd3e9`).
  5. Public evidence tree `kebag-logic/milan-fpga@64e5bbde.../review-evidence/pp125-r1`.
- All five lenses applied independently. Result: one MINOR finding and three SUGGESTIONs.

## Prior public review findings

When I checked after my own pass, no review round had published findings on PR #126 or issue #125. The PR has two review-start notices, no review bodies and no inline comments (`receipts/pr126-comments.json`, `pr126-reviews.json`, `pr126-review-comments.json`). There is nothing to resolve or retain.

R331-1 S4 (a parent #509 review SUGGESTION on the handoff wording) is judged below as assigned. I retain it at this head and raise it to MINOR as R343-1-M1, because the omission now misleads in published processor text.

## Findings

### R343-1-M1 MINOR - Conformance, Docs - `docs/architecture/07_memory_maps.md:86-115`

**Authority/evidence.**
- Issue #125 scope requires that the contract "does not assign descriptor semantics to 'model lint' without saying who implements which check".
- The parent page that section 3.1 cites as the record (`PP_DESCRIPTOR_OWNERSHIP.md@e0920d77:36-38`) states:
  - parent shipping checks are authoritative for all generated model content;
  - retained processor semantic checks are defence in depth;
  - generic packer checks remain authoritative for packed-image acceptance.
- The processor text at `:99-103` restates the split more narrowly:
  - The parent is authoritative only for a colon-enumerated list of four classes: identity/evolution, AUDIO_UNIT rate list, clock sources, ADP maxima.
  - "Processor checks retained for the same semantic constraints are defence in depth." This covers only those four.
  - The processor-owned list at `:89-92` names six generic items.
- Six rules of the table at `:117-128` fall in neither list: L1's single-parent partition, L3, L4, L5, L7 and L8.
- For some of these the parent already holds authoritative refusals. Parent matrix rows `:60` and `:64`: `B._streams` refuses an empty stream direction (L3) and a static listener map (L7); `_map_duplicate_rule` refuses duplicate output targets (L7).
- Processor #60, still open, is titled "Entity-model lint L1-L8 ... add it to gen_desc_image.py or re-scope". Its obvious landing place is the packer, but the processor contract gives no authority for such checks.
- R331-1 S4 predicted exactly this divergence.

**Impact.**
- Read alone, the processor contract implies by exclusion that the parent is not authoritative for L1/L3/L4/L5/L7/L8.
- It also implies that a processor semantic check added under #60 would not be defence in depth.
- The two repositories' contracts then state authority differently for six of ten rules. The issue's "who implements which check" requirement is left unmet for those rules.
- No behaviour is affected today.

**Required outcome.** In section 3.1, state the authority split for the remaining model rules (L1 partition, L3, L4, L5, L7, L8) the same way the parent page does:
- parent shipping checks are authoritative for generated model content;
- processor semantic checks, including any added under #60, are defence in depth;
- generic packer checks remain authoritative for packed-image acceptance.

If the maintainer instead decides the processor is authoritative for any of these rules, record that decision and have the parent page corrected. The two contracts must not diverge.

**Verification.** Compare 07 section 3.1 side by side with `PP_DESCRIPTOR_OWNERSHIP.md:36-38` and rows `:58-65`. Every L1-L10 rule should have one stated authoritative layer, and it should be the same in both documents.

### R343-1-S1 SUGGESTION - Docs - `docs/guides/integrator.md:241-256`

- **Evidence:** The new paragraphs sit between the port table (`:239`, the "Talker sources" row `cfg_src_en_i`, `cfg_src_iface_i`, `cfg_stream_id_i`) and the existing sentence "The three per-source vectors are flat packed bit vectors" (`:256`). The nearest preceding text now names three other inputs: `talker_sources_i`, `listener_sinks_i` and `identify_index_i`. These are scalar `[15:0]` inputs (`hdl/top/protocol_processor_top.sv:185-190`).
- **Impact:** A reader can attach "the three per-source vectors" to the wrong ports. The widths make a wiring error unlikely.
- **Optional outcome:** Name the three `cfg_src_*` vectors in that sentence, or put the new paragraphs after it.
- **Verification:** Reread `:236-260`.

### R343-1-S2 SUGGESTION - Conformance, Docs - `docs/guides/integrator.md:241-243`; `docs/architecture/07_memory_maps.md:127` (L9, pre-existing)

- **Evidence:** "Zero and all-ones are invalid" carries no clause. Milan v1.2 §5.3.3.1 (printed p. 25) states it: entity_model_id "shall be a valid EUI-64 (neither all zeros nor all ones)". The L9 row cites only Milan §5.3.1, which carries only the model-change note (`receipts/clause-citations.txt`). The rule itself is correct.
- **Optional outcome:** Cite Milan §5.3.3.1 in the integrator sentence, and add it to L9's clause column.
- **Verification:** Reread both clause columns against the extracted pages.

### R343-1-S3 SUGGESTION - Conformance, Docs - `docs/architecture/07_memory_maps.md:78-84`

- **Evidence:**
  - The paragraph leaves "the product correction to the parent" but links only the #122 disposition. The parent owner, kebag-logic/milan-fpga#584 (open), was filed after the commit (PR comment 5853945556). Once #126 closes #122, the processor text has no live link to the owner of the conformance defect.
  - "dynamic mapping sets the latter to zero, not the cluster minimum" can be misread as "sets number_of_maps to zero rather than to the minimum".
- **Optional outcome:**
  - Link milan-fpga#584.
  - Reword, for example: "dynamic mapping sets `number_of_maps` to zero; it does not relax the cluster count".
- **Verification:** Reread `:78-84`.

## Required verification items

### 1. Clause reading (#122): verified; STOP is correct

I extracted only the cited pages myself (`receipts/clause-citations.txt`; the extracted text stays in unpublished scratch).

- **Milan v1.2 §5.3.3.8**, PDF p. 34 = printed p. 27 (footer verified; printed = PDF − 7, per `docs/README.md` §4): "Each Stream Port Input of a Configuration shall contain at least one AUDIO_CLUSTER descriptor." The next sentence states the output minimum. The clause has no exception.
- **Milan §5.3.3.7/§5.3.3.9**, same page: they forbid input AUDIO_MAPs (dynamic input mapping). They do not relax clusters.
- **IEEE 1722.1-2021 §7.2.13**, heading on p. 81 and Table 7-23 on p. 82 (PDF = printed): `number_of_clusters` is at offset 12, "The number of clusters within the Port."
- **Dynamic mapping:** the sentence on p. 82 says dynamic-mapping entities "set the number_of_maps field to zero (0)". It is silent on clusters. A dynamic map also needs cluster targets. So number_of_maps=0 does not waive the Milan minimum.
- **Conclusion:** F07.2's `1..*` stands.
- **Parent state:** parent D8 at `e0920d77` (`docs/ENDSTATION_BUILDER.md:248-253`) confirms the 8×8 listener ports "own zero local AUDIO_CLUSTERs".
- **No waiver from packing:** the packer accepts a zero-cluster STREAM_PORT_INPUT (informational probe row). That is exactly why packing cannot be read as a waiver, as the text says.

### 2. Enforcement statements at `493e5e4b`: all true

The packer is byte-identical between base and head (`receipts/no-code-change.txt`). Read against `hdl/aecp/desc/gen_desc_image.py`:

| Statement | Source line |
|---|---|
| Configuration gaps refused | `:450-451` |
| Per-type index gaps refused | `:344-346` |
| Duplicate keys refused | `:230-232` |
| Invalid name binding refused | `:239-290` |
| Line-buffer bound refused | `:325-329` |
| Body/key disagreement refused, both `fields` and `bytes` forms (PR #124) | `:216-222` after `descriptor_bytes` `:178-194` |
| L10 semantic check | absent |
| L6 list-shape check | absent |
| Model lint in the repository | none (#60 is open and says so) |

`scripts/probe_packer.py` exercises each statement: 20 rows, 0 mismatches (`receipts/probe_packer_head.log`).

- **Refused as documented:**
  - 577-byte descriptor (576 accepted);
  - index gap;
  - configuration gap;
  - duplicate key;
  - inline-name mismatch;
  - body type and body index mismatch in both input forms.
- **Accepted, with the mutated bytes present in the image:**
  - L10 offset 143;
  - count 9 / length 180;
  - count 3 with two words;
  - one byte short;
  - L6 lists `[1,0]` and `[1]`.
- **Accepted boundary:** eight entries.

The probes discriminate:

- **Mutant M1** removes the body/key check. It flips exactly the four body/key rows (`receipts/probe_packer_mutant_M1_no_body_key.log`).
- **Mutant M2** adds L10/L6 refusals. It flips the six "not enforced" rows. It also flips the 576-byte padding row, which pads AUDIO_UNIT beyond 144+4N and is therefore correctly refused by an exact-length check. Controls and the eight-entry boundary stay accepted (`receipts/probe_packer_mutant_M2_l6_l10.log`).

Open-owner references are accurate (`receipts/external-links.txt`, `issue89.json`):

- #89's acceptance names both L10 (item 1) and L6 (item 2).
- Parent F6 is milan-fpga#577, open.
- #123 is closed by #124 and correctly no longer listed.
- #38, #39 and #60 are open, with the stated scopes.

The author's eight enforcement observations (`pp125-r1/author/ENFORCEMENT-PROBES.txt`) agree with mine.

### 3. Ownership text vs parent page at `e0920d77`

- **Consistent:** processor generic ownership (`:89-92` vs parent `:31-34`); "allocation is not implementation" (`:92-93` vs `:33-34`); construction vs refusal; the four configuration-dependent classes (matching decision 5844867005); the AUDIO_UNIT extent; the separate 1/3-word shipping, 8-entry loader and 48/96/192 kHz conversion limits (`:130-137` vs parent rows `:67` and `:102-110`). The text follows the handoff wording, correctly updated for #124: the handoff's "does not compare the descriptor body's type/index" became an enforced statement.
- **Inconsistent:** the authority split for the remaining #60 rules (L1 partition, L3/L4/L5/L7/L8) is omitted. This is judged misleading and raised as **R343-1-M1**.

### 4. Integrator §6 `entity_model_id_i` rule: correct

- **Data path:** `entity_model_id_i` reaches only the ADPDU (`KL_adp_engine.sv:859`; no other use in `hdl/`). ENTITY bytes come from the image, so "same identity as the ENTITY bytes" is a genuine integrator obligation.
- **Zero/all-ones:** matches Milan §5.3.3.1 (see S2).
- **"New model ID on static change, subject to exclusions":** matches IEEE §6.2.2.8 (p. 50, enumerated exclusions).
- **Stream-count maxima:** match Milan §5.3.3.1.
- **Primary IDENTIFY index:** matches Milan §5.3.3.10. The processor always advertises AEM_IDENTIFY_CONTROL_INDEX_VALID (`hdl/adp/pp_adp_pkg.sv:51-53`, `0x0000C588`), so "present in every configuration" is the right obligation.

### 5. No code change; docs gates pass

- **No code change:** only two `.md` files changed. `hdl`, `tb`, `scripts`, `syn`, `.github` and `Makefile` are identical to base.
- **Gates:** `scripts/run_gates.sh` ran nine gates, all rc 0 with non-vacuous counts (`receipts/gates/gates-summary.txt`):
  - check-links (917 links);
  - check-matrix (115 REQ / 17 GAP);
  - check-integrator-params (24/24/24);
  - render-wavedrom `--check` (18 blocks);
  - make stale;
  - make lint (41 mermaid + 18 wavedrom);
  - gen_matrix `--check` (92 rows, 0 untested);
  - `git diff --check` base..head;
  - make check.

  The output matches the author's DOCS-GATES.log line for line.
- **External links:** check-links skips them, so I resolved each one read-only: the #122 comment, parent blob `e0920d77` (resolves to `e0920d77162284d8...`), and #38/#39/#60/#89.
- **Anchor:** `07_memory_maps.md#31-descriptor-tree` from the integrator guide is covered by check-links.

## Per-lens results

```text
[R343] UNCLEAN Conformance - 07_memory_maps.md:78-137 vs Milan §5.3.3.1/.7/.8/.9/.10, IEEE §6.2.2.8, §7.2.13 Table 7-23, PP_DESCRIPTOR_OWNERSHIP.md@e0920d77, decision 5844867005, #89 acceptance - clause reading and STOP correct; enforcement statements true; authority split for L1/L3/L4/L5/L7/L8 omitted (M1)
[R343] CLEAN   RTL - no HDL/tb/syn change (receipts/no-code-change.txt); integrator ports traced: protocol_processor_top.sv:183-190,1651-1658 -> KL_adp_engine.sv:110-117,859-871; ADP caps pp_adp_pkg.sv:51-53 - the text matches the data path
[R343] CLEAN   Robustness - packer fail-closed paths gen_desc_image.py:178-235,325-346,450; 20 probes with byte survival; mutants M1/M2 discriminate; the zero-cluster port packs (documented as not a waiver)
[R343] CLEAN   Tests - tb/desc_store/test_gen_desc_image.py 6/6 OK (receipts/test_gen_desc_image.log); reviewer probe bank 20/0 and mutation flips; docs-only change needs no new test
[R343] UNCLEAN Docs - 07 section 3.1 and integrator §6; nine docs gates rc 0; external links resolved - M1 open; S1-S3 are suggestions
```

## Completion ledger (reviewer-owned)

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (M1) | Milan v1.2 pp. 31/32/34/35 and IEEE 1722.1-2021 pp. 50/81/82 (cited pages only); 07 §3.1; parent ownership page `e0920d77`; decision 5844867005; #509 handoff wording; R331-1 S4; issues #38/#39/#60/#89/#122/#123/#125; parent D8, #577, #584 | R343-1 | `1d249e6e18a91c16a2620904483634548b0414a6` |
| RTL | CLEAN | No RTL in diff; top/ADP port path and capability constant traced for the integrator rules | R343-1 | `1d249e6e18a91c16a2620904483634548b0414a6` |
| Robustness | CLEAN | Packer refusal paths; 20-row probe bank with byte-survival check; mutants M1/M2 | R343-1 | `1d249e6e18a91c16a2620904483634548b0414a6` |
| Tests | CLEAN | Packer unit tests 6/6; probe bank; mutation discrimination; author enforcement observations cross-checked | R343-1 | `1d249e6e18a91c16a2620904483634548b0414a6` |
| Docs | UNCLEAN (M1) | 07 and integrator diff; docs/README conventions; 9 docs gates; external links; S1-S3 | R343-1 | `1d249e6e18a91c16a2620904483634548b0414a6` |

## Limits

- **RTL simulation not run.** The assigned pinned Verilator 5.050 path (`$VALIDATION_STORAGE/372-manager-candidate1/pinned-tool-bin/verilator`) does not exist on this host; its parent directory is absent. I did not substitute the unpinned system build (5.052). The RTL lens rests on the byte-identical HDL tree and source tracing. No descriptor-store simulation was executed by this reviewer.
- **Manager banks not visible.** No manager bank-result comment exists on #125 or #126, and the public evidence tree `pp125-r1` holds only author artifacts (docs-gates log, enforcement observations, handoff, #122 report, PR body, review-ready). I could not inspect the full static/builder/native bank results stated in the assignment, and I did not re-run them (excluded).
- **Hosted checks at the exact head** when read (`receipts/hosted-checks-1d249e6e.txt`): docs-gates ×2 and portability ×2 completed success; suites ×2 still `in_progress`; the combined status context was `pending` with 0 statuses. I did not wait for or accept them.
- **Standards:** only the cited pages were extracted; standard text is limited to one-sentence citations. The #509 handoff and R331-1 were read from public artifacts. The #509 decision and the parent page were read at the stated commits.
- **Out of scope:** physical calibration was not run, and no hardware or field claim is made. Multi-configuration behaviour is untested by anyone; the parent emits one configuration per image.
- **Review clone restored:** after the gates, `.venv-wavedrom/` was removed. Final state (`receipts/clone_integrity.txt`):
  - HEAD and tree exact;
  - index tree equals HEAD tree;
  - 249 entries rehash with 0 blob or mode mismatches;
  - 0 non-`H` index flags;
  - 0 status lines including ignored;
  - no gitlinks in this repository's tree, so no submodules are required.

## Pending manager duties

- Route M1 to the executor. R331-1 S4 is now carried as R343-1-M1. Decide whether S1-S3 are taken in the same round.
- Publish or link the manager's source static/builder and native bank receipts at this head; they are not in the public tree or comments yet.
- Hosted acceptance at the exact head, including the in-progress `suites` contexts.
- Final current-dev candidate at the merge turn (source base `493e5e4b`, live dev `e0920d77`).
- Parent follow-through on milan-fpga#584 (zero-cluster inputs) and #577 (F6).
- Merge authorization, containment and board state.

R343-1 FINISHED
