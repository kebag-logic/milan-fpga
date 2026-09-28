#!/usr/bin/env python3
"""Apply one source mutant per copy of the reviewed tree and run the
declaration suite. Usage: mutants.py <pristine-tree> <scratch-dir>.
Each mutant must match its anchor exactly once; a KILLED mutant is one whose
suite exits nonzero. The first assertion/traceback line is recorded."""
import shutil, subprocess, sys
from pathlib import Path

SRC = "sw/builder/endstation_builder.py"
MUTANTS = {
    # rule 1: the historical str() reread of YAML integers in _mac48
    "M1_mac48_str_reread": [(
        '    if not isinstance(v, str):\n        raise ConfigError(f"{ctx}: quote the hexadecimal value as a YAML string")\n    s = v.replace(":", "")',
        '    s = str(v).replace(":", "")')],
    # rule 1 variant: _mac48 accepts integers at face value
    "M2_mac48_int_face_value": [(
        '    if not isinstance(v, str):\n        raise ConfigError(f"{ctx}: quote the hexadecimal value as a YAML string")\n    s = v.replace(":", "")',
        '    if isinstance(v, int) and not isinstance(v, bool):\n        v = f"{v:x}"\n    if not isinstance(v, str):\n        raise ConfigError(f"{ctx}: quote the hexadecimal value as a YAML string")\n    s = v.replace(":", "")')],
    # rule 1: explicit null mac treated as omitted again
    "M3_mac_null_is_missing": [(
        '    if "mac_address" not in raw:', '    if p["mac_address"] is None:')],
    # rule 1: dash spelling loses its meaning
    "M4_mac_dash_dropped": [(
        's = v.replace(":", "").replace("-", "").replace("_", "")',
        's = v.replace(":", "").replace("_", "")')],
    # rule 2: historical integer acceptance in _declared_uint
    "M5_declared_uint_int_accept": [(
        '    """An unsigned quoted hex field, refused outside `bits` bits."""\n    if not isinstance(v, str):\n        raise ConfigError(f"{ctx}: quote the hexadecimal value as a YAML string")\n    try:\n        n = int(v, 16)',
        '    """An unsigned quoted hex field, refused outside `bits` bits."""\n    if isinstance(v, bool) or not isinstance(v, (int, str)):\n        raise ConfigError(f"{ctx}: {v!r} is not an integer")\n    try:\n        n = v if isinstance(v, int) else int(v, 16)')],
    # rule 2 variant: _declared_uint rereads str(v) as hex
    "M6_declared_uint_str_reread": [(
        '    """An unsigned quoted hex field, refused outside `bits` bits."""\n    if not isinstance(v, str):\n        raise ConfigError(f"{ctx}: quote the hexadecimal value as a YAML string")\n    try:\n        n = int(v, 16)',
        '    """An unsigned quoted hex field, refused outside `bits` bits."""\n    if isinstance(v, bool) or v is None:\n        raise ConfigError(f"{ctx}: quote the hexadecimal value as a YAML string")\n    try:\n        n = int(str(v), 16)')],
    # rule 2: explicit null vendor_oui/entity_capabilities defaulted again
    "M7_oui_null_default": [(
        '    if "vendor_oui" not in ent:', '    if ent.get("vendor_oui") is None:')],
    "M8_caps_null_skip": [(
        '    if "entity_capabilities" not in ent:', '    if ent.get("entity_capabilities") is None:')],
    # rule 3: scalar formats (historical code)
    "M9_formats_scalar_historical": [(
        '        fmts = s.get("formats", [])\n        if not isinstance(fmts, list):\n            raise ConfigError(f"{sctx}.formats: must be a list of quoted hexadecimal strings")\n        fmts = fmts or [f"0x{aaf_pcm32(ch, rate_hz):016X}"]',
        '        fmts = s.get("formats") or [f"0x{aaf_pcm32(ch, rate_hz):016X}"]')],
    # rule 3 variant: only str refused
    "M10_formats_only_str_refused": [(
        '        if not isinstance(fmts, list):', '        if isinstance(fmts, str):')],
    # rule 3 variant: falsy non-lists default before the type check
    "M11_formats_falsy_default": [(
        '        fmts = s.get("formats", [])', '        fmts = s.get("formats") or []')],
    # rule 3 variant: tuples/other sequences accepted (list-or-sequence)
    "M12_formats_any_iterable": [(
        '        if not isinstance(fmts, list):', '        if not hasattr(fmts, "__iter__") or isinstance(fmts, str):')],
}

def main():
    pristine, scratch = Path(sys.argv[1]), Path(sys.argv[2])
    names = sys.argv[3:] or list(MUTANTS)
    for name in names:
        tree = scratch / name
        if tree.exists():
            shutil.rmtree(tree)
        shutil.copytree(pristine, tree, symlinks=True)
        f = tree / SRC
        text = f.read_text()
        for old, new in MUTANTS[name]:
            assert text.count(old) == 1, (name, text.count(old))
            text = text.replace(old, new)
        f.write_text(text)
        r = subprocess.run([sys.executable, "-B", "test_declarations.py"], cwd=tree / "sw/builder",
                           capture_output=True, text=True, timeout=900)
        err = [l for l in (r.stderr or "").splitlines() if l.strip()]
        tail = err[-1] if err else ""
        frame = [l.strip() for l in err if l.strip().startswith('File "') and "test_declarations.py" in l]
        where = frame[-1] if frame else ""
        verdict = "KILLED" if r.returncode else "SURVIVED"
        print(f"{name}\t{verdict}\trc={r.returncode}\t{where}\t{tail[:300]}", flush=True)
        shutil.rmtree(tree)

if __name__ == "__main__":
    main()
