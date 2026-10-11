#!/bin/sh
exec $PACKET/scratch/rv32sdk/bin/riscv32-linux-gcc -fno-stack-protector "$@"
