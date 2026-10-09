import importlib.util, json, time
from pathlib import Path
w = Path(__file__).resolve().parent
bench = w / "bench-inputs/tb/verilator/milan_dp_render"
spec = importlib.util.spec_from_file_location("render_mutations", bench / "tdm8_render_mutants.py")
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
case, = [c for c in m.MUTATIONS if c[0] == "the settle recentre never pulses"]
name, source, edits, leg, mode, breaks = case
out = w / "pullin-control"
out.mkdir()
value, error = m.plant(source, edits, out, "no_settle")
assert value is not None, error
start = time.monotonic()
exe = m.build(leg, {m.SOURCES[source][1]: value}, out / "obj")
assert exe is not None, "control build failed"
rc, log = m.run_leg(exe, mode)
(out / "negative.log").write_text(log)
(out / "negative.rc").write_text(str(rc) + "\n")
v = m.verdict(rc, log, breaks)
receipt = dict(case=name, mode=mode, expected_failure=breaks, rc=rc, verdict=v,
               seconds=round(time.monotonic() - start, 3))
(out / "result.json").write_text(json.dumps(receipt, indent=2) + "\n")
print(json.dumps(receipt, indent=2), flush=True)
assert v == "caught", v
print("PULLIN control: named defect caught", flush=True)
