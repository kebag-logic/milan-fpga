# Standalone bounded validation helper; run from a disposable candidate checkout.
import ast
import json
import os
from pathlib import Path
import subprocess
import sys
import types

repo = Path.cwd()
work = Path(os.environ["VALIDATION_WORK"]).resolve()
sys.path.insert(0, str(repo / "sw/builder"))
import test_builder as gate
from test_declarations import test_declaration_contracts
from test_clock_contract import (test_baremetal_clock_contract, test_builder_clock_source,
                                test_extra_sweep_clocks, test_extra_sweep_invocation,
                                test_sim_clock, test_tap_clock_docs)
for name, value in list(globals().items()):
    if name.startswith("test_"):
        setattr(gate, name, value)

source = ast.parse((repo / "sw/builder/test_builder.py").read_text())
main = source.body[-1]
loop = next(n for n in main.body if isinstance(n, ast.For))
names = [n.id for n in loop.iter.elts]
first, last = map(int, sys.argv[1:3])
original_run = subprocess.run
old_cc = str(Path.home() / "br-milan-rv32/host/bin/riscv32-linux-gcc")
new_cc = str(Path(os.environ["RV32_SDK"]) / "bin/riscv32-linux-gcc")

def run(argv, *args, **kwargs):
    if isinstance(argv, (list, tuple)) and argv and str(argv[0]) == old_cc:
        argv = [new_cc, *argv[1:]]
    return original_run(argv, *args, **kwargs)

subprocess.run = run
# Function 13's census is divided into disjoint slices. The prefix phase runs
# the function through its mutation loop over one slice, then applies the
# loop's own elaboration accounting (asserted after the loop in the original)
# before returning. The suffix phase skips the mutation loop and runs the
# rest of the function, with one slice of the disconnected identity controls.
# Every assertion inside both loops is unchanged.
if "--census-shard" in sys.argv:
    shard, count = map(int, sys.argv[sys.argv.index("--census-shard")+1].split("/"))
    phase = sys.argv[sys.argv.index("--census-phase")+1]
    assert phase in ("prefix", "suffix")
    function = next(n for n in source.body if isinstance(n, ast.FunctionDef) and n.name == "test_baremetal_profile_contract")
    loops = [n for n in ast.walk(function) if isinstance(n, ast.For) and isinstance(n.target, ast.Name)
             and n.target.id == "mutation" and isinstance(n.iter, ast.Name) and n.iter.id == "mutations"]
    assert len(loops) == 1 and loops[0] in function.body
    mutation_loop = loops[0]
    manifest = {}
    path = work / f"builder-{phase}-{shard}-cases.json"
    def cases(items, kind):
        items = list(items)
        chosen = items[shard::count]
        manifest.update(all=[m[0] for m in items], selected=[m[0] for m in chosen],
                        completed=[], shard=shard, count=count, phase=phase, kind=kind)
        path.write_text(json.dumps(manifest)+"\n")
        print(f"Census {phase} {shard}/{count}: {len(chosen)} of {len(items)} {kind}", flush=True)
        for case in chosen:
            print("Census case", case[0], flush=True)
            yield case
            manifest["completed"].append(case[0])
            path.write_text(json.dumps(manifest)+"\n")
            print("Census case passed", case[0], flush=True)
    def shard_mutations(mutations):
        return cases(mutations, "mutations") if phase == "prefix" else ()
    def census_prefix_done(verilator, elaboration):
        assert verilator, "census prefix needs Verilator; RTL mutation elaboration would stand down"
        assert elaboration["passed"] == elaboration["requested"], \
            "not every RTL mutation was elaborated before being counted"
        assert manifest["completed"] == manifest["selected"]
        manifest.update(rtl_requested=elaboration["requested"], rtl_passed=elaboration["passed"])
        path.write_text(json.dumps(manifest)+"\n")
        print(f"Census prefix {shard}/{count}: {len(manifest['completed'])} mutations rejected; "
              f"{elaboration['passed']}/{elaboration['requested']} RTL variants elaborated", flush=True)
    mutation_loop.iter = ast.copy_location(ast.Call(func=ast.Name(id="shard_mutations", ctx=ast.Load()),
                                                   args=[mutation_loop.iter], keywords=[]), mutation_loop.iter)
    gate.shard_mutations = shard_mutations
    gate.census_prefix_done = census_prefix_done
    if phase == "prefix":
        position = function.body.index(mutation_loop)
        tail = ast.parse("census_prefix_done(verilator, rtl_mutant_elaboration)\nreturn").body
        for node in tail:
            ast.copy_location(node, mutation_loop)
        function.body[position+1:position+1] = tail
    else:
        controls = [n for n in ast.walk(function) if isinstance(n, ast.For)
                    and ast.unparse(n.target) == "(label, fixture)" and ast.unparse(n.iter) == "controls.items()"]
        assert len(controls) == 1
        controls[0].iter = ast.copy_location(ast.Call(func=ast.Name(id="shard_controls", ctx=ast.Load()),
                                                     args=[controls[0].iter], keywords=[]), controls[0].iter)
        gate.shard_controls = lambda values: cases(values, "disconnected identity controls")
    ast.fix_missing_locations(function)
    exec(compile(ast.Module(body=[function], type_ignores=[]), str(repo/"sw/builder/test_builder.py"), "exec"), gate.__dict__)

print(f"Builder batch {first}-{last}/{len(names)}; pinned SDK compiler mapping only", flush=True)
selected = [n for n in names[first-1:last] if "--without-census" not in sys.argv or n != "test_baremetal_profile_contract"]
for name in selected:
    print(name, flush=True)
    getattr(gate, name)()
for skipped in gate.SKIPPED:
    print("NOT RUN", skipped, flush=True)
label = f"{first}-{last}" + (f"-{phase}-{shard}" if "--census-shard" in sys.argv else "")
print(f"Builder batch {label}: {len(selected)} selected functions/phases completed, {len(gate.SKIPPED)} recorded skips", flush=True)
(work / f"builder-{label}.json").write_text(json.dumps(dict(tests=selected, skipped=gate.SKIPPED)) + "\n")
