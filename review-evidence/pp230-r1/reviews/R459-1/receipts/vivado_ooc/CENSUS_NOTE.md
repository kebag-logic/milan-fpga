# census.tsv columns

`pattern <TAB> flip-flops <TAB> distributed-RAM cells <TAB> block-RAM cells`

- Only the flip-flop column (`PRIMITIVE_GROUP == FLOP_LATCH`, cell name matching `*<pattern>_reg*`) is meaningful.
- The RAM and BRAM columns read 0 throughout. The probe filtered on group names (`DISTRIBUTED_MEMORY`, `BLOCKRAM`) that
  7-series cells do not carry. For the RAM mapping, use `ram.rpt`, `util_hier.rpt` and the "Distributed RAM / Block RAM:
  Final Mapping Report" sections of `vivado.log`.
- `sid_r` also matches `a_sid_r`, `fsysid_r` and the listener `sid_r`. `mfs_r` and `mif_r` also match the top's
  `a_mfs_r`, `adm_mfs_r` and similar names. `lat_r` also matches the listener's registration `lat_r`. Read those rows
  as name-pattern totals, not single registers.
