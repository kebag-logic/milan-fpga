"""Plant mutants in kl_servo_reset_sync_constraints and run the stub-netlist test on each.

usage: python3 -I -B tcl_mutants.py <clean-tree> <scratch-dir> <out-dir>
Each mutant is one exact text replacement in a disposable copy of
sw/litex/clock_constraints.tcl; the clean tree is never written. KILLED means
the test exits non-zero; SURVIVED means it passes with the mutant planted.
"""
import json
import shutil
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

clean, scratch, out = (Path(a).resolve() for a in sys.argv[1:4])
driver = Path(__file__).resolve().parent / "servo_stub_driver.py"
TCL = "sw/litex/clock_constraints.tcl"

MUTANTS = {
    "K00-control-unmutated": [],
    "K01-cut-removed": [("    set_false_path -from $src -to $pin\n", "")],
    "K02-cut-widened-from-dropped": [("set_false_path -from $src -to $pin", "set_false_path -to $pin")],
    "K03-cut-on-second-stage": [("-of_objects $first -filter {REF_PIN_NAME == D}", "-of_objects $second -filter {REF_PIN_NAME == D}")],
    "K04-cut-setup-only": [("set_false_path -from $src -to $pin", "set_false_path -setup -from $src -to $pin")],
    "K05-cut-to-cell-not-pin": [("set_false_path -from $src -to $pin", "set_false_path -from $src -to $first")],
    "K06-stage-count-check-dropped": [("    if {[llength $stages] != 2} {\n", "    if {0} {\n")],
    "K07-asyncreg-check-dropped": [("if {![string is true -strict [get_property ASYNC_REG $cell]]} {", "if {0} {")],
    "K08-asyncreg-check-first-listed-cell-only": [("if {![string is true -strict [get_property ASYNC_REG $cell]]} {", "if {$cell eq [lindex $stages 0] && ![string is true -strict [get_property ASYNC_REG $cell]]} {")],
    "K09-asyncreg-check-last-listed-cell-only": [("if {![string is true -strict [get_property ASYNC_REG $cell]]} {", "if {$cell eq [lindex $stages end] && ![string is true -strict [get_property ASYNC_REG $cell]]} {")],
    "K10-asyncreg-non-strict-any-value": [("if {![string is true -strict [get_property ASYNC_REG $cell]]} {", "if {[get_property ASYNC_REG $cell] eq {}} {")],
    "K11-chain-check-dropped": [("    if {[llength $first] != 1 || [llength $second] != 1} {\n", "    if {0} {\n")],
    "K12-chain-check-first-only": [("[llength $first] != 1 || [llength $second] != 1", "[llength $first] < 1")],
    "K13-clock-check-dropped": [("    if {[llength $dst] != 1 || [lindex $dst 0] eq [lindex $src 0]} {\n", "    if {0} {\n")],
    "K14-clock-check-distinct-only": [("[llength $dst] != 1 || [lindex $dst 0] eq [lindex $src 0]", "[lindex $dst 0] eq [lindex $src 0]")],
    "K15-clock-check-count-only": [("[llength $dst] != 1 || [lindex $dst 0] eq [lindex $src 0]", "[llength $dst] != 1")],
    "K16-src-clock-unchecked": [("    set src [kl_net_clock $milan_net]\n", "    set src [get_clocks -of_objects [get_nets $milan_net]]\n")],
    "K17-stage-filter-widened-to-any-psrst": [('-filter {NAME =~ "*mmcm_servo/psrst_sync_r_reg*"}', '-filter {NAME =~ "*psrst*"}')],
}


def run(name: str, edits: list) -> dict:
    tree = scratch / name
    shutil.rmtree(tree, ignore_errors=True)
    for rel in ("sw/builder/test_clock_constraints.py", "sw/litex/clock_constraints.py", TCL):
        (tree / rel).parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(clean / rel, tree / rel)
    text = (tree / TCL).read_text()
    for old, new in edits:
        assert text.count(old) == 1, f"{name}: anchor not unique: {old!r}"
        text = text.replace(old, new)
    (tree / TCL).write_text(text)
    result = subprocess.run([sys.executable, "-I", "-B", str(driver), str(tree)],
                            capture_output=True, text=True, timeout=120)
    log = out / f"{name}.log"
    log.write_text(f"rc={result.returncode}\n--- stdout\n{result.stdout}--- stderr\n{result.stderr}")
    killed = result.returncode != 0
    expected_pass = not edits
    verdict = ("CONTROL-PASS" if not killed else "CONTROL-FAIL") if expected_pass else ("KILLED" if killed else "SURVIVED")
    last = [l for l in (result.stdout + result.stderr).splitlines() if l.strip()]
    return {"mutant": name, "rc": result.returncode, "verdict": verdict, "last_line": last[-1] if last else ""}


out.mkdir(parents=True, exist_ok=True)
with ThreadPoolExecutor(max_workers=16) as pool:
    results = list(pool.map(lambda kv: run(*kv), MUTANTS.items()))
(out / "results.json").write_text(json.dumps(results, indent=1) + "\n")
for r in results:
    print(f"{r['verdict']:13s} {r['mutant']}  rc={r['rc']}  | {r['last_line'][:150]}")
