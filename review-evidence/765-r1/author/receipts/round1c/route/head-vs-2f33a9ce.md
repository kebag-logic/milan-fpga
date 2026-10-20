# route-1x1 at 75db4b57 against round 1b's route at 2f33a9ce

Build inputs differ by two RTL comment lines (git diff 2f33a9ce 75db4b57 -- hdl).

| Report | SHA-256 head (first 16) | SHA-256 2f33a9ce (first 16) | Body compare |
|---|---|---|---|
| `alinx_ax7101_timing.rpt` | `377b7ce95fe27bcc` | `79576ed304c52bd9` | from the Design Timing Summary to the end, work-directory prefix removed: 0 differing lines |
| `alinx_ax7101_utilization_place.rpt` | `de2e8738b328bff4` | `65966a050764c743` | header lines (Date, Tool Version, Host, Command, Design) removed: 0 differing lines |
| `alinx_ax7101_utilization_hierarchical_place.rpt` | `1a5f412a776ddb74` | `f65322b48bd8d26e` | header lines (Date, Tool Version, Host, Command, Design) removed: 0 differing lines |
| `alinx_ax7101_utilization_hierarchical_synth.rpt` | `b4ffbfb8ef5018e0` | `78c944cd762f2fe6` | header lines (Date, Tool Version, Host, Command, Design) removed: 0 differing lines |
| `alinx_ax7101_route_status.rpt` | `ce9b87928ee6b6b3` | `ce9b87928ee6b6b3` | header lines (Date, Tool Version, Host, Command, Design) removed: 0 differing lines |

Full timing report, head: SHA-256 377b7ce95fe27bccc825787b1a0a45f8ada3bcf6d048dc695fc60545e44ea39d, 1294971 bytes (kept in scratch).
`timing_summary.txt` and `worst_setup_path.txt` are byte-identical to round 1b's (`../../round1b/route/cand-2f33a9ce/`): yes / yes.
