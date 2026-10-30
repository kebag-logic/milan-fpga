#!/usr/bin/env python3
"""Classify every changed line of the bare-metal firmware between BASE and HEAD
as comment or code, list the code lines, and report whether any changed code line
stores to PP_CTRL or ADP_CTRL, or touches aem_loaded / entity_advertise's call.
Also extract both versions of the functions that write either enable bit and
compare them with their printf lines removed. Usage: REPO BASE"""
import re, subprocess, sys
repo, base = sys.argv[1], sys.argv[2]
F = 'sw/firmware/milan_baremetal/milan_baremetal.c'
diff = subprocess.run(['git', '-C', repo, 'diff', '-U0', base, 'HEAD', '--', F], capture_output=True, text=True, check=True).stdout
code = []
in_comment = False
for line in diff.splitlines():
    if line.startswith(('+++', '---', '@@')) or not line[:1] in '+-':
        continue
    body = line[1:].strip()
    is_comment = in_comment or body.startswith(('/*', '*', '//'))
    if '/*' in body and '*/' not in body: in_comment = True
    if '*/' in body: in_comment = False
    if not is_comment and body:
        code.append(line)
print('changed code lines:')
for c in code: print('  ', c)
bad = [c for c in code if re.search(r'MILAN_(PP|ADP)_CTRL|aem_loaded|entity_advertise\s*\(', c)]
print('changed code lines naming PP_CTRL/ADP_CTRL/aem_loaded/entity_advertise:', bad if bad else 'none')
def func(src, name):
    m = re.search(r'\n(static [^\n]*\b' + name + r'\([^)]*\)\n\{.*?\n\})', src, re.S)
    return m.group(1) if m else None
src_b = subprocess.run(['git', '-C', repo, 'show', f'{base}:{F}'], capture_output=True, text=True, check=True).stdout
src_h = open(f'{repo}/{F}').read()
for name in ('entity_advertise', 'configure_fabric', 'nvm_restore_walk', 'milan_init', 'load_aem_image'):
    b, h = func(src_b, name), func(src_h, name)
    strip = lambda s: '\n'.join(l for l in s.splitlines() if 'printf(' not in l)
    print(f'{name}: found base={b is not None} head={h is not None} identical_without_printf={b is not None and h is not None and strip(b) == strip(h)}')
for label, src in (('base', src_b), ('head', src_h)):
    sites = [(i + 1, l.strip()) for i, l in enumerate(src.splitlines()) if re.search(r'milan_write\(MILAN_(PP|ADP)_CTRL', l)]
    print(label, 'enable-register store sites:', sites)
