#!/usr/bin/env python3
"""Stream equivalence of a head log with a round-1 log, ignoring only the new passive markers.

Usage: stream_equiv.py <round1.log> <head.log>
Reports: (a) line-based identity after dropping 'kind=ticks'/'kind=aem_read' EVENT lines;
(b) identity of the pre-existing EVENT lines (kind, cycle, fields); (c) identity of the UART
character stream with every EVENT line and its framing newlines removed.
"""
import re, sys
old, new = (open(p).read() for p in sys.argv[1:3])
lines = [l for l in new.splitlines() if not re.match(r'EVENT cycle=\d+ kind=(ticks|aem_read)\b', l)]
print('line-based identity:', lines == old.splitlines())
ev = lambda s: [l for l in s.splitlines() if l.startswith('EVENT ') and not re.match(r'EVENT cycle=\d+ kind=(ticks|aem_read)\b', l)]
print('pre-existing EVENT lines identical:', ev(old) == ev(new), len(ev(old)), len(ev(new)))
uart = lambda s: re.sub(r'\n?EVENT [^\n]*\n', '', s).replace('\n', '')
print('UART text (newlines ignored) identical:', uart(old) == uart(new), len(uart(old)))
