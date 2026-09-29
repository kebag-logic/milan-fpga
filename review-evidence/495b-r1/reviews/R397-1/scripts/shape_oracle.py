#!/usr/bin/env python3
"""Reviewer oracle for the #495 item 6 disposition (issue comment 5882165062).

Independent of the parser under review: written from the disposition text
without regular expressions, then compared with the builder's _mac48 and
_hex_text over structured and random spellings.

Usage: shape_oracle.py <tree> [--random N] [--seed S]
Prints every disagreement and a summary; exit 1 if any disagreement.
"""
from __future__ import annotations

import itertools
import random
import sys
from pathlib import Path

HEX = set("0123456789abcdefABCDEF")


def hex_body_digits(body: str) -> int | None:
    """Digit count of `body` if it is hex digits with single underscores
    strictly between two digits; None otherwise."""
    if not body:
        return None
    prev_us = True  # a leading underscore is refused
    count = 0
    for ch in body:
        if ch == "_":
            if prev_us:
                return None
            prev_us = True
        elif ch in HEX:
            count += 1
            prev_us = False
        else:
            return None
    if prev_us:  # trailing underscore
        return None
    return count


def hex_text_digits(text: str) -> int | None:
    """Optional 0x/0X then a hex body; the digit count or None.

    Ambiguity note: "0x..." is read with the prefix when that parse is
    legal; a bare body can never contain 'x', so there is only one parse.
    """
    if text[:2] in ("0x", "0X"):
        return hex_body_digits(text[2:])
    return hex_body_digits(text)


def oracle_mac_shape(text: str) -> bool:
    parts_colon, parts_dash = text.split(":"), text.split("-")
    for parts in (parts_colon, parts_dash):
        if len(parts) == 6 and all(len(p) == 2 and set(p) <= HEX for p in parts):
            return True
    return hex_text_digits(text) == 12


def oracle_hex_shape(text: str, bits: int) -> str:
    n = hex_text_digits(text)
    if n is None:
        return "shape"
    if n > bits // 4:
        return "width"
    return "ok"


def parser_mac_shape(eb, text: str) -> bool:
    try:
        eb._mac48(text, "f")
    except eb.ConfigError as exc:
        return "is not a MAC-48" not in str(exc)
    return True


def parser_hex_shape(eb, text: str, bits: int) -> str:
    try:
        eb._hex_text(text, bits, "f", "x")
    except eb.ConfigError as exc:
        return "width" if "outside" in str(exc) else "shape"
    return "ok"


def structured() -> list[str]:
    legal = ["02:00:00:00:00:02", "02-00-00-00-00-02", "020000000002",
             "0x020000000002", "0X0200_0000_0002", "02_00_00_00_00_02",
             "0x001BC50AC1000005", "0x91E0F000FE01", "123456", "0x0"]
    out = set(legal)
    ins = ["", " ", "\t", "\n", "\r", "\v", "\f", "\x00", " ", " ",
           "+", "-", "_", "__", ":", "-", "0x", "0X", "x", "0", "g", "٠",
           "０", "²", "\U0001d7ce", "0b", "#", ".", " 0x"]
    for s in legal:
        for i in range(len(s) + 1):
            for c in ins:
                out.add(s[:i] + c + s[i:])
        for i in range(len(s)):
            out.add(s[:i] + s[i + 1:])
            for c in ins:
                out.add(s[:i] + c + s[i + 1:])
    # every short/unpadded octet layout
    for lens in itertools.product((1, 2, 3), repeat=6):
        for sep in ":-_. ":
            out.add(sep.join("a" * n for n in lens))
    for sep in ":-":
        for k in (4, 5, 7):
            out.add(sep.join(["02"] * k))
    out |= {"", "0x", "0X", "_", "0x_", "0x0_", "0_x1", "00x1", "0xx1",
            "0x" + "0" * 12, "0" * 13, "0x" + "0" * 17, "0" * 16, "0" * 17,
            "0x1_2_3_4_5_6_7_8_9_a_b_c", "1-2-3-4-5-6", "01:23:45:67:89:ab:",
            ":01:23:45:67:89:ab", "01::23:45:67:89:ab", "0123:4567:89ab",
            "0123.4567.89ab", "01 23 45 67 89 ab", "0x01:23:45:67:89:ab",
            "01:23:45:67:89:AB", "01-23-45-67-89-ab", "01:23-45:67-89:ab"}
    return sorted(out)


def randoms(n: int, seed: int) -> list[str]:
    rng = random.Random(seed)
    alphabet = list("0123456789abcdefABCDEF") + ["x", "X", "_", ":", "-", " ",
                                                 "+", "\t", "\n", "g", "٠"]
    weights = [3] * 22 + [2, 1, 3, 3, 3, 1, 1, 1, 1, 1, 1]
    return ["".join(rng.choices(alphabet, weights, k=rng.randint(0, 20)))
            for _ in range(n)]


def main() -> int:
    tree = Path(sys.argv[1]).resolve()
    n = int(sys.argv[sys.argv.index("--random") + 1]) if "--random" in sys.argv else 200000
    seed = int(sys.argv[sys.argv.index("--seed") + 1]) if "--seed" in sys.argv else 495
    sys.path.insert(0, str(tree / "sw/builder"))
    import endstation_builder as eb  # noqa: E402
    spellings = structured() + randoms(n, seed)
    bad = 0
    accepted_mac = accepted_hex = 0
    for s in spellings:
        want, got = oracle_mac_shape(s), parser_mac_shape(eb, s)
        accepted_mac += got
        if want != got:
            bad += 1
            print(f"MAC DISAGREE {s!r}: oracle={'accept' if want else 'refuse'} "
                  f"parser={'accept' if got else 'refuse'}")
        for bits in (24, 32, 48, 64):
            want_h, got_h = oracle_hex_shape(s, bits), parser_hex_shape(eb, s, bits)
            accepted_hex += got_h == "ok"
            if want_h != got_h:
                bad += 1
                print(f"HEX{bits} DISAGREE {s!r}: oracle={want_h} parser={got_h}")
    print(f"spellings={len(spellings)} (structured={len(structured())}, random={n}, seed={seed}) "
          f"mac_shape_accepted={accepted_mac} hex_ok_verdicts={accepted_hex} disagreements={bad}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
