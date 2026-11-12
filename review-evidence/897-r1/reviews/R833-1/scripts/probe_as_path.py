# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Reviewer probe for #897 / PR #898: the GET_AS_PATH face read.

Usage: python3 -B probe_as_path.py <repo checkout> <output dir> [--jobs N]

1. Clean arms at the reviewed head: the AECP application arm at one and two
   interfaces (every test), and the platform boot arm at one and two.
2. The author's nine AECP plants and one platform plant, each by name, through
   the repository's own planting and catch rules (aecp_mutants.caught,
   ctrl_mutants.caught).
3. Reviewer-own plants on aecp_face.c path(), each required caught by at least
   one failing test in the app arm at two interfaces (any test, any words), so
   an escape names a rule no test pins.
Every planted copy lives under <output dir>/work; the checkout is not written.
"""
from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

repo = Path(sys.argv[1]).resolve()
out = Path(sys.argv[2]).resolve()
jobs = int(sys.argv[sys.argv.index("--jobs") + 1]) if "--jobs" in sys.argv else 8
sys.path.insert(0, str(repo / "sw/firmware/ctrl/test"))
sys.path.insert(0, str(repo / "sw/firmware/gtest"))

import aecp_arms  # noqa: E402
import aecp_mutants  # noqa: E402
import ctrl_mutants  # noqa: E402
import fw_gtest  # noqa: E402
import plat_arms  # noqa: E402
from ctrl_build import CTRL, ROOT, STACK, Tree, Outcome, Refusal  # noqa: E402

assert CTRL.resolve().is_relative_to(repo), CTRL
out.mkdir(parents=True, exist_ok=True)
config = ROOT / "configs/endstation_ax7101_1x1_tdm8.yaml"
receipts: dict = {"clean": {}, "author_aecp": [], "author_plat": [], "reviewer": []}


def fresh(name: str) -> Path:
    """A planted-copy tree of sw/firmware/ctrl and its ctrl_nvm sibling."""
    root = out / "work" / name
    if root.exists():
        shutil.rmtree(root)
    src = root / "ctrl"
    shutil.copytree(CTRL, src, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
    shutil.copytree(CTRL.parent / "ctrl_nvm", root / "ctrl_nvm",
                    ignore=shutil.ignore_patterns("test", "__pycache__", "*.pyc"))
    return src


build = fw_gtest.Build(jobs=jobs)


def tree_of(src: Path, tag: str) -> Tree:
    return Tree(src, out / "build" / tag, out / "reuse", build, STACK)


def save(name: str, result: Outcome) -> None:
    (out / "logs").mkdir(parents=True, exist_ok=True)
    (out / "logs" / (name + ".log")).write_text(result.log)


def flush() -> None:
    (out / "results.json").write_text(json.dumps(receipts, indent=2) + "\n")


# ---- 1. clean arms --------------------------------------------------------
clean = fresh("clean")
for label, fn in (("app-if1", lambda t: aecp_arms.core_arm(t, config, 1, "app")),
                  ("app-if2", lambda t: aecp_arms.core_arm(t, config, 2, "app")),
                  ("platboot1", lambda t: plat_arms.arm_platboot(t, 1)),
                  ("platboot2", lambda t: plat_arms.arm_platboot(t, 2))):
    try:
        r = fn(tree_of(clean, "clean-" + label))
    except Refusal as e:
        r = Outcome(label, 2, f"refused: {e}")
    save("clean-" + label, r)
    receipts["clean"][label] = {"rc": r.rc, "passed_line": [ln for ln in r.log.splitlines() if "verdict" in ln or "PASSED" in ln][-3:]}
    print(f"[clean] {label}: rc {r.rc}", flush=True)
    flush()

# ---- 2. the author's plants -----------------------------------------------
NEW_AECP = ("face-as-path-count-read-as-avb-info", "face-as-path-entries-at-one-ordinal",
            "face-as-path-through-the-first-interface", "face-as-path-truncated-at-its-bound",
            "face-as-path-bound-off-by-one", "face-as-path-count-unanswered-ignored",
            "face-as-path-entry-unanswered-ignored", "face-as-path-change-notifies-avb-info",
            "face-as-path-change-on-the-first-interface")
aecp_mutants.controls()  # the whole table names every test (raises on drift)
table = {d.name: d for d in aecp_mutants.DEFECTS}
assert all(n in table for n in NEW_AECP)


def plant_and_run(name: str, path: str, old: str, new: str, tests: str, interfaces: int = 2) -> Outcome:
    src = fresh(name)
    target = src / path
    text = target.read_text()
    if text.count(old) != 1:
        return Outcome(name, 2, f"refused: {text.count(old)} planting sites")
    target.write_text(text.replace(old, new))
    try:
        return aecp_arms.core_arm(tree_of(src, "m-" + name), config, interfaces, "app", tests)
    except Refusal as e:
        return Outcome(name, 2, f"refused: {e}")


for name in NEW_AECP:
    d = table[name]
    r = plant_and_run(name, d.path, d.old, d.new, ":".join(t for t, _ in d.checks))
    save("aecp-" + name, r)
    ok = all(aecp_mutants.caught(t, w, r) for t, w in d.checks)
    receipts["author_aecp"].append({"name": name, "checks": d.checks, "rc": r.rc, "caught": ok})
    print(f"[{'ok' if ok else 'ESCAPED'}] {name}", flush=True)
    flush()

plat = [m for m in ctrl_mutants.MUTANTS if m.name == "plat-as-path-unavailable"]
assert len(plat) == 1
m = plat[0]
src = fresh("plat-as-path-unavailable")
target = src / m.path
text = target.read_text()
assert text.count(m.old) == 1
target.write_text(text.replace(m.old, m.new))
missed = []
for arm, test, needle in m.kills():
    n = int(arm[-1])
    try:
        r = plat_arms.arm_platboot(tree_of(src, f"m-plat-{arm}"), n)
    except Refusal as e:
        r = Outcome(arm, 2, f"refused: {e}")
    save(f"plat-as-path-unavailable-{arm}", r)
    if not ctrl_mutants.caught(test, needle, r):
        missed.append(arm)
receipts["author_plat"].append({"name": m.name, "kills": m.kills(), "missed": missed})
print(f"[{'ok' if not missed else 'ESCAPED'}] plat-as-path-unavailable {missed}", flush=True)
flush()

# ---- 3. reviewer-own plants on path() --------------------------------------
COUNT = aecp_mutants.AS_PATH_COUNT
ENTRY = aecp_mutants.AS_PATH_ENTRY
OWN = (
    ("r-entry-selector-9", ENTRY, ENTRY.replace("8u, k, 0u", "9u, k, 0u")),
    ("r-count-selector-1", COUNT, COUNT.replace("index, 0u, 0u, 0u, &n", "index, 1u, 0u, 0u, &n")),
    ("r-count-low-16-bits", COUNT, COUNT.replace("&n) || n > capacity", "&n) || (n &= 0xFFFFu, n > capacity)")),
    ("r-entries-into-slot-0", ENTRY, ENTRY.replace("&out[k]", "&out[0]")),
    ("r-count-not-reported", "\t*count = (size_t)n;\n", "\t(void)count;\n"),
    ("r-count-type-stream-input", COUNT, COUNT.replace("2u, AVB_INTERFACE, index, 0u", "2u, 5u, index, 0u")),
    ("r-entry-index-0", ENTRY, ENTRY.replace("AVB_INTERFACE, index, 8u", "AVB_INTERFACE, 0u, 8u")),
    ("r-entry-ordinal-plus-1", ENTRY, ENTRY.replace("8u, k, 0u", "8u, k + 1u, 0u")),
    ("r-last-entry-skipped", "\tfor (unsigned k = 0; k < (unsigned)n; ++k) {\n",
     "\tfor (unsigned k = 0; k + 1u < (unsigned)n; ++k) {\n"),
)
for name, old, new in OWN:
    r = plant_and_run(name, "aecp/aecp_face.c", old, new, "Face.*:AppFace.*")
    save(name, r)
    fails = [ln for ln in r.log.splitlines() if ln.startswith("[  FAILED  ]") and "(" in ln]
    ok = r.rc == 1 and bool(fails)
    receipts["reviewer"].append({"name": name, "old": old, "new": new, "rc": r.rc, "caught": ok,
                                 "failed_tests": sorted(set(ln.split("]")[1].split("(")[0].strip() for ln in fails))})
    print(f"[{'ok' if ok else 'ESCAPED'}] {name}: {len(fails)} failing test line(s)", flush=True)
    flush()

shutil.rmtree(out / "work", ignore_errors=True)
print("PROBE DONE", flush=True)
