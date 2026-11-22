#!/usr/bin/env python3
"""build3.py ROUND2_PACKET OUT HEAD REBUILT: round 3's identity packet, from round 2's (its operands unchanged):

  * every compressed operand whose bytes the publication's privacy scrub would alter is re-encoded (the same
    compressor, another level) until the scrub leaves its bytes unchanged; its decompressed content must equal the
    round-2 file's, and binding.json `reencoded` records the round-2 file hash, the new file hash and the content
    hash side by side;
  * the tools are this round's (replay, rmutants, seal, this builder, the publication check);
  * the harness rebuild at HEAD (REBUILT, a scratch tree of hbuild2.sh) and the input carry at HEAD are added to
    receipts/, and binding.json's rebuild rows name HEAD when its images equal the recorded ones;
  * every text file is checked to pass the scrub unchanged too.
The manifests are written by seal.py afterwards."""
import gzip
import hashlib
import json
import lzma
import shutil
import sys
from pathlib import Path

sys.path.insert(0, "<home>/milan-fpga-management/2026-09-23")
import privacy  # noqa: E402  the publication's scrub

SRC, OUT, HEAD, REBUILT = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3], Path(sys.argv[4])
S = Path("<scratch>")
SANITISE = (("<train-scratch>", "<train-scratch>"), (str(S), "<scratch>"),
            ("<lane>", "<lane>"), ("<home>", "<home>"), ("<host-tools>", "<host-tools>"),
            ("<host-tmp>", "<host-tmp>"), ("<host-data>", "<host-data>"))


def sha(data):
    return hashlib.sha256(data).hexdigest()


def stable(data):
    return privacy.scrub_redact(data) == data


def decode(path):
    data = path.read_bytes()
    return lzma.decompress(data) if path.suffix == ".xz" else gzip.decompress(data)


def encodings(suffix):
    if suffix == ".xz":
        return [(f"xz preset {k}", lambda c, k=k: lzma.compress(c, preset=k)) for k in (6, 9, 8, 7, 5, 4)]
    return [(f"gzip level {k} (mtime 0)", lambda c, k=k: gzip.compress(c, compresslevel=k, mtime=0))
            for k in (9, 8, 7, 6, 5, 4)]


if OUT.exists():
    shutil.rmtree(OUT)
shutil.copytree(SRC, OUT)
for name in ("replay-output.txt", "plants.txt", "MANIFEST.sha256", "MANIFEST.content.sha256"):
    (OUT / name).unlink(missing_ok=True)
binding = json.loads((OUT / "binding.json").read_text())
binding["reencoded"] = []
for path in sorted(p for p in OUT.rglob("*") if p.is_file() and p.suffix in (".xz", ".gz")):
    old = path.read_bytes()
    if stable(old):
        continue
    body = decode(path)
    for label, encode in encodings(path.suffix):
        new = encode(body)
        if stable(new):
            assert (lzma.decompress(new) if path.suffix == ".xz" else gzip.decompress(new)) == body
            path.write_bytes(new)
            binding["reencoded"].append({"path": str(path.relative_to(OUT)), "round2_sha256": sha(old),
                                         "sha256": sha(new), "content_sha256": sha(body), "encoding": label,
                                         "why": "the round-2 bytes match a publication scrub pattern by chance, so "
                                                "the archive left the file out; the content is unchanged"})
            print(f"re-encoded {path.relative_to(OUT)}: {label}, content {sha(body)[:16]}")
            break
    else:
        raise SystemExit(f"no scrub-stable encoding for {path}")

# tools of this round
for name in ("replay.py", "rmutants.py", "seal.py", "build3.py", "publish_check.py"):
    text = (S / "bin" / name).read_text()
    for a, b in SANITISE:
        text = text.replace(a, b)
    (OUT / "tools" / name).write_text(text)

# the harness rebuild and the input carry at HEAD
h10 = HEAD[:10]
for point in ("1x1", "8x8-1if"):
    (OUT / f"receipts/harness-rebuild-{h10}-{point}.txt").write_text((REBUILT / point / "hashes.txt").read_text())
for p in ("1x1", "8x8"):
    text = (S / f"logs2/inputs-carry-{p}-{h10}.txt").read_text()
    for a, b in SANITISE:
        text = text.replace(a, b)
    (OUT / f"receipts/inputs-carry-{p}-{h10}.txt").write_text(text)
moved = 0
for row in binding["rebuilds"]:
    if row["head"].startswith("this head"):
        point, arm = row["operand"].split("/")[1:3]
        rebuilt = sha((REBUILT / point / arm / "image/ctrl_app.elf").read_bytes())
        if rebuilt != row["sha256"]:
            raise SystemExit(f"{row['operand']}: the image rebuilt at {HEAD} differs from the recorded one")
        row["head"] = f"this head {HEAD}"
        moved += 1
print(f"rebuild rows at {HEAD}: {moved}")
(OUT / "binding.json").write_text(json.dumps(binding, indent=1) + "\n")
(OUT / "README.md").write_text((S / "bin/identity-README.md").read_text())

unstable = [str(p.relative_to(OUT)) for p in sorted(OUT.rglob("*")) if p.is_file() and not stable(p.read_bytes())]
print(f"files the scrub would alter: {unstable or 'none'}")
sys.exit(1 if unstable else 0)
