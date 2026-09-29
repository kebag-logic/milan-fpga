#!/usr/bin/env python3
"""Item 6 probe: what the builder's parsers do with every named spelling.

Run from sw/builder. Prints one line per spelling (accepted value or the
refusal) for the MAC table and, per hex field width, the hex table the named
tests use; the last line counts the acceptances. Always exits 0: it reports,
the named tests judge. mutate.py runs it at the head and with the builder
swapped to 51ca45c7 (restored afterwards).
"""
import endstation_builder as eb
import test_declarations as t

accepted = 0
for rule, spellings in t.MAC_SHAPE_REFUSALS:
    for spelling in spellings:
        try:
            got = f"accepted {eb._mac48(spelling, 'mac'):012X}"
            accepted += 1
        except eb.ConfigError as exc:
            got = f"refused: {exc}"
        print(f"MAC {rule}: {spelling!r} -> {got}")
for legal, bits in (("0x123456", 24), ("0x0205EA70", 32), ("0x91E0F000FE01", 48),
                    ("0x001BC50AC1000005", 64)):
    digits = legal.removeprefix("0x")
    cases = list(t._hex_shape_refusals(legal)) + [("past the width", "0x0" + digits),
                                                   ("past the width", "0" + digits)]
    for rule, spelling in cases:
        try:
            if bits == 48:
                value = eb._srp_dmac({"stream_dmac_base": spelling})
            elif bits == 64:
                value = eb._eui64(spelling, "hex")
            else:
                value = eb._declared_uint(spelling, bits, "hex")
            got = f"accepted {value:X}"
            accepted += 1
        except eb.ConfigError as exc:
            got = f"refused: {exc}"
        print(f"hex{bits} {rule}: {spelling!r} -> {got}")
print(f"ACCEPTED: {accepted}")
