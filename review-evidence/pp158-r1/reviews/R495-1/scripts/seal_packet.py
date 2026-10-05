#!/usr/bin/env python3
"""Seal an explicit publication allowlist; preserve raw local logs in scratch."""
import argparse,hashlib,json,pathlib,re
p=argparse.ArgumentParser();p.add_argument("--packet",type=pathlib.Path,required=True);p.add_argument("--source",type=pathlib.Path,required=True);a=p.parse_args();packet=a.packet.resolve()
files=["REPORT.md"]
files += [str(f.relative_to(packet)) for f in sorted((packet/"scripts").glob("*")) if f.is_file()]
names=["red.log","red.rc","controls.log","controls.rc","focused-results.json","planting.json","planting.log","planting.rc","extra-boundaries.log","extra-boundaries.patch","extra-boundaries.rc","docs-focused.log","docs-focused.rc","docs-full.log","docs-full.rc","docs-dependency.log","docs-dependency.rc","simulator-identity.txt","identity-and-area.log","identity-and-area.rc","final-identity.log","final-identity.rc","exact-head.diff","public-HANDOFF.md","public-MANIFEST.json","issue-158.json","issue-158-comments-latest.json","pr-161.json","pr-161-comments-latest.json","pr-reviews.json","pr-review-comments.json","hosted-runs.json","hosted-jobs-37348936371.json","hosted-jobs-37348944062.json","hosted-check-runs-final.json","observation-time.txt","parent-adoption-148.patch","parent-148-apply-check.log","parent-148-apply-check.rc","parent-661.json","parent-dev-tree.json","parent-dev-commit.json"]
files += ["receipts/"+n for n in names]
files += [str(f.relative_to(packet)) for f in sorted((packet/"receipts/controls").glob("*")) if f.is_file()]
provenance=[]
for rel in files:
 path=packet/rel;assert path.is_file(),rel
 if not rel.endswith(".log"):continue
 raw=packet/"scratch/raw-receipts"/rel
 if not raw.exists():raw.parent.mkdir(parents=True,exist_ok=True);raw.write_bytes(path.read_bytes())
 source=raw.read_bytes();text=source.decode()
 text=text.replace(str(packet),"$PACKET").replace(str(a.source.resolve()),"$SOURCE")
 text=re.sub(r"/home/[^/]+/\.local/share/containers/storage/overlay/[0-9a-f]+/diff", "$SCOPED_RUNTIME", text)
 text=text.replace("$VALIDATION_TOOLS/pinned-verilator-5.050/verilator", "$SCOPED_SIMULATOR")
 path.write_text(text)
 provenance.append(dict(file=rel,raw_sha256=hashlib.sha256(source).hexdigest(),published_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),path_normalized=source!=path.read_bytes()))
(packet/"receipts/log-provenance.json").write_text(json.dumps({"policy":"Local path prefixes only; no diagnostics, counts or verdicts removed. Raw originals are in scratch/raw-receipts and not publishable.","logs":provenance},indent=2)+"\n")
files.append("receipts/log-provenance.json")
report=(packet/"REPORT.md").read_text();assert report.startswith("[R495] POSITIVE - exact head 79571006b803a4ab4af65358f0d87bc3af73180e\n");assert report.endswith("R495-1 FINISHED\n");assert "SKELETON" not in report
for f in files:assert not f.startswith("scratch/")
manifest="".join(hashlib.sha256((packet/f).read_bytes()).hexdigest()+"  "+f+"\n" for f in sorted(set(files)))
(packet/"MANIFEST.sha256").write_text(manifest)
print("Sealed",len(set(files)),"publishable files; scratch and setup attempts excluded.")
