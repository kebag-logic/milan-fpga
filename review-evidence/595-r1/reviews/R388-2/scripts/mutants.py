#!/usr/bin/env python3
"""Apply one source mutant at a time to a disposable head copy, run the
declaration suite, record rc and the first failing assertion, then restore.
Usage: mutants.py <disposable-head-tree>"""
import subprocess, sys
from pathlib import Path
tree = Path(sys.argv[1]).resolve()
src = tree / "sw/builder/endstation_builder.py"
orig = src.read_bytes()
G_MAC = ('    if not isinstance(v, str):\n        raise ConfigError(f"{ctx}: quote the hexadecimal value as a YAML string")\n'
         '    s = v.replace(":", "").replace("-", "").replace("_", "")\n')
G_UINT = ('    """An unsigned quoted hex field, refused outside `bits` bits."""\n    if not isinstance(v, str):\n        raise ConfigError(f"{ctx}: quote the hexadecimal value as a YAML string")\n'
          '    try:\n        n = int(v, 16)\n')
FMT = ('        fmts = s.get("formats", [])\n        if not isinstance(fmts, list):\n'
       '            raise ConfigError(f"{sctx}.formats: must be a list of quoted hexadecimal strings")\n'
       '        fmts = fmts or [f"0x{aaf_pcm32(ch, rate_hz):016X}"]\n')
MUTANTS = {
    "M1 mac int(str(v),16) reread (pre-PR)":
        (G_MAC, '    s = str(v).replace(":", "").replace("-", "").replace("_", "")\n'),
    "M2 mac bool-only refusal then str(v) reread":
        (G_MAC, '    if isinstance(v, bool) or v is None:\n        raise ConfigError(f"{ctx}: quote the hexadecimal value as a YAML string")\n'
                '    s = str(v).replace(":", "").replace("-", "").replace("_", "")\n'),
    "M3 mac accepts ints at face value":
        (G_MAC, '    if isinstance(v, int) and not isinstance(v, bool):\n        v = f"{v:x}"\n'
                '    if not isinstance(v, str):\n        raise ConfigError(f"{ctx}: quote the hexadecimal value as a YAML string")\n'
                '    s = v.replace(":", "").replace("-", "").replace("_", "")\n'),
    "M4 mac drops dash separator":
        ('    s = v.replace(":", "").replace("-", "").replace("_", "")\n', '    s = v.replace(":", "").replace("_", "")\n'),
    "M5 uint integer acceptance (pre-PR)":
        (G_UINT, '    """mutant"""\n    if isinstance(v, bool) or not isinstance(v, (int, str)):\n        raise ConfigError(f"{ctx}: {v!r} is not an integer")\n'
                 '    try:\n        n = v if isinstance(v, int) else int(v, 16)\n'),
    "M6 uint int(str(v),16) reread":
        (G_UINT, '    """mutant"""\n    if isinstance(v, bool) or v is None:\n        raise ConfigError(f"{ctx}: quote the hexadecimal value as a YAML string")\n'
                 '    try:\n        n = int(str(v), 16)\n'),
    "M7 formats scalar accepted (pre-PR)":
        (FMT, '        fmts = s.get("formats") or [f"0x{aaf_pcm32(ch, rate_hz):016X}"]\n'),
    "M8 formats falsy scalars default":
        (FMT, '        fmts = s.get("formats") or []\n        if not isinstance(fmts, list):\n'
              '            raise ConfigError(f"{sctx}.formats: must be a list of quoted hexadecimal strings")\n'
              '        fmts = fmts or [f"0x{aaf_pcm32(ch, rate_hz):016X}"]\n'),
    "M9 formats str wrapped into a list":
        (FMT, '        fmts = s.get("formats", [])\n        if isinstance(fmts, str):\n            fmts = [fmts]\n'
              '        if not isinstance(fmts, list):\n'
              '            raise ConfigError(f"{sctx}.formats: must be a list of quoted hexadecimal strings")\n'
              '        fmts = fmts or [f"0x{aaf_pcm32(ch, rate_hz):016X}"]\n'),
    "M10 platform null mac -> required (pre-PR presence test)":
        ('    if "mac_address" not in raw:\n', '    if p["mac_address"] is None:\n'),
    "M11 vendor_oui null -> default (pre-PR presence test)":
        ('    if "vendor_oui" not in ent:\n', '    if ent.get("vendor_oui") is None:\n'),
    "M12 entity_capabilities null -> skipped (pre-PR presence test)":
        ('    if "entity_capabilities" not in ent:\n', '    if ent.get("entity_capabilities") is None:\n'),
    "M13 capabilities call-site str() coercion":
        ('_declared_uint(ent["entity_capabilities"], 32,', '_declared_uint(str(ent["entity_capabilities"]), 32,'),
    "M14 vendor_oui call-site str() coercion":
        ('_declared_uint(ent["vendor_oui"], 24,', '_declared_uint(str(ent["vendor_oui"]), 24,'),
}
def run(label):
    r = subprocess.run([sys.executable, "sw/builder/test_declarations.py"], cwd=tree,
                       capture_output=True, text=True, timeout=900)
    out = (r.stdout + r.stderr).strip().splitlines()
    tail = [l for l in out if "Error" in l or l.startswith("  File") and "test_declarations" in l]
    return r.returncode, tail[-3:] if tail else out[-2:]
try:
    rc, _ = run("control")
    print(f"CONTROL (unmutated head copy): rc={rc}")
    for name, (old, new) in MUTANTS.items():
        text = orig.decode()
        assert text.count(old) == 1, (name, text.count(old))
        src.write_bytes(text.replace(old, new).encode())
        rc, tail = run(name)
        print(f"{'KILLED' if rc else 'SURVIVED'} rc={rc} {name}")
        for l in tail:
            print(f"    {l.strip()[:300]}")
        src.write_bytes(orig)
    rc, _ = run("restored")
    print(f"RESTORED CONTROL: rc={rc}")
finally:
    src.write_bytes(orig)
