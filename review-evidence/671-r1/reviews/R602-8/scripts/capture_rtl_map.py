"""Map dev's RTL delta onto the capture SoC's registered source lists, without importing LiteX.

Usage: python3 -I capture_rtl_map.py <repo-root> <base-rev> <dev-rev>
"""
import re
import subprocess
import sys
from pathlib import Path

root, base, dev = Path(sys.argv[1]), sys.argv[2], sys.argv[3]
names = subprocess.run(['git', '-C', str(root), 'diff', '--name-only', base, dev],
                       capture_output=True, text=True, check=True).stdout.split()
rtl = [n for n in names if re.search(r'\.(sv|svh|v|vh)$', n)]
soc = (root / 'sw/litex/milan_soc.py').read_text()


def literal_list(name):
    body = re.search(name + r' = \[(.*?)\n\]', soc, re.S).group(1)
    return set(re.findall(r'"([^"]+\.(?:sv|svh|v|vh))"', body))


dp, mbx = literal_list('_MILAN_DATAPATH_SOURCES'), literal_list('_CTRL_MAILBOX_SOURCES')
capture = (root / 'tb/verilator/nvm_capture_cpu/soc.py').read_text()
print('capture soc.py enables ctrl_mailbox:', 'ctrl_mailbox' in capture)
inside = 0
for n in rtl:
    where = 'datapath list (capture SoC)' if n in dp else 'ctrl mailbox list (opt-in)' if n in mbx else 'not registered'
    inside += n in dp
    print(f'{n}: {where}')
print(f'dev RTL files in the capture SoC datapath list: {inside} of {len(rtl)}')
