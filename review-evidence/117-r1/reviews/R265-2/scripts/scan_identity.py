#!/usr/bin/env python3
"""Residual bench-identity scan for the issue 117 evidence archive.

usage: scan_identity.py <pre-redaction-dir> <pinned-dir> <repo-checkout> [<extra-dir>...]

The token set is DERIVED, never spelled: every byte run the redaction
changed between the pre-redaction commit and the pinned commit is widened
to its alphanumeric word(s), and each word of three or more characters
that the replacement text does not also carry becomes a token. The pinned
archive (contents and file names) and every extra directory are then
searched for each token in three encodings: raw bytes, lowercase hex and
uppercase hex of its ASCII bytes. The repository's own privacy rules
(SCRUB_RULES in scripts/docs_check.py) are applied to text in the same
scan. A token the repository's own tracked Markdown already spells as a
word (a board model, a host role name) is reported as repository-public
and its hits are listed separately; only the remaining private tokens and
the SCRUB_RULES classes count as residual identity. Output names tokens
only by index and length and rules only by class, so this script and its
output republish nothing.
Exit 0 when nothing is found, 1 otherwise.
"""
import importlib.util
import json
import re
import sys
from pathlib import Path

WORD = re.compile(rb"[A-Za-z0-9]+")


def runs(x: bytes, y: bytes):
    """(start, end) of differing runs for equal-length inputs."""
    out = []
    i, n = 0, len(x)
    while i < n:
        if x[i] != y[i]:
            j = i
            while j < n and x[j] != y[j]:
                j += 1
            out.append((i, j))
            i = j
        else:
            i += 1
    return out


def widen(b: bytes, s: int, e: int):
    while s > 0 and (chr(b[s - 1]).isalnum()):
        s -= 1
    while e < len(b) and chr(b[e]).isalnum():
        e += 1
    return s, e


def derive_tokens(pre: Path, pin: Path):
    man = json.loads((pin / "MANIFEST.json").read_text())
    toks = set()
    for ent in man:
        if not ent.get("identity_redacted"):
            continue
        x = (pre / ent["file"]).read_bytes()
        y = (pin / ent["file"]).read_bytes()
        if len(x) == len(y):
            for s, e in runs(x, y):
                s2, e2 = widen(x, s, e)
                orig = set(WORD.findall(x[s2:e2]))
                repl = set(WORD.findall(y[s2:e2]))
                toks |= {w for w in orig - repl if len(w) >= 3}
        else:
            # Unequal length: align on common prefix/suffix per line.
            xl, yl = x.split(b"\n"), y.split(b"\n")
            if len(xl) != len(yl):
                continue
            for a, b in zip(xl, yl):
                if a == b:
                    continue
                p = 0
                while p < min(len(a), len(b)) and a[p] == b[p]:
                    p += 1
                q = 0
                while q < min(len(a), len(b)) - p and a[-1 - q] == b[-1 - q]:
                    q += 1
                s2, e2 = widen(a, p, len(a) - q)
                orig = set(WORD.findall(a[s2:e2]))
                repl = set(WORD.findall(b[p:len(b) - q]))
                toks |= {w for w in orig - repl if len(w) >= 3}
    # Drop tokens that are ordinary content of files the redaction never
    # touched in the same form (pure hex, numbers, generic words).
    return sorted(t for t in toks if not re.fullmatch(rb"[0-9a-f]+|[0-9]+", t))


def load_rules(docs_check: Path):
    spec = importlib.util.spec_from_file_location("docs_check", docs_check)
    mod = importlib.util.module_from_spec(spec)
    sys.argv, saved = [str(docs_check)], sys.argv
    try:
        spec.loader.exec_module(mod)
    finally:
        sys.argv = saved
    return mod.SCRUB_RULES


def scan(root: Path, label: str, tokens, rules, hits):
    for p in sorted(root.rglob("*")):
        if not p.is_file():
            continue
        rel = str(p.relative_to(root))
        data = p.read_bytes()
        for k, t in enumerate(tokens):
            forms = {"raw": t, "hex": t.hex().encode(), "HEX": t.hex().upper().encode()}
            for fname, needle in forms.items():
                c = data.count(needle)
                if c:
                    hits.append((label, rel, f"token#{k}(len {len(t)})", fname, c))
            if t in rel.encode():
                hits.append((label, rel, f"token#{k}(len {len(t)})", "file name", 1))
        text = data.decode("utf-8", "replace")
        for rx, cls, _fix in rules:
            c = len(rx.findall(text)) + len(rx.findall(rel))
            if c:
                hits.append((label, rel, f"rule:{cls}", "text", c))


def repo_public(repo: Path, tokens):
    import subprocess
    md = subprocess.run(["git", "-C", str(repo), "ls-files", "*.md"],
                        capture_output=True, text=True, check=True).stdout.split()
    blob = b"\n".join((repo / f).read_bytes() for f in md if (repo / f).is_file())
    return {t for t in tokens if re.search(rb"(?<![A-Za-z0-9])" + re.escape(t) + rb"(?![A-Za-z])", blob)}


def main() -> int:
    pre, pin, repo = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
    extras = [Path(a) for a in sys.argv[4:]]
    tokens = derive_tokens(pre, pin)
    rules = load_rules(repo / "scripts" / "docs_check.py")
    public = repo_public(repo, tokens)
    print(f"derived tokens: {len(tokens)} (lengths {[len(t) for t in tokens]})")
    print(f"repository-public tokens (spelled in tracked Markdown): "
          f"{[f'token#{k}' for k, t in enumerate(tokens) if t in public]}")
    print(f"docs_check SCRUB_RULES classes: {[c for _r, c, _f in rules]}")
    hits = []
    scan(pin, "pinned", tokens, rules, hits)
    for ex in extras:
        scan(ex, str(ex), tokens, rules, hits)
    pub_ids = {f"token#{k}(len {len(t)})" for k, t in enumerate(tokens) if t in public}
    residual = [h for h in hits if h[2] not in pub_ids]
    info = [h for h in hits if h[2] in pub_ids]
    for h in residual:
        print("HIT", *h)
    print(f"repository-public token hits (not counted): {len(info)} in "
          f"{len({(h[0], h[1]) for h in info})} files")
    print(f"residual hits: {len(residual)} in {len({(h[0], h[1]) for h in residual})} files")
    print("RESULT:", "CLEAN" if not residual else "RESIDUAL IDENTITY FOUND")
    return 0 if not residual else 1


if __name__ == "__main__":
    sys.exit(main())
