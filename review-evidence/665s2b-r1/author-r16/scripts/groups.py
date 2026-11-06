#!/usr/bin/env python3
"""The group lists of this round's legs (#665): print one by name.

usage: groups.py backlog|windows|aged2|aged1|aged|subset
"""
import sys

PHASES, TICK_PHASES = ('blank', 'program', 'verify'), 8
backlog = ['backlog', 'backlog-adp', 'backlog-adp-refill', 'backlog-owed']
windows = [f'backlog-adp@{p}-{k}' for p in PHASES for k in range(TICK_PHASES)]
aged2 = [f'backlog-adp@{p}-aged2-{k}' for p in PHASES for k in range(TICK_PHASES)]
aged = [f'backlog-adp@{p}-aged{a}-{k}' for p in PHASES for a in (2, 1) for k in range(TICK_PHASES)]
aged1 = [f'backlog-adp@{p}-aged1-{k}' for p in PHASES for k in range(TICK_PHASES)]
saves = ['save', 'save-held', 'save-starved']
lists = dict(backlog=backlog, windows=windows, aged2=aged2, aged=aged, aged1=aged1,
             subset=backlog + windows + aged2 + saves)
print(','.join(lists[sys.argv[1]]))
