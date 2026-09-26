#!/usr/bin/env python3
"""Reviewer probe: regenerate each tracked image through the three documented
CLIs, then repeat arty_4x4 in a disposable copy whose IDENTIFY reset_time
literal is edited on disk (a different mutation route from the audit's
in-memory patch).

Usage: cli_identity_probe.py <clean-tree> <mutant-tree> <work-dir> <audit-receipt.json>
The mutant tree must be a disposable copy; this script edits one file in it.
"""
import hashlib
import json
import struct
import subprocess
import sys
from pathlib import Path


def entity_model_id(blob: bytes) -> str:
    """Locate ENTITY(0,0) through the image's index map, not through the builder."""
    assert blob[:4] == b"AEMI"
    rows, index_off = struct.unpack_from(">H", blob, 8)[0], struct.unpack_from(">I", blob, 12)[0]
    for r in range(rows):
        cfg, dtype, count, length, base, _name, _stride = struct.unpack_from(">HHHHIHH", blob, index_off + 16 * r)
        if dtype == 0:
            body = blob[base:base + length]
            assert struct.unpack_from(">HH", body, 0) == (0, 0)
            return f"0x{int.from_bytes(body[12:20], 'big'):016X}"
    raise SystemExit("no ENTITY row")


def generate(tree: Path, work: Path, stem: str, log) -> bytes:
    """Run builder, store generator and image join CLIs for one config."""
    build = work / stem
    overlay = build / stem / "aem_overlay.json"
    image = work / f"{stem}.bin"
    for cmd in (
        [sys.executable, "-B", "sw/builder/endstation_builder.py", f"configs/{stem}.yaml", "-o", str(build)],
        [sys.executable, "-B", "avdecc/gen_aem_store.py", "--overlay", str(overlay), "--out-dir", str(work / f"{stem}-store")],
        [sys.executable, "-B", "avdecc/gen_aemi_image.py", "--overlay", str(overlay), "-o", str(image),
         "-m", str(image.with_suffix(".map")), "--json", str(image.with_suffix(".json"))],
    ):
        log.write(json.dumps([str(tree.name)] + cmd[1:]) + "\n")
        log.flush()
        subprocess.run(cmd, cwd=tree, check=True, stdout=log, stderr=subprocess.STDOUT, timeout=3600)
    return image.read_bytes()


def main() -> None:
    clean, mutant, work, receipt = (Path(a) for a in sys.argv[1:5])
    audit = json.loads(receipt.read_text())
    out = {"cli": [], "identity": {}}
    work.mkdir(parents=True, exist_ok=True)
    with (work / "cli.log").open("w") as log:
        for item in audit["configurations"]:
            stem = Path(item["config"]).stem
            blob = generate(clean, work / "clean", stem, log)
            digest = hashlib.sha256(blob).hexdigest()
            out["cli"].append(dict(config=stem, bytes=len(blob), sha256=digest,
                                   matches_audit=digest == item["sha256"] and len(blob) == item["image_bytes"],
                                   model_id=entity_model_id(blob)))
        src = mutant / "avdecc" / "aem_descriptors.py"
        text = src.read_text()
        old = "    b += be32(0)                        # reset_time (no automatic reset)\n"
        assert text.count(old) == 1
        src.write_text(text.replace(old, "    b += be32(3)                        # reset_time (reviewer probe)\n"))
        before = generate(clean, work / "clean-id", "endstation_arty_4x4", log)
        after = generate(mutant, work / "mutant", "endstation_arty_4x4", log)
    out["identity"] = dict(
        before_sha256=hashlib.sha256(before).hexdigest(), after_sha256=hashlib.sha256(after).hexdigest(),
        before_model_id=entity_model_id(before), after_model_id=entity_model_id(after),
        changed_offsets=[i for i, (a, b) in enumerate(zip(before, after)) if a != b],
        same_length=len(before) == len(after),
        changed_value_after=int.from_bytes(after[6741 - 3:6741 + 1], "big") if len(after) > 6741 else None)
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
