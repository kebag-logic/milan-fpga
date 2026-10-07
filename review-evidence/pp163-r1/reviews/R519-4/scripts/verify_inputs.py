#!/usr/bin/env python3
"""Independently bind every published input component to bytes and replay the chain.

Usage: python3 scripts/verify_inputs.py PROCESSOR_CLONE PACKET
Run fetch_public.py and fetch_sources.py first. All disposable files remain in scratch.
No synthesis, source edits, or source checkout writes are performed.
"""
import argparse
import collections
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys

HEAD = "c4539ff107a6a4c7d2e4a4844182b00a2bf33c82"
TREE = "4378652558345d65dd87efd4f092f41f413226c8"
DIGEST = "24ba6a244a83a0b764e6de5131a9c94752135f01ecab5afad83258c7b4767be1"


def sha(data):
    return hashlib.sha256(data).hexdigest()


def chain(rows, generics, images):
    # Use independently recomputed binary file hashes, never the advertised values.
    payload = bytearray()
    for row in rows:
        payload.extend(row["name"].encode())
        payload.append(0)
        payload.extend(bytes.fromhex(row["computed_sha256"]))
    for generic in generics:
        payload.extend(generic.encode() + b"\0")
    for image in sorted(images, key=lambda item: Path(item["path"]).name):
        payload.extend(Path(image["path"]).name.encode() + b"\0")
        payload.extend(image["sha256"].encode() + b"\0")
    return sha(payload)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("packet", type=Path)
    args = parser.parse_args()
    source, packet = args.source.resolve(), args.packet.resolve()
    out = packet / "receipts"
    scratch = packet / "scratch"
    public = out / "public/author-r3/measurement-m3final"
    evidence = public / "inputs-digest"
    parent = scratch / "parent-sources"
    git = lambda *a: subprocess.check_output(["git", "-C", str(source), *a], text=True).strip()
    assert git("rev-parse", "HEAD") == HEAD
    assert git("rev-parse", "HEAD^{tree}") == TREE
    components = json.loads((evidence / "inputs-components.json").read_text())
    images = json.loads((evidence / "baseline_images.json").read_text())
    record = json.loads((public / "record-m3final.stdout").read_text())
    assert components["recorded_inputs_sha256"] == record["inputs_sha256"] == DIGEST
    assert (evidence / "baseline_images.json").read_bytes() == (public / "ooc-m3final/baseline_images.json").read_bytes()
    assert len(components["files"]) == 124
    rows = []
    for order, row in enumerate(components["files"], 1):
        assert row["order"] == order
        name, path = row["name"], row["path"]
        assert Path(path).name == name
        git_blob = None
        if path.startswith("$ROOT1/protocol-processor/"):
            rel = path.removeprefix("$ROOT1/protocol-processor/")
            local = source / rel
            data = subprocess.check_output(["git", "-C", str(source), "show", f"{HEAD}:{rel}"])
            assert data == local.read_bytes(), rel
            git_blob = git("rev-parse", f"{HEAD}:{rel}")
            origin = "exact_processor_head"
        elif path.startswith("$ROOT1/"):
            local = parent / path.removeprefix("$ROOT1/")
            data = local.read_bytes()
            origin = "recorded_parent_or_dependency_revision"
        elif path == "$ROOT0/alinx_ax7101.v":
            local = evidence / "inputs/alinx_ax7101.normalized.v"
            data = local.read_bytes()
            assert row["normalized"] is True
            assert re.sub(rb"//[^\n]*", b"", data) == data
            origin = "published_normalized_top"
        elif path == "$ROOT2/clock.xdc":
            local = public / "ooc-m3final/clock.xdc"
            data = local.read_bytes()
            assert data == b"create_clock -period 20.000 -name clk [get_ports clk_i]\n"
            origin = "published_clock_derived_from_50MHz"
        else:
            assert order in (117, 118, 119)
            local = evidence / "inputs" / name
            data = local.read_bytes()
            origin = "published_non_tree_input"
        if order != 120:
            assert row["normalized"] is False
        computed = sha(data)
        assert computed == row["component_sha256"], (order, name, computed, row["component_sha256"])
        rows.append(dict(order=order, name=name, public_path=path, origin=origin,
                         bytes=len(data), computed_sha256=computed,
                         expected_sha256=row["component_sha256"], git_blob=git_blob, match=True))

    # Read source order and generic values from the published recipe independently.
    recipe = (public / "ooc-m3final/baseline_ooc.tcl").read_text()
    read_paths = []
    for line in recipe.splitlines():
        fields = line.split()
        if fields and fields[0] in ("read_verilog", "read_xdc", "source"):
            read_paths.append(fields[-1].strip("{}"))
    headers = json.loads((out / "source-fetch.json").read_text())["include_headers"]
    names = [Path(x).name for x in read_paths] + [Path(x).name for x in headers]
    assert names == [r["name"] for r in rows]
    public_roots = {
        "$VALIDATION_STORAGE/pp163-a553/meas/ax7101/gateware": "$ROOT0",
        "$VALIDATION_STORAGE/pp163-a553/parent": "$ROOT1",
    }
    normalized_paths = []
    for path in read_paths:
        for old, new in public_roots.items():
            path = path.replace(old, new)
        if path == "clock.xdc":
            path = "$ROOT2/clock.xdc"
        normalized_paths.append(path)
    normalized_paths += ["$ROOT1/" + h for h in headers]
    assert normalized_paths == [r["public_path"] for r in rows]
    generic_strings = []
    for part in recipe.split("-generic {")[1:]:
        value = part.split("}", 1)[0]
        key, val = value.split("=", 1)
        if val.startswith('"'):
            val = '"' + Path(val.strip('"')).name + '"'
        generic_strings.append(key + "=" + val)
    assert generic_strings == components["generics"]
    params = json.loads((public / "ooc-m3final/baseline_parameters.json").read_text())
    assert generic_strings == [f'{k}="{Path(v).name}"' if isinstance(v, str) else f"{k}={v}" for k, v in params.items()]
    assert len(generic_strings) == 21 and len(images) == 6
    independent_digest = chain(rows, generic_strings, images)
    assert independent_digest == DIGEST

    # Restore a relocatable measurement layout and execute the actual recorded-parent
    # gate function. The public normalized top is intentionally already normalized.
    generated = scratch / "replay-generated"
    measure = scratch / "replay-ooc"
    generated.mkdir(exist_ok=True)
    measure.mkdir(exist_ok=True)
    shutil.copyfile(evidence / "inputs/alinx_ax7101.normalized.v", generated / "alinx_ax7101.v")
    shutil.copyfile(public / "ooc-m3final/clock.xdc", measure / "clock.xdc")
    shutil.copyfile(evidence / "baseline_images.json", measure / "baseline_images.json")
    pp_link = parent / "protocol-processor"
    if pp_link.is_symlink():
        assert pp_link.resolve() == source
    else:
        assert not pp_link.exists()
        pp_link.symlink_to(source, target_is_directory=True)
    relocated = recipe.replace("$VALIDATION_STORAGE/pp163-a553/parent", str(parent))
    relocated = relocated.replace("$VALIDATION_STORAGE/pp163-a553/meas/ax7101/gateware", str(generated))
    relocated = relocated.replace("$WORKSPACE_HOME/litex-milan/pythondata-cpu-vexiiriscv/pythondata_cpu_vexiiriscv/verilog", str(evidence / "inputs"))
    (measure / "baseline_ooc.tcl").write_text(relocated)
    sys.dont_write_bytecode = True
    sys.path.insert(0, str(parent / "syn/ooc"))
    spec = importlib.util.spec_from_file_location("recorded_gate", parent / "syn/ooc/pp_resource_gate.py")
    gate = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(gate)
    paths, _ = gate.located(measure, relocated)
    assert [p.name for p in paths] == names
    actual_gate_digest = gate.inputs(measure, relocated)
    assert actual_gate_digest == DIGEST
    replay = subprocess.run([sys.executable, str(evidence / "replay_inputs.py"),
                             str(evidence / "inputs-components.json"), str(evidence / "baseline_images.json")],
                            text=True, capture_output=True, check=True)
    assert replay.stdout.strip() == DIGEST + " match"
    (out / "published-replay.stdout").write_text(replay.stdout)
    (out / "published-replay.rc").write_text(str(replay.returncode) + "\n")

    # Six independently chosen perturbations demonstrate ordered byte coverage.
    mutations = {}
    changed = copy.deepcopy(rows)
    changed[0]["computed_sha256"] = sha(b"deliberately different source")
    mutations["changed_component"] = chain(changed, generic_strings, images)
    mutations["omitted_component"] = chain(rows[:-1], generic_strings, images)
    mutations["reordered_components"] = chain([rows[1], rows[0], *rows[2:]], generic_strings, images)
    mutations["changed_generic"] = chain(rows, ["TDATA_WIDTH_P=32", *generic_strings[1:]], images)
    changed_images = copy.deepcopy(images)
    changed_images[0]["sha256"] = "0" * 64
    mutations["changed_image_identity"] = chain(rows, generic_strings, changed_images)
    top_path = generated / "alinx_ax7101.v"
    original_top = top_path.read_bytes()
    try:
        top_path.write_bytes(original_top + b"\n")
        mutations["actual_gate_changed_normalized_top"] = gate.inputs(measure, relocated)
    finally:
        top_path.write_bytes(original_top)
    assert all(value != DIGEST for value in mutations.values())
    assert gate.inputs(measure, relocated) == DIGEST
    result = dict(head=HEAD, tree=TREE, recorded_inputs_sha256=DIGEST,
                  independent_inputs_sha256=independent_digest,
                  recorded_parent_gate_inputs_sha256=actual_gate_digest,
                  counts=dict(collections.Counter(r["origin"] for r in rows)),
                  components=124, generics=21, images=6,
                  recipe_order_and_paths_match=True, parameter_table_match=True,
                  published_replay_match=True, components_detail=rows,
                  negative_controls={key:dict(digest=val, detected=True) for key, val in mutations.items()},
                  image_limit="The six image identities are replayed from the published manifest; this is not a firmware rebuild or synthesis rerun.")
    (out / "independent-inputs.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({k: v for k, v in result.items() if k != "components_detail"}, indent=2))


if __name__ == "__main__":
    main()
