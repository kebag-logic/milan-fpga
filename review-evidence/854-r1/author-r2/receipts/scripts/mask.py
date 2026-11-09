"""mask.py: the host-path and bench-identifier masks every receipt goes through (privacy rules of the assignment)."""
import re

MASK = (
    ('$HOME/litex-milan', '<litex>'), ('$VALIDATION_STORAGE/scratch/854-a756b', '<scratch>'), ('$VALIDATION_STORAGE/scratch/854-a756', '<round1-scratch>'),
    ('$VALIDATION_STORAGE/scratch', '<scratch-root>'), ('$VALIDATION_STORAGE/worktrees', '<worktrees>'),
    ('$LANES', '<lanes>'), ('$VALIDATION_TOOLS', '<tools>'), ('$VALIDATION_STORAGE', '<tmp-root>'),
    ('$HOME/milan-fpga-management', '<mgmt-root>'), ('$HOME/Xilinx', '<xilinx>'), ('$HOME', '<home>'),
    ('/tmp/milan-vivado', '<vivado-lock>'),
)
PATTERNS = (
    (re.compile(r'usb-Silicon_Labs_CP2102N[^\s"\']*'), '<console>'),
    (re.compile(r'210512180081'), '<cable>'),
    (re.compile(r'\bamx-pi\b'), '<power-host>'),
    (re.compile(r'\barchlinux\b'), '<host>'),
)


def mask(text):
    for a, b in MASK:
        text = text.replace(a, b)
    for pat, rep in PATTERNS:
        text = pat.sub(rep, text)
    return text
