"""Print KL_gptp_engine's parameter and port declarations, comments removed."""
import re, sys
s = open(sys.argv[1], encoding="utf-8").read()
s = re.sub(r"/\*.*?\*/", "", s, flags=re.S)
s = re.sub(r"//[^\n]*", "", s)
m = re.search(r"module\s+KL_gptp_engine(.*?)\);", s, flags=re.S)
for line in m.group(1).splitlines():
    line = " ".join(line.split())
    if line:
        print(line)
