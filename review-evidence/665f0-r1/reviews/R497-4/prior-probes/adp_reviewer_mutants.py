#!/usr/bin/env python3
"""Reviewer probe (R496-3): plant extra defects in a COPY of the ADP core and
run the head's own adp and port arms on each; report which checks redden.

usage: adp_reviewer_mutants.py <exported head tree> <scratch dir>
"""
import pathlib, shutil, subprocess, sys

TREE = pathlib.Path(sys.argv[1]).resolve()
OUT = pathlib.Path(sys.argv[2]).resolve()
CTRL = "sw/firmware/ctrl"
SRC = ("mbx/mbx.c", "loop/ctrl_loop.c", "port/ctrl_pool.c", "port/ctrl_debug.c", "port/shlan_port.c",
       "adp/adp.c", "adp/adp_mbx.c", "app/ctrl_app.c", "host/mbx_model.c", "host/mbx_plat_host.c",
       "test/test_check.c")
INC = ("mbx", "wire", "host", "port", "loop", "adp", "app", "test")

M = {
    "queued-departing-keeps-first-index": ("adp/adp.c",
        "\ta->departing_owed--;\n\ta->departing_index = 0;\n", "\ta->departing_owed--;\n"),
    "poll-forgets-owed-available": ("adp/adp.c",
        "\treturn a->departing_owed != 0u || a->available_owed;\n}", "\treturn a->departing_owed != 0u;\n}"),
    "blocked-available-not-owed": ("adp/adp.c",
        "\ta->available_owed = true;\n\tif (a->departing_owed != 0u ||",
        "\tif (a->departing_owed != 0u) {\n\t\treturn;\n\t}\n\ta->available_owed = true;\n\tif ("),
    "poll-sends-two-frames": ("adp/adp.c",
        "\tif (a->departing_owed != 0u) {\n\t\tdepart(a);\n\t} else if (a->available_owed) {",
        "\tif (a->departing_owed != 0u) {\n\t\tdepart(a);\n\t}\n\tif (a->departing_owed == 0u && a->available_owed) {"),
    "gm-change-drops-owed-available": ("adp/adp.c",
        "\ta->gm_changed++;\n", "\ta->gm_changed++;\n\ta->available_owed = false;\n"),
    "second-shutdown-overwrites-index": ("adp/adp.c",
        "\t} else if (a->departing_owed != UINT32_MAX) {\n",
        "\t} else if (a->departing_owed != UINT32_MAX) {\n\t\ta->departing_index = index;\n"),
    "link-loss-keeps-owed-available": ("adp/adp.c",
        "\t\ta->available_owed = false;                              // an owed DEPARTING stays owed\n", ""),
    "link-loss-drops-owed-departing": ("adp/adp.c",
        "\t\ta->available_owed = false;                              // an owed DEPARTING stays owed\n",
        "\t\ta->available_owed = false;\n\t\ta->departing_owed = 0u;\n"),
}

def build_run(root: pathlib.Path, test: str, tag: str) -> tuple[int, str]:
    c = root / CTRL
    exe = OUT / f"{tag}_{test}"
    argv = ["gcc", "-std=c11", "-O2", "-Wall", "-Wextra", "-pedantic", *[f"-I{c / d}" for d in INC],
            *[str(c / s) for s in SRC], str(c / "test" / f"{test}.c"), "-o", str(exe)]
    b = subprocess.run(argv, capture_output=True, text=True)
    if b.returncode != 0:
        return 99, b.stderr
    r = subprocess.run([str(exe)], capture_output=True, text=True, timeout=600)
    return r.returncode, r.stdout + r.stderr

def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    for test in ("test_adp", "test_port_loop"):
        rc, log = build_run(TREE, test, "control")
        print(f"control {test}: rc={rc} {[l for l in log.splitlines() if 'checks:' in l]}")
    for name, (rel, old, new) in M.items():
        root = OUT / name
        if root.exists():
            shutil.rmtree(root)
        shutil.copytree(TREE / CTRL, root / CTRL)
        p = root / CTRL / rel
        s = p.read_text()
        if s.count(old) != 1:
            print(f"{name}: PATCH SITE NOT UNIQUE ({s.count(old)})")
            continue
        p.write_text(s.replace(old, new))
        for test in ("test_adp", "test_port_loop"):
            rc, log = build_run(root, test, name)
            fails = [l.strip() for l in log.splitlines() if "[FAIL]" in l]
            print(f"{name} {test}: rc={rc} fails={len(fails)}")
            for f in fails[:4]:
                print(f"    {f}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
