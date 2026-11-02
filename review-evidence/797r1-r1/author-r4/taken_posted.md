[A711d] TAKEN
Branch: `797-r1-regref` (PR #825), from head `e90284bd0896067eba6f10b3e5b0e534c9b0e017`. Local commits only; nothing is pushed from this lane.
Authoritative references: R753-3 F1 and R754-3 F1 on PR #825, both NEGATIVE at `e90284bd`; section 2 of issuecomment-6522974767; `hdl/common/csr/milan_csr.sv` at the `STRMW_SRP` and `RENDER_STAT` read decodes.
Interpreted scope: state the `STRMW_SRP` index-0 condition by the value of `STRM_SEL[9]` (R753-3 F1), and make the `RENDER_STAT` read table true at any `N_LISTENERS_P` (R754-3 F1). Extend the read-table sweep to all 17 read tables on the shipping and the 2x2 build, map every clause to what the page prints, report disagreements per table and fix any row it finds false. One commit per finding plus one for the sweep. No new gate, no new diagram, no text moved between pages, no RTL change, no dev merge. Suggestions not taken.
Validation plan: every `run:` step of `.github/workflows/docs.yml` that can run outside GitHub, `gen_register_reference.py --selftest` and `--check`, `git diff --check 1f29f189 HEAD` and one merge base, on a clean clone of the committed head, each log and rc in the receipts.
Blockers: none.
Posted: issuecomment-6573241681
