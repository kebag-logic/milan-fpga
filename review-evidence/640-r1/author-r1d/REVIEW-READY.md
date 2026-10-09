[A540] REVIEW READY - Round 1d

Commit: `7387bb6f6ae98f3e1d2e4a1f62c2c66f094fe783`
Branch: `640-mark2-plan`; PR #698.
Assignment: [6081895732](https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-6081895732).
Two new commits after `39258a1486897127288f82fbb1b86333febf6f00`; no rebase or amend.

Changed: `docs/design/MARK_II_AREA_PLAN.md` and `docs/design/AREA_BUDGET.md` only.

| Step | Result | Commit |
|---|---|---|
| 1 | Owner decision, F5 preflight, memory ledger, reclamation order and checkpoint duties mirrored | `9b6a04e10499b060eb25dc7c3d489e03c177c566` |
| 2 | RAM arithmetic recomputed; equation and unchanged LUT estimates recorded | `7387bb6f6ae98f3e1d2e4a1f62c2c66f094fe783` |

The [owner decision](https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-6081706413) is incorporated: 224 KB for F5, including AECP, budgeted at about 50 RAMB36 tiles.
The [preflight](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6081556432) measured 94,688 bytes for shipping 1x1 with one interface and 147,360 for the largest shape with two interfaces, before AECP.
Its BSS includes static pools; the plan counts them once.

The source baseline remains `a5ca6e5110d515bf5f894f87b94f9bf6f6836bbb`, carried by dev `5603c353`.
The recorded route uses 74 RAMB36 and 27 RAMB18, or 87.5 tiles.
The ledger is `87.5 - 6.5 + 6 - 18.5 + 50 + 2 = 120.5` tiles.
The 18.5-tile CPU-memory reuse is explicitly a historical census estimate.
It must be confirmed at the implementation checkpoint.

Eleven additional wrapper tiles are named as conditional reclamation.
They cover five RX pools, MRP strip, TX slots, timer, trace, validator and control FIFO.
Their release gives 109.5 tiles; replacement buffers must be debited.
If further memory is needed, M2/M6/M7 conversions yield and their LUT savings are repriced.
Diagnostics and protocol capacities remain required.
The usable ceiling stays 121.5, preserving the separate 13.5-tile reserve.

A 4 KiB usable mapping needs 56 tiles for 224 KiB.
That illustration gives 115.5 tiles after conditional reclamation, before unpriced buffers.
Partial placement with the same 50-tile hold gives 126.5 before extra fabric-AECP staging.
It cannot borrow full-split reclamation; M0s must report the actual allocation.
These estimates establish no routed fit or new firmware byte threshold.

Both M0s routes, the default flip and M9 report RAMB36/RAMB18 against the ledger.
The [F5/default-flip duties](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6081705916) include the four shape/interface combinations and five largest BSS consumers with reduction options.
The default flip requires routed LUT, FF and RAMB36 evidence with firmware in block RAM and the reserve intact.
The LUT estimate stays 31,667 centrally, spanning 27,567-35,867.

Validation at the head: **51/51 commands returned 0**.
The campaign used eight concurrent workers, separate logs/rc files and no pipes.
The resource self-test passed 260 arms and 500 generated cases.
Its control passed and all 174 mutants were rejected.
Arithmetic checks passed 174 LUT checks, 54 scenario cells and 80 memory cells.
The new checker verifies the disjoint release partition and the reserve calculations.
The resource record and policy values are unchanged.

The exact command table follows. It uses the pinned Markdown environment and initialized submodules.
`EVIDENCE` denotes the packet directory containing the three arithmetic scripts.

| Gate | Command | rc |
|---|---|---:|
| docs_check | `rtk proxy python3 scripts/docs_check.py` | 0 |
| docs_self | `rtk proxy python3 scripts/docs_check.py --selftest` | 0 |
| feature_status | `rtk proxy python3 scripts/check_feature_status.py` | 0 |
| feature_self | `rtk proxy python3 scripts/check_feature_status.py --self-test` | 0 |
| em_dash | `rtk proxy python3 scripts/check_em_dash.py --base 5603c353137e90c1fa95429f6d00ef7a2298d9ee` | 0 |
| em_dash_self | `rtk proxy python3 scripts/check_em_dash.py --selftest` | 0 |
| doc_style | `rtk proxy python3 scripts/check_doc_style.py` | 0 |
| doc_style_self | `rtk proxy python3 scripts/check_doc_style.py --selftest` | 0 |
| gptp_docs | `rtk proxy python3 scripts/check_gptp_docs.py --with-submodule` | 0 |
| gptp_docs_self | `rtk proxy python3 scripts/check_gptp_docs.py --selftest` | 0 |
| doc_map | `rtk proxy python3 docs/DOC_MAP.gen.py --check` | 0 |
| doc_map_self | `rtk proxy python3 docs/DOC_MAP.gen.py --selftest` | 0 |
| timesync | `rtk proxy python3 docs/diagrams/timesync_chain.gen.py --check` | 0 |
| timesync_self | `rtk proxy python3 docs/diagrams/timesync_chain.gen.py --selftest` | 0 |
| solution | `rtk proxy python3 scripts/check_solution_docs.py` | 0 |
| solution_self | `rtk proxy python3 scripts/check_solution_docs.py --selftest` | 0 |
| submodule_diagram | `rtk proxy python3 docs/diagrams/submodule_boundaries.gen.py --check` | 0 |
| submodule_diagram_self | `rtk proxy python3 docs/diagrams/submodule_boundaries.gen.py --selftest` | 0 |
| submodule_docs | `rtk proxy python3 scripts/check_submodule_docs.py` | 0 |
| submodule_docs_self | `rtk proxy python3 scripts/check_submodule_docs.py --selftest` | 0 |
| diagram_pngs | `rtk proxy python3 scripts/check_diagram_pngs.py` | 0 |
| diagram_pngs_self | `rtk proxy python3 scripts/check_diagram_pngs.py --selftest` | 0 |
| module_matrix | `rtk proxy python3 docs/traceability/gen_module_matrix.py --check` | 0 |
| baremetal | `rtk proxy python3 scripts/check_baremetal_only.py --check` | 0 |
| baremetal_self | `rtk proxy python3 scripts/check_baremetal_only.py --selftest` | 0 |
| doc_paths | `rtk proxy python3 scripts/check_doc_paths.py` | 0 |
| archive | `rtk proxy python3 scripts/check_archive.py` | 0 |
| archive_self | `rtk proxy python3 scripts/check_archive.py --selftest` | 0 |
| toc_self | `rtk proxy python3 scripts/gen_toc.py --selftest` | 0 |
| toc_anchors | `rtk proxy python3 scripts/gen_toc.py --verify-anchors` | 0 |
| toc_check | `rtk proxy python3 scripts/gen_toc.py --check` | 0 |
| todo | `rtk proxy python3 scripts/check_todo_ownership.py` | 0 |
| hygiene | `rtk proxy python3 scripts/check_hygiene.py --check` | 0 |
| wire | `rtk proxy python3 scripts/check_wire_accountability.py --self-test` | 0 |
| resource_baseline | `rtk proxy python3 syn/ooc/pp_resource_gate.py check-baseline` | 0 |
| resource_self | `rtk proxy python3 syn/ooc/pp_resource_gate.py --selftest` | 0 |
| resource_mutants | `rtk proxy python3 syn/ooc/pp_resource_gate_mutants.py` | 0 |
| ci_scope | `rtk proxy python3 scripts/ci_scope.py --selftest` | 0 |
| ci_events | `rtk proxy python3 scripts/ci_events.py --check` | 0 |
| wavedrom_self | `rtk proxy python3 scripts/gen_wavedrom.py --selftest` | 0 |
| wavedrom_axis | `rtk proxy python3 scripts/gen_wavedrom.py docs/diagrams/wd_axis_backpressure.json --background=white --check` | 0 |
| wavedrom_cdc | `rtk proxy python3 scripts/gen_wavedrom.py docs/diagrams/wd_cdc_handshake.json --background=white --check` | 0 |
| wavedrom_gptp | `rtk proxy python3 scripts/gen_wavedrom.py docs/diagrams/wd_gptp_pdelay.json --background=white --check` | 0 |
| pp_sources | `rtk proxy python3 scripts/pp_srcs.py --check --selftest` | 0 |
| docs_nogit | `rtk proxy env GIT_DIR=/dev/null python3 scripts/docs_check.py` | 0 |
| gptp_make | `rtk proxy make -j16 -C gptp-processor docs` | 0 |
| diff_base | `rtk proxy git diff --check 5603c353137e90c1fa95429f6d00ef7a2298d9ee HEAD` | 0 |
| diff_tree | `rtk proxy git diff --check` | 0 |
| recompute_ledger | `rtk proxy python3 "$EVIDENCE/recompute_ledger.py" .` | 0 |
| verify_round1c | `rtk proxy python3 "$EVIDENCE/verify_round1c.py" .` | 0 |
| verify_round1d | `rtk proxy python3 "$EVIDENCE/verify_round1d.py" .` | 0 |

Acceptance: both Round 1d documentation steps are met.
HANDOFF.md and PR-BODY.md include Round 1d, the source checkpoint, current inventory, lever bases/risks/verification, lane sequence and exact-head gate table.
The packet includes arithmetic scripts, logs and receipts with sizes and digests.
All output files remain under 200 KB; PR-BODY.md has no host paths or private account names.

Remaining obligations: measured CPU-memory reuse, actual firmware packing and replacement buffers; F5 integration; service bounds; independent review and routed/bench qualification.
These are author checks, not review verdicts.
The worktree is clean. No RTL, port, register-map, parameter or gate implementation changed.
No new Vivado run, hardware access, push or PR edit was performed.
