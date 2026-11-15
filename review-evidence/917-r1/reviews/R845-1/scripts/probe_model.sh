#!/bin/sh
# Usage: probe_model.sh <clone> <probe_tests-root> <out-dir>: the reviewer probe checks (probe_tests.py's
# scratch suite copy) on the head host model, built with the Makefile's run-if2 model recipe at one interface.
set -eu
C=$1; T=$2/tb/verilator/mbx; O=$3; F=$C/sw/firmware/ctrl; S=$C/third_party/tsn-c-stack
mkdir -p $O
INC="-I$F/mbx -I$F/host -I$F/port -I$F/loop -I$F/adp -I$F/maap -I$F/acmp -I$F/app -I$S/include -I$C/sw/firmware/ctrl_nvm"
cc -std=c11 -O2 -Wall -Wextra -Werror -pedantic $INC -c $F/host/mbx_model.c -o $O/mbx_model.o
c++ -std=c++17 -O2 -Wall -Wextra -Werror -I$T -I$F/test $INC $T/model_main.cpp $O/mbx_model.o -o $O/Vmbx_model
$O/Vmbx_model
