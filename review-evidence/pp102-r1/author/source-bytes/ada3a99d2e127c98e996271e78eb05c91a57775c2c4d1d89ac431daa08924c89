<!-- SPDX-License-Identifier: CERN-OHL-W-2.0 -->
# HDL — the implementation of this architecture

This directory is the **home of the RTL**. The architecture under
[`../docs/`](../docs/README.md) is HDL-agnostic; *this* implementation is
**SystemVerilog**, written to be consumed by the reference integration platform
([milan-fpga](https://github.com/kebag-logic/milan-fpga), Artix-7 xc7a100t) which
includes this repository as a **git submodule** and instantiates the processor from
here. The HDL is authored here and only *consumed* there — never copied.

## Layout (mirrors the architecture documents)

| Path | Implements | Architecture doc |
|---|---|---|
| `hdl/packet_engine/` | shared RX classify/parse + TX arbiter/builder | [`03_packet_engine.md`](../docs/architecture/03_packet_engine.md) |
| `hdl/adp/` | ADP discovery engine | [`04_adp_engine.md`](../docs/architecture/04_adp_engine.md) |
| `hdl/acmp/` | Milan ACMP binding/probing engine | [`05_acmp_engine.md`](../docs/architecture/05_acmp_engine.md) |
| `hdl/aecp/` | AECP/AEM micro-coded engine + controller registry | [`06_aecp_engine.md`](../docs/architecture/06_aecp_engine.md) |
| `hdl/srp/` | MSRP/MVRP endpoint participant: Domain + VLAN FSMs, per-stream FSMs, vector codec | [`10_srp_engine.md`](../docs/architecture/10_srp_engine.md) |
| `hdl/common/` | shared across engines: the timer service, the PRNG, and `pp_pkg` — the cross-cutting types, hazard classes and derived timer-slot map | [`02_interfaces.md`](../docs/architecture/02_interfaces.md), [`08_timing.md`](../docs/architecture/08_timing.md) |
| `hdl/top/` | `protocol_processor_top` — the one instantiation boundary — and `KL_mrp_strip`, the recorded RX seam | [`01_overview.md`](../docs/architecture/01_overview.md) |
| `../tb/` | one self-checking Verilator suite per module (exit 0 = PASS) | [`09_verification.md`](../docs/architecture/09_verification.md) |

Directories appear as their first module lands; none are created empty. There is **no CDC
primitive and no memory primitive** in this tree: every clock crossing is the integrator's
(see the [integrator guide](../docs/guides/integrator.md)), and memories are inferred, not
instantiated.

The generated module ↔ testbench matrix is
[`docs/traceability/MODULE_MATRIX.md`](../docs/traceability/MODULE_MATRIX.md); regenerate
it with `python3 scripts/gen_matrix.py`.

## Which guide you want

| | |
|---|---|
| Changing a module | [HDL engineer guide](../docs/guides/hdl-engineer.md) |
| Instantiating the top | [Integrator guide](../docs/guides/integrator.md) |
| Debugging a live board | [Operator guide](../docs/guides/operator.md) |

## Rules of this directory

1. **SystemVerilog only**, vendor-neutral: no Xilinx/Lattice primitives, no
   `xpm_*`. Anything device-flavored belongs to the consumer repository's
   integration layer, behind `hdl/top/`.
2. **Tool floor**: Verilator ≥ 5.050 and Yosys (via sv2v) must both elaborate
   every module. Portability is a gate, not an aspiration.
3. **A module is not done until its testbench is** — every RTL commit carries its
   `tb/<suite>/` update: an SV wrap exposing internal state, an *independent*
   reference model (never a copy of DUT logic), a `sim_main.cpp` with a
   machine-readable tally, and a `README.md` stating what the suite proves.
4. **Single-source values**: timing constants come from
   [`08_timing.md`](../docs/architecture/08_timing.md) `F08.1` and parameter
   defaults from [`01_overview.md`](../docs/architecture/01_overview.md) `F01.5`.
   RTL localparams cite the `T-…`/parameter ID they implement; a derived copy of
   a value that exists elsewhere is a defect.
5. **Spec citations in headers**: every module banner names the clause(s) it
   implements — `(Milan §…)`, `(IEEE 1722.1 §…)` — in the same plain-text form
   the documents use.

## Consumption contract (submodule)

The consumer pins this repository at a commit; the pin is only ever moved to a
commit whose `make check` and full `tb/` sweep are green here first. Interface
stability at `hdl/top/` follows [`02_interfaces.md`](../docs/architecture/02_interfaces.md):
a breaking port change is a documented interface change *before* it is an RTL
change.
