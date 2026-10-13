"""Print the bytecode of execute_act_boundary's lines 5350-5351 and the monitor's yield/except lines.

Usage (inside scripts/sandbox.sh): python3 -I dis_boundary_finally.py <tree-root>
An eval-breaker check (where a Python signal handler can run without a tracer)
sits only at RESUME, JUMP_BACKWARD and the CALL family; this lists the
instructions a first signal could meet between an exception reaching the
boundary's `finally` and the mask-restoring call.
"""
import dis, importlib.util, pathlib, sys
root = pathlib.Path(sys.argv[1]).resolve()
spec = importlib.util.spec_from_file_location("act_ci_dis", root / "scripts" / "act_ci.py")
m = importlib.util.module_from_spec(spec); sys.modules["act_ci_dis"] = m; spec.loader.exec_module(m)
print(sys.version)
for ins in dis.get_instructions(m.execute_act_boundary):
    if ins.positions and ins.positions.lineno in (5350, 5351):
        print(ins.positions.lineno, ins.offset, ins.opname, ins.argrepr)
