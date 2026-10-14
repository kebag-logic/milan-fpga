"""Prove docs/design/MAILBOX_SPLIT.md is still a registered gate-read page.

Reads GATE_READ_DOCS from the checkout's scripts/ci_scope.py, requires the
page exactly once, and requires the checkout's classifier to file the page as
relevant to the classifier-gated jobs. Planted controls copy ci_scope.py and
.gitmodules into a disposable directory, edit only the registration, and
require both the registration check and the copied classifier to change.
"""
import argparse
import ast
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

PAGE = "docs/design/MAILBOX_SPLIT.md"
ENTRY = '    "docs/design/MAILBOX_SPLIT.md",\n'


def registered(source):
    for node in ast.parse(source).body:
        if isinstance(node, ast.Assign) and any(getattr(t, "id", "") == "GATE_READ_DOCS" for t in node.targets):
            return [ast.literal_eval(item) for item in node.value.elts]
    raise SystemExit("GATE_READ_DOCS not found")


def problems(source):
    pages = registered(source)
    if pages.count(PAGE) != 1:
        return ["%s registered %d times" % (PAGE, pages.count(PAGE))]
    return []


def classify(script):
    result = subprocess.run([sys.executable, "-I", str(script), PAGE], capture_output=True, text=True, timeout=60)
    if result.returncode != 0:
        raise SystemExit("classifier failed: %s" % result.stderr)
    return result.stdout.strip()


parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--repo", type=Path, required=True)
args = parser.parse_args()
script = args.repo / "scripts/ci_scope.py"
source = script.read_text()
pages = registered(source)
print("GATE_READ_DOCS:", len(pages), "pages")
for page in pages:
    print("  ", page)
found = problems(source)
assert not found, found
live = classify(script)
print("live classifier:", PAGE, "->", live)
assert live == "true", live
assert source.count(ENTRY) == 1, "entry spelling changed"

controls = [
    ("registration removed", source.replace(ENTRY, "")),
    ("registration commented out", source.replace(ENTRY, "    # " + ENTRY.lstrip())),
    ("registration misspelled", source.replace(ENTRY, ENTRY.replace("MAILBOX_SPLIT", "MAILBOX_SPLlT"))),
    ("registration duplicated", source.replace(ENTRY, ENTRY + ENTRY)),
]
with tempfile.TemporaryDirectory(prefix="mailbox-split-controls-") as raw:
    work = Path(raw)
    for name, mutated in controls:
        assert mutated != source, name + ": mutation not applied"
        found = problems(mutated)
        root = work / name.replace(" ", "-")
        (root / "scripts").mkdir(parents=True)
        shutil.copyfile(args.repo / ".gitmodules", root / ".gitmodules")
        (root / "scripts/ci_scope.py").write_text(mutated)
        verdict = classify(root / "scripts/ci_scope.py")
        print("control", name, "->", "refused" if found else "ACCEPTED", found, "; copied classifier ->", verdict)
        assert found, name + " escaped the registration check"
        if name != "registration duplicated":
            assert verdict == "false", name + ": classifier still files the page as relevant"
    # The unmodified copy must still classify as the live file does, so the
    # disposable layout is not what changes the controls' verdicts.
    root = work / "unmodified"
    (root / "scripts").mkdir(parents=True)
    shutil.copyfile(args.repo / ".gitmodules", root / ".gitmodules")
    (root / "scripts/ci_scope.py").write_text(source)
    baseline = classify(root / "scripts/ci_scope.py")
    print("control unmodified copy -> copied classifier ->", baseline)
    assert baseline == "true", baseline
print("mailbox-split registration controls: %d/%d refused" % (len(controls), len(controls)))
