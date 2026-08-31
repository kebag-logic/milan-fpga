# Version one history

These pages preserve obsolete version-one documentation.

Nothing here defines current behavior.

<!-- docs-check: allow-dead-refs -->

## Contents

- **[Read safely](#read-safely)** — Check evidence before reusing it.
- **[Required metadata](#required-metadata)** — Preserve provenance and successors.
- **[Migration record](#migration-record)** — Understand the archive consolidation.
- **[Archived pages](#archived-pages)** — Find every preserved page.

## Read safely

- Confirm the archived date.
- Read the stated historical purpose.
- Open the named current successor.
- Never derive current requirements here.
- Use Git for detailed evolution.

## Required metadata

Every migrated page declares five fields.

> Status: Historical
>
> Original path: repository-relative path
>
> Archived: YYYY-MM-DD
>
> Relocated: YYYY-MM-DD
>
> Current successor: repository-relative link

Each page retains its original obsolete header.

## Migration record

Earlier files used two historical storage patterns.

- Ten pages lived under `historical_now_obsolete/`.
- Thirty pages remained beside current documentation.
- One legacy index documented the earlier archive.
- Three obsolete diagram files remained current.

The 2026-08-31 migration preserved every tracked artifact.

## Archived pages

| Historical page | Original path | Archived | Why archived | Current successor |
|---|---|---|---|---|
| [TODO](TODO.md) | `TODO.md` | 2026-08-31 | Retired phase and platform snapshot | [Milan roadmap](../../MILAN_V12_ROADMAP.md) |
| [Conformance testing guide](tests/CONFORMANCE_TESTING_HOWTO.md) | `tests/CONFORMANCE_TESTING_HOWTO.md` | 2026-08-31 | Deleted feature inventory | [Test index](../../../tests/README.md) |
| [Compliance gaps](MILAN_COMPLIANCE_GAPS.md) | `docs/MILAN_COMPLIANCE_GAPS.md` | 2026-08-31 | Expired gap inventory | [Milan roadmap](../../MILAN_V12_ROADMAP.md) |
| [MVP talker](MVP_TALKER.md) | `docs/MVP_TALKER.md` | 2026-08-31 | Expired milestone assumptions | [Dataplane walkthrough](../../fpga/DATAPLANE_WALKTHROUGH.md) |
| [NxN architecture](NXN_ARCHITECTURE.md) | `docs/NXN_ARCHITECTURE.md` | 2026-08-31 | Mixed ownership eras | [Architecture](../../overview/ARCHITECTURE.md) |
| [Specification traceability](SPEC_TRACEABILITY.md) | `docs/SPEC_TRACEABILITY.md` | 2026-08-31 | Stale manual tallies | [Module matrix](../../traceability/MODULE_MATRIX.md) |
| [Systems engineer guide](SYSTEMS_ENGINEER_GUIDE.md) | `docs/SYSTEMS_ENGINEER_GUIDE.md` | 2026-08-31 | Replaced reader map | [Role guides](../../guides/README.md) |
| [CPU and FPGA split](architecture/CPU_FPGA_SPLIT.md) | `docs/architecture/CPU_FPGA_SPLIT.md` | 2026-08-31 | Duplicated ownership model | [Current ownership split](../../ARCHITECTURE_HW_SW_SPLIT.md) |
| [Area campaign](design/AREA_80_CAMPAIGN.md) | `docs/design/AREA_80_CAMPAIGN.md` | 2026-08-31 | Completed reduction campaign | [Area budget](../../design/AREA_BUDGET.md) |
| [Audio streaming](design/AUDIO_STREAMING.md) | `docs/design/AUDIO_STREAMING.md` | 2026-08-31 | Retired media topology | [Dataplane walkthrough](../../fpga/DATAPLANE_WALKTHROUGH.md) |
| [Talker state machine](design/MILAN_TALKER_SM.md) | `docs/design/MILAN_TALKER_SM.md` | 2026-08-31 | Deleted local engines | [Architecture](../../overview/ARCHITECTURE.md) |
| [Static ADP shape](findings/ADP_SHAPE_STATIC_0727.md) | `docs/findings/ADP_SHAPE_STATIC_0727.md` | 2026-08-31 | Fixed generated-shape finding | [End-station builder](../../ENDSTATION_BUILDER.md) |
| [Media-clock lock](findings/MEDIA_CLOCK_LOCK_0810.md) | `docs/findings/MEDIA_CLOCK_LOCK_0810.md` | 2026-08-31 | Superseded diagnosis | [Time synchronization](../../design/TIME_SYNC.md) |
| [Physical-family triage](findings/PHYSICAL_FAMILY_TRIAGE_0802.md) | `docs/findings/PHYSICAL_FAMILY_TRIAGE_0802.md` | 2026-08-31 | Superseded single-run triage | [Milan audit](../../testing/MILAN_V12_AUDIT_2026-08-16.md) |
| [Protocol area measurement](findings/PP_SHADOW_AREA_0812.md) | `docs/findings/PP_SHADOW_AREA_0812.md` | 2026-08-31 | Pre-integration measurement | [Area budget](../../design/AREA_BUDGET.md) |
| [RX performance tuning map](findings/RX_PERF_TUNING_MAP.md) | `docs/findings/RX_PERF_TUNING_MAP.md` | 2026-08-31 | Retired host-driver tuning map | [Performance goal](../../findings/PERFORMANCE_GOAL.md) |
| [Board profiling method](findings/PERF_ON_MILAN.md) | `docs/findings/PERF_ON_MILAN.md` | 2026-08-31 | Retired runtime profiling method | [Performance goal](../../findings/PERFORMANCE_GOAL.md) |
| [Known limitations snapshot](limitations/KNOWN_ISSUES_AND_LIMITATIONS.md) | `docs/limitations/KNOWN_ISSUES_AND_LIMITATIONS.md` | 2026-08-31 | Stale capability snapshot | [Milan audit](../../testing/MILAN_V12_AUDIT_2026-08-16.md) |
| [At a glance](overview/AT_A_GLANCE.md) | `docs/overview/AT_A_GLANCE.md` | 2026-08-31 | Stale status summary | [Documentation index](../../README.md) |
| [Dependency matrix](reference/MILAN_V12_DEPENDENCY_MATRIX.md) | `docs/reference/MILAN_V12_DEPENDENCY_MATRIX.md` | 2026-08-31 | Stale manual dependencies | [Requirements register](../../reference/FR_NFR.md) |
| [Protocol traceability](reference/PROTOCOL_TRACEABILITY.md) | `docs/reference/PROTOCOL_TRACEABILITY.md` | 2026-08-31 | Deleted engine mapping | [Module matrix](../../traceability/MODULE_MATRIX.md) |
| [Behave test plan](testing/BEHAVE_TEST_PLAN.md) | `docs/testing/BEHAVE_TEST_PLAN.md` | 2026-08-31 | Expired suite plan | [Test index](../../../tests/README.md) |
| [Compliance matrix](testing/MILAN_COMPLIANCE_MATRIX.md) | `docs/testing/MILAN_COMPLIANCE_MATRIX.md` | 2026-08-31 | Contradicted manual statuses | [Feature ledger](../../reference/MILAN_FEATURE_STATUS.md) |
| [Getter-setter verification](testing/PDU_GETTER_SETTER_VERIFICATION.md) | `docs/testing/PDU_GETTER_SETTER_VERIFICATION.md` | 2026-08-31 | Superseded landing plan | [Milan audit](../../testing/MILAN_V12_AUDIT_2026-08-16.md) |
| [Protocol sweep](testing/PROTOCOL_SWEEP_PLAN.md) | `docs/testing/PROTOCOL_SWEEP_PLAN.md` | 2026-08-31 | Invalidated execution plan | [Running tests](../../testing/RUNNING_TESTS.md) |
| [Protocol validation](testing/PROTOCOL_VALIDATION_MATRIX.md) | `docs/testing/PROTOCOL_VALIDATION_MATRIX.md` | 2026-08-31 | Stale validation matrix | [Testing guide](../../testing/TESTING.md) |
| [Torture campaign](testing/TORTURE_CAMPAIGN.md) | `docs/testing/TORTURE_CAMPAIGN.md` | 2026-08-31 | Retired campaign contract | [Running tests](../../testing/RUNNING_TESTS.md) |
| [IEEE 1722 traceability](traceability/ieee1722-2016.md) | `docs/traceability/ieee1722-2016.md` | 2026-08-31 | Stale module rows | [Module matrix](../../traceability/MODULE_MATRIX.md) |
| [IEEE 1722.1 traceability](traceability/ieee1722_1-2021.md) | `docs/traceability/ieee1722_1-2021.md` | 2026-08-31 | Deleted control mapping | [Milan audit](../../testing/MILAN_V12_AUDIT_2026-08-16.md) |
| [Milan profile traceability](traceability/milan-v12.md) | `docs/traceability/milan-v12.md` | 2026-08-31 | Stale profile verdicts | [Requirements register](../../reference/FR_NFR.md) |
| [Campaign 500 plan](findings/CAMPAIGN_500_PLAN.md) | `historical_now_obsolete/findings/CAMPAIGN_500_PLAN.md` | 2026-07-23 | Completed gated plan | [Performance goal](../../findings/PERFORMANCE_GOAL.md) |
| [Gigabit headroom](findings/GIGABIT_HEADROOM_ANALYSIS.md) | `historical_now_obsolete/findings/GIGABIT_HEADROOM_ANALYSIS.md` | 2026-07-25 | Consolidated budget model | [Performance goal](../../findings/PERFORMANCE_GOAL.md) |
| [RX overload wedge](findings/RX_OVERLOAD_WEDGE.md) | `historical_now_obsolete/findings/RX_OVERLOAD_WEDGE.md` | 2026-07-23 | Fixed receive-storm defect | [Pipeline stages](../../fpga/PIPELINE_STAGES.md) |
| [RX ring DMA](findings/RX_RING_DMA.md) | `historical_now_obsolete/findings/RX_RING_DMA.md` | 2026-07-23 | Superseded byte-ring design | [Pipeline stages](../../fpga/PIPELINE_STAGES.md) |
| [RX and TX performance](findings/RX_TX_PERFORMANCE.md) | `historical_now_obsolete/findings/RX_TX_PERFORMANCE.md` | 2026-07-25 | Consolidated campaign narrative | [Performance goal](../../findings/PERFORMANCE_GOAL.md) |
| [Single-port performance](findings/SINGLE_PORT_PERF.md) | `historical_now_obsolete/findings/SINGLE_PORT_PERF.md` | 2026-07-25 | Consolidated latency conclusion | [Latency investigation](../../findings/LATENCY_INVESTIGATION.md) |
| [TX reader prefetch](findings/TX_READER_PREFETCH_PLAN.md) | `historical_now_obsolete/findings/TX_READER_PREFETCH_PLAN.md` | 2026-07-23 | Completed rejected plan | [Pipeline stages](../../fpga/PIPELINE_STAGES.md) |
| [Header-split design](fpga/HSPLIT14_DESIGN.md) | `historical_now_obsolete/fpga/HSPLIT14_DESIGN.md` | 2026-07-25 | Consolidated cut-through design | [Header-split design](../../fpga/HEADER_SPLIT_DESIGN.md) |
| [Receive coalescing](fpga/HW_GRO_RSC.md) | `historical_now_obsolete/fpga/HW_GRO_RSC.md` | 2026-07-23 | Consolidated coalescing campaign | [Pipeline stages](../../fpga/PIPELINE_STAGES.md) |
| [Open-source migration](integration/OPEN_SOURCE_MIGRATION.md) | `historical_now_obsolete/integration/OPEN_SOURCE_MIGRATION.md` | 2026-07-23 | Completed vendor-removal plan | [Porting guide](../../integration/PORTING_GUIDE.md) |
| [Legacy archive index](LEGACY_ARCHIVE_INDEX.md) | `historical_now_obsolete/README.md` | 2026-08-31 | Replaced archive index | [Current history index](README.md) |

## Historical diagram files

| Historical asset | Original path | Reason |
|---|---|---|
| [`ROOT_DOC_MAP.drawio`](diagrams/ROOT_DOC_MAP.drawio) | `DOC_MAP.drawio` | Superseded audience map |
| [`ROOT_DOC_MAP.svg`](diagrams/ROOT_DOC_MAP.svg) | `DOC_MAP.svg` | Superseded audience render |
| [`RX_PERF_TUNING_MAP.drawio`](diagrams/RX_PERF_TUNING_MAP.drawio) | `docs/RX_PERF_TUNING_MAP.drawio` | Retired host-driver tuning map |
