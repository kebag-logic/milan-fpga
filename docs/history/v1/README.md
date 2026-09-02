# Version one history

These pages preserve obsolete version-one documentation. Nothing here defines
current behavior.

<!-- docs-check: allow-dead-refs -->

## Contents

- **[Read safely](#read-safely)** — Check provenance before reusing evidence.
- **[Required metadata](#required-metadata)** — Preserve dates, original paths, and successors.
- **[Issue #259 exception](#issue-259-exception)** — Apply the target-only history exception.
- **[Archived pages](#archived-pages)** — Find retained non-product history.
- **[Historical diagram files](#historical-diagram-files)** — Find retained obsolete visual artifacts.

## Read safely

- Confirm the archived date.
- Read the stated historical purpose.
- Open the named current successor.
- Never derive current requirements here.
- Use Git for detailed evolution.

## Required metadata

Every migrated page declares these fields.

> Status: Historical
>
> Original path: repository-relative path
>
> Archived: YYYY-MM-DD
>
> Relocated: YYYY-MM-DD
>
> Current successor: repository-relative link

Replacements may add `Replaced in place: yes`. Each page retains its original
obsolete header.

## Issue #259 exception

The general archive preserves useful obsolete evidence.

Issue #259 removes superseded target-only material from checkout.

That material remains available only in Git history.

Never restore it through an archive move.

Issue #304 adds one clean throughput measurement record. Its full original
prose stays in Git history.

The later, specific #304 instruction overrides this rule. A gate-clean
page still keeps checkouts clean.

- Archive total: 17 Markdown pages.

## Archived pages

| Historical page | Original path | Archived | Why archived | Current successor |
|---|---|---|---|---|
| [Conformance testing guide (historical)](tests/CONFORMANCE_TESTING_HOWTO.md) | `tests/CONFORMANCE_TESTING_HOWTO.md` | 2026-08-31 | Deleted feature inventory | [Test index](../../../tests/README.md) |
| [MVP talker (historical)](MVP_TALKER.md) | `docs/MVP_TALKER.md` | 2026-08-31 | Expired milestone assumptions | [Dataplane walkthrough](../../fpga/DATAPLANE_WALKTHROUGH.md) |
| [NxN architecture (historical)](NXN_ARCHITECTURE.md) | `docs/NXN_ARCHITECTURE.md` | 2026-08-31 | Mixed ownership eras | [Architecture](../../overview/ARCHITECTURE.md) |
| [Specification traceability (historical)](SPEC_TRACEABILITY.md) | `docs/SPEC_TRACEABILITY.md` | 2026-08-31 | Stale manual tallies | [Module matrix](../../traceability/MODULE_MATRIX.md) |
| [Talker state machine (historical)](design/MILAN_TALKER_SM.md) | `docs/design/MILAN_TALKER_SM.md` | 2026-08-31 | Deleted local engines | [Architecture](../../overview/ARCHITECTURE.md) |
| [Static ADP shape (historical)](findings/ADP_SHAPE_STATIC_0727.md) | `docs/findings/ADP_SHAPE_STATIC_0727.md` | 2026-08-31 | Fixed generated-shape finding | [End-station builder](../../ENDSTATION_BUILDER.md) |
| [Throughput campaign record (historical)](findings/PERFORMANCE_GOAL.md) | `docs/findings/PERFORMANCE_GOAL.md` | 2026-09-02 | Closed retired-platform campaign | [Full FPGA solution](../../overview/FULL_FPGA_SOLUTION.md) |
| [Media-clock lock (historical)](findings/MEDIA_CLOCK_LOCK_0810.md) | `docs/findings/MEDIA_CLOCK_LOCK_0810.md` | 2026-08-31 | Superseded diagnosis | [Time synchronization](../../design/TIME_SYNC.md) |
| [Protocol area measurement (historical)](findings/PP_SHADOW_AREA_0812.md) | `docs/findings/PP_SHADOW_AREA_0812.md` | 2026-08-31 | Pre-integration measurement | [Area budget](../../design/AREA_BUDGET.md) |
| [Dependency matrix (historical)](reference/MILAN_V12_DEPENDENCY_MATRIX.md) | `docs/reference/MILAN_V12_DEPENDENCY_MATRIX.md` | 2026-08-31 | Stale manual dependencies | [Requirements register](../../reference/FR_NFR.md) |
| [Protocol traceability (historical)](reference/PROTOCOL_TRACEABILITY.md) | `docs/reference/PROTOCOL_TRACEABILITY.md` | 2026-08-31 | Superseded engine mapping | [Module matrix](../../traceability/MODULE_MATRIX.md) |
| [Compliance matrix (historical)](testing/MILAN_COMPLIANCE_MATRIX.md) | `docs/testing/MILAN_COMPLIANCE_MATRIX.md` | 2026-08-31 | Contradicted manual statuses | [Feature ledger](../../reference/MILAN_FEATURE_STATUS.md) |
| [Getter-setter verification (historical)](testing/PDU_GETTER_SETTER_VERIFICATION.md) | `docs/testing/PDU_GETTER_SETTER_VERIFICATION.md` | 2026-08-31 | Superseded landing plan | [Milan audit](../../testing/MILAN_V12_AUDIT_2026-08-16.md) |
| [Protocol sweep (historical)](testing/PROTOCOL_SWEEP_PLAN.md) | `docs/testing/PROTOCOL_SWEEP_PLAN.md` | 2026-08-31 | Invalidated execution plan | [Running tests](../../testing/RUNNING_TESTS.md) |
| [IEEE 1722 traceability (historical)](traceability/ieee1722-2016.md) | `docs/traceability/ieee1722-2016.md` | 2026-08-31 | Stale module rows | [Module matrix](../../traceability/MODULE_MATRIX.md) |
| [IEEE 1722.1 traceability (historical)](traceability/ieee1722_1-2021.md) | `docs/traceability/ieee1722_1-2021.md` | 2026-08-31 | Superseded control mapping | [Milan audit](../../testing/MILAN_V12_AUDIT_2026-08-16.md) |
| [Milan profile traceability (historical)](traceability/milan-v12.md) | `docs/traceability/milan-v12.md` | 2026-08-31 | Stale profile verdicts | [Requirements register](../../reference/FR_NFR.md) |

## Historical diagram files

| Historical asset | Original path | Reason |
|---|---|---|
| [`ROOT_DOC_MAP.drawio` (historical)](diagrams/ROOT_DOC_MAP.drawio) | `DOC_MAP.drawio` | Superseded audience map |
| [`ROOT_DOC_MAP.svg` (historical)](diagrams/ROOT_DOC_MAP.svg) | `DOC_MAP.svg` | Superseded audience render |
| [`perf_campaign.svg` (historical)](diagrams/perf_campaign.svg) | `docs/perf_campaign.svg` | Closed campaign chart render |
| [`perf_campaign_chart.py` (historical)](diagrams/perf_campaign_chart.py) | `docs/perf_campaign_chart.py` | Closed campaign chart generator |
