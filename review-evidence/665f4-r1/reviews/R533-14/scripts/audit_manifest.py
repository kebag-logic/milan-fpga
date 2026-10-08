#!/usr/bin/env python3
"""Independent static and Git-config probes; never import or execute act_ci.py."""
import argparse
import ast
import hashlib
import os
from pathlib import Path
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument("root", type=Path)
parser.add_argument("scratch", type=Path)
args = parser.parse_args()
root = args.root.resolve()
scratch = args.scratch.resolve()
scratch.mkdir(parents=True, exist_ok=True)
HEAD = "fe1cd0679f5028c749af7242c903a82ca2b3d692"
PARENT = "154722e14781c7373f3229420b6e007f9bcf9835"
LW = ("third_party/lwSRP", "third_party/lwSRP", "https://github.com/kebag-logic/lwSRP.git")
env = {"PATH": os.defpath, "HOME": str(scratch), "LANG": "C.UTF-8",
       "GIT_CONFIG_NOSYSTEM": "1", "GIT_CONFIG_GLOBAL": os.devnull,
       "GIT_NO_REPLACE_OBJECTS": "1", "GIT_OPTIONAL_LOCKS": "0"}

def git(*words):
    return subprocess.check_output(["git", "-C", str(root), *words], env=env)

def assignment(tree, name):
    return next(n.value for n in tree.body if isinstance(n, ast.Assign)
                and any(isinstance(t, ast.Name) and t.id == name for t in n.targets))

def dump(node):
    return ast.dump(node, include_attributes=False)

def functions(tree):
    return {n.name: n for n in tree.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))}

source = git("show", HEAD + ":scripts/act_ci.py").decode()
parent_source = git("show", PARENT + ":scripts/act_ci.py").decode()
tree = ast.parse(source)
old = ast.parse(parent_source)
manifest = ast.literal_eval(assignment(tree, "TRUSTED_SUBMODULES"))
prior = ast.literal_eval(assignment(old, "TRUSTED_SUBMODULES"))
assert manifest == (*prior, LW)
fixture = functions(tree)["selftest_submodule_manifest"]
independent = ast.literal_eval(assignment(fixture, "manifest"))
assert independent == manifest
print("PASS: exact five-entry manifest; independent literal fixture; sole production addition is approved lwSRP tuple")

required_node = assignment(tree, "REQUIRED_SUBMODULES")
expected_expr = ast.parse('tuple(path for name, path, _url in TRUSTED_SUBMODULES if name != "external")', mode="eval").body
assert dump(required_node) == dump(expected_expr)
required = tuple(p for n, p, u in manifest if n != "external")
assert len(required) == 4 and required[-1] == LW[1]
assert all(u.startswith("https://github.com/") for n, p, u in manifest if n != "external")
assert "external" not in required
print("PASS: four public HTTPS dependencies, external excluded, required-submodule derivation unchanged")

def normalized(t):
    kept = []
    for n in t.body:
        if isinstance(n, ast.FunctionDef) and n.name in {"selftest_submodule_manifest", "selftest_lwsrp_manifest"}:
            continue
        if isinstance(n, ast.Assign) and any(isinstance(x, ast.Name) and x.id == "TRUSTED_SUBMODULES" for x in n.targets):
            continue
        kept.append(dump(n))
    return kept

assert normalized(tree) == normalized(old)
print("PASS: every other top-level AST node unchanged, including all production functions and other tests")
changed = git("diff", "--name-only", PARENT, HEAD).decode().splitlines()
assert changed == ["docs/testing/CI_WORKFLOWS.md", "scripts/act_ci.py"]
assert git("rev-list", "--count", PARENT + ".." + HEAD).strip() == b"1"
assert git("rev-parse", HEAD + "^").decode().strip() == PARENT
print("PASS: one commit, two assigned files; no RTL, firmware, workflow or gitlink delta")

gm = git("show", HEAD + ":.gitmodules").decode()
links = [line.split("\t", 1)[1] for line in git("ls-tree", "-r", HEAD).decode().splitlines() if line.startswith("160000 ")]
oracle = {f"submodule.{n}.{k}": v for n, p, u in manifest for k, v in (("path", p), ("url", u))}

def parse(text):
    path = scratch / "candidate.gitmodules"
    path.write_text(text)
    raw = subprocess.check_output(["git", "config", "--null", "--list", "--file", str(path)], env=env)
    pairs = [x.split(b"\n", 1) for x in raw.split(b"\0") if x]
    assert all(len(x) == 2 for x in pairs)
    return [(k.decode(), v.decode()) for k, v in pairs]

def judge(text, paths, expected=None):
    pairs = parse(text)
    if len({k for k, v in pairs}) != len(pairs):
        return "duplicate"
    if dict(pairs) != (oracle if expected is None else expected):
        return "manifest"
    if set(paths) != {p for n, p, u in manifest} or len(paths) != len(set(paths)):
        return "gitlinks"
    return "accepted"

assert judge(gm, links) == "accepted"
stanza = '[submodule "third_party/lwSRP"]\n\tpath = third_party/lwSRP\n\turl = https://github.com/kebag-logic/lwSRP.git\n'
assert gm.count(stanza) == 1
cases = [
    ("drops lwSRP", gm.replace(stanza, ""), links, "manifest"),
    ("duplicates lwSRP", gm + stanza, links, "duplicate"),
    ("adds another lwSRP", gm + stanza.replace("third_party/lwSRP", "third_party/lwSRP-extra"), links, "manifest"),
    ("redirects lwSRP", gm.replace(LW[2], "https://127.0.0.1:9/attacker/lwSRP.git"), links, "manifest"),
    ("drops lwSRP gitlink", gm, [p for p in links if p != LW[1]], "gitlinks"),
    ("adds lwSRP gitlink", gm, links + [LW[1] + "-extra"], "gitlinks"),
    ("wrong lwSRP path", gm.replace("path = " + LW[1], "path = third_party/wrong"), links, "manifest"),
    ("SSH lwSRP URL", gm.replace(LW[2], "git@github.com:kebag-logic/lwSRP.git"), links, "manifest"),
    ("escape lwSRP path", gm.replace("path = " + LW[1], "path = ../lwSRP"), links, "manifest"),
    ("custom lwSRP update", gm + "\tupdate = !false\n", links, "manifest"),
]
for label, text, paths, reason in cases:
    assert judge(text, paths) == reason, label
    print(f"PASS independent Git-config oracle: {label}: {reason}")

# The two changed expected dictionaries leave gitlinks untouched. The checker
# should now accept, so a refusal assertion would record exactly one failure.
for label, text, paths, reason in cases:
    if label not in {"drops lwSRP", "adds another lwSRP"}:
        continue
    assert judge(text, paths, dict(parse(text))) == "accepted"
    print(f"PASS standing-plant reasoning: {label}: unchanged gitlinks cannot mask removed config refusal")

# Sensitivity of this independent inventory check, separate from the candidate's
# published runner mutation results.
assert manifest != prior
assert required != required[:-1]
print("PASS independent inventory controls reject omitted manifest entry and omitted materialization path")
docs = git("show", HEAD + ":docs/testing/CI_WORKFLOWS.md").decode()
contract = docs[docs.index("Before any candidate-directed network operation"):docs.index("The runner then populates")]
for text in ("matching five", "four allowlisted", "`third_party/lwSRP`", "never fetched", "enables only HTTPS"):
    assert text in contract, text
print("PASS prose enumeration: five gitlinks; four fetched public dependencies; HTTPS only; external never fetched")

dev_file = scratch.parent / "live-dev-act_ci.py"
if dev_file.exists():
    dev = ast.parse(dev_file.read_text())
    assert normalized(dev) == normalized(old)
    assert ast.literal_eval(assignment(dev, "TRUSTED_SUBMODULES")) == prior
    dev_bytes = dev_file.read_bytes()
    # Construct inert bytes only. Do not install, import, or execute this file.
    node = assignment(dev, "TRUSTED_SUBMODULES")
    lines = dev_bytes.decode().splitlines(keepends=True)
    insertion = ('    (\n        "third_party/lwSRP",\n        "third_party/lwSRP",\n'
                 '        "https://github.com/kebag-logic/lwSRP.git",\n    ),\n')
    lines.insert(node.end_lineno - 1, insertion)
    adapted = "".join(lines).encode()
    adapted_tree = ast.parse(adapted)
    assert ast.literal_eval(assignment(adapted_tree, "TRUSTED_SUBMODULES")) == manifest
    assert normalized(adapted_tree) == normalized(dev)
    (scratch / "trusted-base-plus-entry.inert.txt").write_bytes(adapted)
    print("PASS manager procedure: trusted live-dev source plus only the tuple preserves every existing production node")
    print("trusted-base SHA256=" + hashlib.sha256(dev_bytes).hexdigest())
    print("inert manifest-only adaptation SHA256=" + hashlib.sha256(adapted).hexdigest())
print("LIMIT: static inspection and independent data probes only; no runner or runner self-test executed")
