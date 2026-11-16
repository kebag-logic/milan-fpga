import sys
# mkmut.py SRC OUT OLD NEW: OUT is SRC with the single occurrence of OLD replaced by NEW (refused unless exactly one)
src, out, old, new = sys.argv[1], sys.argv[2], sys.argv[3].encode().decode('unicode_escape'), sys.argv[4].encode().decode('unicode_escape')
text = open(src).read()
n = text.count(old)
if n != 1:
    sys.exit(f'anchor found {n} times')
open(out, 'w').write(text.replace(old, new))
