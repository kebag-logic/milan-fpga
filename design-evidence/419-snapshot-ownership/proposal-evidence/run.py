#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Issue #419 round 3: the ONE run script behind PROPOSAL.md.

    python3 -B proposal-evidence/run.py [--jobs 8] [--quick] [--skip-area]

What it does, in order, writing only under proposal-evidence/:

 1. PREFLIGHT. Refuses unless the checkout is dev 36ee8a37 with the three
    pins, and records the SHA-256 of every production file it reads; the same
    digests are re-checked at the end and must not have moved.
 2. SHAPES. Runs the repository's own builder and record-space gate for the
    AX7101 1x1 TDM8 and 8x8 configs: the firmware constants, the record table
    and the RTL parameters all come from them, never from a literal here.
 3. BUILDS. One Verilated binary per build: the RTL wrapper (real donor
    manager, port and dynamic-state store; tracked or prototype backend) and
    the host-compiled firmware (tracked or prototype translation unit), in ONE
    process sharing ONE clock. Mutants are single counted replacements.
 4. CASES. Every case on every build, in parallel (at most --jobs at once).
 5. ORACLE. Decodes the dumped journal slots with scripts/nvm_klj2.py and
    compares records with frames it builds itself; grades named checks.
 6. EXPECTATIONS. The prototype passes every check except the ones this file
    lists as expected failures (each with its reason); the tracked build FAILS
    the #418, ERASE-error and #420 checks; every mutant is killed by its named
    check. Exit 0 iff all of that holds.
 7. BUILD-TIME REFUSALS and AREA (yosys out of context, the syn/yosys/ooc.sh
    recipe reimplemented standalone because that script refuses a top outside
    its own list and is a tracked file).
"""
from __future__ import annotations

import argparse
import concurrent.futures as cf
import dataclasses
import datetime as dt
import hashlib
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
ROOT = HERE.parent
HARNESS = HERE / "harness"
STUBS = HARNESS / "stubs"
PROTO_SV = HERE / "prototype" / "KL_nvm_backend.proto.sv"
PROTO_FW = HERE / "prototype" / "milan_baremetal.proto.c"
WRAPPER = HERE / "rtl" / "cosim_top.sv"
BUILD = HERE / "build"
RUNS = HERE / "runs"
LOGS = HERE / "logs"

EXPECT_HEAD = "36ee8a3714f511d4717513be28b590da26ce1e4e"
EXPECT_PINS = {
    "protocol-processor": "8f2f58fb2cc26e3d37170744b83f9909786a3105",
    "gptp-processor": "c1b617435824929a790739ea8585c3fe1a328cc0",
    "third_party/verilog-axis": "48ff7a7e2ef782cf778d47910cf85835c64b1bce",
}
PP = "protocol-processor/hdl"
DONOR_SV = [f"{PP}/acmp/pp_acmp_pkg.sv", f"{PP}/aecp/KL_aecp_dyn_state.sv",
            f"{PP}/acmp/KL_acmp_nvm_shadow.sv", f"{PP}/packet_engine/KL_pp_nvm_port.sv"]
PRODUCTION = [
    "hdl/milan/KL_nvm_backend.sv", "hdl/milan/KL_pp_shadow.sv",
    "hdl/common/csr/milan_csr.sv",
    "sw/firmware/milan_baremetal/milan_baremetal.c",
    "sw/firmware/nvm_hosttest/nvm_host.c", "sw/firmware/nvm_hosttest/test_nvm_firmware.py",
    "scripts/nvm_klj2.py", "scripts/nvm_contract.py", "scripts/nvm_shape.py",
    "scripts/check_nvm_record_space.py", "syn/yosys/ooc.sh",
    "docs/design/SAVED_STATE_FASTCONNECT.md", "REQUIREMENTS.md",
    f"{PP}/top/protocol_processor_top.sv", *DONOR_SV,
]
SHAPES = {"1x1": "configs/endstation_ax7101_1x1_tdm8.yaml",
          "8x8": "configs/endstation_ax7101_8x8.yaml"}
CLK_HZ = 1_000_000      # the co-simulation's backend clock in MODEL time
T_HOLD_MS = 50
TAG_C3 = 0xC3

sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "sw" / "firmware" / "nvm_hosttest"))
import test_nvm_firmware as ref   # noqa: E402  (the repository's own host gate)
from nvm_klj2 import klj2_decode  # noqa: E402
from nvm_contract import VD_OK    # noqa: E402

MANIFEST: list[dict] = []


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")


def cmd(argv: list[str], log: Path, cwd: Path = ROOT, check: bool = True,
        timeout: int = 1800) -> subprocess.CompletedProcess:
    """Run one command with rtk and taskset in front, log it, manifest it."""
    full = ["rtk", "proxy", "taskset", "-c", "16-31", *argv]
    t0, s0 = time.time(), now()
    p = subprocess.run(full, cwd=cwd, text=True, capture_output=True, timeout=timeout,
                       env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1",
                            "TMPDIR": str(HERE / "tmp")})
    log.parent.mkdir(parents=True, exist_ok=True)
    log.write_text(p.stdout + p.stderr)
    MANIFEST.append(dict(argv=[str(a).replace(str(ROOT), "<CHECKOUT>") for a in argv],
                         start=s0, wall_s=round(time.time() - t0, 3), exit=p.returncode,
                         log=str(log.relative_to(HERE))))
    if check and p.returncode:
        raise SystemExit(f"FAILED ({p.returncode}): {' '.join(map(str, argv))}\n  see {log}")
    return p


# ----------------------------------------------------------------- preflight
def git(*args: str, cwd: Path = ROOT) -> str:
    return subprocess.check_output(["rtk", "proxy", "git", *args], cwd=cwd, text=True).strip()


def preflight() -> dict:
    head = git("rev-parse", "HEAD")
    if head != EXPECT_HEAD:
        raise SystemExit(f"refused: HEAD is {head}, this evidence is for {EXPECT_HEAD}")
    for sub, pin in EXPECT_PINS.items():
        got = git("rev-parse", "HEAD", cwd=ROOT / sub)
        if got != pin:
            raise SystemExit(f"refused: {sub} is at {got}, expected {pin}")
    # tracked changes refuse; an untracked file someone else placed in the
    # checkout is recorded, never touched
    dirty = git("status", "--porcelain", "--untracked-files=no").splitlines()
    if dirty:
        raise SystemExit(f"refused: tracked changes present: {dirty}")
    return {p: sha(ROOT / p) for p in PRODUCTION}


# -------------------------------------------------------------------- shapes
@dataclasses.dataclass
class ShapeInfo:
    name: str
    header: str            # the repository's constants header (tracked writer)
    records: Path          # the record table from the record-space gate
    params: dict
    donor: object
    ident: object
    expect: dict
    img_len: int
    recs: dict             # rid -> (offset, framed length)


def shape(name: str) -> ShapeInfo:
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
    cmd(["python3", "-B", "scripts/check_nvm_record_space.py", "--emit-record-table",
         str(cfg), "-o", str(table)], LOGS / f"shape-{name}-record-table.log")
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


def proto_header(tracked: str) -> str:
    """The contract-3 generator's soc.h: MILAN_NVM_IMAGE_BASE is WITHDRAWN (the
    build-time refusal of an older writer) and the live window, the private
    stage and the contract number are published instead."""
    line = next(ln for ln in tracked.splitlines() if ln.startswith("#define MILAN_NVM_IMAGE_BASE"))
    live = line.replace("MILAN_NVM_IMAGE_BASE", "MILAN_NVM_LIVE_BASE")
    stage = (f"#define MILAN_NVM_STAGE_BASE ((uintptr_t)nvm_host_ddr + "
             f"0x{ref.IMAGE_OFF - 0x10000:x}u)")
    out = tracked.replace(line, "\n".join([live, stage, "#define MILAN_NVM_CONTRACT 3u"]))
    assert "MILAN_NVM_IMAGE_BASE" not in out
    return out


# ------------------------------------------------------------------ firmware
FW_SUBS = [
    ("static inline uint32_t milan_read(unsigned int offset)\n{\n\treturn *milan_reg(offset);\n}",
     "static inline uint32_t milan_read(unsigned int offset)\n{\n\treturn nvm_host_csr_read(offset);\n}"),
    ("\t*milan_reg(offset) = value;\n\t__asm__ volatile(\"fence iorw, iorw\" ::: \"memory\");\n",
     "\tnvm_host_csr_write(offset, value);\n"),
]
FENCE_RW = "__asm__ volatile(\"fence rw, rw\" ::: \"memory\");"


def host_firmware(text: str, fences: int) -> str:
    """The host build of a firmware translation unit: the two CSR access
    primitives route to the model and the remaining fences are blanked, the
    same adapter the repository's host gate applies, counted."""
    for old, new in FW_SUBS:
        if text.count(old) != 1:
            raise SystemExit(f"firmware seam count {text.count(old)}: {old[:50]!r}")
        text = text.replace(old, new)
    if text.count(FENCE_RW) != fences:
        raise SystemExit(f"expected {fences} rw fences, found {text.count(FENCE_RW)}")
    return text.replace(FENCE_RW, "(void)0;")


# ------------------------------------------------------------------- mutants
RTL_MUT = {
    "M01_open_at_erase_completion": [(
        "                          | (set_q_r & hit_w)\n",
        "                          | (done_r & ~was_write_r & op_mut_r & hit_w)\n")],
    "M02_close_on_any_completion": [(
        "  assign rec_close_w = done_r & was_write_r & op_mut_r & op_full_r;\n",
        "  assign rec_close_w = done_r & op_mut_r;\n")],
    "M03_close_on_partial_write": [(
        "  assign rec_close_w = done_r & was_write_r & op_mut_r & op_full_r;\n",
        "  assign rec_close_w = done_r & was_write_r & op_mut_r;\n")],
    "M04_ack_ignores_identity": [(
        "                     & (ack_id_w == cap_id_r) & ~void_hard_w;\n",
        "                     & ~void_hard_w;\n")],
    "M05_ack_retires_live_work": [(
        "  assign dirty_live_n_w = rec_close_w ? 1'b1\n                        : reload_w    ? 1'b0\n",
        "  assign dirty_live_n_w = rec_close_w ? 1'b1\n                        : ack_ok_w    ? 1'b0\n"
        "                        : reload_w    ? 1'b0\n")],
    "M06_hold_does_not_defer": [(
        "  assign gnt_now_w   = (st_r == S_IDLE) && dev_req_i && !(cap_hold_r && mut_req_w);\n",
        "  assign gnt_now_w   = (st_r == S_IDLE) && dev_req_i;\n")],
    "M07_hold_never_expires": [(
        "  assign hold_exp_w  = cap_hold_r & ms_tick_w & (hold_r == HOLD_W_C'(1));\n",
        "  assign hold_exp_w  = 1'b0;\n")],
    "M08_certificate_ignores_grant": [(
        "  assign cert_ok_w   = cert_w & cap_open_r & ~cap_cert_r & cap_valid_r\n"
        "                     & ~void_grant_w & ~void_hard_w;\n",
        "  assign cert_ok_w   = cert_w & cap_open_r & ~cap_cert_r & ~void_hard_w;\n")],
    "M09_second_arm_accepted": [(
        "  assign arm_ok_w    = arm_w & img_cfg_w & img_valid_r & ~cap_open_r & ~void_hard_w;\n",
        "  assign arm_ok_w    = arm_w & img_cfg_w & img_valid_r & ~void_hard_w;\n")],
    "M10_release_forgets_work": [(
        "                        : drop_w      ? (dirty_live_r | dirty_cap_r)\n",
        "                        : drop_w      ? dirty_live_r\n")],
    "M11_dirty_from_bytes_not_close": [(
        "  assign dirty_live_n_w = rec_close_w ? 1'b1\n",
        "  assign dirty_live_n_w = (mem_wr_valid_o & mem_wr_ready_i) ? 1'b1\n")],
    "M12_alarm_not_revoking": [(
        "  assign loss_ev_w = alive_exp_w | commit_exp_w | fail_rep_w | alarm_i;\n",
        "  assign loss_ev_w = alive_exp_w | commit_exp_w | fail_rep_w;\n")],
    "M13_report_not_revoking": [(
        "  assign loss_ev_w = alive_exp_w | commit_exp_w | fail_rep_w | alarm_i;\n",
        "  assign loss_ev_w = alive_exp_w | commit_exp_w | alarm_i;\n")],
    "M14_pending_bit_misses_producer": [(
        "  assign nvm_pend_o    = pend_r | unres_w;\n",
        "  assign nvm_pend_o    = unres_w;\n")],
    "M15_pending_bit_misses_open_record": [(
        "  assign nvm_pend_o    = pend_r | unres_w;\n",
        "  assign nvm_pend_o    = pend_r;\n")],
    "M17_hold_expiry_voids_capture": [(
        "                   : (close_w | void_grant_w) ? 1'b0 : cap_valid_r;\n",
        "                   : (close_w | void_grant_w | hold_exp_w) ? 1'b0 : cap_valid_r;\n")],
    # the vacuity control for the owner's separate pending bit: a bit that is
    # simply held at 1 passes every "no false durable claim" check, and must
    # be caught by convergence instead
    "M18_pending_bit_stuck": [(
        "  assign nvm_pend_o    = pend_r | unres_w;\n",
        "  assign nvm_pend_o    = 1'b1;\n")],
    # NOT a mutant: the REJECTED ALTERNATIVE of the owner's question 11(a),
    # executed so its rejection has an executed reason. The pending work is
    # folded into nvm_dirty (the status bit, the writer's commit trigger and
    # the stale recovery all read the composite).
    "A01_composite_durable_bit": [
        ("  assign nvm_dirty_o   = dirty_img_w;\n",
         "  assign nvm_dirty_o   = dirty_img_w | nvm_pend_o;\n"),
        ("                                     nvm_stale_o, dirty_img_w, img_valid_r,\n",
         "                                     nvm_stale_o, (dirty_img_w | nvm_pend_o), img_valid_r,\n"),
        ("  assign comp_n_w  = dirty_live_n_w | dirty_cap_n_w;\n",
         "  assign comp_n_w  = dirty_live_n_w | dirty_cap_n_w | pend_i | unres_w;\n")],
}
FW_MUT = {
    "F01_certificate_not_checked": [(
        "\tif (!(milan_read(MILAN_PP_NVM_STAT) & NVM_RD_CAP_CERT)) {\n",
        "\tif (!(milan_read(MILAN_PP_NVM_STAT) & NVM_RD_CAP_CERT) && 0) {\n")],
    "F02_copies_open_records": [(
        "\t\tif (!((own[rec.id >> 5] >> (rec.id & 31u)) & 1u))\n",
        "\t\tif (!((own[rec.id >> 5] >> (rec.id & 31u)) & 0u))\n")],
    "F03_prefill_from_blank": [(
        "\tif (nvm_auth_slot == NVM_SLOT_NONE) {\n\t\tnvm_stage_blank_image();\n",
        "\tif (1) {\n\t\tnvm_stage_blank_image();\n")],
    "F04_ack_without_identity": [(
        "\tmilan_write(MILAN_PP_NVM_STAT, NVM_STROBE_ACK | (cap_id << 16));\n",
        "\tmilan_write(MILAN_PP_NVM_STAT, NVM_STROBE_ACK);\n")],
    "F05_device_busy_gate_kept": [(
        "\tif (stat & NVM_RD_COMMIT_BUSY)\n\t\treturn;\n",
        "\tif (stat & (NVM_RD_DEV_BUSY | NVM_RD_COMMIT_BUSY))\n\t\treturn;\n")],
    # an acknowledgement for a slot that did NOT verify: the identity is
    # right, the evidence is not
    "F06_ack_after_failed_slot": [(
        "\t\tnvm_csr_write(NVM_W_STAT, NVM_STAT_VALID | vd);\n"
        "\t\tmilan_write(MILAN_PP_NVM_STAT, NVM_STROBE_RELEASE);\n",
        "\t\tnvm_csr_write(NVM_W_STAT, NVM_STAT_VALID | vd);\n"
        "\t\tmilan_write(MILAN_PP_NVM_STAT, NVM_STROBE_ACK | (cap_id << 16));\n")],
}
GLUE_MUT = {
    "G01_pending_from_edge_detector": [(
        "  assign pend_w = aecp_dyn_dirty_w | (d1_en_i & (|mgr_dirty_w));\n",
        "  logic dyn_q_mut;\n  always_ff @(posedge clk_i) dyn_q_mut <= aecp_dyn_dirty_w;\n"
        "  assign pend_w = (aecp_dyn_dirty_w & ~dyn_q_mut) | (d1_en_i & (|mgr_dirty_w));\n")],
}
#: each mutant and the named check that must kill it (case, check)
KILLER = {
    "M01_open_at_erase_completion": ("B1_erase_error_full_span", "last_verified_kept@end:0x20"),
    "M02_close_on_any_completion": ("C1g_real_port_copy_inside_erase_write_gap", "never_torn_or_erased@after:0x21"),
    "M03_close_on_partial_write": ("B10_partial_write_never_closes", "later_record_persists@end:0x21"),
    "M04_ack_ignores_identity": ("A6_late_ack_while_new_capture_open", "stale_identity_refused@stray"),
    "M05_ack_retires_live_work": ("A2_write_between_verify_and_ack", "ack_retires_only_slot@post_ack:0x20"),
    "M06_hold_does_not_defer": ("C1_request_during_hold_is_deferred", "deferred_until_certificate:0x21"),
    "M07_hold_never_expires": ("C2_hold_expiry_then_erase_with_stale_mask", "hold_bounded:0x21"),
    "M08_certificate_ignores_grant": ("C2_hold_expiry_then_erase_with_stale_mask", "last_verified_kept@after:0x21"),
    "M09_second_arm_accepted": ("C5_concurrent_arm_refused", "concurrent_arm_refused@stray"),
    "M10_release_forgets_work": ("C2_hold_expiry_then_erase_with_stale_mask", "later_record_persists@after:0x20"),
    "M11_dirty_from_bytes_not_close": ("A12_last_byte_before_arm_done_after", "converged@end"),
    "M12_alarm_not_revoking": ("B1_erase_error_full_span", "alarm_revokes@end"),
    "M13_report_not_revoking": ("F2_reported_flash_failure", "failure_revokes"),
    "M14_pending_bit_misses_producer": ("E1_dyn_change_ack_then_second_change", "no_durable_claim_unmaterialized@end"),
    "M15_pending_bit_misses_open_record": ("B5_erase_then_no_write_yet", "no_durable_claim@gap"),
    "M17_hold_expiry_voids_capture": ("C3_hold_expiry_without_producer", "slow_copy_certifies"),
    "M18_pending_bit_stuck": ("A1_stable_no_change", "converged@end"),
    "A01_composite_durable_bit": ("E1_dyn_change_ack_then_second_change", "pending_drives_no_commit@end"),
    "F06_ack_after_failed_slot": ("F2_reported_flash_failure", "converged@end"),
    "F01_certificate_not_checked": ("C2_hold_expiry_then_erase_with_stale_mask", "last_verified_kept@after:0x21"),
    "F02_copies_open_records": ("B1_erase_error_full_span", "last_verified_kept@end:0x20"),
    "F03_prefill_from_blank": ("B1_erase_error_full_span", "last_verified_kept@end:0x20"),
    "F04_ack_without_identity": ("A1_stable_no_change", "stable_no_churn"),
    "F05_device_busy_gate_kept": ("B9_abandoned_write_stream", "later_record_persists@abandoned:0x20"),
    "G01_pending_from_edge_detector": ("E1_dyn_change_ack_then_second_change", "no_durable_claim_unmaterialized@end"),
}


def mutate(text: str, subs: list[tuple[str, str]], what: str) -> str:
    for old, new in subs:
        if text.count(old) != 1:
            raise SystemExit(f"mutant {what}: seam hit {text.count(old)} times: {old[:60]!r}")
        text = text.replace(old, new)
    return text


# -------------------------------------------------------------------- builds
@dataclasses.dataclass
class Build:
    name: str
    shape: str
    proto: bool                 # prototype RTL + glue
    fw_proto: bool              # prototype firmware
    rtl_mut: list = dataclasses.field(default_factory=list)
    fw_mut: list = dataclasses.field(default_factory=list)
    glue_mut: list = dataclasses.field(default_factory=list)
    cap_id_w: int = 16
    binary: Path | None = None


def do_build(b: Build, shapes: dict[str, ShapeInfo]) -> Build:
    s = shapes[b.shape]
    work = BUILD / b.name
    if work.exists():
        shutil.rmtree(work)
    (work / "generated").mkdir(parents=True)
    header = proto_header(s.header) if b.fw_proto else s.header
    (work / "generated" / "soc.h").write_text(header)
    fw_src = PROTO_FW.read_text() if b.fw_proto else (ROOT / PRODUCTION[3]).read_text()
    fw_src = mutate(fw_src, b.fw_mut, b.name)
    (work / "milan_baremetal.host.c").write_text(host_firmware(fw_src, 2 if b.fw_proto else 1))
    be = PROTO_SV.read_text() if b.proto else (ROOT / PRODUCTION[0]).read_text()
    (work / "KL_nvm_backend.sv").write_text(mutate(be, b.rtl_mut, b.name))
    (work / "cosim_top.sv").write_text(mutate(WRAPPER.read_text(), b.glue_mut, b.name))
    defs = [f"-DNVM_HOST_JOURNAL_OFFSET=0x{ref.JOURNAL:x}u",
            f"-DNVM_HOST_AEM_OFFSET=0x{ref.AEM_OFFSET:x}u",
            f"-DNVM_HOST_IMAGE_OFF=0x{ref.IMAGE_OFF:x}u"]
    cc = ["gcc", "-std=gnu11", "-O2", "-g", "-Wall", "-Wextra", "-Werror",
          f"-I{work}", f"-I{HARNESS}", f"-I{STUBS}"]
    cmd(cc + defs + ["-c", str(HARNESS / "cosim_host.c"), "-o", str(work / "host.o")],
        LOGS / "build" / f"{b.name}-host.log")
    cmd(cc + ["-Wno-format", "-c", str(work / "milan_baremetal.host.c"),
              "-o", str(work / "fw.o")], LOGS / "build" / f"{b.name}-fw.log")
    gparams = [f"-G{k}={v}" for k, v in s.params.items()] + [f"-GCLK_HZ_P={CLK_HZ}"]
    if b.proto:
        gparams.append(f"-GCAP_ID_W_P={b.cap_id_w}")
    vl = ["verilator", "--cc", "--exe", "--build", "-j", "2", "--top-module", "cosim_top",
          "--Mdir", str(work / "obj"), "-Wall", "-Wno-fatal", "-Wno-UNUSEDSIGNAL",
          "-Wno-UNUSEDPARAM", "--x-assign", "unique", "--x-initial", "unique"]
    if b.proto:
        vl.append("+define+PROTO")
    vl += gparams
    vl += ["-CFLAGS", f"-std=c++17 -O2 -I{HARNESS} -I{STUBS} {' '.join(defs)}",
           "-LDFLAGS", f"{work / 'host.o'} {work / 'fw.o'}"]
    vl += [str(ROOT / p) for p in DONOR_SV]
    vl += [str(work / "KL_nvm_backend.sv"), str(work / "cosim_top.sv"),
           str(HARNESS / "cosim_bridge.cpp"), str(HARNESS / "cosim_cases.cpp"), "-o", "cosim"]
    cmd(vl, LOGS / "build" / f"{b.name}-verilator.log", timeout=3600)
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
    p = subprocess.run(["taskset", "-c", "16-31", *argv], text=True, capture_output=True,
                       timeout=900)
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


def c_copy_in_gap(rid):
    """The ERASE was granted before the arm, completed with done before the
    firmware read the ownership vector, and the WRITE of the same logical
    record was requested before that read and granted only at or after the
    certificate: the capture looked at the record inside the gap."""
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
                    f"{w['gnt'] - arm}; certificate {cert - arm}")
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
    capture was open and not yet certified or released, with that capture's
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
            return False, f"request at {op['req']}: its capture was never certified"
        ok = op["gnt"] >= cert and op["gnt"] - arm <= T_HOLD_MS * 1000 + 1000
        return ok, f"requested {op['req'] - arm} cycles after the arm, granted {op['gnt'] - arm} after it, certificate at {cert - arm}"
    return ck(f"deferred_until_certificate:0x{rid:02x}" + ("" if src == "bfm" else f":{src}"), f)


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
        refused = [ln for ln in c.r.fw if "not certified" in ln]
        return bool(refused), f"refused captures reported: {len(refused)}"
    return ck("uncertified_capture_never_flashed", f)


def c_slow_copy():
    def f(c):
        if not strobes(c, 0x8):
            return None, "no capture on this build"
        refused = [ln for ln in c.r.fw if "not certified" in ln]
        return not refused, f"refused captures {len(refused)}"
    return ck("slow_copy_certifies", f)


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


def c_cert_voided(tag):
    def f(c):
        if not c.contract(tag):
            return None, "no certificate on this build"
        st = c.o(tag)["stat"]
        held = c.r.notes.get("deferred_while_hold", {}).get("value", 1) == 0
        return (not (st >> 19) & 1) and held, f"certified {(st >> 19) & 1}, deferred during the hold {held}"
    return ck(f"grant_on_certify_edge_voids@{tag}", f)


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
    "A11_inflight_write_closes_after_arm": [c_rec("first", 0x21, "Z", "inflight_record_excluded"),
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
    "C8_ack_refused_after_verified_slot": [c_refused_ack("pre_hb"), c_rec("pre_hb", 0x20, "X2", "certified_slot_promoted"),
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
    "U3_grant_on_certify_edge": [c_cert_voided("cert")],
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
#: cases the tracked writer cannot express (they hook contract-3 strobes)
CONTRACT_ONLY = {"A6_late_ack_while_new_capture_open", "A8_identity_wrap",
                 "C1r_real_port_request_deferred", "C2r_real_port_torn_record_under_stale_mask",
                 "C2e_real_port_erased_span_under_stale_mask",
                 "C1a_real_port_arm_after_erase_done", "C1g_real_port_copy_inside_erase_write_gap",
                 "A11_inflight_write_closes_after_arm", "A12_last_byte_before_arm_done_after",
                 "C1_request_during_hold_is_deferred", "C2_hold_expiry_then_erase_with_stale_mask",
                 "C3_hold_expiry_without_producer", "C5_concurrent_arm_refused",
                 "C8_ack_refused_after_verified_slot", "D4e_silent_inside_capture",
                 "U2_close_on_arm_edge", "U3_grant_on_certify_edge"}
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
            "E1_dyn_change_ack_then_second_change"]


PRODUCER = {'A11_inflight_write_closes_after_arm': 'real + bfm', 'A12_last_byte_before_arm_done_after': 'real + bfm', 'A1_stable_no_change': 'real', 'A2_write_between_verify_and_ack': 'real, #418', 'A3_write_done_on_ack_edge': 'bfm, #418 control', 'A4_write_after_ack': 'real', 'A5_stray_duplicate_ack': 'real + stray', 'A6_late_ack_while_new_capture_open': 'real + stray', 'A8_identity_wrap': 'real + stray', 'A9_updates_during_slow_erase': 'real', 'B10_partial_write_never_closes': 'real + bfm', 'B1_erase_error_full_span': 'real', 'B2_erase_error_partial_span': 'real', 'B3_erase_error_no_byte': 'real', 'B4_write_error_after_erase': 'real', 'B5_erase_then_no_write_yet': 'real + bfm', 'B6_two_failed_records_partial': 'real + bfm', 'B6b_two_failed_records_full': 'real + bfm', 'B7_first_boot_erased_records': 'real', 'B8_first_boot_failed_erase': 'real + bfm', 'B9_abandoned_write_stream': 'real + bfm', 'C1_request_during_hold_is_deferred': 'real + bfm', 'C1r_real_port_request_deferred': 'real', 'C2_hold_expiry_then_erase_with_stale_mask': 'real + bfm', 'C2r_real_port_torn_record_under_stale_mask': 'real', 'C3_hold_expiry_without_producer': 'real', 'C5_concurrent_arm_refused': 'real + stray', 'C7_late_ack_after_commit_deadline': 'real', 'C8_ack_refused_after_verified_slot': 'real + stray', 'D1_writer_loss_and_recovery': 'real', 'D4c_accepted_write_silent': 'real', 'D4d_readiness_withheld': 'real', 'D4e_silent_inside_capture': 'real', 'E1_dyn_change_ack_then_second_change': 'real dyn store', 'E3_binding_inside_manager_debounce': 'real', 'F2_reported_flash_failure': 'real', 'F3_flash_absent_producer_unblocked': 'real', 'U1_post_reset_ack': 'unit', 'U2_close_on_arm_edge': 'unit', 'U3_grant_on_certify_edge': 'unit', 'C2e_real_port_erased_span_under_stale_mask': 'real', 'C1a_real_port_arm_after_erase_done': 'real', 'C1g_real_port_copy_inside_erase_write_gap': 'real'}


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
    checks = list(CHECKS.get(run.case, [])) + [c_no_101()]
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


# ------------------------------------------------------------- firmware size
SIZE_STUBS = HARNESS / "size_stubs"


def fw_size(shapes: dict) -> list[dict]:
    """Both writers compiled for the product's RV32I target at -Os against the
    SAME target-like stubs, fences intact, so the delta is the writer's own."""
    out = []
    for sname, s in shapes.items():
        for label, proto in (("tracked", False), ("proto", True)):
            hdr = proto_header(s.header) if proto else s.header
            hdr = "\n".join(ln for ln in hdr.splitlines() if "nvm_host.h" not in ln)
            hdr = hdr.replace("(uintptr_t)nvm_host_ddr", "0x7f700000u") + "\n"
            w = BUILD / f"size-{label}-{sname}"
            (w / "generated").mkdir(parents=True, exist_ok=True)
            (w / "generated" / "soc.h").write_text(hdr)
            src = PROTO_FW if proto else ROOT / PRODUCTION[3]
            cmd(["riscv64-elf-gcc", "-march=rv32i", "-mabi=ilp32", "-Os", "-c", f"-I{w}",
                 f"-I{SIZE_STUBS}", str(src), "-o", str(w / "fw.o")],
                LOGS / "size" / f"{label}-{sname}-cc.log")
            p = cmd(["riscv64-elf-size", str(w / "fw.o")], LOGS / "size" / f"{label}-{sname}-size.log")
            text, data, bss = (int(x) for x in p.stdout.splitlines()[1].split()[:3])
            out.append(dict(tag=f"{label}-{sname}", text=text, data=data, bss=bss))
    return out


# ---------------------------------------------------------------------- area
def area(proto: bool, shape_params: dict, nodsp: bool, tag: str) -> dict:
    """sv2v then yosys `synth_xilinx -family xc7 [-nodsp] -flatten`, parsed as
    syn/yosys/ooc.sh parses it (LUT_TOT = LUT + the LUTRAM LUT6 equivalents)."""
    work = BUILD / "area"
    work.mkdir(parents=True, exist_ok=True)
    src = PROTO_SV if proto else ROOT / PRODUCTION[0]
    v = work / f"{tag}.v"
    p = cmd(["sv2v", "--top=KL_nvm_backend", "-DSYNTHESIS", str(src)], LOGS / "area" / f"{tag}-sv2v.log")
    v.write_text(p.stdout)
    chp = "".join(f" chparam -set {k} {val} KL_nvm_backend;" for k, val in shape_params.items())
    script = (f"read_verilog {v};{chp} synth_xilinx -family xc7{' -nodsp' if nodsp else ''} "
              f"-top KL_nvm_backend -flatten; stat")
    p = cmd(["yosys", "-q", "-p", script, "-l", str(work / f"{tag}.log")],
            LOGS / "area" / f"{tag}-yosys.log", timeout=3600)
    text = (work / f"{tag}.log").read_text()
    blocks = text.split("=== KL_nvm_backend ===")
    last = blocks[-1]
    lut = lram = ff = dsp = c4 = r36 = 0
    for ln in last.splitlines():
        f = ln.split()
        if len(f) < 2 or not f[0].isdigit():
            continue
        n, t = int(f[0]), f[1]
        if re.fullmatch(r"LUT[1-6]", t):
            lut += n
        elif t.startswith("RAM") and not t.startswith("RAMB"):
            lram += n * (4 if t in ("RAM32M", "RAM64M", "RAM128X1D") else
                         2 if t in ("RAM32X1D", "RAM64X1D") else 1)
        elif re.fullmatch(r"FD[CPRS]E?", t):
            ff += n
        elif t == "DSP48E1":
            dsp += n
        elif t == "CARRY4":
            c4 += n
        elif t == "RAMB36E1":
            r36 += n
    return dict(tag=tag, LUT=lut, LUTRAM=lram, LUT_TOT=lut + lram, FF=ff, DSP=dsp,
                CARRY4=c4, RAMB36=r36)


# ---------------------------------------------------------------------- main
def all_builds(quick: bool) -> list[Build]:
    builds = [Build("prod-1x1", "1x1", False, False), Build("proto-1x1", "1x1", True, True),
              Build("proto-w2-1x1", "1x1", True, True, cap_id_w=2),
              Build("mix-newfw-oldgw-1x1", "1x1", False, True)]
    if not quick:
        builds += [Build("prod-8x8", "8x8", False, False), Build("proto-8x8", "8x8", True, True)]
        builds += [Build(f"mut-{m}", "1x1", True, True, rtl_mut=s) for m, s in RTL_MUT.items()]
        builds += [Build(f"mut-{m}", "1x1", True, True, fw_mut=s) for m, s in FW_MUT.items()]
        builds += [Build(f"mut-{m}", "1x1", True, True, glue_mut=s) for m, s in GLUE_MUT.items()]
    for b in builds:
        b.binary = BUILD / b.name / "obj" / "cosim"
    return builds


def case_jobs(b: Build, cases: list[str]) -> list[tuple]:
    if b.name.startswith("mix-"):
        return [(b, "A1_stable_no_change", "", ())]
    out = []
    for case in (CORE_8X8 if b.shape == "8x8" else cases):
        if b.name == "proto-w2-1x1" and case != "A8_identity_wrap":
            continue
        if case == "E3_binding_inside_manager_debounce":
            out += [(b, case, f"d1={d}", ("--d1", d)) for d in ("0", "1")]
        else:
            out.append((b, case, "", ()))
    return out


def save_run(r: Run) -> Run:
    (r.outdir / "meta.json").write_text(json.dumps(dict(
        case=r.case, build=r.build, variant=r.variant, exit=r.exit, wall_s=r.wall_s)))
    return r


def load_run(meta: Path) -> Run:
    m = json.loads(meta.read_text())
    out = meta.parent
    obs, notes, evts, fw, done, pending = {}, {}, [], [], False, False
    for ln in (out / "stdout.log").read_text().splitlines():
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
            done, pending = True, ln.endswith("hooks_pending=1")
    return Run(m["case"], m["build"], m["variant"], m["exit"], m["wall_s"], obs, notes, evts,
               fw, done, pending, out)


def phase_run(builds, shapes, cases, jobs):
    jobsq = [j for b in builds for j in case_jobs(b, cases)]
    with cf.ThreadPoolExecutor(max_workers=jobs) as ex:
        runs = list(ex.map(lambda j: save_run(run_case(j[0], shapes, j[1], j[2], j[3])), jobsq))
    pc = [(next(x for x in builds if x.name == r.build), "R_power_cycle", f"{r.case}@end",
           ("--slot-a", str(r.outdir / "end-slotA.bin"),
            "--slot-b", str(r.outdir / "end-slotB.bin")))
          for r in runs if r.case in POWER_CYCLE and "end" in r.obs]
    with cf.ThreadPoolExecutor(max_workers=jobs) as ex:
        list(ex.map(lambda j: save_run(run_case(j[0], shapes, j[1], j[2], j[3])), pc))


def phase_grade(builds, shapes, before, skip_area) -> int:
    graded = {}
    shape_of = {b.name: b.shape for b in builds}
    for meta in sorted(RUNS.glob("*/*/meta.json")):
        r = load_run(meta)
        if r.build not in shape_of:
            continue
        graded[(r.build, r.case, r.variant)] = (r, grade(r, shapes[shape_of[r.build]]))
    findings = []

    def res(build, case, variant, check):
        g = graded.get((build, case, variant))
        return None if g is None else g[1].get(check, (None, None))[0]

    for (bname, case, variant), (r, g) in sorted(graded.items()):
        if not bname.startswith("proto-") or bname == "proto-w2-1x1":
            continue
        for chk, (st, det) in g.items():
            if st == "fail" and (case, variant, chk) not in PROTO_EXPECTED_FAIL:
                findings.append(f"PROTOTYPE {bname} {case} {variant} {chk}: {det}")
            if st == "n/a" and case not in CONTRACT_ONLY:
                findings.append(f"PROTOTYPE {bname} {case} {variant} {chk}: not expressible")
    for (case, variant, chk), why in PROTO_EXPECTED_FAIL.items():
        if res("proto-1x1", case, variant, chk) != "fail":
            findings.append(f"EXPECTED-FAIL control did not fail: {case} {variant} {chk} ({why})")
    for bname in [b.name for b in builds if b.name.startswith("prod-")]:
        for case, chk, what in PROD_MUST_FAIL:
            if res(bname, case, "", chk) != "fail":
                findings.append(f"TRACKED {bname} did not fail {case} {chk} ({what})")
    if res("proto-w2-1x1", "A8_identity_wrap", "", "ack_retires_only_slot@end:0x20") != "fail":
        findings.append("identity wrap: the 2-bit identity did not alias")
    if res("proto-1x1", "A8_identity_wrap", "", "ack_retires_only_slot@end:0x20") != "pass":
        findings.append("identity wrap: the 16-bit identity did not hold")
    mix = graded.get(("mix-newfw-oldgw-1x1", "A1_stable_no_change", ""))
    mix_ok = mix is not None and any("does not carry saved-state contract 3" in ln for ln in mix[0].fw) \
        and mix[0].obs.get("end", {}).get("erases", 1) == 0
    if not mix_ok:
        findings.append("new writer on old gateware did not refuse to persist")
    mutants = {}
    for b in builds:
        if not b.name.startswith("mut-"):
            continue
        m = b.name[4:]
        kcase, kcheck = KILLER[m]
        st = res(b.name, kcase, "", kcheck)
        kills = sorted({f"{case}:{chk}" for (bn, case, v), (_, g) in graded.items()
                        if bn == b.name for chk, (s2, _) in g.items() if s2 == "fail"})
        mutants[m] = dict(killer=f"{kcase}:{kcheck}", killer_result=st, all_failing=kills)
        if st != "fail":
            findings.append(f"MUTANT {m} survived its named check {kcase}:{kcheck} ({st})")

    refusals = {}
    s1 = shapes["1x1"]
    for label, fw, hdr, needle in (
            ("old_writer_new_generator", (ROOT / PRODUCTION[3]).read_text(), proto_header(s1.header),
             "MILAN_NVM_IMAGE_BASE"),
            ("new_writer_old_generator", PROTO_FW.read_text(), s1.header, "contract 3")):
        w = BUILD / f"refusal-{label}"
        (w / "generated").mkdir(parents=True, exist_ok=True)
        (w / "generated" / "soc.h").write_text(hdr)
        (w / "fw.c").write_text(host_firmware(fw, 2 if "new_writer" in label else 1))
        p = cmd(["gcc", "-std=gnu11", "-fsyntax-only", "-Wall", "-Wextra", "-Werror",
                 "-Wno-format", f"-I{w}", f"-I{STUBS}", str(w / "fw.c")],
                LOGS / f"refusal-{label}.log", check=False)
        ok = p.returncode != 0 and needle in (p.stdout + p.stderr)
        refusals[label] = dict(exit=p.returncode, refused=ok)
        if not ok:
            findings.append(f"build-time refusal {label} did not refuse")

    sizes = fw_size(shapes)
    areas = []
    if not skip_area:
        for sname, s in shapes.items():
            for proto in (False, True):
                for nodsp in (False, True):
                    tag = f"{'proto' if proto else 'tracked'}-{sname}{'-nodsp' if nodsp else ''}"
                    areas.append(area(proto, s.params, nodsp, tag))
        # calibration: the tracked module at the name bound design page
        # section 8.3 was measured at, which must reproduce that table's row
        areas.append(area(False, dict(shapes["1x1"].params, N_NAME_P=30), False,
                          "tracked-1x1-page-bound-30"))
        areas.append(area(False, dict(shapes["1x1"].params, N_NAME_P=30), True,
                          "tracked-1x1-page-bound-30-nodsp"))

    after = {p: sha(ROOT / p) for p in PRODUCTION}
    if after != before:
        findings.append("a production file changed during the run")
    summary = dict(
        finished=now(), head=EXPECT_HEAD, pins=EXPECT_PINS,
        production_sha256=before, production_unchanged=(after == before),
        clk_hz_model=CLK_HZ, t_hold_ms=T_HOLD_MS,
        shapes={n: dict(params=s.params, img_len=s.img_len, records=len(s.recs))
                for n, s in shapes.items()},
        producer=PRODUCER,
        runs=[dict(build=r.build, case=r.case, variant=r.variant, exit=r.exit,
                   wall_s=round(r.wall_s, 2),
                   model_ms=max([o["ms"] for o in r.obs.values()], default=0),
                   cycles=max([o["cycle"] for o in r.obs.values()], default=0),
                   checks={k: list(v) for k, v in g.items()})
              for (_, _, _), (r, g) in sorted(graded.items())],
        mutants=mutants, refusals=refusals, area=areas, fw_size=sizes, findings=findings,
        manifest=MANIFEST)
    (HERE / "results.json").write_text(json.dumps(summary, indent=1) + "\n")
    lines = []
    for (bname, case, variant), (r, g) in sorted(graded.items()):
        np_ = sum(1 for v in g.values() if v[0] == "pass")
        fl = [k for k, v in g.items() if v[0] == "fail"]
        na = sum(1 for v in g.values() if v[0] == "n/a")
        lines.append(f"{bname:40s} {case + ('~' + variant if variant else ''):52s} "
                     f"pass={np_:2d} fail={len(fl):2d} n/a={na:2d} {' '.join(fl)}")
    for m, v in sorted(mutants.items()):
        lines.append(f"MUTANT {m:40s} killer {v['killer']} -> {v['killer_result']}; "
                     f"{len(v['all_failing'])} failing checks")
    for a in areas:
        lines.append(f"AREA {a['tag']:34s} LUT={a['LUT']:5d} LUTRAM={a['LUTRAM']:4d} "
                     f"LUT_TOT={a['LUT_TOT']:5d} FF={a['FF']:4d} DSP={a['DSP']} CARRY4={a['CARRY4']}")
    for sz in sizes:
        lines.append(f"FWSIZE {sz['tag']:14s} text={sz['text']} data={sz['data']} bss={sz['bss']}")
    for k, v in refusals.items():
        lines.append(f"REFUSAL {k}: exit {v['exit']} refused {v['refused']}")
    lines += [f"FINDING {f}" for f in findings] or ["NO FINDINGS: every expectation holds"]
    (HERE / "results.txt").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))
    return 1 if findings else 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--jobs", type=int, default=8)
    ap.add_argument("--quick", action="store_true", help="1x1 tracked and prototype only")
    ap.add_argument("--skip-area", action="store_true")
    ap.add_argument("--phase", choices=("all", "build", "run", "grade"), default="all")
    ap.add_argument("--builds", default="*", help="fnmatch pattern over build names")
    args = ap.parse_args()
    jobs = min(args.jobs, 8)
    for d in (BUILD, RUNS, LOGS, HERE / "tmp"):
        d.mkdir(parents=True, exist_ok=True)
    before = preflight()
    shapes = {n: shape(n) for n in (("1x1",) if args.quick else ("1x1", "8x8"))}
    builds = all_builds(args.quick)
    import fnmatch
    sel = [b for b in builds if fnmatch.fnmatch(b.name, args.builds)]
    if args.phase in ("all", "build"):
        with cf.ThreadPoolExecutor(max_workers=max(1, jobs // 2)) as ex:
            list(ex.map(lambda b: do_build(b, shapes), sel))
    if args.phase in ("all", "run"):
        cases = subprocess.check_output([str(builds[1].binary), "--list"], text=True).split()
        phase_run([b for b in sel if b.binary.exists()], shapes, cases, jobs)
    if args.phase == "build" or args.phase == "run":
        (LOGS / f"manifest-{args.phase}-{now().replace(':', '')}.json").write_text(
            json.dumps(MANIFEST, indent=1) + "\n")
        return 0
    return phase_grade(builds, shapes, before, args.skip_area)


if __name__ == "__main__":
    sys.exit(main())
