#!/usr/bin/env python3
"""R425-5: public-text scan of the page, PR body, index row and commit message.

Usage: r425_5_pubscan.py <file>...
Generic, reviewer-side patterns only (no private list): network identities,
paths and device nodes, bench host roles named in the issue body, common
audio-interface/switch/instrument vendors and transports, wiring, channel-map,
capture-layout, clock-topology and stream-count wording. Prints file:line,
the pattern label and the matched token for each hit. Every pattern is first
checked against a planted line (power check).
"""
import re, sys

P = {
    'mac': r'\b[0-9a-fA-F]{2}(?:[:-][0-9a-fA-F]{2}){5}\b',
    'ipv4': r'\b(?:\d{1,3}\.){3}\d{1,3}\b',
    'path': r'(?:/home/|/dev/|/data/|/tmp/|~/|\bhw:\d)',
    'iface': r'\b(?:eth\d|enp\w+|eno\d|wlan\d|br\d|tap\d)\b',
    'bench-host': r'\b(?:pw0|pw1|ubuntu|build box|buildbox|beaglebone|raspberry)\b',
    'vendor': r'\b(?:motu|rme|focusrite|scarlett|presonus|behringer|steinberg|universal audio|apogee|'
              r'audient|antelope|ferrofish|merging|l-acoustics|<bench-switch-vendor-name>|meyer|avid|digico|yamaha|allen|'
              r'cisco|netgear|extreme|luminex|mellanox|intel|broadcom|realtek|marvell|microchip|'
              r'xmos|biamp|qsc|bss|tascam|zoom|roland|apple|macbook|linux|alsa|pipewire|jack)\b',
    'transport': r'\b(?:adat|s/pdif|spdif|aes3|aes/ebu|madi|toslink|optical|coax|xlr|bnc|word ?clock)\b',
    'wiring': r'\b(?:wired|cable[ds]?|patch(?:ed|ing)?|loopback|plugged|jack)\b',
    'channel-map': r'\b(?:channel map|capture channels? \d+|input \d+|inputs \d+|channels? \d+ (?:and|to) \d+ of the capture)\b',
    'clock-topology': r'\b(?:master clock|clock master|clock slave|follows? the (?:switch|capture)|clocked from|sync source|reference clock)\b',
    'peer-count': r'\b(?:\d+|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|sixteen|eighteen|\d+ of \d+) '
                  r'(?:peer )?(?:stream(?:s| states?| ports?)|clusters?)\b',
    'tool-name': r'\b(?:la_avdecc|hive|behave|wireshark|tshark|tcpdump|arecord|aplay|sox|ffmpeg)\b',
}
PLANT = {
    'mac': 'aa:bb:cc:dd:ee:ff', 'ipv4': '10.0.0.1', 'path': '<home-path>', 'iface': 'eth0',
    'bench-host': 'pw1', 'vendor': 'MOTU', 'transport': 'ADAT', 'wiring': 'cabled',
    'channel-map': 'channel map', 'clock-topology': 'word clock master clock',
    'peer-count': 'four clusters', 'tool-name': 'la_avdecc',
}
for k, rx in P.items():
    assert re.search(rx, PLANT[k], re.I), f'power check failed: {k}'
print(f'power check: {len(P)} of {len(P)} patterns hit their planted line')
total = 0
for f in sys.argv[1:]:
    for i, line in enumerate(open(f, encoding='utf-8').read().splitlines(), 1):
        for k, rx in P.items():
            for m in re.finditer(rx, line, re.I):
                total += 1
                print(f'{f}:{i}: {k}: {m.group(0)!r}')
print(f'{total} hits')
