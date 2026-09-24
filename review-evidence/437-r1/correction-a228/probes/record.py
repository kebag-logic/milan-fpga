"""Render pages through GitHub's Markdown API with gh api, keeping the
exact request and response bytes (A212's record.py method, context kept in
both modes).  Usage: record.py <pages.json> <out.json>
pages.json: list of {"mode": "gfm"|"markdown", "page": ..., other keys kept}.
Every request and response is cached under ../render-cache/<request sha256>."""
import datetime, hashlib, json, subprocess, sys, time
from pathlib import Path

CACHE = Path(__file__).resolve().parent.parent / "render-cache"
CONTEXT = "kebag-logic/milan-fpga"


def request_bytes(mode: str, page: str) -> bytes:
    return json.dumps({"context": CONTEXT, "mode": mode, "text": page}, sort_keys=True,
                      separators=(",", ":"), ensure_ascii=True).encode("ascii")


def render(mode: str, page: str) -> dict:
    req = request_bytes(mode, page)
    key = hashlib.sha256(req).hexdigest()
    CACHE.mkdir(exist_ok=True)
    rq, rs, meta = CACHE / f"{key}.req", CACHE / f"{key}.resp", CACHE / f"{key}.meta"
    if not rs.exists():
        for attempt in range(6):
            out = subprocess.run(["gh", "api", "--method", "POST", "markdown", "--input", "-"],
                                 input=req, capture_output=True)
            if out.returncode == 0:
                break
            print("retry", key[:12], out.stderr.decode()[:200], file=sys.stderr)
            time.sleep(5 * (attempt + 1))
        else:
            raise SystemExit(f"render failed for {page[:80]!r}")
        rq.write_bytes(req)
        rs.write_bytes(out.stdout)
        meta.write_text(json.dumps({"recorded_utc": datetime.datetime.now(
            datetime.timezone.utc).isoformat(timespec="seconds")}))
        time.sleep(0.5)
    resp = rs.read_bytes()
    return {"request_bytes": req.decode("ascii"), "request_sha256": key,
            "response_bytes": resp.decode("utf-8"),
            "response_sha256": hashlib.sha256(resp).hexdigest(),
            "recorded_utc": json.loads(meta.read_text())["recorded_utc"]}


if __name__ == "__main__":
    rows = json.loads(Path(sys.argv[1]).read_text())
    out = [dict(row, **render(row["mode"], row["page"])) for row in rows]
    Path(sys.argv[2]).write_text(json.dumps(out, indent=1, ensure_ascii=False))
    print(len(out), "rendered")
