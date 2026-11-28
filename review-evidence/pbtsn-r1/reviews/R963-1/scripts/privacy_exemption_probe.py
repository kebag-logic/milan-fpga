#!/usr/bin/env python3
"""Probe: apply the base (79c4ba8) and head privacy commit rules to the exempted merges and to a
near-miss. Usage: privacy_exemption_probe.py OLD_MODULE_PATH NEW_MODULE_PATH REPO"""
import importlib.util, subprocess, sys

def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

old, new, repo = load(sys.argv[1], 'old'), load(sys.argv[2], 'new'), sys.argv[3]
for commit in ('d7e6a2a19a57a8277cd26042557a8c99f2ee5496', '5a07d9b7d87298f04b15aa28f0304ec88b0aef81'):
    lines = subprocess.check_output(['git', '-C', repo, 'show', '-s', '--format=%an <%ae>%n%cn <%ce>%n%B', commit]).decode().splitlines()
    print(commit[:8], 'base rule:', old.commit_errors(commit, lines) or 'pass', '| head rule:', new.commit_errors(commit, lines) or 'pass')
lines = subprocess.check_output(['git', '-C', repo, 'show', '-s', '--format=%an <%ae>%n%cn <%ce>%n%B', '5a07d9b7d87298f04b15aa28f0304ec88b0aef81']).decode().splitlines()
near = '5a07d9b7d87298f04b15aa28f0304ec88b0aef80'
print('near-miss hash with the same message, head rule:', new.commit_errors(near, lines) or 'pass')
foreign = ['someone <a@b.c>', 'someone <a@b.c>'] + lines[2:]
print('exempt hash with a foreign identity, head rule:', new.commit_errors('5a07d9b7d87298f04b15aa28f0304ec88b0aef81', foreign) or 'pass')
print('content scan of the exempt message, head rule:', new.scan('5a07d9b7', '\n'.join(lines).encode()) or 'clean')
