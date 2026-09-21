#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Build, run and grade the D3 co-simulation (design evidence, milan-fpga #500).

What is REAL in every build: the pinned processor's KL_aecp_dyn_state and
KL_aecp_desc_store (424c688f), the shipping hdl/milan/KL_nvm_backend.sv and
the shipping writer sw/firmware/milan_baremetal/milan_baremetal.c compiled for
the host exactly as tb/verilator/nvm_cosim compiles it, with counted changes
(FW_SUBS, BOOT_NEW, FW_REPORT). AMENDED PROTOTYPES (revision c): the pinned
KL_pp_nvm_port and KL_acmp_nvm_shadow with declared amendments only
(AMENDMENTS; every action refuses a file that differs from its pinned source
by anything else). PROTOTYPE: KL_aecp_nvm_writer, KL_pp_nvm_mgr_arb and
KL_aecp_desc_mem_guard. The TRACKED build instantiates the PINNED port and
binding manager, as the parent ships them. MODEL: the uCPU (a bus-functional
model with the dispatch hold-off), the parent's map plane and the memories.

Every case is graded by NAMED checks over the journal the case binary prints,
with the repository's own scripts/nvm_klj2.py decoding every slot. Every
mutant is killed by EVERY check this file names for it, each in a run that
COMPLETED, or the run fails.

    run.py prep                 build the shape inputs (every shape)
    run.py build [NAME...]      build co-simulations (default: every build)
    run.py run   [NAME...]      run and grade. With no NAME it is the FULL run:
                                every build and every planned case must be
                                there, and it writes results.txt/results.json
                                beside this file. With NAMEs it is a FOCUSED
                                run: it says so, names its narrower coverage
                                and writes results-focused.* under $D3_OUT.
    run.py controls             the process-level negative controls: each
                                runs the real CLI on a doctored output tree
                                and requires its exit status and diagnostic
    run.py receipts             sha256 of every tracked evidence file and of
                                the repository files the model reads
    run.py amend                (re)write the amended prototypes from their
                                pinned sources and declared amendments; every
                                other action only checks them

Exit status: 0 no verdict failure; 1 verdict failures (each printed); 2 the
run was refused (a build or case missing, an empty selection).

Shapes: 1x1 and 8x8 are the SHIPPED configurations. 1x1r2 is a SYNTHETIC
test configuration, not a shipped one: the 1x1 configuration with its
AUDIO_UNIT listing a second sampling rate (clocking.audio_unit_rates_hz
[48000, 96000], which the builder accepts and marks planned), so a legal
non-default sampling rate can be saved and restored at all.

Outputs go under $D3_OUT (default /data/milan/tmp/500/d3). Nothing is written into the
repository tree except results.txt and results.json beside this file.
"""
from __future__ import annotations

import argparse
import concurrent.futures as cf
import dataclasses
import hashlib
import json
import os
import re
import shutil
import struct
import subprocess
import sys
import zlib
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
HARNESS = HERE / "harness"
PROTO = HERE / "prototype"
STUBS = HARNESS / "stubs"
OUT = Path(os.environ.get("D3_OUT", "/data/milan/tmp/500/d3"))

sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "sw" / "firmware" / "nvm_hosttest"))
import test_nvm_firmware as ref                                   # noqa: E402
from nvm_klj2 import (erased_record, frame_record, klj2_assemble,  # noqa: E402
                      klj2_decode, key_of_id, rid_of_key)
from nvm_shape import build as shape_build                        # noqa: E402
from check_nvm_record_space import expected_payloads              # noqa: E402

PP = ROOT / "protocol-processor" / "hdl"
#: the pinned processor modules every build compiles unchanged
DONOR_SV = [PP / "acmp/pp_acmp_pkg.sv", PP / "aecp/KL_aecp_dyn_state.sv",
            PP / "aecp/KL_aecp_desc_store.sv"]
#: the pinned port and binding manager: the TRACKED build's, unchanged
PINNED_PORT = PP / "packet_engine/KL_pp_nvm_port.sv"
PINNED_BIND = PP / "acmp/KL_acmp_nvm_shadow.sv"
BACKEND = ROOT / "hdl/milan/KL_nvm_backend.sv"
WRITER = ROOT / "sw/firmware/milan_baremetal/milan_baremetal.c"
SHAPES = {"1x1": "configs/endstation_ax7101_1x1_tdm8.yaml",
          "8x8": "configs/endstation_ax7101_8x8.yaml",
          "1x1r2": "configs/endstation_ax7101_1x1_tdm8.yaml"}
SHIPPED = ["1x1", "8x8"]
#: the synthetic shape: (the one line of the shipped config it replaces, its
#: replacement, the derived file's stem). Derived at prep time, never copied.
SYNTH = {"1x1r2": ("  audio_unit_rates_hz: [48000]\n", "  audio_unit_rates_hz: [48000, 96000]\n",
                   "endstation_ax7101_1x1_tdm8_r2")}
#: the D3 restore watchdog of d3_top (D3_RS_TMO_CYC_P), in model cycles
RS_TMO = 20000
FENCE_RW = "__asm__ volatile(\"fence rw, rw\" ::: \"memory\");"
FW_SUBS = [
    ("static inline uint32_t milan_read(unsigned int offset)\n{\n\treturn *milan_reg(offset);\n}",
     "static inline uint32_t milan_read(unsigned int offset)\n{\n\treturn nvm_host_csr_read(offset);\n}"),
    ("\t*milan_reg(offset) = value;\n\t__asm__ volatile(\"fence iorw, iorw\" ::: \"memory\");\n",
     "\tnvm_host_csr_write(offset, value);\n"),
]
#: THE ONE FIRMWARE CHANGE D3 NEEDS (page section 8.2): the entity model is
#: in DDR before the restore walk, so the walk can judge values against it
#: and write names back after the descriptor store has walked it
BOOT_OLD = ("\tnvm_boot();\n\taem_loaded = load_aem_image();\n\tentity_advertise(aem_loaded);\n")
BOOT_NEW = ("\taem_loaded = load_aem_image();\n\tnvm_boot();\n\tentity_advertise(aem_loaded);\n")
#: THE SECOND FIRMWARE CHANGE (page section 5.3): the enable is released by
#: the restore now (section 8.8), so the firmware's bounded wait REPORTS and
#: its enable line says what it did; neither decides anything
FW_REPORT = [
    ('\t\t\tprintf("Milan NVM: the restore walk did not sequence in time.\\n");\n',
     '\t\t\tprintf("Milan NVM: the restore has not reached its terminal; the fabric holds the entity enable until it does.\\n");\n'),
    ('\tprintf("Milan baremetal: fabric entity enabled; UART diagnostics ready.\\n");\n',
     '\tprintf("Milan baremetal: entity enable requested; the fabric releases it when the restore is done; UART diagnostics ready.\\n");\n'),
]


#: THE AMENDED PROTOTYPES (revision c): (pinned source, amended prototype,
#: the declared amendments). An amended file is EXACTLY its pinned source
#: with these (text that must occur once, its replacement) applied, which
#: check_amendments() proves before any build or run.
PORT_BANNER = """//  File        : KL_pp_nvm_port.amended.proto.sv
//                AMENDED PROTOTYPE (design evidence, milan-fpga #500, seam S1),
//                NOT the pinned RTL: the pinned KL_pp_nvm_port at
//                protocol-processor 424c688f with ONE amendment, the terminal
//                cause nvm_err_cause_o, and the module renamed
//                KL_pp_nvm_port_amd so the two cannot be confused. run.py
//                refuses to build unless this file is exactly the pinned one
//                with the amendments it declares (AMENDMENTS["port"]).
"""

AMENDMENTS = {
    "port": (PINNED_PORT, PROTO / "KL_pp_nvm_port.amended.proto.sv", [
        ("//  File        : KL_pp_nvm_port.sv\n", PORT_BANNER),
        ("module KL_pp_nvm_port #(\n", "module KL_pp_nvm_port_amd #(\n"),
        ("\n    //! ---- device face (initiator toward the side-port backend, 02 §8-free) ----\n",
         "\n    //! AMENDMENT (#500 S1): the terminal cause, valid with nvm_err_o and 0\n"
         "    //! otherwise. 1 DEVICE: the device reported an error in any state, or\n"
         "    //! ended the header read short. 2 UNFRAMED: the device COMPLETED the\n"
         "    //! 8-byte header read and the header failed the magic or length gate\n"
         "    //! (restore), or the manager's own commit header failed it. 3 is\n"
         "    //! reserved for a deadline (processor issue 15), never produced here.\n"
         "    output logic [1:0]  nvm_err_cause_o,\n"
         "\n    //! ---- device face (initiator toward the side-port backend, 02 §8-free) ----\n"),
        ("  // ---- manager face outputs ----------------------------------------------\n",
         "  // ---- AMENDMENT (#500 S1): the terminal cause ---------------------------\n"
         "  //! UNFRAMED only where the FSM itself refuses a header the device\n"
         "  //! delivered whole (S_RHWAIT: done, no err, !hdr_ok_w) or the manager\n"
         "  //! streamed (S_WHDR's eighth byte, !hdr_ok_w). Every other err is\n"
         "  //! DEVICE. The cause is held through S_FIN, the cycle nvm_err_o pulses.\n"
         "  localparam logic [1:0] CAUSE_DEVICE_C   = 2'd1;\n"
         "  localparam logic [1:0] CAUSE_UNFRAMED_C = 2'd2;\n"
         "  logic [1:0] cause_r;\n"
         "\n"
         "  always_ff @(posedge clk_i) begin : nvm_port_cause\n"
         "    if (!rst_n) begin\n"
         "      cause_r <= 2'd0;\n"
         "    end else if (((state_r == S_RHWAIT) && !dev_err_i && (dev_done_i || done_seen_r)\n"
         "                  && !hdr_ok_w)\n"
         "                 || ((state_r == S_WHDR) && nvm_wvalid_i && (hidx_r == 3'd7)\n"
         "                     && !hdr_ok_w)) begin\n"
         "      cause_r <= CAUSE_UNFRAMED_C;\n"
         "    end else if ((state_r != S_FIN) && (state_r != S_IDLE)) begin\n"
         "      cause_r <= CAUSE_DEVICE_C;\n"
         "    end\n"
         "  end\n"
         "  assign nvm_err_cause_o = nvm_err_o ? cause_r : 2'd0;\n"
         "\n"
         "  // ---- manager face outputs ----------------------------------------------\n"),
    ]),
    "bind": (PINNED_BIND, PROTO / "KL_acmp_nvm_shadow.amended.proto.sv", [
        ("//  File        : KL_acmp_nvm_shadow.sv\n",
         "//  File        : KL_acmp_nvm_shadow.amended.proto.sv\n"
         "//                AMENDED PROTOTYPE (design evidence, milan-fpga #500, seams\n"
         "//                S1 and S3), NOT the pinned RTL: the pinned KL_acmp_nvm_shadow\n"
         "//                at protocol-processor 424c688f with TWO amendments, and the\n"
         "//                module renamed KL_acmp_nvm_shadow_amd. S1: a zero-byte err\n"
         "//                is an empty record only when the port's cause says UNFRAMED;\n"
         "//                a zero-byte DEVICE error fails the whole walk (processor\n"
         "//                issue 20). S3: the READ phase of the restore walk has a\n"
         "//                no-progress deadline, RS_TMO_CYC_P; its expiry fails the\n"
         "//                whole walk and abandons an issued read to the arbiter's\n"
         "//                drain (nvm_abort_o). run.py refuses to build unless this file\n"
         "//                is exactly the pinned one with the amendments it declares\n"
         "//                (AMENDMENTS[\"bind\"]).\n"),
        ("module KL_acmp_nvm_shadow\n", "module KL_acmp_nvm_shadow_amd\n"),
        ("    parameter int unsigned RETRY_MAX_P   = 2,\n",
         "    parameter int unsigned RETRY_MAX_P   = 2,\n"
         "    //! AMENDMENT (#500 S3): the restore walk's no-progress deadline, in\n"
         "    //! clocks. Every READ-phase wait on the port ends within it.\n"
         "    parameter int unsigned RS_TMO_CYC_P  = 20000,\n"),
        ("    input  wire                        nvm_err_i,      //! one-cycle pulse: op failed\n",
         "    input  wire                        nvm_err_i,      //! one-cycle pulse: op failed\n"
         "    //! AMENDMENT (#500 S1): the port's terminal cause with nvm_err_i\n"
         "    //! (KL_pp_nvm_port_amd): 1 DEVICE, 2 UNFRAMED\n"
         "    input  wire  [1:0]                 nvm_err_cause_i,\n"
         "    //! AMENDMENT (#500 S3): the walk abandons the read the port is\n"
         "    //! serving (its deadline expired); the arbiter drains it\n"
         "    output logic                       nvm_abort_o,\n"
         "    //! AMENDMENT (#500 S3): why the walk failed: 0 none, 1 torn, 2 a\n"
         "    //! device error with nothing forwarded, 3 the deadline\n"
         "    output logic [1:0]                 restore_cause_o,\n"),
        ("  // ---- restore stream terminal events ------------------------------------\n",
         "  // ---- AMENDMENT (#500 S3): the restore walk's deadline -------------------\n"
         "  //! Consecutive cycles of the READ phase that wait on the port\n"
         "  //! (H_RS_REQ: the port idle; H_RS_STREAM: a byte, done or err) without\n"
         "  //! that event. Expiry ends the WHOLE walk as a failed one, as a torn\n"
         "  //! read does (fail, done, no preload, every uncaptured sink at its\n"
         "  //! vendor default), and abandons an issued read to the arbiter's drain\n"
         "  //! (nvm_abort_o). The preload phase waits on the on-chip listener and\n"
         "  //! is not watched here.\n"
         "  logic [31:0] rs_wd_r;\n"
         "  logic        rs_stall_w, rs_tmo_w;\n"
         "\n"
         "  assign rs_stall_w = ((hs_r == H_RS_REQ) && (nvm_busy_i || nvm_done_i || nvm_err_i))\n"
         "                    || ((hs_r == H_RS_STREAM) && !nvm_rvalid_i && !nvm_done_i && !nvm_err_i);\n"
         "  assign rs_tmo_w    = rs_stall_w && (rs_wd_r >= 32'(RS_TMO_CYC_P - 1));\n"
         "  assign nvm_abort_o = rs_tmo_w && (hs_r == H_RS_STREAM);\n"
         "\n"
         "  always_ff @(posedge clk_i) begin : rs_wd_ff\n"
         "    if (!rst_n)          rs_wd_r <= 32'd0;\n"
         "    else if (rs_stall_w) rs_wd_r <= rs_wd_r + 32'd1;\n"
         "    else                 rs_wd_r <= 32'd0;\n"
         "  end\n"
         "\n"
         "  // ---- restore stream terminal events ------------------------------------\n"),
        ("  assign rs_torn_w = (hs_r == H_RS_STREAM)\n"
         "                   && ((nvm_err_i && (rbcnt_r != 17'd0))\n"
         "                       || (nvm_done_i && (rbcnt_r != 17'd0)\n"
         "                           && ((rbcnt_r < 17'd8) || (rbcnt_r != rexp_total_w))));\n"
         "  assign rs_empty_w = (hs_r == H_RS_STREAM)\n"
         "                    && ((nvm_err_i && (rbcnt_r == 17'd0))\n"
         "                        || (nvm_done_i && (rbcnt_r == 17'd0)));\n",
         "  //! AMENDMENT (#500 S1, S3): a zero-byte err is an empty record ONLY\n"
         "  //! when the port says the device answered with a header that is not a\n"
         "  //! record (UNFRAMED); a zero-byte DEVICE error, and the deadline, fail\n"
         "  //! the whole walk as a torn read does\n"
         "  logic rs_dev0_w;\n"
         "  assign rs_dev0_w = (hs_r == H_RS_STREAM) && nvm_err_i && (rbcnt_r == 17'd0)\n"
         "                   && (nvm_err_cause_i != 2'd2);\n"
         "  assign rs_torn_w = ((hs_r == H_RS_STREAM)\n"
         "                      && ((nvm_err_i && (rbcnt_r != 17'd0))\n"
         "                          || (nvm_done_i && (rbcnt_r != 17'd0)\n"
         "                              && ((rbcnt_r < 17'd8) || (rbcnt_r != rexp_total_w)))))\n"
         "                   || rs_dev0_w || rs_tmo_w;\n"
         "  assign rs_empty_w = (hs_r == H_RS_STREAM)\n"
         "                    && ((nvm_err_i && (rbcnt_r == 17'd0) && (nvm_err_cause_i == 2'd2))\n"
         "                        || (nvm_done_i && (rbcnt_r == 17'd0)));\n"),
        ("  // ---- flush terminal events ----------------------------------------------\n",
         "  // ---- AMENDMENT (#500 S3): why the walk failed ---------------------------\n"
         "  logic [1:0] rs_cause_r;\n"
         "  always_ff @(posedge clk_i) begin : rs_cause_ff\n"
         "    if (!rst_n)                                 rs_cause_r <= 2'd0;\n"
         "    else if (go_take_w)                         rs_cause_r <= 2'd0;\n"
         "    else if (rs_torn_w && (rs_cause_r == 2'd0)) rs_cause_r <= rs_tmo_w ? 2'd3\n"
         "                                                              : (rs_dev0_w ? 2'd2 : 2'd1);\n"
         "  end\n"
         "  assign restore_cause_o = rs_cause_r;\n"
         "\n"
         "  // ---- flush terminal events ----------------------------------------------\n"),
        ("        H_RS_REQ: begin\n"
         "          if (!nvm_busy_i && !nvm_done_i && !nvm_err_i) begin\n",
         "        H_RS_REQ: begin\n"
         "          if (rs_tmo_w) begin\n"
         "            // AMENDMENT (#500 S3): the deadline expired waiting for the port\n"
         "            fail_r    <= 1'b1;\n"
         "            done_r    <= 1'b1;\n"
         "            any_rec_r <= 1'b0;\n"
         "            hs_r      <= H_RUN;\n"
         "          end else if (!nvm_busy_i && !nvm_done_i && !nvm_err_i) begin\n"),
    ]),
}



def amended_text(key: str) -> str:
    pinned, _amended, seam_list = AMENDMENTS[key]
    text = pinned.read_text()
    for old, new in seam_list:
        if text.count(old) != 1:
            raise SystemExit(f"amendment {key}: seam count {text.count(old)}: {old[:60]!r}")
        text = text.replace(old, new)
    return text


def check_amendments() -> None:
    """Refuse to go on if an amended prototype is anything but its pinned
    source with the declared amendments."""
    for key, (pinned, amended, _s) in AMENDMENTS.items():
        if amended.read_text() != amended_text(key):
            raise SystemExit(f"REFUSED: {amended.name} is not {pinned.name} with AMENDMENTS[{key!r}] only; "
                             f"run.py amend rewrites it")


def cmd(argv: list, log: Path, cwd: Path = ROOT) -> subprocess.CompletedProcess:
    """Run one build step, log it, refuse on a non-zero exit."""
    log.parent.mkdir(parents=True, exist_ok=True)
    p = subprocess.run([str(a) for a in argv], cwd=cwd, text=True, capture_output=True,
                       env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"})
    log.write_text(p.stdout + p.stderr)
    if p.returncode:
        raise SystemExit(f"FAILED ({p.returncode}): {' '.join(map(str, argv))}\n  see {log}")
    return p


# ---------------------------------------------------------------- the shapes
@dataclasses.dataclass
class Shape:
    name: str
    work: Path
    table: Path
    facts: Path
    aem: Path
    header: str
    params: dict
    recs: dict            # rid -> (off, flen, plen, group, index)
    donor: object
    ident: object
    expect: dict
    img_len: int
    def_fmt_in: list
    def_fmt_out: list
    rates: list
    clk_count: int
    names: list


def parse_aemi(img: bytes, dc: dict) -> dict:
    """The facts a case needs, read out of the shape's own AEMI image: the
    header and index map as KL_aecp_desc_store walks them (its banner), then
    the descriptors at the offsets avdecc/aem_descriptors.py emits."""
    magic, ver, n_config = struct.unpack_from(">IHH", img, 0)
    if magic != 0x41454D49:
        raise SystemExit("not an AEMI image")
    n_entries, n_names, index_off = struct.unpack_from(">HHI", img, 8)
    names_off, _image_bytes = struct.unpack_from(">II", img, 16)
    entries = [struct.unpack_from(">HHHHIHH", img, index_off + 16 * e) for e in range(n_entries)]

    def desc(dtype: int, index: int) -> bytes:
        base = 0
        for cfg, t, count, elen, eoff, _nb, stride in entries:
            if cfg != 0 or t != dtype:
                continue
            if base <= index < base + count:
                o = eoff + stride * (index - base)
                return img[o:o + elen]
            base += count
        raise SystemExit(f"descriptor {dtype:#x}[{index}] not in the image")

    fmt_in = [int.from_bytes(desc(0x0005, i)[74:82], "big") for i in range(dc["STREAM_INPUT"])]
    fmt_out = [int.from_bytes(desc(0x0006, i)[74:82], "big") for i in range(dc["STREAM_OUTPUT"])]
    au = desc(0x0002, 0)
    rates = [int.from_bytes(au[144 + 4 * k:148 + 4 * k], "big")
             for k in range(int.from_bytes(au[142:144], "big"))]
    cd = desc(0x0024, 0)
    clk = int.from_bytes(cd[74:76], "big")
    names = [img[names_off + 64 * k:names_off + 64 * (k + 1)] for k in range(n_names)]
    return dict(n_config=n_config, n_entries=n_entries, n_names=n_names, fmt_in=fmt_in,
                fmt_out=fmt_out, rates=rates, clk_count=clk, names=names, version=ver)


def prep_shape(name: str) -> Shape:
    cfg = ROOT / SHAPES[name]
    work = OUT / f"shape-{name}"
    work.mkdir(parents=True, exist_ok=True)
    if name in SYNTH:
        old, new, stem = SYNTH[name]
        text = cfg.read_text()
        if text.count(old) != 1:
            raise SystemExit(f"{name}: the line it replaces occurs {text.count(old)} times in {cfg}")
        (work / "cfg").mkdir(exist_ok=True)
        cfg = work / "cfg" / f"{stem}.yaml"
        cfg.write_text(text.replace(old, new))
    names, dc, spi, spo = shape_build(cfg, work / "builder")
    shp = ref.Shape(cfg=cfg, names=names, dc=dc, spi=spi, spo=spo)
    donor = ref.Donor(base=ref.binding_base(), layout=ref.layout_version())
    overlay = json.loads((work / "builder" / cfg.stem / "aem_overlay.json").read_text())
    ident = ref.Ident(seq=0, entity_id=int(overlay["adp"]["entity_id"], 16),
                      model_id=int(overlay["entity"]["entity_model_id"], 16))
    aem = work / "builder" / f"{cfg.stem}.img.bin"
    img = aem.read_bytes()
    facts = parse_aemi(img, dc)
    if facts["n_names"] != names:
        raise SystemExit(f"{name}: the AEMI header carries {facts['n_names']} names, the builder {names}")
    table = work / "records.txt"
    cmd([sys.executable, "-B", "scripts/check_nvm_record_space.py", "--emit-record-table",
         cfg, "-o", table], work / "record-table.log")
    recs, img_len = {}, 0
    for ln in table.read_text().splitlines():
        f = ln.split()
        if f and f[0] == "imglen":
            img_len = int(f[1])
        if f and f[0] == "rec":
            recs[int(f[1], 16)] = (int(f[2]), int(f[3]), int(f[4]), f[5], int(f[6]))
    header = ref.constants_header(shp, donor, ident)
    header = re.sub(r"#define MILAN_AEM_IMAGE_BYTES \d+u", f"#define MILAN_AEM_IMAGE_BYTES {len(img)}u", header)
    header = re.sub(r"#define MILAN_AEM_IMAGE_CRC32 \d+u",
                    f"#define MILAN_AEM_IMAGE_CRC32 {zlib.crc32(img) & 0xFFFFFFFF}u", header)
    ids = sorted(recs)
    cls_in = [recs[r][2] // 8 for r in ids if 0x60 <= r < 0x70]
    cls_out = [recs[r][2] // 8 for r in ids if 0x70 <= r < 0x80]
    count = lambda lo, hi: sum(1 for r in ids if lo <= r < hi)   # noqa: E731
    params = dict(N_STREAM_IN_P=count(0x30, 0x40), N_STREAM_OUT_P=count(0x40, 0x50),
                  N_SPORT_IN_P=len(cls_in), N_SPORT_OUT_P=len(cls_out),
                  N_AUDIO_UNIT_P=count(0x02, 0x0A), N_CLK_DOM_P=count(0x0A, 0x12),
                  N_NAME_P=count(0x80, 0x100))
    params["MAPI_CLS_P"] = f"{8 * len(cls_in)}'d{sum(c << (8 * i) for i, c in enumerate(cls_in))}"
    params["MAPO_CLS_P"] = f"{8 * len(cls_out)}'d{sum(c << (8 * i) for i, c in enumerate(cls_out))}"
    params["MAP_ENT_MAX_P"] = max(cls_in + cls_out + [1])
    params["IDX_ENTRIES_P"] = 32 if facts["n_entries"] <= 32 else 64
    lines = [f"fmt_in {f:016x}" for f in facts["fmt_in"]]
    lines += [f"fmt_out {f:016x}" for f in facts["fmt_out"]]
    lines += [f"rate {r:08x}" for r in facts["rates"]]
    lines += [f"clk_count {facts['clk_count']}", f"n_cfg {facts['n_config']}"]
    (work / "facts.txt").write_text("\n".join(lines) + "\n")
    return Shape(name, work, table, work / "facts.txt", aem, header, params, recs, donor, ident,
                 expected_payloads(shp), img_len, facts["fmt_in"], facts["fmt_out"],
                 facts["rates"], facts["clk_count"], facts["names"])


# ------------------------------------------------------------------- builds
@dataclasses.dataclass
class Build:
    name: str
    shape: str
    mut: str = ""
    fw_old_boot: bool = False
    tracked: bool = False
    binary: Path | None = None


#: every source a mutation may name: its key, the tracked file and the name
#: its (possibly mutated) copy takes in the build tree (the module's name)
SOURCES = {
    "writer": (PROTO / "KL_aecp_nvm_writer.proto.sv", "KL_aecp_nvm_writer.sv"),
    "arb": (PROTO / "KL_pp_nvm_mgr_arb.proto.sv", "KL_pp_nvm_mgr_arb.sv"),
    "guard": (PROTO / "KL_aecp_desc_mem_guard.proto.sv", "KL_aecp_desc_mem_guard.sv"),
    "port": (PROTO / "KL_pp_nvm_port.amended.proto.sv", "KL_pp_nvm_port_amd.sv"),
    "bind": (PROTO / "KL_acmp_nvm_shadow.amended.proto.sv", "KL_acmp_nvm_shadow_amd.sv"),
    "top": (HARNESS / "d3_top.sv", "d3_top.sv"),
}


#: every mutation: (file key, the text that must occur exactly once, its
#: replacement). A mutation whose seam moved stops the build.
MUTATIONS = {
    "M01_taint_ignored": ("writer",
        "  assign fl_done_ok_w = (st_r == F_WAIT) && m_done_i && !taint_r;",
        "  assign fl_done_ok_w = (st_r == F_WAIT) && m_done_i;"),
    "M02_clear_at_latch": ("writer",
        "  assign fl_done_ok_w = (st_r == F_WAIT) && m_done_i && !taint_r;",
        "  assign fl_done_ok_w = (st_r == F_REL) && !taint_r;"),
    "M03_clear_wins_same_edge": ("writer",
        "      else if (set_w[gs]) dirty_r[gs] <= 1'b1;\n      else if (clr_w[gs]) dirty_r[gs] <= 1'b0;",
        "      else if (clr_w[gs]) dirty_r[gs] <= 1'b0;\n      else if (set_w[gs]) dirty_r[gs] <= 1'b1;"),
    "M04_clear_by_group": ("writer",
        "    assign clr_w[gs] = clr_en_w && (cg_r == grp_f(SW_C'(gs)))\n"
        "                     && (ci_r[7:0] == 8'(gs - base_f(grp_f(SW_C'(gs)))));",
        "    assign clr_w[gs] = clr_en_w && (cg_r == grp_f(SW_C'(gs)));"),
    "M05_latch_ignores_program": ("writer",
        "          if (!prog_busy_i) begin\n            own_r <= 1'b1; ptr_r <= '0;",
        "          if (1'b1) begin\n            own_r <= 1'b1; ptr_r <= '0;"),
    "M06_identify_is_a_change": ("writer",
        "  assign set_w[S_CFG_C] = dyn_w && (u_sel_w == 13'd0) && (u_didx_i == 16'd0);",
        "  assign set_w[S_CFG_C] = dyn_w && ((u_sel_w == 13'd0) || (u_sel_w == 13'd7)) && (u_didx_i == 16'd0);"),
    "M08_restore_skips_image_check": ("writer",
        "          if (desc_img_valid_i) begin\n            img_ok_r <= 1'b1; cur_r <= '0; st_r <= R_NEXT;",
        "          if (1'b1) begin\n            img_ok_r <= 1'b1; cur_r <= '0; st_r <= R_NEXT;"),
    "M09_apply_blindly": ("writer",
        "        R_AUX: begin\n          // per-group value judgement, by the rule the SET program applies\n",
        "        R_AUX: begin\n          // per-group value judgement, by the rule the SET program applies\n"
        "          if (is_scalar_w && !(cg_r == 4'(G_FMTI) || cg_r == 4'(G_FMTO))) st_r <= R_APPLY; else\n"),
    "M10_fmt_full_judge": ("writer",
        "                if (aux_r[0]) begin\n                  frest_r[",
        "                if (aux_r[0] && aux_r[1]) begin\n                  frest_r["),
    "M11_no_orphan_check": ("writer",
        "            chk_done_r <= 1'b1; k_r <= 8'd0; st_r <= R_CHK;",
        "            chk_done_r <= 1'b1; k_r <= 8'd0; st_r <= R_NEXT;"),
    "M12_no_revert_before_readd": ("writer",
        "            rs_ref_r <= rs_ref_r + 8'd1; k_r <= 8'd0; sub_r <= 4'd0; st_r <= R_MVW;",
        "            rs_ref_r <= rs_ref_r + 8'd1; k_r <= 8'd0; sub_r <= 4'd0; st_r <= R_MVW;\n"
        "            mr_add_r <= 1'b1; mr_from_a_r <= 1'b1; ret_r <= R_MD; st_r <= X_MRH;"),
    "M13_restore_applies_nothing": ("writer",
        "            sb_req_r <= 1'b1; sb_we_r <= 1'b1; sb_name_r <= 1'b0;\n"
        "            sb_addr_r <= {RG_DYN_C, sel_f(cg_r), 3'b000};\n"
        "            sb_didx_r <= (cg_r == 4'(G_CFG)) ? 16'd0 : ci_r;\n"
        "            sb_wdata_r <= val_r; sub_r <= 4'd15; ret_r <= R_APPLY; st_r <= X_BUS;",
        "            sub_r <= 4'd15;"),
    "G01_pend_misses_d3": ("top",
        "  assign pend_w  = (|mgr_dirty_w) | d3_unfl_w;",
        "  assign pend_w  = (|mgr_dirty_w);"),
    "G02_restore_done_without_d3": ("top",
        "  assign rs_done_w = mgr_done_w & d3_done_w;",
        "  assign rs_done_w = mgr_done_w;"),
    #! the snoop taps the SHARED bus, strobe, address and index alike, so the
    #! writer's own restore writes decode to their records
    "G03_restore_writes_are_changes": [
        ("top",
         "  assign u_dyn_ack_w  = !snoop_off_i && !d3_own_w && ub_req_i && ub_we_i && dyn_sel_w && dyn_ready_w;",
         "  assign u_dyn_ack_w  = !snoop_off_i && (d3_own_w ? (sb_req_w && sb_we_w && dyn_sel_w) : (ub_req_i && ub_we_i && dyn_sel_w && dyn_ready_w));"),
        ("top", "      .u_addr_i         (ub_addr_i),", "      .u_addr_i         (st_addr_w),"),
        ("top", "      .u_didx_i         (ub_didx_i),", "      .u_didx_i         (st_didx_w),")],
    "M14_clear_by_index": ("writer",
        "    assign clr_w[gs] = clr_en_w && (cg_r == grp_f(SW_C'(gs)))\n"
        "                     && (ci_r[7:0] == 8'(gs - base_f(grp_f(SW_C'(gs)))));",
        "    assign clr_w[gs] = clr_en_w\n"
        "                     && (ci_r[7:0] == 8'(gs - base_f(grp_f(SW_C'(gs)))));"),
    "M15_overflow_forgets_the_change": ("writer",
        "  assign fl_giveup_w  = fl_err_w && (32'(retry_r) >= RETRY_MAX_P);",
        "  assign fl_giveup_w  = (fl_err_w && (32'(retry_r) >= RETRY_MAX_P)) || fl_ovf_w;"),
    "M16_single_pass_restore": ("writer",
        "      rpass_r <= 1'b0;\n",
        "      rpass_r <= 1'b1;\n"),
    "G04_blank_ignores_d3": ("top",
        "  assign restore_blank_o = mgr_blank_w & d3_blank_w & !restore_fail_o;",
        "  assign restore_blank_o = mgr_blank_w & !restore_fail_o;"),
    "A01_grant_cycle_not_busy": ("arb",
        "  assign m0_busy_o   = p_busy_i || (own_r == O_M1) || iss1_w;",
        "  assign m0_busy_o   = p_busy_i || (own_r == O_M1);"),
    # ---- the restore transaction (page section 8.6) ----
    "R01_no_rollback": ("writer",
        "          end else if (rpass_r) begin\n            rb_act_r <= 1'b1;",
        "          end else if (1'b0) begin\n            rb_act_r <= 1'b1;"),
    "R02_rollback_skips_dyn_store": ("top",
        "      .rst_n           (own_rst_n_w),",
        "      .rst_n           (rst_n),"),
    "R03_rollback_skips_desc_store": ("top",
        "      .rst_n             (own_rst_n_w),",
        "      .rst_n             (rst_n),"),
    "R04_rollback_skips_maps": ("top",
        "  assign map_rst_o           = rb_rst_w;",
        "  assign map_rst_o           = 1'b0;"),
    "R05_closed_releases_the_entity": ("writer",
        "          end else begin\n            rs_closed_r <= 1'b1; st_r <= T_CLOSED;\n          end\n        end\n"
        "        T_CLOSED",
        "          end else begin\n            own_r <= 1'b0; rs_done_r <= 1'b1; st_r <= F_RUN;\n          end\n"
        "        end\n        T_CLOSED"),
    #! the per-record pass agreement deleted: no check at all
    "X01_passes_may_disagree": [
        ("writer", "              if (rpass_r && whole0_r[cur_r]) begin", "              if (1'b0) begin"),
        ("writer", "            end else if (!whole0_r[cur_r]) begin", "            end else if (1'b0) begin")],
    #! round two's rule restored in its place: the passes COUNT their whole
    #! records and must count the same
    "X02_passes_compared_by_count": [
        ("writer", "              if (rpass_r && whole0_r[cur_r]) begin", "              if (1'b0) begin"),
        ("writer", "            end else if (!whole0_r[cur_r]) begin", "            end else if (1'b0) begin"),
        ("writer", "  logic [N_REC_C-1:0] whole0_r;\n", "  logic [N_REC_C-1:0] whole0_r;\n  logic [7:0] x2c0_r, x2c1_r;\n"),
        ("writer", "      pad_bad_r <= 1'b0; whole0_r <= '0;\n",
         "      pad_bad_r <= 1'b0; whole0_r <= '0; x2c0_r <= '0; x2c1_r <= '0;\n"),
        ("writer", "              whole0_r[cur_r] <= 1'b1; st_r <= R_ADV;",
         "              whole0_r[cur_r] <= 1'b1; x2c0_r <= x2c0_r + 8'd1; st_r <= R_ADV;"),
        ("writer", "              rs_ref_r <= rs_ref_r + 8'd1; st_r <= R_ADV;\n            end else begin\n"
                   "              ptr_r <= '0; val_r <= '0; sub_r <= 4'd0; any_rec_r <= 1'b1; st_r <= R_VAL;",
         "              rs_ref_r <= rs_ref_r + 8'd1; x2c1_r <= x2c1_r + 8'd1; st_r <= R_ADV;\n"
         "            end else begin\n"
         "              x2c1_r <= x2c1_r + 8'd1; ptr_r <= '0; val_r <= '0; sub_r <= 4'd0; any_rec_r <= 1'b1; st_r <= R_VAL;"),
        ("writer", "            //! every record agreed with pass 0 as it was read\n            st_r <= R_FIN;",
         "            if (x2c1_r == x2c0_r) st_r <= R_FIN;\n"
         "            else begin if (rs_cause_r == 3'd0) rs_cause_r <= 3'd5; st_r <= R_ABORT; end")],
    "O01_own_taken_at_the_walk": [
        ("writer",
         "      taint_r <= 1'b0; own_r <= 1'b1; alarm_r <= 1'b0;",
         "      taint_r <= 1'b0; own_r <= 1'b0; alarm_r <= 1'b0;"),
        ("writer",
         "        W_WAITGO: if (restore_go_i) st_r <= R_IMG;",
         "        W_WAITGO: if (restore_go_i && !prog_busy_i) begin own_r <= 1'b1; st_r <= R_IMG; end")],
    # ---- the deadline and the drain (page section 8.8) ----
    "W01_no_restore_watchdog": ("writer",
        "  assign wd_exp_w  = rs_active_w && stall_w && (wd_r >= 32'(RS_TMO_CYC_P - 1));",
        "  assign wd_exp_w  = 1'b0;"),
    "D01_abandoned_read_not_drained": ("arb",
        "                    : (own_r == O_M1) ? (drain_r || m1_rready_i) : 1'b0;",
        "                    : (own_r == O_M1) ? m1_rready_i : 1'b0;"),
    "G05_enable_not_released_by_restore": ("top",
        "  assign entity_en_o = en_req_i && rs_done_w;",
        "  assign entity_en_o = en_req_i;"),
    # ---- revision c: what is a transport failure (seam S1) ----
    #! round two's rule: any zero-byte err is an erased record
    "C01_device_error_reads_as_blank": ("writer",
        "            if ((bcnt_r == 17'd0) && !(m_err_i && (m_err_cause_i != CAUSE_UNFRAMED_C))) begin",
        "            if (bcnt_r == 17'd0) begin"),
    #! the port says UNFRAMED for every err: the pinned port's information
    "C02_port_cause_collapsed": ("port",
        "  assign nvm_err_cause_o = nvm_err_o ? cause_r : 2'd0;",
        "  assign nvm_err_cause_o = nvm_err_o ? CAUSE_UNFRAMED_C : 2'd0;"),
    #! the reverse: an erased or unframed header aborts like a device error
    "C03_unframed_reads_as_device_error": ("writer",
        "            if ((bcnt_r == 17'd0) && !(m_err_i && (m_err_cause_i != CAUSE_UNFRAMED_C))) begin",
        "            if ((bcnt_r == 17'd0) && !m_err_i) begin"),
    # ---- revision c: descriptor faults ----
    #! round two's rule: a failed rule fetch is a refused value
    "DF01_desc_error_is_a_refusal": ("writer",
        "            if (rs_cause_r == 3'd0) rs_cause_r <= 3'd6;\n            st_r <= R_ABORT;\n"
        "          end else\n          unique case (cg_r)",
        "            rs_ref_r <= rs_ref_r + 8'd1; st_r <= R_ADV;\n          end else\n          unique case (cg_r)"),
    "DF02_map_revert_read_error_ignored": ("writer",
        "          if (((sub_r == 4'd4) || (sub_r == 4'd5) || (sub_r == 4'd6)) && sb_errq_r) begin",
        "          if (1'b0) begin"),
    "DF03_final_revert_read_error_ignored": ("writer",
        "          if (((sub_r == 4'd2) || (sub_r == 4'd3) || (sub_r == 4'd4)) && sb_errq_r) begin",
        "          if (1'b0) begin"),
    #! an image the restore cannot prove is walked as if it were
    "IMG01_unproven_image_continues": ("writer",
        "          if (desc_img_valid_i && !sb_errq_r) begin\n            img_ok_r <= 1'b1; cur_r <= '0; st_r <= R_NEXT;",
        "          if (1'b1) begin\n            img_ok_r <= 1'b1; cur_r <= '0; st_r <= R_NEXT;"),
    # ---- revision c: descriptor memory response isolation (seam S2) ----
    "DG01_guard_admits_a_request_while_owed": [
        ("guard", "  assign m_req_valid_o = s_req_valid_i && !owed_r;", "  assign m_req_valid_o = s_req_valid_i;"),
        ("guard", "  assign s_req_ready_o = m_req_ready_i && !owed_r;", "  assign s_req_ready_o = m_req_ready_i;")],
    "DG02_rollback_ignores_mem_debt": ("writer",
        "          if ((rb_cnt_r != 2'd0) && !desc_debt_i) begin rb_rst_r <= 1'b0; st_r <= B_LOC; end",
        "          if (rb_cnt_r != 2'd0) begin rb_rst_r <= 1'b0; st_r <= B_LOC; end"),
    # ---- revision c: the bounded binding walk (seams S1, S3) ----
    "B01_binding_walk_no_deadline": ("bind",
        "  assign rs_tmo_w    = rs_stall_w && (rs_wd_r >= 32'(RS_TMO_CYC_P - 1));",
        "  assign rs_tmo_w    = 1'b0;"),
    #! processor issue 20's defect: the binding manager ignores the cause
    "B02_binding_device_error_reads_as_empty": [
        ("bind", "                   && (nvm_err_cause_i != 2'd2);", "                   && 1'b0;"),
        ("bind", "                    && ((nvm_err_i && (rbcnt_r == 17'd0) && (nvm_err_cause_i == 2'd2))",
         "                    && ((nvm_err_i && (rbcnt_r == 17'd0))")],
    "B03_binding_abort_not_drained": ("arb",
        "    else if (m0_abort_i && (own_r == O_M0))      drain_r <= 1'b1;",
        "    else if (1'b0)      drain_r <= 1'b1;"),
    "B04_binding_unframed_reads_as_device_error": [
        ("bind", "                   && (nvm_err_cause_i != 2'd2);", "                   && 1'b1;"),
        ("bind", "                    && ((nvm_err_i && (rbcnt_r == 17'd0) && (nvm_err_cause_i == 2'd2))",
         "                    && ((1'b0)")],
    # ---- the map record's framing (page section 8.3) ----
    "P01_padding_by_first_byte": ("writer",
        "            allff_r <= allff_r && (bs_rd_w == 8'hFF);",
        "            allff_r <= (eb_r == 4'd0) ? (bs_rd_w == 8'hFF) : allff_r;"),
    "P02_padding_holes_not_refused": ("writer",
        "            else if (seen_pad_r) pad_bad_r  <= 1'b1;",
        "            else if (1'b0) pad_bad_r  <= 1'b1;"),
}

#: PER-GROUP TRIGGER DELETION (the restatement of the saved-state page's mark
#: acceptance, page section 15 item 1): each deletes one group's live-write
#: trigger, both format directions and both map directions separately
TRIGGER_SEAMS = {
    "cfg":  ("  assign set_w[S_CFG_C] = dyn_w && (u_sel_w == 13'd0) && (u_didx_i == 16'd0);",
             "  assign set_w[S_CFG_C] = 1'b0;"),
    "rate": ("    assign set_w[S_RATE_C + gi] = dyn_w && (u_sel_w == 13'd1) && (u_didx_i == 16'(gi));",
             "    assign set_w[S_RATE_C + gi] = 1'b0;"),
    "clks": ("    assign set_w[S_CLKS_C + gi] = dyn_w && (u_sel_w == 13'd2) && (u_didx_i == 16'(gi));",
             "    assign set_w[S_CLKS_C + gi] = 1'b0;"),
    "fmti": ("    assign set_w[S_FMTI_C + gi] = dyn_w && (u_sel_w == 13'd3) && (u_didx_i == 16'(gi));",
             "    assign set_w[S_FMTI_C + gi] = 1'b0;"),
    "fmto": ("    assign set_w[S_FMTO_C + gi] = dyn_w && (u_sel_w == 13'd4) && (u_didx_i == 16'(gi));",
             "    assign set_w[S_FMTO_C + gi] = 1'b0;"),
    "ptof": ("    assign set_w[S_PTOF_C + gi] = dyn_w && (u_sel_w == 13'd5) && (u_didx_i == 16'(gi));",
             "    assign set_w[S_PTOF_C + gi] = 1'b0;"),
    "mapi": ("    assign set_w[S_MAPI_C + gi] = map_w && (me_type_i == T_SPI_C) && (me_idx_i == 16'(gi));",
             "    assign set_w[S_MAPI_C + gi] = 1'b0;"),
    "mapo": ("    assign set_w[S_MAPO_C + gi] = map_w && (me_type_i == T_SPO_C) && (me_idx_i == 16'(gi));",
             "    assign set_w[S_MAPO_C + gi] = 1'b0;"),
    "name": ("    assign set_w[S_NAME_C + gi] = name_w && (u_addr_i[15:6] == 10'(gi));",
             "    assign set_w[S_NAME_C + gi] = 1'b0;"),
}
#: PER-GROUP REPLAY DELETION: each skips one group's restore write, and only it
APPLY_SEAM = "        R_APPLY: begin\n          //! write the value back with its valid flag; not a change\n"
MAP_SEAM = "            4'(G_MAPI), 4'(G_MAPO): begin\n"
REPLAY_SEAMS = {
    g: ("writer", APPLY_SEAM, APPLY_SEAM.replace("R_APPLY: begin", f"R_APPLY: if (cg_r == 4'(G_{G})) st_r <= R_ADV; else begin"))
    for g, G in (("cfg", "CFG"), ("rate", "RATE"), ("clks", "CLKS"), ("fmti", "FMTI"), ("fmto", "FMTO"),
                 ("ptof", "PTOF"))}
REPLAY_SEAMS["mapi"] = ("writer", MAP_SEAM, MAP_SEAM.replace(": begin", ": if (cg_r == 4'(G_MAPI)) st_r <= R_ADV; else begin"))
REPLAY_SEAMS["mapo"] = ("writer", MAP_SEAM, MAP_SEAM.replace(": begin", ": if (cg_r == 4'(G_MAPO)) st_r <= R_ADV; else begin"))
REPLAY_SEAMS["name"] = ("writer",
                        "              ptr_r <= '0; k_r <= 8'd0; eb_r <= '0; st_r <= R_NAMEW;",
                        "              ptr_r <= '0; k_r <= 8'd0; eb_r <= '0; st_r <= R_ADV;")
#: the record each group's first index lives at
GROUP_RID = {"cfg": 0x00, "rate": 0x02, "clks": 0x0A, "fmti": 0x30, "fmto": 0x40, "ptof": 0x50,
             "mapi": 0x60, "mapo": 0x70, "name": 0x80}
#: the shape each group is expressible at: a legal non-default sampling rate
#: needs two listed rates (the synthetic shape); an input map needs clusters
GROUP_SHAPE = {g: ("1x1r2" if g == "rate" else "1x1") for g in GROUP_RID}
for _g, (_old, _new) in TRIGGER_SEAMS.items():
    MUTATIONS[f"TRG_{_g}"] = ("writer", _old, _new)
for _g, _m in REPLAY_SEAMS.items():
    MUTATIONS[f"RPL_{_g}"] = _m

#: case K15's sweep: the D3 writer released N cycles after the binding
#: manager enters H_FL_CRC. The base build must commit both records at EVERY
#: N and must reach the grant-cycle collision at one N at least.
K15_SWEEP = [f"g{n}" for n in range(0, 8)]

#: mutant -> (case, variant, THE ONE CHECK that must kill it, shape). The
#: variant "*" is K15's sweep: killed when the check fails at any N. A kill
#: counts only in a run that COMPLETED (case_completed passes).
KILLERS = {
    "M01_taint_ignored": ("K2_change_during_record_write", "", "no_durable_claim_over_unsaved", "1x1"),
    "M02_clear_at_latch": ("K1_single_change_converges", "", "no_durable_claim_over_unsaved", "1x1"),
    "M03_clear_wins_same_edge": ("K5_change_on_the_done_edge", "", "same_edge_change_survives@end:0x50", "1x1"),
    "M04_clear_by_group": ("K4_second_record_in_flight", "", "value_in_slot@end:0x51", "1x1"),
    "M05_latch_ignores_program": ("K11_name_latch_waits_for_the_program", "", "written_value_was_set:0x80", "1x1"),
    "M06_identify_is_a_change": ("K14_identify_is_not_persisted", "", "identify_never_persisted", "1x1"),
    "M08_restore_skips_image_check": ("V7_names_only", "", "restored_name_survives_first_command:0x80", "1x1"),
    "M09_apply_blindly": ("V2_refused_rate", "", "refused_value_not_applied:0x02", "1x1"),
    "M10_fmt_full_judge": ("V6b_restore_coupled_pair", "", "coupled_pair_restored", "1x1"),
    "M11_no_orphan_check": ("V8_orphaning_format_reverted", "", "no_orphaned_mapping_after_restore", "1x1"),
    "M12_no_revert_before_readd": ("V9_refused_maps_revert_their_formats", "",
                                   "refused_group_falls_back_to_default:0x70", "1x1"),
    "M13_restore_applies_nothing": ("V1b_restore_everything", "", "value_restored:0x50", "1x1"),
    "M14_clear_by_index": ("K4g_second_group_in_flight", "", "value_in_slot@end:0x0a", "1x1"),
    "M15_overflow_forgets_the_change": ("K16_map_set_larger_than_its_record", "",
                                        "no_durable_claim_over_unsaved", "8x8"),
    "M16_single_pass_restore": ("V11_torn_read_restores_nothing", "", "torn_walk_applies_nothing@boot", "1x1"),
    "G01_pend_misses_d3": ("K1_single_change_converges", "", "no_durable_claim_over_unsaved", "1x1"),
    "G02_restore_done_without_d3": ("V1b_restore_everything", "", "entity_enabled_after_restore@boot", "1x1"),
    "G03_restore_writes_are_changes": ("V1b_restore_everything", "", "restore_sets_no_dirty@boot", "1x1"),
    "G04_blank_ignores_d3": ("V7_names_only", "", "blank_is_both_walks@boot", "1x1"),
    "A01_grant_cycle_not_busy": ("K15_binding_on_the_d3_grant_cycle", "*", "both_records_committed", "1x1"),
    "F01_old_boot_order": ("V1b_restore_everything", "", "value_restored:0x50", "1x1"),
    "R01_no_rollback": ("V15_rollback_pass1_late", "", "rolled_back_to_defaults@terminal", "1x1"),
    "R02_rollback_skips_dyn_store": ("V15_rollback_pass1_late", "", "rolled_back_to_defaults@terminal", "1x1"),
    "R03_rollback_skips_desc_store": ("V15_rollback_pass1_late", "", "rolled_back_to_defaults@terminal", "1x1"),
    "R04_rollback_skips_maps": ("V16_rollback_pass1_maps", "", "rolled_back_to_defaults@terminal", "1x1"),
    "R05_closed_releases_the_entity": ("V17_rollback_cannot_validate", "", "closed_keeps_entity_dark@recovered",
                                       "1x1"),
    "X01_passes_may_disagree": ("V18b_header_changed_between_passes", "", "rolled_back_to_defaults@terminal",
                                "1x1"),
    "X02_passes_compared_by_count": ("V18c_changes_balance_counts", "", "rolled_back_to_defaults@terminal", "1x1"),
    "C01_device_error_reads_as_blank": ("H8_header_error_sole_saved_record", "", "header_fault_contained@terminal",
                                        "1x1"),
    "C02_port_cause_collapsed": ("H1_header_error_both_passes", "", "header_fault_contained@terminal", "1x1"),
    "C03_unframed_reads_as_device_error": ("V10_blank_first_boot", "", "blank_boot_is_not_a_failure@boot", "1x1"),
    "DF01_desc_error_is_a_refusal": ("V20b_desc_error_once_after_apply", "", "rolled_back_to_defaults@terminal",
                                     "1x1"),
    #! its garbage default is refused by the re-add judge, so the restore still
    #! rolls back: the kill is the cause it then reports (4, not the truth, 6)
    "DF02_map_revert_read_error_ignored": ("V20c_desc_error_in_the_map_revert", "",
                                           "rollback_premise@terminal", "1x1"),
    "DF03_final_revert_read_error_ignored": ("V20d_desc_error_in_the_final_revert", "",
                                             "rolled_back_to_defaults@terminal", "1x1"),
    "IMG01_unproven_image_continues": ("V22b_image_unproven_simple_records", "",
                                       "closed_when_image_unproven@recovered", "1x1"),
    "DG01_guard_admits_a_request_while_owed": ("V23_late_desc_beats_in_service", "",
                                               "late_beats_never_served@restored", "1x1"),
    "DG02_rollback_ignores_mem_debt": ("V21b_desc_debt_outlasts_the_store", "", "rolled_back_to_defaults@terminal",
                                       "1x1"),
    "B01_binding_walk_no_deadline": ("W13_binding_walk_silent", "", "binding_walk_bounded@terminal", "1x1"),
    "B02_binding_device_error_reads_as_empty": ("W16_binding_header_device_error", "",
                                                "binding_walk_failed@terminal", "1x1"),
    "B03_binding_abort_not_drained": ("W13c_binding_late_after_deadline", "", "later_change_persists@recovered",
                                      "1x1"),
    "B04_binding_unframed_reads_as_device_error": ("V10_blank_first_boot", "", "blank_boot_is_not_a_failure@boot",
                                                   "1x1"),
    "O01_own_taken_at_the_walk": ("K19_command_before_the_restore", "", "value_in_slot@end:0x50", "1x1"),
    "W01_no_restore_watchdog": ("W4_silent_pass1", "", "restore_terminal_bounded@terminal", "1x1"),
    "D01_abandoned_read_not_drained": ("W6_late_pass1_after_deadline", "", "later_change_persists@recovered", "1x1"),
    "G05_enable_not_released_by_restore": ("W14_enable_requested_before_the_restore", "",
                                           "entity_enabled_after_terminal@boot", "1x1"),
    "P01_padding_by_first_byte": ("V3a_map_index_0xff00", "", "map_record_verdict:0x70", "1x1"),
    "P02_padding_holes_not_refused": ("V3e_map_hole", "", "malformed_refused_untouched:0x70", "1x1"),
}
for _g, _rid in GROUP_RID.items():
    KILLERS[f"TRG_{_g}"] = ("V1a_set_everything", "", f"value_in_slot@cut:{_rid:#04x}", GROUP_SHAPE[_g])
    KILLERS[f"RPL_{_g}"] = ("V1b_restore_everything", "", f"value_restored:{_rid:#04x}", GROUP_SHAPE[_g])
#: the stream formats are killed TWICE: by V1a/V1b, whose output value is a
#: SYNTHETIC narrowing, and by the SHIPPING-LEGAL V1s pair (the declared
#: output format and a family-legal input format); a kill needs both
for _g, _rid in (("fmti", 0x30), ("fmto", 0x40)):
    KILLERS[f"TRG_{_g}"] = [KILLERS[f"TRG_{_g}"],
                            ("V1s_a_shipping_output_format", "", f"value_in_slot@cut:{_rid:#04x}", "1x1")]
    KILLERS[f"RPL_{_g}"] = [KILLERS[f"RPL_{_g}"],
                            ("V1s_b_shipping_output_format_restore", "", f"value_restored:{_rid:#04x}", "1x1")]

#: WHAT REPRODUCES TODAY. The tracked glue (d3_top.sv under D3_TRACKED, the
#: parent as it ships at dev 07294a76) must FAIL these checks, which shows
#: they are not vacuous: nothing is written, nothing converges, nothing comes
#: back. Two of them are a finding about today's glue rather than the gap:
#: it takes the class-6/7 COMMIT MARK, which the SET_NAME and ADD/REMOVE
#: programs raise only after the live write, so the status reads durable
#: over an applied name or map for the program's tail.
TRACKED_CASES = ["K1_single_change_converges", "K10_name_change_converges", "K12_map_change_converges"]
TRACKED_MUST_FAIL = [
    ("K1_single_change_converges", "converged@end"),
    ("K1_single_change_converges", "value_in_slot@end:0x50"),
    ("K10_name_change_converges", "value_in_slot@end:0x80"),
    ("K10_name_change_converges", "no_durable_claim_over_unsaved"),
    ("K12_map_change_converges", "value_in_slot@end:0x70"),
    ("K12_map_change_converges", "no_durable_claim_over_unsaved"),
    ("V1b_restore_everything", "set_value_survives_power_cycle:0x50"),
]
#: ...and must PASS these: a dynamic-state change is reported by the store's
#: own sticky level from the write, so today's status never reads durable
#: over one, and every case runs to its end
TRACKED_MUST_PASS = [
    ("K1_single_change_converges", "no_durable_claim_over_unsaved"),
    ("V1a_set_everything", "no_durable_claim_over_unsaved"),
    ("V1b_restore_everything", "no_durable_claim_over_unsaved"),
    ("*", "case_completed"),
]

#: the binding manager's state encoding the harness compares against (the
#: bridge's H_FL_REQ = 13 and the K15 case's H_FL_CRC = 12)
M0_STATES = {"H_FL_CRC": 12, "H_FL_REQ": 13}


def check_m0_encoding() -> None:
    """Refuse to run if the donor, or its amended prototype, moved the states
    the harness names."""
    for path in (PINNED_BIND, SOURCES["bind"][0]):
        src = path.read_text()
        m = re.search(r"typedef enum logic \[3:0\] \{(.*?)\} hstate_e;", src, re.S)
        if not m:
            raise SystemExit(f"{path.name}: hstate_e not found")
        names = re.findall(r"^\s*(H_[A-Z_]+)", m.group(1), re.M)
        for name, code in M0_STATES.items():
            if name not in names or names.index(name) != code:
                raise SystemExit(f"{path.name}: {name} is not encoding {code} ({names})")


def seams(name: str) -> list:
    m = MUTATIONS[name]
    return m if isinstance(m, list) else [m]


def mutate_text(key: str, text: str, name: str) -> str:
    for k, old, new in seams(name):
        if k != key:
            continue
        if text.count(old) != 1:
            raise SystemExit(f"mutation {name}: seam count {text.count(old)}")
        text = text.replace(old, new)
    return text


def host_firmware(text: str, old_boot: bool) -> str:
    for old, new in FW_SUBS:
        if text.count(old) != 1:
            raise SystemExit(f"firmware seam count {text.count(old)}: {old[:50]!r}")
        text = text.replace(old, new)
    if text.count(FENCE_RW) != 3:
        raise SystemExit(f"expected 3 rw fences, found {text.count(FENCE_RW)}")
    text = text.replace(FENCE_RW, "(void)0;")
    if text.count(BOOT_OLD) != 1:
        raise SystemExit("the milan_init boot order seam moved")
    if not old_boot:
        text = text.replace(BOOT_OLD, BOOT_NEW)
    for old, new in FW_REPORT:
        if text.count(old) != 1:
            raise SystemExit(f"firmware report seam count {text.count(old)}: {old[:50]!r}")
        text = text.replace(old, new)
    return text


def killers(m: str) -> list:
    """Every (case, variant, check, shape) that must kill mutant m."""
    k = KILLERS[m]
    return k if isinstance(k, list) else [k]


def all_builds(shapes: list[str]) -> list[Build]:
    out = [Build(f"base-{s}", s) for s in SHAPES]
    out.append(Build("tracked-1x1", "1x1", tracked=True))
    for m in MUTATIONS:
        unknown = {k for k, _o, _n in seams(m)} - set(SOURCES)
        if unknown:
            raise SystemExit(f"mutation {m} names unknown sources {unknown}")
        shapes_of = {k[3] for k in killers(m)}
        if len(shapes_of) != 1:
            raise SystemExit(f"mutation {m}: its killers run at {shapes_of}, one shape is required")
        out.append(Build(f"mut-{m}", shapes_of.pop(), mut=m))
    out.append(Build("mut-F01_old_boot_order", KILLERS["F01_old_boot_order"][3], fw_old_boot=True))
    return out


def do_build(b: Build, s: Shape, jobs: int) -> Build:
    work = OUT / "build" / b.name
    if work.exists():
        shutil.rmtree(work)
    (work / "generated").mkdir(parents=True)
    (work / "generated" / "soc.h").write_text(s.header)
    fw = host_firmware(WRITER.read_text(), b.fw_old_boot)
    (work / "milan_baremetal.host.c").write_text(fw)
    for key, (src, dst) in SOURCES.items():
        text = src.read_text()
        if b.mut:
            text = mutate_text(key, text, b.mut)
        (work / dst).write_text(text)
    defs = [f"-DNVM_HOST_JOURNAL_OFFSET=0x{ref.JOURNAL:x}u",
            f"-DNVM_HOST_AEM_OFFSET=0x{ref.AEM_OFFSET:x}u",
            f"-DNVM_HOST_IMAGE_OFF=0x{ref.IMAGE_OFF:x}u"]
    cc = ["gcc", "-std=gnu11", "-O2", "-g", "-Wall", "-Wextra", "-Werror",
          f"-I{work}", f"-I{HARNESS}", f"-I{STUBS}"]
    logs = OUT / "logs"
    cmd(cc + defs + ["-c", HARNESS / "d3_host.c", "-o", work / "host.o"], logs / f"{b.name}-host.log")
    cmd(cc + ["-Wno-format", "-c", work / "milan_baremetal.host.c", "-o", work / "fw.o"],
        logs / f"{b.name}-fw.log")
    gparams = [f"-G{k}={v}" for k, v in s.params.items()]
    vl = ["verilator", "--cc", "--exe", "--build", "-j", str(jobs), "--top-module", "d3_top",
          "--Mdir", work / "obj", "-Wall", "-Wno-fatal", "-Werror-USERERROR", "-Wno-UNUSEDSIGNAL",
          "-Wno-UNUSEDPARAM", "--x-assign", "unique", "--x-initial", "unique"] + gparams
    if b.tracked:
        vl += ["+define+D3_TRACKED"]
    vl += ["-CFLAGS", f"-std=c++17 -O2 -I{HARNESS} -I{STUBS} {' '.join(defs)}",
           "-LDFLAGS", f"{work / 'host.o'} {work / 'fw.o'}"]
    rtl = DONOR_SV + [BACKEND, work / "KL_pp_nvm_mgr_arb.sv"]
    if b.tracked:
        #! the parent as it ships: the PINNED port and binding manager
        rtl += [PINNED_PORT, PINNED_BIND]
    else:
        rtl += [work / "KL_pp_nvm_port_amd.sv", work / "KL_acmp_nvm_shadow_amd.sv",
                work / "KL_aecp_desc_mem_guard.sv", work / "KL_aecp_nvm_writer.sv"]
    vl += rtl + [work / "d3_top.sv", HARNESS / "d3_bridge.cpp", HARNESS / "d3_cases.cpp",
                 "-o", "d3sim"]
    cmd(vl, logs / f"{b.name}-verilator.log")
    b.binary = work / "obj" / "d3sim"
    return b


# -------------------------------------------------------------------- running
@dataclasses.dataclass
class Run:
    case: str
    build: str
    variant: str
    rc: int
    obs: dict
    evts: list
    fw: list
    done: bool
    out: Path
    slots_in: tuple | None = None
    notes: dict = dataclasses.field(default_factory=dict)
    snaps: dict = dataclasses.field(default_factory=dict)


def run_case(b: Build, s: Shape, case: str, variant: str = "",
             slots: tuple | None = None) -> Run:
    tag = case + (f"~{variant}" if variant else "")
    out = OUT / "runs" / b.name / tag
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)
    argv = [str(b.binary), "--case", case, "--out", str(out), "--records", str(s.table),
            "--facts", str(s.facts), "--aem", str(s.aem)]
    if variant:
        argv += ["--variant", variant]
    if slots:
        argv += ["--slot-a", str(slots[0]), "--slot-b", str(slots[1])]
    p = subprocess.run(argv, text=True, capture_output=True)
    (out / "stdout.log").write_text(p.stdout)
    (out / "stderr.log").write_text(p.stderr)
    obs, evts, fw, done, notes, snaps = {}, [], [], False, {}, {}
    for ln in p.stdout.splitlines():
        if ln.startswith("SNAP "):
            sn = json.loads(ln[5:])
            snaps[sn["tag"]] = sn["s"]
            continue
        if ln.startswith("OBS "):
            o = json.loads(ln[4:])
            obs[o["tag"]] = o
        elif ln.startswith("EVT "):
            evts.append(json.loads(ln[4:]))
        elif ln.startswith("NOTE "):
            n = json.loads(ln[5:])
            notes[n["key"]] = n
        elif ln.startswith("Milan "):
            fw.append(ln)
        elif ln.startswith("CASE_DONE"):
            done = True
    return Run(case, b.name, variant, p.returncode, obs, evts, fw, done, out, slots, notes, snaps)


def blank_slot() -> bytes:
    return b"\xff" * 0x10000


def crafted(s: Shape, name: str, over: dict) -> tuple:
    """A slot image the writer accepts (section 6.2 of the saved-state page):
    every record ERASED but the ones this case sets."""
    frames = {}
    for rid, (_off, _flen, plen, _g, _i) in s.recs.items():
        frames[rid] = frame_record(rid, over[rid], s.donor.layout) if rid in over else erased_record(plen)
    ident = ref.Ident(seq=1, entity_id=s.ident.entity_id, model_id=s.ident.model_id)
    blob, _ = klj2_assemble(frames, s.donor, ident)
    d = OUT / "crafted" / s.name
    d.mkdir(parents=True, exist_ok=True)
    a, bb = d / f"{name}-slotA.bin", d / f"{name}-slotB.bin"
    a.write_bytes(blob + b"\xff" * (0x10000 - len(blob)))
    bb.write_bytes(blank_slot())
    return (a, bb)


def narrower(f: int, ch: int) -> int:
    return (f & ~((1 << 52) | (0x3FF << 22))) | (ch << 22)


def default_out_maps(s: Shape, port: int) -> list:
    """The MODEL's image-default set for OUT port `port` (d3_cases.cpp
    default_maps): cluster k maps to channel k of stream port % n_so."""
    n_so = s.params["N_STREAM_OUT_P"]
    cls = [s.recs[r][2] // 8 for r in sorted(s.recs) if 0x70 <= r < 0x80]
    st = port % n_so
    ch = (s.def_fmt_out[st] >> 22) & 0x3FF if (s.def_fmt_out[st] >> 56) == 0x02 else 0
    return [(st, k, k, 0) for k in range(min(cls[port], ch, 8))]


def default_in_maps(s: Shape, port: int) -> list:
    """The MODEL's image-default set for IN port `port` (d3_cases.cpp
    default_maps): cluster k maps to channel k of stream port % n_si."""
    n_si = s.params["N_STREAM_IN_P"]
    cls = [s.recs[r][2] // 8 for r in sorted(s.recs) if 0x60 <= r < 0x70]
    st = port % n_si
    ch = (s.def_fmt_in[st] >> 22) & 0x3FF if (s.def_fmt_in[st] >> 56) == 0x02 else 0
    return [(st, k, k, 0) for k in range(min(cls[port], ch))]


def map_bytes(maps: list, clusters: int) -> bytes:
    v = b"".join(struct.pack(">HHHH", *m) for m in maps)
    return v + b"\xff" * (8 * clusters - len(v))


#: the dynamic-state selector of each scalar group, its record base and width
SEL_OF = {0x00: (0, 1, 2), 0x02: (1, 8, 4), 0x0A: (2, 8, 2), 0x30: (3, 16, 8), 0x40: (4, 16, 8),
          0x50: (5, 16, 4)}


def show(got, want) -> str:
    """A live value against the value wanted: bytes from their first
    difference, scalars whole."""
    if isinstance(got, bytes) and isinstance(want, bytes):
        k = next((i for i in range(min(len(got), len(want))) if got[i] != want[i]), min(len(got), len(want)))
        return f"live {got[k:k + 12].hex() or '(end)'} want {want[k:k + 12].hex() or '(end)'} from byte {k}"
    return f"live {got} want {want}"


def scalar_of(rid: int) -> tuple | None:
    """(selector, index, width) of a scalar record id, else None."""
    for base, (sel, span, width) in SEL_OF.items():
        if base <= rid < base + span:
            return sel, rid - base, width
    return None


# ---------------------------------------------------------------------- grading
class Grade:
    def __init__(self, run: Run, s: Shape):
        self.r, self.s = run, s
        self.checks: dict[str, tuple[bool, str]] = {}

    def check(self, name: str, ok: bool, detail: str) -> None:
        self.checks[name] = (bool(ok), detail)

    # ---- journal helpers
    def slots(self, a: Path, b: Path) -> dict:
        best = None
        for blob in (a.read_bytes(), b.read_bytes()):
            img_len = struct.unpack_from("<I", blob, 16)[0] if blob[:4] == b"KLJ2" else 0
            if not (44 <= img_len <= 0x10000):
                continue
            v, applied = klj2_decode(blob[:img_len], self.s.donor, self.s.ident_any(blob), self.s.expect)
            if v != 0:
                continue
            seq = struct.unpack_from("<I", blob, 8)[0]
            if best is None or ((seq - best[0]) & 0xFFFFFFFF) < 0x80000000:
                best = (seq, {rid_of_key(k, self.s.donor.base): p for k, p in applied.items()})
        return best[1] if best else {}

    def tag_slots(self, tag: str) -> dict:
        return self.slots(self.r.out / f"{tag}-slotA.bin", self.r.out / f"{tag}-slotB.bin")

    def changes(self) -> list:
        return [(e["cyc"], e["rid"], bytes.fromhex(e["v"])) for e in self.r.evts if e["k"] == "chg"]

    def ops(self) -> list:
        return [e for e in self.r.evts if e["k"] == "op"]

    def ans(self, tag: str) -> tuple:
        for e in self.r.evts:
            if e["k"] == "ans" and e["tag"] == tag:
                return int(e["v"], 16), e["err"]
        return None, None

    def boot(self) -> dict:
        for e in self.r.evts:
            if e["k"] == "boot":
                return e
        return {}

    def name_of(self, tag: str) -> bytes | None:
        out = b""
        for l in range(8):
            v, _e = self.ans(f"{tag}.lane{l}")
            if v is None:
                return None
            out += v.to_bytes(8, "big")
        return out

    # ---- the bridge's snapshots: every row, name and map set at one cycle
    def d3_rids(self) -> list:
        return sorted(r for r in self.s.recs
                      if r != 0x01 and not 0x12 <= r < 0x1A and not 0x20 <= r < 0x30)

    def snap_value(self, sn: dict, rid: int):
        """The live value of record `rid` in snapshot `sn`: a scalar as
        (value, valid), a map set or a name as bytes."""
        sc = scalar_of(rid)
        if sc:
            sel, idx, _w = sc
            for row in sn["rows"]:
                if row[0] == sel and row[1] == idx:
                    return int(row[2], 16), row[3]
            return None
        if 0x60 <= rid < 0x70:
            return bytes.fromhex(sn["maps_in"][rid - 0x60])
        if 0x70 <= rid < 0x80:
            return bytes.fromhex(sn["maps_out"][rid - 0x70])
        return bytes.fromhex(sn["names"][rid - 0x80])

    def default_of(self, rid: int):
        if scalar_of(rid):
            return 0, 0
        if 0x60 <= rid < 0x70:
            return map_bytes(default_in_maps(self.s, rid - 0x60), self.s.recs[rid][2] // 8)
        if 0x70 <= rid < 0x80:
            return map_bytes(default_out_maps(self.s, rid - 0x70), self.s.recs[rid][2] // 8)
        return self.s.names[rid - 0x80]

    def want_of(self, rid: int, payload: bytes):
        """What restoring `payload` into record `rid` leaves live."""
        sc = scalar_of(rid)
        if sc:
            return int.from_bytes(payload, "big"), 1
        return payload

    def mismatches(self, sn: dict | None, want: dict) -> list:
        """Every D3 record whose live value in `sn` is not `want[rid]` when
        the record is in `want`, or not its reset/image default otherwise."""
        if not sn:
            return ["no snapshot"]
        bad = []
        for rid in self.d3_rids():
            got = self.snap_value(sn, rid)
            exp = self.want_of(rid, want[rid]) if rid in want else self.default_of(rid)
            if got != exp:
                bad.append(f"{rid:#04x} {show(got, exp)}")
        return bad

    def boot_evt(self, key: str, default=0):
        return self.boot().get(key, default)

    def rs_writes(self) -> list:
        return [(e["cyc"], e["what"]) for e in self.r.evts if e["k"] == "rsw"]

    def hold(self) -> dict:
        for e in self.r.evts:
            if e["k"] == "hold":
                return e
        return {}

    def contained(self, want_rb: int, name: str = "rolled_back_to_defaults@terminal") -> None:
        """The restore transaction ended in DEFAULTS: every D3 record at its
        reset or image default at the terminal, done and fail, rolled back
        iff pass 1 had begun, and the bus released."""
        sn = self.r.snaps.get("terminal")
        o = self.r.obs.get("terminal", {})
        bad = self.mismatches(sn, {})
        ok = (not bad and o.get("d3_done") == 1 and o.get("d3_fail") == 1 and o.get("d3_rb") == want_rb
              and o.get("d3_closed") == 0 and o.get("own") == 0)
        self.check(name, ok, f"{len(bad)} records off their defaults {bad[:2]}; D3 done {o.get('d3_done')} "
                             f"fail {o.get('d3_fail')} rolled back {o.get('d3_rb')} (want {want_rb}) closed "
                             f"{o.get('d3_closed')} own {o.get('own')} cause {o.get('d3_cause')}")

    def enable_after_terminal(self) -> None:
        b = self.boot()
        en, term, done = b.get("enable", 0), b.get("terminal", 0), b.get("restore_done", 0)
        self.check("entity_enabled_after_terminal@boot", en > 0 and term > 0 and done > 0 and en >= term and en >= done,
                   f"entity enabled at {en}, D3 terminal at {term}, restore done at {done}, firmware asked at "
                   f"{b.get('fw_enable')}")

    def no_restore_write_after(self) -> None:
        b = self.boot()
        term, en = b.get("terminal", 0), b.get("enable", 0)
        late = [(c, w) for c, w in self.rs_writes() if (term and c > term) or (en and c >= en)]
        self.check("no_restore_write_after_terminal", term > 0 and not late,
                   f"{len(self.rs_writes())} restore writes, the last at "
                   f"{self.rs_writes()[-1][0] if self.rs_writes() else None}; terminal {term}, enable {en}; "
                   f"after them {late[:3]}")

    def served_after_recovery(self, want: tuple) -> None:
        v, _e = self.ans("rec.ptof0.value")
        valid, _e2 = self.ans("rec.ptof0.valid")
        self.check("command_served_after_recovery@recovered", v is not None and (v, valid) == want,
                   f"GET after recovery answered {v} valid {valid}, want {want}")

    def preloads(self) -> list:
        return [(e["cyc"], e["sink"]) for e in self.r.evts if e["k"] == "pre"]

    def saved_state_kept(self, extra: dict, tag: str = "recovered") -> None:
        """A failed restore rewrites nothing: the newest verified slot still
        holds every record the boot slot held but 0x50 (the later SET)."""
        cut = extra.get("cut_slots") or extra.get("crafted", {})
        now = self.tag_slots(tag)
        kept = {rid: v for rid, v in cut.items() if rid != 0x50}
        lost = [f"{rid:#04x}" for rid, v in kept.items() if now.get(rid) != v]
        self.check(f"saved_state_kept@{tag}", bool(cut) and not lost,
                   f"{len(kept)} saved records besides 0x50, {len(lost)} changed in the newest verified slot "
                   f"{lost[:4]}")

    def closed_dark(self, name: str = "closed_keeps_entity_dark@recovered") -> None:
        o = self.r.obs.get("recovered", {})
        b = self.boot()
        ans, _ = self.ans("rec.ptof0.value")
        ok = (o.get("d3_closed") == 1 and o.get("restore_done") == 0 and o.get("restore_fail") == 1
              and o.get("own") == 1 and o.get("entity_en") == 0 and b.get("enable", 0) == 0 and ans is None
              and b.get("fw_enable", 0) > 0)
        self.check(name, ok,
                   f"closed {o.get('d3_closed')}, restore done {o.get('restore_done')} fail {o.get('restore_fail')}, "
                   f"own {o.get('own')}, entity enabled {o.get('entity_en')} (first {b.get('enable')}), firmware "
                   f"asked at {b.get('fw_enable')}, a GET answered {ans}, cause {b.get('cause')}")

    def restore_complete(self, extra: dict) -> None:
        cut = extra.get("cut_slots") or extra.get("crafted", {})
        saved = {rid: v for rid, v in cut.items() if rid in self.d3_rids()}
        bad = self.mismatches(self.r.snaps.get("terminal"), saved)
        o = self.r.obs.get("terminal", {})
        self.check("restore_complete@terminal", not bad and o.get("d3_done") == 1 and o.get("d3_fail") == 0,
                   f"{len(bad)} records not as saved {bad[:2]}, D3 done {o.get('d3_done')} fail {o.get('d3_fail')}")

    def terminal_bounded(self, start: int, bound: int) -> None:
        term = self.boot_evt("terminal")
        self.check("restore_terminal_bounded@terminal", term > 0 and start > 0 and term - start <= bound,
                   f"stall began at {start}, D3 terminal at {term} (bound {bound} cycles)")

    # ---- the global property
    def durability(self) -> None:
        """NO DURABLE CLAIM OVER AN UNSAVED CHANGE: whenever the status reads
        durable (backed 1, dirty 0, stale 0, pend 0), every record's latest
        accepted value is the value the newest verified slot holds; and a
        change inside a durable interval ends it within 3 cycles."""
        acks = [(e["cyc"], e["n"]) for e in self.r.evts if e["k"] == "ack"]
        ack_slots = {n: self.slots(self.r.out / f"ack{n}-slotA.bin", self.r.out / f"ack{n}-slotB.bin")
                     for _c, n in acks}
        init = self.slots(*self.r.slots_in) if self.r.slots_in else {}
        dur = [(e["cyc"], e["v"]) for e in self.r.evts if e["k"] == "dur"]
        chg = self.changes()
        bad = []
        intervals = []
        for i, (c, v) in enumerate(dur):
            if v == 1:
                end = dur[i + 1][0] if i + 1 < len(dur) else 1 << 62
                intervals.append((c, end))
        for start, end in intervals:
            prior = [n for c, n in acks if c <= start]
            slot = ack_slots[prior[-1]] if prior else init
            latest = {}
            for c, rid, v in chg:
                if c <= start:
                    latest[rid] = v
            for rid, v in latest.items():
                if slot.get(rid) != v:
                    bad.append(f"durable at {start}: record {rid:#04x} latest {v.hex()} slot "
                               f"{slot.get(rid).hex() if slot.get(rid) is not None else None}")
            for c, rid, v in chg:
                if start < c < end and end - c > 3:
                    bad.append(f"change of {rid:#04x} at {c} inside a durable interval ending {end}")
        self.check("no_durable_claim_over_unsaved", not bad,
                   "; ".join(bad[:3]) if bad else f"{len(intervals)} durable intervals, {len(chg)} changes, "
                                                 f"{len(acks)} acknowledgements")

    def written_values(self) -> None:
        """Every record the writer wrote carries a value some completed
        command left (or a restored one), in a frame whose crc closes."""
        vals: dict[int, set] = {}
        for _c, rid, v in self.changes():
            vals.setdefault(rid, set()).add(v)
        init = self.slots(*self.r.slots_in) if self.r.slots_in else {}
        for rid, v in init.items():
            vals.setdefault(rid, set()).add(v)
        per: dict[int, list] = {}
        frames = {rid: [frame_record(rid, v, self.s.donor.layout) for v in vs] for rid, vs in vals.items()}
        for o in self.ops():
            if o["op"] != 1 or not (o["rid"] < 0x20 or o["rid"] >= 0x30):
                continue
            w = bytes.fromhex(o["w"])
            if o["res"] != "done":
                #! an aborted WRITE leaves its record open (never captured);
                #! what it did put on the face must still be a valid frame's head
                ok = any(f[:len(w)] == w for f in frames.get(o["rid"], []))
                per.setdefault(o["rid"], []).append((ok, w.hex(), True))
                continue
            if len(w) < 8:
                per.setdefault(o["rid"], []).append((False, w.hex(), False))
                continue
            plen = (w[4] << 8) | w[5]
            pay = w[8:8 + plen]
            from nvm_klj2 import crc16_ccitt
            crc_ok = crc16_ccitt(w[:6] + pay) == ((w[6] << 8) | w[7]) and len(w) == 8 + plen
            ok = crc_ok and (pay in vals.get(o["rid"], set()))
            per.setdefault(o["rid"], []).append((ok, pay.hex(), crc_ok))
        for rid, lst in per.items():
            bad = [x for x in lst if not x[0]]
            self.check(f"written_value_was_set:{rid:#04x}", not bad,
                       f"{len(lst)} writes; first bad {bad[0][1]} crc_ok={bad[0][2]}" if bad
                       else f"{len(lst)} writes, every one a value a command left")

    def latch(self) -> None:
        b = self.boot()
        own = b.get("own_max", 0)
        self.check("latch_window_bounded", own <= 2000, f"longest ownership window {own} cycles (bound 2000)")

    # ---- per-case
    def converged(self, tag: str) -> None:
        o = self.r.obs.get(tag, {})
        ok = o.get("backed") == 1 and o.get("dirty") == 0 and o.get("stale") == 0 and o.get("pend") == 0
        self.check(f"converged@{tag}", ok, f"backed {o.get('backed')} dirty {o.get('dirty')} stale "
                                           f"{o.get('stale')} pend {o.get('pend')}")

    def value_in_slot(self, tag: str, rid: int, name: str | None = None) -> None:
        latest = None
        for _c, r, v in self.changes():
            if r == rid:
                latest = v
        got = self.tag_slots(tag).get(rid)
        self.check(name or f"value_in_slot@{tag}:{rid:#04x}", latest is not None and got == latest,
                   f"latest {latest.hex() if latest else None}, newest verified slot "
                   f"{got.hex() if got is not None else None}")


def ident_any(self, blob):   # the slots carry the shape's identity
    return self.ident


Shape.ident_any = ident_any


def grade_run(r: Run, s: Shape, extra: dict) -> Grade:
    g = Grade(r, s)
    g.check("case_completed", r.rc == 0 and r.done, f"rc {r.rc}, done {r.done}")
    g.durability()
    g.written_values()
    g.latch()
    c = r.case
    n_rec = sum(1 for rid in s.recs if rid != 0x01 and not 0x12 <= rid < 0x1A and not 0x20 <= rid < 0x30)
    if c == "K1_single_change_converges":
        g.converged("end")
        g.value_in_slot("end", 0x50)
    elif c == "K2_change_during_record_write":
        g.converged("end")
        g.value_in_slot("end", 0x50)
        w = [o for o in g.ops() if o["op"] == 1 and o["rid"] == 0x50 and o["res"] == "done"]
        last = [v for _c, rid, v in g.changes() if rid == 0x50]
        ok = len(w) >= 2 and last and bytes.fromhex(w[-1]["w"])[8:12] == last[-1]
        g.check("taint_rewrites:0x50", ok, f"{len(w)} completed writes of 0x50; the last carries "
                                           f"{bytes.fromhex(w[-1]['w'])[8:12].hex() if w else None}")
    elif c == "K3_two_changes_one_debounce":
        g.value_in_slot("end", 0x50)
        w = [o for o in g.ops() if o["op"] == 1 and o["rid"] == 0x50]
        g.check("coalesced:0x50", len(w) == 1, f"{len(w)} writes of 0x50 for two changes in one window")
    elif c == "K4_second_record_in_flight":
        g.value_in_slot("end", 0x50)
        g.value_in_slot("end", 0x51)
    elif c == "K5_change_on_the_done_edge":
        g.value_in_slot("end", 0x50, "same_edge_change_survives@end:0x50")
    elif c == "K6b_restore_after_cut":
        v, _ = g.ans("ptof0.value")
        valid, _ = g.ans("ptof0.valid")
        cut = extra.get("cut_slots", {}).get(0x50)
        ok = valid == 1 and cut is not None and v == int.from_bytes(cut, "big") and v != 6000001
        g.check("power_cut_loses_only_unsaved:0x50", ok,
                f"restored {v} (valid {valid}), the cut's newest verified slot {cut.hex() if cut else None}, "
                f"the unsaved value 6000001")
    elif c == "K7b_restore_after_ack":
        v, _ = g.ans("ptof0.value")
        valid, _ = g.ans("ptof0.valid")
        g.check("value_restored:0x50", valid == 1 and v == 7000001, f"restored {v} valid {valid}")
    elif c == "K8_record_write_error_retried":
        g.converged("end")
        g.value_in_slot("end", 0x50)
        errs = [o for o in g.ops() if o["rid"] == 0x50 and o["res"] == "err"]
        g.check("retry_converges:0x50", len(errs) >= 1 and g.checks["value_in_slot@end:0x50"][0],
                f"{len(errs)} failed operations on 0x50, then committed")
    elif c == "K9_record_write_given_up":
        o = r.obs.get("end", {})
        got = g.tag_slots("end").get(0x50)
        ok = o.get("alarm") == 1 and o.get("backed") == 0 and got != (9000001).to_bytes(4, "big")
        g.check("giveup_revokes:0x50", ok, f"alarm {o.get('alarm')} backed {o.get('backed')} slot "
                                           f"{got.hex() if got else None}")
    elif c == "K10_name_change_converges":
        g.converged("end")
        g.value_in_slot("end", 0x80)
    elif c == "K11_name_latch_waits_for_the_program":
        g.value_in_slot("end", 0x80)
    elif c == "K12_map_change_converges":
        g.converged("end")
        g.value_in_slot("end", 0x70)
    elif c == "K13_binding_and_d3_share_the_port":
        sl = g.tag_slots("end")
        bind = sl.get(0x20)
        ok = bind is not None and bind[0] & 1 == 1 and sl.get(0x50) == (1300013).to_bytes(4, "big")
        g.check("both_records_committed", ok, f"binding {bind.hex() if bind else None}, 0x50 "
                                              f"{sl.get(0x50).hex() if sl.get(0x50) else None}")
    elif c == "K14_identify_is_not_persisted":
        o = r.obs.get("end", {})
        b0 = r.obs.get("boot", {})
        w = [x for x in g.ops() if x["op"] == 1 and (x["rid"] < 0x20 or x["rid"] >= 0x30)]
        ok = not w and o.get("dirty_count") == 0 and o.get("pend") == 0 and o.get("programs") == b0.get("programs")
        g.check("identify_never_persisted", ok, f"{len(w)} record writes, dirty {o.get('dirty_count')}, "
                                                f"pend {o.get('pend')}, flash programs {b0.get('programs')} -> "
                                                f"{o.get('programs')}")
    elif c.startswith("V1b"):
        cut = extra["cut_slots"]
        saved = {rid: v for rid, v in cut.items() if rid in g.d3_rids()}
        # CLEARED FIRST (issue #70's vacuity trap), every row, name and map set,
        # by the bridge's peeks: the rows and the map sets when the D3 walk
        # starts, the names when its pass 1 starts (after the image walk)
        pre, p1 = r.snaps.get("prerestore"), r.snaps.get("pass1")
        bad = []
        if pre is None or p1 is None:
            bad = ["no snapshot"]
        else:
            bad = [m for m in g.mismatches(pre, {}) if not 0x80 <= int(m[:4], 16)]
            bad += [m for m in g.mismatches(p1, {}) if 0x80 <= int(m[:4], 16)]
        g.check("rows_cleared_before_restore@boot", not bad,
                f"{len(bad)} rows, names or map sets not at their reset or image default before the restore "
                f"{bad[:3]}")
        # every saved record, value AND valid flag, at the D3 terminal
        term = r.snaps.get("terminal")
        for rid, payload in sorted(saved.items()):
            got = g.snap_value(term, rid) if term else None
            want = g.want_of(rid, payload)
            ok = got == want and (not isinstance(want, bytes) or rid < 0x80 or want != s.names[rid - 0x80])
            g.check(f"value_restored:{rid:#04x}", ok,
                    (f"{show(got, want)}" if got != want else f"live equals the slot, {len(payload)} bytes")
                    + (" (value, valid)" if scalar_of(rid) else ""))
        # and every record the slot does NOT hold is still at its default
        rest = [m for m in g.mismatches(term, saved) if int(m[:4], 16) not in saved] if term else ["no snapshot"]
        g.check("unsaved_records_keep_defaults@restored", term is not None and not rest,
                f"{len(rest)} unsaved records off their defaults {rest[:3]}")
        #! against the value V1a SET, not against the slot: the check a
        #! build that saves nothing (the tracked glue) must fail
        pv, _ = g.ans("post.ptof0.value")
        pvalid, _ = g.ans("post.ptof0.valid")
        g.check("set_value_survives_power_cycle:0x50", pvalid == 1 and pv == 1500000,
                f"restored {pv} valid {pvalid}, set 1500000")
        # the controller's view: GET answers for the rows a controller reads
        gets = []
        for tag, rid in (("cfg", 0x00), ("rate", 0x02), ("clks", 0x0A), ("fmti0", 0x30),
                         ("fmto0", 0x40), ("ptof0", 0x50), ("ptoflast", 0x50 + s.params["N_STREAM_OUT_P"] - 1)):
            v, _ = g.ans(f"post.{tag}.value")
            valid, _ = g.ans(f"post.{tag}.valid")
            want = g.want_of(rid, saved[rid]) if rid in saved else (None, 0)
            if (want[1] == 1 and (v, valid) != want) or (want[1] == 0 and valid != 0):
                gets.append(f"{tag} {v} valid {valid}, want {want}")
        g.check("get_answers_restored_values@restored", not gets, "; ".join(gets) if gets else
                "cfg, rate, clock source, fmti0, fmto0, ptof0 and the last ptof answered as saved")
        for rid, tag in ((0x80, "name0"), (0x80 + s.params["N_NAME_P"] - 1, "namelast")):
            want = cut.get(rid)
            after = g.name_of(f"after.{tag}")
            g.check(f"restored_name_survives_first_command:{rid:#04x}", want is not None and after == want,
                    f"after the first command {after[:24] if after else None}")
        g.enable_after_terminal()
        b = g.boot()
        g.check("entity_enabled_after_restore@boot",
                b.get("enable", 0) > 0 and b.get("d3_done", 0) > 0 and b.get("enable") > b.get("d3_done"),
                f"enabled at {b.get('enable')}, D3 restore done at {b.get('d3_done')}, restore done at "
                f"{b.get('restore_done')}")
        o = r.obs.get("restored", {})
        b0 = r.obs.get("boot", {})
        w = [x for x in g.ops() if x["op"] == 1 and (x["rid"] < 0x20 or x["rid"] >= 0x30)]
        g.check("restore_sets_no_dirty@boot", not w and o.get("dirty_count") == 0 and
                o.get("erases") == b0.get("erases"),
                f"{len(w)} record writes after the restore, dirty {o.get('dirty_count')}, flash erases "
                f"{b0.get('erases')} -> {o.get('erases')}")
        # EXACT counts: applied = the records the slot holds, blank = the rest
        g.check("restore_counts@boot", o.get("rs_ref") == 0 and o.get("rs_app") == len(saved)
                and o.get("rs_blank") == n_rec - len(saved),
                f"applied {o.get('rs_app')} refused {o.get('rs_ref')} blank {o.get('rs_blank')} of {n_rec}; the "
                f"slot holds {len(saved)}")
    elif c == "V1a_set_everything":
        g.converged("cut")
        # every record the case changed is in the newest verified slot: the
        # per-group trigger-deletion killers
        for rid in sorted({rid for _c, rid, _v in g.changes() if rid in g.d3_rids()}):
            g.value_in_slot("cut", rid, f"value_in_slot@cut:{rid:#04x}")
    elif c == "V2_refused_rate":
        valid, _ = g.ans("post.rate.valid")
        o = r.obs.get("restored", {})
        g.check("refused_value_not_applied:0x02", valid == 0 and o.get("rs_ref", 0) >= 1,
                f"rate row valid {valid}, refused {o.get('rs_ref')}")
    elif c == "V3_refused_map_for_a_removed_cluster":
        o = r.obs.get("restored", {})
        cls = s.recs[0x70][2] // 8
        want = map_bytes(default_out_maps(s, 0), cls).hex()
        g.check("refused_group_falls_back_to_default:0x70",
                o.get("maps_out", [None])[0] == want and o.get("rs_ref", 0) >= 1,
                f"live OUT0 equals the default {o.get('maps_out', [None])[0] == want}, refused {o.get('rs_ref')}")
    elif c == "V4_refused_configuration_index":
        valid, _ = g.ans("post.cfg.valid")
        o = r.obs.get("restored", {})
        g.check("refused_value_not_applied:0x00", valid == 0 and o.get("rs_ref", 0) >= 1,
                f"cfg row valid {valid}, refused {o.get('rs_ref')}")
    elif c == "V5_record_corrupted_after_the_load":
        v, _ = g.ans("post.ptof0.valid")
        f, _ = g.ans("post.ptof1.value")
        fv, _ = g.ans("post.ptof1.valid")
        o = r.obs.get("restored", {})
        g.check("corrupted_record_refused:0x50", v == 0 and o.get("rs_ref", 0) >= 1,
                f"ptof0 valid {v}, refused {o.get('rs_ref')}")
        g.check("other_records_still_applied:0x51", fv == 1 and f == 1600000, f"ptof1 {f} valid {fv}")
    elif c == "V6b_restore_coupled_pair":
        v, _ = g.ans("post.fmto0.value")
        valid, _ = g.ans("post.fmto0.valid")
        o = r.obs.get("restored", {})
        cut = extra["cut_slots"]
        ok = valid == 1 and cut.get(0x40) is not None and v == int.from_bytes(cut[0x40], "big") and \
            cut.get(0x70) is not None and o.get("maps_out", [None])[0] == cut[0x70].hex()
        g.check("coupled_pair_restored", ok, f"fmto0 {v} valid {valid}; OUT0 set matches the slot "
                                             f"{cut.get(0x70) is not None and o.get('maps_out', [None])[0] == cut[0x70].hex()}")
    elif c == "V8_orphaning_format_reverted":
        v, _ = g.ans("post.fmto0.value")
        valid, _ = g.ans("post.fmto0.valid")
        live = v if valid == 1 else s.def_fmt_out[0]
        ch = (live >> 22) & 0x3FF if live is not None else 0
        o = r.obs.get("restored", {})
        mo = bytes.fromhex(o.get("maps_out", [""])[0] or "")
        maps = [struct.unpack_from(">HHHH", mo, 8 * k) for k in range(len(mo) // 8)]
        orphan = [m for m in maps if m[0] == 0 and m[1] != 0xFFFF and m[1] >= ch]
        g.check("no_orphaned_mapping_after_restore", not orphan,
                f"stream 0 format {live:#x} ({ch} channels), {len(orphan)} orphaned mappings")
        g.check("format_reverted:0x40", live == s.def_fmt_out[0], f"fmto0 {live:#x}")
    elif c == "V9_refused_maps_revert_their_formats":
        o = r.obs.get("restored", {})
        cls = s.recs[0x70][2] // 8
        want = map_bytes(default_out_maps(s, 0), cls).hex()
        v, _ = g.ans("post.fmto0.value")
        valid, _ = g.ans("post.fmto0.valid")
        live = v if valid == 1 else s.def_fmt_out[0]
        pv, _ = g.ans("post.ptof0.value")
        pvalid, _ = g.ans("post.ptof0.valid")
        #! a refused set falls back PER RECORD: the other record the slot
        #! holds stays applied, and nothing is rolled back
        g.check("refused_group_falls_back_to_default:0x70",
                o.get("maps_out", [None])[0] == want and live == s.def_fmt_out[0] and pvalid == 1
                and pv == 1500000 and o.get("d3_rb") == 0,
                f"live OUT0 equals the default {o.get('maps_out', [None])[0] == want}, fmto0 {live:#x}, ptof0 "
                f"{pv} valid {pvalid}, rolled back {o.get('d3_rb')}")
    elif c == "V7_names_only":
        want = extra["crafted"][0x80]
        after = g.name_of("after.name0")
        post = g.name_of("post.name0")
        g.check("value_restored:0x80", post == want, f"restored {post[:24] if post else None}")
        g.check("restored_name_survives_first_command:0x80", after == want,
                f"after the first command {after[:24] if after else None}")
        o = r.obs.get("restored", {})
        g.check("blank_is_both_walks@boot", o.get("blank") == 0 and o.get("restore_done") == 1,
                f"a name came back and no binding did: blank {o.get('blank')}, done {o.get('restore_done')}")
    elif c == "V11_torn_read_restores_nothing":
        valid, _ = g.ans("post.ptof0.valid")
        o = r.obs.get("restored", {})
        #! pass 0 refuses a slot torn AT REST before anything is applied, so
        #! nothing is applied and nothing needs rolling back
        g.check("torn_walk_applies_nothing@boot",
                valid == 0 and o.get("restore_fail") == 1 and o.get("d3_fail") == 1 and o.get("rs_app") == 0
                and o.get("d3_rb") == 0,
                f"ptof0 valid {valid} (its record was read whole before the torn one), restore fail "
                f"{o.get('restore_fail')}, D3 fail {o.get('d3_fail')}, applied {o.get('rs_app')}, rolled back "
                f"{o.get('d3_rb')}")
    elif c == "V10_blank_first_boot":
        o = r.obs.get("restored", {})
        valid, _ = g.ans("post.ptof0.valid")
        g.check("blank_boot_applies_nothing@boot", o.get("rs_blank") == n_rec and o.get("rs_app") == 0 and
                valid == 0 and o.get("blank") == 1,
                f"blank {o.get('rs_blank')} of {n_rec}, applied {o.get('rs_app')}, ptof0 valid {valid}, "
                f"status blank {o.get('blank')}")
        #! the ERASED-RECORD CONTROL of seam S1: every record, binding and D3,
        #! is an erased header the device delivered whole (UNFRAMED): no walk
        #! fails, no cause is reported
        g.check("blank_boot_is_not_a_failure@boot",
                o.get("restore_fail") == 0 and o.get("d3_fail") == 0 and o.get("mgr_fail") == 0
                and o.get("d3_cause") == 0 and o.get("mgr_cause") == 0 and o.get("restore_done") == 1,
                f"restore fail {o.get('restore_fail')} (D3 {o.get('d3_fail')}, binding {o.get('mgr_fail')}), "
                f"causes D3 {o.get('d3_cause')} binding {o.get('mgr_cause')}, done {o.get('restore_done')}")
    elif c == "K4g_second_group_in_flight":
        g.converged("end")
        g.value_in_slot("end", 0x50)
        g.value_in_slot("end", 0x0A)
    elif c == "K15_binding_on_the_d3_grant_cycle":
        g.converged("end")
        sl = g.tag_slots("end")
        bind = sl.get(0x20)
        ok = bind is not None and bind[0] & 1 == 1 and sl.get(0x50) == (1500015).to_bytes(4, "big")
        g.check("both_records_committed", ok,
                f"binding {bind.hex() if bind else None}, 0x50 {sl.get(0x50).hex() if sl.get(0x50) else None}, "
                f"grant-cycle collisions {g.boot().get('collisions')}")
    elif c == "K16_map_set_larger_than_its_record":
        over = r.obs.get("over", {})
        size = r.notes.get("over_size", {}).get("value")
        chg = [cy for cy, rid, _v in g.changes() if rid == 0x70]
        first = chg[0] if chg else None
        ocyc = over.get("cycle", 0)
        w = [o for o in g.ops() if o["op"] == 1 and o["rid"] == 0x70 and o["res"] == "done"
             and first is not None and first < o["gnt"] <= ocyc]
        cls = s.recs[0x70][2] // 8
        ok = (size is not None and size > cls and over.get("pend") == 1 and over.get("d3_alarm") == 0
              and over.get("backed") == 1 and not w)
        g.check("oversized_set_stays_pending@over", ok,
                f"{size} mappings on a {cls}-entry record; pend {over.get('pend')}, D3 alarm "
                f"{over.get('d3_alarm')}, backed {over.get('backed')}, WRITEs of 0x70 {len(w)}")
        g.converged("end")
        g.value_in_slot("end", 0x70)
    elif c == "K17a_cut_during_record_write":
        nb = r.notes.get("cut_write_bytes", {}).get("value")
        g.check("cut_inside_the_write@cut", nb is not None and 0 < nb < 12,
                f"the WRITE of 0x50 had taken {nb} of 12 bytes at the cut")
    elif c == "K18a_cut_inside_the_debounce":
        o = r.obs.get("cut", {})
        w = [x for x in g.ops() if x["op"] == 1 and x["rid"] == 0x50 and x["res"] == "done"
             and bytes.fromhex(x["w"])[8:12] == (1818002).to_bytes(4, "big")]
        g.check("pending_at_the_cut@cut", o.get("pend") == 1 and o.get("d3_unfl") == 1 and not w,
                f"pend {o.get('pend')}, D3 unflushed {o.get('d3_unfl')}, WRITEs of the unsaved value {len(w)}")
    elif c in ("K17b_restore_after_cut_in_write", "K18b_restore_after_cut_in_debounce"):
        unsaved = 1717002 if c.startswith("K17") else 1818002
        v, _ = g.ans("ptof0.value")
        valid, _ = g.ans("ptof0.valid")
        cut = extra.get("cut_slots", {}).get(0x50)
        ok = valid == 1 and cut is not None and v == int.from_bytes(cut, "big") and v != unsaved
        g.check("power_cut_loses_only_unsaved:0x50", ok,
                f"restored {v} (valid {valid}), the cut's newest verified slot {cut.hex() if cut else None}, "
                f"the unsaved value {unsaved}")
    # ================= THE RESTORE TRANSACTION (page section 8.6) ==========
    elif c in ("V12_abort_pass0_early", "V13_abort_pass0_late"):
        # pass 0 applied nothing: defaults, done and fail, NOT rolled back
        g.contained(0, "abort_applies_nothing@terminal")
        g.check("abort_premise@terminal", r.obs.get("terminal", {}).get("rs_app") == 0
                and g.boot_evt("cause") in (1, 2) and g.boot_evt("rollback") == 0,
                f"applied {r.obs.get('terminal', {}).get('rs_app')}, abort cause {g.boot_evt('cause')}, "
                f"roll-back at {g.boot_evt('rollback')}")
        g.enable_after_terminal()
        g.no_restore_write_after()
        g.served_after_recovery((0, 0))
        g.converged("recovered")
        g.value_in_slot("recovered", 0x50, "later_change_persists@recovered")
    elif c in PASS1_ROLLBACK:
        # pass 1 had applied values before the fault: ROLLED BACK to defaults
        # that are PROVEN (every row reset, every name the re-walked image's)
        g.contained(1)
        o = r.obs.get("terminal", {})
        g.check("rollback_premise@terminal", o.get("rs_app", 0) >= 1 and g.boot_evt("rollback") > 0 and
                g.boot_evt("cause") in PASS1_ROLLBACK[c],
                f"{o.get('rs_app')} records applied before the fault, roll-back at {g.boot_evt('rollback')}, "
                f"abort cause {g.boot_evt('cause')} (want {PASS1_ROLLBACK[c]})")
        if PASS1_ROLLBACK[c] == (6,) and c != "V20c_desc_error_in_the_map_revert":
            #! a rule or default that could not be FETCHED is no refused value
            g.check("descriptor_fault_is_not_a_refusal@terminal", o.get("rs_ref") == 0,
                    f"refused {o.get('rs_ref')} at the terminal, abort cause {g.boot_evt('cause')}")
        if c in ("V20b_desc_error_once_after_apply", "V20c_desc_error_in_the_map_revert",
                 "V20d_desc_error_in_the_final_revert"):
            g.check("descriptor_fault_premise@terminal",
                    0 < g.boot_evt("desc_err") <= g.boot_evt("abort"),
                    f"the descriptor memory answered an error beat at {g.boot_evt('desc_err')}, the writer "
                    f"aborted at {g.boot_evt('abort')}")
        if c in ("V21_desc_late_after_apply", "V21b_desc_debt_outlasts_the_store"):
            acc, beat = g.boot_evt("desc_delay_acc"), g.boot_evt("desc_delay_beat")
            ab, rb_end = g.boot_evt("abort"), g.boot_evt("rb_end")
            #! the store's own watchdog answered first (the abort), the late
            #! burst came after it, and the owners left reset only after it
            g.check("rollback_waited_for_the_memory@terminal",
                    0 < acc < ab < beat < rb_end and ab - acc >= 4096,
                    f"request accepted at {acc}, the store's error answer aborted the restore at {ab} "
                    f"({ab - acc} cycles), the late burst came at {beat}, the owners left reset at {rb_end}")
        g.enable_after_terminal()
        g.no_restore_write_after()
        g.served_after_recovery((0, 0))
        g.converged("recovered")
        g.value_in_slot("recovered", 0x50, "later_change_persists@recovered")
        g.saved_state_kept(extra)
    # ================= HEADER TRANSPORT FAULTS (revision c, seam S1) ========
    elif c in HEADER_PASS0 or c == "H8_header_error_sole_saved_record":
        # the device error is met in pass 0: nothing applied, DEFAULTS
        g.contained(0, "header_fault_contained@terminal")
        o = r.obs.get("terminal", {})
        g.check("header_fault_premise@terminal", o.get("rs_app") == 0 and g.boot_evt("cause") == 2
                and g.boot_evt("rollback") == 0,
                f"applied {o.get('rs_app')}, abort cause {g.boot_evt('cause')} (a device error), roll-back at "
                f"{g.boot_evt('rollback')}")
        #! a failed restore is never read as a clean blank boot, even when the
        #! one record lost was the only one saved
        g.check("failure_not_blank@terminal", o.get("restore_fail") == 1 and o.get("d3_fail") == 1
                and o.get("blank") == 0,
                f"restore fail {o.get('restore_fail')}, D3 fail {o.get('d3_fail')}, blank {o.get('blank')}")
        g.enable_after_terminal()
        g.no_restore_write_after()
        g.served_after_recovery((0, 0))
        g.converged("recovered")
        g.value_in_slot("recovered", 0x50, "later_change_persists@recovered")
        if c != "H8_header_error_sole_saved_record":
            g.saved_state_kept(extra)
    elif c == "V17_rollback_cannot_validate":
        g.closed_dark()
    elif c in ("V20_desc_error_after_apply", "V21c_desc_debt_outlasts_the_deadline"):
        # a descriptor fault after an application: the roll-back cannot prove
        # its image (the memory still failing, or its late burst outlasting
        # the deadline), so the restore ends CLOSED, never enabled
        g.closed_dark()
        g.check("descriptor_fault_closes@terminal", g.boot_evt("cause") == 6 and g.boot_evt("rollback") > 0,
                f"abort cause {g.boot_evt('cause')}, roll-back at {g.boot_evt('rollback')}")
        if c.startswith("V21c"):
            term, beat, ab = g.boot_evt("terminal"), g.boot_evt("desc_delay_beat"), g.boot_evt("abort")
            g.check("closed_before_the_late_burst@terminal",
                    0 < ab < term < beat and term - ab <= RS_TMO + 1000,
                    f"aborted at {ab}, CLOSED at {term} ({term - ab} cycles), the late burst came at {beat}")
    elif c in ("V22_desc_fails_before_boot", "V22b_image_unproven_simple_records"):
        # the image cannot be proven at the start: CLOSED, nothing applied,
        # nothing refused, never a successful restore
        g.closed_dark()
        o = r.obs.get("terminal", {})
        g.check("closed_when_image_unproven@recovered",
                g.boot_evt("cause") == 7 and o.get("rs_app") == 0 and o.get("rs_ref") == 0
                and o.get("desc_valid") == 0 and o.get("d3_closed") == 1,
                f"abort cause {g.boot_evt('cause')}, applied {o.get('rs_app')}, refused {o.get('rs_ref')}, "
                f"image validated {o.get('desc_valid')}, closed {o.get('d3_closed')}")
    elif c == "V11b_torn_in_pass1_rolls_back":
        g.contained(1)
        valid, _ = g.ans("post.ptof0.valid")
        g.check("torn_in_pass1_leaves_no_partial_restore@restored", valid == 0,
                f"ptof0 valid {valid} after the pass-1 tear (0x50 had been applied before it)")
        g.enable_after_terminal()
        g.no_restore_write_after()
    # ================= DEADLINES (page section 8.8) ==========================
    elif c in ("W1_silent_pass0", "W4_silent_pass1", "W7_silent_pass1_last_name"):
        h = g.hold()
        g.check("held_premise@terminal", h.get("active") == 1 and h.get("released") == 0 and g.boot_evt("cause") == 3,
                f"memory read of {h.get('rid', 0):#04x} in pass {h.get('pass')} held from {h.get('start')}, "
                f"released {h.get('released')}, abort cause {g.boot_evt('cause')}")
        g.terminal_bounded(h.get("start", 0), RS_TMO + 10000)
        g.contained(0 if c.startswith("W1") else 1)
        g.enable_after_terminal()
        g.no_restore_write_after()
        g.served_after_recovery((0, 0))
        # the port serves the abandoned read for ever: the later change reads
        # pending, and the status never reads durable over it
        o = r.obs.get("recovered", {})
        chg = [cy for cy, rid, _v in g.changes() if rid == 0x50]
        g.check("later_change_reported@recovered", bool(chg) and o.get("pend") == 1 and o.get("port_busy") == 1,
                f"a SET of 0x50 at {chg[:1]}, pend {o.get('pend')}, port busy {o.get('port_busy')}")
    elif c in ("W2_late_pass0_before_deadline", "W5_late_pass1_before_deadline"):
        h = g.hold()
        g.check("held_premise@terminal", h.get("released") == 1 and h.get("wd_max", 0) >= RS_TMO - 64
                and g.boot_evt("cause") == 0,
                f"held from {h.get('start')} to {h.get('end')}, the watchdog reached {h.get('wd_max')} of {RS_TMO}, "
                f"abort cause {g.boot_evt('cause')}")
        cut = extra.get("cut_slots", {})
        saved = {rid: v for rid, v in cut.items() if rid in g.d3_rids()}
        bad = g.mismatches(r.snaps.get("terminal"), saved)
        o = r.obs.get("terminal", {})
        g.check("restore_complete@terminal", not bad and o.get("d3_done") == 1 and o.get("d3_fail") == 0,
                f"{len(bad)} records not as saved {bad[:2]}, D3 done {o.get('d3_done')} fail {o.get('d3_fail')}")
        g.enable_after_terminal()
        g.no_restore_write_after()
        g.converged("recovered")
        g.value_in_slot("recovered", 0x50, "later_change_persists@recovered")
    elif c in ("W3_late_pass0_after_deadline", "W6_late_pass1_after_deadline"):
        h = g.hold()
        ab = g.boot_evt("abort")
        g.check("held_premise@terminal", h.get("released") == 1 and g.boot_evt("cause") == 3 and ab > 0
                and 0 <= h.get("end", 0) - ab <= 10,
                f"held from {h.get('start')}, the writer aborted at {ab}, the response came at {h.get('end')}")
        g.contained(0 if c.startswith("W3") else 1)
        g.enable_after_terminal()
        g.no_restore_write_after()
        g.served_after_recovery((0, 0))
        # the late response ENDED the drained read, so the port is free again
        g.converged("recovered")
        g.value_in_slot("recovered", 0x50, "later_change_persists@recovered")
    elif c in ("W8_map_face_silent_pass1", "W9_judge_silent_pass1", "W10_edit_face_silent_pass1"):
        f = [e for e in r.evts if e["k"] == "face"]
        f = f[0] if f else {}
        g.check("face_premise@terminal", f.get("done") == 1 and g.boot_evt("cause") == 3,
                f"face {f.get('face')} silent from {f.get('start')}, healed {f.get('done')}, abort cause "
                f"{g.boot_evt('cause')}")
        g.terminal_bounded(f.get("start", 0), RS_TMO + 10000)
        g.contained(1)
        g.enable_after_terminal()
        g.no_restore_write_after()
        g.served_after_recovery((0, 0))
        g.converged("recovered")
        g.value_in_slot("recovered", 0x50, "later_change_persists@recovered")
    elif c in ("W11_r217_first_read_late", "W12_r218_read_late_after_apply"):
        h = g.hold()
        g.check("held_premise@terminal", h.get("released") == 1 and h.get("end", 0) - h.get("start", 0) >= 3000000
                and g.boot_evt("cause") == 3,
                f"held from {h.get('start')} to {h.get('end')}, abort cause {g.boot_evt('cause')}")
        g.terminal_bounded(h.get("start", 0), RS_TMO + 10000)
        g.contained(0 if c.startswith("W11") else 1)
        g.enable_after_terminal()
        g.no_restore_write_after()
        g.served_after_recovery((0, 0))
        g.converged("recovered")
        g.value_in_slot("recovered", 0x50, "later_change_persists@recovered")
    elif c == "W13_binding_walk_silent":
        # the binding walk's first read never answers: its own deadline ends
        # the walk failed with nothing preloaded, the D3 walk meets the
        # quarantined port and ends at its deadline on defaults, and commands
        # are served; the port stays quarantined, the later SET pending
        h = g.hold()
        b = g.boot()
        o = r.obs.get("terminal", {})
        mgr = b.get("mgr_done", 0)
        g.check("held_premise@terminal", h.get("active") == 1 and h.get("released") == 0
                and b.get("m0_abort", 0) > 0,
                f"binding read held from {h.get('start')}, released {h.get('released')}, abandoned to the drain "
                f"at {b.get('m0_abort')}")
        g.check("binding_walk_bounded@terminal", mgr > 0 and h.get("start", 0) > 0
                and mgr - h.get("start", 0) <= RS_TMO + 100,
                f"silence from {h.get('start')}, the binding walk's terminal at {mgr} (bound {RS_TMO} + 100)")
        g.check("binding_walk_failed@terminal", o.get("mgr_fail") == 1 and o.get("mgr_cause") == 3
                and not g.preloads() and o.get("restore_fail") == 1,
                f"binding fail {o.get('mgr_fail')} cause {o.get('mgr_cause')}, preloads {g.preloads()[:2]}, "
                f"restore fail {o.get('restore_fail')}")
        g.terminal_bounded(h.get("start", 0), 2 * RS_TMO + 10000)
        g.contained(0)
        g.enable_after_terminal()
        g.no_restore_write_after()
        g.served_after_recovery((0, 0))
        o2 = r.obs.get("recovered", {})
        chg = [cy for cy, rid, _v in g.changes() if rid == 0x50]
        g.check("persistence_quarantined@recovered", bool(chg) and o2.get("pend") == 1
                and o2.get("port_busy") == 1,
                f"a SET of 0x50 at {chg[:1]} served, pend {o2.get('pend')}, port busy {o2.get('port_busy')}: the "
                f"device never ended the abandoned read")
    elif c == "W13b_binding_late_before_deadline":
        h = g.hold()
        o = r.obs.get("terminal", {})
        g.check("held_premise@terminal", h.get("released") == 1 and h.get("m0_wd_max", 0) >= RS_TMO - 64
                and o.get("mgr_cause") == 0,
                f"held from {h.get('start')} to {h.get('end')}, the binding deadline count reached "
                f"{h.get('m0_wd_max')} of {RS_TMO}, binding cause {o.get('mgr_cause')}")
        pre = g.preloads()
        mgr = g.boot_evt("mgr_done")
        g.check("binding_restored@terminal", o.get("mgr_fail") == 0 and any(s == 0 for _c, s in pre)
                and all(cy <= mgr for cy, _s in pre),
                f"binding fail {o.get('mgr_fail')}, preloads {pre[:2]}, the binding walk ended at {mgr}")
        g.restore_complete(extra)
        g.enable_after_terminal()
        g.no_restore_write_after()
        g.converged("recovered")
        g.value_in_slot("recovered", 0x50, "later_change_persists@recovered")
    elif c in ("W13c_binding_late_after_deadline", "W15_binding_answer_after_enable"):
        h = g.hold()
        b = g.boot()
        o = r.obs.get("terminal", {})
        ab = b.get("m0_abort", 0)
        if c.startswith("W13c"):
            g.check("held_premise@terminal", h.get("released") == 1 and ab > 0 and 0 <= h.get("end", 0) - ab <= 10,
                    f"held from {h.get('start')}, abandoned at {ab}, the response came at {h.get('end')}")
            g.restore_complete(extra)
        else:
            g.check("held_premise@terminal", h.get("released") == 1 and ab > 0
                    and h.get("end", 0) > b.get("enable", 0) > 0,
                    f"held from {h.get('start')}, abandoned at {ab}, the entity enabled at {b.get('enable')}, "
                    f"the response came at {h.get('end')}")
            #! the drained read kept the port from the D3 walk: it ended at
            #! its own deadline, on defaults
            g.contained(0)
            g.served_after_recovery((0, 0))
        g.check("binding_walk_failed@terminal", o.get("mgr_fail") == 1 and o.get("mgr_cause") == 3
                and o.get("restore_fail") == 1,
                f"binding fail {o.get('mgr_fail')} cause {o.get('mgr_cause')}, restore fail {o.get('restore_fail')}")
        #! the late response was drained: no binding reaches the listener
        g.check("no_preload_after_the_binding_terminal@recovered", not g.preloads(),
                f"preloads {g.preloads()[:3]}, the binding walk ended at {b.get('mgr_done')}")
        g.enable_after_terminal()
        g.no_restore_write_after()
        #! the device ended the abandoned read, so the port serves again
        g.converged("recovered")
        g.value_in_slot("recovered", 0x50, "later_change_persists@recovered")
    elif c == "W16_binding_header_device_error":
        o = r.obs.get("terminal", {})
        g.check("binding_walk_failed@terminal", o.get("mgr_fail") == 1 and o.get("mgr_cause") == 2
                and not g.preloads() and o.get("restore_fail") == 1 and o.get("blank") == 0,
                f"binding fail {o.get('mgr_fail')} cause {o.get('mgr_cause')} (a device error on the header), "
                f"preloads {g.preloads()[:2]}, restore fail {o.get('restore_fail')}, blank {o.get('blank')}")
        g.restore_complete(extra)
        g.enable_after_terminal()
        g.no_restore_write_after()
        v, _ = g.ans("rec.ptof0.value")
        valid, _ = g.ans("rec.ptof0.valid")
        g.check("command_served_after_recovery@recovered", (v, valid) == (1500000, 1),
                f"GET after recovery answered {v} valid {valid}, want the restored (1500000, 1)")
        g.converged("recovered")
        g.value_in_slot("recovered", 0x50, "later_change_persists@recovered")
    elif c == "W14_enable_requested_before_the_restore":
        b = g.boot()
        g.check("early_request_premise@terminal", 0 < b.get("fw_enable", 0) < b.get("restore_done", 0),
                f"the enable requested at {b.get('fw_enable')}, restore done at {b.get('restore_done')}")
        g.restore_complete(extra)
        g.enable_after_terminal()
        g.no_restore_write_after()
        g.converged("recovered")
        g.value_in_slot("recovered", 0x50, "later_change_persists@recovered")
    elif c == "V21d_desc_slow_within_the_store_bound":
        acc, beat = g.boot_evt("desc_delay_acc"), g.boot_evt("desc_delay_beat")
        g.check("slow_premise@terminal", 0 < acc < beat and 3900 <= beat - acc < 4096 and g.boot_evt("cause") == 0,
                f"request accepted at {acc}, its first beat at {beat} ({beat - acc} cycles, the store's own watchdog "
                f"4096), abort cause {g.boot_evt('cause')}")
        g.restore_complete(extra)
        g.enable_after_terminal()
        g.no_restore_write_after()
        g.converged("recovered")
        g.value_in_slot("recovered", 0x50, "later_change_persists@recovered")
    elif c == "V2b_refused_clock_source":
        valid, _ = g.ans("post.clks.valid")
        o = r.obs.get("restored", {})
        g.check("refused_value_not_applied:0x0a", valid == 0 and o.get("rs_ref", 0) >= 1,
                f"clock source row valid {valid}, refused {o.get('rs_ref')}")
        #! the rule WAS fetched: a refused value is per record, never a failure
        g.check("value_refusal_is_not_a_failure@restored", o.get("d3_fail") == 0 and o.get("d3_rb") == 0
                and o.get("d3_cause") == 0 and o.get("restore_fail") == 0,
                f"D3 fail {o.get('d3_fail')}, rolled back {o.get('d3_rb')}, cause {o.get('d3_cause')}, restore "
                f"fail {o.get('restore_fail')}")
    elif c == "V23_late_desc_beats_in_service":
        _v1, e1 = g.ans("late.locate")
        acc, beat = g.boot_evt("desc_delay_acc"), g.boot_evt("desc_delay_beat")
        g.check("late_premise@restored", e1 == 1 and 0 < acc < beat,
                f"the first locate answered err {e1} (the store's own watchdog), its burst accepted at {acc} came at "
                f"{beat}")

        def served(tag: str) -> tuple:
            _v, e = g.ans(f"{tag}.locate")
            lane, _ = g.ans(f"{tag}.lane0")
            return e, (lane >> 48) if lane is not None else None
        e3, typ3 = served("third")
        #! the third locate's request is PRESENTED while the late burst is owed
        #! (the second fails at once: the pinned store's watchdog is not re-armed
        #! after a fetch timed out); it must get its own STREAM_INPUT, never the
        #! late STREAM_OUTPUT burst's bytes
        e2, typ2 = served("next")
        g.check("late_beats_never_served@restored",
                all(e == 1 or (e == 0 and typ == 0x0005) for e, typ in ((e2, typ2), (e3, typ3)))
                and e3 == 0 and typ3 == 0x0005,
                f"second locate err {e2} type {typ2 if typ2 is None else hex(typ2)}; third locate err {e3} type "
                f"{typ3 if typ3 is None else hex(typ3)} (want STREAM_INPUT 0x5, never the late burst's 0x6)")
        e4, typ4 = served("after")
        g.check("store_serves_after_the_late_burst@restored", e4 == 0 and typ4 == 0x0005,
                f"after the late burst ended, a locate answered err {e4}, descriptor_type "
                f"{typ4 if typ4 is None else hex(typ4)}")
    # ================= OUTPUT FORMAT, SHIPPING-LEGAL (revision c, F6) =======
    elif c == "V1s_a_shipping_output_format":
        nar, _ = g.ans("set.fmto0.narrow")
        dec, _ = g.ans("set.fmto0.declared")
        inp, _ = g.ans("set.fmti0.narrow")
        g.check("shipping_judge_verdicts@cut", nar == 0 and dec == 1 and inp == 1 and g.boot_evt("judge_shipping") == 1,
                f"SET output 0 to a narrower format {'refused' if nar == 0 else nar}, to its declared format "
                f"{'accepted' if dec == 1 else dec}, SET input 0 to 2 channels {'accepted' if inp == 1 else inp}; "
                f"shipping judge {g.boot_evt('judge_shipping')}")
        narrow = narrower(s.def_fmt_out[0], 4).to_bytes(8, "big")
        bad = [v.hex() for _c, rid, v in g.changes() if rid == 0x40 and v == narrow]
        g.check("refused_set_writes_nothing:0x40", not bad, f"{len(bad)} changes of 0x40 to the refused format")
        g.converged("cut")
        for rid in sorted({rid for _c, rid, _v in g.changes() if rid in g.d3_rids()}):
            g.value_in_slot("cut", rid, f"value_in_slot@cut:{rid:#04x}")
    elif c == "V1s_b_shipping_output_format_restore":
        cut = extra["cut_slots"]
        saved = {rid: v for rid, v in cut.items() if rid in g.d3_rids()}
        term = r.snaps.get("terminal")
        for rid, payload in sorted(saved.items()):
            got = g.snap_value(term, rid) if term else None
            want = g.want_of(rid, payload)
            g.check(f"value_restored:{rid:#04x}", got == want,
                    (f"{show(got, want)}" if got != want else f"live equals the slot, {len(payload)} bytes")
                    + (" (value, valid)" if scalar_of(rid) else ""))
        v, _ = g.ans("post.fmto0.value")
        valid, _ = g.ans("post.fmto0.valid")
        g.check("declared_output_format_restored_valid:0x40", (v, valid) == (s.def_fmt_out[0], 1),
                f"GET output 0 format {v if v is None else hex(v)} valid {valid}, want the declared "
                f"{s.def_fmt_out[0]:#x} WITH its valid flag (a deleted replay leaves it 0)")
        o = r.obs.get("restored", {})
        g.check("restore_counts@boot", o.get("rs_ref") == 0 and o.get("rs_app") == len(saved),
                f"applied {o.get('rs_app')} refused {o.get('rs_ref')}; the slot holds {len(saved)}")
    elif c == "V1s_c_shipping_refuses_a_narrower_saved_output":
        v, _ = g.ans("post.fmto0.value")
        valid, _ = g.ans("post.fmto0.valid")
        o = r.obs.get("restored", {})
        g.check("narrower_output_refused_on_replay:0x40", valid == 0 and o.get("rs_ref", 0) >= 1
                and o.get("d3_fail") == 0,
                f"output 0 format valid {valid} (value {v}), refused {o.get('rs_ref')}, D3 fail {o.get('d3_fail')}")
    elif c == "K19_command_before_the_restore":
        g.converged("end")
        g.value_in_slot("end", 0x50)
        chg = [cy for cy, rid, _v in g.changes() if rid == 0x50]
        term = g.boot_evt("terminal")
        g.check("command_waits_for_the_restore@end", bool(chg) and term > 0 and chg[0] >= term,
                f"the waiting SET was taken at {chg[:1]}, the D3 terminal at {term}")
    # ================= THE MAP RECORD'S FRAMING (page section 8.3) ==========
    elif c.startswith("V3") and c != "V3_refused_map_for_a_removed_cluster":
        o = r.obs.get("restored", {})
        cls = s.recs[0x70][2] // 8
        empty = c == "V3g_map_valid_empty_set"
        want = map_bytes([], cls) if empty else map_bytes(default_out_maps(s, 0), cls)
        live = bytes.fromhex(o.get("maps_out", [""])[0] or "")
        ok = (live == want and o.get("rs_app") == (2 if empty else 1) and o.get("rs_ref") == (0 if empty else 1)
              and o.get("rs_blank") == n_rec - 2)
        g.check("map_record_verdict:0x70", ok,
                f"live OUT0 {'empty' if not live.strip(bytes([255])) else live.hex()[:32]} "
                f"(want {'the empty set' if empty else 'the default set'}); applied {o.get('rs_app')} refused "
                f"{o.get('rs_ref')} blank {o.get('rs_blank')} of {n_rec}")
        v, _ = g.ans("post.ptof0.value")
        valid, _ = g.ans("post.ptof0.valid")
        g.check("other_record_applied:0x50", valid == 1 and v == 1500000, f"ptof0 {v} valid {valid}")
        if c in ("V3d_map_sentinel_tail", "V3e_map_hole"):
            ed = [w for w in g.rs_writes() if w[1].startswith("map")]
            g.check("malformed_refused_untouched:0x70", not ed,
                    f"{len(ed)} map sets staged for a malformed record {ed[:2]}")
    return g


# ----------------------------------------------------------------- the plan
BASE_CASES = [
    "K1_single_change_converges", "K2_change_during_record_write", "K3_two_changes_one_debounce",
    "K4_second_record_in_flight", "K4g_second_group_in_flight", "K5_change_on_the_done_edge",
    "K8_record_write_error_retried", "K9_record_write_given_up", "K10_name_change_converges",
    "K11_name_latch_waits_for_the_program", "K12_map_change_converges",
    "K13_binding_and_d3_share_the_port", "K14_identify_is_not_persisted",
]
#: a case that boots from the slots another case left: the power cycle
V1A = "V1a_set_everything"
V1SA = "V1s_a_shipping_output_format"
DEPENDS = {"K6b_restore_after_cut": "K6a_cut_after_record_before_commit",
           "K7b_restore_after_ack": "K7a_cut_after_ack",
           "K17b_restore_after_cut_in_write": "K17a_cut_during_record_write",
           "K18b_restore_after_cut_in_debounce": "K18a_cut_inside_the_debounce",
           "V1b_restore_everything": V1A,
           "V6b_restore_coupled_pair": "V6a_set_coupled_narrower_pair",
           "V1s_b_shipping_output_format_restore": V1SA}
#: the restore transaction and its deadlines, each on V1a's slots (every
#: group non-default)
#: header transport faults ending in pass 0 (nothing applied) and in pass 1
#: (rolled back), each with the abort cause it must report
HEADER_PASS0 = ["H1_header_error_both_passes", "H2_header_errors_balance_counts", "H2b_header_errors_swap",
                "H3_header_error_pass0_only", "H4_header_error_first_record", "H5_header_error_map_record",
                "H6_header_error_last_name"]
#: pass-1 aborts rolled back to proven defaults: the case and its abort cause
PASS1_ROLLBACK = {"V14_rollback_pass1_early": (1, 2), "V15_rollback_pass1_late": (1, 2),
                  "V16_rollback_pass1_maps": (1, 2), "V18_header_error_pass1": (2,),
                  "H7_header_error_last_name_pass1": (2,), "V18b_header_changed_between_passes": (5,),
                  "V18c_changes_balance_counts": (5,), "V20b_desc_error_once_after_apply": (6,),
                  "V20c_desc_error_in_the_map_revert": (6,), "V20d_desc_error_in_the_final_revert": (6,),
                  "V21_desc_late_after_apply": (6,), "V21b_desc_debt_outlasts_the_store": (6,)}
TRANSACTION = ["V12_abort_pass0_early", "V13_abort_pass0_late", "V14_rollback_pass1_early",
               "V15_rollback_pass1_late", "V16_rollback_pass1_maps", "V17_rollback_cannot_validate",
               "V18_header_error_pass1", "V18b_header_changed_between_passes", "V18c_changes_balance_counts",
               *HEADER_PASS0, "H7_header_error_last_name_pass1",
               "V20_desc_error_after_apply", "V20b_desc_error_once_after_apply", "V21_desc_late_after_apply",
               "V21b_desc_debt_outlasts_the_store", "V21c_desc_debt_outlasts_the_deadline",
               "V21d_desc_slow_within_the_store_bound", "V22_desc_fails_before_boot",
               "W1_silent_pass0", "W2_late_pass0_before_deadline",
               "W3_late_pass0_after_deadline", "W4_silent_pass1", "W5_late_pass1_before_deadline",
               "W6_late_pass1_after_deadline", "W7_silent_pass1_last_name", "W8_map_face_silent_pass1",
               "W9_judge_silent_pass1", "W10_edit_face_silent_pass1", "W12_r218_read_late_after_apply",
               "W13_binding_walk_silent", "W13b_binding_late_before_deadline", "W13c_binding_late_after_deadline",
               "W14_enable_requested_before_the_restore", "W15_binding_answer_after_enable",
               "W16_binding_header_device_error", "K19_command_before_the_restore"]
DEPENDS.update({c: V1A for c in TRANSACTION})
#: the binding walk has one implementation whatever the shape: its deadline,
#: cause and enable cases run at 1x1 only
ONLY_1X1 = {"W13_binding_walk_silent", "W13b_binding_late_before_deadline", "W13c_binding_late_after_deadline",
            "W14_enable_requested_before_the_restore", "W15_binding_answer_after_enable",
            "W16_binding_header_device_error"}
#: cases one shape alone can express: K16 needs an output port whose stream
#: channels outnumber its clusters (8x8: 72 against 9; 1x1: 16 against 17)
SHAPE_CASES = {"8x8": ["K16_map_set_larger_than_its_record"]}
V3X = ["V3a_map_index_0xff00", "V3b_map_index_0xfeff", "V3c_map_index_0xfffe", "V3d_map_sentinel_tail",
       "V3e_map_hole", "V3f_map_index_out_of_range", "V3g_map_valid_empty_set"]
CRAFTED = ["V2_refused_rate", "V3_refused_map_for_a_removed_cluster", *V3X, "V4_refused_configuration_index",
           "V5_record_corrupted_after_the_load", "V7_names_only", "V8_orphaning_format_reverted",
           "V9_refused_maps_revert_their_formats", "V11_torn_read_restores_nothing",
           "V11b_torn_in_pass1_rolls_back", "W11_r217_first_read_late",
           "H8_header_error_sole_saved_record", "V20c_desc_error_in_the_map_revert",
           "V20d_desc_error_in_the_final_revert", "V22b_image_unproven_simple_records", "V2b_refused_clock_source",
           "V1s_c_shipping_refuses_a_narrower_saved_output"]
#: cases that boot with NO slot (blank flash)
UNSLOTTED = ["V10_blank_first_boot", "V23_late_desc_beats_in_service"]
#: the cases whose stimulus includes a NARROWED OUTPUT format, legal only
#: under the SYNTHETIC judge: the product admits an output's declared format
#: alone. Every case booting from V1a's slots restores one.
SYNTHETIC_OUTPUT = {V1A, "V1b_restore_everything", "V6a_set_coupled_narrower_pair", "V6b_restore_coupled_pair",
                    "V8_orphaning_format_reverted", "V9_refused_maps_revert_their_formats",
                    "V20c_desc_error_in_the_map_revert", "V20d_desc_error_in_the_final_revert"}
#: the SYNTHETIC shape exists for the sampling-rate group alone
SYNTH_CASES = [V1A, "V1b_restore_everything", "V2_refused_rate"]


def crafted_for(s: Shape, case: str) -> tuple[tuple, dict]:
    cls_out0 = s.recs[0x70][2] // 8
    two = narrower(s.def_fmt_out[0], 2)
    ptof = {0x50: (1500000).to_bytes(4, "big")}
    ff = b"\xff" * 8
    if case == "V2_refused_rate":
        over = {0x02: (12345).to_bytes(4, "big")}
    elif case == "V3_refused_map_for_a_removed_cluster":
        over = {0x70: map_bytes([(0, 0, cls_out0 + 3, 0)], cls_out0)}
    elif case in ("V3a_map_index_0xff00", "V3b_map_index_0xfeff", "V3c_map_index_0xfffe"):
        si = {"V3a": 0xFF00, "V3b": 0xFEFF, "V3c": 0xFFFE}[case[:3]]
        over = {0x70: map_bytes([(si, 0, 0, 0)], cls_out0), **ptof}
    elif case == "V3d_map_sentinel_tail":
        # a mapping, unused entries, and a LAST entry that is not quite one
        pay = bytearray(map_bytes([(0, 0, 0, 0)], cls_out0))
        pay[-1] = 0x00
        over = {0x70: bytes(pay), **ptof}
    elif case == "V3e_map_hole":
        # an unused entry, then a mapping: a hole
        over = {0x70: ff + map_bytes([(0, 0, 0, 0)], cls_out0 - 1), **ptof}
    elif case == "V3f_map_index_out_of_range":
        over = {0x70: map_bytes([(s.params["N_STREAM_OUT_P"], 0, 0, 0)], cls_out0), **ptof}
    elif case == "V3g_map_valid_empty_set":
        over = {0x70: map_bytes([], cls_out0), **ptof}
    elif case == "V4_refused_configuration_index":
        over = {0x00: (1).to_bytes(2, "big")}
    elif case == "V5_record_corrupted_after_the_load":
        over = {0x50: (1500000).to_bytes(4, "big"), 0x51: (1600000).to_bytes(4, "big")}
    elif case == "V7_names_only":
        over = {0x80: b"V7 names only restore".ljust(64, b"\x00")}
    elif case == "V8_orphaning_format_reverted":
        over = {0x40: two.to_bytes(8, "big")}
    elif case == "V9_refused_maps_revert_their_formats":
        over = {0x40: two.to_bytes(8, "big"), 0x70: map_bytes([(0, 0, cls_out0 + 3, 0)], cls_out0), **ptof}
    elif case in ("V11_torn_read_restores_nothing", "V11b_torn_in_pass1_rolls_back", "W11_r217_first_read_late"):
        over = {0x50: (1100011).to_bytes(4, "big"), 0x80: b"V11 name".ljust(64, b"\x00")}
    elif case == "H8_header_error_sole_saved_record":
        over = {**ptof}
    elif case == "V20c_desc_error_in_the_map_revert":
        over = {0x40: two.to_bytes(8, "big"), 0x70: map_bytes([(0, 0, cls_out0 + 3, 0)], cls_out0), **ptof}
    elif case == "V20d_desc_error_in_the_final_revert":
        over = {0x40: two.to_bytes(8, "big")}
    elif case == "V22b_image_unproven_simple_records":
        over = {**ptof, 0x80: b"V22b name".ljust(64, b"\x00")}
    elif case == "V2b_refused_clock_source":
        # one past the last clock source: the rule is fetched, the value fails it
        over = {0x0A: s.clk_count.to_bytes(2, "big")}
    elif case == "V1s_c_shipping_refuses_a_narrower_saved_output":
        over = {0x40: narrower(s.def_fmt_out[0], 4).to_bytes(8, "big")}
    else:
        raise SystemExit(case)
    return crafted(s, case, over), over


def plan(build: Build) -> list:
    """(case, variant, slots-from) for one build, every source before the
    cases that boot from its slots. Base builds of the shipped shapes run
    everything; the synthetic shape runs its own cases; the tracked build
    runs what reproduces today; a mutant runs the one case its killer lives
    in (and that case's source), or K15's whole sweep."""
    def with_sources(cases: list, variant: str = "") -> list:
        out, seen = [], set()
        for cse in cases:
            src = DEPENDS.get(cse)
            if src and src not in seen:
                out.append((src, "", None))
                seen.add(src)
            if cse not in seen or variant:
                out.append((cse, variant, src))
                seen.add(cse)
        return out
    items = []
    if build.name.startswith("base-") and build.shape in SHIPPED:
        cases = BASE_CASES + CRAFTED + UNSLOTTED + SHAPE_CASES.get(build.shape, [])
        cases += [a for a, _b in (("K6a_cut_after_record_before_commit", 0), ("K7a_cut_after_ack", 0),
                                  ("K17a_cut_during_record_write", 0), ("K18a_cut_inside_the_debounce", 0),
                                  ("V6a_set_coupled_narrower_pair", 0), (V1SA, 0))]
        cases += [c for c in DEPENDS if build.shape == "1x1" or c not in ONLY_1X1]
        items += with_sources(cases)
        items += [("V1b_restore_everything", "stale", V1A)]
        if build.shape == "1x1":
            items += [("K15_binding_on_the_d3_grant_cycle", v, None) for v in K15_SWEEP]
    elif build.name.startswith("base-"):
        items += with_sources(SYNTH_CASES)
        items += [("V1b_restore_everything", "stale", V1A)]
    elif build.tracked:
        items += with_sources(TRACKED_CASES + [V1A, "V1b_restore_everything"])
    else:
        m = build.name[4:]
        ks = killers(m)
        if ks[0][1] == "*":
            return [(ks[0][0], v, None) for v in K15_SWEEP]
        items += with_sources([k[0] for k in ks])
        if m == "M13_restore_applies_nothing":
            items.append(("V1b_restore_everything", "stale", V1A))
    return items


def execute(build: Build, s: Shape) -> list:
    results = []
    runs = {}
    for case, variant, src in plan(build):
        slots, extra = None, {}
        if src:
            a = runs[src]
            slots = (a.out / "cut-slotA.bin", a.out / "cut-slotB.bin")
            extra["cut_slots"] = Grade(a, s).tag_slots("cut")
        elif case in CRAFTED:
            slots, over = crafted_for(s, case)
            extra["crafted"] = over
        r = run_case(build, s, case, variant, slots)
        runs[case if not variant else f"{case}~{variant}"] = r
        g = grade_run(r, s, extra)
        results.append((r, g))
    return results


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("action", choices=["prep", "build", "run", "controls", "receipts", "amend"])
    ap.add_argument("names", nargs="*")
    ap.add_argument("--shapes", default=",".join(SHAPES))
    ap.add_argument("--jobs", type=int, default=8)
    ap.add_argument("--pool", type=int, default=4)
    args = ap.parse_args()
    if args.action == "receipts":
        return receipts()
    if args.action == "amend":
        for key, (_pinned, amended, _s) in AMENDMENTS.items():
            amended.write_text(amended_text(key))
            print(f"wrote {amended.relative_to(HERE)}")
        return 0
    check_amendments()
    if args.action == "controls":
        return controls(args.pool)
    check_m0_encoding()
    shapes_wanted = args.shapes.split(",")
    unknown = [n for n in shapes_wanted if n not in SHAPES]
    if unknown:
        print(f"REFUSED: unknown shape {unknown}")
        return 2
    shapes = {n: prep_shape(n) for n in shapes_wanted}
    builds = [b for b in all_builds(shapes_wanted) if b.shape in shapes]
    focused = bool(args.names) or set(shapes_wanted) != set(SHAPES)
    if args.names:
        missing = [n for n in args.names if n not in {b.name for b in builds}]
        if missing:
            print(f"REFUSED: no such build {missing} at shapes {shapes_wanted}")
            return 2
        builds = [b for b in builds if b.name in args.names]
    if args.action == "prep":
        for n, s in shapes.items():
            kind = "SYNTHETIC" if n in SYNTH else "shipped"
            print(f"shape {n} ({kind}): {len(s.recs)} records, params {s.params}, rates {s.rates}, clk "
                  f"{s.clk_count}, fmt_out {[hex(f) for f in s.def_fmt_out]}, fmt_in {[hex(f) for f in s.def_fmt_in]}")
        return 0
    if args.action == "build":
        with cf.ThreadPoolExecutor(max_workers=args.pool) as ex:
            futs = {ex.submit(do_build, b, shapes[b.shape], args.jobs): b for b in builds}
            for f in cf.as_completed(futs):
                b = f.result()
                print(f"built {b.name}")
        return 0
    # run: every selected build must exist; nothing is skipped silently
    absent = []
    for b in builds:
        b.binary = OUT / "build" / b.name / "obj" / "d3sim"
        if not b.binary.exists():
            absent.append(b.name)
    if absent:
        for n in absent:
            print(f"REFUSED: {n} is not built")
        return 2
    if focused:
        print(f"FOCUSED RUN, not a full-run claim: builds {[b.name for b in builds]} at shapes {shapes_wanted}")
    allres = {}
    with cf.ThreadPoolExecutor(max_workers=args.pool) as ex:
        futs = {ex.submit(execute, b, shapes[b.shape]): b for b in builds}
        for f in cf.as_completed(futs):
            b = futs[f]
            allres[b.name] = f.result()
    fail = report(allres, builds, focused)
    return 1 if fail else 0


def report(allres: dict, builds: list, focused: bool) -> int:
    """Write the graded results and return the number of VERDICT failures:
    an unexpected base result, a tracked control that does not hold, a
    mutant that was not killed by its named check in a COMPLETED run, a
    vacuity control that does not hold, an unreached premise, or a planned
    case that did not run."""
    lines, js = [], {"builds": {}}
    fail = 0
    for bname in sorted(allres):
        js["builds"][bname] = []
        for r, g in allres[bname]:
            tag = r.case + (f"~{r.variant}" if r.variant else "")
            for name, (ok, detail) in sorted(g.checks.items()):
                lines.append(f"{bname:40s} {tag:48s} {'PASS' if ok else 'FAIL'} {name} -- {detail}")
            js["builds"][bname].append({"case": tag, "checks": {k: {"pass": v[0], "detail": v[1]}
                                                                for k, v in g.checks.items()}})
    verdict = []
    # every planned case of every selected build ran
    for b in builds:
        want = [c + (f"~{v}" if v else "") for c, v, _s in plan(b)]
        got = [r.case + (f"~{r.variant}" if r.variant else "") for r, _g in allres.get(b.name, [])]
        if sorted(want) != sorted(got):
            fail += 1
            verdict.append(f"INCOMPLETE {b.name}: planned {len(want)} runs, graded {len(got)}")
    for bname, res in sorted(allres.items()):
        if bname.startswith("base-"):
            for r, g in res:
                tag = r.case + (f"~{r.variant}" if r.variant else "")
                for name, (ok, _d) in g.checks.items():
                    expected_fail = (r.variant == "stale" and name == "rows_cleared_before_restore@boot")
                    if ok == expected_fail:
                        fail += 1
                        verdict.append(f"UNEXPECTED {bname} {tag} {name} {'PASS' if ok else 'FAIL'}")
            sweep = [(r.variant, g.boot().get("collisions", 0)) for r, g in res
                     if r.case == "K15_binding_on_the_d3_grant_cycle"]
            if sweep:
                hits = [v for v, n in sweep if n > 0]
                ok = bool(hits)
                if not ok:
                    fail += 1
                verdict.append(f"PREMISE {bname} K15: the binding manager sampled busy on the D3 writer's "
                               f"grant cycle at {', '.join(hits) if hits else 'NO release'} "
                               f"({len(hits)} of {len(sweep)} releases) -> {'reached' if ok else 'NOT REACHED'}")
        elif bname.startswith("tracked-"):
            got = {}
            for r, g in res:
                tag = r.case + (f"~{r.variant}" if r.variant else "")
                for name, (ok, _d) in g.checks.items():
                    got[(tag, name)] = ok
            for case, name in TRACKED_MUST_FAIL:
                ok = got.get((case, name))
                good = ok is False
                if not good:
                    fail += 1
                verdict.append(f"TRACKED {case} : {name} "
                               f"{'FAILS, as it must at the current source' if good else f'DOES NOT FAIL ({ok})'}")
            for case, name in TRACKED_MUST_PASS:
                keys = [k for k in got if k[1] == name and (case == "*" or k[0] == case)]
                bad = [k for k in keys if not got[k]]
                good = bool(keys) and not bad
                if not good:
                    fail += 1
                verdict.append(f"TRACKED {case} : {name} "
                               f"{'PASSES, as it must' if good else f'DOES NOT PASS ({bad or keys})'}")
        else:
            m = bname[4:]
            states = []
            for case, variant, killer, _s in killers(m):
                state, where, why = "SURVIVED", None, ""
                for r, g in res:
                    if r.case != case or (variant != "*" and r.variant != variant):
                        continue
                    t_ = r.case + (f"~{r.variant}" if r.variant else "")
                    if not g.checks.get("case_completed", (False,))[0]:
                        #! a run that did not complete kills nothing
                        state, where, why = ("NOT COMPLETED", t_,
                                             f" ({g.checks.get('case_completed', (0, 'no run'))[1]})")
                        continue
                    if killer not in g.checks:
                        if state != "NOT COMPLETED":
                            state, where, why = "KILLER ABSENT", t_, ""
                        continue
                    if not g.checks[killer][0]:
                        state, where, why = "KILLED", t_, f" -- {g.checks[killer][1][:140]}"
                        break
                tag = where or (case + (f"~{variant}" if variant else ""))
                states.append((state, f"{tag} : {killer}{why}"))
            #! killed only when EVERY named check killed it
            state = "KILLED" if all(st == "KILLED" for st, _w in states) else \
                next(st for st, _w in states if st != "KILLED")
            if state != "KILLED":
                fail += 1
            verdict.append(f"MUTANT {m}: {state} by " + " AND ".join(w for _st, w in states))
            if m == "M13_restore_applies_nothing":
                for r, g in res:
                    if r.variant == "stale":
                        naive = g.checks.get("value_restored:0x50", (None,))[0]
                        cleared = g.checks.get("rows_cleared_before_restore@boot", (None,))[0]
                        done = g.checks.get("case_completed", (False,))[0]
                        ok = done and naive is True and cleared is False
                        if not ok:
                            fail += 1
                        verdict.append(f"CONTROL stale store under M13: naive read-back "
                                       f"{'PASSES' if naive else 'FAILS'}, cleared-first "
                                       f"{'FAILS' if cleared is False else 'PASSES'} -> "
                                       f"{'as required' if ok else 'NOT AS REQUIRED'}")
    #! which runs rest on the SYNTHETIC output-format judge: a narrowed output
    #! in their stimulus is legal only there (the product admits an output's
    #! declared format alone); the V1s cases run the SHIPPING judge
    synth = sorted({r.case for res in allres.values() for r, _g in res
                    if r.case in SYNTHETIC_OUTPUT or DEPENDS.get(r.case) == V1A})
    ship = sorted({r.case for res in allres.values() for r, g in res if g.boot().get("judge_shipping") == 1})
    if synth:
        verdict.append(f"LABEL SYNTHETIC output-format judge (a narrowed output format, product-illegal): "
                       f"{len(synth)} cases: {', '.join(synth)}")
    if ship:
        verdict.append(f"LABEL SHIPPING output-format judge (milan_datapath.sv sfv_supported_w): {', '.join(ship)}")
    total = sum(len(g.checks) for res in allres.values() for _r, g in res)
    runs = sum(len(res) for res in allres.values())
    kind = "FOCUSED" if focused else "FULL"
    summary = f"SUMMARY {kind} builds {len(allres)}, runs {runs}, checks {total}, verdict failures {fail}"
    text = "\n".join(lines + [""] + verdict + ["", summary]) + "\n"
    stem = (OUT / "results-focused") if focused else (HERE / "results")
    stem.parent.mkdir(parents=True, exist_ok=True)
    stem.with_suffix(".txt").write_text(text)
    js["verdict"] = verdict
    js["summary"] = summary
    stem.with_suffix(".json").write_text(json.dumps(js, indent=1) + "\n")
    print("\n".join(verdict))
    print(summary)
    return fail


# --------------------------------------------------------- process controls
#: each: (name, build to run, its shape, doctored binaries {build: source},
#: extra environment, the exit status it must end with, the diagnostics its
#: output must contain). A source "false" is an executable that fails before
#: any scenario; a source None leaves the build absent.
CONTROLS = [
    ("healthy_binary_as_mutant", "mut-M01_taint_ignored", "1x1", {"mut-M01_taint_ignored": "base-1x1"}, {}, 1,
     ["MUTANT M01_taint_ignored: SURVIVED", "verdict failures 1"]),
    ("binary_fails_before_the_scenario", "mut-M06_identify_is_a_change", "1x1",
     {"mut-M06_identify_is_a_change": "false"}, {}, 1,
     ["MUTANT M06_identify_is_a_change: NOT COMPLETED", "verdict failures 1"]),
    ("failed_baseline_result", "base-1x1r2", "1x1r2", {"base-1x1r2": "mut-RPL_rate"}, {}, 1,
     ["UNEXPECTED base-1x1r2 V1b_restore_everything value_restored:0x02 FAIL"]),
    ("tracked_control_violated", "tracked-1x1", "1x1", {"tracked-1x1": "base-1x1"}, {}, 1,
     ["TRACKED K1_single_change_converges : converged@end DOES NOT FAIL"]),
    ("vacuity_control_violated", "mut-M13_restore_applies_nothing", "1x1",
     {"mut-M13_restore_applies_nothing": "mut-M13_restore_applies_nothing"},
     {"D3_CONTROL_SKIP_STALE_SEED": "1"}, 1,
     ["CONTROL stale store under M13: naive read-back FAILS, cleared-first PASSES -> NOT AS REQUIRED",
      "verdict failures 1"]),
    ("tracked_control_absent", "tracked-1x1", "1x1", {"tracked-1x1": None}, {}, 2,
     ["REFUSED: tracked-1x1 is not built"]),
    ("empty_selection", "no-such-build", "1x1", {}, {}, 2, ["REFUSED: no such build ['no-such-build']"]),
]


def controls(pool: int) -> int:
    """The runner's own verdict propagation, executed through its real CLI.
    Each control doctors a COPY of the built binaries in a private output
    tree and requires the exit status and the diagnostic it names."""
    bad = 0
    for name, build, shape, doctor, env, want_rc, want_text in CONTROLS:
        root = OUT / "controls" / name
        if root.exists():
            shutil.rmtree(root)
        for b, src in doctor.items():
            if src is None:
                continue
            dst = root / "build" / b / "obj" / "d3sim"
            dst.parent.mkdir(parents=True)
            if src == "false":
                dst.write_text("#!/bin/sh\nexit 1\n")
                dst.chmod(0o755)
            else:
                shutil.copy2(OUT / "build" / src / "obj" / "d3sim", dst)
        p = subprocess.run([sys.executable, "-B", str(HERE / "run.py"), "run", build, "--shapes", shape,
                            "--pool", str(pool)], text=True, capture_output=True,
                           env={**os.environ, **env, "D3_OUT": str(root), "PYTHONDONTWRITEBYTECODE": "1"})
        (root / "control.log").parent.mkdir(parents=True, exist_ok=True)
        (root / "control.log").write_text(p.stdout + p.stderr)
        missing = [w for w in want_text if w not in p.stdout]
        ok = p.returncode == want_rc and not missing
        bad += not ok
        print(f"CONTROL {name}: {'AS REQUIRED' if ok else 'NOT AS REQUIRED'} -- exit {p.returncode} "
              f"(required {want_rc}); diagnostics {'found' if not missing else f'MISSING {missing}'}")
    print(f"CONTROLS {len(CONTROLS)}, not as required {bad}")
    return 1 if bad else 0


# ------------------------------------------------------------------ receipts
#: the repository files the model reads or compiles, besides the evidence
REPO_READ = [PP / "acmp/pp_acmp_pkg.sv", PP / "aecp/KL_aecp_dyn_state.sv", PP / "aecp/KL_aecp_desc_store.sv",
             PINNED_BIND, PINNED_PORT, BACKEND, WRITER,
             ROOT / "scripts/nvm_klj2.py", ROOT / "scripts/nvm_shape.py", ROOT / "scripts/check_nvm_record_space.py",
             ROOT / "sw/firmware/nvm_hosttest/test_nvm_firmware.py", ROOT / SHAPES["1x1"], ROOT / SHAPES["8x8"],
             ROOT / "sw/builder/endstation_builder.py",
             #! not read at run time: the shipping judge is transcribed from it
             ROOT / "hdl/milan/milan_datapath.sv"]


def receipts() -> int:
    """sha256 of every TRACKED file of the evidence directory (git ls-files,
    so an ignored incidental file such as a tool's history can never enter
    the record) but the command record itself, and of the repository files
    the model reads."""
    top = HERE.parent
    p = subprocess.run(["git", "ls-files", "-z", "--", "."], cwd=top, capture_output=True)
    if p.returncode:
        print("REFUSED: git ls-files failed")
        return 2
    files = sorted(f for f in p.stdout.decode().split("\0") if f and f != "COMMAND_RESULTS.md")
    print("| File (relative to design-evidence/500-materialization) | sha256 |")
    print("|---|---|")
    for f in files:
        print(f"| `{f}` | `{hashlib.sha256((top / f).read_bytes()).hexdigest()}` |")
    print()
    print("| Repository file | sha256 |")
    print("|---|---|")
    for f in REPO_READ:
        print(f"| `{f.relative_to(ROOT)}` | `{hashlib.sha256(f.read_bytes()).hexdigest()}` |")
    return 0


if __name__ == "__main__":
    sys.exit(main())
