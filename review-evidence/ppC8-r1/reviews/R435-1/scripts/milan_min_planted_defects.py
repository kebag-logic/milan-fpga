#!/usr/bin/env python3
"""Reviewer-planted defects in hdl/aecp/desc/milan_min.json.

Each defect edits one named field (or appends bytes) of one descriptor of the
positive model in an isolated copy of the processor tree, then runs the
generator gate. With `rerecord` the copy's model_ids.json is also updated to
the edited model's digest, so only the LINT can catch the defect (the digest
record would otherwise catch any structural edit).

usage: milan_min_planted_defects.py <clean-processor-tree> <work-dir>
"""
import importlib.util
import json
import shutil
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

# id, (type, index), field name, new value, rerecord, what it plants
DEFECTS = [
    ("buf-short", ("STREAM_INPUT", 0), "buffer_length", 2125999, False,
     "Listener buffer_length 1 ns under Milan 5.3.3.4"),
    ("buf-short-rerec", ("STREAM_INPUT", 0), "buffer_length", 2125999, True,
     "the same, with the digest re-recorded"),
    ("talkers2-rerec", ("ENTITY", 0), "talker_stream_sources", 2, True,
     "ENTITY talker_stream_sources not the maximum"),
    ("emid-rerec", ("ENTITY", 0), "entity_model_id", "0x0000000000000000", True,
     "entity_model_id 0"),
    ("emid-norec", ("ENTITY", 0), "entity_model_id", "0x020000FFFE00C802", False,
     "a new entity_model_id not recorded"),
    ("ifflags-rerec", ("AVB_INTERFACE", 0), "interface_flags", 0, True,
     "AVB_INTERFACE interface_flags without GPTP/SRP_SUPPORTED (disclosed as not linted)"),
    ("ifflags-norec", ("AVB_INTERFACE", 0), "interface_flags", 0, False,
     "the same, digest record left as is"),
    ("caps-rerec", ("ENTITY", 0), "entity_capabilities", 0, True,
     "ENTITY entity_capabilities 0 (disclosed as not linted)"),
    ("cluster-ch2-rerec", ("AUDIO_CLUSTER", 1), "channel_count", 2, True,
     "a stereo AUDIO_CLUSTER"),
    ("srcloc-rerec", ("CLOCK_SOURCE", 1), "clock_source_location_index", 0, True,
     "the CRF input's source moved to the AAF input"),
    ("curfmt-rerec", ("STREAM_OUTPUT", 0), "current_format", "0x020702200080C000", True,
     "Talker current_format not in its list"),
    ("cluster-pad-rerec", ("AUDIO_CLUSTER", 0), "+pad", 4, True,
     "AUDIO_CLUSTER 0 four octets longer than IEEE 7.2.16's 90"),
]


def load(path):
    spec = importlib.util.spec_from_file_location("gen_desc_image", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def run(tree: Path, work: Path, defect) -> str:
    ident, (dtype, index), field, value, rerecord, what = defect
    copy = work / ident
    if copy.exists():
        shutil.rmtree(copy)
    shutil.copytree(tree, copy, ignore=shutil.ignore_patterns("obj_dir", "__pycache__"))
    desc = copy / "hdl/aecp/desc"
    model = json.loads((desc / "milan_min.json").read_text(encoding="utf-8"))
    row = next(r for r in model["descriptors"] if r["type"] == dtype and r["index"] == index)
    if field == "+pad":
        row["fields"].append({"name": "reviewer_pad", "size": value, "value": 0})
    else:
        hits = [f for f in row["fields"] if f.get("name") == field]
        if len(hits) != 1:
            return f"{ident} INVALID (field {field} found {len(hits)} times) | {what}"
        hits[0]["value"] = value
    (desc / "milan_min.json").write_text(json.dumps(model, indent=1), encoding="utf-8")
    if rerecord:
        gen = load(desc / "gen_desc_image.py")
        digest = gen.model_lint.lint(gen._grouped_descriptors(model)).digest
        ids = json.loads((desc / "model_ids.json").read_text(encoding="utf-8"))
        ent = next(r for r in model["descriptors"] if r["type"] == "ENTITY")
        emid = next(f["value"] for f in ent["fields"] if f["name"] == "entity_model_id")
        ids["models"] = {str(emid).upper().replace("0X", "0x"): digest}
        (desc / "model_ids.json").write_text(json.dumps(ids, indent=1), encoding="utf-8")
    proc = subprocess.run([sys.executable, "-B", "test_gen_desc_image.py"],
                          cwd=copy / "tb/desc_store", capture_output=True, text=True)
    tail = [ln for ln in proc.stderr.splitlines() if ln.startswith(("FAILED", "OK"))]
    (work / f"{ident}.log").write_text(proc.stderr, encoding="utf-8")
    shutil.rmtree(copy)
    verdict = "KILLED" if proc.returncode else "SURVIVED"
    return f"{ident} {verdict} {' '.join(tail)} | rerecord={rerecord} | {what}"


def main() -> int:
    tree, work = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
    work.mkdir(parents=True, exist_ok=True)
    with ThreadPoolExecutor(max_workers=12) as pool:
        for line in pool.map(lambda d: run(tree, work, d), DEFECTS):
            print(line, flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
