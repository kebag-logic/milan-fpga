#!/usr/bin/env python3
"""Single-line source mutants of scripts/docs_inventory.py against --selftest and --check.

Usage: python3 -I mutate_inventory.py SOURCE_CLONE WORKDIR

Extends the round-1 reviewer's mutant script (R741-1 mutate_selftest.py) to the
round-2 code: the same mutants where their lines still exist, re-spelled where
the line moved, plus mutants of the status rule, the gate's committed-page
invariant, the entry-point dispatch and the Git environment. Each mutant runs on
a `git clone --no-local` of SOURCE_CLONE at HEAD (no submodules). KILLED means
--selftest exited non-zero; CAUGHT means --check on the real tree did. Mutants
marked EQUIVALENT cannot change any output at this head and are not counted.
"""
import os
import shutil
import subprocess
import sys
from pathlib import Path

src, work = Path(sys.argv[1]), Path(sys.argv[2])
GEN = "scripts/docs_inventory.py"
EQUIVALENT = {"git-listing-keeps-gitlinks", "release-facing-extra-alternative"}
MUTANTS = [
    # R741-1's mutants, at their round-2 spelling.
    ("check-always-fresh", "    if actual == expected and not broken:", "    if True:"),
    ("check-returns-0-when-stale", "    print(\"regenerate with: python3 scripts/docs_inventory.py --write\")\n    return 1",
     "    print(\"regenerate with: python3 scripts/docs_inventory.py --write\")\n    return 0"),
    ("git-listing-includes-untracked", "[\"git\", \"-C\", str(root), \"ls-files\", \"-z\"]",
     "[\"git\", \"-C\", str(root), \"ls-files\", \"-z\", \"--cached\", \"--others\"]"),
    ("git-listing-keeps-gitlinks", "if p and p not in modules]", "if p]"),
    ("locate-never-finds", "        if quote in line:\n            return number", "        if False:\n            return number"),
    ("status-rule-removed", "    if page_findings and state == \"current\":", "    if False:"),
    ("release-facing-extra-alternative", "RELEASE_FACING = re.compile(r\"README", "RELEASE_FACING = re.compile(r\"NEVER|README"),
    ("lines-off-by-one", "    return text.count(\"\\n\") + (1 if text and not text.endswith(\"\\n\") else 0)",
     "    return text.count(\"\\n\") + 1"),
    ("lines-unterminated-dropped", "    return text.count(\"\\n\") + (1 if text and not text.endswith(\"\\n\") else 0)",
     "    return text.count(\"\\n\")"),
    ("readme-only-not-a-document", "    return path.endswith(\".md\") or name.upper().startswith(\"README\")",
     "    return path.endswith(\".md\")"),
    ("banner-scan-1-line", "BANNER_SCAN_LINES = 15", "BANNER_SCAN_LINES = 1"),
    # Round 2: the committed-page invariant, the dispatch and the refusal status.
    ("invariant-never-runs", "    broken = current_with_findings(actual)", "    broken = []"),
    ("invariant-reads-wrong-cell", "                states[link.group(1)] = parts[5]", "                states[link.group(1)] = parts[6]"),
    ("invariant-ignores-findings", "                listed.add(link.group(1))", "                pass"),
    ("check-on-the-real-tree", "            return check(root)", "            return check(ROOT)"),
    ("write-to-the-real-tree", "        (root / OUTPUT).write_text(generate(root), encoding=\"utf-8\")\n        print(f\"wrote {OUTPUT}\")",
     "        (ROOT / OUTPUT).write_text(generate(ROOT), encoding=\"utf-8\")\n        print(f\"wrote {OUTPUT}\")"),
    ("refusal-exits-1", "        print(f\"REFUSED: {refusal}\")\n        return 2", "        print(f\"REFUSED: {refusal}\")\n        return 1"),
    ("judged-current-wins", "        return judged[path]\n", "        return judged[path] if judged[path][0] != \"current\" else (\"current!\", \"x\")\n"),
    ("walk-includes-submodules", "                 and not any(p == m or p.startswith(m + \"/\") for m in modules)]", "]"),
]


def run(cwd: Path, *args: str, env: dict | None = None) -> int:
    return subprocess.run(["python3", "-I", GEN, *args], cwd=cwd, capture_output=True, text=True,
                          env=env).returncode


work.mkdir(parents=True, exist_ok=True)
base = work / "base"
if base.exists():
    shutil.rmtree(base)
subprocess.run(["git", "clone", "-q", "--no-local", str(src), str(base)], check=True)
head = subprocess.run(["git", "-C", str(src), "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
subprocess.run(["git", "-C", str(base), "checkout", "-q", "--detach", head], check=True)
original = (base / GEN).read_text(encoding="utf-8")
print(f"head {head}")
print(f"baseline selftest rc={run(base, '--selftest')} check rc={run(base, '--check')}")
killed = survived = 0
for name, old, new in MUTANTS:
    if original.count(old) != 1:
        print(f"{name}: PATTERN-NOT-UNIQUE ({original.count(old)})")
        survived += 1
        continue
    (base / GEN).write_text(original.replace(old, new), encoding="utf-8")
    st, ck = run(base, "--selftest"), run(base, "--check")
    tag = " (EQUIVALENT, not counted)" if name in EQUIVALENT else ""
    print(f"{name}: selftest {'KILLED' if st else 'SURVIVED'} (rc={st}); "
          f"check on real tree {'CAUGHT' if ck else 'PASSED'} (rc={ck}){tag}")
    if name not in EQUIVALENT:
        killed += bool(st)
        survived += not st
    subprocess.run(["git", "-C", str(base), "checkout", "-q", "--", "."], check=True)
(base / GEN).write_text(original, encoding="utf-8")
print(f"restored selftest rc={run(base, '--selftest')} check rc={run(base, '--check')}")

# The Git environment: --selftest under a hook's GIT_DIR / GIT_INDEX_FILE must pass and must not touch
# the repository those variables name, and the gate must still list the real tree.
victim = work / "victim"
if victim.exists():
    shutil.rmtree(victim)
subprocess.run(["git", "init", "-q", str(victim)], check=True)
index = victim / ".git" / "index"
before = index.read_bytes() if index.exists() else b""
hooked = dict(os.environ, GIT_DIR=str(victim / ".git"), GIT_WORK_TREE=str(victim), GIT_INDEX_FILE=str(index))
st, ck = run(base, "--selftest", env=hooked), run(base, "--check", env=hooked)
after = index.read_bytes() if index.exists() else b""
print(f"hook environment: selftest rc={st} check rc={ck}; victim index {'UNCHANGED' if before == after else 'CHANGED'}")
unsafe = original.replace(", env=git_environment())", ")")
(base / GEN).write_text(unsafe, encoding="utf-8")
st = run(base, "--selftest", env=hooked)
after = index.read_bytes() if index.exists() else b""
print(f"git-environment-not-cleaned under the hook environment: selftest {'KILLED' if st else 'SURVIVED'} (rc={st}); "
      f"victim index {'UNCHANGED' if before == after else 'CHANGED'}")
killed += bool(st)
survived += not st
(base / GEN).write_text(original, encoding="utf-8")
print(f"counted mutants: {killed + survived}, killed {killed}, survived {survived}")
