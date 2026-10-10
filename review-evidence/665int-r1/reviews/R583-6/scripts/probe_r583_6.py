#!/usr/bin/env python3
"""R583-6 independent census probes (disposable; review evidence only).

Each probe is a planted copy of hdl/milan/milan_datapath.sv, judged by the
census exactly as CI runs it: publication_census.py --check --datapath COPY,
so every shape the builder builds is elaborated.  Usage:

    probe_r583_6.py TREE OUTDIR JOBS [NAME ...]

TREE is a checkout of the head under review (never edited: the planted copy
is written under OUTDIR).  Each probe writes OUTDIR/<name>.sv, <name>.log and
<name>.rc, and prints one verdict line: whether the census refused it, and
whether that was the expected outcome.
"""
import subprocess
import sys
from pathlib import Path

CRF_DECL = "  wire crft_class_a_w = (ACMP_SRC_C > N_STREAMS) &"
VLAN_EN = "    .vlan_en_i  (crft_class_a_w),"
WIRE = "pp_cd_srp_over_limit_w"


def routed(cond: str, label: str, src: str = WIRE) -> list[tuple[str, str]]:
    """An unmapped read of src inside `if (cond)`, ANDed onto the CRF talker's vlan_en_i (the wire)."""
    decl = (f"  wire probe_w;\n  if ({cond}) begin : {label}\n    assign probe_w = |{src};\n"
            f"  end else begin : {label}_n\n    assign probe_w = 1'b0;\n  end\n")
    return [(CRF_DECL, decl + CRF_DECL), (VLAN_EN, "    .vlan_en_i  (crft_class_a_w & ~probe_w),")]


def status_on_wire(cond: str, label: str) -> list[tuple[str, str]]:
    """The status consumer lwsrp_talker_declared routed onto the wire, only inside `if (cond)`."""
    decl = (f"  wire probe_w;\n  if ({cond}) begin : {label}\n    assign probe_w = lwsrp_talker_declared;\n"
            f"  end else begin : {label}_n\n    assign probe_w = 1'b0;\n  end\n")
    return [(CRF_DECL, decl + CRF_DECL), (VLAN_EN, "    .vlan_en_i  (crft_class_a_w & ~probe_w),")]


#: name -> (edits, expect_refused, words the refusal must carry, why)
PROBES = {
    "wirechans": (routed("TALKER_WIRE_CHANS_P > 4", "g_r5836_wc"), True,
                  ("unmapped read: pp_cd_srp_over_limit_w -> probe_w",),
                  "a read only shapes with 8-channel talkers build (arty_8ch, ax7101_*)"),
    "render": (routed("AUDIO_IF_RENDER_SLOTS_P != 0", "g_r5836_rs"), True,
               ("unmapped read: pp_cd_srp_over_limit_w -> probe_w",),
               "a read only endstation_ax7101_1x1_tdm8 builds (AUDIO_IF_RENDER_SLOTS_P=8)"),
    "status8": (status_on_wire("N_STREAMS > 7", "g_r5836_s8"), True,
                ("lwsrp_talker_declared: counted as status, but it reaches the wire",),
                "a status read on the wire only in the 8-stream shape (endstation_ax7101_8x8)"),
    "gptplat": (routed("GPTP_INGRESS_LAT_NS_P != 0", "g_r5836_gl"), True,
                ("unmapped read: pp_cd_srp_over_limit_w -> probe_w",),
                "a read only the shapes binding a gPTP ingress latency build (ax7101_*)"),
    "unbuilt": (routed("N_STREAMS > 8", "g_r5836_nb"), False, (),
                "limit control: a branch no shape the builder builds elaborates (disclosed limit)"),
}


def main() -> int:
    tree, out, jobs = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve(), sys.argv[3]
    names = sys.argv[4:] or list(PROBES)
    out.mkdir(parents=True, exist_ok=True)
    text = (tree / "hdl/milan/milan_datapath.sv").read_text(encoding="utf-8")
    bad = 0
    for name in names:
        edits, expect, words, why = PROBES[name]
        planted = text
        for old, new in edits:
            assert planted.count(old) == 1, f"{name}: fixture occurs {planted.count(old)} times"
            planted = planted.replace(old, new, 1)
        sv = out / f"{name}.sv"
        sv.write_text(planted, encoding="utf-8")
        done = subprocess.run([sys.executable, "-B", "sw/mailbox/publication_census.py", "--check",
                               "--datapath", str(sv), "--jobs", jobs],
                              cwd=tree, capture_output=True, text=True, check=False)
        log = done.stdout + done.stderr
        (out / f"{name}.log").write_text(log, encoding="utf-8")
        (out / f"{name}.rc").write_text(f"{done.returncode}\n", encoding="utf-8")
        fails = [ln for ln in log.splitlines() if ln.startswith("[FAIL]")]
        refused = done.returncode != 0
        carried = all(any(w in f for f in fails) for w in words)
        ok = refused == expect and (carried if expect else True)
        bad += not ok
        print(f"[{'ok' if ok else 'BAD'}] {name}: rc={done.returncode} refused={refused} expected={expect} "
              f"({why}); first finding: {fails[0] if fails else 'none'}", flush=True)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
