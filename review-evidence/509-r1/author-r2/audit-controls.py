"""Exercise explicit audit refusals and the identity observation control."""
import importlib.util
import json
from pathlib import Path
import struct
import sys
from unittest.mock import patch

root = Path(sys.argv[1])
spec = importlib.util.spec_from_file_location("descriptor_audit", root / "scripts/audit_pp_descriptors.py")
audit = importlib.util.module_from_spec(spec)
spec.loader.exec_module(audit)
path = root / "configs/endstation_arty_4x4.yaml"
cfg = audit.builder.load_config(path)
document, blob = audit.generate(cfg)
audit.packed_rows(blob)
audit.assert_packed_bytes(document, blob)
audit.check_identity_probe(path)
results = [{"probe": "legal image and identity control", "result": "accepted"}]


def refused(label, call):
    try:
        call()
    except audit.AuditError as exc:
        results.append({"probe": label, "result": "refused", "reason": str(exc)})
    else:
        raise RuntimeError(label + " escaped audit refusal")


for label, at, value, width in (
    ("bad magic", 0, 0, 4),
    ("bad version", 4, 2, 2),
    ("wrong image length", 20, len(blob) + 1, 4),
    ("bad header checksum", 28, int.from_bytes(blob[28:32], "big") ^ 1, 4),
):
    mutant = bytearray(blob)
    mutant[at:at + width] = value.to_bytes(width, "big")
    refused(label, lambda: audit.packed_rows(bytes(mutant)))
index = audit.uint(blob, 12, 4)
base = audit.uint(blob, index + 8, 4)
for label, at in (("body type mismatch", base), ("body index mismatch", base + 2)):
    mutant = bytearray(blob)
    mutant[at:at + 2] = (99).to_bytes(2, "big")
    refused(label, lambda: audit.packed_rows(bytes(mutant)))
mutant = bytearray(blob)
mutant[index + 8:index + 12] = (len(blob) - 1).to_bytes(4, "big")
refused("descriptor outside image", lambda: audit.packed_rows(bytes(mutant)))
with patch.object(audit.builder, "_entity_model_image", return_value={"aem_desc.bin": b"wrong"}):
    refused("builder image disagreement", lambda: audit.generate(cfg))
mutant = bytearray(blob)
mutant[base + 12] ^= 1
refused("packer normalizes body bytes", lambda: audit.assert_packed_bytes(document, bytes(mutant)))
original = audit.builder.derive_model_id


def ignoring_changed_field(shape, oui):
    return original({k: v for k, v in shape.items() if k != "audit_identify"}, oui)


with patch.object(audit.builder, "derive_model_id", ignoring_changed_field):
    refused("identity derivation ignores changed field", lambda: audit.check_identity_probe(path))
print(json.dumps({"optimized": sys.flags.optimize, "results": results}, indent=2))
