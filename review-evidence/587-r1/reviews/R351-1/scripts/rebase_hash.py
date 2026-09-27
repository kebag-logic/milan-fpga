#!/usr/bin/env python3
"""Hash a generated file after substituting the reviewer's roots with the executor's published roots.

Usage: rebase_hash.py FILE OLD=NEW [OLD=NEW ...]
The executor's checkout root is public in the issue's REVIEW READY comment.
"""
import hashlib, sys
data = open(sys.argv[1], "rb").read()
for pair in sys.argv[2:]:
    old, new = pair.split("=", 1)
    data = data.replace(old.encode(), new.encode())
print(hashlib.sha256(data).hexdigest(), len(data))
