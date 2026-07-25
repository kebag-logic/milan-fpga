#!/usr/bin/env python3
"""Docs gate: markdown link integrity + wording deny-list.

Run from the repo root:

    python3 scripts/docs_check.py

Checks every git-tracked ``*.md`` file for:

1. **Link integrity** — every relative markdown link/image target resolves to
   a file or directory in the tree (http/mailto/anchor-only links are skipped).
2. **Wording deny-list** — terms that must not appear in committed docs.
   Spec/artifact identifiers that legitimately contain a denied substring are
   masked first (see ``ALLOW``).

Exit 0 = clean; exit 1 = findings, printed one per line as
``path:line: message``.
"""

import re
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent

# Exact substrings that are legitimate despite containing a denied stem:
# spec field names, schema/repo identifiers, third-party project names.
ALLOW = (
    "certification_version",        # Milan GET_MILAN_INFO wire field (Table 5.20)
    "milan-endstation-config",      # the builder's config-schema repo name
    "OpenAvnu",                     # third-party open-source project
    "openavnu",
)

DENY_CI = re.compile(r"avnu|aets|certif", re.IGNORECASE)
DENY_CS = re.compile(r"\bCERT\b")   # the old evidence token, case-sensitive

LINK_RE = re.compile(r"!?\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
CODE_FENCE_RE = re.compile(r"^\s*(```|~~~)")


def tracked_md():
    out = subprocess.run(
        ["git", "ls-files", "*.md"], cwd=REPO, capture_output=True, text=True,
        check=True,
    )
    return [REPO / p for p in out.stdout.splitlines() if p]


def check_file(path):
    findings = []
    rel = path.relative_to(REPO)
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except UnicodeDecodeError:
        return [f"{rel}:0: not valid UTF-8"]

    in_fence = False
    for lineno, line in enumerate(lines, 1):
        if CODE_FENCE_RE.match(line):
            in_fence = not in_fence

        # --- wording deny-list (applies everywhere, fences included) ---
        masked = line
        for allow in ALLOW:
            masked = masked.replace(allow, "#" * len(allow))
        m = DENY_CI.search(masked) or DENY_CS.search(masked)
        if m:
            findings.append(
                f"{rel}:{lineno}: denied wording '{m.group(0)}'"
            )

        # --- link integrity (markdown links only, skip code fences) ---
        if in_fence:
            continue
        for lm in LINK_RE.finditer(line):
            target = lm.group(1)
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            target = target.split("#", 1)[0]
            if not target:
                continue
            resolved = (path.parent / target).resolve()
            if not resolved.exists():
                findings.append(f"{rel}:{lineno}: broken link -> {target}")
    return findings


def main():
    findings = []
    for path in tracked_md():
        findings.extend(check_file(path))
    for f in findings:
        print(f)
    print(
        f"docs_check: {len(findings)} finding(s) across "
        f"{len(tracked_md())} tracked md files"
    )
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
