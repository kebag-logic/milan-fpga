#!/usr/bin/env python3
"""Planted-drift controls for scripts/ci_tool_inventory.py --check on the real tree.

usage: inventory_controls.py <pristine exact-head tree> <scratch dir>
Each control copies the tree, applies one textual mutation, and runs --check.
"REFUSE" controls must exit 2; "GAP" probes record whether a real installation
form is noticed (rc 2) or missed (rc 0).
"""
import json, shutil, subprocess, sys
from pathlib import Path

SRC, SCRATCH = Path(sys.argv[1]), Path(sys.argv[2])

def sub(rel, old, new, count=1):
    def apply(root):
        p = root / rel
        text = p.read_text()
        assert text.count(old) >= 1, (rel, old)
        p.write_text(text.replace(old, new, count))
    return apply

def append(rel, text):
    def apply(root):
        p = root / rel
        p.write_text(p.read_text() + text)
    return apply

SETUP_JAVA = ("      - uses: actions/checkout@v4\n        with:\n          fetch-depth: 0\n",
              "      - uses: actions/checkout@v4\n        with:\n          fetch-depth: 0\n"
              "      - uses: actions/setup-java@v4\n        with:\n          distribution: temurin\n"
              "          java-version: '21'\n")
CONTROLS = [
    ("REFUSE", "added apt tool", sub(".github/workflows/docs.yml", "--no-install-recommends librsvg2-bin",
                                     "--no-install-recommends librsvg2-bin jq")),
    ("REFUSE", "removed tool leaves orphan entry", sub(".github/workflows/rtl-fast.yml",
                                                       "run: python3 -m pip install --quiet behave",
                                                       "run: python3 --version")),
    ("REFUSE", "changed pip pin", sub(".github/workflows/docs.yml", "wavedrom==2.0.3.post3", "wavedrom==2.0.3.post2")),
    ("REFUSE", "changed archive sha", sub(".github/workflows/rtl.yml",
                                          "sha256=ff8c9eea5bc029b372fb4953427625cddb7cf7e58c1240623ac9f260818d5a00",
                                          "sha256=" + "0" * 64)),
    ("REFUSE", "changed Verilator env pin", sub(".github/workflows/rtl.yml", "VERILATOR_VERSION: v5.050",
                                                "VERILATOR_VERSION: v5.052")),
    ("REFUSE", "changed requirement hash", sub("tools/markdown/requirements.txt", "--hash=sha256:", "--hash=sha256:0", 1)),
    ("REFUSE", "changed LiteX git pin", sub("sw/litex/litex_pins.txt", "a1e1c3652ec2f1346ebaea7663d2867f393ae2c4",
                                            "b1e1c3652ec2f1346ebaea7663d2867f393ae2c4")),
    ("REFUSE", "install in called Python script", append("scripts/check_doc_paths.py",
                                                         '\nimport subprocess\nsubprocess.run(["pip", "install", "x"])\n')),
    ("REFUSE", "install in called shell script", append("scripts/run_litex_sims.sh", "\npip install x\n")),
    ("REFUSE", "orphan inventory entry", lambda root: (root / "ci/image/tool-inventory.json").write_text(
        json.dumps({**json.loads((root / "ci/image/tool-inventory.json").read_text()),
                    "tools": json.loads((root / "ci/image/tool-inventory.json").read_text())["tools"]
                    + [{"tool": "unused", "kind": "apt", "pin": None, "installed_by": []}]},
                   sort_keys=True, indent=2) + "\n")),
    ("GAP", "shell-string subprocess install in called script", append(
        "scripts/check_doc_paths.py", '\nimport subprocess\nsubprocess.run("pip install x", shell=True)\n')),
    ("GAP", "os.system install in called script", append(
        "scripts/check_doc_paths.py", '\nimport os\nos.system("apt-get install -y x")\n')),
    ("GAP", "pipx install in workflow run", sub(".github/workflows/rtl-fast.yml",
                                                "run: python3 -m pip install --quiet behave",
                                                "run: |\n          python3 -m pip install --quiet behave\n          pipx install x")),
    ("GAP", "Makefile recipe install under a workflow-run suite", append(
        "tb/verilator/aaf/Makefile", "\nimage-probe:\n\tpip install x\n")),
    ("GAP", "setup-java action version", sub(".github/workflows/docs.yml", *SETUP_JAVA)),
]

def check(root):
    r = subprocess.run([sys.executable, "scripts/ci_tool_inventory.py", "--check"], cwd=root,
                       capture_output=True, text=True)
    return r.returncode, (r.stdout + r.stderr).strip().splitlines()[-1]

results = []
rc0, msg0 = check(SRC)
results.append({"kind": "BASELINE", "name": "pristine exact head", "rc": rc0, "message": msg0})
for kind, name, mutate in CONTROLS:
    root = SCRATCH / name.replace(" ", "-")
    if root.exists():
        shutil.rmtree(root)
    shutil.copytree(SRC, root, symlinks=True)
    mutate(root)
    rc, msg = check(root)
    row = {"kind": kind, "name": name, "rc": rc, "message": msg}
    if name == "setup-java action version":
        w = subprocess.run([sys.executable, "scripts/ci_tool_inventory.py", "--write"], cwd=root,
                           capture_output=True, text=True)
        inv = json.loads((root / "ci/image/tool-inventory.json").read_text())
        row["after_write_tools_named_java"] = [t for t in inv["tools"] if "java" in t["tool"].lower()]
        v = subprocess.run([sys.executable, "-c", "import json,build;build.validate_pins(json.loads((build.HERE/'sources.lock.json').read_text()));print('validate_pins accepted')"],
                           cwd=root / "ci/image", capture_output=True, text=True)
        row["validate_pins_after_write"] = (v.stdout + v.stderr).strip().splitlines()[-1]
    results.append(row)
    shutil.rmtree(root)
ok = True
for row in results:
    verdict = ""
    if row["kind"] == "REFUSE":
        verdict = "PASS" if row["rc"] == 2 else "FAIL"
        ok &= row["rc"] == 2
    elif row["kind"] == "GAP":
        verdict = "NOTICED" if row["rc"] == 2 else "MISSED"
    elif row["kind"] == "BASELINE":
        ok &= row["rc"] == 0
        verdict = "PASS" if row["rc"] == 0 else "FAIL"
    row["verdict"] = verdict
    print(json.dumps(row, sort_keys=True))
print("ALL REFUSE CONTROLS PASS" if ok else "A REFUSE CONTROL FAILED")
sys.exit(0 if ok else 1)
