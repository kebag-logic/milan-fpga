#!/usr/bin/env python3
"""Run the default ci_events self-test with one in-memory source mutation."""
import hashlib
from pathlib import Path
import sys
import types
root = Path.cwd()
source = (root / "scripts/ci_events.py").read_text()
name = sys.argv[1]
edits = {
    "omit-call": ("            check_carrier_script(c, path, what, at, entry)", "            pass"),
    "omit-seven-jobs": ("or (path, jid) in RTL_STEP_LISTS", "or False"),
    "omit-sha-step": ('and entry.get("id") == PIN_STEP_ID', 'and False'),
    "accept-content-drift": ("c.item(tuple(lines) == canonical, path,", "c.item(True, path,"),
    "accept-missing-record": ("c.item(recorded, path,", "c.item(True, path,"),
}
old, new = edits[name]
assert source.count(old) == 1, (name, source.count(old))
mutated = source.replace(old, new)
output = Path(__file__).resolve().parent / "mutants"
output.mkdir(exist_ok=True)
(output / (name + ".py")).write_text(mutated)
print(f"mutation={name} source_sha256={hashlib.sha256(mutated.encode()).hexdigest()}")
module = types.ModuleType("ci_events_mutant")
module.__file__ = str(root / "scripts/ci_events.py")
sys.modules[module.__name__] = module
exec(compile(mutated, module.__file__, "exec"), module.__dict__)
clean = module.check(module.parse_world(module.read_tree(root)))
print(f"mutated live check: items={clean.checked} findings={clean.findings!r}")
sys.exit(module.selftest(root))
