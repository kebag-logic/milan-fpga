[A540] Mark II area plan (#640)

## Status

Round 1b is ready for review at `c4b8b7d373c9233bc9e71c6ed32eae9ad2b3f970`.
Executor: [A540]. Reviewers: [R492] internal, [R493] external.
Relates to #640; this is its stage-1 area plan, not completion of the redesign.

## Description

The earlier plan predates the default control-plane split and the current resource records.
This revision starts from the recorded 50,267-LUT image, prices the qualified split and
orders the remaining lanes against NFR-RES-01's 38,040-LUT limit with timing met.

Only `docs/design/MARK_II_AREA_PLAN.md` and `docs/design/AREA_BUDGET.md` differ from
dev `5603c353137e90c1fa95429f6d00ef7a2298d9ee`.

## Round 1b

- Merged the assigned dev revision with merge commit `a959b7879ed05a24c89bf71424e02c3049042463`.
- Incorporated every decision linked by #640 comment 6080904058, including diagnostics retained,
  on-chip memory approved, the smaller core conditional, one-percent planning margin, and
  F0-F5 as the qualified default before P3. Earlier placement alternatives are explicitly superseded.
- Reused all three committed resource endpoints: route-1x1 50,267 LUT, ooc-1x1 23,179 LUT,
  ooc-8x8 30,135 LUT. Their measured source is `a5ca6e5110d515bf5f894f87b94f9bf6f6836bbb`,
  carried by the assigned dev revision. This revision introduces no new Vivado measurement.
- Estimated split saving: 14,000 LUT (11,500-16,000), from disjoint source scopes with
  measured 3,102-LUT mailbox replacement cost and explicit integration/mapping allowances.
- Recomputed the complete ledger: 31,067 LUT centrally, 35,067 conservatively; without the
  conditional smaller core, the conservative estimate is 36,367. These are planning estimates.
- Gave M2, M3, M5, M6, M7, M8, M10 and M9 scope, dependencies, order and verification cost.
  M3/M10 have zero default-image credit because F5 already removes their AECP hardware.
  M1 is dropped and F4 replaces M4. The supported fabric-AECP opportunities remain separately priced.
- Aligned AREA_BUDGET with that ledger and D7: intermediate deltas remain visible against the last
  record; M9 re-records at the target with timing. Gate policy and resource records are unchanged.

## How to reproduce

Read the plan's recorded-baseline, inventory, levers, ledger, lane-sequence and recorded-decisions sections.
Compare its three endpoint rows with `syn/ooc/pp_resource_baseline.json` and the source receipt in
`docs/findings/234_PP_SHADOW_AREA_BASELINE.md`. The mailbox debit comes from
`docs/design/MAILBOX_SPLIT.md`'s measured-area section.

For the split arithmetic, the disjoint wrapper subtotal is 17,678 LUT, plus parent MAAP 429,
minus mailbox 3,102 and integration allowance 1,000: 14,005, rounded down to 14,000.
The range varies integration and mapping allowances; it is not a measured integrated delta.

## How to validate

The full documentation and applicable resource-policy campaign completed at the head above:
48/48 commands returned 0. The exact command table follows, using the environment pinned by
`tools/markdown/requirements.txt` and initialized submodules. Checks ran without shell pipes.
The evidence is validation of this documentation change, not an independent review verdict.

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

## DoD

- [x] Assigned development revision merged without rebase or amend.
- [x] Linked decisions and all three recorded endpoints incorporated.
- [x] Split and remaining estimates have saving basis, dependencies and verification cost.
- [x] AREA_BUDGET agrees; policy values and measured records remain unchanged.
- [x] Documentation and applicable resource-policy gates pass at the stated head.
- [ ] Independent reviews and publication by the manager.

The implementation still must prove full split integration, F5 storage capacity, bounded CPU service,
F2-F5 suite and bench acceptance, and final routed fit/timing. Default placement changes only after
qualification; unqualified functions keep their fabric owner. M9 also needs reviewed measurement
coverage for a split image without the wrapper, preserving all-fabric standalone references.
