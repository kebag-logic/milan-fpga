#!/usr/bin/env python3
"""census_generate_cone_probe.py - a status read put on the wire inside an EXISTING generate loop the census's shape does not build.

milan_datapath.sv's `for (genvar gs = 1; gs < N_STREAMS; gs++) begin :
g_aaf_stream_en` builds the AAF stream gate of streams 1..N-1. At the census's
one elaboration (default N_STREAMS = 1) the loop has no iteration. This probe
adds one term, `& ~lwsrp_talker_declared` (the status consumer the census
counts as CSR read-back only, row pp_cd_srp_tk_decl_state_w ->
lwsrp_talker_declared), to that loop's existing gate expression, and as a
control to stream 0's gate outside the loop:

  arm D  control: stream 0's gate (outside the loop), default parameters -> must be refused
  arm E  the loop's gate, default parameters (as CI runs)                 -> census verdict?
  arm F  arm E's copy at the arty 4x4 shape (N_STREAMS = 4)               -> must be refused

Each copy goes through the census's own findings() (an in-memory overlay;
the checkout is not modified).

Usage: census_generate_cone_probe.py <checkout>
"""
import sys
from dataclasses import replace
from pathlib import Path

LOOP = "           (acmp_talker_active_aaf_w[gs] & lwsrp_stream_gate[gs]));"
STREAM0 = "  assign aaf_stream_en_raw_w[0] = aaf_gate;"
SHAPE_4X4 = (("parameter int N_STREAMS = 1,", "parameter int N_STREAMS = 4,"),
             ("parameter int MILAN_CLK_FREQ_HZ = 100_000_000,", "parameter int MILAN_CLK_FREQ_HZ = 50_000_000,"),
             ("parameter int TALKER_WIRE_CHANS_P = 2,", "parameter int TALKER_WIRE_CHANS_P = 4,"),
             ("parameter int AUDIO_IF_SLOTS_P = 0,", "parameter int AUDIO_IF_SLOTS_P = 8,"),
             ("parameter int AUDIO_IF_MASTER_P = 0,", "parameter int AUDIO_IF_MASTER_P = 1,"),
             ("parameter int AUDIO_IF_I2S_PAIR_P = 0,", "parameter int AUDIO_IF_I2S_PAIR_P = 1,"))


def edit(text: str, *pairs) -> str:
    for old, new in pairs:
        assert text.count(old) == 1, old
        text = text.replace(old, new, 1)
    return text


def main() -> int:
    repo = Path(sys.argv[1]).resolve()
    sys.path.insert(0, str(repo / "sw/mailbox"))
    import census_elab as ce
    import publication_census as pc
    import mailbox_model

    known = pc.fields(mailbox_model.load())
    src = pc.load(pc.DATAPATH, pc.WRAPPER_SV)
    in_loop = edit(src.datapath, (LOOP, LOOP.replace("lwsrp_stream_gate[gs]));",
                                                     "lwsrp_stream_gate[gs] & ~lwsrp_talker_declared));")))
    outside = edit(src.datapath, (STREAM0, STREAM0.replace("aaf_gate;", "aaf_gate & ~lwsrp_talker_declared;")))
    verdicts = []
    for what, text, shape in (("D control: stream 0's gate, default parameters", outside, False),
                              ("E g_aaf_stream_en's gate, default parameters (as CI runs)", in_loop, False),
                              ("F g_aaf_stream_en's gate at the arty 4x4 shape (N_STREAMS = 4)", in_loop, True)):
        if shape:
            base = ce.recipe()
            rcp = ce.Recipe(base.defines, (repo / "configs/generated/endstation_arty_4x4", *base.incdirs[1:]),
                            base.sources)
            ce.recipe = pc.recipe = (lambda: rcp)
            ce.tracked_openers.cache_clear()
            text = edit(text, *SHAPE_4X4)
        out, sv = pc.findings(replace(src, datapath=text), pc.CENSUS, known)
        hit = [f for f in out if "lwsrp_talker_declared" in f]
        verdicts.append(bool(hit))
        print(f"ARM {what}: {'REFUSED' if hit else 'ACCEPTED'} ({len(out)} finding(s); reads={len(sv.reads)})")
        for f in out:
            print(f"    {f}")
    print(f"SUMMARY control_refused={verdicts[0]} loop_default_refused={verdicts[1]} "
          f"loop_arty4x4_refused={verdicts[2]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
