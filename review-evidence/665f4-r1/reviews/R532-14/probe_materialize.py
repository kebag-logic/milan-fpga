#!/usr/bin/env python3
"""Reviewer probe: run the exact-head materialization command on a scratch clone.

Usage: python3 -I probe_materialize.py <probe_manifest.py> <act_ci.py copy> <superproject clone> <home>
Runs the extracted initialize_required_submodules() with the runner's git prefix
and environment (protocol.allow=never, HTTPS only, no credential helper), then
prints each gitlink's initialized state and the configured remote URL.
"""
import importlib.util, pathlib, subprocess, sys
spec = importlib.util.spec_from_file_location("probe", sys.argv[1])
probe = importlib.util.module_from_spec(spec); spec.loader.exec_module(probe)
probe.MODULE = probe.build(pathlib.Path(sys.argv[2]).read_text(encoding="utf-8"))
m = probe.MODULE
checkout, home = pathlib.Path(sys.argv[3]).resolve(), pathlib.Path(sys.argv[4]).resolve()
print("REQUIRED_SUBMODULES", list(m.REQUIRED_SUBMODULES))
print("prefix", m.git_prefix()[1:])
m.initialize_required_submodules(checkout, home)
print(subprocess.run(["git", "-C", str(checkout), "submodule", "status"], capture_output=True, text=True).stdout, end="")
for name, path, url in m.TRUSTED_SUBMODULES:
    cfg = subprocess.run(["git", "-C", str(checkout), "config", "--get", f"submodule.{name}.url"], capture_output=True, text=True).stdout.strip()
    populated = (checkout / path / ".git").exists()
    print(f"{path}: populated={populated} configured_url={cfg or '-'} trusted_url={url}")
