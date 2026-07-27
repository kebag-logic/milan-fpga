# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
#
#! The alert hook - fires ONCE, on the first transition to FAILED.
#!
#! Contract: `docs/testing/TESTING.md` section 6b. Field names (`alert_webhook`,
#! `alert_timeout_s`) and the POST shape follow that section exactly.
#!
#!   * **Silence on success is the requirement.** A notification nobody needed
#!     trains people to ignore the next one.
#!   * **`BLOCKED` never alerts.** Blocked means the harness could not run the
#!     item (board unreachable, tool missing) - not a defect. Waking someone for
#!     that is precisely the false alarm to avoid; blocked items are counted and
#!     reported instead.
#!   * **Exactly once.** A single defect must not produce a hundred overnight
#!     messages, so subsequent failures are recorded and do not re-alert.
#!   * **An undeliverable alert is a logging problem, never a test result.**
#!     `curl` is timeout-bounded, its exit status is recorded, and the campaign
#!     continues either way.
#!   * **Unset is a clean no-op**, not an error.

from __future__ import annotations

import shlex
import socket
import subprocess

#: Kept short enough to survive mobile truncation, and leading with the
#: actionable part (TESTING.md 6b).
MAX_BODY = 220


def build_body(item: str, reason: str, run_id: str,
               host: str | None = None) -> str:
    host = host or socket.gethostname()
    reason = " ".join(str(reason).split())
    body = f"milan campaign FAILED: {item} - {reason} (host {host}, run {run_id})"
    if len(body) > MAX_BODY:
        keep = MAX_BODY - len(f"milan campaign FAILED: {item} - ... (host {host}, run {run_id})")
        body = (f"milan campaign FAILED: {item} - {reason[:max(keep, 0)]}... "
                f"(host {host}, run {run_id})")
    return body


class Notifier:
    """One-shot alert dispatcher. Construct per run; `fired` survives a resume
    because the runner reloads it from the run's own records."""

    def __init__(self, cfg, *, run_id: str, runner=None):
        n = cfg.section("notify")
        self.webhook = str(n.get("alert_webhook", "") or "")
        self.timeout = int(n.get("alert_timeout_s", 10))
        self.command = list(n.get("alert_command", []) or [])
        self.run_id = run_id
        self.fired = False
        self._runner = runner or _run_argv

    @property
    def configured(self) -> bool:
        return bool(self.webhook or self.command)

    def alert_failed(self, item: str, reason: str) -> dict:
        """Fire the hook. Returns a record for the JSONL - always, never raises."""
        if self.fired:
            return {"sent": False, "why": "already alerted for this run",
                    "channels": []}
        self.fired = True
        body = build_body(item, reason, self.run_id)
        rec = {"sent": False, "body": body, "channels": [],
               "why": "no channel configured"}
        if not self.configured:
            return rec
        rec["why"] = ""
        if self.webhook:
            argv = ["curl", "-fsS", "--max-time", str(self.timeout),
                    "-X", "POST", "-H", "Content-Type: text/plain",
                    "--data", body, self.webhook]
            rc, err = self._runner(argv, self.timeout + 5)
            rec["channels"].append(
                {"kind": "webhook", "rc": rc, "err": err[:200],
                 "delivered": rc == 0,
                 # The endpoint itself is site information; the record proves a
                 # call happened without carrying the URL into the log.
                 "endpoint": "configured"})
            rec["sent"] = rec["sent"] or rc == 0
        for raw in ([self.command] if self.command else []):
            argv = list(raw) + [body]
            rc, err = self._runner(argv, self.timeout + 5)
            rec["channels"].append({"kind": "command", "rc": rc,
                                    "err": err[:200], "delivered": rc == 0,
                                    "argv": " ".join(shlex.quote(a) for a in raw)})
            rec["sent"] = rec["sent"] or rc == 0
        if not rec["sent"]:
            rec["why"] = ("every configured channel failed - recorded, campaign "
                          "continues (an alert that cannot be delivered is a "
                          "logging problem, not a test result)")
        return rec


def _run_argv(argv: list[str], timeout: int) -> tuple[int, str]:
    try:
        p = subprocess.run(argv, capture_output=True, text=True, timeout=timeout)
        return (p.returncode, p.stderr or "")
    except subprocess.TimeoutExpired:
        return (124, f"timed out after {timeout}s")
    except FileNotFoundError as exc:
        return (127, str(exc))
    except OSError as exc:                       # pragma: no cover - defensive
        return (1, str(exc))
