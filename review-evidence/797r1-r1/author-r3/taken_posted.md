[A711c] TAKEN
Branch: `797-r1-regref` (PR #825), from head `96bfa8513978ebc8c2f2e73bd98914b56e84bf12`. Local commits only; nothing is pushed from this lane.
Authoritative references: R753-2 and R754-2 on PR #825, both NEGATIVE at `96bfa851`; section 2 of issuecomment-6522974767; `hdl/common/csr/milan_csr.sv`; the firmware, SoC and processor lines those reports cite.
Interpreted scope: statement fixes only. `MAC_STATUS` publication, the entity-enable request, the REBOOT hold on `milan_mac_phy_crg_reset`, read-condition grouping (generator fix with a selftest arm), `ADP_CMD` strobes, `PP_NVM_STAT` strobe rows with a control, `STRM_SEL[9]` at `[8]` = 1, and every residue. One commit per finding group. No text moves to other pages, no new gate, no new diagram, no RTL change.
Validation plan: every `run:` step of `.github/workflows/docs.yml`, `gen_register_reference.py --selftest` and `git diff --check` against the merge base, on a clean clone of the committed head, each log and rc in the receipts.
Blockers: none.
