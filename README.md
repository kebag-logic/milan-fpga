# milan-fpga — IEEE 1722 / 1722.1 / Milan v1.2 on FPGA

> A fully-FPGA **Milan v1.2 AVB/TSN audio end-station**: a RISC-V/LiteX softcore SoC
> running Linux, with the entire TSN datapath in **vendor-neutral SystemVerilog fabric**, on
> an Alinx AX7101 (Artix-7). Evolving toward a 4-port AVB switch.

```sh
git clone https://github.com/kebag-logic/milan-fpga && cd milan-fpga
git submodule update --init third_party/verilog-axis   # REQUIRED — not optional
cd tb/verilator/tcam && make                           # ~5 s → RESULT: PASS
```

**Never seen this repo before?** → **[QUICKSTART.md](QUICKSTART.md)** — clone to a green
test run in 30 minutes, no FPGA and no bench access assumed. Want to know what this *is*
before installing anything? → **[docs/overview/AT_A_GLANCE.md](docs/overview/AT_A_GLANCE.md)**
(one page: block diagram, the standards, the register map, what's proven).

![System domain map — every module by layer](docs/SYSTEM_DOMAIN_MAP.png)

## Who are you?

Four doors, three links each. Every other doc hangs off one of these.

| | You are… | Start | Then | Then |
|---|---|---|---|---|
| 🔌 | **Integrator** — putting this datapath in *your* SoC or on *your* board | [integration/INTEGRATION_GUIDE.md](docs/integration/INTEGRATION_GUIDE.md) — the `milan_datapath` boundary as a port-by-port contract | [reference/REGISTER_MAP.md](docs/reference/REGISTER_MAP.md) — the AXI4-Lite ABI your driver programs | [integration/PORTING_GUIDE.md](docs/integration/PORTING_GUIDE.md) — off-Xilinx, off-Vivado, per-vendor translation |
| 🛠 | **RTL developer** — changing or adding fabric | [overview/ARCHITECTURE.md](docs/overview/ARCHITECTURE.md) §8 "where to change things" | [fpga/FPGA_DESIGN.md](docs/fpga/FPGA_DESIGN.md) — every module in `hdl/` and the harness that verifies it | [CONTRIBUTING.md](CONTRIBUTING.md) — house style; a DUT change ships its testbench in the same commit |
| 🔧 | **Bench operator** — building, flashing, bringing a board up | [integration/BUILDING.md](docs/integration/BUILDING.md) — `build.sh` configs and the gates a build must pass | [integration/QSPI_FLASHBOOT.md](docs/integration/QSPI_FLASHBOOT.md) — flash a **matched** image set, boot Linux | [limitations/TROUBLESHOOTING.md](docs/limitations/TROUBLESHOOTING.md) — symptom → cause → fix, from the field |
| 📖 | **Curious reader / evaluator** — deciding if this is worth your time | [overview/AT_A_GLANCE.md](docs/overview/AT_A_GLANCE.md) — the whole thing on one page | [SPEC_TRACEABILITY.md](docs/SPEC_TRACEABILITY.md) — clause-level verification status, 204 rows | [limitations/KNOWN_ISSUES_AND_LIMITATIONS.md](docs/limitations/KNOWN_ISSUES_AND_LIMITATIONS.md) — what does not work |

More lanes (system engineer, tester, hobbyist) and the full index:
**[docs/README.md](docs/README.md)**. Everyone's long-form orientation is the
**[Systems-Engineer Guide](docs/SYSTEMS_ENGINEER_GUIDE.md)**. Terms →
[glossary](docs/GLOSSARY.md).

![Documentation map — the four reading lanes by role](docs/DOC_MAP.png)

## What's proven on silicon

| Area | State |
|---|---|
| Milan v1.2 end-station (talker + listener) | internal conformance suite **green on both boards** |
| TSN datapath in fabric | MAC · 802.1Qav CBS · gPTP · AVTP/AAF/CRF · ADP/AECP/ACMP · MAAP · lwSRP |
| Media-clock servo | MMCM-DRP, analog loop **−83.9 dB** (converter floor) |
| Networking / boot | ring-DMA line-rate ingest · QSPI flash-boot (zero-upload) |
| Audio | ALSA record over Milan · live talker↔listener E2E |
| CPU / board | 1-hart VexiiRiscv RV64 Linux SoC · xc7a100t · DDR3 512 MB |
| Portability | no Xilinx primitives — machine-checked by the [Yosys/ECP5 flow](syn/yosys/README.md) |

> Those rows are **measurements on specific boards on specific dates**, not promises about
> your hardware. Live perf numbers live in the measured ledger — [CHANGELOG.md](CHANGELOG.md) +
> [docs/findings/](docs/findings/README.md). Any number quoted elsewhere is a dated snapshot.

## Prerequisites — by what you actually want to do

Everything is open-source **except the final Xilinx bitstream**. Package names are Arch; the
equivalents exist on any distro. Each tier *adds* to the one above it.

**Tier 1 · simulate + run every testbench** — no FPGA, no vendor tools, ~2 min to install:

```sh
sudo pacman -S --needed gcc make python python-yaml verilator git
git submodule update --init third_party/verilog-axis     # anonymous HTTPS
```

Verilator must be **≥ 5.050** — that is the CI pin, and CI builds it from source
at that tag rather than trusting a distro package, because 5.020 (Ubuntu 24.04)
cannot build four of the suites and 5.032 (Debian trixie) reads back zeros on six
`aecp` checks. The measured table is in
[docs/testing/TESTING.md](docs/testing/TESTING.md) §7. The repo's *other* submodule, `external`, is SSH-only and is
**not needed** for anything here — leave it uninitialised. A GitHub *"Download ZIP"* has no
submodule content, so the datapath testbenches will not build from a zip.

**Tier 2 · prove device portability (generic synthesis + Lattice ECP5)** — add:

| Tool | Install | Note |
|---|---|---|
| `yosys` | `pacman -S yosys` | in the Arch official repos |
| `sv2v` | **not in the Arch repos (AUR only)** — take the upstream prebuilt static Linux binary from [github.com/zachjs/sv2v/releases](https://github.com/zachjs/sv2v/releases) and drop it in `~/.local/bin` | yosys cannot read SystemVerilog interfaces without it |

**Tier 3 · build a bitstream / run on hardware** — add:

| Tool | Install (Arch) | Needed for | Required? |
|---|---|---|---|
| `riscv64-elf-gcc` + binutils + newlib | `pacman -S riscv64-elf-gcc riscv64-elf-binutils riscv64-elf-newlib` | BIOS + firmware | ✅ to build gateware |
| `jdk17` + `sbt` | `pacman -S jdk17-openjdk sbt` | generate the VexiiRiscv/NaxRiscv core (SpinalHDL, in Scala) | ✅ to build gateware |
| `meson ninja cmake dtc` | `pacman -S meson ninja cmake dtc` | build tooling + device tree | ✅ to build gateware |
| Python 3 + the **LiteX venv** | `litex_setup.py` — see [QUICKSTART.md](QUICKSTART.md) §6 | SoC elaboration (LiteX/Migen, installed from git) | ✅ to build gateware |
| **Vivado 2026.1** with Artix-7 | Xilinx installer | place & route → `.bit` | ⬦ **proprietary**; only to build a bitstream |
| `openFPGALoader` | `pacman -S openfpgaloader` | flash the board over JTAG | ⬦ only to flash hardware |

Prefer not to install anything? [`Containerfile.dev`](Containerfile.dev) pins tiers 1 and 2
exactly: `podman build -t milan-fpga-dev -f Containerfile.dev . && podman run --rm -v "$PWD":/work:z milan-fpga-dev`.

## Quickstart — copy/paste

```sh
# 1 · clone + the one required submodule
git clone https://github.com/kebag-logic/milan-fpga && cd milan-fpga
git submodule update --init third_party/verilog-axis

# 2 · tier-1 toolchain, once (Arch shown — see Prerequisites for your distro)
sudo pacman -S --needed gcc make python python-yaml verilator git

# 3 · run a self-checking testbench — no vendor tools, exit 0 = PASS
cd tb/verilator/milan_dp && make

# 4 · run the three repo gates — pure Python, seconds
python3 scripts/docs_check.py
python3 docs/traceability/gen_module_matrix.py --check
python3 sw/builder/test_builder.py

# 5 · build a real bitstream — needs the tier-3 toolchain + Vivado
python3 -m venv ~/litex-milan/venv && . ~/litex-milan/venv/bin/activate
curl -sSL https://raw.githubusercontent.com/enjoy-digital/litex/master/litex_setup.py \
     | python - --init --install --config=full
export JAVA_HOME=/usr/lib/jvm/java-17-openjdk
cd sw/litex && ./build.sh ax7101
```

> ⚠️ Run builds from **any directory except** the litex-repos parent, or `import litex` resolves
> to the repo root (a namespace package) and `get_data_mod` fails.

The long form, with what is verified vs what needs a bench: [QUICKSTART.md](QUICKSTART.md).

## Run the tests

| Suite | Command | Needs |
|---|---|---|
| **All Verilator TBs** (one dir per suite, self-checking) | `cd tb/verilator && for d in */; do (cd "$d" && make) \|\| break; done` | verilator ≥ 5.050 (the CI pin) |
| One TB | `cd tb/verilator/<suite> && make` (exit 0 = PASS) | verilator |
| Docs gate (links, wording, dead references) | `python3 scripts/docs_check.py` | python3 — **git optional** |
| Traceability no-drift gate | `python3 docs/traceability/gen_module_matrix.py --check` | python3 |
| End-station builder gates | `python3 sw/builder/test_builder.py` | python3 + pyyaml |
| Device portability | `cd syn/yosys && make && make ecp5` | yosys + sv2v |
| **BDD conformance suite** (21 features / 113 scenarios, offline, ~3 s) | `cd tests && behave -f plain` | `behave` (any venv; the `@tsn_gen` tier also wants `TSAGEN_DIR`) |

`ls tb/verilator/` is the authoritative suite list. Full map: [docs/testing/TESTING.md](docs/testing/TESTING.md).

## Build & flash a board

`./build.sh ax7101` (or `arty`) → `./deploy.sh flash` + `flash-images`. The full flow, with the
load-bearing rules (compressed bitstream, matched image set, recovery) in one picture:

![Build → Flash → Boot → Verify pipeline](docs/BUILD_FLASH_BOOT.png)

Details: [docs/integration/BUILDING.md](docs/integration/BUILDING.md) ·
[docs/integration/QSPI_FLASHBOOT.md](docs/integration/QSPI_FLASHBOOT.md) ·
[docs/findings/BENCH_TOPOLOGY.md](docs/findings/BENCH_TOPOLOGY.md).

## Credits

**Developers:** [Cemal Dogan](https://github.com/cemaldogann) · [Oguz Kahraman](https://github.com/OguzKahramn)
**Maintainer:** [Alexandre Malki](https://github.com/Mister-M-alt)

Licence: CERN-OHL-W-2.0 ([LICENSE](LICENSE)) · vendored third-party code and pins:
[THIRD_PARTY.md](THIRD_PARTY.md).
