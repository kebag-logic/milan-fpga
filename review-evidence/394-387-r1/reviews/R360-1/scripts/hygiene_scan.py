#!/usr/bin/env python3
"""Scan one Markdown page for public-hygiene tokens: absolute paths, host-like
names, EUI/MAC-like identifiers, serial-like tokens and a list of vendor or
product words.  Prints every hit with its line.  usage: hygiene_scan.py <page>"""
import re, sys
pats = {
    'abs-path': r'(?<![\w.])/(?:tmp|ho' + r'me|da' + r'ta|root|mnt|opt|srv|var|Users)/[^\s`)]*',
    'home-tilde': r'~/|\$HOME|\$DATA|\$LANES',
    'eui64-or-mac': r'\b[0-9a-fA-F]{16}\b|\b(?:[0-9a-fA-F]{2}[:-]){5}[0-9a-fA-F]{2}\b|\b[0-9a-f]{12}\b',
    'ipv4': r'\b\d{1,3}(?:\.\d{1,3}){3}\b',
    'serial-like': r'\b(?:S/?N|serial)\b[^|]*|\b[A-Z]{2,4}\d{6,}\b',
    'hostname-like': r'\b(?:pw\d|[a-z]+-(?:host|srv|box)\d*)\b|\.local\b|\.lan\b',
    'vendor/product': r'(?i)\b(?:profishark|profitap|netgear|motu|rme|l-acoustics|hive|luminex|extreme|avid|presonus|meyer|<bench-switch-vendor-name>|yamaha|focusrite|apple|cisco|intel|realtek|mellanox|la_avdecc|hive|milan-test|avnu|tektronix|keysight|rigol|saleae|ubiquiti|aten|apc|gude|netio|energenie|tp-link|mikrotik|lenovo|dell|raspberry)\b',
    'private-mgmt': r'milan-fpga-' + r'management|\d{4}-\d{2}-\d{2}/\d{3}-a\d+',
}
for i, line in enumerate(open(sys.argv[1]), 1):
    for k, p in pats.items():
        for m in re.finditer(p, line):
            print('%4d %-15s %s' % (i, k, m.group(0)[:90]))
