# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""refusal.py - the grader's refusal, grade.Refusal, in a module of its own so the modules grade.py imports can raise
it without importing grade.py (channel_gate.py)."""


class Refusal(RuntimeError):
    """A log or a probe the grader cannot accept; the message names the rule."""
