#!/usr/bin/env python3
"""Time gate 1h's reads, serially or across worker threads, with the gate's own functions.

usage: gate1h_cost.py <clone root> <workers>. Prints wall seconds and every control's answer count.
"""
import concurrent.futures, importlib.util, pathlib, sys, time
root = pathlib.Path(sys.argv[1]).resolve()
workers = int(sys.argv[2])
sys.argv = [sys.argv[0]]
sys.path.insert(0, str(root / "sw/builder"))
spec = importlib.util.spec_from_file_location("tb", root / "sw/builder/test_builder.py")
tb = importlib.util.module_from_spec(spec)
spec.loader.exec_module(tb)
rtl = (root / "hdl/milan/milan_datapath.sv").read_text()
cuts = tb._datapath_shape_cuts(rtl)
keeps = tb._datapath_shape_keeps(rtl)
texts = [rtl] + [c[1] for c in cuts] + [k[1] for k in keeps]
start = time.monotonic()
with concurrent.futures.ThreadPoolExecutor(workers) as pool:
    answers = list(pool.map(tb._datapath_shape_findings, texts))
wall = time.monotonic() - start
wrong = bool(answers[0]) + sum(not any(c[2] in a for a in ans) for c, ans in zip(cuts, answers[1:]))
wrong += sum(bool(ans) for ans in answers[1 + len(cuts):])
print(f"reads {len(texts)} workers {workers} wall {wall:.1f} s per read {wall / len(texts):.2f} s wrong {wrong}")
