# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
#
#! The runner: one entry point, eight phases, unattended for days.
#!
#! Invariants it enforces so no phase has to:
#!
#!   * **No interactive prompt, ever.** Nothing here reads stdin.
#!   * **Every phase has a timeout, and so does every item.** A hung step fails
#!     THAT step (`SIGALRM` on the main thread) and the run moves on.
#!   * **Checkpoint after every item.** The cursor is written before the next
#!     item starts, so a crash resumes at the next one with NO arguments.
#!   * **Silence on success.** `STATUS` goes RUNNING -> DONE with nobody woken;
#!     the alert hook fires exactly once, on the first transition to FAILED.
#!   * **FAILED vs BLOCKED.** A defect in the device is FAILED. The harness
#!     unable to run an item - board unreachable, tool missing, registry absent
#!     - is BLOCKED: counted, reported, never alerted on.
#!   * **Bounded growth.** Free space is checked before each phase; the human
#!     log rotates and gzips; JSONL rotates per phase; per-item output is capped.

from __future__ import annotations

import signal
import threading
import time
import traceback
from dataclasses import dataclass, field
from pathlib import Path

from . import log as logmod
from . import registry as regmod
from .config import Config
from .csr import Csr, CsrError, SafetyViolation
from .notify import Notifier
from .recovery import NotKnownGood
from .transport import Outage, StepTimeout, Transport

#: Phase order. `--from` names one of these.
PHASES = ("baseline", "smoke", "validation", "counters", "matrix",
          "adversarial", "quality", "soak")


class ItemTimeout(Exception):
    pass


def _alarm(_sig, _frm):
    raise ItemTimeout("item exceeded its timeout")


@dataclass
class Ctx:
    """What every phase gets. Phases never touch the run directory directly."""
    cfg: Config
    run: logmod.RunDir
    transport: Transport
    registry: "regmod.Registry | None"
    registry_error: str
    boards: dict
    csrs: dict
    seed: int
    dry_run: bool
    only: str
    counters_path: Path
    stats: dict = field(default_factory=lambda: {
        "PASS": 0, "FAIL": 0, "BLOCKED": 0, "SKIP": 0, "INFO": 0})
    _first_failure: dict | None = None

    # ------------------------------------------------------------- recording
    def check(self, item: str, verdict: str, *, measured=None, detail="",
              kind="check", **extra) -> dict:
        rec = self.run.record(item=item, verdict=verdict, kind=kind,
                              measured=measured, detail=detail, **extra)
        self.stats[verdict] = self.stats.get(verdict, 0) + 1
        if verdict in (logmod.FAIL, logmod.BLOCKED):
            self.run.say(f"{verdict} {item}: {detail}", level=verdict)
        return rec

    def info(self, item: str, detail: str, measured=None, kind="info",
             **extra) -> dict:
        return self.check(item, logmod.INFO, measured=measured, detail=detail,
                          kind=kind, **extra)

    def blocked(self, item: str, why: str, **extra) -> dict:
        """The harness could not run it. Counted, reported, never alerted on."""
        return self.check(item, logmod.BLOCKED, detail=why, kind="blocked", **extra)

    def board(self, name: str):
        return self.boards[name]

    def csr(self, name: str) -> Csr:
        return self.csrs[name]

    @property
    def board_names(self) -> list[str]:
        return list(self.boards)


class Runner:
    def __init__(self, cfg: Config, *, run_dir: logmod.RunDir, dry_run: bool,
                 seed: int, transport_runner=None, from_phase: str = "",
                 only: str = "", phases: tuple[str, ...] = PHASES):
        self.cfg = cfg
        self.run = run_dir
        self.dry_run = dry_run
        self.seed = seed
        self.from_phase = from_phase
        self.only = only
        self.phases = phases
        self.notifier = Notifier(cfg, run_id=run_dir.rid)
        self.transport = Transport(cfg, on_outage=self._on_outage,
                                   runner=transport_runner)
        self._hb_stop = threading.Event()
        self._hb_thread: threading.Thread | None = None
        self._hb_state = {"phase": "init", "item": "", "iteration": 0}
        self.ctx: Ctx | None = None

    # -------------------------------------------------------------- lifecycle
    def _on_outage(self, info: dict) -> None:
        """A blip is a RECORD, not an abort. Days-long runs live through these."""
        self.run.record(item=self._hb_state.get("item", ""), verdict=logmod.INFO,
                        kind="outage", measured=info,
                        detail=f"{info['target']} unreachable "
                               f"(attempt {info['attempt']}, {info['outage_s']}s)")

    def _heartbeat_loop(self, every: float) -> None:
        while not self._hb_stop.wait(every):
            self.run.heartbeat(**self._hb_state)

    def _beat(self, **kw) -> None:
        self._hb_state.update(kw)
        self.run.heartbeat(**self._hb_state)

    # ------------------------------------------------------------------- main
    def execute(self) -> int:
        """Run the campaign. Returns a process exit code (0 = DONE)."""
        cfg = self.cfg
        self.run.set_status(logmod.STATUS_RUNNING, "starting")
        self.run.say(f"run {self.run.rid} starting (dry_run={self.dry_run}, "
                     f"seed={self.seed})")

        # An earlier FAILED in this same run directory means the alert already
        # went out; resuming must not re-alert.
        state, _reason = self.run.status()
        for rec in self.run.read_records():
            if rec.get("kind") == "alert":
                self.notifier.fired = True

        registry, registry_error = self._load_registry()
        boards = {b.name: b for b in cfg.boards}
        transport = self.transport
        ctx = Ctx(cfg=cfg, run=self.run, transport=transport, registry=registry,
                  registry_error=registry_error, boards=boards,
                  csrs={n: Csr(transport, b) for n, b in boards.items()},
                  seed=self.seed, dry_run=self.dry_run, only=self.only,
                  counters_path=Path(__file__).resolve().parent.parent
                  / "config" / "counters.toml")
        self.ctx = ctx

        ctx.info("harness", "run parameters", measured={
            "run_id": self.run.rid, "seed": self.seed, "dry_run": self.dry_run,
            "config": str(cfg.path), "phases": list(self.phases),
            "from_phase": self.from_phase, "only": self.only,
            "registry": (registry.tally() if registry else None),
            "registry_error": registry_error,
            "alert_configured": self.notifier.configured,
        })

        every = float(cfg.get("run", "heartbeat_secs", 15))
        self._hb_thread = threading.Thread(target=self._heartbeat_loop,
                                           args=(every,), daemon=True)
        self._hb_thread.start()

        cursor = self.run.load_cursor()
        start_at = 0
        if self.from_phase:
            if self.from_phase not in self.phases:
                raise SystemExit(f"--from: unknown phase {self.from_phase!r}")
            start_at = self.phases.index(self.from_phase)
        elif cursor.get("done_phases"):
            # Argument-free resume: continue after the last completed phase.
            done = [p for p in self.phases if p in cursor["done_phases"]]
            if done:
                start_at = self.phases.index(done[-1]) + 1
                self.run.say(f"resuming after completed phase {done[-1]!r} "
                             f"(cursor {self.run.cursor_path.name})")
                # Record WHAT was skipped: a resumed run must be as
                # reconstructable from its log as a fresh one.
                ctx.info("harness", f"resumed from the persisted cursor - "
                                    f"skipping {len(self.phases[:start_at])} "
                                    f"completed phase(s)", kind="resume",
                         measured={"skipped": list(self.phases[:start_at]),
                                   "continuing_at": self.phases[start_at]
                                   if start_at < len(self.phases) else None,
                                   "done_items": len(cursor.get("done_items", []))})

        try:
            for phase in self.phases[start_at:]:
                if phase in cursor.get("done_phases", []) and not self.from_phase:
                    ctx.info(phase, "phase already completed in this run - skipping",
                             kind="resume")
                    continue
                self._run_phase(ctx, phase)
        except KeyboardInterrupt:
            self.run.say("interrupted", level="WARN")
            self._finish(ctx, interrupted=True)
            return 130
        finally:
            self._hb_stop.set()

        return self._finish(ctx)

    # ------------------------------------------------------------------ phase
    def _run_phase(self, ctx: Ctx, phase: str) -> None:
        from . import phases as phasemod

        self.run.set_phase(phase)
        self._beat(phase=phase, item="", iteration=0)
        ok, free = self.run.check_disk()
        if not ok:
            ctx.blocked(phase, f"only {free} MB free, below run.min_free_disk_mb "
                               f"- refusing to start the phase and fill the disk")
            return
        budget = float(self.cfg.phase_timeouts.get(phase, 3600))
        deadline = time.monotonic() + budget
        ctx.info(phase, f"phase start (budget {budget:.0f}s, {free} MB free)",
                 kind="phase-start")
        fn = phasemod.PHASE_FUNCS.get(phase)
        if fn is None:
            ctx.blocked(phase, "no driver registered for this phase")
            return
        try:
            fn(ctx, PhaseClock(deadline, self))
        except Outage as exc:
            ctx.blocked(phase, f"bench unreachable during the phase: {exc}")
        except (NotKnownGood, SafetyViolation) as exc:
            self._fail(ctx, phase, str(exc))
        except Exception as exc:                      # noqa: BLE001 - last resort
            self._fail(ctx, phase, f"phase driver crashed: {exc}",
                       trace=traceback.format_exc())
        finally:
            self.run.mark_phase_done(phase)
            ctx.info(phase, "phase end", kind="phase-end",
                     measured=dict(ctx.stats))

    # ------------------------------------------------------------------- item
    def run_item(self, ctx: Ctx, phase: str, item: str, fn, *,
                 timeout: float | None = None, iteration: int = 0) -> str:
        """Run one item with its own timeout and its own checkpoint.

        Returns the verdict. Never raises: an item's failure is that item's
        verdict, which is the whole point of an unattended harness.
        """
        cursor = self.run.load_cursor()
        if f"{phase}/{item}" in cursor.get("done_items", []) and not self.only:
            ctx.check(item, logmod.SKIP, detail="already done in this run (cursor)",
                      kind="resume")
            return logmod.SKIP
        if self.only and item != self.only:
            return logmod.SKIP

        self._beat(phase=phase, item=item, iteration=iteration)
        tmo = float(timeout or self.cfg.phase_timeouts.get("item", 600))
        t0 = time.monotonic()
        prev = signal.signal(signal.SIGALRM, _alarm) if _can_alarm() else None
        if prev is not None:
            signal.setitimer(signal.ITIMER_REAL, tmo)
        try:
            verdict = fn() or logmod.PASS
        except ItemTimeout:
            verdict = logmod.FAIL
            ctx.check(item, logmod.FAIL, detail=f"timed out after {tmo:.0f}s",
                      measured={"timeout_s": tmo})
            self._maybe_first_failure(ctx, item, f"timed out after {tmo:.0f}s")
        except Outage as exc:
            verdict = logmod.BLOCKED
            ctx.blocked(item, f"bench unreachable: {exc}")
        except StepTimeout as exc:
            verdict = logmod.FAIL
            ctx.check(item, logmod.FAIL, detail=str(exc))
            self._maybe_first_failure(ctx, item, str(exc))
        except regmod.RegistryMissing as exc:
            verdict = logmod.BLOCKED
            ctx.blocked(item, str(exc))
        except (CsrError, SafetyViolation, NotKnownGood) as exc:
            verdict = logmod.FAIL
            ctx.check(item, logmod.FAIL, detail=str(exc))
            self._maybe_first_failure(ctx, item, str(exc))
        except Exception as exc:                      # noqa: BLE001
            verdict = logmod.FAIL
            ctx.check(item, logmod.FAIL, detail=f"runner crashed: {exc}",
                      measured={"traceback": traceback.format_exc()[-2000:]})
            self._maybe_first_failure(ctx, item, f"runner crashed: {exc}")
        finally:
            if prev is not None:
                signal.setitimer(signal.ITIMER_REAL, 0)
                signal.signal(signal.SIGALRM, prev)
            # Checkpoint AFTER the item, before the next one starts.
            self.run.mark_item_done(phase, item)
            self.run.say(f"{item}: {verdict} ({time.monotonic() - t0:.1f}s)")
        if verdict == logmod.FAIL:
            self._maybe_first_failure(ctx, item, "item reported FAIL")
        return verdict

    # ------------------------------------------------------------- escalation
    def _maybe_first_failure(self, ctx: Ctx, item: str, reason: str) -> None:
        """On the FIRST failure: FAILED, forensic bundle, one alert. Then stop
        escalating - a single defect must not produce a hundred messages."""
        if ctx._first_failure is not None:
            return
        ctx._first_failure = {"item": item, "reason": reason,
                              "ts": logmod.utc_now()}
        self.run.set_status(logmod.STATUS_FAILED, f"{item}: {reason}"[:200])
        bundle = self._forensics(ctx, item, reason)
        rec = self.notifier.alert_failed(item, reason)
        rec["bundle"] = str(bundle)
        self.run.record(item=item, verdict=logmod.INFO, kind="alert",
                        measured=rec, detail="first failure escalation")

    def _fail(self, ctx: Ctx, item: str, reason: str, trace: str = "") -> None:
        ctx.check(item, logmod.FAIL, detail=reason,
                  measured={"traceback": trace[-2000:]} if trace else None)
        self._maybe_first_failure(ctx, item, reason)

    def _forensics(self, ctx: Ctx, item: str, reason: str) -> Path:
        """Everything a diagnosis needs, captured once, standing alone."""
        payload = {
            "run": self.run.rid, "item": item, "reason": reason,
            "seed": self.seed, "phase": self._hb_state.get("phase"),
            "iteration": self._hb_state.get("iteration"),
            "config_path": str(self.cfg.path),
            "stats": dict(ctx.stats),
            "boards": {},
        }
        for name, csr in ctx.csrs.items():
            try:
                snap = csr.snapshot(timeout=120)
                payload["boards"][name] = {
                    "method": snap.method,
                    "registers": {k: f"0x{v:08X}" for k, v in
                                  sorted(snap.as_named().items())},
                }
            except Exception as exc:                  # noqa: BLE001
                payload["boards"][name] = {"error": str(exc)}
        return self.run.forensic_bundle(
            f"{item.replace('/', '_')}-{time.strftime('%H%M%S', time.gmtime())}",
            payload)

    # ------------------------------------------------------------------ finish
    def _finish(self, ctx: Ctx, *, interrupted: bool = False) -> int:
        from .report import write_report

        self.run.set_phase("report")
        path = write_report(ctx, self.run, interrupted=interrupted)
        self.run.say(f"report written: {path}")
        if ctx._first_failure:
            self.run.set_status(logmod.STATUS_FAILED,
                                f"{ctx._first_failure['item']}: "
                                f"{ctx._first_failure['reason']}"[:200])
            return 1
        if interrupted:
            self.run.set_status(logmod.STATUS_RUNNING, "interrupted - resumable")
            return 130
        blocked = ctx.stats.get(logmod.BLOCKED, 0)
        reason = "every item passed" if not blocked else \
            f"every item that could run passed ({blocked} blocked)"
        self.run.set_status(logmod.STATUS_DONE, reason)
        return 0

    # ---------------------------------------------------------------- registry
    def _load_registry(self):
        try:
            reg = regmod.load(self.cfg.items_path, self.cfg.items_overlay or None)
            return reg, ""
        except regmod.RegistryMissing as exc:
            self.run.say(f"item registry unavailable: {exc}", level="WARN")
            return None, str(exc)
        except regmod.RegistryError as exc:
            self.run.say(f"item registry unusable: {exc}", level="WARN")
            return None, str(exc)


@dataclass
class PhaseClock:
    """Lets a phase ask 'do I still have time?' without owning the timeout."""
    deadline: float
    runner: Runner

    @property
    def remaining(self) -> float:
        return max(0.0, self.deadline - time.monotonic())

    @property
    def expired(self) -> bool:
        return time.monotonic() >= self.deadline

    def item(self, ctx: Ctx, phase: str, item: str, fn, *, iteration: int = 0,
             timeout: float | None = None) -> str:
        if self.expired:
            ctx.blocked(item, "phase budget exhausted before this item started")
            return logmod.BLOCKED
        cap = min(self.remaining, float(timeout or 1e9)) or None
        return self.runner.run_item(ctx, phase, item, fn, timeout=cap,
                                    iteration=iteration)


def _can_alarm() -> bool:
    return (hasattr(signal, "SIGALRM")
            and threading.current_thread() is threading.main_thread())
