#!/usr/bin/env python3
"""census_generate_probe.py - a class-D read inside a parameter-dependent generate branch.

The census elaborates milan_datapath once, at its default parameters
(N_STREAMS = 1) and the endstation_arty_current shape header. This probe plants
an unmapped read of a class-D net onto the wire (the CRF talker's vlan_en_i,
the same sink the census's own `routed` plants use) inside a generate branch
that only the N_STREAMS > 1 shapes (arty 4x4, AX7101 8x8) build, and a control
with the same read outside any generate branch. Each planted copy goes through
the census's own findings() as its self-test does (an in-memory overlay; the
checkout is not modified):

  arm A  control, no generate branch, default parameters   -> must be refused
  arm B  N_STREAMS > 1 branch, default parameters (= CI)   -> census verdict?
  arm C  arm B's copy at the arty 4x4 shape (N_STREAMS = 4) -> must be refused

Usage: census_generate_probe.py <checkout>
"""
import sys
from dataclasses import replace
from pathlib import Path

WIRE = "pp_cd_srp_over_limit_w"
CRF_DECL = "  wire crft_class_a_w = (ACMP_SRC_C > N_STREAMS) &"
VLAN_EN = "    .vlan_en_i  (crft_class_a_w),"
NSTREAMS = "  parameter int N_STREAMS = 1,"


def plant(text: str, decl: str) -> str:
    for old, new in ((CRF_DECL, decl + CRF_DECL), (VLAN_EN, "    .vlan_en_i  (crft_class_a_w & ~probe_w),")):
        assert text.count(old) == 1, old
        text = text.replace(old, new, 1)
    return text


def main() -> int:
    repo = Path(sys.argv[1]).resolve()
    sys.path.insert(0, str(repo / "sw/mailbox"))
    import publication_census as pc
    import mailbox_model

    known = pc.fields(mailbox_model.load())
    src = pc.load(pc.DATAPATH, pc.WRAPPER_SV)
    assert src.datapath.count(NSTREAMS) == 1
    control = f"  wire probe_w;\n  assign probe_w = |{WIRE};\n"
    gen = (f"  wire probe_w;\n  if (N_STREAMS > 1) begin : g_probe_shape\n    assign probe_w = |{WIRE};\n"
           f"  end else begin : g_probe_shape_off\n    assign probe_w = 1'b0;\n  end\n")
    arms = (("A control: plain assign, default parameters", plant(src.datapath, control)),
            ("B generate branch on N_STREAMS > 1, default parameters (as CI runs)", plant(src.datapath, gen)),
            ("C the same copy with N_STREAMS defaulted to 8",
             plant(src.datapath, gen).replace(NSTREAMS, "  parameter int N_STREAMS = 8,")))
    verdicts = []
    for what, text in arms:
        if what.startswith("C"):
            # the arty 4x4 shape: its generated header leads the include path,
            # and the builder's parameters for it (census_shape_probe.py's run)
            import census_elab as ce
            base = ce.recipe()
            rcp = ce.Recipe(base.defines, (repo / "configs/generated/endstation_arty_4x4", *base.incdirs[1:]),
                            base.sources)
            ce.recipe = pc.recipe = (lambda: rcp)
            ce.tracked_openers.cache_clear()
            for old, new in (("parameter int N_STREAMS = 8,", "parameter int N_STREAMS = 4,"),
                             ("parameter int MILAN_CLK_FREQ_HZ = 100_000_000,",
                              "parameter int MILAN_CLK_FREQ_HZ = 50_000_000,"),
                             ("parameter int TALKER_WIRE_CHANS_P = 2,", "parameter int TALKER_WIRE_CHANS_P = 4,"),
                             ("parameter int AUDIO_IF_SLOTS_P = 0,", "parameter int AUDIO_IF_SLOTS_P = 8,"),
                             ("parameter int AUDIO_IF_MASTER_P = 0,", "parameter int AUDIO_IF_MASTER_P = 1,"),
                             ("parameter int AUDIO_IF_I2S_PAIR_P = 0,", "parameter int AUDIO_IF_I2S_PAIR_P = 1,")):
                assert text.count(old) == 1, old
                text = text.replace(old, new, 1)
            what = "C the same copy at the arty 4x4 shape (N_STREAMS = 4, its header and builder parameters)"
        out, sv = pc.findings(replace(src, datapath=text), pc.CENSUS, known)
        hit = [f for f in out if WIRE in f]
        verdicts.append(bool(hit))
        print(f"ARM {what}: {'REFUSED' if hit else 'ACCEPTED'} ({len(out)} finding(s); reads={len(sv.reads)})")
        for f in out:
            print(f"    {f}")
    print(f"SUMMARY control_refused={verdicts[0]} generate_default_refused={verdicts[1]} "
          f"generate_arty4x4_refused={verdicts[2]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
