#!/usr/bin/env python3
"""Reviewer harness (R583-5): run an earlier reviewer's in-process census probe,
unmodified, against the head, with the probe modules it instantiates defined.

usage: run_prior_probes.py REPO PROBE_SCRIPT [define|asis]

The earlier probes instantiate KL_probe_sink and KL_probe_buf without defining
them; a netlist census elaborated with `hierarchy -check` refuses any arm for
that alone. With `define`, this harness wraps publication_census.load so the
datapath text it returns ends with blackbox definitions of both modules (every
port name any probe connects), then runs PROBE_SCRIPT as __main__ with argv
[PROBE_SCRIPT, REPO]. With `asis`, the probe runs with nothing defined.
"""
import runpy
import sys
from dataclasses import replace
from pathlib import Path

repo, probe = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
mode = sys.argv[3] if len(sys.argv) > 3 else "define"
sys.path.insert(0, str(repo / "sw/mailbox"))
import publication_census as pc  # noqa: E402

TAIL = "\n`default_nettype wire\n"
MODS = ("module KL_probe_sink (input logic [1:0] a_i, input logic [1:0] a_o);\nendmodule\n"
        "module KL_probe_buf (input logic [1:0] a, output logic y_o, input logic [1:0] lwsrp_talker_declared,\n"
        "  input logic [1:0] gsi_tkdcl_w, input logic [1:0] pp_cd_srp_over_limit_w);\nendmodule\n")

if mode == "define":
    orig = pc.load

    def load(datapath, wrapper):
        src = orig(datapath, wrapper)
        assert src.datapath.endswith(TAIL), "the datapath no longer ends where the probe modules go"
        return replace(src, datapath=src.datapath + MODS)
    pc.load = load
sys.argv = [str(probe), str(repo)]
runpy.run_path(str(probe), run_name="__main__")
