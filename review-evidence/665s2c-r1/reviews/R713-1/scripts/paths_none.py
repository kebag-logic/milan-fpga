"""Print each path's worst instance (ms, bound, verdict) from an archived table.md, for
comparing the README's 'none' and '4 KiB' columns. usage: paths_none.py TABLE [filter...]"""
import re
import sys
text = open(sys.argv[1]).read().split('\n\nComposed windows')[0]
for line in text.splitlines():
    m = re.match(r'^\| (.+?) \| (\d+) \| `[^`]+` \([^)]*\) \| ([^|]+) \| ([^|]+) \|', line)
    if m and (len(sys.argv) < 3 or any(f in line for f in sys.argv[2:])):
        print(' | '.join(x.strip() for x in m.groups()))
