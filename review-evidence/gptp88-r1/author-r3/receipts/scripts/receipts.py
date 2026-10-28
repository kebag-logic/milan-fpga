"""Copy gate records into the output directory as receipts, without host paths.

usage: receipts.py copy <src file> <dest file>
       receipts.py results <runner results.json> <dest file>
       receipts.py index <receipts dir>

Every copied text has its host paths replaced by named placeholders. A file
that would exceed the size cap keeps its head and tail plus the sha256 of
the complete sanitised text, and says so in its first line.
"""
import hashlib
import json
import re
import sys
from pathlib import Path

CAP = 190_000
S = "<scratch>"
VROOT = ("<home>/.local/share/containers/storage/overlay/"
         "9517af577e2019496be7a9f3df0cdeafba0a4f827989b59cb358abf6403fbbde/diff")
SUBS = [
    (f"{VROOT}/usr/share/verilator", "<verilator-5.050-root>"),
    (f"{VROOT}/usr/bin/verilator", "<verilator-5.050>"),
    (VROOT, "<verilator-5.050-image>"),
    (f"{S}/repo-head", "<repo-head>"),
    (f"{S}/repo-base", "<repo-base>"),
    (f"{S}/pA", "<parent-head-A>"),
    (f"{S}/pB", "<parent-head-B>"),
    (f"{S}/pC", "<parent-head-C>"),
    (f"{S}/pD", "<parent-head-D>"),
    (f"{S}/pF", "<parent-head-fuzz>"),
    (f"{S}/bA", "<parent-base>"),
    (f"{S}/bF", "<parent-base-fuzz>"),
    (f"{S}/mut", "<parent-mut>"),
    (f"{S}/try1", "<parent-try>"),
    (f"{S}/try-s1", "<parent-base-try>"),
    (f"{S}/parent-work", "<parent-work>"),
    (f"{S}/pinned-tool-bin", "<pinned-tools>"),
    (f"{S}/tsn-gen", "<tsn-gen-pinned>"),
    (f"{S}/tmp", "<tmp>"),
    (S, "<scratch>"),
    ("<lane>", "<lane>"),
    ("<tools>", "<tools>"),
    ("<tsn-gen-local>", "<tsn-gen-local>"),
    ("<user-bin>", "<user-bin>"),
    ("<management>", "<management>"),
    ("<home>", "<home>"),
    ("<data>", "<data>"),
]
LEFTOVER = re.compile(r"/(?:home|data|tmp|root|Users)/[A-Za-z0-9._-]+")


def clean(text: str) -> str:
    for a, b in SUBS:
        text = text.replace(a, b)
    text = text.replace("<user>", "<user>")
    return LEFTOVER.sub("<path>", text)


def write_capped(text: str, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    data = text.encode()
    if len(data) <= CAP:
        dest.write_bytes(data)
        return
    digest = hashlib.sha256(data).hexdigest()
    lines = text.splitlines(keepends=True)
    head, tail, size = [], [], 0
    for line in lines:
        if size > CAP * 0.35:
            break
        head.append(line); size += len(line.encode())
    size = 0
    for line in reversed(lines[len(head):]):
        if size > CAP * 0.55:
            break
        tail.insert(0, line); size += len(line.encode())
    cut = len(lines) - len(head) - len(tail)
    note = (f"[receipt trimmed: {len(lines)} lines, {len(data)} bytes, "
            f"sha256 {digest}; first {len(head)} and last {len(tail)} lines "
            f"kept, {cut} omitted]\n")
    dest.write_text(note + "".join(head) +
                    f"\n[... {cut} lines omitted ...]\n\n" + "".join(tail))


def main() -> None:
    mode = sys.argv[1]
    if mode == "copy":
        write_capped(clean(Path(sys.argv[2]).read_text(errors="replace")),
                     Path(sys.argv[3]))
    elif mode == "results":
        d = json.loads(Path(sys.argv[2]).read_text())
        for row in d["results"]:
            row["command"] = [clean(a) for a in row["command"]]
            row["log"] = Path(row["log"]).name
        write_capped(clean(json.dumps(d, indent=2)) + "\n", Path(sys.argv[3]))
    elif mode == "index":
        root = Path(sys.argv[2])
        rows = []
        for p in sorted(root.rglob("*")):
            if p.is_file() and p.name != "INDEX.md":
                b = p.read_bytes()
                rows.append(f"| `{p.relative_to(root)}` | {len(b)} | "
                            f"`{hashlib.sha256(b).hexdigest()[:16]}` |")
        (root / "INDEX.md").write_text(
            "# Receipt index\n\nGenerated from the files present in this "
            "directory (path, bytes, sha256 prefix).\n\n"
            "| File | Bytes | sha256 |\n|---|---:|---|\n" + "\n".join(rows) + "\n")
        print(len(rows), "files indexed")


main()
