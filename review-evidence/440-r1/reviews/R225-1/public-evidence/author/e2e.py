"""Compare the shipped CLI and per-page gate at base/head on exact fixtures."""
import argparse
import dataclasses
import importlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

from measure import renderer_row

root = Path(__file__).resolve().parent
ap = argparse.ArgumentParser()
ap.add_argument("--scripts", type=Path, required=True)
ap.add_argument("--label", required=True)
ap.add_argument("--render", action="store_true")
args = ap.parse_args()
sys.path.insert(0, str(args.scripts.resolve()))
gate = importlib.import_module("check_em_dash")
toc = importlib.import_module("gen_toc")
prefixes = [
    ("space", "<pre>\n</pre >\n"), ("tab", "<pre>\n</pre\t>\n"),
    ("inline", "<pre>x</pre >\n"), ("inline-tab", "<pre>x</pre\t>\n"),
    ("cross", "<pre>\n</style>\n"), ("cross-inline", "<pre>x</TEXTAREA>\n"),
    ("ascii", "<script>\n</SCRIPT>\n"), ("long-s", "<script>\n</\u017fcript>\n"),
    ("dotless-i", "<script>\n</scr\u0131pt>\n"), ("dotted-i", "<script>x</scr\u0130pt>\n"),
    ("fence-ff", "```\n```\f\n"), ("fence-nbsp", "~~~\n~~~\u00a0\n"),
    ("inner-ff", "<pre>\n</pre\f>\n"), ("fence-tab", "```\n```\t\n"),
    ("fence-crlf", "```\r\n```\r\n"), ("fence-cr", "```\r```\r"),
    ("inner-cr", "<pre>\n</pre\r>\n"),
]
heading = "## Old \u2014 heading\n"
tail = "\n## Alpha\n\nBody.\n\n## Beta\n\nBody.\n\n## Gamma\n\nBody.\n"
navigation = ("## Contents\n\n- **[Old \u2014 heading](#old--heading)** -- Copied.\n"
              "- **[Alpha](#alpha)** -- What alpha holds.\n"
              "- **[Beta](#beta)** -- What beta holds.\n"
              "- **[Gamma](#gamma)** -- What gamma holds.\n\n")
head = "# Page\n\n" + navigation + heading + tail
sources = {name: "# Page\n\n" + prefix + heading + tail for name, prefix in prefixes}
fixtures = [dict(id="E-"+name, family="em-dash-base", source=source) for name,source in sources.items()]
fixtures.append(dict(id="E-head", family="em-dash-head", source=head))
(root / "e2e-fixtures.json").write_text(json.dumps(fixtures, indent=2, ensure_ascii=True)+"\n")
if args.render:
    rendered = [renderer_row(row) for row in fixtures]
    (root / "e2e-renderer.json").write_text(json.dumps(rendered, indent=2)+"\n")
results = []
with tempfile.TemporaryDirectory(prefix="i440.cli.") as tmp:
    repo = Path(tmp)
    scripts = repo / "scripts"
    scripts.mkdir()
    for name in ("gen_toc.py", "gen_toc_cases.py", "gen_toc_guards.py", "check_em_dash.py", "gen_toc_closer_cases.py"):
        source = args.scripts / name
        if source.exists():
            shutil.copyfile(source, scripts / name)
    gate._fixture_git(repo, "init", "-q", "--initial-branch=main")
    for name, source in sources.items():
        (repo / (name+".md")).write_bytes(source.encode())
    base = gate._commit(repo, "synthetic base")
    for name in sources:
        (repo / (name+".md")).write_text(head)
    gate._commit(repo, "synthetic head")
    for name in sources:
        path = name+".md"
        verdict = gate.Verdict()
        gate.judge_page(repo, base, gate.Change(path,path), verdict)
        normalized = gate.git(repo, "show", base+":"+path)
        added = gate.added_lines(repo, base, gate.Change(path,path))
        results.append(dict(id="E-"+name, verdict=dataclasses.asdict(verdict),
                            base_refusals=toc.refusals(normalized), base_headings=toc.headings(normalized),
                            head_provenance=toc.generated_block(head, path),
                            added=[dataclasses.asdict(line) for line in added]))
    command = [sys.executable, "-B", str(scripts/"check_em_dash.py"), "--base", base]
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    (root / f"e2e-cli-{args.label}.log").write_bytes(result.stdout)
    assert result.returncode == 1, result.stdout.decode()
(root / f"e2e-{args.label}.json").write_text(json.dumps(results, indent=2, ensure_ascii=True)+"\n")
for row in results:
    print(row["id"], len(row["verdict"]["findings"]), row["verdict"]["exempt"],
          bool(row["base_refusals"]))
print(f"Shipped {args.label} CLI exit {result.returncode}; exact fixtures, diffs and findings saved")
