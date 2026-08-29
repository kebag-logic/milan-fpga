#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Shared first-party scope for the code-quality measurements and gates.

The shipping RTL spans this superproject and two project-owned submodules.
Git does not recurse into gitlinks for an ordinary ``git ls-files``, so every
quality rule uses this helper instead of silently treating those processors as
vendored code.  ``third_party`` and ``external`` remain upstream/vendor scope.
"""

import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
PROJECT_SUBMODULES = ("protocol-processor", "gptp-processor")


def _assert_pinned_submodules():
    """Refuse an absent or off-pin project submodule, with exit 2.

    A partial scan must never establish a smaller baseline.  ``git submodule
    status`` prefixes a healthy, checked-out pinned commit with one space; ``-``
    means absent, ``+`` means a different commit, and ``U`` means conflicted.
    Only the pinned HEAD is proved here: a working-tree edit inside a submodule
    that still sits at its pin is scanned as-is, which is what lets a reviewer
    inject a probe there and watch the gate see it.
    """
    run = subprocess.run(
        ["git", "submodule", "status", "--", *PROJECT_SUBMODULES],
        cwd=REPO, capture_output=True, text=True, check=True)
    rows = [line for line in run.stdout.splitlines() if line]
    if len(rows) != len(PROJECT_SUBMODULES) or any(line[0] != " " for line in rows):
        detail = "; ".join(rows) if rows else "no submodule status returned"
        # A named refusal with exit 2, not a traceback: the same shape the
        # lint and xvlog gates use. Exit 2 is "the population could not be
        # established", which no caller may read as a count of zero.
        print("REFUSED: project submodules must be initialized at their pinned "
              f"commits before a code-quality scan ({detail}); run `git submodule "
              "update --init protocol-processor gptp-processor`", file=sys.stderr)
        sys.exit(2)


def scoped_pathspecs(*patterns):
    """Return each superproject pathspec plus its two submodule equivalents."""
    out = list(patterns)
    for submodule in PROJECT_SUBMODULES:
        out.extend(f"{submodule}/{pattern}" for pattern in patterns)
    return out


def tracked(*patterns):
    """Tracked first-party paths across the superproject and project submodules."""
    _assert_pinned_submodules()
    run = subprocess.run(
        ["git", "ls-files", "--recurse-submodules", "--", *scoped_pathspecs(*patterns)],
        cwd=REPO, capture_output=True, text=True, check=True)
    return run.stdout.splitlines()
