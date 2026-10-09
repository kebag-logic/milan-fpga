#!/usr/bin/env python3
"""Independent compatibility and negative probes; every synthetic input stays in scratch."""
import copy
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

root, packet = map(lambda x: Path(x).resolve(), sys.argv[1:3])
scratch = Path(tempfile.mkdtemp(prefix="independent-", dir=packet / "scratch"))
base = "7c1b52bee26b497080ee22b1c1986109f80a5ee7"
sys.path.insert(0, str(root / "syn/ooc"))
import pp_baseline as recipe
import pp_resource_gate as gate
import pp_placement as placement
from pp_resource_gate_selftest import fixture

def load_base(name):
    path = scratch / ("base_" + name + ".py")
    path.write_bytes(subprocess.check_output(["git", "-C", str(root), "show", base + ":syn/ooc/" + name + ".py"]))
    spec = importlib.util.spec_from_file_location("base_" + name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

old_recipe, old_gate = load_base("pp_baseline"), load_base("pp_resource_gate")
baseline_path = root / "syn/ooc/pp_resource_baseline.json"
baseline_bytes = baseline_path.read_bytes()
assert baseline_bytes == subprocess.check_output(["git", "-C", str(root), "show", base + ":syn/ooc/pp_resource_baseline.json"])
baseline = gate.load(baseline_path)
print("BASELINE unchanged:", hashlib.sha256(baseline_bytes).hexdigest(), len(baseline_bytes), "bytes")
for field in ("ROWS", "GATED", "TIMING", "CEILINGS", "COLUMNS", "POLICY", "RECORD", "IDENTITY", "SCOPE", "NOTES"):
    assert getattr(gate, field) == getattr(old_gate, field), field
assert old_gate.policy_table((root / "docs/design/AREA_BUDGET.md").read_text()) == gate.policy_table((root / "docs/design/AREA_BUDGET.md").read_text())
print("PASS: accepted schema and policy constants match base")

# Rejudge the three stored records, explicitly without inventing route-status evidence.
for endpoint, entry in baseline["endpoints"].items():
    status, lines = gate.judge(entry, copy.deepcopy(entry["record"]))
    assert (status, lines) == old_gate.judge(entry, copy.deepcopy(entry["record"]))
    assert status == 0
    print("STORED RECORD REPLAY", endpoint, "status", status, "(not a new measurement)")
    print(json.dumps(entry["record"]["identity"], sort_keys=True))
    print(json.dumps(entry["record"]["figures"], sort_keys=True))
    print("\n".join(lines))
    # Real parser and check CLI over unchanged synthetic report sets in both revisions.
    folder = fixture(scratch / endpoint, entry["record"]["kind"])
    before = old_gate.record(folder, entry["record"]["kind"])
    after = gate.record(folder, entry["record"]["kind"], "all-fabric")
    assert before == after, endpoint
    if entry["record"]["kind"] == "route":
        assert old_gate.routing(folder, "route") == gate.routing(folder, "route") == []
    print("PASS: base/head report parsing, input digest, figures, scopes and route-status parity", endpoint)

# A compact synthetic export independently exercises generated Tcl byte parity.
folder = scratch / "export"
folder.mkdir(exist_ok=True)
reads, bindings = [], []
for parameter, package, widthname, depthname, depthvalue in (
    ("PP_TROM_HEX_P", "pp_acmp_pkg.sv", "TROM_W_C", "TROM_DEPTH_C", 4),
    ("PP_UCODE_HEX_P", "ucpu_pkg.sv", "UCODE_W_C", "UPC_W_C", 2),
    ("GPTP_UCODE_HEX_P", "gptp_ucpu_pkg.sv", "UCODE_W_C", "UPC_W_C", 2),
):
    path = folder / package
    path.write_text(f"parameter {widthname} = 16;\nparameter {depthname} = {depthvalue};\n")
    rom = folder / (parameter + ".hex")
    rom.write_text("1234\n5678\n9abc\ndef0\n")
    reads.append(f"read_verilog {{{path}}}\n")
    bindings.append(f'.{parameter}("{rom}")')
wrapper = folder / "KL_pp_shadow.sv"
wrapper.write_text("parameter int unsigned N_STREAM_IN_P = 1,\nparameter int unsigned N_STREAM_OUT_P = 1,\nparameter int unsigned CLK_HZ_P = 50_000_000,\n")
reads.append(f"read_verilog {{{wrapper}}}\n")
top = folder / "alinx_ax7101.v"
top.write_text("\n".join(bindings) + "\n")
source = ("create_project -force -name alinx_ax7101 -part xc7a100t-fgg484-2\n"
          "set_param general.maxThreads 32\n" + "".join(reads) + "# Add constraints\n"
          "synth_design -directive AreaOptimized_high -top alinx_ax7101 -part xc7a100t-fgg484-2\n"
          "# Add pre-optimize commands\nopt_design -directive ExploreArea\n"
          "place_design -directive ExtraPostPlacementOpt\nphys_opt_design -directive AggressiveExplore\n"
          "route_design -directive AggressiveExplore\n# Bitstream generation\n")
(folder / "alinx_ax7101.tcl").write_text(source)
log = folder / "synthesis.log"
for shape in (1, 8):
    log.write_text("INFO: synthesizing module 'KL_pp_shadow' [wrapper.sv:1]\n"
                   f"Parameter N_STREAM_IN_P bound to: {shape} - type: integer\n"
                   f"Parameter N_STREAM_OUT_P bound to: {shape} - type: integer\n"
                   "Parameter CLK_HZ_P bound to: 50000000 - type: integer\nINFO: end\n")
    out = scratch / ("standalone-" + str(shape))
    for label, target, evidence, synth in (
        ("route", folder, None, False), ("integrated-synthesis", folder, None, True),
        ("standalone", out, log, False),
    ):
        old_recipe.prepare(folder, target, evidence, synth, integrated_clock=bool(evidence))
        names = ["baseline_images.json", "baseline_ooc.tcl" if evidence else "baseline_integrated.tcl"]
        if evidence:
            names += ["clock.xdc", "baseline_parameters.json", "baseline_chparam.txt"]
        expected = {name: (target / name).read_bytes() for name in names}
        recipe.prepare(folder, target, evidence, synth, integrated_clock=bool(evidence))
        assert expected == {name: (target / name).read_bytes() for name in names}
        print(f"PASS: base/head recipe byte parity {label} shape {shape}x{shape}")

# Independent split census format and cardinality probes beyond the committed suite.
roles = ("wrapper", "adp", "acmp-listener", "acmp-talker", "srp", "maap", "processor-maap", "aecp", "notify", "mailbox", "gptp")
for selected, counts in (
    ("f0-f4", [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1]),
    ("full-split", [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1]),
):
    report = folder / "baseline_placement.tsv"
    text = "placement\trole\tcount\n" + "".join(f"{selected}\t{role}\t{count}\n" for role, count in zip(roles, counts))
    marker = "# baseline placement: " + selected + "\n"
    report.write_text(text)
    placement.validate(folder, marker, selected)
    for label, changed, reason in (
        ("oversized count", text.replace("\tmailbox\t1", "\tmailbox\t" + "1"*16), "invalid"),
        ("unicode count", text.replace("\tmailbox\t1", "\tmailbox\t１"), "invalid"),
        ("unknown role", text + f"{selected}\textra\t0\n", "invalid"),
        ("duplicate required engine", text.replace("\tgptp\t1", "\tgptp\t2"), "gptp"),
        ("missing mailbox", text.replace("\tmailbox\t1", "\tmailbox\t0"), "mailbox"),
        ("retained moved engine", text.replace("\tsrp\t0", "\tsrp\t1"), "srp"),
    ):
        report.write_text(changed)
        try:
            placement.validate(folder, marker, selected)
        except ValueError as error:
            assert reason in str(error), error
            print("PASS named refusal", selected, label, str(error))
        else:
            raise AssertionError((selected, label, "accepted"))
    report.write_text(text)
    if selected == "f0-f4":
        report.write_text(text.replace("\twrapper\t0", "\twrapper\t1"))
        placement.validate(folder, marker, selected)
        print("PASS: partial placement accepts exactly zero or one wrapper")
assert baseline_path.read_bytes() == baseline_bytes
modules = ("KL_pp_shadow", "KL_adp_engine", "KL_pp_acmp_listener", "KL_acmp_talker", "KL_srp_top", "KL_maap", "KL_pp_maap", "KL_aecp_engine", "KL_aecp_notify", "KL_mbx", "KL_gptp_shadow")
for selected, counts in (("f0-f4", [0,0,0,0,0,0,0,1,1,1,1]),
                         ("full-split", [0,0,0,0,0,0,0,0,0,1,1])):
    recipe.prepare_split(folder, False, selected)
    generated = (folder / "baseline_integrated.tcl").read_text()
    preamble = r'''
set queries 0
set phase setup
foreach command {create_project set_param read_verilog set_msg_config opt_design place_design phys_opt_design} {
  proc $command {args} {}
}
proc synth_design {args} {global phase; set phase synthesis}
proc route_design {args} {global phase; set phase route}
proc get_cells {args} {
  global population queries phase fault
  set filter [lindex $args end]
  if {[regexp {ORIG_REF_NAME == (\w+)} $filter -> module]} {
    incr queries
    if {$fault eq "late-mailbox" && $phase eq "route" && $module eq "KL_mbx"} {return {}}
    if {$fault eq "early-adp" && $module eq "KL_adp_engine"} {return unexpected_adp}
    return [lrepeat [dict get $population $module] instance]
  }
  if {$filter eq "IS_SEQUENTIAL == 1" || $filter eq "IS_PRIMITIVE == 1"} {return reg0}
  error "unexpected query: $filter"
}
proc get_property {name object} {
  if {$name eq "SLACK"} {return 0.350}
  if {$name eq "REF_NAME"} {return FDRE}
  error "unexpected property"
}
proc get_timing_paths {args} {return path0}
proc report_utilization {args} {set f [open [lindex $args end] w]; puts $f fixture; close $f}
proc report_timing_summary {args} {set f [open [lindex $args end] w]; puts $f fixture; close $f}
proc quit {} {global queries; if {$queries != 22} {error "missing census stage"}; puts "PASS: both census stages executed"}
'''
    for fault, expected in (("none", "PASS: both census stages executed"),
                            ("early-adp", "adp (KL_adp_engine)"),
                            ("late-mailbox", "mailbox (KL_mbx)")):
        model = "set population {" + " ".join(f"{module} {count}" for module,count in zip(modules,counts)) + "}\n"
        path = folder / "execute-generated.tcl"
        path.write_text(model + "set fault " + fault + "\n" + preamble + generated)
        result = subprocess.run(["tclsh", str(path)], cwd=folder, text=True, capture_output=True, timeout=10)
        assert (result.returncode == 0) == (fault == "none"), result
        assert expected in result.stdout + result.stderr, result
        if fault == "none":
            assert (folder / "baseline_scope_timing.tsv").read_text().splitlines()[1] == "image\t1\t0.350"
            placement.validate(folder, generated, selected)
        print("PASS: entire generated Tcl", selected, fault, "rc", result.returncode, expected)

# The legacy wrapper requirement is executed, not inferred from a matching string.
path = folder / "missing-wrapper.tcl"
path.write_text("proc get_cells {args} {return {}}\n" + recipe.PP_REPORTS)
result = subprocess.run(["tclsh", str(path)], cwd=folder, text=True, capture_output=True, timeout=10)
assert result.returncode != 0 and "Expected exactly one protocol wrapper" in result.stderr
print("PASS: legacy missing-wrapper fails by name: Expected exactly one protocol wrapper")
print("PASS: all independent probes; no accepted record or source byte changed")
