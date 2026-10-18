#!/usr/bin/env python3
"""Seal all public packet files, excluding disposable scratch and the report itself."""
import hashlib,pathlib
p=pathlib.Path(__file__).resolve().parents[1]
report=(p/"REPORT.md").read_text()
assert report.splitlines()[0]=="[R649] POSITIVE - exact head c5afc0a42f200af01dd83e67b579dc3badc42601"
assert report.rstrip().endswith("R649-2 FINISHED")
assert "SKELETON" not in report
files=sorted(f for f in p.rglob("*") if f.is_file() and f.relative_to(p).parts[0]!="scratch" and f.name not in ("REPORT.md","MANIFEST.sha256") and "__pycache__" not in f.parts)
rows=[]
for f in files:
 assert not f.is_symlink(),str(f)
 rows.append(hashlib.sha256(f.read_bytes()).hexdigest()+"  "+f.relative_to(p).as_posix())
(p/"MANIFEST.sha256").write_text("\n".join(rows)+"\n")
for row in rows:
 sha,rel=row.split("  ",1);assert hashlib.sha256((p/rel).read_bytes()).hexdigest()==sha
print(f"Sealed and verified {len(rows)} public files; report complete; scratch excluded.")
