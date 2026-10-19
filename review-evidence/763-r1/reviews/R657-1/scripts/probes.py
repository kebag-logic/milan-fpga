#!/usr/bin/env python3
"""Disposable fault probes for the #763 test: plant one edit into a scratch copy of the firmware tree and its
saved-state store, run the AECP app arm (two interfaces, the shipping 1x1 shape) with a GoogleTest filter, and
grade the named diagnostics with the campaign's own reader.

usage: probes.py <checkout> <work-dir> <out-dir> [probe ...]   (no probe names: all)
The checkout is only read; every copy, build and log is under <work-dir> and <out-dir>."""
from __future__ import annotations

import json
import shutil
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

checkout, work, out = (Path(a).resolve() for a in sys.argv[1:4])
sys.path[:0] = [str(checkout / "sw/firmware/ctrl/test"), str(checkout / "sw/firmware/gtest")]
import aecp_arms  # noqa: E402
import aecp_mutants  # noqa: E402
import fw_gtest  # noqa: E402
from ctrl_build import CTRL, Refusal, Tree  # noqa: E402

NEW = "Nvm.EmptyAndNonDefaultMapsSurviveTheRealStorePowerCycle"
FRAMING = "Nvm.WholeMapFramingAndEmptySetAreDistinct"
ACCEPTED = "Nvm.AcceptedStateSurvivesTheRealStorePowerCycle"
RESTORE = "\t\tunsigned status = aecp_map_restore(n->core, m, n->scratch, count);"
LATCH = "\tif (!s->latch(s->ctx, r.group, r.index, nvm_payload, r.plen))\n\t\treturn;"
TABLE = {d.name: d for d in aecp_mutants.DEFECTS}
M1, M2 = TABLE["nvm-empty-map-keeps-defaults"], TABLE["nvm-unused-payload-reads-erased"]

# name: (path, old, new, filter, [(test, words, expect_failure)], expect_rc)
PROBES = {
    "clean": (None, None, None, "Nvm.*", [], 0),
    "m1-table": (M1.path, M1.old, M1.new, "Nvm.*",
                 [(NEW, "the empty list survives the power cycle", True),
                  (FRAMING, "all UNUSED is an intentional empty set", True)], 1),
    "m2-table": (M2.path, M2.old, M2.new, "Nvm.*",
                 [(NEW, "the empty list survives the power cycle", True)], 1),
    "m2-gap-full-arm-without-new-test": (M2.path, M2.old, M2.new, "*:-" + NEW, [], 0),
    "m1-full-arm-without-new-test": (M1.path, M1.old, M1.new, "*:-" + NEW,
                                     [(FRAMING, "all UNUSED is an intentional empty set", True)], 1),
    "writer-skips-all-unused-payload": ("../ctrl_nvm/nvm_store.c", LATCH,
                                        "\tif (!s->latch(s->ctx, r.group, r.index, nvm_payload, r.plen) ||\n"
                                        "\t    nvm_all_erased(nvm_payload, r.plen))\n\t\treturn;", "Nvm.*",
                                        [(NEW, "the empty set is a framed record, not an erased one", True),
                                         (NEW, "the empty list survives the power cycle", True)], 1),
    "writer-skips-all-unused-payload-without-new-test": (
        "../ctrl_nvm/nvm_store.c", LATCH,
        "\tif (!s->latch(s->ctx, r.group, r.index, nvm_payload, r.plen) ||\n"
        "\t    nvm_all_erased(nvm_payload, r.plen))\n\t\treturn;", "*:-" + NEW, [], None),
    "output-only-empty-keeps-defaults": ("aecp/aecp_nvm.c", RESTORE,
                                         "\t\tif (count == 0 && group == NVM_G_MAPO) return NVM_APPLIED;\n" + RESTORE,
                                         "Nvm.*", [(NEW, "the empty list survives the power cycle", True)], 1),
    "input-only-empty-keeps-defaults": ("aecp/aecp_nvm.c", RESTORE,
                                        "\t\tif (count == 0 && group == NVM_G_MAPI) return NVM_APPLIED;\n" + RESTORE,
                                        "Nvm.*", [(NEW, "the empty list survives the power cycle", True)], 1),
    "nonempty-saved-map-ignored": ("aecp/aecp_nvm.c", RESTORE,
                                   "\t\tif (count != 0) return NVM_APPLIED;\n" + RESTORE, NEW,
                                   [(NEW, "the non-default list survives the power cycle", True)], 1),
}


def probe(name: str) -> dict:
    path, old, new, selected, checks, expect_rc = PROBES[name]
    root = work / name
    shutil.rmtree(root, ignore_errors=True)
    src = root / "ctrl"
    shutil.copytree(CTRL, src, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
    shutil.copytree(CTRL.parent / "ctrl_nvm", root / "ctrl_nvm",
                    ignore=shutil.ignore_patterns("test", "__pycache__", "*.pyc"))
    if path:
        target = src / path
        text = target.read_text()
        if text.count(old) != 1:
            return {"probe": name, "ok": False, "why": f"{text.count(old)} planting sites"}
        target.write_text(text.replace(old, new))
    tree = Tree(src, root / "build", root / "reuse", fw_gtest.Build(jobs=2))
    try:
        result = aecp_arms.core_arm(tree, checkout / "configs/endstation_ax7101_1x1_tdm8.yaml", 2, "app", selected)
    except Refusal as error:
        (out / f"{name}.log").write_text(str(error))
        return {"probe": name, "ok": False, "why": "refused"}
    (out / f"{name}.log").write_text(result.log)
    graded = [{"test": t, "words": w, "expect_failure": f, "caught": aecp_mutants.caught(t, w, result)}
              for t, w, f in checks]
    ok = (expect_rc is None or result.rc == expect_rc) and all(g["caught"] == g["expect_failure"] for g in graded)
    summary = [line for line in result.log.splitlines()
               if line.startswith(("[  FAILED  ] ", "[  PASSED  ]", "RESULT", "  verdict", "verdict"))]
    return {"probe": name, "filter": selected, "rc": result.rc, "expect_rc": expect_rc, "checks": graded,
            "ok": ok, "summary": summary}


def main() -> int:
    names = sys.argv[4:] or list(PROBES)
    out.mkdir(parents=True, exist_ok=True)
    with ThreadPoolExecutor(max_workers=2) as pool:
        results = list(pool.map(probe, names))
    (out / "probes.json").write_text(json.dumps(results, indent=2) + "\n")
    for r in results:
        print(f"[{'as-expected' if r['ok'] else 'UNEXPECTED'}] {r['probe']}: rc {r.get('rc')} {r.get('summary', r.get('why'))}")
    return 0 if all(r["ok"] for r in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
