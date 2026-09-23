"""Find two-byte sequences whose surrogateescape decode/encode is not the identity."""
import itertools, sys
CODECS = sys.argv[1:] or ["utf-8", "latin-1", "ascii", "shift_jis", "cp932", "euc_jp",
          "euc_jis_2004", "shift_jis_2004", "big5", "big5hkscs", "gbk", "gb18030",
          "euc_kr", "cp949", "koi8_r", "cp1251", "iso8859_15", "tis_620"]
for name in CODECS:
    bad = []
    for a, b in itertools.product(range(256), repeat=2):
        raw = bytes((a, b))
        try:
            back = raw.decode(name, "surrogateescape").encode(name, "surrogateescape")
        except Exception as exc:
            bad.append((raw.hex(), type(exc).__name__)); continue
        if back != raw:
            bad.append((raw.hex(), back.hex()))
    print(f"{name}: {len(bad)} non-identity two-byte sequences; first: {bad[:4]}")
