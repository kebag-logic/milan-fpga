# Round 4 handoff

Author: [A353]
Issue: https://github.com/kebag-logic/milan-fpga/issues/502
Review: https://github.com/kebag-logic/milan-fpga/pull/579
Assignment: https://github.com/kebag-logic/milan-fpga/issues/502#issuecomment-5854288100
Starting head: `867a2e38a4e3231545a0a24b97d1e5612a6659fe`
Branch: `502-pending-live-write`
Origin verified: `https://github.com/kebag-logic/milan-fpga.git`

## Status

All three assignment items are committed at `92c6154a17d1f1192f20a3a642e6a01b616afb67`.
Every required final gate passes. The public review-ready comment is posted.
No executable RTL, firmware, configuration, or submodule edits.
The three changed SystemVerilog files contain documentation-only edits.
The datapath VERSION assertion changes its diagnostic string only.

## Public context and behavior

- R329-3: https://github.com/kebag-logic/milan-fpga/pull/579#issuecomment-5854248329
- R328-3: https://github.com/kebag-logic/milan-fpga/pull/579#issuecomment-5854285010
- Read the current review body, requirements, ownership/materialization contracts, and repository workflow.
- Read the delivered pending glue and parent actual-write predicate.
- Names use accepted `aecp_name_wr_o`; maps use actual parent phase-5 `amap_edit_live_wr_p`.
- Marks remain command-completion triggers. Unchanged maps raise nothing.
- Pending stays sticky until reset; materialization remains separate work.

## Sweep method

All searches cover every tracked first-party path, including history, comments, READMEs, tests and changelog.
Submodules are gitlinks and are not recursively searched or edited.
Commands ran from `$LANES/502-pending-live-write`.
S1-S6 used `git grep -n -i -I -E <pattern> -- .` before edits.
S7 used `git grep -n -i -I -E <pattern> 867a2e38 -- .`.
Each row below names its original file:line at the starting head.
Multiple patterns matching one line share one row; no hits are omitted.
S1/S2 were broad exploratory expressions; S4/S5/S7 correct their POSIX newline-class limitation.
Fixed means text or its explicit historical qualification was changed.
Historical means retained, explicitly scoped evidence or original behavior.
Already-accurate statements and lexical false positives are separately identified to avoid claiming nonexistent edits.

## Every search pattern

| ID | Exact extended regular expression | Hits |
|---|---|---|
| S1 | `NVM_MARK&#124;aecp_mark_pend_r&#124;mark[^\n]*pend&#124;pend[^\n]*mark` | 66 |
| S2 | `commit[- ]beats?&#124;conservative[^\n]*duplicat&#124;duplicat[^\n]*conservative` | 2 |
| S3 | `#502&#124;late[- ]mark&#124;mark[- ]tail&#124;durable[^\n]*tail&#124;tail[^\n]*durable` | 37 |
| S4 | `NVM_MARK&#124;aecp_mark_pend_r&#124;commit marks?&#124;command[- ]marks?&#124;mark[- ]trigger&#124;\bmarks?\b.*\b(pending&#124;pend_i)\b&#124;\b(pending&#124;pend_i)\b.*\bmarks?\b&#124;class[- ]?[67]` | 62 |
| S5 | `conservative.*duplicat&#124;duplicat.*conservative&#124;every.*commit&#124;commit.*every&#124;late[- ]mark&#124;mark[- ]tail&#124;durable.*tail&#124;tail.*durable` | 97 |
| S6 | `aecp_mark_pend_r` | 0 |
| S7 | `conservative&#124;aecp_mark_pend_r&#124;every (accepted )?(map )?commit&#124;commit[- ]beats?&#124;late[-_ ]mark&#124;mark[-_ ]tail` | 71 |

## Every hit and disposition

| Patterns | Original file:line | Disposition | Reason |
|---|---|---|---|
| S7 | `.github/workflows/rtl-fast.yml:35` | Not a claim | Workflow, renderer, or Git commit policy; no name/map pending-trigger claim. |
| S5 | `.github/workflows/rtl.yml:49` | Not a claim | Workflow, renderer, or Git commit policy; no name/map pending-trigger claim. |
| S3 | `CHANGELOG.md:37` | Current (verified) | Correct live-write tests or intentionally restored historical late-mark mutant; marks remain observable completion events. |
| S4 | `CHANGELOG.md:42` | Current (verified) | Correct live-write tests or intentionally restored historical late-mark mutant; marks remain observable completion events. |
| S3, S5, S7 | `CHANGELOG.md:45` | Current (verified) | Correct live-write tests or intentionally restored historical late-mark mutant; marks remain observable completion events. |
| S1, S4 | `CHANGELOG.md:262` | Historical | Original 0x0060 section now explicitly labeled pre-#502 history. |
| S4 | `CHANGELOG.md:265` | Historical | Original 0x0060 section now explicitly labeled pre-#502 history. |
| S1, S4 | `CHANGELOG.md:266` | Fixed | Original release behavior explicitly labeled historical; current #502 entry already states actual writes. |
| S5 | `CONTRIBUTING.md:254` | Not a claim | Workflow, renderer, or Git commit policy; no name/map pending-trigger claim. |
| S5, S7 | `CONTRIBUTING.md:566` | Not a claim | Workflow, renderer, or Git commit policy; no name/map pending-trigger claim. |
| S5, S7 | `CONTRIBUTING.md:696` | Not a claim | Workflow, renderer, or Git commit policy; no name/map pending-trigger claim. |
| S7 | `configs/endstation_arty_current.yaml:139` | Not a claim | Different commit/marker or conservative-bound context; no #502 pending-trigger statement. |
| S1 | `docs/BUILD_FLASH_BOOT.gen.py:81` | Not a claim | Broad search matched append/marker identifiers; no persistence trigger statement. |
| S5, S7 | `docs/DOC_GENERATION.md:5` | Not a claim | Different commit/marker or conservative-bound context; no #502 pending-trigger statement. |
| S5 | `docs/MILAN_V12_ROADMAP.md:352` | Not a claim | Different commit/marker or conservative-bound context; no #502 pending-trigger statement. |
| S5, S7 | `docs/README.md:137` | Not a claim | Different commit/marker or conservative-bound context; no #502 pending-trigger statement. |
| S1 | `docs/SYSTEM_DOMAIN_MAP.gen.py:122` | Not a claim | Broad search matched append/marker identifiers; no persistence trigger statement. |
| S5 | `docs/design/SAVED_STATE_FASTCONNECT.md:105` | Current (verified) | Image commit/durability contract is separate from the pending-source trigger. |
| S4 | `docs/design/SAVED_STATE_FASTCONNECT.md:110` | Historical | Inventory at 44489453 and original mark acceptance; D3 amendment remains explicitly proposed. |
| S1, S4 | `docs/design/SAVED_STATE_FASTCONNECT.md:114` | Historical | Inventory at 44489453 and original mark acceptance; D3 amendment remains explicitly proposed. |
| S1, S4, S5 | `docs/design/SAVED_STATE_FASTCONNECT.md:123` | Fixed | Unobserved marks row explicitly labeled historical at 44489453. |
| S5 | `docs/design/SAVED_STATE_FASTCONNECT.md:130` | Current (verified) | Image commit/durability contract is separate from the pending-source trigger. |
| S5 | `docs/design/SAVED_STATE_FASTCONNECT.md:164` | Current (verified) | Image commit/durability contract is separate from the pending-source trigger. |
| S5 | `docs/design/SAVED_STATE_FASTCONNECT.md:1085` | Current (verified) | Image commit/durability contract is separate from the pending-source trigger. |
| S5, S7 | `docs/design/SAVED_STATE_FASTCONNECT.md:1145` | Current (verified) | Image commit/durability contract is separate from the pending-source trigger. |
| S5 | `docs/design/SAVED_STATE_FASTCONNECT.md:1195` | Current (verified) | Image commit/durability contract is separate from the pending-source trigger. |
| S5 | `docs/design/SAVED_STATE_FASTCONNECT.md:1201` | Current (verified) | Image commit/durability contract is separate from the pending-source trigger. |
| S5 | `docs/design/SAVED_STATE_FASTCONNECT.md:1269` | Current (verified) | Image commit/durability contract is separate from the pending-source trigger. |
| S4 | `docs/design/SAVED_STATE_FASTCONNECT.md:1333` | Historical | Inventory at 44489453 and original mark acceptance; D3 amendment remains explicitly proposed. |
| S1, S4 | `docs/design/SAVED_STATE_FASTCONNECT.md:1337` | Historical | Inventory at 44489453 and original mark acceptance; D3 amendment remains explicitly proposed. |
| S1, S4 | `docs/design/SAVED_STATE_FASTCONNECT.md:1371` | Fixed | Replaced stale current routing with historical pin and current exported completion marks/live writes. |
| S4 | `docs/design/SAVED_STATE_FASTCONNECT.md:1391` | Fixed | States missing materializer without implying current pending uses commit marks. |
| S5 | `docs/design/SAVED_STATE_FASTCONNECT.md:1541` | Current (verified) | Image commit/durability contract is separate from the pending-source trigger. |
| S5 | `docs/design/SAVED_STATE_MATERIALIZATION.md:64` | Current (verified) | Correct live-write description, mutation requirement, or distinct D3 contract; no stale current trigger claim. |
| S3 | `docs/design/SAVED_STATE_MATERIALIZATION.md:111` | Current (verified) | Valid release dependency/ticket reference; implementation does not waive landing or persistence proof. |
| S3 | `docs/design/SAVED_STATE_MATERIALIZATION.md:172` | Current (verified) | Valid release dependency/ticket reference; implementation does not waive landing or persistence proof. |
| S4 | `docs/design/SAVED_STATE_MATERIALIZATION.md:213` | Fixed | Pre-#502 mark-based reporting explicitly historical; current correction follows. |
| S1, S4 | `docs/design/SAVED_STATE_MATERIALIZATION.md:215` | Historical | Pinned design evidence/review history; current behavior and issue disposition are stated separately. |
| S3 | `docs/design/SAVED_STATE_MATERIALIZATION.md:221` | Fixed | Replaced present defect wording with implemented correction and retained release prerequisite. |
| S3 | `docs/design/SAVED_STATE_MATERIALIZATION.md:224` | Current (verified) | Correct live-write description, mutation requirement, or distinct D3 contract; no stale current trigger claim. |
| S4 | `docs/design/SAVED_STATE_MATERIALIZATION.md:232` | Current (verified) | Correct live-write description, mutation requirement, or distinct D3 contract; no stale current trigger claim. |
| S3, S5, S7 | `docs/design/SAVED_STATE_MATERIALIZATION.md:245` | Current (verified) | Correct live-write description, mutation requirement, or distinct D3 contract; no stale current trigger claim. |
| S4 | `docs/design/SAVED_STATE_MATERIALIZATION.md:267` | Current (verified) | Correct live-write description, mutation requirement, or distinct D3 contract; no stale current trigger claim. |
| S4 | `docs/design/SAVED_STATE_MATERIALIZATION.md:297` | Fixed | Planned retirement now names the sticky live-name/map source. |
| S4 | `docs/design/SAVED_STATE_MATERIALIZATION.md:458` | Current (verified) | Correct live-write description, mutation requirement, or distinct D3 contract; no stale current trigger claim. |
| S1, S4 | `docs/design/SAVED_STATE_MATERIALIZATION.md:476` | Current (verified) | Proposed D3 record-writer contract/amendment, not the delivered pending source; unchanged. |
| S4 | `docs/design/SAVED_STATE_MATERIALIZATION.md:479` | Current (verified) | Proposed D3 record-writer contract/amendment, not the delivered pending source; unchanged. |
| S5 | `docs/design/SAVED_STATE_MATERIALIZATION.md:681` | Current (verified) | Correct live-write description, mutation requirement, or distinct D3 contract; no stale current trigger claim. |
| S4 | `docs/design/SAVED_STATE_MATERIALIZATION.md:732` | Fixed | Names aecp_live_pend_r instead of a superseded class-mark bit. |
| S4 | `docs/design/SAVED_STATE_MATERIALIZATION.md:1612` | Current (verified) | Correct live-write description, mutation requirement, or distinct D3 contract; no stale current trigger claim. |
| S3 | `docs/design/SAVED_STATE_MATERIALIZATION.md:1654` | Fixed | Retains landing prerequisite; no longer claims current status has the tail defect. |
| S3 | `docs/design/SAVED_STATE_MATERIALIZATION.md:1657` | Fixed | Specifies accepted name writes, actual parent map writes, and completion-only marks. |
| S3 | `docs/design/SAVED_STATE_MATERIALIZATION.md:1659` | Fixed | Retains landing prerequisite and separates materialization. |
| S3 | `docs/design/SAVED_STATE_MATERIALIZATION.md:1672` | Fixed | Permitted work no longer treats the implemented correction as unstarted. |
| S3 | `docs/design/SAVED_STATE_MATERIALIZATION.md:1676` | Current (verified) | Valid release dependency/ticket reference; implementation does not waive landing or persistence proof. |
| S3 | `docs/design/SAVED_STATE_MATERIALIZATION.md:1686` | Current (verified) | Valid release dependency/ticket reference; implementation does not waive landing or persistence proof. |
| S3, S4 | `docs/design/SAVED_STATE_MATERIALIZATION.md:1687` | Fixed | Stage 2 retires live name reporting from the sticky source. |
| S4 | `docs/design/SAVED_STATE_MATERIALIZATION.md:1688` | Fixed | Stage 3 removes the sticky live-name/map bit. |
| S4 | `docs/design/SAVED_STATE_MATERIALIZATION.md:1697` | Fixed | Replaced old class-bit conditional with the implemented live-write source and planned retirement. |
| S3 | `docs/design/SAVED_STATE_MATERIALIZATION.md:1698` | Fixed | Removed the conditional implying #502 might not be implemented. |
| S3 | `docs/design/SAVED_STATE_MATERIALIZATION.md:1704` | Current (verified) | Valid release dependency/ticket reference; implementation does not waive landing or persistence proof. |
| S3, S4, S5 | `docs/design/SAVED_STATE_MATERIALIZATION.md:1717` | Fixed | Rejected mark trigger explicitly belongs to historical pre-#502 glue. |
| S4 | `docs/design/SAVED_STATE_MATERIALIZATION.md:1916` | Historical | Pinned design evidence/review history; current behavior and issue disposition are stated separately. |
| S3, S5, S7 | `docs/design/SAVED_STATE_MATERIALIZATION.md:1971` | Historical | Pinned design evidence/review history; current behavior and issue disposition are stated separately. |
| S1, S4 | `docs/design/SAVED_STATE_MATERIALIZATION.md:2056` | Fixed | Removed stale present-tense ownership quotation; original D2 behavior is history. |
| S1, S4 | `docs/design/SAVED_STATE_MATERIALIZATION.md:2060` | Current (verified) | Proposed D3 record-writer contract/amendment, not the delivered pending source; unchanged. |
| S2, S7 | `docs/design/SAVED_STATE_MATERIALIZATION.md:2061` | Current (verified) | Proposed D3 record-writer contract/amendment, not the delivered pending source; unchanged. |
| S4 | `docs/design/SAVED_STATE_MATERIALIZATION.md:2070` | Fixed | Tail failure explicitly historical pre-#502 evidence. |
| S3, S5, S7 | `docs/design/SAVED_STATE_MATERIALIZATION.md:2081` | Fixed | UNRESOLVED item 3 now says RESOLVED by #502 and names both delivered triggers. |
| S5 | `docs/design/SAVED_STATE_MATERIALIZATION.md:2082` | Fixed | Replaced present defect with actual writes, unchanged-map exclusion, and completion mark. |
| S2, S7 | `docs/design/SAVED_STATE_MATERIALIZATION.md:2117` | Fixed | Explicitly scoped to proposed D3 writer; current pending excludes unchanged maps. |
| S3 | `docs/design/SAVED_STATE_MATERIALIZATION.md:2223` | Historical | Pinned design evidence/review history; current behavior and issue disposition are stated separately. |
| S4 | `docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md:27` | Fixed | Intro now distinguishes original exports from #502 live-write reporting. |
| S5 | `docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md:119` | Current (verified) | Existing live-write or separate snapshot contract remains accurate. |
| S5 | `docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md:659` | Current (verified) | Existing live-write or separate snapshot contract remains accurate. |
| S3 | `docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md:955` | Current (verified) | Existing live-write or separate snapshot contract remains accurate. |
| S4 | `docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md:973` | Current (verified) | Existing live-write or separate snapshot contract remains accurate. |
| S5 | `docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md:1049` | Current (verified) | Existing live-write or separate snapshot contract remains accurate. |
| S5 | `docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md:1192` | Current (verified) | Existing live-write or separate snapshot contract remains accurate. |
| S5 | `docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md:1237` | Current (verified) | Existing live-write or separate snapshot contract remains accurate. |
| S3 | `docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md:1263` | Current (verified) | Existing live-write or separate snapshot contract remains accurate. |
| S3 | `docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md:1264` | Current (verified) | Existing live-write or separate snapshot contract remains accurate. |
| S3 | `docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md:1271` | Current (verified) | Existing live-write or separate snapshot contract remains accurate. |
| S4 | `docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md:1361` | Historical | D2 exports and original parent use explicitly identified as original; adjacent #502 text gives current behavior. |
| S1, S4 | `docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md:1365` | Historical | D2 exports and original parent use explicitly identified as original; adjacent #502 text gives current behavior. |
| S1, S4 | `docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md:1366` | Historical | D2 exports and original parent use explicitly identified as original; adjacent #502 text gives current behavior. |
| S1, S4 | `docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md:1367` | Historical | D2 exports and original parent use explicitly identified as original; adjacent #502 text gives current behavior. |
| S1, S4 | `docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md:1369` | Historical | D2 exports and original parent use explicitly identified as original; adjacent #502 text gives current behavior. |
| S1, S4 | `docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md:1375` | Historical | D2 exports and original parent use explicitly identified as original; adjacent #502 text gives current behavior. |
| S3 | `docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md:1380` | Current (verified) | Existing live-write or separate snapshot contract remains accurate. |
| S5 | `docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md:1422` | Current (verified) | Existing live-write or separate snapshot contract remains accurate. |
| S5 | `docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md:1429` | Current (verified) | Existing live-write or separate snapshot contract remains accurate. |
| S4 | `docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md:1739` | Current (verified) | Existing live-write or separate snapshot contract remains accurate. |
| S1, S3, S4 | `docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md:1740` | Current (verified) | Existing live-write or separate snapshot contract remains accurate. |
| S7 | `docs/design/TIME_SYNC.md:280` | Not a claim | Different commit/marker or conservative-bound context; no #502 pending-trigger statement. |
| S5 | `docs/design/TIME_SYNC.md:365` | Not a claim | Different commit/marker or conservative-bound context; no #502 pending-trigger statement. |
| S5 | `docs/development/CODE_QUALITY.md:1944` | Not a claim | Different commit/marker or conservative-bound context; no #502 pending-trigger statement. |
| S5, S7 | `docs/diagrams/README.md:139` | Not a claim | Different commit/marker or conservative-bound context; no #502 pending-trigger statement. |
| S1 | `docs/diagrams/audio_stream_path.gen.py:152` | Not a claim | Broad search matched append/marker identifiers; no persistence trigger statement. |
| S1 | `docs/diagrams/svglib.py:99` | Not a claim | Broad search matched append/marker identifiers; no persistence trigger statement. |
| S5 | `docs/findings/117_GPTP_SILICON_EVIDENCE.md:548` | Not a claim | Different commit/marker or conservative-bound context; no #502 pending-trigger statement. |
| S7 | `docs/fpga/FPGA_DESIGN.md:223` | Not a claim | Different commit/marker or conservative-bound context; no #502 pending-trigger statement. |
| S7 | `docs/history/v1/NXN_ARCHITECTURE.md:505` | Historical | Versioned history page; unrelated preserved evidence, not current pending behavior. |
| S7 | `docs/history/v1/NXN_ARCHITECTURE.md:954` | Historical | Versioned history page; unrelated preserved evidence, not current pending behavior. |
| S7 | `docs/history/v1/findings/PP_SHADOW_AREA_0812.md:234` | Historical | Versioned history page; unrelated preserved evidence, not current pending behavior. |
| S7 | `docs/history/v1/reference/MILAN_V12_DEPENDENCY_MATRIX.md:230` | Historical | Versioned history page; unrelated preserved evidence, not current pending behavior. |
| S7 | `docs/history/v1/reference/PROTOCOL_TRACEABILITY.md:376` | Historical | Versioned history page; unrelated preserved evidence, not current pending behavior. |
| S7 | `docs/history/v1/reference/PROTOCOL_TRACEABILITY.md:388` | Historical | Versioned history page; unrelated preserved evidence, not current pending behavior. |
| S7 | `docs/history/v1/reference/PROTOCOL_TRACEABILITY.md:396` | Historical | Versioned history page; unrelated preserved evidence, not current pending behavior. |
| S5 | `docs/history/v1/reference/PROTOCOL_TRACEABILITY.md:440` | Historical | Versioned history page; unrelated preserved evidence, not current pending behavior. |
| S5 | `docs/history/v1/reference/PROTOCOL_TRACEABILITY.md:443` | Historical | Versioned history page; unrelated preserved evidence, not current pending behavior. |
| S5 | `docs/history/v1/traceability/ieee1722-2016.md:78` | Historical | Versioned history page; unrelated preserved evidence, not current pending behavior. |
| S5 | `docs/history/v1/traceability/ieee1722_1-2021.md:273` | Historical | Versioned history page; unrelated preserved evidence, not current pending behavior. |
| S7 | `docs/integration/BAREMETAL_FIRMWARE.md:1466` | Not a claim | Different commit/marker or conservative-bound context; no #502 pending-trigger statement. |
| S7 | `docs/integration/BAREMETAL_FIRMWARE.md:1467` | Not a claim | Different commit/marker or conservative-bound context; no #502 pending-trigger statement. |
| S5, S7 | `docs/integration/BAREMETAL_FIRMWARE.md:1571` | Not a claim | Different commit/marker or conservative-bound context; no #502 pending-trigger statement. |
| S7 | `docs/integration/BAREMETAL_FIRMWARE.md:1815` | Not a claim | Different commit/marker or conservative-bound context; no #502 pending-trigger statement. |
| S5 | `docs/integration/BUILDING.md:144` | Not a claim | Different commit/marker or conservative-bound context; no #502 pending-trigger statement. |
| S5 | `docs/integration/BUILDING.md:147` | Not a claim | Different commit/marker or conservative-bound context; no #502 pending-trigger statement. |
| S5 | `docs/integration/BUILDING.md:435` | Not a claim | Different commit/marker or conservative-bound context; no #502 pending-trigger statement. |
| S5 | `docs/limitations/RECURRING_DEFECT_PATTERNS.md:147` | Not a claim | Different commit/marker or conservative-bound context; no #502 pending-trigger statement. |
| S7 | `docs/reference/EGRESS_QUEUE_MAP.md:74` | Not a claim | Different commit/marker or conservative-bound context; no #502 pending-trigger statement. |
| S7 | `docs/reference/REGISTER_MAP.md:190` | Not a claim | Different commit/marker or conservative-bound context; no #502 pending-trigger statement. |
| S5 | `docs/reference/REGISTER_MAP.md:358` | Not a claim | Different commit/marker or conservative-bound context; no #502 pending-trigger statement. |
| S5 | `docs/reference/REGISTER_MAP.md:1528` | Not a claim | Different commit/marker or conservative-bound context; no #502 pending-trigger statement. |
| S5 | `docs/reference/REGISTER_MAP.md:1674` | Not a claim | Different commit/marker or conservative-bound context; no #502 pending-trigger statement. |
| S5 | `docs/reference/REGISTER_MAP.md:1679` | Not a claim | Different commit/marker or conservative-bound context; no #502 pending-trigger statement. |
| S1 | `docs/reference/REGISTER_MAP.md:1909` | Not a claim | Different commit/marker or conservative-bound context; no #502 pending-trigger statement. |
| S5 | `docs/reference/REGISTER_MAP.md:2239` | Not a claim | Different commit/marker or conservative-bound context; no #502 pending-trigger statement. |
| S5 | `docs/reference/REGISTER_MAP_CLASSES.md:95` | Not a claim | Different commit/marker or conservative-bound context; no #502 pending-trigger statement. |
| S3 | `docs/reference/SUBMODULES.md:57` | Current (verified) | Pin history already names accepted names and actual parent map writes. |
| S7 | `docs/testing/CI_WORKFLOWS.md:27` | Not a claim | Workflow, renderer, or Git commit policy; no name/map pending-trigger claim. |
| S7 | `docs/testing/CI_WORKFLOWS.md:293` | Not a claim | Workflow, renderer, or Git commit policy; no name/map pending-trigger claim. |
| S7 | `docs/testing/CI_WORKFLOWS.md:560` | Not a claim | Workflow, renderer, or Git commit policy; no name/map pending-trigger claim. |
| S5 | `docs/testing/CI_WORKFLOWS.md:997` | Not a claim | Workflow, renderer, or Git commit policy; no name/map pending-trigger claim. |
| S5 | `docs/testing/CI_WORKFLOWS.md:1000` | Not a claim | Workflow, renderer, or Git commit policy; no name/map pending-trigger claim. |
| S4 | `docs/testing/MILAN_V12_AUDIT_2026-08-16.md:131` | Historical | Dated protocol audit; changed-command marks/other protocol behavior, not current pending. |
| S5 | `docs/testing/MILAN_V12_AUDIT_2026-08-16.md:256` | Historical | Dated protocol audit; changed-command marks/other protocol behavior, not current pending. |
| S3, S4, S5, S7 | `docs/testing/TESTING.md:268` | Current (verified) | Correct live-write tests or intentionally restored historical late-mark mutant; marks remain observable completion events. |
| S5 | `docs/testing/TESTING.md:492` | Not a claim | Different commit/marker or conservative-bound context; no #502 pending-trigger statement. |
| S5 | `docs/testing/TESTING.md:493` | Not a claim | Different commit/marker or conservative-bound context; no #502 pending-trigger statement. |
| S5 | `docs/testing/TESTING.md:967` | Not a claim | Different commit/marker or conservative-bound context; no #502 pending-trigger statement. |
| S7 | `hdl/common/cdc_pair_fifo.sv:23` | Not a claim | Different commit/marker or conservative-bound context; no #502 pending-trigger statement. |
| S4 | `hdl/common/csr/milan_csr.sv:184` | Fixed | Comment labels original VERSION behavior historical and explains current write triggers. |
| S5 | `hdl/ieee1722/avtp/KL_avtp_rx_monitor_ctx.sv:1068` | Not a claim | Different commit/marker or conservative-bound context; no #502 pending-trigger statement. |
| S5 | `hdl/ieee1722/avtp/doc/KL_avtp_rx_monitor/KL_avtp_rx_monitor.md:5` | Not a claim | Different commit/marker or conservative-bound context; no #502 pending-trigger statement. |
| S7 | `hdl/ieee1722/crf/KL_crf_rx.sv:282` | Not a claim | Different commit/marker or conservative-bound context; no #502 pending-trigger statement. |
| S5 | `hdl/ieee1722/crf/KL_mmcm_drp_servo.sv:73` | Not a claim | Different commit/marker or conservative-bound context; no #502 pending-trigger statement. |
| S7 | `hdl/ieee8021as/gptp_plane/KL_gptp_shadow.sv:479` | Current (verified) | Separate gPTP mark port/waiver; no name/map pending-source claim. |
| S1, S4 | `hdl/ieee8021as/gptp_plane/KL_gptp_shadow.sv:696` | Current (verified) | Separate gPTP mark port/waiver; no name/map pending-source claim. |
| S7 | `hdl/ieee8021q/ts/credit_based_shaper.sv:245` | Not a claim | Different commit/marker or conservative-bound context; no #502 pending-trigger statement. |
| S7 | `hdl/ieee8021q/ts/credit_based_shaper.sv:246` | Not a claim | Different commit/marker or conservative-bound context; no #502 pending-trigger statement. |
| S5 | `hdl/ieee8021q/ts/credit_based_shaper.sv:258` | Not a claim | Different commit/marker or conservative-bound context; no #502 pending-trigger statement. |
| S7 | `hdl/ieee8021q/ts/traffic_shaping_core.sv:165` | Not a claim | Different commit/marker or conservative-bound context; no #502 pending-trigger statement. |
| S4 | `hdl/milan/KL_nvm_backend.sv:202` | Fixed | Port comment now describes accepted live writes plus sticky history. |
| S4 | `hdl/milan/KL_pp_shadow.sv:927` | Current (verified) | Marks are retained completion outputs; actual pending uses aecp_name_wr_w, amap_live_wr_i, and sticky history. |
| S1, S4 | `hdl/milan/KL_pp_shadow.sv:940` | Current (verified) | Marks are retained completion outputs; actual pending uses aecp_name_wr_w, amap_live_wr_i, and sticky history. |
| S1, S4 | `hdl/milan/KL_pp_shadow.sv:943` | Current (verified) | Marks are retained completion outputs; actual pending uses aecp_name_wr_w, amap_live_wr_i, and sticky history. |
| S1, S4 | `hdl/milan/KL_pp_shadow.sv:1086` | Current (verified) | Marks are retained completion outputs; actual pending uses aecp_name_wr_w, amap_live_wr_i, and sticky history. |
| S5 | `hdl/milan/milan_datapath.sv:6457` | Not a claim | Different commit/marker or conservative-bound context; no #502 pending-trigger statement. |
| S5 | `hdl/milan/milan_datapath.sv:7165` | Not a claim | Different commit/marker or conservative-bound context; no #502 pending-trigger statement. |
| S7 | `scripts/act_ci.py:176` | Not a claim | Workflow, renderer, or Git commit policy; no name/map pending-trigger claim. |
| S5 | `scripts/check_doc_paths.py:4` | Not a claim | Workflow, renderer, or Git commit policy; no name/map pending-trigger claim. |
| S5 | `scripts/check_em_dash.py:450` | Not a claim | Workflow, renderer, or Git commit policy; no name/map pending-trigger claim. |
| S5 | `scripts/check_em_dash.py:548` | Not a claim | Workflow, renderer, or Git commit policy; no name/map pending-trigger claim. |
| S1 | `scripts/check_feature_status.py:660` | Not a claim | Broad search matched append/marker identifiers; no persistence trigger statement. |
| S1 | `scripts/check_feature_status_selftest.py:234` | Not a claim | Broad search matched append/marker identifiers; no persistence trigger statement. |
| S1 | `scripts/check_feature_status_selftest.py:236` | Not a claim | Broad search matched append/marker identifiers; no persistence trigger statement. |
| S1 | `scripts/check_feature_status_selftest.py:242` | Not a claim | Broad search matched append/marker identifiers; no persistence trigger statement. |
| S5 | `scripts/check_merge_containment.py:16` | Not a claim | Workflow, renderer, or Git commit policy; no name/map pending-trigger claim. |
| S5, S7 | `scripts/check_merge_containment.py:507` | Not a claim | Workflow, renderer, or Git commit policy; no name/map pending-trigger claim. |
| S5 | `scripts/check_merge_containment.py:551` | Not a claim | Workflow, renderer, or Git commit policy; no name/map pending-trigger claim. |
| S5 | `scripts/check_merge_containment.py:556` | Not a claim | Workflow, renderer, or Git commit policy; no name/map pending-trigger claim. |
| S5 | `scripts/check_nvm_record_space.py:5` | Not a claim | Workflow, renderer, or Git commit policy; no name/map pending-trigger claim. |
| S5 | `scripts/check_nvm_record_space.py:852` | Not a claim | Workflow, renderer, or Git commit policy; no name/map pending-trigger claim. |
| S5 | `scripts/ci_events.py:28` | Not a claim | Workflow, renderer, or Git commit policy; no name/map pending-trigger claim. |
| S7 | `scripts/ci_events.py:2376` | Not a claim | Workflow, renderer, or Git commit policy; no name/map pending-trigger claim. |
| S7 | `scripts/ci_scope.py:242` | Not a claim | Workflow, renderer, or Git commit policy; no name/map pending-trigger claim. |
| S1 | `scripts/gen_hdl_reference.py:664` | Not a claim | Broad search matched append/marker identifiers; no persistence trigger statement. |
| S1 | `scripts/gen_toc_renderer.py:276` | Not a claim | Broad search matched append/marker identifiers; no persistence trigger statement. |
| S1 | `scripts/gen_toc_renderer.py:285` | Not a claim | Broad search matched append/marker identifiers; no persistence trigger statement. |
| S1 | `scripts/gen_toc_renderer.py:288` | Not a claim | Broad search matched append/marker identifiers; no persistence trigger statement. |
| S5 | `scripts/gen_toc_shapes.json:2` | Not a claim | Workflow, renderer, or Git commit policy; no name/map pending-trigger claim. |
| S3, S4, S5, S7 | `scripts/measure_test_evidence.py:601` | Current (verified) | Correct live-write tests or intentionally restored historical late-mark mutant; marks remain observable completion events. |
| S5 | `scripts/merge_containment_git.py:24` | Not a claim | Workflow, renderer, or Git commit policy; no name/map pending-trigger claim. |
| S7 | `scripts/merge_containment_selftest_content.py:163` | Not a claim | Workflow, renderer, or Git commit policy; no name/map pending-trigger claim. |
| S5, S7 | `scripts/merge_containment_selftest_content.py:258` | Not a claim | Workflow, renderer, or Git commit policy; no name/map pending-trigger claim. |
| S7 | `scripts/merge_containment_selftest_replay.py:4` | Not a claim | Workflow, renderer, or Git commit policy; no name/map pending-trigger claim. |
| S1, S4 | `scripts/port_docs.budget:33` | Current (verified) | Separate gPTP mark port/waiver; no name/map pending-source claim. |
| S7 | `sw/builder/endstation_builder.py:499` | Not a claim | Different commit/marker or conservative-bound context; no #502 pending-trigger statement. |
| S1 | `sw/builder/endstation_builder.py:4332` | Not a claim | Broad search matched append/marker identifiers; no persistence trigger statement. |
| S1 | `sw/builder/endstation_builder.py:4337` | Not a claim | Broad search matched append/marker identifiers; no persistence trigger statement. |
| S1 | `sw/builder/endstation_builder.py:4339` | Not a claim | Broad search matched append/marker identifiers; no persistence trigger statement. |
| S1 | `sw/builder/endstation_builder.py:4343` | Not a claim | Broad search matched append/marker identifiers; no persistence trigger statement. |
| S1 | `sw/builder/endstation_builder.py:4345` | Not a claim | Broad search matched append/marker identifiers; no persistence trigger statement. |
| S1 | `sw/builder/endstation_builder.py:4347` | Not a claim | Broad search matched append/marker identifiers; no persistence trigger statement. |
| S1 | `sw/builder/endstation_builder.py:4362` | Not a claim | Broad search matched append/marker identifiers; no persistence trigger statement. |
| S1 | `sw/builder/endstation_builder.py:4376` | Not a claim | Broad search matched append/marker identifiers; no persistence trigger statement. |
| S1 | `sw/builder/endstation_builder.py:4389` | Not a claim | Broad search matched append/marker identifiers; no persistence trigger statement. |
| S1 | `sw/builder/endstation_builder.py:4398` | Not a claim | Broad search matched append/marker identifiers; no persistence trigger statement. |
| S1 | `sw/builder/endstation_builder.py:4456` | Not a claim | Broad search matched append/marker identifiers; no persistence trigger statement. |
| S1 | `sw/builder/endstation_builder.py:4464` | Not a claim | Broad search matched append/marker identifiers; no persistence trigger statement. |
| S1 | `sw/builder/endstation_builder.py:4474` | Not a claim | Broad search matched append/marker identifiers; no persistence trigger statement. |
| S1 | `sw/builder/endstation_builder.py:4516` | Not a claim | Broad search matched append/marker identifiers; no persistence trigger statement. |
| S1 | `sw/builder/endstation_builder.py:4527` | Not a claim | Broad search matched append/marker identifiers; no persistence trigger statement. |
| S1 | `sw/builder/endstation_builder.py:4541` | Not a claim | Broad search matched append/marker identifiers; no persistence trigger statement. |
| S1 | `sw/builder/endstation_builder.py:4554` | Not a claim | Broad search matched append/marker identifiers; no persistence trigger statement. |
| S1 | `sw/builder/endstation_builder.py:4579` | Not a claim | Broad search matched append/marker identifiers; no persistence trigger statement. |
| S1 | `sw/builder/endstation_builder.py:4588` | Not a claim | Broad search matched append/marker identifiers; no persistence trigger statement. |
| S1 | `sw/builder/endstation_builder.py:4599` | Not a claim | Broad search matched append/marker identifiers; no persistence trigger statement. |
| S1 | `sw/builder/endstation_builder.py:4619` | Not a claim | Broad search matched append/marker identifiers; no persistence trigger statement. |
| S7 | `sw/builder/test_builder.py:1570` | Not a claim | Different commit/marker or conservative-bound context; no #502 pending-trigger statement. |
| S1 | `sw/builder/test_builder.py:3260` | Not a claim | Broad search matched append/marker identifiers; no persistence trigger statement. |
| S5, S7 | `sw/builder/test_builder.py:4705` | Not a claim | Different commit/marker or conservative-bound context; no #502 pending-trigger statement. |
| S7 | `sw/builder/test_builder.py:5132` | Not a claim | Different commit/marker or conservative-bound context; no #502 pending-trigger statement. |
| S7 | `sw/builder/test_builder.py:16283` | Not a claim | Different commit/marker or conservative-bound context; no #502 pending-trigger statement. |
| S5 | `sw/builder/test_builder.py:17665` | Not a claim | Different commit/marker or conservative-bound context; no #502 pending-trigger statement. |
| S5 | `sw/litex/litex_pins.txt:10` | Not a claim | Different commit/marker or conservative-bound context; no #502 pending-trigger statement. |
| S7 | `sw/litex/milan_soc.py:2148` | Not a claim | Different commit/marker or conservative-bound context; no #502 pending-trigger statement. |
| S7 | `syn/ooc/dp_srcs.py:618` | Not a claim | Different commit/marker or conservative-bound context; no #502 pending-trigger statement. |
| S7 | `syn/yosys/README.md:117` | Not a claim | Different commit/marker or conservative-bound context; no #502 pending-trigger statement. |
| S7 | `syn/yosys/run.sh:506` | Not a claim | Different commit/marker or conservative-bound context; no #502 pending-trigger statement. |
| S7 | `tb/tools/torture_campaign.py:3107` | Not a claim | Different commit/marker or conservative-bound context; no #502 pending-trigger statement. |
| S7 | `tb/tools/torture_campaign.py:3305` | Not a claim | Different commit/marker or conservative-bound context; no #502 pending-trigger statement. |
| S5 | `tb/verilator/csr/README.md:84` | Not a claim | Different commit/marker or conservative-bound context; no #502 pending-trigger statement. |
| S1, S4 | `tb/verilator/gptp_plane/gptp_plane_wrap.sv:160` | Current (verified) | Separate gPTP mark port/waiver; no name/map pending-source claim. |
| S5 | `tb/verilator/gptp_shadow/sim_main.cpp:2313` | Not a claim | Different commit/marker or conservative-bound context; no #502 pending-trigger statement. |
| S7 | `tb/verilator/gptp_txts/sim_main.cpp:76` | Not a claim | Different commit/marker or conservative-bound context; no #502 pending-trigger statement. |
| S7 | `tb/verilator/milan_dp/README.md:256` | Not a claim | Different commit/marker or conservative-bound context; no #502 pending-trigger statement. |
| S7 | `tb/verilator/milan_dp/README.md:292` | Not a claim | Different commit/marker or conservative-bound context; no #502 pending-trigger statement. |
| S5 | `tb/verilator/milan_dp/README.md:607` | Not a claim | Different commit/marker or conservative-bound context; no #502 pending-trigger statement. |
| S5 | `tb/verilator/milan_dp/sim_gmstep.cpp:7` | Not a claim | Different commit/marker or conservative-bound context; no #502 pending-trigger statement. |
| S5 | `tb/verilator/milan_dp/sim_nxn.cpp:1358` | Not a claim | Different commit/marker or conservative-bound context; no #502 pending-trigger statement. |
| S4 | `tb/verilator/milan_dp/sim_nxn.cpp:2324` | Fixed | Diagnostic distinguishes original VERSION behavior from current #502 reporting. |
| S5 | `tb/verilator/milan_dp_render/sim_tdm8_render.cpp:664` | Not a claim | Different commit/marker or conservative-bound context; no #502 pending-trigger statement. |
| S5 | `tb/verilator/milan_dp_render/sim_tdm8_render.cpp:2241` | Not a claim | Different commit/marker or conservative-bound context; no #502 pending-trigger statement. |
| S5 | `tb/verilator/milan_dp_render/sim_tdm8_render.cpp:2924` | Not a claim | Different commit/marker or conservative-bound context; no #502 pending-trigger statement. |
| S5 | `tb/verilator/milan_dp_render/sim_tdm8_render.cpp:2925` | Not a claim | Different commit/marker or conservative-bound context; no #502 pending-trigger statement. |
| S5 | `tb/verilator/mmcm_servo/sim_phc_step.cpp:509` | Not a claim | Different commit/marker or conservative-bound context; no #502 pending-trigger statement. |
| S5 | `tb/verilator/mmcm_servo_autorepair/drp_model.h:13` | Not a claim | Different commit/marker or conservative-bound context; no #502 pending-trigger statement. |
| S4 | `tb/verilator/nvm_cosim/cosim_top.sv:425` | Fixed | Comment names current live-write source and shipping pp_shadow coverage. |
| S3 | `tb/verilator/pp_shadow/README.md:52` | Current (verified) | Correct live-write tests or intentionally restored historical late-mark mutant; marks remain observable completion events. |
| S3, S4, S5, S7 | `tb/verilator/pp_shadow/README.md:100` | Current (verified) | Correct live-write tests or intentionally restored historical late-mark mutant; marks remain observable completion events. |
| S3, S4, S5, S7 | `tb/verilator/pp_shadow/pending_mutant.py:4` | Current (verified) | Correct live-write tests or intentionally restored historical late-mark mutant; marks remain observable completion events. |
| S1, S4 | `tb/verilator/pp_shadow/pending_mutant.py:42` | Current (verified) | Correct live-write tests or intentionally restored historical late-mark mutant; marks remain observable completion events. |
| S1, S4 | `tb/verilator/pp_shadow/pending_mutant.py:43` | Current (verified) | Correct live-write tests or intentionally restored historical late-mark mutant; marks remain observable completion events. |
| S3, S5, S7 | `tb/verilator/pp_shadow/pending_mutant.py:60` | Current (verified) | Correct live-write tests or intentionally restored historical late-mark mutant; marks remain observable completion events. |
| S3, S5, S7 | `tb/verilator/pp_shadow/pending_mutant.py:64` | Current (verified) | Correct live-write tests or intentionally restored historical late-mark mutant; marks remain observable completion events. |
| S3, S5, S7 | `tb/verilator/pp_shadow/pending_mutant.py:67` | Current (verified) | Correct live-write tests or intentionally restored historical late-mark mutant; marks remain observable completion events. |
| S1, S4 | `tb/verilator/pp_shadow/pending_probes.vlt:9` | Current (verified) | Correct live-write tests or intentionally restored historical late-mark mutant; marks remain observable completion events. |
| S4 | `tb/verilator/pp_shadow/sim_main.cpp:316` | Current (verified) | Correct live-write tests or intentionally restored historical late-mark mutant; marks remain observable completion events. |
| S1, S4 | `tb/verilator/pp_shadow/sim_main.cpp:318` | Current (verified) | Correct live-write tests or intentionally restored historical late-mark mutant; marks remain observable completion events. |
| S1 | `tb/verilator/pp_shadow/sim_main.cpp:320` | Current (verified) | Correct live-write tests or intentionally restored historical late-mark mutant; marks remain observable completion events. |
| S3 | `tb/verilator/pp_shadow/sim_main.cpp:743` | Current (verified) | Correct live-write tests or intentionally restored historical late-mark mutant; marks remain observable completion events. |
| S1, S4 | `tb/verilator/pp_shadow/sim_main.cpp:1383` | Current (verified) | Correct live-write tests or intentionally restored historical late-mark mutant; marks remain observable completion events. |
| S1, S4 | `tb/verilator/pp_shadow/sim_main.cpp:1384` | Current (verified) | Correct live-write tests or intentionally restored historical late-mark mutant; marks remain observable completion events. |
| S1 | `tb/verilator/pp_shadow/sim_main.cpp:1387` | Current (verified) | Correct live-write tests or intentionally restored historical late-mark mutant; marks remain observable completion events. |
| S1 | `tb/verilator/pp_shadow/sim_main.cpp:1390` | Current (verified) | Correct live-write tests or intentionally restored historical late-mark mutant; marks remain observable completion events. |
| S3 | `tb/verilator/pp_shadow/sim_main.cpp:1494` | Current (verified) | Correct live-write tests or intentionally restored historical late-mark mutant; marks remain observable completion events. |
| S7 | `tb/verilator/tdm/sim_main.cpp:381` | Not a claim | late_mark is an audio sample-log index, not a persistence mark. |
| S7 | `tb/verilator/tdm/sim_main.cpp:687` | Not a claim | late_mark is an audio sample-log index, not a persistence mark. |
| S7 | `tb/verilator/tdm/sim_main.cpp:692` | Not a claim | late_mark is an audio sample-log index, not a persistence mark. |
| S7 | `tb/verilator/tdm/sim_main.cpp:694` | Not a claim | late_mark is an audio sample-log index, not a persistence mark. |
| S7 | `tb/verilator/tdm/sim_main.cpp:696` | Not a claim | late_mark is an audio sample-log index, not a persistence mark. |

Total: 335 pattern hits, 264 distinct file:line hits.

## Final commit

`92c6154a17d1f1192f20a3a642e6a01b616afb67`

Subject: Clarify live-write pending documentation and tag refusal diagnostics

Exactly one commit after the required starting head. No body or trailers.
The worktree is clean. The validated bytes were committed unchanged.
`scope-check.log` verifies comment-only SystemVerilog changes, identical trigger modules,
an unchanged VERSION assertion apart from its label, and unchanged gitlinks.

## Gate table

All required final gate verdicts are rc 0.

| Command | Result | Receipt |
|---|---|---|
| `make -C tb/verilator/pp_shadow` | rc 0; 591 + 591 + 591 + 295 checks; zero failures; 67.64 seconds | `pp-shadow-final.log` |
| `make -C tb/verilator/pp_shadow pending-mutant` | rc 0; clean 295/0; historical trigger produces 12 expected failures, including K10/K12; 29.93 seconds | `pending-mutant.log` |
| `python3 scripts/docs_check.py` | rc 0; 4.17 seconds | `docs-git-final.log` |
| `env GIT_DIR=/dev/null python3 scripts/docs_check.py` | rc 0; zero findings; inventory-parity self-test correctly skipped without Git; 4.17 seconds | `docs-no-git.log` |
| `python3 scripts/check_em_dash.py --base 831f94f4` | rc 0; zero findings; 339/339 control arms; 3.02 seconds | `em-dash.log` |
| `python3 scripts/check_doc_style.py` | rc 0; 0.06 seconds | `doc-style.log` |
| `python3 scripts/gen_toc.py --check` | rc 0; 2.52 seconds | `toc-check.log` |
| `python3 scripts/gen_toc.py --verify-anchors` | rc 0; 1.62 seconds | `anchors.log` |
| `python3 scripts/check_doc_paths.py` | rc 0; 0.06 seconds | `doc-paths.log` |
| `git diff --check` | rc 0; 0.03 seconds | `diff-worktree.log` |
| `git diff --check 867a2e38 HEAD` | rc 0; 0.02 seconds | `diff-commit.log` |
| `git diff --check 831f94f4 HEAD` | rc 0; 0.03 seconds | `diff-base.log` |

Additional staged whitespace check: `git diff --cached --check`, rc 0 before committing.
The base and delta checks cover the committed changes; the worktree check preceded staging.
`tag-receipts.log` records each input/output refusal status and map-count diagnostic.

### Setup attempt and environment

The first default run passed its base leg, then stopped at fixture generation.
Its temporary Python environment hid installed PyYAML; it returned rc 2.
No product assertion failed. The failed attempt is `pp-shadow-setup.log`.
System packages were enabled, retaining the pinned Markdown dependencies.
The complete default target then passed, as recorded above.
Earlier Git-mode docs success is retained in `docs-git.log`.
`gates.jsonl` records every attempt, including the environment failure.

The installed simulator is version 5.052, with build concurrency capped at eight.
The Markdown environment uses `tools/markdown/requirements.txt` with hash verification.
All gate commands run from `$LANES/502-pending-live-write`.
Commands run in the foreground with a four-hour process timeout, never through a pipe.
Full build logs and temporary dependencies stay outside this output directory.
Bounded receipt logs are below 200 KB; no toolchain or tree export is stored here.

## Delivery and limits

All three assignment items are complete: R329-3 F1/S1, the whole-tree sweep,
and R328-3 S1 diagnostic tags. The full replacement body is `PR-BODY.md`.
No push or review edit was performed. No merge, other checkout, hardware,
or submodule edit was performed. No additional review verdict is claimed.
Broader prior-round suite, builder, synthesis and hardware evidence was not rerun.
Independent re-review, publication and hosted acceptance remain with the maintainer.

Public review-ready comment: https://github.com/kebag-logic/milan-fpga/issues/502#issuecomment-5854406717

The posted body is preserved in `REVIEW-READY.md`. No further repository or remote action followed publication.
