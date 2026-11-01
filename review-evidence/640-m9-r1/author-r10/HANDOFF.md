# [A10] HANDOFF: PR #828 round 10

One commit over `d63b378d`, by the manager, 4 pages, 13 lines added. No figure changes.

| Finding | Change |
|---|---|
| R757-10-F1 | `docs/design/MAILBOX_SPLIT.md`: "It keeps the gPTP plane until F6, then firmware owns the protocol and servo." |
| R758-10-R1 | `docs/traceability/ieee8021q.md`: the MRP text continues the Reservation bullet, and the Mark II sentences are their own paragraph |
| R758-10-R2 | `docs/design/AREA_BUDGET.md`: the three lines say "at 32x32" |
| R758-10-R3 | `docs/design/AREA_BUDGET.md`: "The next three sentences are history, against the replaced 60 percent." |
| R758-10-R4 | `docs/guides/gptp/MANAGER.md`: scoped to the fabric plane until F6, with the split contract linked; shortened, and given its own paragraph, to pass the style gate |

The same phrasing was searched over the tree: the other hits (`README.md`, `docs/overview/FULL_FPGA_SOLUTION.md`, `docs/overview/ARCHITECTURE.md`, `docs/integration/AXIS_CORES_ON_BAREMETAL_SOC.md`) say "until F6", `docs/reference/FR_NFR.md:328` is the scoped requirement, and `docs/findings/451_TDM8_FIRST_LIGHT.md` is a dated finding about another clock.

Gates on the head, rc 0: `check_doc_style.py`, `docs_check.py`, `check_gptp_docs.py`, `gen_toc.py --check`, `check_em_dash.py --base 1f29f189`, `check_feature_status.py`, `check_doc_paths.py`, `check_baremetal_only.py --check`, `ctrl_service_bounds.py` (the mailbox page's reader), `pp_resource_gate.py check-baseline`, `git diff --check`. The local replay and hosted workflows run the rest at this head.
