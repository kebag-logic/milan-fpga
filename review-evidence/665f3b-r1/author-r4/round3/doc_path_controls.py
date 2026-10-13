"""Exercise the documentation path gate on disposable tracked fixtures."""
import argparse
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--repo", type=Path, required=True)
args = parser.parse_args()
with tempfile.TemporaryDirectory(prefix="doc-path-controls-") as directory:
    root = Path(directory)
    (root / "scripts").mkdir()
    (root / "docs").mkdir()
    shutil.copyfile(args.repo / "scripts/check_doc_paths.py", root / "scripts/check_doc_paths.py")
    (root / "scripts/present.py").write_text("pass\n")
    page = root / "docs/page.md"
    page.write_text("fixture\n")
    subprocess.run(["git", "init", "-q", str(root)], check=True)
    subprocess.run(["git", "-C", str(root), "add", "docs/page.md", "scripts"], check=True)
    cases = [
        ("valid", "`scripts/present.py`\n[present](../scripts/present.py#L1)\n", 0),
        ("missing-path", "`scripts/missing.py`\n", 1),
        ("past-end-anchor", "[present](../scripts/present.py#L2)\n", 1),
    ]
    for name, text, expected in cases:
        page.write_text(text)
        result = subprocess.run([sys.executable, str(root / "scripts/check_doc_paths.py")],
                                capture_output=True, text=True)
        print(name, "expected", expected, "observed", result.returncode)
        print(result.stdout)
        assert result.returncode == expected, result.stderr
print("doc-path controls: 3/3 PASS")
