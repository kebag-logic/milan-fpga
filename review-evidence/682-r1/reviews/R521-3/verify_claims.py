#!/usr/bin/env python3
"""Verify the round's documentary claims without rebuilding the product."""
import copy
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

root = Path.cwd()
packet = Path(__file__).resolve().parent
env = dict(os.environ, GIT_NO_REPLACE_OBJECTS="1")
old = "ead8036035affd53ef4b29979190f2f4f67084c0"
pin = "2ad2f845dd583f8310075fa2380cb60a04fd091a"
base = "e21c1ca024d37ea188ad15b5c8f9c2dae18628df"

def git(*args, sub=False):
    cwd = root / "protocol-processor" if sub else root
    return subprocess.check_output(["git", "-C", str(cwd), *args], env=env)

top = "hdl/top/protocol_processor_top.sv"
top_old, top_new = (git("show", rev + ":" + top, sub=True) for rev in (old, pin))
assert top_old == top_new
merges = {}
for number in (156, 159, 160, 161, 162, 164):
    public = json.loads((packet / "scratch" / f"processor-pr-{number}.json").read_text())
    merge = public["merge_commit_sha"]
    git("merge-base", "--is-ancestor", merge, pin, sub=True)
    merges[str(number)] = dict(merge=merge, title=public["title"], url=public["html_url"])
interface = "docs/architecture/02_interfaces.md"
prior_interface = git("show", old + ":" + interface, sub=True).decode()
assert "**synchronous and active low**" in prior_interface
git("merge-base", "--is-ancestor", "371505db", "b0a74196", sub=True)
git("merge-base", "--is-ancestor", "b0a74196", old, sub=True)

ledger = {}
for line in (root / "syn/yosys/rom_digests.tsv").read_text().splitlines():
    if line and not line.startswith("#"):
        revision, name, digest = line.split()
        if revision in (old, pin):
            ledger.setdefault(revision, {})[name] = digest
assert ledger[old] == ledger[pin]
assert len(ledger[pin]) == 2

baseline = json.loads((root / "syn/ooc/pp_resource_baseline.json").read_text())
original = json.loads(git("show", base + ":syn/ooc/pp_resource_baseline.json"))
assert (root / "syn/ooc/pp_resource_baseline.json").read_bytes() == (packet / "scratch/round2-baseline-F.json").read_bytes()
sys.path.insert(0, str(root / "syn/ooc"))
import pp_resource_gate
flow_checks = {}
for name, entry in baseline["endpoints"].items():
    identity = entry["record"]["identity"]
    assert identity["flow"][0] == "set_param synth.maxThreads 1"
    assert "set_param general.maxThreads 32" in identity["flow"]
    assert "Combination F" in entry["measured"]
    for policy in ("tolerance", "floor", "ceiling"):
        assert entry.get(policy) == original["endpoints"][name].get(policy)
    identical = copy.deepcopy(entry["record"])
    control, _ = pp_resource_gate.judge(entry, identical, [])
    assert control == 0
    altered = copy.deepcopy(identical)
    altered["identity"]["flow"].remove("set_param synth.maxThreads 1")
    refusal, messages = pp_resource_gate.judge(entry, altered, [])
    assert refusal == 2 and "flow" in messages[0]
    flow_checks[name] = dict(identity=identity, control=control,
                            missing_cap=refusal, diagnostic=messages,
                            policies_unchanged=True)

recipe = (root / "docs/testing/PP_SHADOW_BASELINE_RECIPE.md").read_text().replace("\\\n", " ")
preparations = [line.strip() for line in recipe.splitlines()
                if line.strip().startswith("python3 syn/ooc/pp_baseline.py ")
                and "--selftest" not in line]
assert len(preparations) == 5
assert all("--single-thread-synthesis" in line for line in preparations)
assert "Use `--integrated-clock` for every standalone endpoint the gate judges." in recipe

equal_scopes = ["sw/firmware/milan_baremetal", "tb/verilator/nvm_capture_cpu", "hdl", "configs"]
for scope in equal_scopes:
    assert not git("diff", "--name-only", base, "HEAD", "--", scope)
measurement = json.loads((root / "tb/verilator/nvm_capture_cpu/measurements.json").read_text())
assert measurement["product_firmware_sha256"] == hashlib.sha256((root / "sw/firmware/milan_baremetal/milan_baremetal.c").read_bytes()).hexdigest()
for name in ("round2-render-adopted-clean-epoch.log", "round2-render-prior-clean-epoch.log"):
    raw = (packet / "scratch" / name).read_bytes()
    assert len(raw) == 3746
    assert hashlib.sha256(raw).hexdigest() == "3ef42e34ca3874e90fd2929f869dd0f37343e04b9cb2cb0c5f294262448c1c6b"

print(json.dumps(dict(processor_top_sha256=hashlib.sha256(top_new).hexdigest(),
    processor_top_identical=True, merged_prs=merges,
    reset_attribution=dict(change="371505db", merge="b0a74196", already_present_at=old),
    rom_rows=ledger, resource_record_matches_public_F=True,
    endpoint_flow_controls=flow_checks, recipe_preparations=preparations,
    unchanged_product_scopes=equal_scopes,
    capture_firmware_sha256=measurement["product_firmware_sha256"],
    capture_maxima=measurement["maxima"],
    public_render_clean_epoch_identical=True), indent=2))
