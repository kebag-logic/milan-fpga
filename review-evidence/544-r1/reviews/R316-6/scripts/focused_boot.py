#!/usr/bin/env python3
"""Exercise composition through Gate 1b without running its complete bank.

Load exact candidate source in memory. Return Gate 1b's helpers before its
large lexer/corpus bank. Only the compiler candidate selector and output
directory are redirected; every production assertion remains intact.
"""
import argparse
import ast
import importlib.util
from pathlib import Path
import re
import sys

p = argparse.ArgumentParser()
p.add_argument("root", type=Path)
p.add_argument("scratch", type=Path)
p.add_argument("--compiler", type=Path)
a = p.parse_args()
path = a.root.resolve() / "sw/builder/test_builder.py"
spec = importlib.util.spec_from_file_location("composition_builder", path)
m = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = m
spec.loader.exec_module(m)
m.OUT = a.scratch.resolve() / ("focused-sdk" if a.compiler else "focused-absent")
tree = ast.parse(path.read_text())
fn = next(n for n in tree.body if isinstance(n, ast.FunctionDef)
          and n.name == "test_baremetal_profile_contract")
cut = next(i for i, n in enumerate(fn.body) if isinstance(n, ast.Assign)
           and any(isinstance(t, ast.Name) and t.id == "subset_note" for t in n.targets))
fn.body = fn.body[:cut] + [ast.Return(ast.Call(ast.Name("locals", ast.Load()), [], []))]
selectors = 0
for n in fn.body:
    if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "census_compilers" for t in n.targets):
        n.value = ast.Tuple([ast.Constant(str(a.compiler.absolute()))] if a.compiler else
                           [ast.Constant("cc"), ast.Constant("gcc")], ast.Load())
        selectors += 1
assert selectors == 1
exec(compile(ast.fix_missing_locations(ast.Module([fn], [])), str(path), "exec"), m.__dict__)
d = m.test_baremetal_profile_contract()
gate = d["assert_boot_contract"]
fw, docs, csr, dp = (d[k] for k in ("firmware_source", "docs_source", "csr_source", "datapath_source"))
count = 0
def accepted(label, firmware=fw):
    global count
    verdict = gate(firmware, docs, csr)
    assert bool(verdict["ran"]) == bool(a.compiler)
    count += 1
    print("PASS", label, "compiled census ran:", verdict["ran"])
def refused(label, reason, firmware=fw, datapath=dp):
    global count
    try:
        gate(firmware, docs, csr, datapath=datapath)
    except AssertionError as exc:
        assert reason in str(exc), (label, str(exc))
        count += 1
        print("PASS", label, "refused:", reason)
    else:
        raise AssertionError(label + " unexpectedly accepted")
def replace(text, old, new):
    assert text.count(old) == 1, old
    return text.replace(old, new)
accepted("composed production firmware and NVM entries")
read = re.search(r"uint32_t id = milan_read\(MILAN_ID\);", fw).group()
accepted("authorized discarded sample read", replace(fw, read, read + "\n\t(void)(id & 1u);"))
accepted("fifth existing fence form", replace(fw, read, '__asm__ volatile("fence rw, rw" ::: "memory");\n\t' + read))
for replacement in ("x = MILAN_ID_MAGIC", "((x) = MILAN_ID_MAGIC)"):
    macro = replace(fw, "static int aem_loaded;", "#define MILAN_FORGE(x) " + replacement + "\nstatic int aem_loaded;")
    macro = replace(macro, read, read + "\n\tMILAN_FORGE(id);")
    reason = "identity-sample absence rule" if a.compiler else "identity-sample macro replacement rule"
    refused("published macro " + replacement, reason, firmware=macro)
    key = "assert_preprocessed_identity_sample" if a.compiler else "assert_identity_macro_free"
    cell = dict(zip(gate.__code__.co_freevars, gate.__closure__))[key]
    original = cell.cell_contents
    try:
        cell.cell_contents = lambda *args: None
        accepted("disconnected " + replacement, macro)
    finally:
        cell.cell_contents = original
render = "       media_rebase_p_w\n       | src_recentre_p_r;"
rebase = "wire media_rebase_p_w = eff_ptp_adjust_w | cfg_ptp_cmd_load;"
restart = "                       | media_rebase_p_w;"
controls = (
    ("render ADP term", render, render[:-1] + " | cfg_adp_enable;", "render recentre pulse must read only the media re-base"),
    ("render GM term", render, render.replace("media_rebase_p_w", "gm_recentre_p_r | media_rebase_p_w"), "render recentre pulse must read only the media re-base"),
    ("rebase ADP term", rebase, rebase[:-1] + " | cfg_adp_enable;", "media re-base pulse must read only adjtime and settime"),
    ("restart ADP term", restart, restart[:-1] + " | cfg_adp_enable;", "media restart pulse must read only selected CRF disruption"),
    ("extra PHC reader", rebase, rebase + "\n wire extra_phc_reader_w = phc_load_ts_w;", "phc_load_ts_w must have exactly 4 live references, found 5"),
    ("extra rebase reader", rebase, rebase + "\n wire extra_media_reader_w = media_rebase_p_w;", "media_rebase_p_w must have exactly 3 live references, found 4"),
    ("extra restart reader", restart, restart + "\n wire extra_restart_reader_w = mcr_restart_p_w;", "mcr_restart_p_w must have exactly 2 live references, found 3"),
)
for label, old, new, reason in controls:
    refused(label, reason, datapath=replace(dp, old, new))
port = re.search(r"\.restart_p_i\s*\(mcr_restart_p_w\)", dp).group()
refused("restart port ADP gate", "media restart engine must consume mcr_restart_p_w directly",
        datapath=replace(dp, port, port.replace("mcr_restart_p_w", "mcr_restart_p_w & cfg_adp_enable")))
assert all(f"MILAN_NVM_MAP{direction}_ENTRIES_{k}" in d["census_defines"]
           for direction in ("IN", "OUT") for k in range(16))
assert not any("_CLUSTERS_" in k for k in d["census_defines"])
print("PASS #501 census constants: all 32 entry keys, no stale cluster keys")
print("PASS focused boot cases:", count, "mode:", "SDK" if a.compiler else "ABSENT")
print("Scope: production path, two legitimate controls, original macro/disconnection controls, eight predecessor structural refusals; no full builder bank or RTL elaboration.")
