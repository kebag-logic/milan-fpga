#!/usr/bin/env python3
"""Fault and mutation probes for docs_inventory.py on disposable copies.

Usage: probes.py REPO HEAD SCRATCH RECEIPTS. Nothing is written to REPO.
"""
import concurrent.futures as cf, hashlib, json, os, re, shutil, subprocess, sys
from pathlib import Path

repo, head, scratch, receipts = sys.argv[1], sys.argv[2], Path(sys.argv[3]), Path(sys.argv[4])
GEN = "scripts/docs_inventory.py"
DATA = "scripts/docs_inventory.json"
AUDIT = "docs/DOCUMENTATION_AUDIT.md"


def sh(cmd, cwd=None, timeout=500):
    r = subprocess.run(cmd, cwd=cwd, shell=isinstance(cmd, str), capture_output=True, text=True, timeout=timeout)
    return r.returncode, r.stdout + r.stderr


def export(dest):
    """A tree of the exact head with no Git metadata."""
    dest.mkdir(parents=True, exist_ok=True)
    sh(f"git -C {repo} archive {head} | tar -x -C {dest}")


def clone(dest):
    """A clone at the exact head, no submodules populated."""
    sh(["git", "clone", "-q", "--no-checkout", "--shared", repo, str(dest)])
    sh(["git", "-C", str(dest), "checkout", "-q", "--detach", head])


def gen(cwd, *args):
    return sh(["python3", GEN, *args], cwd=cwd)


# ---- mutants: (name, old, new)
RULE = 're.fullmatch(r"README\\.md|REQUIREMENTS\\.md|docs/README\\.md|docs/(guides|integration|reference)/.*", path)'
CELL = 'verified = "archive" if path.startswith(ARCHIVE_PREFIX) else "D0" if path in checked else "area lane"'
GUARD = 'if not isinstance(checked, list) or not all(isinstance(page, str) and page in known for page in checked):'
MUTANTS = [
    ("M00 identity", None, None),
    ("M01 old path rule restored", CELL, f'verified = "archive" if path.startswith(ARCHIVE_PREFIX) else "D0" if {RULE} else "area lane"'),
    ("M02 list or path rule", CELL, f'verified = "archive" if path.startswith(ARCHIVE_PREFIX) else "D0" if path in checked or {RULE} else "area lane"'),
    ("M03 path rule narrowed to guides only added", CELL, 'verified = "archive" if path.startswith(ARCHIVE_PREFIX) else "D0" if path in checked or path.startswith("docs/guides/") else "area lane"'),
    ("M04 integration prefix inherits D0", CELL, 'verified = "archive" if path.startswith(ARCHIVE_PREFIX) else "D0" if path in checked or path.startswith("docs/integration/") else "area lane"'),
    ("M05 reference prefix inherits D0", CELL, 'verified = "archive" if path.startswith(ARCHIVE_PREFIX) else "D0" if path in checked or path.startswith("docs/reference/") else "area lane"'),
    ("M06 no page is D0", CELL, 'verified = "archive" if path.startswith(ARCHIVE_PREFIX) else "area lane"'),
    ("M07 D0 tested before archive", CELL, 'verified = "D0" if path in checked else "archive" if path.startswith(ARCHIVE_PREFIX) else "area lane"'),
    ("M08 archive cell lost", CELL, 'verified = "D0" if path in checked else "area lane"'),
    ("M09 tracked check dropped", GUARD, 'if not isinstance(checked, list) or not all(isinstance(page, str) for page in checked):'),
    ("M10 list check dropped", GUARD, 'if not all(isinstance(page, str) and page in known for page in checked):'),
    ("M11 str check dropped", GUARD, 'if not isinstance(checked, list) or not all(page in known for page in checked):'),
    ("M12 tracked check reads the disk not the population", GUARD, 'if not isinstance(checked, list) or not all(isinstance(page, str) and (root / page).is_file() for page in checked):'),
    ("M13 refusal loses its advice", "`verified_pages` must list tracked pages; update it when a listed page moves or leaves", "`verified_pages` is bad"),
    ("M14 lane figure counts non-area-lane cells", "{sum(p.verified == 'D0' for p in chosen)}", "{sum(p.verified != 'area lane' for p in chosen)}"),
    ("M15 lane figure counts every page", "{sum(p.verified == 'D0' for p in chosen)}", "{len(chosen)}"),
    ("M16 key misread", 'data.get("verified_pages", [])', 'data.get("verified", [])'),
    ("M17 missing key refused", 'data.get("verified_pages", [])', 'data["verified_pages"]'),
    ("M18 data file absent returns everything verified", 'return "--", "--", set(), {}, []', 'return "--", "--", set(paths), {}, []'),
]


def run_mutant(item):
    index, (name, old, new) = item
    work = scratch / f"mut{index:02d}"
    shutil.rmtree(work, ignore_errors=True)
    export(work)
    path = work / GEN
    text = path.read_text(encoding="utf-8")
    if old is not None:
        if text.count(old) != 1:
            return name, "NOT-APPLIED", "", ""
        path.write_text(text.replace(old, new), encoding="utf-8")
    src = work / GEN
    rc_self, out_self = sh(["python3", str(src), "--selftest"], cwd=work)
    rc_check, _ = sh(["python3", str(src), "--check"], cwd=work)
    fail = [l for l in out_self.splitlines() if l.startswith(("FAIL", "SELFTEST", "control")) or "FAIL" in l][:3]
    shutil.rmtree(work, ignore_errors=True)
    return name, rc_self, rc_check, " / ".join(x[:150] for x in fail)


def tree_probes():
    lines = []
    base = scratch / "base"
    shutil.rmtree(base, ignore_errors=True)
    clone(base)
    rc, out = gen(base, "--check")
    lines.append(f"head --check rc {rc}: {out.strip()[:120]}")
    rc, out = gen(base, "--selftest")
    lines.append(f"head --selftest rc {rc}: {out.strip().splitlines()[-1][:120]}")
    before = hashlib.sha256((base / AUDIT).read_bytes()).hexdigest()
    rc, _ = gen(base, "--write")
    after = hashlib.sha256((base / AUDIT).read_bytes()).hexdigest()
    lines.append(f"--write rc {rc}; audit sha256 before {before} after {after} identical {before == after}")

    # No Git metadata.
    ng = scratch / "nogit"
    shutil.rmtree(ng, ignore_errors=True)
    export(ng)
    rc, out = gen(ng, "--check")
    lines.append(f"no .git export: .git present {(ng / '.git').exists()} --check rc {rc}: {out.strip()[:120]}")

    # One-commit clone lacking the baseline.
    one = scratch / "shallow"
    shutil.rmtree(one, ignore_errors=True)
    sh(["git", "clone", "-q", "--depth", "1", f"file://{repo}", str(one)])
    sh(["git", "-C", str(one), "checkout", "-q", "--detach", head])
    rc_base, _ = sh(["git", "-C", str(one), "cat-file", "-e", "1e80128f^{commit}"])
    count = sh(["git", "-C", str(one), "rev-list", "--count", "HEAD"])[1].strip()
    rc, out = gen(one, "--check")
    lines.append(f"shallow clone: commits {count}, baseline present rc {rc_base} (non-zero means absent), head {sh(['git','-C',str(one),'rev-parse','HEAD'])[1].strip()} --check rc {rc}: {out.strip()[:100]}")
    # Git absent from PATH entirely, with the export.
    env_rc = subprocess.run(["env", "PATH=/nonexistent", sys.executable, GEN, "--check"], cwd=ng, capture_output=True, text=True)
    lines.append(f"no .git and no git binary on PATH: --check rc {env_rc.returncode}: {(env_rc.stdout + env_rc.stderr).strip()[:100]}")

    def fresh(name):
        work = scratch / name
        shutil.rmtree(work, ignore_errors=True)
        clone(work)
        return work

    def d0_rows(work):
        rows = [l for l in (work / AUDIT).read_text(encoding="utf-8").splitlines() if l.startswith("| [") and l.rstrip().split("|")[-3].strip() == "D0"]
        return len(rows)

    def ref_line(work):
        return next(l for l in (work / AUDIT).read_text(encoding="utf-8").splitlines() if l.startswith("| reference |"))

    # Rename and removal of a listed page.
    w = fresh("p_rename")
    sh(["git", "mv", "docs/reference/SUBMODULES.md", "docs/reference/SUBMODULES2.md"], cwd=w)
    rc, out = gen(w, "--check"); lines.append(f"git mv listed page, --check rc {rc}: {out.strip()}")
    rc, out = gen(w, "--write"); lines.append(f"git mv listed page, --write rc {rc}, audit untouched {sh(['git','diff','--quiet','--',AUDIT],cwd=w)[0] == 0}")
    data = json.loads((w / DATA).read_text(encoding="utf-8"))
    data["verified_pages"] = sorted("docs/reference/SUBMODULES2.md" if p == "docs/reference/SUBMODULES.md" else p for p in data["verified_pages"])
    (w / DATA).write_text(json.dumps(data, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    rc, out = gen(w, "--write"); rc2, out2 = gen(w, "--check")
    lines.append(f"rename followed in the list: --write rc {rc}, --check rc {rc2}, D0 rows {d0_rows(w)}, {ref_line(w)}")

    w = fresh("p_remove")
    sh(["git", "rm", "-q", "docs/reference/SUBMODULES.md"], cwd=w)
    rc, out = gen(w, "--check"); lines.append(f"git rm listed page, --check rc {rc}: {out.strip()}")
    data = json.loads((w / DATA).read_text(encoding="utf-8"))
    data["verified_pages"].remove("docs/reference/SUBMODULES.md")
    (w / DATA).write_text(json.dumps(data, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    rc, out = gen(w, "--check"); lines.append(f"removal followed in the list, before --write: --check rc {rc}: {out.strip()[:100]}")
    rc, _ = gen(w, "--write"); rc2, _ = gen(w, "--check")
    lines.append(f"removal followed in the list: --write rc {rc}, --check rc {rc2}, D0 rows {d0_rows(w)}, {ref_line(w)}")

    w = fresh("p_disk")
    (w / "docs/reference/SUBMODULES.md").unlink()
    rc, out = gen(w, "--check"); lines.append(f"listed page deleted on disk only, --check rc {rc}: {out.strip()[:140]}")

    w = fresh("p_stale_reuse")
    sh(["git", "rm", "-q", "docs/reference/SUBMODULES.md"], cwd=w)
    p = w / "docs/reference/SUBMODULES.md"; p.write_text("# Replacement at the same path\n", encoding="utf-8")
    sh(["git", "add", "docs/reference/SUBMODULES.md"], cwd=w)
    rc, out = gen(w, "--write"); row = next(l for l in (w / AUDIT).read_text(encoding='utf-8').splitlines() if "reference/SUBMODULES.md](" in l)
    lines.append(f"listed page replaced in place: --write rc {rc}, row cell {row.rstrip().split('|')[-3].strip()}")

    # New pages under each old release-facing root.
    for name, new in (("p_new_guide", "docs/guides/NEW.md"), ("p_new_int", "docs/integration/NEW.md"), ("p_new_ref", "docs/reference/NEW.md"), ("p_new_gptp", "docs/guides/gptp/NEW.md")):
        w = fresh(name)
        (w / new).write_text("# New page\n", encoding="utf-8")
        sh(["git", "add", new], cwd=w)
        rc, _ = gen(w, "--check")
        rc_w, _ = gen(w, "--write"); rc2, _ = gen(w, "--check")
        row = next(l for l in (w / AUDIT).read_text(encoding="utf-8").splitlines() if f"[{new}]" in l)
        lines.append(f"new {new}: --check rc {rc}, --write rc {rc_w}, --check rc {rc2}, cell {row.rstrip().split('|')[-3].strip()}, D0 rows {d0_rows(w)}, {ref_line(w)}")

    # Data edits.
    def data_probe(name, change):
        w = fresh(name)
        data = json.loads((w / DATA).read_text(encoding="utf-8"))
        change(data)
        (w / DATA).write_text(json.dumps(data, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
        rc, out = gen(w, "--check")
        rc_w, _ = gen(w, "--write")
        return w, rc, rc_w, out.strip()[:130]

    w, rc, rc_w, out = data_probe("p_key", lambda d: d.pop("verified_pages"))
    lines.append(f"key removed: --check rc {rc} ({out}), --write rc {rc_w}, D0 rows after write {d0_rows(w)}")
    w, rc, rc_w, out = data_probe("p_dup", lambda d: d["verified_pages"].append("README.md"))
    lines.append(f"duplicate entry: --check rc {rc} ({out}), --write rc {rc_w}, D0 rows {d0_rows(w)}")
    w, rc, rc_w, out = data_probe("p_arch", lambda d: d["verified_pages"].append("docs/history/v1/README.md"))
    row = next(l for l in (w / AUDIT).read_text(encoding="utf-8").splitlines() if "[docs/history/v1/README.md]" in l)
    lines.append(f"archive page listed: --check rc {rc} ({out}), --write rc {rc_w}, cell {row.rstrip().split('|')[-3].strip()}, D0 rows {d0_rows(w)}")
    w, rc, rc_w, out = data_probe("p_grow", lambda d: d["verified_pages"].append("docs/reference/STRICTER_READINGS.md"))
    lines.append(f"post-baseline page added to the list: --check rc {rc} ({out}), --write rc {rc_w}, D0 rows {d0_rows(w)}, {ref_line(w)}")
    w, rc, rc_w, out = data_probe("p_nonpage", lambda d: d["verified_pages"].append("docs/reference/milan_feature_status.json"))
    lines.append(f"tracked non-document listed: --check rc {rc} ({out})")
    return lines


def main():
    scratch.mkdir(parents=True, exist_ok=True)
    with cf.ThreadPoolExecutor(max_workers=14) as pool:
        tree = pool.submit(tree_probes)
        rows = list(pool.map(run_mutant, enumerate(MUTANTS)))
        out = tree.result()
    (receipts / "tree_probes.txt").write_text("\n".join(out) + "\n", encoding="utf-8")
    with open(receipts / "mutants.txt", "w", encoding="utf-8") as f:
        f.write("name | selftest rc | check rc | first failing lines\n")
        for row in rows:
            f.write(" | ".join(str(x) for x in row) + "\n")


main()
