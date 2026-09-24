#!/usr/bin/env python3
"""Run the parent's unchanged Rule 11 measurement in disposable scratch."""
import hashlib
import importlib.util
from pathlib import Path
import shutil
import sys
import tempfile

sys.dont_write_bytecode = True
parent = Path('$LANES/pp43-parent-consumer/scripts')
source = Path(sys.argv[1]).resolve()
text = source.read_text()
with tempfile.TemporaryDirectory(prefix='pp43-a262-cpp-', dir='/tmp') as temp:
    scratch = Path(temp)
    for name in ('check_cpp_idiom.py', 'cpp_idiom.budget', 'code_quality_scope.py'):
        original = parent / name
        copied = scratch / name
        shutil.copy2(original, copied)
        assert original.read_bytes() == copied.read_bytes()
        digest = hashlib.sha256(copied.read_bytes()).hexdigest()
        print(f'Copied unchanged {name}: sha256 {digest}')
    spec = importlib.util.spec_from_file_location('check_cpp_idiom', scratch / 'check_cpp_idiom.py')
    gate = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(gate)
    code = gate.blank_non_code(text)
    functions = gate.long_functions(code, limit=0)
    oversized = gate.long_functions(code)
    counts = gate.scan(text, 'tb/srp_stream_fsms/sim_main.cpp')
    budget = gate.read_budget()
    failures, notes = gate.ratchet(counts, budget)
    print(f'Source: {source}')
    print(f'Source sha256: {hashlib.sha256(source.read_bytes()).hexdigest()}')
    print(f'Limit: {gate.LONG_FUNCTION_LINES} physical lines (inclusive signature and closing brace)')
    print(f'Functions measured: {len(functions)}')
    for line, length in functions:
        print(f'{line}: {length} lines: {text.splitlines()[line - 1].strip()}')
    print(f'Maximum: {max(length for _, length in functions)} lines')
    print(f'long_functions(): {oversized}')
    print(f'long function: {counts["long function"]} <= {budget["long function"]}: '
          f'{"PASS" if counts["long function"] <= budget["long function"] else "FAIL"}')
    for finding in failures + notes:
        print(finding)
    verdict = bool(failures or any(counts[key] for key in gate.REFUSED))
    print(f'Source scan and unchanged budget: {"FAIL" if verdict else "PASS"}')
print(f'Scratch deleted: {not scratch.exists()} ({scratch})')
sys.exit(1 if verdict else 0)
