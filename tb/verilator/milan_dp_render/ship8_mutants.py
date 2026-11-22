#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Planted faults for the 8x8/1if render leg (#584): prove sim_ship8_render can fail.

sim_ship8_render.cpp grades, at the generated 8x8 shape and the shipping render parameters, that STREAM_PORT_INPUT
0's one cluster reaches slot 0 of the TDM32 bus and nothing reaches slots 1-31, that ports 1-7 reach no render key
and no pin, that a REMOVE silences the slot, and that a bind fall and a reset leave no stale sample. This runner
plants one defect at a time at the three boundaries that path crosses between the map store and the pins:

  * the PROJECTION, in a copy of the generated shape header: input key 0 projected onto render key 3, past the
    one-slot lane; and port 1's unrouted cluster projected onto render key 2, the lane's key;
  * the ADAPTER, in a copy of milan_datapath.sv: the burst walk's first write takes the key after the lane base;
  * the BUS BINDING, in the same copy: the serializer framed as an eight-slot bus inside the capture master's
    32-slot frame (its frame position narrowed to match, so it elaborates). The direct mis-tie, BUS_SLOTS_P bound
    to the render width, is a separate arm: KL_tdm_render_master's frame-position guard must refuse it at
    elaboration, by its words.

Each planted copy is elaborated through the suite's own recipe (`make ship8-build` with SHIP8_SHAPE or DP_SRC and
SHIP8_MDIR overridden) and must FAIL by the leg's own verdict, every named check among the failures; a crash or an
abort is not a catch. The unplanted leg runs first and must pass. The tracked sources are never edited. Every mode
of the leg is cycle bounded, so a run ends whatever the planted gateware does.

    python3 tb/verilator/milan_dp_render/ship8_mutants.py [--jobs N]
    or: make -C tb/verilator/milan_dp_render ship8-mutants
Exit 0 = the clean leg passed and every plant was caught.
"""

import argparse
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent
DP_RTL = HERE / "../../../hdl/milan/milan_datapath.sv"
SHAPE_SVH = HERE / "../../../configs/generated/endstation_ax7101_8x8/gen/adp_shape_defaults.svh"
sys.path.insert(0, str(HERE / "../../../scripts"))
from suite_tally import log_reports_failure  # noqa: E402

#: the source a plant edits, and the recipe variable that selects its copy
SOURCES = {"shape": (SHAPE_SVH, "SHIP8_SHAPE"), "dp": (DP_RTL, "DP_SRC")}
RPHYS = "'{7'h42, 7'h00, 7'h00,"
ADAPTER_FIRST = "            tdmr_data_r  <= chmap_phys_w[CHMAP_RPHYS_TDM_BASE_C*24 +: 24];\n"
BUS_BINDING = ("        .BUS_SLOTS_P   (AUDIO_IF_SLOTS_P),\n"
               "        .SLOT_BITS_P   (AIF_WORD_BITS_C),\n"
               "        .FIFO_LOG2_P   (2),\n"
               "        .FRAME_POS_W_P (AIF_FPOS_W_C)\n"
               "      ) chan_tdm_render (\n")
#: (name, source, [(pattern, replacement)], the checks that must fail) - the
#: check names are sim_ship8_render.cpp's own words
PLANTS = [
    ("projection: input key 0 onto render key 3, past the one-slot lane", "shape",
     [(RPHYS, "'{7'h43, 7'h00, 7'h00,")],
     ("P1 POWER-ON: render keys 0-9 hold port 0's mapping on key 2 and nothing else",
      "P3 POWER-ON RENDER: slot 0 carries stream 0 channel 0 in every frame")),
    ("projection: unrouted port 1's cluster onto render key 2, the lane's key", "shape",
     [(RPHYS, "'{7'h42, 7'h42, 7'h00,")],
     ("U3: render keys 0-9 hold port 0's mapping on key 2 and nothing else",
      "U4 RENDER: slot 0 carries stream 3 channel 2 in every frame")),
    ("adapter: the walk's first write takes the key after the lane base", "dp",
     [(ADAPTER_FIRST,
       "            tdmr_data_r  <= chmap_phys_w[(CHMAP_RPHYS_TDM_BASE_C+1)*24 +: 24];\n")],
     ("P3 POWER-ON RENDER: slot 0 carries stream 0 channel 0 in every frame",
      "R1 RENDER: slot 0 carries stream 0 channel 5 in every frame")),
    ("bus binding: the serializer framed as eight slots inside the 32-slot bus frame", "dp",
     [(BUS_BINDING, BUS_BINDING.replace("(AUDIO_IF_SLOTS_P),", "(AUDIO_IF_SLOTS_P / 4),")
                               .replace("(AIF_FPOS_W_C)", "(AIF_FPOS_W_C - 2)"))],
     ("P3 POWER-ON RENDER: slots 1-31 carry zero in every frame",
      "R1 RENDER: slots 1-31 carry zero in every frame")),
]
#: (name, source, edits, the words the elaboration must refuse it with)
REFUSALS = [
    ("bus binding: BUS_SLOTS_P bound to the render width", "dp",
     [(BUS_BINDING, BUS_BINDING.replace("(AUDIO_IF_SLOTS_P),", "(AUDIO_IF_RENDER_SLOTS_P),"))],
     "does not match $clog2(BUS_SLOTS_P*SLOT_BITS_P)"),
]


def plant(source: str, edits: list[tuple[str, str]], work: Path, tag: str) -> tuple[str | None, str]:
    """Write the planted copy and return the recipe value that selects it, or None and why."""
    path, _ = SOURCES[source]
    text = path.read_text()
    for pattern, replacement in edits:
        if text.count(pattern) != 1:
            return None, (f"its pattern appears {text.count(pattern)} time(s) in {path.name}, expected exactly 1: "
                          "the source moved, so fix the pattern rather than drop the plant")
        text = text.replace(pattern, replacement)
    if source == "shape":
        gen = work / f"shape_{tag}" / "gen"
        gen.mkdir(parents=True)
        (gen / "adp_shape_defaults.svh").write_text(text)
        return f"+incdir+{gen.parent}", ""
    out = work / f"{path.stem}_{tag}.sv"
    out.write_text(text)
    return str(out), ""


def build(overrides: dict[str, str], mdir: Path) -> tuple[Path | None, str]:
    """Elaborate through the suite's own recipe; the executable, or None and the build's output."""
    cmd = ["make", "--no-print-directory", "-s", "-C", str(HERE), "ship8-build", f"SHIP8_MDIR={mdir}"]
    cmd += [f"{k}={v}" for k, v in overrides.items()]
    out = subprocess.run(cmd, capture_output=True, text=True, check=False)
    exe = mdir / "Vmilan_dp_ship8"
    if out.returncode != 0 or not exe.is_file():
        return None, out.stdout + out.stderr
    return exe, ""


def verdict(exe: Path, must_fail: tuple[str, ...]) -> str:
    """'pass', 'caught', or why the run is not evidence; caught only when every named check failed."""
    proc = subprocess.run([str(exe)], cwd=str(HERE), capture_output=True, text=True, check=False)
    out = proc.stdout + proc.stderr
    reason, failed = log_reports_failure(out)
    if proc.returncode == 0 and not failed:
        return "pass"
    if proc.returncode == 0:
        return f"exited 0 but {reason}: a masked verdict is not evidence"
    if not failed:
        return f"exited {proc.returncode} with no harness verdict: a crash or a DUT abort is not a catch"
    fails = [line for line in out.splitlines() if line.strip().startswith("[FAIL]")]
    missing = [n for n in must_fail if not any(n in line for line in fails)]
    return f"failed, but not the named check {missing[0]!r}" if missing else "caught"


def tag_of(name: str) -> str:
    """A directory-safe tag for a plant's name."""
    return "".join(c if c.isalnum() else "_" for c in name)[:48]


def run_plant(work: Path, name: str, source: str, edits: list[tuple[str, str]], breaks: tuple[str, ...]) -> str:
    """One plant, start to verdict: the line this runner prints for it."""
    tag = tag_of(name)
    value, why = plant(source, edits, work, tag)
    if value is None:
        return f"[FAIL] plant {name!r}: {why}"
    exe, log = build({SOURCES[source][1]: value}, work / f"obj_{tag}")
    if exe is None:
        return f"[FAIL] plant {name!r} did not build; a plant that cannot build proves nothing\n{log[-1500:]}"
    answer = verdict(exe, breaks)
    if answer == "caught":
        return f"[PASS] plant caught: {name} - breaks \"{breaks[0]}\" and {len(breaks) - 1} more"
    if answer == "pass":
        return f"[FAIL] plant SURVIVED: {name}. The leg does not prove \"{breaks[0]}\"."
    return f"[FAIL] plant {name!r} {answer}"


def run_refusal(work: Path, name: str, source: str, edits: list[tuple[str, str]], words: str) -> str:
    """One plant the elaboration must refuse, by its words."""
    tag = tag_of(name)
    value, why = plant(source, edits, work, tag)
    if value is None:
        return f"[FAIL] refusal {name!r}: {why}"
    exe, log = build({SOURCES[source][1]: value}, work / f"obj_{tag}")
    if exe is not None:
        return f"[FAIL] refusal {name!r}: the planted copy elaborated"
    if words not in log:
        return f"[FAIL] refusal {name!r}: the build failed, but not with \"{words}\"\n{log[-1500:]}"
    return f"[PASS] refused at elaboration: {name} - \"{words}\""


def main() -> int:
    """The clean control, then every plant and refusal; 1 if any survived."""
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--jobs", type=int, choices=range(1, 9), default=4)
    args = parser.parse_args()
    clean = HERE / "obj_ship8" / "Vmilan_dp_ship8"
    if not clean.is_file():
        print("[FAIL] the clean leg is not built (make ship8-build)")
        return 1
    lines = []
    control = verdict(clean, ())
    lines.append("[PASS] the unplanted leg passes" if control == "pass"
                 else f"[FAIL] the unplanted leg does not pass ({control}): no plant below is evidence")
    with tempfile.TemporaryDirectory(prefix="ship8-mutants-") as td:
        work = Path(td)
        with ThreadPoolExecutor(max_workers=args.jobs) as pool:
            jobs = [pool.submit(run_plant, work, *p) for p in PLANTS]
            jobs += [pool.submit(run_refusal, work, *r) for r in REFUSALS]
            lines += [j.result() for j in jobs]
    print("\n".join(lines))
    passes = sum(line.startswith("[PASS]") for line in lines)
    print(f"\n{len(lines)} checks: {passes} PASS, {len(lines) - passes} FAIL")
    return 0 if passes == len(lines) else 1


if __name__ == "__main__":
    sys.exit(main())
