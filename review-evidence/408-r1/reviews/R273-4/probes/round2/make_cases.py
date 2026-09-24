#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Reviewer probe cases for gate 1b (round R273-2 of PR #535).

Writes cases.json (whole firmwares handed to gate 1b's own
assert_boot_contract()) and spellings.json (texts handed to its own
lexer_keeps(), the reader the lexer corpus pins), both derived from the
firmware in --repo, so the same cases run against any revision.
"""

import argparse
import json
from pathlib import Path

SPLICE = "\\\n"
DIGRAPH_SPLIT = "%" + SPLICE + ":"          # `%:` with a splice between
DIGRAPH_SPLIT_SP = "%\\ \n:"                # the same, blank before newline


def once(text: str, old: str, new: str) -> str:
    assert text.count(old) == 1, old
    return text.replace(old, new)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    fw = (args.repo / "sw/firmware/milan_baremetal/milan_baremetal.c").read_text()

    tail = "\tmilan_write(MILAN_CRF_TX_CTRL, MILAN_CRF_TX_CTRL_BOOT);\n}\n"
    typedef = ("typedef struct { volatile uint32_t ctrl; } *r273_blk;\n\n"
               "static int aem_loaded;")
    store = "\t((r273_blk)0x90000600u)->ctrl = 1u;\n"

    def overlay(open_line: str, close_line: str) -> str:
        body = once(fw, "static int aem_loaded;", typedef)
        return once(body, tail, tail[:-2] + open_line + store + close_line + "}\n")

    cases = []

    def add(label: str, text: str) -> None:
        cases.append({"label": label, "firmware": text})

    add("C0 shipping firmware unchanged (must be ACCEPTED)", fw)
    add("C1 struct-overlay store to ADP_CTRL, unconditional", overlay("", ""))
    add("C2 same store in a plain `#ifdef CSR_UART_BASE` arm (product-only)",
        overlay("#ifdef CSR_UART_BASE\n", "#endif\n"))
    add("C3 same store, `#ifdef CSR_UART_BASE` behind a form feed (R272 F1 shape)",
        overlay("\f#ifdef CSR_UART_BASE\n", "\f#endif\n"))
    add("C4 same store, plain `%:ifdef` digraph (kept ban)",
        overlay("%:ifdef CSR_UART_BASE\n", "%:endif\n"))
    add("H1 same store, `%:` digraph SPLIT BY A SPLICE, #ifdef CSR_UART_BASE",
        overlay(DIGRAPH_SPLIT + "ifdef CSR_UART_BASE\n",
                DIGRAPH_SPLIT + "endif\n"))
    add("H2 same store, split digraph, #ifndef MILAN_CENSUS_SOC",
        overlay(DIGRAPH_SPLIT + "ifndef MILAN_CENSUS_SOC\n",
                DIGRAPH_SPLIT + "endif\n"))
    add("H3 same store, split digraph with a blank before the newline",
        overlay(DIGRAPH_SPLIT_SP + "ifdef CSR_UART_BASE\n",
                DIGRAPH_SPLIT_SP + "endif\n"))

    # The choke point's verdict test, `0 &&` in a product-only arm.
    verdict = "\tif (!verified)\n\t\treturn;\n"
    add("C5 `0 &&` in the verdict test under a plain #ifdef CSR_UART_BASE",
        once(fw, verdict, "\tif (\n#ifdef CSR_UART_BASE\n\t    0 &&\n#endif\n"
                          "\t    !verified)\n\t\treturn;\n"))
    add("H4 `0 &&` in the verdict test under a split-digraph #ifdef CSR_UART_BASE",
        once(fw, verdict, "\tif (\n" + DIGRAPH_SPLIT + "ifdef CSR_UART_BASE\n"
                          "\t    0 &&\n" + DIGRAPH_SPLIT + "endif\n"
                          "\t    !verified)\n\t\treturn;\n"))

    # A second definition of the identity magic (R273-1 F1(a) shape) ...
    magic = "#define MILAN_ID_MAGIC       0x4d494c4eu\n"
    second = "#define MILAN_ID_MAGIC (milan_read(MILAN_ID))\n"
    anchor = "static inline void milan_write(unsigned int offset, uint32_t value)\n"
    add("C6 second #define of MILAN_ID_MAGIC as a fresh read (plain `#`)",
        once(fw, anchor, second + "\n" + anchor))
    add("H5 same second definition spelled with a split `%:` digraph",
        once(fw, anchor, DIGRAPH_SPLIT + second[1:] + "\n" + anchor))
    assert magic in fw

    # ... a hidden #undef/#define pair retargeting a register name.
    add("H6 split-digraph #undef + #define retargeting MILAN_ADP_EID_LO to ADP_CTRL",
        once(fw, anchor, DIGRAPH_SPLIT + "undef MILAN_ADP_EID_LO\n"
             + DIGRAPH_SPLIT + "define MILAN_ADP_EID_LO 0x600u\n\n" + anchor))

    # A UTF-8 byte order mark: GCC skips it at the start of the file.
    add("B1 a byte order mark before the first line, nothing else",
        "﻿" + fw)
    add("B2 a byte order mark, then `#include <string.h>` on line 1",
        "﻿#include <string.h>\n" + fw)

    spellings = [
        {"label": "S1 `%:` split by a splice (ifdef FOO)",
         "text": "int a;\n" + DIGRAPH_SPLIT + "ifdef FOO\nint b;\n"
                 + DIGRAPH_SPLIT + "endif\nint z;\n"},
        {"label": "S2 `%:` split by a splice (ifndef FOO)",
         "text": "int a;\n" + DIGRAPH_SPLIT + "ifndef FOO\nint b;\n"
                 + DIGRAPH_SPLIT + "endif\nint z;\n"},
        {"label": "S3 `%:` split by a splice with a blank",
         "text": "int a;\n" + DIGRAPH_SPLIT_SP + "ifdef FOO\nint b;\n"
                 + DIGRAPH_SPLIT_SP + "endif\nint z;\n"},
        {"label": "S4 byte order mark then #ifdef FOO on line 1",
         "text": "﻿#ifdef FOO\nint b;\n#endif\nint z;\n"},
        {"label": "S5 `%:` split by a splice, #define FOO",
         "text": DIGRAPH_SPLIT + "define FOO\n#ifdef FOO\nint b;\n#endif\nint z;\n"},
        {"label": "S6 corpus control: a form feed before #",
         "text": "int a;\n\f#ifdef FOO\nint b;\n\f#endif\nint z;\n"},
    ]
    args.out.mkdir(parents=True, exist_ok=True)
    (args.out / "cases.json").write_text(json.dumps(cases, indent=1))
    (args.out / "spellings.json").write_text(json.dumps(spellings, indent=1))
    for spell in spellings:
        (args.out / (spell["label"].split()[0] + ".c")).write_bytes(
            spell["text"].encode("utf-8"))
    print(f"{len(cases)} cases, {len(spellings)} spellings -> {args.out}")


if __name__ == "__main__":
    main()
