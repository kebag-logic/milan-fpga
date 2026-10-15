#!/usr/bin/env python3
"""Replay of the R638-5 P3b-P7 and R639-5 make_target_override / traversal-cache forms at this head."""
import sys
from probe_lib import both, dump
H = 'brand_new_command'
both('P3b_leading_space_assignment', {'Makefile': f'CMD = echo ok\n CMD = {H} # note:\nall: ; $(CMD)\n'}, 'make')
both('P6b_bang_assignment', {'Makefile': f'X != {H} >&2; echo a:\nall: ; echo okay\n'}, 'make')
both('P4_builtin_implicit_rule', {'probe_builtin.c': 'int main(void){return 0;}\n',
     'Makefile': f'CC = {H} ; cc\nprobe_builtin: probe_builtin.c\n'}, 'make probe_builtin')
both('P5_implicit_dollar_less', {'benign.sh': 'echo okay\n', 'probe_evil.sh': f'{H}\n',
     'Makefile': 'probe.out: benign.sh\n%.out: %_evil.sh\n\tbash $<\n'}, 'make probe.out')
both('P7_redirected_pwd', {'zz_probe_cwd.py': f'import subprocess\nsubprocess.run(["{H}"])\n', 'scripts/zz_probe_cwd.py': 'VALUE = 1\n'},
     'cd "$(cd scripts && pwd > /dev/null)"; python3 zz_probe_cwd.py')
both('R639_make_target_override', {'benign.sh': 'echo okay\n', 'hidden.sh': f'{H}\n',
     'Makefile': 'all: SCRIPT=benign.sh\nall: ; bash $(SCRIPT)\n'}, 'make SCRIPT=hidden.sh')
both('R639_make_environment_memo', {'Makefile': 'TOOL ?= echo\nall: ; $(TOOL) okay\n'}, f'TOOL=echo make; TOOL={H} make')
both('R639_shell_script_environment_memo', {'bootstrap.sh': '"$TOOL" okay\n'}, f'TOOL=echo bash bootstrap.sh; TOOL={H} bash bootstrap.sh')
dump(sys.argv[1])
