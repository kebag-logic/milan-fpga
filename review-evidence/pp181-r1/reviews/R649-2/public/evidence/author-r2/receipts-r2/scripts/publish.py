#!/usr/bin/env python3
"""Copy round-2 receipts into the output directory (issue #181).

usage: publish.py <dest-root> <subdir> <source> [<source> ...]
Each source file or directory is copied under <dest-root>/<subdir>/. A text
file of at most 200 KB is copied with host paths redacted (<home>, <data>,
<slots>, <host>); anything larger, or binary, is not copied and is listed in
<dest-root>/LARGE.tsv with its sha256, size and scratch path (redacted). The
redaction is the only edit, and each copied file's raw sha256 is kept in
<dest-root>/RAW.sha256.
"""
import hashlib
import re
import socket
import sys
from pathlib import Path

LIMIT = 200 * 1024
SUBS = [("<home>", "<home>"), ("<data>", "<data>"), ("<slots>", "<slots>"),
        (socket.gethostname(), "<host>")]
KEY = re.compile(r"ERROR|CRITICAL|WNS|Slack|Logic Levels|report_|Command:|^source |rc=|"
                 r"Timing constraints|All user specified timing|proven|FAIL|PASS")
SKIP_DIRS = {".Xil", "__pycache__", "obj_dir", "obj_idn", "obj_if2"}


def redact(text: str) -> str:
    for old, new in SUBS:
        text = text.replace(old, new)
    return text


def excerpt(text: str, digest: str, size: int, dest: Path) -> None:
    """A large text log's first 80 lines, its key lines and its last 40 lines."""
    lines = text.splitlines()
    keys = [f"{i + 1}: {l}" for i, l in enumerate(lines)
            if KEY.search(l)][:400]
    body = [f"# excerpt: full file sha256 {digest}, {size} bytes, kept in scratch",
            "# --- first 80 lines", *lines[:80], "# --- key lines (line: text)", *keys,
            "# --- last 40 lines", *lines[-40:]]
    out = redact("\n".join(body) + "\n")
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(out[:LIMIT])


def main() -> int:
    root = Path(sys.argv[1])
    sub = sys.argv[2]
    large = (root / "LARGE.tsv").open("a")
    raw = (root / "RAW.sha256").open("a")
    for src in map(Path, sys.argv[3:]):
        files = [src] if src.is_file() else sorted(p for p in src.rglob("*") if p.is_file())
        for f in files:
            if any(part in SKIP_DIRS for part in f.parts):
                continue
            rel = f.name if src.is_file() else f.relative_to(src.parent).as_posix()
            data = f.read_bytes()
            digest = hashlib.sha256(data).hexdigest()
            dest = root / sub / rel
            try:
                text = data.decode("utf-8")
            except UnicodeDecodeError:
                text = None
            if text is None or len(data) > LIMIT:
                large.write(f"{digest}\t{len(data)}\t{sub}/{rel}\t{redact(str(f))}\n")
                if text is not None:
                    excerpt(text, digest, len(data), dest.with_name(dest.name + ".excerpt.txt"))
                continue
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_text(redact(text))
            raw.write(f"{digest}  {sub}/{rel}\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
