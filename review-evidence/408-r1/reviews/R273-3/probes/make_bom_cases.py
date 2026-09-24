#!/usr/bin/env python3
"""Hostile and control firmwares for the UTF-8 BOM spelling (R273-3).

GCC 14.3 skips a UTF-8 byte-order mark at the start of a file, so a
directive right after it is a directive to the compiler. Gate 1b's shared
directive anchor (`^[ \\t]*#`) does not skip U+FEFF. Each case below moves
ONE `#define` or `#include` to offset 0 behind a BOM; the rest is the
shipping firmware or a published R273-1 case (V2b, H4).

usage: make_bom_cases.py <repo-root> <published hostile.json> <out.json>
"""
import json
from pathlib import Path
import sys

BOM = "﻿"


def once(text, old, new):
    assert text.count(old) >= 1, old
    return text.replace(old, new, 1)


def main():
    root, hostile, out = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
    fw = (root / "sw/firmware/milan_baremetal/milan_baremetal.c").read_text(
        encoding="utf-8")
    published = {c["label"]: c["firmware"] for c in
                 json.loads(hostile.read_text(encoding="utf-8"))}
    v2b = next(v for k, v in published.items() if k.startswith("R273 V2b"))
    h4 = next(v for k, v in published.items() if k.startswith("R273 H4"))
    cat = "\n#define MILAN_CAT(a, b) a##b\n"
    guard = "\tif (id != MILAN_ID_MAGIC) {"
    verdict = "\taem_loaded = load_aem_image();\n"
    uart_tail = "\tprint_tod(gettime_ns());\n}"
    on = ("#define MILAN_ADP_ON() milan_write(MILAN_ADP_CTRL, "
          "milan_read(MILAN_ADP_CTRL) | 1u)")
    cases = [
        {"label": "B1 BOM: identity local forged by a ## paste whose "
                  "#define sits behind a BOM at offset 0 (V2b respelled)",
         "firmware": BOM + cat.strip("\n") + "\n" + once(v2b, cat, "\n")},
        {"label": "B1c control: the same paste #define at offset 0 with "
                  "no BOM (V2b respelled)",
         "firmware": cat.strip("\n") + "\n" + once(v2b, cat, "\n")},
        {"label": "B2 BOM: verdict overwritten by a ## paste whose #define "
                  "sits behind a BOM at offset 0 (H4 respelled)",
         "firmware": BOM + cat.strip("\n") + "\n" + once(h4, cat, "\n")},
        {"label": "B2c control: the same verdict overwrite through a plain "
                  "function-like macro, no paste, no BOM",
         "firmware": once(once(fw, verdict, verdict +
                               "\tMILAN_SETV(aem_loaded);\n"),
                          "#define MILAN_PTP_SNAPSHOT   0x4u\n",
                          "#define MILAN_PTP_SNAPSHOT   0x4u\n"
                          "#define MILAN_SETV(x) x = 1\n")},
        {"label": "B3 BOM: store primitive hidden in a macro behind a BOM, "
                  "invoked in a UART command handler",
         "firmware": BOM + on + "\n" + once(
             fw, uart_tail, "\tMILAN_ADP_ON();\n" + uart_tail)},
        {"label": "B3c control: the same macro with no BOM",
         "firmware": on + "\n" + once(
             fw, uart_tail, "\tMILAN_ADP_ON();\n" + uart_tail)},
        {"label": "B4 BOM: a twelfth #include <string.h> behind a BOM",
         "firmware": BOM + "#include <string.h>\n" + fw},
        {"label": "B4c control: the same #include with no BOM",
         "firmware": "#include <string.h>\n" + fw},
        {"label": "B5 BOM: a literal-address cast store macro behind a BOM, "
                  "invoked in a UART command handler",
         "firmware": BOM + "#define MILAN_POKE() (*(volatile unsigned int *)"
                     "0x90000600u = 1u)\n" + once(
                         fw, uart_tail, "\tMILAN_POKE();\n" + uart_tail)},
        {"label": "B6 BOM alone at offset 0, nothing else changed (benign "
                  "control)",
         "firmware": BOM + fw},
        {"label": "B7 BOM: #line behind a BOM",
         "firmware": BOM + "#line 1 \"milan_baremetal.c\"\n" + fw},
    ]
    out.write_text(json.dumps(cases, indent=1) + "\n", encoding="utf-8")
    print(f"{len(cases)} cases -> {out}")


if __name__ == "__main__":
    main()
