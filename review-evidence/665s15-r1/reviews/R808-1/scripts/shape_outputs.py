#!/usr/bin/env python3
"""Hash every generated output of each existing shape with a tree's own generators.

usage: python3 -I shape_outputs.py TREE OUT.json [CONFIG_STEM ...]

For each config: every file the tree's end-station builder writes into a scratch
directory (build(), the tree's own function), the firmware's three entity headers
from the tree's own generators, the mailbox contract's two-interface variant, and,
with --with-shape-variant, nothing else. The tree is a clean clone; the builder's
per-config include copy lands in the tree and is checked by `git status` after.
"""
import hashlib
import json
import subprocess
import sys
import tempfile
from pathlib import Path

tree = Path(sys.argv[1]).resolve()
out_json = Path(sys.argv[2])
stems = sys.argv[3:] or ["endstation_arty_4x4", "endstation_arty_8ch", "endstation_arty_current",
                         "endstation_ax7101_1x1_tdm8", "endstation_ax7101_8x8"]
sys.path.insert(0, str(tree / "sw/builder"))
sys.path.insert(0, str(tree / "sw/mailbox"))
import endstation_builder as eb  # noqa: E402
import gen_mailbox  # noqa: E402

result = {}
with tempfile.TemporaryDirectory(prefix="r808-shape-") as tmp:
    root = Path(tmp)
    for stem in stems:
        config = tree / "configs" / f"{stem}.yaml"
        files = {}
        r = eb.build(str(config), str(root / stem / "builder"))
        for label, written in sorted(r["paths"].items()):
            p = Path(written)
            if p.is_file():
                files[f"builder:{label}:{p.name}"] = p.read_bytes()
        for sub in sorted((root / stem / "builder").rglob("*")):
            if sub.is_file():
                files[f"builder-dir:{sub.relative_to(root / stem / 'builder')}"] = sub.read_bytes()
        for tag, gen in (("adp_entity_gen.h", "sw/firmware/ctrl/adp/adp_entity.py"),
                         ("srp_entity_gen.h", "sw/firmware/ctrl/srp/srp_entity.py"),
                         ("aecp_entity_gen.h", "sw/firmware/ctrl/aecp/aecp_entity.py")):
            target = root / stem / tag
            subprocess.run([sys.executable, "-B", str(tree / gen), str(config), "-o", str(target)],
                           check=True, cwd=tree, capture_output=True)
            files[f"firmware:{tag}"] = target.read_bytes()
        result[stem] = {k: hashlib.sha256(v).hexdigest() for k, v in sorted(files.items())}
    findings = gen_mailbox.write_variant(gen_mailbox.load(), 2, root / "if2")
    assert not findings, findings
    result["mailbox-if2"] = {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
                             for p in sorted((root / "if2").iterdir())}
status = subprocess.run(["git", "-C", str(tree), "status", "--porcelain", "--untracked-files=all"],
                        capture_output=True, text=True, check=True).stdout
result["_tree_status_after"] = status.splitlines()
result["_head"] = subprocess.run(["git", "-C", str(tree), "rev-parse", "HEAD"], capture_output=True,
                                 text=True, check=True).stdout.strip()
out_json.write_text(json.dumps(result, indent=1, sort_keys=True) + "\n")
print(f"{result['_head']}: {sum(len(v) for k, v in result.items() if not k.startswith('_'))} outputs; "
      f"tree status after: {len(status.splitlines())} lines")
