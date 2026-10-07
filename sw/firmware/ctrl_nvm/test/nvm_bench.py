# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""nvm_bench.py - build and run the saved-state store's GoogleTest suite for one shape.

One `Bench` per shipped shape: the builder's shape and identity, the Python
encoder's frames for that shape (scripts/nvm_klj2.py, the reference) and the
shape's system clock as LiteX's generated/soc.h carries it. nvm_fixture.py
writes the suite's oracle from it. `build_suite` compiles the store against
the generated constants header (the SAME derivation sw/litex/milan_soc.py
publishes for the shipping writer) into a GoogleTest binary, and `run_suite`
runs it over a fixture.
"""

from __future__ import annotations

import json
import os
import re
import sys
from collections.abc import Sequence
from dataclasses import dataclass, replace
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
TREE = HERE.parent
ROOT = HERE.parents[3]
HARNESS = ROOT / "sw/firmware/gtest"
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "sw/litex"))
sys.path.insert(0, str(HARNESS))

import fw_gtest                                                         # noqa: E402

from nvm_contract import REC_HDR, Donor, Ident, Shape                  # noqa: E402
from nvm_klj2 import (erased_record, frame_record, klj2_assemble,      # noqa: E402
                      klj2_decode, payload_bytes)
from nvm_shape import (binding_base, build, firmware_constants,        # noqa: E402
                       inventory, layout_version)
from check_nvm_record_space import expected_payloads                   # noqa: E402
from flash_map import literal                                          # noqa: E402

#: The store as it ships and its two flash ports: the firmware, measured.
STORE_SOURCES = ("nvm_klj2.c", "nvm_store.c", "plat/nvm_flash_litespi.c")
#: The host models behind the ports: test equipment, never measured.
MODEL_SOURCES = ("host/nvm_fmodel.c", "host/nvm_smodel.c", "host/litespi_model.c")


@dataclass(frozen=True)
class Binary:
    """One GoogleTest binary of a shape: its tests, the firmware and models it
    links, and the shape-header constants it is built with instead of the
    builder's (`edit`: a doctored build no shipped shape is)."""

    name: str
    tests: tuple[str, ...]
    store: tuple[str, ...] = ("nvm_klj2.c", "nvm_store.c", "plat/nvm_flash_litespi.c")
    models: tuple[str, ...] = ("host/nvm_fmodel.c", "host/nvm_smodel.c", "host/litespi_model.c")
    edit: tuple[tuple[str, int], ...] = ()
    cflags: tuple[str, ...] = ()
    defines: tuple[str, ...] = ()
    vector: bool = False
    address_sanitizer: bool = False


RIG = ("nvm_rig.cpp", "nvm_suite.cpp")
#: Every shape: the boot and write paths, the codec and the extra store paths.
SUITE = Binary("suite", (*RIG, "test_nvm_boot.cpp", "test_nvm_write.cpp", "test_nvm_codec.cpp", "test_nvm_more.cpp",
                         "test_nvm_flashmock.cpp"))
#: The shapes tb/verilator/nvm_backend records a vector of, under its identity.
VECTOR = Binary("vector", (*RIG, "test_nvm_vector.cpp"), vector=True)
#: The shipping 1x1 shape only: two doctored builds (a map the codec's byte
#: table cannot hold, which only the -Woverflow it then raises is let pass;
#: no name record) and the LiteSPI port alone on its mocked command master.
UNITS = (Binary("mapin", (*RIG, "test_nvm_shapes.cpp"), edit=(("MILAN_NVM_MAPIN_ENTRIES_0", 0x100),),
                cflags=("-Wno-overflow",), defines=("-DNVM_DOCTORED_MAPIN",)),
         Binary("noname", (*RIG, "test_nvm_shapes.cpp"), edit=(("MILAN_NVM_N_NAME", 0),),
                defines=("-DNVM_DOCTORED_NONAME",)),
         Binary("litespi", ("mock_litespi_csr.cpp", "test_nvm_litespi.cpp"), store=("plat/nvm_flash_litespi.c",),
                models=("host/nvm_fmodel.c",)),
         Binary("prefix", ("test_nvm_prefix.cpp",), store=("nvm_klj2.c",), models=(), address_sanitizer=True))
#: The journal, read out of the SoC source the way every other consumer reads it.
JOURNAL = literal("FLASHBOOT_RESERVED")["journal"]
SLOT = JOURNAL["size"] // 2
#: The identity the recorded vectors are made with
#: (scripts/check_nvm_record_space.py render_record_table).
VECTOR_IDENT = Ident(seq=7, entity_id=0x0011223344556677, model_id=0x8899AABBCCDDEEFF)
CFLAGS = ("-std=c11", "-O1", "-g", "-Wall", "-Wextra", "-Werror", "-pedantic")
#: The system clock milan_soc.py builds when the builder passes no
#: --sys-clk-freq (that option's default, sw/litex/milan_soc.py).
SOC_DEFAULT_HZ = 100_000_000


class Refusal(Exception):
    """The bench could not be built or run: exit 2, never a pass."""


@dataclass
class Bench:
    """One shape's reference side: its frames and how nvm_klj2.py packs them."""

    cfg: Path
    shape: Shape
    donor: Donor
    ident: Ident
    frames: dict[int, bytes]
    expect: dict
    #: the system clock timer0 counts, in hertz, as the shape's config sets it
    clock_hz: int

    @property
    def stem(self) -> str:
        """The shape's config name."""
        return self.cfg.stem

    def assemble(self, frames: dict[int, bytes], seq: int, ident: Ident | None = None) -> bytes:
        """The Python encoder's container for `frames` at sequence `seq`."""
        who = ident or self.ident
        return klj2_assemble(frames, self.donor, Ident(seq=seq, entity_id=who.entity_id,
                                                       model_id=who.model_id))[0]

    def offsets(self) -> dict[int, int]:
        """record_id -> offset of its frame inside the record area."""
        return klj2_assemble(self.frames, self.donor, self.ident)[1]

    def decode(self, blob: bytes) -> tuple[int, dict]:
        """What `klj2_decode` says about `blob` for this shape."""
        return klj2_decode(blob, self.donor, self.ident, self.expect)

    def erased_frames(self) -> dict[int, bytes]:
        """Every record of the shape erased."""
        return {rid: erased_record(len(fr) - REC_HDR) for rid, fr in self.frames.items()}


def shape_header(shape: Shape, donor: Donor, ident: Ident) -> str:
    """nvm_shape_gen.h for the host: what generated/soc.h carries on the target,
    from the same derivation, plus the identity and the journal."""
    values = dict(firmware_constants(shape, donor))
    values.update(MILAN_ENTITY_ID_LO=ident.entity_id & 0xFFFF_FFFF,
                  MILAN_ENTITY_ID_HI=ident.entity_id >> 32,
                  MILAN_MODEL_ID_LO=ident.model_id & 0xFFFF_FFFF,
                  MILAN_MODEL_ID_HI=ident.model_id >> 32,
                  MILAN_FLASH_JOURNAL_OFFSET=JOURNAL["offset"],
                  MILAN_FLASH_JOURNAL_SIZE=JOURNAL["size"])
    lines = ["/* generated by sw/firmware/ctrl_nvm/test/nvm_bench.py */",
             "#ifndef NVM_SHAPE_GEN_H", "#define NVM_SHAPE_GEN_H"]
    lines += [f"#define {name} 0x{value:x}u" for name, value in values.items()]
    lines.append("#endif")
    return "\n".join(lines) + "\n"


def soc_header(clock_hz: int) -> str:
    """generated/soc.h as LiteX writes the system clock, at the shape's own:
    what the LiteSPI port's timer0 counts, on the host and in the RV32 arm."""
    return ("/* generated by sw/firmware/ctrl_nvm/test/nvm_bench.py */\n"
            "#ifndef GENERATED_SOC_H\n#define GENERATED_SOC_H\n"
            f"#define CONFIG_CLOCK_FREQUENCY {clock_hz}\n#endif\n")


def write_headers(gen: Path, header: str, clock_hz: int) -> None:
    """The generated headers one build of the store reads, in `gen`."""
    (gen / "generated").mkdir(parents=True, exist_ok=True)
    (gen / "nvm_shape_gen.h").write_text(header)
    (gen / "generated" / "soc.h").write_text(soc_header(clock_hz))


def includes(tree: Path, gen: Path) -> list[str]:
    """The store's include path: the shape's generated headers first, then the
    tree's own directories and the host stubs of LiteX's CSR and memory map."""
    return [f"-I{gen}", f"-I{tree}", f"-I{tree / 'host'}", f"-I{tree / 'plat'}", f"-I{tree / 'host/stubs'}",
            f"-I{HARNESS}", f"-I{HERE}"]


def doctor(header: str, edit: tuple[tuple[str, int], ...]) -> str:
    """The shape header with each named constant replaced."""
    for name, value in edit:
        header, n = re.subn(rf"^#define {name} .*$", f"#define {name} 0x{value:x}u", header, flags=re.M)
        if n != 1:
            raise Refusal(f"the shape header defines {name} {n} times, not once")
    return header


def build_suite(inputs: ShapeInputs, work: Path, b: fw_gtest.Build, binary: Binary, tree: Path = TREE) -> Path:
    """One GoogleTest binary of one shape, from `tree`: the store with every
    warning an error (a planted copy may leave a variable unused), the host
    models, and the tests compiled from this directory against the tree's
    headers."""
    b = replace(b, address_sanitizer=binary.address_sanitizer)
    gen = work / "gen"
    header = shape_header(inputs.shape, inputs.donor, VECTOR_IDENT if binary.vector else inputs.ident)
    write_headers(gen, doctor(header, binary.edit), inputs.clock_hz)
    flags = (*(CFLAGS if tree == TREE else tuple(x for x in CFLAGS if x != "-Werror")), *binary.cflags)
    inc = includes(tree, gen)
    try:
        objects = fw_gtest.compile_c(b, flags, inc, [tree / s for s in binary.store], work / "store")
        objects += fw_gtest.compile_c(b, flags, inc, [tree / s for s in binary.models], work / "models",
                                      measured=False)
        objects += fw_gtest.compile_tests(b, inc, [HERE / s for s in binary.tests], work / "tests",
                                          (f'-DNVM_TALLY_SHAPE="{inputs.cfg.stem}"', *binary.defines))
        objects.append(fw_gtest.main_object(b, work / "harness"))
        return fw_gtest.link(b, objects, work / f"nvm_{binary.name}")
    except fw_gtest.BuildError as exc:
        raise Refusal(f"{inputs.cfg.stem}: {exc}") from exc


def run_suite(exe: Path, fixture: Path, only: Sequence[str] = ()) -> tuple[bool, str]:
    """Run a suite binary over its fixture, all of its tests or `only` these
    (GoogleTest test names); (passed, the log)."""
    args = [f"--gtest_filter={':'.join(f'*.{name}:*.{name}/*' for name in only)}"] if only else []
    env = {**os.environ, "NVM_FIXTURE": str(fixture)}
    if exe.name == "nvm_prefix":
        # Preserve the named failing test in the tally on a sanitizer error.
        env["ASAN_OPTIONS"] = "abort_on_error=1"
    return fw_gtest.run_binary(exe, args, env=env)


@dataclass(frozen=True)
class ShapeInputs:
    """What the builder says about one config, computed once and reused."""

    cfg: Path
    shape: Shape
    donor: Donor
    ident: Ident
    clock_hz: int


def sys_clock(cfg: Path, built: Path) -> int:
    """The shape's system clock in hertz, which LiteX emits as
    CONFIG_CLOCK_FREQUENCY and timer0 counts: the config's
    board.constraints.sys_clk_hz, held to what the builder hands milan_soc.py
    (its --sys-clk-freq, or that option's default when it passes none)."""
    argv = json.loads((built / cfg.stem / "soc_params.json").read_text())["argv"]
    soc = (int(float(argv[argv.index("--sys-clk-freq") + 1])) if "--sys-clk-freq" in argv
           else SOC_DEFAULT_HZ)
    constraints = yaml.safe_load(cfg.read_text())["board"]["constraints"]
    hz = int(constraints.get("sys_clk_hz", soc))
    if hz != soc:
        raise Refusal(f"{cfg.stem}: sys_clk_hz is {hz} Hz but milan_soc.py is given {soc} Hz")
    return hz


def shape_inputs(cfg: Path, work: Path) -> ShapeInputs:
    """Run the builder for `cfg` and read its shape, identity and clock back."""
    names, dc, spi, spo = build(cfg, work / "builder")
    overlay = json.loads((work / "builder" / cfg.stem / "aem_overlay.json").read_text())
    ident = Ident(seq=0, entity_id=int(overlay["adp"]["entity_id"], 16),
                  model_id=int(overlay["entity"]["entity_model_id"], 16))
    return ShapeInputs(cfg=cfg, shape=Shape(cfg=cfg, names=names, dc=dc, spi=spi, spo=spo),
                       donor=Donor(base=binding_base(), layout=layout_version()), ident=ident,
                       clock_hz=sys_clock(cfg, work / "builder"))


def make_bench(inputs: ShapeInputs, ident: Ident | None = None) -> Bench:
    """The reference side of one shape (under `ident`, the shape's own identity
    unless given): its golden records framed by nvm_klj2.py."""
    who = ident or inputs.ident
    frames = {r: frame_record(r, payload_bytes(g, i, r, p), inputs.donor.layout)
              for g, i, r, p, _b in inventory(inputs.shape, inputs.donor.base) if r is not None}
    return Bench(cfg=inputs.cfg, shape=inputs.shape, donor=inputs.donor, ident=who, frames=frames,
                 expect=expected_payloads(inputs.shape), clock_hz=inputs.clock_hz)
