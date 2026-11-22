#!/usr/bin/env python3
"""Recompress each re-encoded operand's decompressed content under candidate encodings and report whether any
reproduces the round-2 file hash recorded in binding.json (a byte preimage of the round-2 file)."""
import gzip, hashlib, json, lzma, subprocess, sys, zlib, io
from pathlib import Path
root = Path(sys.argv[1])
b = json.loads((root / "binding.json").read_text())
for e in b["reencoded"]:
    p = root / e["path"]
    raw = p.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == e["sha256"], p
    content = gzip.decompress(raw) if p.suffix == ".gz" else lzma.decompress(raw)
    ch = hashlib.sha256(content).hexdigest()
    print(f"{e['path']}: file {e['sha256'][:8]} ok; content {ch[:8]} {'==' if ch == e['content_sha256'] else '!='} binding {e['content_sha256'][:8]}; {len(content)} B")
    hits = []
    if p.suffix == ".gz":
        for lvl in range(1, 10):
            for mt in (0,):
                buf = io.BytesIO()
                with gzip.GzipFile(filename="", mode="wb", compresslevel=lvl, fileobj=buf, mtime=mt) as f:
                    f.write(content)
                if hashlib.sha256(buf.getvalue()).hexdigest() == e["round2_sha256"]:
                    hits.append(f"python gzip level {lvl} mtime 0")
            for flag in ("-n",):
                r = subprocess.run(["gzip", f"-{lvl}", flag, "-c"], input=content, capture_output=True)
                if hashlib.sha256(r.stdout).hexdigest() == e["round2_sha256"]:
                    hits.append(f"gzip -{lvl} {flag}")
    else:
        for preset in list(range(0, 10)) + [x | lzma.PRESET_EXTREME for x in range(0, 10)]:
            for chk in (lzma.CHECK_CRC64, lzma.CHECK_CRC32, lzma.CHECK_SHA256):
                out = lzma.compress(content, preset=preset, check=chk)
                if hashlib.sha256(out).hexdigest() == e["round2_sha256"]:
                    hits.append(f"lzma preset {preset & 0xff}{'e' if preset & lzma.PRESET_EXTREME else ''} check {chk}")
                if hashlib.sha256(out).hexdigest() == e["sha256"] and chk == lzma.CHECK_CRC64:
                    print(f"   (round-3 bytes reproduce at preset {preset & 0xff}{'e' if preset & lzma.PRESET_EXTREME else ''})")
    print("   round-2 bytes reproduced by: " + (", ".join(hits) if hits else "NONE of the candidates"))
