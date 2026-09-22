"""R226 sweep: GitHub renderer vs base/head walk on the R226 fixture population.

Usage:
  python3 -B r226_sweep.py render   OUTDIR            # query GitHub (gfm + markdown modes), cached
  python3 -B r226_sweep.py observe  OUTDIR SCRIPTS LABEL
  python3 -B r226_sweep.py compare  OUTDIR

Only synthetic fixture text leaves the machine. Each request/response is kept
byte-exact with SHA-256 digests under OUTDIR/renderer/<mode>/<id>/.
"""
import datetime
import hashlib
import importlib
import json
import subprocess
import sys
import tempfile
import time
from html.parser import HTMLParser
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from r226_fixtures import fixtures  # noqa: E402

MODES = ("gfm", "markdown")


class H2(HTMLParser):
    def __init__(self):
        super().__init__()
        self.count = 0

    def handle_starttag(self, tag, attrs):
        if tag == "h2":
            self.count += 1


def render_one(out: Path, row: dict, mode: str) -> dict:
    folder = out / "renderer" / mode / row["id"]
    folder.mkdir(parents=True, exist_ok=True)
    source = row["source"].encode("utf-8")
    request = json.dumps({"text": row["source"], "mode": mode}, ensure_ascii=True).encode()
    (folder / "fixture.bin").write_bytes(source)
    (folder / "request.json").write_bytes(request)
    html = folder / "response.html"
    if not html.exists():
        for attempt in range(12):
            time.sleep(1.2)                  # stay under GitHub's secondary rate limit
            res = subprocess.run(["gh", "api", "markdown", "--method", "POST", "--input", "-"],
                                 input=request, capture_output=True)
            if res.returncode == 0:
                break
            if b"secondary rate limit" in res.stderr:
                time.sleep(60 * (attempt + 1))
                continue
            raise RuntimeError(f"{row['id']} {mode}: {res.stderr.decode()}")
        if res.returncode:
            raise RuntimeError(f"{row['id']} {mode}: {res.stderr.decode()}")
        html.write_bytes(res.stdout)
        (folder / "receipt.json").write_text(json.dumps({
            "utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "command": "gh api markdown --method POST --input -",
            "source_sha256": hashlib.sha256(source).hexdigest(),
            "request_sha256": hashlib.sha256(request).hexdigest(),
            "html_sha256": hashlib.sha256(res.stdout).hexdigest()}, indent=1) + "\n")
    p = H2()
    p.feed(html.read_bytes().decode("utf-8"))
    return {"id": row["id"], "mode": mode, "h2": p.count}


def render(out: Path) -> None:
    rows = fixtures()
    (out / "fixtures.json").write_text(json.dumps(rows, indent=1, ensure_ascii=True) + "\n")
    jobs = [(r, m) for r in rows for m in MODES]
    res = [render_one(out, *a) for a in jobs]      # sequential after a 403 at 4 workers
    index = {}
    for r in res:
        index.setdefault(r["id"], {})[r["mode"]] = r["h2"]
    (out / "renderer-index.json").write_text(json.dumps(index, indent=1) + "\n")
    print(f"rendered {len(rows)} fixtures x {len(MODES)} modes")


def observe(out: Path, scripts: Path, label: str) -> None:
    sys.path.insert(0, str(scripts.resolve()))
    toc = importlib.import_module("gen_toc")
    rows = []
    with tempfile.TemporaryDirectory() as tmp:
        page = Path(tmp) / "page.md"
        for row in fixtures():
            raw = row["source"]
            page.write_bytes(raw.encode("utf-8"))
            normalized = page.read_text()          # the generator's own reader
            # the gate's reader: git text mode through subprocess (same translation)
            gate_text = subprocess.run(["cat", str(page)], capture_output=True, text=True,
                                       encoding="utf-8", errors="replace").stdout

            def obs(text):
                return {"h2": sum(1 for lvl, _, _ in toc.headings(text) if lvl == 2),
                        "refused": bool(toc.refusals(text))}
            rows.append({"id": row["id"], "raw": obs(raw), "reader": obs(normalized),
                         "gate_reader_same": gate_text == normalized})
    (out / f"observe-{label}.json").write_text(json.dumps(rows, indent=1) + "\n")
    print(f"{label}: observed {len(rows)} fixtures with {scripts}")


def direction(walk: int, html: int) -> str:
    return "AGREE" if walk == html else ("ESCAPE" if walk > html else "WITHHOLD")


def compare(out: Path) -> None:
    rows = fixtures()
    rend = json.loads((out / "renderer-index.json").read_text())
    base = {r["id"]: r for r in json.loads((out / "observe-base.json").read_text())}
    head = {r["id"]: r for r in json.loads((out / "observe-head.json").read_text())}
    table, summary = [], {}
    for row in rows:
        rid = row["id"]
        g, m = rend[rid]["gfm"], rend[rid]["markdown"]
        rec = {"id": rid, "family": row["family"], "gfm": g, "markdown": m}
        for lab, obs in (("base", base[rid]), ("head", head[rid])):
            for mode in ("raw", "reader"):
                rec[f"{lab}_{mode}_h2"] = obs[mode]["h2"]
                rec[f"{lab}_{mode}_refused"] = obs[mode]["refused"]
                rec[f"{lab}_{mode}_dir"] = direction(obs[mode]["h2"], g)
            # shipped answer: reader-normalized text, refusal applied
            rec[f"{lab}_shipped"] = ("REFUSED" if obs["reader"]["refused"]
                                     else direction(obs["reader"]["h2"], g))
            rec[f"{lab}_gate_reader_same"] = obs["gate_reader_same"]
        table.append(rec)
    for lab in ("base", "head"):
        for col in ("raw_dir", "reader_dir", "shipped"):
            key = f"{lab}_{col}"
            counts = {}
            for rec in table:
                counts[rec[key]] = counts.get(rec[key], 0) + 1
            summary[key] = counts
    summary["rows"] = len(table)
    summary["gfm_vs_markdown_mode_differ"] = [r["id"] for r in table if r["gfm"] != r["markdown"]]
    summary["head_shipped_not_agree_or_refused"] = [r["id"] for r in table
                                                   if r["head_shipped"] not in ("AGREE", "REFUSED")]
    summary["head_raw_not_agree"] = [(r["id"], r["head_raw_dir"], r["head_raw_refused"])
                                     for r in table if r["head_raw_dir"] != "AGREE"]
    summary["changed_base_to_head_reader"] = [r["id"] for r in table
                                             if r["base_reader_h2"] != r["head_reader_h2"]]
    summary["changed_base_to_head_raw"] = [r["id"] for r in table if r["base_raw_h2"] != r["head_raw_h2"]]
    summary["base_shipped_escapes"] = [r["id"] for r in table if r["base_shipped"] == "ESCAPE"]
    summary["base_shipped_withholds"] = [r["id"] for r in table if r["base_shipped"] == "WITHHOLD"]
    summary["gate_reader_mismatch"] = [r["id"] for r in table
                                       if not (r["base_gate_reader_same"] and r["head_gate_reader_same"])]
    (out / "comparison.json").write_text(json.dumps(table, indent=1) + "\n")
    cols = list(table[0])
    (out / "comparison.tsv").write_text("\t".join(cols) + "\n" + "".join(
        "\t".join(str(r[c]) for c in cols) + "\n" for r in table))
    (out / "summary.json").write_text(json.dumps(summary, indent=1) + "\n")
    print(json.dumps(summary, indent=1))


if __name__ == "__main__":
    cmd, out = sys.argv[1], Path(sys.argv[2])
    out.mkdir(parents=True, exist_ok=True)
    if cmd == "render":
        render(out)
    elif cmd == "observe":
        observe(out, Path(sys.argv[3]), sys.argv[4])
    else:
        compare(out)
