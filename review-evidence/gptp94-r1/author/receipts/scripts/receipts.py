"""Copy receipts into the output directory with host details replaced, and
index every file present there.

usage: receipts.py copy <src> <dest under receipts/>   one file
       receipts.py index                               write receipts/INDEX.md
A file over LIMIT bytes after scrubbing is stored as a digest: its first and
last 60 lines plus every verdict line, with the full file's size and SHA-256.
"""
import hashlib
import re
import socket
import sys
from pathlib import Path

OUT = Path("<management>/2026-09-23/gptp94-a695")
REC = OUT / "receipts"
LIMIT = 190_000
VROOT = ("<home>/.local/share/containers/storage/overlay/"
         "9517af577e2019496be7a9f3df0cdeafba0a4f827989b59cb358abf6403fbbde/diff/usr")
SUBS = [
    (VROOT + "/share/verilator", "<verilator-5.050-root>"),
    (VROOT + "/bin/verilator", "<verilator-5.050-bin>"),
    (VROOT, "<verilator-5.050>"),
    ("<scratch>", "<scratch>"),
    ("<lane>", "<lane>"),
    ("<management>", "<management>"),
    ("<vivado-install>", "<vivado-install>"),
    ("<projects>", "<projects>"),
    ("<user-bin>", "<user-bin>"),
    ("<home>", "<home>"),
    ("<tools>", "<tools>"),
    ("<data>", "<data>"),
    ("<run-user>", "<run-user>"),
]
HOST = socket.gethostname()
VERDICT = re.compile(r"(\[PASS\]|\[FAIL\]|FAIL |checks:|RESULT|PASS|rc=|caught|SURVIVED)")


def scrub(text: str) -> str:
    for a, b in SUBS:
        text = text.replace(a, b)
    if HOST:
        text = re.sub(re.escape(HOST), "<host>", text)
    text = re.sub(r"\balex\b", "<user>", text)
    return text


def copy(src: Path, dest: Path) -> None:
    raw = src.read_bytes()
    text = scrub(raw.decode("utf-8", errors="replace"))
    data = text.encode()
    if len(data) > LIMIT:
        lines = text.splitlines()
        keep = lines[:60] + ["", "[... digest: verdict lines only ...]", ""]
        keep += [l for l in lines[60:-60] if VERDICT.search(l)][:3000]
        keep += ["", "[... last 60 lines ...]", ""] + lines[-60:]
        head = (f"DIGEST of {scrub(str(src))}: {len(raw)} bytes, sha256 "
                f"{hashlib.sha256(raw).hexdigest()}; the full log stays in scratch\n")
        data = (head + "\n".join(keep) + "\n").encode()
        if len(data) > LIMIT:
            data = data[:LIMIT - 64] + b"\n[... truncated at the receipt size limit ...]\n"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(data)


def index() -> None:
    rows = []
    for p in sorted(REC.rglob("*")):
        if p.is_file() and p.name != "INDEX.md":
            b = p.read_bytes()
            rows.append(f"| `{p.relative_to(REC)}` | {len(b)} | `{hashlib.sha256(b).hexdigest()[:16]}` |")
    body = ["# Receipts index", "",
            "Generated from the files present under `receipts/`.", "",
            "Host paths are replaced by named placeholders such as `<scratch>` and `<lane>`.", "",
            "| File | Bytes | SHA-256 prefix |", "|---|---:|---|"] + rows
    (REC / "INDEX.md").write_text("\n".join(body) + "\n")
    print(len(rows), "files indexed")


if __name__ == "__main__":
    if sys.argv[1] == "copy":
        copy(Path(sys.argv[2]), REC / sys.argv[3])
    else:
        index()
