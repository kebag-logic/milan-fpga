"""Render pages through GitHub's Markdown API (POST /markdown, mode gfm) with gh api.

Every exact request and response byte string is cached under render-cache/<request sha256>.{req,resp,meta}.
Usage: python3 record.py pages.json out.json   (pages.json: list of {"page": ...} objects, extra keys kept)
"""
import datetime, hashlib, json, subprocess, sys, time
from pathlib import Path

CACHE = Path(__file__).resolve().parent.parent / "render-cache"
CONTEXT = "kebag-logic/milan-fpga"
import os
MODE = os.environ.get("RENDER_MODE", "gfm")


def request_bytes(page: str) -> bytes:
    body = {"context": CONTEXT, "mode": MODE, "text": page} if MODE == "gfm" else {"mode": MODE, "text": page}
    return json.dumps(body, sort_keys=True,
                      separators=(",", ":"), ensure_ascii=True).encode("ascii")


def render(page: str) -> dict:
    req = request_bytes(page)
    key = hashlib.sha256(req).hexdigest()
    CACHE.mkdir(exist_ok=True)
    rq, rs, meta = CACHE / f"{key}.req", CACHE / f"{key}.resp", CACHE / f"{key}.meta"
    if not rs.exists():
        for attempt in range(8):
            out = subprocess.run(["gh", "api", "--method", "POST", "markdown", "--input", "-"],
                                 input=req, capture_output=True)
            if out.returncode == 0:
                break
            time.sleep(5 * (attempt + 1))
            print("retry", key[:12], out.stderr.decode()[:200], file=sys.stderr)
        else:
            raise SystemExit(f"render failed for {page!r}")
        rq.write_bytes(req)
        rs.write_bytes(out.stdout)
        meta.write_text(json.dumps({"recorded_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")}))
        time.sleep(0.4)
    resp = rs.read_bytes()
    return {"request_bytes": req.decode("ascii"), "request_sha256": key,
            "response_bytes": resp.decode("utf-8"), "response_sha256": hashlib.sha256(resp).hexdigest(),
            "recorded_utc": json.loads(meta.read_text())["recorded_utc"]}


if __name__ == "__main__":
    pages = json.loads(Path(sys.argv[1]).read_text())
    out = []
    for i, item in enumerate(pages):
        out.append(dict(item, **render(item["page"])))
        if i % 25 == 0:
            print(i, len(pages), file=sys.stderr)
    Path(sys.argv[2]).write_text(json.dumps(out, indent=1, ensure_ascii=False))
