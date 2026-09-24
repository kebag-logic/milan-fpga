# [A226] handoff: PR #537 correction round 1 (R274-1 / R275-1 F1 and F2)

Lane: `$LANES/394-510-511-decisions`, branch `394-510-511-decisions`.

| Item | Value |
|---|---|
| Base | `759da623072358afdb0e9d570a7b4b6a788492c9` |
| Reviewed head (R274-1, R275-1) | `64bcf768d28b4b9763fbe5917a734bcefa2a66e0` |
| New head | `70f2c50d45550f65c9d71ed0f5b0d70dc48acdb6`, tree `ef96bf2fe0d66dd9c0b1ba45c6b4300d89ba658c` |
| Pushed? | No. The push, the PR body update and the merge belong to the manager, per the brief |

## Commit (one-line subject, no trailers)

| SHA | Subject |
|---|---|
| `70f2c50d45550f65c9d71ed0f5b0d70dc48acdb6` | Name every delayAsymmetry term in the #511 record, state its Table 14-6 grade and add the 802.1AS management revisit condition |

The commit touches Markdown only: 4 files, +40/-9. There is no RTL, firmware, builder, configuration, test or gitlink change (`receipts/scope-and-proof-plan.txt`).

## What was fixed

### F1 (Conformance, Docs): every place delayAsymmetry enters the arithmetic

The findings are R274-1 F1 and R275-1 F1. `docs/design/GPTP_PLANE.md` changes in three places:

- **The "Where would it enter?" row** now says "three terms". Its authority cell cites Figure 10-9's two assignments.
- **A new table, "#### Where the term enters",** lists the arithmetic:
  - 11.2.13.2.1 f) `upstreamTxTime` subtracts `delayAsymmetry/rateRatio`. 11.1.3 d) describes it.
  - 10.2.12 Figure 10-9 `syncReceiptTime` adds `+delayAsymmetry`.
  - 10.2.12 Figure 10-9 `syncReceiptLocalTime` adds `+delayAsymmetry/rateRatio`. That undoes the f) subtraction, to within the Figure 10-4 `neighborRateRatio` update, which NOTE 2 of 11.2.13.2.1 calls usually negligible.
  - 11.2.14.2.3 a) `setFollowUp()` carries the first term into a relayed Follow_Up `correctionField`. 11.1.3 e) and Table 11-5 describe this. Only a port that relays another port's Sync does it (10.2.11 `localPortNumber != thisPort`). A grandmaster-sourced Sync has `upstreamTxTime = localTime` (10.2.8.2.1 g)). So a one-port end station never carries the term.
  - Annex E.5.2.2 (CSN): not applicable, because there is no CSN port (AS-11).
  - An 802.1AS-2020 comparison row: the same terms at 10.2.13, 11.2.14.2.1 and 11.2.15.2.3. With CMLDS, 11.2.17.2 a) folds the term into the mean link delay.

  Two short statements follow the table:
  - Net effect: `syncReceiptTime` gains `delayAsymmetry`, and its paired local time does not move.
  - An adoption that omits the `syncReceiptLocalTime` term roughly doubles the shift.
- **The "Application point" row** in "What an adoption must define" now names all three terms, notes the 11.2.14.2.3 inheritance, and keeps "never `computePropTime()`".

### F2 (Conformance, Docs): Table 14-6 and the management revisit condition

The findings are R274-1 F2 and R275-1 F2.

- **The `GPTP_PLANE.md` "Is it managed?" row** now states Table 14-6 (14.6.25). Cor1's replacement table keeps this row.
  - Operations: read-write.
  - Conformance: `Tdot3FD`, "Required for time-aware IEEE 802.3 full-duplex port".
  - So such a port must carry the object wherever 802.1AS management is implemented.
  - "(recommended)" qualifies the `scaledNs` data type. 14.3.2 states the same pattern for `offsetFromMaster`.
  - 14.6.9 defines the object without grading it.
  - PICS `MGT` (A.5) is `O`. The product claims no 802.1AS management.
- **The `GPTP_PLANE.md` revisit trigger** gains three statements:
  - "Revisit also before the product claims 802.1AS management."
  - "Table 14-6 then requires a read-write `delayAsymmetry` object."
  - "Check this before the P4 802.1AS conformance run." The README roadmap lists that item under P4.

  It also gains "A write to that managed object is one such correction", tying the object to the REQ-PTP-06 amendment.
- **Three more pages carry the same management condition:**
  - the `REQUIREMENTS.md` REQ-PTP-06 scope note, as R274-1 and R275-1 require;
  - the `docs/reference/FR_NFR.md` Section 5 out-of-scope entry. It restated the trigger ("revisit before a second cabled port"), so leaving it would have kept an incomplete copy;
  - the `docs/reference/MILAN_COMPLIANCE_MATRIX.md` Section 4 row. It cites 14.6.9 next to "optional to model", so it now states the Table 14-6 grade and that no management is claimed.
- **The optional R274-1 point is taken.** The "Units" row cites Table 14-6 for `scaledNs`, because 10.2.4.8 names no data type.

### Deliberately unchanged

- **The adoption proof plan** ("#### What an adoption must prove" through the ownership table) is byte-identical to `64bcf768`, sha256 `5efb6309...0ce3` at both heads. So no arm the Tests lens covered has changed. It starts at line 426 at the new head, shifted by the inserted rows.
- **The SUGGESTIONs** are not taken, because the brief limits this round to the two MINORs and all of them are optional:
  - R275-1 S2: gate AS-13.
  - R275-1 S3 = R274-1 S1: a builder test with an asymmetry key.
  - R275-1 S4: label AS-13's edition.
- **The held files are untouched:** `CHANGELOG.md`, `docs/integration/BAREMETAL_FIRMWARE.md` and the builder page. The brief names the builder page `docs/design/ENDSTATION_BUILDER.md`, but the tree holds it at `docs/ENDSTATION_BUILDER.md`.

## Validation (receipts/gates-at-head.txt)

Every command exits 0 at `70f2c50d`, with the submodules at their gitlinks:

- **Base docs gates:**
  - `docs_check` reports 0 findings.
  - `check_em_dash --base 759da623` reports 0 findings over 230 lines in 11 pages. `--base 64bcf768` reports 0 over 40 lines in 4 pages.
  - `check_feature_status --self-test` passes 46/46.
  - `check_baremetal_only` passes `--check`, and `--selftest` passes 377 arms.
  - `gen_module_matrix --check` passes.
- **Style and gPTP gates:**
  - `check_gptp_docs` passes plain and `--with-submodule`, and `--selftest` passes 30 controls.
  - `check_doc_style` passes, and `--selftest` passes.
- **TOC, paths and submodules:**
  - `gen_toc` passes `--check` and `--verify-anchors`.
  - `check_doc_paths` passes.
  - `check_submodule_docs` passes, and `--selftest` passes.
- **Solution, diagram and wire gates:**
  - `check_solution_docs` passes, and `--selftest` passes.
  - `DOC_MAP.gen.py --check`, `timesync_chain.gen.py --check`, `submodule_boundaries.gen.py --check` and `check_diagram_pngs` all pass.
  - `check_wire_accountability` runs 42 checks with 0 findings.
- **Whitespace:** `git diff --check` is clean against both `759da623` and `64bcf768`.

The first `check_doc_style` run found one 11-word sentence in the new table's lead. It was reworded before the commit.

Not run at this head:

- **`sw/builder/test_builder.py`.** The four changed pages are named in code only in the style and gPTP gates' page lists, a docstring (`check_wire_accountability.py:96`) and a comment (`test_builder.py:23971`). The builder reads none of them. [A215]'s `64bcf768` result, `ALL GATES PASS EXCEPT 1 NOT RUN`, still describes it.
- **The pp_top run.** The processor pin `424c688` is unchanged.
- **Hosted CI and act.** Nothing is pushed.

## Clause evidence (receipts/standards-clause-receipts.txt)

- The receipt holds line-numbered `pdftotext -layout` excerpts of the local 802.1AS-2011, Cor1-2013, Cor2-2015 and 2020 PDFs, with the PDFs' sha256.
- It lists every `delayAsymmetry` hit in 2011. The arithmetic ones are 2130/2132 (the 8.3 definition), 4615/4617, 6917/6930, 7399 and Table 11-5 at 8472. The others are definitions, notes, management, MIB, PICS and Annex E.
- Cor2 has 0 delayAsymmetry hits.
- Cor1 changes 10.2.12.2.1 prose only, not Figure 10-9. It restates 11.2.13.2.1 f) unchanged and replaces Table 14-6 with an identical delayAsymmetry row.

## Posted

- #511: `[A226] REVIEW READY` (source `comments/511-review-ready.md`; URL in `comments/posted-511.url`).
- Nothing was posted on the PR, and the PR was not edited. `PR-BODY.md` is ready for the manager to apply.

## For the manager

1. Push `70f2c50d` and replace the PR body with `PR-BODY.md`. Then run the R274 and R275 re-review. The changed files are Conformance and Docs scope only. The proof plan and every gate are unchanged.
2. Get the owner to confirm or replace the #511 revisit trigger. It now has three conditions: a second cabled port, a claim of 802.1AS management, and a REQ-PTP-06 amendment before any runtime correction.
3. The [A215] #511 REVIEW READY's two superseded statements are annotated in the [A226] REVIEW READY on #511.
4. The out-of-diff items from R274-1/R275-1 "Pending manager duties" are unchanged by this round. They include the `aecp_response_contract.feature` GET_MILAN_INFO item and keeping #394 and #510 open.

## Worktree state

- Tracked files are clean, and the three submodules sit clean at their gitlinks.
- The only files modified this session are the four committed pages.
- Ignored artifacts predate this session and were left untouched: `__pycache__` directories, `configs/generated/*.hex` and `sw/builder/out/`, all timestamped 2026-09-23 21:10-21:46 CEST.
- The standards text extractions are in `/tmp/a226-std`, outside the repository and the packet, and are not committed.
