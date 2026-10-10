#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Grade one raw MSRP MRPDU file with the reviewer decoder.
Usage: r587_grade_bin.py PDU.bin"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from r587_decode import decode, grade  # noqa: E402

d = open(sys.argv[1], "rb").read()
m, e, t = decode(d, 0x22EA)
lists = [(d[3] << 8) | d[4]] if len(d) > 4 else []
fv = [v["fv"] for _, vecs, _ in m for v in vecs if not v["la"]]
print(f"octets={len(d)} messages={len(m)} vectors={sum(len(v) for _, v, _ in m)} "
      f"first_list_length={lists} ascending={fv == sorted(fv)} grade={grade(m, e, t, 0x22EA) or 'OK'}")
