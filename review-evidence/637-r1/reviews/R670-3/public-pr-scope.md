https://github.com/kebag-logic/milan-fpga/pull/768#issuecomment-6268143552

[A10] INDEPENDENT REVIEW STARTED: R669-1

R669 (internal reviewer) reconstructs issue #637 / PR #768 at exact head `63a187e1579474bca562d85304b9a91466877c33`, tree `45c859e17681896f2fa3db26c04de75ef9f125d4`, in a cleared context from public scope, requirements, diff and evidence, applying all five lenses with a reviewer-owned ledger. Owner decision 2026-09-23: while the previously assigned internal review system is at its usage limit, the internal role runs as a separate cleared-context independent session with its own clone; the two reviews stay independent. No source edits or merge while this review runs; merge still requires two independent positive reviews and the full completion bar.


https://github.com/kebag-logic/milan-fpga/pull/768#issuecomment-6269551811

[A10] INDEPENDENT REVIEW STARTED: R670-1

R670 (external reviewer) reconstructs issue #637 / PR #768 at exact head `63a187e1579474bca562d85304b9a91466877c33`, tree `45c859e17681896f2fa3db26c04de75ef9f125d4`, in a cleared context from public scope, requirements, diff and evidence, applying all five lenses with a reviewer-owned ledger. No source edits or merge while this review runs; merge still requires two independent positive reviews and the full completion bar.


https://github.com/kebag-logic/milan-fpga/pull/768#issuecomment-6269988820

[A10] Round 2 assignment for [A656], head 63a187e1. It answers R669-1 (issuecomment-6268811441) and R670-1 (issuecomment-6269970193).

**Rulings first**

- **The one-pass restore is accepted** (R670-F6). This answers the open risk in the REVIEW READY comment. Conditions:
  - one read pass, with every map rolled back to its reset set on any failure;
  - no controller can see a partial set, because every face stays held until the restore ends.

  With those, the outcome equals the two-pass transaction. Amend the D3 decision text (section 3 / 18.4) to this transaction, citing this comment. State the validation obligation for one pass and its deadlines, and state the map-only transaction boundary explicitly. The two-pass requirement no longer applies to the map records.
- **Cross-port ownership: fix it** (R670-F2, R669-F5). A documented limitation is refused. The final state of a saved configuration must be restored whatever the port order (Milan v1.2 5.3.10.1). For example, first take down every reset set a valid saved record replaces, then put the saved sets back. The roll-back keeps covering every port.

**Work items**

1. **Status** (R670-F1, R669-F1, with S2). PP_STAT tells the truth about the composed restore under the D3 rules:
   - `[3]` failed includes a failed map walk;
   - `[7]` blank only when neither the processor nor the map walk validated a record and neither failed;
   - `[1]` restore_busy covers the map restore.

   This is parent-side composition only; the processor interface does not change. Write public-register assertions for: blank boot, saved maps, device error, both deadline paths and refused put-back. Each needs a control that disconnects the outcome.
2. **Cross-port fix** (ruling above). Real multi-port save, reset and restore with:
   - transfers in both port orders;
   - a cyclic swap.

   Grade GET, ownership and routing, with a control that restores the current ordering.
3. **Restore arms** (R670-F3, R669-F2). Committed checks with killing controls, on the real restore path, for: put-back, holes, layout/id, ranges, conflicting keys and pass-0 DEFAULTS. Include the directional and port-boundary coverage of 18.4.
4. **Gates** (R670-F4, R669-F3/F4). Every required docs-workflow gate and self-test passes at the head, without loosening a ratchet. Justify the literal-bound port. The validation account separates executed, skipped and cancelled work.
5. **Docs** (R670-F5, R669-F6). PP_STAT `[4]` names the parent map writer (#637), with its three-attempt, reset-sticky semantics.
6. **Residue** (R669-R1 to R3): apply as written. R669-S1 goes into 18.4 as one sentence. S3 is not assigned.

**Base and scope**

- Merge dev e26f1816 into the branch first. It carries #763 (PR #766), which touches the same dynamic-map paths. Use a merge commit, no rebase. Then re-run the full gate list, dynmap and dynmap-mutants, route-1x1 and ooc at the new head.
- STOP on any processor register-map, top-level port or parameter change.


https://github.com/kebag-logic/milan-fpga/pull/768#issuecomment-6294832626

[A10] INDEPENDENT REVIEW STARTED: R669-2

R669 (internal reviewer) reconstructs issue #637 / PR #768 at exact head `8000520cc12ec5d107a2a67f8ba3d6134b87d2b5`, tree `fc876150e72e530d5c4122f04c3ec89700523b2a`, in a cleared context from public scope, requirements, diff and evidence, applying all five lenses with a reviewer-owned ledger. Owner decision 2026-09-23: while the previously assigned internal review system is at its usage limit, the internal role runs as a separate cleared-context independent session with its own clone; the two reviews stay independent. No source edits or merge while this review runs; merge still requires two independent positive reviews and the full completion bar.


https://github.com/kebag-logic/milan-fpga/pull/768#issuecomment-6294842809

[A10] INDEPENDENT REVIEW STARTED: R670-2

R670 (external reviewer) reconstructs issue #637 / PR #768 at exact head `8000520cc12ec5d107a2a67f8ba3d6134b87d2b5`, tree `fc876150e72e530d5c4122f04c3ec89700523b2a`, in a cleared context from public scope, requirements, diff and evidence, applying all five lenses with a reviewer-owned ledger. No source edits or merge while this review runs; merge still requires two independent positive reviews and the full completion bar.


https://github.com/kebag-logic/milan-fpga/pull/768#issuecomment-6295599722

[A10] Round 3 assignment for [A656], head 8000520c. It answers R669-2 (issuecomment-6295588258) and R670-2 (issuecomment-6295076402). No RTL change is expected.

1. **R669-2-F1 (tests).** The committed `[MAPREC]` section grades PP_STAT blank 1, fail 0 and done 1 for a window whose only record is a framed map record that fails the validated test, with at least one CRC case and one layout-or-id case (D3 section 3 rule 7). Plant controls that remove the CRC term and the layout/id term of `amr_rs_valid_r`; each must be caught. A magic/length-term control is optional.
2. **R669-2-F2 (docs).** `docs/reference/REGISTER_MAP.md:2378` and the PP_STAT `[3]` row at `:2401`, and `docs/design/SAVED_STATE_MATERIALIZATION.md:1499-1500`, state what holds when the binding walk also failed. For example: the map restore adds no cause of its own; `[20:18]` reads 0 because the D3 walk ended COMPLETE, and `[22:21]` keeps the binding walk's.
3. **R670-2-F1 (validation account).** The PR body, HANDOFF and the issue record separate:
   - the full mutation campaign (rc 2, 63/65 checks passed);
   - the listener re-run (rc 0, 2/2);
   - the aggregate: 60/60 mutations caught and five clean legs passed across those executions.

   Keep the synthesis rc 0 separate and link both receipts.
4. **Residue** from both reviews goes to the checklist at merge. Do not apply it unless it falls inside an edit you already make.

New commits on 8000520c (no rebase, no amend). Re-run `milan_dp` dynmap and maprec legs, dynmap-mutants, the docs gates, and the builder bank.


https://github.com/kebag-logic/milan-fpga/pull/768#issuecomment-6298509526

[A10] INDEPENDENT REVIEW STARTED: R669-3

R669 (internal reviewer) reconstructs issue #637 / PR #768 at exact head `1e914414557874648ac5041aff88b96908e0e053`, tree `033e6bc1fb66904e7faf7b57929d6c7a28d89732`, in a cleared context from public scope, requirements, diff and evidence, applying all five lenses with a reviewer-owned ledger. Owner decision 2026-09-23: while the previously assigned internal review system is at its usage limit, the internal role runs as a separate cleared-context independent session with its own clone; the two reviews stay independent. No source edits or merge while this review runs; merge still requires two independent positive reviews and the full completion bar.


https://github.com/kebag-logic/milan-fpga/pull/768#issuecomment-6298519097

[A10] INDEPENDENT REVIEW STARTED: R670-3

R670 (external reviewer) reconstructs issue #637 / PR #768 at exact head `1e914414557874648ac5041aff88b96908e0e053`, tree `033e6bc1fb66904e7faf7b57929d6c7a28d89732`, in a cleared context from public scope, requirements, diff and evidence, applying all five lenses with a reviewer-owned ledger. No source edits or merge while this review runs; merge still requires two independent positive reviews and the full completion bar.
