#!/usr/bin/env python3
"""Compare only five shipping exports and emitted source lists at three heads."""
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

root, packet = (Path(arg).resolve() for arg in sys.argv[1:])
scratch = packet / "scratch"
revisions = ("42f654478c11bd8f2b070969d83140587190f276",
             "ba57a3bc5", "3880c1eb6e2f927a07f98150d5b05a228f8f4efd")
submodules = ("protocol-processor", "gptp-processor", "third_party/verilog-axis")
env = {**os.environ, "PYTHONDONTWRITEBYTECODE": "1", "TMPDIR": str(scratch)}


def run(command, cwd, log):
    result = subprocess.run(command, cwd=cwd, env=env, stdout=log, stderr=subprocess.STDOUT, timeout=300)
    assert result.returncode == 0, command


def examine(revision):
    tree = scratch / ("compare-" + revision[:8])
    raw = scratch / ("compare-" + revision[:8] + ".raw.log")
    with raw.open("w") as log:
        if not tree.exists():
            run(["git", "clone", "--shared", "--no-checkout", str(root), str(tree)], scratch, log)
            run(["git", "checkout", "--detach", revision], tree, log)
            for sub in submodules:
                run(["git", "config", "submodule." + sub + ".url", str(root / sub)], tree, log)
            run(["git", "-c", "protocol.file.allow=always", "submodule", "update", "--init", *submodules], tree, log)
        assert subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=tree).decode().startswith(revision)
        out = scratch / ("exports-" + revision[:8])
        for config in sorted((tree / "configs").glob("endstation_*.yaml")):
            run([sys.executable, "sw/builder/endstation_builder.py", str(config), "-o", str(out)], tree, log)
            run([sys.executable, "avdecc/gen_aemi_image.py", "--overlay",
                 str(out / config.stem / "aem_overlay.json"), "--line-bytes", "576",
                 "-o", str(out / config.stem / "aem_desc.bin")], tree, log)
        sources = {}
        for top in ("milan_datapath", "KL_pp_shadow"):
            emitted = subprocess.check_output(["bash", "syn/yosys/run.sh", "--emit", top], cwd=tree, env=env)
            sources[top] = emitted.decode().replace(str(tree), "$REPO")
        source_hashes = {}
        for record in sources.values():
            for line in record.splitlines():
                if line.startswith("src="):
                    name = line[4:].replace("$REPO/", "")
                    source_hashes[name] = hashlib.sha256((tree / name).read_bytes()).hexdigest()
        artifacts = {str(path.relative_to(out)): hashlib.sha256(path.read_bytes()).hexdigest()
                     for path in sorted(out.rglob("*")) if path.is_file()}
    text = raw.read_text().replace(str(root), "$REPO").replace(str(packet), "$PACKET")
    (packet / "receipts" / ("compare-" + revision[:8] + ".log")).write_text(text)
    print(json.dumps({"revision": revision, "export_files": len(artifacts), "rc": 0}), flush=True)
    return {"revision": revision, "artifacts": artifacts, "source_lists": sources,
            "source_hashes": source_hashes}


with ThreadPoolExecutor(max_workers=3) as pool:
    results = list(pool.map(examine, revisions))
for result in results[1:]:
    assert result["artifacts"] == results[0]["artifacts"], "export bytes differ"
    assert result["source_lists"] == results[0]["source_lists"], "emitted lists differ"
delta = [name for name, value in results[-1]["source_hashes"].items()
         if value != results[0]["source_hashes"][name]]
assert delta == ["hdl/milan/KL_nvm_backend.sv"], delta
print(json.dumps({"all_export_bytes_equal": True, "all_source_lists_equal": True,
                  "files_per_revision": len(results[0]["artifacts"]), "changed_sources": delta}))
(packet / "receipts/build-comparison.json").write_text(json.dumps(results, indent=2) + "\n")
