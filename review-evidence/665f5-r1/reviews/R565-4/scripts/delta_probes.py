#!/usr/bin/env python3
"""Wire differential at one and two interfaces, core-side plants on the wire path,
and independently formulated reordering plants on the native gtest path.

Usage: python3 -I delta_probes.py --repo <clone> --packet <packet> --verilator <bin>
Only copies under <packet>/scratch are planted; the clone is read-only here.
"""
import argparse, concurrent.futures, hashlib, json, os, re, shutil, subprocess, sys, threading
from pathlib import Path

p = argparse.ArgumentParser()
p.add_argument("--repo", type=Path, required=True)
p.add_argument("--packet", type=Path, required=True)
p.add_argument("--verilator", required=True)
p.add_argument("--wire-plants-only", action="store_true", help="rerun only the wire-path plants")
a = p.parse_args()
a.repo = a.repo.resolve(); a.packet = a.packet.resolve()
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"; sys.dont_write_bytecode = True
scratch = a.packet / "scratch"; os.environ["TMPDIR"] = str(scratch)
receipts = a.packet / "receipts"; receipts.mkdir(exist_ok=True)
sys.path.insert(0, str(a.repo / "sw/firmware/ctrl/test"))
import ctrl_build, aecp_arms, fw_gtest  # noqa: E402

version = subprocess.check_output([a.verilator, "--version"], text=True).strip()
assert "Verilator 5.050" in version, version

SRC = "aecp/aecp_commands.c"
# Wire-path plants: the same two defect shapes named by the prior finding.
WIRE_PLANTS = {
    "X8": ("\t\tif (info.running) {\n",
           "\t\tif ((wire_be32(in + 4) & 0xfaf80000u) == 0u && !aecp_foreign_lock(a)) {\n"
           "\t\t\twire_put_be(out + 4, flags & ~0x20000000u, 4);\n\t\t\treturn AECP_SUCCESS;\n\t\t}\n"
           "\t\tif (info.running) {\n", "running STREAM_OUTPUT SET refusal"),
    "X9": ("\t\tif (type == 5u) {\n\t\t\treturn AECP_NOT_SUPPORTED;\n\t\t}\n",
           "\t\tif (type == 5u && (wire_be32(in + 4) & 0xfaf80000u) != 0u) {\n"
           "\t\t\treturn AECP_NOT_SUPPORTED;\n\t\t}\n", "STREAM_INPUT SET refusal"),
}
# Independent formulations: move each refusal below the no-sub-command early return.
EARLY = ("\t\tif ((requested & 0x20000000u) == 0u) {\n"
         "\t\t\twire_put_be(out + 4, flags & ~0x20000000u, 4);\n\t\t\treturn AECP_SUCCESS;\n\t\t}\n")
RUN = "\t\tif (info.running) {\n\t\t\treturn AECP_STREAM_IS_RUNNING;\n\t\t}\n"
INP = "\t\tif (type == 5u) {\n\t\t\treturn AECP_NOT_SUPPORTED;\n\t\t}\n"
NATIVE_PLANTS = {
    "V8-running-check-after-nosub-return": (RUN, EARLY, "Core.S1_NoSubcommandSetOnRunningOutputIsRefused",
                                            "STREAM_IS_RUNNING for a no-sub-command SET"),
    "V9-input-check-after-nosub-return": (INP, EARLY, "Core.S2_NoSubcommandSetOnInputIsNotSupported",
                                          "NOT_SUPPORTED for a no-sub-command SET to a STREAM_INPUT"),
}


def reorder(text, block, early):
    assert text.count(block) == 1 and text.count(early) == 1
    text = text.replace(block, "", 1)
    return text.replace(early, early + block, 1)


def mini_root(tag):
    """Symlink the clone except a real copy of sw/firmware/ctrl, so ROOT resolves here."""
    root = scratch / f"wroot-{tag}"
    if root.exists():
        shutil.rmtree(root)
    def link(src, dst, keep):
        dst.mkdir(parents=True)
        for child in src.iterdir():
            if child.name == keep[0]:
                if len(keep) == 1:
                    shutil.copytree(child, dst / child.name, ignore=shutil.ignore_patterns("__pycache__"))
                else:
                    link(child, dst / child.name, keep[1:])
            elif child.name != ".git":
                (dst / child.name).symlink_to(child)
    link(a.repo, root, ["sw", "firmware", "ctrl"])
    return root


wire_gate = threading.Semaphore(2)  # each wire build runs make/verilator at -j 8


def wire(tag, interfaces, plant=None):
    reference = a.repo / "protocol-processor" if interfaces == 1 else scratch / "reference-two"
    base = a.repo
    if plant:
        base = mini_root(f"{tag}-if{interfaces}")
        path = base / "sw/firmware/ctrl" / SRC
        old, new, _ = WIRE_PLANTS[plant]
        text = path.read_text(); assert text.count(old) == 1
        path.write_text(text.replace(old, new))
    out = scratch / f"wire-{tag}-if{interfaces}"
    if out.exists():
        shutil.rmtree(out)
    cmd = [sys.executable, "-B", str(base / "sw/firmware/ctrl/test/aecp_wire.py"), "--reference", str(reference),
           "--interfaces", str(interfaces), "--output", str(out), "--verilator", a.verilator]
    name = f"wire-{tag}-if{interfaces}"
    with wire_gate, (receipts / f"{name}.log").open("w") as log:
        r = subprocess.run(cmd, stdout=log, stderr=subprocess.STDOUT, timeout=1500)
    (receipts / f"{name}.rc").write_text(f"{r.returncode}\n")
    text = (receipts / f"{name}.log").read_text()
    res = {"case": name, "rc": r.returncode}
    if plant is None:
        assert r.returncode == 0, name
        dest = receipts / name; dest.mkdir(exist_ok=True)
        for f in ["verdict.json", "reference-sha256.json"] + [f"wire-if{i}.log" for i in range(interfaces)]:
            shutil.copy2(out / f, dest / f)
        res["verdict"] = json.loads((out / "verdict.json").read_text())
    else:
        want = WIRE_PLANTS[plant][2]
        found = re.findall(r"^AssertionError: (.*)$", text, re.M)
        res["diagnostic"] = found[-1] if found else None
        assert r.returncode != 0 and found and found[-1] == want, (name, found)
        dest = receipts / name; dest.mkdir(exist_ok=True)
        shutil.copy2(out / "wire-if0.log", dest / "wire-if0.log")
    return res


def native(interfaces):
    root = scratch / f"variant-if{interfaces}"
    if root.exists():
        shutil.rmtree(root)
    src = root / "ctrl"
    shutil.copytree(a.repo / "sw/firmware/ctrl", src, ignore=shutil.ignore_patterns("__pycache__"))
    tree = ctrl_build.Tree(src, root / "build", root / "reuse", fw_gtest.Build(jobs=2))
    config = a.repo / "configs/endstation_ax7101_1x1_tdm8.yaml"
    path = src / SRC; original = path.read_text(); out = []
    for label, (block, early, test, words) in NATIVE_PLANTS.items():
        path.write_text(reorder(original, block, early))
        try:
            r = aecp_arms.core_arm(tree, config, interfaces, "core", test)
        finally:
            path.write_text(original)
        tag = f"{label}-if{interfaces}"
        (receipts / f"{tag}.log").write_text(r.log); (receipts / f"{tag}.rc").write_text(f"{r.rc}\n")
        m = re.search(r"\[ RUN      \] " + re.escape(test) + r"\n(.*?)\[  FAILED  \] " + re.escape(test) + r" \(",
                      r.log, re.S)
        assert r.rc == 1 and m and words in m[1], tag
        out.append({"case": tag, "test": test, "diagnostic": words, "rc": r.rc,
                    "named_failures": m[1].count(words)})
    assert path.read_text() == original
    return out


jobs = {}
with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
    for n in (1, 2):
        if not a.wire_plants_only:
            jobs[pool.submit(wire, "clean", n)] = f"wire-clean-if{n}"
        for plant in WIRE_PLANTS:
            jobs[pool.submit(wire, plant, n, plant)] = f"wire-{plant}-if{n}"
    results = {}
    prior = receipts / "delta-probes.json"
    if a.wire_plants_only and prior.exists():
        results = {k: v for k, v in json.loads(prior.read_text()).items() if k not in jobs.values()}
    for f in concurrent.futures.as_completed(jobs):
        try:
            results[jobs[f]] = f.result(); print(jobs[f], "ok", flush=True)
        except Exception as e:
            results[jobs[f]] = {"error": repr(e)}; print(jobs[f], "ERROR", repr(e), flush=True)
# Native variants after the wire builds so the parallel job count stays within budget.
for n in (() if a.wire_plants_only else (1, 2)):
    try:
        results[f"native-variants-if{n}"] = native(n); print(f"native-variants-if{n} ok", flush=True)
    except Exception as e:
        results[f"native-variants-if{n}"] = {"error": repr(e)}; print(f"native-variants-if{n} ERROR", repr(e), flush=True)
(receipts / "delta-probes.json").write_text(json.dumps(results, indent=2, sort_keys=True) + "\n")
bad = [k for k, v in results.items() if isinstance(v, dict) and "error" in v]
print("FAIL" if bad else "PASS", bad, flush=True)
sys.exit(1 if bad else 0)
