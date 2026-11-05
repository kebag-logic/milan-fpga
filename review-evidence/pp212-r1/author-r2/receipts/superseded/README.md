# Superseded runs (kept, not cited as gate results)

- `aecp-dispatch-first-start/`: the first AECP-dispatch campaign start, stopped after 4
  minutes to move the long D3 campaign into its own chain. The gate result is
  `campaigns/aecp-dispatch-a2fce43/`.
- `host-reset-1310/`: the ACMP, AECP-dispatch and D3 campaigns and the parent's
  firmware-control shard (1 of 4), each stopped mid-run by the host reset at 13:10 on
  2026-11-05. No arm had escaped in these partial logs. Each gate was run again from the
  start on the same clean clones. The results are `campaigns/acmp-a2fce43/`,
  `campaigns/aecp-dispatch-a2fce43/`, `campaigns/d3-a2fce43/` and
  `parent/pin-a2fce43/fw_shard1.*`.
