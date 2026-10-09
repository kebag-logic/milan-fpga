#!/usr/bin/env python3
# Independent probes of scripts/check_comments.py check(); argv[1] = tree root.
import sys
sys.path.insert(0, sys.argv[1] + '/scripts')
import check_comments as cc
probes = {
    # name: (source, assembly, expected_refused)
    'plain prose': ('// narrative\n', False, True),
    'SPDX block rest': ('/* SPDX-License-Identifier: MIT\n   narrative */\n', False, True),
    'SPDX same-line prose': ('/* SPDX-License-Identifier: MIT */ /* narrative */\n', False, True),
    'splice after SPDX line': ('// SPDX-License-Identifier: MIT\\\nnarrative\n', False, True),
    'CRLF splice': ('// SPDX-License-Identifier: MIT\\\r\nnarrative\r\n', False, True),
    'asm prose line': ('# narrative\nnop\n', True, True),
    'asm trailing prose': ('nop # narrative\n', True, True),
    'asm C comment': ('nop /* narrative */\n', True, True),
    'if 0': ('#if 0\nnarrative\n#endif\n', False, True),
    'if 0 spaced': ('  #  if   0\nnarrative\n#endif\n', False, True),
    'if (0)': ('#if (0)\nx\n#endif\n', False, True),
    'if 0x0': ('#if 0x0\nx\n#endif\n', False, True),
    'elif 0': ('#if 1\n#elif 0\nnarrative\n#endif\n', False, True),
    'if 00 (octal zero)': ('#if 00\nnarrative\n#endif\n', False, True),
    'if false (C++)': ('#if false\nnarrative\n#endif\n', False, True),
    'C++14 digit separator masks comment': ("int a = 1'000; // narrative\nint b = 2'000;\n", False, True),
    'asm char constant masks comment': ("li a0, 'A\n# narrative\nli a1, 'B\n", True, True),
    'legit SPDX + copyright block': ('/* SPDX-FileCopyrightText: 2026 Kebag Logic\n * SPDX-License-Identifier: MIT\n */\n', False, False),
    'legit tracing': ('// REQ: ADP-01\n// Milan v1.2 5.5.3.5.36\n', False, False),
    'legit asm SPDX': ('# SPDX-License-Identifier: MIT\n.globl _start\n', True, False),
}
bad = 0
for name, (src, asm, refuse) in probes.items():
    got = bool(cc.check(src, asm))
    verdict = 'refused' if got else 'pass'
    ok = got == refuse
    bad += not ok
    print(f"{'OK ' if ok else 'GAP'} {name}: gate {verdict}, expected {'refused' if refuse else 'pass'}")
print('gaps:', bad)
