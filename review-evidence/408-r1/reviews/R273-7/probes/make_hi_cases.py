#!/usr/bin/env python3
"""Hostile and control firmwares for R273-4: a header name in
`__has_include(<...>)` that holds `/*`.

GCC lexes the operand of `__has_include` in an `#if` as a HEADER NAME, so
`<r273/*none>` is one token and the `/*` in it opens no comment. Gate 1b's
_c_phases() has no header-name state: it reads `/*` as a comment that runs
to the next `*/`. Put that `*/` behind a `//` on the next line and the gate
reads one directive line where GCC reads a directive, then a line of code:
the code is compiled by the product and blanked out of every text the gate
reads, the arm selections it compiles included.

usage: make_hi_cases.py <repo-root> <out.json>
"""
import json
from pathlib import Path
import sys

HIDE_OPEN = "#if !__has_include(<r273/*none>)\n"
HIDE_CLOSE = "#endif\n"


def hidden(line):
    """`line` (a statement, tab-indented, no newline) behind the header
    name: compiled by GCC, a comment to gate 1b."""
    return HIDE_OPEN + line + " // */\n" + HIDE_CLOSE


def once(text, old, new):
    assert text.count(old) >= 1, old
    return text.replace(old, new, 1)


def main():
    root, out = Path(sys.argv[1]), Path(sys.argv[2])
    fw = (root / "sw/firmware/milan_baremetal/milan_baremetal.c").read_text(
        encoding="utf-8")
    id_read = "\tuint32_t id = milan_read(MILAN_ID);\n"
    verdict = "\taem_loaded = load_aem_image();\n"
    uart_tail = "\tprint_tod(gettime_ns());\n}"
    forge = "\tid = MILAN_ID_MAGIC;"
    enable = "\tmilan_write(MILAN_ADP_CTRL, milan_read(MILAN_ADP_CTRL) | 1u);"
    poke = "\t*(volatile unsigned int *)0x90000600u = 1u;"
    cases = [
        {"label": "HI1 identity sample forged in milan_init() behind "
                  "`#if !__has_include(<r273/*none>)`, `*/` behind a //",
         "firmware": once(fw, id_read, id_read + hidden(forge))},
        {"label": "HI1q control: the same with the QUOTED header name "
                  "\"r273/*none\" (a string to the gate)",
         "firmware": once(fw, id_read, id_read + hidden(forge).replace(
             "<r273/*none>", "\"r273/*none\""))},
        {"label": "HI1p control: the same forgery under a plain `#if 1`",
         "firmware": once(fw, id_read,
                          id_read + "#if 1\n" + forge + "\n#endif\n")},
        {"label": "HI2 ADP enable in a UART command handler behind the "
                  "header name",
         "firmware": once(fw, uart_tail, hidden(enable) + uart_tail)},
        {"label": "HI2p control: the same enable in the handler, plain",
         "firmware": once(fw, uart_tail, enable + "\n" + uart_tail)},
        {"label": "HI3 literal-address cast store into the CSR window in a "
                  "UART command handler behind the header name",
         "firmware": once(fw, uart_tail, hidden(poke) + uart_tail)},
        {"label": "HI3p control: the same store, plain",
         "firmware": once(fw, uart_tail, poke + "\n" + uart_tail)},
        {"label": "HI4 AEM verdict overwritten after the verifier behind "
                  "the header name",
         "firmware": once(fw, verdict, verdict + hidden("\taem_loaded = 1;"))},
        {"label": "HI5 benign control: a printf in a UART command handler "
                  "behind the header name",
         "firmware": once(fw, uart_tail,
                          hidden("\tprintf(\"r273\\n\");") + uart_tail)},
    ]
    out.write_text(json.dumps(cases, indent=1) + "\n", encoding="utf-8")
    print(f"{len(cases)} cases -> {out}")


if __name__ == "__main__":
    main()
