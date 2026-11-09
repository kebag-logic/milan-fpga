#!/usr/bin/env python3
"""Digest every generated output of every config a tree's base ships (configs/endstation_*.yaml given on argv),
through that tree's own builder and generators: builder outputs, the three firmware entity headers, and the
mailbox variants at 1, 2 interfaces. Usage: shape_digests.py TREE OUT.json CONFIG_STEM..."""
import hashlib, json, subprocess, sys, tempfile
from pathlib import Path
tree = Path(sys.argv[1]).resolve(); out = Path(sys.argv[2]); stems = sys.argv[3:]
sys.path[:0] = [str(tree / "sw/builder"), str(tree / "sw/mailbox")]
import endstation_builder as eb
import gen_mailbox
res = {}
with tempfile.TemporaryDirectory() as tmp:
    root = Path(tmp)
    for stem in stems:
        cfg = tree / "configs" / f"{stem}.yaml"
        files = {}
        r = eb.build(str(cfg), str(root / stem / "b"))
        for label, written in sorted(r["paths"].items()):
            p = Path(written)
            if p.is_file():
                files[f"builder:{label}"] = p.read_bytes()
        argv = eb.emit_soc_argv(eb.load_config(str(cfg)))
        files["builder:argv"] = " ".join(argv).encode()
        for tag, gen in (("adp", "sw/firmware/ctrl/adp/adp_entity.py"), ("srp", "sw/firmware/ctrl/srp/srp_entity.py"),
                         ("aecp", "sw/firmware/ctrl/aecp/aecp_entity.py")):
            t = root / stem / f"{tag}_entity_gen.h"
            subprocess.run([sys.executable, "-B", str(tree / gen), str(cfg), "-o", str(t)], check=True, cwd=tree,
                           capture_output=True)
            files[f"firmware:{tag}_entity_gen.h"] = t.read_bytes()
        res[stem] = {k: hashlib.sha256(v).hexdigest() for k, v in sorted(files.items())}
    for n in (1, 2):
        d = root / f"if{n}"
        f = gen_mailbox.write_variant(gen_mailbox.load(), n, d)
        res[f"mailbox-if{n}"] = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(d.iterdir())}
        res[f"mailbox-if{n}"]["findings"] = str(f)
out.write_text(json.dumps(res, indent=1, sort_keys=True) + "\n")
print(out, sum(len(v) for v in res.values()), "digests")
