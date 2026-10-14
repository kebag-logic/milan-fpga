#!/usr/bin/env bash
# R638-4: show that bash, make, python and xargs really execute each probe's hidden file.
# Usage: real_semantics.sh <empty scratch dir>
set -u
D=$1; mkdir -p "$D/sub" "$D/tools"; cd "$D"
cat > hidden.sh <<'EOF'
echo "HIDDEN-EXECUTED $0 $*" >> "${MARK:-/dev/stderr}"
EOF
cp hidden.sh sub/bootstrap.sh; echo 'echo root' > bootstrap.sh; chmod +x hidden.sh sub/bootstrap.sh bootstrap.sh
printf '#!/bin/sh\necho "HIDDEN-EXECUTED tools/git $*" >> "$MARK"\n' > tools/git; chmod +x tools/git
t(){ id=$1; shift; export MARK=$D/mark.$id; rm -f "$MARK"; ( eval "$@" ) >/dev/null 2>&1
  if [ -s "$MARK" ]; then echo "$id REAL-EXECUTES-HIDDEN: $(head -1 "$MARK" | sed "s#$D#<scratch>#g")"; else echo "$id hidden NOT executed"; fi; }
bash --version | head -1; make --version | head -1; python3 --version
t S2 "bash -c 'name=bootstrap.sh; printf -v name %s hidden.sh; bash \"\$name\"'"
t S3 "bash -c 'f=bootstrap.sh; read -r f <<< hidden.sh; bash \"\$f\"'"
echo 'name=hidden.sh' > fragS4.sh; t S4 "bash -c 'name=bootstrap.sh; source fragS4.sh; bash \"\$name\"'"
echo 'cd sub' > fragS5.sh; t S5 "bash -c 'source fragS5.sh; bash bootstrap.sh'"
t S7 "bash -c 'PATH=\"sub:\$PATH\" bootstrap.sh'"
t W5 "bash -c 'export PATH=\"tools:\$PATH\"; git rev-parse HEAD'"
echo 'echo okay' > step.sh
t W3 "BASH_ENV=hidden.sh bash --noprofile --norc -eo pipefail step.sh"
t W1 "bash hidden.sh step.sh"
printf 'SHELL := ./hidden.sh\nall:\n\techo okay\n' > M1.mk; t M1 "make -f M1.mk"
printf 'TOOL ?= echo\nall:\n\t$(TOOL) okay\n' > M2.mk; t M2 "TOOL=./hidden.sh make -f M2.mk"
printf 'all: sub/x\nsub/x:\n\tbash ./$(@D)/bootstrap.sh\n' > M3.mk; t M3 "make -f M3.mk"
mkdir -p m4/sub; printf 'all:\n\t$(MAKE) -C sub\n' > m4/Makefile; printf 'TOOL = echo\nall:\n\t$(TOOL) okay\n' > m4/sub/Makefile
t M4 "make -C m4 TOOL=$D/hidden.sh"
t X3 "echo hidden.sh | xargs bash"
echo "X1/X2 argv seen by the child: $(echo evilpkg | xargs echo python3 -m pip install)"
t Y1 "python3 -c 'import ctypes,os; ctypes.CDLL(None).system((\"sh \"+os.path.abspath(\"hidden.sh\")).encode())'"
t Y2 "python3 -c 'import os; getattr(os, \"system\")(\"sh hidden.sh\")'"
mkdir -p y3/firmware; : > y3/firmware/__init__.py
printf 'import subprocess\nsubprocess.run(["sh", "%s/hidden.sh"])\n' "$D" > y3/firmware/hidden.py
echo 'from firmware import hidden' > y3/bootstrap.py; t Y3 "cd y3 && python3 bootstrap.py"
