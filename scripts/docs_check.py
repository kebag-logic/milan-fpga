#!/usr/bin/env python3
"""Docs gate: link integrity + wording deny-list + bare references + local info.

Run from the repo root:

    python3 scripts/docs_check.py

Checks, over every git-tracked ``*.md`` file:

1. **Link integrity** — every relative markdown link/image target resolves to
   a file or directory in the tree (http/mailto/anchor-only links skipped).
2. **Wording deny-list** — terms that must not appear in committed docs.
   Legitimate identifiers containing a denied stem are masked (``ALLOW``).
3. **Bare doc references** — a mention of an existing tracked ``.md`` file
   that is not an actual markdown link (living tree only; generated files,
   code fences, HTML comments and ``historical_now_obsolete/`` are exempt).
4. **Local information** — bench/host-identifying patterns (hostnames, home
   paths, bench subnet, MAC-derived interface names, USB-serial paths) must
   not appear; also swept over ``docs/**`` diagram sources (``.gen.py``,
   ``.drawio``).

Exit 0 = clean; exit 1 = findings, one per line as ``path:line: message``.
"""

import re
import subprocess
import sys
from collections import Counter
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

# Bench/host-identifying patterns (generic shapes only — never the literals).
LOCAL_RE = re.compile(
    r"amx-|/home/alex|enx[0-9a-f]{8,}|serial/by-id/usb-[A-Za-z0-9]|192\.168\.127"
)

LINK_RE = re.compile(r"!?\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
LINK_SPAN_RE = re.compile(r"!?\[[^\]]*\]\([^)]*\)")
FENCE_RE = re.compile(r"^\s*(```|~~~)")
CAND_RE = re.compile(r"(?<![\w/.-])((?:[\w.-]+/)*[\w][\w.-]*\.md)\b")
GENERATED_MARK = re.compile(r"GENERATED", re.IGNORECASE)


def tracked(pattern):
    out = subprocess.run(["git", "ls-files", pattern], cwd=REPO,
                         capture_output=True, text=True, check=True)
    return [p for p in out.stdout.splitlines() if p]


def norm_join(base, ref):
    parts = []
    for seg in (str(base) + "/" + ref).replace("\\", "/").split("/"):
        if seg == "..":
            if parts:
                parts.pop()
            else:
                return None
        elif seg not in (".", ""):
            parts.append(seg)
    return "/".join(parts)


def make_resolver(tracked_md):
    tracked_set = set(tracked_md)
    by_base = Counter(Path(p).name for p in tracked_md)

    def resolve(ref, filedir):
        for base in (filedir, Path("."), Path("docs")):
            n = norm_join(base, ref)
            if n and n in tracked_set:
                return n
        if "/" not in ref and by_base.get(ref, 0) == 1:
            for p in tracked_md:
                if Path(p).name == ref:
                    return p
        return None

    return resolve


def check_md(path, relpath, resolve):
    findings = []
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return [f"{relpath}:0: not valid UTF-8"]
    lines = text.splitlines()
    generated = bool(GENERATED_MARK.search(text[:400]))
    historical = relpath.startswith("historical_now_obsolete/")
    filedir = Path(relpath).parent

    in_fence = in_comment = False
    for lineno, line in enumerate(lines, 1):
        if FENCE_RE.match(line):
            in_fence = not in_fence

        # --- wording deny-list + local info (everywhere, fences included) ---
        masked = line
        for allow in ALLOW:
            masked = masked.replace(allow, "#" * len(allow))
        m = DENY_CI.search(masked) or DENY_CS.search(masked)
        if m:
            findings.append(f"{relpath}:{lineno}: denied wording '{m.group(0)}'")
        lm = LOCAL_RE.search(line)
        if lm:
            findings.append(f"{relpath}:{lineno}: local info '{lm.group(0)}'")

        if in_fence:
            continue
        if "<!--" in line and "-->" not in line:
            in_comment = True
            continue
        if in_comment:
            if "-->" in line:
                in_comment = False
            continue

        # --- link integrity ---
        for lk in LINK_RE.finditer(line):
            target = lk.group(1)
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            target = target.split("#", 1)[0]
            if not target:
                continue
            resolved = (path.parent / target).resolve()
            if not resolved.exists():
                findings.append(f"{relpath}:{lineno}: broken link -> {target}")

        # --- bare doc references (living, non-generated files only) ---
        if generated or historical:
            continue
        stripped = LINK_SPAN_RE.sub(" ", line)
        for cm in CAND_RE.finditer(stripped):
            ref = cm.group(1)
            if ref == Path(relpath).name and "/" not in ref:
                continue
            target = resolve(ref, filedir)
            if target and target != relpath:
                findings.append(
                    f"{relpath}:{lineno}: bare reference to {target} — make it a link"
                )
    return findings


def main():
    findings = []
    md = tracked("*.md")
    resolve = make_resolver(md)
    for rel in md:
        findings.extend(check_md(REPO / rel, rel, resolve))
    # local-info sweep over diagram sources (text formats only)
    for pattern in ("docs/*.gen.py", "docs/**/*.gen.py", "docs/*.drawio",
                    "docs/**/*.drawio"):
        for rel in tracked(pattern):
            for lineno, line in enumerate(
                    (REPO / rel).read_text(encoding="utf-8",
                                           errors="replace").splitlines(), 1):
                lm = LOCAL_RE.search(line)
                if lm:
                    findings.append(f"{rel}:{lineno}: local info '{lm.group(0)}'")
    findings = sorted(set(findings))
    for f in findings:
        print(f)
    print(f"docs_check: {len(findings)} finding(s) across {len(md)} tracked md files")
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
