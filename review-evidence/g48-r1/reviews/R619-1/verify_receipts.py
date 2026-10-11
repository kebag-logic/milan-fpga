#!/usr/bin/env python3
"""Verify saved public source and author evidence against their published identities."""
import hashlib
import json
from pathlib import Path


def blob(data):
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()


def main():
    root = Path(__file__).resolve().parent / "receipts"
    parent = json.loads((root / "parent-provenance.json").read_text())
    assert parent["parent"] == "ac2c5e77bba1c0ae20ce2f69f711a1d17ead94a5"
    for entry in parent["files"]:
        data = (root / "authorities" / entry["path"].replace("/", "__")).read_bytes()
        assert blob(data) == entry["sha"]
        assert hashlib.sha256(data).hexdigest() == entry["sha256"]
        print("PASS parent source: " + entry["path"] + " " + entry["sha"])
    evidence = root / "public-evidence"
    tree = {v["path"].split("review-evidence/g48-r1/", 1)[1]: v
            for v in json.loads((root / "evidence-tree.json").read_text())["tree"]
            if v["type"] == "blob"}
    manifest = json.loads((evidence / "MANIFEST.json").read_text())
    count = 0
    for entry in manifest:
        path = evidence / entry["file"]
        if not path.exists():
            assert entry["file"] in {"author/HANDOFF.md", "author/PR-BODY.md", "author/REVIEW-READY.txt"}
            continue
        data = path.read_bytes()
        assert hashlib.sha256(data).hexdigest() == entry["published_sha256"]
        assert blob(data) == tree[entry["file"]]["sha"]
        print("PASS author receipt: " + entry["file"])
        count += 1
    assert count == 22
    assert blob((evidence / "MANIFEST.json").read_bytes()) == tree["MANIFEST.json"]["sha"]
    assert (evidence / "author/validation/head.txt").read_text().strip() == "7cc9c492145dd9e7c5c0e1d4695a261ea8025850"
    results = sorted((evidence / "author/validation").glob("*.rc"))
    assert len(results) == 10
    assert all(path.read_text().strip() == "0" for path in results)
    print("PASS: six parent source files; published manifest and 22 author receipts; ten successful author commands; exact source head")


if __name__ == "__main__":
    main()
