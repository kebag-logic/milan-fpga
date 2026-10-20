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

