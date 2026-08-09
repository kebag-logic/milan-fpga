# QUICKSTART — clone → green test run in 30 minutes

You do **not** need an FPGA, a Xilinx licence, or access to anyone's lab bench to
get a meaningful, self-checking result out of this repo. This page is the shortest
honest path from `git clone` to something green on your own machine.

```sh
git clone https://github.com/kebag-logic/milan-fpga && cd milan-fpga
git submodule update --init third_party/verilog-axis     # NOT optional — see §0
```

> **§0 — the one thing people get wrong.** [`third_party/verilog-axis`](third_party/verilog-axis) is a git
> submodule (anonymous HTTPS, no account needed). Several testbenches and most of
> the datapath will **not build without it**, and a GitHub *"Download ZIP"* does
> not contain it.
>
> Already took a zip or a tarball? You do not have to start over — just drop the
> dependency in by hand (verified to work: `milan_dp` builds and passes 98 checks
> afterwards):
>
> ```sh
> git clone https://github.com/alexforencich/verilog-axis third_party/verilog-axis
> ```
>
> The exact revision this repo pins is recorded in its git tree
> (`git ls-tree HEAD third_party/verilog-axis`); `git checkout <that sha>` inside
> [`third_party/verilog-axis`](third_party/verilog-axis) if you want to match it exactly.
>
> The repo's *other* submodule, `external`, is **SSH-only and not needed** for
> anything on this page — leave it uninitialised.

---

## Contents

- **[1. Pick a track](#1-pick-a-track)** — Four rows: what each track gets you, what it costs to install, and which ones need something proprietary. Tracks 1 and 2 are the verified content on this page; 3 and 4 are maps, not recipes.
- **[2. Track 1 — simulate (no FPGA, no vendor tools)](#2-track-1--simulate-no-fpga-no-vendor-tools)** — The whole no-hardware path: seven packages measured against a bare container, the three pure-Python gates, and a cold-build table from `tcam` (~5 s) to `milan_dp` (~85 s). Read the Verilator floor first — 5.020 cannot build the datapath harnesses at all and 5.032 fails six `aecp` checks.
- **[3. Track 2 — device portability, still no vendor tools](#3-track-2--device-portability-still-no-vendor-tools)** — Two `make` targets in [`syn/yosys`](syn/yosys) that end in `tops: 47 pass: 47 fail: 0` — the machine proof that no Xilinx primitive survives, plus a real ECP5 mapping. Includes the `sv2v` install, which is the step people get stuck on.
- **[4. What works with no board at all](#4-what-works-with-no-board-at-all)** — A capability table for readers who will never buy an FPGA. Everything upstream of place & route is open; place & route on Artix-7 is the one genuinely closed step.
- **[5. One command: the container](#5-one-command-the-container)** — `Containerfile.dev` pinned to the measured package set. The repo is bind-mounted rather than copied, so your edits are what the four gates actually test.
- **[6. Track 3 — build a bitstream (Vivado)](#6-track-3--build-a-bitstream-vivado)** — Not re-verified while writing the page. The four extra prerequisites and why each is there — the RISC-V core is *generated* from Scala at build time — and the `import litex` namespace-package trap that catches everybody once.
- **[7. Track 4 — run it on hardware](#7-track-4--run-it-on-hardware)** — Bench-only, and explicitly an engineering record rather than a reproducible recipe. Gives the ordering (a gateware-only flash will not boot) and five hand-offs, including the lethal gateware⇄driver pairings to check *before* flashing.
- **[8. Where to go next](#8-where-to-go-next)** — Routing table from who you are — evaluating, integrating, about to write RTL, lost in the vocabulary — to the one page to open next.

## 1. Pick a track

| Track | What you get | Toolchain | Proprietary? |
|---|---|---|---|
| **1 · Simulate** | every self-checking Verilator testbench, the three repo gates, the end-station builder | `gcc make python python-yaml verilator git` | ❌ none |
| **2 · Portability** | machine-proof that the RTL maps to a non-Xilinx device (generic + Lattice ECP5) | + `yosys` + an `sv2v` binary | ❌ none |
| **3 · Bitstream** | a `.bit` for an Artix-7 board | + LiteX/migen, a JVM, a RISC-V toolchain, **Vivado** | ✅ Vivado |
| **4 · Hardware** | a booting Linux SoC that talks Milan on the wire | + a board, a flasher, an AVB-capable switch | ✅ Vivado + hardware |

Tracks 1 and 2 are the whole of this page's *verified* content. Tracks 3 and 4 are
summarised and then handed off to the deep docs — they were **not** re-run while
writing this page and are labelled accordingly.

---

## 2. Track 1 — simulate (no FPGA, no vendor tools)

### 2.1 Install

Measured against a bare `archlinux:latest` container, which ships **only bash** —
no compiler, no python, no git. This is the complete list, nothing implied:

```sh
sudo pacman -S --needed gcc make python python-yaml verilator yosys git which
```

Verified working versions: verilator 5.050, yosys 0.66, python 3.14.6, gcc 16.1.1.

> **Verilator version matters.** Measured: **5.020** (Ubuntu 24.04) *cannot build*
> the datapath harnesses at all, and **5.032** (Debian trixie / Ubuntu 25.04) builds
> but fails 6 `aecp` checks. **Use 5.050 or newer.** If your distro ships an older
> one, build it from source — that is exactly what CI does, pinned. The small
> self-contained suites (`tcam`, `cbs`, `csr`) work on older versions; it is the
> datapath harnesses that do not. Details and the measured table:
> [docs/testing/TESTING.md](docs/testing/TESTING.md) §7.
Verilator **≥ 5.050** is the real requirement (that is the CI pin; see the note above).

On other distributions install the same seven things — the package *names* differ
and are deliberately not guessed here. If you would rather not think about it at
all, [`Containerfile.dev`](Containerfile.dev) is the exact, reproducible recipe
(see [§5](#5-one-command-the-container)).

### 2.2 The three repo gates — pure Python, seconds

These are the same gates CI runs. None of them needs a compiler, a simulator, or
a board:

```sh
python3 scripts/docs_check.py                        # link/wording/dead-ref gate
python3 docs/traceability/gen_module_matrix.py --check # spec↔module↔test no-drift
python3 sw/builder/test_builder.py                   # end-station builder, 17 gates
```

Green looks like:

```
docs_check: 0 finding(s) across <N> md files [git ls-files]
traceability matrix up to date (<N> modules, 1 untested)
ALL GATES PASS
```

`docs_check.py` works **with or without git** — inside a git working tree it uses
`git ls-files`, in an extracted tarball it falls back to a `.gitignore`-aware
filesystem walk and prints which one it used. `test_builder.py` needs only Python
and PyYAML; it writes its emissions under `sw/builder/out/` (gitignored).

There is a fourth CI gate that is *not* pure Python — the RTL lint — because it
needs the Verilator you install in §2.3:

```sh
python3 scripts/lint_rtl.py --check   # every module in hdl/, ~10 s, exit 0 = PASS
```

It fails on a **new** Verilator `--lint-only` violation; the existing 150 are
grandfathered by a per-directory ratchet in
[`scripts/lint.budget`](scripts/lint.budget) and printed in full on every run.
Details and the Verible comparison: [`docs/testing/TESTING.md`](docs/testing/TESTING.md) §4b.

### 2.3 The Verilator testbenches

One directory per suite under [`tb/verilator/`](tb/verilator); each is self-checking and exits
non-zero on failure. **`ls tb/verilator/` is the authoritative suite list** — any
count written in prose goes stale.

```sh
cd tb/verilator/tcam && make      # smallest suite: 19 checks, ~5 s from cold
```

Green looks like:

```
== tcam (ternary MAC CAM) harness ==
checks: 19   failures: 0
RESULT: PASS
```

Measured here, cold build on a desktop x86-64:

| Suite | What it proves | Cold build+run |
|---|---|---|
| `tcam` | ternary CAM dest-MAC database | ~5 s |
| `cbs` | 802.1Qav credit maths, 87 233 cycle checks vs a reference model | ~5 s |
| `csr` | the AXI4-Lite register ABI — the executable form of [the register map](docs/reference/REGISTER_MAP.md); three executables | ~18 s |
| `milan_dp` | whole-datapath integration: CPU reads `ID="MILN"`, frame in → frame out byte-exact (98 checks) | ~85 s |

Run everything (never hand-list suites — the glob is the contract):

```sh
cd tb/verilator && for d in */ ; do ( cd "$d" && make clean >/dev/null && make ) || exit 1; done
```

Suite-by-suite detail: [`tb/verilator/README.md`](tb/verilator/README.md).
The test taxonomy across all layers: [`docs/testing/TESTING.md`](docs/testing/TESTING.md).

### 2.4 If a testbench cannot find a module

This exact shape means §0 — the submodule is not checked out (verified by
deleting it and re-running [`tb/verilator/milan_dp`](tb/verilator/milan_dp)):

```
%Error: Cannot find file containing module: '../../../third_party/verilog-axis/rtl/axis_fifo.v'
%Error: Cannot find file containing module: '../../../third_party/verilog-axis/rtl/axis_demux.v'
```

Fix: `git submodule update --init third_party/verilog-axis`, then `make clean`
in the suite before rebuilding.

---

## 3. Track 2 — device portability, still no vendor tools

This is the machine-checked proof that the RTL contains **no Xilinx primitives**:
`yosys` synthesises every top to a generic cell library, and `hierarchy -check`
fails if any undefined/vendor cell survives. `make ecp5` then maps to a real
non-Xilinx device (Lattice ECP5).

```sh
cd syn/yosys && make            # generic synth of every top
cd syn/yosys && make ecp5       # map to Lattice ECP5 (TRELLIS_FF/LUT4)
```

Both were run here (yosys 0.66 + sv2v v0.0.13), and both end in:

```
tops: 47   pass: 47   fail: 0
RESULT: PASS
```

`make` took ~8 min, `make ecp5` ~11 min on a desktop x86-64 — `milan_datapath`,
the full integration wrapper, is most of it. Each run then prints two extra,
non-fatal reports: a tied-off-input inventory for `milan_datapath` (which
`WARNING` lines flag inputs constant at every wiring site) and an observer-purity
structural check (`TAP-PURITY RESULT: PASS` — it self-tests against a
deliberately broken fixture first).

**You need `sv2v` on `PATH`** — yosys's Verilog frontend cannot read SystemVerilog
interfaces and packages. On Arch `sv2v` is **AUR-only, not in the official
repositories**, so the least painful route on any distribution is the upstream
prebuilt static Linux binary:

```sh
mkdir -p ~/.local/bin
curl -fsSL -o /tmp/sv2v.zip \
  https://github.com/zachjs/sv2v/releases/download/v0.0.13/sv2v-Linux.zip
unzip -q /tmp/sv2v.zip -d /tmp && install -m0755 /tmp/sv2v-Linux/sv2v ~/.local/bin/sv2v
sv2v --version                  # -> sv2v v0.0.13   (needs ~/.local/bin on PATH)
```

(Releases: [github.com/zachjs/sv2v/releases](https://github.com/zachjs/sv2v/releases).)

Details, the authoritative `tops` list and what is deliberately *not* covered:
[`syn/yosys/README.md`](syn/yosys/README.md).

---

## 4. What works with **no board at all**

If you never buy an FPGA, this is still a usable repo. Nothing in this column
needs a vendor licence:

| You can | How | Needs |
|---|---|---|
| Run every self-checking RTL testbench | [§2.3](#23-the-verilator-testbenches) | verilator, gcc |
| Prove the RTL is vendor-neutral, and map it to an ECP5 | [§3](#3-track-2--device-portability-still-no-vendor-tools) | yosys, sv2v |
| Generate a whole end-station (AEM descriptors, SV headers, build plan) from a YAML declaration | `python3 sw/builder/endstation_builder.py configs/endstation_arty_4x4.yaml` · [`docs/ENDSTATION_BUILDER.md`](docs/ENDSTATION_BUILDER.md) | python, pyyaml |
| Read the register ABI and write driver code against it | [`docs/reference/REGISTER_MAP.md`](docs/reference/REGISTER_MAP.md), asserted by the `csr` suite | nothing |
| Check the spec↔module↔test coverage of every clause | [`docs/SPEC_TRACEABILITY.md`](docs/SPEC_TRACEABILITY.md), [`docs/traceability/MODULE_MATRIX.md`](docs/traceability/MODULE_MATRIX.md) | nothing |
| Simulate the softcore booting with the NIC attached (sim DUT) | [`sw/litex/milan_sim.py`](sw/litex/milan_sim.py) — **needs the LiteX stack + a JVM**, see [§6](#6-track-3--build-a-bitstream-vivado) | migen/litex, JDK |

What you **cannot** do without proprietary tools: place & route (`.bit`
generation) is Vivado-only. There is no open bitstream flow for Artix-7 in this
repo. Everything upstream of place & route is open.

---

## 5. One command: the container

[`Containerfile.dev`](Containerfile.dev) pins exactly the working set above —
Arch base, the measured package set, plus a pinned `sv2v` binary:

```sh
podman build -t milan-fpga-dev -f Containerfile.dev .
podman run --rm -v "$PWD":/work:z milan-fpga-dev            # runs the four gates
podman run --rm -it -v "$PWD":/work:z milan-fpga-dev bash   # interactive
```

The repo is bind-mounted, not copied, so your edits are what gets tested. The
default command initialises the submodule if it is missing, then runs the docs
gate, the traceability gate, the builder gate and one Verilator suite. Docker
works too — drop the `:z` if your setup has no SELinux.

There is a second, unrelated image in the tree,
[`Containerfile.dut-sim`](Containerfile.dut-sim), for the AECP DUT-simulation
server; it is not part of this on-ramp.

---

## 6. Track 3 — build a bitstream (Vivado)

> ⚠️ **Not re-verified while writing this page** — it needs a Vivado install and
> ~1 h of place & route. Treat the commands as a map, and
> [`docs/integration/BUILDING.md`](docs/integration/BUILDING.md) as the truth.

On top of track 1 you additionally need:

- **LiteX + migen**, installed from git into a virtualenv (not on PyPI in the
  version this repo pins),
- a **JVM (JDK 17)** and `sbt` — the VexiiRiscv/NaxRiscv cores are *generated* by
  SpinalHDL, in Scala, at build time,
- a **RISC-V bare-metal toolchain** (`riscv64-elf-gcc` + binutils + newlib) for
  the LiteX BIOS,
- **Vivado 2026.1** with Artix-7 device support — proprietary, and the only
  closed-source step in the whole flow.

```sh
python3 -m venv ~/litex-milan/venv && . ~/litex-milan/venv/bin/activate
curl -sSL https://raw.githubusercontent.com/enjoy-digital/litex/master/litex_setup.py \
     | python - --init --install --config=full
export JAVA_HOME=/usr/lib/jvm/java-17-openjdk
cd sw/litex && ./build.sh ax7101          # or: ./build.sh arty
```

> Run builds from **any directory except** the litex-repos parent, or
> `import litex` resolves to the repo root (a namespace package) and
> `get_data_mod` fails. This one bites everybody once.

Read before you build: [`docs/integration/BUILDING.md`](docs/integration/BUILDING.md)
(named configs, the parallel-launch discipline, the timing/utilisation gates) and
[`docs/litex/LITEX_SOC.md`](docs/litex/LITEX_SOC.md) §4 (the mandatory non-obvious
flags and *why* each is mandatory).

Porting to a board that is not an AX7101 or an Arty:
[`docs/integration/PORTING_GUIDE.md`](docs/integration/PORTING_GUIDE.md), with
[`docs/integration/BOARD_PORTING_AX7101.md`](docs/integration/BOARD_PORTING_AX7101.md)
as the worked example.

---

## 7. Track 4 — run it on hardware

> ⚠️ **Bench-only.** Nothing in this section was run while writing this page, and
> some of it cannot be reproduced without an AVB-capable switch and a second
> talker/listener. The linked docs record what was measured, on which board, on
> which date — read them as an engineering record, not as a recipe that will
> reproduce identically on your desk.

The order is: build (§6) → flash a **matched image set** (a gateware-only load
will not boot) → boot Linux → bring the network up → connect a stream.

1. [`docs/integration/QSPI_FLASHBOOT.md`](docs/integration/QSPI_FLASHBOOT.md) —
   flash layout, `deploy.sh flash-images`, why the set must match.
2. [`docs/limitations/TROUBLESHOOTING.md`](docs/limitations/TROUBLESHOOTING.md) —
   the field log: symptom → cause → fix, for boot, flash, link and stream faults.
3. [`docs/limitations/KNOWN_ISSUES_AND_LIMITATIONS.md`](docs/limitations/KNOWN_ISSUES_AND_LIMITATIONS.md)
   — read the **lethal gateware⇄driver pairings** table *before* flashing anything.
4. [`docs/findings/BENCH_TOPOLOGY.md`](docs/findings/BENCH_TOPOLOGY.md) — how the
   reference lab is wired, which board runs which image. Host names, outlet
   numbers and addresses in there are specific to that lab; the *topology* is the
   part you can copy.
5. [`docs/integration/PIPEWIRE_AVB_PEER.md`](docs/integration/PIPEWIRE_AVB_PEER.md)
   — the cheapest second endpoint: a Linux box running PipeWire as the AVB peer,
   instead of a second FPGA.

You will also need an **802.1AS-capable switch** for anything involving two
endpoints. gPTP is not optional in Milan — without a working time domain there is
no media clock and no stream.

---

## 8. Where to go next

| You are | Read |
|---|---|
| deciding whether to use this at all | [`docs/overview/AT_A_GLANCE.md`](docs/overview/AT_A_GLANCE.md) — the one-page picture |
| integrating the datapath into your own SoC | [`docs/integration/INTEGRATION_GUIDE.md`](docs/integration/INTEGRATION_GUIDE.md) → [`docs/reference/REGISTER_MAP.md`](docs/reference/REGISTER_MAP.md) |
| going to write RTL | [`docs/overview/ARCHITECTURE.md`](docs/overview/ARCHITECTURE.md) §8 → [`docs/fpga/FPGA_DESIGN.md`](docs/fpga/FPGA_DESIGN.md) → [`CONTRIBUTING.md`](CONTRIBUTING.md) |
| lost in the vocabulary | [`docs/GLOSSARY.md`](docs/GLOSSARY.md) |
| looking for the full doc index | [`docs/README.md`](docs/README.md) |
