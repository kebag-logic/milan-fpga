#!/usr/bin/env python3
"""Reviewer probe: run the extracted production manifest validator on real commits.

Usage: python3 -I probe_validate.py <probe_manifest.py> <checkout> <commit> <act_ci.py copy>...
For each runner copy, lists the commit's gitlinks with `ls-tree -r` exactly as the
runner does, calls validate_submodule_manifest(), and prints ACCEPT or REFUSE <reason>.
"""
import importlib.util, pathlib, sys
spec = importlib.util.spec_from_file_location("probe", sys.argv[1])
probe = importlib.util.module_from_spec(spec); spec.loader.exec_module(probe)
probe.NAMES -= {"selftest_submodule_manifest", "selftest_lwsrp_manifest"}
checkout, commit = pathlib.Path(sys.argv[2]).resolve(), sys.argv[3]
for runner in sys.argv[4:]:
    probe.MODULE = m = probe.build(pathlib.Path(runner).read_text(encoding="utf-8"))
    tree = m.git_capture(checkout, ["ls-tree", "-r", commit], home=checkout.parent, description="tree")
    links = [l.split("\t", 1)[-1] for l in tree.splitlines() if l.startswith("160000 ")]
    try:
        m.validate_submodule_manifest(checkout, commit, links)
        verdict = "ACCEPT"
    except m.Refusal as exc:
        verdict = f"REFUSE {exc}"
    print(f"{pathlib.Path(runner).name} @ {commit[:12]} gitlinks={len(links)}: {verdict}")
