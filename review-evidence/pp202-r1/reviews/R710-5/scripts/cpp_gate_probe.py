"""Apply the parent Rule 11 gate's per-file scan() to protocol-processor C++ files at two commits.

Usage: python3 -I cpp_gate_probe.py <gate_scripts_dir> <pp_repo> <commit> [<commit> ...]
Prints per-commit nonzero counts for every C++ file the PR (ed211803..commit) touched, and
the total over every tracked tb/ C++ file in the submodule.
"""
import subprocess
import sys
import types

gate_dir, repo, *commits = sys.argv[1:]
stub = types.ModuleType("code_quality_scope")
stub.PROJECT_SUBMODULES = ("protocol-processor", "gptp-processor")
stub.tracked = lambda *a: []
sys.modules["code_quality_scope"] = stub
sys.path.insert(0, gate_dir)
import check_cpp_idiom as g  # noqa: E402

SUF = (".c", ".cpp", ".cc", ".cxx", ".h", ".hpp")


def git(*a):
    return subprocess.run(["git", "-C", repo, *a], check=True, capture_output=True, text=True).stdout


for c in commits:
    files = [f for f in git("ls-tree", "-r", "--name-only", c, "tb/").split() if f.endswith(SUF)]
    touched = {f for f in git("diff", "--name-only", "ed211803", c).split() if f.endswith(SUF)}
    total = {}
    for f in files:
        counts = g.scan(git("show", f"{c}:{f}"), "protocol-processor/" + f)
        for k, v in counts.items():
            total[k] = total.get(k, 0) + v
        if f in touched:
            nz = {k: v for k, v in counts.items() if v}
            print(f"{c[:8]} touched {f}: {nz or 'all zero'}")
            if nz.get("multi-declarator declaration"):
                for ln, s in g.sites(git("show", f"{c}:{f}"), "multi-declarator declaration", f):
                    print(f"    ES.10 line {ln}: {s.strip()}")
    print(f"{c[:8]} all tb C++ files ({len(files)}): { {k: v for k, v in total.items() if v} or 'all zero'}")
