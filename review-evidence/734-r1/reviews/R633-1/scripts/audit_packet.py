#!/usr/bin/env python3
"""Audit exact source bytes, public author receipts, and reviewer linked images."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess

p = argparse.ArgumentParser()
p.add_argument("source", type=Path)
p.add_argument("packet", type=Path)
a = p.parse_args()
source = a.source.resolve()
packet = a.packet.resolve()
env = dict(os.environ, GIT_NO_REPLACE_OBJECTS="1")
head = "0519ff3684258482a56892056edbfbb65c186f88"
base = "a0f39ad4f4bfc9ed4805bac049c4f2b926a94ec0"
evidence = "a7ca711b8256ea6d655203364a2b83c1af340f48"

def git(root, *args):
    return subprocess.check_output(["git", "-C", str(root), *args], env=env)

def digest(data):
    return hashlib.sha256(data).hexdigest()

def emit(name, value):
    (packet/"receipts"/name).write_text(json.dumps(value, indent=2)+"\n")
    print(name, json.dumps(value))

def verify_tree(root, revision):
    rows = git(root, "ls-tree", "-rz", revision).split(b"\0")
    expected_index = []
    blobs = 0
    links = {}
    for row in rows:
        if not row:
            continue
        fields, raw_path = row.split(b"\t", 1)
        mode, kind, oid = fields.split()
        expected_index.append(mode+b" "+oid+b" 0\t"+raw_path)
        path = root/os.fsdecode(raw_path)
        if mode == b"160000":
            links[os.fsdecode(raw_path)] = oid.decode()
            continue
        metadata = path.lstat()
        if mode == b"120000":
            assert stat.S_ISLNK(metadata.st_mode), raw_path
            data = os.fsencode(os.readlink(path))
        else:
            assert stat.S_ISREG(metadata.st_mode), raw_path
            observed_mode = b"100755" if metadata.st_mode & 0o111 else b"100644"
            assert observed_mode == mode, raw_path
            data = path.read_bytes()
        observed_oid = hashlib.sha1(b"blob "+str(len(data)).encode()+b"\0"+data).hexdigest()
        assert observed_oid == oid.decode(), raw_path
        blobs += 1
    actual_index = [r for r in git(root, "ls-files", "--stage", "-z").split(b"\0") if r]
    assert actual_index == expected_index, "index entries differ from pinned tree"
    return dict(tracked_blobs_verified=blobs, index="exact", modes="exact", gitlinks=links)

assert git(source,"rev-parse","HEAD").decode().strip() == head
assert git(source,"rev-parse","HEAD^{tree}").decode().strip() == "a7777345d841a565687c667bee6d53e0f5a734b8"
state = verify_tree(source, head)
state.update(head=head, tree="a7777345d841a565687c667bee6d53e0f5a734b8")
state["initialized_required_submodules"] = {}
for path in ("protocol-processor", "gptp-processor", "third_party/verilog-axis"):
    sub = source/path
    pin = state["gitlinks"][path]
    assert (sub/".git").is_file()
    assert git(sub,"rev-parse","HEAD").decode().strip() == pin
    parent = git(sub,"rev-parse","--show-superproject-working-tree").decode().strip()
    assert Path(parent).resolve() == source
    state["initialized_required_submodules"][path] = verify_tree(sub,pin)
state["status_porcelain"] = git(source,"status","--porcelain=v1").decode().splitlines()
assert not state["status_porcelain"]
emit("tree-integrity.json",state)

public = packet/"scratch/public-evidence"
manifest = json.loads((public/"MANIFEST.json").read_text())
checked = []
for row in manifest:
    path = public/row["file"]
    if not path.exists():
        assert row["file"] in ("author/HANDOFF.md","author/PR-BODY.md")
        continue
    got = digest(path.read_bytes())
    assert got == row["published_sha256"], row["file"]
    checked.append(dict(file=row["file"], sha256=got))
validated = json.loads((public/"author/validated-files.json").read_text())
for path,want in validated.items():
    assert digest((source/path).read_bytes()) == want,path
selected = ["scope-final","act-selftest-final","ci-events-check-final","ci-events-selftest",
            "docs-check-final","docs-no-git","docs-paths","toc-check","toc-anchors",
            "em-dash-head","python-idiom-accepted","pp-sources","evidence-readers",
            "images-before","images-after","image-audit-controls"]
receipts=[]
for name in selected:
    row=json.loads((public/"author"/(name+".json")).read_text())
    assert row["rc"] == 0
    receipts.append(dict(name=name,rc=row["rc"],seconds=row["seconds"]))
emit("public-evidence-audit.json", dict(commit=evidence, published_digests_verified=checked,
      exact_head_files_verified=validated, selected_author_gate_results=receipts,
      limitations="Author source-head receipts only. No manager source bank is claimed."))

product_paths=["hdl","sw","configs","syn","REQUIREMENTS.md","protocol-processor",
               "gptp-processor","third_party"]
assert not git(source,"diff","--name-only",base,head,"--",*product_paths)
images=packet/"scratch/linked-images-final/images"
published=json.loads((public/"author/image-hashes.json").read_text())
hashes=[]
for item in published:
    shape=item["shape"]
    before=(images/"base"/shape/"ctrl_app.elf").read_bytes()
    after=(images/"head"/shape/"ctrl_app.elf").read_bytes()
    assert before == after,shape
    got=digest(after)
    assert got == item["before_sha256"] == item["after_sha256"],shape
    assert len(after) == item["before_bytes"] == item["after_bytes"],shape
    hashes.append(dict(shape=shape,base_sha256=digest(before),head_sha256=got,
                       bytes=len(after),byte_identical=True,agrees_with_author=True))
emit("linked-image-hashes.json", dict(base=base,head=head,images=hashes,
      unchanged_product_input_paths=product_paths,
      limitation="Measurement fixtures; no physical calibration or hardware execution."))
