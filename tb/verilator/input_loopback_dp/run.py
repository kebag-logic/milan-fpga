#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Generate an enabled product shape and execute its parent integration test."""
import argparse
import json
import os
from pathlib import Path
import shlex
import subprocess
import sys
import yaml

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / "tb/verilator/milan_dp_render"))
from ship8_params import derive, header, listener_format


def main() -> None:
    """Generate the selected enabled shape, build the parent test and run it."""
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--shape", type=int, choices=(1, 8), required=True)
    p.add_argument("--work", type=Path, required=True)
    p.add_argument("--dp-source", type=Path)
    p.add_argument("--queue-source", type=Path)
    p.add_argument("--build-only", action="store_true")
    a = p.parse_args()
    w = a.work.resolve()
    w.mkdir(parents=True, exist_ok=True)
    name = "endstation_ax7101_1x1_tdm8" if a.shape == 1 else "endstation_ax7101_8x8"
    raw = yaml.safe_load((ROOT / "configs" / (name + ".yaml")).read_text())
    raw["audio_interface"]["cluster_mapping"]["fabric"].update(input_loopback_lane=True, loopback_lane=False)
    cfg = w / (name + ".yaml")
    cfg.write_text(yaml.safe_dump(raw))
    def run(cmd: list, cwd: Path = ROOT) -> None:
        """Echo and execute one command, failing on a nonzero exit."""
        print(shlex.join(list(map(str, cmd))), flush=True)
        subprocess.run(list(map(str, cmd)), cwd=cwd, check=True, timeout=7200)
    run([sys.executable, ROOT / "sw/builder/endstation_builder.py", cfg, "-o", w / "gen"])
    gen = w / "gen" / name
    overlay = json.loads((gen / "aem_overlay.json").read_text())
    params = derive(json.loads((gen / "soc_params.json").read_text())["argv"])
    params["INPUT_LOOPBACK_P"] = 1
    params["CTRL_SPLIT_P"] = 1
    geometry = header(params, listener_format(overlay))
    ports = overlay["stream_ports"]["input"]
    for key, field in (("kInputBase", "base_cluster"), ("kInputWidth", "clusters")):
        geometry += "constexpr int " + key + "[] = {" + ",".join(str(x[field]) for x in ports) + "};\n"
    (w / "geometry.hpp").write_text(geometry)
    run([sys.executable, ROOT / "avdecc/gen_aemi_image.py", "--overlay", gen / "aem_overlay.json",
         "--line-bytes", "576", "-o", w / "aemi.bin"])
    ctrl = ROOT / "sw/firmware/ctrl"
    run([sys.executable, ctrl / "aecp/aecp_entity.py", cfg, "-o", w / "aecp_entity_gen.h"])
    includes = ["-I" + str(d) for d in (w, ctrl / "aecp", ctrl / "loop", ctrl / "mbx",
                ROOT / "third_party/tsn-c-stack/include")]
    units = ["aecp.c", "aecp_commands.c", "aecp_maps.c", "aecp_image.c", "aecp_state.c"]
    objects = []
    for unit in units:
        obj = w / (unit + ".o")
        run(["cc", "-std=c11", "-O2", *includes, "-c", ctrl / "aecp" / unit, "-o", obj])
        objects.append(obj)
    run(["ar", "rcs", w / "libaecp.a", *objects])
    def make_words(target: str) -> list[str]:
        """Return the milan_dp Makefile's words for one print target."""
        cmd = ["make", "-s", "--no-print-directory", "-C", str(ROOT / "tb/verilator/milan_dp"),
               target, "VERILATOR_JOBS=" + os.environ.get("VERILATOR_JOBS", "4")]
        if a.dp_source:
            cmd.append("DP_SRC=" + str(a.dp_source.resolve()))
        if a.queue_source:
            cmd.append("RQ_SRC=" + str(a.queue_source.resolve()))
        return shlex.split(subprocess.check_output(cmd, text=True))
    cmd = [os.environ.get("VERILATOR", "verilator"), "+incdir+" + str(gen), *make_words("print-dp-vflags"),
           "--Mdir", str(w / "obj"), "-CFLAGS", " ".join(includes), "-LDFLAGS", str(w / "libaecp.a"),
           str(HERE / "probes.vlt")]
    cmd += ["-G" + k + "=" + str(v) for k, v in params.items()]
    cmd += make_words("print-srcs") + [str(HERE / "sim_main.cpp"), "-o", "parent_loopback"]
    (w / "build-command.json").write_text(json.dumps(cmd, indent=2) + "\n")
    run(cmd, HERE)
    if not a.build_only:
        run([w / "obj/parent_loopback"], w)


if __name__ == "__main__":
    main()
