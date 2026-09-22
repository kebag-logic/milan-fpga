<!-- SPDX-License-Identifier: CERN-OHL-W-2.0 -->
# HDL engineer guide — modifying a module in this tree

You are about to change an FSM, add a counter, widen a record or land a new block. This
page is the shortest path from "I have never opened this repository" to "I can make a
change that will survive review". It states what is true of the tree; the normative
behaviour lives in [`../architecture/`](../architecture/) and is linked from each
section.

**Read the module banner first.** Every file under [`../../hdl/`](../../hdl/) opens with
a `//!`-style header that carries the design rationale — why a store is a RAM and not
flops, which failure mode a guard exists to prevent, which clause a rule implements.
Those banners are the primary source in this project. If a banner and this page
disagree, the banner is right.

---

## 1. The shape of the tree

```
hdl/common/         pp_pkg, the timer service, the PRNG
hdl/packet_engine/  the shared RX and TX datapath, side port, trace ring, NVM port
hdl/adp/            discovery
hdl/acmp/           Milan binding and probing, plus the binding persistence shadow
hdl/aecp/           the micro-coded AEM engine, descriptor store, response buffer
hdl/srp/            the MSRP/MVRP endpoint participant
hdl/maap/           the IEEE 1722-2016 Annex B address-claim engine
hdl/top/            protocol_processor_top and the one recorded RX seam
tb/                 one self-checking Verilator suite per module
```

Do not count modules by hand. The authoritative list — every module and package, its
file, and every suite that elaborates it — is generated:

```sh
python3 scripts/gen_matrix.py          # regenerate docs/traceability/MODULE_MATRIX.md
python3 scripts/gen_matrix.py --check  # fail on drift, or on any module with no suite
```

The untested budget is zero. A new module with no suite fails that check outright.

For how a frame actually moves through these blocks, see
**[`../diagrams/20-rtl-dataflow.svg`](../diagrams/20-rtl-dataflow.svg)** — it is drawn
from the landed wiring in [`protocol_processor_top.sv`](../../hdl/top/protocol_processor_top.sv),
not from the specification.

Directory-to-document mapping and the submodule consumption contract are in
[`../../hdl/README.md`](../../hdl/README.md).

---

## 2. Conventions that bind every file

| Rule | Detail |
|---|---|
| Language | SystemVerilog only. No vendor primitives, no `xpm_*`. Device-flavoured things belong to the consumer's integration layer, outside `hdl/top/`. |
| File frame | SPDX header, then the banner, then `` `default_nettype none ``; the file closes with `` `default_nettype wire ``. |
| Ports | documented inline with `//!`, one line each. |
| Suffixes | `_i` / `_o` ports · `_P` parameters · `_C` localparams and constants · `_r` registered state · `_w` combinational nets. |
| Clock | one clock, `clk_i`, in the `CLK_HZ_P` domain. The only annotated exception is [`KL_pp_side_port`](../../hdl/packet_engine/KL_pp_side_port.sv), which may be driven from a bridged management clock. |
| Reset | `rst_n`, **synchronous**, active low. There are no asynchronous resets in this tree. Mixing an async reset into a synchronous tree is a review stopper. |
| CDC | none is inside these modules. Level inputs that cross a domain (`link_up_i`, `gm_change_i`) are annotated "2FF-synced upstream" — the synchroniser is the integrator's. |
| Citations | a banner names the clause it implements in plain text: `(Milan §5.6.3)`, `(IEEE 1722.1 §9.3.5.3.3)`. |
| Single source | timing values come from [`08_timing.md`](../architecture/08_timing.md) `F08.1` and parameter defaults from [`01_overview.md`](../architecture/01_overview.md) `F01.5`. A localparam cites the `T-…` or `P-…` ID it implements. A copied constant is a defect: it diverges in silence. |

---

## 3. The two rules that shape almost every block

### 3.1 Storage: a 1W1R sync-read RAM, never a flop mirror

Nearly every storage-bearing banner in this tree repeats the same decision, and cites the
same measured failure mode from the reference platform: a flop array read through a wide
combinational mux cost roughly nine hundred extra LUTs. So per-index records, deadline
slots, trace records, pending tables and packed stores are all single-write,
single-read memories with **one cycle of read latency**, and every consumer is built to
absorb that cycle.

The consequence you must respect when editing: **a read never mutates, and data arrives
one cycle after the enable, with no stall path**. Several engines assume exactly that.

The deliberate exceptions are the CAM-shaped structures, where every entry must be
compared in the same cycle — [`KL_pp_scoreboard`](../../hdl/packet_engine/KL_pp_scoreboard.sv),
[`KL_pp_originator`](../../hdl/packet_engine/KL_pp_originator.sv),
[`KL_pp_event_router`](../../hdl/packet_engine/KL_pp_event_router.sv) and the two SRP
stream-FSM arrays. Those are flops on purpose, and their banners say why.

### 3.2 Drops: count them, never swallow them

A frame or event this processor discards is always counted. Counters saturate rather than
wrap, so a maximum reading means "at least this many", never "none". There is no silent
drop anywhere in the RX path after the slot gate, and the dispatch queues do not drop at
all — producers **stall**, which is why the per-queue counters are stall-cycle counters
and not overflow counters.

---

## 4. The shared services, and how an engine talks to them

| Service | Module | Contract you must not break |
|---|---|---|
| Timebase and deadlines | [`KL_pp_timer_service`](../../hdl/common/KL_pp_timer_service.sv) | One arm/cancel port and one expiry bus, shared by every engine. A slot is armed with a deadline and an **owner tag**. |
| Randomness | [`KL_pp_prng`](../../hdl/common/KL_pp_prng.sv) | One LFSR, several draw kinds. It seeds **once**, on the first `link_up_i` rise. The top routes `draw_valid` to the owning client — a broadcast valid would complete the wrong client's draw. |
| Admission | [`KL_pp_scoreboard`](../../hdl/packet_engine/KL_pp_scoreboard.sv) | Nine hazard classes with serialization keys, defined once in [`pp_pkg`](../../hdl/common/pp_pkg.sv). |
| Events | [`KL_pp_event_router`](../../hdl/packet_engine/KL_pp_event_router.sv) | An event is sticky: it holds with its first payload until acknowledged. A re-strobe while unacknowledged coalesces and ticks a lost counter. |
| Self-issued commands | [`KL_pp_originator`](../../hdl/packet_engine/KL_pp_originator.sv) | Sequence assignment, slot held across the exchange, one retry that is an exact duplicate, then failure to the owner. |
| TX slots | [`KL_pp_tx_slots`](../../hdl/packet_engine/KL_pp_tx_slots.sv) | Random-access writes, so a header may legally be written after its payload. There is **no abort arc** — an allocated slot must be committed with a non-zero length. |

### The timer slot map is derived, and it is load-bearing

`pp_timer_map()` in [`pp_pkg`](../../hdl/common/pp_pkg.sv) is the one place the
slot arithmetic exists. Every base is the running sum of the group extents before it, so
the map is correct at any stream shape. Literals are forbidden here for a specific
reason recorded in the top's banner: at one shape the old literals aliased a listener
sink onto the talker base and an SRP talker onto the SRP listener base. The first
**silently loses** a deadline and the second **misdelivers** one, because the ACMP
engines filter expiries by owner tag while ADP and SRP filter by slot. Neither raises an
error or moves a counter; on silicon they read as an intermittent ACMP timeout and a
reservation that leaves at the wrong moment.

The elaboration guards in
[`protocol_processor_top.sv`](../../hdl/top/protocol_processor_top.sv) exist to make an
over-large shape fail **loudly** instead. If you add a timer group, extend the map
function and the guards together — never one without the other.

Allocation order and the slot budget are owned by
[`08_timing.md` §5](../architecture/08_timing.md).

---

## 5. Where the per-engine detail lives

| Engine | Modules | Document | Key figures |
|---|---|---|---|
| Packet engine | [`hdl/packet_engine/`](../../hdl/packet_engine/) | [03](../architecture/03_packet_engine.md) | validate/decode flow, transaction lifecycle, hazard classes, TX path |
| ADP | [`KL_adp_engine`](../../hdl/adp/KL_adp_engine.sv), [`pp_adp_pkg`](../../hdl/adp/pp_adp_pkg.sv) | [04](../architecture/04_adp_engine.md) | [F04.2 advertise SM](../architecture/04_adp_engine.md#fig-04-advsm), [F04.3 talker discovery](../architecture/04_adp_engine.md#fig-04-discsm) |
| ACMP | [`KL_pp_acmp_listener`](../../hdl/acmp/KL_pp_acmp_listener.sv), [`KL_acmp_talker`](../../hdl/acmp/KL_acmp_talker.sv), [`KL_acmp_nvm_shadow`](../../hdl/acmp/KL_acmp_nvm_shadow.sv) | [05](../architecture/05_acmp_engine.md) | [F05.3 the authoritative transition matrix](../architecture/05_acmp_engine.md#fig-05-listener-matrix) |
| AECP | [`hdl/aecp/`](../../hdl/aecp/) | [06](../architecture/06_aecp_engine.md) | [F06.14 command table](../architecture/06_aecp_engine.md#fig-06-cmdtable) |
| SRP | [`hdl/srp/`](../../hdl/srp/) | [10](../architecture/10_srp_engine.md) | [F10.1 internals](../architecture/10_srp_engine.md#fig-10-blocks) |
| MAAP | [`KL_pp_maap`](../../hdl/maap/KL_pp_maap.sv) | [11](../architecture/11_maap_engine.md) | the Table B.7 conflict matrix ([11 §6](../architecture/11_maap_engine.md)) |

### The ACMP listener is a ROM walker, not hand-written arcs

The listener's behaviour **is** the transition ROM. States and events in
[`pp_acmp_pkg`](../../hdl/acmp/pp_acmp_pkg.sv) are encoded so that their codes *are* the
ROM address geometry, and the actions are hardwired primitives sequenced in one fixed
canonical order. That is what lets a profile change behaviour by swapping a ROM image
without touching the datapath. **Changing listener behaviour means changing the ROM
generator and [F05.3](../architecture/05_acmp_engine.md#fig-05-listener-matrix), not the
executor.**

### The AECP path goes through the integrator's main memory

Neither the entity model nor the response buffer is on chip. Both live in the
integrator's memory at compile-time bases. The whole path, including what appears on the
wire when the memory system fails, is
**[`../diagrams/22-aecp-descriptor-fetch.svg`](../diagrams/22-aecp-descriptor-fetch.svg)**.

Two encoding rules travel with that decision and are easy to break:

- **`COPY_BUFFER` advances by bytes copied, not by the lane it read.** A descriptor whose
  length is not a multiple of eight has to stop mid-lane; advancing by the whole lane
  puts the next descriptor's bytes on the wire and lies about `control_data_length`.
- **The response buffer places fields big-endian**, and byte addresses arrive
  non-decreasing from byte 12 upward. The rule lives in
  [`KL_aecp_resp_buf`](../../hdl/aecp/KL_aecp_resp_buf.sv) because the µISA has no
  byte-swap operation.

---

## 6. Running the testbenches

Each suite is a Verilator build with an independent C++ reference model — never a copy of
DUT logic — and a machine-readable tally.

```sh
cd tb/<suite> && make          # one suite; exit 0 = PASS
./scripts/run_suites.sh        # every suite under tb/, summed; exit = number failing
./scripts/lint_hdl.sh          # Verilator --lint-only over every module, zero tolerance
make check                     # the documentation gates (see section 8)
```

`run_suites.sh` globs `tb/*/` rather than keeping a list, and exits 90 if a suite passes
but its tally line cannot be read — a suite whose check count cannot be read is unproven.

Each `tb/<suite>/README.md` states what that suite proves, the seams it deliberately does
not cover, and — for the suites that have been through one — a **mutation record**: a
table of deliberate breakages and how many checks each turned red. That table is the
evidence a suite has teeth. If you add checks, add to it.

### Rule 3: a module is not done until its testbench is

Every RTL commit carries its `tb/<suite>/` update: a SystemVerilog wrap exposing internal
state, an independent reference model, a `sim_main.cpp` with the tally, and a `README.md`
saying what is proven. This is enforced socially by review and mechanically by
`gen_matrix.py --check`.

---

## 7. Testbench conventions worth knowing before you write one

- **Time is compressed.** `TIM_DIV_US_P` and `TIM_DIV_MS_P` override the timer
  prescaler so a millisecond costs a hundred clocks. The timer and PRNG paths under test
  are still the real ones — only the prescaler changes.
- **Expectations are built from the documents**, byte offset by byte offset, in the
  suite's own C++ — not by calling into the DUT.
- **ROM images are generated, not committed.** `ltn_rom.hex` and `ucode.hex` are produced
  by their generators under `hdl/acmp/rom/` and `hdl/aecp/ucode/`, and are ignored by git.
- **Relative ROM paths resolve against the tool's run directory**, which is why
  `TROM_HEX_P` and `UCODE_HEX_P` are parameters at all.

---

## 8. The gates

| Command | Checks |
|---|---|
| `make check` | diagram lint, WaveDrom freshness, documentation links, compliance-matrix consistency, and diagram export staleness |
| `python3 scripts/gen_matrix.py --check` | module ↔ testbench matrix drift, and the zero-untested budget |
| `./scripts/lint_hdl.sh` | Verilator lint over every module, zero warnings tolerated; a waiver is a justified `lint_off` pragma in the RTL with a reason |
| `./scripts/run_suites.sh` | every simulation suite |

The submodule pin in the consuming platform is only ever moved to a commit where all of
these are green here first.

---

## 9. Where the specification and the tree still disagree

These are known. They are recorded here so nobody rediscovers them the hard way. In every
case **the tree is right**.

| Divergence | Detail |
|---|---|
| ADP advertise machine has four states, not three | [F04.2](../architecture/04_adp_engine.md#fig-04-advsm) draws DOWN / DELAY / WAITING. [`pp_adp_pkg`](../../hdl/adp/pp_adp_pkg.sv) splits the delay into its two real hardware phases: `ADP_ADV_DRAW` (the PRNG rejection sampler is running) then `ADP_ADV_DELAY` (the timer is armed). The banner records this as a deliberate refinement of the figure, and the state is externally visible — see the [operator guide](operator.md). |
| There is no shutdown port | [01 §5](../architecture/01_overview.md) describes a `SHUTDOWN` request. In the RTL, deasserting `entity_enable_i` **is** the shutdown: it emits ENTITY_DEPARTING and resets `available_index`. |
| The class-A packet interface is 8-bit | [02 §2](../architecture/02_interfaces.md) specifies a 32-bit word stream with `ready`, `empty` and `err`. The landed top is a byte stream — `rx_valid_i` / `rx_data_i[7:0]` / `rx_last_i` in, with **no RX backpressure at all**, and `tx_valid_o` / `tx_sof_o` / `tx_data_o[7:0]` / `tx_eof_o` / `tx_ready_i` out. The [integrator guide](integrator.md) documents the landed face. |
| No dispatch ROM exists | [06 §4](../architecture/06_aecp_engine.md) specifies a dispatch ROM per opcode and [06 §8](../architecture/06_aecp_engine.md) fixes its entry shape, but no ROM and no generator ship. [`KL_aecp_engine`](../../hdl/aecp/KL_aecp_engine.sv) uses a direct three-arm opcode decode and its banner records that as a documented choice. |
| TX lane 1 is idle | The lane map reserves lane 1 for unsolicited notifications; nothing drives it yet. Lane 0 **is** driven, by the AECP engine. |
| The descriptor image is not on chip | Several places still show it inside the on-chip RAM complex, including the rendered F03.1 and F07.1 figures and the `P-DESCR-IMAGE-BYTES` parameter, which has no consumer in the RTL. The current truth is [07 §3.3](../architecture/07_memory_maps.md) and diagram 22. |

---

## 10. See also

- [Integrator guide](integrator.md) — if your change touches a top-level port, it is an
  interface change before it is an RTL change.
- [Operator guide](operator.md) — if your change adds observable state, it belongs in the
  snapshot window and in that guide's word map.
- [`../README.md`](../README.md) — documentation conventions, figure rules, ID registries.
