#!/usr/bin/env python3
"""Scan the head's added lines and the PR body for host/path/address/serial shapes.
usage: privacy_scan.py <repo> <base> <head> <pr_body_file>"""
import re, subprocess, sys
repo, base, head, body = sys.argv[1:5]
added = [l[1:] for l in subprocess.run(['git', '-C', repo, 'diff', f'{base}..{head}'], capture_output=True, text=True).stdout.splitlines()
         if l.startswith('+') and not l.startswith('+++')]
texts = {'diff-added': '\n'.join(added), 'pr-body': open(body).read()}
pats = {'abs-path': r'(?<![\w.`])/(?:home|tmp|data|root|Users|opt|mnt|media|srv|var)/\S*', 'home-tilde': r'~/', 'ipv4': r'\b\d{1,3}(?:\.\d{1,3}){3}\b',
        'mac': r'\b[0-9a-fA-F]{2}(?::[0-9a-fA-F]{2}){5}\b', 'iface': r'\b(?:eth\d|enp\w+|eno\w+|wlp\w+|enx\w+)\b',
        'host-ish': r'\b[\w-]+\.(?:local|lan|home|internal)\b', 'usb-serial': r'\b(?:ttyUSB|ttyACM)\d', 'staging': r'a535/|/tmp/a5',
        'vendor-eid-oui': r'\b001b92\w*|\b001bc5\w*', 'placeholder': r'<[a-z-]+>'}
n = 0
for name, t in texts.items():
    for k, p in pats.items():
        for m in re.finditer(p, t):
            n += 1
            ln = t[:m.start()].count('\n') + 1
            print(f'{name}:{ln}: {k}: {m.group(0)!r}')
print('matches', n)
