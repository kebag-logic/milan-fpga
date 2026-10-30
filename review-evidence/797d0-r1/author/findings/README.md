# D0 findings for the #797 area lanes

Verified against dev `1e80128f` (the lane's base). The per-lane files in this directory are generated from the
in-tree data file by `python3 scripts/docs_inventory.py --findings-dir <dir>`; the same 23 findings are the
Findings table of the regenerated `docs/DOCUMENTATION_AUDIT.md`, so the public page and these files cannot
disagree. An area lane that fixes a statement removes its entry from `scripts/docs_inventory.json` and
regenerates the page in the same commit; a quote that leaves its page without that is rendered
"re-verify: quote not found" and the freshness gate fails until the page is regenerated.

| Area lane | File | Findings | Pages |
|---|---|---:|---|
| overview and guides | [overview-and-guides.md](overview-and-guides.md) | 6 | `README.md` |
| reference (includes integration, per the plan's ETH_GUARD scope) | [reference.md](reference.md) | 17 | `REGISTER_MAP.md` 8, `BAREMETAL_FIRMWARE.md` 3, `FR_NFR.md` 2, `MILAN_COMPLIANCE_MATRIX.md` 2, `REGISTER_MAP_CLASSES.md` 1, `BOARD_PORTING_AX7101.md` 1 |
| design, testing and CI, findings, module READMEs | none | 0 | not in D0's verification set; the inventory marks them "area lane" |

## Pages that must wait for a running lane

- `docs/integration/BAREMETAL_FIRMWARE.md` (D0-011, D0-012, D0-013) is on the [A10] release list.
- `docs/reference/FR_NFR.md` (D0-019, D0-020) is edited on `dev-soft-core` by open PR #810; fix on dev and let the
  next dev sync carry it, or coordinate with that lane.
- `docs/reference/SUBMODULES.md` and `docs/guides/gptp/*.md` (PR #813) carry no finding.

## Fixed in D0 (one-line factual errors on pages no running lane touches)

| File:line | Was | Now | Evidence |
|---|---|---|---|
| `docs/guides/VERIFICATION_DEVELOPER.md:129` | `python3 sw/litex/test_ring_dma.py` | `python3 sw/litex/test_gmii_rx_capture.py` | the old script was deleted in `ecf18de2`; the new one is in `scripts/run_litex_sims.sh`'s `INVENTORY` |
| `docs/README.md:72` | "Media-clock following, proposed" | "Media-clock following, implemented" | `docs/design/MEDIA_CLOCK_FOLLOWING.md` line 6 and `hdl/milan/milan_datapath.sv` lines 704-720 |
| `docs/reference/REGISTER_MAP.md:428` | "acceptance remains on #599" | links the #599 link-cycle finding | #599 closed as completed 2026-09-29; `docs/findings/599_394_E1_LINK_CYCLES.md` |

## The scope addition (issuecomment-6489587365) checked against the code

Five items are confirmed and filed as reference-lane findings (D0-014 ETH_GUARD row, D0-015 PHY_RESET inert and
`milan_mac_phy_crg_reset`, D0-016 LINK_CTRL[1] masking, D0-017 MAC_STATUS reset value, D0-018 the classes overlay).
Two statements in the scope addition are contradicted by the code at `1e80128f` and need a decision before the
reference lane writes them:

1. "the LiteX PHY clock/reset block's reset is blocked" / "ETH_GUARD gates it". Nothing in `sw/litex/milan_soc.py`
   consumes `self.eth_guard`: it is driven from the datapath's `o_eth_guard` (line 2070) with the comment "exported
   for future SoC-side gating of the LiteEth phy_crg_reset chain (v2)" (lines 2067-2069), and the CRG reset in
   `sw/litex/patches/0002-liteeth-gmii-tx-clk-invert.patch` drives `pads.rst_n` from `self._reset.storage` with no
   guard term. The RTL comment `hdl/common/csr/milan_csr.sv` lines 889-890 (copied in
   `tb/verilator/csr/milan_csr_ref.sv` line 887) claims the gating exists. Either the SoC gating is implemented
   (a code issue) or the map documents the CRG reset as ungated.
2. "MAC_STATUS ... nothing writes it. It does not follow the link." Since `f420e1a7` (#599, 2026-09-28) the
   firmware's `phy_link_tick()` (`sw/firmware/milan_baremetal/milan_baremetal.c` lines 1042-1075) publishes the
   MDIO-resolved link, speed and duplex into `milan_mac_link_status`. It runs from `nvm_heartbeat_tick()` (line 1094),
   which returns until `nvm_started` (line 1668) is set, so a refused record-set shape leaves MAC_STATUS at its reset
   value. D0-009 and D0-017 state the code's behaviour.

## Verification coverage (D0 release-facing set)

Mechanical checks over every release-facing page (`README.md`, `docs/README.md`, `docs/guides/**`,
`docs/integration/**`, `docs/reference/**`, `REQUIREMENTS.md`); the tools and their raw output are under
`../receipts/tools` and `../receipts/verification`:

| Check | Population | Result |
|---|---|---|
| Clause and table numbers exist in the cited standard (Milan v1.2, 1722.1-2021, 1722-2016, 802.1AS-2011 + Cor1/Cor2, 802.1Q-2018/2022, 802.1BA) | 239 citations | 234 resolve; 3 errors filed (D0-006, D0-007, D0-008); "Table 7.157" (dot form) cosmetic; "Milan 1.3 5.3.8.10" not checkable, no 1.3 text in the standards set |
| Every `A_*` CSR address in `milan_csr.sv` has a map row | 204 constants | only 0x7D8 missing (D0-014) |
| Literal reset values in the map equal `csr_default()` and the generated lwSRP defaults | every literal row | 0 mismatches |
| Printed commands name an existing script and existing flags | every command line | 1 error, fixed (`VERIFICATION_DEVELOPER.md:129`) |
| Requirement IDs cited are defined | 112 defined IDs | all resolve |
| Backticked code identifiers exist in the source (first-party and both processors) | every code span | 195 unmatched tokens triaged; 2 real (D0-004) |
| Issues described as open or pending are open | 35 issue numbers | 4 stale claims (D0-010, D0-011, D0-012, and the fixed `REGISTER_MAP.md:428`) |
| Register name and offset pairs on other pages equal the map | 9 pages | 0 mismatches |
| Generated pages are fresh | `MAILBOX_CONTRACT.md`, `TRACE_EVENTS.md` | both generators' `--check` rc 0 |
| Content gates | feature ledger, submodule docs, gPTP docs, solution docs | all rc 0 |

Pages read against source beyond the mechanical checks: `README.md` (whole), `docs/README.md` (whole), the five
role guides, `INTEGRATION_GUIDE.md`, `QSPI_FLASHBOOT.md`, `BOARD_PORTING_AX7101.md` status rows, the MAC, PHY and
link rows of `REGISTER_MAP.md`, the FR/NFR status table, the 802.1Q rows of `MILAN_COMPLIANCE_MATRIX.md`,
`EGRESS_QUEUE_MAP.md`'s scope paragraph and `REQUIREMENTS.md` sections 3, 4 (timestamp scope), 7 and 8 (numeric
statements). `BUILDING.md` and `BAREMETAL_FIRMWARE.md` (release lanes) and `PP_DESCRIPTOR_OWNERSHIP.md` received the
mechanical checks only; their prose is for the reference lane to read in full.
