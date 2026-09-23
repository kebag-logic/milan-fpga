"""List Python codecs whose decode->encode does not return the input bytes.

Enumerates every 1- and 2-byte sequence; prints the first few witnesses and
the count per codec.  Used to pick a second non-injective filesystem codec,
independent of the Big5 witness the self-test already uses.
"""
import codecs, json, sys

CANDIDATES = ["big5", "big5hkscs", "cp950", "shift_jis", "cp932", "euc_jp",
              "euc_jis_2004", "shift_jis_2004", "euc_kr", "cp949", "gbk",
              "gb18030", "gb2312", "johab", "koi8_r", "cp1251", "iso8859_15",
              "tis_620", "cp1255", "euc_tw" ]
out = {}
for name in CANDIDATES:
    try:
        codecs.lookup(name)
    except LookupError:
        out[name] = "unavailable"
        continue
    witnesses = []
    count = 0
    seqs = [bytes([a]) for a in range(256)] + [bytes([a, b]) for a in range(0x80, 256) for b in range(256)]
    for seq in seqs:
        try:
            text = seq.decode(name)
        except UnicodeDecodeError:
            continue
        again = text.encode(name, "surrogateescape")
        if again != seq:
            count += 1
            if len(witnesses) < 3:
                witnesses.append([seq.hex(), again.hex(), [hex(ord(c)) for c in text]])
    out[name] = {"lossy": count, "witnesses": witnesses}
json.dump(out, sys.stdout, indent=1)
