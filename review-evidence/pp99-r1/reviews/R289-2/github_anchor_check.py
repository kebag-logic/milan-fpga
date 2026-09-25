#!/usr/bin/env python3
"""Independent GitHub-anchor check for markdown links (R289-2).

Usage: github_anchor_check.py CLONE [--online OWNER/REPO SHA] [--files F ...]

For every markdown link carrying a '#fragment' whose source is one of FILES
(default: every tracked .md) and whose target is a .md file, the fragment is
checked against two anchor sets of the target:

  offline: GitHub-style heading slugs (github-slugger rules: lowercase, drop
           everything that is not a letter, digit, mark, '_', '-' or space,
           spaces -> '-', duplicate slugs get -1, -2 ...) plus explicit
           id=/name= attributes in raw HTML.
  online:  the ids GitHub itself renders for the target at the exact SHA
           (contents API, rendered HTML media type; 'user-content-' prefix
           stripped). Read-only GET requests via `gh api`.

A link is dead if its fragment is missing from the set in force. Exit 1 on
any dead link, 0 otherwise. Controls (--control FRAG@TARGET) must be dead;
a control that resolves is reported and also yields exit 1.
"""
import argparse
import html
import os
import re
import subprocess
import sys
import unicodedata

LINK = re.compile(r'(?<!\!)\[(?:[^\]\[]|\[[^\]]*\])*\]\(\s*<?([^)\s>]*)>?(?:\s+"[^"]*")?\s*\)')
ID_ATTR = re.compile(r'<[a-zA-Z][^>]*?\b(?:id|name)\s*=\s*"([^"]+)"')
ATX = re.compile(r'^ {0,3}(#{1,6})[ \t]+(.*?)[ \t]*#*[ \t]*$')
FENCE = re.compile(r'^ {0,3}(```|~~~)')


def strip_inline(text):
    text = re.sub(r'`([^`]*)`', r'\1', text)
    text = re.sub(r'!?\[([^\]]*)\]\([^)]*\)', r'\1', text)
    text = re.sub(r'<[^>]+>', '', text)
    text = re.sub(r'(\*\*|__|\*)', '', text)
    return html.unescape(text)


def slug(text):
    out = []
    for ch in strip_inline(text).strip().lower():
        cat = unicodedata.category(ch)
        if ch in ' -_' or cat[0] in 'LNM':
            out.append('-' if ch == ' ' else ch)
    return ''.join(out)


def lines_outside_fences(path):
    fenced = False
    with open(path, encoding='utf-8') as fh:
        for no, line in enumerate(fh, 1):
            if FENCE.match(line):
                fenced = not fenced
                continue
            if not fenced:
                yield no, line.rstrip('\n')


def offline_anchors(path):
    ids, seen = set(), {}
    for _, line in lines_outside_fences(path):
        for m in ID_ATTR.finditer(line):
            ids.add(m.group(1))
        h = ATX.match(line)
        if h:
            s = slug(h.group(2))
            n = seen.get(s, 0)
            seen[s] = n + 1
            ids.add(s if n == 0 else f'{s}-{n}')
    return ids


_online_cache = {}


def online_anchors(repo, sha, relpath):
    key = relpath
    if key not in _online_cache:
        out = subprocess.run(
            ['gh', 'api', '-H', 'Accept: application/vnd.github.html',
             f'repos/{repo}/contents/{relpath}?ref={sha}'],
            capture_output=True, text=True, check=True).stdout
        ids = set()
        for m in re.finditer(r'\b(?:id|name)="([^"]+)"', out):
            v = html.unescape(m.group(1))
            ids.add(v[len('user-content-'):] if v.startswith('user-content-') else v)
        _online_cache[key] = (ids, out)
    return _online_cache[key][0]


def iter_links(path):
    for no, line in lines_outside_fences(path):
        code_free = re.sub(r'`[^`]*`', '', line)
        for m in LINK.finditer(code_free):
            url = m.group(1)
            if '#' not in url or re.match(r'^[a-z]+:', url):
                continue
            target, frag = url.split('#', 1)
            yield no, target, frag


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('clone')
    ap.add_argument('--online', nargs=2, metavar=('REPO', 'SHA'))
    ap.add_argument('--files', nargs='*')
    ap.add_argument('--control', action='append', default=[],
                    help='FRAG@TARGET_RELPATH that must NOT resolve')
    a = ap.parse_args()
    clone = os.path.abspath(a.clone)
    files = a.files
    if not files:
        files = subprocess.run(['git', '-C', clone, 'ls-files', '*.md'],
                               capture_output=True, text=True, check=True).stdout.split()
    checked = dead = 0
    for rel in files:
        src = os.path.join(clone, rel)
        for no, target, frag in iter_links(src):
            tpath = os.path.normpath(os.path.join(os.path.dirname(src), target)) if target else src
            trel = os.path.relpath(tpath, clone)
            if not trel.endswith('.md'):
                continue
            checked += 1
            if not os.path.exists(tpath):
                print(f'DEAD-FILE {rel}:{no} -> {trel}#{frag}')
                dead += 1
                continue
            off = frag in offline_anchors(tpath)
            on = None
            if a.online:
                on = frag in online_anchors(a.online[0], a.online[1], trel)
            ok = off and (on is not False)
            tag = 'OK  ' if ok else 'DEAD'
            print(f'{tag} {rel}:{no} -> {trel}#{frag} offline={off} online={on}')
            dead += not ok
    ctrl_bad = 0
    for c in a.control:
        frag, trel = c.split('@', 1)
        tpath = os.path.join(clone, trel)
        off = frag in offline_anchors(tpath)
        on = frag in online_anchors(a.online[0], a.online[1], trel) if a.online else None
        good = (not off) and (on is not True)
        print(f'CONTROL {"DEAD(expected)" if good else "RESOLVES(unexpected)"} {trel}#{frag} offline={off} online={on}')
        ctrl_bad += not good
    print(f'SUMMARY files={len(files)} checked={checked} dead={dead} controls={len(a.control)} control_failures={ctrl_bad}')
    return 1 if dead or ctrl_bad else 0


if __name__ == '__main__':
    sys.exit(main())
