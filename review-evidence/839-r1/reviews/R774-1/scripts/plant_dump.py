#!/usr/bin/env python3
"""Probe leg: print every byte of the first two MSRP frames and the first MAAP/CRF frame the DUT sends."""
import sys
from pathlib import Path
p = Path(sys.argv[1])
t = p.read_text()
old = "    sent_.push_back(s);\n    frames_.push_back(tx_cur_);\n"
new = ("    {\n        static int dumped_msrp = 0;\n"
       "        if (s.kind == Kind::Msrp && dumped_msrp < 2) {\n"
       "            ++dumped_msrp;\n"
       "            printf(\"[DUMP] MSRP len %zu cycle %llu:\", tx_cur_.size(), static_cast<unsigned long long>(cyc_));\n"
       "            for (size_t i = 0; i < tx_cur_.size(); ++i) printf(\"%s%02x\", (i == 6 || i == 12) ? \" | \" : \"\", tx_cur_[i]);\n"
       "            printf(\"\\n\");\n        }\n    }\n" + old)
assert t.count(old) == 1
p.write_text(t.replace(old, new))
print("planted dump probe")
