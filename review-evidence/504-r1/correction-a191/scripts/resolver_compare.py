#!/usr/bin/env python3
"""Compare what two copies of the RV32 resolver report for census assemblies.

Usage: resolver_compare.py <old test_builder.py> <new test_builder.py> <asm>...

Each copy is executed as its own module whose `__file__` is the lane's
sw/builder/test_builder.py (the new copy's path), so both resolve the same
repository root; only the source text differs. For every assembly, the whole-unit
resolution (rv32_unit) is taken with each copy and every function's store,
call and return observations are compared. Prints one line per assembly
and every difference; exit 0 when all agree, 1 otherwise.
"""
import importlib.util
import sys
from pathlib import Path


def load(path: Path, name: str, origin: Path):
    """Execute one resolver copy's text as module `name` at `origin`."""
    spec = importlib.util.spec_from_loader(name, loader=None, origin=str(origin))
    module = importlib.util.module_from_spec(spec)
    module.__file__ = str(origin)
    sys.modules[name] = module
    exec(compile(path.read_text(), str(origin), "exec"), module.__dict__)  # noqa: S102
    return module


def picture(module, text: str) -> dict:
    """Every function's observations, spelled as comparable strings.
    `addresses` is the part rules 1, 1b and 1d read; `stores` adds the
    value each store carries, which no rule reads."""
    unit = module.rv32_unit(text)
    out = {}
    for name, run in sorted(unit["runs"].items()):
        out[name] = {
            "addresses": [f"{at}:{address!r}"
                          for at, (address, _value) in run["stores"]],
            "stores": [f"{at}:{address!r}={value!r}"
                       for at, (address, value) in run["stores"]],
            "calls": [f"{at}:{callee}:{sorted(handed.items())!r}"
                      for at, (callee, handed) in run["calls"]],
            "rets": [f"{at}:{value!r}" for at, value in run["rets"]],
        }
    out["@seeds"] = repr(sorted((k, sorted(v.items()))
                                for k, v in unit["seeds"].items()))
    return out


def main() -> int:
    old_path, new_path = Path(sys.argv[1]), Path(sys.argv[2]).resolve()
    lane = new_path.parents[2]
    sys.path[:0] = [str(lane / "sw/builder"), str(lane / "scripts")]
    old = load(old_path, "tb_old", new_path)
    new = load(new_path, "tb_new", new_path)
    differing = 0
    for asm in sys.argv[3:]:
        text = Path(asm).read_text()
        a, b = picture(old, text), picture(new, text)
        diffs = []
        for name in sorted(set(a) | set(b)):
            if a.get(name) != b.get(name):
                diffs.append(name)
        print(f"{Path(asm).name}: {'SAME' if not diffs else 'DIFFERS in ' + ', '.join(diffs)}")
        parts = {"addresses": [], "stores": [], "calls": [], "rets": []}
        for name in diffs:
            differing += 1
            if name == "@seeds":
                print(f"  seeds old {a[name]}\n  seeds new {b[name]}")
                parts.setdefault("seeds", []).append(name)
                continue
            for part in ("addresses", "stores", "calls", "rets"):
                if a[name][part] != b[name][part]:
                    parts[part].append(name)
                    print(f"  {name} {part}:\n    old {a[name][part]}\n    new {b[name][part]}")
        for part in ("addresses", "calls", "seeds", "stores", "rets"):
            print(f"  {part}: {'identical' if not parts.get(part) else 'differ in ' + ', '.join(parts[part])}")
    return 1 if differing else 0


if __name__ == "__main__":
    sys.exit(main())
