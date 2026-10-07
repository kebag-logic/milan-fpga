#!/usr/bin/env python3
"""Exercise checker failures and the empty-suite guard in disposable trees.

Usage: python3 scripts/probe_checks.py SOURCE PACKET
"""
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

source, packet = map(lambda p: Path(p).resolve(), sys.argv[1:3])
scratch = packet / "scratch"
fixture = scratch / "checker-fixture"
shutil.copytree(source / "doc/tools", fixture / "doc/tools", dirs_exist_ok=True)
log = []

def run(name, command, expected, cwd=fixture, env=None, stdin=None):
    result = subprocess.run(command, cwd=cwd, env=env, input=stdin, text=True,
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=120)
    output = result.stdout.replace(str(packet), "<packet>").replace(str(source), "<source>").replace(str(Path.home()), "<home>")
    (packet / "receipts" / (name + ".log")).write_text(output)
    (packet / "receipts" / (name + ".rc")).write_text(str(result.returncode) + "\n")
    log.append(dict(name=name, rc=result.returncode, expected=expected, passed=result.returncode == expected))
    assert result.returncode == expected, output

# Only the fixture document belongs to each deliberately reduced input tree.
(fixture / "doc/tools/README.md").unlink()
page = fixture / "README.md"
page.write_text("# Example\n\n" + " ".join(["word"] * 26) + ".\n")
run("probe-long-sentence", ["python3", "doc/tools/check_sentences.py"], 1)
page.write_text("# Example\n\nUse `mrp_rx` from src/core/mrp_mad.c for clause 10.7 and issue #1.\n")
run("probe-unlinked-references", ["python3", "doc/tools/check_references.py"], 1)
(fixture / "sample.c").write_text("int sample;\n")
page.write_text("# Example\n\n[missing](missing.c) [range](sample.c#L2-L3) [heading](README.md#absent)\n")
run("probe-bad-links", ["python3", "doc/tools/check_links.py", "--local-only"], 1)
page.write_text("# Example\n\n[valid](sample.c#L1) [heading](README.md#example)\n")
run("probe-good-links", ["python3", "doc/tools/check_links.py", "--local-only"], 0)
page.write_text("# Example\n\n~~~mermaid\nflowchart TD\n" + "\n".join(f"N{i}[Node {i}]" for i in range(16)) + "\n~~~\n")
run("probe-large-graph", ["python3", "doc/tools/render_mermaid.py", "--output", str(scratch / "fixture-graphs")], 1)

sys.path.insert(0, str(fixture / "doc/tools"))
from check_links import repository_endpoint
cases = [
    ("https://github.com/kebag-logic/lwSRP/issues/1", "repos/kebag-logic/lwSRP/issues/1"),
    ("https://github.com/kebag-logic/lwSRP/pull/5#issuecomment-6030839413", "repos/kebag-logic/lwSRP/issues/comments/6030839413"),
    ("https://github.com/kebag-logic/lwSRP-extra/issues/1", None),
    ("https://github.com.example.org/kebag-logic/lwSRP/issues/1", None),
    ("https://github.com/kebag-logic/lwSRP/blob/main/README.md", ""),
]
for url, expected in cases:
    actual = repository_endpoint(url, "kebag-logic/lwSRP")
    assert actual == expected
    log.append(dict(url=url, expected=expected, actual=actual, passed=True))

checkout = scratch / "command-source"
prefix = scratch / "dependency-prefix"
env = os.environ.copy()
env.update(CPATH=str(prefix / "include"), LIBRARY_PATH=str(prefix / "lib"), LD_LIBRARY_PATH=str(prefix / "lib"))
unit = checkout / "build/unit_tests"
backup = checkout / "build/unit_tests.original"
unit.rename(backup)
try:
    stub = '#include <cgreen/cgreen.h>\nint main(void) { return run_test_suite(create_test_suite(), create_text_reporter()); }\n'
    run("probe-empty-suite-compile", ["cc", "-xc", "-", "-lcgreen", "-o", str(unit)], 0, checkout, env, stub)
    run("probe-empty-suite-direct", [str(unit)], 0, checkout, env)
    run("probe-empty-suite-guard", ["ctest", "--test-dir", "build", "--output-on-failure"], 8, checkout, env)
finally:
    unit.unlink(missing_ok=True)
    backup.rename(unit)
(packet / "receipts/probes.json").write_text(json.dumps(log, indent=2) + "\n")
print(json.dumps(log, indent=2))
