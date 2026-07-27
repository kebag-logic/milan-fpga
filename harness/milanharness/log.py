# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
#
#! Run directory: structured logging, status, heartbeat, resume cursor.
#!
#! The contract this module implements:
#!
#!   * **A run is fully reconstructable from the logs alone.** Every check
#!     appends one JSONL record carrying item id, phase, verdict, the measured
#!     values and a timestamp. Nothing is kept only in memory.
#!   * **Append-only JSONL, rotated per phase.** Days of run produce large
#!     files; splitting by phase bounds each one without ever rewriting a
#!     record that was already written.
#!   * **The human log rotates and gzips.** Bounded growth on a days-long run.
#!   * **`STATUS` is the contract**, holding exactly one of RUNNING / FAILED /
#!     DONE plus a one-line reason. Everything else is detail.
#!   * **`heartbeat.json`** answers "is it still alive?" without reading a log.
#!   * **`cursor.json`** is the resume cursor: a crashed run continues at the
#!     next item, with no arguments.

from __future__ import annotations

import gzip
import json
import os
import shutil
import time
from dataclasses import dataclass
from pathlib import Path

STATUS_RUNNING = "RUNNING"
STATUS_FAILED = "FAILED"
STATUS_DONE = "DONE"

#: Verdicts. FAILED wakes a human; BLOCKED never does.
PASS = "PASS"
FAIL = "FAIL"
BLOCKED = "BLOCKED"
SKIP = "SKIP"
INFO = "INFO"

VERDICTS = (PASS, FAIL, BLOCKED, SKIP, INFO)


def utc_now() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def run_id(now: float | None = None, root: Path | None = None) -> str:
    """A fresh run id. Unique even for two runs started in the same second.

    The suffix matters: `--new` twice inside one second must not silently append
    to the previous run's directory and mix two campaigns' records.
    """
    base = time.strftime("run-%Y%m%d-%H%M%S", time.gmtime(now or time.time()))
    if root is None:
        return base
    root = Path(root)
    rid, n = base, 1
    while (root / rid).exists():
        n += 1
        rid = f"{base}-{n}"
    return rid


@dataclass
class Limits:
    human_log_max_bytes: int = 8 << 20
    human_log_keep: int = 40
    max_item_output_bytes: int = 256 << 10
    min_free_disk_mb: int = 512


class RunDir:
    """Owns everything written for one run.

    Instances are cheap and re-openable: resuming a crashed run is just
    constructing one on the same directory, which is why every writer here
    opens in append mode and no state is cached across calls that matters.
    """

    def __init__(self, root: Path, rid: str, limits: Limits | None = None):
        self.root = Path(root)
        self.rid = rid
        self.dir = self.root / rid
        self.limits = limits or Limits()
        self.jsonl_dir = self.dir / "jsonl"
        self.forensics_dir = self.dir / "forensics"
        for d in (self.dir, self.jsonl_dir, self.forensics_dir):
            d.mkdir(parents=True, exist_ok=True)
        self._phase = "init"
        self._seq = self._resume_seq()

    # ---------------------------------------------------------------- paths
    @property
    def status_path(self) -> Path:
        return self.dir / "STATUS"

    @property
    def heartbeat_path(self) -> Path:
        return self.dir / "heartbeat.json"

    @property
    def cursor_path(self) -> Path:
        return self.dir / "cursor.json"

    @property
    def human_path(self) -> Path:
        return self.dir / "harness.log"

    def jsonl_path(self, phase: str | None = None) -> Path:
        return self.jsonl_dir / f"{phase or self._phase}.jsonl"

    # ---------------------------------------------------------------- phase
    def set_phase(self, phase: str) -> None:
        self._phase = phase

    def _resume_seq(self) -> int:
        """Continue the global record sequence across a resume."""
        n = 0
        for p in sorted(self.jsonl_dir.glob("*.jsonl")):
            with p.open("r", encoding="utf-8", errors="replace") as fh:
                for _ in fh:
                    n += 1
        return n

    # --------------------------------------------------------------- record
    def record(self, *, item: str, verdict: str, kind: str = "check",
               measured: dict | None = None, detail: str = "",
               phase: str | None = None, **extra) -> dict:
        """Append ONE JSONL record. This is the authoritative run history."""
        if verdict not in VERDICTS:
            raise ValueError(f"unknown verdict {verdict!r}")
        self._seq += 1
        rec = {
            "ts": utc_now(),
            "mono": round(time.monotonic(), 3),
            "run": self.rid,
            "seq": self._seq,
            "phase": phase or self._phase,
            "item": item,
            "kind": kind,
            "verdict": verdict,
            "measured": measured or {},
            "detail": _cap(detail, self.limits.max_item_output_bytes),
        }
        rec.update(extra)
        path = self.jsonl_path(rec["phase"])
        with path.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(rec, sort_keys=True) + "\n")
            fh.flush()
            os.fsync(fh.fileno())
        return rec

    def read_records(self) -> list[dict]:
        """Every record of the run, in write order. Used by resume and report."""
        out: list[dict] = []
        for p in sorted(self.jsonl_dir.glob("*.jsonl")):
            with p.open("r", encoding="utf-8", errors="replace") as fh:
                for line in fh:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        out.append(json.loads(line))
                    except json.JSONDecodeError:
                        # A torn last line (power cut mid-write) must not make
                        # the whole run unreadable.
                        continue
        out.sort(key=lambda r: r.get("seq", 0))
        return out

    # ----------------------------------------------------------- human log
    def say(self, msg: str, level: str = "INFO") -> None:
        line = f"{utc_now()} {level:<7} [{self._phase}] {msg}\n"
        self._rotate_if_needed()
        with self.human_path.open("a", encoding="utf-8") as fh:
            fh.write(line)

    def _rotate_if_needed(self) -> None:
        try:
            size = self.human_path.stat().st_size
        except FileNotFoundError:
            return
        if size < self.limits.human_log_max_bytes:
            return
        stamp = time.strftime("%Y%m%d-%H%M%S", time.gmtime())
        gz = self.dir / f"harness.log.{stamp}.gz"
        with self.human_path.open("rb") as src, gzip.open(gz, "wb") as dst:
            shutil.copyfileobj(src, dst)
        self.human_path.write_text("")
        parts = sorted(self.dir.glob("harness.log.*.gz"))
        for old in parts[:-self.limits.human_log_keep]:
            old.unlink(missing_ok=True)

    # -------------------------------------------------------------- status
    def status(self) -> tuple[str, str]:
        try:
            txt = self.status_path.read_text(encoding="utf-8").strip()
        except FileNotFoundError:
            return ("", "")
        state, _, reason = txt.partition(" ")
        return (state, reason.strip())

    def set_status(self, state: str, reason: str = "") -> None:
        if state not in (STATUS_RUNNING, STATUS_FAILED, STATUS_DONE):
            raise ValueError(f"bad STATUS {state!r}")
        _atomic_write(self.status_path, f"{state} {reason}".strip() + "\n")

    # ----------------------------------------------------------- heartbeat
    def heartbeat(self, *, phase: str = "", item: str = "",
                  iteration: int = 0) -> None:
        _atomic_write(self.heartbeat_path, json.dumps({
            "timestamp": utc_now(),
            "epoch": int(time.time()),
            "phase": phase or self._phase,
            "item": item,
            "iteration": iteration,
            "pid": os.getpid(),
        }, sort_keys=True) + "\n")

    # -------------------------------------------------------------- cursor
    def load_cursor(self) -> dict:
        try:
            return json.loads(self.cursor_path.read_text(encoding="utf-8"))
        except (FileNotFoundError, json.JSONDecodeError):
            return {"done_phases": [], "done_items": [], "phase": "", "item": ""}

    def save_cursor(self, cursor: dict) -> None:
        _atomic_write(self.cursor_path, json.dumps(cursor, sort_keys=True) + "\n")

    def mark_item_done(self, phase: str, item: str) -> dict:
        c = self.load_cursor()
        key = f"{phase}/{item}"
        if key not in c["done_items"]:
            c["done_items"].append(key)
        c["phase"], c["item"] = phase, item
        self.save_cursor(c)
        return c

    def mark_phase_done(self, phase: str) -> dict:
        c = self.load_cursor()
        if phase not in c["done_phases"]:
            c["done_phases"].append(phase)
        self.save_cursor(c)
        return c

    # ------------------------------------------------------------- forensics
    def forensic_bundle(self, name: str, payload: dict,
                        tail_lines: int = 400) -> Path:
        """Capture on the FIRST failure only (the runner enforces the once-ness).

        Carries what a diagnosis actually needs: the failing item's inputs, the
        RNG seed, both boards' full CSR snapshots, and the tail of the human
        log - so the bundle stands alone even if the run keeps going.
        """
        d = self.forensics_dir / name
        d.mkdir(parents=True, exist_ok=True)
        _atomic_write(d / "failure.json",
                      json.dumps(payload, indent=2, sort_keys=True, default=str) + "\n")
        try:
            lines = self.human_path.read_text(encoding="utf-8",
                                              errors="replace").splitlines()
            _atomic_write(d / "harness.log.tail", "\n".join(lines[-tail_lines:]) + "\n")
        except FileNotFoundError:
            pass
        recs = self.read_records()[-tail_lines:]
        _atomic_write(d / "records.tail.jsonl",
                      "".join(json.dumps(r, sort_keys=True) + "\n" for r in recs))
        return d

    # ----------------------------------------------------------------- disk
    def free_mb(self) -> int:
        st = os.statvfs(self.dir)
        return int(st.f_bavail * st.f_frsize / (1 << 20))

    def check_disk(self) -> tuple[bool, int]:
        free = self.free_mb()
        return (free >= self.limits.min_free_disk_mb, free)


def _atomic_write(path: Path, text: str) -> None:
    tmp = path.with_suffix(path.suffix + ".tmp")
    with tmp.open("w", encoding="utf-8") as fh:
        fh.write(text)
        fh.flush()
        os.fsync(fh.fileno())
    os.replace(tmp, path)


def _cap(text: str, limit: int) -> str:
    if limit <= 0 or len(text) <= limit:
        return text
    keep = max(0, limit - 80)
    return text[:keep] + f"\n...[truncated {len(text) - keep} bytes by run.max_item_output_bytes]"


def latest_run(root: Path) -> str | None:
    """The most recent run id under `root`, or None. Drives argument-free resume."""
    root = Path(root)
    if not root.is_dir():
        return None
    runs = sorted((p.stat().st_mtime, p.name) for p in root.iterdir()
                  if p.is_dir() and p.name.startswith("run-"))
    return runs[-1][1] if runs else None
