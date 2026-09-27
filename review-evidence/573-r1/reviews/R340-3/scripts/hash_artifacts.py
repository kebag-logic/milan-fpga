"""Hash every generated builder, AEM store and AEM image artifact of the
five tracked end-station configurations of one source tree.

Usage: python3 hash_artifacts.py <tree root> <output json>
All generation happens in temporary directories; the tree is only read,
except that the builder may refresh its own ignored out/ directory.
"""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(ROOT / "sw/builder"))
import endstation_builder as builder  # noqa: E402


def main() -> None:
    rows = []
    names = subprocess.check_output(
        ["git", "ls-files", "configs/endstation_*.yaml"], cwd=ROOT, text=True).split()
    assert len(names) == 5, names
    for name in names:
        with tempfile.TemporaryDirectory(prefix="r340-artifacts-") as scratch:
            work = Path(scratch)
            result = builder.build(str(ROOT / name), str(work / "builder"))
            built = work / "builder" / Path(name).stem
            overlay = built / "aem_overlay.json"
            store, image = work / "store", work / "image"
            image.mkdir()
            for command in (
                    [sys.executable, str(ROOT / "avdecc/gen_aem_store.py"),
                     "--overlay", str(overlay), "--out-dir", str(store)],
                    [sys.executable, str(ROOT / "avdecc/gen_aemi_image.py"),
                     "--overlay", str(overlay), "-o", str(image / "aem_desc.bin"),
                     "-m", str(image / "aem_desc.map"), "--json", str(image / "aem_desc.json")]):
                subprocess.run(command, check=True, cwd=ROOT, capture_output=True, timeout=600)
            data = {"builder/" + str(p.relative_to(built)): p.read_bytes()
                    for p in built.rglob("*") if p.is_file()}
            data["builder/cfg_adp_shape_svh"] = Path(result["paths"]["cfg_adp_shape_svh"]).read_bytes()
            data["builder/sweep_opts"] = str(result["sweep_opts"]).encode()
            for label, where in (("store", store), ("image", image)):
                data.update({f"{label}/{p.relative_to(where)}": p.read_bytes()
                             for p in where.rglob("*") if p.is_file()})
            for label, blob in sorted(data.items()):
                rows.append(dict(configuration=Path(name).stem, artifact=label,
                                 bytes=len(blob), sha256=hashlib.sha256(blob).hexdigest()))
    Path(sys.argv[2]).write_text(json.dumps(rows, indent=1) + "\n")
    print(f"{ROOT}: {len(rows)} artifacts hashed")


if __name__ == "__main__":
    main()
