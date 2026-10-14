#!/usr/bin/env python3
"""After a planted installation, does --write refuse or record it, or silently omit it?

usage: inventory_write_gaps.py <pristine exact-head tree> <scratch dir>
--check compares text, so any edit to a followed script differs. The meaningful
question for an installation form is what regeneration (--write) does with it.
"""
import json, shutil, subprocess, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
SRC, SCRATCH = Path(sys.argv[1]), Path(sys.argv[2])

def append(rel, text):
    return lambda root: (root / rel).write_text((root / rel).read_text() + text)

def sub(rel, old, new):
    def apply(root):
        t = (root / rel).read_text(); assert old in t; (root / rel).write_text(t.replace(old, new, 1))
    return apply

PROBES = [
    ("list subprocess pip install (supported form)", append("scripts/check_doc_paths.py",
        '\nimport subprocess\nsubprocess.run(["pip", "install", "probe-tool"])\n'), "probe-tool"),
    ("shell-string subprocess pip install", append("scripts/check_doc_paths.py",
        '\nimport subprocess\nsubprocess.run("pip install probe-tool", shell=True)\n'), "probe-tool"),
    ("os.system apt-get install", append("scripts/check_doc_paths.py",
        '\nimport os\nos.system("apt-get install -y probe-tool")\n'), "probe-tool"),
    ("pipx install in workflow run", sub(".github/workflows/rtl-fast.yml",
        "run: python3 -m pip install --quiet behave",
        "run: |\n          python3 -m pip install --quiet behave\n          pipx install probe-tool"), "probe-tool"),
    ("Makefile recipe install in a suite run by a workflow", append("tb/verilator/aaf/Makefile",
        "\nimage-probe:\n\tpip install probe-tool\n"), "probe-tool"),
    ("setup-java action with a version", sub(".github/workflows/docs.yml",
        "      - uses: actions/checkout@v4\n        with:\n          fetch-depth: 0\n",
        "      - uses: actions/checkout@v4\n        with:\n          fetch-depth: 0\n"
        "      - uses: actions/setup-java@v4\n        with:\n          distribution: temurin\n          java-version: '21'\n"), "java"),
]
for name, mutate, needle in PROBES:
    root = SCRATCH / ("w-" + name.replace(" ", "-"))
    if root.exists():
        shutil.rmtree(root)
    shutil.copytree(SRC, root, symlinks=True)
    mutate(root)
    w = subprocess.run([sys.executable, "scripts/ci_tool_inventory.py", "--write"], cwd=root, capture_output=True, text=True)
    row = {"probe": name, "write_rc": w.returncode, "write_message": (w.stdout + w.stderr).strip().splitlines()[-1]}
    if w.returncode == 0:
        inv = json.loads((root / "ci/image/tool-inventory.json").read_text())
        row["recorded"] = [t["tool"] for t in inv["tools"] if needle in t["tool"].lower()]
        c = subprocess.run([sys.executable, "scripts/ci_tool_inventory.py", "--check"], cwd=root, capture_output=True, text=True)
        row["check_rc_after_write"] = c.returncode
        v = subprocess.run([sys.executable, "-c", "import json,build;build.validate_pins(json.loads((build.HERE/'sources.lock.json').read_text()));print('validate_pins accepted')"],
                           cwd=root / "ci/image", capture_output=True, text=True)
        row["validate_pins"] = (v.stdout + v.stderr).strip().splitlines()[-1]
    row["verdict"] = "REFUSED" if w.returncode == 2 else ("RECORDED" if row.get("recorded") else "SILENTLY OMITTED")
    print(json.dumps(row, sort_keys=True))
    shutil.rmtree(root)
