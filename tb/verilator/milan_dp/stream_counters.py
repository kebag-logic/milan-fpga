#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Run #726 packet, reset and notification checks through the parent MAC.

Build inputs come from this suite's source and flag exports. All generated
files, planted RTL copies and logs stay below --work. A mutant must fail its
named check group and then pass with exactly that group omitted. Neither a
build failure nor a crash counts as detection. No submodule file is edited.
"""

import argparse
import os
from pathlib import Path
import shlex
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
TX = "hdl/ieee1722/avtp/KL_talker_diag_ctx.sv"
RX = "hdl/ieee1722/crf/KL_crf_rx.sv"
AAF = "hdl/ieee1722/avtp/KL_avtp_rx_monitor_ctx.sv"
DP = "hdl/milan/milan_datapath.sv"
GROUPS = {"tx-interval": "TX", "rx-interval": "RX", "tx-reset": "TX_RESET",
          "aaf-reset": "RX_RESET", "crf-reset": "RX_RESET",
          "rx-saturation": "RX", "late": "CADENCE", "rate": "RATE",
          "tx-nodirty": "OUTPUT_CADENCE"}


def replace_once(text, old, new):
    if text.count(old) != 1:
        raise ValueError(f"plant anchor occurred {text.count(old)} times: {old!r}")
    return text.replace(old, new)


def plant(variant, work, output_condition):
    files = {rel: (ROOT / rel).read_text() for rel in (TX, RX, AAF, DP)}
    if variant == "before":
        for rel in files:
            files[rel] = subprocess.check_output(
                ["git", "show", f"c6bd08c6:{rel}"], cwd=ROOT, text=True)
    elif variant == "tx-interval":
        files[TX] = replace_once(files[TX], "  always_ff @(posedge clk_i) begin : diag_track", """
  logic [N_CTX_P-1:0] counted_r;
  always_ff @(posedge clk_i) begin
    if (!rst_n) counted_r <= '0;
    else for (int c=0; c<N_CTX_P; c++) begin
      if (tick_p_r || (streaming_i[c] && !strm_q_r[c])) counted_r[c] <= ev_f_w[c];
      else if (ev_f_w[c]) counted_r[c] <= 1'b1;
    end
  end
  always_ff @(posedge clk_i) begin : diag_track""")
        files[TX] = replace_once(files[TX], "ftx_r[c] <= ftx_r[c] + 32'd1;",
                                "ftx_r[c] <= ftx_r[c] + 32'(!counted_r[c] || tick_p_r);")
    elif variant == "rx-interval":
        files[RX] = replace_once(files[RX], "  always_ff @(posedge clk_i) begin : engine", """
  logic counted_r;
  always_ff @(posedge clk_i) begin
    if (!rst_n || w_bind_rise_w) counted_r <= 1'b0;
    else if (iv_tick_r) counted_r <= w_acc;
    else if (w_acc) counted_r <= 1'b1;
  end
  always_ff @(posedge clk_i) begin : engine""")
        files[RX] = replace_once(files[RX], "pdu_count_o <= pdu_count_o + 32'd1;",
                                "pdu_count_o <= pdu_count_o + 32'(!counted_r || iv_tick_r);")
    elif variant == "tx-nodirty":
        files[TX] = replace_once(files[TX],
                                "ftx_r[c] <= ftx_r[c] + 32'd1;\n          dirty_p_o[c] <= 1'b1;",
                                "ftx_r[c] <= ftx_r[c] + 32'd1;")
    elif variant == "tx-reset":
        files[TX] = replace_once(files[TX], "ftx_r[c]    <= {31'd0, ev_f_w[c]};",
                                "ftx_r[c]    <= ftx_r[c];")
    elif variant == "aaf-reset":
        files[AAF] = replace_once(files[AAF], "else if (bind_zero_r) begin\n          eng_we_w    = 1'b1;",
                                 "else if (bind_zero_r) begin\n          eng_we_w    = (zero_idx_r != C_FRX_C);")
    elif variant == "crf-reset":
        files[RX] = replace_once(files[RX], "        pdu_count_o    <= '0;",
                                "        pdu_count_o    <= pdu_count_o;")
    elif variant == "rx-saturation":
        files[AAF] = replace_once(files[AAF], "if (iv_set_w[s][C_FRX_C])",
                                 "if (iv_set_w[s][C_FRX_C] && frx_acc_r[s] < 32'd65535)")
    elif variant == "late":
        files[DP] = replace_once(files[DP],
                                "assign pp_ctr_sin_dirty_w = {crf_dirty_p_w, avtprx_dirty_p_w};",
                                "assign pp_ctr_sin_dirty_w = {crf_dirty_p_w, avtprx_dirty_p_w}"
                                " & {PP_CTR_SIN_N_C{s_axi_awvalid && s_axi_awaddr == 12'hFFC}};")
    elif variant == "rate":
        files[DP] = replace_once(files[DP], ".TIM_DIV_MS_P   (PP_TIM_DIV_MS_P),",
                                ".TIM_DIV_MS_P   (PP_TIM_DIV_MS_P / 2),")
    if output_condition == "frames-only":
        # Model the locked-PHC condition at both talker inputs. The real
        # packetizers stamp tu=0 and their completed-frame bits feed diagnostics.
        anchor = ".ts_uncertain_i (clkv_tu_w)"
        if files[DP].count(anchor) != 2:
            raise ValueError("expected AAF and CRF timestamp-uncertainty inputs")
        files[DP] = files[DP].replace(anchor, ".ts_uncertain_i (1'b0)")
    paths = {}
    for rel, text in files.items():
        dest = work / Path(rel).name
        if not dest.exists() or dest.read_text() != text:
            dest.write_text(text)
        paths[str(ROOT / rel)] = str(dest)
    return paths


def run(shape, variant, work, verilator, output_condition):
    work.mkdir(parents=True, exist_ok=True)
    # Preserve the fixture's repository-relative descriptor paths without
    # writing ROM images or object files into the checkout.
    for name in ("configs", "sw", "hdl", "scripts", "avdecc", "protocol-processor"):
        path = work / name
        if not path.exists():
            path.symlink_to(ROOT / name, target_is_directory=True)
    runtime = work / "tb/verilator/milan_dp"
    runtime.mkdir(parents=True, exist_ok=True)
    flags = shlex.split(subprocess.check_output(
        ["make", "-s", "print-dp-vflags"], cwd=HERE, text=True))
    flags = [f.replace("../../../", str(ROOT) + "/") for f in flags
             if not f.startswith(("-GDIAG_TICK", "-GLDIAG_IVAL"))]
    flags[flags.index("-j") + 1] = "2"
    config = "endstation_ax7101_1x1_tdm8" if shape == 1 else "endstation_ax7101_8x8"
    flags.insert(0, "+incdir+" + str(ROOT / "configs/generated" / config))
    flags += ["-GDIAG_TICK_CYC_P=1000000", "-GLDIAG_IVAL_CYC_P=1000000",
              "-GMILAN_CLK_FREQ_HZ=50000000", "-GPP_TIM_DIV_US_P=1",
              "-GPP_TIM_DIV_MS_P=1000", f"-GN_STREAMS={shape}",
              "-GTALKER_WIRE_CHANS_P=8", "-GAUDIO_IF_MASTER_P=1",
              f"-GAUDIO_IF_SLOTS_P={8 if shape == 1 else 32}",
              f"-GAUDIO_IF_CLK_HZ_P={24576000 if shape == 1 else 98304000}",
              "-GI2SPB_P=0", "-GLPF_P=0", "-CFLAGS",
              f"-DNSTREAMS_TB={shape} -DMS_CYC_TB=1000 -DSTREAM_COUNTERS_TB=1 "
              f"-DCOUNTERS_FRAMES_ONLY_TB={int(output_condition == 'frames-only')}",
              "--Mdir", str(work / "obj")]
    sources = shlex.split(subprocess.check_output(
        ["make", "-s", "print-srcs"], cwd=HERE, text=True))
    sources = [str((HERE / s).resolve()) for s in sources]
    replacements = plant(variant, work, output_condition)
    sources = [replacements.get(s, s) for s in sources]
    with (work / "build.log").open("w") as log:
        subprocess.run([verilator, *flags, *sources, str(HERE / "sim_nxn.cpp"),
                        "-o", "stream_counters"], cwd=work, stdout=log,
                       stderr=subprocess.STDOUT, check=True)
    for script, output in (("protocol-processor/hdl/acmp/rom/gen_ltn_rom.py", "ltn_rom.hex"),
                           ("protocol-processor/hdl/aecp/ucode/gen_ucode.py", "ucode.hex")):
        subprocess.run([sys.executable, str(ROOT / script), "-o", output],
                       cwd=runtime, check=True)
    env = dict(os.environ)
    env.pop("COUNTERS_OMIT_CHECK", None)
    exe = work / "obj/stream_counters"
    for omitted in (None, GROUPS[variant]) if variant in GROUPS else (None,):
        name = "escape.log" if omitted else "run.log"
        if omitted:
            env["COUNTERS_OMIT_CHECK"] = omitted
        with (work / name).open("w") as log:
            result = subprocess.run([str(exe)], cwd=runtime, env=env,
                                    stdout=log, stderr=subprocess.STDOUT, check=False)
        text = (work / name).read_text()
        failures = [line for line in text.splitlines() if "[FAIL]" in line]
        if variant in GROUPS and omitted is None:
            marker = "[726 " + GROUPS[variant] + "]"
            if result.returncode != 1 or not failures or any(marker not in f for f in failures):
                raise RuntimeError(f"{variant}: no attributable named detection: {failures}")
        elif variant == "before":
            expected = {"TX", "RX", "CADENCE"}
            found = {group for group in expected
                     if any("[726 " + group + "]" in f for f in failures)}
            if (result.returncode != 1 or found != expected or
                    any(not any("[726 " + group + "]" in f for group in expected)
                        for f in failures)):
                raise RuntimeError(f"baseline lacks named TX/RX/CADENCE defects: {failures}")
        elif result.returncode != 0 or failures or "RESULT: PASS" not in text:
            raise RuntimeError(f"{variant}/{name}: rc={result.returncode}, {failures}")
        print(f"{shape}x{shape} {variant} {output_condition} {name}: rc={result.returncode}, failures={len(failures)}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--work", type=Path)
    parser.add_argument("--shape", type=int, choices=(1, 8), default=1)
    parser.add_argument("--variant", choices=("clean", "before", *GROUPS), default="clean")
    parser.add_argument("--output-condition", choices=("uncertain", "frames-only"),
                        help="default: frames-only for tx-nodirty, uncertain otherwise")
    args = parser.parse_args()
    condition = args.output_condition or ("frames-only" if args.variant == "tx-nodirty" else "uncertain")
    if args.variant == "tx-nodirty" and condition != "frames-only":
        parser.error("tx-nodirty requires the frames-only output condition")
    verilator = os.environ.get("VERILATOR", "verilator")
    if args.work:
        run(args.shape, args.variant, args.work.resolve(), verilator, condition)
    else:
        with tempfile.TemporaryDirectory(prefix="stream-counters-") as work:
            run(args.shape, args.variant, Path(work), verilator, condition)


if __name__ == "__main__":
    main()
