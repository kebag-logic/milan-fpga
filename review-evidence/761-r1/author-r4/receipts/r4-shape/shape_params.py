#!/usr/bin/env python3
"""Compare the dynmap leg's elaborated datapath parameters with the shipping AX7101 shape.

Usage: shape_params.py <repo-root> <leg-run-log>

The leg prints its elaborated parameters as `[i] elaborated...` lines (read back
from the model through dynmap_probes.vlt). The shipping values are derived from
the entity definition's generated design argv, configs/generated/sweep_opts_ax7101.sh
(OPTS, generated from configs/endstation_ax7101_1x1_tdm8.yaml), mapped onto
milan_datapath parameters the way sw/litex/milan_soc.py add_milan_datapath does,
and from the config's generated gen/adp_shape_defaults.svh. Prints one row per
parameter: name, elaborated, shipping, verdict. Exit 0 always; the table is the
receipt.
"""
import re
import shlex
import sys
from pathlib import Path


def opts(root: Path) -> dict:
    text = (root / "configs/generated/sweep_opts_ax7101.sh").read_text()
    argv = shlex.split(re.search(r'^OPTS="([^"]*)"', text, re.M).group(1))
    out, i = {}, 0
    while i < len(argv):
        a = argv[i]
        if i + 1 < len(argv) and not argv[i + 1].startswith("--"):
            out[a] = argv[i + 1]
            i += 2
        else:
            out[a] = True
            i += 1
    return out


def svh(root: Path) -> dict:
    text = (root / "configs/generated/endstation_ax7101_1x1_tdm8/gen/adp_shape_defaults.svh").read_text()
    return {m.group(1): int(m.group(2))
            for m in re.finditer(r"localparam int (ADP_\w+_C)\s*=\s*(\d+);", text)}


def shipping(root: Path) -> dict:
    o = opts(root)
    g = svh(root)
    slots = {"i2s_philips": 0, "tdm8": 8, "tdm16": 16, "tdm32": 32}[o.get("--audio-interface", "i2s_philips")]
    master = int(bool(o.get("--audio-interface-master")) and slots > 0)
    fs = int(o.get("--audio-fs-hz", 48000))
    bits = int(o.get("--audio-word-bits", 32))
    n = int(o.get("--num-streams", 1))
    return {
        "N_STREAMS": n,
        "ADP_TALKER_SRC_C": g["ADP_TALKER_SRC_C"],
        "ADP_LISTENER_SINK_C": g["ADP_LISTENER_SINK_C"],
        "CRF_SNK_IDX_C": n if g["ADP_LISTENER_SINK_C"] > n else 0,
        "MILAN_CLK_FREQ_HZ": int(float(o["--milan-clk-freq"])),
        "GPTP_PLANE_EN_P": int(bool(o.get("--fabric-gptp"))),
        "TALKER_WIRE_CHANS_P": int(o.get("--talker-wire-chans", 2)),
        "AUDIO_IF_SLOTS_P": slots,
        "AUDIO_IF_MASTER_P": master,
        # with the TDM header on pins (the config's J11 bus); 0 without a master
        "AUDIO_IF_RENDER_SLOTS_P": int(o.get("--audio-interface-render", 0)) if master else 0,
        # the blend needs I2S pads too, and the config routes none
        "AUDIO_IF_I2S_PAIR_P": 0,
        "AUDIO_IF_WORD_BITS_P": bits,
        "AUDIO_IF_FS_HZ_P": fs,
        "AUDIO_IF_CLK_HZ_P": 2 * slots * bits * fs if master else 24576000,
        "LOOPBACK_P": int(bool(o.get("--loopback-lane"))),
        "MCSERVO_P": int(not o.get("--no-media-clock-servo")),
        "LTAP_P": int(not o.get("--no-latency-taps")),
        "MAAP_P": int(not o.get("--no-maap")),
        "I2SPB_P": int(not o.get("--no-i2s-playback")),
        "RXFILT_P": int(not o.get("--no-rx-mac-filter")),
        "LPF_P": int(not o.get("--no-render-lpf")),
        "DPROBES_P": int(not o.get("--no-datapath-probes")),
    }


# The verification substitutes every obj_ax1x1-geometry leg shares, and where
# the suite covers what each one leaves out.
SUBSTITUTE = {
    "MILAN_CLK_FREQ_HZ": "verification fabric clock: the obj_ax1x1-geometry legs (ax1x1, aclk, dynmap) keep the 100 MHz default, which the [762-DP] 1 ms step assumes",
    "GPTP_PLANE_EN_P": "direct option OFF (Makefile GPTP_OFF_VFLAGS); the fabric gPTP plane is obj_gptp / obj_ax1x1gptp",
    "AUDIO_IF_RENDER_SLOTS_P": "render lane pruned in the obj_ax1x1 argv; the shipping TDM8 render lane is tb/verilator/milan_dp_render",
}


def main() -> int:
    root, log = Path(sys.argv[1]), Path(sys.argv[2])
    got = {}
    for line in log.read_text().splitlines():
        if "[i]    elaborated" in line:
            for k, v in re.findall(r"([A-Z][A-Z0-9_]+) (\d+)", line):
                got[k] = int(v)
    want = shipping(root)
    print("| Parameter | Elaborated (leg) | Shipping (entity definition) | Verdict |")
    print("|---|---:|---:|---|")
    same = differ = 0
    for k, w in want.items():
        g = got.get(k)
        if g == w:
            verdict, same = "same", same + 1
        else:
            verdict, differ = "DIFFERS: " + SUBSTITUTE.get(k, "UNEXPLAINED"), differ + 1
        print(f"| `{k}` | {g} | {w} | {verdict} |")
    print(f"\n{same} same, {differ} differ "
          f"({sum(1 for k in want if got.get(k) != want[k] and k not in SUBSTITUTE)} unexplained)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
