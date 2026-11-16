#!/usr/bin/env python3
"""Reviewer probe (R847-1, PR #931): plant reviewer-chosen defects into a COPY of the
firmware tree, one at a time, using the AECP campaign's own build (aecp_mutants.campaign's
Tree and aecp_arms.core_arm, app mode at two interfaces), and report which tests fail.

Usage: python3 -B r847_probe_mutants.py <checkout> <output-dir> [--jobs N] [--only NAME]
Exit 0 always (it reports; the reviewer grades). Writes <output-dir>/probes.json and one log per probe.
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from pathlib import Path

PROBES = (
    # name, file under sw/firmware/ctrl, old (exactly one site), new, gtest filter
    ("restore-loop2-unmoved-dropped", "aecp/aecp_maps.c",
     "\t\tif (m->configuration == a->configuration && !unmoved(a, m) && commit(a, m, false, false) != AECP_SUCCESS) {",
     "\t\tif (m->configuration == a->configuration && commit(a, m, false, false) != AECP_SUCCESS) {",
     "Core.*:Face.*:AppStore.*"),
    ("kept-length-boundary", "aecp/aecp_maps.c",
     "\treturn d != NULL && d->length >= 82u && r->channel < channels(wire_be64(d->value + 74));",
     "\treturn d != NULL && d->length > 82u && r->channel < channels(wire_be64(d->value + 74));",
     "Core.*:Face.*:AppStore.*"),
    ("face-finish-dropped", "aecp/aecp_face.c",
     "\t(void)beat(f, request, FINISH, 0u, 1u, 2u, &ok);\n\treturn AECP_SUCCESS;",
     "\treturn AECP_SUCCESS;",
     "Face.*"),
    ("face-unanswered-commit-begin-trusted", "aecp/aecp_face.c",
     "\t\tstatus = !beat(f, request, COMMIT, 0u, 1u, 2u, &ok) ? AECP_ENTITY_MISBEHAVING",
     "\t\tstatus = !beat(f, request, COMMIT, 0u, 1u, 2u, &ok) ? AECP_SUCCESS",
     "Face.*"),
    ("face-pick-ignored", "aecp/aecp_face.c",
     "\tconst uint8_t *r = records + 8u * (pick != NULL ? pick[k] : k);",
     "\tconst uint8_t *r = records + 8u * (pick != NULL ? k : k);",
     "Core.*:Face.*:AppStore.*"),
    ("face-apply-record-zero", "aecp/aecp_face.c",
     "\t\t(void)record(f, request, APPLY, records, pick, k, &ok);",
     "\t\t(void)record(f, request, APPLY, records, pick, 0u, &ok);",
     "Face.*"),
)


def failed_tests(log: str) -> list[str]:
    return sorted(set(re.findall(r"^\[  FAILED  \] (\w+\.\w+) \(", log, re.M)))


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("checkout", type=Path)
    ap.add_argument("output", type=Path)
    ap.add_argument("--jobs", type=int, default=4)
    ap.add_argument("--only", default=None)
    args = ap.parse_args()
    test_dir = (args.checkout / "sw/firmware/ctrl/test").resolve()
    sys.path.insert(0, str(test_dir))
    sys.path.insert(0, str((args.checkout / "sw/firmware/gtest").resolve()))
    import aecp_arms  # noqa: E402
    import fw_gtest  # noqa: E402
    from ctrl_build import CTRL, ROOT, STACK, Tree, Refusal  # noqa: E402
    root = args.output.resolve()
    root.mkdir(parents=True, exist_ok=True)
    src = root / "work/ctrl"
    shutil.copytree(CTRL, src, dirs_exist_ok=True, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
    shutil.copytree(CTRL.parent / "ctrl_nvm", src.parent / "ctrl_nvm", dirs_exist_ok=True,
                    ignore=shutil.ignore_patterns("test", "__pycache__", "*.pyc"))
    tree = Tree(src, root / "work/build", root / "work/reuse", fw_gtest.Build(jobs=args.jobs), STACK)
    config = ROOT / "configs/endstation_ax7101_1x1_tdm8.yaml"
    receipts = []
    for name, path, old, new, selected in (("control-unplanted", "", "", "", "Core.*:Face.*:AppStore.*"), *PROBES):
        if args.only and name != args.only and name != "control-unplanted":
            continue
        target = src / path if path else None
        original = target.read_text() if target else None
        if target is not None:
            if original.count(old) != 1:
                receipts.append({"probe": name, "error": f"sites {original.count(old)}"})
                continue
            target.write_text(original.replace(old, new))
        try:
            result = aecp_arms.core_arm(tree, config, 2, "app", selected)
            log, rc = result.log, result.rc
        except Refusal as error:
            log, rc = str(error), -1
        finally:
            if target is not None:
                target.write_text(original)
        fails = failed_tests(log)
        (root / f"{name}.log").write_text(log)
        receipts.append({"probe": name, "file": path, "filter": selected, "rc": rc, "failed": fails,
                         "caught": bool(fails) if path else None})
        print(f"[{name}] rc={rc} failed={fails}", flush=True)
        (root / "probes.json").write_text(json.dumps(receipts, indent=2) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
