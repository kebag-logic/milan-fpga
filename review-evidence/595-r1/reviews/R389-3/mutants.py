#!/usr/bin/env python3
"""Composed-tree mutation controls. Usage: mutants.py <disposable tree root>

Each mutant edits sw/builder/endstation_builder.py in the disposable tree,
runs its killing check, then restores the exact original bytes. Controls run
the same checks unmutated first and last.
  M1 _mac48 rereads str(v) as hex (integer acceptance)      -> test_declarations.py
  M2 _declared_uint accepts YAML integers                    -> test_declarations.py
  M3 scalar `formats` falls back to defaults / iterates      -> test_declarations.py
  M4 #577 image check removed from _entity_model_image       -> gate 36b functions
  M5 #577 image check error swallowed                        -> gate 36b functions
"""
import hashlib
import subprocess
import sys
from pathlib import Path

root = Path(sys.argv[1]).resolve()
target = root / "sw/builder/endstation_builder.py"
original = target.read_bytes()
digest = hashlib.sha256(original).hexdigest()

DECL = [sys.executable, "sw/builder/test_declarations.py"]
GATE36B = [sys.executable, "-c",
           "import sys; sys.path.insert(0, 'sw/builder'); import test_builder as t; "
           "t.test_shipping_image_contract(); t.test_soc_shipping_image_contract(); "
           "t.test_schema_12_refusals(); print('36b+schema12 ok')"]

MUTANTS = {
    "M1": ('    if not isinstance(v, str):\n'
           '        raise ConfigError(f"{ctx}: quote the hexadecimal value as a YAML string")\n'
           '    s = v.replace(":", "").replace("-", "").replace("_", "")',
           '    s = str(v).replace(":", "").replace("-", "").replace("_", "")', DECL),
    "M2": ('    """An unsigned quoted hex field, refused outside `bits` bits."""\n'
           '    if not isinstance(v, str):\n'
           '        raise ConfigError(f"{ctx}: quote the hexadecimal value as a YAML string")\n'
           '    try:\n'
           '        n = int(v, 16)',
           '    """An unsigned quoted hex field, refused outside `bits` bits."""\n'
           '    if isinstance(v, bool) or not isinstance(v, (int, str)):\n'
           '        raise ConfigError(f"{ctx}: quote the hexadecimal value as a YAML string")\n'
           '    try:\n'
           '        n = v if isinstance(v, int) else int(v, 16)', DECL),
    "M3": ('        fmts = s.get("formats", [])\n'
           '        if not isinstance(fmts, list):\n'
           '            raise ConfigError(f"{sctx}.formats: must be a list of quoted hexadecimal strings")\n'
           '        fmts = fmts or [f"0x{aaf_pcm32(ch, rate_hz):016X}"]',
           '        fmts = s.get("formats") or [f"0x{aaf_pcm32(ch, rate_hz):016X}"]', DECL),
    "M4": ('        aem_image_checks.validate_shipping_image(blob)\n',
           '        pass\n', GATE36B),
    "M5": ('        raise ConfigError(f"aem_desc.bin: {exc}") from exc\n',
           '        pass\n', GATE36B),
}


def run(argv):
    r = subprocess.run(argv, cwd=root, capture_output=True, text=True)
    tail = (r.stdout + r.stderr).strip().splitlines()[-1:] or [""]
    return r.returncode, tail[0][:160]


ok = True
for name, argv in (("control-decl", DECL), ("control-36b", GATE36B)):
    rc, tail = run(argv)
    print(f"{name}: rc={rc} {tail}")
    ok &= rc == 0
text = original.decode()
for name, (old, new, argv) in MUTANTS.items():
    assert text.count(old) == 1, f"{name}: anchor not unique ({text.count(old)})"
    target.write_text(text.replace(old, new))
    try:
        rc, tail = run(argv)
    finally:
        target.write_bytes(original)
    killed = rc != 0
    print(f"{name}: rc={rc} {'KILLED' if killed else 'SURVIVED'} :: {tail}")
    ok &= killed
for name, argv in (("restored-decl", DECL), ("restored-36b", GATE36B)):
    rc, tail = run(argv)
    print(f"{name}: rc={rc} {tail}")
    ok &= rc == 0
assert hashlib.sha256(target.read_bytes()).hexdigest() == digest
print("source restored: sha256", digest)
sys.exit(0 if ok else 1)
