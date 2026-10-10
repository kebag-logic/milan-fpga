#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Reviewer-owned planted defects for lwSRP PR #18 (written independently of
tests/check_reversals.py). Each plant is applied in its own local clone under
the scratch directory; the reviewed checkout is never written.

Usage: r587_plants.py <lwSRP checkout> <unit framework prefix> <scratch> <receipt dir> [plant ...]
For each plant and each Registrar profile: build, run the unit runner (failing
test names), run tests/check_equivalence.py, and run the reviewer fuzz.
"""
import concurrent.futures as cf
import json
import os
import re
import subprocess
import sys
from pathlib import Path

MAD = "src/core/mrp_mad.c"
PLANTS = {
    # Split Message: a third value vector of a type opens a second Message.
    "P1-split-after-two": (MAD,
        "        v += size;\n    }\n    return tx_close(ops, buf, v);",
        "        v += size;\n        if (v - first == 2 * (long)size) {\n"
        "            buf = tx_close(ops, buf, v);\n            v = first = tx_open(ops, type, buf);\n"
        "        }\n    }\n    return tx_close(ops, buf, v);"),
    # Wrong EndMark count: MVRP/MMRP Messages lose their AttributeList EndMark.
    "P2-no-list-endmark-without-length": (MAD,
        "    end[0] = 0; end[1] = 0;\n    end += 2;\n    if (tx_header_len(ops) == 4u) {",
        "    if (tx_header_len(ops) == 4u) {\n        end[0] = 0; end[1] = 0;\n        end += 2;\n    }\n"
        "    if (tx_header_len(ops) == 4u) {"),
    # Wrong vector order: only the first FirstValue octet is compared.
    "P3-order-first-octet-only": (MAD,
        "memcmp(at - size + 2, at + 2, len) > 0", "memcmp(at - size + 2, at + 2, 1) > 0"),
    # Dropped vector: the list-head value is committed but not written.
    "P4-drop-list-head": (MAD,
        "if (!a->tx_selected || a->attr_type != type || e->tx == TX_MSG_NONE) {",
        "if (!a->tx_selected || a->attr_type != type || e->tx == TX_MSG_NONE || a == ps->attrs) {"),
    # LeaveAll vector written after the values instead of first.
    "P5-leaveall-last": (MAD,
        "    if (la) {\n        v[0] = 0x20; v[1] = 0;\n        memset(v + 2, 0, len);\n        v += 2u + len;\n    }\n"
        "    uint8_t *first = v;",
        "    uint8_t *first = v;"),
    # Messages in descending AttributeType order.
    "P6-descending-types": (MAD,
        "    for (unsigned type = 0; type < 256u; ++type) {\n        if (!tx_type_in(types->open, type)) {",
        "    for (unsigned type = 256u; type-- > 0;) {\n        if (!tx_type_in(types->open, type)) {"),
    # Sizing: the first vector of a type does not pay its EndMark.
    "P7-cost-misses-endmark": (MAD, "n += hdr + 2u;", "n += hdr;"),
    # Event semantics: values with no transmit message are written as well.
    "P8-write-none-values": (MAD,
        "if (!a->tx_selected || a->attr_type != type || e->tx == TX_MSG_NONE) {",
        "if (!a->tx_selected || a->attr_type != type) {"),
    # Receive: only the first VectorAttribute of each Message is delivered.
    "Q1-rx-first-vector-only": ("src/core/mrp_pdu.c",
        "            vector_seen = true;\n",
        "            if (vector_seen) {\n                continue;\n            }\n            vector_seen = true;\n"),
    # Receive: "+k" offsets are ignored; every value decodes as FirstValue.
    "Q2-rx-ignores-offset": ("src/core/mrp_pdu.c",
        "int r = ops->decode_attr(type, k, fv, alen, value);",
        "int r = ops->decode_attr(type, 0, fv, alen, value);"),
}
P5_TAIL = ("        v += size;\n    }\n    return tx_close(ops, buf, v);",
           "        v += size;\n    }\n    if (la) {\n        v[0] = 0x20; v[1] = 0;\n        memset(v + 2, 0, len);\n"
           "        v += 2u + len;\n    }\n    return tx_close(ops, buf, v);")


def sh(cmd, log, env=None, cwd=None, timeout=900):
    r = subprocess.run(cmd, cwd=cwd, env=env, capture_output=True, text=True, timeout=timeout)
    Path(log).write_text(" ".join(map(str, cmd)) + "\n" + r.stdout + r.stderr)
    return r.returncode, r.stdout + r.stderr


def run_plant(name, src, prefix, scratch, out, scripts):
    work = scratch / name
    tree = work / "tree"
    if tree.exists():
        subprocess.run(["rm", "-rf", str(work)], check=True)
    work.mkdir(parents=True)
    subprocess.run(["git", "clone", "-q", "--no-hardlinks", str(src), str(tree)], check=True)
    path, old, new = PLANTS[name]
    text = (tree / path).read_text()
    assert text.count(old) == 1, f"{name}: target count {text.count(old)}"
    text = text.replace(old, new)
    if name == "P5-leaveall-last":
        assert text.count(P5_TAIL[0]) == 1
        text = text.replace(P5_TAIL[0], P5_TAIL[1])
    (tree / path).write_text(text)
    diff = subprocess.run(["git", "-C", str(tree), "diff"], capture_output=True, text=True).stdout
    result = {"plant": name, "diff": diff}
    env = os.environ.copy()
    env["LD_LIBRARY_PATH"] = f"{prefix}/lib" + os.pathsep + env.get("LD_LIBRARY_PATH", "")
    for prof in ("OFF", "ON"):
        b = work / f"build-{prof}"
        rc, _ = sh(["cmake", "-S", str(tree), "-B", str(b), "-DCMAKE_BUILD_TYPE=Debug",
                    f"-DCMAKE_PREFIX_PATH={prefix}", f"-DLWSRP_MILAN={prof}"], work / f"configure-{prof}.log", env)
        rc2, _ = sh(["cmake", "--build", str(b), "--parallel", "2"], work / f"build-{prof}.log", env)
        if rc or rc2:
            result[prof] = {"build": "FAILED"}
            continue
        rc, output = sh([str(b / "unit_tests")], work / f"unit-{prof}.log", env, cwd=b, timeout=300)
        failing = sorted(set(re.findall(r"Failure: \S+ -> (\S+)", output)))
        exc = sorted(set(re.findall(r"Exception: \S+ -> (\S+)", output)))
        eq_rc, eq_out = sh([sys.executable, str(tree / "tests/check_equivalence.py"), "--work-dir",
                            str(work / f"eq-{prof}"), "--prefix", str(prefix), "--milan", prof],
                           work / f"equivalence-{prof}.log", env, cwd=tree)
        summary = [l for l in eq_out.splitlines() if l.startswith("Scenarios:")]
        # Fuzz: link the reviewer driver against this plant's library.
        fz = work / f"fuzz-{prof}"
        cc_rc, _ = sh(["gcc", "-std=c11", "-O1", f"-I{tree}/src/include", f"-I{tree}/src",
                       str(scripts / "r587_fuzz.c"), "-o", str(fz), f"-L{b}", "-lshlan", f"-Wl,-rpath,{b}"],
                      work / f"fuzz-build-{prof}.log")
        base_fz = scratch.parent / "fuzz" / f"fuzz-{prof}-base"
        fuzz_fail = 0
        fuzz_jobs = 0
        for app, eth in ((0, "22ea"), (1, "88f5"), (2, "88f6")):
            for mode in ("roomy", "tight"):
                for seed in range(1, 9):
                    tag = f"{prof}-{app}-{mode}-{seed}"
                    with open(work / f"{tag}.head", "w") as f:
                        subprocess.run([str(fz), str(seed), str(app), "1" if mode == "tight" else "0", "400"],
                                       stdout=f, stderr=subprocess.STDOUT, timeout=120)
                    base = "-"
                    if mode == "roomy":
                        with open(work / f"{tag}.base", "w") as f:
                            subprocess.run([str(base_fz), str(seed), str(app), "0", "400"],
                                           stdout=f, stderr=subprocess.STDOUT, timeout=120)
                        base = str(work / f"{tag}.base")
                    r = subprocess.run([sys.executable, "-I", str(scripts / "r587_fuzz_compare.py"), eth, mode,
                                        base, str(work / f"{tag}.head")], capture_output=True, text=True)
                    fuzz_jobs += 1
                    fuzz_fail += r.returncode != 0
        result[prof] = {"unit_rc": rc, "failing_tests": failing, "exceptions": exc,
                        "equivalence_rc": eq_rc, "equivalence": summary,
                        "fuzz_jobs": fuzz_jobs, "fuzz_failing": fuzz_fail}
    (out / f"{name}.json").write_text(json.dumps(result, indent=2) + "\n")
    lines = [f"{name}"]
    for prof in ("OFF", "ON"):
        r = result.get(prof, {})
        if "unit_rc" in r:
            lines.append(f"  {prof}: unit rc={r['unit_rc']} failing={len(r['failing_tests'])} "
                         f"exceptions={len(r['exceptions'])} equivalence rc={r['equivalence_rc']} "
                         f"{' '.join(r['equivalence'])} fuzz failing={r['fuzz_failing']}/{r['fuzz_jobs']}")
        else:
            lines.append(f"  {prof}: {r}")
    return "\n".join(lines)


def main():
    src, prefix, scratch, out = (Path(a).resolve() for a in sys.argv[1:5])
    names = sys.argv[5:] or list(PLANTS)
    out.mkdir(parents=True, exist_ok=True)
    scripts = Path(__file__).resolve().parent
    with cf.ThreadPoolExecutor(max_workers=8) as pool:
        for text in pool.map(lambda n: run_plant(n, src, prefix, scratch, out, scripts), names):
            print(text, flush=True)


if __name__ == "__main__":
    main()
