#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Render every embedded ```wavedrom block to a committed SVG.

GitHub renders Mermaid natively but NOT WaveDrom, so each block's rendered SVG is
committed under docs/diagrams/wavedrom/ and embedded by the host document; the fenced
JSON stays the editable source (collapsed in a <details> right below the image).

Naming: each block takes the id of the nearest preceding `<a id="fig-..."></a>` anchor
in its document -> docs/diagrams/wavedrom/<anchor>.svg.

Modes:
  render (default) - (re)write all SVGs
  --check          - fail if any committed SVG differs from a fresh render
                     (the wavedrompy output is deterministic)

Uses the `wavedrom` Python package (wavedrompy). If it is not importable, a local
virtualenv is bootstrapped at .venv-wavedrom/ (gitignored) and the script re-executes
itself inside it.
"""
import os
import re
import subprocess
import sys
from pathlib import Path

SELF = Path(__file__).resolve()
ROOT = SELF.parent.parent
OUTDIR = ROOT / "docs" / "diagrams" / "wavedrom"
VENV = ROOT / ".venv-wavedrom"
ANCHOR = re.compile(r'<a id="(fig-[a-z0-9-]+)"></a>')


def ensure_wavedrom() -> None:
    """Guarantee `wavedrom` is importable, re-executing this script if it is not.

    A host without wavedrompy gets a one-time .venv-wavedrom bootstrap and the
    script restarts inside it, so the same command works on a fresh checkout
    and in CI without anyone being told to pip-install first.
    """
    try:
        import wavedrom  # noqa: F401
        return
    except ModuleNotFoundError:
        pass
    vpy = VENV / "bin" / "python"
    if not vpy.exists():
        print("bootstrapping .venv-wavedrom (one-time) ...")
        import venv
        venv.create(VENV, with_pip=True)
        subprocess.run([str(vpy), "-m", "pip", "install", "--quiet",
                        "wavedrom"], check=True)
    # `.resolve()` on both sides, as `os.path.realpath` did: the venv's
    # `bin/python` is a symlink, so the comparison is between interpreters and
    # not between the two spellings of one.
    if Path(sys.executable).resolve() != vpy.resolve():
        os.execv(vpy, [str(vpy), str(SELF)] + sys.argv[1:])


def collect_blocks() -> list[tuple[Path, str, str]]:
    """-> list of (md_path, anchor, json_source)"""
    blocks = []
    for base_dir, _dirs, files in os.walk(ROOT / "docs"):
        base = Path(base_dir)
        if base.is_relative_to(OUTDIR):   # OUTDIR itself included
            continue
        for name in sorted(files):
            if not name.endswith(".md"):
                continue
            path = base / name
            anchor, inblock, buf = None, False, []
            with path.open(encoding="utf-8") as fh:
                for line in fh:
                    if not inblock:
                        m = ANCHOR.search(line)
                        if m:
                            anchor = m.group(1)
                        if line.rstrip() == "```wavedrom":
                            if anchor is None:
                                sys.exit(f"FAIL: wavedrom block without a preceding "
                                         f"fig anchor in {path}")
                            inblock, buf = True, []
                    elif line.rstrip() == "```":
                        blocks.append((path, anchor, "".join(buf)))
                        inblock = False
                    else:
                        buf.append(line)
    dupes = {a for _, a, _ in blocks
             if sum(1 for _, b, _ in blocks if b == a) > 1}
    if dupes:
        sys.exit(f"FAIL: anchor(s) used by more than one wavedrom block: {dupes}")
    return blocks


def main() -> int:
    """Render every embedded block, or under --check name the anchors whose
    committed SVG no longer matches a fresh render (exit 1)."""
    ensure_wavedrom()
    import wavedrom

    check = "--check" in sys.argv
    OUTDIR.mkdir(parents=True, exist_ok=True)
    blocks, stale = collect_blocks(), []
    for path, anchor, src in blocks:
        try:
            svg = wavedrom.render(src).tostring()
        except Exception as exc:
            sys.exit(f"FAIL: {anchor} in {path.relative_to(ROOT)}: {exc}")
        out = OUTDIR / f"{anchor}.svg"
        old = out.read_text(encoding="utf-8") if out.exists() else None
        if check:
            if svg != old:
                stale.append(anchor)
        elif svg != old:
            out.write_text(svg, encoding="utf-8")
            print(f"rendered {out.relative_to(ROOT)}")

    if check and stale:
        print(f"WAVEDROM STALE: {', '.join(stale)} "
              f"(run: python3 scripts/render-wavedrom.py)")
        return 1
    print(f"wavedrom: {len(blocks)} blocks "
          f"{'checked, OK' if check else 'rendered'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
