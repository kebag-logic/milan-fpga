# R496-2 reviewer scripts

All scripts are reviewer-owned probes. They write only into the paths they are
given (the review used `scratch/` under the packet), never into the checkout
under review. `TREE` is a checkout of `a3ea8ffe16585270911705ffabd68ca5e17fc9e0`
with `protocol-processor`, `gptp-processor` and `third_party/verilog-axis`
initialised; `DEVTREE` is the same at dev `510fae60b26bef1db138de5cf2ac72b17b5011a5`.

| Script | What it does | Run |
|---|---|---|
| `default_build_probe.py` | runs the end-station builder for one shipped config, then that tree's own `milan_soc.py` with `--no-compile-software --no-compile-gateware` (extra arguments appended, e.g. `--ctrl-mailbox` or the Arty `--sys-clk-freq 100e6` proxy) | `PYTHONHASHSEED=0 <litex python> default_build_probe.py TREE endstation_<cfg> OUT [args]` |
| `normalise_compare.py` | compares two exports after removing paths, date stamps and LiteX's comment-only hierarchy tree; `litex.log` (a console transcript with interleaved writers) is compared as a sorted line set | `normalise_compare.py OUT_A/soc TREE_A OUT_B/soc TREE_B` |
| `reviewer_rtl_probes.py` | 12 RTL defects that are not in the lane's `mutants.py`, planted and built with that file's own helpers | `PATH=<verilator 5.050>:$PATH reviewer_rtl_probes.py TREE SCRATCH --jobs 3` |
| `reviewer_rtl_probes_a2.py` | two defects aimed at the A2 (W before AW) group | `reviewer_rtl_probes_a2.py TREE SCRATCH` |
| `axil_stream_probe.patch.py` | adds one data-checked back-to-back write stream (RP0) to a SCRATCH copy of `axil_checks.hpp`; run `make run-axil` in that copy with the head RTL and with the drain-cycle WREADY defect | see `receipts/axil_stream_probe.txt` |
| `reviewer_fw_probes.py` | 9 firmware defects that are not in `ctrl_mutants.py`, planted with its own helper and graded by the named arm | `reviewer_fw_probes.py TREE SCRATCH` |
| `tick_carry_probe.c` | a 40-centisecond TICK backlog, then one more centisecond arriving while 24 are carried; exit 0 when all 41 reach the consumer | compile with `mbx.c ctrl_loop.c mbx_model.c mbx_plat_host.c` and `-I` for `mbx wire host port loop`; see `receipts/tick_carry_probe.txt` |

Exit codes: the probe drivers exit 0 when they ran; each line reports
`caught` or `ESCAPED`. `tick_carry_probe` exits 1 on the planted copy by design.
