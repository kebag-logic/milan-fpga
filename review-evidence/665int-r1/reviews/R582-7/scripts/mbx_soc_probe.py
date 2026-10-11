#!/usr/bin/env python3
"""mbx_soc_probe.py CLONE CONFIG_YAML OUT_JSON SCRATCH [--ctrl-mailbox]

Build the SoC milan_soc.py describes for one config's own emitted argv (the
argv test_builder.py's _config_argv gives, optionally plus --ctrl-mailbox),
stop it at Builder() so nothing is exported or synthesised, and record what
the composition review needs:

  regions   every bus region (origin, size), and any pair that overlaps
  csr       every CSR bank's location; irq every interrupt's
  arrays    every storage Memory in the SoC's module tree (path, width,
            depth, ram_style, read-port mode): the M2 crossings' split
  mbx       the KL_mbx / KL_mbx_wb Instance ports (name, direction, width,
            tied to a constant)

Run with an interpreter that imports migen, litex and litex_boards.
"""
import contextlib
import io
import json
import logging
import os
import sys
import types

clone, cfg_path, out_json, scratch = (os.path.abspath(a) for a in sys.argv[1:5])
flag = sys.argv[5:]
soc_dir = os.path.join(clone, "sw/litex")
sys.path.insert(0, os.path.join(clone, "sw/builder"))
sys.path.insert(0, soc_dir)
os.chdir(soc_dir)
logging.disable(logging.CRITICAL)

import endstation_builder as eb  # noqa: E402

cfg = eb.load_config(cfg_path)
# milan_soc.py reads the builder's output from sw/builder/out (test_builder's OUT)
eb.build(cfg_path, os.path.join(clone, "sw/builder/out"))
gen = os.path.join(clone, "configs/generated", cfg["name"])
build_out = os.path.join(scratch, "build-out")
os.makedirs(build_out, exist_ok=True)
argv = [build_out if a == "@BUILD_OUT@" else a for a in eb.emit_soc_argv(cfg)]
argv += ["--entity-gen-dir", gen] + flag

soc_path = os.path.join(soc_dir, "milan_soc.py")
mod = types.ModuleType("milan_soc_probe")
mod.__file__ = soc_path
sys.modules[mod.__name__] = mod
exec(compile(open(soc_path).read(), soc_path, "exec"), mod.__dict__)


class _Got(Exception):
    def __init__(self, soc):
        Exception.__init__(self)
        self.soc = soc


def _spy_builder(soc, *a, **k):
    raise _Got(soc)


mod.Builder = _spy_builder
sys.argv = ["milan_soc.py"] + argv
sink = io.StringIO()
try:
    with contextlib.redirect_stdout(sink), contextlib.redirect_stderr(sink):
        mod.main()
    raise SystemExit("main() returned without reaching Builder()")
except _Got as got:
    soc = got.soc

from migen import Memory  # noqa: E402
from migen.fhdl.specials import Instance  # noqa: E402
from migen.fhdl.structure import Constant  # noqa: E402


def walk(m, path, seen):
    if id(m) in seen:
        return
    seen.add(id(m))
    yield path, m
    for name, sub in getattr(m, "_submodules", []):
        yield from walk(sub, f"{path}.{name or type(sub).__name__}", seen)


arrays, instances = [], {}
for path, m in walk(soc, "soc", set()):
    frag = getattr(m, "_fragment", None)
    if frag is None:
        continue
    for s in frag.specials:
        if isinstance(s, Memory):
            attrs = sorted(str(x) for x in (getattr(s, "attr", None) or ()))
            arrays.append({"path": path, "width": s.width, "depth": s.depth,
                           "attr": attrs,
                           "ports": [{"we": p.we is not None, "async": bool(p.async_read),
                                      "mode": int(p.mode), "cd": p.clock.cd} for p in s.ports]})
        if isinstance(s, Instance) and s.of in ("KL_mbx", "KL_mbx_wb"):
            ports = []
            for it in s.items:
                if isinstance(it, (Instance.Input, Instance.Output, Instance.InOut)):
                    ports.append([it.name, type(it).__name__, len(it.expr),
                                  isinstance(it.expr, Constant)])
            instances[s.of] = ports

regions = {n: [r.origin, r.size] for n, r in soc.bus.regions.items()}
overlaps = []
names = sorted(regions)
for i, a in enumerate(names):
    for b in names[i + 1:]:
        oa, sa = regions[a]
        ob, sb = regions[b]
        if oa < ob + sb and ob < oa + sa:
            overlaps.append([a, b])
out = {
    "config": cfg["name"], "argv": argv,
    "has_ctrl_mbx": hasattr(soc, "ctrl_mbx"),
    "has_milan_axil_cdc": hasattr(soc, "milan_axil_cdc"),
    "regions": regions, "overlaps": overlaps,
    "csr": dict(sorted(soc.csr.locs.items())),
    "irq": dict(sorted(soc.irq.locs.items())) if soc.irq.enabled else {},
    "arrays": sorted(arrays, key=lambda a: (a["path"], a["width"])),
    "mbx_instances": instances,
}
with open(out_json, "w") as fh:
    json.dump(out, fh, indent=1, sort_keys=True)
print(json.dumps({k: out[k] for k in ("config", "has_ctrl_mbx", "has_milan_axil_cdc",
                                       "overlaps")}),
      "regions:", len(regions), "csr:", len(out["csr"]), "arrays:", len(arrays),
      "mbx ports:", {k: len(v) for k, v in instances.items()})
