"""Read back the published receipts and require exact local payload equality."""
import base64
import gzip
import hashlib
import json
from pathlib import Path
import re
import subprocess

root = Path(__file__).resolve().parent
parts = []
for number in (5771717445,5771717582):
    result = subprocess.run(["gh","api",f"repos/kebag-logic/milan-fpga/issues/comments/{number}"],
                            check=True,stdout=subprocess.PIPE)
    (root/"public"/f"receipt-comment-{number}.json").write_bytes(result.stdout)
    body = json.loads(result.stdout)["body"]
    parts.append(re.search(r"```text\n(.*?)\n```",body,re.S).group(1))
packed = base64.b64decode("".join(parts))
assert packed == (root/"portable-receipts.json.gz").read_bytes()
payload = json.loads(gzip.decompress(packed))
assert payload["head"] == "0d43ff25d38917e77bb5c3d2ddb6473013cea3ba"
print("Published payload matches local bytes:",hashlib.sha256(packed).hexdigest())
print("Recoverable UTF-8 files:",len(payload["files"]))
result = subprocess.run(["gh","api","repos/kebag-logic/milan-fpga/issues/comments/5771736515"],
                        check=True,stdout=subprocess.PIPE)
(root/"public"/"author-measurement.json").write_bytes(result.stdout)
comment = json.loads(result.stdout)
assert comment["body"].strip() == (root/"PUBLISH-MEASUREMENT.md").read_text().strip()
(root/"public"/"author-measurement-url.txt").write_text(comment["html_url"]+"\n")
print("Published measurement matches saved summary:",comment["html_url"])
