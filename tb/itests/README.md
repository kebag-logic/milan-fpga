# Integration testbenches (legacy, Vivado xsim)

Hand-written SystemVerilog integration TBs from the Zynq era, run under
Vivado **xsim**. They are kept for waveform-level debugging; the live,
tool-free integration regression is `tb/verilator/` (`milan_dp`, `datapath`,
`controller_rate`) — see [`docs/testing/TESTING.md`](../../docs/testing/TESTING.md).

| Directory | DUT | How to run |
|---|---|---|
| `ptp_timestamp/` | `ptp_ts_top` | `cd ptp_timestamp && vivado -mode tcl -source tb_ptp_ts_top.tcl` (written against Vivado 2023.1, part `xc7a35tcpg236-1`) |
| `802_1q_traffic_shaper/` | `traffic_controller_802_1q` | **No `.tcl` runner** — add `tb_traffic_controller_802_1q.sv` to a Vivado project by hand, or prefer `tb/verilator/controller_rate` / `tb/verilator/datapath` |

These TBs use the shared BFM in `tb/common/axi_stream_driver.svh` and the
packet classes in `tb/avtp_packet_gen_sv/`. They are **not** self-checking by
exit code and may lag interface reworks — where they disagree with the
Verilator suites, trust the Verilator suites.
