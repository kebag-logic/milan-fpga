#!/usr/bin/env python3
"""Portable focused review: python3 scripts/probe.py CHECKOUT PACKET objects|sparse|docs.
All children are joined; disposable source/build files remain in PACKET/scratch.
"""
import concurrent.futures as cf
import hashlib, importlib.util, io, json, os, pathlib, subprocess, sys, tarfile
sys.dont_write_bytecode = True
repo, packet = map(lambda x: pathlib.Path(x).resolve(), sys.argv[1:3])
mode = sys.argv[3]
base = "d1bb4f4e5954af6dabe7f210a6bf7adbb76bdd6b"
head = "50a2106483141fcd7d1b20654bcf0803e7c3020a"
work = packet / "scratch" / ("probe-" + mode)
work.mkdir(parents=True, exist_ok=False)
receipts = packet / "receipts"
def run(cmd, cwd=None):
    p = subprocess.run(cmd, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=240)
    if p.returncode:
        raise RuntimeError(str(cmd) + "\n" + p.stdout.decode(errors="replace"))
    return p.stdout
def export(rev, name):
    dest = work / name
    dest.mkdir()
    data = run(["git", "archive", rev, "src"], repo)
    with tarfile.open(fileobj=io.BytesIO(data)) as t:
        t.extractall(dest, filter="data")
    return dest
def digest(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()
if mode == "objects":
    trees = {"base": export(base, "base"), "head": export(head, "head")}
    sources = ["core/mrp_mad.c", "core/mrp_pdu.c", "core/switch.c", "ports/timer.c",
               "ports/alloc.c", "modules/msrp.c", "modules/mvrp.c", "modules/mmrp.c"]
    flags = {opt + ("-milan" if milan else ""): ["-" + opt] + (["-DLWSRP_MILAN=1"] if milan else [])
             for opt in ("O0", "O2", "Os") for milan in (False, True)}
    flags.update({opt + "-fPIC": ["-" + opt, "-fPIC"] for opt in ("O0", "O2")})
    def compare(task):
        label, opts, source, debug = task
        hashes = {}
        for name, tree in trees.items():
            obj = work / (label + "-" + name + "-" + source.replace("/", "_") + ".o")
            run(["cc", "-std=c11", *opts, "-Isrc/include", "-Isrc", "-c", "src/" + source, "-o", str(obj)], tree)
            if debug:
                run(["objcopy", "--strip-debug", str(obj)])
            hashes[name] = digest(obj)
        return {"flags": opts, "source": source, "stripped_debug": debug, **hashes, "equal": hashes["base"] == hashes["head"]}
    tasks = [(label, opts, s, False) for label, opts in flags.items() for s in sources]
    tasks += [(opt+"-debug", ["-"+opt, "-g"], s, True) for opt in ("O0", "O2", "Os") for s in sources]
    with cf.ThreadPoolExecutor(max_workers=8) as pool:
        rows = list(pool.map(compare, tasks))
    result = {"base": base, "head": head, "compiler": run(["cc", "--version"]).decode().splitlines()[0],
              "target": run(["cc", "-dumpmachine"]).decode().strip(), "rows": rows,
              "equal": sum(x["equal"] for x in rows), "total": len(rows)}
    (receipts / "objects.json").write_text(json.dumps(result, indent=2)+"\n")
    print("Non-debug objects:", sum(r["equal"] for r in rows if not r["stripped_debug"]), "/ 64")
    print("Stripped debug objects:", sum(r["equal"] for r in rows if r["stripped_debug"]), "/ 24")
    assert all(r["equal"] for r in rows)
elif mode == "sparse":
    trees = {"base": export(base, "base"), "head": export(head, "head"), "mutant": export(head, "mutant")}
    p = trees["mutant"] / "src/core/mrp_mad.c"
    text = p.read_text()
    old, new = "            type |= 31u;\n            continue;", "            type = 255u;\n            continue;"
    assert text.count(old) == 1
    p.write_text(text.replace(old, new))
    spec = importlib.util.spec_from_file_location("differential", repo/"tests/check_differential.py")
    cd = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(cd)
    sources = cd.PROGRAMS["mad"][1]
    def trial(task):
        milan, config, opts = task
        outputs, builds = {}, {}
        for name, tree in trees.items():
            extra = [] if name == "base" else opts + ["-DTRACE_ATTR_KEY"]
            exe = work / f"{milan}-{config}-{name}"
            cmd = ["cc", *cd.FLAGS, *extra, f"-DLWSRP_MILAN={milan}", "-Isrc", "-Isrc/include",
                   str(repo/"tests/differential/mad_trace.c"), *["src/"+s for s in sources], "-o", str(exe)]
            run(cmd, tree)
            out = run([str(exe), "3", "3000"])
            outputs[name] = cd.compared("mad", opts, out)
            raw = receipts / f"sparse-{milan}-{config}-{name}.trace"
            raw.write_bytes(out)
            builds[name] = {"rc": 0, "trace_sha256": digest(raw), "trace_lines": out.count(b"\n")}
        return {"milan": milan, "config": config, "seed": 3, "steps": 3000, "builds": builds,
                "head_equal": outputs["head"] == outputs["base"], "mutant_differs": outputs["mutant"] != outputs["base"],
                "not_excused": all(x is not None for x in outputs.values())}
    with cf.ThreadPoolExecutor(max_workers=4) as pool:
        rows = list(pool.map(trial, [(m,c,opts) for m in (0,1) for c,opts in (("lean-tx",cd.LEAN_TX),("end-station",cd.END_STATION))]))
    (receipts/"sparse.json").write_text(json.dumps(rows,indent=2)+"\n")
    for row in rows:
        print(row["milan"], row["config"], "baseline/head equal",row["head_equal"],"mutant differs",row["mutant_differs"],"not excused",row["not_excused"])
    assert all(x["head_equal"] and x["mutant_differs"] and x["not_excused"] for x in rows)
elif mode == "docs":
    cmds = [["python3","-B","doc/tools/check_sentences.py"],
            ["python3","-B","doc/tools/check_references.py"],
            ["python3","-B","doc/tools/check_references.py","--self-test"]]
    for i,cmd in enumerate(cmds):
        out=run(cmd,repo)
        (receipts/f"docs-{i}.log").write_bytes(out)
        print(cmd[-1], "rc=0", out.decode().splitlines()[-1])
else:
    raise ValueError(mode)
