#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Run and grade the saved-state snapshot-ownership co-simulation.

This is the suite's runner. It builds the SHIPPING
``hdl/milan/KL_nvm_backend.sv`` and the SHIPPING
``sw/firmware/milan_baremetal/milan_baremetal.c`` -- the writer compiled for
the host, its two CSR primitives routed to the model, exactly as
``sw/firmware/nvm_hosttest`` routes them -- against the REAL donor producer
path at the pinned revision, and runs every EXECUTED case of section 9 of
``docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md`` over them.

Three things it does that a plain Verilator suite does not:

* **The firmware is in the loop.** The writer's own boot, capture, seal,
  program and acknowledge sequence drives the RTL, so what is graded is the
  pair, not the module. `cosim_host.c` models the flash, the DDR window and
  the clock; every PP_NVM access reaches the Verilated backend.
* **Each case is graded by NAMED checks** over a dumped journal, decoded with
  the repository's own ``scripts/nvm_klj2.py`` and compared against records
  this file frames independently. `cosim_cases.cpp` is stimulus only.
* **Every mutant the page names is killed by its named check** (``mutate.py``),
  and the three historical defects are run RED against a pre-contract backend
  and writer to show the checks are not vacuous in either direction.

WHAT IT DOES NOT MODEL, stated plainly: CPU instruction time, DDR and bus
latency and arbitration, clock-domain crossings, the product's clock rate and
real flash timing. The backend clock is 1 MHz of MODEL time, so one cycle is
one microsecond and the deadlines, the hold and the heartbeat are counted in
it. See README.md.
"""
from __future__ import annotations

import argparse
import concurrent.futures as cf
import dataclasses
import json
import os
import re
import shutil
import struct
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
STUBS = HERE / "stubs"
BUILD = HERE / "build"
RUNS = HERE / "runs"

PP = "protocol-processor/hdl"
#: the donor sources the model compiles: the binding record manager, the
#: device-face initiator, the AECP dynamic-state store and their package
DONOR_SV = [f"{PP}/acmp/pp_acmp_pkg.sv", f"{PP}/aecp/KL_aecp_dyn_state.sv",
            f"{PP}/acmp/KL_acmp_nvm_shadow.sv", f"{PP}/packet_engine/KL_pp_nvm_port.sv"]
BACKEND = "hdl/milan/KL_nvm_backend.sv"
WRITER = "sw/firmware/milan_baremetal/milan_baremetal.c"
SHAPES = {"1x1": "configs/endstation_ax7101_1x1_tdm8.yaml",
          "8x8": "configs/endstation_ax7101_8x8.yaml"}
CLK_HZ = 1_000_000      # the backend clock in MODEL time: one cycle is 1 us
T_HOLD_MS = 50
TAG_C3 = 0xC3
#: `fence rw, rw` statements in the shipping writer: the capture, the window
#: load and the AEM image check. A writer from before the contract has one.
FENCES_CONTRACT, FENCES_LEGACY = 3, 1

sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "sw" / "firmware" / "nvm_hosttest"))
import test_nvm_firmware as ref   # noqa: E402  (the repository's own host gate)
from nvm_klj2 import klj2_decode  # noqa: E402
from nvm_contract import VD_OK    # noqa: E402


def cmd(argv: list[str], log: Path, cwd: Path = ROOT, timeout: int = 3600):
    """Run one build command, log it, and refuse on a non-zero exit."""
    log.parent.mkdir(parents=True, exist_ok=True)
    p = subprocess.run(argv, cwd=cwd, text=True, capture_output=True, timeout=timeout,
                       env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"})
    log.write_text(p.stdout + p.stderr)
    if p.returncode:
        raise SystemExit(f"FAILED ({p.returncode}): {' '.join(map(str, argv))}\n  see {log}")
    return p


# -------------------------------------------------------------------- shapes
@dataclasses.dataclass
class ShapeInfo:
    name: str
    header: str            # the generated constants header
    records: Path          # the record table from the record-space gate
    params: dict
    donor: object
    ident: object
    expect: dict
    img_len: int
    recs: dict             # rid -> (offset, framed length)


def shape(name: str) -> ShapeInfo:
    """One shape, built from the repository's own generators: the record
    table from the record-space gate, the constants header and the expected
    payloads from the host gate, and the name bound from the generated RTL
    header, which must agree with the AEMI image's."""
    cfg = ROOT / SHAPES[name]
    work = BUILD / f"shape-{name}"
    work.mkdir(parents=True, exist_ok=True)
    names, dc, spi, spo = ref.build(cfg, work / "builder")
    shp = ref.Shape(cfg=cfg, names=names, dc=dc, spi=spi, spo=spo)
    donor = ref.Donor(base=ref.binding_base(), layout=ref.layout_version())
    overlay = json.loads((work / "builder" / cfg.stem / "aem_overlay.json").read_text())
    ident = ref.Ident(seq=0, entity_id=int(overlay["adp"]["entity_id"], 16),
                      model_id=int(overlay["entity"]["entity_model_id"], 16))
    table = work / "records.txt"
    cmd([sys.executable, "-B", "scripts/check_nvm_record_space.py", "--emit-record-table",
         str(cfg), "-o", str(table)], BUILD / "logs" / f"shape-{name}-record-table.log")
    recs, img_len = {}, 0
    for ln in table.read_text().splitlines():
        f = ln.split()
        if f and f[0] == "imglen":
            img_len = int(f[1])
        if f and f[0] == "rec":
            recs[int(f[1], 16)] = (int(f[2]), int(f[3]))
    svh = (ROOT / "configs/generated" / cfg.stem / "gen/adp_shape_defaults.svh").read_text()
    n_name = int(re.search(r"AEM_NAME_ENTRIES_C = (\d+);", svh).group(1))
    if n_name != names:
        raise SystemExit(f"shape {name}: the AEMI header says {names} names, the generated "
                         f"RTL header {n_name}")
    params = dict(N_STREAM_IN_P=dc["STREAM_INPUT"], N_STREAM_OUT_P=dc["STREAM_OUTPUT"],
                  N_SPORT_IN_P=dc["STREAM_PORT_INPUT"], N_SPORT_OUT_P=dc["STREAM_PORT_OUTPUT"],
                  N_AUDIO_UNIT_P=dc["AUDIO_UNIT"], N_CLK_DOM_P=dc["CLOCK_DOMAIN"],
                  N_NAME_P=names)
    return ShapeInfo(name, ref.constants_header(shp, donor, ident), table, params, donor,
                     ident, ref.expected_payloads(shp), img_len, recs)


def legacy_header(current: str) -> str:
    """The generator from BEFORE the contract, for the non-vacuity control:
    MILAN_NVM_LIVE_BASE, MILAN_NVM_STAGE_BASE and MILAN_NVM_CONTRACT are the
    contract-3 generator's (section 14), so a pre-contract writer is compiled
    against the constant it names, MILAN_NVM_IMAGE_BASE, and against nothing
    else this generator added."""
    out = []
    for ln in current.splitlines():
        if ln.startswith("#define MILAN_NVM_LIVE_BASE"):
            out.append(ln.replace("MILAN_NVM_LIVE_BASE", "MILAN_NVM_IMAGE_BASE"))
        elif ln.startswith(("#define MILAN_NVM_STAGE_BASE", "#define MILAN_NVM_CONTRACT")):
            continue
        else:
            out.append(ln)
    assert "MILAN_NVM_IMAGE_BASE" in "\n".join(out)
    return "\n".join(out) + "\n"


# ------------------------------------------------------------------ firmware
FW_SUBS = [
    ("static inline uint32_t milan_read(unsigned int offset)\n{\n\treturn *milan_reg(offset);\n}",
     "static inline uint32_t milan_read(unsigned int offset)\n{\n\treturn nvm_host_csr_read(offset);\n}"),
    ("\t*milan_reg(offset) = value;\n\t__asm__ volatile(\"fence iorw, iorw\" ::: \"memory\");\n",
     "\tnvm_host_csr_write(offset, value);\n"),
]
FENCE_RW = "__asm__ volatile(\"fence rw, rw\" ::: \"memory\");"


def host_firmware(text: str, fences: int) -> str:
    """The host build of the writer: the two CSR access primitives route to
    the model and the remaining fences are blanked, the same adapter the
    repository's host gate applies -- COUNTED, so a seam that moves stops the
    build rather than silently compiling a different program."""
    for old, new in FW_SUBS:
        if text.count(old) != 1:
            raise SystemExit(f"firmware seam count {text.count(old)}: {old[:50]!r}")
        text = text.replace(old, new)
    if text.count(FENCE_RW) != fences:
        raise SystemExit(f"expected {fences} rw fences, found {text.count(FENCE_RW)}")
    return text.replace(FENCE_RW, "(void)0;")


#: the writer's file-scope state and its initial value: what a CPU-only reset
#: gives back (the C start-up zeroes .bss and reloads .data)
WRITER_STATICS = {"nvm_ready": "0", "nvm_retired": "0", "nvm_in_commit": "0", "nvm_seq": "0",
                  "nvm_auth_slot": "NVM_SLOT_NONE", "nvm_verdict_a": "0",
                  "nvm_verdict_b": "0", "nvm_last_verdict": "0", "nvm_commits_ok": "0",
                  "nvm_commits_failed": "0", "nvm_captures_refused": "0",
                  "nvm_acks_refused": "0", "nvm_hb_last": "0", "nvm_dirty_since": "0"}


def host_restart(text: str) -> str:
    """HOST MODEL ONLY, appended to the host build of the writer: a CPU-only
    reset, the writer's restart without a fabric reset. Refuses unless it
    names every file-scope variable of the writer, so a new one cannot
    survive the modelled reset unnoticed. NOTHING ELSE of a CPU reset is
    modelled -- not the boot code's memory initialisation, not the memory
    holding the live window, not the bus fabric -- so W1 to W4 ASSUME
    obligation O4 of the contract page and cannot test it."""
    found = set(re.findall(r"^static (?:int|uint32_t|uint64_t|unsigned int) (nvm_\w+)(?: = [^;(]+)?;$",
                           text, re.M))
    if found != set(WRITER_STATICS):
        raise SystemExit(f"writer statics {sorted(found)} != restart model {sorted(WRITER_STATICS)}")
    body = "".join(f"\t{k} = {v};\n" for k, v in WRITER_STATICS.items())
    return ("\n/* HOST MODEL ONLY, appended by run_cases.py: a CPU-only reset of the\n"
            " * writer. The fabric, the backend and the media keep their state; every\n"
            " * static of the writer returns to its initial value and the writer boots\n"
            " * again. */\n"
            "void nvm_host_writer_restart(void);\n"
            "void nvm_host_writer_restart(void)\n{\n" + body +
            "\tset_idle_hook(0);\n\tnvm_boot();\n}\n")


# -------------------------------------------------------------------- builds
@dataclasses.dataclass
class Build:
    name: str
    shape: str
    contract: bool = True       # the shipping backend and writer
    rtl_mut: str = ""           # a mutate.py mutation name
    fw_mut: str = ""
    glue_mut: str = ""
    cap_id_w: int = 16
    binary: Path | None = None


def mutate(kind: str, name: str, src: Path, dst: Path) -> None:
    cmd([sys.executable, "-B", str(HERE / "mutate.py"), kind, name, str(src), str(dst)],
        BUILD / "logs" / f"mutate-{name}.log", cwd=HERE)


def do_build(b: Build, shapes: dict[str, ShapeInfo], jobs: int) -> Build:
    s = shapes[b.shape]
    work = BUILD / b.name
    if work.exists():
        shutil.rmtree(work)
    (work / "generated").mkdir(parents=True)
    (work / "generated" / "soc.h").write_text(
        s.header if b.contract else legacy_header(s.header))
    fw_src = ROOT / WRITER if b.contract else LEGACY_DIR / "milan_baremetal.c"
    fw_path = work / "writer.c"
    if b.fw_mut:
        mutate("fw", b.fw_mut, fw_src, fw_path)
    else:
        fw_path.write_text(Path(fw_src).read_text())
    host = host_firmware(fw_path.read_text(),
                         FENCES_CONTRACT if b.contract else FENCES_LEGACY)
    if b.contract:
        host += host_restart(fw_path.read_text())
    (work / "milan_baremetal.host.c").write_text(host)
    be_src = ROOT / BACKEND if b.contract else LEGACY_DIR / "KL_nvm_backend.sv"
    if b.rtl_mut:
        mutate("rtl", b.rtl_mut, be_src, work / "KL_nvm_backend.sv")
    else:
        (work / "KL_nvm_backend.sv").write_text(Path(be_src).read_text())
    if b.glue_mut:
        mutate("glue", b.glue_mut, HERE / "cosim_top.sv", work / "cosim_top.sv")
    else:
        (work / "cosim_top.sv").write_text((HERE / "cosim_top.sv").read_text())
    defs = [f"-DNVM_HOST_JOURNAL_OFFSET=0x{ref.JOURNAL:x}u",
            f"-DNVM_HOST_AEM_OFFSET=0x{ref.AEM_OFFSET:x}u",
            f"-DNVM_HOST_IMAGE_OFF=0x{ref.IMAGE_OFF:x}u"]
    cc = ["gcc", "-std=gnu11", "-O2", "-g", "-Wall", "-Wextra", "-Werror",
          f"-I{work}", f"-I{HERE}", f"-I{STUBS}"]
    cmd(cc + defs + ["-c", str(HERE / "cosim_host.c"), "-o", str(work / "host.o")],
        BUILD / "logs" / f"{b.name}-host.log")
    cmd(cc + ["-Wno-format", "-c", str(work / "milan_baremetal.host.c"),
              "-o", str(work / "fw.o")], BUILD / "logs" / f"{b.name}-fw.log")
    gparams = [f"-G{k}={v}" for k, v in s.params.items()] + [f"-GCLK_HZ_P={CLK_HZ}"]
    if b.contract:
        gparams += [f"-GT_HOLD_MS_P={T_HOLD_MS}", f"-GCAP_ID_W_P={b.cap_id_w}"]
    vl = ["verilator", "--cc", "--exe", "--build", "-j", str(jobs), "--top-module", "cosim_top",
          "--Mdir", str(work / "obj"), "-Wall", "-Wno-fatal", "-Wno-UNUSEDSIGNAL",
          "-Wno-UNUSEDPARAM", "--x-assign", "unique", "--x-initial", "unique"]
    if b.contract:
        vl.append("+define+NVM_CONTRACT_3")
    vl += gparams
    vl += ["-CFLAGS", f"-std=c++17 -O2 -I{HERE} -I{STUBS} {' '.join(defs)}",
           "-LDFLAGS", f"{work / 'host.o'} {work / 'fw.o'}"]
    vl += [str(ROOT / p) for p in DONOR_SV]
    vl += [str(work / "KL_nvm_backend.sv"), str(work / "cosim_top.sv"),
           str(HERE / "cosim_bridge.cpp"), str(HERE / "cosim_cases.cpp"), "-o", "cosim"]
    cmd(vl, BUILD / "logs" / f"{b.name}-verilator.log")
    b.binary = work / "obj" / "cosim"
    return b


# ------------------------------------------------------------------- running
@dataclasses.dataclass
class Run:
    case: str
    build: str
    variant: str
    exit: int
    wall_s: float
    obs: dict
    notes: dict
    evts: list
    fw: list
    done: bool
    pending: bool
    outdir: Path


def run_case(b: Build, shapes: dict[str, ShapeInfo], case: str, variant: str = "",
             extra: tuple = ()) -> Run:
    s = shapes[b.shape]
    tag = case + (f"~{variant}" if variant else "")
    out = RUNS / b.name / tag
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)
    argv = [str(b.binary), "--case", case, "--out", str(out), "--records", str(s.records),
            *extra]
    t0 = time.time()
    p = subprocess.run(argv, text=True, capture_output=True, timeout=900)
    wall = time.time() - t0
    (out / "stdout.log").write_text(p.stdout)
    (out / "stderr.log").write_text(p.stderr)
    obs, notes, evts, fw, done, pending = {}, {}, [], [], False, False
    for ln in p.stdout.splitlines():
        if ln.startswith("OBS "):
            o = json.loads(ln[4:])
            obs[o["tag"]] = o
        elif ln.startswith("NOTE "):
            n = json.loads(ln[5:])
            notes[n["key"]] = n
        elif ln.startswith("EVT "):
            evts.append(json.loads(ln[4:]))
        elif ln.startswith("Milan NVM:"):
            fw.append(ln)
        elif ln.startswith("CASE_DONE"):
            done = True
            pending = ln.endswith("hooks_pending=1")
    return Run(case, b.name, variant, p.returncode, wall, obs, notes, evts, fw, done, pending,
               out)


# -------------------------------------------------------------------- oracle
def crc16(d: bytes) -> int:
    c = 0xFFFF
    for x in d:
        c ^= x << 8
        for _ in range(8):
            c = ((c << 1) ^ 0x1021) & 0xFFFF if c & 0x8000 else (c << 1) & 0xFFFF
    return c


def frame(rid: int, payload: bytes) -> bytes:
    hdr = bytes([0x17, 0x22, 0x02, rid, len(payload) >> 8, len(payload) & 0xFF])
    return hdr + crc16(hdr + payload).to_bytes(2, "big") + payload


def bind_frame(sink, bound, started, sw, uid, teid, ceid) -> bytes:
    pl = bytes([bound | started << 1 | sw << 2, 0]) + uid.to_bytes(2, "big") + \
        teid.to_bytes(8, "big") + ceid.to_bytes(8, "big")
    return frame(0x20 + sink, pl)


B = {  # the case file's bindings, framed independently here
    "X": (0, 1, 1, 0, 1, 0x1122334455667788, 0x99aabbccddeeffff),
    "X2": (0, 1, 0, 0, 1, 0x1122334455667788, 0x99aabbccddeeffff),
    "X3": (0, 1, 1, 1, 3, 0x2122232425262728, 0x99aabbccddeeffff),
    "Z": (1, 1, 1, 0, 2, 0x0102030405060708, 0x1112131415161718),
    "Z2": (1, 1, 0, 0, 2, 0x0102030405060708, 0x1112131415161718),
    "Z3": (1, 1, 1, 1, 4, 0x3132333435363738, 0x1112131415161718),
}
F = {k: bind_frame(*v) for k, v in B.items()}
F["FMT_A"] = frame(0x30, bytes([0x00, 0xA0, 0x02, 0x01, 0x00, 0x40, 0x00, 0x08]))


class Ctx:
    """What a check may read about one run."""

    def __init__(self, run: Run, s: ShapeInfo):
        self.r, self.s = run, s
        self._slots = {}

    def o(self, tag):
        if tag not in self.r.obs:
            raise KeyError(f"no observation '{tag}'")
        return self.r.obs[tag]

    def contract(self, tag="boot"):
        return (self.o(tag)["stat"] >> 24) == TAG_C3

    def newest(self, tag):
        """The slot the A/B rule of section 7 would offer, decoded by the
        repository's klj2_decode: (letter, blob, seq) or None."""
        if tag in self._slots:
            return self._slots[tag]
        ok = []
        for letter in "AB":
            raw = (self.r.outdir / f"{tag}-slot{letter}.bin").read_bytes()
            n = struct.unpack_from("<I", raw, 16)[0] if raw[:4] != b"\xff" * 4 else 0
            blob = raw[:n] if 44 <= n <= 65536 else raw[:44]
            vd, _ = klj2_decode(blob, self.s.donor, self.s.ident, self.s.expect)
            if vd == VD_OK:
                ok.append((letter, blob, struct.unpack_from("<I", blob, 8)[0]))
        res = None
        if len(ok) == 2:
            a, b = ok
            d = (a[2] - b[2]) & 0xFFFFFFFF
            res = a if d < 0x80000000 else b
        elif ok:
            res = ok[0]
        self._slots[tag] = res
        return res

    def rec(self, tag, rid):
        n = self.newest(tag)
        if n is None:
            return None
        off, ln = self.s.recs[rid]
        return n[1][40 + off:40 + off + ln]

    def durable_claim(self, tag):
        """What a reader of the published bits concludes: durable when
        backed, not dirty, not stale and -- on a build that has it, per the
        owner decision -- nothing pending. The tracked build has no pending
        bit, so its claim is the section 9.3 (1, 0, 0) row."""
        o = self.o(tag)
        return (o["backed"] == 1 and o["dirty_pub"] == 0 and o["stale"] == 0
                and o["pend"] == 0)

    def dirty_img(self, tag):
        return (self.o(tag)["stat"] >> 8) & 1


def erased(b: bytes | None) -> bool:
    return b is not None and all(x == 0xFF for x in b)


def ck(name, fn):
    return (name, fn)


def c_rec(tag, rid, key, label):
    def f(c):
        got = c.rec(tag, rid)
        if got is None:
            return False, f"no accepted slot at {tag}"
        return got == F[key], f"record 0x{rid:02x} at {tag}: {'expected ' + key if got == F[key] else ('ERASED' if erased(got) else got.hex())}"
    return ck(f"{label}@{tag}:0x{rid:02x}", f)


def c_rec_in(tag, rid, keys, label):
    def f(c):
        got = c.rec(tag, rid)
        if got is None:
            return False, f"no accepted slot at {tag}"
        hit = [k for k in keys if F[k] == got]
        return bool(hit), f"record 0x{rid:02x} at {tag}: {hit[0] if hit else ('ERASED' if erased(got) else got.hex())}"
    return ck(f"{label}@{tag}:0x{rid:02x}", f)


def c_converged(tag, want):
    """Convergence is the records AND the published status: once changes
    stop, the slot holds them, nothing is committable, and the status claims
    durability again. A bit held at 1 to make a safety check pass (nvm_dirty
    or the pending bit) fails here."""
    def f(c):
        bad = [f"0x{r:02x}" for r, k in want.items() if c.rec(tag, r) != F[k]]
        di = c.dirty_img(tag)
        claim = c.durable_claim(tag)
        return (not bad and di == 0 and claim), \
            f"mismatched {bad or 'none'}, committable work {di}, status claims durable {claim}"
    return ck(f"converged@{tag}", f)


def c_arm_in_gap(rid):
    """The case really placed the arm between the port's ERASE completion and
    the grant of the WRITE that completes the same logical record."""
    def f(c):
        if "erase_done_before_arm" not in c.r.notes:
            return None, "hook not reached on this build"
        t = c.r.notes["erase_done_before_arm"]["value"]
        arm = min([a for a in strobes(c, 0x8) if a >= t], default=None)
        er = [o for o in op_evts(c, "port", rid, 2) if o["end"] and o["end"] <= t]
        wr = [o for o in op_evts(c, "port", rid, 1) if er and o["req"] >= er[-1]["end"]]
        if arm is None or not er or not wr:
            return False, "no ERASE, WRITE and arm to order"
        ok = er[-1]["end"] <= arm <= wr[0]["gnt"]
        return ok, (f"ERASE done at {er[-1]['end']}, arm at {arm}, WRITE requested at "
                    f"{wr[0]['req']} and granted at {wr[0]['gnt']}")
    return ck(f"arm_inside_erase_write_gap:0x{rid:02x}", f)


def c_inflight_at_arm(rid):
    """Revision b premise of A11: the BFM WRITE was GRANTED before the arm
    edge and was still in flight at it (not requested on the arm's own
    edge, which is deferred now)."""
    def f(c):
        wr = [o for o in op_evts(c, "bfm", rid, 1)]
        arms = strobes(c, 0x8)
        if not wr or not arms:
            return None, "no WRITE or no arm on this build"
        w = wr[-1]
        arm = min([a for a in arms if a >= w["gnt"]], default=None)
        ok = arm is not None and w["gnt"] < arm < w["end"]
        return ok, f"WRITE granted {w['gnt'] - arm if arm else None} relative to the arm, ends {w['end'] - arm if arm else None}"
    return ck(f"write_in_flight_at_arm:0x{rid:02x}", f)


def c_copy_in_gap(rid):
    """The ERASE was granted before the arm, completed with done before the
    firmware read the ownership vector, and the WRITE of the same logical
    record was requested before that read and granted only at or after the
    attestation: the capture looked at the record inside the gap."""
    def f(c):
        if "gap_observed" not in c.r.notes:
            return None, "hook not reached on this build"
        t = c.r.notes["gap_observed"]["value"]
        arm = max([a for a in strobes(c, 0x8) if a <= t], default=None)
        cert = min([x for x in strobes(c, 0x10) if x >= t], default=None)
        er = [o for o in op_evts(c, "port", rid, 2)
              if arm is not None and o["gnt"] <= arm and o["end"] and o["end"] <= t]
        wr = [o for o in op_evts(c, "port", rid, 1) if er and o["req"] >= er[-1]["end"]]
        if arm is None or cert is None or not er or not wr:
            return False, "no ERASE, arm, gap and WRITE to order"
        e, w = er[-1], wr[0]
        ok = e["gnt"] <= arm and e["end"] <= t < cert <= w["gnt"] and w["req"] < t
        return ok, (f"relative to the arm: ERASE granted {e['gnt'] - arm}, done {e['end'] - arm}; "
                    f"ownership read after {t - arm}; WRITE requested {w['req'] - arm}, granted "
                    f"{w['gnt'] - arm}; attestation {cert - arm}")
    return ck(f"capture_inside_erase_write_gap:0x{rid:02x}", f)


def c_ack_only_slot(tag, rid, key):
    def f(c):
        in_slot = c.rec(tag, rid) == F[key]
        di = c.dirty_img(tag)
        return (in_slot or di == 1), f"newer record in slot {in_slot}, still owned (dirty) {di}"
    return ck(f"ack_retires_only_slot@{tag}:0x{rid:02x}", f)


def c_no_durable_claim(tag, accepted):
    def f(c):
        missing = [f"0x{r:02x}" for r, k in accepted.items() if c.rec(tag, r) != F[k]]
        claim = c.durable_claim(tag)
        return not (missing and claim), f"accepted but not in the slot {missing or 'none'}; status claims durable {claim}"
    return ck(f"no_durable_claim@{tag}", f)


def c_alarm_revokes(tag):
    def f(c):
        o = c.o(tag)
        return not (o["alarm"] and o["backed"]), f"alarm {o['alarm']} backed {o['backed']}"
    return ck(f"alarm_revokes@{tag}", f)


def c_no_101():
    def f(c):
        last = max(c.r.obs.values(), key=lambda o: o["cycle"])
        return last["bad101"] == 0, f"cycles holding (backed 1, dirty 0, stale 1): {last['bad101']}"
    return ck("unreachable_row_never_held", f)


def c_stuck_reported(tag):
    def f(c):
        o = c.o(tag)
        return o["dev_busy"] == 1 and not c.durable_claim(tag), f"dev_busy {o['dev_busy']} durable claim {c.durable_claim(tag)}"
    return ck(f"stuck_record_reported@{tag}", f)


def c_unres_bits(tag, rids):
    def f(c):
        if not c.contract(tag):
            return None, "no ownership vector on this build"
        own = c.o(tag)["own"]
        got = sorted(w * 32 + b for w in range(8) for b in range(32) if (own[w] >> b) & 1)
        return got == sorted(rids), f"open records {[hex(x) for x in got]}"
    return ck(f"open_records_named@{tag}", f)


def c_first_boot_blank(tag):
    def f(c):
        n = c.newest(tag)
        if n is None:
            return False, "no accepted slot"
        bad = [hex(r) for r in c.s.recs if not erased(c.rec(tag, r))]
        return not bad, f"framed records {bad or 'none'} (all must be erased)"
    return ck(f"first_boot_erased_image_accepted@{tag}", f)


def op_evts(c, src=None, rid=None, op=None):
    return [e for e in c.r.evts if e["k"] == "op" and (src is None or e["src"] == src)
            and (rid is None or e["rid"] == rid) and (op is None or e["op"] == op)]


def strobes(c, bit):
    return [e["cyc"] for e in c.r.evts if e["k"] == "strobe" and e["v"] & bit and not e["stray"]]


def held_op(c, src, rid):
    """The first ERASE of this source on this record REQUESTED while a
    capture was open and not yet attested or released, with that capture's
    arm: the request the hold must defer. An earlier operation on the same
    record (the base bindings the real manager flushes before any capture)
    is not it, which is why this is not simply the first operation."""
    arms = strobes(c, 0x8)
    ends = sorted(strobes(c, 0x10) + strobes(c, 0x20))
    for op in op_evts(c, src, rid, 2):
        arm = max([a for a in arms if a <= op["req"]], default=None)
        if arm is None:
            continue
        end = min([x for x in ends if x >= arm], default=None)
        if end is None or op["req"] <= end:
            return op, arm
    return None, None


def c_deferred(rid, src="bfm"):
    def f(c):
        if not op_evts(c, src, rid, 2) or not strobes(c, 0x8):
            return None, "no request or no capture on this build"
        op, arm = held_op(c, src, rid)
        if op is None:
            return False, "no request landed inside a capture"
        cert = min([x for x in strobes(c, 0x10) if x >= arm], default=None)
        if cert is None:
            return False, f"request at {op['req']}: its capture was never attested"
        ok = op["gnt"] >= cert and op["gnt"] - arm <= T_HOLD_MS * 1000 + 1000
        return ok, f"requested {op['req'] - arm} cycles after the arm, granted {op['gnt'] - arm} after it, attestation at {cert - arm}"
    return ck(f"deferred_until_attestation:0x{rid:02x}" + ("" if src == "bfm" else f":{src}"), f)


def c_hold_bounded(rid, src="bfm"):
    def f(c):
        if not op_evts(c, src, rid, 2) or not strobes(c, 0x8):
            return None, "no request or no capture on this build"
        op, arm = held_op(c, src, rid)
        if op is None:
            return False, "no request landed inside a capture"
        d = op["gnt"] - arm
        lo, hi = (T_HOLD_MS - 1) * 1000, (T_HOLD_MS + 1) * 1000
        return lo <= d <= hi, f"held {d} cycles (bound {T_HOLD_MS} ms = {T_HOLD_MS * 1000})"
    return ck(f"hold_bounded:0x{rid:02x}" + ("" if src == "bfm" else f":{src}"), f)


def c_no_uncert_flash():
    def f(c):
        if not strobes(c, 0x8):
            return None, "no capture on this build"
        refused = [ln for ln in c.r.fw if "not attested" in ln]
        return bool(refused), f"refused captures reported: {len(refused)}"
    return ck("unattested_capture_never_flashed", f)


def c_slow_copy():
    def f(c):
        if not strobes(c, 0x8):
            return None, "no capture on this build"
        refused = [ln for ln in c.r.fw if "not attested" in ln]
        return not refused, f"refused captures {len(refused)}"
    return ck("slow_copy_attests", f)


def c_arm_refused(tag):
    def f(c):
        if "capid_before_stray" not in c.r.notes:
            return None, "hook not reached on this build"
        o = c.o(tag)
        st = o["stat"]
        before = c.r.notes["capid_before_stray"]["value"]
        ok = (st >> 21) & 1 and (st >> 16) & 1 and o["capid"] == before
        return bool(ok), f"arm_refused {(st >> 21) & 1} open {(st >> 16) & 1} id {before}->{o['capid']}"
    return ck(f"concurrent_arm_refused@{tag}", f)


def c_own_ack_ok():
    def f(c):
        refused = [ln for ln in c.r.fw if "REFUSED" in ln]
        return not refused, f"refused acknowledgements {len(refused)}"
    return ck("own_acknowledgements_accepted", f)


def c_stale_id_refused(tag):
    def f(c):
        if "open_capture_id" not in c.r.notes:
            return None, "hook not reached on this build"
        st = c.o(tag)["stat"]
        ok = (st >> 20) & 1 and (st >> 16) & 1 and (st >> 8) & 1
        return bool(ok), f"ack_refused {(st >> 20) & 1} capture open {(st >> 16) & 1} work owned {(st >> 8) & 1}"
    return ck(f"stale_identity_refused@{tag}", f)


def c_late_ack(tag):
    def f(c):
        o = c.o(tag)
        return c.dirty_img(tag) == 0 and o["backed"] == 0, f"committable work {c.dirty_img(tag)} backed {o['backed']}"
    return ck(f"late_ack_accepted_not_resurrecting@{tag}", f)


def c_refused_ack(tag):
    def f(c):
        if not strobes(c, 0x8):
            return None, "no capture on this build"
        refused = [ln for ln in c.r.fw if "REFUSED" in ln]
        return bool(refused) and c.dirty_img(tag) == 1, f"refusal reported {bool(refused)}, work still owned {c.dirty_img(tag)}"
    return ck(f"refused_ack_retires_nothing@{tag}", f)


def c_bits(tag, backed, dirty, stale):
    def f(c):
        o = c.o(tag)
        got = (o["backed"], o["dirty_pub"], o["stale"])
        return got == (backed, dirty, stale), f"(backed, dirty, stale) {got}"
    return ck(f"status@{tag}=({backed},{dirty},{stale})", f)


def c_unmaterialized(tag):
    def f(c):
        o = c.o(tag)
        live = o["dyn_fmt0_v"] == 1
        slot = c.rec(tag, 0x30)
        missing = live and (slot is None or erased(slot))
        claim = c.durable_claim(tag)
        return not (missing and claim), f"live format set {live}, record 0x30 in slot {'erased' if erased(slot) else slot}, durable claim {claim}"
    return ck(f"no_durable_claim_unmaterialized@{tag}", f)


def c_no_churn_pend(tag):
    def f(c):
        if not c.contract(tag):
            return None, "no pending state on this build"
        return c.o(tag)["erases"] == 0, f"erases {c.o(tag)['erases']}"
    return ck(f"pending_drives_no_commit@{tag}", f)


def c_failure_revokes(at_report):
    def f(c):
        hooks = [e for e in c.r.evts if e["k"] == "hook" and e["name"] == "w_stat"
                 and 11 <= (e["v"] & 0xF) <= 13]
        if not hooks:
            return False, "no failure was reported"
        rep = hooks[0]["cyc"]
        losses = [e["cyc"] for e in c.r.evts if e["k"] == "loss" and e["cyc"] >= rep]
        if at_report:
            if not c.contract():
                return None, "the tracked module revokes by the commit deadline"
            ok = bool(losses) and losses[0] - rep <= 5
        else:
            ok = bool(losses) and losses[0] - rep <= 10_000_000
        return ok, f"reported at {rep}, first loss {losses[0] - rep if losses else None} cycles later"
    return ck("failure_revokes_at_report" if at_report else "failure_revokes", f)


def c_producer_never_blocked():
    def f(c):
        ops = op_evts(c, "port")
        if not ops:
            return False, "no producer operation"
        worst = max(o["gnt"] - o["req"] for o in ops)
        return worst <= T_HOLD_MS * 1000 + 1000, f"longest request-to-grant wait {worst} cycles over {len(ops)} operations"
    return ck("producer_wait_bounded_by_hold", f)


def c_no_loss():
    def f(c):
        n = len([e for e in c.r.evts if e["k"] == "loss"])
        return n == 0, f"backed fell {n} time(s)"
    return ck("no_revocation_from_concurrent_update", f)


def c_hb_gap(limit_ms):
    def f(c):
        last = max(c.r.obs.values(), key=lambda o: o["cycle"])
        return last["hb_max_gap_ms"] <= limit_ms, f"largest heartbeat gap {last['hb_max_gap_ms']} ms"
    return ck(f"heartbeat_gap<={limit_ms}ms", f)


def c_stable(t0, t1):
    def f(c):
        e0, e1 = c.o(t0)["erases"], c.o(t1)["erases"]
        return e1 == e0 and c.dirty_img(t1) == 0, f"erases {e0}->{e1}"
    return ck("stable_no_churn", f)


def c_dirty_img(tag, want, label):
    def f(c):
        return c.dirty_img(tag) == want, f"committable work {c.dirty_img(tag)}"
    return ck(f"{label}@{tag}", f)


def c_attest_voided(tag):
    def f(c):
        if not c.contract(tag):
            return None, "no attestation on this build"
        st = c.o(tag)["stat"]
        held = c.r.notes.get("deferred_while_hold", {}).get("value", 1) == 0
        return (not (st >> 19) & 1) and held, f"attested {(st >> 19) & 1}, deferred during the hold {held}"
    return ck(f"grant_on_attest_edge_voids@{tag}", f)


def c_restore(tag, want):
    def f(c):
        pre = {p["sink"]: p for p in c.o(tag)["preloads"]}
        bad = []
        for sink, key in want.items():
            v = B[key]
            p = pre.get(sink)
            if key is None:
                continue
            if p is None or int(p["teid"], 16) != v[5] or p["uid"] != v[4] or \
                    int(p["ceid"], 16) != v[6] or p["started"] != v[2]:
                bad.append(f"sink {sink}: {p}")
        return not bad, f"restored {sorted(pre)}; mismatches {bad or 'none'}"
    return ck(f"restores_last_verified@{tag}", f)


def c_pend_bit():
    """PP_NVM_STAT[22] IS the pending bit the port publishes, at every
    observation of a build that carries the contract (revision b: one wire)."""
    def f(c):
        bad = [t for t, o in c.r.obs.items()
               if (o["stat"] >> 24) == TAG_C3 and ((o["stat"] >> 22) & 1) != o["pend"]]
        return not bad, f"observations where PP_NVM_STAT[22] differs from nvm_pend: {bad or 'none'}"
    return ck("pending_bit_is_status_bit_22", f)


# ---------------------------------------------------- revision b: the load
def all_strobes(c, bit):
    """Every strobe carrying `bit`, stray or not: the unit cases write theirs
    by hand, so they are all stray."""
    return [e["cyc"] for e in c.r.evts if e["k"] == "strobe" and e["v"] & bit]


def live_rec(c, tag, rid):
    """The record's bytes in the LIVE window at the observation."""
    raw = (c.r.outdir / f"{tag}-live.bin").read_bytes()
    off, ln = c.s.recs[rid]
    return raw[40 + off:40 + off + ln]


def own_bit(c, tag, rid):
    return (c.o(tag)["own"][rid >> 5] >> (rid & 31)) & 1


def show(b, key):
    return "expected " + key if b == F[key] else ("ERASED" if erased(b) else b.hex())


def c_every_slot(tag, rid, key):
    """EVERY slot that validates holds the record, not just the newest: what a
    power cycle at any later point could restore."""
    def f(c):
        got = []
        for letter in "AB":
            raw = (c.r.outdir / f"{tag}-slot{letter}.bin").read_bytes()
            n = struct.unpack_from("<I", raw, 16)[0] if raw[:4] != b"\xff" * 4 else 0
            blob = raw[:n] if 44 <= n <= 65536 else raw[:44]
            vd, _ = klj2_decode(blob, c.s.donor, c.s.ident, c.s.expect)
            if vd == VD_OK:
                off, ln = c.s.recs[rid]
                got.append(f"{letter}: {show(blob[40 + off:40 + off + ln], key)}")
        ok = bool(got) and all(g.endswith("expected " + key) for g in got)
        return ok, f"verified slots {got or 'none'}"
    return ck(f"every_verified_slot_keeps@{tag}:0x{rid:02x}", f)


def c_no_claim_over_erased_live(tag, rid):
    def f(c):
        live, claim = live_rec(c, tag, rid), c.durable_claim(tag)
        return not (erased(live) and claim), \
            f"live record 0x{rid:02x} erased {erased(live)}, status claims durable {claim}"
    return ck(f"no_durable_reading_over_erased_live@{tag}:0x{rid:02x}", f)


def c_reload_retried(tag):
    def f(c):
        if not c.contract(tag):
            return None, "no RELOAD on this build"
        st = c.o(tag)["stat"]
        said = any("refused 1 window load(s); accepted at attempt 2" in ln for ln in c.r.fw)
        return said and not (st >> 3) & 1, \
            f"one refusal then acceptance reported {said}, load pending {(st >> 3) & 1}"
    return ck(f"reload_refused_then_reloaded@{tag}", f)


def c_arm_edge_deferred(rid):
    """The ERASE was requested in the ARM's own cycle and granted only after
    the attestation: the hold covers the arm edge itself."""
    def f(c):
        if not c.contract("arm"):
            return None, "no arm on this build"
        arms, att = all_strobes(c, 0x8), all_strobes(c, 0x10)
        ops = [o for o in op_evts(c, "bfm", rid, 2) if arms and o["req"] == arms[-1]]
        if not arms or not att or not ops:
            return False, "no ERASE requested in the arm's own cycle"
        op, arm = ops[0], arms[-1]
        a = min([x for x in att if x > arm], default=None)
        ok = a is not None and op["gnt"] > a
        return ok, (f"ERASE requested in the arm's cycle, granted {op['gnt'] - arm} cycles after "
                    f"it, attestation at {a - arm if a is not None else None}")
    return ck(f"arm_edge_request_deferred:0x{rid:02x}", f)


def c_own_exact_after_arm(tag, rid):
    def f(c):
        if not c.contract(tag):
            return None, "no ownership vector on this build"
        busy, bit = c.o(tag)["dev_busy"], own_bit(c, tag, rid)
        return not (busy and not bit), \
            f"first cycle after the arm edge: dev_busy {busy}, record 0x{rid:02x} open {bit}"
    return ck(f"ownership_exact_after_arm@{tag}:0x{rid:02x}", f)


def c_attest_intact(tag, rid, key):
    def f(c):
        if not c.contract(tag):
            return None, "no attestation on this build"
        att, live = (c.o(tag)["stat"] >> 19) & 1, live_rec(c, tag, rid)
        return att == 1 and live == F[key], f"attested {att}, live record 0x{rid:02x} {show(live, key)}"
    return ck(f"attested_over_intact_record@{tag}:0x{rid:02x}", f)


def c_refused_open(tag, rid, label):
    """The RELOAD was refused and the record still reads open."""
    def f(c):
        if not c.contract(tag):
            return None, "no RELOAD on this build"
        ref, bit = (c.o(tag)["stat"] >> 11) & 1, own_bit(c, tag, rid)
        return ref == 1 and bit == 1, f"reload refused {ref}, record 0x{rid:02x} open {bit}"
    return ck(f"{label}@{tag}:0x{rid:02x}", f)


def c_closed_equals_load(tag, rid, key):
    """A record that reads closed holds exactly what the load wrote."""
    def f(c):
        if not c.contract(tag):
            return None, "no ownership vector on this build"
        bit, live = own_bit(c, tag, rid), live_rec(c, tag, rid)
        return bit == 1 or live == F[key], f"record 0x{rid:02x} open {bit}, live {show(live, key)}"
    return ck(f"closed_record_equals_load@{tag}:0x{rid:02x}", f)


def c_held_work(tag):
    def f(c):
        if not c.contract(tag):
            return None, "no RELOAD on this build"
        o = c.o(tag)
        ref = (o["stat"] >> 11) & 1
        ok = c.dirty_img(tag) == 1 and o["pend"] == 1 and ref == 1
        return ok, f"committable work {c.dirty_img(tag)}, pending {o['pend']}, reload refused {ref}"
    return ck(f"held_work_survives_post_boot_reload@{tag}", f)


RESET_ROW = {"open": (16, 0), "hold": (17, 0), "valid": (18, 0), "attested": (19, 0),
             "ack_refused": (20, 0), "arm_refused": (21, 0), "pend_bit": (22, 1),
             "committable": (8, 0), "img_cfg": (5, 0), "img_valid": (7, 0),
             "load_pending": (3, 1), "load_accepted": (2, 0), "reload_refused": (11, 0)}


def c_reset_row(tag):
    """The reset row of the capture machine: the page's table, bit by bit."""
    def f(c):
        if not c.contract(tag):
            return None, "no capture state on this build"
        o = c.o(tag)
        st = o["stat"]
        bad = {k: (st >> b) & 1 for k, (b, v) in RESET_ROW.items() if (st >> b) & 1 != v}
        for k, v in (("capid", 0), ("pend", 1), ("backed", 0), ("stale", 0)):
            if o[k] != v:
                bad[k] = o[k]
        own = sorted(w * 32 + b for w in range(8) for b in range(32) if (o["own"][w] >> b) & 1)
        every = own == sorted(c.s.recs)
        #! [2] load accepted is 0 in the row, and it is what refuses an ARM
        #! after reset: the image is not configured either, but the
        #! accepted-load term of section 5.3 rule 9 refuses one even after a
        #! writer configures and validates the window (issue #484)
        return not bad and every, (f"mismatches {bad or 'none'}; every allocated record open "
                                   f"{every} ({len(own)} of {len(c.s.recs)}); an ARM here is "
                                   f"refused by the accepted-load term, [2] = {(st >> 2) & 1}")
    return ck(f"reset_row@{tag}", f)


def c_early_ack(tag):
    def f(c):
        if not c.contract(tag):
            return None, "no capture state on this build"
        o = c.o(tag)
        st = o["stat"]
        ok = (st >> 20) & 1 and not (st >> 16) & 1 and o["capid"] == 0
        return bool(ok), f"ack refused {(st >> 20) & 1}, capture open {(st >> 16) & 1}, id {o['capid']}"
    return ck(f"pre_reset_ack_refused@{tag}", f)


def c_reattached(tag):
    def f(c):
        if not c.contract(tag):
            return None, "no restart model on this build"
        ref = (c.o(tag)["stat"] >> 11) & 1
        said = any("re-attached" in ln for ln in c.r.fw)
        ok = said and not ref and c.dirty_img(tag) == 1
        return ok, (f"re-attach reported {said}, reload refused {ref}, "
                    f"committable work kept {c.dirty_img(tag)}")
    return ck(f"restart_reattaches@{tag}", f)


def c_grant_wins_rebase(tag, rid):
    """Revision c: the mutating grant landed on the LAST re-base write's own
    edge, and the load flag stayed clear -- the RELOAD is refused and the
    record the ERASE blanked still reads open. Nothing was in flight at that
    edge, so only the priority between the two arms can refuse it."""
    def f(c):
        if not c.contract(tag):
            return None, "no RELOAD on this build"
        ops = op_evts(c, "bfm", rid, 2)
        rb = c.r.notes.get("rebase_cycle", {}).get("value")
        if not ops or rb is None:
            return False, "no ERASE and no recorded re-base cycle"
        # dev_gnt_o is REGISTERED: a grant decided on the edge that ends
        # cycle N (the edge the re-base write is applied on) is seen at N+1
        same = ops[0]["gnt"] == rb + 1
        ref, bit = (c.o(tag)["stat"] >> 11) & 1, own_bit(c, tag, rid)
        return same and ref == 1 and bit == 1, \
            (f"grant registered at {ops[0]['gnt']}, decided on the re-base write's own edge "
             f"{rb} ({same}), reload refused {ref}, record 0x{rid:02x} open {bit}")
    return ck(f"grant_wins_over_rebase_edge@{tag}:0x{rid:02x}", f)


def c_hold_bounded_chained(rid):
    """Revision c: a request deferred by one capture is granted at most
    T_HOLD_MS_P after it was raised, THOUGH a second arm followed the first
    capture's end in the adjacent cycle."""
    def f(c):
        ops, arms = op_evts(c, "bfm", rid, 2), all_strobes(c, 0x8)
        if not ops or len(arms) < 2:
            return None, "no chained captures on this build"
        op = ops[0]
        d = op["gnt"] - op["req"]
        return d <= (T_HOLD_MS + 1) * 1000, \
            (f"{len(arms)} arms, the second {arms[1] - arms[0]} cycles after the first; "
             f"request granted {d} cycles after it was raised (bound {(T_HOLD_MS + 1) * 1000})")
    return ck(f"hold_bounded_across_captures:0x{rid:02x}", f)


def c_arm_refused_while_deferred(tag):
    def f(c):
        if not c.contract(tag):
            return None, "no capture state on this build"
        st = c.o(tag)["stat"]
        ref, open_b = (st >> 21) & 1, (st >> 16) & 1
        return ref == 1 and open_b == 0, f"arm refused {ref}, capture open {open_b}"
    return ck(f"arm_refused_while_request_deferred@{tag}", f)


#: the terminal row of section 5.3, bit by bit: the bits the STATE fixes,
#: whatever the ordering that reached it (revision d adds [2] load accepted,
#: which is 0 in every one of them). nvm_backed, nvm_stale and the
#: committable bit are NOT here: they depend on whether the writer ever
#: heartbeated before it retired, and each row grades them itself.
#: The bits the STATE fixes (issue #484, the acceptance reviews' first two
#: corrections). [23] unres and [22] nvm_pend are NOT here: they read 1, 1 at
#: the boot and FALL once no record is open, which W4 reaches by rewriting
#: every record whole. [11] reload refused, [21] arm refused and [20] ack
#: refused are not here either: each is decided by whether the writer strobed
#: the thing it reports, not by the state, and a writer that retires before it
#: ever arms leaves [21] at 0. All five are graded where the ordering fixes
#: them, by the arguments of c_terminal_row.
TERMINAL_ROW = {"open": (16, 0), "hold": (17, 0), "attested": (19, 0),
                "cap_valid": (18, 0),
                "commit_busy": (10, 0), "img_cfg": (5, 1),
                "img_valid": (7, 0), "load_pending": (3, 0), "load_accepted": (2, 0)}


def c_terminal_row(tag, backed, dirty, stale, said_text, label,
                   ordering=(("unres", 23, 1), ("pend_bit", 22, 1),
                             ("reload_refused", 11, 1), ("arm_refused", 21, 0),
                             ("ack_refused", 20, 0))):
    """What a controller reads in the terminal state: the bits the state
    fixes, and the three the ordering decides. The saved state is NOT
    restored in that boot although a verified slot exists: img_valid 0 and
    the walk's fail and blank say so, the pending bit is 1, no window load
    was accepted ([2] 0) so nothing in this boot may be captured, and the
    boot load is over ([3] 0) so no later RELOAD can close a record over the
    live window."""
    def f(c):
        if not c.contract(tag):
            return None, "no window load on this build"
        o = c.o(tag)
        st = o["stat"]
        bad = {k: (st >> b) & 1 for k, (b, v) in TERMINAL_ROW.items() if (st >> b) & 1 != v}
        #! the bits the ORDERING decides, each with the value THIS ordering
        #! reaches: a lane that built its test from the fixed half alone would
        #! refuse a conforming implementation (issue #484)
        bad.update({k: (st >> b) & 1 for k, b, v in ordering if (st >> b) & 1 != v})
        for k, v in (("restore_done", 1), ("restore_fail", 1), ("blank", 1),
                     ("erases", 0), ("backed", backed), ("stale", stale)):
            if o[k] != v:
                bad[k] = o[k]
        if c.dirty_img(tag) != dirty:
            bad["committable"] = c.dirty_img(tag)
        said = any(said_text in ln for ln in c.r.fw)
        return not bad and said, (f"mismatches {bad or 'none'}, status 0x{st:08x}, "
                                  f"the writer reported it {said}")
    return ck(f"{label}@{tag}", f)


def c_arm_refused_no_load(tag):
    """REVISION D, the new term: no capture is armed until a RELOAD has been
    accepted since reset. The image is configured and the writer's own
    validity bit is set, so nothing but the backend's own flag can refuse
    this ARM; the identity does not advance, so no acknowledgement can ever
    quote the capture that was not opened."""
    def f(c):
        if not c.contract(tag):
            return None, "no capture state on this build"
        o = c.o(tag)
        st = o["stat"]
        acc, valid = (st >> 2) & 1, (st >> 7) & 1
        ref, open_b = (st >> 21) & 1, (st >> 16) & 1
        ok = acc == 0 and valid == 1 and ref == 1 and open_b == 0 and o["capid"] == 0
        return ok, (f"load accepted {acc}, img valid {valid}, arm refused {ref}, "
                    f"capture open {open_b}, capture identity {o['capid']}")
    return ck(f"arm_refused_without_accepted_load@{tag}", f)


def c_no_capture_no_load(tag):
    """And nothing the control face does afterwards retires anything: with
    no capture open an ATTEST and an ACK are refused, so the work a closed
    record holds is still reported and no reading is durable."""
    def f(c):
        if not c.contract(tag):
            return None, "no capture state on this build"
        o = c.o(tag)
        st = o["stat"]
        ok = (o["capid"] == 0 and (st >> 19) & 1 == 0 and (st >> 16) & 1 == 0
              and c.dirty_img(tag) == 1 and not c.durable_claim(tag))
        return ok, (f"capture identity {o['capid']}, attested {(st >> 19) & 1}, "
                    f"committable work {c.dirty_img(tag)}, status claims durable "
                    f"{c.durable_claim(tag)}")
    return ck(f"no_capture_without_accepted_load@{tag}", f)


def c_repeat_stops_when_live(tag, want):
    """REVISION D, the writer half: once the window has GONE LIVE (load
    pending 0 with no accepted load) no later RELOAD can be accepted, so the
    writer stops repeating instead of re-basing and refilling a window the
    producer owns."""
    def f(c):
        if not c.contract(tag):
            return None, "no window load on this build"
        st = c.o(tag)["stat"]
        strobed = len(all_strobes(c, 0x40))
        live = any("window then went live" in ln for ln in c.r.fw)
        ok = live and strobed == want and (st >> 3) & 1 == 0 and (st >> 2) & 1 == 0
        return ok, (f"window went live {live}, RELOAD strobes {strobed} (want {want}), "
                    f"load pending {(st >> 3) & 1}, load accepted {(st >> 2) & 1}")
    return ck(f"window_live_stops_the_repeat@{tag}", f)


def c_restart_stays_retired(tag):
    """REVISION D: a writer restarted in a boot whose window load was never
    accepted does NOT re-attach. It reads [2] and stays retired, so it
    publishes no validity bit over a window no load vouches for; and the
    backend's term refuses every ARM, so a writer that ignored the rule
    could capture nothing either."""
    def f(c):
        if not c.contract(tag):
            return None, "no restart model on this build"
        o = c.o(tag)
        st = o["stat"]
        said = any("stays retired" in ln for ln in c.r.fw)
        re_att = any("re-attached" in ln for ln in c.r.fw)
        ok = (said and not re_att and (st >> 2) & 1 == 0 and o["capid"] == 0
              and (st >> 16) & 1 == 0 and not c.durable_claim(tag))
        return ok, (f"stayed retired {said}, re-attached {re_att}, load accepted "
                    f"{(st >> 2) & 1}, capture identity {o['capid']}, capture open "
                    f"{(st >> 16) & 1}, status claims durable {c.durable_claim(tag)}")
    return ck(f"restart_stays_retired_without_load@{tag}", f)


def c_write_spans_fill(tag, rid):
    """The PREMISE of the re-review's probe H1, graded: a whole-record WRITE
    was granted before the last RELOAD strobe and ended with done after it,
    so the writer's own FILL wrote the record's bytes while that WRITE was
    streaming and the record now reads CLOSED over bytes the producer did
    not write. If the case fails to place that overlap it fails here rather
    than passing the checks below for the wrong reason."""
    def f(c):
        if not c.contract(tag):
            return None, "no window load on this build"
        ops = op_evts(c, "bfm", rid, 1)
        rl = all_strobes(c, 0x40)
        if not ops or not rl:
            return False, "no BFM WRITE, or no RELOAD strobe"
        op, last = ops[-1], rl[-1]
        bit = own_bit(c, tag, rid)
        ok = (op["gnt"] < last and op["end"] > last and "done" in op["res"] and bit == 0)
        return ok, (f"WRITE granted {op['gnt']}, last RELOAD strobe {last}, ended {op['end']} "
                    f"({op['res']}), record 0x{rid:02x} open {bit}")
    return ck(f"write_spans_refused_fill@{tag}:0x{rid:02x}", f)


def c_nothing_durable_when_closed(tag):
    """The re-review's probe H2: every record rewritten whole, so nothing is
    left open by accident and the pending bit falls. The reading is still
    not durable and no slot was touched, because a boot with no accepted
    load captured nothing.

    ITS OWN PREMISE IS GRADED (issue #484). The check says something about a
    state in which NOTHING IS OPEN; a run that left a record open would reach
    the same verdict for a reason the check is not about, and would pass
    vacuously. So "records open 0 and pending 0" is required, not reported."""
    def f(c):
        o = c.o(tag)
        nothing_open = (o["stat"] >> 23) & 1 == 0 and o["pend"] == 0
        ok = nothing_open and not c.durable_claim(tag) and o["erases"] == 0
        return ok, (f"records open {(o['stat'] >> 23) & 1}, pending {o['pend']}, backed "
                    f"{o['backed']}, committable {c.dirty_img(tag)}, status claims durable "
                    f"{c.durable_claim(tag)}, flash erases {o['erases']}, "
                    f"premise (nothing left open) {nothing_open}")
    return ck(f"no_durable_reading_when_nothing_open@{tag}", f)


def c_boot_load_closed(tag):
    """Revision c, the construction itself: once the window has gone live --
    the restore walk's first read, or an enabled producer -- the boot load is
    over, whether or not one was ever accepted."""
    def f(c):
        if not c.contract(tag):
            return None, "no window load on this build"
        st = c.o(tag)["stat"]
        return (st >> 3) & 1 == 0, f"load pending {(st >> 3) & 1}, reload refused {(st >> 11) & 1}"
    return ck(f"boot_load_closed_when_live@{tag}", f)


def c_writer_retired(tag):
    """A writer that has disabled itself for this reset answers the liveness
    deadline no more, so the state reads as a port with NO writer and never
    as a commit in flight."""
    def f(c):
        if not c.contract(tag):
            return None, "no window load on this build"
        o = c.o(tag)
        return o["backed"] == 0 and o["erases"] == 0, \
            f"backed {o['backed']}, pending {o['pend']}, flash erases {o['erases']}"
    return ck(f"writer_absent_when_retired@{tag}", f)


def c_landed_or_reported(tag, rid, key):
    """The change the producer accepted ends in a verified slot, or is still
    reported as owned; never a durable reading over work no slot holds."""
    def f(c):
        got = c.rec(tag, rid)
        in_slot = got == F[key]
        o = c.o(tag)
        reported = c.dirty_img(tag) == 1 or o["pend"] == 1
        claim = c.durable_claim(tag)
        return (in_slot or reported) and not claim, \
            (f"record 0x{rid:02x} in the newest verified slot {in_slot}, still reported "
             f"{reported}, status claims durable {claim}")
    return ck(f"change_landed_or_reported@{tag}:0x{rid:02x}", f)


def c_restart_takes_no_cold_boot(tag):
    """Revision c: a writer restarted over a live window never reloads it.
    No RELOAD is accepted after the restart (the boot load is over), the
    change stays in the window and stays owned."""
    def f(c):
        if not c.contract(tag):
            return None, "no restart model on this build"
        o = c.o(tag)
        st = o["stat"]
        cold = sum("refused 4 window loads" in ln for ln in c.r.fw) > 1
        said = any("re-attached" in ln or "stays disabled" in ln or "stays retired" in ln
                   for ln in c.r.fw)
        ok = said and not cold and (st >> 3) & 1 == 0 and c.dirty_img(tag) == 1
        return ok, (f"restart reported {said}, cold-boot path taken {cold}, load pending "
                    f"{(st >> 3) & 1}, committable work kept {c.dirty_img(tag)}")
    return ck(f"restart_never_reloads_live_window@{tag}", f)


def later(tag, rid, key):
    return c_rec(tag, rid, key, "later_record_persists")


def kept(tag, rid, key):
    return c_rec(tag, rid, key, "last_verified_kept")


CHECKS = {
    "A1_stable_no_change": [c_converged("end", {0x20: "X", 0x21: "Z"}), c_stable("base", "end")],
    "A2_write_between_verify_and_ack": [c_ack_only_slot("post_ack", 0x20, "X2"),
                                        c_converged("end", {0x20: "X2", 0x21: "Z"})],
    "A3_write_done_on_ack_edge": [c_ack_only_slot("post_ack", 0x20, "X2"),
                                  c_converged("end", {0x20: "X2", 0x21: "Z"})],
    "A4_write_after_ack": [c_converged("end", {0x20: "X2", 0x21: "Z"})],
    "A5_stray_duplicate_ack": [c_ack_only_slot("after_stray", 0x20, "X2"),
                               c_converged("end", {0x20: "X2", 0x21: "Z"})],
    "A6_late_ack_while_new_capture_open": [c_stale_id_refused("stray"),
                                           c_converged("end", {0x20: "X2", 0x21: "Z"})],
    "A8_identity_wrap": [c_ack_only_slot("end", 0x20, "X2")],
    "A9_updates_during_slow_erase": [c_converged("end", {0x20: "X3", 0x21: "Z"}), c_no_loss(),
                                     c_hb_gap(500)],
    "A11_inflight_write_closes_after_arm": [c_inflight_at_arm(0x21),
                                            c_rec("first", 0x21, "Z", "inflight_record_excluded"),
                                            c_converged("end", {0x20: "X2", 0x21: "Z2"})],
    "A12_last_byte_before_arm_done_after": [c_converged("end", {0x20: "X2", 0x21: "Z2"})],
    "B5_erase_then_no_write_yet": [kept("gap", 0x20, "X"), later("gap", 0x21, "Z2"),
                                   c_no_durable_claim("gap", {0x20: "X3"}),
                                   c_converged("end", {0x20: "X3", 0x21: "Z2"})],
    "B7_first_boot_erased_records": [c_first_boot_blank("blank_commit"),
                                     c_converged("end", {0x20: "X"})],
    "B8_first_boot_failed_erase": [later("end", 0x21, "Z"),
                                   ck("never_written_record_stays_erased@end:0x20",
                                      lambda c: (erased(c.rec("end", 0x20)), "record 0x20 erased"))],
    "B9_abandoned_write_stream": [later("abandoned", 0x20, "X2"), kept("abandoned", 0x21, "Z"),
                                  c_stuck_reported("abandoned"),
                                  c_converged("end", {0x20: "X2", 0x21: "Z2"})],
    "B10_partial_write_never_closes": [kept("end", 0x20, "X"), later("end", 0x21, "Z2")],
    "C1_request_during_hold_is_deferred": [c_deferred(0x21),
                                           c_converged("end", {0x20: "X2", 0x21: "Z2"})],
    "C2_hold_expiry_then_erase_with_stale_mask": [
        c_hold_bounded(0x21), c_no_uncert_flash(), kept("after", 0x21, "Z"),
        later("after", 0x20, "X2"), c_converged("end", {0x20: "X2", 0x21: "Z3"})],
    "C1r_real_port_request_deferred": [c_deferred(0x21, "port"),
                                       c_converged("end", {0x20: "X2", 0x21: "Z2"})],
    "C2r_real_port_torn_record_under_stale_mask": [
        c_hold_bounded(0x21, "port"), c_no_uncert_flash(),
        c_rec_in("after", 0x21, ["Z", "Z2"], "never_torn_or_erased"),
        later("after", 0x20, "X2"), c_converged("end", {0x20: "X2", 0x21: "Z2"})],
    "C2e_real_port_erased_span_under_stale_mask": [
        c_hold_bounded(0x21, "port"), c_no_uncert_flash(),
        c_rec_in("after", 0x21, ["Z", "Z2"], "never_torn_or_erased"),
        later("after", 0x20, "X2"), c_converged("end", {0x20: "X2", 0x21: "Z2"})],
    "C1a_real_port_arm_after_erase_done": [
        c_arm_in_gap(0x21), c_rec_in("after", 0x21, ["Z", "Z2"], "never_torn_or_erased"),
        later("after", 0x20, "X2"), c_converged("end", {0x20: "X2", 0x21: "Z2"})],
    "C1g_real_port_copy_inside_erase_write_gap": [
        c_copy_in_gap(0x21), c_rec_in("after", 0x21, ["Z", "Z2"], "never_torn_or_erased"),
        later("after", 0x20, "X2"), c_converged("end", {0x20: "X2", 0x21: "Z2"})],
    "C3_hold_expiry_without_producer": [c_slow_copy(), c_converged("end", {0x20: "X2", 0x21: "Z"})],
    "C5_concurrent_arm_refused": [c_arm_refused("stray"), c_own_ack_ok(),
                                  c_converged("end", {0x20: "X2", 0x21: "Z"})],
    "C7_late_ack_after_commit_deadline": [c_late_ack("pre_hb"), c_bits("end", 1, 0, 0),
                                          c_converged("end", {0x20: "X2", 0x21: "Z"})],
    "C8_ack_refused_after_verified_slot": [c_refused_ack("pre_hb"), c_rec("pre_hb", 0x20, "X2", "attested_slot_promoted"),
                                           c_converged("end", {0x20: "X2", 0x21: "Z"})],
    "D1_writer_loss_and_recovery": [c_bits("lost", 0, 0, 1), c_bits("back", 1, 0, 0),
                                    c_bits("lost2", 0, 1, 1), c_bits("end", 1, 0, 0),
                                    c_converged("end", {0x20: "X2", 0x21: "Z"})],
    "E1_dyn_change_ack_then_second_change": [c_unmaterialized("first"), c_unmaterialized("end"),
                                             c_no_churn_pend("end")],
    "E3_binding_inside_manager_debounce": [c_no_durable_claim("in_debounce", {0x20: "X2"}),
                                           c_converged("end", {0x20: "X2", 0x21: "Z"})],
    "F2_reported_flash_failure": [c_failure_revokes(False), c_failure_revokes(True),
                                  kept("failed", 0x20, "X"),
                                  ck("stale_until_good_commit@failed",
                                     lambda c: (c.o("failed")["stale"] == 1, f"stale {c.o('failed')['stale']}")),
                                  c_bits("end", 1, 0, 0), c_converged("end", {0x20: "X2", 0x21: "Z"})],
    "F3_flash_absent_producer_unblocked": [c_producer_never_blocked(), kept("end", 0x20, "X"),
                                           kept("end", 0x21, "Z"), c_dirty_img("end", 1, "work_still_owned"),
                                           ck("manager_flushed_everything@end",
                                              lambda c: (c.o("end")["mgr_dirty"] == 0, f"manager dirty {c.o('end')['mgr_dirty']}"))],
    "U1_post_reset_ack": [c_dirty_img("after", 1, "post_reset_ack_retires_nothing")],
    "U2_close_on_arm_edge": [c_dirty_img("acked", 1, "close_on_arm_edge_stays_live")],
    "U3_grant_on_attest_edge": [c_attest_voided("attest")],
    # revision b
    "U4_grant_request_on_arm_edge": [c_arm_edge_deferred(0x20), c_own_exact_after_arm("arm", 0x20),
                                     c_attest_intact("attest", 0x20, "X")],
    "U5_reload_refused_inflight_at_rebase": [
        c_refused_open("after", 0x20, "reload_refused_inflight_at_rebase"),
        c_closed_equals_load("after", 0x20, "X")],
    "U6_reload_refused_after_boot": [c_refused_open("gap", 0x21, "gap_record_stays_open"),
                                     c_refused_open("inflight", 0x21, "inflight_record_stays_open"),
                                     c_held_work("reload")],
    "U7_reset_row_and_pre_reset_ack": [c_reset_row("reset"), c_early_ack("early_ack"),
                                       c_dirty_img("after", 1, "post_reset_ack_retires_nothing")],
    "R1_reload_after_failed_erase": [c_reload_retried("boot"), kept("end", 0x20, "X"),
                                     c_every_slot("end", 0x20, "X"), later("end", 0x21, "Z2"),
                                     c_no_claim_over_erased_live("boot", 0x20),
                                     c_no_claim_over_erased_live("end", 0x20),
                                     c_converged("end", {0x20: "X", 0x21: "Z2"})],
    "W1_writer_restart_reattaches": [c_reattached("restarted"),
                                     c_no_durable_claim("restarted", {0x20: "X2"}),
                                     c_converged("end", {0x20: "X2", 0x21: "Z"})],
    # revision c
    "U8_grant_on_rebase_edge": [c_grant_wins_rebase("after", 0x20),
                                c_closed_equals_load("after", 0x20, "X")],
    "U10_arm_refused_while_request_deferred": [c_hold_bounded_chained(0x21),
                                               c_arm_refused_while_deferred("arm2")],
    "U9_four_window_loads_refused": [c_terminal_row("boot", 0, 0, 0, "refused 4 window loads",
                                                    "four_refusal_terminal_row"),
                                     c_boot_load_closed("boot"),
                                     c_writer_retired("end"),
                                     kept("end", 0x20, "X"), c_every_slot("end", 0x20, "X"),
                                     c_no_claim_over_erased_live("boot", 0x20),
                                     c_landed_or_reported("end", 0x21, "Z2")],
    # revision d: W2's expectation CHANGES. The restarted writer no longer
    # re-attaches and no longer commits what the window holds, so the
    # accepted change ends REPORTED beside the intact slot instead of in a
    # verified slot, and nothing in this boot reads durable.
    "W2_restart_after_refused_loads": [c_restart_takes_no_cold_boot("restarted"),
                                       c_restart_stays_retired("restarted"),
                                       c_no_claim_over_erased_live("restarted", 0x20),
                                       kept("end", 0x20, "X"), c_every_slot("end", 0x20, "X"),
                                       c_writer_retired("end"),
                                       c_landed_or_reported("end", 0x21, "Z2")],
    # revision d
    "U11_arm_refused_without_accepted_load": [c_arm_refused_no_load("stray"),
                                              c_no_capture_no_load("end")],
    "U12_window_live_stops_the_repeat": [c_repeat_stops_when_live("boot", 1),
                                         c_writer_retired("end"),
                                         kept("end", 0x20, "X"), c_every_slot("end", 0x20, "X"),
                                         c_landed_or_reported("end", 0x21, "Z2")],
    "U13_four_refusals_with_the_device_busy": [
        c_terminal_row("boot", 1, 1, 0, "refused 4 window loads", "terminal_row_writer_was_live"),
        c_terminal_row("end", 0, 1, 1, "refused 4 window loads", "terminal_row_after_the_loss"),
        kept("end", 0x20, "X"), c_every_slot("end", 0x20, "X"),
        c_landed_or_reported("end", 0x21, "Z")],
    "W3_write_across_refused_fill_then_restart": [c_write_spans_fill("live", 0x21),
                                                  c_restart_stays_retired("restarted"),
                                                  c_writer_retired("end"),
                                                  kept("end", 0x20, "X"),
                                                  c_every_slot("end", 0x20, "X"),
                                                  c_landed_or_reported("end", 0x21, "Z2")],
    "W4_all_records_rewritten_after_refused_fill": [c_write_spans_fill("live", 0x21),
                                                    c_restart_stays_retired("restarted"),
                                                    c_nothing_durable_when_closed("rewritten"),
                                                    c_nothing_durable_when_closed("end2"),
                                                    kept("end2", 0x20, "X"),
                                                    c_every_slot("end2", 0x20, "X")],
}
for name in ("B1_erase_error_full_span", "B2_erase_error_partial_span",
             "B3_erase_error_no_byte", "B4_write_error_after_erase"):
    CHECKS[name] = [kept("end", 0x20, "X"), later("end", 0x21, "Z2"),
                    c_no_durable_claim("end", {0x20: "X2", 0x21: "Z2"}),
                    c_alarm_revokes("gave_up"), c_alarm_revokes("end")]
for name in ("B6_two_failed_records_partial", "B6b_two_failed_records_full"):
    CHECKS[name] = [kept("end", 0x20, "X"), c_rec("end", 0x30, "FMT_A", "last_verified_kept"),
                    later("end", 0x21, "Z2"), c_unres_bits("end", [0x20, 0x30])]
for name in ("D4c_accepted_write_silent", "D4d_readiness_withheld", "D4e_silent_inside_capture"):
    CHECKS[name] = [later("stuck", 0x20, "X2"), kept("stuck", 0x21, "Z"), c_stuck_reported("stuck")]
POWER_CYCLE = {   # case -> the bindings a power cycle must restore
    "B1_erase_error_full_span": {0: "X", 1: "Z2"},
    "B2_erase_error_partial_span": {0: "X", 1: "Z2"},
    "B4_write_error_after_erase": {0: "X", 1: "Z2"},
    "B9_abandoned_write_stream": {0: "X2", 1: "Z2"},
}
#: cases a PRE-CONTRACT writer cannot express (they hook contract-3 strobes)
CONTRACT_ONLY = {"A6_late_ack_while_new_capture_open", "A8_identity_wrap",
                 "C1r_real_port_request_deferred", "C2r_real_port_torn_record_under_stale_mask",
                 "C2e_real_port_erased_span_under_stale_mask",
                 "C1a_real_port_arm_after_erase_done", "C1g_real_port_copy_inside_erase_write_gap",
                 "A11_inflight_write_closes_after_arm", "A12_last_byte_before_arm_done_after",
                 "C1_request_during_hold_is_deferred", "C2_hold_expiry_then_erase_with_stale_mask",
                 "C3_hold_expiry_without_producer", "C5_concurrent_arm_refused",
                 "C8_ack_refused_after_verified_slot", "D4e_silent_inside_capture",
                 "U2_close_on_arm_edge", "U3_grant_on_attest_edge",
                 "U4_grant_request_on_arm_edge", "U5_reload_refused_inflight_at_rebase",
                 "U6_reload_refused_after_boot", "U7_reset_row_and_pre_reset_ack",
                 "R1_reload_after_failed_erase", "W1_writer_restart_reattaches",
                 "U8_grant_on_rebase_edge", "U10_arm_refused_while_request_deferred",
                 "U9_four_window_loads_refused", "W2_restart_after_refused_loads",
                 "U11_arm_refused_without_accepted_load", "U12_window_live_stops_the_repeat",
                 "U13_four_refusals_with_the_device_busy",
                 "W3_write_across_refused_fill_then_restart",
                 "W4_all_records_rewritten_after_refused_fill"}
#: cases that run AFTER another case of the same build, on the slots it left
#: (the reviewers' RELOAD ordering starts from a verified slot A holding X)
DEPENDENT = {"R1_reload_after_failed_erase": "A1_stable_no_change",
             "U9_four_window_loads_refused": "A1_stable_no_change",
             "W2_restart_after_refused_loads": "A1_stable_no_change",
             "U12_window_live_stops_the_repeat": "A1_stable_no_change",
             "U13_four_refusals_with_the_device_busy": "A1_stable_no_change",
             "W3_write_across_refused_fill_then_restart": "A1_stable_no_change",
             "W4_all_records_rewritten_after_refused_fill": "A1_stable_no_change"}
#: the prototype's EXPECTED failures, each with its reason
PROTO_EXPECTED_FAIL = {
    ("E3_binding_inside_manager_debounce", "d1=0", "no_durable_claim@in_debounce"):
        "without donor scope D1 the parent cannot see a change the manager is debouncing",
}
#: checks the TRACKED build must fail: the #418 race, the ERASE-error
#: counterexample and the #420 one-pulse re-arm failure
PROD_MUST_FAIL = [
    ("A2_write_between_verify_and_ack", "ack_retires_only_slot@post_ack:0x20", "#418 ACK race"),
    ("B1_erase_error_full_span", "last_verified_kept@end:0x20", "round-1 ERASE-error counterexample"),
    ("E1_dyn_change_ack_then_second_change", "no_durable_claim_unmaterialized@end", "#420 one-pulse re-arm"),
]
CORE_8X8 = ["A2_write_between_verify_and_ack", "A3_write_done_on_ack_edge", "B1_erase_error_full_span",
            "B2_erase_error_partial_span", "B5_erase_then_no_write_yet", "B6_two_failed_records_partial",
            "B9_abandoned_write_stream", "C1_request_during_hold_is_deferred",
            "C2_hold_expiry_then_erase_with_stale_mask", "D1_writer_loss_and_recovery",
            "E1_dyn_change_ack_then_second_change",
            # revision b: the load, the arm edge and the reset row at the other shape
            "A1_stable_no_change", "R1_reload_after_failed_erase", "U4_grant_request_on_arm_edge",
            "U5_reload_refused_inflight_at_rebase", "U6_reload_refused_after_boot",
            "U7_reset_row_and_pre_reset_ack",
            # the boot that accepts no load, the writer restarts and the
            # record closed across a refused fill: each follows A1 on every
            # build that runs it, so the other shape gets them for free
            "U9_four_window_loads_refused", "U12_window_live_stops_the_repeat",
            "U13_four_refusals_with_the_device_busy",
            "W2_restart_after_refused_loads",
            "W3_write_across_refused_fill_then_restart",
            "W4_all_records_rewritten_after_refused_fill",
            # issue #484: the accepted-load term is shape-independent, and the
            # acceptance review asked for it to be shown so at the other shape
            "U11_arm_refused_without_accepted_load"]


PRODUCER = {'A11_inflight_write_closes_after_arm': 'real + bfm', 'A12_last_byte_before_arm_done_after': 'real + bfm', 'A1_stable_no_change': 'real', 'A2_write_between_verify_and_ack': 'real, #418', 'A3_write_done_on_ack_edge': 'bfm, #418 control', 'A4_write_after_ack': 'real', 'A5_stray_duplicate_ack': 'real + stray', 'A6_late_ack_while_new_capture_open': 'real + stray', 'A8_identity_wrap': 'real + stray', 'A9_updates_during_slow_erase': 'real', 'B10_partial_write_never_closes': 'real + bfm', 'B1_erase_error_full_span': 'real', 'B2_erase_error_partial_span': 'real', 'B3_erase_error_no_byte': 'real', 'B4_write_error_after_erase': 'real', 'B5_erase_then_no_write_yet': 'real + bfm', 'B6_two_failed_records_partial': 'real + bfm', 'B6b_two_failed_records_full': 'real + bfm', 'B7_first_boot_erased_records': 'real', 'B8_first_boot_failed_erase': 'real + bfm', 'B9_abandoned_write_stream': 'real + bfm', 'C1_request_during_hold_is_deferred': 'real + bfm', 'C1r_real_port_request_deferred': 'real', 'C2_hold_expiry_then_erase_with_stale_mask': 'real + bfm', 'C2r_real_port_torn_record_under_stale_mask': 'real', 'C3_hold_expiry_without_producer': 'real', 'C5_concurrent_arm_refused': 'real + stray', 'C7_late_ack_after_commit_deadline': 'real', 'C8_ack_refused_after_verified_slot': 'real + stray', 'D1_writer_loss_and_recovery': 'real', 'D4c_accepted_write_silent': 'real', 'D4d_readiness_withheld': 'real', 'D4e_silent_inside_capture': 'real', 'E1_dyn_change_ack_then_second_change': 'real dyn store', 'E3_binding_inside_manager_debounce': 'real', 'F2_reported_flash_failure': 'real', 'F3_flash_absent_producer_unblocked': 'real', 'U1_post_reset_ack': 'unit', 'U2_close_on_arm_edge': 'unit', 'U3_grant_on_attest_edge': 'unit', 'C2e_real_port_erased_span_under_stale_mask': 'real', 'C1a_real_port_arm_after_erase_done': 'real', 'C1g_real_port_copy_inside_erase_write_gap': 'real'}


PRODUCER.update({"U4_grant_request_on_arm_edge": "unit", "U5_reload_refused_inflight_at_rebase": "unit",
                 "U6_reload_refused_after_boot": "unit", "U7_reset_row_and_pre_reset_ack": "unit",
                 "R1_reload_after_failed_erase": "real + bfm, slots of A1",
                 "W1_writer_restart_reattaches": "real, writer restart model",
                 "U8_grant_on_rebase_edge": "unit",
                 "U10_arm_refused_while_request_deferred": "unit",
                 "U9_four_window_loads_refused": "real + bfm, slots of A1",
                 "W2_restart_after_refused_loads": "real + bfm, restart model, slots of A1",
                 "U11_arm_refused_without_accepted_load": "unit",
                 "U12_window_live_stops_the_repeat": "real + bfm, slots of A1",
                 "U13_four_refusals_with_the_device_busy": "real + bfm, slots of A1",
                 "W3_write_across_refused_fill_then_restart":
                     "real + bfm, restart model, slots of A1",
                 "W4_all_records_rewritten_after_refused_fill":
                     "real + bfm, restart model, slots of A1"})


def grade(run: Run, s: ShapeInfo) -> dict:
    """Every named check of one run: pass, fail, n/a (not expressible)."""
    c = Ctx(run, s)
    out = {}
    if run.exit != 0 or not run.done:
        return {"_harness": ("fail", f"exit {run.exit}, finished {run.done}")}
    if run.case.startswith("R_power_cycle"):
        base = run.variant.split("@")[0]
        return {n: ("pass" if ok else "fail", d) for n, (ok, d) in
                [(nm, f(c)) for nm, f in [c_restore("restored", POWER_CYCLE[base])]]}
    checks = list(CHECKS.get(run.case, [])) + [c_no_101(), c_pend_bit()]
    if run.pending:
        return {n: ("n/a", "the hook this case needs never fired on this build")
                for n, _ in checks}
    for name, fn in checks:
        try:
            ok, detail = fn(c)
        except KeyError as e:
            ok, detail = False, f"missing: {e}"
        out[name] = ("n/a" if ok is None else "pass" if ok else "fail", detail)
    return out


# -------------------------------------------------------------------- phases
#: Every mutant the contract page names, with the CHECK that must kill it.
#: A mutant whose named killer passes means that check is VACUOUS, and this
#: suite fails on it; a mutant that is killed only by some OTHER check is a
#: mutant aimed at the wrong place, and fails the same way.
MUTANTS = {
    # name: (which source, the case that runs it, its variant,
    #        and THE ONE CHECK the contract page names as its killer)
    'A01_composite_durable_bit':
        ('rtl', 'E1_dyn_change_ack_then_second_change', "", 'pending_drives_no_commit@end'),
    'F01_attestation_not_checked':
        ('fw', 'C2_hold_expiry_then_erase_with_stale_mask', "", 'last_verified_kept@after:0x21'),
    'F02_copies_open_records':
        ('fw', 'B1_erase_error_full_span', "", 'last_verified_kept@end:0x20'),
    'F03_prefill_from_blank':
        ('fw', 'B1_erase_error_full_span', "", 'last_verified_kept@end:0x20'),
    'F04_ack_without_identity':
        ('fw', 'A1_stable_no_change', "", 'stable_no_churn'),
    'F05_device_busy_gate_kept':
        ('fw', 'B9_abandoned_write_stream', "", 'later_record_persists@abandoned:0x20'),
    'F06_ack_after_failed_slot':
        ('fw', 'F2_reported_flash_failure', "", 'converged@end'),
    'F07_reload_refusal_ignored':
        ('fw', 'R1_reload_after_failed_erase', "", 'converged@end'),
    'F08_restart_reloads_window':
        ('fw', 'W1_writer_restart_reattaches', "", 'converged@end'),
    'F10_retired_writer_keeps_heartbeating':
        ('fw', 'U9_four_window_loads_refused', "", 'writer_absent_when_retired@end'),
    'F11_restart_reattaches_without_load':
        ('fw', 'W2_restart_after_refused_loads', "", 'restart_stays_retired_without_load@restarted'),
    'F12_repeat_ignores_window_live':
        ('fw', 'U12_window_live_stops_the_repeat', "", 'window_live_stops_the_repeat@boot'),
    'G01_edge_detected_change':
        ('glue', 'E1_dyn_change_ack_then_second_change', "", 'no_durable_claim_unmaterialized@end'),
    'M01_open_at_erase_completion':
        ('rtl', 'B1_erase_error_full_span', "", 'last_verified_kept@end:0x20'),
    'M02_close_on_any_completion':
        ('rtl', 'C1g_real_port_copy_inside_erase_write_gap', "", 'never_torn_or_erased@after:0x21'),
    'M03_close_on_partial_write':
        ('rtl', 'B10_partial_write_never_closes', "", 'later_record_persists@end:0x21'),
    'M04_ack_ignores_identity':
        ('rtl', 'A6_late_ack_while_new_capture_open', "", 'stale_identity_refused@stray'),
    'M05_ack_retires_live_work':
        ('rtl', 'A2_write_between_verify_and_ack', "", 'ack_retires_only_slot@post_ack:0x20'),
    'M06_hold_does_not_defer':
        ('rtl', 'C1_request_during_hold_is_deferred', "", 'deferred_until_attestation:0x21'),
    'M07_hold_never_expires':
        ('rtl', 'C2_hold_expiry_then_erase_with_stale_mask', "", 'hold_bounded:0x21'),
    'M08_attestation_ignores_grant':
        ('rtl', 'C2_hold_expiry_then_erase_with_stale_mask', "", 'last_verified_kept@after:0x21'),
    'M09_second_arm_accepted':
        ('rtl', 'C5_concurrent_arm_refused', "", 'concurrent_arm_refused@stray'),
    'M10_release_forgets_work':
        ('rtl', 'C2_hold_expiry_then_erase_with_stale_mask', "", 'later_record_persists@after:0x20'),
    'M11_dirty_from_accepted_bytes':
        ('rtl', 'A12_last_byte_before_arm_done_after', "", 'converged@end'),
    'M12_alarm_not_revoking':
        ('rtl', 'B1_erase_error_full_span', "", 'alarm_revokes@end'),
    'M13_report_not_revoking':
        ('rtl', 'F2_reported_flash_failure', "", 'failure_revokes'),
    'M14_pending_bit_misses_producer':
        ('rtl', 'E1_dyn_change_ack_then_second_change', "", 'no_durable_claim_unmaterialized@end'),
    'M15_pending_bit_misses_open_record':
        ('rtl', 'B5_erase_then_no_write_yet', "", 'no_durable_claim@gap'),
    'M17_hold_expiry_voids_capture':
        ('rtl', 'C3_hold_expiry_without_producer', "", 'slow_copy_attests'),
    'M18_pending_bit_stuck':
        ('rtl', 'A1_stable_no_change', "", 'converged@end'),
    'M19_arm_edge_grant_not_deferred':
        ('rtl', 'U4_grant_request_on_arm_edge', "", 'arm_edge_request_deferred:0x20'),
    'M20_arm_accepted_while_request_deferred':
        ('rtl', 'U10_arm_refused_while_request_deferred', "", 'hold_bounded_across_captures:0x21'),
    'R01_reload_ignores_inflight':
        ('rtl', 'U5_reload_refused_inflight_at_rebase', "", 'reload_refused_inflight_at_rebase@after:0x20'),
    'R02_reload_ignores_grant_since_rebase':
        ('rtl', 'R1_reload_after_failed_erase', "", 'last_verified_kept@end:0x20'),
    'R03_reload_not_once_per_reset':
        ('rtl', 'U6_reload_refused_after_boot', "", 'held_work_survives_post_boot_reload@reload'),
    'R04_rebase_wins_over_same_edge_grant':
        ('rtl', 'U8_grant_on_rebase_edge', "", 'grant_wins_over_rebase_edge@after:0x20'),
    'R05_boot_load_stays_pending_when_live':
        ('rtl', 'U9_four_window_loads_refused', "", 'boot_load_closed_when_live@boot'),
    'R06_revision_b_load_rule':
        ('rtl+fw', 'W2_restart_after_refused_loads', "", 'change_landed_or_reported@end:0x21'),
    'R07_arm_without_accepted_load':
        ('rtl', 'U11_arm_refused_without_accepted_load', "", 'arm_refused_without_accepted_load@stray'),
}
def one_shape_cases(shape: str, contract: bool) -> list[str]:
    if shape == "8x8":
        return list(CORE_8X8)
    cases = sorted(CHECKS)
    if not contract:
        cases = [c for c in cases if c not in CONTRACT_ONLY]
    return cases


def jobs_for(b: Build, shapes) -> list[tuple]:
    out = []
    for case in one_shape_cases(b.shape, b.contract):
        if case in DEPENDENT:
            continue
        if case == "E3_binding_inside_manager_debounce":
            out += [(b, case, f"d1={d}", ("--d1", d)) for d in ("0", "1")]
        else:
            out.append((b, case, "", ()))
    return out


def run_build(b: Build, shapes, pool: int, only: list[tuple] | None = None) -> list[Run]:
    jobsq = only if only is not None else jobs_for(b, shapes)
    with cf.ThreadPoolExecutor(max_workers=pool) as ex:
        runs = list(ex.map(lambda j: run_case(j[0], shapes, j[1], j[2], j[3]), jobsq))
    extra = [(b, "R_power_cycle", f"{r.case}@end",
              ("--slot-a", str(r.outdir / "end-slotA.bin"),
               "--slot-b", str(r.outdir / "end-slotB.bin")))
             for r in runs if r.case in POWER_CYCLE and "end" in r.obs]
    extra += [(b, dep, "",
               ("--slot-a", str(r.outdir / "end-slotA.bin"),
                "--slot-b", str(r.outdir / "end-slotB.bin")))
              for dep, parent in DEPENDENT.items() for r in runs
              if r.case == parent and "end" in r.obs
              and dep in one_shape_cases(b.shape, b.contract)]
    if extra:
        with cf.ThreadPoolExecutor(max_workers=pool) as ex:
            runs += list(ex.map(lambda j: run_case(j[0], shapes, j[1], j[2], j[3]), extra))
    return runs


def report(runs: list[Run], shapes, label: str, expect_fail: dict,
           control: bool = False) -> tuple[int, int, int]:
    """Print every graded check of a build and count what it did.

    On the CONTROL build -- a backend and a writer from before the contract --
    a failing check is the point: it is the defect the contract answers,
    reproduced on the source it was reported against. Those are printed as
    REPRODUCED and do not fail the suite; what fails the suite there is a
    check of PROD_MUST_FAIL that does NOT go red, which main() tests."""
    npass = nfail = nna = 0
    for r in sorted(runs, key=lambda x: (x.case, x.variant)):
        s = shapes[next(b.shape for b in ALL_BUILDS if b.name == r.build)]
        for name, (verdict, detail) in grade(r, s).items():
            key = (r.case, r.variant, name)
            if verdict == "fail" and key in expect_fail:
                print(f"  EXPECTED-FAIL {label} {r.case}{'~' + r.variant if r.variant else ''} "
                      f": {name} -- {expect_fail[key]}")
                npass += 1
                continue
            if verdict == "fail":
                print(f"  {'REPRODUCED' if control else 'FAIL'} {label} "
                      f"{r.case}{'~' + r.variant if r.variant else ''} "
                      f": {name} -- {detail}")
                nfail += 1
            elif verdict == "n/a":
                nna += 1
            else:
                npass += 1
    return npass, nfail, nna


ALL_BUILDS: list[Build] = []


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--shapes", default="1x1,8x8")
    ap.add_argument("--jobs", type=int, default=8)
    ap.add_argument("--pool", type=int, default=8)
    ap.add_argument("--skip-mutants", action="store_true",
                    help="grade the shipping builds only (a fast local loop)")
    ap.add_argument("--legacy-dir", default="",
                    help="a directory holding KL_nvm_backend.sv and milan_baremetal.c from "
                         "BEFORE the contract; with it the suite also runs the non-vacuity "
                         "control that must reproduce the three historical defects")
    a = ap.parse_args()
    global LEGACY_DIR
    LEGACY_DIR = Path(a.legacy_dir).resolve() if a.legacy_dir else None
    want = [s.strip() for s in a.shapes.split(",") if s.strip()]
    shapes = {n: shape(n) for n in want}

    builds = [Build(f"contract-{n}", n) for n in want]
    if "1x1" in want:
        # the identity-wrap control: a 2-bit identity MUST alias, which is
        # what shows the 16-bit one is doing work (A8)
        builds.append(Build("idw2-1x1", "1x1", cap_id_w=2))
    if LEGACY_DIR:
        builds.append(Build("legacy-1x1", "1x1", contract=False))
    if not a.skip_mutants:
        for m, (kind, _, _, _) in MUTANTS.items():
            kw = {f"{k}_mut": m for k in kind.split("+")}
            builds.append(Build(f"mut-{m}", "1x1", **kw))
    ALL_BUILDS.extend(builds)

    print(f"building {len(builds)} build(s)")
    with cf.ThreadPoolExecutor(max_workers=max(1, a.jobs // 2)) as ex:
        list(ex.map(lambda b: do_build(b, shapes, 2), builds))

    rc = 0
    totals = [0, 0, 0]
    for b in builds:
        if b.name.startswith("mut-") or b.name == "idw2-1x1":
            continue
        expect = {}
        if b.contract:
            expect = {("E3_binding_inside_manager_debounce", "d1=0",
                       "no_durable_claim@in_debounce"):
                      "KNOWN LIMITATION: without donor scope D1 (filed as "
                      "protocol-processor-control-plane-avb-milan issue 90) the parent "
                      "cannot see a binding the manager is debouncing"}
        runs = run_build(b, shapes, a.pool)
        p, f, n = report(runs, shapes, b.name, expect, control=not b.contract)
        if b.contract:
            totals = [totals[0] + p, totals[1] + f, totals[2] + n]
            #! NOT in a shape scripts/suite_tally.py counts: only the ONE
            #! closing line below is the suite's tally, or the per-build lines
            #! would be added to it and the sweep would quote a number two and
            #! a half times the checks this suite ran
            print(f"[{b.name}] {len(runs)} case run(s): {p} ok, {f} bad, "
                  f"{n} not expressible")
            if f:
                rc = 1
        else:
            print(f"[{b.name}] the pre-contract source reproduces {f} failing "
                  f"check(s) over {len(runs)} case run(s); {p} ok and {n} not "
                  f"expressible there (it has no arm, attestation or identity)")
        if not b.contract:
            # the non-vacuity control, in the other direction: the three
            # historical defects MUST reproduce on a pre-contract source
            graded = {(r.case, k): v for r in runs for k, v in grade(r, shapes[b.shape]).items()}
            for case, check, why in PROD_MUST_FAIL:
                got = graded.get((case, check), ("absent", ""))[0]
                if got != "fail":
                    print(f"  SELF-TEST FAILED: {case} : {check} reads {got} on the "
                          f"pre-contract source; it must FAIL there ({why}).")
                    rc = 1
                else:
                    print(f"  non-vacuity control: {case} : {check} RED as required -- {why}")

    if "1x1" in want and not a.skip_mutants:
        b = next(x for x in builds if x.name == "idw2-1x1")
        runs = run_build(b, shapes, a.pool,
                         only=[(b, "A8_identity_wrap", "", ())])
        v = grade(runs[0], shapes["1x1"]).get("ack_retires_only_slot@end:0x20", ("absent", ""))
        if v[0] != "fail":
            print(f"  SELF-TEST FAILED: a 2-bit capture identity reads {v[0]} on A8; it "
                  f"must alias and FAIL, or the 16-bit identity proves nothing.")
            rc = 1
        else:
            print("  identity control: a 2-bit identity aliases on A8 as required")

    killed = 0
    if not a.skip_mutants:
        print("---- mutants: each MUST be killed by its NAMED check ------------------")
        for m, (kind, case, variant, check) in MUTANTS.items():
            b = next(x for x in builds if x.name == f"mut-{m}")
            extra = ("--d1", variant.split("=")[1]) if variant.startswith("d1=") else ()
            todo = [(b, case, variant, extra)]
            if case in DEPENDENT:
                parent = DEPENDENT[case]
                runs = run_build(b, shapes, a.pool, only=[(b, parent, "", ())])
                r0 = runs[0]
                todo = [(b, case, variant,
                         ("--slot-a", str(r0.outdir / "end-slotA.bin"),
                          "--slot-b", str(r0.outdir / "end-slotB.bin")) + extra)]
            runs = run_build(b, shapes, a.pool, only=todo)
            #! run_build also runs the power-cycle and dependent follow-ups of
            #! whatever it ran, so the killer's own run is selected by NAME,
            #! never by position: taking the last would grade a follow-up and
            #! report every such mutant as surviving a check that never ran
            target = next(r for r in runs if r.case == case)
            g = grade(target, shapes["1x1"])
            got = g.get(check, ("absent", "the named check did not run"))
            if got[0] == "fail":
                killed += 1
                print(f"  {m}: killed by {check} -- {got[1]}")
            else:
                print(f"  SELF-TEST FAILED: {m} survives its named check {check} "
                      f"({got[0]}: {got[1]}). That check is vacuous.")
                rc = 1
        print(f"{killed} of {len(MUTANTS)} mutant(s) killed by their named check")

    #! THE suite tally, in the shape scripts/suite_tally.py reads first
    print(f"nvm_cosim: {totals[0] + totals[1]} checks: {totals[0]} PASS, "
          f"{totals[1]} FAIL ({totals[2]} not expressible)")
    print("RESULT: PASS" if rc == 0 else "RESULT: FAIL")
    return rc


LEGACY_DIR: Path | None = None

if __name__ == "__main__":
    raise SystemExit(main())
