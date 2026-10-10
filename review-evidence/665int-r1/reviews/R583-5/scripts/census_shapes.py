#!/usr/bin/env python3
"""Reviewer probe (R583-5): run the publication census of PR #704, unmodified,
over milan_datapath elaborated in other shipping shapes' parameters.

usage: census_shapes.py REPO [JOBS]

The census elaborates milan_datapath at its default parameters with the
arty_current header directory. The SoC passes N_STREAMS, the audio front-end,
LOOPBACK_P and the optional-block prunes per shape (sw/litex/milan_soc.py
dp_params; configs/generated/sweep_opts_*.sh), and Yosys prunes a generate
branch whose condition is false. This probe adds `-chparam` to the census's
own `hierarchy -check -top milan_datapath` and swaps the generated header
directory; nothing else of the census changes. For each shape it prints the
census's findings against its own CENSUS table, and every (wire, consumer)
read that differs from the default shape's.
"""
import re
import sys
from concurrent.futures import ProcessPoolExecutor
import multiprocessing
from pathlib import Path

repo = Path(sys.argv[1]).resolve()
jobs = int(sys.argv[2]) if len(sys.argv) > 2 else 4
sys.path.insert(0, str(repo / "sw/mailbox"))
import census_elab as ce  # noqa: E402
import publication_census as pc  # noqa: E402

ORIG_RECIPE, ORIG_RUN = ce.recipe, ce.run   # each shape patches from these, never from a previous shape

GEN = repo / "configs/generated"
SHAPES = {
    "default (arty_current, the census's own)": ("endstation_arty_current", {}),
    "arty_4x4 (sweep_opts_arty.sh)": ("endstation_arty_4x4", dict(
        N_STREAMS=4, AUDIO_IF_SLOTS_P=8, AUDIO_IF_MASTER_P=1, TALKER_WIRE_CHANS_P=4)),
    "ax7101_1x1_tdm8 (sweep_opts_ax7101.sh)": ("endstation_ax7101_1x1_tdm8", dict(
        N_STREAMS=1, AUDIO_IF_SLOTS_P=8, AUDIO_IF_MASTER_P=1, AUDIO_IF_RENDER_SLOTS_P=8, TALKER_WIRE_CHANS_P=8,
        LOOPBACK_P=1, I2SPB_P=0, LPF_P=0, GPTP_INGRESS_LAT_NS_P=656, GPTP_EGRESS_LAT_NS_P=219)),
    "8 streams, loopback lane (ax7101_8x8 header)": ("endstation_ax7101_8x8", dict(
        N_STREAMS=8, AUDIO_IF_SLOTS_P=8, AUDIO_IF_MASTER_P=1, TALKER_WIRE_CHANS_P=8, LOOPBACK_P=1)),
    "2 streams (arty_current header)": ("endstation_arty_current", dict(N_STREAMS=2)),
    "every optional block pruned, gPTP plane off": ("endstation_arty_current", dict(
        GPTP_PLANE_EN_P=0, MCSERVO_P=0, LTAP_P=0, MAAP_P=0, I2SPB_P=0, RXFILT_P=0, LPF_P=0, DPROBES_P=0)),
}


def shaped(gen: str, params: dict):
    base = ORIG_RECIPE()
    incdirs = tuple(GEN / gen if Path(d).resolve() == (GEN / "endstation_arty_current").resolve() else d
                    for d in base.incdirs)
    rcp = ce.Recipe(base.defines, incdirs, base.sources)
    ce.recipe = lambda: rcp
    pc.recipe = lambda: rcp
    chp = " ".join(f"-chparam {k} {v}" for k, v in params.items())
    orig = ORIG_RUN

    def run(argv, cwd, what):
        if chp:
            # a deferred read, so the datapath is elaborated only with the shape's parameters (a plain read
            # elaborates the defaults first, and the datapath's shape guard refuses those with this header);
            # the derived top renamed back to the name the census reads
            argv = [re.sub(r"read_verilog (\S+/top\.v)", r"read_verilog -defer \1", a).replace(
                f"hierarchy -check -top {ce.TOP}", f"hierarchy -check -top {ce.TOP} {chp}; rename -top {ce.TOP}")
                for a in argv]
        return orig(argv, cwd, what)
    ce.run = run


def one(name: str):
    gen, params = SHAPES[name]
    shaped(gen, params)
    try:
        src = pc.load(pc.DATAPATH, pc.WRAPPER_SV)
        out, sv = pc.findings(src, pc.CENSUS, pc.fields(pc.mailbox_model.load()))
    except ce.CensusError as exc:
        return name, None, [f"census cannot read it: {exc}"]
    reads = {(r.wire, r.consumer): ",".join(sorted({k for k, _ in r.ends})) for r in sv.reads}
    return name, reads, out + [f"(info) netlist: {sv.size}"]


if __name__ == "__main__":
    ce.recipe()
    with ProcessPoolExecutor(max_workers=jobs, mp_context=multiprocessing.get_context("fork")) as pool:
        res = list(pool.map(one, SHAPES))
    base = res[0][1] or {}
    res = [(n, r, o) for n, r, o in res]
    bad = 0
    for name, reads, out in res:
        print(f"== shape: {name}  params={SHAPES[name][1]}")
        if reads is None:
            print("   " + out[0][:400])
            continue
        info = [f for f in out if f.startswith("(info)")]
        out = [f for f in out if not f.startswith("(info)")]
        print(f"   reads: {len(reads)}; census findings: {len(out)}; {info[0][7:]}")
        for f in out:
            print(f"   [FINDING] {f}")
        for k in sorted(set(reads) | set(base)):
            if reads.get(k) != base.get(k):
                print(f"   [DIFF vs default] {k[0]} -> {k[1]}: default={base.get(k)} here={reads.get(k)}")
        bad += bool(out)
    print(f"census_shapes: {bad} shape(s) with census findings")
