#!/usr/bin/env python3
"""Composition fault probes for PR #522 in the #439 + #520 merge-train candidate.

Run against a DISPOSABLE checkout of the candidate (never the review clone):

    python3 probes.py <disposable-candidate-checkout> <receipt-dir>

Each probe edits one file in the working tree, runs the gate that reads it,
records the exit status and diagnostic, restores the file from HEAD and
proves the tree is clean again. No commit is made.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

RTL = ".github/workflows/rtl.yml"
POLICY = "docs/testing/CI_WORKFLOWS.md"
SHARD_RUN = "      - name: Run this weighted portability shard\n        run: |\n"
PR_COMMENT_HEAD = "      # THE RESULT CACHE (#350): a top is skipped and reports the stored\n"
PR_SOURCE = "d253f86e410e301d146d4bd4e74d027f00cfb462"   # this PR's head, no #439
PRED_439 = "f01f237d4b48c7b1ed59c80aca51430901791624"   # #439's head, no #520


def sh(repo: Path, *cmd: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, cwd=repo, capture_output=True, text=True,
                          env={"PYTHONDONTWRITEBYTECODE": "1", "PATH": "/usr/bin:/bin"})


def replace_once(text: str, old: str, new: str) -> str:
    if text.count(old) != 1:
        raise SystemExit(f"fixture drift: {old!r} occurs {text.count(old)} times")
    return text.replace(old, new)


def mutate_text(repo: Path, rel: str, old: str, new: str) -> None:
    path = repo / rel
    path.write_text(replace_once(path.read_text(encoding="utf-8"), old, new), encoding="utf-8")


def replace_blob(repo: Path, rel: str, rev: str) -> None:
    blob = sh(repo, "git", "show", f"{rev}:{rel}")
    if blob.returncode:
        raise SystemExit(blob.stderr)
    (repo / rel).write_text(blob.stdout, encoding="utf-8")


PROBES = [
    {
        "id": "P1",
        "what": "#439 content pin x this PR's rtl.yml edit: the same kind of comment placed "
                "INSIDE the yosys-shards run body instead of between steps",
        "expect": "refused",
        "file": RTL,
        "apply": lambda r: mutate_text(r, RTL, SHARD_RUN,
                                       SHARD_RUN + "          # the generated ROM bundle (#520) is in the key\n"),
        "gate": ["python3", "scripts/ci_events.py", "--check"],
    },
    {
        "id": "P2",
        "what": "control for P1: an extra YAML comment line between steps, where this PR put its "
                "comment",
        "expect": "accepted",
        "file": RTL,
        "apply": lambda r: mutate_text(r, RTL, PR_COMMENT_HEAD,
                                       "      # probe: extra between-step comment\n" + PR_COMMENT_HEAD),
        "gate": ["python3", "scripts/ci_events.py", "--check"],
    },
    {
        "id": "P3",
        "what": "#350 policy mark in the result-cache paragraph this PR edited: drop "
                "`syn/yosys/result_cache.py` from the composed page",
        "expect": "refused",
        "file": POLICY,
        "apply": lambda r: mutate_text(r, POLICY,
                                       "`syn/yosys/result_cache.py`, which refuses an entry",
                                       "the cache helper, which refuses an entry"),
        "gate": ["python3", "scripts/ci_events.py", "--check"],
    },
    {
        "id": "P4",
        "what": "mis-merge model: shared page taken from this PR's source head (drops #439's prose)",
        "expect": "informational",
        "file": POLICY,
        "apply": lambda r: replace_blob(r, POLICY, PR_SOURCE),
        "gate": ["python3", "scripts/ci_events.py", "--check"],
    },
    {
        "id": "P5",
        "what": "mis-merge model: shared page taken from #439's head (drops this PR's prose)",
        "expect": "informational",
        "file": POLICY,
        "apply": lambda r: replace_blob(r, POLICY, PRED_439),
        "gate": ["python3", "scripts/ci_events.py", "--check"],
    },
    {
        "id": "P6",
        "what": "same as P5, through the docs gates that read the page",
        "expect": "informational",
        "file": POLICY,
        "apply": lambda r: replace_blob(r, POLICY, PRED_439),
        "gate": ["bash", "-c", "python3 scripts/docs_check.py && python3 scripts/gen_toc.py --check "
                               "&& python3 scripts/check_doc_style.py"],
    },
]


def main() -> int:
    repo = Path(sys.argv[1]).resolve()
    out = Path(sys.argv[2]).resolve()
    out.mkdir(parents=True, exist_ok=True)
    head = sh(repo, "git", "rev-parse", "HEAD").stdout.strip()
    if head != "2a77ace7d98cda18ece9f7aba9c4a408850eb926":
        raise SystemExit(f"not the candidate: {head}")
    if sh(repo, "git", "status", "--porcelain").stdout:
        raise SystemExit("disposable checkout is not clean")
    base = sh(repo, *PROBES[0]["gate"])
    rows = [{"id": "P0", "what": "unmutated candidate", "expect": "accepted",
             "exit": base.returncode, "tail": (base.stdout + base.stderr).strip().splitlines()[-1:]}]
    (out / "P0.log").write_text(base.stdout + base.stderr, encoding="utf-8")
    for probe in PROBES:
        probe["apply"](repo)
        diffstat = sh(repo, "git", "diff", "--stat").stdout.strip()
        res = sh(repo, *probe["gate"])
        text = res.stdout + res.stderr
        (out / f"{probe['id']}.log").write_text(
            f"$ {' '.join(probe['gate'])}\n[mutation] {diffstat}\n{text}[exit {res.returncode}]\n",
            encoding="utf-8")
        sh(repo, "git", "checkout", "--", probe["file"])
        clean = not sh(repo, "git", "status", "--porcelain").stdout
        findings = [ln.strip() for ln in text.splitlines()
                    if ln.strip().startswith(("FAIL", "fail", "ERROR", "x ", "✗")) or "must" in ln][:4]
        rows.append({"id": probe["id"], "what": probe["what"], "expect": probe["expect"],
                     "exit": res.returncode, "restored_clean": clean,
                     "tail": text.strip().splitlines()[-1:], "diagnostics": findings})
        if not clean:
            raise SystemExit(f"{probe['id']}: restore failed")
    (out / "probes.json").write_text(json.dumps(rows, indent=2) + "\n", encoding="utf-8")
    for row in rows:
        print(f"{row['id']}\texit={row['exit']}\texpect={row['expect']}\t{row['tail']}")
    ok = (rows[0]["exit"] == 0 and rows[1]["exit"] != 0 and rows[2]["exit"] == 0
          and rows[3]["exit"] != 0)
    print("PROBES", "AS-EXPECTED" if ok else "UNEXPECTED")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
