#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Build, run and grade the D3 co-simulation (design evidence, milan-fpga #500).

What is REAL in every build: the pinned processor's KL_aecp_dyn_state,
KL_aecp_desc_store, KL_acmp_nvm_shadow and KL_pp_nvm_port (424c688f), the
shipping hdl/milan/KL_nvm_backend.sv and the shipping writer
sw/firmware/milan_baremetal/milan_baremetal.c compiled for the host exactly as
tb/verilator/nvm_cosim compiles it, with ONE counted change: milan_init loads
the entity model before nvm_boot (the design page's section 8.2). PROTOTYPE:
KL_aecp_nvm_writer and KL_pp_nvm_mgr_arb. MODEL: the uCPU (a bus-functional
model with the dispatch hold-off) and the parent's map plane.

Every case is graded by NAMED checks over the journal the case binary prints,
with the repository's own scripts/nvm_klj2.py decoding every slot. Every
mutant is killed by the ONE check this file names for it, or the run fails.

    run.py prep                 build the shape inputs (both shapes)
    run.py build [NAME...]      build co-simulations (default: every build)
    run.py run   [--builds ..]  run and grade; writes results.txt/results.json

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
DONOR_SV = [PP / "acmp/pp_acmp_pkg.sv", PP / "aecp/KL_aecp_dyn_state.sv",
            PP / "aecp/KL_aecp_desc_store.sv", PP / "acmp/KL_acmp_nvm_shadow.sv",
            PP / "packet_engine/KL_pp_nvm_port.sv"]
BACKEND = ROOT / "hdl/milan/KL_nvm_backend.sv"
WRITER = ROOT / "sw/firmware/milan_baremetal/milan_baremetal.c"
SHAPES = {"1x1": "configs/endstation_ax7101_1x1_tdm8.yaml",
          "8x8": "configs/endstation_ax7101_8x8.yaml"}
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
    rtl_mut: str = ""
    glue_mut: str = ""
    arb_mut: str = ""
    fw_old_boot: bool = False
    tracked: bool = False
    binary: Path | None = None


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
        "          if (desc_img_valid_i) begin\n            cur_r <= '0; st_r <= R_NEXT;",
        "          if (1'b1) begin\n            cur_r <= '0; st_r <= R_NEXT;"),
    "M09_apply_blindly": ("writer",
        "        R_AUX: begin\n          // per-group value judgement, by the rule the SET program applies\n          unique case (cg_r)",
        "        R_AUX: begin\n          // per-group value judgement, by the rule the SET program applies\n"
        "          if (is_scalar_w && !(cg_r == 4'(G_FMTI) || cg_r == 4'(G_FMTO))) st_r <= R_APPLY; else\n          unique case (cg_r)"),
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
    "G03_restore_writes_are_changes": ("top",
        "  assign u_dyn_ack_w  = !snoop_off_i && !d3_own_w && ub_req_i && ub_we_i && dyn_sel_w && dyn_ready_w;",
        "  assign u_dyn_ack_w  = !snoop_off_i && (d3_own_w ? (sb_req_w && sb_we_w && dyn_sel_w) : (ub_req_i && ub_we_i && dyn_sel_w && dyn_ready_w));"),
    "M14_clear_by_index": ("writer",
        "    assign clr_w[gs] = clr_en_w && (cg_r == grp_f(SW_C'(gs)))\n"
        "                     && (ci_r[7:0] == 8'(gs - base_f(grp_f(SW_C'(gs)))));",
        "    assign clr_w[gs] = clr_en_w\n"
        "                     && (ci_r[7:0] == 8'(gs - base_f(grp_f(SW_C'(gs)))));"),
    "M15_overflow_forgets_the_change": ("writer",
        "  assign fl_giveup_w  = fl_err_w && (32'(retry_r) >= RETRY_MAX_P);",
        "  assign fl_giveup_w  = (fl_err_w && (32'(retry_r) >= RETRY_MAX_P)) || fl_ovf_w;"),
    "M17_trigger_misses_ptof": ("writer",
        "    assign set_w[S_PTOF_C + gi] = dyn_w && (u_sel_w == 13'd5) && (u_didx_i == 16'(gi));",
        "    assign set_w[S_PTOF_C + gi] = 1'b0;"),
    "M18_trigger_misses_names": ("writer",
        "    assign set_w[S_NAME_C + gi] = name_w && (u_addr_i[15:6] == 10'(gi));",
        "    assign set_w[S_NAME_C + gi] = 1'b0;"),
    "M19_trigger_misses_out_maps": ("writer",
        "    assign set_w[S_MAPO_C + gi] = map_w && (me_type_i == T_SPO_C) && (me_idx_i == 16'(gi));",
        "    assign set_w[S_MAPO_C + gi] = 1'b0;"),
    "M16_single_pass_restore": ("writer",
        "      rpass_r <= 1'b0;\n",
        "      rpass_r <= 1'b1;\n"),
    "G04_blank_ignores_d3": ("top",
        "  assign restore_blank_o = mgr_blank_w & d3_blank_w;",
        "  assign restore_blank_o = mgr_blank_w;"),
    "A01_grant_cycle_not_busy": ("arb",
        "  assign m0_busy_o   = p_busy_i || (own_r == O_M1) || iss1_w;",
        "  assign m0_busy_o   = p_busy_i || (own_r == O_M1);"),
}

#: case K15's sweep: the D3 writer released N cycles after the binding
#: manager enters H_FL_CRC. The base build must commit both records at EVERY
#: N and must reach the grant-cycle collision at one N at least.
K15_SWEEP = [f"g{n}" for n in range(0, 8)]

#: mutant -> (case, variant, THE ONE CHECK that must kill it, shape). The
#: variant "*" is K15's sweep: killed when the check fails at any N.
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
    "M17_trigger_misses_ptof": ("K1_single_change_converges", "", "no_durable_claim_over_unsaved", "1x1"),
    "M18_trigger_misses_names": ("K10_name_change_converges", "", "no_durable_claim_over_unsaved", "1x1"),
    "M19_trigger_misses_out_maps": ("K12_map_change_converges", "", "no_durable_claim_over_unsaved", "1x1"),
    "G01_pend_misses_d3": ("K1_single_change_converges", "", "no_durable_claim_over_unsaved", "1x1"),
    "G02_restore_done_without_d3": ("V1b_restore_everything", "", "entity_enabled_after_restore@boot", "1x1"),
    "G03_restore_writes_are_changes": ("V1b_restore_everything", "", "restore_sets_no_dirty@boot", "1x1"),
    "G04_blank_ignores_d3": ("V7_names_only", "", "blank_is_both_walks@boot", "1x1"),
    "A01_grant_cycle_not_busy": ("K15_binding_on_the_d3_grant_cycle", "*", "both_records_committed", "1x1"),
    "F01_old_boot_order": ("V1b_restore_everything", "", "value_restored:0x50", "1x1"),
}

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
    """Refuse to run if the donor moved the states the harness names."""
    src = (PP / "acmp/KL_acmp_nvm_shadow.sv").read_text()
    m = re.search(r"typedef enum logic \[3:0\] \{(.*?)\} hstate_e;", src, re.S)
    if not m:
        raise SystemExit("KL_acmp_nvm_shadow: hstate_e not found")
    names = re.findall(r"^\s*(H_[A-Z_]+)", m.group(1), re.M)
    for name, code in M0_STATES.items():
        if name not in names or names.index(name) != code:
            raise SystemExit(f"KL_acmp_nvm_shadow: {name} is not encoding {code} ({names})")


def mutate_text(key: str, text: str, name: str) -> str:
    k, old, new = MUTATIONS[name]
    if k != key:
        return text
    if text.count(old) != 1:
        raise SystemExit(f"mutation {name}: seam count {text.count(old)}")
    return text.replace(old, new)


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
    return text


def all_builds(shapes: list[str]) -> list[Build]:
    out = [Build(f"base-{s}", s) for s in shapes]
    out.append(Build("tracked-1x1", "1x1", tracked=True))
    for m in MUTATIONS:
        kind = MUTATIONS[m][0]
        b = Build(f"mut-{m}", KILLERS[m][3])
        if kind == "writer":
            b.rtl_mut = m
        elif kind == "top":
            b.glue_mut = m
        else:
            b.arb_mut = m
        out.append(b)
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
    w = (PROTO / "KL_aecp_nvm_writer.proto.sv").read_text()
    a = (PROTO / "KL_pp_nvm_mgr_arb.proto.sv").read_text()
    t = (HARNESS / "d3_top.sv").read_text()
    if b.rtl_mut:
        w = mutate_text("writer", w, b.rtl_mut)
    if b.glue_mut:
        t = mutate_text("top", t, b.glue_mut)
    if b.arb_mut:
        a = mutate_text("arb", a, b.arb_mut)
    (work / "KL_aecp_nvm_writer.sv").write_text(w)
    (work / "KL_pp_nvm_mgr_arb.sv").write_text(a)
    (work / "d3_top.sv").write_text(t)
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
    if not b.tracked:
        rtl.append(work / "KL_aecp_nvm_writer.sv")
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
    obs, evts, fw, done, notes = {}, [], [], False, {}
    for ln in p.stdout.splitlines():
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
    return Run(case, b.name, variant, p.returncode, obs, evts, fw, done, out, slots, notes)


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


def map_bytes(maps: list, clusters: int) -> bytes:
    v = b"".join(struct.pack(">HHHH", *m) for m in maps)
    return v + b"\xff" * (8 * clusters - len(v))


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
        pre = {k: g.ans(f"pre.{k}.valid")[0] for k in ("cfg", "rate", "clks", "fmti0", "ptof0")}
        g.check("rows_cleared_before_restore@boot", all(v == 0 for v in pre.values()),
                f"valid flags before the restore {pre}")
        cut = extra["cut_slots"]
        def restored(rid, tag, width):
            v, _ = g.ans(f"post.{tag}.value")
            valid, _ = g.ans(f"post.{tag}.valid")
            want = cut.get(rid)
            if want is None:
                return
            ok = valid == 1 and v is not None and (v & ((1 << (8 * width)) - 1)) == int.from_bytes(want, "big")
            g.check(f"value_restored:{rid:#04x}", ok, f"restored {v} valid {valid}, slot {want.hex()}")
        restored(0x50, "ptof0", 4)
        #! against the value V1a SET, not against the slot: the check a
        #! build that saves nothing (the tracked glue) must fail
        pv, _ = g.ans("post.ptof0.value")
        pvalid, _ = g.ans("post.ptof0.valid")
        g.check("set_value_survives_power_cycle:0x50", pvalid == 1 and pv == 1500000,
                f"restored {pv} valid {pvalid}, set 1500000")
        restored(0x30, "fmti0", 8)
        if s.rates and len(s.rates) > 1:
            restored(0x02, "rate", 4)
        if s.clk_count > 1:
            restored(0x0A, "clks", 2)
        for rid, tag in ((0x80, "name0"), (0x80 + s.params["N_NAME_P"] - 1, "namelast")):
            got = g.name_of(f"post.{tag}")
            want = cut.get(rid)
            g.check(f"value_restored:{rid:#04x}", want is not None and got == want and
                    got != s.names[rid - 0x80],
                    f"restored {got[:24] if got else None}, slot {want[:24] if want else None}")
            after = g.name_of(f"after.{tag}")
            g.check(f"restored_name_survives_first_command:{rid:#04x}", want is not None and after == want,
                    f"after the first command {after[:24] if after else None}")
        for rid, key in ((0x70, "maps_out"), (0x60, "maps_in")):
            mo = r.obs.get("restored", {}).get(key, [None])[0]
            want = cut.get(rid)
            if want is None:
                continue
            g.check(f"value_restored:{rid:#04x}", mo == want.hex(),
                    f"live port 0 set {mo[:32] if mo else None}.., slot {want.hex()[:32]}..")
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
        g.check("restore_counts@boot", o.get("rs_ref") == 0 and o.get("rs_app", 0) + o.get("rs_blank", 0) <= n_rec,
                f"applied {o.get('rs_app')} refused {o.get('rs_ref')} blank {o.get('rs_blank')} of {n_rec}")
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
        g.check("refused_group_falls_back_to_default:0x70",
                o.get("maps_out", [None])[0] == want and live == s.def_fmt_out[0],
                f"live OUT0 equals the default {o.get('maps_out', [None])[0] == want}, fmto0 {live:#x}")
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
        g.check("torn_walk_applies_nothing@boot",
                valid == 0 and o.get("restore_fail") == 1 and o.get("d3_fail") == 1 and o.get("rs_app") == 0,
                f"ptof0 valid {valid} (its record was read whole before the torn one), restore fail "
                f"{o.get('restore_fail')}, D3 fail {o.get('d3_fail')}, applied {o.get('rs_app')}")
    elif c == "V10_blank_first_boot":
        o = r.obs.get("restored", {})
        valid, _ = g.ans("post.ptof0.valid")
        g.check("blank_boot_applies_nothing@boot", o.get("rs_blank") == n_rec and o.get("rs_app") == 0 and
                valid == 0 and o.get("blank") == 1,
                f"blank {o.get('rs_blank')} of {n_rec}, applied {o.get('rs_app')}, ptof0 valid {valid}, "
                f"status blank {o.get('blank')}")
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
    return g


# ----------------------------------------------------------------- the plan
BASE_CASES = [
    "K1_single_change_converges", "K2_change_during_record_write", "K3_two_changes_one_debounce",
    "K4_second_record_in_flight", "K4g_second_group_in_flight", "K5_change_on_the_done_edge",
    "K8_record_write_error_retried", "K9_record_write_given_up", "K10_name_change_converges",
    "K11_name_latch_waits_for_the_program", "K12_map_change_converges",
    "K13_binding_and_d3_share_the_port", "K14_identify_is_not_persisted",
]
CHAINS = [("K6a_cut_after_record_before_commit", "K6b_restore_after_cut"),
          ("K7a_cut_after_ack", "K7b_restore_after_ack"),
          ("K17a_cut_during_record_write", "K17b_restore_after_cut_in_write"),
          ("K18a_cut_inside_the_debounce", "K18b_restore_after_cut_in_debounce"),
          ("V1a_set_everything", "V1b_restore_everything"),
          ("V6a_set_coupled_narrower_pair", "V6b_restore_coupled_pair")]
#: cases one shape alone can express: K16 needs an output port whose stream
#: channels outnumber its clusters (8x8: 72 against 9; 1x1: 16 against 17)
SHAPE_CASES = {"8x8": ["K16_map_set_larger_than_its_record"]}
CRAFTED = ["V2_refused_rate", "V3_refused_map_for_a_removed_cluster", "V4_refused_configuration_index",
           "V5_record_corrupted_after_the_load", "V7_names_only", "V8_orphaning_format_reverted",
           "V9_refused_maps_revert_their_formats", "V11_torn_read_restores_nothing"]


def crafted_for(s: Shape, case: str) -> tuple[tuple, dict]:
    cls_out0 = s.recs[0x70][2] // 8
    two = narrower(s.def_fmt_out[0], 2)
    if case == "V2_refused_rate":
        over = {0x02: (12345).to_bytes(4, "big")}
    elif case == "V3_refused_map_for_a_removed_cluster":
        over = {0x70: map_bytes([(0, 0, cls_out0 + 3, 0)], cls_out0)}
    elif case == "V4_refused_configuration_index":
        over = {0x00: (1).to_bytes(2, "big")}
    elif case == "V5_record_corrupted_after_the_load":
        over = {0x50: (1500000).to_bytes(4, "big"), 0x51: (1600000).to_bytes(4, "big")}
    elif case == "V7_names_only":
        over = {0x80: b"V7 names only restore".ljust(64, b"\x00")}
    elif case == "V8_orphaning_format_reverted":
        over = {0x40: two.to_bytes(8, "big")}
    elif case == "V9_refused_maps_revert_their_formats":
        over = {0x40: two.to_bytes(8, "big"), 0x70: map_bytes([(0, 0, cls_out0 + 3, 0)], cls_out0)}
    elif case == "V11_torn_read_restores_nothing":
        over = {0x50: (1100011).to_bytes(4, "big"), 0x80: b"V11 name".ljust(64, b"\x00")}
    else:
        raise SystemExit(case)
    return crafted(s, case, over), over


def plan(build: Build) -> list:
    """(case, variant, slots-from) for one build: base builds run everything;
    the tracked build runs what reproduces today; a mutant runs the one case
    (and chain, or K15's whole sweep) its killer lives in."""
    items = []
    if build.name.startswith("base-"):
        items += [(c, "", None) for c in BASE_CASES + CRAFTED + ["V10_blank_first_boot"]]
        items += [(c, "", None) for c in SHAPE_CASES.get(build.shape, [])]
        items += [(a, "", None) for a, _b in CHAINS] + [(b, "", a) for a, b in CHAINS]
        items += [("V1b_restore_everything", "stale", "V1a_set_everything")]
        if build.shape == "1x1":
            items += [("K15_binding_on_the_d3_grant_cycle", v, None) for v in K15_SWEEP]
    elif build.tracked:
        items += [(c, "", None) for c in TRACKED_CASES]
        items += [("V1a_set_everything", "", None), ("V1b_restore_everything", "", "V1a_set_everything")]
    else:
        m = build.name[4:]
        case, variant, _k, _s = KILLERS[m]
        if variant == "*":
            items += [(case, v, None) for v in K15_SWEEP]
            return items
        for a, b in CHAINS:
            if case == b:
                items.append((a, "", None))
                items.append((b, variant, a))
                break
        else:
            items.append((case, variant, None))
        if m == "M13_restore_applies_nothing":
            items.append(("V1b_restore_everything", "stale", "V1a_set_everything"))
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
    ap.add_argument("action", choices=["prep", "build", "run"])
    ap.add_argument("names", nargs="*")
    ap.add_argument("--shapes", default="1x1,8x8")
    ap.add_argument("--jobs", type=int, default=8)
    ap.add_argument("--pool", type=int, default=4)
    args = ap.parse_args()
    check_m0_encoding()
    shapes_wanted = args.shapes.split(",")
    shapes = {n: prep_shape(n) for n in shapes_wanted}
    builds = [b for b in all_builds(shapes_wanted) if b.shape in shapes]
    if args.names:
        builds = [b for b in builds if b.name in args.names]
    if args.action == "prep":
        for n, s in shapes.items():
            print(f"shape {n}: {len(s.recs)} records, params {s.params}, rates {s.rates}, clk {s.clk_count}, "
                  f"fmt_out {[hex(f) for f in s.def_fmt_out]}, fmt_in {[hex(f) for f in s.def_fmt_in]}")
        return 0
    if args.action == "build":
        with cf.ThreadPoolExecutor(max_workers=args.pool) as ex:
            futs = {ex.submit(do_build, b, shapes[b.shape], args.jobs): b for b in builds}
            for f in cf.as_completed(futs):
                b = f.result()
                print(f"built {b.name}")
        return 0
    # run
    for b in builds:
        b.binary = OUT / "build" / b.name / "obj" / "d3sim"
        if not b.binary.exists():
            raise SystemExit(f"{b.name} is not built")
    allres = {}
    with cf.ThreadPoolExecutor(max_workers=args.pool) as ex:
        futs = {ex.submit(execute, b, shapes[b.shape]): b for b in builds}
        for f in cf.as_completed(futs):
            b = futs[f]
            allres[b.name] = f.result()
    report(allres)
    return 0


def report(allres: dict) -> None:
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
    # verdicts
    verdict = []
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
            case, variant, killer, _s = KILLERS[m]
            killed, where = False, None
            for r, g in res:
                if r.case != case or (variant != "*" and r.variant != variant):
                    continue
                if killer in g.checks and not g.checks[killer][0]:
                    killed, where = True, r.case + (f"~{r.variant}" if r.variant else "")
                    break
            if not killed:
                fail += 1
            tag = where or (case + (f"~{variant}" if variant else ""))
            verdict.append(f"MUTANT {m}: {'KILLED' if killed else 'SURVIVED'} by {tag} : {killer}")
            if m == "M13_restore_applies_nothing":
                for r, g in res:
                    if r.variant == "stale":
                        naive = g.checks.get("value_restored:0x50", (None,))[0]
                        cleared = g.checks.get("rows_cleared_before_restore@boot", (None,))[0]
                        ok = naive is True and cleared is False
                        if not ok:
                            fail += 1
                        verdict.append(f"CONTROL stale store under M13: naive read-back "
                                       f"{'PASSES' if naive else 'FAILS'}, cleared-first "
                                       f"{'FAILS' if cleared is False else 'PASSES'} -> "
                                       f"{'as required' if ok else 'NOT AS REQUIRED'}")
    total = sum(len(g.checks) for res in allres.values() for _r, g in res)
    runs = sum(len(res) for res in allres.values())
    summary = f"SUMMARY runs {runs}, checks {total}, verdict failures {fail}"
    text = "\n".join(lines + [""] + verdict + ["", summary]) + "\n"
    (HERE / "results.txt").write_text(text)
    js["verdict"] = verdict
    js["summary"] = summary
    (HERE / "results.json").write_text(json.dumps(js, indent=1) + "\n")
    print("\n".join(verdict))
    print(summary)


if __name__ == "__main__":
    sys.exit(main())
