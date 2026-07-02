# Legacy 802.1Q traffic-shaper unit tests (Vivado xsim)

These are the original Vivado/xsim testbenches. Some target module interfaces
that changed with the runtime-configurable TSN rework (2026-07), so prefer the
self-checking Verilator harnesses under `tb/verilator/` for CI and regression:

| Legacy TB | Status | Superseded by |
|-----------|--------|---------------|
| `tb_credit_based_shaper.sv` | **removed** — CBS is now runtime-configured (`shaped_i`/`idle_slope_i`/`hi_credit_i`/`lo_credit_i` ports) | [`tb/verilator/cbs`](../../verilator/cbs) |
| `tb_traffic_shaping_core.sv` | stale ports (per-queue CBS config is now packed `cbs_*_i`) | [`tb/verilator/shaper_core`](../../verilator/shaper_core) |
| `tb_traffic_classifier.sv` | stale (classification is now CSR-driven; decode moved to `traffic_class_map`) | [`tb/verilator/cls`](../../verilator/cls) |
| `tb_traffic_queues.sv` | still valid (`traffic_queues` interface unchanged) | — |

The Verilator harnesses need only `verilator >= 5.0` + a C++17 compiler (no
Xilinx tools) and each exits non-zero on failure. See
[`tb/verilator/README.md`](../../verilator/README.md).
