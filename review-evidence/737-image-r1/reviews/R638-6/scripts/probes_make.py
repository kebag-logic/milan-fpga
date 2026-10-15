#!/usr/bin/env python3
"""Reviewer-owned Make probes: each is compared with the image's GNU Make 4.3 by real_tools.sh."""
import sys
from probe_lib import both, dump

H = 'brand_new_command'
both('M1_else_prefixed_assignment_in_conditional',
     {'Makefile': f'ifeq (a,b)\nelseX = echo\nendif\nall: ; $(elseX) {H}\n'}, 'make')
both('M2_endif_prefixed_assignment_in_conditional',
     {'Makefile': f'ifeq (a,b)\nendifX = echo\nendif\nall: ; $(endifX) {H}\n'}, 'make')
both('M3_env_variable_append_flavor',
     {'Makefile': f'FOO += $(BAR)\nBAR = ; {H}\nall: ; $(FOO) okay\n'}, 'make', {'FOO': 'echo'})
both('M3b_env_variable_append_flavor_exported_shell',
     {'Makefile': f'FOO += $(BAR)\nBAR = ; {H}\nall: ; $(FOO) okay\n'}, 'export FOO=echo; make')
both('M4_call_zero_binding',
     {'Makefile': f'RUN = $(if $(0),,echo) {H}\nall: ; $(call RUN)\n'}, 'make')
both('M5_nested_call_argument_shadowing',
     {'Makefile': f'inner = $(if $(2),echo,{H}) okay\nouter = $(call inner,x)\nall: ; $(call outer,a,b)\n'}, 'make')
both('M6_target_specific_inheritance',
     {'Makefile': f'all: X = {H}\nall: dep ; @echo done\ndep: ; $(X) okay\n'}, 'make')
both('M7_tab_endef',
     {'Makefile': f'define X\necho a\n\tendef\nY = {H}\nendef\nall: ; $(X) $(Y)\n'}, 'make')
both('M8_wildcard_order',
     {'b.sh': f'{H}\n', 'a.sh': 'echo okay\n', 'Makefile': 'all: ; bash $(firstword $(wildcard *.sh))\n'}, 'make')
both('M9_if_unselected_branch',
     {'Makefile': f'all: ; $(if x,echo,$(shell {H})) okay\n'}, 'make')
both('M10_default_goal_after_rules',
     {'Makefile': f'first: ; echo okay\nsecond: ; {H}\n.DEFAULT_GOAL := second\n'}, 'make')
both('M11_commandline_recursive_override',
     {'Makefile': f'BAR = {H}\nall: ; $(FOO) okay\n'}, "make 'FOO=$(BAR)'")
both('M12_hash_inside_reference',
     {'Makefile': f'X := $(subst a,#,abc)\nall: ; echo $(X) ; {H}\n'}, 'make')
both('M13_override_after_target_variable_env',
     {'Makefile': f'all: TOOL = echo\nall: ; $(TOOL) okay\n'}, f'TOOL={H} make')
both('M14_empty_recipe_semicolon_then_tab',
     {'Makefile': f'all: ;\n\t{H}\n'}, 'make')
both('M15_conditional_rule_line',
     {'Makefile': f'ifeq (a,b)\nelse: ; echo\nendif\nall: ; echo okay\n'}, 'make')
both('M16_recipe_after_blank_and_comment',
     {'Makefile': f'all:\n\techo okay\n\n# c\n\t{H}\n'}, 'make')
both('M17_variable_named_like_directive_prefix_rule',
     {'Makefile': f'ifeq (a,b)\nelsewhere: ; {H}\nendif\nall: elsewhere ; echo okay\n'}, 'make')
both('M18_make_n_flag',
     {'Makefile': f'all: ; $(MAKE) -C sub\n', 'sub/Makefile': f'all: ; {H}\n'}, 'make -n')
both('M19_target_specific_on_second_rule_line',
     {'Makefile': f'X = echo\nall: dep\ndep: ; $(X) okay\nall: X = {H}\n'}, 'make')
dump(sys.argv[1])
