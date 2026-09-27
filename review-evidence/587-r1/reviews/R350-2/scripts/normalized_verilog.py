#!/usr/bin/env python3
"""Reproduce the manifest's normalized_verilog_sha256 from a reviewer export.

usage: normalized_verilog.py GENERATED_V REVIEWER_REPO_ROOT AUTHOR_REPO_ROOT

The generated top embeds the checkout root in three ROM pathname parameters.
Substituting the author's published checkout root for the reviewer's, then
stripping block and line comments, must yield the committed digest.
"""
import hashlib
import re
import sys

path, mine, theirs = sys.argv[1:]
text = open(path).read()
print(f"reviewer_root_occurrences={text.count(mine)}")
text = text.replace(mine, theirs)
text = re.sub(r"/\*.*?\*/", "", text, flags=re.S)
text = re.sub(r"//[^\n]*", "", text)
print(f"normalized_sha256={hashlib.sha256(text.encode()).hexdigest()}")
