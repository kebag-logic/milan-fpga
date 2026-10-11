https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/pull/174#issuecomment-6107310880
**R609-2-F1 — MINOR — Docs — semantic export fields described as prose-only**

- **Where:** `hdl/aecp/ucode/aecp_commands.json:28`; `docs/architecture/09_verification.md:540`; PR #174, field-reference description. Data begins at `aecp_commands.json:426`; readers are `scripts/aecp_gate/rtl.py:134` and `scripts/aecp_gate/record.py:393`.
- **Authority/evidence:** the frozen scope names this JSON as the parent export; round two requires the docs to describe exactly what the gate holds. The reference classifies the whole `documented` collection as “F06.14 prose only: no consumer reads them as machine semantics.” Six rows actually supply otherwise-unserved legal GET_DYNAMIC_INFO members. `scripts/probe_export_fields.py` changes GET_VIDEO_FORMAT's `gdi`, `rtl`, then `opcode`, regenerating F06.14 each time. All three edits produce semantic `decode:` or `engine:` failures, with no F06.14 mismatch. `receipts/export-fields.log` retains the output.
- **Impact:** a consumer following the reference could discard six GDI membership rows as presentation data or treat edits to them as semantically inert. The gate itself correctly protects the fields; no current RTL malfunction is claimed. This is an incorrect machine-field contract in the exported model, not harmless editorial residue.
- **Required outcome:** remove the blanket prose-only classification. Describe `documented[].opcode`, optional `rtl`, and optional `gdi` as semantic inputs for the unimplemented GDI members; distinguish identity/diagnostic fields from `section`/`cells` rendering data. Make 09 §8.10 and the PR field-reference description agree. No production RTL change is needed.
- **Verification:** the reference identifies the existing readers and six rows accurately; `make aecpcmd` passes; the three controls still fail semantically when planted. Do not imply that dropping the whole collection preserves GDI semantics.

**R609-2-R1 — RESIDUE — Docs — stale publication wording**

- **Artifact:** PR #174, Validation introduction: “All results below are local at those commits; the new commits have not been pushed.”
- **Evidence:** the PR API names the exact reviewed commit as its published head (`receipts/pr-wording.txt`).
- **Impact:** publication-status wording only; no measurement, test, code, generated artifact or conformance claim changes.
- **Exact fix:** replace the sentence with “All results below were run locally at those commits.”
- **Verification:** manager residue checklist confirms the replacement. This does not affect the verdict or add an unclean lens.

