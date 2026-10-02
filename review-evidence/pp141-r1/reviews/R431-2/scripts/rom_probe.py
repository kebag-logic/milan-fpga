#!/usr/bin/env python3
"""Reviewer probe: ROMs, ROM word map and campaign-patch plants per revision.

usage: rom_probe.py REPO WORKDIR OUTDIR REV[=LABEL] ...

For each revision: export the tree with `git archive`, run every ROM
generator (ucode.hex, ltn_rom.hex, image.bin), record the uCPU program map
(start, length, symbolic entry name) from the generator's own `placed` and
`occupied` sets, run `git apply --check -v` of every committed *.patch in the
exported tree against that same pristine tree, and for every patch that
touches gen_ucode.py plant it in a copy, regenerate ucode.hex and record the
changed words (address: base value -> mutant value). Extra patch files can be
planted at a revision with PATCH@REV=FILE arguments (used for the pre-refresh
forms of the round-2 patches). Writes JSON and a text summary to OUTDIR.
"""
import hashlib
import json
import runpy
import shutil
import subprocess
import sys
from pathlib import Path


def sh(*args, cwd=None, check=True):
    return subprocess.run(args, cwd=cwd, check=check, capture_output=True, text=True)


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def export(repo, rev, dst):
    if dst.exists():
        shutil.rmtree(dst)
    dst.mkdir(parents=True)
    arc = subprocess.run(["git", "-C", repo, "archive", rev], check=True, capture_output=True).stdout
    subprocess.run(["tar", "-x", "-C", str(dst)], input=arc, check=True)
    # git apply needs a repository to resolve paths the way the drivers do
    sh("git", "init", "-q", cwd=dst)


def gen_ucode(tree, out):
    r = sh(sys.executable, "hdl/aecp/ucode/gen_ucode.py", "-o", str(out), cwd=tree)
    return r.stdout.strip()


def words(path):
    return [int(x, 16) for x in Path(path).read_text().split()]


def program_map(tree):
    ns = runpy.run_path(str(tree / "hdl/aecp/ucode/gen_ucode.py"), run_name="probe")
    starts = sorted(ns["placed"])
    occ = ns["occupied"]
    names = {}
    for k, v in ns.items():
        if k.startswith("E_") and isinstance(v, int) and v in starts:
            names.setdefault(v, []).append(k)
    progs = []
    for s in starts:
        n = 0
        while (s + n) in occ and (n == 0 or (s + n) not in starts):
            n += 1
        progs.append({"start": s, "len": n, "end": s + n - 1,
                      "names": sorted(names.get(s, []))})
    return {"programs": progs, "occupied_words": len(occ), "program_count": len(starts)}


def main():
    repo, work, outdir = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
    revs, extras = [], []
    for a in sys.argv[4:]:
        if "@" in a and "=" in a and a.index("@") < a.index("="):
            lab, rest = a.split("@", 1)
            rev, f = rest.split("=", 1)
            extras.append((lab, rev, f))
        else:
            rev, _, lab = a.partition("=")
            revs.append((rev, lab or rev))
    outdir.mkdir(parents=True, exist_ok=True)
    result = {}
    for rev, lab in revs:
        tree = work / lab
        export(repo, rev, tree)
        full = sh("git", "-C", str(repo), "rev-parse", rev).stdout.strip()
        res = {"rev": full}
        base = work / f"{lab}.ucode.hex"
        res["gen_ucode_stdout"] = gen_ucode(tree, base)
        res["ucode_sha256"] = sha(base)
        res["ucode_bytes"] = base.stat().st_size
        ltn = work / f"{lab}.ltn_rom.hex"
        sh(sys.executable, "hdl/acmp/rom/gen_ltn_rom.py", "-o", str(ltn), cwd=tree)
        res["ltn_rom_sha256"] = sha(ltn)
        res["ltn_rom_bytes"] = ltn.stat().st_size
        gd = tree / "hdl/aecp/desc/gen_desc_image.py"
        if not gd.exists():
            found = list(tree.glob("hdl/**/gen_desc_image.py"))
            gd = found[0] if found else None
        if gd:
            js = list(gd.parent.glob("**/example_milan_8.json")) or list(tree.glob("hdl/**/example_milan_8.json"))
            img = work / f"{lab}.image.bin"
            r = sh(sys.executable, str(gd), "-i", str(js[0]), "-o", str(img), cwd=tree, check=False)
            res["image_cmd_rc"] = r.returncode
            res["image_err"] = (r.stderr or "")[-400:]
            if img.exists():
                res["image_sha256"] = sha(img)
                res["image_bytes"] = img.stat().st_size
        res["map"] = program_map(tree)
        bw = words(base)
        patches = sorted(str(p.relative_to(tree)) for p in tree.glob("tb/**/*.patch"))
        applies = {}
        for p in patches:
            r = sh("git", "apply", "--check", "-v", p, cwd=tree, check=False)
            applies[p] = {"rc": r.returncode, "log": (r.stdout + r.stderr).strip().splitlines()}
        res["apply_check"] = applies
        plants = {}
        todo = [(p, tree / p) for p in patches if "gen_ucode.py" in (tree / p).read_text()]
        todo += [(f"{x[0]}", Path(x[2])) for x in extras if x[1] == lab]
        for name, path in todo:
            cp = work / f"{lab}.plant"
            if cp.exists():
                shutil.rmtree(cp)
            shutil.copytree(tree / "hdl", cp / "hdl")
            sh("git", "init", "-q", cwd=cp)
            r = sh("git", "apply", str(path.resolve()), cwd=cp, check=False)
            if r.returncode:
                plants[name] = {"apply_rc": r.returncode, "err": r.stderr.strip()}
                continue
            mh = work / f"{lab}.mut.hex"
            gen_ucode(cp, mh)
            mw = words(mh)
            diff = {i: [f"{bw[i]:012x}", f"{mw[i]:012x}"] for i in range(len(bw)) if bw[i] != mw[i]}
            plants[name] = {"apply_rc": 0, "ucode_sha256": sha(mh), "changed_words": diff}
        res["plants"] = plants
        result[lab] = res
    (outdir / "rom_probe.json").write_text(json.dumps(result, indent=1, sort_keys=True))
    with open(outdir / "rom_probe.txt", "w") as f:
        for lab, res in result.items():
            m = res["map"]
            refused = [p for p, v in res["apply_check"].items() if v["rc"]]
            f.write(f"== {lab} {res['rev']}\n")
            f.write(f"  ucode.hex {res['ucode_bytes']} B {res['ucode_sha256']} ({res['gen_ucode_stdout']})\n")
            f.write(f"  ltn_rom.hex {res['ltn_rom_bytes']} B {res['ltn_rom_sha256']}\n")
            f.write(f"  image.bin {res.get('image_bytes')} B {res.get('image_sha256')} rc={res.get('image_cmd_rc')}\n")
            f.write(f"  map: {m['program_count']} programs, {m['occupied_words']} words\n")
            for pr in m["programs"]:
                if set(pr["names"]) & {"E_SCLKS", "E_SCLKSRF", "E_IDNOTIF", "E_SINFOUNS"}:
                    f.write(f"    {','.join(pr['names'])}: {pr['start']}..{pr['end']} ({pr['len']})\n")
            f.write(f"  apply --check: {len(res['apply_check'])} patches, refused {len(refused)} {refused}\n")
            for name, v in sorted(res["plants"].items()):
                if v["apply_rc"]:
                    f.write(f"    plant {name}: APPLY FAILED\n")
                else:
                    cw = v["changed_words"]
                    f.write(f"    plant {name}: {len(cw)} words {sorted(int(k) for k in cw)[:12]} ucode {v['ucode_sha256'][:16]}\n")


if __name__ == "__main__":
    main()
