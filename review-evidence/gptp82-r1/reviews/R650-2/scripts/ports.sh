#!/bin/sh
# Print KL_gptp_engine's parameter and port header (module .. first ");"
# that closes the port list), comments stripped and whitespace collapsed,
# for a git revision. Usage: ports.sh REPO REV
git -C "$1" show "$2:hdl/top/KL_gptp_engine.sv" |
python3 -I -c '
import re,sys
t=sys.stdin.read()
t=re.sub(r"/\*.*?\*/","",t,flags=re.S)
t=re.sub(r"//[^\n]*","",t)
m=re.search(r"\bmodule\s+KL_gptp_engine\b(.*?)\)\s*;",t,flags=re.S)
s=m.group(1)
# the header ends at the first ");" after "(" of the port list
print(re.sub(r"\s+"," ",s).strip())'
