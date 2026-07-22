# System diagrams

- **`milan_system_map.drawio`** — THE GIANT single-page system map (4640x2980):
  the complete AX7101 SoC + NIC datapath with every block, bus width and
  byte-lane convention on every edge, clock domains by colour, DMA/ring
  geometry, and all address maps (SoC, milan_csr, AEM store, QSPI slots,
  control-plane frame formats). Rendered: `.svg` / `.png`.
  Regenerate: `python3 milan_system_map.gen.py milan_system_map.drawio`,
  render with `../../hdl/ieee17221/aecp/doc/atdecc_architecture.render.py`.
- The ATDECC subsystem's own multi-page deep-dive (per-block, bit level) lives
  in `hdl/ieee17221/aecp/doc/atdecc_architecture.drawio` (pages 1-9).
