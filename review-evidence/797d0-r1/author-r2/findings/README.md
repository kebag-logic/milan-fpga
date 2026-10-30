# D0 findings for the #797 area lanes (round 2)

Verified against dev `1e80128f`, the lane's base, at the round-2 head. The two per-lane files beside this one
are generated from the in-tree data file by `python3 scripts/docs_inventory.py --findings-dir <dir>`; the same 62
findings are the Findings table of the regenerated `docs/DOCUMENTATION_AUDIT.md`, so the page and these files
cannot disagree. Each finding has the page and line, the exact statement, the source line or clause that
contradicts it, and the correction.

A page with an open finding is never current: the generator renders it stale, and `--check` fails a committed
page that marks such a page current. An area lane that fixes a statement removes its entry from
`scripts/docs_inventory.json` and regenerates the page in the same commit.

| Area lane | File | Findings | Pages (finding count) |
|---|---|---:|---|
| overview and guides | [overview-and-guides.md](overview-and-guides.md) | 10 | `README.md` 8, `docs/guides/VERIFICATION_DEVELOPER.md` 2 |
| reference (with integration) | [reference.md](reference.md) | 52 | `REGISTER_MAP.md` 12, `MILAN_COMPLIANCE_MATRIX.md` 7, `REGISTER_MAP_CLASSES.md` 6, `PP_DESCRIPTOR_OWNERSHIP.md` 6, `QSPI_FLASHBOOT.md` 5, `BAREMETAL_FIRMWARE.md` 5, `BOARD_PORTING_AX7101.md` 3, `FR_NFR.md` 3, `AXIS_CORES_ON_BAREMETAL_SOC.md` 2, `TRACE_EVENTS.md` 2, `EGRESS_QUEUE_MAP.md` 1 |
| design, testing and CI, findings, module READMEs | none | 0 | outside D0's verification set; the inventory marks them "area lane" |

Round 1 recorded D0-001 to D0-023. Round 2 adds D0-024 to D0-062:

- **The two reviews' findings** (D0-024 to D0-033): `QSPI_FLASHBOOT.md` persistence (R742-1 F1), the aggregate
  Migen runner and the host C harness (R742-1 F2), the swapped q2/q3 roles (R742-1 F3), four compliance-matrix
  rows resting on the uninstantiated chain (R741-1 F1) and the bare-metal default on
  `AXIS_CORES_ON_BAREMETAL_SOC.md` (R741-1 F2).
- **The deeper sampling** (D0-034 to D0-062): the MAC crossing type, the AEM copy routine, the SPI read mode and the
  named-config sentence (integration); the cache size and the refused `--xlen 64` command (AX7101 porting); four
  persistence statements and two stale descriptions on `REGISTER_MAP_CLASSES.md`; the timestamp owner on the
  matrix; the roadmap's closed #394 item and "the write side" (README); the trace producer the shipping image
  does not link and the journal event's retired CSRs; six stale measurements on `PP_DESCRIPTOR_OWNERSHIP.md`,
  recomputed with `scripts/audit_pp_descriptors.py`; the bare-metal default on `FR_NFR.md`; four
  `REGISTER_MAP.md` statements (the presentation offset, two persistence claims, the shipping shape); the missing
  `TCAM_CTRL` row and the superseded route record on `BAREMETAL_FIRMWARE.md`.

## Pages that must wait for a running lane

Findings are recorded, not fixed. Open PRs at the round-2 start: #813 (dev) edits `docs/reference/SUBMODULES.md`
and `docs/guides/gptp/*.md`; #810 and #812 (`dev-soft-core`) edit `docs/reference/FR_NFR.md` and
`docs/ARCHITECTURE_HW_SW_SPLIT.md`. The [A10] release list also holds `CHANGELOG.md`, `docs/design/AREA_BUDGET.md`,
`docs/testing/TESTING.md`, `docs/integration/BUILDING.md`, `docs/integration/BAREMETAL_FIRMWARE.md`,
`docs/design/REBOOT_RESET.md` and the diagrams. Held pages with findings: `BAREMETAL_FIRMWARE.md` (D0-011,
D0-012, D0-013, D0-061, D0-062) and `FR_NFR.md` (D0-019, D0-020, D0-056). `SUBMODULES.md`, `BUILDING.md` and the
gPTP guides carry none.

## Consistency: one statement, one judgement

D0-001 (`README.md`), D0-033 (`AXIS_CORES_ON_BAREMETAL_SOC.md`) and D0-056 (`FR_NFR.md`) are the same sentence
shape: "Mark II selects each function ... Its default is bare-metal control", beside a line saying all-fabric is
the shipping default. `docs/ARCHITECTURE_HW_SW_SPLIT.md` lines 3-6 use the same shape for its "Mark II default
placement" (outside D0's page set, held by #810 and #812). The correction is the same on all three: name the
Mark II placement's default and the build's default separately.

## The scope addition (issuecomment-6489587365) checked against the code

Unchanged from round 1: five items are confirmed and filed (D0-014 to D0-018). Two statements in the scope
addition are contradicted by the code and need a decision before the reference lane writes them:

1. ETH_GUARD does not gate the LiteX PHY CRG reset: `sw/litex/milan_soc.py` lines 2067-2070 export the guard
   "for future SoC-side gating" and nothing consumes `self.eth_guard`; the RTL comments in
   `hdl/common/csr/milan_csr.sv` (lines 708 and 889-890) claim the gating.
2. The firmware does write MAC_STATUS: `phy_link_tick()` publishes the MDIO-resolved link, speed and duplex, but only
   while the saved-state writer runs (D0-009, D0-017).

## Incidental source-comment errors (outside D0's page scope)

Recorded for #746 or the reference lane, not fixed here:

- `hdl/common/csr/milan_csr.sv` lines 708 and 889-890, and `tb/verilator/csr/milan_csr_ref.sv` line 887: the
  ETH_GUARD-gates-the-CRG claim above.
- `hdl/common/csr/milan_csr.sv` around line 2012 and `hdl/milan/milan_datapath.sv` line 66 call the AX7101
  axis clock 100 MHz; `configs/endstation_ax7101_1x1_tdm8.yaml` line 44 sets `milan_clk_hz` to 50 MHz.
- `hdl/milan/KL_pp_shadow.sv` line 688 and `hdl/milan/milan_datapath.sv` line 8651 cite 802.1Q 35.2.2.7.4, the
  miscitation of D0-006 (review suggestion S2).
- `sw/trace/gen_trace_events.py` line 117 and `sw/trace/milan_trace.yaml` carry the text of D0-048 and D0-049;
  the fix for that generated page is in its generator.

## Verification coverage

The per-page sentence counts are [`../sampling/README.md`](../sampling/README.md), with one ledger per page. The
mechanical checks (paths, issue and PR states, CSR addresses and access classes, VERSION literals, clause and
table numbers, commands, matrix clauses, descriptor identifiers and the descriptor audit) are the tools under
`../tools/` and their output under `../sampling/` and `../receipts/sampling/`.
