"""Every existing shape's generated outputs by SHA-256 (every endstation config but the 32x32 simulation shape),
from ROOT's own builder and generators.

The same inventory as the lane's byte-identity gate (every file the builder writes, the three
entity headers, the 8x8 two-interface mailbox variant), computed from any tree, so a base tree
that does not carry the gate can be compared with the lane's golden. With --placement split,
each config is built from a copy declaring `control: {placement: split}` (S6a's key), the copy
under the same file name in one fixed directory, since the outputs name the config's path.

usage: python3 -I shape_digests.py ROOT OUT.json [--placement split]
"""
import hashlib
import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(sys.argv[1]).resolve()
OUT = Path(sys.argv[2])
SPLIT = sys.argv[3:] == ["--placement", "split"]
sys.path[:0] = [str(ROOT / "sw/builder"), str(ROOT / "sw/mailbox")]
import endstation_builder as eb  # noqa: E402
import gen_mailbox  # noqa: E402

NAMES = tuple(sorted(p.stem.removeprefix("endstation_") for p in (ROOT / "configs").glob("endstation_*.yaml")
                    if p.stem != "endstation_ax7101_32x32"))
out = {"_root_head": subprocess.run(["git", "-C", str(ROOT), "rev-parse", "HEAD"], capture_output=True,
                                    text=True, check=True).stdout.strip(),
       "_placement": "split" if SPLIT else "as tracked"}
with tempfile.TemporaryDirectory(prefix="shape-digests-") as tmp:
    root = Path(tmp)
    for name in NAMES:
        config = ROOT / f"configs/endstation_{name}.yaml"
        if SPLIT:
            fixed = Path("$SCRATCH/split-cfg")  # one path for both trees: the outputs name it
            fixed.mkdir(exist_ok=True)
            copy = fixed / config.name
            copy.write_text(config.read_text() + "\ncontrol:\n  placement: split\n")
            config = copy
        files = {}
        r = eb.build(str(config), str(root / "builder"))
        for label, written in sorted(r["paths"].items()):
            files[f"builder:{label}"] = Path(written).read_bytes()
        entity = root / name
        entity.mkdir()
        for tag, generator in (("adp_entity_gen.h", "sw/firmware/ctrl/adp/adp_entity.py"),
                               ("srp_entity_gen.h", "sw/firmware/ctrl/srp/srp_entity.py"),
                               ("aecp_entity_gen.h", "sw/firmware/ctrl/aecp/aecp_entity.py")):
            subprocess.run([sys.executable, "-B", str(ROOT / generator), str(config), "-o", str(entity / tag)],
                           check=True, cwd=ROOT, capture_output=True)
            files[f"firmware:{tag}"] = (entity / tag).read_bytes()
        if name == "ax7101_8x8":
            findings = gen_mailbox.write_variant(gen_mailbox.load(), 2, entity / "if2")
            assert not findings, findings
            for path in gen_mailbox.VARIANT_OUTPUTS:
                files[f"mailbox-if2:{Path(path).name}"] = (entity / "if2" / Path(path).name).read_bytes()
        out[name] = {label: hashlib.sha256(data).hexdigest() for label, data in sorted(files.items())}
OUT.write_text(json.dumps(out, indent=1) + "\n")
print(f"{OUT.name}: {sum(len(v) for k, v in out.items() if not k.startswith('_'))} outputs from {out['_root_head'][:10]}")
