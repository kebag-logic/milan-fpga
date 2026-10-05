# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""nvm_bench.py - build and run the saved-state store's host suite for one shape.

One `Bench` per shipped shape: the builder's shape and identity, the Python
encoder's frames for that shape (scripts/nvm_klj2.py, the reference), the
generated constants header the C store compiles against (the SAME derivation
sw/litex/milan_soc.py publishes for the shipping writer), and the compiled
scenario runner. A `Run` is one execution of that runner, parsed.
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

HERE = Path(__file__).resolve().parent
TREE = HERE.parent
ROOT = HERE.parents[3]
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "sw/litex"))

from nvm_contract import REC_HDR, Donor, Ident, Shape                  # noqa: E402
from nvm_klj2 import (erased_record, frame_record, klj2_assemble,      # noqa: E402
                      klj2_decode, payload_bytes)
from nvm_shape import (binding_base, build, firmware_constants,        # noqa: E402
                       inventory, layout_version)
from check_nvm_record_space import expected_payloads                   # noqa: E402
from flash_map import literal                                          # noqa: E402

#: The store as it ships, both flash ports, both host models and the runner.
SOURCES = ("nvm_klj2.c", "nvm_store.c", "nvm_flash.c", "plat/nvm_flash_litespi.c",
           "host/nvm_fmodel.c", "host/nvm_smodel.c", "host/litespi_model.c",
           "test/nvm_test.c")
#: The journal, read out of the SoC source the way every other consumer reads it.
JOURNAL = literal("FLASHBOOT_RESERVED")["journal"]
SLOT = JOURNAL["size"] // 2
#: The identity the recorded vectors are made with
#: (scripts/check_nvm_record_space.py render_record_table).
VECTOR_IDENT = Ident(seq=7, entity_id=0x0011223344556677, model_id=0x8899AABBCCDDEEFF)
CFLAGS = ("-std=c11", "-O1", "-g", "-Wall", "-Wextra", "-Werror", "-pedantic")
SUMMARY_RE = re.compile(r"^SUMMARY (.*)$", re.M)
POWERCUT_RE = re.compile(r"^POWERCUT (.*)$", re.M)
GUARD_RE = re.compile(r"^GUARD took=(\d+)$", re.M)
ERASES_RE = re.compile(r"^ERASES(.*)$", re.M)


class Refusal(Exception):
    """The bench could not be built or run: exit 2, never a pass."""


@dataclass
class Run:
    """One execution of the scenario runner, parsed."""

    out: str
    s: dict[str, int]
    powercut: dict[str, int]
    guard: int | None
    erases: list[int]
    fails: list[str]


@dataclass
class Bench:
    """One shape's compiled store and the Python side of its images."""

    cfg: Path
    shape: Shape
    donor: Donor
    ident: Ident
    work: Path
    binary: Path
    frames: dict[int, bytes]
    expect: dict
    runs: int = 0
    #: the same store compiled under the recorded vectors' identity, for the
    #: shapes tb/verilator/nvm_backend records a vector of
    vector: Bench | None = None

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

    def file(self, name: str, blob: bytes) -> str:
        """Write `blob` into the bench's directory; its path."""
        path = self.work / name
        path.write_bytes(blob)
        return str(path)

    def run(self, *args: str) -> Run:
        """Run the scenario script `args`; the parsed result."""
        self.runs += 1
        r = subprocess.run([str(self.binary), *args], capture_output=True, text=True,
                           cwd=self.work, check=False)
        if r.returncode:
            raise Refusal(f"{self.stem}: runner exit {r.returncode} for {' '.join(args)}\n"
                          f"{r.stdout}\n{r.stderr}")
        summary: dict[str, int] = {}
        for line in SUMMARY_RE.findall(r.stdout):
            summary.update({k: int(v) for k, v in (kv.split("=") for kv in line.split())})
        cut = POWERCUT_RE.search(r.stdout)
        guard = GUARD_RE.search(r.stdout)
        erases = ERASES_RE.search(r.stdout)
        return Run(out=r.stdout, s=summary,
                   powercut={k: int(v) for k, v in (kv.split("=") for kv in cut.group(1).split())}
                   if cut else {},
                   guard=int(guard.group(1)) if guard else None,
                   erases=[int(x) for x in erases.group(1).split()] if erases else [],
                   fails=re.findall(r"^FAIL .*$", r.stdout, re.M))


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


def compile_runner(tree: Path, work: Path, header: str) -> Path:
    """Build the scenario runner from `tree`: the store with every warning an
    error, or a planted copy, where a defect may leave a variable unused."""
    gen = work / "gen"
    gen.mkdir(parents=True, exist_ok=True)
    (gen / "nvm_shape_gen.h").write_text(header)
    binary = work / "nvm_test"
    flags = CFLAGS if tree == TREE else tuple(x for x in CFLAGS if x != "-Werror")
    cmd = ["gcc", *flags, f"-I{gen}", f"-I{tree / 'host/stubs'}",
           *(str(tree / s) for s in SOURCES), "-o", str(binary)]
    r = subprocess.run(cmd, capture_output=True, text=True, check=False)
    if r.returncode:
        raise Refusal(f"host build failed in {work}:\n{r.stderr}")
    return binary


@dataclass(frozen=True)
class ShapeInputs:
    """What the builder says about one config, computed once and reused."""

    cfg: Path
    shape: Shape
    donor: Donor
    ident: Ident


def shape_inputs(cfg: Path, work: Path) -> ShapeInputs:
    """Run the builder for `cfg` and read its shape and identity back."""
    names, dc, spi, spo = build(cfg, work / "builder")
    overlay = json.loads((work / "builder" / cfg.stem / "aem_overlay.json").read_text())
    ident = Ident(seq=0, entity_id=int(overlay["adp"]["entity_id"], 16),
                  model_id=int(overlay["entity"]["entity_model_id"], 16))
    return ShapeInputs(cfg=cfg, shape=Shape(cfg=cfg, names=names, dc=dc, spi=spi, spo=spo),
                       donor=Donor(base=binding_base(), layout=layout_version()), ident=ident)


def make_bench(inputs: ShapeInputs, work: Path, tree: Path = TREE,
               ident: Ident | None = None) -> Bench:
    """Compile the store from `tree` for one shape (under `ident`, the shape's
    own identity unless given) and frame its golden records."""
    who = ident or inputs.ident
    binary = compile_runner(tree, work, shape_header(inputs.shape, inputs.donor, who))
    frames = {r: frame_record(r, payload_bytes(g, i, r, p), inputs.donor.layout)
              for g, i, r, p, _b in inventory(inputs.shape, inputs.donor.base) if r is not None}
    return Bench(cfg=inputs.cfg, shape=inputs.shape, donor=inputs.donor, ident=who, work=work,
                 binary=binary, frames=frames, expect=expected_payloads(inputs.shape))


def read_state(path: Path) -> dict[int, tuple[int, bytes]]:
    """The runner's --dump-state file: record id -> (valid, payload)."""
    out = {}
    for line in path.read_text().splitlines():
        _tag, rid, valid, *rest = line.split()
        out[int(rid)] = (int(valid), bytes.fromhex(rest[0]) if rest else b"")
    return out


def default_payload(rid: int, plen: int) -> bytes:
    """The state model's image default for a record (host/nvm_smodel.c)."""
    return bytes((rid * 7 + j * 3 + 0x5A) & 0xFF for j in range(plen))
