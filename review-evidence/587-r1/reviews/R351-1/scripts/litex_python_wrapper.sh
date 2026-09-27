#!/bin/bash
# Reviewer-private LiteX interpreter: host venv interpreter, private package copies first, no bytecode writes.
L=$REVIEWS/587-r351-1-packet/scratch/litex
export PYTHONDONTWRITEBYTECODE=1
export PYTHONPATH="$L/litex:$L/liteeth:$L/litedram:$L/litex-boards:$L/pythondata-cpu-vexiiriscv:$L/pythondata-software-picolibc:$L/pythondata-software-compiler_rt${PYTHONPATH:+:$PYTHONPATH}"
exec $HOME/litex-milan/venv/bin/python3 "$@"
