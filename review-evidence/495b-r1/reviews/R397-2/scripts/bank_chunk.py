#!/usr/bin/env python3
"""Run a contiguous slice of a bank's own `for fn in (...)` run list, unmodified otherwise.

The bank file is parsed and compiled from its own path with its own line numbers;
the only change is that the run-list tuple is subscripted with [START:END], and each
fn call is timed on stderr. The bank's own verdict code (SKIPPED ledger, ALL GATES
PASS, --require-elaboration exit) runs at the end of each slice. Used because the full
bank exceeds a single ten-minute foreground command on this host.

Usage: bank_chunk.py <bank.py> <start> <end> [bank args...]
"""
import ast, sys, time, os
bank, start, end = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
bank = os.path.abspath(bank)
src = open(bank).read()
tree = ast.parse(src, bank)
loops = [n for n in ast.walk(tree) if isinstance(n, ast.For) and isinstance(n.target, ast.Name) and n.target.id == "fn"]
assert len(loops) == 1, "run list not found exactly once"
loop = loops[0]
names = [e.id for e in loop.iter.elts]
print(f"[chunk] {bank} slice [{start}:{end}] of {len(names)}: {names[start:end]}", file=sys.stderr, flush=True)
loop.iter = ast.Subscript(value=loop.iter, slice=ast.Slice(lower=ast.Constant(start), upper=ast.Constant(end)), ctx=ast.Load())
# time each call: wrap body as  _t0=time.time(); <body>; print elapsed
timing_pre = ast.parse("import time as _chunk_time, sys as _chunk_sys\n_chunk_t0 = _chunk_time.time()").body
timing_post = ast.parse("print(f'[chunk-time] {fn.__name__} {_chunk_time.time()-_chunk_t0:.1f}s', file=_chunk_sys.stderr, flush=True)").body
loop.body = timing_pre + loop.body + timing_post
ast.fix_missing_locations(tree)
code = compile(tree, bank, "exec")
sys.argv = [bank] + sys.argv[4:]
sys.path.insert(0, os.path.dirname(bank))
g = {"__name__": "__main__", "__file__": bank, "__builtins__": __builtins__}
sys.modules["__main__"].__dict__.update(g)
exec(code, sys.modules["__main__"].__dict__)
