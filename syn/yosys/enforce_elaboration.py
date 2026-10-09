#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Restore converted elaboration errors as `$error` tasks (#651)."""
from __future__ import annotations

import argparse
from pathlib import Path
import re

# Newer converters lower elaboration errors to printable messages. Restore
# the task, leaving its generate condition intact: an inactive guard is legal.
# Native $error/$fatal tasks already fail in the synthesis frontend.
CONVERTED_GUARD = re.compile(r'\$display\s*(\(\s*"(?:Error|Fatal) \[elaboration\])')


def enforce(source: str) -> str:
    """Restore only converted error/fatal tasks; retain diagnostics and guards."""
    return CONVERTED_GUARD.sub(r'$error\1', source)


def main() -> None:
    """Rewrite the disposable input before synthesis or result-cache lookup."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source', type=Path)
    args = parser.parse_args()
    args.source.write_text(enforce(args.source.read_text(encoding='utf-8')), encoding='utf-8')


if __name__ == '__main__':
    main()
