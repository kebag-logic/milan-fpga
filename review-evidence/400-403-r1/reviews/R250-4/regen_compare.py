"""Regenerate builder artifacts for every shipped config at two commits and compare.

Usage: python3 -B regen_compare.py <clone> <base-sha> <head-sha> <scratch-dir>

Each commit is exported with `git archive` into its own tree (submodule
directories are symlinked read-only from the clone), the real
endstation_builder.build() is called there for every configs/endstation_*.yaml,
and afterwards every file in both exported trees is hashed. The comparison
covers the builder's output directory AND every file the build wrote back
into the tree (tracked header copies), excluding only the files the delta
itself edits. Prints a JSON summary; exit 0 iff everything generated is
byte-identical and the tree-wide comparison differs only in the edited files.
"""
import hashlib
import json
import subprocess
import sys
from pathlib import Path

clone, base, head, scratch = Path(sys.argv[1]).resolve(), sys.argv[2], sys.argv[3], Path(sys.argv[4]).resolve()
SUBMODULES = ["external", "gptp-processor", "protocol-processor", "third_party/verilog-axis"]


def export(sha: str, dest: Path) -> None:
    dest.mkdir(parents=True, exist_ok=False)
    archive = subprocess.run(["git", "-C", str(clone), "archive", sha], check=True,
                             capture_output=True).stdout
    subprocess.run(["tar", "-x", "-C", str(dest)], input=archive, check=True)
    for sub in SUBMODULES:
        target = dest / sub
        if target.exists() and not any(target.iterdir()):
            target.rmdir()
        if not target.exists() and (clone / sub).exists():
            target.symlink_to(clone / sub)


def build_all(tree: Path, out: Path) -> dict:
    code = f"""
import sys, json
from pathlib import Path
sys.path.insert(0, 'sw/builder')
import endstation_builder as eb
res = {{}}
for cfg in sorted(Path('configs').glob('endstation_*.yaml')):
    r = eb.build(str(cfg), {str(out)!r})
    d = Path({str(out)!r}) / r['cfg']['name']
    (d / 'sweep_opts.sh').write_text(r['sweep_opts'])
    res[str(cfg)] = sorted(k for k in r['paths'])
print(json.dumps(res))
"""
    p = subprocess.run([sys.executable, "-B", "-c", code], cwd=tree,
                       capture_output=True, text=True)
    return dict(rc=p.returncode, stdout=p.stdout[-4000:], stderr=p.stderr[-4000:])


def manifest(root: Path) -> dict:
    out = {}
    for path in sorted(root.rglob("*")):
        if path.is_symlink() or not path.is_file():
            continue
        if "__pycache__" in path.parts:
            continue
        out[str(path.relative_to(root))] = hashlib.sha256(path.read_bytes()).hexdigest()
    return out


edited = subprocess.run(["git", "-C", str(clone), "diff", "--name-only", base, head],
                        check=True, capture_output=True, text=True).stdout.split()
summary = dict(base=base, head=head, edited_files=edited)
trees, outs = {}, {}
for tag, sha in (("base", base), ("head", head)):
    trees[tag] = scratch / f"tree-{tag}"
    outs[tag] = scratch / f"out-{tag}"
    export(sha, trees[tag])
    pre = manifest(trees[tag])
    outs[tag].mkdir(parents=True)
    summary[f"build_{tag}"] = build_all(trees[tag], outs[tag])
    post = manifest(trees[tag])
    summary[f"tree_files_written_by_build_{tag}"] = sorted(
        k for k in post if pre.get(k) != post[k])
m_out = {t: manifest(outs[t]) for t in outs}
m_tree = {t: manifest(trees[t]) for t in trees}
summary["output_files"] = {t: len(m_out[t]) for t in m_out}
summary["output_bytes"] = {t: sum(p.stat().st_size for p in outs[t].rglob("*") if p.is_file())
                           for t in outs}
summary["output_differences"] = sorted(
    k for k in set(m_out["base"]) | set(m_out["head"]) if m_out["base"].get(k) != m_out["head"].get(k))
tree_diff = sorted(k for k in set(m_tree["base"]) | set(m_tree["head"])
                   if m_tree["base"].get(k) != m_tree["head"].get(k))
summary["tree_differences"] = tree_diff
summary["tree_differences_outside_edited"] = [k for k in tree_diff if k not in edited]
summary["written_copies_sha256"] = {
    k: [m_tree["base"].get(k), m_tree["head"].get(k)]
    for k in summary["tree_files_written_by_build_head"]}
ok = (summary["build_base"]["rc"] == 0 and summary["build_head"]["rc"] == 0
      and not summary["output_differences"] and not summary["tree_differences_outside_edited"]
      and summary["output_files"]["base"] > 0)
summary["verdict"] = "IDENTICAL" if ok else "DIFFERENT_OR_FAILED"
print(json.dumps(summary, indent=2))
sys.exit(0 if ok else 1)
