"""Redact host paths in the round's receipts, then write receipts/INDEX.md from the files present."""
import hashlib
import pathlib
import sys

SUBST = (
    ("$WORKSPACE_HOME/litex-milan/venv", "$LITEX_VENV"),
    ("$WORKSPACE_HOME/br-milan-rv32", "$RV32_SDK"),
    ("/tmp/a683zp-mdvenv", "$DOCS_VENV"),
    ("/tmp/a683zp-tmp", "$TMPDIR"),
    ("$LANES/665-s2b-cycles", "$LANE"),
)


def main() -> int:
    """Redact every receipt in place and write the index; return 0."""
    out = pathlib.Path(sys.argv[1])
    receipts = out / "receipts"
    for path in sorted([*receipts.rglob("*"), *(out / "scripts").glob("*.sh")]):
        if not path.is_file() or path.name == "INDEX.md":
            continue
        text = path.read_text(encoding="utf-8")
        for old, new in SUBST:
            text = text.replace(old, new)
        path.write_text(text, encoding="utf-8")
    rows = ["# Receipts index", "",
            "Generated from the files present. Host paths are redacted: "
            + ", ".join(f"`{new}`" for _, new in SUBST) + ".", "",
            "| File | Bytes | sha256 |", "|---|---:|---|"]
    for path in sorted(out.rglob("*")):
        if not path.is_file() or path.name == "INDEX.md":
            continue
        data = path.read_bytes()
        rows.append(f"| `{path.relative_to(out)}` | {len(data):,} | `{hashlib.sha256(data).hexdigest()}` |")
    (receipts / "INDEX.md").write_text("\n".join(rows) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
