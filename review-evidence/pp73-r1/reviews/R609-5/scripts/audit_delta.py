#!/usr/bin/env python3
"""Check merge provenance, regeneration, named plants and real public trace receipts."""
import copy
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import subprocess
import sys

source = Path(sys.argv[1]).resolve()
packet = Path(__file__).resolve().parents[1]
scratch = packet / "scratch"
out = packet / "receipts"
os.environ["TMPDIR"] = str(scratch / "tmp")
sys.dont_write_bytecode = True
sys.path.insert(0, str(source / "scripts"))
from aecp_gate import selftest as st
from aecp_gate.inputs import load, DOC
from aecp_gate.fields import registry, plant_field
from aecp_gate.doc import regenerated

def git(*args):
    return subprocess.check_output(["git", "-C", str(source), *args])

def blob(ref, path):
    return git("show", ref + ":" + path)

def write(name, obj):
    (out / name).write_text(json.dumps(obj, indent=2) + "\n")

head = git("rev-parse", "HEAD").decode().strip()
assert head == "4bee75b2e647507a71ece50359fceb135c334757"
parents = git("show", "-s", "--format=%P", "HEAD").decode().strip().split()
assert parents == ["4029dc5de2a0a540d6a015c747319fbee7abba2e", "6d536868ee2a4762ab307d5ed51ff09c01130942"]
sv = [p for p in git("ls-tree", "-r", "--name-only", "HEAD", "hdl").decode().splitlines() if p.endswith(".sv")]
assert all(blob("HEAD", p) == blob(parents[1], p) for p in sv)
model = ["hdl/aecp/ucode/" + p for p in ("aecp_commands.json", "aecp_fields.json", "gen_ucode.py")]
assert all(blob("HEAD", p) == blob(parents[0], p) for p in model)
rules = ["scripts/check-req-tags.py", "tb/common/req_tag.py", "tb/common/req_tag.hpp",
         "tb/elab_guards/guards.py", "tb/elab_guards/mutants.py"]
assert all(blob("HEAD", p) == blob(parents[1], p) for p in rules)
remerge = git("show", "--format=", "--remerge-diff", "HEAD").decode()
changed = re.findall(r"^diff --git a/(.+) b/", remerge, re.M)
expected = ["Makefile", "docs/00_MILAN_COMPLIANCE_REVIEW.md", "docs/architecture/06_aecp_engine.md",
            "docs/architecture/09_verification.md", "scripts/aecp_gate/field_docs.py",
            "tb/aecp_cmds/Makefile", "tb/aecp_cmds/README.md", "tb/aecp_cmds/check_observed.py",
            "tb/aecp_cmds/decode.json"]
assert set(changed) == set(expected), changed
old = json.loads(blob(parents[0], "tb/aecp_cmds/decode.json"))
new = json.loads(blob("HEAD", "tb/aecp_cmds/decode.json"))
old_inputs = old["sweep"].pop("inputs") if "sweep" in old else None
new_inputs = new["sweep"].pop("inputs") if "sweep" in new else None
assert old_inputs is not None and new_inputs is not None
assert old == new
changed_inputs = [k for k in new_inputs if new_inputs[k] != old_inputs[k]]
assert len(changed_inputs) == 5
write("merge-audit.json", dict(head=head, tree=git("rev-parse", "HEAD^{tree}").decode().strip(),
      parents=parents, production_sv_identical_to_main=sv, model_identical_to_round4=model,
      imported_rules_identical_to_main=rules, only_merge_resolutions_and_adaptations=changed,
      observation_behavior_identical=True, changed_observation_digests=changed_inputs))

# The field generator must recreate a deliberately damaged reference and be idempotent.
tree = scratch / "gates"
paths = ["scripts/check_aecp_commands.py", "docs/architecture/06_aecp_engine.md",
         "docs/architecture/09_verification.md", "docs/00_MILAN_COMPLIANCE_REVIEW.md"]
before = {p: (tree / p).read_bytes() for p in paths}
for p in paths:
    text = before[p].decode()
    if "<!-- AECP ARCH -->" in text:
        text = re.sub(r"(?<=<!-- AECP ARCH -->).*?(?=<!-- /AECP ARCH -->)", "PLANTED", text)
    elif "<!-- BEGIN F06.14:" in text:
        text = text.replace("40 B echo (cdl 28)", "41 B echo (cdl 29)", 1)
    else:
        text = text.replace("held to nothing", "PLANTED", 1)
    assert text.encode() != before[p], p
    (tree / p).write_text(text)
with (out / "regeneration.log").open("w") as log:
    for _ in range(2):
        subprocess.run([sys.executable, "-B", "scripts/check_aecp_commands.py", "--write"],
                       cwd=tree, stdout=log, stderr=subprocess.STDOUT, check=True)
assert all((tree/p).read_bytes() == before[p] for p in paths)
write("regeneration.json", {p: dict(repaired_and_idempotent=True, sha256=hashlib.sha256(before[p]).hexdigest()) for p in paths})

# Recompute traceability records using the unchanged #173 authority itself.
spec = importlib.util.spec_from_file_location("trace_gate", source / "scripts/check-req-tags.py")
trace = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = trace
spec.loader.exec_module(trace)
review = (source / trace.REVIEW).read_text()
verify = (source / trace.VERIFY).read_text()
problems = []
rows = trace.read_rows(review)
tags = trace.read_tags(source, rows, problems)
waivers = trace.read_waivers(verify, rows, problems)
states = trace.row_states(rows, tags, waivers, problems)
trace.check_records(rows, states, verify, problems)
assert not problems, problems
assert states["REQ-VER-002"] == "no check"
write("regenerated-trace-records.json", dict(rows=states, tags=[t._asdict() for t in tags], problems=problems))

# Revalidate the author's actual complete suite log and its own execution evidence.
public = out / "public-author-r5"
suite_log = (public / "logs/head-suites.log").read_text()
tag_log = (public / "head-tags.txt").read_text()
problems = []
ran = trace.check_executed(tags, suite_log, tag_log, problems)
assert not problems and ran == 226, problems
own_tag = (out / "observed-tags.txt").read_text().strip()
assert own_tag in tag_log.splitlines(), own_tag
missing = "\n".join(line for line in tag_log.splitlines() if line != own_tag) + "\n"
refusals = []
trace.check_executed(tags, suite_log, missing, refusals)
assert len(refusals) == 1 and "DEAD TAG REQ-VER-002" in refusals[0], refusals
write("trace-execution-audit.json", dict(public_run_rechecked=True, evidence_lines=ran,
      reviewer_fresh_tag=own_tag, omitted_tag_refusal=refusals, full_suites_executed_by_reviewer=False))

# Keep the actual named diagnostics, including all registry plants and echo-hide.
base = load(source)
assert not st.check(base)
records = []
for family, cases, invoke in [
    ("memory", st.MUTANTS + st.FIELD_MUTANTS, lambda fn: st.in_memory(base, fn)),
    ("observed", st.OBSERVED_MUTANTS, lambda fn: st.on_copy(base, fn)),
    ("file", st.FILE_MUTANTS, lambda fn: st.planted_copy(source, fn)),
    ("generator", st.GENERATOR_MUTANTS, lambda fn: st.generator_copy(source, fn)),
]:
    for name, fn, words in cases:
        got = invoke(fn)
        named = [line for line in got if all(w in line for w in words)]
        assert named, (name, words, got)
        records.append(dict(family=family, plant=name, expected_words=words, named_failures=named))
for entry in registry(base):
    if entry["status"] != "held":
        continue
    def plant(inp):
        plant_field(inp, entry["probe"])
        inp.texts[DOC] = regenerated(inp.table, inp.texts[DOC])
    got = st.in_memory(base, plant)
    named = [line for line in got if all(w in line for w in entry["probe"]["words"])]
    assert named, entry["path"]
    records.append(dict(family="field", plant=entry["path"], named_failures=named))
assert len(records) == 231
write("named-plants.json", records)
print("PASS: merge provenance; repaired/idempotent generated references; regenerated trace records; 226 public execution tags; fresh local tag; omitted tag refusal; 231 named plants.")
