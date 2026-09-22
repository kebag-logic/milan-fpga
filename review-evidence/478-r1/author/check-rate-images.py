from pathlib import Path
import hashlib
import json
import sys
sys.path.insert(0, str(Path.cwd() / "sw/builder"))
import test_builder as tb
out = Path(__file__).resolve().parent
rows = {}
for name, path in tb.CONFIGS.items():
    cfg = tb.eb.load_config(path)
    blob = tb.eb._entity_model_image(cfg, tb.eb.emit_aem_overlay(cfg))["aem_desc.bin"]
    desc = tb.image_descriptor(blob, 2)
    offset = int.from_bytes(desc[140:142], "big")
    count = int.from_bytes(desc[142:144], "big")
    rates = [int.from_bytes(desc[offset+4*k:offset+4*k+4], "big") for k in range(count)]
    rows[name] = dict(rates=rates, offset=offset, count=count, image_sha256=hashlib.sha256(blob).hexdigest(), config_sha256=hashlib.sha256(path.read_bytes()).hexdigest())
assert rows == json.loads((out / "baseline-rates.json").read_text()), "shipping image or config changed"
(out / "after-rates.json").write_text(json.dumps(rows, indent=2) + "\n")
print("PASS: all five config and packed AEM-image SHA-256 values match pre-edit base")
for name, row in rows.items():
    print(name, row["rates"], row["image_sha256"])
