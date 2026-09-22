<!-- SPDX-License-Identifier: CERN-OHL-W-2.0 -->
# Documentation Guide — Conventions, Reading Order, Audiences

This directory specifies the architecture of an IEEE 1722.1-2021 protocol processor
implementing the control plane of a **non-redundant Milan v1.2 PAAD**.

> **Looking for a place to start reading, not a place to start writing?**
> Go to [`guides/`](guides/README.md) — three task-shaped entry points, one for someone
> [modifying a module](guides/hdl-engineer.md), one for someone
> [integrating the top into an SoC](guides/integrator.md), and one for someone
> [bringing a board up](guides/operator.md). They index into the architecture documents
> below.

This page is for **authors**: it defines the conventions every architecture document
relies on. Read it before editing anything under `architecture/`.

## 1. Reading order

Read top to bottom on a first pass. Each row says what the document answers and what
it assumes you have already read, so a row can also be entered directly once its
"Read after" column is covered.

| Step | Document | What it answers | Read after | Why it sits here |
|---|---|---|---|---|
| 0 | [docs/README.md](README.md) (this page) | the conventions, IDs and figure rules every other page relies on | nothing | the IDs below (`F`, `REQ`, `T`, `P`, `Δ`) are defined in [section 2](#2-identifier-registries) |
| 1 | [00 Compliance review](00_MILAN_COMPLIANCE_REVIEW.md) | why the architecture looks the way it does: the gap findings and the compliance matrix | step 0 | the requirements the other pages trace to; implementers may skim it now and return on a second pass |
| 2 | [01 Overview](architecture/01_overview.md) | scope, top level, parameters, the Milan-over-IEEE deltas | step 1 | names every engine and every `P-` and `Δ` ID used later |
| 3 | [02 External interfaces](architecture/02_interfaces.md) | every external contract: streams, engine API, events, status, side-port, NVM | step 2 | the engines are described in terms of these interface classes |
| 4 | [03 Packet engine](architecture/03_packet_engine.md) | the shared RX/TX datapath all engines sit on | step 3 | every protocol engine receives from and transmits through it |
| 5 | [04 ADP engine](architecture/04_adp_engine.md) | discovery: the entity's advertisement and the ADP events the other engines consume | step 4 | ACMP consumes ADP events, so 04 comes before 05 |
| 6 | [05 ACMP engine](architecture/05_acmp_engine.md) | Milan connection management, the listener and talker state machines | step 5 | it calls into SRP and MAAP, which the next two steps define |
| 7 | [10 SRP engine](architecture/10_srp_engine.md) | the MSRP/MVRP endpoint participant behind ACMP's reservation calls | step 6 | read with or right after 05: it serves 05's `srp` calls |
| 8 | [11 MAAP engine](architecture/11_maap_engine.md) | dynamic multicast address acquisition behind ACMP's address calls | step 6 | read with or right after 05: it serves 05's `maap` calls; independent of step 7 |
| 9 | [06 AECP engine](architecture/06_aecp_engine.md) | AEM and Milan Vendor Unique commands, the command master table | steps 6 to 8 | its commands read and change the state the earlier engines own |
| 10 | [07 Memory maps](architecture/07_memory_maps.md) | records, register and memory layouts, persistence | step 9 | the single home of every layout the engine pages link to |
| 11 | [08 Timing](architecture/08_timing.md) | every timer, deadline and tick source (`T-` IDs) | step 10 | the single home of every timing value the state machines cite |
| 12 | [09 Verification](architecture/09_verification.md) | test categories, coverage goals, how compliance is demonstrated | step 11 | it walks the tables and timers of all the pages above |

Not on the path: [10 Resource and effort](10_RESOURCE_AND_EFFORT.md) sizes the
implementation on the reference platform; read it for planning, after step 2. It is a
different document from step 7's `architecture/10_srp_engine.md`.

### Paths by role

Steps refer to the table above.

| Role | Path | Entry points worth bookmarking |
|---|---|---|
| Implementer (RTL) | steps 2, 3, 4, 5, 6, 7, 8, 9, 10, 11 in order; step 1 on the second pass | [F05.3 listener matrix](architecture/05_acmp_engine.md#fig-05-listener-matrix), [F06.14 command master table](architecture/06_aecp_engine.md#fig-06-cmdtable) |
| Verifier | step 1's [compliance matrix](00_MILAN_COMPLIANCE_REVIEW.md#6-compliance-matrix-f001), then steps 2, 11, 12, then the two behavior tables | [09 test categories](architecture/09_verification.md#3-test-categories), [F05.3](architecture/05_acmp_engine.md#fig-05-listener-matrix), [F06.14](architecture/06_aecp_engine.md#fig-06-cmdtable) |
| System integrator | steps 2 and 3, then persistence, then the side-port | [07 persistence](architecture/07_memory_maps.md#5-persistence), [02 management side-port](architecture/02_interfaces.md#fig-02-memwave) |
| Compliance reviewer | step 1 only, following its links into the architecture | [00 gap findings](00_MILAN_COMPLIANCE_REVIEW.md#5-gap-findings), [00 compliance matrix](00_MILAN_COMPLIANCE_REVIEW.md#6-compliance-matrix-f001) |

## 2. Identifier registries

Every normative artifact has a stable ID. IDs never change meaning; new ones are appended.

| Prefix | Meaning | Defined in |
|---|---|---|
| `F<doc>.<n>` | Figure/table of documentation rank (e.g. `F05.3`) | the host document |
| `REQ-<AREA>-<nnn>` | Requirement row of the compliance matrix | 00 §6 |
| `GAP-<nn>` | Review finding | 00 §5 |
| `T-<ENGINE>-<NAME>` | Timing constant (e.g. `T-ACMP-CMD`) | **08 §2 only** |
| `P-<NAME>` | Synthesis-time parameter (e.g. `P-N-CONTROLLERS`) | **01 §7 only** |
| `A<n>` | Listener-state-machine action primitive | 05 §6.3 legend |
| `Δ<n>` | Milan-overrides-IEEE delta | **01 §6 only** |

**Single-source rules** — a value lives in exactly one table; everywhere else references the ID:
- Timing values only in `F08.1`. FSM arcs are labeled `T-…`, never `200 ms`.
- Parameter values only in `F01.5`.
- External status signal names only in `F02.10`.
- Milan↔IEEE deltas only in `F01.4`; documents cite `Δn`.
- Record/memory layouts only in 07; engine docs link to them.

Scope of those rules: they bind the **architecture** documents (01–10). Three
deliberate exceptions: the compliance review (00) quotes spec requirement text
*including its values* — that is its job; tick-generation rates belong to the clocking
contract (02 §2 with `F08.2`); and PDU field constants such as ADP `valid_time` belong
to their field-sourcing table. `make check` enforces the rest.

## 3. Figures: one source, one home

- Every figure exists in **exactly one** host document, preceded by an explicit anchor:
  `<a id="fig-05-listener-matrix"></a>`. Reuse is a relative link, never a copy.
- **Mermaid** (block/FSM/sequence/flow): fenced ` ```mermaid ` blocks — the fence *is* the
  editable source. Style: one diagram per fence; no `%%{init}%%` theming; stable
  lower-kebab node IDs; no HTML labels; `stateDiagram-v2` for FSMs, `sequenceDiagram`
  for on-the-wire flows, `flowchart` for datapaths/decision trees, `classDiagram` only
  for the descriptor tree.
- **WaveDrom** (waveforms and PDU/register bit layouts): GitHub does **not** render
  WaveDrom natively, so every block appears as a committed SVG
  (`docs/diagrams/wavedrom/<anchor>.svg`, rendered by `make wavedrom` via the Python
  `wavedrom` package) with the fenced ` ```wavedrom ` source — still the single
  editable artifact — collapsed in a `<details>` block directly below the image.
  Sources are **strict JSON** (double-quoted keys). `reg` conventions: fields listed in
  wire order render **bottom lane first** (standard bitfield layout — every caption
  says so); field names carry the byte offset (`@n`) or mask where ambiguity is
  dangerous; keep fields ≤ 64 bits (wider fields leave unlabeled middle lanes); `head`/
  `foot` text is signal-format-only — for `reg`, put it in the caption. Editing a block
  without re-rendering fails `make check` (`wavedrom-check`).
- **draw.io** (the three richest pictures only): source `docs/diagrams/src/<name>.drawio`,
  committed export `docs/diagrams/<name>.svg`, embedded via `![…](../diagrams/<name>.svg)`.
  Regenerate with `make diagrams` (see `docs/diagrams/README.md`).
- Interface waveforms are **class templates** (one per interface class); per-instance
  differences live in signal tables, never in cloned waveforms.

## 4. Spec citation and terminology

- Citations are plain text: `(Milan §5.5.3.5)`, `(IEEE 1722.1 §8.2.1)`, `(IEEE 1722.1
  Table 7-140)` — no links to the (non-distributed, copyrighted) PDFs.
  Milan page references are *printed* pages (printed = PDF − 7).
- **Milan naming is primary**: `BIND_RX` (IEEE `CONNECT_RX`), `UNBIND_RX`
  (`DISCONNECT_RX`), `PROBE_TX` (`CONNECT_TX`). The IEEE name appears in parentheses at
  first use per document. Precedence: where Milan differs from IEEE 1722.1, **Milan wins**
  (Milan §5.5.2.1); every such point is tagged with a `Δn` callout:

  > **Δn — Milan overrides IEEE:** one-line statement. *(template)*

- Bit-numbering warning, repeated verbatim above every mask table:

  > ⚠ Bit tables in Milan and IEEE 1722.1 are **MSB-first** (bit 31 ⇔ mask
  > `0x00000001`). The **hex mask column is authoritative**; never derive shifts from
  > bit-number columns.

- PDU length rule: total PDU size = `control_data_length` **+ 12** (figures in IEEE
  1722.1-2021 printing `+ 8` are an erratum). Padding to minimum Ethernet frame is
  **excluded** from `control_data_length`.

## 5. Sequence-diagram participants (fixed vocabulary)

All `sequenceDiagram` figures use these participant names so separate diagrams compose
into one story:

| Name | Is |
|---|---|
| `CTRL` | remote ATDECC controller |
| `TALKER` | remote talker entity (its ACMP/ADP/SRP behavior) |
| `ADP` / `ACMP` / `AECP` | the corresponding engine inside this processor |
| `NOTIF` | unsolicited-notification engine + controller registry |
| `SRP` | SRP/MSRP + MAAP adapter (and, transitively, the SRP network) |
| `GPTP` / `AVTP` / `MCLK` | gPTP / streaming / media-clock adapters |
| `NVM` | persistence manager |
| `TX` | TX arbiter / wire egress |

## 6. Editing workflow

| To change… | Do |
|---|---|
| A block/FSM/sequence figure | edit the ` ```mermaid ` fence in place; `make lint` |
| A waveform or bit layout | expand the `<details>` under the image, edit the ` ```wavedrom ` JSON in place, run `make wavedrom` (re-renders the SVG); `make check` |
| A top-level picture | edit `docs/diagrams/src/*.drawio` in the draw.io app; `make diagrams`; commit source **and** SVG |
| A timing value | edit `F08.1` only; consumers reference `T-…` IDs |
| A parameter default | edit `F01.5` only |
| Anything | `make check` (lint + links + matrix + stale) must pass before commit |
