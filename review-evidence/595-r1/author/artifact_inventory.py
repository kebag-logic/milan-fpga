"""Build every configuration; record bytes without changing tracked output."""
from pathlib import Path
import hashlib
import json
import sys

ROOT = Path("$LANES/595-yaml-int-refusal")
sys.path.insert(0, str(ROOT / "sw/builder"))
import endstation_builder as eb

phase, scratch = sys.argv[1], Path(sys.argv[2])
rows = []
for source in sorted((ROOT / "configs").glob("endstation_*.yaml")):
    art = eb._derive_artifacts(source)
    directory, _ = eb._write_artifact_dir(art, scratch / phase)
    (directory / f"sweep_opts_{art.cfg['board_target']}.sh").write_text(art.sweep)
    for name, content in eb._entity_model_image(art.cfg, art.overlay).items():
        (directory / name).write_bytes(content if isinstance(content, bytes) else content.encode())
    for path in [source, *sorted(directory.iterdir())]:
        data = path.read_bytes()
        rel = str(source.relative_to(ROOT)) if path == source else str(path.relative_to(scratch / phase))
        rows.append(dict(path=rel, size=len(data), sha256=hashlib.sha256(data).hexdigest()))
        if phase == "after" and path != source:
            before = scratch / "before" / path.relative_to(scratch / phase)
            assert data == before.read_bytes(), f"artifact byte drift: {rel}"
result = Path(__file__).with_name(f"artifacts-{phase}.json")
result.write_text(json.dumps(rows, indent=2) + "\n")
if phase == "after":
    assert rows == json.loads(result.with_name("artifacts-before.json").read_text())
print(f"{phase}: {len(rows)} hashes (five configurations and {len(rows)-5} artifacts)")
