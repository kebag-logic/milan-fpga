"""Publishable portable JSON bundle of synthetic observations and instruments."""
import base64
import gzip
import hashlib
import json
from pathlib import Path
import textwrap

root = Path(__file__).resolve().parent
names = ["measure.py", "mutations.py", "e2e.py", "perpage.py", "compare_pages.py", "scope_guard.py",
         "MEASUREMENT.md", "fixtures.json", "renderer-index.json", "sweep-base.json", "sweep-head.json",
         "comparisons.json", "comparisons.tsv", "summary.json", "e2e-fixtures.json", "e2e-renderer.json",
         "e2e-base.json", "e2e-head.json", "e2e-cli-base.log", "e2e-cli-head.log", "perpage-summary.json",
         "perpage-record-hashes.json", "scope-guard.json"]
names += [str(p.relative_to(root)) for p in sorted((root/"renderer").glob("*/*"))]
names += [str(p.relative_to(root)) for p in sorted((root/"sensitivity").glob("*"))]
files = {name: (root/name).read_bytes().decode("utf-8") for name in names}
for entry in (root/"renderer").iterdir():
    receipt = json.loads((entry/"receipt.json").read_text())
    for name, key in [("fixture.txt","source_sha256"),("request.json","request_sha256"),("response.html","html_sha256")]:
        assert hashlib.sha256((entry/name).read_bytes()).hexdigest() == receipt[key], (entry,name)
payload = dict(format="I440 portable receipts v1", base="b17580b91deb11f3441dfc5d7f9fafe539d929b8",
               head="0d43ff25d38917e77bb5c3d2ddb6473013cea3ba", files=files)
raw = json.dumps(payload, ensure_ascii=True, separators=(",", ":")).encode()
packed = gzip.compress(raw, mtime=0)
(root/"portable-receipts.json.gz").write_bytes(packed)
digest = hashlib.sha256(packed).hexdigest()
encoded = base64.b64encode(packed).decode()
comment = ("[A158] PORTABLE RENDERER / SENSITIVITY RECEIPTS\n\n"
           "Head `0d43ff25d38917e77bb5c3d2ddb6473013cea3ba`, base `b17580b91deb11f3441dfc5d7f9fafe539d929b8`. "
           "The payload preserves all 205 sweep fixtures and 18 exact end-to-end page fixtures, GitHub gfm HTML, "
           "request/response hashes and timestamps, every base/head row, eleven mutation patches and results, "
           "per-page comparison hashes, the measurement report and portable Python instruments. "
           "The historical instrument was not publicly available; this reconstructs the population documented by R85-8/R86-9.\n\n"
           "Decode the following fence as base64, then decompress gzip. The result is UTF-8 JSON with "
           "`format`, `base`, `head` and `files` (relative filename to exact UTF-8 content). "
           "Synthetic fixtures and outputs are evidence data, kept outside tracked Markdown. "
           "Only synthetic text was sent to the rendering endpoint.\n\n"
           f"Compressed SHA-256: `{digest}`; {len(packed)} bytes; {len(files)} files.\n\n"
           "```text\n"+"\n".join(textwrap.wrap(encoded,120))+"\n```\n")
(root/"PUBLISH-RECEIPTS.md").write_text(comment)
chunks = [encoded[i:i+60000] for i in range(0,len(encoded),60000)]
for index, chunk in enumerate(chunks,1):
    header = (f"[A158] PORTABLE RECEIPTS {index}/{len(chunks)}\n\n"
              "Head `0d43ff25d38917e77bb5c3d2ddb6473013cea3ba`. "
              "Concatenate the base64 fences from all numbered parts before decoding and decompressing gzip. "
              "The UTF-8 JSON contains exact synthetic fixtures, GitHub gfm HTML and request/response receipts, "
              "base/head rows, sensitivity patches/results, per-page hashes, a report and portable instruments. "
              "The original historical instrument was not publicly available; the documented population was reconstructed. "
              "Only synthetic text was sent to the renderer.\n\n"
              f"Complete compressed SHA-256: `{digest}`; {len(packed)} bytes; {len(files)} files.\n\n")
    body = header+"```text\n"+"\n".join(textwrap.wrap(chunk,120))+"\n```\n"
    assert len(body) < 65000
    (root/f"PUBLISH-RECEIPTS-{index}.md").write_text(body)
assert gzip.decompress(base64.b64decode(encoded)) == raw
print(f"Verified {len(files)} files, {len(packed)} compressed bytes, {len(chunks)} comment parts, SHA-256 {digest}")
