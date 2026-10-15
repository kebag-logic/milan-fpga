#!/usr/bin/env python3
"""Reviewer-owned shell and extra Make probes, compared with the image's bash 5.2 / GNU Make 4.3."""
import os, sys
from probe_lib import both, dump

H = 'brand_new_command'
EVIL = f'{H}\n'
OK = 'echo okay\n'
both('S1_function_shadows_dirname',
     {'x/run.sh': OK, 'sub/run.sh': EVIL},
     'dirname() { echo sub; }\nbash "$(dirname x/run.sh)/run.sh"')
both('S2_function_shadows_cd_in_substitution',
     {'scripts/run.sh': OK, 'run.sh': EVIL},
     'cd() { :; }\nd="$(cd scripts && pwd)"\nbash "$d/run.sh"')
both('S3_function_shadows_pwd',
     {'scripts/run.sh': OK, 'sub/run.sh': EVIL},
     'pwd() { echo sub; }\nbash "$(cd scripts && pwd)/run.sh"')
both('S4_function_shadows_cd_statement',
     {'scripts/run.sh': OK, 'run.sh': EVIL},
     'cd() { :; }\ncd scripts\nbash run.sh')
both('S5_cd_dash_in_substitution',
     {'-/run.sh': OK, 'run.sh': EVIL},
     'bash "$(cd - && pwd)/run.sh"')
both('S6_realpath_function',
     {'x/run.sh': OK, 'sub/run.sh': EVIL},
     'realpath() { echo sub/run.sh; }\nbash "$(realpath x/run.sh)"')
both('S7_function_shadows_echo_command',
     {}, f'echo() {{ {H}; }}\necho okay')
both('S8_function_shadows_bash',
     {'run.sh': OK}, f'bash() {{ {H}; }}\nbash run.sh')
both('S9_alias_expansion_noninteractive',
     {'run.sh': OK}, f'shopt -s expand_aliases\nalias bash={H}\nbash run.sh')
both('S10_command_builtin_bypasses_function',
     {'scripts/run.sh': OK, 'run.sh': EVIL}, 'command cd scripts\nbash run.sh')
# Extra Make forms
both('M20_abspath_symlink_lexical',
     {'Makefile': 'all: ; bash $(abspath sub/link/../run.sh)\n', 'sub/run.sh': EVIL,
      'other/deep/.keep': '', 'other/run.sh': OK}, 'ln -s ../other/deep sub/link 2>/dev/null || true; make')
both('M21_recipe_function_shadow_via_make',
     {'Makefile': f'all: ; dirname() {{ echo sub; }}; bash "$$(dirname x/run.sh)/run.sh"\n',
      'x/run.sh': OK, 'sub/run.sh': EVIL}, 'make')
dump(sys.argv[1])
