#!/usr/bin/env python3
"""Replace host-identifying path prefixes in published receipts with placeholders.

Only the listed literal prefixes are rewritten; every other byte is kept.
usage: sanitize_receipts.py <packet-dir> <clone-dir> <pinned-tool-bin> <verilator-prefix>
"""
import os
import re
import sys


def main() -> int:
    packet, clone, toolbin, vprefix = sys.argv[1:5]
    home = os.path.expanduser("~")
    subs = [
        (re.compile(r"PATH=" + re.escape(toolbin) + r":\S*"), "PATH=<pinned-tool-bin>:$PATH"),
        (re.compile(re.escape(vprefix)), "<verilator-5.050-prefix>"),
        (re.compile(re.escape(toolbin)), "<pinned-tool-bin>"),
        (re.compile(re.escape(clone)), "<clone>"),
        (re.compile(re.escape(packet)), "<packet>"),
        (re.compile(re.escape(home)), "$HOME"),
    ]
    changed = 0
    for root, dirs, files in os.walk(os.path.join(packet, "receipts")):
        for name in files:
            path = os.path.join(root, name)
            with open(path, "rb") as fh:
                text = fh.read().decode("utf-8", "surrogateescape")
            new = text
            for rx, rep in subs:
                new = rx.sub(lambda _m, r=rep: r, new)
            if new != text:
                with open(path, "wb") as fh:
                    fh.write(new.encode("utf-8", "surrogateescape"))
                changed += 1
                print("sanitized", os.path.relpath(path, packet))
    print(f"{changed} file(s) rewritten")
    return 0


if __name__ == "__main__":
    sys.exit(main())
