"""Portable I440 renderer population and identical base/head measurements.

Only generated synthetic fixture text is sent to GitHub. Cache receipts retain
exact UTF-8 input, request JSON, response HTML, timestamps and SHA-256 digests.
This reconstructs the documented population, not the unavailable old instrument.
"""
import argparse
import concurrent.futures
import datetime
import hashlib
from html.parser import HTMLParser
import importlib
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
BASE = "b17580b91deb11f3441dfc5d7f9fafe539d929b8"
CHARS = [0x0b, 0x0c, 0x0d, *range(0x1c, 0x20), 0x85, 0xa0, 0x1680,
         *range(0x2000, 0x200b), 0x2028, 0x2029, 0x202f, 0x205f, 0x3000]


def fixtures():
    rows = []
    def add(name, family, source):
        rows.append(dict(id=name, family=family, source=source))
    for fence, marker in [("backtick", "```"), ("tilde", "~~~")]:
        for code in [None, 0x20, 0x09, *CHARS]:
            trailer = "" if code is None else chr(code)
            key = "empty" if code is None else f"U{code:04X}"
            add(f"F-{fence}-{key}", "fence", f"{marker}\n{marker}{trailer}\n## Probe\n")
    for joiner, where in [("\n", "later"), ("x", "opening")]:
        for code in [None, 0x20, 0x09, *CHARS]:
            trailer = "" if code is None else chr(code)
            key = "empty" if code is None else f"U{code:04X}"
            add(f"T-{where}-{key}", "type1-character", f"<pre>{joiner}</pre{trailer}>\n## Probe\n")
        for opener in ("pre", "script", "style", "textarea"):
            for closer in ("pre", "script", "style", "textarea"):
                for name in (closer, closer.upper()):
                    add(f"N-{where}-{opener}-{name}", "type1-name", f"<{opener}>{joiner}</{name}>\n## Probe\n")
        for name in ("\u017fcript", "scr\u0131pt", "scr\u0130pt", "\u017ftyle"):
            opener = "style" if "tyle" in name else "script"
            key = name.encode("unicode_escape").decode().replace("\\", "")
            add(f"U-{where}-{key}", "unicode-fold", f"<{opener}>{joiner}</{name}>\n## Probe\n")
    for name, source in [
        ("inner-two-spaces", "<pre>\n</pre  >\n## Probe\n"),
        ("inner-mixed", "<pre>\n</PRE \t>\n## Probe\n"),
        ("inner-slash", "<pre>\n</ pre>\n## Probe\n"),
        ("long-name", "<pre>\n</prelude>\n## Probe\n"),
        ("embedded", "<pre>\ntext </sTyLe> tail\n## Probe\n"),
        ("embedded-opening", "<pre>text </sTyLe> tail\n## Probe\n"),
        ("short-fence", "````\n```\n## Probe\n"),
        ("other-fence", "~~~\n```\n## Probe\n"),
        ("mixed-trailer", "```\n``` \t \n## Probe\n"),
        ("info-trailer", "```\n``` x\n## Probe\n"),
        ("html-in-fence", "```\n</pre>\n## Probe\n"),
        ("type6-precedence", "<div>\n</pre>\n## Probe\n"),
        ("reset", "<pre></style>\n<script>\n## Probe\n"),
        ("fence-crlf", "```\r\n```\r\n## Probe\r\n"),
        ("fence-cr", "```\r```\r## Probe\r"),
        ("type1-crlf", "<pre>\r\n</style>\r\n## Probe\r\n"),
        ("type1-cr", "<pre>\r</style>\r## Probe\r"),
    ]:
        add("B-" + name, "boundary", source)
    return rows


class Headings(HTMLParser):
    def __init__(self):
        super().__init__()
        self.count = 0
    def handle_starttag(self, tag, attrs):
        if tag == "h2":
            self.count += 1


def renderer_row(row):
    folder = ROOT / "renderer" / row["id"]
    folder.mkdir(parents=True, exist_ok=True)
    source = row["source"].encode("utf-8")
    (folder / "fixture.txt").write_bytes(source)
    request = json.dumps(dict(text=row["source"], mode="gfm"), ensure_ascii=True).encode()
    (folder / "request.json").write_bytes(request)
    html_path = folder / "response.html"
    if not html_path.exists():
        result = subprocess.run(["gh", "api", "markdown", "--method", "POST", "--input", "-"],
                                input=request, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode:
            raise RuntimeError("%s: %s" % (row["id"], result.stderr.decode()))
        html_path.write_bytes(result.stdout)
        (folder / "receipt.json").write_text(json.dumps(dict(
            command=["gh", "api", "markdown", "--method", "POST", "--input", "-"],
            utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
            request_sha256=hashlib.sha256(request).hexdigest(),
            source_sha256=hashlib.sha256(source).hexdigest(),
            html_sha256=hashlib.sha256(result.stdout).hexdigest(), exit=0), indent=2)+"\n")
    parser = Headings()
    parser.feed(html_path.read_text())
    return dict(id=row["id"], family=row["family"], rendered_h2=parser.count)


def snapshot(repo):
    scripts = ROOT / "base" / "scripts"
    scripts.mkdir(parents=True, exist_ok=True)
    for name in ["gen_toc.py", "gen_toc_cases.py", "gen_toc_guards.py", "check_em_dash.py"]:
        result = subprocess.run(["git", "-C", str(repo), "show", f"{BASE}:scripts/{name}"],
                                check=True, stdout=subprocess.PIPE)
        (scripts / name).write_bytes(result.stdout)
    print(f"Saved public base scripts at {BASE}")


def observe(scripts, label):
    sys.path.insert(0, str(scripts.resolve()))
    toc = importlib.import_module("gen_toc")
    import tempfile
    rows = []
    with tempfile.TemporaryDirectory() as tmp:
        page = Path(tmp) / "fixture.txt"
        for row in fixtures():
            source = row["source"]
            page.write_bytes(source.encode())
            normalized = page.read_text()  # Actual generator reader.
            def read(text):
                return dict(h2=sum(level == 2 for level, _, _ in toc.headings(text)),
                            blocks=toc.blocks(text), refusals=toc.refusals(text))
            rows.append(dict(id=row["id"], family=row["family"], raw=read(source), reader=read(normalized)))
    (ROOT / f"sweep-{label}.json").write_text(json.dumps(rows, indent=2, ensure_ascii=True)+"\n")
    print(f"{label}: observed identical {len(rows)} fixtures")


def compare():
    base = json.loads((ROOT / "sweep-base.json").read_text())
    head = json.loads((ROOT / "sweep-head.json").read_text())
    rendered = json.loads((ROOT / "renderer-index.json").read_text())
    records = []
    def direction(walk, html):
        return "AGREE" if walk == html else "ESCAPE" if walk > html else "WITHHOLD"
    for old, new, oracle in zip(base, head, rendered, strict=True):
        assert old["id"] == new["id"] == oracle["id"]
        html = oracle["rendered_h2"]
        row = dict(id=old["id"], family=old["family"], renderer=html)
        for name, observation in [("base", old), ("head", new)]:
            for mode in ("raw", "reader"):
                data = observation[mode]
                row[f"{name}_{mode}_h2"] = data["h2"]
                row[f"{name}_{mode}_direction"] = direction(data["h2"], html)
                row[f"{name}_{mode}_refused"] = bool(data["refusals"])
        records.append(row)
    (ROOT / "comparisons.json").write_text(json.dumps(records, indent=2)+"\n")
    fields = list(records[0])
    (ROOT / "comparisons.tsv").write_text("\t".join(fields)+"\n"+"".join(
        "\t".join(str(row[key]) for key in fields)+"\n" for row in records))
    summary = {}
    for label in ("base", "head"):
        for mode in ("raw", "reader"):
            key = f"{label}_{mode}"
            summary[key] = {value: sum(row[key+"_direction"] == value for row in records)
                            for value in ("AGREE", "ESCAPE", "WITHHOLD")}
            summary[key]["refused"] = sum(row[key+"_refused"] for row in records)
    summary["changed_raw_rows"] = [r["id"] for r in records if r["base_raw_h2"] != r["head_raw_h2"]]
    summary["head_reader_unrefused_disagreements"] = [r["id"] for r in records
        if not r["head_reader_refused"] and r["head_reader_direction"] != "AGREE"]
    (ROOT / "summary.json").write_text(json.dumps(summary, indent=2)+"\n")
    print(json.dumps(summary, indent=2))
    assert not summary["head_reader_unrefused_disagreements"]


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", choices=["snapshot", "renderer", "observe", "compare"])
    ap.add_argument("--repo", type=Path, default=Path.cwd())
    ap.add_argument("--scripts", type=Path)
    ap.add_argument("--label")
    args = ap.parse_args()
    if args.mode == "snapshot":
        snapshot(args.repo)
    elif args.mode == "renderer":
        rows = fixtures()
        (ROOT / "fixtures.json").write_text(json.dumps(rows, indent=2, ensure_ascii=True)+"\n")
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
            results = list(pool.map(renderer_row, rows))
        (ROOT / "renderer-index.json").write_text(json.dumps(results, indent=2)+"\n")
        print(f"GitHub gfm: {len(results)} synthetic fixtures, exact HTML receipts saved")
    elif args.mode == "observe":
        observe(args.scripts, args.label)
    else:
        compare()
